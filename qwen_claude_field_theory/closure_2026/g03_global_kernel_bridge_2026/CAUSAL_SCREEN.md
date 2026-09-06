# Causal-screen gate: three distinct costs, no completed theory

Decision: the minimal repairs tested here do not supply the requested full
theory. This is **not** a universal no-go, a new empirical law, or a novelty
claim. It prevents three specific shortcuts from being counted as closure.
The live HEAD remained `90dab18b8`; unrelated dirty files were preserved.

## 1. Retarded substitution is not ordinary action variation

For an ordinary single-copy quadratic action with commuting fields,

\[
 S[u]=\tfrac12u^TRu\quad\Longrightarrow\quad
 {\delta S\over\delta u}=\tfrac12(R+R^T)u.
\]

A nonsymmetric retarded kernel cannot simply be substituted into this action
and then treated as the variational field equation. The code differentiates
a three-time-step example, including its actual Hessian. This issue is known:
[Galley, arXiv:1210.2745v2, equations (1)--(4)](https://arxiv.org/pdf/1210.2745v2)
derives the retarded/advanced symmetrization; his doubled-history formalism
provides a different variational prescription, not a proof of a closed MOND
model. The source does not rule out causal local actions or in-in effective
equations.

Source record: Chad R. Galley, *The classical mechanics of non-conservative
systems*, v2, 12 June 2013; checked 5 September 2026, pp. 1--2. Existing local
extraction `real_research/reviews/nonlocal_MI/GALLEY.txt` has SHA-256
`9e957b10c901bdabeb07146e2b290078805a854e31a9b692152058d1a353ce35` and matches
the checked equations and version marker. Notation: his q,Q map to u,r here.
Overlap: known after notation translation. Search scope: this exact primary
source, its local extraction, and the repository's existing `build1_galley_memory_kernel.py`
and `routeE_galley_field_theory.py`; no broad novelty search. Those repository
files were inspected, not accepted as validated theories or rerun.

## 2. A minimal dynamical localization retains its mode

At each spatial momentum, test the explicit quadratic action

\[
 L_\sigma={\dot u^2-\omega_u^2u^2\over2}
 +{\sigma\over2}(\dot r^2-\Omega^2r^2)+gur,\qquad \sigma=\pm1.
\]

This is a necessary response-sector test, **not** the proposed full
relativistic MOND action. Variation and elimination, with z=omega^2, give

\[
 M(z)=\begin{pmatrix}z-\omega_u^2&g\\g&\sigma(z-\Omega^2)\end{pmatrix},
 \qquad M_{u,\mathrm{eff}}=z-\omega_u^2+
 {g^2\over\sigma(\Omega^2-z)}.
\]

The Legendre map is invertible for sigma!=0: p_u=udot, p_r=sigma rdot;
there are no primary or secondary constraints in this two-oscillator model.
Both kinetic ranks and propagator poles are computed. With omega_u^2=4,
Omega^2=9, g=1, the healthy case has two positive-frequency poles and no
negative kinetic eigenvalues; it is a positive control, not automatically
rejected as unstable. The ghost case also has real positive frequencies,
but has one negative kinetic eigenvalue. Real frequencies alone are not
health.

Without a contact counterterm, the negative response correction needed for
this stiffening ansatz requires sigma=-1. The healthy sign gives positive
static response correction (softening of stiffness). Setting the homogeneous
solution of r to zero selects initial data; it is not a Dirac constraint
removing the extra mode. Genuine added matter modes could be admitted only
with explicit counting and health tests; none is silently classified as an
auxiliary constraint here.

The relevant generalization is exact. For unconstrained physical variables
x and healthy auxiliaries r with positive static block H,

\[
 U=\tfrac12x^TVx-x^TCr+\tfrac12r^THr
 =\tfrac12x^T(V-CH^{-1}C^T)x+
 \tfrac12(r-H^{-1}C^Tx)^TH(r-H^{-1}C^Tx).
\]

Therefore Veff<=V as quadratic forms. A pre-existing negative direction
cannot be repaired by these couplings while V is unchanged. A fresh source
build supplies the last turn's gravity witness; its tested direction changes
from -133334/1875 to -10666729/150000, remaining negative. The generic
completed-square identity is verified symbolically, not inferred from this
one witness. The argument applies to any finite number of these auxiliaries.

Scope: positive full velocity-decoupled kinetic energy, real couplings,
positive auxiliary static block, and no new constraints. Contact terms
changing V, constraints excluding the negative direction, derivative or
gyroscopic couplings, and alternative background branches require fresh
analysis. No general ban on causal nonlocal gravity follows.

## 3. An elliptic auxiliary can remove the mode, but not its spatial tail

Importantly, a wrong-sign **nondynamical** auxiliary is not automatically a
ghost. The code explicitly tests the alternative real scalar field action

\[
 L_k=\tfrac12\dot u^2-\tfrac12(k^2+m_0^2)u^2
       +\tfrac12(k^2+m^2)r^2+gur,
 \qquad m,m_0>0,\quad g\ne0.
\]

In position space the r terms are positive spatial-gradient and mass terms,
with no r time derivative. Its primary p_r=0 and secondary
C=(k^2+m^2)r+gu have bracket matrix

\[
 \begin{pmatrix}0&-(k^2+m^2)\\k^2+m^2&0\end{pmatrix}.
\]

Preservation fixes the r multiplier to -g p_u/(k^2+m^2), and closes.
The computed rank is two: one physical mode remains. Eliminating r gives

\[
 \ddot u+\left[-\Delta+m_0^2+{g^2\over m^2-\Delta}\right]u=0,
 \quad \omega^2=k^2+m_0^2+{g^2\over k^2+m^2}>0.
\]

The reduced kinetic and potential energies are positive. Nevertheless, if
u is a physical observable, it has no finite domain of propagation. For
u(0,x)=delta^3(x), udot=0, at radius R>0,

\[
 \boxed{\ddot u(0,R)=-{g^2e^{-mR}\over4\pi R}\ne0.}
\]

The script verifies the Yukawa Green equation away from zero and its unit
delta normalization by flux. Smooth nonnegative compact initial data give
the same nonzero exterior convolution. Equivalently, a local impulsive
source produces u(0)=0, udot(0)=delta^3(x): the displayed expression is then
the third time derivative, yielding an exterior response at order t^3.
This is a physical-channel example, not an inference from an instantaneous
gauge potential such as a GR lapse. Gauge/metric cancellations in a different
theory are not excluded by this test.

k=0 is well defined here because m>0: the same elliptic constraint pair
survives. This toy homogeneous limit is not FLRW or the gravitational
homogeneous constraint count. The source-gravity witness remains k!=0.

## Research consequence and next unavoidable calculation

The requested simultaneous properties do not follow by labeling a response
retarded, integrating away a dynamical mode, or using a healthy reduced
elliptic energy. The next useful construction must specify its **constraint
structure and physical causal observables together**, before fitting a MOND
kernel. For the matched screen, this requires new constraints or a changed
original quadratic block, not merely another auxiliary propagator. These
results do not identify a successful alternative.

Exact mu, lensing, full PPN, Ward identities, tensor speed, FLRW, nonlinear
Dirac closure, and empirical novelty are not certified by these response
models. No results from different actions have been combined into a PASS.
All displayed calculations are dimensionless and independent of a0, so both
repository acceleration-scale footings have the same verdict.

## Files, execution, and verification

Created in this directory: `causal_screen.py`, `test_causal_screen.py`,
`causal_screen_results.json`, `causal_screen_manifest.json`, and this report.
No existing theory file was changed; no commit/push.

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_causal_screen.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/causal_screen.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/causal_screen_results.json
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/causal_screen.py --require-causal-hidden-free
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
git diff --check
```

Test-first failures were observed for the absent implementation and absent
elliptic branch. A later real test failure exposed a symbolic-normalization
bug: a zero constraint residual was compared structurally after substitution
without rational cancellation. The residual was independently reduced to
zero; the check was fixed, not bypassed. Final results are in the manifest.
The strict gate intentionally exits 2 if none of these minimal cases meets
the combined requirement; that is not a theorem about every possible action.

Mathbox computation audit determined the separate mathematical and finite
contracts and source provenance. Final mathematical proofreading covers only
this report; no mathematical-token corrections were needed. The general
completed-square and retarded-Hessian arguments received an independent
algebra review; executable checks remain the evidence.
