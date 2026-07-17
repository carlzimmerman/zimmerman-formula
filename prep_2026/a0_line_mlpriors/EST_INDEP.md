# EST_INDEP — the per-galaxy-independent lane of the a0-line Upsilon split

**Lane question:** re-run the a0-line model-based iterated GLS with the stellar
mass-to-light (Υ) systematic SPLIT into a **coherent SPS/IMF floor** (does NOT average
down) + a **per-galaxy relative part** (averages ~1/√N via external colour/SPS priors).
Does beating Υ drop the residual error below the ~0.98e-11 footing-split threshold and
**decide** whether a0-from-rotation is the dark-energy scale a0 = cH_Λ/Z?

Script: `est_indep.py` (exit 0). Results: `est_indep_results.json`, `_est_indep_console.txt`.
Reuses `../a0_line/fire_common.py` READ-ONLY (data, cuts, fiducials, the biased=False
iterated-GLS guard that killed the fake 3.3e-11 observed-weight deficit).

## Verdict: **TIGHTENS — GAS-CAL (+ estimator spread) IS NOW THE WALL. NON-DECISIVE.**

Beating Υ works mechanically — the coherent/per-galaxy split nearly **halves** sysU
(9.6→5.8e-12 balanced, 7.2e-12 NIR at Ud=0.7). But it does **not** decide the footing
in **any** configuration, and the hard limit proves why: **even with sysU→0 entirely**
(perfect external M/L, coherent floor included) the total error stays **above** the
|Δ|/2 = 9.75e-12 needed to split the footings at 2σ. Υ is **not** the binding wall.

## Numbers (both footings, both Ud, TRGB fD∈{2,3} + full gas)

canonical a0 = 9.355e-11 (cH_Λ/Z) · ALT a0 = 1.1305e-10 (cH0/Z) · gap 20.9% · |Δ|/2 = 9.75e-12

| Ud | set | a0-hat (e-10) | sysU banked | sysU split (bal / NIR) | tot (bal / NIR) | footing sep σ | sysU→0 tot / sep σ |
|----|-----|------|------|------|------|------|------|
| 0.5 | ALLgas | 1.363 | 10.53 | 6.36 / 7.93 | 20.06 / 20.61 | 1.28 / 1.25 | 19.03 / 1.35 |
| 0.5 | TRGB   | 1.490 | 11.52 | 7.04 / 8.73 | 16.06 / 16.87 | 1.75 / 1.66 | 14.43 / 1.94 |
| 0.7 | ALLgas | 1.181 |  9.57 | 5.79 / 7.21 | 17.43 / 17.95 | 1.28 / 1.24 | 16.44 / 1.36 |
| 0.7 | TRGB   | 1.333 | 11.18 | 6.83 / 8.46 | 14.65 / 15.48 | 1.72 / 1.62 | 12.96 / 1.94 |

(all sys/tot in e-12; "sep σ" = convention-robust separation of the two footings in σ,
= |t_canon − t_alt|; bans separation reaches 2.60 at Ud=0.5 TRGB balanced but bans are
convention-fragile — the σ separation is the number that governs.)

**a0-hat shift from the split: exactly 0.000e-12** — the Υ split touches only the error
budget, not the central value (as it must; it is a re-weighting of systematics).

## Reading

1. **The lever fires but the ceiling is low by construction.** At [3.6] most of the
   0.0999-dex Υ scatter is the coherent SPS/IMF zero-point external colours cannot
   touch (NIR-realistic: 0.075 coherent vs 0.040 residual per-galaxy). The per-galaxy
   part that averages down is already tiny — the fully-independent floor of 0.0999 dex
   is only 1.7–3.3e-12 vs the 9.6–11.5e-12 banked coherent number. So the split moves
   sysU from ~10e-12 to ~6–9e-12, no further.

2. **sysU→0 hard limit settles it.** Zero Υ completely: tot = 12.96e-12 (best case,
   Ud=0.7 TRGB), footing separation 1.94σ / 2.23 bans. Still above |Δ|/2, still under
   2σ. **The Υ systematic is not the binding wall** — the framework cannot decide the
   footing by beating M/L even in the perfect-external-prior limit.

3. **What the wall now is:** after the split, on the sharp TRGB set the **largest single
   systematic is gas-cal** sysG = 9.46e-12 (Ud=0.7 TRGB) — bigger than the reduced sysU.
   On the full-gas set the wall is the **estimator-choice spread** sysEst = 10.4e-12
   (GLS vs median disagreement — itself the fingerprint of the nu-shape curvature).
   Below those sit the stat + inclination + distance floor (~8e-12 in quadrature).
   To cross 2σ you need to beat **gas-mass calibration** (needs a better HI/He+H2 scale)
   and grow N (BIG-SPARC) to shrink stat + tame sysEst — not M/L.

## Caveats (carried, honest both ways)

- **a0-hat sits ABOVE both footings** (1.18–1.49e-10). It nominally "leans ALT," but it
  is above ALT too; this is not a clean single-footing detection. The high central is
  soft — see next.
- **Per-point a0 = E/g_bar DECLINES with g_bar** (Ud=0.7 TRGB terciles: 1.62 → 1.25 →
  0.62 e-10). This is nu-shape curvature leaking into the magnitude (the verifier's
  catch); the gb²-weighted estimators are pulled by the high-gb tail. The honest a0 is a
  **box straddling both footings**, not a point that favours one.
- **Literature decomposition, flagged.** No local external per-galaxy colour/SPS M/L
  vector exists for SPARC (L36 is a luminosity; rotmods ship ONE fixed Υ). The
  coherent/per-galaxy split is the defensible literature model (calibration-preserving,
  quadrature ≈ banked 0.0999 dex; it redistributes, does not inflate), cited to
  Schombert-McGaugh-Lelli 2019, Meidt+2014, McGaugh-Schombert 2014, Bell-de Jong 2001,
  Lelli-McGaugh-Schombert 2016 (SPARC).
- **a0's value and the s = −1 sign remain postulates** regardless of this run.

## Bottom line for the a0-line program

Distance was spent (TRGB lever). Now **M/L is spent too**: external per-galaxy Υ priors
tighten sysU but cannot cross the 2-ban / 2σ footing-split line — not even in the
sysU→0 limit. The binding wall has moved to **gas-mass calibration** (a better HI/molecular
scale) plus **sample count** (BIG-SPARC, to shrink stat and the estimator-spread
signature of the nu-shape). Canonical 9.355e-11 vs ALT 1.1305e-10 stays **UNDECIDED**;
the honest result is a box straddling both footings. No footing is proven.
