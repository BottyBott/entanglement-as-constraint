"""State factories for entanglement-as-constraint demos."""

from __future__ import annotations

from typing import Literal, Optional

import numpy as np

try:
    import qutip
except ImportError:  # pragma: no cover - optional dependency
    qutip = None

BellLabel = Literal["Phi+", "Phi-", "Psi+", "Psi-"]
Backend = Literal["numpy", "qutip"]


def _bell_vector(label: BellLabel) -> np.ndarray:
    root2 = np.sqrt(2.0)
    zero = np.array([1.0, 0.0], dtype=np.complex128)
    one = np.array([0.0, 1.0], dtype=np.complex128)
    basis = {
        "00": np.kron(zero, zero),
        "01": np.kron(zero, one),
        "10": np.kron(one, zero),
        "11": np.kron(one, one),
    }
    if label == "Phi+":
        return (basis["00"] + basis["11"]) / root2
    if label == "Phi-":
        return (basis["00"] - basis["11"]) / root2
    if label == "Psi+":
        return (basis["01"] + basis["10"]) / root2
    if label == "Psi-":
        return (basis["01"] - basis["10"]) / root2
    raise ValueError(f"Unsupported Bell label {label!r}")


def as_density_matrix(state: np.ndarray) -> np.ndarray:
    """Convert a state vector or density matrix into a density matrix."""
    state = np.asarray(state, dtype=np.complex128)
    if state.ndim == 1:
        return np.outer(state, state.conj())
    if state.ndim == 2:
        return state
    raise ValueError("State must be a vector or density matrix.")


def _to_backend(array: np.ndarray, backend: Backend):
    if backend == "numpy":
        return array
    if backend == "qutip":
        if qutip is None:  # pragma: no cover - optional dependency
            raise RuntimeError("qutip is not installed but backend='qutip' was requested")
        return qutip.Qobj(array)
    raise ValueError(f"Unknown backend {backend!r}")


def bell_state(
    label: BellLabel = "Phi+",
    *,
    as_density: bool = True,
    backend: Backend = "numpy",
):
    """Return the requested Bell state."""
    vec = _bell_vector(label)
    data = as_density_matrix(vec) if as_density else vec
    return _to_backend(data, backend)


def werner_state(
    visibility: float,
    *,
    singlet: BellLabel = "Phi+",
    backend: Backend = "numpy",
):
    """Return a Werner state ρ = v|ψ⟩⟨ψ| + (1-v) I/4."""
    if not 0.0 <= visibility <= 1.0:
        raise ValueError("visibility must lie in [0, 1].")
    pure = as_density_matrix(_bell_vector(singlet))
    identity = np.eye(pure.shape[0], dtype=np.complex128) / pure.shape[0]
    rho = visibility * pure + (1.0 - visibility) * identity
    return _to_backend(rho, backend)


def load_state(
    label: Optional[BellLabel] = None,
    *,
    visibility: Optional[float] = None,
    backend: Backend = "numpy",
):
    """Convenience loader used by CLIs to pick a Bell or Werner state."""
    if visibility is not None:
        return werner_state(visibility, backend=backend)
    if label is None:
        label = "Phi+"
    return bell_state(label, backend=backend)
