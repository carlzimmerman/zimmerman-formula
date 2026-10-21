# CFG931 AMENDMENT A2 (POST HOC, 2026-10-20, AFTER the main run): inventory correction (LITTLE THINGS is on disk) and one labelled INFO analysis

Frozen criteria: cad92ca1c. Amendment A1: 165bb5c71. Written AFTER the K, MUTATE and main runs of `cfg931.py` (whose classes
stand unchanged), and BEFORE any LITTLE THINGS residual was computed.

## A2-1. The frozen inventory was wrong about LITTLE THINGS

Criteria section 3 says "No LITTLE THINGS, SHIELD, FIGGS or Leo P kinematics are on disk". **That is false for LITTLE
THINGS.** My targeted listings covered `real_research/data` and `_external_data`, not the lane data directories. After the main
run, the memory index pointed to CFG442/CFG449, and their data directories hold (owner-approved fetches, 2026-10-06/07, with
FETCH_LOGs):
- `CFG442_a0_rung_expansion/data/`: **Oh+2015** (VizieR J/AJ/149/180): 26 asymmetric-drift-corrected rotation curves (scaled,
  `oh15_rotdmbar.dat`), table2 with R_max, V(R_max), M_gas, M*_K, M*_SED; **Hunter+2012** (J/AJ/144/134) table1.
- `CFG449_a0_rung_iorio_edd/data/iorio17_finalrot.zip`: **Iorio+2017**, 17 LITTLE THINGS curves (V_c asymmetric-drift
  corrected, Σ_HI), no mass models.
- Neither reduction has a tabulated per-radius baryonic decomposition (CFG442 digitised Oh+2015 figure paths; CFG449's Iorio
  route failed its integrator test K0b).

**A known method offset (record):** both LITTLE THINGS reductions FAILED the overlap control against SPARC on the same dwarfs
(CFG442 C2: Oh+2015 a0 +0.196 dex; CFG449: Iorio+2017 +0.16 dex; DDO 168 up to +0.49). In the deep regime that is about
+0.08–0.10 dex in g_obs. LITTLE THINGS and SPARC rotators are therefore never pooled here.

**Outcome-blind count (done before writing this; table2 M*_SED, M_gas and R_max only, no velocity used).** One point per
galaxy at R_max, g_bar = G(M_gas + M*_SED)/R_max²:
- M*_SED < 1e7: 5 galaxies (DDO 210 6.0e5, CVn I dwA 4.9e6, UGC 8508 7.7e6, DDO 154 8.3e6, DDO 53 9.7e6).
- Of these, g_bar(R_max) < 10^−11.5: **4** (CVn I dwA −12.15, UGC 8508 −12.10, DDO 154 −12.03, DDO 210 −11.54).
- Four galaxies (DDO 43, DDO 46, DDO 47, F564-V3) have no M* in table2.
- M* conventions disagree at the split: DDO 154 is 8.3e6 by Oh+2015 SED but 2.6e7 by SPARC's 0.5 L[3.6]; WLM (= SPARC's
  UGCA 444) is 1.6e7 by SED but 6.0e6 by SPARC.

**Consequence for the frozen class:** the primary split needs N_i ≥ 5 galaxies. LITTLE THINGS supplies at most 4 (and they
cannot be pooled with SPARC, which supplies 0). **The lane class, NOT DIAGNOSTIC (DATA), would not change** with the on-disk
LITTLE THINGS sample under the frozen rules. The corrected inventory replaces section 3's sentence in the README.

## A2-2. POST-HOC INFO analysis (no class weight), defined here before any LITTLE THINGS residual

Script `cfg931_lt_info.py` → `cfg931_lt_info.out` / `cfg931_lt_info.json`. One core, seconds.

- **LITTLE THINGS single point (Oh+2015 table2):** g_obs = V(R_max)²/R_max (asymmetric-drift corrected); g_bar = G(M_gas +
  M*_SED)/R_max² (all tabulated baryons inside R_max, spherical); Δ = log10(g_obs/g_law), ν_e, both footings. Galaxies
  without M*_SED are left out. M_gas is used as tabulated.
- **Known biases, disclosed in advance:** the gas usually extends beyond R_max (g_bar too high, Δ too low, i.e. toward K);
  a thin disc pulls harder than a sphere of the same enclosed mass (the other way); the LITTLE THINGS curves sit above SPARC
  (Δ higher, i.e. toward E).
- **Printed:** for each split (1e7, 3e7, 1e8) and each 0.5-dex cell in [10^−12.5, 10^−11.0): the mean Δ and N of LITTLE
  THINGS M* < split, LITTLE THINGS M* ≥ split, and CFG880 dSphs M* < split; the per-galaxy list; within-LITTLE-THINGS
  differences d_K^LT = E(i) − E(ii) and d_E^LT = E(iii) − E(i) over cells holding all three groups (≥ 1 / ≥ 1 / ≥ 3; weights
  ∝ n_i), with system bootstraps (4000, rng 9313) and the 0.05 dex floor. No class is assigned.
- **Overlap rows (INFO):** for DDO 154 and DDO 168 (in SPARC Q ≤ 2) and WLM (= UGCA 444, SPARC points all fail the error
  cut), the LITTLE THINGS single-point Δ next to the SPARC Δ at the nearest radius to R_max (WLM without the cut).
- **K-check inside the script:** the CFG880 dSph cell means at split 1e7 reproduce the main run's printed values (+0.318 in
  [−12.5, −12), +0.216 in [−12, −11.5), canonical) to 1e-3.

Nothing here changes a frozen rule, the main run, or the lane class.

κ = ½ FITTED; footings never pooled; not theory closed.
