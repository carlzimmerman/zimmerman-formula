# CFG541 FROZEN CRITERIA -- the cold-energy equations of motion made precise (class A of CFG539)

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-09.

## Scope and settings

CFG539 Stage 1 (criteria 12f575de1, results 6f0ddbf42) left one dissipative survivor, class A (overdamped settling flow), with
open items: the edge T2 INHERITED, the energy sink NOT SUPPLIED, causality COND, and a coefficient fixed by the "lambda = 1
convention" (CFG489). This lane writes class A as a complete, precise system and tests the open items analytically (sympy) and with
small 1-D spherical numerics. NO PM runs. Nothing in `CFG539_cold_energy_equation_of_motion/` is edited (read-only; its Stage 2
runs are a separate job). Other lanes are read or imported read-only.

Settings: kappa = 1/2 FITTED; footings 9.3603e-11 (can) and 1.1312e-10 (alt), judged separately, never pooled; kernel
nu(y) = 1/(1 - exp(-sqrt y)); candidate B (law inside bound systems via f_sw); no EFE (R7); G9 (matter conservation; cold
energy feels baryons only through gravity); Omega_c/Omega_b = 5.364 (engine f_b = 0.02237/0.14237); round rule (CFG516) vs
QUMOND phantom. No dark-matter particle species. The cold energy's MASS is still required. Not "theory closed". No downloads.
Compute: `nice -n 10`, <= 2 threads.

**No knobs.** Every constant must be one of kappa, 5.364/f_b, G, c, rho_DE (through a0), or an INHERITED item listed by name
with its source lane. Any timescale must be built from G and a local density (or H, a0, c). A dimensionless O(1) factor that
the equations do not fix is reported as FREE, never tuned.

## Deliverables

`EQUATIONS.md` (the system), `cfg541.py` (sympy + 1-D numerics; writes `cfg541.out`, `cfg541_results.json`;
`CFG541_MUTATE=1` writes `cfg541_MUTATE.out`, `cfg541_results_MUTATE.json`), `README.md`.

## Declared models (inputs, not fitted)

- **1-D spherical drift model.** Baryons static. The cold energy starts at rest, uniform (top-hat) inside the turnaround radius
  r_ta, holding the cosmic ratio: M_cat = (1 - f_b)/f_b x M_b,now/f_ret (= (1 - f_b) M_ta with M_ta = M_b,now/(f_ret f_b)),
  r_ta from M_ta = (4 pi/3) r_ta^3 Delta_ta(z=0) rho_m,bar (Delta_ta from the spherical-collapse ODE in flat LCDM, Omega_m from
  the engine's omega_b + omega_c, h = 0.674; background only). f_ret = CFG515 `fret_census` (imported read-only). Only the
  drift sub-flow is integrated (v_orb off): this is the Lyapunov/steady-state part of class A, not the full kinetic system.
  Finite-volume, log-r grid (400 cells, inner edge 1e-3 r_M for point masses, 1e-2 a for Hernquist), donor-cell fluxes,
  mobility zero outside r_ta, exact mass conservation; step limited by CFL 0.4 and Gamma dt <= 0.2.
- **Systems.** MW-like: M_b,now = 6.0e10 Msun, point mass and Hernquist a = 2.5 kpc (illustrative). Group-like: the median
  (log M_b, Re) of CFG540's 63 Tian+26 groups (data read from the local VizieR file CFG540 already used), Hernquist
  a = Re/1.8153. Cluster-like (energy upper bound only): point mass M_b,now = 1.5e14 Msun.
- **Group sample (item T2b).** All 63 CFG540 groups, CFG540's estimator imported read-only (Hernquist, aperture infinity,
  beta = 0, round rule), with the edge replaced by the class-A exhaustion radius (below).

## Items, each with its rule

### E1 -- EQUATIONS.md (task 1)
Contents required: every field with definition and SI units; the baryon Vlasov-Poisson part; the cold-energy kinetic equation
(Vlasov + velocity-independent drift advection); the deficit, psi and its boundary conditions; f_sw and catch defined from the
fields; round vs QUMOND; what is conserved (mass; energy) and the energy-change rate; every constant with its origin.
Label: **FULLY SPECIFIED** if every quantity is defined from the state and no item is open; **SPECIFIED WITH OPEN ITEMS**
(listed) if defined but some items are open; **INCONSISTENT** if the dimensional audit (D1) fails, or mass is not conserved,
or two equations require incompatible stationary states.

### V -- variational origin (task 2)
- V1 (sympy, discrete model): with d = s max(rho_ph - rho_c, 0) and F = (1/8 pi G) int |grad psi|^2 = -(1/2) int psi d, the
  first variation is dF/drho_c = s psi on {d > 0} and the interval [s psi, 0] on {d = 0, s > 0}, {0} where s = 0. PASS if
  sympy confirms on a 3-5 cell model.
- V2 (gradient-flow test): a drift v = -tau grad mu is a gradient (Wasserstein/Onsager) flow of F only if mu is a selection of
  dF/drho_c, equivalently the response matrix dmu_i/drho_j is symmetric on the mobile set. Evaluate on a discrete model for
  (a) the VARIATIONAL form: s = f_sw x catch (no census edge), mobility rho_c tau on s; (b) CFG539's COMMITTED form: deficit
  confined by the edge, mobility on the whole catchment. Label each IS / IS NOT a gradient flow.
- V3 (Lyapunov): for the form(s) that ARE gradient flows, dF/dt = -int rho_c tau |grad psi|^2 <= 0 (sympy identity with no
  boundary term), and numerically in the 1-D model: max over steps of (F_{n+1} - F_n)/F_0 <= 1e-9. PASS/FAIL.
- V4 (minimiser): the minimiser of F at fixed catchment mass is the inside-out fill (filled core, empty shell): KKT holds with
  lambda = psi(r_*) (sympy/numerical check on the 1-D steady state: max KKT violation <= 1e-6 of max|psi|). And the 1-D flow's
  steady state matches the analytic inside-out fill: |r_*,flow/r_*,analytic - 1| <= 0.01. PASS/FAIL.
- V5 (coefficient): mobility tau = alpha (4 pi G rho_m)^(-1/2). Stationary states independent of alpha (sympy: the stationary
  condition contains no tau; numerics: settled-mass profiles at alpha = 0.5, 1, 2 agree to 1e-3 in M_c(<r)/M_cat). Label:
  **COEFFICIENT FIXED** only if the variational structure determines alpha (an argument, not a convention); otherwise
  **O(1) FREE** with the robustness requirement stated and evaluated: t_90 (time to 90% of the steady-state settled mass) for
  alpha = 0.5 below 10 Gyr in both MW-like and group-like models on both footings -> **ROBUST (idealised)**; else
  **RATE-SENSITIVE**.

### T2 -- the edge (task 3)
- T2a: run the 1-D variational flow (no census edge in s) with the turnaround catchment for point masses (MW-like and group-like
  masses, both footings). r_*,flow = outermost face with rho_c/rho_ph >= 0.5 at steady state. Label **EMERGENT** if
  |r_*,flow / r_census - 1| <= 0.01 in every cell, r_census = r_M/ln(1 + f_ret f_b/(1 - f_b)), AND the fill is inside-out
  (the front radius is non-decreasing in time). **INHERITED** otherwise, naming what is missing. The inputs the emergent edge
  still needs (catchment = turnaround sphere at the cosmic ratio; for observed systems, M_ta inferred through the census f_ret)
  are listed as INHERITED INPUTS in either case.
- T2b (groups): for each CFG540 group the class-A edge is the exhaustion radius of the Hernquist phantom,
  M_ph(<r_*) = 5.364 M_b/f_ret (census f_ret). Report median r_*/Re and the class mean Delta = log sigma_obs - log sigma_pred (can,
  alt). Rule: **PROBLEM PERSISTS** if mean Delta (can) >= +0.063 (3 x CFG540's SE 0.021); **RESOLVED** if |mean Delta| < 0.042;
  **REDUCED** otherwise. Also report the supply multiple that would bring the group mean to |Delta| < 0.042 (bracket scan of a
  supply factor, report only; not a fit adopted anywhere).

### S -- energy sink (task 4)
- S0: per unit settled mass, Delta W/M_cat (gravitational energy released, initial top-hat at rest -> final steady state) and
  E_sink/M_cat = (W_i - W_f - K_f)/M_cat, K_f = the isotropic Jeans kinetic energy the settled profile needs to be a collisionless
  equilibrium in the final field; in km^2/s^2 and in units of V_f^2 = sqrt(G M_b a0). Also Delta F (the deficit field energy) for
  comparison. MW-like and group-like (Hernquist), both footings; cluster-like (point) for the upper bound.
- S(i) heat in the cold energy: retained heat raises the dispersion to sigma_heat^2/sigma_J^2 = 1 + E_sink/K_f. **EXCLUDED** if
  log10(1 + E_sink/K_f) > 0.1 in any system (the hydrostatic profile then misses the phantom/round target), else ALLOWED. If
  E_sink < 0 the label is "SOURCE NEEDED" (no sink problem).
- S(ii) exchange with dark energy: cosmic upper bound Delta rho_DE/rho_DE = (Omega_c/Omega_Lambda) x f_set x max(e/c^2) with
  f_set = 1; Delta log10 a0 = (1/2) log10(1 + Delta rho_DE/rho_DE). Local: injected energy density at r_M, rho_ph(r_M) e, over
  rho_DE c^2, (a) if it stays (clustering DE) and (b) if it leaves at c (factor (r_M/c)/t_90). **ALLOWED** if cosmic
  Delta log10 a0 < 0.004 dex (one tenth of DESI's +-0.04 dex, CFG512) and case (b) local Delta a0/a0 < 1e-3; **EXCLUDED** if cosmic
  Delta log10 a0 > 0.04 dex. Structural conditions printed with the label: an exact Lambda (w = -1) cannot exchange energy
  (div of Lambda g^{mu nu} = 0); the exchange coupling Q is not derived (open item). Case (a) reported with its own label by the
  same 1e-3 local rule.
- S(iii) radiation: electromagnetic -- cold energy has no EM coupling (structural EXCLUDED). Gravitational waves: upper bound
  P_GW = (G/5c^5)(eps M_cat r_*^2/t_90^3)^2 with eps = 1 vs P_req = E_sink/t_90; **EXCLUDED** if P_GW/P_req < 1e-3.
- S(iv) the baryons: the drift force is not gravitational, so handing its work to baryons needs a cold-baryon coupling: EXCLUDED
  by G9 (structural); E_sink/K_b (K_b = (3/4) V_f^2 M_b) reported.

### C -- causality (task 5)
- C1: drift speeds in the 1-D models at t = 0: max |v_s|/c and max |v_s|/V_c(r) over the reservoir; subluminal if
  max |v_s|/c < 1e-2.
- C2 (sympy + root scans): linear dispersion about a uniform state for (A0) class A as written (instantaneous psi); (A1) psi
  retarded, undamped wave; (A2) psi a damped wave with damping time tau_psi; (A3) Cattaneo drift tau dv/dt + v = -tau grad psi with
  instantaneous psi; (A4) Cattaneo + undamped wave; (A5) Cattaneo + damped wave. Stability by Routh-Hurwitz (sympy) and by
  numerical roots on a grid of k c/Gamma in [1e-3, 1e3] and rho_c/rho_m in (0, 1).
- Labels: **CAUSAL** if the system as written has every signal speed <= c; **CAUSAL-WITH-tau** if it has an instantaneous
  (elliptic) element but a completion with a relaxation time built from G and the local density (no new constant) has front
  speed c, is linearly stable for every admissible state 0 < rho_c/rho_m < 1, and reduces to class A in the static limit;
  **ACAUSAL** otherwise. The undamped retarded completion is reported with its own STABLE/UNSTABLE label.

### D/M -- dimensional audit and MUTATE (task 6)
- D1 (main): sympy units audit of every equation in EQUATIONS.md (each term same dimension; tau, Gamma, v_s, psi, d, Q built only
  from the listed constants). PASS/FAIL.
- MUTATE (`CFG541_MUTATE=1`; each must FAIL its property, i.e. the teeth must bite):
  - M1 sign-reversed drift v = +tau grad psi: F must increase (max step (F_{n+1}-F_n)/F_0 > +1e-3).
  - M2 reservoir constraint removed (outer boundary cell held at its initial density, unlimited supply): the cap must break
    (settled mass > 1.05 M_cat and front radius > 1.05 r_* within the run).
  - M3 audit with a hidden constant (tau = 1 Gyr inserted): D1 must flag it.
  - The MUTATE run exits 1 when all three bite (as designed); the main run exits 0 when V1-V5, T2a numerics, C2 and D1 checks run
    without error.

## Overall label
FULLY SPECIFIED / SPECIFIED WITH OPEN ITEMS (listed) / INCONSISTENT, per E1, with per-item EMERGENT/INHERITED,
ALLOWED/EXCLUDED, CAUSAL/ACAUSAL/CAUSAL-WITH-tau.

## Pre-freeze disclosures (not blind)
- Read before this freeze: CFG539 criteria/Stage 1, CFG489, CFG461, CFG462, CFG515 lib, CFG540 README + estimator,
  THEORY_v1, T17. Reasoned (not computed) expectations: the variational form needs the census edge removed from s, and the
  census edge then coincides with the turnaround catchment's exhaustion radius for a point mass (because M_cat = 5.364 M_b/f_ret is
  an identity when M_ta = M_b/(f_ret f_b)); CFG462's F-H/CAT run (23.38 r_M) and CFG540's post-freeze supply-cap variant
  (edge x1.36, groups +0.118/+0.105) point the same way, so T2b is expected to PERSIST; the undamped retarded psi is expected
  unstable and a damped one stable when Gamma tau_psi < 1; the heat route is expected EXCLUDED (CFG489: target 2.2-7.7x more
  bound than infall). These are expectations, not results; the script decides.
- The 1-D model is the drift sub-flow only (no orbital motion, no expansion, static baryons): its times are idealised.
