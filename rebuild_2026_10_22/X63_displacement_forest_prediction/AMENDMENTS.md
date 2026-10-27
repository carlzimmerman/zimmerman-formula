# X63_displacement_forest_prediction: AMENDMENTS (post-result, disclosed)

## A1: check K4 is graded at fixed comoving k (recorded after the first run, before any README)

- **What happened.** The first run of `x63_m6_forest.py` (uncommitted) failed the frozen check K4: S(5.4, k)/S(4.2, k) was
  compared with [D(4.2)/D(5.4)]² at the same k in **s/km**. The run otherwise passed K0–K3, K5 and K6.
- **Why the frozen K4 was mis-specified.** A frozen isocurvature mode against a D²-growing adiabatic mode gives the
  1/D² scaling at fixed **comoving** k. A fixed velocity wavenumber maps to k[h/Mpc] = k[s/km] × 100 E(z)/(1 + z), which
  differs between z = 4.2 and 5.4. So the frozen K4 compares the ratio at two different comoving scales. It cannot hold
  to 1e-6 even for a correct implementation. The deviation is largest near the zeros of the top-hat window.
- **Amendment.** K4 is graded on a fixed comoving grid (k = 0.5–15 h/Mpc, 20 log points, R_J = 0.1 Mpc/h, both footings).
  The frozen K4 at fixed s/km is still computed and printed as `K4_as_frozen` (reported, not graded).
- **What does not change.** The observable, the amplitude, the filtering, the gates, the verdict classes and the MUTATE
  plan are unchanged. The MUTATE requirement that K4 fail applies to the amended K4. This amendment cannot change a
  verdict: K4 is an implementation check, not a grade.
- κ = ½ FITTED; not theory closed.
