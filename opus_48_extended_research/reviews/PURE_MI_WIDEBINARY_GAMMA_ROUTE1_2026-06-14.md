# Route [pure_mi_gamma]: the wide-binary EFE boost on the framework's OWN dS-Unruh MODIFIED INERTIA (no AQUAL, no simple-mu)

*Opus 4.8 (1M) extended-research, 2026-06-14. Framework a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 (Lambda-only; a0/Z NOT
asserted derived). Built PURELY on the dS-Unruh modified-inertia equation of motion mu(|a|/a0) a_vec = F_vec, the
inertia mu = inverse companion of the framework's own nu(y)=sqrt(1+1/y). NO AQUAL field-equation tensor, NO simple-mu.
Scripts: /tmp/mi_efe_dsunruh.py, /tmp/mi_tensor_derive.py, /tmp/mi_identity.py, /tmp/mi_efe_final.py (reproducible,
numpy only). Anchored on banked real_research/reviews/toe_law/mi_f4_widebinary_efe.py + efe_clinch_framework.py.*

## THE HEADLINE

**On the framework's OWN modified inertia, the wide-binary EFE cap is gamma_cap = 1.137 (v/v_N = 1.066, +6.6%) — NOT
1.32 (AQUAL simple-mu, modified gravity) and NOT 1.198 (the banked "dS-Unruh own", which was the pure-tangential limit,
not the orbit-average).** The previously banked headline band 1.20–1.32 is confirmed to be normal-MOND machinery: 1.32 is
the AQUAL anisotropic-G tensor (Bekenstein-Milgrom MODIFIED GRAVITY), and 1.198 is nu(e) on the *total* acceleration
(the perpendicular/tangential response only). The framework's actual MI prediction, orbit-averaged, is **~14% lower than
the AQUAL number.** Milgrom's own statement holds: MI and MG give DIFFERENT EFE predictions, and here the gap is real
(0.137 vs 0.324 over Newton — the AQUAL boost is ~2.4x the MI boost).

## The dS-Unruh modified-inertia law (framework's own, derived explicitly)

The isolated framework relation is g_obs = sqrt(g_N^2 + g_N a0), i.e. g_obs = g_N nu(y), nu(y)=sqrt(1+1/y), y=g_N/a0.
Inverting to the **inertia** form (Milgrom MI: m mu(a/a0) a_vec = F_vec, the inertia coefficient depends on the
particle's TOTAL acceleration magnitude; the force is ordinary Newtonian gravity, linear, no field equation):

    g_obs = sqrt(g_N^2 + g_N a0)  ->  x^2 = y^2 + y  (x=a/a0, y=g_N/a0)  ->  y = (-1+sqrt(1+4x^2))/2
    ==>  mu(x) = y/x = (-1 + sqrt(1+4x^2)) / (2x)      [the dS-Unruh inertia, exact inverse companion of nu]

Verified mu and nu are exact inverse companions (max |mu(nu(y)y)*nu(y)y - y| = 1.8e-15). This mu IS the framework's
own; it is NOT simple-mu x/(1+x) and NOT standard-mu x/sqrt(1+x^2).

## The MI-EFE derivation (NOT AQUAL — differentiate the INERTIA, not a field equation)

A binary star feels F_vec = g_int n_hat + g_ext z_hat (companion + Milky Way; ordinary linear gravity). Its inertia is
set by its TOTAL acceleration: mu(|a|/a0) a_vec = F_vec. The EFE is the linear response of the internal relative motion
to the small internal force g_int, superposed on the dominant external g_ext. This is the JACOBIAN of the map
a_vec -> F_vec = mu(|a|/a0) a_vec, evaluated at the external operating point:

    dF/da = mu(x_op) [ I + L_mu(x_op) a_hat a_hat ],   L_mu = d ln mu / d ln x
    da/dF = (1/mu(x_op)) [ I - (L/(1+L)) a_hat a_hat ]   (the inverse inertia tensor)

**Load-bearing subtlety (this is what the banked routes got wrong):** the operating point is the OBSERVED total
acceleration x_op = a_ext/a0 = nu(e)*e = 2.753, NOT e = g_ext/a0 = 2.298. (The external field g_ext is the Newtonian
force; the star's actual acceleration is the MI-boosted a_ext = nu(e) g_ext.) Evaluating mu at x_op gives the clean
identity 1/mu(x_op) = nu(e), machine-verified.

    boost perpendicular to g_ext (tangential):  gamma_perp = 1/mu(x_op) = nu(e)            = 1.1979
    boost parallel to g_ext      (radial):      gamma_par  = 1/[mu(x_op)(1+L_mu(x_op))]    = 1.0164
    isotropic orbit average:    gamma_cap = (2/3) gamma_perp + (1/3) gamma_par             = **1.1374**

This was confirmed THREE independent ways, all agreeing to <0.001: (i) the analytic inertia tensor; (ii) a full 2D
Newton-iteration solve of the actual vector EOM mu(|a|/a0)a_vec = F_vec with a tiny perpendicular/parallel force
perturbation; (iii) the finite-g_int orbit-averaged Jacobian. The full gamma(s) curve solves the exact 2D EOM at every
orientation and orbit-averages — it reaches the same 1.137 cap from below.

## The gamma(s) curve (framework's own MI, M_tot=1.5 Msun)

| s_proj (kAU) | g_int/a0 | g_int/g_ext | gamma_MI (framework own) | v/v_N |
|---|---|---|---|---|
| 3  | 10.56 | 4.60 | 1.046 | 1.022 |
| 5  | 3.80  | 1.65 | 1.109 | 1.053 |
| 7  | 1.94  | 0.84 | 1.136 | 1.066 |
| 10 | 0.95  | 0.41 | 1.137 | 1.066 |
| 15 | 0.42  | 0.18 | 1.137 | 1.066 |
| 20 | 0.24  | 0.10 | 1.137 | 1.067 |
| cap | 0    | 0    | **1.137** | **1.066** |

g_int=g_ext at s_3D=6.43 kAU -> s_proj~5.06 kAU (deprojection 1.27), 90%-of-cap by s~6 kAU — matches Chae's 2-5 kAU onset.

## The framework's OWN number vs the normal-MOND headline 1.32

| theory class | interpolation | gamma_cap (framework a0) | over Newton |
|---|---|---|---|
| **modified INERTIA (framework dS-Unruh, OWN)** | mu=inv(nu), isotropic avg | **1.137** | **+0.137** |
| modified inertia, pure-tangential limit | dS-Unruh nu(e) | 1.198 | +0.198 |
| modified GRAVITY (AQUAL, Bekenstein-Milgrom) | simple-mu | 1.324 | +0.324 |
| Newton | — | 1.000 | 0 |

**The framework's own MI cap (1.137) is SMALLER than BOTH 1.20 and the normal-MOND 1.32.** The AQUAL simple-mu boost is
~2.4x larger over Newton. The 1.198 figure carried as "dS-Unruh own" in the banked synthesis is the perpendicular-only
(pure-tangential) response — it drops the (1/3)-weighted radial direction whose boost is only 1.016, so the true
orbit-average is 1.137, ~5% below 1.198. **The headline 1.32 was indeed normal-MOND machinery (AQUAL modified gravity);
the framework's modified inertia genuinely predicts less.**

## Robustness (both ways)

- **g_ext (Vc=233+/-6 km/s, R0=8.178+/-0.022 kpc):** gamma_cap = 1.131–1.145. Negligible (~0.01).
- **Cosmological a0 via Lambda:** <0.01 on the cap.
- **Orbit-average weighting (the one real convention choice):** isotropic 3D (2/3,1/3) = 1.137; pure-tangential = 1.198;
  2D-projected (1/2,1/2) = 1.107. The framework's MI cap is **robust in 1.11–1.20**, with the physical (isotropic) value
  1.137. Even the most generous (pure-tangential 1.198) stays well below AQUAL's 1.32.
- **The interpolation/theory-class is STILL the dominant axis:** standard-mu-as-MI would give ~1.04–1.08; the AQUAL MG
  tensor gives 1.32. The framework's own dS-Unruh MI lands at 1.137, between these — and the MI-vs-MG (theory class) gap
  (0.137 vs 0.324) dwarfs the framework-vs-standard-a0 gap within MI (0.037).

## Verdict impact (does the clean-vs-Newton / MOND-degenerate verdict survive?)

**The qualitative verdict SURVIVES but the Newton clinch is THINNER and the MOND-degeneracy is WORSE.**

- **Framework-vs-Newton (the winnable axis):** gap-to-Newton drops from the banked 0.20–0.32 to **0.137**. At the DR4
  target contamination f_t=0.03 (floor +0.036), the signal still clears the floor (0.137 vs 0.036) — **the Newton clinch
  SURVIVES** — but the margin is thinner: at realistic f_t~0.05–0.07 (floor +0.06–0.08) the net is only ~0.05–0.06. DR4
  SNR (N~5000): fw-vs-Newton ~3.6 sigma (well-controlled) / ~2.2 sigma (realistic) — DOWN from the banked 5.3–8.5 sigma.
  Still a detectable super-Newtonian boost, but at the lower end, and contingent on the Saad-Ting deprojection systematic.

- **Framework-vs-standard-MOND:** on pure MI both use the same dS-Unruh inertia, only a0 differs — std-MOND MI cap = 1.174.
  The MI gap is only **0.037**, even SMALLER than the banked 0.05–0.07. **MOND-degeneracy is WORSE on pure MI; wide
  binaries are even more firmly NOT an a0 test.** (And vs AQUAL-MOND specifically, the framework MI sits 0.187 below 1.32
  — but that is a theory-class difference MI-vs-MG, not an a0 difference, so it is not a clean discriminator either.)

- **HIDDEN DISCRIMINATOR opened:** the MI radial/tangential ANISOTROPY (gamma_perp=1.198 vs gamma_par=1.016, a factor
  1.18 split) is a genuine MI-vs-MG signature. AQUAL also predicts an anisotropy but a DIFFERENT one (G_par/G_perp ratio
  differs). A DR4 sample with enough pairs to bin by the angle between the separation vector and the Galactic-center
  direction could in principle separate MI from MG — but this needs the full orientation-resolved velocity field, far
  beyond a cap measurement. Flagged as a forward target, not a current clinch.

## What this means for the corpus

The banked WIDEBINARY_GAMMA_FORWARD_MODEL_SYNTHESIS and FRAMEWORK_GAMMA_S_FORWARD_MODEL caps (1.20–1.32) are
normal-MOND-contaminated: 1.32 = AQUAL MG, 1.198 = the tangential-only MI limit. The framework's clean MODIFIED-INERTIA
prediction on its own terms is **gamma_cap = 1.137 (isotropic), 1.11–1.20 across the orbit-average convention.** This
LOWERS the framework's headline WB boost by ~14% relative to the published 1.32, makes the Newton clinch thinner (3-4
sigma not 5-8 sigma at DR4), and deepens the MOND degeneracy. It does NOT flip the front: WB remain a clean-ish
framework-vs-Newton test (after contamination + deprojection control) and a non-test of a0. Both ways: no manufactured
win (the boost is smaller than published), no manufactured deficit (the boost is still real and super-Newtonian).
Quarantine held: a0/Z never asserted derived; the interpolation/theory-class flagged as the dominant axis throughout.
