# YM-C1-C: continuum spectral transfer and a collapse obstruction

Assigned base: `b73311096299e2f1816be00036ccdb2922bc44d4`.
Owner: `ym_continuum`. Date: 2026-09-22.
Write scope: this `continuum/` directory only.

**Status.** The transfer lemmas and counterexamples below are elementary
operator proofs. Their application to four-dimensional Yang–Mills is conditional
on an actual continuum construction and the displayed estimates. The Clay
problem has not been solved. No novelty claim is made.

## 1. Target and units

The official Jaffe–Witten formulation requires, for every compact simple group,
a nontrivial Yang–Mills QFT on R^4 with the stated axiomatic strength. Its
Hamiltonian mass is positive **and finite**. The surrounding definition includes
gauge-invariant local curvature observables and the prescribed short-distance
behavior. Thus a one-dimensional vacuum theory is insufficient. These are the
source-dependent target facts used here; see [SOURCES.md](SOURCES.md), §JW.

Write the spacing-one Hamiltonian of I15 as H_lat(x), where x=g^2, and let
E_lat be its actual vacuum energy in finite volume. In units hbar=c=1,

    K_a = [H_lat(x(a)) - E_lat(x(a))]/a,
    Delta_phys(a) = Delta_lat(x(a))/a,
    exp(-t K_a) = exp[-(t/a)(H_lat-E_lat)].                    (1)

The infinite-volume version uses the ground-state GNS generator, whose vacuum
energy is already zero. No infinite extensive vacuum energy is subtracted as
a number. The factor 1/a is part of the Hamiltonian normalization in the
contract, not a conclusion inferred from a Euclidean transfer matrix. If a
different time calibration is introduced, it must be carried through (1).

I15 gives Delta_lat >= 3x/16 for x>=X_d, uniformly in volume and N. That is a
strong-coupling statement at fixed spacing. The proof below determines exactly
what it does and does not supply after division by a.

## 2. Common observable and continuum contract

Let a_n -> 0. At cutoff n let H_n be a Hilbert space, Omega_n a unit vacuum,
and K_n a nonnegative self-adjoint physical Hamiltonian with K_n Omega_n=0.
Let V be a complex vector space of labels and let

    F -> psi_n(F) in Omega_n^perp

be linear. A standard choice is

    psi_n(F) = [A_n(F)-omega_n(A_n(F)) I] Omega_n.              (2)

The observable prescription must use the actual interacting state omega_n;
it may include a linear renormalization/mixing prescription and smearing.
Products and linear combinations of local observables must be included if
needed for cyclicity. Looking only at one elementary field need not suffice.

Define positive diagonal time correlations and their Gram forms by

    C_n(F,G;t) = <psi_n(F), exp(-t K_n) psi_n(G)>,
    G_n(F,G) = C_n(F,G;0).                                   (3)

The continuum input used below is:

* There are a Hilbert space H, unit Omega, nonnegative self-adjoint K with
  K Omega=0, and a linear map psi:V -> Omega^perp.
* psi(V) is dense in Omega^perp. In particular it is a vector subspace, not
  merely a collection whose linear span is dense.
* For every F,G in V, G_n(F,G) -> <psi(F),psi(G)> and the time correlations
  at the times used below converge to
  C(F,G;t)=<psi(F),exp(-tK)psi(G)>.

Call this contract **CT**. A QFT construction must establish considerably more,
including its field algebra, locality, covariance, ultraviolet regularity, and
the Yang–Mills identification. CT supplies only the Hilbert and time-evolution
interface needed for spectral transfer. Positive scalar kernel limits alone
must not be silently promoted to CT: semigroup composition, strong continuity,
and coverage of the reconstructed state space still require proof.

For diagonal results one only needs the diagonal convergence. Polarization
recovers the mixed Gram/correlation limits when all complex linear combinations
in V are included.

## 3. A single physical-time contraction is sufficient

**Theorem C1.** Assume CT. Fix tau>0 and 0<q<1. Suppose, for every F in V,

    limsup_n [C_n(F,F;tau) - q G_n(F,F)] <= 0.                (4)

Then zero is a simple eigenvalue of K, and

    spec(K) subset {0} union [m_0,infinity),
    m_0 = -log(q)/tau > 0.                                  (5)

The Hilbert space may still be one-dimensional; see C3 below.

**Proof.** Passing to the limit in (4) gives

    <psi(F), exp(-tau K) psi(F)> <= q ||psi(F)||^2.

Omega^perp reduces K since Omega is a zero eigenvector. The bounded positive
operator exp(-tau K) restricted to this subspace therefore has quadratic form
at most q on a dense vector subspace, hence everywhere by continuity. For any
0<=r<m_0, a vector in its spectral subspace E_K([0,r])Omega^perp would satisfy

    exp(-tau r)||v||^2 <= <v,exp(-tau K)v> <= q||v||^2.

Since exp(-tau r)>q, v=0. Increasing r to m_0 excludes [0,m_0) on
Omega^perp, proving (5) and vacuum uniqueness. QED.

The bound need not hold for all n or for all vectors at each cutoff. Vanishing
errors r_n(F) in C_n<=qG_n+r_n(F) suffice. The constants q and tau, however,
are common to the whole dense vector subspace. Checking (4) on selected basis
vectors without their linear combinations is insufficient; see §7F.

**Corollary C2 (cutoff gaps).** Assume CT at every positive time and suppose
K_n has simple vacuum and gap at least m_n. If

    liminf_n m_n >= m_*>0,

then K has simple vacuum and gap at least m_*.

**Proof.** For any 0<m<m_*, all sufficiently large n satisfy
C_n(F,F;t)<=exp(-mt)G_n(F,F). Apply C1 with q=exp(-m tau), then let
m increase to m_*. The endpoint version follows directly by spectral
exclusion. QED.

For (1), the sufficient cutoff hypothesis is

    liminf_n Delta_lat(x(a_n))/a_n > 0,                      (6)

with volume and observable coverage as in CT. Positivity of Delta_lat at each
individual a_n is not (6).

## 4. Large-time decay and the role of constants

**Theorem C2b.** Assume CT at every t>0. Let D be any total set in Omega^perp.
Suppose every u in D satisfies, for a common delta>0,

    <u,exp(-tK)u> <= M_u exp(-delta t),  t>=T_u,             (7)

where M_u<infinity and T_u<infinity may depend on u. Then the conclusion of C2
holds with m_*=delta.

**Proof.** For 0<=r<delta, positivity of the spectral measure gives

    ||E_K([0,r])u||^2 exp(-rt)
      <= <u,exp(-tK)u> <= M_u exp(-delta t).

Let t go to infinity. The spectral projection annihilates D, hence its closed
linear span Omega^perp. Let r increase to delta. QED.

Thus the decay rate must be common; the prefactor and onset need not be
uniform across observables. To pass (7) from cutoffs it is sufficient, for
each fixed label, that its prefactors stay bounded and its onset times have a
finite common upper bound as n varies. Divergent prefactors or onset times
cannot simply be discarded before taking n->infinity. C1 is quantitatively
different: at one time its norm-relative bound is required on every linear
combination in a dense subspace.

The diagonal positivity here is essential. A mixed correlation
<u,exp(-tK)v> may vanish by orthogonality even in a gapless theory.

## 5. A finite-energy witness and avoidance of triviality

**Theorem C3.** Under C1, suppose some F_0 in V and constants 0<v<=M<infinity
satisfy

    liminf_n C_n(F_0,F_0;tau) >= v,
    limsup_n G_n(F_0,F_0) <= M.                              (8)

Then Omega^perp is nonzero, and its spectral bottom m obeys

    0 < m_0 <= m <= tau^(-1) log(M/v) < infinity.            (9)

**Proof.** The limiting vector u=psi(F_0) has C(u;tau)>=v>0 and norm
squared at most M, so u is nonzero. A nonzero vector has spectral measure
on some bounded interval: E_K([0,R]) increases strongly to I as R increases.
Thus m is finite. Since all its spectral support lies above m,

    v <= <u,exp(-tau K)u> <= exp(-tau m)||u||^2
      <= exp(-tau m)M.

Rearrange, and use (5). QED.

One may replace (8) by norm nondegeneracy plus a uniform energy expectation
bound on an admissible vector, as follows. Condition (8) is often easier to
express in Euclidean correlators and does not require differentiating at zero.
It proves a nonzero observable sector and a finite Hamiltonian mass, not by
itself a non-Gaussian Yang–Mills field theory.

**Lemma C3b (witness extraction).** Suppose centered vectors u_n in the form
domain of K_n satisfy

    0<c<=||u_n||^2<=M,
    ||K_n^(1/2)u_n||^2 / ||u_n||^2 <= E < infinity.          (9a)

Then <u_n,exp(-tau K_n)u_n> >= c exp(-tau E) for every tau>0.
Indeed, normalize the spectral measure by ||u_n||^2 and use Jensen's
inequality for the convex function exp(-tau lambda). If these are the
convergent observable vectors in CT, they furnish (8).

More explicitly, whenever ||u||^2<=M and C(u;tau)>=v, the spectral weight
w_R=||E_K([0,R])u||^2 satisfies

    w_R >= [v-M exp(-tau R)]/[1-exp(-tau R)] > 0            (9b)

for R>tau^(-1)log(M/v). This follows by bounding the integrand by 1 below R
and by exp(-tau R) above R. Under C1 that nonzero weight lies in [m_0,R].
Thus the correlation witness prevents all observable spectral weight from
escaping to infinite energy. Abstract cutoff trial vectors do not suffice
unless they belong to a family with the continuum identification in CT.

### Positive-time regularization

Unsmeared or coincident-point composite fields can have divergent G_n. A
legitimate alternative is to fix s>0 and replace the vectors by

    chi_n(F) = exp(-s K_n) psi_n(F),
    G_n^s(F,G) = C_n(F,G;2s),
    C_n^s(F,G;t) = C_n(F,G;2s+t).                            (10)

Apply C1 and C3 to chi_n, requiring finite limits at 2s and 2s+tau. This
is a fixed positive physical separation; its number of lattice time units
diverges as a goes to zero. If psi(V) was dense in Omega^perp, so is the span
of exp(-sK)psi(V): exp(-sK) is bounded and has dense range, since it is
self-adjoint with zero kernel. When original continuum psi(F) are undefined,
the regularized vectors themselves must be shown dense by the construction.

Multiplicative field renormalization cancels in each ratio C_n^s/G_n^s. It
cannot repair a divergent physical lower gap while keeping G_n^s bounded and
C_n^s(tau) bounded below.

## 6. The strong-coupling collapse theorem

**Theorem C4.** Suppose K_n has simple vacuum and gap >=m_n with m_n->infinity.
For a family satisfying CT with finite Gram limits,

    C(F,F;t)=0 for every F and t>0.

Strong continuity at t=0 forces psi(F)=0. If these vectors are dense in the
excited complement, H=span{Omega}. The same assertion applies to the
regularized contract (10).

**Proof.** For each fixed t>0,

    0 <= C_n(F,F;t) <= exp(-m_n t)G_n(F,F) -> 0.

Take n->infinity and then t down to zero, using strong continuity of exp(-tK).
The regularized proof uses bounded G_n^s in the identical estimate. QED.

For any sequence staying in I15's regime x(a_n)>=X_d>0, its lower bound gives

    m_n >= 3x(a_n)/(16a_n) -> infinity.                      (11)

Consequently that regime cannot produce a nontrivial strongly continuous
continuum limit under CT, even after positive-time regularization. The
obstruction is stronger than the absence of a proof: a proposed construction
that simultaneously asserts CT, nontriviality, and this scaling of I15 is
inconsistent. This does not refute Yang–Mills; it rules out this fixed-regime
continuum route and fixes the energy normalization a successful route needs.

## 7. Explicit failures of tempting weaker statements

### A. Positive gaps at every cutoff can converge to a gapless theory

On H=C Omega direct-sum L2((0,1),dx), put

    a_n=1/n,  K_n=0 direct-sum M_(x+1/n),
    H_lat,n=a_n K_n.

Each K_n has a unique vacuum and physical gap 1/n; each H_lat,n has lattice
gap 1/n^2>0. K_n converges in operator norm to K=0 direct-sum M_x. Its
vacuum is still unique because {x=0} has measure zero, but spec(K) contains
[0,1], so there is no mass gap. All bounded-time semigroup and dense-vector
correlation limits exist. For the centered unit vector 1 in L2((0,1)),

    C_n(t)=exp(-t/n)(1-exp(-t))/t,
    C(t)=(1-exp(-t))/t,  C(0)=1.

The large-time decay is polynomial. This example preserves continuum vacuum
uniqueness, unlike the less informative two-level example with a gap falling
to zero and producing a degenerate vacuum.

### B. Diverging physical gaps do not give finite-mass nontriviality

On C^2 let K_n=diag(0,n), Omega=e_0, and psi_n=e_1. Then G_n=1 while
C_n(t)=exp(-nt)->0 for every t>0. The pointwise limit is discontinuous at
zero and therefore is not the matrix element of a strongly continuous
semigroup with the nonzero limiting vector e_1. If instead psi_n=n^(-1)e_1,
all Gram and correlation limits vanish and the observable Hilbert space
collapses to the vacuum. A spectral exclusion with an arbitrarily large
lower bound does not construct the requested theory.

### C. A single observable can decay exponentially in a gapless theory

On C Omega direct-sum C e direct-sum L2((0,1)), let

    K=0 direct-sum 1 direct-sum M_x,
    A=|e><Omega|+|Omega><e|.

A is bounded and centered, and <A Omega,exp(-tK)A Omega>=exp(-t). Yet
K is gapless because of the L2 summand. The chosen observable algebra misses
that sector. Finite families can miss sectors in exactly the same way.

### D. A positive rate for each observable is not a common positive rate

On C Omega direct-sum ell2(N), let K e_j=j^(-1)e_j. Every finitely supported
centered vector has exponential decay with some positive rate depending on
its largest occupied j. Their span is dense, the vacuum is unique, and the
full theory is gapless. The missing quantifier is a common delta>0 in (7).

### E. Uncentered or merely mixed correlations do not certify the gap

The identity observable has <Omega,I exp(-tK)I Omega>=1 in every model.
Two centered vectors with disjoint spectral supports have mixed correlation
zero in every model, including gapless ones. A gap criterion uses positive
diagonal correlations of vectors orthogonal to the actual vacuum. Neither
the electric trial state nor an arbitrary scalar energy subtraction provides
that orthogonality.

### F. A one-time bound on a total basis is insufficient

Let u,v be orthonormal excited eigenvectors with energies epsilon=1/10 and
M=10. Put f_1=(u+v)/sqrt(2), f_2=(u-v)/sqrt(2), tau=1, q=1/2.
Each f_i has unit norm and

    <f_i,exp(-K)f_i> = (exp(-1/10)+exp(-10))/2 < 1/2.

The strict inequality is exact: exp(-1/10)<10/11 and exp(-10)<1/11,
using exp(y)>1+y for y>0. Also log(2)>=1/2>1/10.
They span the excited space, but its gap is 1/10<log(2). The vector
f_1+f_2 isolates u and violates (4). Hence C1 requires a dense vector
subspace with the inequality on every combination, equivalently a matrix
inequality for every finite family, not just diagonal tests of its members.

## 8. Exact quantitative target for the next route

The following is a concrete sufficient **conditional interface**, not a
new unconditional solution. At one fixed physical tau>0, construct a cyclic
renormalized observable space V and finite limiting Gram/time matrices. Prove
that, for every finite family F_1,...,F_k and coefficients z_1,...,z_k,

    limsup_n sum_ij conjugate(z_i) z_j
       [C_n(F_i,F_j;tau)-qG_n(F_i,F_j)] <= 0,  0<q<1,       (12)

and exhibit one label with the lower correlation and upper norm bounds (8).
Under CT this supplies a simple vacuum and the two-sided finite mass window
(9). A QFT construction still has to verify the rest of the target in §1.

If the root block route proves vacuum-subtracted physical cutoff gaps by

    gap(K_n) >= [gamma^(-1)+sum_j d_j^(-1)]^(-1),             (13)

with gamma>0 and sum_j d_j^(-1)<=S<infinity uniformly in the cutoff and
volume, then C2 gives a continuum gap >=(gamma^(-1)+S)^(-1), conditional on
CT. Equation (13) is an input from the block route, not proved here. Neither
summability nor a terminal coarse gap supplies the nontriviality witness (8).

### Weak-coupling mass scale, with explicit conditional status

For clarity this paragraph assumes, rather than proves for the lattice
Hamiltonian, a physical coupling calibration at mu=1/a with

    mu dg/dmu = -beta_0 g^3-beta_1 g^5+O(g^7), beta_0>0.      (14)

The notation beta_i avoids confusion with I15's magnetic coefficient b_N.
Elementary inversion and integration give

    d log(mu)/dg = -1/(beta_0 g^3)
                   +beta_1/(beta_0^2 g)+O(g),
    a Lambda = exp[-1/(2 beta_0 g^2)]
                 (beta_0 g^2)^[-beta_1/(2 beta_0^2)]
                 [1+O(g^2)].                               (15)

The multiplicative integration constant is absorbed into Lambda. This is a
conditional asymptotic calculation, not a nonperturbative existence theorem
or a checked beta function for every normalization in I15. No numerical
beta coefficients are borrowed across those normalizations.

If a finite nonzero cutoff mass itself converges, Delta_phys(a)->m, then
Delta_lat(a)=a m[1+o(1)] by (1). Along (15), the corresponding lattice gap
is exponentially small in 1/g^2, up to the displayed power. A sufficient
lower-bound target is Delta_lat(a)>=c a Lambda with c>0, together with CT
and (8). Equality or an asymptotic mass coefficient is not needed for C2.

Conversely, if along (15) one somehow proved Delta_lat>=c g^p for any fixed
real p and c>0, then Delta_lat/a->infinity because the exponential dominates
every power. C4 would force collapse under CT. Thus extending I15's algebraic
lower bound all the way to g->0 would contradict the desired finite-energy
continuum sector. A successful weak-coupling bound must have the right scale;
mere preservation of positivity is inadequate.

## 9. Remaining implication

The source I15 supplies neither CT along x(a)->0, the quantitative estimate
(12) in that regime, nor a finite-energy nontriviality witness. The exact
new information is the transfer interface and the impossibility of combining
the fixed strong-coupling lower gap with a regular nontrivial scaling limit.
The nearest executable target is the common Gram-matrix contraction (12)
plus one positive correlation witness, after a genuine gauge-preserving
renormalization construction supplies the observables and their limits.
