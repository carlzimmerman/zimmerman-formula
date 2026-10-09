# CFG528b FROZEN CRITERIA: the four SLUGGS centrals with MEASURED GC density profiles and MEASURED anisotropy

Written 2026-10-09, after the source files were read for input values and before any CFG528b code was written or any CFG528b
number computed. κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10, never pooled. Kernel ν_mono. The cold energy's mass is still
required. Not "theory closed". No knob is fitted.

## Data provenance
The coordinating session fetched the arXiv LaTeX sources on the owner's direct approval. They are stored outside git in
`../_external_data/cfg528_work/src/`; the log is copied as `FETCH_LOG.md`. All 7 SHA-256 values were re-verified on 2026-10-09.
The total is 26.6 MB, larger than the ~1 MB estimate but under the 50 MB limit. Each paper's title and galaxy were checked in its
own .tex. Line numbers refer to the .tex named.

| galaxy | source (.tex, lines) | value used | projected or 3D |
|---|---|---|---|
| NGC 4374 | Gómez & Richtler 2004, "The Globular Cluster System of NGC 4374", h4350.tex L733–740 | all GCs: Σ ∝ R^(−1.09 ± 0.12), measured ~5 kpc–350″ | **projected** (the text names it "the cluster surface density"). 3D: γ = 1 + 1.09 = 2.09 ± 0.12 |
| NGC 4374 (reported) | same, L613–614 | red R^(−1.22 ± 0.12), blue R^(−1.00 ± 0.15) | projected (same table/procedure); 3D 2.22 / 2.00 |
| NGC 4365 | Blom+12, "Wide-field imaging of NGC 4365's globular cluster system", 4365photom_astroph.tex Table tab:gcSers (L346–352), Eq. L332–339 | Sérsic, all GCs brighter than the turnover: n = 2.68 ± 0.41, R_e = 6.1 ± 1.2 arcmin, b_n = 1.9992n − 0.3271 (their equation) | projected; deprojected numerically (Abel) |
| NGC 4365 (reported) | same, L357 | power law beyond R_e: −1.21 ± 0.03 | projected; 3D 2.21 |
| NGC 5846 | Napolitano+14, "The SLUGGS Survey: Breaking degeneracies ... NGC 5846", napolitano_R2.tex L133, L148 | red: n = 2.9, R_e = 160″, N_e = 3.3; blue: n = 2.9, R_e = 780″, N_e = 0.24 (same units); b_n by Ciotti–Bertin | projected; tracer = red + blue sum, deprojected |
| NGC 5846 β | same, L300–305, L395, L499, Table tab:jeanssumm (ani-noAC row) | β(r) = (β₂ r^c + β₁ r_a^c)/(r^c + r_a^c), β₁ = 0, c = 6; red r_a = 200″, β₂ = 0.43; blue r_a = 100″, β₂ = 0.15; typical uncertainty ~0.1 (table caption) | 3D |
| M87 density | Agnello+14 three populations (the record's measured tracer, CFG323/CFG466 values); alternative: Peng+08 via Zhu+14 (ms_apj.tex L161–166, CFG323 `Z14`) | as in CFG466 | projected; deprojected |
| M87 β | Zhu+14, "NGVS V. ... M87 with the made-to-measure method", ms_apj.tex L118, L642 | text: β = −0.2 at the centre, negative inside ~15 kpc, maximum +0.2 at ~40 kpc, back to 0 at ~120 kpc. Digitised from the text as nodes (≤5 kpc, −0.2), (15, 0), (40, +0.2), (≥120, 0), linear in ln r. The tex gives no table, so this is a declared digitisation | 3D |
| M87 β (reported only) | Agnello+14, secpaper4.tex L1402–1412 | qualitative: red slightly tangential, intermediate ≈ +0.3, blue isotropic → mildly tangential; posteriors only in figures | not used numerically |
| NGC 4365, 4374 β | none in the fetched files (Pota+13 1209.4351 gives density fits only in figures; Kartha+14 1310.1979 covers other galaxies, unused) | UNMEASURED | — |

Caveats declared now:
- (i) The NGC 5846 and M87 β values come from Newtonian models (NFW halo, or M2M with a dark halo). The kurtosis-based
  anisotropy is less model-dependent, but it is not the law's own fit.
- (ii) The photometric GC mixture is applied to the spectroscopic SLUGGS sample.
- (iii) Distance differences between papers (arcsec → kpc) use the SLUGGS SBF distance. Zhu's kpc nodes are used as printed.

## Machinery (unchanged from CFG528)
- CFG331's source is exec'd read-only to its run block. Same bins, outer mask, JAM calibration, gas, members, readings and
  per-galaxy σ_i (CFG466 bootstrap at γ = 3; CFG466 shows σ_i is flat in γ).
- New code: a Jeans solver for tabulated ρ(r) with radially varying β(r) and several populations. Each population j gets
  ρ_j σ_r,j² = F_j⁻¹ ∫_r^∞ F_j ρ_j g dr, with F_j = exp ∫ 2β_j d ln r. The projection is
  σ_los² = Σ_j ∫(1 − β_j R²/r²) ρ_j σ_r,j² … / Σ_j ∫ρ_j ….
- Z_i, CLEARED (Z < 2), REVERSED (Z < −2) and CLOSES (≥ 3/4 cleared, none reversed, BOTH footings) are as in CFG528.

## Rows (both footings)
- **M (measured, primary):** each galaxy's measured density at central values, and measured β where available (M87 Zhu, NGC 5846 Napolitano ani-noAC). NGC 4365 and 4374 get β = 0. Readings: K0 (stars only), R-bar, R-own.
- **Reported rows:**
  - M with β = 0 for all;
  - NGC 4374 red-only and blue-only slopes;
  - NGC 4365 power law 2.21;
  - M87 Peng/Zhu density;
  - NGC 5846 red-only tracer with red β.
- **J (joint best case):** R-own; heaviest admissible IMF per galaxy (as CFG528); distance × 1.1. Then, per galaxy, the most favourable of:
  - **density:** central and ±2σ edges of each quoted parameter, i.e. NGC 4374 slope 1.09 ± 0.24; NGC 4365 n ± 0.82, R_e ± 2.4′ (4 corners + centre); NGC 5846 n and R_e of both populations jointly × (1 ± 0.2), declared because no errors are quoted; M87 Agnello central or Peng/Zhu;
  - **β:** measured β profile shifted by ±0.1 or 0 (M87, NGC 5846); {−0.5, 0, +0.5} for the unmeasured NGC 4365 and 4374.

  This is propagation of quoted uncertainty, not a fit. The grid is fixed here.

## Verdict (in order)
1. **DATA-ISSUE** (the γ = 3 / isotropic assumption caused the fail) if row M under K0 CLOSES.
2. **MECHANISM FOUND** if row M under R-bar or R-own CLOSES.
3. **NOT DIAGNOSTIC** if J CLOSES.
4. **GENUINE TENSION** otherwise, with σ = Z_class of J on the less favourable footing.

The template is not used.

## Controls
- **K1** The new solver with ρ ∝ r⁻³ and constant β ∈ {0, +0.5} reproduces CFG331's `sig_los` offsets to ≤ 1e-3 dex.
- **K2** Abel deprojection of a Plummer surface density matches the analytic ρ to ≤ 1e-3 relative over the GC range.
- **K3** The M87 Agnello central profile with β = 0 under K0 reproduces CFG466's C4 offset (+0.2178 can / +0.2062 alt) to ≤ 2e-3.
- **K4** The SHA-256 of each source tar matches FETCH_LOG.md (checked in the script).

## MUTATE (`CFG528B_MUTATE=1`, separate outputs)
- **MA (must reproduce):** γ = 3 power law and β = 0 for all four. It must reproduce CFG528's K0 and R-own per central to ≤ 1e-3 dex.
- **MB (must FAIL to close):** γ = 4 power law and β = −0.5, K0. It must not close on either footing, and every offset must be ≥ that galaxy's row-M K0 offset. If it closes, the MUTATE FAILS (kept).

## Outputs
`cfg528b_measured_tracers.py` → `.out`, `_results.json`, `_MUTATE.*`. The README gets a CFG528b section. Frozen text is never edited.
