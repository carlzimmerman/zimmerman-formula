# VERIFY — SNe dark-energy density vs. MI-framework galaxy prediction

Adversarial re-run of `/Users/carlzimmerman/new_physics/prep_2026/sne_lambda/`.
Hunted a manufactured **agreement** and a manufactured **tension** with equal
suspicion. Frozen `a0_line` repo left read-only.

## 0. Re-run (exit 0)
All three scripts re-run clean:
- `setup.py` — EXIT 0
- `sne_extract.py` — EXIT 0
- `predict_diagram.py` — EXIT 0

Every headline number independently reproduced from first principles (constants
`c=2.99792458e8`, `G=6.6743e-11`, `MPC=3.0856776e22`).

## 1. Circularity — is any "agreement" the CANONICAL a0? (kill circular wins)
**Handled, with one soft spot flagged.**
- The canonical a0=9.3548e-11 → rho_DE=5.8355e-27 is, by direct arithmetic,
  **Planck rho_Λ to 0.12%** (Planck Ω_Λ=0.6847, H0=67.4 → 5.8424e-27, ratio
  0.9988). This nails the circularity at the level of arithmetic: canonical
  a0 = cH_Λ/Z was *defined* from a cosmological (Planck) Λ, so its 1.027×/+0.98σ
  "match" to SNe rho_DE re-checks Planck-vs-SNe Λ, **not** the framework. It
  carries zero evidential weight. This is flagged CIRCULAR in every docstring,
  every JSON footing note, and every prose verdict.
- **The genuine headline is the MEASURED a0** (SPARC rotation-curve dynamics
  alone, Λ-blind): GLS 1.638×/+1.53σ (Planck), 1.396×/+1.03σ (SH0ES); median
  1.110×/0.946×. No circular number is used as a headline.
- SOFT SPOT: the JSON field `cases.Planck_67.4.closest_footing = "canonical"`
  reports canonical as "closest" at Planck H0 without an inline circular tag.
  It must **never** be quoted as a win. Of the non-circular footings the median
  (1.110×) is closest at Planck and median (0.946×) at SH0ES — that is the honest
  read, and the prose says so.

## 2. SNe honesty — is the H0 dependence shown?
**Yes.** SNe give Ω_Λ via the diagram SHAPE (q0=Ω_m/2−Ω_Λ=−0.499, accelerating);
the ABSOLUTE rho_DE = Ω_Λ·3H0²/8πG needs H0 because SNe are M_B–H0 degenerate.
Both H0 carried everywhere:
- H0=67.4 (Planck): rho_DE = 5.683e-27 ± 1.54e-28 kg/m³
- H0=73.0 (SH0ES): rho_DE = 6.666e-27 ± 1.80e-28 kg/m³
- **H0 lever alone = (73/67.4)² = 1.173× → SNe rho_DE differs 17.3%** between the
  two H0 (task's "~18%"). The ± is Ω_Λ-only (~2.7%); H0 is an explicitly separate
  axis, not folded into the error bar. Honest.

## 3. "No framework-native SNe formula; background = ΛCDM" — stated, not blurred?
**Stated in all three docstrings, not blurred.** The framework modifies galaxy
INERTIA (a0), not the expansion; Λ is a genuine constant, so H(z) and mu(z) are
STANDARD flat ΛCDM. "rho_DE from SNe" IS the standard extraction. The
`predict_diagram.py` "zero-free-parameter" test plugs the *galaxy-measured Λ* into
the **standard** ΛCDM mu(z) — it is a cross-check of Ω_Λ-from-galaxies, NOT a
framework SNe formula. Not presented as "the framework predicts the supernovae."

## 4. Measured-a0 box error propagated into the sigma-tension?
**Yes.** frac_err(a0) = 1.9026e-11/1.1814e-10 = 16.1% (stat+sys, banked from
`a0_line/fire_slope_results.json` budget_gas, verified identical). rho_DE∝a0² →
sigma_ln(rho) = 2×16.1% = 32.2%. This 32% box **dominates** the significance and
correctly softens it: GLS lands +1.53σ (Planck) / +1.03σ (SH0ES), not a spurious
high-sigma number. Measured a0 inputs match the frozen source exactly
(a0hat=1.1814e-10, a0med=9.7256e-11, tot=1.9026e-11).

## 5. Both footings + both H0?
**Present.** canonical + alt + measured(GLS + median) × {67.4, 73.0}, throughout
`setup.py`, `sne_extract.py`, and `predict_diagram.py`.

## 6. Manufactured agreement AND manufactured tension — equally?
**Both checked; neither sits in a headline.**
- Manufactured AGREEMENT: canonical 1.027×/+0.98σ — CIRCULAR, discounted (§1).
- Manufactured TENSION (symmetric artifact): the **alt** footing shows +15.0σ
  (Planck) / +9.1σ (SH0ES). This is a **zero-error-bar fixed-footing artifact** —
  alt carries no measurement uncertainty, so its log-tension is computed against
  the tiny SNe error alone. It is exactly as unreal as canonical's +0.98σ
  agreement, and for the same reason. It is NOT a headline; the headline is the
  measured a0 with its full 32% box. Flagged so it is never cited as a real kill.
- The `predict_diagram.py` GLS Δχ²=+41 (Planck) is **diagonal-errors-only** and
  uses flat-form d_L with Ω_m+Ω_Λ=1.42≠1 (curvature term omitted) — both inflate
  it. Correctly caveated in-file as "NOT a clean 6-sigma kill; full covariance
  would shrink every Δχ²." The real density tension is +1.0–1.5σ; the diagram is
  harsher on the high GLS tail but that harshness is an artifact of the two
  approximations, not a robust falsification. Honest.

## VERDICT
**PASS — honest both ways.** The SNe extraction is standard ΛCDM (the framework
does not touch the background; no framework-native SNe formula exists). SNe
rho_DE = 5.68e-27 (Planck H0) to 6.67e-27 (SH0ES H0) kg/m³, Ω_Λ=0.666±0.018,
17.3% H0-driven spread shown explicitly. The framework's genuine, Λ-blind,
rotation-curve-measured a0 inverts to rho_DE = 9.31e-27 ± 3.0e-27 (GLS) landing
1.4–1.6× the SNe density at ≤1.5σ (both H0), and 0.9–1.1× for the median variant
(<0.3σ) — a real, independent, factor-level cross-corroboration of the very
dark-energy density Sarkar's SNe-leg critique targets. NOT a proof, NOT a null.
The apparently-perfect canonical match (1.027×) is CIRCULAR (canonical a0 =
Planck rho_Λ to 0.12% by construction) and is correctly given zero weight; the
alt +15σ "tension" is an equal-and-opposite zero-error-bar artifact. No
manufactured win, no manufactured deficit survived.
