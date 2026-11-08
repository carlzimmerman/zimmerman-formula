# CMB1: anatomy of the primary-CMB requirement for a cold component

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Anatomy lane (cold dark energy; no particle). Footings graded
separately, never pooled. No LCDM prior.
- **Criteria:** FROZEN_CRITERIA.md (local a66f9d1254, origin 0b04506ce2), committed and pushed alone before any script
  or number.
- **Scripts:**
  - cmb1.py uses F1A's own likelihood (own CamSpec NPIPE P-ACT cut + ACT DR6 reader) and CAMB 1.6.6.
    - `base` writes parts/base.json.
    - `fit E|B` writes parts/fit_*.json, run by run_c.sh.
    - `post` writes parts/post.json.
  - ob_scan.py writes parts/ob_scan.json (a reported reading).
  - cmb1_grade.py writes cmb1.json / cmb1.out and cmb1_MUTATE.json / cmb1_MUTATE.out.
- **Resources:** one thread, peak 0.69 GB, nothing downloaded.
- **Subagents not used.** The blocks ran one after another, not as one subagent per block as asked. Each block loads the
  likelihood (0.6-0.9 GB), so parallel runs would break the < 1 GB rule. This was frozen.

## Label: NO VERDICT (lane), because M1 failed on its frozen rule. Block C reads CLUSTERING PINNED on both footings

**Why NO VERDICT.** M1 swaps omega_b and omega_d at the cold best fit.
- It moves the odd/even ratio H1/H2 by +343 sigma and the third-to-second ratio H3/H2 by +197 sigma, on both footings.
- The frozen rule asked the two shifts to differ by sign, or by a factor outside [0.5, 2]. They are in the same direction,
  ratio 0.57, so M1 fails.
- Reading: H3 is also a compression peak, so extra baryon loading raises it too. Also, the swapped spectrum's third peak
  moves to L 461, outside the fixed L 760-880 window, so the window estimator extrapolates there.
- The frozen expectation was wrong in direction. The estimator, KA-1 and M2 are fine.
- The readings below are reported under NO VERDICT, not as a lane verdict.

## Block C: which the data pin, equality epoch or baryon density

| | canonical | alt |
|---|---|---|
| Baryons-only DeltaMB (F1A) | +172,915.6 | +166,674.4 |
| **E**, smooth matter-like component, c_s^2 = 1 (sets z_eq and the expansion, does not cluster): Delta_E | **+35,812** | **+35,378** |
| Share of DeltaMB recovered by E, f_E | **0.79** | **0.79** |
| E best fit omega_X / omega_b | 0.108 / 0.0215 (R 5.0) | 0.108 / 0.0230 (R 4.7) |
| **B**, baryon density free to 0.20: Delta_B | **+172,905** | **+166,674** |
| Share recovered by B, f_B | 0.0001 | 0.0000 |
| Apparatus gate 10 O (KA-E) | 248, passed | 233, passed |
| Block C label | **CLUSTERING PINNED** | **CLUSTERING PINNED** |

- **Baryons-only profile over omega_b** (ob_scan, lnA re-fit, tau 0.06):
  - chi2 rises monotonically from omega_b 0.03 to 0.20: 181k -> 323k (canonical, n_s 1.3); 175k -> 324k (alt).
  - More baryons only make it worse. The B fit sits at omega_b 0.022.

## Block A: where the 170k sits (additive, c_i = r_i (C^-1 r)_i; the pieces sum exactly, M2)

| piece | canonical | share | alt | share |
|---|---|---|---|---|
| Planck TE 30-500 | +30,517 | 17.6 % | +30,969 | 18.6 % |
| Planck TT 500-1000 | +28,330 | 16.4 % | +27,578 | 16.5 % |
| ACT TT 1000-2000 | +25,487 | 14.7 % | +23,551 | 14.1 % |
| Planck EE 30-500 | +21,233 | 12.3 % | +20,212 | 12.1 % |
| Planck TT 30-500 | +13,335 | 7.7 % | +11,925 | 7.2 % |
| ACT EE 600-1000 | +10,250 | 5.9 % | +9,262 | 5.6 % |
| ACT TT 600-1000 | +9,030 | 5.2 % | +8,547 | 5.1 % |
| ACT TT > 2000 | +8,783 | 5.1 % | +6,708 | 4.0 % |
| ACT TE 1000-2000 | +8,494 | 4.9 % | +9,824 | 5.9 % |
| ACT EE 1000-2000 | +8,005 | 4.6 % | +8,510 | 5.1 % |
| Planck TE 500-600 | +6,376 | 3.7 % | +5,388 | 3.2 % |
| Planck EE 500-600 | +1,866 | 1.1 % | +3,372 | 2.0 % |
| ACT TE > 2000 | +1,706 | 1.0 % | +1,146 | 0.7 % |
| ACT TE 600-1000 / ACT EE > 2000 | -659 / -99 | | -546 / -40 | |
| calibration priors | +263 | 0.2 % | +268 | 0.2 % |
| L < 30 | no data in PA | | no data in PA | |

- By spectrum (canonical): TT 49 %, TE 27 %, EE 24 %. No single piece carries more than 19 %.
- The baryons-only failure is spread over every multipole range and all three spectra.
- After E (no clustering), the 35.8k left over sits mostly in Planck TE 30-500 (11.9k), Planck TT 500-1000 (8.9k),
  Planck EE 30-500 (3.8k) and Planck TT 30-500 (3.6k). That is, at L < 1000, around the first three acoustic peaks.

## Block B: the physical features (one estimator on data and models; z in data sigma)

| feature | data (sigma) | cold | baryons-only | E (no clustering) |
|---|---|---|---|---|
| H1 / H2, odd/even (baryon loading) | 2.210 (0.030) | -0.2 | +35.1 / +27.3 | **-16.2 / -15.6** |
| H3 / H2, the third peak | 0.976 (0.009) | +0.9 | +66.4 / +61.6 | **-36.8 / -36.7** |
| damping ratio, ACT TT 2000-3000 over 600-1000 | 0.0619 (0.0009) | +0.6 | **+126.1 / +112.2** | +4.9 / +7.7 |
| first peak L1 | 223.1 (2.2) | -1.1 | +84.3 / +65.1 | -15.9 / -15.7 |
| peak spacing (L3 - L1) / 2 | 295.3 (1.4) | +0.3 | -63.1 / -59.1 | +17.7 / +17.9 |

- The cold fit meets every feature within 1.1 sigma.
- Values are canonical / alt. The B column equals baryons-only within 0.2 sigma.
- The baryons-only and swapped spectra have peaks outside the fixed windows, so their feature values are window
  extrapolations, not true peak positions.
- Feature z values are not additive with block A.
- **Carrier statement (frozen rules).**
  - At baryons-only, the largest miss is the damping ratio (+126 / +112 sigma).
  - At E, the largest miss is the third-to-second peak ratio (-36.8 / -36.7 sigma).
  - The frozen third-peak rule (F_32 off by more than 5 sigma while L1 and the spacing are within 3) is not met, because
    E also misses L1 by -16 sigma and the spacing by +18 sigma.

## In plain words (reported under NO VERDICT)

1. **Baryons alone fail everywhere, not in one feature.** The deficit is about 170k, spread across all three spectra
   and every range of L. No piece carries more than 19 %. Raising the baryon density never helps: chi2 rises
   steadily to omega_b 0.20.
2. **About 4/5 of it is the expansion history.** A smooth matter-like density of omega ~ 0.108, about 5 x baryons, that
   only sets the expansion (matter-radiation equality, sound horizon, distance to z 1100) and never clusters, recovers
   79 % of the deficit. That part of the requirement says "the universe at z 1100 holds about 5 x the baryon density in
   something that redshifts like matter". It does not by itself say the thing clusters.
3. **The last 1/5 (Delta about +35.6k, still enormous) is clustering.** With that same density smooth, the model misses:
   - the third-to-second peak ratio, 0.644 against the data's 0.976, at -37 sigma;
   - the odd/even ratio, 1.73 against 2.21, at -16 sigma;
   - the first-peak position, 188.5 against 223, at -16 sigma (in data sigma).

   The deficit sits around the first three peaks in TE, TT and EE. These are the features of potential wells that stay
   put through recombination, made by a component that does not feel photon pressure. When the matter is smooth, the
   potentials decay inside the horizon, the odd peaks lose their extra compression, and the third peak drops.
4. **Could anything else produce it?**
   - In this lane: neither the expansion alone nor baryon density alone.
   - CMB2 (cd1c7c35a3): no degree of freedom in the action supplies a still potential. The law's phantom follows its
     source, with one open item at a0(z 1100) >= 30 x today, which no record history gives.
   - So what would do it is anything that holds still potential wells of the right depth at k ~ 0.03-0.3 through
     z 1100. A pressureless clustering component of ~5 x baryons does. Nothing else tested in the record does.

## Known answers and MUTATE (cmb1_MUTATE.json)

- **KA-1:** the rebuilt DeltaMB equals F1A's, 172,915.56 / 166,674.43. **PASS.**
- **M2:** the pieces plus the prior row sum to the total to < 1e-9. **PASS.**
- **KA-E:**
  - Background: fluid H(z) within 3.6e-7 and theta* within 1.7e-6. **PASS.**
  - Apparatus offset O: 24.8 / 23.3. That is the fluid at c_s^2 = 1e-6 vs real cold dust at the cold best fit. Delta_E is
    over 1,400 x O, so it is graded.
- **M1: FAIL** (above), so the lane label is NO VERDICT.

## Disclosed

- **E fit edges.** The E fit sits at bracket edges:
  - n_s at 1.30 on both footings;
  - omega_b at the 0.0215 floor (canonical);
  - tau at the 0.01 floor (alt).
  A wider n_s bracket could lower Delta_E. The baryons-only fits also sit at n_s 1.3, as in F1A and QX15.
- **L < 30.** There is no L < 30 data. tau is free with a flat bracket, so nothing graded rests on reionization.
- **Fluid apparatus.** It uses a tabulated w(a) with c_s^2 = 1 for Lambda + X. Its low sound speed version matches the
  cold model only to O = 24 chi2, which is small next to Delta_E.
- **Pre-freeze sight.** The fluid feasibility test was seen before the freeze, at a non-fit cosmology. With c_s^2 = 1
  the first peak sat at L 165.
- **F1A amendment A2** (2b55e1e2df, after the F1A result) corrects G4's start (CMB2's finding). CMB1 does not use G4.

Kappa = 1/2 FITTED; not theory closed.
