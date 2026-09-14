"""Follow-up contracts; preserve the accepted study's strict scorer unchanged."""
import random
import re
from task import A_WORDS, B_WORDS, C_WORDS, DEV_WORDS, cases, scope, score, route

ARMS = ('only', 'repeat', 'narrow', 'broad')
ANCHORED_ARMS = ('only', 'triple', 'boundary-repeat', 'boundary-history')
TARGETS = [c for c in cases(C_WORDS) if scope(c)]
HISTORY = cases(A_WORDS) + cases(B_WORDS, ('amber', 'teal'))
BROAD = [c for c in HISTORY if not scope(c)]
CONDITIONS = [(ch, p) for ch in ('copper', 'violet', 'amber', 'teal')
              for p in ('slow', 'fast') if (ch, p) != ('copper', 'fast')]
NARROW = [dict(channel=ch, priority=p, identifier='druvan' if ch in ('copper', 'violet') else 'fepzan')
          for ch, p in CONDITIONS]
BOUNDARY = [dict(channel=ch, priority=p, identifier=C_WORDS[0]) for ch,p in CONDITIONS]

def block_updates(mode, target, narrow, broad):
    result = [('target', target)]
    if mode in ('repeat','triple'): result += [('repeat',target)] * (1 if mode == 'repeat' else 2)
    elif mode in ('narrow','broad'): result += [('replay',narrow if mode == 'narrow' else broad)]
    elif mode in ('boundary-repeat','boundary-history'):
        boundary = dict(narrow, identifier=C_WORDS[0])
        result += [('boundary',boundary), ('boundary-repeat',boundary) if mode == 'boundary-repeat' else ('history',broad)]
    else: assert mode == 'only'
    return result

def components(raw, c, revised=True):
    result = score(raw, c, revised)
    result['strict_route'] = result.pop('route')
    # Recognize a tool at the start only, before '(' or whitespace/end. A malformed
    # argument does not turn an unambiguous tool choice into a routing error.
    match = re.match(r'^\s*(kestrel|marten)(?=\s|\(|$)', raw)
    tool = match.group(1) if match else None
    result.update(route=tool == route(c, revised), tool_known=tool is not None,
                  stale=bool(revised and scope(c) and tool == route(c, False)),
                  overgeneralized=bool(revised and c['channel'] == 'copper' and c['priority'] == 'slow' and tool == 'marten'))
    return result

def schedule(blocks):
    rng = random.Random(73)
    target_order = []
    while len(target_order) < blocks:
        order = list(range(4)); rng.shuffle(order); target_order.extend(order)
    replay = []
    cycle = 0
    while len(replay) < blocks:
        order = list(range(7)); rng.shuffle(order)
        for index in order:
            narrow = NARROW[index]
            words = A_WORDS if narrow['channel'] in ('copper', 'violet') else B_WORDS
            offset = 1 if words == A_WORDS else 0
            broad = dict(narrow, identifier=words[(cycle + offset) % 4])
            replay.append((narrow, broad))
        cycle += 1
    return [(TARGETS[t], *r) for t, r in zip(target_order[:blocks], replay[:blocks])]
