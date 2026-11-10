# NH2: a measured mass for NGC 1052 against what tides on DF2 / DF4 need under form B. FROZEN CRITERIA

TEST lane, quarantined. It adopts nothing, relabels nothing (RB2's labels stand) and registers nothing. kappa = 1/2
FITTED; not theory closed. Cold dark energy is a gravitating field component, never a particle. Footings canonical
(a0 9.3603e-11 m/s^2) and alt (1.1312e-10), never pooled. Written and committed alone, before any script or number of
this lane. The only numbers read before this file are RB2's stored needs (rb2.out), the published values the brief
names, and the raw rows of the two tables (group 9843 in KT2017; the GC table's column layout).

## 0. The question (PAPER72 open item 9)

RB2 (closure_2026_11_09/RB2_form_b_hosted_rows, rb2.out lines 25-26 and 44-45, D = 20 Mpc) finds DF2 and DF4 LOW under
form B (-0.743 / -0.943 dex canonical, -0.781 / -0.981 alt) and TIDES CANNOT REACH with NGC 1052's law mass. The host
mass inside the projected distance that B would need (k = 3, E_B + 2e = 0):

| dwarf | d_proj (D = 20) | M_need canonical | ratio to B | M_need alt | ratio to B |
|---|---|---|---|---|---|
| DF2 | 79.3 kpc | 1.1632e13 Msun | 16.57 | 1.3466e13 | 17.58 |
| DF4 | 165.3 kpc | 1.3959e14 Msun | 99.31 | 1.6181e14 | 105.06 |

Because the Jacobi condition reads g_iso(r_J)/r_J = k G M(<d)/d^3, the need is a minimum MEAN DENSITY inside d. The
projected distance is a lower bound on the 3D distance and the mean enclosed density does not rise outward, so these are
minimum needs at every true 3D distance (and k = 3 is the point-mass value; an extended host needs more).

Question per dwarf (radius), per footing, per distance: is NGC 1052's enclosed mass M(<d) at least M_need?

## 1. Form B's own NGC 1052 (reported, and row S)

Baryons 1e11 Msun (RB2's MH_1052), a point mass under the law: M_B(<r) = r^2 a0 gl(G M_b/(r^2 a0)) / G, with
gl(y) = y/2 + sqrt(y^2/4 + y). Share cap (rule 5 of THEORY_ASSEMBLED: a galaxy's charge is 59.5 M_b, the law until used
up): M_B <= 60.5 M_b. The script prints the cap radius and confirms the cap does not bind at d (if it binds, the capped
value is used). Printed at 23 kpc, r_out of the GCs, d_DF2, d_DF4, per footing and distance.

## 2. Distances (a bracket, never pooled)

Host and dwarfs share one distance D in {13.5, 19.4, 20.0} Mpc (13.5: Trujillo+19's near distance; 19.4: Forbes+19's SBF
distance for NGC 1052; 20.0: RB2's geometry). Projected radii scale as D; d_proj(D) = d_proj(20) D/20. The needs are
recomputed at each D with RB2's own df_E / gl / gNp / rJ_iso / gB copied verbatim (Ms scales as D^2, R_e as D, sigma_obs
fixed). If a dwarf is not LOW at some D, that cell is NO RESCUE NEEDED (reported, not graded). A split distance (dwarf at
13.5, NGC 1052 at ~19-20) puts the dwarf megaparsecs from the host: no tide at all; stated, not computed.

## 3. Estimators and ceilings

**C1, density ceiling from the globular clusters (primary).** GCs from Forbes+19 Appendix A (parsed from the TeX with my
own script, `python3 -I`, commented rows included; positions and heliocentric velocities). Projected radius from
NGC 1052 at (40.2700, -8.2558). Watkins, Evans & An (2010) projected tracer mass estimator:
M(<r_out) = C/G <v_los^2 R^alpha> r_out^(1-alpha), C = (alpha + gamma - 2 beta) / I(alpha, beta),
I = sqrt(pi) Gamma(alpha/2 + 1) / (4 Gamma(alpha/2 + 5/2)) [alpha + 3 - beta(alpha + 2)];
v_los relative to v_sys = 1510 km/s; r_out = the largest GC radius. Uncertainty: 4000 bootstrap resamples of the GCs (seed
20261110). Bracket corners: alpha in {0, 0.22, 0.55}, gamma in {2.5, 2.9, 3.5}, beta in {-0.5, 0, 0.5}. The ceiling is the
largest 97.725th bootstrap percentile over the corners. Then, with a density that does not rise outward,
M(<d) <= M(<r_out) (d / r_out)^3. C1 is BELOW when that ceiling < M_need.

**C2, outer tracers beyond d.** Group members of KT2017 group PGC1 9843 (table 3) with projected R >= d. Statistic
T = sum v_los^2 R. Hypothesis H: M(<r) >= M_need for all r >= d (every selected tracer has r >= R >= d, so a point mass
M_need is the lightest potential H allows there). For each observed R_i, draw the line-of-sight depth from a tracer
density rho ~ r^-gamma truncated at r_max, and v_los from the Jeans solution in that point mass,
sigma_r^2 = G M /((gamma + 1 - 2 beta) r) [1 - (r/r_max)^(gamma + 1 - 2 beta)], sigma_t^2 = (1 - beta) sigma_r^2.
20000 draws. p = P(T_sim <= T_obs). Corners: gamma in {2, 3, 4}, beta in {-0.5, 0, 0.5, 0.9}, r_max in {1.5 R_max, inf},
v_sys in {1510, NGC 1052's KT2017 HRV}. C2 is BELOW when the largest p over the corners < 0.02275. It is computed twice:
C2a KT2017 members only; C2b adding DF2 (1803 km/s, van Dokkum+18) and DF4 (1444 km/s, van Dokkum+19) as cited
published values. C2 counts as BELOW only if both are. Fewer than 3 tracers beyond d: C2 = NO POWER.

**C3, the whole group as a ceiling.** All 16 members (tracers about NGC 1052's group). Estimators: KT2017's virial form
M = (2.5 pi / 2G) sigma_v^2 R_g with R_g = N^2 / sum_{i<j} 1/R_ij (per KT2017's definition as reproduced in KA2),
and the projected-mass estimator about the group centre (Heisler, Tremaine & Bahcall 1985) with f = 32/pi (isotropic)
and 64/pi (radial). Uncertainty: 4000 bootstrap resamples of members. C3's ceiling is the largest 97.725th percentile
over the three estimators. M(<d) <= M_group. C3 is BELOW when that ceiling < M_need.

**Floor (for CAN REACH).** M(<d) >= M(<r_out) for d >= r_out; floor = smallest 2.275th bootstrap percentile of C1's TME
over the corners.

## 4. Labels

Per dwarf, footing, distance:
- **TIDES CAN REACH** if floor >= M_need.
- **TIDES CANNOT REACH** if C1 is BELOW and at least one of C2, C3 is BELOW (two ceilings, one of them using tracers at or
  beyond d, so the label does not rest on the density assumption alone).
- **NOT DECIDED** otherwise (naming which ceilings are BELOW: e.g. "C1 ONLY").

Per dwarf and footing: the label if the three distances agree; otherwise NOT DECIDED (DISTANCE), with the cells shown.
Lane label per footing: HOST CANNOT RESCUE DF2 / DF4 if both dwarfs are CANNOT; HOST CAN RESCUE if both CAN; else the
two dwarf labels.

**Row S (secondary, B's own host).** Measured M(<r_out) from the GCs (the corner alpha 0.22, gamma 2.9, beta 0 and the
bracket of corners) against M_B(<r_out): B HOST CONSISTENT if M_B lies inside the bracket's 2-sigma span (smallest
2.275th to largest 97.725th percentile), else B HOST TOO LIGHT / TOO HEAVY. HI (3.1e11 inside 23 kpc, van Gorkom 1986
via Forbes+19, reported not raw) is printed beside it, not graded.

## 5. What counts against form B

- TIDES CANNOT REACH for a dwarf: that dwarf stays a LOW row with no rescue inside form B, now against a measured host
  (item 9 stands against B).
- TIDES CAN REACH: item 9 closes for that dwarf, but the host then holds >= 17 (DF2) or >= 100 (DF4) times B's law mass,
  which counts against B's own host prediction (stated as a new open item).
- Row S outside 2 sigma either way counts against B's host mass.
- NOT DECIDED leaves item 9 open.

## 6. Known answers (must pass before grading is read)

- **KA1** GC table: >= 70 GCs parsed (the paper says 77). The GC mean velocity and dispersion within 1 sigma of 1503 +- 15
  and 132 +- 15 km/s. r_out within 10 % of 40 kpc at 19.4 Mpc. The TME at alpha 0.22, gamma 2.9, beta 0, D 19.4 within
  10 % of 4.14e11 Msun; the same inside 23 kpc physical (GCs with R <= 23 kpc, r_out = 23) within 15 % of 2.44e11.
- **KA2** KT2017 group 9843: 16 members found; sigma_v of their HRV within 5 % of 143 km/s; R_g at 17.20 Mpc within
  10 % of 0.373 Mpc; KT2017's sigma_v and R_g in the virial form give log M = 12.844 within 0.01 dex.
- **KA3** RB2's needs at D = 20 reproduced to 1e-6 relative, both footings.
- **KA4** Mock with known mass: (a) 200 mock GC systems (power-law tracers, isotropic, in a known logarithmic potential,
  77 tracers, alpha matching) give a median TME within 10 % of the true M(<r_out); (b) C2 on 400 mocks drawn under the
  hypothesis itself rejects at the 2.275 % level in 0.5 % to 6 % of them; on mocks with a host 10 times lighter it
  rejects in >= 50 % (power, reported with the number); (c) the virial and PME estimators on 200 mock groups (16 members)
  give a median within 25 % of the true mass.
- **KA5** The density theorem: M(<d) <= M(<r)(d/r)^3 for d > r holds for isothermal, NFW, Hernquist and the law's own
  profile on a grid (sanity).

## 7. MUTATE twins (each must bite: change at least one dwarf label in at least one footing)

- **M1** every line-of-sight velocity offset (GCs and members) times 4 (mass times 16).
- **M2** the needs divided by 100.
- **M3** end to end on planted data: the GC and member velocities redrawn from a point-mass host of 3 times DF4's
  canonical need (M3 must not return TIDES CANNOT REACH for either dwarf).

## 8. Honest limits written before the numbers

Beyond ~40 kpc only a handful of member galaxies trace the potential, so any direct estimate there is weak; the lane
leans on bounds (C1's density ceiling, C3's whole-group ceiling) rather than on a measurement at 79 / 165 kpc. All
estimators assume equilibrium and spherical symmetry. Interlopers and the host's own motion in the group inflate the
velocities, which makes the ceilings more lenient to H, not less. KT2017's galaxy velocities differ from the NED values
Forbes+19 quote (by up to 150 km/s); KT2017 is used as the raw table.

## 9. Hand estimate (frozen)

M(<40 kpc) ~ 4e11, so C1 gives M(<79) <~ 4e12 and M(<165) <~ 4e13: below both needs. The group's virial mass ~ 7e12 sits
far below DF4's need and near DF2's (C3 may not decide DF2). Expect DF4 TIDES CANNOT REACH and DF2 either CANNOT or
NOT DECIDED (C1 only). Row S: B's law mass at 40 kpc ~ 4e11, expected CONSISTENT.

## 10. Files

nh2.py (one script; `--mutate` for the twins), nh2.out / nh2.json, nh2_MUTATE.out / .json, RESULT.md. Run with
`OMP_NUM_THREADS=1 python3 -I nh2.py`. Data are read from their paths, never copied, never executed.
