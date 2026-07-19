# a0(z) directly from Type Ia supernovae (model-independent)

de Sitter–Unruh **MODIFIED-INERTIA** framework (Carl Zimmerman). "Get dark
energy from the SNe using the framework instead of ΛCDM": ΛCDM *assumes* the
leftover is a constant Λ and fits it; here we *read the leftover density off the
SNe point-by-point* and convert it to the galaxy acceleration scale a0(z).

Run: `python3 extract_a0z.py` (exit 0; numpy/scipy). Outputs: `extract_a0z.out.txt`,
`a0z_fig.png`. Data: `../sne_lambda/pantheonplus_full.dat` (Pantheon+SH0ES,
IS_CALIBRATOR==0 & zHD>0.01 → 1580 cosmology SNe, z∈[0.010, 2.261]).

## Equations (the deliverable)
No Λ, no w(z) assumed — ρ_DE(z) is **measured**, not modeled:

    d_L(z) reconstructed NONPARAMETRICALLY (GP)  →  H(z) = c / d(d_C)/dz,  d_C=d_L/(1+z)
    ρ_DE(z) = 3[H(z)² − Ω_m H0² (1+z)³] / (8πG)             (GR background kept)
    a0(z)   = (c/2)√(G ρ_DE) = (c/Z) √(H² − Ω_m H0²(1+z)³),  Z=√(32π/3)=5.789

This is the **CANONICAL (ρ_DE) footing** by construction. `Z` is **posited** — a0's
magnitude inherits it. Milgrom is the acceleration-scale kernel wellhead; the
framework's distinctive content is the cH_Λ/Z coefficient.

## Method (Seikel–Clarkson–Smith 2012 style)
- Bin the Hubble diagram (40 equal-count z-bins, inverse-variance weighted).
- **Squared-exponential GP** on the distance-modulus residual vs a smooth LCDM
  template (template = numerical conditioner only; H(z) uses the full μ, so the
  template does **not** bias the result). Hyperparameters by marginal likelihood
  (A=0.055 mag, ℓ=0.60 in z, capped so curvature isn't over-smoothed away).
- **Analytic derivative GP**: joint posterior over [μ(z), μ′(z)] via the SE-kernel
  derivative identities, so H(z)=c/d_C′ carries an honest, correlated error band
  (3000 Monte-Carlo draws, not finite-difference noise). ρ_DE<0 draws → NaN,
  reported as "% of draws with ρ_DE>0".

## Inputs that remain (stated, not circular)
- **Ω_m** (matter, not dark energy → no circularity): Planck 0.315, sensitivity 0.29–0.35.
- **GR/Friedmann background** (the framework keeps GR for the background).
- **H0** enters only via the M_B↔H0 degeneracy scale (M_B=−19.253 → H0≈73 internally;
  H0=67.4 obtained by the uniform 67.4/73 rescaling). The a0(z) **shape is
  H0-robust**; the **absolute a0(0) carries H0**.

## Results

### a0(0) — the robust SNe output
E(0)=1 exactly, so a0(0) = (c/Z) H0 √(1−Ω_m) — this **is the local Λ leftover**
(ρ_DE today), essentially SNe-noise-free, carrying H0:

| H0 (km/s/Mpc) | Ω_m=0.315 | Ω_m=0.29 | Ω_m=0.35 |
|---|---|---|---|
| **67.4** | **9.36e-11** | 9.47e-11 | 9.05e-11 |
| **73.0** | **1.014e-10** | 1.026e-10 | 9.80e-11 |

a0(0)[67.4, 0.315] = **9.36e-11** reproduces the **canonical** a0=9.355e-11 by
construction (H_Λ = H0√(1−Ω_m)). Both footings sit within the SPARC z=0 band
**1.181e-10 ± 1.90e-11** (Λ-blind GLS gas-dominated): 67.4 low by ~1.3σ,
73.0 low by ~0.9σ — cross-scale **consistent**, not a detection either way.

### a0(z) with error bands (canonical Ω_m=0.315), median [68%]
| z | H0=67.4 | H0=73.0 | note |
|---|---|---|---|
| 0.5 | 1.01e-10 [0.97,1.04] | 1.09e-10 [1.05,1.13] | in data |
| 1.0 | 1.11e-10 [0.90,1.30] | 1.20e-10 [0.97,1.41] | in data |
| 2.0 | 1.24e-10 [0.63,2.12] | 1.35e-10 [0.68,2.30] | near data edge; ρ_DE>0 in 25% of draws |
| 3.0 | 3.54e-10 [1.8,6.6] | 3.83e-10 [1.9,7.2] | **EXTRAPOLATED** past z=2.26; ρ_DE>0 in 47% |

a0 ∝ H0 uniformly (shape identical across H0). At z≳1 the band explodes and ρ_DE
goes negative in most draws — SNe carry **almost no** a0(z) information there.

### THE KEY QUESTION — is da0/dz distinguishable from zero?
**No, not robustly.** The low-z shape is **degenerate with Ω_m** (matter
under/over-subtraction), so the honest slope test marginalizes Ω_m∈[0.29,0.35]:

| a0(z)/a0(0), Ω_m-marginalized | median [68%] | consistent with 1 (flat/Λ)? |
|---|---|---|
| z=0.5 | 1.077 [1.029, 1.121] | no (~1.6σ, **Ω_m-driven**) |
| z=1.0 | 1.172 [0.921, 1.388] | **YES** |
| z=2.0 | 1.342 [0.751, 2.263] | **YES** |
| z=3.0 | 3.838 [1.96, 7.23] | no (**extrapolation/noise**, not a detection) |

The only sub-z=0.5 nominal >1σ excursion is a **RISE** that is entirely an Ω_m
artifact — at fixed Ω_m it slides from 1.119 [1.08,1.15] (Ω_m=0.29, "off 1") to
**1.028 [0.99,1.07] (Ω_m=0.35, consistent with 1)**. Local slope da0/dz|_{z≈0.3}
= 1.85e-11 [0.69, 2.91]e-11 m/s² (H0=73): nonzero at ~2σ but **Ω_m-sourced**, not
a genuine dark-energy-evolution signal. **We do not manufacture a decline.**

### The 0.60–0.75 "decline" benchmark
**Not supported by the SNe.** The reconstruction leans flat-to-mild-*rise* at low
z (Ω_m-degenerate) and is noise-dominated at high z; only ~1% of z=3 draws land in
[0.60,0.75]. Constant Λ (ratio ≡ 1, i.e. a0(z) **flat**, since w=−1 ⇒ ρ_DE const
⇒ a0 const) is consistent across the whole probed range.

## Verdict
**a0(0) is the robust, model-independent SNe output** — it is the local Λ leftover,
carries H0 (9.36e-11 at 67.4 = canonical; 1.014e-10 at 73.0), both consistent with
the SPARC z=0 a0 within ~1σ. **The a0(z) SLOPE is NOT robustly detected by SNe
alone**: differentiating d_L amplifies noise, the low-z shape is Ω_m-degenerate,
and ρ_DE(z) is consistent with constant (a0(z) flat-consistent). Neither the
0.60–0.75 decline nor any robust evolution is seen. This matches the banked SNe
result (Pantheon+ alone gives Δχ²~0.5 for w0waCDM — no preference for evolving DE).

**Alt footing (separate, NOT canonical):** a0 = cH_Λ/Z here uses ρ_DE; an
alternative a0 ~ cH(z)/Z from ρ_total would instead *rise* with z as E(z) (opposite
sign of the ρ_DE reading). Reported above is the canonical ρ_DE footing by
construction, per a0 = (c/2)√(G ρ_DE).

Credits: Milgrom (kernel); Brout+2022 / Scolnic+2022 (Pantheon+SH0ES);
Seikel, Clarkson & Smith 2012 (GP model-independent H(z)).
