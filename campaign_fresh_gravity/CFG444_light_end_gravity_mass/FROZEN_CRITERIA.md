# CFG444 FROZEN CRITERIA: the light end of the wave-field window via holes with GRAVITY-class (dynamical) masses
(owner 10-06, swing CFG440-449: "light end via GRAVITY-mass hole"; committed before any table is compiled, any script is written, or any number is read off a paper)

**Question.** CFG394 (criteria 5aff6a7ba, result 66469e59b) left 2.01-4.35e-20 eV open and named the decider: a hole of 0.8-1.5e9 Msun with a ~10% (1 sigma) dynamical mass and a reflection spin whose lower edge is >= 0.9 under every soft-excess treatment. Does any hole with a precise dynamical mass in 3e8-3e9 Msun already have a published spin that excludes part of the light end under CFG367's code run unchanged? If not, which named AGN would decide it?

**Field, physics, exclusion rule.** Exactly CFG367's, as in CFG394 (free complex scalar; Detweiler x2, l = 1-3, 200 e-folds in 4.5e7 yr; 9-point log mass grid over CFG367's `mass_range`; m excluded only if excluded at every grid mass). Nothing is re-chosen.

**Code identity (C0).** `CFG367_superradiance_window/cfg367_superradiance.py` executed from its committed bytes, sha256 d78a38121a865094d8d333108533bd67e378f6c7aabc0ad6edcf74ae8bb0237e, with `__file__` pointed at a run directory inside this lane (CFG394's wrapper method). Hash mismatch stops the run.

**Compilation (S), all from paper tables/text (arXiv HTML/source, VizieR), matched by row position; WebFetch/WebSearch summaries are pointers only; every fetch logged in FETCH_LOG.md.**
- S1. Masses: (a) every AGN with a VLTI/GRAVITY (or GRAVITY+) BLR-interferometry mass, including joint spectroastrometry+reverberation (SARM) fits, 2018-2026; (b) other dynamical masses: H2O maser discs, stellar dynamics, resolved gas (ALMA/HST) dynamics.
- S2. Mass window 3e8 <= M <= 3e9 Msun (central value). Objects outside are listed with M and dropped.
- S3. Spins: ANY published spin 2010-2026 is recorded (reflection, thin-disc continuum/SED, jet, polarisation, EHT, other) with error and method. Only reflection (spin free) and thin-disc continuum/SED (spin free) can enter a run (CFG394 S3).

**Robustness rule (R), CFG394's, frozen here before compiling.**
- R1. Lower edge = lower end of the 90% interval or quoted lower limit; a 1-sigma interval converts as centre - 1.645 x sigma_lo; an upper limit sets floor 0.
- R2. LOWEST lower edge across all acceptable models in a paper and across all accepted papers on that object.
- R3. "Precise" mass: dynamical method (S1) and 1-sigma error <= 0.15 dex, taken as max(log(c+e_hi) - log c, log c - log(c-e_lo)). If a paper gives several models/methods, the statistical-plus-quoted-systematic error is used; if two dynamical masses disagree by more than their combined errors, the object is NOT precise (method dependence).
- TIER A (decides): precise mass AND R2 lower edge >= 0.5 from S3-accepted methods. Run with the paper's 1-sigma errors (asymmetric dex errors converted to linear about c).
- TIER B (indicative only): R2 edge >= 0.5 with a dynamical mass of 0.15-0.4 dex error, entered at its own errors.
- Others listed with the reason, not run.

**Runs.** CONTROL (CFG367's own CSV, byte-identical copy, sha256 6b3b1c49...d963, must reproduce CFG367's committed intervals exactly, as CFG394's C1); RUN_A (TIER A; decides); RUN_AB (indicative); MUTATE (CFG367_MUTATE=1 on RUN_AB list, or on the full compiled list if RUN_AB is empty, with every compiled object entered at its spin floor; union must be empty).
For every compiled object report alpha = 7.49e9 M m at 2.01e-20 and 4.35e-20 eV (central M and mass-range ends) and Omega_H at its R2 floor.

**Verdict (RUN_A, inside [2.01e-20, 4.35e-20] eV).** LIGHT END CLOSED (all excluded) / NARROWED (part; survivors reported) / STAYS OPEN (none).

**Decider list (deliverable if not CLOSED).**
- D1. Candidates: compiled objects with precise dynamical mass (R3) and 0.8e9 <= M <= 1.5e9; then, separately labelled, 3e8-3e9 objects with precise masses (wider band) and 0.8-1.5e9 objects with 0.15-0.3 dex dynamical masses.
- D2. Decider-grid value per candidate: CFG394's grid recomputed at the candidate's OWN central mass and OWN 1-sigma mass errors, with hypothetical spin floors a_lo in {0.7, 0.9, 0.98}: fraction of the light end excluded (200-point log grid in m), via CFG367's `mass_range`/`excluded`. Pairs: union fraction for every pair of candidates at a_lo = 0.98 and 0.9; pairs reaching >= 0.99 are named as closing pairs.
- D3. X-ray readiness: existing XMM-Newton and NuSTAR exposure (HEASARC master catalogues) and a 2-10 keV (or nearest band) flux from a catalogue (4XMM, eROSITA, Swift/BAT, Chandra, ROSAT, in that preference), recorded with source. "Lacks good spectra" = no NuSTAR pointing, or NuSTAR+XMM total < ~20,000 counts expected; stated per object.
- D4. Accretion-state flag: reflection spins need a radiatively efficient thin disc. Objects without broad lines / with L_bol/L_Edd < 1e-3 (LLAGN/RIAF) are flagged "reflection spin not expected" and ranked below every radiatively efficient candidate.
- D5. Rank: (i) D4 flag, (ii) decider value at a_lo = 0.98 (descending), (iii) 2-10 keV flux (descending).

**Controls.** C0 hash; C1 CFG394-style control reproduces CFG367 exactly; C2 CFG367's internal checks pass in every run; C3 CFG394's own decider row (M = 1.0e9, +/-10%, a >= 0.98) reproduced to the committed fraction; MUTATE empty.

**Departures** disclosed in README; failed controls kept. Outputs `.out` / `_results.json`, MUTATE `_MUTATE`.

**Scope.** Gravity-only; bounds where the field's mass can be, detects nothing. The cold-fluid amount stays free. kappa = 1/2 is fitted. No dark-matter particle species is claimed.
