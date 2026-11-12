# WD1 RESULT: FAIL / FAIL (criteria 0cd6ef1dcb)

Outside proposal: a supplementary component of cosmic amount 4.40 x baryons that clusters as cold dust before shell-crossing
and afterwards sits in a 1.6 Mpc Thomas-Fermi core around every collisionless baryonic centroid, the core lowered in groups and
clusters by a merger-driven decoherence scalar, satellites keeping (v_esc/sigma_host)^3 of their share. Graded AS WRITTEN under
the record's gates as a quarantined TEST lane (owner decision ../OWNER_DECISION_2026-11-08_WD1_LAUNCH.md). Adopts nothing; the
owner adopts. No dark-matter particle is adopted: a declared component is graded as PJ1 and BG1 were. kappa = 1/2 FITTED; not
theory closed. Footings canonical (a0 9.3603e-11 m/s^2) and alt (a0 1.1312e-10), the record's kappa = 1/2 values, graded
separately, never pooled.

Label rule (frozen): PASS iff the as-written declared inputs pass G1-G10; FAIL iff they do not; NO VERDICT only for a NOT
EVALUABLE gate. **As written, 4 of 11 gates pass on each footing (G1, G1b, G8, G10); G2, G3, G4, G5, G6, G7 and G9 fail on
both. No gate is NOT EVALUABLE. Label FAIL on canonical, FAIL on alt.** The derived bracket (the proposal's own dynamic integrator,
one event, d_sep0 = R500 for groups and clusters, 40 kpc for ellipticals, 3:2) passes no gate the as-written fails.

## What was built (wd1.py, wd1_bullet.py, wd1_cmb.py, wd1_web.py, wd1_grade.py; run_chain.sh runs them in order)
- Own implementation of the component in its quasistatic form: W_lag(r) = 16 mu^2 (d^2/(r^2 + d^2))^2, s(r) = gamma N W_lag^2 /
  (W_lag + W_crit), R_c(r) = R_c0 e^(-s/2), M(<r) = f M_b r^3/(r^2 + R_c(r)^2)^(3/2), evaluated LITERALLY with R_c at the
  radius asked (the proposal's own code does the same), declared constants f 4.40, R_c0 1.60 Mpc, W_crit 0.020, gamma 2.0,
  mu 0.25, per-class inputs spirals N 0, ellipticals N 1 d 35 kpc, groups N 4 d 400 kpc (N 4.5 d 420 reported), clusters N 6 d
  600 kpc, Bullet main / sub N 6 / 5, d 600 / 500 kpc; capture min[1, (v_esc/sigma_host)^3] with v_esc the central escape speed
  of the satellite's own stars (Plummer, S1's shape) and sigma_host 1000 km/s for Coma. Adopted law on the total Newtonian
  source; the proposal's own nu(y) = 1/(1 - e^(-sqrt y)) run as a reported bracket.
- Own rebuild of the dynamic integrator from its equations (tidal tensor of Plummer-softened progenitors, Israel-Stewart
  relaxation of the tracked tensor with tau = the local dynamical time, ds/dt = gamma |E| W^2/(W + W_crit) with W = |E - Sigma|^2 /
  (|E|^2 + Lambda_IR), decaying circular inspiral, tracers on tilted rings, RK4). The tidal tensor was checked against a
  finite-difference Hessian of the Plummer potential (max relative deviation 3.6e-8).
- Local gates through the record's loaders read-only (QX8 SPARC exact-field parts, GB1 / QX5 battery, UD1 / UD2, S1, X1 / LW1);
  G6 through DB1 / UX6's Bullet child; G7 through F1A's machinery with PJ1's Planck-2500 CamSpec reader; G8 / G9 through the
  QX3 iter2 growth ODE, GL1's corrected lensing kernel and NC2 G3's forest machinery as PJ1 carries them (own transcription).

## Known answers

| KA | what | result |
|---|---|---|
| KA1 | r 500 kpc, M_b 1.2e11, N 0: component 0.117 M_b, +0.025 dex with the proposal's nu | **PASS** 0.1168 M_b; +0.0243 dex (nu), +0.0243 dex (adopted law), both footings and at a0 1.2e-10 |
| KA2 | group proxy r 200 kpc, M_b 1.5e12, N 4.5, d 420: R_c <= 150 kpc, component >= 3.0 M_b | **PASS** s 5.81, R_c 87.8 kpc, 3.38 M_b |
| KA3 | rebuilt integrator: case A s(300 kpc) in [0.005, 0.02]; case B s(200 kpc) in [4.5, 6.5] | **FAIL** case A s(300) 1e-15 (s(50) 2e-3, s(100) 5e-6); case B s(200) 0.095 (s(50) 0.83, s(100) 0.48, s(300) 0.024). By the frozen rule the quasistatic form is graded alone; the dynamic bracket is reported only and no bracket PASS is credited (none occurs) |
| KA4 | f -> 0 replays the record's law-only numbers to 1e-6 | **PASS** both footings: SPARC rms 0.056046 / 0.055826 (QX8), KiDS shift 0, X-COP +0.467500/0.476307 and +0.434524/0.444158 (GB1 L0), groups 0/0 (GB1), UDGs +1.120753 / +1.077576 (GB1) |
| KA5 | F1A's constant-weight CMB chi^2 at the record's own amount | **PASS** F1A PA chi^2 at the B2 best fit +1.98 / +1.96 (within 3); Planck-2500 chi^2 at w 1 equals PJ1's direct CAMB value to 1e-12 (1072.229 / 1071.511) |
| web | R = 1 identities (fs8 ratios 1, lensing and forest Delta chi^2 0); baseline lensing chi^2 8.5599 / 8.5604 = PJ1's | **PASS** |
| Bullet | law alone reproduces DB1 K1 (M300 1.112e14 / 7.337e13, dkappa -0.068 / -0.111) | **PASS** |

## Gate table, AS WRITTEN (bracket = dynamic integrator one event, d_sep0 R500 / 40 kpc, 3:2; nu = the proposal's own interpolation; both reported, never graded)

| gate | canonical | alt | bracket (can / alt) | proposal nu (can / alt) |
|---|---|---|---|---|
| G1 SPARC (rms <= law + 0.010, \|mean\| <= 0.05) | **PASS** 0.0560 (line 0.0660), mean +0.0008; component 1.5e-6 M_b at the last point (max 1.4e-3) | **PASS** 0.0558 (line 0.0658), -0.0023 | same (N 0) | PASS 0.0552 / 0.0553 |
| G1b massive tail v_flat >= 250 (10 galaxies) | **PASS** 0.0375 (line 0.0475) | **PASS** 0.0326 (line 0.0426) | same | PASS |
| G1c AGC 114905 / Malin 1 chi^2 (informational) | 843.6 -> 843.6; 69.0 -> 69.1 | 995.8 -> 995.8; 132.5 -> 132.6 | same | - |
| G2 KiDS 59 points, every bin \|shift\| <= 0.05 | **FAIL** max 0.297 at 1.7 Mpc; 15 of 59 over; mean shift by radius < 0.1 Mpc 0.000, 0.1-0.3 +0.002, 0.3-1.0 +0.040, >= 1 Mpc +0.213; ETG inputs (N 1 d 35) identical | **FAIL** 0.296 | FAIL 0.297 / 0.296 | FAIL 0.297 / 0.296 |
| G3 X-COP amount (\|mean\| <= 0.05, rms <= 0.10) + NA2 per-bin shape (each bin within 0.10) | **FAIL** -0.614 / 0.789; bins r/R500 0-0.25 -1.132 (n 14), 0.25-0.5 -0.595 (7), 0.5-0.75 -0.105 (14); concentration M(<0.25)/M(<0.7 R500) component 3.34 vs gas 0.20, need 0.27; 4.38 M_b inside 100 kpc, 3.36 inside 500 kpc; R_c 7 kpc at 0.1 R500, 353 kpc at 0.5 R500 | **FAIL** -0.627 / 0.793; bins -1.136, -0.605, -0.131 | FAIL, under-filled: +0.334/0.363 (bins +0.455 +0.378 +0.192) / +0.304/0.335 | FAIL -0.602/0.779 / -0.615/0.783 |
| G3 monotone reading (negative shells floored) | FAIL -0.726 / 0.824 | FAIL -0.737 / 0.831 | - | - |
| G4 groups >= 16/20 at f* 0 and f* 1 | **FAIL** 3 / 4 (N 4 d 400); 2 / 2 at the code's N 4.5 d 420; 9-14 M_b at R2500, 0.4-0.6 at R500 | **FAIL** 4 / 3; 1 / 0 | FAIL 0 / 1 both | FAIL 3 / 4, 4 / 4 |
| G5 Coma UDGs within 2 sigma_U (0.262) | **FAIL** +1.240 (+4.73 sigma_U); capture median 4.9e-6 (max 1.4e-5), b 1.0000; without Coma's component in the external field +1.121 (the law-only value); Coma's component 1.24 M_b inside 1 Mpc raises the host field x1.72 | **FAIL** +1.202 (+4.59); +1.078 without; x1.67 | FAIL +1.215 / +1.175 | FAIL +1.244 / +1.206 |
| G5b MW classical (8) / bright M31 (25) dSphs, reported | law residual median +0.245 / +0.227; component shift <= 3e-13 (capture <= 1.8e-3 at sigma_host 180) | +0.206 / +0.187; <= 3e-13 | - | - |
| G6 Bullet, reading (b) gas-traced Mach-6 fluid (the label rests on it) | **FAIL** cls FAIL; dkappa -0.230, -0.449; peak 51 / 41 kpc from the gas, 260 / 199 kpc from the galaxies; M300 3.46, 2.14 e14 (Z -0.07, -0.47) | **FAIL** dkappa -0.242, -0.462; M300 3.64, 2.26 e14 (Z +0.26, -0.10) | - | - |
| G6 reading (a) asserted centering on the galaxies | PASS, cls TENSION; dkappa +0.244, +0.030; peak 41 / 63 kpc from the galaxies; M300 4.52, 2.07 e14 (Z +1.94, -0.67) | FAIL, cls TENSION; M300 4.73 e14 (Z +2.33) | - | - |
| G7 primary CMB, 4.40 omega_b clustered on the footing background, Delta chi^2 <= 10 | **FAIL** +3682.7 before the refit; +1524.8 after the 5-parameter refit (100 evaluations; ob driven to its 0.023 bound, ns to 1.04); +15,970 on the proposal's own background (od = 4.40 ob, four parameters) | **FAIL** +3699.6; +1490.1; +12,013 | - | - |
| G8 growth (by construction before shell-crossing) + PR4 lensing with the 1.6 Mpc physical cores | **PASS** fsigma8 ratios 1 (stated); lensing Delta chi^2 -0.00 with the one-halo suppression (S_1h at z 0: 0.95 at k 0.1, 0.73 at 0.3, 0.23 at 1, 0.04 at 3 Mpc^-1; the kernel's weight S_L 1.003 at L 100, 0.991 at L 400; nonlinear-baseline reading -0.18) | **PASS** same | - | - |
| G8 footing-background reading (only 4.40 of 5.41 omega_b clusters), reported | fs8 FAIL, Rf 0.37-0.38; lensing +2.30 | same | - | - |
| G9 forest (NC2 band, Delta chi^2 <= 4) | **FAIL** 216,405; P1D ratio 0.006-0.19, 0.02-0.03 at every z 2.2-4.4; matter ratio at z 3: 0.82 at k 0.1, 0.45 at 0.3, 0.15 at 1 Mpc^-1; the sharper k^4 filter 219,383 | **FAIL** 216,406; 219,384 | - | - |
| G10 Cassini + c_T = 1 | **PASS** 3.55e4 Msun inside 8.2 kpc (= 4.4 M_b (8.2/1600)^3), rho 1.5e-8 Msun/pc^3, Cassini use 2.8e-8, worst planet 0.21; N 1 d 35 bracket PASS (5.0e5 Msun); c_T = 1 stated | **PASS** 2.0e-8, 0.19 | PASS | PASS |
| gates passed | 4 of 11 | 4 of 11 | - | - |

## Hand estimates (frozen) and expected kills (owner decision), as they fired

| estimate | canonical | alt | |
|---|---|---|---|
| outer KiDS bins fail by 0.2-0.4 dex | 0.297 at 1.7 Mpc; +0.21 mean beyond 1 Mpc | 0.296 | **HIT** |
| X-COP inner bin < -0.2 dex | -1.132 | -1.136 | **HIT** |
| Coma UDGs stay ~+1.1 dex | +1.240 | +1.202 | **HIT** |
| forest FAIL | 216,405 | 216,406 | **HIT** |

Expected kills: KiDS outer bins FIRES; Coma UDGs FIRES; X-COP per-bin shape FIRES; forest FIRES; Bullet (b) FIRES; primary CMB
at 4.40 FIRES. All six on both footings.

## MUTATE (wd1_MUTATE.json / .out; criteria hash in every output: True)
- M1 R_c0 -> 50 kpc (no puffing): G1 FAIL 0.091 / 0.098 (line 0.066; component 0.047 M_b at the last point), G2 FAIL 0.370 /
  0.369 (57 of 59 over) -> **BITES** both footings.
- M2 W_crit -> infinity (no decoherence): X-COP swings from over-filled -0.614 to under-filled +0.354 (0.117 M_b inside 500 kpc)
  / -0.627 to +0.323; groups 0/0 and 0/1 -> **BITES** (G3 and G4 FAIL, the cluster core stays at 1.6 Mpc).
- M3 f -> 0: G1, G2, G10 PASS at the record's law-only numbers; G3 +0.4675 / +0.4345, G4 0/0, G5 +1.121 / +1.078 FAIL (the
  record's law-only FAILs), every number to 1e-6 of QX8 / GB1 L0 -> **BITES** (KA4 replay).

## Disclosures
1. KA3: the integrator rebuilt from the proposal's equations and stated discretisation gives s(300 kpc) 1e-15 for its case A
   (claimed 0.005-0.02) and s(200 kpc) 0.095 for its case B (claimed 4.5-6.5); the tidal tensor matches a finite-difference
   Hessian to 3.6e-8. The proposal's own module was not executed (reference only). The quasistatic form is graded alone; the
   dynamic bracket (one event, 3:2, d_sep0 R500 / 40 kpc, orbital speed = the adopted law's circular speed on the baryons at
   d_sep0, duration one orbit, 600 RK4 steps, 12 tracers per ring) is reported beside every local gate. It decoheres only the
   inner ~0.1 d_sep0 (s 0.1-0.8 inside 100 kpc for a 2e13 group, 0 beyond 300 kpc), so clusters keep the 1.6 Mpc core and
   X-COP flips to under-filled (+0.33 / +0.30) while the groups fall to 0/1.
2. Literal enclosed mass: with R_c(r) evaluated at the radius asked, the as-written M(<r) FALLS outward wherever R_c grows
   faster than r (clusters between ~0.2 and 0.6 R500), i.e. negative shell densities. The literal form is the primary (it is
   what the proposal's code evaluates); the monotone reading (negative shells floored) is reported and fails the same gates
   (X-COP -0.726 / -0.737, groups 6/0 and 1/0).
3. G5: the record's Coma residuals (S1's static solve with the hydrostatic beta-model host field) are the base; the UDG's own
   component enters as a multiplier on its internal source (b = 1.000000 at capture 5e-6), and Coma's own component enters the
   external field through a one-dimensional map on the law's nu with the law-implied Newtonian source of the record's host
   field (Coma's baryons 3.2e14 / 2.8e14 Msun inside the law-implied R500 1066 / 1020 kpc; declared approximation, S1's exact
   solve not re-run). Without the host term the gate reads the law-only value (+1.121 / +1.078); with it +1.240 / +1.202. Both
   fail; the direction is the one the hand estimate named.
4. G2: the component is depth-free, so "stacked with the lenses' own depths" adds nothing; each lens bin carries its stellar
   mass as the record's loader gives it (QX5 lensing(), 59 points, 25 beyond 0.3 Mpc). The ETG inputs (N 1, d 35 kpc) and the
   40 kpc dynamic bracket leave s = 0 beyond 100 kpc, so the ETG bracket equals the N 0 primary.
5. G3: the amount is f x the cluster's baryons inside the outermost radius where gas and stars are both measured (GB1's
   Mb_last), no fitted amplitude. The inner bin's -1.13 dex is the 7 kpc core at 0.1 R500 putting 4.4 M_b inside 100 kpc.
6. G6: DB1 places the component on the galaxies' (a) or the gas's (b) own field shape, not on the Thomas-Fermi profile; the
   as-written cores at 300 kpc are 39 kpc (main, 4.29 M_b inside) and 118 kpc (sub, 3.55 M_b), so the component is as compact
   as the stars and the placement test is the centering test the gate asks. Reading (a) passes the offset test on canonical
   only (cls TENSION, M300 Z +1.94 / +2.33) and is the asserted rule, not the fluid's own behaviour; the label rests on (b).
7. G7: the F1A background has omega_d = 5.41 omega_b; 4.40 omega_b clusters and the remaining 1.01 omega_b is carried as a
   smooth c_s^2 = 1 fluid (PJ1's construction; the lensing potential here is the consistent fluid cosmology's, where PJ1's
   constant-weight variant lensed with the w = 1 potential and read +3667 / +3684). The 5-parameter refit (100 Nelder-Mead
   evaluations, one CAMB run each, clustered amount held at 4.40 ob) is not converged (ob at its upper bound) but sits 150 x
   the line; the proposal's own background (od = 4.40 ob exactly) is worse by an order of magnitude.
8. G8: the record's lensing kernel (GL1 / BG1 limber4) integrates linear power, so the halo-model one-halo suppression enters
   as the ratio P_supp / P_halofit of nonlinear powers (P_supp = P_lin + (P_halofit - P_lin)_+ x [(f u + 1)/(1 + f)]^2 with u =
   x K_1(x) the Plummer-core profile at x = k R_c0/a); on the PR4 kernel (L < 400) the one-halo term is small and the gate
   passes. The frozen statement that growth passes by construction is taken; the footing-background reading (only 4.40 of 5.41
   omega_b clustering) would fail fsigma8 (ratios 0.37) and is reported, not graded.
9. G9: the Jeans-type suppression is entered as the component's clustering fraction T_J = 1/(1 + (k/k_J)^2), k_J = pi a/R_c0
   (1.6 Mpc physical from z 20 on), through BG1's non-clustering fraction in the growth ODE; the k^4 form is reported. Both erase
   97-98 % of the P1D at every forest redshift.
10. The shared checkout is behind origin and lacks PJ1 on disk; PJ1's lane directory was taken from origin/main into a
    read-only scratch copy (env WD1_PJ1_DIR, default the repo's own path) with the repo's data folders linked beside it. The
    record's untracked data folders (X-COP, SPARC, Planck, DESI P1D, PR4) are the shared checkout's own.
11. Compute: local 17 s at 0.12 GB; mutants 17-18 s each; Bullet 16 s with DB1's child at 1.46 GB (the record's machinery, as
    PJ1 ran it at 1.39 GB; disclosed); CMB 335 / 330 s at 0.69 GB per footing; web 32 s at 0.46 GB. One child at a time, nice
    10, df checked before each (compute was held once while the volume sat at 1.6 GiB free; resumed at 9.4 GiB).

## Reading
The proposal does what it says only where the record already passes: with N 0 the 1.6 Mpc core holds 1.5e-6 of a disc's
baryons inside its last point (G1, G1b, G10 untouched) and 0.1 M_b inside 500 kpc of a lens, but 0.6 M_b at 1 Mpc and 1.7 M_b at
1.7 Mpc, so the outermost KiDS bins rise by 0.2-0.3 dex (G2). The merger key then over-corrects the hot systems: at the declared
cluster inputs the core is 7 kpc at 0.1 R500 and 4.4 M_b sits inside 100 kpc (X-COP inner bin -1.13 dex, the stars-traced shape
NA2 already failed made more concentrated still), while the literal profile loses mass outward between 0.2 and 0.6 R500; the
groups get 9-14 M_b at R2500 and 0.5 M_b at R500 (3-4 of 20). The capture rule hands the Coma UDGs nothing (5e-6) and Coma's
own component deepens their external field, so the UDG shortfall grows from +1.12 to +1.24 dex. Its own equation of state makes
the component a Mach-6 fluid in the Bullet encounter, where it follows the gas (G6 b). On the CMB a clustered 4.40 omega_b on
the footing background misses by Delta chi^2 3,700 (1,500 after refitting), and the forest cannot carry a 1.6 Mpc physical
Jeans scale (P1D down by 97 %). Seven gates fail on both footings; the dynamic integrator, rebuilt from its equations, does not
reproduce the proposal's own decoherence values and would leave the cluster cores at 1.6 Mpc. The record's statement stands: no
mechanism in the record passes every gate; this one adds a merger-history key to the list.
