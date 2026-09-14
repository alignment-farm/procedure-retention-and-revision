from copy import deepcopy
from typing import Dict, List, Tuple
from collections import deque
import os
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch.nn import CrossEntropyLoss
import torch.nn.functional as F

from ...util import nethook
from ...util.generate import generate_fast

from .loki_hparams import LOKIHyperParams
import random
from .compute_ks import compute_ks
from .hsic import hsic_normalized_cca

CONTEXT_TEMPLATES_CACHE = None
COV_CACHE = {}
w_Ps = {}
rand_inds = {}

P_loaded = False
cache_c_new = False
memory_data = None

def apply_loki_to_model(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    requests: List[Dict],
    hparams: LOKIHyperParams,
    copy=False,
    return_orig_weights=False,
    keep_original_weight=False,
    **kwargs
) -> Tuple[AutoModelForCausalLM, List[str]]:

    global P, P_loaded, cache_c, cache_c_new, memory_data, w_Ps


    if not cache_c_new:
        # W_out = nethook.get_parameter(model, f"{hparams.rewrite_module_tmp.format(hparams.layers[-1])}.weight")
        # if "llama" in hparams.model_name.lower() or "qwen" in hparams.model_name.lower():
        #     cache_c = torch.zeros(( hparams.batch_size, W_out.shape[1]), device="cpu")
        # elif "gpt2-xl" in hparams.model_name.lower():
        #     cache_c = torch.zeros((len(hparams.layers), hparams.batch_size, W_out.shape[0]), device="cpu")
        # del W_out
        cache_c = [[] for _ in range(hparams.loss_layer)] 
        cache_c_new = True
    context_templates = get_context_templates(model, tok)


    

    
        # print(layer_ks.shape)
        # exit()
    # if memory_data is None:
    #     memory_data = get_ds()
    #     print("Num of memory data samples:", len(memory_data))
    #     exit()

    if copy:
        model = deepcopy(model)
    
    weights_copy = {}
    device = torch.device(f'cuda:{hparams.device}')

    # if not os.path.exists(hparams.P_loc):
    #     print(f"The null-space projection matrix P does not exist and now calculate.")
    #     W_out = nethook.get_parameter(model, f"{hparams.rewrite_module_tmp.format(hparams.layers[-1])}.weight")
    #     if "llama" in hparams.model_name.lower() or "gpt-j-6b" in hparams.model_name.lower():
    #         P = torch.zeros((len(hparams.layers), W_out.shape[1], W_out.shape[1]), device="cpu")
    #     elif "gpt2-xl" in hparams.model_name.lower():
    #         P = torch.zeros((len(hparams.layers), W_out.shape[0], W_out.shape[0]), device="cpu")
    #     del W_out
    #     for i, layer in enumerate(hparams.layers):
    #         P[i,:,:] = get_project(model, tok, layer, hparams)
    #     torch.save(P, "null_space_project.pt")
    #     P_loaded = True
    # elif P_loaded == False:
    #     P = torch.load(hparams.P_loc)
    #     P_loaded = True
    # P = P.to(device)

    # neuron_masks = get_ib_masks(model, tok, requests, hparams)

    deltas = execute_loki(model, tok, requests, hparams)

    with torch.no_grad():
        for w_name, upd_matrix in deltas.items():
            w = nethook.get_parameter(model, w_name)
            if return_orig_weights and w_name not in weights_copy:
                weights_copy[w_name] = w.detach().clone()

            w[...] += upd_matrix


    print(f"New weights successfully inserted into {list(deltas.keys())}")

    requests_k = deepcopy(requests)
    for i, request in enumerate(requests_k):
        if request["target_new"][0] != " ":
            # Space required for correct tokenization
            requests_k[i]["target_new"] = " " + request["target_new"]
        if '{}' not in request['prompt']:
            assert request['subject'] in request['prompt'] or \
                   print(f"Subject:{request['subject']} do not exist in prompt: {request['prompt']}")
        requests_k[i]['prompt'] = requests_k[i]['prompt'].replace(requests_k[i]['subject'], '{}')
        print(
            f"Caching LOKI algo for: "
            f"[{request['prompt']}] -> [{request['target_new']}]"
        )

    for i, layer in enumerate(hparams.layers):
        # print(context_templates)
        layer_ks = compute_ks(model, tok, requests_k, hparams, layer, context_templates)
        cache_c[layer].append(layer_ks.cpu())
    

    return model, weights_copy

def _extract_tensor(value, context=""):
    """
    Extract the first tensor from a potentially nested tuple/list structure.
    This handles cases where layer inputs/outputs are wrapped in tuples.
    For GPT-J and similar models, inputs can be nested tuples like ((hidden_states,), ...).
    
    Args:
        value: The value to extract tensor from (can be tensor, tuple, list, or BaseModelOutput)
        context: Optional context string for better error messages
    
    Returns:
        torch.Tensor: The extracted tensor
        
    Raises:
        ValueError: If no tensor can be extracted
    """
    if isinstance(value, torch.Tensor):
        return value
    elif isinstance(value, (tuple, list)):
        if len(value) == 0:
            raise ValueError(
                f"Empty tuple/list encountered when extracting tensor. {context}"
            )
        # For layer inputs, the first element is typically the hidden states tensor
        # For layer outputs, it might be wrapped differently
        first_elem = value[0]
        # Recursively extract from the first element
        result = _extract_tensor(first_elem, context=f"{context} (from first element)")
        if isinstance(result, torch.Tensor):
            return result
        # If first element didn't yield a tensor, try all elements
        for idx, item in enumerate(value):
            result = _extract_tensor(item, context=f"{context} (from element {idx})")
            if isinstance(result, torch.Tensor):
                return result
        # If we still don't have a tensor, raise an error with details
        raise ValueError(
            f"Could not extract tensor from tuple/list. {context}\n"
            f"Value type: {type(value)}, Length: {len(value)}\n"
            f"Element types: {[type(item) for item in value]}"
        )
    elif hasattr(value, 'last_hidden_state'):
        # Handle BaseModelOutput objects
        return value.last_hidden_state
    else:
        raise ValueError(
            f"Cannot extract tensor from type {type(value)}. {context}\n"
            f"Value: {value}"
        )


def _safe_extract_tensor(value, context="", default=None):
    """
    Safely extract tensor with fallback handling.
    
    Args:
        value: The value to extract tensor from
        context: Optional context string for better error messages
        default: Default value to return if extraction fails (None by default)
        
    Returns:
        torch.Tensor or default value
    """
    try:
        return _extract_tensor(value, context=context)
    except ValueError as e:
        if default is not None:
            return default
        raise

def compute_layer_ks(model, tok, texts, hparams, context_templates):
    layer_ks_inp, layer_ks_out = {}, {}
    OFFSET = int(hparams.layer_offset)
    with torch.no_grad():
        layers = [hparams.layer_module_tmp.format(0)] +\
            [hparams.rewrite_module_tmp.format(layer) for layer in range(OFFSET, hparams.loss_layer - OFFSET)] +\
                [hparams.layer_module_tmp.format(hparams.loss_layer)]
        for i, txt in enumerate(
            chunks(texts, hparams.batch_size)
        ):
            inputs = tok(txt, return_tensors="pt", padding=True).to(model.device)
            with nethook.TraceDict(
                module=model,
                layers=layers,
                retain_input=True,
                retain_output=True,
            ) as tr:
                model(**inputs)
            for l in layers:
                # Extract tensors from potentially nested tuple/list structures
                # This handles cases where GPT-J and other models wrap inputs/outputs in tuples
                input_raw = tr[l].input
                output_raw = tr[l].output
                
                # Handle empty input case (some layers may have empty inputs)
                # This can happen when inputs are passed as keyword arguments instead of positional
                if input_raw == () or (isinstance(input_raw, (tuple, list)) and len(input_raw) == 0):
                    # For empty inputs, use the previous layer's output as input
                    # This can happen for transformer layers in some model architectures (e.g., GPT-J)
                    layer_idx = layers.index(l)
                    if layer_idx > 0:
                        # Use previous layer's output as input
                        try:
                            prev_output = _extract_tensor(
                                tr[layers[layer_idx - 1]].output,
                                context=f"Previous layer {layers[layer_idx - 1]} output for layer {l}"
                            )
                            input_tensor = prev_output
                        except (ValueError, AttributeError) as e:
                            raise ValueError(
                                f"Layer {l} has empty input and failed to extract tensor from previous layer. "
                                f"Previous layer: {layers[layer_idx - 1]}"
                            ) from e
                    else:
                        # First layer with empty input - compute embeddings from input_ids
                        # For GPT-J and similar models, the first transformer block receives
                        # inputs via keyword args, so nethook captures empty tuple
                        # We need to compute the embeddings manually
                        if hasattr(model, 'transformer') and hasattr(model.transformer, 'wte'):
                            # GPT-J style: use word token embeddings
                            input_tensor = model.transformer.wte(inputs['input_ids'])
                        elif hasattr(model, 'transformer') and hasattr(model.transformer, 'word_embeddings'):
                            # Alternative embedding name
                            input_tensor = model.transformer.word_embeddings(inputs['input_ids'])
                        elif hasattr(model, 'embeddings'):
                            # Generic embeddings
                            input_tensor = model.embeddings(inputs['input_ids'])
                        else:
                            # Last resort: try to get from model's embed_tokens or similar
                            # This handles various model architectures
                            embed_attr = None
                            for attr in ['embed_tokens', 'wte', 'word_embeddings']:
                                if hasattr(model, attr):
                                    embed_attr = getattr(model, attr)
                                    break
                                elif hasattr(model, 'transformer') and hasattr(model.transformer, attr):
                                    embed_attr = getattr(model.transformer, attr)
                                    break
                            
                            if embed_attr is not None:
                                input_tensor = embed_attr(inputs['input_ids'])
                            else:
                                raise ValueError(
                                    f"Layer {l} (first layer) has empty input and cannot find embeddings layer. "
                                    f"Raw input: {input_raw}. "
                                    f"This may indicate an issue with layer tracing for this model architecture. "
                                    f"Model type: {type(model)}"
                                )
                else:
                    try:
                        input_tensor = _extract_tensor(
                            input_raw,
                            context=f"Layer {l} input"
                        )
                    except (ValueError, AttributeError) as e:
                        raise ValueError(
                            f"Failed to extract input tensor from layer {l}. "
                            f"Input type: {type(input_raw)}, Value: {input_raw}"
                        ) from e
                
                try:
                    output = _extract_tensor(
                        output_raw,
                        context=f"Layer {l} output"
                    )
                except (ValueError, AttributeError) as e:
                    raise ValueError(
                        f"Failed to extract output tensor from layer {l}. "
                        f"Output type: {type(output_raw)}, Value: {output_raw}"
                    ) from e
                
                # Safety check: ensure we have tensors
                if not isinstance(input_tensor, torch.Tensor):
                    raise TypeError(
                        f"Expected tensor for layer {l} input, got {type(input_tensor)}. "
                        f"Raw input type: {type(input_raw)}, value: {input_raw}"
                    )
                if not isinstance(output, torch.Tensor):
                    raise TypeError(
                        f"Expected tensor for layer {l} output, got {type(output)}. "
                        f"Raw output type: {type(output_raw)}, value: {output_raw}"
                    )
                
                if l not in layer_ks_inp:
                    layer_ks_inp[l] = [input_tensor.mean(dim=1)]
                    layer_ks_out[l] = [output.mean(dim=1)]
                else:
                    layer_ks_inp[l].append(input_tensor.mean(dim=1))
                    layer_ks_out[l].append(output.mean(dim=1))
        for l in layers:
            inp = torch.cat(layer_ks_inp[l], dim=0)
            out = torch.cat(layer_ks_out[l], dim=0)
            layer_ks_inp[l] = inp
            layer_ks_out[l] = out
    return layer_ks_inp, layer_ks_out

def compute_layer_hsics(layer_ks_inp, layer_ks_out, hparams):
    X_in = layer_ks_inp[hparams.layer_module_tmp.format(0)]
    X_out = layer_ks_out[hparams.layer_module_tmp.format(hparams.loss_layer)]
    scores = []
    OFFSET = int(hparams.layer_offset)
    for layer in range(OFFSET, hparams.loss_layer - OFFSET):
        X0 = layer_ks_inp[hparams.rewrite_module_tmp.format(layer)]
        if hparams.layer_hsic_type == 'subtract':
            hsic_score = hparams.hy * (hsic_normalized_cca(X_out, X0, sigma=hparams.hsigma)) - hparams.hx * hsic_normalized_cca(X0, X_in, sigma=hparams.hsigma)
        elif hparams.layer_hsic_type == 'ratio':
            hsic_score = hsic_normalized_cca(X_out, X0, sigma=hparams.hsigma)/hsic_normalized_cca(X0, X_in, sigma=hparams.hsigma)
        scores.append(hsic_score)
    _, top_ind = torch.topk(torch.Tensor(scores), k=hparams.num_layers, largest=True)
    hparams.layers = [l.item() + OFFSET for l in top_ind]

# bottom 5 layers hsic 'post': {'rewrite_acc': np.float64(0.93), 'rephrase_acc': np.float64(0.8649999999999999), 'locality': {'neighborhood_acc': np.float64(0.9700892857142858)}, 'portability': {'one_hop_acc': np.float64(0.5780952380952382)
# top 5 hsic layers 'post': {'rewrite_acc': np.float64(0.9349999999999999), 'rephrase_acc': np.float64(0.9550000000000001), 'locality': {'neighborhood_acc': np.float64(0.990625)}, 'portability': {'one_hop_acc': np.float64(0.4314285714285714)
# TODO try ratio/info added instead
def execute_loki(
    model: AutoModelForCausalLM,
    tok: AutoTokenizer,
    requests: List[Dict],
    hparams: LOKIHyperParams,
) -> Dict[str, Tuple[torch.Tensor]]:
    """
    Executes the LOKI update algorithm for the specified update at the specified layer
    Invariant: model at beginning of function == model at end of function
    """

    device = torch.device(f'cuda:{hparams.device}')
    # model = model.to(device)
    # Update target and print info
    requests = deepcopy(requests)
    for request in requests:
        if request["target_new"] != " ":
            # Space required for correct tokenization
            request["target_new"] = " " + request["target_new"]
        # print(
        #     f"Executing FT algo for: "
        #     f"[{request['prompt']}] -> [{request['target_new']}]"
        # )
    context_templates = get_context_templates(model, tok)

    rewrite_texts, kl_texts = [], []
    targets = []
    for request in requests:
        # target_ids = tok.encode(request["target_new"], return_tensors="pt", add_special_tokens=False).to(f"cuda:{hparams.device}")[0]
        rewriting_prompts, kl_prompts = [
            context.format(request["prompt"])
            for context_types in context_templates
            for context in context_types
        ], ["{} is a"]
        rewrite_texts.extend(rewriting_prompts)
        targets.extend([request["target_new"]] * len(rewriting_prompts))
        # all_prompts = rewriting_prompts + kl_prompts
    texts = rewrite_texts
    packed = list(zip(texts, targets))
    random.shuffle(packed)
    texts, targets = (list(t) for t in zip(*packed))

    layer_ks_inp, layer_ks_out = compute_layer_ks(model, tok, texts, hparams, context_templates)
    if hparams.dynamic_layer:
        compute_layer_hsics(layer_ks_inp, layer_ks_out, hparams)


    weights = {
        n: p
        for n, p in model.named_parameters()
        for layer in hparams.layers
        if hparams.rewrite_module_tmp.format(layer) in n
        and not n.endswith('.bias')  # Exclude bias parameters (1D tensors)
        and len(p.shape) >= 2  # Only include 2D+ weight matrices
    }

    # print(weights)
    opt = torch.optim.Adam(weights.values(), lr=hparams.w_lr)
    for name, w in model.named_parameters():
        w.requires_grad = name in weights
    
    

    # print(len(texts))
    # exit()
    # # print(list(zip(texts,targets)))
    # print(texts)
    # exit()
    # texts = [r["prompt"] for r in requests]
    # targets = [r["target_new"] for r in requests]
    kl_subjects = [r["subject"] for r in requests]

    weights_copy = {k: v.detach().clone() for k, v in weights.items()}
    # print(f"Weights to be updated: {list(weights.keys())}")
    for i, name in enumerate(weights):
        w = nethook.get_parameter(model, name)
        # Debug: check if w is a tensor with expected shape
        if not isinstance(w, torch.Tensor):
            raise TypeError(f"Parameter {name} is not a tensor, got {type(w)}: {w}")
        if len(w.shape) < 2:
            raise ValueError(
                f"Parameter {name} has unexpected shape {w.shape}. "
                f"Expected at least 2 dimensions for weight matrix."
            )
        # w_Ps[name] = P[i,:,:].to(device)
        w_P = get_project_w(w, hparams, cache_c[hparams.layers[i]])#, ks_only=True)#, layer_ks=layer_ks, layer_name=name)
        w_Ps[name] = w_P.to(device)
        d1 = w.shape[0]
        # print(w.shape)

    # f_masks = {}
    # f_noise = {}

    # for layer in hparams.layers:
    #     f_masks[hparams.layer_module_tmp.format(layer)] = torch.ones((d1), device=device) * 5
    #     f_masks[hparams.layer_module_tmp.format(layer)].requires_grad_() 
    #     f_noise[hparams.layer_module_tmp.format(layer)] = torch.randn((d1), device=device)
    # opt_masks = torch.optim.SGD(f_masks.values(), lr=hparams.w_lr * 100)
    
    # means_clean = {}
    # means_noisy = {}
    # covs_clean = {}
    # covs_noisy = {}
    # def edit_output_fn(cur_out, cur_layer):

    #     for name in f_masks.keys():
    #         if cur_layer == name:
    #             m = F.sigmoid(f_masks[name])
    #             vec = torch.mean(cur_out, dim=1)
    #             means_clean[name] = torch.mean(vec, dim=0)
    #             covs_clean[name] = torch.cov(vec.transpose(0,1))
    #             print(covs_clean[name].shape, means_clean[name].shape)
    #             print(cur_out.shape)
    #             exit()
    #             s = torch.std(cur_out, dim=2)[:,:,None].detach()
    #             means = torch.mean(cur_out, dim=2)
    #             # cov_clean[name] = torch.cov(cur_out.)
    #             # cur_out *= (m)
    #             # cur_out += (1 - m) * f_noise[name] 


    #     return cur_out

    kl_logits = []
    
    loss_meter = AverageMeter()
    opt_bs = 10
    for it in range(hparams.num_steps):
        print(20 * "=")
        print(f"Epoch: {it}")
        print(20 * "=")
        loss_meter.reset()
        # if it == 0:
        #     if type(hparams.norm_constraint) is float:
        #         eps = hparams.norm_constraint
        #         with torch.no_grad():
        #                 for name in weights:
        #                     w = nethook.get_parameter(model, name)
        #                     w[...] += torch.randn_like(w) * eps/5 * torch.linalg.norm(w)
        for i, (txt, tgt, subj) in enumerate(zip(
            chunks(texts, opt_bs), chunks(targets, opt_bs), chunks(kl_subjects, opt_bs)
        )):
            inputs = tok(txt, return_tensors="pt", padding=True).to(device)
            target_ids = tok(tgt, return_tensors="pt", padding=True)["input_ids"].to(
                device
            )
            kl_inp = tok(
                ["{} is a ".format(s) for s in subj],
                return_tensors="pt",
                padding=True,
            ).to(f"cuda:{hparams.device}")
            
            if it == 0:
                kl_logits.append(get_logits(kl_inp, model).detach())

            if hparams.objective_optimization == 'prompt_last':
                last_token_inds = inputs["attention_mask"].sum(dim=1) - 1
                if tok.unk_token_id is not None:
                    loss_mask = torch.ne(target_ids, tok.unk_token_id)
                else:
                    loss_mask = torch.ones_like(target_ids, dtype=torch.bool)
            elif hparams.objective_optimization == 'target_new':
                inputs_targets = [txt_ + tgt_ for txt_, tgt_ in zip(txt, tgt)]
                inputs_targets = tok(inputs_targets, return_tensors="pt", padding=True).to(device)
                num_prompt_toks = [int((i != tok.pad_token_id).sum()) for i in inputs['input_ids'].cpu()]
                num_pad_toks = [int((i == tok.pad_token_id).sum()) for i in inputs_targets['input_ids'].cpu()]
                prompt_len = [x + y for x, y in zip(num_pad_toks, num_prompt_toks)]
                prompt_target_len = inputs_targets['input_ids'].size(1)
                label_mask = torch.tensor([[False] * length + [True] * (prompt_target_len - length) for length in prompt_len]).to(device)
                # print(txt, tgt, label_mask, subj)
                # exit()
            else:
                print(f"{hparams.objective_optimization} has not been supported yet.")
                raise NotImplementedError

            opt.zero_grad()
            loss = calculate_loss(inputs, inputs_targets, target_ids, kl_inp, kl_logits[i], label_mask, model, hparams)
            # kl_loss = calc_kl_loss(inputs, inputs_targets, target_ids, label_mask, model, hparams)
            
            bs = inputs["input_ids"].shape[0]
            print(f"Batch loss {loss.item()}")
            loss_meter.update(loss.item(), n=bs)

            if loss.item() >= 1e-2:
                loss.backward()

                opt.step()
                with torch.no_grad():
                    for name in weights:
                        w = nethook.get_parameter(model, name)
                        delta = w - weights_copy[name]
                        V = w_Ps[name]
                        P = V @ V.T
                        delta = (delta @ P)
                        # angles = torch.abs((delta @ V))
                        # for i in range(delta.size(0)):
                        #     inds = torch.argsort(torch.abs(angles[i,:]).view(-1), dim=0, descending=True)[:8000]
                        #     P = V[:, inds] @ V[:, inds].T
                        #     delta[i, :] = (delta[i, :] @ P) #(torch.eye(delta.shape[-1]).to(w.device) - w_Ps[name]))#(delta @ 
                        w[...] = weights_copy[name] + delta
                        # # print(w.grad.data.shape, P.shape)
                        # w.grad.data = (w.grad.data @ w_Ps[name]).squeeze()

            if type(hparams.norm_constraint) is float:
                eps = hparams.norm_constraint
                # with torch.no_grad():
                #     for k, v in weights.items():
                #         v[...] = torch.clamp(
                #             v, min=weights_copy[k] - eps, max=weights_copy[k] + eps
                #         )
                with torch.no_grad():
                    for k, v in weights.items():
                        delta = v - weights_copy[k]
                        delta_norm = torch.norm(delta)
                        w_norm = torch.norm(weights_copy[k])
                        if delta_norm > eps * w_norm:
                            delta = (delta / delta_norm) * eps * w_norm
                            v[...] = weights_copy[k] + delta

        print(f"Total loss {loss_meter.avg}")

        if loss_meter.avg < 1e-2:
            break
    # print("Calculating Bottleneck mask...")
    # for it in range(hparams.num_steps):
    #     print(20 * "=")
    #     print(f"Epoch: {it}")
    #     print(20 * "=")
    #     loss_meter.reset()
    #     # if it == 0:
    #     #     if type(hparams.norm_constraint) is float:
    #     #         eps = hparams.norm_constraint
    #     #         with torch.no_grad():
    #     #                 for name in weights:
    #     #                     w = nethook.get_parameter(model, name)
    #     #                     w[...] += torch.randn_like(w) * eps/5 * torch.linalg.norm(w)
    #     for i, (txt, tgt, subj) in enumerate(zip(
    #         chunks(texts, opt_bs), chunks(targets, opt_bs), chunks(kl_subjects, opt_bs)
    #     )):
    #         inputs = tok(txt, return_tensors="pt", padding=True).to(device)
    #         target_ids = tok(tgt, return_tensors="pt", padding=True)["input_ids"].to(
    #             device
    #         )
    #         kl_inp = tok(
    #             ["{} is a ".format(s) for s in subj],
    #             return_tensors="pt",
    #             padding=True,
    #         ).to(f"cuda:{hparams.device}")
            

    #         if hparams.objective_optimization == 'prompt_last':
    #             last_token_inds = inputs["attention_mask"].sum(dim=1) - 1
    #             if tok.unk_token_id is not None:
    #                 loss_mask = torch.ne(target_ids, tok.unk_token_id)
    #             else:
    #                 loss_mask = torch.ones_like(target_ids, dtype=torch.bool)
    #         elif hparams.objective_optimization == 'target_new':
    #             inputs_targets = [txt_ + tgt_ for txt_, tgt_ in zip(txt, tgt)]
    #             inputs_targets = tok(inputs_targets, return_tensors="pt", padding=True).to(device)
    #             num_prompt_toks = [int((i != tok.pad_token_id).sum()) for i in inputs['input_ids'].cpu()]
    #             num_pad_toks = [int((i == tok.pad_token_id).sum()) for i in inputs_targets['input_ids'].cpu()]
    #             prompt_len = [x + y for x, y in zip(num_pad_toks, num_prompt_toks)]
    #             prompt_target_len = inputs_targets['input_ids'].size(1)
    #             label_mask = torch.tensor([[False] * length + [True] * (prompt_target_len - length) for length in prompt_len]).to(device)
    #         else:
    #             print(f"{hparams.objective_optimization} has not been supported yet.")
    #             raise NotImplementedError

    #         opt_masks.zero_grad()
    #         with nethook.TraceDict(
    #             module=model,
    #             layers=[
    #                 hparams.layer_module_tmp.format(layer) for layer in hparams.layers
    #             ],
    #             retain_input=False,
    #             retain_output=True,
    #             edit_output=edit_output_fn,
    #         ) as tr:
    #             loss = calculate_loss(inputs, inputs_targets, target_ids, kl_inp, kl_logits[i], label_mask, model, hparams) 
    #         print("Batch CE Loss:", loss.item())
    #         print("Mask L1 norms", sum([torch.linalg.norm(m, ord=1).item() for m in f_masks.values()]))
    #         for _, m in f_masks.items():
    #             loss_l1 = hparams.l1_lambda * torch.linalg.norm(m, ord=1)/len(f_masks)
    #             print(torch.autograd.grad(loss_l1, m, retain_graph=True))
    #             print(torch.autograd.grad(loss, m, retain_graph=True))
    #             print(m)
    #             print("="*50)
    #             # exit()
    #         loss += loss_l1
    #         loss.backward()
    #         opt_masks.step()

    deltas = {k: (weights[k] - weights_copy[k]).detach() for k in weights}

    # Restore state of original model
    with torch.no_grad():
        for k, v in weights.items():
            v[...] = weights_copy[k]

    print(f"Deltas successfully computed for {list(weights.keys())}")

    return deltas

def calculate_loss(inputs, inputs_targets, target_ids, kl_inp, kl_logits, label_mask, model, hparams):
    bs = inputs["input_ids"].shape[0]
    layers = [hparams.layer_module_tmp.format(hparams.loss_layer)] +\
             [hparams.rewrite_module_tmp.format(layer) for layer in hparams.layers] +\
             [hparams.layer_module_tmp.format(0)]
    with nethook.TraceDict(
                module=model,
                layers=layers,
                retain_input=True,
                retain_output=True,
            ) as tr:
        if 't5' in hparams.model_name.lower():
            inputs['decoder_input_ids'] = target_ids
            logits = model(**inputs).logits
            unmasked_log_probs = logits.log_softmax(-1).gather(-1, inputs['decoder_input_ids'].unsqueeze(-1)).squeeze(-1)

            mask = inputs['decoder_input_ids'] != -100
            n_tokens = mask.float().sum()
            avg_log_prob = (unmasked_log_probs * mask.float()).sum() / n_tokens
            nll = -avg_log_prob
            loss = nll
        elif 'chatglm' in hparams.model_name.lower():

            input_ids = inputs['input_ids'].tolist()
            labels = target_ids.tolist()
            assert len(input_ids) == len(labels)
            len_batches = [len(input_ids[i]) + len(labels[i]) + 1
                                for i in range(len(input_ids))]
            len_max_batch = max(len_batches)
            batch_input_ids = []
            batch_attention_mask = []
            batch_labels = []
            for x, y in zip(input_ids, labels):
                len_padding = len_max_batch - len(x) - len(y)
                if tok.padding_side and tok.padding_side == "left":
                    batch_label = [-100] * len_padding + [-100] * len(x) + y
                    batch_input_id = [0] * (len_padding) + x + y
                else:
                    batch_label = [-100] * len(x) + y + [-100] * len_padding
                    batch_input_id = x + y + [0] * (len_padding)

                # tensor_attention_mask = get_masks(batch_input_id, bos_token_id=64792)
                tensor_input_ids = torch.tensor(batch_input_id, dtype=torch.long)
                tensor_labels = torch.tensor(batch_label, dtype=torch.long)
                batch_input_ids.append(tensor_input_ids)
                # batch_attention_mask.append(tensor_attention_mask)
                batch_labels.append(tensor_labels)
            # batch_attention_mask = torch.stack(batch_attention_mask).to(device)
            batch_input_ids = torch.stack(batch_input_ids).to(device)
            batch_labels = torch.stack(batch_labels).to(device)
            # loss = model(input_ids=batch_input_ids, labels=batch_labels).loss
            lm_logits = model(input_ids=batch_input_ids)['logits']
            lm_logits = lm_logits.to(torch.float32)
            shift_logits = lm_logits[..., :-1, :].contiguous()
            shift_labels = batch_labels[..., 1:].contiguous()
            # Flatten the tokens
            loss_fct = CrossEntropyLoss(ignore_index=-100)
            loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
            loss = loss.to(lm_logits.dtype)
        else:
            if hparams.objective_optimization == 'prompt_last':
                probs = torch.nn.functional.log_softmax(
                    model(**inputs).logits[torch.arange(bs), last_token_inds], dim=-1
                )
                loss = -(torch.gather(probs, 1, target_ids) * loss_mask).sum(
                    1
                ) / loss_mask.sum(1)
                loss = loss.mean()
            elif hparams.objective_optimization == 'target_new':
                logits = model(**inputs_targets).logits
                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = inputs_targets['input_ids'][..., 1:].contiguous()
                loss_fct = CrossEntropyLoss(reduction='none')
                loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
                loss = loss.view(bs, -1)
                loss = (loss * label_mask[:,1:]).sum(1) / label_mask[:,1:].sum(1)
                loss = loss.mean()
            else:
                raise NotImplementedError
    hsic_loss = 0
    # Safely extract tensors with context for debugging
    # Handle empty input for first layer (layers[-1] is layer 0)
    f_first_raw = tr[layers[-1]].input
    if f_first_raw == () or (isinstance(f_first_raw, (tuple, list)) and len(f_first_raw) == 0):
        # First layer with empty input - compute embeddings from input_ids
        # This happens for GPT-J and similar models where inputs are passed as keyword args
        if hasattr(model, 'transformer') and hasattr(model.transformer, 'wte'):
            f_first = model.transformer.wte(inputs['input_ids']).mean(dim=1)
        elif hasattr(model, 'transformer') and hasattr(model.transformer, 'word_embeddings'):
            f_first = model.transformer.word_embeddings(inputs['input_ids']).mean(dim=1)
        elif hasattr(model, 'embeddings'):
            f_first = model.embeddings(inputs['input_ids']).mean(dim=1)
        else:
            # Try to find embeddings layer
            embed_attr = None
            for attr in ['embed_tokens', 'wte', 'word_embeddings']:
                if hasattr(model, attr):
                    embed_attr = getattr(model, attr)
                    break
                elif hasattr(model, 'transformer') and hasattr(model.transformer, attr):
                    embed_attr = getattr(model.transformer, attr)
                    break
            
            if embed_attr is not None:
                f_first = embed_attr(inputs['input_ids']).mean(dim=1)
            else:
                raise ValueError(
                    f"Layer {layers[-1]} (first layer) has empty input and cannot find embeddings layer. "
                    f"Raw input: {f_first_raw}. Model type: {type(model)}"
                )
    else:
        try:
            f_first = _extract_tensor(f_first_raw, context=f"layer {layers[-1]} input").mean(dim=1)
        except (ValueError, AttributeError) as e:
            raise ValueError(
                f"Failed to extract input tensor from layer {layers[-1]}. "
                f"Input type: {type(f_first_raw)}, Value: {f_first_raw}"
            ) from e
    
    try:
        output_0_raw = tr[layers[0]].output
        output_0 = _extract_tensor(output_0_raw, context=f"layer {layers[0]} output")
        f_last = output_0.mean(dim=1)
    except (ValueError, AttributeError) as e:
        raise ValueError(
            f"Failed to extract output tensor from layer {layers[0]}. "
            f"Output type: {type(output_0_raw)}, Value: {output_0_raw}"
        ) from e
    
    for l in layers[1:-1]:
        try:
            output_l_raw = tr[l].output
            output_l = _extract_tensor(output_l_raw, context=f"layer {l} output")
            f_layer = output_l.mean(dim=1)
        except (ValueError, AttributeError) as e:
            raise ValueError(
                f"Failed to extract output tensor from layer {l}. "
                f"Output type: {type(output_l_raw)}, Value: {output_l_raw}"
            ) from e
        # features hsic bneck
        hsic_loss += hparams.hx * (hsic_normalized_cca(f_first, f_layer, sigma=hparams.hsigma)) - hparams.hy * hsic_normalized_cca(f_layer, f_last, sigma=hparams.hsigma)
        # labels hsic bneck
        # hsic_loss += hparams.hx * (hsic_normalized_cca(f_first, f_layer, sigma=hparams.hsigma)) - hparams.hy * hsic_normalized_cca(f_layer, f_last, sigma=hparams.hsigma)
    # print(hsic_loss.item())
    # exit()
    kl_logits_now = get_logits(kl_inp, model)
    logprobs_now = F.log_softmax(kl_logits_now, dim=-1)
    logprobs_init = F.log_softmax(kl_logits, dim=-1)
    kl_div = F.kl_div(logprobs_init, logprobs_now, log_target=True, reduction='batchmean')
    loss += hparams.kl_factor * kl_div + hsic_loss
    
    return loss
#default first 300 'post': {'rewrite_acc': np.float64(0.9800000000000001), 'rephrase_acc': np.float64(0.8649999999999999), 'locality': {'neighborhood_acc': np.float64(0.9732142857142858)}, 'portability': {'one_hop_acc': np.float64(0.6523809523809523)}
# top 300 'post': {'rewrite_acc': np.float64(0.905), 'rephrase_acc': np.float64(0.93), 'locality': {'neighborhood_acc': np.float64(0.81875)}, 'portability': {'one_hop_acc': np.float64(0.5047619047619047)}}}
# top 300 mean after abs 'post': {'rewrite_acc': np.float64(0.93), 'rephrase_acc': np.float64(0.8899999999999999), 'locality': {'neighborhood_acc': np.float64(0.6891369047619048)}, 'portability': {'one_hop_acc': np.float64(0.5647619047619048)}}}
# bottom 300 'post': {'rewrite_acc': np.float64(0.93), 'rephrase_acc': np.float64(0.74), 'locality': {'neighborhood_acc': np.float64(0.9700892857142858)}, 'portability': {'one_hop_acc': np.float64(0.6523809523809523)}}}
# bottom 300 mean after abs 'post': {'rewrite_acc': np.float64(0.93), 'rephrase_acc': np.float64(0.7649999999999999), 'locality': {'neighborhood_acc': np.float64(0.984375)}, 'portability': {'one_hop_acc': np.float64(0.5714285714285714)}}}
# rand 300 'post': {'rewrite_acc': np.float64(0.93), 'rephrase_acc': np.float64(0.86), 'locality': {'neighborhood_acc': np.float64(0.9589285714285714)}, 'portability': {'one_hop_acc': np.float64(0.47904761904761894)}}}
# fixed rand 300 'post': {'rewrite_acc': np.float64(0.9550000000000001), 'rephrase_acc': np.float64(0.9099999999999999), 'locality': {'neighborhood_acc': np.float64(0.9700892857142858)}, 'portability': {'one_hop_acc': np.float64(0.619047619047619)}}}



def get_logits(inputs, model):
    logits = model(**inputs).logits
    return logits[:, -1, :]
    
def calc_kl_loss(inputs, inputs_targets, target_ids, label_mask, model, hparams):
    bs = inputs["input_ids"].shape[0]
    logits = model(**inputs_targets).logits
    shift_logits = logits[..., :-1, :].contiguous()
    shift_labels = inputs_targets['input_ids'][..., 1:].contiguous()
    # print(inputs["input_ids"].shape, inputs_targets['input_ids'].shape, target_ids.shape, shift_logits.shape, logits.shape, shift_labels.shape)
    # exit()

def upd_matrix_match_shape(matrix: torch.Tensor, shape: torch.Size) -> torch.Tensor:
    """
    GPT-2 and GPT-J have transposed weight representations.
    Returns a matrix that matches the desired shape, else raises a ValueError
    """

    if matrix.shape == shape:
        return matrix
    elif matrix.T.shape == shape:
        return matrix.T
    else:
        raise ValueError(
            "Update matrix computed by ROME does not match original weight shape. "
            "Check for bugs in the code?"
        )


def get_context_templates(model, tok):
    global CONTEXT_TEMPLATES_CACHE

    if CONTEXT_TEMPLATES_CACHE is None:
        CONTEXT_TEMPLATES_CACHE = [["{}"]] + [
            [
                f.replace("{", " ").replace("}", " ") + ". {}"
                for f in generate_fast(
                    model,
                    tok,
                    ["The", "Therefore", "Because", "I", "You"],
                    n_gen_per_prompt=n_gen // 5,
                    max_out_len=length,
                )
            ]
            for length, n_gen in [(10, 5)]  # Be careful about changing this.
        ]
        print(f"Cached context templates {CONTEXT_TEMPLATES_CACHE}")

    return CONTEXT_TEMPLATES_CACHE



def chunks(arr, n):
    """Yield successive n-sized chunks from arr."""
    chunk = []
    for a in arr:
        chunk.append(a)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if len(chunk) > 0:
        yield chunk

class AverageMeter:
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def get_project_w(w, hparams, ks=None, ks_only=False, layer_ks=None, layer_name=None, rand=False):
    force_recompute = False
    # Ensure w is a tensor and extract from tuple if needed
    if isinstance(w, (tuple, list)):
        # If w is a tuple/list, try to extract the tensor
        w = _extract_tensor(w)
    elif not isinstance(w, torch.Tensor):
        raise TypeError(f"Expected tensor for weight parameter, got {type(w)}: {w}")
    
    # Ensure w has at least 2 dimensions
    if not hasattr(w, 'shape') or len(w.shape) < 2:
        raise ValueError(
            f"Weight parameter must have at least 2 dimensions, got shape: {w.shape if hasattr(w, 'shape') else 'no shape attribute'}. "
            f"Parameter type: {type(w)}"
        )
    
    d1, d2 = w.shape[0], w.shape[1]
    ind_null = d1
    if ks is not None and len(ks) > 0:
        ks = torch.concat(ks, dim=0).to(w.device)
        ind_null += ks.size(0)
        if ks_only:
            w_exp = ks
        else:
            w_exp = torch.concat((w, ks), dim=0)
        # print(w_exp.shape)
    else:
        w_exp = w
    U, S, V = torch.linalg.svd(w_exp, full_matrices=True)
    V = V.T
    # indices = torch.randperm(V.size(1) - ind_null)[:500] + ind_null
    # print(U.shape, V.shape, ind_null)
    # print(S.shape, ind_null)
    # print( S[ind_null:].sum(), S[ind_null])
    # exit()
    if layer_ks==None:
        V = V[:, ind_null:ind_null + hparams.null_dim]
    else:
        with torch.no_grad():
            # X1 = layer_ks[layer_name.replace(".weight","")].clone().to(w.device).mean(dim=0)
            # scores = torch.abs(X1 @ V[:, ind_null:])
            # # print(X1.shape, scores.shape)
            # _, max_ind = torch.topk(scores, k=hparams.null_dim, sorted=False, largest=False)
            if layer_name not in rand_inds:
                max_ind = torch.randperm(d2 - d1 - 10)[:hparams.null_dim]
                rand_inds[layer_name] = max_ind
            else:
                max_ind = rand_inds[layer_name]
            V = V[:, d1 + 10 + max_ind]
        #hsic
        # P = torch.ones((d2 - ind_null,),  device=w.device, dtype=w.dtype, requires_grad=True)#torch.randint(0,2,(d2,), device=w.device, dtype=w.dtype, requires_grad=True)
        # opt_P = torch.optim.Adam([P], lr=5)
        # X1 = layer_ks[layer_name.replace(".weight","")].clone().to(w.device).transpose(0,1)
        # O = layer_ks[hparams.rewrite_module_tmp.format(hparams.loss_layer)].clone().to(w.device).transpose(0,1)
        # V_c = V[:, ind_null:].clone().detach()
        # for it in range(10):
        #     opt_P.zero_grad()
        #     X2 = V_c @ torch.diag(P) @ V_c.T @ X10
        #     loss = (hsic_normalized_cca(X1.T, X2.T, sigma=5) - hsic_normalized_cca(X2.T, O.T, sigma=5))
        #     # print(loss)
        #     loss.backward()
        #     print(P.grad.abs().topk(k=10)[0])
        #     # exit()
        #     print(loss)
        #     opt_P.step()
        #     if (it) % 3 == 0:
        #         with torch.no_grad():
        #             _, max_ind = torch.topk(P, k=300)
        #             # print(max_ind)
        #             P[:] = 0
        #             P[max_ind] = 1
        # print('=======================')
        # max_ind += ind_null
        # V = V[:, max_ind]
            

    # print(V @ V.T)
    # threshold = hparams.nullspace_threshold * 10
    # assert hparams.svd_quantile < 1.0 and hparams.svd_quantile > 0.0, "svd_quantile should be between 0 and 1."
    # q = torch.tensor(hparams.svd_quantile).to(S.device)
    # threshold = torch.quantile(S, q).item()
    # small_singular_indices = (S < threshold).nonzero(as_tuple=True)[0]

    # p = torch.randn(d2, d1).to(w.device)
    # return p @ p.T

    return V #@ V.T


