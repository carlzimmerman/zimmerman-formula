# CFG966 FROZEN CRITERIA: stars vs HI inside the same dwarfs (WLM, IC 1613, DDO 210, DDO 216)

Block 960–969 (LEDGER row CFG960–969, owner reservation 2026-10-21; CFG966 = NA-4 of `NEW_ANGLES_SCOUT_2026-10-21.md`,
b54828855). Frozen 2026-10-23, committed ALONE before any script of this lane exists. Kind: DATA DISCRIMINATOR
(pre-registered), N = 4: **a pointer, not a verdict.** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never
pooled. Raw data and framework-native quantities only. Extra mass is cold energy, not a particle. Not "theory closed".
Nothing here says the data favour the framework.

## 1. Question

Pressure-supported dwarfs sit about +0.37 dex above the law g_N = g²/(g + a0) (CFG919 dwarf class +0.372 / +0.332 dex,
canonical / alt, ν_e), while rotators sit on it (CFG828, CFG843, CFG860, CFG919). Every comparison so far uses DIFFERENT
systems. In a dwarf with BOTH a stellar velocity dispersion and an HI rotation curve, one potential is traced twice at the
same radius:
- **system property:** both tracers show the excess;
- **tracer / estimator property:** only the stellar dispersion shows it.

## 2. Record check (targeted reads only, before freezing)

- `NEW_ANGLES_SCOUT_2026-10-21.md` NA-4 (lines 222–258).
- CFG874 (`cfg874.py` in full, README): the record's dwarf estimator. Wolf at r½ = (4/3)·rhalf_sph_physical, g_obs = 3σ²/r½,
  Υ_V = 2, g_bar = G(Υ_V L_V/2 + M_gas(<r½))/r½², M_gas = 1.33 M_HI inside r½ from the Wang+16 disc (extended root), ν_e.
  CFG874 / CFG880 / CFG828 / CFG852 / CFG860 / CFG931 all EXCLUDE WLM, IC 1613 and Pegasus dIrr (rotating / gas-rich set);
  Aquarius (= DDO 210) is in CFG874 / CFG860 / CFG880 / CFG828.
- CFG880 (README, estimator lines), CFG919 (README, kernel lines 72–74: ν_e primary, ν_simple bracket), CFG828 (README),
  CFG931 (README, `cfg931_lt_info.out`, SPARC loader + `rot_delta`/`rot_cells` + A1-3 UGCA 444 INFO code),
  CFG442 (README, Oh+2015 VizieR ReadMe), CFG449 (FETCH_LOG, result commit 65d5795904).
- Owner / coordinator note 2026-10-23: the framework's action is AQUAL with μ(x) = x/(1+x), not QUMOND (doors push E2); for
  isolated dwarfs the two agree; any EFE or ν choice uses the record's AQUAL statement.

**Stored numbers seen before freezing:** Aquarius Δ★ (CFG874 primary, gas, ν_e) −0.04408 / −0.08229; Aquarius zero-gas
(CFG860) +0.13177 / +0.09265; CFG880 Aquarius σ_law 8.21 vs σ_obs 7.80; CFG931 A1-3 UGCA 444 cell means
[−12.5,−12) +0.19659 (3 pts) / [−12,−11.5) −0.01555 (7 pts) canonical, +0.15704 / −0.05366 alt; CFG931 LITTLE THINGS
single-point (R_max) residuals for DDO 210, DDO 216, WLM, IC 1613.

**This lane is NOT blind.** Before freezing I also read the Iorio+2017 tables for WLM, DDO 210, DDO 216 (including the
asymmetric-drift column: in DDO 210 V_a ≫ V_r near r½) and the Oh+2015 scaled curves, and made by-hand estimates with the
record's estimator (canonical, ν_e): stellar excess WLM ≈ −0.1, IC 1613 ≈ −0.5, Pegasus dIrr ≈ +0.1 dex (Aquarius −0.04,
stored); stars minus HI at r½ ≈ +0.1 (WLM), ≈ 0.0 (IC 1613), ≈ +0.2 (Pegasus dIrr). **Expected outcome, written down now:
NOT DIAGNOSTIC** (DDO 210 asymmetric-drift dominated, and fewer than 3 dwarfs with a > 2σ stellar excess). The reading rules
in section 6 are the brief's; the operational definitions needed to compute them are marked [OP] and were written with the
above in view.

## 3. Data (on disk, read-only; nothing downloaded)

| input | path | sha256 |
|---|---|---|
| LVD local field (σ, r_h, M_V, M_HI, distances) | `real_research/data/dsph/lvd_dwarf_local_field.csv` | d9ea1a0c…85db |
| LVD MW / M31 (K only, CFG874 sample) | `real_research/data/dsph/lvd_dwarf_mw.csv`, `lvd_dwarf_m31.csv` | 6970dea6…fa5f / eb5a6ced…1b35 |
| Oh+2015 curves (AD-corrected 'Data', scaled) | `campaign_fresh_gravity/CFG442_a0_rung_expansion/data/oh15_rotdmbar.dat` | 1ce3e9ee…efe4c |
| Oh+2015 table 2 (R_max, V(R_max)) | `…/CFG442_a0_rung_expansion/data/oh15_table2.dat` | cc8ab9e5…0efb |
| Oh+2015 table 1 (distances) | `…/CFG442_a0_rung_expansion/data/oh15_table1.dat` | 4dc9f372…b3f4 |
| Iorio+2017 curves (V_r, V_a, V_c) | `campaign_fresh_gravity/CFG449_a0_rung_iorio_edd/data/iorio17_finalrot.zip` | d4c456c6…2ce2285 |
| SPARC UGCA 444 (= WLM) | `real_research/data/sparc_data/UGCA444_rotmod.dat` | 75814d6f…3787 |
| SPARC Table 1 (Q, Inc; K only) | `real_research/data/SPARC_Lelli2016c.mrt` | 5aa0501f…8243 |
| record outputs (K) | CFG874 / CFG860 / CFG931 `*_results.json` | read-only |

`SPARC_table.txt` is a saved 404 page and is never read. Full checksums are printed by the script.

**Inventory.** LVD dwarfs with a measured σ and HI: LMC, SMC, LGS 3, NGC 185, NGC 205, Antlia B, Aquarius, IC 1613, Leo A,
Leo T, NGC 6822, Pegasus dIrr, Phoenix, Sagittarius dIrr, UGC 4879, WLM. Of these, only WLM, IC 1613, Aquarius (DDO 210)
and Pegasus dIrr (DDO 216) have an HI rotation curve on disk (Oh+2015 26 galaxies; Iorio+2017 17; SPARC: UGCA 444 only).
The sample is these four. IC 1613 has Oh+2015 only.

## 4. Estimators

- **Radius:** r½ = (4/3)·rhalf_sph_physical (LVD), the record's Wolf radius. The LVD distance is the common distance: HI
  radii are rescaled R → R·D_LVD/D_curve (Oh table 1 / Iorio header / SPARC header distance); velocities unchanged.
- **Stellar:** g★ = 3σ²/r½ (Wolf), σ = LVD vlos_sigma, error (em + ep)/2, δlog g★ = (2/ln10)·δσ/σ. No stellar-rotation term
  (none on disk; the record never applied one). Stellar rotation would RAISE g★ (disclosed direction).
- **Baryons (identical for both tracers):** g_bar = G(Υ_V L_V/2 + M_gas(<r½))/r½², Υ_V = 2, L_V from LVD M_V
  (M_V,⊙ = 4.83), M_gas = CFG874 primary `gas_in(lHI, r½, "disc")` copied unchanged.
- **HI:** g_HI = V_c(r½)²/r½, V_c = the authors' asymmetric-drift-corrected circular speed (Oh 'Data'; Iorio V_c), linear
  interpolation in R, error δV interpolated, δlog g_HI = (2/ln10)·δV/V. Spherical potential assumed. SPARC V_obs is used as
  compiled (source Ke07), with the record's CFG931-V3 pressure bracket (V² + 2·8²) as a variant.
  Reach rule [OP]: interpolate inside the curve; for R_last < r½ ≤ 1.10·R_last use the outermost point; beyond that the set
  does not reach r½. Oh curves are truncated at table 2 R_max (WLM's file continues past R_max with unrelated low values).
- **Kernels.** PRIMARY: ν_A(y) = ½(1 + √(1 + 4/y)), the exact spherical inverse of the record's AQUAL statement
  μ(x) = x/(1+x), i.e. g_N = g²/(g + a0); for an isolated, spherically averaged system AQUAL and QUMOND coincide.
  CO-READING: ν_e(y) = 1/(1 − e^(−√y)), the kernel behind the record's stored dwarf excess (CFG874/880/919), needed for K.
  The class is stated for both; if they differ the lane carries the flag KERNEL-SENSITIVE (the primary reading stands).
- **EFE:** none (isolated dwarfs, record convention CFG874; record's AQUAL statement). The EFE changes the prediction, not
  either measured g_obs, so Δ below is EFE-independent.
- **Residuals:** E_X = log10(g_X / (g_bar·ν(g_bar/a0))) dex, X = ★ or HI. **Δ = E★ − E_HI = log10(3σ²/V_c(r½)²)**: by
  construction independent of footing, kernel, baryon model and EFE (checked as an identity, K5).
- **Errors:** σ(E★) = kin★ ⊕ 0.05 floor; σ(E_HI) = kin_HI ⊕ σ_curve ⊕ 0.05 floor; σ(Δ) = kin★ ⊕ kin_HI ⊕ σ_curve.
  σ_curve,i [OP] = max(½ × the largest pairwise |E_HI| difference among the curve sets reaching r½ in dwarf i, 0.05 dex).

## 5. Curve sets

- **Primary:** Oh+2015. Where Oh does not reach r½ (reach rule), the primary for that dwarf is Iorio+2017 [OP].
- **Brackets:** Iorio+2017 (WLM, DDO 210, DDO 216 scenario 1; `ddo216b` scenario 2 is variant V3); SPARC UGCA 444 (WLM).
  E_HI is reported on every set that reaches r½.

## 6. Reading (per footing, per kernel; never pooled)

Usable dwarf [OP]: E★ > 0 with E★/σ(E★) > 2, and the primary HI set reaches r½.

Applied in this order:
1. **NOT DIAGNOSTIC (CURVES):** WLM's two curve sets, Oh+2015 vs SPARC UGCA 444, differ by > 0.15 dex in E_HI at r½
   (Iorio–SPARC and Oh–Iorio reported, not graded).
2. **NOT DIAGNOSTIC (AD):** the asymmetric-drift correction at r½ in DDO 210 or DDO 216 (scenario 1), c_AD =
   log10(V_c²/V_r²) from Iorio+2017 (the only set with V_r and V_a separately), exceeds the effect. Effect [OP] = the
   CFG919 dwarf-class excess, 0.372 dex canonical / 0.332 dex alt (used for both kernels).
3. **NOT DIAGNOSTIC (NO LEVER):** fewer than 3 usable dwarfs.
4. **SYSTEM PROPERTY:** ≥ 3 usable dwarfs with E_HI ≥ 0.5·E★ (the HI residual carries ≥ 50% of the stellar excess).
5. **TRACER PROPERTY:** ≥ 3 usable dwarfs with E_HI < 0.5·E★ AND |E_HI| < 2σ(E_HI) (HI consistent with 0 while the stellar
   excess is > 2σ). The SYSTEM and TRACER counts are disjoint, so both cannot fire.
6. otherwise **MIXED**.

Footing class = the result of 1–6. Lane class = the primary-kernel class if canonical and alt agree, else UNDECIDED
(FOOTING-SPLIT). A labelled SHADOW reading, with no class weight, applies 3–6 with switches 1–2 ignored (any dwarf whose c_AD
exceeds the effect dropped), so the per-dwarf content is visible whatever the switches do.

**Secondary (the scout's NA-4 (iv) rule; no class weight):** D̄ = inverse-variance mean of Δ_i over dwarfs whose primary
HI reaches r½ (footing- and kernel-independent). |D̄| < 0.10 → "tracers agree"; D̄ > 0.20 at ≥ 2σ → "stellar estimator
high"; otherwise "unresolved". Also reported: whether D̄ + 2σ(D̄) < 0.372 ("an estimator inflation as large as the full
dwarf excess is disfavoured in these systems"). Where no dwarf carries an excess, D̄ measures estimator agreement, not the
excess's origin, and it is reported that way.

## 7. Variants (reported; a class change marks the lane FRAGILE)

V1 major-axis radius, r½ = (4/3)·rhalf_physical. V2 Iorio+2017 as primary where it reaches r½. V3 DDO 216 scenario 2
(`ddo216b`). V4 gas compact root (CFG874 bracket). V5 no gas. V6 SPARC with the CFG931-V3 pressure term (enters the WLM
switch-1 comparison only).

## 8. Controls

- **K1 (record excess):** with ν_e and CFG874's primary gas, Aquarius Δ★ = −0.04408 / −0.08229 reproduced to 1e-9; with
  gas zero, CFG860's +0.13177 / +0.09265 to 1e-9.
- **K2:** WLM, IC 1613 and Pegasus dIrr have NO stored stellar excess in the record (excluded by CFG828/852/860/874/880/931).
  K2 verifies their absence from the CFG874 stored members and says so; there is nothing to reproduce.
- **K3 (SPARC residual for UGCA 444):** CFG931's A1-3 cell means (no point cut, ν_e, Υ_disk 0.5) reproduced to 1e-9.
- **K4 (parse):** Oh V at table 2 R_max equals table 2 V(R_max) within 0.6 km/s for the four; Iorio
  |V_c − √(V_r² + V_a²)| ≤ 0.02 km/s on every row used.
- **K5 (identity, by construction):** E★ − E_HI = log10(3σ²/V_c²) to 1e-12 on every footing and kernel.
- **MUTATE** (separate `_MUTATE_<mode>` outputs). The data switches 1–2 are properties of the real curves that a plant does
  not change, so MUTATE grades the decision core (3–6) and reports the switches.
  - `hi` (the brief's control): +0.37 dex on every HI curve set (V_c² × 10^0.37). Must flip the core to SYSTEM if the main
    core reads TRACER. If the main core is NO LEVER, this mode cannot flip anything by construction; it is then reported as
    "not applicable (no stellar lever)" and the two plants below carry the control.
  - `plant_system`: exact-float plants, E★ := +0.37 and E_HI := +0.37 at every dwarf (σ and V_c replaced by the values the
    law + 0.37 dex predicts at each dwarf's g_bar; real errors kept). The core must read SYSTEM on both footings and kernels.
  - `plant_tracer`: E★ := +0.37, E_HI := 0. The core must read TRACER on both footings and kernels.
  Exit 0 only if every graded requirement holds; exit 1 otherwise. The main run exits 1 if any K fails.

## 9. Compute and hygiene

One core (OMP_NUM_THREADS=1, `nice -n 10`), < 100 MB, seconds; numpy only. No downloads. No other lane's file is edited;
record outputs are read-only. Outputs: `cfg966.py`, `cfg966.out`, `cfg966_results.json`, `cfg966_MUTATE_<mode>.out`,
`cfg966_results_MUTATE_<mode>.json`, README (five-sentence plain summary first).
