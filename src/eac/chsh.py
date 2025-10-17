"""CHSH correlations and diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

from .measure import observable, sample_outcome
from .states import as_density_matrix


Angles = Tuple[Tuple[float, float], Tuple[float, float]]


@dataclass
class CorrelationResult:
    value: float
    shots: int


def correlation(
    state,
    theta_a: float,
    theta_b: float,
    *,
    shots: int = 10_000,
    rng: np.random.Generator | None = None,
) -> CorrelationResult:
    """Estimate E(theta_a, theta_b) = ⟨A B⟩."""
    if rng is None:
        rng = np.random.default_rng()
    outcomes = np.empty(shots, dtype=float)
    for i in range(shots):
        a, b = sample_outcome(state, theta_a, theta_b, rng=rng)
        outcomes[i] = a * b
    return CorrelationResult(value=float(outcomes.mean()), shots=shots)


def correlation_exact(
    state,
    theta_a: float,
    theta_b: float,
) -> CorrelationResult:
    """Exact expectation value ⟨A B⟩ without sampling."""
    rho = as_density_matrix(state)
    a_op = observable(theta_a)
    b_op = observable(theta_b)
    op = np.kron(a_op, b_op)
    value = float(np.real(np.trace(op @ rho)))
    return CorrelationResult(value=value, shots=0)


def chsh_value(
    state,
    angles: Angles,
    *,
    shots: int = 10_000,
    rng: np.random.Generator | None = None,
) -> CorrelationResult:
    """Estimate the CHSH S value for the specified angles."""
    if rng is None:
        rng = np.random.default_rng()
    (a, a_prime), (b, b_prime) = angles
    corr_ab = correlation(state, a, b, shots=shots, rng=rng)
    corr_abp = correlation(state, a, b_prime, shots=shots, rng=rng)
    corr_apb = correlation(state, a_prime, b, shots=shots, rng=rng)
    corr_apbp = correlation(state, a_prime, b_prime, shots=shots, rng=rng)
    value = (
        corr_ab.value
        + corr_abp.value
        + corr_apb.value
        - corr_apbp.value
    )
    return CorrelationResult(value=float(value), shots=4 * shots)


def chsh_exact(
    state,
    angles: Angles,
) -> CorrelationResult:
    """Exact CHSH value using analytic expectation values."""
    (a, a_prime), (b, b_prime) = angles
    corr_ab = correlation_exact(state, a, b)
    corr_abp = correlation_exact(state, a, b_prime)
    corr_apb = correlation_exact(state, a_prime, b)
    corr_apbp = correlation_exact(state, a_prime, b_prime)
    value = (
        corr_ab.value
        + corr_abp.value
        + corr_apb.value
        - corr_apbp.value
    )
    return CorrelationResult(value=float(value), shots=0)


def _marginal_probability(
    state,
    theta_a: float,
    theta_b: float,
    *,
    shots: int,
    target: str,
    rng: np.random.Generator,
) -> float:
    hits = 0
    for _ in range(shots):
        a, b = sample_outcome(state, theta_a, theta_b, rng=rng)
        if target == "alice" and a == +1:
            hits += 1
        if target == "bob" and b == +1:
            hits += 1
    return hits / shots


def check_no_signaling(
    state,
    angles: Angles,
    *,
    shots: int = 20_000,
    rng: np.random.Generator | None = None,
):
    """Return marginal probabilities for Alice and Bob under setting changes."""
    if shots < 4:
        raise ValueError("shots must be >= 4 to run the no-signaling check.")
    if rng is None:
        rng = np.random.default_rng()
    (a, a_prime), (b, b_prime) = angles
    per_case = max(1, shots // 4)
    alice_p = {
        "b": _marginal_probability(state, a, b, shots=per_case, target="alice", rng=rng),
        "b_prime": _marginal_probability(
            state, a, b_prime, shots=per_case, target="alice", rng=rng
        ),
    }
    bob_p = {
        "a": _marginal_probability(state, a, b, shots=per_case, target="bob", rng=rng),
        "a_prime": _marginal_probability(
            state, a_prime, b, shots=per_case, target="bob", rng=rng
        ),
    }
    deviation = max(
        abs(alice_p["b"] - alice_p["b_prime"]),
        abs(bob_p["a"] - bob_p["a_prime"]),
    )
    return {
        "alice": alice_p,
        "bob": bob_p,
        "max_deviation": deviation,
        "shots_per_case": per_case,
    }
