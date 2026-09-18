# N13 — CONSTRUCTION EXPONENT-CONSISTENCY AUDIT (registration 2026-09-17)

**Object:** OpenAI *Finite Time Blowup for Navier–Stokes* (Sept 8 2026; for every
ν>0 a smooth forced blowup with uniformly bounded kinetic energy). **Scope:** the
construction's **scaling skeleton only** — the kind of check that catches fatal
internal contradictions without reading the proof (sections 4–10 untouched).
**Method:** independent sympy recomputation of every identity below, exact where
rational; paper text from the cached copy (`cdn.openai.com-bfcbecef31.md`), line
cites per item. Companion: `N13_construction_audit.py` (all gates, reproducible),
`.out`, `_results.json`. **Result: 7/8 PASS, 0 FAIL, A5 REGISTERED.**

## Gate table

| # | Claim (paper) | Skeleton identity (sympy-exact) | Value | Gate |
|---|---|---|---|---|
| A1 | exo-exponents (Sec 2.1 l.210-216, Sec 3.1 l.536-540) | ℓ_r=τ^½, ℓ_z=τ^(½−h), 0<h<1/100; ℓ_r/ℓ_z = τ^h → 0; vol = ℓ_r²·ℓ_z = τ^(3/2−h) | ratio τ^h (→0), vol τ^(3/2−h) | **PASS** |
| A2 | velocity exponents, Re (Sec 2.1 l.219-243) | \|u_θ\|,\|u_z\|≈τ^(−½−h); \|u_r\|=O(τ^−½); Re_θ=\|u_θ\|ℓ_r/ν ≈ τ^−h → ∞; Re_r = O(1) | Re_θ=τ^−h, Re_r=τ⁰ | **PASS** |
| A3 | diffusion-rate balance (Sec 2.1 l.247-268) | \|u_r\|/ℓ_r = τ^−1; \|u_z\|/ℓ_z = τ^−1; ν/ℓ_r² ≈ τ^−1 (ν fixed); ν/ℓ_z² ÷ ν/ℓ_r² = ℓ_r²/ℓ_z² = τ^(2h) → 0 | τ^−1, τ^−1, τ^−1, τ^(2h)→0 | **PASS** |
| A4 | core energy/dissipation integrability (Sec 2.1 l.227-228, Sec 3.5 l.1230-1243) | E_core = vol·\|u\|² = τ^(3/2−h)·τ^(−1−2h) = τ^(½−3h) → 0; D_core = vol·(\|u\|/ℓ_r)² = τ^(−½−3h); ∫₀^τ0 τ^(−½−3h) dτ = τ0^(½−3h)/(½−3h) < ∞ iff h<1/6; h<1/100<1/6 ✓ | E=τ^(½−3h), D=τ^(−½−3h); ∫ = 1.536 (τ0=½, h=1/100) | **PASS** |
| A5 | global energy bound sup_{t<1}‖u‖_L² < ∞ (Thm 3.1, Lemma 10.4) | core contribution → 0 (A4); **pulse/exterior energy control is proof-level, not skeleton-level** | — | **REGISTERED** (needs full proof) |
| A6 | material acceleration ~ \|u\|²/ℓ_r class (Sec 2.1 exponents; Sec 3.3 l.859-862 anchors τ^(−3/2−h) stress scale) | \|Du/Dt\| ~ \|u\|²/ℓ_r = τ^(−1−2h)/τ^½ = τ^(−3/2−2h) → ∞ | τ^(−3/2−2h) | **PASS** |
| A7 | pulse stress cone (Sec 3.3 l.911-920, App C) | ⟨cos²⟩=½, ⟨cos·sin⟩=0; families (½,0),(0,½): rank 2 ⇒ span ℝ²; target (a,b) via c₁=2a, c₂=2b | rank 2 | **PASS** |
| A8 | honesty box | skeleton audit ≠ proof audit (below) | — | **PASS** |

**0 FAILED** — no exponent-level internal contradiction found in the skeleton.

## A6 — material-acceleration window exit (framework numbers)

Skeleton law (paper exponents): |Du/Dt| ≍ τ^(−(3/2+2h)) — the |u|²/ℓ_r class,
dominated by the centripetal u_θ²/r term. Lab mapping (N05/N08 convention:
\|u\|=O(1) at τ=1 → 1 m/s, L₀=1 m ⇒ a_scale = 1 m/s²; a₀ = 9.3619e-11 m/s²,
floor W = 3.5):

- η(τ) = a_scale/a₀ · τ^(−(3/2+2h)), η(1) = 1/a₀ = **1.068e10** (Newtonian face
  by ~10 orders at τ=1).
- Exit of the N05 floor: η(τ_exit) = 3.5 ⇒ **τ_exit = (3.5·a₀/a_scale)^(2/(3+4h))**:
  - h → 0: **τ_exit = 4.753e-7**
  - h = 1/200: **τ_exit = 5.234e-7**

Both ≈ 5e-7 (order 1e-7): the construction is Newtonian-face by ~10 orders and
exits the measured floor near τ ~ 5e-7 while still smooth — **consistent with
N08** (which registered 5.2e-7 at h = 0.005; matches to 3 s.f.). The scaling law
is from the paper; the a₀ normalization and floor are the framework's (N05).

## A5 — registration (not graded)

The skeleton guarantees only E_core → 0 (A4). The theorem's global energy bound
sup_{t<1}‖u(t)‖_L² < ∞ additionally requires controlled pulse and exterior
energies — that is established in the proof (Thm 3.1(ii)-(iii); Lemma 10.4), not
in the scaling skeleton, and is **NOT claimed as audited here**.

## A8 — honesty box

This audit verifies the construction's **scaling skeleton** — exponent
arithmetic consistent with the paper's own definitions — and nothing more. A
PASS means: no fatal internal contradiction of the exponent skeleton. It is
**not** an endorsement of the theorem. Claimed-but-NOT-audited: the
residual-smoothing ladder, the flatness estimates, Lemmas 10.4 and 10.5,
everything past Section 3.6 (sections 4–10, Appendices A–C). A5 is registered,
not passed.

---
**Verdict:** COMPLETE — 7/8 checks PASS (A5 REGISTERED: needs the full proof;
0 FAILED).