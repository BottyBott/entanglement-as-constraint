import math

import numpy as np

from eac.chsh import chsh_value
from eac.states import werner_state


ANGLES = (
    (0.0, math.pi / 2),
    (math.pi / 4, -math.pi / 4),
)


def test_werner_visibility_crosses_local_bound_near_target():
    rng = np.random.default_rng(7)
    visibilities = np.linspace(0.5, 1.0, 12)
    estimates = []
    for v in visibilities:
        s_val = chsh_value(werner_state(v), ANGLES, shots=25_000, rng=rng).value
        estimates.append((v, s_val))
    target = 1 / math.sqrt(2)
    crossing = min(estimates, key=lambda item: abs(item[1] - 2.0))[0]
    assert abs(crossing - target) < 0.03
