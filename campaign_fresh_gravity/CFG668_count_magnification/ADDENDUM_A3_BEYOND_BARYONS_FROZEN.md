# CFG668 addendum A3 — magnification BEYOND the cluster baryons (FROZEN, before any A3 number is computed)

Idea: look where only cold energy can be. Cluster baryons (stars + hot gas) end within ~2 Mpc. Outside them a baryons-only lens has
convergence κ = 0, so magnification μ − 1 ≈ γ² is negligible (point-mass shear θ_E²/θ² ~ 1e-4 at 8'). The law's cold energy
(deep-MOND phantom density ∝ 1/r², sourced by the cluster baryons) gives κ(θ) ∝ 1/θ out to tens of arcminutes.
Question: is there magnification at 8–40' around clusters, where there are no cluster baryons?

## Data — the A2 files (no new download): Quaia G<20 (primary) and SDSS DR16Q; redMaPPer λ ≥ 20, 0.2 ≤ z_λ ≤ 0.6
(z ≥ 0.2 so that 8' is ≥ 1.6 Mpc for any reasonable distance scale). Quasars z_Q > z_λ + 0.5. Same blanks/footprint cut as A2.

## Estimator (self-calibrated, double ratio)
For each pointing, density in annulus a ∈ {8–12', 12–20', 20–40'} divided by density in its own control ring 60–90'.
R_j(a) = ⟨clusters⟩ / ⟨blanks⟩ of that local ratio, per magnitude bin j (A2 bins). Slope s_j from blanks (A2 method).
Lensing estimator: K = Σ_j w_j (R_j − 1) / Σ_j w_j², w_j = 2.5 s_j − 1 (estimates μ − 1 ≈ 2κ, control ring taken as κ≈0).
Errors: jackknife over 48 sky patches (equal-count in RA×Dec), which captures large-scale correlated noise.

## Decision rules (8–40' aperture = all three annuli pooled)
- MASS BEYOND BARYONS DETECTED: K > 0 at ≥ 3σ, Quaia and DR16Q combined by inverse variance, each with K > 0.
- WRONG SIGN: K < 0 at ≥ 3σ.
- NULL (baryons-only consistent): |K| < 2σ. Then report the 2σ upper limit on κ at 8–40'.
- Reported regardless: K per annulus (the law predicts K ∝ 1/θ, i.e. 8–12' : 12–20' : 20–40' ≈ 2.7 : 1.7 : 1, area-weighted means).
- The detection says lensing mass sits beyond the cluster baryons. It does not by itself separate cold energy from a dark-matter
  halo; no ΛCDM halo is used. Amplitude-vs-baryon-mass comparison is a later step.
MUTATE: half the blanks play clusters → K must be 0.
κ fitted; cold energy mass required; not theory closed.
