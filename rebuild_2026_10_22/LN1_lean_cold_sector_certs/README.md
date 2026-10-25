# LN1_lean_cold_sector_certs — Lean 4 + Mathlib certificates for the 2026-10-25 cold-sector lanes

`ColdSectorCerts.lean` compiles with **no `sorry`**. Every theorem depends only on Lean's standard axioms (propext,
Classical.choice, Quot.sound), printed in `ColdSectorCerts.out`. `ColdSectorCerts_MUTATE.lean` breaks two definitions:
- the arctan sign in Bk, flipped;
- the SIDM exponent, 1+n → 1−n.

It fails to compile (exit 1, errors at the Burkert derivative, the bound and the SIDM identity).

**Lean certifies mathematics from stated premises only.** It does not certify that halos are Burkert, that
Σ = a₀/(2πG), any measured number, or any physical premise. κ = ½ FITTED; not "theory closed"; nothing here says the data
favour the framework or ΛCDM.

Compile: `cd fable_independent_2026/lean_2026 && lake env lean ../../rebuild_2026_10_22/LN1_lean_cold_sector_certs/ColdSectorCerts.lean`

## What is certified

| # | theorem | statement | used by |
|---|---|---|---|
| T1 | `Bk_hasDerivAt`, `Bk_zero` | Bk(x) = ln(1+x²) + 2 ln(1+x) − 2 arctan x has Bk′ = 4x²/((1+x)(1+x²)) and Bk(0) = 0, so π ρ₀ r₀³ Bk(r/r₀) is the Burkert enclosed mass | X38, X39, CD1, NM1 |
| T2 | `accel_shape` | G M(r)/r² = π G Σ · Bk(x)/x², x = r/r₀: a fixed-Σ halo's pull depends on r, r₀ only through x | CD1 |
| T3 | `Bk_le`, `Bk_one_gt` | Bk(x) ≤ (9/16) x² for all x ≥ 0, and Bk(1) = 3 ln 2 − π/2 > 1/2 | CD1 |
| — | `ceiling` | with Σ = a₀/(2πG): **G M(r)/r² ≤ (9/32) a₀ = 0.28125 a₀ for every r and every r₀**; the sup is ≥ a₀/4. CD1's numeric 0.2545 a₀ lies in [0.25, 0.28125] a₀ | CD1 |
| T4 | `fold_source` | for H = A p²/2 + B x p + C x + Φ(x), ∂²H/∂x² = Φ″(x): any spatially uniform drive drops out of the fold source | DH1 statement 1 |
| T5 | `windows_disjoint` | no A satisfies 2.695 ≤ A ≤ 1.424 (canonical) or 2.856 ≤ A ≤ 1.472 (alt) (DH1's numbers as premises) | DH1 statement 2 |
| T6 | `gbar_distance_free` | g_bar = G Υ F 4π d² / (θ d)² is independent of d | HG1/HG2 K3 |
| T7 | `sidm_core_surface` | isothermal core ρ₀r₀² = 9σ²/(4πG) plus ρ₀ = 1/(K σ^(1−n) t) give **Σ₀² = 9 σ^(1+n) / (4πG K t)**, so Σ₀ ∝ σ^q t^(−1/2), q = (1+n)/2 | the open question |
| T8 | `sidm_window` | if galaxies (same age) keep Σ within a factor F over a dispersion ratio σ₂/σ₁, and clusters need Σ_cl/Σ_gal ≥ Q with σ_cl/σ_gal ≤ R_c and t_cl/t_gal ≥ τ, then **log Q + ½ log τ ≤ q log R_c and q log(σ₂/σ₁) ≤ log F** | the open question |

## The open question: cored galaxies and dwarfs, denser cluster cores

X38, CD1 and NM1 left one requirement on the record. Galaxies and dwarfs want cores at Σ_a0 = a₀/(2πG). Heavy cluster
cores want about 2× (X39) to 3–5× (X40b (C)) of that. T7 shows that a self-coupled cold dark energy with a power-law
velocity-dependent interaction (σ/m ∝ v^(−n)) gives Σ₀ ∝ σ^((1+n)/2) t^(−1/2). T8 turns the data's shape into a certified
window on q. `window_eval.py` evaluates it under stated scenarios (`window_eval.out`):

- **Clusters need ≤ ~3× and galaxies tolerate Σ varying ×2 across σ ×8:** the window is OPEN, q ≈ 0.28–0.33, so
  **n ≈ −0.44 to −0.33**: a cross-section per mass that rises weakly with velocity, σ/m ∝ v^(0.33–0.44).
- **Clusters need ≥ 4× (canonical scenarios), or galaxies must stay within ×1.5:** EMPTY. No power law does both.
- So it is a narrow door. It needs the cluster requirement near X40b's lower end and some slack in galaxy Σ.

**What is still not derived.** The normalisation K (a new constant) and the exponent n do not follow from a₀ or Λ here.
Fixing K with Σ_a0 at galaxy scale would make a₀ set the coupling. Fixing n is the open target. The interesting value
q = 1/3 (n = −1/3) sits at the top edge of the open window. Weakly rising cross-sections are unusual: most published
self-interacting models fall with velocity. That is a reason for caution, not a result.

Next decisive step (needs its own frozen criteria): grade the T7 law with q fixed at a candidate value on SPARC (does Σ
varying as σ^q still pass X38's line?) and on X30's cluster cells. The galaxy-flatness premise F is the number SPARC must
supply.
