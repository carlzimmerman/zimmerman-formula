# CFG495: the cold-fluid drawdown around every halo, and its KiDS lensing signature. EXCLUDED by the frozen rule, but NOT ROBUST and MODEL-INADEQUATE. In substance KiDS cannot separate the drawdown from halo mass

The criteria were committed alone, after the simulation and prediction steps and before the shear signal was read (a703a87da). On-disk data only; no downloads.
- κ = ½ is fitted.
- The cold mass is still required, and no particle species is added.
- The footings 9.3603e-11 and 1.1312e-10 are scored separately and never pooled.
- Nothing here says the data favour the framework.

## Bottom line
1. **The simulations show the drawdown.** Around resolved group halos in the zero-knob runs (512³, two seeds, both footings), the cold fluid is depleted by **8–17%** between r_edge and r_ta, and by 30% around clusters. The depletion does not stop at r_ta: overlapping catchments carry 8–15% out to 2 r_ta. Against the matched ΛCDM-equivalent control (S0):
   - the total effective density has a **−4 to −11% deficit at 0.35–0.55 r_ta**, −3 to −6% at 0.75–0.95 r_ta, and −1 to −3% at 1.15 r_ta;
   - ΔΣ falls by **−1 to −7%** at 0.55–1.15 r_ta;
   - clusters instead show a +4 to +20% excess;
   - the drawdown term alone is −5.5 to −12.5% of the control's ΔΣ (groups) and −26% (clusters).
   - **These amplitudes are mesh-limited lower bounds.** The per-host q is 0.03–0.13 at 512³, against the continuum engine rule's 0.53–0.62 at the same masses, because the edge is about one cell.
2. **The prediction for KiDS lenses is large but not distinctive.** The engine rule applied to one isolated lens (log M* 10.5–11, z ≈ 0.3) gives q = 0.34 / 0.36 (log M* 10.5, canonical / alt), 0.30 / 0.31 (10.75) and 0.14 / 0.18 (11.0). The drawdown lowers the stacked ΔΣ by **18–24% in every bin from 0.05 to 2.2 Mpc**. Because the draw is proportional to the cold density, that is nearly a uniform rescaling of the cold halo, which is **degenerate with the halo mass**. This was stated in the criteria before the test.
3. **The test, by the frozen rule: EXCLUDED on both footings, with two labels that make it non-decisive.**
   - With Moster+13 halo masses and the frozen two-halo term, the data disfavour the drawdown: Δχ² +81.1 (canonical) / +79.7 (alt). The fitted amplitude is A = −0.32 ± 0.14 / −0.20 ± 0.13, against the predicted 1.
   - **NOT ROBUST:** with halo masses 0.2 dex heavier, the verdict flips to DETECTED: Δχ² −52.8 / −58.5, A = 1.01 ± 0.14 / 0.97 ± 0.13. The sign of the result is set by the stellar-to-halo-mass normalisation, not by the drawdown.
   - **MODEL-INADEQUATE:** no frozen model fits the stack. Best χ² is 122.7–128.5 / 15, p ≈ 1e-19. The outer bins (0.98 Msun/pc² at 2.17 Mpc) sit far above every frozen model (0.26–0.37).
   - So this is not a measurement of the drawdown. **KiDS alone cannot test it.**

## Step 1: simulation (`cfg495_sim.py`, `cfg495_sim_analysis.py`)
**Inputs.** The z = 0 snapshots of CFG425/439/460 (512³: seed 360 canonical, seed 359 canonical and alt) and CFG424 (256³: canonical, alt, NOCOMP). The matched-seed S0 controls are CFG460's seed-360 run, CFG411's seed-359 512³ run and CFG359's 256³ run; identical initial conditions are confirmed by σ₈(z_i).

**Method.** The source fields are recomputed with the CFG424 engine's own functions, imported read-only:
- **K1:** the engine's q_max is reproduced to < 1e-6.
- **K2:** the source sums to zero per catchment.
- **K3:** the peak catalogue rebuilds the engine's catchment and edge masks with zero mismatch.

**Stacks (512³, groups log M_ta 13.2–14.2 Msun/h; clusters ≥ 14.2; 7,600–7,700 resolved hosts per run):**

| quantity | groups | clusters |
|---|---|---|
| cold depletion depth, r_edge–r_ta | 0.08–0.17 | 0.30 |
| depletion at 1–2 r_ta (overlapping catchments) | 0.08–0.15 | 0.21–0.22 |
| effective density − S0, 0.35–0.55 r_ta | −4 to −11% | +6 to +13% |
| ΔΣ (TA total − S0), 0.55–1.15 r_ta | −1 to −7% | +4 to +20% |
| ΔΣ of the drawdown alone, 0.3–1 r_ta | −5.5 to −12.5% | −26% |
| per-host q (sim) vs continuum rule | 0.03–0.13 vs 0.53–0.62 | 0.29–0.30 vs 0.45–0.47 |

The edge positions x_edge = 0.17–0.34 match the analytic edge to 1e-3.

**The outer-shell-only variant** draws Σe only from catchment cells outside the edge balls, recomputed statically at z = 0, with no rerun.
- It overdraws (q_sh > 1) in 2–14% of catchment mass at 512³.
- Its ΔΣ is −0.1 to −0.6 h Msun/pc² beyond 0.5 r_ta.

**The NOCOMP dynamical run (256³)** differs from the full run's particles by at most 0.35 h Msun/pc² (clusters). The drawdown's lensing is mostly the source term, not the particles' response.

## Step 2: prediction (`cfg495_lenslib.py`, `cfg495_predict.py`)
This step read only the lens catalogue and pair weights.

**The engine rule written for one lens:**
- the ΛCDM-equivalent matter is an NFW profile (Moster+13 M200c, Duffy+08 c; **(U): recalled, not on disk**), out to r_ta;
- f_ret = M_gal/(f_b M_ta);
- r_edge = r_M/ln(1 + f_ret f_b/(1−f_b));
- M_e = ∫_{r<r_edge} max(ρ_ph − ρ_c, 0) dV;
- PROP = −(M_e/M_c(<r_ta)) ρ_c.

| log M* | r_ta (Mpc) | r_edge can / alt | q can / alt | ΔΣ_dd at 0.1 / 0.3 / 0.6 / 1 / 2 Mpc (can, Msun/pc²) |
|---|---|---|---|---|
| 10.5 | 0.91 | 0.40 / 0.36 | 0.34 / 0.36 | −4.6 / −1.24 / −0.46 / −0.22 / −0.05 |
| 10.75 | 1.21 | 0.70 / 0.63 | 0.30 / 0.31 | −6.7 / −2.0 / −0.80 / −0.38 / −0.11 |
| 11.0 | 2.03 | = r_ta | 0.14 / 0.18 | −6.8 / −2.7 / −1.2 / −0.61 / −0.23 |

- **Stack:** PROP / (F_nodd + 2h) is −0.18 to −0.24 in all 15 bins.
- **Shell-only variant:** infeasible for 75–87% of lens groups (the shell holds less cold fluid than the phantom excess needs).
- **Frozen two-halo term.** This is the S0 control's lensing by everything outside each lens's r_ta ball, around isolated (iso05) peaks of matching M_ta. It is nearly zero: as CFG377's R^-0.8 amplitude, A_equiv = −0.02. CFG413/486's free fits needed 0.95–1.57.

## Step 3: test (`cfg495_test.py`)
**Data:** CFG377's primary stack (181,477 lenses, 15 bins, 50-patch jackknife, Hartlap 0.6735).

χ² / 15:

| model | canonical | alt |
|---|---|---|
| LCDM (NFW + frozen 2h) | 189.1 | 189.1 |
| F_nodd (law to r_edge + undrawn cold) | 128.5 | 122.7 |
| **F_dd (+ drawdown, the prediction)** | **209.6** | **202.4** |
| F_shell (variant) | 152.7 | 151.0 |
| PILEUP (opposite sign, MUTATE) | 146.8 | 156.9 |

**Sensitivity**, as Δχ² (F_dd − F_nodd), canonical / alt:
- **two-halo variants** (iso1, all, D¹, D⁰, none): +78.6 to +82.0;
- **f30 strict isolation:** +11.0 / +9.8;
- **halo mass −0.2 dex:** +140 / +137;
- **halo mass +0.2 dex: −52.8 / −58.5. This row flips the verdict.**

**Reported only (not in the verdict):**
- **Trusted 9 inner bins:** +30.1 / +26.8.
- **Free R^-0.8 two-halo amplitude (CFG413 floor):** F_dd fits best: χ² 20.9 against 66.1 (F_nodd) and 79.4 (LCDM), with A = 1.03. That template's amplitude was judged implausible as a two-halo term in CFG486. **This is not a detection.**

## Controls and MUTATE (all pass)
- **C1 / C2:** the data vector reproduces CFG377 exactly; 15 bins.
- **Opposite sign:** the pile-up is not preferred (+18.3 / +34.2 against F_nodd).
- **Simulation, shuffled centres:** the drawdown falls to ≤ 2% of its halo-centred amplitude in every mass bin, at both 512³ and 256³.
- **KiDS, lens positions displaced 1–2°** (`cfg495_stage_random.py`, the CFG110 estimator verbatim; 147,849 positions with sources): A = −0.05 ± 0.13 / −0.04 ± 0.12.
- **KiDS cross shear (CFG116):** A = +0.16 ± 0.15 / +0.15 ± 0.14.

## Correction made after the freeze (kept on the record)
**The bug.** The first run (`*_v1_prefix.*`) had a bug in the simulation's ΔΣ estimator. On the 0.39 Mpc/h lattice some thin annuli contain no cell centres. Those annuli were given a mean of 0, so ΔΣ there returned the inner mean, a spurious value.

**How it showed up.** The simulation MUTATE (shuffled centres) **failed** in the lowest mass bins (ratio 0.27–0.39).

**The fix.** Empty annuli are now NaN, and the stacks use NaN-aware means. The shuffled-centre control then passes.

**What the bug affected:**
- the simulation ΔΣ stacks;
- the frozen two-halo template, whose A_equiv went from 0.07 to −0.02.

**What it did not affect:**
- the analytic drawdown prediction (PROP), which is unchanged;
- the verdict: v1 gave Δχ² +75.1 / +73.3 with the same labels; v2 gives +81.1 / +79.7.

The FROZEN_CRITERIA Step 1 numbers were taken from v1. The corrected values are the ones in the table above. The corrected drawdown-only range is −5.5 to −12.5% (v1 quoted −9 to −12%).

## What would decide it (needs owner go; no download made)
- **Proportional draw.** Because the draw is degenerate with halo mass, KiDS stacks need an **independent halo-mass calibration good to about 0.04 dex** for isolated lenses. Candidate sources are satellite kinematics, or abundance matching with controlled systematics. The halo mass would then be fixed rather than recalled.
- **A shape-sensitive test.** It must compare the lensing mass inside r_ta with the turnaround mass from infall kinematics around the same isolated lenses; the drawdown conserves M(<r_ta) and the no-drawdown reading does not.
- **The outer-shell reading** is ruled out by its own mass budget for typical KiDS lenses, so it is not a target.
- **The baseline must fit first.** A two-halo/environment model for isolated lenses that actually fits the outer KiDS bins (p > 0.001) is needed before any drawdown verdict can be read. This repeats CFG413/486's open need.

## Caveats
- **Simulation:**
  - The drawdown is engine bookkeeping (a Poisson source term), not moved cold fluid.
  - The edge is one cell, so the simulated amplitude is not converged: the mass-weighted q rises from 0.10 (256³) to 0.16–0.18 (512³).
  - No KiDS-mass halo is resolved, so the galaxy prediction is the analytic engine rule.
- **Lens model:**
  - The halo masses and concentrations are literature relations recalled, not read from disk (U).
  - f_ret uses the ΛCDM-equivalent M_ta.
  - The two-halo term comes from a z = 0 mesh control, mapped to z ≈ 0.3 by (1+z)² D².
- **Never cite** "drawdown detected" or "drawdown excluded" without both labels.

## Run
```
./run_495_sim.sh                                                  # Step 1 sims (512^3 one at a time, nice 15, 4 threads) + shuffled-centre MUTATE
nice -n 15 python3 cfg495_sim.py N256_s359_can                    # 256^3 canonical (+ NOCOMP run)
nice -n 15 python3 cfg495_sim_analysis.py                         # -> cfg495_sim_analysis.out / _results.json
CFG495_MUTATE=1 nice -n 15 python3 cfg495_sim_analysis.py         # -> *_MUTATE.* (shuffled centres)
nice -n 15 python3 cfg495_predict.py                              # Step 2 -> cfg495_predict.out / _results.json
nice -n 15 python3 -u cfg495_stage_random.py                      # displaced-position KiDS stack (about 2-4 min)
nice -n 15 python3 cfg495_test.py                                 # Step 3 -> cfg495_test.out / _results.json
CFG495_MUTATE=1 nice -n 15 python3 cfg495_test.py                 # null stacks -> cfg495_test_MUTATE.*
```
Large arrays (stacks, tables, the random-position sums) live in `../../../_external_data/cfg495_work/` and are not committed.
