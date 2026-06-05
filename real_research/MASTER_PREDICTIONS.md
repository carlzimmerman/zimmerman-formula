# Master list of testable predictions — a₀ = c²√(Λ/32π)

*The framework's complete, de-duplicated testable-prediction set, each with its computed value, the real data it is
(or would be) tested against, status, and whether it is **distinctive** to this framework or **shared** with ordinary
constant-a₀ MOND. All numbers reproduce from the committed scripts (`predictions/`), verified in the full integrity
audit (`INTEGRITY_AUDIT.md`). Constants: Planck 2018 Λ, DESI DR2 w₀=−0.752, wₐ=−0.86.*

## The honest one-line frame

Almost everything *measured today* (the a₀ value, rotation curves, dwarfs, lensing, clusters, wide binaries) is
**shared with ordinary MOND** — real and validated, but a test of the *value* of a₀, not of this framework. The
**only distinctive content is the evolution** a₀(z) = a₀(0)·√(ρ_DE(z)/ρ_DE0), which constant-a₀ MOND fixes at 1. The
three decisive predictions below are all evolution predictions, and all are **forward** (no z>2 kinematics exist yet).

## ★ The 3 decisive, distinctive, falsifiable predictions

| # | Prediction | Value | Tested against | Status |
|---|---|---|---|---|
| **1** | **The a₀(z)↔Λ bridge** (coefficient-free): a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE0) | 1.01, 0.86, 0.74 at z=1,2,3 | DESI w₀wₐ (input) × high-z galaxy dynamics | **forward** · distinctive |
| **2** | **High-z BTFR offset**: fixed-M_bar discs rotate slower, dlogV=⅛·log₁₀(ρ_DE ratio) | **−7.3% in V at z=3** (−0.033 dex), −16% at z=6 | JWST/ALMA z≳3 resolved rotation curves vs z=0 BTFR | **forward** · distinctive |
| **3** | **EFE strengthens with redshift**: e_N(z)=g_ext/a₀(z) ∝ 1/√ρ_DE | **+36% by z=3**; marginal galaxies cross to Newtonian | high-z grouped-galaxy kinematics — *no DM halo can fake an EFE (SEP violation)* | **forward** · distinctive |

**Sign test (the cleanest discriminator):** the high-z BTFR offset is **negative** (discs *below* the z=0 relation).
The rising √ρ_total reading predicts the *opposite* sign (+16% at z=1 to +80% at z=6); a third reading (1/R_e) rises
mildly (×1.8 at z=3). One clean z≳3 BTFR point splits all three. Übler+2017 KMOS³D matches the *direction* but the
magnitude (~0.001–0.025 dex over z~1–2.5) is below current per-galaxy scatter — existing data cannot yet decide.

**The decisive-test forecast (honest, DESI-limited):** statistically ~30 discs at z=3 → 3σ, ~60 → 5σ; **but**
marginalizing over the DESI w₀/wₐ uncertainty imposes a floor σ(β)≈0.5–0.6 *independent of sample size*, capping
single-redshift significance at ~1.6–2.0σ. **Clean 5σ needs multi-redshift BTFR (z=3 & z=5) *and* a ~2× tighter DESI
prior** — the bottleneck above ~30 discs is DESI, not telescope time (`combined_fisher_ultra.py`).

## The full set, by channel

| Channel | Prediction | Value (computed) | Real data | Status | Distinct? |
|---|---|---|---|---|---|
| **a₀ value** | a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ) | **9.355×10⁻¹¹ m/s²** (±0.96% stat, ±14% syst) | SPARC RAR best-fit (9.1×10⁻¹¹ simple-μ; 1.2×10⁻¹⁰ McGaugh) | consistent | shared |
| **Coefficient** | Z = cH_Λ/a₀ = √(32π/3); κ = ½ | **5.7888** and **0.5000** (exact, ℏ⁰); data band Z∈[4.2,6.0] | measured a₀ excludes Z=1,2,2.9 | consistent | distinctive (value) |
| **MDAR/RAR** | g_obs = g_bar·ν(g_bar/a₀) | scatter **0.195 dex** (175 SPARC, 3389 pts); deep-MOND −12% at z=3 | sparc_data/*_rotmod.dat | validated (z=0) | shared; evolution distinct |
| **BTFR** | V_flat = (G M_bar a₀)^¼, slope 4 | e.g. 10¹⁰ M_⊙ → 106 km/s | 175 SPARC galaxies | validated | shared |
| **Dwarf σ** | σ = (4G M a₀/81)^¼ (+EFE) | **5/8** classical dSph within ~40%; σ(z=3)=0.927 | 8 classical MW dSph (McConnachie 2012) | consistent (3 tensions) | shared; evolution distinct |
| **Lensing** | saturated α_∞ = 2π√(GMa₀)/c² (b-independent) | **0.51″/5.08″/16.1″** (10¹¹/¹³/¹⁴ M_⊙); non-monotonic, peak z~0.4 | KiDS GGL RAR (Brouwer+2021) | consistent/forward | shared; saturation+evolution distinct |
| **Clusters** | residual after MOND boost | **η = 1.92 ± 0.20** (misses ~1.9× at R500) | **9830 real eRASS1 clusters** (Bulbul+2024) | **tension (4.7σ)** | shared (inherited MOND failure) |
| **Wide binaries** | transition s_t=√(GM/a₀); EFE-suppressed boost | **9753 AU**; boost +2–11% | Gaia (contested: Chae yes / Banik null) | consistent (contested) | shared (no z=0 leverage) |
| **EFE (z=0)** | internal dynamics depend on g_ext (SEP violation) | detected ~4–5σ (Chae 2020, *published*; not reproduced here) | SPARC | consistent | distinctive vs dark matter |

## Meta-falsifiers (what kills it)

- **DESI reverts to w=−1** → a₀ constant → **no distinctive content left** (identical to ordinary MOND). The
  framework's distinctiveness is *hostage* to DESI's contested dynamical-DE signal (~2.8–4.2σ; verdict ~2027, DR3).
- **The high-z BTFR comes back flat-or-positive** when DESI says dynamical → direct falsification of the bridge.
- **A direct dark-matter detection** → kills MOND and this framework together.
- **The √ρ_total (rising) reading proves correct** → predicts the disfavored rising a₀.

## Honest non-predictions / open

- **The coefficient 32π is not uniquely derived** — data-selected to ~15% (the "4" = free-fall/Bekenstein–Hawking ½;
  `THE_FACTOR_OF_FOUR.md`). It cancels in the bridge, so it doesn't enter the decisive tests.
- **Clusters and the bullet cluster** are inherited MOND failures the framework does **not** fix.
- **Declining a₀ does *not* help** JWST's "too-massive-too-early" galaxies — an honest non-win.
