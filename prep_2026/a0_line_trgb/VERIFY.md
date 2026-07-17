# VERIFY — TRGB lever on the a0-line (adversarial, independent re-derivation)

Scripts re-run, all **exit 0**: `scout_split.py`, `est_gls.py`, `est_robust.py`,
`est_forecast.py`. Independent verifier added: **`verify_trgb.py`** (exit 0) +
`verify_trgb_results.json` + `_verify_console.txt`. Frozen repo `real_research/`
untouched (git status clean); `fire_common.py` imported READ-ONLY for data/cuts only —
the a0 estimators in `verify_trgb.py` are re-implemented from scratch, not trusted from
`fc.budget`.

Footings (both, from `concordance_ledger/anchor_values.json`): canonical
a0=9.355e-11 (cH_Λ/Z) vs ALT 1.1305e-10 (cH0/Z), gap 20.9%. Comparison anchors:
McGaugh+2016 g†=1.2e-10; SPARC = Lelli-McGaugh-Schombert 2016.

---

## (1) Weight-noise-bias fake-deficit trap — CONFIRMED PRESENT & AVOIDED
Re-derived a0 on the TRGB/Cepheid gas set (fD∈{2,3}) three independent, weight-free-or-
model-weighted ways, plus the observed-error-weight control:

| set (Ud=0.7) | OLS unwt | median | model-GLS | **obs-weight (TRAP)** |
|---|---|---|---|---|
| all-gas | 0.959 | 0.973 | 1.181 | **0.455** |
| TRGB | 0.891 | 1.273 | 1.333 | **0.629** |
| Hubble-flow | 0.976 | 0.805 | 0.954 | **0.386** |

Observed-error weighting collapses a0 to 0.45–0.63e-10 on every subset — the same
low-pull mechanism that manufactured the banked 3.3e-11 artifact. The banked/GLS pipeline
uses **model-based** weights (`fc.gls(..., biased=False)`, weights ∝ g_bar² + a0·g_bar,
independent of the kinematic noise in g_obs), so the trap is correctly quarantined. **No
raw observed-error weighting sneaks into the reported number.** Guard holds.

## (1b) NEW adversarial catch — the "moves up to 1.33" is estimator-WEIGHTING-dependent
The three honest estimators do **not** all agree on the TRGB set: median 1.273 and GLS
1.333 agree, but a weight-free **g_bar²-weighted OLS-through-origin gives 0.891** (near
canonical). Cause, from binning per-point a0=E/g_bar by g_bar (TRGB, Ud=0.7):

| g_bar tercile | median a0 |
|---|---|
| deep [0.9–3.0e-12] | **1.62e-10** |
| mid [3.0–5.5e-12] | 1.25e-10 |
| high [5.5–17e-12] | **0.62e-10** |

Per-point a0 **declines steeply with g_bar** (1.62→0.62). The framework predicts
E=a0·g_bar *exactly* (constant slope); the data curve, so the "central a0" depends on
which g_bar points dominate the estimator. Median/GLS weight the deep regime (→1.3),
OLS weights the high-g_bar tail (→0.9). So the banked "central MOVES UP, robust across
estimators" is really **"the deep-regime slope is ~1.3–1.6"**; it is nu-SHAPE curvature
leaking into the magnitude, not a clean single-number a0. This TEMPERS the upward-move
claim and REINFORCES non-diagnostic. (It is honest both ways: the low OLS is *not* a
canonical detection either — g_bar²-weighting is the wrong weighting for the strongly
heteroskedastic E, over-weighting the noisiest high-g points.)

## (2) Selection bias — the TRGB shift is NOT a g_bar-segment artifact
TRGB dwarfs are closer (D_med 4.4 vs 12.5 Mpc) and lower-mass by construction. Test:
restrict the **Hubble-flow-ONLY** set to the TRGB g_bar window and recompute. Result: the
two subsamples already occupy the **same g_bar window** ([~9e-13, 1.7e-11]); range-
matching trims **zero** points (154→154). So the TRGB-vs-Hubble-flow gap (+0.38e-10) is
**0% g_bar-segment** — it is a **distance-scale** difference, not a sampling-of-the-line
artifact. Honest limit: N=18 cannot resolve whether Hubble-flow distances are mildly
biased (suppressing the full-sample a0) OR nearby-dwarf selection lifts the TRGB a0. The
range-match rules out the segment artifact; the distance confound stays open.

## (3) Small-N — bootstrap, no discrimination survives
Galaxy-level bootstrap (N=18 gal, 4000 resamples, GLS): a0 = 1.329
[16–84%: 1.173, 1.486]e-10. This GLS band excludes BOTH canonical (0.935) and ALT
(1.131). BUT because the central is estimator-dependent (OLS 0.89 ↔ GLS 1.33, §1b), any
"canonical excluded" claim flips with estimator choice — **no discrimination claim is
robust to estimator × N=18.**

## (4)/(5) No manufactured detection, no manufactured deficit — both footings
- Not a canonical detection: median/GLS sit 1.3σ–2.8σ *above* canonical.
- Not a manufactured deficit: the low obs-weight 0.63e-10 is the KNOWN trap, quarantined;
  the low OLS 0.89 is wrong-weight, not a deficit signal.
- Honest central straddles both footings across estimators (0.89–1.49e-10).

## (6) Occam bans — prior-convention-fragile; robust reading is σ-tension
Reproduced the banked **log-flat** convention EXACTLY (Ud=0.7 TRGB): canon **−0.49**,
alt **+0.80**, sep 1.29 bans — matches the banked GLS/Robust verdicts. But under a
**linear-flat** prior the same data give canon **+0.19**, alt +1.06 — the ban *sign flips*.
The convention-robust quantity is the σ-tension: **canon −2.75σ (measurement above
canonical), alt −1.28σ**. Under the adversarial informed-prior 15% systematic floor,
footing separation drops to **0.94 bans (log-flat) / 0.63 (lin-flat)** — **NON-DECISIVE
(<2 bans) on every convention.** No footing is selected by the data.

## Λ-inversion (Λ=3Z²a0²/c⁴, Z=5.789, Planck 1.089e-52)
TRGB GLS Ud=0.7 → **2.03× Planck** [1.57, 2.52]; Ud=0.5 → 2.54× [1.93, 3.21]. The clean-
distance subset inverts **higher** than the banked 1.6× — dwarf rotation still inverts to
Λ within a factor ~2 across ~52 a-priori orders, but the TRGB lever pulls **above** Planck,
not onto it (canonical a0 inverts to 1.00× by construction). Not new data — a reframing.

---

## VERDICT — **TIGHTENS-BUT-NON-DIAGNOSTIC, upheld; both footings; honest both ways**

The banked verdict survives adversarial verification and its headline numbers reproduce
exactly (log-flat bans canon −0.49 / alt +0.80; median↔GLS 1.27↔1.33). Three refinements,
all pushing toward *more* caution, none manufacturing a detection or a deficit:

1. The weight-noise trap is real (obs-weight → 0.63e-10) and correctly avoided by the
   model-based GLS — guard confirmed independently.
2. The TRGB-vs-Hubble-flow gap is distance-scale, **not** a g_bar-segment selection
   artifact (samples share the g_bar window); the distance confound is unresolved at N=18.
3. **The "central moves up to 1.33" is estimator-weighting-dependent** — a weight-free
   g_bar²-OLS gives 0.89e-10 (near canonical) because per-point a0 declines steeply with
   g_bar (nu-shape curvature). The robust reading is "deep-regime slope ~1.3–1.6," not a
   clean single a0.

Neither footing is detected: canonical sits ~2.75σ low, ALT ~1.3σ low, footing separation
**≤1.3 bans and <1 ban under the adversarial floor** — below the 2-ban decisive line on
both prior conventions. The Occam-ban sign is itself prior-convention-fragile. The wall is
the global M/L + gas-cal + nu-shape systematic, not the distance flag (which the lever *does*
cut ~2–3.5× as advertised). To become diagnostic needs the CCHP/EDD TRGB program or
BIG-SPARC — more clean-distance dwarfs, external M/L priors, and any points reaching y~1 to
break the magnitude/shape degeneracy. **No "proves"; no manufactured canonical detection;
no manufactured deficit.**
