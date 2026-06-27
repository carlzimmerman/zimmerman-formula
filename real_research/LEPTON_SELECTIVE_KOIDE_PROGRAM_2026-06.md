# The Lepton-Selective Koide Problem as a Standalone Research Program

**Date:** 2026-06-27
**Scope:** EXPLICITLY OUTSIDE the de Sitter–Unruh framework. `a0`, `Z`, the kernel `(3/8π)^(1/4)`,
`ρ_DE`, `T_dS` — NONE are used anywhere in this program. Nothing here is tied to the framework; the
framework provably cannot reach the lepton sector (flavor-blind by the equivalence principle), so the
Koide problem is treated purely as standalone charged-lepton physics.
**Verdict:** **IMPOSE-NOT-DERIVE (clean, computed NULL on derivation) + a sharp falsifiable frontier map.**
No manufactured crack. The 45-year-open problem stays open; the precise location of the wall and the
single most-promising surviving angle are named below.

Every quantitative claim traces to a RUNNABLE script that exits 0. Scripts:
- `reviews/koide_mechanism_audit.py` (exit 0) — survey + non-circularity audit of the four published mechanisms.
- `reviews/koide_qed_running.py` (exit 0) — QED-running threat + Sumino protection scale.
- `reviews/koide_twoflavon_cone_construct.py` (exit 0) — the ONE new construction attempt (this workflow).
- Supporting (prior corpus, re-read, all exit 0): `koide_circularity_INDEP_verify.py`, `koide_missing_ingredient.py`,
  `koide_new_construction.py`.

---

## 0. The circularity knife (the bar every claim must clear) — `koide_mechanism_audit.py`, sympy-exact

For the Koide parametrization √m_i = M(1 + r·cos(θ + 2πk/3)):

```
Q := (Σ m_i)/(Σ √m_i)²  =  1/3 + r²/6        (θ and M cancel — Q depends ONLY on r)
Q = 2/3   ⇔   r = √2   ⇔   cos²(angle of √-mass vector to (1,1,1)) = 1/2   ⇔   45° EXACTLY
```

Real leptons (m_e=0.51099895, m_mu=105.6583755, m_tau=1776.86 MeV): **Q = 0.66666051**, angle = 44.99974°,
cos² = 0.500005. (Q − 2/3 = −6.16×10⁻⁶.)

**Consequence (the brutal test):** "choose a potential minimized at r=√2 / equal singlet+doublet norm / 45°"
**is identical to** "assume Q=2/3." A mechanism DERIVES Koide only if 45° EMERGES from inputs that never
mention 45°/√2/2/3, AND is ROBUST (perturb the inputs → 45° stays; a slide means it was tuned).

---

## 1. Which surveyed mechanism DERIVES vs IMPOSES equipartition? — `koide_mechanism_audit.py` (14/14 checks pass)

**0 of 4 published lepton-selective mechanisms derives the 45° non-circularly.** All impose r=√2.

| Mechanism | Verdict | Why (computed) | Status |
|---|---|---|---|
| **(a) Sumino U(3) family gauge** (0812.2103) | **IMPOSES** + PARTIAL protector | Tree VEV engineered onto the Koide locus a/b = 4±3√2 (**IRRATIONAL** → not a symmetry-protected rational extremum {0,1,∞}). The gauge loop forces the protector's SIGN+SHAPE+the **1/4 coefficient** (real, group-theoretic) but TUNES the magnitude α_F = 4·α(m_τ) ("accidental", no Ward identity). | viable-untested (protector); NOT a 45° derivation |
| **(b) Koide yukawaon** (Koide 2008+) | **IMPOSES (by construction)** | The "vacuum condition" (Tr P)² = (3/2)Tr(P²) is **algebraically identical to Q=2/3** — written into the superpotential. Perturbation: dQ/dε = +0.20 ≠ 0 at the Koide point → NO dynamical fixed point. | viable-untested (UV scaffold) |
| **(c) Foot geometric** (hep-ph/9402242) | **IMPOSES / no dynamics** | 45° is the geometric **identity** cos² = 1/(3Q) = 1/2 — a re-statement of Q=2/3, not a force. S3 alignment extrema sit at **54.7°/35.3°/0°, never 45°**. | EXCLUDED as a derivation (it is a definition) |
| **(d) democratic / S3** | **IMPOSES** | Democratic matrix eigenvalues {1 (singlet), 0, 0 (doublet)}: S3 fixes ONLY the singlet; the doublet amplitude (→ r) is a free knob (g=0.5→Q=0.417, g=1→0.667, g=2→0.641). Inequivalent irreps → no group element equates their norms → no forced equipartition. | viable-untested (host structure) |

**Two genuine PARTIALS credited loudly (both ways — these are real, not dismissed):**
1. **Sumino's family-GAUGE IR protector** forces the QED-cancellation's sign + shape + the **1/4 coefficient**
   (pure group theory: conjugate reps + log v² = ½ log m²). A real mechanism; only the magnitude is tuned.
2. **The S3/democratic 1+2 decomposition** (singlet ⊕ doublet) is the **correct symmetry HOME** for Koide.

Neither forces the *number*. The entire unforced content of Koide is the single amplitude **r = √2 (the 45°)**.

---

## 2. Does QED-protection work, and what scale does it predict? — `koide_qed_running.py` (all checks pass)

**QED genuinely threatens Koide, and Sumino genuinely protects it — by tuning, with a falsifiable signature.**

- **Experimental precision:** σ_Q(exp) = **6.78×10⁻⁶** (PDG pole-mass errors, m_τ's 0.12 MeV dominant). Data
  currently pin Q to ~1 part in 10⁵.
- **The drift (real threat):** with the 1-loop pole↔MS̄ relation m_i(μ) = M_i[1 − (α/π)(1 + (3/4)ln(μ²/M_i²))],
  Q drifts UP monotonically: **Q(10¹⁶ MeV) = 0.668222, drift = +1.556×10⁻³ = +230·σ_exp** at the GUT scale.
  **Diagnosis (decisive):** dropping the flavor-dependent (3/4)ln(μ²/M_i²) term leaves Q = 0.66666051 EXACTLY
  (scale-invariant) — so the **entire drift is the flavor-dependent −(α/π)(3/4)ln(m_i)** piece. A protector is
  genuinely needed; this is not a dismissal artifact. (Consistent with the corpus's ~0.19%/~178σ at lower scale.)
- **Sumino protection works by a tuned coupling:** the ln-m_i slope cancels iff **α_F = (3/4)·α_em/c** (a chosen
  O(1) ratio; c=1 → α_F = 5.47×10⁻³, g_F ≈ 0.262). It PROTECTS, does not GENERATE: fed a non-Koide triple
  (0.5, 100, 1500 MeV, Q=0.6549), the slope-cancellation keeps Q=0.6549 — it never pulls a non-2/3 spectrum to 2/3.
- **PREDICTED SCALE (the falsifiable handle):** new family gauge bosons at **Λ_fam ≳ 32 TeV** (tree-level FCNC
  μ→3e floor, SINDRUM BR<10⁻¹², O(1) mixing; Sumino's own quote 10²–10³ TeV is the better reference). Correlated
  charged-lepton-flavor-violation (**μ→3e, μ→eγ, μ–e conversion**) sits just below current limits — probed by
  **Mu3e (~10⁻¹⁵–10⁻¹⁶), MEG-II, Mu2e**. A null from those at improving sensitivity squeezes/excludes the
  natural-coupling Sumino window. Residual uncancelled 2-loop drift ~ **8.7·σ_exp** is a near-future precision target.

**Honest caveat (in-script):** the exact drift magnitude is scheme/order-dependent; the robust, scheme-independent
statement is that the drift is FLAVOR-DEPENDENT and ≫ σ_Q(exp), so a protector is needed. The 230σ headline is
order-of-magnitude, not precision. Λ_fam ≳ 32 TeV is a crude O(1)-mixing floor, not a scale prediction.

---

## 3. Did any NEW construction produce equipartition non-circularly? — `koide_twoflavon_cone_construct.py` (this workflow)

**The one new angle attacked (genuinely new vs the closed corpus).** The banked corpus has already run and
closed: S3/A4 single-flavon potential, entropy/moment extremum, IR-RG fixed point, measure/channel-count,
self-duality, gauge-anomaly cancellation, modular flavor, Dirac/EJA, exceptional geometry. The banked
`koide_new_construction.py` itself ends by naming the exact gap it could not fill:

> *"a genuine Koide derivation must be a symmetry-breaking potential with a NON-renormalizable or MULTI-FIELD
> structure whose minimum lands 3 distinct levels at the equal-norm cone for a reason independent of the cone."*

**This script builds that object:** a **two-flavon (multi-field) S3 potential** — the door the corpus flagged
but never built. Two S3-triplet flavons φ, χ; √-mass vector s_i = φ_i + κ·χ_i; the most general renormalizable
S3-invariant potential in the 8 basic invariants (A2, B2, C, A4, B4, D, E=Σφ³χ, F=Σφχ³), with NO term referencing
45°/√2/2/3. Three questions, each computed:

1. **Degeneracy theorem (Section 1, re-proven sympy-exact):** a renormalizable SINGLE-flavon S3 minimum forces
   active components equal in magnitude → ≤2 distinct levels. A Koide triple needs 3 distinct → single-flavon is
   structurally dead. **This is why multi-field is the only door.**

2. **(Q1) Does the multi-field minimum carry 3 distinct levels?** — **NO, generically.** Across 150 generic
   coupling sets, **0/150** gave a 3-distinct-level minimum (they fall into the symmetric democratic Q=1/3 or
   aligned vacua). Even with a symmetry-lowering cross-term (hE=Σφ³χ), the global minimum prefers a residual
   **1+2 (doublet-degenerate) ≤2-level structure** (best min-gap/spread ~ 0.00). **The S3 doublet degeneracy is
   STICKY** — a deeper wall than the prior assumption. The degeneracy theorem is evaded *in principle* (multi-field
   allows 3 levels) but the *energetics still prefer degeneracy.*

3. **(Q2/Q3) Does the 45° cone emerge / attract non-circularly?** — **NO.** Generic minima land within 1° of 45°
   in **0/1** of the 3-distinct cases. Tuning hE to hit 45° works, but: the closest-to-45 minimum is a
   **degenerate (a,a,b) 2-level state (levels [0.0744, 0.0744, 0.569]), NOT a real 3-distinct Koide triple** —
   the cone is hit by a degenerate config, not a Koide spectrum (the angle to (1,1,1) varies continuously even
   for 2-level configs, so angle-variation alone does not imply distinct masses). And the angle **SLIDES** with
   the coupling: **d(angle)/d(hE) ≈ −43 deg/unit** → a TUNED PASS-THROUGH, not an attractor.

**Section 4 (the structural reason, sympy-checked):** the 45° cone is a **codimension-1 surface** (one equation
(d₁+d₂+d₃)² = (3/2)Σd²) in √-mass direction space. A generic potential's minimum is an isolated point; the set
of couplings whose minimum lands on a codim-1 surface is itself codim-1 (measure zero). No S3-invariant is
extremized ON the cone (S3 extrema sit at 54.7°/35.3°/0°). So the multi-field freedom **removes the degeneracy
OBSTRUCTION but adds NO FORCE toward equipartition.**

**RESULT: IMPOSE-NOT-DERIVE (clean NULL).** The new construction FAILS TWICE — (i) its minimum prefers a
degenerate 2-level state, not even a 3-distinct spectrum; (ii) the angle it reaches is hit by that degenerate
config and slides freely. The honest expected outcome for a 45-year-open problem. No manufactured win.

---

## 4. The neutrino Q_ν(m₁) status — `koide_missing_ingredient.py`

The selector that lands 2/3 must be **specific to the charged-lepton Yukawa/QED sector**, NOT color/structure:

| m₁ (eV) | neutrino Q (normal ordering, Δm²₂₁=7.5×10⁻⁵, Δm²₃₁=2.5×10⁻³) |
|---|---|
| 0.000 | 0.585 |
| 0.001 | 0.491 |
| 0.010 | 0.382 |
| 0.050 | 0.336 |

Charged-lepton Q = 0.66666 (hits 2/3); **neutrino Q is a free function of m₁, generally ≠ 2/3.** Neutrinos are
the most point-like leptons and they do NOT sit at 2/3 → **any "leptons-are-point-like / color-blind" selector is
falsified.** This is the neutrino wall: it forces the Koide selector into the charged-lepton Yukawa sector (the
QED −log running Sumino cancels), and it makes Q_ν a *prediction target* for any future model that ties the sectors.

---

## 5. Frontier map (the research-program deliverable)

A genuine non-circular Koide derivation must EVADE, simultaneously, every failure mode mapped here:

- **NOT a symmetry-restoring fixed point** — those give the democratic Q=1/3 (the opposite of a 3-mass spectrum).
- **NOT a moment/entropy constraint** — R = (Σs)²/(Σs²) = 1/Q is an identity, so fixing the moments *is* fixing Q.
- **NOT a renormalizable single-flavon gradient** — degeneracy theorem forbids a 3-distinct-mass minimum (≤2 levels).
- **NOT a generic multi-flavon gradient either** (NEW, this workflow) — the doublet degeneracy is sticky; the
  minimum prefers ≤2 levels, and the cone is a codim-1 surface no S3-invariant is extremized on.
- **NOT self-duality / measure / anomaly** — all closed in the corpus (geometric relabels or per-state overshoot r=2).

It must therefore be a **symmetry-BREAKING dynamics with a lepton-selective IR fixed point** that (i) cancels the
QED −log(m_i) drift and (ii) pins the √-mass vector at the equal-norm cone *for a reason independent of the cone*.
The **only known object meeting (i)** is Sumino-class new physics (a gauged family symmetry + a tuned IR protector),
and it IMPOSES (ii) via the potential rather than deriving it.

**Sharpest near-term test of Koide-as-physics (two-pronged):**
1. **Precision spectroscopy of m_τ.** Q is exact at the pole to ~σ_Q = 6.8×10⁻⁶, m_τ-dominated. A better m_τ
   (BES III / Belle II, target ~±0.1 MeV) sharpens or breaks the 2/3 value to ~5 digits — Koide is genuinely
   falsifiable by data, not just a numerical curio.
2. **Charged-lepton-flavor-violation (the Sumino discriminator).** If the QED protector is Sumino-class, it
   predicts family gauge bosons at Λ_fam ≳ 32 TeV (Sumino: 10²–10³ TeV) with correlated μ→3e / μ→eγ / μ–e
   conversion just below current limits. **Mu3e, MEG-II, Mu2e** progressively squeeze (and can exclude) the
   natural-coupling window — the one concrete experimental handle on whether the Koide coincidence has a
   protective mechanism behind it.

---

## 6. Bottom line — what to tell Carl, straight

**Is the open Koide problem crackable by a new mechanism, or is the honest state "impose-not-derive + a
falsifiable frontier"?** It is **impose-not-derive.** All four published mechanisms IMPOSE r=√2 (Sumino via a tree
VEV on the irrational Koide locus, the yukawaon as a trace identity in the superpotential, Foot as a geometric
definition, democratic/S3 with a free doublet amplitude). The ONE new construction this workflow built — the
multi-field two-flavon S3 potential the corpus had flagged as the open gap — does NOT crack it: its minimum
prefers a degenerate 2-level state and lands the 45° cone only by a measure-zero coupling tuning that slides off
under perturbation. The circularity theorem held throughout (r and the angle reported alongside every Q); the
framework was never invoked (a0/Z appear nowhere).

**Single most-promising surviving angle:** **the QED-protection / Sumino-class lepton-selective IR fixed point.**
It is the only route that does real, non-circular work — it forces the protector's sign+shape+1/4 coefficient and
genuinely cancels the flavor-dependent QED drift — and it is the only one with a *falsifiable* signature
(family bosons + correlated CLFV near current bounds). It still IMPOSES the 45° via the potential rather than
deriving it, so it is not a crack; but it is the live frontier where the next genuine progress (or a clean
experimental kill) will come from. Everything is computed, exits 0, and is honest both ways: QED really threatens
Koide (credited), Sumino really protects it with a testable prediction (credited), but no mechanism — old or new —
derives the value 2/3.

**One line:** The lepton-selective Koide problem is IMPOSE-NOT-DERIVE — four published mechanisms and one new
multi-field construction all tune r=√2 in rather than deriving it (the new two-flavon route fails twice: sticky
doublet degeneracy + a codim-1 cone with no force toward it), and the single live frontier is the Sumino-class
QED protector, whose 32 TeV–10³ TeV family bosons and correlated μ→3e/μ→eγ CLFV (Mu3e/MEG-II/Mu2e) are the
sharpest near-term test of whether Koide is protected physics — all standalone, a0/Z untouched.
