# GH6_frb_dm_cgm: FROZEN CRITERIA (committed alone, before any FRB is matched to any galaxy)

**Question.** GH3–GH5 used tSZ, which measures pressure and is blind to cool gas. Route E needs mass. Dispersion measure
counts ionized electrons at any temperature. **Can the localized FRBs on disk measure the gas column around MW-mass
centrals, and can they tell gas ending at R_vir from gas reaching 1.8 R_vir?** This is answered by a power gate first.

## Data (nothing new fetched)

- **FRBs:** `frb_sharma26/repo/data/frb_results/frb_sample.csv`. PRIMARY: `sharma_sample == yes` (N = 92, arcsec
  localizations). Reported forecast: yes + unclear (N = 114; the unclear ones have arcmin localizations).
- **Lenses:** DESI DR1 `BGS_BRIGHT_full_HPmapcut` with ZWARN = 0, DELTACHI2 > 40, joined to CIGALE (main/bright) LOGM as
  GH5, whole sky. LOGM to native as GH5. Central = no more massive BGS neighbour within 1 Mpc and |Δv| < 2000 km/s.
- **PRIMARY lenses:** log M★ 10.6–11.0 (Zhang's measured MW-mass range, as GH3–GH5), z ≥ 0.01. **Wide forecast:** log M★
  10–11.5, Zhang's 1.84 M★ extrapolated.
- **Footprint:** an FRB counts if at least 90 % of the nside 128 pixels within 1° of it hold at least one good BGS galaxy.
- **Foreground:** z_lens < z_FRB − 0.005, so the host's own halo and neighbours are excluded.

## Model (no free parameter)

- Zhang gas as GH3–GH5: β 0.43, r_c 6 kpc, M(<R_vir) = 1.84 M★, μ_e 1.14, R_vir from Table 1, cut at k R_vir, k = 1, 1.8, 3.
- Observed DM from one lens at impact b: DM = N_e(b; lm, k) / (1 + z_lens). Native h 0.679, Ω_m 0.3085.
- m_i(k) = the sum over foreground central lenses for FRB i.

## Power gate (positions, redshifts and catalogues only; DMexgal is NOT read)

- **Noise per FRB, fixed in advance:** σ_i² = σ_c(z_i)² + σ_h(z_i)².
  - σ_c: the authors' median band in `DMvar_Sharma2026.npz`, interpolated.
  - σ_h = 117 / (1 + z) pc cm⁻³ (log-normal host at the centre of the authors' box, μ = 5, s = 0.6).
- **Fit:** DM_i = c0 + c1 D(z_i) + A m_i(k), with D(z) = ∫(1+z)/E dz, weights 1/σ_i². With P the weighted projector
  orthogonal to (1, D), S(v) = sqrt(vᵀ P v).
- **G1, detect:** S(m(k=1)) ≥ 3.
- **G2, extent:** S(m(1.8) − m(1)) ≥ 3.
- **Outcomes:**
  - G1 fails: **NON-DIAGNOSTIC**. DMexgal is not correlated with lenses at all, and the lane ends with the forecast.
  - G1 passes, G2 fails: amplitude only, no extent verdict.
  - Both pass: the measurement below runs.
- **Reported, no gate weight:** S for m(3) and m(3) − m(1); the wide-mass and N = 114 forecasts; N_FRB needed for G1 and
  G2, scaling S ∝ √N at this sample's z distribution and footprint fraction.

## Measurement (only if G1 passes)

- Weighted least squares for A(k) on the PRIMARY sample; DMexgal as tabulated, unclipped.
- Errors and p from 2000 null realisations: FRB positions rotated in RA within the footprint, keeping z and DM.
- **Classes:**
  - **GAS DETECTED** if the null p < 0.003 for k = 1, positive A.
  - **NO DETECTION** otherwise, and the upper limit on A is quoted.
- **Extent, only if G2 passes:**
  - **EXTENDED** if A(1.8) is consistent with 1 within 2σ and A(k=1) is above 1 by more than 2σ.
  - **MEASURED EXTENT** if the reverse holds.
  - **NOT DECIDED** otherwise.
- **Two-halo lock:** large-scale structure around lenses also carries electrons, so a positive A is an upper bound on the
  lenses' own gas. No two-halo term is modelled.

## Checks

- **K1:** β = 2/3 projection closed form within 1e-4.
- **K2:** the area integral of N_e μ_e m_p over the plane out to k R_vir, for k = 1, recovers the mass within R_vir projected
  on a sphere-limited cut: the integral equals 1.84 M★ within 1 %.
- **K3:** Fisher S agrees with the scatter of Â in 2000 Gaussian mocks with the same σ_i, within 10 %.
- **K4:** mocks with A = 1 injected recover mean Â within 3 standard errors of 1.
- **MUTATE:** gas mass × 10 gives S × 10 exactly (linearity). Rotated FRB positions give mean S(m(1)) within a factor of 2 of
  the true positions' S; a larger gap would mean FRB positions are unusually placed, and is reported.

**Scope.**
- CIGALE masses are not Zhang's; missing lenses (BGS completeness, fibres) go into noise, not signal.
- FRB samples may under-represent high-DM sightlines through host-association bias; not modelled.
- Gas with T ≲ 1e4 K that is neutral does not count in DM.
- κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing
  here says the data favour the framework. One thread, nice 15, RSS < 3 GB.
