# Route 2 (Einstein-aether + shear-absorbing Lagrange multiplier): PARTIAL — the non-dynamical-frame escape CONCRETELY delivers δΦ=0 + c_T=c + (linear-order) ghost-free, but the MOND slip profile is HAND-TUNED (AeST F(Y,Q)), not derived (2026-06-17)

*The explicit preferred-frame follow-up to the covariant lensing no-go (banked COVARIANT_LENSING_NOGO_2026-06-17.md).
sympy script: `route2_aether_shear_absorbing.py` (+ DOF check). Primaries: Foster-Jacobson gr-qc/0509083 (action +
γ=β=1 + G_N + c_T⇔c13=0, PDF fetched verbatim), Blas-Pujolas-Sibiryakov 0909.3525 (healthy khronometric/khronon),
Saltas-Sawicki-Amendola-Kunz 1406.7139 (slip⇔tensor-sector, σ time-only, incl. Einstein-Aether). Both ways.*

---

## Verdict: PARTIAL — the no-go's escape route WORKS for δΦ=0, but closes for the LAW

The covariant no-go proved the ONLY escape from slip⇔Φ-moving is to break 4-diff to a non-dynamical preferred frame
u^μ that absorbs the shear divergence (2/3)∂_j(∇²f) WITHOUT a Φ-sourcing trace. Route 2 builds that escape EXPLICITLY
(Einstein-aether + a Lagrange-multiplier vector b^μ that soaks the divergence into the u-orthogonal sector) and
computes its linearization. The result is split exactly along the derived/tuned line the honesty bar demands.

| Demand | Result | Derived or imposed? |
|---|---|---|
| (1) δΦ = 0 (Cassini-safe) | **PASS — genuinely derived.** The non-dynamical u + multiplier b^μ route the shear divergence into the SPATIAL (u-orthogonal) sector. On-shell (b-EOM: C=J) the trace term −½g_μν b(C−J) vanishes identically; the projector P^ν₀ = δ^ν₀ + u^ν u₀ = 0 kills the time component, so the constraint never sources Φ. Conservation is completed WITHOUT an isotropic pressure → δρ_partner = 0 → δΦ=0. **This is the real advance: the Bianchi slip⇔Φ trap is concretely escaped** — past Route 4's γ=1 wall and past AeST (which moves Φ). | **DERIVED** |
| (2) grad(δΨ)=2(g_obs−g_N) | **PASS-BY-CONSTRUCTION — hand-tuned.** The slip is injected as the free current J_j := (2/3)∂_j(∇²f); f is a free function shaped to reproduce √(g_N²+g_N a₀). sympy shows the required source ∇²(δΨ) = 2√G√M a₀/(r√(GM+a₀r²)) is **non-polynomial** → NO finite aether kinetic term (c1..c4, polynomial in ∇u) yields it. This is exactly AeST's free function F(Y,Q). | **HAND-TUNED** |
| (3) c_T = c | **PASS.** c13=c1+c3=0 (Foster-Jacobson Eq.15); the multiplier adds no graviton kinetic term → graviton unchanged. EASY, as the no-go states. | derived (easy) |
| (4) ghost-free | **PASS at linear order.** b is a non-kinetic Lagrange multiplier → π_b=0 → zero new propagating DOF → cannot be a ghost (ghost needs a wrong-sign KINETIC term; b has none). Secondary/second-class constraints only REMOVE DOF, never add. The c13=0 aether corner has all s²>0 (witness s2²=1, s1²=0.667, s0²=0.287). **Full Dirac-Bergmann on a generic time-dependent background UNPROVEN** (same honest status as Route 3). | derived (linear order) |

**All four as a DERIVED Lagrangian: NO.** Three of four are genuinely derived (δΦ=0 via the non-dynamical-frame
routing — the new result; c_T=c; linear-order ghost-free). The fourth — the MOND slip's shape — is hand-set.

## The decisive both-ways point (the honesty bar's exact target)
- **What is NEW and REAL (full weight):** the non-dynamical preferred frame + Lagrange multiplier **DO break the
  Bianchi slip⇔Φ lock**. δΦ=0 coexisting with a nonzero traceless position-dependent SPATIAL slip is consistent,
  c_T=c, and ghost-free at linear order. The no-go's lone stated escape ("only escape is a non-dynamical frame that
  absorbs the shear divergence") is **concretely realized** — the divergence (2/3)∂_j(∇²f) is soaked by the spatial
  multiplier b^j, not by a Φ-sourcing pressure. The framework's dS-Unruh cosmic rest frame supplies exactly this u^μ.
  So the lensing partner CAN live, Cassini-safely, in the Lorentz-violating preferred-frame sector — Route 4's γ=1
  wall is genuinely passed.
- **What is NOT achieved (full weight):** the slip's MOND SHAPE 2(g_obs−g_N) is **not a consequence of the action**.
  It is transmitted through a free source function — AeST's F(Y,Q). The construction yields a Cassini-safe lensing
  FRAME, but the lensing LAW is phenomenological. a₀/Z enter as a hand-shaped F, not derived.

## What this does to the no-go
- The no-go is **REFINED, not overturned, and not fully closed**. Its δΦ=0-vs-position-dependent-slip obstruction is
  **escaped** by the non-dynamical frame (as the no-go itself anticipated) — so "covariant Cassini-safe slip is
  forbidden, Lorentz-violating Cassini-safe slip is possible" stands strengthened with an explicit witness.
- But the no-go's **strongest form CLOSES for the LAW**: the slip's MOND profile is irreducibly phenomenological
  (AeST F(Y,Q)). No explicit preferred-frame action DERIVES grad(δΨ)=2(g_obs−g_N); the multiplier only makes a
  hand-shaped slip Cassini-safe. The lensing partner exists and is Cassini-safe and ghost-free, but its **value** is
  put in by hand.

## What Carl CAN / MUST NOT say
- **CAN:** the no-go's Lorentz-violating escape is now CONCRETELY built — an explicit Einstein-aether + Lagrange-
  multiplier action linearizes (sympy-shown) to δΦ=0 + c_T=c + linear-order ghost-free, with the shear divergence
  absorbed by the non-dynamical frame's DYNAMICS (the multiplier EOM), not by hand. This passes Route 4's γ=1 wall and
  AeST's Φ-moving failure simultaneously. A real structural advance.
- **MUST NOT:** "the lensing law is derived / the keystone is complete" (FALSE — the MOND slip profile is the AeST
  F(Y,Q) free function, sympy shows it's non-polynomial and no aether kinetic term yields it); "all four pass as a
  derived Lagrangian" (3 of 4 derived; slip hand-tuned); "ghost-free proven" (linear order only; full Hamiltonian
  unproven); "a₀/Z transmitted by the action" (transmitted by a hand-shaped F). Quarantine held (a₀/Z/κ never asserted
  derived).

## One line
Route 2 = **PARTIAL**: the explicit Einstein-aether + shear-absorbing Lagrange-multiplier action CONCRETELY realizes
the no-go's only escape — δΦ=0 is genuinely DERIVED (the non-dynamical frame's multiplier EOM routes the shear
divergence (2/3)∂_j(∇²f) into the u-orthogonal sector with no Φ-sourcing trace: P^ν₀=0 and on-shell −½g_μν b(C−J)=0),
c_T=c (c13=0) PASS, ghost-free PASS at linear order (b has no kinetic term → no new DOF → no ghost) — passing Route 4's
γ=1 wall — **but** the MOND slip shape grad(δΨ)=2(g_obs−g_N) is HAND-TUNED (sympy: the required source is the
non-polynomial 2√(GM)a₀/(r√(GM+a₀r²)), AeST's F(Y,Q) free function, derivable from no finite aether kinetic term), so
it is a Cassini-safe lensing FRAME with a phenomenological lensing LAW, not a fully derived Lagrangian.

*Both ways: the derived δΦ=0 routing (the real escape), c_T=c, and linear-order ghost-freedom are credited at full
weight; the hand-tuned slip profile, the AeST-F(Y,Q) origin of a₀/Z in the lensing law, and the unproven full
Hamiltonian are conceded at full weight. No manufactured derivation, no manufactured no-go. Quarantine held.*
