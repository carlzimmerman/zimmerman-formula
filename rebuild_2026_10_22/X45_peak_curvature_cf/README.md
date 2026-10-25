# X45_peak_curvature_cf: peak height and curvature plus spherical collapse do not produce c_f ≈ 4. The collapsed formation object is a near-uniform core.

Criteria: `FROZEN_CRITERIA.md` (1fd8e1238a). `AMENDMENT_A1.md` holds A1 (normalisation inconsistency and K2's design) and
A2 (the unsmoothed cross-correlation profile). Both are post-result, so **this lane's verdict is post-hoc and exploratory**.
RUN1 and RUN2 are kept. κ = ½ FITTED. Footings never pooled. The record's own P(k). No simulation calibration. Not
"theory closed". Nothing here says the data favour the framework.

## Result: **PK FAILS** in every run (RUN1, RUN2, RUN3 = A1 + A2), both footings

- **No mass from 10¹⁰ to 10^15.5 M☉ produces a −2 log slope inside the formation object.** Every c_f falls back to X44's
  1.85, so the regrade equals X44: groups Z +2.48 / +2.29, MID T3 Z +2.9, MGAS T3 OUTER Z +4.08.
- **Why (diagnosed, RUN2 and RUN3).** Shell by shell, spherical collapse of the BBKS peak profile, with ν set so the
  half-mass object collapses at z_f, gives a profile with slope ≈ 0 over 75 % of the shells and only −0.6 at the edge.
  All shells of the formation object collapse at nearly the same time, and each ends at ½ r_ta, so the object is a
  near-uniform core. That holds whether the profile is smoothed (W²) or unsmoothed around a smoothed peak (W).
- The peak statistics themselves behave as they should: ν rises from 0.4 to 3.6, ⟨x|ν⟩ from 2.15 to 3.2, and γ from 0.51
  to 0.71 over 10¹⁰–10^15.5 M☉.

**Checks 5/5** (K3 EM1 σ₈; K1 BBKS identities δ(0) = νσ₀ and −∇²δ(0) = x̄σ₂ to 1e-16; K2 the high-ν limit, at ν = 30
after A1; K0 constant c_f = 4 reproduces X43; K4 1.1 GB). `--mutate` (curvature term flipped) fails K1, exit 1.

## Reading

- **c_f ≈ 4 is not a property of the initial peak plus spherical collapse.** Steep inner slopes, with r₋₂ well inside the
  halo, come from shell crossing, orbit mixing and mergers. None of that is spherical, and none of it is captured
  shell by shell.
- That is consistent with X44 (scale-free infall gives 1.85) and with the standard picture, in which concentrations are
  measured from N-body relaxation, not derived analytically.
- **What a framework-native c_f needs:** a measurement in the record's own collisionless simulations. The PM engine's S0
  control runs (CFG596/CFG654, 1024³, the record's own background and P(k)) contain halos at their formation epochs.
  Measuring c_f there would be native, with no ΛCDM-calibrated relation and no import. It would replace X43's one external
  number with the record's own.
- Until then X43 stands as the phenomenology: one rule with one standard number, c_f ≈ 4. The data independently pin that
  number at 4–4.2 (X44, X42).

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `x45_peak_cf.py`, `.out` / `_results.json` (RUN3), `_RUN1` / `_RUN2`,
`_MUTATE`, `x45_regrade_*`, `RUN1_*`, `RUN2_*`, `x45_x30_machinery*.log`.
