# Koide C-path: Does any Zimmerman-framework number FIX a Sumino free parameter so the potential minimum lands at r=√2 (Koide) WITHOUT inputting 2/3?

**Date:** 2026-06-25
**Verdict:** **NO-FIX-DEAD** (with a CIRCULAR-DEAD fallback on the lone numerical collision)
**Question closed:** the Koide-*derivation* question is now exhausted on BOTH the measure route (closed prior) and the mechanism-parameter route (closed here).

---

## 0. Anti-circularity guard (verified first, mpmath dps=40)

`Q = 1/3 + r²/6`, phase-independent. At `r=√2`: `Q = 1/3 + 2/6 = 2/3` **exactly** (verified to 35 digits).
Therefore **"tune any parameter to give r=√2" ⟺ "assume Q=2/3."** A framework "fix" counts as a real
derivation ONLY if a framework number fixes a Sumino parameter via a relation derived WITHOUT reference to
2/3 or √2, and the minimum THEN happens to land at r=√2. Every step below is flagged for whether 2/3 or √2
would have to be known in advance.

Framework numbers in play (dps=40):
- `Z = √(32π/3) = 5.78881003646…`
- kernel `(3/8π)^(1/4) = √(2/Z) = 0.58778750367…`  (so `kernel⁴ = 3/(8π) = 0.11936620732…`)
- dS scale: `T_dS = 2cH_Λ`, `a₀ = 9.36e-11 m/s²`, `ρ_DE` — all **cosmological IR** (~10⁻³³ eV).

---

## 1. Sumino's actual structure (from arXiv:0903.3640 full text + 0812.2090 full text)

Sumino's construction has **two logically separate ingredients**. Koide = 2/3 only emerges from BOTH:

### (I) The QED-cancellation relation  α = ¼ α_F  (0812.2090 eq.19, 0903.3640 eq.17)
This keeps Koide *scale-stable* (cancels the 0.1% QED running of eq.6/2). The factor **¼ is PURE GROUP
THEORY**, not a free parameter:
- QED `m log m²` coefficient: `−3α/(4π)` (eq.6).
- Family `m log m²` coefficient: `+(3α_F/8π)·(½)` since `log v_i² = ½ log m_i²` (eq.13/15).
- Cancellation ⟹ `α = α_F·(3/8·½)/(3/4) = α_F/4`. **Verified: ratio = 0.25 exactly.**

The `¼` is dictated by the conjugate-representation assignment `ψ_L:(3,1)`, `e_R:(3̄,−1)` and the breaking
pattern `U(3)→U(2)→U(1)→nothing` (0903.3640 §3, features 1–4). **There is NO free number here for a
framework to fix.** Sumino then *explains* `α_F ≈ 4α(m_τ)` by `SU(2)_L`-unification at 10²–10³ TeV
(`sin²θ_W ≈ ¼`) — a particle-physics UV coincidence, not a tunable knob.

### (II) The Koide vacuum from the X-field  (0903.3640 eqs.27–31)
Koide itself = `(Φ⁰)² = ΦᵃΦᵃ` (eq.29 = the 45° / r=√2 condition) follows from combining:
- `⟨X^{αβ}⟩ = diag(−1,+1,…,+1)` (one −1 at the U(1) slot α=0, eight +1 at the SU(3) slots) — eq.27;
- `Φ^β X^{βγ} Φ^γ = 0` (the ε_K term minimum) — eq.28.
Plug 27 into 28: `−|Φ⁰|² + Σ_a|Φᵃ|² = 0 ⟹ |Φ⁰|² = Σ_a|Φᵃ|²` = eq.29 = Koide.

**The Koide condition is therefore a DISCRETE datum** — the signature `(−1,+1⁸)` of the SU(9)×U(1)→U(3)×O(3)
breaking — i.e. the 1-vs-8 count of the 9-dimensional T^α basis (T⁰ the U(1) generator, T^{1..8} the SU(3)
generators). The 45° angle = `cos⁻¹(1/√2)` = the geometry of the coset, **not a continuous ratio at all.**

### The genuinely-free continuous parameters
The hierarchy `m̃², λ, ε_K, h̃₁ ≫ g₂ ≫ g₁` (eqs.30–31), sizes ~**10⁻³–10⁻⁴**, where `g₁,g₂` are the
**SU(9)×U(1)-violating** terms `tr(Φ†ΦΦ†Φ)`, `tr(ΦΦᵀΦ*Φ†)`. These control:
- (a) how *cleanly* Koide holds (suppressing g₁,g₂ keeps the vacuum on the cone), and
- (b) **WHERE on the Koide cone the spectrum sits** — i.e. `m_e/m_τ`, `m_μ/m_τ` (g₂ fixes the point;
  Sumino: minimizing g₂ alone gives `m_e/m_τ` ~15% off, `m_μ/m_τ` ~1.5% off).

So the free continuous knobs set the **point on the cone (the mass ratios), NOT whether Koide holds.**
Koide-holds = the discrete X-signature.

---

## 2. Does ANY framework number touch ANY Sumino parameter? (mpmath dps=40)

| Sumino parameter | What it is | Framework number that could fix it | Result |
|---|---|---|---|
| `¼` in α=¼α_F | pure group theory (1-vs-8 + conjugate reps) | n/a — not a free parameter | **No knob to fix.** No framework number = ¼; closest is `1/Z·something`, all off (Z/4=1.45, kernel²=0.345, 1/Z=0.173 — none near 0.25 or 4). |
| α_F (value) | set by SU(2)_L unification at 10²–10³ TeV (`sin²θ_W≈¼`) | dimensionful: T_dS, a₀, ρ_DE | **48-order gap.** Framework scale ~10⁻³³ eV (Hubble IR); Sumino scale ~10¹⁴–10¹⁵ eV (UV). No dimensionful bridge. |
| Koide-holds | discrete `⟨X⟩=(−1,+1⁸)` signature = SU(9)/[U(3)×O(3)] geometry | a continuous framework number | **Category mismatch.** Koide-holds is a Z₂-type discrete sign choice (which slot is −1), not a continuous ratio a number could land. |
| hierarchy g₁,g₂,h̃₁,ε_K (~10⁻³–10⁻⁴) | the SU(9)×U(1)-violating tilt/cone-point couplings | Z, kernel, 1/Z, 1/Z², kernel⁴… | **Wrong order.** Smallest natural framework number `1/Z²=0.0298` (~10⁻²); `1/Z³=0.0052`. None reaches 10⁻³–10⁻⁴ without an arbitrary power chosen to hit it. And these set the MASS RATIOS, not Koide. |
| the spectrum point (m_e/m_τ, m_μ/m_τ) | g₂-minimum on the cone | any framework number | Even if a framework number set this, it would fix the *ratios*, NOT reproduce r=√2 — Koide is already imposed by (I)+(II) upstream. |

### The one numerical collision (stress-tested to break)
Framework `kernel⁴ = 3/(8π) = 0.11936620732…` **equals** the numeric part of Sumino's family-correction
prefactor `3α_F/(8π)` (eq.15). Identical numbers. **But it is a coincidence-mining collision, not a bridge:**
1. **Unrelated origins.** Framework `3/(8π)`: from `ρ_DE = Λc²/(8πG)` (Einstein 8πG) and Friedmann `3H²` — a
   *gravitational/cosmological* normalization. Sumino `3/(8π)`: a *1-loop gauge self-energy* coefficient (the 3
   is the QED anomalous-dimension `3/4`×group factor; the 8π is loop phase space, **not** Einstein gravity). To
   "use" the match you must equate Einstein-8πG with a loop-8π — no relation.
2. **It cancels.** Sumino's `3α_F/(8π)` is the coefficient that is **deliberately set to cancel** against QED
   via α=¼α_F. It does **not survive into any Koide observable** — it is on its way to zero by design. A number
   that is constructed to vanish cannot be the carrier of a derivation of 2/3.
3. **Circular if forced.** The only way to make `kernel` reproduce r=√2 through this slot is to *choose* the
   mapping because you already know it must give Koide → the 171st circular re-labeling.

`sin²θ_W ≈ ¼` (Sumino's anchor for α_F) also has no framework match (`kernel²=0.345 ≠ 0.231`).

---

## 3. Verdict

**NO-FIX-DEAD.** No framework number (Z, the kernel `(3/8π)^(1/4)`, T_dS=2cH_Λ, a₀, ρ_DE) fixes any of
Sumino's free parameters in a way that lands the potential minimum at r=√2:

- The **¼** that stabilizes Koide is **pure group theory** (1-vs-8 count + conjugate reps) — no free knob exists
  for a framework to touch.
- **Koide-holds is a DISCRETE datum** — the `(−1,+1⁸)` X-signature of SU(9)×U(1)→U(3)×O(3) — a category a
  continuous framework number cannot supply.
- The genuinely-free continuous parameters (hierarchies ~10⁻³–10⁻⁴; g₂ cone-point) sit at the **wrong order**
  for every framework number and, crucially, set the **mass RATIOS, not Koide** — so even a hypothetical match
  would not be a derivation of 2/3.
- The **dimensionful** hook (α_F via 10²–10³ TeV unification) is **~48 orders** above any framework scale.
- The lone numerical collision (`3/8π`) is an **unrelated-physics coincidence on a coefficient that cancels** →
  using it is **CIRCULAR-DEAD**.

This matches the honest prior exactly: the SM Yukawa/family sector is **kernel-free**. There is no forced kernel
in Sumino's family-gauge construction for a framework number to grab; the framework's only surviving SM bridge
remains the SME/Lorentz one, which **induces, never derives**.

## 4. Bottom line (one line)

**Sumino's Koide = a discrete SU(9)→U(3)×O(3) X-signature plus a group-theoretic ¼ plus ~10⁻³ hierarchy knobs that set the mass RATIOS — none of which any Zimmerman number fixes (wrong category, wrong order, 48-order scale gap), and the one 3/8π collision is an unrelated cancelling coefficient → the Koide-derivation question is now COMPLETELY exhausted: measure-route (closed) + mechanism-parameter-route (closed here), both NO-FIX/CIRCULAR. The framework still only RE-LABELS Q=2/3; it does not derive it.**
