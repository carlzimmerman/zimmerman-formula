# CFG563: CFG561's void lensing test redone with GAMA spectroscopic redshifts. NON-DISCRIMINATING. Purity is fixed but the test is UNDERPOWERED (declared before scoring)

**Ledger line:** CFG563 KiDS isolated lenses matched to GAMA DR4 spectroscopic redshifts (1.5″), environment from the published
GAMA tidal-tensor catalogue (Eardley+2015 GeoS4; the Alpaslan+2014 void class has only 160 lenses), void vs (M*, z_spec,
colour)-matched outside. The positive control now PASSES: void lenses have far fewer GAMA neighbours (T = −0.46 ± 0.015 dex,
−32σ). Outer bins 0–7: Δ = −0.04 ± 0.28 dex (−0.14σ). K1: −0.19 ± 0.28. Result: NON-DISCRIMINATING. Power to see a 0.1 dex outer
offset at 3σ is 0.4%, and the expected 2σ null bound is 0.54 dex. The spectroscopic overlap holds only 2,050 void lenses
across 12 June patches. κ fitted; cold mass still required; not theory closed.

- **Criteria:** `FROZEN_CRITERIA.md` (7f876f805), committed alone before any script or lensing number.
- **Script:** `cfg563_voids_specz.py` (~8 s). Main run: 5/5 checks pass, exit 0. MUTATE (flags shuffled): C3 fails, exit 1.
- **Data:** per-lens sums `real_research/data/lensing_rar/cfg110_perlens.npz` + `lr_lenses.npz` + `lr_esd_jackknife.npz`
  (read only). GAMA DR4 from Data Central TAP: Eardley+2015 `GalaxiesClassifiedv01` (git-ignored, `_external_data/cfg563/`)
  and Alpaslan+2014 `Fil/Tendril/VoidGalsv02` (`data/`). CFG471's `G3CGalv10.csv` is reused read only, and its sha256 matches
  CFG471's log. The script checks all five hashes (`FETCH_LOG.md`). This is pure data, so the a₀ footings (9.3603e-11 /
  1.1312e-10) do not enter.

## Verdict table

| row | N_void (N_out) | Δ outer (bins 0–7), dex | Δ K1 (bins 8–14), dex | tracer T, dex | verdict |
|---|---|---|---|---|---|
| **headline** GeoS4 void vs sheet/filament/knot, matched | 2,050 (6,092; eff. 4,753) | **−0.038 ± 0.282 (−0.14σ)** | −0.193 ± 0.284 (−0.68σ) | −0.462 ± 0.015 | **NON-DISCRIMINATING** (both) |
| headline, 36 sub-patch jackknife (reported) | 2,050 | −0.038 ± 0.252 | −0.193 ± 0.278 | −0.462 | — |
| GeoS10 void (reported) | 1,707 | −0.37 ± 0.31 (−1.2σ) | −0.98 ± NaN | −0.43 | — |
| void vs sheet + filament, knots dropped (reported) | 2,050 | −0.035 ± 0.293 | −0.20 ± 0.30 | −0.44 | — |
| early only (reported) | 883 | −0.72 ± NaN | −0.30 ± 0.36 | −0.46 | — |
| late only (reported) | 1,167 | +0.36 ± 0.33 (+1.1σ) | +0.05 ± 0.50 | −0.46 | — |
| Alpaslan void vs filament + tendril (reported) | 157 | +0.64 ± 0.37 (+1.7σ) | −0.19 ± NaN | −0.27 | — |

"NaN" means at least one jackknife replicate had a pooled ESD ≤ 0, so its log ratio is undefined. This happens because the
outer signal of a few hundred to ~1,000 lenses is noise-dominated. Those rows carry no usable error. No row reaches 2σ.

## Power (printed before any void number)

From 100 random analysis-set subsets of the void size (2,059), matched the same way, the expected σ_Δ is 0.27 dex for the outer
bins and 0.19 dex for K1. P(3σ | true 0.1 dex) = 0.004 (outer) and 0.007 (K1). P(3σ | 0.3 dex) = 0.03 and 0.08. The expected 2σ null
bound is 0.54 dex, and NULL needs < 0.1. In 5 of the 100 outer subsets the log ratio is undefined. The lane was declared
**UNDERPOWERED** before scoring. Spectroscopic membership removes CFG561's purity loss (0.40 → 1). It also shrinks the sample
from 10,472 to 2,050 void lenses and the jackknife from 25 to 12 patches, so the net error is ~4× worse than CFG561's.
Simple σ ∝ N^−½ arithmetic on the printed σ puts a 3σ test of 0.1 dex at roughly 70× more void lenses with spectroscopic
environment, beyond GAMA × KiDS-1000.

## Controls

- **C1a PASS:** the per-lens sums reproduce CFG88's full-sample K1 split to 5 × 10⁻¹⁴, with χ² 35.0418/7 (CFG561's C1).
- **C1b PASS:** the same early/late split inside the GAMA footprint gives a K1 log ratio of +0.116 ± 0.055, against +0.182 for the
  full sample (−1.2σ, 12 patches).
- **C2 PASS:** the chance-match rate is 0.14% of the real 1.5″ match rate (20,542 of 34,872 footprint lenses matched).
  69 lenses with a catastrophic photo-z were dropped.
- **C3 PASS (the positive control CFG561 failed):** void lenses have 0.46 dex fewer G3CGal neighbours within 8 Mpc/h projected
  and ±1000 km/s (−32σ). The Eardley flag is built from GAMA density, so this checks the flag-to-lens pipeline. It does not
  independently show that voids exist (stated in the criteria).
- **C5 PASS (reported):** the null z-spread is 0.82 (outer) and 0.97 (K1).
- **MUTATE:** shuffling the flags (seed 563) gives T = −0.002 ± 0.007 and C3 FAILS, so the script exits 1. The shuffled Δs are null:
  outer −0.24 ± 0.31, K1 +0.06 ± 0.21. Note that the shuffled outer value is larger than the real one. That shows how noisy the
  outer bins are at this size.

## Departures (disclosed)

1. **Catalogue choice, decided on counts only, before freezing.** The task preferred Alpaslan+2014, but its void class holds
   160 matched lenses. The headline uses the other published GAMA LSS catalogue, Eardley+2015 GeoS4. Alpaslan is kept as a
   reported row.
2. **The ESD uses the photo-z.** The per-lens sums were built with photo-z lens redshifts and are not recomputed. The spec-z sets
   environment, matching cells and the tracer.
3. **Bug fix after run 1.** Run 1 read P = NaN (undefined outer log ratios in the power subsets) as "powered". The fix makes
   NaN, or any undefined subset, count as UNDERPOWERED, which is the only reading consistent with the frozen P < 0.5 rule.
   It changes no Δ, error or verdict. Run 1 is kept as `cfg563_voids_specz_RUN1_powerNaN.out` / `_results.json`.

## Reading

- CFG561's tracer failure is fixed. With spectroscopic environment, "void" really does select empty surroundings at −32σ.
- The lensing contrast is unmeasurable at this size: ±0.28 dex in the outer bins. No sign is seen. The headline is slightly
  negative at −0.14σ. The reported early/late, GeoS10 and Alpaslan rows scatter in both directions at < 2σ, and nothing is
  claimed from them.
- Even a future SETTLING-SIGN would not separate settling from ΛCDM by itself, because the 2-halo term is lower around void
  galaxies in ΛCDM too (frozen caveat). The FORCE-SIGN foil is neither supported nor excluded here.
- What would make this test bite: spectroscopic environment over a much larger lensing area, for example DESI BGS with
  KiDS-Legacy or a later lensing survey. Of order 10⁵ void lenses are needed.

κ = ½ fitted. No dark-matter particle: the framework's cold mass is still required, amount free. Not theory closed. Nothing here
says the data favour the framework over ΛCDM.

## Files

`FROZEN_CRITERIA.md`, `FETCH_LOG.md`, `cfg563_voids_specz.py`, `cfg563_voids_specz.out` / `_results.json` (main),
`cfg563_voids_specz_MUTATE.out` / `_results.json`, `cfg563_voids_specz_RUN1_powerNaN.out` / `_results.json` (run 1, power
bug), `data/{Void,Tendril,Fil}Galsv02.csv` (Alpaslan+2014, Data Central).
