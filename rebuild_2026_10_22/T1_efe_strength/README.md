# T1_efe_strength: how strong an external-field effect do the data want?

One diagnostic number, ε, multiplies the total host field that enters v3's AQUAL solve. ε = 1 is v3. ε = 0 is no
external-field effect (EFE). ε is a measuring stick, not a new theory. Every dataset is run through its own lane's
solver and inputs, read-only (S1, F2, P2, D10, C6, E2), on both footings. κ = ½ is FITTED. The footings are never
pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict

**By the frozen rule: FOOTING SPLIT, and FRAGILE on both footings.**
- Canonical: **DATA PREFER WEAK EFE**, ε̂ = 0.02, 95 % interval [0, 0.26].
- Alt: **NOT DECIDED**. ε = 1 is disfavoured at Δχ² 7.96, under the frozen line of 9.
- The primary set is {satellites, Coma UDGs, P2 lensing, globulars}, per AMENDMENT A1.

**What the numbers say:** one EFE strength does not fit these data under v3's other assumptions.
- **The conflict:** the Coma UDGs want ε ≤ 0.21 / 0.24. P2's spectroscopic lensing wants ε ≥ 0.67 / 0.81 (95 %).
  - Their 95 % intervals do not overlap.
  - One-ε consistency for the primary set: χ²_PG = 9.49 / 10.67 on 3 dof, p = 0.023 / 0.014. That is just above the
    frozen INCONSISTENT line (p < 0.01).
  - Coma + P2 alone give p = 0.013 / 0.006. Without the satellites, the set gives p = 0.009 / 0.005 (INCONSISTENT). The
    satellites add almost no weight, because they fail at every ε.
- **The weak-EFE consensus came from F2's leaky sample.** With F2 in place of P2 (the frozen primary C7), one weak ε fits
  everything: ε̂ = 0.16 / 0.17, 95 % [0, 0.22 / 0.23], p_PG = 0.16 / 0.18. With P2, it does not.

### Per dataset (canonical / alt)

| dataset | ε̂ | 95 % interval | Δχ² at ε = 1 | Δχ² at ε = 0 | fit at ε̂ |
|---|---|---|---|---|---|
| SAT: dwarf satellites (S1 tile 26) | 0 / 0.05 | [0, 0.23] / [0, 0.24] | 29.4 / 30.3 | 0 / 0.6 | **fails at every ε**: χ²_min 52 / 47 |
| COMA: 9 UDGs (S1 tile 29), dmean | 0 / 0 | [0, 0.21] / [0, 0.24] | 15.6 / 14.8 | 0 / 0 | fits: z_sys 1.65 / 1.45 at ε = 0 |
| LENS-P2: GAMA spec-isolated (primary lensing) | edge 1.5 / 1.5 | [0.67, 1.5] / [0.81, 1.5] | 2.0 / 2.7 | 6.2 / 7.6 | fits: p 0.10 / 0.06 |
| LENS-F2: KiDS photo-z isolated (C7, reported) | 0.16 / 0.17 | [0.11, 0.20] / [0.13, 0.22] | 274 / 266 | 6.9 / 10.6 | **fails at every ε**: χ²_min 154 / 117 on 59 dof |
| GC: outer globulars at the L★ floor | edge 1.5 / 1.5 | [0, 1.5] / [0, 1.5] | 0.59 / 0.54 | 3.37 / 3.13 | −2 ln L 3.71 / 3.75 at ε̂ (Newton 0.50) |
| SS: Cassini and planets (screened) | flat | all | 0 | 0 | Q₂/bound ≤ 5e-8 at any ε ≤ 1.5 |
| WB: wide binaries (screened) | flat | all | 0 | 0 | γ_v − 1 = 8.1e-6, set by L★ |

- P2's ε is measured in units of its catalogue field, which holds only the galaxies' baryons. That field is a lower
  bound on v3's field. On P2's whole scan, a zero field sits at Δχ² 8.95 / 11.29. The best field is x_e ≈ 0.032, which is
  ε ≈ 4 of the catalogue field. If all baryons traced the galaxies ("bary" reference), P2 needs ε ≥ 0.25 / 0.31. That
  still does not overlap Coma's interval: C9b gives p = 0.004 / 0.002.
- **In absolute field units there is no contradiction.** The Coma UDGs sit in x_e ≈ 0.85 / 0.70 and allow an acting field
  up to x_e ≈ 0.18 / 0.17. P2's lenses need x_e ≥ 0.0095 / 0.011. What fails is one universal multiplier on v3's expected
  field.

### Satellites: a weaker EFE does not rescue them

- At ε = 0 the satellites still sit **+0.91 / +0.89 dex** above v3 (7.2 / 6.9 sd). At the L★ floor, the EFE accounts for
  only +0.42 / +0.41 dex of the +1.33 / +1.30 gap. S1's +0.58 is the L★ = 0 step.
- Worst-clean data W sit at +0.61 / +0.59 dex even at ε = 0. E-V gives +0.88 / +0.85 dex.
- **Tracking.** The residual rises with the host field at every ε: slope +0.76 ± 0.26 dex per dex at ε = 0, and
  +1.10 ± 0.21 at ε = 1.
  - A too-strong EFE would give this sign. But the slope survives at ε = 0, and with log y₀ controlled it is still
    +0.78 ± 0.28 (A3, post-result).
  - So something else tracks the host field: tides, host-related extra mass, or non-equilibrium. A negative ε would be
    needed, and that is not physical in AQUAL.
- Host-mass bracket: if the hosts are E_lo or E_hi, the satellites' ε scale moves ×1.24 or ×0.68.

### Globulars: they need screening, not the EFE

- Re-floored at each ε, L★_95 runs from **21.69 / 22.85 pc at ε = 1** (D10 reproduced) to **28.42 / 29.25 pc at ε = 0**.
  The ε = 0 value matches E4's isolated 28.85 / 29.12 pc.
- At the fixed floor, ε = 0 costs Δχ² 3.37 / 3.13, below 3.84. Part of that cost is built in: the floor was set at ε = 1.

## What this means for theory (frozen wording, §5 + A1 §4)

- **Not "ε ≈ 1 consistent everywhere".** Coma excludes the full AQUAL EFE (Δχ² 15.6 / 14.8). The satellites prefer weak
  EFE too, but they fail at every ε.
- **Not cleanly "ε ≈ 0 preferred and tolerated elsewhere".** P2 rejects a zero field. The record's Chae amplitude also
  points to an EFE (0.76 ± 0.16 / 0.88 ± 0.15; standard-MOND machinery). The globulars at the floor lean the same way,
  weakly.
- **So the reading is "inconsistent": COMA vs LENS-P2, and COMA vs the Chae record.** Each side rests on a stated
  assumption:
  - Coma's on equilibrium in the present field and no extra bound mass;
  - P2's on its galaxies-only field, which is a lower bound on v3's field.
  If the dust traced the galaxies too (P2's "matter" bracket, which is ΛCDM-processed and flagged), P2's required ε
  would fall to ≈ 0.1 and the conflict would go away. That case is not tested here.
- **If the weak-EFE reading were right,** E2 shows the action gives AQUAL, and QUMOND changes EFE observables by only
  1.2–1.5× in Q₂ and 0.01 in γ_v. A weak EFE would therefore need a different action. ε → 0 re-opens the status board's
  no-go (tile 51, "law + a¹ growth + no EFE, local"; CFG946 L-G and CFG179: any local field that supplies the deep law
  has an EFE). Nothing here forces that step. This lane does not propose one.

## Why F2 and P2 differ (A1)

| | allowed or needed field (absolute x_e) | zero field |
|---|---|---|
| F2, photo-z isolated KiDS (S²-scaled) | x_e ≤ 0.0066 / 0.0062; best 0.0045 | disfavoured, Δχ² +6.9 / +10.6 unscaled |
| P2, spec-isolated GAMA, hole subtracted | x_e ≥ 0.0095 / 0.0106; best 0.032 | rejected, Δχ² 8.95 / 11.29 |

- On one x_e axis the two samples disagree: χ²_PG = 7.2 / 8.8 on 1 dof (p 0.007 / 0.003).
- F2's sample leaks hosts. Its F2 AMENDMENT A1 estimates about 38 % leakage, and its cleaner post-hoc veto (S_x300) already
  lost the tension. A leaked host adds outer lensing, so it penalises any EFE cut-off.
- P2 vetoes hosts spectroscopically and subtracts the isolation hole with matched randoms. P2 is therefore the primary.
- **Correction to this lane's brief.** "F2: environmental fields make v3's outer prediction 4.5–12× too high" has the sign
  flipped. F2's A_O2 = data/model = 4.45 (noclu) to 12.2 (maxclu). The EFE prediction is too *low*.
- **S2.** Inside 0.31 Mpc the field barely matters. F2's inner χ² moves only 71.9 → 69.7 up to x_e 0.02. S2's committed
  A_blue = 0.878 / 0.882 / 1.035 at y_e 0 / noclu / maxclu.

## Record EFE claims (classes, criteria §6)

| claim | class | why |
|---|---|---|
| (a) Chae SPARC (CFG8, CFG179 M5): A = 0.76 ± 0.16 / 0.88 ± 0.15 | **CONTRADICTED BY THIS LANE** (mechanical: no overlap with the primary [0, 0.26] / [0, 0.30]); **NOT A DETECTION** | The tracking slope 0.71 ± 0.80 is non-diagnostic. It conflicts with Coma (C6: p 0.001), agrees with P2 and the globulars, and uses standard-MOND machinery. |
| (b) Directional EFE: n = 16 Â +2.95 ± 3.13; WALLABY −1.70 ± 2.98 | **NOT DIAGNOSTIC** | Combined +0.51 ± 2.16 in units of the AQUAL floor (ε = Â/k, k 1–5). |
| (c) Wide binaries: CFG447 ("law with no EFE excluded") | **OTHER READING** | Unscreened law; uses the non-scoring DR3 dry run. |
| (c) CFG825 DR3 R = 0.973 ± 0.178 | **NOT DIAGNOSTIC** for v3 | Screened γ_v − 1 ≈ 8e-6 at any ε. The unscreened law-first contrast (not v3): γ_pm 1.53 / 1.59 at ε = 0 sits 3.2 / 3.5σ above R, so the unscreened law needs ε ≥ 0.5 / 0.75. |
| (d) CFG478 (QUMOND force-with-EFE vs satellite lensing) | **OTHER READING** | Ownership-era model. |
| (e) S1 "+0.58 dex EFE cost" | **CORRECT, but the L★ = 0 step** | At v3's floor the step is +0.42 / +0.41 dex. |

## Checks: 10/11 PASS (exit 1)

- **K1:** SAT reproduces S1 exactly at ε = 1 and ε = 0 (0.0 dex).
- **K2:** COMA reproduces S1 at ε = 1, 0.5 and 0.
- **K3:** LENS-F2 reproduces F2's χ² at five fields (Δχ² 0.000).
- **K3b FAILS (frozen, A1).** Its GLS clause was mis-specified by this lane, because P2's amplitude is diagonal-weighted
  (A2). K3c (A2) reproduces P2's own estimator to 1e-6, with σ within 1 %.
- **K4:** D10's σ tables to 1.3e-7, and the floor 21.69 / 22.85 pc.
- **K5:** ε → 0 continuity, 3e-9.
- **K6:** screened Q₂/bound 5e-8.
- **K7:** γ_pm(1) = 1.173 / 1.207 against E2's 1.167 / 1.199.
- **K8:** the D10 solver to 1.0e-10. The F2 solver's last change is 3.1e-4 (A1 line < 1e-3).
- **K9:** peak RSS ≤ 0.51 GB in every process.

`--mutate` hands every solver ε·y_e (the Newtonian field) instead of ε·x_e. It breaks K1 (0.31 dex), K2, K3 (Δχ² 642),
K4 (σ tables 0.80; floor 27.6 / 28.4 pc), K7 and K8: 4/11, exit 1 (`*_MUTATE.*`).

## What this does not show

- No new data and no new solves of P2 (its scan is read). P2's ε reference is the galaxies-only field.
- The ε range is [0, 1.5]. P2's best field lies beyond it in catalogue units; it is shown in absolute x_e.
- The satellites and UDGs are uniform-field Plummer spheres in equilibrium. Tides are not modelled, and the extra bound
  mass v3 may need is not included. The satellites' ε information is therefore conditional, and they fail at every ε.
- The globulars' ε information exists only at fixed L★.
- Chae's amplitude and the directional Â are read from the record, not recomputed with v3's AQUAL.

## Files and run

- Criteria and ledger: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (0fbdb17c87, committed alone first).
- Amendments: `AMENDMENT_A1.md` (pre-result, P2; 3d0f37f40f), `AMENDMENT_A2.md` (post-hoc K3c; fb48dca3f2),
  `AMENDMENT_A3.md` (post-result, reported only).
- Outputs: `t1_efe_strength.py`, `.out`, `_results.json`, `t1_stage_{satcoma,lens,gc,wb}.json`, `*_MUTATE.*`.
- Runtime: satcoma 1060 s, lens 236 s, gc 561 s, wb 17 s. Single thread, nice 15, no downloads.

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/T1_efe_strength/t1_efe_strength.py            # ~31 min, exit 1 (K3b)
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/T1_efe_strength/t1_efe_strength.py --mutate   # check cells only
```
