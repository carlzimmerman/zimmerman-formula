# CK4 frozen criteria: cosmology under the kicked collisionless carrier (RESOLUTION_2026_11_07 lane CK4)

Frozen before any CK4 script or CK4 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (owner 11-04
rule; RESOLUTION_2026_11_07.md section 3, lane CK4; FRAMEWORK CANDIDATE 51cd404f0c registers it). The id CK4 is free in
closure_2026_11_07/ (fable_independent_2026/clock_swarm_2026/CK01-CK02 are a different series, 4-digit names, unrelated).
Name: cold dark energy (the vacuum carrier's cold phase), never cold dark matter; no particle; no LCDM parameter values.
Both footings where a0 enters (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2), never pooled; every gate below is a
linear-cosmology gate in which a0 does not enter, so it is stated once for both footings (as CE2's CMB-side gates). No
downloads. One thread; RSS < 1 GB (disclosed if exceeded).

## 0. The object (as RESOLUTION section 1-2 and L365/L388 define it; no new constant beyond the declared brackets)

- **Parent:** a cold, collisionless phase at the CMB's amount: omega_d 0.11958 on QX7 iter_4's background (QX3 iter2 worst
  corner: omega_b 0.0215, H0 65, n_s 0.95), the background CE2 used, so CE2's cold reference is this lane's v_k = 0 case.
  It feels Newtonian gravity of the total field (kernel-invisible, L365 spec (1)).
- **Trigger (posited, no action; L365/L388):** parent mass converts to daughters when it virialises in a halo of mass
  M >= M_min. M_min primary 1e11 Msun (L388's trigger: x~ >= 2.5 on a 0.39 Mpc/h mesh, ~20 mesh cells of 5e9 Msun/h);
  brackets 1e10 and 1e12 Msun reported and labelled, not part of the CANDIDATE label.
- **Daughters:** same mass (non-relativistic; w ~ v^2/3c^2 ~ 1e-6, background unchanged), isotropic kick of speed v_k,
  collisionless. v_k in {550, 575, 600} km/s, each labelled.
- **Production history (no LCDM input):** collapsed fraction F(>M, z) from Sheth-Tormen (p 0.3, q 0.707, delta_c 1.686)
  on the parent's own linear power (the cold reference CLASS model of QX3/iter_4, MC.pk_lin, top-hat sigma(M)). Parent mass
  converts at the rate dF(>M_min)/dlna (> 0; clipped at 0).
- **Escape (primary, reading B):** a daughter escapes its halo if v_k > v_esc(M, z), with v_esc = 2.69 v_vir (NFW c = 5,
  potential at r_s; declared, not derived; v_vir from Delta_vir = 18 pi^2 in the parent's background). Escaping daughters
  keep v_inf = sqrt(v_k^2 - v_esc^2). Daughters born in halos with v_esc >= v_k stay bound and are counted with the parent
  (cold; they cluster with their halo). The newly converted mass is split over halo mass by d/dlna of dF(>M)/dlnM (positive
  part) between M_min and infinity.
- **Reading A (harsh bracket, reported and labelled, not in the CANDIDATE label):** every converted daughter escapes with
  v_inf = v_k.
- **Linear treatment:** the escaped daughters are a fluid with sound speed equal to their 1D velocity dispersion,
  sigma^2(a) = sum over births of (v_inf^2/3)(a_birth/a)^2 (mass-weighted), the standard free-streaming-scale matching
  (k_fs = sqrt(3/2) aH/sigma). Born with the parent's local delta and velocity (linear; halo bias at birth not modelled,
  disclosed). Equations in ln a with Theta = -d delta/dlna for each species (cold parent c, escaped daughters d, baryons b):
  delta_c' = -Theta_c; Theta_c' = -(2 + dlnH/dlna) Theta_c - 1.5 S;
  delta_d' = -Theta_d + r (delta_c - delta_d); Theta_d' = -(2 + dlnH/dlna) Theta_d - 1.5 S + (sigma k / aH)^2 delta_d
  + r (Theta_c - Theta_d); baryons as QX3's solver (after a_dec); S = Omega_c(a) delta_c + Omega_d(a) delta_d +
  Omega_b(a) delta_b; r = (dF_esc/dlna)/F_esc. Same implicit trapezoid scheme and grid as QX3 iter3 / iter_4's solve_gen.
  R(k, z) = delta_m(kick) / delta_m(v_k = 0) from the same solver; the v_k = 0 run must equal iter_4's ref (KA).

## 1. Gates (per v_k; primary = reading B at M_min 1e11)

| Row | Statistic | PASS line | Source |
|---|---|---|---|
| GL CMB lensing | iter_4's G2' machinery exactly as CE2 (I2.limber_ratio on N3's kgrid x zgrid with R(k, z), raw PR4 9 bandpowers L <= 400, A_s refit): chi^2 = c0 + Delta chi^2 | chi^2 <= 18.48 AND Delta chi^2 <= 4 | QX3 iter2 / CE2 GL |
| GF fsigma8 at z < 1 | CE2's fs8_ratio on R(k, z) (sigma8 from the cold reference P_lin x R^2, fsigma8 = d sigma8/dlna) | at BGS 0.295, LRG1 0.510, LRG2 0.706, LRG3 0.919: Rf <= 1.001 AND \|Rf - r_DESI\| <= 2 err on BOTH DESI DR1 Table 9 panels (CE2's transcription, errors symmetrised) | CE2 GF |
| GFo forest (daughters' free streaming) | linear 1D matter power ratio P1D_kick / P1D_cold, P1D(k_par) = (1/2pi) int_{k_par}^{k_max} k P(k) dk, k_max 50 h/Mpc, same solver on an extended k grid, at z = 2, 3, 4 | \|1 - ratio\| <= 0.10 at every k_par in 0.2-2 h/Mpc (11 log points) and every z (L365's G2 10 % band; linear proxy for the flux power, disclosed) | L365 G2 |
| GEB early black hole (cold parent) | EB1's timing gate for A2744-QSO1 (z 7.0451; Eddington seed time, eps 0.1, M_seed 1e5 Msun, M_BH 10^7.7 and 10^6.9; clump M_clump = 10 M_seed of baryons) with the cold parent clustering: halo mass M_h = M_clump (1 + omega_d/omega_b); Newtonian spherical collapse (delta_c 1.686) on sigma(M_h, z) of the cold reference linear power; nu_req = smallest nu in {1..5} with t(z_coll) <= t_seed | EASY (nu_req <= 2) or RARE (2 < nu_req <= 4) on both M_BH = PASS; EXTREME / NO = FAIL. Daughters are reported (escaped fraction at z 7.05); they enter only if that fraction exceeds 1e-3, in which case sigma is taken from P_lin x R^2 at z 7.05 | EB1 (7ac6bbb3f9) |

- The GEB A_s: the GL machinery's own reference (N3's CLASS model as CE2), not EB1's baryons-only A_s 2.1e-9 (that run had no
  cold sector). EB1's R0/R1 rows (no cold sector) are not reproduced here; GEB is a new row.

## 2. Labels

- Per gate x v_k x reading x M_min: PASS / FAIL / NO VERDICT (a known answer for that gate fails, or a MUTATE that must
  bite does not).
- **CK4 PASS at v_k** if GL, GF, GFo and GEB all pass at that v_k in the primary (reading B, M_min 1e11).
- **CK4 label:** PASS if at least one v_k in {550, 575, 600} passes; FAIL otherwise, naming the blocking gate(s) and the
  size of each miss. The brackets (reading A; M_min 1e10, 1e12) are reported with their own labels and the lane says
  whether the PASS survives them.

## 3. Known answers (a KA FAIL stops the grade of the gates it covers)

- KA1 (CE2 where the physics coincides): the new solver with no daughters (v_k = 0) returns iter_4's ref to 1e-9 relative
  at every (k, z), so CE2's cold reference c0 is reproduced to 0 (GL chi^2 = c0, Delta chi^2 = 0 to 1e-6), CE2's KA4
  Rf = 1 at R = 1 to 1e-6, and CE2's four CMB-side passes are the same machinery (iter_4's K1 55.6403 reproduced to 1e-6).
- KA2: the solver with the daughters' sound speed replaced by iter_4's Jeans term for ALL the dark component (F = 1 from
  a_i, k_J from C1) reproduces CE2's C1 Delta chi^2 0.31 (iter_4's 0.3111) to 1e-6 (the pressure term is wired the same
  way).
- KA3: Sheth-Tormen collapsed fraction F(>M_min, z) at z = 0 is between 0 and 1 and decreasing in M_min (sanity), and the
  free-streaming wavenumber printed at z = 1 for v_inf = 575 km/s equals sqrt(3/2) aH / (575/sqrt 3) to 1e-6.

## 4. MUTATE (separate outputs ck4_MUTATE.*; each must bite)

- M1: daughters at v_k = 3000 km/s (primary reading) must FAIL GL (Delta chi^2 > 4 or chi^2 > 18.48).
- M2: v_k = 0 must reproduce the cold case (KA1: R = 1 to 1e-9, Delta chi^2 = 0) and pass every gate; it is the
  cold-sector control and is not a candidate in itself.
- M3: reading A at M_min 1e8 Msun (production in every small halo from z ~ 6) must FAIL GFo.

## 5. Reported, not graded

- F_conv(z) and F_esc(z) at z = 0, 0.5, 1, 2, 3, 5, 7 per v_k; sigma(z); k_fs(z).
- sigma8 ratio at z = 0 (S8 direction) and R(k, 0) at k = 0.1, 0.3, 1 /Mpc.
- Note (not graded): the record's L388 boxes found S8 0.96-0.98 of their LCDM-IC reference and the forest within 4 %;
  those used LCDM ICs and are not reproduced.

## 6. Outputs

ck4.py writes ck4.json / ck4.out (and ck4_MUTATE.*). RESULT.md: gate x v_k table, labels, brackets. Gates may be built by
subagents (GEB separately); every number in RESULT.md comes from committed scripts. Any change after this freeze is
disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
