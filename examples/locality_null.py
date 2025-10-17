"""Local hidden-variable sampler: proves the S<=2 ceiling."""

from __future__ import annotations

import argparse
import math
from typing import Dict, Tuple

import numpy as np

DEFAULT_ANGLES: Tuple[Tuple[float, float], Tuple[float, float]] = (
    (0.0, math.pi / 2),
    (math.pi / 4, -math.pi / 4),
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", type=int, default=50_000, help="Number of trials.")
    parser.add_argument("--schedule", choices=("cycle", "random"), default="cycle")
    parser.add_argument("--seed", type=int, default=None, help="Random seed.")
    parser.add_argument(
        "--angles",
        type=str,
        default=None,
        help="Optional custom angles 'a,a_prime;b,b_prime' (radians).",
    )
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    angles = DEFAULT_ANGLES
    if args.angles:
        from examples.chsh_realtime import parse_angles  # reuse parser

        angles = parse_angles(args.angles)
    (a, a_prime), (b, b_prime) = angles
    pairs = (
        ("a", "b"),
        ("a", "b_prime"),
        ("a_prime", "b"),
        ("a_prime", "b_prime"),
    )
    corr_sums: Dict[str, float] = {f"{p[0]}{p[1]}": 0.0 for p in pairs}
    corr_counts: Dict[str, int] = {key: 0 for key in corr_sums}
    labels = ("a", "a_prime", "b", "b_prime")

    for shot in range(1, args.shots + 1):
        hidden = {label: rng.choice((-1, 1)) for label in labels}
        if args.schedule == "random":
            pair = pairs[int(rng.integers(len(pairs)))]
        else:
            pair = pairs[(shot - 1) % len(pairs)]
        key = f"{pair[0]}{pair[1]}"
        result = hidden[pair[0]] * hidden[pair[1]]
        corr_sums[key] += result
        corr_counts[key] += 1

    def safe_mean(key: str) -> float:
        if corr_counts[key] == 0:
            return float("nan")
        return corr_sums[key] / corr_counts[key]

    e_ab = safe_mean("ab")
    e_abp = safe_mean("ab_prime")
    e_apb = safe_mean("a_primeb")
    e_apbp = safe_mean("a_primeb_prime")
    s_val = e_ab + e_abp + e_apb - e_apbp

    print(f"Angles: Alice {angles[0]}, Bob {angles[1]}")
    print("Local model correlations:")
    print(f"  E(a,b)      = {e_ab:.3f}")
    print(f"  E(a,b')     = {e_abp:.3f}")
    print(f"  E(a',b)     = {e_apb:.3f}")
    print(f"  E(a',b')    = {e_apbp:.3f}")
    print(f"S_local ≈ {s_val:.3f} (≤ 2 by construction)")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
