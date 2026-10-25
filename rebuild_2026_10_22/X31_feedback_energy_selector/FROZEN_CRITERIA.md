# X31_feedback_energy_selector — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** Does the cumulative feedback / heating energy per baryon, relative to the system's binding energy per
baryon, F = e_fb / e_bind, separate the classes that need extra cold mass from those that need none, and does it order
the amounts?

Standing rules: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m s⁻², never pooled. No
dark-matter particle (the extra is "cold energy", a field). No fitting and no knob scan: every constant below is a
standard value, labelled, and fixed here. Not "theory closed". Nothing here may say the data favour the framework.
Raw data and framework-native record results only; no downloads.

## 1. The class table and labels (X19, exactly; step 0 must reproduce it)

Source: X19_selector_rank_test (criteria 8960ea2285, A1 0fc9bade54, result with A2), `x19_selector_rank_test_results.json`
keys `E_table["<footing>|iso"|"<footing>|efe"]` and `results.labels`. E in dex of g over the baseline, s its sd, Z its
significance. Label rule L-S (X19 §1): EXTRA if Z ≥ 2, NONE if Z < 1, AMBIG if 1 ≤ Z < 2; AMBIG classes are shown but do
not constrain.

| class | canonical B_iso E (s) Z, label | canonical B_EFE | alt B_iso | alt B_EFE |
|---|---|---|---|---|
| SPARC small | −0.046 (0.027) −1.71 NONE | same | −0.070 (0.027) −2.60 NONE | same |
| SPARC large | −0.047 (0.015) −3.06 NONE | same | −0.055 (0.015) −3.61 NONE | same |
| Groups | +0.020 (0.065) +0.31 NONE | same | −0.021 (0.065) −0.31 NONE | same |
| Clusters T1 | +0.040 (0.133) +0.29 NONE | same | +0.001 (0.133) +0.01 NONE | same |
| Clusters T2 | +0.268 (0.087) +2.29 EXTRA | same | +0.230 (0.087) +2.05 EXTRA | same |
| Clusters T3 | +0.264 (0.041) +4.83 EXTRA | same | +0.228 (0.041) +4.32 EXTRA | same |
| MW disc | −0.143 (0.014) −9.93 NONE | same | −0.164 (0.014) −11.40 NONE | same |
| LG field (13) | +0.055 (0.080) +0.68 NONE | +0.055 (0.081) +0.68 NONE | +0.017 (0.080) +0.21 NONE | +0.018 (0.080) +0.22 NONE |
| MW classical (8) | +0.277 (0.148) +1.87 AMBIG | +0.335 (0.251) +1.33 AMBIG | +0.235 (0.150) +1.57 AMBIG | +0.294 (0.255) +1.15 AMBIG |
| MW ultra-faint (31) | +0.625 (0.111) +5.62 EXTRA | +1.350 (0.189) +7.15 EXTRA | +0.585 (0.109) +5.37 EXTRA | +1.315 (0.183) +7.19 EXTRA |
| bright M31 (25) | +0.249 (0.092) +2.70 EXTRA | +0.578 (0.131) +4.41 EXTRA | +0.211 (0.090) +2.34 EXTRA | +0.544 (0.132) +4.11 EXTRA |
| M31 others (5) | +0.644 (0.283) +2.28 EXTRA | +0.990 (0.337) +2.94 EXTRA | +0.587 (0.284) +2.07 EXTRA | +0.934 (0.340) +2.75 EXTRA |
| Crater II | −0.443 (0.134) −3.31 NONE | +0.494 (0.139) +3.56 EXTRA | −0.478 (0.128) −3.73 NONE | +0.465 (0.132) +3.51 EXTRA |
| Antlia II | +0.060 (0.054) +1.11 AMBIG | +1.007 (0.072) +13.97 EXTRA | +0.024 (0.055) +0.44 NONE | +0.972 (0.073) +13.24 EXTRA |
| Coma UDGs (9) | +0.325 (0.198) +1.64 AMBIG | +1.121 (0.262) +4.28 EXTRA | +0.285 (0.197) +1.45 AMBIG | +1.078 (0.262) +4.11 EXTRA |
| UMa members (28) | −0.063 (0.027) −2.28 NONE | same | −0.060 (0.028) −2.11 NONE | same |
| TDGs (6) | −0.691 (0.102) −6.80 NONE | −0.587 (0.110) −5.35 NONE | −0.728 (0.102) −7.17 NONE | −0.623 (0.110) −5.68 NONE |
| DF2/DF4 (2) | −0.843 (0.209) −4.04 NONE | −0.720 (0.209) −3.45 NONE | −0.881 (0.209) −4.22 NONE | −0.756 (0.209) −3.63 NONE |
| Cosmic background | +0.804 (requirement) EXTRA | same | same | same |

**X24's per-mass dwarf extra (context, from `x24_dwarf_velocity_floor_results.json` `footings.<f>.A`).** At matched
log M★ 5.4–6.8 the hosted (23) and field (6) median E are +0.243 / +0.207 (canonical) and +0.191 / +0.170 (alt); hosted
minus field Z 0.27 / 0.16 (MASS-DRIVEN). Field-only Spearman(E, log M★) −0.731 (p 0.003), all dwarfs −0.633 / −0.632. The
per-system dwarf E used here are X20's (`x20_per_system.csv`, `E_B_iso`, `lab_B_iso`, `E_B_EFE`, `lab_B_EFE`).

## 2. Proxies (specific energies, per unit baryon mass, in (km/s)²; never fitted)

**(a) Supernova energy per baryon.** e_SN = ε_SN · E_SN · η_SN · M★ / (1 − R) / M_den.
- E_SN = 10⁵¹ erg per core-collapse SN. η_SN = N(8–100 M☉) / M(0.1–100 M☉) for a Kroupa (2001) IMF, ξ ∝ m^−1.3 on
  0.1–0.5 M☉ and m^−2.3 on 0.5–100 M☉, continuous at 0.5; computed in-script in closed form.
- R = 0.4: the mass returned to the gas by an old population (M_formed = M★/(1 − R)), applied to every system.
- ε_SN = 1 (PRIMARY): the total energy injected, with no coupling efficiency assumed. ε_SN = 0.1 is reported only.
- Not counted: SN Ia, stellar winds, galaxy-scale AGN.

**Reionization (all systems).** e_re = (3/2) k T_re / (μ m_p), with T_re = 2×10⁴ K and μ = 0.6. It is added to every bound
system's e_fb.

**(b) Cluster gas thermal energy per baryon.** e_ICM = (1/1.2) · (3/2) kT / (μ m_p) from eRASS1 KT (KT > 0 rows only),
μ = 0.6 (X19). Baryons are 1.2 × MGAS500 (F1's f★ = 0.20, X19). Stars, 0.2/1.2 of the baryons, carry e_SN as in (a) with
M_den = M_b. The record holds no per-cluster entropy profiles, so the "entropy excess" is replaced by the **thermal excess
over virial**: e_exc = (1/1.2)(3/2) max(kT − kT₅₀₀, 0)/(μ m_p), with kT₅₀₀ ≡ μ m_p G M500/(2 R500) (eRASS1 M500, R500).
F_exc (with e_exc in place of e_ICM) is reported, and is a second variable in the per-cluster test (§5).

**(c) Binding energy per baryon.** e_bind = σ_b². Galaxy scale: X19's σ for each system (σ_LOS for pressure-supported
systems, V/√2 for rotators: SPARC and UMa at the last point, TDG V_circ, MW v_c(R₀)/√2, groups σ). Clusters:
σ_b² = G M500 / (2 R500) from eRASS1 M500 and R500. X19's cluster σ (from KT) is **not** used, because it would make F
circular.

**(d) F = (e_SN + e_ICM + e_re) / e_bind**, plus the gas-expelled flag G.
- G = 1: every hosted dwarf in X1 (MW classical, ultra-faints, bright M31, M31 others, Crater II, Antlia II), the isolated
  LG dwarfs Cetus and Tucana, the Coma UDGs and DF2/DF4.
- G = 0: the gas-rich LG field dIrrs (Antlia B, Aquarius, IC 1613, Leo A, Leo T, NGC 6822, Pegasus dIrr, Phoenix,
  Sagittarius dIrr, UGC 4879, WLM), LGS 3 (the bright-M31 transition dwarf with HI), SPARC, UMa, the MW, TDGs, groups and
  clusters.
- These morphology labels are PROVISIONAL (from memory). G is never fitted.

**Denominator M_den (baryons).**
- **C1 (PRIMARY).** Use the record's baryons. Where the record's inventory is stars only (X1 dwarfs, Coma UDGs, DF2/DF4),
  use M_den = M★ (1 + g_ref). Here g_ref is the median of 1.33 M_HI / (U₀ L[3.6]) over SPARC galaxies with
  U₀ L[3.6] ≤ 10⁹ M☉, with U₀ from CFG695 per footing, computed at load time. For G = 1 systems this is the expelled
  share at a gas-rich dwarf's gas-to-star ratio. For the gas-rich LG dIrrs it stands for current gas that is missing from
  the record's inventory.
- **C0 (reported).** The record's M_b exactly (stars only for the dwarfs).
- **C2 (reported, cosmic fair share).** For G = 1 systems, M_den = M★ / f★,cos with f★,cos = 0.07 (PROVISIONAL: stellar
  share of cosmic baryons); otherwise as C1.

**Groups.** Tian+26 gives only M_bar, whose composition is not on disk. M★/M_bar is therefore a band [0.1, 1]
(PROVISIONAL). The class interval runs from the 16 % point at 0.1 to the 84 % point at 1.0, a band in X19's sense.
**Cosmic background.** There is no binding energy, so F is not placeable. As in X19, the verdict runs on bound systems
(qualifier).

## 3. Rank test and separation rule (X19 §4, identical)

X19's own `rank_test` and `two_var` functions are exec'd verbatim from `x19_selector_rank_test.py`, on log₁₀ F.
- **Intervals.** 16–84 % of members (N ≥ 3); min–max for N < 3; bands for groups.
- **(a) Gap.** max(hi over NONE) < min(lo over EXTRA) (UP), or the reverse (DOWN). F* is the geometric centre of the gap.
- **(b) Grading.** Among EXTRA classes ordered by median F, no pair is reversed by more than √(s_i² + s_j²).
- **(c) Completeness.** Every decisive bound class has a value.
- **Offenders.** The classes misordered at the best threshold.
- **Two-variable search (reported qualifier).** Run if F fails. It uses X19's `two_var` on (F, G) and on F paired with
  each of X19's verdict-bearing V (X19's per-class intervals).

**Ordering statistic (for the ORDERS class).** Spearman ρ between log₁₀ F_median and E over every bound class with both
values (decisive and AMBIG). One-sided permutation p (H₁: ρ > 0), 20 000 permutations, seed 3131.

## 4. Verdict classes (primary: B_iso, L-S labels, C1, ε_SN = 1, 16–84 % intervals)

- **FEEDBACK SEPARATES (threshold F\*)**: X19 status "SEPARATES" (a + b + c) on both footings.
- **FEEDBACK ORDERS BUT DOES NOT SEPARATE**: not the above, but on both footings either the status is "SEPARATES, NOT
  GRADED", or ρ ≥ +0.5 with p ≤ 0.05.
- **FEEDBACK FAILS (offending classes named)**: neither, on both footings.
- **UNDECIDED**: the footings disagree in class; or fewer than 2 placeable EXTRA or 2 placeable NONE classes; or the
  step-0 stop rule fires.

Qualifiers (reported, no verdict weight): B_EFE; C0; C2; ε_SN = 0.1; strict min–max intervals; L-B labels; F_exc for the
clusters; the two-variable searches. Each one's class is stated, and so is any change from the primary.

**Hard cases (reported individually).** For Crater II, DF2/DF4, Antlia II, TDGs and cluster T1 vs T2/T3: F (median and
interval), and whether it lies on its label's side of the best threshold, on both footings and both baselines.

## 5. Per-system tests (reported, no verdict weight)

- **P1, dwarfs.** X20's per-system E and labels (B_iso, B_EFE) are joined to X1's per-system M★ and σ. Reported per
  footing and per baseline:
  - Spearman(log F, E), with Spearman(log M★, E) beside it;
  - the X19 rank test on per-system points (zero-width intervals; L-S labels from X20);
  - the gas-expelled vs gas-rich medians of E.
- **P2, clusters.** X21's unbinned machinery is exec'd from `x21_switch_anatomy.py` (C*, CAL, 4 cells, permutation p,
  same seeds by variable index). Variables:
  - V0, MGAS500 (control);
  - V1, KT (both reproductions);
  - F1, F_cl per cluster (KT > 0);
  - F2, F_exc per cluster.
  X21's classes are DETECTED / WEAK / NONE and THRESHOLD / SMOOTH / SHAPE UNRESOLVED. The tercile medians of F for
  T1 vs T2 + T3 are also reported, with a Mann–Whitney p.

## 6. Step 0 (stop rule)

X19's class-table machinery (its source up to the rank-test definitions) is exec'd read-only with X19_MUTATE unset.
- **K0.** Every class's E, s and Z (both footings, both baselines) and every L-S label (both footings) must equal X19's
  committed JSON exactly (float equality; the background's Z is infinite).
- **Stop rule.** Any mismatch stops the lane with verdict UNDECIDED.
- **K0b.** X19's per-class M_b and σ intervals must equal the JSON's `intervals`.

In the cluster script, X21's V0 and V1 cells must reproduce X21's JSON `tests` to ≤ 1e-9 (b, s_b, Z_lin, D_med, Z_b, Z_c,
p_scan). Otherwise P2 is marked NOT REPRODUCED and is not reported as a result.

## 7. Checks

- K0 / K0b: step 0, as in §6.
- K1: unit identities.
  - η_SN closed form vs numerical quadrature, ≤ 1e-6 relative.
  - σ(1 keV, μ 0.6) = 399.6 km s⁻¹ ± 1 %.
  - kT₅₀₀ round trip ≤ 1e-12.
- K2 (positive control): an oracle F_or = 10^E per class must separate under L-S on both footings, using the same
  machinery and interval layout.
- K3 (F identity): each class's F median recomputed from its own member list equals the tabled value (≤ 1e-12).
- K4: peak RSS < 1 GB.
- K5 (cluster script): X21 reproduction (§6).
- K6 (cluster script): each cluster's F recomputes from that cluster's own KT, M500 and R500 (≤ 1e-12).

## 8. MUTATE (`X31_MUTATE=1`; outputs `*_MUTATE.*`, exit 1)

- **Class script.**
  - (i) The per-class F lists are permuted across the bound classes (seed 3131, a derangement).
  - (ii) E, s and Z are swapped between the MW ultra-faints and the LG field, and between T1 and T3, in the table used
    for testing (as X19).
  - Required: **K0 FAILS** (the swapped rows no longer match X19's JSON) and **K3 FAILS** (class F no longer recomputes
    from its members).
- **Cluster script.**
  - F_cl and F_exc are permuted across clusters (seed 3131).
  - Required: **K6 FAILS**.

## 9. Step 5 (reported only)

If F separates or orders, state the coupling it would imply: an energy exchange between baryon feedback and the cold
sector, per baryon, keyed to F. Grep the record for an action that carries it: CFG643 (baryon → cold heat exchange),
X23_late_heated_cold, X23_late_heating_graded, X24b_vacuum_heated_cold and `campaign_fresh_gravity/LEDGER.md`. State
whether it would be new physics (+ constants). If F fails, report what the record already says about these mechanisms.

## 10. Compute

Two scripts: `x31_feedback_energy_selector.py` (classes, P1) and `x31_cluster_F_unbinned.py` (P2, X21 machinery).
- Single thread, `nice -n 15`, PYTHONHASHSEED=0, < 1 GB, minutes. No downloads. Nothing outside this lane is written.
- Outputs `.out`, `_results.json` and a per-class CSV. Every README number comes from these.
