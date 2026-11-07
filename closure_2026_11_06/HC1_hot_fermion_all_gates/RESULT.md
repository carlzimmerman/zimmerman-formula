# HC1: a light thermal fermion with the a0 law. FAILS: it blocks on 7 of 9 gates on both footings

EXPERIMENT. Adopts nothing; the no-particle rule is lifted for HC1 only. Kappa = 1/2 FITTED; not theory closed.
Footings are graded separately and never pooled. Nothing here says the data favour the framework.

- Criteria: FROZEN_CRITERIA.md (c207d70254), committed alone before any script.
- Scripts:
  - hc1.py: GB1's battery G1-G8, exec'd read-only, with HF1's solver.
  - hc1_g9.py: CMB-lensing shape, QX3 iter2's statistic.
  - hc1_report.py: post-freeze readings, reported only.
- Each grading script has a MUTATE twin (*_MUTATE.*).
- Compute: one thread, minutes each.

**Label: FAILS.** The fermion passes SPARC (G1) and the Solar System (G8) on both footings. It fails X-COP, groups,
ellipticals, Coma UDGs, the dSph classes, the KiDS split and CMB-lensing shape (G2-G7, G9) on both footings.

## The fermion, fixed once

- **m = 11.1377 eV**, g_f = 2, Fermi-Dirac, thermal at T_nu (CLASS T_ncdm 0.71611).
- **How it was fixed:** a fermion that decoupled while relativistic at T_nu has omega_f = m / 93.14 eV. HC1 sets
  omega_f to the cold abundance the record's own lensing fit needs: QX3 iter2's worst-corner dust, omega_d = 0.11958
  (the corner QX7/QX10 use, with omega_b 0.0215). So m = 93.14 x 0.11958 eV.
  - CLASS returns omega_ncdm = 0.11958 at this m (KA5).
  - Cosmic ratio R = 5.562, the record's own value.
  - Nothing is fitted per gate. G9 fits only A_s.
- **How it enters:** separate collisionless stress-energy. The graded rule (TOT) has the a0 law act on baryons plus
  fermion. Rule BAR (law on baryons, fermion Newtonian) is reported only; it moves no label.
- **Profile in each system:** HF1's rule R4. The fermion is isothermal in the law's potential, holds a fair share
  (R x baryons) inside turnaround, and is capped by Tremaine-Gunn at the system's own sigma = V_max / sqrt 2.

## Gate x footing (canonical / alt)

| Gate | Line | Canonical | Alt | Blocks? By how much |
|---|---|---|---|---|
| G1 SPARC (not retained by discs) | \|Z\| <= 0.057, rms <= rms(L0) + 0.010 | PASS: Z +0.012, rms 0.1355 (line 0.1457) | PASS: Z -0.018, rms 0.1372 (line 0.1425) | No. Weak row, see disclosure 3 |
| G2 X-COP | \|mean\| <= 0.05, rms <= 0.10 | FAIL: +0.392, rms 0.411 | FAIL: +0.360, rms 0.381 | **Yes**, +0.34 / +0.31 dex over the mean line. HF1's own pipeline at this m reads +0.178 / +0.147, rms 0.260 / 0.240: also FAIL (disclosure 2) |
| G3 groups | >= 16 of 20, f* = 0 and 1 | FAIL: 0 and 3 of 20 (median residual +0.211 / +0.062) | FAIL: 0 and 3 of 20 (+0.173 / +0.025) | **Yes**, 16 / 13 groups short |
| G4 ellipticals | \|mean\| <= 0.15 | FAIL: +0.207 | FAIL: +0.184 | **Yes**, +0.057 / +0.034 dex over |
| G5 Coma UDGs | \|mean\| <= 2 sigma_U | FAIL: +1.120 (+4.27 sigma_U) | FAIL: +1.077 (+4.11 sigma_U) | **Yes**, 2.3 / 2.1 sigma_U beyond the line. At the MAXIMUM fermion bound still +1.000 (3.82 sigma) / +0.953 (3.63 sigma) |
| G6 dSph classes | each 95 % CI contains 0 | FAIL: bright M31 +0.214 [+0.094, +0.408]; MW classical +0.232 [-0.034, +0.559]; LG field +0.034 [-0.012, +0.179] | FAIL: bright M31 +0.205 [+0.086, +0.400]; others contain 0 | **Yes**, bright M31's CI misses 0 by +0.094 / +0.086. Not robust: a host fermion sea at 50 kpc would pass it (disclosure 5) |
| G7 KiDS colour split | \|R\| < 2 sigma_tot | FAIL: R +0.155 (2.42 sigma) | FAIL: R +0.155 (2.42 sigma) | **Yes**, 0.42 sigma beyond. The fermion predicts no split (D_cand +0.003) |
| G8 Solar System | uses <= 1 | PASS: 0.211 (planets), Cassini 2.8e-8 | PASS: 0.190, 2.0e-8 | No |
| G9 CMB-lensing shape (footing-free) | worst-corner chi^2 <= 18.48 | FAIL: chi^2 166.0-194.2 over 8 corners | (same) | **Yes**, 10.5x the line at the worst corner. The same omega as dust gives 8.3-8.9 |

## Known answers and twins (all pass)

| Check | Result |
|---|---|
| KA1: fermion off reproduces GB1's L0 (59 graded numbers per footing) | max \|d\| 0, both footings |
| KA2: HF1's own X-COP pipeline at m 11.8 reproduces HF1 | +0.178197 / 0.259719 canonical, +0.147592 / 0.239806 alt; \|d\| 4e-11 |
| KA3: Tremaine-Gunn closed form | ratio 1.000000000000 |
| KA4: 608 solves | all converged, no cap violation, fair share held wherever the cap does not bind |
| KA5: QX3 iter2 corner | dust chi^2 8.5709, baryons only 895.33, CLASS omega_ncdm 0.11958 |
| G9 twin, baryons only | min chi^2 869 > 18.48 at every corner: BITES |
| Static twin M2, Newton + fermion | fails G1 on both footings: BITES |
| Static twin M1, cap x 1e4 (a CDM-like, phase-space-free species) | fails G1 on alt only (rms 0.1451 vs 0.1425). Canonical passes (Z -0.016, rms 0.1367): **NO POWER on G1 canonical**, as frozen (disclosure 3) |

## What blocked it, physically

1. **Phase space does the "not in galaxies" job, and that is all it does.**
   - The Tremaine-Gunn cap binds in every SPARC galaxy, elliptical, UDG and dSph (cap-binding share 1.0).
   - So the fermion is nearly absent where the law already works. Median M_f/M_b is 0.04 at SPARC's R_last (max
     0.84), 0.002 in the ellipticals, 0.002 inside the UDGs' r_h and 3e-6 in the dSphs.
   - The same cap keeps it out of the systems that need it. dSph sigma 4.5 km/s and UDG sigma 18 km/s give caps of
     8e-28 and 5e-26 kg/m^3. The UDGs sit +1.1 dex (about 12x) above the law, and even the most generous bound reachable from
     the data (twice the degenerate limit, plus Coma's whole mean interior density) adds at most 0.06-0.19 dex.
2. **Clusters and groups are supply-limited, not phase-space limited.** The cap binds in no cluster or group.
   - At X-COP's graded radii M_f/M_b is 0.31.
   - With HF1's longer baryon chain the fermion has more supply (M_f/M_b 0.6-3.7), but its shape is wrong: +0.42 at
     0.1 R500, -0.09 at 0.7 R500.
   - Groups take M_f of about M_b and stay under the line (0-3 of 20).
   - So the triangle's "present in clusters at the measured boosts" fails on profile and amount together.
3. **Isolated galaxy halos retain it.** In the KiDS lenses (50-290 kpc) M_f/M_b is 0.7-1.6.
   - Reported, not a graded row: late-type lenses are over-predicted by +0.21 dex (canonical) / +0.25 (alt).
   - The fermion adds the same +0.18 to early and late lenses, so it cannot make the observed colour split (G7).
   - This is QX12's T2 violated, the same way QX7's switched sector was killed.
4. **Free streaming kills CMB-lensing shape.**
   - Linear P(k), fermion over dust at the same omega, z = 0: 0.99 at 0.01 h/Mpc, 0.84-0.89 at 0.03, 0.05-0.12 at
     0.1, 0 at 0.27. The half-power point is at about k 0.04 h/Mpc (interpolated), a comoving scale of about
     150 Mpc/h.
   - After the amplitude refit the model is 1.32-1.36x the data in the lowest PR4 bandpower and 0.34-0.44x in the three
     highest (up to L 400).
   - An 11 eV thermal relic is a hot species; the lensing kernel sees the missing small-scale power. This is HF1's
     gate-1 failure seen in the lensing channel (HF1's primary-CMB cells at m 11 and 11.8, p about 1e-69, carried).
5. **The VW1 conflict, sharpened.** A colder spectrum would fix G9 (dust at the same omega passes, 8.3-8.9). But a
   colder fermion fills discs: M1, the phase-space-free twin, puts M_f/M_b 0.45 into SPARC's R_last. This lane cannot
   tell that apart on G1 canonical; VW1's Upsilon floor can.

## Disclosed (post-freeze)

1. **KA2 inputs regenerated.** CRG1's inputs/ held only its MANIFEST, so HF1's pipeline could not run. I ran CRG1's
   own extract_inputs.py, redirected into this lane's cache_crg/ (git-ignored), with --no-efe. 307 of 309 files are
   sha256-identical to CRG1's MANIFEST. The 2 EFE tables were not built and are not used by xcop_rows. hc1.py's input
   path was edited after the first run crashed on the missing file, before any graded number existed.
2. **X-COP has two readings.** The graded cell uses GB1's points. Their baryon profile stops at Mb_last, so the fair
   share inside turnaround is smaller than in CRG1's chain, which extends the gas out to r_ta. HF1's pipeline at
   HC1's m and R (reported in hc1.json) gives +0.178 / +0.147, rms 0.260 / 0.240. Both readings fail, by 3-8x the
   mean line.
3. **G1 has little power for disc retention at fixed Upsilon.** GB1's rms line is L0's own rms + 0.010, so a CDM-like
   species (M1) passes canonical. G1's PASS means the fermion does not break SPARC's fixed-Upsilon RAR. The direct
   evidence that discs do not retain it is the small M_f/M_b (0.04 median), set by the Tremaine-Gunn cap.
4. **Profile readings declared in the criteria:** KiDS Hernquist a = R_med/20, UDG/dSph Hernquist at r_h, z = 0 for
   every turnaround radius, the Solar-System density at the Milky Way cap (4.7e-4 Msun/pc^3, 1.3e-20 m/s^2 at Saturn).
5. **dSph host sea (hc1_report.py, reported).** MW and M31 solved with HC1's rule, with Hernquist baryons of
   6e10 / 1e11 Msun (a = 3 / 4 kpc). These are readings chosen post-freeze.
   - Sea density at 50 / 100 / 200 kpc: 6-7e-5, 1.0-1.4e-5, 1-2e-6 Msun/pc^3.
   - Added to each satellite, G6 passes at 50 kpc (bright M31 +0.150 [-0.035, +0.405] canonical) and fails at 100 and
     200 kpc.
   - So G6's FAIL depends on where the satellites sit. The criteria's maximum bound (34x the host cap) is too loose
     to decide it.
   - It does not change the label: six other gates block.
6. **G9 is footing-free:** linear CLASS has no a0 term (HF1's liability, stated). WG1-WG6 already show that the law's
   late boost cannot repair the shape.
7. **Primary CMB (TT/TE/EE) was not regraded.** HF1's FD cells at m 11 / 11.8 (fitted temperature) fail at p about
   1e-69. HC1's T_nu relic carries N_eff 4.05.

Kappa = 1/2 FITTED; not theory closed.
