# CFG220 — CRISTAL at the outer radius on the INDEPENDENT baryon route (class A only), and the calibration that would reverse it

- **Criteria:** `FROZEN_CRITERIA.md` (2e025c40e), committed before the independent-route numbers. **κ = ½ is FITTED, NOT DERIVED.** Author decompositions, not a direct a₀ measurement. **Not blind:** CFG213's fit-route outer numbers and its R_e route swap were known.
- **Run:** `python3 campaign_fresh_gravity/CFG220_cristal_outer_independent/cfg220_outer_independent.py` (a few seconds; `MUTATE=1` runs the response control), `cfg220_plot.py` for the chart. Controls C1–C4 pass (C1 reproduces CFG213's committed twelve-disc outer-radius medians, max difference 4.9e-4 against its three-decimal values), MUTATE passes.
- **Sample:** the six CRISTAL discs with an SED M★ and a dust-DETECTED gas mass (02, 03, 07a, 11, 19, 20). Vector curves and radii from `cristal_outer_summary.csv` (table R_out and the outermost data marker); baryon normalisation from M★/(1 − f_molgas) against the fit's M_bary, the curve shape being the fit's.

## Bottom line

- **No separation.** Independent route, table R_out, ν_mono, canonical (n = 6): flat **+0.106 [−0.138, +0.343] CONSISTENT**, rival **−0.203 [−0.477, +0.029] CONSISTENT** → **BOTH-CONSISTENT**. Across the eight cells (2 kernels × 2 footings × 2 radius definitions) seven are BOTH-CONSISTENT and one (ν_mono, alt footing, table R_out, the rival's CI upper edge at −0.004) is FLAT-SUPPORTED: **KERNEL/FOOTING/RADIUS-DEPENDENT**. **Not LOO-robust** (dropping CRISTAL-11 gives FLAT-SUPPORTED). **CALIBRATION-LIMITED.**
- **The route decides it, and two discs decide the route.** The fit route on the same six discs is FLAT-SUPPORTED in all eight cells (flat +0.019, rival −0.283). The independent route removes that because the SED + dust baryon masses of **CRISTAL-11 and -19 are 0.35 and 0.47 dex below the fit's M_bary** (route factors log ρ: 02 +0.04, 03 +0.06, 07a +0.04, 11 −0.35, 19 −0.47, 20 +0.09), so their D goes from 1.4 and 1.2 to 3.2 and 3.4 at g_bar/a₀ of 1.6 and 1.0.
- **The calibration flip is small.** With a uniform gas-mass offset τ on all six discs (τ = 0 is the dust-based gas): BOTH-CONSISTENT for τ < +0.07 dex, **FLAT-SUPPORTED for +0.07 ≤ τ < +0.54, BOTH-DISFAVOURED beyond**, and **never RIVAL-SUPPORTED anywhere in |τ| ≤ 1**. The class changes at +0.07 dex, 0.3 × the 0.25 dex baseline. The flat law's median δ is 0 at τ = +0.33 (gas ×2.1).
- **The rival's median never reaches 0.** It is −0.20 at τ = 0 and stays below 0 for every τ (**−0.09 even with no gas at all**, τ = −3). That its CI includes 0 at τ = 0 (upper edge +0.029) is the six-disc scatter, not the median. This is a statement about the rival a₀ ∝ E(z) at these six discs, not a detection of anything for the flat law, whose own median is +0.11 and needs more gas than the dust says.
- **Against the forecast** (CFG219, R_out, six discs): the realised (δ_flat, δ_rival) = (+0.106, −0.203) sits between flat-true (0, −0.34) and rival-true (+0.28, 0): 0.9 and 1.4 scatters from flat-true, 1.5 and 2.1 from rival-true (CFG219's τ = 0.25 total scatter, 0.10 to 0.12). Closer to flat-true, neither rejected; a description, not a test (a thin-disc model baryon curve there, the fit's here).
- **Post hoc (reported only): the forecast's scatter was optimistic.** The disc-to-disc scatter of the realised δ is **0.25 dex for the rival and 0.24 for the flat law** (sd of the six per-disc values), against **0.14** per disc from CFG219's baryon-error-only noise at R_out, about **1.8× larger**. The excess is what the forecast omitted (velocity and f_DM errors, bulge, geometry, the fit's baryon shape); if it is random, the number of discs CFG219 gives for 3σ grows by about 1.8² ≈ 3, and its N values are lower bounds. Six discs make the ratio uncertain by about ±30%.

## One-sided bounds (the three dust upper limits; never entered in a median)

| disc | δ_flat ≥ | δ_rival ≥ |
|---|---|---|
| CRISTAL-08 | +0.328 | −0.024 |
| CRISTAL-12 | −0.076 | −0.443 |
| CRISTAL-23b | −0.209 | −0.403 |

One of three lower bounds lies above the six-disc median for each law: they carry no information beyond the six.

## Per disc (independent route, table R_out, ν_mono, canonical)

| disc | z | R (kpc) | g_bar/a₀ (fit) | D_ind (D_fit) | δ_flat | δ_rival |
|---|---|---|---|---|---|---|
| 02 | 5.294 | 8.10 | 0.77 (0.69) | 1.03 (1.14) | −0.221 | −0.582 |
| 03 | 5.689 | 3.45 | 4.40 (3.83) | 1.02 (1.17) | −0.054 | −0.304 |
| 07a | 5.154 | 4.20 | 1.10 (1.00) | 2.62 (2.91) | +0.232 | −0.102 |
| 11 | 4.439 | 4.35 | 1.58 (3.54) | 3.21 (1.43) | +0.360 | +0.079 |
| 19 | 5.233 | 3.91 | 0.96 (2.80) | 3.39 (1.16) | +0.326 | −0.021 |
| 20 | 5.545 | 5.25 | 1.08 (0.89) | 1.48 (1.80) | −0.021 | −0.373 |

## Limits and disclosures

- n = 6 and the bootstrap sees only the disc-to-disc scatter, not the SED or f_molgas errors. The curves are the authors' model curves, extrapolated beyond the last marker; the pressure correction is theirs; only the baryon normalisation changes, the shape stays the fit's.
- The class labels come from bootstrap CIs and are discontinuous in τ: the flip at +0.07 dex is the rival's CI upper edge crossing 0, not a jump in the median.
- C1's frozen tolerance was 1e-3 against CFG213's committed three-decimal values; the maximum difference is 4.9e-4 (rounding).
- The forecast-scatter comparison and the τ = −3 (no gas) remark are post hoc.
- Nothing here says the data favour the framework: the outcome is BOTH-CONSISTENT, calibration-limited and not LOO-robust.

## Chart

`cfg220_calibration_scan.png` (from `cfg220_plot.py`, the lane's own functions): each law's median δ and 95% CI against the gas-mass offset τ, the class windows below, the fit route's medians as diamonds at the left.
