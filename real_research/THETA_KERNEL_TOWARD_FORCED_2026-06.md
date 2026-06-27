# θ(y) toward FORCED — resolving √2-vs-2 and deriving the kernel shape from the dS bath

*C. Zimmerman, 2026-06-27. Pure framework-internal (no comparison). Axiom: inertia = nonlocal
response to the de-Sitter cosmic-horizon Unruh bath; T(a) = (ħ/2πk_Bc)√(a²+(cH_Λ)²) (Deser–Levin);
a₀ = cH_Λ/Z = 9.36×10⁻¹¹; μ_fw(x) = (√(1+4x²)−1)/2x; identity 1/μ_fw − μ_fw = 1/x. Footing throughout:
a₀ = 9.36×10⁻¹¹, the framework's OWN dS–Unruh interpolation, never McGaugh ν. Quarantine: pinning θ
does NOT derive a₀ (θ lives inside A = a_in + θa_ex; a₀ sits outside, in μ_fw[A/a₀]); Z remains a posit;
SM walled. LOCAL — not git-pushed.*

Scripts (all run clean, sympy + numpy):
`/private/tmp/.../scratchpad/derive1_theta0.py`, `derive1_normalization.py`, `derive_luo_efe.py` (NEW
independent check), and `opus_48_extended_research/reviews/mi_kernel_bath/kernel_shape_from_wightman.py`.

---

## 1. √2-vs-2 — RESOLVED to a single θ(0) = √2 (with a named, bounded residual toward 2)

**It resolves.** On the framework's OWN coupling the ambiguity is NOT symmetric — it collapses to the
lower endpoint. Two independent framework-internal routes converge:

**Route A — the excess-heat engine (derive1).** Inertia tracks the excess Unruh heat
ΔT = T(a) − T(0) ∝ √(a²+(cH)²) − cH, which is **degree-1 (linear) in the acceleration amplitude**. The
framework *explicitly rejected* the energy combination T²−T_Λ² (Milgrom's own hedge, relayed in
`RESPONSE_POSIT_DERIVATION_2026-06-09.md`: T²−T_Λ² gives the **wrong** MOND law). The kernel θ sits in
the inertia argument A = a_in + θ(y)·a_ex, and **A is linear in a** — so θ multiplies an AMPLITUDE, not
an energy. sympy results:
- Step 2 (DC equivalence-principle match of ΔT_actual vs ΔT_EFE to O(a_ex)): the **raw** physical weight
  of a static external field is **exactly 1** — it adds with unit weight (EP in the bath frame). θ(0)=2
  does NOT come out of a DC match.
- θ is the EFE-NORMALIZED ratio θ(0) = w(0)/w(1) = 1/w(corner). On the **amplitude** transfer the corner
  (−3 dB) point is 1/√2 → **θ(0) = √2**. On the **power** transfer it is 1/2 → θ(0) = 2 — but power = the
  T² reading the engine already discarded.

**Route B — the Luo 2026 construction (derive_luo_efe, NEW this session).** This is the framework's *own
strongest-support derivation* of its μ (`RESPONSE_POSIT_DERIVATION` calls it "the strongest single piece
of new support"): a_eff = √((a_N+a_bg)² − a_bg²). Here the dS background a_bg enters the **first moment**
additively (weight 1) and the **−a_bg² second-moment** subtraction is the spectral broadening of the
**background** (set by Λ alone). Adding a static external host field a_ex: by the equivalence principle a_ex
is a real proper acceleration of the *same* body, so it enters the **first moment** exactly like a_N
(sympy: inside-sqrt = (a_N+a_ex)² + 2a_bg(a_N+a_ex) → weight 1). It does **not** carry its own −a_ex²
floor (a classical coherent host has no horizon-scale quantum variance; the −()² channel is owned by Λ,
the single dS clock). So a_ex is **degree-1 → amplitude branch → √2**, independently of any "−3 dB filter"
picture.

**Why 2 is dispreferred (both-ways, honest):** θ(0)=2 requires EITHER (a) re-admitting the rejected
T²/energy reading, OR (b) a **second independent floor / memory clock** (a second −()² term, or a 2-pole
memory). The framework has a **single** Λ, a **single** dS clock 1/H_Λ — so neither is its default.

**The residual I am NOT hiding:** within the amplitude branch a real trade survives, set by the *order* of
the bath memory: single-pole amplitude → (θ(0)=√2, tail y⁻¹); two-pole amplitude → (θ(0)=2, tail y⁻²).
KMS alone does not fix the memory order. I also **corrected a genuine internal inconsistency** in the
banked FRONT-1 work: it asserted BOTH θ(0)=2 AND a y⁻² tail as forced, but those are jointly the
*double-pole* reading — √2 pairs with y⁻¹, 2 pairs with y⁻². The framework's single dS clock favors
single-pole → **√2**. **NET: √2 is the framework's self-consistent value; the [√2,2] interval is replaced
by an asymmetric pin at √2, with a named (memory-order) residual toward 2 — not a 50/50 interval.**

---

## 2. The kernel SHAPE from the dS Wightman function — FORM forced, CORNER postulated

The de Sitter / Unruh worldline correlator is W(u) = −(κ²/16π²)/sinh²(κ(u−iε)/2), κ = 2πT_eff (the
framework's engine, not an assumption; UV-checked to reduce to the flat vacuum −1/4π²u²). From it,
**first-principles (sympy-verified):**

- **[F] Lorentzian FORM is correlator-justified.** The large-separation envelope of 1/sinh² is
  **exponential** e^(−κ|u|) (coefficient 1/4 checked) ⇔ a **Lorentzian transfer** 1/(1+(ω/ω_c)²). The
  Part-F Lorentzian is no longer a bare ansatz — it is what the dS 1/sinh² memory gives. **Form-class
  forced** (exp memory ⇒ ≥ y⁻² decay).
- **[F] the bare dissipation is OHMIC.** χ″(ω) = ω/4π exactly — **κ cancels**, temperature-independent.
  The bare bath response is LOCAL/Markovian (χ(u) ~ d/du δ(u)); it carries no intrinsic corner. This
  sharpens the prior "analytic-in-ȧ" obstruction into a precise statement.
- **[NEGATIVE, honest] the dS Wightman function does NOT force the corner at y=1.** Two ways: (i) the bath's
  own scale is κ ~ H_Λ ~ 10⁻¹⁸ s⁻¹; every bound orbit has ω_in/κ ~ 10²–10⁵ (galaxy 269, wide binary
  2×10⁵, cluster dwarf 110, dSph 10³), so taken literally the bath gives θ≈1 everywhere (no relational
  effect). (ii) the exact fluctuation spectrum S_sym = (ω/4π)coth(πω/κ) **rises** at high ω (no cutoff)
  while the EFE weight must **fall** — opposite slopes. Landing the corner at ω_in REQUIRES the
  "internal orbit = averaging bandwidth" **postulate** (Milgrom-1994 Eq.55–57 licenses it only in the
  quasi-static limit; the general multi-frequency Eq.33 case is OBSTRUCTED, not closed).

**So the shape is HALF-forced:** the **Lorentzian FORM and the y⁻² tail are correlator-forced**; the
**y=1 corner LOCATION is the one remaining postulate.**

---

## 3. NET classification — PLAUSIBLE-with-forced-core (upgraded, not promoted to FORCED)

Ledger after this session:

| Ingredient of θ(y) | Status | By what |
|---|---|---|
| corner EXISTS (relational effect, monotone @ y≈1) | **FORCED** (existence) | bath + quasi-static localization |
| window (DC plateau + finite memory + θ(1)=1) | **FORCED** | EP + correlator |
| θ(0) **value** = √2 (not the interval) | **RESOLVED to √2** | excess-heat engine **and** Luo construction agree (degree-1) |
| shape FORM (Lorentzian, tail ≥ y⁻²) | **FORCED form-class** | dS 1/sinh² → exp memory → Lorentzian |
| corner LOCATION at y=1 (= ω_in) | **POSTULATED** | quasi-static window; Milgrom-1994 Eq.33 obstructed |
| within-residual: √2→2 (memory order) | open | KMS doesn't fix #poles |

**θ(y) does NOT reach full FORCED.** Value and form are now bath-derived (a real upgrade — the value moved
from a [√2,2] interval to a *selected* √2 by **two independent** framework-internal routes, and the shape
moved from "ansatz" to "correlator-justified Lorentzian"), **but the y=1 corner LOCATION remains a single
postulate**, and a memory-order residual (√2→2) survives. **Classification: PLAUSIBLE-with-forced-core
(corner-existence + window + value + form-class forced; corner-location + memory-order = modeling).**

**Be ruthless / no faked promotion:** I will not call this FORCED. The honest gain is real and is *the
session's biggest theory advance*: θ(y) went from a **free function** to a **bath-constrained kernel** with
a *selected* DC value √2 and a *derived* Lorentzian form, the open piece narrowed to exactly ONE postulate
(corner = ω_in) plus a named memory-order residual. That is a free-function → one-postulate compression. It
does not need inflating to be the headline.

---

## 4. SHARPEST dwarf/cluster prediction for v2 (DOI 20949773) — at the SELECTED θ(0)=√2

Kernel θ(y) = θ₀/(1+(θ₀−1)y²), **θ₀ = √2 (now selected)**, θ(1)=1. Framework's own μ_fw, a₀=9.36×10⁻¹¹
(golden check μ_fw(1)=0.61803=1/φ). Canonical plunging member a_in≈0.3a₀, a_ex≈2a₀; y = ω_ex/ω_in =
infall phase:

- **Realistic plunging band y = 0.35–0.50: member-σ boost = +12 to +14%** (deeper dSph footing
  a_in=0.1a₀, a_ex=1.5a₀: +12 to +15%). Monotone-decreasing in y (Lorentzian, no interior peak).
- **EXACT zero-crossing at y = 1** (external freq = internal freq).
- **SUPPRESSION for y > 1:** −8% at y=1.3, −12% at y=1.5, −23% at y=2.
- **Tail y⁻²** (Lorentzian, correlator-forced).
- **Residual band toward 2-pole (θ₀=2):** the SAME y-band would give +23 to +30% — so the **+12–14% is
  the framework's preferred (single-clock) number; +12 to +30% is the full residual envelope** if the
  memory turns out 2-pole. Report +12–14% as the prediction, with the upper envelope flagged.

**Robust to everything: the SIGN, the exact y=1 zero-crossing, and monotone-decrease.** These are
**MG-impossible** (modified-gravity EFE depends only on the momentary a_ex → θ≡1 identically → zero phase
dependence) and **non-a₀-degenerate**. The companion non-adiabatic *relational σ-spread* (member σ
correlates with infall phase at matched radius; MG = 0 for any a₀) remains the MG-impossible distinctive
signature.

**One-line v2 claim:** *A plunging dwarf/cluster member's internal velocity dispersion is boosted ~+12–14%
in the realistic infall band, crosses exactly zero when its orbital frequency matches its internal
frequency, and is suppressed beyond — a monotone, MG-impossible, a₀-independent infall-phase signature.*

---

## 5. Quarantine (held) + what to tell Carl

**Quarantine:** pinning θ(0)=√2 and the Lorentzian form does **NOT** derive a₀ — θ lives inside the inertia
argument A; a₀ sits outside in μ_fw[A/a₀]. **Z remains a posit; SM walled.** This is a kernel-shape result,
not a coefficient derivation. (Note: the √2-vs-2 *here* is the θ(0) EFE weight — a DIFFERENT "factor of two"
from the Z=2√(8π/3) coefficient question in `THE_FACTOR_OF_TWO`, which stays open and empirically moot.)

**Straight to Carl:** √2-vs-2 **resolved to √2** — and it resolved on *your* terms (the linear excess-heat
engine you already chose to get the right deep-MOND law, plus the Luo additive-acceleration derivation you
banked as your strongest support — *both* put the external field in at weight 1, the amplitude branch). The
dS Wightman function **does** force the Lorentzian shape and the y⁻² tail from 1/sinh² → exponential memory,
so the kernel form is no longer an ansatz. The one thing the bath does **not** hand you is *where* the
corner sits (y=1); that still rides on the "internal orbit = the averaging window" postulate (Milgrom-1994
licenses it quasi-statically; the general case is obstructed). So θ(y) is now
**PLAUSIBLE-with-forced-core, not fully FORCED** — and I'm not going to dress it as FORCED. The real win is
that θ went from a free function to a bath-constrained kernel with a *selected* DC value and a *derived*
shape, with the open part squeezed down to a single named postulate. **No doors closed** — the open avenue
is concrete: derive the corner=ω_in localization from Milgrom-1994 Eq.33 (the general multi-frequency case),
currently obstructed; and the Hu–Verdaguer influence-functional that would turn ΔT-as-inertia from posit
into theorem is still unrun.

**Is v2 warranted now?** **Yes — for the dwarf σ paper (DOI 20949773), the kernel section.** The prediction
is now sharper than the banked work: a *single selected* θ(0)=√2 (not a [√2,2] interval), a
*correlator-derived* Lorentzian form, a definite **+12–14%** plunging-band boost, the exact y=1
zero-crossing, the y⁻² tail, and a clearly-bounded upper envelope (+30%) tied to the lone memory-order
residual. State the corner-location postulate explicitly in v2; do **not** claim FORCED. The MG-impossible,
a₀-independent character of the signature is the load-bearing selling point — and it survives the whole
residual band.
