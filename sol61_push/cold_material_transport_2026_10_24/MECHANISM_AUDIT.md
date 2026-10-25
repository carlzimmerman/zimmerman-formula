# Material transport, gravity bookkeeping and the finite-solver defect

This audit concerns one implication: can labels transported with eta Im(psi*grad psi)/|psi|² be identified as material subsets of the saved CCT fields? Verdict: **correct only after a stated restriction** to a sufficiently resolved local continuum evolution (or another explicitly validated conservative discretization). It is not established for the saved finite Galerkin evolutions. This correction does not change their measured field densities or restore their failed dwarf profiles.

## Local continuum versus projected angular dynamics

For a regular continuum field with a real potential,

    i eta psi_t = -(eta²/2) lap psi + Phi psi,
    rho = |psi|²,  j = eta Im(psi* grad psi),
    rho_t + div j = 0.

An amplitude absorber -i eta gamma psi adds -2 gamma rho. Where rho>0 and transport is regular, a passive fraction f with f_t+(j/rho).grad f=0 gives rho_tag=f rho. If initially0<=f<=1, it remains a positive material fraction. Consequently, in any spatial region B,

    M_tag(B) <= M_total(B).

This inequality alone does not assume a spherical galaxy or a stationary core. Nodes and weak-transport uniqueness require additional care; the recorded tracer runs encountered no declared low-density threshold events, but that does not prove global regularity.

The angular solver instead uses an orthogonal finite projection P with P psi=psi:

    i eta psi_t = K psi + P(Phi psi),
    rho_t + div j = S_P,
    S_P = (2/eta) Im[psi* P(Phi psi)].

Here K is written as the continuum differential kinetic operator only to isolate the **angular** defect. The actual radial discretization has further current errors. Pointwise Phi |psi|² is real, but its projected counterpart need not be. Hermiticity guarantees integral S_P=0 because <psi,P(Phi psi)>=<psi,Phi psi> is real; it does not guarantee S_P=0 locally. Thus a global mass ledger or good radial CDF can coexist with wrong local tagged-mass transport.

The source sign and normalization agree with an independent central finite-difference density derivative to1.18e-11 on the finite fixture. The nonzero small-basis source disappears to1.31e-15 when the product-complete angular basis is used for that fixture. This verifies the identified mechanism in the fixture, not convergence of the nonlinear galaxy runs. Saved dwarf snapshots have roughly2.7–2.9% relative angular potential residual norm. The absolute local source inside the selected core is about1.3–1.4% of core mass per code time for Draco and0.33–0.48% for Sextans at the measured endpoints. These endpoint rates are not an integrated error bound.

The nonlinear tracer benchmark uses cubic radial reconstruction and phase-aligned temporal interpolation. Uniform phase alignment does not alter rho or j. Free boosted/spreading Gaussian velocity error is2.84e-7 and trajectory error6.08e-8 in benchmark code units. These checks establish basic transport implementation correctness; they do not remove the finite-generator mismatch.

## What is sourced, and what is not

The cold field sources Phi_c once through lap Phi_c=4 pi G rho_c. Its self-energy is (1/2) integral rho_c Phi_c. The material labels are passive numerical integration points, not a particle component, new mass, additional stress source, reset mode population or an extra gravity enhancement.

The selectively coupled CCT hypothesis has a shared Newtonian field for cold and baryons plus baryon-only Xi. Stars feel the sum; cold feels the shared Newtonian field. The old source-free pre-stellar cold trajectory is replayed here and stars are passive, with the same rigid spherical baryonic Newtonian-plus-Xi background as CCT010. That approximation is disclosed; it does not close mutual stellar/cold energy or momentum exchange. No additional cold enhancement is inserted. This candidate is not derived from the literal v3s action, and is not SCT-M.

## Why the same history is difficult for Fornax and Leo I

Their larger prescribed supply makes eta/(R sqrt(G M/R)) smaller: the same incoming prescription has shorter spatial phase scales. The initial phase-gradient kinetic check rejects Fornax nr8192 at3.13% discrepancy; nr16384 gives0.79%. Leo I nr4096 gives0.77%. Resolving that radial phase does not resolve generated azimuthal modes. Low-cutoff pilots hit their m boundary, and the first larger-cutoff runs did too.

An additional implementation issue was caught before interpretation: recomputing the angular-minimum infall phase on a different angular grid changes the incoming wave. Despite only~0.78% initial energy change, phase-aligned initial-field differences were0.599/0.152 in norm for Fornax/Leo I. Those first larger-cutoff runs are retained, but are **not clean convergence controls**. `assembly_matched.py` copies the smaller run's exact initial field into the larger basis with zero new-mode amplitudes. The final control comparison must use these fixed-initial runs.

The5% edge-occupancy gate is a new exploratory resolution stop, not a physical dwarf-exclusion criterion. An early pre-stellar snapshot with a large spherical gravity diagnostic is not a late overboost exclusion; stars need not yet exist and the later wave/mass export has not been computed reliably.

## Next discriminating calculation

A material claim needs a local conservative representation with separately converged radial/angular currents, the same initial wave for convergence controls, and density-equivariant tags in the **core**, not merely globally. Then include live stars and baryonic backreaction, and carry one independently specified source inventory/energy/angular spectrum through all four dwarfs. Current source inventory, eta and incoming pulse are postulates; numerical progress does not derive them from data.

One exact reparameterization worth benchmarking before another large run is phase factoring, not a new force. Write psi=A exp(i S/eta), with real S:

    i eta A_t = -(eta²/2) lap A
                - i eta (grad S . grad A + (lap S) A/2)
                + [Phi + S_t + |grad S|²/2] A,
    rho=|A|²,
    j=rho grad S + eta Im(A*grad A).

Choosing S_t+|grad S|²/2+Phi_ref=0 leaves Phi-Phi_ref in the amplitude equation. Phi_ref is already accounted for through S; adding it again would double count. This identity is derived, **not an implemented or validated galaxy solver**. It may reduce the radial cost of an incoming phase but does not by itself handle later counterstreaming, caustics or fast nonspherical structure. Before use: analytic boosted/spreading packets, self-gravitating translation/recoil, phase rebasing, mass/current/energy consistency, and comparison to a resolved original formulation.
