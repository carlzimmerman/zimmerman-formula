# HANDOFF TO CONDUCTOR — from AG4 (argon interactive session, 2026-10-15)

Lane: `argon_push/AG4_law_from_action/` — LANDED. **BRANCH (a) CONFIRMED** (pre-registered
in AG3 HANDOFF §4): the unique static rest state of the frozen S2 action is the canonical
law ḡ = g²/(g+a₀). Lean 12/12, axioms clean. G4 FAILED-as-frozen, kept failed on record
(exit 1); physics bound γ-correction ≤1.09% recorded loud. Mutations M1–M3 as designed.
Register rows below are PROPOSALS per LOOP_CONDUCTOR §2.9; this session touched only
`argon_push/`.

## Proposed register rows

1. **LAW-FORM ADJUDICATED (theory-internal): rest state of the frozen S2 action =
   canonical ḡ = g²/(g+a₀) (n=1).** Derivation: δL/δΦ ⇒ ∇·A = 4πGρ_b (A ≡ ∇Φ−KP is
   baryon-only); δL/δP at rest ⇒ ḡ = u²/(a₀−u), u = K|P| = g_ph; ⇔ u²+ḡu = a₀ḡ ⇔
   g² = ḡ(g+a₀). PAPER49's uniqueness claim DERIVED (algebra Lean-certified T1–T9b);
   anchors exact: ν(10⁻⁴a₀) = 100.50125 vs cited 100.5; Σ̄_max = a₀/(πG) = 213.7 vs cited
   214; ARGON02 P1 M_ph/M_b = (√(1+4x²)−1)/2 and ρ_ph = M_b/(2πr_M²r√(1+4x²)) derived
   from the action. Verification: ag4_derive_results.json, AG4_law_from_action.out.
2. **The quadratic a₀-line g²−ḡ² = a₀ḡ is the n=2 (half-capacity) rest state — a
   DIFFERENT theory** (K W_rem′ = u²/(a₀−2u); tether bound g_ph < a₀/2; Σ̄_max ≈ 107).
   Certified distinct (T7_n2_not_canonical: canonical law holds on the n=2 rest state only
   if ḡu = 0). Consequence routing (OWNER DECISION, below).
3. **G4 γ-reduction bound:** ratio |γ∇²P|/tether → (L*/r_M)² structurally; ≤1.09% in all
   four corners for r ≥ 10r_s; ≤0.004% at fiducial L*=5.75 pc. Frozen thresholds sat at
   the structural asymptote ⇒ gate FAILED as frozen, recorded, not re-adjudicated. The
   γ=0 reduction used by ARGON02/AG1/AG3 is valid at the percent level outside the
   screening core.
4. **Open empirical counterweight (registered, not buried):** SPARC mildly prefers n=2
   (AG3 lawform diagnostic: paired rms 0.178 vs 0.220 dex; ρ=½ crossings +0.063 vs
   +0.493; band ratios −0.204 vs −0.466). γ corrections cannot explain it (10⁻⁹ at
   fiducial L*); a 16–25% Υ_disk overestimation (fit circularity) fully absorbs it.
5. **PAPER49/S2 mislabel:** ḡ = g²/(g+a₀) is called the "simple interpolating function
   (Famaey & Binney 2005)" in both; the algebra + ν=100.5 pin standard μ = x/(1+x).
   Dated-erratum proposal (label only; math untouched).

## OWNER DECISION required (physics, not process)

The user-profile statement of the program carries the quadratic a₀-line
(g_obs² − g_bar² = a₀·g_bar) as THE law; the frozen canonical S2 + PAPER49 + the action
derivation carry ḡ = g²/(g+a₀). Both cannot be the rest state of the same action. Routes:
- **(A)** Canonical stands (AG4 branch a): profile shorthand + G071's tested form get a
  dated correction note; G071 re-runs under canonical (expected pooled rms ~0.17–0.22 on
  AG3-style cuts; registered benchmark comparison becomes canonical-vs-RAR).
- **(B)** Carl holds the a₀-line as THE law: S2's W_rem gets a dated v2 with capacity
  a₀/2 — and PAPER49's ν=100.5 and Σ̄=214 anchors CHANGE (they are n=1 numbers: ν=100.5
  would become ~100.005... exactly: ν_n2(10⁻⁴a₀) = (1+√(1+1/10⁻⁴·...)) — script it),
  ARGON02 P2/P3 re-derive (r_e 5.843 → 6.285 r_M), and the tether-capacity falsifier
  (row 6) becomes the discriminator.
Either route is append-only; no file outside argon_push/ was touched.

## Spawn proposals

- **AG4b — Υ-marginalized SPARC law-form re-analysis** (resolves row 4): re-fit Υ_disk
  per galaxy (prior from stellar populations, NOT from the rotation curve) and re-run the
  paired law comparison; pre-registered: canonical survives if the preference flips or
  falls below 2σ; ≥3σ survival of the n=2 preference escalates to the owner decision.
- **AG4c — capacity census** (row 6 falsifier, frozen recipe): max phantom surface
  density over strong-lensing arcs + edge-on disk warps; any well-measured sheet with
  Σ_ph ∈ (107, 214] M⊙/pc² excludes n=2. Numbers frozen HERE, before any data pull.
- **AG2 — tether-medium mode analysis** (carried): does W_rem + γ change the AG1 ladders?
  AG3 B2 (baryon drift) stabilizes; AG4 G4 bounds γ ≤1.09% — AG2's stiffness question is
  now tightly bracketed.
- **AG3b — three named candidates** (carried from AG3): UGC 06787 / 02953 / 09133
  disturbance check.
- **AG1-L — Lean certification of AG1 identities** (carried; AG4's file is the template:
  cached Mathlib via fable_independent_2026/lean_2026, lake env lean).

## Housekeeping

- Frozen-first chain: 93e579ec1 (criteria) + c80cdb5fd (AMD-A), both pre-run, both
  committed alone.
- Exit codes: MAIN 1 (G4 failed-as-frozen; branch (a) established; all other gates PASS);
  MUTATE 1 (same) with M1–M3 True. Lean exit 0.
- Kill test 3 (S2 text drift): asserted verbatim at runtime; passed.
- Sibling processes untouched; G071/G081/G111/GF2/ARGON02/PAPER49 files read-only.
