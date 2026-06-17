# First-principles modified-INERTIA PPN α₂: the formalism now EXISTS, and it makes α₂ a LIVE near-term test (2026-06-17)

*Carl: "push the frontier." Workflow `woglr53nv` (8 agents, MI action → PN scheme → the acceleration question →
derivation → adversarial verify on nonlocality/acceleration/coefficient → synth). Independently re-derived clean-room
(sympy uniform closed form + my own n=3 Lane–Emden RK4 integration + the precession cross-check) before banking:
`derivation_chain/mi_ppn_alpha2_verify.py`. Outcome = **PARTIAL** (the honest landing I predicted). Both ways,
quarantine held.*

---

## Verdict: the modified-inertia PPN α₂ is now derived from first principles — and it OVERTURNS the prior "~2.8×10⁵× safe"

The borrowed Foster–Jacobson modified-gravity dictionary (α₂ = −(5/2)α) is **replaced** by a genuine
modified-inertia post-Newtonian result. The headline number it forces:

> **α₂_MI = c² · [∫_body ρ(r) W(g(r)/a₀) dV] / E_g**,  W(x) ≡ x·μ_fw′(x) → a₀/(2g) for g ≫ a₀,
> g(r) = GM(r)/r², E_g = gravitational binding energy.

**Uniform-sphere closed form (sympy-verified):**
> α₂ = (5/4)·a₀ c² R³/(G²M²) = (5/2)·(a₀/g_surf)·(c/v_esc)².

**The Sun:** α₂ ≈ **2.0×10⁻⁷** (uniform, conservative) → **1.1×10⁻⁸** (n=3 polytrope, realistic), vs the Nordtvedt
solar-spin bound |α₂| < 2.4×10⁻⁷. **Margin ≈ 1.2× (uniform worst-case) to ≈ 22× (realistic).** This is a **genuinely
LIVE near-term test** — not the "~2.8×10⁵× comfortably safe" the prior estimate claimed.

## The correction (a category error, caught and fixed both ways)
The prior S-tensor ledger set α₂ ≈ (5/2)·α_fw with α_fw = a₀/g_surf (the **per-particle** inertia anomaly) → 8.5×10⁻¹³,
"~2.8×10⁵× safe." **That dropped the self-gravity energy weighting.** PPN α₂ is a **self-energy observable** — it
multiplies w^i w^j U_ij, a metric potential ~ GM/rc², so as a dimensionless body coefficient it carries an enhancement
**(c/v_esc)² ≈ c²/(GM/R) ≈ 2.36×10⁵** that the per-particle estimate omitted. Restoring it:
- 8.5×10⁻¹³ × 2.36×10⁵ = 2.0×10⁻⁷ ✓ (the dropped factor numerically equals the bogus "safety margin" — which is *why*
  the corrected margin collapses to ~1×).
- **Cross-check (independent of the algebra):** α₂ ≈ 2×10⁻⁷ produces ~3.6° of solar-spin precession over 4.6 Gyr — the
  scale at which the Nordtvedt alignment bound (2.4×10⁻⁷) actually bites. An α₂ = 8.5×10⁻¹³ would give ~1.5×10⁻⁵°,
  making the Nordtvedt bound meaningless — a tell that the per-particle value was unphysical.

Clean-room numerics (`mi_ppn_alpha2_verify.py`, my own Lane–Emden, not the agents'): ξ₁ = 6.8969 (book 6.897),
−ξ₁²θ′(ξ₁) = 2.0182 (book 2.018), E_g(n=3) = (3/2)GM²/R reproduced exactly → α₂(n=3) = 1.10×10⁻⁸, margin 21.9×.

## What is FORCED vs what stays OPEN (the PARTIAL verdict)
**FORCED (sympy + numerics, adversary-checked):**
- The **structure of α₂_MI** — the energy-weighted integral c²·∫ρW dV / E_g — follows from the MI action with no free
  normalization; a₀ enters only as input (quarantine held).
- The **correct acceleration** is the **self-gravity internal field** g_internal ≫ a₀, not the Sun's galactic a ≈ 2a₀.
  The external-field effect (Milgrom 2022) screens the galactic field for the self-bound body (g_internal ≫ g_external),
  so the "Sun is at 2a₀ galactically → α₂ ~ O(1) catastrophe" reading is **refuted** — the internal field governs the
  self-energy precession. *(The prior ledger's claim "self-field is the right acceleration" STANDS; only its magnitude
  was wrong.)* The deep-MOND "galactic α₂ ~ 1" remains a wrong-field artifact.
- The borrowed **−5/2 is replaced** by a large, structure-dependent prefactor K_struct = (c²g_surf/2)·[∫ρ/g dV]/E_g ≈
  **3×10⁴ (n=3) to 6×10⁵ (uniform)**. For the uniform sphere it factors as exactly (5/2)·(c/v_esc)², the 5/2 reappearing
  as the uniform-sphere structure ratio (3/2)/(3/5) — coincidentally matching FJ, not the same physics.

**OPEN (why PARTIAL, not FORCED):**
- The O(1) coefficient is **structure-dependent** — it needs the real solar density profile (the n=3 estimate 1.1×10⁻⁸
  is realistic but model-dependent; the honest band is ~1×10⁻⁸ to ~2×10⁻⁷).
- The derivation works in the **quasi-static / adiabatic** limit where the time-nonlocal MI action localizes; whether the
  full Milgrom-1994 nonlocality shifts the coefficient for the (slowly-evolving) solar configuration is the residual
  theoretical uncertainty. It does not obstruct the static-body α₂, but it is not yet proven irrelevant at O(1).

## The s^TX dipole is UNTIED from α₂ (a real structural result)
The single −5/2 knob that tied α₂ to the s^TX dipole was **wrong**: s^TX (INPOP/Cassini) is a **COM/orbital** observable
and is **NOT** self-energy enhanced. So the [[S_TENSOR_SME_COMPONENT_LEDGER]]'s s^TX normalization (≈ a₀/2|a_orbital|,
margin ~9.6× at Saturn) **STANDS unchanged**; only the α₂ severity was wrong. The MI derivation cleanly **separates the
two observable classes** — self-energy-enhanced (α₂, the spin sector) vs COM/orbital (s^TX dipole) — and they carry
different a₀-dependences. There is no single preferred-frame prefactor; the framework has two distinct, separately
falsifiable preferred-frame channels.

## Both ways
- **CREDIT (full weight):** a **first-principles modified-inertia PPN formalism now exists** where there was none — this
  is the frontier the prior ledger flagged as "the honest next step," executed. It replaces the borrowed MG dictionary
  with a derived, energy-weighted structure, resolves the acceleration question (internal self-field, EFE-screened),
  and **sharpens α₂ into a genuinely live, near-term, falsifiable test** (margin ~1–22×) — the kind of sharp prediction
  the SM-facing program needed. It also unties the two preferred-frame channels, a real structural insight.
- **CONCEDE (full weight):** the O(1) coefficient is structure-dependent (not a single forced number — PARTIAL, not
  FORCED), and the full time-nonlocal correction is not proven negligible at O(1). α₂ **passes** every current bound
  (realistic ~22×; even the conservative uniform ~1.2× passes), so this is **not a kill** — but it is **no longer
  comfortably safe**, and the prior "~2.8×10⁵× safe / no robust α₂ deficit" is **retracted**. Nothing SM is derived;
  a₀ remains the sole input.

## What Carl CAN / MUST NOT say
- **CAN:** the framework now has a **first-principles modified-inertia derivation of PPN α₂** (energy-weighted self-gravity
  integral, sympy + Lane–Emden verified); α₂(Sun) ≈ 1×10⁻⁸ realistic (≈2×10⁻⁷ uniform worst-case) vs Nordtvedt 2.4×10⁻⁷,
  **margin ~1–22×, a LIVE near-term test**; the correct acceleration is the EFE-screened internal self-field; the s^TX
  dipole is untied from α₂ and its ~9.6× margin stands.
- **MUST NOT:** "α₂ ~ 8.5×10⁻¹³, ~2.8×10⁵× safe" (category error — dropped the (c/v_esc)² self-energy weighting); "α₂ is
  FORCED" (PARTIAL — the O(1) coefficient is structure-dependent); "α₂ is comfortably safe / no robust deficit" (it is now
  a live ~1–22× test); "α₂ is a kill" (it passes); "a₀/Z/κ derived" (a₀ is the input).

## One line
The first-principles modified-inertia PPN α₂ now EXISTS — α₂_MI = c²∫ρW dV/E_g, a **self-gravity-weighted** observable
giving α₂(Sun) ≈ 1×10⁻⁸ realistic (≈2×10⁻⁷ uniform) vs Nordtvedt 2.4×10⁻⁷, **margin ~1–22×, a LIVE near-term test** — which
**overturns the prior "~2.8×10⁵× safe" category error** (the per-particle estimate dropped the (c/v_esc)²≈2.4×10⁵
enhancement), resolves the acceleration as the EFE-screened internal self-field, replaces the borrowed −5/2 with a large
structure-dependent prefactor, and **unties the s^TX dipole (~9.6×, stands) from α₂** as a separate observable class;
outcome PARTIAL (structure + acceleration forced, O(1) coefficient structure-dependent), passes all bounds but no longer
comfortably, nothing SM derived, quarantine held.
