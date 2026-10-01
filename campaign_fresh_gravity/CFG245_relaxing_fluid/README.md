# CFG245 -- an early cold fluid that relaxes, at a vacuum-set rate, toward the law's local-field dark density: phase 2 (Gate T is the binding FAIL; a scoped no-go)

Criteria frozen and committed before any script: `campaign_fresh_gravity/CFG245_FROZEN_CRITERIA.md` (commit 63b7ad8e2, sha256 `3f7dbda7029d8e8abd7648760367272423bd843035ae210b60e3e87d6eef449b`, identical to the file I wrote). Run as frozen; every departure and every ambiguity is listed in section 9. Written only in a scratch directory; the repository was only READ.

**Nothing here is closure. kappa = 1/2 stays FITTED. There is no dark-matter particle and no new species: the class is a pressureless, collisionless FLUID, and the cold MASS (Omega_c h^2 = 0.1200) is still REQUIRED and supplied by nothing in the class. A scoped no-go is not a theorem. A lean is not a detection. T3 (the a0_eff(z) row) is a PREDICTION of the model class; it says nothing about which a0(z) law the data favour, and nothing here says any data favour or disfavour the framework or LambdaCDM.**

**Re-run (about 40 s).** From this directory: `ZF_REPO=<repo root> bash CFG245_run_all.sh` (inside the repository the root is found by walking up, so `bash CFG245_run_all.sh` suffices). It runs G0, T, then C, A, E (as POST-HOC extras because T bound), the 16 MUTATE controls with the frozen expected exit code beside the observed one, then `CFG245_verdict.py`, and ends with `unexpected outcomes: N` (observed: 1, the frozen-premise failure of MG2, section 8). Python 3 with numpy, scipy, sympy; nothing is downloaded. Every output was re-generated twice: all 22 `_results.json` files are identical apart from the `seconds` field and every `.out` is byte-identical. No output prints an absolute home path (`<repo>` and `<lane>` are substituted; checked by grep).

## 1. Bottom line

- **Gate T, sub-test T-G1, is the BINDING FAIL.** The relaxation (mass-conserving flux form, R-FLUX-2) at any of the three declared vacuum-set rates leaves most of the passive-infall deviation in place at z = 0, even in the deliberately generous bracket tau = t_0 = 13.80 Gyr (relaxation active since the start). Gamma*tau = **0.787** (G-H = H_Lambda), **0.136 / 0.164** (G-a = a0/c, canonical / alt), **0.272 / 0.329** (G-b = sqrt(G rho_Lambda), canonical / alt), i.e. residual fractions e^(-Gamma tau) = 0.455 / 0.873, 0.849 / 0.762, 0.720. The 10% line on the cumulative amount (x in [0.3, 20], all four masses, best bracket q) needs Gamma*tau >= **4.23** (canonical) / **4.07** (alt), i.e. Gamma >= **5.37 / 5.17 H_Lambda** at tau = t_0. All three candidates FAIL on both footings, so the FAIL binds and the lane stops there.
- **The owner's question (T-RAR; reported, not binding): partial relaxation does NOT give the RAR at SPARC precision for any declared rate.** On x in [0.3, 10] the largest offset from the law and the mass spread at fixed x are D1/D2 = 0.163/0.151 dex (G-H canonical, best bracket q = 0.05), 0.273/0.275 (G-a), 0.247/0.241 (G-b); alt 0.147/0.145, 0.244/0.263, 0.215/0.221, against the lines 0.048 (the record's intrinsic bound) and 0.10 (SPARC rms): every candidate FAIL. The rate that would reach the 0.10 line is **1.73 H_Lambda** (canonical; 1.58 alt) and the 0.048 line **2.73 / 2.58 H_Lambda**, at tau = t_0.
- **Post-hoc extras (labelled; no verdict depends on them) all would also bind on their own frozen lines:** Gate C (the pincer): at the generous joint bracket the window [Gamma_T,min, Gamma_C,max] = [1.73, 1.93] H_Lambda (canonical) / [1.58, 2.15] (alt) is non-empty but contains none of the declared rates (1.00, 0.17-0.21, 0.35-0.42 H_Lambda); at the central bracket it is empty. Gate A, supply ceiling A0: S/M_ph(<30) = 0.886-0.897 against the line 0.90 (a knife-edge FAIL of the frozen line; x_cap = 26.7-27.0). Gate E1: |Delta E|/(1/2 M_b V_f^2) = 0.49 to 9.5 (generous closure; up to 18.9) against the line 1.
- **The pre-specified extras:** the local-field target is NOT the CFG44 target for extended baryons (R_loc up to 2.33 for P2, 2.47 for nu_mono; exactly 1.000 for a point mass); the local target is non-negative on two masses and a thin disc to a negative-mass fraction of at most 9e-4 (my hand estimate that it would exceed 1% was wrong); the local form does not produce ownership (internal-to-Newtonian ratio up to 3.16 where the owned reading needs 1); the a0_eff(z = 2.5) prediction is -1.19 / -1.40 / -1.35 dex (G-H / G-a / G-b).
- **Nothing passed a binding gate**, so no independent re-derivation is owed. Controls: all seven reproduction controls PASS (plus one extra, C-E2); of the 16 MUTATE controls 15 behave as frozen (13 bite, MN1 and MN2 do not bite, as declared) and **MG2 fails its frozen premise** (it does not bite because the baseline already passed).

## 2. Gate table (P = PASS, F = FAIL, U = UNDEFINED, N = NOT ADDRESSED; each cell cites its script; MAIN = the frozen stop-rule verdict, PH = post-hoc extra after the stop, never part of the verdict)

| gate | cell | outcome | script |
|---|---|---|---|
| G0 controls | C-L1 (3D local-field target vs spherical form and hand closed form, tol 1e-3; worst 2.5e-4), C-L2 (point mass C_loc = C_44 for P2 to 2.5e-7; nu_mono ratio at x = 1: 1.4565) | **P** | `CFG245_G0_target.py` |
| G0.2 target identity (reported) | R_loc = C_loc/C_44 on CFG118's exponential spheres | **DIFFERS** (max 2.33 P2 / 2.47 nu_mono; point mass 1.000) | same |
| G0.3 positivity | spherical min rho_ph > 0; two equal masses f_neg <= 9e-4; thin disc f_neg = 0 | **P** (hand estimate wrong) | same |
| G0.4 conservation | flux operator conserves mass in D (0.0) and keeps shell masses >= 0 | **P** (tautological by the closed-domain construction; section 9) | same |
| G0.5 ownership from the local form | internal/Newtonian ratio 1.04-3.16 (isolated law 1.044 / 1.414 / 3.162 at r = 0.3 / 1 / 3 r_M); needs 1 | **F** (as expected: ownership is a separate label) | same |
| controls C-T0, C-T1 | CFG244's committed A2 numbers and exponents reproduced (displayed precision); e^(-Gamma t_0) table | **P** | `CFG245_T_timescale.py` |
| **Gate T, T-G1 (binding)** | per candidate and footing, section 3 | **F, BINDING, STOP (MAIN)** for all of G-H, G-a, G-b on both footings | same |
| T-RAR (reported) | D1/D2 vs 0.048 / 0.10 dex | **F** for all three, both footings, both kernels | same |
| T3 (reported, prediction only) | a0_eff(z = 2.5) | OUTSIDE THE CALIBRATION BAND, all three | same |
| controls C-C1 | Gamma = 0 reproduces the record's identity reading 0.946 | **P** | `CFG245_C_clusters.py` (outputs carry `_POSTHOC`) |
| Gate C, C1 | X-COP identity, generous bracket tau_cl = 3.5 Gyr | PH: **P** for all three (med abs(Q-1) 0.068-0.133 vs 0.20) | same |
| Gate C, C2 | Bullet, delta_B <= 0.10 | PH: **P** (max 0.0057) | same |
| Gate C, window | binding rule | PH: **F** (no declared rate inside the window) | same |
| control C-A1 | M_ta/M_b = 23.642 (CFG118 23.6) | **P** | `CFG245_A_supply.py` (outputs carry `_POSTHOC`) |
| Gate A, A0 | S/M_ph(<30) >= 0.90 | PH: **F** (0.886-0.897; knife-edge) | same |
| Gate A, A1, A2 | relaxed state, selectivity | PH: P-DECLARED / restatement | same |
| controls C-E1, C-E2 | virial identity, W integral; ball energy 1.171 M_b c^2 | **P** | `CFG245_E_ledger.py` (outputs carry `_POSTHOC`) |
| Gate E, E1 | energy at the shared G3 line | PH: **F** (0.49-9.5; up to 18.9) | same |
| Gate E, E2 | drift speed <= 1e-3 c | PH: **P** (max 121.6 km/s = 4.1e-4 c) | same |
| Gate E, E2 relativistic completion, E4 reaction | no action written | **U** | same |
| Gate E, E3(a), E3(b) | single eigenvalue -Gamma; Lyapunov exp(-2 Gamma t) | PH: **P** | same |
| Gate E, E3(c), E3(d) | coupled system; gate as an action term | **N** | same |
| variants R-FLUX-1, nu_mono | T-RAR FAIL (R-FLUX-1: never reachable, D1 >= 0.27); nu_mono FAIL | reported | `CFG245_T_timescale.py` |
| variant V-CREATE | creation form: mass created +14.4 M_b at Gamma = infinity (G0.4 / MM1); rest-mass ledger covered by CFG131/CFG243 | not scored beyond this row | `CFG245_A_supply.py` MM1 |

## 3. Gate T in full (T-G1 first; both footings; P2 kernel; point cores; committed CFG244 passive products read-only)

Favourable bracket tau_gal = t_0 = 13.796 Gyr (H_Lambda = 0.05705 /Gyr, 1/H_Lambda = 17.53 Gyr, Planck-2018 inputs H0 = 67.4, Omega_m = 0.315). Noise guard as CFG244: guarded and unguarded failing-bin counts are nearly equal (the guard rescues at most 10 of the 65 failing bins in any case), so no failure is a noise artefact.

| cand | footing | rate /Gyr | Gamma*tau | residual e | T-G1 | max abs(R-1) q = .05 / .1 / .2 | Gamma*tau needed | needed / H_Lambda |
|---|---|---|---|---|---|---|---|---|
| G-H | canonical | 0.057050 | 0.787 | 0.455 | **FAIL** | 4.89 / 4.16 / 3.64 | 4.23 | 5.37 |
| G-a | canonical | 0.009853 | 0.136 | 0.873 | **FAIL** | 9.37 / 7.98 / 6.97 | 4.23 | 5.37 |
| G-b | canonical | 0.019706 | 0.272 | 0.762 | **FAIL** | 8.18 / 6.96 / 6.09 | 4.23 | 5.37 |
| G-H | alt | 0.057050 | 0.787 | 0.455 | **FAIL** | 4.46 / 3.74 / 3.11 | 4.07 | 5.17 |
| G-a | alt | 0.011908 | 0.164 | 0.849 | **FAIL** | 8.32 / 6.97 / 5.80 | 4.07 | 5.17 |
| G-b | alt | 0.023815 | 0.329 | 0.720 | **FAIL** | 7.06 / 5.91 / 4.92 | 4.07 | 5.17 |

The passive deviation itself is the committed CFG244 one (A2 largest abs(ratio - 1) over brackets 7.99-10.73 canonical, 6.83-9.81 alt on x in [0.3, 30]: control C-T0 reproduces CFG244's 8.0-10.7 / 6.8-9.8 and exponents p = 0.3427 / 0.3392 / 0.3269). Sensitivity (reported, never in the verdict): tau_gal = 10.5 and 7 Gyr make every residual larger (G-H 0.55 and 0.67) and every category the same.

**T-RAR** (x in [0.3, 10]; D1 = max abs(Delta), D2 = mass spread at fixed x, dex; best bracket q = 0.05; category FAIL if D1 or D2 > 0.10 for every q):

| cand | canonical D1 / D2 | alt D1 / D2 | Gamma*tau needed (0.048; 0.10) | needed / H_Lambda (0.048; 0.10) can / alt |
|---|---|---|---|---|
| G-H | 0.163 / 0.151 | 0.147 / 0.145 | 2.15 ; 1.36 (can), 2.03 ; 1.24 (alt) | 2.73 ; 1.73 / 2.58 ; 1.58 |
| G-a | 0.273 / 0.275 | 0.244 / 0.263 | same (a property of the passive state) | same |
| G-b | 0.247 / 0.241 | 0.215 / 0.221 | same | same |

nu_mono (its own local target): D1/D2 0.130/0.143 (G-H canonical), 0.222/0.272 (G-a), 0.199/0.237 (G-b); all FAIL; the kernel moves the category not at all (MN1). R-FLUX-1 (fill-only): D1 >= 0.267 for every candidate and no Gamma*tau <= 30 reaches the 0.10 line (the excess inside x about 1.1 is never removed). The extension x in [10, 28.2] with the supply-capped target: D1/D2 = 0.152/0.111 (G-H canonical q = 0.1), 0.326/0.236 (G-a), 0.273/0.200 (G-b).

Deviations at the extremes against the frozen hand numbers (q = 0.1, canonical): x = 1.12, Delta in [+0.018, +0.165] (G-H; hand +0.017 to +0.165), [+0.033, +0.276] (G-a; hand the same), [+0.029, +0.249] (G-b); x = 28.2, [-0.152, -0.083] (G-H; hand -0.138 to -0.072: the supply cap lowers it by about 0.01 dex), [-0.326, -0.152] (G-a), [-0.273, -0.133] (G-b). The passive cumulative ratios: 1.271 / 1.983 / 2.774 / 4.038 at x = 1.12 and 0.379 / 0.470 / 0.570 / 0.655 at x = 28.2 for 1e9 ... 1e12 Msun.

**T3 -- a prediction of the model class, NOT a data preference.** delta(z) = 2 log10[f(z)/f(0)], f = 1 - exp(-Gamma t(z)) (deep regime a0_eff proportional to f^2):

| cand (canonical) | z = 0.3 | 0.85 | 1.5 | 2.5 | 4.4 | 5.5 | category |
|---|---|---|---|---|---|---|---|
| G-H | -0.18 | -0.49 | -0.80 | **-1.19** | -1.72 | -1.95 | OUTSIDE THE CALIBRATION BAND |
| G-a | -0.24 | -0.62 | -0.98 | **-1.40** | -1.95 | -2.19 | OUTSIDE THE CALIBRATION BAND |
| G-b | -0.23 | -0.59 | -0.94 | **-1.35** | -1.90 | -2.14 | OUTSIDE THE CALIBRATION BAND |

(alt: G-a -1.39, G-b -1.33 at z = 2.5.) For comparison, as numbers only: the record's flat law 0.00; a0 proportional to H(z) +0.58 at z = 2.5; the T law t(z)/t_0 -0.51 at z = 1.5 and -0.72 at z = 2.5. The class's a0_eff falls with z, is steeper than the T law, and has the opposite sign to a0 proportional to H(z). The record's own T-law verdict was not robust (`STANDING_2026-09-29.md:104`) and every committed high-z compilation is calibration-limited; this row compares the class's prediction with the record's scored laws and the calibration band and **claims no preference of any data for any law**. The z = 0 value f(0) < 1 means the fitted kappa would be kappa_true f(0); kappa = 1/2 stays FITTED.

## 4. Gate C (post-hoc extra; the file is `CFG245_C_clusters_POSTHOC.out`)

- **C1** (X-COP identity, 12 clusters, 0.8 R500; Q = (M_b + M_class)/M_HSE; PASS iff median abs(Q - 1) <= 0.20 on both footings). Control C-C1 passes: Gamma = 0 gives median Q = 0.9457, the record's identity reading. Complete relaxation (the attractor) gives median Q = 0.493 (canonical) / 0.537 (alt): the law alone (committed eta = 2.03 / 1.86, a 17 / 15 sigma residual). C1 passes iff e_cl >= **0.680** (canonical) / **0.651** (alt), i.e. Gamma*tau_cl <= 0.386 / 0.429 (frozen hand 0.625 / 0.47: optimistic).

| cand | footing | tau_cl = 3.5 Gyr (generous): e / med abs(Q-1) | 7.9 Gyr (central) | 13.8 Gyr |
|---|---|---|---|---|
| G-H | canonical | 0.819 / 0.133 **P** | 0.637 / 0.221 **F** | 0.455 / 0.311 **F** |
| G-a | canonical | 0.966 / 0.068 **P** | 0.925 / 0.084 **P** | 0.873 / 0.109 **P** |
| G-b | canonical | 0.933 / 0.081 **P** | 0.856 / 0.117 **P** | 0.762 / 0.159 **P** |
| G-H | alt | 0.819 / 0.124 **P** | 0.637 / 0.206 **F** | 0.455 / 0.286 **F** |
| G-a | alt | 0.959 / 0.069 **P** | 0.910 / 0.087 **P** | 0.848 / 0.113 **P** |
| G-b | alt | 0.920 / 0.082 **P** | 0.828 / 0.120 **P** | 0.720 / 0.169 **P** |

R-FLUX-1 (fill-only) keeps the cosmic share (med abs(Q-1) = 0.054, the identity reading) for every candidate; nu_mono two-sided at the generous bracket 0.066-0.122, all PASS.
- **C2 (Bullet).** t_c = 0.1 Gyr (cores passed about 100 Myr ago, `opus_48_extended_research/reviews/bullet/bullet_data_table.py:150`); delta_B = 0.0057 (G-H), 0.0010-0.0012 (G-a), 0.0020-0.0024 (G-b); the flux-law enhancement max(1, median rho_ph/rho_c) = 1.00. PASS for every candidate. The Bullet does not bind.
- **C3.** Cold mass after relaxation (median, units M_b): two-sided 4.83 / 5.26 / 5.17 (G-H / G-a / G-b canonical; 4.88 / 5.26 / 5.15 alt) against the law's phantom 2.39 (canonical) / 2.70 (alt), the record's residual 3.47 / 3.14 M_b and Newtonian dark 5.73; fill-only 5.36 for all. The class supplies no mass of its own: it keeps the cosmic share or removes it toward the phantom.
- **Window (the pincer).** Generous joint bracket (tau_gal = 13.8, tau_cl = 3.5 Gyr): Gamma_T,min (0.10-dex line) = 1.73 H_Lambda, Gamma_C,max = 1.93 H_Lambda (canonical); 1.58 and 2.15 (alt): non-empty but containing none of the candidates (1.00, 0.17, 0.35 H_Lambda canonical; 1.00, 0.21, 0.42 alt). Central bracket (tau_gal = 10.5, tau_cl = 7.9 Gyr): Gamma_T,min = 2.27 / 2.07, Gamma_C,max = 0.86 / 0.95 H_Lambda: **EMPTY**. Gamma_G1,req (the T-G1 line) = 5.37 / 5.17 H_Lambda (generous), 7.06 / 6.79 (central), far above Gamma_C,max in both. R-FLUX-1: the window is empty by construction. The binding rule (no declared candidate inside) says FAIL. Disclosure (as in the frozen file): a rate of about 1.7 to 1.9 H_Lambda would sit in the generous window; 2 H_Lambda (= H_Lambda/kappa) lies above the canonical window (Gamma_C,max = 1.93) and inside the alt window (up to 2.15); it is not a declared candidate and earns no credit (the window is narrow and footing-dependent).

## 5. Gate A (post-hoc extra; `CFG245_A_supply_POSTHOC.out`)

- **A0, the supply ceiling.** S = frac_bound x M_out from the passive run = 26.02 M_b at all masses and brackets except 25.71 M_b at (1e10, q = 0.05); the target at x = 30 needs M_ph = 29.017 M_b. S/M_ph(<30) = **0.897** (0.886 at the one lower case) against the line 0.90: **FAIL by the frozen line, a knife-edge** (a 0.3-1.4% margin; one shell is 0.0039 M_b). x_cap = 27.0 (26.7), x(S/M_ph = 0.9) = 29.9 (29.6). The cosmic-share cap is x = 6.28. R_cum(x = 30) = 0.897 means -0.046 dex in g_tot at x = 30 and -0.019 dex at x = 28.2.
- **A1 (relaxed state, Gamma = infinity).** R_cum = 1 to machine precision for x <= x_cap at every mass: PASS as P-DECLARED (the evaluator control, not a result; the scale is supplied by the target). Exponential spheres: the relaxed fluid builds the LOCAL-FIELD target; its cumulative mass over the sims' C_44 cumulative target is 1.018-1.513 (1e9), 1.003-1.411 (1e10), 1.000-1.199 (1e11), 1.000-1.040 (1e12) canonical: the class cannot pass the shared G1 exponential-sphere cell against C_44 even at Gamma = infinity wherever that leaves [0.90, 1.10].
- **A2 (selectivity).** A Verlinde-shaped target (M_V = M_b x) is reproduced to 0.0: P-derived is impossible.
- **A3 (reported).** SHMR-halo supply (a declared function shape, f_ret from `CFG243_turnaround_dust/README.md:74`): S = 51.5 / 20.8 / 62.3 / 2680 M_b, S/M_ph(<30) = 1.78 / 0.72 / 2.15 / 92 (the 1e12 row is the record's flagged-absurd Moster inversion). The renormalised-amplitude reading: S/M_ph(<r_ta) = 0.135 / 0.199 / 0.293 / 0.433 (x_ta = 193 / 132 / 90 / 61), an amplitude spread 3.20 and an a0_eff spread of 1.01 dex across 1e9-1e12 (canonical; alt 3.19, 1.01 dex).

## 6. Gate E (post-hoc extra; `CFG245_E_ledger_POSTHOC.out`)

- **E1.** E_eq = W_c/2 (virial), W_c from the cumulative profiles; the passive profile beyond the last grid radius (x = 28.2) is not in the committed products, so two declared closures (all outer bound mass at x = 28.2 "near", or at the passive turnaround radius "far") bracket it and the verdict uses the smaller |Delta E| per case. Ratio |Delta E|/(1/2 M_b V_f^2) (= |Delta W| in G M_b^2/r_M) = 0.49 to 9.5 (generous closure; worst bracket q = 0.05 / 0.1 / 0.2: 8.64 / 9.06 / 9.55), up to 18.9 with the other closure, against the line 1: **FAIL**. The SIGN depends on the mass: energy must be REMOVED for 1e9-1e10 Msun (the target is more bound than the passive state) and SUPPLIED for 1e11-1e12 (the passive state has more mass inside x about 1 than the target). |Delta E|/(M_b c^2) = 1.6e-7 / 3.1e-7 / 2.7e-7 / 4.7e-6 (V_f = 59 / 106 / 188 / 334 km/s); against the vacuum energy of the turnaround ball 1.4e-7 to 4.0e-6 (CFG48 convention, 1.171 M_b c^2 reproduced) and 1.7e-9 to 2.7e-7 (B's law r_ta, 97.5 / 54.8 / 30.8 / 17.3 M_b c^2 against CFG243's 98 / 55 / 31 / 18).
- **Heating row** (reported only; limits from memory, unverified): a 1e11 Msun galaxy, |Delta E| = 4.8e58 erg, 1.1e41 erg/s averaged over t_0; not compared further.
- **E2.** The drift speed at the start of the relaxation, w = Gamma abs(M_target - M_inf)/(dM_inf/dr), is at most 121.6 km/s = 4.1e-4 c (canonical, G-H) and 112.7 km/s (alt): PASS the line 1e-3 c. Relativistic completion: UNDEFINED.
- **E3.** The relaxation block has the single eigenvalue -Gamma (sympy: div J = Gamma(rho_c - rho_ph); the discretised operator has all eigenvalues -1 in units of Gamma): PASS. The Lyapunov functional falls as exp(-2 Gamma t) (slope -0.114101 /Gyr, equal to -2 Gamma to 6 digits): PASS. E3(c), E3(d): NOT ADDRESSED. E4 (reaction): UNDEFINED.

## 7. How the frozen hand estimates fared (kept, wrong ones included)

| estimate (frozen) | result | |
|---|---|---|
| E-T1: P(T-G1 FAIL for all three) 0.95; Gamma*tau needed 4.7 against 0.79 / 0.14-0.16 / 0.27-0.33 | FAIL for all; needed 4.23 / 4.07; the others exact | held (the needed value 10% lower: the guard and the x <= 20 range) |
| E-T2: T-RAR G-H FAIL 0.62 / AMBIGUOUS 0.30 / PASS 0.08; G-a FAIL 0.99; G-b FAIL 0.97; P(some candidate not FAIL) = 0.35 | all three FAIL on both footings | held (the 0.65 side) |
| hand Delta numbers (x = 1.12 and 28.2); Gamma_req RAR 2.2-2.8 and 1.4-1.7 H_Lambda | +0.018..+0.165; -0.152..-0.083; 2.73 / 2.58 and 1.73 / 1.58 | held (x = 28.2 off by 0.01 dex: the cap) |
| E-T3: T3 category OUTSIDE BAND P = 0.97; |delta(2.5)| about 1.2-1.4 | all three OUTSIDE; -1.19 / -1.40 / -1.35 | held |
| E-T4: Gamma_req(G1)/H_Lambda in [5, 7] P = 0.85 (hand 5.9) | 5.37 / 5.17 | held |
| E-C1: complete relaxation FAIL (Q about 0.56) P = 0.99; generous bracket PASS all P = 0.85; central: G-H marginal PASS P = 0.5 | Q = 0.493 / 0.537; generous PASS all; central G-H FAIL (0.221, 0.206) | held, held, **wrong** (the line needs e >= 0.68 / 0.65, not 0.625) |
| E-C2: Bullet PASS P = 0.97 | PASS, max 0.0057 | held |
| E-C3: window non-empty at the generous bracket P = 0.55, [1.7, 2.4] H_Lambda; empty at central P = 0.80; P(C binds given reached) = 0.50 | non-empty [1.73, 1.93] canonical, [1.58, 2.15] alt (narrower); empty at central; C binds | held; the quoted upper edge 2.4 was wrong (1.9 canonical) |
| E-A1: A0 FAIL P = 0.75 with S = 22.6-25 M_b, ratio 0.78-0.86 | FAIL, but S = 25.7-26.0 M_b, ratio 0.886-0.897 | verdict held, **numbers wrong** (the bound shells beyond the turnaround add 3.4 M_b; the failure is a knife-edge) |
| E-A1 numbers x_cap 23.6-26.0, x(ratio 0.9) 26.1 / 28.8 | 26.7-27.0, 29.6-29.9 | wrong |
| E-A2: A1/A2 controls PASS, P-DECLARED P = 0.99 | as stated | held |
| E-A3: amplitude spread 3.2, about 1 dex in a0_eff P = 0.8 | 3.20; 1.01 dex | held |
| E-E1: FAIL P = 0.95; central ratio 20 (10-40) | FAIL; 0.49-9.5 (up to 18.9) | verdict held, **magnitude about 2x high and the sign wrong for 1e11-1e12** |
| E-E1: vacuum-ball ratio about 1e-5, below 1e-3 P = 0.8 | 1.4e-7 to 4.0e-6 (CFG48), 1.7e-9 to 2.7e-7 (B's) | held (below 1e-3); the central value 1e-5 was high |
| E-E2: drift speed PASS P = 0.95 (0.1-150 km/s) | max 121.6 km/s | held |
| E-E3: E3(a) PASS 0.95, E3(b) 0.97 | both PASS | held |
| G0: C-L1 pass 0.93, hand closed form 0.92 | PASS, worst 2.5e-4 | held |
| G0.2: DIFFERS 0.95; max R_loc 1.2-2.0 (P = 0.8 for [1.15, 2.5]); point mass 1.000 | DIFFERS; max 2.33 / 2.47; 1.0000 (2.5e-7) | held; the central range was low |
| G0.3: spherical min >= 0 (0.99) | held (min 8.8e-5 > 0) | held |
| G0.3: non-spherical f_neg > 0.01: two masses P = 0.65, thin disc P = 0.4 | two masses <= 9e-4 (negative pockets up to -0.02 in rho_ph near the saddle, tiny weight); disc 0 | **wrong** (both) |
| G0.5: ratio != 1 P = 0.98 | up to 3.16; FAIL | held |
| first binding gate: T 0.95, C 0.025, A 0.015, E 0.008, none 0.002 | T bound; C, A, E would each also bind on their own frozen lines | held |
| controls: reproduction controls pass at first run P = 0.7; at least one noise-limited or definitional control fails P = 0.4 | all seven passed at first run; no reproduction control failed | first held, second **not realised** (the only failed control is the MUTATE MG2 premise) |

## 8. MUTATE controls and failed controls (frozen expected exit codes; observed)

The frozen text says "15 MUTATE controls" but its table lists 16 ids (MG1-MG3, MT1, MT2a, MT2b, MT3, MM1, MC1, MC2, MA1, MA2, ME1, ME2, MN1, MN2); all 16 were run.

| id | change | target cell | expected | observed |
|---|---|---|---|---|
| MG1 | target replaced by C_44 | G0.2 DIFFERS -> IDENTICAL | bites (1) | **bites** (1) |
| MG2 | nu = 1 in the two-mass positivity test | f_neg cell UNDEFINED -> PASS | bites (1) | **does NOT bite (0): CONTROL FAILED** -- the baseline already passed (f_neg <= 9e-4 < 0.01), so there was nothing to flip; the frozen premise (baseline f_neg > 0.01) was a wrong estimate; kept, not repaired |
| MG3 | bound-only label added in G0.5 | ownership cell FAIL -> PASS | bites (1) | **bites** (1) |
| MT1 | passive state := target | T-G1 FAIL -> PASS | bites (1) | **bites** (1) |
| MT2a | Gamma = infinity | T-G1 FAIL -> PASS | bites (1) | **bites** (1) |
| MT2b | Gamma = 0 | C1 at the rate T-G1 requires: FAIL -> PASS (identity reading 0.946) | bites (1) | **bites** (1) [reading disclosed, section 9] |
| MT3 | flux sign flipped | Lyapunov cell E3(b) PASS -> FAIL (L grows x1.77 in 5 Gyr) | bites (1) | **bites** (1) |
| MM1 | creation form, no cap | A0 FAIL -> PASS; mass created +14.4 M_b | bites (1) | **bites** (1) |
| MC1 | one-sided (fill-only) | C1 at the rate T-G1 requires: FAIL -> PASS | bites (1) | **bites** (1) [reading disclosed] |
| MC2 | Gamma x 1e3 in the Bullet cell | C2 PASS -> FAIL | bites (1) | **bites** (1) |
| MA1 | true C(r), Gamma = S = infinity | A0 FAIL -> PASS | bites (1) | **bites** (1) |
| MA2 | S = 5.36 M_b | x_cap 26.97 -> 6.28 | bites (1) | **bites** (1) |
| ME1 | passive := relaxed (Delta E = 0) | E1 FAIL -> PASS | bites (1) | **bites** (1) |
| ME2 | damping sign flipped | E3(a) PASS -> FAIL | bites (1) | **bites** (1) |
| MN1 | P2 -> nu_mono in the T-RAR category | category (FAIL on all three both ways) | declared non-biting (0) | **does not bite** (0) |
| MN2 | canonical -> alt in the T-G1 category | category (FAIL on all three both ways) | declared non-biting (0) | **does not bite** (0) |

`unexpected outcomes: 1` (MG2). Reproduction controls (all PASS): C-L1, C-L2, C-T0 (at displayed precision, see section 9), C-T1, C-C1, C-A1, C-E1 (plus the extra C-E2).

## 9. Departures and ambiguities (each handled as the frozen file's rules require)

1. **Shared products.** The committed CFG244 sims JSON DOES hold the cumulative bound mass on the 0.1-dex grid (`runs[i].foot[footing].inst.Mc`, with the shell-bootstrap sd and the 5,000-shell runs), so NO CFG118/CFG244 code was imported or run; the JSON was read-only. The cluster arrays of `CFG4_clusters_results.json` were read-only. The one piece of record code exec'd read-only is FP1's nu_mono table slice (as CFG4_common does).
2. **C-T0 precision.** The frozen text said "to 1e-9": the committed README quotes 1-3 decimals, so the reproduction is at displayed precision (A2 ranges 7.99-10.73 vs 8.0-10.7; p = 0.3427 / 0.3392 / 0.3269 vs 0.343 / 0.339 / 0.327; the target to 3e-7).
3. **Supply S.** The frozen text defines S as CFG244's bound cumulative mass; implemented as frac_bound_all x M_out (all bound shells out to 3 r_ta) = 26.0 M_b, larger than my hand 22.6-25.
4. **E1 and the r_ta conventions.** The frozen text applied the line "in both r_ta conventions". Delta E here is the energy of the whole bound domain D and does not depend on the convention; the two conventions enter only the vacuum-ball ratio (reported). The outer part of the passive profile (beyond x = 28.2) is not in the committed products: two closures, verdict on the generous one.
5. **MT2b and MC1 baseline.** The frozen text says "C1: FAIL -> PASS" without saying at which rate; I evaluate C1 at the rate the T-G1 line requires (5.4 H_Lambda), where the baseline FAILs, and flip Gamma to 0 (MT2b) or to the one-sided law (MC1).
6. **MT3** is implemented in the E script (its target cell E3(b)); its effect on the T-G1 deviation is not printed separately.
7. **G0.4** is tautological by construction (a closed domain whose supply cap equals the mass inside): the mass inside D changes by exactly 0; the only non-trivial content is the non-negative shell masses. It is reported as PASS with that label.
8. **T-G1 guard** for the one-sided variant uses the factor 1 (lenient).
9. **G0.3 resolution.** Plummer softening 0.3 r_M, 4th-order differences, two resolutions (h = 0.25, 0.20); the null point is a singular point of the field and resolution-limited; the negative-mass fraction was stable between the two resolutions (9e-4 at d = 10).
10. **Frozen "15 vs 16" MUTATE count** (section 8).

## 10. What was NOT tested

A coupled dynamical simulation of the relaxation with back-reaction on the infall (only the linear-response model of Gate T; a faster nonlinear response would change the Gamma needed); non-spherical collapse, mergers and tidal fields (G0.3 and G0.5 are field computations only); a relativistic completion and any action (E2 causal cone, E4 UNDEFINED); the velocity-drag form; satellites and the Gate H populations (inherited from CFG244: H4, not re-run); Solar System and wide-binary safety beyond the statement that the label D, not the local form, excludes ambient fluid; the CMB, Boltzmann evolution and the cosmic amount (premise); the cosmic web and any extension of the local-field target to unbound regions; KiDS lensing, the forest, SN-Ia and the DR4 arms; numerical AQUAL (true-potential) solutions (the target is the QUMOND form); the velocity structure of the relaxed state beyond the quasi-static assumption; the heating limits beyond the reported ratios (from memory, unverified); any Gamma off the three declared candidates; the real assembly epochs (tau brackets only; the favourable bracket is deliberately generous and not physical). Literature facts marked "(memory)" are unverified. **Nothing here says the theory is closed or refuted; kappa = 1/2 stays fitted; the cold mass is still required; there is no dark-matter particle; a lean is not a detection; T3 is a prediction only and never a data preference.**

## 11. Files

`CFG245_common.py`, `CFG245_G0_target.py`, `CFG245_T_timescale.py`, `CFG245_C_clusters.py`, `CFG245_A_supply.py`, `CFG245_E_ledger.py`, `CFG245_verdict.py`, `CFG245_run_all.sh`; outputs `CFG245_G0_target.out` / `_results.json`, `CFG245_T_timescale.out` / `_results.json`, `CFG245_C_clusters_POSTHOC.out` / `_results.json`, `CFG245_A_supply_POSTHOC.out` / `_results.json`, `CFG245_E_ledger_POSTHOC.out` / `_results.json`, `CFG245_verdict.out` / `_results.json`, `CFG245_run_all.out`, and for each MUTATE `CFG245_<script>_MUTATE_<id>.out` / `_results.json` (16); this `README.md`. The frozen criteria are `../CFG245_FROZEN_CRITERIA.md` (63b7ad8e2).

## In-place re-run (orchestrator)

`CFG245_run_all.sh` was re-run in this directory (about 40 s; `CFG245_run_all.out` ends `unexpected outcomes: 1`, the MG2 premise failure kept as reported). Every `_results.json` is identical to the agent's apart from the `seconds` field; `.out` files identical. Verdicts, gate cells and table numbers are unchanged: T-G1 the binding FAIL for all three rates on both footings; T-RAR FAIL; C, A, E are post-hoc extras. Not blind: the frozen estimates restate CFG118/131/242/243/244; no CFG118/CFG244 code was run (the committed CFG244 sims JSON and the CFG4 cluster arrays were read-only). T-G1 was nearly decided by arithmetic, as the criteria said; the lane's content is the pre-specified extras. The frozen text says 15 MUTATE controls but its table lists 16; all 16 were run. Two things the README's extras say that qualify earlier hand reasoning: the energy sign for 1e11-1e12 is that energy must be supplied, not removed, and the supply ceiling S/M_ph(<30) = 0.886-0.897 misses its 0.90 line by a knife-edge.
