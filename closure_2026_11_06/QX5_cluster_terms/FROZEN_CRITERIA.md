# QX5 frozen criteria (common protocol): new action terms keyed on a cluster-vs-galaxy variable

Frozen before any QX5 script exists. Rules: closure_2026_11_06/SWARM_BRIEF.md. Kappa = 1/2 FITTED; not theory
closed. Adopts nothing. No dark-matter particle. No LCDM inputs.

## Why

QX2 (34a3050f18): at the same y = g_N/a0, X-COP needs 0.30-0.51 dex more boost than SPARC, so no universal nu
(J(Y)) works, and every static term of v3s/AC2q fails G-X. A pass therefore needs a NEW term whose effect depends
on a variable k that differs between clusters and galaxies at equal y. QX5 grades five key classes (a)-(e), one
iteration each (iter_*/FROZEN_CRITERIA.md gives the key, the covariant term and the static equation).

## Common form of the static effect

Each new term enters as a phantom multiplier: static spherical
    M_model(r) = M_b(r) + F(k(r)) [M_law(M_b, r) - M_b(r)],
with M_law the law-S algebraic mass (QX2 iter 1), F >= 0 a function of the key only. F = 1 is v3s/AC2q. The
monotone direction of F is fixed a priori from each class's physics (stated per iteration). Because F multiplies
only the phantom, which is <= 1e-13 g_N at 1 AU (AC12, C6P), Cassini/PPN at O(GM) are unaffected for any
F <= 4.8e7 (C6P margin): that recheck is analytic, stated per iteration.

## Data (all on disk)

- X-COP: QX2's builder (35 points, x = 0.1-0.7 R500). Gate G-X: |mean Delta| <= 0.05, rms <= 0.10.
- SPARC (calibration C): QX2's cuts (Q <= 2, inc >= 30, eV/V <= 0.1, Upsilon disc 0.5, bulge 0.7). Points used to
  constrain F only where the law's phantom fraction (g_law - g_bar)/g_law >= 0.3. Required
  F_i = (g_obs - g_bar)/(g_law - g_bar); sigma_F from eV (2 eV/V in g) plus 0.054 dex intrinsic, in quadrature.
- Ellipticals (C): Humphrey et al. 2006 (7 X-ray ellipticals). Total M(r) from their NFW+stars fit (X-ray
  measured), baryons = Upsilon_Kroupa x L_K in a Hernquist profile (a = Re/1.8153), hot gas neglected (small).
  Points r = 2, 4, 8 Re. sigma: 0.15 dex on M_b (Kroupa vs Salpeter spread).
- Lensing (C, keys a and d only): Brouwer et al. 2021 KiDS isolated lenses, four stellar-mass bins (Fig-9 files),
  g_obs = 4 G ESD/bias, g_bar from the file, r = sqrt(G M_b/g_bar) with M_b = 10^(bin midpoint) Msun (key use
  only). Points with g_obs > 0.
- Groups (gate, never calibration): Lovisari et al. 2015 (20 groups), R2500 and R500: M_HSE, Mgas, kT. Stars
  unknown: bracket M_star in [0, Mgas]. Groups PASS if the bracket of mean Delta overlaps [-0.05, 0.05].

## Protocol P (graded; the only route to PASS)

Weighted isotonic regression of F on calibration set C (SPARC + ellipticals, + lensing for keys a, d) in the
stated direction. Predict F at each X-COP and group key by interpolation, flat beyond the calibrated range. No
constant is set by any cluster or group. PASS (class) iff G-X passes on both footings, groups pass, and the
rechecks hold: SPARC rms rises <= 0.01 dex and mean shifts <= 0.02 dex vs the plain law; ellipticals mean
|Delta| shift <= 0.15; lensing mean Delta shift <= 0.05.

## Kill check K (decides DEAD; reported)

Isotonic fit on C + X-COP together (same direction). DEAD if, even so, X-COP fails G-X, or a recheck above fails.
If K passes X-COP and the rechecks: predict groups from the K fit. DEAD-BY-GROUPS if the groups gate fails.
Otherwise CLUSTER-SET: a monotone F exists but only clusters set it. That is a FAIL under the no-tuning rule, but a
lead, reported to the owner, not adopted.

## Labels per class

PASS (from P) / CLUSTER-SET (FAIL by rule; lead) / DEAD-BY-GROUPS / DEAD. Class (c) may be closed analytically
(its iteration file says how).

## Controls (separate outputs, qx5_MUTATE.*)

- M1 (K has power): replace X-COP's M_HSE by M_b + F_true (M_law - M_b) with F_true = 2.8 above the largest
  calibration key (key a). K must then pass G-X on X-COP. If not, K cannot see a viable class: no DEAD label stands.
- M2 (P has power): set the ellipticals' required F to 2.8 (their M_obs raised accordingly), key a. P must then move
  X-COP's mean Delta by <= -0.2. If not, P cannot see a viable class: no PASS/FAIL from P stands.

## Known answers

- With F == 1 the X-COP stats equal QX2 iteration 1 (mean +0.468 / +0.435) to 1e-3.
- Lean (fable_independent_2026/lean_2026/QX5_monotone_sandwich.lean + MUTATE twin): a monotone F whose value is
  <= 1 + eps at calibration keys bracketing k cannot exceed 1 + eps at k; certified, 0 sorry, standard axioms.

## Scope

Statics, spherical symmetry, hydrostatic masses. The phantom-multiplier form is the leading static effect of each
term; lensing = dynamics and growth for a surviving class are owed, not graded here.
