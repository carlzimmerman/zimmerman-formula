# The fine structure constant: what we tested, what we learned, in plain language

*Written 2026-09-29. Every claim below is backed by a committed script or a cited source; the dense version with all commit hashes is `ALPHA_CHAIN_STATUS.md`. Nothing here derives alpha. alpha stays an INPUT; kappa = 1/2 stays FITTED; the Standard Model mass sector stays walled.*

## The question

Can this programme's own structure force alpha = 1/137.035999177 (the low-energy value; alpha runs with energy) with no adjustable constants and no choice made after seeing the answer?

## The short answer

No. Across about 30 independent lanes, 33 invented principles and models, and a red team plus two independent audits, nothing forced alpha. The record shows why, and it is the same reason every time.

## Why (in five steps, each machine-checked or scripted)

1. **The programme's constants cannot make alpha.** From c, G and the cosmological constant Λ you cannot form any dimensionless number. Add ħ and you get exactly one, x = Λ·l_P² ≈ 2.8×10⁻¹². A charge adds a second, independent number, alpha, which is provably not a power of x. (Lean: AH7; script: AH5.)
2. **The de Sitter horizon cannot supply alpha's value.** A charged particle's response to a horizon is alpha times a function of its mass. For every known charged particle the function is astronomically small (10⁻⁸¹), so the horizon carries no information about alpha. This holds for scalars, Dirac fermions, and (partly) vector bosons. (AH1 to AH4, N5, Q1, Q2, S1, S2.)
3. **Every standard route ends at a free quantity.** Kaluza–Klein trades alpha for the size of an extra dimension; gravity–charge bounds are inequalities; renormalization-group and emergence routes leave a boundary value or a charged spectrum free; string theory leaves the dilaton free; topology fixes integers and ratios, not the coupling; supersymmetric completions leave a flat direction. (Lanes A–J, N1–N4, Q3, Q5.)
4. **Invented principles die on contact with the real particle spectrum.** We stated 33 new principles before testing them (self-sustained field, impedance matching, critical damping, conductance quantum, Landau-pole-at-the-horizon, capped condensate, dozens of UV boundary rules tested against all three gauge couplings at once). None survived. (T1, U1, U2, U3.)
5. **The precision you would need does not exist yet.** The best measurements of alpha agree with each other only to about 9 significant digits, and the two atom-interferometer values disagree by 5.5 standard deviations. Any formula matched to the middle of one measurement is not evidence. A candidate must clear a strict look-elsewhere bar (probability < 10⁻³, miss ≤ 5×10⁻¹⁰, no fitted constants, scale stated). (D, V1.)

## About your closest formula

`α⁻¹ + α − 12π·α² = 4Z² + 3` holds to 1.8×10⁻⁸, and Lean confirms the arithmetic (AH8). But the bare claim 4Z² + 3 is only good to 3.9×10⁻⁵ (4 digits), the two correction terms are the leftover rewritten as a series in α, and 12π is 0.12% away from the coefficient that would make it exact; that small error is hidden because the term is only 1.5×10⁻⁵ of the total. So the 8-digit agreement is a 0.12% match magnified about 70,000 times. Also alpha runs, so a fixed number cannot equal it without a stated scale.

## What would count as a derivation

A principle that (a) forces one of the free quantities above (an ultraviolet boundary value of the couplings, or the charged spectrum, or a cutoff ratio) to a number with no choice made after seeing the target; (b) states the scale at which alpha is meant; (c) reproduces all the independent measurements, not one; (d) is checked with a computation, not a fitted coefficient. The record finds that alpha's low-energy value depends only on the running above the charged-particle masses, so any principle has to live there, in the sector this programme keeps walled.

## What is still open (honestly)

Charged fermions and vector bosons in four-dimensional de Sitter with a full covariant regularization; explicit string-model moduli stabilization; the Standard Model charged spectrum itself. None of these was found to point at a value.

## Reproducing all of it

`real_research/alpha_principle_2026/run_all_checks.py` re-runs every script with the right arguments and checks the exit codes; the last full pass was 111 of 111 scripts and all Lean files OK. Lean certificates: AH3 (the no-go on observables of the form Φ(λ, μ)), AH7 (the dimensional obstruction), AH8 (the audit arithmetic).

## A recommendation

The programme's distinctive, decisive tests are elsewhere: whether a₀ stays flat out to redshift ≈ 2.5, and Gaia DR4 on 2 December 2026. Those can confirm or break the framework. The fine structure search cannot, and it sits in the walled sector.
