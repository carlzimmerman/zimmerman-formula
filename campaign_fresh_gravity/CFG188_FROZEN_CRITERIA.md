# CFG188 — Independent referee re-derivation of the physics core of CFG172 (door 11C, time-direction flowing vacuum). FROZEN CRITERIA (phase 1)

Written 2026-09-29 by the referee agent, before any CFG188 script. No physics script was written or run in phase 1. Anything marked "hand" is arithmetic done on paper after reading the CFG172 frozen file and README; it is a hand ESTIMATE, not a result, and is itself to be checked in phase 2. Literature facts are from memory, unverified, unless a record file is cited. kappa = 1/2 is FITTED. Nothing here says the theory is closed, that the timelike-flow reading is refuted outside the frozen class, or that any data favour the framework. A failed control or a wrong expectation is kept and reported, never repaired. If a CFG188 result disagrees with CFG172, the disagreement is reported as found.

## 0. What was read (phase 1) and what was NOT

Read: `campaign_fresh_gravity/CFG172_FROZEN_CRITERIA.md` (incl. Erratum 1), `campaign_fresh_gravity/CFG172_door11C/README.md`, `campaign_fresh_gravity/closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`, `campaign_fresh_gravity/CFG44_fluid_target/README.md`, the kernel block of `CFG44_fluid_target/Bcommon.py` (nu_p2, nu_mono definitions only), `qwen_claude_field_theory/closure_2026/fc_kh_terminal/FC_KH_PAPER_vNEXT.md` and `PASS_KILL.md`, and the docstring header (lines 1-50) of `real_research/khronon_momentum_2026/KM1_khronon_carries_phantom.py`.

NOT read, and not to be read before my own main and MUTATE runs are saved: every `*.py`, `.out`, `.json` in `CFG172_door11C/`. In phase 2 those may be opened only after my outputs are saved; any change to my scripts after that is a disclosed departure.

Contamination disclosed: the README's headline numbers are known to me. They are TARGETS to reproduce, not blind predictions. Where a hand estimate below equals a README number, the estimate was made after seeing it and carries no evidential weight beyond "I can reproduce it by hand".

## 1. What is re-derived, and where independence STOPS

Re-derived independently (my own sympy/numpy, from the actions written in the frozen file, in a different gauge and route from what the frozen file describes):

R1. The static spherical field equations of 11C-a (and the a-channel of 11C-b, 11C-c) from the **unitary-gauge (ADM) form** of the action, S = (1/16 pi G) Int dt d3x N sqrt(h) [ K_ij K^ij - (1+c2) K^2 + R3 - 2 Lambda + F_a(a^2) ], a_i = d_i ln N (c13 = 0, omega = 0, so aether = khronon), in the **areal gauge** ds^2 = -N(r)^2 c^2 dt^2 + A(r)^2 dr^2 + r^2 dOmega^2, fully nonlinear in Phi/c^2 (the frozen file uses an isotropic weak-field (Phi, Psi) Lagrangian). Also the covariant aether equation for the static aligned u (does the radial component vanish for a general F_a?). Then the G1 grid (7 masses, point and exponential sphere, both footings, P2 primary, nu_mono reported) solved from the derived equations.
R2. The kinetic (no-ghost) structure of the flow's radial and tangential perturbations, (y q)' and q, in two ways: (i) the decoupling limit (metric fixed) and (ii) a STRETCH local high-k analysis with the metric dynamical (uniform-acceleration background, unitary gauge, scalar sector phi, psi, B, E). The P2 tail bound in closed form, its dependence on the band and on the target kernel, and Q2 by three recipes.
R3. 11C-b: the static reduction of M^2 F(K), the redundancy of the overall size of (c2, c14, M), the operating-point (anchor) analysis, the continuation dependence, the G6/G7 side with the F-dressing question, and D1.
R4. 11C-c: elimination of the theta response, the effective baryon pressure, c_s^2 = -K_c rho and its sign under the flips of the coupling and of c2; a retarded (finite khronon speed) dispersion toy.

Independence STOPS at (each is imported as a record fact, labelled, not re-derived unless the STRETCH item says so):
- S-1. The action class as written in the frozen file (I derive from it; attack (a) asks whether it is the right class but cannot make it the right class).
- S-2. The targets: CFG44's P2 and nu_mono kernels (read-only import of `Bcommon.py` allowed; P2 is trivial and re-implemented by me), the exponential sphere, both a0 footings.
- S-3. Q2 <= 5.2e-27 s^-2, Saturn's distance, the ephemeris delta A_R bounds (3.66e-14 / 3.72e-14 m/s^2 at Earth/Mars, quoted in the CFG185 commit message seen in my session context, not re-derived). The CFG7 "tide = max(|dg/dR|, g/R)" recipe is taken as stated in the frozen file (I never open CFG7).
- S-4. The Flanagan (2302.14846) stability condition and the record's full-ADM c^2_par expression (PASS_KILL.md) are record facts; R2(ii) is a check AGAINST them, not a re-derivation of them, and is a STRETCH.
- S-5. alpha_1 = -4 c14, alpha_2 = c14 (c14 - c2 + 2 c14 c2) / (c2 (2 - c14)) (Yagi et al., from memory / as the frozen file quotes), the PPN limits (3.4e-5, 1.6e-9, alt 3.5e-5, 2.1e-5) and KM1's G7 threshold (c2 >= 2.7e-5 at 600 km/s) are quoted. My stretch item R3-S re-derives the moving-source coefficient only if time allows; otherwise G7 numbers are quoted and labelled so.
- S-6. G2 (growth), G3 (energy), G4 count as such, S1/S2 stress-energy (Addendum 2): out of scope; I do not opine on them.
- S-7. CV4's statement "K = 3H(z) inside bound regions" is re-derived only in its divergence structure (R3, step B3); no non-linear "maximal-leaf" branch.

## 2. Headline pinned (README numbers = targets) and hand checks already done on paper

| # | CFG172 README headline | my hand check (paper arithmetic, after reading the README) |
|---|---|---|
| H1 | 11C-a G1-law max dev 5e-14 (P2), 5e-6 (nu_mono); 7 masses x point/exp sphere x both footings | expected: identity for spherical baryons (algebraic law mu g = g_N); numbers here are root-finder tolerances |
| H2 | P2 kernel mu(y_g) = (sqrt(1+4y^2)-1)/(2y); (y q)' = 1 - 2y/sqrt(1+4y^2) > 0; q -> 1/(2y) | verified by hand from g^2 = g_N^2 + a0 g_N; (yq)' = 1/(8y^2) at large y |
| H3 | minimal tail forced by the +-10% band and (yq)' >= 0: **0.282 a0**; simple kernel 0.4675; nu_mono 0.424 | P2 closed form: h_min(eps) = (1 - sqrt(1-eps^2))/2 with eps = 1 - band; eps = 0.9 gives **0.28206**; simple kernel by hand: y_N* = 1.478, 0.4676 (matches); nu_mono not done by hand |
| H4 | isolated Sun's own P2 tail = a0/2 at Saturn: Q2 = **6.3e3 x** (canonical), 7.6e3 x (alt footing); minimal-tail kernel Q2 >= 3.6e3 x | 0.5 a0 / R_Sat (R_Sat = 9.54 AU = 1.427e12 m) / 5.2e-27 = 6.31e3 (alt: 7.62e3); 0.282/0.5 x 6.31e3 = 3.56e3 |
| H5 | 11C-b: G1 needs offset t <= 1.2e-6 (Newtonian continuation), 4e-4 (mirrored); G6/G7 need t >= 4.0e6; gap 3e12 / 1e10 | t = K_bg / DeltaK = 440 (c2/c14); with c2 >= 2.7e-5 and c14 <= 3.2e-9 (alpha_2 = -c14/2): 440 x 8.4e3 = **3.7e6** (lane 4.0e6: 8% off); G1 tolerance from the x = 30 end: y_g^2 = 1.1e-3, shift tolerance ~ 2e-4 to 4e-4 (mirrored, matches 4e-4); the Newtonian-continuation 1.2e-6 I cannot reproduce by hand |
| H6 | 11C-b D1: a_*(z)/a_*(0) = 1.79, 3.77, 8.29 at z = 1, 2.5, 5 | E(z) = sqrt(0.3153 (1+z)^3 + 0.6847) = 1.79, 3.77, 8.29 by hand (H(z)/H0, Omega_m = 0.3153) |
| H7 | 11C-c: K_c = 8 pi G beta^2 c^4 / (c2 theta_L^2), P = -K_c rho^2/2, c_s^2 = -K_c rho < 0 for c2 > 0 | by hand: L_eff = +K_c rho^2/2 after eliminating delta-theta with the leaf constraint; P = rho eps' - eps = -K_c rho^2/2; agrees |
| H8 | README C5 failed (CFG7 MW tide 3e-5 of the bound, not 4-6x), A5.1 failed, M6 (Newtonian) did not bite, M7 tautological | kept as record; I do not attempt to repair them |

## 3. Hand ESTIMATES (labelled; made after reading the README) with reproduction probabilities

"Reproduce" = my independent number lies within the stated agreement tolerance (section 8).

| item | my estimate | P(reproduce CFG172's number) |
|---|---|---|
| E1 static reduction: mu(y) g = g_N, mu = 1 - q, q = Q'/(2y), Psi = Phi at leading order; the covariant aether equation is satisfied by static aligned u for any F_a | agree structurally | 0.95 |
| E2 Psi/Phi - 1 (exact nonlinear equations, worst grid cell) | 1e-5 to 1e-4 (size a_* r at x = 30, M = 1e12 gives a_* r = 4e-5, plus Phi/c^2 ~ 1e-6) | 0.85 that it is <= 1e-3 (the lane says exactly 0 in the weak-field limit; mine will be small but nonzero: not a disagreement) |
| E3 G1-law max dev, P2 | <= 1e-6 (root-finding) | 0.90 |
| E4 G1-law max dev, nu_mono | <= 1e-4 | 0.85 |
| E5 number of hidden free objects in 11C-a's static reduction | 1 free function (F_a of one variable, pointwise equal to the inverse of the target kernel: G1 is an identity) + 2 constants (a_* by rule T, c2 inert in the static sector); the pass carries zero evidence for the kernel | 0.97 |
| E6 (yq)' sign, K_x = (yq)', K_perp = q (decoupling limit) | as the lane | 0.90 |
| E7 full-theory (metric dynamical, local high-k) radial kinetic coefficient has the sign of (yq)' times a positive factor (2 - c14_eff = 2 mu > 0, c2-dependent normalisation) | supports the lane; **P 0.6**; P 0.3 not completed in the time budget (reported NOT DONE, never as agreement); P 0.1 a different sign structure is found (then G5's "theorem" is decoupling-limit conditional) | 0.6 |
| E8 tail lower bound, P2, +-10%: closed form (1 - sqrt(1-eps^2))/2 | 0.28206; +-20% gives 0.2000 (exact); +-50% gives 0.0670; the band at which the tail bound alone stops violating the Q2 bound (tail <= 7.9e-5) is eps ~ 0.018, i.e. band ~ 98% | 0.97 (0.282), 0.90 (98% figure) |
| E9 tail lower bound, simple kernel; nu_mono | 0.4676; nu_mono ~ 0.42 (numerical; depends on the floored-derivative repair) | 0.95; 0.70 |
| E10 Q2 canonical / alt / minimal-tail | 6.3e3 / 7.6e3 / 3.6e3 | 0.90 each |
| E11 alternative Q2 mappings (direct apsidal precession of a constant radial acceleration; direct delta A_R at Earth/Mars) | precession per orbit = 2 pi eps/g_N (hand, near-circular): Saturn 4.5e-6 rad/orbit = 3.2 arcsec/century for eps = a0/2; Earth/Mars: 0.5 a0/3.7e-14 = 1.3e3; the pincer survives every recipe by >= 3 orders of magnitude (against bounds quoted from memory) | not a lane number; direction of agreement 0.9 |
| E12 continuation independence of the tail bound for 11C-a | none: s(y) = y q(y) is non-decreasing for all y >= y_* = 0.929 (P2 at eps = 0.9), so s(1e6..1e8) >= 0.282 whatever the continuation; the lane's M6 non-bite concerns 11C-b's F below the branch point, not the a-channel | 0.95 |
| E13 11C-b G1 tolerance on the offset t: mirrored | 3e-4 to 4e-4 | 0.70 (within a factor 1.5 of 4e-4) |
| E14 11C-b G1 tolerance on t: Newtonian continuation | mine ~ 2e-4 to 4e-4 (the shift acts through the smallest-y grid point, y_g^2 = 1.1e-3); the lane's 1.2e-6 is unexplained by my hand analysis | 0.30 (within a factor 3 of 1.2e-6); P 0.6 that I get a number > 30x larger and must report "continuation-conditional", NOT "lane wrong" |
| E15 11C-b t required by G6 and G7 (undressed, theta = 3 H0) | 3.7e6 | 0.80 (within 15% of 4.0e6) |
| E16 11C-b: overall size of (c2, c14, M^2) is a field redefinition of F's argument; only R = c14/c2 and the function F are physical; the effective couplings are c14_eff = 2 q(y), c2_eff = 2 q(y)/R (dressing cancels in the ratio) | confirmed symbolically | 0.85; consequence: the lane's "overall size of c2 free" (G4 strict = 1) is overstated |
| E17 11C-b: G6(b) under F-dressing (c2 and c14 both multiplied by F' at the test system's acceleration) | alpha_2 ~ R q_p (R >> 1); pulsar row y_p ~ 8e11 gives ~2e-10 (< 1.6e-9): PASS; planetary systems would fail if alpha_2 were applied to them; lane's undressed FAIL becomes reading-dependent | 0.55 that the dressed reading flips the G6(b) cell to PASS |
| E18 11C-b pincer under dressing | G1 x G7 x (c14_eff < 2 for spin-0 stability): needs t <= 4e-4 and c2 >= 2.7e-5 with c14 < 2, i.e. t >= 440 x 2.7e-5 / 2 = 6e-3; gap ~ 15 (not 1e10-3e12) at the frozen band and x_max = 30; disappears if x_max <= ~10 or band >= ~60% | 0.50 that this weaker pincer is what remains |
| E19 11C-b anchor: F's kernel anchored at K = 0 (rule T, the lane's) versus at K_bg(z = 0): the second passes G1 at z = 0 at any R, at the price of an H0-dependent constant in F, and a_*(z) not flat | G1(b) passes at z = 0 | 0.95 |
| E20 (y q_eff)' for u = y^2 - t is negative just above the branch point for any t > 0 (finite slope Q'(0) = -1 gives (y q)' = Q + (y^2/w) Q' -> -infinity as w -> 0+) | confirmed | 0.95 |
| E21 D1 numbers 1.79, 3.77, 8.29 | reproduced (hand) | 0.99 |
| E22 11C-c c_s^2 = -K_c rho, K_c = 8 pi G beta^2 c^4/(c2 theta_L^2) (sign independent of beta; c2 -> -c2 flips the sign of c_s^2 and makes the khronon a ghost) | agree | 0.95 sign; 0.90 coefficient |
| E23 11C-c retarded dispersion: growth persists for k below the khronon crossing scale; UV growth rate ~ k sqrt(K_c rho) unbounded (lane) | mine may find a k^4 (c2 (nabla^2 chi)^2) regularisation at very high k | 0.55 for "unbounded in the UV" |

Overall estimate: P(CFG188 agrees with CFG172 on every gate verdict of 11C-a, 11C-c) ~ 0.85. P(CFG188 finds the 11C-b verdict "G1 x (G6, G7) pincer with gap 1e10-3e12" reading-conditional or overstated) ~ 0.55. P(CFG188 finds an outright arithmetic/derivation error in the lane's static reductions or tail bound) ~ 0.05.

## 4. Derivations and exact pass lines (R1-R4)

### R1. Static reduction (11C-a; a-channel of b, c)  — procedure and lines

Procedure. sympy: metric above; K_ij = 0 for the static slicing (the Hubble tilt is carried by u, not by the static slicing: a_i = d_i ln N, theta = 3H does not enter the static equations; the leaf-averaged theta term drops out). Reduced Lagrangian L(N, N', A, A') = N A r^2 [ R3(A, r) + F_a(X) ] - 8 pi G rho c^2-style matter term with X = N'^2/(N^2 A^2); F_a normalised so that (1/16 pi G) F_a(a^2) = (1/8 pi G) a0^2 Q(y) with a_* = a0/c^2 (the frozen normalisation). Euler-Lagrange for N and A (the theta-theta equation follows from matter conservation for pressureless static dust; I check that it is consistent to the order kept). Expand in 1/c^2 with y = O(1); keep the leading term.

Lines.
- R1.a: the N-equation reduces to nabla.((1 - q) nabla Phi) = 4 pi G rho with q = Q'(y)/(2y); residual simplify == 0 symbolically. FAIL if the coefficient differs from mu = 1 - q (e.g. an extra factor or a different argument y).
- R1.b: the A-equation gives Psi = Phi at leading order; report max |Psi/Phi - 1| on the G1 grid from the exact nonlinear solve. Agreement line: <= 1e-3 (E2); anything larger is a finding.
- R1.c: covariant aether equation, radial projection (for u = static Killing direction, F_a generic): sympy shows it vanishes identically. FAIL if a nonzero radial residual survives (then the aligned static aether is not a solution and 11C-a's static reduction is incomplete).
- R1.d: G1-law from the DERIVED equations: kernel q is obtained from the target by inversion, then Q(y) = Int 2 y q dy, then the equations of R1.a are solved for g(r) by brentq (point mass) and by radial integration of the enclosed baryon mass (exponential sphere, h = 2 kpc); 7 log-spaced masses 1e9-1e12, x in [0.1, 30], canonical (a0 = 9.3603e-11) and alt (1.1312e-10) footings. PASS line = the frozen 10% line and my own tighter reporting line: P2 <= 1e-6, nu_mono <= 1e-4 (E3, E4). The result is an identity check; it is NOT scored as evidence for the kernel.
- Controls (main, exit 1 if any fails): C1 GR limit F_a = 0 reproduces exact Schwarzschild N^2 = 1 - r_s/r, A^2 = 1/(1 - r_s/r) from the derived N/A equations. C2 linear aether F_a = c14 a^2 gives G_N = G/(1 - c14/2) at leading order (Eling-Jacobson; from memory), i.e. q = c14/2: this pins my normalisation against the published one. C3 exponential kernel: q = e^{-y}, (yq)' = (1-y) e^{-y}, and 1 - (yq)' = 1 + (y-1)e^{-y} (record's W''). C4 P2 identities: g^2 = g_N^2 + a0 g_N, M_c = M(sqrt(1+x^2) - 1) (CFG44), mu = (sqrt(1+4y^2) - 1)/(2y).

### R2. Stability, tail bound, Q2

R2.a (decoupling limit). sympy: perturb the foliation (chi) in the fixed background, expand N sqrt(h) F_a(a^2) to second order in the acceleration perturbation; the Hessian of F_a with respect to a_i gives K_x = (yq)' along the acceleration and K_perp = q transverse (up to a common positive factor). Line: (yq)' as printed in H2; sign table for P2 (positive), exponential kernel (negative for y > 1: C3).

R2.b (STRETCH, full theory, local high-k). Quadratic action for (phi, psi, B, E) in unitary gauge about a locally uniform acceleration background (N = 1 + a.x; h_ij flat; background-equation terms dropped, high-k only; approximation stated), plane waves parallel and perpendicular to a; extract the radial and tangential dispersion. Line: sign of the radial kinetic coefficient equals sign of (yq)' (times positive factors); compare the closed form with PASS_KILL.md's c^2_par ONLY AFTER my own is saved. Outcomes: SUPPORTS (E7 mainline), DIFFERS (then the (yq)' >= 0 premise of the tail theorem is decoupling-limit conditional, and the theorem is reported "not established in the full theory"), NOT DONE (declared; never counted as agreement).

R2.c (tail bound, exact). Definition: s(y) = y q(y) = (g - g_N)/a0 is the anomalous acceleration in units of a0 (g_N = mu g). Band: g in [eps, 2 - eps] g_t(y_N) with g_t the target (P2: g_t = a0 sqrt(y_N^2 + y_N)). Constraint from below: s(y_g) >= y_g - Y(y_g/eps), Y(z) = (-1 + sqrt(1+4z^2))/2. With (yq)' >= 0 (s non-decreasing) the tail for all y >= y_* is >= max_y [y - Y(y/eps)] = (1 - sqrt(1 - eps^2))/2 (hand). sympy proves the closed form; scipy maximises numerically for P2, the simple kernel, nu_mono; sweep the band from 1% to 99%.
Lines: P2 at 10%: 0.2821 (+-0.003); 20%: 0.2000 (+-0.001); 50%: 0.0670; band at which the bound reaches 7.9e-5 (the Q2 tolerance): 98.2% (+-1%); simple 0.4675 (+-0.003); nu_mono 0.424 (+-0.02).

R2.d (Q2 recipes). Q2 in units of the bound Q2max = 5.2e-27 s^-2.
- Recipe A (lane's, CFG7 H1 as described in the frozen file): tide = max(|d g_ph/dR|, g_ph/R), g_ph = a0 s(y). Sun's own P2 tail (s -> 1/2) at Saturn (9.54 AU), both footings: line 6.3e3 (+-3%), 7.6e3 (+-3%); minimal-tail kernel 3.6e3 (+-5%).
- Recipe B (direct physics): apsidal precession per orbit of a near-circular orbit under g(r) = g_N + eps: 2 pi eps / g_N (hand); at Saturn, Earth, Mars; report as a multiple of an ephemeris apsidal-precession bound taken from memory (labelled unverified; if I cannot state it, I report the precession in arcsec/century only and mark the ratio NOT SCORED).
- Recipe C: direct anomalous radial acceleration against the quoted delta A_R bounds at Earth/Mars (S-3).
Line for "pincer survives": every recipe gives ratio >= 100 for the minimal tail. FAIL of that line (some recipe gives < 100) would be reported as a recipe-sensitive result.
- EFE remark (not scored; hand): with a uniform external field g_e << g_N, the phantom source div(q grad Phi) = (a0/2) div n_hat stays a0/2 at leading order; sympy check of the first correction (g_e/g_N)^1 only, labelled diagnostic.

### R3. 11C-b

B1 (own reduction). Static law at theta = theta_bg: a-dependence of M^2 F(K), K = (c2 theta_bg^2 - c14 a^2)/M^2, with F anchored per rule T: F(K) = P2-function of u = -K/DeltaK, DeltaK = c14 a_*^2/M^2, so u = y^2 - t, t = K_bg/DeltaK = (c2/c14)(theta_bg c/a0)^2 (440 c2/c14 at theta = 3 H0, 301.6 c2/c14 at theta_Lambda). q_eff(y; t) = Q(sqrt(y^2 - t)) for u >= 0; continuation for u < 0: (N) q = 0; (Mi) q(u<0) = Q(sqrt(|u|)) (mirrored); (L) q = 1 (linear standard aether). Solve mu_eff(g) g = g_N for the G1 grid over t; find t_max at the 10% line for each continuation and for x_max = 30, 10, 3.
Lines: t_max(Mi) within a factor 2 of 4e-4; t_max(N) within a factor 3 of 1.2e-6 (else "continuation-conditional", E14).
B2 (G6/G7 side). Undressed: c14 = R c2, alpha_1 = -4 c14, alpha_2 from S-5; feasible region in (c2, c14) for alpha_1 <= 3.4e-5 (also 3.5e-5, 2.1e-5), alpha_2 <= 1.6e-9, c2 >= 2.7e-5 (S-5); minimal t on that region: line 4.0e6 (+-15%). Note: the alpha_2 = 0 (equal-speed) branch c14 ~ c2 is reported separately (it is excluded undressed by alpha_1; E15 says the lane's region is the small-c14 branch only).
B3 (redundancy; CV4 structure). sympy: L = M^2 F(K) is invariant under (c2, c14, M^2, F) -> (s c2, s c14, s M^2, F(K/...)) with the argument rescaled: only R and the function F are physical. Effective local couplings c14_eff = 2 q(y), c2_eff = 2 q(y)/R, F' cancels in the ratio. The static khronon equation for theta: D_i (N F'(K) c2 D^i K) = 0 (divergence form), so K = const = 3H(z) is the regular solution for any F' of one sign. Lines: invariance residual == 0; the divergence form printed; F' sign along the G1 solution (positive definite or not: if F' changes sign the operator degenerates: reported).
B4 (dressed G6/G7). Evaluate alpha_1, alpha_2 at (i) the cosmic background, (ii) a galaxy (y = 1, 10), (iii) Saturn, (iv) the pulsar row (y ~ 8e11), with c14_eff, c2_eff of B3; KM1's G7 with c2_eff(y). Line: the printed table; the verdict flip test of E17.
B5 (anchor and D1). Anchor at K_bg(z = 0): G1(b) at z = 0 passes for any R (line: max dev <= 1e-6); a_*(z) and t(z) at z = 0, 1, 2.5, 5 for both anchors: E(z) numbers 1.79, 3.77, 8.29 for the K = 0 anchor (line +-1%), and the consequence for the K_bg anchor (feature displaced by (H^2(z) - H0^2)/H0^2 in units of DeltaK).
B6 (pincer status). Report min t on the G6 x G7 region (undressed: 3.7e6; dressed: 6e-3 with c14_eff < 2), the G1 t_max for each continuation and x_max, and the gaps; verdict wording: "pincer" only if the gap is >= 1e3 under both dressing readings.
R3-S (stretch). Moving-source linear solve in khronometric gravity for the coefficient C = 2(2+3c2)/(c2(2-c14)) and D/3 = 0.114, 0.285 at 620 km/s; if not done, G7 numbers are marked QUOTED.

### R4. 11C-c

Procedure. sympy on a lattice (N cells) and in the continuum: L = -(c2/16 pi G) sum dtheta_i^2 - (beta c^2/theta_L) sum rho_i dtheta_i with constraint sum dtheta_i = 0 (leaf average) and the khronon equation nabla^2 (dL/dtheta) = 0; solve; substitute back; get eps(rho) = rho c^2 - K_c rho^2/2, P = rho eps' - eps, c_s^2 = dP/drho. Envelope check: the force on a lattice baryon equals the gradient of eps (finite differences). Retarded toy: linear hydrodynamics of the baryons coupled to a scalar dtheta with a finite propagation speed c_theta = sqrt(c2/q) c (q = 1 as a bound); dispersion relation omega(k). Flips: beta -> 0 (no force), c2 -> -c2.
Lines: K_c coefficient +-1%, sign of c_s^2 negative for c2 > 0 for every beta != 0; linear-versus-saturating h reported as the lane's (lin) and (sat) cases (in sat, c_s^2 = -K_c(rho) rho(1+...) sign only). G1(c) inherited from the a-channel: not re-scored. Also the count of hidden objects: 2 (beta free, c2) + the declared h shape.

## 5. The four attacks — frozen procedures, pass/fail meaning

Attack (a): is the frozen action class right and complete, and does a gauge/constraint choice change the static reduction?
- Procedure: (i) R1.c (aether vs khronon: same static reduction if the aligned static aether solves the radial aether equation); (ii) list every invariant that is non-zero on a static slice of a bound region: a^2, theta (= 3H), R3 (the slice's 3-Ricci scalar, size y a_*/L >> a_*^2 by 1e6), divergence of a; sympy shows that F(a^2, theta) changes the static law only through theta_bg (this IS 11C-b), and that a term of the form g(R3/a_*^2) or g(div a) would enter the static reduction at the same order as the kernel (the lane's class omits them by declaration; attack notes the class is a choice, not derived); (iii) c13 = 0 with c1 = -c3 != 0: shear/twist vanish on static slices (sympy); (iv) the constraint choice: Lagrange multiplier vs khronon vs Stueckelberg: same static equations.
- Meaning: PASS (lane's class is right for the scored static reduction) = R1.a, R1.c hold and (ii)-(iv) add nothing inside the class. DISAGREE if R1.c leaves a residual. Extra terms (R3, div a) are reported as "outside the frozen class, would change the static law": a scope note, not an error.

Attack (b): is the 0.282 a0 tail bound a theorem or an artefact of the +-10% band and of P2?
- Procedure: R2.c band sweep; R2.c other targets (simple, nu_mono); R2.a/R2.b for the premise (yq)' >= 0.
- Meaning: the bound is a THEOREM OF THE BAND (band-robust up to ~98% and target-robust across P2, simple, nu_mono) if the closed form holds and the premise (yq)' >= 0 is supported. It is CONDITIONAL on the premise: if R2.b DIFFERS, the tail bound is only a decoupling-limit statement (q ~ O(1) at y ~ 1, where the metric mixing is O(1)); then the lane's G5 FAIL for 11C-a is "not established in the full theory". If R2.b is NOT DONE, the report says so.

Attack (c): is Q2 sensitive to the continuation to 1 AU and to the recipe?
- Procedure: E12 (monotone s(y) is continuation-independent for the a-channel); R2.d recipes A, B, C at Earth, Mars, Saturn; R3-B1 continuation study for 11C-b (Newtonian, mirrored, linear) — the only place where a continuation matters.
- Meaning: PASS (lane robust) if all recipes give ratio >= 100 for the minimal tail and the a-channel bound has no continuation dependence. For 11C-b the M6 non-bite is explained if the G1 tolerance t_max is continuation-insensitive in my run (then Newtonian vs mirrored differ only by the exact form, not by orders of magnitude); if mine shows a large continuation dependence (E14: > 30x), the lane's 1.2e-6 versus 4e-4 spread is a real feature and the pincer gap must be quoted as a range (3e12 to 1e10), which the lane did.

Attack (d): does the G1-law pass for 11C-a genuinely require the declared kernel; how many free functions/constants does the static reduction hide?
- Procedure: R1.d plus: (i) replace F_a by any other function with the same rule-T scale (M1-type control: mu -> a different interpolating function); G1 vs P2 fails at the 10% line by amounts that equal the kernel difference (the simple kernel differs from P2 by up to 15.5% in nu); (ii) show, by sympy, that the reduced action determines q(y) and nothing else about the law; (iii) count: functions (F_a: 1), constants (a_*: tied by rule T, c2: inert in the static sector, kappa = 1/2 FITTED inside a_*), structural choices (c13 = 0; baryons only as source; minimal coupling; sign/branch of q >= 0).
- Meaning: the G1-law pass is an identity requiring the declared kernel (agrees with the lane's P-declared grade); any pass not requiring it would be a finding. If the stationary point of the reduced action selects q uniquely from something other than the declared function (it will not, E5), the count changes.

## 6. MUTATE controls (each flips a load-bearing cell; `MUTATE=<name>`; the control must make its claim fail, exit 1; outputs named by mode; a control that does not bite is a declared control failure, kept)

- M1 (drop the monotonicity premise): allow (yq)' < 0 (exponential-type q = e^{-y}-like fall after y_*). The tail lower bound must drop to ~0 (Q2 pincer cell flips to PASS). Bites iff min tail < 1e-4. Tests that the pincer's load is (yq)' >= 0.
- M2 (widen the band to 99%): the closed-form tail bound falls below the Q2 tolerance (7.9e-5); the cell "tail bound exceeds the Q2 tolerance" must flip. Shows the bound is band-conditional only at absurd bands.
- M3 (kernel -> GR, q = 0): G1-law flips to FAIL (dev 0.97 at x = 30) and the tail and Q2 vanish (the two ends of the pincer move in opposite directions).
- M4 (flip q -> -q, mu > 1): G1-law flips to FAIL; the no-ghost cell (K_perp = q) flips to FAIL.
- M5 (11C-b anchor moved to K_bg): the cell "G1(b) fails at the rule-T anchor" must flip to PASS at z = 0 (max dev <= 1e-6). Tests that the pincer is anchor-conditional.
- M6 (11C-b dressing): apply F-dressing to c2 and c14 in alpha_2 (B4); the cell "G6(b) FAILs at every c2 that G7 allows" must flip. Tests E17.
- M7 (11C-c sign flip c2 -> -c2): c_s^2 must become positive (and the khronon flagged as a ghost by the kinetic sign of the c2 term); the cell "c_s^2 < 0" flips.
- M8 (11C-c beta -> 0): the contact force and K_c vanish (G1(c) inheritance untouched): cell "compaction force non-zero" flips.
- M9 (R1 static reduction): drop the N'-dependent term of F_a (F_a -> 0) inside R1's derivation: the derived equation must fail to give mu = 1 - q (R1.a residual != 0 for nonzero q): confirms R1.a is not a tautology.
- M10 (band definition control for R2.c): compute the tail bound with the band applied to g_N instead of g (a wrong definition): must change the number by > 5% (shows the definition is load-bearing).
Each MUTATE flips exactly one named cell; positive control (prescribed flow v(r) = sqrt(2 Int g dr): G1-law passes, grade M0) is C5 of the main run.

## 7. Script plan

Location: the scratch dir (`<scratch>/cfg188/`), later the orchestrator's lane directory. numpy/scipy/sympy only. Repo root from `ZF_REPO` or by walking up from `__file__`; printed paths are `<repo>/...` and `<scratch>/...`; no absolute home path is ever printed or stored. Each run < 15 min. Exit convention: main run exits 0 if all reproduction controls (C1-C5 and internal identities) pass; verdicts AGREE/DISAGREE/CONDITIONAL are results, not exit codes; a control failure exits 1 and is kept; `MUTATE=<name>` exits 1 when the control bites (the targeted claim fails as required); outputs `*_MUTATE_<name>.out/.json`; a MUTATE run that does not bite is a declared control failure (exit 0 is then reported as "did not bite").

| script | content | MUTATE |
|---|---|---|
| `cfg188_common.py` | constants (both footings), P2, simple, nu_mono (read-only import of CFG44 `Bcommon.py` if present, else labelled rebuild), exponential sphere, band helpers, repo-root helper, no-absolute-path printer | - |
| `CFG188_R1_static_reduction.py` | R1.a-d, controls C1-C4, attack (a)(i)(iii)(iv), attack (d)(i)-(iii), C5 prescribed flow | M3, M4, M9 |
| `CFG188_R2_stability_tail.py` | R2.a, R2.b (STRETCH, clearly flagged), R2.c band and kernel sweep, R2.d recipes A/B/C, EFE remark | M1, M2, M10 |
| `CFG188_R3_b_operating_point.py` | B1-B6, R3-S if time allows, attack (a)(ii), attack (c) for 11C-b | M5, M6 |
| `CFG188_R4_c_response.py` | R4, lattice, retarded toy, flips | M7, M8 |
| `CFG188_verdict.py` | reads the JSONs, prints AGREE / DISAGREE / CONDITIONAL against the section-2 targets with the section-8 tolerances; in phase 2 only, after my own outputs are saved, may read the lane's outputs for a side-by-side | - |
| `run_all.sh` | order R1, R2, R3, R4, verdict; ZF_REPO handling | - |

## 8. Agreement tolerances and what would count as disagreement

Agreement (AGREE):
- G1-law verdicts equal (both PASS at the 10% line) and my max deviation <= 1e-3 (P2) / 1e-3 (nu_mono).
- Tail bounds: P2 0.282 +-0.003; simple 0.4675 +-0.003; nu_mono 0.424 +-0.02; Q2: 6.3e3, 7.6e3, 3.6e3 within +-5%.
- (yq)' expression and sign identical; c_s^2 sign identical and K_c within 1%.
- t_max (Mi) within a factor 2 of 4e-4; t_G6G7 within 15% of 4.0e6; D1 numbers within 1%.

CONDITIONAL (reported, not an error; the lane's verdict depends on a declared choice I can identify): Newtonian-continuation t_max differing from 1.2e-6 by more than a factor 3; the G6(b) verdict under dressing; the pincer gap under the anchor (rule T at K = 0 versus K_bg); the pincer gap versus x_max and the band; the (yq)' premise if R2.b is NOT DONE or DIFFERS.

DISAGREE (would count as a finding against the lane's derivation or headline):
- D-1 my R1.a coefficient differs from mu = 1 - q (structural), or R1.c leaves a non-zero radial aether residual, or |Psi/Phi - 1| > 1e-3 on the grid.
- D-2 a different sign of (yq)' for P2, or a tail lower bound outside +-0.01 of 0.282 from the same definitions, or Q2 canonical outside 6.3e3 +-10% with the frozen recipe.
- D-3 c_s^2 > 0 for c2 > 0 in 11C-c, or K_c off by more than 5%.
- D-4 t_G6G7 or the G1 t_max off by more than a factor 10 with the same declared continuation and the same dressing reading.
- D-5 the README's statement "overall size of c2 free" survives (E16 fails: the redundancy is not present).
A DISAGREE is reported with the cell, both numbers and my derivation, not adjusted.

## 9. Declared choices, forking paths, and what is NOT covered

- The suspicions in section 3 (E2, E11, E16-E20) were formed while reading the README; they are pre-registered here, before any script. The tests may falsify them.
- I choose the areal gauge and the ADM (unitary-gauge) form because they are independent of the frozen isotropic weak-field Lagrangian; the price is that a static Killing slicing is assumed (no Hubble tilt). The Hubble tilt (a_i = static acceleration + O(H^2 r/c^2), theta = 3H) is argued by hand only: v = H r = 2 km/s at 30 kpc, H^2 r ~ 4e-15 m/s^2 << a0 (not scored).
- R2.b is a STRETCH with an explicit approximation (uniform-acceleration background, high k); NOT DONE is a legitimate outcome. R3-S is a STRETCH.
- Dressing (E17) is a reading, not a derivation, of which coefficients a test system sees; both readings are reported, never pooled.
- Not covered: G2, G3, G4-as-count, S1/S2 (Addendum 2), growth/CMB, non-spherical baryons, twist mode, c13 != 0, EFE beyond the first correction, the maximal-leaf branch, AeST, nonlocal gates, alpha_3 and retardation, lensing beyond Psi = Phi, any data. Q2 numbers and PPN limits are quoted, not verified.
- Literature (Flanagan, Yagi et al., Eling-Jacobson, Shao-Wex, INPOP/ephemeris precession bounds) is from memory or as the record cites it; none re-read.

Hash of this file is reported by the writer after the last edit; a later change would void it.
