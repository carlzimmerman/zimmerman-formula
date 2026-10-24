# X20_hosted_dwarf_requirement — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** At the level of individual systems (not class medians), what does the required extra in hosted dwarfs
track, and is it a physical selector or a measurement artefact?

Standing rules: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m s⁻², never pooled. No
dark-matter particle (the extra is "cold energy", a field). No knob scan, no fit: every threshold is read off the data
ordering, never tuned to a χ². Not "theory closed". Nothing here may say the data favour the framework. No downloads.

## 0. Step 0 (stop rule)

The lane recomputes X1's per-system draws from X1's committed inputs: the LVD tables, CFG257's Arroyo-Polonio / Geha
tables and X1's committed stage tables `x1_stage_tables_{canonical,alt}.json`. It uses X1's code path, copied with
provenance (X1 commit c74c622229): `build`, `pred_draws`, `boot_ix`, `boot_median`, the seed 20261031 and the same
order of RNG calls.

- **K0 (per system).** Every system's median draw for B_iso and B_EFE (and Newton) must equal `x1_per_system.csv`
  (`Delta[...]`, `sdMC[...]`) to ≤ 1e-9 dex, on both footings, for all 89 systems.
- **K1 (class medians).** X1's bootstrap class medians and sd (`class_stats["<f>|<class>|primary|<key>"]`, keys
  `iso AQUAL L*0` and `AQUAL + EFE L*0 (exact MOND + EFE)`) must reproduce to ≤ 1e-9 for all 10 classes, both footings.

If K0 or K1 fails, the verdict is **UNDECIDED (stop rule)** and no correlation is graded.

## 1. Required extra per system

For system i, baseline b, footing f:

- **E_i** = median over X1's MC draws of Δ = log₁₀(g_obs/g_pred,b), dex in g (X1's primary dataset: Υ_V = 2, free-f
  binary ratio applied only to M_V > −7.7, LVD σ).
- **s_i** = √(sdMC² + (0.15·k_i)²): sdMC is the draws' sd, and 0.15 dex is X1's Υ prior (UPS_PRIOR). k_i =
  |1 + d log G_b/d log y| from the system's own committed b-table (column E-W, central finite difference over ±0.6
  dex), the same construction as X1's k_i for the v3 floor.
- **Z_i** = E_i / s_i. Labels (X19's L-S rule): **EXTRA** if Z ≥ 2; **NONE** if Z < 1 (includes every negative E);
  **AMBIGUOUS** if 1 ≤ Z < 2.

Baselines:
- **B_iso (PRIMARY):** `iso AQUAL L*0` (isolated law, μ = x/(1+x), no external field).
- **B_EFE (SECONDARY, verdict qualifier):** `AQUAL + EFE L*0 (exact MOND + EFE)`, v3s's static prediction in the host
  field, as X19 used it.

Samples:
- **ALL:** X1's 89 systems (MW, M31, LG field; LMC, SMC, M32 excluded by X1).
- **HOSTED (verdict sample):** host = MW or M31 (76 systems: every X1 class except "LG field").

## 2. Candidate variables (per system; computed from the record's catalogue values; never fitted)

Physical (P):
| id | V | definition |
|---|---|---|
| P0 | log M★ | X1's logMstar (Υ_V = 2) — added: X19's M_b and Z2's M_V proxy |
| P1 | log r_half | X1's rh_pc (LVD rhalf_sph_physical, else rhalf_physical) |
| P2 | log Σ | M★ / (2π r_half²) [M☉ pc⁻²] |
| P3 | log x | g_N/a₀ at r₁/₂ = 4/3 r_half: G(M★/2)/r₁/₂² / a₀ (footing-dependent) |
| P4 | log e | X1's x_e_mid (S1 host field at X1's host distance, E_mid host) |
| P5 | log (x/e) | P3 − P4 |
| P6 | log (V_rel / V_esc,b) | CFG939: V_esc,b = √(2\|Φ_b(r₁/₂)\|), Plummer Φ_b = −G M★ / √(r₁/₂² + r_half²). V_rel = the host's law circular speed at the host distance, √(g_host · R) with X1's g_host (S1 host model, E_mid; LG field: X1's MW-mass convention). A bound satellite's orbital speed relative to the host's settled medium |
| P7 | log q | r₁₂/r_t at the PM pericentre from Z2's committed `z2_per_system.csv` (q_ISO for B_iso, q_MOND for B_EFE; only rows with pm = True). SUBSET: MW E3 systems only |
| P8 | ellipticity | LVD `ellipticity` (missing → excluded from that V) |
| P9 | log d_host | X1's d_host_kpc |

Measurement (M):
| id | V | definition |
|---|---|---|
| M1 | log (δσ/σ) | LVD ½(vlos_sigma_em + vlos_sigma_ep)/vlos_sigma (complete; monotone in the N_eff proxy, so it doubles as the star-count proxy) |
| M2 | log N★ | member stars with velocities, only where the count is for the same dataset as the LVD σ (Z2's rule, copied: Geha II for Geha-cited rows; Collins 2013 for Collins-cited M31 rows; Arroyo-Polonio when its reference equals LVD's). SUBSET |
| M3 | log b | binary-correction factor X1 applied (Arroyo-Polonio per-system free-f ratio, else its median for M_V > −7.7, else 1) |
| M3f | binary flag | 1 if b ≠ 1 else 0 (binary-corrected or not) |
| M4 | source | LVD `ref_vlos`, grouped by first-author token (letters before the year); families with ≥ 3 members graded, the rest pooled as "other" |
| M5 | single epoch | NOT ON DISK per system (declared; no proxy is graded). Reported as unavailable |

## 3. Statistics

For each variable, baseline, footing and sample (ALL, HOSTED):
- Spearman ρ_S and Kendall τ_b between V and E_i (systems with V defined).
- **Bootstrap sd:** 2000 resamples of systems (seed 2026102401). In each resample, E_i is redrawn as E_i + s_i·N(0,1),
  so the error carries both sampling and per-system measurement error.
- **Strength z** = |ρ_S| / sd_boot(ρ_S) (Kendall reported beside it). Permutation p (2000 shuffles of E) reported.
- **M4 (categorical):** Kruskal–Wallis H across families. Permutation p (2000 shuffles) → z = Φ⁻¹(1 − p/2), capped at
  the resolution (p ≥ 1/2001).
- Variables with fewer than 10 defined systems in a cell are reported but not graded (SUBSET variables P7, M2 are graded
  only where N ≥ 10).

**Per-system separation test (X19's, at points).** EXTRA vs NONE labels (AMBIGUOUS dropped). For each V, scan every
threshold between consecutive sorted values, both orientations. Offenders = systems on the wrong side; report the
minimum count, the threshold, and the AUC (Mann–Whitney EXTRA vs NONE) with its bootstrap sd. **SEPARATES** iff 0
offenders with ≥ 3 systems on each side.

**Collinearity (reported, qualifies the verdict).** For the best P and best M in the verdict cell, their mutual ρ_S and
the partial Spearman of E on each controlling the other (rank-residual method), with the same bootstrap.

**Baseline dependence (reported).** Label counts per baseline in HOSTED; the systems whose label changes between B_iso
and B_EFE; ρ_S of (E_EFE − E_iso) with P4 (log e).

## 4. Frozen verdict (per footing; the verdict cell is HOSTED × B_iso; then both footings must agree)

Let z_P = max strength over graded physical variables (P0–P9), z_M = max over graded measurement variables (M1–M4),
in HOSTED × B_iso.

1. **Stop rule:** K0 or K1 fails → UNDECIDED.
2. **BASELINE-DRIVEN:** in HOSTED, fewer than 3 systems are EXTRA on B_iso while at least 3 are EXTRA on B_EFE.
3. **MEASUREMENT-DRIVEN: V_M** if z_M ≥ 3 and z_M ≥ z_P.
4. **PHYSICAL SELECTOR: V_P** if (z_P ≥ 3 or V_P SEPARATES) and z_P > z_M.
5. **NO ORDERING:** z_P < 3, z_M < 3 and no variable SEPARATES.
6. The two footings give different classes (or different V) → **UNDECIDED**.

**Qualifiers (stated with the class, never change it):**
- [EFE-DIFFERS] if the same rule on B_EFE gives a different class or V.
- [CONFOUNDED] if the best P and best M have mutual |ρ_S| ≥ 0.5 and neither partial reaches 2σ.
- [ALL-DIFFERS] if the rule on ALL gives a different class or V.

## 5. Checks (all must PASS in the normal run; exit 1 if any fails)

| id | check |
|---|---|
| K0 | per-system draws reproduce `x1_per_system.csv` (§0) |
| K1 | X1 class bootstrap medians reproduced (§0) |
| K2 | positive control: the oracle V = the E column from `x1_per_system.csv` itself has strength z ≥ 3 on HOSTED × B_iso and SEPARATES (both footings) |
| K3 | null control: 200 random-normal V (seeded) give a false-alarm rate (z ≥ 3) ≤ 5 % |
| K4 | Spearman/Kendall implementation equals scipy.stats (if importable) to 1e-12; else a hand-checked 5-point case |
| K5 | Plummer V_esc,b: closed form vs numerical ∫ g_N dr to ≤ 1e-6 relative (3 test systems) |
| K6 | peak RSS < 1 GB |

**MUTATE twin** (env `X20_MUTATE=1`): after the draws are rebuilt, the per-system rows of the B_iso and B_EFE draw
arrays are shuffled across systems (seeded permutation, per footing). Required: K0, K1 and K2 FAIL; outputs written to
`*_MUTATE.*`; exit 1.

## 6. Outputs

`x20_hosted_dwarf_requirement.py` → `x20_hosted_dwarf_requirement.out`, `_results.json`, `x20_per_system.csv`; MUTATE
twins `*_MUTATE.*`. Run: `OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 x20_hosted_dwarf_requirement.py`. Every
README number comes from these files.
