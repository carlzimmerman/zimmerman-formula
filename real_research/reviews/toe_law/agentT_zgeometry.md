# Agent T — does the Jacobson-construction breakdown acceleration carry a forced coefficient?

*agentT, 2026-06-10. Companion to `agentQ_jacobson_DL.md` (DL = Tolman-shifted GH; merger at 89% static-patch
depth; (H/a)² = Z² = 32π/3 at a = a₀). Artifacts: `agentT_zgeometry.py` + `.out`. No git.*

## 0. PRE-REGISTRATION (binding — written before any computation was run)

**Question.** The Jacobson Clausius construction's validity domain collapses at low acceleration. Does the
breakdown acceleration a_break — computable from geometry alone — carry a forced dimensionless coefficient?

**Three pre-registered outcomes (locked):**
- **(Z-CANDIDATE)** a_break = cH/√(32π/3), forced by the geometry with no tunable choices. This would be
  EXTRAORDINARY and triggers the mandatory hostile tier: do NOT celebrate; list every choice made and whether
  an alternative choice changes the number.
- **(O(1)-NULL)** a_break = cH × O(1) with the O(1) scheme-dependent (like agentQ's {0, 1/6, 1/3, 1/2}
  spread). Then Z = √(32π/3) stays DATA-SELECTED; the merger-depth reading is a consistency statement, not a
  derivation. Reported at full weight — this is the expected outcome.
- **(ILL-POSED)** the breakdown has no sharp boundary. Say so.

**The plan (locked):** three independent definitions of the validity boundary, each computed exactly in the
dS static patch, sympy-verified:
- **(a) the merger condition** — where the local Rindler horizon distance (the Rindler depth c²/a) equals the
  proper distance to the cosmological horizon for the stationary (Deser–Levin) worldline at static-patch
  radius r. Derive r(a) for the stationary family first, properly from the static-patch metric.
- **(b) the Killing-failure condition** — where the construction's neglected O(x²·Riemann) boost-Killing
  failure terms (Guedens–Jacobson–Sarkar, arXiv:1112.6215) become O(1) relative to the leading Clausius
  balance; the exact coefficient of the failure term.
- **(c) the equilibrium/adiabatic condition** — where the local patch's light-crossing time becomes
  comparable to the inverse temperature.

For each: the dimensionless c_i in a_break,i = c_i·cH, exact where possible, reported RAW first; only then
compared to {1, 1/Z = 0.1727, Z = 5.789, 2π, 1/6, √(32π/3)}. For each c_i: which choices it depends on
(factor conventions, which horizon distance, proper vs coordinate), and the SPREAD across defensible
choices — the spread IS the answer to whether anything is forced. The single sharp question for the
framework's own reading: does ANY computed c_i equal 1/√(32π/3) EXACTLY (symbolic match, not
numerically-close)? **The prior is the banked verdict (Z is data-selected); overturning it requires a forced
symbolic match surviving the choice-spread audit.** Coefficient near-misses are the repo's #1 failure mode —
every near-miss gets flagged as such, not celebrated.

*(Computation begins below this line. Nothing above was edited after the runs.)*

---

# RESULTS (28/28 machine checks PASS, `agentT_zgeometry.out`)

## VERDICT FIRST: **O(1)-NULL** — the pre-registered expected outcome — with two of the three definitions resolving to the ILL-POSED horn, and **NO symbolic match to 1/Z anywhere**. Z stays DATA-SELECTED; the banked verdict stands undisturbed.

## 1. The stationary family (the substrate, derived from the metric) — `.out` Part A
Full-Christoffel computation in the static patch ([A1]): the static worldline at radius r has proper
acceleration **a(r) = H²r/√(1−H²r²)** (the prompt's draft form `(Hr/√(1−H²r²))c²` is dimensionally off;
corrected — with c restored: a = H²r/√(1−H²r²/c²), H in 1/time). Inverted ([A2]):
> **r(a) = a/(H√(a²+H²))**, i.e. **H·r(a) = a/√(a²+H²) = μ_F4 exactly** —
the dimensionless static-patch radius of the stationary worldline IS the F4 kernel. *Flagged as an identity
echo (the third independent appearance of a/κ after agentQ's D2a–c), not a derivation.* Proper distance to
the cosmological horizon ([A3–A5]): ℓ(r) = arccos(Hr)/H, a(ℓ) = H·cot(Hℓ), **Hℓ(a) = arctan(H/a)**. The
bookkeeping variable throughout: x = Hℓ = arctan(H/a); deep-MOND onset a₀ = cH/Z ⇔ x₀ = arctan(Z) = 1.39974
= 89.1% of the patch depth π/2 (agentQ's merger point, reproduced).

## 2. Definition (a) — the merger condition: a sharp NON-boundary plus a free threshold — `.out` Part B
The flat Rindler depth is d_R = 1/a = tan(x)/H; the true proper distance to the horizon is ℓ = x/H.
- **The strict merger condition d_R = ℓ has NO finite-a solution** ([B1]: d/dx(tan x − x) = tan²x > 0, so
  tan x > x strictly on (0, π/2)). The flat-frame Rindler wedge **always** overshoots the cosmological
  horizon — at every finite acceleration, not below some a_break. As a sharp equality the merger condition
  is ILL-POSED; equality holds only asymptotically (a → ∞).
- The graded misfit m = (tan x − x)/x has **exact leading coefficient 1/3**: m = (1/3)(H/a)² − (4/45)(H/a)⁴
  ([B2–B3]) — and grows without bound as a → 0 (the only channel of the three that does).
- A boundary therefore exists **only by threshold fiat**, and the root obeys c_a = cot x\* = 1/((1+m\*)x\*)
  ([B4–B6]): m\*=50% → c_a = 0.689; **m\*=100% → c_a = 0.429**; m\*=200% → 0.252; m\*=300% → 0.179;
  d_R = patch depth π/(2H) → c_a = **2/π** exactly; d_R = curvature radius 1/H → c_a = 1.
  **Spread within definition (a) alone: ×5.6, set entirely by the threshold.**
- **Numerology-bait flagged ([B7])**: the misfit at a₀ is m(a₀) = (Z − arctan Z)/arctan Z = 3.13564 — a
  **0.19% near-miss to π**. "Z = (1+π)arctan Z" has no derivation behind it; transcendental coincidence;
  structurally meaningless per the coefficient discipline. NOT fed.

## 3. Definition (b) — the Killing-failure term: the dS coefficient is EXACTLY ZERO — `.out` Part C
This is the memo's new theorem-grade fact, and it cuts **against** any breakdown-coefficient reading:
- **In exact dS the GJS O(x²·Riemann) failure of Jacobson's approximate boost Killing field vanishes
  identically — to all orders in x.** Reason (classical theorem): an isometry fixing p satisfies
  φ(exp_p v) = exp_p(dφ_p v), so **any Killing field vanishing at p is exactly linear in Riemann normal
  coordinates**. dS is maximally symmetric: the local boost about any horizon point IS an exact Killing
  field (the static-patch boost), and Jacobson's χ = κ(x¹, x⁰, 0, 0) is its exact RNC expression.
  Machine-verified three ways: (i) the truncated-RNC failure tensor ∇_(μχ_ν) vanishes component-by-component
  at O(x²) for the dS Riemann ([C1]); (ii) the closed-form constant-curvature RNC metric
  g = φ(s)η + (1−φ)x x/s, φ = sin²(H√s)/(H²s) satisfies **L_χ g = 0 exactly, all components, all orders**
  ([C3]; closed form certified: matches the RNC expansion at O(s) [C4], Sherman–Morrison inverse exact [C5a],
  numeric Ricci = 3H²g to 10⁻¹⁴ [C5b]); (iii) breaking the Lorentz invariance of the Riemann tensor
  (R₀₂₀₂ → R₀₂₀₂ + δ) switches the failure back on, **exactly linear in δ** with exact components
  S₀₁ = −δκx₂²/6, S₂₂ = −δκx₀x₁/3, … ([C2]).
- **Consequence:** definition (b) produces **NO cH-proportional breakdown acceleration at all**. In exact dS
  the channel is empty (the construction's Killing field is not approximate there). In perturbed dS the
  failure is O(x²·δRiemann) — set by the **matter perturbation** (δR ~ GT), not by H: a boundary on a
  different axis entirely. c_b = NONE.
- What DOES degrade is the flat-frame **bookkeeping** (norm/temperature weights): exact coefficient **1/6**
  (1 − sin x/x = x²/6 − …, [C6]) — and this graded error **never reaches O(1) inside the static patch**
  (max 36.3% norm / 57.1% temperature at the patch edge; at a₀ it is only **29.6% / 42.1%** [C7]). Reaching
  deviation = 1 requires x = π or 1.896 — both outside the patch. The extrapolated "boundary" c = 1/√6 =
  0.408 is flagged invalid (the extrapolation leaves the domain).
- **Refinement of agentQ Part F (recorded at full weight):** agentQ justified the scheme spread
  {0, 1/6, 1/3, 1/2} as degenerate with "the construction's own neglected O(x²·Riemann) terms". In exact dS
  those terms are exactly zero, so the degeneracy argument does not apply there; the spread stands on the
  acceleration/weight bookkeeping choices alone (which it does — agentQ F1 is intact). Net effect:
  **agentQ's R1 exactness is STRENGTHENED** — in exact dS, Clausius with the exact boost is exact at every
  a, and the verdict "Jacobson-with-DL = Jacobson identically" needs no small-(Hℓ) caveat.

## 4. Definition (c) — equilibrium/adiabatic: scale-invariant, bounded, never fires — `.out` Part D
- **Flat bookkeeping:** t_cross × T_Unruh = (1/a)(a/2π) = **1/(2π) exactly** — independent of a AND H. The
  standard equilibrium criterion is scale-invariant and **never breaks** ([D1]).
- **Exact dS bookkeeping:** P(a) = ℓ(a)·T_DL(a) = arctan(H/a)√(a²+H²)/(2πH) is **bounded and monotone on
  the entire acceleration range**: P(∞) = 1/(2π), P(0) = **1/4** ([D2, D4]). It never becomes O(1); the
  total drift across all of parameter space is 57%. Deviation series: 2πP = 1 + (1/6)(H/a)² — **the same
  exact 1/6** as the norm channel ([D3]). The criterion NEVER fires: as a sharp boundary, ILL-POSED.
- **Radar reading:** light-crossing to the horizon in observer proper time diverges logarithmically at
  every a — exactly as in flat Rindler; not H-keyed ([D5]).
- Boundaries appear only by threshold fiat ([D6]): T_DL/T_U = 2 → c = 1/√3 = 0.577; naive ratio = 1 →
  c = 1/√(4π²−1) = 0.161; flat patch = curvature radius → c = 1; = patch depth → 2/π; thermal wavelength
  = 1/H → c = 2π.

## 5. Coefficient discipline: raw table, then the sharp question — `.out` Part E
Raw c_i (a_break = c_i·cH), with what each depends on:
| definition / variant | c exact | c | depends on |
|---|---|---|---|
| (a) misfit 300% / 200% / 100% / 50% | 1/((1+m\*)x\*) | 0.179 / 0.252 / 0.429 / 0.689 | free threshold m\* |
| (a) depth = patch / curvature radius | 2/π / 1 | 0.637 / 1 | which depth scale |
| (b) Killing failure, exact dS | **NONE — failure ≡ 0, all orders** | — | channel empty |
| (b) norm channel, extrapolated | 1/√6 | 0.408 | invalid extrapolation |
| (c) exact equilibrium ratio | **NONE — bounded in [1/(2π), 1/4]** | — | never fires |
| (c) T_DL/T_U = 2 / ratio = 1 | 1/√3 / 1/√(4π²−1) | 0.577 / 0.161 | threshold + 2π placement |
| (c) length pairs | 1 / 2/π / 2π | 1 / 0.637 / 6.283 | which length pair |

**Spread of finite candidates: [0.161, 6.283] — a factor 39. The spread IS the answer.**

**The single sharp question (#3): does ANY c_i = 1/√(32π/3) symbolically? NO MATCH** ([E1]). Every closed-form
candidate match would force a false π-identity: 2/π ⇒ π = 128/3; 1 ⇒ π = 3/32; 1/√6 ⇒ π = 9/16; 1/√3 ⇒
π = 9/32; 2π ⇒ π³ = 3/128; 1/√(4π²−1) ⇒ 12π² − 32π − 3 = 0 (π algebraic — excluded by transcendence). The
transcendental-root family is numeric-only and lands nowhere on 1/Z; the threshold that WOULD produce
c_a = 1/Z is m\* = m(a₀) = 3.13564 exactly — a **tautological crossing** of a continuum family ([E2]), and
nothing selects it.

**Near-miss flags (all structurally meaningless, per discipline, none fed):**
- m(a₀) = 3.13564 vs π: 0.19% — transcendental coincidence (§2).
- (a) m\*=3 row c = 0.17944 vs 1/Z = 0.17275: 3.9% — pure artifact of m(a₀) ≈ 3 (the tautological sweep).
- 1/√(4π²−1) = 0.16121 vs 1/Z (6.7%) and vs 1/6 (3.3%) — threshold artifacts.
- 2π vs Z: 8.5% — (2π)² = 4π² vs Z² = 32π/3 ⇔ π vs 8/3: symbolically distinct.

## 6. Both ways, full weight
- **Framework-unfavorable (the headline):** no forced coefficient exists. The breakdown acceleration is not
  a geometric invariant of the construction: one definition has no solution, one has an identically zero
  coefficient in exact dS, one never fires; every finite candidate is threshold- or convention-set, with a
  ×39 spread. **Z = √(32π/3) remains data-selected**; agentQ's 89%-depth merger reading remains a
  consistency statement, not a derivation. The pre-registered prior stands.
- **Framework-favorable nuances (raw, not oversold):** (i) Hr(a) = μ_F4 — the F4 kernel is literally the
  dimensionless radius of the stationary family (identity echo #3); (ii) at a₀ the graded exact-channel
  degradation is only 30–42% — i.e. the well-defined parts of the construction are NOT catastrophically
  broken at a₀; what is broken there is **locality** (the flat wedge overshoots the horizon by 314%, the
  wedge spans 89% of the patch). The convention-robust restatement of agentQ's F2: at a ≲ a₀ the
  construction does not so much FAIL as cease to be local — it becomes Gibbons–Hawking thermodynamics of
  the cosmological horizon itself, the Λ sector already in the Einstein equation. Same verdict, sharper
  attribution.
- **What would have changed the verdict** (pre-stated in §0): a c_i equal to 1/√(32π/3) symbolically,
  surviving the choice audit. None of the three definitions produced one; two produced no boundary at all.
  The hostile tier was armed and was not needed.

## 7. Disposition
- Banked: **Z is data-selected — unchanged, now with the breakdown-geometry door closed from three
  independent directions.**
- New exact facts banked for the program: the dS Killing-failure zero (strengthens agentQ R1; any future
  "finite-(H/a) Jacobson correction" claim citing O(x²·Riemann) terms in exact dS is wrong on its face);
  the universal graded coefficient 1/6 appearing in three independent exact channels (norm, temperature,
  equilibrium ratio) — a bookkeeping constant of the flat-frame approximation, NOT related to Z (3.5%
  near-miss to 1/Z already flagged meaningless in agentB/agentQ); the strict-merger no-solution theorem
  (tan x > x).
- The π-coincidence m(a₀) ≈ π (0.19%) is recorded HERE so that no future agent rediscovers it and feeds it:
  it is a transcendental near-miss with no derivation, the exact analogue of the 1/6-vs-1/Z bait.
