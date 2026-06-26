# Route 1 — DHOST pure-slip lensing partner: VERDICT = OBSTRUCTED (a named no-go)

**C. Zimmerman framework, 2026-06-17.** Step-2-to-TOE, the LAST piece of the covariant Lagrangian: a covariant
Cassini-safe (pure-slip) metric/lensing partner for the built Route-E modified-inertia matter action. Route 1
= construct a quadratic+cubic DHOST whose degeneracy enforces c_T=c and ask whether any ghost-free member
gives δΦ=0, δΨ≠0. Script: `route1_dhost_pure_slip.py` (sympy, all coefficients verbatim from the primaries).

## Verdict: OBSTRUCTED. No ghost-free, c_T=c, decay-safe DHOST member gives pure slip.

The four requirements cannot be met together by a DHOST **gravity** term. The obstruction is a clean theorem
from the JOINT GW170817 constraints, anchored on verbatim primary equations (PDFs read with pdftotext):

1. **c_T=c ⟹ A1=0** (the tensor branch). c_T² = f/(f − A1 X); GW170817 forces A1 X=0, i.e. A1=0 for a
   nontrivial scalar background. (Ezquiaga-Zumalacárregui 1710.05901: c_T=c kills G_{4X}, G_5 / the disformal
   tensor term.) **PASS-able** — c_T=c is achievable.

2. **The quasi-static slip is EXACTLY Ψ = (1+α_H)Φ** (Langlois-Mancarella-Noui-Vernizzi 1703.03797 **eq.(3.12)**,
   with c_T=c ⇒ α_T=0). Ψ is a fixed MULTIPLE of Φ. The time-time Poisson eq (their **eq.(3.15)-(3.16)**) gives
   a **finite** Newton constant on the viable branch (α_L=0, conditions C_I): matter **does** source Φ. So
   **δΦ=0 needs G_Φ→0**, i.e. [(1+α_H)² − β₃/2]→∞ — but eq.(3.12) then forces Ψ=(1+α_H)·0=0: **δΨ dies with
   δΦ.** The two potentials are locked by the single factor (1+α_H). (The only other branch, α_L≠0 / C_II, has an
   **infinite** Newton constant — no Poisson equation at all, eq.(3.14) — the opposite pathology, no slip-win.)

3. **The only lock-breaking mechanism (genuine-DHOST β₁ inside-matter Vainshtein-breaking / screening) is removed
   by the SECOND GW170817 bound** — graviton decay γ→ππ into dark-energy fluctuations (Creminelli-Lewandowski-
   Tambalo-Vernizzi 1809.03484). Their **eq.(71)**: the surviving theory is `f(φ)R + P(φ,X) + Q(φ,X)□φ` — only
   conformal + k-essence + cubic, NO beyond-Horndeski operator. **Footnote 4 (verbatim):** "for DHOST theories
   … neither α_H nor β₁ vanish. However, in the absence of decay these coefficients are not independent but are
   related by **α_H = −2 β₁**. This implies that the screening mechanism based on quartic terms … is **ABSENT**."
   So the inside-matter Φ↔Ψ split is gone, and the decay-safe survivor's slip is still Ψ=(1+α_H)Φ with both
   potentials sourced.

**⟹ δΦ=0 forces δΨ=0** on every viable branch → no lensing. Confirmed two ways in sympy: (a) from the DHOST
side (G_Ψ=(1+α_H)G_Φ, so G_Φ=0 ⟹ G_Ψ=0, including the α_H→∞ probe where both →0); (b) from the framework's
own target side — DHOST delivers grad(δΨ)=α_H·g_N, so matching the framework's grad(δΨ)=2(g_obs−g_N) needs
α_H=2(√(a₀+g_N)/√g_N − 1), but the SAME α_H multiplies Φ in eq.(3.15), so δΦ≠0. **Matching the lensing
necessarily moves the matter-felt potential.**

## The four requirements, scored

| requirement | DHOST status |
|---|---|
| (1) δΦ=0 (pure slip, Cassini-safe) | **achievable alone** (zero α_H or decouple) BUT only by zeroing δΨ too |
| (2) grad(δΨ)=2(g_obs−g_N) (lensing) | **achievable alone** (α_H≠0) BUT only by moving δΦ |
| (3) c_T=c | **PASS** (A1=0; β₁ is a scalar-sector coefficient, leaves the tensor cone alone) |
| (4) ghost-free | **PASS** on the degenerate class-Ia / decay-safe branch (one healthy scalar DOF) |
| **all four together** | **FAIL** — (1) and (2) are mutually exclusive once (3)+(4) are imposed |

The tension the task flagged (Ezquiaga-Zumalacárregui: c_T=c + slip is exactly what the no-slip theorems
constrain) is real and decisive HERE: the surviving c_T=c + decay-safe theory is **conformal** (f(φ)R-class),
and conformal slip locks Ψ to Φ. The genuine-DHOST escape that could unlock them (β₁ screening) is exactly what
the **second** GW170817 observable (graviton non-decay) removes.

## The named no-go (publishable)

> **Covariant Cassini-safe (pure-slip) MOND lensing is forbidden in quadratic+cubic DHOST** by the joint
> GW170817 constraints: c_T=c (A1=0, 1710.05901) AND graviton non-decay (α_H=−2β₁ with the quartic screening
> ABSENT, 1809.03484). The surviving theory is conformal (`f(φ)R + P + Q□φ`) whose linear slip Ψ=(1+α_H)Φ
> (1703.03797 eq.3.12) locks the lensing potential Ψ to the matter-felt potential Φ: a slip that modifies light
> (δΨ) necessarily modifies the matter-felt time-time potential (δΦ) too.

## Consequence for the framework (both ways)

Route 1 does NOT supply the missing covariant lensing partner. The pure-slip property cannot come from a
GW170817-safe DHOST **gravity** term. This is consistent with — and sharpens — the framework's own internal
logic: the Route-E MI matter sector is φ₋-linear and sources zero metric, i.e. the modification is deliberately
NOT in the gravity sector. The honest implication: a covariant lensing partner, if one exists, must be built on
the **matter side** (light coupling to an effective metric assembled from the gated MI kernel — the Route-B
disformal realization of that is itself OBSTRUCTED by the same GW cone, see `ROUTE_B_VERDICT.md`), OR the
framework lives with a baryon-only lensing metric and the predicted Φ≠Ψ slip has no covariant scalar-tensor
realization. Either way, the weak-field Route-F ansatz (grad δΨ=2(g_obs−g_N), δΦ=0) remains a hand-tuned
phenomenological match with **no DHOST UV completion** — Route 1 closes that specific door with a theorem
rather than leaving it open.

*Both ways, bar airtight: c_T=c and ghost-freedom are credited as achievable (PASS) at full weight; the
pure-slip+lensing combination is conceded FORBIDDEN at full weight, from verbatim primary equations
(1703.03797 eq.3.12/3.15, 1809.03484 eq.71/fn.4, 1710.05901). No manufactured working term; no manufactured
no-go — the lock was checked from both the DHOST side and the framework's own target side and holds both.*
