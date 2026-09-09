# L87 — Is there a STIFF-FREE (linear-in-charge) dust in the F(Q)Θ family?

**Script:** `L87_stiff_free_dust.py` · **Output:** `L87_stiff_free_dust.out` · **Result:** 19/19 checks PASS
(each PASS = the stated claim is TRUE). Self-contained sympy/numpy; imports nothing from `qwen_claude_field_theory/`.
Controls first (reproduce astra's quadratic ρ, the `k₂=3f²/4M²` degeneracy, and L84's dust/stiff split). Both a₀
footings on every dimensional number — a₀ is absent from the FLRW K/charge algebra, so both give bit-identical
results (demonstrated, check **P6**).

## Verdict — one line

**NO stiff-free dust exists within the healthy F(Q)Θ family. The square (the a⁻⁶ stiff partner) is STRUCTURAL, so
the L84/L86 ~24-order BBN fine-tuning is INTRINSIC, not a removable artefact of one action choice.** Every way to
linearise the dust either deletes the dust, breaks the metric–scalar braiding, or turns the clock into a
non-propagating constraint field. The only genuinely stiff-free dust is a *separate* `ρ=mn` fluid — external CDM,
which re-imports the L61 excess-spent-once overshoot and abandons the one-action structure.

## The problem (L84/L86, reproduced faithfully — checks C0–C2)

astra's F(Q)Θ affine action gives, on flat FLRW, `ρ = B + 3M²H² − (M²/3f²)(A + C/a³)²`, whose perfect square
splits into a `w=0` dust `−2M²AC/(3f²)·a⁻³` **and** a BBN-forbidden stiff `w=1` partner `−M²C²/(3f²)·a⁻⁶`. The
stiff term forces `|C|/|A| ≲ 3×10⁻²⁴` (L84), a fine-tuning L86 found genuine and not removable within the action.
The stiff term exists *only because ρ is quadratic in C* (the square). This lane asks constructively whether any
sibling gives dust **linear** in the charge (`ρ ~ a⁻³`, like `ρ=mn`) with no a⁻⁶ partner.

## 1. WHY ρ is quadratic — the trace, and the structural lock (checks C0, C1, P1)

- **C0 — the clean identity.** `ρ = K − QK_Q + 3HF_QQ = K(Q) + Q·(C/a³)` **exactly**, for any K and any F: using the
  conserved charge `C/a³ = −K_Q + 3HF_Q` the two `K_Q` terms cancel, and the *entire* charge/H dependence of ρ
  collapses to one explicit product `Q·(C/a³)`. This is the cleanest way to see the origin of the square.
- **C1 — health forces K exactly quadratic.** The background-independent velocity-Hessian degeneracy
  `det W = (3a⁴/N²)(2M²K_QQ − 3F_Q² − 6M²H F_QQ) = 0` (reproduced exactly) forces `F_QQ=0` (F affine, `F_Q=f`
  const) and then `K_QQ = 3f²/(2M²) = 2k₂`. Because `F_Q=f` is **constant**, `K_QQ` is **constant** ⇒ **K is
  exactly quadratic** (`K_QQQ=0`). Health pins the constitutive curvature.
- **P1 — the a⁻⁶ term IS the curvature `K_QQ`.** Generally (F affine),
  `d²ρ/du² = −1/K_QQ − 3Hf·K_QQQ/K_QQ³` with `u ≡ C/a³`; the stiff coefficient is `½·d²ρ/du²`. To kill it for **all**
  backgrounds H needs, term by term in H, **both** `1/K_QQ = 0` (`K_QQ→∞`: a non-propagating constraint field) **and**
  `K_QQQ=0`. For any *finite-curvature* quadratic K the stiff coefficient is `−1/(2K_QQ) = −M²/(3f²) ≠ 0`.
  **The very degeneracy that lets the clock source a dust forbids the dust from being linear-in-charge** — the dust
  `−A/(2k₂)` and the stiff `−1/(4k₂)` are the cross term and the square of one perfect square `−(A+C/a³)²/(4k₂)`,
  sharing the same `1/(4k₂)` that also fixes the correct gravitational back-reaction `3M²H²`.

## 2. Every linearisation kills the dust (or the braiding) — checks P2, P3

| Escape | What happens | Verdict |
|---|---|---|
| **(a-i) Linear K, `k₂=0`** | `K_Q=A` const ⇒ the charge relation fixes the *background* (`−A+3Hf = C/a³`), not Q; Q carries no field info | **no a⁻³ dust** (P2a) |
| **(a-ii) `f=0`** | mixed Hessian `W_aφ ∝ F_Q → 0` (braiding gone, clock decouples), **and** ρ is *still* quadratic (`stiff=−1/4k₂≠0`) | breaks braiding, keeps square — worst of both (P2b) |
| **(b) Cuscuton `K∝|Q|`** | `K_Q=λ` const (`K_QQ=0`) ⇒ ρ becomes linear (`3HfQ`) but Q is an undetermined constraint direction, a non-propagating field, not a conserved a⁻³ number | square gone **and** no dust (P3a/b) |
| **(b′) Engineer `ρ = m·(C/a³)`** | demanding energy = mass×number for all H forces `3f(Q−m)=0 ⇒ Q=m` pinned constant | constraint field, no propagating dust (P3c) |

The stiff-free condition needs `K_QQ→0` (cuscuton) or `K_QQ→∞` — **both remove the propagating charge that IS the
dust.** Linear energy in the clock charge is possible only as a constraint field, never as clustering dust.

## 3. The only stiff-free dust is EXTERNAL CDM — check P4

- **P4a — a separate Schutz/Brown fluid `ρ=mn` IS stiff-free.** Number conservation `∇·(nu)=0` gives `n∝a⁻³` and
  `ρ=mn∝a⁻³`, exactly linear in the conserved number, **no a⁻⁶ partner** (energy = mass × number, like ordinary CDM).
- **P4b — but it is not the clock.** A kinetic scalar's energy is `ρ=K(Q)+Qu` with K forced quadratic; a fluid's
  energy is `m×(independent number n)`. The braided clock **cannot** be a `ρ=mn` fluid (P3c: linear clock energy ⇒ Q
  pinned ⇒ constraint). So (c)/(d) **add** dark matter rather than derive it from the clock.
- **P4c — and it re-imports L61.** A minimally-coupled `ρ=mn` CDM satisfies the L61 excess-spent-once hypotheses
  (reproduces deep MOND with cold part off; CMB-fixed amount; transmits Newtonian pull in galaxies at efficiency ≥
  recombination) ⇒ the branch-independent theorem forces a median ~1.69× pointwise rotation-curve overshoot.
  Stiff-free, but it double-counts the pull and defeats the framework's central claim.

## 4. Higher-order K is worse — check P5

A cubic `k₃Q³` makes `K_QQ = 2k₂+6k₃Q` non-constant, **violating** the background-independent degeneracy (Boulware–Deser
ghost), **and** adds an even stiffer `C³/a⁹` (`w=2`) partner. Going beyond quadratic worsens both health and the stiff tower.

## a₀-independence — check P6

a₀ enters astra's action only through the galaxy MOND term `M²a₀²G(|V|/a₀)`, never the FLRW stress `ρ=K+Qu`, the charge,
or the degeneracy. The entire L87 analysis is a₀-free; both footings (9.3619e-11 / 1.1279e-10 m/s²) give the identical
result (demonstrated, not assumed).

## Confidence

- **HIGH** on the algebra and the structural theorem: the `ρ=K+Qu` identity (C0), degeneracy ⇒ K exactly quadratic (C1),
  finite `K_QQ` ⇒ nonzero stiff (P1), and every linearisation deleting the dust or the braiding (P2/P3) are exact sympy
  statements.
- **HIGH** that a separate `ρ=mn` fluid is the only stiff-free route and that it re-imports L61.

**Bottom line.** The dust and its pathological stiff partner are two faces of the **same** quadratic constitutive
relation that the health degeneracy *requires*. You cannot keep the F(Q)Θ charge-sourced dust and drop the a⁻⁶ term.
This elevates L84/L86 from "a fine-tuning cost" to "an **intrinsic** fine-tuning forced by health" — a real, valuable
negative. The only stiff-free alternative (external `ρ=mn` CDM) defeats the framework's purpose (one action, no
double-counted DM pull; L61). Not a new kill — the theory remains viable at the tuned point (L86) — but the ~24-order
`|C|/|A|` tuning is now shown to be structural, closing the constructive "linearise the dust" door.
