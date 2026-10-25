# X31_feedback_energy_selector: does feedback energy per unit binding energy separate the classes that need extra cold mass?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (1aa11f9bcb, committed alone first); `AMENDMENT_A1.md` (358e3859ed,
pre-result, per-row implementation); `AMENDMENT_A2.md` (post-result, reporting only). κ = ½ FITTED. Footings 9.3603e-11 /
1.1312e-10 m s⁻², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the
framework. Every number is in `x31_feedback_energy_selector.out` / `_results.json` / `x31_classes.csv` or
`x31_cluster_F_unbinned.out` / `_results.json`.

## Verdict: FEEDBACK FAILS (both footings)

**F = e_fb / σ_b² does not separate EXTRA from NONE, and it does not order the amounts.**
- **Primary cell** (B_iso, L-S labels, C1, ε_SN = 1). X19's rule finds the best threshold in the **DOWN** direction, at
  F ≈ 10^0.06. Four classes are misordered there: cluster T2 (straddles), the MW ultra-faints, bright M31 and M31 others.
- **Class ordering.** Spearman(log F, E) is +0.102 / +0.096 (p 0.34 / 0.35, n 18). The ORDERS bar is ρ ≥ 0.5 with p ≤ 0.05.
- **In the hypothesis's direction** (UP: more feedback, more extra; A2, reported only), the best threshold still has five
  offenders:
  - canonical, at F ≈ 10^3.22: LG field, Crater II, DF2/DF4, T2, T3;
  - alt, at 10^3.91: Crater II, T2, T3, bright M31, M31 others.
- **Every qualifier also FAILS:** B_EFE, the L-B labels, strict intervals, the C0 and C2 denominators, ε_SN = 0.1, and the
  clusters' F_exc. The closest any comes to ordering is B_EFE: ρ +0.472 / +0.465, p 0.026 / 0.027, still below 0.5.

**Why it fails: the two EXTRA families sit at opposite ends of F.**
- **F spans five decades and is set mostly by 1/σ_b².** Clusters sit at F ≈ 1, because their thermal energy is about their
  binding energy. The NONE galaxies sit at F ≈ 30–300. The gas-poor dwarfs sit at 3e3–5e4.
- **The heavy clusters (EXTRA) have the lowest F of all.** It falls from T1 to T3: 1.56 → 1.04 → 0.78 (Mann–Whitney T1 vs
  T2+T3 p 1e-8). Per unit binding, the clusters that need extra hold *less* thermal energy, not more.
- **The small dwarfs (EXTRA) have high F, but so do NONE systems.** Crater II, at F 5.2e4, is the most feedback-dominated
  system in the table and needs *less* than the law. DF2/DF4 (NONE) has the same F as bright M31 and M31 others (EXTRA).

## F by class (canonical; alt within 0.03 dex for galaxies, identical for clusters, TDGs and groups)

| class | label B_iso / B_EFE | E_iso | F median [16–84 %] | log F | G | σ_b [km/s] |
|---|---|---|---|---|---|---|
| SPARC small | NONE / NONE | −0.046 | 140 [78, 498] | 2.14 | 0 | 44.7 |
| SPARC large | NONE / NONE | −0.047 | 54.9 [30.2, 101] | 1.74 | 0 | 106.8 |
| Groups (band, M★/M_bar 0.1–1) | NONE / NONE | +0.020 | 14.2 [1.95, 128] | 1.15 | 0 | — |
| Clusters T1 (29 with KT) | NONE / NONE | +0.040 | 1.56 [1.18, 2.15] | 0.19 | 0 | 552 |
| Clusters T2 (39) | EXTRA / EXTRA | +0.268 | 1.04 [0.77, 1.37] | 0.02 | 0 | 712 |
| Clusters T3 (38) | EXTRA / EXTRA | +0.264 | 0.776 [0.606, 1.11] | −0.11 | 0 | 888 |
| MW disc | NONE / NONE | −0.143 | 29.2 | 1.47 | 0 | 162 |
| LG field (13) | NONE / NONE | +0.055 | 3.31e3 [1.82e3, 4.93e3] | 3.52 | mixed | 9.3 |
| MW classical (8) | AMBIG / AMBIG | +0.277 | 3.52e3 [3.16e3, 5.00e3] | 3.55 | 1 | 9.0 |
| MW ultra-faint (31) | EXTRA / EXTRA | +0.625 | 2.07e4 [8.92e3, 4.06e4] | 4.32 | 1 | 3.7 |
| bright M31 (25) | EXTRA / EXTRA | +0.249 | 4.71e3 [2.35e3, 1.65e4] | 3.67 | 1 (LGS 3: 0) | 7.8 |
| M31 others (5) | EXTRA / EXTRA | +0.644 | 5.68e3 [4.57e3, 1.86e4] | 3.75 | 1 | 7.1 |
| Crater II | NONE / EXTRA | −0.443 | 5.23e4 | 4.72 | 1 | 2.3 |
| Antlia II | AMBIG / EXTRA | +0.060 | 8.01e3 | 3.90 | 1 | 6.0 |
| Coma UDGs (9) | AMBIG / EXTRA | +0.325 | 592 [339, 859] | 2.77 | 1 | 22.0 |
| UMa members (28) | NONE / NONE | −0.063 | 80.4 [54.7, 127] | 1.91 | 0 | 96.5 |
| TDGs (6) | NONE / NONE | −0.691 | 294 [74.9, 1.50e3] | 2.47 | 0 | 17.5 |
| DF2/DF4 | NONE / NONE | −0.843 | 5.59e3 [3.97e3, 7.22e3] | 3.75 | 1 | 7.5 |
| Cosmic background | EXTRA (requirement) | +0.804 | not placeable (no binding energy) | — | — | — |

**Constants** (`.out` "CONSTANTS"):
- **Supernovae.** Kroupa IMF η_SN = 0.011132 per M☉ formed; R 0.4; E_SN 10⁵¹ erg. That gives
  e_SN = (965.8 km/s)² × M★/M_den.
- **Reionization.** e_re = 412.7 (km/s)² (2×10⁴ K).
- **Expelled-gas share.** g_ref = 2.2603 / 2.3871 (SPARC with M★ ≤ 1e9 M☉, N 59 / 64).
- **MW gas.** 1.191e10 M☉ (A1).

## Hard cases (B_iso; B_EFE in brackets)

| case | F | label | side, X19 best threshold (DOWN, 10^0.06) | side against the hypothesis (UP; A2) |
|---|---|---|---|---|
| Crater II | 5.23e4 / 5.04e4 | NONE [EXTRA] | right [right] | **WRONG** on both footings [right]: the highest F in the table on a system that needs less than the law |
| DF2/DF4 | 5.59e3 / 5.38e3 | NONE [NONE] | right [**WRONG**] | **WRONG** canonical, right alt [**WRONG**]: same F as bright M31 / M31 others |
| Antlia II | 8.01e3 / 7.71e3 | AMBIG canonical, NONE alt [EXTRA] | — / right [right] | — / right (alt's UP threshold 10^3.91 is 0.01 dex above it) |
| TDGs | 294 | NONE [NONE] | right [right] | right [right]: gas-rich, young, F below the dwarfs |
| Clusters T1 vs T2/T3 | 1.56 vs 1.04 / 0.776 | NONE vs EXTRA | T1 right, T2 straddles, T3 right [T2, T3 WRONG] | T2 and T3 **WRONG**: the extra clusters have the *lower* F |
| MW ultra-faints | 2.07e4 / 1.99e4 | EXTRA [EXTRA] | **WRONG** | right |

The two directions trade offenders. DOWN keeps the clusters and loses the dwarfs; UP keeps the dwarfs and loses the clusters,
Crater II and DF2/DF4. No direction keeps both.

## Gas-expelled flag and two-variable search (X19's `two_var`, reported)

- **G alone FAILS.** Offenders: Crater II, DF2/DF4, T2, T3, the background, plus Antlia II on alt.
- **(F, G) does not separate.** Canonical offenders are T2, T3 and DF2/DF4; alt adds Antlia II. On B_EFE the offenders are
  T1 and DF2/DF4.
- **No pair (F, V) with an X19 variable separates.** The best is (F, M_b), with two offenders (bright M31, T1). That is not
  better than X19's (M_b, |Φ|) near miss, which had one.

## Per-system tests (reported, no verdict weight)

**P1, dwarfs** (89 X20 systems per footing; F under C1). Inside the dwarfs, F ∝ 1/σ² (ledger disclosure).

| | Spearman(log F, E) | Spearman(log M★, E) | per-system rank test | median E gas-expelled (77) vs gas-rich (12) |
|---|---|---|---|---|
| canonical B_iso | +0.101 (p 0.35) | −0.654 (p 3.7e-12) | FAILS (27 offenders) | +0.376 vs +0.072 (p 0.021) |
| canonical B_EFE | +0.429 (p 2.8e-5) | −0.807 (p 1.4e-21) | FAILS (18) | +0.846 vs +0.073 |
| alt B_iso | +0.098 (p 0.36) | −0.652 (p 4.5e-12) | FAILS (30) | +0.332 vs +0.036 (p 0.022) |
| alt B_EFE | +0.431 (p 2.5e-5) | −0.808 (p 1.2e-21) | FAILS (20) | +0.802 vs +0.037 |

- **Stellar mass orders the dwarfs, and F does not.** This agrees with X24 (MASS-DRIVEN).
- **The gas-expelled vs gas-rich difference is confounded with mass.** The 12 gas-rich systems are the heavier LG dIrrs, and
  X24 found no hosted-vs-field difference at matched mass. It is not read as a feedback effect.

**P2, clusters** (X21's unbinned machinery exec'd read-only; 106 clusters with KT; 4 cells).

| variable | X21 class | max Δχ² per cell | Spearman with MGAS500 | Z_b at fixed MGAS500 |
|---|---|---|---|---|
| MGAS500 (control, reproduced) | NONE | 3.75 / 3.46 / 3.86 / 3.56 | +1.00 | — |
| KT (reproduced) | DETECTED (SHAPE UNRESOLVED) | 9.13 / 9.72 / 9.24 / 9.83 | +0.58 | — |
| F_cl | **NONE** | 0.42 / 0.61 / 0.43 / 0.62 | −0.65 | +1.09 / +0.97 / +1.09 / +0.97 |
| F_exc (thermal excess) | **NONE** | 1.26 / 1.43 / 1.30 / 1.46 | −0.91 | +2.02 / +1.76 / +2.02 / +1.76 |

- KT tracks the per-cluster excess, but F does not. Dividing KT by the binding energy removes the signal.
- F_exc's partial Z_b ≈ +2 at fixed MGAS500 is reported, not graded.

## Step 5: coupling (reported only)

F neither separates nor orders, so it implies no feedback → cold-sector coupling. The record already closes the nearby
mechanisms:
- **CFG643**, the baryon → cold heat exchange Q_c = C a₀ v ρ_b, is CLOSED on both footings. Its G3 shows that even every
  catchment baryon donating V_f² leaves the budget 1.5–3.5× short.
- **X23_late_heated_cold** has no action and a WRONG AMPLITUDE (12–15×). The heating energy it needs per baryon is about
  8–10 × a SN/AGN feedback scale.
- **X23_late_heating_graded**: LATE HEATING FAILS (under on the dwarfs, over on the clusters).
- **X24b**: vacuum heating has no ε window and the wrong sign.
- **CFG930**: energy-limited settling is CONTRADICTED (X19 step 2).

No action in the record keys the cold sector to feedback energy.

## Checks

- **Class script: 6/6 PASS** (exit 0, 0.97 s, 0.31 GB).
  - **K0.** X19's table is reproduced exactly: E, s and Z on both baselines and both footings, and every L-S label (0
    mismatches).
  - **K0b.** The M_b and σ intervals match exactly.
  - **K1.** η closed form vs quadrature agree to 6.7e-16; σ(1 keV) = 399.6 km/s; the kT₅₀₀ round trip closes to 3.3e-16.
  - **K2.** The oracle 10^E SEPARATES on both footings.
  - **K3.** Every class's F recomputes from its own members.
  - **K4.** Peak RSS is under 1 GB.
- **Cluster script: 6/6 PASS** (exit 0, 24 s, 0.55 GB).
  - X21's own K1, K0 (X7 bins to 4.4e-16) and K2 pass.
  - **K5.** X21's V0 and V1 cells are reproduced to 0.0 (56 numbers).
  - **K6.** Each cluster's F recomputes from its own eRASS1 row (0.0).
  - **K4.** Peak RSS is under 1 GB.
  - X21's inherited code prints RuntimeWarnings (overflow in its scan matmul); the reproduction is exact regardless.

**MUTATE** (`X31_MUTATE=1`):
- **Class script.** F lists are deranged across classes, and E/s/Z are swapped (UFD ↔ LG field, T1 ↔ T3). **K0 FAILS**
  (48 mismatches) and **K3 FAILS** (34 classes), as required. Result: 4/6, exit 1.
- **Cluster script.** F is permuted across clusters. **K6 FAILS** (rel dev 2.1), as required. Result: 5/6, exit 1. The
  shuffled F turns WEAK (Δχ² 3.8–5.5) by chance.
- Outputs are `*_MUTATE.*`.

## What this does not show

- **e_fb is injected energy, not retained energy, for galaxies.** It is a present-day thermal energy for clusters. ε_SN = 0.1
  moves all galaxies down one decade together and does not rescue the test (FAILS on both footings).
- **The record has no cluster entropy profiles.** F_exc, the excess of kT over kT₅₀₀ from eRASS1 M500/R500 (scaling-relation
  masses), is a crude stand-in for the entropy excess.
- **Several inputs are PROVISIONAL (from memory):** the IMF, R, T_re, f★,cos, the groups' M★ band and the gas flags.
  Groups are a band, and the background is not placeable.
- **Not blind.** The ledger stated before any number that F would inherit σ's galaxy-scale offenders, and it does. The
  clusters' place (lowest F) was not known in advance.

## Files and commits

- `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (1aa11f9bcb); `AMENDMENT_A1.md` (358e3859ed); `AMENDMENT_A2.md` (result
  commit).
- `x31_feedback_energy_selector.py`, with `.out`, `_results.json`, `x31_classes.csv` and the `_MUTATE` twins.
- `x31_cluster_F_unbinned.py`, with `.out`, `_results.json` and the `_MUTATE` twins.
- Run: `OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 <script>` (and with `X31_MUTATE=1`).
- No downloads. Inputs are read-only: X19, X20, X1, X24, X21/X7/X2/X13, SPARC, Lelli+15, CFG657, Tian+26, eRASS1 and CFG695.
