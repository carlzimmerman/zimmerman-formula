# CFG878 — deriving the cold-energy fragment (clump) mass

Criteria: `FROZEN_CRITERIA.md` (f39ef2490, committed alone before the script; owner block 870–879). Run: `python3 cfg878.py`
(`CFG878_MUTATE=1` → constant bath). Under a minute, numpy only. κ = ½ fitted; ν_e; footings never pooled.

## Results
**A. The fragment mass is set by its velocity dispersion alone (derived, the law only).** A self-gravitating isothermal cold-energy
clump under the full law has total mass M = f · 81σ⁴/(4Ga0), with f = 0.75–0.95 over a 300× range of central density (deep
limit f → 1). For σ = 7.53 km/s: 4.0–5.0e6 M_⊙ canonical (3.4–4.1e6 alt). K-A1 PASS (deep limit within 5%); K-A2 PASS (Newtonian
run gives M ∝ r, slope 1.004). So "derive the fragment mass" reduces exactly to "derive the fragment's σ".

**B. The record's own bath gives the wrong scaling — RECORD BATH EXCLUDED (both footings).**
- **The derivation.** The record's bath (CFG544/554/558) is the settled cold energy's own Jeans dispersion. A fragment relaxed to
  it inherits the host's σ, and the law then gives M_frag ≈ (2.9–4.3) × M_b of the host. That is (81/16) f in the deep limit,
  and smaller at r½.
- **The comparison.** Fragment mass therefore scales one-to-one with the host. On CFG872's 19 dwarfs the record-bath slope is
  s_rec = +1.045, against the measured +0.241 ± 0.163 (**4.9σ**); alt +1.016 against +0.253 ± 0.253 (3.0σ).
- **The absolute mass is right only in the middle.** Median M_frag is 2.7e6 against a measured 4.3e6. But Leo IV gets 4.5e4
  (measured 2.2e5), Fornax 1.4e8 and NGC 185 1.1e9 (measured clumps 5e6–3e7). This is the same over-fill CFG853 found.
- **So the cold-energy equations as written cannot make the clump.** The bath needs a universal velocity scale from outside the
  cold sector.
- *(81/16 = 5.06 is close to the record's 5.364; it is not used and is flagged as a coincidence.)*

**C. Universal velocity scales from fixed physics (hypothesis; POST-HOC comparison).**
| candidate | σ (km/s) | M_frag canonical (M_⊙) |
|---|---|---|
| **(i) neutral primordial gas at the hydrogen-cooling floor, 8000 K–10⁴ K (μ = 1.22)** | **7.36–8.22** | **3.6e6–7.1e6** |
| (ii) ionized gas, same T (μ = 0.59) | 10.6–11.8 | 1.5e7–3.0e7 (×6 too heavy) |
| (iii) σ² = a0 L*, L* ≥ 24 pc | ≥ 8.33 / 9.15 | ≥ 6.0e6 (CFG858's coincidence) |

The measured clump σ (CFG877 7.53 / 7.49 km/s) lies inside candidate (i). **H-GASBATH: CONSISTENT (post-hoc).** CFG872's per-dwarf
medians (7.16 / 6.56) sit just below the bracket.

**How (i) could work (two routes, neither in the record yet):**
1. **A cold-energy–gas coupling** that relaxes cold energy toward the gas's velocity dispersion. It must vanish in mergers
   (α ≈ 0, CFG623/641).
2. **The record's own bath acting once, in the first systems that can cool.** Gas cools by atomic hydrogen only in systems with
   σ ≳ σ(8000 K), so the first star-forming systems have σ ≈ 7.4–8.2 km/s. Their cold energy relaxes to that σ and fragments at
   M ≈ 81σ⁴/(4Ga0). The clump is then inherited and kept: overfill that later settling does not drain, the record's open
   "overfill not handled" item.

Route 2 predicts a clump mass independent of today's host (s ≈ 0; measured 0.24 ± 0.16) and of environment (CFG873–875: no host
effect). It also predicts no clump in systems that never went through atomic cooling. That last part is untested, and collision
debris such as DF2/DF4 is a possible case.

## Controls
- K-A1 PASS, K-A2 PASS.
- **K-B1 FAILED as frozen.** It compared σ_J at r12 with the deep-limit formula, which holds only at r ≫ r_h (ratio 2.96 against
  4.30). **Post-hoc diagnostic (disclosed, added after the run):** at 5–50 r_h the code gives σ_J within 1.5% of V_flat/√2 and
  M_frag/M_b = 4.07–4.25 against 4.30. The code is right, and the frozen check was mis-specified. The slope result does not
  depend on it.
- MUTATE (constant 7.5 km/s bath) → s_rec = 0.000, CONSISTENT. The slope tracks the bath.

## What is and is not derived
- **Derived:** M_frag(σ) (Part A); the record bath's s ≈ 1 and its exclusion (Part B).
- **Not derived:** the value σ ≈ 7.5 km/s. Candidate (i) matches it, but post-hoc, and either route needs physics the record
  does not contain yet.

## Audit notes (2026-10-20; Codex arrival audit `sol61_push/cold_final_mile_2026_10_13/gas_bath_arrival_2026_10_20/`, checked here)
- **Equal-temperature thermal contact cannot transfer 7.5 km/s.** In thermal equilibrium σ² = k_B T/m depends on the carrier's mass.
  At 8000–10⁴ K, 1 MeV carriers would have 249–278 km/s, and much heavier lumps far less. Candidate (i) survives only as
  velocity inheritance in a shared potential (route 2: cold energy relaxing to the same per-unit-mass dispersion as the gas in the
  first cooling systems), not as thermal equilibrium with the gas. Route 1 would need velocity matching (drag), not heat exchange.
- **Catchment stock.** A universal 5.25e6 M_⊙ clump exceeds the record's largest catchment stock (53.64 M_b) for every dwarf with
  M_b ≲ 1e5 M_⊙ (the ultra-faints). The clump therefore cannot be drawn from a stock proportional to today's baryons. Route 2
  requires the stock to be set by the progenitor's original baryons.
