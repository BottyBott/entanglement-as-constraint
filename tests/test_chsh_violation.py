import math

import numpy as np

from eac.chsh import chsh_value
from eac.states import bell_state


ANGLES = (
    (0.0, math.pi / 2),
    (math.pi / 4, -math.pi / 4),
)


def test_bell_state_violates_chsh():
    rng = np.random.default_rng(2024)
    result = chsh_value(bell_state(), ANGLES, shots=25_000, rng=rng)
    assert result.value > 2.6
