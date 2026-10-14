# CFG773: can the tether's field law be built on a bench?

**Label:**
- **ELECTRIC FORBIDDEN.**
- **MAGNETIC BUILDABLE** (Maxwell-Garnett composite) / **APPROXIMATE** (Bruggeman).
- **DEEP REGIME NOT REACHED.**

A composite of superconducting grains, with critical fields spread like a shape-1 Lomax distribution, reproduces the simple
μ(x) = x/(1 + x) exactly in effective-medium theory. With five real elemental superconductors it reaches it to rms 0.028.
It reproduces the law's *transition* (a boost of up to 2.5× in MG, 10× in BR), but not its flat deep-MOND tail.

A web search on 2026-10-14 found no prior MOND/AQUAL bench analogue.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (276866312). Block CFG770–779.
- **Script:** `python3 cfg773.py` (1 s, exit 0). `CFG773_MUTATE=1` exits 1 as designed. M1 bites; M2 does not (see Disclosures).

## Results

| step | result |
|---|---|
| **A1** electric | 0 of 10⁴ passive Drude–Lorentz media have ε(0) < 1; the Kramers–Kronig sum rule is reproduced to 3e-13. Gravity's polarization *anti-screens* (g > g_N), which needs ε < 1, and no passive dielectric can do that. **FORBIDDEN** |
| **A2** magnetic mapping | magnetic poles in a current-free nonlinear medium, ∇·(μ_r(H)H) = ρ_m, reproduce g_N = g²/(g + a₀) to 1.7e-14. Map: H ↔ g, B/μ₀ ↔ g_N, H₀ ↔ a₀. μ_r < 1 is allowed (superconductors: μ = 0) |
| **A3** exact design | superconducting fraction needed: MG f_s = 2/(2 + 3x), BR f_s = (2/3)/(1 + x). Both need a shape-1 Lomax (Pareto II) distribution of grain switching fields. Monte-Carlo (10⁵ grains): max \|Δμ\| 0.0025 (MG, f = 0.5, reaches x ≥ 0.667, boost ≤ 2.5×) and 0.0008 (BR, f = 0.6, x ≥ 0.111, boost ≤ 10×) |
| **A4** real metals | MG: H₀ = 8.7 mT with Al 0.43, In 0.26, Hg 0.09, Pb 0.11, Nb 0.11. rms \|Δμ\| 0.028 (max 0.073) over x = 0.67–30; B(H) monotone (stable). **BUILDABLE.** BR: rms 0.053. **APPROXIMATE** |
| **A5** analogue rotation curve | the longest flat run (\|dln(rH)/dln r\| ≤ 0.1) is 0.18 decades (MG) and 0.16 decades (BR), against ≥ 2.3 decades for the law (grid edge). **DEEP REGIME NOT REACHED** |

## Reading
1. **The bench can test the shape of the interpolation function**, μ(x) = x/(1 + x) over x ≈ 0.1–30. A field map around a
   magnetic pole embedded in a superconducting-grain composite (about 9 mT scale, below each metal's T_c) would show the
   law's transition. That is the part of the law SPARC actually constrains.
2. **The deep regime needs μ_eff → 0**, i.e. a superconducting network held just at percolation at low field. Effective-medium
   theory cannot be trusted there, so it is not claimed.
3. **What the bench cannot test:** cold energy, the tether's dynamics, a₀'s tie to ρ_DE, or anything gravitational. It is an
   analogue of one field equation, like Blanchet's dielectric picture made physical.

## Disclosures
- **M2 did not bite.** Multiplying alternate critical fields by 10^±1 gave rms 0.030 (MG) / 0.048 (BR), against 0.028 /
  0.053. The non-negative least-squares (NNLS) weights and the H₀ rescan absorb the shuffle: the fit depends on having about
  five critical fields spread over at least a decade, not on which metals. The tooth as frozen does not test material
  specificity. This is reported, not hidden.
- **Spurious warnings.** numpy 1.26 with Apple Accelerate prints divide-by-zero/overflow warnings in `matmul` at line 156.
  The values are finite and equal an explicit sum to 2e-16.
- Critical fields are from memory (provisional).
- Grain-size effects (λ_L), demagnetisation beyond the sphere intermediate state, and hysteresis are not modelled.
- MG is approximate at f = 0.5; Bruggeman is unreliable near percolation.
- κ fitted; not theory closed.
