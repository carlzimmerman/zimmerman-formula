# Instability gated transport contract

This is a distinct closure, introduced after persistent thermal conduction
gave continuing central contraction and entropy loss in the core through t=16.
Damping-only suppresses radial breathing but retains adverse entropy ordering.
Neither result is labeled stable settling.

Use the same material energy, compression heater and signed bulk damping.
For outward neighboring cells define chi=K/Kstar, center separation delta_r,
psi=chi (W/rho_q)^(3/2), and

\[
 z=\frac{\ell_g[(\chi_i-\chi_j)/\Delta r]_+}
 {\chi_g+(\chi_i+\chi_j)/2},\qquad a=\frac z{1+z},
\]
\[
 L_{ij}=P_0D\frac{4\pi r_{ij}^2}{\Delta r}
 h_i h_j a[\psi_i-\psi_j]_+ .
\]

This is an outward heat-transport hypothesis, not resolved parcel convection.
The same shared luminosity enters the two energy equations with opposite
signs. Heat travels only from hotter to colder material, so entropy production
is nonnegative. A dormant neighbor blocks the face exactly. Stable outward
entropy ordering turns transport off, allowing nonisothermal endpoints.

The gate uses a gradient times fixed physical length ell_g, not a raw
mesh-dependent difference. Declare D=0.1, damping strength=1,
chi_d=chi_g=0.01, ell_g=0.1, tau=0.5 before the first run. The initial sphere
and other units match TARGET.md. No coefficients change with shell count.

At fixed valid geometry each face flux is monotone in supplying K and antitone
in receiving K. At a global minimum K, rightward outflow is zero and leftward
inflow is nonnegative. Together with the nonnegative heaters this is a
minimum principle for the full material domain. It preserves an existing
positive global floor; it does not itself supply one from K=0, or justify a
floor in an expanding active component receiving unheated material.

## Finite experiment

Begin N32/N64 through t=8. If late drift/settling improves, extend both to
t=32 and compare N128/N256 at matched times. Require late kinetic/binding
ratio <1e-3, 5% density peak-to-peak and secular change <2%, and hydrostatic
force residual <2% of gravity. The last requirement explicitly excludes
quasistatic viscous creep with tiny kinetic energy. Verify energy error <1e-6
or convergence with tighter time integration. Record entropy, late central
minima, 1/5/10% densities and mesh dependence independently.

Finite positive K is not a continuum theorem. A physical bound must be
supported by an invariant or a mesh-uniform heating/transport estimate, not
post-run clipping, sorting, coefficient scaling, or an inserted floor.
