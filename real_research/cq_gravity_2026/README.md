# L313 — postquantum classical gravity priced on the framework's gates

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
