# Independent high-precision shared-action seed and third-mass check

2026-09-10. Requested task base:
`de6b2c1a948c043a3a3c7130f88051db66c6bc46`.
The live repository moved to `ce9b690dfa213dae2ac002910399afe3d0828a40` during
this work; this task made no commits. The actual run revision and exact input
hashes are recorded in the manifest. Only new files under `precision/` were
authored for this task.

The selected two-mass jet is independently reproduced at 60 digits and checked
against 80 digits. Both scalar principal matrices have positive time kinetic
coefficient, negative radial and angular coefficients, and a strict physical
light-cone margin. The chosen third-mass root has the same local health and
action jet, but fails preservation at the next derivative. Neither result is
a global solution or a no-go for the action class.

## Inputs and independent derivative construction

Use the same explicit ticking clock action
\(\sqrt{-g}[mR/2+P(X)-G(X)\Box\phi]+S_m[g]\), with
\(\phi=qt+\psi(r)\), \(X=-\tfrac12(\nabla\phi)^2>0\), \(J^r=0\).
No dark matter particles are introduced. Set \(m=a_0=c=|q|=1\).
The target and generic inverse chart are

\[
 r=\frac{\epsilon}{\sqrt{y(1-e^{-y})}},\quad
 g=\frac{y}{1-2ry},\quad T=1+2rg,\quad B=\frac{T}{1+r^2P},
 \quad U=\frac{q^2}{A}-2X>0,\quad Z=\frac UX-rg,
\]
\[
 E_0=\frac{1-1/B}{r^2}+\frac{(B_r)|_P}{B^2r}+P,
 \quad W=\frac{ZE_0}{r(1+Z/T)},\quad
 H=\frac{\sqrt{BU}\,r}{2XZ}=\frac{G_X}{P_X}.
\]

The symbol \(H\) here is an inverse-action ratio, not the cosmological Hubble
rate. The computation requires \(P_X,Z,W\ne0\), regular positive metric,
and nonzero constraint denominator. It does not investigate singular charts.

Input decimals are converted directly to arbitrary-precision numbers:
\(\epsilon_1=10^{-6}\), \(\epsilon_2=2\times10^{-6}\),
\(X=1/2\), \(P=0\), \(y_1=0.1\), \(y_2=0.3\), and
\(U_1=0.25Xr_1g_1\). The positive \(\sqrt{U_2}\) is selected from the
unsquared signed \(H_2=H_1\) equation. Here both \(H_i\) are negative.

The implementation does not reuse `joint_static.py`'s coefficient formulas
or complex-step derivative. It differentiates \(r(y)\), \(g(y)\), and
\(B(y)|_P\) directly with mpmath. In the independent coordinates
\((X,y,U,P)\), partial differentiation of \(H\) gives

\[
 D_0=H_{,X}-2H_{,U},\qquad
 D_1=\frac{H_{,y}}{r_yW}
      -\frac{2g(2X+U)H_{,U}}W+H_{,P}.
\]

Along each inverse trajectory,
\(dH/dX=D_0+P_XD_1\). Preserving \(H_1-H_2=0\) fixes

\[
 P_X=-\frac{D_{01}-D_{02}}{D_{11}-D_{12}}.
\]

This is then differentiated as a function of all six coordinates
\((X,y_1,U_1,y_2,U_2,P)\) along

\[
 \frac{dy_i}{dX}=\frac{P_X}{r_{y_i}W_i},\qquad
 \frac{dU_i}{dX}=-2-\frac{2g_i(2X+U_i)P_X}{W_i},\qquad
 \frac{dP}{dX}=P_X.
\]

The derivative is mpmath's real arbitrary-precision step derivative. There is
no tunable \(P_{XX}\) and no complex-step evaluation in this construction.
Finally \(G_X=P_XH\) and
\(G_{XX}=P_{XX}H+P_X(dH/dX)\) are inserted into the original SymPy coupled
principal and stress expressions from `kgb_inverse.py`. The action variation
itself is reused, not independently redone by this task.

## Two-mass result

\[
 P_X=10454.55170814545345175645,\qquad
 P_{XX}=43547587356.37278706905049,
\]
\[
 G_X=-49.89793855362644972522,\qquad
 G_{XX}=2357114.79859006007899.
\]

The independent preservation denominator is approximately \(-3.40505676878\).
The common \(H=-0.00477284344146\) and \(dH/dX=20106.3553342\).

| Quantity | \(\epsilon_1=10^{-6}\) | \(\epsilon_2=2\times10^{-6}\) |
| --- | ---: | ---: |
| \(U\) | \(1.28137956865206\times10^{-7}\) | \(5.29245945667915\times10^{-7}\) |
| \(\rho\) | 19018.5600372 | 77235.4767115 |
| \(C_{00}\) | \(4.31430715167935\times10^{10}\) | \(4.03931129308210\times10^{10}\) |
| \(C_{01}\) | \(1.57652288367485\times10^7\) | \(3.20398229567741\times10^7\) |
| \(C_{11}\) | -10535.9726082 | -6145.23621363 |
| \(C_{22}=C_{33}\) | -22967.9363969 | -134580.293747 |
| \(C_{01}^2-C_{00}C_{11}\) | \(7.03096660011344\times10^{14}\) | \(1.27477547546517\times10^{15}\) |
| Minimum light-cone margin | \(4.31115305231474\times10^{10}\) | \(4.03290271396712\times10^{10}\) |

The cone margin is the minimum over \(0\le t\le1\) of

\[
 C_{00}+C_{22}-2|C_{01}|t+(C_{11}-C_{22})t^2.
\]

The code checks the endpoints and any interior minimum; both minima occur at
\(t=1\). It separately checks \(C_{00}>|C_{01}|\). Together with negative
spatial coefficients this yields bounded quadratic energy relative to the
static time and strict scalar characteristic-cone containment. This does not
certify the full nonlinear Hamiltonian or every sector of the theory.

At 60 digits, relative stress errors are below \(2.42\times10^{-56}\);
the current residual rounds to zero at that precision. Relative mismatches in
\(G_X\) and \(G_{XX}\) are below \(4.0\times10^{-61}\) and
\(3.55\times10^{-59}\), respectively. The 80-digit run reduces stress errors
below \(1.92\times10^{-76}\) and agrees with the 60-digit action and principal
coefficients to more than 45 digits. Zero printed numerical residuals are not
asserted to be exact symbolic identities.

## Selected third-mass derivative obstruction

For \(\epsilon_3=1.5\times10^{-6}\), positive \(U_3\) is determined by the
same signed \(H\) equation. A real mpmath root solve near \(y_3=0.16\) enforces
\(dH_3/dX=dH_1/dX\). It finds

\[
 y_3=0.160398504741293796249681,\qquad
 U_3=2.60284719305681252138095\times10^{-7}.
\]

The value mismatch is below \(1.6\times10^{-61}\), and the first-derivative
mismatch is below \(1.4\times10^{-56}\). This third local jet remains bounded
and strictly causal with the shared \(P_X,P_{XX},G_X,G_{XX}\).

For each halo, differentiate \(D_0+P_XD_1\) along its flow while holding
\(P_X\) fixed within that differentiated function, obtaining \(K_i\).
The full second derivative is \(K_i+D_{1i}P_{XX}\). Third-mass preservation
would require

\[
 P_{XX}^{(1,3)}=-\frac{K_3-K_1}{D_{13}-D_{11}}
 =37146432306.40535985082830,
\]

which is 14.6992 percent below the already fixed two-mass value. With the actual
shared value, \(H_{XX,1}=-1.09037606934254\times10^{11}\) and
\(H_{XX,3}=-9.34948558330960\times10^{10}\); their relative discrepancy is
0.1425448663 when normalized by the larger absolute value. This normalization
need not equal a diagnostic based on derivatives of \(\log|H|\).

This rejects smooth preservation through this particular third-mass root with
the fixed two-mass action derivatives. It does not exclude other roots, seeds,
metric completions, singular charts, or a different universal action.

## Formula review and reproducibility

No error was identified in the selected local formulas. The signed root solves
the unsquared equation with positive \(\sqrt U\). Direct chain differentiation
agrees with the source's \(a,b\) preservation construction; the source's total
curvature includes the explicit \(X\) derivative and every state derivative.
The source's \(G_{XX}\) and cone polynomial agree with this recomputation.
Numerically, the source's \(P_X,P_{XX}\) differ by less than
\(6.3\times10^{-16}\) relative; all compared action and principal entries
differ by less than \(2.7\times10^{-14}\). This is a local review, not an
audit of all continuation, event, or root-search behavior.

Run from repository root:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/precision/test_precision.py
```

Seven tests pass. `run_001/results.json` preserves the 60- and 80-digit results,
source-comparison errors, selected third-mass result, and test counts.
`run_001/manifest.json` records exact argument vectors, versions, input and
output hashes, exit status, and resource caps. This is numerical evidence
conditional on mpmath and the imported original principal expression.

The computation-audit skill supplied the independent-derivative contract and
provenance workflow. Proofread-math self-review covered this new report. No
literature, empirical novelty, full PPN, FLRW, global, or full-theory claim is
made. No commits or pushes were performed by this task.
