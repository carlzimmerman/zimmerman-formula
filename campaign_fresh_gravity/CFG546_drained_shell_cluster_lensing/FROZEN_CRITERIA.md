# CFG546 FROZEN CRITERIA: the drained shell around settled halos in stacked lensing, and how to tell it from splashback

Committed alone, 2026-10-09, before any script of this lane exists, before any simulation profile of this lane is stacked, and before any DESI ΔΣ value is read.
- Read before this freeze: the committed CFG495 / CFG504 / CFG515 / CFG541 / CFG527 / CFG530 records; the column names and r_p bin edges of the DESI DR1 LRG ΔΣ FITS files (not the `ds` column); the DESI joint covariance (already read by CFG315); the header/info strings of `cfg526_LRcan_L200.npz` (engine bookkeeping, no profile).
- No downloads. κ = ½ is FITTED. The cold energy's MASS is still required; no particle species. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are scored separately and never pooled. Not "theory closed". Nothing here may be read as "the data favour the framework".

## The idea (owner-approved scoping, 2026-10-09)
Settled systems drain the cold energy of their surrounding reservoir. Stacked lensing around halos should therefore show a DEPLETED shell just outside the settled region. ΛCDM predicts smooth continued infall: a splashback steepening near r_sp ≈ 1–1.5 r_200m, then a smooth power-law outer (two-halo) profile (DK14).

**Known from the record (not re-derived here).** CFG495's proportional-draw engine gives, around clusters (log M_ta ≥ 14.2), an effective-density EXCESS of +5 to +20% at 0.25–1.1 r_ta and a DEFICIT of −4 to −10% at 1.3–2 r_ta (512³); the projected ΔΣ difference stays positive at every R ≥ 0.3 r_ta. So for clusters the drained shell is a change of shape near r_ta, not a ΔΣ deficit. THEORY_v1 rule R5 ("draw from the outer reservoir", CFG527/530) has replaced the proportional draw. The primary prediction of this lane is therefore R5's, measured here for the first time beyond r_ta; CFG495's is a reported variant.

## Step P: the prediction (simulation templates)
**Inputs (read-only, on disk).** `_external_data/cfg530_work/profiles/N512/cfg526_{LRcan,S0}_L200_rhog.npy` (R5 engine, canonical, 512³, L = 200 Mpc/h, seed 359; and the matched CFG411 S0 control, identical ICs per cfg530_s0reuse) and `profiles/N256/cfg526_{LRcan,LRalt,S0}_L200_rhog.npy` (256³, both footings). `rho_g` is the gravitating (lensing) density in units of the mean: particles plus the engine's source term.

**Centres.** The S0 candidate peaks `pk` of `cfg526_S0_L200.npz` (per resolution). For each, r_ta is recomputed from the S0 field as the largest radius whose mean enclosed density is ≥ Δ_ta = 11.806 (z = 0, CFG361 table), on a radial grid of 0.25 cells, from a sub-cube. Candidates inside r_ta of a heavier one are dropped. M_ta = Δ_ta ρ̄_m (4/3)π r_ta³ (Ω_m from the npz). Bins (Msun/h): **groups 13.2 ≤ log M_ta < 14.2**, **clusters log M_ta ≥ 14.2** (CFG495's bins). Resolution rule: a bin counts only if its median r_ta ≥ 5 cells.

**Templates.**
- **3D (primary):** rel(x) = ⟨ρ_g,F − ρ_g,S0⟩ / ⟨ρ_g,S0 − 1⟩ (ratio of stacked means) in x = r/r_ta bins of width 0.1 from 0 to 4.
- **2D (cross-check, reported):** full-box projections along the three axes, T2D(X) = ⟨ΔΣ_F − ΔΣ_S0⟩ / ⟨ΔΣ_S0⟩ in X = R/r_ta bins of 0.1 to 4.
- Template used in modelling: rel(x) set to 0 for x < 0.2 (mesh core; the one-halo nuisances absorb it) and for x > 4; smoothed by a lognormal r_ta scatter σ_ln r = 0.2 (stack mass spread).
- **Footings.** Canonical primary = 512³ canonical. No 512³ alt R5 run exists, so alt primary = the 256³ alt template × s_res, where s_res is the least-squares scale of the 512³ canonical template onto the 256³ canonical one over 0.2 ≤ x ≤ 3. Pure 256³ templates of both footings are reported.
- **Reported variant:** CFG495's committed proportional-draw templates (`cfg495_sim_analysis_results.json`: eff3d_minus_S0 / dS0_3d, x 0.05–2.95), both footings.

**Prediction declared from the templates (stated, not tuned):** the depletion depth D = −min over 1 ≤ x ≤ 3 of rel(x) (bin-smoothed over 3 bins), the excess E = max over 0.2 ≤ x ≤ 1 of rel(x), and x of the sign change. The drained shell is DEFINED to exist in the prediction iff D ≥ 0.02 at ≥ 3σ of the stacking error (bootstrap over centres, 200 draws). If it does not exist on a footing, that footing's forecast is reported but carries the label **NO DRAINED SHELL PREDICTED**.

## Step F: the forecast (frozen statistic)
**Baseline (ΛCDM, DK14) in 3D, comoving h-units:**
Δρ(r) = ρ_s exp{−(2/α)[(r/r_s)^α − 1]} [1 + (r/r_t)^β]^(−γ/β) + ρ̄_m b_e (r / 5r_200m)^(−s_e).
- Fiducial per dataset: M_200m and z_l from the dataset table below; c_200m from colossus `diemer19`; α = 0.155 + 0.0095 ν²; r_t = (1.9 − 0.18 ν) r_200m; β = 4, γ = 6; b_e = 1.0, s_e = 1.5; ρ_s normalised so M(<r_200m) of ρ̄_m + Δρ equals M_200m.
- r_ta of a profile = the radius where its mean enclosed density (ρ̄_m + Δρ) equals Δ_ta(z_l) ρ̄_m(z_l) (CFG361 table, linear interpolation). r_sp = the radius of the steepest logarithmic slope of ρ̄_m + Δρ.
- Projection: Σ(R) = 2∫₀^40 Δρ(√(R² + l²)) dl; ΔΣ = Σ̄(<R) − Σ(R); bin-averaged with area weights.
- Observation model: ΔΣ_obs = ΔΣ × (1 + m₀ + m₁ ln(R / 1 Mpc/h)).

**Drained-shell model:** Δρ_F = Δρ_θ × [1 + A rel(r / r_ta(θ))]. Prediction A = 1; null A = 0.

**Free parameters:** A, ln ρ_s, ln r_s, ln α, ln r_t, ln β, ln γ, b_e, s_e, m₀, m₁.
- Gaussian priors: ln α ± 0.6, ln β ± 0.2, ln γ ± 0.2 (the DK14 practice of More+16 / Chang+18); m₀ ± 0.03; m₁ ± 0.03 for cluster surveys and ± 1 (effectively free) for DESI (the release files are labelled "blindA" and the paper's blinding function is linear in ln R).
- r_t, b_e, s_e, ρ_s, r_s are free (flat). **Splashback is marginalised by freeing r_t (and β, γ).**

**Statistic.** Fisher matrix F = Jᵀ C⁻¹ J + priors, J by central differences at the fiducial (A = 0). σ_A = √(F⁻¹)_AA; **Z = 1/σ_A** (expected significance of the predicted amplitude).

**Separating the drained shell from splashback (frozen diagnostics).**
1. r_sp / r_ta of every fiducial is reported. The drained shell (x ≳ 1) and splashback (x ≈ 0.3–0.5 expected) sit at different radii in units of r_ta; that radial separation is the only lever.
2. Z_fixed / Z_marg: Z with r_t, β, γ held fixed against Z marginalised. The ratio is the cost of the splashback degeneracy.
3. corr(A, ln r_t) and corr(A, s_e) from F⁻¹.
4. **Apparent splashback shift (reported only):** the linear bias δθ = F_θθ⁻¹ Jᵀ C⁻¹ δΔΣ_template on ln r_t and on r_sp when the drained shell (A = 1) is fitted with the ΛCDM baseline alone.

**Shared systematics the statistic must see:** m₀, m₁ (shear calibration, photo-z, blinding slope); the halo-mass placement of the template (variants r_ta × 10^(±0.05), i.e. M × 10^(±0.15)); covariance × 1.3 (CFG315's s ≈ 1.2–1.4); LSS term × 2 (cluster–cluster correlation) for constructed covariances.

**Datasets.**
- **On disk:** DESI DR1 LRG1 (0.4 < z < 0.6) × {KiDS-1000 bins 4–5, DES-Y3 bin 4, HSC-Y3 bins 3–4} (the CFG315 conservative combinations, tomographic), joint analytic covariance `dscovcorr_kids1000desy3hscy3_desiy1lrg_pzwei.dat`; LRG2 (0.6–0.8) × HSC-Y3 3–4 reported. Primary range 0.5 ≤ r_p ≤ 30 h⁻¹ Mpc comoving (variants: 1.0–30; 0.5–80). Fiducial for the pre-data forecast: log M_200m = 13.4 Msun/h (U: recalled DESI-LRG HOD scale, provisional), group template. A group template stands in for a galaxy-selected LRG stack with ~10% satellites: label **GALAXY-SELECTED, NOT HALO-CENTRED**.
- **Not on disk, constructed covariances (shape noise + Limber LSS from camb halofit at z_l, + intrinsic halo-to-halo 25% per cluster with ln R correlation length 1), survey parameters (U: recalled, provisional, to be checked against the papers before any download):**

| ID | dataset | N_lens | z_l | log M_200m | n_eff (arcmin⁻²) | σ_e | z_s | published R range (U) |
|---|---|---|---|---|---|---|---|---|
| D1 | DES-Y1 redMaPPer λ ≥ 20 (McClintock+19; Chang+18) | 6500 | 0.40 | 14.3 | 6.0 | 0.27 | 0.75 | 0.03–30 Mpc |
| D2 | DES-Y3 redMaPPer λ ≥ 20 | 16000 | 0.42 | 14.3 | 5.6 | 0.26 | 0.75 | 0.03–30 Mpc |
| D3 | SDSS redMaPPer × SDSS shear (Simet+17) | 5500 | 0.24 | 14.3 | 1.2 | 0.36 | 0.40 | 0.1–30 Mpc |
| D4 | HSC-Y3 × CAMIRA / redMaPPer (Murata+19 class) | 1800 | 0.50 | 14.1 | 15 | 0.24 | 1.0 | 0.1–15 Mpc |
| D5 | KiDS-1000 × GAMA groups N_fof ≥ 5 (Viola+15; Dvornik+17) | 2400 | 0.20 | 13.6 | 6.2 | 0.27 | 0.65 | 0.02–2 Mpc |
| D6 | eRASS1 × DES/KiDS/HSC (Grandis+24) | 2200 | 0.30 | 14.4 | 6.0 | 0.26 | 0.75 | 0.5–3.2 Mpc |
| D7 | SPT × DES-Y3 (Bocquet+24) | 700 | 0.55 | 14.8 | 5.6 | 0.26 | 0.85 | 0.5–3.2 Mpc |
| D8 | ACT DR5 × DES-Y3 / HSC (Shin+21 class) | 1000 | 0.50 | 14.6 | 5.6 | 0.26 | 0.85 | 0.1–10 Mpc |

  Area does not enter: N_lens carries shape noise; the LSS term is per sight line / N_lens (×2 variant). Each is forecast on (a) its published range (U) and (b) an extended range 0.3–30 h⁻¹ Mpc comoving (what a re-measurement from the public shear catalogue could reach), 15 log bins. Clusters use the cluster template, D5 and DESI the group template. Euclid Q1: no tabulated stacked cluster profile is known (U); listed, not forecast.

## Step T: the test (only if adequate)
**Adequacy (frozen).** A dataset on disk is ADEQUATE iff Z_marg ≥ 3 on both footings with the primary template at its post-baseline-fit fiducial (the Fisher re-evaluated at the ΛCDM fit, which never involves A), AND the ΛCDM baseline fit passes G0: p(χ², dof) > 0.001.

**If adequate:** fit A with all nuisances free (priors as above), by least squares from the ΛCDM best fit; σ_A from the Hessian.
- **DEPLETION SEEN:** Â ≥ 2σ_A on both footings.
- **DEPLETION NOT SEEN:** Â ≤ 1 − 2σ_A on both footings (the predicted amplitude excluded at 2σ).
- **NOT DIAGNOSTIC:** otherwise.
- **Labels (attached, never replace the verdict):** NOT ROBUST if the per-footing verdict flips under {R range variants, each survey alone, r_ta × 10^±0.05, covariance × 1.3}; SPLASHBACK-DEGENERATE if |corr(A, ln r_t)| > 0.7; MODEL-INADEQUATE if G0 fails.
- **Data null (gate):** the same fit on the random-point signal `ds_r` must give |Â/σ_A| < 2, else label SYSTEMATIC.

**If not adequate,** the test is not run and the data vector is not fitted for A.

## Lane verdict (frozen)
- **TEST RUN (DEPLETION SEEN / NOT SEEN / NOT DIAGNOSTIC)** if an on-disk dataset is adequate.
- Otherwise **TEST NEEDS DOWNLOAD** with a ranked list if any candidate reaches Z_marg ≥ 3 on both footings (primary template; published or extended range, the range stated). 2 ≤ Z < 3 is listed as MARGINAL.
- **NOT POSSIBLE** if no candidate reaches Z_marg ≥ 2 on both footings, or if |corr(A, ln r_t)| > 0.9 for every candidate (splashback degeneracy unbreakable at current precision).
- Label **RESOLUTION-CONDITIONAL** if the ranking's Z ≥ 3 holds with the 512³-based template but Z < 2 with the 256³ template. Label **PREDICTION NOT ON R5** if only CFG495's variant gives Z ≥ 3.

## Controls and MUTATE
- **K1 (gate):** the S0 field's mean is 1 within 1e-5; mean(ρ_g,F) − mean(ρ_g,S0) within 1e-4 (mass conservation); large-scale (8 Mpc/h top-hat) correlation of F and S0 ≥ 0.95 (matched ICs).
- **K2 (gate):** the recomputed r_ta agrees with the npz `ron` within one coarse-grid step (factor 1.26) for ≥ 90% of kept centres.
- **K3 (reported):** projecting the 3D template on the S0 stack reproduces T2D within 3σ over 0.3–3 R/r_ta.
- **K4 (gate):** the projection code reproduces an analytic NFW ΔΣ to 1% at 0.1–10 R/r_s.
- **MUTATE-SIM (gate):** shuffled centres (uniform random, same r_ta list): |rel| averaged over 1–3 r_ta ≤ 10% of the halo-centred |rel| average there, or ≤ 0.005 absolute.
- **MUTATE-FORECAST (gate), per dataset family (one cluster dataset D2-extended and DESI):** 300 noise realisations from C around the fiducial with A = 0 injected → mean Â within 0.2 σ_A of 0 and the fraction |Â/σ_A| > 2 in 2–10%; with A = 1 injected → mean Â within 0.2 σ_A of 1 and the scatter of Â within 25% of the Fisher σ_A. Outputs `*_MUTATE.*`.

## Caveats stated before any number
- The templates are z = 0, 0.39 Mpc/h-mesh (512³) and 0.78 Mpc/h (256³) products; amplitudes may not be converged (CFG495: q mesh-limited). Applied in units of r_ta(z_l).
- The S0 control stands in for ΛCDM; DK14 with free r_t, β, γ, b_e, s_e is the ΛCDM baseline that is fitted.
- All non-disk survey parameters are recalled (U); every constructed forecast is provisional until the paper's tabulated errors are read.
- Constructed covariances ignore miscentring, boost and source-lens association beyond the R_min cuts.
