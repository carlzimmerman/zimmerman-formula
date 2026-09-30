# CFG214 — NOEMA3D (z ≈ 1.1–1.6, measured CO gas): a₀ from the OUTERMOST measured rotation point, flat vs rival. FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, BEFORE any digitised NOEMA3D curve value exists in this chat. The data chat digitises the curves, hashes them and holds the values until this file is committed. **κ = ½ FITTED, NOT DERIVED.**

## Why

- CFG213 (fa7d7549f) found no separation at R_e,disk for NOEMA3D. There the discs are baryon-dominated: g_bar ~ 2–12 a₀, where the flat law and the rival (a₀ × E(z) ≈ × 1.9–2.4) predict similar D.
- The curves reach about 2.7 R_e on average. That is lower acceleration and more leverage.
- NOEMA3D is the only public sample with resolved CO curves, MEASURED CO gas and SED M★.

## Exposure, disclosed

- Everything listed in CFG213's criteria.
- CFG213's per-galaxy table for NOEMA3D at R_e, printed by its run: g_bar/A0, D_obs, D_flat and D_rival for all 10.
- The data chat's notes:
  - the curves are one raster image (paper 1 PDF Fig. 5);
  - the outermost radius averages 2.74 R_e;
  - GN4_32842's inclination is 49° in paper 1 and 20° in paper 2.
- No curve value has been seen.

## Inputs

- `data_assembly/noema3d/noema3d_per_galaxy.csv`: z, R_e,disk (fixed), R_e,bulge, B/T (paper 1, the one DysmalPy used), inclination (paper 1), V_c(R_e,disk), f_DM(R_e,disk), σ₀, log M_bary (fit), SED log M★, CO log M_gas (paper 1), R_e,CO (paper 2).
- The data chat's digitised Fig. 5, with hash recorded:
  - rotation data markers (R, V, errors, side);
  - the model curve;
  - dispersion markers;
  - CO flux profile;
  - outermost data radius.
- **Validation gate.** A galaxy enters only if its digitised MODEL V at R_e,disk matches Table 3's V_c(R_e,disk) within 5%, the raster tolerance. Otherwise it is reported and excluded.
- **Deprojection.**
  - If the figure's V axis is labelled as observed or projected, V_rot = V / sin i, with paper 1's i.
  - If it is labelled intrinsic or deprojected, it is used as is.
  - The label as read by the data chat is recorded.
  - For GN4_32842, a variant uses paper 2's i.

## Quantities, per galaxy, at R_last

R_last is the outermost data marker. If both sides are shown, it is the mean radius of the two outermost markers, one per side, and V is their mean.

- **Pressure:** V_circ² = V_rot² + α σ(R)² (R/R_e,disk).
  - σ(R) is the dispersion data marker nearest R_last, or σ₀ from the table if there is none.
  - α = 3.36 is the Burkert self-gravitating exponential disc and DysmalPy's default (PRIMARY). α = 1.68 is a variant. α = 0 is reported only.
- **g_obs = V_circ²/R_last.**
- **FIT route, g_bar:**
  - V_bary²(R) = V_bary²(R_e,disk) × S(R)/S(R_e,disk), with V_bary²(R_e,disk) = (1 − f_DM) V_c(R_e,disk)² from Table 3.
  - S is the unit-mass baryonic shape: (1 − B/T) × a thin exponential disc (R_d = R_e,disk/1.678, Freeman) plus B/T × a Hernquist bulge (a = R_e,bulge/1.8153).
- **INDEPENDENT route (primary for the verdict here, because the CO gas is measured), g_bar:**
  - stars M★,SED with the same disc + bulge shape;
  - gas M_gas,CO as a thin exponential disc with R_e,CO (paper 2), or R_e,disk where R_e,CO is missing.
- **Comparison:** D_obs = g_obs/g_bar; D_pred,L = ν(g_bar/a₀,L); δ = log₁₀(D_obs/D_pred,L).
  - Laws: flat A0_f; rival A0_f E(z), with Ω_m = 0.315.
  - Kernels: ν_mono (primary) and P2.
  - Footings: canonical and alt.

## Statistic and decision rows

- **Statistic:** the median δ over the validated galaxies at R_last, with a 95% CI from 10,000 bootstrap resamples (seed 214).
- **Verdicts:** CONSISTENT / DISFAVOURED-over / DISFAVOURED-under, as in CFG213.
- **Robust** means the same verdict across both footings, both kernels and α ∈ {3.36, 1.68}.
- **H.** The outer points separate the laws iff exactly one law is robustly DISFAVOURED on the INDEPENDENT route.
  - The FIT route is reported beside it.
  - If the two routes disagree, the verdict is "route-dependent".
- **Reported, not graded:**
  - every data marker beyond R_e,disk: δ against R/R_e;
  - GN4_32842's inclination variant;
  - the model curve at R_last against the data marker (does the model follow the data there?).
- **Language:** nothing here says the data favour the framework. A flat-law failure is reported plainly.

## Controls

- **C1.** S(R_e)/S(R_e) = 1, and a thin exponential disc's V² at 50 R_d is Keplerian within 0.5%.
- **C2.** A synthetic galaxy placed exactly on each law returns δ = 0 to 1e-12.
- **C3.** The validation gate, as above.
- **MUTATE=1.** Every V_rot × 1.1. At fixed g_bar every δ must rise by 2 log₁₀ 1.1 (to 1e-9) wherever α = 0, and by more than 0.05 at α = 3.36. Outputs are written separately.

## Hand expectation, disclosed

- At R_e both laws fit. At R_last, g_bar falls by a factor of about 3–5, and the laws' D predictions spread apart.
- I do not know which way the data go. The CO gas is measured, but only the molecular phase; HI is not included in either route.
