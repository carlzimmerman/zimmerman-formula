# CFG163 — KURVS-15's cold gas from archival ALMA: does its gas fall below 0.65, between 0.65 and 2.14, or above 2.14 M*? FROZEN PLAN

Written 2026-09-29, at the orchestrator's go, before any cube is downloaded or read.
- **The products** are priced by the data chat (a1c633697, `data_assembly/alma_archive_footprint/KURVS15_PRICE_SHEET.md`). The download waits for that chat's own user.
- **The data chat's role** is to extract the cubes and report only header facts (beam, channels, frequency axis, file hashes). It opens no flux value.
- **Every flux, moment and conversion is this lane's,** and none is computed before this file is committed.
- Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## The question

Does KURVS-15's cold gas mass support a total gas fraction μ = M_gas/M* below 0.65, between 0.65 and 2.14, or above 2.14?
- These two numbers are the break-evens found by CFG165, the Opus chat's re-derivation of CFG160, and are taken as given: under P4 the rival a₀ ∝ H(z) fits exactly at μ = 0.65, and flat a₀ at μ = 2.14.
- **This is one disc,** so it checks the gas prior of CFG160/CFG162. It is not an a₀ test.
- **CO measures molecular gas only.** The measured μ_mol is therefore a lower bound on the total μ; HI is unmeasured.

## The data (from the price sheet; header facts to be confirmed by the data chat)

- KURVS-15 = CANDELS cdfs_31127; z_Hα = 1.613, so CO(2-1) is at 88.23 GHz and CO(5-4) near 220.5 GHz.
- **Ibar Band 3** (2018.1.00164.S, spw 29, 2.48″ beam): the CO(2-1) cube, pbcor and pb. The whole galaxy lies in one beam. **This is the primary total CO flux.**
- **Molina Band 3** (2019.1.01238.S, spw 23 repBW, 0.11″): CO(2-1) at about 1 kpc resolution. The source is resolved into many beams, and extended flux can be resolved out. **Its flux is a lower bound, used for structure and a consistency check, not for the total.**
- **Ibar Band 6** (spw 29, 1.0″): CO(5-4), **used for excitation only (R52), never for a gas mass**; plus the 1.2-mm dust continuum image, a second, independent gas estimate.

## Measurement (declared)

- **Position:** the KURVS position of KURVS-15 (data chat, e08195747).
- **Velocity window:** centred at z_Hα. The primary window is ±300 km/s; ±400 km/s is a variant.
- **Ibar Band 3 (primary):**
  - The spectrum is the peak-pixel spectrum at the position, in Jy/beam, which is the total flux for a source smaller than the beam.
  - A 1.5″-radius aperture sum is a variant that tests for extension.
  - S_CO Δv is the channel sum over the window times the channel width.
- **Noise:**
  - σ_int = the standard deviation of the same window-sum at 20 or more line-free positions in the cube, each at least 3 beams from KURVS-15 and inside the pb ≥ 0.5 region.
  - The channel-rms estimate σ_ch √N_ch Δv is reported beside it.
- **Detection:** S_CO Δv ≥ 4 σ_int (the known position and redshift).
- **Upper limit** if not detected: 3 σ_int. It is never read as zero.
- **Molina Band 3:** the aperture sum in radii of 0.5″ and 1.0″ over the same window, with its own σ_int from off-source apertures of the same size. The flux is reported as a lower bound, and the resolved-out risk is stated.
- **Dust (Ibar Band 6 continuum):**
  - The peak-pixel flux at the position; a 1.0″ aperture as a variant.
  - Detection at ≥ 4σ against the image rms from off-source pixels; a 3σ limit otherwise.
  - M_ISM from CFG142's Scoville et al. 2016 conversion (T_d = 25 K) at the image's reference frequency, with the ×2 gas-to-dust bracket.

## Conversion (declared)

- **Luminosity:** L′_CO(2-1) = 3.25 × 10⁷ S_CO Δv ν_obs⁻² D_L² (1+z)⁻³ K km s⁻¹ pc². Here S in Jy km s⁻¹, ν_obs in GHz and D_L in Mpc (Planck18), following Solomon & Vanden Bout 2005.
- **CO(1-0):** L′_CO(1-0) = L′_CO(2-1)/R21, with R21 = 0.8 primary and a bracket of 0.6–1.0.
- **Molecular mass:** M_mol = α_CO L′_CO(1-0).
  - α_CO = 4.36 M☉ (K km s⁻¹ pc²)⁻¹ is primary: Galactic, including helium, the standard for main-sequence discs at these masses.
  - The bracket is 0.8 (ULIRG-like) to 4.36.
  - An α_CO of 8 (sub-solar metallicity) is reported as an upper-side variant.
- **M*:** MAGPHYS from the KURVS table (log M* = 10.07), ±0.2 dex.
- **The gas fraction:** μ_mol = M_mol/M*. The dust gives μ_dust, as in CFG142.

## Power (computed from the price sheet's stated sensitivities, before any data)

- **The expected flux** at α_CO = 4.36, R21 = 0.8, D_L = 12.25 Gpc:
  - μ_mol = 0.65 gives S_CO Δv ≈ 0.040 Jy km s⁻¹;
  - μ_mol = 2.14 gives ≈ 0.130 Jy km s⁻¹.
- **Ibar Band 3** (1.1 mJy/beam per 10 km s⁻¹; ±300 km/s is 60 channels):
  - σ_int ≈ 1.1 × 10 × √60 ≈ 85 mJy km s⁻¹.
  - A 4σ detection needs S ≳ 0.34 Jy km s⁻¹, i.e. μ_mol ≳ 5.5.
  - A non-detection limits μ_mol ≲ 4.2 (3σ).
  - **So the CO test can only (a) detect a gas-rich disc (μ_mol ≳ 5.5, above both break-evens), or (b) return a non-diagnostic limit above 2.14.** It cannot reach either break-even with a non-detection.
- **Molina Band 3:** at 0.11″ the source spans about 100 beams, so its integrated noise is larger still. It is not a total-flux test.
- **Dust (Ibar Band 6, 816 s):**
  - The image rms is not in the archive metadata. A declared rough expectation is 30–40 μJy/beam; the measured rms replaces it after reading, and that is disclosed.
  - At that rms, μ_dust = 2 gives about 0.17 mJy (CFG142's conversion at about 250 GHz): a 4–6σ detection.
  - **So the dust may be the only channel with power at the break-evens.** This is recorded before the data.

## Outcomes and what each would mean (declared)

Primary conversions throughout. The α_CO and R21 bracket is reported, with whether it straddles a break-even.

- **Gas detected with μ_mol (or μ_dust) > 2.14:** KURVS-15's molecular gas alone exceeds flat's break-even. At this gas both readings over-predict under P4. For this disc the gas prior sits on the high side, where CFG160's lean toward the rival does not hold. It is one disc.
- **Detected with 0.65 ≤ μ < 2.14:** the gas is at least at the rival's break-even. The rival would then over-predict, while flat is not excluded, since HI would raise the total. It weakens the lean for this disc.
- **Detected with μ < 0.65:** the molecular gas is below the rival's break-even. The total turns on HI. It is consistent with the low-gas side, where the lean holds, but only if HI is small.
- **Not detected, with the limit μ_lim:**
  - μ_lim < 0.65: as the previous case, but as a limit.
  - 0.65 ≤ μ_lim < 2.14: it excludes only molecular gas above μ_lim.
  - μ_lim ≥ 2.14: NON-DIAGNOSTIC. This is the expected CO outcome, per the power row.
- **For CFG160 and CFG162:** any of these is reported as a gas-prior statement for one disc. The decision cell (μ = 0.67) and the frozen verdicts are not re-scored.

## Checks

- **C1 CONTROL (injection):** a synthetic line of known flux (0.5 Jy km s⁻¹, Gaussian, FWHM 250 km s⁻¹, a point source) is injected at an off-source position inside pb ≥ 0.5 of the Ibar Band 3 cube. The peak-pixel pipeline must recover it within 15%.
- **C2 CONTROL:** the cube's frequency axis contains 88.23 GHz ± the window (from the header).
- **C3 CONTROL:** σ_int from off-source window-sums and from σ_ch√N Δv agree within 30%.
- **C4 CONTROL:** the L′ formula reproduces a hand-worked example to 1e-10, and the dust conversion reproduces CFG142's C-0 value.

## MUTATE (two pinned controls, since the outcome's direction is unknown)

- **MUTATE=1:** a line of μ_mol = 8 (primary conversion) is injected at KURVS-15's position. The classification must read "detected, > 2.14".
- **MUTATE=2:** KURVS-15's spectrum is replaced by the spectrum at an off-source position. The classification must read "not detected".
- One of the two necessarily differs from the main run. Both must behave as stated.

## Untested (declared)

- HI;
- α_CO beyond the bracket;
- CO excitation beyond R21;
- the dust temperature beyond 25 K (35 K is reported);
- dust-to-gas below the ×2 bracket;
- the ten-disc gas distribution (this is one disc);
- the P4 model itself.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Addendum (2026-09-29, before any number; at the orchestrator's check; the criteria above are otherwise unchanged)

This addendum was written after the data chat reported the continuum image's header-level facts (no pixel value), and before any file was downloaded or read.

**(1) The Band 6 continuum is at 227.3 GHz (1.32 mm), not 1.2 mm.**
- **The image:** four windows at 219.4, 221.2, 233.4 and 235.2 GHz (mean 227.3 GHz), with a 1.0″ beam and 816 s on source.
- **Rest frame:** at z = 1.613 the rest frequency is 594 GHz, i.e. a rest wavelength of 505 μm.
- **The extrapolation:** Scoville et al. 2016's conversion is calibrated at rest 850 μm and carried to other rest frequencies by its ν^3.8 factor (β = 1.8) and the Rayleigh–Jeans correction Γ_RJ(T_d, ν_obs, z).
  - At rest 505 μm and T_d = 25 K, Γ_RJ = 0.536 against Γ₀ = 0.699.
  - The dust temperature bracket is declared as 25 K (primary) to 35 K.
- **The requirement flux at 227.3 GHz** (nominal M*, dust-to-gas × 1):

  | T_d | μ_dust = 2 | μ_dust = 0.65 | μ_dust = 2.14 |
  |---|---|---|---|
  | 25 K | 0.128 mJy | 0.042 mJy | 0.137 mJy |
  | 35 K | 0.139 mJy | 0.045 mJy | 0.148 mJy |

  This replaces the plan's 0.17 mJy, which was for 250 GHz.
- **The power depends on the rms, which is not yet measured.** The archive's own estimate is 0.0646 per 1.875-GHz window (unit unstated, presumably mJy/beam).
  - **If that averages down over the four windows to ≈ 32 μJy/beam:**
    - μ_dust = 2 is a 3.9σ signal (4.3σ at 35 K);
    - a 4σ detection needs μ_dust ≥ 2.03;
    - a 3σ non-detection limits μ_dust ≤ 1.52;
    - μ = 0.65 is only 1.3σ.
  - **If 0.0646 mJy/beam is the combined rms:**
    - μ_dust = 2 is 2.0σ;
    - a detection needs μ_dust ≥ 4.05;
    - a non-detection limits μ_dust ≤ 3.04.
    - **The power then collapses at both break-evens.**
  - **Either way,** the dust channel cannot reach the rival's break-even (0.65). At best it can tell whether the gas is near or above flat's break-even (2.14), and only at the nominal gas-to-dust ratio. With the ×2 bracket the 32-μJy limit becomes μ_total ≤ 3.0.

**(2) The rms rule and a power gate (fixed now, applied before the source flux is read).**
- **Measuring σ₀:** robust σ₀ = 1.4826 × MAD of (pbcor × pb) pixels in an annulus 3″–10″ from KURVS-15, restricted to pb ≥ 0.5, with 2″ excluded around every GOODS-ALMA 2.0 catalogue source and every KURVS position.
- **The noise at the source:** σ = σ₀/pb(KURVS-15).
- **The power gate:** μ_dust,3σ = 3σ/(S per unit μ_dust) at 25 K, nominal M*. If μ_dust,3σ ≥ 2.14, the dust channel is declared NON-DIAGNOSTIC and the flux at KURVS-15 is not read for a verdict (it may be reported afterwards, labelled). Otherwise the plan proceeds.
- The archive estimate is reported beside the measured value.

**(3) Beam against source size (as declared).**
- At 1.0″ (8.6 kpc at z = 1.613) KURVS-15's dust is expected to be close to unresolved.
- The peak pixel is primary, and the 1.0″ aperture sum is the declared variant. Their ratio is reported as a size check.

**(4) Recommendation to the data chat** (a statement of expected value; the download decision is its user's):
- **The continuum image and its pb** (about 0.4 MB) are cheap, and the power gate decides their value from the measured rms.
- **The CO(2-1) cubes** (6.6 GB) are non-diagnostic at both break-evens by the plan's power row. They can only detect a disc with μ_mol ≳ 5.5. Their expected value for this question is low.
