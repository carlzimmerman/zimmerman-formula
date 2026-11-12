# WM1 (warm component with law-boosted baryons): FROZEN CRITERIA, committed alone before any WM1 script or number

TEST lane, quarantined; registered RUNNING at 37e0da29ed (owner decision OWNER_DECISION_2026-11-09_WM1_LAUNCH.md, binding). The
no-particle rule is lifted for this lane only, as for HC1. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings
canonical (a0 9.3603e-11) and alt (1.1312e-10), never pooled. A FAIL is verified as hard as a PASS. Read-only machinery: SS1
(ss1.py run_local, ss1v.py VComp, ss1_core.py halos, ss1_cosmo.py BAO+SN / Limber / forest / fsigma8), SS4 (option (c) table,
Bullet child), SS5 (D1 two-fluid growth), HC1 (CLASS ncdm setup, G9 statistic), QX15 (qx15_like.py), QX3 iter2 (PR4 lensing).
Nothing in those lanes is edited; WM1 imports or execs them in its own processes.

## 1. Construction W, frozen once

**Species.** One thermal-relic fermion (CLASS ncdm, deg 1, Fermi-Dirac, HC1's setup with ncdm_fluid_approximation 3), the only
non-baryonic matter (omega_cdm 1e-7). Abundance omega_chi = R omega_b with each footing's QX15 main point (R 5.409 canonical /
5.411 alt; the record's 5.41). Mass m and temperature T_ncdm follow from M_hm (below): omega_chi = (m / 93.14 eV)(T_ncdm / 0.71611)^3.

**Baryons obey the law** g = nu(|g_N| / a0) g_N, nu(y) = 1/2 + sqrt(1/4 + 1/y), on the peculiar field (the record's convention,
SV5 / SS5); the component feels g_N only. Background: GR with the footing's bare Lambda.

**The warm suppression of a system's share.** S(M) = (1 + M_hm / M)^-1.16 (Schneider et al. 2012 WDM/CDM halo mass function ratio),
read as the fraction of a system's cosmic share that sits in collapsed structure at the system's mass M = M200 of its primary
halo. Each system's component is SS1's primary halo (KD1 P3: truncated SIS at z 0.55, M_chi0 = f_cap R M_b, f_cap 0.76) times
S(M200): M_chi(<r) = S(M200) M_chi0 min(r, R200) / R200. Members (Coma UDGs) use their own halos (UA1, reported).

**M_hm, fixed ONCE by a stated rule (no scan).** S at the heaviest KiDS isolated-lens bin's primary halo equals option (c)'s
smallest allowance:
- heaviest KiDS bin: log M_b 10.9, primary M200 = 4.060e11 Msun, R200 127 kpc (SS1 parts/local.json, primary_SIS, G1 per_bin);
- option (c), the compact limit R_c 0.12 Mpc: f_gal max 0.050 (SS4 RESULT; the primary halo is compact, R200 < 0.13 Mpc);
- S(4.060e11) = 0.050 gives M_hm = (0.050^(-1/1.16) - 1) x 4.060e11 = **4.97e12 Msun** (same on both footings).

**Relic mass from M_hm (standard thermal-relic transfer function).** Viel et al. 2005:
T(k) = [1 + (alpha k)^(2 nu)]^(-5/nu), nu 1.12, alpha = 0.049 (m/keV)^-1.11 (Omega_chi/0.25)^0.11 (h/0.7)^1.22 h^-1 Mpc;
half-mode T = 1/2, lambda_hm = 2 pi / k_hm, M_hm = (4 pi / 3) rho_m (lambda_hm / 2)^3. Result (computed from the formula only):
**m = 188.6 eV**, lambda_hm 6.20 Mpc, k_hm 1.50 h/Mpc, T_ncdm 0.2799 (canonical; alt the same to 1e-4).
- Brackets, reported only, never graded: M_hm x 1/3 (1.66e12; 262.4 eV, T_ncdm 0.2508) and x 3 (1.49e13; 135.6 eV, 0.3124).
- MUTATE values: x 10 (4.97e13; 94.5 eV, 0.3525) and / 10 (4.97e11; 376.6 eV, 0.2223).

**Form choices beside the label:** the S(M) form and exponent 1.16, the M200-of-primary-halo argument, the 0.050 anchor, the
Viel fit, ncdm deg 1. Fitted: 0 (M_hm is set by the rule above from two record numbers).

**Reading R-acc (reported, never graded).** S = 1 in every system: the warm cutoff does nothing to secondary infall of the
component onto the wells the law-boosted baryons dig. This equals SS1 MG3 / SS4 MK1 (full share in the primary halo; KiDS 0.378).
It is the physical objection to S, stated now; the lane reports which reading the dynamics favour in RESULT, from D1 only.

## 2. Linear growth with the baryons on the law (SS5 D1, read-only form)

For each footing, at the KG x ZG grid of ss1_cosmo.py (100 k from 1e-4 to 200 Mpc^-1; z 0.02-20) and ss1v's fine z grid
(0-1.2, 241 points):
- delta_chi'' + (2 + dlnH) delta_chi' = (3/2)(Omega_chi delta_chi + Omega_b delta_b);
- delta_b'' + (2 + dlnH) delta_b' = (3/2) nu(k, z)(Omega_chi delta_chi + Omega_b delta_b);
- start z 1090 (delta_b = 0, delta_chi growing mode), SS5's convention; nu(k, z) = nu(y), y = |delta g_N| / a0,
  delta g_N = (3/2) H0^2 Omega_m delta_rms(k, z) / (a^2 k), delta_rms from **the warm model's own CLASS linear power** (SS5 used
  the cold reference; the warm P has less power above k_hm, so y is smaller and nu larger there). Above z 20, EdS scaling as SS5.
- B_m(k, z) = delta_m(law) / delta_m(nu = 1) from the same initial condition; B_b(k, z) = delta_b(law) / delta_m(nu = 1).
- Total matter ratio to the record's cold reference: R_m(k, z) = sqrt(P_warm / P_ref)(k, z) x B_m(k, z), with P_warm from CLASS
  (Newtonian, it carries free streaming) and P_ref the ss1_cosmo cold reference. Disclosed factorisation: free streaming from
  CLASS, the law's boost from the two-fluid ODE (linear in the initial amplitude, so B does not depend on the warm IC shape).
  The baryon (gas) tracer ratio R_b = sqrt(P_warm / P_ref) x B_b is reported beside.

**Does SV5's statement apply?** Yes, by construction: WM1 is a member of SV5's class W (a sector supplying the Newtonian source
with the law on the linear web). The cutoff changes only y above k_hm. RESULT states the boost WM1 actually gets.

## 3. Gates, lines, label

| # | gate | statistic and line |
|---|---|---|
| 1 | KiDS isolated lenses | SS1 gate 1 (59 Brouwer+2021 points, pointwise, \|shift\| <= 0.05 each) |
| 2 | groups (Lovisari 20) | SS1 gate 2 (>= 16 of 20 at f* = 0 and 1) |
| 3 | X-COP | SS1 gate 3 (amount \|mean\| <= 0.05, rms <= 0.10; per-bin within 0.10); retained / M_dyn per bin vs TR1 0.71 / 0.66 / 0.58 reported |
| 4 | Coma UDGs | SS1 gate 4, reported (UA1) |
| 5 | SPARC | SS1 gate 5 (+F2) |
| 5b | Ursa Major | SS1 gate 5b (EV1) |
| 6 | BAO + SN | ss1_cosmo bao_sn (DESI DR2 + Pantheon+), CLASS warm background and r_d vs the cold reference at fixed h: Delta chi^2 <= 4 |
| 7a | CMB primary | qx15_like PA (Pcut + ACT), nuisances profiled, CLASS lensed TT/TE/EE warm minus CLASS cold at each footing's QX15 main point (no refit; a refit only lowers Delta): <= 4 PASS, 4-25 TENSION (blocks), > 25 FAIL |
| 7b-N | CMB lensing at the cutoff (footing-free) | HC1 G9 exactly: cfg917_lib PR4, A_s fitted, 8 corners (omega_b 0.0215/0.0230, H0 65/75, n_s 0.95/0.98), omega_chi = 5.41 omega_b, m fixed: worst corner chi^2 <= 18.48 |
| 7b-L | CMB lensing with the law on the web | QX3 iter2 G1 statistic at each footing's point: X = X_warm(CLASS) x S_B(L), S_B = Limber[P_warm B_m^2] / Limber[P_warm] (ss1_cosmo limber4_bg kernel): chi^2 <= 18.48 |
| 8 | forest z 2-4 + fsigma8 | ss1_cosmo forest_eval on R_m (DESI DR1 P1D, Delta chi^2 <= 4); fsigma8 by ss1v's fine-grid rule (DESI DR1 rows, both columns within 2 sigma, ratio <= 1.001). R_b forest reported |
| CS | small-scale power / shear | SS4's line: \|S8 / S8_ref - 1\| <= 5.9 % with R_m; P / P_ref at k 0.3, 1, 3 h/Mpc, z 0.3 and 0.5 reported; Newtonian warm (B = 1) beside |
| 9 | Bullet | DB1 child (SS4's bchild), galaxy-traced (collisionless relic); component inside R200 of each subcluster = S(M200) x primary; gas-traced reported |
| 10 | Cassini | SS1 gate 10 |

**Label:** PASS iff 1, 2, 3, 5, 5b, 6, 7a, 7b-N, 7b-L, 8, CS, 9, 10 all pass on that footing; otherwise FAIL, naming the first
failing gate in that order. KiDS 2-halo: the record's KiDS machinery is pointwise from the lens's own enclosed mass; no 2-halo
model exists in the record, so it is NOT EVALUATED, with a hand estimate stated in RESULT.

## 4. Hand estimates and expected kills (before any number)

- **KiDS:** passes by the M_hm rule at the heaviest bin (S 0.05); lighter bins S < 0.02. Not a test of W; the rule spends it.
- **SPARC / UMa / Cassini:** pass (S <= 0.06 at M_b 1e11).
- **Groups:** primary M200 0.5-5e13 gives S 0.45-0.91, i.e. 1.4-3.7 M_b against a need of about 1.2-3.5: may pass.
- **X-COP: expected FAIL (kill 1).** S >= 0.98 at 1e14-1e15: the full share in the primary halo, as SS2's G (1.57 / 0.90 / 0.75
  of M_dyn vs TR1 0.71 / 0.66 / 0.58) and SS1 MG3. Over-filled and too concentrated in the inner bin.
- **Coma UDGs:** S ~ 1e-4: law alone, +1.1 dex (reported, as HC1).
- **BAO + SN, CMB primary:** pass (the relic is non-relativistic before z 1e5; Delta N_eff about (0.28/0.716)^4 = 0.02).
- **7b-N:** probably passes: k_hm 1.5 h/Mpc sits above the lensing kernel's k 0.02-0.3 h/Mpc; a few % at L 400 (the orchestrator
  expected a kill here; the estimate says no).
- **7b-L, 8, CS: expected FAIL (kills 2-3, the SV5 wall).** SS5 D1 gives delta_b / delta_chi 6.5-18 at z 0, so delta_m grows about
  2-4x and lensing power about 10-100x (SV5: 75-89x); sigma8 roughly doubles; d ln delta / d ln a > the reference so fsigma8's
  ratio exceeds 1.001; the forest sees P1D boosted by B^2.
- **Bullet:** galaxy-traced full share in both subclusters: pass likely (cold-like at 1e14-1e15).
- **Label expected: FAIL / FAIL, first failing gate 3 X-COP.**

## 5. Known answers (NO VERDICT if KA-W1, KA-W2 or KA-W3 fails)

- **KA-W1:** HC1's G9 with its 11.1377 eV relic (omega 0.11958, T_ncdm 0.71611): worst / best corner chi^2 194.2 / 166.0 within 0.2.
- **KA-W2:** my vectorised D1 solver with the cold reference P and SS5's settings reproduces SS5's own D1 (ss5.py executed
  read-only up to its D2 section) at k 0.1 / 0.3 / 1 / 3 h/Mpc and z 3 / 1.2 / 0 within 1 %, both footings (SS5's printed
  canonical z 0: 6.52 / 7.87 / 11.4 / 17.6).
- **KA-W3:** CLASS omega_ncdm equals the target within 1 %; CLASS's own half-mode k (P_warm / P_cold = 1/4 at z 0) is reported
  beside the Viel fit's 1.50 h/Mpc (disclosed if they differ by more than 25 %).
- **KA-W4:** component -> 0 replay of the local gates (SS1 KA3).

## 6. MUTATE (separate outputs)

- **MW1 (M_hm x 10, 94.5 eV) and MW2 (M_hm / 10, 376.6 eV):** the per-gate status vector must change against the main run on
  at least one footing for each; otherwise that MUTATE is NO BITE (disclosed).
- **MN (baryons Newtonian, B = 1):**
  - MN0, cold limit (omega_cdm = omega_chi, B = 1): R = 1, the forest Delta chi^2 = 0 and the lensing chi^2 = the reference
    (8.56) to 1e-6: the pipeline reproduces the cold-relic forest.
  - MN-W (the 188.6 eV relic, B = 1): the forest must FAIL (thermal relics of 0.2 keV are far below published forest bounds); if it
    passes, the forest gate has no power at this cutoff and that is disclosed (NO POWER on gate 8's forest half).

## 7. Operational

- One thread, nice 10; RSS < 1 GB except CLASS (disclosed); outputs small json/out, no arrays dumped beyond grids needed.
- Disk at about 3.9 GiB free: no scratch kept; chain stops under 2 GiB.
- Files: wm1_local.py (gates 1-5b, 10, Bullet), wm1_cosmo.py (CLASS, D1, gates 6-8, CS, KA-W2/W3, MN), wm1_hc1.py (7b-N, KA-W1),
  wm1_grade.py, wm1.json / .out, wm1_MUTATE.json / .out, RESULT.md.
- Explicit-path commits via a sparse temporary worktree of origin/main, removed after.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
