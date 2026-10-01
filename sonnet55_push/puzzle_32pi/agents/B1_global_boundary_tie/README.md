# Lane B1: a global/boundary-value tie for the 32 pi puzzle (verdict: SHARP NO-GO; kappa = 1/2 stays FITTED)

## Bottom line
1. No global condition built from {r_s, r_b, r_c, r_N, r_ZF, r_J, r_ES} gives r^2 Lambda = 8 pi together with kappa r = 1/2 at one mass. Every pair coincidence is algebraic (r^2 Lambda = 1, 3/2, 3 in the Nariai/junction/zero-force cases), so it can never be 8 pi (b01, 17/17). SdS horizons obey r_b^2 Lambda <= 1 and r_c^2 Lambda <= 3 independent of how the Killing vector is normalised.
2. The inner relation is local, so an outer boundary only fixes the integration constant M. The horizon relation 1 - 2 kappa r = Lambda r^2 holds at every SdS horizon; kappa r = 1/2 holds only inside a Lambda-free vacuole, where the Schwarzschild radius r_s = 2M is a genuine horizon. There the puzzle's second relation is just a choice of M (M = 1.447 L = 7.52 M_N), not a boundary consequence.
3. The only global tie that exists is Einstein-Straus: the hole fits a vacuole iff rho_m/rho_L <= 3/(8 pi) (an INEQUALITY, the pi enters through the sphere volume, b02 9/9). That holds only after a = 1.57 (about +7 Gyr). The required vacuole is 3.1 Hubble radii wide, and any sub-Hubble vacuole caps r_s^2 Lambda below 3.
4. Mass: M = 1.6e23 solar masses = 0.34 of the observable-universe matter, 11x today's Hubble-sphere matter, 7.5 M_N. Not a meaningful object (it exceeds the Hubble sphere; closeness to a cosmic mass has a 41% decoy hit-rate).
Nearest curiosity (not the puzzle): at the cosmological horizon, |kappa_c| r_c = 1/2 holds exactly at r_c^2 Lambda = 2, M = M_N/sqrt2 (the same point as lane L's n = 3). The coefficient there is 2, not 8 pi.

## Declared before computing (hash `PREDECLARED.sha256`, 32bd1289...)
Radii R1-R7, kappa conventions, conditions G1-G13, success criterion (one M and r with r^2 Lambda = 8 pi, kappa r = 1/2, no 8 pi or a0 inserted). Disclosed priors: algebraic coincidences, r_s above L, ES gives only an inequality. All three were confirmed; none were tuned.

## Scripts (`run_all.sh`, exit 0)
- `b01_radii_coincidences.py` 17/17 (sympy identities + mpmath roots + algebraicity detector with a control that cannot find 8 pi).
- `b02_epoch_mass_decoys.py` 9/9 (LCDM Om = 0.315, H0 = 67.4, rho_Lambda footing; epoch, mass, sub-Hubble bound, decoy hit rate, mutation).

## Results
Facts, each verified: (a) for f = 1 - 2M/r - Lambda r^2/3 every horizon has 1 - 2 kappa_f r = Lambda r^2, so kappa_b r_b = (1 - Lambda r_b^2)/2 and |kappa_c| r_c = |1 - Lambda r_c^2|/2; (b) shell-free Schwarzschild/dS junction R^3 = 6M/Lambda is exactly the Einstein-Straus radius with rho_m = rho_L; (c) the standard ES radius R^3 = 3M/(4 pi rho_m) does not involve Lambda at all (Lambda cancels between interior and FRW), so the task's r_ES^3 = 3M/Lambda is really the zero-force radius, which equals r_ES for rho_m = 2 rho_L; (d) horizons exist iff r_s^2 Lambda < 4/9 (the puzzle is 56.5x above it); (e) the de Sitter-regular normalisation kappa_BH(c) = H holds only at M = 0.

| condition | M/M_N | r^2 Lambda |
|---|---|---|
| r_s = r_ZF | 1.837 | 3/2 |
| r_s = r_J | 2.598 | 3 (r_s = L) |
| r_c = r_J | 0.9186 | 3/2 |
| r_b = r_c = r_ZF | 1 | 1 |
| r_s = r_b, r_c; r_b = r_J; r_ZF = r_J | none for M > 0 | |
| r^2 Lambda = 8 pi for r_s / r_ZF / r_J | 7.52 / 126 / 63 | 8 pi |
At M = 7.52 M_N the junction radius is 1.425 L, inside r_s = 2.894 L: no consistent w = 1 vacuole. pi-count: each coincidence is a polynomial system over Q, so algebraic; 8 pi appears only when w = 3/(8 pi) or M = sqrt(2 pi/Lambda) is imposed, which is the puzzle restated (rho_hole/rho_L = 3/(8 pi) <=> rho_L r_s^2 = 1).

## Not established
Israel-shell surface pressure at r_J, McVittie with time-dependent H (only the constant-H = SdS limit is used), Bousso-Hawking vs f normalisation (left open; the radii bounds do not depend on it), non-GR or MOND-sector horizons. Mass-menu numbers are a posteriori. kappa = 1/2 remains FITTED; nothing derived.
