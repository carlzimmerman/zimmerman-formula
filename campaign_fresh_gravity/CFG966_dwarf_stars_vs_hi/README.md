# CFG966: stars vs HI inside the same dwarfs (WLM, IC 1613, DDO 210, DDO 216)

**Plain summary.** Four Local Group dwarfs have both a stellar velocity dispersion and an HI rotation curve on disk, so the
same gravity can be measured twice at the same radius. With the record's own estimator, none of the four shows the dwarf
excess in its stars: they sit at g_bar ≈ 10^−11.7 to 10^−11.1 m/s², above the region where the +0.37 dex excess lives. The
pre-registered class is therefore **NOT DIAGNOSTIC**: DDO 210's HI curve at r½ is dominated by its asymmetric-drift
correction, and no dwarf carries a > 2σ stellar excess to split. What the data do show is that the two tracers agree with
each other: stars minus HI at r½ averages +0.05 ± 0.09 dex. So in these four systems the stellar-dispersion estimator does
not inflate gravity by anything like the full excess, but with N = 4 gas-rich dwarfs this is a pointer, not a verdict, and it
says nothing directly about the faint pressure-supported dwarfs below 10^−12 that carry the excess.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only. Cold
energy, not a particle. Not "theory closed". Nothing here says the data favour the framework.

- **Kind:** DATA DISCRIMINATOR (pre-registered), NA-4 of `NEW_ANGLES_SCOUT_2026-10-21.md`. Block 960–969.
- **Criteria:** `FROZEN_CRITERIA.md`, 5ec3dc16a, committed alone before any script.
- **Not blind** (disclosed in the criteria, section 2): by-hand estimates and the Iorio asymmetric-drift columns were seen
  before freezing. The expected outcome written there was "NOT DIAGNOSTIC". That is what happened.
- **Run:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg966.py` (0.1 s, peak RSS 46 MB, numpy only, nothing downloaded).
  `CFG966_MUTATE=hi|plant_system|plant_tracer` writes `cfg966_MUTATE_<mode>.out` / `cfg966_results_MUTATE_<mode>.json`.

## Method (as frozen)

- **Same estimator for both tracers (CFG874):** r½ = (4/3)·rhalf_sph (LVD), Υ_V = 2, gas inside r½ from the Wang+16 disc
  (extended root), g_bar = G(Υ_V L_V/2 + M_gas)/r½². LVD distances throughout; HI radii rescaled to them.
- **Stars:** g★ = 3σ²/r½ (Wolf). **HI:** g_HI = V_c(r½)²/r½, with V_c the authors' asymmetric-drift-corrected circular
  speed. Oh+2015 is primary (Iorio+2017 where Oh does not reach r½); Iorio+2017 and SPARC UGCA 444 are brackets.
- **Kernel:** primary ν_A = ½(1 + √(1 + 4/y)), the exact spherical inverse of the record's AQUAL statement μ = x/(1+x)
  (AQUAL and QUMOND agree for isolated dwarfs). Co-reading: ν_e, the kernel behind the record's stored dwarf excess. No EFE
  (isolated dwarfs; record convention).
- **Residuals:** E_X = log10(g_X / g_law). **Δ = E★ − E_HI = log10(3σ²/V_c²)** is independent of footing, kernel, baryon
  model and EFE (K5 checks the identity).

## Result

**LANE CLASS: NOT DIAGNOSTIC (AD)**: both footings, both kernels. Switch 2 fires: DDO 210's asymmetric-drift correction at r½
is 0.962 dex, against an effect of 0.372 / 0.332. Underneath it, the decision core reads **NO LEVER** in every reading: zero
dwarfs have a stellar excess > 2σ. The shadow reading (switches ignored) is also NO LEVER.

Per-dwarf table, canonical footing, ν_A (dex; ν_e differs by ≤ 0.002):

| dwarf | r½ pc | log g_bar | E★ (stars) | E_HI (primary set) | Oh15 / Iorio17 / SPARC | **Δ = E★ − E_HI** | c_AD at r½ |
|---|---|---|---|---|---|---|---|
| WLM | 1066 | −11.12 | −0.043 ± 0.111 | −0.147 ± 0.140 (Oh15) | −0.147 / −0.243 / −0.199 | **+0.104 ± 0.164** | 0.017 |
| IC 1613 | 1920 | −11.32 | −0.603 ± 0.091 | −0.588 ± 0.120 (Oh15) | −0.588 / – / – | **−0.016 ± 0.133** | – |
| DDO 210 (Aquarius) | 426 | −11.66 | −0.044 ± 0.169 | +0.142 ± 0.430 (Iorio17) | – / +0.142 / – | **−0.186 ± 0.457** | **0.962** |
| DDO 216 (Pegasus dIrr) | 869 | −11.72 | +0.073 ± 0.095 | −0.083 ± 0.199 (Oh15) | −0.083 / −0.304 / – | **+0.156 ± 0.209** | 0.094 |

Alt footing (ν_A): E★ −0.079 / −0.640 / −0.083 / +0.034; E_HI −0.182 / −0.624 / +0.103 / −0.122. Δ is unchanged.

- **Switch 1 (WLM curve sets, Oh15 vs SPARC at r½):** 0.052 dex, below 0.15, so it does not fire. Iorio–SPARC differ by
  0.044 dex and Oh–Iorio by 0.096 dex.
- **Switch 2:** DDO 210 0.962 dex (Iorio: V_r ≈ 5.5 km/s vs V_c ≈ 16.7 km/s at r½), so it **fires**. DDO 216: 0.094 dex. Oh's
  DDO 210 curve ends at 0.34 kpc (at the LVD distance), short of r½ = 0.43 kpc.
- **Secondary (the scout's NA-4 rule; no class weight; footing- and kernel-free):**
  - D̄ = **+0.047 ± 0.091 dex** inverse-variance (unweighted +0.015, N = 4), so the reading is "tracers agree";
  - D̄ + 2σ = 0.23 < 0.372, so an estimator inflation as large as the full dwarf excess is disfavoured in these four systems;
  - because no dwarf carries an excess, this measures estimator agreement, not the excess's origin.

**Variants** (all NOT DIAGNOSTIC, both kernels; no class change, so not FRAGILE):
- V2 Iorio primary, V3 DDO 216 scenario 2, V4 compact gas, V5 no gas, V6 SPARC + CFG931-V3 pressure term: NOT DIAGNOSTIC
  (AD).
- V1 major-axis r½: NOT DIAGNOSTIC (NO LEVER). This is a sub-label change only: at the larger radius no HI set reaches r½
  in DDO 210 or DDO 216, so switch 2 cannot be evaluated.
- V5 (no gas) raises E★ to +0.02 / −0.54 / +0.13 / +0.19. Still no dwarf is > 2σ.
- V6 lowers the WLM switch to 0.027 dex.

**INFO** (not in the criteria; no class weight): with SPARC's own disc baryons, WLM gives log g_bar −11.21 (vs the record's
spherical −11.12) and E_HI −0.145 (vs −0.147). The baryon geometry does not matter at r½.

## Controls

| control | result |
|---|---|
| K1 record excess (Aquarius) | CFG874 primary −0.04408 / −0.08229 and CFG860 zero-gas +0.13177 / +0.09265 reproduced, max diff 0 |
| K2 | WLM, IC 1613 and Pegasus dIrr have **no stored stellar excess** in the record: CFG828/852/860/874/880/931 excluded them as the rotating / gas-rich set. Nothing to reproduce. This lane is the first to compute it |
| K3 SPARC residual, UGCA 444 | CFG931 A1-3 cells +0.19659 (3 pts) / −0.01555 (7 pts) canonical, +0.15704 / −0.05366 alt, max diff 0 |
| K4 parse | Oh V(R_max) vs table 2: 37.35/37.3, 16.95/16.9, 12.02/12.0, 18.91/18.9; Iorio V_c² = V_r² + V_a² to 0.008 km/s |
| K5 identity (by construction) | E★ − E_HI = log10(3σ²/V_c²) to 9.7e-17 |
| MUTATE `hi` (+0.37 dex on all HI) | **Not applicable as a flip.** The main core is NO LEVER, not TRACER, so there is no stellar excess for the HI plant to match. The plant does register: E_HI +0.37 in every dwarf and D̄ +0.047 → −0.323 |
| MUTATE `plant_system` (E★ = E_HI = +0.37, real errors) | core **SYSTEM PROPERTY** in 4/4 readings (4 usable, SYSTEM count 4): BITES |
| MUTATE `plant_tracer` (E★ = +0.37, E_HI = 0) | core **TRACER PROPERTY** in 4/4 readings (TRACER count 4): BITES |

## Caveats

- **N = 4: a pointer, not a verdict.** These are gas-rich, star-forming, rotating dIrrs at g_bar ≈ 10^−11.7 to 10^−11.1. They
  are not the faint dSphs below 10^−12 that carry the +0.37 dex excess (CFG828: the excess lives below SPARC's floor). The
  lane holds the system fixed only where there is no excess to attribute.
- **Stellar rotation is not treated** (none on disk; the record never applied it). WLM's stars rotate. A v_rms term would
  raise E★ and Δ for WLM.
- **Υ_V = 2 is the dSph convention.** A lower V-band M/L, plausible for star-forming dIrrs, raises E★ and E_HI by the same
  amount and leaves Δ unchanged. IC 1613 sits 0.6 dex BELOW the law in both tracers at r½. That is a baryon-side or law-side
  question this lane does not address.
- **DDO 216:** Oh and Iorio differ by 0.22 dex at r½, and Iorio's scenario 2 does not reach r½. The Oh distance (1.1 Mpc)
  differs from LVD's (0.887 Mpc); radii are rescaled and velocities are not.
- **EFE:** none applied. IC 1613 and Pegasus dIrr lie 511 and 457 kpc from M31. An AQUAL external field changes the law
  prediction for both tracers equally, so Δ is unaffected.
- **One post-freeze implementation choice, disclosed.** The frozen "a class change marks FRAGILE" is implemented as a change
  of class without its sub-label (the CFG931 convention). This was decided after the first run showed V1's sub-label move
  from AD to NO LEVER. Either way the class is NOT DIAGNOSTIC.
- Spherical potential assumed for g_HI = V_c²/r. The SPARC-disc INFO line shows this matters < 0.01 dex for WLM at r½.

## Files and hashes

- `FROZEN_CRITERIA.md` (5ec3dc16a), `cfg966.py`, `cfg966.out`, `cfg966_results.json`, `cfg966_MUTATE_{hi,plant_system,plant_tracer}.out`,
  `cfg966_results_MUTATE_{hi,plant_system,plant_tracer}.json`.
- **Inputs (sha256, read-only):**
  - `real_research/data/dsph/lvd_dwarf_local_field.csv` d9ea1a0cf93e2eb1e7f3ed29590211a310c6c6065f064c7dd158793de1b285db;
  - `campaign_fresh_gravity/CFG442_a0_rung_expansion/data/oh15_rotdmbar.dat` 1ce3e9ee850b0a25c5f97fa36db3b0705fb558979f1e5df77eea71c3c56efe4c;
  - `oh15_table2.dat` cc8ab9e5351d60b5ee017a61d0d6a1fa42d0d85a278a6c4ea136cfd53f940efb;
  - `oh15_table1.dat` 4dc9f3727818062ea1e424e10dcfedf385af5723c79ff3b213702cc39d96b3f4;
  - `campaign_fresh_gravity/CFG449_a0_rung_iorio_edd/data/iorio17_finalrot.zip` d4c456c65801f65742a6c5b2b377cbd7c05b30db1acca75523554d0b98ce2285;
  - `real_research/data/sparc_data/UGCA444_rotmod.dat` 75814d6f80287edb44afdb4aa7ffb174eb8617ab9a7c2b073fd1eab3a9b03787;
  - `real_research/data/SPARC_Lelli2016c.mrt` 5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243;
  - the LVD MW/M31 files and the CFG874/860/931 result JSONs (all checksums are printed in `cfg966.out`).
- `SPARC_table.txt` (a saved 404 page) is never read.
