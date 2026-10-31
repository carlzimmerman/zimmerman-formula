# CR2_core_scale_origin: the S(M) slope is collapse scaling, so it is not a carrier filter

**Verdict: ORIGIN IS COLLAPSE (T1), and self-coupling is not needed for the slope and has no valid window on the alt footing (T3, T5).** This corrects CR1. "Collapse scaling" is a statement about P(k) and formation time. It does not derive the core form or the amplitude. κ = ½ FITTED. Not "theory closed". Criteria: `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`. Script: `cr2_check.py`.

**My error in CR1.** I labelled 1/3 as Σ_coll's scaling and offered S ∝ M^0.24 as a filter on carriers. The record's Σ_coll runs M^0.24, and the brief's version N already has S = f_c η Σ_coll. CR1's row-by-row grades stand; that reading does not.

| test | result |
|---|---|
| T1 slope | Σ_coll 0.247–0.254 against ET1 0.238 ± 0.034, z +0.26 to +0.47 in all four variants: **ORIGIN IS COLLAPSE** |
| T2 ratio | S_need = 32.4 ± 1.9 Σ_coll, χ² 5.35 for 5 dof, one number across 20–400 km/s. Flat S: χ² 54.5. A/f_cη = 1.49 at 1e12, 2.18 at 1e13, 2.28 at 1e14: amplitude is open at Υ 0.50 (see T6) |
| T3 self-coupling slope | q 0.71 ± 0.10, n 0.43 ± 0.20; OS1's q_f within 1.7σ, 0.3σ. It fits too, but OS1's dwarf caps sit 5.7σ, 4.9σ below. Row J: dwarfs EXCLUDE, R7 fail |
| T4 lock on a heavy field | R gives m 663–2423 GeV over T* 130–200 GeV, c 0.1–10. Above p = 5's floor of 556; one corner (663) is under p = 7's 685. A field quantum at that mass is a heavy particle by any test: R7 fails |
| T5 validity | b₁M ≥ 1 at 20 and 1000 km/s: p = 7 **invalid** by 1e3 (b₁M 9e-4 at cluster speeds). p = 5 invalid at clusters by × 3 (0.32), valid at 20 km/s (1.55). Factor 3 is within order-unity coefficients, so p = 5 is marginal, not excluded |
| T6 X80, post-result | Native exponent 10¹⁰–10¹²: **0.242 smooth, 0.239 converged**, z +0.12, +0.04, with no extrapolation. S_need/native cold S ≈ 1.2–1.6 at Υ 0.50 |

## Where it lands
1. **The slope needs no new microphysics.** Native zooms give it on the record's own P(k), and X80 finds η flat at 0.026 per dex. Self-coupling reproduces it only with a new constant and fails dwarfs.
2. **The amplitude at galaxies is tied up with Υ.** At Υ 0.50 SPARC asks for about × 1.5 more than the zooms. X80's native version N passes the SPARC line at Υ 0.70 / 0.72 with no floor, though with Υ running from 1.20 in dwarfs to 0.54 at 150–200 km/s. This is not two gaps. Galaxy-to-cluster, ratio A/f_cη changes × 1.5, as FC1's cluster keys show.
3. **What is still open for a carrier.** Not the slope. It is core form (zooms make cusps; X81) and crossing streams without quanta (CR1). η is a smooth-core fit to cusped halos, so agreement in S does not say the halo is cored.
4. **Limits.** S_need's errors are sample scatter only. M200 comes from the fitted EM1 relation, built on NFW halos, so the slope inherits that choice. ET1's 1/3 exclusion should not be read as a physics result.
