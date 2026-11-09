# SQ1 (component-screened law, the outside source's variant Q): FROZEN CRITERIA, committed alone before any SQ1 script or number

TEST lane, quarantined; registered RUNNING by the orchestrator. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11, v_stiff 265.8) and alt (1.1312e-10, 288.1), never pooled; QX15 footing h and omega. Read-only machinery:
PD1 / PD2 (loaders, KiDS / SPARC evaluators, DB1 Newtonian child), SS1 (primary halos), WM1 (wm1_cosmo.py via patch, as TS1),
WL1 / GSMF.

## 1. Construction Q, frozen once

**Content.** A cold component chi (omega_chi = 5.41 omega_b) gravitates normally. The law's phantom is modified gravity, not mass,
multiplied by a screening factor:
- S(rho_chi) = 1 / (1 + x^2), with x = rho_chi / rho_screen and rho_screen = a0 H0 / (2 pi G c). So
  rho_screen / rho_crit = 4 a0 / (3 c H0), recomputed per footing.
- The baryons feel g = g_N + S(rho_chi,local) (nu(g_N,b / a0) - 1) g_N,b. Here g_N is all matter, Newtonian, and the phantom acts
  on the baryons' own field.

**Lagrangian (the source's).** L = -|grad Phi|^2 / (8 pi G) - (rho_b + rho_chi) Phi - U_Q S(rho_chi), with
U_Q = (a0^2 / (8 pi G)) F(y), y = |grad Phi_b| / a0, and F'(y) = 2 y (nu(y) - 1). The deep limit is F = (4/3) y^(3/2) (frozen,
stated).

**The force on the component, from the stated L.** Varying rho_chi in the fluid action gives the chemical potential
mu_rep = d(U_Q S) / d rho_chi = U_Q S'(rho_chi). So the component's acceleration is -grad Phi - grad(U_Q S').
- S' < 0, so mu_rep is negative and deepest where U_Q is largest. **The stated Lagrangian attracts the component toward luminous
  galaxies.**
- The source's V_rep = -U_Q dS/d rho > 0, repulsive, has the opposite sign.
- The lane grades the stated Lagrangian's sign (G) and reports the source's sign (R) as a bracket.

**Readings for galaxy-scale halos.**
- **G (graded):** the component sits in SS1's primary halos (KD1 P3: truncated SIS, f_cap R M_b), with no depletion; Q1 decides
  whether any depletion is reachable. Outside R200 it is at the cosmic mean.
- **C (bracket, the source's claim):** isolated lenses and spirals depleted to 0.2 rho_screen out to 3 Mpc.

**Groups and clusters (the source's rule, graded).**
- The retained component inside r follows the primary halo with f_ret(u) = (1/sqrt 2) exp(-(v_stiff / v_vir)^2 / g_pot(u)),
  g_pot(u) = (u / (0.05 + u))(1 - 0.42 u), u = r / R500, v_vir = sqrt(G M500 / R500) of the primary halo (SS1 convention).
- Local S comes from the retained component's local density at each point.
- **Form choices:** the 1/sqrt 2, g_pot, the 0.2 rho_screen, the 3 Mpc, the squared form of S.

## 2. Gates (order Q1, Q-KiDS, Q-SPARC, Q-groups, Q-X-COP, Q2, Q-web, Q5 Bullet, Q3, Q-Cassini)

| gate | quantity | line |
|---|---|---|
| **Q1 depletion dynamics** | Spherical shells of the component around an isolated galaxy (M_b 1e10, 1e10.5, 1e11), Lagrangian radii 0.05-6 Mpc, integrated from z 1.5 to 0. Forces: background (matter + Lambda, as WL1), the baryon point mass and the enclosed component excess, plus the component force -grad(U_Q S') with x(z) = the shell's own density / rho_screen (from shell crossing-free mass conservation). Sign G graded; R reported | PASS iff the component density inside 3 Mpc at z 0 is <= 0.2 rho_screen (the source's requirement) |
| Q-KiDS | 59 points, pointwise. g = g_N,b + G dM_chi,excess / r^2 + S_local (nu - 1) g_N,b. Reading G; C reported | \|shift\| <= 0.05 (SS1 gate 1) |
| Q-SPARC | QX8 evaluator with g = g_N(1 + f_chi) + S_local (nu - 1) g_N,b; S_local from the primary halo's density at R. Reading G; C reported | SS1 G5 |
| Q-groups | Lovisari 20, f_ret rule, local S | >= 16 / 20 at f* 0 and 1 |
| Q-X-COP | likewise; f_miss per bin vs TR1 | SS1 gate 3 |
| **Q2 volume filling** (the orchestrator's first expected kill) | Graded on reading C. n(M* > 1e10) from the Driver GSMF; Poisson filling f_V = 1 - exp(-n (4 pi / 3)(3 Mpc)^3) (an upper bound; clustering lowers it, stated). The displaced mass fraction, the complement density rho_hi, and the two-phase (Boolean-sphere) component power P_2p(k) at k 0.3 / 1 / 3 h/Mpc relative to the cold linear P_ref(z 0). S8 change with sigma_8,new^2 = sigma_8^2 + (omega_chi / omega_m)^2 sigma_2p^2(8 Mpc/h), against SS4's CS line (\|change\| <= 5.9 %) | CS line; P_2p / P_ref reported |
| Q-web | WM1's D1 / cosmo machinery with a cold component (no relic) and nu_eff = 1 + (nu - 1) S(z). Graded: S(z) at the cosmic mean density, x = x0 (1 + z)^3. Reported: reading C, S_eff = f_V x 0.96. Gates 7b-L, forest + fsigma8, CS | WM1 lines |
| Q5 Bullet | screened (S about 0): Newtonian + the f_ret component inside R200, galaxy-traced (PD1 A2 child) | DB1 label |
| Q3 Ursa Major / LG | local S at the host's mean density inside 1.5 Mpc (G); under C, the host's v_vir vs v_stiff decides depletion | reported (the SPARC gate carries the RAR) |
| Q4 z turn-on | S at the cosmic mean and in the C-depleted state at z 0, 0.3, 0.5, 1, 1.5 | reported |
| Q-Cassini | inside the Sun's neighbourhood rho_chi >> rho_screen, so S is about 0: Newtonian, with the record's Cassini PASS carried | carried |

**Label:** PASS iff every graded gate passes (Q3, Q4 reported). Otherwise FAIL, naming the first failing gate.

## 3. Known answers

- **KA-S1:** rho_screen / rho_crit = 4 a0 / (3 c H0), numerically from both definitions to 1e-12.
- **KA-S2:** with S = 1 everywhere and no component, the local gates reproduce law-only: KiDS 0, X-COP +0.4675 / +0.4345.
- **KA-S3:** with the component force off, the Q1 shells reproduce WL1's Newtonian turnaround radius for dM = M_b (1 + R), to 1 %.
- **KA-S4:** F'(y) = 2 y (nu - 1), checked numerically against the deep form (4/3) y^(3/2) at y = 1e-6, to 1e-3.

## 4. Hand estimates (before any number)

- **rho_screen** is about 0.19 / 0.23 rho_crit, so the mean component is about 1.4 / 1.2 rho_screen today and S(mean) is about
  0.34 / 0.43. At z 1, S(mean) is about 0.008.
- **Q1:** the component force over gravity at r is about |S'| rho_screen 0.32 ... sqrt(y) c / (H0 r), about 16 at 1 Mpc for M_b 8e10.
  It falls as r^-4.
  - With sign R, a shell at 1 Mpc moves about 70 kpc in 5 Gyr, so draining to 3 Mpc is unreachable.
  - With sign G it falls inward.
  - **Expected FAIL.**
- **KiDS (G):** S at the mean density is 0.34, so the phantom is cut by 3x beyond R200: about -0.4 dex. FAIL.
- **SPARC (G):** inside halos x >> 1, S about 0: Newtonian + halo. FAIL.
- **Q2 (C):** n is about 0.01 / Mpc^3, so f_V is about 0.68. The complement holds about 2.8 rho_bar. S8 may move by less than 6 %.
- **Q-web:** S(mean) of 0.1-0.34 at z 0-0.3 with nu 13-30 still boosts the linear web several-fold. fsigma8 and S8 FAIL.
- **Clusters:** screened. X-COP from f_ret (claimed to match TR1). Groups (v_vir about v_stiff) lose most of the component and the
  law turns on.
- **Expected label: FAIL / FAIL at Q1.**

## 5. MUTATE

- **MS1:** rho_screen x 10 (S near 1 more widely): KiDS (G) must move.
- **MS2:** the component force off: Q1's shells must reproduce KA-S3 (null).

## 6. Operational

- One thread, nice 10; RSS < 1 GB except CLASS (disclosed); small outputs.
- Explicit-path commits via a sparse temporary worktree, scripted, removed after.
- Files: sq1.py (Q1, local gates, Q2, Q3, Q4, Bullet), sq1_cosmo.py (Q-web via patched WM1), sq1.json / .out, RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
