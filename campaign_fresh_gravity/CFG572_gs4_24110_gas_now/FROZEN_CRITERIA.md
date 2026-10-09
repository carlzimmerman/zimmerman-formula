# CFG572 FROZEN CRITERIA: GS4_24110's gas mass from PUBLIC data, tested against CFG571's frozen prediction

Committed alone, before any cube is downloaded or measured. Owner request (10-09): "yeah get them all and put them in a chart for me" (an explicit yes for the literature look-up and the public cube downloads).

## Why this lane exists
CFG571 (259f7825c) froze per-model predictions of GS4_24110's total gas mass (z 1.997). GS4_24110 is ASPECS **1mm.C10**, and older public ALMA data on it exist (found 10-09).

**Disclosure.** Before writing this file I read Boogaard+2020 (arXiv 2009.04348, TeX source saved in `data_assembly/gs4_24110_lit/`). For 1mm.C10 it gives:
- log M★ = 11.1 ± 0.1 (ASPECS SED);
- S(1.2 mm) = 342 ± 34 μJy and L_ν(850 μm, rest) = 32.1 ± 3.2 × 10²⁹ erg s⁻¹ Hz⁻¹;
- CO(6-5) at 1.09 ± 0.22 Jy km/s, FWHM 248 ± 44 km/s, z 1.9975;
- no Band 3 CO coverage.

I mentally converted L850 to a gas mass (~10^10.5–10.7) before freezing. The dust-route rule below is the standard one, fixed as written, not tuned.

## Gas-mass routes (each reported separately, never pooled)
- **D (dust, literature):** M_mol = L_ν(850)/α850, with α850 = 6.7×10¹⁹ erg s⁻¹ Hz⁻¹ M☉⁻¹ (Scoville+2016, which assumes α_CO = 6.5 incl. He). Primary rescales to α_CO 4.36 (×4.36/6.5); the unscaled value is also reported. Scatter 0.2 dex (Boogaard+2020 footnote).
- **CI (measured here):** the [CI](1-0) line (rest 492.161 GHz → 164.19 GHz) in public MOUS uid://A001/X1465/X99e (2019.1.01528.S).
  - Formula: L'_CI = 3.25×10⁷ S Δv ν_obs⁻² D_L² (1+z)⁻³. M_CI = 5.706×10⁻⁴ Q(T_ex) (1/3) e^(23.6/T_ex) L'_CI, with Q = 1 + 3e^(−23.6/T_ex) + 5e^(−62.5/T_ex) and T_ex = 25 K. Then M_mol = 1.36 × M_CI / (6 X_CI).
  - X_CI primary = 1.9×10⁻⁵ (Boogaard+2020's ASPECS average); branch 3.0×10⁻⁵.
- **CO43 (measured here):** CO(4-3) (rest 461.041 → 153.81 GHz) in public MOUS uid://A001/X1465/X99a. M_mol = α_CO L'_CO(4-3)/r41, with α_CO = 4.36. r41 primary 0.37; branches 0.25 and 0.55 (Boogaard+2020's r42 0.36–0.41 times r21 ~0.75–1, and higher excitation at z ≥ 2).
- Cosmology for D_L: flat ΛCDM, H0 70, Ωm 0.3.

## Measurement (CI and CO43)
- **Products:** the pipeline `*.pbcor.fits` image cube of the spectral window containing the line, from the MOUS product tar only (no ASDM).
- **Position:** RA 53.166889, Dec −27.798733 (KMOS3D).
- **Aperture:** circular, radius 1.5″ (the beams are ~1.6–1.8″, so the source is unresolved). Flux = Σ pixels / (beam area in pixels).
- **Velocity window:** ±300 km/s about z = 1.9975 (≈ ±1.2 × the CO(6-5) FWHM). Integrated flux S Δv = Σ_channels flux × Δv. Continuum: the median of the line-free channels (|v| > 600 km/s) in the same aperture, subtracted per channel.
- **Noise:** the standard deviation of S Δv in 8 equal apertures on a ring 5–8″ from the source (inside the primary beam). Detection if S Δv ≥ 3σ; otherwise a 3σ upper limit.

## Comparison with CFG571 (frozen numbers, read from `cfg571_prereg_results.json`; never recomputed)
- For each route and branch, M_gas,meas is compared with each model's required total M_gas (R_g = R_d primary). For a model whose prediction is FLOOR, any M_gas,meas ≥ 3σ above zero counts against it.
- In velocity space: Δ_v = log(V_bar,meas² / V_bar,req²) at R_e = 7.39 kpc, with V_bar,meas² = V★² (Freeman, CFG571's stellar branches) + V_gas² (an exponential with R_g = R_d holding M_gas,meas).
- **Post-freeze stellar branch (reported only, not a verdict):** Boogaard's log M★ = 11.1, with CFG571's own functions.
- **Single disc = demonstration.** No model is excluded on one disc (CFG571 criteria). The verdict wording is "consistent with" or "in tension with (Δ_v beyond ±2 × the propagated error)".

## Controls
- **C1 injection:** a synthetic point source of known S Δv, injected 10″ from the target, is recovered within 20% by the same aperture code.
- **C2 negative:** apertures at 5 off-source positions in the line window are consistent with zero (|S Δv| < 3σ).
- **C3 header:** the cube's frequency axis covers the line and the beam keywords exist.
- **MUTATE:** the velocity window is shifted by +2000 km/s. If the line is detected at the true redshift, the shifted flux must drop below 3σ (detected, exit 1). If the line is not detected, MUTATE is non-diagnostic and is reported as such.
- Failed controls are kept and reported. Cubes are deleted after the run unless the owner says keep (only extracted spectra and numbers are committed).

## Chart
One figure for the owner: each model's predicted gas mass (CFG571, frozen) beside the measured gas mass from each route, with errors.

## Not claimed
One galaxy; no a0(z) measurement. κ = ½ fitted; the cold mass is still required.
