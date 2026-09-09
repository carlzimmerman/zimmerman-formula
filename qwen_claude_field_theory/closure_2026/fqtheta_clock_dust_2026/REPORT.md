# The \(F(Q)\Theta\) grand-prize door — bounded result

This lane tests the only operator identified by the latest Fable degeneracy
analysis as capable of mixing the MOND scalar with metric velocities:

\[
S=\int\sqrt{-g}\left[\frac{M^2}{2}R-\Lambda M^2-K(Q)+F(Q)\Theta
 +M^2a_0^2G(|V|/a_0)\right]+S_m[g,\psi],
\quad \Theta=\nabla_\mu n^\mu .
\]

Here \(n_\mu=-\partial_\mu T/\sqrt{-\partial T^2}\), \(Q=n^\mu\partial_\mu\varphi\),
and \(V_\mu=q_\mu{}^\nu\partial_\nu\varphi\). The exact exponential primitive
is \(G(y)=y^2+2(1+y)e^{-y}-2\), with \(G'(y)/(2y)=1-e^{-y}\). All gates
below are derived from this one action; no phenomenological source is pasted
in.

## Derived homogeneous equations

On flat FLRW in unitary clock gauge,

\[
L_h=-3M^2a\dot a^2/N-2\Lambda M^2Na^3-Na^3K(Q)
 +3a^2\dot aF(Q),\qquad Q=\dot\varphi/N.
\]

The velocity Hessian in \((\dot a,\dot\varphi)\) is computed directly:

\[
\det W=\frac{3a^4}{N^2}
\left(2M^2K_{QQ}-3F_Q^2-6M^2H F_{QQ}\right),
\qquad H=\dot a/(aN).
\]

Thus the generic mixed-degeneracy condition is
\[
K_{QQ}=\frac{3F_Q^2}{2M^2}+3H F_{QQ}.
\]
Because a fixed action cannot be degenerate only at one selected Hubble rate,
degeneracy on a family of expanding backgrounds forces \(F_{QQ}=0\): \(F\)
is affine. Taking \(F(0)=0\), the background-independent condition is
\(K_{QQ}=3F_Q^2/(2M^2)\). The mixed entry is
\(W_{a\varphi}=3a^2F_Q/N\), so this is a genuine architectural opening rather
than an asserted rank.

The lapse and scale variations give the auxiliary stress
\[
\rho=K-QK_Q+3HQF_Q,\qquad p=-K-F_Q\dot Q,
\]
and the shift-symmetric scalar charge obeys
\[
\frac{d}{dt}\left[a^3(-K_Q+3HF_Q)\right]=0.
\]

## Static branch

For a stationary foliation \(Q=0=\Theta\), choosing \(F(0)=0\) leaves the
static weak-field action unchanged. Independent variation of the two metric
potentials gives
\[
\Psi''-\Phi''=0\quad\Rightarrow\quad\Phi=\Psi
\]
under regular isolated boundary data. Variation of \(\Phi\) gives
\[
4M^2\nabla\!\cdot\!\left[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi\right]=\rho,
\]
with \(G_{\rm measured}=1/(16\pi M^2)\) in this normalization. Thus the
operator preserves the exact exponential/no-slip static gate.

## The bounded obstruction found

The explicit affine witness
\[
F(Q)=Q,\qquad K(Q)=\tfrac34Q^2-3Q+\tfrac94
\]
at \(Q_*=1,M^2=1\) satisfies the background-independent degeneracy relation,
has \(K(Q_*)=0\), \(\rho_{\rm bare}=K-Q_*K_Q=3/2>0\), and \(p_{\rm bare}=0\).
Its fixed-metric (decoupling) sound-speed square is
\[
c_{\rm bare}^2=\frac{p_Q}{\rho_Q}
=\frac{K_Q}{QK_{QQ}}=-1.
\]

This is a real warning: positive pressureless dust on the mixed-degenerate
locus drives the bare scalar kinetic/gradient ratio negative. Since
\(F(Q)\Theta\) braids metric and scalar, this is **not yet a full
inhomogeneous ghost theorem**; the complete ADM reduction could change the
physical eigenmode. The candidate is therefore **OPEN**, not certified and
not universally killed.

## Reproducibility

~~~
python3 -B qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/fqtheta_gate.py --output-dir qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/run_001
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026 -p 'test_*.py' -v
~~~

The script derives the Hessian, determinant, degeneracy relation, static
Euler–Lagrange equations, FLRW stress/charge and witness in exact SymPy
arithmetic. It does not hard-code a rank, PPN parameter or degree-of-freedom
count.

**Next unavoidable calculation:** retain lapse, shift, the khronon and the
spatial MOND gradient in the full ADM quadratic action, then run the actual
Dirac chain and principal-symbol eigenanalysis on an expanding \(H\ne0\)
branch. Only that calculation can decide whether the braiding turns this
opening into a healthy two-tensor-plus-clock theory.
