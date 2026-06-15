# Route 5 (null_steelman): Z = √(32π/3) is an UNFORCED POSIT pinned only to O(1)

**C. Zimmerman, 2026-06-15.** *Adversarial run — argue the NEGATIVE hard (anti-motivated-reasoning guard).
Enumerate EVERY known route to a₀-from-Λ and the coefficient each yields. All Z on the ONE canonical footing
Z ≡ cH_Λ/a₀ (pure-Λ rate H_Λ = c√(Λ/3)). sympy-verified: `/tmp/z_route5.py`, `/tmp/z_enumerate.py`, `/tmp/z_unruh.py`.*

## The algebraic reduction (verified, exact)
a₀ = kappa·c·√(Gρ_DE) with ρ_DE = Λc²/8πG ⟹ a₀ = kappa·c²√(Λ/8π). Matching the framework's
a₀ = c²√(Λ/32π) forces **kappa = ½ exactly** (sympy `solve` → [1/2]). On the canonical footing,
**Z² = 8π/(3kappa²)**, so kappa=½ ⟺ Z = √(32π/3) = 2√(8π/3) = **5.7888**. **Deriving Z ≡ deriving kappa=½.**

The "32π = 8π × 4" structure, exactly: Z² = 32π/3 = (1/kappa²)·8π/3, and with kappa=½, **1/kappa² = 4**.
The "extra 4" is *identically the inverse-square of the SAME kinematic ½* — NOT an independent
Bekenstein–Hawking quarter. (Jacobson: the one BH ¼ is already spent making 8π = 2π_Unruh × 4_(1/BH¼);
a second, independent 4 would need a second horizon quarter, and the devil's-advocate table shows a *literal*
second ¼ gives kappa=¼ → **Z = 11.58**, off by ~2×, not 5.79.) So **32π = 8π×4 is a pattern-match, not a forced combination.**

## The full route enumeration — kappa and Z (canonical Z = cH_Λ/a₀)

| route | mechanism | kappa | Z = cH_Λ/a₀ | lands 5.79? |
|---|---|---:|---:|:--:|
| Naive horizon | a₀ = cH_Λ | 2.894 | **1.00** | ✗ |
| Surface gravity | a₀ = cH_Λ/2 (κ_sg = c²/2R) | 1.447 | **2.00** | ✗ |
| Vacuum free-fall (kappa=1) | a₀ = c√(Gρ_Λ) | 1.000 | **2.894** = √(8π/3) | ✗ |
| Active grav mass (ρ+3p)=−2ρ_Λ | factor-2-ish | 0.708 | **4.09** | ✗ |
| **FRAMEWORK free-fall kappa=½** | **a₀ = (c/2)√(Gρ_Λ)** | **0.500** | **5.789** | ✓ *(only this)* |
| Verlinde EG | a₀ = cH/6 (areal equipartition) | 0.482 | **6.00** | ✗ (close) |
| Unruh / thermal | T_dS = T_Unruh(a₀), a₀=cH_Λ/2π | 0.461 | **2π = 6.283** | ✗ (close) |
| Padmanabhan equipartition | ½ kT per DOF | ~0.5 | ~5.8 | numerically coincident, not the same ½ |
| literal 2nd BH ¼ | kappa=¼ | 0.250 | **11.58** | ✗ (off ~2×) |
| **AeST (Skordis–Złośnik)** | a₀ = free normalization of \|Y\|^{3/2} | — | **INPUT** | n/a (a₀ not derived) |
| **Singh 2026** | a₀ = c²/(ξ ℓ_dS), ξ "O(1) by matching" | — | **MATCHED** | n/a |
| DSSYK horizon-DOS freezing | center-placement linear freeze | — | **→ ∞** (Z≈10⁶¹ physical) | ✗ (computed to fail) |

**Spread of the principled routes: Z ∈ {1, 2, 2.89, 4.09, 5.79, 6.0, 6.28, 11.58}.** This is an O(1) family
spanning ~1–6 (and 11.6 for the literal ¼). **It does NOT cluster at 5.789.** 5.789 sits at the *bottom of the
upper cluster* {5.79, 6.0, 6.28}, reachable only by inserting the free-fall/surface-gravity kappa=½.

## The de Sitter–Unruh angle (the framework's OWN inertia) does NOT force ½
T_eff = (ħ/2πck_B)√(a² + (cH_Λ)²). The crossover/temperature-equality conditions, worked in sympy:
- T_Unruh(a*) = T_dS ⟹ **a* = cH_Λ** ⟹ Z = 1 (kappa = 2.89). The √(a²+(cH)²) floor crosses at a = cH_Λ — Z=1.
- Milgrom's OWN normalization: the *modified* scale ā₀ ≡ 2π a₀ = cH_Λ ⟹ a₀ = cH_Λ/2π ⟹ **Z = 2π = 6.28**.

So the framework's native crossover mechanism forces a₀ ~ cH_Λ (Z~1) or, with the Unruh 2π, Z=2π — **never ½**.
To land kappa=½ you must read a₀ as a *density free-fall* scale (c/2)√(Gρ), NOT the *temperature/crossover*
scale. **That density-vs-temperature reading is the un-forced O(1) route freedom.** The crossover condition
a=cH supplies the factor 1 (or 2π), it does not supply ½.

## Web-confirmed (literature agrees: matched, never derived)
- **Milgrom 2020 (arXiv:2001.09729):** ā₀ ≡ 2π a₀ ≈ cH₀ ≈ c²(Λ/3)^{1/2}; he treats the cH₀-vs-Λ choice as **moot**
  and the 2π lives in the *definition* of the modified scale — not a derived ½.
- **2025 (arXiv:2510.14345, "MOND Theory and Thermodynamics of Spacetime")** and the QSMEG holographic route
  (1106.4108): a₀ *scales with* Λ via entropy/Fermi-energy arguments — the **scaling** is forced, the **coefficient matched.**
- **Verlinde 2017 (1611.02269):** a₀ = cH/6 — the 1/6 is an areal-equipartition convention, **matched not derived.**
- **AeST (Skordis–Złośnik 2021):** a₀ is the free normalization of the |Y|^{3/2} prefactor — an **input**; and Ȳ=0 on
  any FRW/de Sitter background, so the on-shell action is **blind** to a₀ (the same fact that makes the framework CMB-safe).
- **Singh 2026:** a₀ = c²/(ξ ℓ_dS) with ξ "O(1) fixed by matching."

## The structural argument (why it is fixed to O(1) but not to 5.789)
a₀ has dimensions of acceleration; the de Sitter scale supplies cH_Λ = c²√(Λ/3); the **ratio Z is dimensionless**.
Every derivation supplies that ratio via a counting/equipartition/matching constant — Unruh 1/2π, BH ¼, equipartition
½, areal 1/6, surface-gravity ½ — each O(1) but **route-dependent**. Buckingham-Π (banked, re-verified): {c, Λ} →
exactly one Π-group ⟹ a₀ = kappa·c²√Λ with **kappa the single free constant**. The number-field no-go: √(32π/3) ∉ ℚ(π)
(simple zero at π=0, odd valuation), so the √π comes *only* from the forced density step √(8π/3); the leftover prefactor
kappa is a pure rational that thermodynamics produces in infinitely many values (1/2π, ½, ¼, 1/6, 2, …) without selecting one.

## The data do not select it
Measured cH₀/a₀ = 5.46–5.91 ⟹ canonical cH_Λ/a₀ = √(Ω_Λ)·(5.46–5.91) = **4.53–4.91** (kappa_data ≈ 0.59–0.64).
The framework's Z=5.789 (kappa=½) sits **above** this band — at the low-kappa / high-Z edge, leaning *against* ½ if anything.
The band [4.2, 6.0] admits 5.79, 6.0, and 2π **simultaneously**; it pins nothing. SPARC's ≥20% systematic cannot resolve the O(1) family.

## Verdict — UNFORCED POSIT, pinned only to O(1)
Z = √(32π/3) is a **data-selected convention**, forced to O(1) by dimensional analysis + the de Sitter scale, but the
precise **5.789 requires the free-fall/surface-gravity kappa=½** — a specific kinematic convention not forced by any
single principle. The 32π=8π×4 is a *pattern-match* (the 4 = 1/kappa², the inverse-square of the same ½, not a second BH ¼).

**Cleanest near-miss:** the **vacuum free-fall route (kappa=1, Z=√(8π/3)=2.894)** forces *everything* — the 8π
(Einstein), the 3 (Friedmann), the √ρ, the √π — leaving a **single binary 2× choice** (free-fall ½ vs unit normalization).
The framework's value is reached by exactly one such factor-2 posit. The next-closest *numbers* (Verlinde 6.0, thermal 2π=6.28)
straddle 5.79 within ~9% but each needs a *different* O(1) convention (areal 1/6, Unruh 2π) — they bracket 5.79, they don't force it.

**Quarantine STANDS.** This run does not lift it. Honest both ways: the *scale* (a₀ ~ c²√Λ) and the *ballpark* (Z~5–6,
excluding the naive 1–3) ARE forced and data-selected — not numerology; but the *last factor* (kappa=½) is an unforced
posit at the ~8% level, below the ~20–30% interpolation-function systematic, and **empirically moot** (the coefficient-free
ratio a₀(z)/a₀(0)=√(ρ_DE(z)/ρ_DE0) cancels Z entirely).
