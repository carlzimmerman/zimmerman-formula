# Exact zero-field MOND destabilizes this trace-constrained metric candidate

2026-09-08. Base `89588dd6f76c1996d8deee5cf6084eec41c2e614`.

**Verdict: the specific VCDM+f(a²) candidate fails the healthy matter-FLRW
requirement.** This is an action-derived obstruction, not a failure to find
a numerical parameter fit. The overall gravity research objective remains
OPEN; other kinetic/constraint architectures are not excluded.

## 1. Precise theorem and assumptions

Consider the candidate proposed in `../gate1_constitutive_2026/`:

\[
S_g=M^2\int dt\,d^3x\,N\sqrt h\left[
\frac{R+K_{ij}K^{ij}-K^2}{2}-V(\varphi)-\frac34\lambda^2
-\lambda(K+\varphi)-\frac{\lambda_{\rm gf}^i}{N}D_i\varphi+f(s)\right],
\]
\[
s=a_i a^i,\quad a_i=D_i\ln N,\quad
f(s)=2a_0^2[1-(1+y)e^{-y}],\quad y=\sqrt{s}/a_0.
\]

Units c=1, M²>0, Kij=(dot h_ij-Lie_shift h_ij)/(2N). Ordinary matter
couples to this same metric through Sm=integral sqrt(-g) P(X), with
X=-(partial sigma)²/2. On a smooth flat FLRW background let

\[
q=\dot{\bar\sigma}\ne0,\quad Z=P_X>0,\quad
D=P_X+q^2P_{XX}>0,\quad c_m^2=Z/D.
\]

These are the standard positive kinetic/spatial coefficients of the matter
action before coupling. The result concerns nonzero spatial modes, regular
background coefficients, and the continuum/local high-momentum regime of
THIS explicit action, with no unspecified higher-derivative completion.

**Claim proved below:** f_s(0)=1 implies a negative reduced matter kinetic
coefficient and a negative physical high-momentum squared propagation
coefficient on every such FLRW solution. No differentiable choice of the
derivative-free V removes it. This does not assert a no-go for all MOND,
all clocks, or all two-tensor theories.

The unmodified VCDM action is published, not claimed as our invention:
[De Felice, Doll and Mukohyama, arXiv:2004.12549v2, Eq. 36](https://arxiv.org/html/2004.12549v2).
The new calculation here is the modified coupled FLRW gate; no global
novelty search has been performed.

## 2. Why this is the exact MOND endpoint

The static weak-field variation gives mu=1-f_s. The chosen f has
f_s=e^-y, so mu=1-e^-y. Around FLRW, a_i=0 and

\[
f(s)=s-\frac{2}{3a_0}s^{3/2}+O(s^2),\qquad f_s(0)=1.
\]

The quadratic lapse-gradient term is therefore fixed; it is not an adjustable
cosmological parameter. The amplitude expansion is taken at fixed wavelength
before the local high-momentum limit. Cubic nonanalytic terms cannot correct
the linear principal coefficient. A cutoff/new operator would define a
different completion, whose constraints and static law must be checked anew.

## 3. Vary, eliminate, and retain the homogeneous mode

Lambda variation gives lambda=-2(K+varphi)/3. Substitution yields

\[
\mathcal L_g/(M^2N\sqrt h)
=\tfrac12R+\tfrac12K_T^{ij}K^T_{ij}+\tfrac23\varphi K
+U(\varphi)+f(s),\qquad U=\varphi^2/3-V.
\]

The multiplier equation is D_i varphi=0. For k!=0 it removes delta varphi,
but NOT its homogeneous value. Since
N sqrt(h) K=partial_t sqrt(h)-partial_i(sqrt(h)N^i), its trace term can be
integrated to -(2/3)M² dot(varphi) sqrt(h). The script independently expands
both forms and verifies the discarded boundary term exactly.

The background equations used in the reduction are

\[
M^2U=\rho=q^2Z-P,\quad
\dot\varphi=\frac{3q^2Z}{2M^2},\quad
3H+\varphi=\frac32V',\quad
\partial_t(a^3Zq)=0.
\]

These allow H!=0. They are not static approximations. In particular V=0,
P=X² admits a=sqrt(t), M=1, q=1/sqrt(t), rho=3/(4t²), varphi=-3/(2t).

Matter conservation is not the failure: varying Sm gives
E_sigma=nabla_mu(P_X nabla^mu sigma)=0 and
T_m^{mu nu}=P_X nabla^mu sigma nabla^nu sigma+P g^{mu nu}.
The product rule and symmetry of scalar second derivatives give the off-shell
identity nabla_mu T_m^{mu nu}=E_sigma nabla^nu sigma. Hence ordinary matter
is conserved on its own field equation; no extra nonmetric force was added.

## 4. The complete scalar quadratic action in spatial gauge

Set h_ij=a² exp(2 zeta) delta_ij, N=1+n and use one real mode:
zeta=z cos(kx), delta sigma=u cos(kx), N^x=v sin(kx).
Let kappa=k/a and alpha=f_s(0). The code builds the actual ADM extrinsic
curvature and spatial Christoffel/Ricci tensors. Twice the spatial average
gives L2=a³ times

\[
\frac D2\dot u^2-qD n\dot u+3qZ z\dot u+\frac{q^2D}{2}n^2
-\frac{Z\kappa^2}{2}u^2+qZkvu
+M^2[\kappa^2(z^2+2nz+\alpha n^2)+k^2v^2/3].
\]

The background z² and nz terms cancel separately between gravity and matter.
No metric velocity or source term is discarded after the action is varied.
The nonzero-mode auxiliary varphi equation fixes its longitudinal multiplier;
it does not supply an extra equation deleting this matter mode.

At alpha=1, write w=z+n. Direct variation gives

\[
w=-\frac{3qZ\dot u}{2M^2\kappa^2},\quad
n=\frac{D+3Z}{qD}\dot u,\quad
v=-\frac{3qZ}{2M^2 k}u.
\]

The auxiliary Hessian determinant is computed to be
4D M^4 kappa² k² q²/3, strictly positive in the stated domain. All three
solutions give zero residual in the original variations.

Consequently

\[
L_{\rm red}=\frac{a^3}{2}[\mathcal K\dot u^2-\mathcal B u^2],
\]
\[
\boxed{\mathcal K=-6Z-\frac{9Z^2}{D}
-\frac{9q^2Z^2}{2M^2\kappa^2}<0},\qquad
\mathcal B=Z\kappa^2+\frac{3q^2Z^2}{2M^2}>0.
\]

All terms in -K are positive. This sign is an analytic result over the stated
domain, not a finite scan. The physical high-momentum coefficient is

\[
\boxed{c_{\rm UV,eff}^2=\lim_{\kappa\to\infty}
\frac{\omega^2}{\kappa^2}=-\frac1{6+9c_m^2}<0.}
\]

Canonical P=X gives -1/15; radiation-like P=X² gives -1/9. Negative kinetic
energy is relative to the positive tensor/matter-control normalization.
Independently, the negative UV frequency coefficient demonstrates a gradient
instability. Finite-k B/K is only a frozen-coefficient diagnostic; exact
expanding-space evolution uses (a³ K u_dot)_dot+a³ B u=0.

This is not a gauge-only mode. Its density perturbation is
delta rho=qD(u_dot-qn)=-3qZ u_dot. It equals the gauge-invariant combination
delta rho-(rho_dot/varphi_dot)delta varphi on uniform-varphi slices, because
varphi_dot=3q²Z/(2M²) is nonzero.

For alpha=0, the independently reduced control instead has K->D and
c_UV²->Z/D. The modification, not the bare matter sign, causes this UV failure.
No inference about a physical IR ghost is drawn from finite-k rational poles
of a particular control variable.

## 5. Canonical preservation and exceptional strata

For the scalar quadratic sector retain (u,n,z,v) and all four canonical
momenta. Only u has a velocity: p_n=p_z=p_v=0 are primary. The script
Legendre-transforms L2, generates three secondaries by Poisson brackets,
and calculates the full six-by-six matrix. Its determinant is

\[
\det\Omega=\frac{4M^4 Z^2a^{14}k^4q^4}{D^2}
[4DM^2k^2+3DZ a^2q^2+6M^2Zk^2]^2>0.
\]

The computed rank is six: all six are second class and one matter canonical
pair remains. Secondary preservation determines the three primary multipliers;
the script checks exact zero residuals, including arbitrary explicit time
derivatives of the secondary coefficients. No tertiary condition can be used
to remove the unstable mode on this regular stratum. This is a gauge-reduced
quadratic scalar count, not a full nonlinear gravitational DOF certificate.

**q=0 is recalculated, not reached by dividing by q.** For canonical vacuum
matter there are two independent secondaries, bracket rank four, one linear
first-class direction and a healthy free matter scalar. This extra linear null
direction does not prove a nonlinear gauge symmetry. Empty vacuum cannot
certify the matter-filled cosmology by continuity.

**k=0 is independently retained.** For canonical matter and volume v0=a³,
define W=V-varphi²/3 and gamma=2M²/3. The actual homogeneous Lagrangian is
L0=gamma varphi dot(v0)-N M²v0W+v0 dot(sigma)²/(2N). Its constraints are
p_N, p_v0-gamma varphi, p_varphi, and C=M²v0W+p_sigma²/(2v0).
Their computed bracket rank is two, with two first-class and two second-class
constraints on regular backgrounds; preservation closes exactly. V''=2/3
does NOT change this rank. A constructed de Sitter solution with positive
stiff matter verifies this special coefficient explicitly. At rho=H=0 the
constraint differential can become irregular; the generic count is not used
there. These homogeneous controls do not repair the k!=0 instability.

## 6. Actual expanding radiation evolution, not only a frozen symbol

On the exact V=0, P=X² background above, evolve the DERIVED reduced equation
from t=1 to 4, k=30, initial (u,u_dot)=(1,10). These dimensionless amplitudes
define a linear transfer function and can be scaled down arbitrarily.

| Run | Final u | Sampled maximum of abs(u) |
|---|---:|---:|
| Exact-MOND candidate | 487,932,737.7333 | 487,932,737.7333 |
| Unmodified control | -1.03135 | 1.15619 |

DOP853 relative tolerances 1e-9 and 1e-11 change the MOND result by
2.52e-9 relatively. An independent Radau calculation using separately derived
ODE coefficients agrees to 2.3e-11 relatively. This is linear amplification,
not observed data, nonlinear structure formation or a prediction that finite
perturbations remain linear through that growth.

## 7. Consequences for the research programme

The proposed VCDM+f theory is **DEAD as a healthy ordinary-fluid FLRW
completion under the assumptions above**. Changing only V, or keeping only
vacuum de Sitter, cannot rescue it. There is no justification for spending
tokens on this candidate's full PPN or cluster fits before changing the action.

The independently checked G03 causal-symbol transfer supplies a separate
conditional obstruction at finite nonzero acceleration: the D_i varphi
constraint removes its nonzero mode, leaving the same leading metric/lapse
block and the nonlocal curvature coefficient. That transfer still needs its
regular-background/source-domain assumptions. The FLRW instability established
here does not rely on arbitrary external conserved sources: its matter is
varied and evolved from the same action on an explicit solved background.

**Next necessary research question:** can a different degenerate kinetic or
constraint structure distinguish a static galaxy from a homogeneous expanding
universe, retaining the exact static exponential law without inheriting this
negative matter coefficient? Any proposed new term must first pass both the
velocity-Hessian/constraint test and this same P(X) FLRW control. Merely
renaming the homogeneous potential is not a new route. No such repaired
action is certified in this checkpoint, and no global novelty claim is made.

Independent reviewers reconstructed the quadratic action, canonical brackets,
physical density mode and numerical evolution. Final reviewed script SHA-256:
`940d0b2eb80892abd00e31589795e560e0fb805c3866eb70283dee25c36c6850`.
Mathbox's computation and proof audits enforced separate k=0/q=0 treatment,
control checks and explicit limits on the no-go. All original files remain
unchanged; commands, exits and new-file inventory are in REPRODUCE.md.
