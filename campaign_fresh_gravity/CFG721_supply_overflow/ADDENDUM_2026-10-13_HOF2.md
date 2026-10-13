# CFG721 ADDENDUM (2026-10-13): the two-population variant H-OF2. Committed alone, before H-OF2 is computed

This addendum does not edit `FROZEN_CRITERIA.md` (93d53f734). It was written while the H-OF stages were still running and before
any H-OF target score existed (only the T-K pair runs and the ACCEPT runs had finished; their logs show overflow fractions, and no
statistic against data had been computed). Requested by the orchestrator after CFG722 (cold_kinetic_bridge) and CFG724.

## New inputs since the freeze
- CFG722 (identification coupling, B8): tethered cold energy has a capacity, mean Σ̄_c(<r) ≤ a₀/πG = 213.8 / 258.3 M☉ pc⁻², and a
  tethered core exports any excess to the basin edge. Overflow can sit in a core only as a SECOND, UNTETHERED population.
- CFG724: the Bullet cores hold 3.6–4.8× that capacity; SPARC deep-regime Σ stays below it (median ≈ 0.3).

## H-OF2 definition (no new constant)
- **Tethered part:** the law's settled phantom of the source (all / cond), cut at its own supply edge and confined to r_ta (as
  H-OF), additionally capped at M_teth(<r) ≤ a₀ r²/G (mean Σ̄ ≤ a₀/πG). In the code this is the kernel
  ν_cap(y) = min(ν(y), 1 + 1/y), since M_ph = (ν − 1) M_src and a₀r²/G = M_src/y.
- **Free part:** supply − tethered, collisionless, moving in the total potential, placed by CFG637 Method A (unchanged).
- Everything else (catchment, supply, harnesses, statistics, pass rules, both kernels, both footings, both sources) as frozen.

## A derivation fact found while writing this addendum (disclosed; it decides the expectation)
- For ν_s, (ν_s − 1) y = y(√(¼ + 1/y) − ½) < 1 for every y (square both sides: ¼ + t < ¼ + t + t², t = 1/y). **The law's own
  phantom never reaches the capacity** — this is CFG695's saturation, and CFG722's wall is the same statement.
- For ν_mono, (ν − 1) y exceeds 1 only for y > 2.65 × 10⁵ (g_N > 2.65 × 10⁵ a₀, the innermost parsecs of a baryonic centre), by at
  most 4.3%, on a phantom that is itself ~1/y ≈ 4 × 10⁻⁶ of the baryons there.
- **Expectation:** the cap binds nowhere observable, so H-OF2's tethered part equals H-OF's settled phantom and H-OF2's free part
  equals H-OF's reservoir. H-OF already places the reservoir as an untethered collisionless population (CFG637's G9). H-OF2 is then
  numerically H-OF, and its scores are H-OF's scores.

## Verification rule (frozen here)
- Run the H-OF2 kernel ν_cap for both base kernels on: the 8 ACCEPT clusters (all sources, kernels, footings), the T-K pairs, and
  the first 20 eRASS1 clusters (canonical, both kernels, both sources).
- If max |ΔΣ_HOF2/ΔΣ_HOF − 1| ≤ 1e-3 over all of them (and the overflow fractions agree to 1e-3), H-OF2 takes H-OF's scores on
  every target, reported side by side. If not, H-OF2 is scored on every target with the full stage runs (a new run, reported).

## Added target: Bullet cores (both H-OF and H-OF2)
- Source: CFG637's committed Bullet B1 runs (cfg637_gates_results.json, T4 core, primary RD/P/phase cells). H-OF(cond) = H-CB and
  H-OF(all) = candidate B, ν_mono. ν_s is NOT run for the Bullet (disclosed; the cell is "not run").
- Disclosure: those CFG637 numbers were already in the record and were read while writing this addendum (main M(<250 kpc)/P16 =
  0.786 / 0.775 cond, 0.323 / 0.347 all; sub 0.11–0.18).
- P16 (Paraficz+16, M(<250 kpc) 2.5e14 / 2.0e14 M☉) is PROVISIONAL (recalled, no quoted error in the record). Declared band:
  **PASS iff 0.75 ≤ M_model(<250)/P16 ≤ 1.25 for the main AND the sub, on both footings.** The sub is input-mass-limited
  (CFG629); a sub fail is reported with that caveat but still counts.
- Capacity check (reported): the tethered part's mean Σ̄(<250 kpc) must be ≤ a₀/πG; the free part carries the rest.

## Verdict
H-OF2 is reported per (source, kernel) exactly like H-OF, with the Bullet core added to both. Post-hoc, every target already seen.

κ fitted; cold energy mass required; not theory closed.
