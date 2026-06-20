# ODA arXiv:2509.23648 — does it DERIVE the framework's GAP-1 kinetic-term origin? — verdict 2026-06-19

**Workflow:** `oda-gap1-origin` (bridge-scout's best GAP-1 origin lead; verbatim PDF read of Oda
arXiv:2509.23648v1 "Emergence of General Relativity from Cosmological Constant Via Ghost Condensation,"
Eqs. 2.1–3.8 inspected directly; 2 sympy scripts in `oda_door/`, both exit 0; 3 pro-Oda steelmans both ways;
independent re-verification of the load-bearing G-cancellation this session).

## HEADLINE (both ways): GR-ONLY / FALSE-COGNATE. The deepest wall (GAP-1) did NOT move.

Oda's "ghost condensation" generates the **Einstein–Hilbert R term** from a Faddeev–Popov **anticommuting
gauge-ghost** bilinear VEV `2i⟨c̄c⟩ = 1/16πG` (Eq. 3.1) — a FALSE COGNATE of the framework's GAP-1 object,
the **commuting bosonic** ghost-condensate `K(Q)=μ²(Q−1)²` (ACLM/Blanchet–Skordis P(X), wrong-sign-then-
stabilized minimum at X₀>0). They share only the word "condensate." Oda (a) does **NOT** derive the FORM
K(Q)=μ²(Q−1)², (b) does **NOT** transmit to MOND/a₀/preferred-frame, (c) does **NOT** fix κ/Z/a₀. This is a
Door-D-class **PARTIAL/NOT-FORCED**, and on the deciding axis it is **weaker than an analogy** (boson↔fermion
mismatch). Honest residual credit at full weight: Oda IS the closest published existence-proof that a
condensate VEV can dynamically generate a *gravitational kinetic structure* from a Λ-only start. Honest
concession at full weight: wrong term (EH not K(Q)), wrong field (fermionic gauge ghost not bosonic scalar),
wrong output (Lorentz-INVARIANT GR that STRUCTURALLY EXCLUDES the extra scalar), Λ not consumed, a₀ untouched.

---

## (1) What Oda's mechanism actually does — GR-from-Λ via FP-ghost condensation (steps verbatim)

1. **Bare Λ action** `S₀=(Λ/16πG)∫√−g` (Eq. 2.1) — pure cosmological constant, NO scalar kinetic term, NO matter.
2. **Weyl-covariantize** with a non-dynamical scalar: `Sc=λ∫√−g φ⁴` (Eq. 2.2), invariant under g→Ω²g, φ→Ω⁻¹φ
   (Eq. 2.3). Gauge φ=v with λv⁴=Λ/16πG reproduces (2.1).
3. **BRST gauge-fix Weyl with R=0** (Eq. 2.5) using the Weyl-BRST transform δ_B g_μν=2c g_μν, δ_B φ=−cφ,
   δ_B c̄=iB (Eq. 2.4). The BRST-exact action `S_GF+FP=−i∫δ_B(√−g c̄R)=∫√−g[(B+2i c̄c)R − 6i c̄□c]` (Eq. 2.6),
   c, c̄ anticommuting FP ghost/antighost.
4. Redefine B̃=B+2i c̄c → `Sq=∫√−g[B̃R + λφ⁴ − 6i c̄□c]` (Eq. 2.10).
5. **THE CONDENSATION (postulated):** strong gravity near M_Pl is ASSUMED to drive the FP-ghost bilinear to
   condense, VEV POSTULATED as `2i⟨c̄c⟩=1/16πG` (Eq. 3.1); also ⟨c̄□c⟩=0.
6. Substituting → **final** `Sq=∫√−g[(1/16πG)R + λφ⁴]` (Eq. 3.5) — EH + a still-present cosmological term.
   Oda's framing: 2 fermionic FP-ghost dof removed → 2 bosonic graviton dof created; the {c̄c, …} bound state
   is a BRST quartet **confined to the unphysical Hilbert space** (Eqs. 3.6–3.8), no Goldstone left behind.

## (2) Does it DERIVE K(Q)=μ²(Q−1)² FROM Λ? — NO. Not even a partial-FORM motivation: a FALSE COGNATE.

`oda_gap1_mapping.py` CHECK 1 (sympy): framework K'(Q₀)=0 at Q₀=1, K''(1)=2μ²>0 — a **bosonic P(X)** with a
stabilized minimum. Oda's object is a **constant fermionic bilinear VEV** with a STANDARD right-sign kinetic
term −6i c̄□c (Eq. 2.10) — no function K(·), no derivative VEV ⟨(∂φ)²⟩=X₀, no wrong-sign-then-stabilized
minimum. Structural mismatch on EVERY axis: field statistics (boson↔fermion), object type (P(X)↔bilinear VEV),
breaking (spontaneous Lorentz/frame ↔ Weyl gauge-fix/BRST), spectrum (physical propagating ↔ unphysical
confined). **Not a partial-form motivation — a false cognate.** Oda generates ONLY the EH graviton structure.

## (3) Does it TRANSMIT to MOND/a₀, and does it FIX the coefficient (circular?) — NO and NO (a₀ is G-independent).

- **Transmit: NO.** Final action (Eq. 3.5) = (1/16πG)R + λφ⁴: exactly 2 graviton dof, fully Lorentz-INVARIANT
  GR. None of the framework's MOND ingredients appear (no propagating dark scalar, no J(Y), no a₀, no aether
  u^μ, no disformal/LV structure). Oda goes further and **STRUCTURALLY EXCLUDES** the extra scalar: the gauge
  R=0 is chosen so even an f(R)/R² scalaron "cannot be derived and only Einstein's general relativity can be
  induced" (p.6, verbatim). The framework's dark sector IS exactly such a scalar — Oda's construction forbids
  it. CHECK 2b: Λ is **not consumed** — it survives intact as λφ⁴ in Eq. 3.5; the R term comes from the
  SEPARATE FP-ghost VEV. So even "EH from Λ" is really "EH from a new VEV alongside an untouched Λ."
- **Coefficient: NO, and a₀-IRRELEVANT.** Oda pins only Newton's constant 1/16πG. **Independently re-verified
  this session** (sympy): a₀ = κc·√(G·ρ_DE) with ρ_DE=Λc²/8πG ⟹ a₀ = √2·√Λ·c²·κ/(4√π) = κc²√(Λ/8π),
  **∂a₀/∂G = 0 exactly** — G cancels. Pinning G (Oda's only output) cannot touch a₀, κ, or Z. And even G_N is
  not genuinely derived: ⟨c̄c⟩ at coincident points is ill-defined (Eq. 3.2, conceded), regularization "beyond
  the scope," 1/16πG ASSUMED by dimensional matching. The free O(1) magnitude is CHOSEN to land 1/16πG —
  structurally the banked CKN circularity. Confirms KAPPA_FORCING_DOOR_CLOSED.

**Steelmans (both ways, all FAIL):** S1 "condensate-VEV-from-Λ mechanism class" survives only as a LOOSE
analogy (broken on target term EH-not-K(Q), field fermion-not-boson, output unphysical-confined). S2
"spontaneous breaking" FAILS — OPPOSITE direction (Oda gauge-fixes Weyl and RESTORES Lorentz-invariant GR;
GAP-1 needs Lorentz-VIOLATING frame selection). S3 "fermionic→bosonic dof trade" FAILS — the 2 traded dof land
on the graviton and EXCLUDE the extra scalar.

## (4) Updated GAP-1 / founded-not-derived standing — the deepest wall did NOT move; where it stops.

GAP-1 stays **POSTULATED-not-DERIVED**. Oda joins Door D (Mersini–Houghton phantom forcing, vacuous since the
framework is never phantom) and the dead dS-Unruh SO(4,1) route as a **NOT-FORCED** origin candidate. The
ghost-condensate lineage (Hořava → ACLM/Mukohyama → Lim-Sawicki-Vikman → AeST → Blanchet–Skordis) supplies the
framework's EFT *home* and frame-selection *mechanism* (banked GHOST_CONDENSATE_2026-06-19: gate genuinely
evaded, Jeans instability dS-cured) but **still no UV ORIGIN for the FORM of K(Q)** — and Oda, the most direct
published "ghost condensate FROM Λ," turns out to be the FP-gauge-ghost kind, not the ACLM bosonic kind. Where
it stops: the wall is exactly K(Q)=μ²(Q−1)² being **postulated**; Oda derives EH (never the wall) via a
different-statistics condensate that excludes the very scalar the framework needs.

Quarantine held: a₀/Z/κ/I₀ never asserted derived. Both-ways: closest-published-mechanism-class existence
proof credited at full weight; GR-only + false-cognate + Λ-not-consumed + a₀-untouched conceded at full weight.
No manufactured origin; no reflexive dismissal.

**Files (absolute):**
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/oda_door/oda_gap1_mapping.py (exit 0)
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/oda_door/oda_steelman_bothways.py (exit 0)
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/GHOST_CONDENSATE_2026-06-19.md (banked GAP-1 standing)
