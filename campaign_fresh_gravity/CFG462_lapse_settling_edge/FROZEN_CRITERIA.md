# CFG462 FROZEN CRITERIA: does the khronon lapse make settling stop at the edge nu = Omega_m/Omega_b?

Committed alone, before any script exists. kappa = 1/2 is FITTED and fixed. Both footings (a0 = 9.3603e-11 and
1.1312e-10 m/s^2) are scored separately and never pooled. No dark-matter particle is added: the cold fluid's MASS is still
required and its amount is an input. Gate G9 (no direct baryon-cold coupling) stands. No knob scans. Never "theory closed".
Offline theory + numerics only; no data, no downloads.

## The question (failure ledger 2026-10-08, top-3 item 1; CFG461's lead)

CFG461 found that the settling temperature sigma^4 = G M_b a0/4 holds exactly if a conserved cold fluid fills the law's
target and stops where the law's boost equals the cosmic matter-to-baryon ratio:
nu(y_e) = Omega_m/Omega_b = 1/f_b, f_b = 1/(1 + 5.364) = 0.157134, so
y_e = g_N/a0 = ln^2(1/(1 - f_b)) = 0.029223, total field nu(y_e) y_e a0 = 0.18597 a0,
r_edge = r_M / ln(1/(1 - f_b)) = 5.8498 r_M (point mass; r_M = sqrt(G M_b/a0)). This is CFG424's zero-knob edge.
The record's only zero-constant carrier of the local total field is the khronon lapse (CFG373 G1). CFG381: the khronon
alone gives no settling force or sink without a +1 fluid-khronon coupling.

**Test:** solve the lapse equation as committed in CFG373 with a settling cold fluid around a Hernquist baryon host
(the settled part is the law's phantom, an SIS in the deep regime) and ask whether a NO-FLUX edge for the settling fluid
appears at r_edge WITHOUT inserting a new constant or the edge by hand. Then ask whether the same field supplies the
energy sink that CFG461's contraction factors (R_vir/r_edge = 3.5 / 2.0 / 1.3 at z_c = 1, canonical) require.

## What "the lapse equation as committed in CFG373" is (copied into the script, not imported or edited)

- Leaf-elliptic (instantaneous) weak-field lapse: c^2 grad ln N = g, div g = -4 pi G_N (rho_b + rho_c), with
  G_N = G/(1 - alpha_c/2) and alpha_c <= 3.2e-9 (factor applied at the window maximum and reported; negligible).
  Spherical: g(r) = G_N [M_b(<r) + M_c(<r)]/r^2, exact.
- Mass-shell inverse g_N(g) of the kernel: P2 closed form g_N = sqrt(g^2 + a_L^2) - a_L, a_L = a0/2 (CFG373's own);
  nu_mono: the numerical inverse of y nu(y) = g/a0 (monotone; bisection).
- The lapse-local target (CFG373 G1): M_t[g](<r) = r^2 (g - g_N(g))/G, rho_t[g] = dM_t/dV.
- Kernel scored: nu_mono (FP1's committed table, read-only through CFG4_common, as CFG461 does; = 1/(1 - exp(-sqrt y))
  below y = 2.54). P2 is run as CFG373's closed-form cross-check and reported, not scored.

## Set-up (declared)

- Baryons: Hernquist, M_b(<r) = M_b r^2/(r + a)^2, M_b = 1e9, 10^10.5, 10^11.5 M_sun.
  Scored host a = 0.3 r_M (true a0); a = 1.0 r_M reported (CFG461 C2b used the same two).
- The SIS phantom: wherever the fluid is settled to the target, the lapse fixed point is the law's phantom
  M_ph(<r) = (nu(y_b) - 1) M_b(<r) (checked by control K2); in the deep regime it is the SIS of T13/CFG472.
- Domain: the galaxy's z = 0 turnaround sphere, no-flux at r_ta (matter beyond is in the Hubble flow).
  r_ta = 236 kpc (M_b/1e9 M_sun)^(1/3) (CFG118's committed z = 0 turnaround, point cores; cosmology only, a0-free).
- Two supplies of cold fluid inside the domain:
  - **CAT (scored): the record's turnaround catchment.** CFG118: M_ta = 23.6 M_b including the core, so the cold fluid
    available inside r_ta is S_cat = 22.6 M_b. This exceeds the cosmic share 5.364 M_b, as on the record (CFG424: at most
    30% of a catchment's cold fluid is used; CFG245: bound supply ~0.89 M_ph(<30 r_M)).
  - **SHARE (control, a restatement): exactly the cosmic share S = 5.364 M_b.** Initial state: CFG461's C4 toy, a
    truncated SIS at R_vir = (5/12) R_ta(M_b/f_b, z_c = 1) (formula copied).
  - Sensitivity (reported, not scored): S = 2 x 5.364 M_b.
- Why CAT is the scored supply. r_edge is BY DEFINITION the radius where the law's phantom has used up exactly the cosmic
  share (T10 S6 r_supply, Lean `supply_mass_exact`; CFG423). Any inside-out fill of exactly that supply ends there. So a
  SHARE run that lands on r_edge is the CFG423 / CFG461-R0 bookkeeping restated: it inserts the edge through the supply.
  A NO-FLUX edge, i.e. settling that STOPS, must appear at r_edge when more cold fluid is available than the share.

## Settling dynamics (declared family; all scored; none dropped after the run)

CFG373 fixes the carrier (the target) but not the settling dynamics (its G2 cites CFG245). Each flow below is a
mass-conserving Wasserstein gradient flow d_t rho_c = div(rho_c grad dF/drho_c) of a declared zero-constant mismatch
functional, with the target re-read from the lapse at every instant. A mobility D (units of time) sets only the clock;
it does not enter any equilibrium, so it does not enter the edge. D is a coupling: it is CFG381's direct fluid-khronon
coupling (+1 constant) and is reported as such (or the zero-constant t_dyn form of CFG382, which is equally irrelevant
to the edge).

- **F-H, field energy of the mismatch (H^-1):** F = (1/8 pi G) Int |grad phi|^2, lap phi = 4 pi G (rho_c - rho_t[g]).
  Spherical velocity v = D G [M_c(<r) - M_t[g](<r)]/r^2 = D [g_N(g) - g_b]. Equilibrium (KKT): M_c = min(M_t[g], S),
  self-consistent. Also time-integrated as Lagrangian shells (control K4).
- **F-2, L^2 of the density mismatch:** F = (1/2) Int (rho_c - rho_t[g])^2 dV, v = -D d_r(rho_c - rho_t[g]).
  Equilibrium: rho_c = (rho_t[g] - mu)_+, mu set by the supply (on the support the lapse fixed point reduces to the law
  applied to rho_b - mu).
- **F-KL, relative entropy (T3/T10's JKO settling):** F = Int rho_c ln(rho_c/rho_t[g]) dV, v = -D d_r ln(rho_c/rho_t[g]).
  Equilibrium: rho_c = lambda rho_t[g] on the domain, lambda set by the supply.
- **F-0, the linearised chassis as committed (no settling term; CFG381):** the fluid feels only gravity and stays in its
  virialised state. Edge = its initial support (R_vir for SHARE, r_ta for CAT).

Edge r_e := the outer boundary of the equilibrium support of rho_c (rho_c > 1e-6 rho_t[g]); the domain boundary r_ta if
the support fills the domain.

## Gates (per flow)

- **P1 (edge, the user's line):** |log10(r_e/r_edge)| <= 0.05 for all 3 masses x 2 footings, CAT supply, a = 0.3 r_M,
  nu_mono, r_edge = 5.8498 r_M(true a0).
- **P2 (no new constant):** nothing beyond kappa (a0), G, f_b / the cosmic share, the cosmological catchment and the
  baryon profile enters the edge. Any constant or threshold that had to be chosen to place the edge is a FAIL of this
  gate and its value is reported. (The mobility D is reported as a coupling; it is checked not to move the edge.)
- **P3 (MUTATE, `CFG462_MUTATE=1`):** a0 -> 2 a0 inside the lapse (kernel argument and a_L) for every flow; the baryon
  host scale a and the catchment stay at their true values; edges scored against the TRUE r_edge. Predicted shift of
  an edge that tracks r_M: log10(2^-1/2) = -0.1505 dex. A flow that passes P1 must move by -0.1505 +- 0.05 dex (and
  therefore fail P1 under MUTATE); a flow whose edge does not move under MUTATE is not keyed to the law.
- **Reported, load-bearing for the reading (not extra gates):**
  - L (locality / G9): can the flow's drive be computed from the lapse g and the fluid's own LOCAL state alone, or does
    it need the baryons' own Newtonian field g_b separately (a baryon-keyed, nonlocal signal: the CFG60/CFG473 class)?
  - f_b-test (the analogue of CFG461's c-test): change f_b by x1.2 wherever it enters each mechanism (supply included)
    and report d ln y_e / d ln f_b. A genuine nu = Omega_m/Omega_b edge needs 2.181 (nu_mono, point mass).
  - Edge-state flux: the configuration settled exactly to r_edge (law target inside) plus the CAT remainder spread at
    uniform mu = r^2 rho over [r_edge, r_ta] (tanh step of width 0.02 dex in log r). Report the sign of each flow's mass
    flux across 1.0 and 1.1 r_edge and rho_t[g]/rho_c just outside r_edge. A no-flux edge needs zero flux there.

## Energy sink (the second question; frozen line)

- Required: the energy the cold fluid must shed to settle from the virialised state to the edge-settled state, two ways:
  (a) CFG461's truncated-SIS toy (copied): Delta E = (G M_tot^2/4)(1/r_edge - 1/R_vir), M_tot = M_b/f_b, z_c = 1
  (z_c = 3 reported: the massive end must EXPAND, so the sink is negative there);
  (b) virial: Delta E = (W_i - W_f)/2 with W = -Int G M(<r) dM/r of baryons + cold, initial = Hernquist + truncated SIS
  (share) at R_vir(z_c = 1), final = the F-H/SHARE equilibrium (a = 0.3 r_M).
- Capacity of the same field, three channels:
  (i) the lapse constraint itself: in the weak field its field energy (1/8 pi G) Int |g|^2 dV equals |W| (sympy, K5), so
  it is the energy SOURCE of the contraction, not a sink: capacity 0 by identity;
  (ii) the static alpha_c channel: capacity <= (alpha_c/2)|Delta W| = alpha_c Delta E, alpha_c <= 3.2e-9 (L340 window);
  (iii) the c_2 K^2 channel with CFG381's derived induced expansion K = 2 (alpha_c/c_2)(V_f/c)^2 Gamma/c (formula
  copied): capacity c_2 c^4 K^2 Vol(R_vir)/(16 pi G) x max(1, Gamma t_H), Gamma = 3.21 H_Lambda (CFG370) and 1/t_H,
  over the window alpha_c in (9.62e-14, 3.2e-9), c_2 in (7.29e-3, 0.0667).
- **SINK SUPPLIED** iff some channel's capacity/required >= 1 in all 6 cells (z_c = 1). Otherwise **NOT SUPPLIED**; then
  report the direct fluid-khronon coupling the sink needs (CFG381's +1 constant) as the required enhancement of K over
  the gravitationally induced K, per galaxy (value and spread).

## Controls (load-bearing; the main run exits 0 only if all pass)

- **K1 (sympy, copied CFG373 identities):** P2 perfect square g^2 + a_L^2 = (g_N + a_L)^2; the point-mass local target
  equals CFG44's M(sqrt(1 + x^2) - 1); the AQUAL flux identity. Plus the nu_mono inverse round trip, max relative error
  <= 1e-9 on y in [1e-5, 1e5].
- **K2 (the carrier on an extended host):** with unlimited supply the self-consistent fixed point M_c = M_t[g] (iterated
  from M_c = 0) reproduces the law's M_ph(<r) for the Hernquist host to <= 1e-6 relative on [0.05, 50] r_M, both kernels.
- **K3 (restatement control: the gate can pass):** F-H with exactly the cosmic share: point-mass host edge = 5.8498 r_M
  to 1e-3 relative; Hernquist a = 0.3 r_M edge within 0.05 dex of r_edge in all 6 cells.
- **K4 (dynamic solver):** the Lagrangian time integration of F-H (middle galaxy, canonical, CAT supply, uniform-mu
  start over [0.01 r_M, r_ta]) converges to the F-H equilibrium edge within 0.01 dex, with M_c(<r) within 1% of it on
  [0.1, 0.9] r_e.
- **K5 (sympy):** for a bounded spherical mass (truncated SIS) (1/8 pi G) Int_0^inf |g|^2 4 pi r^2 dr = -W.

## Verdicts

- **LAPSE NO-FLUX EDGE FOUND:** some flow passes P1, P2 and P3 (and its L flag is reported).
- **EXHAUSTION ONLY (FAIL):** no flow passes P1 with the CAT supply, and the edge appears only as the exhaustion radius of
  exactly the cosmic share (K3): CFG423 / T10-S6 bookkeeping, not a lapse no-flux boundary.
- **NO EDGE (FAIL):** neither.
- Sink: SUPPLIED / NOT SUPPLIED as above.
- MUTATE run: exits 1 when the teeth are detected: the K3 control edge moves by -0.1505 +- 0.02 dex and fails P1 against
  the true r_edge, and no flow passes P1.

**Expected before running (stated so a fail is not manufactured after the fact):** the CFG373 lapse system contains
{G, a0, kernel} and no f_b, so no lapse-local criterion can place an edge at y_e(f_b); f_b enters only through the supply.
I expect EXHAUSTION ONLY: F-H lands on r_edge only with the SHARE supply, and with CAT its edge moves out to where
M_ph = 22.6 M_b (~23 r_M); F-KL fills the domain; F-2 lands off r_edge; F-0 does not move. I expect NOT SUPPLIED for the
sink (CFG381). If the numbers say otherwise, the numbers win.

Local compute only. Outputs: script, .out, _MUTATE.out, results JSON (both modes), README. Commit locally; do not push.
