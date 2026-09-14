from dataclasses import dataclass
from typing import List
import yaml

from ...util.hparams import HyperParams


@dataclass
class LOKIHyperParams(HyperParams):
    # Model / framework
    alg_name: str
    model_name: str
    device: int

    # Layers edited (static fallback list) and where the FFN down-projection lives
    layers: List[int]
    loss_layer: int
    rewrite_module_tmp: str
    layer_module_tmp: str
    fact_token: str

    # Knowledge insertion (projected gradient descent)
    w_lr: float
    num_steps: int
    norm_constraint: float
    kl_factor: float
    objective_optimization: str
    batch_size: int

    # Dynamic (per-sample) layer selection
    num_layers: int = 5            # number of layers to edit (m)
    layer_offset: int = 4
    layer_hsic_type: str = 'subtract'
    dynamic_layer: bool = True

    # Null-space projection + HSIC information bottleneck
    null_dim: int = 300
    hx: float = 0.001              # HSIC coefficient lambda_x
    hy: float = 0.001              # HSIC coefficient lambda_y
    hsigma: float = 1.0            # HSIC kernel bandwidth

    # Runtime
    max_length: int = 40
    model_parallel: bool = False
    fp16: bool = False


    @classmethod
    def from_hparams(cls, hparams_name_or_path: str):

        if '.yaml' not in hparams_name_or_path:
            hparams_name_or_path = hparams_name_or_path + '.yaml'

        with open(hparams_name_or_path, "r") as stream:
            config = yaml.safe_load(stream)
            config = super().construct_float_from_scientific_notation(config)

        assert (config and config['alg_name'] == 'LOKI') or print(f'LOKIHyperParams can not load from {hparams_name_or_path}, '
                                                f'alg_name is {config["alg_name"]} ')
        return cls(**config)
