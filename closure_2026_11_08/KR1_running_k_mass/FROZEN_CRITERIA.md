# KR1 frozen criteria: a running K-mass from a non-quadratic K(Q)

Frozen before any KR1 script or KR1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane under
the owner's 11-04 rule (test lanes may reopen frozen items): it reopens v3s's K(Q) sector, which is cold dark energy, never
dark matter, and has no particle. Brief: `closure_2026_11_08/KR1_KR2_BRIEF_2026_11_08.md` (4056ce3a48), tightened where
stated below, never loosened. Both footings (canonical / alt, as F1A and GB1 define them) are graded separately and never
pooled. Raw data or framework-native inputs only; no LambdaCDM parameter values. One thread, RSS < 1 GB, no downloads.

## 0. Record check (done before this file; it changes the framing, not the question)

- **The brief's "361".** No growth line of 361 Mpc^-1 exists in the record. The corrected-kernel constant-mu growth/lensing
  line is **631 Mpc^-1** (GL1 L2/L6: mu_min_n4 = 630.957 at every QX3 iter2 corner; 936 h/Mpc at h 0.674). 631 is
  read as the brief's digit transposition and used: it is the tighter line. The 361 reading is reported, not graded.
- **The brief's "198 at z 3400"** is KD1 B1a's quadratic-K value of mu for w(z 3400) <= 0.01. For a running K the line is
  the statistic itself, w(z 3400) <= 0.01 (B1a below), not a mu value.
- **"Non-quadratic K" and "running" are in the record under other names.**
  - Q7 (`rebuild_2026_10_22/Q7_bs25_cosmology`) graded Blanchet-Skordis's own DBI K at galaxy-cap mu: BBN fixed,
    growth fails; the growth door needs lambda_D,95 = 7.8e9 at the cap; X4 closed that corner with the forest.
  - QX3 iter3 graded the power-law class K ~ (Q-1)^n (lambda_J ~ rho^beta) on a grid; GL1 L3 re-read it with the corrected
    kernel and found one member passing lensing (beta 0.8, mu0 1259 Mpc^-1). Its BBN and primary CMB were never graded.
  - What is NOT in the record: a K whose mass has run up by z 3 to the corrected growth line (Q7's members run only at
    z >~ 40) and that is graded on BBN, primary CMB, corrected-kernel lensing, fsigma8, P1D, statics and galaxy capture
    together. That is this lane.

## 1. Equations (certified forms, unchanged; nothing new is added to the action)

- Action v3s: (c^3/16 pi G) Int sqrt(-g) [R - 2 J(Y) + 2 K(Q)] + stiffness + S_m (EQUATIONS_IN_ORDER section 1, QX17/QX17D
  field equations; the Pi^6 blend in the P sector is untouched). Only the function K changes.
- FRW (QX17B `frw_dust`; BS24 Eqs. 14-16 as Q7 S3 checked): the khronon's shift charge is conserved, K'(Qbar) = I0/a^3;
  8 pi G rho_K = Qbar K' - K; 8 pi G p_K = K; w = K/(Qbar K' - K). The 11-06 FRW reconciliation (1-z)^2 factor concerns
  AC2q's lapse term and does not enter the v3s K(Q) background (stated; the stiffness stress is zero on FRW).
- Linear kernel (Q7 S8, exact for any K; = U1 / BSK2 kernel at Qbar = 1, K'' = 2 mu^2): hold k > a M with
  **M^2(a) = Qbar^2 K''(Qbar)/2**. This is the brief's mu_K(z). For a cold sector it is also the Jeans wavenumber
  k_J^2 = 4 pi G rho_K / c_s^2 with c_s^2 = K'/(Q K'') (to O(w)).
- Static weak field, stationary branch (KD1 P1; QX17 "static, weak"; BS25 Eq. 13): delta Q = -psi/c^2, i.e. inside a bound
  system the khronon charge is q = Q - 1 ~ |psi|/c^2, which is a kinematic relation (Q = 1/N for a static khronon) and
  does not depend on K.
- Q is a local scalar. For convex K (K'' > 0), rho_K(Q) is strictly increasing (d rho/dQ = Q K''/8 pi G), so **M is a
  single-valued function of the sector's own local density, M = M(rho_K)**, in the background and in every collapsed
  region alike (any K(Q) is a barotrope; QX3 iter3's class statement, here without the power-law restriction).

## 2. The family (frozen): Blanchet-Skordis DBI

    K(Q) = (2 mu^2 / lambda) [1 - sqrt(1 - lambda q^2)],   q = Q - 1,   mu > 0, lambda >= 0.

Why it is the natural generalisation of the quadratic K:
1. It is the only non-quadratic K written by the action's own authors (BS24 Eq. 87, BS25 Eq. 6); KR1 adds no new function.
2. lambda -> 0 gives mu^2 q^2 exactly (Q7 S1); K(1) = K'(1) = 0 and K''(1) = 2 mu^2 are kept, so the static weak-field
   coefficient of row 2.5 is unchanged at Q = 1.
3. It is the minimal way to evade the stiff-partner theorem: K' = 2 mu^2 q/sqrt(1 - lambda q^2) diverges at the finite charge
   q_max = lambda^(-1/2), so dK/dQ is not asymptotically linear; Qbar stays below 1 + q_max as I0/a^3 -> infinity and
   w -> 0 early (no a^-6 phase).
4. Its mass runs with the background: with Z = I0/(2 mu^2 a^3) and r = sqrt(1 + lambda Z^2) (Q7's cancellation-free forms):
   Qbar = 1 + Z/r, K = 2 mu^2 Z^2/(r(r+1)), K' = 2 mu^2 Z, K'' = 2 mu^2 r^3, so **M = mu Qbar r^(3/2)**: M -> mu late and
   M ~ mu (lambda Z^2)^(3/4) ~ a^(-9/2) early. It runs the right way (larger early).
   Background excess over dust: 8 pi G rho_K - I0/a^3 = 2 mu^2 Z^2/(r + 1) (lambda = 0: I0 w0/a^6, KD1's stiff part).

**Amplitude (fixed once, per footing):** I0 = 3 (100/c)^2 omega_d [Mpc^-2] with omega_d = F1A's B2 best-fit oc
(canonical 0.120941676, alt 0.120892958; F1A RESULT G3: omega_d/omega_b 5.410 / 5.412). Nothing refits it.

**Parameters fixed by the constraints, not scanned.** (i) does not bind (section 3). (ii) binds at its lowest redshift,
because M decreases monotonically with a (checked on the grid): lambda is fixed by **M(z = 3) = 630.957 Mpc^-1** exactly
(brentq in log lambda). That leaves the action constant mu as the one free direction of the constraint set. KR1 grades four
members on that curve, at the record's own landmarks for mu (not chosen by any KR1 number):

| member | mu (Mpc^-1) | landmark |
|---|---|---|
| D0 | 1e-3 | two decades below S4's isolated-galaxy guard (probes the small-mu end of the curve) |
| D1 | 0.1 | S4 guard |
| D2 | 9.998 | BS24 galaxy cap (mu^-1 = 100 kpc) |
| D3 | 79.4328 | QX3 G3 capture bound |

**mu_K(0) = M(z = 0) is READ** for each member, and the curve's infimum of mu_K(0) is reported (analytically
M_line (a3)^(9/2) = 630.957/4^4.5 in the early-regime limit; numerically on the members).

## 3. Columns (per member x footing; PASS line, source)

| Col | Statistic | PASS line | Source |
|---|---|---|---|
| B1a cold at z 3400 | w(z 3400) | <= 0.01 | KD1 B1a |
| B1b BBN (i) | X = (8 pi G rho_K - I0 a^-3) / (3 (100/c)^2 omega_r a^-4) at T 0.1 MeV (1+z = 1e5 eV/(k T_cmb), T_cmb 2.7255 K), omega_r = 2.47e-5 (1 + 0.2271 x 3.046) | <= 0.067 (Delta N_eff <= 0.5) | KD1 B1b, generalised (equals KD1's statistic at lambda = 0) |
| R2 running line (ii) | min M(z) over z in [3, 1100] (200 log points) | >= 630.957 Mpc^-1 (PASS by construction at z 3; graded to catch non-monotone M) | GL1 L2 |
| C1 primary CMB at mu_K(1100) | the F1A/QX15 cold fit applies unchanged iff over z in [100, 3400]: (a) w <= 1e-3; (b) comoving hold a M >= 10 k_max with k_max = 0.25 Mpc^-1 (TT ell 2500 at chi* ~ 13.9 Gpc); (c) abundance rho_K a^3 / (I0/8 pi G) within 1e-3 of 1 at z 1100 | (a), (b), (c) all hold; the replayed cold fit (KA2) is then the column's chi^2. The residual hold factor (k_max/(aM))^2 is reported | F1A / QX15 |
| GL CMB lensing (corrected kernel) | CK4/CE2 engine: three-species solver `solve3` with every dark element in the Jeans slot, kJ(a) = M(a); R = delta_m / ref on N3's kgrid x zgrid; GL1's `limber_n` with n = 4 (GL2-confirmed k^-4); raw PR4 9 bandpowers L <= 400, CMB-marginalised covariance, A_s refit | chi^2 <= 18.48 AND Delta chi^2 <= 4 | GL1 / GL2 d0c3692fc6 / QX3 iter2 |
| GF DESI fsigma8 | CK4's fs8_ratio + fs8_gate on R(k, z) | CK4's line (Rf <= 1.001 and within 2 err on both DESI DR1 Table 9 panels, BGS + LRG1-3) | CK4 / CE2 |
| GFo forest P1D | CK4's linear P1D ratio on the extended grid, z 2, 3, 4, k_par 0.2-2 h/Mpc | \|1 - ratio\| <= 0.10 everywhere | CK4 / L365 G2 |
| CT tensor speed | analytic: K depends on Q = (-g^{mu nu} d tau d tau)^(1/2) only; transverse-traceless h_ij leave Q unchanged at linear order and the K-fluid has no anisotropic stress, so the tensor equation is GR's for any K | c_T = c | QX17B (c_T = c) |
| S0 stationary branch exists | q_max = lambda^(-1/2) against the khronon charge the stationary branch needs: Solar System at 1 AU GM_sun/(c^2 AU) = 9.87e-9; Milky Way v_c^2/c^2 = 5.38e-7 (220 km/s); cluster 1.11e-5 (1000 km/s). v_c^2/c^2 under-states \|psi\|/c^2, so these lines favour the candidate | q_max >= each line (three sub-rows; the column passes only if all three pass) | Q7 section 0 item 3 / section 8 (there reported, PROVISIONAL; graded here, which tightens) |
| CS Cassini | P sector and stiffness untouched, so the screening of record (X3, CW lanes) is unchanged IF the stationary branch exists at the Sun; the K near-field (M_loc r)^2/2 at Saturn (9.58 AU) with M_loc = M at q = 9.87e-9 + 5.38e-7 | S0 Solar System and MW sub-rows PASS AND near-field <= 2.3e-5 | KD1 reported line, EQUATIONS 2.5 |
| GC galaxy capture | dust at a galaxy's turnaround: rho_ta = 5.55 (1 + z_c)^3 rho_K0 at z_c = 2 (QX3 G3 convention); M_ta = M(rho_ta) from the exact inverse of rho_K(Q); captured iff 2 pi / M_ta < r_ta = 0.234 Mpc (QX3 G3' line) | NOT captured | QX3 G3 / G3' |
| G1-G8 (only if GC captures; reported as the consequence) | KD1's model P battery (`kd1.py` exec'd read-only: KD, grade, GB1 gates) with the constant mu replaced by M_ta, the lowest local mass the captured dust has (M rises with density for DBI, so this is the most favourable reading, KD1 P5) | GB1's lines | KD1 / GB1 |
| (iii) today | mu_K(0) read | <= 79.4328 (QX3) graded; <= 0.1 (S4) reported; KR2's window graded if it arrives before RESULT.md, said so either way | brief (iii) |

## 4. The family-free ordering (stated before any number; the script checks the arithmetic)

Claim GC-T. For ANY convex K(Q), if (ii) holds (M >= M_line on the background densities of z in [3, 1100]), then the
dust is captured in every galaxy that turns around at z_c >= 1.259, whenever M_line > 2 pi / r_ta = 26.85 Mpc^-1.
Proof sketch. M = M(rho_K) (section 1). The background spans rho_K in [64, 1.33e9] x rho_K0 over z in [3, 1100]. A cold
sector follows the matter on galactic scales once k << a M, so at turnaround rho_ta = 5.55 (1 + z_c)^3 rho_K0, which is
>= 64 rho_K0 iff (1 + z_c)^3 >= 11.53. At z_c = 2, rho_ta = 149.9 rho_K0 = rho_K(z = 4.31), inside the window, so
M_ta >= M_line > 26.85 and the Jeans length is below r_ta. The virialised density is higher still (also inside the window).
QED for any K. Corollary: the present background mass mu_K(0) is not the mass the galaxy's dust feels; condition (iii) as
the brief states it cannot make galaxies clean. The forest line alone (a M(z) >= 2 pi h / 0.42 at z 2-4.6, QX3 G4') already
needs M >= 53 Mpc^-1 at rho_K(z = 4.31), above 26.85.

## 5. Labels

- Per column x member x footing: PASS / FAIL / NO VERDICT (a KA or MUTATE that the column relies on fails) / NOT EVALUABLE.
- A member PASSES if B1a, B1b, R2, C1, GL, GF, GFo, CT, S0, CS, GC and (iii) all pass (G1-G8 enter only if GC captures).
- **Lane label per footing:** PASS if at least one member passes; otherwise FAIL, naming the blocking columns per member and
  the size of each miss.
- **Brief kill** (reported beside the label): FIRES iff no member meets (i) + (ii) with mu_K(0) <= 79.4328, or M(z) runs the
  wrong way (smaller early).
- Reported row RB (not a member, not graded into the label): GL1's corrected-kernel iter3 member (beta 0.8, mu0 1259):
  its K ~ q^n with n = 1.3846, its q(z), the redshift where q reaches 1, M(1100), and its (i)/(ii) status.

## 6. Known answers (a KA FAIL means stop and fix; nothing is graded until all pass)

- KA1 (KD1 FRW): the general background machinery at lambda = 0, on KD1's own setting (QX15 omega_d and h per footing,
  kd1.json), gives mu_B1a and mu_B1b equal to kd1.json's to <= 1e-9 relative, both footings.
- KA2 (F1A cold fit): omega_d/omega_b from f1a.json best_B2 equals R_B2 (5.4096 / 5.4123) to 1e-9.
- KA3 (kernel): sympy, DBI on its background: K'(Qbar) - I0/a^3 = 0, K'' - 2 mu^2 r^3 = 0, the excess formula, and the
  lambda -> 0 limit of rho_K equals KD1/QX17B's I0 (1 + w0/a^3)/a^3 with w0 = I0/(4 mu^2) (all residual 0); M at lambda = 0
  equals mu Qbar (U1 kernel at Qbar = 1).
- KA4 (engine): `solve3` with constant kJ = mu and GL1's n = 4 kernel reproduces GL1's L2 rows_n4 at N3's corner for mu in
  {63.1, 100, 251.2, 631.0, 1000} to max(0.05, 1 %) in Delta chi^2; and with kJ = mu0 a^(3 beta) at (0.8, 1258.93)
  reproduces GL1 L3's n4 Delta chi^2 2.7798 to 0.05.
- KA5 (cold limit): kJ = 1e12 gives fsigma8 ratios and P1D ratios within 1e-3 of 1 and Delta chi^2 within 0.01 of 0.
- KA6 (static, only if G1-G8 run): KD1's kd1.py prefix loads and its KA1/KA2 (GB1 L0 class means; KD at I0 = 0 equals L0)
  pass as in kd1.json.

## 7. MUTATE twin (`--mutate`, separate outputs *_MUTATE.*)

- M-A (quadratic K, partner present): lambda = 0 at each member's mu, same I0. B1b must FAIL at every member (and B1a at
  mu <= 79.43). At mu = 79.4328 with KD1's setting, w(z 3400) and X must equal KD1's converse (0.059, 8.4e8) to 1e-6 rel.
- M-B (mu_K constant reproduces wall 1): constant kJ = mu at each member's mu on the GL engine: Delta chi^2 > 4 at every
  member mu <= 79.43 (D3 must sit near GL1/KD1's converse, 309-449 on N3's corner).
- M-C (GC has power): with constant M = 0.1 (no running), GC must PASS (not captured).
- If any of M-A, M-B, M-C does not bite, the column it tests is NO VERDICT.

## 8. Outputs

`kr1.py` -> kr1.json / kr1.out (background, BBN, R2, C1, GL, GF, GFo, S0, CS, GC, (iii), RB, KA1-KA5); `kr1_static.py`
-> kr1_static.json / .out (G1-G8 at M_ta, KA6) if GC captures; `--mutate` twins. RESULT.md: label per footing, the
column x member x footing table, the mu_K(z) table at z 0, 3, 10, 100, 1100, 3400, 1e5 per member and footing, the read
mu_K(0), the KR2 window reading, disclosures, and a plain-words paragraph. Any change after this freeze is disclosed in
RESULT.md as post-freeze.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
