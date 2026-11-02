# HF1 AMENDMENT A2: post-result, disclosed as such

Written after gate 1's numbers at m 11.8, 11, 9, 7 were read (all four FAIL). kappa = 1/2 FITTED. Not theory closed.

**1. m 5 and 3.74 never ran.** CLASS stopped: N_eff lies outside its BBN helium table, so `FD_m5` and `FD_m3.74` are CLASS_FAIL. They hadn't failed anything. The first grade printed EARLY FAIL over them, which overclaimed. The label now counts them separately.

**2. Those two cells run with YHe fixed at 0.2454,** cells `FDY_m5`, `FDY_m3.74`, same channels, line and CLASS settings, each started from FD m 7's fit. 0.2454 is a stated value, about the standard-N_eff BBN number at this omega_b, recalled and not computed here. It isn't this model's own helium: at these N_eff, BBN would give more, and that isn't computed either. So these cells aren't BBN-consistent, and a number from them says nothing on BBN. No other cell changes.

**Label rule.** EARLY FAIL only if all six have numbers and all six fail. Otherwise: fails at n of 6, k UNDETERMINED. CHI and COLD stay reported variants; their cells that stop on the same table stay unrun and aren't given fixed helium here.

**3. K_off_zero, a check defect, no physics change.** Control maxfrac 9e188 at Rf = 0. Diagnosed: the ratio divided by a 1e-300 floor at the first grid point, where the measured chain's Mb is exactly 0. The solver's Rf = 0 mass is at its bisection floor, about 1e-133 Msun at r_ta, max Mf/Mb 8e-146 where Mb > 0. So the suspected nonzero rho exists but is negligible. `hf1_fermion.solve` is unchanged. The check now tests Mf/Mb where Mb > 0, and Mf below 1 Msun where Mb = 0. The line 1e-6 is unchanged.

**4. R3 selection pool.** With no gate-1 passer, the rule runs over every m with numbers, FD plus the FDY cells. Gates 2 and 3 are numbers only. Gate 4 isn't run while gate 1 fails for every m with numbers. Gate 5 runs only on a surviving m.
