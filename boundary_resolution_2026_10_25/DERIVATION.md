# Boundary drift: force, grid resolution, and a new combined test

The target remains simultaneous material/conversion equilibrium, original law through 50 kpc, materially populated transition, restoring finite boundary, and a free exterior. Total mass stays 5.364 Mb. The law requires 4.801579 Mb inside 50 kpc; density, radius and exterior mass may all adjust. No target-law penalty, density prior or prescribed boundary is added.

## What pushes a response-weighted wall outward

In an approximately empty transition region, hold the enclosed T mass M fixed and write u=M/R². The base phase energy per area is

    ∫[(ell²/2)F(u)x′²+beta C F(u)s(x)]dr,
    s=sin²(πx)/π².

For a locally planar, stationary unit wall with u treated as constant across its width, the first integral gives ell²x′²/2=beta C s. The tension coefficient is

    sigma_response = A F(u), A=2 ell sqrt(2 beta C)/π².

Thus the spherical thin-wall energy is

    E_response(R)=A R²F(M/R²)=A M²/(R²−M),
    F_response=−dE/dR=2 A M²R/(R²−M)²>0.

It falls approximately as R^-2 and pushes outward. This is a controlled thin-wall comparison in a depleted region, not the full force in a materially populated transition. Curvature, finite width, changing enclosed mass and material stresses modify it. A local positive Hessian on a coarse grid cannot by itself eliminate this force or establish convergence. The derivation provides a physical diagnostic, not a proof that every saved drift is solely a grid artifact.

## Constant surface stress supplies an inward force

Add the existing type of interface area energy, now tested jointly with mobile coupled material stiffness and no supplied charge:

    E_sigma=sigma∫r²D(q′)dr,
    D(v)=sqrt(v²+delta²)−delta, q=sin²(πx/2).

No prescribed radius appears. Its complete variations per radial volume are

    μrho,sigma=0,
    cq,sigma=−sigma r⁻²∂r[r²D′(q′)],
    cx,sigma=cq,sigma q_x.

Species potentials receive

    μT,sigma=(1−q)cq,sigma/rho,
    μF,sigma=−q cq,sigma/rho,
    force_i,sigma=−∂r μi,sigma.

The boundary variation is sigma r²D′ δq. Pure endpoints require varying the energy directly, not dividing by q_x=0 or rho=0. The term does not directly bind matter at fixed phase: material support must come from the full coupled equilibrium. It is therefore not presumed to solve the gap.

For a sharp monotone unit wall E_sigma≈sigma R² and F_sigma≈−2 sigma R. At fixed M, the approximate combined energy has a finite minimum:

    Ewall=sigma R²+A M²/(R²−M),
    R_*²=M[1+sqrt(A/sigma)],
    Kwall=8 A M² R_*²/(R_*²−M)³>0.

This supplies an inward stress without introducing charge production. It is a new combination with coupled mobile material stiffness, not a claim that the earlier standalone area/charge routes succeeded. M is an equilibrium output. The full calculation must include gravity, F pressure, conversion, changing M and density relaxation; the sharp-wall radius is not imposed.

## All retained material and conversion forces

Let a=sqrt(rho), w=a′−eta a q′ and κ=(L/rM)³. The coupled material energy is Ec=κ/2∫r²w²dr, with

    μrho,c=−κ/(2 a)[r⁻²∂r(r²w)+eta q′w],
    cq,c=κ eta r⁻²∂r(r²a w).

Define A0=W′(u)+beta C F′(u)s+(ell²/2)F′(u)x′²,
Psi=∫ᵣ∞A0 ds, Xi=beta C F s′−ell²r⁻²∂r(r²F x′), and hF=(5/2)K[rho(1−q)]^(2/3). Full derivatives are

    μrho=Phi+q Psi+(1−q)hF+μrho,c,
    cx=rho q_x(Psi−hF)+Xi+q_x(cq,c+cq,sigma).

Transform via μT=μrho+(1−q)cx/(rho q_x), μF=μrho−q cx/(rho q_x), then take negative radial derivatives for the forces. Gravity includes baryons and every material cell; all mixed terms are retained by differentiating one energy. Coupled stiffness still adds a bulk force, so the cold-law proof is not automatically preserved. Positive fixed-density wall stiffness is not the relaxed stiffness; test the full tangent Hessian and joint displacements.

## Grid test

The previous quadratic grids supplied only a few cells across the wall. BR-1 instead uses a fixed physical interval 25–225 kpc with 2 kpc spacing,64 quadratic core cells and 32 logarithmic exterior cells. It does not move its concentration to a desired boundary. A promising state must be rechecked at 1 kpc or finer spacing, with material support measured across both sides of the interface (at least to 1.2 R), endpoint-aware law errors and the mass budget. Tails near the density floor do not count as support.

Screen coefficients: L=1 kpc with sigma=.003,.01,.03, plus L=3 kpc with sigma=.01; beta 2,K 30,phase length 10 kpc,eta 3,charge 0,domain 12. All are constitutive hypotheses, not microscopic deductions or observational fits. Both original and added surface stresses are counted exactly once: the inherited carrier model has tau 0, and the new term is added explicitly.

## BR-5: density-gated conversion chemical energy

Surface stress stabilizes a radius but does not by itself feed enough mass into the galaxy. Test the new local conversion energy

    Echem=−epsilon∫r² rho q S(rho)dr,
    t=clamp[(rho−.001)/.002,0,1],
    S=t³(10−15 t+6 t²).

The density thresholds and epsilon are new constitutive parameters, not quantities derived from the original formula or a microscopic theory. The gate is evaluated on the actual evolving density, not radius or a target density curve. The full derivatives are

    μrho,chem=−epsilon q[S+rho S_rho],
    cq,chem=−epsilon rho S,
    μT,chem=−epsilon[S+q rho S_rho],
    μF,chem=−epsilon q rho S_rho,
    force_i,chem=−∂r μi,chem.

All gate derivatives are essential in the switch region. In a saturated dense region S=1,S_rho=0, the T potential is shifted by the constant−epsilon and the F potential is unchanged: both added transport forces vanish there, including in mixed material. The term changes conversion energetics. In dilute material S=0 and every added first variation vanishes. It can still draw the entire reservoir inward or induce a dense shell; the exterior population must be measured, not presumed.

The local density curvature contribution is−epsilon q[2 S_rho+rho S_rhorho], which is not necessarily positive. Thus the chemical hypothesis needs a coupled Hessian and refinement check. A positive scalar gradient energy does not automatically cure a negative local compressibility. The mechanism is a static energy hypothesis; conversion heat transport, microscopic latent heat and physical formation dynamics are not provided.

At L=0, the pure dense cold-T transport equation remains exactly g=W′(u), and hence g²/(1+g)=gb+gF. At L>0 the already derived material-gradient force remains. In the actual transition, finite phase gradients, nonzero F source and density-switch derivatives still require a numerical law check. Echem cannot be called a proof of exact law preservation everywhere.

BR-5 varies epsilon=.03,.1,.3 with sigma=.01,ell 10 kpc,L 1,eta 3,beta 2,K 30. BR-6 tests ell 3 kpc,sigma=.003, preserving the sharp-wall ratio A/sigma, at epsilon=.2,.3 and L 0,1. A fixed mesh resolves 35–80 kpc at.5 kpc spacing with 80 core and 64 exterior cells. Removing L is an ablation of the added bulk-gradient force, not a change to the original gravity/response/phase-pressure energy. No enclosed mass or law residual is constrained in these minimizations.

## Removing the density-gate chemical-potential overshoot (BR-16)

The density-gated binding term has a thermodynamic problem distinct from mesh
resolution: its T chemical potential is `-epsilon[S+q rho S']`. The extra
`rho S'` can favor the activation-density band more strongly than the dense
core. Adding stiffness of S then preserves a dense shell rather than supplying
the desired inward redistribution. BR-14 initially also missed negative KKT
forces in microscopic mass cells; BR-15 corrects that active set. Neither is a
successful physical construction. The old fixed-density, spatially gated
binding in finite_interface is a different route: its position dependence
introduced an unacceptable bulk force.

A new, explicitly postulated local phase free energy is

    e_add(rho,q) = q (B - epsilon rho),  B>0, epsilon>0.

B is a constant energy per volume and epsilon a constant energy per T mass.
There is no radius selector, density gate, extra global density stiffness or
constant surface tension in BR-16. The original response-weighted wall energy
is retained. Fixed total mass is unchanged. This is a constitutive hypothesis,
not a microscopic derivation or an empirical determination of B and epsilon.

At fixed rho and q its variations are

    mu_rho,add = -epsilon q,     c_q,add = B-epsilon rho.

With rho_T=rho q and rho_F=rho(1-q), the species potentials and radial forces are

    mu_T,add = -epsilon + B(1-q)/rho,
    mu_F,add = -B q/rho,
    f_T,add = B[q'/rho + (1-q)rho'/rho^2],
    f_F,add = B[q'/rho - q rho'/rho^2].

These are accelerations per species mass, added to all previous forces. The
singular-looking species expressions are used only where rho>0; the actual
energy and its fixed-rho,q variations are nonsingular. Additional pressure is
`P_add=-B q`. In pure T, the binding potential is constant, so the added force
vanishes and the old cold-T galaxy law is retained. In pure F, the F potential
and added force vanish. In the mixed wall all derivatives must be retained.
An approximately pure F tail is still subject to its gas and gravity forces;
"free reservoir" means conversion and added interactions are not imposed there,
not that the reservoir is force-free.

Near the all-F phase x=0, q=pi^2 x^2/4+O(x^4), so the new local quadratic phase
coefficient, including the original F gas, is

    (pi^2/4) [B-rho(epsilon+h_F)] x^2, h_F=(5/2)K rho^(2/3).

Response W starts at quartic order here. Dense matter can prefer conversion
while sufficiently dilute matter remains locally stable in F. This is an
actual seed-stability criterion, not evidence of time-dependent formation.

For an empty thin transition surrounding fixed T mass M, let
`A=2 ell sqrt(2 beta C)/pi^2`. The response wall energy and added volume cost give

    E_wall(R) = A M^2/(R^2-M) + B R^3/3,
    F_R = 2 A M^2 R/(R^2-M)^2 - B R^2,    R>sqrt(M).

Writing `E'=R h(R)` with `h=B R-2 A M^2/(R^2-M)^2`, h increases strictly from
minus infinity to plus infinity. Thus there is exactly one finite-radius
minimum on this fixed-M thin-wall branch. At its root,

    k_R = B R + 8 A M^2 R^2/(R^2-M)^3 > 0.

This calculation derives the restoring term but does NOT establish restoration
when density, phase shape and enclosed mass relax. The full constrained Hessian,
finite displaced recoveries, law errors and mesh convergence decide that test.
The law is tested on 1.5--50 kpc only; finite total mass cannot obey it to infinity.

## Independent material support and wall-width control (BR-18--20)

The force-converged BR-17 volume-bound branch at B=.001 still has a cavity;
positive volume energy alone does not fix material support. With B=.003 the
cavity closes but the boundary is too far inward and the law error is large.
The actual successful-candidate energy adds weak ordinary material stiffness

    E_kappa=(kappa/2) integral r^2 [d sqrt(rho)/dr]^2 dr,
    kappa=(0.25 kpc/rM)^2,
    mu_kappa= -kappa Delta sqrt(rho)/(2 sqrt(rho)).

Both species receive `-d mu_kappa/dr`. The term acts in pure phases too: its
bulk-law error must be measured. This is the same ordinary material stiffness
previously found insufficient by itself. Here its role is only material
support; the B volume term supplies independent boundary restoration. It is
not claimed to be a new interaction or to vanish in the exterior.

BR-19 narrows the conversion layer at fixed leading response wall tension by
holding `ell sqrt(beta)=3 sqrt(2) kpc` and increasing beta from 2 to 4 or 8. The
beta 4 candidate has ell=2.12132034 kpc, B=.001, epsilon=.3, K=30, charge 0 and
no added constant surface stress. The response barrier/stiffness, constant
phase volume cost, particle binding, gas, baryonic gravity, self-gravity and
material stiffness all participate in the same variational solve. No law
residual is in that energy. The coefficients are feasibility parameters;
they have not been derived or fitted across galaxies.

For clarity, write Xi_x=beta C F s_x-ell^2 div(F grad x), q_x=(pi/2)sin(pi x),
and Psi(r)=integral_r^infinity [W'(u)+beta C F'(u)s+
(ell^2/2)F'(u)x'^2] ds. The full mixed-region species potentials are

    mu_T=Phi+Psi-epsilon+B(1-q)/rho+mu_kappa
         +(1-q)Xi_x/(rho q_x),
    mu_F=Phi+h_F-B q/rho+mu_kappa-q Xi_x/(rho q_x),
    h_F=(5/2)K[rho(1-q)]^(2/3),    f_i=-d mu_i/dr.

These formulas include the response-induced nonlocal matter force as well as
explicit phase forces. Endpoint divisions are not evaluated: pure-phase
variations and Hessians are taken directly from the energy. At pure T,

    g-W'(u)+mu_kappa'=0,

so the exact unmodified cold-bulk identity is only the kappa->0 limit.
The actual measured law error, rather than that limiting identity, determines
whether the finite-kappa candidate preserves the requested law accurately.
The outer reservoir remains mobile and phase-unconstrained; free does not
mean gas/gravity/material forces are removed.

The gas implementation needs an algebraic numerical repair at pure T:
`[rho(1-sin^2(pi x/2))]^(5/3)` has an AD second derivative containing
`0*infinity` at x=1. BR-16 stops on a nonfinite Hessian, not a physical result.
BR-17 onward use the equal expression
`rho^(5/3)*abs(cos(pi x/2))^(10/3)`, whose first two derivatives are finite
there. A direct energy-value equality check passes to 1e-12.

For the full finite-grid restoring force, let Z span the active fixed-mass
tangent directions, H the energy Hessian, and c=dR/dv the derivative of the
interpolated outer q=.5 crossing. Minimizing the second variation over every
other density and phase degree of freedom gives

    k_rel = [c Z (Z^T H Z)^(-1) Z^T c^T]^(-1),
    F_R = -k_rel deltaR + O(deltaR^2).

This is the actual relaxed radial local stiffness of the computed model, not
just the thin-wall estimate. It requires positive active H. Endpoint
curvatures are checked separately; small masses and phase cutoffs are stated
in the result. BR-20 additionally displaces the species distributions by
+/-1 kpc with conservative transport, then frees every mass and phase again.
These are joint relaxations, not imposed fixed-density wall scans or actual
time evolution. Global, nonspherical and dynamical stability remain unproved.
