# Independent audit of the dynamical critical-charge stiff pair

15 October 2026. Primary verdict: **proved as written within the declared
Newtonian instantaneous-electric model**. The exact Maxwell equilibrium has
positive coupled radial potential energy, and the finite-D0 model has an actual
sufficiently small compact branch with the same radial positivity property.
The proof does not establish angular stability, global nonlinear free-boundary
evolution, a healthy relativistic exterior or a physical baryonic EOS. Its
explicit exclusions are essential. This is a fresh reconstruction by a separate
agent using the same model family, not external peer review or formal proof
certification.

Audited SHA-256 values:

- PROOF.md: `1daad4bb6a6c2e4f8f058095f7bfde0e54ba0c811e3d200ddf4f1a30a3031d82`
- check_critical_stiff.py: `aada2f9c541def3420766e3a456c4be8c02b6523aeb84b02b27c131a52b1d533`
- computation_contract.json: `4907dbef076b7794f189c4b9d29022de4f551dcd1e98304010e4ab1e23ea96c7`
- run_v1/results.json: `c1dda469880a4c6756b2c8bb19fb11cee4ff6974e8d0018e4aa356ea6d367889`
- run_v1/manifest.json: `6f76bda8176cbd900761050a7885e4521a33d3da7ae22e37a9462048717fd89a`

The manifest validates against the repository inputs and outputs at these
bytes. I inspected the exact code, contract and raw result, rather than accepting
only a status summary. The mathematics below supplies the scope; its truth is
not inferred from the check count.

## Counted equations and the Maxwell base

Both species are dynamical. In the Maxwell limit the neutral baryon feels
G(Mb+Mc)/r^2, while the critical charged species feels only GMb/r^2 after its
own Coulomb repulsion cancels its own gravity. No baryon/cold gravitational
cross term cancels. With P_i=K_i rho_i^2, the specific enthalpy is 2K_i rho_i.
Inserting rho_c=f rho_b into the two hydrostatic equations requires exactly
Kc=Kb/[f(1+f)]. The remaining density equation is

    Delta rho_b +[2 pi G(1+f)/Kb] rho_b=0.

Its regular positive first lobe is the stated sin(kr)/(kr), with first zero
R0=pi/k and R0^2=pi Kb/[2G(1+f)]. Both density zeros are simple. The pressures
vanish at the free edge, and Gauss preserves the nonzero exterior charge flux.
Thus this is an actual two-fluid equilibrium; no held central source supplies
an unvaried force or missing work.

The EOS normalizations, central density and f are selected continuum inputs.
Calling b an ordinary neutral baryonic fluid specifies its charge and gravity;
it does not derive this polytrope from real baryonic microphysics.

## Full radial Hessian and the channel transformation

Let u=delta Mb and v=delta Mc, with separately conserved species masses.
The internal Hessian contributes Kb/(2pi) integral u'^2/r^2 and Kc/(2pi)
integral v'^2/r^2. Newtonian gravity contributes
-G integral (u+v)^2/r^2. Actual critical Coulomb energy contributes
+G integral v^2/r^2. Their sum is precisely equation (5), including the
remaining -2Guv term. Here Q is the full second variation; the corresponding
quadratic Taylor energy is Q/2.

For **mass** channel variables u=a+b, v=f a-(1+f)b, direct expansion gives

    A u'^2+[A/(f(1+f))]v'^2
      =(1+2f)[A a'^2/(1+f)+A b'^2/f],
    u^2+2uv=(1+2f)(a^2-b^2),
    determinant=-(1+2f) !=0.

This is a congruence of the mass quadratic form. It must not be confused with
a change of enthalpy coordinates in the equilibrium ODE. Both congruences can
be derived, but their variables are different.

Writing y=z/r and integrating the cross term gives

    integral z'^2/r^2 = integral [y'^2+2y^2/r^2],

with the endpoint term zero for the stated regular mass form domain. The
Dirichlet sine identity bounds the first term below by
(pi/L)^2 integral y^2; r^-2>=L^-2 bounds the second. Consequently the claimed
(pi^2+2)/L^2 inequality follows. One can first use smooth regular variables
with zero traces and then pass to the weighted form closure, as the proof says.
Using R0^2=pi^2 A/[G(1+f)] gives exactly the positive 2/pi^2 margin in the
attractive a channel; the independent b channel already has positive signs.

This controls all admissible **radial** mass pairs, not just a selected trial
function. Positive fluid kinetic energy supplies the radial quadratic
Hamiltonian for suitable linear solutions. It is not a theorem about angular
modes or arbitrary finite-amplitude rearrangements. The two species' vanishing
densities at their free edges justify the zero mass-perturbation traces for
regular material variations; a fixed external pressure wall is not being added.

## Finite nonlinear field: actual branch and its exterior

I reconstructed the dimensionless equations from the force law rather than
from a neutral-potential surrogate. With ell^2=Kb/(2piG), the cold equation
has factor lambda=Kb/Kc=f(1+f), and the electric argument is exactly
x=eta mc/t^2, eta=4piG rho_* ell/a0. The positive parts source physical
nonnegative densities; continued negative enthalpies are only auxiliary ODE
variables.

At the center, bounded enthalpies imply m_i=O(t^3), so division by t^2 leaves
an integrable O(t) gravitational kernel, and the nonlinear correction is
O(eta t^2). On a sufficiently short interval the integral map is locally
contractive in bounded enthalpies, uniformly for small eta. Beyond that interval
ordinary continuation away from x=1 applies. Continuous parameter dependence
and the transverse Maxwell zeros give first zeros near R0. This is a qualitative
existence argument for a small open branch, not an inference from a finite
floating integration.

Compactness also requires excluding a later cold re-entry, which the proof
correctly addresses. At the cold first zero the strict condition
mb>mc x/(1-x) holds for sufficiently small eta by continuity from the positive
Maxwell mass. Beyond it, mc is fixed, x decreases and mb cannot decrease, so
cold enthalpy stays negative. Baryonic enthalpy is always decreasing. Hence
both stocks are genuinely compact and finite, with a well-defined nonlinear
exterior field in this stipulated Newtonian model.

The cooperative z,n system is valid while both fluids are occupied. Its
positive forcing implies cold density is still positive at the baryon zero,
so Rb<Rc for eta>0. After that, mc continues increasing while mb is fixed.
Accordingly the finite-eta total mass ratio exceeds the chosen base f; it is
not exactly 5.364. The proof and raw results disclose this rather than silently
retuning an EOS coefficient.

The nonlinear electric Hessian in the radial Gauss direction is
H''=(1-x)^-2>=1. Therefore its correction to the critical Maxwell radial
Hessian is nonnegative for every admissible radial perturbation. The same
mass-channel congruence remains available at the new background because Kb,Kc
are unchanged. Extending mass variations by zero beyond each own edge to the
common outer radius L gives the bound with

    kappa_L=(1+2/pi^2) R0^2/L^2-1.

Since L tends to R0, this is positive on a sufficiently small nonlinear branch.
No explicit universal eta threshold is claimed. This supplies the requested
moving-source radial-energy result with both fluids varied.

## Computation interpretation and retained limits

The raw run has 24 exact checks, a Maxwell ODE benchmark and three finite-eta
floating illustrations. The largest displayed eta=0.01 has diagnostic
kappa_L about 0.07963 and mass ratio about 6.14377, with a strictly positive
no-reentry margin. These are implementation diagnostics, not interval proofs
of those radii, a certified field supremum or a quantified branch threshold.
The code labels its sampled maximum and numerical tolerances accordingly.

The optional radial S2 identification Kc=gamma/2 counts the gradient-density
energy once; it also requires the chosen baryonic coefficient
Kb=f(1+f)gamma/2. It does not justify adding a second copy of Kc rho_c^2 or
transferring the radial argument to every angular stiffness mode.

At the outer cold edge the charge field is nonzero while both matter densities
tend to zero. The retained RTM inertia threshold therefore fails inside the
occupied taper at finite D0. Its failure and the positive nonlinear-to-Maxwell
traction mismatch are separate from the Newtonian radial result. Neither can
be repaired by this energy bound. The stipulated global nonlinear exterior,
the selected baryonic EOS and normalizations remain physical inputs needing
identification, and no relativistic vacuum or full-theory closure follows.

All load-bearing obligations in the stated radial Newtonian theorem pass this
reconstruction. The smallest remaining physical implication is an actual
healthy matter/exterior completion for a dynamical pair, with its own common
energy and constraints; an angular or relativistic theorem is outside the
proved statement.
