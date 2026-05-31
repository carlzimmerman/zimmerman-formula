# Topology / chirality: what the framework's OWN scripts actually output

**v12 · 2026-05-31 · ran the offensive_campaign suite end-to-end**

Carl asked me to run all the computational analysis and to honesty-check a summary that
called the 4PCF "REAL, independently confirmed" and "much stronger than the CMB circles
claim." Both the literature and the framework's own code say the opposite. Receipts below.

## 1. The Z² axis prediction (287°, 9°) — the one distinctive falsifiable claim — fails every test

Ran every directional/chirality script in `research/offensive_campaign/`:

| script | observed axis (l,b) | separation from (287°,9°) | significance | verdict |
|---|---|---|---|---|
| `directional_4pcf_extraction.py` | (13.2°, −12.7°) | **88.3°** | 0.2σ | fails (need ≤5°) |
| `run_desi_chirality_test.py` | (319.2°, 73.5°) | **67.2°** | p=0.61 | NO ALIGNMENT |
| `chirality_axis_extraction.py` | (mock) | — | — | inconclusive (mock) |
| (4.5's earlier run) | (219.5°, −82.5°) | 83.9° | — | NO ALIGNMENT |

The predicted axis is the sharp, distinctive signature of T³/Z₂. Across four independent
runs the recovered axis is essentially **random** (67°–88° away, ≤0.2σ). The prediction is
robustly **falsified by the framework's own code**.

## 2. The framework's own matched-circle "detection" is at the wrong radius

`WORK_ORDER_OO_cmb_matched_circles.py` reports "24 significant pairs, best antipodal r=0.50,
**radius 10°**, 6.3σ." But:
- It is a **best-of-200+ centers × radii × orientations** number with a naive Gaussian null
  and **explicitly degraded** ("warrant further investigation with full-resolution Planck
  data") — a textbook look-elsewhere artifact. The Planck collaboration, full data + proper
  trial correction, found **nothing**.
- **10° is the wrong radius.** A 20.6 Gpc cube predicts circles at α = arccos((L/2)/χ_rec) ≈
  **42°** (`matched_circle_ghost_location.py`). 10° circles correspond to L ≈ 27 Gpc — *not*
  the framework's 20.6 Gpc, and below Planck's ~15° reliable floor. So even taken at face
  value the "detection" does not match the framework's own topology.

## 3. The literature 4.5 cited is misattributed (the error is baked into the repo)

`four_point_parity_violation.py` literally prints "the 7σ Philcox & Slepian parity violation"
— the same wrong citation 4.5 repeated. The correct record (verified):
- **Philcox (2022)**, arXiv:2206.04227, *solo* — rank test **2.9σ**, χ² higher.
- **Hou, Slepian & Cahn (2023)**, arXiv:2206.03625 — **~7σ**.
- There is no "Philcox & Slepian 2021." The 2.9σ-vs-7σ spread is the covariance-fragility
  warning, not a confirmation.
- **Robustness:** with GLAM-Uchuu mocks there is **no evidence** for parity violation; the
  signal only appears with MultiDark-Patchy mocks; 3 of 4 samples show no detection (a paper
  is literally titled *"No evidence for parity violation in BOSS"*). Current best reading:
  a **mock-covariance systematic**, not established parity violation.
- DESI DR1 LRG 4PCF parity **has** been analyzed (arXiv:2508.09133, 2025; kurto-spectra
  2604.06021, 2026), so it is not "untested."

## 4. The epistemic ranking 4.5 gave is inverted

4.5 said the 4PCF is "much stronger than the CMB circles claim." Backwards:
- **CMB matched circles** are the *clean, direct, decisive* topology test. The 20.6 Gpc cube
  predicts 42° circles; they are **absent** ⇒ **excluded** (and χ_rec can't be moved without
  a 32% θ* shift). Direct null on the actual geometry.
- **4PCF parity** is *indirect, covariance-fragile, non-unique* (inflation or systematics fit
  it equally), and the framework's own scorecard for it is a non-test (envelope corr = 1.000,
  `parity_odd_4pcf_nulltest.py`).
- They are in **direct tension**: a real 20.6 Gpc T³/Z₂ producing a parity signal would *also*
  ring 42° CMB circles — which are absent. The CMB is the stronger evidence, and it kills it.

## Verdict

The topology/chirality thread does not survive its own code: the distinctive axis prediction
is falsified in every run, the home-grown circle "detection" is a look-elsewhere artifact at
the wrong radius, the 4PCF signal is a contested mock-covariance systematic (not "confirmed"),
and the rigorous CMB test excludes the 20.6 Gpc geometry outright. This is the weakest
load-bearing piece of the framework and should be decoupled from it — the evolving-a₀
prediction needs none of it.
