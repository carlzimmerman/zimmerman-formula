# AC19 frozen criteria: does an action on the table supply FN6's mass-dependent screening length?

Frozen before any script. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle.
No LCDM input: rho_DE is the framework's own (rho_DE = 4 a0^2/(G c^2) from a0 = kappa c sqrt(G rho_DE)).

## Door

Closure doc section 2, "Covariant source for the FN6 window": NO VERDICT (AZ41, read only). FN6
(finish_2026_11_04/FN6_powerlaw_screening) found a WINDOW for a Gaussian screen of width
L = L_MW (M / 6e10 Msun)^p: p in [0.30, 0.45], L_MW 1.5-3 kpc (both footings). FN6 says no action
produces this length. AZ41 screened a NEW constitutive family (power-law stiffness) and found no
regular member. This lane asks the narrower closing question: do the actions ON THE TABLE (v3s, adopted
scoped; AC2q, candidate) produce a length with exponent p in [0.30, 0.45] from their own equations?

## Method (sympy, exact exponents; numbers for size only)

Static, spherical, isolated point mass M, mu_K = 0 (v3s in galaxies), the PN Lagrangians already on
record (AC8's L_v3s and AC2q's on-region L_q):
Poisson del^2 phi = K(rho + D.P [+ s^2 terms]), P equation W'(K|P|) + stiffness gamma_L grad(D.P [+ s^2]).

Enumerate every term in these static equations and the scale it carries:
- source / MOND term J(Y) / W: a0 -> r_M = sqrt(GM/a0)
- stiffness gamma_L = K Lstar^2/2: Lstar (fixed, the record's lower bound 21.7 / 22.9 pc)
- AC2q charge offset 2X = s^2 <= 2 rho_DE (static, framework-native bound, taken at equality)
- curvature / horizon: GM/c^2 and c^2/a0
- v3s dust term mu_K: free constant, mass independent (and set to 0 in galaxies)

An admissible length is a BALANCE RADIUS: the r at which two terms of the same equation are equal, on
the regime where that balance is evaluated (deep-MOND r >> r_M uses g = sqrt(GM a0)/r,
rho_ph = D.P = sqrt(GM a0)/(4 pi G r^2); Newtonian r << r_M uses g_ph -> a0, rho_ph = 2 a0/(4 pi G r)),
plus the fixed lengths themselves. Its mass exponent is p = d ln r / d ln M, derived symbolically.
No geometric means, products or powers of scales are admitted unless they are such a balance radius
(no knob scan, no constructed length). A balance radius is kept only if it lies inside the regime used
to derive it (consistency check, stated per row).

## Lines

- PASS: at least one admissible, regime-consistent length of v3s or AC2q has p in [0.30, 0.45] AND its
  MW value (M = 6e10 Msun, both footings) is within a factor 3 of FN6's L_MW range 1.5-3 kpc.
- FAIL: every admissible length of both actions has p outside [0.30, 0.45], or the ones inside miss the
  size line. The label is scoped to the actions on the table; new constitutive families stay as AZ41 left
  them (screened, none regular). FAIL closes the door for v3s and AC2q.
- NO VERDICT: a known answer or the MUTATE fails.

## Known answers

- KA1: v3s stiffness vs source balance in deep MOND reproduces AZ41's q = 2 crossover r = Lstar^2/r_M,
  exponent (q - 3)/(4q - 6) = -1/2, exactly.
- KA2: AZ41's high-field ratio at q = 2 is radius-independent (no crossover), reproduced.
- KA3: rho_DE = 4 a0^2/(G c^2) gives 5.8424e-27 / 8.5328e-27 kg/m^3 (AC6/AC7 values) to 1e-3.

## MUTATE (separate output)

Plant a mass-dependent offset density rho_X proportional to M^(-1/4) in place of s^2 (normalized so its
MW balance radius is 2 kpc). Its balance radius has p = 3/8 and must grade PASS. If the grader does not
flag it, the method cannot see a window length and no verdict stands.

## Scope

Static, spherical, isolated. Says nothing about environment-embedded lengths beyond those listed
(D10's embedded scale is proportional to Lstar, p = 0, and is listed), nonlinear or dynamical lengths,
or constitutive families not on the table.
