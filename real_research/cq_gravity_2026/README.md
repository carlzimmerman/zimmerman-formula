# L313–L315 — postquantum classical gravity, and the phantom law against SPARC

## L313 — postquantum classical gravity priced on the framework's gates

`L313_cq_rectification_lensing.py` (20/20, rc=0; `MUTATE=1` breaks the Einstein routine and fails the Isaacson and Schwarzschild controls, rc=1). Run it from the repository root. The output is in `.out`, and the results are in `_results.json` for the main run and `_results_MUTATE.json` for the mutation run.

**Why this lane exists.** One external theory claims the framework's tie a₀ ∝ √Λ from first principles, and the repository had never engaged it. That theory is Oppenheim & Russo 2024 (arXiv:2402.19459), working in postquantum classical gravity (Oppenheim, PRX 13, 041040), with a critique by Hertzberg & Loeb, JCAP 09 (2024) 046. The theory's metric noise is classical, so it is the one mechanism that escapes the 2026-09-01 ħ-counting no-go on graviton-bath drift.

**Method.** The observable is derived from the averaged second-order Einstein tensor for a stochastic metric −(1+2Φ)dt² + (1−2Ψ)dx², worked in the short-wavelength (Isaacson / Green–Wald) regime. The phantom's lensing/dynamics ratio is fixed by ε = (p_r+2p_t)/ρ_eff. That is scored against the committed KiDS gate |ε| < 0.0489 at 1σ (sf38). The machinery reproduces Isaacson's gravitational-wave stress and exact Schwarzschild.

| Result | Number | Status |
|---|---|---|
| OR24's coefficient, completely positive β < 0 | κ = 1.30–1.45 vs measured 0.465 ± 0.076 | ≥ 11σ off |
| κ = ½ inside OR24 | needs β = 0.2353 (outside complete positivity) | reachable only by dropping positivity of correlations |
| OR24 as a Tully–Fisher normaliser, β → −∞ | a₀ = 2cH_Λ exactly (Milgrom 1999) | excluded (15.6σ on record) |
| OR24's γ₁r term (constant acceleration) | lensing-RAR slope 0 vs 0.537 ± 0.026 (L248) | 20σ |
| Phantom carried by GR-compliant fluctuations (waves, any graviton bath) | w = 1/3, lensing/dynamics = 0.75 | 11σ, independent of convention |
| Static scalar noise, Einstein–Langevin ⟨G_μν⟩ | min \|ε\| = (√53 − 7)/4 = 0.0700; lensing ≥ 3.8% above dynamics | 1.6σ, **not excluded**; sign and floor are a falsifier |
| OR24's own ansatz φ = ψ | ε = −1/9; lensing +6.2% | 2.6σ |
| Pure lapse noise; OR24's white-in-time limit taken literally | active mass < 0 | rectifies to **repulsion** |
| Averaging convention for constraint-violating noise | min \|ε\|: lower 0.070, mixed 0.10, densitized = no active mass, upper = 0 | the lensing prediction moves at O(1) with the convention |
| Static noise plus a fast anti-correlated component | ε = 0 reachable (weight 0.06–0.28 at 1σ) | lensing alone does not close the class |
| Amplitude the noise must carry to be the phantom | rms acceleration ≈ 1100× the mean field at r_M | underived; D₀ is free, κ stays measured |

**Standing.** The published coefficient is excluded. The shape is excluded. Any phantom made of gravitational-wave energy is dead. The one live corner is constraint-violating quasi-static scalar noise, which only classical-quantum gravity supplies, and it is open but unpriced. Its lensing is undetermined until the theory states which tensor density its noise is unbiased in. On the standard Einstein–Langevin convention it predicts lensing ≥ 3.8% above dynamics, which a 1%-level Euclid/LSST lensing-versus-kinematics comparison decides. This lane derives neither κ nor the amplitude law, so do not cite it as a derivation.

## L314 — the homogeneous-noise pincer (closes L313's live corner for the published theory)

`L314_cq_homogeneous_noise_pincer.py` (4/4; `MUTATE=1` uses a background that does not solve Poisson, and S1 fails, rc=1).

- Around its saddle, the Oppenheim–Russo action is −c₀(1−β)/G² (∇²δΦ)² with **no m(x)**. The noise statistics are therefore exactly independent of the matter, and every rectified density is uniform.
- **Shape:** a uniform density gives a lensing-RAR slope of −½, against the measured +0.537 ± 0.026. That is 39σ off.
- **Magnitude:** a density large enough to be a galaxy's phantom at r_M is ≥ 4×10⁴ times the whole cosmic dark-matter density on every footing, and still ≥ 400 times it at 10 r_M.
- The relativistic weight √−g adds only O(v²/c²) ≈ 4×10⁻⁷ of source dependence, while the phantom's contrast across a galaxy is ~10⁴.

**Standing:** postquantum classical gravity is **closed** as a source of the phantom and of κ. It survives only as a host with a diffusion kernel D₀(x) tuned by hand to the MOND law, which is a reparametrisation.

## L315 — the phantom law (L311/L312) against SPARC

`L315_phantom_law_vs_sparc.py` (5/5; `MUTATE=1` swaps in data where the law is true, and the kill checks fail, rc=1). The sample is SPARC with Q ≤ 2 and i ≥ 30°: 151 galaxies and 2,361 points in the law's domain x ≤ 1. All errors come from a galaxy bootstrap. Injection-recovery gives A = 1.02 ± 0.04 when the law is injected and 0.00 when it is absent.

| Reading | Active-mass amplitude A (the law needs 1) | Within-galaxy shape |
|---|---|---|
| **The law as written**, g² = a₀ g_N,tot, a₀ = cH_Λ/Z fixed | 0.70 ± 0.13 at Υ = 0.5 (2.2σ); **0.24 ± 0.17 with M/L profiled (4.4σ)** | 3.8σ off |
| As written, a₀ free | 0.00 (a₀ moves to 1.44e-10) | — |
| Embedded in the ν_RAR kernel: literal / self-similar / enclosed | 0.00 / 0.00 / 0.10 ± 0.14 (≥ 6.5σ) | 13.6σ / 17.3σ / 4.6σ |
| Head-to-head at the law's own a₀ | the kernel with **no** active mass fits better: Δχ² = +5429 ± 1330 (4.1 bootstrap σ); 83% of galaxies prefer it | — |

**Standing:** on its own terms the phantom law is **disfavoured at about 4σ, not killed**, and its active mass is not needed by the data. L312's I3 mass slope is not a discriminator: it sits 0.9σ from the data, so the law fails on its level and its shape instead. With M/L profiled per galaxy, the ordinary kernel wants a₀ ≈ 9.8×10⁻¹¹ (5.6% grid), consistent with κ = ½.
