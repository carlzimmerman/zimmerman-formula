# Selective confinement requires an interaction not yet supplied

2026-10-13. This examines the construction requirement left by the outgoing-transport calculation. The preceding goal turn made progress by correcting the escape threshold. A nonreflecting boundary was still an assumption; this turn asks what could hold the background at that boundary.

Two results follow: the existing repulsive untrapped carrier does not admit the subthreshold stationary localized state needed for self-confinement; an explicitly added external well has a nonempty **necessary** energy window for binding the background while allowing the produced excitations to escape. The well is not derived from the repo's action, so this is a specification of the missing physics, not a completed device.

## What the current carrier action permits

The copied action excerpt defines delta>0 and kappa>c3²/delta. For regular finite-energy standing waves psi(x,t)=exp(-i mu t)phi(x), b(x,t)=exp(-2i mu t)B(x), with no gravity, external trap or time-dependent drive,

\[
\mu\phi=-\frac{\nabla^2\phi}{2m}+2\kappa|\phi|^2\phi+2c_3B\phi^*,
\]
\[
A_\mu B=-c_3\phi^2,\qquad
A_\mu=-\frac{\nabla^2}{2M}+\delta-2\mu.
\]

For mu≤0, A_mu is positive and its inverse has operator norm at most 1/(delta-2mu). Multiplying the first equation by phi* and integrating yields

\[
\mu N_\phi=T_\phi+2\kappa U_4
-2c_3^2\langle\phi^2,A_\mu^{-1}\phi^2\rangle
\ge T_\phi+2\left[\kappa-\frac{c_3^2}{\delta-2\mu}\right]U_4>0
\]

for nonzero phi. But mu N_phi≤0, a contradiction. This uses finite quartic norm, nonnegative kinetic energy and boundary decay sufficient for integration by parts. A source-only localized stationary state also cannot be supported by the free positive operator in this subthreshold range.

Thus there is no nonzero stationary, exponentially localized subthreshold lump in this isolated repulsive model. This is not a claim about every transient, a periodically driven state, embedded exceptional states at positive chemical potential, or a gravitationally bound configuration. The existing positive energy bound alone would not have established all those stronger statements.

A static classical electromagnetic field in the proposed portal changes the source–pair coupling c3. At tree level, it does not insert an independent one-body term U(x)|psi|². If that changed coupling remains bounded by c_max and kappa>c_max²/delta, the same inverse-operator estimate still excludes a subthreshold localized state. Driving the coupling beyond that bound is not evidence for a stable droplet; the effective quartic can become attractive and stability must be reanalyzed. Time-dependent and loop-induced trapping effects are not excluded or derived here.

## Explicitly added well: what it would have to do

For a conditional interface model, add an external charge-proportional potential U(x)(|psi|²+2|b|²), and eliminate the weakly mixed source at leading order. This is a new assumed external term, **not a term shown to exist in the original action**. Set kappa_eff=kappa-c3²/delta and define the bulk interaction chemical potential

\[
\mu_{\rm int}=2\kappa_{\rm eff}n.
\]

Take U=-V0 inside and U=0 outside. The global chemical potential is mu_global=mu_int-V0. The background can decay into the empty exterior only if V0>mu_int. A produced quasiparticle of energy E, measured relative to the condensate chemical potential, has exterior particle kinetic energy E+mu_global. An energetically open exterior channel therefore requires

\[
\boxed{\mu_{\rm int}<V_0<\mu_{\rm int}+E.}
\]

This is a necessary window; it does not prove negligible reflection or stable nonlinear transport. At the previous m=1 MeV, delta=5 eV, lambda_tot=10⁻⁶, epsilon=10⁻⁴ and x=2/7 benchmark, mu_int≈0.714214 eV and E≈1.785934 eV. Thus

\[
0.714214\ \mathrm{eV}<V_0<2.500149\ \mathrm{eV}.
\]

The source-eliminated chemical potential is a leading weak-mixing approximation, distinct from the exact homogeneous two-field value in earlier reports. A full two-field wall must replace it before precision matching.

## An analytic background interface exists for that imposed well

Let xi=(2m mu_int)^(-1/2), measure position in xi, and write psi=sqrt(n)y. Put beta=V0/mu_int-1>0. The static one-field equations are

\[
-y''-y+y^3=0\quad(x<0),\qquad
-y''+\beta y+y^3=0\quad(x>0).
\]

A positive profile tending to one inside and zero outside is

\[
y_{\rm in}=\tanh[(x_0-x)/\sqrt2],\qquad
y_{\rm out}=\sqrt{2\beta}\,\operatorname{csch}[\sqrt\beta(x+x_1)].
\]

Continuity of y and y' at the interface fixes

\[
y(0)^2=\frac1{2(1+\beta)}=\frac{\mu_{\rm int}}{2V_0},
\quad x_0=\sqrt2\operatorname{arctanh}y(0),
\quad x_1=\frac{\operatorname{arsinh}(\sqrt{2\beta}/y(0))}{\sqrt\beta}.
\]

The profile equations and slope matching are checked symbolically and numerically. The physical healing length is about 1.65×10⁻¹⁰ m, so a millimeter-scale sample has a locally planar wall in this approximation.

| Assumed V0 | Exterior condensate chemical potential | Escaping particle kinetic energy | Exterior decay length |
|---:|---:|---:|---:|
| 1 eV | -0.286 eV | 1.500 eV | 0.261 nm |
| 1.5 eV | -0.786 eV | 1.000 eV | 0.157 nm |
| 2 eV | -1.286 eV | 0.500 eV | 0.123 nm |

An open kinetic-energy channel does not imply a perfectly transmitting interface. The actual Bogoliubov scattering problem on this profile is still required before importing the outgoing-boundary gain threshold. The condensate itself is assumed to have been assembled; this solution does not calculate assembly.

## Gravity comparison and physical status

A potential depth of 1 eV for a 1 MeV particle corresponds to |Phi|/c²≈10⁻⁶. The elementary GM/R comparison at R=5 mm requires approximately **6.73×10¹⁸ kg**. This is not a proposed shell, an equilibrium structure or a practical trapping source; it illustrates why ordinary gravity does not automatically provide the stipulated millimeter well. The shell or other gravitating structure would itself require a consistent stress-energy and equilibrium model.

The carrier and proposed photon portal have therefore not yet supplied selective confinement. The conditional well model shows the required depth is compatible with energetic escape and provides a concrete profile on which to test reflection. It does not justify silently adding that potential to claim the original theory is complete.

## Evidence and next decision

Twenty-seven finite coefficient checks supplement the general positivity argument. Three symbolic identities and three wall-depth cases check the interface algebra and physical conversions. The bounded-run contract pins the actual action excerpt and script.

Three Lean statements certify positive effective coupling under the stated inequalities, contradiction from the abstract stationary energy inequality, and a nonempty midpoint inside the necessary well-depth interval. They do not formalize the inverse-operator estimate, functional spaces, PDE reduction, scattering or physical implementation. Compiler logs and hashes preserve this exact scope.

The next useful test is interface transmission on the explicit profile, while keeping the missing microscopic trap interaction visible. If reflection prevents the necessary escape, the current well specification needs revision; if it transmits, an actual term producing U remains a separate unmet requirement. The overall cold-energy objective remains unverified.
