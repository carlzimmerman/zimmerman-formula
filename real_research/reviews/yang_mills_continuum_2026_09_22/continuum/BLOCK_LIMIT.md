# YM-C1-C2: exact block lifts, an abstract limit, and loss of the form

Base: `b73311096299e2f1816be00036ccdb2922bc44d4`.
Owner: `ym_continuum`. Second-cycle bounded test, 2026-09-22.
Inputs: root's exact Schur graph-isometry hypothesis and this route's
`PROOF.md`, especially C3b. No additional external theorem is asserted here
beyond standard Hilbert-space spectral/variational facts proved in the uses
needed below. No Yang–Mills construction or no-go theorem is claimed.

**Result.** Compatible isometric form systems with a uniform positive gap do
construct a canonical abstract self-adjoint Hamiltonian and semigroup limit.
Persistent finite-energy vectors survive in that limit. However, the limiting
form need not agree with the compatible forms on their common algebraic
domain. Exact Schur structure and a summable eliminated-mode inverse-gap budget
do not repair that failure. The explicit example below has all those
properties and a nonclosable common form.

## 1. What the graph lift preserves

Index the cutoff Hilbert spaces mathcal H_N from coarse to fine, with
self-adjoint Hamiltonians H_N and associated closed nonnegative forms q_N.
Suppose isometries V_N:mathcal H_N -> mathcal H_(N+1) preserve the unit
vacuum and the forms:

    V_N Omega_N = Omega_(N+1),
    V_N D(q_N) subset D(q_(N+1)),
    q_(N+1)[V_N u] = q_N[u].                               (1)

The corresponding sesquilinear equality follows by polarization. Root's
U=J G^(-1/2), with Jp=(p,-D^(-1)Bp), is an instance when the normalized
Schur operator is the coarse Hamiltonian.

**Cross-cutoff consistency is a separate hypothesis.** Equations (1) must
hold for one genuinely compatible nested family across all UV cutoffs.
Producing a finite Schur chain separately for each tuned H_lat(a) does not
establish this: its generated coarse couplings, metrics, and even its
fixed-scale coarse operators may depend on total UV depth. Without common
identifications and (1) across those chains, the inverse monotonicity used
below is unavailable. Exactness within each individual chain is insufficient.

A vector u in mathcal H_(N0), orthogonal to the vacuum and in D(q_(N0)), lifts to
u_N by composition of the isometries. Then, exactly,

    ||u_N||=||u||,   <Omega_N,u_N>=0,
    q_N[u_N]/||u_N||^2 = E := q_(N0)[u]/||u||^2.             (2)

Hence Jensen's inequality for its normalized spectral measure gives

    <u_N,exp(-tH_N)u_N> >= ||u||^2 exp(-tE), t>0.           (3)

This is the C3b finite-energy witness. It requires no intertwining of the
Hamiltonians or semigroups. Form compatibility by itself does not give

    V_N exp(-tH_N) = exp(-tH_(N+1)) V_N.                    (4)

Nevertheless an abstract limiting semigroup can be constructed as follows.

## 2. A positive answer for the abstract Hamiltonian limit

**Theorem BL1.** Under (1), assume each Omega_N is the unique vacuum and
H_N >= m on Omega_N^perp for one fixed m>0. Form the Hilbert inductive limit
using V_N; write i_N for the resulting isometric inclusions. Then there is
a canonical nonnegative self-adjoint operator H on the limit Hilbert space
with kernel span{Omega} and gap at least m, such that for every t>0,

    i_N exp(-tH_N) i_N^* -> exp(-tH) strongly.               (5)

The union of the cutoff Hilbert spaces is dense by the definition of this
inductive limit. If any cutoff has a nonzero centered finite-energy vector,
the limiting excited sector is nonzero and its mass is finite. For the
vector in (2), its mass is at most E.

**Proof.** Work first on the excited complements, so all H_N >= m. Identify
the spaces as nested subspaces through i_N. Put

    R_N = i_N H_N^(-1) i_N^*,   0<=R_N<=m^(-1)I.            (6)

For any f in the inductive-limit Hilbert space, the form variational identity
is

    <f,R_N f> = sup_(u in D(q_N))
                  [2 Re<f,i_N u>-q_N[u]].                  (7)

This follows by completing the square in the Hilbert norm defined by q_N;
the optimizer is H_N^(-1)i_N^*f and lies in the operator domain. The domains
in (7) are nested and their forms agree by (1). Thus R_N increases in the
operator order. Its bounded increasing quadratic forms define a positive
bounded R. Moreover R_N -> R strongly: with A_N=R-R_N,

    ||A_N f||^2 <= m^(-1)<f,A_N f> -> 0.

R has zero kernel. Indeed <f,Rf>=0 forces <f,R_N f>=0 for every N,
and the injectivity of H_N^(-1) implies i_N^*f=0 for every N. Density then
gives f=0. Thus R has dense range and its inverse H_ex=R^(-1), defined by
the spectral theorem, is densely defined, self-adjoint, and >=m.

For fixed t>0 let f_t(s)=exp(-t/s) on s>0 and f_t(0)=0. This is continuous
on [0,m^(-1)]. Strong convergence of the uniformly bounded self-adjoint R_N
implies strong convergence of f_t(R_N) to f_t(R), by uniform polynomial
approximation. On the orthogonal complement of i_N mathcal H_N the operator R_N
vanishes, while on i_N mathcal H_N functional calculus gives

    f_t(R_N)=i_N exp(-tH_N)i_N^*.

This proves (5) on the excited sector. Adjoin H Omega=0 and the common vacuum
projection to get (5) on the full Hilbert space. Strong continuity of the
limiting semigroup follows from self-adjointness of H; at t=0 the cutoff
projections converge strongly to I.

The lifted vector u_N identifies with one fixed nonzero vector u in this
Hilbert space. Taking the limit in (3) gives a positive time correlation
bounded below by ||u||^2 exp(-tE). Since the spectrum on the excited sector
is bounded below by its mass M, that correlation is at most
||u||^2 exp(-tM). Therefore m<=M<=E<infinity. QED.

No summability of eliminated-mode costs is needed beyond its possible use
to establish the common positive gap m. Exact Schur structure is likewise
not needed for this abstract theorem once (1) is given.

**What BL1 does not prove.** The inductive-limit Hilbert space has no supplied
local field algebra, spatial translations, Euclidean symmetry, locality,
Yang–Mills ultraviolet behavior, or identification with physical continuum
observables. A vector surviving abstract graph lifts need not be a limit of
renormalized local observables. Furthermore, the limit can be the relaxed
form rather than the closure of the algebraic compatible form; the latter
may not even be closable. The next example proves that distinction.

## 3. Uniformly gapped compatible forms that are not closable

Take the excited cutoff spaces mathcal H_N=C^N with the ordinary inclusions into
ell2(N), and append one common zero-energy vacuum to each. For i>=1 put
w_i=2^i and c_i=2^(i/2). Define the finite positive matrices

    W_N=diag(w_1,...,w_N),  c^(N)=(c_1,...,c_N),
    H_N=W_N+c^(N)(c^(N))^*.

Their forms on the algebraic union c00 agree with

    q[x]=sum_i 2^i |x_i|^2 + |sum_i 2^(i/2)x_i|^2.          (8)

They have gap >=2, and the persistent unit vector e_1 has q[e_1]=4.
Thus both uniform coercivity and the exact finite-energy witness hold.

Nevertheless q is not closable on ell2. Set

    x_i^(N)=2^(-i/2)/N for i<=N, and zero otherwise.

Then ||x^(N)||->0,

    sum_i 2^i |x_i^(N)|^2=1/N,
    sum_i 2^(i/2)x_i^(N)=1,
    q[x^(N)]=1+1/N -> 1.

For M,N the linear functional in (8) vanishes on x^(N)-x^(M), and

    q[x^(N)-x^(M)] <= (N^(-1/2)+M^(-1/2))^2 -> 0.

This violates the defining closability criterion. In particular no closed
form can agree with q on all of c00: every restriction of a closed form is
closable.

## 4. The same example has exact Schur graph lifts

For the N-dimensional fine matrix H_N, let R_(N-1) be the first N-1
coordinate subspace. Choose the one-dimensional eliminated space

    Q_N=span{v_N},   v_N=H_N^(-1)e_N,
    P_N=Q_N^perp.                                          (9)

For r in R_(N-1), <r,H_N v_N>=<r,e_N>=0. Also the Nth component of
v_N is positive, so R_(N-1) intersects Q_N trivially and projects
bijectively onto P_N. In the orthogonal splitting P_N direct-sum Q_N write

    H_N = [[A,B^*],[B,D]],  D>0.

The H_N-orthogonality just proved implies

    R_(N-1)=Ran(J),  Jp=(p,-D^(-1)Bp).

Consequently U=J(J^*J)^(-1/2) is exactly the normalized Schur graph isometry
onto R_(N-1). If V is ordinary coordinate inclusion of C^(N-1), then
W=U^*V is unitary from the coarse coordinate space to P_N, and

    V=UW,
    H_(N-1)=W^* [(J^*J)^(-1/2)
                  (A-B^*D^(-1)B)(J^*J)^(-1/2)] W.          (10)

Thus the compatible inclusions are exact normalized Schur graph isometries
up to unitary coarse coordinates. Those coordinates can be chosen at every
step to make the root's equality literal. Appending the vacuum preserves
these statements; B annihilates the vacuum and U fixes it.

The projectors (9) are nonlocal and depend on the complete finite matrix.
This example therefore refutes an abstract automatic-closability claim,
not a locality-sensitive assertion about Yang–Mills blocks.

## 5. Even the eliminated inverse-gap cost is summable

Let T_(N-1)=sum_(i<N)2^(-i)<1. Sherman–Morrison gives

    H_N^(-1)=W_N^(-1)-z_N z_N^*/(N+1),
    (z_N)_i=2^(-i/2),
    (H_N^(-1))_(NN)=2^(-N) N/(N+1).

Since D on Q_N is scalar, its value d_N is

    d_N = <v_N,H_N v_N>/||v_N||^2,
    1/d_N = 2^(-N) N/(N+1) + T_(N-1)/[N(N+1)].             (11)

In particular sum_N 1/d_N<infinity. In fact its value is exactly 1:
interchanging the positive double sum in the second term gives

    sum_N T_(N-1)/[N(N+1)] = sum_(i>=1) 2^(-i)/(i+1),

which complements the first term to sum_N 2^(-N)=1.
The steps relevant to a fixed nonempty terminal space start at N=2; their
sum is 3/4. Exact Schur structure plus this favorable cost still leaves (8)
nonclosable.

## 6. Identify the limit rather than claiming its nonexistence

Embed H_N^(-1) into ell2 by zero off its first N coordinates. Formula (11)
shows that these embedded inverses converge even in operator norm to

    R=diag(2^(-i)),

because the diagonal truncation error is 2^(-(N+1)) and the rank-one term
has norm T_N/(N+1)->0. Hence BL1 gives the self-adjoint limiting Hamiltonian

    H=diag(2^i),
    D(q_H)={x:sum_i 2^i |x_i|^2<infinity},
    q_H[x]=sum_i 2^i |x_i|^2.                               (12)

The rank-one functional term in (8) is lost. For example,

    q_N[e_1]=4 for every N,  but q_H[e_1]=2,
    <e_1,exp(-tH_N)e_1> -> exp(-2t).

The lower bound exp(-4t) from the preserved Rayleigh quotient remains valid,
but preserving Rayleigh quotients did not preserve them in the limit. This
is exactly why finite form compatibility and finite-cutoff differentiation
of correlations cannot justify interchanging the cutoff limit with the
time derivative at zero. Equation (4) fails already for H_1=[4] and
H_2=[[4,2sqrt(2)],[2sqrt(2),8]], since the included e_1 is not an eigenvector
of H_2.

## 7. Consequence for the parent route

If the actual gauge-theory blocks supply exact vacuum-preserving isometries
and one compatible family of forms across cutoffs, plus the parent's uniform
gap estimate,
BL1 provides an abstract gapped Hamiltonian limit and preserves any finite
terminal excitation as a finite-energy correlation witness. This is stronger
than needing to assume an arbitrary semigroup limit from scratch.

But the result must be called an abstract inductive-limit Hamiltonian until
local physical observables, translations, their limiting correlations, and
the required field axioms are constructed. Even agreement of the limiting
closed form with the intended algebraic form needs additional regularity.
Neither exact Schur structure nor summability of (11) supplies that agreement.

Self-review: reconstructed (7) by completing the square; checked density
for inverse injectivity and continuity of f_t at zero; checked the exact
nonclosability sequence, unitary coordinate identification in (10), and all
entries in (11). The root independently recomputed (11). No numerical
experiment, external construction theorem, or full-QFT conclusion is used.
