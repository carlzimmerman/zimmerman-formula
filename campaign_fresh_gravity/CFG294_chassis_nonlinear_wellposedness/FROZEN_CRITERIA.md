# CFG294 — FROZEN CRITERIA: nonlinear local well-posedness of the relativistic chassis (C-H/K) on the khronon's leaves

Frozen 2026-10-02, before any CFG294 script was written or run. Nothing below may be edited after the commit
that adds this file. Corrections go in a dated section appended at the end.

What this lane addresses: CFG292's "not proven" list (README, "Verdict, scope, caveats"). That list has three items:

- nonlinear local well-posedness, i.e. a smooth symmetriser for the quasilinear system;
- constraint propagation for the C_i;
- an elliptic–hyperbolic coupling theorem.

The task is a first-principles derivation, certified by computation where an algebraic statement is involved. It is
not a literature survey.

## 1. The system (committed, not chosen here)

- **Action.** L340's C-H/K: I_CHK = I_CH + c^3/(16 pi G) Int sqrt(-g) [alpha_c a_mu a^mu - c_2 K^2].
  - beta = 0 (c_T = 1) and lambda_K = 1 + c_2.
  - The clock, N = X^(-1/2), a = D ln N and K are C-H's own
    (`qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`).
  - The full C-H variations are taken from FULL_VARIATION.md §1: the lapse derivative H, the stress P^{ij} and the
    auxiliary equations.
- **Formulation F2a.** This is CFG292's verdict formulation, reused exactly through `cfg292_lib.py`, which is imported
  read-only from the CFG292 lane:
  - unitary time gauge t = tau;
  - the spatial diffeomorphisms fixed by the spatial components of the de Donder vector (4-D trace), with gauge term
    -1/2 N sqrt(gamma) gamma^{ij} C_i C_j;
  - the lapse h_00 eliminated through its leaf-elliptic equation.

  The evolved fields are (h_0i, h_ij), 9 components.
- **Domain (ACTION.md).** Closed, compact, connected leaves, with T^3 included explicitly.
- **Principal part.** GR + the BPS khronon. CFG292's R0 re-verified this in-lane: the MOND/filter sector is order
  -infinity wherever the filtered field is non-zero. CFG292's numbers are read from its committed results JSON, not
  recomputed.
- **Parameters.**
  - The 18 record points are exactly CFG292's: alpha_c in {alpha_min, alpha_max} of L340 P1, times c_2 in {the six L350
    G2 ceilings, the P1 c2 edges, the recipe edge 0.10}. They are exact rationals at 6 significant digits, with the same
    `rat()` rounding as CFG292.
  - Two windows are certified:
    - W_P1 = [alpha_min, alpha_max] x [c2_min, c2_max] (L340 P1);
    - W_rec = [alpha_min, alpha_max] x [min c_2, max c_2] over the 18 points, i.e. [9.624e-14, 3.2e-9] x
      [6.310e-4, 0.10].
  - No parameter is scanned or tuned. kappa = 1/2 is FITTED and plays no role.

## 2. The derivation steps and what certifies each

The scalar speed is c_S^2 = c_2 (2 - alpha_c) / (alpha_c (2 + 3 c_2)) (beta = 0; CFG292 T1). On a frozen background
with lapse N, shift N^i and leaf metric gamma, write nu = N^i k_i and rho = N^2 gamma^{ij} k_i k_j.

### S1 — Constant multiplicity

Claim to be certified: the characteristic roots of the lapse-reduced F2a symbol are lambda = nu +- sqrt(rho), with
multiplicity 8 each, and nu +- c_S sqrt(rho), with multiplicity 1 each. Both families are semisimple, and they never
cross on W_rec, uniformly in (N > 0, N^i, gamma > 0) and in the direction of k.

- **S1a, symbolic in (alpha, c_2) at beta = 0, aligned background, khat = z.** For each helicity block (tensor,
  vector, scalar after the lapse elimination), with M the first-order companion
  M = [[0, I], [-A^-1 C, -A^-1 B]] of P_red(lambda) = A lambda^2 + B lambda + C, both of the following hold:
  - the characteristic polynomial is exactly the predicted product;
  - the minimal-polynomial identity holds identically as rational functions:
    (M^2 - 1)(M^2 - c_S^2) = 0 in the scalar block, and M^2 - 1 = 0 in the vector and tensor blocks.

  Together these prove semisimplicity at every (alpha, c_2) where the entries are defined and c_S^2 is not 0 or 1.
- **S1b, rigorous interval arithmetic** (mpmath.iv, outward rounding) on the exact c_S^2 formula over W_P1 and W_rec.
  - The lower bound of c_S^2 - 1 must be > 0.
  - Exact monotonicity (the signs of dc_S^2/d alpha and dc_S^2/dc_2 on the boxes) locates the minimum at the corner
    (alpha_max, c2_low). There the exact minimum gap |c_S - 1| is reported, together with the minimum separation of
    distinct eigenvalues, min(2, c_S - 1) in units of sqrt(rho).
  - Reported for both windows.
- **S1c, exact certification of uniformity.**
  - Set 1: the unsplit 10 x 10 F2a symbol at all 18 points x 24 exact rational unit directions (stereographic, fixed
    seed), aligned background.
  - Set 2: 6 random rational frozen backgrounds (lapse in [1/2, 2], shift components in [-1/2, 1/2],
    gamma = I + a rational symmetric perturbation, positive definite by Sylvester), at 3 corner points
    (max c_S, min c_S, and (alpha_max, c2_max of P1)), x 4 rational k each.
  - At each point, all of the following hold exactly:
    1. P_00,00 is lambda-free and equals (2 alpha - 1) sqrt(gamma) gamma^{ij} k_i k_j / (4 N^3), the predicted formula.
    2. P_0r is at most linear in lambda, so the Schur complement is a quadratic pencil.
    3. det A != 0.
    4. det P_red(lambda) is proportional to [(lambda - nu)^2 - rho]^8 [(lambda - nu)^2 - c_S^2 rho].
    5. ((M - nu)^2 - rho)((M - nu)^2 - c_S^2 rho) = 0 exactly. This certifies semisimplicity and the constant
       multiplicities (8, 8, 1, 1) with no square roots.
  - Frame covariance is the analytic argument behind uniformity. Every frozen background is related to the aligned one
    by a leaf-preserving linear frame change (a Galilean shift, spatial GL(3), and a rescaling of t). Under such a
    change the gauge term and the action density transform covariantly. The README states this argument; set 2 checks
    it.
- **S1d, degeneracy loci.** The distance of W_rec from each locus is reported:
  - alpha = 0: det A = 0 (minimal Horava);
  - alpha = 1/2: the F2a lapse coefficient vanishes (a gauge artefact);
  - c_S^2 = 1: alpha = c_2/(1 + 2 c_2);
  - c_S^2 = 0: c_2 = 0 or alpha = 2.

  The record point closest to the crossing locus is named.

### S2 — Symmetriser (Kreiss)

- **Theorem cited.** Kreiss (1970, Comm. Pure Appl. Math. 23, 277), in the form of Kreiss & Lorenz (1989) and Sarbach &
  Tiglio (2012, Living Rev. Relativ. 15, 9, §3): strong hyperbolicity with eigenvalues of constant multiplicity implies
  a symmetriser H(u, xi) that is smooth in (u, xi), homogeneous of degree 0 in xi, and uniformly positive on compact
  sets, with H M symmetric. Métivier (2014, J. Éc. polytech. Math. 1, 39) gives the L^2 theory, with symmetrisers smooth
  in xi and Lipschitz in (t, x).
- **Explicit construction used here, not merely cited.**
  - The spectral projectors come from Lagrange interpolation in M' = (M - nu)/sqrt(rho):
    - P_{+-1} = +- R (M' +- 1)/2, with R = (M'^2 - c_S^2)/(1 - c_S^2);
    - P_{+-c} = +- Q (M' +- c_S)/(2 c_S), with Q = (M'^2 - 1)/(c_S^2 - 1).
  - H = Sum_j P_j^T P_j = 1/2 [R^T R + M'^T R^T R M'] + 1/2 [Q^T Q + M'^T Q^T Q M' / c_S^2]. This is rational in the
    data; no square root appears, so the identity is exact.
  - Analytic facts to be stated and checked:
    - H M' = Sum_j lambda_j P_j^T P_j is symmetric;
    - Sum_j P_j = I gives v^T H v >= |v|^2 / 4, hence lambda_min(H) >= 1/4 and kappa(H) <= 4 Sum_j ||P_j||^2.
  - The field-space inner product is CFG292's Frobenius scaling (off-diagonal h components weighted by 1/sqrt 2), so the
    numbers are comparable.
- **S2a, exact, at every S1c point.** The following hold exactly:
  - H = H^T;
  - H M - M^T H = 0;
  - H is positive definite: every exact LDL^T pivot is > 0.

  lambda_min(H) >= 1/4 is checked in mpmath at 50 digits. kappa(H) is reported and compared with the bound and with
  CFG292's kappa(T).
- **S2b, dense directions.** At each of the 18 points, 500 random unit directions in mpmath at 40 digits.
  - H must be symmetric, positive definite and H M symmetric, each to a relative 1e-25.
  - kappa(H) must be direction-independent to a relative 1e-20 (rotation covariance about the aether).
- **S2c, smoothness.** The entries of H at khat = z are rational in (alpha, c_2), computed symbolically at beta = 0. Their
  denominators may vanish only on the S1d loci; this is listed and checked to miss W_rec. Away from those loci H is
  real-analytic in (background, khat), because M is rational in them with non-vanishing denominators (S1c 1, 3).
- **S2d, finding, not load-bearing: the canonical-energy route (Hughes–Kato–Marsden 1977).** Report the inertia of A and
  C of the symmetric reduced pencil at the 18 points.
  - If A is definite and C has the opposite definiteness, the Lagrangian energy is itself a symmetriser.
  - If not, the HKM hypothesis of a positive canonical energy fails, and the Kreiss symmetriser is what carries S3.

### S3 — Quasilinear local existence for the hyperbolic part

- **Theorems cited.**
  - Kato (1975a), Arch. Rational Mech. Anal. 58, 181 (quasilinear symmetric hyperbolic systems), and Kato (1975b),
    Lecture Notes in Math. 448, 25 (the abstract theorem for quasilinear evolution equations, with spaces X ⊃ Y and an
    isomorphism S).
  - The symmetrisable, pseudo-differential form: Taylor, PDE III, ch. 16 §2 ("Symmetrizable hyperbolic systems") and §3
    (second-order systems).
- **Conclusion of the theorems.** Local existence, uniqueness and continuous dependence in H^s, s > n/2 + 1 = 5/2, for
  data in an open state set O.
- **Hypotheses, each with its evidence.**
  - **K1 — state set and coefficient smoothness.** O = {N > 0, gamma > 0}. The F2a Lagrangian density is a quadratic form
    in the first jets of g, with coefficients rational in (g_mu nu, N, sqrt gamma). So the principal coefficients depend
    on g only, not on its derivatives, and the lower-order terms are quadratic in the derivatives of g with smooth
    coefficients.
    - Certified by a symbolic frozen background with N, one shift component, and a non-diagonal 2 x 2 block of gamma
      left as symbols: every entry of the F2a symbol has a denominator that is a product of powers of N and det gamma
      (and sqrt det gamma).
    - Disclosed fall-back: if this is computationally infeasible, the reduction actually used is disclosed.
  - **K2 — symmetriser.** S1 + S2.
  - **K3 — Sobolev index.** s > 5/2. The admissible s-range is reported after K4.
  - **K4 — lower-order terms.** The gravitational lower-order terms are smooth by K1. For the MOND/filter terms, each of
    the following is computed and reported:
    - **K4a, the explicit bound.** On {y >= y_min}, the frozen linearised MOND block e^{-xi^2 k^2} k^T C k (and the
      U-elimination Schur complement 2 C E/(1 + C E) k^2) obeys
      ||T u||_{H^{r+m}} <= C_max(y_min) M_m(xi) ||u||_{H^r}, with M_m(xi) = sup_k k^2 (1 + k^2)^{m/2} e^{-xi^2 k^2}.
      M_0 = 1/(e xi^2) is checked in sympy, and M_1, M_2 numerically. C_max(y_min) = max over y >= y_min of
      max(C_T, C_L) for nu_mono, tabulated at y_min in {1e-1, 1e-2, 1e-4, 1e-6}, together with its divergence law
      (~ y_min^(-1/2)).
    - **K4b, the C-H lapse terms.** On the U-shell they are H_CH = 2|D chi|^2 + 2 alpha_M^2 q_b - lambda_0, with
      chi = U - ln N solving D.(N D chi) = -N lambda_0/4. These are lower order (chi gains two derivatives over
      lambda_0). The algebraic identity H -> H_CH on the U-equation is checked in sympy.
    - **K4c, the regularity of nu_mono at its splice y\*.** One-sided derivatives are compared. The splice is expected
      to be C^{1,1}: C_T and C_L continuous, dC_L/dy jumping (XC4 S5). If so, C_T composed with a smooth y lies in
      H^{5/2 - eps}. The C-H stress P_ij is then in H^{s-1} only for s < 7/2, which gives the admissible range
      s in (5/2, 7/2) for the ν_mono-as-defined kernel. With a C-infinity splice (the recipe's open "smooth max"
      variant) the range would be any s > 5/2.
    - **K4d, the zero-field set (disclosure).** Write Z_0 = {D S U = 0}. On a closed leaf, a single-valued U has
      max/min points of S U, so Z_0 is non-empty: at least 2 points, and at least 4 on T^3 (Lusternik–Schnirelmann).
      A numerical illustration (Newton refinement of a critical point of a random smooth periodic S U) is
      non-load-bearing.
      - The scope "data away from zero-field regions" is therefore non-empty on closed leaves only for U with
        non-trivial periods (D U closed but not exact). That is an extension of the field space, like the domain
        extension in FULL_VARIATION.md §2.
      - Otherwise the isolated-zero regularity (XC2 B7) must be ASSUMED. Each status is reported as found.

### S4 — The elliptic lapse and the mixed system

- **S4a, the nonlinear lapse equation, derived from the action.** In unitary gauge, with lambda = 1 + c_2 and beta = 0:

      E_N = R^(3) - (K_ij K^ij - lambda K^2) + alpha_c a_i a^i - 2 alpha_c Delta_gamma N / N - 2 Lambda - 16 pi G rho_N + H_CH = 0,

  with H_CH from FULL_VARIATION.md. With N = w^2 this is 4 alpha_c Delta w / w + (K.K - lambda K^2) = R^(3) - 2 Lambda
  - 16 pi G rho + H_CH.
  - In Hamiltonian variables (momenta fixed) it is linear in w: -4 alpha_c Delta w + V w = 0.
  - In Lagrangian variables (velocities fixed) it is Lichnerowicz-type, with K = E/(2 w^2).
  - Sympy checks:
    - (i) the variational identity for alpha sqrt(gamma) |D N|^2 / N on a conformally flat leaf with arbitrary N and
      psi (euler_equations);
    - (ii) the substitution identity 2 Delta N / N - |D N|^2 / N^2 = 4 Delta w / w;
    - (iii) the minisuperspace (Bianchi I) variation of the kinetic term;
    - (iv) the FLRW reduction (9 lambda - 3) H^2 / N^2 = 2 Lambda + 16 pi G rho, i.e. G_cos / G = 1/(1 + 3 c_2/2).
      This must agree with L340 P1's "|G_cos/G_N - 1| ~ 1.5 c_2" to first order in c_2;
    - (v) the linearisation about flat space reproduces CFG292's lapse coefficients: physical / F2b alpha/2, F2a
      (2 alpha - 1)/4. The gauge-term contribution comes from C_i containing -d_i ln N.
- **S4b, uniform ellipticity on the window.**
  - The physical lapse operator has principal coefficient 4 alpha_c > 0, with alpha_c >= 9.624e-14 on the window.
  - The F2a lapse operator has principal coefficient (1 - 2 alpha_c)/4, which needs alpha_c != 1/2.
  - The joint leaf system (N, chi) has a triangular principal symbol, elliptic iff alpha_c != 0.
  - The general-background formula is S1c item 1.
- **S4c, the kernel.**
  - **(Ham)** In Hamiltonian form the equation is homogeneous in w, so a trivial kernel is impossible.
    - The claim to be certified: the kernel is exactly span{w}, w > 0 being the simple ground state of
      -4 alpha_c Delta + V for any bounded V (Krein–Rutman; no sign condition). This is the tau -> f(tau) relabelling
      mode.
    - Solvability is the global constraint lambda_1(-4 alpha_c Delta + V) = 0. This is the first-class global part of
      the scalar constraint (Donnelly & Jacobson 2011, PRD 84 104019: "linear in the square root of the lapse"; quoted
      PROVISIONALLY).
    - Numerical certification on periodic 2-D finite-difference leaves, with 3 random, sign-indefinite smooth
      potentials at three effective stiffnesses:
      - (a) the lowest eigenvalue is simple (positive gap to the second);
      - (b) the ground state has one sign;
      - (c) after the shift by lambda_1 the null space is exactly 1-dimensional;
      - (d) fixing the mean of w gives a unique solution.
    - Disclosed: the localisation of w as alpha_c -> 0 (Agmon rate). Uniform positivity of N therefore requires the data
      to satisfy V = O(alpha_c), i.e. the GR-like Hamiltonian constraint, to that accuracy.
  - **(Lag / F2a)** This is the operator F2a's second-order scheme actually inverts, with the velocities fixed.
    - The exact lapse Hessian h(k) is computed with sympy on homogeneous flat-leaf Bianchi I backgrounds: lapse N_0,
      gamma = diag(a_i^2), velocities a_i dot, shift 0, the full nonlinear C_i, matter = Lambda + dust (at rest and
      moving in the khronon frame) + a homogeneous scalar field. Both forms are computed:
      - physical: alpha_c |k|^2 + W;
      - F2a: (alpha_c - 1/2) |k|^2 + W.

      Here W, the zeroth-order part, is derived and then rewritten with the background lapse equation.
    - Sign condition for a trivial kernel of the F2a operator (maximum principle): W <= 0, W not identically 0. It is
      checked for FLRW + Lambda + comoving dust at every c_2 of the 18 points. The derived general form of W (including
      khronon-frame-moving matter) is reported as found.
    - For the physical form, the zero of alpha_c |k|^2 + W at |k|_*^2 = -W/alpha_c (a resonance) is reported, as
      k_*/H over the window.
    - For general inhomogeneous data W has no definite sign. Invertibility is then an open condition on the data, and
      is stated as such.
- **S4d, linearised constraint propagation.**
  - Spatial gauge generators Z(xi) (zeta^0 = 0) satisfy Z^T P_inv = 0, with P_inv = the EH + khronon symbol in unitary
    gauge. So on solutions of the reduced system the de Donder vector C obeys (M_C Z)^T C = 0. Here M_C Z(xi) is the
    3 x 3 constraint-propagation symbol.
  - Certified on the aligned background and on the S1c set-2 backgrounds:
    - Z^T P_inv = 0 exactly;
    - det(M_C Z) is proportional to (light cone)^3, with complete eigenvectors (strongly hyperbolic constraint
      subsystem).
  - The nonlinear propagation (Noether identity of foliation-preserving diffeomorphisms + uniqueness for the linear
    constraint system) and the propagation of the global constraint are ASSUMED, stated, and not computed.
- **S4e, the mixed-system theorem.**
  - Andersson & Moncrief 2003 (Ann. Henri Poincaré 4, 1: "locally strongly well posed" in the CMC + spatial-harmonic
    gauge; abstract quoted provisionally) is mapped item by item:
    - AM1 closed Cauchy surface, H^s x H^{s-1} data, s > n/2 + 1;
    - AM2 CMC slicing;
    - AM3 spatial harmonic coordinates with an elliptic shift;
    - AM4 the lapse equation uniformly elliptic with a trivial kernel;
    - AM5 the elliptic variables lower order: the lapse source contains no second derivatives of the hyperbolic
      variables, so N is in H^{s+1};
    - AM6 strong/symmetric hyperbolicity of the reduced evolution;
    - AM7 coefficients smooth in the fields;
    - AM8 gauge and constraint propagation;
    - AM9 the elliptic–hyperbolic iteration theorem itself.
  - Each item gets exactly one status: VERIFIED (by a computed check here), ASSUMED (named, not computed), or FAILED
    (with the computed reason, and the replacement if one exists).
  - AM5 is decided by computation: compare det P_rr (the lapse frozen at principal order) with det P_red (the lapse
    eliminated). If they differ, the lapse is coupled at principal order and AM5 FAILS for C-H/K.
  - The replacement route to be assessed: Kato's abstract theorem (1975b) applied to the lapse-reduced
    pseudo-differential system, with the S2 symmetriser. Its remaining analytic inputs are named as ASSUMED: the
    commutator and paraproduct estimates for the nonlocal lapse solve with H^s coefficients, and continuous dependence
    in the top norm across the ν_mono splice.

## 3. Controls (each can fail; a misbehaving control makes the verdict OPEN)

- **C-GRa: GR in full harmonic gauge** (Choquet-Bruhat; the same Lagrangian machinery, CFG292's C1 symbol).
  - S1: one family ±1, multiplicity 10, with (M^2 - 1) = 0 exactly.
  - S2: H from P_{±1} = ±(M ± 1)/2 is positive definite and H M is symmetric.
  - Must pass.
- **C-GRb: GR in CMC + spatial harmonic gauge** (the Andersson–Moncrief case).
  - Hyperbolic part: (gamma, k) with the lapse and shift lower order, symbol -(lambda - X.k)^2 + N^2 |k|^2_gamma times
    I_6.
  - Lapse: -Delta N + (k_ij k^ij + matter) N = -d_t tau, with source free of second derivatives of gamma once the
    Hamiltonian constraint is used.
  - Required:
    - S1, S2 pass;
    - S4c: the potential is >= tau^2/3 > 0 for tau != 0, so the kernel is trivial (numerically, random k with
      tr k = tau on a periodic grid);
    - S4e: AM5 is VERIFIED (no R^(3) in the lapse source), so every AM item that the computation decides is VERIFIED.
  - Sub-probe, pre-registered to FAIL the trivial-kernel check: maximal slicing with k = 0 (time-symmetric vacuum data),
    where the kernel is the constants. If that sub-probe passes, C-GRb fails.
- **C-H0: minimal Horava** (alpha_c = 0, beta = 0, c_2 = c2_max of P1). It must FAIL S1 or S2:
  - the scalar leading matrix is singular, so the pencil degree is < 2n and there is an eigenvalue at infinity
    (c_S = infinity);
  - so no companion M and no symmetriser.

  S4b must also fail for the physical lapse (principal coefficient 4 alpha_c = 0).
- **MUTATE (env MUTATE=1, separate *_MUTATE outputs, rc = 1 required).** The 18 points are replaced by 9 points on the
  crossing locus alpha = c_2/(1 + 2 c_2), i.e. c_S = 1, for the 9 record c_2 values, plus 9 points at
  alpha = 1.01 x that.
  - S1 must FAIL:
    - the interval box over these points contains c_S = 1;
    - the multiplicity of the eigenvalue +1 is 9 on the locus and 8 off it.
  - S2 must FLAG: the projector denominators (1 - c_S^2) vanish. The symmetriser built from the merged eigenvalue's
    projector at c_S = 1 is compared with the limit of the S2 construction as c_S -> 1, and the jump is reported.
  - Disclosed in advance: at exactly c_S = 1 the merged eigenvalue is semisimple (CFG292 C5), so strong hyperbolicity
    survives there. What fails is the constant-multiplicity family split (8, 1) and the uniformity of the gap.

## 4. Decision rule (recipe §6 vocabulary, exactly one)

- **KILL** if, with the controls behaving, any of the following holds at a record point or on W_rec:
  - S1 fails: a crossing, a non-semisimple eigenvalue, or a failed lapse elimination;
  - S2 fails: H not positive definite, or H M not symmetric;
  - the physical lapse ellipticity fails.
- **OPEN** if any of the following holds:
  - a control misbehaves;
  - S1 and S2 pass, but an AM / replacement hypothesis is FAILED with no replacement route whose hypotheses can be stated;
  - no s > 5/2 makes the MOND forcing bounded in H^{s-1};
  - S4c yields no non-empty data class with an invertible lapse operator (modulo the relabelling mode).
- **CONDITIONAL** if all of the following hold:
  - S1 and S2 pass on W_rec (all 18 points, all directions, all backgrounds);
  - S3 leaves a non-empty s-range;
  - S4b passes;
  - S4c yields a non-empty data class with an invertible lapse operator (mod the relabelling mode);
  - every AM item is VERIFIED, or ASSUMED (named), or FAILED with a replacement whose remaining inputs are named as
    ASSUMED;
  - the controls behave.

  The CONDITIONAL verdict must list every condition and every assumption. Mandatory scope label: local in time; data
  away from zero-field regions (with the K4d status); beta = 0; F2a on the khronon's leaves.
- **PASS (local-in-time scope)** only if all of CONDITIONAL holds and no item is ASSUMED. Recorded in advance; it is
  not expected, because the pseudo-differential commutator estimates and the nonlinear constraint propagation are not
  computed here.

## 5. Wording and scope rules

- Never "theory closed", "well-posed theory", "data favour the framework" or "kappa derived".
- Per recipe §11: "no ill-posedness in the tested sector and scope". Local well-posedness is claimed only as the stated
  verdict, with its conditions.
- Lean (optional): it certifies algebraic inequalities only, such as the S1b gap on W_rec, the projector-sum bound
  v^T H v >= |v|^2/4, and the sign facts of S4. It never certifies the analysis theorems.
- Literature quotations came through summarised abstract pages and are PROVISIONAL. The results here do not depend on
  their wording; every algebraic statement is computed.
- No personal names or home paths in any file. The orchestrator re-runs and commits the lane.

---

## Appended 2026-10-02, after the run (the frozen text above is unchanged)

Eight disclosures. None of them changes a test or the decision rule.

1. **S1c item 4.** det P_red(lambda) was certified through the companion linearisation, det P_red = det(A) det(lambda - M).
   - det A != 0 was checked exactly.
   - det(lambda - M) was compared exactly with [(lambda - nu)^2 - rho]^8 [(lambda - nu)^2 - c_S^2 rho].
   - The identity is equivalent to the frozen one, and avoids a 9 x 9 polynomial determinant per case.
2. **S2c.** The denominators of H(khat = z) are alpha, 2 alpha - 1, alpha - 2, c_2 and 2 + 3 c_2.
   - The factor 2 + 3 c_2 was not among the S1d loci. Its zero, c_2 = -2/3, is the pole of c_S^2, and it misses W_rec.
   - No (c_S^2 - 1) factor survives. This is a finding, reported as found.
3. **The crossing (MUTATE and the normal-run preview).** Approaching c_S = 1:
   - the family projectors stay bounded (||P_j||_G ≈ 1.30) and converge;
   - the four-projector H has a finite limit that still symmetrises M at the crossing (residual 9e-9 at distance 1e-8);
   - that limit differs from the merged-eigenvalue construction by 1.54 in relative norm. The frozen text asked for this
     jump to be reported, and it is.

   The S2 flag is the vanishing projector denominator, as frozen. Reading as found: the crossing defeats Kreiss's
   constant-multiplicity hypothesis and the Lagrange formula, not the existence of a continuous symmetriser.
4. **K4a.** M_1 and M_2 come from the closed-form maximiser t^2 = (m + sqrt(m^2 + 16))/4, cross-checked on a grid. This
   replaced mpmath's findroot, which failed to converge in the first debug run.
5. **S4e under MUTATE.** AM6 cannot be certified once S1 fails, so the S4e check fails in the MUTATE run as well. This is
   an expected consequence of the crossing, not a separate defect.
6. **S4c (Ham), item (c).** "Null space exactly 1-dimensional" was implemented as follows: the smallest |eigenvalue| of
   L - lambda_1 is below 1e-8, and the second smallest exceeds 1e3 times it. The spectral gaps found (0.13 to 15.7) are
   resolved with a wide margin.
7. **S1b wording.** The printout labels the corner value as "c_S - 1 at the minimising corner". It is the minimum gap
   when positive; under MUTATE it is negative, because the box then contains c_S < 1.
8. **Debug runs.** Three debug runs, writing to a scratch directory, preceded the recorded runs. They corrected:
   - a min/max slip in the S1d "nearest point" printout;
   - the K4a root-finder;
   - an S4e polynomial root-finder (now roots factor by factor);
   - the crossing reading text and its convergence test (relative, geometric), together with item 3 above.

   No criterion, threshold or decision rule was changed.
