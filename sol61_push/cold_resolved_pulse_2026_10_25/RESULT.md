# CCT016: redistribution survives checks; core cooling is not demonstrated

The most useful new result is a sign test, not a completed mechanism. In the conditional Draco wave trial, central mass and angular momentum leave, but the central canonical energy rises. The outgoing mass pulse therefore cannot be presented as demonstrated core cooling. This is a finite finding for this incoming-field/assembly family, not a no-go for all cold fields.

## Measured pulse

| Interval / grid | Central aperture mass at end | Energy / spin accuracy | Interpretation |
|---|---:|---|---|
| Original joint ne256 nt40 nf64, T0→20 | 22.04 million Msun nodal; 21.99 million weak inventory | E drift9.17e-6; J drift−2.633%; polar tail3.046% | Late endpoint fails physical acceptance |
| Conditional nt48 nf80, T14.74→17.30 | 41.24 million nodal; 41.15 million weak | E drift2.05e-5; J drift−.0412%; polar tail.522% | Clean saved wave, still evolving |
| Same conditional48x80 continuation toT19.74 | 23.32 million nodal | J drift−.2386%; polar tail1.0022% | STOP; failed1% polar gate, never resumed |
| Conditional nt56 nf64, T14.74→17.58 | 37.86 million nodal | J drift−1.0067%; polar tail.1863% | STOP; failed1% spin gate, never resumed |

The conditional Draco target from the prior fit is11.615 million Msun inside the reference radius. Aperture mass is not retained bound material, a material core, or a stellar survival result. Even the numerically clean interval has not settled to that target. Both angular refinements begin from the actual clean nt40 nf64 s05 wave atT14.74, not the inaccurate T20 state. They preserve the complex angular field, radial mass, total mass, Jz and radial kinetic energy to roundoff; no normalization or fitted core is inserted. The angular kinetic/W discretization jumps are reported and <1% of K+|W|. The reference is reset locally: these are conditional late pulses, not corrected formation histories.

The48x80 and56x64 aperture masses agree to1.08e-8 relative at64 common sample times throughT17.26. They change both angular directions, so this is a cross-check, not monotone convergence. Their divergent total-spin errors expose the need for BOTH polar and azimuth bandwidth before a late transport claim.

## Energy sign and timestep discrimination

For48x80 T14.74→17.30, integrated outward canonical energy through r=1 is−0.00352814 code units; core canonical energy increases+0.00356939. Closure residual/transport is1.169%. The longer failed interval has the same sign. Positive outgoing energy occurs at larger radii, but this does not reverse the measured core-boundary sign or establish energy/spin escape to infinity.

Two separate short pulses from the clean T17.30 saved wave toT17.50 keep changed timesteps out of the cumulative history:

| dt | Core outward energy | Core energy change | Global E error |
|---|---:|---:|---:|
| .04 | −1.12137e-4 | +1.08205e-4 | 1.10017e-6 |
| .02 | −1.10267e-4 | +1.08312e-4 | 7.04675e-8 |

Final complex waves differ by1.20315e-4 relative L2. The global energy defect falls15.6-fold, and the core-energy sign is unchanged. The integrated core luminosity changes1.70%; the finer core shell residual is1.77% of transported energy. This supports the sign discrimination, not percent-level capacity closure. Outer shell residuals remain much worse at some radii; neither global conservation nor a kinetic interface identity certifies the full physical luminosity. See pulse_summary.json and the raw states/history.

The outer stock also remains unresolved. At the cleanT17.30 checkpoint, about1.042 billion Msun remains inside r=8 (1545.76pc), about32.4 times the PRIOR CONDITIONAL Plummer mass at that radius. Moving central mass into this envelope has not disposed of the excess supply. This is a fitted-reference comparison, not a new survey likelihood or an observational upper bound; stock_check.py/json pins the calculation. It prevents treating a nearly target central aperture as a complete dwarf mass budget.

## Why this advances the mechanism

MECHANISM.md gives the conditional action, wave/Poisson equations, Madelung stress and conserved energy/spin currents. There is one cold gravitational source and half global self-energy. Collapse can redistribute energy and angular momentum without particle collisions. What matters is whether a bound low-spin core remains while a supported envelope and outgoing waves receive the appropriate energy and spin. The measured pulse shows redistribution; it does not yet establish that required outcome.

INVENTORY_AND_SUPPORT.md derives the corrected mapped-SEM shell inventory and the conditional Plummer support requirement. Element-local weak derivatives and mapped LGL integration reproduce global K/W to roundoff; old trapezoidal/averaged-gradient inventories can misstate shell residuals. The old frozen outputs are preserved, with new interpretations explicitly separate. A smooth stationary phase-only envelope is too restrictive; time-dependent/granular wave support remains possible. The Sextans17.70km/s phase-support bound applies only to an EXACT smooth Plummer wave density, not an averaged granular profile.

The observed coarse T20 field is expanding (discrete I_dot positive) and fails angular acceptance. Do not call it a stationary halo. No new Sextans, Fornax, Leo I or evolved-star simulation is claimed. The old same-supply control-family overboost remains unresolved. No result here establishes that cold energy is fundamentally nonparticle or bridges this conditional wave action to the owner's current theory.

## Checks, resources and retained failures

Nine finite control programs were freshly executed under audit_controls_001: baseline equivalence, analytic free-wave/current refinement, amplitude/phase partition, checkpoint mutations, Gauss dense-Pade/interface/order tests, fast-flux equivalence, Poisson equivalence, memory-kernel/inventory equivalence and smooth-profile support integrals. Independent review also tested a nonconstant carrier and checked the written action/current signs. See REVIEW.md.

Twenty outside-runner producer records retain exact source/input hashes before/after, argv, revisions, software, raw states, wall time and measured RSS. Process completion is separate from physical acceptance. Soft resource gates are not hard allocation certificates. Every measured experiment stayed below1GB; accepted production headroom remained750MB. The48x96 preflight failures, initial roundoff-limited Gauss ratio failure and superseded phase-only labels remain in FAILED_PREFLIGHTS.md and their original files. No frozen criteria, prior results or publication was changed.

The summary's initial metadata omitted direct hashes for the two raw wave files used in its L2 comparison. pulse_summary_initial.* preserves that first record; the current summary adds those raw-state/source pins without changing the calculations.

NEXT.md gives reproduction and the next discriminating obligations. The theory and the four-dwarf mechanism remain open.
