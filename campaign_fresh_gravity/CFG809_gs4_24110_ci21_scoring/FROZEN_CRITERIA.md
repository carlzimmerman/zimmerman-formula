# CFG809 FROZEN CRITERIA (DRAFT, not yet committed): scoring GS4_24110's [CI](2-1) + dust data against the predictions frozen in CFG571

**Status: DRAFT written 2026-10-15. It becomes frozen only when it is committed alone, before any download.** After that, never edit it;
any change goes in a new dated file. The predictions are CFG571's (commit 259f7825c, `PREDICTIONS_HASH.txt` SHA-256
be27457db6bad870a734c52d2bad92c6669cde53ca7a81553e79154dbedc3714), unchanged. This file freezes only **how the new data will be read and
scored**. κ = ½ is fitted, not derived. The cold mass is still required. Nothing here says the data favour the framework.

## 0. Disclosure: this file is NOT blind to the earlier GS4_24110 results
Before writing it I had read CFG572 (public CO(4-3), [CI](1-0), dust: gas tracers disagree by ~0.7 dex) and CFG573 (the 0.13″ dust image is not
detected at 2.6σ; a post-freeze reading puts the dust at R_e ≈ 1.8–2.9 kpc, against 7.4 kpc for the stars; reported only, never a verdict). Those
numbers shaped two choices below: the gas size is measured from the new data (section 3.2), and tracer disagreement gets a frozen rule (section 4).
What has **not** been read: any of programme 2025.1.01377.L. The 0.7 dex disagreement and the compact-dust hint are the reason the routes are
kept separate and never averaged.

## 1. Target and data
- **Target:** GS4_24110 = KMOS3DGS4-24110 = ASPECS 1mm.C10 = RC100 GS3 15675, z = 1.9975 (CO(6-5)). RC100 corrected copy: V_c(R_e) 206 km/s, R_e 7.39 kpc,
  σ0 82 km/s, log M_bar 10.76 (`real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv`). KMOS3D log M★ 10.89. RA 53.166889, Dec −27.798733.
- **Data:** ALMA programme 2025.1.01377.L, [CI](2-1) (rest 809.342 GHz, observed ≈ 270.0 GHz) and continuum, 0.09″, 3.9 h. Public date **2026-11-28** per
  CFG570's archive metadata (commit 185251551); **not re-verified with the archive**.
- **Access:** downloaded only on the owner's explicit yes, after the file size is stated. Take the archive's imaged cube and continuum image. If none is
  provided, image the visibilities (CASA `tclean`, Briggs robust 0.5, channel width ≤ 20 km/s) and list that as a **departure** (section 8). The cube is deleted
  after the run; only derived products and their SHA-256 are kept.
- **Cosmology:** flat ΛCDM, H0 70, Ωm 0.3, as in CFG571/572 (angular size and D_L).

## 2. What was predicted (CFG571; read from `cfg571_prereg_results.json`, never recomputed)
Required total gas mass, log10 M_gas [M☉], gas disc R_g = R_d | 1.5 R_d. FLOOR means the stars alone already exceed the baryons the model allows.

| M★ | footing | F-DESI | F-flat | R-H | L-fb (RAR-equivalent) |
|---|---|---|---|---|---|
| 10.89 | canon 9.36e-11 | 9.82 \| 10.09 | 9.46 \| 9.73 | FLOOR | FLOOR |
| 10.89 | alt 1.13e-10 | 9.11 \| 9.38 | FLOOR | FLOOR | FLOOR |
| 10.76 | canon | 10.43 \| 10.69 | 10.36 \| 10.63 | FLOOR | FLOOR |
| 10.76 | alt | 10.33 \| 10.60 | 10.24 \| 10.51 | FLOOR | FLOOR |

## 3. Measurements, in order (each gate is checked before the next step is read)
**G1, [CI](2-1) detection.** Integrated flux S Δv in a ≥ 2σ moment-0 mask, velocity window ±300 km/s about z = 1.9975 (CFG572's window), continuum from the
median of the line-free channels (|v| > 600 km/s). Noise: the standard deviation of S Δv in 8 equal apertures on a ring 5–8″ away (or the cube's noise map if
the primary beam is smaller). **Detected if S/N ≥ 5.** Otherwise a 3σ upper limit on M_gas and stop at 3.3.

**3.1 Continuum.** Peak S/N and total flux in the same mask. If S/N ≥ 5, fit a 2D elliptical Gaussian convolved with the beam; report FWHM and its error.

**3.2 Gas size (primary comparison radius).**
- Fit the same 2D Gaussian to the [CI](2-1) moment-0. The circularized half-light radius R_e,CI = FWHM/2 (circularized) and the exponential scale length
  R_g = R_e,CI/1.678.
- **Gate G3:** the size is used only if the fitted FWHM exceeds twice its 1σ error and the source is detected at ≥ 5σ. Otherwise the gas shapes are
  CFG571's: R_g = R_d (primary) and 1.5 R_d, and the size is reported as an upper limit.
- **Never pooled:** the measured-size result and the CFG571 shapes are reported side by side.

**3.3 Gas mass, routes reported separately and never averaged.**
- **CI21 (primary, new):** L′_CI(2-1) = 3.25×10⁷ S Δv ν_obs⁻² D_L² (1+z)⁻³ [K km s⁻¹ pc², S Δv in Jy km/s, ν_obs in GHz, D_L in Mpc]. Then
  **M_CI = 4.566×10⁻⁴ Q(T_ex) (1/5) e^{+62.5/T_ex} L′_CI(2-1)** [M☉], with Q = 1 + 3e^(−23.6/T_ex) + 5e^(−62.5/T_ex) and **T_ex = 25 K**. Then
  M_mol = 1.36 M_CI / (6 X_CI), **X_CI = 1.9×10⁻⁵ primary**, 3.0×10⁻⁵ branch. (A T_ex = 40 K value is printed as information only.)
  - **Formula status, stated plainly:** the coefficient 4.566×10⁻⁴ and the form are those cited in later papers for Weiß et al. (2003); the original paper has **not
    been read**. They are checked by control C4 below, not trusted.
- **CO43 and CI10 (public, as CFG572):** the CFG572 results are re-quoted unchanged (CO(4-3) 0.621 ± 0.036 Jy km/s → log M_gas 10.95; [CI](1-0) < 10.28/10.08
  at 3σ). No new fit.
- **D (dust, literature):** L_ν(850 μm) from Boogaard+2020, as CFG572 (10.51 at α_CO 4.36; 10.68 Scoville). **The new continuum (rest ≈ 370 μm at 270 GHz) is used
  only for size and a flux sanity check, not for a new dust mass**, because converting it to rest 850 μm needs a dust temperature and β that are not frozen.

**3.4 Kinematics (secondary).** The CFG571 comparison uses V_c = 206 km/s at R_e (the RC100 Hα value), unchanged. If the [CI] cube resolves rotation (gate G4: moment-1
shows a monotonic gradient across ≥ 2 beams with S/N ≥ 5), also fit V_c at R_e from [CI] as a **branch**, with the same arctan model and pressure branch as CFG808
(P-B primary, P0 branch). Never pooled with the 206 km/s value.

## 4. Scoring (a single disc; a demonstration; no model is excluded)
- **Δ_v** (CFG572's definition): Δ_v = log(V_bar,meas² / V_bar,req²) at R_e = 7.39 kpc, with V_bar,meas² = V★² (Freeman, M★ 10.89 primary | 10.76) + V_gas² (an
  exponential disc of the measured M_gas and the shape of 3.2). Computed with the CFG571 functions, imported read-only. Per route, footing, stellar branch and gas-shape
  branch; never pooled.
- **Error:** σ_Δv propagates the flux error ⊕ a 0.2 dex gas-route systematic (X_CI, α_CO, dust α) and a 0.2 dex stellar-mass systematic through the same functions.
- **Wording (frozen):** "consistent with" if |Δ_v| ≤ 2σ_Δv; "in tension with" if |Δ_v| > 2σ_Δv. A model that is FLOOR is **in tension** whenever gas is detected on that route
  (stars alone already exceed what it allows), reduced and reported as such if M★ is taken 0.2 dex lower.
- **Robustness flag (frozen).** A model's verdict on the primary route (CI21) is **ROBUST** only if the same wording holds on every other route that has a detection
  (CO43, D). If the wordings differ, the verdict is **NOT ROBUST** and no model is described as supported or disfavoured by this disc. (CFG572 already shows that CO43 and
  [CI](1-0)/dust sit ~0.7 dex apart; this rule decides in advance what happens if CI21 lands between them.)
- **Not allowed:** pooling routes, footings, stellar branches or this disc with U4_27928 (CFG808); choosing the primary route after seeing Δ_v; any exclusion statement.

## 5. Controls (a failed control is kept and reported, and makes the run NOT DIAGNOSTIC)
- **C1 injection:** a synthetic Gaussian source of known flux and size, injected 10″ from the target in the real cube's noise, is recovered with flux within 20% and size within 25%.
- **C2 negative:** 5 off-source apertures in the line window are consistent with zero (|S Δv| < 3σ).
- **C3 headers:** the cube's frequency axis covers 270.0 GHz; the beam and channel width keywords exist; the detected line redshift is 1.9975 ± 0.002.
- **C4 formula check (new):** with the Einstein coefficients A10 = 7.93×10⁻⁸ s⁻¹ and A21 = 2.68×10⁻⁷ s⁻¹, rest frequencies 492.161 and 809.342 GHz, the (2-1) coefficient
  must equal 5.706×10⁻⁴ × (ν21²/A21)/(ν10²/A10) to within 1% (this gives 4.566×10⁻⁴), and the two mass formulas must return the same M_CI to < 1e-6 when given the LTE
  luminosity ratio at T_ex = 25 K.
- **C5:** CFG571's own controls C3 (Freeman peak 0.387) and C4 (Newtonian round trip) re-run.
- **MUTATE:** shift the velocity window by +2000 km/s. If the line is detected at the true redshift, the shifted flux must drop below 3σ (detected, exit 1). If the line is not
  detected, MUTATE is non-diagnostic and is reported as such. The output carries the `_MUTATE` tag.

## 6. Scripts and outputs
`cfg809_gs4.py` (with `--mutate`), `cfg809_gs4.out`, `cfg809_gs4_results.json`. It imports `cfg571_prereg.py` read-only and changes no model.

## 7. Pre-data forecast (committed with the criteria)
The table in section 2 is the forecast. The run prints, for the measured gas mass, which models are consistent and which are FLOOR, branch by branch.

## 8. Departure rule
Anything added or changed after the first measured number is printed (an imaging choice, a mask, a branch) is listed under "Departures" in the README with its reason, as CFG572 did. The
comparison rules of sections 4 and 5 may not be changed.

## 9. Not claimed
No a0 measurement. One disc, a demonstration. κ = ½ is fitted; the cold mass is still required; "theory closed" is never said. These are scoring rules for predictions made before the data.
