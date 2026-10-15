# CFG806: can the framework derive the baryon census f_ret(M_ta)? NOT DERIVED as frozen. A ceiling-only energy budget gets the SHAPE

- **Criteria:** `FROZEN_CRITERIA.md` (fb6a0f9d4), committed alone first.
- **Script:** `nice python3 cfg806.py` (seconds) → `cfg806.out`, `cfg806_results.json`. `CFG806_MUTATE=1` (e_SN = 0) → `_MUTATE`, exits 1.
- **Settings:** κ = ½ fitted; footings never pooled; no dark matter particle species; not theory closed.

**Question.** CFG804 closed the inner KiDS lensing with N = 1/f_ret, but f_ret is the observational census (CFG416). Can the
framework predict it? The framework inputs are the law, the native turnaround catchment (CFG654 Δ_ta) and f_b = 1/6.364.

**External inputs (provisional):**
- SN energy, 10⁴⁹ erg per M☉ formed;
- the record's Tozzi–Norman cooling fit (CFG640);
- IGM temperatures 10⁴ / 10⁶ K.

## Result: f_ret (ratio to census) at log M_ta = 12 / 13 / 14 / 15

| mechanism | canonical | alt | class |
|---|---|---|---|
| census (CFG416) | 0.10 / 0.325 / 0.70 / 0.90 | | |
| **M2 PRIMARY** (energy, with stars only from gas that cools; t_cool = r/V), ε = 1 | 0.99 / 1.00 / 1.00 / 1.00 (×9.9 at 12) | same | **NOT DERIVED** |
| M1 (energy; every retained baryon becomes stars), ε = 1 | **0.16 / 0.46 / 0.75 / 0.90** (1.60 / 1.41 / 1.07 / 1.00) | 0.19 / 0.50 / 0.77 / 0.91 | SHAPE DERIVED |
| M1, ε = 0.1 | 0.78 / 0.92 / 0.97 / 0.99 | | NOT DERIVED |
| M3 (accretion vs the catchment's escape) | 1 / 1 / 1 / 1 | same | NOT DERIVED |

KiDS check (N ≥ 3 / 4 at CFG804's bins):
- M2 gives N ≈ 1 in both footings: **FAIL**.
- Post-freeze diagnostic, M1: N = 6.4 / 4.5 / 4.1 / 3.5 canonical, which passes. The alt footing gives 6.6 / 4.4 / 4.0 / 3.4, which fails in bin 4 (it needs 4).

## Reading
1. **The frozen primary fails.** Cooling decides it:
   - In the framework's potential, retained gas spread to r_ta (0.8–8 Mpc) sits at kT 0.14–4 keV.
   - Only 0.1–0.4% of it can cool in a dynamical time (χ ≤ 0.004 at log M_ta ≥ 12).
   - So few stars form, there is little supernova energy, and nearly everything is retained (f ≈ 1).
   - The fixed point is unique (post-freeze root scan).
   - The cooling channel cannot by itself produce a 10% census.
2. **The one near-hit, M1, is not a derivation:**
   - It lifts gas from r_M to r_ta in the law's logarithmic potential, ΔΦ ≈ 3.3–4.7 V², using all the supernova energy.
   - That gives f = ΔΦ/(ΔΦ + e_SN). The trend comes out right: within ×1.5 at 13–15, and ×1.60 at 12 (canonical; alt ×1.85).
   - But it needs **ε = 1**, i.e. every supernova erg doing work against gravity, with nothing radiated. It also needs every retained baryon to cycle through stars.
   - Both are ceilings, not physics. At a typical ε = 0.1 the retention is 0.78 at log M_ta 12.
   - Treat M1 as a bound: even maximal stellar feedback in the law's potential only just reaches the census.
3. **Accretion (iii) retains everything.** The law's deep potential to r_ta (ΔΦ ≈ 4 V², V ≥ 150 km/s) captures gas at 10⁴ and at 10⁶ K. This is the same reason the photo-evaporation selector (CFG782) only acts on the smallest systems.
4. **What follows:**
   - The census still enters CFG804 as an observational input, so CFG804's inner-lensing closure is not parameter-free.
   - A framework mechanism would have to expel ≈ 85–90% of a galaxy catchment's baryons, or stop them accreting. Nothing on record does this without a ceiling-level efficiency.
   - Open channels, not run here: AGN at full coupling (the bracket barely moves M2); gas concentrated rather than spread to r_ta, which would change χ; pre-heating at z ≈ 2.

**Disclosed.**
- Gas is taken as ρ ∝ r⁻² out to r_ta (a frozen choice). A concentrated profile would cool more.
- The potential is that of the final retained mass, which makes ejection cheapest.
- M_ta is taken in M☉ (the M☉/h bracket is reported).
- MUTATE bites trivially for M2, since it is already NOT DERIVED. For M1 it bites properly: SHAPE becomes NOT DERIVED.
- K1–K3 PASS.

κ fitted; not theory closed.
