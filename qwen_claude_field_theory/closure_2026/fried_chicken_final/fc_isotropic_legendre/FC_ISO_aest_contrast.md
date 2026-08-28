# FC-ISO — AeST contrast: how 6 DOF cancels the anisotropic stress that a 2-DOF theory cannot

**Task.** Derive how AeST + J₁₀ achieves Φ = Ψ (γ_PPN = 1, VERIFIED) despite carrying
the *same* anisotropic scalar Hessian Aⁱʲ = μγⁱʲ + (y μ′)uⁱuʲ that forces a metric slip
in every 2-DOF constraint completion (setup: Σ_P = y μ′). Identify the exact cancellation
mechanism; show whether it provably requires the extra propagating field(s) a 2-DOF theory
lacks; if so, that is the physical content of the unified no-go on the lensing axis.

**Files.**
- `fc_iso_aest_contrast.py` — 14/14 sympy certificates, exit 0.
- `fc_iso_aest_contrast.out` — full run log.
- Committed cite (re-run this session, **44/44, exit 0**):
  `real_research/reviews/typeII_direct_variation_2026.py`.

---

## Result in one paragraph

AeST reaches Φ = Ψ because its MOND kinetic invariant is contracted with the
**aether-orthogonal projector** hᵘᵛ = gᵘᵛ + AᵘAᵛ, not with the bare inverse metric. Because
the aether Aᵤ is unit-timelike (enforced by the Lagrange multiplier λ(A·A+1)), that projector
is **metric-independent**: 𝒴 = |∇φ + Q₀a|² at O(ε²) with no metric-shear coupling whatsoever
(PART 2, reproducing committed checks A6/A7). The dangerous anisotropic gradient stress
∂ᵢφ∂ⱼφ — the *same* y μ′ Hessian a 2-DOF theory carries — is therefore removed from the
gravitational (traceless) sector, and its residual Bekenstein–Milgrom curl is carried by the
aether **transverse mode** aᵀ (committed typeII E3/D7: 2K_B ∇²aᵀ = 2(2−K_B)Q₀ Sᵀ). The dark
sector supplies **no anisotropic metric stress**, so the traceless ij Einstein equation is
∂ᵢ∂ⱼ(Φ−Ψ) = 0 with no source (typeII D1–D3) ⇒ γ_PPN = 1 for every K_B, every free function,
every Q₀. Both structures used in the cancellation — the unit-timelike vector and its
propagating transverse mode — are **absent from a 2-DOF constraint theory**. Hence a pure
2-DOF completion of an isotropic MOND law with μ′ ≠ 0 cannot cancel Σ_P = y μ′: the slip is
**forced**.

---

## The mechanism, step by step

### 1. The projector identity (THEOREM, PART 1, off-shell algebra)
For hᵘ_ν = δᵘ_ν + AᵘA_ν with s ≡ A·A:
- **h² − h = (s+1) AᵘA_ν** ⇒ h is idempotent **iff** A·A = −1 (unit-timelike). *(check 01)*
- **hᵘ_ν Aᵛ = (1+s)Aᵘ = 0** on-shell ⇒ h projects **out** the aether direction. *(check 02)*

So the invariant 𝒴 = hᵘᵛ∂ᵤφ∂ᵥφ measures the scalar gradient **orthogonal to the aether**.
The projector is a genuine projector *only because* the aether carries a unit-norm constraint —
i.e. it is the constraint of a dynamical vector field.

### 2. CRUX — 𝒴 is metric-independent (DERIVATION, PART 2)
Generic 10-component static metric H_{μν}, generic aether (a₀, aᵢ), unit constraint solved
order by order (residual = 0, check 04). Then:
- 𝒴 has **no ε⁰, no ε¹** piece (check 05);
- **𝒴 at O(ε²) is independent of every metric component H_{mn}** (check 06) — the projector
  absorbs all of it — and equals **|∇w + Q₀a|² exactly** (check 07).

This is the whole trick: the metric-shear coupling that a bare scalar has is *not present* in
𝒴, because Aᵘ (whose A₀ = −H₀₀/2 + … is fixed by the constraint) rides the metric and cancels
it. Reproduces committed typeII A6/A7.

### 3. Contrast — the bare (2-DOF/AQUAL) scalar keeps the stress (DERIVATION, PART 3)
The correct source of the traceless Einstein equation is the stress **∂𝒴/∂gⁱʲ** (not the ε²
metric-coefficient, which hides the shear coupling at ε³/2PN). Computing it from the definition:
- **bare:** ∂𝒴_bare/∂gⁱʲ ∼ ∂ᵢφ∂ⱼφ — off-diagonal nonzero (checks 08–09) ⇒ traceless stress
  2F′(𝒴)[∂ᵢφ∂ⱼφ]ᵀᶠ ≠ 0 ⇒ **Φ ≠ Ψ** (the York/AQUAL slip; `theory_2026/york/ppn_lensing_cassini_2026.py`).
- Frozen kernel: Σ_P = y μ₁₀′ = y(1+y¹⁰)^(−11/10) > 0, never 0 for μ′ ≠ 0 (check 11; setup 18/19).
- **AeST:** ∂𝒴_aest/∂gⁱʲ = ∂ᵢφ∂ⱼφ + 2𝒬·∂(Aᵘ∂ᵤφ)/∂gⁱʲ — an **extra aether-projection term**
  ∝ 𝒬 = Aᵘ∂ᵤφ (check 10). This extra term **vanishes if Aᵤ → 0** (check 12): no aether, no cancellation.

### 4. What the aether must do, and the committed full result (PART 4)
γ_PPN = 1 requires the **total** traceless dark stress to vanish:
0 = Tᵀᶠ_ij[scalar] + Tᵀᶠ_ij[aether F² + constraint]. The scalar alone gives 2F′[∂ᵢφ∂ⱼφ]ᵀᶠ ≠ 0;
the projector (PART 2) plus the aether kinetic/constraint stress remove it. The full-action
proof (all ten H components kept, aether varied, multiplier retained) is committed and re-run
this session:
- **D1** the entire non-Einstein sector is independent of h_ij at quadratic order;
- **D2** off-diagonal ij equations are ∂ᵢ∂ⱼ(Φ−Ψ) = 0 with **no source**;
- **D3** γ_PPN = 1 **exactly** for every K_B, every free function, every Q₀;
- **E3/D7** the residual BM curl is carried by the aether **transverse mode** (a propagating vector).

---

## Does the cancellation require the extra DOF? — YES (THEOREM, PART 5)

Two structures are load-bearing above, **both absent from a 2-DOF constraint theory**:

| structure | role | present in AeST | present in 2-DOF |
|---|---|---|---|
| unit-timelike **vector Aᵤ** (constraint λ(A·A+1)) | builds the metric-free projector h = g + A⊗A that zeros the ∂ᵢφ∂ⱼφ coupling | ✔ (3 vector DOF) | ✗ — no vector; MOND invariant must be gⁱʲ∂ᵢq∂ⱼq (metric-dependent) → slip |
| aether **transverse mode aᵀ** (propagating) | carries the Bekenstein–Milgrom curl in non-symmetric sources | ✔ | ✗ |

A 2-DOF constraint theory has only **{2 metric polarizations} + {a second-class auxiliary q}**.
The auxiliary q is non-dynamical (its conjugate momentum is fixed by the second-class
constraint), so it carries **zero traceless stress** — certified in `fc_iso_setup` PART 5:
q’s isotropic μδⁱʲ modulus is pure-trace (pressure), only the (y μ′)uu piece is traceless,
and there is no other field to cancel it.

**DOF ledgers (checks 13–14):** AeST healthy = 2(tensor)+1(scalar)+3(vector) = **6** (SZ21,
arXiv:2007.00082 / 2307.15126). 2-DOF constraint theory = 2(tensor)+0(auxiliary) = **2**.
The vector — precisely the field that supplies the cancelling stress — is exactly what the
2-DOF theory lacks.

**Conclusion.** The cancelling traceless stress must come from a *field*. AeST supplies it with
the aether (unit vector + transverse mode, 4 extra propagating DOF). A pure 2-DOF constraint
theory has no field with independent traceless stress, so it cannot cancel Σ_P = y μ′. The slip
is **forced** whenever μ′ ≠ 0. On the lensing axis this closes the constraint-first isotropic-
Legendre program: **sourcing a MOND-enhanced Φ = Ψ requires extra propagating structure; 2 DOF
is insufficient.**

---

## Honesty ledger

| claim | label |
|---|---|
| projector idempotency ⇔ A·A=−1; h projects out A | THEOREM (sympy, checks 01–02) |
| 𝒴 metric-free at O(ε²), = \|∇w+Q₀a\|² | DERIVATION (checks 03–07; reproduces committed A6/A7) |
| bare scalar stress ∂𝒴/∂gⁱʲ ∼ ∂ᵢφ∂ⱼφ ≠ 0 ⇒ slip; Σ_P = y μ′ | DERIVATION (checks 08–11; matches setup + York) |
| AeST adds an aether-projection stress ∝ 𝒬, vanishing if Aᵤ→0 | DERIVATION (checks 10, 12) |
| full-action γ_PPN=1 for every K_B/free-function/Q₀; transverse-mode carrier | EXTERNAL-INPUT / committed (typeII D1–D3, E3; re-run 44/44, exit 0) |
| AeST action; 6-DOF ledger | EXTERNAL-INPUT (SZ21 2007.00082; 2307.15126) |
| cancelling stress must come from a field; 2-DOF has none ⇒ slip forced | THEOREM (structural, checks 13–14 + fc_iso_setup PART 5) |

**Scope caveat (not overstated).** PART 5 closes the **isotropic-Legendre / second-class 2-DOF
class** — the program’s actual scope. It does not claim “no conceivable trick” outside that class;
it shows that *within* it, the field content that AeST uses to cancel the anisotropic stress is
provably unavailable, so the lensing slip is forced. The decisive question of the setup —
“does an isotropic second-class Legendre completion with Σ_P = 0 and μ′ ≠ 0 exist?” — is answered
**NO** on the mechanism side: the object that would set Σ_P = 0 is an extra propagating field, and
adding it exits the 2-DOF class.
