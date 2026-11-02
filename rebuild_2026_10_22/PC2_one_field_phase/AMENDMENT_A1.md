# PC2 AMENDMENT A1, post-result, committed alone before the rerun

A first run exists, and I read it. Labels of gates 1 and 2 stay on the frozen rows and tolerances. **Bug, mine:** gate 5's kg/m^3 to g/cm^3 factor was 1e-9, not 1e-3, so s_min read 1e6 too large; caught by hand arithmetic (1/(rho v t) = 2.6 cm^2/g at R_last, 200-250 km/s), and it reverses the reading at R_last. Also dropped a meaningless Delta Neff print.

Gate 2 read MARGINAL, +0.09, against my 70 % expectation of failing. So these POST-HOC rows test it harder. None changes a frozen label; each is printed as POST-HOC:
1. X-COP inside x 0.1 (x 0.03, 0.05, 0.07) from the same hydro, gas and stellar files: Q and the required mass there, since the cold mass read at x 0.1 lies inside it.
2. KiDS at 0.31 Mpc for log M* 10.1, 10.5, 10.9 and at 1 Mpc: the mass bins' spread, and where the record's law reach ends.
3. Q_bg for C1's thermal relic against law classes.
4. N_bg from Liouville, and Gamma/H with it, at s_min from R_last and from the lens radius.
5. Polytrope pincer, parameter-free: a law phase with P = K rho^3 (n = 1/2) or K rho^2 (n = 1), K set by the c_s MC1's P1a needs to clear discs, 0.6-0.8 V, evaluated on FRW: z at w = 1/3, against dust by z 3e4.
6. The mass log M at R200 implied by the gate-2 gap, and whether that landing is independent, given 0.31 Mpc is about R200(T).
