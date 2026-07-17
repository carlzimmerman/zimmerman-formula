# VERIFY — adversarial verification of the MI covariant PT pass

**Date:** 2026-07-17. **Verifier:** independent re-run + independent reimplementation of the
growth/σ8/bulk-flow arithmetic + independent scrutiny of the crux derivation. Both a₀ footings
(canonical 9.36×10⁻¹¹, alt 1.13×10⁻¹⁰) carried. No repo files modified; this file is the only output.

## Bottom line

**CONCUR with the verdict: VIABLE-BUT-AeST/ΛCDM-DEGENERATE (both footings)** — with one honest
qualification on the word *derived*. The degenerate verdict is **robust and not manufactured**; no
viable-and-distinctive middle is smuggled; the arithmetic is exact. But the derivation is **partial**:
Part A is rigorously computed, while the floor's magnitude rests on an **imported** dS-Unruh pole plus
an **adiabatic H_Λ→H(z) substitution** that this pass does not itself derive. The verdict survives that
gap because the MI-off conclusion is forced algebraically by `a₀=cH_Λ/Z` and the pole floor, independent
of the substitution.

## 1. Reproduction (exit 0, numbers re-derived independently)

- `perturb_mi.py` → **17/17**, exit 0. `solve_growth.py` → **12/12**, exit 0. Re-run clean.
- Independent reimplementation (my own integrator, my own BBKS/top-hat bulk-flow, not their code)
  reproduces **every** load-bearing number:
  - X_floor(z=0,can)=48.92 = Z²/Ω_Λ (analytic identity confirmed); ν(z=0)=1.0740 (can)/1.0900 (alt).
  - D_MI/D_ΛCDM(z=0)=1.0221/1.0268; σ8=0.828/0.832 vs ΛCDM 0.811; f(z=0)=0.544/0.547 vs 0.527;
    fσ8(0)=0.450/0.455 vs 0.427 (+5.4%).
  - Bulk flow V(35)=333/351/355, V(100)=202/212/215 km/s; tensions vs Qin: **35 h⁻¹Mpc** ΛCDM 1.89σ →
    MI 1.17σ; **100 h⁻¹Mpc** ΛCDM 2.61σ → MI 2.47σ. All match RESULT.md to rounding.
- Numbers move when the physics moves (footing swap 0.828↔0.832; counterfactual blows up) → not
  hard-coded. Every check is a numeric residual, no boolean literals.

## 2. THE CRUX — is the effective argument DERIVED or ASSUMED?

Re-derived each ingredient independently:

**(i) Part A — |a_pec|² demoted: GENUINELY DERIVED.** The fixed-comoving-coordinate (CMB rest-frame)
observer's covariant 4-acceleration in conformal-Newtonian gauge is `a_i = ∂_iΨ` (first order), and
`|a|² = |∇Ψ|²/a² = g_pec²` is **second order** (sympy O(ε⁰)=O(ε¹)=0, O(ε²)=g_pec²). I confirm this is
correct and gauge-sensible: the static observer is held against the peculiar field, so it carries a
first-order acceleration, but its *square* is second order. The alternative frame choice (matter rest
frame, u^i=v^i) makes the matter free-falling ⇒ `a^μ=0` at linear order — **also** demoting the bare
first moment. So the conclusion "reading (a) cannot enter linear growth at leading order" is **robust to
the frame choice** and correctly derived. This is the solid half of the crux.

**(ii) The floor Z²(H/H_Λ)² — IMPORTED + adiabatically extended, not freshly computed.** The script does
**not** dynamically compute δ(□_u) from a velocity-sourced δu (as the task envisioned). It fixes u^i=0
and **imports** the pole κ_eff²=H²+(a/c)² from PULLBACK.md — which was derived on **exact de Sitter with
constant H=H_Λ** — then **substitutes H_Λ→H(z)** to obtain the *rising* floor. That substitution (the
dS-Unruh horizon temperature tracks the instantaneous FLRW expansion rate) is physically reasonable
(apparent-horizon Gibbons-Hawking) but is **an assumption this pass does not derive**. PERTURBATION.md is
partly honest about this (labels PT-D2 "PULLBACK-anchored"), but the headline "the perturbed □_u DERIVES
reading (b)" **overstates** what was computed. Recommend downgrading that phrasing to "the perturbed □_u,
combined with the frozen dS-Unruh pole and an adiabatic H(z) reading, gives reading (b)."

**(iii) Why the gap does not change the verdict.** The MI-off conclusion is **forced algebraically**:
κ_eff ≥ H_Λ always, and a₀=cH_Λ/Z, so X=(cκ_eff/a₀)² ≥ Z² ≈ **33.5** in *every* case — including the pure
reading-(d) H_Λ floor. At X=33.5, ν=1.090; any larger H(z) only pushes ν closer to 1. So ν∈[1, 1.09] at
z=0 **regardless** of the H_Λ-vs-H(z) choice. To get a *distinctive* ν (e.g. ν=2) you would need a₀ ≳ 10×
canonical — excluded by the a₀=cH_Λ/Z definition itself. **The degeneracy is a consequence of the factor
Z≈5.8 between a₀ and cH_Λ, plus the pole floor — genuinely derived, not posited.** The un-derived H(z)
substitution only sets the tiny z-*evolution* of an already-tiny enhancement.

**(iv) No k² (reading c): ARGUED, not fully computed.** The claim rests on □_u=(u·∇)² being purely
along-u/temporal, so e^{ik·x} passes as phase. This is structurally sound and I agree it is the right
reading; but because δ(□_u) with a dynamical δu was not carried out, "no k²" is a structural argument
rather than an explicit linear-PT computation. Conclusion defensible; derivation partial.

## 3. Is a viable-and-distinctive middle SMUGGLED? — NO.

If anything the setup leans *away* from distinctiveness: fixing u^i=0 removes the velocity-sourced δu
that is the only plausible route to k-dependence, and the result is scale-independent G_eff=ν(z)G. The
"exciting middle" is genuinely **not produced** and is honestly deferred to the 2nd-order/quasilinear
sector where (a_pec/a₀)² first enters. No smuggling detected.

## 4. Is a dead/degenerate outcome MANUFACTURED? — NO.

The degenerate ν≈1 is forced by a₀=cH_Λ/Z + κ_eff≥H_Λ (§2iii), not by a modeling choice tuned to kill
the signal. The "MI DEAD" overshoot (Part D, σ8 blown up 10³–10¹⁶×) is an explicit *counterfactual*
illustrating what reading (a) *would* do, correctly excluded because Part A demoted its source. Neither
prong is manufactured; the fork resolves to the middle-of-the-two by a real algebraic mechanism.

## 5. AeST-background reuse — LEGITIMATE, with one flagged incompleteness.

Reusing the AeST/ghost-condensate background + CMB (Skordis-Zlosnik 2021) for the expansion and the
early-universe normalization is legitimate and **not** a double-count of the growth boost: MI=ΛCDM at
high z (floor enormous, ν→1), and the σ8 enhancement is computed as a purely **late-time** ratio on a
fixed early normalization. **Soft spot:** ν(z) is applied to the *full* Ω_m=0.315, but in AeST the
condensate itself supplies the CDM-like clustering — whether ν should dress baryons only, or
baryons+condensate, and how the condensate's own perturbations respond, is exactly the "condensate-baryon
coupling + its own PT" the pass flags OPEN. This does **not** inflate the result (the enhancement is a few
% either way), but it means the growth treatment is a first-pass proxy, not the full AeST+MI PT. Honestly
flagged in both scripts.

## 6. σ8 / bulk-flow arithmetic — CONFIRMED.

Independently reproduced (§1). Caveats, honestly reflected in the scripts: the ΛCDM bulk-flow *absolute*
prediction (333/202 km/s) uses a simplified top-hat window and BBKS transfer, so the ~1σ "MI marginally
closer than ΛCDM at 35 h⁻¹Mpc" is a sanity-level statement, not a measurement-grade discriminator; the
W09 410@100 point is an old/contested large-scale excess and the script correctly reports MI does **not**
cure it (2.6σ→2.5σ). Not oversold.

## 7. Both footings — CARRIED CORRECTLY throughout. Canonical/alt differ only by the a₀ relabel; both
land in the degenerate prong (ν∈{1.074, 1.090} at z=0).

## Ledger

| # | Statement | Verifier finding |
|---|---|---|
| V1 | Scripts exit 0; 17/17 + 12/12; numbers independently reproduced | **CONFIRMED** |
| V2 | Part A: bare \|a_pec\|² is ≥2nd order ⇒ excluded from linear growth | **CONFIRMED, genuinely derived** (robust to frame choice) |
| V3 | Floor = Z²(H/H_Λ)²; MI switched (nearly) off, ν∈[1,1.09] at z=0 | **CONFIRMED as robust**, but H(z) form is an imported/adiabatic reading, not freshly computed |
| V4 | "the perturbed □_u DERIVES reading (b)" | **OVERSTATED** — recommend "gives, via the PULLBACK pole + adiabatic H(z)"; the *magnitude/dominance* is derived, the *H(z) evolution* is assumed |
| V5 | No k² / scale-independent | **CONFIRMED as defensible** (structural argument; δ(□_u) not explicitly computed) |
| V6 | Viable-and-distinctive middle smuggled? | **NO** |
| V7 | Dead/degenerate manufactured? | **NO** (forced by a₀=cH_Λ/Z + pole floor) |
| V8 | AeST reuse legitimate, not double-counted | **CONFIRMED**; condensate-vs-baryon dressing on the growing mode is an open first-pass proxy |
| V9 | σ8 / f / fσ8 / bulk-flow arithmetic, both footings | **CONFIRMED** to <0.5% |
| V10 | s=−1 and a₀'s value/footing remain postulated | **CONFIRMED** |

**Verdict:** VIABLE-BUT-AeST/ΛCDM-DEGENERATE — upheld. The distinctive MI cosmological signal, if any,
is not in the linear growing mode (forced degenerate by a₀=cH_Λ/Z); it can only live in the flagged-open
2nd-order/quasilinear sector. The one correction to the write-up is language: the H(z) floor is
*anchored+assumed*, not *derived*, though the degenerate verdict does not depend on it.

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_covariant_pt && python3 perturb_mi.py &&
python3 solve_growth.py` (both exit 0). Independent checks done in a separate scratch reimplementation.
No 'proves'/'closed'/TOE.
