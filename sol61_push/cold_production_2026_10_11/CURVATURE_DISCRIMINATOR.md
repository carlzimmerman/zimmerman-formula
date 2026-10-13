# A dust curvature discriminator and why halo stress matters

Status: exact algebraic reconstruction on Einstein backgrounds. A curvature
combination cancels pressureless matter, but it does not isolate vacuum
energy for the pressured, possibly anisotropic cold medium being produced.
No new interacting action or halo-selection mechanism is established.

## Constructing and testing the candidate

Use metric signature -+++ and Einstein equation

    G_ab+Lambda g_ab=k_E T_ab,    k_E=8 pi G/c^4.

For an ordinary perfect fluid let epsilon be energy density and p its
isotropic pressure, excluding Lambda. Define the traceless Ricci tensor
S_ab=R_ab-R g_ab/4. The trace equation and contraction give

    R=4Lambda+k_E(epsilon-3p),
    S_ab S^ab=(3/4) k_E^2 (epsilon+p)^2.

For epsilon+p>=0, the scalar

    L_dust=(1/4)[R-sqrt((4/3) S_ab S^ab)]

therefore equals

    L_dust=Lambda-k_E p.

It equals Lambda exactly for pressureless dust of any positive density.
This does improve on a simple Ricci-scalar portal, whose matter-density
contribution dominated the vacuum contribution in the earlier audit.
However, the residual is the actual pressure, not zero merely because
p/epsilon is small. Relative to vacuum curvature, the error is

    (Lambda-L_dust)/Lambda=p/(rho_Lambda c^2).

For the declared Plummer kinetic equilibrium,

    p(r)=rho0 sigma0^2 (1+r^2/b^2)^(-3).

With rho0=1e-21 kg/m^3, sigma0=200 km/s, and the illustrative
rho_Lambda=6e-27 kg/m^3, the relative bias is 0.0741767 at the center and
0.00927208 at r=b. Thus the putative vacuum indicator varies spatially
even though Lambda is constant. These numbers describe the initial test
halo; baryonic pressure, a different halo or a changed reaction state would
change them. They are not bounds for the universe.

A radiation component has p=epsilon/3, so the indicator can even become
negative when its pressure exceeds vacuum energy density. Taking its square
root to define a universal acceleration would then require another rule.
An exact dust identity cannot be silently carried through the earlier
radiation-era production calculation.

## Anisotropic stress adds another contribution

For a type-I stress tensor with rest-frame principal pressures p1,p2,p3,
write pbar=(p1+p2+p3)/3 and D=sum_i (pi-pbar)^2. Direct contraction gives

    (4/3) S_ab S^ab=k_E^2[(epsilon+pbar)^2+(4/3)D],
    L_dust=Lambda+(k_E/4)[epsilon-3pbar
                         -sqrt((epsilon+pbar)^2+(4/3)D)].

When epsilon+pbar>=0, anisotropy lowers L_dust further relative to
Lambda-k_E pbar. The multimode medium's stress tensor is therefore needed;
a dust or isotropic replacement can discard precisely the information
that contaminates this candidate vacuum response. These formulas assume
a rest frame with diagonal type-I stress, not arbitrary energy flux tensors.

## What geometry alone cannot identify without a matter assumption

The Einstein equation is invariant under the simultaneous constant shift

    Lambda -> Lambda+delta,
    T_ab -> T_ab+(delta/k_E) g_ab.

For a perfect fluid this means epsilon -> epsilon-delta/k_E and
p -> p+delta/k_E. The same metric and every curvature invariant remain
unchanged, while the division between the named cosmological term and
matter's vacuum-like stress changes. Small shifts can preserve positive
energy density and enthalpy. A matter equation of state or a microscopic
action can fix the division; unrestricted local curvature data cannot.

This is not a theorem that a specified matter theory can never determine
Lambda. It shows why the exact dust cancellation relied on p=0 and why
removing that assumption requires additional physical input. The full
massive-field model already specifies stress through its action, so a
consistent calculation could use that information. Doing so must be
derived explicitly rather than identifying L_dust with Lambda by definition.

## An invariant is not yet an acceptable interaction

At S_ab=0 the square-root term is not differentiable in all tensor
directions. Along a traceless perfect-fluid direction S_ab=t A_ab with
(4/3) A_ab A^ab=1, it becomes |t|. The left and right derivatives at zero
differ. A one-sided positive-density restriction does not supply the
unrestricted metric variation required to define a smooth local action.

Away from that point, dependence on nonlinear Ricci invariants also
requires an explicit metric variation and constraint analysis. One cannot
import the former positive-square energy proof, or assume second-order
metric equations, after inserting this expression into the mass gap.
No ghost, cutoff or stability conclusion has been established here.

## Evidence and next research requirement

curvature_discriminator.py constructs mixed Ricci components from exact
rational stress tensors and checks the trace, invariant, anisotropic and
vacuum-split identities. It also evaluates the illustrative pressure bias.
All 41 checks pass; the manifest validates the saved inputs and outputs.
The general identities are derived above, not inferred from finite samples.
The derivation and interpretation are self-reviewed.

A limited literature search found related Ricci-based characterization of
perfect-fluid geometries in Ferrando and Saez, arXiv:1701.05023v1
(https://arxiv.org/abs/1701.05023). Only its abstract was inspected for
context; no theorem or novelty claim is imported from it. The equations
used here follow directly from the declared Einstein equation.

The previous turn quantified the simple Ricci portal's density contamination.
This turn improves that route to exact dust cancellation and identifies its
pressure, anisotropy and variational limits. A successful selector still
needs a specified dynamical coupling, a well-defined vacuum/matter split,
and a derivation of the requested halo response. The cold-energy goal
remains active and incomplete.
