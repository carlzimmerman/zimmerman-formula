# PLAN — nonradial stability and MeV continuation of the diffuse mixed condensate

Checkpoint label: **CL-2F-2026-10-19-01** (parent EKG-2026-10-19-C).
Written and committed ALONE, before any script or run in this directory.
Base HEAD at writing: 42b43a572c921d2894ad475a0969a0078c89b286.

Question carried by the handoff (sol61_push/CLAUDE_HANDOFF_CONTINUUM_MEV_2026_10_19.txt):
"check continuum and nonradial stability of the diffuse mixed condensate, then
continue it toward our physical MeV parameters. Does a stable state survive
without changing the action?"

Inputs verified before writing (SHA256 as given by the brief):
- full_two_field_2026_10_19/checkpoint.json  1a111b5c...0324e64  (match)
- full_two_field_2026_10_19/RESULT.txt       f3d800c3...eb80aba9 (match)
- gradient_analysis/STABILITY_AUDIT.txt      a5a94ea3...e1ac4a   (match, final timed pin)
Existing files are read only; nothing outside this directory is modified.
The theory is NOT closed; no statement here closes it.

## 0. Action, units, the one varied parameter

Action unchanged: canonical complex Phi (charge 1, mass m), X (charge 2, mass M),
minimal Einstein gravity, signature +---,
V = m^2|Phi|^2 + M^2|X|^2 + g(X* Phi^2 + c.c.) + lambda|Phi|^4,
Delta = M^2 - 4m^2 > 0, lambda = lambda_rep + g^2/Delta.
Scale fields by m/sqrt(lambda), r by 1/m. Then m = lambda = 1, and with u* = 0.02,
r_lambda = 2 held FIXED: M^2 = 4(1+u*^2) = 4.0016, g_hat = sqrt(4u*^2/(1+r_lambda))
= 0.023094010767585032, lambda_rep = 2/3. The only remaining parameter is
Gamma = G m^2 / lambda_tot.
Endpoint: Gamma_phys = G_N (1 MeV)^2 / lambda_tot, lambda_tot recomputed by script from
sigma_0/m = lambda_rep^2/(8 pi m^3) = 0.3 cm^2/g, lambda_tot = (1 + 1/r_lambda) lambda_rep
(expected ~7.61e-43). At Gamma_phys the rescaled action IS the benchmark action.
Intermediate Gamma are different members of the same family (a homotopy), not a
change of units.

## 1. Branch label (declared)

Primary branch: central field amplitude f_c = 0.009888264649460883 (units m/sqrt(lambda_tot))
held fixed, u*, r_lambda fixed. In the Thomas-Fermi (TF) limit this is central chemical
fraction x_c = 0.4, i.e. fixed central local chemical frequency; compactness and
1 - omega tend to Gamma-independent TF values. The charge is NOT held fixed: at leading
order Q_hat, M_hat scale as Gamma^(-3/2) and the radius as Gamma^(-1/2). This is stated in
RESULT; the endpoint object is "the same intensive state", not the same charge.
Secondary label (scaling statement only, no stability verdict): fixed Q_hat = 2.2669e7.

## 2. Part N — nonradial (l >= 1) stability of the existing diffuse state (Gamma = 1e-8)

N1 Axial sector (analytic + symbolic). Scalar perturbations are all polar (parity
(-1)^l), so axial perturbations carry no matter degree of freedom. Derive with sympy the
axial Regge-Wheeler-gauge equations on the static anisotropic background with
delta T_mn = -p_t h_mn (exact for complex scalars: delta L = 0 for axial h, L = p_t),
reduce to a master wave equation, check the vacuum limit reproduces Regge-Wheeler, and
evaluate the potential V_ax(r) on the saved GR profile for l = 2, 3, 10.
Pass: V_ax > 0 everywhere (then the conserved/decreasing energy with outgoing
radiative boundary condition excludes growing axial modes). l = 1 axial: shown to be
stationary rotation/gauge only.

N2 Polar sector at leading (Newtonian) order — LABELLED APPROXIMATION.
Model "NR-GPP": the nonrelativistic two-component Gross-Pitaevskii-Poisson reduction of
the same action (fields Phi -> e^{-it} Phi, X -> e^{-2it} X, drop O(|d_t|^2/m^2)),
energy H = int |grad Phi|^2 + |grad X|^2 + Delta|X|^2 + g(X*Phi^2+c.c.) + lambda|Phi|^4
- (Gamma/2) int int rho rho'/|x-x'|, rho = 2(|Phi|^2 + 4|X|^2), charge N = int rho.
The linearized Newtonian potential is solved self-consistently in every l-sector
(multipole kernel r_<^l / r_>^(l+1)); this is NOT the Cowling approximation.
Analytic part (to be written in RESULT with proof): second variation splits into
L+^(l) (real parts) and L-^(l) (imaginary parts). Claims to be proved:
 (a) both are "cooperative" (off-diagonal -2g f <= 0, gravity = minus a positive kernel),
     so their semigroups are positivity improving (Perron-Frobenius);
 (b) L-^(0) (f,2h) = 0 and L+^(1) (f',h') = 0 exactly (phase, translation);
 (c) K_l (gravity multipole operator) is operator-decreasing in l, kinetic increasing;
 (d) hence, IF f,h > 0 and f',h' < 0 on (0,inf) [hypothesis H1, checked numerically],
     L-^(l>=1) > 0, L+^(1) >= 0 with kernel = the 3 translations, L+^(l>=2) > 0, and the
     essential spectrum (Weyl; exponential tails) starts at 2(1-omega) > 0 (Phi) and
     Delta + 8(1-omega) (X), so all l >= 1 sectors are coercive modulo translations
     and no l >= 1 growing mode exists at this order, for ALL l at once.
Numerical part: Newtonian "shadow" background at the same Gamma and same f_c, solved by
Newton iteration on the same grid (exact discrete stationary point); then for
l = 0,1,2,3,4 (+ l = 8,16 trend): lowest eigenvalues of L+^(l), L-^(l) and the
Bogoliubov frequencies sigma^2 = eig(W^-1 L- W^-1 L+) (W = diag(2,4) symplectic weights)
via symmetric Cholesky reduction; l = 0 restricted to the fixed-charge tangent and
quotiented by the phase orbit with the paired projection (as in STABILITY_AUDIT.txt).
Radial Vakhitov-Kolokolov cross-check: number of negative eigenvalues of unconstrained
L+^(0) and the sign of dN/dmu along the branch.
Discretizations (two genuinely different):
 D1 second-order finite differences in y = r w (Dirichlet at 0 and R_box), multipole
    kernel by trapezoid quadrature; resolutions h = 8, 5.333, 4 at R_box = 8000; domain
    check R_box = 10000 at h = 5.
 D2 sine-DVR (spectral kinetic matrix) on the same domain, N = 1000, 1500.
Convergence / acceptance (declared now):
 C1 sign of every reported eigenvalue identical across all D1/D2 resolutions and domains;
 C2 reported frequencies agree to <= 1e-3 relative between finest D1 and finest D2;
 C3 the l = 1 translation eigenvalue is <= 1e-2 of the next l = 1 eigenvalue and
    shrinks under refinement (~h^2 for D1);
 C4 discrete stationarity residual <= 1e-10 relative; phase-kernel residual reported;
 C5 hypothesis H1 checked on every background used (f,h > 0, f',h' < 0 except
    numerically-zero far tail below 1e-12 f_c, which is reported).
GR calibration (the only sector where full GR exists): NR-GPP l = 0 lowest frequency vs
the existing full constrained ADM value 2.303832927e-6 m (stability/run_018).
 Pass if |relative difference| <= 1e-2 (expected O(eps), eps = max(1-omega, 2GM(r)/r)).
 If it fails, the polar nonradial verdict is downgraded to UNDECIDED.
Instability sign check: NR-GPP at the compact control (G = 8.5e-5, central h = 0.02,
seeded from equilibria/run_001/mixed_center.npz) must be reported. Pass if a real growing
radial pair appears with gamma within a factor 2 of 1.411e-6. If NR-GPP finds it stable,
this is recorded as "NR misses a GR-sensitive marginal instability" and the transfer
criterion below is tightened by the observed |sigma^2| scale of that control.
GR transfer criterion for l >= 1 polar: the lowest non-symmetry NR sigma^2_l must exceed
100 * eps * (4 pi Gamma q_c), q_c = 2(f_c^2 + 4 h_c^2), with eps measured on the GR
profile; l = 1 translations are exact symmetries of the asymptotically flat system in
GR (zero modes with boost partners, not instabilities). For l >= 2 the GR gravitational-
wave continuum carries positive canonical energy and zero U(1) charge, so radiation can
only decrease delta^2(H - omega Q); with a positive matter Hessian it damps, it cannot
drive growth (no rotation, no negative-energy mode, hence no CFS-type route). This is an
argument at leading order, not a full-GR polar QNM computation; RESULT will say so.

Continuum statement: essential spectrum from the asymptotic free operators (particle and
antiparticle branches of both fields give positive H - omega Q since omega < m,
2 omega < M); the computed low modes must lie below the Phi threshold (checked); a
high-wavenumber coercivity bound (kinetic term minus sup of local and gravity terms) is
reported to show any negative direction would have to live inside the resolved band.

## 3. Part C — continuation toward Gamma_phys at fixed f_c

C1 Full-GR static BVP (new script here; same equations as
   equilibria/solve_tf_seeded_ekg.py, z = sqrt(Gamma) r, states f,f_z,h,h_z,v,b,
   omega via logit), seeded from the previous step in z:
   Gamma = 1e-8 * 10^(-k/2), k = 0..8 (1e-8 ... 1e-12).
   Step 0 must reproduce the saved benchmark (omega within 1e-9 absolute; M_ADM, Q within
   1e-6 relative; R99 within 1e-5 relative of mixed_G1em8_x04.json).
   Per step record omega, Omega_c, v = Gamma^(3/2) M_ADM, Gamma^(3/2) Q, z99 = sqrt(Gamma) R99,
   C99, min N, h_c, edge length; independent off-grid residual check (4th-order finite
   differences of the interpolated solution in the original r-form KG/Einstein
   equations) and independent charge/mass quadrature. Acceptance per step: collocation
   rms residual <= 1e-6, independent relative KG residual <= 1e-5 away from the far tail,
   mass/charge quadratures agree <= 1e-6.
   Failure handling: one retry with halved step / more nodes; a remaining failure is
   reported as METHODOLOGICAL (not nonexistence) unless a fold is evidenced by
   the trend (d(observable)/d ln Gamma diverging) AND the TF-limit structure (C2).
C2 GR TF limit (Gamma -> 0 exactly): TOV with the algebraic two-field TF EOS at x_c = 0.4
   (Gamma-independent in z). C1 observables must approach C2 values with a fitted power
   law in Gamma; the fitted correction at Gamma_phys is reported.
   Edge boundary layer: measured edge length in z must scale ~ Gamma^(1/3) (Airy /
   Painleve-II matching); the fitted exponent is reported (pass if within 0.25-0.45).
C3 Stability along the path: NR-GPP (D1) at Gamma = 1e-8, 1e-9, 1e-10, 1e-11, 1e-12 at
   fixed f_c (two resolutions each; agreement <= 1e-2 relative on s^2 required; 1e-12
   included only if met with N <= 2500 per component), reporting s^2 = sigma^2/(4 pi Gamma q_c)
   for l = 0 (fixed charge), l = 1 (translation and next), l = 2, 3, 4, plus H1, n(L+^(0))
   and dN/dmu.
C4 Gamma = 0 anchor, independent equations: irrotational barotropic Newtonian
   hydrodynamics of the TF star (single superfluid, relative phase and composition
   locked by conversion), sigma^2 delta q = -div(q grad(e''(q) delta q + delta U)),
   full linearized Poisson (no Cowling), l = 0 (fixed mass), 1, 2, 3, 4, two grids.
   Pass: C3 s^2 values approach C4 values with a fitted power law.
C5 Endpoint at Gamma_phys: equilibrium = TF interior (C2) + edge layer of relative width
   ~Gamma^(1/3) + exponential tail; stability = C4 values with fitted corrections and
   O(eps) GR corrections; physical radius, mass, charge and mode periods in SI.
Labels: "survives" if all monitored sigma^2 > 0 at every computed Gamma and at the C4
anchor, no fold; "loses stability" if any sign change is robust under C1 (sign) checks;
"folds" if C1 shows a turning point confirmed by refinement and C2.

## 4. Answer classes (declared before running)

- YES (classical, linear, leading order with bounded GR correction): H1 holds; N1 passes;
  N2 positivity confirmed on D1 and D2 for l = 1 (minus translations), 2, 3, 4; GR
  calibration <= 1e-2; transfer criterion met; C1-C4 show no fold or sign change and
  convergence to a positive TF anchor. RESULT then lists, separately, what is NOT shown:
  full-GR polar spectrum, rigorous interval enclosure, nonlinear, quantum/many-body,
  formation, lifetime, abundance.
- NO: a robust negative sigma^2 in any sector of the branch, or a confirmed fold before
  Gamma_phys.
- UNDECIDED: any acceptance criterion above fails without a robust negative result.

## 5. Resources and hygiene

Every run: nice -n 19, one thread (OMP/OPENBLAS/VECLIB/MKL_NUM_THREADS=1), peak RSS
recorded (getrusage) and kept < 2 GB (dense matrices <= 5000 x 5000), wall < 20 min each.
The live 1024^3 engines (cfg650/cfg654, chain6.sh) are not touched. No downloads.
Outputs are JSON/text in this directory; logs scrubbed of home paths. Only files in this
directory are committed, by explicit path; no push.
