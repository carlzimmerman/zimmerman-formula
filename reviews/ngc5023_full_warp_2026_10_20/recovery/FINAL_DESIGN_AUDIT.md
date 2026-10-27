# Final finite-family design check

Checkpoint `ngc5023-full-warp-2026-10-20`, base
`c821a8bccc8a20e107b4c6771d31e02d05aa8b10`. Read-only check on
20 October 2026 of the declared scenario parameters and runner source.
No cube fit, residual result, significance, or execution-completion claim
is made here. The detailed publication-error scope remains in
`UNCERTAINTY_SCOPE.md`.

The design contains104 original cases and14 supplementary graphical
cases: **118 unique scenario IDs,117 distinct parameter sets**.
`joint_sobol_01` is exactly the nominal parameter set; it is an intentional
Sobol center point and cannot count as additional physical evidence.
Source-anchored, graphical, structural, local-center, literal-center and
joint-box directions are labeled separately. The JSON disclaims both
probability weights and confidence coverage. That scope is appropriate.

The original generator's broad phase/width dispatch was corrected before
this final snapshot. Direct JSON inspection confirms that phase slope,
phase curvature and width slope now produce their intended distinct
radial profiles. Every case preserves the inner-ten-ring inclination/PA
ties and equal disk rotation profiles. All radius arrays are strictly
increasing. The14 supplemental cases supply separate coherent±arm
phase2°, width0.4arcsec, peak brightness1e−5Jy km/s/arcsec² and
nonzero-radius0.448arcsec directions, with the radial origin fixed and
support changed consistently. These are chosen graphical modes, not an
exhaustion of independent node perturbations.

The publication-error caveats remain necessary in the report:

- Table4 ranges are average one-at-a-time visual deviations, not joint
  hard limits. Its quoted rotation error applies at D_HI; applying that
  error as a coherent whole-curve offset is a selected mode. The lag's
  error instead comes from the source's two-start TiRiFiC procedure.
- Smooth phase/width/brightness and counterwarp modes address important
  omitted directions, but do not recover the unknown ring covariance or
  the complete206-parameter model freedom. Sobol box sampling is a
  deterministic finite sensitivity design, not a posterior sample.
- Separate peak-fixed raw predictions and conditional component-mass
  calibrations distinguish literal brightness/width changes from a chosen
  compensating amplitude rule. The three Table4 masses are same-cube
  constraints, not independent external priors. Clamping widths to zero
  at finite local peak does not require divergent local peaks; the runner
  must continue to identify the global flux calibration as conditional.
- Vertical-family, interpolation, support, wedge and model-class changes
  remain analyst structural sensitivities. Numerical, beam/channel and
  empirical-noise controls belong to their separately recorded checks.
  Their completeness or validity is not established by scenario counts.

The relative training-loss gates1.10/1.25/1.50 are correctly labeled
sensitivity gates rather than confidence thresholds, and the design
retains failures. Absolute ordinary-data adequacy must still be assessed:
a family of poor fits cannot certify either a novel residual or its
absence. Component-amplitude bound hits and weighted design singular
values are recorded by the inspected runner, which helps distinguish
source-bound constraints from identification by the central strip.

One reporting convention deserves explicit wording. `regions()` selects
20arcsec-bin **centers** with|z|≤10arcsec, giving the full central-bin
footprint|z|≤20arcsec stated in the JSON. Validation/guarded center cuts
|z|≥50/70arcsec have minimum bin-footprint edges40/60arcsec, before
beam wings. They should not be described as full sky footprints entirely
beyond50/70arcsec. Feature masks remain fixed to observed coordinates
while trial model centers move. The20 translated blank maxima are
correlated empirical controls; the declared absence of a Gaussian
p-value or blind-holdout claim must be preserved in the final analysis.

Hashes of inspected versions:

| Artifact | SHA256 |
|---|---|
| `scenarios.py` | `ef85a80bf2c98cb3eb43f4ac62a8a36eaee0dcbcfb0414c982d2ef6cbba72c66` |
| `uncertainty_scenarios.json` | `4dc182edf9c6d42c51431fc99ad296c648ccb0e2f238420937583cd1feadc6e5` |
| `trace_scenarios.json` | `f9b58b73e7d7c5b94db3f35cd0128d9ca521b2ed3bd9ac58347def0c69d9e221` |
| `run_family_v2.py` | `7b8d9556b3ba707bb92f67f60bf9ef28fb931129ae4e544ed7c94a35b1be2dae` |
| `compare_model.py` | `49a2d60ab132a12d671a49cb77258768dce3ef16f4e81508b9bc59691698f54d` |

Later code, input or interpretation changes require a new review snapshot;
this check does not authenticate the missing preferred TiRiFiC file.
