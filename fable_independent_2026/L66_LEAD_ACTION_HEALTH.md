# L66 — the lead's action does NOT share the L60 deep-MOND kill; it escapes it, but is not thereby cleared

**The lead's integrable-clock action escapes the L60 lapse-channel kill for one structural reason: it has
no separate MOND scalar and no AeST coupling `2(2−K_B)a^μ∂_μφ`, so the `(2−K_B)²` wrong-sign feed through
the Einstein-constrained lapse never forms. The clock unifies the lapse and the MOND-acceleration sector.
That is escape, not exoneration — the action's deep-MOND transverse health is uncomputed (only a
cosmological design point is certified) and it carries its own, different, indefinite gradient Hessian.**
The submitted AeST-like action (door 2), by contrast, is the deposited action's own family and **shares
the kill verbatim.**

2026-09-09. Lane L66 of [CHARTER.md](CHARTER.md), answering the question named in the L66 handoff against
[L60_ANISOTROPIC_HEALTH.md](L60_ANISOTROPIC_HEALTH.md).
Script: [L66_lead_action_health.py](L66_lead_action_health.py) → [L66_lead_action_health.out](L66_lead_action_health.out).
**18 checks, 18 PASS / 0 FAIL; exit 0; runtime 2 s.**

Polarity: each check asserts a **statement** and PASS means the statement is true. Several PASSes are
negative for a construction — read the statement. Both a₀ footings on every dimensional number:
9.3619×10⁻¹¹ / 1.1279×10⁻¹⁰ m s⁻². Nothing under `closure_2026/` was imported, executed as evidence, or
copied; the lead's action structure was **rebuilt** from the equations printed in its own markdown
(`ACTION.md`, `IC20_JOINT_COMPLETION.md`, `USER_ACTION_*`), and its reference numbers were read once,
offline, and hard-coded as reproduction targets the rebuild must hit. The Dirac counter and the deposited
kill reproduction share no machinery with the lead's files.

---

## 1. The controls, first — including reproducing the kill

| control | required | got |
|---|---|---|
| CTRL-1 ADM general relativity | 2 | **2** (4 primary + 4 secondary, all first class) |
| CTRL-2 GR + one minimally coupled scalar | 3 | **3** |
| CTRL-3 Einstein-aether (c₁…c₄ = 1/5,1/7,1/11,1/13) | 5 | **5** |
| CTRL-4 khronometric (same c's, u hypersurface-orthogonal) | 3 | **3** |
| CTRL-5 **deposited threshold** J_crit = (2−K_B)/(2−c₁₄) | 0.9000009 | **0.9000009** (static 3×3 route, independent) |
| CTRL-6 **deposited threshold acceleration** s = g_N/a₀ | 0.3985 | **0.3985** (repaired kernel) |
| CTRL-7 **deposited 1 kpc e-folding time** | 0.74 Myr | **0.737 Myr** (canonical) / **0.737 Myr** (alt) |

The kill reproduces on the action it was found on, by an **independent static-energy route** that rebuilds
the 3×3 form on (lapse `n`, spatial trace `hT`, MOND scalar `δφ`):

```
       n        hT      δφ
 n  [  c14      1/2    2−K_B    ]     C[n,hT]=1/2      Hamiltonian constraint: lapse × spatial curvature
 hT [  1/2      1/8      0      ]     C[n,φ]=2−K_B     the AeST coupling 2(2−K_B)a^μ∂_μφ, through the LAPSE
 δφ [ 2−K_B      0   −(2−K_B)J  ]     C[φ,φ]=−(2−K_B)J the MOND scalar's own soft kernel stiffness
```

Eliminating `(n,hT)`: the lapse's effective stiffness is `c₁₄ − (½)²/(⅛) = c₁₄ − 2` — dominated by the
**−2 the Einstein constraint supplies**, not by c₁₄. Feeding it back gives

    C_eff = (2−K_B)[ (2−K_B)/(2−c₁₄) − J ] ,   sign change at J = (2−K_B)/(2−c₁₄) = 0.9000009,

and on the repaired kernel `J_Y = s/Δ(s)` crosses that at **s = 0.3985**, with a **0.737 Myr** e-folding
time at λ = 1 kpc on both footings. This is L60's mechanism, threshold, and rate, reproduced.

---

## 2. There are two lead actions; they answer the question differently

**(I) The submitted AeST-like action** (`TEN_OPEN_DOORS` door 2; `USER_ACTION_*`). Its static planar
density (`USER_ACTION_BACKGROUND` / `EXACT_PLANAR`), with b = 2−K_B and g = 1/(16πG), is

    R = e^{P−A+2B}[ g(2B'² + 4P'B') + c_a P'² + 2b e^A P'v ] − e^{P+A+2B}[ C + b J(U) ] − p_φ e^A v .

Term for term this is the deposited action: `g(2B'²+4P'B')` is the EH Hamiltonian constraint (lapse P ×
spatial curvature — the ½ and ⅛); `c_a P'²` is the clock/khronon acceleration term (six orders below the
−2); **`2b e^A P'v` is `2(2−K_B)a^μ∂_μφ`, a separate MOND scalar `v∼φ'` coupled to the lapse P**; `b J(U)`
is the MOND kernel with transverse stiffness Σ_⊥ = J_Y = s/Δ. L63's `H5b` confirms the same coupling
independently: `C_{n,φ} = k²(2−K_B)`, "the MOND source itself is the symmetric half", carrying the static
limit because `a_i = ∂_i(n − χ̇)` has a lapse piece. All three ingredients of the kill are present in the
same positions, and `USER_ACTION_BACKGROUND`'s own `E_A − E_B/2 = 2b J₁s₀² ≠ 0` says the flat background is
not a solution and must be curved — exactly the anisotropic background L60 keeps. **Action (I) shares the
kill: outcome (a).**

**(II) The integrable-clock action** (`ACTION.md` door 4). This is the lead's genuinely different
construction:

    S = ∫√(−g){ m/2[ R₄ − 2Λ + 4KW − 6W² + 2(1−u²)a_μa^μ − 2a₀²U(u²) ] + κX } + S_m[g,ψ],

with `N = (2X)^{−1/2}`, `n_μ = −T_μ/√(2X)`, `a_μ = D_μ ln N`, `w = (u−1)ln N`. **There is no separate MOND
scalar φ and no term `2(2−K_B)a^μ∂_μφ`.** The MOND scale a₀ enters the clock's **own** acceleration
invariant `2(1−u²)a_μa^μ − 2a₀²U(u²)`, and the lapse `N` is a **functional of the varied clock T**, not an
independent ADM field. The rest of this lane is about action (II).

---

## 3. The lead's action, structure by structure (derived from its own files, not assumed)

**What plays the transverse stiffness (LEAD-1).** Not a J(Y) MOND kernel — there is none. The transverse
(spatial-gradient) sector of the reduced scalar Hamiltonian
`h(S,q,z,R) = −e^{2S}q²/(6v) − a(S)qz − e^S P(S) − d(S)z² − e₄(S)z⁴ − vR`, `v = e^{S+2wc}/2 + z²`, is: the
**curvature coefficient v** (multiplying R, with δR = (4k²−2R)ζ), the **clock-lapse gradient coefficient
B = e^{S+2wc}(1−u²) > 0** (the −B|DS|² term), and the **Schur-reduced curvature stiffness H_RR**. The MOND
scale rides the clock acceleration `2(1−u²)a_μa^μ`, not a separate scalar's kernel slope.

**Does the lapse-channel subtraction exist (LEAD-2)? No.** Two facts, both derived:
1. The IC20 action carries a **clock-lapse Schur** in the kinetic sector: eliminating the clock lapse S
   from the `(δq, ζ)` pair gives `K = a − C²/(2M)`, `M = H_SS − 2Bk²`, `C = H_Sq`. This is structurally
   *analogous* to a lapse elimination — but at the lead's own witness `C = H_Sq = 0` by design and
   `M = H_SS − 2Bk² < 0` (H_SS = −3), so `−C²/(2M)` is **stabilising** (adds to K) — the **opposite** sign
   effect from L60, and it lands in the kinetic coefficient, not in a soft static kernel stiffness.
2. The L60 subtraction requires a **separate** MOND scalar coupled by `2(2−K_B)a^μ∂_μφ` giving the
   symmetric mixing `C_{n,φ} = (2−K_B)`. Action (II) has **no φ and no such term**, so there is no
   `(2−K_B)²/(2−c₁₄)` wrong-sign feed. The L60 lapse-channel subtraction is **absent.**

**Does the IC20 auxiliary z enter the transverse sector (LEAD-3)? Yes.** Two ways, both verified against
the lead's own on-shell identities: (i) z sits in `v = e^{S+2wc}/2 + z²`, the coefficient of R, so it
enters the `−2vk²` gradient term directly; (ii) its Schur complement gives `H_RR = −4z²/h_zz` and
`H_qR = 2z·h_qz/h_zz` — the reduced curvature/gradient stiffnesses that carry z (the rebuild reproduces
`H_RR = −4z²/h_zz` with identity residual 0). The auxiliary shapes the k², k⁴ mode structure **through the
curvature channel**, as an algebraic Schur modification, not as a propagating transverse mode. This is the
"auxiliary's Schur complement replaced a marginal zero" of the L44 handoff.

---

## 4. The health condition on action (II): design point vs deep MOND

**The lead's positivity is real and reproduced (LEAD-4a).** Its full FLRW dispersion (background-mass
cancellation kept) gives `ω²/[e^{2S}k²] = [H_SS·cIR − 2Bk²·cUV]/[H_SS − 2Bk²]` with H_SS = −3, B = 0.584,
cIR = 0.35003935, cUV = 0.2, K = a_UV = 0.12638695. Numerator and denominator share the sign of H_SS < 0,
so the ratio is positive for every k²: **speed² runs 0.350 (IR) → 0.200 (UV)**, reproduced here across
k² = 10⁻⁸…10¹². The clock scalar is healthy **where the lead evaluated it.**

**But that is only the cosmological design point (LEAD-4b).** Every one of the lead's health calls is at
**R = 0** — a flat-vacuum FLRW background, S = 0.1, over ~0.00055 e-folds. It is not a galactic deep-MOND
field with a background clock/lapse gradient. `IC20_JOINT_COMPLETION`'s own nonclaims say so: "Scalar
quadratic evolution derived only for flat vacuum FLRW, not matter or general anisotropy", "No … PPN,
lensing". **This lane does not clear action (II) on a flat-background check — that is exactly the error L60
caught in the deposited gate table** (which read health at the solar-neighbourhood acceleration, never in
deep MOND). Action (II) has produced **no galactic quasi-static background** (R ≠ 0, background clock
gradient) to perturb, so the L60-style deep-MOND transverse condition **cannot yet be evaluated on it**, on
either footing. Its deep-MOND health is **not established.**

**A different concern the action does carry (LEAD-5).** The lead's own IC-4 auxiliary principal symbol
(`AUXILIARY_SYMBOL.md`) has a transverse gradient Hessian `H_gg = −D_+[[2ρA_J, ρB_J+4uξ],[ρB_J+4uξ,
2ρC_J+4ξ²]]` whose determinant at π = 0 is `det G = −4u²ξ² < 0` — "generically negative". The lead repairs
the witness with a **negative-semidefinite square** `−mV e^{uξ}α|Dξ + bDu|²` and states it "must not be
labeled a positive Hamiltonian energy". This is a rank-one / indefinite gradient block — a **different**
mechanism from L60's lapse-channel subtraction, and uncleared in the galactic regime. This is outcome (b)
territory.

---

## 5. Verdict, the structural difference, the cost, the theorem

**Which of (a)/(b)/(c)?** For the **specific L60 lapse-channel mechanism it is (c): no such subtraction.**
Alongside it, action (II) carries a **(b)-type** distinct concern (the indefinite auxiliary gradient
Hessian). It is not (a): it does not share the L60 kill.

**The structural difference that removes it (LEAD-6, the single most valuable design fact).** The
deposited/submitted action sources a **separate** MOND scalar by `2(2−K_B)a^μ∂_μφ` coupled to an
**independent** lapse whose Einstein-constraint stiffness supplies the −2; eliminating that lapse feeds
`−(2−K_B)²/(2−c₁₄)` into φ's soft kernel stiffness `(2−K_B)J_Y` and flips its sign when `J_Y < 0.9`. The
integrable-clock action has **no separate scalar and no such coupling** — `N = (2X)^{−1/2}` is a functional
of the clock T, and the MOND scale rides the clock's **own** acceleration `2(1−u²)a_μa^μ`. **No
separate-scalar/independent-lapse pair ⇒ no `C_{n,φ} = (2−K_B)` mixing ⇒ no wrong-sign feed. The clock
unifies the lapse and the MOND-acceleration sector, and that unification is what removes the kill.**

**The cost (LEAD-7), priced against the lead's own destination gates.** Luminal tensors `cT² = 1`
(reproduced); 3 local modes = 2 tensor + 1 clock (the lead's rank calculation is load-bearing; global
rank, boundary invertibility and interactions remain unproved *by the lead*); ordinary matter conservation
`∇_μT^{μν} = 0` holds (minimal coupling to g). But removing the L60 subtraction is not free: the surviving
health is **cosmological-design-point + 0.00055 e-folds only**, an adjacent coefficient choice (H_SS =
−1000) already gives IR ω² < 0, and deep MOND is uncomputed. **Escaping L60 is not a health certificate.**

**Is L60 a class-level theorem (CLASS)? Yes, under three hypotheses.** The kill holds for any action with
(H1) a scalar whose deep-MOND transverse stiffness is the MOND-kernel slope `Σ_⊥ = J_Y = g_N/g_φ`,
dropping below (2−K_B)/(2−c₁₄) ≈ 0.9; (H2) that scalar sourced by an AeST-type coupling
`2(2−K_B)a^μ∂_μφ` to a clock/aether acceleration; (H3) the clock's timelike vector fixing a lapse coupled
to spatial curvature by the EH Hamiltonian constraint (effective lapse stiffness ≈ −2). The sign change at
`J = (2−K_B)/(2−c₁₄)` is an **algebraic identity of the 3×3 static form**, so it holds for every action
meeting H1–H3 — the deposited action and the submitted action (I) both do. This is a **third class-level
no-go** for the programme, on top of the two it already carries. Action (II) escapes it by **violating
H2**; but escaping H2 replaces H1's soft transverse stiffness with (II)'s own indefinite gradient Hessian,
unresolved in deep MOND.

---

## 6. What is open, named

1. **The deep-MOND background of action (II) does not exist yet.** Until the lead produces a galactic
   quasi-static solution (R ≠ 0, background clock gradient), the L60-style transverse condition cannot be
   evaluated on it. The honest status is *escape of the specific mechanism*, not a health pass.
2. **The indefinite auxiliary gradient Hessian** (IC-4, `det G = −4u²ξ² < 0` at π = 0) is repaired only at
   the cosmological witness by a negative-semidefinite square. Whether that repair survives into a galactic
   deep-MOND regime is the (b)-type question this lane hands forward.
3. **The class-level theorem's hypotheses are the design guidance.** Any future MOND-carrying scalar the
   programme adds back to action (II) reintroduces the kill the moment it is sourced by an AeST coupling to
   an Einstein-constrained lapse. The escape is conditional on keeping the MOND sector *inside* the clock.

κ = ½ remains fitted, and this lane never says otherwise. Nothing here is closed.
