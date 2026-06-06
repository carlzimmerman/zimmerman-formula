# The MOND interpolation function is DERIVED from the vacuum — tested on 175 SPARC galaxies, no dark matter

*C. Zimmerman, 2026-06-06. Forward research, fully inside the framework (emergent gravity, no dark matter). The deepest
tractable question: is the *shape* of the radial-acceleration relation — MOND's interpolation function — predicted by
the vacuum, or just fit? Result: the framework's emergent-gravity origin predicts the RAR shape with **zero shape
freedom**, and it fits all 175 SPARC galaxies — a prediction ΛCDM cannot make. It's not yet *uniquely* confirmed
(degenerate with empirical fits at today's precision), and the real discriminator is non-circular dynamics. Script:
`rar_emergent_discriminate.py`.*

## The prediction (derived two independent ways)
The framework is emergent gravity sourced by the vacuum; de Sitter–Unruh **modified inertia** gives a *specific*
interpolation, with **no free shape**:
> `g_obs = √(g_bar² + g_bar·a₀)`  (equivalently `ν(y)=√(1+1/y)`, `y=g_bar/a₀`).

I verified this falls out **two ways**: (a) `μ(a)=[√(a²+(cH)²)−cH]/a`; (b) the Luo 2026 form
`μ(x)=(√(1+4x²)−1)/2x` — *both* reduce to the same `g_obs(g_bar)`. So the shape is a robust consequence of the
vacuum-temperature origin, not a chosen fitting function. **ΛCDM has no analog**: in ΛCDM the RAR is an emergent
by-product of feedback + halos with intrinsic scatter; it predicts no functional form.

## The test (175 SPARC galaxies, 3389 points, no dark matter)

| interpolation | best a₀ [10⁻¹⁰] | RAR scatter [dex] |
|---|---|---|
| **emergent (DERIVED)** `√(g_bar²+g_bar a₀)` | 1.78 | **0.105** |
| McGaugh 2016 (empirical fit) | 1.36 | 0.101 |
| "simple" μ=x/(1+x) | 1.32 | 0.100 |

**The derived shape — with zero shape freedom — fits as well as the best empirical fit** (0.105 vs 0.101 dex,
difference 0.005 dex, negligible). That is a genuine success: the framework predicts the entire `g_obs(g_bar)` curve,
and 175 real galaxies accept it, with **no dark matter**.

## Honest: consistent, not yet UNIQUE — and where the discriminator is
The emergent shape does **not** beat the empirical fits (it's degenerate at 0.10 dex). The forms diverge only in the
**transition region**:

| y=g_bar/a₀ | ν_emergent | ν_McGaugh | diff [dex] |
|---|---|---|---|
| 0.1 | 3.32 | 3.69 | 0.046 |
| 0.3 | 2.08 | 2.37 | **0.057** |
| 1.0 | 1.41 | 1.58 | 0.049 |
| ≥10 | → agree | → agree | 0.00 |

The deep-MOND tail and the Newtonian limit **agree** (both → `√(g_bar a₀)` and → `g_bar`); the forms differ ~**0.06
dex** only at `y~0.3–1`. To distinguish them in the RAR you need transition-region precision below ~0.06 dex — right at
the intrinsic-scatter floor. So the RAR alone is *marginal* for confirming the emergent shape.

**The real discriminator is non-circular dynamics.** The emergent prediction is **modified INERTIA** (the inertia of a
mass depends on its acceleration *history*, non-locally), which is genuinely distinct from modified *gravity* (a local
force law) — and the RAR, measured on near-circular orbits, can't tell them apart. They diverge in **eccentric orbits,
the external-field effect, and vertical disk dynamics.** That is where the vacuum-origin of MOND is decisively
testable — and it's the framework-internal forward frontier (the EFE is also the one ΛCDM-impossible MOND signal).

## The scale a₀ — the known coefficient posit (shape doesn't depend on it)
The framework's `a₀ = c²√(Λ/32π) = 0.94×10⁻¹⁰` is **1.4–1.9× below** the RAR-preferred value (1.32–1.78, μ-form
dependent; the framework's own emergent μ wants 1.78). This is purely the **unfalsifiable coefficient** (the "32π" is a
posit; the data prefer ~28; both are O(1)·c²√Λ). It cancels in every a₀(z) ratio test and **does not touch the shape
prediction.** So: *shape derived (and tested); scale set by Λ up to the free coefficient.*

## Forward verdict (no dark matter)
- **Genuine success:** the framework predicts MOND's interpolation function from vacuum thermodynamics — a
  zero-shape-freedom prediction ΛCDM cannot make — and it fits 175 SPARC galaxies at 0.10 dex with **no dark matter**.
  This is the framework's core IR claim, holding on real data.
- **Honest limit:** the RAR can't yet *uniquely* confirm the emergent shape (degenerate at 0.06 dex in the transition).
- **The decisive next test** is non-circular dynamics — the external-field effect / eccentric-orbit / vertical-force
  signatures where **modified inertia (the vacuum prediction) ≠ modified gravity**. That confronts the framework's
  actual mechanism, uses data in hand (SPARC EFE, the Milky Way vertical force, wide binaries' orientation dependence),
  and is the genuine frontier — no dark matter anywhere in it.

*Sources: SPARC [Lelli+2016]; de Sitter–Unruh modified inertia [Milgrom 1999; Luo 2026, 2602.14515]; RAR [McGaugh+2016,
1609.05917]; a₀–Λ [Milgrom 1110.2580].*
