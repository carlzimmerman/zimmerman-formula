# QX7 iter_3: cold dark energy heated by the dark-energy fraction, lambda_J = lambda_* Omega_DE(a)^p. FAIL (no window)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria f9020230b6. Script: qx7_iter3.py (one thread, a few minutes).
Outputs: qx7_iter3.json/.out, qx7_iter3_MUTATE.json/.out; run logs run_main.txt / run_mutate.txt.

## Result

- Omega_DE on the QX3 background: 0.030 (z=3), 0.069 (z=2), 0.199 (z=1), 0.371 (z=0.5), 0.666 (z=0). The switch saturates (Lean
  `omega_de_lt_one`, `omega_de_mono`).
- 31 of 2,989 cells pass the forest, the reference galaxy and the 12 massive systems.
- **G2' (CMB-lensing growth): no cell passes.** The closest is Delta chi^2 = 17.87, against a line of 4.
- Label: **FAIL (no window)**. It does worse than iter_2's power law (9.47), because Omega_DE only doubles between z = 3 and z = 2.
  So a large p is needed to clear the ellipticals, and then the late-time Jeans length grows by Omega_DE(0)/Omega_DE(2) = 9.7
  to the power p.
- Reading 3b (Omega_DE read locally through the khronon expansion): virialised regions would be hot, so no bound system captures
  dust and clusters get QX2 iteration 1's FAIL. That label comes from the argument in the criteria.
- Sensitivity (no label): G3b at z_c = 1 gives 78 analytic cells, z_c = 3 gives 0, M_t = M_b gives 79.

## Known answers and controls

- K1 (frozen): the generalised solver equals iter3's g2 at (beta -1, mu0 1e3): 8e-6 = 8e-6. That point is nearly trivial, so
  K1b is reported (not frozen) at mu0 = 1: 55.6403 = 55.6403.
- MUTATE 1 (massive M_b x 10): analytic cells 31 -> 3. **BITES.**
- MUTATE 2 (f_cap 0): X-COP mean +0.4675 / +0.4345 = QX2. **BITES.** MUTATE 3 (f_cap x3): moves it by +0.318 / +0.311. **BITES.**
- First run: the label block crashed (KeyError, a misplaced else) after every number had printed. It was fixed and rerun, with the
  numbers identical.

## What iter_2 and iter_3 show together

On these two forms a leaf-uniform (clock) heating cannot keep the dust OUT of the 12 massive law-obeying systems by z = 2
(lambda_J >= 0.45 Mpc physical), keep the forest cold at z = 3 (lambda_J <= 0.15 Mpc), and keep the dust clustering
through the lensing kernel. Only the first two form an ordering, as in QX3 iter3: a 3x rise in lambda_J over Delta z = 1.
The growth gate fails because both forms keep rising afterwards. A heating that stopped after z = 2 is not graded here.
iter_4 keeps the switch and drops the requirement that dust stay out of galaxies at z = 2: early capture and late puffing up.
