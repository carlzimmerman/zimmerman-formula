# Route 2 — the de Sitter–Unruh crossover: does a temperature/horizon condition FORCE kappa=1/2 (Z=√(32π/3))? — VERDICT (2026-06-15)

**GRADE: UNFORCED-POSIT. The dS–Unruh crossovers BRACKET 5.789 but no clean physical crossover LANDS on it.**
Z is O(1)-not-forced on this route. Cleanest near-miss: the density/free-fall route at kappa=1 gives Z=√(8π/3)=2.89;
the framework's 5.789 needs the extra kappa=1/2 (free-fall/equipartition), which no temperature-equality supplies.
Code: `/tmp/route2_dsunruh_crossover.py`, `/tmp/route2_floor_transition.py` (sympy, all identities re-derived).

## Setup (verified, sympy)
- Canonical convention throughout: **Z ≡ cH_Λ/a0**, H_Λ = c√(Λ/3), ρ_DE = Λc²/(8πG).
- `a0 = kappa·c·√(Gρ_DE)` ⟹ **Z(kappa) = √(8π/3)/kappa**. kappa=1/2 ⟺ Z=√(32π/3)=5.78881 (sympy `solve`, exact).
- So "force Z" ⟺ "force kappa=1/2" ⟺ "force the factor of 2 in c/2." Confirmed.

## The crossovers and what each gives (sympy, exact)
| crossover condition | a0 | Z=cH/a0 | kappa |
|---|---|---|---|
| (i) a = cH_Λ (naive onset) | cH_Λ | **1** | 2.894 |
| (ii) T_Unruh(a0) = T_dS (temperature equality) | cH_Λ | **1** | 2.894 |
| (ii') a0 = de Sitter surface gravity c²/2R_dS = cH_Λ/2 | cH_Λ/2 | **2** | 1.447 |
| (iii) Rindler horizon dist c²/a = R_dS | cH_Λ | **1** | 2.894 |
| (iii-2π) thermal wavelength 2πc²/a = R_dS | cH_Λ/2π | **2π=6.283** | 0.159 |
| (iv) vacuum free-fall a0 = c√(Gρ_DE) | — | **√(8π/3)=2.894** | 1 |
| **FRAMEWORK (c/2)√(Gρ_DE)** | — | **√(32π/3)=5.789** | **1/2** |
| Verlinde a_M = cH/6 | cH/6 | 6.000 | 0.482 |

**The decisive structural fact (sympy-confirmed):** the floor T_eff = (ħ/2πckB)√(a² + (cH_Λ)²) is additive-in-quadrature,
so its crossover knee is at **a = cH_Λ EXACTLY (Z=1) by construction** — there is no O(1) other than 1 hiding in that
functional form. Temperature-equality T_Unruh(a0)=T_dS is the SAME condition (T_Unruh∝a, T_dS∝H ⟹ a0=cH ⟹ Z=1). I tried
to manufacture the factor-2 by "doubling" T_eff(a0)=2·T_dS (gives Z=1/√3=0.577) and T_eff=√2·T_dS (gives Z=1) — **neither
is 5.789, and both are arbitrary thresholds.**

## Why no temperature crossover can land on 5.789 (the honest mechanism)
kappa=1/2 sits in front of **√(Gρ_DE)** — a DENSITY / free-fall scale — not in front of cH (a rate). Since
cH = √(8π/3)·c√(Gρ_DE), the 1/2 is a free-fall/equipartition kinematic prefactor on the *density* route. The
temperature/rate crossovers natively produce Z ∈ {1, 2, 2π} (a=cH; surface-gravity cH/2; thermal 2π·cH); the
entropic route gives 6. **5.789 = (kappa=1) density scale × an extra 1/2.** That extra 1/2 is the surface-gravity /
free-fall convention, identical to the "(2)²/3·8π = 32π/3" decomposition already banked in FORCING_THE_COEFFICIENT.md:
8π (Einstein) and 3 (Friedmann) are FORCED; the (2)² is the kinematic convention. This route reaches the SAME wall from
the temperature side.

## Both ways
- **In the framework's favor (credited):** the dS–Unruh crossovers genuinely BRACKET 5.789 tightly — 2.89 (free-fall),
  5.79 (framework), 6.0 (Verlinde), 6.28 (thermal) — and EXCLUDE the naive 1–2. The scale a0 ~ c√(Gρ_Λ) and the
  ballpark Z~3–6 ARE forced. The data band cH_Λ/a0 ≈ 4.5–4.9 (pure-Λ) admits 5.79 but sits at its low edge. The
  √-form/deep-MOND law and the a0↔Λ identity are forced; only the O(1) is not.
- **Against (no manufactured win):** NO clean physical crossover gives EXACTLY √(32π/3). Every temperature-equality
  collapses to Z=1; the only conditions giving 2π or 6 are different routes (thermal, entropic), not the framework's.
  The factor-2 is inserted by the free-fall/equipartition convention — a posit, not a forced second Bekenstein–Hawking ¼.
  This matches the banked DEFINITIVE_VERDICT (κ structurally unfixable by equilibrium horizon thermodynamics; the
  "literal second ¼" gives Z=11.58, not 5.79) and the COrresponding number-field no-go √(32π/3)∉ℚ(π).

## Literature (web, 2026-06-15) — confirms "matched, not forced"
- **Milgrom** (pedagogical review; a0-cosmology connection, arXiv:2001.09729): in de Sitter the expansion rate, curvature
  and Λ coincide, so "the above lesson… **does not tell us which** of the cosmological acceleration parameters is to be
  identified with a0." The de Sitter route fixes the *scale*, not the *coefficient*.
- **Singh 2026, "A Relativistic MOND"** (arXiv:2601.04290): a0 = c²/(ξ·ℓ_dS) with **ξ = O(1) fixed by matching** the
  relativistic action to the AQUAL static limit. Coefficient matched, not derived — exactly as banked.

## Verdict
**UNFORCED-POSIT — quarantine HOLDS.** The de Sitter–Unruh crossover does NOT force kappa=1/2. (i) a=cH_Λ → Z=1 (wrong);
(ii) temperature-equality T_Unruh(a0)=T_dS → Z=1 (identical to (i), the only natural T-condition); (iii) Unruh-wavelength =
horizon → Z=1, or Z=2π with the thermal 2π; (ii') surface gravity → Z=2; (iv) free-fall density → Z=2.89. These O(1)
values BRACKET 5.789 but none pins it. The framework's 5.789 requires the free-fall/equipartition kappa=1/2 on the
*density* route — a kinematic convention, not a crossover output. **No new derivation; the cleanest near-miss is the
kappa=1 free-fall scale Z=√(8π/3)=2.89, off the framework by exactly the disputed factor of 2.** Moot for the empirical
program (the a0(z)/a0(0)=√(ρ_DE(z)/ρ_DE0) test cancels Z).

*Both ways enforced: bracketing/scale-forcing credited at full weight (no high-priest dismissal); the absence of an
exact-5.789 crossover stated plainly with the smuggled 1/2 flagged (no manufactured derivation, no numerology dressed as
physics). Quarantine default held: a0/Z posited, never asserted derived.*
