# CFG970 FROZEN CRITERIA: the SN Refsdal host's CO(3-2) line, gas mass, edge clipping and baryonic-Tully–Fisher consistency (ALMA 2013.1.00582.S, A1.4 cube)

Committed alone, with its LEDGER row, before any script exists and **before any pixel value of the cube has been read** (headers only). κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 m/s² never pooled; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework. Owner (2026-10-27): "Yes, write frozen criteria for measuring the Refsdal host's CO(3-2) rotation curve and gas mass from the A1.4 cube (including the edge-clipping and BTFR-consistency checks) before reading any values." The owner chose ID CFG970; it is unused in the LEDGER, directories and committed .md files.

## Why
The top-ranked lensed disc of the a₀(z) target search (`data_assembly/a0z_lensed_targets_2026-10-27/`) is the SN Refsdal host (Sp1149, MACS1149-1501). Di Teodoro+2018 (arXiv:1801.06546, MUSE [OII], their M3 image) report a curve that peaks near 1 kpc, then declines and flattens to **V_flat = 128 (+29 / −19) km/s**. That fit is at i = 35°, with errors from 25° / 45° models, because the galaxy is nearly face-on. They give σ_gas = 27 ± 5 km/s and **M★ ≈ 5 × 10⁹ (10^9.5–9.7) M☉**.

Under the law, V_flat⁴ = G M_b a₀, so the law **needs M_b ≈ 2.2 × 10¹⁰ M☉** at canonical a₀ (1.1–4.9 × 10¹⁰ across 109–157 km/s), i.e. **≈ 1.7 × 10¹⁰ M☉ of gas**. The CO cube measures that gas.

## Data (outside the repo; `new_physics/_external_data/alma_2013.1.00582.S_A1.4/`; sha256 from `data_assembly/FETCH_MANIFEST_2026-10-01.jsonl`)
- CO(3-2) `.pbcor.fits`: 614,698,560 B, sha256 64fb0ec2…dc38. 784² × 250 channels, 0.080″ pixels, beam 0.44″ × 0.35″, 2.00 km/s channels, 138.703–138.934 GHz.
- CO `.flux.fits.gz` (primary-beam response): sha256 04dce427…bd72.
- Continuum `.pbcor.fits` / `.flux.fits.gz` (151 GHz): sha256 6b2b7847…c1f9 and fbefd9e9…75e2.

## Fixed inputs
- **z = 1.4906.** CO(3-2) is at 138.8404 GHz; the cube's RESTFRQ of 138.8181 GHz is its own reference and velocities are taken relative to z = 1.4906.
- **Distances:** native BAO-raw D_M (CFG686's PCHIP of DESI DR2 D_M/r_d, h r_d = 101.54 Mpc, h = 0.70), with D_L = (1+z) D_M. The h70 / Ω_m 0.3 ΛCDM value is reported only.
- **Published values (Di Teodoro+2018 text):**
  - V_flat 128 (109 / 157) km/s at i = 35° (25° / 45°).
  - M★ ∈ {10^9.5, 10^9.7}.
  - μ ≈ 4 for their M3 image.
  - KLASS: μ 5.42 (Girard+20) / 12.42 (Mason+17) at the KLASS position; i = 12° and V_max 227 km/s (Mason+17), **reported only**.
- **The magnification of the image(s) inside this cube is not known without a lens model.** It is therefore never assumed: see S6.

## Steps (memory-mapped, chunked plane by plane, RSS < 1 GB, single thread)
**S1 Source finding (image plane).**
- Smooth spatially with a Gaussian to 2× the beam FWHM, and spectrally with a 3-channel boxcar.
- Per-plane noise is the robust MAD of the smoothed planes in the outer 40 channels on each side, inside primary-beam response ≥ 0.3.
- Mask: 3-D connected regions seeded at ≥ 4σ, grown to ≥ 2σ, keeping regions ≥ 1 beam in area, ≥ 3 channels long and at PB ≥ 0.3.
- **Primary image:** the region whose flux-weighted centroid lies ≤ 3″ from the KLASS position (177.397034, 22.396011). Every other region is listed with its position and flux. If no region lies within 3″, the result is NOT FOUND, reported with an upper limit.

**G0 detection gate** (on the primary image's integrated S/N in S2):
- **DETECTED** if ≥ 5.
- **MARGINAL** if 3–5 (values reported, flagged).
- **UPPER LIMIT** if < 3: 3σ in a 2″-radius aperture over ±200 km/s.

**S2 Integrated flux.** S Δv (Jy km/s) is the sum of the unsmoothed pbcor cube inside the mask × (pixel area / beam area) × Δv. The error comes from the per-channel noise scaled by the mask's beams and channels. A 2″-radius aperture variant is reported.

**S3 Edge clipping (frozen):**
- Sum the integrated spectrum (mask footprint, unsmoothed) over the 10 outermost channels (20 km/s) at each band edge.
- **CLEAN** if both edge sums are within ±2σ of zero **and** both W20 crossings lie ≥ 20 km/s inside the band.
- Otherwise **CLIPPED-LOW / CLIPPED-HIGH / CLIPPED-BOTH**. Under any CLIPPED class, W20 and every CO velocity are **lower bounds**.

**S4 Line width and CO velocity.**
- W50 and W20 come from the integrated spectrum (2-channel boxcar), with linear-interpolated crossings and 200 noise realisations (`default_rng(970)`) for the errors.
- **V_CO = W50 / (2 sin i)** at i ∈ {25°, 35°, 45°} (W20 is a variant).
- **Spectral asymmetry:** the ratio of flux on the blue and red sides of the W50 midpoint is reported. **≥ 1.5 is flagged as LOPSIDED**, because differential magnification can weight one side (the two-sided rule of CFG405 / arXiv:2507.10544).

**S5 Gas mass (apparent, not de-lensed).**
- L′_CO(3-2) = 3.25 × 10⁷ S Δv ν_obs⁻² D_L² (1+z)⁻³ [K km/s pc²].
- L′_CO(1-0) = L′(3-2)/R₃₁, with R₃₁ ∈ {0.5, 0.8}.
- **M_gas,app = α_CO L′_CO(1-0)**, with α_CO ∈ {0.8, 4.3} M☉ (K km/s pc²)⁻¹, including helium.

**S6 BTFR consistency (graded).**
- **What the law requires:** M_b,req = V⁴/(G a₀) for V ∈ {109, 128, 157} km/s (Di Teodoro). M_gas,req = M_b,req − M★ for M★ ∈ {10^9.5, 10^9.7}.
- **The statistic is the magnification the law would need:** μ* = M_gas,app / M_gas,req for every (α_CO, R₃₁, V, M★, footing) corner. The law is consistent with the measured CO if the image's real magnification equals μ*.
- **Classes (frozen), against the published magnification range μ_pub = [4, 12.4]:**
  - **CONSISTENT:** the μ* range across corners overlaps [4, 12.4].
  - **GAS SHORT:** every corner has μ* < 4 / 2 = 2. The measured gas is too little even at the lowest published magnification, by more than ×2, so the law lacks baryons. **TENSION.**
  - **GAS EXCESS:** every corner has μ* > 12.4 × 2 = 24.8. More gas than the law allows, by more than ×2. **TENSION** in the other direction.
  - **UNDECIDED:** otherwise.
- Under UPPER LIMIT, μ* is an upper bound: only GAS SHORT can be read. Under CLIPPED, nothing changes in S6, which uses Di Teodoro's V.
- **Reported, not graded:**
  - The same with V_CO (S4) in place of V_flat, if CLEAN.
  - The implied a₀ ratio V⁴/(G M_b a₀,local) at μ = 4 / 5.42 / 12.4, set against FLAT (1), DE-tracking (≈ 0.93, interpolated from CFG571's 0.94 / 0.92 at z 1.4 / 1.6) and H(z) (E(1.4906) = 2.355, Ω_m 0.315). **One disc excludes nothing** (CFG571's rule).

**S7 Position–velocity diagram (reported, not graded).**
- The kinematic major axis comes from the moment-1 gradient of the primary image. The PV is image-plane offset (″) vs velocity, and the plateau is described qualitatively.
- **The source-plane rotation curve needs a lens model.** It is a separate later lane: a lens-model download needs the owner's go, and that lane has its own criteria.

## Controls (each must pass, or the lane is INVALID)
- **K1 identity:** the four files' sha256 values equal the manifest's, and the headers equal those recorded above.
- **K2 noise:** the measured rms per 2 km/s channel at PB ≥ 0.9 in line-free channels lies within ×1.5 of the ObsCore-scaled expectation. That expectation is 66.6 μJy/beam at the native 488 kHz × √(0.488/0.926) = 48.4 μJy/beam.
- **K3 injection:** three synthetic exponential discs are injected into line-free regions at PB ≥ 0.7, at different positions. Each has scale 0.5″, projected V sin i = 60 km/s, and fluxes 0.1 / 0.3 / 1.0 Jy km/s. Each must be recovered by S1–S4 with S Δv within 20 % and W50 within 10 km/s.
- **MUTATE (rc 1):** channels shuffled (`default_rng(9701)`). The primary image's integrated S/N must fall below 3.

## Not blind (disclosed)
- **Seen:** the four FITS headers; Di Teodoro+2018's text values; KLASS and OLAS table values; ObsCore sensitivities.
- **Not seen:** any pixel value, moment map, spectrum or flux of the cube.
- **Power, stated honestly:** the brackets (α_CO × 5.4, R₃₁ × 1.6, V⁴ range × 4.3, M★ × 1.6) span about 1.5 dex in μ*. The test can only decide if the measured gas is far from the law's need (≳ × 2 outside the published μ range). **UNDECIDED is the likeliest outcome.**

## Statement-change rule
Only the a₀(z) target-search README's entry for this galaxy (rank 1) and a LEDGER row may change, per the frozen class. No a₀ value is quoted as a measurement, and no "favours".

## Files
`cfg970_co_btfr.py` (`MUTATE=1`). Outputs: `cfg970.out`, `cfg970_results.json`, small PNGs of the moment-0 map, spectrum and PV. Nothing large is written into the repo; the cube stays in `_external_data`.
