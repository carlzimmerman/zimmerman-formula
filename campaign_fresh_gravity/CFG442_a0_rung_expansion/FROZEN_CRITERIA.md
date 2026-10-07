# CFG442: expanding the ladder-anchored gas-dominated a₀ rung. FROZEN before any fitting script exists

Owner chat 10-06 (a₀ rung expansion; data fetches approved for this lane). κ = ½ is FITTED, never derived; both footings are reported (9.3603e-11 / 1.1312e-10 m/s²). No DM particle; the cold mass is still required.

**Why.** CFG397 (fe7a17fc5) measured a₀ from SPARC points where gas dominates the baryons. The 10 ladder-distance galaxies gave log a₀ = −9.953 ± 0.071, NOT ESTABLISHED because σ > 0.05. This lane adds more ladder-distance gas-dominated discs, using the same statistic.

**Pre-freeze data audit (disclosed).** Before freezing I checked only the data formats, never a₀ and never g_obs against g_bar. The audit found the following:
- the Oh+2015 VizieR tables (J/AJ/149/180) carry only the total and the DM-only curves;
- the arXiv source of Oh+2015 (1502.01281) has vector PDF figures whose disk–halo panels hold the gas (dotted) and stellar (dash-dot) curves as vector paths;
- calibrating each panel's axes on the VizieR total-curve markers reproduces V_gas² + V_star² = V_tot² − V_DM² to about 0.2% on 5 of 6 test galaxies (NGC 1569 failed);
- five galaxies have no stellar curve (no 3.6 µm image);
- CF4 table2 (J/ApJ/944/94) lacks four of the galaxies.

## Samples
- **S0 (control, unchanged).** CFG397's anchor: CFG4_common.load_sparc(), Q ≤ 2, ≥ 3 gas-dominated points, f_D ∈ {2, 3, 5}, SPARC distances. **C0:** the script must reproduce CFG397's anchor log a₀ to within 0.002 dex and its bootstrap σ to within 0.002.
- **SR (SPARC re-distanced).** These are galaxies that pass CFG397's selection (Q ≤ 2, ≥ 3 gas points) with f_D ∈ {1 Hubble flow, 4 UMa}, for which Cosmicflows-4 table2 gives a TRGB modulus (DMtrgb) or, failing that, a Cepheid modulus (DMceph). Each SPARC name is resolved to coordinates with CDS Sesame and matched to the nearest CF4 entry within 1′; the PGC is reported. Rescaling uses f = D_new/D_SPARC: R → fR, and V_gas², V_disk², V_bul² → f × (themselves). V_obs and e_V are unchanged. A galaxy without a CF4 TRGB or Cepheid modulus is not added.
- **LT (new galaxies, LITTLE THINGS, Oh+2015).** This sample is the 26 galaxies minus:
  - (i) the SPARC members, frozen alias list: DDO 50 = UGC 4305, DDO 87 = UGC 5918, DDO 126 = UGC 7559, DDO 154, DDO 168, Haro 29 = UGCA 281, NGC 2366, WLM = UGCA 444;
  - (ii) the galaxies without an authors' stellar curve: DDO 43, DDO 46, DDO 47, F564-V3, Haro 29;
  - (iii) the galaxies without a ladder distance.
  - **Distance rule.** The CF4 DMtrgb is used, else the DMceph, matched by the Hunter+2012 PGC (CVn I dwA = UGCA 292 = PGC 42275). If the galaxy is absent from CF4, the "fallback" is the Hunter+2012 distance, accepted only when its reference is a TRGB/Cepheid paper: DDO 70 (Sakai+2004), NGC 1569 (Grocholski+2008), UGC 8508 (Dalcanton+2009 ANGST). These three are flagged. Haro 36 (velocity distance) and DDO 101 (CF4 Tully-Fisher only) are excluded.
  - **Data.** V_obs and e_V come from the rotdmbar "Data" rows (asymmetric-drift corrected), de-scaled by R0.3 and V0.3. V_gas and V_star come from the vector paths in the disk–halo panel of the arXiv-source figure `rMD_DH_DM_profiles_<name>.pdf`: gas is the dotted path [1.44 2.88], stars the dash-dot path [1.44 2.88 7.68 2.88], both inside the panel frame.
  - **Axis calibration.** The grey filled "Total" markers are matched to the VizieR (R, V_tot) by RANSAC (seed 1, 60,000 trials, inlier tolerance 0.5 pt, sanity spans: the R-span ≥ 0.4 of the frame width and the V-span ≥ 0.15 of the frame height), followed by a least-squares refit on the inliers.
  - Curves are linearly interpolated onto the VizieR radii, with no extrapolation. The signed convention is V|V|.
  - V_gas² is multiplied by 1.33/1.4, from Oh's helium factor 1.4 to SPARC's 1.33. Stars stay at the authors' SPS Υ_3.6.
  - Distance rescaling uses f = D_new/D_Hunter: R → fR, and V_gas², V_star² → f × (themselves).
  - **C1 gates (per LT galaxy; a failed galaxy is excluded and listed):**
    - (a) the inliers number ≥ 0.8 × min(N_VizieR, N_markers − 1), and the rms is ≤ 0.15 pt on each axis;
    - (b) consistency: the median over matched radii of |V_gas² + V_star² − (V_tot² − V_DM²)| / V_tot² is ≤ 0.02, using the raw curves (1.4 helium) at radii where rotdm has a point within 0.1%.

## Selection and fit (CFG397, unchanged)
- **Selection.** A point is gas-dominated if V_gas² ≥ 0.7 V_bar², where V_bar² = V_gas|V_gas| + 0.5 V_disk² + 0.7 V_bul² for SPARC and V_gas|V_gas| + V_star,auth² for LT. It also needs V_bar² > 0 and V_obs > 0. A galaxy needs ≥ 3 such points.
- **Fit.** g = V²/R; the weights are w = 1/(max(e_V, 1)/max(V_obs, 1))². One free a₀ minimises Σ w (log g_obs − log[ν_mono(g_bar/a₀) g_bar])², bounded to (−10.8, −9.3) with xatol 1e-5. The bootstrap is over galaxies, 500 draws, seed 7, per sample.
- **Samples reported:**
  - **COMBINED = S0 + SR + LT (primary)**;
  - NEW-ONLY = SR + LT;
  - SR only;
  - LT only;
  - S0;
  - COMBINED without the three fallback-distance galaxies (reported only).

## Controls and verdict
- **K1 (Υ check, on COMBINED).** SPARC Υ_disk goes 0.5 → 0.7 (bulge 1.4Υ); LT V_star² is multiplied by 1.4. The point selection stays frozen at the baseline. PASS if |Δ log a₀| ≤ 0.05 dex. The 0.3 / ×0.6 variant is also reported.
- **C2 (LT-route method control).** The LT galaxies also in SPARC that have a stellar curve and pass C1 are rescaled to the SPARC distance. a₀ is fitted for the same galaxy set (those with ≥ 3 gas points in both routes), once through the LT route and once through the SPARC route. PASS if |Δ log a₀| ≤ 0.10 dex. **If C2 fails, the verdict is evaluated on S0 + SR only, and LT is reported only.**
- **RUNG ESTABLISHED** if the verdict sample (COMBINED, or S0 + SR after a C2 fail) has bootstrap σ ≤ 0.05 dex AND K1 passes. Otherwise NOT ESTABLISHED.
- **Reported:**
  - the distance of the verdict-sample a₀ from each footing (9.3603e-11, 1.1312e-10) and from PAPER43's 8.3e-11, in units of its σ, with |Δ| < 2σ = consistent;
  - its shift from CFG397's anchor;
  - the CF4/SPARC distance ratios for SR.
- **Disclosed departures:**
  - distance errors are not propagated (the same statistic as CFG397);
  - the LT baryons come from vector figure paths, not from a table;
  - LT stars use the authors' SPS Υ, not 0.5;
  - the three fallback distances rest on Hunter+2012's reference choice.
- **MUTATE (`--mutate`).** Drop the gas term (V_gas → 0) in every route. The gas-dominated selection then becomes empty; the script must detect it and exit 1. Outputs carry the `_MUTATE` suffix.

**Data and fetch rules.** Every fetch is logged in FETCH_LOG.md (URL, date, bytes, sha256). Files > 5 MB go to campaign_fresh_gravity/_external_data/cfg442/ (git-ignored).
