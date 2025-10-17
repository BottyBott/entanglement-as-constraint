import math

import numpy as np

from eac.chsh import check_no_signaling
from eac.states import bell_state


ANGLES = (
    (0.0, math.pi / 2),
    (math.pi / 4, -math.pi / 4),
)


def test_no_signaling_marginals_stay_balanced():
    rng = np.random.default_rng(99)
    report = check_no_signaling(bell_state(), ANGLES, shots=40_000, rng=rng)
    assert report["max_deviation"] < 0.02
