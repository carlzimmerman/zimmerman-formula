# CFG489 FROZEN CRITERIA: NC1's decisive tests (GR + Lambda chassis, MOND only in the cold fluid)

Frozen 2026-10-08, before any CFG489 script exists. Nothing below may be edited after the commit that adds this file;
corrections go in a dated section appended at the end.

Theory plus offline numerics. No downloads. Every other lane is read-only. kappa = 1/2 is FITTED. Both a0 footings
(canonical 9.3603e-11, alt 1.1312e-10 m/s^2) are run wherever a0 enters a number, never pooled. No dark-matter particle
species is added; the cold fluid's mass is still required and its amount (Omega_c/Omega_b = 5.364) is an input. Nothing
here says "theory closed". Untested is not passed.

## 0. The question, and disclosure

CFG484 (f46275103) named NC1 its top new candidate: gravity is exactly GR + Lambda; the cold fluid relaxes, by a
dissipative (non-Lagrangian) law, toward the target rho_t[A] = div[F(|A|) A_hat] / 4 pi G, where A is the fluid's OWN
4-acceleration and F(g) = g - g_N(g) inverts the declared kernel (g = nu(g_N/a0) g_N). CFG484 left open G1 (fluid-sector
well-posedness), H3 (attractor and support), the energy supply, and G14 (capture by an embedded point mass). CFG489 runs
those four tests, in order.

**Not blind.** CFG484, CFG44, CFG373, CFG461, CFG462, CFG464, CFG472, CFG473, CFG475 and CFG487 were read first. Before
writing this file I sketched the linear dispersion relation by hand (section 2's tau = 0 closed form and the A-hyd
k^4 / k^(4/3) growth). Expectations, stated now so that they cannot be tuned toward:
- (1) PASS for the scored member (A = true 4-acceleration, positive relaxation); the A-hyd variant ill-posed;
- (2) likely FAIL: the deep-regime target is nearly degenerate (stiffness ~ g/a0) and the support temperature is set by
  the collapse, not the law (CFG461, CFG472);
- (3) likely FAIL: CFG461/CFG462 put the needed energy change at 2.50 / 0.97 / 0.34 virial binding energies;
- (4) PASS under the local-density relaxation time, FAIL under an orbital relaxation time.

## 1. The NC1 relaxation system (fixed)

Newtonian limit of GR + Lambda (Lambda negligible on galaxy scales; GR corrections <= 3e-4 for M_b <= 1e12, CFG44).
Baryons are a static host (fixed profile). Cold fluid: continuity, momentum, internal energy, ideal gas gamma = 5/3
(the Jeans-fluid closure; NC1 needs a collisional fluid, because each particle of a collisionless medium is in free fall
and has A = 0; this is stated as a requirement, not tested).

    d rho/dt + div(rho v) = 0
    rho Dv/Dt = -rho grad Phi - grad(P + p_s) [+ shock viscosity q]
    De/Dt = -(P + q)/rho div v        [reservoir form, scored in (2)]
    De/Dt = -(P + q + p_s)/rho div v  [energy-conserving form "EC", reported in (2), used in (3)]
    lap Phi = 4 pi G (rho + rho_b)
    A = Dv/Dt + grad Phi = -grad(P + p_s + q)/rho     (A-kin: the TRUE 4-acceleration, Newtonian limit)
    rho_t = div[ F(|A|) A_hat ] / 4 pi G,  F(g) = g - g_N(g)

Members (fixed now; ONE is scored):
- **M1 (scored): relaxing settling stress, L2 mismatch at the fluid's own temperature.**
  tau Dp_s/Dt = -(p_s - p_eq),  p_eq = s (P/rho)(rho - rho_t),  s = +1,
  tau = 1/sqrt(4 pi G rho_m), rho_m = the LOCAL total matter density (cold fluid + baryons at that point), lambda = 1
  (CFG464 / CFG487's zero-constant t_dyn convention). Target read from A-kin.
- M2 (reported): M1's instantaneous limit tau -> 0 (p_s = p_eq, an implicit solve each instant).
- M3 (reported): CFG462's F-H flow made inertial: radial force per unit mass f = s G (M_c(<r) - M_t(<r)) / r^2
  (3-D form: force -grad chi, lap chi = -4 pi G s (rho - rho_t)), instantaneous, A-kin includes f. NONLOCAL: it needs
  the fluid's own enclosed mass (a fluid-sourced elliptic field; CFG462's G9 tension). It cannot make NC1 ALIVE.
- A-hyd variants of M1 and M2 (reported, step (1) only): the target read from -grad(P)/rho alone (the settling stress
  excluded from A). This is not NC1's definition; it shows what the self-consistent reading does.
- KL form p_eq = s P ln(rho/rho_t): linearises identically to M1; not run in 1-D (rho_t <= 0 occurs). Stated only.
- Kernel: nu_mono (the record's FP1 monotone repair, CFG44 Bcommon) scored; P2 reported.

Constants: chassis 0. Fluid sector: lambda = 1 (zero-constant), s = +1 and gamma = 5/3 are structural (not tuned, never
scanned), the shock viscosity is numerical. No other constant. kappa fitted; 5.364 input.

## 2. Step (1), G1 well-posedness (dispersion relation)

Linearise about a static state at the target (p_s0 = 0), plane wave exp(i(k.x - w t)), longitudinal. Background enters
only through n = k_hat.N.k_hat, N = g_N'(g0) r_hat r_hat + (g_N(g0)/g0)(I - r_hat r_hat); sigma^2 = P0/rho0;
c_s^2 = gamma sigma^2 (adiabatic; isothermal c_s^2 = sigma^2 reported); w_J^2 = 4 pi G rho0. M1 gives the cubic

    (w^2 + w_J^2 - c_s^2 k^2)(1 + B - i w tau) - k^2 C = 0,
    B = s sigma^2 (1 - n) k^2 / w_J^2,  C = s sigma^2 [1 - (1 - n) c_s^2 k^2 / w_J^2],

whose tau = 0 limit is w^2 = w_J^2 [(c_s^2 + s sigma^2 n) k^2 - w_J^2] / (w_J^2 + s sigma^2 (1 - n) k^2). sympy derives
the cubic from the linear system (control K2).

Backgrounds:
- (a) homogeneous (Jeans swindle): A0 = 0, so n = 0; units w_J = 1, sigma = 1, tau = 1/w_J.
- (b) deep-MOND SIS, sigma^2 = V_f^2/2: rho0 = V_f^2/(4 pi G r^2), g0 = V_f^2/r, w_J = V_f/r, tau = r/V_f, at
  x = r/r_M in {3, 5.85, 10, 30, 100}; theta (k vs r_hat) in {0, pi/4, pi/2}; both kernels (n from g0/a0 = 1/x). WKB
  is taken as valid for k r >= 3; smaller k r is printed but not scored.
- (c) reported sweep over all frozen coefficients: n in {0, 0.01, 0.1, 0.5, 0.9, 0.99}, w_J tau in {0.1, 1, 10},
  c_s^2/sigma^2 in {1, 5/3}.

k grid: 2401 log points spanning 12 decades (k sigma/w_J from 1e-4 to 1e8). G(k) = max Im w over the roots.

**PASS line (Petrovskii / Hadamard), per background, angle, kernel:** all three of
- (P-a) the coefficient of the highest time derivative never vanishes for k > 0 (for tau = 0 forms: 1 + B, or
  1 + s(1 - n) for M3, keeps its sign);
- (P-b) sup_k G(k) <= 2 w_ref, w_ref = max(w_J, 1/tau);
- (P-c) no growth that rises with k at the top of the grid: G(k_max) <= G(k_max/100) + 1e-9 w_ref.

Step (1) PASS iff M1 passes on (a) and on every (b) cell (both kernels, both c_s choices, all angles, all x).

Reported alongside, not in the PASS line:
- the high-k character of each member (hyperbolic, or parabolic damping ~ k^2);
- relativistic causality: a parabolic mode has unbounded signal speed in the Newtonian limit, so a covariant version
  needs a second-order (Israel-Stewart / BDNK-type) regulator. Its status is COND, never PASS here.

The footings do not enter (1) in units of r_M; this is said, not run twice.

## 3. Step (2), H3 attractor (spherical 1-D time evolution)

Code: 1-D spherical Lagrangian hydro (C core compiled at run time into a temporary directory, called through ctypes;
CFG118's convention). N = 240 shells (scored), geometric in enclosed fluid mass from 2e-4 M_b to 5.364 M_b. Reflecting
wall at r_w = 0.02 r_M (no fluid inside; M_t at the wall set to 0). Free outer surface (P = p_s = 0 outside). Staggered
leapfrog, energy updated with time-centred pressure; von Neumann-Richtmyer + linear shock viscosity (C2 = 2, C1 = 0.3);
CFL 0.25 using c_eff^2 = gamma sigma^2 + |s| sigma^2 (1 + |rho_t|/rho). p_s is advanced semi-implicitly: its
dependence on itself through A-kin is linearised and solved as a tridiagonal system each step, with the exact
exponential relaxation factor exp(-dt/tau). M2 uses the same solve with the factor set to 0. M3 solves its pointwise
implicit A each step.

Units: G = M_b = a0 (true footing) = 1, so r_M = 1, V_f = 1. The footing and M_b enter only through R_ta / r_M.

Hosts (static baryons):
- point mass, M_b in {1e9, 1e10, 1e11, 1e12} Msun, both footings (8 cells);
- CFG473's compactness family: Hernquist M_b(<r) = M r^2/(r + a)^2, a/r_M in {0.1, 0.3, 1, 3}, at M_b = 1e10, both
  footings (8 cells);
- CFG44's far-shell test: (A) exponential sphere M_b = 1e10, h = 2 kpc; (B) the same plus a baryon shell of 10 M_b at
  R' = 40 kpc, tanh width 0.5 kpc (CFG44 B3), converted to r_M units per footing (4 cells). The cold supply is 5.364 x
  the CORE's baryons in both A and B (the shell brings no cold fluid; declared).

Initial state ("cosmic-share infall"): cold fluid of mass 5.364 M_b, uniform inside R_ta, at rest, e0 = 1e-4 V_f^2.
R_ta is CFG461's C4 turnaround radius for M_tot = M_b / f_b, f_b = 1/6.364, collapse at z_c = 1 (EdS turnaround
density (9 pi^2/16) Omega_m rho_crit0 (2^(2/3)(1 + z_c))^3, H0 = 67.4, Omega_m = 0.315). Baryons sit in their final
profile from t = 0 (declared simplification).

Run length: t_end = t_coll + 40 t_e, t_coll = (pi/2) sqrt(R_ta^3 / (2 G M_tot)), t_e = r_e / V_f, where r_e is the
supply edge: the radius at which the law's phantom mass r^2 (g_law - g_N)/G equals 5.364 M_b for that host.

Metric: V_c(x) = sqrt(G (M_b(<r) + M_c(<r)) / r) on 60 log points in x in [0.1, x_e], time-averaged over the 5 t_e
before the scoring time; V_law = sqrt(r nu(g_N/a0) g_N) with the host's M_b(<r) and the true a0.
D = max_x |log10(V_c / V_law)|. D is computed at t_coll + 10, + 20 and + 40 t_e (D10, D20, D40); D40 is scored.
Also reported: D on [0.1, 0.9 x_e].

Cell PASS iff: not crashed (no NaN, no shell inversion, dt >= 1e-9, steps <= 4e7), settled (|D40 - D20| <= 0.02),
and D40 <= 0.05 dex.

**Step (2) PASS iff every scored cell passes (8 point-mass + 8 compactness + 4 far-shell) with M1 + nu_mono, AND the
far-shell pair agrees inside: max |log10(V_c,A / V_c,B)| <= 0.05 over x in [0.1, min(x_e, 0.9 R'/r_M)], both footings.**

Reported (not scored): the P2 kernel on the 8 point-mass cells; M2, M3 and the EC form on the point-mass cells (EC also
on all scored hosts, for step (3)); a pure-hydro baseline (s = 0) on the 1e10 canonical point mass.

Resolution: the 1e10 canonical point-mass cell is re-run at N = 480. If |D40(480) - D40(240)| > 0.02 the step-(2)
verdict carries the label NOT CONVERGED (and cannot be PASS).

## 4. Step (3), H3 energy (support from settling heat, no external sink)

- (3a) Static budget. E_t = energy of the target state (cold fluid at rho_t inside r_e, hydrostatic thermal support
  with P(r_e) = 0, at rest): thermal (3/2) Int P dV + self-gravity + interaction with the fixed baryons. E_i = energy of
  the initial state (cold uniform sphere at R_ta, at rest). Without a sink the fluid's energy is conserved, so the
  target is reachable only if E_t = E_i. PASS iff |E_t - E_i| <= 0.1 |E_t| in every scored host cell (20).
- (3b) Dynamic. In the scored (2) runs (reservoir form), W_res = the cumulative work the settling stress put into the
  fluid (the energy an external reservoir must supply or absorb). PASS iff |W_res| <= 0.1 |E_t| in every scored cell.
- (3c) Reported: the EC runs (the settling stress's work drawn from the fluid's own heat): D40, whether e reached its
  floor (heat exhausted), the energy-conservation error, and the settling stress's entropy production
  Sum(-p_s dV / T) (negative = second-law violation).
- Compared, not scored: CFG461/462's (R_vir/r_e - 1) = 2.50 / 0.97 / 0.34 virial binding energies.

**Step (3) PASS iff (3a) and (3b) pass.**

## 5. Step (4), G14 capture by the embedded Sun

Inputs as CFG484 N1d: Milky Way P2 point-mass law, M_b = 6e10 Msun, R0 = 8.2 kpc, host fluid density and
sigma = V_c(R0)/sqrt 2 per footing; v_rel = 230 km/s; GM_sun; Mars 1.523679 AU, Saturn 9.5826 AU; ephemeris bounds
1.4e-15 / 7.0e-15 m/s^2 (LIT, provisional, as CFG484).

- (4a) Liouville cap on fluid bound to the Sun (non-dissipative capture): reproduce CFG484 R1. PASS iff the anomaly is
  <= 0.1 x the bound at Mars and Saturn, both footings.
- (4b) Relaxation-limited build-up during transit (scored relaxation time). Upper bound: the target near the Sun is
  taken as the Sun's OWN nu_mono target (CFG484 R2, the largest the fluid's A could ask for). The fluid crosses radius r
  in t_res = 2 r / v_rel; tau = 1/sqrt(4 pi G rho_m) with rho_m the local matter density = the host fluid density (the
  Sun's mass is not local density outside the Sun). The achieved fraction of the Sun's target is bounded by
      f(r) = 3 (2 r/(v_rel tau)) [1 + (4/3)(sigma^2/v_rel^2)(1 + ln(R_far/r))],  R_far = sqrt(GM_sun / g_host),
  g_host = V_c(R0)^2/R0 (the factor 3 is a declared safety margin over the linear estimate). Anomaly = f(r) x the R2
  anomaly. PASS iff <= 0.1 x the bound at Mars and Saturn, both footings. P2 reported.
- (4c) Bracket (decides PASS vs COND): the orbital relaxation-time reading, rho_orb = V_kep(r)^2/(4 pi G r^2) (the
  CFG464 ledger formula applied at r), f = min(1, the same formula). Reported number, used only for the label.
- (4d) Reported: the Bondi-Hoyle-Lyttleton radius and the mass accreted over 4.6 Gyr.

**Step (4) = PASS iff (4a), (4b) and (4c) all pass; COND iff (4a) and (4b) pass and (4c) fails; FAIL iff (4a) or (4b)
fails.**

## 6. Verdict (fixed)

- **NC1 DEAD** if step (1) or step (2) FAILS (or (2) is NOT CONVERGED). The chassis question then returns to CFG484's
  runner-up R04 (C-H/K + Horava UV sector M_*), whose decisive test is CFG319's moving-black-hole count redone with the
  z = 3 Horava terms at the universal horizon.
- **NC1 ALIVE** if steps (1) and (2) PASS.
- **NC1 FULL PASS** if ALIVE and steps (3) and (4) PASS. ALIVE with (4) COND is reported as "ALIVE, G14 COND".

Only member M1 decides. If another member passes where M1 fails, that is reported as a lead for a new lane, never as
this lane's verdict.

## 7. Controls

Load-bearing (main exits 0 iff all pass):
- K1 (sympy): for ds^2 = -(1 + 2 Phi) dt^2 + (1 - 2 Phi) dx^2 and u = gamma(1, v), the 4-acceleration's spatial part
  equals dv/dt + (v.grad) v + grad Phi up to second-order small terms (Phi v, v^2 grad Phi, v dPhi/dt).
- K2 (sympy): the M1 cubic follows from the linear system; its tau = 0 limit equals the closed form; s = 0 gives Jeans.
- K3: g_N'(g) and g_N(g)/g lie in (0, 1) for g in [1e-8, 1e8] a0 (nu_mono and P2), so n is in (0, 1) for every
  background.
- K4: the C core's target routine at static A = g_law reproduces the P2 point-mass cold mass M (sqrt(1 + x^2) - 1)
  to <= 1e-6 relative on x in [0.1, 10]; the nu_mono point-mass supply edge x_e = 5.8498 +- 0.001.
- K5: CFG461's contraction factors R_vir/r_e = 3.50 / 1.97 / 1.34 (log M_b = 9 / 10.5 / 11.5, canonical, z_c = 1),
  with R_vir = (5/12) R_ta and r_e = r_M / ln(1/(1 - f_b)), to 1%.
- K6: CFG484 N1d reproduces from its committed JSON: R1 Liouville ratios (Mars, Saturn) and R2 nu_mono ratios, both
  footings, to 1%.
- C-static: start exactly at the target (discrete hydrostatic support, P(r_e) = 0, p_s = 0) for the 1e10 canonical
  point mass and Hernquist a = 1; after 20 t_e, D <= 0.01 and max |v| <= 0.01 V_f.
- C-energy: the EC run of the 1e10 canonical point mass conserves total energy to <= 2e-3 |E_t|.

Reported diagnostics: C-heat / C-cool (the exact target state with e scaled by 1.2 / 0.8, run 20 t_e with M1: the
residual D measures the target's grip against a wrong temperature); the pure-hydro baseline; the resolution re-run.

## 8. MUTATE (`CFG489_MUTATE=1`)

- MA (anti-relaxation, s = -1) in step (1), every member and background: M1 must FAIL the PASS line. The check "step (1)
  PASS for the scored member under MA" is printed and must fail, so the MUTATE run exits 1.
- MA-1D: one 1-D run (1e10 canonical point mass) with s = -1, reported (expected to crash or blow up).
- MB (target a0 -> 2 a0 inside F; the scoring law stays at the true a0) on the 8 point-mass cells. Reported: D against
  the true law, D against the 2 a0 law, and the attractor shift Delta(x) = log V_c(MB) - log V_c(main) against the
  predicted Delta_law(x) = log V_law(2 a0) - log V_law(a0) over x in [1, min x_e]. "Moves as predicted" iff
  rms(Delta - Delta_law) <= 0.02 dex and the mean shift has the predicted sign and at least half its size. If the main
  step (2) PASSES, MB must give D > 0.05 against the true law (teeth); if the main FAILS, MB says whether the
  equilibrium tracks the target's a0 at all.
- Outputs carry the _MUTATE tag and never overwrite the main outputs.

## 9. Outputs

`cfg489_nc1.py`, `cfg489_core.c`, `cfg489_nc1.out`, `cfg489_results.json`, `cfg489_nc1_MUTATE.out`,
`cfg489_results_MUTATE.json`, `README.md` (plain: the four verdicts, the constant count, what failed and why).
git add only this folder; commit locally; do not push. No names or home paths in committed files.

## 10. What this lane cannot say

It tests one declared relaxation law (and reports three relatives). A FAIL kills this NC1 member and, by the frozen
rule, NC1 as CFG484 posed it; it does not exclude every conceivable fluid dynamics. A PASS would not derive kappa, the
amount 5.364, or the switch (H4 is not tested here). Spherical, static baryons, Newtonian limit, one collapse redshift.
It says nothing about data favouring the framework.

## Correction 1 (2026-10-08, after run 2; appended, nothing above edited)

**Numerics only.** The physics, members, hosts, initial states, run lengths, metric, pass lines, verdict rules, controls
and MUTATE are unchanged.

What changes in the 1-D code (section 3):
- (a) Wall: r_w = 0.02 -> 0.05 r_M (half the inner scored radius 0.1).
- (b) Target at the wall: M_t,0 = 0 -> r_w^2 F(g_wall), the wall's own 4-acceleration. An inert core holds the law's
  target phantom inside the wall, M_core = M_ph(<r_w) (2.0e-3 M_b for the nu_mono point mass, 1.4e-3 for Hernquist
  a = 1). It is counted in gravity and in V_c. The dynamic supply is 5.364 - M_core, so the total is still 5.364 M_b.
- (c) Shell masses: "geometric in enclosed mass from 2e-4 M_b" -> smooth geometric shell masses (one constant
  neighbour ratio). The first shell is 2e-4 M_b at N = 240 and 1e-4 M_b at N = 480.
- (d) Step cap: 4e7 -> 2e8. This is a resource limit only.

Why:
- Run 2 used the frozen numerics. It failed the load-bearing control C-static: the exact Hernquist a = 1 target state
  crashed at t = 0.25 (dt < 1e-9).
- The failure is a grid-scale sawtooth at shells 2-3, next to the first shell. In the frozen grid that shell carries
  23 times its neighbour's mass. With M_t,0 = 0 it is also given a target it can never meet: the law's phantom inside the
  wall (3.4e-4 M_b for nu_mono) exceeds the 2e-4 M_b shell.
- Every scored cell of run 2 crashed at t = 0.3 to 2, in the same place. So run 2 cannot separate the physics from the
  discretisation.

Tests made after run 2 (not frozen):
- Halving the CFL, or doubling N, changes the crash.
- The smooth grid with the consistent wall holds the exact target state: C-static D = 2.5e-4 (point mass) and 2.7e-4
  (Hernquist a = 1) over 2 t_e. The frozen numerics reproduce run 2's crash exactly.

**Disclosed:** before writing this correction, the corrected numerics were run once on one scored cell, the 1e10
canonical point mass with M1. It completed: D10/20/40 = 0.185 / 0.178 / 0.180. The correction was chosen so that
C-static passes, not to move D.

### Readings applied to cases the text did not foresee

- **C-energy:** an EC run that crashed cannot certify energy conservation, so the check fails.
- **Resolution rule:** if the N = 240 and N = 480 runs both crash, the outcome is resolution-consistent.
- **(3b):** the W_res of a crashed scored run is untested, not passed.

### Operational

- Run 1 was terminated (SIGTERM, on a shared machine) before it wrote any outputs; its log is kept.
- Runs 2 and later ran under `nice -n 15` with 4 workers and 1 BLAS thread, at the coordinator's request.
- K3 is now computed in cancellation-free form. Run 1 showed P2's g_N' rounding to 1.0 at g = 1e8 a0 (a float artefact).
  The identity and the pass line are unchanged.

None of these changes the physics.
