# CFG553: sealed Milky Way predictions for Gaia DR4 (release 2026-12-02)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (43fb64612).
- **Scripts:** `cfg553_predict.py` writes `cfg553_predictions.json` (the sealed object), `cfg553_predict.out`;
  `CFG553_MUTATE=1` writes `_MUTATE` outputs and exits 1 (DETECTED). `cfg553_write_md.py` writes `PREDICTIONS.md`
  (all tables, every number from the JSON). Runs in a few seconds, nice 10, 2 threads. Re-running reproduces the JSON
  byte for byte (no timestamps inside).
- **Seal:** `PREDICTIONS_HASH.txt` = SHA-256 of `cfg553_predictions.json`, committed before DR4 exists. Never edit
  these files after the seal; any change goes in a new, dated file.
- **Separate from the wide-binary prereg.** `prep_2026/gaia_dr4_prep/` (PREREGISTRATION_DR4.md, amendments, every
  `*_HASH.txt`) was read for scope only and not touched. CFG553 adds five Milky Way observables; no wide-binary claim.
- **Re-used, not edited:** CFG514's solver and McMillan17 baryons, CFG516's round-rule machinery, CFG532's mixes,
  `v_model`, `slope`, `fit_nfw` and data loaders, executed read-only.
- κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10, never pooled. ν_mono. No EFE. McMillan17 census held (A = 1); band =
  census stellar mass ± 1σ (5.43 ± 0.57e10). The cold energy's mass is still required. Not theory closed. These are
  predictions, not results, and nothing here says the data favour the framework.

## Headline sealed numbers (census central (census band); from the JSON)

| | RM-v can / alt | RM-φ can / alt | PD (QUMOND disc) can / alt | NFW fit to Ou+24 |
|---|---|---|---|---|
| P1 K_z(R0, 1.1)/2πG [M☉ pc⁻²] | 74.1 (68.3–79.9) / 75.6 | 70.3 (64.8–75.8) / 71.6 | 90.1 (84.6–95.5) / 94.8 | 76.3 (72.7–79.8) |
| P1 K_z(16 kpc, 1.1)/2πG | 18.6 / 19.2 | 17.7 / 18.2 | 26.7 / 28.5 | 19.4 |
| P1 ν_z² ratio PD/RM at R0 / 16 kpc | 1.38 / 1.90 (can), 1.44 / 2.01 (alt) | 1.40 / 1.93, 1.46 / 2.04 | — | — |
| P2 V(20 kpc) [km/s] | 199.5 (193.9–204.8) / 206.6 | 192.4 / 199.3 | 195.4 / 202.7 | 207.3 |
| P2 dlnV/dlnR 15–22 kpc | −0.162 / −0.149 | −0.120 / −0.108 | −0.115 / −0.105 | −0.171 |
| P2 dlnV/dlnR 15–27.5 kpc | −0.148 / −0.136 | −0.110 / −0.099 | −0.108 / −0.098 | −0.174 |
| P3 local dark density [GeV cm⁻³] | 0.323 (0.310–0.335) / 0.360 | 0.254 / 0.287 | 2.01 / 2.34 (midplane phantom) | 0.338 |
| P3 Σ(\|z\| < 1.1) true column [M☉ pc⁻²] | 73.6 / 75.8 | 69.7 / 71.6 | 91.1 / 96.6 | 74.5 |
| P3 ρ_tot(R0, 0) Oort limit [M☉ pc⁻³] | 0.116 / 0.117 | 0.114 / 0.115 | 0.160 / 0.169 | 0.116 |
| P4 σ_z(R0), thin tracer h 0.30 kpc [km/s] | 16.8 / 16.9 | 16.6 / 16.7 | 19.3 / 19.8 | 17.0 |
| P5 V_c(60 kpc) [km/s] | 178.1 (173.9–182.1) / 186.0 | 176.9 / 184.7 | 178.1 / 186.0 | 166.5 (163.6–170.5) |
| P5 mean V_c 30–60 kpc | 182.6 / 190.3 | 180.1 / 187.8 | 182.1 / 189.9 | 178.3 |

## What separates what, and the DR4 precision needed (3σ, framework-central truth vs the rival's census band)

- **Round vs disc (vs PD): the vertical observables.**
  - K_z(R0, 1.1): Δ −16 to −23 M☉ pc⁻²; σ_req 3.5–5.8 M☉ pc⁻² on one value.
  - The 36-cell K_z(R, z) grid separates even at 40–80% per-point error (independent errors assumed; floor 5%), because
    PD/RM rises from 1.11–1.18 at 5 kpc to 1.50–1.62 at 16 kpc.
  - Local dark density: PD 2.0–2.3 vs RM 0.25–0.36 GeV cm⁻³ (σ_req ≈ 0.55–0.68). Σ_1.1: σ_req 4–7 M☉ pc⁻². Oort limit:
    σ_req 0.012–0.016 M☉ pc⁻³. σ_z(R0) thin tracer: Δ 2.4–3.1 km/s, σ_req 0.6–0.9 km/s.
  - In-plane observables separate PD from RM-v only (RM-v's g is ~9% higher): V_c(R) at 0.9–1.4% per point, the
    15–27.5 slope at σ ≈ 0.010. **RM-φ and PD have the same in-plane speed by construction, so P2 and P5 cannot
    separate them.**
- **Framework vs NFW (fitted to Ou+24): the halo tracers, not the disc.**
  - P1/P3/P4: NOT SEPARABLE for RM-v (K_z(R0, 1.1) Δ −0.7 to −2.2; the vector is FLOOR-LIMITED). RM-φ vs NFW: P1 vector
    needs 6–12% per point. This repeats CFG513: inside ~50 kpc an NFW mimics the round rule.
  - **P5 is the discriminator:** V_c(60 kpc) framework 177–186 vs NFW 166.5; σ_req 2.0–2.5 km/s (canonical), 4.6–5.2
    km/s (alt). Mean 30–60 kpc: σ_req 1.6–3.1 km/s on the alt footing; on the canonical footing NOT SEPARABLE
    (RM-φ) or 0.5 km/s (RM-v).
  - Slopes vs NFW need σ ≤ 0.009 for RM-v (not realistic) and 0.014–0.022 for RM-φ.
- **The live tension is not a rival split.** DR3 curves give 15–27.5 kpc slopes near −0.3 (CFG532b); every model
  here sits at −0.10 to −0.18. If DR4 holds that slope with σ ≤ 0.04, P2's slope verdict is BOTH EXCLUDED (a framework
  fail; the fitted NFW fails too).

## Controls (from the JSON)

- **K1 PASS:** CFG516's K_z χ² (B1 F0; PD, RM-φ, RM-v; both footings) reproduced exactly (144.95 / 46.70 / 43.82 can;
  210.18 / 44.29 / 45.80 alt).
- **K2 PASS:** CFG532's census V(20 kpc) reproduced exactly: RM-v 199.52 / 206.61, RM-φ 192.40 / 199.32 km/s; its DR4
  6-point slope too.
- **K3, K4, K5 PASS** (mix linearity; fitted-NFW χ² 9.872 on Ou+24; Jeans integrator; unit 37.966 GeV cm⁻³ per M☉ pc⁻³).
- **K6 FAILS as frozen:** in-plane vs spherical-equivalent V_c at 30–60 kpc differ by up to 1.1% (RM, NFW: the extended
  gas disc's quadrupole) and 2.75% (PD: flattened phantom), not < 1%. The frozen expectation was mis-specified. The
  spherical-equivalent P5 (√(GM(<r)/r), Gauss flux) was added to the JSON after the first run, before the seal; the
  DR4 comparison uses the column matching the analysis's definition (dated disclosure, 2026-10-10).
- **K7 (added; scorer self-test, no data) PASS:** the frozen scalar and vector scorers return SUPPORTED / EXCLUDED on
  synthetic framework / PD truths.
- **MUTATE (round ↔ disc swap) DETECTED:** ν_z² ratio at 16 kpc 1.90–2.04 in every footing × form (inside ×1.6–3.6);
  the swapped K_z(R, 1.1) is outside the RM census band at every R ≥ 8 kpc.

## Disclosures and limits

- Numbers from CFG513/516/532/574 were known before freezing (listed in the criteria §0).
- Vector precisions assume independent per-point errors on the declared grid; correlated DR4 systematics will raise them.
- P4 is tracer-model conditional (isothermal, exponential h, tilt term neglected); a DR4 tracer with h off by > 15% is
  scored by re-running the frozen script with the measured h.
- The NFW is fitted to Ou+24 and the band absorbs baryon changes, so its V_c(5–27 kpc) band is narrow by construction.
- Static, axisymmetric, equilibrium models; non-equilibrium effects enter only through DR4 analyses' systematic budgets.
- The census edge (287 / 261 kpc) is outside every predicted radius.
- Context only (CFG516, on disk): Bovy & Rix 2013 K_z(R0, 1.1) = 66.4 ± 2.2 sits below RM-v's census band (68.3–79.9) and
  far below PD's.
