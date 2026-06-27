# AS-B: is κ=½ a Reuter critical exponent θ_i or an IR de Sitter RG-attractor? — DOES-NOT-DELIVER (2026-06)

*Gemini idea #13, the lone explicitly-open theory door after KAPPA_ALL_DOORS / TOPOLOGICAL_KAPPA_ETA. Framework:
a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ) = cH_Λ/Z, Z = 2√(8π/3); √(8π/3) FORCED (Einstein-8π × Friedmann-3). Lone free number =
the OUTSIDE κ=½. Question: is κ a critical exponent θ_i (eigenvalue of the Reuter stability matrix) or an IR-attractor
value of the SO(4,1)/gravity RG flow? Anti-circularity gate HIGH: κ symbolic; a win must OUTPUT ½ from FP structure
without inputting Z by hand. DEAD-do-not-rerun: running-G→MOND (Donoghue 1911.02967, the one AS-MOND paper withdrawn).*

---

## VERDICT: **DOES-NOT-DELIVER THE NUMBER — and the deeper reading is a TYPE-MISMATCH, not just a non-match.**

The honest both-ways outcome the prior review predicted. Two layers:

**Layer 1 (the literal check — NO exponent = ½ or Z⁻¹).** The Reuter NGFP critical exponents in the Einstein-Hilbert
truncation are a **complex-conjugate pair** θ₁,₂ = θ′ ± iθ″ with central values across schemes:

| scheme | θ′ | θ″ |
|---|---|---|
| Litim cutoff (Codello-Percacci-Rahmede 2009) | 1.475 | 3.043 |
| Sharp cutoff (Lauscher-Reuter 2002) | 1.667 | 4.308 |
| Exponential cutoff (Lauscher-Reuter) | 1.376 | 3.106 |
| EH no-matter (typical) | 2.63 | 1.39 |

None of {θ′, \|θ\|} is within ~10% of **κ=½=0.5** or **Z⁻¹=√(3/32π)=0.1727**. The R² truncation adds a *third, real*
exponent θ₃ ~ +1.5…+2.5 — still O(1), still moving with truncation order, still not ½ nor 0.1727. The exponents are
genuinely **irrational and complex** and are the field's textbook example of **scheme/truncation-dependent** (non-clean)
numbers (Bonanno et al, "Critical Reflections on Asymptotically Safe Gravity"). So the "1/2 = exponent" idea is a hopeful
coincidence with no candidate even present; no universal clean rational exponent equals ½.

**Layer 2 (the structural why — κ is the wrong KIND of object for BOTH readings).** This is the load-bearing finding and
is *consistent with* the scale-fraction wall, restated in RG language:

- **κ as a critical EXPONENT θ_i = a TYPE ERROR.** θ_i is the eigenvalue of −∂β/∂g at the FP; it governs how a coupling
  *approaches* the FP as a **power** in the RG scale, g(k)−g_* ~ (k/k₀)^(−θ). κ is a **multiplicative constant in a
  definitional relation** a₀ = κ·c·√(Gρ_Λ) — no RG scale k, no eigen-direction, no β_{a₀}. The sympy-banked κ-blindness
  **a₀(2κ) = 2·a₀(κ) (strictly LINEAR, p=1 in κ)** is precisely the wrong functional form for an exponent (which enters as
  a power). An exponent structurally cannot BE the outside linear multiplier.

- **κ as an IR-ATTRACTOR / FP-value (the reading the prompt flags "NOT auto-blocked" because AS is type-different and was
  never run) — runnable, but FAILS, for a fresh reason.** Computed this session:
  1. With G CANCELLED, sympy gives **a₀ = κ·c²·√(Λ/8π)** (the √(8π) is *inside*; κ multiplies a pure-Λ combination
     outside). a₀ is **not a coupling in the gravitational action** — there is no "a₀ coupling" with a β-function whose FP
     value the flow could fix. AS gravity contains g_* and λ_* (and higher-derivative FP values); it contains **no a₀, no
     MOND, no inertia sector** (TOE_PARAMETER_SPACE: "DEAD for a₀"). The attractor has nothing to attract κ to.
  2. Even the values AS *does* fix (g_*, λ_*) are **UV** (k→∞). The **IR endpoint** where we live is a **FREE initial
     condition on every relevant direction** — that is what "relevant" means. Λ_today and G_today are tuned to data, not
     FP outputs; κ·√(Λ) inherits that IR freedom.
  3. The one genuine AS statement about IR Λ is the **opposite** of helpful: Wetterich's "graviton fluctuations erase the
     cosmological constant" drives λ→0 in the deep IR (banked ASYMPTOTIC_SAFETY_LAMBDA_NOTE). A Λ→0 attractor sends
     a₀→0 (directionally consistent with the framework's own ρ_DE-dilution far-future a₀→0, a *rhyme*) — it does **not**
     pin a FINITE outside ratio ½.

So the door that was "never run and not auto-blocked" was run: AS is indeed type-different (it outputs real g_*, λ_*, θ_i),
but **none of those three output-types is κ's slot** — θ_i is a power-law exponent (wrong form), g_*/λ_* are UV couplings
of the gravity action (a₀ is not among them), and the IR endpoint is a free datum (and Λ→0 anyway). The factor of ½ is
not produced.

---

## Both-ways credit and honest limits

**Credit (a real push).** This was correctly ranked the #1 / lone-open theory door — AS genuinely outputs the right
*category* of object (dimensionless universal numbers from a gravitational FP), unlike the mod-Z / energy-coefficient /
phase probes that the other ~24 routes hit. If a clean universal exponent had equaled ½ in the right slot it would have
been the zero-parameter derivation of a₀'s value. The exponents were looked up faithfully (real literature spread, the
complex pair, the R² third exponent) and the IR-attractor reading was steelmanned (it is the one non-type-mismatched
candidate) before being refuted on structure (no a₀ coupling; IR-free; Λ→0).

**Honest caveats (both ways).**
1. This is "**the FP does not deliver ½**," a strong negative for the EH and EH+R² truncations and for the structural
   reason that a₀ is not an RG coupling — **not a formal no-go** against every conceivable AS construction (e.g. an
   enlarged truncation that promotes a MOND/inertia operator to the FRG flow and reads its FP value — but that operator is
   absent from the framework's forced content, so inserting it to harvest ½ would be circular, the same gate that sank the
   q=4 lens and the added parity fermion).
2. The exponents' **scheme-dependence cuts against the idea on its own terms**: even if some truncation/scheme nudged an
   exponent to ≈0.5, a scheme-dependent O(1) is not a *universal* prediction — it would be a hopeful coincidence, not a
   forcing. The framework needs a clean universal output; AS exponents are the canonical example of non-clean.
3. Running-G→MOND stays DEAD and was not reproduced (Donoghue 1911.02967; the AS-MOND paper withdrawn). This is the
   *distinct* exponent-as-κ / FP-value-as-κ route, and it returns the predicted "doesn't deliver the number."

---

## Net

Consistent with and **completing** KAPPA_FORCING_DOOR_CLOSED + TOPOLOGICAL_KAPPA_ETA_VERDICT + KAPPA_FIVE_HAIL_MARY +
KAPPA_ALL_DOORS. The asymptotic-safety critical-exponent / IR-attractor route — the lone explicitly-open theory door — is
now run and **closed for κ**: no EH/R² exponent equals ½ or Z⁻¹; the exponents are complex, scheme-dependent, non-clean;
and structurally κ is neither a power-law exponent θ_i (type error: κ enters linearly, a₀(2κ)=2a₀(κ)) nor a FP coupling
(a₀ is not in the gravity action; the IR endpoint is free; AS drives Λ→0). **κ=½ stays UNFORCEABLE; a₀'s value stays
NOT-derived; the framework is a provably one-parameter EFT and the κ-forcing theory program is now COMPLETE including its
last-named open avenue.** AS remains a non-hostile QG-UV companion (directional Λ-is-dynamical rhyme), not a κ source.

*Scripts this session (κ symbolic): `/tmp/as_b_check.py` (exponent spread vs ½ / 0.1727 — none match; targets
Z⁻¹=√6/(8√π)=0.17275, Z=5.78881), `/tmp/as_b_structural.py` (a₀=κc²√(Λ/8π) with G cancelled; type-match A=exponent
[linear, not power → type error], B=attractor [no a₀ coupling, IR-free, Λ→0]). Literature: Lauscher-Reuter hep-th/0205062,
Codello-Percacci-Rahmede, Bonanno et al "Critical Reflections" (scheme-dependence). Running-G→MOND DEAD: Donoghue 1911.02967.*
