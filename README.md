# Entanglement as Constraint

A present-centered demo that treats entanglement as a global constraint producing contextual correlations. Measurements are performances defined by the current apparatus; change the context and the correlations—and the effective laws you witness—shift with it.

## Quick Start

```bash
pip install -e .               # installs numpy; qutip is optional
python3 -m examples.chsh_realtime --shots 50000
python3 -m examples.werner_threshold --shots 20000 --v-grid 21
python3 -m examples.locality_null --shots 50000
```

What you will see:

- CHSH violations around \(S \approx 2.82\) for the Bell state \(|\Phi^+\rangle\).
- No-signaling marginals that hover near 0.5 regardless of the remote setting.
- A visibility sweep where the Werner state crosses the local bound \(S=2\) close to \(v = 1/\sqrt{2}\).

## Work in Jupyter

Prefer notebooks? Install the plotting extra and launch any of the ready-made demos in `notebooks/`:

```bash
pip install -e .[notebooks]
jupyter notebook notebooks/chsh_realtime.ipynb
```

Available notebooks mirror the CLI scripts:

- `notebooks/chsh_realtime.ipynb`: running \(S_n\) estimates and marginal plots.
- `notebooks/werner_threshold.ipynb`: visibility sweep for the Werner state.
- `notebooks/locality_null.ipynb`: classical baseline that never climbs past \(S=2\).

## Why This Repo Exists

My thesis (not included) argues that science should privilege present constraints over speculative histories. This repo operationalises that stance for entanglement:

- Measurements are **contextual performances**; the apparatus and the angles picked now define the observable.
- Probabilities encode our best statements; we do not tell stories about hidden histories.
- Correlations express a **global constraint**. Alter the constraint—by shifting angles or adding noise—and the behaviour changes immediately.

Each module grounds a point from the thesis: states define the shared constraint, measurement modules enforce contextuality, CHSH utilities track probability-first claims, and the simulator streams running statistics so the discussion stays anchored in live data.
