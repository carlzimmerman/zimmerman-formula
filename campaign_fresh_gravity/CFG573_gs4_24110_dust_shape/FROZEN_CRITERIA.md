# CFG573 FROZEN CRITERIA: where GS4_24110's gas sits (public 0.13″ dust image), and how that moves CFG572's Δ_v

Committed alone, before the image is downloaded. Owner yes (10-09: "yeah", to "want me to grab the dust map?").

## Why
CFG572 (12779c1e5) assumed the gas follows an exponential disc with R_g = R_d = R_e/1.678 = 4.40 kpc (primary) or 1.5 R_d. Where the gas sits changes how much of it acts inside R_e = 7.39 kpc. Compact gas puts more mass inside R_e, which raises Δ_v.

## Data
- Public 2015.1.00664.S, MOUS uid://A001/X2fe/X93e, target KMOS3DGS4-24110.
- Only the ARI-L continuum image `...KMOS3DGS4-24110_sci.spw0_1_2_3_264927MHz.12m.cont.I.pbcor.fits` and its `.pb.fits.gz` (~10 MB). No cubes, no ASDM.

## Measurement
- **Detection:** peak S/N ≥ 5 within 0.5″ of the KMOS3D position. Noise = robust σ (1.4826 × MAD) of the image within 2–6″ of the source, using pb ≥ 0.5.
- **Size:** fit an elliptical 2-D Gaussian (free centre, amplitude, σ_x, σ_y, PA) to a 2″ × 2″ cutout. Deconvolve the beam in quadrature (per axis, circularised). The circularised half-light radius is R_e,dust = FWHM_deconv / 2 (Gaussian), in kpc at D_A (flat ΛCDM, H0 70, Ωm 0.3). Uncertainty: refit on 200 noise realisations, made by adding cutouts drawn from source-free regions of the same image.
- **Flux recovery:** the integrated Gaussian flux is compared with Boogaard+2020's 1.2 mm 342 ± 34 μJy, scaled to 264.9 GHz as (ν/242.6 GHz)^(2+β), β = 1.8.
  - If recovery < 50%, extended emission is resolved out. R_e,dust is then reported as a **lower bound** and the gas is plausibly more extended.

## Effect on Δ_v (CFG572 recipe, dust-route gas 10^10.51, canon footing; stellar branches 10.89 / 10.76)
- **Gas shape S1:** an exponential disc with R_d,gas = R_e,dust / 1.678 (Freeman).
- **Gas shape S2:** a spherical Gaussian with the same R_e (enclosed-mass, reported).
- Report Δ_v per model (F-DESI, F-flat, R-H, L-fb RAR-eq) and the Newtonian reference, next to CFG572's value. Verdict words as in CFG572 (tension = |Δ_v| > 2σ).

## Controls
- **C1:** a beam-shaped point source injected 3″ away is fit with a deconvolved size < beam/3, and its flux is recovered within 15%.
- **C2:** the fit on the KMOS3D position shifted by 2″ (blank sky) gives no ≥ 5σ detection.
- **MUTATE:** run the full pipeline on the 2″-shifted position. It must fail detection (exit 1). Output tagged _MUTATE.
- Failed controls are kept and reported.

## Not claimed
Dust shape = gas shape is an assumption (declared). One galaxy. κ = ½ fitted; the cold mass is still required.
