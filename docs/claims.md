# Manuscript ↔ Code Crosswalk

| Manuscript claim | Artifact | Demonstrated when… |
| ---------------- | -------- | ------------------- |
| Measurements are contextual performances determined by present apparatus. | `examples/chsh_realtime.py`, `eac.measure` | Changing angle inputs shifts the running \(S_n\) while marginals remain balanced. |
| Probability is the right grammar; do not infer hidden properties. | `eac.chsh`, `tests/test_chsh_violation.py` | Violations arise from sampled correlations; no state ever stores pre-assigned outcomes. |
| Entanglement encodes a global constraint spanning both parties. | `eac.states`, `eac.simulate` | The same qubits obey different “laws” (distinct \(S\)) under different measurement contexts. |
| Constraint strength governs observable behaviour. | `examples/werner_threshold.py`, `tests/test_werner_threshold.py` | Weakening visibility drags \(S\) back to the local bound near \(v=1/\sqrt{2}\). |
| Local hidden-history stories cannot match entangled correlations. | `examples/locality_null.py`, `tests/test_no_signaling.py` | Local models respect the \(S \le 2\) ceiling and still satisfy no-signaling, so the gap is empirical. |
