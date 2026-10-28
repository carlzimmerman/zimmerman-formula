# Whole-layer coercivity: a working quadratic estimate and two failed extensions

Checkpoint YM-C3. Input commit `01b05ecab81a5a4876b429d09711180b7da01436`.
Date: 2026-09-22. Analytic derivation and self-review; no novelty claim.

**The requested weak-coupling, volume-uniform multiscale estimate for the
actual Yang–Mills Hamiltonian is not established.** This attempt constructs
and proves a whole-layer estimate in a covariant quadratic model, then tests
the two proposed extensions to the nonlinear problem. Both extensions fail
in the general form tested. These are failures of shortcuts, not a disproof
of the desired Yang–Mills estimate.

The estimate still sought is, at every exact elimination scale j,

    <f,H_j f> >= d_j ||f||^2 for f in ran(Q_j),
    sup_(volume,cutoff depth) sum_j d_j^(-1) < infinity,

with H_j in physical units, shifted by the actual vacuum energy, the induced
Schur metric retained, and Q_j constructed without assuming the target gap.
The terminal gap and continuum field construction remain separate obligations.

## 1. A whole-layer geometric inequality, uniform in background and volume

Let a finite cubic spatial lattice of dimension d have open or periodic
boundary conditions and be tiled by cubes of L^d sites, L>=2. For periodic
lattices take side lengths at least 2L. At each site put a real vector v_z
in R^r. Assign an orthogonal transport R_zw to each oriented nearest-neighbor
edge, with R_wz=R_zw^{-1}. This includes adjoint SU(N) transport. Define

    E_R(v) = sum_{unoriented edges zw} |v_z-R_zw v_w|^2,
    K_R = nabla_R^* nabla_R.

Choose a rooted spanning tree in each cube, with each root-to-site path of
length at most d(L-1). Let T_z transport v_z along that tree to the root,
and define the normalized block average

    (A_R v)_B = L^(-d/2) sum_{z in B} T_z v_z.

Then A_R A_R^*=I on the coarse vector space. Put F=ker A_R and

    C_(d,L) = d(L-1)L^d/2.

**Lemma 1.** For every choice of orthogonal transports and every v in F,

    ||v||^2 <= C_(d,L) E_R(v).                             (1)

The constant does not depend on the number of cubes or on r. All block
fluctuations are controlled simultaneously; this is not a sum of inverse
single-block gaps.

Proof. In one cube put m=L^d and w_z=T_z v_z. Their sum is zero. The variance
identity gives

    sum_z |w_z|^2 = (1/m) sum_{z<w} |w_z-w_w|^2.

A tree path has length at most D=2d(L-1). Cauchy–Schwarz along that path
bounds its endpoint difference by D times its edge energy. A tree edge
separates n_e and m-n_e vertices, so it occurs in n_e(m-n_e)<=m^2/4
unordered paths. Consequently the variance is at most

    (D m/4) sum_{tree edges} |w_z-w_w|^2.

On a tree edge, |w_z-w_w|=|v_z-R_zw v_w|. Summing over cubes and adding
the other nonnegative edge energies proves (1). The root and tree choices
are fixed geometric choices; no flatness assumption is used. Under a gauge
change O_z, T_z transforms to O_root T_z O_z^{-1}. Thus the average and its
kernel transform covariantly. Finally, E_R(v)<=4d||v||^2 by the degree bound,
so 0<=K_R<=4d I.

## 2. An actual vacuum-sector bound for the quadratic model

Fix 0<epsilon<=1 and K=K_R+epsilon I, Omega=sqrt(K). Consider the specified
oscillator Hamiltonian on L2(R^(r|Lambda|)):

    H_G = (1/(2a))[-x Delta_q + x^(-1) q^T K q], x,a>0.

Its normalized ground-state density is proportional to
exp(-q^T Omega q/x). This is a background-covariant Gaussian model, not the
compact-link Yang–Mills Hamiltonian. The background R is fixed, not integrated.

Let P_G be conditional expectation in this exact Gaussian ground measure
given A_R q, and Q_G=I-P_G. Define

    gamma_(d,L) = 1/[C_(d,L) sqrt(4d+1)].

**Proposition 2.** The ground-state transform of H_G-E_G, restricted as a
quadratic form to ran(Q_G), obeys

    D_G >= gamma_(d,L)/a.                                (2)

This holds uniformly in lattice volume, all transports R, x>0 and
epsilon in (0,1]. It does not assert a global oscillator gap uniform as
epsilon tends to zero.

Proof. Spectral calculus on 0<K<=4d+1 gives

    Omega >= K/sqrt(4d+1).

For v in F, (1) therefore gives

    <v,Omega v> >= gamma_(d,L)||v||^2.

The Gaussian conditional measure on an affine fiber of A_R has precision
2 Omega_FF/x, where Omega_FF is the compression to F. Its Poincare constant
is at most x/(2 gamma_(d,L)), independently of the conditional mean. Integrate
the conditional inequality over the coarse variables and use the exact form

    <f,psi_G^{-1}(H_G-E_G)psi_G f>
       = x/(2a) integral |grad f|^2 dmu_G.

Since the full gradient controls the fiber gradient, (2) follows. This
argument uses the compression of sqrt(K), not the generally different
square root of the compressed K. Conditional integration is over all fast
variables at once; no unproved tensorization of an interacting measure is used.

At a family of physical scales a_j=A L^(-j), separate models of this form
have the volume-uniform inverse budget

    sum_(j>=1) 1/d_j <= A/[gamma_(d,L)(L-1)].              (3)

Equation (3) is an estimate for a stated family of quadratic models. It
does not say they are successive exact normalized Schur transforms of
one another. That additional identification is precisely tested next.

## 3. Exact Schur elimination does not preserve the quadratic class

**Proposition 3 (counterexample).** Start with two bosonic modes and the
positive one-particle matrix

    h = [[2,1],[1,2]],       H=dGamma(h).

Let P retain every occupation state |n,0> with the second mode in its
vacuum. P preserves the true Fock vacuum. Define S,G and the normalized
Schur operator K_eff exactly as in `../blocking/SCHUR_GAP.md`.
Then K_eff is not a single harmonic oscillator: its first two positive
eigenvalues are 6/5 and 84/29, rather than omega and 2 omega.

Proof. Total particle number n is preserved by H,P and all the block maps.
For n=1 the retained sector is one-dimensional and

    S_1=2-1/2=3/2, G_1=1+1/4=5/4, K_1=6/5.

For n=2, in the ordered basis |2,0>, |1,1>, |0,2>,

    H_2 = [[4,sqrt(2),0],[sqrt(2),4,sqrt(2)],[0,sqrt(2),4]].

Writing D for the bottom-right two-by-two block and B=(sqrt(2),0)^T,

    D^{-1} B = (2 sqrt(2)/7,-1/7)^T,
    S_2=24/7, G_2=58/49, K_2=84/29 != 2 K_1.

To check these really are the first two positive levels, h>=I implies
H_n>=nI. The normalized graph embedding U_n is an isometry, so
K_n=U_n^*H_nU_n>=n. Therefore n>=3 cannot precede K_2<3.
The vacuum is K_0=0. The form construction is also legitimate on full
Fock space: D_n>=n for n>=1 and ||B_n||=sqrt(n), hence
||D_n^{-1}B_n||<=1/sqrt(n). The direct-sum graph operator is bounded.

Thus Gaussian integration of a coordinate density and the metric-normalized
Schur elimination of a quantum Hamiltonian are different transformations.
The covariance Schur complement alone cannot justify iterating (2) through
the earlier quantum bridge. This does not refute the bridge, and it does not
rule out controlling its generated operators in a larger class.

## 4. The nonlinear Wilson Hessian can be negative on block fluctuations

A second proposed extension would compare the full Wilson magnetic Hessian
to a positive covariant lattice Laplacian on discarded directions at every
background. The following actual SU(2) configuration refutes that extension.

On an even periodic cubic lattice in d>=2, let e_i be coordinate directions
and choose central links

    U_i(z)=(-I)^(sum_{k<i} z_k).

Every elementary plaquette is -I. Periodicity follows from even side lengths;
the product around each cube is consistent. All adjoint transports are the
identity because central elements act trivially in the adjoint representation.

Choose a real link field v and the Abelian variation

    U_i(z;t)=U_i(z) exp(i t v_i(z) sigma_3/2).

Commutativity gives U_p(t)=-exp(i t (dv)_p sigma_3/2), and therefore

    d^2/dt^2 [(b/x) sum_p (1-Re Tr U_p(t)/2)] at t=0
       = -b/(4x) sum_p |(dv)_p|^2.                        (4)

For b>0 this is strictly negative whenever dv is nonzero. In particular,
take a circulation around a single square inside a 2-by-2-by-... block:

    v_1(0)=1, v_2(e_1)=1, v_1(e_2)=-1, v_2(0)=-1,

with all other links zero. Its discrete divergence is zero. The sum of each
link component over the block's starting sites is zero, so it is a discarded
direction for componentwise block averaging, while (dv)_(12)(0)=4. It is
therefore neither a retained constant mode nor a pure infinitesimal gauge
direction. Since the background is central, the covariant versions of these
linear conditions agree with the ordinary ones.

This is a finite-lattice algebraic counterexample to a pointwise, all-background
positive-Hessian comparison. The negative direction persists in an open
neighborhood of this configuration by continuity. The actual finite-volume
ground function is positive there, but that fact provides no useful uniform
lower bound on the neighborhood's vacuum probability.

Equation (4) does NOT make H-E0 negative, does NOT imply a small discarded
quantum gap, and does NOT disprove weighted Poincare coercivity. A potential
can have negative curvature while its ground-state-transformed generator is
gapped. It shows why a proof based only on uniformly positive quadratic
fluctuations cannot cover the full compact configuration space. Regions of
large field strength need a separate estimate, in the actual vacuum measure.

## 5. What has and has not been established for actual Yang–Mills

At the already proved strong-coupling fixed-lattice endpoint, the existing
I15 bound does give D>=3x/(16a) for every discarded subspace orthogonal to
the true vacuum, uniformly in its stated open volumes. Any valid normalized
Schur graph restriction also preserves that lower gap, by its isometric
energy embedding. This is a consequence of the existing global theorem;
it does not extend its coupling range to x(a)->0.

At weak coupling the available unconditional actual-vacuum statement is
still the fixed-finite-block theorem of YM-C2. The estimate for a whole
elimination layer has now been proved only for the explicitly specified
quadratic model. No replacement of the nonlinear Yang–Mills vacuum by that
model, and no uniform control of the generated exact coarse operators, has
been proved.

The next mathematical input must handle the collective discarded variables
in the actual compact-link ground measure, including configurations outside
a small-field chart, and remain valid after exact elimination. Controlling
only a covariant Laplacian, repeating finite-block estimates, or assuming
that exact Schur elimination stays Gaussian would leave a specific missing
implication. The present calculation does not discharge it.
