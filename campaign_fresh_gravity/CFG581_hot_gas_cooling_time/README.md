# CFG581: can CFG580's hidden hot gas persist? ESCAPE UNPHYSICAL as a hot halo: it would cool out in 0.4–4 Gyr

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (59dad4b30). (owner chat 10-09)
- **Script:** `cfg581_cooling.py` → `cfg581_cooling.out`, `cfg581_results.json`; MUTATE `CFG581_MUTATE=1` (mass × 0.01) → `_MUTATE`.
- **Atomic data:** AtomDB v3.1.3 already local from CFG580 (`ATOMDB=../_external_data/atomdb/atomdb_v3.1.3`); no new downloads (directory size unchanged).
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Setup
Required gas 0.8 M* (canonical) / 0.55 M* (alt), M* = 10^10.8, in a uniform 100 kpc sphere (the lowest density, so
the LONGEST cooling time — the most favourable case for the escape). Scored only in CFG580's X-ray-hidden cells.
Free fall in the law's own deep-limit field: v_c ≈ 194 / 196 km/s, t_ff ≈ 0.71 Gyr; hydrostatic kT ≈ 0.12 keV
(inside the 0.10–0.13 keV range used).

## Result (log M* 10.8)
| footing | n_H (cm⁻³) | hidden cells | t_cool range | max t_cool / t_ff | heating needed to stay hot |
|---|---|---|---|---|---|
| canonical | 3.5e-4 | Z 0.1 (all kT), Z 0.3 (kT ≤ 0.11) | 0.76–2.9 Gyr | 4.0 | 3.4–9.9 × 10^41 erg/s |
| alt | 2.4e-4 | Z 0.1, Z 0.3 (all), Z 1 (kT 0.10) | 0.35–4.2 Gyr | 5.9 | 1.6–14.6 × 10^41 erg/s |

- **Verdict as frozen: ESCAPE UNPHYSICAL** on both footings: t_cool / t_ff < 10 in every hidden cell (precipitation
  threshold ≈ 10, PROVISIONAL literature value declared in the criteria). M* 10.7 / 10.9 give max ratios 4.8 / 3.4
  (canonical) and 7.0 / 5.0 (alt). A concentrated β-model (r_c 10 kpc) has a central density ×16.8 higher, so its
  centre cools ×17 faster.
- The power needed to keep it hot (10^41.2–10^42.2 erg/s) would be radiated 96–99% below 0.5 keV, i.e. outside the
  eROSITA band — which is exactly why it hides there.
- Controls 2/2: C1 Λ(1 keV, Z = 0) 8.92e-24 vs bremsstrahlung 8.01e-24 (11%); C2 metals raise Λ(0.12 keV) ×30.
- MUTATE (mass × 0.01): t_cool/t_ff rises to 400–590, ESCAPE PHYSICALLY ALLOWED, as required.

## Reading (not a verdict)
- The KiDS early-type shortfall cannot be a static, X-ray-hidden hot halo: gas cool and metal-poor enough to hide
  from eROSITA cools in a few free-fall times, unless something continuously re-heats it at ≈ 10^41.5 erg/s.
- **What this does NOT exclude:** the same mass already cooled into ≈10^4 K clouds (cool CGM), which X-rays never see.
  UV absorption surveys (e.g. COS-Halos) report substantial cool gas around L* galaxies, including passive ones; that
  route needs measured cool-CGM masses inside 100 kpc for early types (provisional pointer, not checked here).
- So: hot-gas escape closed (CFG580 + CFG581); a cool-gas escape remains untested.
