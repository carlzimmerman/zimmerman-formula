# TS1 RESULT (criteria 4b352f2a37): every sub-variant FAILS on both footings

TS1 grades a tidal-signature switch on the law, nu_eff = 1 + (nu - 1) max(0, I/2), with
I = -det H / (Tr H^2 / 6)^(3/2) on Phi_N of all matter. TEST lane, quarantined. Adopts nothing. kappa = 1/2 FITTED; not theory
closed. Footings never pooled.

| sub-variant | canonical | alt | first failing gate |
|---|---|---|---|
| **M-W** (switch + WM1's 188.7 eV relic) | FAIL | FAIL | **0 seeding**; also T1, 1, T3, 2, 3, T4, 8, CS |
| **M-split** (50 % 188.7 eV + 50 % 18.87 eV) | FAIL | FAIL | **0 seeding**; also T1, T3, 2, 3, T4, 7a, 7b-N, 7b-L, 8 |
| **M-law** (switch, no component) | FAIL | FAIL | **T1 SPARC in the disc**; also T3, 2, 3, T4, 7a |

- Known answers all pass: KA-T, KA-T6 (exact replay of law-only), KA-T7 (ensemble). The criteria (section 2) record I = -2 sqrt 2
  for an isotropic overdensity; the orchestrator's stated -2/sqrt 3 does not follow from the definition.
- MUTATE: MT1 (s = 0) bites T1. MT2 (h_z x 3) and MT3 (D 7 Mpc) move their statistics as required.

## The first expected kill: T1, SPARC inside the disc

Mid-plane Hessian (Phi_RR, g_N/R, 4 pi G rho_0 - Phi_RR - g_N/R), with rho_0 from the stellar disc only. Bulge and gas are left
out, which is generous to the switch.

| | canonical | alt |
|---|---|---|
| s at the measured points, median at Upsilon 0.5 | 0.28 (p10 0.00, p90 1.08); 61 % of points below 0.5 | same |
| M-W rms | 0.121 (line 0.066) | 0.123 (line 0.066) |
| M-split rms | 0.121 | 0.123 |
| M-law rms | 0.122 | 0.124 |
| above the disc (2 h_z) | 0.099 | 0.101 |
| h_z x 3 | 0.095 | 0.099 |
| s = 0 (Newton) | 0.245 | 0.245 |

- In the disc 4 pi G rho_0 dominates the Hessian, so I is near 0 and the switch removes most of the law's boost exactly where
  rotation curves are measured.
- Every reading fails by about 2x the line.

## Local gates (canonical; alt the same within 0.03)

- **Spherical systems.** I depends only on x = rho / rho_bar(<r): s = 1 in vacuum, sqrt 2 at x = 1/3 (isothermal), 0 for x > 2/3.
  - Cluster and group outskirts sit near s = 1.41, so the law is boosted, not switched off.
- **M-W:**
  - X-COP -0.25, bins -0.32 / -0.19 / -0.21 at s 1.41. Retained / M_dyn 1.51 / 0.87 / 0.71 vs TR1 0.71 / 0.66 / 0.58.
  - Groups 1/0.
  - KiDS single lens 0.074: s = sqrt 2 inside the SIS primary halo.
- **M-split:**
  - X-COP -0.085, bins -0.13 / -0.02 / -0.07. Retained 0.79 / 0.46 / 0.37; the source claimed 0.755 / 0.62 / 0.54.
  - Groups 7/1 (alt 5/0); the source claimed 18-19 of 20.
  - KiDS single lens 0.040 PASS.
- **M-law:** X-COP +0.51 and groups 0/0, as law alone. The cores switch partly off (s 0.73 inner).
- **T3, KiDS to the saddle** (an equal neighbour at 3.5 Mpc): the direction-averaged s falls to 0.76 at r/D 0.6-0.8. KiDS max
  0.086 / 0.099 / 0.118 (M-W / M-split / M-law): FAIL in all three.
- **T4, WL1's population phantom.** Outside every isolated host's matter, I = 2 exactly, so s = 1. The switch leaves WL1's
  retained phantom untouched except inside the baryon body.
  - Bound: q_pop >= 0.905 / 1.045 (canonical / alt) against the 0.0354 line: FAIL x26 / x30.
  - The source's "cosmic mean phantom vanishes" is false: the switch is fully on around every halo.

## The linear web (T6) and voids (T2)

- **Gaussian Hessian ensemble (2e6 samples):** the switch is on in 50.1 % of space. <s> is 0.25 by volume and **0.23 weighted by
  delta^2** (the graded linear-response coefficient). Overdense regions have <s> 0.40, underdense 0.11.
- **The web is not Newtonian by construction.** It keeps 23 % of the law's boost.
- **M-W with nu_eff_web:**
  - B_m at z 0.02 is 1.47 / 1.34 / 1.34 / 1.43 / 1.68 / 2.16 at k 0.01 / 0.03 / 0.1 / 0.3 / 1 / 3 h/Mpc (it was 3-18 in WM1).
  - **7b-L passes** (14.0 / 15.3, line 18.48).
  - fsigma8 ratio 1.57-1.45 (alt 1.65-1.51): FAIL. S8 +37 % / +42 %: FAIL. Forest 1.5e5: FAIL.
  - The forest fails anyway, because the 188.7 eV relic alone fails it (1.67e5).
- **M-split:**
  - S8 passes (-1.5 % / +1.9 %), because the hot half cancels the boost.
  - fsigma8 ratio 1.13-1.04: FAIL.
  - 7b-L: 35.1 / 37.9, FAIL.
  - 7b-N (HC1 G9, two species): worst corner 22.15, FAIL (T5's expected kill holds).
  - 7a: +82.0 / +82.9 from ACT (TT at L 3000 is 0.95 of cold): FAIL.
  - BAO+SN: +3.26, PASS.
- **Voids (T2):** at an isotropic void centre s = sqrt 2, so the switch amplifies the law there. The record has no void line.

## Gate 0, seeding (WM1 A2 machinery with nu_eff_web)

n(> M) / cold reference, sharp-k. Line 0.5.

| sub-variant, footing | 1e10, z 2 | 1e10, z 0 | 1e11, z 2 | 1e11, z 0 |
|---|---|---|---|---|
| M-W canonical | 0.006 | 0.012 | 0.054 | 0.084 |
| M-split canonical | 1.3e-4 | 0.011 | 9e-4 | 0.060 |

- Alt is the same within 10 %.
- The switch lowers the law's boost, so it cannot help seeding: WM1's Newton reading already failed.

## T7, covariance

- I is a non-polynomial function (e3 / (e1^2 - 2 e2)^(3/2)) of the second-derivative invariants of Phi_N, cut by a non-smooth
  max(0, .).
- Galileon, Horndeski and DHOST theories admit only specific polynomial, antisymmetrised (or degenerate) combinations of second
  derivatives. A general function of e2 and e3 gives fourth-order equations for Phi_N, i.e. an Ostrogradsky ghost unless a
  degeneracy condition holds, and this one does not.
- Non-relativistically, ∇^2 Phi = ∇.(nu_eff ∇Phi_N) is still a well-posed prescription, because Phi_N is solved first.
- **Recorded as a phenomenological switch.** No known healthy covariant action carries it. Changing that would need I replaced by
  a combination of the allowed Galileon / DHOST structures that keeps I's signature properties, and none is known.

## Reading

- **The switch fails where it acts.**
  - Inside discs, where rotation curves are measured, the matter density sets I near 0 and removes the law's boost: SPARC rms
    doubles.
  - Around isolated halos it is exactly on (I = 2), so the phantom WL1 found remains.
  - On the linear web it keeps about 23 % of the boost.
- **It does help two numbers.** M-W's law-on lensing (108 -> 14, now passing) and S8 (x 3.6 -> x 1.37).
- **But not enough.** fsigma8 and S8 still fail for M-W. The hot half of M-split fixes S8 but fails CMB lensing and the CMB
  primary. Seeding fails in every component variant.

**A repair would need:**
1. a switch that is ON inside baryonic discs (I there is near 0);
2. OFF around isolated halos (I there is exactly 2), which contradicts the signature I uses;
3. zero on the linear web (<s>_w 0.23);
4. plus WM1's seeding and cluster requirements.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Scripts:
  - `ts1_core.py`: KA-T, ensemble, T3 table.
  - `ts1_local.py`: T1, 1, T3, 2, 3, MUTATE.
  - `ts1_cosmo.py`: WM1's cosmo / seed / hc1 / cmb, exec'd read-only with in-process patches.
  - `ts1_grade.py`.
  - `run_chain.sh`.
- Outputs:
  - `ts1.json` / `ts1.out`, `ts1_MUTATE.json` / `ts1_MUTATE.out`.
  - `parts/` (core, local, cosmo_*, seed_*, g9_MSPLIT, cmb7a_MSPLIT_*).
  - Logs `run_*.txt`.
- Carried, not recomputed:
  - M-W 7a and 7b-N from WM1.
  - M-law 7a from QX15's MB control.
  - Cassini: s = 1 outside the Sun.
- NOT RUN: Bullet, UMa, Coma UDGs (reasons in the criteria), and M-law's cosmology beyond 7a.
- Compute: one thread; local 2 s, 0.2 GB; cosmology 0.5 GB with CLASS; 7a 1.6 GB with CLASS (disclosed).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
