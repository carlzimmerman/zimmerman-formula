# VERIFY — adversarial verification of the MI-lensing completion lane (C1/C2/C3 + NO-GO)

**Date:** 2026-07-17 · **Scope:** re-run + independent re-derivation of every load-bearing
claim in `mi_lensing_completion/`. Frozen repo untouched (read-only). Both a₀ footings carried
(9.36e-11 canonical = cH_Λ/Z · 1.13e-10 alt). Credits: Deffayet–Woodard 2011 (1106.4984),
Skordis–Zlosnik AeST 2021, Milgrom (AQUAL / MOND-as-inertia).

## 1. Re-run — all scripts exit 0

| script | result |
|---|---|
| `c1_frame_curvature.py` | 11/11 PASS, exit 0 |
| `c2_nonlocal.py` | 18 PASS / 0 FAIL, exit 0 |
| `c3_carrier.py` | expected-negative checks as designed, exit 0 |
| `nogo.py` | all checks pass, exit 0 |
| `verify_adversarial.py` (**this pass, independent**) | all checks pass, exit 0 |

## 2. What I independently re-derived (did NOT reuse the candidate assertions)

- **[A] The wedge.** From the assembled MI stress the on-shell source dressing is `K = 1/ν`
  (SUPPRESSION); correct single-metric lensing needs `ν·ρ`. Wedge = **ν² = 1+1/y**, reproduced
  from scratch. Phantom coefficient needed = `ν − 1/ν = 1/√(y(y+1))`, which **diverges** deep-MOND.
- **[B] The crux — passivity/amplification dichotomy.** a₀ = cH_Λ/Z is derived *only because*
  the modification is a **passive, causal, completely-monotone (Herglotz/Stieltjes) vacuum
  response** with a normalized measure ⇒ `|K| ≤ K(0) = 1` ⇒ it can only **suppress** (delivers
  1/ν). The framework's own kernel `K(z)=(√(1+4z)−1)/(2√z)` is exactly such a Stieltjes function.
  MOND-lensing needs **enhancement to ν > 1**, which lies strictly **outside the passive cone**.
  Enhancement requires an anti-dissipative (pumped) kernel whose amplitude is a **free coupling**
  ⇒ a₀ no longer cH_Λ/Z. This is a **structural sup-argument, not failure-to-find.**
- **[C] Evasion 1 (local, a₀-locked coefficient).** Forced to be **mass-blind**: the required
  local F′(y) carries √M (ratio √(M₂/M₁), y-independent, a₀ cancels). Fit on a 6e10 galaxy →
  a 1e14 cluster gets phantom fraction 0.024 (≈24× under-lensed). ⇒ **¬L**, both footings identical.
- **[D] Evasion 2 (lock the carrier's kinetic normalization to a₀ via the frame).** The fork is
  forced: frame-locked ⇒ delivers bounded O(K)=1/ν, shortfall ν² diverges deep-MOND (**¬L**);
  freed to reach ν ⇒ the boost is a y-dependent unbounded factor, not a fixed a₀-locked constant
  (**¬D**). No third option delivers {D ∧ L} on one metric.
- **[E] Direct counterexample search.** No normalized passive kernel reaches ν on the RAR shell
  (deep-MOND miss ≈ 30.6; passive cap = 1.0 vs target ≈ 31.6). The value the frame actually
  realizes is 1/ν — the *farthest* point from ν.
- **[F] Manufactured-F→1 check.** C2's F→1 is a **genuine** closure (isotropic phantom `ν·ρ` +
  no-slip Φ=Ψ ⇒ g_lens=ν g_bar), **not** faked — but it is a **modified-gravity** win: ν is
  form-invariant under (a₀,g_bar)→λ(a₀,g_bar), so a₀ is a free, footing-non-diagnostic coupling.
  Correctly downgraded to CLOSES-BUT-a0-FREE, not passed off as an MI completion.

## 3. Trap sweep (both directions)

- **Manufactured completion?** NONE. No candidate claims PASSES-ALL-FIVE-a0-DERIVED. C1 =
  FAILS-LENSING (keeps a₀ derived, fails L by mass-blindness + honest-variation Ostrogradsky);
  C2, C3b = CLOSES-BUT-a0-FREE (honest MG partials). The one "completes the theory" phrase in
  C2.md is explicitly qualified "**as modified gravity, losing the vacuum-derived a₀**." No
  ground-rule-forbidden "proves/solved/complete-field-theory" language survives.
- **Hidden ghost in a winner?** No winner. C2 self-reports a would-be ghost (eigenvalues ±½,
  tamed only by the *contested* retarded prescription) as a COST; C1 self-reports the
  Ostrogradsky (3rd metric derivatives from `□F(K)` when X is varied honestly). Both disclosed.
- **c_γ = c_GW preserved?** Yes. C2 purely metric; C3b scalar sources via its own T_μν. The
  disformal 2nd cone (GW170817-dead, ~7 orders) is **not** reopened anywhere.
- **Cassini / cosmology.** C2 Cassini PASS* (ν−1≈5e-7 at y=1e6) with the honestly-flagged
  inherited AeST Q₂-quadrupole caveat (Desmond–Hees–Famaey 2024) — a *shared MG* cost, not a
  clean pass. Cosmology = TUNE (separate fit of f, not the MI horizon-floor theorem). Honest.
- **No-go genuine theorem vs failure-to-find?** **Genuine**, modulo one banked premise: that the
  MI vacuum-response kernel is passive/completely-monotone (‖K‖≤1, the Herglotz–Nevanlinna
  representation + the ∫dμ/|t|=1 sum rule established in the frozen repo v4/v11). Given that
  premise — which is *also* what makes a₀ derived — enhancement is impossible without leaving the
  class, and every constructed evasion (C, D, E) lands on ¬D or ¬L. This is the appropriate,
  honest strength: a theorem conditional on the (independently banked) kernel-passivity result.

## 4. Verdict

**UPHELD.** The sharpened no-go stands and is a **structural obstruction**, not a failed search.
Within mandatory single-metric (S), the exact mutually-exclusive pair is

> **a₀-DERIVED (passive, bounded/normalized frame kernel)  XOR  single-metric MOND-lensing phantom (ν−1)ρ.**

Ghost-freedom G is not the binding lever (C1 fails L by mass-blindness regardless of its ghost).
The theory **can** be completed for lensing — but only **as modified gravity** (C2 / C3b:
single-metric, ghost-cost, MOND-lensing) at the price of a₀ becoming a **free** coupling,
forfeiting the vacuum-derived a₀=cH_Λ/Z. That is a **partial**, reported as such. No manufactured
completion; no manufactured no-go. Both footings; a₀ is footing-non-diagnostic on the L side (the
signature of a free parameter), which itself corroborates L ⇒ ¬D.
