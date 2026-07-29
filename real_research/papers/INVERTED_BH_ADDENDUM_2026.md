# One Rational Number, and a Stress-Test of the Inverted-Black-Hole Null

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · 2026-07-29*

*Addendum to "The Inverted Black Hole: Why the de Sitter–MOND Acceleration Scale Is Uniquely
Cosmic" (DOI 10.5281/zenodo.20947913) and "One Free Number" (DOI 10.5281/zenodo.20938891).
All numbers are printed by committed scripts named per section, in the repository linked below.*

---

## Abstract

Three results, one of them a correction of presentation in the parent papers.

**First, the coefficient reduces to a single rational.** The parent note writes
`a₀ = cH_Λ/Z` with `Z = √(32π/3)`, factored as "the Einstein coupling 8π times the Friedmann 3,
with a single free outside factor of 2." That factorisation is now exact and complete: writing
`32π` as `8π/κ²` and substituting `Λ = 8πGρ_Λ/c²`, **every π, the 32 and the 3 all cancel**, and

> **a₀ = κ · c · √(G ρ_Λ)**, exactly, with **κ = 1/2**.

So "32π/3" is not a compound of three geometric factors — it is an artifact of routing one
statement through Λ and Einstein's 8π. The framework's entire dimensionless content is the single
rational **κ = 1/2**, and the honest form of the open problem is "why κ = ½", not "why 32π/3".
This strengthens the *One Free Number* thesis: the number is not merely single, it is rational, and
the transcendental `√π` that the parent papers carry belongs to **general relativity**, not to this
framework.

**Second, the inverted-black-hole null survives a deliberate attack, for a stronger reason than
the parent note gave.** That note argues the universal crossover `r_cross = √Z · r_s = 2.406 r_s`
self-cancels into exact GR via (a) mass-independence and (b) the free-fall/Hartle–Hawking theorem.
Argument (b) protects only *geodesic* observers, which is a real gap: a **static** observer at
radius `r` has proper acceleration `a = (GM/r²)/√(1 − r_s/r)`, which is non-zero and diverges at
the horizon. We evaluate the framework's own kernel for exactly that observer at exactly `r_cross`.
The fractional deviation from Newtonian inertia is

| hole | a_proper at r_cross (m s⁻²) | ν − 1 (cosmic a₀) |
|---|---|---|
| stellar, 10 M_⊙ | 3.438e+11 | **1.36e−22** |
| Sgr A\* | 7.995e+05 | **5.85e−17** |
| M87\* | 5.289e+02 | **8.85e−14** |

against a pre-declared interest threshold of 1e−6. The worst case is **10⁷ times below** what
ngEHT or LISA could notice. A tidal channel fares worse still: every tidal scale at `r_cross`
sits 10–21 orders *above* a₀. So the null is confirmed on the non-geodesic branch too, and
`r_cross` remains a prediction of **exactly-GR** shadows, ISCO frequencies, ringdown spectra and
inspiral waveforms.

**Third, and stated against interest, the parent note carries a presentational risk that a
referee will find.** It explicitly rejects the objection "g ≫ a₀ near a horizon, so the effect
vanishes," on the correct ground that the formal dual `a₀_BH = c⁴/4GMZ` scales up identically,
keeping `a/a₀_BH` of order unity down to the horizon — indeed we find `ν − 1 = 0.3283` at
`r_cross`, **identical for all three holes**, a clean exhibition of the mass-independence. But the
framework's *operative* scale is the **cosmic** a₀ — its own §1.2 states that inertia responds to
the bath of the inverted cosmic horizon — and at that scale the effect *does* vanish, by ~22
orders. **Both statements are true of different scales, and they differ by 3.7×10¹² at fixed
radius.** The rejection is sound as written but reads as a claim of a real strong-field signal.
One sentence fixes it, and this addendum supplies it.

---

## 1. The reduction: `a₀ = κ c √(Gρ_Λ)`

`reviews/mi_kappa_spectral_reduction_2026.py`.

Write the normalisation with κ explicit, `a₀ = c²√(κ²Λ/8π)`, so that κ = ½ reproduces the
published `c²√(Λ/32π)`. Substituting the definition of the dark-energy density,
`Λ = 8πGρ_Λ/c²`:

```
a₀ = c² √( κ² · 8πGρ_Λ / (8π c²) ) = κ c √(G ρ_Λ)
```

verified symbolically. With κ = ½ this is `a₀ = (c/2)√(Gρ_Λ)`. Two consequences.

**(i) The open problem is one rational.** `Z(κ) = √(8π/3)/κ`, so `32π/3 = (8π/3)/κ²`. "Derive Z"
and "derive κ" are the same problem, and the second is the honest statement. The 8π is Einstein's
and the 3 is Friedmann's; neither is the framework's.

**(ii) The transcendence obstruction belongs to GR, not here.** The standing obstruction —
"Z carries a transcendental √π while flavour data is algebraic" — is correct about Z, but Z's
√π comes from Einstein's 8π. **The framework's own number is rational.** This matters for how the
obstruction is cited: it constrains what can be built from a GR-derived vocabulary, not what this
framework asserts.

## 2. Stress-testing the null

`real_research/reviews/mi_bh_cancellation_stress_2026.py` (all checks pass, exit 0).

Four attacks, each with thresholds fixed before evaluation (1e−6 = of interest to ngEHT/LISA;
1e−3 = already excluded by existing strong-field data).

**A1, the static observer — the one that mattered.** The free-fall theorem covers geodesic
observers only. A static observer is non-geodesic and its proper acceleration diverges at the
horizon, so this is a genuine gap in argument (b). Evaluating the framework's own
`ν(y) = √(1+1/y)` at `y = a_proper/a₀` gives the table above: worst case 8.85e−14, i.e. 1.1×10⁷
below the interest threshold. **The gap is real and the conclusion survives it.**

**A2, which scale is operative.** At fixed radius the two readings differ by 3.7×10¹². This is
not a matter of convention: the framework's physical claim fixes the cosmic scale, and the dual is
a formal exercise. §3 below states the consequence.

**A3, the tidal channel.** The kernel argument takes `□_u u`, the second derivative along the
worldline, not `|a|`. Being maximally generous (body size L = r) gives `a_tid ~ c²r_s/r²`, the
same order as g itself: 5.6e+21, 1.3e+16 and 8.6e+12 times a₀ for the three holes. The tidal
channel is *more* deeply switched off, not less.

**A4, where the physics actually lives.** Solving `a_proper(r) = a₀` returns the a₀ shell,
`r = √(GM/a₀)`: 0.122 pc for a stellar hole, 80 pc for Sgr A\*, 3.1 kpc for M87\* — that is
**1.3×10¹¹, 1.9×10⁸ and 5.0×10⁶ Schwarzschild radii**. The framework meets a black hole parsecs
to kiloparsecs outside it. `r_cross = 2.406 r_s` is where the formal dual would switch on, never
where the framework's physics does. (Both footings carried; alt-footing values in the script.)

## 3. The clarification the parent note needs

The parent note's rejection of "g ≫ a₀ so the effect vanishes" is **correct about the dual and
misleading about the framework**. Recommended single sentence:

> *The naïve objection fails for the formal dual `a₀_BH`, whose ratio `a/a₀_BH` stays O(1) to the
> horizon; but the framework's operative scale is the cosmic a₀, at which the deviation at
> `r_cross` is ≤ 8.85×10⁻¹⁴ and the effect does vanish — so the strong-field prediction is a null
> either way, and the duality is structural rather than observational.*

This subtracts a possible reading of a positive signal that was never claimed.

## 4. Two kept numbers from the de Sitter side

`real_research/reviews/mi_bh_unravel_desitter_2026.py` (22/22 pass).

- **`T_dS / T_U(a₀) = Z`**, exactly, canonical footing — the coefficient restated as a pure
  temperature ratio.
- **The a₀ shell of the maximal (Nariai) de Sitter black hole coincides with the de Sitter
  horizon**: `√(Z/3√3) = 1.0555` canonical, `0.9616` alt — within 6% of unity from pure numbers,
  no fit. Reported **with its ~2%-by-chance prior**: a structural coincidence, *not* a derivation
  of Z. Making it more would require deriving Z from the Schwarzschild–de Sitter double-root
  constant `3√3` — the κ-forcing route, closed 2026-06-17 by ghost-freedom, unitarity and
  holography.

Also unchanged and not a framework result: every black hole de Sitter permits does evaporate,
because the equilibrium mass `1.299 × M_Nariai` is forbidden, so `T₊ > T_c` across 40 decades of
mass. That is Gibbons & Hawking (1977) in plain GR + Λ. Modified inertia contributes **nothing**:
at a stellar horizon `y = g/a₀ ~ 10²³` and `ν − 1 = 3.1×10⁻²³`. **Black holes are the most purely
general-relativistic objects this framework knows** — which is precisely why it survives the solar
system.

## 5. What is not claimed

No new observable. No derivation of Z, κ, the response sign, or a₀'s value — all remain
**postulated**. The strong-field axis stays a null whose discriminating power is against
*metric-shifting* completions such as MOG, and not against this framework or against AeST, whose
published black holes are stealth (Skordis & Złośnik, arXiv:2412.15395). Credit as in the parent
papers: the interpolation `ν(y) = √(1+1/y)` and the identity `g_obs² − g_bar² = a₀ g_bar` are
Milgrom (1999, Phys. Lett. A 253, 273) Eqs. (8)–(9); the a₀–Λ tie is Milgrom's and Smolin's with a
2π coefficient, and **no priority is claimed for it**. What is ours is the coefficient `cH_Λ/Z`,
the modified-inertia completion, and the results above.

---

## References

Gibbons, G. W. & Hawking, S. W. 1977, *Phys. Rev. D* **15**, 2738.
Nariai, H. 1950; Bousso, R. & Hawking, S. W. 1996 — the Nariai bound and near-extremal instability.
Milgrom, M. 1999, *Phys. Lett. A* **253**, 273.
Skordis, C. & Złośnik, T. 2024, arXiv:2412.15395 — stealth AeST black holes.
Zimmerman, C. P. 2026, DOI 10.5281/zenodo.20947913 (parent), 10.5281/zenodo.20938891 (One Free Number).
