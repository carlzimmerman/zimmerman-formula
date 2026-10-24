# ZT_zstar_tests — FROZEN CRITERIA (committed alone, before any script or number)

Lane `rebuild_2026_10_22/ZT_zstar_tests/`. Written 2026-10-23. Rules: `rebuild_2026_10_22/BRIEF.md` and
`doors_push_2026_10_22/BRIEF.md`. κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt), scored
separately, never pooled. No dark-matter particle (the cold sector is cold energy, a medium). Fix-forward only. No new
fitted constant to pass a line; no knob scans. No personal names or home paths. Never "theory closed"; never "the data
favour the framework". Compute: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes, no downloads. Pathspec commits of
this lane only; never push.

## 0. What is run, and the governing plan

The first three decisive tests of design Z★ (v3s-OC), **exactly as frozen** in
`rebuild_2026_10_22/Z1_successor_design/TEST_PLAN.md`, committed alone in **0d1959a4f5** before any test ran
(sha256 8d0ef349fdcf05ab…; unchanged at HEAD). Its §2 frozen lines for **Z-T1** (hosted retention, with the Coma UDG
side line), **Z-T2** (capacity-truncated law on the cluster terciles) and **Z-T3** (two-sided obstacle 0 ≤ D·P ≤ ρ_d)
govern. The design is `Z1_successor_design/DESIGN.md` (f65f181cc1). This file adds only the implementation choices the
plan leaves open (§2–§4), declared before any Z-T number was computed. Where this file and the plan differ, the plan wins.

## 1. Inputs (read-only; scripts are copied or exec'd from source text, never edited)

| input | commit | sha256 (16) | used for |
|---|---|---|---|
| `X1_hosted_recount/x1_per_system.csv`, `x1_hosted_recount_results.json` | c74c622229 | cda27005b8a6173b, e3c7558661c1b020 | Z-T1 classes, Δ[iso AQUAL L*0], class bootstrap median ± sd, control members |
| `real_research/data/dsph/lvd_dwarf_{local_field,mw,m31}.csv` (LVD, Pace 2024) | 2b6bb658a1 (last touch) | d9ea1a0cf93e2eb1, 6970dea6a1c29f9e, eb5a6cedf4a585cf | RAW HI flux_HI (Jy km/s) + distance; MDF mean and width (extension only) |
| `P1_dwarf_chemistry/p1_per_system.csv`, `p1_dwarf_chemistry.py` | e9f445a580 | 3f178a6e7d5c2b36, 129c03dc39e8bd3e | Δ_hi = ½ log₁₀ L_MDF_I0_m05; the copied L_MDF function (extension only) |
| `S1_v3_hosted_small/s1_v3_hosted_small_results.json` | 2b6bb658a1 | 9a5322d13799ebfe | Coma isolated-law excess and its error |
| `campaign_fresh_gravity/CFG948_nocapture_vs_udgs/cfg948_results.json` | 4a06363f9f | ff21ef3b2ef3872d | field HI-UDG gas fraction (R6_HUD) |
| `X2_cluster_outskirts/x2_cluster_outskirts.py`, `_results.json`, `x2_replay_percluster.npz` | 1d837f6945 | 52ed15f74e716ad4, 81a80fc099e98e30, 8d473764e791df67 | Z-T2 data, statistics, systematics (e), terciles, projector, gas shapes, reduced shear |
| `F1_cluster_cores/f1_cluster_cores.py`, `F2_outer_lensing/f2_aqual.py`, `CFG949_clusters_untethered/cfg949.py` | f1803b0256, —, 012eaa526e | 4837ade939d4dc83, 7420d7290e63132a, 0ea76d16354b9e49 | as exec'd by X2 (F1 constants/kernels; EFE table for the K0 reproduction only; CFG930/949 debris profile) |
| `X3_switched_stiffness/x3_switched_stiffness.py`, `_results.json` | 31febd3b70 | 9b7098982ae0528f, 8d63aac13dbadcd3 | Z-T3 slab (copied function) and B2-S symbol |
| `Z1_successor_design/z1_successor_design.py` | f65f181cc1 | 292d3ef04703bd4e | f_s = 5.364, Ω_m = 0.2976, K5/K10 closed forms |

**Coverage facts found while inventorying (before any Z-T number; they decide which legs can run):**
1. P1 has L_MDF for **0 / 8 MW classical**, **0 / 5 M31 others** (P1 "not tested": no MDF width on disk),
   **3 / 25 (canonical), 4 / 25 (alt) bright M31**, and **26 / 31 MW ultra-faints** (P1 tested; Carina III, Grus I,
   Pictor II, Tucana II, Tucana IV not tested).
2. X1's 13 isolated LG field dwarfs span log M★ 5.43–8.51 (LVD, Υ_V = 2). An owner with log M★ < 4.93 has **no isolated
   dwarf within ±0.5 dex**: 30 / 31 ultra-faints and 4 / 5 M31 others. RAW HI (flux_HI, distance) is on disk for 11 of the
   13; Cetus and Tucana carry HI upper limits only.

## 2. Z-T1 (hosted retention) — implementation choices

**Observed.** For each class the bootstrap class median of Δ[iso AQUAL L*0] and its bootstrap sd σ are X1's committed
`class_stats["<foot>|<class>|primary|iso AQUAL L*0"]` (median, sd). Classes and membership exactly as X1's `cls` column:
MW classical (8), bright M31 (25), MW ultra-faint (31), M31 others (5); control LG field (13). The four `indiv:` systems
and the M31 dEs are in no class (reported only).

**Δ_lo,i.** M_HI,j = 2.356e5 (D_j/Mpc)² S_j M☉ from LVD `flux_HI` (Jy km/s) and `distance` (RAW; check against LVD
`mass_HI`); M_gas = **1.33** M_HI (the record's He factor, CFG948 l.529, P1 `GAS_FAC`); M★,j = 10^logMstar (X1/LVD,
Υ_V = 2). HI upper limits (Cetus, Tucana): **primary gas = 0**; at-the-limit reported. Window: the isolated dwarfs j with
|log M★,j − log M★,i| ≤ 0.5 (an owner in the control includes itself). Δ_lo,i = ½ log₁₀(1 + median_j(M_gas/M★)_j).
Empty window: **Δ_lo,i UNDEFINED** (no substitute).

**Δ_hi,i** = ½ log₁₀(L_MDF_I0_m05,i) from P1's committed CSV, same footing, any P1-tested system (flags OK and ABOVE
both carry P1's L). Not in P1: **UNDEFINED** (no substitute).

**Class edges.** Δ_lo,class = median over members with a defined Δ_lo,i; Δ_hi,class likewise. An edge is defined only if
**at least half** of the class's members have the per-owner value; otherwise the edge is UNDEFINED and its missing inputs
are listed. The edges are treated as exact; σ is the observed class sd only.

**Class status (per footing).** IN if Δ_lo,class − 2σ ≤ Δ_obs ≤ Δ_hi,class + 2σ with both edges defined. OUT if a defined
edge is violated (Δ_obs < Δ_lo,class − 2σ, or Δ_obs > Δ_hi,class + 2σ), whether or not the other edge is defined.
UNDETERMINED otherwise.

**Control.** Δ_lo,control = median of the 13 control members' Δ_lo,i. Passes if |Δ_obs,control − Δ_lo,control| ≤ 2σ_control,
per footing.

**Frozen verdict (plan §2, verbatim logic).** PASS: ≥ 3 of 4 classes IN on both footings and the control passes on both.
FAIL: ≥ 2 classes OUT on either footing, or the control fails on either. Otherwise UNDECIDED (with the reason: coverage or
data). A Z-T1 FAIL kills Z★.

**Reported only, no verdict weight (declared now):** (E1) empty window → Δ_lo,i = 0, the design's own floor (K9 with no
loss); (E2) empty window → the isolated dwarf nearest in log M★; (E3) Δ_hi for members without a P1 value from P1's own
`lmdf()` exec'd from its source on LVD `metallicity` and the LVD width (P1's `lvd_sigma`, interval I0, log y −0.5,
M_gas = 1.33 M_HI), admissible only if it reproduces P1's committed L_MDF_I0_m05 on every P1-tested system to ≤ 1e-9
relative; (E4) HI upper limits at the limit; (E5) control leave-one-out. An "extended" class table (E1 or E2 with E3) is
printed with the class rule applied, labelled EXTENSION, never the verdict.

**Coma side line (frozen).** Δ_pred = ½ log₁₀(1/(1 − 0.81)) = 0.361 dex (the plan's number). Observed: S1's isolated
AQUAL excess `coma.<foot>|S2 AQUAL isolated L*0 E-W.meanE_dex` (0.325 / 0.285); σ = S1's `se`/ln 10 (statistical).
PASS if |Δ_pred − Δ_obs| ≤ 2σ, per footing. Reported: S1's S0 (CFG933 law, 0.330 / 0.291), σ with S1's σ_sys in
quadrature, Δ_pred at CFG948's unrounded median and at its Υ_g = 0.5 / 2 brackets.

**Checks.** K1 RAW HI reproduces LVD `mass_HI` (≤ 0.02 dex, all detections); K2 X1 class_stats reproduce X1's README
iso-AQUAL row (rounded to 0.01) for all five classes on both footings; K3 the copied `lmdf` reproduces P1's committed
L_MDF_I0_m05 on all P1-tested systems (≤ 1e-9 rel; gates E3); K4 deep-AQUAL retention identity: for the spherical
simple-μ law at x ≤ 1e-4, log g(M_orig) − log g(M_now) = ½ log(M_orig/M_now) to ≤ 1e-3 (the ½ in Δ_lo, Δ_hi, Δ_pred);
K5 Coma inputs: CFG948 R6 `Ups1.0|all` median rounds to 0.81; S1 S0 meanE/ln 10 = 0.330 / 0.291 (rounded); K6 RSS < 1 GB.
**`--mutate`:** Newtonian retention (exponent 1 instead of ½) and HI mass without the D² factor; K1 and K4 must FAIL.

## 3. Z-T2 (cluster terciles) — implementation choices

**Data and statistics.** X2's replay npz (equal to F1's cache), X2's catalogue-Mgas500 terciles (T1/T2/T3), X2's
`stats()` (A per band, jackknife over F1's 30 RA patches restricted to the tercile, systematics (e): cross shear and
random-minus-random in quadrature). Functions are exec'd read-only from X2's and F1's source text, as X2 did with F1.
Boost convention primary; clipped reported. Both of X2's native-h cells, h = 0.672 and 0.686.

**Baseline (primary) = C*_own** = X2's C* without the EFE: CFG814 gas (a1), reduced shear (d), systematics (e). Reason:
R2's owner frame removes the EFE from the owner's own law (DESIGN §4, K6); X2 found the EFE moves A by ≤ 0.017.
Reported: C0 + (e) (F1's β = 2/3 gas, no reduced shear).

**The Z★ profile per cluster** (X2's rescaled gas, M_b = 1.2 M_gas as X2/F1):
- Law: g_law = F1's `g_aqual_sph`(G M_b(<r)/r², a₀); phantom M_ph(<r) = g_law r²/G − M_b(<r).
- R_own: the radius where (1 + f_s) M_b(<R) = (4π/3) Δ ρ_ref R³ (K10's definition with the profile), f_s = 5.364, with
  ρ_ref at the cluster's redshift, flat native background Ω_m = 0.2976 and the cell's h:
  Δρ_ref = 200 ρ_c(z), and Δρ_ref = 18π² Ω_m ρ_c0 (1+z)³ (EdS convention, as Z1). **Both reported and both scored.**
- M_b,own = M_b(<R_own); supply S = f_s M_b,own.
- r_s, two definitions (an implementation bracket, the plan's own rule: a class is drawn only where both agree):
  **(cap)** the radius where M_ph(<r) = S (capacity exhausted; R1; equals the plan's closed form for point-mass baryons,
  check K2); **(lit)** the plan's closed form r_s = r_M √(f_s(f_s+1)), r_M = √(G M_b,own/a₀), with the enclosed-mass step at
  r_s (a shell of mass S − M_ph(<r_s)) kept as it falls; negative-density cells are floored by X2's projector and their
  fraction is reported.
- Not supply-rich (R_own ≥ r_s): M = M_b + M_ph inside r_s; M = M_b + S beyond.
- Supply-rich (R_own < r_s): M = M_b + M_ph inside R_own; beyond, M = M_b + M_ph(R_own) + E_f·m_deb(<r)/m_deb(∞),
  E_f = S − M_ph(R_own), with m_deb CFG930's native debris profile as exec'd by X2 (CFG949 `supply("S-cen")` with
  f★ = 0.20 on this cluster's gas, `prof930(M_ta, z, 3000, "rta")`, `cold_profile`). The law is not continued beyond
  R_own (that would double count the supply).
- Projection, miscentring, ΔΣ, reduced shear: X2's `model()` code path unchanged from M(<r) on.

**Frozen class (plan §2).** Per footing, R_own convention, r_s definition and h cell: a tercile passes a band if
|A − 1| ≤ 2 s_tot. **PASS:** MID and OUTER pass in all three terciles. **PARTIAL:** OUTER passes in all three, MID fails in
≥ 1. **FAIL:** otherwise. Per footing and R_own convention, the class stands if both h cells and both r_s definitions give
it; otherwise "SPLIT" with the cells listed. The plan forecasts MID unchanged (T2, T3 fail). Z-T2 does not kill Z★; it
records the cluster row.

**Checks.** K0 X2's tercile A and s_jk at C0 and C* (boost, law, all four cells) reproduced to ≤ 1e-6 (needs F2's EFE
noclu table: two solves); K1 f_s = 1e6 reproduces the C*_own law ΔΣ to ≤ 1e-9 relative; K2 on point-mass baryons r_s(cap)
= r_s(lit) = r_M √(f_s(f_s+1)) to ≤ 1e-3; K3 bookkeeping M(r_max) = M_b(r_max) + S for every cluster and variant to
≤ 1e-6 relative; K4 reduced-shear factor ≥ 1, median κ_MID < 0.1; K5 RSS < 1 GB. **`--mutate`:** cross shear as the data
and the held dust added on top of the untruncated law (M = M_b + M_ph + S); K0 and K3 must FAIL.

## 4. Z-T3 (two-sided obstacle) — implementation choices

**Symbol (B2-S, sympy).** X3's principal part c² = (s₀ + ρ_d)(γ_L/2)F″(s₀) with the two-sided stiffness
F = max(s, 0)² on s ≤ ρ_d plus the upper obstacle (indicator of s ≤ ρ_d). In the saturated set {s₀ = ρ_d}: one-sided
F″(ρ_d⁻) = 2; the exact penalty form F_P = max(s,0)² + P·max(s − ρ_d, 0)² (P ≥ 0, P → ∞ is the obstacle) gives
c² = γ_L(s₀ + ρ_d)(1 + P·Θ(s₀ − ρ_d)). Line: c² ≥ 0 for every s₀ in the saturated set, for every ρ_d > 0 and P ≥ 0, with
γ_L = K L★²/2 at each footing's L★ floor (21.68 / 22.85 pc). Reported: a smoothed upper wall (support reaching s < −ρ_d)
puts c² < 0 in the soft region, as X3 found for the lower switch; a penalty whose support starts at ρ_d − ε keeps c² ≥ 0
iff ε ≤ 2ρ_d.

**Slab (Part C copied).** X3's `slab()` is exec'd from its source text (K0: it reproduces X3's committed C2 ladder at
γ_L = 1e-3 to ≤ 1e-9). The two-sided version (this lane's copy): background held density s₀^Z = min(s₀, ρ_d) with
X3's s₀ = −0.5 + cos 2πz; ρ_τ = s₀^Z + ρ_d on faces; stiffness γ_L on nodes with s₀^Z > 0; saturated nodes s₀ ≥ ρ_d.
The one-sided (variational-inequality) linearisation is bracketed by two linear limits:
**(ii) released** — saturated nodes keep γ_L (perturbations below the wall), the sup over the whole space;
**(i) pinned** — δ(D·P) = 0 on saturated nodes (held = all dust, infinite stiffness), imposed exactly by restricting
L⁻¹ to the null space of the saturated rows of D, the sup over the subspace. Primary: ρ_d = 0.1 (X3's C2) on X3's
unaligned grid, N = 64, 128, 256, 512, 1024.
**Footings:** γ_L = K L★,floor²/(2λ²) for slab period λ = 0.1 kpc and 1 kpc (canonical 2.350e-2 / 2.350e-4, alt
2.610e-2 / 2.610e-4); X3's 1e-3 also run.

**Frozen line (plan §2).** **PASS:** for both brackets (i) and (ii), both footings and both λ: the finest two levels agree
within 10 %, Γ ≤ X3's rigorous discrete bound √(K(M − 1 + f₋)·max|ρ_τ⁻|) at every level, and the symbol's c² ≥ 0 in the
saturated set for ρ_d > 0. **FAIL:** a finest ratio > 1.10 (divergence) in any primary ladder, or c² < 0 anywhere in a
saturated region. Otherwise UNDECIDED. A Z-T3 FAIL kills Z★.

**Diagnostics, no verdict weight:** ρ_d = 0.01 and ρ_d = 0 (the degenerate wall coinciding with the switch) on aligned and
unaligned grids up to N = 2048; X3's sign-violation count; the literal lower obstacle of R1 (s₀ clamped to [0, ρ_d], so
ρ_τ ≥ ρ_d > 0 everywhere), stated with its static consequence (v3s's D·P < 0 lobes would be forbidden; X3's statics lemma
no longer covers them). **`--mutate`:** the switch removed (Θ = 1) inside the two-sided ladder; the slab line must FAIL.

## 5. Overall reading

Z★ survives these three tests only if Z-T1 is not FAIL and Z-T3 is not FAIL. Z-T2 records the cluster row. An UNDECIDED
is stated with its reason and the missing inputs, not upgraded.

## 6. Disclosures (not blind)

Before this file, the following were already public and were read: X1's class medians (README table), P1's L_MDF values,
S1's Coma excess, CFG948's 0.81, X2's tercile A values (C0 and C*), X3's slab ladders, and Z1's own forecasts (K9 lost
fractions; tercile total/law ≤ 1.04; design/law at 2 Mpc 0.24 / 0.44 / 0.68). The coverage facts in §1 were found by
joining file columns, before any Z-T number. Z-T2's r_s bracket and the C*_own baseline were chosen knowing X2's EFE
effect is ≤ 0.017; Z-T3's footing γ_L mapping was chosen knowing X3's Γ is γ_L-independent at convergence.

## 7. Assumption ledger (BRIEF rule 2; classes RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY)

| ingredient | class | where |
|---|---|---|
| LVD HI flux, distance, σ, r_h, M_V | RAW (compilation) | LVD csv |
| M★ at Υ_V = 2; M_gas = 1.33 M_HI | SURVEY-CALIBRATION | X1, CFG948, P1 |
| Δ[iso AQUAL L*0] (spherical Plummer, Wolf estimator, binary correction) | FRAMEWORK-NATIVE (AQUAL, μ = x/(1+x)) on X1's estimator conventions | X1 |
| L_MDF (one-zone ζ ≥ 1 family, log y −0.5) | external chemistry model, CFG317 yield bracket | P1 |
| retention Δ = ½ log(M_orig/M_now) (deep law, before tides) | FRAMEWORK-NATIVE (Z1 K9) | Z1 |
| Coma f_gas 0.81 (Leisman+17 HUDs at Υ_g = 1) | SURVEY-CALIBRATION | CFG948 R6 |
| eRASS1 Mgas500, R500 (rescaled to native h) | SURVEY-CALIBRATION (h-rescaled) | X2/F1 |
| KiDS ΔΣ stack, n(z), boost, miscentring | RAW + SURVEY-CALIBRATION | F1/X2 |
| β-model gas (r_c 0.15 R500), CFG814 r⁻³ beyond 2.2 R500, f★ = 0.20 | SURVEY-CALIBRATION | F1/X2 |
| f_s = 5.364 (Ω_c/Ω_b) | ΛCDM-PROCESSED (record input, used as the design's supply ratio) | Z1 |
| Ω_m = 0.2976, h 0.672 / 0.686, 200ρ_c, 18π²ρ̄_m (EdS) | FRAMEWORK-NATIVE background; overdensity conventions | Z1, X2 |
| CFG930 debris profile (NFW form, C = 3000, r_b = r_ta) | conventions (NFW form flagged in X2) | CFG949 |
| slab model K = 1, M = 2, s₀ = −0.5 + cos 2πz | H4/X3 test model | X3 |
| no EFE inside an owner (R2) | FRAMEWORK-NATIVE design rule, NON-VARIATIONAL | Z1 DESIGN §2 |
| R1 capacity 0 ≤ D·P ≤ ρ_d, held/free exchange | design rule, NON-VARIATIONAL dynamics | Z1 DESIGN §2 |

No STANDARD-MOND-MACHINERY is used for a verdict (no QUMOND, no additive EFE recipe; the law is the spherical AQUAL
first integral).
