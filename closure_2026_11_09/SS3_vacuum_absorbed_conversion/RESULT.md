# SS3 RESULT: FAIL / FAIL (criteria 3a8a5a9fce)

This lane grades variant J, the outside source's vacuum-absorbed conversion. TEST lane, quarantined; adopts nothing; no
particle adopted. kappa = 1/2 FITTED; not theory closed. Footings graded separately, never pooled.

**The construction.** G's onset and rate. The converted matter becomes w = -1 vacuum, and only inside collapsed halos. Two
helicity halves:
- the transverse half converts at Gamma0 everywhere;
- the longitudinal half at Gamma0 (v_stiff / sigma_1D)^2.

So f(r) = 0.5 e^-alpha + 0.5 exp(-alpha (v_stiff / sigma_1D(r))^2).

**Machinery.** SS1's machinery is used read-only: J's retention is injected inside SS3's own processes, and no SS1 / SS2
file was edited for this lane.

**Label (frozen order 1, 2, 3, 5, 5b, 6, N1, N3, 7b, 8, 9, 10): FAIL on canonical, FAIL on alt. First failing gate: 2,
groups.**
- Also failing: 6 BAO + SN, N1 rho_DE(z), N3 covariance, 8 growth, 9 Bullet, and 3 X-COP on canonical (alt passes).
- Passing: 1 KiDS, 5 SPARC, 5b Ursa Major, 10 Cassini.
- N2 is NOT EVALUABLE, as expected.

Count beside the label: 0 fitted constants. Form choices: the 50/50 helicity split, (v_stiff / sigma)^2, the 200 rho_crit
activation, and G's cube root / 4 pi.

## Gate table, primary (KD1 P3 SIS halos; canonical / alt)

| gate | canonical | alt |
|---|---|---|
| 1 KiDS | PASS max 0.006 (galaxies keep 0.6 %) | PASS |
| **2 groups** | **FAIL** 0/20, 2/20; median +0.31 / +0.11 (under-filled: groups keep 3-10 %) | **FAIL** 0/20, 2/20; +0.29 / +0.09 |
| 3 X-COP | FAIL mean +0.047, rms 0.102; bins -0.00, +0.11, +0.07; retained / M_dyn 0.58 / 0.35 / 0.27 (TR1 0.71 / 0.66 / 0.58) | PASS +0.034, rms 0.094; bins -0.01, +0.09, +0.05 |
| 5 SPARC | PASS rms 0.0559 | PASS |
| 5b Ursa Major | PASS (-0.000) | PASS |
| 6 BAO + SN (theta_s held) | FAIL Delta chi^2 +283; h 0.674 -> 0.778; Omega_DE0 0.915 (ref 0.685); D_M / r_d(0.51) 12.78 (ref 13.51) | FAIL +287 |
| N1 rho_DE(z) vs CFG689 nodes | FAIL: rho_DE rises 143 % from z_dec to 0; pulls +10.4, +5.0, -2.6, -0.4, -0.4, -0.1 (z 0, 0.4, 0.7, 1, 1.5, 2.33); chi^2 141 vs best constant 2.1 | FAIL: +145 %; chi^2 143 |
| N2 a0(z) | NOT EVALUABLE (AT2 cells BLOCKED; CFG689 a0 bands 0.3-0.6 dex). J's own drift +56 %; a0 today vs the footing +33 % (kappa fitted, so SPARC would absorb it) | same |
| N3 covariance | FAIL (below) | FAIL |
| 7(b) lensing | NO VERDICT; reading 13.77 | NO VERDICT; 13.83 |
| 8 forest + fsigma8 | FAIL: 76 % of the component converts; sigma8 0.791, S8 0.421 (Omega_m 0.08); Rf BGS 0.88, LRG1 1.02, LRG2 1.07, LRG3 1.05 (above CE2's 1.001 cap: the re-solved background changes growth before onset too) | FAIL |
| 9 Bullet | FAIL (cls FAIL; M300 Z -1.8, -3.5: retained 1.7 / 0.9 M_b) | FAIL |
| 10 Cassini | PASS | PASS |

## N3: why no perturbation-free vacuum can absorb a halo-local transfer

- **The coupled equations:** nabla_mu T^mu_nu(chi) = -Q_nu and nabla_mu T^mu_nu(vac) = +Q_nu, with T^mu_nu(vac) = -rho_vac
  delta^mu_nu. So Q_nu = -partial_nu rho_vac: Q must be a gradient.
- **The halo transfer is not a gradient.** For a static halo with Q_nu = Gamma(r) rho_chi(r) u_nu, the curl is
  partial_t Q_r - partial_r Q_t = d(Gamma rho_chi)/dr, which is non-zero (sympy, ss3_n3.py). Known answer: a uniform
  Gamma rho_chi gives 0, the homogeneous cosmological case.
- **What energy conservation then forces.** partial_t rho_vac = Gamma rho_chi, so the vacuum piles up where the halo
  converts, delta rho_vac = integral of Gamma rho_chi dt. The momentum equation is then left with the residual
  -t d(Gamma rho_chi)/dr, and nothing balances it. No static configuration exists: in linear GR a static source with
  delta p = -delta rho != 0 is inconsistent with Phi = Psi.
- **So "no perturbations, no shelf" holds only if local energy-momentum conservation fails.** If the energy stays local, the
  halo's lensing mass stays the pre-conversion one. That is the lane's full-retention reading (SS1 MG3), KiDS 0.378 / 0.376
  dex: a KiDS FAIL.

## Brackets

- **J-src** (the source's g_NFW) and **J-NFW** (Duffy): groups 0/2 in both. X-COP FAIL (+0.06 / +0.14).
- **M_min 2e11** (the source's "halos below 2e11 never reach 200 rho_crit"):
  - 40 % of the component converts;
  - rho_DE rises 60 %;
  - BAO + SN +76 / +78;
  - N1 chi^2 36 vs 2;
  - sigma8 0.799, S8 0.62;
  - every cosmological gate still FAILS.

## The source's claims, computed

| claim | source | lane (canonical) |
|---|---|---|
| converted share of the component | 18.5-28.4 % | 76 % (M_min 1e6) / 40 % (2e11) |
| rho_DE rise | +7.45 % | +143 % / +60 % |
| Omega_DE | 0.641 -> 0.689 | 0.685 -> 0.915 at the theta_s-held h |
| a0 | +3.66 % | +56 % / +26 % |
| D_M / r_d(0.51) | 13.56 | 12.78 / 13.16 (ref 13.51) |
| S8 | 0.766 | 0.421 / 0.621 |
| X-COP retained / M_dyn | 0.72 / 0.64 / 0.53 | 0.58 / 0.35 / 0.27 |
| groups | 25-48 % | 3-10 % |

The +7.45 % appears to count the converted matter at today's density. Energy conservation creates vacuum at the
density the matter had when it converted (z 0.1-0.6), which is (1+z)^3 larger.

## MUTATE and known answers

- **MJ1 (product -> radiation): BITES.** BAO + SN +10 (the A class); N1 flips to PASS.
- **MJ2 (v_stiff -> 0): BITES.** Groups 9/3, median +0.02; X-COP -0.025; KiDS 0.26.
- **KA-J1:** formula reproduced to 1e-12.
- **KA-J2:** law-only replay PASS.
- **KA-J3:** with no conversion, h returns 0.674078 / 0.673998.
- **KA-J4:** CFG689 nodes read from cfg689.json.
- **N3 KA:** the uniform case gives a zero curl.

## Reading

Turning the converted matter into vacuum removes SS1's radiation-BAO problem only if very little converts. On the record's
collapsed fraction, 40-76 % of the component converts at z < 0.63. That raises rho_DE by 60-145 % since z 0.63, against
CFG689's posterior, which prefers rho_DE flat or slightly falling. BAO + SN is off by 76-287 in chi^2. Locally, the
longitudinal escape law empties groups (3-10 % kept). It nearly works for X-COP (passes on alt), but then needs clusters to
keep more than groups by more than (v_stiff / sigma)^2 gives. Covariantly, a w = -1 recipient cannot absorb a halo-local
transfer at all (N3).

**What a repair would need:**
- the converted energy must go to something that may be inhomogeneous and carries momentum, which is not vacuum;
- its total must stay below about 2 % of rho_DE (N1);
- groups must keep 30-85 %.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Scripts: `ss3.py`, `ss3_cosmo.py`, `ss3_n3.py`, `ss3_grade.py`, `run_chain.sh`.
- Outputs: `ss3.json` / `ss3.out`, `ss3_MUTATE.json` / `.out`, `parts/`, the run logs `run_*.txt`.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
