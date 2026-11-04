# Weak-coupling matter calculation: results and next steps

Checkpoint: CC11, 4 November 2026. Parameters remain e=.003, mu=2e6 GeV,
xi=.02 and the existing leading gravity trajectory. The calculations below
are complete in their stated finite domains; a complete viable cold-matter
history has not been established.

## Results

- **Energy defect repaired in fresh warm histories.** The old energy/work
  error was about 24% of scalar oscillation energy. The refined 30-group run
  reduces it to 1.30e-7 of that energy. Halving the step still changes scalar
  action by 5.53% and photino yield by 1.82%; these state errors remain explicit.
- **Polarized vectors and cold scalar transport implemented.** Vectors retain
  charge, inverse reactions, energy and force. In the separate conditional late
  test, adding elastic scattering changes the surviving charged abundance by
  only +.1444%. It remains about 304 times the chosen charged-relic gate.
- **Leading on-shell neutral-adjoint decay matching completed and reviewed.**
  The late photino component travels on average 67–302 Mpc and supplies only
  2.18e-7 of the required dark-matter rest density under the old-late
  normalization. Its absorption probability is below .067%, insufficient to
  cool the bulk. Gauge and partner daughter populations remain separate.
- **An early cold seed remains possible.** Conserving the computed refined
  warm photino population and settling its mass to the pole value would give
  mean travel .182 kpc, but only .02585% of dark matter. Survival and subsequent
  production have not been derived. A high-precision small-excitation orbit
  ingredient now resolves energies lost by the old total-energy calculation.

Vacuum normalization is still tuned, rather than a derived dark-energy link.
The late test and the new early history are distinct; they must not be spliced.

## Next steps, in priority order

1. **Finish the coupled cold numerical interface.** Carry excitation separately
   from the minimum energy; compute stable minimum-energy differences and retain
   collision increments and compensated work. Integrate the checked
   `cold_offsets/` oracle. Establish state convergence beyond the present BE
   timestep bias. The attempted midpoint replacement was not validated.
2. **Continue one fresh common history through trapping and depletion.** Start
   from `integration/run_joint_fine009/result.json`, carry all 30 species and
   evolving baths, and add adaptive hard momentum support or explicit cohorts.
   Include cold self-scattering only where its scalar-dominated assumptions
   apply, and use the checked decay/inverse packet only in its fixed-pole domain.
3. **Apply the physical viability gates to that same history.** Require retained
   vacuum, sufficiently depleted charged rest density, sufficient cold photinos,
   and separately accounted partner/radiation components. Recheck opacity,
   gravity matching and vacuum normalization before declaring a successful model.

## Where to continue

- [Detailed handoff](reviews/weak_completion_2026_11_04/HANDOFF.md)
- [Plan and completion status](reviews/weak_completion_2026_11_04/PLAN.md)
- [Warm comparison and seed result](reviews/weak_completion_2026_11_04/integration/run_warm_seed001/result.json)
- [Independent energy review](reviews/weak_completion_2026_11_04/review/energy/REVIEW.md)
- [Independent decay review](reviews/weak_completion_2026_11_04/review/decay/REVIEW.md)
- [Integrity certificate](reviews/weak_completion_2026_11_04/VERIFICATION.json)

The research phase performed no Git mutations. This separate packaging step is
authorized by the user's subsequent instruction to commit and push the results.
No additional physics runs are part of this publication step.
