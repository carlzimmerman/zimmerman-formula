# UD3: Malin 1 with a warped outer disc (FROZEN CRITERIA)

Committed alone, before any script or number of this lane exists. κ = ½ FITTED. Not theory closed. Footings never
pooled. Not blind: UD2's result is known (the law fails on shape at one inclination; the paper says outer i 32° would
fit MOND). Adopts nothing. One galaxy excludes nothing.

## 0. Why

Owner 2026-11-04: "Yes, test the warp". UD2 (46d8dcd8c5) graded one inclination for all rings. Lelli+2010 found the
position angle constant inside 15″ ≈ 24 kpc and rising linearly to 65° at 65″ outside it (a warp). They fixed i = 38°
because the velocity field could not constrain i(R), and they state that 32° in the outer parts "cannot be ruled out"
and would agree with MOND.

## 1. Inputs (no new data)

Table 3 rotation curve and errors as in UD2. Baryon components at the Table radii are read from UD2's committed output
ud2.json (key decoHL: gas, LSB, HSB at M/L 3.3 and 0.9). The law, ν and footings are as UD1/UD2. Rings inside 24 kpc
(12.5 kpc) keep i = 38°.

## 2. Warp models (V and its error at a warped ring × sin 38° / sin i(R))

- **Primary (step):** i = i_out for R > 24 kpc (rings 37.5, 62.5 and 87.5 kpc), with i_out = 32°.
- **Reported, also labelled:** ramp, i linear from 38° at 24 kpc to i_out at 101.6 kpc (65″, the end of the PA ramp);
  step on the outer two rings only.
- **Free scan (step and ramp):** i_out 15° to 60° in steps of 0.1°; the i_out range with p ≥ 0.05 is reported.

## 3. Baryons under the warp

- **Primary:** baryon components fixed as published (the paper's MOND statement made no change).
- **Variant, graded beside:** the deprojected gas and LSB surface densities at warped rings scaled by cos i(R)/cos 38°,
  applied locally to V_gas² and V_LSB² at those rings. This is a stated local approximation to the non-local potential.

## 4. Labels (per footing, per model)

- χ² over all four rings; **CONSISTENT** p ≥ 0.05, **FAIL** p < 0.01, **TENSION** between (as UD2).
- **RESCUED BY WARP** if, in the primary step model with fixed baryons, some i_out ≥ 32° gives p ≥ 0.05. That is a change of at most
  6°: the authors' stated amount, and 2σ of the published i0 ± 3°. **NOT RESCUED** otherwise, with the i_out needed
  stated.
- The primary step at exactly 32° gives the headline label.

## 5. Checks

- **K0:** at i_out = 38° every model returns UD2's χ² to 1e-6.
- **K1:** no optimiser.
- **K2 (wiring, a reproduction; not "Newton must lose"):** the paper's MOND-fit total from UD2 (mond2comp) under the
  same 32° step gives a χ² printed beside. The criterion is only that it is computed from the same code path.
- **Rerun:** byte-identical.
