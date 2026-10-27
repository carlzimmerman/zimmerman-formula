# GC2_turnaround_baryon_budget: FROZEN CRITERIA (committed alone, before any script or number)

**Synthesis behind this lane.** The record's negative results point at one place:

1. Every tested core rule leaves G-OUT-M3 UNDER, the outer band of the most gas-rich clusters:
   - X43 c_f = 4: +2.41;
   - c_f = 5: the only failing line;
   - X38: +5.4;
   - IB1 with the hydrostatic gas mass as the total: +5.02.
2. The measured outer ratio rises steadily with mass: X7 quintiles 0.65 → 1.37.
3. GC1 finds that correlated structure beyond turnaround adds almost nothing at 1.4–3 Mpc, because it projects flat. The
   missing lensing mass therefore lies **inside** turnaround.
4. IB1 reads the data as "outskirts follow the baryon mass".

**The concrete candidate.** The X2 → X30 `gas()` profile is **cut at 3 Mpc**, so Mbt = M_b(< 3 Mpc), and the whole cold
dark energy halo normalisation (Mfair = (Ω_c/Ω_b) Mbt, together with r_ta) is set by baryons inside 3 Mpc only. The
model *defines* the halo as the fair share of the turnaround region, which is about 7 Mpc for massive clusters. The cut
therefore under-counts the turnaround baryon budget, and the shortfall grows with cluster mass:

- massive clusters (2.2 R500 ≈ 2.9 Mpc) lose their whole r⁻³ tail;
- small clusters (r_ta ≈ 3–4 Mpc) lose little.

**The fix has no new parameter.** It is the record's own "P" gas profile (β-model, r⁻³ beyond 2.2 R500, CFG814),
counted to the model's own r_ta. That is a fixed point, because r_ta depends on M_b.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Model change (frozen)

**The change.** In X30's `prep`, the gas mass profile is recomputed without the 3 Mpc cut, using the same β-model and
the same r⁻³ continuation beyond 2.2 R500, up to the grid edge (30 Mpc). Then:

- M_b,ext(r) = 1.2 M_gas,ext(r), with the same star factor as X30;
- r_ta solves r_ta = r_ta_com(M_b,ext(r_ta))/(1 + z), found by fixed-point iteration from X30's value, to 1e-6
  relative;
- Mbt = M_b,ext(r_ta);
- Mfair = (Ω_c/Ω_b) Mbt;
- the baryon lensing profile is M_b,ext(min(r, r_ta)).

**Background.** Native (owner rule 10-25), applied as in GC1 (d1da6b8185): Ω_c/Ω_b = 5.2715 with h 0.6856427,
Ω_m 0.2976016 and ω_b 0.0223081, in `r_ta_com` and Mfair. The inherited configuration is reported only.

**Unchanged:** everything else in X43, including the core rule, the 15 keys, the C* reference, groups and SPARC. Groups
and SPARC do not use X30's `prep`, so they are unchanged by construction.

## 2. Rules and configurations

- **Rules:** R4 (X43, c_f = 4), R5 (c_f = 5) and RX48 (X48 ng48 3-seed table), as in GC1.
- **Configurations:** {inherited, native} × {cut at 3 Mpc, extended to r_ta}.
- **Graded configuration:** native + extended.
- **Variant V-R5shape:** the r⁻³ continuation starts at R500 instead of 2.2 R500 (X2's "R5" shape), which tests
  sensitivity to the extrapolation.

## 3. Step 0 (stop rule)

- **S0a.** Inherited + cut + R4 reproduces X43 to 3 decimals: G-OUT-M3 pred 1.120 / 1.108, groups Z +2.05,
  SPARC 0.0782.
- **S0b.** The fixed point converges for every cluster in under 50 iterations. The per-cluster ratio
  Mbt,ext / Mbt,cut is reported: median, the median per Mgas500 tercile, minimum and maximum.

## 4. Verdict (per footing)

- **TURNAROUND BUDGET REPAIRS M3.** On R4 native + extended, |Z(G-OUT-M3)| ≤ 2 in both h cells, and no cluster key that
  passed on R4 native + cut newly fails.
- **REPAIRS M3 BUT BREAKS.** M3 passes but at least one other key newly fails. The keys are named.
- **NOT REPAIRED.** M3 still fails.
- **Per rule (R4, R5, RX48; native + extended):** whether the rule passes **every** X43 line, meaning SPARC on both
  backgrounds, groups, and all 15 keys in both h cells. A rule that does is reported as "PASSES THE X43 LINE SET". That
  statement is scoped to these lines only: KiDS lensing (X53) and dwarfs (X51) are not regraded here.
- **Robustness.** ROBUST if V-R5shape gives the same R4 class; otherwise FRAGILE.

## 5. Checks and twin

- **K1.** The extended Mbt is ≥ the cut Mbt for every cluster.
- **K2.** The ratio rises with Mgas500. The median of the top tercile is above the median of the bottom tercile. This is
  the predicted direction; a failure is reported, not hidden.
- **K3.** Peak RSS < 1 GB, one thread.
- **MUTATE (`GC2_MUTATE=1`, separate outputs).**
  - m1: the extension is replaced by a cut at 2 Mpc, an anti-extension.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and K1.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gc2_budget.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.
