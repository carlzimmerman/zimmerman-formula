# CFG375 FROZEN CRITERIA: the minimum energy any settling mechanism must handle (optimal transport), against the vacuum budget

Committed alone, before any script. kappa = 1/2 FITTED and fixed. Kernel nu_mono(y) = 1/(1 - exp(-sqrt y)) (the record's monotonised implementation in CFG100's cfg100_lib.py). No dark-matter particle species: the cold fluid's AMOUNT is still required and kept (Omega_c/Omega_b = 5.364, not derived). No knob scans. Never "theory closed". Both a0 footings, never pooled: canonical 9.3603e-11, alt 1.1312e-10 m/s^2.

**Question.** The working model (WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md) has a conserved cold fluid settling into rho_ph = (1/4 pi G) div[(nu_mono(|g_b|/a0) - 1) g_b]. CFG373 G4 estimated that the khronon could absorb settling energy of 3e-8 to 1.3e-5 rho_Lambda c^2. What is the MINIMUM energy that ANY settling mechanism must move or absorb, and does it fit inside the local vacuum energy?

## Construction (declared)
- Cosmology: Omega_m 0.3153, h 0.6736, Omega_b 0.0493, Omega_c = Omega_m - Omega_b, Omega_Lambda = 1 - Omega_m; rho_Lambda c^2 from these.
- **Baryons:** a point mass M_b (as in CFG100's r_ta_law). Host grid M_b in {1e9, 1e10, 6e10, 1e11, 1e12, 1e13} Msun.
- **Framework field from the baryons:** g(r) = nu_mono(y) G M_b / r^2, y = G M_b/(r^2 a0). Enclosed phantom M_ph(<r) = M_b (nu_mono(y) - 1).
- **Turnaround:** r_ta solves mean enclosed (M_b + M_ph) density = Delta_ta(z=0) rho_m, Delta_ta = 11.806 (CFG100 r_ta_law). **Ownership edge** r_out = 0.4 r_ta.
- **Supply:** S = 5.364 M_b / f_ret, f_ret in {1, 0.18}, at the mean cosmic cold density rho_c_bar = Omega_c rho_crit (z=0, physical), in its Lagrangian sphere R_L: (4 pi/3) R_L^3 rho_c_bar = S. V_catch = (4 pi/3) R_L^3. Never collected (initial state uniform).
- **Transported mass** M_t = min(M_ph(<r_out), S).
  - Source: the innermost M_t of the supply sphere (uniform ball of radius R_t, R_t <= R_L). For radially concentrated targets this is the cheapest selection under any radially increasing cost.
  - Target: the phantom profile inside r_out scaled by s = M_t / M_ph(<r_out) (shape kept; the law partly realised uniformly when supply binds).
- **OT map:** for radially symmetric measures the Brenier map is radial (uniqueness plus rotational invariance; OpenAI-math result 374 context; 360 for regularity) and monotone, i.e. the equal enclosed-mass-fraction rearrangement r_i(q) -> r_f(q), q in [0,1]. W2^2 = integral_0^1 (r_i(q) - r_f(q))^2 dq (per unit mass).
- **Bound (a) kinetic:** Benamou-Brenier E_kin = M_t W2^2 / (2 tau^2), tau in {10.3 Gyr, 1 Gyr} (declared bracket). This is the minimum time-averaged kinetic energy of ANY flow doing the rearrangement in time tau.
- **Bound (b) binding:** Delta U = U_f - U_i of the transported mass, released energy E_bind = -Delta U (must be dissipated or absorbed somewhere).
  - U = integral dm Phi_b(r) + W_self, with W_self = -integral G M_t(<r) dm / r (Newtonian self-energy of the transported fluid; initial uniform ball W_i = -(3/5) G M_t^2 / R_t). Untransported fluid and the background (Jeans swindle) are ignored.
  - **Primary (B1):** Phi_b from the full framework field g(r) above (deep-MOND log at large r, Newtonian inside) plus the Newtonian self-term. This is the prompt's construction (the deep-MOND log potential is the large-r limit of this field).
  - **Variant (B2):** pure deep-MOND log, Phi_b = sqrt(G M_b a0) ln r, plus self-term (upper variant).
  - **Variant (B3):** working-model eq. 1 reading, Phi_b = -G M_b / r (Newtonian baryons only) plus self-term.
  - Verdict on B1. B2 and B3 reported; a category disagreement is flagged.

## Budget metric and verdict
epsilon = E / (rho_Lambda c^2 V_catch), per host, per f_ret, per tau (bound a), per footing.
- Since a0 is proportional to sqrt(rho_Lambda), a fractional vacuum-energy change epsilon shifts local a0 by epsilon/2.
- **ALLOWED:** epsilon <= 0.1 (local a0 uniform to 5%).
- **MARGINAL:** 0.1 < epsilon <= 1.
- **EXCLUDED:** epsilon > 1 (more than the whole vacuum energy of the catchment).
- Per bound, the lane category is the WORST cell over hosts, f_ret and tau, reported per footing (never pooled).
- Also reported: whether the bound sits inside CFG373's G4 absorption range (3e-8 to 1.3e-5); a minimum above 1.3e-5 means CFG373's G4 estimate was too low (a consistency FAIL for CFG373's number, not for the vacuum budget).

## Controls
- **C1:** Delta_ta from CFG100's dta(0) equals 11.806 to 1e-3; nu_mono(y) matches 1/(1 - exp(-sqrt y)) to 1e-3 on 0.01 <= y <= 100.
- **C2 (OT optimality):** W2^2 of the monotone map <= W2^2 of the anti-monotone map (q -> 1 - q) and of 20 random quantile permutations (fixed seed) for every cell.
- **C3:** uniform-ball self-energy from the numerical routine matches -(3/5) G M^2 / R to 1e-3.
- **C4:** mass conservation: target mass integrates to M_t to 1e-6.

**MUTATE (CFG375_MUTATE=1, outputs suffixed _MUTATE):** replace the monotone map by the anti-monotone rearrangement. C2 must FAIL (the declared map is no longer the minimum) and the run must exit rc 1.

Optional: a Lean file certifying epsilon_max <= 1/10 at the computed rational upper bounds (arithmetic only, not physics).

Local compute only. No downloads. Seconds of CPU.
