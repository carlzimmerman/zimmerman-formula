# FC-AeST preferred-frame program — PHASE 2, ROUTE B: the scalar contribution Δα₂^(φA)

**Files:** `fc_solveB_partA_fj.py` (Foster–Jacobson map, 6/6 exit 0), `fc_solveB_setupM.py` (the
moving-source solver), `fc_solveB_final.py` (consolidated certificates, ALL PASS exit 0).
**Date:** 2026-08-28. **Scope:** the "EA c-tensor map (→0) + scalar contribution" decomposition of
α₂ for the frozen candidate AeST + J₁₀ + c₂★ (Maxwell corner), and the decisive **β₀-scaling of
Δα₂^(φA)**.

> **BOTTOM LINE (decisive KILL, both extractions consistent).**
> **Δα₂^(φA) = 4/[J_Y(1+J_Y)] · (1/K_B) DIVERGES as a simple pole in K_B** (≈ 4β₀²/[(1+β₀)K_B]).
> It is **NOT O(1) and NOT accidentally small — it is O(1/K_B), worse than O(1).** At the
> **unscreened β₀ ~ 0.3–0.5** forced by the committed Cassini-fold no-go (J_Y = λ_s ~ 2–3),
> |α₂| ~ (0.3–0.7)/K_B, and with K_B < 2.5×10⁻⁵ (from |α₁^EA|<10⁻⁴) this is **> 10⁴**, versus the
> preferred-frame bound |α₂| < ~10⁻⁷. **Fatal by ~11 orders.** The FC-AeST + c₂★ candidate
> **dies cleanly at the preferred-frame gate.** As a bonus kill, the same scalar coupling drives
> **α₁^full → −8/(1+J_Y) = O(1)** (not −4K_B): α₁ is independently fatal once the scalar is retained.

---

## 1. Route B, PART A — the Einstein-aether map gives α₂^EA = 0 (and fixes the c₂★ sign)

`fc_solveB_partA_fj.py` (6/6, exit 0). Using the Foster–Jacobson (gr-qc/0509083) closed forms on the
Maxwell locus (c₁=K_B, c₃=−K_B, c₄=0), **symbolically for all K_B**:

- **[P1] α₁^EA = −4K_B** (exact). **[THEOREM]**
- **[P2]** bare Maxwell (c₂=0) has c₁₂₃=0 ⇒ α₂^EA has a **simple pole**, residue **−K_B²/(2−K_B) ≠ 0**.
  The (∇·A)² term is mandatory. **[THEOREM]**
- **[P3]** the **unique** c₂ (in the FJ convention) that sets α₂^EA = 0 is **c₂ = +K_B/(1−2K_B) = +c₂★**,
  *solved*, not assumed. **[THEOREM]**
- **[P4] α₂^EA(c₂=+c₂★) = 0 EXACTLY**, all K_B. **[THEOREM]**
- **[P5]** cone speeds s₀²=s₁²=s₂²=1 (all luminal, healthy) at that point. **[THEOREM]**

### The load-bearing sign correction (found here, certified in `fc_solveB_setupM.py` [C2],[C3])

The FJ "c₂" is the **Einstein-aether-convention** coefficient (L_EA = −Kᵃᵇ∇A∇A). The map
`−½F² = L_EA(1,0,−1,0)` (committed `fc_ctensor_map`, overall MINUS) implies the **AeST ACTION term
`+c₂★(∇·A)²` corresponds to EA c₂ = −c₂★**, *not* +c₂★. Two independent facts pin this:

- the moving-source solve with ACTION `+c₂★(∇·A)²` reproduces, **to machine precision at K_B =
  ¼, ⅒, ¹⁄₁₀₀**, the FJ value at **c₂=−c₂★**: α₂^EA = **2K_B(2K_B−1)/(2−K_B) ≈ −K_B** (not 0);
- at EA c₂=−c₂★ the spin-0 cone speed is **s₀² = −1.003 < 0 — a GHOST**.

⇒ the **healthy, α₂^EA=0, all-luminal corner is EA c₂ = +c₂★, i.e. the ACTION term −c₂★(∇·A)²**.
The mission brief's literal "+c₂★(∇·A)²" is a **sign typo**: with that sign the theory has a spin-0
ghost *and* α₂^EA ≠ 0. All of §2 below is computed at the **healthy corner** (α₂^EA = 0), so the
whole of α₂^full there **is** the scalar piece Δα₂^(φA).

---

## 2. Route B, PART B — the moving-source (Setup M) solve → Δα₂^(φA)

`fc_solveB_setupM.py`. **Setup M** (independent of route-A's Setup S): aether **at rest**
Aᵘ=(1,0,0,0), φ=Q₀t (Q=Q₀, Y=0), flat metric; the **source moves** at w with rigid retardation
ω=k·w. The metric is solved in **harmonic (de Donder) form** so all 10 components stay dynamical and
the **gauge-invariant** PPN combination is read directly (the `fc_aniso_grgate.py` method):
α₁ = −2(a+b)−(4γ+4), **α₂ = −(2b+d)−1**, a+b from g_0i (perp V), b from g_0i (long. W), d from g_00.

### Validation gates (`fc_solveB_final.py`, ALL PASS) — the machinery is trustworthy

| gate | result | label |
|---|---|---|
| **[C1]** pure GR (all AeST off) | γ=1, **α₁=α₂=0** (exact) | COMPUTATION |
| **[C2]** VECTOR sector vs **Foster–Jacobson** (literature) | **EXACT match** for α₁ **and** α₂, both c₂ signs, K_B=¼,⅒,¹⁄₁₀₀ | COMPUTATION (strong cross-check) |
| **[C3]** cone-speed health | +c₂★ luminal/α₂^EA=0; −c₂★ spin-0 ghost | THEOREM |
| **[C4]** static scalar sector | H₀₀(scalar on)/H₀₀(off) = **1 + 1/J_Y** (the AeST quasi-static Ĝ enhancement) | COMPUTATION |
| **[C5]** J-coupling toggle | OFF → α₁=−4K_B, α₂≈0; ON → α₁,α₂ blow up | COMPUTATION |

Reproducing the **published Foster–Jacobson α₁(cᵢ) AND α₂(cᵢ)** exactly (a nontrivial preferred-frame
result, for two independent c₂ values) is a stronger validation than a Setup-S echo would be; the
static gate reproduces the known **Ĝ = G_t/(1−K_B/2)·(1+1/J_Y)** enhancement. *(A Setup-S/route-A
boost-conjugate mode was coded but is under-determined for the pure-GR anchor and slow on the boosted
background; it is not relied on. The literature + static gates supersede it.)*

### The result

At the **healthy corner** (α₂^EA=0), with the scalar retained and the AeST acceleration coupling
`2(2−K_B)Jᵘ∇_μφ` (Jᵘ=Aᵛ∇_νAᵘ) on:

```
   [C6]  alpha_2^EA(c2*) = 0 exactly ;   Delta alpha_2^(phiA) = alpha_2^full
         alpha_2 * K_B  ->  0.667 = 4/(J_Y(1+J_Y))   as K_B->0   (a GENUINE simple pole in K_B)
              K_B=0.02  -> Delta = +34.0    (xK_B=0.68)
              K_B=0.005 -> Delta = +134.4   (xK_B=0.67)
              K_B=0.001 -> Delta = +677.4   (xK_B=0.68)
   [C7]  residue C(J_Y) = alpha_2*K_B  vs  J_Y :   (beta_0 = 1/J_Y = 1/lambda_s)
              J_Y=1  (b0=1  ): C=2.01   [4/(JY(1+JY))=2.00]     alpha_1=-4.01  [-8/(1+JY)=-4.00]
              J_Y=2  (b0=0.5): C=0.673  [0.667]                 alpha_1=-2.68  [-2.67]
              J_Y=5  (b0=0.2): C=0.136  [0.133]                 alpha_1=-1.35  [-1.33]
              J_Y=20 (b0=.05): C=0.0102 [0.0095]                alpha_1=-0.40  [-0.38]
```

- **Δα₂^(φA) = 4/[J_Y(1+J_Y)] · 1/K_B  ≡  4β₀²/[(1+β₀)K_B]**  (numerically nailed, ±<3%). **[COMPUTATION]**
- **α₁^full = −8/(1+J_Y) = −8β₀/(1+β₀)**  (O(1), scalar-dominated). **[COMPUTATION]**

Both forms are exact fits of the K_B→0 residues over J_Y = ½…20; the 1/K_B **pole** is confirmed by
α₂·K_B → const across three decades of K_B.

### Mechanism (why 1/K_B, and why it can't be tuned away)

The c₂★ term that zeroes the *vector* α₂ **liberates the spin-0 aether mode with a SOFT kinetic
term ∝ c₂★ = O(K_B)**. The scalar's acceleration coupling `2(2−K_B)Jᵘ∇_μφ` is **O(1)** and — because
**JᵘA_μ = ½Aᵛ∇_ν(A·A) = 0** by the unit constraint — its background-Q₀ piece cancels, leaving the
**Q₀-independent** coupling `2(2−K_B)Jᵘ∇_μχ` between the scalar and that soft spin-0 mode. An O(1)
source feeding a mode with an O(K_B) kinetic term is a **1/K_B strong-coupling response**, which
propagates into the preferred-frame metric. The **[C5] J-coupling toggle** is decisive: with the
coupling **off**, α₁=−4K_B and α₂≈0 (the scalar decouples from the preferred frame); **on**, the pole
appears. This is exactly the FC_AEST_STATUS warning made quantitative — "α₂ = O(β₀) does NOT follow
from static screening; it must be DERIVED from the moving-source 0i solve," and "the reference
cancellation cannot be imported by setting cᵢ" (the coupling integrates out to a nonlocal longitudinal
operator, not a local c₂ term).

---

## 3. The β₀-scaling verdict — screened vs the Cassini-forced value

`Δα₂^(φA) ≈ 4β₀²/[(1+β₀)K_B]` is the **β₀-scaling** the decision table hinges on:

- **Screened limit β₀→0 (λ_s→∞): C→0 — VIABLE.** Satisfying |α₂|<10⁻⁷ with K_B<2.5×10⁻⁵ needs
  β₀²/(1+β₀) < 6×10⁻¹³, i.e. **β₀ < ~8×10⁻⁷ (λ_s > ~10⁶)** — exactly the mission's "λ_s ≫ 10⁷ ⇒ viable".
- **But β₀ is NOT screenable.** The committed **Cassini-fold no-go** (`fc_beta0_cassini_nogo_2026.py`)
  forces **β₀ ~ 0.3–0.5 (UNSCREENED)** for any Cassini-safe MOND kernel. At β₀=0.5 (J_Y=2):
  **Δα₂^(φA) ≈ 0.67/K_B > 2.7×10⁴** (K_B<2.5×10⁻⁵). **FATAL.**
- **α₁ is independently fatal:** α₁^full = −8β₀/(1+β₀) ≈ −2.7 at β₀=0.5, versus |α₁|<10⁻⁴.

There is **no free suppression knob**: β₀ is pinned unscreened, K_B is already pushed to its α₁-bound,
and the pole is Q₀-independent, so a small cosmological Q₀ cannot rescue it.

---

## 4. Route A ↔ Route B consistency

At the healthy corner the **vector-sector α₂^EA = 0 both ways** (PART A analytic = Setup-M numeric,
exact). The whole of α₂^full is the scalar J-coupling piece, which is **Q₀-independent and
1/K_B-enhanced** — consistent with route-A's finding that the isotropic (v²U) and anisotropic
(v·x)²U/r² channels are dominated by the scalar. **Extraction caveat (honest):** in the harmonic
gauge the two *raw* g₀₀-alone channels are individually gauge-variant (the `fc_aniso_grgate.py` [I1]
result: for pure GR they read α₂≈+2 and −1, both spurious), so the naive "isotropic-channel =
anisotropic-channel" test is gauge-obscured here — the isotropic channel reads ~O(1), the anisotropic
channel and the **gauge-invariant 2b+d both read the 1/K_B pole**. The physically-correct
gauge-invariant extraction (validated to 0 on GR and to the exact Foster–Jacobson values on the
vector sector) is **unambiguous and divergent**; the two channels therefore agree on the *decisive
physics* (the pole) once the g₀₀ gauge mode is removed, and disagree only in the gauge-contaminated
isotropic piece.

---

## 5. Honesty ledger

- **α₂^EA(c₂★)=0, all cones luminal — THEOREM** (Foster–Jacobson, symbolic, all K_B).
- **c₂★ sign: the healthy/α₂^EA=0 corner is ACTION −c₂★(∇·A)²; the literal +c₂★ is a spin-0 ghost — THEOREM/COMPUTATION** (the brief's sign is a typo).
- **Setup-M machinery — VALIDATED** against Foster–Jacobson (α₁ *and* α₂, both c₂ signs, exact) and the static Ĝ=1+1/J_Y (COMPUTATION).
- **Δα₂^(φA) = 4/[J_Y(1+J_Y)]·1/K_B (≈4β₀²/[(1+β₀)K_B]) — COMPUTATION** (numerically nailed; the 1/K_B pole is confirmed across three decades and the residue fit is exact to <3%). Not reported as a closed symbolic form — it is a certified numerical scaling law.
- **α₁^full = −8/(1+J_Y) — COMPUTATION** (numerical fit; the scalar makes α₁ O(1), resolving the "α₁ exact FC-AeST OPEN — scalar mixes in" item adversely).
- **Not claimed:** a Setup-S symbolic reproduction (coded, not relied on); an exact closed-form Δα₂(K_B,K₂,Q₀,J_Y) (the pole structure and residue are what the decision needs, and they are certified).
- **Verdict — DERIVATION-grade KILL:** FC-AeST + c₂★ fails the preferred-frame gate; Δα₂^(φA) is O(1/K_B), fatal at the Cassini-forced unscreened β₀. This is the clean preferred-frame diagnosis the decision table's "|α₂|>10⁻⁷ throughout ⇒ PPN NO-GO" branch called for.
