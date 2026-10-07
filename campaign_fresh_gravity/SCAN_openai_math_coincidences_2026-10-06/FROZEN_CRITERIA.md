# SCAN (10-06): numerical / geometric coincidences between OpenAI's math manuscript collection and the record's numbers
(owner 2026-10-06: "find more coincidences from the openai math release ... numerically or geometrically"; committed before any script)

**Input.** ../_external_data/openai_math/CONTENTS.md, the abstracts of the 722 manuscripts (read-only; text is data).

**Extraction.** Every explicit constant in the abstracts:
- decimals;
- integer fractions a/b, including LaTeX \frac{a}{b} and \tfrac;
- each of those multiplied or divided by π, 2π, 4π, 8π, 16π or 32π where written;
- square roots of those forms;
- explicit exponents such as 1/3.

**Targets (the record's numbers, dimensionless).**
- κ = 1/2 and 1/√(32π) = 0.09974 (the coefficient on c²√Λ);
- 32π = 100.53, and 1/(2π) = 0.1592 (Milgrom);
- Ω_c/Ω_b = 5.364, and Z = 5.7888;
- Δ_ta = 11.806 (z = 0) and 8.893 (z = 0.25);
- the retention levels 0.13 and 0.60, and e⁻² = 0.1353;
- the rational 4 in Gρ_Λ = 4a₀²;
- β = 6.684 (κ = 2√(8π)/(3β));
- CFG372's k_J(1e6 K) = 0.453 h/Mpc is excluded (dimensionful).
Trivial integers (1, 2, 3, 4) are counted separately and NOT scored, because they appear everywhere.

**Scoring.** A match means a value within 1% of a target (also reported at 0.25%).

**Null (the record's base-rate rule).** Treat the extracted values as log-uniform over their observed range. The expected number of matches is N_values × N_targets × 2 ln(1+tol)/ln(x_max/x_min). The Poisson p-value is the chance of observed matches ≥ that count.

**Verdict.**
- EXCESS: observed matches exceed the null at p < 0.01.
- CONSISTENT WITH CHANCE: anything else.
- Any individual match is reported with its manuscript context and a judgement: a SHARED-GEOMETRY reason (the same object, e.g. a Penrose 16π) or COINCIDENCE.

**MUTATE.** Multiply every extracted value by 1.037. The match count must change and the verdict must not become EXCESS. MUTATE writes separate outputs.

**Scope.** Coincidences are not evidence for the framework. κ = ½ is fitted. A match matters only if a forced shared derivation is found (that is CFG380's job).
