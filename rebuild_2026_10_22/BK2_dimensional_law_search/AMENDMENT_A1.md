# BK2 AMENDMENT A1, committed before any search number or any formula other than the law's own known-answer row

Numbers I had seen at this point: the law's known-answer row through `bk2_lib.py`, and the fast key tier's check. No candidate formula has been evaluated. No gate or tolerance is widened.

1. **Fast key tier refused, as frozen.** SL1's cached linear response reproduces LW1's law row at gas +0, f* 0.034 only to max |dZ| 0.34-0.38 (G-OUT-Mall), M3 +4.56 against +4.81, against the frozen 0.1. So G8 uses LW1's real path only. `bk2_keys_fast.py` stays as the record of that failed check.
2. **rho_b, Sigma_b floor.** The freeze said negative slopes are clipped at 0. A zero makes every inverse of them infinite on data rows, which would delete those forms for a noise reason. Floor: dM/dlnr >= 0.01 M. This doesn't change any line.
3. **S line's rms is 0.110,** read from `X36_efe_discriminator/step0_em1/em1_emergent.py` `line()`: rms <= 0.110 and median U 0.50-0.80. Per-galaxy Upsilon on UPS, weights and OK mask from SL1's cache; bulge x 1.4 U as there. Known answer: law rms 0.0541, 0.0537, U 0.52, 0.44.
4. **Groups use the real Hernquist profile** for Sigma_b, rho_b, Phi_b, since SL1's path has it, so they aren't [ONE-POINT]. Stars only, g_gas 0, as on record.
5. **IC 1613:** LW1 printed E -0.593, Z -7.9 as READ FG1, which came from BS1's row at its own constants. X1's row through LW1's estimator, the path I freeze, gives -0.535, Z -6.75 canonical. So the frozen known-answer check on IC 1613 **FAILS at 0.01** on value. I keep the X1 row, which is the same path as G9, and report both. No line is near either number for the law.
6. **Structural windows.** The search needn't evaluate every pair at the Saturn point. I_k is increasing in Y and A + B, A - B, H x H are monotone, so the pairs inside G1a's window at Saturn come from sorted-array searches. Pairs outside are counted as enumerated and pruned, not evaluated. Results are identical to the full loop; a unit test checks that on a small closure.
7. **Near-miss tally order:** Saturn window, Mars and Earth, X-COP prefilter, SPARC subsample prefilter, then the harvest's full train gates, G2, G3, both readings.
8. **Harvest budget:** if prefilter hits exceed the 200 MB cap, those over it are counted and dropped by run order, and the title says so.
9. **G12's sigma_c** is computed as half-range of 1/c over c 1.2-1.9 relative to its midpoint, 0.23 of r. That is what the freeze's words give; stated so it isn't chosen later.

kappa = 1/2 FITTED. Not theory closed.
