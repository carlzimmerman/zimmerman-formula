# LWB1R RESULT_BLIND: re-grade of LWB1's weak-lensing amplitude cross-check (DESI DR1 Lensing Without Borders)

## Label (LWB1's frozen lines, my code)

**J (KiDS-1000 + DES Y3 + HSC Y3 jointly): AMPLITUDE CONSISTENT / AMPLITUDE CONSISTENT (canonical / alt), FRAGILE.**
Every gating known answer passes and J's label is the same at pi_max 40, 80 and 100, so the frozen reading is graded
(it does not depend on LWB1's AMENDMENT A1, which concerns LWB1's own check). Per survey the sources disagree: DES alone
and K+D sit in TENSION (theory above the data), HSC-Y3 is consistent from the other side, KiDS has NO POWER (width 0.051).

This is a consistency check, not independent evidence: KiDS-1000 and DES Y3 are sources already tested (KL1, CO2).
CONSISTENT is not a pass for the theory, and nothing here says the data favour the framework. Cold dark energy at 5.41
times the baryons; footings never pooled.

**Blindness, as stated in READING.md.** Before writing READING I saw LWB1's canonical first-run rows (quoted in its
AMENDMENT_A1, which I was allowed to open) and its RESULT commit subject (from a `git log` on its folder). I did not open
any lwb1 script, json, out file or RESULT.md before this commit. My numbers come from my own code; the closeness to the
seen rows below is a result, not a target.

## Table (sigma8 best +- width from the parabola rule; gap g = (target - best)/width; p of best fit)

| vector | canonical (target 0.8121) | alt (target 0.8120) | label (both) |
|---|---|---|---|
| **J** | 0.7862 +- 0.0285, g +0.91, p 0.078 | 0.7871 +- 0.0285, g +0.87, p 0.078 | **AMPLITUDE CONSISTENT**, FRAGILE |
| KiDS | 0.7590 +- 0.0509, g +1.04, p 0.050 | 0.7600 +- 0.0510, g +1.02 | NO POWER, FRAGILE |
| DES | 0.6466 +- 0.0474, g +3.49, p 0.65 | 0.6475 +- 0.0474, g +3.47 | TENSION (theory above), FRAGILE |
| HSC-Y3 | 0.8575 +- 0.0353, g -1.28, p 0.64 | 0.8585 +- 0.0354, g -1.32 | AMPLITUDE CONSISTENT, FRAGILE |
| K+D | 0.6988 +- 0.0363, g +3.12, p 0.081 | 0.6997 +- 0.0364, g +3.09 | TENSION (theory above), FRAGILE |

Exact Delta chi^2 = 1 profile agrees with the parabola to <= 0.0004 in best and width. 101 Delta Sigma points, 10 wp points.

**What makes J FRAGILE (brackets, canonical; alt within 0.04 in g):** point-mass term 0.680 +- 0.050 (NO POWER, g +2.64);
R_min 12: 0.730 +- 0.035 (GAP STAYS, +2.33); R_min 5: 0.805 (g +0.29, but p < 0.01); pi_max infinite: 0.767 (g +1.64,
p < 0.01); N = 1 (pure linear): 0.873 (g -1.93, p < 0.01). Not moving the label: pi_max 80 / 100 (+0.87 / +0.96), wp bins
correlated 0.5 (+1.27), DS at the rp column (+1.39), edge scale cut (+1.05), `ds` without the magnification column (0.812,
+0.00), N tail above k 8 removed (+0.94), CAMB halofit at KL1's parameters x R_tot (+1.15).

## Reference-spectrum check (V5; Planck 2018 CAMB 1.6.6 + Takahashi halofit, same pipeline)

K+D: S8 = **0.710 +- 0.037** against the published 0.794 +- 0.023 (Lange+, DES + KiDS; PROVISIONAL: the value is quoted in
LWB1's criteria from a web read, the paper is not on disk): -1.92 combined widths, inside LWB1's 2-width line but **my
pipeline reads low by 0.084 in S8 (11 %)** on K+D. J reads 0.798 +- 0.029 (+0.11), DES alone 0.654, HSC-Y3 0.868.
Reported row: shifting the theory's S8 reading on each vector by the pipeline's own offset (0.794 minus its Planck reading
there) leaves offset-shifted gaps of +1.05 J, +0.55 KiDS, +0.61 DES, +0.77 HSC-Y3, +0.87 K+D (canonical; alt -0.02 to
-0.04). The DES and K+D tensions are carried by the same offset the Planck spectrum shows; they are a property of this
pipeline on these vectors (R >= 8, linear bias), not specific to form B.

## Validation (all gating lines pass)

- V1 power law (gamma 1.8): wp within 0.10 %, Delta Sigma within 0.010 % at 1-60 h^-1 Mpc (line 1 %); xi to 1e-8.
- V1b my sine transform of the real spectrum vs brute-force trapezoid: <= 0.19 % at r 0.05-83.
- V2 sigma8 of my EH no-wiggle P_lin0 on an independent grid: 0.81100 (line 0.3 %).
- V3 B-mode null with the Delta Sigma template: KiDS +1.47, DES -0.17, HSC-Y3 +0.51, joint +0.87 sigma (line 3).
- V4 blinding slope (KiDS/DES, HSC/DES non-tomographic ratios): pooled c 0.028 +- 0.012, 2.46 sigma (line 3; close).
- MU1 every Delta Sigma x 0.85: J sigma8 ratio 0.8565 / 0.8565 (line 0.85 +- 0.02); J goes to TENSION. Bites.

## Shared with LWB1 / not checked

Shared inputs: the DESI DR1 release vectors and covariances, BX1's stored pair-A splice spectrum (N), CO1's `co1_hm.json`
(R_tot), KL1's `kl1_nu.json` (target sigma8, Omega_m), and LWB1's frozen model choices. Written fresh: EH spectrum, growth,
xi transform, projections, Kaiser wp, data assembly, fit, labels. Not checked: Lange's 0.794 (not on disk); whether the
`blindA` files are unblinded beyond V4's slope test; the BGS-LRG and wp-Delta Sigma cross-covariances (not on disk, zero).

Files: `lwb1r.py` (run: `nice -n 19 python3 -W ignore lwb1r.py [--mutate MU1]`, about 3 minutes, 4 processes),
`lwb1r.json/.out`, `lwb1r_MUTATE_MU1.json/.out`, `lwb1r_grade.py` -> `lwb1r_grade.json/.out`. READING 55b7a264a6; code and
run 434df4e462; graded rows ee6f51a542.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
