# CFG668 addendum A1 — deep rerun on KiDS DR5 and DES Y6 (FROZEN, committed before any KiDS/DES count is pulled)

Why: the SDSS run (33ff902b3) was NOT DIAGNOSTIC. Every SDSS bin had a count slope s > 0.4, so the sign-flip test could not run,
and member leakage through SDSS photo-z dominated. Deeper data reaches magnitudes where s < 0.4, and the photo-z are better.

## Data (raw; no cosmology; angular annuli 0–2', 2–4', 4–6')
- KiDS DR5 (ESO TAP, KiDS_DR5_0_ugriZYJHKs_cat_fits): SG_FLAG=1, MASK=0, MAG_AUTO (r) 20–24, Z_B photo-z.
- DES Y6 Gold (NOIRLab Data Lab, des_dr2.y6_gold): ext_mash>=3, flags_gold=0, mag_auto_r 20–24, dnf_z photo-z.
- Clusters: SDSS redMaPPer DR8, λ > 30 (lowered from 60 because the footprint overlap is small; fixed now, before any counts),
  0.1 ≤ z_λ ≤ 0.3, inside each survey's footprint. Same cluster selection for both surveys.
- Blank fields: 2 per cluster, offset 1–3° (seed 668), no redMaPPer λ>20 cluster within 15'.
- Footprint/edge cut, same for clusters and blanks: keep a pointing only if its total galaxy count within 6' (no photo-z cut)
  is ≥ 0.7 × the median over blank fields of that survey.
- Magnitude bins (r): 20–22, 22–23, 23–24. Slope s from the blank-field counts in each bin.

## Photo-z gap
Primary gap: photo-z > z_λ + 0.3. Confirming gap: + 0.4. Full ladder 0.1–0.5 reported. (0.3/0.4 were chosen from the SDSS ladder,
where leakage had mostly gone by 0.3–0.4; KiDS/DES photo-z are better, so this is conservative. Disclosed.)

## Decision rules (per survey, then combined by inverse-variance)
- LENSING DETECTED: in the 0–2' or 2–4' annulus, at BOTH primary and confirming gaps, a bin with s < 0.4 shows a DEFICIT
  (R < 1 at ≥ 2σ, bootstrap over pointings) AND a bin with s > 0.4 shows an excess or R ≥ 1. A deficit cannot come from member leakage.
- OBSCURATION FLAG: a deficit in every bin including s > 0.4 → masking by members, not diagnostic.
- CONTAMINATED: excess ≥ 2σ in every bin including s < 0.4 → not diagnostic.
- NULL: no bin departs from 1 at ≥ 2σ.
- If detected: report implied μ = R^(1/(2.5s−1)) and weak-field κ ≈ (μ−1)/2 as a raw statement that mass lenses along cluster
  sightlines. No ΛCDM halo comparison. A baryons-only κ needs cluster gas maps and is not part of this addendum.
MUTATE: half the blanks play clusters → R must return to 1.
κ fitted; cold energy mass required; not theory closed.
