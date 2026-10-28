# EF1_basin_external_field: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run the IC 1613 / field-dwarf lane with the AQUAL external field
from the Local Group basin's total mass, graded on the stellar sigma."

**Why.**
- The literature check (2c6b17d683) found IC 1613's HI inclination contested.
- The inclination-free stellar-σ tracer (HO3) still over-predicts it.
- X1's external field for the field dwarfs used the **Milky Way's baryons alone** (MOND field of 6e10 M☉ at the dwarf's
  heliocentric distance; IC 1613 x_e = 0.013).
- In the basin picture (BS1, 979363d820), the LG basin's total gravitating mass is 10^12.392 M☉: baryons plus
  cold dark energy halos, i.e. Newtonian mass under route E. The field dwarfs sit at BS1's barycentric distances R.

**Expectation, stated before the run (disclosed).**
- A rough estimate gives x_e ≈ 0.017 for IC 1613, close to X1's 0.013.
- IC 1613's internal field at r₁₂ (with X1's M★) is about 0.04.
- **The EFE is therefore expected to change IC 1613 by little.** The lane is run because the owner asked and because the
  record has not graded the basin field.

**Standing rules.**
- κ = ½ FITTED.
- Footings never pooled; canonical is primary.
- Cold dark energy is not matter and not a particle.
- No ΛCDM number enters a rule.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads.

## 1. Method (frozen)

**External field.** For each of the 13 LG field dwarfs (X1's class), at BS1's barycentric R:
- g_e = G M_basin / R², with M_basin = 10^12.392 M☉ (BS1 `LG.basin.lgM`). The basin mass is treated as Newtonian
  (route E halos are Newtonian mass), and all of it is taken as enclosed (R ≥ 415 kpc).
- x_e = g_e / a₀ per footing.
- Antlia B has no R in BS1. It keeps X1's x_e (disclosed).

**Solver.** X1's exact 2D AQUAL + EFE solver: `d10_solver` read-only, with S1's wrappers and X1's grid nper 24, Nt 16.
- log G_iso = logG(y₀, 0, 0) and log G_EF = logG(y₀, x_e, 0), at X1's y₀ = G M★ / (r_h² a₀), using the E-W estimator
  (column 0).

**Graded residual.**

    E_EF = E_HO3 − (log G_EF − log G_iso)

E_HO3 is HO3's committed law-branch E (stellar σ). Z = E_EF / s, with s = HO3's s.

**Reported:**
- the same calculation at X1's own x_e (sanity: X1's iso/emb difference);
- a variant with FD1's UNGC baryons (M★ from K + HI), where y₀ uses M_b.

## 2. Verdict (canonical primary; alt reported with its own)

| verdict | condition (IC 1613) |
|---|---|
| **BASIN FIELD RESOLVES IC 1613** | \|Z\| < 2 |
| **BASIN FIELD REDUCES IC 1613** | \|Z\| ≤ ½ × 6.75 |
| **BASIN FIELD DOES NOT HELP** | otherwise |

**Also reported:** HO3's S1, S2 and S3 on all 13 field dwarfs with E_EF.

## 3. Checks and twin

- **K0.** At X1's x_e, (log G_emb − log G_iso) reproduces X1's committed tables (emb0 − iso0 at the middle y) to
  0.002 dex for IC 1613, WLM and Leo T.
- **K1.** The isolated deep-limit control: X1's C3a check (solver against σ⁴ = (4/81) G M a₀) passes to 0.005 dex at
  y = 1e-3.
- **K2.** Peak RSS < 1 GB.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`EF1_MUTATE=1`, separate outputs).** x_e is computed with M_basin × 100, so K0 must still pass but a K3
  check fails. K3 is the rule "x_e < 0.1 for every field dwarf", a sanity bound on the basin field.

**Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ef1_basin_external_field.py`
