# CFG668 addendum A3G — lens-geometry test (FROZEN with A3, before any A3/A3G number is computed)

Owner, 2026-10-12: "use a new geometric perspective". Lensing has a fixed geometry: a lens at z_l magnifies a source at z_s by an
amount ∝ β = D_ls/D_s (flat: β = 1 − D_M(z_l)/D_M(z_s); β = 0 for a source IN FRONT of the lens). A quasar in front of a cluster
shines through no cold energy; one far behind shines through all of it. Survey systematics (depth, extinction, cluster-finder
correlations) do not know z_s relative to z_l.

## Distances — raw measured geometry only
D_M/r_d from DESI DR2 BAO (arXiv 2503.14738, Table: LRG1 0.510 13.588; LRG2 0.706 17.351; LRG3+ELG1 0.934 21.576; ELG2 1.321
27.601; QSO 1.484 30.512; Lyα 2.330 38.988), BGS z=0.295 D_V/r_d = 7.942 converted with D_H linearly extrapolated from LRG1/LRG2,
D_M(0)=0, monotone PCHIP interpolation; beyond 2.33, D_H ∝ (1+z)^−1.5 from Lyα D_H/r_d = 8.632. r_d cancels in β. No ΛCDM model.

## Estimator
Same pointings, annuli, control ring and K estimator as A3, but quasars split by β of each (cluster, quasar) pair — blanks carry
their parent cluster's z_l, so β is computed identically:
  FG: z_Q < z_l − 0.1 (β = 0, in front)   B1: 0 < β < 0.55   B2: 0.55 ≤ β < 0.70   B3: β ≥ 0.70.
Slopes s per β-bin from blanks. Fit K_b = A · β̄_b + C by generalised least squares with the jackknife covariance (48 patches).
C absorbs anything that ignores geometry; A is lensing.

## Decision rules (8–40' aperture; Quaia + DR16Q pooled pair lists, each also reported alone)
- GEOMETRIC LENSING BEYOND BARYONS: A > 0 at ≥ 3σ. STRONG: also K_FG consistent with 0 (|z| < 2).
- WRONG GEOMETRY: A < 0 at ≥ 3σ.
- NULL: |A| < 2σ → report 2σ upper limit on κ(8–40') at β = 1 (κ ≈ A/2).
- Also run on 0–4' (inside the baryons) for reference; not a decision.
MUTATE: half the blanks play clusters → A must be 0.
κ fitted; cold energy mass required; not theory closed.
