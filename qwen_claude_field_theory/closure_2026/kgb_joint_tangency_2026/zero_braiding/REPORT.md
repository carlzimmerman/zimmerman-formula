# Regular zero-braiding checkpoint

Base: `f109d3d8ce1cdab6b5f63bea75bca83a8d4798f9`. This is a bounded
construction/audit of a branch omitted by the earlier negative-
\(w\), nonzero-braiding search. It constructs pressure-matched positive-
\(w\) pairs, derives the actual remaining action-matching conditions, and
finds an exact **conditional local EF scalar-energy obstruction**. It does
not eliminate all clock theories, establish a CMB fit, or count full modes.

## Action, chart and source chain

The same physical action is

\[
\sqrt{-g}\left[F(X)R+\frac{3F_X^2}{2F}(\nabla X)^2
 +P(X)-G(X)\Box\phi\right]+\mathcal L_m[g],\qquad
 X=-\tfrac12(\nabla\phi)^2.
\]

The explicit clock is \(\phi=q t+\psi(r)\), locally \(q=-1\).
No dark-matter particles are added. One global constant \(a_0\) is used
as the acceleration unit; \(\epsilon_1\ne\epsilon_2\) labels different
target masses, not independently adjusted acceleration scales.

The construction uses the committed `structure/closed_inverse.py` from
`kgb_universal_clock_2026`. Derivatives below are independently obtained
by real `mp.diff` along that inverse, **not by differentiating a projection
back onto the zero-braiding surface**. EF evaluation uses the general
dictionary from `kgb_nonaffine_clock_2026/dictionary/general_ef.py`, which
loads the original coupled scalar principal/stress from
`ticking_kgb_inverse_2026/kgb_inverse.py`. No external physical theorem
or empirical claim is needed for the new algebra. The manifest pins all
three actual code inputs and the Lean environment.

Assumptions for the inverse chart: \(F,X,U,r,B>0\), \(f=F_X\ne0\),
\(w=fX'\ne0\), \(Q=2X+U>0\), \(p=\sqrt{BU}\),
\(\Delta=2(F-Xf)\ne0\), and positive areal Jacobian
\(D=1+rw/(2F)>0\). The conformal map is
\(\widetilde g=2F g\), \(\chi=X/(2F)\). Either sign of \(\Delta\)
is allowed. All numerical checks here use exterior vacuum: physical
minimally coupled matter is not silently treated as EF minimally coupled
matter. The local EF principal criterion is not a full physical-frame
Dirac/Hamiltonian or matter-coupled stability certificate.

## Lower matching and the actual returning curvature

Write \(g=A'/(2A)\), \(\kappa=P_X/f\), \(\Gamma=G_X/f\).
For the exact target \(B=1+2rg=1/(1-2ry)\), the closed inverse gives

\[
\begin{split}
S&=2F(g+2/r)\rho+\frac{4w(rg-1)}{r^2B},\qquad
\Gamma=\frac{prS}{2Qw},\\
P&=\frac{2w(g+2/r)+3w^2/(2F)}B,\\
H&=\frac{(2/r+w/F)U-(2g+w/F)X}{p},\qquad
\kappa=\frac{2P}{F}+H\Gamma.
\end{split}
\]

Thus \(\Gamma=0\) fixes

\[
w_0=\frac{F(g+2/r)\rho r^2B}{2(1-rg)}>0
\]

when \(\rho>0\), \(rg<1\). It does not fix \(U\). At common
\(F,X,f\), common \(P\) then automatically matches \(P_X\) and
\(G_X=0\); no lower-order \(H\) matching is needed.

Let \(\mathcal D\) be the **actual** inverse \(X\)-flow and
\(j=F_{XX}\). At this point, not on an assumed zero-braiding trajectory,

\[
G_{XX}=f\mathcal D\Gamma,\qquad
P_{XX}=\frac{2Pj}{F}+\frac{2Pf^2}{F^2}+H G_{XX}.
\]

Consequently, common nonzero \(G_{XX}\) makes matching \(P_{XX}\)
require \(H_1=H_2\) again. The exception \(G_{XX,1}=G_{XX,2}=0\)
is retained, not divided out.

There is also no new shared \(j\) repair at the next gate. For
\(v=(\kappa,\Gamma)\), set \(E=\mathcal Dv\). At \(\Gamma=0\),
\(E=f\mathcal B\). If \(N=(\mathcal DE)_{j=0}\), then
\(\mathcal DE=N+j\mathcal B\), and the physical third jets are

\[
(P_{XXX},G_{XXX})=F_{XXX}v+3jE+fN.
\]

Once the five lower jets match at common \(f\ne0\), both \(v\) and
\(E\) agree, so the remaining third-jet difference is \(f(N_1-N_2)\):
neither shared \(j\) nor \(F_{XXX}\) changes that difference. This is a
conditional next-gate formula; none of the distinct-mass pairs below
passes the second-jet gate, so no numerical third-jet-matched seed is claimed.

## A finite discriminator for both second jets

At \(S=0\), let \(W=dw/dr\), as returned by the actual inverse, and define

\[
\mathscr S=\frac{S_y}{r_yw}+\frac{S_wW}{w}+S_F,
\quad K_i=\frac{\sqrt{B_i}r_i\mathscr S_i}{2w_i},
\quad x_i=\frac{U_i}{2X+U_i}\in(0,1).
\]

Then \(G_{XX,i}/f^2=K_i\sqrt{x_i(1-x_i)}/\sqrt{2X}\).
With \(a_i=2/r_i+w_i/F\), \(b_i=2g_i+w_i/F\),

\[
t_i=K_i(a_i+b_i/2)/\sqrt{B_i},\quad
v_i=-K_i b_i/(2\sqrt{B_i}),\quad
H_iG_{XX,i}/f^2=t_ix_i+v_i.
\]

The second-jet matching problem reduces to a line and a quadratic.
For \(u=t_1/t_2\), \(v=(v_1-v_2)/t_2\), \(x_2=ux_1+v\), it is

\[
(-K_1^2+K_2^2u^2)x_1^2+
[K_1^2-K_2^2u(1-2v)]x_1-K_2^2v(1-v)=0.
\]

Every candidate must still satisfy \(0<x_1,x_2<1\) and the **unsquared**
signed-curvature equality. The implementation handles linear, constant,
identity-polynomial, one-zero and both-zero \(K\) sectors explicitly.
It raises for a nonregular zero \(t_2\), rather than pretending success.
An identical-state control is accepted as a continuous matching family.

At 80 digits, \(F=.525,X=.5,\epsilon_1=10^{-6},\epsilon_2=2\,10^{-6}\),
eight explicitly seeded pressure pairs give:

| \(y_1\) | \(y_2\) | Second-jet candidates |
|---|---:|---|
| .01 | .0141568426703454 | Both outside physical \(x\) interval |
| .01 | 16.1738437345259 | Outside interval; opposite curvature signs |
| .1 | .142972693552079 | Both outside interval |
| .1 | 10.5441650525587 | Outside interval; opposite curvature signs |
| 1 | 1.81965113611641 | Both outside interval |
| 1 | 3.80556093322927 | One physical squared root, rejected by sign |
| 10 | .255673565086637 | Outside interval; opposite curvature signs |
| 10 | 9.05931605995810 | Both outside interval |

The largest pressure relative residual is below \(4.3\,10^{-81}\).
For the tempting physical squared root in the sixth row,
\((x_1,x_2)\simeq(4.2404545\,10^{-6},1.0164369\,10^{-6})\), the
unsquared relative mismatch is **2**, not a common action.
These are eight roots, not an exhaustive search of all masses or \(y\).

## Exact conditional scalar-energy obstruction

Zero braiding and the matched first derivative give
\(\widetilde G_\chi=\widetilde P_\chi=0\). The mapped second jets obey
\(\widetilde P_{\chi\chi}=H\widetilde G_{\chi\chi}/(2F)\);
their \(j\) slopes vanish. This cancellation is checked symbolically.

More generally, in a static spherical EF orthonormal frame write
\(v=(v_0,v_1,0,0)\) and Hessian \(\mathsf H\). Static \(\chi\) means
\(\mathsf H_{01}=\mathsf H_{00}v_0/v_1\). If
\(v_0^2>v_1^2>0\) and the radial \(\chi\) gradient is nonzero, the
original on-shell scalar equation at
\(\widetilde G_\chi=\widetilde P_\chi=0\) gives

\[
\widetilde P_{\chi\chi}=
\widetilde G_{\chi\chi}
\left[\frac{\mathsf H_{00}(v_0^2-v_1^2)}{v_1^2}+2\mathsf H_{22}\right].
\]

Substituting this relation into the **original coupled** principal yields

\[
\mathcal M=\operatorname{diag}
\left(\frac{v_0^2-v_1^2}{v_1^2}\,T,0,T,T\right),
\qquad
T=\widetilde G_{\chi\chi}
(\mathsf H_{00}v_0^2-\mathsf H_{11}v_1^2).
\]

All 16 matrix residuals vanish exactly in SymPy. Timelikeness makes the
displayed ratio positive, so \(\mathcal M_{00}>0\) and
\(\mathcal M_{22}<0\) cannot coexist; moreover \(\mathcal M_{11}=0\).
The strict local static scalar-energy criterion therefore fails, including
the \(\widetilde G_{\chi\chi}=0\) case. A vanishing coefficient is not
used to declare a new mode, eliminate a mode, or prove strong coupling.

`ZeroBraiding.lean` formalizes only the real-algebra sign step, with the
explicit hypotheses \(v_0^2>v_1^2>0\) and the already-derived matrix
relation. Three lemmas compile; the reported axioms are
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.
The action variation and the on-shell reduction remain symbolic/numerical
dependencies, not Lean-formalized gravity.

Two actual 80-digit controls use \(\epsilon=10^{-6}\),
\(U=10^{-7},F=.525,X=.5,f=.05\), and independently \(j=0,10^{10}\):

| \(y\) | \(w\) | Time coefficient | Angular coefficient |
|---|---:|---:|---:|
| .1 | .102354054571589 | \(-1.9018083024\,10^9\) | \(-190.18083024\) |
| 10 | .009530196743129 | \(1.4984650931\,10^{13}\) | \(1.4984650931\,10^6\) |

Both are locally on shell but fail the stated energy criterion, for
different signs of the same ratio. The radial/cross coefficients are
zero analytically; numerical residues are below \(6\,10^{-70}\).
Independent EF Einstein residuals are below \(1.8\,10^{-73}\), scalar
relation residuals below \(7\,10^{-75}\), and principal-identity residuals
below \(7\,10^{-76}\), including the large-\(j\) controls. Current error
is normalized by \(\max(1,\sum|\text{terms}|)\), since division by a
nearly zero current-term norm would be meaningless on this branch.
These two controls are not advertised as one common-action two-mass seed.

## Dependence on the exact metric ansatz

The pressure-root table and finite matching coefficients depend on the
exact target \(B=1+2rg\), which sets the physical effective radial
Einstein pressure to zero. This is stronger than leading weak-field
\(\Phi=\Psi\). Those numerical exclusions are **not** necessary
observational exclusions for every metric with the same leading potentials.

In contrast, the conditional principal reduction contains no \(B=1+2rg\)
assumption and no MOND interpolation function. An \(O(\epsilon^2)\)
change in \(B\) cannot repair a state retaining its explicit hypotheses.
For a general metric, zero mapped EF radial current with
\(\widetilde G_\chi=0\) and nonzero radial clock implies
\(\widetilde P_\chi=0\). Applying this statement to physical variables
requires the regular on-shell current map; it must not be replaced by the
unextended physical KGB current. Nonzero current, nonzero braiding,
vanishing radial invariant gradient, a null/spacelike clock, a singular
map, matter inside the region, or a changed action falls outside the
conditional obstruction. No new general-metric route was built here.

## Execution and limitations

The first TDD run failed because `zero_gamma.py` did not yet exist; after
implementation all **8 tests pass**. Commands executed from repository root:

```text
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/kgb_joint_tangency_2026/zero_braiding -p 'test_zero_gamma.py'
python3 -B qwen_claude_field_theory/closure_2026/kgb_joint_tangency_2026/zero_braiding/zero_gamma.py
```

The Lean command is `lake env lean <absolute path>/ZeroBraiding.lean`,
run from `clock_constitutive_construction_2026/lean_formalization_2026`.
An initial attempt from the unrelated Fable Lean project failed before
compilation because its dependencies were unavailable offline; the
existing prepared toolchain above compiles the proof successfully. No
old source file, index, or HEAD was edited by this subtask.

`run_zero_gamma.py` reruns the eight tests, all three Lean declarations
and the complete 80-digit computation, recording outputs/statuses.
`audit_contract.json` and `run_001/manifest.json` pin the bounded claim,
input hashes, software and command; `run_001/results.json` holds the
full computed values. There is no global action continuation, interior
source matching, FLRW solution, CMB likelihood, assigned PPN parameter,
complete Hamiltonian constraint analysis, or empirical novelty claim.
