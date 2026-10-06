# Independent finite-acceleration symbol audit

Verdict: the exact planar constrained high-frequency kinetic calculation is correct under its stated local assumptions. It improves the earlier lapse-response test: in this planar sector the negative response curvature survives elimination of both auxiliary lapse and longitudinal shift. The strongest supported statement remains a constrained-symbol result on constraint-compatible initial jets, conditional on these jets being admitted by an actual evolving background. It is not a ghost diagnosis for a sourced galaxy or a full time-evolution existence theorem.

Reviewed actual inputs, without taking the author's verdict as a premise:

- `finite_acceleration_symbol_2026_10_06/REPORT.md`, SHA256 01a850848bc2cfd1d7af4a9e443124741964ab87b51d07c5b646af84553c1384.
- `finite_acceleration_symbol_2026_10_06/checks.py`, SHA256 6e996a620314e2d4b54e41fe47105d092ca94bad14d5ce5957e223ee50cef403.
- Actual shared HEAD at review: 3f59dab1bec9d533a4dceed0f48c039ac05cce87.

No peer inputs were edited or rerun with outputs in their folder. All three existing manifests were independently validated; main_a has23 passing assertions, the shift and kinetic controls each fail their intended assertion. Those records support exact bookkeeping, not the unproved evolution implication. This audit additionally differentiated the lapse action directly rather than accepting the Hamiltonian equation encoded in checks.py.

## Raw action, fields, and constraints

The action used is

L=N sqrtγ {M/2[R3+KijKij−θ²]+2c lnN−Veff−b θ lnN+M Q(a)},
b=2c/(3H*), a_i=D_i lnN, M=K_E>0.

It is the timelike unitary-clock action with fixed A. The clock time gauge removes δφ, while a spatial longitudinal diffeomorphism removes one of the two SO(2)-scalar spatial metric components. On the flat planar initial slice the surviving scalar can be represented by γij=e^(2ζ)δij. This gauge representation does not require the subsequent background evolution to remain isotropic or conformally flat. The lapse N=N0 expν has no time derivative in this action. The x-directed shift v is an independent auxiliary field. No matter shift block is present because the calculation is vacuum.

For L0=N0h+ζdot, t=(L0−vζ′)/N and d=v′/N, the three K eigenvalues are t−d,t,t. Consequently the EH kinetic density is M e^(3ζ)[−3(L0−vζ′)²+2(L0−vζ′)v′]/N and the braid density is −b e^(3ζ)[3(L0−vζ′)−v′]lnN. These reproduce the report including all signs. The (v′)² coefficient vanishes identically. At the background ζ′=0 there is also no pure v² coefficient. Varying v before freezing background gradients gives E_v=−e^(3ζ)∂x[2M L0/N+b lnN] at v=0. Terms nonlinear in v multiply perturbative ζ′ and do not generate a linear pure-shift block about this slice.

Background momentum therefore requires 2Mh′+ba=0. A finite-a, constant-h freeze would be inadmissible; the report retains the required derivative. Linear momentum on a constraint-compatible background is
∂x[ζdot/N0−Dν]=0, D=h−b/(2M).
For the nonzero local wavevector, with the homogeneous spatial integration mode removed, ν=ζdot/(N0D). This removal is appropriate to the local principal calculation or compactly supported wavepackets; it is not a complete global boundary prescription. Spatial derivatives of N0,D remain in the exact derivative of this solution, but contribute lower powers of k and cannot alter the leading k² coefficient.

The auxiliary quadratic mixing is −2M k² β(ζdot/N0−Dν), v=β′. Its lapse variation has coefficient 2M D k²β, nonzero for k≠0,D≠0, and determines β rather than imposing a second condition eliminating ζ. Thus substituting the shift constraint is a genuine constrained reduction. Adding the scalar equation again would double-count the diffeomorphism Noether identity for a timelike clock.

## Leading physical kinetic sign

Direct expansion of the response gives M N0 Qaa(ν′)²/2. Substitution of the constraint yields
M Qaa k² ζdot²/[2N0D²]
plus lower principal powers from derivatives of coefficients. EH/KGB terms without spatial lapse derivatives contribute order-k0 scalar kinetic. Curvature νζ″ and response metric/lapse cross terms contribute spatial terms or at most one time derivative; they do not supply another leading k² ζdot². Thus Qaa<0 yields negative high-k kinetic in this constrained scalar sector if the prescribed action remains valid at those momenta and the background admits the stated jets.

The yz rotation symmetry of this genuinely planar background separates the SO(2) scalar from transverse vector and traceless tensor perturbations. In particular a tensor or transverse shift cannot cancel this scalar direction by mixing in this sector. Positive EH tensor kinetic fixes the relative energy convention. This is an indefinite physical kinetic form, not merely a negative eigenvalue of the uneliminated lapse. It does not itself determine dispersion, a growth rate, or Hadamard ill-posedness.

The claim excludes D=0, k=0 and Qaa=0. WKB also requires k larger than the background inverse lengths, and sufficiently large to dominate the finite lower kinetic terms. A finite EFT cutoff can invalidate extrapolation to that range. No such cutoff or higher operators are supplied by this action; claiming a repair would require their actual principal contribution.

## Constraint-compatible jets and the precise missing arrow

Independent lapse Euler differentiation, holding the spatial metric velocity fixed before writing h, gives the EH/potential/braid part
3Mh²+2c lnN0−Veff+2c−3bh.
Independent differentiation of M N0 Q(N0′/N0) gives
M[Q−aQa−Qaa a′].
Together these exactly reproduce the report's Hamiltonian equation. In particular the Qaa a′ term cannot be dropped when freezing a finite-acceleration jet. Combining this equation with N0′=N0a and h′=−ba/(2M) is a smooth first-order local ODE on Qaa≠0,N0>0. It supplies local initial slices satisfying both ADM constraints. D≠0 is needed for the scalar auxiliary reduction, not for the background ODE itself.

The report correctly stops short of showing that the spatial metric evolution equations preserve these lapse/shift solutions and produce a full on-shell spacetime. That is the smallest missing implication needed to turn the constrained-jet result into a realized-background ghost statement. The construction is substantially stronger than an arbitrary off-shell negative Qaa freeze, but initial constraint satisfaction alone does not prove this implication. Boundary conditions, the permitted clock-gradient domain and lapse equation solvability in time also remain relevant. Nothing here proves a physical galactic clock reaches the high-gradient interval.

## Generic directions and cutoff consequences

The weighted Hessian integration identity and the stated scalar auxiliary Schur algebra are consistent. The Schur factor is C/[D²−SC/2]; a negative C alone does not fix its sign for general S. The report appropriately labels this as a conditional template rather than an all-background full symbol. This audit's decisive acceptance is the exact axial planar result S=0; it does not promote the nonplanar template to a completed tensor/metric constraint audit.

The response dictionary gives Qaa=2δ′/(1+δ′) at epsilon0 when a=s+δ(s), 1+δ′>0. A positive excess tending to zero must decrease somewhere, so there is an acceleration interval with Qaa<0. The report's all-admitted-planar-jets health obstruction follows with its explicit proviso that these constraint-compatible jets belong to the dynamical background domain. It is not a no-go for every MOND theory or every low-clock sourced branch. The epsilon threshold for uncut P2 also follows directly by squaring the positive equation 1−epsilon=2a/sqrt(A²+4a²); its stated range0<epsilon<1 and threshold are correct.

The physical metric force and clock acceleration can differ strongly on a flowing clock. None of these signs may be substituted into solar or galactic force data without a matched solution. The low-clock freefall escape is therefore still logically open, as are specified higher-operator completions. No A/H or32π selector is established.
