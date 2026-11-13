# EXR2 AMENDMENT A1 (POST HOC), 2026-11-12

Committed alone, after the frozen run (criteria `512015c599`, run `0712e53975`) and before any amended number was
computed. Everything here is post hoc: the frozen run's numbers were seen first. **The frozen word stays
NOT EVALUABLE / NOT EVALUABLE**, and the frozen Part C word stays NOT EVALUABLE. Nothing below changes them.

## What failed and why

The criteria call a position usable only if the service's `Flag_pos` is 0, on the assumption that the flag marks bad
data. It marks the opposite: an aperture that holds a catalogued source.

- All 128 catalogued sources of check K2 return `Flag_pos = 1` at their own positions (and `Bkg_SourceMap` there is
  close to `Count`, the source's own counts). Moved 0.1° away, 115 of 128 return 0. So K2 had no usable source and
  failed, as it should.
- 36 of the 237 wide lenses are flagged in band 022 (48 in band 024); their counts run up to 19 (25), against 0 to 7
  at unflagged lenses. The frozen rule therefore removed the X-ray-brightest lenses from the stack. That lowers the
  measurement, which is the side that favours EXCLUDED. The frozen run's numbers are not a result.

A design error of the criteria, caught by the criteria's own check. The test queries made before freezing met the
flag once (at a position with no counts returned) and its meaning was not looked up.

## Seen before this amendment (disclosed)

- The whole frozen run (`exr2.out`): stack on 195 unflagged lenses +1.75 ± 0.47; predictions 18.9 / 16.0 (Z = 0) and
  104 / 87 (Z = 0.3); brackets down to 8.6 (inner radius 2 R_E) and 11.8 (transmission 0.25) for Z = 0, canonical.
- One diagnostic on the stored answers: the flag counts above; K2 with the flag ignored (median ratio 1.046, 16 to
  84 %: 0.97 to 1.11; moved −0.002); the counts at flagged wide lenses; total counts at the 237 W targets (374 in
  band 022).
- My arithmetic from those counts: with every lens kept, the band 022 stack should be near 5 × 10⁻¹⁵.

## Reading A1 (post hoc; no frozen threshold changes)

- **Usable position:** `de_sky` true, `Exposure` > 0 and `Count` returned. `Flag_pos` is ignored, for targets and for
  offsets alike. (Flagged offsets are kept on purpose: an offset that lands on a source is part of the sky that the
  subtraction is there to remove.)
- Everything else exactly as frozen: values, weights, σ, the conversion, the model and its factors 0.80 and 0.40,
  checks K1 to K6 with their thresholds, family words, the lane-word rule, the six brackets, Part C, Part D.
- Its word is reported as **the A1 reading**, never as the lane word.
- Twins under A1: `EXR2_MUTATE=inject` must read Z = 0 ALLOWED on both footings; `EXR2_MUTATE=shift` must fail K2
  (now a real test: under A1 the true positions pass); `EXR2_MUTATE=newton` must raise pred(Z = 0). Each exits 1.

## Expectation before the A1 run (unverified)

Stack about 5 ± 1 × 10⁻¹⁵. Z = 0.3 EXCLUDED by a wide margin on both footings. Z = 0 EXCLUDED on the primary by a
factor of about 2 to 3 over measured + 2σ, and close to the line in the brackets "inner radius 2 R_E" and
"transmission 0.25", so the A1 reading may carry a bracket tag or read CUSP EXCLUDED UNLESS METAL-FREE there.

## How it is run

`exr2.py` gains one switch, `EXR2_AMEND=A1`, which changes the usable rule and writes `exr2_a1*` files. With the
switch unset the script must reproduce the frozen run's files byte for byte; that is checked and reported.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
