# FA2 Amendment A1 (technical, after the first run stopped at KA, before any graded number)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

The first run (run_main.txt, kept) stopped at KA-ell, so nothing was graded. KA-GB1, KA-K, KA-SV5 and KA-WL1 passed;
the sympy statements printed. KA-ell read 0.5000 (Newtonian, line 0.5 +- 1e-3: PASS) and 0.9950 (deep, line 1 +- 1e-3).

The deep line was mis-stated, not the code: at y = 1e-4 the exact law S has g = g_N/2 + sqrt(g_N^2/4 + a0 g_N), so
d ln g / d ln g_N = 1/2 + O(sqrt y) and ell / r = 1 / |s| = 0.99505 analytically. The frozen "deep limit" intent
needs a point where sqrt(y) << 1e-3.

**Change (KA-ell only):** the deep check is made at y = 1e-8 (ell / r within 1e-3 of 1), and the code's ell at
y = 1e-4 must equal the analytic 1 / |s| = 1 / (2 g_N g'/g) of law S to 1e-6. No gate, line, oracle or label moves.

Kappa = 1/2 FITTED; not theory closed.
