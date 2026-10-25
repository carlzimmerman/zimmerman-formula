# X29 AMENDMENT A1 (written during the main run, after canonical's numbers were seen; disclosed)

Two implementation issues showed up in the main run (`run_main.log`). Neither changes a frozen line, the model or the data.

1. **K0's tolerance was wrong for this control.** With T² ≡ 1, F's framework nodes take the S0 run's `P_grav` while the
   control arm takes its `P` (CFG654 `build()`). In the S0 control these differ at the 1e-7 level in σ₈, which gives
   Δχ² = −4.3e-5 (KiDS) and −2.1e-5 (DES), not 0 to 1e-10. K0 is re-read as |Δχ²| ≤ 1e-3, with the offset printed. The
   frozen 1e-10 line is reported as FAILED.
2. **Floor on T² (rerun, `--floor`).** Where linear Jeans oscillation drives δ through zero, T² reaches ≈ 0 at k ≳ 1–3
   h/Mpc. The scorer's log-power interpolation then breaks: Δχ² of 1e19 to 1e47 appears on some points. Those numbers are
   artefacts. Their direction (very large) is right, but their size is meaningless. The rerun floors T² at 1e-6 before
   the log interpolation, and is otherwise identical. Outputs carry `_A1FLOOR`.
   - Grading: a point whose main-run Δχ² is non-finite or > 1e6 is graded from the floor run.
   - If the class counts differ between the runs, both are reported. The floor-run class becomes the verdict only if every
     difference comes from such artefact points.
   - Assumption A is restated: a linear T² that passes through zero overstates the suppression of the nonlinear power, so
     the excluded points are excluded under a model that is harsher than the real nonlinear response. This is disclosed,
     not corrected.

**Provenance note (added 10-25, after the coordinator's rerun):** the committed main `x29_late_power_shear.out` /
`_results.json` came from the script **as it was before A1's code edit** (the run started before 1e06cc9946). It therefore
grades K0 against the frozen 1e-10 line (FAIL, 5/6). The committed script carries A1's 1e-3 K0 line, so rerunning it on the
identical Δχ² values grades K0 PASS (6/6). The coordinator's rerun matches every number. The `_A1FLOOR` and `_MUTATE`
outputs were produced by the post-A1 script. No graded number differs between the two script versions; only the K0 label
does.
