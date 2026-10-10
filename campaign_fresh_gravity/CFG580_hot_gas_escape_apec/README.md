# CFG580: can hidden hot gas supply the KiDS early-type shortfall? ESCAPE OPEN: cool, metal-poor gas could hide below eROSITA

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (c147d86a6). (owner chat 10-09; AtomDB download approved by the owner)
- **Script:** `cfg580_apec.py` → `cfg580_apec.out`, `cfg580_results.json`; MUTATE `CFG580_MUTATE=1` (gas × 0.01) → `_MUTATE`.
- **Atomic data:** AtomDB v3.1.3 (`atomdb_v3.1.3.tar.bz2`, 176 MB, official CfA release, md5 c6f13b893358cc17e35f22cb81a8490b verified), via pyatomdb 1.2.2 with `ATOMDB=../_external_data/atomdb/atomdb_v3.1.3` (outside the repo). Usage reporting disabled (USERID 0). **Disclosed:** on first use pyatomdb fetched its ionisation-balance files (`APED/`, 30 files, ~190 MB) from the AtomDB server automatically, beyond the approved tarball.
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Inputs (from the record)
- Required extra baryons: 0.8 M* (canonical) / 0.55 M* (alt) inside ≈ 100 kpc (CFG531 template row).
- Bound: eRASS:4 quiescent stack at log M* 10.5–11.0, L(0.5–2 keV) = (1.1 ± 0.4) × 10^40 erg/s; 2σ upper 1.9 × 10^40
  (Zhang et al. 2025 Table 3, as recorded in KIDS_HOT_GAS_ESCAPE_NOTE_2026-09-29).

## Result (log M* 10.8, uniform 100 kpc sphere = minimum-luminosity case, rest-frame 0.5–2 keV)
| footing | gas | Z = 0.1 | Z = 0.3 | Z = 1.0 |
|---|---|---|---|---|
| canonical (0.8 M*) | 5.1e10 M☉ | 3.5e39–1.1e40 | 9.8e39–2.9e40 | 3.2e40–9.5e40 |
| alt (0.55 M*) | 3.5e10 M☉ | 1.7e39–5.0e39 | 4.6e39–1.4e40 | 1.5e40–4.5e40 |

(ranges over kT 0.10–0.13 keV, erg/s; bound 1.9e40)

- **Verdict as frozen: ESCAPE OPEN.** The required gas stays below the eROSITA bound for metal-poor gas
  (Z = 0.1 everywhere in kT 0.10–0.13; Z = 0.3 at kT ≤ 0.11 canonical, ≤ 0.13 alt). Solar-metallicity gas would be
  seen above kT ≈ 0.11 keV (canonical).
- Gas fraction that just reaches the bound: f = 1.86 / 1.07 (Z 0.1, kT 0.10 / 0.13), 1.12 / 0.64 (Z 0.3), 0.62 / 0.36 (Z 1).
- A concentrated β-model (r_c 10 kpc) is 1.7× brighter; M* 10.7 / 10.9 shift the luminosities by ×0.63 / ×1.6.
- Controls 2/2: C1 Z = 0 band emissivity 7.31e-25 vs analytic free-free 8.23e-25 erg cm³/s (11%); C2 metals raise it ×9.
- MUTATE (gas × 0.01): ESCAPE OPEN, as required.

## Reading (not a verdict)
- eROSITA cannot exclude the hot-gas explanation of the KiDS early-type shortfall: 0.55–0.8 M* of cool (≈0.1 keV),
  metal-poor (≲0.3 Z☉) gas inside 100 kpc would be X-ray-invisible in the 0.5–2 keV stacks.
- This keeps the shortfall's cause open (missing baryons vs the law), not resolved. Whether such gas exists needs
  other probes (UV absorption around early types, SZ stacks, or the gas's thermal stability at 0.1 keV with that
  density — its cooling time), not more X-ray band data.
- SLUGGS stays closed by measurement (needs ×17–268 its measured gas, CFG528).
