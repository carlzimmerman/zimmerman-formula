# A different inverse source that preserves a nonlinear lapse constraint

This is a new candidate action, not the old inverse-Ricci action with coefficients renamed. It closes exact background matching and a nonlinear Hamiltonian-constraint step. Full constraint closure, curved-background stability and a physical realization remain open.

## Why deleting one quadratic coefficient is insufficient

At H_AB=0, the old inverse-metric strains with their explicit clock coefficient deleted still give, at γ=I and constant shift β,

\[
\sqrt{-g}L_{\rm strain}=h[2|\beta|^2-|\beta|^4/2]/N^3.
\]

The absence of a quadratic α² term at β=0 does not make this expression linear in N nonlinearly. At β=(v,0,0), its local potential Hessian has lapse Schur complement

\[
-{12hv^2(v^2+2)\over N^5(2-3v^2)},
\]

which is nonzero at generic small v≠0. This is a potential-sector degeneracy failure. It is not, by itself, a full Hamiltonian ghost proof for an action containing derivative repair operators. It does show why the flat quadratic constraint theorem cannot be promoted to a nonlinear theorem just by setting one coefficient to zero.

## Use proper material velocity and spatial strain

Keep the clock U and projector P, and define

\[
B^I=U^\mu\partial_\mu\Phi^I,\qquad
C^{IJ}=P^{\mu\nu}\partial_\mu\Phi^I\partial_\nu\Phi^J-\delta^{IJ}.
\]

In unitary gauge Φ=x these are **exactly** B=−β/N and C=γinverse−I. Consider the algebraic constitutive theory

\[
S=\int\sqrt{-g}[M^2R/2+\mathcal F(\Phi,B,C)]\,d^4x.
\]

No Θ-square, derivative elasticity, acceleration square or shear-gradient operator is included in this particular candidate. Importing those terms would require redoing the nonlinear Hamiltonian argument below.

Let the desired steady target again have γ*=I, N*=1, β*=b(Φ)ez, with b=Vσ(r). Take its required Einstein source and decompose it in the normal frame as energy ρ, momentum ji=−Tni, and spatial stress Sij. Put B*=−b ez and define

\[
F_0=bj_z-\rho,\qquad f_I=-j_I,\qquad
A_{IJ}=\tfrac12(F_0\delta_{IJ}-S_{IJ}).
\]

An explicit source is

\[
\mathcal F=F_0+f_I(B^I-B_*^I)+A_{IJ}C^{IJ}
+2h|B-B_*|^2-\tfrac h2|C|^2,
\]

where h≥0 is a smooth compact profile containing the curvature source. Other constitutive second derivatives could be studied; the displayed quadratic completion is a definite candidate, not a stability certificate. It supplies positive normal-velocity stiffness and positive spatial strain energy in the flat rest limit.

### All ten Einstein source components match

At the target, δB=b ez δN−δβ and δC=−δγ. Therefore

\[
\delta(N\sqrt\gamma\mathcal F)
=(F_0+b f_z)\delta N-f_i\delta\beta^i
+(F_0\delta_{ij}/2-A_{ij})\delta\gamma_{ij}
=-\rho\delta N+j_i\delta\beta^i+\tfrac12S_{ij}\delta\gamma_{ij}.
\]

This is the full ADM matter variation, so it matches all ten components of the specified target stress, not only the normal energy. The quadratic completion vanishes with its first variation. Taking (ρ,j,S)=M²G[g*] therefore makes that stationary metric an exact solution of the metric equations. General covariance and the invertible material-coordinate Jacobian then imply the four scalar equations through the Bianchi identity. This is a constructed constitutive source, not a prediction of a known medium.

For the smooth spherical wall, curvature vanishes outside its transition. Thus F0,f,A vanish there. Choosing h compact gives an exactly Einstein exterior in the pure gravitational/material action. B* may remain a nonzero constant there, but it multiplies no matter density once these coefficients are zero.

The wall still requires

\[
\rho=-{M^2\over4}[(\partial_xb)^2+(\partial_yb)^2].
\]

Negative source energy has not disappeared. No baryonic material, dark-energy constituent or manufactured cold carrier has been shown to realize these functions.

## Exact nonlinear lapse factorization for this action

The constitutive action contains no metric velocity. The Einstein canonical Hamiltonian, after the usual integration by parts, has density N HGR+βi Pi. The matter contribution is −N√γ F(C,−β/N). Write β=N s. Then

\[
\mathcal H=N[H_{\rm GR}+s^iP_i-\sqrt\gamma\mathcal F(C,-s)].
\]

The s equations are independent of N. Where FBB is invertible they determine s(γ,p,Φ), and eliminating s leaves N times a function independent of N. Thus the lapse still enforces a **nonlinear Hamiltonian constraint**. In vacuum, where the constitutive coefficients vanish, s imposes the usual spatial Einstein constraints instead of being inverted; factorization still holds. There is no division by h at a material boundary in this statement.

For the displayed quadratic completion, in the region h>0 this reduction can be written explicitly. Set Fsp=F0+A:C−h|C|²/2. Then

\[
H_{\rm eff}=H_{\rm GR}-B_*^iP_i-\sqrt\gamma F_{\rm sp}
+{|P+\sqrt\gamma f|^2\over8h\sqrt\gamma}.
\]

The stationary shift ratio is s=−B*+(P/√γ+f)/(4h). The denominator is used only on h>0; in vacuum the unreduced GR constraints must be retained. This formula makes the next exact question explicit: evaluate the Poisson bracket of H_eff(x) and H_eff(y), preserve all resulting constraints, and determine the actual reduced degrees of freedom. In particular, the flat rest theory can have nondynamical directions that activate on a curved background; a benign quadratic rest energy does not rule out such strong coupling.

This is stronger than vanishing of a single quadratic α² coefficient. It does **not** establish the Poisson algebra of the remaining constraints. Preservation in time can produce further constraints or an equation for the lapse. The nonlinear degree-of-freedom count, any instantaneous modes and ghost freedom require that analysis. In ordinary Dirac terminology the lapse momentum is a primary constraint and its equation supplies a Hamiltonian constraint; no further constraint is being assumed here.

At the flat rest state V=0, the source jets vanish and the displayed F reduces to 2hB²−hC²/2. Its quadratic action belongs to the globally constrained finite-body theorem in [REPLACEMENTS.md](REPLACEMENTS.md), with θ=κ=0 and h_s=h_m=h. It has nonnegative physical quadratic energy in that scoped sense. Some directions are nondynamical or gauge null; this is not a strict kinetic gap or a nonlinear mode-count proof.

## One fixed action containing the stationary speed family

Promote V to Λ, and define the constitutive coefficients above from the constant-parameter target b=Λσ(Φ), evaluated as functions of Φ and Λ. The theory does not assert that substituting an arbitrary Λ(t,x) in the target metric solves the equations.

The target normal momentum and energy, independently obtained from the flat-slice Hamiltonian and momentum constraints with Kij=−(∂ib δjz+∂jb δiz)/2, are

\[
j_z={M^2\Lambda\over2}\Delta_\perp\sigma,\quad
j_x=-{M^2\Lambda\over2}\sigma_{xz},\quad
j_y=-{M^2\Lambda\over2}\sigma_{yz},\quad
\rho=-{M^2\Lambda^2\over4}|\nabla_\perp\sigma|^2.
\]

Take h independent of Λ. Differentiating F with respect to Λ **at fixed B and C**, before evaluating on the target, gives

\[
\left.\partial_\Lambda\mathcal F\right|_*
=b\partial_\Lambda j_z-\partial_\Lambda\rho
={M^2\Lambda\over4}\Delta_\perp(\sigma^2).
\]

The transverse Laplacian, and its sign, differ from the old inverse-Ricci source because this is a different off-background action. Reusing the old controller current would be wrong.

Let E_A^μ be the inverse material-coordinate Jacobian. Add

\[
L_\Lambda=-\tfrac12F_c^2(\partial\Lambda)^2+J^\mu\partial_\mu\Lambda,
\qquad
J^\mu={M^2\Lambda\over4}(E_1^\mu\partial_{\Phi^1}+E_2^\mu\partial_{\Phi^2})\sigma^2.
\]

At each constant Λ target, ∂Λ=0, so the added densities and metric/material first variations vanish. The Λ variation is FΛ−∂μJμ, which is zero on that target since √−g=1. Thus one specified covariant action now contains the whole stationary family. The current is compact because σ is constant outside the wall.

In unitary gauge J0=0 and JI is independent of N and β. Its density is N√γ JI∂IΛ, hence also linear in N. The canonical scalar has Hamiltonian N HΛ+βi πΛ∂iΛ. Both retain the lapse factorization above when β=N s. This establishes preservation of that nonlinear Hamiltonian-constraint step in the extended candidate. It does not prove positivity of the coupled controller modes. The previous unconfined-controller stiffness/activation numbers cannot certify this different action.

An optical energy input could be postulated as before, but no such input, carrier conversion or operating pulse is included in the positivity theorem. The source, current and clock are hypothetical fields, not laboratory components.

## What this actually closes

Exact finite-source stationary matching, a correct controller source/current, and nonlinear lapse factorization are now explicit for the proper B,C candidate. The previous stronger-κ finite clock-mass route is closed by a counterexample, not left as a missing proof. What remains mathematically decisive for this new candidate is the full constraint algebra and reduced curved-wall energy, followed by a controlled launch and payload solution. Physical realization of the source is a separate unsolved problem.
