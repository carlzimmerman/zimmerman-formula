# CFG443: in CFG378's settled two-species boxes, is the cold component in massive halos more concentrated than the law's target (the X-COP "NEITHER" shape)? FROZEN before any CFG378 output was read

Owner chat 10-06 ("swing all of em"); agreed with the orchestrating session, which owns CFG378: read-only analysis, run only after CFG378's verdict is committed. κ = ½ fitted; both footings. No DM particle; the cold mass is still required. **At the time of freezing, no CFG378 256³ output has been opened by this session.**

**Why.** CFG440 session05 found the X-COP mass beyond the law more centrally concentrated than both the law's phantom and the baryons (log-slopes of the ratios −0.46 ± 0.07 and −0.33 ± 0.07 over 0.1–1 Mpc). CFG378's declared settling scheme relaxes the cold density geometrically toward the target, and is **two-sided** (it pushes cold OUT where ρ_c > ρ_t in ON cells). So it should drive halos toward the target shape, not the X-COP shape. This lane measures which one the box actually produces.

**Inputs (read-only).** `../_external_data/cfg378_work/cfg378_<tag>_z0.npz` (pos_c, pos_b) for the four frozen 256³ runs ({g = 1, g = 0.1} × {canonical, alt}), and a g = 0 run as the no-settling reference: at 256³ if CFG378 made one; otherwise the 128³ DEV g = 0 run, compared only with 128³ DEV runs, labelled as such. Fields: CIC (the engine's `deposit_raw`) for ρ_c and ρ_b; ρ_t from the engine's own `target_field` (imported from `../CFG378_two_fluid_ot_settling/cfg378_pm.py`, never edited), at a = 1, per footing.

**Halos.** The 20 highest local maxima of the total density (ρ = f_b ρ_b + (1 − f_b) ρ_c, smoothed with a 1-cell Gaussian), mutually separated by ≥ 8 cells. Centre = the maximum's cell.

**Profiles.** Cumulative M_c(<r), M_t(<r) and M_b(<r) in spheres of r = 2, 3, 4, 6 cells (1.6–4.7 Mpc/h at 0.78 Mpc/h per cell). r = 1 cell is excluded (CIC-dominated).

**Statistic.** Per halo, the OLS slope against log r of log(M_c/M_t) and of log(M_c/M_b). Median over the 20 halos, bootstrap over halos (2000, seed 61). Per run, and the g = 1 minus g = 0 difference of medians.

**Verdict per run (g = 1 primary).**
- **X-COP-LIKE** if the median slope of log(M_c/M_t) < −0.1 at > 3σ.
- **TARGET-SHAPED** if it is within 2σ of 0.
- **ANTI-CONCENTRATED** if it is > +0.1 at > 3σ.
- Otherwise INCONCLUSIVE.
- The settling effect is measurable only if |g = 1 − g = 0| > 2σ (otherwise "settling invisible at these radii").

**Declared limit.** The resolvable radii (1.6–4.7 Mpc/h) lie at and beyond the X-COP clusters' R500 (~1–1.4 Mpc), with **no overlap** with X-COP's 0.1–1 Mpc. So any verdict says what the scheme produces at resolvable scales. It cannot confirm or refute the X-COP shape directly. A zoom or higher-resolution box would be needed for that.

**Controls.**
- K1: the deposited cold total equals the cold particle count to 1e-10 relative.
- K2: at z = 0, Q = Σ f·ρ_c / Σ f·ρ_t recomputed here (with the engine's `switch_field` and its turnaround table) matches CFG378's reported z = 0 Q for the same run to 1e-3 relative. If CFG378 does not report Q at z = 0 for a run, K2 is reported as not applicable for that run.

**MUTATE (`--mutate`).** The cold positions are replaced by the baryon positions (cold traces baryons by construction). The median slope of log(M_c/M_b) must be |·| < 0.01 on the canonical g = 1 run; exit 1 when that is detected.
