# Interacting-vacuum coercivity route: exact reductions and two obstructions

Base: `b73311096299e2f1816be00036ccdb2922bc44d4`. Date: 2026-09-22.
Route scope: finite SU(N) link Hamiltonians, the physical ground-state
transform, weak-coupling single-plaquette behavior, and a local-to-global
coercivity mechanism. This is a self-reviewed research derivation.

**Primary verdict: incomplete, with the smallest missing implication being a
volume-uniform interacting-vacuum coercivity estimate at weak bare coupling.**
The transform is an exact equivalence, not a solution of that estimate. The
two counterexamples below rule out proposed shortcuts, not Yang–Mills itself.

## 1. Claim card and conventions

Fix a finite graph with E oriented link representatives, selected elementary
plaquettes, SU(N) with N>=2, x>0, and fixed b=b_N>=0. Put M=SU(N)^E with
normalized product Haar measure dU. The bi-invariant metric makes the
left-invariant fields X_(l,a), for tr(t_a t_b)=delta_ab/2, orthonormal.
Thus C_l=-sum_a X_(l,a)^2 and

    H=-(x/2) Delta_M+V,
    V=(b/x) sum_p (1-Re Tr U_p/N).

The vertex group acts by U_l -> g_(s(l)) U_l g_(t(l))^-1. Physical functions
are its invariant functions; there are no external charges. The finite
Hamiltonian is the bounded-potential perturbation of the compact-manifold
Laplacian. The graph need not be connected. M is connected even then.

The intended physical conclusion is a nonzero spectral threshold m>0 for
(H-E0)/a along x=x(a)->0, uniformly through volumes large enough to recover
infinite physical space. A finite-volume identity alone does not construct
the limiting theory, prove nontriviality, or justify convergence of spectra.

## 2. Exact finite-volume ground-state transform

**Lemma 1.** H has a unique normalized ground function psi>0, smooth on M,
and psi is gauge invariant. With dmu=psi^2 dU and

    Gamma(f)=sum_(l,a) |X_(l,a) f|^2,
    lambda_phys(mu)=inf {int Gamma(f)dmu / int |f|^2dmu:
                         f gauge invariant, int f dmu=0, f!=0},

the infimum is over the weighted H1 form domain and

    gap_phys(H)=(x/2) lambda_phys(mu).                 (1)

An empty physical excited sector is assigned lambda_phys=+infinity.

Proof of positivity/uniqueness: the product compact connected Lie group has
a strictly positive heat kernel for every positive time. The Brownian
Feynman–Kac weight for bounded real V is strictly positive and bounded
above and below by positive constants at a fixed time. Hence exp(-tH) is
positivity improving. Compact resolvent gives a lowest eigenvector;
replacing it by its absolute value cannot increase the Dirichlet form.
The elliptic strong maximum principle makes a nonnegative minimizer
strictly positive. If the ground eigenspace had dimension greater than one,
a real ground vector orthogonal to this positive minimizer would change
sign; strict positivity improvement, or the equality case in the absolute
value form inequality, rules that out. Elliptic regularity gives smoothness.
Gauge transformations commute with H and preserve positivity and norm,
so uniqueness gives their invariance of psi.

For smooth complex f, direct integration by parts and H psi=E0 psi give

    <psi f,(H-E0)psi f>_(dU)=(x/2) int Gamma(f) psi^2 dU.   (2)

Indeed, expanding the gradient of psi f gives the |f|^2 |grad psi|^2
and mixed terms; after integration by parts they combine with V|psi f|^2
to E0|psi f|^2. Multiplication by psi is unitary L2(mu)->L2(dU),
takes 1 to psi, and preserves the gauge-invariant subspaces. Since psi
is smooth and bounded away from zero on this fixed compact M, this
identity extends by form closure in both directions. Min–max proves (1).

The transformed generator is

    L_mu=Delta_M+2 grad(log psi).grad,
    psi^-1 (H-E0) psi=-(x/2)L_mu.                    (3)

There is no replacement of psi by the electric constant state here.

**Exact scaling target.** For a chosen m>0, the finite-volume physical
gap bound gap_phys((H-E0)/a)>=m is equivalent to

    Var_mu(f) <= [x(a)/(2 a m)] int Gamma(f)dmu       (4)

for all physical f. Uniformity means the SAME m for all chosen small a
and all sufficiently large volumes, with specified boundary conditions.
A sharper necessary-and-sufficient positive-liminf formulation is

    liminf_(a->0) inf_Lambda [x(a)/(2a)]
                               lambda_phys(mu_(a,Lambda)) > 0.

Passing this estimate to a nontrivial continuum Hilbert space additionally
requires the independent continuum construction and spectral-transfer map.
Neither the transform nor finite-volume positivity supplies that map.

## 3. A genuine sufficient curvature lemma, and its explicit failure

Put W=-2 log psi, so dmu=exp(-W)dU. On this compact smooth product, if

    Ric_M+Hess W >= kappa g_M, kappa>0,              (5)

then lambda_phys(mu)>=lambda_all(mu)>=kappa and gap_phys(H)>=x kappa/2.
This implication does not itself assume the missing Poincare inequality:
it is a pointwise second-derivative condition on the actual vacuum.

For completeness, the Bochner identity for L_mu is

    Gamma_2(f)=|Hess f|^2+(Ric_M+Hess W)(grad f,grad f).

Integration against the invariant measure gives
int Gamma_2(f)dmu=int (L_mu f)^2dmu. Apply this to an eigenfunction
L_mu f=-lambda f and use int Gamma(f)=lambda int f^2 to obtain
lambda^2>=kappa lambda. Completeness of the elliptic spectrum proves the
Poincare inequality. For the stated normalization Ric_SU(N)=(N/4)g:
Ric_ab=(1/4)sum_cd f_acd f_bcd=N delta_ab/4. The one-plaquette SU(2)
case below also follows from the sphere S3 of radius 2, Ric=(1/2)g.

**Lemma 2 (actual interacting SU(2) counterexample to (5)).** On an open
four-link plaquette, with b>0, no positive kappa satisfies (5) if
x^2<2b/3.

Proof: gauge invariance reduces psi to a smooth central function phi of
the plaquette holonomy. At any configuration U_* with U_p=-I, the
differential of phi vanishes: conjugation fixes -I and its differential
acts as the three-dimensional adjoint representation, which has no
invariant covector. Consequently grad_M psi(U_*)=0. The eigen-equation
gives

    Delta_M psi(U_*)/psi(U_*)=(2/x)(2b/x-E0).

The normalized constant trial function has expectation b/x, so E0<=b/x.
Since dim M=12 and scalar curvature=12/2=6,

    tr_g(Ric_M-2 Hess log psi)(U_*)
       =6-(4/x)(2b/x-E0)
       <=6-4b/x^2 <0.                              (6)

A negative trace rules out a positive semidefinite tensor. By smoothness,
this is also a neighborhood obstruction, not only a measure-zero point.

This conclusion concerns the sufficient full-product tensor inequality.
It does NOT refute physical Poincare coercivity. In particular, a smooth
class function has zero differential at the central point; the restricted
Bochner identity also contains its Hessian term. Dropping that distinction
would incorrectly turn failure of a sufficient condition into failure of
the desired spectral gap. Lemma 3 shows the physical gap actually remains
positive as x->0 for this very system.

An additional elementary ceiling holds for any such smooth density on M:
integrating tr(Ric+Hess W) against unweighted Haar gives dim(M) N/4,
because int Delta W dU=0. Thus a global tensor lower bound can never have
kappa>N/4, however tightly the vacuum concentrates. A curvature argument
on a quotient or a restricted function class is a different argument.

## 4. Single-plaquette weak coupling is not the obstruction

**Lemma 3.** For one SU(2) plaquette with fixed b>0,

    E_n(x) -> (2n+3/2) sqrt(b), n=0,1,...,
    gap_phys(H_x) -> 2 sqrt(b),
    lambda_phys(mu_x) ~ 4 sqrt(b)/x,                (7)

where n indexes the physical spectrum from zero. No finite representation
truncation is used in this statement.

Write U=cos(theta) I+i sin(theta) n.sigma, 0<=theta<=pi. Class Haar
measure is (2/pi)sin^2(theta)dtheta, T=cos(theta), and

    C=-(1/4)[d^2/dtheta^2+2cot(theta)d/dtheta].

The four link Casimirs each act as C. The unitary multiplication by
sin(theta), ignoring its constant normalization, sends the physical
Hamiltonian to the Friedrichs Dirichlet operator

    h_x=-(x/2)d^2/dtheta^2+(b/x)(1-cos(theta))-x/2
                         on L2((0,pi),dtheta).    (8)

This follows directly by differentiating u=sin(theta)f. Endpoint
regularity gives the Dirichlet conditions; equivalently the SU(2)
characters map to the complete sine basis sin((2j+1)theta), j=0,1/2,... .

Rescale theta=sqrt(x)y. Then h_x+x/2 is unitarily equivalent to

    A_x=-(1/2)d^2/dy^2+(b/x)(1-cos(sqrt(x)y)),
                        y in (0,pi/sqrt(x)),     (9)

with Dirichlet endpoints. The potential tends locally uniformly to
b y^2/2. Moreover 1-cos(theta)>=2theta^2/pi^2 throughout [0,pi], so
the potential in (9) is bounded below by 2b y^2/pi^2, uniformly in x.

Here are the needed convergence details. For limsup of the nth
min–max value, approximate the first n+1 half-line oscillator eigenvectors
in its form norm by smooth compactly supported Dirichlet test functions.
For small x their supports fit the interval in (9), and their entire
finite-dimensional form matrix converges. For liminf, extend normalized
low-energy eigenvectors by zero onto the half-line. The uniform lower
bound controls both their H1 seminorm and int y^2|u|^2. Rellich compactness
on bounded intervals and the y^2 tail bound give strong L2 subsequences;
orthogonality is retained. Weak H1 lower semicontinuity and local potential
convergence give the oscillator form lower bound on every combination
of the first n+1 vectors. Min–max proves convergence of each eigenvalue.

The half-line Dirichlet oscillator is the odd part of the full-line
oscillator of frequency sqrt(b); its levels are (2n+3/2)sqrt(b).
Restoring -x/2 gives (7). This finite-system argument proves no estimate
uniform in an increasing number of plaquettes: low collective modes
can appear only as the volume grows.

## 5. Uniform conditional gaps fail to control collective modes

The next example is an exact finite-range oscillator Hamiltonian. It is
NOT an alternative definition or proved scaling limit of the SU(N)
Hamiltonian. Its role is to disprove the general inference that uniform
one-coordinate conditional Poincare gaps force a volume-uniform full gap.
It also keeps an actual color-singlet restriction, to prevent mistaking
the soft mode for a non-invariant linear observable.

**Lemma 4 (exact counterexample to the conditional shortcut).** Let K_L
be the L-by-L Dirichlet nearest-neighbor matrix with diagonal 2 and
off-diagonal -1. Let r=N^2-1, q_j in R^r, and

    H_(L,x)=-(x/2)sum_j Delta_(q_j)
                  +(1/(2x)) sum_a (q^a)^T K_L q^a, x>0.   (10)

Restrict to simultaneous Ad(SU(N))-invariant functions of all q_j. Its
ground density is

    dmu proportional to exp[-(1/x)sum_a (q^a)^T Q_L q^a] dq,
    Q_L=sqrt(K_L).

Every conditional distribution of q_j given all other sites has
Poincare eigenvalue 2(Q_L)_(jj)/x>=2/x, uniformly in L and the
conditioning. Nevertheless

    gap_all(H_(L,x))=omega_1,
    gap_singlet(H_(L,x))=2 omega_1,
    omega_1=2 sin(pi/[2(L+1)]) ->0.                 (11)

The corresponding full and singlet Poincare eigenvalues are
2 omega_1/x and 4 omega_1/x respectively.

Proof: K_L has orthonormal sine eigenvectors and eigenvalues
4 sin^2(k pi/[2(L+1)]), 1<=k<=L. Orthogonal mode transformation
diagonalizes (10) into independent r-component oscillators of frequencies
omega_k. Their ground wavefunction is the stated Gaussian square root.
Completing the square in q_j gives covariance x/[2(Q_L)_(jj)] times I_r
for its conditional distribution. A scalar Gaussian of variance s^2 has
Poincare eigenvalue 1/s^2, by its Hermite spectrum. Since all eigenvalues
of K_L lie in (0,4), sqrt(K_L)>=K_L/2 as matrices, giving (Q_L)_(jj)>=1.

The linear first-mode excitation has energy omega_1 but is adjoint
valued, hence not a singlet. All one-quantum states are copies of the
adjoint representation, with no invariant vector. Every state of degree
at least two has excitation energy >=2 omega_1. The explicit function

    f(q)=|qhat_1|^2-r x/(2 omega_1)                 (12)

is a centered adjoint-invariant quadratic Hermite eigenfunction and
attains energy 2 omega_1. This proves the singlet equality in (11).

The same f quantifies the missing mixing step. If an approximate
tensorization inequality were asserted in the singlet sector,

    Var_mu(f)<=C_L sum_j E_mu Var(f | all sites except j),  (13)

then necessarily C_L>=1/(2 omega_1), which diverges with L. To see this,
put v_j for the normalized first sine eigenvector. Conditional variance
of |v_j q_j+h|^2 for a Gaussian q_j of covariance
s_j^2 I=x I/[2 Q_jj] is
2r v_j^4 s_j^4+4 v_j^2 s_j^2 |conditional mean(qhat_1)|^2.
After expectation, using Var(qhat_1^a)=x/(2omega_1), one obtains exactly

    E Var_j(f)=r x^2 [v_j^2/(Q_jj omega_1)
                                     -v_j^4/(2 Q_jj^2)],
    Var(f)=r x^2/(2omega_1^2).

Since Q_jj>=1 and sum v_j^2=1, the sum of conditional variances is
at most r x^2/omega_1. Their ratio is at least 1/(2omega_1).

Thus local coercivity alone misses a quantitatively divergent spatial
mixing factor, even on invariant functions and even for a Hamiltonian
with finite-range quadratic interactions. An assertion of (13) with
uniform C would need separate, nontrivial interacting-vacuum evidence.

## 6. Relation to the actual weak-field lattice model

This subsection only identifies a perturbative obstruction; no claim of
uniform approximation to Yang–Mills is made. Set U_l=exp(i A_l^a t_a).
To quadratic order about the identity, the plaquette angle is dA and

    1-Re Tr U_p/N=|dA_p|^2/(4N)+higher orders.

On transverse, nonzero lattice Fourier modes, the quadratic Hamiltonian
is therefore an oscillator system with

    omega(k)=sqrt(b/(2N)) s(k),
    s(k)^2=4 sum_i sin^2(k_i/2).                   (14)

Its vacuum precision is proportional to sqrt(d^*d)/x, not to the local
magnetic Hessian d^*d/x. Modes with |k|~1/L have frequency O(1/L).
Color contraction of two quanta gives a global singlet with energy of
the same O(1/L) order. Periodic zero modes and nonlinear Gauss law need
separate treatment; (14) does not solve either. Dirichlet Lemma 4 avoids
all zero-mode ambiguities while proving the precise local-to-global
failure relevant to this candidate mechanism.

Consequently, neither the isolated-plaquette oscillator scale in (7)
nor uniform local conditional gaps establishes a mass. The required new
information concerns nonlinear long-distance behavior of the actual
vacuum. The linearized approximation alone has no such mass-generating
coercivity.

## 7. Dependency and obligation record

| Arrow or obligation | Status | Evidence |
|---|---|---|
| finite positive physical vacuum | passed | positivity and compactness proof in section 2 |
| interacting gap = weighted Poincare constant | passed | form identity (2), unitary and gauge checks |
| correct a,x normalization | passed | (1) divided by a gives (4) |
| positive BE curvature implies gap | passed | integrated Bochner proof; primary source cross-check |
| weak-coupling global positive BE curvature | failed | actual SU(2) trace counterexample (6) |
| weak single-plaquette gap collapse | refuted for fixed b>0 | exact reduction and oscillator convergence (7) |
| local conditional gaps imply uniform singlet gap | refuted | exact oscillator family (10)-(13) |
| Gaussian model equals full YM at growing volume | not addressed | explicitly not assumed |
| actual weak-coupling volume-uniform vacuum coercivity | not addressed | no derived mixing/confinement estimate |
| continuum construction and nontriviality | out of route scope | separate continuum route |

Strongest safe conclusion: the vacuum reformulation and finite-plaquette
asymptotic are exact; a standard full-product curvature shortcut is false,
and local conditional coercivity cannot remove collective infrared modes
without an additional spatial estimate. The cheapest next discriminating
check is a provable multiscale mixing estimate for the actual psi^2,
with its volume dependence explicit. Simply postulating that estimate
would restate the unresolved mass-gap input.
