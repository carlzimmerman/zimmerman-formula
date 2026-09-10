# Constant-F sector: direct local construction

Execution HEAD: `2bd887e8e93e1cb1cfa9942949184adb0e42d7eb`. Only this new
directory is owned by this subtask. The parent aggregate records final
input hashes. The action is the same one with **constant positive** \(F\):
\(F R+P(X)-G(X)\Box\phi\). No particle sector, independently fitted
halo acceleration, or different matter coupling is introduced. One global
constant \(a_0\) remains the unit choice, and \(\phi=-t+\psi(r)\).

The normalized chart \(w=F_X X'\) is singular when \(F_X=0\). This
does **not** make the physical field map singular: \(C=2F>0\),
\(\chi=X/C\), and \(C-XC_X=C\ne0\). The present construction does not
divide by \(F_X\) or take an ill-conditioned normalized-chart limit.

## Direct raw equations and compatible clock

With \(z=X'\), \(U=p^2/B\), \(p=\psi'\), \(Q=2X+U\), and
\(C_J=2(U/r-Xg)/p\), the undivided equations give

\[
P=2Fp_r,\qquad P_Xz=2Fp_r',\qquad
P_X-C_JG_X=0,\qquad (2Xz/p)G_X=2F(\rho+p_r).
\]

Hence compatibility requires

\[
\left(\frac{U}{Xr}-g\right)(\rho+p_r)=p_r'.
\]

Using the geometric identity
\(p_r'=-g(\rho+p_r)+2(p_t-p_r)/r\), define

\[
c(r)=\frac{p_t-p_r}{\rho+p_r},\qquad
U=2Xc,\qquad
z=-X\left(2g+\frac{c'}{1+c}\right).
\]

The last relation follows by differentiating \(U\) and requiring the
actual clock norm derivative \(U'=-2gQ-2z\). It also ensures
\(A=1/[2X(1+c)]\) has \(A'/(2A)=g\). Thus this is a locally
constructible radial clock, not an independently assigned \(X'\).
For \(X,F>0,c>0,z\ne0,\rho+p_r\ne0\), reconstruct

\[
P_X=\frac{2Fp_r'}z,\qquad
G_X=\frac{Fp(\rho+p_r)}{Xz}.
\]

`jets` differentiates these first jets along
\((dy/dr,dX/dr)=(1/r_y,z)\), then divides by \(z\), to obtain
\(P_{XX},G_{XX}\). No action curvature is a health control. Since
\(z\ne0\), local integration gives functions \(P(X),G(X)\) for this
one background. This does not assert one action works for another mass
or extends to cosmology/interior boundary data.

## Corrected logarithmic target and actual single point

Use the committed reference geometry
\(r=\epsilon/\sqrt{y(1-e^{-y})}\),
\(B=4/[1+\sqrt{1-4ry}]^2\), \(g=yB\).
Exact symbolic substitution verifies
\(p_r=-g^2/B\), \(p_t=+g^2/B\). The metric and its derivatives are
not taken from the earlier zero-pressure target.

At 65 digits, \(\epsilon=10^{-6},y=.1,X=.5,F=.525\), the actual
construction gives approximately

\[
U=1.05160731788743\,10^{-6},\quad z=-.0973372403392067,
\quad P=-.0105000215271878,
\]
\[
P_X=-21576.6558343405,\quad G_X=-210.385014068784,
\quad P_{XX}=-4.49876221150479\,10^{10},
\quad G_{XX}=-2.16978799368392\,10^8.
\]

The original coupled KGB principal, evaluated using the **constant**
conformal EF map and these actual derivatives, has

\[
\mathcal M_{00}\simeq-2.03740442568\,10^9,\quad
\mathcal M_{01}\simeq-2.22037605236\,10^7,\quad
\mathcal M_{11}\simeq-62322.985852,\quad
\mathcal M_{22}\simeq+22202.042726.
\]

This point fails the strict local EF static scalar-energy and cone
criterion. That is a computed single-point result, **not** an all-\(y\),
all-mass, constant-F or full-theory no-go. The regular map itself passes:
\(C-XC_X=1.05\), and the areal-coordinate Jacobian is one.

## Checks and reproduction

Three tests pass: exact geometric/clock compatibility, physical plus
independent EF Einstein/current residuals and map regularity, and action
curvatures checked by independently summed radial partial derivatives.
`results.json` records residuals and the full evaluated coefficients.
The first TDD run failed because the implementation was intentionally
absent; the final runner exits zero.

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_logslip_joint_2026/constant_f/run_constant_f.py --result-file qwen_claude_field_theory/closure_2026/kgb_logslip_joint_2026/constant_f/results.json
```

EF evaluation is exterior-vacuum only. It is not a full physical-frame
Hamiltonian/Dirac analysis or a matter-coupled stability certificate.
No PPN value or propagating-mode count is assigned. No matched two-mass
action, global clock normalization against boundary data, radial health
continuation, CMB likelihood, or empirical novelty is claimed. Exceptional
\(c\le0\), \(\rho+p_r=0\), and \(z=0\) sectors are explicitly
rejected by this local reconstruction, not silently declared impossible.
