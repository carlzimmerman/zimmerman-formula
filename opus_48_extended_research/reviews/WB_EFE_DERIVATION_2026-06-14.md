# Wide-binary gamma(s) derived from first principles WITH the Milky Way EFE

*Opus 4.8 (1M) extended-research, 2026-06-14. Route [wb_efe_derivation]. Framework a0 = c^2 sqrt(Lambda/32pi) =
9.355e-11 m/s^2 (Lambda-only), realized covariantly by AeST. The derivation is AQUAL/QUMOND-standard; the framework's
ONLY input is the lower a0. Scripts: /tmp/wb_efe_fix.py, /tmp/wb_efe_aqual.py, /tmp/wb_efe_final.py (reproducible).
Grade: DERIVATION-SHARP — clean derivation, pins a testable prediction; the framework's lower a0 makes a falsifiable,
distinct gamma_cap.*

## The setup (why a solar-neighborhood binary is EFE-dominated, not deep-MOND)

A wide binary near the Sun sits in the Milky Way's external field:

    g_ext = V_c^2 / R0 = (233 km/s)^2 / (8.178 kpc) = 2.151e-10 m/s^2.

This is LARGER than a0 in both conventions, so the binary is **EFE-dominated** (quasi-Newtonian with a renormalized G),
not in pure deep-MOND. The decisive number is g_ext in units of a0:

| convention            | a0 (m/s^2)  | e = g_ext/a0 |
|-----------------------|-------------|--------------|
| framework (Lambda)    | 9.355e-11   | **2.300**    |
| standard MOND/McGaugh | 1.20e-10    | 1.793        |
| Chae 2024 (his fit)   | 1.20e-10    | 1.90 +/- 0.19 |

**The framework's lower a0 RAISES e to 2.30.** A larger external field (in a0 units) Newtonizes the binary MORE, so the
framework predicts a SMALLER boost than standard MOND. This is the load-bearing physics of the whole route.

## The derivation (AQUAL anisotropic G_eff, Bekenstein-Milgrom 1984 / Banik-Zhao 2018)

Deep inside a system (g_int << g_ext) in a dominant external field, AQUAL linearizes to an **anisotropic** effective
Newton constant. Writing e = g_ext/a0, mu the AQUAL interpolation, L_mu = d ln mu / d ln x at x=e:

    G_par / G  = 1 / [ mu(e) (1 + L_mu) ]      (along g_ext)
    G_perp / G = 1 / mu(e)                      (perpendicular)

A wide-binary orbit samples all orientations relative to g_ext, so the observable is the orbit/angle average:

    gamma_cap = <G_eff/G> = (1/3) G_par/G + (2/3) G_perp/G.

For the **simple (Famaey-Binney) mu(x) = x/(1+x)** — the function Chae and the AQUAL fits actually use:

| convention | e=g_ext/a0 | mu(e) | L_mu | G_par/G | G_perp/G | **gamma_cap** | v/v_N |
|---|---|---|---|---|---|---|---|
| **framework** | 2.300 | 0.697 | +0.303 | 1.101 | 1.435 | **1.324** | **1.150 (+15.0%)** |
| standard a0 | 1.793 | 0.642 | +0.358 | 1.147 | 1.558 | **1.421** | 1.192 (+19.2%) |

For the sharp standard mu(x)=x/sqrt(1+x^2) the boost nearly vanishes (gamma_cap ~ 1.04 framework / 1.07 standard) —
the interpolation function is the dominant systematic, exactly as in the rotation-curve case.

**Cross-check:** the simpler nu-form QUMOND angle-average gamma = nu(e)[1 + L_e/3] gives 1.240 (framework) / 1.295
(standard) — about 6-9% below the rigorous mu-form tensor. The mu-form anisotropic AQUAL result (1.324 / 1.421) is the
correct one and is what Chae quotes; the nu-form is a 1-D approximation that undercounts the perpendicular enhancement.
I report the mu-form as the prediction and flag the ~0.08 nu-vs-mu spread as a method systematic.

## The gamma(s) curve (rises from 1 -> EFE cap)

gamma(s) = G_eff/G rises monotonically from 1 (close, Newtonian, g_int >> g_ext) to the EFE cap (wide, g_int << g_ext).
Internal field g_int(s) = G M / s^2 for a 1.5 Msun pair; the transition g_int = g_ext is at s_3D = 6.4 kau
(s_proj ~ 5 kau after the median 3D/projected factor 1.27) — matching Chae's observed onset at 2-5 kau.

| s_proj (kau) | g_int/a0 (fw) | g_int/g_ext | gamma(s) framework | gamma(s) standard a0 |
|---|---|---|---|---|
| 3  | 6.55 | 2.85 | ~1.07 | ~1.10 |
| 5  | 2.36 | 1.03 | ~1.15 | ~1.19 |
| 10 | 0.59 | 0.26 | ~1.25 | ~1.32 |
| 20 | 0.15 | 0.06 | ~1.30 | ~1.39 |
| inf (cap) | 0 | 0 | **1.324** | **1.421** |

(Curve endpoints — gamma=1 close, gamma_cap wide — are exact AQUAL; the interior blend is a smooth interpolation, not a
full orbit integration. The CAP is the robust, falsifiable prediction; the rise location is set by s_t.)

## Uncertainty budget (Monte Carlo, N=2e5)

- **Cosmological (a0 via Lambda):** Omega_L, H0 give d a0/a0 ~ 0.6% -> +/-0.01 on gamma_cap. Negligible.
- **g_ext (V_MW = 233+/-6 km/s, R0 = 8.178+/-0.022 kpc):** +/-0.02 on gamma_cap (the 16-84 band 1.307-1.342, framework).
- **Interpolation function (simple vs standard mu):** gamma_cap in [1.04, 1.32] — **DOMINANT systematic**, same as RAR.
- **Mass (1.5+/-0.15 Msun):** shifts the rise location s_t ~ M^1/2, NOT the cap.
- **Projection (s_3D/s_proj ~ 1.27):** shifts the curve in s, NOT the cap.

## Comparison to data and the framework's distinctive prediction

Chae 2024 measures **gamma = 1.49 +/- 0.2** (consistent with AQUAL nominal ~1.4), calibrated to **his a0 = 1.2e-10**.
- Standard a0 -> gamma_cap = 1.421: a near-perfect match to Chae (0.3 sigma).
- **Framework a0 = 9.36e-11 -> gamma_cap = 1.324**: 0.8 sigma BELOW Chae's central value, but comfortably inside his
  +/-0.2 band. Not excluded; sits at the lower edge.
- Inverse: Chae's gamma=1.49 prefers a0 ~ 1.39e-10 (simple-mu, this g_ext); gamma=1.40 prefers a0 ~ 1.14e-10; the
  framework's 9.36e-11 lands at gamma ~ 1.32.

**This is the framework's distinctive, falsifiable WB prediction: gamma_cap = 1.32 +/- 0.02 (cosmo+g_ext), simple-mu,
vs 1.42 for standard a0.** The ~0.1 difference in gamma_cap (a clean ~7%) is a DIRECT consequence of the framework's
20% lower a0 raising e from 1.79 to 2.30. A precise WB measurement of gamma_cap that lands firmly at 1.4-1.5 mildly
DISFAVORS the framework a0; one landing at 1.30-1.35 mildly FAVORS it over standard MOND. Gaia DR4 3D velocities are the
arbiter.
