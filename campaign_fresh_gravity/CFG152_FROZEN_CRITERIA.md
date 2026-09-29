# CFG152 — referee of CFG124 (door 10, mimetic gravity): the perturbation sound speed and the ghost window. FROZEN CRITERIA

Written 2026-09-29, stage 1, before any script or number of this lane. This lane re-derives ONE headline of CFG124 the CFG84-86 way: with my own derivation and code, working only from CFG124's frozen criteria (`CFG124_FROZEN_CRITERIA.md`) and README (`CFG124_door10_mimetic/README.md`).
- The shared gates are those of `closure_map/TEN_DOORS_GATES_2026-09-29.md`. The line re-derived here is G5 (no ghost, no gradient instability), plus one secondary G1.2 row.
- The headline was known before this file was written: it is in the request, in CFG124's README and in the literature read below. So this is a check of a stated result, not a blind prediction.
- Nothing below may change after a result is seen. Any later deviation goes in the README as a disclosed departure.

## The headline under test (pinned from CFG124's README, verbatim)

- "**G5:** T0.6 derives c_s^2 = gt/(2 - 3 gt) (the recalled value, recomputed) with a **ghost** (negative kinetic term) for every 0 < gt < 2/3, and gradient instability for gt < 0 or gt > 2/3: no stable healthy gt exists"
- "Normalisation (the frozen text under-specified it): gamma is measured in units of M_P^2, gt = 8 pi G gamma."
- Related lines:
  - "the frozen G5 implied a healthy stable window 0 < gt < 1/2; it is a ghost";
  - "class A is frozen by the momentum constraint (no ghost, no instability)";
  - the method: "the scalar and tensor sector of the reduced ADM action (unitary gauge)".

## Definitions (CFG124's, adopted unchanged)

- **The action** is CFG124's frozen section (b), in signature (-,+,+,+) with c = 1:
  S = INT d^4x sqrt(-g) [ R/(16 pi G) + lambda (g^{mu nu} d_mu phi d_nu phi + 1) - V(phi) + (gamma/2) (box phi)^2 ]
  - lambda is a Lagrange multiplier and box phi = nabla_mu nabla^mu phi.
  - The baryons (S_b) are left out, because the headline is a property of the mimetic sector.
- **gt is ONE dimensionless number:** gt = 8 pi G gamma = gamma / M_P^2, with M_P^2 = 1/(8 pi G) (the reduced Planck mass squared, hbar = c = 1).
  - It is not a product of a "g" and a "t". The request's "(g, t) points" are read here as values of gt.
- **Units.** With c = 1 the constraint makes phi a proper time. So [box phi] = 1/length and [gamma] = [1/G], and gt needs no hbar.
- **Sign.** gt > 0 means the (box phi)^2 term enters with the sign written above, next to +R/(16 pi G).
  - (box phi)^2 does not change when the signature flips. So gt > 0 is the same sign as gamma > 0 in CMV 2014 and as f_chichi > 0 in FGM 2017 (both below).
- **Backgrounds** (phi_bar = t in both):
  - **Minkowski**, with V = 0 and lambda_bar = 0. This is empty mimetic dust, an exact solution; the script checks it through the first-order terms.
  - **Flat FRW** with an arbitrary a(t), with V(t) and lambda_bar(t) set by the background equations. This includes CFG124's LCDM-like background (V = const, with the dust amount as the integration constant).
- **Ghost:** after all constraints are solved, the kinetic coefficient K of the one propagating scalar is negative (the mode's energy is negative).
- **Gradient instability:** K > 0 and c_s^2 < 0.

## Method (declared)

**M1: primary, Minkowski, exact in k.**
- **Metric:**
  - g_00 = -(1 + 2 Phi) and g_0x = d_x B;
  - g_xx = 1 - 2 Psi + 2 d_x^2 E;
  - g_yy = 1 - 2 Psi + h and g_zz = 1 - 2 Psi - h;
  - phi = t + dphi and lambda = dlambda.
  - All seven fields depend on (t, x) only. h is one tensor polarisation, kept as a control.
- **Expansion.** sqrt(-g) times the Lagrangian is expanded to second order by brute force from the 4-metric: the inverse metric, the Christoffel symbols, the Ricci scalar, and box phi from its covariant definition.
  - No ADM split, no unitary-gauge or Horava shortcut, and no linearised Einstein-Hilbert formula from memory.
- **Fourier form.** Plane waves exp(i(k x - omega t)) turn the second-order Lagrangian into a Hermitian matrix M(omega, k) in the field amplitudes. Total derivatives drop out identically.
- **Step (i), gauge.** The two scalar gauge vectors are computed from the Lie derivative of the background, not typed in. They must be null vectors of M for all omega, k and gt.
- **Step (ii), dispersion.** det M is restricted to two different complete gauges: unitary (dphi = E = 0) and Newtonian (B = E = 0). The nonzero roots in omega must agree between the two; zero roots are reported with their multiplicity.
- **Step (iii), reduction.** In unitary gauge, dlambda, Phi and B are eliminated by their own equations (a Schur complement). What is left must be one field, with M_red = K (omega^2 - c_s^2 k^2) times a positive function of k.
- **Step (iv), gauge-invariant sign.** At a real root omega0, take the sign of omega0 v^dagger (dM/domega) v on the null space of the full, not gauge-fixed, M(omega0, k). This is a Krein signature, and gauge directions drop out of it.
  - It is the sign of the mode's energy and must equal sign(K).
  - It also works for Lagrangians with higher time derivatives.

**M2: flat FRW, the stated background.**
- **Expansion.** The same brute-force expansion, with a(t) arbitrary and V(phi) general (V, V' and V'' along phi_bar = t). A single Fourier mode is taken as cos(kx), with an average over x.
- **Background.** The first-order terms, with the fields uniform, give the background equations. These fix lambda_bar(t) and V(t) in terms of a(t). The dphi first-order term must then vanish identically (the Bianchi identity).
- **Route U (unitary gauge).** dphi = E = 0 is set in the action (a complete gauge).
  - dlambda imposes Phi = 0 at linear order.
  - Second time derivatives are removed by parts. B must then appear without time derivatives, and it is eliminated. If a B_dot^2 term survives, route U stops and this is reported.
  - The result is A(t) Psi_dot^2 - [G(t) k^2/a^2 + m^2(t)] Psi^2, with any Psi Psi_dot term moved by parts.
  - Then c_s^2 = G/A, and the mode is a ghost if and only if A < 0.
- **Route N (Newtonian gauge).** This route uses the Euler-Lagrange equations of all six scalar fields, with B = E = 0 set AFTER variation, so no gauge fixing happens in the action.
  - From the dlambda equation, Phi = dphi_dot.
  - From the E equation, the relation between Phi and Psi (Phi = Psi is expected, not assumed).
  - These are substituted into the B equation (the 0i equation), which is then simplified with the background equations to give one equation for dphi.
  - The Phi, Psi and dphi equations are then checked for consistency.

**Tools:** sympy for M1 and M2; numpy and mpmath for the numerics (N1).

## Controls (each is kept and disclosed if it fails)

- **C0 (GR alone, M1).** With phi, lambda, V and gamma removed:
  - the scalar sector has no propagating mode (the gauge-fixed det has no root in omega);
  - the tensor mode h has omega^2 = k^2 and positive energy (a positive Krein sign).
  - The tensor mode is also checked at every gt of N1: gamma leaves it unchanged, and its sign stays positive.
- **C1 (required: the higher-derivative term off, gt = 0).** Pure mimetic dust has c_s^2 = 0, and this must hold for any V (this also covers CFG124's class B statement that V leaves c_s = 0).
  - M1: every root of the det is omega = 0, so there is no wave.
  - M2 route U: B enters only linearly (no B^2 or B_dot^2 term survives), and its equation is Psi_dot = 0 up to a nonzero factor.
  - M2 route N: the dphi equation is dphi_ddot + H dphi_dot + H_dot dphi = 0, with no gradient term.
- **C2 (required: a literature result for the standard model).** The source is CMV 2014, arXiv:1403.3961, read on ar5iv.
  - CMV's action (their eq. 69) is -R/2 + lambda (g^{mu nu} d phi d phi - 1) - V + (gamma/2)(box phi)^2, in signature (+,-,-,-) (their eq. 20: ds^2 = dt^2 - a^2 dx^2) with 8 pi G = 1.
  - With g -> -g this is CFG124's action with lambda -> -lambda and gamma_CMV = gt.
  - Pass: my M2 reproduces under this map, with M_P^2 restored:
    - eq. (77), 2 H_dot + 3 H^2 = 2 V/(2 - 3 gamma);
    - eq. (80), lambda = (3 gamma - 1) H_dot, i.e. lambda_bar = (1 - 3 gt) M_P^2 H_dot in CFG124's sign;
    - eq. (82), c_s^2 = gamma/(2 - 3 gamma).
  - Also required: eq. (81) (Newtonian gauge), dphi_ddot + H dphi_dot - (c_s^2/a^2) Laplacian dphi + H_dot dphi = 0. It passes if my route-N equation equals this one times a nonzero function of t.
- **C3 (literature, the sign).** The source is FGM 2017, arXiv:1703.02923, read on ar5iv.
  - Their action (eq. 2, signature (-,+,+,+), constraint eq. 1: g^{ab} d phi d phi = -1) is CFG124's with f(box phi) = (gamma/2)(box phi)^2. So f_chichi = gt, and they set M_P = 1.
  - Pass: my route-U Lagrangian equals their eq. (24), S = INT dt d^3x a^3 [(3 - 2/f_chichi) R_dot^2 + (d R)^2/a^2], under the declared normalisation:
    - M_P^2 is restored;
    - the x average gives a factor 1/2;
    - their metric is h_ij = a^2 exp(2 psi) delta_ij with R = psi in unitary gauge, so Psi = -R at linear order;
    - there is no mass term.
  - Their eq. (26), c_s^2 = f_chichi/(2 - 3 f_chichi), then follows.
- **C4 (sign machinery).** A canonical scalar with L = -(s/2)(d chi)^2 goes through the same Fourier and Krein code. It must give omega^2 = k^2 and energy sign s, for s = +1 and for s = -1.
- **What C2 and C3 add.** They are the same physics as the headline, because CFG124's model is the standard one. Their independent content is:
  - the convention map;
  - the terms the headline does not use: the background, lambda_bar, the H terms of eq. (81), and the absence of a mass term.
  C0, C1 and C4 do not depend on the sign or size of gamma.
- **Transcription.** The literature equations were read through a fetch tool that summarises pages. If my derivation disagrees with a quoted equation, I re-read the source before calling it a disagreement, and the README says so.

## Headline pass line (H)

H passes only if H-a, H-b and H-c all hold.

- **H-a (the form).** c_s^2 = gt/(2 - 3 gt) exactly. It must come from:
  - M1 steps (ii) and (iii);
  - M2 route U, independent of a, H, H_dot and V;
  - M2 route N (the gradient coefficient of the dphi equation, normalised to dphi_ddot).
- **"Exactly"** means that sympy simplify returns 0 for the difference. If simplify does not return 0, then 30 random rational evaluations at 50 digits, all with |difference| < 1e-40, count as exact, and this is disclosed.
- **Allowed field redefinitions,** declared now:
  - Psi -> -Psi;
  - a nonzero rescaling by a function of t and k only;
  - second-order changes that vanish on the background equations (Psi versus psi in h_ij = a^2 exp(2 psi) delta_ij).
  Anything else is a departure.
- **H-b (the sign).** K = -(2 - 3 gt)/gt times a positive factor, from M1 step (iii) and from M2 route U. The gauge-invariant sign of M1 step (iv) must agree at every real root sampled in N1.
- **H-c (the windows).** These are solved exactly as sets in gt by sympy:
  - ghost (K < 0 with c_s^2 > 0): exactly 0 < gt < 2/3;
  - gradient instability (K > 0 with c_s^2 < 0): exactly gt < 0 and gt > 2/3;
  - ghost-free and gradient-stable (K > 0 with c_s^2 > 0): the empty set.
- **End points** (part of H-c):
  - gt = 0 is the dust limit (C1). There is no wave, K diverges and the mode is frozen, so at linear order there is neither a ghost nor a gradient instability.
  - gt = 2/3 is singular: K = 0, c_s^2 has a pole, and the background coefficient 2 - 3 gt vanishes.
- **Reported, not a pass line:** c_s^2 > 1 (superluminal) for 1/2 < gt < 2/3, which is inside the ghost window.
- **Partial result.** If H-a holds but H-b or H-c fails, the headline is reported as partly reproduced: the sound speed yes, the ghost window no.

## Numerical confirmation (N1)

- **Points:** gt in {-1, -0.2, -0.01, 8.5e-11, 0.01, 0.2, 0.4, 0.55, 0.65, 0.7, 1, 3} and k in {0.5, 2}.
  - The units are M_P = 1; on Minkowski only omega/k matters.
  - 8.5e-11 is CFG124's G2 bound gt_max.
- **Procedure:** at each point, the brute-force M1 matrix is evaluated numerically; the closed form is not used.
  - The unitary-gauge det is solved for omega with numpy, or with mpmath at 50 digits for gt = 8.5e-11.
  - The null space of the full matrix at each real root is found by SVD.
- **Pass:**
  - A real root has omega0^2/k^2 = gt/(2 - 3 gt) to 1e-8 relative (1e-30 for the mpmath point).
  - An imaginary root has |Im omega0|/k = sqrt(|gt/(2 - 3 gt)|) to the same tolerance.
  - At a real root, the null space is 3-dimensional, and the form restricted to it has exactly one nonzero eigenvalue. That eigenvalue's sign is negative for 0 < gt < 2/3. Here zero means below 1e-9 of the largest singular value (1e-35 with mpmath).
  - The tensor mode has omega^2 = k^2 and a positive sign at every point.
- **Reported row:** CFG124's G2 pair ("c_s^2,max at k = 30/Mpc, z = 10 is 4.2e-11 (gt_max = 8.5e-11)") is checked against the formula at its printed precision.

## Secondary row (S): "0 of 2624 shell cases survive 10 Gyr", point-mass half only

- **Pinned from CFG124's README:** "the flow is geodesic whatever V, gamma or D-terms are added (T0.3a): the fall time over x in [0.3, 30] is 0.003-3.7 Gyr across masses 1e9-1e12, both profiles, both footings; 0 of 2624 shell cases survive 10 Gyr, so the first crossing is before 10 Gyr at every scored x."
- **The definition** (CFG124's frozen G1.2): shells start on the target with v = 0. A case survives only if there is no shell crossing before 10 Gyr AND C(r, 10 Gyr) is within 10% of C_44.
- **What cannot be pinned.** The README does not say how 2624 splits: neither the grid size nor the number of profiles or classes per case. So I do not try to reproduce the count. I test the statement "no case survives" on my own grid, plus the fall-time range.
- **Set-up:**
  - the point mass only;
  - M_b in {1e9, 1e10, 1e11, 1e12} Msun;
  - a0 in {9.3603e-11, 1.1312e-10} m/s^2;
  - x0 on a 200-point log grid in [0.3, 30], giving 1600 cases;
  - r_M = sqrt(G M_b/a0);
  - the target from the gates file, M_c(<r) = M_b (sqrt(1 + x^2) - 1);
  - GM_sun = 1.32712440018e20 m^3/s^2 and 1 Gyr = 3.15576e16 s.
- **S0 (dynamics).** The flow is class A. The constraint alone makes the flow geodesic, u^nu nabla_nu u_mu = (1/2) d_mu X = 0 on X = -1, for any V and gamma.
  - S0 checks this with sympy on a general (t, x)-dependent 2-D metric.
  - The weak field gives Newtonian radial free fall.
  - Before any crossing, each shell encloses the constant mass M_b sqrt(1 + x0^2).
- **Fall time.** The time to reach r = 0 is t_fall = (pi/2) sqrt(r0^3 / (2 G M_b sqrt(1 + x0^2))).
  - It is cross-checked by integrating the radial ODE (scipy, rtol 1e-10, stopped at r = 1e-6 r0) for every 20th x0 of each case.
  - The two must agree to 1e-6 relative.
- **Crossing bound.** t_fall rises with x0 (checked on the grid), so inner shells reach the centre first. Passing through the centre, they meet the shell at x0 no later than t_fall(x0). A case can therefore survive 10 Gyr only if t_fall >= 10 Gyr.
- **Pass line (S):** the number of cases with t_fall >= 10 Gyr is 0.
- **Reported row: the fall-time range.** The minimum and maximum t_fall per footing are compared with the printed "0.003-3.7 Gyr".
  - That printed range spans both profiles, and it may be a crossing time rather than a fall time.
  - "Agrees at the printed precision" means a minimum in [0.0025, 0.0035) Gyr and a maximum in [3.65, 3.75) Gyr.
- **Hand estimate made while drafting (disclosed):** the point-mass maximum is about 3.77 Gyr (M_b = 1e12, x0 = 30, canonical a0), which would print as 3.8. A difference at that level is recorded and resolved in stage 2 from CFG124's script, not by tuning mine.
- **Not covered:**
  - the exponential sphere (its definition is in CFG44's `Bcommon.py`, which this lane has not read);
  - class C's density source;
  - the C(r, 10 Gyr) part.

## MUTATE (each must change a headline and exit 1; a MUTATE that fails to bite is kept and disclosed)

- **MUTATE=a (sign of the higher-derivative coupling).** The action gets -(gamma/2)(box phi)^2; everything else is the same, and gt is still 8 pi G gamma.
  - Expected: c_s^2 becomes -gt/(2 + 3 gt), and the ghost window moves to -2/3 < gt < 0.
  - H must fail, and so must C2 and C3, which carry the same sign. C0, C1 and C4 must still pass.
- **MUTATE=b (normalisation).** (gamma/2)(box phi)^2 becomes gamma (box phi)^2.
  - Expected: c_s^2 becomes gt/(1 - 3 gt), with a window 0 < gt < 1/3. H must fail.
- **MUTATE=s (secondary).** Every shell gets the target's own hydrostatic support, so the net force is zero (this is CFG124's MUTATE=a idea). All 1600 cases then survive, and S must fail.
- **MUTATE=1** applies a, b and s together.
- Each script runs main and every mode that applies to it; a mode that does not apply is not run for that script.
- **Exit code:** main exits 0 only if every pass line and control passes. Any failure exits 1 and is disclosed.

## Readings and expectations (declared before running)

- **Expectation for H:** reproduced. The literature (C2 and C3) states it, and hand calculations I did while drafting agree with it:
  - Minkowski in unitary and Newtonian gauges;
  - the FRW background equation and CMV's eq. (80) in unitary gauge.
  These used the linearised Einstein-Hilbert action and the ADM form from memory, so they are not counted. The residual risk is a convention slip between gt and the action's gamma, which is exactly what H-a and H-b test. My probability for H: about 0.95.
- **Expectation for S:** pass (0 of 1600 survive). The maximum fall time may print as 3.8 against CFG124's 3.7.
- **H PASS:** CFG124's G5 line for class C stands as derived. It says nothing about CFG124's other gates.
- **H FAIL or partial:** the discrepancy is reported in stage 2 with both derivations side by side. CFG124's files are not edited by this lane.

## Read, not read, and where independence stops

- **Read:**
  - CFG124's frozen criteria and README;
  - `closure_map/TEN_DOORS_GATES_2026-09-29.md`;
  - `CFG118_FROZEN_CRITERIA.md` (for house style only).
- **Read on arXiv:**
  - CMV 2014, arXiv:1403.3961: the abstract, and on ar5iv eqs. 20, 69 and 76-82;
  - FGM 2017, arXiv:1703.02923: the abstract, and on ar5iv eqs. 1, 2, 24 and 26, with the ADM ansatz and the definition of R;
  - abstracts only:
    - arXiv:1308.5410 (the original mimetic dark matter paper);
    - arXiv:1601.05405 (the ghost branch of projectable Horava gravity, which the abstract says also applies to mimetic matter);
    - arXiv:1604.08586 (gradient instabilities in mimetic cosmology);
    - arXiv:1704.06031 (instabilities of mimetic matter with higher derivatives, and a healthy extension);
    - arXiv:1802.03394 (mimetic theories as DHOST).
- **Also seen, in the session context:** the subject line of commit 9e4757627, which states the same headline.
- **Not read, and not to be opened before my frozen runs:**
  - CFG124's scripts, .out, .json, run_all.log and exit-code files;
  - CFG44's `Bcommon.py`;
  - any other lane's code.
- **Where independence stops:**
  - The action, its sign conventions and the normalisation gt = 8 pi G gamma are CFG124's, taken as given.
  - The answer was known in advance: from the request, the README, the literature and my hand calculations.
  - CFG124 derived its result from the reduced ADM action in unitary gauge. M1 (covariant brute force, two gauges, a gauge-invariant sign) and M2 route N (Newtonian gauge, equations of motion) are different routes. M2 route U uses the same gauge as CFG124, with a different computation.
  - Both lanes probably use sympy. A bug shared by the library would be caught only by the numpy and mpmath numerics and by the literature controls.
  - Both lanes are written by AI agents in the same programme, so the two derivations may share habits and therefore errors.
  - For S, the target, the a0 values, the x range and the 10 Gyr line are CFG124's and the gates file's.

## Untested (declared)

- Stability beyond linear order.
- Whether a ghost with a cutoff is tolerable (arXiv:1601.05405 argues it can be). The headline is a classical, linear statement.
- The Hamiltonian or DHOST analysis of the constraints.
- Backgrounds other than Minkowski and flat FRW: inside a halo, anisotropic backgrounds, or baryons as a second fluid (CFG124's G2 has baryons).
- The vector sector, and the tensor sector on FRW.
- CFG124's G5 lines for class D and E1 (the scan of 234,834 points and the E1 stiffness), and its G1-G4 verdicts, apart from the point-mass half of the G1.2 row.
- The exponential-sphere half of that row, how the count 2624 splits, class C's density source in G1.2, and the C(r, 10 Gyr) test after crossing.
- The projectable Horava correspondence (recalled as lambda_HL = 1 - gt; not used).
- Strong coupling near gt -> 0 and near gt -> 2/3.

## Script plan (stage 2; working names, in `CFG152_door10_mimetic_referee/`)

- `cfg152_common.py`: the brute-force expansion, the Fourier form and the Krein sign.
- `cfg152_M1_minkowski.py`: M1, C0, C1, C4, N1 and H on Minkowski; modes main, a, b and 1.
- `cfg152_M2_frw.py`: M2, C1, C2, C3 and H on FRW; modes main, a, b and 1.
- `cfg152_S_shells.py`: S0 and S; modes main, s and 1.
- Outputs are named by mode: `<script>.out`, `<script>_MUTATE_<mode>.out` and the matching `_results.json`.
- The scripts import nothing from other lanes.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
