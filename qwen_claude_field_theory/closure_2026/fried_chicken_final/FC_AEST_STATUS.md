# FC-FINAL — session capstone: the constraint-first no-go + AeST+J₁₀ conditional closure (2026-08-28)

> ## ⛔ 2026-08-29 — α₂ RESOLVED = PPN-KILL. STANDING FLIPS: `CONDITIONALLY CLOSED / PPN-OPEN` → **`PPN-KILLED (preferred-frame)`.**
>
> The decisive scalar-retained anisotropic O(w²) 1PN α₂ (the "last lock", §"one remaining calculation" below) is **DONE**, by
> **two independent GR-validated 1PN solves that AGREE** (workflow wmqmofvp4, run wf_c7afe60e-738, 4 agents; committed 66cf94e5
> in `fc_alpha2_aniso/`). **The AeST scalar does NOT regularise the c₁₂₃=0 Einstein-aether α₂ pole — it ADDS a fresh 1/K_B pole.**
> - **Route A** `fc_alpha2_aniso/fc_solveA_setupM.py` (direct anisotropic O(w²) coupled solve; FP linearized-Einstein EH
>   `L_EH=−½h·G^(1)` — verified `√−g R|_ε² == −½h·G^(1)`, EOM ratio EXACTLY −1 — + full covariant dark sector incl. c₂★(∇·A)²;
>   **the O(ε²) unit-constraint temporal piece b₀ retained = THE blocker that defeated every prior attempt** incl. the incomplete
>   `fc_alpha2_scalar_retained.py`; harmonic gauge after field eqs, gauge-invariant `2b+d` extraction):
>   **α₂ = 1/λ_s + 2/(K_B·λ_s²)**, α₁ = −4K_B + O(1/λ_s). Gates ALL PASS (dark OFF→GR α₁=α₂=0 exact; EA+c₂★ Maxwell corner
>   scalar-OFF→α₁=−4K_B & α₂=0 EXACTLY all K_B; 107s).
> - **Route B** `fc_alpha2_aniso/fc_solveB_final.py` (EA c-tensor map — machinery **validated to reproduce PUBLISHED
>   Foster–Jacobson EA α₁ AND α₂ exactly**, both c₂ signs — + independent moving-source Setup-M solve):
>   **α₂ = 4/(J_Y(1+J_Y)·K_B)**, α₁ = −8/(1+J_Y). Both routes agree to a factor ~1.3; both a **simple 1/K_B pole**.
>
> **The kill (CORRECTED reasoning, 2026-08-29 — supersedes the "fold-forces β₀~0.5" line, which was a CONFLATION):** the parameter
> λ_s in α₂=1/λ_s+2/(K_B λ_s²) is the **AeST asymptotic-slope screening parameter** — λ_s = lim_{Y→∞} 𝒥/Y, β₀≡1/λ_s (MNRAS 531,272
> defn) — NOT the local constitutive derivative J_Y(Y_SS). **For frozen J₁₀ this slope is EXACTLY 1 (VERIFIED sympy: 𝒥_Y=1−e^{−√Y/a₀},
> so 𝒥→Y−2a₀², lim 𝒥/Y=1 ⇒ λ_s=1, β₀=1).** Hence **α₂ = 1 + 2/K_B ≈ 8×10⁴** at K_B<2.5×10⁻⁵ — over |α₂|<10⁻⁷ by ~11 orders. The
> screening escape (λ_s≫1) is UNAVAILABLE to this kernel because its asymptotic slope is pinned to 1.
> **⚠️ The script `[RESULT]` line "λ_s=J_Y=2g_bar/a₀~1.3e8 → α₂~8e-9 PASSES" is a VARIABLE-IDENTIFICATION ERROR** (J_Y=1−e^{−u}∈[0,1)
> can NOT equal 2g/a₀; the huge quantity is J_Y/(1−J_Y)=e^{u}−1, which is NOT λ_s). Do not use that PASS reading. **α₁** likewise:
> −4K_B is the pure-VECTOR value (Route A reproduces it exactly scalar-OFF); the scalar's `2(2−K_B)J·∇φ` acceleration coupling shifts
> it to O(1) at finite λ_s (α₁=−8/(1+J_Y)~−2.7, Route B) = an independent kill. **NOTE the verdict flip-flopped (KILL→OPEN→KILL) once
> during derivation on exactly this λ_s-vs-J_Y notation ambiguity; it is now settled by the symbolic λ_s=1 check — DON'T re-open it
> on the screened-PASS line.**
>
> **SCOPE (honest):** kills the specific frozen **FC-AeST + c₂★** chassis at the PREFERRED-FRAME gate. **STATIC sector untouched:**
> γ_PPN=1, Φ=Ψ lensing, c_T=1, BTFR, 6-DOF, Cassini-μ₁₀ all still stand (Parts I–II below unchanged). **J₁₀ never failed** — this
> kill is the AeST vector+scalar preferred-frame structure, kernel-independent. Everything below is the (now-superseded) pre-α₂
> "conditionally closed" record; read it as the road that led here, not the current verdict.

---

**Frozen candidate under test:** FC-AeST = AeST (Skordis–Złośnik, 6 physical DOF) + `𝓕(Y,Q)=𝓕_Q★(Q)+a₀²J₁₀(√Y/a₀)`,
`μ₁₀(y)=y/(1+y¹⁰)^{1/10}`, **a₀ constant**. Matter minimally coupled to the single metric g. All verdicts below are backed
by committed, re-run scripts in `fried_chicken_final/` (and subdirs) unless marked EXTERNAL-INPUT.

---

## Part I — The constraint-first 2-DOF program is closed on the lensing axis (scoped no-go, verified)

Every attempt to realize relativistic MOND with only **2 gravitational DOF** (a constraint-first / MMG chassis) fails to lens,
by a single unified mechanism (`fc_isotropic_legendre/`, `fc_final_4ac/`, `fc_no_go_Hperp_unsources_Phi.py`; 37/37 + 28/28 + 14/14 + 12/12, all exit 0):

> **THEOREM (scoped).** An isotropic MOND law couples to the metric only through `s=√(γ^ij D_iq D_jq)`, so the *same* constitutive
> object `μ=J'/s` controls both the AQUAL Gauss law and the on-shell traceless metric stress `Σ_P`. Both exhaustive local classes
> force `Σ_P≠0`: covariant/QUMOND carrier → `Σ_P=−μs²`; lapse-tied 4-AC → `Σ_P=yμ'`, slip `(μ+yμ')/μ: 1→3/2→2`.
> `Σ_P=0 ⟺ μ=0` (no MOND) or `μ'=0` (linear). **⇒ Φ≠Ψ is forced in every local ≤2-derivative 2-DOF constraint MOND construction.**

This subsumes the three earlier no-gos (source-free γ_PPN=0; lapse-slip; covariant carrier). **Scope (honest):** local, action-based,
≤2-derivative, second-class/Legendre class. **Two flagged open residuals** (NOT "theory closed"): a fully general symmetric-tensor
Lagrange multiplier forcing Φ=Ψ (only the mimetic instance certified to add a dust DOF); and the non-local QUMOND-as-phantom-density route.

**Why AeST escapes (the mechanism, derived):** AeST reaches Φ=Ψ with the *same* yμ' Hessian because its MOND invariant contracts with
the **metric-independent aether-orthogonal projector** `h^μν=g^μν+A^μA^ν` (A unit-timelike); at O(ε²) zero metric-shear coupling, the
cancelling traceless stress carried by the **transverse aether mode** (∝Q=A^μ∂_μφ, →0 as A→0). Cancelling Σ_P *requires* a field with
independent traceless stress = unit-timelike vector + transverse mode = **4 extra DOF → 6, not 2**. **The 6 DOF are exactly what sources
correct lensing.** So AeST+J₁₀ is not just *a* surviving candidate — it is essentially the *necessary* form.

---

## Part II — FC-AeST + J₁₀: CONDITIONALLY CLOSED (all derived gates pass; α₂ + finite-k characteristic are the named unproved gates)

| Gate | Verdict | Basis / provenance |
|---|---|---|
| Exact J₁₀ MOND interpolation, BTFR `v⁴=G_N M a₀` | **PASS** | committed (fc8) |
| Φ=Ψ (weak-field, incl. non-spherical) | **PASS** | AeST reduction; M24 KiDS RAR χ²/dof=0.64 @ canonical a₀ (`fc_lensing_rar_mu10_2026.py`) |
| c_T = 1 (GW170817) | **PASS** (exact, kernel-indep) | committed |
| 6 nonlinear DOF (4 FC + 4 SC) | **PASS** | EXTERNAL-INPUT (PRD 110.044015) |
| δ²J₁₀ on FLRW (Y=0) | **= 0** | J₁₀=O(Y^{3/2})=O(δφ³); F_YQ=0 (separable) ⇒ MOND sector does NOT contaminate the quadratic FLRW Hessian; F_YY→∞ is a Y-chart coordinate feature |
| IR low-k mode (k<k*) | **nonpropagating** (`ω_Y=0`, Jeans-like constraint mode), NOT a propagating ghost | EXTERNAL-INPUT (2109.13287) + `fc_flrw_ir_sign_certificate.py` 20/20 |
| de Sitter k→0 dilution | **PASS** (repair argument, NOT an all-k theorem): χ bounded, `E=Π²/(2K₀)a⁻³→0` even for K₀<0 | `fc_flrw_ir_sign_certificate.py` |
| Healthy scalar region | **nonempty** `c_s²=(2−K_B)(1+K_Bλ_s/2)/(K₂K_B)`; e.g. (K_B,λ_s,K₂)=(0.1,1,20)→c_s²≈0.998 (subluminal) | DERIVATION |
| Healthy vector region | **PASS** `ω_V²=k²+(2−K_B)(1+λ_s)Q₀²/K_B>0` for 0<K_B<2 | EXTERNAL-INPUT (2109.13287) |
| **α₁ exact FC-AeST** | **RESOLVED (2026-08-29) → α₁ = −8/(1+J_Y) ~ −2.7 (O(1)) = KILL** (pure-vector −4K_B shifted by the J·∇φ coupling) | see top banner; `fc_alpha2_aniso/fc_solveA_setupM.py`, `fc_solveB_final.py` |
| **α₂ exact FC-AeST** | **RESOLVED (2026-08-29) → α₂ = 1/λ_s + 2/(K_B·λ_s²) ~ 2×10⁴ at forced β₀~0.5 = KILL** (1/K_B pole; scalar ADDS not cancels) | see top banner; two independent GR-validated 1PN solves agree |
| Full finite-k FLRW characteristic matrix (H≪k<k*) | **OPEN** | the exact time-dependent K/B/Ω not certified |

**Key structural facts that make α₂ the *whole* game:** in the Solar System `1−μ₁₀~1/(10y¹⁰)~10⁻⁴⁰`, so J₁₀ is negligible there ⇒
**the preferred-frame parameters are pure AeST-background — no kernel tweak (10→8→12) can touch α₁,α₂.** And there is *no PPN no-go*: a
closely-related scalar-Einstein-aether theory has an **exact α₁=α₂=0 surface over a nonempty, positive-energy region** (the scalar is
retained, not discarded), so "healthy aether+scalar ⇒ α₂≠0" is **false**. But that precedent is *not* an AeST derivation — the AeST-specific
`f₁,f₂` must be computed. As of this session the `fc_alpha2_scalar_retained.py` derivation is **incomplete** (fails an intermediate
unit-constraint check; no final f₁,f₂ emitted) — so **α₂ remains genuinely underived**, and no α₂=0 may be claimed.

---

## Why μ₁₀ specifically (empirical, committed): Cassini selects the sharp kernel
The exponential-kernel FC-AeST is **KILLED by the Solar-System Cassini/EFE phantom quadrupole** — μ=1−e⁻ʸ gives Q₂/ceiling=**3.76×**
(FAIL), RouteA/MS08 6.23× (FAIL), FC-tanh 6.09× (FAIL). The sharp family μ_n=y/(1+yⁿ)^{1/n} PASSES for n≥4: μ₅=0.31×, **μ₁₀=0.06×
(comfortable PASS)** (`FC_AEST/scripts/fc_cassini_quadrupole_2026.py`, committed; verified this session). **The structural trap:** the gradual
(exponential) transition that removes the old ks/(1−2s) pole is the SAME shape that maximizes the phantom quadrupole — one kernel can't do both;
only a sharp μ_n clears Cassini. So **μ₁₀ is the empirically-selected kernel**, not just tolerated: it is the safest Cassini member of the
surviving family. (Liabilities inherited: RAR scatter 0.108→0.123/0.127 dex; the registered wide-binary γ_v discriminator = the empirical
falsifier, DR4.) The exponential branch is retired; the 2-DOF constraint-first branch stays dead (Part I).

## The c₂ preferred-frame repair candidate (VERIFIED reference sector; full-AeST OPEN)
To address α₂, add a direct `c₂(∇_μA^μ)²` term with **c₂=K_B/(1−2K_B)** on the Maxwell locus (c₁=K_B, c₃=−K_B, c₄=0), K_B<2.5×10⁻⁵.
**Reference Einstein-aether sector — VERIFIED by sympy this session:** `α₁=−4K_B, α₂=0 EXACTLY, c_T²=c_V²=1, c_S²∈[1−K_B,1]` (healthy,
~luminal, non-superluminal; positive kinetic coefficients). **But this is NOT the full AeST answer** (Carl): the scalar (Q=A^μ∇φ, the
J^μ∇φ acceleration coupling) contributes `α₂^full = α₂^ae(=0) + Δα₂^(φA)`, and **the c₂ term changes the constraint structure — the 6-DOF
count must be RE-DERIVED** (c₁₂₃=0→c₂ liberates the spin-0 aether mode; possible 7th DOF/ghost). The Sagi 2009 generalized-TeVeS PPN
calculation (arXiv:0905.4001) proves scalar-aether α₁=α₂=0 is achievable in a finite region ⇒ **no general PPN no-go** — but it does not
place AeST on that surface. **Final-oven decision table** (running workflow wu1m3w9nx): 6-DOF + |α₂|<1e-7 + healthy finite-k ⇒ GOLDEN CORNER;
6-DOF + |α₂|>1e-7 throughout ⇒ PPN NO-GO; extra-DOF/degenerate Hessian ⇒ REPAIR FAILS; can't complete from the exact action ⇒ α₂-OPEN.
The decisive quantity is the **β₀-scaling of Δα₂^(φA)**: O(β₀)/O(K_B Q₀) screened (λ_s≫10⁷) ⇒ viable; O(1) ⇒ dies. J₁₀ is out of this calc.

## The one remaining calculation (the last lock)

$$\text{Derive } f_1=\alpha_1^{\rm AeST}(K_B,K_2,\lambda_s,Q_0),\ f_2=\alpha_2^{\rm AeST}(K_B,K_2,\lambda_s,Q_0)\text{ from the full }(g,A,\phi)\text{ 1PN system, then intersect } f_1=0,\ |f_2|<10^{-7}\text{ with } \{0<K_B<2,\ K_2>0,\ \lambda_s>0,\ 0<c_s^2\le1,\ c_T=1\}.$$

- Intersection **nonempty** ⇒ FC-AeST+J₁₀ has a genuinely complete viable parameter point → **FRIED**.
- Intersection **empty** ⇒ FC-AeST+J₁₀ **dies cleanly at the preferred-frame gate** (a clean reason the 6-DOF structure wasn't enough).
- Not another architecture, not another kernel — a finite algebraic intersection problem.

## Verdict

> **FC-AeST + J₁₀ = CONDITIONALLY CLOSED / GOLDEN-CORNER CANDIDATE.** A viable parameter region exists at the level of every gate
> derived so far; the AeST-specific α₂ (decisive) and the full finite-k characteristic closure remain **unproved** — one of them (α₂)
> could still kill it. Crispy candidate, honestly conditional — not a fabricated "fully proven" theory.

## SESSION-END FROZEN VERDICT (2026-08-28)

**FROZEN CANDIDATE (stop modifying):** `AeST + μ₁₀`, with the `c₂(Q₀)=K_B/(1−2K_B)` term treated as a **TEST DEFORMATION**, not part
of the certified theory. Do not swap the kernel, do not architecture-hop.

**STATUS: `CONDITIONALLY CLOSED / PPN-OPEN`.** This is the exact point where the equations stop yielding a number without the full
moving-source calculation — not a fabricated closure.

What is genuinely established (banked, committed, verified this session):
1. **2-DOF constraint-first MOND: CLOSED on the lensing axis** — the unified secant/tangent anisotropic-Hessian no-go (Part I). AeST's
   6-DOF (aether) structure is precisely what evades it.
2. **AeST + μ₁₀ is the surviving architecture**, empirically Cassini-selected (μ₁₀ at 0.06× ceiling; exponential kernels FAIL 3.76–6.23×).
3. **c₂★ = K_B/(1−2K_B) is an EXACT reference-Einstein-aether cancellation** on the Maxwell slice (c₄=0): α₁=−4K_B, α₂=0, c_T=s₁=s₀=1
   (all cones luminal, positive kinetic) — verified `fc_maxwell_vs_c4_corner_2026.py`. **c₄=0 is the vector-health condition** (s₁²=c₁/c₁₄);
   the c₄≈−c₁ alternative is pathological (vector ~10⁴c).
4. **But this is the REFERENCE-aether locus, NOT a certified AeST locus.** The AeST scalar enters via the acceleration coupling
   `2(2−K_B)J^μ∇_μφ` (J^μ=A^ν∇_νA^μ), which integrates out to a NONLOCAL longitudinal operator, **not** a local `c₂(∇·A)²` — so the
   reference cancellation cannot be imported by setting c_i. The full answer is `α₂^full = 0 + Δα₂^(φA)`, and **Δα₂^(φA) is undetermined
   by any available AeST equation/literature** (no published scalar-retained AeST 1PN α₂ exists).
5. **Corrections banked (no manufactured claims):** (a) "adding c₂ liberates a 7th DOF" is NOT established — the Dirac rank of the
   repaired action is OPEN (6 or 7), must be recomputed, not assumed. (b) c₂(Q) shares the quadratic Hessian/DOF with constant c₂ but its
   1PN α₂ can differ (the O(δ³) term feeds the 1PN equations).

**THE ONE REMAINING DECISIVE CALCULATION (no algebraic shortcut):** the coupled scalar-retained moving-source 1PN solve
`(g_{0i}, A_i, φ)_1PN → α₂^AeST`, plus the repaired-action Dirac rank. Outcome: `Δα₂^(φA)<10⁻⁷` + nondegenerate rank + healthy
finite-k ⇒ FRIED; else a clean preferred-frame diagnosis. This is genuine unpublished frontier work (an agent-run attempt, wu1m3w9nx,
did not close it — consistent with α₂-OPEN); the legitimate next step is a dedicated multi-pass derivation adapting Sagi (PRD 80.044032)
to the J^μ∇φ coupling, NOT another one-line swing.

**Honest bottom line:** we are at the fryer control panel, not the plate. J₁₀ never failed anywhere — every kill this session was
architectural. AeST+μ₁₀ is the strongest defensible relativistic-MOND candidate the program has produced, frozen at CONDITIONALLY CLOSED
/ PPN-OPEN.

### The new-model endpoint (defensible publication claim, 2026-08-28)
The deformation `S_new = S_AeST[J₁₀] + (c⁴/16πG★)∫√−g · c₂★(∇_μA^μ)²` on the Maxwell locus
(c₁=K_B, c₃=−K_B, c₄=0, c₂★=K_B/(1−2K_B), K_B<2.5×10⁻⁵), with J₁₀ chosen so the observable quasistatic response is μ₁₀, **appears to
be a genuinely new AeST model** — a literature search (relayed) did not find this exact action/locus worked out. **Defensible claim (NOT
"we proved it viable"):** *this specific AeST deformation's Einstein-aether limit sits exactly on an α₂=0, c_T=1, all-luminal
(s₀=s₁=s₂=c) surface while retaining a sharp Cassini-safe MOND sector.* The open binary that no existing paper closes: **`rank H_new`
(repaired-action Dirac count, 6 or changed) and `α₂^new` (the full scalar-retained AeST 1PN coefficient).**

**Screening→α₂ existence argument — PROPOSED (two forms) then RETRACTED (honest, load-bearing):** the high-gradient AeST limit screens the
scalar (χ=β₀Φ̃, β₀=1/λ_s; equivalently the scalar gradient-Hessian ∝ λ_s makes δφ=O(1/λ_s)), which was argued to give `α₂^full = C/λ_s`
⇒ tunable → 0 for any finite C. **BOTH forms (β₀-screening and λ_s⁻¹-Hessian-scaling) are WITHDRAWN**, for one decisive reason: **screening
the STATIC scalar PROFILE (χ=O(β₀)) is NOT the same as suppressing the 1PN PREFERRED-FRAME coefficient.** α₂ is extracted from the moving-source
0i vector metric, whose equations carry derivatives of A_i, the background Q₀, and the inverse scalar operator O_φ⁻¹ — any of which can leave an
**O(1)** contribution even when the static scalar amplitude is O(β₀). So `α₂ = O(β₀)` does NOT follow from the screening; it must be DERIVED from
the full {E_0i, E_Ai, E_φ}_1PN solve. (Consistent: Skordis 2023 states nonzero α₁,α₂ are *expected* for AeST.) Secondary caveats also noted:
λ_s is entangled with μ₁₀ (can't dial β₀ holding μ₁₀ fixed), and β₀→0 forces K₂≳λ_s (extreme hierarchy, possible low EFT cutoff). **Net: there
is NO free suppression knob; α₂^new is genuinely UNRESOLVED — the actual 1PN calculation is the only arbiter.**

**The ONE remaining computation (no architecture left to invent, no parameter tweak substitutes):** the complete Sagi-style
(PRD 80.044032) moving-source 1PN reduction of `S_new` → the coefficient multiplying W_i (= α₂^new), plus `rank H_new`. Finite regular
C₂ + rank-6 ⇒ the chicken exists; a 1/β₀ enhancement, strong coupling, or rank change ⇒ clean kill. (Running: wbswygtm2.)
