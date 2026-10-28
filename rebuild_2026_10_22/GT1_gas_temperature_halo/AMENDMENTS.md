# GT1_gas_temperature_halo: AMENDMENTS (committed alone, before the script and before any GT1 number)

Written 2026-10-28, after reading the harnesses (IB1, GS1, CL2, BS1, HO1, HG2/HG1, X43, X30) and before writing
`gt1_gas_temperature_halo.py`. FROZEN_CRITERIA.md (ef8161361e) is not edited. Each item fixes a point the frozen text
leaves open or that cannot be implemented literally. None was chosen from a GT1 result; no GT1 number existed when this
file was written.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Not "theory closed".

## A1. K0's IB1 target cannot be reached literally; it is reproduced in IB1's own configuration

**Why.** The frozen K0 says "with R_g = r_ta and k unused, the inner rule reproduces IB1's HG cluster Z (G-OUT-M3
+5.02 / +4.36)". IB1's +5.02 / +4.36 is not an r_ta run. It is IB1's graded primary:
- the HG mass truncated at r_t = 3 Mpc, floored at M_b;
- the tercile σ fill;
- IB1's own X30 machinery, where the measured cells' C\* denominator uses the record's "P" baryons, not GS1's budget.

GS1's budget changes the C\* denominator (for example, G-OUT-all meas is 0.716 in IB1 and 0.780 in CL2/BS1), so the GT
harness cannot reproduce IB1's Z to 1e-6. IB1's own "r_t = r_ta" variant used the inherited (non-native) r_ta and has no
committed G-OUT-M3 Z.

**K0 (IB1 part), as implemented.**
- X43's copy is executed **without** GS1's budget edit (IB1's machinery: X30 executed unmodified).
- Its cluster line takes IB1's `m_hg` verbatim: r_t = 3 Mpc, floor M_b, tercile fill.
- All 15 keys × 2 h × 2 footings, pred and Z, must equal `ib1_hse_halo_results.json` to 1e-6. That includes G-OUT-M3
  +5.02 / +4.36.
- The same run with the RF fill must equal `ib1_rf_results.json` to 1e-6.
- The literal "R_g = r_ta, k unused" profile inside the GT harness is run and **reported**. It is not a K0 target.

## A2. Cluster implementation details

**M_CL2.** M_CL2(r) is the base route-E profile the X43 copy already builds on its RM grid: GS1's baryons plus the Burkert
halo, truncated at r_ta.
- M_CL2(R_g) = the baryon grid interpolated (linear) at R_g, plus the Burkert mass evaluated analytically.
- M_CL2(r_ta) = M_b,t plus the Burkert mass at r_ta.
- M_budget = M_b,t + M_fair (prep's own values).

**M_HG.**
- M_HG = 3β σ² r³ / [G (r² + r_c²)], with β = 2/3, r_c = 0.15 R500 (prep's R500) and G = X30's G.
- There is no floor and no truncation inside R_g; the frozen rule has neither. (IB1's floor bound in 0 cells.)

**σ.**
- KT clusters: σ² = kT/(0.6 m_p), using X30's constants.
- The other 220: the RF fill, recomputed with IB1 RF's exact least-squares on the tercile-filled σ. Its (a, b) must equal
  `ib1_rf_results.json` to 1e-12.
- The tercile fill is the reported variant.

**Where GT acts.**
- GT acts in `grade_clusters`' graded call (rule = True). X43's internal K0x38 diagnostic call (rule = False) stays on
  the base.
- GT applies to every eRASS1 cluster whatever its switch branch. The number below the switch is reported (expected 0).

**R_g.**
- Primary: R500.
- Reported variants: 0.7 R500, r_ta/2, the continuity-offset variant, and the tercile fill.
- Also reported: the literal R_g = r_ta (A1).
- If R_g ≥ r_ta, the outer piece is empty (counted).

**k.**
- k = (M_budget − M_HG(R_g)) / (M_CL2(r_ta) − M_CL2(R_g)).
- If M_HG(R_g) ≥ M_budget, then k = 0 and the excess M_HG(R_g)/M_budget is reported.

**K2.** For k > 0, the profile's grid values beyond r_ta must equal M_budget to 1e-6 (relative). Clusters whose r_ta lies
beyond the grid (30 Mpc) are counted and checked analytically instead.

## A3. HG2 BRIGHT groups (the frozen text does not define a group's M_CL2, M_budget or r_ta)

**Geometry.**
- R_g = the matched eRASS1 R500 (HG1's `r500`).
- σ² = σ_LOS² (KT2017 σ), so β_spec = 1 (frozen).
- β = 2/3 and r_c = 0.15 R500, HG1's `beta_mass_fraction` convention.
- Radii are HO1's: r = (4/3) R_h, in metres via HG1's MPC. G is EM1's G (GE), as HO1 uses for the halo.

**M_CL2(x).** This is HO1's group profile, extended in radius with the same functions:
- baryons: M_b(<x) = 0.5 M★ + M_gas,500 f_β(x; R500), HG1's function (no truncation). At x = r this gives HG1's g_bar
  exactly;
- halo: the X43 group Burkert halo M_h(<min(x, R200)), at M200 from M★ + M_gas,500 (HO1's).

**M_budget and r_ta.** GS1's own `_gc2_ext` (the namespace's, s = 2.777, native r_ta) is run on (M_gas,500, R500, z_eRASS1)
from HO1's start, 3 × 1.2 × M_gas,500.
- M_budget = M_b,t + (Ω_c/Ω_b)_native M_b,t.
- **Disclosed:** GS1's 1.2 star factor on gas stands in for the stars. The group's own M★ is not added.

**Prediction.**
- On the GT branch, g_pred(r) = G M_tot(r) / r². This is total mass: no separate baryon term and no law.
- FAINT groups keep HO1's base exactly.
- D_pred is HG1's `D_stat` on Δ_pred = log g_pred − log g_ref(g_bar), with HG2's blue-lens reference. g_bar stays HG1's
  for both arms.

**Interval.** The measured interval [−0.511, −0.076] is read from HG2's committed JSON. HG2's D on the measured Δ is
recomputed (no RNG) as a sample-identity check, together with the 190 / 14 / 188 counts.

**Variants.** The R_g variants (0.7 R500 and r_ta/2) and the continuity offset are applied to the BRIGHT groups too
(reported). The σ fill does not apply to groups.

## A4. K4 (X-COP construction check, reported only)

- **Points:** CS2's 35 points, executed from CS2's source as HO1 does. All lie at x ≤ 0.7, inside R500.
- **Prediction:** g_GT = G M_HG(r)/r², with β = 2/3 and r_c = 0.15 R500 (the X-COP header R500).
- **σ:** from the eRASS1 primary catalogue's KT if the cluster matches an entry (nearest within 3′, |Δz| ≤ 0.02, KT > 0).
  Otherwise from the RF fill at M_gas,500 = MGAS at R500 (HO1's XMETA).
- **Reported:** Δ = log g_obs − log g_GT (mean, rms, per radius, per cluster), beside HO1's base numbers. Not graded.

## A5. K0 for the base lines (BS1) and what GT re-runs

**K0 (BS1).** BS1's primary configuration is re-run with GT off, through BS1's own head (executed read-only as text up to its
Step 0 block; output names re-prefixed to gt1_). It must reproduce BS1's committed `primary` block:
- the grade: every leaf on both footings to 1e-6, with exact fail lists (BS1's `same()`);
- the MW box: classes and counts exact; the McMillan V_c, K_z and z to 1e-6;
- the 13 field dwarfs: E and Z to 1e-6, and S1–S3 identical.

**K0 (HO1(b)).** The same GT-off run must reproduce D_pred +0.229 / +0.201 (HO1's committed JSON) to 1e-6.

**With GT on.**
- The X53 (lensing), X51 (dwarfs) and MW runs are carried from the GT-off run: they hold no hot system (criteria §2).
- The X43 copy is re-run, because the clusters change. Its SPARC (both backgrounds) and 63-group results must equal the
  GT-off run exactly. That is K1's "non-hot profile equals base" half, together with the FAINT groups' g_pred identity.

## A6. Reading of the verdict lines

- **(A) passes** iff |Z| ≤ 2 in all 15 keys in both h cells, on that footing.
- **(B) passes** iff D_pred ∈ [−0.511, −0.076] on that footing.
- **(C) passes** iff Step 0's base reproduction holds and, on that footing:
  - no non-cluster line fails: SPARC line, groups, dwarf classes, lensing;
  - BS1's MW line is fixed (at least one box cell passes L1 + L2a + L2b).
- The field-dwarf S3 failure (IC 1613) is the open item stated in advance (criteria §3). It is reported, not part of (C).
- **Alt** is given its own verdict by the same table. Its known BS1 failures (the SPARC line and the MW ultra-faints) make
  its (C) fail by construction (stated now).

## A7. SLUGGS and the 63 groups

- **SLUGGS:** NOT A TEST (criteria §2). Its base-picture numbers are quoted from HO2's committed JSON. They are unchanged
  under BS1 (BS1 criteria (e)).
- **The 63 groups:** they keep the base. Their Z is the GT run's own, and it must equal BS1's.

## A8. MUTATE

- `GT1_MUTATE=1` doubles σ² on K1's analytic side, for both the clusters and the BRIGHT groups. Everything else is
  unchanged.
- Outputs carry `_MUTATE`, including the per-run copy outputs.
- K1 must fail and the run must exit 1.
