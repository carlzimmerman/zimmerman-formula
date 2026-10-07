# T7 — second-generation coincidence scan (openai/math vs framework)

Predecessor: `campaign_fresh_gravity/SCAN_openai_math_coincidences_2026-10-06`
(abstract-level; verdict: nothing beyond the ubiquitous ½). This lane is the
manuscript-level follow-up with the full inventory now available: **57 exact
constants** extracted from the release by lanes T1–T6 (values verbatim from
their committed outputs), **15 framework targets** (DERIVED / FITTED /
REQUIRED / MEASURED / CALIBRATED, both footings where applicable), and the
**891-form base-rate family** F = {(p/q)πⁿ, √((p/q)πⁿ)} (the record's null;
q = 32 ∉ F so the null is not trivially satisfied).

Script: `t7_coincidences.py` (checks can fail; MUTATE via `T7_MUTATE=1`
perturbs all targets ×1.05 and writes `t7_results_MUTATE.json` + separate
.out). Main run: **7/7 PASS, rc 0**; MUTATE: **3/7, rc 1** with C0, C1, C2,
C3 flipping as declared (misses 5.2% / 4.9% where the main run had 0.33% /
4×10⁻⁵).

## Result table (all hits within 1% log-miss)

| corpus constant | target | miss | p_base | verdict |
|---|---|---|---|---|
| κ₁ = 9.87 (JKO settling eigenvalue, T3) | (π² = 9.8696) | 4.0×10⁻⁵ | — | **STRUCTURAL**: μ = r²ρ reduction makes the settling exactly the Neumann heat equation on [0,1]; first eigenvalue π²(1+O(r_in/r_out)) — an identity, not a coincidence |
| a_TF = 3/7 (family 263 Thomas–Fermi) | X-COP cluster completeness 0.430 at R500 | 3.3×10⁻³ | 0.0034 | **NUMEROLOGY** (headline find): p_base < 1% but no derivation; ±0.15 measurement uncertainty swallows 0.33%; 3/7 has no link to Λ or G. Report as curiosity with a recording duty (below) |
| elasticity 0.4964/0.4960 (T1) | κ = ½ | 7.2×10⁻³ / 8.0×10⁻³ | 0.0045 | UBIQUITOUS-1/2: the deep-MOND M_ph ∝ √M_b law has slope ½ — the framework's own ½, not a corpus find |
| supercharge ½ (270) | κ = ½ | exact | 0.0011 | CALIBRATION + the corpus's own ubiquitous ½ (263 half-electron, 215 mixing, etc.) |
| 5 curation self-pairs (elasticity, M_ph, realisable, κ₁, λ) | — | exact | — | CALIBRATION (same quantity both sides) |
| everything else = 57×15 − 11 | — | > 1% | — | NULL / no hit |

Base-rate reproducibility: 1%-window share vs T = **0.0022** (record
0.002–0.003 confirmed on the 891-form family).

## Pair-ratio scan (1596 pairs × 891 forms)

730 pairs land within 1% of an F-form (expected 343 under a uniform-log
Poisson null — found ≤ 3× expected, C4 PASS). Of these, 76 are
**algebraically exact** identities (both members π-rationals, e.g.
TF_k/c_F = 1/(4π), a_TF/(1/4π) = 12π/7, twocell/deep-dens = 4 — the corpus is
partly π-quantised by construction); the residual 654 is null-consistent
(C4b PASS). No free, unexplained pair coincidence survives.

## Honest bottom line

Second-generation scan confirms and sharpens the predecessor: **the only new
near-hit is a_TF = 3/7 ↔ 0.430** (0.33%), one of ~3 F-forms that close; it is
coincidence-only (no mechanism, uncertainty-dominated). The structural result
worth keeping is **κ₁ = π² to 4×10⁻⁵** — the settling is literally the heat
equation in μ-space, which pins the undamped rate exactly (used by T3: ×353
above CFG382's λ). Nothing in the release's constants forces 4, 32π, 5.36, or
any measured completeness; κ = ½ stays fitted.

## Recording duty (if any follow-up lane wants it)

The 3/7 ↔ 0.430 near-hit deserves a falsifier line only because the record
already owns the measured number: if a future cluster sample (e.g. eRASS or
X-COP+SPT) tightened the R500 completeness to 0.430 ± 0.03, 3/7 would still
be a coincidence, not a prediction — unless a derivation appears (the TF
hull-radius prefactor has no gravity content). Do not spend a lane on it
before that tightening exists.