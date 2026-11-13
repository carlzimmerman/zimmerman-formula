# Paused before any numerical run

The user paused research on 2026-11-13 and requested a commit/push plus Claude handoff. This directory contains **unexecuted draft work, not a velocity-dispersion measurement**. No contract, run directory, numerical result, manifest, plot, or test result has yet been generated. Do not cite the draft as evidence. No live tool session or numerical job was launched by this task. A final process-list query was denied by the sandbox; this is not a global claim about other agents' processes.

## Files preserved

- `fit_dispersion.py`: newly written, unexecuted native-pixel forward-model draft. No syntax check or benchmark has been run. It must be reviewed before execution.
- `inputs/desispec_resolution.py` and `.provenance.json`: official DESI resolution implementation, URL, retrieval metadata, byte count and SHA-256.
- `inputs/ppxf_template_readme.md` and `.provenance.json`: official pPXF template provenance.
- `inputs/ppxf_population_sdss.ipynb` and `.provenance.json`: official pPXF example explicitly identifying SDSS vacuum versus MILES air wavelengths.

The three downloads completed. The failed preliminary shell invocation `/ private/tmp/...` was a typo after successful directory creation; it launched no Python process and modified no inputs.

## Scientific motivation and available inputs

L017819 / SDSS J1524+4409 has secure lens/source redshifts approximately 0.320/1.210. Guo et al. 2026 reports new DESI stellar dispersion 222.26 ± 15 km/s. Parent-agent target-specific FastSpec checks report v2.1 317.619 ± 25.811 and v3.0 284.418 ± 33.142 km/s. These use the same photons and are not independent measurements or independent significance tests. The disagreement motivates a transparent instrumental-resolution and quasar-contamination audit; no complete uncertainty of 15 km/s has been validated here.

Raw inputs are finalized in sibling `desi_spectrum/`: `target_coadd.npz`, `target_coadd_derived.fits`, `validation.json`, raw HTTP ranges and extraction provenance. TARGETID 39633153882587315, coadd row 141, redrock z=0.3202209572, ZWARN=0. Native B/R/Z wavelengths have 0.8 Å pixels. Resolution arrays are `(1,11,nwave)` in **scipy DIA storage**, with offsets `[5,4,3,2,1,0,-1,-2,-3,-4,-5]`. Some entries are negative and must be preserved. Do not transpose or normalize them without a documented control. The parent 124 MB coadd was not downloaded in full; extracted ranges and derived-file consistency were validated by another agent.

Local E-MILES templates: `_external_data/lam2_templates_2026_11_03/spectra_emiles_9.0.npz`, 25 ages × 6 metallicities, 0.9 Å native sampling, optical FWHM 2.51 Å over the proposed fit windows. Prior provenance records SHA-256 `6a1b1a70db4d95f67afe0adbe254f111eb2b50412b9f311714c54ffba18c6f0e`, and official pPXF README identifies Padova/Salpeter E-MILES. They are kinematic nuisance templates here, not a new population-mass inference.

A quick read-only feasibility calculation gave median native pixel S/N approximately 6.46 in B and 10.32 in R over positive-IVAR, zero-mask pixels between observed 5000 and 7300 Å. The draft proposes blue Ca H/K + G-band and red Mg/Fe absorption windows, allowing smooth additive continuum and masking the broad source Mg II region. That is an approximation to quasar contamination, not a physical quasar/Fe II model.

The fiber center is offset 0.2980 arcsec from the Euclid catalogue coordinate (east +0.29638, north −0.03110); the actual fitted galaxy-light center may differ. No aperture correction or Jeans inference is performed by this draft. Do not assume an exactly centered 0.75 arcsec radius aperture.

## Next steps only after research resumes

1. Review the draft before freezing inputs. In particular, `benchmarks()` currently contains a **placeholder/incorrect diagnostic expression** for `template_air_to_vac_offset_kms`: it algebraically reports a constant based on 1.00028 instead of the actual wavelength-dependent conversion. Replace that diagnostic with an evaluation at declared air wavelengths. It does not feed the forward model, but must not be reported as a measurement. Also reconcile the profile velocity bounds (±220 km/s) with the optimizer bounds (±300 km/s), or explicitly justify the narrower profiling domain. These issues were noticed before pause and intentionally left unfixed.
2. Independently inspect the local Gaussian variance subtraction used to account for intrinsic template FWHM before applying the actual DESI resolution operator. It is a slowly varying wavelength approximation, not an exact deconvolution. Validate its analytic-line tests, sampling sensitivity, resolution orientation, array indexing and operator edges before interpreting any spectrum fit.
3. Write a computation-audit contract with exact input closure and software versions. Use the installed bounded v2 runner, initially with a roughly 300 s cap and one numerical thread. No reproduction command exists yet because no experiment has been frozen or executed.
4. Run the proposed finite tests: exact official-DESI versus independent diagonal indexing, analytic Gaussian lines, planted-mixture recovery, then conditional fits with blue/red/both windows, polynomial-degree and old-template controls, and a sampling control. Preserve failures rather than editing live or hashed inputs.
5. Report profile curves, control spread, residual plots and all limitations. Do not adopt a single conditional profile interval as complete stellar-dispersion uncertainty, and do not use differences from Guo/FastSpec as independent-dataset significances.

The available venv is `/private/tmp/forj0332-fit-venv/bin/python`; NumPy 1.26.4, SciPy 1.13.1, Astropy 6.0.1, Matplotlib 3.9.4 were available. Neither pPXF nor desispec was installed there at the last inspection. The draft imports the cached official DESI constructor for its benchmark, not an installed desispec package.

## Earlier completed independent task

`../../external_spectroscopic_matches/other_candidate_audit/README.md` contains the completed and bounded three-candidate SILO audit; `run_01/manifest.json` was completed and validated against 91 inputs. L015442 has the strongest alternative multi-line source evidence (O II S/N 8.93, O III 5007 S/N 6.10) but remains a candidate with disk-like imaging, no accepted Euclid mass model, and no new joint test. L001244 and L013442 have weaker source confirmation and rejected/undecided model status. This completed evidence is separate from the unexecuted L017819 draft.
