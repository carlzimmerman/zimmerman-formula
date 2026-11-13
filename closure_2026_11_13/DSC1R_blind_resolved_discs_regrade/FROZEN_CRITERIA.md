# DSC1R FROZEN CRITERIA: blind re-grade of the crossing-speed joint on resolved high-redshift rotation curves

Written and committed alone, before any script of this lane exists and before any fit number is computed or seen.
TEST lane, blind and independent. Adopts nothing, relabels nothing. kappa = 1/2 and X = 5.41 are FITTED.
Footings canonical (a0 9.3603e-11 m/s^2) and alt (a0 1.1312e-10 m/s^2), never pooled. Cold dark energy is a
gravitating field component, not a particle.

## 0. Blindness and what was read before freezing

Not opened, listed or searched: the earlier lane on this question and the other lanes the brief names (only the folder
names of `closure_2026_11_13/` were seen in a directory listing). Read: the brief; CFG400 `cfg400_test.py` and its
criteria lines 1-40; CFG401 `cfg401_gas_shape.py`; CFG402 `cfg402_robustness.py`; CFG405 `cfg405_robustness.py`
lines 1-80 and its criteria lines on inclination; CFG278 criteria sections 0-7; the Lelli+2023 digitised CSV (head, all
25 rows were printed: radii and velocities of the two discs, no model or fit) and its README; SRJ3's script, criteria
and RESULT head; SRJ2 `srj2_rc.py` lines 1-30; FRZ1 `frz1_hm.py` lines 1-135; CFG556 constants (h, Om, FB, RHO_M);
PD1's X medians (59.49 / 55.72 canonical, 59.50 / 55.73 alt); SRH1 `srh1_hm.py` lines 1-42; FLD1 criteria lines 1-40
and one run file (log M_b 11.2 canonical: R_fold about 60-100 kpc at z 1.5-2.5); JNT2 `jnt2_common.py` grep lines
(definition of v* only). Seen: the Genzel point file's point counts, offset ranges and spacing (no velocities read
into any statistic). No rotation-curve fit, chi^2 or A has been computed.

## 1. Rule under test (from the brief)

v*(z) = v*(0) / E(z), E(z) = sqrt(0.3153 (1+z)^3 + 0.6847), v*(0) = a0 / (10 (1 + X) H0), X = 5.41, H0 = 67.4,
a0 constant in z: 668.5 km/s canonical, 807.9 km/s alt. A disc is ABOVE iff v_L = (10 G (1 + X) M_b H(z))^(1/3) > v*(z),
i.e. log M_b > log(v*(z)^4 / (G a0)) (11.279 / 11.526 at z = 2).
- ABOVE statement: g(R) = g_N,bar(R) + A g_ref(R) with A = 1, no law boost.
- BELOW statement: g(R) = law(g_N,bar(R)), law: g^2 / (a0 + g) = g_N, i.e. g = (g_N + sqrt(g_N^2 + 4 a0 g_N)) / 2,
  no extra halo inside the settled radius.

**Reference halo g_ref (the record's cold reference profile, FRZ1 / SRJ3 construction, X set to 5.41 as the brief
states):** M_ta = X M_b h / (1 - FB) in Msun/h, h = 0.6736, FB = 0.02237 / 0.14237 (CFG556), Om = 0.3153;
NFW with M200m concentration c = 10.14 (M / 2e12)^-0.081 (1+z)^-1.01 (M in Msun/h); turnaround overdensity
Delta_ta(z) = 5.55 + (11.81 - 5.55) (1 - Om(z)) / (1 - Om) relative to 200 x mean (x_ta solves m(c x)/m(c)/x^3 = Delta_ta/200);
M200m solved so that the mass inside r_ta equals M_ta; radii comoving Mpc/h, physical r = r / (1+z) / h.
Cold mass inside r: C(r) = X M_b m(r / r_s) / m(c x_ta), r capped at r_ta; g_ref = G C(r) / r^2. A free multiple A
multiplies this fixed profile (shape built once at A = 1).

**Reported, not graded:** the record's PD1 X (about 56-59) corresponds to A = X_PD1 / 5.41 (about 10.3-11.0); RESULT
states where that falls relative to the interval of A.

## 2. Sample and membership (nominal M_b; computed before freezing from the definitions, no fit)

| disc | source | z | log M_b | log threshold can / alt | margin can / alt | group can / alt |
|---|---|---|---|---|---|---|
| COS4 01351 | Genzel+17 | 0.854 | 10.954 | 12.345 / 12.592 | -1.39 / -1.64 | below / below |
| D3a 6397 | Genzel+17 | 1.500 | 11.362 | 11.708 / 11.955 | -0.35 / -0.59 | below / below |
| GS4 43501 | Genzel+17 | 1.613 | 10.875 | 11.606 / 11.853 | -0.73 / -0.98 | below / below |
| zC 406690 | Genzel+17 | 2.196 | 11.146 | 11.125 / 11.372 | +0.02 / -0.23 | ABOVE / below |
| zC 400569 | Genzel+17 | 2.242 | 11.398 | 11.090 / 11.337 | +0.31 / +0.06 | ABOVE / ABOVE |
| D3a 15504 | Genzel+17 | 2.383 | 11.301 | 10.986 / 11.232 | +0.32 / +0.07 | ABOVE / ABOVE |
| zC-488879 | Lelli+23 | 1.470 | 10.890 | 11.736 / 11.982 | -0.85 / -1.09 | below / below |

**Edge discs (margin within the 0.2 dex mass prior):** zC 406690 (canonical, +0.02), zC 400569 (alt, +0.06),
D3a 15504 (alt, +0.07); zC 406690 alt (-0.23) is just outside. Groups: canonical above 3 / below 4; alt above 2 / below 5.
z range 0.85-2.38 (COS4 01351 at 0.854 is kept; the brief's "about 0.8").

Lelli+23 zC-400569 is the same galaxy as Genzel's zC 400569: its curve enters only as the alternative-curve bracket.
No other resolved high-z curve is used (none was searched beyond the brief's files; RC100 has one point per disc).

## 3. Data construction

**Genzel+17 (`cfg400_points.csv`, kind v; Table 1 as typed in CFG401: z, kpc/", i, R_1/2, sigma0, B/T, vc, M*, M_b).**
R = |offset| x kpc/" (both sides kept, each point once). V = |v| / sin i, eV = max(err, 1) / sin i. Main beam cut:
|offset| >= 0.30" (half the 0.6" FWHM, CFG400). V_c^2 = V^2 + k 3.36 sigma0^2 (R / R_1/2), k = 1 nominal (Genzel's
asymmetric-drift term). g_obs = V_c^2 / R. Point error in log g: sqrt((2 V eV / V_c^2 / ln 10)^2 + 0.05^2).
**Lelli+23 (digitised CSV), zC-488879 (main, below) and zC-400569 (alt-curve bracket only):** all lines pooled;
R = r" x kpc/" from the brief's cosmology; V as published (already deprojected at i = 71.6 / 54.5); eV = mean of the two
half bars; nominal asymmetric drift with the paper's upper limits sigma = 15 km/s (CO) and 37 km/s (H-alpha):
V_c^2 = V^2 + k 3.36 sigma^2 (R / R_e,disc), k = 1 nominal. Same log-g error with the 0.05 dex floor.

**Baryon models (Newtonian g_N,bar, sum of components):**
- Genzel discs: M_b from Table 1 (Mbaryon), M* from Table 1; bulge (Hernquist, a = 1 kpc / 1.8153) mass
  min(B/T x M_b, M*); stellar disc (thin exponential, Freeman, R_d = R_1/2 / 1.678) M* - bulge; gas M_b - M* in a thin
  exponential disc of scale 2 R_d (the record's convention). Prior sigma(log M_b) = 0.20 dex (declared).
- zC-488879: M* = 5.2e10 (SED); bulge fraction 0.63 of M* (Hernquist, R_e 3.0 kpc), disc R_e 0.88" (R_d = R_e / 1.678);
  gas = alpha_CO L'_CO(1-0), L' from CO(2-1) 0.56 Jy km/s, R21 = 0.85, nominal alpha_CO = 1.31 (geometric mean of the
  paper's bracketing 0.4 and 4.3), exponential disc of the stellar disc's R_e. Prior: stars 0.30 dex (CFG278).
- zC-400569 alt-curve bracket: Genzel's baryon model for the galaxy (only the curve changes).

**Correlated points.** Each disc's chi^2 is divided by c_j = N_j / N_eff,j. Genzel: N_eff = sum over the two sides of
max(1, (r_max,side - r_cut) / 0.6"). Lelli: c = 2 for every line (rings at about half a beam).

## 4. Statistic and fits (per footing, per group; footings never pooled)

chi^2(model) = sum_j (1 / c_j) sum_i ((log g_obs,i - log g_mod,i) / sigma_i)^2, masses and inclinations fixed at the
frozen values (brackets move them). dof = sum_j N_eff,j - (number of free parameters).
Misfit scale s^2 = max(1, chi^2_min / dof) (chi^2_min of the best layout fitted in that group).

**Above group.** g_mod = g_N,bar + A g_ref, one A common to the group, A on a grid -2 to 40 (step 0.005; a model with
g_mod <= 0 at any point is excluded). 95 % interval: chi^2(A) <= chi^2_min + 3.84 s^2. Per-disc A reported.
- Power: the interval excludes at least one of A = 0, 1, 2.
- **JOINT'S STATEMENT HOLDS:** power, A = 1 inside, A = 0 excluded.
- **JOINT'S STATEMENT FAILS:** power and A = 1 excluded (the sign of A_best - 1 is named).
- **NO POWER:** otherwise (including: A = 1 inside, A = 0 not excluded, A = 2 excluded; or an empty group).
Reported: absolute fit (chi^2 / dof and its p), and the law on the above discs as context (not graded).

**Below group.** Three layouts: L (law on baryons, no free parameter), N (baryons alone), H (baryons + A g_ref, A >= 0
free, one A for the group). s^2 from min(chi^2_L, chi^2_N, chi^2_H) / its dof.
- Power: max(|chi^2_N - chi^2_L|, |chi^2_H(A=1) - chi^2_L|) >= 9 s^2.
- **LAW FAILS BELOW:** power, and min(chi^2_N, chi^2_H,best) <= chi^2_L - 9 s^2 (another layout preferred by 9 s^2),
  and the law is rejected in absolute terms: p(chi^2_L, dof_L = sum N_eff) < 0.0027.
- **LAW HOLDS BELOW:** power and not FAILS.
- **NO POWER:** no power (or empty group).
A HOLDS is a hit, not a pass.

**Settled radius (reported).** R_fold(z, M_b) per footing from FLD1's run files (`series` z, R_fold_kpc; interpolated in
z, then linearly in (log M_b, log R_fold) over FLD1's mass grid). Every below-group point is expected inside R_fold
(f = 1); any point outside is listed. No point is re-modelled for it.

## 5. Brackets (each run on BOTH groups and BOTH footings with the same rule; FRAGILE if any flips a word)

| id | assumption |
|---|---|
| AD0 / AD2 | asymmetric-drift term off (k = 0) / doubled (k = 2) |
| M- / M+ | every disc's M_b at -1 sigma / +1 sigma (Genzel 0.20 dex all components; zC-488879 stars 0.30 dex); membership recomputed |
| STARS | stars alone (gas removed); membership recomputed |
| GLO / GHI | gas x 10^-0.3 / x 10^+0.3 (Genzel); alpha_CO 0.4 / 4.3 (zC-488879); membership recomputed |
| I- / I+ | inclination -/+ its error (Genzel +-10 deg as CFG405, zC 406690 +-12 deg as CFG402; zC-488879 +-4.1 deg), clipped 10-85 deg; V and eV rescaled by sin i0 / sin i |
| BEAM | Genzel cut at |offset| >= 0.6" (full FWHM); Lelli innermost ring of each line dropped |
| OUT | outermost point of each side (Genzel) / of each line (Lelli) dropped |
| ALTC | zC 400569 replaced by Lelli+23's curve of zC-400569 (where it is a member; elsewhere identical to main, said so) |

Membership in a bracket that changes M_b is recomputed with the bracket's mass; an emptied group reads NO POWER.
RESULT reports, per label, which bracket flips it and which bracket moves A (above) or chi^2_L - min(chi^2_N, chi^2_H)
(below) the most.

## 6. Known answers (must pass, else the lane's labels read NO POWER)

- **KA1 (SI):** v*(0) = 668.5 / 807.9 km/s to 0.1 km/s; log threshold at z = 2 = 11.279 / 11.526 to 0.005; the halo's
  cold mass at r_ta equals X M_b to 1e-8; r200m recomputed in SI from rho_m(z) agrees with the script to 0.1 %.
- **KA2 (synthetic, above):** g_obs replaced by the A = 1 model on the real radii and errors (noise-free): the fit returns
  A = 1 within 0.01 and the word JOINT'S STATEMENT HOLDS on each footing.
- **KA3 (synthetic, below):** g_obs replaced by the law on the baryons (noise-free): chi^2_L < 1e-6 and the word is
  LAW HOLDS BELOW on each footing.

## 7. Mutation twins (outputs `*_MUTATE_<id>`; must bite on both groups and both footings, else that group reads NO POWER)

- **TW-V:** every observed V multiplied by 1.25 (g x 1.5625). Bites (above) if A_best moves by >= 0.5 or the word
  changes; (below) if chi^2_L - min(chi^2_N, chi^2_H) moves by >= 9 or the word changes.
- **TW-M:** every model baryon mass halved (halo scales with it). Same bite rule.

## 8. Labels table and RESULT

RESULT_BLIND.md leads with the labels (group x footing, FRAGILE appended where a bracket flips the word), then
per-disc membership and numbers, A with its interval, the bracket table for both groups, known answers, twins, what
was left out, and one plain paragraph. Any change after this freeze is a dated amendment committed alone, with the
as-frozen reading first.

## 9. Hand estimate (before any number)

Above discs (log M_b 11.15-11.40, z 2.2-2.4): M_ta about 6.4 M_b ~ 1.5e12 Msun, r200m ~ 100 kpc, c ~ 3.3,
r_s ~ 30 kpc; at R = 10 kpc m(0.34) / m(c x_ta ~ 10.6) ~ 0.039 / 1.54, so the cold mass ~ 0.14 M_b against ~ 0.8 M_b
of baryons: the halo adds ~ 15-20 % to g at 10 kpc and less inside. A = 0 and A = 1 differ by ~ 0.07 dex in the outer
points; with ~ 3-6 independent beams per disc and 0.05-0.1 dex errors, Delta chi^2(0 vs 1) ~ 5-15 before s^2.
Genzel's outer curves fall, which pulls A down. P(NO POWER) 0.40, P(FAILS, A < 1) 0.35, P(HOLDS) 0.20,
P(FAILS, A > 1) 0.05; alt (two discs) more likely NO POWER.
Below discs: g_N/a0 ~ 1-3 at the outer points, the law boosts g by 30-60 %, so law vs Newton differs by much more than
9 s^2: power likely. The falling Genzel curves and the strong drift correction make the law look heavy:
P(LAW FAILS BELOW) 0.45, P(LAW HOLDS BELOW) 0.35, P(NO POWER) 0.20. Most likely flip: AD0 / AD2 (pressure) and M- / M+.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
