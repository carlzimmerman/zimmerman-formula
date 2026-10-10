# CFG547: cosmic-time triangulation of dark energy, cold energy and galaxy baryons

**Owner request (2026-10-09):** look at the dark-energy density over cosmic time, where the cold energy is clumping and settling at each time, and the baryons in galaxies in relation to all that; triangulate and see if anything meaningful falls out.

κ = ½ is FITTED. The cold energy's mass is required; no particle is proposed. Footings are scored separately (canonical 9.36e-11, alt 1.13e-10) and never pooled. Nothing here closes the theory or says the data favour the framework.

## Files
- `FROZEN_CRITERIA.md`, committed alone first in **55cf38038**.
- `cfg547_timeline.py` takes about 20 s (nice -n 10, 2 threads).
  - Main run: `cfg547.out`, `cfg547_results.json`, `cfg547_timeline.png`.
  - `CFG547_MUTATE=1`: `cfg547_MUTATE.out`, `cfg547_results_MUTATE.json`.
- `TIMELINE.md` holds the descriptive map and the figure.
- Data: everything was already on disk and nothing was downloaded.
  - DESI DR2 w0wa chains, read as CFG511 does.
  - The RC100 corrected table (CFG289).
  - CFG303's native per-galaxy baryons.
  - The typical-galaxy size and gas scalings are recalled values, labelled PROVISIONAL: van der Wel+14 late types, and the record's Tacconi-type μ_gas from CFG217.

## Controls: one FAIL, disclosed
K1, K3, K4 and K5 pass:
- κ c √(Gρ_Λ) = 9.3625e-11.
- DESI a0(2.5)/a0(0) per chain is 0.827 / 0.782 / 0.798, matching CFG511.
- Λ: z_acc 0.632, z_eq 0.296.
- Age 13.796 Gyr.

**K2 FAILS as frozen.** The thin-disc reconstruction of CFG303's g_bar_native_B deviates by up to 4.25e-5 against a 1e-6 tolerance, so both runs exit 1.

Post-freeze diagnostic (2026-10-09, no verdict weight):
- The deviation comes from two input details: the CSV's 4-decimal μ_t18 column, and this script's kpc constant (3.0857e19 m against CFG216's 3.0856776e19).
- With μ recomputed and CFG216's constant, the deviation is 4.4e-7, below the CSV print floor.
- Test (a) reads g_bar_native_B directly, so its predictions are unaffected. The 1e-6 tolerance was set tighter than the stored precision. The frozen text is not edited.

## Verdicts

### Test (a): the cold-energy fraction inside R_e versus z (RC100, N = 100, z quartiles 0.61–0.92 / 0.99–1.53 / 1.53–2.19 / 2.19–2.52)

| model | O1 published f_DM (halo-fit, MODEL-OTHER) | O2 native 1 − g_bar/g_obs | verdict |
|---|---|---|---|
| FLAT a0 | CONSISTENT (max \|Z\| 1.2 canonical / 0.8 alt); slope −0.086 predicted vs −0.080 ± 0.035 observed (Z +0.2) | TENSION: slope −0.088 predicted vs −0.379 ± 0.142 observed (Z −2.3, both footings) | **ROUTE-DEPENDENT → NOT DIAGNOSTIC** |
| DESI-tracking a0 | CONSISTENT (1.7 / 1.3) | TENSION (Z −2.1) | **ROUTE-DEPENDENT → NOT DIAGNOSTIC** |
| RIVAL a0 ∝ H(z) | TENSION: slope −0.007 predicted vs −0.080 (Z −2.2 / −2.3) | TENSION: bin 3 Z −2.9 / −3.2, slope Z −2.9 / −3.0 | **TENSION (Z 2.2–3.2)** |
| NEWTON, a0 → 0 (MUTATE) | TENSION (bin Z up to +6.6) | TENSION (+4.2) | fails, as required |

**Does the decline follow from compact baryons under a fixed a0? YES, as frozen, on both footings.** The rule's three conditions are met:
- The observed O1 decline is significant: −0.080 ± 0.035 per unit z (−2.3σ).
- FLAT predicts a decline of matching size, −0.086, from the native baryons alone.
- FLAT is CONSISTENT on O1.

The decline is not route-robust:
- On the native route the observed fall is 4× steeper than FLAT predicts. The reason is that 41 of 100 discs have native baryons at or above the dynamics (O2 < 0 in the top two bins). That is CFG303's calibration wall, not a dark-fraction measurement.
- So the FLAT verdict word is ROUTE-DEPENDENT.

Model discrimination:
- **FLAT vs RIVAL: NOT DIAGNOSTIC.** The predictions separate by 0.21–0.22 in f_DM in bins 3–4. That clears 2σ (0.13–0.16) on O1 but on no bin of O2. No model reaches |Z| ≥ 3 on both routes.
- **FLAT vs DESI: NOT DIAGNOSTIC.** The separation is ≤ 0.03, against a 2σ noise of 0.13–0.19.

Post-freeze observation, no verdict weight: FLAT under-predicts O1 by a near-constant +0.08 to +0.10 (canonical) or +0.05 to +0.07 (alt) in every bin. Each bin sits at Z ≤ 1.2, and the systematic is shared between bins, so the bins cannot be summed.

MUTATE results:
- M1: Newton fails, as required.
- M2: shuffling z kills the O1 trend. The median |slope| over 200 shuffles is 0.021 against 0.080 real, and 4.5% of shuffles reach |Z| ≥ 2. PASS.

### Test (b): the switch-on epoch
- Under FLAT a0, the outskirts of a typical disc first drop below a0 at different redshifts for each case: z_on = 0.98–3.04 across the 8 cases (2 masses × 2R_e or 3R_e × 2 footings), a spread of 2.06.
- Dark energy took over at z_eq 0.30 and z_acc 0.63 (Λ); the DESI values are 0.33–0.36 and 0.74–0.78.
- **NO ROBUST EPOCH.** Every z_on lies above both dark-energy epochs and depends on mass and radius. The law reached typical outskirts before dark energy dominated, at a time set by galaxy sizes, which are astrophysical inputs. No coincidence is claimed.
- Under the rival a0 ∝ H(z), the outskirts are in the law's regime at all z ≤ 6 (7 of 8 cases).

### Test (c): other relations, no data test

| | relation | label |
|---|---|---|
| C1 | a0/(cH) = κ√(3Ω_DE/8π). It is 0.143 today and 0.014 at z = 6. a0 = cH0/2π would need Ω_DE = 0.849 | **TAUTOLOGICAL** |
| C2 | The census edge (f_ret 0.1) reaches the catchment turnaround radius at z ≈ 1.9–2.8 | DESCRIPTIVE |
| C3 | t_ff(edge) ≈ 3.2–3.9 Gyr at every z, because t_ff(edge) ∝ (GM_b)^{1/4} a0^{−3/4} follows from the edge's definition. It exceeds the age above z ≈ 1.75–2.6. C2 and C3 are the same statement, since turnaround means t_ff ~ age | DESCRIPTIVE; the epoch-independence is by construction |
| C4 | g_bar(R_e)/a0 ∝ (1+z)^2.06 (log M★ 10.7) or (1+z)^2.20 (log M★ 10.0) under flat a0, from PROVISIONAL scalings | DESCRIPTIVE |

## What survived
1. **Compact, gas-rich baryons under an unchanged a0 reproduce the size of the published f_DM decline with z.** On RC100's published route the slope is −0.086 predicted vs −0.080 ± 0.035 observed, and the rule's YES holds on both footings.
   - This is not new physics: it is the law applied to the measured baryons.
   - It is ROUTE-DEPENDENT, failing at Z −2.3 on native baryons, so the FLAT verdict is NOT DIAGNOSTIC.
   - The rival a0 ∝ H(z) predicts almost no decline (−0.007). It sits in TENSION on both routes (Z 2.2–3.2), but the calibration wall keeps the comparison NOT DIAGNOSTIC.
2. **A candidate for a future frozen lane, conditional on the free-fall settling rate (which CFG541 found FREE):**
   - Settling to the census edge takes a fixed ~3.5 Gyr.
   - So systems at z ≳ 2 cannot yet have settled cold energy out to the edge.
   - High-z outer halos would then be under-filled relative to the full census profile.
   - Untested.
3. **No non-trivial coincidence between dark-energy epochs and galaxy epochs.** The a0 ~ cH0 match is the definition plus the present epoch (TAUTOLOGICAL).

Commits: criteria 55cf38038; results in the commit that adds this README.
