# Actual-vacuum layer bounds: a criterion and two obstructions

Owner: `/root/layer_tensorization`. Base checkpoint: `YM-LAYER-2026-10-28-C0`.
Assigned base Git revision: `5bb77f83c618cab437a705c7aa19d7fe0b7aead7`.
Observed checkout HEAD while reading: `9c9d980ba0a972f1661de3b64d8296ea7edd5af6`.
Date: 2026-10-28. No paper edits; no novelty claim.

**The requested weak-coupling, volume-uniform actual Yang–Mills layer bound,
including stability under exact quantum coarse graining, remains open.**
The results below prove a compact-group layer criterion, refute a proposed
conditional-independence shortcut in an actual SU(2) Wilson Hamiltonian, and
show that the existing local estimates alone cannot imply the target.

## 1. Contract and fixed input

Use the normalization of `papers/yang_mills_bounds_2026/sections/vacuum.tex`:

\[
 H=\frac{x}{2}\sum_{\ell} C_\ell+
 \frac b x\sum_p(1-\operatorname{ReTr}U_p/N),\quad
 d\mu=\psi^2dU,\quad
 k[f]=\frac{x}{2a}\int |\nabla f|^2d\mu .
\]

Here the Casimir metric has fundamental Casimir
\(C_F=(N^2-1)/(2N)\), and \(\psi\) is the actual positive ground function.
Let the extensive fast layer be the disjoint union
\(F=B_1\sqcup\cdots\sqcup B_M\), each block having the same fixed number
\(m\) of links. Let \(y\) denote all links outside this layer, and put
\(P_F=E_\mu[\cdot\mid y]\), \(Q_F=I-P_F\). The goal is a bound on the form
compression to \(\operatorname{Ran}Q_F\) independent of \(M\), exterior
volume, and subsequent exact elimination depth. Equal block sizes are only
used to apply the precise common-spin-space formulation in source [W].

The proved fixed-block theorem gives, uniformly in all remaining coordinates,

\[
 \operatorname{Var}_{\mu(du_i\mid u_{-i},y)}g
 \leq \lambda_0^{-1}\int |\nabla_i g|^2d\mu(du_i\mid u_{-i},y),\qquad
 \lambda_0=C_F\kappa_N(s)^{-2m}
       \exp[-8sbp_*/x^2],                                      \tag{1}
\]

provided every block meets at most \(p_*\) plaquettes. This holds for every
\(s>0\). It is a one-block statement conditioned on *every* other block.
It is not the desired collective inequality.

## 2. A precise Dobrushin-to-layer theorem

For each fixed exterior \(y\), define the actual-vacuum interdependence
matrix by \(c_{ii}(y)=0\) and

\[
 c_{ij}(y)=\sup_{z=z'\ {\rm off}\ j}
 \sup_A\left|
 \mu(u_i\in A\mid z,y)-\mu(u_i\in A\mid z',y)
 \right|,\qquad i\ne j.                                     \tag{2}
\]

The supremum is over all fast boundary configurations for block \(i\).
There is no Markov or finite-range assumption on these conditional laws.
Assume the additional, presently unproved Yang–Mills hypothesis

\[
 \sup_y r_{\rm sp}(C(y))\leq q<1,                            \tag{3}
\]

with the same \(q\) for every volume under consideration.

**Theorem 1 (conditional layer upgrade).** Under (1) and (3),

\[
 \|Q_F f\|^2_{L^2(\mu)}
 \leq\frac1{(1-q)\lambda_0}
       \int\sum_{i=1}^M|\nabla_i f|^2d\mu,
 \qquad
 D_F\geq \frac{x}{2a}(1-q)\lambda_0 I.                       \tag{4}
\]

Proof. At fixed \(y\), apply Wu's Theorem 2.1 [W] with spin space
\(SU(N)^m\), discrete metric \(d(u,v)=1_{u\ne v}\), and actual conditional
measure \(\mu_y\). This is a measurable-space case expressly covered by
that theorem; the metric's second-moment assumption is automatic. Its
Wasserstein distance is exactly the total variation convention in (2).
The result is

\[
 (1-r_{\rm sp}(C(y)))\operatorname{Var}_{\mu_y}f
 \leq\sum_i E_{\mu_y}\operatorname{Var}_{\mu_i(\cdot\mid u_{-i},y)}f.
\]

Apply (1) to each summand and integrate in \(y\). The exact ground-state
form dominates the fast gradient energy. Smooth density and closed-form
restriction are justified as in the input finite-block theorem: smooth
positive density on each fixed compact graph makes conditional projection
bounded on its Sobolev form domain. No volume-uniform Sobolev norm comparison
is required. This proves (4).

The vertex gauge action transforms each selected block and the exterior
separately, preserving Haar measure and \(\psi\). Thus \(P_F\) commutes with
the action and (4) restricts to physical functions. No quotient manifold or
gauge fixing is required. For complex functions, apply the real inequality
to real and imaginary parts.

This theorem is an exact sufficient condition, not a proof of (3). In
particular it does not insert the target global quantum gap as an assumption.

### A quantitative influence certificate

Set \(W=-2\log\psi\). For fixed \(i\ne j\), let \(\Delta_{ij}\) be the
supremum, also over the exterior, of

\[
 |W(u_i,z)-W(u'_i,z)-W(u_i,z')+W(u'_i,z')|,
 \quad z=z'\text{ off }j .                                 \tag{5}
\]

Then

\[
 c_{ij}(y)\leq\tanh(\Delta_{ij}/4).                         \tag{6}
\]

Indeed, if two probabilities have likelihood ratio \(r\) with
\(a\leq r\leq b\), \(Er=1\), and \(b/a\leq e^\Delta\), convexity of
\(|r-1|\) bounds their total variation by
\((b-1)(1-a)/(b-a)\). Maximizing over \(a\leq1\leq b\) at fixed ratio gives
\((\sqrt{b/a}-1)/(\sqrt{b/a}+1)\leq\tanh(\Delta/4)\).
For conditional Gibbs densities, the oscillation of \(\log r\) is bounded
by (5), since the normalizing constants cancel in the oscillation.

If
\(h_{ij}=\sup\|\nabla_i\nabla_j W\|_{\mathrm{op}}\), integration along two
minimizing geodesics gives
\(\Delta_{ij}\leq D_iD_jh_{ij}\), where \(D_i=\sqrt m D_N\) is the block
diameter. Thus a directly checkable sufficient input is

\[
 \sup_i\sum_{j\ne i}\tanh(mD_N^2h_{ij}/4)<1.                \tag{7}
\]

Neither \(h_{ij}\) nor \(c_{ij}\) concerns the bare magnetic potential.
They concern the logarithm of the actual vacuum density.

The existing one-block ratio is
\(R=\kappa_N(s)^m\exp(4sbp_*/x^2)\). It only gives
\(\operatorname{osc}_{u_i}W\leq2\log R\), hence
\(\Delta_{ij}\leq4\log R\) for every \(j\). The resulting row-sum
certificate is \((M-1)\tanh(\log R)\), which is not uniform as
\(M\to\infty\) for fixed nonzero \(\log R\). This failure of an upper
certificate does not prove that the actual row sums diverge.

## 3. A compact-manifold Hessian criterion, with proof

The following alternative avoids any need to invoke a Euclidean
logarithmic-Sobolev theorem on a gauge quotient.

Let \(\nu=e^{-W}d\mathrm{vol}/Z\) on a finite product of compact, connected,
boundaryless Riemannian manifolds \(M_i\), with \(W\) smooth. Suppose every
one-factor conditional gradient Poincaré gap is at least \(\lambda_i>0\),
uniformly in the other factors. Choose symmetric bounds
\(h_{ij}\geq\sup\|\nabla_i\nabla_jW\|_{\mathrm{op}}\), and define

\[
 A_{ii}=\lambda_i,\qquad A_{ij}=-h_{ij}\quad(i\ne j).
\]

**Theorem 2.** If \(A\geq\rho I\) for \(\rho>0\), then

\[
 \rho\operatorname{Var}_\nu f\leq\int\sum_i|\nabla_i f|^2d\nu. \tag{8}
\]

Proof. Write \(L_i=-\Delta_i+\nabla_iW\cdot\nabla_i\) and \(L=\sum_iL_i\).
The conditional spectral theorem gives
\(\int(L_i f)^2d\nu\geq\lambda_i\int|\nabla_i f|^2d\nu\).
For \(i\ne j\), integration by parts and the product connection give

\[
 \int (L_i f)(L_j f)d\nu
 =\int\|\nabla_i\nabla_jf\|_{\rm HS}^2d\nu
  +\int\nabla_i\nabla_jW(\nabla_i f,\nabla_j f)d\nu.         \tag{9}
\]

To check the sign, differentiate \(L_i f\) in the \(j\) direction:
\(\nabla_jL_i f=L_i\nabla_jf+(\nabla_j\nabla_iW)\nabla_i f\).
No cross-factor curvature term appears. Put
\(v_i=(\int|\nabla_i f|^2d\nu)^{1/2}\). Dropping the nonnegative mixed
Hessian norms and applying Cauchy–Schwarz yields

\[
 \int(Lf)^2d\nu\geq v^TAv\geq\rho\int|\nabla f|^2d\nu.
\]

The smooth weighted elliptic operator \(L\) has compact resolvent and
constant kernel. For an eigenfunction with positive eigenvalue \(\eta\),
the preceding inequality gives \(\eta^2\geq\rho\eta\), so
\(\eta\geq\rho\). Expansion in its eigenfunctions proves (8), extended to
\(H^1\) by closure. This proof works on the unreduced compact group product.

Applied conditionally to \(\mu_y\), this gives
\(D_F\geq x\rho/(2a)\) if the same matrix lower bound holds uniformly in
\(y\) and volume. For example, \(\lambda_i\geq\lambda_0\) and
\(\sup_i\sum_{j\ne i}h_{ij}\leq(1-\delta)\lambda_0\) imply
\(\rho\geq\delta\lambda_0\). With the presently proved exponentially small
\(\lambda_0\), this is a stringent unproved input at weak coupling.

Ordinary coordinate marginalization preserves (8): apply it to a function
of the retained coordinates alone. This observation does **not** identify
marginalization with metric-normalized quantum Schur elimination. The
existing two-oscillator counterexample in the input layer record blocks
that identification; no exact-coarse stability follows here.

## 4. Local bounds alone cannot imply a whole-layer bound

This is a counterexample to an inference about measures, not a counterexample
to Yang–Mills. It also remains a counterexample after imposing gauge invariance.

Take \(M\) disjoint square loops, with four SU(2) link variables per loop.
One may connect the loops by tree edges carrying independent Haar variables.
Put \(h_i=\operatorname{Tr}U_{p_i}/2\) and fix \(0<\epsilon<1\). Relative
to product Haar define the smooth positive probability density

\[
 w_M=\tfrac12\prod_{i=1}^M(1+\epsilon h_i)
          +\tfrac12\prod_{i=1}^M(1-\epsilon h_i).            \tag{10}
\]

It is gauge invariant. Haar orthogonality of the fundamental SU(2)
character gives \(\int h_i=0\), \(\int h_i^2=1/4\); also
\(\sum_{\ell\in p_i}C_\ell h_i=3h_i\).

Condition on every link outside any set of \(r\) complete loops. The
conditional density is a convex mixture of the two corresponding product
densities. It lies between \((1-\epsilon)^r\) and
\((1+\epsilon)^r\), so its maximum/minimum ratio is at most
\(((1+\epsilon)/(1-\epsilon))^r\), independently of \(M\) and the
conditioning configuration. Haar comparison therefore gives a conditional
gradient Poincaré gap at least

\[
 C_F\left(\frac{1-\epsilon}{1+\epsilon}\right)^r.           \tag{11}
\]

The same fixed-size conclusion holds for arbitrary selected raw-link sets:
only the loops they meet contribute nonconstant factors, at most their link
count. The positive mixture coefficients may depend on the fixed exterior,
but the same ratio bound with that loop count holds before normalization.

Nevertheless, let the physical test function be
\(f_M=M^{-1}\sum_i h_i\). In the plus/minus product component its conditional
mean is respectively \(\pm\epsilon/4\). The total-variance identity gives
\(\operatorname{Var}_{w_M}f_M\geq\epsilon^2/16\). Each one-loop marginal
of (10) is exactly Haar, so

\[
 \int|\nabla f_M|^2w_MdU
 =\frac1{M^2}\sum_i\int|\nabla h_i|^2dU
 =\frac{3}{4M}.
\]

Consequently its physical-sector gradient gap is at most

\[
 \operatorname{gap}(w_M)\leq\frac{12}{\epsilon^2M}\to0.     \tag{12}
\]

Thus even gauge-invariant smooth measures with every bounded-block
conditional ratio and Poincaré estimate uniformly controlled can have no
volume-uniform collective gap. Additional influence/mixing information is
logically necessary for this route. Formula (10) is not asserted to be the
vacuum of a local Wilson Hamiltonian.

## 5. Plaquette-separated selected links are not conditionally independent

This obstruction *does* use the actual vacuum of a finite SU(2) Wilson
Hamiltonian on two adjacent squares. Let their plaquettes \(p,q\) share one
link \(e\); let \(u\) be a link belonging only to \(p\), and \(v\) a link
belonging only to \(q\). No plaquette contains both selected links.
Put \(F_p=\operatorname{Tr}U_p/2\), \(F_q=\operatorname{Tr}U_q/2\),
\(S=F_p+F_q\), \(T=\sum_\ell C_\ell\), and \(g=2b/x^2\).
After division by \(x/2\) and removal of a constant the actual operator is

\[
 T-gS.                                                     \tag{13}
\]

At \(g=0\), the ground function is constant and the next eigenvalue of
\(T\) is at least \(C_F=3/4\). Since \(S\) is a bounded multiplier,
a resolvent Neumann series on a circle of radius \(3/8\) constructs an
analytic rank-one ground spectral projection whenever \(2|g|<3/8\).
The positive normalized eigenfunction and its logarithm are analytic near
zero (elliptic regularity upgrades the expansion to any fixed smooth norm).
Fix the harmless scalar normalization by \(\int\log\psi_g\,dU=0\), and write

\[
 \ell_g=\log\psi_g=g\ell_1+g^2\ell_2+O(g^3),\qquad
 \Gamma(f,h)=\sum_\ell\langle\nabla_\ell f,\nabla_\ell h\rangle.
\]

The eigenfunction equation is

\[
 T\ell_g-\Gamma(\ell_g,\ell_g)-gS=e(g).
\]

Since \(TF_p=TF_q=3F_{p,q}\), its first two orders give

\[
 \ell_1=S/3,\qquad
 T\ell_2=\tfrac19\{\Gamma(F_p,F_p)+\Gamma(F_q,F_q)
                       +2\Gamma(F_p,F_q)\}+e_2.           \tag{14}
\]

Let \(J=(I-E_u^{\rm Haar})(I-E_v^{\rm Haar})\). It commutes with \(T\)
and kills functions lacking either selected variable. Thus

\[
 T J\ell_2=\tfrac29J\Gamma(F_p,F_q).                       \tag{15}
\]

Only the shared edge contributes to \(\Gamma(F_p,F_q)\). To see the right
side is nonzero, set the remaining links to the identity, orient the loops
so the shared edge appears oppositely, and write
\(u=\exp(it\sigma_3/2)\), \(v=\exp(is\sigma_3/2)\), \(e=I\).
The local traces then have the form \(F_p=\operatorname{Tr}(ue)/2\),
\(F_q=\operatorname{Tr}(ve^{-1})/2\). In the common-edge Lie algebra
frame, their only nonzero derivatives are

\[
 X_{e,3}F_p=-\tfrac12\sin(t/2),\qquad
 X_{e,3}F_q=\tfrac12\sin(s/2).
\]

Hence \(\Gamma(F_p,F_q)=-\tfrac14\sin(t/2)\sin(s/2)\) on this slice.
Its mixed rectangle difference between \((t,s),(t,0),(0,s),(0,0)\) is
nonzero. Therefore it cannot be a sum of a function lacking \(u\) and a
function lacking \(v\), equivalently \(J\Gamma(F_p,F_q)\ne0\). Equation
(15) implies \(J\ell_2\ne0\), and analyticity yields

\[
 J\log\psi_g=g^2J\ell_2+O(g^3)\ne0
\]

for all sufficiently small nonzero real \(g\).

For a strictly positive smooth density, conditional independence of \(u,v\)
given all exterior links would require its logarithm to be additive in
\(u,v\) at every exterior configuration (or almost every configuration,
which smoothness upgrades). That would force \(J\log\psi_g=0\).
Thus the actual Wilson vacuum violates this independence claim already
arbitrarily near \(g=0\). Gauge invariance is preserved throughout; the
identity-link slice is only an evaluation of smooth invariant functions,
not a gauge-fixing argument.

This proves neither large influence nor failure of (3). It proves that
bare plaquette separation does not set the vacuum influence to zero.

## 6. What locality survives: an exact perturbative support statement

On any fixed finite lattice, use (13) with \(S=\sum_pF_p\), all square
plaquettes, and the same logarithmic normalization. The formal coefficients
obey

\[
 T\ell_1=S,\qquad
 T\ell_n=\sum_{r=1}^{n-1}\Gamma(\ell_r,\ell_{n-r})+e_n,
 \quad n\geq2,                                             \tag{16}
\]

where \(e_n\) removes the Haar mean. Each \(\ell_n\) can be written as a
sum of functions supported on connected clusters of at most \(n\)
plaquettes, where adjacency means sharing a link and repeated plaquettes
are allowed in the coefficient construction.

Proof by induction. A single plaquette term is an eigenfunction of \(T\),
so the assertion holds for \(n=1\). A carré-du-champ term between functions
on disjoint link supports vanishes. If it is nonzero, the two connected
supports share a link and their union is connected, with size at most
\(r+(n-r)=n\). The mean-zero inverse of \(T\) preserves support: its heat
semigroup integral acts only on variables on which its argument depends.
Subtracting the Haar mean also preserves support. This proves the induction.

Consequently mixed dependence between links first appears no earlier than
the size of a smallest connected plaquette cluster containing both. Section
5 shows the lower order can be attained at size two. This is a genuine
finite-volume statement about the actual-vacuum perturbation series. It is
not a volume-uniform convergence bound, an estimate at \(g\to\infty\)
(the weak-coupling regime \(x\to0\)), or a bound after exact Schur elimination.

## 7. Remaining obligations and continuation

1. Prove a summable, volume-uniform bound on actual-vacuum influences (2),
   or on mixed log-vacuum Hessians sufficient for Theorem 2, in a regime
   extending beyond the already known strong-coupling result. The formal
   connected-cluster support statement does not control coefficient size.
2. For exact coarse operators, prove a representation/comparison of their
   true forms with a measure and gradient form to which a layer criterion
   applies, preserving the induced quantum Schur metric. Ordinary marginal
   Poincaré stability does not supply this bridge.
3. Establish the inverse-gap scale budget on the resulting actual sequence.
   No such sequence or budget is established by this route.

Executable continuation: derive an explicit connected-cluster norm bound
from (16), rather than reusing bare plaquette sparsity as if it held for
\(\log\psi\). Its likely directly accessible domain is small \(g\), which
must be compared with existing strong-coupling constants before claiming a
new regime. Weak coupling and exact coarse stability require further inputs.

Review status: analytic derivations and separate self-audit; an independent
review is requested from the coordinator. The exact source implication in
Theorem 1 is checked in `SOURCES.md`. No computation is load-bearing.
