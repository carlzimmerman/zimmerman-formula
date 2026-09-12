# Fixed-action closure checkpoint

This checkpoint began at `ac2052ae0`, then audited L206 and time-certificate
commit `0eee1a513`. Later L207/L208 were read for dependency impact. No original
Claude/Hermes file or coefficient function was changed. The full theory is OPEN.

Before this checkpoint was published, Claude's `63c71679b` (L210) accepted
the sign and pressure corrections and withdrew the affected claims. The
historical reports retain their exact audited targets; the exact turning
bound below is an additional result.

Read `../../gw_clock_timing_2026/REPORT.md` for the cited GW/time investigation
and `../../gw_clock_timing_2026/VERIFICATION.md` for the consolidated commands.

Results, with deliberately separate scopes:

- `health/REPORT.md`: L205's static gradient-energy sign is reversed for its
  stated Q=0, gamma=0 scalar action. The original near-origin health condition
  is U>4dell, not the lower bound used by L207/L208's search window. This is
  not a full metric health theorem; the added operator needs its own analysis.
- `health/pressure/REPORT.md`: arbitrary-lapse action variation retains the W0
  counterterm omitted in L206. On Q=qbar(tau), p=U(s-1) exactly. An equation
  of state does not replace the clock Euler equation or prove a free-w branch.
- `health/turning/REPORT.md`: the exact L207 turning-point bound is
  beta²<=16d²/(243ell); the proposed approximate `Y_min` is instead near the
  maximum of W_Y. A falling W_Y at Y_star requires the exact local bound
  recorded there. Three Lean theorems certify the coefficient inequality.
- `boosted/REPORT.md`: aligned Y_background=0 does not remove perturbation
  mixing. The leading minimally coupled moving-dust scalar and lapse residues
  are derived; global retarded solutions and PPN matching remain undone.
- `boosted/tensor_cone.py`: on homogeneous aligned FLRW the tensor and Maxwell
  physical speeds are independently computed as one from their action
  coefficients. Current output is `tensor_result_v2.json`; the earlier result
  is preserved only as a superseded checkpoint.
- `boosted/ClockGeometry.lean` and `clock_lapse.py`: normalized clock geometry,
  proper-time rate, expansion and acceleration are distinguished. Homogeneous
  expansion is not normal acceleration, and a scalar-clock rate is not a
  relative photon/tensor propagation speed.

Do not use 1<4dell/U<8 as a certified search gate. Its original lower-bound
energy interpretation fails, and its upper-bound Hubble-kernel identification
is not derived from this action. Do not change coefficient histories merely
to force entry into that window.

All new Python scripts were executed; each Lean certificate was compiled and
its printed axioms inspected. These checks establish their written bounded
claims, not empirical or full relativistic closure.
