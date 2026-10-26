# Actual stellar chronology: source checks, not inputs fitted into CCT021

Primary versions checked on2026-10-25. These contextual results do not alter the running initial conditions, source, birth rule, mass supply or acceptance criteria.

- [Aparicio, Carrera & Martinez-Delgado (2001), astro-ph/0108159v1](https://arxiv.org/abs/astro-ph/0108159v1), abstract: wide-field Draco photometry indicates a predominantly old population, with most formation earlier than about10Gyr lookback. That is not a precise first-star timestamp.
- [Bettinelli et al. (2018), arXiv:1801.08145v1](https://arxiv.org/abs/1801.08145v1), abstract: an inner-core Sextans photometric reconstruction finds a short main burst, about0.6Gyr, ending within roughly1.3Gyr of the Big Bang. The restricted radial coverage must not be treated as a measured global history of an extended envelope.
- [Piatti (2026), arXiv:2606.23216v1](https://arxiv.org/html/2606.23216v1), sectionsIII–V: wider DECam reconstruction proposes different core/ring/outer histories and a merger near13Gyr lookback. Its core half-mass age is12.95(+.92/−.78)Gyr. The author explicitly calls the merger/abundance interpretation plausible pending spectroscopy, and CMD metallicities model dependent. It is a candidate assembly history, not a uniquely established merger chronology.
- [Yang et al. (2026), arXiv:2610.26375v1](https://arxiv.org/html/2610.26375v1), sectionsIV.1–IV.4: a DESI-based Draco chemical model finds low SFE and baryonic wind loading around172–260. SectionIV.3 assumes the14Gyr-lookback onset; it does not measure that onset independently. Chemical-model gas outflow and the field kinetic coefficient are different quantities.

## Consequences for this test

For each stellar component a necessary chronology is

    cosmic_collapse_start + simulated_time_to_settle < cosmic_first_star_time.

CCT021 has no cosmological collapse-start epoch or dynamical gas-to-stars model. Neither a CMD half-mass age nor an assumed age-grid onset supplies that missing clock. Delaying passive stars numerically is not evidence that real stars waited. If a spatial merger reconstruction is adopted, pre-existing core stars must be carried through later envelope assembly; one simultaneous whole-galaxy birth may be inadequate. That is a next hypothesis requiring data/stellar dynamics, not a retrospective rescue of this run.

Failed implication preserved: a baryonic wind-loading estimate near200 does **not** validate the old hypothetical cold reservoir proportional to5.364*200*formed stellar mass. It neither measures cold-field capture nor derives a conversion efficiency, universal cosmological ratio bridge, or conserved energy/mass transport law. Do not use that numerical resemblance as a cold-mass detection or an independent prior on these runs.

The observation-derived chronology and model assumptions must be propagated with radial selection and uncertainties before any pre-stellar formation claim. No cosmological age relation from another gravity theory is silently imported here.
