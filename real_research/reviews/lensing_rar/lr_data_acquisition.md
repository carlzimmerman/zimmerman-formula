# LR data acquisition — full KiDS-1000 + GAMA re-run (Carl's choice: gold standard)

> **REORDER (Fable, 2026-06-10):** Brouwer's **measured ESD profiles are a public release** (`brouwer2021_rar.tar`, 2.3 MB,
> kids.strw.leidenuniv.nl/sci_data — pre-split per figure incl. Fig-8 colour/Sérsic early/late + covariances). The systematics
> **battery runs directly on these profiles** (see `lr_battery_results.md`), so GAP-1 (the exact u−r threshold, which turned out
> to be **2.5** from the covariance bin-edges) is moot for the battery. The **16 GB shear stack demotes to an independent
> re-measurement** (validate the released profiles from scratch). The battery is DONE; the re-measurement is the open track.

*C. Zimmerman, 2026-06-10. Provenance log for the from-scratch ESD re-run. DOI-pinned per the standing rule. The large FITS
are gitignored (`real_research/data/lensing_rar/.gitignore`); this log + the pipeline scripts are the versioned record.*

## Data products (located, pinned)
| Product | File | Size | Rows | DOI / cite | Status |
|---|---|---|---|---|---|
| **Lens photo-z** (KiDS-bright) | `KiDS_DR4_brightsample.fits` | 85 MB | 1,239,422 | Bilicki+2021, **10.1051/0004-6361/202140352** | ✅ down + FITS-verified |
| **Lens physical props** (LePhare) | `KiDS_DR4_brightsample_LePhare.fits` | 246 MB | 1,239,422 | same | ✅ down + verified |
| **Source shear** (SOM-gold WL) | `KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits` | **16 GB** | ~millions | Kuijken+2019, Giblin+2021, Hildebrandt+2021 (A&A 647 A124 / 645 A105) | ⏳ downloading (bg) |
| GAMA spectroscopy (validation) | — | — | 238k | Driver+2011, GAMA DR4 | ⏳ to fetch (validation only) |
All from the official KiDS DR4 release `https://kids.strw.leidenuniv.nl/DR4/` (`brightsample.php`, `lensing.php`). Direct,
public, no auth. Checksums = the Content-Length verified on download (89,259,840 / 257,817,600 bytes).

## Columns confirmed (lens side — everything needed except Sérsic)
- **brightsample:** `ID, RAJ2000, DECJ2000, MAG_AUTO_CALIB (r), zphot_ANNz2, MASK, masked`.
- **LePhare:** `MASS_MED/BEST` (stellar mass PDF median/best), `MAG_ABS_u…Ks` (rest-frame absolute mags → **u−r = MAG_ABS_u − MAG_ABS_r**),
  `K_COR_*`, `REDSHIFT`, `SFR_*`.
- ⇒ **lens selection, isolation, M⋆, and the u−r morphological split are ALL reproducible from these two files.**

## The Sérsic gap (GAP-1, logged honestly)
Sérsic index n is **not** in the bright-sample release. Brouwer split on **both** Sérsic n AND u−r. Plan: run the **u−r split as
primary** (fully reproducible here); obtain the KiDS 2DPHOT/Sérsic morphology catalogue (La Barbera-style) for the n-split as a
cross-check. If the n-catalogue is not public, the u−r split alone still tests claim (b) — and Brouwer report the 6σ for *each*
split independently, so u−r is a valid standalone replication. Flag any single-axis limitation in the verdict.

## Fidelity details to honor (transcribed)
- **M⋆ fluxscale:** Bilicki masses need the GAaP→total `fluxscale` aperture correction (Brouwer: "with fluxscale correction
  required"). Check whether `MASS_MED` is pre- or post-fluxscale; apply if needed. *(GAP-1b)*
- **Cold gas:** M_gal = M⋆(1+f_cold), log f_cold = −0.69 log(M⋆) + 6.63 (Boselli+2014).
- **g_obs = 4 G ΔΣ_obs** (SIS, Eq. 7); **g_bar = G M_gal/r²** (point mass).
- **Isolation:** no satellite with M⋆,sat/M⋆,lens > 0.1 within 3 h₇₀⁻¹ Mpc (compute on the bright sample itself).

## Pipeline plan (next, once shear lands)
1. **Lens side (buildable NOW):** select r<20, 0.1<z<0.5, M⋆<10¹¹, masked==0; compute isolation; derive u−r; split early/late.
2. **GGL ESD stack:** for each lens, stack source tangential ellipticities in log-R bins, Σ_crit-weighted by lens/source photo-z
   geometry; ΔΣ(R) per Eq. 1; analytic covariance (Viola+2015). Bin by g_bar (15 bins, 1e-15–5e-12).
3. **RAR:** g_obs = 4GΔΣ; g_bar = GM_gal/r²; build early/late RAR; compute the split significance (χ² over bins).
4. **Gate:** our split within ~1.5× of 6σ → proceed to the systematics battery; else waterfall-diff.
5. a₀-insensitivity check (1.2e-10 vs 9.36e-11) as in the WB note.

## Status
Lens catalogs down + verified (1.24M galaxies, matches Brouwer ~1M). Shear catalog (16 GB) downloading in background. Lens-side
pipeline is the immediate next build; the ESD stack + gate follow shear completion. **No significance computed yet — gate pending data.**
