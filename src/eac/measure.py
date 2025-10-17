"""Contextual measurement utilities."""

from __future__ import annotations

from typing import Tuple

import numpy as np

try:
    import qutip
except ImportError:  # pragma: no cover - optional dependency
    qutip = None

from .states import as_density_matrix

Outcome = Tuple[int, int]


def projector(theta: float) -> Tuple[np.ndarray, np.ndarray]:
    """Return projectors onto ±1 eigenstates for σ·n in the x–z plane."""
    half = theta / 2.0
    v_plus = np.array([np.cos(half), np.sin(half)], dtype=np.complex128)
    v_minus = np.array([-np.sin(half), np.cos(half)], dtype=np.complex128)
    p_plus = np.outer(v_plus, v_plus.conj())
    p_minus = np.outer(v_minus, v_minus.conj())
    return p_plus, p_minus


def _to_density(state) -> np.ndarray:
    if qutip is not None and isinstance(state, qutip.Qobj):  # pragma: no cover - optional dependency
        return as_density_matrix(np.asarray(state.full(), dtype=np.complex128))
    return as_density_matrix(state)


def sample_outcome(
    state,
    theta_a: float,
    theta_b: float,
    rng: np.random.Generator | None = None,
) -> Outcome:
    """Draw a joint outcome (+/-1, +/-1) using the Born rule."""
    if rng is None:
        rng = np.random.default_rng()
    rho = _to_density(state)
    p_a_plus, p_a_minus = projector(theta_a)
    p_b_plus, p_b_minus = projector(theta_b)
    ops = {
        (+1, +1): np.kron(p_a_plus, p_b_plus),
        (+1, -1): np.kron(p_a_plus, p_b_minus),
        (-1, +1): np.kron(p_a_minus, p_b_plus),
        (-1, -1): np.kron(p_a_minus, p_b_minus),
    }
    probs = np.array([np.real(np.trace(op @ rho)) for op in ops.values()], dtype=float)
    probs = np.clip(probs, 0.0, 1.0)
    probs /= probs.sum()
    outcomes = list(ops.keys())
    choice = rng.choice(len(outcomes), p=probs)
    return outcomes[choice]
