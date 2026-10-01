# Independent root-only audit: FGF041 packet defect

Primary verdict: **proved as written**, for this explicit approximate-state sequence and the precise residual/limit topologies stated. No mathematical error was found. The nonzero defect is present in the initial data. The construction does not produce exact nonlinear solutions or energy from zero-energy data, and the sufficient compactness assumptions are not derived from the equations.

## Claim, independence and pins

The specified moving packet has uniformly bounded finite energy, weakly convergent field gradients/velocities and vanishing residuals in the stated weak spaces. Its quadratic momentum, stress, energy density and energy flux converge as measures to the background expressions plus nonzero transported concentrations. Thus these bounds and residual topologies alone do not identify nonlinear quantities from the weak field limit. A vanishing additional amplitude removes this defect. Separate strong-convergence assumptions suffice to identify combined momentum coefficients and, with additional entropy/potential hypotheses, energy density.

This is an independent root-only analytic reconstruction under the proof-audit workflow. The root proof and record and task FGF041 were read. The pinned old FGF040 proof and FGF023 action were inspected in preceding audit work and their hashes were checked again. No new author or other reviewer proof was read. There was no numerical scan or mathematical computation run. All hashes in PROOF_RECORD.json matched actual files. Its independence timing is recorded as root's provenance declaration rather than independently reconstructed from all root messages. Original proof bytes are preserved.

- ROOT_DERIVATION.md: 57549a5543c71a35307ed3ccef9036fe8a0cb6d015bfed8e0a20bb294a80ca3b
- PROOF_RECORD.json: 83e8aed4aa5e70177365bfc3a28dcfaf739e5a1fe0c0f6c8597c5b98cfce8ff6
- Task FGF-041.md: c48235050daa00451072139935ca103ee8b4115ab3f11196f294c390c5d22894
- FGF040 ROOT_DERIVATION.md: 9eb8d61177602f4cf4cc093bf43162ec997ced56693dc9e0ee709e601c5d534a
- FGF023 DERIVATION.md: 0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a

## Dependencies and obligation matrix

| Obligation | Status | Decisive check |
|---|---|---|
| Fixed Q action and background | Conditional inherited input | Positive coefficients, actual static crossing and fixed walls |
| Packet scaling and wall/mass admissibility | Passed | Compact trajectory support, exact derivatives and fixed density/scale |
| Global Q bounds at large signed gradients | Passed | Exact constitutive algebra, not a deep-gradient truncation |
| Every actual equation residual | Passed | Potential H−1 residual; matter/scale L1 residuals; exact continuity/compatibilities |
| Combined momentum residual | Passed | Direct flux expansion and transported-square cancellation |
| Full energy and its flux residual | Passed | Both kinetic/gradient contributions and n phi retained |
| Four measure limits | Passed | Exact change of variables and vanishing L1 remainders |
| Initial defect and amplitude control | Passed | Fixed nonzero initial L2 energy versus vanishing extra amplitude |
| Strong-convergence identification conditions | Passed as sufficient | Vacuum compatibility, strong L2 products and separate entropy control |
| General matter energy-flux identification | Not claimed | Further velocity/enthalpy product bounds needed |
| Exact solution existence, stability or physical closure | Out of scope | Explicitly excluded |

Dependency chain: exact packet derivatives and Q algebra -> small equation residuals and explicit energy/momentum expansions; shrinking support -> weak field limits and transported square measure; direct flux differentiation -> weak balance residuals. The initial data carry the same measure. The final sufficient compactness conditions are a separate implication; the packet does not satisfy them and the PDE is not shown to supply them.

## Reconstructed checks

**Scaling and support.** Differentiating the packet gives h=(Phi/L)epsilon^(-1/2)F' and u=-v h. Its squared spatial norm is exactly A0=(Phi²/L)integral F'^2, while its L1 norm is O(sqrt(epsilon)), its potential supremum is O(sqrt(epsilon)) and its potential L2 norm is O(epsilon). The compact trajectory can be chosen for a sufficiently short fixed time slab for every positive finite tau. The support remains away from the cusp and walls; hence wall data, fixed mass, impermeability and the scale cap are retained. The cusp's global lack of C2 regularity is not silently removed. For a fixed spacetime L2 test, absolute continuity of its squared integral over the shrinking tube proves weak L2 convergence of h and u to zero. Changing variables x=X(t)+L epsilon y proves h² dxdt -> A0 delta_X dt; the same calculation gives the fixed-time measure, including t=0.

**Exact Q estimates.** For s>=0, b-s lies between -a/2 and zero because 2s<=sqrt(a²+4s²)<=2s+a. Integration yields |W-s²/2|<=as/2. Combining this with |b-s|<=a/2 yields the stated conservative |S-s²/2|<=as. Also |B|<=|g|. Differentiating T=-W_chi gives T_s=a b/sqrt(a²+4s²), between zero and a/2. Since ||g+h|-|g||<=|h|, the Lipschitz estimate for T is global in the signed gradient, including every zero and sign reversal of F'. No invalid small-gradient series enters the concentrating region.

**Individual residuals.** The defect e_B=(B(g0+h)-g0-h)-(B0-g0) is supported in the tube and bounded by a. Thus its spatial L2 norm is O(sqrt(epsilon)) uniformly in time. With tau v²=1, phi_tt=v² h_x and B0_x=C rho give R_phi=-partial_x e_B exactly, so its L-infinity-in-time H−1-in-space norm vanishes. This does not bound the residual derivative in L1 or pointwise. Continuity and both kinematic identities are exact. Hydrostatic balance yields R_m=rho h, bounded in spatial L1 by a constant times sqrt(epsilon), uniformly in time. The background scale equation yields R_chi=T(|g0|)-T(|g0+h|), whose spatial/spacetime L1 norm obeys the same bound. The claimed conclusion does not require this scale residual to vanish in L2. These are the actual dynamic Q source and coupled equations, with no static-source constraint imposed on the packet.

**Momentum expansion and residual.** P=-tau u(g0+h)/C equals h²/(Cv)+tau v g0h/C because tau v=1/v. The second term has vanishing L1 norm. For the stress, the potential kinetic part is h²/2 and the Q S difference is h²/2+g0h plus an error supported in the tube and bounded by a constant times |h|+1. Hence Pi=Pi0+h²/C+rPi with rPi L1-small. The static background stress is constant: its derivative reduces to cs²rho_x+rho g0 after the static scale equation cancels the scale terms. No center delta is produced by the continuous background stress. Since (h²)_t+v(h²)_x=0, the leading momentum residual cancels exactly. Derivatives of the L1-small remainders tend to zero against compact C1 tests with the stated derivative supremum bound. They are not asserted to be L1-small functions. In particular no residual multiplication by the unbounded h was used.

**Full energy density and flux.** The kinetic potential energy supplies h²/(2C). W(g0+h)-W(g0) supplies h²/(2C) plus an L1-small error, by the same global Q bound and bounded background. The interaction rho psi is retained and has L1 size O(epsilon^(3/2)); density internal energy and scale terms are unchanged. Thus the full energy excess density is h²/C+rH, uniformly L1-small remainder. The actual constitutive energy flux for this ansatz is -B u/C=v B h/C; matter current and scale velocity vanish. Since B=B0+h+e_B with B0 and e_B bounded, this is v h²/C plus an L1-small remainder. The transported leading square cancels in the energy-balance residual as well. This is a direct approximate balance, not proof of exact conservation by the approximants.

The resulting singular weights are exactly A0/(Cv) in P, A0/C in Pi and full energy, and v A0/C in energy flux. They obey the transport balances. Inserting the weak limiting fields instead yields the static background expressions, so nonlinear identification fails in the demonstrated topology even though the background itself remains a solution.

**Initial state and amplitude control.** At t=0 the same square measure is already concentrated at x0 and the integrated excess is A0/C+O(sqrt(epsilon)). Neither initial gradient nor initial velocity converges strongly in L2. Uniform convergence of potential values is insufficient to remove this initial energy defect. Multiplying the packet by any positive b_epsilon tending to zero makes its gradient and velocity L2 norms tend to zero; their square weights become b_epsilon² A0. All remainders still vanish (the global estimates remain valid whether or not the rescaled peak gradient grows). Exact initial and subsequent excess energies then converge to the background energy. No initial-energy creation, exact-solution counterexample or uniqueness conclusion follows from the nonzero-defect case.

**Sufficient compactness conditions.** Strong L2 convergence of g,u,k,w identifies all their quadratic products in L1. Strong L2 convergence of r=sqrt(n) and z=j/sqrt(n) identifies n=r² and j=rz in L1. To identify z² with the quotient of those limiting fields, z must also vanish where r=0; the proof explicitly includes this condition. It is not automatic: r_epsilon can tend to zero while z_epsilon tends strongly to a nonzero function, leaving a kinetic contribution on vacuum. With the stipulated compatibility, the quotient j²/n is z² under the vacuum convention and converges in L1.

Uniform bounded convergence of chi identifies a, U and U'. The pointwise bounds |B_g|<=1 and |B_a|<=1/2 give strong L2 convergence of B on the finite slab, and hence L1 convergence of Bg. The bound for W differences in g follows by integrating |B|<=|g|; the scale change is bounded by |W_a|=T/a<=|g|/2. Strong L2 gradients and uniform scale convergence therefore identify W in L1. These assumptions suffice for all combined momentum coefficients.

Energy density needs the separately stated L1 convergence of e(n), and bounded uniformly convergent potentials to identify n phi. Strong density L1 convergence alone does not identify entropy. Convergence in measure plus uniform integrability of entropy densities gives the required L1 convergence by bounded truncation and small tails. Likewise convergence in measure of derivatives plus uniform integrability of their squares gives strong L2 convergence; uniform integrability alone does not eliminate oscillations. No such condition is asserted to follow from energy bounds and weak residuals. General matter energy flux contains additional velocity/enthalpy products and is explicitly excluded from this sufficient identification claim; only the zero-current packet flux has been directly checked.

**Units and branch scope.** epsilon and F are dimensionless; Phi is a potential and L is a length, so h is an acceleration. Tau v²=1 uses the inherited inertia coefficient, with v a speed, without identifying it with a physical photon speed. A0/C is integrated energy per transverse area, A0/(Cv) integrated momentum per area, and vA0/C the corresponding integrated energy-flux weight. Both positive a0 backgrounds and constant-vacuum, frozen-H and evolving-H uses remain distinct. This fixed-reference Q construction supplies no evolving-scale reservoir, physical metric/photon coupling or RAR/M transfer.

## Exact remaining gap

The demonstrated obstruction is failure of one specific compactness implication: bounded energy and these vanishing weak residuals do not identify nonlinear momentum and energy quantities from weak field limits. It is not failure of the limiting background to solve its equations. Initial strong energy convergence, exact solutions, boundary/initial trace closure and a general energy-flux theorem are not supplied or contradicted.

A useful next target is a specified approximation mechanism that propagates or establishes the sufficient compactness properties, or explicitly retains the resulting defect measures. The present proof neither selects such a mechanism nor proves nonlinear existence, uniqueness, energy creation, physical stability or theory closure. No source correction is required for the reviewed claims.
