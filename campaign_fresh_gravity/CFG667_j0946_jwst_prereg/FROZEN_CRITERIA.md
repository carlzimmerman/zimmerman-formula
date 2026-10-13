# CFG667 FROZEN CRITERIA: sealed prediction for JWST GO 12088 (the J0946+1006 lens perturber)

Date: 2026-10-12. Committed ALONE before any CFG667 script or number. Block CFG660–669. Append-only after commit.
κ = ½ FITTED; footings separate (never pooled); cold energy mass required; no particle species; not "theory closed".

## 0. Why, and what has been seen

JWST GO 12088 (PI Q. He, Kapteyn; Cycle 5; 5.3 h NIRCam F070W/F115W/F200W/F277W/F356W/F444W; status "Flight Ready"; MAST
calib_level −1 = not yet observed on 2026-10-12; 12-month exclusive access) is titled "Unveiling the Nature of an Unusual Dark
Matter Subhalo in the Strong Lensing System SDSSJ0946+1006 with JWST". CFG666 (b9b9009ad + result) found the perturber's
published solutions split: dark (M3D<0.3 kpc 5.8e8, L_V < 5e6) EXCLUDED under the law, luminous (L 10^8.4, M_proj<1 kpc 10^8.9)
CONSISTENT. GO 12088 will measure the perturber's stellar light directly. No GO 12088 data exist; this is a prediction.

## 1. The prediction (a function of whatever lensing mass is reported)

The law with cold energy settled in the satellite's own baryons (R-iso) or with the host's field acting (R-EFE) brackets the
baryonic mass inside any radius R where lensing measures M_lens(<R):
  **M_lens / ν_mono(g_N/a0) ≤ M_b(<R) ≤ M_lens**, with g_N = G M_b(<R)/R² solved self-consistently (spherical).
Equivalently the dynamical-to-baryonic ratio Q(R) = M_lens/M_b(<R) lies in [1, Q_max(M_lens, R)].
The script tabulates Q_max on a grid M_lens ∈ [1e7, 1e10] M☉ × R ∈ [0.1, 2] kpc, both footings, and evaluates it at the
published points (0.3 kpc / 5.8e8; 0.6 kpc / 1.1e9; 1 kpc / 10^8.9 and its 95% ends 10^8.1, 10^10.0).
M_b = stars + gas. For a satellite inside an early-type lens, gas is taken as ≤ 20% of M_b (stated assumption; a measured gas
mass replaces it).

## 2. Decision rules for the GO 12088 result (applied by whoever scores it; frozen now)

Let Q_obs(R) = M_lens(<R)/M_*(<R) from the GO 12088 team's (or an independent) joint lens + light analysis, M_* from their
stellar-population fit, at the radius where the lensing mass is best constrained.
- **SURVIVES** if Q_obs ≤ 1.25 × Q_max (1.25 = the gas allowance; the M_* error bar is added in quadrature as reported).
- **EXCLUDED** if Q_obs > 3 × Q_max at ≥ 2σ of the reported M_* error (3 = a generous IMF/population systematic).
- **TENSION** in between. **NOT DIAGNOSTIC** if no stellar counterpart is constrained (neither detected nor limited) within 1 kpc.
- A non-detection gives an upper limit on M_*: EXCLUDED if M_lens/M_*,lim > 3 Q_max.
ΛCDM context only (no verdict weight): a dark-matter-dominated subhalo centre gives Q ≫ Q_max at 0.3 kpc.

## 3. Seal

The script writes `cfg667_predictions.json`; its sha256 is committed in `cfg667_PREDICTIONS_HASH.txt` in the result commit.
Neither file is edited afterwards. MUTATE (`CFG667_MUTATE=1`): a0 → 0 must give Q_max = 1 everywhere (exit 1 iff it bites).

## 4. Limits named now

Spherical treatment of projected masses; Υ and IMF of the satellite; line-of-sight position (perturber may not be in the lens
plane); lens-light subtraction systematics in the data; the GO 12088 team's choices. The prediction is the law's, not a model fit.
