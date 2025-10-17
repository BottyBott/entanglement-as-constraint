"""Sweep Werner-state visibility and watch the CHSH value cross 2."""

from __future__ import annotations

import argparse
import math
from typing import Tuple

import numpy as np

from eac.chsh import chsh_value
from eac.states import werner_state


DEFAULT_ANGLES: Tuple[Tuple[float, float], Tuple[float, float]] = (
    (0.0, math.pi / 2),
    (math.pi / 4, -math.pi / 4),
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", type=int, default=20_000, help="Shots per visibility value.")
    parser.add_argument("--v-grid", type=int, default=21, help="Number of visibility samples.")
    parser.add_argument("--min-v", type=float, default=0.0, help="Minimum visibility.")
    parser.add_argument("--max-v", type=float, default=1.0, help="Maximum visibility.")
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
        from examples.chsh_realtime import parse_angles  # lazy import to reuse parser

        angles = parse_angles(args.angles)

    visibilities = np.linspace(args.min_v, args.max_v, args.v_grid)
    print("# v\tS")
    crossing_v = None
    for v in visibilities:
        rho = werner_state(v)
        s_est = chsh_value(rho, angles, shots=args.shots, rng=rng).value
        print(f"{v:.4f}\t{s_est:.4f}")
        if crossing_v is None and s_est > 2.0:
            crossing_v = v
    target = 1 / math.sqrt(2)
    if crossing_v is None:
        print(f"No violation detected; target visibility ≈ {target:.4f}")
    else:
        delta = abs(crossing_v - target)
        print(f"First violation near v={crossing_v:.4f}; |Δ| ≈ {delta:.4f} (target {target:.4f})")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
