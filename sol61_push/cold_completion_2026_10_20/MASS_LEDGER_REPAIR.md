# A conservative repair to specify before regrading settling

20 October 2026. Analytic continuation to the **provisional** CFG932 arrival
audit, not an edit of its frozen criteria, script, output or class.

The no-crossing condition has two physically different meanings. If
M_p(r)-M_s(r)<=0 everywhere, there is no positive cumulative central surplus
in that region. If M_p(r)-M_s(r)>0 everywhere, there is surplus but no
equal-mass outer boundary. Both cannot be assigned the same zero-cost
interpretation. The present source's `Rx=None` branch does so in five flagged
rows; the arrival audit records the exact cases and bytes.

For an energy-per-unit-mass function e_law(r), the identity is

    integral_0^R e_law d(M_s-M_p)
      = e_law(R)[M_s(R)-M_p(R)]
          - integral_0^R [M_s-M_p] e_law'(r) dr,

assuming the central boundary term vanishes. The boundary term may be dropped
at an equal-mass crossing. It cannot be dropped merely because a crossing
was not found. Changing e_law by a constant changes an unmatched comparison
by that constant times the missing mass; the destination's energy must supply
the corresponding term in a closed ledger.

## Three explicit continuations

1. Keep all the declared cold mass and find an actual inside-out fill radius
   beyond the old clipped radius, if the physical catchment/boundary permits it.
   Recompute the exterior field, escape and energy; an extended radius is a
   changed model input, not the old endpoint.
2. Put the residual mass into a specified bound outer receiver or outgoing
   population and include its mass, kinetic, potential, charge and J. The
   interior law profile can remain a proposed target, but the outer material
   is not zero mass or zero energy.
3. Keep the current boundary/profile and label the declared mass-conserving
   endpoint infeasible/undefined. Do not convert an uncosted rearrangement
   into eps_req=0 and use it as evidence for an empty physical window.

These are alternatives to be investigated and disclosed, not permission to
choose the one that yields a favorable efficiency window. No class is regraded
here. A receiver construction must be tested under the same criterion or a
clearly declared new one.

## Explicit boundary-shell accounting option

The flagged source actually writes M_s(r>R)=M_cat after clipping R=r_ta,
while M_s(R)=M_ph(R)<M_cat. Interpreted literally, the cumulative profile has
a jump Delta M=M_cat-M_ph(R) just outside R. Its smooth derivative omits the
associated surface density. One possible mathematical completion is a thin
spherical shell; it is a new, explicit receiver assumption.

For a fixed spherical interior with total baryon-plus-cold mass M_in and
Newtonian gravitational energy W_in, a shell of mass Delta M at R adds

    W_cross = -G M_in Delta M/R,
    W_self  = -G (Delta M)^2/(2R),
    W_total = W_in + W_cross + W_self.

The self term follows by integrating -G M dM/R while building the shell,
not by treating its entire mass as a point particle in its own field. A
shell's constant interior potential also contributes to the interior-shell
interaction even though its interior force vanishes.

If one additionally constructs a uniform ensemble on circular tangent orbits
and uses the mean self-field of the shell, the required kinetic energy is

    K_shell = G M_in Delta M/(2R) + G (Delta M)^2/(4R),
    E_shell,orb = K_shell + W_cross + W_self
                = -G M_in Delta M/(2R) - G (Delta M)^2/(4R).

This is a conditional endpoint ledger, not a proof that an infinitesimal shell
is stable or can form. Arbitrary radial outflow has a different K and need
not obey this virial/circular formula. The radius and velocity distribution
must also provide the required angular momentum; for a nonrelativistic
orbital receiver, J<=R sqrt(2 Delta M K_shell) is only a capacity bound.

Thus there is a concrete way to include the omitted mass and energy, but it
requires a real receiver and a revised calculation. The same microphysics
must determine how the mass reaches it, which binding/feedback reservoir
pays for the trajectory, whether it returns, and how stars respond. None of
these formulas closes the separate Sextans stock/profile problem or the
Draco/Sextans versus Fornax/LeoI formation selection.
