"""Entanglement-as-constraint utilities."""

from .states import bell_state, werner_state, as_density_matrix
from .measure import projector, sample_outcome, observable
from .chsh import correlation, chsh_value, check_no_signaling, correlation_exact, chsh_exact
from .simulate import chsh_stream

__all__ = [
    "as_density_matrix",
    "bell_state",
    "werner_state",
    "projector",
    "observable",
    "sample_outcome",
    "correlation",
    "chsh_value",
    "correlation_exact",
    "chsh_exact",
    "check_no_signaling",
    "chsh_stream",
]
