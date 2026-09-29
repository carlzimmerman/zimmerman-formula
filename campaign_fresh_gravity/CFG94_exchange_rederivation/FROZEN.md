# CFG94 FROZEN SPEC (written before any run; never edited afterwards)

Independent re-derivation of the enclosed-mass-exchange headline numbers (CFG48 G4 / CFG70). kappa = 1/2 is FITTED. Nothing here
says the theory is closed or that data favour it. Own code only; the CFG48 G4 script, the CFG70 scripts, their .out/_results.json and
CFG48_referee_rederive.* are NOT opened, read, exec'd or imported before my frozen main and MUTATE runs are complete.

Read before freezing (and only these): CFG44 README, CFG48 README, GATES_FROZEN.md, CFG48_REFEREE.md, CFG70 README, and the definitions
of nu_mono (CFG3_common._build_mono, read as a description: h_RAR(y)=y/(exp(sqrt y)-1); nu_mono = 1 + h_mono/y with h_mono the
monotone version: h_RAR up to its peak y_p (h' = 0), then h' floored at 0.05 h_p/(y+y_p); I rebuild it myself), of B's committed r_ta
(CFG4_target.r_turnaround / CFG11.rta_of: the radius where the law's enclosed total mass M_b nu(GM_b/(r^2 a0)), phantom included, falls
to Delta_ta(z) rho_m) and of CFG48's r_ta (as described in CFG48_REFEREE section 5: from the collapse mass M_b(1+Omega_c/Omega_b)).
NOTE: the referee section I was allowed to read contains the CFG48 closed forms and 1.5 x_e; my derivation below is therefore NOT blind
to those targets, only blind to their code. The README of CFG48 also states them. I derive them myself anyway and test them numerically.

## Question
Reproduce, to 3 significant digits, (i) the late-time reaction of the enclosed-mass exchange on a point baryon mass, reaction/g_law at
x = r/r_M = 0.3, 1, 3, 10, 30 (targets pressure reading 0.065/0.53/2.13/7.46/22.5; sigma reading 0.062/0.398/1.17/3.77/11.x; the
0.10 g_law line crossed at x = 0.38) and (ii) the energy the exchange must supply, E_c/((1/2) M_b V_f^2), for M_b = 1e9/1e10/1e12 Msun
(targets 72.8/49.6/23.0 in CFG48's r_ta convention, 318/179/57 in B's committed r_ta with canonical a0 and nu_mono). Then attack the
conventions and ask whether any choice passes both lines (reaction <= 0.10 g_law on x in [0.3,30] AND E_c <= (1/2) M_b V_f^2).

## The target and the functional, as read
Point baryon mass M, a0 = 9.3603e-11 m/s^2 (canonical; alt 1.1312e-10), r_M = sqrt(G M/a0), x = r/r_M, g_N = G M/r^2 = a0/x^2.
Law (P2): g_law = sqrt(g_N^2 + a0 g_N) = a0 sqrt(1+x^2)/x^2. CFG44 target: the cold fluid obeys C(r) = rho_c r^3 g_tot = (a0/4pi) M_b(<r), so
rho_c = a0 M/(4 pi r^3 g_tot) with g_tot = G (M + M_c(<r))/r^2 = g_law (self-consistent: M_c = M(sqrt(1+x^2)-1)). Hydrostatics dP/dr = -rho_c g_tot
gives P = a0 M/(8 pi r^2); sigma^2 = P/rho_c = r g_tot/2 = V_c^2/2. Internal energy density u = (3/2) P (= (3/2) rho_c sigma^2).
Exchange as a bilocal energy: E[q; m, M] = integral_0^inf 4 pi s^2 u(s; M_enc(s)) ds with M_enc(s) = M + m Theta(s - q): a probe baryon shell of
mass m at radius q raises the enclosed mass seen by every fluid shell at s > q ("enclosed mass keyed" exchange). The fluid is in its target
state (late time, static limit, r = 1: all the heat is booked in the closed baryon+fluid ledger). Reaction on the probe (outward positive) per unit
mass: a(q) = -(1/m) dE/dq in the limit m -> 0. Two readings of what is held fixed when M_enc changes:
  pressure reading (P-slaved): the fluid volume elements are fixed, u = (3/2) P(s, M_enc) with P = a0 M_enc/(8 pi s^2).
  sigma reading (sigma-slaved): the fluid SHELL MASSES dm_c = 4 pi s^2 rho_c^target(s) ds are fixed; the energy per unit mass is (3/2) sigma^2 with
  sigma^2 = V_c^2/2 = (s/2) g(s; M_enc), g = sqrt(g_N^2 + a0 g_N), g_N = G M_enc/s^2.
Reported ratio: a/g_law(q). The energy the exchange must supply: E_c(<r_e) = integral_0^{r_e} 4 pi s^2 u ds at the target (both readings identical there),
compared with (1/2) M V_f^2, V_f^4 = G M a0 (the law's asymptotic flat speed; alternatives listed in the sweep).
Edge r_e = 0.4 r_ta (B's declared centre of the window [0.31, 0.48]). r_ta conventions: (A) CFG48: (4pi/3) Delta_ta rho_m r^3 = M_b (1+Omega_c/Omega_b);
(B) B committed: M_b nu(G M_b/(r^2 a0)) = (4pi/3) Delta_ta rho_m r^3 with nu = P2 [sqrt(1+1/y)] and nu = nu_mono (own rebuild).
Cosmology: flat LCDM Omega_m = 0.3153, h = 0.6736, Omega_c h^2 = 0.1200, Omega_b h^2 = 0.02237 (Planck 2018; MY choice, the READMEs do not state it: they imply
Omega_c/Omega_b = 5.36), z = 0. Delta_ta = 1+delta at turnaround for a shell turning around today, from my own spherical-collapse
integral (time from R = 0 to turnaround = age of the universe); CFG48 uses 11.81; both reported, headline = mine, then a labelled variant with 11.81.

## Pass lines (fixed now)
R1. Reaction numbers reproduce the printed values to 3 significant digits (relative difference <= 0.5% counted as a match to the printed 3 s.f.; the
    printed sigma value at x = 30 is "11.x", accepted if 11.0 <= value < 12.0; 11.3 is quoted by CFG70). Crossing 0.10 at x = 0.38 to 2 digits.
R2. Energy numbers reproduce 72.8/49.6/23.0 (A) and 318/179/57 (B, nu_mono) to 3 s.f. (relative <= 0.5%; ONE-digit-in-the-third-place differences are reported as the
    cosmology/Delta_ta sensitivity, not tuned away).
R3. No tuning after seeing numbers; a failed control is a failure; non-reproduction is a valid outcome.

## Controls (each must pass or is reported FAIL)
C1. M_c(<r) = integral 4 pi s^2 rho_c ds = M (sqrt(1+x^2)-1) to 1e-7 (numerical quadrature) at x = 0.3, 1, 3, 30.
C2. Hydrostatic identity dP/dr = -rho_c G (M+M_c(<r))/r^2 to 1e-6 (numerical derivative) and sigma^2 = V_c^2/2 to 1e-12.
C3. Reaction by numerical differentiation of the bilocal energy (smoothed probe step of width w = 1e-3 q, extrapolated with w = 5e-4 q; m/M = 1e-4 with +- m symmetrised)
    agrees with my closed form (3/4) a0 (P) and (3/8) a0 (2+x^2)/(1+x^2) (sigma) to 1e-3 relative at every x in the table.
C4. Asymptotics: x -> 0: a/g_law -> (3/4) x^2 in both readings (ratio to that within 1e-2 at x = 1e-3); x -> inf: P: (3/4) x, sigma: (3/8) x (within 1e-3 at x = 1e4).
C5. Energy at zero reaction: scale the internal-energy coefficient lambda (u = lambda P) to 0: both the reaction and the energy vanish (< 1e-30 relative to lambda=3/2), and
    E_c/(M r_e a_react(P)) = 1 exactly (pressure reading: E_c = (dE/dM_enc) M r_e) to 1e-9, i.e. the two pass lines are locked by the same coefficient.
C6. Spherical collapse: Omega_m = 1 returns (3 pi/4)^2 = 5.5517 to 1e-5; my Delta_ta(Omega_m = 0.3153) is printed with its residual (time match) < 1e-8.
C7. nu_mono rebuild: equals nu_RAR for y <= y_p, y_p from h' = 0 (~2.54), h_mono nondecreasing, nu_mono/nu_RAR - 1 <= 3% up to y = 30, and the r_ta (B) with nu_mono vs P2 differ by < 1%.
C8. Unit sanity: r_M(1e10) = 3.86 kpc at a0 = 9.3603e-11; r_ta (A) for 1e10 = 319 kpc within 1% (an independent hand computation before the run: rho_m = 3.97e10 Msun/Mpc^3, Delta 11.8).

## Convention sweep (declared now; results are reported, none is tuned)
S1 pressure vs sigma reading. S2 r_ta: A, B(P2), B(nu_mono), B(nu_RAR). S3 edge fraction 0.31/0.40/0.48. S4 Delta_ta: mine, 11.81, EdS 5.552, and a small-radius
convention r_200c (Delta = 200 rho_crit/rho_m). S5 a0 footing: canonical / alt. S6 V_f^2 alternatives: sqrt(GMa0) [headline], V_c^2 at r_M (= sqrt2 V_f^2), and the
binding-energy-like 2x. S7 internal-energy coefficient lambda: 3/2 (headline), 1, 1/2, 3. S8 reference acceleration g_law vs g_N. S9 exchange confined to x <= x_e (edge) vs the full
x in [0.3,30]. S10 M_b in {1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14}.
Scoped-no-go test: over all (S1-S10) combinations, is there any with max_x in [0.3,30 (or <= x_e)] reaction/g_law <= 0.10 AND E_c <= (1/2) M V_f^2? Also the analytic threshold: the largest lambda
passing each line, and the largest M_b-independent edge x_e that passes both.

## MUTATE (must change the numbers; each must make the reproduction gates R1/R2 FAIL and the script exit 1)
MUTATE=1: internal-energy coefficient 3/2 -> 1 in both the reaction and the energy. Predicted: every reaction and energy number x 2/3 exactly.
MUTATE=2: the probe raises the enclosed mass of EVERY shell (M_enc = M + m for all s, not only s > q): the bilocal energy no longer depends on q, so the reaction -> 0
          (the "enclosed only" structure is the load-bearing hypothesis). Predicted: reaction 0 (R1 fails), energy unchanged (R2 holds).
Exit code: 0 if all controls and (in the main run) all reproduction gates pass; 1 otherwise (main run non-reproduction = exit 1 with the differences printed).
