# Input and assumption ledger

| Ingredient | Classification | Treatment |
|---|---|---|
| Published Chandra kT | RAW measurement with SURVEY-CALIBRATION | Spectral fit, plasma and abundance model, absorption and backgrounds retained; not a virial temperature. Source Babyk2018 Tables1–2. |
| beta/core density fits | SURVEY-CALIBRATION | Projected surface-brightness fit; HSE requires spherical geometry, single beta and isothermality. Poor fit statistics disclosed; no universal profile claim. Babyk2018 Table3/section4. |
| Distance/5Re aperture | SURVEY-CALIBRATION | Published distance recorded; radius/core rescaled by SLUGGS/source DA. Distance errors not absorbed into formal kT error. |
| GC velocities | RAW with instrument errors | Existing Forbes2017 source tables are read again by inherited loader; no published inferred halo mass used as observation. |
| GC tracer density/anisotropy | SURVEY-CALIBRATION / externally calibrated dynamics | Existing CFG528b tracer profiles retained. M87 and5846 anisotropy is literature model-derived;4365/4374 isotropy is assumed. This limits independent interpretation. |
| Hydrostatic formula | Equilibrium inference, not FRAMEWORK-NATIVE derivation | Total gravitational acceleration, so do not add stellar gravity again. mu=.62 from source, not a fit. |
| Canonical/alt a0 | FRAMEWORK-NATIVE | Separate inherited baseline checks. New HSE force itself contains no a0. kappa=.5 fitted. |
| CLoGS kT/morphology | RAW measurement with SURVEY-CALIBRATION | Thermal spectral temperature and extent flags retained; galaxy-scale halos are not group-scale detections. |
| CLoGS R500/M500 | Externally calibrated scaling | Sun2009-scaled quantities explicitly excluded from new candidate admission and force diagnostic. |
| KT membership/sigma | SURVEY-CALIBRATION | Existing optical catalogue associations only; no new membership fit. Position/redshift thresholds stated before crossmatch. |
| HG flag | Survey selection | No selected eRASS source match. It is not a thermodynamic absence test; NGC4261 supplies an explicit counterexample. |
| HG stellar masses/radius | SURVEY-CALIBRATION | Stored HG rows quoted; no K-band mass or radius recalibration, gas profile or D recomputation claimed. |
| IC1613 stellar inclination | SURVEY-CALIBRATION / equilibrium inference | Different stellar populations, same potential/inclination; asymmetric drift and intrinsic shape assumptions. General method imports HI core radius. |
| IC1613 speed scaling | Conditional numerical bound | Total published speed already pressure corrected; whole-speed scaling is optimistic. No new Z or likelihood grade. |
| Standard MOND/NFW machinery | None introduced | No EFE, NFW halo prior, concentration relation or MOND shortcut used in new diagnostics. Old K0 reproduction is only a machinery check. |

No new fitted parameter was added. The thermal/shared-potential construction is a hypothesis, not an action or a derivation of the cold sector. A mixture of positive and negative conditional residuals is not evidence that the framework is preferred.
