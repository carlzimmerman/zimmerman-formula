# CFG665: thermal equilibrium is not the selector

**Label as frozen: VOID (K1 fails).** **Reading, verified post hoc: S\* has no regular solution for any baryon distribution.** An
isothermal settled cold energy with the co-retained cosmic share, a universal edge acceleration f_b a₀ and edge pressure
(f_b a₀)²/8πG cannot be closed at the centre. The D1 numbers in `cfg665.out` are artifacts and carry no meaning.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (79599c03e), 2026-10-12. Block CFG660–669.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
- **Script:** `cfg665.py` (one process, a few minutes) → `cfg665.out`, `cfg665_results.json`. MUTATE was not run: the lane is
  VOID at its control, and the teeth would test artifacts.

## What happened

| item | result |
|---|---|
| K1 (Hernquist a = 0.01 r_M, r_min = 1e-3 r_M) | σ⁴ +4.96 dex above G M_b a₀/4 → **K1 FAILS → VOID** |
| D1 as run (meaningless, see below) | 97 of 175 galaxies (55%) "unsolvable"; on the rest rms 0.54 vs law 0.17, mean residual −0.38 |
| **Diagnostic (post hoc): r_min dependence** | the shooting root grows without bound as the inner cutoff shrinks: σ = 1297 / 3636 / 10474 / 30633 km/s at r_min = 1e-3 / 1e-4 / 1e-5 / 1e-6 r_M (×2.8 per decade), **identically** for a = 0.01 r_M and a = 1 r_M |
| diagnostic: other concentrations | a/r_M = 0.01 to 30 with a small r_min: no root up to 2000 km/s |

The "root" is only the σ at which the cold mass happens to run out exactly at the chosen cutoff. As r_min → 0 it diverges: there is
no σ for which the inward-integrated isothermal cold sphere ends regularly at the centre.

## Why (the flaw in the derivation, stated plainly)

The disclosed identity σ⁴ = G M_tot g_e/4 with M_tot = M_b/f_b is exact for a singular isothermal sphere of **total** mass, i.e. if
the baryons shared the isothermal profile. In S\* only the cold component is isothermal. The three edge conditions are then those of
an SIS of total mass, while the baryons, concentrated inside, deepen the potential; the Boltzmann factor drives the cold density
above the SIS inward and the supply is exhausted at finite radius for every finite σ. This is the same physics as CFG461's finding
that the SIS is the unstable centre of the Emden spiral, now with baryons: the isothermal family has a free core, and these
universal edge conditions cannot fix it consistently.

## Consequence for the selector

Thermal equilibrium of the settled cold energy, closed by a universal dark-energy-scale edge, is **not** the selector. Together
with the record this closes the c-carrying routes tried so far:

| route | result |
|---|---|
| any c-free mechanism (violent relaxation, max entropy, virialisation, adiabatic response, Jeans marginality) | excluded by CFG461's c-test (σ⁴ is linear in c) |
| law applied to all mass (C2b) | wrong state, +0.2 dex, double counting |
| Unruh/de Sitter bath (C3a) | c cancels; one σ for all galaxies |
| vacuum-pressure edge a₀²/8πG (C3b) | σ free |
| baryon heating Q = C a₀ v ρ_b | CLOSED (CFG643) |
| energy-bounded settling (ρ_DE c² capacity) | not derivable knob-free (CFG645) |
| local stress of the cold energy | NO-GO with {G, a₀} (CFG660, CFG661) |
| **isothermal + universal edge (S\*)** | **no regular solution (this lane)** |

The unexplored c-carrying channel left is a direct cold-energy/vacuum coupling with real microphysics (for example astra's
four-form portal, `sol61_push/cold_production_2026_10_11/FOUR_FORM_PORTAL.md`, or the record's Henneaux–Teitelboim Λ field, CFG43).
