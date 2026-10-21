# W4-21: π bookkeeping for the medium ratio. FILTER HOLDS (a screen, not a selection)

**Bottom line.**
- W4-04 turned "why ξ = ¼" into one target for any single-mediator medium: **R ≡ εC₃²/C₂³ = 128π/9**. That number carries
  exactly **one** power of π.
- **Any medium whose π's all arrive attached to a scale gives an R with no π at all.** Examples are thermal media (πθ) and
  H-type routes (8πG/3 used consistently). R combines one ε and two C₃'s over three C₂'s, and 1 + 2 − 3 = 0, so every common
  factor and every scale cancels, and the π's attached to them cancel too.
- Then ξ = 8Ω_n/(9R) keeps the sphere's π and is **never ¼, in any spatial dimension** (n = 2–5 checked: weight 1, 1, 2, 2).
- The record's thermal miss (W4-04: 16/5, 16/15) and its H-type misses (W4-05, W4-07, W4-19: R = 4/9, √3/9, 4/3, 2/3) are
  **the same failure**. The thermal route was doomed by π content alone, before its sign and state problems.
- **Necessary condition** for ξ = ¼ at n = 3: wt ε + 2·wt C₃ − 3·wt C₂ = 1. With every weight in {−1, 0, 1} it has exactly
  three solutions, listed below.

**κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095). A screen fixes nothing, and passing it is not evidence for ½. Not theory
closed.

## In plain words

Write each of the three medium numbers as a fraction times some power of π. The target 128π/9 needs one π left over after
forming ε × C₃ × C₃ ÷ (C₂ × C₂ × C₂). If every π in the medium rides along with a temperature or a Hubble rate, it cancels
exactly as the temperature does, and R comes out a plain fraction such as 16/5. A plain fraction can never equal 128π/9. So
the winning medium needs a π that belongs to no scale: one from geometry or topology, sitting in the right coefficient.

## Results (`w4_21.out`; footing ρ_DE; n = 3 unless stated)

| check | what | result |
|---|---|---|
| K1 | A1 dictionary re-derived from the two asymptotes and the flux law; the deep regime is g² = g_N a₀ | ξ = 8ΩC₂³/(9εC₃²); R* = 128π/9, weight 1 |
| K2 | W4-04 thermal coefficients | R = **16/5** (ε_rad) and **16/15** (\|F(0)\|), weight 0 |
| K2b | glued form | each coefficient = (π-free) × π⁻² × (πθ)^p, p = 4, 2, 1 |
| K2c | high-T coefficients π²/90, 1/24, 1/(12π) against the bosonic integral (mpmath, 30 digits) | residual/cubic 0.0158 → 0.0087 (y 0.02 → 0.01), the expected y ln y tail |
| K3 | L1 symbolic, generic glued coefficients; two glued scales; two-scale control | R = r_e r₃²/r₂³ (free of Q, s, π); the control keeps (θ/M)⁶, so H1 is needed |
| K4 | record H-type κ² mapped through A1 | EiBI and Zhao 4/9, f(R) √3/9, DGP 4/3, PM/conformal 2/3, all weight 0 |
| K5 | Ω_n for n = 2–5 | weight 1, 1, 2, 2: algebraic R never gives ¼ |
| K6 | L3 solutions with \|w\| ≤ 1 | (wt ε, wt C₃, wt C₂) = **(1, 0, 0), (−1, 1, 0), (0, −1, −1)** |
| I1, I3 | forbidden constants; invariance under a common factor Z and under φ → sφ | pass |

## The three shapes that survive the screen

1. **(1, 0, 0).** The vacuum energy carries one π that the stiffnesses don't: a vacuum term that is itself a flux or
   solid-angle quantity. Equivalently ε = 32π × C₂h*², which is 32π times the Newtonian field energy at the crossover
   h* = 2C₂/(3C₃).
2. **(−1, 1, 0).** The vacuum carries 1/π and the MOND stiffness carries π.
3. **(0, −1, −1).** Both stiffnesses carry one 1/π from the same source, and the vacuum carries none. One example is a
   quantized level k/(4π) multiplying both stiffness terms.

Each is only a necessary condition. A medium of any of these shapes still has to give the right fraction, pass W4-04's
health and force tests, clear S1–S8, and make a second prediction.

## Correction disclosed

The chat summary that led to this lane said "a Chern–Simons-type k/(4π) gives one free π". That is right only for where it
sits. On C₃ alone it gives weight −2. On both stiffnesses (shape 3) it gives +1. L3's table replaces the earlier wording.
This correction was frozen in the criteria before any script ran.

## Scope

- **D1.** Weights are defined only on numbers of the form (algebraic) × π^w, W4-02 Claim C's restricted grammar. A medium
  whose coefficients involve ζ(odd), Euler's γ or logarithms is outside the class, and the screen says nothing about it.
  Thermal media in odd spacetime dimension bring ζ(D), for example.
- **Glued means one weight per scale in all three coefficients.** A route that attaches π to H differently in different
  places is not glued. For example, a₀ = cH/2π puts 8π/3 in ε but 1/2π in a₀.
- **Single mediator only** (W4-04's A1). A tensor-plus-mediator theory must redo G before this applies.

## MUTATE (`w4_21_MUTATE.out`, exit 1 by design)

- **MU1, un-glue ε** (π²θ⁴/90 → πθ⁴/90): R → 16/(5π), weight −1. K2 and K2b fail. Bites.
- **MU2, n = 3 → 4:** R* → 64π²/9, weight 2. L3's right-hand side becomes 2 and K6 fails. Bites.
- Untouched checks (K2c, K3, K4, K5, I1, I3) still pass.

## Files

- `FROZEN_CRITERIA.md`: committed alone, a67f9ed9c, under the number W4-20. Another session's lattice lane took W4-20 34 s
  later and finished first, so this lane was renumbered W4-21. The criteria's appendix records the renumbering; no criterion
  changed, and the first run under the old names gave the same results.
- `w4_21.py`: sympy plus mpmath, single core, 0.6 s, 63 MB.
- `w4_21.out` / `w4_21_results.json`: the normal run.
- `w4_21_MUTATE.out` / `w4_21_results_MUTATE.json`: the control run.

## Appendix (2026-10-20, from W4-22 K0): the three shapes are one class

The three solutions listed above are **one condition, not three kinds of model**. Two conventions leave R unchanged:
- multiplying ε, C₂ and C₃ by a common factor shifts the weights by (1, 1, 1);
- rescaling the field φ → π^g φ shifts them by (0, 3g, 2g).

These shifts span every solution of wt ε + 2 wt C₃ − 3 wt C₂ = 0 (checked in W4-22 K0). So the screen's only invariant
content is **wt R = 1**. The arithmetic above stands; the reading "three shapes" is withdrawn. W4-22 builds a model in this
class.
