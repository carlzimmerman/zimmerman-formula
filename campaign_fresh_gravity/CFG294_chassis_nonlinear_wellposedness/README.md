# CFG294: nonlinear local well-posedness of the relativistic chassis (C-H/K) on the khronon's leaves

**Status (frozen rule): CONDITIONAL, at local-in-time scope.** The conditions and the assumed analytic inputs are listed below.
The criteria were frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit 2821be492. Implementation disclosures
are appended at the end of that file; the frozen text is unchanged.

Say "no ill-posedness in the tested sector and scope", and "locally well-posed under the stated conditions and
assumptions". Never make an unconditional well-posedness claim (recipe §11).

## What was asked

CFG292 showed that the chassis, in formulation F2a, is strongly hyperbolic at all 18 record points. F2a is: khronon time
t = tau, spatial de Donder coordinates with the 4-D trace, and the lapse eliminated through its leaf-elliptic equation.
CFG292 left three things unproven:

- a smooth symmetriser for the quasilinear system;
- constraint propagation;
- an elliptic–hyperbolic coupling theorem.

This lane carries the frozen-symbol result as far as it can be derived from first principles:

1. constant multiplicity;
2. an explicit Kreiss symmetriser;
3. Kato's quasilinear theorem for the hyperbolic part;
4. the elliptic lapse and the mixed system, with Andersson & Moncrief (2003) mapped hypothesis by hypothesis.

The system is L340's C-H/K: I_CH + c^3/(16 pi G) Int sqrt(-g) [alpha_c a.a - c_2 K^2], with beta = 0 and
lambda_K = 1 + c_2. The F2a symbol is built with `cfg292_lib.py`, imported read-only.

- **Record windows.**
  - W_P1 = alpha_c in [9.624e-14, 3.2e-9] x c_2 in [7.289e-3, 0.0667];
  - W_rec = [9.624e-14, 3.2e-9] x [6.310e-4, 0.10]. This covers all 18 points, including the L350 ceilings and the
    recipe edge.
- **Scalar speed.** c_S^2 = c_2 (2 - alpha_c) / (alpha_c (2 + 3 c_2)).
- **What it does not rest on.** It does not rest on CFG292's verdict reading (OPEN literal / CONDITIONAL post hoc).
  S1–S2 re-certify F2a's symbol independently, in exact arithmetic.

## The derivation, step by step

### S1: Constant multiplicity (PASS on W_rec)

**Statement.** Fix any frozen background with N > 0, any shift N^i and gamma > 0. Write nu = N^i k_i and
rho = N^2 gamma^{ij} k_i k_j. Then the characteristic roots of the lapse-reduced F2a symbol are:

- lambda = nu ± sqrt(rho), each with multiplicity 8 (tensor 2, gauge vector 4, gauge scalar 2);
- lambda = nu ± c_S sqrt(rho), each with multiplicity 1 (the khronon scalar).

All four eigenvalues are semisimple. On W_rec the two families never meet.

How each part was certified:

1. **Symbolic, for all (alpha_c, c_2) at once.** The check covers every helicity block (tensor, two vector, and scalar
   after the lapse elimination). Each block's companion matrix M has characteristic polynomial
   (lambda^2 - 1)^m (lambda^2 - c_S^2)^n. Each block also satisfies its minimal-polynomial identity identically as rational
   functions:
   - (M^2 - 1)(M^2 - c_S^2) = 0 in the scalar block;
   - M^2 - 1 = 0 in the vector and tensor blocks.

   Hence M is diagonalisable at every parameter point where the denominators alpha, 2 alpha - 1 and 2 + 3 c_2 are
   non-zero and c_S^2 is not 0 or 1.
2. **Frame covariance gives uniformity in the background.** Every frozen background is the aligned one after a
   leaf-preserving linear frame change: a Galilean shift x -> x + N t, a spatial GL(3), and t -> N t.
   - Under such a change ∂t/∂x'^i = 0. So the spatial de Donder covector, gamma^{ij} and sqrt(-g) transform covariantly,
     and the action density is a scalar density.
   - The lapse direction (h_00 alone) maps to the lapse direction, while the complementary variables mix only among
     themselves. So the Schur complement that eliminates the lapse is also covariant.
   - The general-background check below confirms this numerically.
3. **The gap, by rigorous interval arithmetic** (mpmath.iv, outward rounding; each variable used once, so the interval
   is tight).
   - c_S^2 >= 196 987.6 on W_rec and >= 2 253 116 on W_P1.
   - The minimum is at the corner (alpha_max, lowest c_2), because dc_S^2/d alpha < 0 and dc_S^2/dc_2 > 0 there.
   - Minimum gaps:

     | Window | min c_S | min gap \|c_S − 1\| |
     |---|---|---|
     | W_rec | 443.833 | **442.833** |
     | W_P1 | 1501.04 | **1500.04** |

   - The smallest separation between any two distinct eigenvalues is 2 sqrt(rho) (between +1 and −1), uniformly.
4. **Exact certification.** 432 cases on the aligned background (18 points x 24 exact rational unit directions) and 72
   cases on general backgrounds (6 random rational backgrounds with lapse 3/5 to 7/5, a shift and non-diagonal gamma,
   x 3 corner points x 4 values of k). In every case all of the following hold:
   - P_00,00 is lambda-free and equals (2 alpha - 1) sqrt(gamma) |k|^2_gamma / (4 N^3);
   - P_0r is linear in lambda, so the Schur complement is a quadratic pencil;
   - det A != 0;
   - det(lambda - M) = [(lambda - nu)^2 - rho]^8 [(lambda - nu)^2 - c_S^2 rho];
   - ((M - nu)^2 - rho)((M - nu)^2 - c_S^2 rho) = 0, exactly.
5. **Degeneracy loci, and their distance from W_rec.**

   | Locus | What it is | Distance from W_rec |
   |---|---|---|
   | alpha = 0 | minimal Horava, det A = 0 | 9.6e-14 |
   | alpha = 1/2 | F2a lapse coefficient vanishes | 0.5 |
   | c_S = 1, i.e. alpha = c_2/(1 + 2 c_2) | the families cross | 6.3e-4 |
   | c_2 = 0, alpha = 2 | c_S = 0 | 6.3e-4 and 2 |

   - alpha = 1/2 is a gauge artefact: the physical lapse coefficient alpha_c/2 does not vanish there.
   - The record point nearest the crossing has alpha/alpha_cross = 5.1e-6.

### S2: Symmetriser (PASS)

**Theorem cited.** This is Kreiss (1970), as stated in Kreiss & Lorenz (1989) and Sarbach & Tiglio (2012, Living Rev.
Relativ. 15, 9, §3); Métivier (2014) gives the L^2 theory. A strongly hyperbolic system whose eigenvalues have constant
multiplicity has a symmetriser H(u, xi) with these properties:

- smooth in (u, xi);
- homogeneous of degree 0 in xi;
- uniformly positive on compact sets;
- H M symmetric.

**Construction, explicit.** The spectral projectors come from Lagrange interpolation in M' = (M - nu)/sqrt(rho):

- P_{±1} = ± R (M' ± 1)/2, with R = (M'^2 - c_S^2)/(1 - c_S^2);
- P_{±c} = ± Q (M' ± c_S)/(2 c_S), with Q = (M'^2 - 1)/(c_S^2 - 1).

Then:

    H = Sum_j P_j^T G P_j = 1/2 [R^T G R + M'^T R^T G R M'] + 1/2 [Q^T G Q + M'^T Q^T G Q M' / c_S^2].

This is rational in the data, with no square roots. G is the Frobenius metric on symmetric tensors. Two consequences
follow directly:

- H M' = Sum_j lambda_j P_j^T G P_j is symmetric;
- because Sum_j P_j = I, v^T H v >= |v|^2_G / 4.

| Check | Result |
|---|---|
| Exact, at all 504 S1 cases | H = H^T, H M symmetric, all exact LDL^T pivots > 0. lambda_min(H) = 0.418 everywhere (>= 1/4). kappa(H) = 3.25e5 at (alpha_max, c_2 = 6.31e-4) up to 1.96e12 at (alpha_min, c_2 = 0.1); up to 1.4e13 on the general backgrounds. kappa(H) <= 4 Sum ||P_j||^2 holds. kappa(H) ≈ 2 c_S^2 ≈ kappa(T)^2/2 of CFG292. |
| Dense directions | 9000 directions (18 points x 500, mpmath 40 digits): relative asymmetry of H M <= 2e-28; kappa(H) direction-independent to 8e-28 (rotation covariance about the aether). |
| Smoothness (symbolic, khat = z) | The denominators of H are alpha, 2 alpha - 1, alpha - 2, c_2 and 2 + 3 c_2. None vanishes on W_rec (interval check). No (c_S^2 - 1) factor survives. Together with S1 item 2, H is real-analytic in (background, khat). |
| Canonical energy (finding) | The Lagrangian energy is **indefinite**: A has inertia (6+, 3−) and C has (3+, 6−). So Hughes–Kato–Marsden's positive-energy hypothesis fails, and the Kreiss symmetriser is what carries the energy estimate. |

### S3: Quasilinear local existence for the hyperbolic part (PASS, with a restricted s-range)

**Theorems cited.**

- Kato (1975a), Arch. Rational Mech. Anal. 58, 181;
- Kato (1975b), Lecture Notes in Math. 448, 25 (the abstract X ⊃ Y theorem);
- the symmetrisable / pseudo-differential form: Taylor, PDE III, ch. 16 §§2–3.

They give local existence, uniqueness and continuous dependence in H^s for s > n/2 + 1 = 5/2. Hypotheses:

- **K1 — VERIFIED.** On a symbolic background (lapse, a shift component, a non-diagonal 2 x 2 block of gamma), every
  entry of the F2a symbol has denominators only N and det gamma. So the coefficients are smooth on O = {N > 0, gamma > 0}.
  - The Lagrangian is a quadratic form in the first jets with g-dependent coefficients: the principal part depends on g
    only, and the lower-order part is quadratic in dg.
  - The lapse coefficient (2 alpha - 1) sqrt(gamma) |k|^2_gamma / (4 N^3) holds symbolically.
- **K2 — VERIFIED.** S1 + S2.
- **K3 / K4c — VERIFIED with a restriction.** ν_mono's splice at y\* = 2.3374 is C^{1,1} and not C^2.
  - C_T and C_L are continuous there, but dC_L/dy jumps from −0.0361 to −0.0014 and d^2C_T/dy^2 jumps by 0.0149.
  - So C_T(y(x)) is in H^{5/2-ε}: its Fourier envelope falls as k^{−2.98}. The splice-free ν_RAR control instead drops
    to round-off (2e-18).
  - The C-H stress P_ij ~ C_T w w is therefore in H^{s-1} only for s < 7/2. **Admissible s ∈ (5/2, 7/2).** A
    C-infinity "smooth max" splice (left open in the recipe) would remove the upper end.
- **K4a — VERIFIED where the filtered field is non-zero.** On {y >= y_min} the linearised MOND/filter block and the
  U-elimination Schur complement are bounded lower-order operators:

      ||T u||_{H^{r+m}} <= C_max(y_min) M_m(xi) ||u||_{H^r}

  - M_0 = 1/(e xi^2) (sympy). At xi = 1, M_1 = 0.537 and M_2 = 0.840.
  - C_max(y_min) = C_T(y_min) takes the values 2.69, 9.51, 99.5 and 999.5 at y_min = 0.1, 1e-2, 1e-4 and 1e-6.
  - C_max sqrt(y_min) -> 1, so the constant diverges as y_min^{-1/2}, and only at zero field.
  - The excluded set is Z_0 = {D S U = 0}.
- **K4b — VERIFIED.** On the U-equation shell, the C-H lapse derivative of FULL_VARIATION.md is
  H_CH = 2|D chi|^2 + 2 alpha_M^2 q_b - lambda_0, with chi = U - ln N and D.(N D chi) = -N lambda_0/4.
  - No second derivative of N survives, so the C-H sector enters the lapse equation at lower order.
  - chi gains two derivatives over the heat-smoothed lambda_0.
- **K4d — disclosed.** On a closed leaf a single-valued S U has critical points: at least 2, and at least 4 on T^3. So
  Z_0 is never empty. A Newton refinement on a random periodic field reaches |D S U| = 6e-18.
  - "Data away from zero-field regions" is therefore non-empty on the ACTION.md domain only for U with non-trivial
    periods (D U closed but not exact). That extends the field space, as FULL_VARIATION.md §2 also does.
  - Otherwise the isolated-zero regularity must be assumed (A5).

### S4: The elliptic lapse and the mixed system

**S4a. The lapse equation, derived from the action** (unitary gauge, beta = 0, lambda = 1 + c_2):

    E_N = R^(3) - (K_ij K^ij - lambda K^2) + alpha_c a_i a^i - 2 alpha_c Delta N / N - 2 Lambda - 16 pi G rho_N + H_CH = 0.

With N = w^2 it takes two forms, depending on what is held fixed:

- **Velocities fixed (Lagrangian, Lichnerowicz-type):**
  4 alpha_c Delta w = w [R^(3) - 2 Lambda - 16 pi G rho + H_CH] - N^2 (K.K - lambda K^2) w^{-3}.
- **Momenta fixed (Hamiltonian, linear in sqrt N):**
  -4 alpha_c Delta w + V w = 0, with V = R^(3) - (K.K - lambda K^2)[pi] - 2 Lambda - 16 pi G rho + H_CH.

  This matches Donnelly & Jacobson (2011, PRD 84 104019; quoted provisionally): "linear in the square root of the
  lapse", with a first-class global part that generates time reparametrisations.

Sympy checks:

- the alpha-term variation on an arbitrary conformally flat leaf;
- the w-substitution identity;
- the kinetic variation;
- the FLRW reduction (9 lambda - 3) H^2/N^2 = 2 Lambda + 16 pi G rho, i.e. G_cos/G = 1/(1 + 3c_2/2). This agrees with
  L340's 1.5 c_2;
- the linearisation reproduces CFG292's committed lapse coefficients alpha/2 (physical) and (2 alpha - 1)/4 (F2a). The
  F2a gauge term contributes -1/4 because C_i = -d_i ln N exactly.

**S4b. Uniform ellipticity — VERIFIED on W_rec.**

| Operator | Principal coefficient | On W_rec |
|---|---|---|
| Physical (w-form) | 4 alpha_c | >= 3.85e-13 > 0 |
| F2a | \|2 alpha_c - 1\|/4 | >= 0.2499999984 |
| Joint (N, chi) leaf system | triangular, det = 4 N alpha_c k^4 | elliptic iff alpha_c != 0 |

**S4c. Kernel and the sign condition.**

- **Hamiltonian form.** A trivial kernel is impossible by symmetry (tau -> f(tau)). What holds instead, and needs **no
  sign condition**, is the following.
  - The kernel is exactly span{w}, where w > 0 is the simple ground state of -4 alpha Delta + V for any bounded V
    (Krein–Rutman). This is the relabelling mode.
  - Solvability is the global constraint lambda_1 = 0.
  - Fixing the clock calibration <w> makes the solution unique.
  - Certified on periodic finite-difference leaves for 3 sign-indefinite potentials x 3 stiffnesses (9/9): simple lowest
    eigenvalue, one-signed ground state, 1-dimensional null space after the shift, unique bordered solve.
  - *Disclosed:* as alpha_c -> 0 the ground state localises (Agmon slope 0.197). At alpha_c = 3.2e-9, keeping
    N_max/N_min <= 10 needs the GR-like Hamiltonian-constraint violation to satisfy dV L^2 <= 1.1e-7. A unit violation
    gives ln(N_max/N_min) ~ 7e3. Uniform positivity of N thus requires data that satisfy that constraint to O(alpha_c).
- **Lagrangian form, i.e. the operator F2a's scheme inverts** (velocities fixed). It was computed exactly on Bianchi-I
  flat-leaf backgrounds with Lambda, dust (comoving and moving in the khronon frame) and a scalar field:

      h_F2a(k) ∝ (alpha_c - 1/2) |k|^2_gamma + W,   h_phys(k) ∝ alpha_c |k|^2_gamma + W,
      W = -2 Lambda - 16 pi G V(phi) - 8 pi G rho_rest (2 - 3u^2)/(1 - u^2)^{3/2}.

  The background lapse equation is used to rewrite W. The scalar field's kinetic energy cancels exactly.
  - **Sign condition for a trivial kernel (F2a): W <= 0, W != 0.**
    - It **holds** for FLRW + Lambda + comoving dust at every c_2 of the 18 points (W = -(2 Lambda + 16 pi G rho)).
    - Vacuum (Kasner-type) gives W = 0: the k = 0 mode is the relabelling mode, quotiented as above.
    - Dust faster than sqrt(2/3) in the khronon frame makes its term positive.
  - The physical velocity-fixed form vanishes at (k_*/a)/(H/N) = sqrt((6 + 9 c_2)/alpha_c) ∈ [4.3e4, 8.5e6], a
    resonance. F2a has none when W < 0.
  - On general inhomogeneous data W has no definite sign, and invertibility is an open condition near the homogeneous
    class.

**S4d. Linearised constraint propagation — VERIFIED at symbol level.** Checked on the aligned background and two general
backgrounds:

- spatial diffeomorphisms annihilate the EH + khronon symbol;
- M_C Z = (g^{mu nu} xi_mu xi_nu) gamma_ij;
- Z^T P_gf = -sqrt(-g) (M_C Z)^T gamma^{-1} M_C.

So on solutions of the reduced system (g^{mu nu} xi xi) C_i = 0, a light-cone, complete, strongly hyperbolic constraint
subsystem. C = 0 at t = 0 is a choice of initial shift velocity; d_t C = 0 at t = 0 is the momentum constraint.

**S4e. Andersson & Moncrief (2003), item by item.** The abstract is quoted provisionally: "locally strongly well posed"
in CMC + spatial harmonic gauge.

| Item | Hypothesis | C-H/K in F2a |
|---|---|---|
| AM1 | closed Cauchy surface, H^s x H^{s-1}, s > n/2 + 1 | **VERIFIED (restricted):** T^3 leaves; s ∈ (5/2, 7/2) (K4c) |
| AM2 | CMC slicing | **FAILED (replaced):** the slicing is forced to the khronon leaves (CFG292 T7); the lapse equation is the khronon's E_N |
| AM3 | spatial harmonic coordinates, elliptic shift | **FAILED (replaced):** F2a's shift is hyperbolic, part of the S1/S2 system |
| AM4 | lapse uniformly elliptic, trivial kernel | **VERIFIED** (ellipticity) / **CONDITION** (kernel): relabelling mode (Hamiltonian form) or W <= 0 (F2a form) |
| AM5 | elliptic variables lower order (no d^2 g in the lapse source; N ∈ H^{s+1}) | **FAILED, by computation.** With the lapse frozen at principal order the scalar roots are ±0.0178 i. With it eliminated they are ±c_S = ±443.8. The lapse source contains R^(3) with weight 1/(4 alpha_c), and no constraint can remove it, because the scalar constraint *is* the lapse equation. Replacement: eliminate the lapse at symbol level, giving a quasilinear pseudo-differential hyperbolic system. |
| AM6 | strong/symmetric hyperbolicity of the reduced evolution | **VERIFIED:** S1 + S2 for the lapse-reduced symbol |
| AM7 | coefficients smooth in the fields | **VERIFIED (restricted):** gravity rational in g (K1); MOND smooth off Z_0, C^{1,1} at the splice |
| AM8 | gauge/constraint propagation | **VERIFIED (linear)** (S4d) / **ASSUMED (nonlinear)** (A2, A3) |
| AM9 | the elliptic–hyperbolic iteration theorem | **FAILED (replaced):** AM's iteration uses AM5. Replacement: Kato's abstract theorem on the lapse-reduced system with the S2 symmetriser; inputs verified K1–K4 (restricted), assumed A1, A4 (+A5) |

So AM does not apply verbatim. No item is left FAILED without a replacement whose remaining inputs are named.

## Controls (all behave)

- **C-GRa, GR in full harmonic gauge.** One family ±1 with multiplicity 10, (M^2 - 1) = 0 exactly. H = (G + M^T G M)/2
  is positive definite and H M is symmetric. PASS.
- **C-GRb, GR in CMC + spatial harmonic gauge (the Andersson–Moncrief case).** The hyperbolic part passes S1 and S2. The
  CMC lapse operator -Delta + |k|^2 has lambda_min = 1.36 >= tau^2/3, so its kernel is trivial. AM5 is VERIFIED: once
  the Hamiltonian constraint is used, the lapse source contains no R. The pre-registered sub-probe (maximal slicing,
  k = 0) **fails** the kernel check as required: lambda_min = 3e-13, kernel = constants.
- **C-H0, minimal Horava (alpha_c = 0).** det A = 0, so there is an eigenvalue at infinity and no companion matrix. S1
  and S2 fail, and the physical lapse ellipticity fails.
- **MUTATE: the 18 points moved onto the crossing c_S = 1 and 1% off it** (`*_MUTATE` outputs, rc = 1; 16/23 checks
  pass, 6 load-bearing failures).
  - S1 fails: the box's c_S^2 interval is [0.0072, 138], which contains 1, and mult(+1) is 9 on the locus instead of 8.
    S1b, S1c and S1d all fail.
  - S2 flags it: the projector denominator 1 - c_S^2 vanishes at the 9 crossing points, so S2a and S2b fail.
  - S4e fails too, because AM6 can no longer be certified.
  - The jump of H across the crossing is reported (see disclosures).
  - The Lean MUTATE file (the same gap theorem on a window reaching the crossing) fails to compile, as required.

## Verdict, scope, conditions, assumptions

**CONDITIONAL.**

**Scope.** Local in time; beta = 0; F2a on the khronon's leaves; data away from zero-field regions (K4d status).

**Conditions** (data or setting; each holds on a stated non-empty class):

| | Condition | Where it comes from |
|---|---|---|
| C1 | beta = 0, 0 < alpha_c < 1/2 (alpha_c != 1/2 is the F2a gauge artefact), c_2 > 0. The whole of W_rec satisfies it. | S1b, S1d |
| C2 | s ∈ (5/2, 7/2) for ν_mono with its C^{1,1} splice; any s > 5/2 with a C-infinity splice. | K4c |
| C3 | The filtered field has no zeros on the leaf. On closed leaves this needs U with non-trivial periods; otherwise A5. | K4d |
| C4 | An invertible lapse operator at the data: F2a's W <= 0, W != 0 (holds on FLRW + Lambda + comoving dust and nearby), or the Hamiltonian form with the relabelling mode quotiented and the global constraint imposed. | S4c |
| C5 | For a lower bound on N that does not degrade as alpha_c -> 0: data obeying the GR-like Hamiltonian constraint to O(alpha_c). | S4c, disclosed |

**Assumed** (named, not computed here):

- **A1.** The pseudo-differential (paradifferential) form of Kato's theorem for the lapse-reduced system: the
  commutator/paraproduct estimates for the nonlocal lapse solve with H^s coefficients. This is standard for symbols
  smooth in xi and H^s in x, but is not verified here.
- **A2.** Nonlinear propagation of C_i = 0 (Noether identity for foliation-preserving diffeomorphisms + uniqueness).
- **A3.** Propagation of the global relabelling constraint.
- **A4.** Continuous dependence in the top norm across the splice level set (it needs the level set to be null).
- **A5.** That isolated zeros of the filtered field do not obstruct the H^s estimates. Needed only for single-valued U
  on closed leaves.

**Why not PASS.** A1–A5 are assumed (the frozen rule's PASS needs none assumed).

**Why not OPEN or KILL.** Every failed AM item has a replacement whose remaining inputs are named, and no
gauge-invariant failure occurred.

## Disclosures

- **The crossing.**
  - At c_S = 1 the merged eigenvalue is semisimple (as in CFG292 C5), so strong hyperbolicity survives there.
  - Approaching it, the family projectors stay bounded (||P_j||_G ≈ 1.30) and converge. The four-projector H has a finite
    limit (no (c_S^2 − 1) factor survives, S2c). That limit still symmetrises M at the crossing (residual 9e-9 at
    distance 1e-8), and differs from the merged-eigenvalue construction by 1.54 in relative norm.
  - So what fails at c_S = 1 is Kreiss's constant-multiplicity hypothesis and the Lagrange formula, which is 0/0 there.
    The existence of a continuous symmetriser does not fail.
  - This is moot for the chassis: the crossing lies 6.3e-4 outside W_rec in alpha, and the record point nearest it is at
    alpha/alpha_cross = 5.1e-6.
- **Size of the constants.** kappa(H) reaches 2e12 on the aligned background, and 1.4e13 on the general backgrounds
  tested at alpha_min. The H^s-energy equivalence constants, and hence the guaranteed existence time, degrade like
  c_S^2 ~ 1/alpha_c. Existence is unaffected.
- **The physical lapse in velocity form** has a resonance at k_* ~ H sqrt(6/alpha_c). The F2a gauge term flips the sign
  of the gradient term and removes it on W < 0 data. On the constraint surface C = 0 the two lapse equations coincide.
- **Literature.** Quotations come from summarised abstract pages and are PROVISIONAL: Andersson & Moncrief 2003;
  Métivier 2014; Donnelly & Jacobson 2011; Kato 1975a. Section titles of Taylor PDE III ch. 16 were taken from the
  author's page. Statements of Kreiss's theorem, Kato's hypotheses and Hughes–Kato–Marsden are from standard references,
  not re-read here. Every algebraic statement used is computed in-lane.
- **Context.** kappa = 1/2 is FITTED and plays no role. Nothing here bears on data. L350 found the plain-K^2 c_2 window
  excluded by Planck-era cosmology; the leaf-average form has the same principal symbol.

## Lean (algebraic core only)

`cfg294_algebraic_core.lean` has 9 theorems, all compiled with standard axioms only:

- the gap c_2(2 - alpha) > 443^2 alpha(2 + 3 c_2) on the whole window, and as a statement about c_S^2;
- the crossing locus, and that it lies outside the window;
- the projector-sum bound ‖Σ x_j‖^2 <= 4 Σ‖x_j‖^2, which gives lambda_min(H) >= 1/4;
- the lapse signs;
- F2a definiteness for W < 0, and the physical resonance;
- the dust threshold.

`cfg294_algebraic_core_MUTATE.lean` (the gap theorem on a window reaching the crossing) fails to compile, as required.
Lean certifies these inequalities only. It does not certify Kreiss, Kato, Andersson–Moncrief or any well-posedness
statement.

## Files

| File | Contents |
|---|---|
| `cfg294_chassis_nonlinear_wellposedness.py` | the lane script (S1–S4, controls, verdict); imports `cfg292_lib.py` read-only |
| `cfg294_chassis_nonlinear_wellposedness.out`, `cfg294_chassis_nonlinear_wellposedness_results.json` | the normal run |
| `cfg294_chassis_nonlinear_wellposedness_MUTATE.out`, `cfg294_chassis_nonlinear_wellposedness_results_MUTATE.json` | the MUTATE run (rc = 1) |
| `cfg294_algebraic_core.lean` / `.out` | Lean certificates |
| `cfg294_algebraic_core_MUTATE.lean` / `.out` | must not compile |

Run from the repository root. Each script run takes about 3–4 minutes and uses up to 16 processes for S2b.

    python3 campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/cfg294_chassis_nonlinear_wellposedness.py
    MUTATE=1 python3 campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/cfg294_chassis_nonlinear_wellposedness.py
    (cd fable_independent_2026/lean_2026 && lake env lean ../../campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/cfg294_algebraic_core.lean)
