# CFG945: the satellite hover (F2) in the collapse-gated tether

**Lane label: CONDITIONAL.**
- The collapse gate (CFG941 R3θ) does not change the hover. A settled or freely translating satellite medium has θ = 0, so its gate
  is on. Its tethered medium feels no host force while its stars feel g_host: **Δa/g_host = 1.017–1.107** (CFG941 reproduced exactly).
- **Theorem S:** at leading order, every label-free tether gives this hover.
- Only a **per-label (domain-local) tether, H1**, removes it. It does so at the cost of a non-variational label sector whose seeding
  rule is open: **RESOLVED-WITH-COST**. In effect this is class A's "one tether per catchment", written as fields.
- Anchoring the tether to baryons (H2), restoring the equivalence principle (H3) and dispersion support (H4) are each
  **NOT RESOLVABLE**.

**Settings.**
- **Criteria:** `FROZEN_CRITERIA.md` (618b2fc8b, committed alone first). `AMENDMENT_A1_post_hoc.md` (8943d188e, POST HOC, before any
  main-stage number). Block 940–949.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native only.
- Not "theory closed". Nothing here says the data favour the framework.

## What the data allow (from the record's own numbers)
**Bound on the differential.**
- A differential acceleration ε g_host strips a dwarf's stars from its medium once it exceeds the dwarf's internal field
  g_int = 3σ²/r₁₂. A stripped dwarf's prediction falls to Newtonian.
- CFG874's statistic was reproduced exactly and recomputed against those predictions. It stays within 2 se of "satellites = field"
  only for **ε ≤ ε_B = 0.344 (canonical) / 0.317 (alt)**.
- Doubling the restoring field (κ_r = 2) gives 0.69 / 0.63.
- Under the hover, 19 satellites are stripped and c reads **−0.355 ± 0.114 (−3.1 se)**; with κ_r = 2 it reads −0.230 ± 0.112 (−2.05 se).
- ε_B is set by the six most host-exposed satellites: Sagittarius, And XVII, And XXV, Hydrus I, Boötes II and And I.

**Bound on the EFE.**
- CFG874's 2σ room for a satellite-specific deficit is **δ_c = 0.082 dex**.
- CFG873 (+0.043), CFG860 (+0.094 / +0.122) and CFG875 (+0.109 dex per dex) give bounds of the same size.

**Which the hover breaks.** The gated theory's static satellite phantom is cut by **0.10–0.73 dex**, which breaks δ_c.

**A property of the statistic (A1).** c sees only satellite-specific stripping. Stripping every dwarf is absorbed by its matched-g_bar
regression.

## Candidates and outcomes

| | action change (new constants) | (a) static law | (b) free fall ε | (c) EFE | (d) well-posed | class |
|---|---|---|---|---|---|---|
| P0 = R3θ (reference) | none (0) | PASS 2.2e-16 | FAIL 1.02–1.11 | FAIL 0.10–0.73 dex | PASS (ghost inherited) | — |
| **H1** per-label tether | Σ_q W(\|Dχ_q\|) + λ_q(D²χ_q − Kmn_q), label Q, L2 tidal re-latch (0) | PASS (single-label galaxy) | **PASS 1.6e-5 – 2.0e-3** (tides only) | **PASS 0** (tidal term ≤ 0.052 dex, reported) | PASS (two labels: bounded Jeans; conservation between label changes) | **RESOLVED-WITH-COST** |
| H2 baryon anchor | +mnψ, ∇ψ = law field of baryons (0) | FAIL (H2v: reaction on baryons, a₀/2 deep; dev 2.62 / 2.88) | FAIL (H2g: 0.48–1.00) | FAIL (H2g: 0.10–0.73 dex) | FAIL (H2n: no action, ∂T ≠ 0) | **NOT RESOLVABLE** |
| H3 EP restoration | none possible (0) | PASS | FAIL (hover real; dynamic corrections ≤ 2.4e-2) | FAIL | PASS | **NOT RESOLVABLE** |
| H4 dispersion support | tether share f_T (1) | PASS only at f_T = 1 | FAIL (needs f_T ≤ 0.31 / 0.29) | FAIL | n/a | **NOT RESOLVABLE** |

**H1's costs and open condition.**
- The label sector has no action: the L2 re-latch is local but non-smooth.
- Seeding labels at collapse: no local rule found.
- A continuum of auxiliary (χ_q, λ_q).
- Per-label single stream.
- Energy-momentum conserved only between label changes.
- **Every settled galaxy must be single-label.**
  - Two equal labels give an acceleration floor g → a₀ and miss NGC 3198 by 4.12 / 4.61.
  - Debris left by a failed re-latch misses it by about 2.6q, so q ≲ 3.5e-7 is needed.
- Rule L1 (field dominance) would hand 10/18 satellites to their host and restore the hover, so L2 is required.

**(e) Self-gravity.**
- H1 restores Newtonian gravity between different collapsed objects (different labels). Within one label, D-T still cancels it.
- H2 restores full self-gravity but fails (a), and its law state is Jeans-unstable (e-fold 280 / 267 Myr at NGC 3198's edge).
- H4's warm option would restore everything, but that is a different theory (CFG941 open item 2; how class A's particles are
  supported).

## Other findings
- **Theorem S (same point).** The host's own medium is in equilibrium under the tether force at each point. So any stationary,
  label-free medium element at that point, a satellite's included, feels zero host force at leading order.
  - The cross terms are model-specific. P0's push ε above 1; QUMOND-type anchoring pulls it below 1 (H2g 0.48–1.00).
  - Escapes: a label, support specific to the stream, O(1) velocity dependence, or a non-stationary medium.
  - A velocity-gated tether and a filtered tether both still hover.
- **Gate crossing.** A satellite medium abandoned by its stars reaches θ = θ_s within **1.4–13.5 Myr**. It then enters R3θ's ghost
  band, so the gated theory's satellite transient is undefined until CFG944 cures the ghost.
- **Correction to CFG941's separation estimate.** CFG941 counted only the stars' pull on the medium. With the medium's pull on the
  (extended) stars included, H3 at 250 kpc stays bound (2/18 cases); the rest separate in 9.5–114 Myr.
  - In every case the composite falls at (1 − f_m ε) of g_host: an EP violation **η = 0.76–1.04**.
- **H3.** No gradient-shift symmetry is compatible with the law (W′ ≠ 0). The medium's passive gravitational mass in a settled host's
  field is 0. The hover is dynamic, not an artefact of static equilibrium.

## Controls
- **K: 6/6 pass.**
  - CFG938's NGC 3198 law: 2.2e-16.
  - CFG941's 18 hover ratios and 18 EFE factors: exact.
  - CFG941 M4: 3.5e-16.
  - CFG874's c, se_c: exact.
  - The gate and θ (sympy).
- **MUTATE: exit 3 (A1).**
  - M1: labels removed, the hover returns.
  - M2: tether off gives universal free fall.
  - M3: the H2 reaction is the failing term.
  - M4: two labels break the law.
  - M6: tether off, the stars and medium co-move.
  - Frozen M5 is toothless (flagged); A1's M5b bites at −10.7 / −11.1 se.

## Files and commands (one core, nice 10, ≤ 0.29 GB, 1–10 s each, memory guard, nothing downloaded, no other lane edited)
- `CFG945_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg945.py` → `cfg945_K.out`, `cfg945_results_K.json` (exit 0).
- `CFG945_MUTATE=1 …` → `cfg945_MUTATE.out`, `cfg945_results_MUTATE.json` (exit 3 by the A1 rule).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg945.py` → `cfg945.out`, `cfg945_results.json` (exit 0; all checks pass).
- Kept for disclosure:
  - `cfg945_MUTATE_firstrun_M5toothless.*` (first MUTATE);
  - `cfg945_main_attempt1_killed_pointstars.out` (killed first main attempt).
- `DERIVATION.md` has the equations, every number and the disclosures.

## Disclosures (full list in DERIVATION §9)
- **K4 first run.** It failed at 1e-9 because CFG874 hard-codes rounded footings (`CFG4_common.A0` is 2.65e-6 / 3.13e-6 higher). The
  replica uses CFG874's literals. Fixed before any main number.
- **A1 (post hoc).** M5 was toothless; M5b and exit 3 were added. ε_B is unchanged.
- **First main attempt.**
  - I killed it, blaming the point-star dynamics, and switched to an extended star cloud.
  - The real stall was a sympy series, now replaced by its exact equivalent (W″(0)).
  - That attempt had printed a point-star Q3 table: 8/18 bound, against 2/18 now. Nothing else changed.
- **Wording.** One wording-only fix narrowed Theorem S's printed scope to leading order. All stages were rerun; no number changed.
