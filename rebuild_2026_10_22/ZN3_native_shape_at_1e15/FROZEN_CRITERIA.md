# ZN3_native_shape_at_1e15: FROZEN CRITERIA (committed alone, before any 10¹⁵ zoom has started)

**Question.** ZN1's frozen class is KEYS ONLY. But its top shape tag is lg M₂₀₀ 13.83, and X-COP's clusters sit near 14.6–15, a decade above it, so the rule clamped them to the 10¹⁴ shape. Does the same rule, with the native shape at the mass where these clusters actually are, pass both data sets?

**Disclosed.** This lane exists because of ZN1's result, and I chose it after seeing that result. ZN1, X-COP's gas, f★ 0.034: all 15 keys pass, worst G-IN-Mall −1.73; X-COP FAIL, mean −0.070, rms 0.116, by x −0.164, −0.104, −0.055, −0.010, −0.016. Same at f★ 0.0615: worst −1.83, X-COP −0.078, 0.121. The concentration falls with mass (c_nfw 12.2 at 10¹³, 10.35 at 10¹⁴), so I expect less mass at x 0.1–0.2, and X-COP closer to its line. It could also push the outer keys up. A pass here wouldn't be a blind prediction. It would be the same frozen rule with no fitted parameter, at the right mass. ZN1's class stands whatever this finds.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. No a₀ in the dynamics. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Runs
- Seeds 1–9 at nominal M = 10¹⁵, ng 64. z_f 0.385 from X48's own Lacey–Cole. X48's `x48_zoom.py`, unedited, with ZK1's verified kernel, to z_f; then ZN1's `zn1_continue.py` to z = 0. Same softening fraction, step rule, z_i and background.
- Fewer than 6 finished seeds makes the lane UNDECIDED.
- Single thread, nice 15, preemptible.

## Measurement and rule
ZN1's, unchanged, with one addition. The shape is interpolated in lg M₂₀₀ between the measured tags at 10¹³, 10¹⁴ and 10¹⁵, clamped outside them. The snapshot is the one nearest z_obs, as frozen in ZN1. At 10¹⁵ there's no snapshot at z = 0.5, so that node takes its z_f snapshot (z 0.385), the nearest one it has. M₂₀₀ remains fair share inside R₂₀₀, and M_c(r_ta) = M_fair as frozen.

## Grade and verdict
ZN1's, unchanged: X-COP 35 points, |mean Δ| ≤ 0.05, rms ≤ 0.10; 15 keys, both h, |Z| ≤ 2, one template; f★ 0.034 and 0.0615; X-COP's gas scale primary.
- **Z0 PROFILE PASSES BOTH:** X-COP and all keys, at both f★.
- **F★-DEPENDENT**, **X-COP ONLY**, **KEYS ONLY**, **FAILS BOTH**, or **NEITHER AT ONE f★**.
- **[GAS-SCALE-DEPENDENT]** if eRASS1's own gas gives another class. **[MASS-DEFINITION-DEPENDENT]** if MA1's budget M₂₀₀ does. **[NOISE-LIMITED]** if the class holds in under 68 % of 200 seed bootstrap draws at all three masses.

## Reported, not graded
1. M₂₀₀/M nominal, c_nfw, η and M(<r, z = 0)/M(<r, z_f) at 10¹⁵.
2. The 7 X-COP clusters one by one, against ZN1's numbers.
3. BA1's joint χ² on each job.
4. The fraction of cells clamped above the 10¹⁵ tag.

## Checks
- **K1, harness:** with only the 10¹³ and 10¹⁴ tags, this lane's path reproduces ZN1's predictions and X-COP numbers: |d| ≤ 1e-9.
- **K2:** ZN1's measurement check, unchanged.
- **K3:** ZK1's K3 stands for the kernel.
- **MUTATE:** shape's r × 1.5, as ZN1: must move X-COP's rms by more than 0.01 and G-IN-Mall by more than 0.05, else UNDECIDED.
- Any K failure: no verdict, exit 1.
