# SCS1 RESULT (criteria 5d2870617c; amendments A1 da298a4a52, A2 e079e4b631, A3 1d386d1892)

Commit ids: the hashes in this folder are the shared checkout's (result d157012eae). On origin the same commits are criteria
c9355f4d9d, A1 c88d6cc8dc, A2 b3b863cb75, A3 c54811ca3f and result 0bacbb61f5.

**SCS1: STABLE / STABLE (canonical / alt).** With gravity coupled, the static clock of action (A) is linearly stable. That
is form B's static state: mu_K = 0, no dust of its own, the law's halo around a point baryon mass, gamma_L = 0. Two
independent routes find no growing mode, at any wavenumber, on either footing.

**High-k behaviour.** Nothing grows at any k. The coupled frequency tends to a constant,
omega^2 -> D.P (1 - K m)/m > 0. With the stiffness on, omega^2 rises as k^2 with that positive sign. There is no rate that
rises with k, and no gradient instability.

TEST lane, quarantined. Adopts nothing and relabels nothing. Not registered. kappa = 1/2 FITTED; not theory closed.
Footings are never pooled.

## What it means for form B's static state, in plain words

TPA1 asked whether the law's halo, held static by the clock, would fall apart once disturbed. Around a point mass it does
not. Small disturbances of the clock and of gravity only oscillate. Their rates run from 0.08 to 12 times the local
free-fall rate, so the halo rings and settles back.

The clock resists being bent with a stiffness equal to its own charge density, n_d + D.P. That is the record's conserved
N = rho + Pi. Around a point mass on the law the phantom density D.P is positive, so the stiffness is positive and the
state is stable. Gravity coupling does not change the stiffness. It changes only the clock's inertia, by the factor
1/(1 - K m), which is positive.

This holds with no dust (form B's setting), with dust up to 1e3 times today's mean, and at TPA1's n_crit. The answer does
not change between n_d = 0 and n_d above n_crit: STABLE at mu_K = 0 and at 0.1 per Mpc.

At the CMB-required mu_K* the static state is not stable. The clock then behaves as cold dust on every resolved scale.
Dust and halo clump together at exactly the local free-fall rate, with e-folding times of 17 Myr to 3.9 Gyr. That is
ordinary gravitational (Jeans) collapse, bounded in k: JEANS-ONLY. It is the cosmological setting, not form B's galaxy
setting. FB1 already notes that one K(Q) cannot serve both.

## Labels

| configuration | route 1 (WKB, full covariant, 600 rows) | route 2 (radial eigensolve, l 0/1/2, N 200/400/800) | label |
|---|---|---|---|
| **primary: mu_K 0, n_d 0, gamma_L 0, coupled** | no growing root (smallest omega^2 +4.7e-54 m^-2) | all physical lambda > 0 (smallest 2.5e-16 kpc^-2, inside the WKB band) | **STABLE / STABLE** |
| mu_K 0.1/Mpc, n_d 0 / 1 / 1e3 x mean / n_crit | no growing root | all lambda > 0 | STABLE / STABLE at every n_d |
| mu_K* (8.890e6 / 8.889e6 Mpc^-1), the same four n_d | growing in 585 of 600 rows; Gamma(kr 1e5)/Gamma(kr 1e3) = 0.9993; growth / free fall 0.08 to 1.0000002 | BOUNDED: lambda_min changes by 1.4 to 2.5 % from N 400 to 800; rate / free fall 1.00 | JEANS-ONLY / JEANS-ONLY |
| stiffness on (Lstar 21.7 / 22.9 pc; hand closed form, criteria section 1) | omega^2 > 0 in 400 of 400 rows | not run (hand form only, as frozen) | STABLE / STABLE |

- At mu_K* the e-folding time equals the local free-fall time 1/sqrt(4 pi G (n_d + D.P)). That time is 1.7e7 to
  3.9e9 yr on the grid, and 0.7 to 2.5 times r/v_c.
- The growing mode adds dust and halo with the same sign: delta n_d / delta(D.P) = mu_K^2 Qbar/(K m k^2) > 0, about 1e10 at
  k ~ 1/r and more at larger r. So it is almost entirely dust. This is the analytic WKB value. Route 2's own estimate came out negative and is
  not used: its unstable eigenvectors sit on single grid nodes, because the local rate does not depend on k, so a finite
  difference of chi at the peak is grid noise.
- In the primary, the oscillation rates are 0.08 to 11.9 times the local free-fall rate (kr = 1e3, radial and tangential).
  The local free-fall times are 1.7e7 to 3.9e9 yr.

## Checks

| check | result |
|---|---|
| Route 1 against the hand closed form omega^2 = K G [(1 - K m) k^2 - mu^2 Qbar^2]/(mu^2 Qbar^2 + K m k^2), G = Qbar n_d + D.P, at kr >= 1e3 | max relative 4.3e-7 (line 1e-3), every configuration, both footings |
| Route 2's written tilt term against the local form -(1/2)(D.P)\|grad pi\|^2 | identical spectra (smallest 2.4962e-16 in both) |
| **KA1** decoupled + planar + mu_K* reproduces TPA1 item 6 | 144 rows, relative 1.7e-15; e-folding 5.03e6 to 6.25e8 yr. PASS |
| **KA2** dust Jeans, S = 0 | omega^2 to 1.5e-18 of K n (1 + k^2/mu^2); growth at k = mu/1000 is 0.999999 sqrt(4 pi G n); no growth at k >= 10 mu. PASS (first run: see disclosures) |
| **KA3** TPA1's mixing claim | at mu_K = 0 the kinetic ratio is 1/(1 - K m) to 4.5e-17 and the gradient coefficient is unchanged (exactly 0 change). At mu_K* the claim is wrong by 0.665; the correct factor is 1/(1 - K m - mu^2 Qbar^2/k^2), to 7.3e-17, with the gradient coefficient again unchanged. PASS as frozen |
| **KA4** law off, no dust, point mass (mu_K 0.1/Mpc) | no growth in 240 route-1 rows; route 2 has no negative eigenvalue. PASS |
| MUTATE M1: sign flip of every clock-metric mixing entry | **does not bite** (change exactly 0), as disclosed before any run: it is the field redefinition (phi, psi) -> (-phi, -psi) |
| MUTATE M1b: flip inside the law term only | bites: omega^2 changes by up to x9.4 at mu_K* |
| MUTATE M2: mixing dropped | returns the decoupled result exactly (0.0); differs from the coupled result by up to x170 |
| MUTATE M3: planar background (TPA1's model), primary | bites: all 600 rows grow, bounded in k (ratio 1.000), up to 11.9 x free fall: label NO VERDICT, not STABLE. Route 2's analogue (planar divergence) grows too: BOUNDED, 1.1 to 3.8 x free fall |
| Lean SCS1.lean | 13 theorems, exit 0, standard axioms only. SCS1_MUTATE.lean: 5 false statements, 5 errors, exit 1 |
| No new mode | no (d_t d_t pi)^2 term in the full covariant Hessian; the symbol is quadratic in omega |

## Anything in TPA1 or the FB1 note this lane finds wrong

1. **TPA1 item 6's S = 1 instability is an artefact of its background.**
   - TPA1 froze a planar 2+1 lapse N(x) taken from a point mass's radial profile. In it D.P = p', which is negative because
     the field falls outward.
   - Around a real point mass D.P = p' + 2p/r is the phantom density, and it is positive.
   - The clock's gradient coefficient is n_d + D.P, not n_d + p'.
   - SCS1 reproduces TPA1's numbers exactly in its planar model (KA1), and turning the planar background back on in the
     coupled system brings the growth back (M3).
   - So TPA1's "UNHEALTHY" for the law-on static clock does not hold for a point mass. Its other findings stand: the wall
     is stable, the S = 0 phase is healthy, and S adds no new mode.
2. **TPA1 called it a "gradient instability". Its growth was bounded in k.** omega^2 -> G/m, the same at kr 10 and 1e5,
   which is Jeans-type in rate, not ill-posed. With the stiffness on and G < 0 the rate would rise with k (Lean
   stiffness_unbounded), but G < 0 does not occur around a point mass.
3. **TPA1's hand claim on the mixing** (that it rescales the kinetic coefficient by 1/(1 - S K J'') and leaves the gradient
   coefficient alone) is exact only at mu_K = 0. At mu_K != 0 the factor carries -mu_K^2 Qbar^2/k^2, the Jeans term (KA3).
4. **FB1 note, item 4** ("the static state ... sits in that unstable range") is wrong for a point mass. Form B's static state
   is linearly stable with gravity coupled. The n_crit threshold it quotes does not exist in three dimensions wherever the
   phantom density is positive.
5. TPA1's EQUATIONS.md section 5 and RESULT.md items 5 and 6 carry the same planar statement. This lane does not edit them.

## What this lane does not settle

- **The nonlinear outcome.** This is linear stability only. Finite disturbances, mode coupling and caustics of the
  irrotational clock are not computed.
- **The collapse.** Nothing here shows a free-falling clock reaching the static state. Stability of the end state is not a
  path to it. FB1 item 2 stays open.
- **The cosmological background.** Not addressed. At the mu_K the CMB needs, the static state is Jeans-unstable at the
  free-fall rate, so the galaxy setting and the CMB setting still need different mu_K.
- **Non-spherical baryons.** Only point masses were analysed. For flattened systems the law's phantom density can be negative
  in places. There G = n_d + D.P < 0 gives bounded growth at gamma_L = 0, and with the stiffness on a rate that rises with k
  above 1/Lstar. Discs are therefore not settled. Extended spherical baryon distributions were not run either.
- **Approximations.** Newtonian order; quasi-static metric; shift and momentum constraint dropped by 1PN order counting (not
  computed). WKB with frozen coefficients, plus a radial solve for l <= 2 on [3 kpc, 1 Mpc] with clamped ends. The
  background's own dust gravity is neglected in the brackets. The stiffness bracket comes from the hand form only.

## Disclosures

- **A1.** Growth is read from the Hermitian part of the WKB symbol, as TPA1 did with Re P. Decided after one probe
  background. The antihermitian (transport) part gives |Im omega| up to 2.0e-23 / 2.3e-23 m^-1 on the primary rows,
  falling with kr; it is kept as a diagnostic.
- **A2** (zero tolerance 1e-12 of the largest eigenvalue) and **A3** (keep eigenpairs whose eigenvector carries the clock
  perturbation, |zeta|/|v| > 1e-4) are post hoc. Both were decided after one route-2 row showed -3.1e-20 kpc^-2. That mode
  is a 0/0 null mode of the substitution pi = (chi - phi)/(i omega). The physical and null families are five decades apart.
  The partial runs are kept: scs1_radial_run1_partial.out and scs1_radial_run2_partial.out.
- **KA2, first run.** It failed at k = mu_K, where the target omega^2 vanishes: the script divided by it (rel 3.0 on two
  values that are both zero to 1e-21 of the scale). The test is now measured against K n (1 + k^2/mu^2) with the same 1e-6
  line. The first output is kept as scs1_wkb_run1.json / .out. No other number changed.
- **KA3** was evaluated at kr 1e6 and 1e8. The criteria did not fix kr; at kr 1e3 the O(1/kr) coefficient-gradient terms
  would exceed the frozen 1e-6 line.
- **My pre-freeze expectation (STABLE, TPA1's result planar) is the outcome.** The lead's and TPA1's expectation (the
  gradient instability survives coupling) is not.
- **Resources.** Route 1 builds its Hessian in about 265 s. The main run takes 432 s and each MUTATE arm about 300 s. Route
  2 ran as three single-thread parts of up to 20 min each. Everything stays under 0.15 GB. Lean is compiled in
  fable_independent_2026/lean_2026. Nothing was downloaded.

## Files

- Criteria and amendments: FROZEN_CRITERIA.md, AMENDMENT_A1.md, AMENDMENT_A2.md, AMENDMENT_A3.md.
- Route 1: scs1_wkb.py -> scs1_wkb.json / .out (first run scs1_wkb_run1.*), and scs1_wkb_MUTATE_{M1, M1b, M2, M3}.json / .out.
- Route 2: scs1_radial.py -> scs1_radial.json / .out, scs1_radial_run1_partial.out, scs1_radial_run2_partial.out.
- Stiffness bracket: scs1_stiffness.py -> scs1_stiffness.json / .out.
- Lean: SCS1.lean, SCS1_MUTATE.lean, compile.txt, compile_MUTATE.txt.

Not registered. Does not edit fable52_push/README.md, any PAPER file, the register, the decision files, TPA1's or FB1's files.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
