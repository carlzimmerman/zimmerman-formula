# CFG681 — BAO from raw distances only: no CMB, no CPL, no ΛCDM model (FROZEN, before any number)

Block CFG680–689 (owner reserved 2026-10-12). Owner: "deep dive into the BAO data ... figure it out in a way we couldn't before".
Record map (10-12): every earlier a0(z)-from-DESI result went through published w0–wa chains (BAO+CMB+SN, CPL form), hence
"hostage" to DESI's fit. Never done: a CMB-free, form-free reconstruction of ρ_DE(z); BAO vs SN shape; distance duality; the
D_M/D_H ratio across all tracers. Owner rule: a0(z) = κ c √(G ρ_DE(z)) tracks dark energy, so a0(z)/a0(0) = √X(z), X = ρ_DE(z)/ρ_DE(0).

## Data (raw summary measurements)
- DESI DR2 BAO (arXiv 2503.14738, Table: D_V/r_d for BGS z=0.295; D_M/r_d, D_H/r_d and their correlation r for LRG1 0.510,
  LRG2 0.706, LRG3+ELG1 0.934, ELG2 1.321, QSO 1.484, Lyα 2.330). Tracers independent; 2×2 covariance per tracer.
- Pantheon+ (Scolnic+22/Brout+22): m_b_corr, zHD, STAT+SYS covariance from the public data release (download, ~30 MB),
  non-calibrator SNe with zHD > 0.01. Absolute magnitude M marginalised analytically (shape only).
- Radiation: Ω_r(1+z)^4 with T_CMB = 2.7255 K (FIRAS) and h = 0.68 (enters at ≤ 1% at z = 2.33; disclosed).

## Model-free dark energy
Flat: E(z)² = Ω_m(1+z)³ + Ω_r(1+z)⁴ + (1 − Ω_m − Ω_r) X(z), X piecewise-linear in z on nodes {0, 0.4, 0.7, 1.0, 1.5, 2.33},
X(0) = 1 (5 free nodes), constant beyond 2.33. Nuisance: q = c/(H0 r_d) (BAO), M (SN). Ω_m free in [0.15, 0.45].
The dark degeneracy (Ω_m vs X) is real; results are reported with Ω_m profiled AND on the fixed grid Ω_m = 0.25/0.30/0.35.

## Tests
- T1 BAO-only: Δχ²(X ≡ 1 vs free X), each with Ω_m, q profiled. Converted to a p-value with 5 dof and an equivalent σ.
- T2 BAO + Pantheon+ shape: same.
- T3 Alcock–Paczyński F_AP = D_M/D_H at all six tracers (r_d- and H0-free): χ² of the best X ≡ 1 shape (Ω_m free); per-tracer pulls.
- T4 distance duality: η(z_i) = D_L,SN / [(1+z_i) D_M,BAO], SN distance modulus interpolated to each anisotropic tracer z_i
  (Gaussian kernel σ_z = 0.03, kernel-weighted with the full SN covariance), z_i ≤ 1.5. Fit η ∝ (1+z)^ε with a free normalisation.
  ε = 0 if photon number is conserved along the way (a photon-coupled dark sector would break it).
- a0 band: √X(z) at z = 0.5, 1.0, 1.5, 2.33 with 68/95% profile-likelihood intervals (T1 and T2), next to FLAT (√X = 1).

## Decision rules
- T1/T2: EVOLVING DE REQUIRED by that data set if Δχ² gives ≥ 3σ-equivalent (5 dof); CONSISTENT WITH CONSTANT if < 2σ; else HINT.
  If required: the owner's tracking law then predicts a0 evolution; the √X band is the prediction to confront with kinematic a0(z).
  If not required: a0 flat is allowed by raw BAO alone and the earlier "hostage" decline came from CMB/SN/CPL, not from BAO.
- T3: X ≡ 1 shape EXCLUDED if χ² p < 0.003 (5 dof after Ω_m); per-tracer |pull| > 3 flagged.
- T4: DUALITY VIOLATED if |ε| ≥ 3σ; CONSERVED if |ε| < 2σ; report σ(ε).
MUTATE: (M1) replace the DESI vector by its own X ≡ 1 best fit at the same errors → T1 Δχ² must be ~0 and the √X band must contain 1;
(M2) inject ε = 0.10 into the SN distances → T4 must recover it within 1σ.
κ fitted; cold energy mass required; not theory closed.
