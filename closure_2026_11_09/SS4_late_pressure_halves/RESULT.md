# SS4 RESULT: FAIL / FAIL (criteria f3effad98c)

This lane grades variant K, the outside source's late pressure halves, plus a stand-alone option (c) table. TEST lane,
quarantined; adopts nothing; no particle adopted. kappa = 1/2 FITTED; not theory closed. Footings never pooled. SS1's machinery
is used read-only (monkeypatched inside SS4's own processes).

**Label (frozen order 1, 2, 3, 5, 5b, 6, 7b, 8, CS, 9, 10): FAIL on canonical, FAIL on alt. First failing gate: 1, KiDS.**
- Also failing: 2 groups, 3 X-COP, 9 Bullet.
- Passing: 5 SPARC, 5b Ursa Major, 6 background (no conversion), 8 forest + fsigma8, CS cosmic shear (on the frozen S8 line),
  10 Cassini.
- 7(b) is NO VERDICT, with the reading 8.56.
- Every bracket (K-p2, K-formula) also FAILS at KiDS.
- Count beside the label: 0 fitted constants. Form choices: the 50/50 split, the 4/3 polytrope, R_c1 = 2.60 Mpc, the cube
  power, c_s2's form. The source's R_c1 formula, v_stiff / (4 pi H0), gives 0.314 / 0.340 Mpc, not 2.60.

## Option (c), stand-alone: the largest fraction f_gal of an isolated lens's cosmic share (5.41 M_b) in rho0 / (1 + (r/R_c)^2)^2

| R_c (Mpc) | 0.12 | 0.3 | 0.6 | 1.2 | 2.4 | 3.0 |
|---|---|---|---|---|---|---|
| record's KiDS line (59 points, pointwise) | **0.050** | **0.055** | **0.065** | **0.093** | **0.200** | **0.292** |
| 0.3-1.5 Mpc subset only (reported) | 0.054 | 0.067 | 0.100 | 0.237 | 1.00 | 1.00 |
| the source (Delta Sigma, 0.3-1.5 Mpc) | 0.18 | 0.23 | 0.30 | 0.44 | 1.00 | 1.00 |

Same on both footings. SPARC (the F2 allowance) never binds for R_c >= 0.12 Mpc.
- On the record's line, the binding points are the outer KiDS points beyond 1.5 Mpc (pointwise). An isolated lens can hold
  at most 5-20 % of its share in a core of 0.1-2.4 Mpc.
- The source's numbers are 3-4x larger at small R_c and look at 0.3-1.5 Mpc only.

## K, primary (KD1 P3 halos; canonical / alt)

| gate | canonical | alt |
|---|---|---|
| **1 KiDS** | **FAIL** max 0.219 (11/59 over); at 0.3 / 1 / 1.5 Mpc: 10.45 +0.001 / +0.029 / +0.090; 10.7 +0.003 / +0.056 / +0.128; 10.9 +0.007 / +0.079 / +0.151 (claimed +0.015..+0.029) | **FAIL** 0.204 |
| 2 groups | FAIL 10/20, 1/20; median +0.02 / -0.18 | FAIL 11/20, 0/20 |
| 3 X-COP | FAIL mean -0.454, rms 0.569; bins -0.81, -0.35, -0.15; retained / M_dyn 6.59 / 1.60 / 0.69 (claimed 0.70 / 0.65 / 0.56; TR1 0.71 / 0.66 / 0.58) | FAIL -0.467 |
| 5 SPARC | PASS | PASS |
| 5b Ursa Major | PASS | PASS |
| 6 background | PASS (no conversion) | PASS |
| 7(b) lensing | NO VERDICT; reading 8.56 (baseline 8.56) | NO VERDICT |
| 8 forest + fsigma8 | PASS (Rf BGS 0.946, LRG1 0.980) | PASS |
| CS cosmic shear | PASS: S8 0.816 vs ref 0.828 (-1.5 %, line +-5.9 %); sigma8 ratio 0.985. **But** P_K / P_ref at z 0.3 is 0.98 / 0.84 / 0.18 at k 0.3 / 1 / 3 h/Mpc (0.78 at k 3, z 0.5) | PASS (-1.7 %); P 0.98 / 0.81 / 0.14 |
| 9 Bullet (both halves pressured, gas-traced) | FAIL (cls FAIL; M300 Z -2.15, -2.33); galaxy-traced also FAIL | FAIL |
| 10 Cassini | PASS | PASS |

**Why.**
- **Galaxies:** half 2's core R_c2 = R500 (v_stiff / v_vir)^3 grows to 0.7-0.9 Mpc in galaxy halos. That puts 50 % of the share
  into exactly the cores option (c) allows only 6-9 % in, so KiDS fails at 1-1.5 Mpc.
- **Clusters:** the same rule shrinks R_c2 to 7-44 kpc. Half 2 collapses into a 10-40 kpc core: the X-COP inner bin is
  over-filled by a factor of 6.6 and the shape is far more concentrated than TR1's.
- **Groups:** they sit between and split.
- **Half 1:** at a fixed 2.6 Mpc it is invisible locally (about 6 % inside 1.5 Mpc).

## The five items the orchestrator named

1. **Cosmic shear and small-scale power.** Not a kill on the frozen S8 line. The record's three-fluid Jeans ODE gives
   sigma8 -1.5 %, because the pressured halves stop growing only gradually after z 0.63. But the matter power is down 16-19 %
   at k 1 h/Mpc and 82-86 % at k 3 h/Mpc by z 0.3. A shear statistic weighted to k >= 1 h/Mpc (the KiDS / DES non-linear
   regime) would see it. The record has no shear-C_ell machinery, so this is reported, not graded.
2. **KiDS from half 2 in galaxies:** the first failure, matching option (c) (above).
3. **The condensate rung.** WD1 (a fixed 1.6 Mpc Thomas-Fermi core) failed KiDS at 0.30 dex at 1.7 Mpc and the X-COP inner bin
   at -1.13. QX27-31 (superfluid / tail / dipolar sectors) failed on the hosts. K's new element is the mass-dependent core
   R_c2 proportional to v_vir^-3, steep enough to puff galaxies and collapse clusters. It does not change the outcome:
   - KiDS FAILS (0.22, not WD1's 0.30);
   - the X-COP inner bin FAILS the same way (-0.81 vs WD1's -1.13);
   - the steepness makes clusters worse (cores of 10-40 kpc).
4. **Dynamics: are the cores reachable?** Half 1's frozen core implies c_s1 = R_c1 H sqrt(1.5 Omega_m) / pi = 38 km/s.
   - Half 1: reaching 2.6 Mpc from a collapsed halo at 38 km/s takes 32-65 Gyr against the 6.1 Gyr available. The frozen
     equilibrium for half 1 is unreachable. Half 1 would stay in its pre-conversion halo, which makes KiDS worse, towards
     the MK1 0.36 at half amount.
   - Half 2 in galaxy halos (c_s2 = v_stiff > v_vir) does reach 0.7-0.9 Mpc in 2-3 Gyr: the KiDS failure is reachable.
   - Half 2 in groups and clusters (c_s2 < v_vir) cannot expand. Its frozen 7-44 kpc core needs a contraction the
     construction does not drive; no shell or adiabatic solution was computed (stated).
5. **Bullet with pressured halves:** gas-traced FAIL (M300 Z -2.2 / -2.3). The galaxy-traced reading also FAILS.

## MUTATE and known answers

- **MK1 (pressure off): BITES.** KiDS 0.378 (59/59 over).
- **MK2 (v_stiff x 2):**
  - Canonical: NO BITE by the frozen status rule. The numbers move a lot: KiDS 0.085, groups 1/2, S8 -5.2 %.
  - Alt: BITES (CS FAIL, -6.0 %).
- **KA-K1:** the cored-profile closed form matches quadrature to 6e-17.
- **KA-K2:** law-only replay PASS.
- **KA-K3:** with c_s -> 0 the three-fluid ODE returns the reference growth to < 1e-6.
- **KA-K4:** Bullet K1 PASS.

## Reading

K keeps all the mass (so the background, BAO, growth and sigma8 are safe), and puts half of it under pressure with a core
that scales as v_vir^-3. That scaling is the problem:
- galaxy halos puff half their share to about 1 Mpc, which option (c) shows KiDS allows at only about 6-9 %;
- clusters collapse half 2 to 10-40 kpc, which over-fills X-COP's centre by about 6x.

Half 1's fixed 2.6 Mpc core is unreachable at its own sound speed within 6 Gyr.

**What a repair would need:** galaxy-scale halos must keep no more than about 5-10 % of their share within 3 Mpc
(option (c)), while clusters keep about 50-70 % in a profile as extended as TR1's.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Scripts: `ss4.py`, `ss4_cosmo.py`, `ss4_grade.py`, `run_chain.sh`.
- Outputs: `ss4.json` / `ss4.out`, `ss4_MUTATE.json` / `.out`, `parts/` (optc.json, local, cosmo, Bullet), the run logs
  `run_*.txt`.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
