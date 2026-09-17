# YM00 — THE YANG-MILLS GAP CAMPAIGN (deepseek lane, 2026-09-17)

Folder: `deepseek_push/yang_mills_gap/`. Task: attack the Yang-Mills mass gap
from the framework's first principles, certify every algebraic rung in Lean,
and register the honest verdict — win, loss, or scope — in print BEFORE the
numbers land.

## THE QUESTION, RESTATED FOR THIS FRAMEWORK

The Clay Yang-Mills problem asks for a proof that the SU(3)-class quantum
Hamiltonian's spectrum has a gap above the vacuum. This framework owns no
QCD sector (TOE_STATUS.md: "LACKS -- the electroweak/QCD sector"), so the
honest first-principles question is the framework-native one:

> **YM0: can the framework's own action generate a gapped vector sector, and
> if so, what exactly is the gap?**

The committed record entering this campaign:

- **B8 / E02 / F03 / G081** -- the equilibrium sector's excitation branch is a
  GAUGELESS Goldstone: ω(k) = c_s k, gap EXACTLY ZERO (ω² = 0 EXACT at k = 0,
  cap-invariant). The gaplessness is certified arithmetic on the committed
  record.
- **G054 (glm53_push)** -- the frozen cosmological completion is registered
  with "No background vector, no Stueckelberg, no khronon, no Einstein-
  aether" -- an EXPLICIT background vector is killed.
- **L5 (THE_THEORY.md)** -- the action: L = Λ⁴ f(K), K = −(1/2)(∂φ)²/Λ⁴,
  shift-symmetric (φ → φ + c), no potential V(φ), α₁ = α₂ = 0 by structure.
- **L2 / G031 / G155** -- the kernel: f'(K) = μ₂(u), u = |∂φ|/Λ²,
  μ₂(u) = u(2+u)/(1+u)², the SPARC-selected interpolant (n = 2).
- **L1** -- one constant: ρ_Λ = 4a0²/Gc², Λ⁴ = ρc², Λ ≈ 1.0–2.3 meV.
- **L10** -- one cold species, m ∈ [3.3, 100] keV; the Noether-charge dust.

## THE DOOR (pre-registered)

The B8 branch is gapless because the shift symmetry is GLOBAL. The only
structure-preserving way this action can produce a gapped gauge field is to
LOCALIZE that shift (D_μ φ = ∂_μ φ − m A_μ, the minimal Stueckelberg
gauging): the Goldstone is eaten, the vector becomes massive, and — this is
the derivation to be executed — the mass is set by the framework's OWN
interpolant:

    m_A² = μ₂(u)·m²        (the mass formula, to be derived, not assumed)

If this identity falls out of L5's action exactly, the framework's answer to
"where does the mass gap come from" is: the gap is the eaten Goldstone of the
a0-sector, it is EXACTLY zero where the phantom is absent (μ₂ = 0 at u = 0:
vacuum, the Solar System, beyond the EFE cap), it follows the μ₂-profile
inside the phantom, and it is a needed consequence of localizing the shift —
no non-perturbative miracle required.

## KILL CONDITIONS (pre-registered; any one fires → the door dies)

- **K1 (the mass formula):** if the exact quadratic expansion of Λ⁴f(K) with
  Dφ = ∂φ − mA at a background gradient v does NOT yield m_A² = μ₂(u)·m²
  (coefficient exactly the framework's interpolant, to sympy-residual 0),
  the door is dead: the framework does not generate the gap. FAIL = the
  result.
- **K2 (positivity/consistency):** if μ₂(u) ≤ 0 on any u ≥ 0 (mass-squared
  nonpositive), the sector is ghost/inconsistent — dead. (Committed algebra:
  μ₂ > 0 for u > 0, μ₂(0) = 0 — verified, but re-checked here.)
- **K3 (the G054 boundary):** if the Stueckelberg mass term is NOT
  Lorentz-invariant at the action level (i.e., it reintroduces the killed
  preferred-frame class, α₁ = O(1)), the gauge door is dead by G054. The
  gauged shift has NO explicit background (the gradient v is a solution of
  the sourceless equation, not a term of the action) — registered as the
  boundary; the referee's override kills the door.
- **K4 (the profile is wrong):** the parameter-free prediction is
  m_A(r)/m = √μ₂(u(r)) — if the MW halo's committed gradient profile gives a
  gap that does NOT close toward the EFE cap / vacuum, the structure claim
  fails. (Monotonicity: μ₂ strictly increasing on u > 0.)
- **K5 (the Clay scope):** NOT A KILL — the SU(3)/QCD-scale gap is explicitly
  OUT OF SCOPE (the framework has no QCD sector; an honest lane does not
  claim it). Registered so no reader believes this campaign solved the Clay
  problem. What IS claimed: the framework's own gap mechanism, exact, with
  its scale law.

## THE FALSIFIER RECIPE (parameter-free)

IF the gauged-shift sector exists, the massive-vector dispersion is
ω_A(k) = √(c_s²k² + m_A²) with m_A(r) = m·√(μ₂(u(r))). The RATIO law

    m_A(r)/m_A(r_ref) = √( μ₂(u(r)) / μ₂(u(r_ref)) )

is one number per radius, zero free parameters (m cancels). Data classes
that could kill: (a) a committed massless-vector signature INSIDE the
phantom region at μ₂ > 0 scale; (b) a gap that does NOT vanish in the Solar
System / beyond the cap; (c) a preferred-frame observable (α₁, α₂) that
G054's class forbids. The fiducial absolute scale (m = Λ) is SILENT to
laboratory probes by the framework's own rules — the Solar System is
Newtonian by construction — and the coupling is M_pl-suppressed; silence is
registered honestly as "structure proven, observability silent", never
upgraded to "detected".

## REGISTERED FOLLOW-UPS (from the referee audit, YM_REFEREE.md)

- **G1b — CLOSED (YM02_deep_face_kill, 8/8):** the U-MAP question's exact
  answer: the sourced deep face would carry g² = √(8π)·a0·g_N (+0.3500 dex),
  excluded by G114's own deep end (2.33 rms / 4.38 median) — the sourced face
  dies BY ITS OWN CONSTANTS; the equilibrium face is map-free, RAR-exact.
- **G1c — OPEN (new, from the audit):** the E02 vs B8 registers disagree on
  n·λ_dB³ by ~250× (8.6e-9 vs 3.4e-11) — both ≥8 orders below 2.612 ("not a
  condensate" survives either way) but the two committed registers should be
  reconciled by the owning lanes.
- **G1d — OPEN (the m-pin's falsifier, armed):** the identification
  m_gauge = m_dust is an assumption with a kill switch: the G168 ladder band
  (4, 6) keV firing, or any absolute pinning inconsistent with √μ₂·m.

## DELIVERABLES (this folder)

| File | Content |
|---|---|
| YM00_CAMPAIGN.md | this record (pre-registered gates; K1-K5 all closed 28/28 across YM01+YM02) |
| YM01_gap_derivation.py/.out/_results.json | the derivation lane 20/20 (both mass faces, the profile, the U-MAP finding) |
| YM02_deep_face_kill.py/.out/_results.json | the sourced-face closure 8/8 (g² = √(8π)·a0·g_N — G155's dead door re-derived in one number; the equilibrium face is map-free) |
| YM_PROOF.md | THE PROOF: the pinned theorem chain P1-P18, every row machine-verified |
| YM_REFEREE.md | the adversarial survivability audit (ALIVE 3 / BOUNDARY 4 / KILLED 0; most vulnerable: m = m_dust) |
| YM_NONABELIAN.md | the SU(3) obstruction (rank counting: eaten Goldstones ≤ 1 ≠ 8; no adjoint VEV possible) |
| lean/YM01_gap.lean | 19 theorems, exit 0, zero sorry (the gap spine) |
| lean/YM02_pinned_gap.lean | 17 theorems, exit 0, zero sorry (the pinned spine: ladder mass, C_f_value, deep_coeff, numeric bands) |
| YM_GAP_STATEMENT.md | the verdict: proven mechanism, pinned scale, honest Clay boundary |