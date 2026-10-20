# CFG922: is the cluster-core excess a baryon-census artefact? EXCESS STANDS (both footings, both kernels; frozen and under the post-hoc census amendment A1)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in a9d0669c5 before any script or number. Block CFG920–929 (LEDGER row 663).
- **Label:** DATA RE-CHECK of the ×1.8 core excess (CFG686/687), per the rule that a failure needs a mechanism AND a data
  re-check. No new posit.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 are kept apart. Kernel nu_s (g_N = g²/(g + a0)) is primary and
  nu_mono is the bracket. Raw data and framework-native models only. The extra mass is cold energy, not a particle. Not
  "theory closed".

## Answer
No baryon component that is on disk, or bracketed from on-disk data, comes close to the mass the MID excess needs. To bring
eRASS1 A_MID to 1, the law needs about **2.0–2.4 × 10¹³ M☉ of extra concentrated baryons inside R = 0.5 Mpc** (median per
cluster). That is about **2× the hot gas there** (λ = 2.24 canonical / 1.84 alt × M_gas,cyl), and **22–32× all measured stars**
(the A1 upper end). Any baryon fix that does remove MID also breaks the outer agreement: a concentrated extra pushes OUTER to
0.78 / 0.75 (Z −3.2 / −3.9), and a whole-profile gas rescale pushes it to 0.54 (Z −9.9). Under the law, the census cannot
reconcile MID and OUTER at once. The measured stars are also **fewer** than the f* = 0.20 the scoring assumed, so the measured
census makes the excess **larger**: 2.09 / 1.91, against 1.91 / 1.75 in the baseline.

## Per-component classes (eRASS1 318, nu_s; canonical | alt). Needed value vs the bracket's upper end

| # | component | needed (frozen census) | needed (A1 census) | bracket upper end (source) | class (frozen = A1) |
|---|---|---|---|---|---|
| 1a | BCG + member stars | k = 68.2 / 56.3 × S_up | 32.1 / 26.6 × S_up (3.1e13 / 2.5e13 M☉ vs S_up 9.5e11) | k = 1 (KiDS DR4 bright + LePhare census, §4 of the criteria) | **CANNOT** |
| 1b | ICL / BCG envelope | 56.7 / 46.7 × S_up | 26.7 / 22.0 × S_up | no ICL table on disk | **NOT TESTABLE** (needs > 10 × S_up) |
| 2a | hot-gas normalisation + shape | m = 3.71 / 3.24 | 3.68 / 3.21 | ρ_84 = 1.50 (eRASS1 vs deprojected Chandra/XMM: N 68, median 1.08, 16–84% 0.73–1.50) | **CANNOT** (lenient Z = 2: STRAINED → FRAGILE) |
| 2b | X-COP radius convention | — | — | reused from CFG450: RADIUS is R/R500; CFG686/687 never read X-COP | **CANNOT** (no lever) |
| 2c | hydrostatic bias | b ∈ [0, 0.4] only raises A_MID (2.089 → 2.101) | same sign | X-ray gas mass does not use HSE; b enters only via r_c | **CANNOT** (wrong sign) |
| 2d | clumping | C = 2 raises A_MID to 2.51 / 2.30 | same | C ≥ 1 by definition | **CANNOT** (wrong sign) |
| 2e | Eddington bias (CFG817, reused) | corrections 1.00 / 0.90 / 0.92 raise A_MID to 2.17 / 1.99 | same | CFG817 credible corrections | **CANNOT** (wrong sign) |
| 2f | β-model shape (CFG687, reused) | best stored cell 1.72 / 1.58 vs 1.91 / 1.75 | — | CFG687's 27 cells | **CANNOT** (< half removed) |
| 3a | cold atomic gas | h = 345 / 285 × (f_HI,95 · S_up) | 161 / 133 | f_HI,95 = 0.196 (xGASS log M* ≥ 11, N 168) | **CANNOT** |
| 3b | cold molecular gas (BCG) | 56.9 / 46.9 × S_up | 26.8 / 22.1 × S_up | no table on disk | **NOT TESTABLE** (needs > 10 × S_up) |
| 4 | stellar M/L, IMF | α = 170 / 140 | 72 / 60 | α_max = 3.78 (95th percentile of 1/Fc, SLACS Auger+2009, N 70; median 2.53; Salpeter/Chabrier 1.78) | **CANNOT** |

- **Overall (frozen rule): EXCESS STANDS** on both footings.
  - Every testable component is CANNOT.
  - The combined upper-end corner (gas × 1.50, stars α_max × S_up, HI at f_HI,95) still leaves MID 1.58 ± 0.10 / 1.46 ± 0.09
    (Z +5.9 / +5.0). Under A1 it leaves 1.49 / 1.37 (Z +5.2 / +4.3).
  - The two untestable components need k_ICL = 56.7 / 46.7 and k_H2 = 56.9 / 46.9 (A1: 26.7 / 22.0 and 26.8 / 22.1), all above
    the declared ×10 scale.
- **Agreement:** nu_mono gives the same overall class (not kernel-fragile), and A1 changes no class.
- **Central re-scored census** (gas × ρ_med 1.08, measured stars, median HI): MID 2.000 ± 0.124 / 1.835 ± 0.114 (A1: 1.976 /
  1.814), OUTER 1.06 / 0.97.
- **ACCEPT 8 (reported, no class weight).** Its own MID excess is 1.69 / 1.56, under 2σ.
  - Same classes, except 2a is STRAINED: m = 2.75 / 2.47 against 1.50. At that m, OUTER falls to 0.62 (Z −2.6), so the joint
    check fails.
- **Supplementary checks:**
  - X-COP's own total stellar profiles (Ghizzardi+2020) give M*/M_gas(<0.5 Mpc) = 0.06–0.10 (max upper end 0.104). The needed
    ratio is ≈ 2.27 / 1.88, i.e. ×22 / ×18 above.
  - BUDHIES A963: HI within 0.5 Mpc is 2.7e9 M☉, which is 1.3e-4 of its gas.

## Controls
- **K 5/5 + K0 PASS** (`cfg922_K.out`):
  - **K0, units:** eRASS1 MGAS500 is in 1e11 M☉ and R500 in kpc; X-COP RADIUS is R/R500; M_NFW(1)/M500 = 0.998–1.002.
  - **K1, CFG687:** law max rel 0.0; A_MID 1.9102 ± 0.1186 / 1.7536 ± 0.1089 exactly; vectorised engine vs exec'd law 4.5e-14.
  - **K2, CFG686:** preds 5.9e-14; MID 1.6960 ± 0.3534 / 1.5698 ± 0.3358, replaying its shared bootstrap sequence.
  - **K3, CFG916/726 nu_s:** eRASS1 MID 1.9068 ± 0.1184 / 1.7510 ± 0.1087 and ACCEPT 1.6862 / 1.5622; max diff 4e-15.
  - **K4:** the census code with CFG652's recipe reproduces its 148 stored M_cond/M_bcg exactly.
  - **K5:** record values read (CFG817, CFG450, CFG687 brackets).
- **MUTATE** (`cfg922_MUTATE.out`):
  - **M2:** gas × 1.5 recovered as 1.50000. **BITES.**
  - **M3, null:** A_MID = 1 to 1e-12; knobs 0 / 1. **PASS.**
  - **M4:** a planted 1e12 M☉ galaxy is recovered to 2e-16; 318 random positions give mean net −2.6e9 ± 1.7e9. **BITES.**
  - **M5:** n_e × 2 doubles all 63 ratios exactly. **BITES.**
  - **M1, as frozen: FAILED on its noisy leg.**
    - The noiseless leg recovers k = 4.0000 exactly.
    - The injection (4 × S_up) moves A_MID only to 1.106, far below the shear noise. The noisy recovery gives 1.09 / 1.30
      against the 25% tolerance, about −1σ given the shallow dA/dk.
    - This is a mis-sized control, not a pipeline fault. But it is a frozen failure, and it is recorded as one.
  - **M1b (post hoc, see below):** injecting 2.0 × M_gas,cyl gives A_MID 1.98. It is recovered as 2.0000 noiseless and
    1.817 / 1.829 with noise. **BITES.**

## Post-hoc items and disclosures (all dated 2026-10-20; none changes a class)
1. **M1b added.** It runs after the frozen M1 noisy leg failed for lack of power (above). The frozen failure stands.
2. **Census amendment A1** (`CFG922_AMEND=A1`; outputs `cfg922_A1.out`, `cfg922_results_A1.json`, `cfg922_census_A1.json`).
   After the frozen main run, the KiDS census turned out to be biased low, for three reasons:
   - **Aperture masses.** LePhare masses come from GAaP aperture photometry. For example, a z = 0.25 BCG with r_AUTO = 17.86
     gets log M = 10.85. Sample median AUTO − GAaP(rebuilt) is −0.46 mag (16–84%: −0.67 to −0.30), and larger for bright and
     nearby galaxies.
   - **Masked galaxies.** The CFG652 recipe drops them from the central estimate.
   - **Footprint gaps.** 33 of 318 apertures have coverage < 0.5.

   A1 makes three changes:
   - It rescales each mass to total flux, using a GAaP r magnitude rebuilt from the catalogue's own M_abs + DM + K
     (LePhare-default H0 70 / Ωm 0.3 bookkeeping). The correction only brightens: the central is capped at ×2.5, the upper is
     uncapped.
   - It keeps masked galaxies.
   - For clusters that cannot be measured, it uses the measured clusters' median (central) and 84th-percentile (upper)
     S/M_gas,cyl ratio. Partly covered apertures are divided by their coverage.

   Effect: S_up rises from 3.8e11 to 9.5e11 and S_cen from 9.8e10 to 3.5e11 (medians). Every class and the overall are
   unchanged. The rebuild is approximate: for bright galaxies at z > 0.25 it gives −1.6 to −2.9 mag, which may include
   envelope light. The upper end uses it uncapped, which is generous.
3. **The low-z empirical completeness check is not understood.** For z < 0.12 clusters, the fraction of member mass above
   10^10.5 is 0.016 (frozen) and 0.092 (A1), far below any Schechter shape. The aperture-limited masses of nearby large
   galaxies are the likely cause. It carries no class weight, but it means the declared completeness factors are not
   validated.
4. **Implementation (no number moved):**
   - Chunked FITS column reads (identical to astropy on every column) and projection chunking, to keep each process under
     1 GB. Peak RSS was 0.92–0.98 GB, including file pages; footprint 0.29–0.40 GB.
   - `coverage` and `n_ap_allz` fields added to the census output.
   - An X-COP cross-bracket print line.
   - The frozen main run was re-run after a debug session truncated `cfg922.out`. The new `cfg922_results.json` is identical
     to the first run's: 0 of 1646 values differ.
5. **Gas cross-match representativeness.** The 68 matched clusters have median Mgas500 7.6e13 M☉, against 1.2e13 for the 318.
   There is no ρ trend with mass (Spearman 0.02, p 0.90), and the 8 matches below 3e13 have median ρ 0.79. Post-hoc
   diagnostic, no class weight.

## What is and is not established
- **Established, on the record's own data:**
  - The ×1.8 core excess is not removed by any on-disk baryon component or bracket:
    - stars (KiDS census, X-COP profiles);
    - IMF (SLACS lensing bound);
    - hot-gas calibration (Chandra/XMM cross-match);
    - hydrostatic bias, clumping and selection bias, which all move the wrong way;
    - the β-shape bracket (CFG687);
    - atomic gas (xGASS, BUDHIES).
  - The excess needs about twice the core hot gas in extra concentrated mass, and if that mass were baryons the law would then
    overshoot the outer shear.
  - So the excess **stands** as a property of the extra (cold-energy) mass, not of the census.
- **Not established:**
  - The ICL and BCG molecular gas are NOT TESTABLE on disk. They would have to exceed all measured stars 22–57×.
  - The gas cross-calibration is from massive clusters only.
  - 2a is FRAGILE under the lenient target.
  - The KiDS census rests on a rebuilt total-flux correction (A1).
- **Public tables that would decide the untestable rows (not on disk):**
  - ICL: Kluge et al. 2020 (ApJS 247, 43; BCG+ICL profiles of 170 local clusters); DES Y1 stacked ICL (Zhang et al. 2019).
  - BCG molecular gas: Edge 2001 (MNRAS 328, 762); Pulido et al. 2018 (ApJ 853, 177).
  - Total-flux stellar masses: the KiDS bright-sample GAaP/AUTO columns of the full release.
  - Low-mass gas profiles: deprojected XMM group samples such as X-GAP.
- κ is not derived; this is not "theory closed"; nothing here says the data favour the framework.

## Files and re-run (from this directory, one at a time, OMP_NUM_THREADS=1, nice 10)
| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (a9d0669c5) |
| `cfg922.py` | everything (K, MUTATE, main, A1) |
| `cfg922_K.out`, `cfg922_K.json` | `CFG922_MODE=K python3 cfg922.py` |
| `cfg922_MUTATE.out`, `cfg922_results_MUTATE.json` | `CFG922_MUTATE=1 python3 cfg922.py` |
| `cfg922.out`, `cfg922_results.json`, `cfg922_census.json` | `python3 cfg922.py` (frozen main, about 3 min) |
| `cfg922_A1.out`, `cfg922_results_A1.json`, `cfg922_census_A1.json` | `CFG922_AMEND=A1 python3 cfg922.py` (post hoc) |

- **Read-only inputs:**
  - lane files: CFG686 (exec'd slices of `cfg686_shear.py`; no KiDS shear columns loaded), CFG687 (`law()` slice,
    `cfg687_percluster.npz`, results), CFG916, CFG817, CFG450 and CFG652 results;
  - external data: `cfg726_work` arrays, the eRASS1 tsv and FITS units, the ACCEPT profiles, X-COP gas and stellar profiles,
    the KiDS DR4 bright sample + LePhare, SLACS Auger+2009, xGASS, BUDHIES.
- Nothing was downloaded. No other lane was edited. Every run used one core beside the live 1024³ job.

κ = ½ fitted; footings never pooled; cold energy mass still required; not theory closed.
