# Nonlinear projected-acceleration ADM constraint discriminant

The exact Hamiltonian is linear in the common lapse, but this does **not** make it an arbitrary local multiplier on a nonuniform relative-lapse branch. The mixed functional lapse Hessian is a first-order transport operator. On the lapse equations it has a global clock-relabel null direction and potentially further boundary-dependent kernels. Six Einstein momentum rows remain, and their preservation supplies three relative force rows after the diagonal spatial Ward identity. Their final Dirac classification is not established here.

This is an exact first-stage nonlinear constraint result, including all lapse and shift variations. It is not a complete reduced degree count or a whole-action health theorem. In particular the finite-k coincident scalar calculation cannot be extrapolated into a generic-background count. The same-action coincident vacuum family survives for every positive input A; these constraints do not universally select A or 32π.

## 1. Action, variables and boundary domain

Use the inherited action with n≥3 spatial dimensions, K>0, a common clock timelike for both metrics, and the unitary chart θ=t. Both shifts are retained. Assume either compact spatial slices or boundary conditions allowing the stated integrations by parts; when a boundary term is nonzero it must instead be retained as boundary data. Minimal matter is included separately in each metric's canonical phase space, with its ordinary ADM deformation algebra and its own equations, not an externally frozen stress.

The interaction has no time velocities and is exactly

V=κ a0² sqrt(NL) σ M(I), κ=2Kχ_n,
σ=(detγ det hatγ)^(1/4), h^{ij}=(γ^{ij}+hatγ^{ij})/2,
I=h^{ij}∂i r∂j r/a0², r=ln(N/L).

Here V is a spatial density, and the action adds +∫V. M is the eliminated differentiable envelope on I≥0. At positive I the formulas use two derivatives of M. At I=0 the norm-cube envelope has a C2 field-jet extension even if M_II itself diverges: combinations below have their continuous limits. No uneliminated auxiliary regularity is inferred.

Let λ=sqrt(NL)>0, α=exp(r/2), β=exp(−r/2), so N=λα and L=λβ. Write the individual Einstein-plus-matter energy densities E_g,E_hat and momenta D_gi,D_hati. With π the canonical spatial metric momentum,

E_g=[π^{ij}π_ij−π²/(n−1)]/(K sqrtγ)−K sqrtγ R[γ]+E_m,g,
D_gi=−2γ_ij D_k π^{jk}+D_m,gi,

and hatted counterparts. The π convention follows from K N sqrtγ(K_ij K^ij−K²+R), with extrinsic curvature (dotγ−Lie_shift γ)/(2N). The full canonical Hamiltonian is

H0=∫[λ C+S_g^i D_gi+S_hat^i D_hati],
C=α E_g+β E_hat−U, U=κ a0² σ M(I).

All six shift momenta and both lapse momenta vanish as primary constraints. No lapse- or shift-velocity term is hidden in V.

## 2. Both exact lapse rows and their functional Hessian

The common primary gives C=0. Define

A=(α E_g−β E_hat)/2,
J^i=2κσ m h^{ij}∂j r, m=M_I.

The relative primary gives the complete spatial Euler equation

S=λ A+∂i(λ J^i)=0.

The original two Hamiltonian lapse Euler rows are (λ C/2+S)/N and (λ C/2−S)/L, so both vanish exactly when C=S=0. This derivative includes λ, σ, h, and m. Holding canonical spatial and matter data fixed, the mixed linearization is

δ_r C=B f=A f−J^i∂i f,
B* u=A u+∂i(J^i u), S=B*λ.

The star is the formal spatial adjoint for the declared boundary conditions. Thus the lapse functional Hessian in (λ,r) has blocks

[ 0       B  ]
[ B*   L_r  ],

L_r f=λ(α E_g+β E_hat)f/4+∂i(λ D^{ij}∂j f),
D^{ij}=2κσ[m h^{ij}+(2M_II/a0²)(h^{ik}r_k)(h^{jl}r_l)].

A common-lapse algebraic Hessian rank alone misses B. It is equally incorrect to replace this transport block by an elliptic common-lapse block.

On S=0 the operators simplify exactly to

B f=−λ^−1 ∂i(λ J^i f),
B* u=λ J^i∂i(u/λ).

Consequently u=α_time(t) λ is a null direction on every lapse solution; it is the admitted global time-coordinate/clock-relabel freedom. More kernel functions may be constant along J-flow lines. Their existence and solvability depend on the slice and boundary data. Conversely a generic nonconstant u/λ along a nonzero J flow is not in this kernel. Therefore neither complete mixed-block invertibility nor arbitrary local common-lapse freedom follows. This is a functional, not a pointwise finite-matrix, statement.

In an orthonormal frame for positive h, the relative principal coefficients are proportional to m transverse to grad r and m+2I M_II parallel to it. If both are nonzero with the same sign the relative spatial row is elliptic; if they differ in sign it is mixed; zeros require a separate branch analysis. The Hamiltonian Euler symbol is −λ D^{ij}k_i k_j. None of these signs is a physical time-kinetic sign. For the deep cubic M=−A0+I/2−I^(3/2)/12, x=sqrt I, these eigenvalues are 1/2−x/8 and 1/2−x/4, positive on 0≤x<2. Neglecting dm changes the radial coefficient.

At a coincident lapse/metric branch, grad r=0 and C=S=0 imply A=0; the whole mixed operator B vanishes. The relative elliptic block nevertheless retains D=2κσm(0)h. This is a nonlinear-to-coincident rank change in the mixed block, not a proof of an extra propagating ghost. For a genuinely constant M, m=0 and J=D=0: the relative lapse equation is algebraic. That homogeneous/constant-potential exception must not be conflated with the derivative-bearing envelope at an I=0 background.

## 3. All six shifts and actual preservation rows

Each shift primary gives its own Einstein-plus-matter momentum density D_gi=0 and D_hati=0. The interaction is shift independent, but their preservation is not automatically two separate spatial gauge symmetries.

Define the metric Euler tensor densities of V with lapses held fixed,

V_g^{ij}=λκσ[a0² M γ^{ij}/4−m(γ^{ik}r_k)(γ^{jl}r_l)/2],

and V_hat with the hatted inverse metric. Under an independent spatial deformation ξ of g, keeping both lapses and hatγ fixed, δγ=Lie_ξγ. Integration by parts gives δV=−∫ξ^i 2γ_ij D_k V_g^{jk}. The Einstein energy variation gives −∫ξ^i E_g∂i N. Thus, up to Lie-bracket terms proportional to the momentum rows themselves,

dot D_gi=W_gi=E_g∂i N−2γ_ij D_k V_g^{jk},
dot D_hati=W_hati=E_hat∂i L−2hatγ_ij hatD_k V_hat^{jk}.

D_k here acts on the tensor density of weight one. The corresponding rows W=0 are the required preservation equations; they may be canonical-data constraints, lapse-fixing rows, or dependent rows on a special branch. Calling all of them independent second-class constraints before their Poisson rank and boundaries are checked would be premature.

A simultaneous spatial deformation transforms both metrics and both scalar lapses. Its exact density Ward identity yields

W_gi+W_hati=(E_g−EL_N V)∂i N+(E_hat−EL_L V)∂i L.

The individual lapse Euler equations are equivalent to C=S=0, so the sum vanishes there. There are therefore at most three additional independent relative preservation rows. Their longitudinal and transverse projections supply the scalar and vector relative conditions on a chosen background; the diagonal three spatial gauge directions remain. They are not two independently available spatial gauge groups. In particular the vanishing of some linearized transverse rows at an isotropic coincidence point is not a nonlinear classification of vectors.

For completeness, with r held as a canonical configuration variable but no momentum in C, the smeared bracket is

{C[f],C[g]}=D_g[α²γ inverse(f grad g−g grad f)]
 +D_hat[β²hatγ inverse(f grad g−g grad f)].

The interaction cross brackets cancel locally because U contains no spatial-metric derivatives and is independent of metric momenta. Derivatives of α and β cancel in the antisymmetric EH bracket. This is weakly zero on the momentum rows, but C still has B brackets with the relative-lapse primary and brackets with the independent spatial generators. It is insufficient to declare C a local first-class Hamiltonian constraint.

The next consistency step is genuinely required: preserve C,S,W using the total Hamiltonian including both lapse velocities and all six shift multipliers. It involves the functional matrices {W,D_relative}, δW/δλ, δW/δr and their compatibility with B,L_r. Their rank on actual sourced backgrounds and the boundary kernels have not been calculated here. A physical DOF number, full lapse/shift elimination, or generic ghost diagnosis is deliberately not asserted. This is the remaining nonlinear Dirac arrow, rather than an assumption of failure from nonclosure.

## 4. Clock, matter and coefficient implications

Separate minimal matter covariance gives each matter conservation law on its matter equations. Full diagonal spacetime covariance gives the weighted sum of both metric Euler divergences equal to the clock Euler coefficient times dθ. On both metric and matter equations the clock equation follows since dθ is timelike and nonzero. This is an exact Noether dependency, not permission to omit an independent metric preservation equation or proof that the clock has no physical state. In unitary gauge only common spatial covariance and the admitted global clock-relabel/time freedom are manifest.

The constraints cannot universally select A0. A coincident vacuum, r=0, γ=hatγ and identical extrinsic curvatures, has I=0, U=−κa0²σ A0, E_g=E_hat=U/2, and both momentum and W rows vanish. The common solution is ordinary de Sitter with

Λ=χ_n a0² A0/2, H²=χ_n a0² A0/[n(n−1)].

For every positive A0 these are actual common-metric vacuum solutions, and the clock equation adds no selector. Complete source/interior/boundary admission might constrain combinations for a particular externally specified problem; it cannot erase this freely parameterized vacuum family as a universal action constraint. No target coefficient has been inserted.

## 5. Bounded evidence and first unresolved implication

checks.py verifies generic functional lapse variations and formal adjoints in a one-coordinate fixture with arbitrary coefficient functions and a quadratic M, the exact diagonal-spatial Ward identity with arbitrary two-metric functions, the cubic principal coefficients, and the all-A0 common vacuum normalization. The dimension-free functional derivation above carries the general claims. Three controls discard the mixed transport restriction, discard M_II in the radial coefficient, or falsely grant an independent spatial Ward identity to one metric. These are algebra discriminants, not a nonlinear evolution or Dirac rank certificate.

Nearest earlier results remain intact: the finite-k coincident scalar has one positive reduced branch, its decaying mode yields signed dustlike interaction stress, and the pure static fixed-metric clock has no quadratic time derivative. They do not close the remaining generic coupled constraint classification. The next executable calculation is the full W-preservation Poisson matrix on an admitted noncoincident sourced branch, with boundary conditions and minimally coupled matter retained. The original 32π/cold-sector goal remains open.
