# CFG407: X43's total mass vs X-COP hydrostatic mass at R500–R200. CONSISTENT (frozen); measured baryons flip it to MIXED

**Read first.**
- **Frozen reading (PRIMARY, X43's own recipe): CONSISTENT** in all four footing × h cells. The native background (V-NAT) agrees.
- **Flagged class change: V-MEAS is MIXED.** With X-COP's measured baryons, X-COP exceeds X43 by +0.054 / +0.063 dex (Z 1.8 / 2.2). That is EXCESS CONFIRMED in the two h0686 cells and CONSISTENT in the two h0672 cells.
- **Post hoc, labelled:** the flip comes almost entirely from **stars**. X-COP's measured M★/M_gas(<R500) is 0.035–0.074, against the 0.20 that X43 assumes. X43's agreement with X-COP rests on that stellar fraction.
- **Inherited inputs:** PRIMARY uses X43 as committed, including the Planck ratio 5.364 and X30's H0 67.4 in r_ta, which conflict with the owner's 10-25 rule. V-NAT is the native counterpart (5.2715; L1 / CFG886; K5 confirmed `B_cfg886_bg` is the same fit).

## Process
- Criteria: `FROZEN_CRITERIA.md` (65226042e3, committed alone).
- Script: `cfg407_xcop_outer.py`, committed before its first execution (addeed8f74).
- That first execution stopped at data load: `A1644_mstar.fits` does not exist. It stopped after K1 and K2 and before any X-COP number. **AMENDMENT A1** (3a148acc8c, committed alone) corrects the data section: only 7 of 12 clusters have stellar files. It gives V-MEAS a fallback for the 5 without (stars = 0.20 × measured gas) and adds V-MEAS-7. The script change was committed in 50b27ec7cd.
- One graded run: single thread, niced, 49 s, RSS < 1 GB. MUTATE was a separate run.
- κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

**Controls 5/5 PASS:**
- K1: X43's machinery reproduces its committed G-OUT-M3 / G-OUT-all predictions exactly.
- K2: the single-cluster rule equals X43's in-loop expression exactly.
- K3: X-COP units, max deviation 1.4 %.
- K4: coverage. Gas is short of 0.95 R200 for A3266 (0.69), ZW1215 (0.93) and A1644 (0.95). They are kept and flagged.
- K5: background identity, exact.

**MUTATE** (reversed-M500 pairing): the scatter of Δ_i goes 0.090 → 0.195 dex in every cell, rc 1.

## Results
Δ = log10[M_HSE/(1 − b)/M_X43], averaged over 5 radii from R500 to R200; se = cluster scatter/√N. The two footings agree to the printed precision: at these masses the collapse core rules, not the a₀ floor.

| variant | h cell | Δ̄ (b = 0) | Z | Δ̄ (b = 0.3) | class |
|---|---|---|---|---|---|
| **PRIMARY** (X43 recipe) | 0.672 | **−0.016 ± 0.026** | −0.62 | +0.139 | CONSISTENT (b* 0.036) |
| | 0.686 | −0.008 ± 0.026 | −0.30 | +0.147 | CONSISTENT (b* 0.018) |
| V-NAT (native 5.2715) | 0.672 / 0.686 | −0.010 / −0.001 ± 0.026 | −0.38 / −0.06 | +0.145 / +0.153 | CONSISTENT |
| V-MEAS (12; 5 with fallback stars) | 0.672 / 0.686 | **+0.054 / +0.063 ± 0.029** | +1.84 / +2.16 | +0.209 / +0.218 | CONSISTENT / EXCESS → **MIXED** |
| V-MEAS-7 (measured stars only) | 0.672 / 0.686 | +0.068 / +0.077 ± 0.047 | +1.44 / +1.64 | +0.223 / +0.232 | CONSISTENT |
| V-INNER (0.3–0.7 R500, reported) | 0.672 | −0.048 ± 0.024 | — | — | — |

**Per cluster (PRIMARY, canonical, h 0.672, b = 0):** A1644 −0.012, A1795 −0.051, A2029 +0.012, A2142 −0.009, A2255 −0.010, A2319 −0.135, A3158 −0.012, A3266 +0.089, A644 −0.181, A85 −0.049, RXC1825 +0.001, ZW1215 +0.165.
- The scatter (0.09 dex) is real. It is set by disturbed systems (A644, A2319, ZW1215, A3266), not by the measurement errors (χ² 811/60).
- No cluster was excluded.

## Reading
1. **Frozen: CONSISTENT.**
   - X43's own recipe predicts X-COP's hydrostatic mass at R500–R200 to within 4 % on average.
   - It needs only 2–4 % non-thermal support (b*). Any larger non-thermal pressure would put the true mass slightly *above* X43, within these errors.
   - On X43's own recipe, X-COP does **not** confirm the KiDS heavy-cluster excess (KiDS: +0.087 dex in projected ΔΣ at 1.42–3 Mpc; X-COP: −0.016 dex in 3-D mass).
2. **Your native background changes nothing.** It moves Δ̄ by +0.006 to +0.007 dex, slightly toward agreement.
3. **Post hoc, labelled: the agreement rests on X43's stellar fraction.**
   - Switching to measured baryons moves the 7 clusters *with* measured stars by +0.069 to +0.160 dex. It moves the 5 using the 0.20 fallback by −0.004 to +0.054 dex.
   - X-COP's measured M★/M_gas(<R500) is 0.035 / 0.071 / 0.062 / 0.074 / 0.065 / 0.048 / 0.053 (A85, A644, A1795, A2029, A2142, A2319, ZW1215). That is about 3× below X43's 0.20.
   - Because X43 ties the cold mass to the baryons (M_fair = 5.364 M_bt), the extra assumed stars inflate the whole prediction.
   - With measured stars, X-COP sits **above** X43 by about +0.05 to +0.08 dex (1.4–2.2σ). That is the same sign and about the same size as KiDS's +0.087 dex. CFG922 had already flagged, for cores, that the measured stars are fewer than f★ = 0.20.
4. **What this means for the heavy-cluster question.**
   - On X43 as committed, the excess is **not confirmed**.
   - On measured baryons, X-COP **leans the same way as KiDS** at under 2.2σ.
   - The same f★ = 0.20 sits inside X43's KiDS predictions. With realistic stars, X43's heavy-cluster lensing prediction would also drop, and G-OUT-M3's gap would *widen*.
   - The honest summary: **the heavy-cluster under-supply is not ruled out, and X43's stellar-fraction assumption is masking part of it.** This is not a frozen claim. A frozen test of X43 with measured stellar fractions (on KiDS via a stellar-mass–gas-mass relation, and on X-COP-7) would decide it.
5. **Inner region (reported):** X43 sits slightly above X-COP at 0.3–0.7 R500 (−0.048 ± 0.024), the cores-too-dense direction already seen in IB1 / CS1. So the outer result is not a global offset.

## Files
`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `cfg407_xcop_outer.py` (run plainly; `MUTATE=1` for the reversed pairing), `cfg407.out`, `cfg407_results.json` (every Δ_ik, Δ_i, se, χ², q and coverage), `cfg407_MUTATE.out`, `cfg407_results_MUTATE.json`. The X30 machinery log is redirected here (gitignored).
