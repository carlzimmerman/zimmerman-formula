# I15: actual single-plaquette and volume-uniform lattice gap statements

Base: `e3af62a453ca6625db8428f6d32957b27a7f1331`.
Original arithmetic certificate: `790ee1d37`.
Status: elementary operator proof for one plaquette; an application of an
external stability theorem for the full lattice. Scalar constants and
comparison interfaces are additionally Lean-certified. The operator theory
and external theorem are not claimed as Lean-formalized. No novelty claim.

## 1. Precisely specified Hamiltonian

Fix spatial dimension d >= 2, integer N >= 2, x=g^2>0, and 0<=b_N<=2N.
At lattice spacing one use

    H = (x/2) sum_links C_l + (b_N/x) sum_plaquettes (1-T_p),
    T_p = Re Tr(U_p)/N.

Here a positively oriented link has Hilbert space L2(SU(N), normalized Haar),
C_l is the positive group Casimir with tr(t_a t_b)=delta_ab/2, and U_p is
the oriented four-link holonomy. All reverse links are inverses of their
positive representatives, not extra Hilbert factors. T_p is a real
multiplication operator, with -1<=T_p<=1. The physical Hilbert space is the
subspace invariant under the vertex gauge group, with no external charges.

The repository's displayed YM05 Hamiltonian has b_N=2. The conventional
coefficient b_N=N is also covered, as is b_N=2N. Stating b_N explicitly
prevents borrowing a numerical threshold across magnetic normalizations.
The comparison does not assume the electric vacuum is the interacting
vacuum. For finite graphs the Casimir sum has compact resolvent; bounded
real magnetic multiplication preserves self-adjointness on its domain,
lower semiboundedness, and compact resolvent. Eigenvalues below are ordered
with multiplicity, E0<=E1<=....

## 2. Casimir minimum for every SU(N)

Let omega_i, 1<=i<N, denote the fundamental weights, with long roots of
length squared two. Their Gram matrix is

    (omega_i,omega_j)=min(i,j)*(N-max(i,j))/N > 0.

The irreducible highest weights are lambda=sum a_i omega_i, a_i>=0
integers, and the Casimir normalization above is

    C2(lambda)=(lambda,lambda+2 rho)/2, rho=sum omega_i.

If lambda is nonzero choose i with a_i>=1 and write lambda=omega_i+nu,
where nu is dominant. Positivity of every Gram entry gives

    C2(lambda)-C2(omega_i)
      = (nu,nu)/2 + (nu,omega_i+rho) >= 0.

Furthermore

    C2(omega_i)=i(N-i)(N+1)/(2N)
              >= (N-1)(N+1)/(2N)=C_F,

because i(N-i)-(N-1)=(i-1)(N-i-1)>=0. Equality is attained by the
fundamental and its conjugate. Thus the least nonzero group Casimir is

    C_F=(N^2-1)/(2N) >= 3/4.

This uses the usual compact-group Peter-Weyl decomposition and highest-
weight Casimir formula, not a finite representation cutoff. The displayed
Gram formula also follows directly from omega_i=sum_{k<=i} e_k-(i/N)sum e_k
in the hyperplane sum coordinates=0. These formulas fix the normalization
and give the complete all-N minimization; numerical enumeration is only a
benchmark. The single-loop character/Casimir reduction is also exhibited
in Ligterink, Walet and Bishop, hep-lat/0001028v1, and for SU(3) in the
primary paper Phys. Rev. D 105, 074504, section III, equations (3)-(5).

## 3. Closed single-plaquette theorem

On an open four-link square, gauge fixing a spanning tree leaves one
holonomy, up to conjugation. Consequently the physical Hilbert space is
L2 class functions on SU(N), with all irreducible characters an
orthonormal basis. Each of the four link Casimirs acts on character chi_R
by C2(R). Thus

    H_E chi_R = 2x C2(R) chi_R,
    E0(H_E)=0, E1(H_E)=2x C_F.

The electric ground vector is the constant function 1. It is a trial
vector for H, not an eigenvector of H. Haar averaging of the nontrivial
fundamental character gives <1,T1>=0, and therefore

    E0(H) <= <1,H1> = b_N/x.

Since H_B=(b_N/x)(1-T)>=0, the full min-max principle gives

    E1(H) >= E1(H_E)=2x C_F.

Subtracting these two inequalities proves, on the FULL untruncated
physical Hilbert space,

    gap(H)=E1(H)-E0(H) >= 2x C_F-b_N/x
             >= x(N^2-1)/N-2N/x = gapN(N,x).

For x>=2,

    gapN(N,x) >= N-2/N >= 1.

Thus the original N-uniform scalar expression genuinely bounds an actual
single-plaquette spectral gap. For the repository normalization b_N=2,
the sharper bound at x=2 is 2N-2/N-1, equal to 2 for SU(2) and 13/3 for
SU(3). Neither these nor the original 1 and 7/3 are exact spectral gaps.

This proof controls the entire excited spectrum and the shifted ground
energy. A two-state truncation or a single off-diagonal estimate would
not supply those conclusions. For P plaquettes a naive global magnetic
bound scales with P; the single-plaquette expression must not be copied
unchanged to arbitrary P.

## 4. An actual many-plaquette theorem, uniform in N and volume

For each fixed d there is a finite constant X_d, independent of N, such
that for all N>=2, all 0<=b_N<=2N, and x>=X_d:

* Every finite open subgraph of the cubic lattice (with selected elementary
  plaquettes) has a unique gauge-invariant ground state and a spectral gap
  at least 3x/16 whenever its physical excited sector is nonempty. For a
  graph with no physical excitations the corresponding spectral-exclusion
  statement is vacuous.
* The canonical infinite-volume ground state obtained from the fixed
  homogeneous interaction has a GNS Hamiltonian with a simple zero
  eigenvalue and spectrum outside zero bounded below by 3x/16. The same
  bound holds on the cyclic physical space of gauge-invariant local
  observables.

X_d is specified below in terms of constants from a checked external
theorem. No numerical value of X_d, particularly X_d<=2 or X_d<=8, is
established. This is a fixed-spacing strong-coupling result. It gives no
continuum scaling window, confinement observable, or Clay solution, and
does not assert uniqueness among every possible infinite-volume ground
state/representation or cover periodic tori without a separate argument.

### External theorem used

Yarotsky, *Quasi-particles in weak perturbations of non-interacting quantum
lattice systems*, arXiv:math-ph/0411042v1 (11 November 2004), pp. 2-4,
Theorems 1-3 and equations (1)-(6). The site Hilbert spaces may be infinite
dimensional. On-site self-adjoint nonnegative operators have a unique
zero vector and gap at least one. Bounded self-adjoint interactions have a
fixed finite support S. There are positive constants c1,c2 depending only
on S: for eta=sup_z||phi_z||<c1, finite volumes have a unique ground state
and gap at least 1-c2*eta. The canonical thermodynamic ground state and
its GNS Hamiltonian exist, and the spectral estimate persists there.
Section 2 reviews the proof and refers to the author's 2004 J. Math.
Phys. paper for details. We use this established theorem as an external
leaf; we do not reproduce or claim to mechanize its cluster expansion.

The crucial contract is dependence ONLY on the interaction range, not
the local Hilbert-space dimension or high-energy on-site spectrum.

### Explicit dictionary and small parameter

Group the d outgoing positive links at z into

    H_z=L2(SU(N)^d), h_z=(1/C_F) sum_{i=1}^d C_(z,i).

The product constant is the unique on-site ground vector. Section 2 shows
that h_z has gap one, despite its unbounded infinite-dimensional spectrum.
Normalize energies by s=x C_F/2. Discard the magnetic scalar constant
(b_N/x) times the number of plaquettes; it changes no gap. Let
m=d(d-1)/2 and group the m oriented plaquettes with lower anchor z into

    phi_z = -[2 b_N/(x^2 C_F)] sum_{i<j} T_(z,ij).

Their common support is contained in the FIXED site set
S={0,e1,...,ed}: the four links of a plaquette are assigned to z,z+ei,z+ej.
No gauge fixing or constrained tensor product is needed at this stage.
The tensor product is the unconstrained link space. Since ||T_p||<=1,

    eta <= 2 b_N m/(x^2 C_F)
         <= (32/3) m/x^2 = A_d/x^2,

using b_N/C_F<=16/3. All constants are independent of N and volume.
Choose, for example,

    X_d = max(1, sqrt(2 A_d/c1), sqrt(2 c2 A_d)).

For x>=X_d, eta<=c1/2<c1 and c2*eta<=1/2. The source theorem gives a
normalized gap at least 1/2. Undoing the energy rescaling gives

    gap >= x C_F/4 >= 3x/16.

This is a proof of existence of a common strong-coupling window, not an
estimate of its useful numerical onset. At fixed 't Hooft coupling Nx the
assumption x>=X_d eventually fails as N grows; that different limit is
not covered.

### Finite boundaries

For the canonical infinite system, the source's empty-boundary restriction
keeps each grouped interaction only when its whole declared support fits
inside the site volume. This is a legitimate homogeneous exhaustion of the
same infinite plaquette interaction, though not identical to keeping every
individual plaquette of a usual finite open box near all boundary faces.

For an arbitrary finite open subgraph, assign L2(SU(N)) only to its present
positive links and the one-dimensional space C to absent links. A site is
the tensor product of its present outgoing factors; an empty site has
h_z=0 on C. Its orthogonal vacuum complement is zero, so the local gap
condition holds vacuously. Define phi_z to sum only actual plaquettes and
pad the finite site volume to contain z+S for every active anchor. Absent
factors add no degrees of freedom. The source's finite-volume theorem
applies to this inhomogeneous construction with the same range and norm
bound. Thus no boundary plaquette or external gauge charge is silently
introduced. We use the fixed homogeneous exhaustion, not these changing
padding models, for the infinite-volume existence assertion.

### Gauge constraint and the actual vacuum

All link Casimirs and plaquette traces commute with the finite vertex
gauge group. The unique unconstrained finite ground vector consequently
transforms by a continuous one-dimensional representation of a finite
product of SU(N)'s. This group has no nontrivial such representations, so
the vector is gauge invariant. Its orthogonal complement in the physical
space is a subspace of the full excited complement. Restriction therefore
cannot lower the spectral gap or change the ground energy.

The thermodynamic state is locally gauge invariant, since every finite
ground state is. To make the infinite-space restriction precise without
assuming a continuity property of a possibly infinite-dimensional local
observable algebra, Haar-average a local operator over a finite vertex
set F, calling the normal conditional expectation E_F. Finite ground
states satisfy

    omega(B* E_F(A)) = omega(E_F(B)* A)

and the averaging map contracts the state seminorm. These local identities
pass to the source's limiting state. Hence
P_F pi(A)Omega=pi(E_F(A))Omega is an orthogonal GNS projection. As F
increases, P_F converges strongly to P. For each local A, averaging over
all vertices incident to its support makes it globally gauge invariant;
therefore Ran(P)=closure{pi(A)Omega : A local and gauge invariant}.

The finite Hamiltonian resolvents commute with these averages. The weak
resolvent convergence in the source's Theorem 3 passes the matrix-element
identity to the limiting resolvent. Thus P_F, and then P, commute with
the limiting resolvent. Ran(P) reduces H_infinity, contains Omega, and
inherits both its simple zero eigenvalue and positive spectral gap.

## 5. What failed in the inherited shortcut

The original YM05 source marks the two-level spectral step with literal
`True`; that is not a verification. The electric constant wavefunction
also does not remain an eigenvector under magnetic multiplication. For a
single plaquette,

    H 1 = (b_N/x)(1-T),

which is nonconstant when b_N>0. Subtracting its expectation therefore
does not put the full interacting ground energy at zero. Already a
two-dimensional vacuum/loop principal block after that subtraction has
a nonzero off-diagonal and a negative lowest eigenvalue. YM07's comparison
against the bare electric vacuum requires a new argument for the dressed
vacuum; it is not used here. The two valid routes above explicitly account
for the interacting ground state.

## 6. Evidence and remaining scope

The all-N Casimir minimization and single-plaquette min-max proof are
analytic. The many-plaquette conclusion is a corollary of the exact
external theorem after the displayed normalization, boundary and gauge
checks. It is not inferred from finite diagonalizations.

`verify.py` constructs actual SU(2)/SU(3) character-basis truncations,
checks normalization, cutoff stability and the bounds, and verifies the
Casimir minimum over a stated finite family using exact rational arithmetic.
Its numerical gaps are finite Ritz calculations, not certified lower
bounds for infinite matrices. The analytic proofs supply the lower bounds.
`I15_suN_lattice_gap.lean` formalizes the scalar bound >=1, Casimir floor,
comparison arithmetic, local perturbation normalization, and rescaling.
External source checks and fresh-agent review are recorded separately.

Open: a useful explicit X_d; the claimed x>=2 many-plaquette window; any
continuum limit; any claimed physical connection between this Yang–Mills
model and the repository's scalar/phantom sector. None is assumed by the
theorems above.
