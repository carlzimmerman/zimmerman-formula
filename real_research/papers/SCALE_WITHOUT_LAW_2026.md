# Scale Without Law: Why the de Sitter–Unruh Temperature Forces the MOND Acceleration but Not the Interpolation

**Carl P. Zimmerman** · Briar Creek Tech · 2026-06-28

## Abstract

The MOND acceleration scale satisfies a₀ ≈ c²√(Λ/32π) = cH_Λ/Z to within a factor of order unity — the long-noted coincidence that the scale of galactic dynamics equals a scale built from the cosmological constant. Milgrom (1999) proposed reading this as a vacuum effect: an observer accelerating in de Sitter space sees the Deser–Levin temperature T(a) ∝ √(a² + a_Λ²), with a_Λ = cH_Λ, and the *excess* over the de Sitter background, ΔT = √(a²+a_Λ²) − a_Λ, has the asymptotic form of a MOND inertia. This note asks, with explicit and adversarially-checked calculation, **how far that mechanism actually goes** — and reports an honest, two-sided result. The de Sitter–Unruh temperature **forces the scale** (a₀ ~ c√Λ is recovered, not assumed) and yields the **deep-MOND √-law and the baryonic Tully–Fisher relation** (both exact). It does **not** yield the full interpolation function, the precise coefficient, or a covariant equation of motion — the standing open problem since Milgrom 1999. We make the obstructions precise and contribute three results: (i) the candidate interpolation μ_fw = (√(1+4x²)−1)/2x and the bare dS–Unruh interpolation μ = (√(1+x²)−1)/x are the **same one-parameter family**, separated by a single rescaling, so the whole gap collapses to one undetermined coefficient Z; (ii) a **number-field obstruction** — thermodynamic normalizations lie in ℚ(π) while Z = √(32π/3) lies in ℚ(√π) — proving that no horizon-entropy or temperature factor can ever output the coefficient; (iii) a **strengthened sign theorem** showing the MOND-signed response requires breaking ghost-freedom or supplying an active drive, which blocks a passive-bath covariant completion. The conclusion is deliberately modest: the de Sitter–Unruh route owns the *scale* and the deep-MOND *limit* but not the *law*, and the residual freedom is now reduced to a single, provably-unforced number. This is offered as a map of the obstruction, not a derivation of MOND, and not a theory of anything beyond gravity.

## 1. What the mechanism delivers

Take the Deser–Levin temperature for an observer of proper acceleration a in de Sitter space (Deser & Levin 1997; Narnhofer, Peter & Thirring 1996),

> T(a) = (ℏ/2πck_B) √(a² + a_Λ²),  a_Λ = cH_Λ,

and Milgrom's (1999) postulate that inertia responds to the excess over the de Sitter vacuum, ΔT(a) = √(a²+a_Λ²) − a_Λ. Two things follow without further input (`reviews/deser_levin_mond_derivation.py`, exit 0):

- **The scale is forced.** The transition between the two regimes occurs at a ~ a_Λ = cH_Λ; the acceleration scale is *built from Λ*, not inserted. The a₀ ~ c√Λ coincidence becomes a consequence.
- **The deep-MOND limit is exact.** For a ≪ a_Λ, ΔT ≈ a²/2a_Λ; with the inertial force ∝ ΔT, requiring it equal the Newtonian g_bar gives a = √(2 a_Λ g_bar) — the deep-MOND square-root law. The baryonic Tully–Fisher relation V⁴ = G M a₀ follows (symbolically exact).

This is real, and it is the genuine content of Milgrom's proposal. It is also where the easy progress ends.

## 2. The interpolation: one family, one coefficient (Gap A)

The framework's interpolation, written as g_obs = √(g_bar² + g_bar a₀), is equivalent to the convex function μ_fw(x) = (√(1+4x²)−1)/(2x) with x = a/a₀. The bare excess-temperature postulate of §1, by contrast, yields μ(x) = (√(1+x²)−1)/x. These look different, and a referee would ask which the mechanism actually predicts. The answer (`reviews/close_mu_from_temperature.py`, exit 0, sympy):

> **They are the same one-parameter family.** μ_dl(x) = μ_fw(x/2) exactly; the only difference is a rescaling of the acceleration unit, i.e. a redefinition of the coefficient relating a₀ to a_Λ. The "two interpolation gaps" are one gap: the undetermined number Z.

We tested six principled couplings of inertia to T(a). One — the free-energy reading φ = −T(a), μ = dφ/da = x/√(1+x²) — is genuinely principled, has the correct Newtonian and deep-MOND limits, *and* the correct (MOND) sign. But it produces the **simple-ν** interpolation, not μ_fw, and the choice of free energy is not forced. Reaching μ_fw *exactly* requires inserting the coefficient by hand. That this is reverse-engineering and not derivation we prove constructively: the floor-fit that "recovers" the framework's form reproduces an entire decoy family g_obs² = g_bar² + k·g_bar·a₀ for k = ½, 1, 3, 7/4 *equally well* — it has zero power to discriminate the coefficient. **The interpolation is a posit; what the mechanism fixes is the family, not the member.**

## 3. The coefficient: a number-field obstruction (Gap B)

The bare mechanism's coefficient comes out a₀_eff = 2a_Λ = 2cH_Λ; the framework's is a₀ = cH_Λ/Z with Z = √(32π/3) ≈ 5.789. Can a defensible normalization — the Unruh 2π, the Bekenstein–Hawking ¼, a surface-gravity ½, the dimension factor d(d−1) = 6 — bridge the factor 2Z? We checked each (`reviews/close_coefficient_Z.py`, exit 0). None does, and there is a clean reason:

> **Thermodynamic normalizations live in the field ℚ(π); Z = √(32π/3) lives in ℚ(√π). The two fields do not meet.** A factor assembled from 2π, ¼, 4π, 6, … is rational-in-π and can *bracket* Z (indeed 6 and 2π straddle 5.79) but can never *equal* it. Only an intrinsic √ρ route — a₀ = (c/2)√(Gρ_DE) — lands on Z exactly, and there the ½ prefactor and the ρ_DE-vs-ρ_total choice are provably free (Z ∝ 1/κ).

The tempting factorization Z² = 4·(8π/3) does not rescue it: carried symbolically, the "4" is 1/κ² and equals 4 only at the posited κ = ½ — it is the free prefactor squared, not the area-law ¼. **The coefficient is defined, not derived. It is the one number everything reduces to, and it is unforced.**

## 4. The equation of motion: a negative theorem (Gap C)

A genuine modified-inertia theory needs an action giving F = m μ(a/a₀) a. We re-examined the three routes adversarially (`reviews/close_covariant_eom.py`, `verify_closure_covariant_eom_adversarial.py`, both exit 0, 11/11 attacks survived):

- **Local, time-nonlocal action** → Ostrogradsky ghost (the worldline Hessian is non-degenerate; the DHOST/auxiliary-field escape Legendre-transforms the nonlinearity straight back unless the coupling itself carries the time-nonlocality, i.e. it *is* the nonlocal route).
- **Field-theoretic completion** (khronon/Galileon) → the static slip carries a non-vanishing divergence, fixed by the Solar-System (Cassini) bound; a divergence-free completion is radiative and produces no static MOND force.
- **Nonlocal worldline action** → ghost-free, but the MOND-signed kernel must be **active**: a passive de Sitter bath gives a positive mass renormalization, δm = 2∫ρ(ω)/ω² dω ≥ 0, i.e. the *anti-MOND* sign. We strengthen the standing result: this needs **only ghost-freedom of the bath modes**, not passivity or fluctuation–dissipation; the finite-frequency apparent-escape lives in the Newtonian band and falls as 1/ω², the wrong monotonicity for MOND.

There is no fourth route, and the no-go uses none of {Z, a₀, μ_fw} — it would even forbid an anti-MOND theory. The single honest crack is external: a **non-de-Sitter, in-band, phase-coherent drive** (a "galactic pump") could supply the active kernel — but none is known, and it would still owe an explanation of a₀'s universality.

## 5. The one observational handle

The mechanism's distinctive, falsifiable content is not the static algebra but the *time* dependence. If a₀ is genuinely set by the dark-energy density, then a₀(z) ∝ √ρ_DE(z): on the DESI dynamical-dark-energy branch it declines (~25–40 % by z = 3); under a true cosmological constant (w = −1) it is constant. This is the one place the de Sitter–Unruh reading is separable from a static coincidence — and it dies cleanly if dark energy proves to be Λ.

## 6. Conclusion

The de Sitter–Unruh temperature forces the MOND **scale** and reproduces the deep-MOND **limit** — Milgrom's 1999 insight, made exact. It does not produce the **interpolation** (which collapses to a single undetermined coefficient), the **coefficient** itself (number-field-obstructed; defined, not derived), or a **covariant equation of motion** (blocked by an Ostrogradsky/Cassini/sign-theorem trichotomy). The honest standing is therefore unchanged from 1999 in substance, but sharpened in form: the gap between "the scale" and "the law" is now reduced to one provably-unforced number and a clean sign obstruction, both stated as theorems rather than impressions. We claim no derivation of MOND, no fixing of the coefficient, and nothing about the Standard Model; the value here is a precise map of where an inertia-from-vacuum programme must still do work, and the identification of the single quantity on which everything turns.

## References (representative, real)
- M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A 253 (1999) 273.
- S. Deser, O. Levin, *Accelerated detectors and temperature in (anti–)de Sitter spaces*, Class. Quantum Grav. 14 (1997) L163.
- H. Narnhofer, I. Peter, W. Thirring, *Unruh effect in de Sitter space*, Int. J. Mod. Phys. B 10 (1996) 1507.
- B. Famaey, S. McGaugh, *Modified Newtonian Dynamics: Observational Phenomenology and Relativistic Extensions*, Living Rev. Relativity 15 (2012) 10.
- M. Milgrom, *MOND theory*, Can. J. Phys. 93 (2015) 107 (modified-inertia / nonlocal formulations).

*Reproducible: `reviews/{deser_levin_mond_derivation, close_mu_from_temperature, close_coefficient_Z, close_covariant_eom, verify_closure_gapA_adversarial, verify_closure_covariant_eom_adversarial}.py` (all exit 0). Footing a₀ = c²√(Λ/32π) = cH_Λ/Z, Z = √(32π/3). The author retracted all earlier "theory of everything" claims (2026-06-23); this note makes none, and is a foundations/obstruction map, not a derivation.*
