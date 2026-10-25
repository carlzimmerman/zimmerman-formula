# Continue CCT-010

Read RESULT.md and analysis.json. The moving-frame experiment corrects an earlier stellar interpretation, but does not solve the mass/profile gap. New CCT candidate only; no bridge to literal v3 or retired SCT-M.

1. Inspect runs/draco_track_tracking.json and sextans equivalent: local well versus aperture COM/current, not material labels. Full potential multipoles are in *_tracking.npz.
2. Inspect *_stars_advected.json: passive full-potential cohorts versus rigidly advected initial fields, both timesteps. Draco's original static control remains *_stars.json. Do not call these live DF or survival tests.
3. Inspect *_momentum_momentum.json: explicit sink Pz ledger leaves residuals. M/E/Jz pass does not imply linear momentum conservation. The repeat states agree to <=4.81e-15.
4. Central masses about the evolved stars remain deficient. Sextans actual-position spherical survey diagnostic is 2DeltaNLL63.63 above its conditional reference; Draco global spherical sigma7.13 versus9.55 observed. F/Leo matched pulse controls are still open.
5. Next implement and validate translation/recoil plus a moving-core/live-star calculation with backreaction, then apply one independently paid assembly prescription to all four dwarfs. Do not tune each dwarf to its answer, reset wave occupations, or count gravity twice.

Reproduce from repo root, single numerical thread. Source-free parent pins are in each run JSON. Fresh tags required to preserve raw runs. `evolve.py` original tracker; `evolve_bounded.py` same algorithm with radial chunking of current diagnostics, used for Sextans. `evolve_momentum.py` repeats the field evolution with fast Pz/sink diagnostics. For exact existing commands see CONTRACT.md and each run's parameters; replace only --tag for a reproduction. `stars_advected.py TAG` reads the newly named tracking run. `analyze.py` intentionally uses the two canonical tags; copy/adapt to a new analysis output rather than overwriting this audit.

Final provenance audit command/manifest is in audit_001. It authenticates saved calculations and finite checks, not a fresh cold/star integration. Initial dynamics did not record UTC start/software fingerprints in their own JSONs; the audit observes the present environment and does not invent those historical observations.
