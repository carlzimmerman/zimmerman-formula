# RS3 FROZEN CRITERIA: the residual surface (two local variables)

RS3 = the brief's RS1 (WINNER_SEARCH_BRIEF_2026_11_07.md, a939b13094, section "RS1: the residual surface"). The id
RS1 is taken by rebuild_2026_10_22/RS1_required_source/ (NO SOURCE FORM) and RS2 is also in use, so this lane is RS3,
the id CLOSURE_REGISTER v1.1 (bed393127d) opened for it.

Committed alone, before any script or number of this lane. Not blind: the record's class amounts (KD1, SE2, GB1,
RS1) are known to the author. kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle, no LCDM input, no
download. Both footings, never pooled: canonical a0 9.3603e-11 m/s^2, L* 21.7 pc; alt a0 1.1312e-10 m/s^2, L* 22.9 pc.

## 0. How RS3 differs from RS1_required_source (2c0a6f6f70, f76990a49d, 36742f590f)

RS1 inverted the needed extra source row by row and asked (Part 1) whether it collapses on ONE variable (best 0.59 dex
against a 0.20 line) and (Part 2) whether any of 3.5e9 closed-form source expressions passes a factor-2 gate set.
RS3 asks a different question with a different line:
- PAIRS: every pair of variables from the frozen list below, not one variable and not a grammar of forms.
- A MONOTONE SURFACE y(v1, v2), fitted two ways (section 4): 2D isotonic regression (the most flexible monotone
  surface there is; if it fails, every monotone surface on that pair fails) and a 6-number quadratic in log space.
- The target is the system-level required f with its error and class-correlated systematics (KD1 / SE2 / GB1
  amounts), scored by one chi^2 over all classes together, with a PER-CLASS 2-sigma line (no class may be off by
  more than 2 sigma of its own class-mean error) and SPARC held at f = 0 at GB1's exact-field tolerance.
RS1's loaders are reused read-only where they overlap; the rows here come from GB1's battery (the exact-field lane).

## 1. Classes and rows (one row per system; both footings)

Loaders: GB1 (closure_2026_11_06/GB1_all_gates_battery/gb1.py, exec'd up to its main block, read-only, as SE2 and KD1
do), SE2 se2.json (class shifts and widths), EV1 readings.json (environment field), X1 / LW1 / S1 per-system CSV/JSON.
D = log10(g_obs / g_law) per point as GB1 builds it (plain law, GB1's Upsilon). For each system the required uniform
extra-mass fraction f solves  mean_points[ log10( g_law((1+f) b g_N) / g_law(g_N) ) ] = mean_points(D) - shift_c
(b = 1 except ellipticals, b = GB1's b_imf; the KD1 definition of f applied per system). The fitted quantity is
y = log10(1 + f) (defined for every finite D). Errors in dex are carried to y by the numerical Jacobian J = dy/dD
(+-0.01 dex) of each system.

| Class | N | Row value | Per-system stat sigma (dex) | Class-correlated sigma_sys (dex) | shift_c |
|---|---|---|---|---|---|
| SPARC discs | GB1's set (QX5 filter Q <= 2, i >= 30; N reported) | TARGET y = 0 | rms over galaxies of the galaxy-mean exact-field residual (D - T_geom, QX8 at U = 0.50) | 0.0285 (= GB1 G1 Z line 0.057 / 2) | 0 |
| X-ray ellipticals (after IMF, QX26) | 7 | per-galaxy mean of the L1 (b_imf) residual, 3 radii | SE2 raw_stat_only sd x sqrt(7) (no per-system errors carried) | sqrt(post.sd^2 - raw.sd^2), SE2 ellipticals cell | 0 (QX26 nominal) |
| X-COP (SE2 reading) | 7 | per-cluster mean D | from EM_FORW per point, sqrt(sum sigma^2)/n | sqrt(post.sd^2 - raw.sd^2), SE2 X-COP cell | post.median - raw.median (SE2) |
| groups | 20 | per-group mean D at f* = 0.5 (GB1 groups_pts) | from eM2500 / eM500 per point | sqrt(post.sd^2 - raw.sd^2), SE2 groups cell | post.median - median of the f* 0.5 points (nominal) |
| bright M31 dSphs | 21 admissible (SE2 A1 + A2) | LW1 plain D minus SE2 anchor | X1 sdMC[Newton] | sqrt(post.sd^2 - raw.sd^2), SE2 bright M31 cell | post.median - raw.median |
| Coma UDGs | 9 (main); pericentre-admissible (second reading) | GB1 D (S1 E_v3_dmean / ln 10) | S1 sE / ln 10 | sqrt(post.sd^2 - raw.sd^2), SE2 Coma UDG cell | post.median - raw.median |
| field dwarfs (LG field) | 13 | TARGET y = 0 | rms over the class of (D - anchor) | sqrt(post.sd^2 - raw.sd^2), SE2 LG field cell | 0 |

Covariance per class: C_c = diag((J sigma_i)^2) + (J sigma_sys)(J sigma_sys)^T; block-diagonal across classes.
The pericentre reading replaces the 9 UDGs by those passing SE2's A1 at tau x PERI (PERI = 3^(2/3), SE2's constant).
X-COP per-bin profile (NA2 gas vs stars) is NOT used: the rows are system-level (disclosed).

## 2. Frozen variable list (per system: geometric mean over the system's graded points unless a single value)

| # | Variable | Built as | Classes lacking it |
|---|---|---|---|
| 1 | g_N | x a0 (GB1 feature) | none |
| 2 | g_obs | g_law(g_N) 10^D (raw D) | none |
| 3 | rho_b | 3 M_b,enc / (4 pi r^3) | none |
| 4 | M_b enclosed | GB1 M_b at r; dSphs and UDGs M*/2 at r_1/2 = 4/3 R_e (dSph: 4/3 rh) | none |
| 5 | r / r_half | SPARC: r over the half-mass radius of the baryon curve to the last point; ellipticals: r / (a(1+sqrt 2)), a = R_e/1.8153 (Hernquist, QX5); X-COP: half of M_b at the last baryon radius, log-log interpolated on the graded points; groups: half of Mgas500 on the two-point power law; dSphs, UDGs: 1 | none (built) |
| 6 | depth Phi/c^2 | GB1 depth; dSphs and UDGs BUILT as tail_phi(M*, r_1/2, a0)/c^2 (QX5 law tail, M* as a point mass) | none (built) |
| 7 | sigma or T (one per system) | ellipticals GB1 stellar sigma_0; groups sqrt(kT / (0.6 m_p)); dSphs, UDGs measured sigma; SPARC BUILT V_flat/sqrt 2 (SPARC table; outermost V if V_flat = 0); X-COP BUILT sqrt(G M_obs / 2r) at the outermost graded point (no T on disk) | none (built) |
| 8 | Sigma_b | M_b,enc / (pi r^2) | none |
| 9 | tidal / environment field x_e | EV1 / LW1: SPARC and ellipticals x_e_noclu (EV1 graded reading), dSphs LW1 xe, UDGs S1 x_e_dmean | X-COP, groups: NO positions on disk -> NO VERDICT |
| 10 | f_gas | SPARC vg2/vb2 per point (mean); X-COP M_gas/M_b; groups 1/(1+f*) = 2/3; ellipticals 0; UDGs 0 (no Coma HI on disk); dSphs 1.33 M_HI/(M* + 1.33 M_HI) from LVD (0 where only an upper limit) | none (linear, not log) |
| 11 | age proxy (colour) | RC3 (B-V)_T matched by name for SPARC and ellipticals | X-COP, groups, UDGs, dSphs: NO VERDICT |
| 12 | rho_b / rho_DE | rho_DE = 4 a0^2/(G c^2) (OQ1, kappa 1/2) | none |

Variables 1-9, 12 enter in log10, 10-11 linear. #12 is #3 times a footing constant: every pair with #12 equals the
same pair with #3, and (#3, #12) is a one-variable fit; they are run and reported, not counted twice.
A pair with a NO VERDICT variable for any class is fitted on the classes that carry both and is marked NO VERDICT
for the missing classes, which counts as NOT carrying.

## 3. Search: all 66 pairs x 2 families x 4 orientations (+/+, +/-, -/+, -/-), both footings

## 4. Fit families (chi^2 = r^T C^-1 r over all rows, N = number of rows)
- (I) 2D isotonic: the y values at the rows, monotone in the chosen orientation over the dominance order of the rows
  (ties allowed, equal inputs -> equal values), weighted by C^-1; solved exactly as a QP through its dual NNLS on the
  transitive reduction of the dominance constraints. Free numbers: one per distinct input point (the brief's isotonic
  option; not capped at 6).
- (P) quadratic in standardized log variables, 6 coefficients, GLS with C^-1, with the orientation's sign constraints
  on both partial derivatives imposed at every row (SLSQP; unconstrained solution used if already monotone).

## 5. Pre-registered line (per pair, per family, per footing)
A pair CARRIES on a footing if, in one family: chi^2/N <= 2 AND every class satisfies |rbar_c| / sigma_c <= 2, where
rbar_c = (1^T C_c^-1 r_c)/(1^T C_c^-1 1) and sigma_c = (1^T C_c^-1 1)^-1/2 AND the surface is monotone in each
variable (by construction). It CARRIES only if the same family carries on BOTH footings, on every class (no
NO VERDICT class), AND it survives every leave-one-class-out refit (section 6, M3).

## 6. MUTATE (each must bite, else the label is NO VERDICT)
- M1 shuffled class labels: the variable vectors are permuted across all rows (seed 3, per footing), y and C stay;
  bites if no pair carries under the shuffle on either family. Reported with it: best real vs best shuffled chi^2/N.
- M2 Newtonian f: y_N = log10(g_obs/g_N) (law off) per system, SPARC and LG field rows take their measured y_N with
  the same sigma rule, J = 1; bites if no pair carries.
- M3 leave-one-class-out: each of the 7 classes dropped in turn, refit; a carrying pair must pass the line on the
  remaining classes in all 7. Run for every carrying pair; reported also for the best pair, and as a table of how many
  pairs pass each drop (which class is the wall).

## 7. KA (before grading; any failure -> NO VERDICT, nothing graded)
- KA1: KD1's f table reproduced from GB1's battery with KD1's own procedure: SPARC allows, X-COP, ellipticals, UDGs,
  groups f* 0 / 1, bright M31, MW classical needs equal kd1.json uniform_f_diag to 1e-9 relative, both footings.
- KA2: this lane's per-system inversion applied to each pooled class equals the KD1 X-COP / ellipticals (b = 1) /
  UDG needs to 1e-6 relative.
- KA3: GB1 L0 class means (KA20 table in gb1.py) to 1e-6.
- KA4 planted positive control: on the real rows, variables and C, plant y = 0.5 + 0.4 u - 0.3 v (u = log g_N
  standardized, v = log Sigma_b standardized) plus noise drawn from C (seed 7); the pair (g_N, Sigma_b) must CARRY in
  both families and footings. If it does not, the machinery cannot say yes and the label is NO VERDICT.

## 8. Labels
- PAIR FOUND: <pair(s)> (carries both footings, all classes, all leave-one-out).
- NO PAIR: no pair carries; KA pass; MUTATE bite.
- NO VERDICT: KA fail or a MUTATE does not bite.
The pericentre UDG reading is run in full and reported; if its label differs from the main reading, the label line
states both. Whatever the label, the best pair per footing (lowest chi^2/N among pairs with no NO VERDICT class) is
reported with chi^2/N, the worst class and its sigma miss.

Expected label, stated in advance: NO PAIR (the ~100x spread and the UDG row against SPARC dwarfs).

## 9. Compute
One thread, under 1 GB RSS (peak reported), SIGTERM checkpoint (per-pair results flushed to a checkpoint JSON,
resumed on rerun), small outputs only. Outputs rs3.py, rs3.json / rs3.out (main), rs3_MUTATE.json / .out, RESULT.md.
Any post-freeze change is an amendment committed before the rerun.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
