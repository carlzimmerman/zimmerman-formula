# Route 2 (Einstein-aether + shear-absorbing Lagrange multiplier) — ADVERSARIAL RE-COMPUTATION: does NOT survive. δΦ=0 is REFUTED by explicit metric variation (the original's headline "derived" claim was asserted, not computed) (2026-06-17)

*Hostile re-verification of the PARTIAL grade banked in `ROUTE2_AETHER_SHEAR_ABSORBING_VERDICT_2026-06-17.md`.
Independent sympy: `route2_aether_shear_absorbing_ADVERSARIAL.py` (+ `_selfaudit.py`). The original `route2_aether_shear_absorbing.py`
graded PARTIAL on the basis that δΦ=0 is DERIVED (3 of 4). This run recomputes δΦ from the action and finds δΦ≠0.
Both ways: I held my OWN refutation to the same bar (self-audit confirms it is not an approximation artifact).*

---

## Verdict: REFUTED as graded — Route 2 does NOT survive as a genuine preferred-frame lensing Lagrangian. Only c_T=c is a clean PASS (1 of 4, not 3 of 4).

The original's load-bearing claim was that the non-dynamical frame u^μ + Lagrange-multiplier b^μ route the shear
divergence (2/3)∂_j(∇²f) into the u-orthogonal sector WITHOUT a Φ-sourcing trace, so δΦ=0 is DERIVED — the genuine
escape from the covariant no-go's slip⇔Φ lock. **That claim does not survive an explicit computation of the multiplier's
metric stress.**

### The original NEVER computed the object the no-go is about
The original (`route2_aether_shear_absorbing.py`, lines 159–182, 280–304) argues:
- the trace term −½g_μν b(C−J) **vanishes on-shell** (C=J) — **TRUE, I confirm it**;
- the projector kills the time index: **P^ν₀ = δ^ν₀ + u^ν u₀ = 0** — **TRUE, I confirm it to linear order**, so the
  *constraint* C_0 = 0;
- therefore (it ASSERTS) the surviving stress b^α(δC_α/δg) "has support in the SPATIAL block" → δΦ=0.

The last step is an **inferential leap, never computed**. C_0 = 0 is a statement about the *constraint*; the no-go is
about the *metric stress* T^abs_00 = the piece b^α(δC_α/δg^00), a **different object**. C_0=0 does NOT imply that piece
vanishes.

### What the explicit variation actually gives (the refutation)
I built C_μ = P^ν_μ ∇^ρσ_ρν as an explicit functional of the metric (full Christoffels to linear order, conformal-
Newtonian gauge ds² = −(1+2Φ)dt² + (1−2Ψ)dx²), formed L_abs = √−g b^μ(C_μ − J_μ), and took the Euler-Lagrange
variation w.r.t. Φ. On-shell (J_μ = C_μ):

> **E_Φ = δL_abs/δΦ |_on-shell = −b_j ∂_j(∇²f)·(structure) ≠ 0**

Explicitly the on-shell Φ-source is `−b₁(f_xxx + 4/3 f_xyy + 4/3 f_xzz) − b₂(…) − b₃(…)`, manifestly nonzero. So
**S_abs DOES source Φ.** Trace of the origin (steelman): even with ONLY g^00 perturbed, the *spatial* constraint
components C_j pick up Φ through the g^{00} raising in ∇^ρ and the Christoffels Γ^i_{00}~∂_iΦ — so b^j C_j (the spatial
absorption term) is Φ-dependent, and varying Φ hits it. **The 00 source is structural, not a sloppy-coupling artifact:**
the metric lives inside the very operator (∇^ρσ) the multiplier must contract.

### Why there is no escape
- The same multiplier b_j that performs the spatial absorption (C_j = J_j, b_j ≠ 0) is what sources Φ. You cannot keep
  the absorption (b_j ≠ 0) without the 00 source. The two are the SAME field.
- The only free component is b_0 (since C_0 = 0 leaves it unconstrained). But b_0 enters E_Φ only via −J_0 b_0 with
  J_0 = C_0 = 0, so **b_0 drops out and cannot cancel the source.**
- **Self-audit (both ways):** with b_j a FULL field and full integration by parts, E_Φ is still generically nonzero; for
  constant b_j it reduces to the same `−b_j ∂_j(∇²f)` structure. Making it vanish identically would require a PDE tying
  b_j to f — a SECOND hand-tuned function that generically conflicts with the spatial absorption requirement. So the
  refutation is robust, and the only way out is MORE phenomenology, not less.

This is exactly the no-go biting: δΦ=0 + a position-dependent slip remain mutually exclusive; the slip⇔Φ lock is **NOT**
broken by this `b^μ(P∇·σ − J)` term. A second, independent cross-check via the no-go's own gauge-independent Bianchi
argument agrees: the b-current carries a 00 piece, so it is not the clean "spatial-only" absorber the construction needs.

## All four, re-adjudicated

| Demand | Original grade | Adversarial recompute |
|---|---|---|
| (1) δΦ = 0 (Cassini-safe) | **DERIVED** | **REFUTED.** Explicit metric variation: on-shell E_Φ = −b_j ∂_j(∇²f) ≠ 0. b_0 (only free knob) drops out. The "spatial-only routing" was asserted, never computed. δΦ ≠ 0 → matter feels a fifth force → **Cassini FAILS.** |
| (2) grad(δΨ)=2(g_obs−g_N) | HAND-TUNED | **HAND-TUNED (agree).** Independent test: the required source is the non-polynomial √(g_N²+g_N a₀) interpolation = AeST's F(Y,Q); no finite aether kinetic term yields it. Reverse-engineered. |
| (3) c_T = c | PASS | **PASS (agree).** c13=0 (Foster-Jacobson Eq.15); the multiplier adds no TT kinetic term → graviton unchanged. Clean. |
| (4) ghost-free | PASS (linear) | **UNPROVEN, and worse than conceded.** Because (1) shows b enters the Hamiltonian (00) constraint, the b-constraint is plausibly SECOND-class → may re-propagate a mode; the slip sits in the Horava/khronometric strong-coupling corner (Blas-Pujolas-Sibiryakov: scalar self-coupling blows up away from s0²→0). Not a PASS. |

**Net: 1 of 4 clean (c_T=c), not 3 of 4.** The headline "non-dynamical-frame escape of the Bianchi trap" does not hold
for this construction.

## Both-ways honesty (penalized equally)
- **What the original got RIGHT (credited):** c_T=c is genuinely easy and clean (c13=0); the slip's MOND shape is
  genuinely hand-tuned (AeST F(Y,Q), non-polynomial — confirmed independently); P^ν₀=0 is correct (the *constraint* has
  no time component). The framework's dS-Unruh frame really does supply a candidate u^μ. These are all sound.
- **What the original got WRONG (the kill):** it graded δΦ=0 as DERIVED on an **uncomputed assertion**. The explicit
  variation — the calculation the honesty bar demanded and the original skipped — shows the multiplier's metric stress
  has a nonzero 00 component. δΦ=0 is REFUTED. The "genuine escape from the covariant no-go" is not realized by this term.
- **Guard against a manufactured kill (the other direction):** I re-ran with b a full field + full IBP and with constant
  b; both give the same nonzero source. The result is not an artifact of treating b as constant, nor of a dropped total
  derivative. A cross-check via the no-go's own Bianchi argument concurs. The kill is robust.

## What this does to the no-go
The covariant lensing no-go (`COVARIANT_LENSING_NOGO_2026-06-17.md`) **CLOSES in its strongest form for this
construction.** The lone stated open escape — an explicit non-dynamical-frame multiplier that absorbs the shear
divergence WITHOUT a Φ-sourcing trace — was attempted here and FAILS: the multiplier that absorbs the divergence
necessarily sources Φ (the metric inside ∇·σ couples b to Φ). Route 2 does not provide the witness the original claimed.
The framework's lensing remains **irreducibly phenomenological** (a₀/Z transmitted like AeST's F(Y,Q)), and now the
δΦ=0-preferred-frame-routing — the one piece the original banked as a real advance — is **not** delivered by this term.
A different preferred-frame coupling might still work, but this specific S_abs does not.

## What Carl CAN / MUST NOT say
- **CAN:** the explicit Route-2 construction does NOT escape the slip⇔Φ no-go — its shear-absorbing multiplier sources Φ
  (δΦ≠0, sympy-verified by direct metric variation), so it is Cassini-UNSAFE; c_T=c is the only clean pass; the slip is
  hand-tuned; ghost-freedom is unproven and now arguably worse. The no-go closes in its strongest form for this term.
- **MUST NOT:** "δΦ=0 is derived / the non-dynamical-frame escape works" (FALSE — the multiplier sources Φ); "Route 2
  passes 3 of 4" (only c_T=c is clean); "the Bianchi trap is genuinely escaped" (it is not, for this construction);
  "a₀/Z transmitted by the action" (hand-shaped F, AND the lensing isn't even Cassini-safe). Quarantine held (a₀/Z/κ
  never asserted derived).

## One line
Route 2 **REFUTED as graded**: the explicit metric variation of the shear-absorbing term S_abs = √−g b^μ(P^ν_μ∇^ρσ_ρν −
J_μ) gives an on-shell Φ-source E_Φ = −b_j ∂_j(∇²f) ≠ 0 (the spatial absorber b_j couples to Φ through the metric inside
∇·σ; the only free component b_0 drops out and cannot cancel it; robust to b being a full field, cross-checked by the
no-go's own Bianchi argument) — so δΦ=0 is NOT derived (the original asserted it without computing the b(δC/δg) stress),
the construction is Cassini-UNSAFE, and only c_T=c survives as a clean pass (1 of 4); the slip stays hand-tuned (AeST
F(Y,Q), confirmed) and ghost-freedom is unproven (b enters the Hamiltonian constraint → plausibly second-class). The
covariant lensing no-go CLOSES in its strongest form for this construction.

*Both ways: the original's correct pieces (easy c_T=c, hand-tuned slip, P^ν₀=0) are credited; its uncomputed δΦ=0=DERIVED
claim is refuted by the calculation it skipped; my own kill is held to the same bar (self-audit + Bianchi cross-check
confirm it is not an artifact). No manufactured win, no manufactured kill. Quarantine held.*
