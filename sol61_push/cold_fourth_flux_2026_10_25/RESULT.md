# CCT015 — collisionless collapse now tested; four-dwarf mechanism remains open

The conditional coherent-field equations can concentrate cold mass and transfer energy to an envelope without binary collisions. The tested common incoming/supply family does not yet produce the required selective, low-spin remnants. The important new result is resolved early concentration plus measurable INNER energy exchange, not a completed cooling/escape mechanism.

## Actual finite-time result

All masses below are cold mass in the 3D sphere r=the adopted projected stellar half-light radius, interpolated from the saved cumulative field density. They are not material-tag masses or separately counted gravitational mass. The comparison profiles are the prior CONDITIONAL models in cold_survey_capture_2026_10_24; these are not data-imposed total-mass floors.

| Galaxy | State | Cold sphere mass | Conditional reference | Reading |
|---|---|---:|---:|---|
| Draco | T8, ne256 dt.01, nt24 nf32 | 202.82 million Msun | 11.62 million | 17.46x, early excess |
| Sextans | T8, ne128 nt32 nf64 | 185.43 million Msun | 8.62 million | 21.50x, early excess; full spin/escape not converged |
| Fornax | INCOMING T0, before any evolution | 184.55 million Msun | 17.48 million | 10.56x initial-profile tension |
| Leo I | INCOMING T0, before any evolution | 34.04 million Msun | 6.74 million | 5.05x initial-profile tension |

Draco's T8 sphere mass differs0.405% between ne128/.02 and ne256/.01 using interpolated CDF (sharp-node sphere mass differs0.38%). Enlarging the angular grid from nt24/nf32 to nt32/nf64 at ne128 changes the T8 CDF by less1e-5 of initial inventory. Sextans's T8 sphere mass is185.095 million on the ne256 nt32 nf32 check, versus185.429 million on ne128 nt32 nf64 (0.18% difference), but that fine Sextans case already has1.11% Jz drift atT8, above1% acceptance. This supports an early mass mismatch, not full angular-momentum accuracy or final remnant convergence. The ne128 Sextans angular CDF comparison differs3.04e-5 inventory; its nt24 T8 ell-tail1.24% fails acceptance, while nt32/nf64 tail0.1104% passes that diagnostic.

The instantaneous spherical Plummer virial SCREEN predicts global equilibrium LOS dispersions of about40.64km/s for Draco T8 and24.17 for Sextans T8, compared with archived reference dispersions9.55 and7.9. Incoming Fornax/Leo screens are37.43/27.75, versus reference12.1/9.29. This is an input/profile tension under the screen assumptions, NOT an evolved stellar-heating result, full distribution-function test, survey-matched likelihood, anisotropy fit or final exclusion. Baryon-only Xi and Newtonian cold gravity enter once each. No stars were dynamically evolved in these new collapse runs.

The shared supply hypothesis needs total cold retention fractions D .03148, S .46736, F .001414, Leo .002955 to reach the old conditional total-profile masses. Sextans needs roughly330 times Fornax's retained fraction. No universal rule generating that difference has been derived here. In particular, forcing a common large incoming reservoir into each galaxy already over-supports the initial Fornax/Leo tracers under this screen.

## Energy transfer is not yet escaping cooling plus spin loss

See MECHANISM.md for the actual equations and conserved currents. In Draco's fine T0..8 run, the signed canonical energy through r=2Rstar is +.0616473 code units and through4Rstar +.0334968. Corresponding boundary-corrected energy-budget residuals are5.24e-5 and1.63e-4 (0.085% and0.486% of transported energy). The ne128 integrals are.0611427/.0335156: the inner-envelope energy exchange has a useful matched refinement check.

At those SAME surfaces the integrated outward Jz is NEGATIVE: -.0180742/-.0289585 (initial total Jz~.0399931). Mass is also net inward. Energy export accompanied collapse while the inner field accumulated spin and mass; this does not demonstrate the low-spin final object the proposed route needs.

Weak outer energy currents are not certified. At r8,12,16 the Draco fine budget residual is~20%,322%,1607% of the net transported energy. The innermost r1 energy integral changes by~3x under refinement. Never use small GLOBAL energy drift as a substitute for shell-specific flux accuracy.

The additional resumed T8..8.5 Draco check samples physical flux EVERYdt.01. At r2 it transports mass+.0935144 but energy-.0433656 and Jz-.000545421: an outward mass pulse is not automatically positive-energy cooling or spin export. Its r2 energy budget residual is~0.042% of that flux. At r1 the small positive energy integral+.00032716 closes to~0.061%. Weak far-outer currents remain below their error. These are finite-interval inner exchanges; no infinity escape or late bound-remnant certificate follows.

The larger-angle Draco run reaches11.8 (14.63Myr), then its soft wall cap; sharp-node core mass136.19 million. Its local energy budgets have deteriorated, so neither that late mass nor late flux is a resolved remnant/escape verdict. The extra ne256 nt32 nf32 late checks STOP for >5% Jz drift: Draco10.2, Sextans8.7. They independently expose azimuthal aliasing after collapse. Fornax stops2.4 and Leo6.7 on >5% angular occupancy; do not promote their stopped profiles to final predictions.

## What was fixed and independently checked

The original radial/angular split loses accuracy near the origin despite conserved norm; both original Draco runs fail energy gates. Their sources, raw histories and failed analytic control are preserved. The replacement combines the full radial kinetic/carrier operator and angular barrier in one Hermitian banded CN solve per angular eigenmode, with Yoshida composition and static phase factoring. No numerical carrier energy injection is counted as cooling.

The independent free l2,m2 Gaussian control improves relative wave error2.85e-5 ->2.20e-8 and energy-flux error.001247 ->2.04e-5. Jz flux=2eta times mass flux to roundoff. Gaussian one-source Green/energy-derivative tests pass. Signed finite CN interface transport closes random-state mass/Jz balances at4.9e-16/1.5e-16. Actual v3 radial mass balances close below1e-10 inventory, including negative integration stages. Matter-Jz interface transport excludes gravitational torque and must not be presented as total spin loss.

The independent reviewer found a smooth highm alias counterexample: nf32 gives spurious self-torque-.0348753 even with nearzero ell-tail; nf64 restores torque~roundoff. Added Jz/azimuth checks catch real late failures, but are not substitutes for nf refinement. Canonical shell energy includes +surface(Phi d_rPhi)/(8piG). No auxiliary tag-gradient energy or duplicate cold/Xi gravity is added. Endpoint limitations and all failed implications are in FAILURES.md and REVIEW.md.

## Next decisive obligations

1. Resolve the same late D/S collapse with BOTH radial and azimuth bandwidth, plus physical flux sampled every full timestep. The late256 nf32 shortcut failed spin; ne128 nf64 has inadequate late radial energy budgets. Use checkpointed bounded segments; do not interpret either alone as the answer. Recheck actual measured RSS before stronger grids and keep below1GB.
2. Require shell-by-shell mass, canonical-energy and total-J budgets relative to their transported SIGNAL, a free outer region and box/reflection controls. Classify a stable remnant only after pulses settle; actual signed escaped cold mass must fit the mass inventory. A negative-energy outward pulse is not escape.
3. Derive independently constrained differential supply/assembly and stellar formation timing. The present common200x supply family starts Fornax/Leo too concentrated under the tracer screen. Do not hide that by fitting separate retained fractions. The conditional Sextans total requirement must retain its survey/anisotropy alternatives.
4. Evolve the stars with the SAME converged time-dependent field, moving cores and matched advected controls; check their DF/profile/heating and observational selection. The virial screen is only a screening calculation.
5. Derive a same-model bridge from this CCT wave candidate to the literal current action before transferring any v3 cosmological/cluster verdict. Current owner X40b remains a separate cluster-core scaling failure; old SCT-M CFG960 is not this model.

No frozen criteria, prior packets, publications, shared CURRENT, Claude work or automation was changed. No other chat was messaged. See raw runs, exact before/after source/input hashes, bounded audit directories and per-run v2 records. The theory is not complete.

## Evidence receipt

12 actual galaxy/pulse processes are preserved with12 artifact-validated v2 provenance records. The largest measured process RSS is470,679,552bytes (<1GB; measured, not a hard memory-cap certificate). audit_001 replays3 bounded independent analytic/finite controls. audit_002 checks61 evidence assertions, including exact saved norms/source pins, actual finite radial balances, matched Draco refinement, the Plummer virial coefficient and the preserved aliasing failure/control. Source files compile. Frozen failures remain failed; successful evidence audits do not convert them into physical passes.
