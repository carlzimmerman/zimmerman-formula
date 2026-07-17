# FROZEN — MaNGA DR17 anisotropy-proxy Stage-1 pre-registration

**Frozen at: 2026-07-17T00:21:52Z (UTC)** — written BEFORE any MaNGA data was downloaded to this
lane (remote HEAD checks only: dapall 146,030,400 B / drpall 75,360,960 B confirmed to exist).
No selection, estimator, proxy definition, or regression spec below may be changed after the
catalog is built; any post-hoc variation must be reported as a labelled VARIANT next to the
frozen primary, never in place of it.

**Framework under test (its own terms):** Carl Zimmerman's de Sitter–Unruh **MODIFIED INERTIA**;
own interpolation ν(y)=√(1+1/y), y=g_bar/a₀. **Both footings carried everywhere:**
canonical **a₀ = cH_Λ/Z = 9.36e-11 m/s²** (ρ_DE) and alt **a₀ = 1.13e-10 m/s²** (ρ_tot/cH₀).

**The forced prediction being staged (mi_closure_pin/CONSEQUENCES.md §1, A-2; mi_eta_selection/
SYNTHESIS.md §2):** **d(offset)/d(radial-velocity-anisotropy) > 0** — at matched baryonic
content, radially-anisotropic pressure-supported systems sit HOTTER (above) the framework RAR
than tangentially-anisotropic ones. η(β)-independent in SIGN (survived the 5-weighting flip
attack, Spearman +0.86…+1.0). **MG-with-the-same-ν predicts EXACTLY ZERO** anisotropy
dependence for isolated spherical systems. MG-impossible; not a₀-degenerate; not MOND-shared.
Derived 2026-07-16; never tested by anyone.

---

## 1. Data + sample selection (frozen)

**Inputs:** SDSS DR17 MaNGA DAPall (`dapall-v3_1_1-3.1.0.fits`, HDU `HYB10-MILESHC-MASTARSSP`)
crossmatched to drpall (`drpall-v3_1_1.fits`) on PLATEIFU. Expected ~10,010 DAP rows per DAPTYPE
HDU and ~11,273 drpall cube rows (validate; abort if grossly off).

**Quality gates (all required):**
- `DAPDONE == 1` and `DAPQUAL == 0` (clean DAP run, no critical flags)
- drpall `mngtarg1 > 0` (MaNGA main galaxy sample; excludes ancillary-only)
- `nsa_elpetro_mass > 0`, `nsa_elpetro_th50_r > 0`, `0.005 < nsa_z < 0.15`
- `SNR_MED >= 10` (median g-band S/N per DAPall)
- `STELLAR_SIGMA_1RE >= 70 km/s` — instrumental-resolution floor guard (MaNGA LSF σ_inst ≈ 70
  km/s; below this the dispersion and its aperture correction are unreliable). Stated cost:
  biases the sample to massive ETGs; acceptable for Stage 1, revisit in Stage 2 with per-spaxel
  sigmacorr.
- deduplicate on MANGAID (keep highest SNR_MED PLATEIFU).

**Pressure-supported (slow-rotator proxy) selection — inclination-agnostic by design:**
- global rotation-support proxy (DAPall-level): (V/σ)_glob ≡ [(STELLAR_VEL_HI_CLIP −
  STELLAR_VEL_LO_CLIP)/2] / STELLAR_SIGMA_1RE  (the clipped 2.5–97.5% stellar-velocity-field
  half-amplitude over the 1-Re dispersion).
- **PRIMARY cut: (V/σ)_glob < 0.4.**
- **VARIANT (reported alongside, never replacing the primary): (V/σ)_glob < 0.6.**
- No inclination cut: for pressure-supported systems the selection is inclination-agnostic
  (rotation contamination is what the cut itself removes; residual contamination is the stated
  caveat, §3).

## 2. The offset estimator δ (frozen)

Per galaxy:
- **Dynamical mass proxy:** M_dyn = K_v · σ_e² · R_e / G with **K_v = 5.0** (Cappellari et al.
  2006, ApJ 366, 1126 virial coefficient for M ≈ 5.0 σ_e² R_e/G with elliptical-aperture σ_e;
  K_v uncertainty is common-mode for the SLOPE test — it moves all δ by a constant, not the
  δ-vs-proxy slope). σ_e = STELLAR_SIGMA_1RE (km/s); R_e = physical radius from
  nsa_elpetro_th50_r (arcsec) × D_A(z) with flat ΛCDM **H0 = 70 km/s/Mpc, Ωm = 0.3** (frozen).
- **Baryonic mass:** M_bar = M* = nsa_elpetro_mass / h² with **h = 0.7** (NSA masses are in
  h⁻² M_sun; kcorrect, Chabrier-like IMF). Gas mass neglected for slow-rotator ETGs (stated;
  typically <few % of M*).
- **Framework prediction (its OWN law, never McGaugh's ν):** characteristic baryonic
  acceleration g_bar = G·(M_bar/2)/R_e² (half-mass inside R_e, spherical); y = g_bar/a₀;
  predicted dynamical boost ν(y) = √(1+1/y); predicted M_dyn^pred = ν(y) · M_bar.
- **THE OFFSET:** **δ ≡ log10(M_dyn) − log10(ν(y)·M_bar)**, computed at BOTH footings
  (δ_canon, δ_alt). MG-with-same-ν predicts δ independent of anisotropy; MI predicts
  dδ/d(radial anisotropy) > 0.

**M/L / IMF brackets (frozen):**
- Baseline: fixed NSA (Chabrier-like) M* — one δ per footing.
- **IMF bracket A (fixed heavy):** M* × 1.55 (Salpeter-like) for ALL galaxies — common-mode,
  slope-neutral by construction (control).
- **IMF bracket B (σ-dependent, the dangerous one):** Δlog M*(σ_e) = 0.30 · log10(σ_e/130
  km/s) + const (the Cappellari et al. 2012 / Treu et al. 2010-style trend of IMF mass-excess
  with σ). Direction statement, pre-registered: literature IMF gradients make M/L RISE with σ;
  if the anisotropy proxy correlates positively with σ_e, a fixed-IMF analysis inflates δ at
  high proxy values and can **FAKE a positive (MI-like) slope**. Therefore the primary
  regression controls on log σ_e / log M*, and the bracket-B rerun is mandatory; a slope that
  dies under bracket B is reported as NOT robust.

## 3. Anisotropy proxies (frozen) — and what they are NOT

Resolved, from per-galaxy DAP MAPS (HYB10-MILESHC-MASTARSSP), sigmacorr-corrected in
quadrature (σ_c² = σ² − σ_corr²), flux-weighted (SPX_MFLUX), masked spaxels excluded:
- **P1 — LOS-σ major/minor asymmetry:** σ_maj/σ_min in the 0.5–1.0 Re elliptical annulus;
  major wedge |cos φ| ≥ 0.87 (±30° of major axis), minor wedge |cos φ| ≤ 0.5 (>60°), φ =
  SPX_ELLCOO elliptical azimuth. ≥8 valid spaxels per wedge required.
- **P2 — dispersion-profile slope:** d ln σ_c / d ln R over **0.5 ≤ R/Re ≤ 1.5** (frozen
  window), unweighted OLS in log-log on all valid spaxels, ≥20 spaxels required.
- DAPall-level fallback proxy (whole-sample, no MAPS needed): none frozen — P1/P2 are the
  proxies; the DAPall catalog carries only δ, (V/σ)_glob and controls.

**Jeans-theory basis (stated, cited):** for spherical/axisymmetric systems the LOS projection
of the anisotropic Jeans equations (Binney & Mamon 1982, MNRAS 200, 361; Cappellari 2008,
MNRAS 390, 71 — JAM) makes radially-anisotropic (β>0) systems show (i) steeper outward-falling
σ_LOS(R) profiles (more negative P2) and (ii) characteristic major/minor σ_LOS asymmetry at
fixed intrinsic shape/inclination (P1). Sign convention frozen: **larger radial anisotropy ↔
more NEGATIVE P2**; the MI prediction dδ/dβ_r>0 therefore maps to **dδ/dP2 < 0** and (for
oblate systems viewed away from pole-on, β_z>0 flattening the velocity ellipsoid) **dδ/dP1
sign recorded but treated as secondary** (P1's β mapping is inclination/shape-degenerate).

**THE PROXY IS NOT β (stated prominently):** P1/P2 are LOS signatures contaminated by
inclination, intrinsic shape, rotation residuals, and M/L gradients. The slow-rotator cut
mitigates rotation; nothing here replaces Stage-2 Jeans/JAM per-galaxy β. Stage 1 is a proxy
firing only.

## 4. Regression spec (frozen — NOT run in this staging lane)

δ (each footing, each IMF bracket) vs each proxy (P2 primary, P1 secondary), on the PRIMARY
cut sample (VARIANT alongside):
- estimator: Huber robust linear regression + Spearman partial correlation;
- **controls: log10 M*, log10 R_e(kpc), z; plus log10 σ_e in the bracket-B rerun**; local
  density added IF a public group catalog crossmatch is available at firing time (named in
  STAGE.md), else omitted and said so;
- reported: slope ± bootstrap CI (10,000 resamples), partial Spearman ρ ± CI, per footing ×
  bracket × cut-variant grid — ALL cells shown, no cherry-pick;
- **the discriminator is the SIGN of dδ/dP2 (expect < 0 under MI via the frozen sign map, = 0
  under MG-with-same-ν)**;
- power statement for Stage 2 (full Jeans) computed from the observed proxy scatter.

## 5. Exploratory firewall (frozen)

**No kill conditions exist for this observable — nothing in this run can support or kill the
framework.** The first number is EXPLORATORY: it creates the baseline and pre-registers the
full-Jeans Stage 2. A null or MG-favoring slope is reported straight. A positive slope is
reported with the IMF-fake caveat attached at equal prominence. Both footings always; no
hard-coded verdicts; exit-0 scripts; frozen zimmerman-formula repo read-only.

## 6. Resolved-proxy subsample rule (frozen)

From the PRIMARY-cut catalog: rank by SNR_MED within σ_e terciles and take the top N/3 per
tercile (spread across the σ_e range), target **N = 48** (floor 24 if bandwidth limits;
actual N and the limit stated in STAGE.md). MAPS files: DR17 HYB10-MILESHC-MASTARSSP
`manga-{plate}-{ifudsgn}-MAPS-HYB10-MILESHC-MASTARSSP.fits.gz`.
