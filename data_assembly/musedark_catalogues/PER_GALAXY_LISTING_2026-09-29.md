# MUSE-DARK per-galaxy folders: what the site lists (data front, 2026-09-29)

Read on the owner's go ("read the per-galaxy folder listing"). **Only directory listings (h5ai index pages) of one galaxy, ID0003, were read; no file was fetched apart from HEAD requests for five sizes.** URL pattern: `https://dark-matter.osu-lyon.fr/data/ID<nnnn>/<folder>/` (the site's main page links the same ten folders for each of the 126 galaxies; the page's 1,907 links are consistent with that). Last-modified on the files is 2025-12-01. Everything below is for ID0003 and is assumed, not verified, to hold for the other galaxies.

| folder | files listed (size) | numeric table? |
|---|---|---|
| `RC_decomp/` | `RC_decomp_3.png` (138 KB) | **no**: a plot only |
| `RC_obs/` | `RC_URC_3.png` (77 KB) | no: a plot only |
| `residuals_decomp/`, `residuals_RC/` | `residuals_3.png` (189 KB), `residuals_URC_3.png` (33 KB) | no |
| `DM_density/` | `dm_density_3.png` (211 KB) | no |
| `mass_maps/` | `mass_3.fits` (331 KB), `mass_3.png` | FITS map |
| `input_cube/` | `cube_3.fits` (144 KB) | the MUSE cube cutout |
| `line_maps/`, `morpho_kin/` | `3_flux.png` (339 KB), `morpho_kin_3.png` (1,235 KB) | plots |
| `galpak_run_DC14/` (about 38 files) | text: `DC14_3_galaxy_parameters.txt` (921 B), `DC14_3_galaxy_parameters.dat` (1,530 B), `DC14_3_derived_parameters.txt` (1,300 B), `DC14_3_derived_parameters.dat` (2,215 B), `DC14_3_instrument.txt` (414 B), `DC14_3_run_parameters.txt` (~3 KB), `DC14_3_model.txt`, `DC14_3_stats.dat`, `DC14_3_galaxy_parameters_convergence.dat`; MCMC chain `DC14_3_chain.dat` (1,893 KB); FITS: `3Dkernel`, `convolved_cube`, `deconvolved_cube`, `residuals_cube`, `obs_{vel,disp,flux}_map`, `true_disp_map` (8–132 KB each); plots and PDFs incl. `DC14_3_rotcurve.pdf` (49 KB) / `.png`, `AMprofile.pdf/.png`, `corner_*`, `mcmc`, `geweke`, `images`, `obs_maps` | **yes**: the galaxy-parameter and derived-parameter text files are small tables (contents not read) |

## What this means for the three deciding items
- **Numeric rotation-curve tables: not listed.** The observed and decomposed rotation curves appear only as PNGs (`RC_decomp_3.png`, `RC_URC_3.png`); the GalPaK3D folder has `DC14_3_rotcurve.pdf`/`.png` (a plot, possibly vector in the PDF; not checked). So per-galaxy a_bar(r) and a_tot(r) as numbers are not offered; they would need digitising from a plot, or come from the parameters through the paper's model.
- **The disc–halo fit's stellar and gas masses:** likely in `DC14_<id>_galaxy_parameters.txt/.dat` and `DC14_<id>_derived_parameters.txt/.dat` (the fitted parameters and derived quantities of the DC14 GalPaK3D run), but I have not read their contents, so this is unconfirmed.
- Size if fetched: for ID0003 the four parameter files total about 6 KB (921 + 1,530 + 1,300 + 2,215 B); for all 126 galaxies about 0.75 MB if the others are similar; plus `run_parameters.txt` (3 KB each) if wanted, about 0.4 MB more. The chain (about 1.9 MB per galaxy, ~240 MB in all) and the FITS/PNG files are not needed for the masses.

## Options (each needs the owner's go; names and sizes stated)
1. Pilot: the five small text files of ID0003 only (about 6 KB): `DC14_3_galaxy_parameters.txt/.dat`, `DC14_3_derived_parameters.txt/.dat`, `DC14_3_run_parameters.txt`, to see whether they hold M_disk, M_gas and halo parameters.
2. If they do: the same four to five files for all 126 galaxies (about 1 MB, ~630 small files).
3. Rotation curves: `DC14_<id>_rotcurve.pdf` (about 50 KB each, ~6 MB in all) for a vector-geometry read like the KURVS figures, if the PDFs are vector.
