# EST_ROBUST — the robust-estimator lane of the TRGB lever on the a0-line

**Script:** `est_robust.py` (exit 0) · **JSON:** `est_robust_results.json` · reuses frozen
`../a0_line/fire_common.py` (READ-ONLY). Data: SPARC (Lelli–McGaugh–Schombert 2016),
`real_research/data/sparc_master_clean.csv` (carries the distance-method flag `fD`).

## What this lane does
The a0-line is the framework's own exact identity `E ≡ g_obs² − g_bar² = a0·g_bar`
(from `nu = sqrt(1+1/y)`, the Milgrom-1999 kernel; the framework's distinctive content is
the horizon **coefficient** `a0 = cH_Λ/Z`, not the kernel shape). This lane re-measures the
slope `a0` with the two **robust / weight-free** estimators that cross-checked the banked
GLS central, on the **TRGB/Cepheid-anchored** gas-dominated subsample (`fD ∈ {2,3}`,
σ_lnD = 0.05 — 5× smaller per galaxy than the `fD=1` Hubble-flow 0.25) vs the **full gas**
subsample, **both footings**:

- **R1 median / robust slope** — `a0 = median(E/g_bar)` (Theil-Sen-through-origin; no
  weights → immune to the weight-noise trap that once faked a 3.3e-11 deficit).
- **R2 EIV / ODR** — orthogonal-distance regression of `g_obs² = g_bar² + a0·g_bar` in the
  `(g_bar, g_obs²)` plane, where g_bar (photometry+gas) and g_obs (kinematics) carry
  **independent** errors — the honest errors-in-variables form. Model-based σ, intrinsic
  floor iterated to res_var→1 (the same cure the banked GLS used).
- **GLS** imported only as the **agreement** cross-check. Errors are **galaxy-level
  bootstrap** (2000 resamples of galaxies, not points).

## Headline numbers (Ud = 0.70, banked headline; 18 gals / 147 pts TRGB)

| subsample | median | EIV/ODR | GLS | med~GLS | σ_tot | vs canon | vs ALT |
|---|---|---|---|---|---|---|---|
| GAS-ALL (49/310) | 0.973e-10 | 1.198e-10 | 1.181e-10 | ~1σ | 16.1% | +1.29σ | +0.27σ |
| **TRGB {2,3} (18/147)** | **1.273e-10** | **1.354e-10** | **1.333e-10** | **AGREE (0.2σ)** | **12.8%** | **+2.32σ** | **+1.18σ** |
| Hubble-flow {1} (29/154) | 0.805e-10 | 0.965e-10 | 0.954e-10 | AGREE | — | −1.1σ | −2.7σ (median) |

(Fiducial Ud=0.50 reproduces the same picture, shifted up: TRGB median 1.43e-10 / EIV 1.52e-10.)

## What the lever actually did — four robust findings

1. **The estimator-choice systematic COLLAPSES on the clean set.** median and GLS AGREE
   to 0.2σ on TRGB (1.273 vs 1.333e-10); the sEst budget line drops **1.04e-11 → 2.99e-12**.
   On GAS-ALL the median (0.973) sat ~20% below GLS — and that low median was driven almost
   entirely by the Hubble-flow gas dwarfs (their median is **0.805e-10**). Remove the noisy
   distances and median/GLS converge. **Estimator-owned central is robust on clean distances.**

2. **The central MOVES UP, coherently — it does NOT stay at the banked value, and it does
   NOT land on canonical.** banked GAS-ALL GLS 1.181e-10 → TRGB GLS 1.333e-10 (**+13%**),
   with median and EIV moving up in lockstep. Within 1σ statistically, but a coherent upward
   shift. The tightened central sits at **~1.27–1.35e-10 — >2σ ABOVE canonical 9.36e-11,
   and ~1–1.4σ above/around ALT 1.13e-10.**

3. **The distance systematic did shrink, but the total error only tightened 16.1%→12.8%.**
   sysD 7.63e-12 → 3.78e-12 (50% smaller — not 5×, because only 18 galaxies survive to
   average down); the global Upsilon/gascal terms (~1.1e-11 each) now dominate and do NOT
   shrink with the distance flag. **Distance was NOT the single limiting budget line.**

4. **TRGB-vs-Hubble split: ~1.7–1.8σ, clean set HIGHER (all three estimators).** Consistent
   with EITHER a residual Hubble-flow distance bias dragging the banked central down OR
   small-N (18/29) scatter — **NOT a decisive detection** either way.

## Occam bans (with the TRGB-reduced error, both footings)
`M0: a0 predicted from (c, H_Λ, Z), 0 params` vs `M1: a0 free`. `+ = favors the predicted-a0 model`.

| case | a0_hat | s_ln | B(canon) | B(ALT) |
|---|---|---|---|---|
| GAS-ALL GLS | 1.181e-10 | 0.161 | +0.60 | +1.04 |
| **TRGB GLS (lever central)** | **1.333e-10** | **0.128** | **−0.49** | **+0.80** |
| TRGB median | 1.273e-10 | 0.128 | −0.09 | +0.97 |
| TRGB @canon (if central→pred) | 9.36e-11 | 0.128 | +1.15 | +0.68 |
| TRGB @ALT (if central→pred) | 1.13e-10 | 0.128 | +0.68 | +1.15 |

**Realized, the forecast's canonical arm FIRES AGAINST canonical:** because the tightened
central moved UP (not stayed), canonical goes to **−0.49 bans (mildly disfavored)** while ALT
is +0.80 (weakly favored). But the footing separation is only ~1.3 bans — **under the 2-ban
"decisive" line. Neither footing is selected by the data.**

## Λ-inversion (the thesis: a0-from-rotation = dark-energy density)
`Λ = 3 Z² a0² / c⁴`, Z = 5.7888. Canonical a0 inverts to **exactly 1.00× Planck** by
construction (a0 = cH_Λ/Z). The clean-distance dwarfs invert to:

| | a0 | Λ / Λ_Planck (±1σ) |
|---|---|---|
| GAS-ALL GLS | 1.181e-10 | 1.60× [1.12, 2.15] |
| **TRGB GLS** | **1.333e-10** | **2.03× [1.54, 2.59]** |
| TRGB median | 1.273e-10 | 1.85× [1.39, 2.38] |

Dwarf **rotation curves** still invert to the cosmological constant to a **factor ~2 across
~52 a-priori orders** — a real order-of-magnitude concordance. But the clean-distance subset
sits at **~1.85–2.0× Planck (higher than the banked 1.6×)**, i.e. it is NOT converging onto
Planck; if anything the tighter data pulls the inferred Λ **above** it.

## Verdict — TIGHTENS-BUT-NON-DIAGNOSTIC (honest both ways)
Firing the TRGB lever **tightens** the a0-line (16.1%→12.8% error; the estimator-choice
systematic collapses; median and GLS AGREE) but is **non-diagnostic of the footing fork**:
the tightened central is >2σ above canonical and ~1σ above ALT, the Occam separation is only
~1.3 bans, and N=18 galaxies with global Upsilon/gascal now dominating the budget cap the
power. Critically — **the lever leans mildly AGAINST canonical, not toward it**: the
clean-distance central moved UP ~13% and lands near ALT/RAR, so canonical goes to −0.5 bans.
No canonical detection was manufactured (the data disfavors it), and no deficit was
manufactured (the median AGREES with GLS here — both high; the earlier low median was a
Hubble-flow distance artifact). A decisive footing separation needs the **CCHP/EDD TRGB
program** or **BIG-SPARC** to grow the clean-distance N and independent-M/L constraints to
break the now-dominant Upsilon/gascal wall. No "proves."

_Comparison anchors: McGaugh+2016 g† = 1.2e-10; SPARC = Lelli–McGaugh–Schombert 2016._
