# Are the cluster measurements wrong? The baryon-census audit — SHAVES but does NOT close (residual ~1.6 survives)

*Workflow `w65dpw6uo` (5 agents: 3 parallel route audits → adversarial verify → synthesis), banked
2026-06-20. Carl's question — is the ~1.6–1.8 residual a MEASUREMENT artifact? Verified independently
from the raw eRASS1 FITS (N=9830). Both-ways: every real systematic credited at honest 2024–26
magnitude AND the cosmic f_b ceiling held. The one error found was corrected AGAINST the framework
(the surviving residual is slightly HIGHER). Quarantine: a0=9.36e-11 INPUT.*

## Verdict: the residual is NOT a baryon-census artifact — it is a REAL, ceiling-bounded, shared-MOND gap.

## (0) The composition cap that governs everything (reproduced to the digit)
Real eRASS1 @ R500: **f_gas=0.067, f_star=0.013, f_bar=0.081 = 0.52× cosmic.** **Stars are only 16.7%
of the baryon budget; gas is 83%.** So every stellar-side channel (IMF, ICL) multiplies a piece that
is one-sixth of the baryons — budget-capped before it starts. And the X-ray census is itself DEPLETED
to half-cosmic (eROSITA gas fractions ~2× below sims; feedback-expelled to >R500, Siegel+2025
arXiv:2509.10455).

## (1) Each systematic, honest magnitude, and SIGN
| channel | magnitude (2024–26 lit) | ΔM_bar/M_bar | sign on η |
|---|---|---|---|
| Bottom-heavy IMF (BCG/ETG) | M/L ×1.2–1.6 (Loubser+, Conroy-vanDokkum) | +3.3% to +10.0% | LOWERS |
| ICL under-count | +10–50% of stellar light (The Three Hundred) | +1.7% to +8.4% | LOWERS |
| Cold/molecular gas+dust | <1% of hot ICM | +0.8% | negligible |
| **X-ray clumping** | √C<1.1 @ R500, M_gas biased HIGH ×1.06 | **−4.7%** | **RAISES (wrong sign)** |
| **Missing baryons** | f_b,500~0.11–0.146 vs 0.156, but located **>R500** | **0% at R500** | none |

Two honest subtleties, reported straight: **clumping has the WRONG sign** (de-clumping removes ~6% gas,
raises η ~5%, partly cancelling the IMF+ICL gain); **the missing baryons are MEASURED to be feedback-
expelled to >R500**, so they cannot lower the enclosed g_bar(R500) — they get 0, not a counterfactual
cram-inside.

## (2) The sum, bounded by f_b — and the skeptic's correction AGAINST the framework
**Corrected shave law:** the route used linear η∝1/(1+δ); but the banked residual is
η_resid=(g_obs/g_bar)/ν_frame(g_bar), so adding baryons RAISES g_bar → RAISES ν in the denominator →
partly cancels the gain. Recomputed on the real eRASS1 array:
- PHYSICAL stack δ=+0.061 → shave **0.9696** (not the route's linear 0.9425)
- GENEROUS stack δ=+0.175 → shave **0.9190** (not 0.8511)

**Corrected surviving η** (from the post-hydro+Y-Q start band 1.6–1.8):
- **PHYSICAL census: η → 1.55–1.75 (mid 1.65)**, f_bar=0.086=0.55× cosmic
- **GENEROUS census: η → 1.47–1.65 (mid 1.56)**, f_bar=0.095=0.61× cosmic
- **MAX conceivable** (IMF×2 + ICL+50%): f_bar=0.102 = **0.65× cosmic** — ceiling never threatened.

## (3) Close or stay? — STAYS, two independent walls
- From the high anchors (gas-only 2.57 / WL 2.33): closure to ~1.15 needs f_bar=0.180/0.164 =
  **1.16×/1.05× cosmic → HARD f_b VIOLATION.**
- From the post-Y-Q ~1.6–1.7 end: the needed baryons are **measured at >R500** → cannot touch
  g_bar(R500). Blocked by radial LOCATION, not arithmetic.
- The deep-MOND outskirt formally "closes" only at ~4 Mpc (beyond turnaround, HSE/NFW broken) — an
  unphysical aperture, reported straight, not an R500 escape.

Route C (η footing) separately confirmed: **η(R500) is robust, not a metric artifact** — the residual
survives the radial-profile / acceleration-metric choice.

## (4) Biggest systematic + what would pin it
**The IMF (bottom-heavy stellar M/L in cluster ETGs/BCGs) is the largest LOWERING channel** (+3.3% to
+10%), narrowly ahead of ICL — but **structurally capped by the 17% stellar fraction** (even IMF×2 alone
adds only ~+17% of M_bar). **Pin it with:** cluster-wide mass-weighted IMF (JWST/Euclid resolved
stellar-pop + dynamical M/L across BCG+satellites+ICL, not BCG cores), replacing the assumed 0.2×gas
stellar budget. Even a maximal pin cannot breach the 0.65×-cosmic wall. (De-clumping matters next-most
but RAISES η; the kSZ+WL missing-baryon location is the both-ways anchor that blocks cram-inside-R500.)

## (5) Honest verdict for Carl
**The cluster residual is NOT a baryon-census measurement artifact.** The fuller census + the corrected
nonlinear law shaves η modestly (physical ~3%, generous ~8%), landing the surviving residual at **η ~
1.5–1.7 (central ~1.6)** — still well above 1.3, exactly as the hard f_b constraint predicted. The route
was directionally right and structurally sound; its only flaw over-stated the shave, so the true
residual is marginally HIGHER. This gap is MI ≡ AeST to machine precision (NOT framework-distinctive)
and is NOT a referee-proof kill — but the baryon census cannot make it go away.

### Sources
eRASS1 (Bulbul+2024, erass1cl_primary_v3.2.fits); Siegel+2025 (arXiv:2509.10455); Loubser+2020/21;
Conroy-van Dokkum; Eckert+2015 (clumping); The Three Hundred (ICL). The σ8↔mass direction in
routeB axis-4 is VERIFIED (masses HIGH ⇔ σ8 HIGH; see commit). η baseline 2.334 + a0 quarantine unchanged.

### Scripts (exit 0, under opus_48_extended_research/reviews/cluster_measurement/)
route_a_baryon_census.py · routeB_dynamical_mass_calibration_eta.py · routeC_eta_footing_radial.py
