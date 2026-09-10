# Independent logarithmic no-slip reference

Base: `4fe59c19248663e7e8282dd11e9f55b9badefe17`. This directory adds a
bounded arbitrary-precision reference, not a new action or a broad search.
The action remains \(F R+3F_X^2(\nabla X)^2/(2F)+P-G\Box\phi\), with
an explicit clock, physical minimal matter, and one global constant \(a_0\).
The local clock normalization is \(q=-1\) in every control. No particles
or separate halo acceleration scales are introduced.

## Correct geometry, original general inverse

For \(r=\epsilon/\sqrt{y(1-e^{-y})}\), define \(h=ry<1/4\),
\(s=\sqrt{1-4h}\), and

\[
\sqrt B=\frac2{1+s},\quad g=yB,\quad
B'=\frac{2(\sqrt B)^3(y+r y')}{s}.
\]

This obeys \(\sqrt B=1+rg\), the exact logarithmic no-slip relation,
and \(p_r=-g^2/B\ne0\). It is not the old \(B=1+2rg\) target.
All \(\rho,p_r,p_t,p_r'\) are computed from the generic metric formulas
in the committed `kgb_pressure_freedom_2026/general_inverse/pressure_inverse.py`.
The new reference calls its **actual normalized 3 by 3 solve**, not old
zero-pressure expressions. No special-target derivatives are inherited.

An independent exact SymPy test also validates the parent's proposed fast
general-metric formulas against that matrix for arbitrary symbols
\((r,B,B',g,g')\):

\[
\begin{split}
S&=4F(\rho+p_t)/r+4w(rg-1)/(Br^2),\\
\Gamma&=prS/(2Qw),\qquad Q=2X+U,\quad p=\sqrt{BU},\\
L&=2F(\rho+p_r)+2w(g+B'/(2B))/B+3w^2/(FB),\\
W&=B(L-2Xw\Gamma/p)/2,\\
H&=[(2/r+w/F)U-(2g+w/F)X]/p,\qquad
\kappa=2P/F+H\Gamma.
\end{split}
\]

All three matrix residuals simplify to zero. Here \(p\) without a
subscript is the radial clock derivative, not geometric pressure.
The reference intentionally retains the matrix solve as an independent
comparison for the fast kernel.

## APIs and actual action derivatives

`normalized(eps,y,X,U,w,F)` returns a state. With \(f=F_X\ne0\),
\(j=F_{XX}\), its actual \(X\)-flow is

\[
\mathcal D(y,X,U,w,F,f)=
\left(\frac f{r_yw},1,-2-\frac{2fgQ}{w},\frac{fW}{w},f,j\right).
\]

For \(v=(\kappa,\Gamma)\), `first_derivatives(state,f)` computes
\(E=\mathcal Dv\) by real `mp.diff` along this flow. `jets(state,f,j)`
returns

\[
(P,P_X,G_X,P_{XX},G_{XX})=(P,f\kappa,f\Gamma,jv+fE).
\]

`next_derivatives(state,f,j)` computes \(\mathcal DE\), including
\(df/dX=j\). It is **not** itself the physical third derivative.
`third_jets(state,f,j,ell)` returns

\[
(P_{XXX},G_{XXX})=\ell v+2jE+f\mathcal DE,\qquad \ell=F_{XXX}.
\]

The test differentiates the original second jets with changing \(f\) and
\(j\) and checks this expression directly. Dropping the changing-\(f\)
term produces a nonzero discrepancy. No second jet is chosen independently
to improve health, and no point is projected back onto a matching surface.

`matching_gap(first,second,f,j)` requires common \(F,X\) and returns the
five physical action-jet differences. The same-state control is exactly
zero. Common-\(F,X,f,j\) alone does not make two distinct halos share
\(P,G\). Additive \(G\) constants are immaterial exterior boundary terms;
global action/interior boundary matching remains outside this local check.

`evaluate(state,f,j)` reconstructs the original physical inverse and its
total current, then independently maps the metric and the actual action
curvatures to EF and evaluates the original coupled KGB stress/principal.
It checks the independently transformed Einstein tensor and EF current.
Requirements include \(F,X,U,r,B>0,wf\ne0\),
\(2(F-Xf)\ne0\), and \(1+rw/(2F)>0\). The field Jacobian may have
either sign. Exterior vacuum is essential: physical minimal matter must
not be treated as EF minimal matter inside a source.

## Bounded verification

Seven tests cover exact fast-kernel identities, corrected geometry,
an **explicit generic zero-pressure control** recovering the old inverse,
physical first-jet consistency and \(dP/dX=P_X\), original EF equations
and local health, full next derivatives, and a real shared-action gap.

The runner evaluates two 65-digit controls with
\(\epsilon=10^{-6},2\,10^{-6}\), common
\(y=.1,X=.5,F=.525,f=.05,j=-3000\),
\(U=.25Xrg,w=-.075g\). They pass the local EF scalar criterion but
**do not match the five action jets**. Their nonzero gap is the useful
next construction gate, not a universal obstruction or a new failed-model
catalog. The reported physical third-jet gap uses shared \(\ell=0\);
no higher-order matched seed is claimed.

Run from repository root:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_logslip_joint_2026/reference/run_reference.py --result-file qwen_claude_field_theory/closure_2026/kgb_logslip_joint_2026/reference/results.json
```

`results.json` records tests, actual coefficients, residuals and matching
gaps. The parent aggregate pins source hashes. This is not a common-mass
action construction, radial continuation, CMB likelihood, global clock
solution, PPN assignment, complete Dirac analysis or full physical-frame
stability certificate. The initial test run failed on the intentionally
missing implementation; the completed runner executes the implemented tests.
