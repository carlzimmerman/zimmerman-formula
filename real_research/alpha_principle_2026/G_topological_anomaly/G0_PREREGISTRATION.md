# Lane G -- topological, anomaly and group-theoretic routes to a gauge-coupling value: pre-registration

Written 2026-09-28 BEFORE any script in this directory was run. No paper was fetched; all formulas are derived symbolically in the scripts
(standard textbook facts used as inputs are named as such). Amendments are appended below the last section, never edited in place.

## Question

Does ANY topological or group-theoretic principle (anomaly cancellation, Witten SU(2) anomaly, Dirac quantization, Chern-Simons levels, index theorems,
instanton number, SL(2,Z) duality, embedding of U(1)_Y in a simple group) force a NUMERICAL value of a gauge coupling -- as opposed to an integer,
a ratio between couplings, or a quantization condition? Target if a value were forced: alpha = 1/137.035999177 (Thomson limit). Every claim carries its scale.

## Central structural hypothesis (to be checked, not assumed)

H0: for a U(1) (or product) gauge theory with charges q_i and coupling g, g enters ONLY through the products g q_i in the matter couplings and through
1/g^2 in the kinetic term. Every anomaly polynomial is homogeneous in the charges q_i and contains no g. Every topological invariant is an integer
(or a rational fixed by integers) and therefore locally constant along the continuous family of couplings. Consequence: topology and anomalies fix
{integers, charge RATIOS, coupling RATIOS in a simple group}, and leave the overall coupling as one free real parameter. The only way a topological
condition could bite a coupling is an EQUALITY that mixes g with a topological integer through an extra self-duality or fixed-point hypothesis;
those are tested explicitly in G5 and G4.

## Scripts, declared checks, pass/fail

### g1_anomaly_charges.py  (sympy)
* A1: one SM generation, left-handed Weyl fields Q(3,2), U(3,1), D(3,1), L(1,2), E(1,1), NO nu_R, unknown hypercharges y_Q,y_U,y_D,y_L,y_E.
  Equations: SU(3)^2 U(1), SU(2)^2 U(1), grav^2 U(1), U(1)^3 (SU(2)^3 and SU(3)^3 vanish for these reps; Witten in A3). Declared expectation from hand algebra:
  solution set = branch B1 {y_Q = 0 = y_L = y_E, y_U = -y_D = t free} union branch B2 {y_Q = s free, y_L = -3s, y_E = 6s, (y_U,y_D) = s(-4,2) or s(2,-4)}.
  PASS if sympy's solution set reproduces this exactly (each solution substitutes to zero in all four equations).
* A2: homogeneity. Anomaly polynomials are homogeneous of degree 1 or 3 in the y's, so every solution family is closed under y -> lambda y. Adding the matter
  coupling g y_i: the map (y -> lambda y, g -> g/lambda) leaves every Lagrangian coupling g y_i unchanged. PASS if sympy confirms both statements.
  Consequence to state: the anomaly conditions fix ratios y_i/y_Q only; g (equivalently the normalization of y) is not constrained. Free real parameters after all anomaly
  conditions with fixed representation content: 1 (the overall normalization, i.e. the coupling), plus one discrete choice.
* A3: Witten SU(2) anomaly: number of Weyl doublets = (N_c + 1) N_g must be even. Verify: (3+1)N_g even for every N_g; for N_c = 1..7 list which (N_c,N_g)
  parities pass. Integer statement only.
* A4: general N_c (colour-number) solution with y_Q as normalization: charges of u-quark = (N_c+1)/(2 N_c) times the unit that makes e^- = -1.
  PASS if sympy reproduces q_u = (N_c+1)/(2 N_c), q_d = (1-N_c)/(2 N_c)... [declared check: q_u - q_d = 1 and q_u + N_c... exact form fixed by the script from the equations, compared to the hand result q_u = 1/2 + 1/(2N_c)].
  Integers/ratios only.
* A5: with nu_R added the solution space is 2-dimensional (Y and B-L directions), i.e. anomaly cancellation ALSO leaves a mixing free; count dimension by sympy rank.
* MUTATE: remove E (electron singlet) from the field content; the SM charges must then FAIL A1 (anomaly-free assignment).

### g2_topological_quantities_coupling_free.py  (sympy + mpmath)
* T1: Dirac quantization e g_m = 2 pi n (HL, hbar = c = 1). The pair (e, g_m) has one free real parameter left, e; g_m = 2 pi n / e. Statement only, checked symbolically.
* T2: instanton number k integer, action S_k = 8 pi^2 k / g^2 (SU(N), canonical); theta periodicity 2 pi. The integer k is coupling-independent; S_k is a function of the free g.
  Symbolic: d k / d g = 0 and dS_k/dg != 0. Declared expectation: topology adds nothing to fix g.
* T3: 2+1D Chern-Simons: L = -(1/4 e^2) F^2 + (k/4 pi) eps A dA. Level k integer (large-gauge invariance). Derive the topologically massive photon mass in the rest frame from the
  quadratic form: m = k e^2 / (2 pi). PASS if sympy gives m = k e^2/(2 pi) (up to sign of the root); it shows e^2 stays independent of the integer k.
* T4: quantum Hall bookkeeping: sigma_xy = nu e^2/h, R_K = h/e^2 = mu_0 c/(2 alpha). nu integer; alpha appears as an independent prefactor (CODATA-value check only, no claim).
* T5: N=4 SU(N) SYM: conformal anomaly a = c = (N^2-1)/4 from free-field counting (real scalars 1, Weyl fermion 11/2... i.e. Dirac 11, vector 62, all /360); equals the exact value at every g
  (non-renormalization), while g (tau) is an exactly marginal modulus: an anomaly invariant on a conformal manifold does not see the coupling.
* MUTATE: 4d instanton action with 4 pi^2 in place of 8 pi^2 ... [declared: the mutated Dirac condition e g = 4 pi n must FAIL the check that the electric-magnetic pairing is 2 pi n].

### g3_gut_embedding_ratios.py  (sympy)
* E1: SU(5) fundamental: Y = diag(-1/3,-1/3,-1/3,1/2,1/2); T3 in the SU(2) block. Trace formula sin^2 theta_W = Tr T3^2 / Tr Q^2 over the SM fermions of one generation
  (5bar + 10, i.e. the 15 Weyl fields), evaluate = 3/8 exactly. Same for the 16 of SO(10) (decomposed 5bar + 10 + 1 under SU(5)) and the 27 of E6 (16 + 10 + 1, the extra
  states being vector-like: 10 -> 5 + 5bar, so they must contribute in the ratio 3/8 too if complete SU(5) multiplets). PASS if all three equal 3/8.
* E2: the ratio is forced ONLY by a single simple group: Pati-Salam SU(4)xSU(2)_L xSU(2)_R with independent g_4, g_L, g_R gives sin^2 theta_W as a free function of the coupling ratios;
  show the 3/8 point requires g_4 = g_L = g_R (a coupling relation imposed, not derived) and that the one overall coupling is free. Non-complete multiplets (drop the 10) break 3/8.
* E3: one-loop coefficients b_i from field content: SM (41/10, -19/6, -7), MSSM (33/5, 1, -3). PASS if reproduced.
* E4: alpha_em^{-1}(mu) = (5/3) alpha_1^{-1} + alpha_2^{-1}; at unification = (8/3) alpha_G^{-1}, i.e. alpha_em(M_G) = (3/8) alpha_G. Symbolic.
* MUTATE: drop the 10 of SU(5) from the trace ratio; must FAIL the 3/8 check.

### g4_unification_running_and_handles.py  (numpy/mpmath, inputs declared)
Inputs (declared, MEASURED, NOT derived; PDG-like): m_Z = 91.1876 GeV, alpha_em^{-1}(m_Z) = 127.955, sin^2 theta_W(m_Z, MSbar) = 0.23122, alpha_s(m_Z) = 0.1179.
* U1: with the group-theory b_i of E3 and one-loop running, find the M_G,alpha_G where alpha_1 = alpha_2 (SM and MSSM), and the alpha_3 mismatch there (reported). This is the
  forward relation: the 3 low-energy couplings fix (alpha_G, M_G) + one consistency; group theory supplies b_i and the 3/8 -- and nothing else.
* U2: sensitivity: d alpha_em^{-1}(low)/d alpha_G^{-1} and d alpha_em^{-1}(low)/d ln M_G. Report that alpha_em(low) needs two independent inputs (alpha_G, M_G) beyond group theory,
  plus the spectrum (thresholds).
* U3 (handles): alpha_G^{-1} versus a FIXED list, declared now, of group-theoretic numbers: dim SU(5) = 24, dim SO(10) = 45, dim E6 = 78, dim E8 = 248, 4 pi^2 = 39.478, 8 pi = 25.133.
  TRIAL COUNT = 6 handles x 2 spectra (SM,MSSM) = 12 comparisons. A HIT = |alpha_G^{-1}/handle - 1| < 1e-3.
  Chance-hit expectation: prior log-uniform alpha_G^{-1} in [10,100], window 2e-3 in log => p = 2e-3/ln(10) = 8.7e-4 per comparison, E[chance hits] = 12 x 8.7e-4 = 0.010.
  Also REPORTED, not scored: percentage offsets; the one-loop crossing has O(5-10%) systematics from thresholds/2-loop, so a 1e-3 hit is not even expected to be meaningful.
  Declared expectation: no hit at 1e-3. Post-hoc remarks (MSSM alpha_G^{-1} ~ 24 vs dim SU(5)) are NOT scored.
* U4: the scale statement: the group-theory relation alpha_em = (3/8) alpha_G holds at M_G ~ 1e16 GeV, not at Thomson; alpha_em(Thomson) needs the running through the SM spectrum.
* MUTATE: b_i of SM with b_2 sign flipped; the crossing/consistency check (U1 alpha_3 mismatch below 10 percent for MSSM) must FAIL.

### g5_duality_fixed_points.py  (sympy)
* D1: with minimal electric charge e and minimal Dirac monopole g_m = 2 pi/e, S-duality e -> e_D = 2 pi/e (alpha -> pi/e^2 = 1/(4 alpha)); self-dual point alpha = 1/2. tau = theta/2pi + 2 pi i/e^2 = theta/2pi + i/(2 alpha).
* D2: SL(2,Z) fixed points tau = i (alpha = 1/2, theta = 0) and tau = exp(i pi/3) (alpha = 1/sqrt 3, theta = pi). Both computed; the real-world tau = i/(2 alpha) at alpha = 1/137.036 has Im tau = 68.52.
  Trial count = 2 fixed points (+ the images under SL(2,Z) with the SAME Im tau > 1 only in the fundamental domain, so no other hit is possible). Declared expectation: no hit; S-duality
  as an exact symmetry would put alpha = O(1), excluded by 137x; it is not a symmetry of the real QED spectrum (no light monopoles).
* D3: the Witten effect shifts the electric charge by theta e/2 pi; with theta_QED bounded ~ 0 by neutron EDM/atomic EDM this does not move alpha (statement, not tested numerically).
* MUTATE: Dirac condition with 4 pi; the self-dual point must then not be alpha = 1/2 (check fails).

## Overall pass/fail (declared)

* The route yields a FORCED PRINCIPLE for a gauge-coupling value only if some topological/anomaly/group condition, with no free integer chosen after the target, no mass input,
  the declared trial count and a stated scale, equals alpha (or alpha_G with a forced spectrum and forced M_G) at the 1e-3 level.
* DECLARED EXPECTED OUTCOME: NO. The anomaly polynomials, indices and levels are integers/rationals independent of g; the GUT embedding forces the ratio 3/8 only, with (alpha_G, M_G) free;
  S-duality fixed points give O(1) alpha. The verdict, to be checked, is that the overall coupling is the one parameter every topological principle leaves free.

## Scope / not tested (no computation, no reading)

Heterotic/type I 10D anomaly cancellation (Green-Schwarz) fixes dim G = 496 and ties gauge to gravitational coupling through the DILATON vev (a modulus): not computed here,
stated from memory of the literature and NOT read. Discrete/global anomalies (Z_4-spin, new SU(2), Wang-Wen-Witten) are integer/parity statements, not computed. Non-perturbative
lattice or asymptotic-safety fixed points belong to lane B. kappa = 1/2 stays FITTED, the SM mass sector stays walled, no dark-matter particle.

## Amendment 1 (2026-09-28, appended after the first run of g1, g2, g3; nothing edited above)

* g3 MUTATE as pre-registered ("drop the whole 10") was ILL-DESIGNED: the 5bar alone is a complete SU(5) multiplet and also gives sin^2 theta_W = 3/8, so the first mutation run
  failed only through an unrelated `not MUT` guard I had put on E1e. Replaced by a real mutation: remove u^c from the 10 (an incomplete multiplet). The 3/8 checks must then fail.
* g1 A5: the dimension count was done by a different (stronger) method than declared: the cubic on the 3-dim linear solution space factorises as 18 a0 (2a0 - a2 - a5)(4a0 + a2 - a5),
  so the nu_R solution variety is a UNION OF THREE 2-planes (one of which contains span{Y, B-L}); dimension 2 as declared, but not a single plane.
* g1 A4 and g2 MUTATE lines in this file contain half-edited declared text (the "[declared: ...]" fragments); the scripts' checks are the authoritative statement of what is tested.
* Honest classification of g2 checks: T1b, T2c, T5b are STATEMENTS OF STRUCTURE (a quantity that has no g in it has zero derivative with respect to g), not tests that could have come out otherwise.
  T1a takes L = e g/(4 pi) as textbook input. The nontrivial computations are T2a/T2b (BPST integral), T3 (Chern-Simons mass by explicit EOM) and T4 (Hall bookkeeping numbers).

## Amendment 2 (2026-09-28, appended BEFORE the first run of g4)

g4 gains one extra variant so that the handle comparison is not hostage to the crude "SUSY at m_Z" assumption: a two-segment one-loop running with the SM b_i below M_S = 1 TeV and the MSSM b_i above
(single declared M_S, not scanned). It adds 6 handle comparisons: TOTAL TRIAL COUNT for U3 = 6 handles x 3 spectra (SM; MSSM at m_Z; SM+MSSM with M_S = 1 TeV) = 18, expected chance hits
= 18 x 8.7e-4 = 0.016. The scoring rule (1e-3) is unchanged. If ANY comparison hits I will report it as a hit inside a 18-trial family and state that it is not a derivation
(no forced spectrum, no forced M_G; see U2), and I will not add or remove handles afterwards.
