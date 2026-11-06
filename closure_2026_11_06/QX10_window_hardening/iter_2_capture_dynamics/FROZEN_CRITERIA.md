# QX10 iter_2 frozen criteria: does the sector really leave galaxies? Hydrostatic end state + collapse/heating run

Frozen before any iter_2 number. Kappa = 1/2 FITTED; not theory closed.

## Physics (from the switch, nothing added)

At each point the sector is a barotropic fluid p = K(a) rho^2 with K(a) = G lambda_J(a)^2 / (2 pi): the n = 1 polytrope
whose self-gravitating core radius is lambda_J/2 (QX3 D3; Lean QX3_dust_eos). It gravitates as a source of the a0 law
exactly as QX7 iter_4 graded it: g_tot = glaw(g_N,b + g_N,d, a0), and it is pulled by g_tot.
QX7 iter_4 ignored the host's own pull on the sector. This iteration includes it.

## A (graded): hydrostatic end state today, closed system

Captured mass M_d = f_cap R M_b,tot (f_cap 0.76, R 5.562, as iter_4). n = 1 hydrostatics in the host:
d rho/dr = -g_tot(r) / (2 K0), with M_d(<r) self-consistent. If a profile with rho >= 0 holding M_d ends at R_s <= r_ta
(iter_4's turnaround radius today), the system keeps it with that profile. Otherwise it keeps only the mass of the
profile with rho(r_ta) = 0 and the rest has evaporated.

Host baryons M_b(<r): reference galaxy and the 5 most massive SPARC (iter_4's G5 list) as sphericalised exponential discs
with r_d = R_opt/3.2 (R_opt 10 / 20 kpc); KiDS lens points (iter_4's G6, QX5's LE list) as point masses; ellipticals
(G7) from QX5's Mbar(r); X-COP and groups from QX5's measured baryon profiles, interpolated in log-log, flat beyond the
last point at Mb_last / g5(1+fst).

Gates, same lines as iter_4, both footings: G5 M_d(<R_opt)/M_b <= 0.3; G6 |mean shift| <= 0.05 dex; G7 |mean shift|
<= 0.15 dex. Cluster predictions (X-COP HO1 line, groups strict rule) reported, not graded here.

B (reported only): the open reading, the profile in contact with the cosmic sea at r_ta, rho(r_ta) = mean sector
density today.

## Time-dependent run (graded for consistency)

1D Lagrangian spherical barotropic hydro, 400 shells, von Neumann-Richtmyer artificial viscosity, the host baryons
static at their z = 0 profile (stated approximation). Start z_c = 3: the captured mass as a uniform cold sphere at
r_ta(z = 3), at rest. K(a(t)) from the switch on QX7's corner background (t(a) from its H(z)). Evolve to z = 0 with
the a0 law on. Shells beyond r_ta count as evaporated. Runs: the reference galaxy and one X-COP cluster (the one with
the median Mb_last), for cells C1 and C2, both footings. Convergence: 200 vs 400 shells agree on M_d(<R_ref) to 10 %
(R_ref = R_opt for the galaxy, 0.5 R500 for the cluster).

- D-consistency: the run's final M_d(<R_ref) within 20 % (or both below 1 % of M_b) of the static A value. If not, the
  run's value replaces A for that host and the gates are re-evaluated with it.

## Known answers

- KA1: no baryons, Newtonian gravity: the static solver returns the Lane-Emden n = 1 sphere, R_s = lambda_J(0)/2 to
  1e-3, for any mass.
- KA2: host pull and law off (iter_4's idealisation) reproduces iter_4's G5 ratio for the reference galaxy to 1e-2.
- KA3: the hydro code with K fixed, no baryons, Newtonian, relaxes a perturbed n = 1 sphere back to Lane-Emden
  (radius within 5 %).

## MUTATE (separate outputs)

- M1: lambda_0 = 1e-3 Mpc (compact everywhere) must FAIL G5.
- M2: K x 1e4 (lambda x 100) must evaporate the sector from every galaxy host (G5-G7 return to baseline within 1e-3).

## Label per cell

PASS if A's G5, G6 and G7 pass on both footings, with D-consistency held (or the run's replacement values passing).
FAIL otherwise. NO VERDICT if a known answer fails or a MUTATE does not bite.
