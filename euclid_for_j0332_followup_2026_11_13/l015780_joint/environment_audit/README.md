# L015780 observational environment audit

## Exact finite spectroscopy result

Scanned ALL456 METADATA rows in each cached DESI DR1 FastSpecFit v2.1 and v3.0 main/bright HEALPIX7582 file. Both complete tableHDUs have valid FITS CHECKSUM and DATASUM. TARGETID unique within each table; versions are reductions of the same objects, NOT912 independent spectra. Original official fetch URLs/hashes are in `../../l015780_inputs/fastspec_range_provenance.json`; bounded run hashes actual cached bytes before/after.

Within10arcmin of151.4073110655,+67.5075428182 there are23 rows, all GALAXY, ZWARN0, COADD_FIBERSTATUS0, DELTACHI2>25. This threshold is a transparent audit selection, not a declaration that every individual redshift has been visually validated. Excluding target leaves22 galaxies. No neighbor has |c(z−zl)/(1+zl)|≤1000km/s, zl=.428270373960303. Exactly one lies within3000km/s: TARGETID39633467440367290, RA151.1080771 DEC67.4057388, z=.42037158,552.1618arcsec(9.203arcmin) away, Δv=−1657.95km/s, DELTACHI2=47.410. This isolated distant projected/velocity neighbor does not establish group membership. Velocity-window values are diagnostics, not a binding criterion or halo-mass estimate.

No distinct spectral target within10arcsec; nearest other is124.4219arcsec away at z=.20371470. Therefore these actual main/bright spectra do NOT assign redshifts to the bright ≈3arcsec masked companions seen in the Euclid/HSC images. They cannot establish whether those are foreground, associated, or background. Do not treat absent DESI fibers as absent companions.

## Cheap public cluster cones

Queried10arcmin VizieR cones against WHL/WenHan2015 `J/ApJ/807/178` (returned metadata lists tables1,3,4, including updated WHL12) and redMaPPerDR8 `J/ApJS/224/1/cat_dr8`. Both responses identify the intended catalogue and contain no data rows. Raw responses and URL/SHA/time metadata retained in `catalog_fetch_provenance.json`. Primary data landing pages https://cdsarc.cds.unistra.fr/viz-bin/cat/J/ApJ/807/178 and https://cdsarc.cds.unistra.fr/viz-bin/cat/J/ApJS/224/1 . These are catalogue/footprint/depth-limited null cone results, not a null for all groups or all mass along the line of sight. No full rich-catalogue download was needed.

## Limitations and inference

Same-healpix main/bright metadata are not a spectroscopic completeness survey: other programs, adjacent pixels, fiber selection/collisions, faint objects and galaxies beyond10arcmin are not assessed. FastSpecFit versions cannot substitute for independent observations. No spectroscopically demonstrated group around the lens is established by this bounded data subset, but no robust upper bound on group mass or external convergence follows. External convergence remains UNMEASURED; neither setting it exactly zero nor assigning enough convergence to rescue a lens model is an observational result of this audit. Projected counts and a rich-cluster null are not kappa measurements. A calibrated environment/line-of-sight analysis would require broader galaxy photometry/redshifts, completeness modelling, halo-mass information and geometry.

Reproduction: `neighbors.py`, `contract.json`, `run_01/manifest.json`; completed v2 manifest validated against current inputs. CSVs retain ALL23 nearby rows in both reductions. No image or theory fit performed.
