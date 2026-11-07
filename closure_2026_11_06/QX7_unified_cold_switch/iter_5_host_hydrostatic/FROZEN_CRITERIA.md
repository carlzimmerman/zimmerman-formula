# QX7 iter_5 frozen criteria: today's dust in hydrostatic equilibrium in its HOST's field (replaces iter_4's isolated core)

Frozen before any iter_5 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Test lane under SWARM_BRIEF.md
(cold dark energy, never cold dark matter; no particle; no LCDM inputs; both footings, never pooled).

## Why this iteration (a mutation of iter_4, 22af3e7b43 / result 9a8f2e4778)

iter_4 placed each system's captured dust in the ISOLATED n = 1 core (enclosed fraction (sin xi - xi cos xi)/pi,
R_c = lambda_J(0)/2). That ignores the host: an n = 1 sector (P = K rho^2) in hydrostatic equilibrium obeys
grad h = -g_tot with h = 2 K rho, so it follows the potential of baryons + law phantom + itself. iter_4's own reading of
its cluster FAIL was "too little dust in the centre, too much in the outskirts". The host term is the physics iter_4
dropped. It adds NO constant: K is fixed by the same lambda_J, mu = 2 pi / lambda_0, K = 2 pi G / mu^2.

## Mechanism (frozen)

- Switch, f_cap, R = omega_d/omega_b, capture: unchanged from iter_4. Captured mass M_d,tot = f_cap R M_b,tot, f_cap 0.76.
- Profile: spherical, static. With mu = 2 pi / lambda_0:
      dM_d/dr = 4 pi r^2 rho_d,    d rho_d/dr = -(mu^2 / (4 pi G)) g_tot(r),
      g_tot = g_law( G (M_b(<r) + M_d(<r)) / r^2 ; a0 )   (the a0 law, as the dust and baryons feel it in iter_4's M_law),
  integrated outward from r_min (1e-4 of the isolated R_c, at most 0.1 kpc) with rho_d(r_min) = rho_c, until rho_d = 0 at the
  surface r_s. rho_c is found by bisection (monotone) so that M_d(r_s) = M_d,tot (relative tol 1e-6).
- Retention: a system keeps NO dust if r_s >= r_ta(M_b,tot (1 + R), z = 0) (iter_4's rule with r_s in place of R_c).
- Host baryon profiles M_b(<r), fixed in advance:
  - X-COP: measured gas (fgas_profile MGAS) + stellar (mstar MSTAR) profiles, log-log interpolation; inside the first
    measured radius M ~ r^s with s from the first two points; beyond the last joint radius, constant at Mb_last (iter_4's total).
  - Groups: M_gas power law through (R25, M_gas25) and (R5, M_gas5), times (1 + fst); constant beyond R5 at g5 (1 + fst).
  - Humphrey ellipticals: the Hernquist Mbar(r) (QX16-fixed loader); total Mbar(1e9) as iter_4.
  - KiDS lensing stacks and the G5 SPARC systems: point masses (deepest well for the mass, so the most dust; conservative
    against a galaxy pass).
- Growth (G2') and forest (G4') depend only on the leaf-uniform switch lambda_J(a), not on today's core profile. They are
  CARRIED from qx7_iter4.json (field "evaluated", 857 cells). Reproduction check R1 below.

## Gates (unchanged lines from iter_4)

- G5 SPARC inner mass: M_d(<R_opt)/M_b <= 0.3 for the reference galaxy (1e10, 10 kpc) and the 5 most massive SPARC (20 kpc).
- G6 KiDS isolated lensing: |mean log(g_obs/g_pred) shift| <= 0.05 dex vs M_d = 0, both footings.
- G7 Humphrey ellipticals at 2, 4, 8 R_e: |mean log(M_obs/M_pred) shift| <= 0.15 dex, both footings.
- G4' forest and G2' growth: carried (dchi2 <= the iter_3/iter_4 line I2.DCHI2_LINE).
- Window = cells passing G2', G4' and (recomputed) G5-G7.

## Cluster predictions (no cluster input), PASS line

- X-COP (7 clusters, 35 points, 0.1-0.7 R500): M_pred = M_law(M_b(<r) + M_d(<r)); HO1 line |mean| <= 0.05 and rms <= 0.10.
- Groups (20): strict rule as iter_3/iter_4: >= 16/20 groups with every point within 2 sigma, for BOTH stellar allowances
  fst 0 and 1.
- **PASS** if the window is non-empty and at least one member passes X-COP AND groups (strict) on BOTH footings.
  **FAIL (clusters)** if the window is non-empty and none does. **FAIL (no window)** if the window is empty.
- Reported, not graded: X-COP and groups over every galaxy-gate-passing lambda_0 regardless of growth; per-cluster
  residuals; a Newtonian-g variant of the dust equation; whether a Milky-Way-mass system (M_b 6e10) keeps dust.

## Known answers and controls (each must hold, else the lane reads NO VERDICT)

- K1 (solver): no host and Newtonian self-gravity: r_s = lambda_0 / 2 to 1e-4 relative and the enclosed fraction equals
  (sin xi - xi cos xi)/pi to 1e-4 at five radii.
- R1 (carry): one carried cell's dchi2 is recomputed with iter_3's generalised solver and matches the stored value to 1e-6.
- MUTATE A (host off: isolated core, iter_4's profile): reproduces iter_4's X-COP mean/rms at lambda_0 2.15 Mpc to 2e-3.
  It must, so that any difference is the host term alone.
- MUTATE B (f_cap = 0): X-COP mean equals QX2 iteration 1 (+0.4675 / +0.4345) to 1e-3.
- MUTATE C (bite): lambda_0 = 1e-3 Mpc must fail G5 or G6.
- MUTATE D (bite): f_cap x 3 must move the X-COP mean by more than 0.1 dex at a window lambda_0 where clusters keep dust.

## Out of scope (stated now)

No capture/evaporation dynamics are run (iter_4's caveat stays). The law is assumed off on the linear web for G2' (QX3
A-web). No TT/EE, no full RAR refit. A PASS here would be a scoped candidate for the owner, not an adoption and not an
all-gates claim: CMB TT/EE, UDGs (AGC 114905, Malin 1), FN6 and the remaining QX19 fails would still be open.
