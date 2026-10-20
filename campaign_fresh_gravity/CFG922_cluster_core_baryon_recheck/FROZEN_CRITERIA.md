# CFG922: is the cluster-core excess a baryon-census artefact? (FROZEN, before any script or new number)

- **Block:** CFG920–929 (LEDGER row 663 reserves CFG922 for "cluster-core excess baryon re-check"). Date 2026-10-20.
- **Label:** DATA RE-CHECK (census audit). The standing rule says a failure needs a mechanism AND a data re-check; this lane is
  the data re-check of the ×1.8 core excess (CFG686/687). It adds no new posit.
- **Settings:** κ = ½ FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Extra mass is "cold
  energy"; no particle species. Raw data, framework-native only: no HMcode, BAHAMAS, ΛCDM mass function or halo template
  enters any verdict. Not "theory closed". Nothing here may say the data favour the framework.

## 1. What I read before freezing (targeted, disclosed)
- READMEs (and criteria where noted): CFG450, CFG686 (+criteria, `cfg686_shear.py`), CFG687 (+criteria, `cfg687_stack.py`),
  CFG726, CFG727, CFG808 (+criteria), CFG809, CFG810, CFG811, CFG812, CFG813 (README + criteria lines on M_cond), CFG816,
  CFG817, CFG688, CFG916 (README; stored M-test A values in `cfg916_results.json`), CFG432, CFG656 (head), CFG652 (README
  lines on M_cond; the M_cond recipe in `cfg652_test.py` lines 70–112), THEORY_CANONICAL_2026-10-18.md (lines 1–50 and the
  cluster lines).
- Code: `CFG4_common.py` (A0, nu_mono), `cfg726.py` lines 50–70 (nu_s), the CFG450 data paths.
- Data headers / first rows only: eRASS1 main tsv (first 5 rows) and `erass1cl_primary_v3.2.fits` column units; X-COP
  `A1795`/`A2142` `*_mstar.fits` and `A1795_fgas_profile.fits` headers and first/last rows; ACCEPT `all_profiles.dat` header
  and the first 1E0657 rows, `table1.tsv` first rows; the CLASH Tian+2020 RAR file (first rows; not used); KiDS bright-sample
  column names (no values); xGASS readme; BUDHIES ReadMe; SLACS Auger+2009 column list and Auger+2010 `T_ml_fits.tex`.
- `cfg726_work/erass.npy` structure (first cluster's stored arrays printed).

## 2. Numbers seen before freezing (disclosed)
- Stored band amplitudes: CFG687 MID 1.910 ± 0.119 / 1.754 ± 0.109, OUTER 1.012 / 0.927 (nu_mono); CFG686 MID 1.696 ± 0.353 /
  1.570 ± 0.336; CFG916 LR-c (= plain law, nu_s) eRASS1 MID 1.9068 ± 0.1184 / 1.7510 ± 0.1087, ACCEPT 1.6862 ± 0.3563 /
  1.5622 ± 0.3309; CFG727/809/813/816/817 rows as in their READMEs (e.g. CFG813 λ-based f* median 0.032; CFG817 credible
  Eddington corrections 1.00 / 0.90 / 0.92 by tercile).
- X-COP A1795: M*(<1.58 R500) = 5.8e12 M☉, M_gas(<1.6 R500) = 9.6e13 M☉ (printed rows). CFG432: X-COP hydrostatic M_u/M_gas
  ≈ 10 at 0.1 R500.
- **Hand estimate (made before freezing, disclosed):** at 0.5–1.2 Mpc the eRASS1 baryons sit deep below a0 (g_bar/a0 ~ 0.02),
  where the law's lensing mass is M_L(<r) ≈ r √(a0 M_b(<r)/G). Removing A_MID ≈ 1.9 therefore needs roughly A² ≈ 3–3.6 × the
  baryons enclosed near 0.8 Mpc, i.e. an extra of order 2–3 M_gas(<0.8 Mpc). Typical BCG masses (~1e12 M☉) are far below that.
  This expectation is why the rules below take generous upper ends: they protect against over-claiming EXCESS STANDS.
- Not computed before freezing: the KiDS bright-sample census, the eRASS1–ACCEPT/X-COP gas cross-match, the SLACS IMF
  bound, the xGASS HI bound, BUDHIES A963, and every A value under a modified census.

## 3. The excess and the samples
- **Core excess** = A_MID = Σ W·ΔΣ_obs / Σ W·ΔΣ_model over the MID band (R = 0.556, 0.808, 1.175 Mpc; CFG686 bins 3–5), with
  CFG687's per-cluster ΔΣ_obs, weights and 30-patch RA jackknife (eRASS1) or CFG686's bootstrap (ACCEPT). OUTER = bins 6–7.
  Z = (A − 1)/σ.
- **Decisive sample:** the 318 eRASS1 clusters (`cfg687_percluster.npz`; Mgas500, R500, z, ra, dec, D, E). **Reported
  sample:** the 8 ACCEPT clusters (`cfg686_results.json`); its own MID excess is 1.97σ, so it cannot decide alone.
- **Kernels:** nu_s (g_N = g²/(g + a0), the law as stated; CFG726/916 primary) is primary; nu_mono (CFG687's kernel) is the
  bracket. Never pooled. Classes are decided on nu_s; a different nu_mono class marks the lane FRAGILE (kernel).
- **Core aperture:** projected cylinder R ≤ 0.5 Mpc (physical; BAO-raw distances of CFG686). 3D r ≤ 0.5 Mpc for gas
  cross-calibration (the gas profiles are 3D). All "needed mass" figures are quoted inside this aperture.
- **Baseline model (K):** CFG687's law(): β-model gas (β = 2/3, r_c = 0.15 R500, normalised to Mgas500 at R500, cut at 3 Mpc),
  stars f* = 0.20 × M_gas(<r). ACCEPT: CFG686's law_dsigma (β_out shift 0, f* = 0.20).

## 4. The measured census (new; per cluster, on disk only)
**Stars, BCG + member galaxies** from the KiDS DR4 bright sample + LePhare (`real_research/data/lensing_rar/`, the files
CFG652 used; r ≤ 20, 1,239,422 rows), extending CFG652's recipe with physical apertures (no R500):
- Galaxies with log M* > 5 and |z_ANNz2 − z_cl| ≤ 0.05(1 + z_cl); angular separations by unit-vector chords (not
  ra·cos dec, which distorts at KiDS-South declinations).
- Aperture R ≤ 0.5 Mpc; background from the annulus 2.5–5.0 Mpc scaled by area; BCG = the most massive galaxy within 0.15 Mpc.
- Central S_cen: unmasked galaxies, MASS_MED; net = aperture − background, floored at the BCG (CFG652).
- Upper S_up: all galaxies (masked included), MASS_SUP; net + 2σ_bkg, with σ²_bkg = Σ_annulus m² × (A_ap/A_ann).
- Completeness (members only, never the BCG): c(z) = 1/F(>M_lim(z)), M_lim(z) = median log MASS_MED of bright galaxies with
  19.5 ≤ MAG_AUTO_CALIB ≤ 20.0 and |z_ANNz2 − z| ≤ 0.02. Schechter mass fraction F with log M_char = 11.0: central α = −1.0
  (F = e^−x), upper α = −1.5 (F = erfc √x). These are declared conventions (literature shapes, quoted from memory, not
  measurements); α = −1.5 is chosen to be generous. A low-z (z < 0.12) empirical check is reported, no class weight.
- IMF of the LePhare masses: Chabrier per the catalogue paper (not in the FITS header on disk; provisional).
- Radial placement: BCG as a Hernquist sphere, R_e = 15 kpc (sensitivity R_e = 50 kpc reported); members = (S − BCG)
  distributed ∝ the cluster's gas profile, normalised so their projected mass inside 0.5 Mpc equals S − BCG.
- **Census model:** M_b = gas (pipeline) + S_cen stars (replaces f* = 0.20). Its A_MID is reported as the re-scored excess.

## 5. Components, brackets and rules (each solved for the value that brings A_MID to 1)
Unless stated, tests start from the census model; the solved parameter is monotone and is found by bracketed root finding
(up to ×1000; beyond that "needed > 1000" is reported as a lower limit).

| # | component | knob (needed value solves A_MID = 1) | bracket upper end (source) |
|---|---|---|---|
| 1a | BCG + member stars | k: stars = k × S_up | k ≤ 1 (S_up itself; KiDS bright LePhare, §4) |
| 1b | ICL / diffuse BCG envelope | extra = k_ICL × S_up, Hernquist R_e = 100 kpc | NOT TESTABLE (no ICL table on disk) |
| 2a | hot-gas normalisation + shape inside the aperture | gas × m (whole profile); core-only variant reported | ρ_hi = 84th percentile of ρ = M_gas,meas(<r_cmp)/M_gas,pipe(<r_cmp) over eRASS1 clusters matched to ACCEPT (Chandra n_e) or X-COP (MGAS); r_cmp = min(0.5 Mpc, data edge) ≥ 0.2 Mpc; match ≤ 3′ and Δz ≤ 0.02; N ≥ 5 or NOT TESTABLE |
| 2b | X-COP radius convention | none | reuse CFG450 (RADIUS is R/R500; not a bug); CFG686/687 never read X-COP |
| 2c | hydrostatic bias | r_c = 0.15 R500 (1 − b)^(−1/3) at fixed Mgas500 | b ∈ [0, 0.4]; the gas mass is from X-ray emission, so b enters only through the aperture scaling |
| 2d | clumping | gas × C^(−1/2) | C ∈ [1, 2]; C ≥ 1 by definition (⟨n²⟩ ≥ ⟨n⟩²) |
| 2e | Eddington / selection bias on Mgas500 | gas × corr by gas tercile | reuse CFG817's credible corrections (1.00 / 0.90 / 0.92) |
| 2f | β-model shape bracket | — | reuse CFG687's stored 27 bracket cells per footing |
| 3a | cold atomic gas | extra = h × f_HI,95 × S_up, star template | h ≤ 1; f_HI,95 = 95th percentile of M_HI/M* for xGASS galaxies with log M* ≥ 11 (non-detections at their limits) |
| 3b | cold molecular gas (BCG cooling flows) | extra = k_H2 × S_up, BCG template | NOT TESTABLE (no table on disk) |
| 4 | stellar M/L / IMF | stars = α × S_cen | α_max = 95th percentile of 1/Fc over SLACS (Auger+2009 table on disk): stars cannot exceed the lensing mass inside R_Ein in any theory with a non-negative phantom |

- Supplementary, no class weight: BUDHIES A963 total HI within 0.5 Mpc (|Δv| ≤ 3000 km/s) over its gas mass; X-COP measured
  M*(<0.5 Mpc)/M_gas(<0.5 Mpc) (Ghizzardi+2020 profiles) next to the KiDS census of massive clusters; SLACS median
  Salpeter/Chabrier mass ratio.
- **Per-component class (multiplier knobs 1a, 2a, 3a, 4):** CAN EXPLAIN if needed ≤ bracket upper end; STRAINED if within
  ×1–2 of it; CANNOT if needed > 2 × upper end. Totals are compared (e.g. m_need vs ρ_hi), the lenient reading. If the census
  model has no excess, CAN EXPLAIN.
- **Sign-limited knobs (2c, 2d, 2e, 2f):** CAN EXPLAIN if a value inside the bracket gives A_MID ≤ 1; CANNOT if the most
  favourable value in the bracket removes less than half of (A_MID − 1) (or raises it); STRAINED otherwise.
- **Reuse:** 2b, 2e and 2f inherit their records; nothing there is redone, only re-scored where stated.
- **Always reported:** needed mass in M☉ inside 0.5 Mpc (median over clusters) next to the bracket; A_OUTER and Z_OUTER at the
  needed value (joint check); the lenient target Z_MID = +2 (a component whose class moves under it is FRAGILE).
- **Uniform-template needed mass:** an extra concentrated (BCG Hernquist) mass of λ × M_gas,cyl(<0.5 Mpc) per cluster; λ_need
  reported for both footings and kernels.

## 6. Overall class (eRASS1, nu_s, both footings must agree)
- **Central census:** gas × ρ_med, stars S_cen, HI f_HI,med × S_cen. **Corner:** gas × ρ_hi, stars α_max × S_up,
  HI f_HI,95 × S_up (sign-limited knobs at their neutral values, since they only lower the gas).
- **ARTEFACT LIKELY:** at least one testable component is CAN EXPLAIN on both footings with |Z_OUTER| < 2 at its needed value;
  or the central census gives Z_MID < 2 on both footings with |Z_OUTER| < 2.
- **EXCESS STANDS:** every testable component is CANNOT on both footings; the corner still gives Z_MID ≥ 2 on both footings;
  and the NOT TESTABLE components each need > 10 × S_up (k_ICL > 10, k_H2 > 10) on both footings. The ×10 is a declared
  plausibility scale: an unmeasured component ten times all measured stars would be a new baryon reservoir, not a census
  correction.
- **NOT DIAGNOSTIC:** anything else, including footing disagreement.
- Both outcomes are reported equally plainly.

## 7. Controls
- **K0 data units:** eRASS1 MGAS500 in 1e11 M☉ and R500 in kpc (FITS units); X-COP TUNIT1 = R/R500 in fgas and mstar files;
  CFG450 U2: M_NFW(RADIUS = 1) within 2% of the header M500 for the X-COP files read here.
- **K1 CFG687:** recomputed nu_mono law = stored PL (max rel < 1e-9); A_MID/A_OUTER ± σ canonical and alt = stored (< 1e-6).
- **K2 CFG686:** recomputed ACCEPT predictions = stored (max rel < 1e-9); bootstrap A_MID ± σ = stored (< 1e-6), replaying
  CFG686's shared random sequence.
- **K3 CFG916/726:** recomputed nu_s law = `cfg726_work` 'law|s|*' arrays (max rel < 1e-6); A_MID ± σ = CFG916's stored
  eRASS1 1.9068/1.7510 and ACCEPT 1.6862/1.5622 (< 1e-6).
- **K4 census code:** run with CFG652's recipe and metric on CFG652's stored group positions, it reproduces the stored
  M_cond and M_bcg (max rel < 1e-9).
- **K5 record values:** CFG817 corrections, CFG450 verdict, CFG687 bracket cells read from their files.
- A failed K voids the piece it guards (stated in the README); no silent fix.
- **MUTATE** (separate `_MUTATE` outputs; each arm must bite):
  - M1: mock ΔΣ from the census model plus a hidden concentrated mass of 4 × S_up per cluster. The pipeline must see an
    excess and recover k = 4 within 1% (noiseless), and within 25% with Gaussian noise drawn from the real errors (seed 922).
  - M2: mock with gas × 1.5. The solver must recover m = 1.500 within 1%.
  - M3 null: mock = census model. A_MID = 1 within 1e-9, and no knob may be needed.
  - M4: a planted 1e12 M☉ galaxy at each cluster centre raises S_cen by 1e12 within 1%. At 318 random KiDS positions the
    mean net member mass is within 3 standard errors of 0.
  - M5: ACCEPT n_e × 2 doubles every ρ (to 1e-9).

## 8. Machine and hygiene
- One process at a time, OMP_NUM_THREADS = 1, nice 10, each process < 1 GB, beside the live 1024³ job. Nothing downloaded.
- Outputs: `cfg922.py`; `cfg922_K.out`; `cfg922.out` and `cfg922_results.json`; `cfg922_MUTATE.out` and
  `cfg922_results_MUTATE.json`; `cfg922_census.json`.
- Any post-freeze change will be a dated, labelled amendment in the README.

κ = ½ fitted; footings never pooled; cold energy mass still required; not theory closed.
