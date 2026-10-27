# GC1_group_cluster_core_rule: FROZEN CRITERIA (committed alone, before any script or number)

## Where the core-rule problem stands

The record's map is a subagent read of X38–X62, GR1, IC1, IB1, PS1/2, CS1/2 and IJ1, summarised in the README later.

- **Every tested core rule fails G-OUT-M3**, the outer band (1.42–3 Mpc) of the top Mgas500 tercile. It fails as UNDER
  (prediction below measurement):
  - X43 c_f = 4: Z +2.41 / +2.07 (h0672 / h0686);
  - X43 c_f = 5: still fails, and M3 is its **only** failing line;
  - X38: +5.4;
  - IB1 with the hydrostatic gas mass as the total: +5.02.
- **The measured outer ratio rises steadily with mass.** X7's quintiles of A_OUT/C* run 0.65, 0.43, 0.72, 1.31, 1.37 on
  canonical h0672.
- **The verdict document already flags this cell** (§8, committed HEAD): "MGAS T3 OUTER should get a data-side check
  before more rules are built on it."

## Question

**Is the G-OUT-M3 deficit the projected lensing from correlated structure beyond each cluster's turnaround radius?**

- **Why it could be.** The record's cluster model (X30 → X43) places all of a cluster's mass inside r_ta and treats
  everything beyond as the cosmic mean. Real clusters sit in correlated overdensities, whose excess beyond r_ta projects
  into the 1.4–3 Mpc band. The effect scales with the clustering bias, so it grows with cluster mass. It is not double
  counting, because nothing beyond r_ta is in the model.
- **What the term is.** It is derived with **zero free parameters** from the record's own linear power spectrum and
  spherical collapse. It adds to every cluster in every key. The test is whether it repairs M3 without breaking the
  other keys.
- **Normalisation.** The cluster halo normalisation is moved to the native background (owner rule 10-25). Mfair becomes
  (Ω_c/Ω_b)_native × M_b, with Ω_c/Ω_b = 5.2715 from L1 (h 0.6856427, Ω_m 0.2976016, ω_b 0.0223081), replacing X30's
  inherited 5.364 / h 0.674 / Ω_m 0.315 in `prep` and `r_ta_com`.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. The correlated-structure term (frozen)

For each cluster, the 3D excess density is added as

  ρ_2h(r) = b(M) ρ̄_m(z) ξ_lin(r (1+z), z) for r > r_ta (physical), and 0 inside r_ta.

The term is integrated to the record's grid edge (RG max = 30 Mpc physical). The pieces:

| ingredient | definition |
|---|---|
| ξ_lin(r_c, z) | D(z)² ξ_lin(r_c, 0), from the record's CLASS linear P(k) of the background X43 grades clusters with (EM1 `BGS["A_c2b_refit"]`, `pk_lin`, Mpc units). ξ = (1/2π²) ∫ k² P(k) j₀(kr) e^{−k²(0.05 Mpc)²} dk |
| D(z) | X43's `EPS` growth table |
| ρ̄_m(z) | Ω_m ρ_c (1+z)³ on that background |
| b(M) | Mo & White (1996), derived from spherical collapse plus the peak-background split: b = 1 + (ν² − 1)/δ_c, with ν = δ_c / (σ(M) D(z)) and δ_c = 1.686 (X43's DC) |
| σ(M) | X43's `EPS` table |
| M | M_b + Mfair_native, per cluster |

Implementation: M_2h(r) = ∫_{r_ta}^{r} 4π r'² ρ_2h dr' is added to the mass source in `dvecN`, so it goes through the
same projection, miscentring and reduced-shear chain as the halo.

## 2. Rules graded

- **R4** is X43 with c_f = 4. This is the primary rule.
- **R5** is X43 with c_f = 5.
- **RX48** is the X48 ng48 3-seed table, via X48's `x48_regrade_ng48.json`, using the same patch as X62's `run_x43`.

Each rule is run in four configurations: {inherited normalisation, native normalisation} × {without, with} the
correlated-structure term. The **graded configuration is native + with**. The X43 line set is: SPARC on both
backgrounds, the 63 groups, and the 15 cluster keys in both h cells, on both footings.

## 3. Step 0 (stop rule)

- **S0a.** Inherited normalisation, term off, R4 reproduces X43's committed numbers to 3 decimals: G-OUT-M3 pred 1.120 /
  1.108 (canonical h0672 / h0686), groups Z +2.05, SPARC rms 0.0782. This is a repeat of the X43 run.
- **S0b.** σ₈ recomputed from the same `pk_lin` with an 8 Mpc/h top-hat equals EM1's stored σ₈ for that background
  within 1 %.
- **S0c.** b(ν = 1) = 1 exactly, and b increases with M.

## 4. Verdict (per footing; R4 is the primary rule)

- **TWO-HALO REPAIRS M3.** On R4 native + with, |Z(G-OUT-M3)| ≤ 2 in both h cells, and no other cluster key fails that
  passed on R4 native without the term.
- **REPAIRS M3 BUT BREAKS:** M3 passes but at least one other key newly fails. The keys are named.
- **NOT REPAIRED:** M3 still fails.

**Also graded and reported, per rule:** whether R4, R5 or RX48 (native + with) passes **every** X43 line on both footings.
A rule that does is reported as "PASSES THE X43 LINE SET". That statement is scoped to these lines only: KiDS lensing
(X53) and dwarfs (X51) are not regraded here.

**Reported only, never graded:**
- the per-quintile outer ratio (meas/pred) before and after the term;
- the bias range;
- the fraction of OUTER ΔΣ supplied by the term, per tercile;
- Sheth–Tormen bias (simulation-calibrated, not native) as a sensitivity check.

**Variant V-cut1.5:** the term starts at 1.5 r_ta. This is conservative, with less added mass. The verdict is ROBUST if
V-cut1.5 gives the same R4 class; otherwise it is FRAGILE.

## 5. Checks and twin

- **K1.** The term's ΔΣ is ≥ 0 at every OUTER bin for every cluster (positive ξ beyond r_ta at these scales). Any
  negative value is reported.
- **K2.** Mfair_native / Mfair_inherited = 5.2715/5.364 exactly per cluster.
- **K3.** Peak RSS < 1 GB, one thread.
- **MUTATE (`GC1_MUTATE=1`, separate outputs).**
  - m1: the term's sign is flipped.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and K1.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gc1_two_halo.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.
