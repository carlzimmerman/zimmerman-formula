# LANE SOLVE — MI cosmology consequences from the DERIVED growing-mode argument

**Verdict: VIABLE-BUT-AeST/ΛCDM-DEGENERATE.** Date 2026-07-17.
Script `solve_growth.py` (numpy/scipy, exit 0, **12/12** numeric checks). Figure `mi_pt_fig.png`.
Driven by the argument DERIVED (not posited) in `perturb_mi.py` / `PERTURBATION.md` (17/17). Both a₀
footings carried: **canonical a₀ = cH_Λ/Z = 9.36×10⁻¹¹** (ρ_DE), **alt a₀ = 1.13×10⁻¹⁰** (ρ_tot/cH₀),
Z = √(32π/3) = 5.78881.

**Credit.** Skordis–Złośnik 2021 (PRL 127:161302) — the CMB-safe AeST/ghost-condensate realization the
background + dark sector are built on; this lane adds only the MI kernel's effect on the matter growing
mode. Nusser 2002 (MNRAS 331:909) — deep-MOND linear growth, the reading-(a) overshoot counterfactual.
Qin 2021 — the bulk-flow measurements used as the confrontation.

---

## What this lane computes

The perturbation lane DERIVED that the linear growing mode's kernel sees the **dS-Unruh Hubble FLOOR**,
scale-independent, with the bare peculiar-acceleration term demoted to second order and no k² term:

$$X = \frac{\Box_u}{a_0^2}\Big|_{\text{grow}} = \underbrace{Z^2\Big(\frac{H(z)}{H_\Lambda}\Big)^2}_{\text{floor (b), dominates}} + \underbrace{\Big(\frac{a_{\rm pec}}{a_0}\Big)^2}_{\text{2nd order, }\lesssim3\%} \;\Rightarrow\; G_{\rm eff}(a)=\nu\!\big(X_{\rm floor}(a)\big)\,G,\quad \nu=1/K,\ K(X)=\frac{\sqrt{1+4X}-1}{2\sqrt X}.$$

This lane solves the **consequences** of that argument and confronts data:
growth ODE δ″ + (2 + dlnH/dlnN)δ′ − (3/2)Ω_m(a)ν(X_floor(a))δ = 0, integrated a = 10⁻³→1 (growing-mode
IC), against a ΛCDM baseline (ν≡1); σ₈ from a BBKS-normalized linear P(k) (scale-independent
enhancement ⇒ σ₈_MI = σ₈_ΛCDM·D_MI(1)/D_ΛCDM(1)); fσ₈(z); top-hat bulk flow V(R).

## Results (both footings)

| observable | canonical | alt | ΛCDM / data |
|---|---|---|---|
| X_floor(z=0) | 48.9 | 33.6 | — |
| ν(z=0) = 1/K | 1.074 | 1.090 | 1 (MI off) |
| D_MI/D_ΛCDM(z=0) | 1.022 | 1.027 | 1 |
| **σ₈** | **0.829** | **0.833** | Planck ΛCDM **0.811** |
| f(z=0) | 0.544 | 0.547 | 0.527 |
| fσ₈(z=0) | 0.451 (+5.4%) | 0.453 | 0.428 |
| V(35 h⁻¹Mpc) | 351 km/s | 355 | ΛCDM 333; **Qin CF4TF 380±25** |
| V(100 h⁻¹Mpc) | 213 km/s | 215 | ΛCDM 202; **Qin W09 410±80** |

- **σ₈ +2–3%, f within ~3%, fσ₈ +5%** — a smooth, scale-independent, few-percent late-time boost,
  **absorbable into ΛCDM/AeST normalization**, not a distinctive signal.
- **Bulk flow tracks ΛCDM** (few-% above it). At 35 h⁻¹Mpc, MI V=351 is **1.16σ** from the Qin CF4TF
  point (ΛCDM is 1.87σ) — MI is marginally *closer*, still consistent.
- **Honest finding — the W09 410±80 @ 100 h⁻¹Mpc large-scale bulk-flow excess is NOT cured.** ΛCDM
  sits ~2.6σ low there; MI's few-% boost leaves it ~2.5σ low (would need ~2×). The MI enhancement does
  not resolve the known large-scale bulk-flow tension — reported straight, not oversold.

## The fork, resolved (honest both ways)

- **Reading (b), the DERIVED floor → what we solved above:** viable, degenerate, few-%. **Not** the
  "exciting middle" (viable-*and*-distinctive) — the linear PT gives no k-dependent or enhanced signal,
  so that middle is **not smuggled in**.
- **Reading (a), the bare first moment (counterfactual):** deep-MOND ν = 1/K((a_pec/a₀)²) → σ₈ blows up
  by **10³–10¹⁶×** (a_pec = 0.3–0.03 a₀) — the "MI DEAD" overshoot. **But** the PT (`perturb_mi.py` A5)
  demoted |a_pec|² to a *second-order* source, so **linear PT does not select it.** The overshoot is
  real *if* the bare argument were seen; the PT shows it is not. **Not manufactured.**

## Ledger

| # | check | status |
|---|---|---|
| S0 | a₀ canonical = cH_Λ/Z = 9.36e-11 | PASS |
| S1 | X_floor(z=0,can) = Z²/Ω_Λ (analytic) | PASS |
| S2/S2′ | z=0 MI enhancement few-% (MI nearly off) both footings | PASS |
| S3 | P(k) normalized to ΛCDM σ₈=0.811 | PASS |
| S4-can/alt | σ₈ boost modest (1<ratio<1.15), not overshoot | PASS |
| S5 | fσ₈(z=0) within few-% of ΛCDM (RSD-degenerate) | PASS |
| S6 | MI bulk flow tracks ΛCDM at 35 h⁻¹Mpc | PASS |
| S6′ | V(35) consistent with Qin CF4TF (<1.5σ; MI closer than ΛCDM) | PASS |
| S7 | W09 410@100 tension PERSISTS in MI (not cured) | PASS |
| S8 | counterfactual reading (a) overshoots σ₈ >3× (MI-DEAD, excluded) | PASS |

## Open (flagged — beyond this first pass)

Condensate-baryon coupling and its own PT; the full **nonlocal** K(□_u) time-response beyond the
first-moment/pole reduction; vector/tensor sectors; **second-order / quasilinear** growth where the
(a_pec/a₀)² term first enters — the distinctive MI signal, *if any*, lives there, not in linear theory;
nonlinear scales. **s = −1 and a₀'s value/footing remain POSTULATED.** No "proves"/"closed"/TOE.

---

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_covariant_pt && python3 solve_growth.py`
(exit 0, 12/12). Upstream: `perturb_mi.py` (17/17, derives the argument), `PERTURBATION.md`. Both a₀
footings throughout. Frozen source repo read-only.
