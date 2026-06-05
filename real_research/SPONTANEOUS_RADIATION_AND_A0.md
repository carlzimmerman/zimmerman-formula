# Is there a relationship between "spontaneous radiation" and a₀ = c²√(Λ/32π)?

*An honest verdict from a 19-agent survey→compute→verify→synthesize workflow (6 routes: 0 genuine derivations, 5
same-scale coincidences, 1 shared-word-only). **C.Z. independently re-ran the three headline claims** — all confirmed.
Scripts: `reviews/spontaneous_radiation_a0_route.py`, `predictions/spontaneous_emission_route.py`.*

## Headline: same scale, **no derivation**, and the evolution comes out the **wrong sign**

Three things are true at once:

1. **The scale is real but it's dimensional analysis, not a prediction.** a₀ ≈ 9.36×10⁻¹¹ m/s² *is* the acceleration
   whose Unruh temperature equals the de Sitter (Gibbons–Hawking) horizon temperature — verified: T_dS = 2.20×10⁻³⁰ K,
   T_U(a₀) = 3.79×10⁻³¹ K, ratio **T_dS/T_U(a₀) = 5.789 = Z exactly**. But that ratio is just `cH_Λ/a₀ = Z` restated —
   a tautology, not new physics. Decisive tell: **a₀ carries ℏ⁰** (a₀ = c²√(Λ/32π) has no ℏ), so it is a *classical*
   surface-gravity scale, not a quantum-radiation output. ℏ cancels in every acceleration ratio.

2. **No spontaneous-radiation mechanism derives the coefficient 5.79.** The literal mechanisms (de Sitter
   Schwinger pair-creation, Volovik vacuum decay, the atomic Einstein-A coefficient) contain **no acceleration scale
   at all** — only the rate H_Λ. Forcing an a₀ out of them gives the **naive Z = 1** (a₀ = cH_Λ = 5.4×10⁻¹⁰, ~6× too
   big, **excluded by data**). The only *near*-fit is the **thermal 2π = 6.28** (a₀ = cH_Λ/2π) — but that 2π is the
   Gibbons–Hawking periodicity inserted *by hand*, it sits just past the data band's upper edge, and it is *different
   physics* from the framework's **classical ½** (which gives 5.79). So radiation points at 2π; the framework's 5.79
   is a free-fall/surface-gravity prefactor. The data can't yet separate 5.79 from 6.28 (~8%), but they are distinct.

3. **The evolution fails — the make-or-break.** Every *quantitative* radiation route ties a₀ to the **instantaneous
   Hubble/apparent horizon** (Gibbons–Hawking T set by H(z)): McCulloch QI, Cai–Kim, the redshifting atomic dS-bath.
   All give **a₀ ∝ cH(z) ∝ √ρ_total, RISING ×4.6 by z=3** — the *opposite* of the framework's *declining* √ρ_DE, and
   the branch already disfavored by high-z Tully–Fisher data. (Verified: E(z) = 1.79, 3.03, 4.57 at z = 1, 2, 3.)
   The framework's declining branch comes from tying a₀ to the **future event horizon / dark-energy density**
   (holographic Li-2004 cutoff, DESI dynamical DE) — a *separate idea from any radiation rate*. Telling: Volovik's "de
   Sitter spontaneously radiates matter" *does* decline (right sign!) but by ~10⁻¹²² per Hubble time and with **no a₀
   in the theory**. Milgrom himself wrote that the de Sitter lesson "does not tell us which cosmological acceleration
   parameter is to be identified with a₀."

## Routes table

| Route | Predicted a₀ | Z | In band? | Evolution | Grade |
|---|---|---|---|---|---|
| Atomic spontaneous emission (Einstein-A in dS bath) | none; ≤ cH_Λ | 1.0 | ✗ | rising √ρ_tot | loose analogy |
| Milgrom vacuum-MOND 1999 (Deser–Levin) | 5.4e-10 raw | 1.0 / 2π by hand | ✗ | constant | same-scale coincidence |
| Gibbons–Hawking dS horizon | 5.4e-10 / 8.6e-11 | 1.0 / 6.28 | ✗ | √ρ_DE only if event-horizon-tied | same-scale coincidence |
| McCulloch Quantised Inertia (a₀=2c²/Θ) | 6.6e-10…2.0e-10 | 0.83–2.65 | ✗ | rising √ρ_tot | same-scale coincidence |
| Volovik dS vacuum decay | none | — | — | declining ~10⁻¹²²/Hubble | shared word only |
| Fluctuation-dissipation / vacuum↔inertia | cH_Λ rigorous | 1.0 / ½ by hand | ✗ | √ρ_DE only by assumption | same-scale coincidence |

## A genuinely useful by-product: a clean three-way fork for the z~3 test

The routes surface a *third* evolution option distinct from both forks: the **event-horizon-radius** reading
`a₀ ∝ 1/R_e(z)` rises *mildly* (×1.4 at z=1, ×1.8 at z=3). So the z~3 BTFR/Tully–Fisher measurement resolves a clean
three-way split: **√ρ_total rises ×4.6 · 1/R_e rises ×1.8 · √ρ_DE flat-to-declining.** Worth folding into the z~3
forecast as a discriminator.

## Bottom line

**"Spontaneous radiation" and a₀ = c²√(Λ/32π) share a scale and a coefficient ambiguity — but it is a same-scale
coincidence, not a derivation.** No vacuum-radiation route reproduces the coefficient 5.79 (literal value Z=1,
excluded; near-fit the by-hand thermal 2π=6.28), and the framework's required *declining* √ρ_DE is **not** the natural
radiation output (which gives the *rising* √ρ_total of the Hubble horizon). The declining branch is a dark-energy
**density / event-horizon** statement, a different idea from any radiation rate. The route worth pursuing is the
**holographic (Li-2004 event-horizon) density side**, which the repo already keeps separate from the radiation rate.

**Sources:** [Milgrom 1999 (astro-ph/9805346)](https://arxiv.org/abs/astro-ph/9805346) ·
[Yu & Zhou 2008 (0802.2018)](https://arxiv.org/pdf/0802.2018) ·
[Volovik 2024 (2312.02292)](https://arxiv.org/abs/2312.02292) ·
[McCulloch 2016 (1610.06787)](https://arxiv.org/abs/1610.06787) ·
[Zhu & Yu (gr-qc/0701041)](https://arxiv.org/abs/gr-qc/0701041)
