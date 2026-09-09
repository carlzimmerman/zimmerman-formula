# L69 — the constructive inverse of the L60 kill: what an action must HAVE to be healthy in deep MOND, and whether anything survives

**Nothing does.** The transverse gradient term of a matter-sourced MOND scalar coupled to a clock stays
non-negative through deep MOND **only** by (a) removing the coupling that sources the scalar with matter,
(b) adding a constant stiffness that is L5's already-closed fixed-strength long-range force, or (c) leaving
the single-metric Einstein–Hilbert host. This makes L60 a **third class-level no-go** alongside the
foliation theorem and the excess-spent-once theorem, with its hypotheses derived here for a **general**
coupling structure rather than read off the single deposited action, on both a₀ footings.

2026-09-09. Lane L69 of [CHARTER.md](CHARTER.md), the constructive inverse of the kill in
[L60_ANISOTROPIC_HEALTH.md](L60_ANISOTROPIC_HEALTH.md), building on [L46_MODE_FLOOR.md](L46_MODE_FLOOR.md)
and [L63_DEGENERACY.md](L63_DEGENERACY.md).
Script: [L69_healthy_deepmond.py](L69_healthy_deepmond.py) → [L69_healthy_deepmond.out](L69_healthy_deepmond.out).
**31 checks, 31 PASS / 0 FAIL; exit 0; runtime 1 s.**

**Polarity.** Each check asserts a *statement* and PASS means the statement is true. A PASS on a verdict
line is therefore not a win for the theory — read the statement.

Nothing under `closure_2026/` or any other agent's directory was imported, executed or copied. The ADM
Einstein–Hilbert Lagrangian, the aether/khronon sectors, the MOND sector, the Dirac counter and the static
energy form were rebuilt here in sympy in exact rational arithmetic; the general necessary condition is
derived from scratch with **every structural coefficient kept as a free symbol**.

---

## 1. Controls (PART 0) — nothing below counts without them

| control | required | got |
|---|---|---|
| C1 ADM general relativity | 2 | **2** (4 primary + 4 secondary, all first class, from the algorithm) |
| C2 GR + one minimally coupled scalar | 3 | **3** |
| C3 Einstein-aether (c₁…c₄ = 1/5,1/7,1/11,1/13) | 5 | **5** |
| C4 khronometric | 3 | **3** |
| C5 L60's threshold | (2−K_B)/(2−c₁₄) = 0.9000009 | **0.9000009** |
| C6 L60's deep-MOND failure | s = 0.3985 | **0.3985** (g_N < 3.73e−11 canonical / 4.49e−11 alt) |
| C7 L60's static three-field energy-form route | sign change at (2−K_B)/(2−c₁₄) | **reproduced from the action** |
| C8 J_Y = s/Δ → √s → 0 as s → 0 | the load-bearing fact | **J_Y/√s − 1 < 6e−3 over s = 1e−3…1e−9; J_Y = 3.2e−5 at s = 1e−9** |

C7 rebuilds L60's 3×3 **from the assembled action** — set all time derivatives to zero, restrict to
(lapse n, spatial trace hT, δφ), and read off `C[n,hT] = 1/2` (the Hamiltonian constraint), `C[n,φ] = 2−K_B`
(the AeST coupling through the lapse), `C[φ,φ] = −(2−K_B)J` — and its Schur complement changes sign at
`J = (2−K_B)/(2−c₁₄)`. No dispersion relation, no Dirac algorithm.

---

## 2. The necessary condition, for a general coupling structure (PART 1)

The static transverse sector of **any** theory in this class is a 3×3 quadratic form on (lapse n, a metric
mode h, MOND scalar φ) with the entries kept as **free structural inputs**:

```
        n        h         φ
   n  [ a_c     g_H       λ          ]     a_c    = clock acceleration term (c₁₄ in AeST)
   h  [ g_H     k_H       0          ]     g_H    = lapse × spatial-curvature coupling  (1/2 in GR)
   φ  [ λ       0     −κ_φ Σ_⊥       ]     k_H    = spatial-curvature gradient energy   (1/8 in GR)
                                           λ      = lapse–scalar (clock-acceleration) coupling
                                           κ_φ    = scalar's overall normalisation
                                           Σ_⊥    = transverse gradient stiffness = J_Y + κ
```

`λ = C[n,φ]` is **both** the entry that transmits the matter source to φ (matter couples to the lapse
through the Hamiltonian constraint) **and** the entry that, once the lapse is Schur-eliminated, feeds a
wrong-sign term back into φ's stiffness. Eliminating (n, h):

> **N1 — THE NECESSARY CONDITION, as an inequality on the structural inputs (not on a parameter point):**
>
>     Σ_⊥  >  λ² / [ κ_φ · χ_lapse ]        with   χ_lapse = g_H²/k_H − a_c   (the lapse's effective stiffness)

- **N2.** At the AeST structure (g_H = 1/2, k_H = 1/8, a_c = c₁₄, λ = κ_φ = 2−K_B) this reduces **exactly** to
  L60's threshold `(2−K_B)/(2−c₁₄)`.
- **N3 — the channel, isolated.** χ_lapse's leading piece `g_H²/k_H = (1/2)²/(1/8) = 2` is the **Einstein
  Hamiltonian constraint**, not the clock's `a_c ~ 10⁻⁶`. The subtraction `λ²/χ_lapse` is fixed by GR's
  own constraint structure; the threshold carries a 2 for that reason, with c₁₄ irrelevant to it.

> **N4 — THE DEEP-MOND COROLLARY.** Write Σ_⊥(s) = J_Y(s) + κ, with J_Y = s/Δ the matter-sourced kernel
> piece (C8: → 0 as s → 0) and κ ≥ 0 any extra canonical gradient term. Then lim_{s→0} Σ_⊥ = κ, and the
> condition holds through the **whole** deep-MOND regime **iff**
>
>     λ = 0        OR        χ_lapse ≤ 0        OR        κ ≥ λ²/(κ_φ χ_lapse) > 0.
>
> Because the RHS is a **positive constant** whenever λ ≠ 0 and χ_lapse > 0, while J_Y → 0, the kernel
> piece alone can **never** hold the condition in deep MOND. The three disjuncts are exactly three of the
> structural escapes below; the fourth flips χ_lapse's sign.

---

## 3. The four structural escapes, each run (PART 2)

| # | escape | verdict | number |
|---|---|---|---|
| (i) | remove the lapse subtraction, λ = 0 | **kills the MOND source** | φ_amplitude ∝ λ; λ = 0 ⇒ φ = 0; shift-coupled static `C[n,φ] = 0`, and static matter has zero momentum density |
| (ii) | add a canonical κ\|∇φ\|², Σ_⊥ = J_Y + κ | **L5's excluded constant** | κ ≥ 0.900 ⇒ deep MOND = rescaled G, G_eff/G = 3.0 (10× BBN bound), RAR offset 0.15–0.56 dex (> 0.11 scatter) |
| (iii) | move the threshold via K_B, c₁₄ | **cannot reach ≤ 0** | threshold ∈ [0.875, 1.0] over K_B ≤ 0.25 (BBN), c₁₄ ≤ 1e−4 (Cassini); J_Y → 0 beats any positive threshold |
| (iv) | flip χ_lapse < 0 | **leaves the GR host** | needs a_c = c₁₄ > g_H²/k_H = 2 ⇒ α₁ ~ 8 vs Cassini 1e−4 (excluded ~1e5), or abandon Einstein–Hilbert |

- **Escape (i)** is the sharpest structural point. The coefficient λ that generates the wrong-sign term is
  the **only** channel by which static matter reaches the scalar: matter's energy density couples to the
  lapse via the Hamiltonian constraint, and λ = C[n,φ] is the lapse→scalar link. Sourcing the scalar from a
  spatial current instead (coupling ∂_iφ to the shift/momentum sector) sets `C[n,φ] = 0` — but a static
  galaxy has zero momentum density, so the scalar then has **no source**. Both are built from the action.
  The one place this is escapable — putting the MOND sector **inside** the clock, with no separate scalar
  and no independent lapse — is the integrable-clock construction, which **L66** records as evading this by
  violating the separate-scalar hypothesis; its own deep-MOND health is **uncomputed** and is out of this
  lane's scope.
- **Escape (ii).** A constant added to the deep-MOND stiffness is a rescaling of G: `(J_Y + κ)g_φ = λ g_N`
  becomes, as J_Y → 0, `κ g_φ = λ g_N`, i.e. `g_φ = (λ/κ)g_N` — a fixed-strength, unscreened, long-range
  enhancement of gravity, exactly L5's object, reached here from the health condition instead of from the
  cluster residual. Both horns of L5 fire: BBN (`G_eff/G = 3`, 10× the 0.2 bound) and the rotation-curve fit
  (0.15–0.56 dex off the RAR against 0.11 dex scatter). It buys health by deleting the MOND phenomenology.
- **Escape (iii)** is **sharper than L60's F4**: because J_Y → √s → 0, **no strictly positive threshold** can
  be beaten through the whole deep-MOND regime. Even the most favourable admissible threshold 0.875 is
  violated for all s < 0.383, and any threshold T > 0 is eventually violated as s → 0 (asymptotically below
  s ~ T²). The threshold's value sets **where** the term goes negative, never **whether**.
- **Escape (iv)** shows the destabilising sign is the Einstein Hamiltonian constraint's own. χ_lapse > 0 is
  structural to any single-metric GR host, not a tunable input.

---

## 4. The decisive question and the theorem (PART 3)

**Is there ANY structural feature that keeps the transverse gradient term non-negative through deep MOND
without (a) removing the matter-sourcing that produces MOND, or (b) adding the L5-excluded constant
stiffness? Answer: NO.** The necessary condition N1 has, in deep MOND (Σ_⊥ → κ), exactly three ways to hold
— λ = 0 (escape i, kills sourcing), χ_lapse ≤ 0 (escape iv, leaves the GR host / PPN-excluded), κ ≥ RHS > 0
(escape ii, L5's excluded constant) — and moving the threshold (escape iii) is none of them. There is no
healthy-deep-MOND action left to submit to the Solar-System, preferred-frame, tensor-speed and mode-count
gates; the enumeration is exhaustive on the necessary condition and closes before any candidate reaches
those gates.

> **THEOREM (class-level, hypotheses named and not exceeded).** For any action with
> **H1** — a soft bounded-boost MOND kernel, so Σ_⊥ = J_Y = s/Δ → 0 in deep MOND (the flat-rotation-curve
> requirement Δ → √s);
> **H2** — a **separate** MOND scalar coupled to a clock's 4-acceleration through the lapse (coupling λ ≠ 0);
> and
> **H3** — a single-metric Einstein–Hilbert host, so the lapse's effective stiffness
> χ_lapse = g_H²/k_H − a_c > 0 is fixed by the Hamiltonian constraint —
> the scalar's transverse gradient term is **negative throughout deep MOND**, a gradient instability. The
> only evasions each violate a hypothesis: kill λ (no MOND source, H2), add a constant κ (L5-excluded
> rescaled G, breaks H1's soft limit into a fixed force), or leave the GR host (H3).

This is L60 read as a requirement rather than a computation on one action, and it agrees with **L66**, which
reached the same class statement from the other side by exhibiting that the lead's integrable-clock action
evades the kill precisely by violating H2.

---

## 5. Relation to the two theorems already proved (PART 4)

- **The foliation theorem (L31)** forces MOND + one metric + two tensor modes + locality to carry a
  distinguished timelike direction — a **preferred-frame clock** with (elliptic corollary) a preferred
  foliation on whose leaves the field responds instantaneously. That clock is exactly the ingredient **H3**
  needs: an Einstein-constrained lapse fixed by a clock. **L31 forces the clock; L69 prices it** — the
  clock's lapse coupling to a soft matter-sourced scalar (H1 + H2) is what destabilises deep MOND.
- **The excess-spent-once theorem (L55/L61)** says the galaxy anomaly is one number per point and modes,
  metrics and matter coupling enter only through a single **transmission factor** that can be spent once.
  This lane's **λ is that same channel** seen in the health sector: it is simultaneously the only static
  matter source for the scalar (Ei1) and the coefficient whose square is subtracted from the stiffness (N1).
  The **soft kernel H1** is the shared hypothesis: Σ_⊥ → 0 is the same deep-MOND softness that makes the
  boost a single spendable number in L61.

**The common root.** All three no-goes trace to the single matter-to-MOND transmission channel that "MOND
from one metric" forces into existence. Foliation: it must be a preferred-frame clock. Excess-spent-once:
its output is one number, not reusable. L69: the coupling that feeds it — soft, and routed through the
Einstein Hamiltonian constraint — is destabilising in deep MOND. The lapse coupling λ, the transmission
factor, and the preferred-frame clock are **three faces of the one channel**.

---

## 6. Verdict, in three sentences

**It is a class-level no-go, derived for a general coupling structure rather than the single deposited
action: the transverse gradient term of a matter-sourced MOND scalar coupled to a clock through a lapse
coupling stays non-negative in deep MOND only if the scalar loses its matter source (λ = 0), or acquires an
L5-excluded constant stiffness (κ ≥ 0.9 ⇒ a rescaled-G force that is 10× the BBN bound and 0.15–0.56 dex off
the rotation-curve relation), or leaves the single-metric Einstein–Hilbert host (χ_lapse ≤ 0) — and none of
the three survives.** The instability is generic to any action with H1 (a soft bounded-boost kernel, so the
transverse stiffness J_Y = s/Δ → 0), H2 (a separate MOND scalar coupled to a clock's acceleration through
the lapse), and H3 (an Einstein-constrained lapse whose effective stiffness carries the fixed +2 of the
Hamiltonian constraint), on both a₀ footings, and it is the third such no-go alongside the foliation theorem
that forces the clock and the excess-spent-once theorem that prices its transmission. **κ = ½ remains
fitted; this lane touches only the transverse-sector linear health about a WKB background of a class of
actions, and names its own limits — WKB (B/k ≤ 10⁻⁷), linear, and the integrable-clock escape (H2 violated)
left uncomputed by L66.**

---

## 7. What is open, named

1. **The integrable-clock action's own deep-MOND health.** It evades this theorem by violating H2 (no
   separate scalar), so the theorem says nothing about it; L66 records its deep-MOND transverse health as
   uncomputed and flags a distinct indefinite-Hessian concern. That calculation, on a galactic quasi-static
   background, is the named next step and is out of this lane's scope.
2. **The nonlinear endpoint** (inherited from L60): an unstable linear mode says the background is not the
   endpoint; it does not say what is.
3. **Non-metric hosts.** χ_lapse's positive sign is fixed only for a single-metric Einstein–Hilbert host
   (H3). Whether a bimetric or higher-derivative host with a different lapse constraint could carry χ_lapse ≤ 0
   *and* MOND *and* pass the tensor/PPN gates is not addressed here — it is outside the class the theorem
   names, and overlaps the two-metric branch L61 left deliberately open.

Nothing here is closed. κ = ½ remains **fitted**, and this file never says otherwise.
