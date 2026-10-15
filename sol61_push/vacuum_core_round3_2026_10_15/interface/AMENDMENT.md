# Match the radial inertia to the varied barotropic current action

VC3-INTERFACE-001, 15 October 2026. This supplements the frozen proof and
supersedes its inertia convention when the interface control is embedded in
the inherited relativistic barotropic current action. The static equilibrium,
wall equation, potential-energy form Q and strict bound C>39/5000 do not change.

The frozen proof uses Newtonian fluid kinetic density rho in equations (10),
(13) and (17), but its final local principal-gate paragraph uses the full
current-action enthalpy. These conventions should not be combined silently.
For the full current-action hybrid, with Newtonian gravity coupled to lab
rest density as in the earlier joint audit, the quadratic material kinetic
density is

\[
 H_m/c^2=\rho+6P/c^2,\qquad H_m=\rho c^2+6P.
\]

The proper density decreases by rho*v^2/(2c^2) at fixed lab current density;
expanding -epsilon consequently gives `H_m*v^2/(2c^2)`. The unchanged
compression coefficient is `Gamma*P`, and the gravitational force remains
the explicitly postulated rest-density force. Thus replace the left-hand
side of proof equation (10) by `(rho+6P/c^2)*ddot xi`. The potential form
(12), interface condition (11), wall inertia and all static equations remain
as written. The correct full-current radial inertia is

\[
 I/(4\pi)=\int_0^R(\rho+6P/c^2)\xi^2r^2dr
                    +\sigma R^2\xi(R)^2/c^2,
\]

and equation (17) becomes

\[
 I/(4\pi)\le[(\rho_0+6P_0/c^2)R^2/6
                          +\sigma R/(3c^2)]J.
\]

For the assigned example this gives the exact strict Rayleigh lower bound
`(39/5000)/[(1+6/100)/6+(51/10000)/3]>43/1000`. The v1 check's stronger
`46/1000` bound applies only to its Newtonian rho-inertia convention; it is
not a bound for the full current-action hybrid.

With this correction the inherited local principal paragraph is consistent:
`s_rel^2=Gamma*P/(rho*c^2+6P)` and
`H_m*(1-s_rel^2)=rho*c^2+24P/5`. Radial velocity is parallel to E, so the
constitutive boost still adds no radial kinetic correction. A purely
Newtonian alternative is also a definable model, but then its effective
inertia for the principal pencil would instead be `rho*c^2-Gamma*P`.

The authoritative updated exact checker is `check_interface_v2.py`, with
`computation_contract_v2.json` and `run_v2/`. The frozen v1 record is retained
as historical evidence for its narrower kinetic convention. No full Einstein
metric or relativistic wall-gravity junction is inferred from this correction.
