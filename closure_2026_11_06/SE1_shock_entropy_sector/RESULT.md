# SE1: the shock-entropy sector at action level. FAIL; the last physics class is closed

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. This is a TEST lane, run as the handoff specifies
(HANDOFF_FIELD_EQUATIONS_CHAT_2026_11_06.md, "Lane SE1"). There is no particle.
- Criteria: FROZEN_CRITERIA.md (bf53473414), committed alone before any script.
- Scripts: se1_fieldeq.py (sympy, 9 s), se1.py (about 25 min on one thread, checkpointed in parts/), and se1.py --mutate.
- Lean: fable_independent_2026/lean_2026/SE1_shock_entropy.lean, with its MUTATE twin.
- Outputs: se1.json / se1.out / run_main.txt, se1_MUTATE.* / run_mutate.txt, se1_fieldeq*.json / .out.
- Read-only inputs: GB1, KD1, EN1, QX3 iter2, QX12 iter_3, QX13 (with the QX16 rerun), QX15. None of their files is edited.

**Label: FAIL, both arms, both footings, under every reading and closure.**
- **Arm (a)** fails G1-G7. It is KD1 exactly.
- **Arm (b)**:
  - strict closure (the action's own static solutions): G2-G7 fail.
  - generous stratified closure, at every alpha in the frozen bracket: G3 groups, G5 Coma UDGs, G6 dSph classes and G7 KiDS fail.
  - **no single entropy history alpha passes the classes together.** The discs need alpha <= 2/3; X-COP and the ellipticals need alpha = 5/3.
- **By the no-tuning rule, the shock-entropy class is closed.** A fourth-wall paragraph is appended to
  ALL_GATES_NOGO_2026_11_06.md.
- G9 (CMB lensing, w at z 3400, BBN) PASSES for both arms at their CMB-fixed setting. In both arms that setting is
  exactly what makes the static rows fail (arm a), or it leaves them to the shock history (arm b).

## 1. Field equations (certified)

The action is QX17's Legendre form (A), with v3s's K(Q) term replaced by L_x = F(Q, s) + zeta n^m d_m s:
- **Arm (a):** F = (mu_K^2/2K) g(s) (Q-1)^2.
- **Arm (b):** a gamma = 5/3 ideal fluid, F = K_s(s)^(-3/2) [(2/5)(Q-1)]^(5/2).

| Equation | Statement | Check |
|---|---|---|
| S1 zeta | n^m d_m s = 0 (smooth flow) | sympy EL, residual 0 |
| S2 s | dF/ds = nabla_m (zeta n^m) | residual 0 |
| S3 tau | nabla_m [F_Q n^m - (zeta/Q) D^m s] = 0 (plus QX17's P / lambda current, unchanged and additive) | residual 0 |
| S4 stress | T_mn = g_mn (F + zeta n.ds) + Q F_Q n_m n_n - 2 zeta n_(m d_n) s - zeta (n.ds) n_m n_n; on shell the energy density is Q F_Q - F | residual 0, all 3 components |
| S5 static (Theorem K) | Q = c_tau/N with one global c_tau, d_t zeta = N F_s, T_tx = zeta N s'. A static sector with F_s s' != 0 has a secularly growing T_tx against a static metric, so static sectors are isentropic per region with rho_0 = F_Q(c_tau/N, s): open contact with the cosmic chemical potential | sympy exact, PASS |

- **F1.** Euler-Lagrange derivatives on 1+1 jets, with a general metric, tau, s and zeta.
  - Three seeds with a generic polynomial F, plus each arm's own F once.
  - Worst relative residual 0 at 40 digits (line 1e-25).
  - MUTATE (the zeta flux in S3 and the -2 zeta n_(m d_n) s stress flipped) fails S3 / S4 at 7e-3 to 1.9, as it must.
- **F3, Lean.** Five theorems compile, standard axioms only, 0 sorry:
  - `jeans_mono`;
  - `secular` (the core of Theorem K);
  - `crocco_static`;
  - `shock_enthalpy`;
  - `jeans_adiabatic`.
  The MUTATE twin fails on exactly its three false claims (exit 1).
- **F4, FD solver (Lagrangian shooting).** KA5 below.
  - The truncated n = 3/2 star is recovered: rho_s to 1.0e-5, M(< x_s/2) to 7e-5.
  - Lane-Emden constants: 3.9e-13 and 5e-5. The n = 1 radius pi/k_J is recovered to 6e-6.
  - Step doubling changes b by at most 2.3e-4 (line 1e-3).
  - No solve failed; the largest central hole was 4.4e-3 r_sh.
- **Sun.** The Sun is graded with b = 1 (KD1 P4), so G8 = L0: PASS.
- **Not certified:**
  - The combined QX17 + S-system was not re-varied as one Lagrangian. The terms are additive, so the equations add.
  - The 3+1 form is not separately checked. The equations are written without dimension-specific identities.
  - Shocks are not in the action. They are the conservative weak solutions, with Sigma >= 0 as the admissibility condition.

## 2. Built inputs (frozen in section 4, before grading)

| Input | Value | Source |
|---|---|---|
| R = omega_d/omega_b | 5.4092 / 5.4107 | kd1.json (QX15 main theta) |
| captured share f_cap R (f_cap 0.76) | 4.111 / 4.112; f_cap 1.0 reported | X22 |
| rho_sea | 33.57 / 33.56 Msun/kpc^3 | QX15 |
| shock radius | r_ta/2 (QX10's r_ta), cold sea upstream; r_ta/3 reported | QX13 |
| alpha bracket, K(m) = K_sh (m/M_cap)^alpha | {0, 2/3, 5/3} | shock law K ~ m^(2/3 + eps) |
| primordial c_0 (arm b) | 0.0675 km/s (mu0_J = 631 Mpc^-1) | G9a only |
| Coma ambient upper bound (G5) | Newtonian hydrostatic density of the beta model (8.6 keV, 276 kpc, 0.71) at each d_mean | S1 / CFG948 |
| host temperatures (MUTATE i) | X-COP mean kT(r), group kT, Fukazawa kT_o, SPARC 1e4 K, Coma 8.6 keV | EN1 / GB1 |

The hosts number 145 SPARC, 7 ellipticals, 7 X-COP, 20 + 20 groups, 9 UDGs, 82 dSphs and 14 KiDS bins per footing.

## 3. Gate x footing (canonical / alt identical in status)

| | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | G9a / G9b | B1a / B1b |
|---|---|---|---|---|---|---|---|---|---|---|
| arm (a), any reading (= KD1 at mu*; same statuses at 10, 100 and 1e4 x mu*) | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| arm (b), reading O, strict (Theorem K) | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| arm (b), reading O, generous alpha 0 | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| arm (b), reading O, generous alpha 2/3 | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| arm (b), reading O, generous alpha 5/3 | **FAIL** | **PASS** | FAIL | **PASS** | FAIL | FAIL | FAIL | PASS | PASS | PASS |
| arm (b), reading H (s_0 hosts captured cold, KD1 model P), any closure | FAIL | as O | FAIL | as O | FAIL | FAIL | FAIL | PASS | PASS | PASS |

**Arm (b), reading O, generous, alpha 5/3 (the closest member).**

| Gate | canonical | alt | line |
|---|---|---|---|
| G1 SPARC | Z -0.064, rms 0.150 | Z -0.090, rms 0.163 | rms 0.146 / 0.143 |
| G2 X-COP | +0.037 / 0.096 | +0.015 / 0.087 | PASS |
| G3 groups | 8/20 and 6/20 | 7/20 and 3/20 | 16/20 |
| G4 ellipticals | +0.137 | +0.118 | PASS (0.15) |
| G5 Coma UDGs | +0.993 (3.79 sigma_U) | +0.951 (3.63 sigma_U) | |
| G6 dSph | bright M31 +0.163 [+0.072, +0.429] | bright M31 +0.148 [+0.057, +0.416] (CI excludes 0 on both) | |
| G7 KiDS | R +0.152 (2.37 sigma) | same | |

- f per class, mean b - 1 (canonical; alt within 0.01):

  | | SPARC | X-COP | groups f*0 / f*1 | ellipticals | UDGs | bright M31 | LG field | KiDS early / late |
  |---|---|---|---|---|---|---|---|---|
  | alpha 5/3 | 0.42 | 3.84 | 2.70 / 2.20 | 0.26 | 0.76 | 0.50 | 0.26 | 1.72 / 1.65 |
  | alpha 2/3 | 0.05 | 0.60 | 1.10 / 0.77 | 0.03 | 0.15 | | | |

- Needs (KD1): SPARC <= 0.33 / 0.19; X-COP 4.2 / 3.8; groups 1.2-3.5; ellipticals 0.9; Coma UDGs about 80.
- Reported variants (alpha 2/3), f_cap 1.0 and r_sh = r_ta/3: same statuses as alpha 2/3 (G2 FAIL, X-COP f 0.77 / 0.96).

**Arm (b), G9 and growth.**
- s(z) = s_0 until shell crossing, so c_s = c_0 (1+z) and the Jeans term is k^2/(a mu0^2).
- At c_0 = 0.0675 km/s:
  - chi^2 cold limit 8.56 (line 18.48), Delta chi^2 <= 4;
  - w(3400) 3.5e-7;
  - BBN extra/radiation 6.8e-6.
- So G9a and G9b PASS, B1a and B1b PASS.
- At that c_0, the Jeans mass at turnaround is 2e5 Msun and a 100 km/s infall has Mach 280. Every host's own infall
  shocks, which supports reading O.
- **Converse.** Keeping the smallest SPARC host uncaptured under reading H needs c_0 = 0.80 km/s. That costs
  Delta chi^2 = 1056: FAIL.

**Arm (a), converse (KD1).** The values of mu that galaxies allow (0.1, 79) fail w(3400), BBN and G9a.

## 4. Does the action-level sector escape EN1's radial-shape failure? Partly, and only at a price

X-COP medians, canonical:

| | 0.1 R500 | 0.2 | 0.3 | 0.5 | 0.7 |
|---|---|---|---|---|---|
| needed f (EN1) | 5.34 | 4.93 | 4.44 | 3.33 | 2.39 |
| generous, alpha 5/3 | 7.34 | 4.14 | 3.18 | 2.43 | 2.18 |
| generous, alpha 2/3 | 0.48 | 0.53 | 0.58 | 0.65 | 0.75 |
| strict (Theorem K) | 0.00 | 0.01 | 0.01 | 0.02 | 0.04 |
| sector K (keV cm^2), alpha 5/3 / 2/3 | 47 / 155 | 149 / 380 | 295 / 631 | 687 / 1170 | 1180 / 1720 |
| gas K (EN1 proxy) | 205 | 410 | 603 | 982 | 1075 |

- **The answer is yes in shape, for one history.** At action level the sector's amount is set by hydrostatics in its
  own entropy profile, not by g(K) per baryon. So EN1's monotonicity argument (f a mass-weighted average of a
  non-decreasing g) does not apply. With alpha = 5/3 (low inner entropy, steeper than the gas K) the need's outward
  fall is reproduced and X-COP passes.
- **That same history overfills discs** (G1 FAIL, f 0.42 against 0.33 / 0.19). It still leaves groups at 3-8 of 20,
  and UDGs and dSphs far short.
- The gas-like history (alpha 2/3, whose sector K tracks the gas K to within 25 %) reproduces EN1's failure: f rises
  outward, X-COP is under-filled.
- **The action's own static solutions (Theorem K) are isentropic and give essentially nothing** (f <= 0.04).
- **No-tuning check** (reading O, both footings), alphas that pass each gate:

  | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
  |---|---|---|---|---|---|---|---|
  | {0, 2/3} | {5/3} | none | {5/3} | none | none | none | all |

  The intersection is empty: the classes need different entropy histories. Arm (a) has the same structure exactly:
  - discs and the CMB share s = s_0;
  - the CMB and BBN need mu_K^2 g(s_0) >= (8.9e6)^2 Mpc^-2;
  - galaxies need mu_K^2 g(s_0) <= 79^2;
  - every shocked host has g >= g(s_0) (`jeans_mono`).
- **Coma UDGs (G5) fail every member.**
  - The sector's rest mass is conserved, so a host holds at most the cosmic share f_cap R ~ 4.1. The solved UDG f is 0.15-0.76.
  - Adding the Coma ambient upper bound moves the mean by at most 0.03 dex (still 3.6-4.2 sigma_U).

## 5. Known answers and MUTATE (all PASS / BITE)

- **KA1:** b = 1 equals gb1.json L0, |d| 0. The QX20 means agree to 4.3e-7 / 4.5e-7.
- **KA2 / MUTATE iii:** arm (a) with g constant equals kd1.json's static rows, |d| 0, statuses equal. KD1's Jeans rows
  (n = 1) and chi^2 8.559852 are reproduced, |d| 0.
- **KA3 (QX13 to 0):**
  - qx13.py's own solver reproduces QX16's rerun qx13_FIXED.json, |d| 0.
  - SE1's strict solver in QX13's shock mode reproduces QX13 M1 FIXED, |d| 0.
  - Against the original qx13.json, only G7_shift differs (6e-6, the QX16 elliptical fix).
- **KA4 (EN1):** EN1's within-host table and its V-frac-L constant are reproduced, |d| 0.
- **KA5:** known answers above. **KA6:** shock identity to 8.9e-16.
- **MUTATE (i), s set by host temperature (isentropic, open contact):** it bites.
  - G2 +0.466 / +0.432, G3 0/20, G5 FAIL; G4, G6 and G7 are NO VERDICT (no temperature).
  - It reproduces QX12's fixed-temperature under-fill. G1 passes (see disclosure 4).
- **MUTATE (ii), Sigma flipped (shocked hosts at or below s_0, captured cold):** G1 FAIL, both footings. It bites.
- **MUTATE (iii):** this is KA2, with G1 FAIL. It bites.

## 6. Disclosures

1. **KA3 reference changed after the freeze.** The criteria named qx13.json, but QX16's rerun
   (fixed_outputs/QX13_virial_floor/qx13_FIXED.json) is the current record. KA3 is graded against it, and the
   original is reported. The only difference is G7_shift 6e-6, from QX16's elliptical fix.
2. **Post-freeze code fixes, all before any label was read.**
   - The shooting bracket direction was reversed in the first draft; KA5 caught it.
   - G8 needed KD1's `nodust` tag on Sun features.
   - MUTATE (i) at first skipped the frozen SPARC 1e4 K rule, so G1 read NO VERDICT. It was fixed and only MUTATE was rerun.
     The main outputs do not use that path.
3. **The Lean twin was compiled through the sibling checkout's Mathlib build** ("new_physics copy", same toolchain
   v4.34.0-rc2 and the same lake-manifest), because this checkout's .lake has the Mathlib sources but no build.
   Nothing was downloaded.
4. **Reading H's "captured cold" uses KD1's model P (core collapse).**
   - That is not a static Theorem K solution. A static open-contact gamma = 5/3 sector has rho ~ ((2/5) H/K)^(3/2):
     broad, not core-concentrated, even for tiny K. This is why MUTATE (i) passes G1.
   - Under strict statics, reading H's discs would therefore pass G1, but then nothing collapses anywhere and every
     hot row fails (strict O row).
   - Either way the class fails.
5. **The generous closure ignores Theorem K.** A stratified khronon sector is not a static solution (S5). It needs a
   secularly evolving foliation whose consequences, such as preferred-frame effects, are not graded. It was graded
   as the most favourable case QX13 left unproved. It fails anyway.
6. **G9 with A_s refit** follows QX3 / KD1. Growth has no separate framework-native dataset; G9b takes G9a's window.
7. **The alpha bracket is a physical bracket, not a scan.** No constant was fitted on a hot class. alpha 5/3 passing
   X-COP and the ellipticals is a bracket member, not a tuned value.
8. **dSph satellites are solved isolated.** Host-atmosphere stripping of a collisional sector could only lower them.
   Group "host temperature" is the global kT.
9. **Downloads that would sharpen rows** (none changes the label): a Coma n_e profile, NGC 6482 hot gas, dSph host CGM.
10. **Adopts nothing.**

Kappa = 1/2 FITTED; not theory closed.
