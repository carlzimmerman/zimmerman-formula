# Model-free diagnostics and degeneracy structure for Gaia wide-binary gravity tests

**DRAFT — hold for Carl + Fable review before any circulation.** *C. Zimmerman, 2026-06-10. A methods note, written for
**both** sides of the Chae–Banik dispute. It introduces no new gravity claim and advocates for no theory; the acceleration
scale a₀ enters only as a binning variable, and we show the conclusions are insensitive to its value. All numbers are from
real Gaia eDR3 wide binaries (El-Badry, Rix & Heintz 2021, Zenodo 4435257), reproduced by the committed scripts cited inline.*

## 0. The dispute, and what this note adds
On the same Gaia wide-binary data, Chae (2023, 2024) reports a low-acceleration velocity boost (~5σ, MOND-like) while Banik
et al. (2024) report a Newtonian null (~16–19σ against MOND). The disagreement is not about the photons; it is about
**estimator and modeling**. This note isolates four **model-free diagnostics** (D1, D2, D4, and the scale-free structure of
the projected observable) that any wide-binary gravity test must pass or report, and shows that the present sky-projected
DR3 data are **degeneracy-limited**: the deep-acceleration signal and its leading systematics are not separable in this
observable. The central fork is **velocity treatment** — Chae deprojects to 3D (Monte-Carlo over inclination, eccentricity,
phase), Banik works with the sky-projected ratio (his Appendix E documents the velocity-treatment choice explicitly). We do
not adjudicate the dispute; we map the structure that makes it hard and propose the Gaia DR4 gate that resolves it.

## 1. The observable and its scale-free core
Per pair, ṽ ≡ v_sky / √(GM/r_sky), with v_sky the sky-projected relative velocity and r_sky the projected separation.
For a Keplerian orbit, writing the orbital-plane position p and velocity v in units of a and √(GM/a) and projecting with
random orientation, the node angle drops out of the sky-plane norms and
  **ṽ = ν_sky · √(ρ_sky)**,  a function of **(eccentricity, orbital phase, viewing orientation) ONLY** — independent of M and a.
*Consequence:* a Newtonian population predicts a **flat** median ṽ across every g_N/a₀ bin (circular face-random ⇒ ṽ ≈ 0.63,
matching the observed high-acceleration ≈0.56). **Any rise into low acceleration must come from one of four sources — noise
(D1), contamination (D2/triples), separation-dependent eccentricity, or a genuine boost — and only the last is new physics.**
(Script: `wb_deprojection_mc.py`.)

## 2. D1 — noise-folding inflation
v_sky is a magnitude: the measured sky velocity is the **norm** of a 2D proper-motion-difference vector carrying Gaussian
noise. With per-component error σ_v, the observed magnitude folds (Rice/Eddington):
  ṽ_obs = | ṽ_true·û + (σ_ṽ) g | ,  g ~ 𝒩(0, I₂),  σ_ṽ ≡ σ_v / v_N.
Because v_N = √(GM/r_sky) is **smallest in the widest (deepest) bins**, σ_ṽ is **largest there**, so the fold inflates the
median ṽ preferentially in deep-acceleration bins — manufacturing a rise from a flat intrinsic distribution. **D1 ≡ median
σ_ṽ in the deep bins.** On the faithful Banik-exact sample D1 ≈ 0.12–0.15 — *the same order as the +2–11% boost the test is
trying to detect.* A symmetric-scalar noise model (adding noise to ṽ directly) MISSES this — it does not shift the median;
only the 2D-vector fold does. This is the dominant reason a Newtonian sample shows a deep-bin rise at all.

## 3. D2 — the escape bound, and why it is theory-laden
A bound pair cannot exceed its escape ratio v_esc/v_c. **Under Newton this is √2 ≈ 1.414.** Under the framework's
EFE-suppressed deep-MOND dynamics the potential is deeper and the bound is **higher and anisotropic** in the external
galactic field g_ext: ≈ **1.42 parallel** to g_ext, ≈ **1.65 perpendicular**, ≈ **1.55 angle-averaged**. **D2 ≡ fraction with
ṽ > threshold.** Pairs with **√2 < ṽ < 1.65 are unbound (contamination) under Newton but bound (a boosted population) under
MOND** — the *same pairs*, classified oppositely by hypothesis. Measured deep-bin D2: 0.098 (√2) → 0.078 (1.55) → 0.070
(1.65). **The contamination "demand" is therefore hypothesis-dependent**; the inferred triple fraction is numerically robust
(~0.19–0.20 either way, because each triple's contribution above threshold falls in step) but its *meaning* — junk vs signal —
is not. Any super-escape-based cleaning argument must state which threshold it assumes. (Script: `wb_threshold_audit.py`.)

## 4. D4 — the mass-sensitivity (escape) test
Could a separation-dependent **mass** error masquerade as the velocity trend (low masses → low v_N → high ṽ)? Rescale M_tot
by ±10% and by a separation-tapered bias and recompute the super-escape fraction. **Result: the deep-bin super-escape moves by
1.3–1.4× — below the 1.5× alarm — i.e. NOT mass-limited.** This holds for the Chae-exact and Banik-exact selections alike and
does not require DR4 masses. (Scripts: `wb_exact_replication.py`.) *Caveat owned: an earlier pass inverted the Banik mass
cubic outside its valid M_G∈[0.6,11.1] window, inflating velocities and producing a spurious ~0.48 super-escape; corrected,
the faithful value is ~0.10. Both the bug and the retraction are logged in `WB_R1_EXACT_REPLICATION.md`.*

## 5. The selection ladder (provenance for the numbers)
| Selection | N | deep D1 σ/v_N | deep D2 super-escape (√2) | D4 mass-sensitivity |
|---|---|---|---|---|
| loose hybrid | 73,670 | 0.306 | 0.267\* | — |
| Chae-exact (cuts) | 24,111 | 0.117 | 0.097 | 1.40× |
| Banik-exact | 9,508–10,751 | 0.148–0.154 | 0.098 | 1.32–1.34× |

\*The loose-hybrid 0.267 and an earlier 0.48 are mass-/selection-inflated artifacts, retracted (§4). The faithful samples
agree at D2 ≈ 0.10. Three Banik cuts are not reproducible from the eDR3 catalog (astrometric χ²/ν eq.4; faint-companion
search to m_G<20; DR3-RV triple screen) — logged as catalog/data-availability gaps; the residual count offset is in the
conservative (looser → more contaminated) direction.

## 6. The boost↔contamination degeneracy
Calibrating the Newtonian forward model on the high-acceleration anchor (where the boost is ≈0) fixes the eccentricity prior
and the triple fraction; the deep bins are then a *prediction*. The deep-bin data sit ~3σ above the flat-contamination Newton
baseline — **and that excess is fully absorbed** by a separation-dependent triple fraction (~0.16 in the deep bins) that
*independently* reproduces the measured super-escape. The lone exception is the deepest bin (N=104), whose residual is
**≈1.7–2.4σ standalone — not significant.** So the sky-projected data **do not require** a boost, and **do not exclude** a
mild one: the two hypotheses are not separable in this observable.

## 7. The orbital-prior sensitivity (this weakens everyone's significances)
Replacing the boost-at-fixed-orbit approximation with a real central-force **orbit integration** (potential built from the
effective gravity; orbit roulette sampled by time) reveals that the predicted deep-bin ṽ is **sensitive to the unconstrained
3D semi-major-axis prior**: eccentric orbits with deep-acceleration apocentres seen near pericentre leak boost into
high-acceleration bins, and a Newtonian cross-check fails to reproduce its own baseline under a flat log-a prior. **Implication
for the field:** every published WB significance — the ~16–19σ null and the ~5σ boost alike — inherits an orbital (a, e)
library that the sky-projected data do not pin. WB significances are **orbital-prior-limited**, not just noise-limited.
(Script: `wb_mond_orbit_mc.py`.)

## 8. a₀ enters only as a binning scale (insensitivity check)
Repeating the deep-bin diagnostics with a₀ = 1.2×10⁻¹⁰ (standard MOND) instead of 9.36×10⁻¹¹ (the framework value) changes
nothing material: D1 0.154→0.149, D2 0.098→0.088, **median ṽ 0.661→0.661**. The diagnostics and the degeneracy are properties
of the *data and the projection*, not of any chosen acceleration scale. (Output: `wb_a0_insensitivity.out`.)

## 9. The Gaia DR4 gate (proposal to both teams)
The degeneracy and the prior-sensitivity share one cure: **line-of-sight radial velocities → full 3D relative velocities.**
DR4 (a) collapses the sky-projection that makes boost and contamination inseparable, and (b) constrains the (a, e) orbital
library that §7 shows dominates the error budget. We propose **D1 (noise floor) and the explicit boost↔contamination
degeneracy as gates any DR4 claim must pass**, with the escape threshold stated (Newtonian √2 vs EFE-suppressed 1.42/1.55/1.65)
and the orbital prior reported, not assumed. Until then the honest status is **null-informative / degeneracy-limited**.

## References (to complete on finalize)
Chae 2023 (ApJ 952 128, arXiv:2305.04613); Chae 2024; Banik et al. 2024 (MNRAS 527 4573, arXiv:2311.03436), incl. **Appendix E**
(velocity treatment); El-Badry, Rix & Heintz 2021 (MNRAS 506 2269); Pittordis & Sutherland 2019, 2023; Hwang et al. 2022
(eccentricity–separation). *Framework context (a₀ = 9.36×10⁻¹¹) appears only as the §8 binning-scale check and is not load-bearing.*
