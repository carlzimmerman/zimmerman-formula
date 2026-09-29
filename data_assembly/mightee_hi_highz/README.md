# MIGHTEE-HI z > 0.25: the 11 individually detected HI galaxies (Jarvis+2025, arXiv:2506.11935)

Built 2026-09-29 by `build.py` on the owner's go ("yes, read the MIGHTEE-HI tables from the arXiv page"). Only the arXiv HTML page was fetched (`raw_small/`, sha256 in `manifest.json`); the two tables are parsed from its HTML cells by code.
Data only: no baryonic mass, no velocity, no a0 quantity is computed here.

## Files
`mightee_hi_highz.csv` (12 rows: IDs 1–10, 11a, 11b), `build.py`, `checks.txt` (4 PASS), `manifest.json`.

## Columns
From Table 2: `id`, `ra`, `dec` (hh:mm:ss, dd:mm:ss), `z`, `line_flux_JyHz` ± err, `logMHI` with `logMHI_err_SNRa` and `logMHI_err_syst` (the paper's parenthesised systematic), `snr_a/b/c` (three SNR estimates, defined in the paper's caption), `W50_kms` (measured line width, ± err),
`W50c_kms` (inclination-corrected, ± err), `incl_deg` ± err (from the g-band ellipticity, cos i = b/a, with an assigned ±5° uncertainty). From Table 3: `logMstar_withFarIR`, `logMstar_noFarIR` (BAGPIPES SED fits with and without data longward of 8 μm), SFRs, `S1p28_uJy` radio flux and radio SFR.
`logMHI_recomputed_Planck18` is a check column (my recomputation from the line flux with an assumed Planck18 cosmology).

## Checks that passed
- 12 Table-2 rows, as the paper describes (ID11 has two possible counterparts).
- W50c = W50 / sin(i) within 8% for every row that has both.
- log M_HI recomputed from the line flux agrees with the table within 0.094 dex for every row (the paper's own cosmology was not read; the worst row is ID7).

## What the paper says that bears on use (read from its text)
- The velocity widths are from the **integrated HI line** (channel width 104.5 kHz, ~16 km/s at z = 0.35, plus 5 km/s turbulent broadening); these are **not resolved rotation curves**; no radius is stated. The finite channel width and the inclination correction dominate the width uncertainties.
- The paper's baryonic mass is M_bar = M* + 1.4 M_HI (helium and metals factor). Molecular gas is **not measured**; the authors note it may be comparable to HI for M* > 1e10.
- The line detections are low-significance: SNR_a 4.1–6.4 for IDs 1–10, and 5.7 for ID11 (Table 2), SNR_c as low as 1.5 (ID3).
- Their bTFR result (Fig. 10): all galaxies lie within the scatter of the local Ponomareva+2021 relation, but the high-mass ones lie below it, which they read as a possible flattening or as W50 tracing V_max rather than V_flat in declining curves. I have not read the figure.
- **ID11** is blended (two counterparts, a and b); the paper says the very large corrected width of 11b implies confusion between the two, or that the line comes from 11a. Treat it as unusable.
- **ID10** has inclination 34° and a corrected width (692 km/s) much larger than the others: the inclination correction there is large and uncertain.
- The `*` flag in Table 3 (`star_or_dagger_flag_table3`) means the radio flux density was measured from the peak because the source failed the 5σ catalogue threshold (IDs 3, 4, 6); it is not a quality flag on the HI.

## Limits
- Which stellar-mass column (with or without far-IR) enters the paper's bTFR figure was not established from the text I read; both are included.
- The line fluxes are 4–7σ detections, the widths are from the integrated profile, and the inclinations are optical: this is a bTFR-level data set at z = 0.26–0.38, not a radial acceleration test.
