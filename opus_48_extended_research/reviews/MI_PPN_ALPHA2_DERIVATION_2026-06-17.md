# First-principles modified-INERTIA PPN α₂: the formalism EXISTS, and α₂ ~ a0/g ~ 10⁻¹³ is COMFORTABLY SAFE (2026-06-17)

*Carl: "push the frontier." Workflow `woglr53nv` (8 agents: MI action → PN scheme → the acceleration question →
derivation → adversarial verify → synth). **This file was first written on an INTERMEDIATE result (the "D" derive
agent's self-energy enhancement) that the workflow's own VERIFY_COEFF + SYNTH then OVERTURNED; it is now corrected to the
verified final answer.** Clean-room re-verified: `derivation_chain/mi_ppn_alpha2_verify.py` (Shao–Wex Eq.5 linearity +
rigid-body inertia-tensor toy + the M-vs-E_g normalization). Outcome PARTIAL. Both ways, quarantine held.*

---

## Verdict: the MI PPN α₂ formalism now exists; α₂_MI ~ a few × 10⁻¹³, ~10⁶× under Nordtvedt — SAFE

A first-principles modified-inertia derivation of the PPN preferred-frame parameter α₂ now exists, replacing the borrowed
Foster–Jacobson modified-gravity dictionary. The method: read α₂ off by matching the **boost-induced inertia-tensor
anisotropy** of a self-gravitating body to the linear Nordtvedt/Shao–Wex spin-precession rate.

> **δI/I = (1 − μ_fw)(g_internal) · (w/c)² · O(1)**   matched to   **Ω_prec = −(α₂/2)(2π/P)(w/c)² cos ψ** (Shao–Wex
> arXiv:1307.2552 Eq.5)  ⟹  **α₂_MI = O(1)·(1 − μ_fw)(g_internal) ~ a₀/g_internal.**

**The Sun:** α₂_MI ~ a few × 10⁻¹³ (order a₀/g_internal; ~1.7×10⁻¹³ at the surface g=274, smaller in the deep interior
g~10⁴), vs the Nordtvedt solar-spin bound |α₂| < 2.4×10⁻⁷ → **margin ~10⁶×. COMFORTABLY SAFE — not a live test.**

## The correction record (both ways, on the record)
Two readings were on the table; the verification settles it:
- **The original ledger** had α₂ ~ 8.5×10⁻¹³, "~2.8×10⁵× safe." **Right order, right safety** (it was the per-particle
  inertia anomaly (5/2)(a₀/g_surf), which IS the correct dimensionless α₂ up to an O(1) factor).
- **The intermediate D agent** (relayed and briefly banked) claimed a **self-energy enhancement** α₂ = c²∫ρW dV/E_g =
  (5/4)a₀c²R³/(G²M²) ~ 10⁻⁸–10⁻⁷, a "LIVE ~1–22× Nordtvedt test," calling the prior a "category error." **This was
  itself the error — a c²/(GM/R) ≈ 4.7×10⁵ DOUBLE-COUNT.** PPN α₂ is a *dimensionless* theory constant and the precession
  rate is *strictly linear* in it (Shao–Wex Eq.5, d²Ω/dα₂² = 0, no E_g — verified). The MI effect is an inertia-tensor
  anisotropy δI/I, a **ratio normalized by the moment of inertia I ~ MR² (i.e. by M)**, *not* by E_g/c². D imported the
  c²/E_g from the metric-PPN template (where α₂ multiplies the potential U_ij and genuinely carries self-energy), but a
  Route-E modified-inertia theory has a **standard-GR metric and no U_ij coupling** — self-gravity does not amplify a
  moment-of-inertia ratio by 1/U.

**Clean-room verification (`mi_ppn_alpha2_verify.py`):** (A) Eq.5 is linear in α₂, no E_g. (B) rigid-body toy:
δI/I = (1−μ)β²/5, a pure ratio, ⟹ α₂ = (2/5)(1−μ) = O(1)·(1−μ). (C) ∫ρW/M = 3.5×10⁻¹⁴ (correct) vs c²∫ρW/E_g = 1.1×10⁻⁸
(D's), ratio = 3.14×10⁵ = **Mc²/E_g exactly** — the double-count pinned. (D) margin ~7×10⁶×.

## What is FORCED vs what stays OPEN (PARTIAL)
**FORCED (both ways, over-determined):**
- The **order a₀/g_internal** and the **absence of any c²/(GM/R) self-energy enhancement** (PPN α₂ dimensionless;
  precession linear; δI/I normalized by M).
- The **correct acceleration is the Sun's INTERNAL binding g_internal ≫ a₀** (surface x = g/a₀ ~ 2.9×10¹², deep
  Newtonian tail), NOT the COM galactic field a_gal ~ 2a₀ and NOT the heliocentric 5.9×10⁻³. Forced four ways: (1) the
  observable is the internal pairwise self-energy sum (Shao–Wex Eq.4) — the COM coupling carries no spin torque; (2) a_gal
  is common to every constituent and cancels by the COM/equivalence-principle theorem (enters μ_fw only at
  a_gal/g_internal ~ 7.7×10⁻¹³); (3) the Route-E action is per-worldline; (4) **pulsar reductio** — solitary millisecond
  pulsars in the *same* ~2a₀ galactic field bound |α̂₂| < 1.6×10⁻⁹, which the galactic reading (1−μ(2.24) ~ 0.2) would
  violate by ~10⁸×, so existing data already kills the galactic reading. The "Sun-at-2a₀" subtlety dissolves via the MI
  composite-body decoupling (Milgrom 2022): the galactic ~2a₀ governs the Sun's **COM trajectory** (the real
  framework-distinctive galactic effect), while the internal binding governs the **self-energy spin observable** —
  different accelerations for different observables. The "galactic α₂ ~ 1 catastrophe" is a **wrong-band artifact.**
- The high-acceleration tail 1 − μ_fw = a₀/(2|a|) − … (coeff 1, sympy); α_fw = 2(1−μ_fw) → a₀/|a| (coeff 1).
- The **s^TX boost dipole (~9.6× vs INPOP/Cassini)** is a separate **COM/orbital** observable, **untied from α₂ and
  unchanged** — the SME ledger's binding test is intact.
- α₃ = 0 identically (semiconservative action-derived theory). Quarantine: a₀ is the input throughout.

**OPEN (why PARTIAL, not FORCED):**
- The exact **O(1) geometric/structure prefactor** multiplying (1−μ)(g) — the ratio of the (1−μ)-weighted
  inertia-anisotropy integral to the precession normalization over the real solar density profile — is structure-
  dependent, not a single closed-form number. (It does not change the ~10⁻¹³ order: saturating Nordtvedt would need an
  O(10⁶) prefactor; any plausible O(1)–O(10³) structure factor stays >10³× safe.)
- The multi-internal-band θ(ω_i/ω_j) coupling (Milgrom 2022) can shift the O(1) coefficient (bounded, order-preserving).
- A fully covariant Route-E PN derivation from the Galley in-in kernel without the quasi-static reduction.

## The nonlocality (Milgrom-1994): PERMITS here, OBSTRUCTS the general case
The time-nonlocal MI action localizes EXACTLY to the algebraic μ_fw(|a|/a₀) on a single-frequency/adiabatic trajectory
(Milgrom 1994 Eqs.55–57). The entire solar interior sits at x = g/a₀ ~ 10¹²–10¹³ on **one smooth analytic branch**, never
spanning the x ~ 1 Newtonian↔deep-MOND transition where the strong no-go (Eq.33) bites — so the quasi-static α₂ is
**licensed**, not a forbidden artifact. The general multi-incommensurate-frequency MI PN expansion IS genuinely obstructed
by Eq.33 (no single local Lagrangian across regimes). Crucially, the nonlocality is **not** what caps α₂ at ~10⁻¹³ —
that cap is the dimensionless-α₂/linear-precession structure, independent of nonlocality.

## Both ways
- **CREDIT:** the MI PPN α₂ formalism now EXISTS and is first-principles (inertia-tensor anisotropy matched to the linear
  precession rate), replacing the borrowed −5/2; the correct internal-self-gravity acceleration and the a₀/g order are
  **forced and over-determined** (observable structure + COM cancellation + per-worldline action + pulsar reductio); the
  result is **robustly safe** (~10⁶×, prefactor-insensitive); s^TX (~9.6×) stays the live SME test, untied and intact.
- **CONCEDE:** PARTIAL — the O(1) prefactor is structure-dependent and un-derived; the general multi-frequency case is
  obstructed by the Milgrom-1994 nonlocality; nothing about a₀/Z/κ/SM is derived (a₀ is the input). And the honesty note:
  the intermediate "LIVE ~1–22×" self-energy reading (briefly banked) was a double-count — the correct α₂ is **safe**, so
  α₂ is **NOT a near-term falsifiable test**; the live preferred-frame constraint remains the s^TX dipole.

## What Carl CAN / MUST NOT say
- **CAN:** the framework now has a **first-principles modified-inertia derivation of PPN α₂** (inertia-tensor anisotropy
  → linear Nordtvedt precession), giving α₂_MI ~ a few × 10⁻¹³ (order a₀/g_internal), **~10⁶× under Nordtvedt =
  comfortably safe**; the correct acceleration (internal self-gravity, galactic ~2a₀ empirically excluded by the
  solitary-MSP reductio) is forced; the s^TX dipole (~9.6×) is the live SME test, untied from α₂; outcome PARTIAL.
- **MUST NOT:** "α₂ ~ 10⁻⁸, LIVE ~1–22× Nordtvedt test" (D's self-energy double-count — the correct value is ~10⁻¹³,
  ~10⁶× safe); "α₂ is self-energy-enhanced by (c/v_esc)²" (spurious metric-PPN import; MI has no U_ij coupling); "the prior
  8.5×10⁻¹³ was a category error that dropped the self-energy weighting" (FALSE — that order was correct); "α₂ is FORCED to
  a clean number" (PARTIAL — O(1) prefactor open); "α₂ is OBSTRUCTED with no value" (the quasi-static sector is
  computable); "α₂ is a near-term falsifiable test" (it is ~10⁶× safe); "a₀/Z/κ derived" (a₀ is the input).

## One line
The modified-inertia PPN α₂ formalism now EXISTS (inertia-tensor anisotropy (1−μ)(g)(w/c)² matched to the **linear**
Nordtvedt/Shao–Wex precession), giving **α₂_MI ~ a few × 10⁻¹³ (order a₀/g_internal), ~10⁶× under the 2.4×10⁻⁷ bound =
comfortably SAFE** — with the correct internal-self-gravity acceleration FORCED (galactic ~2a₀ excluded by the
solitary-MSP reductio) and only the O(1) structure prefactor open (PARTIAL); this **overturns the intermediate
self-energy-enhanced "~10⁻⁸, LIVE 1–22×" reading as a c²/(GM/R) double-count** (PPN α₂ is dimensionless; MI has no metric
U_ij coupling — verified by the toy and Eq.5 linearity), confirming the prior ~10⁻¹³ order; the s^TX ~9.6× dipole stays
the live SME test, untied and intact, and a₀ is the input throughout.
