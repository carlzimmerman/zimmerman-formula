# GH7_ksz_desi_centrals: FROZEN CRITERIA (committed alone, before the temperature map is fetched or any velocity is built)

**Question.** tSZ (GH3–GH5) sees pressure and FRBs (GH6) lack power. kSZ measures the electron column at any temperature.
**Is the gas that route E needs on KiDS lensing (Zhang's gas continuing to about 1.8 R_vir, GH2) present around MW-mass
centrals?** Extent is claimed only if its own gate passes.

## Data

- **Map (fetched with the owner's OK):** ACT DR6.02 NILC `act-planck_dr6.02_nilc_blackbody_T.fits`, 1.6′ Gaussian beam, CAR
  0.5′. It is not a deprojected map. Pixels that are zero or non-finite within 15′ of a lens drop that lens.
- **Lenses:** DESI DR1 BGS + CIGALE as GH6's cache (`gh6_bgs.npz`). LOGM 10.6–11.0, z 0.1–0.5, inside the map. Central = no
  more massive BGS neighbour within 1 Mpc and |Δv| < 2000 km/s, as GH5. LOGM to native as GH5.

## Velocities

- **Mesh:** comoving box in native geometry, 8 Mpc/h cells. All BGS galaxies with z 0.05–0.5 are the tracer.
- **Randoms (no DESI randoms on disk):** sky drawn from the nside 64 galaxy-count map, z drawn from the global n(z), 10 × the
  data. δ = 0 where the random density is below 10 % of its mean.
- **Reconstruction:** Gaussian smoothing 12.5 Mpc/h; in Fourier space ψ = i k δ/k²; v = β a H ψ, read at each lens and
  projected on the line of sight. RSD is not removed.
- **β = f/b = 0.44 is INHERITED, not native:** f = Ω_m(z)^0.55 at native Ω_m 0.3085 and z 0.26 gives 0.66; b = 1.5 is a typical
  BGS value. **A scales as β_true/0.44.** Amplitudes depend on it. The profile shape does not.
- **Calibration, no ΛCDM mock:** P(k) measured from this mesh, shot-noise subtracted; a lognormal mock with that P(k), the survey
  window and Poisson sampling at the data density; linear velocities with the same β. The same reconstruction gives r_mock and
  the regression factor R = Cov(v_true, v_rec)/Var(v_rec). The mock has no sub-mesh velocities, so r_mock is an upper bound. The
  published r = 0.64 (arXiv:2604.19745) is context only.

## Measurement

- **Compensated apertures:** CAP(θ) = mean inside θ − mean in [θ, √2 θ], θ = 1, 1.5, 2, 3, 4, 6, 8, 10′, in true sky distance.
- **Estimator per θ:** the mean CAP is subtracted in 10 z bins, which removes tSZ and CIB (even in v). Then
  T̂(θ) = −Σ CAP_i (v_i/c) / Σ (v_i/c)².
- **Model:** Zhang gas (β 0.43, r_c 6 kpc, 1.84 M★, μ_e 1.14, R_vir Table 1) cut at k = 1, 1.8, 3, τ profile beam-convolved,
  apertured, averaged over (z, lm) cells, multiplied by T_CMB and R.
- **Covariance:** velocity-shuffled nulls (200, shuffled within z bins on the real map), which include the real map noise. GH5
  showed jackknife errors low, so jackknife is reported only. A(k) is the matched amplitude on 8 points, with the error from the
  same shuffles.

## Power gate (run after the fetch, with T̂ not computed: it uses CAP scatter and velocity rms only)

- S(v) = sqrt(N-weighted vᵀ C⁻¹ v), with C from the per-lens CAP covariance and the measured rms velocity.
- **G1:** S(k = 1.8) ≥ 3. **G2:** S(1.8 − 1) ≥ 3.
- G1 fails: **NON-DIAGNOSTIC**, T̂ is not computed, and the lane ends. G1 passes, G2 fails: amplitude only, no extent statement.

## Verdict (PRIMARY: A(1.8), error σ from shuffles)

- **GAS DETECTED:** A(1.8)/σ ≥ 3 and shuffle p < 0.003.
- **BELOW ROUTE E'S NEED:** A(1.8) + 2σ < 1.
- **INCONCLUSIVE:** otherwise.
- **Extent, only if G2 passes:** EXTENDED if A(1) sits more than 2σ above 1 while A(1.8) is within 2σ of 1; MEASURED if A(1) is
  within 2σ of 1 while A(1.8) sits more than 2σ below 1; NOT DECIDED otherwise.
- **Reported:** A per k; the jackknife errors; the passive and star-forming split; COMP_TILE-free (no such cut here); footprint
  north and south.

**Interpretation lock.**
- Any A carries the β_true/0.44 and R systematic; a BELOW or DETECTED class within about 30 % of a boundary is stated as
  systematic-limited.
- Correlated neighbours' gas (two-halo) adds to the signal, so a detection is an upper bound on the lenses' own gas, and a
  shortfall is the firmer direction.
- DETECTED is a necessary condition only: GH2 found the law fits KiDS better than route E at any extent.

## Checks

- **K1:** β = 2/3 projection closed form within 1e-4.
- **K2:** pixel geometry vs astropy WCS within 0.01 px.
- **K3:** on the mock, r_mock > 0.3 and v_rec has the sign of v_true.
- **K4:** a beam source of known profile injected into blank-sky stamps at lens positions returns its model CAP within 2 %.
- **K5:** the estimator on real CAPs + injected kSZ using the mock-like relation (−τ T v/c at A = 1 with v = v_rec / R) recovers
  A(1.8) − A(1.8, no injection) = 1 within 2 %.
- **MUTATE:** v → −v flips every T̂ exactly; a shuffled-velocity stack is a null (p > 0.01).

**Scope.** Velocity scale is inherited, flagged above. κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field
component, never a particle; not theory closed; nothing here says the data favour the framework. One thread, nice 15, RSS < 3 GB.
