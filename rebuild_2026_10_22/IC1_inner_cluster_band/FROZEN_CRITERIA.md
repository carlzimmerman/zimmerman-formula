# IC1_inner_cluster_band — FROZEN CRITERIA (committed alone, before the fix is run)

Written 2026-10-25. κ = ½ FITTED. Footings canonical / alt, calibrated and scored separately, never pooled. Cold dark
energy (not matter, never a particle). Nothing here says the data favour the framework or ΛCDM. Not "theory closed".
Name note: the id IC1 is also used by `IC1_inner_column_cores/` (a different, finished lane); this folder is
`IC1_inner_cluster_band/` and its files carry the prefix `ic1b_`.

## 0. The miss

OS1 (frozen 71873e76d3) passes 14/15 X38 cluster cells out of sample. The one miss is G-IN-Mall (INNER band, all 326
eRASS1 clusters, MGAS500 binning): Z −2.41 / −2.06 at h = 0.672 (canonical / alt), an over-prediction.

## 1. Diagnostics already run (post-run on OS1, labelled, NOT graded; `ic1b_diagnostics.py`, uncommitted at freeze time)

At OS1's q_f (0.892 / 0.748); `ic1b_lib` reproduces OS1's cells exactly (max |Δpred| 0).
- **Terciles.** The over-prediction is uniform, about 2×, in every MGAS500 tercile (M1/M2/M3 Z −1.90/−2.90/−1.58,
  canonical h 0.672) and every KT tercile. M3 carries ~50% of the excess, M2 ~29%, M1 ~20%. No single tercile drives it.
- **Error and weighting.** s_IN is dominated by the cross-shear term A_x (≈ −1.0 vs s_STAT 0.29). The KT-only INNER cell
  is over-predicted by the same factor (pred/meas 2.4–2.6 vs 2.1–2.2). It passes only because its s_IN is larger (1.67 vs
  1.05). At M-all's error it would give Z −2.90 / −2.54. **The measured-KT-only subset is therefore rejected as a fix:**
  it would pass by error size, not by physics.
- **Miscentring.** The record's convention (catalogue miscentring, X-ray fit vs catalogue position, F1/X2 A7) is already
  applied at ×1. Offsets ×0 make the miss worse (−2.78); ×2 would pass (−1.84), but ×2 is a knob, not a record convention.
  **Rejected.**
- **BCG.** A 10¹² M☉ central point mass changes nothing at R ≥ 0.15 Mpc.
- **σ fill.** The 220 filled clusters and the 106 KT clusters are over-predicted alike (Z −2.06 vs −1.81). A regression
  fill (σ_KT on Mgas500) leaves the miss (−2.47). **Not the driver.**
- **Shape.** The non-singular isothermal sphere at OS1's q_f, the same Σ = ρ0 r0, and the same mass rule removes the INNER
  miss (Z +0.27 / +0.24). But it breaks seven MID/OUTER cells (G-OUT-M3 +7.99) and worsens SPARC (0.0707 vs 0.0605).
  That q was calibrated for Burkert, not for this shape.

## 2. The one fix (no new fitted constant)

**F-ISO: replace X38's posited Burkert profile by the non-singular isothermal sphere, the premise of LN1's T7**
(`sidm_core_surface`: an isothermal core with ρ0 r0² = 9σ²/(4πG), King radius r0). That premise is what produces the
core law Σ ∝ σ^q in the first place.
- **Shape.** M(<r) = π Σ r0² B_iso(r/r0), with B_iso = 4 m(x), m(x) = ξ²ψ′(ξ)/27 and ξ = 3x (isothermal Lane–Emden,
  ψ(0) = ψ′(0) = 0). Σ = ρ0 r0 = Σ_a0 (σ_i/σ_ref)^q. Applied to SPARC and to clusters alike.
- **Unchanged.** Everything else is OS1/X38's: mass rule M(r_ta) = M_fair (compact root, A1; saturated if needed), σ
  conventions and the tercile fill, gas, f* = 0.20, offsets, C* denominator, statistics, both h.
- **q.** q is re-calibrated once on SPARC under F-ISO by OS1's exact rule (background A; grid 0.00–1.20 step 0.02, then
  step 0.002 within ±0.02). OS1's q_f belongs to the Burkert shape. If the SPARC line (rms ≤ 0.110,
  0.50 ≤ median Υ ≤ 0.80) fails at q_iso, the footing is FAILS. Background B at q_iso is reported.

## 3. Grade (per footing; the verdict needs both footings to agree, else UNDECIDED)

All 15 X38 cells. A cell passes if |Z| ≤ 2 at both h (0.672, 0.686).

| class | rule |
|---|---|
| **PASS** | SPARC line passes at q_iso **and** all 15 cells pass |
| **IMPROVES** | SPARC line passes, none of OS1's 14 passing cells fails, and G-IN-Mall's max over h of \|Z\| is below OS1's (2.41 / 2.06 at h 0.672; the max over both h is taken from OS1's JSON) but still > 2 |
| **FAILS** | anything else (any OS1-passing cell fails, or the SPARC line fails, or G-IN-Mall is not improved) |

Reported only:
- F-ISO at OS1's Burkert q_f (= diagnostic D4);
- cluster fails at q_iso ± 0.05;
- the saturated-halo count.

Dwarfs are **not graded**: CD1's cap 0.254484 a₀ is a Burkert-derived ceiling, and re-deriving it for the isothermal
shape is outside this lane.

## 4. Checks

- **K0** The Burkert path of `ic1b_lib` reproduces OS1:
  - re-running OS1's calibration rule gives q_f = 0.892 / 0.748 exactly, with SPARC A rms equal to OS1's to 1e-9;
  - the cluster preds at q_f equal OS1's to 1e-9.
- **K1** The isothermal table:
  - B_iso agrees with direct quadrature of 4·∫ρ/ρ0 x² dx from the Lane–Emden solution at x = 0.01, 0.3, 1, 3, 30 to a
    relative 1e-6;
  - the large-x limit gives B_iso(x)/(8x/9) within 2% at x = 10⁴;
  - the small-x limit gives B_iso/(4x³/3) within 1e-3 at x = 1e-3;
  - the solved r0 returns M_fair to 1e-8 for a test cluster.
- **K2** Peak RSS < 2 GB, one thread.
- **MUTATE** (`--mutate`, separate outputs `_MUTATE`): the shape table is replaced by the singular isothermal sphere
  (m = 2x/9 at all x, no core). K1 must FAIL, and the script exits 1 if it does. Its grades are reported, not graded.

## 5. Disclosed before running

- D4 already shows F-ISO at the Burkert q_f fixing INNER while breaking seven MID/OUTER cells by under-prediction. At
  fixed Σ and mass, the isothermal r⁻² tail moves mass out past the bands.
- SPARC was worse under F-ISO at that q. Re-calibration may move q up or down; any change in the cluster cells comes
  only through that one SPARC-fixed number.
- **Expected outcome: FAILS on both footings.** It is written down now. The fix is run because it is the only candidate
  with a derivation in the record (T7's premise); the other two candidates were rejected above on diagnostic grounds.
