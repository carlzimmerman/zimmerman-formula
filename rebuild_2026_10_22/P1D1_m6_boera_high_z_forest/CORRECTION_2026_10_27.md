# P1D1 fix-forward correction

This correction preserves the frozen contract and original outputs as history.
P1D1 remains **NOT DIAGNOSTIC**: the primary null fit has chi-square 137.63 for
39 degrees of freedom, and its Asimov separation is 5.58, below its threshold 9.
No full fit was rerun for this correction. P1D2 is outside this correction's scope.

**Physical interpretation.** Rejecting an upper-envelope template at fixed
physical baryon fraction does not reject a weaker realization. The map from
F_b to measured flux power must be established before a template bound becomes
a physical F_b bound. F_b,max was set by an allowed ceiling; it does not prove
the minimum population required to explain galaxies. This lane establishes
neither side of a decisive physical population-versus-forest inequality.

The original pressure-filter/thermal-broadening identification is also not an
exact degeneracy. Pressure filters q inside the three-dimensional projection
integral; thermal broadening filters the line-of-sight k after projection.
Their cancellation in an idealized ratio does not validate the flux response.
These physical issues are not repaired by a successful sign regression.

**Implementation evidence.** The original K3 injects and fits through the same
SIGN-dependent model. Its mutation may fail by a noise or sensitivity accident,
and the primary K3/K4 were vacuous. They must not be cited as independent sign
validation. The new `p1d1_independent_sign_check.py` instead:

- plants a literal six-bin positive excess separately from the candidate;
- executes only the original `Setup.model_shape` and `Setup.gls` definitions
  against controlled spectra, without importing the executable script;
- profiles positive amplitude and mu on [0,3] at fixed nuisance;
- requires recovery for the positive candidate and rejection for the negative
  candidate on the same injection, without a G1 shortcut;
- demonstrates that the historical sign-correlated injection falsely recovers.

This is a finite implementation regression with synthetic sigma=0.1 per bin,
no noise realization and no observational significance interpretation. It does
not test the optimizer's full nuisance surface, physical gas dynamics, survey
likelihood, or response calibration. Run from the repository root:

```bash
python3 rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/p1d1_independent_sign_check.py --output NEW_RESULT.json
```

The output path must not exist. The closure program records its actual run and
input hashes under `closure_program_2026_10_27/technical_fixes/`.
