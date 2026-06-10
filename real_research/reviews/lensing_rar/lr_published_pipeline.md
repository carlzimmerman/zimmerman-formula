# Brouwer+2021 pipeline — transcription (LR-1 Step 1, bound by `lr_preregistration.md`)

*C. Zimmerman, 2026-06-10. Transcribed from Brouwer et al. 2021 (A&A 650 A113, arXiv:2106.11677) via ar5iv + the A&A
HTML. TRANSCRIPTION-GAPs flagged for resolution before the replication gate. No data fetched/processed yet — this is the
fidelity-first record the pre-registration requires.*

## Lens sample
- **KiDS-bright** (KiDS-1000, 1006 deg²): photometric, m_r,auto < 20.0 (≈ GAMA m_r,Petro < 19.8); **0.1 < z < 0.5**,
  ⟨z⟩≈0.25; **M⋆ < 10¹¹ h₇₀⁻² M⊙**; ~1M galaxies. **GAMA** (180 deg², 238k, z-complete 98.5%) as the spectroscopic validation.
- **Isolation:** no satellite with M⋆,sat/M⋆,lens > 0.1 within r_sat = 3 h₇₀⁻¹ Mpc → **isolated subsample N = 259,383**
  (Appendix A: ~80% isolation accuracy, <20% contamination).

## Stellar mass
- KiDS-bright: **LePhare** SED fit, BC03 SPS, **Chabrier IMF**, 9-band KiDS u,g,r,i + VIKING Z,Y,J,H,Ks; ANNz2 photo-z trained
  on GAMA; GAaP `fluxscale` aperture correction. σ_M⋆ = 0.12 dex (stat), 0.2 dex (sys, normalized to GAMA).
- GAMA: Taylor+2011 masses (BC03, 3000–11000 Å). Mocks (MICE): Bell & de Jong 2001 M⋆/L.

## Early-type vs late-type classification (the split — TWO independent axes)
- **(a) Sérsic index** n (2DPHOT on KiDS); **(b) u−r colour** (KiDS 9-band). *(GAP-1: the exact n and u−r thresholds are
  not in the fetched text — needed for exact replication; resolve from §5.4/Table.)*

## ESD → g_obs (the conversion, with its assumption)
- ESD (Eq. 1): ΔΣ(R) = Σ_crit ⟨ε_t⟩ = ⟨Σ⟩(<R) − Σ(R); measured in **15 log bins, 1×10⁻¹⁵ < g_bar < 5×10⁻¹² m/s²**,
  R ∈ [0.03, 3] h₇₀⁻¹ Mpc; analytic covariance (Viola+2015); m-calibration μ≈0.014.
- **SIS approximation** (Eq. 3–7): ρ_SIS = σ²/(2πGr²) ⇒ M_obs(<r) = 4 ΔΣ_obs(r) r² ⇒ **g_obs(r) = 4 G ΔΣ_obs(r)**.
  *This is the sphericity/profile assumption (Battery axis 4).* Validated vs BAHAMAS (§4.4).

## g_bar (baryonic acceleration)
- g_bar(r) = G M(<r)/r²; **point mass** M_gal = M⋆(1 + f_cold), cold-gas fraction (Boselli+2014, Eq. 23):
  log f_cold = −0.69 log(M⋆/h₇₀⁻² M⊙) + 6.63. **Hot gas / CGM NOT included** (§4.3 "missing baryons"; up to ~1 dex at large r).

## The result and the authors' own escape route
- **≥6σ** difference between early- and late-type RARs **at the same M⋆**, split by Sérsic AND u−r (abstract; detail §5.4).
- **Authors' physical explanation (verbatim):** "the difference might be explained if only the early-type galaxies have
  significant **(M_gas ≈ M⋆)** circumgalactic gaseous haloes." → **this names the live escape route AND its size.**
- **Authors already tested stellar-M/L:** M⋆ varied by ±0.2 dex → "does not change the conclusions of §5.4." ⇒ **Battery axis 1
  (M/L) is largely closed BY THE AUTHORS**; to matter it must be *type-dependent* and > the ±0.2 dex they probed.

## The closure arithmetic (Battery framework — setup, NOT a result; battery runs only after the replication gate)
The escape route adds CGM baryons to early-type g_bar only: Δlog g_bar = log₁₀(1 + M_gas/M⋆). So **M_gas ≈ M⋆ ⇒ a 0.30 dex
rightward shift** of the early-type sequence. The audit's quantitative core (Battery axis 2): **is the early/late offset ≈0.30 dex
(closeable by M_gas≈M⋆) or larger, and is M_gas≈M⋆ CGM physically plausible for ISOLATED M⋆<10¹¹ early types?** Cosmic budget
check to run: available CGM ≈ (Ω_b/Ω_m) M_halo − M⋆ ≈ 0.16 M_halo − M⋆; with M_halo ~ 10–30 M⋆ for this regime, the reservoir is
~1–4 M⋆ — so M_gas≈M⋆ is *within* the baryon budget but requires near-total CGM retention AND a strong early-vs-late asymmetry.
**Hostility inversion (locked):** the verifier must argue this escape FAILS (retention too high, asymmetry implausible, offset >0.30 dex).

## TRANSCRIPTION-GAPs to resolve before the replication gate
- **GAP-1:** exact Sérsic-n and u−r thresholds for the split.
- **GAP-2:** the §5.4 quantitative offset (dex) and how "≥6σ" is computed (χ² over which bins / acceleration range).
- **GAP-3 (data acquisition — the gate blocker):** the binned RAR points (early/late g_bar, g_obs, errors) are **not in a
  one-click Zenodo release**. Candidate sources, in order: (i) **CDS/VizieR** catalog for A&A 650 A113; (ii) digitize the §5.4
  RAR figure; (iii) re-run the ESD pipeline on the public KiDS-1000 shear + GAMA (full replication — heaviest). **Resolve GAP-3
  first; the replication gate (our split within ~1.5× of 6σ) cannot run without these points.** Per the pre-reg, no fabrication.

## Status
LR-1 Step 1 (transcription) complete. **Step 2 (replicate the split) is BLOCKED on GAP-3 (data acquisition)** — the honest
gate: obtain the real RAR points before any significance is computed. Battery (Step 3) and verdict (Step 4) follow Step 2.
