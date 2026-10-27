# Actual halo feedback bound and the remaining general case

19 October 2026. Checkpoint ZAR-2026-10-19-10-CX. **The full linear work bound is established for a nonempty, explicitly chosen small-mass subfamily of the actual two-species warm halo. The general fixed-halo bound remains open.** Nonlinear work and all-time confinement are not proved by this checkpoint.

## The actual model result

The [combined proof](ACTUAL_SUBFAMILY_BOUND.md) retains the original reciprocal force law, both gravitating populations, the exact smooth density construction and one fixed positive warmth. Choose

    rM=sqrt(G Mb/a0),  ell=epsilon rM,
    (r0,r1,r2,R)=ell(1,2,3,4),  f=epsilon^2.

For all sufficiently small positive epsilon, every smooth compact fixed-L canonical generator satisfies

    sup_{t>=0,theta0,i,q in CLOSED occupied actions} |W_i(t;theta0,q)|
       <= C_delta (G Mb/ell) epsilon ||g_hat0||C12.

The work uses the full self-consistent linear field on equilibrium receiving paths. The bound includes the circular line and flat energy cap. The constant is uniform in time and in the stated family after nondimensionalization; it can depend on the fixed warmth. The generator normalization and physical potential unit are explicit in the proof.

The decisive step is an actual boundary-operator estimate, not the earlier comparison model. In dimensionless units, the exact susceptibility is O(epsilon), while the frequency remains transverse on a fixed action box. The physical shell harmonics and a fixed-amplitude coarea substitution give

    sup_{0<=Im z<=1} ||K(z)|| + [K]C^(1/8) <= C_delta epsilon.

The boundary inverse then exists by a convergent Neumann series, with norm at most two. Smooth source estimates and a summable receiving-harmonic bound give uniform work. No embedded-mode or threshold exclusion is left as an assumed leaf in this restricted theorem.

The [geometry and exact-DF scaling](GEOMETRY_AND_SCALING.md) and [operator/source proof](SPECTRAL_OPERATOR.md) provide the raw arguments. The combined proof adds two necessary details: frequency transversality on the whole integration box, and a separate O(epsilon) zero-harmonic field estimate. The [independent bound audit](BOUND_AUDIT.md) reviews the combined theorem and its precise scope.

**Scope matters:** the law annulus in this construction is baryon dominated and lies below rM; total cold mass is O(epsilon Mb). This establishes actual members of the existing mathematical family, not the arbitrary halo with cold mass of order Mb or larger. The deep-cubic source and inner-core restrictions remain satisfied. No selected galactic profile has been silently replaced in a claimed general theorem.

## Progress on the nonperturbative feedback route

For a general halo the actual field interaction is indefinite, so the comparison model's positive rank-one proof cannot simply be imported. The [critical receiver analysis](CRITICAL_RECEIVER_CANCELLATION.md) derives an optical identity from the actual reciprocal kernels and replaces finite-part-dependent scalar assumptions by an invariant bordered operator.

A further conditional result removes one unnecessary hurdle: when the complete regular inverse exists but the dressed critical scalar is zero, reciprocity forces the logarithmic field coefficient to vanish at the resonant receiving traces. The coefficient approaches zero fast enough to dominate the shifted work kernel's logarithmic growth. Thus the local receiving work remains uniformly bounded on the stated compact eccentric, positive-weight receiver charts. A bounded full-field norm is a stronger demand. The [critical work audit](CRITICAL_AUDIT.md) gives the checked hypotheses and any restrictions.

This local theorem does not establish the complete regular inverse for an order-one-mass halo, does not sum the whole frequency/harmonic range, and does not include isolated flat-cap or circular receiver extensions. Those remain separate obligations. The bordered algebra also passes review, but its proposed optical interpretation when the regular operator itself is singular needs a separate boundary-pairing argument; the Section 6 local theorem assumes that regular operator is invertible and does not use that extension.

## A boundary condition that cannot be skipped

The [spectral proof](SPECTRAL_OPERATOR.md), section 5, establishes for every closed-set receiver and smooth canonical datum

    lim_{t->infinity} W_k(t;q)/t
       = -i omega psi[P_omega h0]_k(q),  omega=k Omega(q).

Consequently an actual eigenmode with a nonzero resonant trace at an eccentric flat cap would obstruct a uniform bound for all smooth compact canonical data. Interior trace cancellation does not automatically extend to a level set touching only a flat boundary. This identifies a gap in the broader closed-set interpretation of the parent checkpoint's A5(c); it does not construct such a mode or refute the model. The new small-mass theorem avoids the issue by proving the full boundary inverse directly.

## Continuation

The next general-halo task is to discharge the regular or projected inverse in the actual critical-frequency decomposition without a small-susceptibility assumption. The optical and bordered identities state the exact finite-part-invariant problem. A [further bounded pencil analysis](SINGULAR_PENCIL_AND_MODES.md) proves the abstract classification and exact modal work criterion: at a Morse resonance the field coefficient must be bounded by a constant times the quadratic frequency detuning. Energy integrability alone does not supply that rate. Its actual source-duality reduction remains conditional, and this followup has coordinator self-review rather than a fresh independent audit. If a threshold kernel remains, its receiving divisibility must be established before projecting it away. Larger source mass cannot be substituted into the proved Neumann estimate.

For nonlinear confinement, even a general linear work theorem would still need estimates along the actual perturbed paths and control of the nonlinear label-gradient term. No future work bound, invariant narrow source band, or hidden stationary substitute has been assumed here.

All calculations in this checkpoint are analytic. No scientific program, numerical integration, simulation, scientific array analysis or process operation was run. New proofs and provenance are contained in this directory; previous proofs, ledgers, sealed records and other researchers' work were left untouched. `TARGET.json` fixes the requested bound; `CHECKPOINT.json` records reviewed claims and remaining gaps, and `PACKET_SHA256.json` pins the delivered artifacts.
