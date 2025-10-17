"""Stream a running CHSH estimate."""

from __future__ import annotations

import argparse
import math
from typing import Tuple

import numpy as np

from eac.simulate import chsh_stream
from eac.states import load_state


DEFAULT_ANGLES: Tuple[Tuple[float, float], Tuple[float, float]] = (
    (0.0, math.pi / 2),
    (math.pi / 4, -math.pi / 4),
)


def parse_angles(spec: str) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Parse CLI angle specs like '0,1.571;0.785,-0.785'."""
    try:
        alice_raw, bob_raw = spec.split(";")
        a_vals = tuple(float(x) for x in alice_raw.split(","))
        b_vals = tuple(float(x) for x in bob_raw.split(","))
    except ValueError as exc:  # pragma: no cover - user input validation
        raise argparse.ArgumentTypeError("Angles must look like '0,1.571;0.785,-0.785'") from exc
    if len(a_vals) != 2 or len(b_vals) != 2:
        raise argparse.ArgumentTypeError("Provide exactly two angles for each party.")
    return (a_vals[0], a_vals[1]), (b_vals[0], b_vals[1])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", type=int, default=50_000, help="Number of measurement shots.")
    parser.add_argument(
        "--angles",
        type=parse_angles,
        default=DEFAULT_ANGLES,
        help="Format: 'a,a_prime;b,b_prime' (radians).",
    )
    parser.add_argument(
        "--visibility",
        type=float,
        default=None,
        help="Optional Werner-state visibility parameter v.",
    )
    parser.add_argument(
        "--schedule",
        choices=("cycle", "random"),
        default="cycle",
        help="Measurement setting schedule per shot.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Seed for the random generator.")
    parser.add_argument(
        "--every",
        type=int,
        default=1_000,
        help="Print every N shots (also prints the final shot).",
    )
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    state = load_state(visibility=args.visibility)

    for record in chsh_stream(
        state,
        args.angles,
        shots=args.shots,
        schedule=args.schedule,
        rng=rng,
    ):
        should_print = record["shot"] % args.every == 0 or record["shot"] == args.shots
        if not should_print:
            continue
        running_s = record["running_s"]
        s_display = f"{running_s:.3f}" if running_s is not None else "n/a"
        marginals = record["marginals"]
        alice_m = ", ".join(
            f"A({angle:.3f})={prob:.3f}" if prob is not None else f"A({angle:.3f})=n/a"
            for angle, prob in marginals["alice"].items()
        )
        bob_m = ", ".join(
            f"B({angle:.3f})={prob:.3f}" if prob is not None else f"B({angle:.3f})=n/a"
            for angle, prob in marginals["bob"].items()
        )
        print(
            f"shot={record['shot']:>6} "
            f"settings=({record['settings'][0]:.3f},{record['settings'][1]:.3f}) "
            f"outcome={record['outcome']} S≈{s_display} :: {alice_m} | {bob_m}"
        )


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
