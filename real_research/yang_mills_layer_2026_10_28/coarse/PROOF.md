# Exact coarse reduction: comparisons, metric bookkeeping, and a Markov obstruction

Base checkpoint: YM-LAYER-2026-10-28-C0. Requested base commit:
`5bb77f83c618cab437a705c7aa19d7fe0b7aead7`. Owner:
`/root/layer_coarse_closure`. Date: 2026-10-28.

**The actual Yang--Mills uniform-layer and all-scale theorem is not proved.**
The results below are self-contained conditional comparison theorems and an
exact finite-state obstruction. They do not assume that an exact Schur
operator is a local Wilson Hamiltonian or even a Markov generator. The
conditional score bounds required below have not been established for the
actual Yang--Mills vacuum. No novelty claim is made.

## 1. One-step reference-form comparison

Let X and Y be compact connected Riemannian product manifolds. Let
`dμ(x,y)=ρ(x,y)dxdy`, with ρ smooth and strictly positive. Write μ_y for
the conditional measure on X and ν for the marginal on Y. Set

    e[f] = t ∫ (|∇_X f|²+|∇_Y f|²) dμ,  t>0,
    Pf(y) = ∫ f(x,y)dμ_y(x),
    e_Y[u] = t ∫ |∇_Y u|²dν.

Assume, uniformly in y,

    Var_{μ_y}(f) ≤ λ^(-1) ∫ |∇_X f|²dμ_y,  λ>0.          (1)

The centered conditional score is

    σ(x,y) = ∇_Y logρ(x,y) − ∫∇_Y logρ(v,y)dμ_y(v).

Assume its covariance operator on the Y tangent space satisfies

    ∫ σ⊗σ dμ_y ≤ M² I.                                  (2)

This is an operator-norm bound, not a bound on the trace of this covariance.
Put β=M²/λ. Then

    e_Y[Pf] ≤ (1+β)e[f].                                 (3)

Indeed, differentiating the conditional integral gives

    ∇_Y Pf = P∇_Y f + P[(f−Pf)σ].

The second term has squared norm at most M² Var_{μ_y}(f).
Jensen, (1), and Cauchy--Schwarz in R² give

    |∇_Y Pf|² ≤ (1+β)P(|∇_Y f|²+|∇_X f|²).

This proves (3). The same proof applies to complex f by the Hilbert-space
Cauchy--Schwarz inequality. Smooth approximation extends it to H¹.

A sufficient derivative hypothesis for (2) is a pointwise mixed Hessian
bound `||∇_X∇_Y logρ||_op≤L`. For a fixed Y tangent vector v, apply (1)
to the scalar score component v·∇_Y logρ. It gives
`Var(v·∇_Y logρ)≤L²|v|²/λ`; hence M≤L/√λ and β≤L²/λ².
This is only a sufficient replacement hypothesis. No such bound on
the actual Yang--Mills log vacuum, or on all its marginal log densities,
has been proved here.

Define the variational Schur form

    s[u] = inf { e[f] : Pf=u }.

The constrained minimizer is `J u=u−Cu`, with `Cu∈ker P`; it exists and is
unique because (1) makes e coercive on ker P. Consequently

    (1+β)^(-1)e_Y[u] ≤ s[u] ≤ e_Y[u].                    (4)

The upper bound uses f=u and the lower bound applies (3) to every admissible
f. The domain is H¹(Y), and (4) gives closedness by equivalence of form
norms. Orthogonality of the minimizing graph to ker P in the e inner
product gives

    e[Cu]=e[u]−s[u] ≤ β s[u],
    ||Cu||² ≤ β/(tλ) s[u].                              (5)

Thus the metric correction is controlled by energy even when no uniform
L² operator norm for C has been obtained. Equation (5) is not by itself a
proof that C is a bounded or closable L² operator; Section 5 addresses this.

The hypotheses do not assume a global gap. For example, X can have a fixed
gap while an independent Y factor has a gap tending to zero; then M=0,
(1)--(5) remain uniform and no global uniform gap follows.

## 2. Nonlocal reference-form class under successive variational reduction

Let Z_i be nested retained coordinate sets, with Z_0 all coordinates,
Z_{i+1} obtained by integrating X_i⊂Z_i, and μ_i the original marginal on
Z_i. Let H_i=L²(μ_i), embedded isometrically in H_0. Let E_i:H_0→H_i be
conditional expectation, and let P_i=E_{i+1}|H_i, Q_i=I−P_i.
All energies use the same physical units and the same t; inserting
scale-dependent reference metrics requires explicitly changing the bounds.

Define

    e_i[u]=t∫|∇_{Z_i}u|²dμ_i,
    s_i[u]=inf { e_0[f]: E_i f=u }.

Suppose the conditional measure of X_i under μ_i has Poincare constant
λ_i^(-1), and its score in the remaining coordinates has covariance norm
at most M_i². Set

    β_i=M_i²/λ_i,   α_0=1,   α_{i+1}=α_i/(1+β_i).

Then the following reference-form bounds hold:

    α_i e_i ≤ s_i ≤ e_i.                                (6)

Proof: the tower property gives exact associativity

    s_{i+1}[u]=inf {s_i[v]:P_i v=u}.

The lower bound follows from (3), (6) at level i, and minimization; the
upper bound uses the original lift f=u. No Markov property of s_i is used.
For a finite number of smooth compact-coordinate steps, these are closed
forms with domain H¹(Z_i), by the same coercive minimization argument.

In the coordinate Hilbert norm, the discarded restriction satisfies

    D_i ≥ d_i I,   d_i=α_i tλ_i.                         (7)

Let the i-th minimizing lift be j_i u=u−C_i u. Completing the square in
the s_i form gives

    s_i[C_i u]=s_i[u]−s_{i+1}[u]
              ≤ (α_{i+1}^(-1)−1)s_{i+1}[u].

Hence

    ||C_i u||² ≤ ε_i s_{i+1}[u],
    ε_i=(α_{i+1}^(-1)−1)/d_i.                           (8)

This bound is conservative. In particular it can retain earlier losses
even if β_i=0. No assertion of sharpness is made.

The iterated original minimizing lift is

    J_j=j_0 j_1 ... j_{j−1}.

For a final u∈H_j, put u_j=u and u_i=j_i u_{i+1}. Then
u_i−u_{i+1}∈H_i⊖H_{i+1}; these differences are mutually orthogonal in
the original L²(μ_0). Moreover `s_i[u_i]=s_j[u]`. Therefore

    ||J_j u||² = ||u||²+Σ_{i<j}||C_i u_{i+1}||²
               ≤ ||u||²+E_j s_j[u],
    E_j=Σ_{i<j}ε_i.                                    (9)

The metric corrections add; the reference-form constants α_i generally
multiply. A bound on Σβ_i would control that product, but has not been
proved for Yang--Mills.

### Identification with normalized Schur steps

The following identification is rigorous in finite dimensions. It also
holds for the closed forms above **provided** every J_i extends boundedly
on its coordinate L² space and the stated graph-form/domain conditions of
the manuscript's closed-form Schur lemma hold. Those additional analytic
conditions are not inferred from (8).

Let G_i=J_i*J_i and K_i=G_i^(-1/2)S_iG_i^(-1/2). At normalized level i,
choose the discarded subspace

    W_i=G_i^(1/2) Ran(Q_i),

and choose its orthogonal complement as the retained space. This is
constructive from the previous graph metric and the coordinate choice;
it does not use a spectral gap or a spectral cutoff. Since G_i1=1, its
discarded subspace is orthogonal to the constant vacuum.

For w=G_i^(1/2)q, q∈Ran(Q_i), the energy is s_i[q], while
`||w||²=||q||²+|| (J_i−inclusion)q ||²`. Equations (7) and (9) imply

    K_i|W_i ≥ δ_i I,
    δ_i=(d_i^(-1)+E_i)^(-1).                            (10)

Exact normalized Schur reduction with this W_i is unitarily equivalent
to K_{i+1}. To see this, apply G_i^(-1/2) to a fixed retained affine
space plus W_i. Its variations become exactly Ran(Q_i); hence its energy
minimization is the variational problem defining s_{i+1}. The resulting
graph range in the original Hilbert space is J_{i+1}H_{i+1}. Both
normalized constructions are isometric parameterizations of that same
graph range with the same energy. They therefore differ by a unitary.
The affine spaces cover all coordinate constraints: the compression of
G_i^(-1) to H_{i+1} is bounded positive and invertible.

This makes the distinction from simply reusing the coordinate conditional
projection on K_i explicit. W_i is generally a different subspace.

For depth n, this particular inverse-gap certificate is

    Σ_{i<n}δ_i^(-1)
      =Σ_{i<n}d_i^(-1)+Σ_{k<n−1}(n−1−k)ε_k.             (11)

The repeated appearance of accumulated metric distortion is a real loss
of this estimate. Equation (11) is **not** a uniform depth theorem. A
direction-sensitive metric bound, additional decay, or a different
argument would be needed to remove it. Divergence of this upper
certificate does not prove divergence of the actual inverse-gap costs.

## 3. Exact marginal compression and a triangular influence estimate

The Galerkin compression A=P H P, represented by restricting the ground
form to retained-coordinate functions, has exactly the form e_Y. Thus
**marginal/Galerkin compression closes on weighted gradient forms**.
This is a different operation from energy-minimizing Schur elimination;
Section 4 proves they cannot generally be identified.

### Actual-vacuum fixed-block bounds survive every coordinate marginal

There is an unconditional inheritance result for the already proved
Yang--Mills finite-block theorem. Let B be a fixed set of original links,
let F be any subset of the other links, and retain B together with the
remaining exterior Z. Write original configurations as (u,v,z), where v
are the integrated F coordinates. The existing theorem gives, uniformly
in v,z and u,u',

    ψ(u,v,z)/ψ(u',v,z) ≤ R_B(s),
    R_B(s)=κ_N(s)^|B| exp(4sbp_B/x²).

Squaring and integrating v against product Haar gives

    ρ_{B,Z}(u,z)/ρ_{B,Z}(u',z) ≤ R_B(s)²,
    ρ_{B,Z}(u,z)=∫ψ(u,v,z)²dv.                          (19)

The conditional normalization at fixed z cancels in the ratio. The
product Haar comparison in the original theorem therefore proves

    Var_{μ_{B|z}}(f) ≤ [R_B(s)²/C_F] ∫|∇_B f|²dμ_{B|z} (20)

for every such marginal, with the **same** constant. With the original
physical coefficient t=x/(2a), its Galerkin ground form has discarded
block bound

    d_B(s)=x C_F/(2a) κ_N(s)^(-2|B|)
                     exp(−8sbp_B/x²).                  (21)

Thus the bounded-block λ_i hypotheses in (14) can be supplied uniformly
through all coordinate marginalizations of a fixed original vacuum,
provided the block sizes and original plaquette counts p_B are uniformly
bounded. This is more than repeating the estimate for the original
measure: it is an exact stability statement for all its coordinate
marginals. It does not control M_{ki}, make these marginals Wilson
vacua at a new scale, apply to nonlinear coarse holonomies, or establish
Markov closure for S or K. The parameters x,a and original geometry in
(21) are unchanged.

For one split, assume additionally that the marginal ν has Poincare
constant μ^(-1), where μ here denotes a positive number. Put
`a=||∇_Y f||`, `b=||∇_X f||`. Total variance and the score derivative give

    Var(f) ≤ b²/λ + (a+M b/√λ)²/μ.

Consequently the full physical gap is at least `t/λ_max(T)`, where

    T = [[1/μ,              M/(μ√λ)],
         [M/(μ√λ), 1/λ+M²/(μλ)]].                      (12)

Here det T=1/(μλ), and
`λ_max(T)=(tr T+sqrt((tr T)²−4/(μλ)))/2`. This is an explicit two-scale
comparison, not an exact formula for the actual gap.

For many blocks, let μ_i be the successive marginals obtained by
integrating blocks X_0,...,X_{i−1}. Assume that block X_i conditioned on
all remaining blocks under μ_i has Poincare constant λ_i^(-1).
Include the final block, whose inequality is an unconditional marginal
inequality. For k<i, assume the centered conditional score in the X_i
directions, when integrating X_k under μ_k, satisfies

    |Cov_{μ_k(.|Z_{k+1})}(g,σ_{ki})|
       ≤ M_{ki} sqrt(Var_{μ_k(.|Z_{k+1})}(g))            (13)

uniformly in the remaining coordinates. Define

    f_i=E[f|Z_i],  f_{m+1}=E f,
    w_i=||f_i−f_{i+1}||,   a_i=||∇_{X_i}f||.

Repeated differentiation of the conditional integrals, Jensen, and
Minkowski give

    ||∇_{X_i} f_i|| ≤ a_i+Σ_{k<i}M_{ki}w_k.

Applying the conditional Poincare inequality at step i gives

    w_i ≤ λ_i^(-1/2)(a_i+Σ_{k<i}M_{ki}w_k).              (14)

Let R be the strictly lower triangular nonnegative matrix
`R_ik=M_{ki}/sqrt(λ_i)` for k<i, and let
`L=(I−R)^(-1)diag(λ_i^(-1/2))`. Since R is nilpotent, its inverse here
is the finite sum I+R+...+R^m and has nonnegative entries. Thus (14)
implies componentwise w≤La. Orthogonal martingale differences now give

    Var(f)=Σ_i w_i² ≤ ||L||² Σ_i a_i²,
    gap(H) ≥ t/||L||².                                 (15)

In particular, if `||R||_(ℓ²→ℓ²)≤r<1` and `λ_i≥λ_*`, then

    gap(H) ≥ t λ_* (1−r)².                              (16)

The proof is uniform in the number of blocks when these two assumptions
are uniform. Applied throughout to the measure conditional on the fixed
exterior of an elimination layer, (15)--(16) give a whole-layer
conditional bound. This is a genuine sufficient condition: it only asks
for bounded-block conditional inequalities and a specified influence
matrix norm. Its missing Yang--Mills input is the uniform estimate (13)
for the **actual vacuum's successive marginals**, including all exterior
conditions and weak coupling. The original fixed-block oscillation
estimate does not establish (13).

## 4. Conditional-expectation Schur reduction need not be Markov

Take four states with μ=(1/6,1/6,1/3,1/3), and the connected reversible
Markov form

    h[f]=(1/3)[(f1−f3)²+(f2−f4)²+(f1−f2)²/2].

Retain the conditional expectation on the partition
`{1,2},{3},{4}`. Write

    f=(u_A+r,u_A−r,u_B,u_C).

Then `||f||²=(1/3)(||u||²+r²)` and the form block matrices, using this
common factor, are

    A=[[2,-1,-1],[-1,1,0],[-1,0,1]],
    B=(0,-1,1),  D=4.

Thus S=A−B*B/4 already has S_BC=1/4>0. Its Markov property fails.
The vectors (1,1,1), (−2,1,1), (0,1,−1) diagonalize both S and G.
Their S eigenvalues are respectively 0,3,1/2; their G eigenvalues are
1,1,9/8. Hence the normalized Schur operator is exactly

    K=[[ 2,   -1,    -1],
       [-1, 13/18,  5/18],
       [-1,  5/18, 13/18]].                             (17)

The BC entry of exp(−sK) is `−5s/18+O(s²)`, negative for sufficiently
small s>0. Thus K is not a Markov generator in this retained-coordinate
probability representation. Its constant vacuum is nevertheless intact,
and its nonzero eigenvalues are 3 and 4/9. Equivalently the normal
contraction/absolute-value property fails on u=(0,1,−1), since
h_K[|u|]>h_K[u]. No claim is made that this finite graph is Yang--Mills.
It refutes automatic Markov closure from positivity, a constant vacuum,
reversibility, and conditional-expectation projection alone.

## 5. An energy-weighted graph bound does not remove the domain obligation

Let H_P=L²(0,1), H_Q=R, with the form domain H¹(0,1)⊕R. Put

    ℓ(u)=u(0)−∫_0^1u(x)dx,
    h[(u,q)]=∫_0^1|u'(x)|²dx+|q+ℓ(u)|².

This is a closed nonnegative form: the trace functional ℓ is bounded
on H¹, and its form norm is equivalent to the product H¹⊕R norm.
Here D=1, s[u]=∫|u'|², Cu=ℓ(u), C1=0, and

    |Cu|²=|−∫_0^1(1−x)u'(x)dx|² ≤ s[u]/3.              (18)

Nevertheless C is not closable as an L²→R operator. The triangular
boundary functions `u_n(x)=max(1−nx,0)` satisfy u_n→0 in L² but
Cu_n=1−1/(2n)→1. Thus (18), even with D>0, a closed fine form, and
a preserved constant vacuum, does not define a self-adjoint operator
`I+C*C` on the original retained L² space. Extra hypotheses are needed
for that normalization. This is an abstract form-domain obstruction;
the displayed fine form is not asserted to be a product-manifold
Yang--Mills ground-state form.

## 6. Verification and unresolved obligations

The analytic comparison proofs have been self-reviewed. The four-state
counterexample has additionally been independently reconstructed by
`/root/layer_obstructions`, recorded in `../obstructions/PROOF.md`, section 3.
That independent derivation agrees with (17), including the absolute-value
contraction witness. The exact rational check in `verify_exact.py` completed
successfully under the computation-audit runner; its provenance manifest is
`exact_run/manifest.json`, and manifest validation passed. This finite run
checks only the displayed four-state construction.
All analytic claims above are proved directly; no external theorem is
being imported to fill the Yang--Mills score or domain gap.

The strongest current route is (15) conditionally on layer exteriors,
or (6)--(10) for exact graph reductions with verified domain assumptions.
The missing inputs are:

1. a bounded influence matrix for actual-vacuum successive marginals,
   at the required coupling; (19)--(21) supply the bounded-block
   conditional inequalities, with their stated weak-coupling losses;
2. a useful bound on the full accumulated graph metric for exact Schur
   iteration, beyond the repeated-cost estimate (11);
3. bounded graph/domain conditions for the infinite-dimensional normalized
   construction, or a separately justified replacement construction.

None is supplied by the already proved fixed-finite-block oscillation
bound, by Gaussian covariance elimination, or by the arithmetic of a
postulated scale budget. The terminal physical gap and continuum limit
remain separate obligations.
