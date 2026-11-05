# External actions deferred to the owner

Kappa = 1/2 FITTED; not theory closed. No action listed here has been taken.

| Item | Source | Size | Why deferred |
|---|---|---|---|
| a0(z) proposal sample | M A7 / AT2; prospective ALMA multi-tracer sample | Not yet specified; proposal stage | Brief explicitly excludes running this; requires sample/time approval |
| Milky Way thick-share selection function | APOGEE selection products, FN4f | Unknown until exact product is selected | Download not authorized; raw counts alone do not identify the share |
| Local Group star counts | MAST PHATTER and VizieR products, FN4d | Unknown until products are resolved | Downloads not authorized |
| Publication, deposition, messages, or Git push | Any resulting artifacts | Determined only if requested | This goal authorizes local work and commits, not these external actions |
| Authenticated solar interior for lane5(d), AZ38 | [Official Model S distribution](https://phys.au.dk/~jcd/solar_models/), preferably corrected GONG model l5bi.d.15 with radius, density, pressure and thermodynamic variables | Unknown; data payload and transfer metadata not requested | No authenticated local profile found in the recorded filename inventory. The original GONG Ledoux discriminant has a documented correction. Download is outside this run's authorization. Model S is a stellar-model reference, not raw observations; any transfer to a framework-native interior calculation must retain that provenance and its assumptions. |


| IC1613 robust-weighted moment0 for AZ46 flux provenance | [NRAO IC1613 HI directory](https://things.cv.nrao.edu/littlethings/ic1613/HI/), named IC1613_R_X0_P_R.FITS | Directory lists16M; exact byte count not requested | The local natural map differs from the published robust-weighted mass. The robust cube is local, but its archived moment map/mask is not. Download deferred; no new physical label rests on assuming the maps are identical. |
| IC1613 published bulk velocity field and numerical gas/dispersion profiles used by Oh2015 | [Oh2015 sectionsIII.1–III.2](https://arxiv.org/html/1502.01281); exact machine-readable product/source not yet identified | Unknown | Needed to reproduce the paper's16.9km/s corrected curve and trace the5.93e7Msun gas table to its profile integral. Intensity-weighted moment maps are not equivalent. Any download or author contact is deferred. |

| SLACS per-lens resolved rotation for AZ48 / FA1 I2 | Required: aperture-defined V/sigma and uncertainties, or authenticated rotation classifications with the original measurement definition, for CFG713's43 lenses. Local Auger2009/2010 and Etherington2022 text/table inventory is recorded in AZ48_fa1_completion/input_audit.json; a supplying data release/publication has not yet been authenticated. | Unknown until an exact product is selected | The inspected catalogue provides dispersions and morphology, not rotation. The I2 threshold V/sigma<=0.5 cannot be inferred from those fields, or automatically from a generic fast/slow flag. Acquisition or author contact is deferred. The bounded search does not exclude an uninspected existing local product. |

| Native radial gas reconstruction for AZ48 I1/I2 shear keys | eROSITA/eRASS1 cluster X-ray radial surface-brightness or emission-measure products, angular apertures, response/temperature/abundance calibration and uncertainties matched to the local cluster roster; exact supplying product not yet authenticated. Existing erass1cl_primary_v3.2.fits schema and F1/X2/X30 source chain are recorded in AZ48_fa1_completion/shear_inputs.json. | Unknown; depends on profile products versus event-level reconstruction | The audited chain supplies catalogue-derived MGAS500/R500 and an assumed radial shape, not the raw/native reconstruction required by this goal. Download or archive acquisition is deferred; no claim is made that every possible local source has been exhausted. |
| Per-cluster mean-flow constraints for AZ48 I2 shear keys | Resolved gas/galaxy velocity information or aperture-defined rotation-support measurements for the shear cluster roster; publication/release to authenticate | Unknown | Temperature and a projected velocity gradient alone do not identify vorticity. No measured per-system mean-flow field is supplied by the audited chain. Any new acquisition or author contact is deferred. |

Add exact products, links and sizes if a lane discovers them; never invent
sizes or treat elapsed time as permission. Approved dated ALMA release scoring
is governed separately by the existing written approval and the goal brief.
