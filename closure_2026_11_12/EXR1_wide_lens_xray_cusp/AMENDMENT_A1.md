# EXR1 AMENDMENT A1 (POST HOC), 2026-11-12

Committed alone, after the frozen run (criteria `0cc195b7f6`) and before `exr1_a1.py` was run. Everything here is
post hoc: the frozen run's numbers were seen first. **The frozen word stays NOT EVALUABLE / NOT EVALUABLE**, and the
frozen Part C word stays NOT EVALUABLE. Nothing below changes them.

## What failed and why

Check K8 asked the 8 null stacks (the tested lenses moved 0.5°) to average within 3σ/4 of zero. They average
+1.61 × 10⁻¹⁵ erg/s/cm² against a limit of 1.33 (σ = 1.77, itself the null rms, so it carries the same offset); all
eight are positive. The cause is the sky, not the instrument: eRASS1's smooth background map leaves detected sources
out, and a random 30″ aperture holds a catalogued source 1.9 % of the time (Part L, at the shifted positions), so a
random aperture has a positive mean net flux. The same offset makes K7's stack leg read 7.1 σ on the clusters moved
0.5° (twin `shift`); that twin bites only through K7's recovery leg (4 of 60). ESZ1's null test (its K9) assumed zero-mean nulls because ESZ1 subtracted each target's offsets; EXR1's
frozen measurement does not subtract them (chosen as the conservative side), but K8 was copied unchanged. A design
error of the criteria, found when the frozen script first ran on the cached upper limits.

All three frozen twins exit 1. Twin `inject` passes K8 only because the injected predictions spread the lenses'
values and raise σ to 15.0 × 10⁻¹⁵, so it shows the comparison flips, not that K8 is sound.

## Readings added (post hoc; no frozen threshold changes)

- **A1 (ESZ1's construction).** Each tested lens's value = its clipped net aperture flux minus the mean of its valid
  shifted positions (at least 6 of 8, ESZ1's 12-of-16 ratio); null k = shifted position k minus the mean of the same
  lens's other valid shifted positions; σ = max(bootstrap, rms of the 8 null stacks); K8 as frozen on these nulls;
  pred_min, thresholds, brackets and tags as frozen. Its word is reported as **the A1 reading**, never as the lane word.
- **R (the frozen measurement, unsubtracted).** The frozen stack against the frozen pred_min, with
  σ = max(bootstrap, rms of the 8 null stacks about their own mean) and only the scatter half of K8. Reported beside
  A1; it keeps the sky offset in the measurement, which works against EXCLUDED.
- **Part C** under A1: unchanged arithmetic (the sky offset cancels in a wide-minus-control difference), with every
  check other than K8 required; reported as a reading.
- **Twin** `EXR1_A1_MUTATE=inject` (the primary canonical prediction added to every tested lens): the A1 primary word
  must read ALLOWED on both footings; exit 1.

The other checks (K1–K7) are taken from the frozen run as they stand. `exr1_a1.py` reads only the frozen run's
outputs (`exr1_arrays.npz`, `exr1_results.json`).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
