# RF5_growth_native_yardstick: AMENDMENTS (dated; each states whether before or after the numbers it concerns)

**A1, 2026-10-31, before any graded number; only K-check values seen.**
- K4: the first Hankel used linear interpolation in ln ℓ and missed the 1e-3 line (2.2 % in the Gaussian's tail). Cubic spline in ln ℓ:
  8.6e-4. Line unchanged.
- K6: at stride 4 the Gaussian P1D ratio against the analytic projection reached 7.8 % over k_f–8 h/Mpc. The range is set to k_f–6 h/Mpc, as
  P1D4's own A1 did for the same check: 4.9 %, line 5 % unchanged. So the mock's top decade near 8 h/Mpc is not checked at this stride.

**A2, 2026-10-31, after the fits and forest numbers; changes no gate, line or grid.**
- P(k) runs at low z_on stopped in CLASS's stiff solver. Retry at CLASS's default start settings (`pk_retry_default_start`): R1_12000 then completes, R1_7000 does not (its shear stays blank).
- Fit runs have no mPk output, so CLASS prints no σ₈, and the `sigma8` field in the cell JSONs is NaN. σ₈ comes from the P(k) run in `*_channels.json`; the grader overrides from there. No χ² uses σ₈.
- The grader now refuses an unconverged cell (criteria §1: F-K "fails to converge" reads UNDETERMINED; the same is applied to F-R1).
- K9's child timing changed: it is sent SIGTERM once the first checkpoint exists, since fixed sleeps missed that window on a loaded machine.
- `restart` mode added on a coordinator's request (see README §Fit health).

**A3, 2026-10-31, after the forest numbers.** `rf5_diag.py` is a post-hoc, reported-only diagnostic: P(k) ratios, and an R_J = 0.02 Mpc/h node below the frozen floor. It enters no gate.
