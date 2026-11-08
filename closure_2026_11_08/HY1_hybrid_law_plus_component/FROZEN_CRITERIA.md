# HY1 frozen criteria: the a0 law with kappa free plus a universal cold component at the CMB's f

Frozen before any HY1 script or HY1 number exists. Committed alone. Quarantined TEST lane under the owner's 2026-11-08
rule lift (closure_2026_11_08/OWNER_DECISION_2026-11-08_HY1_RULE_LIFT.md, "Lift it, launch HY1"); brief
closure_2026_11_08/HY1_BRIEF_2026_11_08.md (884b9d6aa8). This file may tighten the brief; it never loosens it. Where it
makes a brief item precise, it says so. The component is the record's cold dark energy (v3s's K(Q) dust); it is never
called dark matter and there is no particle. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

Both footings are graded separately and never pooled: canonical a0(1/2) = 9.3603e-11 m/s^2 (L* 21.7 pc), alt
a0(1/2) = 1.1312e-10 m/s^2 (L* 22.9 pc) (QX8 FOOT, GB1/QX5 A0, KX1 A0K). For any kappa the lane uses
a0(kappa) = a0(1/2) x (kappa / 0.5) on that footing. Raw data or framework-native quantities only: no LambdaCDM input, no
simulation halo profile (no NFW, no Einasto, no coreNFW). Nothing is downloaded.

## 0. Question (the brief's)

Is there one pair (kappa, f), a0 = kappa c sqrt(G rho_DE) and f = omega_d / omega_b, such that the law plus the
component passes every column at once on a footing?

## 1. Fixed by the record (replayed, never refitted)

- **f.** F1A's B2 cold fit: R = omega_d/omega_b = 5.4095831638392 (canonical) / 5.41226812314077 (alt) (f1a.json
  R_B2, 7026dcb48e). f is not a free parameter of HY1; the f-axis is touched only by M2 (f = 0) and M3 (f = 2R).
- **Where the component sits (framework-native, KD1 model P, criteria 6c7f83ed02).** The K(Q) dust is an n = 1
  polytrope with Jeans wavenumber mu_K, irrotational, minimally coupled, retained by every host it falls into. A
  system with total baryons M_b,sys captures M_d = f_cap R M_b,sys with f_cap = 0.76 (X22, QX3 FCAP) and holds it as
  M_d(<r) = M_d e(mu_K r), e(xi) = (sin xi - xi cos xi)/pi for xi < pi, 1 beyond.
- **mu_K.** Held at KD1's fixed setting mu* = 8.890e6 / 8.889e6 Mpc^-1, the smallest value the background (B1a cold at
  z 3400) and BBN (B1b) allow (KD1). The core is pi/mu* = 0.35 pc, so e = 1 at every graded radius in every column: the
  dust is a central point mass of f_cap R M_b,sys. KQ1 (07534f282b) M1 shows the host-hydrostatic solver gives the same
  cusp at mu* (enclosed fraction 1 at all X-COP radii). KQ1's smaller mu_K (cored profiles) are excluded by KD1's
  B1b BBN bound and are NOT graded or run here. This is the brief's "KD1 capture profile scaled to f" and "KQ1 shape"
  at the only mu_K the record allows.
- The dust sits inside the law as source mass (KD1 P4): g_pred = g_law(g_N,bar + g_N,dust; a0(kappa)), with
  g_law(x; a0) = x/2 + sqrt(x^2/4 + a0 x). At kappa = 0, g_law = g_N (Newton).

## 2. kappa grid and windows

- Grid K = {0, 0.001, 0.003, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.13, 0.17, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
  0.60, 0.70, 0.85, 1.00, 1.25, 1.50, 2.00}. Same grid, every column, both footings.
- A column's kappa window W_c (per footing) = the set of grid kappas at which it PASSES. Reported as the set and as
  [min, max]; any gap inside it is stated. Where a column changes status between two grid points, the edge is refined
  by 30-step bisection in kappa and reported (refined edges are reported only; windows are the grid sets).

## 3. Columns (each graded per footing, per kappa: PASS / FAIL / NOT EVALUABLE)

**C1 SPARC, per-galaxy rule (the brief's per-galaxy rule made precise).** QX8's pipeline, imported read-only
(closure_2026_11_06/QX8_sparc_exact_field/qx8.py: load_sparc, mask OK, weights W, UPS grid 0.30-1.20 step 0.01,
fit_one per-galaxy U refit, pooled, line) with its committed exact-field corrections T(R, U) (parts/, interpolated in
log U over QX8's NODES as QX10 iter_3 does). Per galaxy, per U: M_b,sys(U) = max(running-max V_bar^2 R / G at the
last radius, U L36 + 1.33 MHI) (QX10 iter_3's total); M_d = f_cap R M_b,sys(U) at every radius;
log10 g_pred = log10 g_law(g_bar + G M_d / R^2; a0(kappa)) + T(R, U). Line (PAPER67's, as QX8): pooled rms <= 0.110
AND 0.50 <= median U <= 0.80. T is computed at a0(1/2); carrying it unchanged at other kappa is a stated approximation
(QX10 iter_3's), so the T = 0 reading (algebraic law) is also computed: at any kappa where the T-carried and T = 0
readings disagree on PASS/FAIL, C1 reads NOT EVALUABLE there. Reported per kappa: rms, median U, and the largest
retained fraction eps_max in [0, 1] (M_d -> eps f_cap R M_b,sys; 30-step bisection on the line) that passes, i.e. the
dust fraction discs would have to keep (f_ret = eps_max f_cap R); "none" if the line fails at eps = 0.
Reported, not graded: GB1's class-level G1 (fixed M/L, |Z| <= 0.057, rms <= rms_L0 + 0.010) with the same candidate.

**C2 X-COP, per-bin shape (NA2's gate, made precise).** GB1's X-COP points (build, read-only; 7 clusters, r <= 0.7
R500, D = log10 M_obs / M_law(1/2)). M_d = f_cap R Mb_last (KD1's M_b,sys for X-COP, the rrM inversion) at every point;
M_pred = g_law(G (M_b(<r) + M_d)/r^2; a0(kappa)) r^2 / G; residual log10 M_obs / M_pred. Gate (NA2 / HO1): |mean| <= 0.05
AND rms <= 0.10 AND every r/R500 bin (edges 0, 0.25, 0.5, 0.75, 1.0, 2.0) with >= 3 points has |bin mean| <= 0.10.
R500 from the X-COP fgas FITS headers as NA2 reads them. Reported per kappa: mean, rms, bin means, and the point-mass
amount F_X(kappa) (in Mb_last) that minimises the rms (golden search on [0, 30]) against f_cap R.

**C3a Groups (UA1 budget).** GB1's 20 groups, points at R2500 and R500, brackets f* = 0 and f* = 1 (groups_pts).
M_d = f_cap R M_b,sys with M_b,sys = g5 (1 + f*) (GB1's rrM inversion), point mass. The hybrid's step over the footing
law at kappa = 1/2 is s(kappa) = mean over the 40 points of log10[g_law(g_N + g_d; a0(kappa)) / g_law(g_N; a0(1/2))].
PASS iff s lies inside UA1's 95 % interval for the groups' step under the full single-width budget
([+0.052, +0.459] canonical, [+0.009, +0.415] alt; ua1.json, 4ad785593c) for BOTH f* brackets. UA1's step is anchored on
the L0 SPARC Z (+0.027 / -0.0006); HY1 uses the law-relative step and says so. Reported, not graded: GB1's strict
per-group rule (>= 16 of 20 within 2 sigma at f* 0 and f* 1).

**C3b Bullet (DB1 arms).** CONDITIONAL: run only on a footing where the common window of section 5 (C1 ∩ C2 ∩ C3a ∩
C4 ∩ C5) is non-empty, because it cannot change a FAIL reached without it. If run: DB1/UX6's Bullet machinery read-only,
dust as a point mass on each subcluster's galaxy centroid at f_cap R of its baryons, at each kappa in that window, DB1's
arms and lines; it must stay under 1 GB RSS (NA2 measured 1.19 GB for this child), else C3b is NOT EVALUABLE. If not
run: NOT RUN (stated), and it does not enter the label.

**C4 KiDS G6 with kSZ gas (KX1 baseline).** KX1's machinery read-only (kx1.py prefix: Brouwer+2021 Fig-9 isolated
lenses, 4 mass bins, full covariance, window 100-300 kpc, CW6 kSZ gas profile P1 central and P1-P6/B1-B5 range, two-halo
at b_cap/2, isolation, stellar-mass shift, calibration; same budget function). The hybrid model replaces KX1's sector by
the point mass M_d = f_cap R M_* (KX1's sector base: the lens stellar mass 10^lm) and a0(1/2) by a0(kappa). E_b = KX1's
law posterior excess (kappa = 1/2, f = 0); W_b(kappa) = loga_law - loga_hybrid; z_b = (W_b - E_b) / sigma_tot,hybrid.
KX1's kill rule made two-sided (the hybrid can fall below the law): FAIL iff |z_b| > 2 in >= 2 of the 4 bins; else PASS.

**C5 Solar System and waves.** GB1's g_ss (Cassini at 9.58 AU with C6P's Hees margin, every planet's hedgehog bound,
L* from the record; no dust at the Sun, KD1 P4 model P) with the non-Newtonian multiplier at kappa
F = (nu(x_kappa) - 1) / (nu(x) - 1), x = g_N / a0(1/2), x_kappa = g_N / a0(kappa), computed in the stable form
(GB1 nu_minus_1). PASS iff GB1's g_ss line holds. c_T: the principal part is GR's exactly (V3W W4a, structural, no a0
in it); the mass-term bound 5.1e-32 / 6.2e-32 at kappa = 1/2 is quoted, and stated as scaling at most as (kappa/0.5)^2
(reported, against GW170817's 3e-15). PPN gamma, beta: V3W W1 remainders 9.8e-14 / 1.1e-12 at kappa = 1/2, stated as
scaling with F (reported). The record's L* is held fixed at every kappa (stated).

**C6 Cosmology.** (a) kappa = 0 (component only, the law off on the web): replays, graded. CMB-lensing shape with the
component at the CMB's amount: KD1 G9a chi^2 at mu -> infinity 8.5599 / 8.5604 (kd1.json; CLASS C_L directly, not
QX3's limber_ratio, so GL2's k^-4 kernel fault does not touch it) against 18.48 -> PASS iff <= 18.48. DESI fsigma8: CE2's
GF convention (Rf relative to the unheated cold sector) gives Rf = 1 for the cold component by construction; stated
PASS with no independent power. Forest P1D: the dust's Jeans length pi/mu* (0.35 pc) against CE2's GFo line 0.162 Mpc
-> PASS iff below. (b) kappa > 0 (the law on the linear web with the component): CONDITIONAL as C3b (run only where
section 5's common window is non-empty on a footing). If run: WG2's engine (rebuild_2026_10_22/WG2_bare_law_web_lensing/
wg2_pm.py, rule R1 QUMOND on the peculiar field, a0 flat) with the clustering source baryons + component at F1A's
omega_d, graded on WG2's PR4 lensing amplitude r against the measured band; only when no `python3 cmb3.py` process is
running (pgrep), else C6b NOT EVALUABLE. If not run: NOT RUN (stated), and C6 at kappa > 0 reads NOT EVALUABLE.

## 4. Power, MUTATE and known answers (all before any graded number; a KA FAIL stops grading: lane NO VERDICT)

KA (each to the stated tolerance, per footing):
- KA1 F1A: f1a.json R_B2 and B2 chi^2 cold 3740.16 / 3740.30 read and used exactly (|d| = 0).
- KA2 SPARC law-only (this is M2 for C1): C1 at kappa = 1/2, f = 0 reproduces QX8 exact rms 0.05604651300949609 /
  0.05582588353469019 and median U 0.58 / 0.52 to 1e-6.
- KA3 X-COP (M2 for C2): C2 at kappa = 1/2, f = 0 gives GB1 KA20 mean +0.467499 / +0.434523 to 1e-6; with KD1's own
  amount (f_cap x QX15's R: captured 4.1110 / 4.1121 from kd1.json) and kappa = 1/2, the X-COP residual equals KD1 G2
  -0.702864 / 0.802677 and -0.714392 / 0.809485 (mean / rms) to 1e-6, and GB1 g_sparc gives KD1 G1 Z / rms
  (-0.718657 / 0.816510, -0.735136 / 0.827508) to 1e-6; the uniform-f bisection reproduces KD1's X-COP need
  4.1786 / 3.7833 to 1e-4.
- KA4 KiDS (M2 for C4): C4's law at kappa = 1/2 reproduces KX1's E_b and sigma_tot per bin (kx1.json grade rows, cell
  rows' law fields) to 1e-9.
- KA5 groups (M2 for C3a): at kappa = 1/2, f = 0, GB1 g_groups equals gb1.json L0 G3 (n_pass and median_res) exactly,
  and s = 0.
- KA6 Solar System (M2 for C5): at kappa = 1/2, F = 1 and GB1 g_ss equals gb1.json L0 G8 numbers to 1e-12.
- KA7 cosmology: kd1.json G9a chi^2 values read exactly.

M1 kappa -> 0 (pure component). The brief asks M1 to reproduce the component-only fits where the record has them. The
record's component-only galaxy fits are the quarantined fried-chicken paper's (ACDM v2.0, DOI 10.5281/zenodo.23958263:
NFW / coreNFW halos with feedback knobs). Those are simulation-shaped profiles that HY1 may not import, and they are not
the K(Q) dust's profile, so they are NOT a known answer for this M1; stated, cited only as such. M1 here: the hybrid at
kappa = 0 must FAIL C1 on both footings (the record says a retained component in every galaxy fails SPARC: KD1 G1, QX10
iter_3 MUTATE rms 0.544 / 0.556). If C1 PASSES at kappa = 0, C1 has no power to kill and reads NO POWER.

M2 f -> 0: the KA2-KA6 replays above (the law's record numbers to 0).

M3 f -> 2R at fixed kappa (brief: must move X-COP and SPARC in opposite directions; made precise). At every grid kappa,
per footing: Delta_S = C1 pooled rms(2R) - rms(R); Delta_X = C2 rms(2R) - rms(R). "Opposite directions" = sign(Delta_S)
!= sign(Delta_X) (one column moves toward its line, the other away). Tightened: both moves must also exceed the column's
resolution (|Delta_S| > 0.010 dex, |Delta_X| > 0.020 dex). M3 BITES on a footing if both hold at one or more grid
kappas. If M3 does not bite on a footing, then, as the brief rules, C1 and C2 read NO POWER on that footing (their
statuses are still reported).

Power of the other columns (from the KA / record controls): C3a has power iff the f = 0 law fails it at kappa = 1/2
(UA1's NOT EXPLAINED, replayed) and its interval is non-empty; C4 has power iff the law passes (KA4) and KD1's dust at
kappa = 1/2 (f_cap R point mass) FAILS it (KX1's M1 analogue); C5's power is the record's screening-removed MUTATE (V3W:
plain AQUAL fails Cassini), quoted; C6a's power is KD1's I0 -> 0 MUTATE (G9a chi^2 888.5 FAIL), quoted.

## 5. Labels

Per column, per footing: PASS / FAIL / NOT EVALUABLE at each kappa; the window W_c; power YES / NO POWER.
Common window on a footing: the intersection of W_c over the columns with power that were evaluated on the full grid
(C1, C2, C3a, C4, C5).
- **FAIL** on a footing: that intersection is empty (this contains the brief's first kill clause, W_SPARC ∩ W_X-COP
  empty, and its second: a column with power that fails at every kappa of the others' common window). An empty W_c
  counts as disjoint from everything.
- **PASS** on a footing: one grid kappa at which every column, C3b and C6 (a and b) included, PASSES with power.
- **NO VERDICT** otherwise (common window non-empty but a column is NOT EVALUABLE / NOT RUN / NO POWER there), or on
  any KA FAIL.
- **NOT EVALUABLE** for the lane only if C1 or C2 cannot be computed at all.
The lane label is stated per footing; the footings are never pooled.

## 6. Reported only (never enters a label)

- Uniform-b bracket: the component tracing the baryons at every radius (b = 1 + f_cap R), the shape KD1 used as its
  diagnostic. It is NOT the K(Q) dust's framework-native profile; it is reported for C1 (QX8 pipeline, g_N x b), C2 and
  C4 at every grid kappa, to show what the deep-regime degeneracy b a0(kappa) = a0(1/2) (kappa = 0.5 / b) does and
  does not buy.
- Refined window edges (section 2); per-kappa F_X; eps_max; GB1 G1 and strict-groups readings.

## 7. Compute and outputs

One thread (OMP/OPENBLAS/VECLIB = 1), nice 10-15, each column in its own process, peak RSS logged and kept under 1 GB;
SIGTERM writes a partial checkpoint. No Boltzmann likelihood is loaded while `python3 cmb3.py` runs (the CMB column is a
replay; C6b as section 3). Scripts: hy1.py (subcommands per column) and hy1_grade.py; outputs hy1.json / hy1.out and,
for M1 and M3, hy1_MUTATE.json / hy1_MUTATE.out (separate outputs). RESULT.md gives the label per footing, per-column
labels, windows, every slip disclosed, and a plain-words paragraph. Any change after this freeze is an amendment,
committed before the numbers it affects, or disclosed as post-freeze.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
