# Full-action finite-gradient initial slices, lapse closure and charge

2026-09-12. Bounded continuation from `738773278`. The actual archived
checkout was `9212f4498479039fb37dba5e71ef8452d28249dd`, dirty; pinned inputs
did not change during the run. Write scope: this directory.

**Primary verdict: computationally verified only in the stated range.**
Two nontrivial plane-symmetric finite-interval initial slices have been
constructed from the unchanged action, including its full gamma terms,
Hamiltonian and momentum constraints, clock constraint, and positive
clock-preserving lapse. The resulting instantaneous scalar/metric Hessians
give a negative longitudinal principal discriminant at every recorded point.
These are constraint-compatible initial patches, not merely added gradients
on an unchanged FLRW geometry. They are not globally matched solutions or
spacetime evolutions, and they do not establish an all-background no-go.

## Fixed action, geometry and data

The source remains `nonlinear_evolution_2026/constitutive.py`, including all
existing gamma-dependent coefficient terms. No coefficient is reconstructed.
The action is

\[
 S=\int\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)
       +P(X,\tau)-V(\tau)+sW(Y,\tau)+\gamma X\Box\chi\right]+S_m,
\]

with signature -+++, gamma=1e-6, M^2=1 and Lambda=.7. The normal is future
directed, and K is positive for expansion. On the initial slice,

\[
 h_{ij}=\delta_{ij},\quad K_i{}^j=\operatorname{diag}(k,h,h),\quad
 \tau=t=0,\quad s=N^{-1},\quad n\chi=Q,\quad D_x\chi=b(x),
 \quad X=Q^2-b^2,\quad Y=b^2.
\]

Here `h` is the transverse extrinsic-curvature eigenvalue, not the spatial
metric. Q is spatially uniform on this slice and is fixed to the first
physical sourced sample, Q=.9078321505772312. It is not the coefficient
reference qbar. The scalar itself is reconstructed by chi(x)=integral_0^x b.
The initial matter has normal-rest dust and radiation, with
rho_r=.01 and rho_b=.001+amplitude*exp[-(x/.3)^2]. No new matter species is
introduced. The central transverse expansion is .5191118192004086 and
N(0)=.9691978557978996, with N'(0)=0.

All calculations use x in [-.5,.5]. Central b is 0 for the homogeneous
control and Gaussian overdensity, and .009 for the uniform-matter gradient
case. The Gaussian amplitude is .0001. Matter density is localized in this
last example, but the complete field/metric data are not matched to an
exterior. In particular, its endpoint b values are approximately
plus/minus 2.51705e-5 and N' is approximately plus/minus .000197030;
neither is set to zero by an exterior boundary condition.

## Exact instantaneous constraints

Write p=P_X, r=P_XX, d=W_Y, C=d+2Y W_YY and theta=k+2h. A prime is a
spatial derivative on the initially flat slice. The general normal/spatial
scalar Hessian, before setting Q'=0, is

\[
 H_{nn}=A,\quad H_{nx}=Q'-kb,\quad
 H_{xx}=b'-kQ,\quad H_{yy}=H_{zz}=-hQ.
\]

Direct contraction of the covariantly varied cubic stress gives

\[
 \rho_3=2\gamma[Xb'-QXk-2Q^3h],\qquad
 T^3_{nx}=2\gamma[XQ'-b(Xk+2Q^2h)].
\]

Both constraints are free of A. With rho_m=rho_b+rho_r,

\[
 M^2(2kh+h^2-\Lambda)=2pQ^2-P+V+\rho_m+\rho_3,
\]
\[
 -2M^2h'=2pQb+T^3_{nx}.
\]

Varying the clock before imposing its aligned gauge gives the remaining
constraint

\[
 T\equiv V_\tau-P_\tau+W(k+2h)-2dkY-2QC b'=0.
\]

Its apparent spatial Q and lapse-gradient terms cancel. The code checks this
cancellation directly from the clock current, not by omitting those terms.
Hamiltonian plus clock are linear equations for (k,b'); momentum then gives
h'. Differentiating these same two constraints in x determines (k',b''),
including the Gaussian matter-density derivative. This is a regular local
ODE construction wherever its displayed matrix is nonsingular.

## Clock preservation is included

The lapse is not assigned arbitrarily after solving T=0. Let a_x=N'/N.
On the uniform-Q slice the geometric normal derivatives satisfy

\[
 nQ=A+a_xb,\quad nb=Qa_x-kb,
\]
\[
 n(b')=Q\frac{N''}{N}-a_xkb-k'b-2kb'.
\]

The last formula retains the normal/spatial-frame commutator. The two
spatial Einstein equations supply

\[
 nh=-\frac12\left(3h^2-\Lambda+T_{xx}/M^2\right),
\]
\[
 nk=\Lambda-k^2-kh-h^2+N''/N-T_{yy}/M^2-nh.
\]

The relevant complete stresses are

\[
 T_{xx}=P-V+s(W-2dY)+2pY
              +2\gamma[XA-2QhY]+\rho_r/3,
\]
\[
 T_{yy}=P-V+sW+2\gamma[Q^2A+QkY+Yb']+\rho_r/3.
\]

For B=g^{mu nu}H_mu_nu=Box(chi), v_cov=(Q,b,0,0), the exact scalar equation
on this slice is

\[
 E_\chi=2pB-4r\,vHv-2sQ P_{X\tau}-2sCb'
       +2\gamma[B^2-H:H-R_{\mu\nu}v^\mu v^\nu]=0.
\]

Einstein trace reversal substitutes the full stress, including the cubic
stress and the cosmological constant, into the last curvature contraction.
The result is exactly linear in A and s, with all gamma-squared feedback
retained. The script evaluates E_A,E_0,E_s and solves
A=A0+As/N, where A0=-E_0/E_A and As=-E_s/E_A. Neither denominator is
replaced by an anticipated kinetic coefficient.

Substituting these actual accelerations into nT=0 gives a linear lapse ODE

\[
 F N''+(F'+4Qbdh)N'+a_0N+f_0=0,
 \qquad F=W-2Q^2C-2Yd.
\]

All coefficients, including a0 and f0, are generated exactly and archived in
`result.json`. For a compact reconstruction, write
nh=u_h0+u_hs/N and nk=N''/N+u_k0+u_ks/N using the preceding Einstein
equations. Then

\[
 a_0=T_Q A0+T_k u_{k0}+T_h u_{h0}-T_bkb
          +T_{b'}(-k'b-2kb'),
\]
\[
 f_0=T_\tau+T_Q As+T_k u_{ks}+T_h u_{hs}.
\]

These partial derivatives treat the constitutive jets by their actual chain
rule, including X=Q^2-b^2. The lapse coefficient F is also the longitudinal
clock principal denominator. Its minimum in these runs is positive,
8.493856e-4; the spatial constraint-matrix condition stays below 114.78.

The slice and lapse equations are solved as central IVPs, not as a two-sided
asymptotic boundary-value problem. Their regularity and positive numerical
lapse provide a local initial-data construction; no spacetime existence or
nonlinear constraint-propagation theorem is supplied by these finite runs.

## Numerical outcome and independent checks

The following ranges cover 101 recorded points in each case. Xi is the
quarter-discriminant of the full cubic, metric-eliminated longitudinal
scalar characteristic, evaluated using the actual solved H and lapse.

| Case | Y range | s range | Xi range |
|---|---|---|---|
| Homogeneous control | zero to roundoff | 1.03178107 | -.00741482 |
| Uniform matter, finite gradient | [7.80012e-5,8.41748e-5] | [1.03138055,1.03178107] | [-5.59308e-4,-3.68913e-5] |
| Gaussian baryon overdensity | [0,6.33556e-10] | [1.03172370,1.03178107] | [-.00741482,-.00740135] |

Thus neither constructed nontrivial slice passes this principal stability
test. One negative direction suffices for failure; no all-direction stability
claim is inferred from only the recorded longitudinal and transverse probes.
These are sampled numerical sign results, not interval-certified coverage.

Fourteen exact algebra checks and five unit tests passed. Algebraic residuals
are below 2e-16 but, by themselves, would merely check solved equations.
Additional independent checks were therefore performed:

- A direct geometric Ricci tensor reconstructed from nk,nh,N''/N,h' agrees
  with the original scalar equation before Einstein elimination, with
  residual below 1e-16.
- Changing maximum spatial step .02 to .005 and relative tolerance 2e-10
  to 2e-12 changes the state by less than 5.81e-13.
- Fourth-order spatial finite differences of the independent dense solution
  differ from the ODE derivatives by less than 8.61e-12.
- A one-sided temporal finite difference recomputes the clock constraint
  from the actual coefficient functions along the solved initial normal
  jets. The largest residual decreases from 2.83e-11 at step1e-4 to
  8.02e-12 at step5e-5. This jet extension is not an evolved solution.
- Reversing b and the spatial frame leaves the principal discriminant
  invariant. The Hessian is reflected along with the gradient.

An independent reviewer reconstructed the slice stress, clock variation,
frame commutator, Einstein equations, scalar equation and lapse reduction,
and reran the five tests. No blocking equation finding was reported.
Analytical inputs remain the covariant variation/commutator and the
Gauss-Codazzi relations; the script does not mechanize all differential
geometry. The computation-audit and proof-audit workflows enforce these
separate evidence scopes. Mathematical self-review covered this report's
notation, equations and numerical claims.

## Charge density and instantaneous redistribution

Keeping Q equal to a sourced background value does **not** retain global
inherited scalar charge. The covariant shift-current projections, checked
from the full action, are at Q'=0

\[
 J^n=2pQ+2\gamma[Qb'-Xk-2Q^2h],
\]
\[
 J^x=2b(s d-p)+2\gamma b[A+Q(k+2h)].
\]

The coordinate clock-time boundary flux is N Jx. On this initially flat
box, charge per unit transverse area is integral Jn dx, and continuity gives
d/dt integral sqrt(det h_ij)Jn dx = (NJx)_left-(NJx)_right. This includes the time
variation of the volume measure. It is not the derivative of Jn alone.

| Case | Box charge | Left NJx | Right NJx | Instantaneous box-charge derivative |
|---|---:|---:|---:|---:|
| Homogeneous control | .09717242386330 | roundoff | roundoff | roundoff |
| Uniform matter, finite gradient | .09707980422225 | -.0008595637 | -.0008274830 | -3.208068e-5 |
| Gaussian overdensity | .09717242347572 | +2.359656e-6 | -2.359656e-6 | +4.719312e-6 |

The homogeneous comparison charge is .09717242386329555. The Gaussian box
has inward flux at both endpoints at this instant. The uniform-matter
gradient case has net charge loss. Neither sign is a reliable long-time
galaxy/depletion prediction because these data fail the principal test.
Global charge, asymptotic matching and future conservation over an evolved
domain were not imposed or demonstrated. No time finite difference of the
current was used: away from this instantaneous uniform-Q slice the general
current contains Q' terms, which could not consistently be omitted.

## Route status

The requested instantaneous full-action construction and its clock-lapse
closure have succeeded on a bounded local interval. The sampled stability
gate fails for both nontrivial patches. Exterior matching, different initial
families and genuine spacetime evolution remain separate questions; this
finite result excludes neither all coefficient-preserving initial data nor
all nonlinear solutions. It supplies no MOND solution, complete cosmology,
or CMB mapping. See `COMMANDS.md` for immutable run provenance and preserved
exploratory stages.
