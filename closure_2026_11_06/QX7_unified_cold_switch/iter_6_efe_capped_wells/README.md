# QX7 iter_6 (door A): iter_5's host-held dust with the measured external field capping every well. FAIL (clusters, 0/20 cells both footings)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria c302aa5804 + Amendment A1, both pushed before any number.
Script: qx7_iter6.py (main) and `--mutate`. Outputs: qx7_iter6.json/.out, qx7_iter6_MUTATE.json/.out, run_main.txt.

The law everywhere is the 1D EFE form g = g_law(g_N + g_Ne) - g_law(g_Ne), with g_Ne = e_N x 1.2e-10 and e_N primary 0.0033.
iter_5's solver, gates and predictor are run from iter_5's own source, and only the law is swapped.

## Result: FAIL (clusters), both footings

- **The galaxy gates now pass for lambda_0 6.81-100 Mpc.** The capped well lets isolated galaxies shed their dust. That gives a
  window of 20 cells, where iter_5 had none.
- **In the window the clusters are the plain law again.** X-COP is +0.33/0.37 to +0.37/0.41 canonical and +0.29/0.34 to +0.34/0.37
  alt, with groups at 0-1 of 20. Not one cell passes on either footing.
- **Below 4.6 Mpc the cap makes KiDS worse, not better.** The shift is -0.46 to -0.29 (iter_5: -0.27 to -0.10). In the weak-field
  linear regime the law counts the dust in full.
- **Clue, ungraded: the EFE wrecks the law's own lensing baseline.** With no dust, the KiDS mean misfit is +0.870 canonical and
  +0.831 alt, against +0.142 and +0.102 for the isolated law. G6 is graded as a shift from that baseline, so the gate passing
  hides this. The measured field cannot cap galaxy wells without also cutting the lensing tail the law gets right.
- **Bracket (reported):** for e_N 0.0004, 0.0052 and 0.026, the smallest |KiDS shift| sits at lambda_0 8.25, 5.62 and 3.83. X-COP
  there is +0.34, +0.29 and +0.20 (rms 0.31-0.38). It is never near the line.

## Controls (all hold)

- K1, e_N 0 reproduces iter_5: X-COP -0.1234 vs -0.1234 and -0.1536 vs -0.1535. PASS.
- K2, the limits of the EFE form: the ratio is 1.000000 in both limits. PASS.
- MUTATE A, e_N x100: the KiDS shift moves from -0.349 to -0.101. BITES.
- MUTATE B, lambda_0 1e-3: all three galaxy gates fail. BITES.
- MUTATE C, f_cap 0: the shift is 0. PASS.

## Reading

Capping the wells moves the window but cannot open clusters. Wherever galaxies are clean, the dust has also left the clusters.
This is iter_5's one-Jeans-length wall, now with the measured EFE added.
