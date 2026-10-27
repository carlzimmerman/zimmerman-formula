# Independent audit: FSP-005 angular connection

**Normalized claim.** For the actual static charge-one SU(2) BPS Cartesian gauge Hessian, smooth Cartesian origin, each integer J>=6 and each magnetic component, the reduced regular DN matrix satisfies (4.2), (5.2)-(5.5); the actual relative 9D+3R wall and its neutral Schur map satisfy (6.1)-(6.4). Relative to the Friedrichs exact diagonal Coulomb DN matrix, (7.3)-(7.5) hold. With the two regular matrices normalized by Y(2)=Y_0(2)=I, their complete relative-wall determinant quotient has a connection constant |c_J|<38 and remainder (8.4). The superalgebraic remainder is uniform for J>=kappa sqrt(R); a degeneracy-weighted finite expanding band kappa sqrt(R)<=J<=Lambda R has vanishing summed remainder.

**Primary verdict: proved as written**, for this normalized claim and the explicit J and radius ranges of its individual statements. This is an independent proof audit of the raw derivation, with a pre-target DN/Riccati reconstruction. It is not a proof of the parent physical determinant or a canonical Frobenius connection bound.

## Exact target, hypotheses, and independence

Target: `fine_structure_puzzle/qcd_closure/angular_connection/RAW_DERIVATION_v1.md`, checkpoint AC-005-001, SHA256 `f68d03648f040637f983aba3abf3d6a1e88204cb6d5aeee5f17e3344248bed81`; current and declared base Git revision `9516ee01c79f35c04b7556050669ba77b0c98b99`. Author scientific files were not modified.

Before opening the target, this reviewer saved `INDEPENDENT_DN_RICCATI_PRETARGET_v1.md`, SHA256 `c063db634a514dcf2bc9ece40598bdac0013d67c18918414a401b08443daf759`. Only the general lower/upper potential hypotheses and the requested review scope were supplied. That reconstruction independently obtained a usable lower bound P>=(1/8)(J/R+Q), an upper bound P<=a/R+Q with a(a-1)=B, and the ordered noncommuting Riccati variation formula. The target, its operator dependencies and computation code were then read; the author's self-verdict was read only after the mathematical audit was substantially complete.

The coefficient space is the complexification of the angular orthonormal real fluctuation space, dimension 12 per magnetic component for J>=2; all inequalities are Hermitian quadratic-form inequalities. Q is a fixed-in-r angular orthogonal projector, although it depends on angular position before angular reduction. The origin is the actual smooth/Friedrichs form closure, not an arbitrary positive Riccati initial condition. The wall projectors act on the actual spatial fluctuation index and retain A4 Dirichlet data.

## Dependency graph

1. Actual Cartesian A, Phi, D and H -> covariant angular Laplacian A(K) and curvature E, equations (2.1)-(2.3). **Internal operator calculation.**
2. Exact profiles -> 0<c<=b<=r^-2 and h>=1/2 on [2,infinity); active 2 tensor 3 curvature algebra -> -4b<=E<=2b. **Internal scalar inequalities and finite matrix algebra.**
3. Actual coupling J=L+T+S -> L and G ranges -> centrifugal coercivity (4.2). **Internal representation calculation.**
4. Coercivity + regular form domain -> invertible regular value matrix, zero origin Wronskian, Hermitian variational P -> charge-sensitive scale comparison. **Internal ODE/form proof.**
5. [P_N,Q]=0 + scale comparison -> triangular actual wall -> positive three-normal block -> charged-normal elimination and neutral Schur bound. **Internal block algebra.**
6. Exact far operator -> regular Coulomb comparison P_0; exact profile subtraction -> e_J; ordered Riccati transport -> epsilon_J and eta_J. **Internal proof; far spectrum also reconstructed from the frozen Pauli/monopole calculation.**
7. Trace identity + integrable Riccati error + actual Robin normal determinant -> fixed-core determinant connection and remainder. **Internal proof.**
8. The 120-component frozen J1 check corroborates operator signs; it does not supply Steps 3-7. **Exact finite computation, audited separately below.**

No whole-space kernel/index theorem, functional-determinant theorem, heat-kernel theorem, or other external theorem is a load-bearing leaf of this particular claim. The determinant in Step 7 is the explicitly defined finite matrix boundary determinant. No source verification is needed for a theorem that the proof does not invoke.

## Obligation matrix

| Obligation | Status | Decisive check |
|---|---|---|
| Actual Cartesian Hessian, including curvature sign | passed | Direct derivation below and pinned J1 crosscheck |
| Global profile bound c<=b | passed | Numerator in (3.1) bounded below by zero using two globally valid inequalities |
| Actual angular L/G ranges and J=6 endpoint | passed | Triangle inequalities with T=1, S=0 or 1; remainder at J=6 is 5(1-K)^2 |
| Quantitative form coercivity, rather than kernel counting | passed | Explicit a_J=(J-1)(J-2)>0 and upper B_J |
| Regular DN definition, Hermiticity and invertibility | passed | Integration by parts, zero origin Wronskian, strict Dirichlet form |
| Neutral and charged DN scales | passed | Completed square and separate fixed-Q trial functions |
| Moving relative wall and normal +1/R shift | passed | Actual reduced Robin functional u'+u/R; no scalar wall substitution |
| Neutral Schur coefficient as J/R tends to zero | passed | Variational characterization of an SPD Schur complement in scaled coordinates |
| Noncommuting Riccati subtraction/transport | passed | W'=E-PW-WP_0 and ordered left/right propagators |
| Error constants and uniform angular bands | passed | Explicit independent bounds and integral splits below |
| Fixed-core determinant connection and c_J | passed | Integrated epsilon kernel and normal Robin determinant estimate |
| Canonical Frobenius connection singular values | not addressed | Explicitly outside the target; fixed-core determinant bounds do not imply them |
| Full infinite angular sum and UV removal | not addressed | Pointwise eta estimate is not a summable angular bound |
| Physical QCD normalization or alpha | out of scope | No physical same-holonomy/charge matching is established here |

## Decisive analytic reconstruction

### Actual operator and coercivity

From the given Cartesian connection, D_i Phi=c e_i+(b-c)n_i n with b=h' and c=Kh/r. At n=e_3 the anti-self-dual curvature sign is F_12=-b n, F_i4=D_i Phi, agreeing with F_mu,nu=-I_a,mu,nu D_a Phi. Because sigma=-iI and T=i ad, 2 sigma T=2I ad. Thus the curvature term is exactly -2ad F, with the sign in (2.2).

The covariant angular momentum is Lambda=L+(1-K)(T-nT_n). Summing the derivative term gives L dot(nT_n)=0, and its adjoint is (nT_n) dot L=0. Squaring therefore gives (2.1), with no assumed commutation between Q and L^2 or G^2. The convex coefficients K and 1-K are nonnegative, so their separate angular spectral bounds may be inserted as form inequalities.

The active curvature matrix has one-dimensional end blocks 2b and two 2-by-2 blocks with diagonal entries 0,-2b and off-diagonal magnitude 2 sqrt(2)c. This gives the three eigenvalues in (3.2), each with multiplicity two. Their extremal bounds are -4b and 2b when c<=b. The scalar proof of c<=b is global: sinh(t)^2>=t^2+t^4/3 and tanh(t)>=t-t^3/3, the latter following from derivative t^2-tanh(t)^2>=0.

Combining the actual L/G ranges yields

 V_J >= [(J-1)(J-2K)-5(1-K^2)]/r^2+h^2Q.

The difference from (J-1)(J-2)/r^2 is (1-K)[2(J-1)-5(1+K)], nonnegative at and above J=6. The upper bound follows by dropping the negative scalar and Q terms in the convex angular expression and using E<=2/r^2. The J=3,4,5 minima stated in the raw proof are also correct, but they are not used to enlarge its DN theorem.

### Variational DN bounds and actual wall

With p=J-1, completing the square gives

 integral (|u'|^2+p(p-1)|u|^2/r^2) >=p|u(R)|^2/R.

The origin endpoint term vanishes in the regular form closure. Coercivity also excludes a nonzero regular solution with zero value at R, and the zero origin Wronskian makes Y'Y^-1 Hermitian. Completing the form around the regular solution proves the variational minimum.

For beta(beta-1)=B_J the neutral trial (r/R)^beta has energy beta/R. The charged trial (r/R)^beta exp(r-R) satisfies w''/w=B_J/r^2+1+2beta/r, so its energy for the comparison potential is at most beta/R+1. Fixed Q permits adding these two trials without cross terms. This proves (5.3).

The half-form split in (5.4) is legitimate: no kinetic energy is counted twice. The free-left-endpoint DN energy for -d^2+1/4 on [2,R] is (1/2)tanh((R-2)/2). The additional half factor gives c_*=(1/4)tanh(1). Since beta<=J+4 and (J-1)/(2J)>=5/12 for J>=6, the constants in (5.5) follow.

The spatial normal projector and internal charge projector commute before and after angular reduction. In scaled variables the wall is precisely

 [[I,0],[A,B_N]],  ||A||<=5/3,  c_*I<=B_N<=(11/6)I.

The +1/R Robin term contributes at most 1/J<=1/6. For completeness the inverse bound follows from

 ||Btilde^-1|| <=sqrt(c_*^2+(5/3)^2+1)/c_* <8/(3c_*).

The neutral Schur form equals the minimum of the three-normal form over its two charged normal coordinates. This preserves both stated scalar bounds. Eliminating charged Dirichlet coordinates first is exact because their block is the identity. The residual neutral off-diagonal bound is finite; for example (5/3)(1+(11/6)/c_*) is a usable bound. None of this assumes P commutes with Q or P_N.

### Coulomb comparison and ordered Riccati transport

The far operator is diagonal after a constant angular isometry. The frozen higher-angular Pauli identities give l=J-1,J,J,J+1 in each charge, and the ordinary spatial-vector/A4 decomposition gives the same neutral list. The charged lower comparison follows from

 1-2/r+l(l+1)/r^2-l(l-1)/r^2=[(r-1)^2+2l-1]/r^2>0.

Its regular/Friedrichs solution therefore gives P_0>=(J-1)/r. The upper comparison has beta_0=J+2. This verifies (7.1) without relying on a pure growing exterior polynomial through its zeros.

An independent norm subtraction gives

 ||A(K)-A(0)||<=2K(J+5),
 ||E_curv-E_curv,0||<=4Kh/r+2K^2/r^2.

For the second line the transverse active matrix sigma_1 T_1+sigma_2 T_2 has norm sqrt(2)<=2. Also K<=3r e^-r and |h^2-(1-1/r)^2|<=6e^-2r on r>=2. The nonangular remainder is bounded by 12e^-r+24e^-2r<16e^-r. These establish the stated e_J, including all charged-neutral mixing.

For W=P-P_0 the exact equation is W'=E-PW-WP_0. If L_P solves L_P'=-P L_P and R_0 solves R_0'=-R_0 P_0, each ordered propagator contracts in Euclidean norm by (s/R)^(J-1). Variation of constants yields (7.3). This argument never treats Z^-1/2 P Z^1/2 as Hermitian. The initial difference bound is the maximum of the positive upper bounds, not their sum: -P_0<=W<=P.

The split at R/2 gives (7.4), since the early interval kernel is at most 2^(-2J+2) and integral_2^infinity e_J<=(3J+31)e^-2. Every term in (7.5) then tends uniformly to zero for J>=kappa sqrt(R), including arbitrarily larger J. This is an upper bound on an individual error, not an infinite-J summation theorem.

### Fixed-core determinant, tail integral and normalization

Restarting (7.3) at R and integrating over t>=R gives

 integral_R^infinity ||W(t)||dt
 <=[R epsilon_J(R)+integral_R^infinity s e_J(s)ds]/(2J-3),

which is exactly (8.2). At R=2, tracing in dimension 12 gives the bound (8.3). Replacing e^-2 by 1/7 yields 12(13J+120)/[7(2J-3)], a decreasing function bounded at J=6 by 264/7<38.

With Y(2)=Y_0(2)=I, log det Y-log det Y_0=integral_2^R tr W, so its limit is c_J. At fixed J, the unsplit formula (7.3) gives epsilon_J(R)=O_J(R^(-2J+2)); this proves that the normal determinant quotient tends to one. The middle term of the looser split bound (7.4) must not be integrated at fixed J.

In the determinant estimate, the comparison block bounded below by J/R is specifically

 B_0=P_N(P_0+I/R)P_N|ran(P_N),

because P_0>=(J-1)/R. Thus the +I/R shift is essential. Equation (8.4)'s phrase “normal DN block” must be read as this already defined normal Robin block from (8.1). No unshifted P_0>=J/R claim is needed. The relative perturbation norm is at most eta_J; three eigenvalues with perturbations in [-eta,eta] give an absolute log determinant bound 6eta when eta<=1/2.

Finally T_J<=J eta_J/(2J-3)+O((1+R/J)e^-R). Therefore the remainder is superalgebraic uniformly in the asserted band. A finite band through Lambda R contains O(R) sectors and O(R^2) total magnetic multiplicity; polynomial counting times the explicit exp(-c sqrt(R)) bound tends to zero.

## Computation and source audit

Outcome: **audited, not executed** for the mathematical checker. No new exact-algebra or ODE run was required. The previously completed finite run was checked by reading its implementation and contract and validating its current pinned input/output hashes.

- Existing code: `angular_connection/check_uniform_v1.py`, SHA256 `bc4f0bf55dd45fc15cda825e03f8ea27a231e50c40b6b32e7349fa27b5c9ed8c`.
- Frozen input: `qcd_completion/higher_angular/inputs_v1/j1_operator.json`, SHA256 `4e98fa28d208693d6559c8bf5b2dd4b1c05e4d5b88827c38fb21230ac645f6bd`.
- Existing manifest: `angular_connection/runs/exact-001/manifest.json`, schema v2, status completed; Python 3.9.6, SymPy 1.14.0, 45-second wall and 1-MiB output caps.
- Existing results: SHA256 `c6ccc35377dc19b2acf32ac58132a027a77e2a17053d83c5081e3516b495d7c1`; 146 checks, including 120 Cartesian component residuals across all ten frozen J1 columns.
- Validation command run by this reviewer: `python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_closure/angular_connection/runs/exact-001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula`.
- Observed result: `valid evidence record (run status: completed); mathematical interpretation requires review`.

The code applies the newly derived operator to actual Cartesian tensors, substitutes the exact BPS derivative identities into the frozen operator, and reduces every residual modulo n.n-1. It uses exact arithmetic and its loops cover exactly the stated ten columns times twelve components. The spherical Laplacian and L dot T implementations have the correct signs. The active curvature polynomial and generic polynomial identities are separately checked. Its finite J1 coverage cannot establish an arbitrary-J theorem: that theorem is supplied by the angular/form arguments audited above. No fresh computation beyond read-only provenance validation is represented as having run.

No external theorem is invoked in the new proof, so the prior index-theorem and singular-origin determinant citations are not new dependencies. In particular, this review does not silently validate those external leaves for other claims.

## Exact remaining obligations and strongest safe use

There is no remaining gap in the normalized claim reviewed here. The parent FSP-005 closure still requires:

1. Restoring the actual canonical regular-origin normalization. If Y_can is the original Frobenius-normalized matrix, then Y=Y_can Y_can(2)^-1, and

   F_can/F_0,can=(F/F_0) det Y_can(2)/det Y_0,can(2).

   The extra ratio can depend strongly on J and is not bounded by 38. It is independent of R at fixed J, but cannot be discarded from a moving angular cutoff or physical normalization without further justification.
2. A matrix connection bound is stronger than a determinant bound: uniformly bounding the determinant does not bound its individual singular values. No such stronger conclusion should be recorded as closed.
3. A common-regulator large-J gauge/ghost subtraction with actual local wall terms, plus origin factors, remains necessary for the full infinite angular product. Uniform smallness over J>=kappa sqrt(R) alone gives no summable angular majorant.
4. The Coulomb Friedrichs comparison is an explicit mathematical comparison; it does not establish a physical same-holonomy vacuum subtraction, nonzero Fourier completion, QCD electromagnetic normalization, or alpha selection.

The strongest safe statement is exactly the J>=6 coercive DN/relative-wall/neutral-Schur theorem plus its fixed-core determinant connection and finite expanding-band remainder. The cheapest next discriminating mathematical check for the parent application is to retain and estimate the canonical origin factors together with a common-regulator large-J symbol subtraction; repeating finite J1 checks would not resolve that obligation.

## Final mathematical proofreading receipt

Self-review covered this new review and the pre-target note for notation, dimensions, signs, exponents, radius ranges, the +1/R shift, and fixed-core versus Frobenius normalization. No author files were edited. Routine edits: none. Mathematical-token changes to audited sources: none. Unresolved mathematical or typographical issue affecting the verdict: none. The phrase “normal DN block” in raw Section 8 is explicitly resolved above by its displayed Robin-block definition.
