"""Shot-by-shot simulation tools."""

from __future__ import annotations

from typing import Dict, Generator, Tuple

import numpy as np

from .measure import sample_outcome
from .chsh import Angles


def chsh_stream(
    state,
    angles: Angles,
    *,
    shots: int,
    schedule: str = "cycle",
    rng: np.random.Generator | None = None,
) -> Generator[dict, None, None]:
    """Yield running statistics for CHSH experiments."""
    if rng is None:
        rng = np.random.default_rng()
    (a, a_prime), (b, b_prime) = angles
    pairs: Tuple[Tuple[float, float], ...] = (
        (a, b),
        (a, b_prime),
        (a_prime, b),
        (a_prime, b_prime),
    )
    corr_sums: Dict[Tuple[float, float], float] = {pair: 0.0 for pair in pairs}
    corr_counts: Dict[Tuple[float, float], int] = {pair: 0 for pair in pairs}
    alice_stats = {a: {"shots": 0, "plus": 0}, a_prime: {"shots": 0, "plus": 0}}
    bob_stats = {b: {"shots": 0, "plus": 0}, b_prime: {"shots": 0, "plus": 0}}
    for shot in range(1, shots + 1):
        if schedule == "random":
            pair = pairs[int(rng.integers(len(pairs)))]
        else:
            pair = pairs[(shot - 1) % len(pairs)]
        outcome = sample_outcome(state, pair[0], pair[1], rng=rng)
        product = outcome[0] * outcome[1]
        corr_sums[pair] += product
        corr_counts[pair] += 1
        alice_stats[pair[0]]["shots"] += 1
        bob_stats[pair[1]]["shots"] += 1
        if outcome[0] == +1:
            alice_stats[pair[0]]["plus"] += 1
        if outcome[1] == +1:
            bob_stats[pair[1]]["plus"] += 1
        running_s = None
        if all(corr_counts[p] > 0 for p in pairs):
            e_vals = [corr_sums[p] / corr_counts[p] for p in pairs]
            running_s = e_vals[0] + e_vals[1] + e_vals[2] - e_vals[3]
        yield {
            "shot": shot,
            "settings": pair,
            "outcome": outcome,
            "running_s": running_s,
            "correlations": {
                str(pair): corr_sums[pair] / corr_counts[pair] for pair in pairs if corr_counts[pair]
            },
            "marginals": {
                "alice": {
                    float(angle): stats["plus"] / stats["shots"] if stats["shots"] else None
                    for angle, stats in alice_stats.items()
                },
                "bob": {
                    float(angle): stats["plus"] / stats["shots"] if stats["shots"] else None
                    for angle, stats in bob_stats.items()
                },
            },
        }
