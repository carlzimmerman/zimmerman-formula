# Route [framework_gamma]: the per-separation gamma(s) forward model + Gaia DR4 forecast

*Opus 4.8 (1M) extended-research, 2026-06-14. Framework a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (Lambda-only;
a0/Z NOT asserted derived) + dS-Unruh modified inertia + Milky-Way EFE. Script: /tmp/gamma_forward_model.py
(reproducible, numpy only). Builds on banked WB_EFE_DERIVATION, mi_f4_widebinary_efe.py, widebinary_chae2601_confront.py.
Both-ways honesty rule applied: the lower-a0 tension is reported, not buried; no manufactured win, no dismissal.*

## 1. The setup (EFE-dominated, NOT deep-MOND)
g_ext(Sun) = V_c^2/R0 = (233 km/s)^2/8.178 kpc = 2.151e-10 m/s^2 (convention-fixed, footing-independent).
- framework a0=9.36e-11 -> e = g_ext/a0 = **2.298**
- standard a0=1.20e-10 -> e = 1.793

The lower framework a0 RAISES e to 2.30 -> Newtonizes the binary MORE -> SMALLER boost. This is the load-bearing physics.

## 2. The EFE cap (g_int -> 0), three methods x three interpolations (framework a0)
| interpolation | AQUAL-tensor | nu-form-1D | MI-vector |
|---|---|---|---|
| dS-Unruh (framework's OWN) | n/a | 1.137 | **1.198** |
| simple-mu (Chae/AQUAL) | **1.324** | 1.240 | 1.328 |
| standard-mu (sharp) | 1.041 | 1.034 | 1.078 |

Reproduces the banked cap exactly (AQUAL simple-mu = 1.324 fw / 1.421 std). **The interpolation function is the
dominant systematic** (cap spans 1.04 -> 1.33 at fixed a0), identical to the RAR case. The framework's OWN dS-Unruh
interpolation (g_obs=sqrt(g_N^2+g_N a0), nu=sqrt(1+1/y)) gives a SMALLER cap (~1.20), not the 1.32 simple-mu cap that
Chae quotes -- carried honestly throughout.

## 3. The gamma(s) forward model (M_tot=1.5 Msun, framework a0, orbit-averaged MI)
gamma = G_eff/G_N (acceleration ratio); velocity ratio v/v_N = sqrt(gamma). Monotone rise from 1 (close, Newtonian)
to the EFE cap (wide). Transition g_int=g_ext at s_3D=6.43 kau -> s_proj~5.1 kau (deprojection 1.27); 90%-of-cap at
s~6 kau -- matches Chae's observed onset at 2-5 kau.

| s_proj (kau) | g_int/a0 (fw) | g_int/g_ext | gamma dS-Unruh | gamma simple-mu | v/v_N (simple) |
|---|---|---|---|---|---|
| 1.5 | 42.2 | 18.4 | 1.012 | 1.005 | 1.003 |
| 3   | 10.6 | 4.60 | 1.046 | 1.017 | 1.008 |
| 5   | 3.80 | 1.65 | 1.123 | 1.032 | 1.016 |
| 10  | 0.95 | 0.41 | 1.197 | 1.051 | 1.025 |
| 20  | 0.24 | 0.10 | 1.198 | 1.061 | 1.030 |
| inf (cap) | 0 | 0 | **1.198** | **1.327** | **1.152** |

Note: the per-separation **1D radial QUMOND** (the simple column) saturates low (~1.06) because it samples only the
field-PARALLEL G_par; the orbit-AVERAGED MI/AQUAL value (2/3 weight on the larger G_perp) is the physical observable
and reaches the ~1.32 cap. The MI-vector orbit-average is the forward model carried.

**Headline gamma in the discriminating regime (5-20 kau), simple-mu, orbit-averaged:**
| interp | framework | standard a0 | gap (MOND-fw) |
|---|---|---|---|
| dS-Unruh (own) | 1.198 | 1.248 | +0.050 |
| simple-mu | **1.327** | **1.397** | **+0.071** |
| standard-mu | 1.079 | 1.118 | +0.039 |

## 4. What Gaia measures + deprojection
Gaia measures sky-projected relative proper motion -> plane-of-sky relative velocity. Chae's gamma is the
regime-averaged G_eff/G from the velocity statistic via Keplerian deprojection. Map: v/v_N = sqrt(gamma).
Framework headline (simple-mu, 12 kau): gamma=1.326 -> **v/v_N = 1.152 (+15.2%)**. The cap is reached deep in the
EFE regime (g_int negligible), so it is deprojection-robust; the 3D/projected factor 1.27 shifts the rise LOCATION
in s, not the cap.

## 5. Contamination model (the dominant systematic: hidden tertiaries)
Pittordis-Sutherland 2023 / Manchanda-Sutherland 2025: the high-velocity tail is faked by ~20% flybys + a
hidden-tertiary population (close to 50% of apparent WBs must host an unresolved 3rd star to reproduce the tail).
A hidden tertiary INFLATES the relative velocity -> one-sided POSITIVE bias on inferred gamma, exactly degenerate
with a gravity boost. Bias slope b~1.2/unit f_t (Pittordis-calibrated: f_t=0.5 fakes the full +0.6 over-Newton tail):
| residual tertiary f_t | Delta gamma_inferred |
|---|---|
| 0.30 (raw El-Badry) | +0.36 |
| 0.10 | +0.12 |
| 0.07 (Chae cleaned) | +0.084 |
| 0.03 | +0.036 |

At RAW tertiary levels (f_t~0.3-0.5) contamination ALONE gives Delta gamma~+0.4-0.6, LARGER than the entire
framework signal (gamma_fw-1=0.32). **Contamination control is the whole game.** Chae's cleaned f_t~0.07 leaves a
residual bias ~+0.08, COMPARABLE to the framework-vs-MOND gap (0.07).

## 6. Gaia DR4 SNR forecast
Calibration: Chae N=36, sigma_gamma=0.155 -> per-pair effective scatter sigma_pp=0.93 (folds in eccentricity/phase/
projection + residual contamination). DR4 clean-3D deep-bin sample (El-Badry 1.3M bound pairs; Chae 2025 3D already
N=312) forecast O(2000-10000) after triple cuts + DR4 RVs.

**Pure statistics (optimistic ceiling):**
| sample | N | sigma_gamma | fw vs Newton | fw vs MOND | dS-Unruh vs Newton |
|---|---|---|---|---|---|
| Chae now | 36 | 0.155 | 2.1s | 0.5s | 1.3s |
| Chae 2025 3D | 312 | 0.053 | 6.2s | 1.3s | 3.8s |
| DR4 conservative | 2000 | 0.021 | 15.7s | 3.4s | 9.5s |
| DR4 optimistic | 10000 | 0.009 | 35.2s | 7.5s | 21.3s |

**With the contamination systematic floor (does NOT shrink with sqrt(N)) -- the REAL limit:**
sigma_tot = sqrt(sigma_stat^2 + sigma_sys^2), sigma_sys = b*sigma_ft.

DR4 (N~5000), well-controlled contamination (sigma_ft=0.03 -> sigma_sys=0.036), sigma_tot~0.038:
- framework vs Newton: **8.5 sigma** -> CLEAN detection of a super-Newtonian boost
- framework vs MOND: **1.8 sigma** -> MARGINAL separation
- dS-Unruh vs Newton: **5.2 sigma** -> still CLEAN

DR4 (N~5000), realistic contamination (sigma_ft=0.05 -> sigma_sys=0.060), sigma_tot~0.061:
- framework vs Newton: **5.3 sigma** -> CLEAN
- framework vs MOND: **1.1 sigma** -> NOT resolved
- dS-Unruh vs Newton: **3.2 sigma** -> CLEAN

## 7. The both-ways verdict (honest, no manufactured win, no dismissal)
The framework's lower a0 is genuinely double-edged, and the forecast quantifies BOTH edges:

**It does NOT blunt the Newton discrimination.** Even at the framework's own less-favorable dS-Unruh interpolation
(gamma=1.20), DR4 separates the framework from Newton at 3-5 sigma after the contamination floor (8.5 sigma on
simple-mu, statistics-limited). Wide binaries REMAIN a clean framework-vs-Newton discriminator. The discriminating
gap to Newton (~0.20-0.32) sits comfortably above the contamination floor (~0.04-0.10) once the sample is cleaned.

**It DOES blunt the MOND discrimination, decisively.** The framework-vs-standard-MOND gap is only +0.071 (simple-mu)
-- and it is BELOW the realistic contamination systematic floor (sigma_sys~0.06). DR4 reaches at best ~1.8 sigma
(well-controlled) and ~1.1 sigma (realistic) on framework-vs-MOND. **Wide binaries do NOT cleanly separate the
framework from standard MOND at DR4.** The signal is super-Newtonian but MOND-degenerate. This is the honest answer
to the prompt's critical tension: the lower a0 makes the WB signal MOND-degenerate, NOT Newton-marginal.

**The interpolation function is a larger uncertainty than a0.** The cap spans 1.04 (standard-mu) to 1.33 (simple-mu)
at fixed framework a0 -- a spread of 0.29, far bigger than the 0.07 framework-vs-MOND gap. Until the WB community
pins the interpolation independently, the a0 footing is not separable from the interpolation choice in the WB cap.

**Net:** Wide binaries are a CLEAN framework-vs-Newton discriminator at DR4 (3-8 sigma, contamination-limited) and a
sharp test of WHETHER gravity is modified at low acceleration -- but they are NOT a clean framework-vs-MOND
discriminator (gap 0.07 < systematic floor). The framework's distinctive falsifiable WB prediction is the CAP
gamma~1.32 (simple-mu) / 1.20 (dS-Unruh own), vs 1.40 standard MOND -- a clean ~7% lower cap, but one that requires
sub-2%-level contamination control to resolve, which DR4 alone likely will not deliver. A measured cap landing firmly
at 1.40-1.50 mildly disfavors the framework a0; one at 1.20-1.33 mildly favors it; the 1.42-vs-1.32 fork is below DR4
resolution under realistic contamination. Gaia DR4 confirms the BOOST cleanly; it does not arbitrate framework-vs-MOND.

## Literature anchors
- Chae 2026 (arXiv:2601.21728): N=36 highest-quality 3D, gamma=1.600 (+0.171/-0.141), 4.9 sigma from Newton.
- Chae 2024 (ApJ 970): gamma~1.4-1.5 calibrated to a0=1.2e-10.
- Pittordis-Sutherland 2023; Manchanda-Sutherland 2025 (arXiv:2504.07569): ~20% flyby + ~50% hidden-tertiary fakes the tail.
- El-Badry 2021: 1.3M bound pairs <1 kpc (the DR4 backbone catalog).
- Banik-Zhao 2018 / Bekenstein-Milgrom 1984: the AQUAL anisotropic-G EFE tensor used for the cap.
