# SYNTHESIS — the first covariant MI perturbation-theory pass on FLRW

**Date:** 2026-07-17. **Lane:** covariant modified-inertia (MI) linear perturbation theory on FLRW,
built on the AeST/ghost-condensate background + dark sector (Skordis–Złośnik 2021, PRL 127:161302).
**Artifacts (all in this dir):** `perturb_mi.py` (17/17, exit 0) → `PERTURBATION.md`;
`solve_growth.py` (12/12, exit 0) → `RESULT.md`, `mi_pt_fig.png`; adversarial `VERIFY.md`.
Both a₀ footings carried throughout: **canonical a₀=cH_Λ/Z=9.36×10⁻¹¹** (ρ_DE), **alt a₀=1.13×10⁻¹⁰**
(ρ_tot/cH₀), Z=√(32π/3)=5.78881. **s=−1 and a₀'s value/footing remain POSTULATED.**
No "proves"/"closed"/TOE.

---

## 1. Headline

**The covariant MI perturbation theory RESOLVES the fork-decider's free gap-A closure to the DEGENERATE
prong: the linear cosmological growing mode sees the dS-Unruh Hubble FLOOR, not the bare first moment —
so MI is switched (nearly) OFF for linear growth and MI cosmology is VIABLE-BUT-AeST/ΛCDM-DEGENERATE
(both footings), a smooth scale-independent few-percent late-time G_eff=ν(z)G boost with no distinctive
LSS signature and no σ₈ overshoot.** The exciting "viable-and-distinctive" middle is **not produced**
(and not smuggled); the "MI-DEAD overshoot" prong is **not selected** (and not manufactured).

## 2. mi_cosmology verdict — **VIABLE-BUT-AeST/ΛCDM-DEGENERATE** (both footings)

**The DERIVED effective argument (the crux the worldline arguments could not give):**

    X ≡ □_u/a₀² |_growing-mode  =  Z²(H(z)/H_Λ)²   +   (a_pec/a₀)²
                                    └── (b) Hubble/mode-freq FLOOR ──┘   └ (a) bare 1st moment ┘
                                        O(30–50) at z=0, dominates          2nd order, ≲3% of floor

- **Reading (b) — the floor — is what the growing mode sees.** The bare peculiar-acceleration first
  moment (reading a) is demoted to **second order** in perturbations (PART A, sympy: the cosmic
  rest-frame observer's 4-acceleration is a_i=∂_iΨ first order, but |a|²=g_pec² is second order — robust
  to the frame choice); the k²-gradient (reading c) is **absent** (□_u=(u·∇)² is along-u/temporal, so
  e^{ik·x} passes as transverse phase); reading (d), H_Λ², is just the a→0 floor of (b).
- **Consequence:** ν=1/K(X_floor) → **ν(z=0)=1.074 (can) / 1.090 (alt)** — MI nearly off.
  G_eff(a)=ν(X_floor(a))G is **scale-independent** (X_floor carries no k). Numbers:

  | | canonical | alt | ΛCDM / data |
  |---|---|---|---|
  | D_MI/D_ΛCDM(z=0) | 1.022 | 1.027 | 1 |
  | **σ₈** | **0.829** | **0.833** | Planck ΛCDM **0.811** (+2–3%, absorbable) |
  | fσ₈(z=0) | 0.451 | 0.453 | 0.428 (+5.4%) |
  | V(35 h⁻¹Mpc) | 351 | 355 | ΛCDM 333; Qin CF4TF 380±25 → MI 1.16σ (ΛCDM 1.87σ) |
  | V(100 h⁻¹Mpc) | 213 | 215 | ΛCDM 202; Qin W09 410±80 → MI ~2.5σ low (NOT cured) |

- **Honest both ways.** The overshoot is **not manufactured** — its source (|a_pec|²) is second order,
  so the reading-(a) counterfactual (σ₈ blown up 10³–10¹⁶×) is correctly *excluded*, not invoked. The
  distinctive middle is **not smuggled** — linear PT yields no k-dependence and no enhanced signal; if
  anything, fixing u^i=0 leans *toward* degeneracy. The W09 large-scale bulk-flow excess is **not
  cured** (ΛCDM ~2.6σ low → MI ~2.5σ low), reported straight.

**Verifier language correction applied (VERIFY.md V4 — now reflected in `perturb_mi.py` PART B and
`PERTURBATION.md` §3):** the write-up's original "the perturbed □_u DERIVES reading (b)" was
**overstated** and has been softened. What is **rigorously derived**: (a) |a_pec|² is ≥2nd order (PART
A), and (b) a₀=cH_Λ/Z plus the pole floor κ_eff≥H_Λ **algebraically force** X≥Z²≈33.5, hence ν∈[1,1.09]
at z=0 **regardless** of the H_Λ-vs-H(z) choice — a distinctive ν (e.g. ν=2) would need a₀≳10×
canonical, excluded by the a₀=cH_Λ/Z definition itself. What is **imported/assumed**: the specific
*rising* floor Z²(H(z)/H_Λ)² rests on the frozen dS-Unruh pole κ_eff²=H²+(a/c)² (derived on **constant-H**
de Sitter, PULLBACK.md) plus an adiabatic H_Λ→H(z) substitution, because this pass fixes u^i=0 rather
than dynamically carrying a velocity-sourced δu; "no k²" is a sound *structural* argument, not an
explicit δ(□_u) computation. **This does not change the verdict:** the MI-off/degenerate conclusion holds
for any H≥H_Λ.

## 3. bracket_collapsed — the fork-decider's free closure is COLLAPSED for the linear sector, still OPEN beyond it

The fork-decider (wjcrfsp1t) said MI cosmology is DEAD (bare first moment → σ₈ 8.5–9.9× Planck) or
LCDM/AeST-DEGENERATE (horizon-floored, MI off), and that **which prong the growing mode takes was a free
gap-A closure no worldline argument could pin.** This pass **collapses that bracket for linear scalar
perturbations**: the choice is *not* free — the demotion of |a_pec|² to second order (rigorously derived,
PART A) plus the algebraically-forced floor X≥Z² (from a₀=cH_Λ/Z) **select the DEGENERATE prong and
exclude the DEAD prong** in linear theory. The middle (viable-and-distinctive) does not appear.

**Caveat on the collapse (honest):** it is collapsed *robustly in magnitude* (ν∈[1,1.09] is forced),
but the derivation is **partial** — the rising-floor *form* and "no k²" rest on the imported pole +
adiabatic reading + the u^i=0 choice, not a full dynamical δ(□_u). And the bracket is **still open beyond
linear order**: the (a_pec/a₀)² term first enters at **second order/quasilinear**, which is exactly where
a distinctive MI signal — if any exists — must live. So: **linear-sector fork collapsed to degenerate;
quasilinear fork still open.**

## 4. next

1. **Second-order / quasilinear MI growth** — carry (a_pec/a₀)² to the order where it first enters
   (loop/mode-coupling); this is the *only* place a distinctive, k-dependent MI signal can appear and is
   the named open computation the linear pass defers to.
2. **Dynamical δ(□_u) with a velocity-sourced δu** — redo the crux without fixing u^i=0, to *derive*
   (not import) the rising floor and the "no k²" structure, closing the V4 language gap at the
   computation level.
3. **Condensate-baryon dressing on the growing mode** — resolve whether ν dresses baryons only or
   baryons+condensate, with the condensate's own AeST perturbations (Skordis–Złośnik) responding; the
   present ν·Ω_m=0.315 treatment is a first-pass proxy (few-% either way, does not inflate).
4. **Measurement-grade σ₈/bulk-flow** — CAMB transfer + proper windows to replace the BBKS/top-hat
   sanity-level absolute V(R) (the MI-vs-ΛCDM *ratio* is already robust; only absolutes are affected).
5. Full nonlocal K(□_u) time-response beyond the first-moment/pole reduction; vector/tensor sectors;
   nonlinear scales. **s=−1 and a₀'s value/footing remain postulated (both footings carried, neither
   derived).**

---

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_covariant_pt && python3 perturb_mi.py &&
python3 solve_growth.py` (both exit 0; 17/17 + 12/12). **Credits:** Skordis–Złośnik 2021 (AeST/
ghost-condensate CMB-safe background + dark sector), Nusser 2002 (deep-MOND linear growth counterfactual),
Qin 2021 (bulk-flow confrontation). Frozen source repo left READ-ONLY.
