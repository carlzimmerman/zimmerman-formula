# CFG408: X43 with measured stellar fractions. KiDS part INVALID (frozen K2); X-COP CONSISTENT

**Read first.**
- **KiDS part: INVALID as frozen.** Control K2 required ≥ 300 of the 326 X7/X30 clusters to match CFG922's stellar census within 30″. **281 matched.** X7's sample and CFG687's 318 are different selections, and 45 X7 clusters are not in the census. The census itself reproduced exactly (0.0340 / 0.2165 / 33). The 300 threshold was my pre-freeze guess, and it was wrong. Under the frozen rule the KiDS grades and the combined label are **not graded**. Their numbers are reported below as such.
- **X-COP part: CONSISTENT (frozen),** in all four cells.
- **Correction to CFG407's post-hoc note:** measured stars are only **~42 %** of CFG407's V-MEAS shift. The rest (~58 %) is X-COP's measured **gas**, which is lower than X43's β-model at large radius. CFG407's README carries a dated correction.
- **Inherited inputs:** X43 as committed, including the Planck ratio 5.364 and H0 67.4 in M_fair / r_ta (owner's 10-25 rule; flagged). X-NAT is the native counterpart for X-COP.

## Process
- Criteria: 34cb560b1d (committed alone).
- Script: b63cfacbc6, committed before its first run.
- One main run: 468 s, single thread, niced. MUTATE was a separate run. No amendment.
- κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

**Controls:**
- **K1 PASS:** f★ = 0.20 through the injection reproduces every committed X43 cluster cell exactly.
- **T3M PASS.**
- **K2 FAIL:** match 281/326.
- **K3 PASS:** X-COP at f★ = 0.20 reproduces CFG407's PRIMARY exactly.
- **K4 PASS:** the X-COP f★ re-read.
- **K5 FAIL as frozen:** the error rescaling is off by 0.17 %, so the stored-X7 keys are marked APPROXIMATE, as in CFG406.

**MUTATE** (f★ = 0.60): KiDS G-OUT-M3 pred 1.120 → 1.204 (canonical) and 1.028 → 1.106 (alt). X-COP Δ̄ −0.016 → −0.115. rc 1.

## Measured stellar fractions used
| source | light / middle / heavy (observed-Mgas500 terciles) |
|---|---|
| CFG922 A1 central, S/gas_cyl (< 0.5 Mpc), **PRIMARY** | 0.0340 / 0.0340 / 0.0339 |
| CFG922 A1 upper | 0.116 / 0.089 / 0.080 |
| CFG922 frozen central | 0.011 / 0.010 / 0.014 |
| X-COP-7, M★/M_gas (< R500) | 0.035–0.074, median 0.0615 |

All of these are **far below X43's assumed 0.20**.

The A1 central medians are flat because 33 unmeasured clusters carry A1's fill value (the global median, 0.0340), and the tercile medians land on it. So the census does not resolve a mass trend at this depth.

## X-COP part (graded): CONSISTENT
X43's recipe gas, with M_b = Mg_P (1 + f★,i). Δ = log10[M_HSE/(1−b)/M_X43] over [R500, R200]. The two footings are identical.

| variant | Δ̄ (b = 0), h 0.672 / 0.686 | class |
|---|---|---|
| **X-PRIMARY** (12; 7 measured, 5 at the median) | **+0.028 / +0.036 ± 0.026** (Z 1.06 / 1.37) | CONSISTENT |
| X-7 (measured only) | +0.009 / +0.017 ± 0.042 | CONSISTENT |
| X-PROF (measured stellar *profiles*, 7) | +0.011 / +0.019 ± 0.043 | CONSISTENT |
| X-NAT (native 5.2715) | +0.034 / +0.042 ± 0.026 | CONSISTENT |
| *(CFG407 PRIMARY, f★ = 0.20, for reference)* | −0.016 / −0.008 ± 0.026 | CONSISTENT |

**With measured stars and X43's own gas recipe, X43 matches X-COP's hydrostatic mass at R500–R200 to within about 0.01–0.04 dex.**

## KiDS part (NOT GRADED: K2 failed; reported only)
G-OUT-M3 fails as an UNDER-prediction in **every** f★ variant, and gets worse than X43's committed Z 2.41:

| f★ variant | G-OUT-M3 Z (h0672 / h0686), canonical | other failures |
|---|---|---|
| f★ = 0.20 (= X43) | +2.41 / +2.07 | none |
| F-TERC (A1 central, 0.034) | **+3.66 / +3.27** | none (G-OUT-Mall +1.55 / +1.71) |
| F-UP / F-CLUSTER / F-FROZEN / F-XCOP | +2.93 to +3.81 | none |

The groups key is unchanged at Z +2.05 (out of scope). The four stored-X7 keys are APPROXIMATE (K5).

## What this means (post hoc, labelled; nothing here is a frozen claim)
1. **Against X-COP (to R200), X43 is fine with measured stars.** The CFG407 V-MEAS lean (+0.05 to +0.08 dex) came more from X-COP's measured gas (steeper than X43's β-model beyond R500) than from stars. With measured stars alone, the residual is about +0.01 to +0.04 dex.
2. **Against KiDS (1.42–3 Mpc), the heavy-cluster shortfall gets *worse* with measured stars** (Z about 2.9–3.8 across variants), and nothing else breaks. That number is not graded here because of K2.
3. **The two probes cover different radii.** X-COP stops at R200 (about 1.8–2.2 Mpc for these clusters), while KiDS's OUTER band runs to 3 Mpc. A shortfall that X-COP doesn't see but KiDS does would sit mostly **beyond R200, in the infall region.** That is where X43's cold halo is truncated at r_ta and capped at the fair share. This is a hypothesis for a next lane, not a result.
4. **To grade the KiDS half properly:** rerun with K2's match requirement set on the X7 sample's census coverage (or a census of the 45 unmatched clusters). That would need a fresh frozen file or an amendment, and it is the owner's call.

## Files
`FROZEN_CRITERIA.md`, `cfg408_measured_fstar.py` (run plainly; `MUTATE=1`; `--x43 TAG` is internal), `cfg408.out`, `cfg408_results.json`, `cfg408_MUTATE.out`, `cfg408_results_MUTATE.json`. Per child run: `cfg408_fstar_*.json`, `cfg408_x43_*_meas.json` / `_arrays.npz`, `x43_collapse_core_*.out` / `_results_*.json`. The X30 machinery logs are gitignored.
