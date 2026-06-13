# agentMM — THE SKEPTIC'S FIREWALL CHARTER: the line a fourth-root-edge derivation must clear, and every way it can be faked

**STATUS: CHARTER ISSUED. This is an adversarial checklist the verify phase runs LINE-BY-LINE against any
claim that the fourth-root edge measure (q=1/4, the σ_req class) has been DERIVED from the pump/Λ dynamics —
as opposed to ASSUMED, requirement-matched, or back-fit. The charter does not itself derive anything. It
defines (1) what counts as a derivation, (2) the smuggle vectors that disqualify a claim, (3) the litmus a
clean derivation must pass. A claim that fails ANY item in §2 is downgraded from DERIVATION to
REQUIREMENT-MATCH, regardless of how many digits it reproduces.**

Date: 2026-06-12 (compute-first relaunch). Repo: zimmerman-formula. Working dir: real_research/reviews/toe_law/.
Hardware: local (sympy, dps≥30). Machine record for the structural facts this charter cites:
`/tmp/agentMM_verify.py`, `/tmp/agentMM_verify2.py` (rerun verbatim; all four anchor facts below confirmed).

**DISCIPLINE (inherited, absolute):**
- ζ̃ and the (16π/3)^(1/4) re-expression stay QUARANTINED as INPUT. They are never re-derived as a Z claim.
  Any pure number a candidate reports is logged RAW. A candidate that "derives" ζ̃ or (16π/3)^(1/4) is
  presumed to have fed it (smuggle vector S6) until proven otherwise.
- A KILL is verified as hard as a PASS. The fourth-root hook is framework-FAVORABLE territory; it therefore
  gets MAXIMUM hostility to wishful steps. The default verdict on any fourth-root "derivation" is
  REQUIREMENT-MATCH until §3's litmus is cleared in full.

---

## 0. THE TWO INPUT FACTS THIS FIREWALL GUARDS (both already flagged by their source agents)

**FACT A — LL's q=1/4 is a REQUIREMENT-MATCH, not a derivation (agentLL §0, §5.6–5.8, §10).**
LL proved a *conversion theorem*: an edge measure e^(−γx^(−q)) on x = c_χ − b, pushed through the Deser–Levin
map κ ∝ x^(−1/2), outputs a Laplace-transform index 2q/(2q+1), and index 1/3 ⟺ q = 1/4 uniquely. LL did NOT
derive that the pump's family measure ρ(b) actually HAS a fourth-root edge. LL explicitly leaves this as the
*named confirming calculation* (§5.5, §10.1): "derive ρ(b) near b = c_χ from the pump construction… PASS ⟺
oscillatory fourth-root essential edge singularity." Until that calculation is done with the fourth-root as
OUTPUT, q=1/4 is the TARGET LL is shooting at, supplied by the fingerprint — not a result LL extracted from
the pump. LL itself stamps this: §0 footnote, §5.7, §5.8 all say "requirement-match only… no identification claimed."

**FACT B — agentV's σ_req fourth-root is an INPUT class, the inverse-image of the data-selected μ-tail (agentV §2.1, §3, §7).**
V solved the INVERSE problem: GIVEN the RAR exponential μ-tail, the unique cut density is
σ_req ~ u^(−13/8) e^(−ζu^(−1/4)) cos(ζu^(−1/4) − π/8) — a fourth-root essential singularity. This is what the
mechanism MUST imprint; it is the demand, not a supply. V's own verdict: this class is ILLEGAL for any
dS-invariant Wightman function (positive Källén–Lehmann measures cannot be C^∞-flat-and-nonzero; the first
TWO power-correction conditions already collapse the measure to the zero-tail conformal point). So the
fourth-root is (i) a requirement extracted from data by inversion, and (ii) forbidden to any spectator
invariant field — it can only come from an invariance-BREAKING sector. A "derivation" that produces it from
a dS-invariant pump pullback is therefore not merely unproven — it is in tension with V's theorem and must
explain how it dodges the KL positivity kill.

**THE FIREWALL'S JOB.** LL §0 explicitly keeps the V-input ω^(1/4) class and the LL-response ω^(1/3) class
DISTINCT and forbids cross-contamination. The single most dangerous failure mode is laundering: taking the
V-side σ_req fourth-root (an INPUT/requirement) and re-presenting it as an LL-side DERIVED ρ(b) edge, so that
"the input matches the output" reads as a derivation when it is the same number entering and leaving. This
charter exists to catch that laundering and every variant of it.

---

## 1. WHAT COUNTS AS *DERIVING* THE FOURTH-ROOT EDGE MEASURE — THE PRECISE DEFINITION

A claim "the fourth-root (q=1/4 / σ_req-class) edge measure is DERIVED from the pump/Λ" is admissible as a
DERIVATION if and only if ALL of the following hold. (Any one missing ⇒ REQUIREMENT-MATCH at best.)

**D1 — Independent inputs.** The only objects fed in are:
  (a) the pump/Λ DYNAMICS (the locked construction's worldline/family equations of motion — EE's banked
      G_b(τ) pullback or its successor, with the family parametrization fixed BEFORE the answer is known), and
  (b) the Deser–Levin geometry (the κ(b) law, the family measure's geometric Jacobian) — fixed independently
      of the target, ideally cross-checked against EE's actual banked κ(b) rather than LL §5.2's reconstruction.
  NOT fed in: σ_req, the fingerprint F_req, q=1/4, the fourth-root, γ_req, ζ̃, or any quantity whose only
  prior source is the inversion/fingerprint side.

**D2 — The fourth-root is OUTPUT.** The exponent q must EMERGE from computing ρ(b)'s edge behavior — the
  worldline construction's family density as b → c_χ — and come out as q = 1/4 (i.e. ρ ~ exp(−γ(c_χ−b)^(−1/4))·…)
  by force of the dynamics, with the value 1/4 not appearing anywhere in the inputs or intermediate ansätze.

**D3 — Agreement discovered LAST.** The match between the derived q and the required q=1/4 (equivalently:
  between the derived transform index and 1/3, between the derived γ and γ_req, between the derived oscillation
  phase and the −π/4 / +π/3 quanta) is observed only AFTER the derivation closes — never used as a constraint
  during it. The clean signature: the deriver could not have known the answer would be 1/4 until the
  computation finished.

**D4 — Oscillatory member, not pure-decay, by the dynamics.** LL §5.6 and V §2.1(a) both require the OSCILLATORY
  member cos(γ x^(−1/4)+φ₀); the pure-decay member e^(−γx^(−1/4)) gives the wrong (no-cos) class and is
  EXCLUDED by the fingerprint. A derivation must produce the oscillation — and its phase — from the dynamics
  (e.g. a genuine complex-conjugate saddle pair / connection formula in the worldline construction), NOT
  insert cos(...) by hand to "match the fingerprint."

**D5 — The amplitude/constant is not laundered.** γ may be reported RAW. If the derivation also claims
  γ = γ_req (and thence ζ̃, and thence anything in the (16π/3)^(1/4) family), that claim is presumed a smuggle
  (S6) until D1–D4 are independently clean AND the constant comes out without ζ̃ ever being an input. Matching
  γ_req is NOT required for a partial-credit class-derivation; CLAIMING to derive ζ̃ triggers the quarantine.

**Machine anchors for what "the answer" is (so verifiers know exactly what a clean OUTPUT must hit):**
- The Deser–Levin map sends edge-exponent q to transform index **2q/(2q+1)** EXACTLY — confirmed numerically
  to diff 0.00e+00 at q ∈ {1/8,1/6,1/4,1/3,1/2,1} (`/tmp/agentMM_verify2.py`, MM-V1b). So index 1/3 ⟺ q=1/4,
  and `solve(2q/(2q+1)=1/3)` returns the single root **q=1/4** (MM-V2b). The map is strictly monotone
  (d/dq = 2/(2q+1)² > 0, MM-V2), so there is NO other edge exponent that fakes index 1/3 — a derivation
  cannot accidentally land 1/3 from a non-1/4 edge.
- The LL oscillation/decay ratio is **tan(π/(2(k+1)))**, strictly monotone in k; k=1/2 ⟹ ratio = √3 exactly
  (MM-V3, MM-V3b). So a clean OUTPUT must independently reproduce the √3 lock and the +π/3 phase quantum, not
  just the index.

---

## 2. THE SMUGGLE VECTORS — every way a "derivation" can secretly import q=1/4 / the fourth-root

Each vector is a CHECK. The verifier reads the candidate derivation line by line and asks the question in
**DETECT**. If the answer is yes, the listed vector fires and the claim drops to REQUIREMENT-MATCH (or worse).
Vectors S1–S4 are the four named in the charter prompt; S5–S9 are the additional laundering routes the two
source memos expose.

### S1 — Boundary-condition smuggle: feeding σ_req's class in as a BC
**The move.** Solving the pump/worldline construction as a boundary-value or matching problem and imposing,
as the edge/IR boundary condition, the fourth-root flatness (or the C^∞-flat-at-lightcone condition, or
"the cut density vanishes faster than every power at the edge"). The fourth-root then "appears" in ρ(b)
because it was nailed to the boundary.
**DETECT.** Does any boundary/matching/regularity condition encode flatness, all-moments-zero, an inverse
quarter-power, or "match σ_req at u→0"? Is the edge behavior of ρ(b) FIXED by a condition rather than COMPUTED
from the interior dynamics? Trace every BC to a dynamical or geometric origin that is blind to the target.
**WHY it's lethal here.** V §2.1(a) proves the fourth-root IS exactly the all-inverse-moments-zero condition
(M_k = ∫ρ u^(−1/2−k) du = 0 ∀k). Imposing flatness as a BC is *literally* imposing the answer. A legal
positive KL measure cannot even satisfy two of these conditions (V §5.2, identity x(x−2)−2(x−2)=(x−2)²,
machine residual = 0, `/tmp/agentMM_verify2.py` MM-V4) — so any BC that yields flatness has imported an
illegal structure as an assumption.

### S2 — Ansatz smuggle: using LL's conversion-theorem TARGET as the ansatz
**The move.** Writing the trial family measure as ρ(b) = (prefactor)·exp(−γ(c_χ−b)^(−q))·cos(…) with q (or the
fourth-root form) as the assumed functional shape, then "solving for" γ or the prefactor. The conversion
theorem's TARGET form is the ansatz; the derivation only fixes constants inside a pre-shaped exponent.
**DETECT.** Does the trial ρ(b) (or trial σ, trial W, trial edge measure) already contain x^(−q), a fractional
inverse power, or an essential singularity of the assumed type before the dynamics constrains it? Is q a free
parameter that gets PINNED to 1/4 by matching, rather than a number that FALLS OUT? If q is fit/solved-for
against the index-1/3 requirement, this is S2 (and overlaps S8).
**WHY it's lethal here.** LL §5.6's conversion theorem is explicitly a map FROM an assumed edge measure
e^(−γx^(−q)) TO an output index. Using its left-hand side as the ansatz means the "derivation" never computed
the edge measure — it postulated it in the exact class the theorem needs. The output index 1/3 is then
guaranteed by construction (the map is a theorem), not discovered.

### S3 — Parametrization smuggle: a pump parametrization pre-shaped to the answer
**The move.** Choosing the worldline/family parametrization, the variable in which "b" is measured, the
profile coordinate, or the pump's time/affine parameter so that the fourth-root is built into the change of
variables — e.g. defining the family coordinate as (already) a square-root or quarter-power of the natural
geometric one, so a benign edge behavior in the chosen coordinate is a fourth-root in the physical one.
**DETECT.** Is the family/edge coordinate the GEOMETRICALLY NATURAL one (the Deser–Levin invariant separation
u = Z−1, the orbit parameter b with EE's banked normalization), or a re-coordinatization introduced by the
deriver? Re-derive the edge exponent in the banked invariant variable u = Z−1 and in b directly; if the
fourth-root only appears after a deriver-chosen variable change, S3 fires. Cross-check the Jacobian dZ/ds =
κ√(u(u+t)) (V [V-A1]) and 2−t = 2a²/κ² (machine MM-V3b) — the geometry is FIXED; a derivation may not
re-define it to manufacture the power.
**WHY it's lethal here.** The Deser–Levin map κ ∝ x^(−1/2) is the ENTIRE 1/4→1/3 converter (LL §5.6: "the
Deser–Levin square-root map is the 1/4→1/3 index converter"). The √-map is geometry and must be used as
banked, not re-chosen. Smuggling a second square root into the parametrization double-counts the map and
fakes the quarter-power.

### S4 — Fit smuggle: fitting γ (or q, or the phase) to γ_req / the fingerprint
**The move.** Treating γ, q, φ₀, or the prefactor power as free parameters and least-squares / matching them
to γ_req = 2^(1/4)√H·ζ̃/(4√π·c_χ^(1/4)) (LL §9), or to the fingerprint's c̃, √3, +π/3. The "agreement" is then
a fit residual, not a derivation.
**DETECT.** Are γ, q, φ₀ outputs of the dynamics, or knobs turned to match a banked target? Is there ANY
optimization, matching, or "choose constants such that" step whose objective references σ_req, F_req, γ_req,
c̃, ζ̃, √3, or π/3? Count the free parameters vs the matched targets — if #targets ≥ #free, the match is fitting.
**WHY it's lethal here.** γ_req already contains ζ̃ (LL §9). Fitting γ to γ_req back-imports ζ̃ — a direct
quarantine breach. Note LL is honest that γ is NOT derived (§9: "γ is NOT derived; fixing it (hence ζ̃)
requires the family-measure derivation"). A candidate that "fixes" γ has either done the real family-measure
derivation (then S1–S3 must also be clean) or fit it (S4).

### S5 — Inverse-image laundering: re-presenting V's σ_req as a derived ρ(b)
**The move.** Taking agentV's σ_req (the INVERSE-image of the data μ-tail, FACT B) — or its proper-time form
exp(−ζ̃/√ρ_c)cos(ζ̃/√ρ_c), or its mass-space ρ_KL ~ exp(−bM^(1/3)) shadow — and inserting it into the pump
calculation as "the correlator the pump produces," then observing it has a fourth-root edge. The number
enters from the data side and leaves looking like a pump output.
**DETECT.** Does the correlator / cut density / W used in the pump derivation trace back to V's inversion
(σ_req, the RAR μ-tail, the double-Laplace inversion of V §1.2) rather than to a forward computation from the
pump Lagrangian/construction? Is the field two-point structure POSTULATED to be σ_req-class, or COMPUTED from
the pump's own dynamics? Any appearance of u^(−13/8), u^(−2)e^(−ζu^(−1/4))sin(...), the −π/4 diagonal, or
ζ = 2^(−1/4)η^(−1/2) sourced from V is laundering.
**WHY it's lethal here.** This is the headline failure mode (§0). LL §0 firewalls the V-input class (ω^(1/4))
from the LL-response class (ω^(1/3)) precisely to prevent it. V §7 further proves σ_req is ILLEGAL for any
dS-invariant W — so if the pump is a dS-invariant pullback, σ_req CANNOT be its forward output, and any
derivation "producing" it has smuggled it past the KL positivity wall.

### S6 — Constant smuggle: deriving ζ̃ or (16π/3)^(1/4)
**The move.** The derivation reports that γ (or ζ, or the edge strength β) comes out equal to a ζ̃-bearing
expression, or that ζ = (16π/3)^(1/4), presenting the quarantined number as a derived result.
**DETECT.** Does any derived constant equal, simplify to, or get compared against ζ̃, (16π/3)^(1/4), Z =
√(32π/3), or the β = ζ̃/2 dictionary (LL §9, LL-2d)? Was ζ̃ an input anywhere upstream (then it's circular)?
**WHY it's lethal here.** ABSOLUTE QUARANTINE. V §6 already flags ζ = (16π/3)^(1/4) = 2.0232 as "a
re-expression of the convention, NOT a derivation." Any candidate re-deriving it has either fed it or
committed the same numerology. Report raw, quarantine, do not grade as a Z claim.

### S7 — Map double-use / circularity: importing the Deser–Levin √ twice or assuming the converted class
**The move.** Using the κ ∝ x^(−1/2) map to "convert" an edge measure whose fourth-root was ITSELF obtained
via the same map (or via the conversion theorem run backward), so the geometry is invoked twice and the index
1/3 is guaranteed by the map's own algebra rather than by independent edge dynamics.
**DETECT.** Is the input edge measure to the conversion theorem independent of the map, or was it produced by
inverting the map against index 1/3? Run the dependency graph: the edge measure must come from the worldline
construction BEFORE any Deser–Levin push-forward; the map is applied ONCE, at the end, to a measure derived
without it.
**WHY it's lethal here.** The conversion theorem (LL §5.6) and the requirement-match (LL §5.7) are the SAME
map in two directions. A derivation that goes target → (map⁻¹) → "required edge measure" → (map) → index 1/3
is a tautology. Only target-FREE edge dynamics → (map) → index breaks it.

### S8 — Solve-for-q smuggle: leaving q free and letting the index-1/3 requirement pin it
**The move.** Carrying q symbolically through the derivation and fixing it at the END by demanding the output
match index 1/3 (or the fingerprint). Looks like a derivation because q "wasn't assumed" — but it was SOLVED
from the target.
**DETECT.** At the moment q acquires the value 1/4, what equation fixes it? If that equation references the
target (index 1/3, F_req, σ_req, √3), it is S8. A clean derivation fixes q from an equation containing ONLY
pump/geometry quantities, and the verifier checks 2q/(2q+1)=1/3 holds AFTERWARD as a discovered coincidence.
**WHY it's lethal here.** Because the map 2q/(2q+1) is invertible and monotone (MM-V2), "solve for q given
index 1/3" ALWAYS returns exactly 1/4 (MM-V2b). That is not evidence the pump produces 1/4 — it is the
inverse function evaluated at the target. The single root means there is no robustness check that could fail;
the verifier must confirm q was fixed by pump dynamics, not by this inversion.

### S9 — Member smuggle: hand-selecting the oscillatory branch to match the fingerprint
**The move.** The dynamics produce a pure-decay edge measure (or an ambiguous real/complex pair) and the
deriver SELECTS the oscillatory member cos(γx^(−1/4)+φ₀) "because the fingerprint has oscillation," or inserts
the −π/4 / +π/3 phase by hand to match.
**DETECT.** Is the oscillation (and its phase) forced by a genuine complex-conjugate saddle pair / connection
formula in the pump construction, or chosen post hoc? Is the pure-decay member excluded by the DYNAMICS or by
appeal to the fingerprint? (V §2.1: pure-decay gives the no-cos class — excluded by the data, NOT by the pump.)
**WHY it's lethal here.** D4 requires the oscillation to be an output. The √3 lock and +π/3 phase are
theorem-grade consequences of a cube-root saddle TRIAD (LL §2); a derivation must exhibit that triad in the
pump's own action, not borrow the phase from LL-2's connection formula.

---

## 2.1 SMUGGLE-VECTOR QUICK TABLE (verifier scans every derivation against all nine)

| #  | Vector                          | One-line detect question                                                    |
|----|---------------------------------|-----------------------------------------------------------------------------|
| S1 | BC smuggle                      | Is edge flatness / fourth-root imposed as a boundary/regularity condition?  |
| S2 | Ansatz smuggle                  | Does the trial measure already contain x^(−q) / the essential singularity?  |
| S3 | Parametrization smuggle         | Does the fourth-root appear only after a deriver-chosen variable change?     |
| S4 | Fit smuggle                     | Is γ/q/φ matched to γ_req / c̃ / √3 / π/3 by optimization?                   |
| S5 | Inverse-image laundering        | Does the correlator trace to V's σ_req inversion, not a forward pump comp?   |
| S6 | Constant smuggle                | Does a derived constant equal ζ̃ or (16π/3)^(1/4)?                          |
| S7 | Map double-use / circularity    | Is the edge measure itself a product of the Deser–Levin map / theorem⁻¹?     |
| S8 | Solve-for-q smuggle             | Is q fixed by an equation that references the target index 1/3?              |
| S9 | Member smuggle                  | Is the oscillatory branch / phase chosen to match the fingerprint by hand?   |

---

## 3. THE LITMUS — the checklist verifiers run line-by-line on any fourth-root "derivation"

A clean derivation must compute **ρ(b)'s edge from the pump dynamics + the Deser–Levin geometry ALONE**, with
the fourth-root as **OUTPUT**, and any agreement with q=1/4 discovered **only at the end**. The verifier walks
the candidate top to bottom and checks each L-item in order. The derivation earns DERIVATION grade only if
EVERY L-item passes. The first failure stamps the verdict and names the firing smuggle vector.

**L0 — Provenance ledger.** List every input the derivation uses. For each, mark its origin: [PUMP] (the
locked construction's Lagrangian/EOM), [GEOM] (Deser–Levin κ(b), the family Jacobian, the invariant Z(s)),
or [TARGET] (σ_req, F_req, q=1/4, the fourth-root, γ_req, ζ̃, √3, π/3, the RAR μ-tail). **PASS ⟺ zero [TARGET]
inputs.** Any [TARGET] input fires the matching vector (σ_req→S5, q/fourth-root ansatz→S2, γ_req→S4, ζ̃→S6)
and ends the review at REQUIREMENT-MATCH. (Enforces D1.)

**L1 — Forward direction.** Confirm the computation runs pump → edge measure → (Deser–Levin map, applied
ONCE) → index, never target → (map⁻¹) → edge measure. Draw the dependency arrows. **PASS ⟺ no arrow points
from the target back into the edge measure.** A backward arrow fires S7/S8. (Enforces D2, D3.)

**L2 — Edge exponent is computed, not assumed.** Locate where q (or the inverse-power exponent of the edge
singularity) acquires the value 1/4. **PASS ⟺ the fixing equation contains ONLY [PUMP]/[GEOM] quantities and
the deriver could not have known it would be 1/4 beforehand.** If q is symbolic and pinned by matching index
1/3, S8 fires; if x^(−q) was in the trial form, S2 fires. The verifier independently recomputes 2q/(2q+1)
from the derived q and checks it lands 1/3 (MM-V1b/V2b) — this check happens AFTER L2 passes, as the
"discovered coincidence," never before. (Enforces D2, D3, kills S2/S8.)

**L3 — Geometry used once, as banked.** Confirm the Deser–Levin √-map κ ∝ x^(−1/2) is applied exactly once
and matches EE's banked κ(b) (or, if LL §5.2's reconstruction κ(b)=H/√(c_χ(c_χ²−b²)) is used, that it is
verified against EE's actual banked value, per LL §10.1). Re-derive the edge exponent in the banked invariant
variable u = Z−1 (Jacobian dZ/ds = κ√(u(u+t)), 2−t = 2a²/κ² — machine MM-V3b) to confirm no second square
root was smuggled into the parametrization. **PASS ⟺ one map use, banked κ, fourth-root survives in the
geometrically natural variable.** Failure fires S3/S7. (Enforces D1.)

**L4 — Oscillation is dynamical.** Find where cos(γx^(−1/4)+φ₀) (the oscillatory member) and its phase come
from. **PASS ⟺ a genuine complex-conjugate saddle pair / connection-formula / cube-root triad in the PUMP's
own action produces the oscillation and the phase; the pure-decay member is excluded by the DYNAMICS, not by
appeal to the fingerprint.** Hand-insertion of cos(...) or the −π/4 / +π/3 phase fires S9. Cross-check that
the derived oscillation/decay ratio independently reproduces √3 (k=1/2, MM-V3) — discovered, not imposed.
(Enforces D4.)

**L5 — No boundary-condition flatness.** Inspect every boundary, matching, and regularity condition. **PASS ⟺
none encodes flatness, all-moments-zero, C^∞-flatness at the lightcone, or "match σ_req at the edge."** Recall
the flatness IS the all-inverse-moments-zero tower (V §2.1a) and is ILLEGAL for any positive KL measure — two
conditions already collapse it (V §5.2, identity residual = 0, MM-V4). A BC that yields flatness imported the
answer: S1 fires. (Enforces D1.)

**L6 — Constants reported raw; ζ̃ not claimed.** Confirm γ and every pure number are reported RAW. **PASS ⟺
the derivation does NOT claim γ = γ_req, ζ = (16π/3)^(1/4), or any ζ̃/Z identity as a result.** If it does, and
ζ̃ was anywhere upstream, the claim is circular (S6) and quarantined; if ζ̃ was genuinely absent upstream, the
constant match is logged RAW and flagged for separate quarantined review — never graded as a Z claim.
(Enforces D5.)

**L7 — Legality reconciliation (the V-theorem gate).** If the pump pullback is dS-INVARIANT, the derivation
claims to produce a cut that V §7 proved no dS-invariant Wightman function can have. **PASS ⟺ the derivation
either (a) explicitly breaks dS invariance in the sector that carries the fourth-root (consistent with V §5.3
and the repo's khronon/condensate spec), and says so; or (b) identifies precisely which step evades V's KL
positivity kill and why that is legitimate.** A silent dS-invariant derivation that yields σ_req-class output
without addressing V's theorem is internally inconsistent — it has smuggled an illegal structure (S1/S5) past
a proven wall. (This is the deepest check: the fourth-root being ILLEGAL for invariant fields means a clean
derivation MUST live in an invariance-breaking sector or it is wrong on its face.)

**L8 — Deep-MOND endpoint honesty.** If the derivation also claims the deep-MOND √x onset, check it against
V's NO-KERNEL theorem: 2−t = 2a²/κ² is analytic in a² (MM-V3b), so any convergent transform gives m_ind =
const + O(a²) at a→0 — μ ∝ (a/a₀)^(1/2) is structurally unreachable by the linear field-bath class. **PASS ⟺
the derivation does NOT claim to derive the exact deep-MOND power from a convergent pump transform** (it may
only claim the high-a fourth-root tail, or must invoke an IR-divergent / invariance-breaking escape and flag
it). A claim of the exact √x onset from a convergent kernel contradicts a machine-backed theorem and fails.

---

## 3.1 THE GRADING LADDER (what the verdict may say)

The verifier returns exactly one grade, with the first-failing L-item and firing S-vector named:

- **DERIVATION (the target outcome, not yet achieved by anyone).** L0–L8 all pass. The pump dynamics + banked
  Deser–Levin geometry output a fourth-root oscillatory edge measure, q=1/4 discovered last, oscillation
  dynamical, constants raw, legality reconciled (invariance-breaking sector identified). Only THIS grade lets
  the chain say the fourth-root edge is derived rather than required.

- **CLASS-DERIVATION, CONSTANT OPEN (partial credit).** L0–L5, L7, L8 pass (the fourth-root edge and its
  oscillation are genuine outputs of the dynamics) but L6 is not attempted or γ is left raw/unmatched. This is
  the honest best-case short of full closure: the CLASS is derived, ζ̃ stays quarantined and underived. This
  is strictly stronger than LL's current state (LL has the conversion theorem but NOT the family-measure
  derivation — LL §10.1 names exactly this as the open calculation).

- **REQUIREMENT-MATCH (LL's current banked state, the default).** Any of L0–L5 fails: the fourth-root was
  assumed, fed, fit, laundered, or BC-imposed. The map 2q/(2q+1)=1/3 is a theorem, so "the index comes out
  1/3" is worth nothing if the edge measure was the conversion-theorem target (S2) or solved from index 1/3
  (S8). This is where LL honestly sits today and where any unverified "derivation" defaults.

- **INCONSISTENT (worse than requirement-match).** L7 fails: a dS-invariant derivation yields the σ_req class
  without addressing V's positivity kill, or L8 fails: a convergent kernel claims the exact deep-MOND power.
  The candidate contradicts a machine-backed theorem and is wrong, not merely unproven.

---

## 4. VERDICT — the charter, stated for the verify phase

**CHARTER ISSUED. The verify phase shall, for ANY claim that the fourth-root / q=1/4 / σ_req-class edge
measure is DERIVED from the pump/Λ:**

1. Build the **L0 provenance ledger**; reject at REQUIREMENT-MATCH on any [TARGET] input.
2. Walk **L1–L8** in order; the first failure stamps the grade and names the firing **S-vector (S1–S9)**.
3. Independently recompute the two map facts as the discovered coincidences (never as inputs): the edge
   exponent → index via **2q/(2q+1)** (machine: exact, diff 0 at all q; root of index-1/3 is the unique
   q=1/4), and the oscillation/decay ratio **√3 at k=1/2** (machine: tan(π/(2(k+1))), strictly monotone).
4. Apply the **L7 legality gate** at full weight: because V proved the fourth-root cut is ILLEGAL for every
   dS-invariant Wightman function (positive KL measures collapse under the first two conditions — identity
   x(x−2)−2(x−2)=(x−2)², machine residual 0), a clean derivation MUST live in an invariance-breaking sector
   and say so, or be graded INCONSISTENT.
5. Return one grade from §3.1, RAW constants only, ζ̃ and (16π/3)^(1/4) QUARANTINED throughout.

**Both-ways honesty, banked.** This territory is framework-FAVORABLE (a fourth-root edge would hand the
a₀ ∝ √ρ_DE kernel law for free — V §6/§7: any O(1)-ζ kernel of this class ⇒ a₀ ∝ cH automatically). Precisely
because it is favorable, the charter is maximally hostile to wishful steps: the default is REQUIREMENT-MATCH,
and a PASS requires clearing all of L0–L8. Symmetrically, the charter does NOT manufacture a kill: a
derivation that genuinely runs pump → edge → (map once) → index 1/3, with oscillation dynamical and the
invariance-breaking sector named, EARNS the DERIVATION grade — the litmus is passable in principle, and the
repo's own spec (khronon/condensate, the invariance-breaking carrier V §5.3 selects) is exactly the sector
where it could pass. The line is drawn so that a real result is recognized and a laundered number is not.

## 5. Files / repro / anchors
- This charter: `real_research/reviews/toe_law/agentMM_firewall.md` (written incrementally).
- Machine record for the four anchor facts: `/tmp/agentMM_verify.py`, `/tmp/agentMM_verify2.py` (rerun:
  `python3 /tmp/agentMM_verify.py && python3 /tmp/agentMM_verify2.py`; sympy; confirms 2q/(2q+1) index map
  exact to diff 0, q=1/4 the unique root of index 1/3, 2−t = 2a²/(H²+a²) ∝ a², KL collapse identity residual 0).
- Sources read (named sections only, per READ-LIGHT): `agentLL_generator_scoping.md` (the conversion theorem
  §5.6, the requirement-match firewall §0/§5.7/§5.8, the named confirming calculation §5.5/§10.1, γ_req §9);
  `agentV_kernel_inversion.md` (σ_req fourth-root class §2.1/§3, the KL positivity kill §5.2/§7, the
  deep-MOND NO-KERNEL wall §2.2, the dS-invariance-breaking escape §5.3).
- Quarantine ledger: ζ̃, (16π/3)^(1/4), Z = √(32π/3), β = ζ̃/2, γ_req — all INPUT, none re-derivable as a Z claim.
