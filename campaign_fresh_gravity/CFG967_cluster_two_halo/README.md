# CFG967: the framework's catalogue two-halo term around the 318 eRASS1 clusters (NA-5). NO EFFECT on both footings; NA-5 is killed

**Plain summary.**
1. CFG687 found that the shear 1.2–3 Mpc from eRASS1 clusters grows with gas mass like M^0.90, steeper than the law's M^0.47. This lane asked whether unseen neighbours around the clusters could explain the gap.
2. The neighbour term is CFG903's own, with no free amplitude: every KiDS-bright galaxy near a cluster, carrying its own baryons and cold energy, minus the same sum around random points.
3. Added to the law, it moves the slope by +0.003 (canonical) and −0.001 (alt), far below the pre-declared 0.1 threshold, so the class is **NO EFFECT** on both footings. No bracket changes that.
4. Even with no exclusion at all (which double counts the clusters' own galaxies), the neighbour term is a near-constant 12% of the law in every gas tercile. It grows like the law, so no multiplier on it can steepen the slope past about 0.49.
5. The core excess (A_MID about 1.9 / 1.75) is untouched. The outer slope problem stays open; it is driven by the light, low-redshift clusters falling below the law, which no positive environment term can fix.

Block CFG960–969 (LEDGER reservation row). Criteria `FROZEN_CRITERIA.md` (**908091f9b**, committed alone before any script).
`AMENDMENT_A1.md` (**7a7faac97**): the d grid was aligned on CFG687's edges after run 1 failed the kernel control K3b. It was made
before any score, with no two-halo vector, A value or slope inspected. Angle NA-5 of `NEW_ANGLES_SCOUT_2026-10-21.md`.

## Law statement (coordinator note, 10-23)

- **Primary:** the record's current statement, AQUAL with μ = x/(1+x) (doors_push E2 / PAPER58). On CFG687's spherical cluster
  model this is exactly g = ν_s(g_N/a0) g_N with ν_s = ½ + √(¼ + 1/y). K5 checks the identity to 6e-16.
- **CFG687 used ν_mono** (FP1's monotone repair of ν_RAR) in the same algebraic form. Its rows are carried in full here.
- The two kernels differ by ≤ 0.3% in A and ≤ 0.001 in s_law.
- CFG903's neighbour cold-energy profile is already the μ = x/(1+x) point-mass phantom, so the primary is one consistent statement.

## Result (primary: AQUAL ν_s, exclusion X1 = each cluster's own catchment edge, C1′, W500, P1, unmasked)

| footing | law | A_MID before → after | A_OUTER before → after | slope s before → after (Δs) | class |
|---|---|---|---|---|---|
| canonical | **ν_s (primary)** | 1.907 ± 0.118 → 1.911 ± 0.119 | 1.011 ± 0.087 → 1.025 ± 0.089 | **0.4664 → 0.4691 (+0.0027)** | **NO EFFECT** |
| canonical | ν_mono (CFG687) | 1.910 → 1.914 | 1.012 → 1.026 | 0.4658 → 0.4685 (+0.0027) | NO EFFECT |
| alt | **ν_s (primary)** | 1.751 ± 0.109 → 1.756 ± 0.109 | 0.926 ± 0.079 → 0.938 ± 0.082 | **0.4639 → 0.4633 (−0.0006)** | **NO EFFECT** |
| alt | ν_mono (CFG687) | 1.754 → 1.759 | 0.927 → 0.938 | 0.4634 → 0.4628 (−0.0006) | NO EFFECT |

- Observed slope: s_obs = **0.896 ± 0.209** (CFG687, reproduced exactly).
- The jackknife σ of s_model(after) is 0.040 / 0.039.
- **A_OUTER stays consistent with 1:** Z = +0.16 (canonical) and −0.43 (alt), with σ_tot including CFG687's random-minus-random
  offset (+0.130 / +0.119). With that offset subtracted, A_OUTER is 0.896 / 0.819.
- **A_MID (core excess): not touched** (|ΔA_MID| = 0.004 / 0.005, against σ 0.118 / 0.109).
- **Headline: NO EFFECT** on both footings. Footings never pooled.
- No bracket flips the class. No advance appears in a double-counting bracket either.

**Brackets (one at a time; Δs canonical / alt; every one is NO EFFECT):**

| bracket | Δs canonical / alt |
|---|---|
| X2, edge from Mgas500 only | −0.017 / −0.017 |
| X3, 3 Mpc | −0.001 / −0.001 |
| E0, no exclusion | +0.004 / +0.004, with A_MID down to 1.58 / 1.47 (double counting) |
| C0 | +0.002 / −0.002 |
| C2′ | +0.002 / −0.002 |
| W300 | +0.001 / −0.002 |
| W1000 | +0.029 / +0.028 |
| P0 | +0.004 / +0.001 |
| P2 | +0.002 / −0.001 |
| M1 | +0.001 / −0.003 |
| ν_mono | +0.003 / −0.001 |

**Gas terciles (CFG815's middle-tercile issue), canonical, primary:**

| tercile | A_OUTER before → after | A_MID before → after |
|---|---|---|
| light (z 0.145) | 0.568 → 0.575 | 1.39 → 1.40 |
| middle (z 0.235) | 0.964 → 0.986 | **2.23 → 2.23** |
| heavy (z 0.311) | 1.376 → 1.386 | 2.00 → 2.00 |

- The middle tercile's core excess is unchanged.
- Alt has the same pattern: A_OUTER 0.52 / 0.90 / 1.27 and A_MID 1.29 / 2.05 / 1.84 after.

**Reported only:**
- **The two-halo stack is tiny.**
  - OUTER: −0.23 ± 0.09 M☉ pc⁻² (canonical), −0.22 ± 0.09 (alt), against a law of 16.4 / 17.9.
  - MID: −0.05 / −0.07.
  - It is slightly negative because the primary edge, median 2.1 / 1.9 Mpc, removes the correlated neighbours inside the band.
- **The random-only (hole) term is −2.0 / −2.1 M☉ pc⁻²,** so the subtraction is essential. K4 shows it is unbiased.
- **Hosts:** no neighbour is more massive than a cluster.
- **The amplitude needed to reach s_obs (or s_obs − 1σ)** is not reached for any multiplier from 0 to 200.
- **Z17 (z ≥ 0.17, 207 clusters, terciles re-cut):**
  - s_obs drops to 0.642 ± 0.112.
  - s_model goes 0.471 → 0.481 (canonical) and 0.468 → 0.475 (alt).
  - So the steepest part of the observed slope comes from the low-z light clusters. This is a pointer, not a verdict.

## Post hoc check of the fail (`cfg967_posthoc.py`; not frozen, no verdict weight)

- **The term grows like the law.**
  - Under E0 (everything kept), the two-halo OUTER per tercile is +1.19 / +2.00 / +3.36 M☉ pc⁻², against a law of
    10.1 / 17.7 / 26.5. That is a constant 12% (11.8 / 11.3 / 12.7%), and the term's own slope is about 0.50.
  - A multiplier scan levels off: s = 0.470 / 0.484 / 0.494 at ×1 / ×10 / ×50 (canonical; alt the same to 0.003).
  - So s_obs − 1σ = 0.686 cannot be reached at any amplitude.
  - X2's term even falls with mass (s goes down as the amplitude rises).
- **What the data would need.** The additive OUTER term each tercile needs for A_OUTER = 1 is −4.4 / −0.6 / +10.0 M☉ pc⁻²
  (canonical) and −5.3 / −2.3 / +7.6 (alt).
  - The light tercile needs mass *removed*, so no positive environment term can fix it.
  - The heavy tercile's need is 3.0× (canonical) and 2.3× (alt) even the double-counting E0 term.
- **The pipeline can see a slope change.** A planted term 0.5 × law × (M_gas/median)^0.43 moves s by +0.149 on both footings
  (expected about +0.14).

## Controls

| control | result |
|---|---|
| K0: completeness functions rebuilt from CFG903's stage JSON vs its stored per-lens values | 0 difference — PASS |
| K1: CFG687 reproduced: ν_mono law = stored PL; A MID/OUTER for canonical, alt and Newton; s_obs, s_err, s_law, s_N | max \|Δ\| 0 — PASS |
| K2: CFG903's stored T2h_primary (both footings, 4 bins × 15) from its own histograms via the exec'd kernel/exclusion code | max \|Δ\| 0 — PASS |
| K2x: this lane's G route = CFG903's verbatim twoh_table / T_at on the same histogram | 0 — PASS |
| K3a: kernel limits | 0 — PASS |
| K3b: uniform field in CFG687's 8 bins | 8.0e-5 Σ₀ — PASS (run 1: 4.6e-3, FAIL → A1) |
| K3c: kernels finite | PASS |
| K4: random halves A − B, OUTER | −0.021 ± 0.022 (−1.0σ) canonical, −0.025 ± 0.022 (−1.1σ) alt — PASS |
| K5: AQUAL identity | 5.6e-16 — PASS |
| MUTATE ×0 | returns CFG687 and the "before" numbers exactly, on both footings — PASS |
| **MUTATE ×2** | **does not bite as frozen** (\|s(×2) − s(×0)\| = 0.0055 / 0.0012 < 0.01) |

- The ×2 response is exactly linear: 2.0× the ×1 shift on both footings. So the frozen "term too small" clause applies, not a
  blind pipeline.
- The post-hoc planted term shows the pipeline responds to a term that grows with mass.

## Disclosures

- **The primary edge is large.** X1 uses (1 + f★) M_gas(< 3 Mpc), median 6.4e13 M☉, and edges of 2.1 / 1.9 Mpc (0.5–5.0). It
  removes most correlated neighbours inside the outer band by construction. X2 (median 1.2 Mpc), X3 and E0 bracket that
  choice, and none moves the slope.
- **Double counting.** CFG687's law term is the no-edge law (phantom to 30 Mpc, CFG903's reference B). Adding a two-halo term to
  it is NA-5's specification and an upper-side choice.
- **The bright sample is flux limited.**
  - m_lim rises with z, and nothing is brighter than r ≈ 15.3 (CFG903 A1).
  - So members and neighbours of the heavy, higher-z clusters are less complete. C1′ and C2′ bracket this.
  - The structural point holds regardless: the light tercile needs negative mass.
- **Not modelled:** neighbour true-z lensing efficiency; photo-z mass errors; catchment sharing (an upper bound); mass not
  attached to catalogued galaxies.
- The census f_ret is a carried observational input. d uses CFG687's BAO-raw D_A; the χ window uses CFG903's χ.
- **Compute:** single thread, nice 10, one process at a time.
  - Stage A: 30 s, peak 834 MB (watchdog at 0.95 GB).
  - Score: 2 s, < 100 MB.
  - Post hoc: about 3 s.

## Files and rerun (from this directory)

- `FROZEN_CRITERIA.md` and `AMENDMENT_A1.md`.
- `cfg967_pairs.py` → `cfg967_pairs.out`, `cfg967_pairs.json`, `cfg967_tables.npz` (per-cluster two-halo vectors: lens and
  random means, edges, completeness).
  - The run-1 files are kept as `*_run1_K3b_fail.*`.
- `cfg967_score.py` → `cfg967_score.out`, `cfg967_results.json`.
  - With `CFG967_MUTATE=1` it writes `cfg967_score_MUTATE.out` and `cfg967_results_MUTATE.json`.
- `cfg967_posthoc.py` → `cfg967_posthoc.out`, `cfg967_posthoc.json`.
- Commands: `OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg967_pairs.py`, then `... cfg967_score.py`, then
  `CFG967_MUTATE=1 ... cfg967_score.py`, then `... cfg967_posthoc.py`.
- Reads CFG903's work arrays in `../../../_external_data/cfg903_work/` (not committed) and the KiDS bright-sample FITS.

κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw KiDS data, framework-native neighbours (no ΛCDM halo-model term); not theory closed. Nothing here says the data favour the framework.
