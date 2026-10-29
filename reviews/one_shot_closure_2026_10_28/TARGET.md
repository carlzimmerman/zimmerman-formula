# One-shot closure review, checkpoint OSC28

User request: review the latest Claude work and attempt to finish the theory in this pass.

Base commit: `44fd23a71c9888d9ea204c0ee832805829f9c090`. The checkout is shared and dirty. Claude subsequently committed FD1 amendment `ae0b838549` and result `36b861cb74`; these are included as explicitly identified later inputs. Original scripts, frozen results and existing modifications are preserved. No publishing or adoption of a new theory is part of this review.

The target is a single predictive physical model connecting the adopted acceleration scale to galaxy dynamics, lensing and the cold cosmological component. Completion requires consistent definitions, a specified conserving evolution or action, a physically admissible halo/field solution selected from stated initial data, calibrated joint observational tests, and honest separation of fitted parameters from derived ones. The coefficient kappa=1/2 may remain fitted if explicitly declared; doing so does not derive it. An empirical pass table, an equilibrium construction or a proof of a different acceleration law is insufficient.

Executed routes:

1. Empirical falsification/reproduction: inspect the newest calibration and later tests, and test the strongest claimed sign exclusion from raw stored rows. Owner: empirical_audit; write scope `empirical/`.
2. Dynamical completion: test whether the finite kinetic log equilibrium can inherit the fluid relaxation dynamics. Owner: mechanism_closure; write scope `mechanism/`.
3. Exact foundations: identify the acceleration law actually implemented, audit theorem transfers, and test parameter selection. Owner: theory_audit; write scope `foundations/`.
4. Coordinator necessary conditions: test whether the core floor can by itself imply the exact law, and turn the new IC 1613 literature into an explicit conditional mass requirement. Write scope `necessary_conditions/` and top-level synthesis.

Failure of one construction is not a universal no-go. Computations of stored statistics are finite checks; literature-derived galaxy quantities are not newly measured data. No new global simulation or survey fit is claimed. Input hashes and commands accompany the results.
