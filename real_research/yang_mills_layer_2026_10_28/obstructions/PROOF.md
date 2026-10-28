# Explicit obstructions to automatic layer and Markov closure

Date: 2026-10-28. Requested base: YM-LAYER-2026-10-28-C0,
`5bb77f83c618cab437a705c7aa19d7fe0b7aead7`. The workspace HEAD observed
while preparing this record was `9c9d980ba0a972f1661de3b64d8296ea7edd5af6`.
Input content hashes, rather than an assumption that HEAD stayed fixed,
are recorded by the computation manifest.

## Claim cards and verdicts

1. **Automatic layer inference.** For local bounded-degree product
Schrodinger Hamiltonians with their actual positive vacuum, uniform
conditional Poincare inequalities for bounded individual blocks imply a
volume-uniform discarded gap for the collective fast layer.
**Verdict: refuted.** Section 1 gives a connected compact-product example
with fixed local interactions. It even admits a nontrivial retained coarse
variable at every site, constructed independently of the gap.

2. **Retaining pair means suffices in local oscillator models.** Uniform
one-pair conditional gaps plus locality imply a uniform gap after retaining
all pair means. **Verdict: refuted.** Section 2 uses a fixed-coefficient local
Gaussian actual vacuum and proves that the full discarded operator, not
only a fiber form, has gap tending to zero.

3. **Automatic Markov closure.** Orthogonal conditional expectation onto a
coarse probability algebra preserves the Markov property under exact Schur
elimination, with or without the induced metric normalization.
**Verdict: refuted.** Section 3 gives four states and exact rational entries.

These are obstructions to implications one might use. They are **not
counterexamples to a Yang--Mills mass gap**, and do not refute any theorem
stated in the current manuscript. Its fixed-block and conditional Schur
statements explicitly leave the necessary stronger hypotheses open.

## 1. A compact, local, bounded-degree actual-vacuum counterexample

### 1.1 The normalized vacuum and its local Hamiltonian

Let T_k be the rooted binary tree of depth k, with L=2^k leaves and
maximum degree three. At each vertex v put theta_v in R/(2 pi Z), with
normalized Haar measure. Define the fixed smooth edge kernel

    p(t) = 16(1+cos t)^3+1,
    kappa(t) = p(t)/41
             = 1+(60/41)cos t+(24/41)cos(2t)+(4/41)cos(3t).

Thus integral kappa=1, 1/41 <= kappa <= 129/41, and its first Fourier
coefficient is t_1=30/41. Set

    dmu_k(theta) = product_{uv in E(T_k)} kappa(theta_u-theta_v) dtheta,
    psi_k = product_{uv in E(T_k)} sqrt(kappa(theta_u-theta_v)).

Successively integrating leaves proves integral dmu_k=1. Equivalently,
sample the root uniformly and each child independently, conditional on its
parent, with the transition density kappa. In particular every one-site
marginal is Haar. All square roots are of strictly positive functions.

Put F=log psi_k and construct the genuine Schrodinger operator

    H_k = -sum_v partial_v^2 + V_k,
    V_k = sum_v [partial_v^2 F + (partial_v F)^2].                 (1)

This is not an assumed replacement of a ground measure: H_k psi_k=0
pointwise and, for every smooth f,

    <psi_k f,H_k psi_k f> = integral sum_v |partial_v f|^2 dmu_k. (2)

Hence H_k>=0, its strictly positive normalized ground function is psi_k,
and its kernel is one-dimensional. The last claim follows directly from
(2), since a zero-gradient function on the connected product torus is
constant; multiplication by the smooth positive psi_k preserves H^1 on
each finite product. Compact ellipticity gives the corresponding operator
and form statements without a uniform bound on the total potential.

The potential is local with constants independent of k. If
a=(log kappa)' and b=(log kappa)'', then

    V_k = sum_v W_v,
    W_v = (1/2) sum_{w~v} b(theta_v-theta_w)
          +(1/4) [sum_{w~v} a(theta_v-theta_w)]^2.                (3)

Each W_v depends only on a vertex and its at most three neighbors.
Every coordinate occurs in at most four such stars. The same functions
a,b are used at every volume, with only degrees one, two and three.
They are bounded because p>=1. For explicit loose bounds,
|p'|<=192, |p''|<=384, so |a|<=192 and |b|<=37248.
Consequently W_v>=-55872 and |W_v|<=138816.
If a nonnegative potential is desired, use W_v+55872 in (1) and subtract
the actual ground energy 55872 |V(T_k)|. This leaves (2) unchanged.

### 1.2 Uniform individual-block conditional inequalities

Given all variables except theta_v, its conditional density is
proportional to at most three kappa factors. Its maximum/minimum ratio
is at most 129^3. The Haar circle Poincare inequality has gap one.
The minimizing-constant variance formula therefore proves

    Var(f | theta_{u != v})
       <= 129^3 integral |partial_v f|^2 dmu_k(. | exterior).    (4)

After integration, the full ground form in (2) controls each individual
discarded subspace with gap at least 129^-3, uniformly in k and the
exterior configuration. For any set B of at most m vertices, the number
of incident edges is at most 3m. The same argument and product Haar
Poincare inequality give the uniform fixed-m bound 129^(-3m).
Neither bound asserts a constant uniform in m.

### 1.3 Exact collective mode and vanishing full discarded gap

The transition kernel gives

    E[exp(i theta_child) | theta_parent]
       = t_1 exp(i theta_parent),       t_1=30/41.

Conditional independence below a common ancestor, or iteration along
the unique path, yields the exact covariance

    E[cos theta_u cos theta_v] = (1/2) t_1^{dist(u,v)}.           (5)

Take f_k=sum_{v a leaf} cos theta_v. Its mean is zero. A fixed leaf has
2^{d-1} other leaves at distance 2d, for 1<=d<=k. Therefore

    ||f_k||^2 = (L/2) [1+(1/2) sum_{d=1}^k R^d],
    h_k[f_k] = L/2,
    R = 2 t_1^2 = 1800/1681 > 1.                              (6)

The second identity uses the Haar marginal and the fact that only leaf
derivatives are nonzero. The exact Rayleigh quotient is

    h_k[f_k]/||f_k||^2
      = [1+(1/2) sum_{d=1}^k (1800/1681)^d]^-1 -> 0.           (7)

This tests the full gradient form (2); no omitted exterior derivatives
can repair this upper bound. With P the expectation onto constants,
f_k is in ran(I-P), so the whole-layer discarded gap tends to zero
despite (4) and every fixed-m version of it.

To make the retained algebra extensive and nontrivial, add an independent
Haar rotor eta_v at every vertex and the free kinetic term
-sum_v partial_{eta_v}^2. The actual ground function remains psi_k(theta).
Retain the explicitly chosen coarse variables

    zeta_v = theta_v + eta_v mod 2 pi,
    P = E_mu[ . | all zeta_v ].                               (8)

The change (theta,eta)->(theta,zeta) preserves Haar volume, and the joint
measure is mu_k(dtheta) times product Haar(dzeta). Thus P f_k=0. The
full energy of f_k is still L/2, and (7) is an upper bound for the
actual whole-layer D defined by (8). No gap is used to choose P.

The individual fast fiber in a pair (theta_v,eta_v) at fixed zeta_v has
metric 2 dtheta_v^2. Its intrinsic energy is one half the coordinate
derivative energy, so (4) yields a uniform conditional fiber gap
at least (1/2)129^-3. The original full gradient controls this fiber
gradient because

    (1/2)|partial_theta f-partial_eta f|^2
       <= |partial_theta f|^2+|partial_eta f|^2.

Thus the counterexample also has uniformly controlled individual fast
fibers under a prescribed retained group-product variable in each pair.

### 1.4 Scope and the missing parameter

This is a connected compact-product Schrodinger example, with finite-range
bounded-degree interactions, a strictly positive actual vacuum, and
uniform individual-block conditional inequalities. It shows that these
properties alone do not control collective correlations. The exact factor
R=2 t_1^2 separates this leaf-mode mechanism: at R>1, branching beats
decay along a path. At R=1 the bracket in (7) grows linearly in k as well.
R<1 only prevents this particular test from closing the gap; it is not
proved here to imply a spectral gap.

The graph family is a tree with a macroscopic boundary, not a fixed-dimensional
cubic lattice. The group is U(1), the potential is engineered by (1), and
it is neither Wilson plaquette form nor gauge invariant in the Yang--Mills
sense. Thus this does not refute an inference that also uses specific
cubic geometry, gauge structure, or Wilson interactions. Such additional
input must be stated and proved; a bounded-degree appeal alone is insufficient.

## 2. Fixed local Gaussian example with all pair means retained

There are n cells, with q_{i,1},q_{i,2} in R. Define orthonormal coordinates

    c_i=(q_{i,1}+q_{i,2})/sqrt(2),
    r_i=(q_{i,1}-q_{i,2})/sqrt(2).

Let L_n be the Dirichlet chain matrix with diagonal 2 and adjacent
off-diagonal -1. In (c,r) coordinates set Omega=I_n direct-sum L_n,
and let

    psi(q) = Z^-1/2 exp[-q^T Omega q/4],
    H = -Delta_q +(1/4)q^T Omega^2 q -(1/2)Tr Omega.             (9)

Here Omega in q coordinates is the orthogonal conjugate just specified.
Its squared matrix has range at most two cells and coefficients bounded
independently of n. Equation (9) is an actual local oscillator Hamiltonian
with zero ground energy, positive normalized ground function psi, and
ground form integral |grad f|^2 dmu. The ground density has precision
I_n direct-sum L_n. The finite-size boundary prescription is Dirichlet;
no parameter tends to zero in the local coefficients.

Given all other cells, the pair (c_i,r_i) has precision diag(1,2).
Its conditional Poincare gap is one, uniformly in n and the exterior
conditional mean. Thus each one-cell discarded operator is bounded below
by one by conditional integration and the full-gradient inequality.

Retain all c_i, precisely the normalized pair means, and set
P=E_mu[. | c]. The r variables are independent of c. The conditional
fast precision is L_n, whose eigenvectors sin(ij pi/(n+1)) have
eigenvalues 2-2 cos(j pi/(n+1)), by direct substitution. Conditional
Gaussian Poincare and the corresponding linear eigenfunction give the
exact full discarded gap

    gap D_n = 2-2 cos(pi/(n+1)) -> 0.                          (10)

For a purely rational witness avoiding the spectral formula, f=sum_i r_i
belongs to ran(I-P), has energy n, and variance

    1^T L_n^-1 1 = n(n+1)(n+2)/12.

Indeed (L_n^-1 1)_i=i(n+1-i)/2, as direct substitution verifies. Thus

    gap D_n <= 12/[(n+1)(n+2)].                               (11)

This example is noncompact and has a deliberately chosen local quadratic
potential. It does not refute the earlier Gaussian result for the specific
precision sqrt(K_R+epsilon I): that result proves an additional geometric
lower bound on its fast compression. Locality and retention of an average
do not supply that lower bound for arbitrary oscillator potentials.

## 3. Independent audit: conditional Schur elimination loses Markovness

This candidate was supplied by the separate coarse-operator investigation;
the derivation below was reconstructed from its original four-state form.
Let the fine probabilities be (1/6,1/6,1/3,1/3) and let

    h[f] = (1/3)[(f_1-f_3)^2+(f_2-f_4)^2+(f_1-f_2)^2/2].     (12)

This is a connected reversible Markov Dirichlet form: every edge
conductance is positive. Its kernel consists of constants. Retain the
partition {1,2},{3},{4}; its three probabilities are all 1/3 and P is the
orthogonal conditional expectation. Write

    p=(a,a,b,c),       q=(t,-t,0,0).

Then ||q||^2=t^2/3 and

    h[p+q] = (1/3)[(a-b)^2+(a-c)^2+2t(c-b)+4t^2].             (13)

Consequently D=4, the minimizing lift has t=(b-c)/4, and the Schur
operator on the coarse L^2 probability space is

    S = [[ 2, -1,  -1 ],
         [-1, 3/4, 1/4],
         [-1, 1/4, 3/4]].

Let v=(0,1,-1). The induced metric is G=I+v v^T/16. The vectors
1, v, and w=(-2,1,1) diagonalize both S and G:

    S: eigenvalues 0, 1/2, 3;
    G: eigenvalues 1, 9/8, 1.

The exact normalized operator K=G^-1/2 S G^-1/2 is therefore

    K = [[ 2, -1,    -1   ],
         [-1, 13/18, 5/18 ],
         [-1, 5/18,  13/18]].                               (14)

Both operators fix constants but have positive off-diagonal entries in
the coarse point basis. More directly, the normal contraction z->|z|
fails for z=(0,1,-1):

    <z,Sz>_mu=1/3,    <|z|,S|z|>_mu=2/3;
    <z,Kz>_mu=8/27,   <|z|,K|z|>_mu=2/3.                    (15)

Thus neither form is Markov on this coarse probability space. There is
no contradiction with trace/Kron reductions that fix actual boundary
values: the present elimination fixes conditional block averages and
allows their within-block deviations to minimize energy.

This refutes only automatic preservation. A proposed exact-elimination
scheme can still work in a larger class, or could establish Markovness
from additional structure absent from (12).

## 4. Audit map, evidence, and outstanding Yang--Mills obligations

Dependency map:

* Section 1: explicit positive kernel -> tree probability factorization ->
  actual local ground-state identity -> single-block comparison and exact
  collective Rayleigh quotient. All steps are internal analytic arguments.
* Section 2: specified positive precision -> exact oscillator ground form ->
  block conditional precision and an admissible Q-linear witness. The
  Gaussian Poincare step also follows by diagonalizing independent
  one-dimensional Gaussian Ornstein--Uhlenbeck forms; (11) alone suffices
  for the counterexample and needs no lower-gap theorem.
* Section 3: specified reversible four-state form -> conditional P/Q
  decomposition -> completion of squares -> exact G normalization ->
  contraction violation. All steps are finite rational algebra.

Obligation matrix: actual-vacuum identity, locality, bounded degree,
nontrivial retained algebra, individual conditional bounds, full-gradient
Q-witness, and exact finite Schur signs are **passed by the written
derivations**. SU(N) Wilson identification, cubic-volume uniformity,
gauge-invariant coarse variables for actual Yang--Mills, weak-coupling
trajectory, generated-operator closure, and continuum spectral transfer
are **out of scope / still open**.

`check.py` independently recomputes the polynomial Fourier coefficients,
enumerates all ordered leaf pairs for depths 0 through 5, checks the
Gaussian rational witness and locality for sizes 1 through 20, and checks
the four-state Schur algebra over exact rational numbers. No sampling or
floating-point acceptance criterion is used. Its finite ranges do not
prove the all-depth/all-size statements; those follow from the identities
above. The run contract and validated v2 manifest give the exact command,
input hashes, software version, and tested range.

Review status: new Sections 1 and 2 have author-side self-review only at
the time this file was written. Section 3 is a separate analytic audit of
the supplied four-state candidate, not independent human peer review.
No external theorem, novelty claim, manuscript edit, or continuum theorem
is asserted by this record.
