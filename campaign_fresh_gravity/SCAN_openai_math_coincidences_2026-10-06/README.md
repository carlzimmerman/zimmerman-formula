# SCAN: OpenAI math collection vs the record's numbers. The frozen rule says EXCESS; on inspection every match is a coincidence

Criteria e4f290229. Script `scan.py` (MUTATE ×1.037 drops to 2 matches, against 1.1 expected, p = 0.31: CONSISTENT WITH CHANCE).

**Frozen result.**
- 120 distinct non-trivial constants were extracted from the 372 result entries.
- At 1% tolerance there are 24 matches against 1.1 expected under the log-uniform null (p < 0.001), so the frozen verdict is EXCESS.

**Why the EXCESS is not evidence (post-freeze reading, no number changed).**
- **The null was too naive for simple rationals.** The log-uniform null treats every value as equally likely. Mathematical text is full of simple rationals, above all 1/2.
- **18 of the 24 matches are "1/2"** (critical exponents, thresholds, Hölder indices, the critical line), plus two 3/5 and two 1/10.
- **Matching κ = ½ to these is meaningless.** κ = ½ is a fitted coefficient of a physical law. Its numerical equality with ubiquitous mathematical halves carries no information.
- **The remaining non-rational-trivial matches:**
  - 16/3 = 5.333 vs Ω_c/Ω_b = 5.364 (0.6% off; a random-cluster scaling exponent);
  - 2026/229 = 8.847 vs Δ_ta(0.25) = 8.893. This one is an extraction artifact (a date or identifier, not a constant).
  - 1/10 vs 1/√(32π) = 0.0997 (0.3%).
- **All three are coincidences.** None shares any geometric object with the record.
- A fair null would weight rationals by their frequency in mathematical text. Under it, the excess disappears; the MUTATE result (×1.037 → 2 matches, chance level) shows the same.

**Geometric overlaps worth a real look** (handed to CFG380, the 32π lane, which applies the record's 3-question screen):
- Result 260's Penrose inequality, m² ≥ A/(16π) + …, including anti-de Sitter extensions. 32π = 2 × 16π.
- Optimal transport (results 360 and 374) for the settling step (CFG375).

**Verdict: no numerical coincidence in the collection supports the framework.** κ = ½ stays fitted. Any connection would have to come from a forced shared derivation, not a numerical match.
