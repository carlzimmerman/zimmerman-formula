# CFG929: four small reframings of the cluster-core excess. None resolves it (a NO EFFECT, b NO EFFECT, c NO EFFECT, d BREAKS SOMETHING)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in f91c25f33 before any script or number. Block CFG920–929 (LEDGER row 663).
- **Label:** HYPOTHESIS TEST. Four reframings, each with zero new constants.
- **Settings:**
  - κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 are kept apart.
  - ν_s (g_N = g²/(g + a0)) decides; ν_mono is the bracket.
  - Raw data and framework-native models only.
  - The extra mass is cold energy, not a particle.
  - Not "theory closed". Nothing here says the data favour the framework.
- **Target:**
  - eRASS1 318 MID excess (ν_s) 1.9068 ± 0.1184 / 1.7510 ± 0.1087, with OUTER 1.0109 ± 0.0868 / 0.9258 ± 0.0795. This is the plain law on CFG687/916 baryons (gas × 1.2).
  - ACCEPT 8 is reported with no class weight. Its own MID excess is below 2σ, so its "RESOLVES" rows mean nothing.

## Bottom line

| reframing | canonical | alt | largest MID removal with OUTER and SPARC kept | in one line |
|---|---|---|---|---|
| **(a)** every declared ν | **NO EFFECT** | **NO EFFECT** | 19.9% / 8.8% (ν_β at the record's SPARC β) | BRACKET-DEPENDENT. The ν_β lower 95% edge removes 40% / 27% but BREAKS OUTER (Z −2.09 / −2.24) and SPARC (rms 0.140 / 0.126 in the Υ window) |
| **(b)** superposition (QUMOND clumpiness) | **NO EFFECT** | **NO EFFECT** | −0.3% (clumpiness *lowers* the lensing mass) | Exact first-order cancellation. Even the algebraic own-halo bracket (Σ ν(g_i) g_i) removes only 13% / 15% |
| **(c)** line-of-sight structure | **NO EFFECT** | **NO EFFECT** | 13.6% / 14.9% (a generous bound) | X-ray neighbours remove 0.5% and lower OUTER more than MID. Measured member stars are below the model's own stars |
| **(d)** CFG640 / M2 cooling + condensed source | **BREAKS SOMETHING** | **BREAKS SOMETHING** | none (the excess grows) | Nothing cools at t_cool = t_dyn. The settled-only M2 reading drops the hot-gas phantom: MID 3.53 / 3.31, OUTER 2.00 / 1.86 |

The cluster-core excess stays open. No small reframing of the law, of its superposition, of projection, or of the record's own
condensation module removes even a quarter of it while keeping OUTER and SPARC.

## (a) Interpolation-function family (eRASS1, each kernel replaces ν_s; `cfg929_part_a.out`)

| kernel | A_MID canonical | A_OUTER (Z) | f_rem | SPARC rms in Υ 0.50–0.80 | class | A_MID alt | f_rem | class |
|---|---|---|---|---|---|---|---|---|
| ν_s (reference) | 1.9068 | 1.011 (+0.13) | 0 | 0.1009 | — | 1.7510 | 0 | — |
| ν_e = ν_RAR | 1.9102 | 1.012 (+0.14) | −0.004 | 0.0999 | NO EFFECT | 1.7536 | −0.003 | NO EFFECT |
| ν_mono | 1.9102 | 1.012 (+0.14) | −0.004 | 0.1003 | NO EFFECT | 1.7536 | −0.003 | NO EFFECT |
| P2 = √(1 + 1/y) | 2.0684 | 1.077 (+0.83) | −0.178 | 0.1083 | NO EFFECT | 1.8888 | −0.184 | NO EFFECT |
| ν_2 standard | 2.0915 | 1.083 (+0.89) | −0.204 | **0.1115** (> 0.110) | **BREAKS** (SPARC) | 1.9064 | −0.207 | NO EFFECT |
| **ν_β, best β 0.4847 / 0.5533** | **1.7268** | 0.936 (−0.80) | **+0.199** | 0.1068 (Υ 0.50, edge; best 0.1011 @ 0.44) | **NO EFFECT** | **1.6846** | +0.088 | NO EFFECT |
| ν_β lower edge 0.3974 / 0.4537 | 1.5430 | **0.848 (−2.09)** | +0.401 | **0.1396** | **BREAKS** (OUTER, SPARC) | 1.5462 | +0.273 | BREAKS (OUTER −2.24, SPARC 0.126) |
| ν_β upper edge 0.5912 / 0.7705 | 1.8702 | 1.000 (0.00) | +0.040 | 0.1021 | NO EFFECT | 1.8320 | −0.108 | NO EFFECT |

- **What moves the clusters.** In the deep regime every declared ν shares y^−½ and differs only in the offset term.
  - ν_s and ν_e carry +½.
  - P2 and ν_2 carry ~0, so they *raise* the excess by 18–21%.
  - Only ν_β(β < ½) carries a growing offset, y^(β−½)/2β.
- **ν_β at the record's SPARC-best β.** It removes 20% (canonical) and 9% (alt), below the 25% PARTIAL line.
  - It needs Υ_disk below the H2 window: its SPARC optimum is Υ 0.44 / 0.46, and inside the window it sits at the 0.50 edge.
- **The ν_β lower band edge.** Removing 40% / 27% takes OUTER below −2σ, and SPARC can then fit only at Υ 0.36 / 0.38, so the
  window rms fails.
  - **The same offset that would fill MID overshoots OUTER.** That is the shape problem in another form: the excess is
    concentrated, a kernel change is not.
- **Disclosures:**
  - ν_e and ν_mono agree to 4 decimals here: ν_mono is ν_RAR below its large-y splice, and cluster accelerations never reach it.
  - Candidates: five alternatives at their primary settings plus two β edges per footing; ν_s is the reference. The criteria's
    "seven chances" counted loosely, and no rule depends on the count.
  - CFG468's stored SPARC Δχ² classes are reported with no class weight:
    - ν_s fails T-free and passes T-fix;
    - ν_2 and P2 fail;
    - ν_RAR passes.

## (b) Superposition / clumpiness (`cfg929_part_b.out`)

**The theorem (frozen before any number).** In the record's settled QUMOND field, the cluster-centred flux to first order in a
member's field is [ν + gν′](g_s) × m_enc. That is exactly the smooth model's response. Clumpiness enters only at second order and in
the members' nonlinear near zones, and the deep-regime second-order coefficients are negative.

| member set (clumps) | ΔM_L/M_L at 0.81 Mpc (median) | A_MID canonical / alt | f_rem | class |
|---|---|---|---|---|
| **A1 census central** (10,103; median 3.0e10 M☉) | **−2.2e-4** | 1.9093 / 1.7532 | −0.003 / −0.003 | **NO EFFECT** |
| A1 census upper, α = −1.5 (48,759) | −5.3e-4 | 1.9099 / 1.7538 | −0.003 / −0.004 | NO EFFECT |
| MAX: all baseline stars (0.20 × gas) in 10¹¹ M☉ clumps (41,054) | −3.8e-3 | 1.9170 / 1.7604 | −0.011 / −0.013 | NO EFFECT |
| ν_mono, census central | −2.2e-4 | 1.9126 / 1.7558 | −0.003 / −0.003 | NO EFFECT |
| **b-ALG bracket** (each member keeps its own halo, Σ ν(g_i) g_i), baseline stars | — | 1.7892 / 1.6419 (OUTER 0.951 / 0.871) | +0.130 / +0.145 | NO EFFECT |
| b-ALG, A1 census central / upper | — | 2.0328 / 1.8651; 1.9482 / 1.7876 | +0.026 / +0.028; +0.057 / +0.063 | NO EFFECT |

- **The full nonlinear field makes clumpy members lens slightly *less* than smooth ones.** A single 10^12.5 M☉ clump at 0.8 Mpc
  carries q = −0.18 f′m at its own radius (MUTATE Mb3).
- **Overlap:** nonlinear zones overlap for 1.1% (census) to 5.5% (MAX) of clumps, so the single-clump sum is safe.
- **The algebraic bracket matches the frozen hand estimate:** ΔM_L/M_L ≈ ½ f_mem.
  - Even with all of the baseline's 0.20 × gas stars as separate halos, it removes 13–15%.
  - With the measured census it removes 3–6%.
  - Its halos end at the equality radius (median 38 / 68 kpc for 10^10.5 / 10^11 M☉ at 0.81 Mpc), far inside CFG726's supply
    edges (175–886 kpc), so no outer memory comes back.
- **SPARC:** unchanged by construction.

## (c) Line-of-sight structure (`cfg929_part_c.out`)

- **Shell theorem (frozen).** In a stacked profile, mass outside 3D radius R gives ΔΣ(R) ≤ 0, Newtonian and under the law. MUTATE Mc1
  confirms it on every cluster: a planted copy at 2 Mpc gives ΔΣ ≤ 0 in all bins inside it.
- **c-X, eRASS1 X-ray neighbours.**
  - Inside 5 Mpc and |Δz| ≤ 0.05(1 + z), there are 0.25 neighbours per target; 56 of 318 targets have any.
  - MID 1.9023 / 1.7468 (f_rem +0.005 / +0.006); OUTER drops 1.011 → 0.968 and 0.926 → 0.887.
  - Neighbours add to OUTER, not MID. **NO EFFECT.**
- **c-G, KiDS member stars inside the MID apertures** (A1 upper census).
  - The measured S_up is a median 0.48 / 0.45 / 0.41 / 0.37 × the model's own 0.20 × gas_cyl stars inside 0.5 / 0.556 / 0.808 /
    1.175 Mpc. The baseline already holds more stellar mass than is seen.
  - Only 95 of 318 clusters show any stellar excess over the model (median 0, 84th percentile 3.5e11 M☉), against the
    2.4e13 M☉ needed.
  - The bound treats ×6 of that excess as a central concentrated mass: MID 1.7875 / 1.6425 (f_rem +0.132 / +0.145).
- **Primary, c-X + c-G (×6) together:** MID 1.7835 / 1.6388, OUTER 0.945 / 0.866, f_rem **+0.136 / +0.149**. **NO EFFECT**, robust as
  a bound.
  - ν_mono gives the same class.
- **Shape bound (reported, no class weight).**
  - The c-X template cannot remove more than 4% / 2% before OUTER reaches −2σ.
  - A central concentrated term could remove up to 72% / 44% before OUTER breaks, but only at ×7.9 / ×3.5 the generous bound. On
    disk there is no such mass (CFG922).

## (d) The record's CFG640 / M2 cooling + condensed-source module (`cfg929_part_d.out`)

The inputs are the record's own: Λ(T), μ, n_e/n_H, t_dyn = r/V, and T from V⁴ = G M a0. They are applied to the measured
β-model gas.

| t_ref | kT median | clusters cooling | r_cool median (max) | M_cool median (max) | cooled cylinder mass / needed λ·gas_cyl |
|---|---|---|---|---|---|
| **r/V (CFG640 K2, as frozen)** | 2.79 / 3.06 keV | **0 / 318** | 0 kpc | 0 | 0 |
| 1/H (CFG640's age bracket) | 2.79 / 3.06 keV | 291 / 281 of 318 | 84 / 76 kpc (160 / 150) | 2.0e11 / 1.5e11 (3.0e12 / 2.5e12) M☉ | 0.9% / 0.8% (max 2.8% / 2.9%) |

- **The rule predicts no core concentration of the right size.**
  - At the frozen t_dyn nothing cools.
  - At the age bracket, the condensed gas is under 3% of the needed concentrated mass in every cluster.
  - This agrees with CFG640's design table: f_c − 0.10 ≤ 5.9e-4.
- **d-M2, primary: BREAKS SOMETHING.**
  - Under theory-v2's source rule, the settled cold energy is the law phantom of condensed baryons only (stars 0.20 × gas +
    cooled gas).
  - Hot gas then sources no phantom: MID 3.53 / 3.31, OUTER **2.00 / 1.86 (Z +5.8 / +5.4)**.
  - Age bracket: MID 3.40 / 3.21, OUTER 1.97 / 1.84.
  - With A1 census stars: MID 6.1 / 5.8.
  - **Frozen monotonicity:** for any amount of cooling the settled part is ≤ the plain law at every r, because condensed ⊂ all and
    h′ ≥ 0. Verified: χ = 1 reproduces the plain law to 2e-14.
- **d-plain:** under the all-baryon source, cooling only relabels phase, so A is identical (|ΔA| = 0).
- **The reservoir reading is CFG727's (tested; not re-run, no class here).**
  - Stored eRASS1 values: MID 0.925 / 1.077, OUTER 1.054 / 1.137.
  - It passes overall only through a cancellation across gas terciles, and fails on ACCEPT (×2) and KiDS early − late (CFG727).
  - The cooling rule would raise CFG727's condensed mass by at most the age-bracket M_cool (≲ 1% of gas), and so lower its free
    reservoir. That cannot repair CFG727's mass trend: its light and middle terciles are already short.

## Controls
- **K 7/7 PASS** (`cfg929_K.out`):
  - **K1, CFG687 ν_mono:** MID 1.9102 ± 0.1186 / 1.7536 ± 0.1089, OUTER 1.0118 / 0.9265; |dA| 4e-16.
  - **K2, CFG916 LR-c ν_s:** eRASS1 and ACCEPT MID and OUTER; |dA| 4e-15; dsig_ML identity 0.
  - **K3, CFG922 A1:** census_central 2.0600 / 1.8903; the stored λ gives A_MID = 1 to 5e-9.
  - **K4, CFG4 SPARC:** P2, ν_mono and ν_β best exactly, |d| = 0.
  - **K5, cooling code vs the record's `chi_cool`:** 80 cells, max rel 6.5e-16.
  - **K6, kernels vs CFG468:** to 0.0004.
  - **K7, census code vs stored A1 values at 0.5 Mpc:** exact.
- **MUTATE** (`cfg929_MUTATE.out`):
  - **Ma** BITES: a0 × 10 moves every kernel by ≥ 10.3σ; a0 → 0 gives 10.1737, equal to the stored value.
  - **Mb1** HOLDS: 0.
  - **Mb2** BITES: in the smooth limit |ΔM_L| falls ×286.
  - **Mb3** BITES: the tiny-clump linear cancellation holds to 3e-5, and the heavy clump gives −0.18 f′m.
  - **Mc1** BITES: the shell sign holds in every bin.
  - **Mc2** HOLDS: random positions give 2.4e9 ± 3.3e9 and 5.6e9 ± 9.5e9 M☉.
  - **Md as frozen: FAILED on one leg.**
    - The χ = 1 leg holds (2.1e-14).
    - "r_cool forced to 3 Mpc" gives 2.6e-4. The cause: CFG687's gas is cumulated by trapezoid, so half a grid step of gas lies just
      beyond the 3 Mpc cut, and a cooling radius of exactly 3.0 Mpc leaves it uncooled.
    - This is a mis-specified control, not an M2 fault, but the frozen failure stands.
  - **Md-b (post hoc):** r_cool at the first node beyond 3 Mpc (3.00878 Mpc) gives 2.1e-14, so it HOLDS. No main number uses a cooling
    radius near 3 Mpc (the largest is 0.28 Mpc).

## Post-hoc items and disclosures (all dated 2026-10-20; none moves a class)
1. **Md-b added** after the frozen Md leg failed (above). The frozen failure stands.
2. **Implementation changes after the criteria; no number moved.**
   - MAIN now runs as four fresh processes (`CFG929_PART=a|b|c|d`), then `assemble`.
   - The KiDS catalogue is read first and freed.
   - `alg_ML` is chunked over clusters.
   - The clump-overlap diagnostic uses a KD-tree.
   - A hard in-script memory guard stops the run at 0.95 GB.
   - The (b) numbers are identical to the first, aborted run's: every printed A agrees to 4 decimals.
   - The (a) overall string gained the BRACKET-DEPENDENT flag that the frozen rule requires (the JSON already carried
     `beta_bracket_dependent`).
3. **Machine-rule breach (disclosed).**
   - The first single-process MAIN run (15:48–16:00) reached **2.4 GB peak RSS**, against the < 1 GB rule. The cause was retained
     heap from an N × N clump-overlap array and repeated full-sample allocations. I stopped it.
   - The second attempt stopped itself through the new guard at 1.02 GB.
   - The final runs peaked at 0.35 / 0.65 / 0.62 / 0.84 GB (parts a–d), 0.94 GB (MUTATE) and 0.65 GB (K).
   - The live NC2x job had already been aborted by its own swap guard at 15:42:00: swap grew 10.6 GB in 20 s, coinciding with a 33 GB
     local LLM server process that started at about 15:41:48. This lane's K stage had ended at 15:41:44 with a 0.62 GB peak, and
     every over-limit run here started after the abort. NC2x was not touched.
4. **Not blind.** The stored numbers listed in criteria §0 were seen before freezing. Every hand estimate frozen there came true in
   direction and size:
   - (a) ~15–20% for ν_β;
   - (b) negative and tiny, with the algebraic bracket ≈ 8% in M_L;
   - (c) small;
   - (d) BREAKS.

## What is and is not established
- **Established, on the record's own data and code:**
  - No interpolation function declared in the record removes ≥ 25% of the MID excess while keeping OUTER and SPARC.
  - In the record's QUMOND field, member clumpiness cannot raise the cluster-centred lensing mass at first order, and its
    second-order effect is negative.
  - Line-of-sight structure, measured (X-ray neighbours) or bounded (KiDS stars), removes ≤ 15%.
  - The CFG640 / M2 cooling rule condenses nothing at its frozen t_dyn, and its settled part can only raise the excess.
- **Not established:**
  - A ν outside the record's declared set. One would be a new constant, and it would still face the same MID-vs-OUTER shape problem
    the ν_β edge shows.
  - Gas-substructure clumping. It enters only at second order in δg/g ~ l/r and is not computed.
  - Non-stacked projection effects such as triaxial alignment with the line of sight. These average out of the stacked profile and
    are not bounded here.
  - The reservoir reading of theory-v2: that is CFG727's.
- κ is not derived. This is not "theory closed". Nothing here says the data favour the framework.

## Files and re-run (from this directory, one process at a time, OMP_NUM_THREADS=1, nice 10)
| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (f91c25f33) |
| `cfg929.py` | everything: K, MUTATE, the four parts and assemble |
| `cfg929_K.out`, `cfg929_K.json` | `CFG929_MODE=K python3 cfg929.py` |
| `cfg929_MUTATE.out`, `cfg929_results_MUTATE.json` | `CFG929_MUTATE=1 python3 cfg929.py` (~2.5 min) |
| `cfg929_part_{a,b,c,d}.out/.json` | `CFG929_PART=a python3 cfg929.py`, then b, c, d (b ≈ 11 min; others seconds) |
| `cfg929.out`, `cfg929_results.json` | `CFG929_PART=assemble python3 cfg929.py` |

- **Read-only inputs:**
  - lane files: exec'd slices of `cfg922.py`, `CFG4_galaxy_law.py` and the CFG640 engine source (cooling rule only, never run as an
    engine); stored results of CFG686, CFG687, CFG916, CFG922 (+ A1 census), CFG4, CFG640 split and CFG727;
  - external data: the eRASS1 main table, and the KiDS DR4 bright sample + LePhare read with a plain FITS parser.
- Nothing was downloaded. No other lane was edited.

κ = ½ fitted; footings never pooled; cold energy mass still required; not theory closed.
