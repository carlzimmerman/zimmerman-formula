# AG5 FROZEN SCORING (2026-10-20): how the November ALMA releases will be measured and scored, fixed before release

Committed alone, before any scorer code and before either dataset is public. Owner's go (2026-10-20, in chat: "swing bro we need
to do it", on the proposal to write and freeze the scoring so the verdict is mechanical on release day). This file adds no
prediction. It fixes how data meet the predictions that are already sealed.

## Sealed predictions scored (sha256 verified by the scorer before anything else)
| seal | kernel | branches | file |
|---|---|---|---|
| CFG571 (canonical November seal) | ν_mono | F-DESI, F-flat, R-H, L-fb | `campaign_fresh_gravity/CFG571_prereg_proprietary_alma/cfg571_prereg_results.json` (hash in `PREDICTIONS_HASH.txt`) |
| CFG775 | ν_mono | BH-k3 | `campaign_fresh_gravity/CFG775_bh_horizon_dark_energy/SEALED_BH_BRANCH.json` (sha 3d236378…) |
| CFG778 | ν_mono | E, E-CCBH | `campaign_fresh_gravity/CFG778_sealed_event_horizon_branch/SEALED_EVENT_HORIZON.json` (sha b9f3e827…) |
| AG4e | n=1 (the action's law) | all seven | `argon_push/AG4e_n1_alma_seal/SEALED_N1.json` (sha 9802de0d…) |
| AG4d | n=2 (a₀-line) | all seven | `argon_push/AG4d_n2_alma_seal/SEALED_N2.json` (sha d64727b5…) |

The required baryons are recomputed with CFG571's own code (its head, executed read-only) at the measured inputs. At the sealed
grid points the recomputation must reproduce every sealed number exactly (control S2).

## Data (downloaded at release, only with the owner's OK and after stating file names and sizes)
- **U4_27928:** ALMA 2024.1.00100.L, CO(2–1) at 0.07″; public 2026-11-06.
- **GS4_24110:** ALMA 2025.1.01377.L, [CI](2–1) and dust continuum at 0.09″; public 2026-11-28.
- Pipeline product cubes from the ALMA archive. The measurement script (`measure_<target>.py`) is written and committed after
  download and header inspection, **before any line or continuum pixel is read.** It implements exactly the procedure below.

## Measurement procedure (frozen)
**Common to both targets**
- **Flux, by curve of growth:**
  - Circular apertures of radius 0.5, 1.0, 1.5 and 2.0″ about the catalogue position.
  - The adopted flux is at the first radius beyond which the next aperture adds less than 1σ; otherwise the 2.0″ value.
  - Flux = Σ pixels / beam area in pixels.
- **Velocity window:** ±400 km/s (U4) and ±300 km/s (GS4, as CFG572) about the catalogue redshift. Continuum comes from the
  median of the line-free channels (|v| > 600 km/s) in the same aperture.
- **Noise:** the standard deviation of the same measurement in 8 equal apertures on a ring 5–8″ from the source. A detection
  needs ≥ 3σ; otherwise a 3σ upper limit is used.
- **Controls:** an injected point source 10″ away must be recovered within 20%; 5 off-source apertures must be consistent with
  zero; the header must cover the line and carry beam keywords (CFG572's C1–C3).
- **Line luminosity:** L′ = 3.25×10⁷ S Δv ν_obs⁻² D_L² (1+z)⁻³ (CFG572), with flat ΛCDM H₀ = 70, Ω_m = 0.3, used for distances
  only (as CFG571).

**U4_27928, gas**
- M_gas = α_CO L′_CO(1–0), with L′(1–0) = L′(2–1)/r₂₁ (CFG571).
- Primary: α_CO = 4.36 (including He), r₂₁ = 0.77. Branch: α_CO = 1.0.

**U4_27928, V_c at 2R_e (8.27 kpc = 0.98″; CFG571's conditional radius)**
- Kinematic PA: the direction of the steepest velocity gradient in the moment-1 map within 1″.
- Position–velocity cut along that PA, slit width two beams.
- At ±0.98″, take the intensity-weighted velocity of each PV column. V_los = ½(V_red − V_blue).
- Inclination from the CO moment-0 axis ratio, using cos²i = ((b/a)² − 0.2²)/(1 − 0.2²). V = V_los/sin i.
- Pressure branches as CFG571, never pooled:
  - P-B (primary): V_c² = V² + 2σ₀²(R/R_d), with σ₀ the median moment-2 dispersion beyond 1R_e and R_d = R_e/1.678;
  - P0: no correction.
- Error: half the red–blue difference ⊕ half a channel ⊕ the inclination term for Δ(b/a) = ±0.1.
- If the PV cut has no ≥ 3σ emission at ±0.98″ on either side, V_c(2R_e) is UNAVAILABLE and U4 is NOT SCORABLE. No other radius
  is substituted.

**GS4_24110, gas**
- **Primary route [CI](2–1):** Boogaard+2020 Eq. MCI21, verified from the on-disk TeX source:
  M_CI = 4.556×10⁻⁴ Q(T_ex) e^(62.5/T_ex)/5 · L′_CI(2–1), with Q = 1 + 3e^(−23.6/T_ex) + 5e^(−62.5/T_ex).
  M_gas = 1.36 M_CI/(6 X_CI) (CFG572).
  - Primary: T_ex = 25 K, X_CI = 1.9×10⁻⁵.
  - Branches: X_CI = 3.0×10⁻⁵, and T_ex = 20 K and 30 K.
- **Dust route:** the continuum flux is measured with the same curve of growth. It is converted to gas only with a formula
  verified from its primary source (Scoville+2016) before the data are opened. Otherwise it is reported as flux only.
- **Reported only:** CFG572's public CO(4–3) and literature-dust routes.
- **Kinematics:** V_c(R_e) from the [CI] cube by the U4 PV method at ±R_e (0.88″). Reported only: the seals use RC100's
  206 km/s, and the primary score keeps 206.

## Score (per law form × branch × footing × M* branch × gas-shape branch; never pooled)
- **Δ** = log(V²_bar,meas R/G) − logVbar2R_G_req. V²_bar,meas = V²_*(R; M*, R_d) + V²_gas(R; M_gas, R_g), with CFG571's
  Freeman functions. R = 2R_e (U4) or R_e (GS4).
- **σ_tot** = √(σ_meas² + 0.15²). σ_meas comes from the flux error; for U4 it also includes V_c's error, propagated by
  rescoring at V_c ± σ_V. The 0.15 dex systematic floor is CFG571's.
- **Readings:** CONSISTENT (|Δ| ≤ 2σ_tot), TENSION (2–3σ_tot), ≥ 3σ OFF (one disc: not an exclusion, per CFG571).
  - A FLOOR model with gas detected at ≥ 3σ counts against that model (CFG572).
  - An upper limit gives a one-sided Δ.
- **THEORY KILL (THEORY_CANONICAL v1 §2, "gas only consistent with a₀ ∝ H(z) or with the horizon branch"):**
  - It is evaluated on the ν_mono seal, the canonical footing and the primary route.
  - It fires if no framework branch (F-flat, F-DESI, BH-k3) is CONSISTENT while R-H, E or E-CCBH is CONSISTENT. For GS4 this
    must hold for both M* branches; U4 has one M* (10.74).
  - **TRACER-LIMITED:** if the primary route and any other measured route differ in log M_gas by more than
    2√(σ₁² + σ₂²), the kill can fire only if it fires on every measured route.
- **Law-form reading (AG4d/AG4e, reported):** which of ν_mono, n=1 and n=2 has at least one CONSISTENT framework branch, per
  M* branch and footing.

## Scorer controls (run before any real data)
- **S1:** every seal's sha256 matches its recorded hash.
- **S2:** CFG571's code, recomputed at the sealed grid points, reproduces every sealed logVbar2R_G exactly, for all three
  kernels.
- **S3:** a synthetic measurement equal to F-DESI's requirement (ν_mono, canonical) reads F-DESI CONSISTENT, and the kill does
  not fire.
- **S4 (MUTATE, `AG5_MUTATE=1`):** a synthetic measurement equal to R-H's requirement, at a V_c where the framework branches
  differ from R-H by more than 3σ_tot, must fire the kill. The scorer then exits 1 (the control bites).

## Settings
κ = ½ fitted; footings never pooled; cold-energy mass required; not theory closed. One disc per date is a demonstration
(CFG571). Only the canonical kill line can falsify, and it is applied exactly as written here.
