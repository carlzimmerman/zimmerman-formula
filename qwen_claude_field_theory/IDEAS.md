# 100 ideas — one per session

Each is self-contained. Do not read the others. Format: **HYP** hypothesis, **DO** method,
**DATA** where to get it, **PASS/KILL** the pre-registered decision, **IMPACT** the roadblock moved.

Every entry names, in USES:, at least two of Carl's own elements:
N1 a0 = kappa c sqrt(G rho_Lambda) = 9.3619e-11 canon / 1.1279e-10 alt, kappa = 1/2 fitted
   (measured 0.529 +/- 0.034);  N2 the promotion a0^2(Q) = kappa^2 G(-K(Q)), a0 is a FIELD;
N3 the beta=1 offset DBI K(Q) = -M^4 sqrt(1-(Q-Q_0)^2/Lambda_D^2), M^4 = rho_Lambda c^2, with a
   WALL at |Q-Q_0| = Lambda_D where -K -> 0 and a0 -> 0;
N4 a0(nu)/a0(0) = [(1+nu_0^2)/(1+nu^2)]^(1/4), nu = nu_0 rho/rho_0, nu_0 <= 2.36e-6;
N5 the a0-line g_obs^2 = g_bar^2 + a0 g_bar (nu = sqrt(1+1/y), U = sqrt(y^2+y)-y -> 1/2);
N6 the legality result: U strictly increasing, legal family J_Y = v/(1-v/s), U -> s
   (U(2) = 0.369 family vs 0.449 a0-line -- NOT the same object);
N7 Q_0 pinned 0.0024-0.0146 Mpc^-1, Lambda_D/Q_0 bounded by growth and the Ly-alpha forest.
Roadblocks served: R1 the s-gap 13,600-17,300x (perihelion s <= 1.27e-5, RAR s >= 0.219 canon /
0.173 alt, NO EFE relief -- the rigorous relief factor is 1.0000003x), R2 the dust (rho = Q_0 n,
endpoint falsified 5.8e5x vs Sgr A*; irrotationality is NOT a theorem but the band is empty by
2.77x), R3 kappa fitted, R4 no cluster mechanism but the a0-bump, R5 no valid PPN limit.

Seeded angles this file expands: S1 a0's own equation of motion (I033, I036, I038, I040, I049);
S2 dark energy is inhomogeneous because -K is a field (I027, I057, I066, I086);
S4 legality RE-DERIVED with a0 a FIELD (I007, I020, I084, I085, I087, I094) -- the 233x
obstruction was derived treating a0 as a CONSTANT, which the framework itself contradicts.

**Frozen ideas — I001 / I003 / I012 / I037** as a blind cross-check against Claude's own runs, and
predate the USES:/IMPACT: convention. Do not edit them.

---

## A. The 233x incompatibility — escape routes (highest value: this is the live problem)

**I001 — Does the EFE factorise against a density-dependent a0?** HYP: the committed EFE
reduction (119-189x) was computed at constant a0; against a0(rho) it may compound
differently. DO: take the EFE suppression as a function of the ratio g_ext/a0, then let a0
vary per the promotion and recompute. DATA: `real_research/reviews/a0_local_ephemeris_2026.py`.
PASS: the combined reduction exceeds 233x. KILL: it stays near the multiplicative estimate.

**I002 — The 1 AU anomaly is s*a0(local), not s*a0(cosmic).** HYP: a0 is a field, so the saturated sunward term at 1 AU
is set by the LOCAL dark-charge density through N4. USES: N2+N4+N6. DO: PRIOR:
`real_research/reviews/a0_local_ephemeris_2026.py` already recomputed the alpha=1 liability with a0 LOCAL -- read its
suppression factor first, do not re-derive it. Then form nu = nu_0*rho_local/rho_0 at nu_0 = 2.36e-6 for rho_local/rho_0
in {1e2, 1e4, 4.24e5, 1e6, 1e8}, evaluate [(1+nu_0^2)/(1+nu^2)]^(1/4), divide the gap 13600 (canon) / 17300 (alt) by it.
DATA: that file + `nbody_2026/stage75_the_closed_theory_2026.py`. PASS: gap shrinks by >100x. KILL: suppression < 3x.
IMPACT: local a0 suppression closes R1's ephemeris end, or provably cannot.

**I003 — Disc (non-spherical) correction to the local law.** HYP: `u J_Y(u^2) = g_bar` is
exact only in spherical symmetry; discs may shift the RAR requirement on s. DO: solve the
AQUAL-type equation for a Miyamoto-Nagai disc numerically, compare u(r) with the spherical
algebraic answer. PASS: the disc value of s needed drops below 0.1. KILL: shift is < 20%.

**I004 — Fit the anomaly's radial SHAPE, not a constant, to planetary residuals.** HYP: the framework predicts
s*a0(rho(r)), whose curvature the precession fits were never given, so s <= 1.27e-5 on a CONSTANT term is the
wrong bound. USES: N2+N4+N6. DO: build a(r) = s*9.3619e-11*[(1+nu_0^2)/(1+(nu_0 rho(r)/rho_0)^2)]^(1/4) with
rho(r) = rho_1AU (r/AU)^-q for q in {0, 1, 2}; fit s jointly with dGM_sun and dJ2 to Mercury/Venus/Earth/Mars
precessions; report the MARGINALISED 2-sigma bound on s. Bounds are Sereno-Jetzer 2006 Tab.1 inverted: dA_R <=
3.66e-14 m/s^2 (Earth), 3.72e-14 (Mars). DATA: `real_research/reviews/a0_local_ephemeris_2026.py`. PASS: bound
on s loosens >10x. KILL: <2x. IMPACT: reopens R1's denominator by degeneracy alone.

**I005 — Build and validate the coupled (phi, Q) static solver every S1/S4 idea needs.** HYP: the corpus has no committed solver in which a0 is a FIELD, so every promotion claim is currently made by
hand-inversion; one validated 1D solver settles them all. USES: N2+N3+N5. DO: write `runs/i005_two_field_solver.py` solving, on a log grid r = 1e-4 to 1e4 kpc with 4000 points, the pair div(J_Y grad
phi) = 4 pi G rho_b with J_Y = v/(1-v/s) and v = |grad phi|/a0(Q), together with Z grad^2 Q = -dK/dQ + lambda_c rho for K = -M^4 sqrt(1-(Q-Q_0)^2/Lambda_D^2), M^4 = rho_Lambda c^2, a0^2(Q) = kappa^2
G(-K), kappa = 0.529. Validate on the two limits with known answers: (i) Lambda_D/Q_0 -> 0 must reproduce the a0-line g_obs^2 = g_bar^2 + a0 g_bar to 1e-6 relative at y = 0.1, 1, 10, 100; (ii) a 1
Msun point mass at s = 1.27e-5 must reproduce g_bar at 1 AU to 1e-10 relative. Both footings, a0(0) = 9.3619e-11 and 1.1279e-10; Q_0 = 0.0024 and 0.0146 Mpc^-1. DATA:
`real_research/bridge1_aest_equations.md` for Z and lambda_c; `nbody_2026/stage75_the_closed_theory_2026.py` for Q_0 and Lambda_D. PASS: both validations meet their tolerances and the script exits 0.
KILL: no convergence for x = (Q-Q_0)/Lambda_D > 0.9 -- report the largest x reached, which is itself the wall's numerical signature. IMPACT: supplies the engine every S1 and S4 idea needs.

**I006 — The brane's stiffness sets a STATIC screening length; compute it.** HYP: K''(Q_0) = M^4/Lambda_D^2
gives the Q excitation a mass, Yukawa-cutting the scalar force below some length and capping the anomaly.
USES: N3+N7+N2. DO: form K'' = M^4/Lambda_D^2 with M^4 = rho_Lambda c^2 = 5.36e-10 J m^-3 (units J m^-3 per
(Mpc^-1)^2); divide by the kinetic normalisation Z (units J m^-3 times m^4) to get m^2 in m^-2 -- this is NOT
a length -- then take lambda = 1/m and scan Lambda_D/Q_0 over {1e-9, 1e-8, 1e-7, 1e-6, 3.1e-6} at both ends of
the Q_0 pin. This is the static range, not a sound speed. DATA: analytic. PASS: lambda < 1e4 AU somewhere in
the band. KILL: lambda > 1 Mpc everywhere. IMPACT: a Yukawa cut kills R1's anomaly, sparing galaxies.

**I007 — Does U still saturate once a0 is a FIELD? (S4)** HYP: legality forces U -> s in v = sqrt(Y)/a0, but a0 depends
on the local charge, so the OBSERVABLE U at fixed radius, plotted against y = g_bar/a0(0), need not be bounded. USES:
N2+N4+N6. DO: write U_eff(y) = (a0(nu)/a0(0)) * U(v) with v = sqrt(Y)/a0(nu(rho)) and U(v) = v/(1+v/s) inverted from J_Y
= v/(1-v/s); tie rho(r) to g_bar by rho = g_bar/(4 pi G r) for a point mass; evaluate U_eff at y = {1, 2, 10, 1e3, 1e6,
6.33e7} for s in {1.27e-5, 1e-3, 0.219} and nu_0 = 2.36e-6. DATA: analytic +
`qwen_38_experiment/data/rar_sparc_a0units.json`. PASS: U_eff(6.33e7)/U_eff(2) < 1e-2 while U(v) stays monotone. KILL:
U_eff bounded by s for every rho(g_bar). IMPACT: would void the legality obstruction that creates the entire 233x gap.

**I008 — Does the Q field equation give nu proportional to rho?** HYP: N4 ASSUMES nu = nu_0 rho/rho_0; nobody
has checked that the static Q equation returns a LINEAR response rather than another power near the wall.
USES: N2+N3+N4. DO: with sympy solve Z grad^2 Q = -K'(Q) + lambda_c rho for K = -M^4
sqrt(1-(Q-Q_0)^2/Lambda_D^2) in the small-x and near-wall limits, and read d log nu / d log rho off x =
(Q-Q_0)/Lambda_D = nu/sqrt(1+nu^2) over rho/rho_0 = 1 to 1e6. DATA: analytic (sympy). PASS: the exponent is 1
within 10% over the whole range. KILL: it departs from 1 by >30% anywhere below rho/rho_0 = 4.24e5 (the nu ~ 1
onset). IMPACT: validates or breaks the density law every N4 idea assumes.

**I009 — Is the a0-line itself legal?** HYP: the obstruction is single-valuedness of F(Y,Q), and U = sqrt(y^2+y) - y is
strictly increasing and bounded by 1/2 -- so Carl's own kernel may be LEGAL and the incompatibility sits elsewhere.
USES: N5+N6. DO: PRIOR: start from `real_research/reviews/typeII_legality_independent_2026.py`, which states the
condition. With sympy differentiate U = sqrt(y^2+y) - y, verify dU/dy > 0 on (0, inf), construct J_Y = y(U)/U by
inverting U, and check single-valuedness explicitly; then confirm U(2) = 0.449 (a0-line) vs 0.369 (legal family at s =
1/2). DATA: analytic (sympy). PASS: the a0-line is legal, so the obstruction must be restated. KILL: J_Y is
double-valued somewhere -- give the y. IMPACT: settles whether Carl's signature kernel is admissible at all.

**I010 — Invert the gap for nu_0 and confront the RAR ceiling.** HYP: closing R1 by density suppression demands a nu_0
that the RAR and recombination already exclude. USES: N2+N4+N6. DO: solve [(1+nu_0^2)/(1+(nu_0 R)^2)]^(1/4) =
1.27e-5/0.219 = 5.80e-5 for nu_0 at density contrasts R = rho_local/rho_0 in {1e2, 1e4, 4.24e5, 1e6, 1e8}; note the LHS
floors at (nu_0 R)^(-1/2) so check solvability first; compare the answer to nu_0 <= 2.36e-6 and to the recombination
pin. Repeat on the alt footing with 1.27e-5/0.173 = 7.34e-5. DATA: `nbody_2026/stage76_nu0_recombination_pin_2026.py`.
PASS: the required nu_0 sits inside both bounds. KILL: it exceeds 2.36e-6 by >10x -- the density escape from R1 is
CLOSED. IMPACT: a clean verdict on whether the promotion can ever close R1.

**I011 — grad a0 across the solar system as a new observable.** HYP: because a0 is a field its gradient gives
a tidal term distinct from the monopole anomaly -- and tides are what LLR bounds best. USES: N2+N4. DO: from
a0(nu) = a0(0)[(1+nu_0^2)/(1+nu^2)]^(1/4) with nu = nu_0 rho(r)/rho_0 get d a0/dr = -a0 (nu^2/(2(1+nu^2))) d
ln rho/d ln r / r; evaluate at r = 1 AU with the committed local dust profile at nu_0 = 2.36e-6, multiply by s
= 0.219 and by the Earth-Moon separation 3.84e8 m to get a differential acceleration in m s^-2. DATA: analytic
+ `nbody_2026/stage75_the_closed_theory_2026.py`. PASS: it exceeds the ~1e-14 m s^-2 LLR floor. KILL: below
1e-18 m s^-2. IMPACT: a solar-system test constant-a0 MOND cannot make.

**I012 — Is the RAR requirement on s really 0.558?** HYP: `U(y~2) >= 0.4` was read off the
a0-line; a proper fit may allow smaller s if Upsilon is refitted. DO: for s in
[0.05, 0.1, 0.2, 0.3, 0.5, 1, 2], refit Upsilon and report the best rms dex. DATA:
`ai_slop/website/public/data/rar_real_sparc.json`. PASS: some s < 0.1 reaches < 0.15 dex.
KILL: rms blows up below s ~ 0.4.

**I013 — The BTFR is s-blind asymptotically; measure its finite-mass CURVATURE instead.** HYP: U -> sqrt(y) for every legal s, so
V^4 = G M a0 is s-blind by theorem, but the APPROACH to it is not: the curvature of log V vs log M_bar at finite mass is an s-meter.
USES: N1+N6+N5. DO: PRIOR: the BTFR coefficient is EXACTLY 1 as a theorem of the convex field theory
(`real_research/reviews/mi_route_a_field_theory_2026.py`) -- assume it, do not refit it. Prove the asymptotic s-blindness in two
lines, compute log V(log M_bar) for J_Y = v/(1-v/s) at s = 0.1, 0.5, 2 over M_bar = 1e8-1e11 M_sun at a0 = 9.3619e-11 AND
1.1279e-10, fit a quadratic, compare its curvature to SPARC. DATA: `real_research/data/sparc_master_clean.csv`. PASS: the three s
separate by >2 sigma. KILL: below SPARC precision. IMPACT: an s-meter needing no a0 normalisation.

**I014 — Wide binaries as an s-meter against the filed DR4 band.** HYP: gamma_v for the legal family depends on s, so
Gaia DR4 measures the legality parameter directly. USES: N1+N6. DO: PRIOR: the registered 1.2139/1.2592 is RETRACTED (it
was the response tensor's largest eigenvalue declared isotropic); the in-force Amendment-10 band is 1.1614-1.1814
canonical / 1.1917-1.2267 alt, edge 1.23. COPY `prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py` into the scratch
dir (do NOT edit the original, PREREGISTRATION_DR4.md, or any *_HASH.txt), swap the kernel for J_Y = v/(1-v/s), compute
gamma_v at s = 0.05, 0.173, 0.219, 0.5, 1, 2. DATA: that script. PASS: neighbouring s separate by >0.02 AND some s lands
in 1.1614-1.1814. KILL: degenerate to <0.005. IMPACT: turns a filed prediction into a measurement of R1's numerator.

**I015 — Clusters as an s-meter with a0 suppressed in the core.** HYP: cluster cores are dense, so a0 is suppressed there, and eta(R500) depends
on s AND nu_0 jointly. USES: N4+N6+N1. DO: PRIOR: STANDING §4 records a structural TRAP -- cluster cores are LESS dense than galaxy inners, so no
density-monotone a0 law boosts clusters without boosting galaxies more; state which side of that trap your answer falls on. Compute eta(R500) for
s in {0.1, 0.2, 0.369, 0.449, 1, 2} with a0 evaluated at the local charge density via nu = nu_0 rho/rho_0 rather than a0(0); target is the
committed spread eta = 1.865 canonical / 1.722 alt on the operative MS08 kernel. DATA: `real_research/data/kt2017_groups.tsv` or
`real_research/data/xcop`. PASS: a (s, nu_0) pair with s <= 0.219 and nu_0 <= 2.36e-6 reaches eta >= 1.72. KILL: none at any allowed nu_0.
IMPACT: gives R4 a mechanism other than the a0-bump, or closes that door.

## B. The legal class — characterise it properly

**I016 — Full characterisation of the legal class, with the a0-line located in it.** HYP: J_Y = y(U)/U is a
bijection from strictly-increasing bounded U onto legal free functions, and the a0-line's U sits either inside
or outside it. USES: N5+N6. DO: with sympy prove or disprove that U -> J_Y(v) = v/U^-1(v) is injective on {U:
U' > 0, U bounded}; then evaluate U(2) for J_Y = v/(1-v/s) at s = 1/2 (expect 0.369) and for U = sqrt(y^2+y)-y
(expect 0.449), and show they are different FUNCTIONS by comparing U(y) at y = 0.1, 1, 2, 10, 1e3 -- a
reparameterisation would match at all five. DATA: analytic. PASS: bijection proved and the a0-line placed
inside or outside. KILL: an explicit counterexample. IMPACT: fixes once and for all which kernels R1 permits.

**I017 — Minimum-anomaly legal kernel at fixed RAR quality.** HYP: among legal U there is one minimising U at solar-system y subject
to rms <= 0.12 dex on the RAR. USES: N5+N6+N1. DO: PRIOR: `real_research/reviews/mi_extremal_kernel_lp_2026.py` settled the
extremal-kernel principle by LP -- reuse its formulation, do not rebuild it. Parameterise U by 6 knots at log10 y = -2, -1, 0, 1, 3,
7.8 with monotonicity enforced by construction (cumulative sum of positive increments); minimise U(y = 6.33e7) subject to RAR rms <=
0.12 dex with Upsilon FREE; report U(6.33e7)/1.27e-5 as the surviving ephemeris ratio, on both footings. DATA:
`qwen_38_experiment/data/rar_sparc_a0units.json`. PASS: the minimiser gets the ratio below 100x. KILL: it cannot go below 3000x.
IMPACT: measures how much of R1 is kernel choice, not structure.

**I018 — Does any property single out the a0-line inside the legal class?** HYP: analyticity in g_bar, an exact
algebraic g_obs-g_bar relation, or minimal parameter count picks out g_obs^2 = g_bar^2 + a0 g_bar. USES: N5+N6. DO:
PRIOR: `real_research/reviews/mi_routeA_admissibility_audit_2026.py` (31/31) already audited every PUBLISHED
admissibility condition -- test only the three properties it did NOT: (a) g_obs is algebraic of degree 2 in (g_obs,
g_bar, a0); (b) U analytic at y = 0 with U ~ sqrt(y); (c) exactly one dimensionful parameter. Evaluate each for U =
sqrt(y^2+y)-y and for J_Y = v/(1-v/s) at s = 0.2, 0.5, 1, 2. DATA: analytic (sympy). PASS: exactly one property selects
the a0-line and no s. KILL: every property is shared. IMPACT: upgrades N5 from a fit to a selection principle.

**I019 — Theorem: monotonicity alone fixes the gap, kernel-independently.** HYP: U strictly increasing with U -> s
implies U(y) <= s for ALL y, so any legal kernel fitting the RAR at y ~ 2 needs s >= U_RAR(2) -- the 13,600x gap is a
property of the CLASS, not a choice. USES: N5+N6+N1. DO: prove sup U = lim U = s in three lines; then read U_RAR(2) =
g_obs/a0 - 2 off the SPARC RAR in the bin y in [1.8, 2.2] on BOTH footings (a0 = 9.3619e-11 and 1.1279e-10 m s^-2) with
Upsilon free, and quote the resulting s floor and s_floor/1.27e-5. DATA:
`ai_slop/website/public/data/rar_real_sparc.json`. PASS: theorem holds and the floor is >= 0.17. KILL: a legal U with
U(2) >= 0.4 and s <= 1e-4 exists. IMPACT: closes kernel-shopping as an R1 escape in one line, or opens it.

**I020 — Let s depend on Q: is F(Y,Q) still single-valued? (S4)** HYP: legality was derived at fixed Q, but a0 is a
field, so the saturation scale may be s(Q) -- tiny where Q is dense (solar system), order 1/2 in galaxies. USES:
N2+N3+N6. DO: with sympy write J_Y = v/(1-v/s(Q)) with v = sqrt(Y)/a0(Q), a0(Q)^2 = kappa^2 G M^4
sqrt(1-(Q-Q_0)^2/Lambda_D^2); integrate J_Y dY at fixed Q to get F(Y,Q); require dF/dY invertible in Y at EVERY Q with
|Q-Q_0| < Lambda_D, i.e. d/dv[v J_Y] > 0; solve that inequality for admissible s(Q) and test s(Q) = s_0 (a0(Q)/a0(0))^p
for p in {-2, -1, 0, 1, 2}. DATA: analytic (sympy). PASS: a non-constant s(Q) is admissible and s(solar)/s(galaxy) <
1e-4. KILL: invertibility forces s constant. IMPACT: the only structural escape from R1 that keeps the framework.

**I021 — Legality at the wall, where a0 -> 0.** HYP: as |Q-Q_0| -> Lambda_D, a0 -> 0 so v = sqrt(Y)/a0
-> infinity and every legal U is pinned at s; check whether the legality criterion itself degenerates
there. USES: N3+N6+N2. DO: with epsilon = 1 - |Q-Q_0|/Lambda_D, expand the longitudinal stiffness
d/dv[v J_Y] and the mixed term F_YQ = dJ_Y/dQ in epsilon; evaluate at epsilon = 1e-1, 1e-3, 1e-6, 1e-9
and report the leading power of epsilon in each. DATA: analytic (sympy). PASS: the criterion
degenerates (leading power negative), so legality is vacuous at the wall. KILL: it tightens (positive
power). IMPACT: says whether N3's wall is a usable R1 regime or a boundary.

**I022 — Legality when Y is built from the total potential gradient.** HYP: if Y uses grad(Phi_total) rather than the scalar's own
gradient, the AQUAL-like variant may admit non-monotone U and rescue the a0-line. USES: N5+N6+N2. DO: use
`real_research/bridge1_aest_equations.md` as the reference transcription (THE_COMPLETION's copy is MIS-transcribed: F added not
subtracted, F outside not inside the 1/16 pi G-tilde prefactor). Substitute Y -> |grad Phi_total|^2 in its kinetic term, re-derive
the single-valuedness condition, and check whether the Q sector carrying recombination (a0(z=1090)/a0(0) = 6.0e-3) is left
untouched. DATA: that file. PASS: a consistent variant with non-monotone U and the recombination ratio moved by <10%. KILL: the Q
sector moves by >2x. IMPACT: an alternative relativistic home for N5 that dissolves R1.

**I023 — Does the c_123 = 0 aether cause the legality obstruction?** HYP: R5 and R1 may be one degeneracy -- the aether on
c_1+c_2+c_3 = 0 removes the term that would let U be non-monotone. USES: N2+N6. DO: PRIOR: stage74 found that at c_123 = 0 the
static longitudinal aether kinetic operator IS c_123, so the equation CHANGES TYPE there -- and K_B < 2.5e-5 and alpha_1 = 0 are
both WITHDRAWN. Retain c_1+c_2+c_3 = epsilon in the quasi-static (Y,Q) solve for epsilon in {1e-8, 1e-6, 1e-4, 1e-2}; report whether
d/dv[v J_Y] > 0 relaxes at O(epsilon) AND whether a0(Q) gains a preferred-frame correction. DATA:
`nbody_2026/stage70_ppn_preferred_frame_2026.py`, `nbody_2026/stage74_ppn_fork_adjudicated_2026.py`. PASS: the criterion relaxes at
O(epsilon). KILL: independent of epsilon. IMPACT: would merge R1 and R5 into a single repair.

**I024 — The 2x2 kinetic matrix with the DBI K supplying F_QQ.** HYP: the no-ghost condition on the (Y,Q) kinetic matrix, with F_QQ from the
brane, adds a term the scalar-only legality derivation missed. USES: N3+N6+N2. DO: PRIOR: the F_YQ mixing matrix and the embedding of F_Y and K
into AeST's single -F(Y,Q) slot are EXPLICITLY OWED -- this idea is that debt, so state the embedding you use. Build [[F_YY, F_YQ],[F_YQ, F_QQ]]
with F_QQ = d^2K/dQ^2 = -M^4 Lambda_D^-2 (1-x^2)^(-3/2) at x = (Q-Q_0)/Lambda_D; impose F_YY > 0 and F_YY F_QQ - F_YQ^2 > 0 (the entries carry
different units -- use these two scalars, never eigenvalues); evaluate at x = 0, 0.5, 0.9, 0.99 and read off the constraint on s. DATA: analytic
(sympy) + `real_research/bridge1_aest_equations.md`. PASS: a new constraint moving the s floor by >2x. KILL: the condition factorises and U is
untouched. IMPACT: tightens or loosens every R1 s-bound.

**I025 — Is the U-MODE superluminal on the DBI background?** HYP: legal kernels near saturation may propagate
the Y-sector perturbation faster than light on the brane background, killing the family outright. USES:
N3+N6+N2. DO: this is the Y-sector mode, NOT the Q-sector sound speed. Perturb Y about a static background
with J_Y = v/(1-v/s) and the brane fixing a0(x), x = (Q-Q_0)/Lambda_D; form c_U^2 = (J_Y + 2 Y J_YY)/J_Y in
units of c^2 and evaluate on the grid x in {0, 0.3, 0.6, 0.9, 0.99} times s in {1.27e-5, 1e-3, 0.173, 0.219,
0.5, 1}. DATA: analytic (sympy). PASS: c_U^2 in [0, 1] over the whole grid. KILL: c_U^2 > 1 or < 0 anywhere
with s >= 0.173 -- report the (x, s) cell. IMPACT: a health verdict on the entire legal family behind R1.

## C. kappa — what the promotion does to Carl's coefficient

**I026 — Is kappa physical, or a normalisation of Y?** HYP: a0^2 = kappa^2 G(-K) at the DBI minimum, where -K = M^4 =
rho_Lambda c^2, reproduces a0 = kappa c sqrt(G rho_Lambda) IDENTICALLY -- so kappa may be absorbable into the definition
of Y and carry no physics. USES: N1+N2+N3. DO: verify kappa^2 G rho_Lambda c^2 = (kappa c)^2 G rho_Lambda dimensionally
(G x energy density has units of acceleration^2); then apply Y -> lambda^2 Y, a0 -> lambda a0, J_Y -> J_Y/lambda for
lambda in {0.5, 1, 2} and check whether the RAR shape at fixed data, the BTFR coefficient (exactly 1 by theorem) or
gamma_v changes. DATA: analytic. PASS: an observable breaks the invariance, so kappa is physical. KILL: all three
invariant -- "derive kappa" is then the wrong question. IMPACT: tells us whether R3 is a real problem or bookkeeping.

**I027 — kappa and the local dark-energy deficit are degenerate. (S2)** HYP: a0^2 = kappa^2 G(-K) means SPARC measures
kappa*sqrt(-K_gal/M^4) = kappa/sqrt(gamma_gal), not kappa: if -K is suppressed inside a galaxy the fitted kappa is BIASED LOW, so
kappa = 0.529 +/- 0.034 is a lower bound on the true coefficient. USES: N1+N2+N3. DO: with gamma = sqrt(1+nu^2) and nu = nu_0
rho/rho_0, compute kappa_true = kappa_fit * gamma_gal^(1/4) for rho_gal/rho_0 in {1e2, 1e4, 1e5, 4.24e5, 1e6} at nu_0 = 2.36e-6 and
at nu_0 = 1e-4; report kappa_true and the nu_0 at which the correction equals the 0.034 error bar. DATA: analytic +
`real_research/rar_framework_a0_mlfit.py` for kappa_fit. PASS: the correction reaches 0.034 at some nu_0 <= 2.36e-6 -- R3's error
budget gains a new systematic. KILL: below 1e-3 for all allowed nu_0. IMPACT: prices a promotion-induced bias on R3.

**I028 — Re-measure kappa with the legal kernel instead of the a0-line.** HYP: kappa = 0.529 +/- 0.034 was measured through nu(y) =
sqrt(1+1/y); the legal family gives a different U at the same y, so kappa moves. USES: N1+N6+N5. DO: PRIOR: stage49's
RAR-SCATTER-MINIMISATION estimator is DEGENERATE (scatter moves 12% across a factor 1.94 in a0 because Upsilon absorbs it) -- do NOT
use it. Use the a0-line SLOPE estimator instead: fit g_obs^2 - g_bar^2 = a0 g_bar by total least squares with Upsilon refitted per
kernel for J_Y = v/(1-v/s) at s = 0.173, 0.219, 0.5, 1, 2, and report kappa +/- sigma per s on both footings. DATA:
`real_research/rar_framework_a0_mlfit.py` + `ai_slop/website/public/data/rar_real_sparc.json`. PASS: kappa within 2 sigma of 0.529
for some legal s. KILL: every legal s pushes kappa off by >3 sigma. IMPACT: prices R1's legality switch in the currency of R3.

**I029 — Does beta = 1 fix kappa?** HYP: the beta = 1 selection ties Lambda_D, M^4 and the mass scale mu, and a0^2 =
kappa^2 G(-K) may then leave kappa determined rather than free. USES: N2+N3+N7. DO: PRIOR: beta = 1 is SELECTED and
BOUNDARY-PINNED, never derived (stage20) -- do not re-argue it, assume it. With sympy write beta = mu^2 Lambda_D^2 / M^4
= 1, substitute M^4 = rho_Lambda c^2 = 5.36e-10 J m^-3, impose a0(Q_0) = 9.3619e-11 m s^-2 (and 1.1279e-10 on the alt
footing), and check whether kappa is forced or only mu is fixed; print the units of every factor. DATA: analytic (sympy)
+ `nbody_2026/stage20_beta_equals_one_derivation_2026.py`. PASS: kappa is determined to within 10%. KILL: kappa cancels
and only mu is fixed. IMPACT: either derives R3's coefficient or closes the brane route to it cleanly.

**I030 — Match the deep-MOND coefficient to the AeST printed form.** HYP: the 2/3 in J -> (2/3) Y^(3/2)/a0 is fixed by
the action, and matching it to the published 2 lambda_s/(3(1+lambda_s) a0) fixes a combination containing kappa. USES:
N1+N6+N2. DO: use `real_research/bridge1_aest_equations.md` as the reference transcription -- THE_COMPLETION's copy is
MIS-transcribed and must not be used. Expand J_Y = v/(1-v/s) at small v to O(v^3), extract the leading coefficient, and
match at FINITE lambda_s in {0.01, 0.1, 1, 10} rather than in the lambda_s -> 0 limit; report whether kappa survives the
match. DATA: that file. PASS: a relation containing kappa with no free normalisation left. KILL: kappa is absent from
the match. IMPACT: a second, action-side handle on R3.

**I031 — kappa from the gas-dominated subsample alone.** HYP: gas-dominated galaxies have no stellar M/L freedom, so they measure
kappa without the Upsilon degeneracy. USES: N1+N5. DO: PRIOR: the a0-line slope is RETRACTED as "shape-free" -- it carries a SHAPE
systematic of 26.3% across four kernels, comparable to or larger than what it is used to probe, so quote a shape systematic
alongside the statistical error or the result is void. Select SPARC galaxies with M_HI/(M_HI + 0.5*L36) > 0.8, fit g_obs^2 - g_bar^2
= a0 g_bar by total least squares, invert a0 = kappa c sqrt(G rho_Lambda) for kappa on both footings. DATA:
`real_research/data/sparc_master_clean.csv` + `ai_slop/website/public/data/rar_real_sparc.json`. PASS: sigma_kappa(stat + shape) <
0.05. KILL: fewer than 15 galaxies pass the cut. IMPACT: the cleanest available measurement of R3's coefficient.

**I032 — a0's correlation length: is a per-galaxy kappa even defined? (S1)** HYP: the Q excitation has mass^2 = K''(Q_0)/Z = M^4/(Z Lambda_D^2),
so a0 cannot vary faster than lambda_a0 = 1/m; if lambda_a0 exceeds a galaxy, "the a0 of this galaxy" is not a local quantity and per-object
kappa scatter is unphysical. USES: N1+N2+N3+N7. DO: compute lambda_a0 in kpc for Lambda_D/Q_0 in {1e-9, 1e-8, 1e-7, 1e-6, 3.1e-6} at Q_0 = 0.0024
and 0.0146 Mpc^-1; compare with 20 kpc (a disc), 1 Mpc (a cluster) and 5 Mpc (SPARC's inter-galaxy spacing). DATA: analytic + the Z normalisation
in `real_research/bridge1_aest_equations.md`. PASS: lambda_a0 < 20 kpc somewhere in the band, so a per-galaxy a0 is meaningful. KILL: lambda_a0 >
5 Mpc everywhere -- then every environment test in this corpus is measuring one shared a0 and the nu_0 bounds must be re-read. IMPACT: decides
whether per-object kappa scatter is signal or nonsense.

**I033 — Does the SAME Z fix kappa and the a0-wave speed? (S1)** HYP: kappa = 1/2 is identically Z = 2 sqrt(8 pi/3); if Z is also the coefficient
of (grad Q)^2 in the action, then the propagation speed of an a0 disturbance is fixed by the same number, giving a second, independent handle on
Z. USES: N1+N2+N3. DO: PRIOR: `nbody_2026/stage43_kappa_reduction_one_factor_2026.py` proved "kappa = 1/2" is identically "Z = 2 sqrt(8 pi/3)" --
assume it. Read the (grad Q)^2 coefficient off `real_research/bridge1_aest_equations.md`, ask symbolically whether it is the SAME Z (state the
identification or its failure explicitly), and if so compute c_a0^2 = Z_kin/Z_mass at Z = 2 sqrt(8 pi/3) = 5.79 and report it in units of c^2.
DATA: that file (sympy). PASS: the two Z's are the same object and c_a0^2 lands in [0, 1]. KILL: they are different objects -- say so plainly and
record that the reduction is bookkeeping only. IMPACT: a second constraint on R3's one free number.

**I034 — Does the promotion break the Ward identity that protects a0?** HYP: the exact shift symmetry closes the ADDITIVE renormalisation of a0
to all orders; but the promotion makes a0 a function of Q, and a Q-dependent a0 is not shift-invariant, so kappa may run. USES: N1+N2+N3. DO:
PRIOR: `real_research/reviews/mi_twoloop_alpha2_transfer_2026.py` (14 checks) established the additive channel is closed to all orders by the
Ward identity and the multiplicative one at two loops -- do not redo either. Write the shift Q -> Q + c and check whether a0^2(Q) = kappa^2 G M^4
sqrt(1-(Q-Q_0)^2/Lambda_D^2) is invariant; if not, identify the operator that breaks it and compute d ln kappa / d ln mu at one loop from its
anomalous dimension. DATA: analytic (sympy). PASS: kappa runs by <1% per decade of scale, so 0.529 is scale-safe. KILL: it runs by >10% per
decade -- then "measure kappa" needs a stated scale. IMPACT: says whether R3's number is even scale-independent.

**I035 — The promotion predicts kappa(cluster) != kappa(galaxy) by a computable factor.** HYP: kappa_fit measured in an object equals
kappa/sqrt(gamma_obj), so the RATIO kappa_clus/kappa_gal = (gamma_gal/gamma_clus)^(1/4) is a pure prediction with no normalisation -- and it is
testable against the committed cluster eta spread. USES: N1+N4+N2. DO: PRIOR: the committed cluster target is eta(R500) = 1.865 canonical / 1.722
alt on the operative MS08 kernel (NOT 2.084/1.917, which is the a0-line kernel, and NOT 2.334, which is eRASS1-specific). Compute gamma =
sqrt(1+nu^2) at rho/rho_0 = 1e5 (cluster R500), 1e6 (galaxy inner) and 1e3 (cluster outskirt) for nu_0 = 2.36e-6 and 1e-4; form the ratio;
convert into the fractional change in eta. DATA: `real_research/data/xcop`. PASS: the ratio moves eta by >5% at some allowed nu_0 -- a
promotion-specific cluster signal. KILL: <0.1% everywhere. IMPACT: ties R3 and R4 to one number.

## D. The dust problem (R2) — and the equation of motion a0 itself obeys (S1)

**I036 — Write a0's equation of motion. (S1)** HYP: the corpus has only ever treated a0 as a number that happens to vary; the promotion makes it
a field, so it has a wave equation with a mass, a source and a speed -- none of which anyone has written down. USES: N2+N3+N7. DO: start from the
Q equation Z (box Q) = -dK/dQ + lambda_c rho with K = -M^4 sqrt(1-(Q-Q_0)^2/Lambda_D^2); substitute Q = Q(a0) by inverting a0^2 = kappa^2 G(-K),
i.e. (Q-Q_0)/Lambda_D = sqrt(1-(a0/a0(0))^4); derive the resulting box a0 = m_a0^2 (a0 - a0(0)) + S[rho] + (nonlinear grad terms) with sympy and
print m_a0^2 in m^-2 and the source coefficient in SI. DATA: analytic (sympy) + `real_research/bridge1_aest_equations.md` for Z. PASS: a closed
second-order equation with a finite m_a0^2 at Q = Q_0. PARTIAL EXPECTED: the linearised equation alone counts as delivered. KILL: the inversion
is singular at the minimum -- report where. IMPACT: opens S1; every later a0-field idea needs this equation.

**I037 — Is the dust forced to be irrotational?** HYP: the corpus assumes an irrotational
potential flow; if vorticity is allowed, centrifugal support evades all five filters. DO:
check whether the shift symmetry plus the equation of motion forbid vorticity identically or
only for irrotational initial data. PASS: vorticity allowed. KILL: forbidden identically.
**This is the highest-value item in section D.**

**I038 — Does a0 LAG the density it tracks, and by how much? (S1)** HYP: N4 is a STATIC relation a0(nu(rho)); if the a0 field relaxes on a
timescale longer than a halo's dynamical time, the real a0 is set by the density the object had in the PAST, and the local reading of N4 is
wrong. USES: N2+N4+N3. DO: from I036's linearised equation the relaxation time is tau = 1/(m_a0 c) with m_a0^2 = M^4/(Z Lambda_D^2); compute tau
in Gyr for Lambda_D/Q_0 in {1e-9, 1e-8, 1e-7, 1e-6, 3.1e-6} at both ends of the Q_0 pin 0.0024-0.0146 Mpc^-1, and compare to (a) a disc dynamical
time 0.25 Gyr, (b) a cluster crossing time 2 Gyr, (c) the Hubble time 13.8 Gyr. DATA: analytic. PASS: tau > 13.8 Gyr somewhere in the band --
then a0 is frozen at its formation value and the local reading of N4 is REPLACED by a formation-epoch reading (see I090). KILL: tau < 0.25 Gyr
everywhere. IMPACT: decides which of N4's two readings is physical.

**I039 — The promotion supplies the outward-FALLING scalar that F5 needs.** HYP: F5 kills gates monotone in a quantity that RISES outward; nu =
nu_0 rho/rho_0 FALLS outward, so a gate built on nu (equivalently on a0, which RISES outward) has the right sign everywhere. USES: N2+N4+N7. DO:
PRIOR: the catalogue's free theorem is r_x/R_supp = [M_bar/((pi^2/3) M_dust)]^(1/3) = 0.194, fixed by the baryon-to-dust ratio ALONE -- compute
that first, it costs nothing, and if the nu gate reproduces 0.194 the idea is dead on arrival. Then substitute the nu gate for the |grad phi|
gate in `dust_filters.crossover_fraction` and `mass_fraction_anti_supported` and recompute r_x/R_supp and the anti-supported mass fraction. DATA:
`qwen_38_experiment/dust_filters.py`, `real_research/reviews/second_field_catalog_2026.py`. PASS: r_x/R_supp > 0.9 AND anti-supported fraction <
10%. KILL: r_x/R_supp = 0.194 +/- 0.02. IMPACT: the framework's own field would supply the support R2 needs.

**I040 — What happens to a0 across an accretion shock? (S1)** HYP: a0 is continuous only if its field equation is second order with
finite coefficients; at a cluster accretion shock rho jumps by 4x in a sound-crossing time, so a0 must either jump, ring, or lag --
and a ringing a0 is a signal no MOND theory has. USES: N2+N4+N3. DO: take I036's linearised equation with a step source rho -> 4 rho
at t = 0; solve for a0(t) analytically (damped oscillator with m_a0 from M^4/(Z Lambda_D^2)); report the overshoot amplitude delta
a0/a0 and the ringing period in Myr for Lambda_D/Q_0 in {1e-9, 1e-7, 3.1e-6} at nu_0 = 2.36e-6 and 1e-4. DATA: analytic. PASS:
overshoot > 1% and period < 1 Gyr -- a post-shock a0 gradient that X-ray + lensing could resolve. KILL: overshoot < 1e-6 (the jump
is quasi-static and a0 is slaved to rho). IMPACT: a spatially resolved discriminator at cluster shock fronts.

**I041 — Which input dominates the Sgr A* falsification?** HYP: the 5.8e5x margin rests on one or two inputs. USES: N4+N7+N3. DO:
PRIOR: the margin is set in `nbody_2026/stage2_spherical_collapse_2026.py` and `nbody_2026/stage3_wave_and_cap_endpoint_2026.py`
(wave scale 0.18 AU); re-derive the 5.8e5x from those, then sweep each input a factor 10 each way -- dust fraction f, initial
overdensity, a0 suppression via nu at nu_0 = 2.36e-6, formation redshift z_f in {2, 6, 10, 20} -- and sweep Q_0 across 0.0024-0.0146
Mpc^-1, which sets the dust mass through rho = Q_0 n. Report a one-factor-at-a-time sensitivity table (d log margin / d log input).
DATA: those two files + `nbody_2026/stage75_the_closed_theory_2026.py`. PASS: a physically allowed corner where the margin drops
below 10x. KILL: no single input moves it below 1e4x. IMPACT: locates the one number in R2 that must be wrong.

**I042 — Split the charge: how much of it can be dust?** HYP: a fraction f of the shift charge is dust and 1-f is something else; the CMB
clustering requirement bounds f from below and the collapse bounds it from above. USES: N4+N7+N2. DO: PRIOR: breaking the shift symmetry frees
the CHARGE but NOT the ENERGY (stage6; nabla_mu T^munu = 0), so f is a split of the charge only -- say what carries the remaining energy or the
idea fails C4. With rho = f Q_0 n at Q_0 = 0.0024 and 0.0146 Mpc^-1, compute the CMB-required clustering amplitude vs f on a grid f in {0.01,
0.03, 0.1, 0.3, 0.5, 1} at the committed nu_0 pin, and the collapse endpoint vs f; intersect the two intervals. DATA:
`nbody_2026/stage76_nu0_recombination_pin_2026.py`, `nbody_2026/stage6_break_shift_symmetry_2026.py` if present else stage75. PASS: a non-empty f
interval. KILL: empty by more than 2x. IMPACT: even a partial split removes R2's black-hole endpoint.

**I043 — Redo the 690 Gyr transport time with the framework's own gravity.** HYP: the committed transport timescale used
Newtonian gravity; with g = nu(y) g_bar and the derived a0(z) it may fall below a Hubble time. USES: N4+N5+N2. DO:
PRIOR: 690 Gyr is the committed number from `nbody_2026/stage6_audit_transport_channels_2026.py` (else stage75) --
reproduce it first as a control, then recompute with g = sqrt(g_bar^2 + a0 g_bar) using a0 evaluated from a0(nu)/a0(0) =
[(1+nu_0^2)/(1+nu^2)]^(1/4) along the committed density history, at nu_0 = 2.36e-6 and 1e-4. Price the rate at the
slowest step and name which radius that is. DATA: that file + `real_research/data/a0_of_z.csv`. PASS: below 13.8 Gyr.
KILL: still >100 Gyr. IMPACT: would let the energy leave, which R2's charge argument forbids.

**I044 — The a0-gate escape corner.** HYP: a support gate switched by the framework's own field has only ever been tested where the
gate variable is large; where nu(r_supp) is small the gate has never been evaluated. USES: N4+N7+N2. DO: define the gate explicitly
as G(r) = [1 + (nu(r)/nu_c)^p]^-1 with nu(r) = nu_0 rho(r)/rho_0 -- note nu_0 * r_supp is NOT dimensionless (nu_0 is a pure number,
r_supp a length), the gate variable is nu(r_supp). Map the (nu_0, rho(r_supp)/rho_0) plane on nu_0 in {1e-8, 1e-7, 1e-6, 2.36e-6}
times rho/rho_0 in {1e2, 1e4, 1e6, 1e8}, mark the cells with nu(r_supp) < 10, and screen each surviving cell with `dust_filters.py`.
DATA: analytic + `qwen_38_experiment/dust_filters.py`. PASS: a cell passes all five filters at nu_0 <= 2.36e-6. KILL: every such
cell needs nu_0 above the ceiling. IMPACT: a surviving corner reopens R2.

**I045 — Maximum lensing pile-up at 0.3-1 Mpc, as a sixth filter.** HYP: the KiDS weak-lensing RAR fit caps how much extra mass the collapsed
dust may add. USES: N1+N5+N2. DO: PRIOR: the pure framework already fits the KiDS lensing RAR from 40 kpc to 2.2 Mpc at chi^2/dof = 2.03
canonical / 0.94 alt with NO dark component (stage12), and that same fit rejected Route A' at Delta chi^2 up to +1698 -- start from those
residuals. Take g_obs^2 = g_bar^2 + a0 g_bar at a0 = 9.3619e-11 AND 1.1279e-10 m s^-2, compute the 2-sigma upper limit on excess enclosed mass at
0.3, 0.5 and 1 Mpc, express as a tolerance curve M_excess_max(r), and APPEND it to `dust_filters.py` as F6 WITHOUT altering F1-F5. DATA:
`prep_2026/kids_rar/kids_rar_lambda.py`, `nbody_2026/stage12_lensing_stack_fit_2026.py`. PASS: a usable curve on both footings. KILL: the KiDS
errors are too wide to bound anything. IMPACT: a new independent filter on every R2 escape.

**I046 — Rotation-curve signature of the a0 dip inside a dust concentration.** HYP: where dust concentrates, nu rises and a0 falls,
giving a LOCAL dip in the MOND enhancement -- a wiggle no constant-a0 theory predicts. USES: N2+N4+N5. DO: state up front that the
effect is O(nu^2), so the dip is invisible unless rho/rho_0 approaches 1/nu_0 = 4.24e5; therefore FIRST solve nu = nu_0 rho/rho_0 =
1 for the required rho/rho_0 at nu_0 in {2.36e-6, 1e-5, 1e-4}, then take a committed dust concentration profile, compute a0(r) from
N4, and plot v_c(r) = sqrt(r sqrt(g_bar^2 + a0(r) g_bar)) over 0.1-10 kpc against the constant-a0 curve for a representative SPARC
baryon profile. DATA: `real_research/data/sparc_master_clean.csv`. PASS: >5 km/s difference at some radius with rho/rho_0 inside the
committed profile. KILL: <1 km/s everywhere. IMPACT: a named observable separating N2 from standard MOND.

**I047 — Recompute the twist band that is "empty by 2.77x".** HYP: R2's vorticity band was closed by 2.77x assuming constant a0;
with a0 suppressed inside the rotating concentration the required rotation drops. USES: N2+N4+N5. DO: PRIOR: irrotationality is NOT
a theorem once the dust rides A^mu (the twist propagates) -- the closure is the 2.77x band, not a proof, so this is the live crack.
Write centrifugal support as omega^2 R = g(R) with g = sqrt(g_bar^2 + a0 g_bar) and a0 -> a0(0)[(1+nu_0^2)/(1+nu^2)]^(1/4), nu =
nu_0 rho/rho_0; recompute the ratio that was 2.77 for nu_0 in {2.36e-6, 1e-5, 1e-4} and rho/rho_0 in {1e4, 1e6, 1e8}. DATA:
`nbody_2026/stage75_the_closed_theory_2026.py`. PASS: the band opens (ratio < 1) at some allowed nu_0. KILL: it stays above 2 for
every allowed nu_0. IMPACT: rotation would support the dust and remove R2's endpoint.

**I048 — Does the DUST collapse finish inside a Hubble time with a0(z)?** HYP: a0(z) makes the MOND enhancement weakest at high z, so the
dark-sector dust's collapse -- not a baryonic halo's -- may never complete. USES: N4+N5+N2. DO: PRIOR:
`nbody_2026/stage26_collapse_acceleration_own_terms_2026.py` already gives the BARYONIC boost 2.03x at z=6 falling to 1.14x at z=25, priced at
TURNAROUND, not the virial radius -- reuse its machinery and do NOT re-derive those numbers; the new object is the DUST, whose own density
history differs. Integrate the spherical collapse time for the committed dust profile with g = nu(y) g_bar, nu(y) = sqrt(1+1/y), and a0 from N4
at each epoch; price at turnaround; compare to 13.8 Gyr. DATA: that file + `real_research/data/a0_of_z.csv`. PASS: exceeds 13.8 Gyr for some nu_0
<= 2.36e-6. KILL: shorter by >10x. IMPACT: an unfinished collapse defuses R2's Sgr A* number.

**I049 — Does the a0 field's own gradient energy weigh anything? (S1)** HYP: if a0 varies across a halo then Q varies, and that gradient carries energy density (1/2) K_QQ(0)
(dQ/dr)^2, which lenses like any other mass -- a component nobody has priced. USES: N2+N3+N7. DO: with K_QQ(0) = M^4/Lambda_D^2 and M^4 = rho_Lambda c^2, build x(r) =
(Q-Q_0)/Lambda_D by solving (1-x^2)^(1/4) = [(1+nu_0^2)/(1+nu(r)^2)]^(1/4) with nu(r) = nu_0 rho_NFW(r)/rho_0 for M_200 = 1e12 Msun, c = 10, r_200 = 200 kpc; form dQ/dr = Lambda_D
dx/dr numerically; integrate M_grad = (4 pi/c^2) int_0^{200 kpc} (1/2) K_QQ(0) (dQ/dr)^2 r^2 dr and report M_grad/M_200 for nu_0 in {2.36e-6, 1.77e-4}, Q_0 in {0.0024, 0.0146}
Mpc^-1 and Lambda_D/Q_0 in {2.3e-9, 1e-7, 3.1e-6}, both footings. State the units of Z and K_QQ explicitly and carry them. DATA: analytic +
`real_research/bridge1_aest_equations.md`. PASS: M_grad/M_200 > 0.01 in any cell -- the a0 field is itself a lensing mass and every lensing fit inherits it. KILL: < 1e-8 everywhere
-- the a0 field is weightless; record it as the licence for ignoring it. IMPACT: prices an unaccounted lensing mass carried by the a0 field.

**I050 — Bound the solar-system dust mass from the same ephemeris data.** HYP: the dust is rho = Q_0 n, so any local concentration
adds Newtonian mass inside planetary orbits, and the precession data that bound s also bound that mass. USES: N4+N7+N1. DO: a
uniform density rho_d inside radius R adds delta a = (4 pi/3) G rho_d r; equate to the Sereno-Jetzer-inverted limits dA_R <=
3.66e-14 m/s^2 (Earth) and 3.72e-14 (Mars) to get rho_d,max and hence M_max inside 1, 5 and 40 AU; then compute the rho_d the
density law needs for a0(nu)/a0(0) <= 5.80e-5 at nu_0 = 2.36e-6 (i.e. rho/rho_0 >= 1/(nu_0 * 5.8e-5^-2)) and compare. DATA:
`real_research/reviews/a0_local_ephemeris_2026.py`. PASS: the needed concentration sits below the mass bound. KILL: it exceeds the
bound by >10x. IMPACT: closes or opens R1's density escape using solar-system data alone.

## E. a0(z), cosmology, CLASS — and inhomogeneous dark energy (S2)

**I051 — Recombination a0 from the LOCAL-density law, not the CPL law.** HYP: read locally, a0(nu)/a0(0) =
[(1+nu_0^2)/(1+nu^2)]^(1/4) with nu = nu_0 rho/rho_0 gives a DIFFERENT recombination off-switch than the retired CPL number 0.0060.
USES: N2+N4. DO: set rho/rho_0 = (1+z)^3 at z = 1090 (so rho/rho_0 = 1.30e9), nu_0 = 2.36e-6, evaluate the ratio analytically; then
sweep nu_0 over {1e-8, 1e-7, 1e-6, 2.36e-6} and tabulate the off-switch at z = 10, 100, 1090, 3400. PRIOR: the CPL law's 6.0e-3 is
SETTLED but comes from `nbody_2026/stage17_a0z_from_the_action_2026.py`, a different reading -- report both side by side and name
which is operative. DATA: analytic + that file. PASS: ratio < 0.05 at z=1090 for the whole nu_0 range. KILL: > 0.1 anywhere. IMPACT:
replaces a retired number; the CMB clustering pass stays a prediction.

**I052 — How much of the nu_0 <= 2.36e-6 ceiling is an Upsilon-treatment artefact?** HYP: the ceiling was read off raw RAR scatter at one Upsilon
convention, so the number every downstream idea quotes may move with that choice alone. USES: N1+N4+N5. DO: PRIOR: freezing Upsilon is a named
corpus failure mode (it produced the retracted "anchored a0 fits BETTER") -- the whole point here is to unfreeze it. COPY
`real_research/rar_framework_a0_mlfit.py` to scratch, insert a0 -> a0(0)*[(1+nu_0^2)/(1+nu^2)]^(1/4) using Sigma_bar/Sigma_0 as an
explicitly-stated dimensionless STAND-IN for rho/rho_0, and profile nu_0 over {1e-8 ... 1e-3} under three treatments: Upsilon = 0.5 fixed, 0.7
fixed, free per galaxy. DATA: `ai_slop/website/public/data/rar_real_sparc.json` + `real_research/data/sparc_master_clean.csv`. PASS: the three
ceilings agree within 2x. KILL: they span >5x. IMPACT: prices the corpus's most-quoted small number, on which N4 rests.

**I053 — The promotion predicts a0 FALLING with redshift; MUSE says rising.** HYP: higher z means higher rho means higher nu, so N4 forces a0(z)
to DECREASE with z -- the opposite sign to MUSE-DARK III. USES: N4+N2. DO: PRIOR: "MUSE confirms rising a0" is RETRACTED as support and the front
was re-graded shared-not-distinctive AND a SHARP NULL (any robust a0 evolution below z ~ 5 falsifies) -- see
`nbody_2026/stage21_muse_msa_reexam_derived_law_2026.py`. Compute a0(z)/a0(0) = [(1+nu_0^2)/(1+(nu_0(1+z)^3)^2)]^(1/4) at the MUSE redshifts for
nu_0 in {1e-8, 1e-6, 2.36e-6}, overlay the measured points with errors, report the SIGNED tension in sigma on both footings. DATA:
`real_research/data/a0_of_z.csv` + that stage. PASS: the framework curve sits within 2 sigma. KILL: > 3 sigma with the sign wrong. IMPACT: a sign
test that could falsify the promotion outright.

**I054 — nu is the DBI brane's rapidity: prove a0 goes as gamma^(-1/2).** HYP: N4 and N3 are the same statement -- (Q-Q_0)/Lambda_D =
nu/sqrt(1+nu^2) makes -K = M^4 sqrt(1-x^2) = M^4/gamma with gamma = sqrt(1+nu^2), so a0 proportional to (-K)^(1/2) is gamma^(-1/2), i.e. N4
exactly. USES: N3+N4+N2. DO: with sympy substitute x = nu/sqrt(1+nu^2) into a0^2 = kappa^2 G(-K(Q)) and test whether it equals a0(0)^2
[(1+nu_0^2)/(1+nu^2)]^(1/2) IDENTICALLY (use `sympy.simplify` on the difference, and confirm at nu = 0, 1e-6, 1, 10, 1e3 numerically). DATA:
analytic (sympy). PASS: the identity holds symbolically -- nu is a boost, gamma a Lorentz factor, and the wall x -> 1 is nu -> infinity, hence
unreachable rather than a cliff. KILL: a residual function of nu survives -- print it, because then N3 and N4 are two different laws and one of
them is misstated. IMPACT: turns two postulates into one and decides whether N3's wall is reachable.

**I055 — Lambda_D/Q_0 re-bounded at the pinned Q_0 by the forest.** HYP: the Ly-alpha bound on Lambda_D/Q_0 predates the Q_0 pin at 0.0024-0.0146 Mpc^-1; the
pin narrows it. USES: N3+N4+N7. DO: PRIOR: the forest bound is a BRACKET with NEITHER edge established -- Lambda_D/Q_0 <= 2.3e-9 (linear-only) OR looser by
orders (response-active); post-recombination growth separately needs Lambda_D/Q_0 <= 1.5-3.1e-6; and Lambda_D = Q_0 is EXCLUDED (c_s^2 = 0.25 during growth).
Quote all three, then at both ends of the Q_0 pin write the forest-epoch excursion as x = (Q-Q_0)/Lambda_D = nu/sqrt(1+nu^2) with nu = nu_0 (1+z)^3 at z = 3,
convert |Q-Q_0| to Mpc^-1, demand x <= 0.1, and report the allowed Lambda_D interval in Mpc^-1. DATA: analytic + `nbody_2026/stage69_cs2_growth_class_2026.py`.
PARTIAL EXPECTED: the transfer function may need reading from the corpus; the x <= 0.1 interval alone counts. PASS: non-empty at both ends. KILL: empty at
either end. IMPACT: converts a free brane scale into a bounded number.

**I056 — Where does the brane cross from dust to dark energy?** HYP: the DBI brane is pressureless dust at
large nu and w = -1 at nu = 0, so w(nu) has a crossover epoch that must sit inside matter domination. USES:
N3+N4+N7. DO: use p = K = -M^4/gamma and rho = M^4 gamma -- NOT rho = 2 Y K_Y - K, which gives w = -1
identically for a K of Q alone -- giving w = -1/(1+nu^2); solve w = -1/2 (nu = 1) and w = -0.1 (nu = 3) and
convert to z by nu = nu_0 (1+z)^3, for nu_0 in {1e-8, 1e-7, 1e-6, 2.36e-6}. DATA: analytic (sympy). PASS: the
w = -1/2 crossover z lies in [10, 3400] for every nu_0 in that set. KILL: outside that window anywhere -- name
the nu_0. IMPACT: one field supplying both R2's dust and Lambda, or not.

**I057 — The ISW signal from inhomogeneous dark energy. (S2)** HYP: a0^2 = kappa^2 G(-K) with -K a field says dark energy is SUPPRESSED wherever
the charge is dense -- so Phi decays differently in clusters and voids and the ISW cross-correlation with galaxies carries a term LCDM does not
have. USES: N1+N2+N3. DO: compute the local dark-energy fraction (-K)/M^4 = 1/gamma = 1/sqrt(1+nu^2) with nu = nu_0 rho/rho_0 at rho/rho_0 = 1e5
(cluster), 1e2 (wall), 0.2 (void) for nu_0 in {2.36e-6, 1e-5, 1e-4}; feed the resulting delta rho_Lambda/rho_Lambda into the linear ISW kernel
dPhi/dz and report the fractional change in the ISW-galaxy cross-power at l = 10-100 against the measured ~3 sigma detection amplitude. DATA:
analytic. PARTIAL EXPECTED: the deficit table alone counts as delivered. PASS: the change exceeds 10% of the measured amplitude at some allowed
nu_0. KILL: below 1e-4 everywhere. IMPACT: opens S2 with a real observable; a second sector from N1+N2.

**I058 — Is w = -1 exact today, and can the brane mimic DESI's w(z)?** HYP: w = -1/(1+nu^2) is always >= -1 and RISES with z (nu
grows as (1+z)^3), while DESI's CPL fit wants w below -1 at high z -- opposite signs. USES: N3+N4+N7. DO: PRIOR: w = -1 + O(nu_0^2)
with offset 1e-10 to 1e-8 is SETTLED, and the "DESI-CPL a0(z) bump at z ~ 0.4" is RETRACTED as never self-consistent with w = -1 --
do not resurrect it. The NEW content is the SIGN: evaluate |w+1| at nu = nu_0 for nu_0 = 2.36e-6 and 1e-8, confirm the leading power
is nu_0^2, then map w(z) over 0 < z < 2 and compare the sign of dw/dz with DESI DR2's published w_0-w_a contour. DATA: analytic +
published DESI w_0-w_a values. PASS: |w+1| < 1e-6 today AND dw/dz agrees in sign with DESI. KILL: signs opposite at > 3 sigma.
IMPACT: says whether DESI can falsify the brane outright.

**I059 — Does the promoted a0 cluster? DE perturbations from the brane.** HYP: if a0 is a field, its fluctuations are dark-pressure fluctuations,
so the dark energy is not smooth; the DBI sound speed sets the scale. USES: N2+N3+N7. DO: PRIOR: the AeST lambda_J = 2.7 Mpc number is RETRACTED
(the k^4 Jeans term is 11 orders too small) -- derive your own and never quote it. Compute c_s^2 = K_Y/(K_Y + 2 Y K_YY) for the beta=1 brane at
nu = nu_0, verify it reduces to 1/gamma^2 = 1/(1+nu_0^2), convert to a comoving Jeans wavelength lambda_J = 2 pi c_s/(sqrt(4 pi G rho) a) in Mpc
at z = 0, 1, 10, and compare with the horizon and with 1/Q_0 at both ends of the pin. DATA: analytic +
`real_research/reviews/mi_cosmo_perturbations_2026.py`. PASS: c_s^2 within a factor 10 of 1 (DE smooth). KILL: c_s^2 << 1, i.e. the dark energy
clusters sub-horizon -- then name the observable. IMPACT: clears the DE sector or hands over a new signal.

**I060 — Does a nonzero a0 at recombination shift the sound horizon?** HYP: even the small a0 from I051 adds a MOND correction to the
baryon-photon fluid's gravity and could move r_s. USES: N2+N4. DO: PRIOR: the real CLASS run with the DERIVED a0(z) law is already at 0.01 sigma
vs cosmic variance (`nbody_2026/stage19_class_rerun_derived_law_2026.py`) -- reproduce that as the control, then the NEW test is r_s
specifically, which that run did not isolate. Multiply the gravitational source by nu(y) = sqrt(1+1/y) evaluated at the I051 recombination a0 (y
= g_bar/a0 with g_bar the fluid's own self-gravity), and report delta r_s in Mpc and delta theta_s in Planck sigmas. DATA: CLASS + that stage.
PARTIAL EXPECTED: a crude effective-G rescaling, not a full modified solver; report the rescaling factor and the resulting delta theta_s. PASS:
|delta theta_s| < 0.2 sigma. KILL: > 1 sigma. IMPACT: confirms or breaks the framework's cleanest cosmological pass.

## F. Clusters and large scale

**I061 — Does the monotone promotion FORBID the a0-bump?** HYP: R4's only live candidate needs mu^2_eff PEAKED at a0, but N4 makes a0 fall
monotonically with density -- so the bump may be inconsistent with the promotion it is supposed to live inside. USES: N2+N4+N1. DO: PRIOR: the
bump response is EXACTLY x/(1+x)^2 with x = Y/A -- single maximum at x = 1, half-maxima at 3 +/- 2 sqrt2, inflection at x = 2, and there is NO
sub-peak; A_max in [2.72, 4.46]x fiducial. Substitute A -> A(rho) via a0(nu) so that x = Y/A(nu_0 rho/rho_0), and ask whether d(response)/dY
still has a single interior zero once A slides with rho; evaluate on rho/rho_0 in {1e2, 1e4, 1e6} at nu_0 in {2.36e-6, 1e-4}. DATA: analytic +
`real_research/reviews/mi_a0_bump_response_2026.py`. PASS: the interior maximum survives with |x_peak - 1| < 0.1. KILL: the peak washes out or
moves to the boundary -- R4's sole candidate dies. IMPACT: decides whether R4's only live mechanism is self-consistent with N2.

**I062 — How far does a0 fall in a cluster core?** HYP: N4 makes a0 decrease with local charge density, so cluster cores have their own
suppressed a0 -- quantify it instead of quoting "13x at 1e6 rho_dm0". USES: N4+N7+N2. DO: PRIOR: `nbody_2026/stage59_local_a0_verdict_2026.py`
gives the committed statement (A suppressed ~2-4% in halos, 13x at 1e6 rho_dm0) -- reproduce it as a control, then replace it with the N4
computation. Take an NFW charge profile with c = 5, M500 = 5e14 M_sun, set its charge density by rho = Q_0 n at Q_0 = 0.0024 and 0.0146 Mpc^-1,
compute nu(r) = nu_0 rho(r)/rho_0 and a0(r)/a0(0) from 10 kpc to 3 Mpc, tabulate at the core (50 kpc) and R500, and state the rho/rho_0 that
WOULD give 13x. DATA: `real_research/data/xcop` if readable, else the analytic NFW. PASS: a0(R500)/a0(0) > 0.9. KILL: < 0.5. IMPACT: replaces a
corpus number with the framework's own; prices R4's lever.

**I063 — Cluster eta under the LEGAL family, not the a0-line.** HYP: published cluster eta used the a0-line kernel, which N6 may forbid; the
legal family U -> s gives a different eta. USES: N6+N5+N1. DO: PRIOR: the committed targets are eta(R500) = 1.865 canonical / 1.722 alt on the
OPERATIVE MS08 kernel nu = 1/(1-e^-sqrt(y)), and 2.084/1.917 on the a0-line kernel -- quote the spread with the kernel named, never unqualified.
For s in {0.1, 0.2, 0.369, 0.449, 1, 2} build J_Y = v/(1-v/s), solve u J_Y(u^2) = g_bar at R500 for the X-COP baryon profile, and report eta(s)
on both footings. DATA: `real_research/data/xcop` + `nbody_2026/stage30_xcop_two_variable_fit_2026.py` for the baryon numbers. PASS: some s
reproduces eta in [1.7, 2.1] AND s <= 0.219, so it also serves R1. KILL: the eta window needs s > 1, i.e. only the illegal kernel works. IMPACT:
would tie R4's fit and R1's gap to one number.

**I064 — Is there a MOND-free zone inside clusters?** HYP: if the local nu is large enough anywhere, a0 -> 0 there and the kernel is
exactly Newtonian -- a sharp radius the framework predicts and LCDM does not. USES: N3+N4+N7. DO: using I062's profile find the
radius (if any) where a0(r) < g_bar(r)/100, state it in kpc, state the matching |Q-Q_0|/Lambda_D = nu/sqrt(1+nu^2) so the distance
from N3's wall is explicit, and convert the Newtonian core into a fractional change in the X-ray hydrostatic mass M(<r) = -(kT r/(G
mu m_p))(dlnP/dlnr + dlnT/dlnr). Scan nu_0 in {2.36e-6, 1e-5, 1e-4, 1e-3}. DATA: analytic + `real_research/data/xcop`. PASS: such a
radius exists for some nu_0 <= 2.36e-6 with a stated X-ray signature > 5%. KILL: it requires nu_0 above the RAR ceiling -- report
the required nu_0. IMPACT: a spatially resolved R4 prediction unique to N2+N3.

**I065 — The Bullet cluster: a0 tracks the charge, not the gas.** HYP: because a0 is sourced by the dark charge, the enhanced-gravity region
follows the collisionless charge and therefore the galaxies, giving a lensing-gas offset without a particle. USES: N2+N4+N5. DO: on a 2-D grid
(512x512, 4 Mpc box) place two charge clumps of 1e14 M_sun separated by 720 kpc plus a central gas clump of 2e14 M_sun; compute nu(x) = nu_0
rho_charge(x)/rho_0 and a0(x) = a0(0)[(1+nu_0^2)/(1+nu^2)]^(1/4); solve g = sqrt(g_bar^2 + a0(x) g_bar) with g_bar from the GAS + galaxies;
integrate the convergence kappa_lens and locate its peaks. Note the sign: N4 SUPPRESSES a0 where the charge is dense, so state whether the peak
follows or ANTI-follows the charge. Scan nu_0 in {2.36e-6, 1e-4, 1e-2}. DATA: analytic toy model. PASS: convergence peaks sit on the charge
clumps with >100 kpc offset from the gas. KILL: peaks sit on the gas. IMPACT: would remove the most-cited anti-MOND datum from R4.

**I066 — Voids: a0 is at its CEILING where nothing lives. (S2)** HYP: N4 makes a0 maximal at rho -> 0, so voids are the most-MONDian
regions in the universe -- and by S2 they are also where the dark energy is least suppressed. USES: N4+N5+N2. DO: compute
a0(rho_void)/a0(0) for rho_void/rho_0 = 0.1 and 0.2, noting first that at nu_0 <= 2.36e-6 the effect is O(nu_0^2) ~ 1e-11; then
INVERT -- state the nu_0 that would give a 5% change in the void radial velocity profile v_r = -(1/3) H r f delta through nu(y), and
separately the nu_0 that would give a 1% change in the local (-K)/M^4 = 1/sqrt(1+nu^2); compare both to 2.36e-6. DATA: analytic.
PASS: either required nu_0 is below 2.36e-6, so voids are a live test. KILL: both above the ceiling -- record the bound as the
deliverable. IMPACT: converts a guaranteed null into a nu_0 bound and an S2 observable.

**I067 — Two competing environment effects that may cancel.** HYP: dense environments suppress a galaxy's internal a0 (N4) but ALSO impose an
external field suppressing the MOND boost -- they may add or partly cancel. USES: N1+N4+N6. DO: PRIOR: the direct environmental test is a
decisive NULL at 10.5 sigma on SPARC (`real_research/reviews/sparc_environmental_a0_test.py`) -- that null is the control this idea must explain,
not re-derive. For each SPARC galaxy compute g_ext from 2MRS and nu = nu_0 Sigma_bar/Sigma_0 from the same local density; predict the RAR
residual from each effect separately and from both, using the LEGAL kernel J_Y = v/(1-v/s) at s = 0.219 for the EFE part and nu_0 in {2.36e-6,
1e-4}. DATA: `real_research/data/2mrs_catalog.csv`, `real_research/data/sparc_a0_environment_table.csv`. PASS: opposite signs cancelling to <30%
of either. KILL: they add, turning the committed null into a tension. IMPACT: says whether that null was luck or structure.

## G. Empirical reanalyses

**I068 — a0-line vs legal family, head to head on the RAR.** HYP: U(2) = 0.449 for the a0-line and 0.369 for the legal s
= 1/2 family -- a 20% difference exactly where SPARC has the most points, so the data can tell them apart. USES:
N5+N6+N1. DO: fit both kernels to the RAR with Upsilon FREE on each side (never freeze it -- freezing Upsilon produced a
retraction in this corpus), a0 held at 9.3619e-11 and repeated at 1.1279e-10, and report rms dex and delta-BIC with the
parameter count stated. Fit the legal family at its best-fit s as well as at s = 1/2. DATA:
`ai_slop/website/public/data/rar_real_sparc.json`. PASS: delta-BIC > 10 favouring one kernel. KILL: |delta-BIC| < 2 --
degenerate, so R1's legality switch costs nothing empirically. IMPACT: settles the empirical price of N6.

**I069 — Does the RAR itself prefer a0 constant or a0(rho)?** HYP: N4 is a testable extra term in the RAR, not just a cosmological law. USES: N2+N4+N5. DO:
PRIOR: a0 proportional to sqrt(G rho_local) is EXCLUDED at 10.5 sigma on SPARC -- N4 is a DIFFERENT functional form (effect O(nu^2), saturating), so state that
difference explicitly or the referee will read this as the dead test. Fit (a) constant a0 and (b) a0 = a0(0)[(1+nu_0^2)/(1+nu^2)]^(1/4) with nu = nu_0
Sigma_bar/Sigma_0 -- Sigma_bar/Sigma_0 is a dimensionless PROXY for the dark-charge ratio N4 names, the substitution I080 adjudicates -- one extra parameter
nu_0 scanned over {1e-8 ... 1e-2}; compare BIC with Upsilon free in both. DATA: `ai_slop/website/public/data/rar_real_sparc.json` +
`real_research/data/sparc_master_clean.csv`. PASS: constant a0 preferred or tied (the promotion hides, as required). KILL: a0(rho) preferred at delta-BIC > 10
-- a major positive result. IMPACT: a first direct empirical handle on N2.

**I070 — The pre-registered SIGN of the RAR residual vs environment.** HYP: N4 predicts denser environments give LOWER a0 and so LOWER g_obs at fixed g_bar -- a
signed, falsifiable correlation. USES: N2+N4. DO: PRIOR: `real_research/reviews/project_sparc_a0_vs_density_direct.py` is already a NULL, so the deliverable
here is a BOUND, not a detection -- say so up front, and note that at nu_0 = 2.36e-6 the predicted slope is O(nu_0^2) and therefore unmeasurable by
construction. Bin SPARC galaxies into 4 quartiles of 2MRS local density, compute the mean RAR residual per bin with Upsilon free, fit the slope, test the
PRE-REGISTERED NEGATIVE sign, and convert the 2-sigma slope limit into a nu_0 ceiling via d ln g_obs/d ln a0. DATA: `real_research/data/2mrs_catalog.csv`,
`real_research/data/sparc_cosmicweb_match.csv`. PASS: slope consistent with zero and the implied nu_0 ceiling below 2.36e-6. KILL: a POSITIVE slope at > 3 sigma
-- wrong sign, falsifying N4's local reading. IMPACT: a sign test that can kill N4's local reading.

**I071 — Intrinsic RAR scatter as an independent ceiling on nu_0.** HYP: any spatial variation of a0 shows up as irreducible RAR scatter, so the
intrinsic-scatter floor bounds nu_0 without using environment data at all. USES: N4+N5+N1. DO: PRIOR: the RAR scatter as a quantitative upper
bound on a0 variation is SETTLED in `real_research/reviews/rar_tightness_intrinsic.py` -- read the committed intrinsic-scatter number from it
rather than re-deriving the decomposition; the NEW work is only the conversion. Convert that intrinsic ceiling into a bound on nu_0 using d ln
a0/d ln rho = -(1/2) nu^2/(1+nu^2) and the SPARC spread in Sigma_bar/Sigma_0, and quote the result on both footings. DATA: that script +
`ai_slop/website/public/data/rar_real_sparc.json`. PASS: the derived ceiling is within 3x of 2.36e-6. KILL: it is 10x tighter (the RAR bound was
too weak) or 10x looser. IMPACT: a second, independent route to N4's only free small parameter.

**I072 — Is g_obs^2 - g_bar^2 really LINEAR in g_bar?** HYP: N5 asserts the exact power 1; the legal family J_Y = v/(1-v/s) does not, so the
measured exponent discriminates the two kernels with no a0 normalisation needed. USES: N5+N6. DO: PRIOR: the a0-line fitted to data generated at
known a0 is UNBIASED on alpha=1 data but biased +10.3% on Route-A data and -83.6% on alpha=2 data -- so run that same injection test as your
calibration before touching real data. Take SPARC galaxies with f_gas > 0.7, fit log(g_obs^2 - g_bar^2) = log A + p log g_bar by total least
squares with errors on both axes, report p +/- sigma, and compute the p the legal family predicts at s = 0.219 and 0.5 over the SAME g_bar range.
DATA: `real_research/data/SPARC_Lelli2016c.mrt`. PASS: p = 1 within 2 sigma AND the family's p excluded at > 2 sigma. KILL: p differs from 1 by >
3 sigma. IMPACT: tests N5's functional form, not just its scale.

**I073 — Measure the saturation constant s directly from high-y SPARC.** HYP: R1 assumes s is whatever the RAR needs (0.219 canonical / 0.173
alt); the highest-y points measure U(y) where it should already be flattening, so s can be read off. USES: N6+N5+N1. DO: PRIOR: only 5.2% of
SPARC points reach g_bar/a0 > 10 and the sample TOPS OUT at y = 110, against Earth's y = 6.33e7 -- state this lever-arm limit before quoting any
s, or the result is an extrapolation dressed as a measurement. Take points with y > 10, form U = g_obs/a0 - y, bin in log y with >= 30 points per
bin, and fit U(y) = s(1 - c/y) reporting s +/- sigma and whether dU/dy is still positive at the top bin. Both footings. DATA:
`qwen_38_experiment/data/rar_sparc_a0units.json`. PASS: s measured with sigma < 0.05 anywhere in [0.1, 0.6]. KILL: U still rising with no plateau
-- saturation is not observed at all in the data. IMPACT: turns R1's numerator into a measurement.

**I074 — Ultra-diffuse galaxies: the promotion predicts a HIGHER a0 there.** HYP: UDGs sit in low-density environments with low internal density, so N4 gives
them a0 nearer the ceiling than spirals -- a specific, signed offset in their RAR. USES: N1+N4+N5. DO: compute delta ln a0 = (1/4)[ln(1+nu_spiral^2) -
ln(1+nu_UDG^2)] with nu = nu_0 rho/rho_0 evaluated at ABSOLUTE contrasts rho_spiral/rho_0 = 1e6 and rho_UDG/rho_0 = 1e4 and 1e5 -- the effect is second order in
nu, so the absolute contrasts and not their ratio decide its size; translate to a shift in log g_obs at fixed g_bar in dex via d ln g_obs/d ln a0 = (1/2) a0
g_bar/(g_bar^2 + a0 g_bar) evaluated at y = 0.3 (the UDG regime); then invert for the nu_0 that reaches 0.05 dex at those contrasts and compare it with the cap
2.36e-6. DATA: DATA WE DO NOT HAVE -- there is no committed UDG rotation table; give the analytic prediction and the measurement precision it would need. PASS:
the shift exceeds 0.05 dex at some nu_0 <= 2.36e-6. KILL: below 0.01 dex throughout. IMPACT: names the sample where N2 is maximally visible.

**I075 — Dwarf spheroidals: which density drives a0 decides the sign.** HYP: dSphs have the LOWEST baryon density and among the HIGHEST
dark-charge contrasts, so N4's baryon reading BOOSTS a0 while its dark-charge reading SUPPRESSES it -- opposite offsets, with the EFE on top.
USES: N1+N4+N6. DO: PRIOR: the dSph closure test is SYSTEMATICS-limited, not sample-limited (per-object scatter 0.38-0.48 dex, the dominant
Upsilon_V error is COHERENT so sqrt(N) does not help) -- so do NOT claim a discrimination from N; report per-object numbers. For the classical
dSphs compute nu under BOTH readings, g_ext from the Milky Way at each distance, predict sigma_v with J_Y = v/(1-v/s) at s = 0.219, and compare
to observed sigma_v. DATA: `real_research/data/dsph` + `real_research/reviews/mi_dsph_closure_test_real_data_2026.py`. PASS: one reading fits >=
6 dwarfs within 30% while the other misses > 2x. KILL: both miss by > 2x. IMPACT: the hardest small-scale test decides N4's density fork.

**I076 — BTFR scatter as a nu_0 meter.** HYP: V^4 = G M a0 means a0 scatter enters the BTFR zero point at power 1/4, so the observed BTFR scatter
caps nu_0 independently of the RAR. USES: N1+N4+N5. DO: PRIOR: the BTFR coefficient is exactly 1 as a THEOREM of the convex field theory --
assume it, do not fit it. Propagate the fractional a0 spread implied by N4 across the SPARC environment range (delta ln a0 = (1/4) delta
ln[(1+nu^2)]) into a BTFR zero-point spread in dex (one quarter of delta log a0), compare to the measured BTFR scatter (report the value you use
and its source), and solve for the nu_0 at which the two become equal. DATA: `real_research/data/sparc_master_clean.csv` +
`real_research/data/sparc_a0_environment_table.csv`. PASS: the implied nu_0 ceiling beats 2.36e-6. KILL: the BTFR is too scattered to constrain
nu_0 -- quote the ceiling anyway. IMPACT: a third independent bound on N4's free parameter.

**I077 — Full rotation-curve fits as an s-meter, not the RAR.** HYP: the RAR averages away the radial shape; fitting whole curves with the legal
family constrains s better because s controls the inner (high-y) rise. USES: N6+N5+N1. DO: fit 20 high-quality SPARC curves (quality flag 1, i >
30 deg) with J_Y = v/(1-v/s), Upsilon_disk and s free per galaxy and a0 held at 9.3619e-11 (repeat at 1.1279e-10); solve u J_Y(u^2) = g_bar for u
at each radius; combine the per-galaxy s posteriors into a global s by inverse-variance weighting, and report the chi^2 penalty relative to the
a0-line kernel on the same curves. DATA: `real_research/data/sparc_data` + `real_research/data/SPARC_Lelli2016c.mrt`. PARTIAL EXPECTED: 20
galaxies may not finish; report however many converge, with the count. PASS: global s determined with sigma < 0.05 and inconsistent with 0.219 at
> 3 sigma. KILL: s unconstrained per galaxy. IMPACT: measures R1's numerator from curve shapes rather than from a binned relation.

**I078 — Is there room for a constant s*a0 sunward in current residuals?** HYP: the legal class's anomaly is CONSTANT in r -- unlike I004's radially varying
form -- so it is not degenerate with a 1/r^2 GM error: its precession contribution grows steeply with orbital radius. USES: N1+N6. DO: PRIOR: the committed
bounds are Sereno-Jetzer 2006 Tab.1 (Pitjeva EPM2004) inverted through their own Eq.(9): dA_R <= 3.66e-14 m/s^2 (Earth, 2 sigma) and 3.72e-14 (Mars); and the
Fienga+2009 global-refit escape (~200x looser) does NOT reach, being outer-planet limits. Compute the perihelion precession induced by a constant radial
acceleration A: dvarpi/dt = -2 pi A a^2 sqrt(1-e^2)/(GM_sun e) per orbit for Mercury, Venus, Earth, Mars; fit s jointly with a dGM_sun offset; report the
MARGINALISED 2-sigma bound on s on both footings. DATA: `real_research/reviews/mi_alpha1_solar_system_2026.py`. PASS: the marginalised bound exceeds 1e-4 (the
gap shrinks > 8x). KILL: stays below 2e-5. IMPACT: directly attacks R1's denominator.

**I079 — Lunar laser ranging: the anomaly is constant, so its LLR signature is peculiar.** HYP: a constant sunward s*a0 acts as a
common-mode force on Earth and Moon and cancels to leading order, leaving only a tidal residual -- LLR may be far weaker than
assumed. USES: N6+N1. DO: for a constant field A r-hat centred on the Sun, the Earth-Moon differential acceleration is delta a = A
(d/R_1AU) with d = 3.84e8 m and R_1AU = 1.496e11 m, i.e. suppressed by 2.57e-3; compute delta a for A = s*a0 at s = 1.27e-5, 1e-3,
0.173, 0.219 on both footings; integrate over the synodic period 29.53 d to a range amplitude in mm using delta r ~ delta a T^2/(4
pi^2). DATA: analytic. PASS: the predicted signal is below the ~1 mm LLR floor for s ~ 0.2. KILL: above 1 cm at s = 0.219. IMPACT:
could remove LLR from R1's constraint list entirely -- or add it.

**I080 — Does the framework's own a0 suppression protect it from pulsar bounds?** HYP: in a binary pulsar the local charge density is huge, so N4 drives a0 -> 0
and the framework predicts NO deviation there -- or the suppression is a fiction because rho is the DARK charge, not the baryon density. USES: N4+N2+N6. DO:
this idea ADJUDICATES the substitution every other N4 idea makes. State both readings; compute a0/a0(0) = [(1+nu_0^2)/(1+nu^2)]^(1/4) at (a) a neutron-star
baryon density 5e17 kg/m^3 and (b) the ambient galactic dark-charge density (rho = Q_0 n at both ends of the pin), for nu_0 in {2.36e-6, 1e-4}; report the two
answers side by side and their ratio. Then say which reading the Q equation's source term lambda_c rho actually couples to. DATA: analytic +
`real_research/bridge1_aest_equations.md` for the source coupling. PASS: the two readings differ by > 100x, so the choice is decidable and matters. KILL: they
agree within 2x. IMPACT: forces the framework to say WHICH density drives a0.

## H. Reframings, alternative homes, and legality RE-DERIVED with a0 a FIELD (S4)

**I081 — The halo profile the a0-line implies, versus the halo the DBI dust makes.** HYP: if the a0-line is recast as an equivalent
dark density, that profile must match what the beta=1 brane's pressureless excitation actually produces -- and R2 says it collapses
instead. USES: N5+N3+N2. DO: invert g_obs^2 = g_bar^2 + a0 g_bar for a point baryon M into rho_eff(r) = (1/4 pi G r^2) d/dr [r^2
(g_obs - g_bar)] with g_bar = GM/r^2, and get the analytic slope d ln rho_eff/d ln r in the deep regime (expect -1 by hand --
verify); compare with the collapsing dust profile from `nbody_2026/stage2_spherical_collapse_2026.py` over r = 1-300 kpc at both
footings. DATA: analytic + that stage. PASS: slopes agree within 0.2 over a decade in r -- the dust IS the a0-line. KILL: they
differ by more than a full power of r. IMPACT: would unify N5's phenomenology with R2's dust, or prove they conflict.

**I082 — Does the legality obstruction apply to TeVeS as well as AeST?** HYP: N6's single-valuedness of F(Y,Q) is an AeST-specific
requirement; TeVeS's free function may admit the a0-line's U legally. USES: N6+N5+N2. DO: TeVeS's scalar action is (1/2) sigma^2
h^ab phi_,a phi_,b + (1/4) G l^-2 sigma^4 F(k G sigma^2); write its quasi-static field equation in the SAME variables (v =
sqrt(Y)/a0, U = (nu-1) y), derive the condition for mu(sigma) to be single-valued, and test U = sqrt(y^2+y) - y against it at y =
0.1, 1, 2, 10, 1e3, 6.33e7. Then ask whether TeVeS can host N2 at all -- a home that escapes N6 but cannot carry a0^2 = kappa^2
G(-K) is not a home; say so in the verdict. DATA: analytic (sympy). PASS: the a0-line is legal in TeVeS AND the promotion embeds.
KILL: the same obstruction appears, or the promotion has nowhere to live. IMPACT: a legal home for N5 would dissolve R1 at a stroke.

**I083 — Does promoting a0 to a field supply the missing PPN limit?** HYP: R5's aether sits at c_123 = 0 where the standard preferred-frame parameters are
undefined; a dynamical a0 adds a scalar channel that may regulate them. USES: N2+N3+N6. DO: PRIOR: the highest-value open PPN item is exactly alpha_1, alpha_2
for the FULL theory with the SCALAR RETAINED, and it turns on ONE number -- whether the LOCAL spin-0 speed exceeds w_sun = 1.234e-3 c (SZ21 Eq.30's c_s is
COSMOLOGICAL, not local). Also: alpha_1 = -4K_B and K_B < 2.5e-5 are both WITHDRAWN; in force is K_B in [2.1e-4, 0.25]. Add the brane's scalar perturbation
(mass^2 = M^4/(Z Lambda_D^2)) to the PPN expansion at c_123 = 0, compute the local spin-0 speed, and compare it to 1.234e-3 c. DATA:
`nbody_2026/stage70_ppn_preferred_frame_2026.py`, `nbody_2026/stage74_ppn_fork_adjudicated_2026.py`. PARTIAL EXPECTED: the local c_s number alone counts as
delivered. PASS: alpha_1, alpha_2 finite and inside experimental bounds. KILL: still singular. IMPACT: closes R5, the quietest structural hole.

**I084 — Redo single-valuedness with a0 INSIDE F(Y,Q). (S4, load-bearing)** HYP: the monotonicity requirement behind R1 was derived treating a0 as a constant; but F(Y,Q) contains
a0(Q), so dF/dY = J_Y(sqrt(Y)/a0(Q)) and the single-valuedness condition acquires a chain-rule term -(v/a0) J_Yv (da0/dQ) that was never there. USES: N2+N3+N6. DO: with sympy write
F(Y,Q) = integral J_Y(sqrt(Y)/a0(Q)) dY with a0(Q)^2 = kappa^2 G M^4 sqrt(1-(Q-Q_0)^2/Lambda_D^2); compute the FULL Hessian condition for F to be a single-valued function of (Y,Q)
-- i.e. that (J_Y, F_Q) is a closed 1-form AND that the map Y -> F_Y is injective at each Q -- and print which of the two conditions the constant-a0 derivation dropped. Evaluate
the dropped term's size at x = (Q-Q_0)/Lambda_D in {0, 0.1, 0.5, 0.9} for s in {1.27e-5, 0.219}. DATA: analytic (sympy) +
`real_research/reviews/typeII_legality_independent_2026.py` for the constant-a0 baseline. PASS: the dropped term is nonzero and changes the condition. KILL: it vanishes identically
-- R1 is confirmed at a deeper level. IMPACT: either the 233x obstruction dissolves at its root, or it hardens.

**I085 — Monotone in y, or monotone in g_bar? (S4)** HYP: the legality theorem is stated as "U(y) strictly increasing" with y = g_bar/a0; but
when a0 is a field, y and g_bar are different variables, and physical single-valuedness is a statement about the map g_bar -> g_obs, not about
U(y). USES: N2+N4+N6. DO: define G(g_bar) = g_obs(g_bar) with a0 = a0(nu(rho(g_bar))) and rho = g_bar/(4 pi G r) for a point mass; compute
dG/dg_bar = (dU/dy)(dy/dg_bar) a0 + U (da0/dg_bar) with da0/dg_bar = -a0 nu^2/(2(1+nu^2) g_bar); show the second term is NEGATIVE and find the
condition on nu for dG/dg_bar to stay positive; scan nu in {1e-6, 1e-3, 1, 10, 1e3}. Report whether a U that is non-monotone in y can still give
a G monotone in g_bar. DATA: analytic (sympy). PASS: the two monotonicity conditions are inequivalent and the g_bar one is weaker. KILL: they are
equivalent for every nu -- the theorem survives the promotion. IMPACT: identifies which variable R1's theorem is actually about.

**I086 — S2's structural ceiling: the deficit is large only where Lambda is irrelevant.** HYP: the dark-energy deficit 1 - [(1+nu_0^2)/(1+nu^2)] needs nu ~ 1, i.e. rho/rho_0 ~ 4e5,
while Lambda's share of the local dynamics falls as rho_Lambda/rho -- so every S2 observable is bounded by the PRODUCT of the two, a ceiling nobody has computed. USES: N1+N2+N4.
DO: form P(rho) = f_def(rho) x [rho_Lambda/rho] with f_def = 1 - [(1+nu_0^2)/(1+(nu_0 rho/rho_0)^2)] and rho_Lambda = 6.0e-27 kg/m^3 (state the footing: recompute it from a0 =
kappa c sqrt(G rho_Lambda) on both); scan rho/rho_0 logarithmically from 0.1 to 1e8 at nu_0 in {2.36e-6, 2.14e-5, 1.77e-4}; report P_max, the rho/rho_0 attaining it, and the object
class that sits there (void, wall, halo, disc, cluster core). DATA: analytic. PASS: P_max > 1e-3 at any allowed nu_0 -- name the object class as S2's best target and hand the
number to I057, I436, I438 and I440 as their ceiling. KILL: P_max < 1e-6 everywhere -- then every S2 observable is null by construction at the cap, and the ceiling itself is the
deliverable; record it so S2 ideas are graded against it. IMPACT: fixes the ceiling on every S2 observable at once.

**I087 — Build a LEGAL coupled system whose APPARENT U is non-monotone. (S4)** HYP: an observer measures U from (g_bar, g_obs) pairs assuming one constant a0;
if the underlying (Y,Q) system is perfectly legal but a0 slides with the source, the RECONSTRUCTED U can be non-monotone -- so the a0-line's shape need not
indicate illegality at all. USES: N2+N4+N6. DO: take the legal J_Y = v/(1-v/s) at s = 1.27e-5 (the ephemeris-allowed value), let a0 =
a0(0)[(1+nu_0^2)/(1+nu^2)]^(1/4) with nu = nu_0 rho/rho_0 and rho = g_bar/(4 pi G r) for a point mass; generate (g_bar, g_obs) over y_apparent = g_bar/a0(0) in
[1e-2, 1e8]; then RECONSTRUCT U_app(y_app) = g_obs/a0(0) - y_app assuming constant a0 and test dU_app/dy_app for sign changes. Scan nu_0 in {1e-6, 2.36e-6,
1e-4, 1e-2}. DATA: analytic. PASS: U_app is non-monotone somewhere while the underlying system is legal -- then "the a0-line is illegal" is an artefact of
assuming constant a0. KILL: U_app is monotone for every nu_0. IMPACT: could reclassify R1 as a measurement artefact rather than a theorem.

**I088 — The promotion predicts kappa is NOT universal -- by a computable amount.** HYP: a per-galaxy fitted kappa varies as gamma^(-1/2), so
kappa scatter is a prediction, not noise. USES: N1+N4+N5. DO: derive d ln a0/d ln rho = -(1/2) nu^2/(1+nu^2) -- it is -1/2 only for nu >> 1 and
goes to ZERO like nu^2/2 for nu << 1, so at nu_0 <= 2.36e-6 the slope is essentially zero, NOT the -1/4 sometimes quoted; state the predicted
slope explicitly at nu_0 in {2.36e-6, 1e-4, 1e-2}. Then fit kappa per SPARC galaxy at a fixed Upsilon prior (0.5 +/- 0.1 dex) and regress log
kappa on log mean baryonic surface density (a stated proxy for rho); compare the fitted slope to the derived one. DATA:
`real_research/data/SPARC_Lelli2016c.mrt` + `ai_slop/website/public/data/rar_real_sparc.json`. PASS: the fitted slope matches the derived one
within 2 sigma. KILL: a nonzero slope at > 3 sigma where the theory predicts ~0. IMPACT: makes R3's kappa scatter a measurement of N4's nu_0.

**I089 — Which footing survives once a0 is a field?** HYP: the rho_DE/cH_Lambda footing gives a0(0) = 9.3619e-11 and rho_total/cH_0 gives
1.1279e-10, but under N2 only the DE piece can be the brane's -K, so the promotion may pick a footing the phenomenology cannot. USES: N1+N2+N3.
DO: write M^4 = rho_Lambda c^2 explicitly and check that kappa^2 G(-K) at the minimum reproduces a0 = kappa c sqrt(G rho_Lambda) with correct
units (G x energy density has units of acceleration^2 -- verify the exponents in [m, kg, s]); then attempt the substitution M^4 -> rho_total c^2
and check whether w = -1 at the minimum survives it (it should not, because rho_total is not constant) -- quantify max|w+1| over 0 < z < 2 under
the substitution. DATA: analytic (sympy). PASS: the promotion admits only the canonical footing, with max|w+1| > 0.1 on the alt. KILL: both work
-- then the fork stays a fit choice. IMPACT: would settle the framework's oldest fork on structural, not fit, grounds.

**I090 — Local density or formation epoch? Two readings of the same law.** HYP: a0(nu) can be read as depending on the LOCAL charge density or on
the cosmic density at the galaxy's formation epoch; these give different, testable SPARC predictions. USES: N4+N2+N5. DO: build predictor (a) nu
= nu_0 Sigma_bar/Sigma_0 from the SPARC mean baryonic surface density, and predictor (b) nu = nu_0 (1+z_f)^3 with z_f estimated per galaxy from
the concentration or the gas fraction (state the proxy and its scatter); fit each to the RAR with Upsilon FREE and nu_0 scanned over {1e-8 ...
1e-2}; compare BIC. PRIOR: I038 decides this on theory grounds via the a0 relaxation time -- if tau > 13.8 Gyr, reading (b) is forced; state
which way I038 would go if you can. DATA: `ai_slop/website/public/data/rar_real_sparc.json` + `real_research/data/sparc_master_clean.csv`. PASS:
one reading preferred at delta-BIC > 10. KILL: indistinguishable. IMPACT: fixes what N4's density argument actually means.

**I091 — Is DBI necessary, or would any bounded K do?** HYP: three properties are claimed for the beta=1 DBI -- w = -1 at the minimum, dust for
small excitations, and a wall where -K -> 0. Test whether these single out DBI. USES: N2+N3+N7. DO: with sympy take K = -M^4 (1-x^2)^p for p =
1/4, 1/2, 1 and K = -M^4 exp(-x^2), x = (Q-Q_0)/Lambda_D; for each DERIVE rho = Q K_Q - K from the same Lagrangian rather than assuming the DBI
answer (for the EXPONENT p = 1/2 the answers are rho = M^4 gamma and PRESSURE P = -M^4/gamma, hence w = -1/gamma^2 -- use that as your check, and
do not confuse the exponent p with the pressure P); report w at x = 0, the small-x equation of state, whether -K -> 0 at finite x, and the
resulting a0(x) = kappa sqrt(G(-K)) law. DATA: analytic (sympy). PASS: only p = 1/2 satisfies all three. KILL: another form does too -- name it,
because then N3 is an assumption not a result. IMPACT: derives the brane form or demotes it.

**I092 — Map the allowed brane exponent from the recombination off-switch plus the RAR.** HYP: the DBI power is selected, not
derived; the a0(z) off-switch (I051) and the RAR nu_0 ceiling together bound it. USES: N3+N4+N7. DO: generalise to K = -M^4
(1-x^2)^p -- call it p, NOT beta, which I029 uses for mu^2 Lambda_D^2/M^4 -- derive a0 proportional to (1+nu^2)^(-p/2) via x =
nu/sqrt(1+nu^2), then scan p over {0.1, 0.25, 0.5, 1, 2, 4} and find which p keep a0(z=1090)/a0(0) < 0.05 at nu_0 = 2.36e-6 while
leaving the RAR fit at < 0.12 dex with Upsilon free. DATA: analytic + `ai_slop/website/public/data/rar_real_sparc.json`. PASS: p =
1/2 sits inside a window less than a factor 2 wide. KILL: a wide range of p works equally -- report the width, since that is the
honest measure of how much N3 is doing. IMPACT: converts a chosen exponent into a bounded one.

**I093 — A second, independent pin on Q_0 from the dust amount.** HYP: rho = Q_0 n ties the charge scale to the dark-matter density, giving a Q_0
independent of the growth/forest pin at 0.0024-0.0146 Mpc^-1. USES: N2+N3+N7. DO: set the EXCITATION density rho_dust = M^4(gamma-1) -- NOT the
value at the minimum, which is rho_Lambda c^2 -- equal to Omega_dm rho_crit c^2 = 0.26 x 8.53e-10 J m^-3; solve for gamma, hence nu, hence x =
nu/sqrt(1+nu^2); then use rho = Q_0 n with M^4 = rho_Lambda c^2 to solve for Q_0 and convert to Mpc^-1, stating the unit conversion for every
factor (Q_0 is mass-dimension 1 in natural units; give the SI bridge explicitly). DATA: analytic (sympy). PASS: the derived Q_0 falls inside
0.0024-0.0146 Mpc^-1. KILL: it lands outside by more than 3x -- an internal inconsistency between N3's two roles, worth reporting loudly. IMPACT:
tests the brane's dark-energy and dark-matter roles against each other.

**I094 — If S4 holds, what number replaces 13,600-17,300x? (S4)** HYP: the s-gap was computed with a single constant a0 on both ends; with a0 a field the numerator (RAR-required U
at y ~ 2) and the denominator (perihelion-allowed U at y ~ 6.33e7) are evaluated at DIFFERENT a0, so the ratio is not 0.219/1.27e-5. USES: N2+N4+N6. DO: define the gap honestly as
Gap = U_req(y_gal; a0_gal)/U_allow(y_sun; a0_sun) where a0_gal = a0(nu(rho_gal)) and a0_sun = a0(nu(rho_sun)); recompute U_req from the RAR bin y in [1.8, 2.2] and U_allow from
dA_R <= 3.66e-14 m/s^2 divided by a0_sun; tabulate Gap on the grid rho_sun/rho_0 in {1e2, 1e4, 4.24e5, 1e6, 1e8} times nu_0 in {2.36e-6, 1e-5, 1e-4, 1e-3}, both footings; state the
minimum Gap and the cell attaining it. DATA: `ai_slop/website/public/data/rar_real_sparc.json` + `real_research/reviews/mi_alpha1_solar_system_2026.py`. PASS: min Gap < 100 inside
the allowed nu_0. KILL: min Gap > 5000 everywhere -- then R1's number is robust to the promotion and should be restated as such. IMPACT: replaces R1's headline number with a
promotion-aware one, either way.

**I095 — Is the dust amplitude an integration constant, or fixed by the wall?** HYP: Omega_dm is claimed free, but if the wall |Q-Q_0| = Lambda_D
imposes a boundary condition the amplitude may be fixed instead. USES: N3+N7+N2. DO: solve the homogeneous Q equation Q'' + 3H Q' + dK/dQ / Z = 0
for the beta=1 brane on an LCDM background from z = 1e6 to 0; count its integration constants; then require |Q(z) - Q_0| < Lambda_D for the WHOLE
history and read off the allowed initial amplitude; convert to Omega_dm via rho_dust = M^4(gamma-1) and quote the allowed Omega_dm range at both
ends of the Q_0 pin and for Lambda_D/Q_0 in {1e-9, 1e-7, 3.1e-6}. DATA: analytic + numerical ODE. PASS: the allowed range excludes Omega_dm
values differing from 0.26 by more than 2x. KILL: any Omega_dm is allowed -- confirms the non-claim, which is worth confirming. IMPACT: would
upgrade a fitted cosmological parameter to a derived one.

**I096 — Which dimensional combinations for a0 can be PROMOTED to a field?** HYP: many combinations of {c, G, rho_Lambda, H_0, Lambda} give an acceleration, but
only those built from a dynamical energy density can satisfy a0^2 = kappa^2 G(-K) -- the promotion is a filter the coincidence enumeration never applied. USES:
N1+N2+N3. DO: PRIOR: the category search already proved a0 = xi c sqrt(G rho) is UNIQUE at determinant 2 -- start from
`real_research/uniqueness_dimensional_proof.py` + `real_research/reviews/mi_third_category_search_2026.py` -- read it, do not re-derive it. Enumerate all
products c^a G^b rho_Lambda^c H_0^d Lambda^e with integer/half-integer exponents in [-2, 2] landing within 20% of 9.36e-11 m s^-2; then strike out every one
whose ingredients are not a LAGRANGIAN energy density that can vary in space (H_0 and Lambda are not). DATA: analytic. PASS: 2 or fewer survive the promotion
filter. KILL: more than 5 survive. IMPACT: makes the a0-Lambda coincidence structurally forced rather than numerological.

**I097 — After the promotion, what coincidence is actually left?** HYP: N2 explains why a0 tracks the dark energy, so the only residual puzzle is why kappa is O(1) -- quantify how
much of the original coincidence the promotion has already discharged. USES: N2+N1+N3. DO: PRIOR: the "simplicity" argument for kappa = 1/2 is RETRACTED as stated -- at +/-7.8%
precision all five natural parameterisations admit a simple rational, and 5/9 (0.11 sigma) and 4/7 (0.48 sigma) sit CLOSER than 1/2 (1.19 sigma); the only defensible statement is
Bayesian, ~6:1 under a 1/q^2 prior. Do not re-derive that. NEW work: state a prior over kappa implied by the BRANE construction (e.g. kappa^2 = the ratio of brane tension M^4 to
the kinetic normalisation Z, with Z's natural range), and compute P(|kappa - 0.529| < 0.034) under it, plus the number of orders of magnitude the promotion removed from the
original a0-vs-Lambda coincidence. DATA: analytic. PASS: the residual coincidence is under 1 order of magnitude. KILL: the prior is unstatable -- say so plainly rather than
inventing one. IMPACT: reframes R3 from "derive kappa" to "explain one O(1) number".

**I098 — Every prediction where a FIELD a0 differs from a CONSTANT a0.** HYP: the promotion, not the a0 value, is what separates this framework from both LCDM
and standard MOND. USES: N2+N4+N5. DO: list ONLY predictions that follow from a0 being a field -- environment dependence of the RAR zero point, the falling
a0(z), cluster-core suppression, void enhancement, per-galaxy kappa scatter, the a0 relaxation time, the local dark-energy deficit -- and give each (i) the
predicted effect size at nu_0 = 2.36e-6 AND at nu_0 = 1e-4, (ii) the current observational error on that quantity with its source, (iii) the ratio. No entry
without all three numbers. Both footings where dimensionful. DATA: analytic, drawing on the committed numbers in `nbody_2026/stage75_the_closed_theory_2026.py`.
PASS: at least one entry where the predicted effect exceeds the current error at nu_0 <= 2.36e-6. KILL: all below current sensitivity -- also decisive, and the
ranking is still the deliverable. IMPACT: defines the observational programme that is unique to N2.

**I099 — Rank the promotion's tests by discriminating power per unit cost.** HYP: the cheapest decisive test of the framework is a
test of N2/N4, not of a0's value. USES: N2+N4+N6. DO: take I098's numbered list plus the s-measurement routes (I073 high-y SPARC,
I077 curve fits, I078 ephemeris, I014 DR4 gamma_v) and rank by (predicted effect / current error) divided by a stated cost tier: 1 =
archival reanalysis of a file already in this repo, 3 = new reduction of public data, 10 = a proposal for new observations. Give the
top three a one-line method and a named dataset. DATA: analytic, drawing on the committed numbers. PASS: a ranked table with the top
three costed and each carrying a number. KILL: n/a -- this one always produces output. IMPACT: tells Carl which single measurement
to chase next against R1 and N2.

**I100 — The honest one-page standing, organised by N1-N7 and R1-R5.** HYP: n/a. USES: N1+N2+N3+N4+N5+N6+N7 (all). DO:
read `RETRACTIONS.md` and `nbody_2026/stage75_the_closed_theory_2026.py`, then write one page with four headings -- what
passes, what fails, what is open, what is genuinely novel -- and for each of R1-R5 give the current best number WITH its
footing and the single idea in this file most likely to move it. Quote the in-force values, not superseded ones: gamma_v
band 1.1614-1.1814 / 1.1917-1.2267 (Amendment 10), eta(R500) 1.865/1.722 on MS08, kappa 0.529 +/- 0.034, s-gap
13,600-17,300x, K_B in [2.1e-4, 0.25]. No new computation. DATA: the two files named. PASS: n/a -- this one always
produces output. KILL: n/a. IMPACT: keeps the ledger honest in both directions, as STANDING rule 5 requires.
