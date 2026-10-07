# CFG394 FROZEN CRITERIA: black-hole spins near 1e9 Msun vs the light end of the wave-field window
(owner 10-06, LEDGER CFG390-399 reservation: "BH spins near 1e9 Msun"; committed before any table is compiled, any script is written, or any number is read off a paper)

**Question.** CFG367 (fdb071536, README 98319d4d8) left the light end of the cold-fluid wave field's mass window, 2.0-4.4e-20 eV, unexcluded. Do published spin measurements of supermassive holes with M ~ 3e8-3e9 Msun exclude any part of it under CFG367's exclusion code, run unchanged?

**Field and physics.** Exactly CFG367's (free complex scalar, no self-interaction; Detweiler x2 rates, l = 1-3, 200 e-folds, Salpeter tau = 4.5e7 yr). Nothing in the physics is re-chosen here.

**Code identity.** `cfg367_superradiance.py` is executed from its committed bytes (sha256 d78a38121a865094d8d333108533bd67e378f6c7aabc0ad6edcf74ae8bb0237e, as in HEAD at freeze). The wrapper reads the file, checks this hash, and runs it with `__file__` pointed at a run directory inside this lane, so it reads that directory's `bh_spins_reynolds2021.csv` and writes its outputs there. No line of it is edited. If the hash does not match, the run stops.

**Data selection (S).**
- S1. SMBH spin measurements published 2019-2026 (refereed or arXiv), plus Reynolds 2021 Table 1 as the base.
- S2. Central mass 3e8 <= M <= 3e9 Msun (as stated by the spin paper or the mass reference it uses).
- S3. Methods accepted: X-ray reflection (relativistic line / reflection continuum fitted with spin free), or thin-disc continuum / SED fitting of the big blue bump with spin free. Jet-power, radiative-efficiency-only, or polarisation-only spins are recorded but not used.
- S4. Every number is taken from the paper's own table or text (arXiv HTML/source, VizieR), matched by row position; WebFetch summaries are provisional pointers only. Every fetch is logged in FETCH_LOG.md.

**Robust spin (R), decided per object before the run.**
- R1. Spin lower edge = the lower edge of the paper's 90% interval, or the quoted lower limit. If only a 1-sigma interval is given, the lower edge is centre - 1.645 x (lower 1-sigma error).
- R2. If the paper reports more than one acceptable model (e.g. different density, emissivity, disc-size or data-set choices), the LOWEST lower edge among them is used. If different papers report the same object in 2019-2026, the lowest lower edge among the accepted papers is used.
- R3. Robust requires lower edge >= 0.5 AND a mass with stated 1-sigma errors from reverberation mapping or a dynamical method (gas, stellar, maser). This is TIER A.
- R4. TIER B (indicative, never decides the verdict): lower edge >= 0.5 with a single-epoch virial, approximate ("~"), or otherwise uncalibrated mass. Such masses enter the CSV as 1-sigma = 0.4 dex (err_lo = c(1 - 10^-0.4), err_hi = c(10^0.4 - 1), approx = 0), which CFG367's mass_range turns into [0.3c, 4.0c].
- R5. Objects failing R3/R4 are listed with the reason and not run.
- R6. TIER A masses keep the paper's 1-sigma errors; CFG367's mass_range applies +/-2 sigma floored at 0.3c. Asymmetric dex errors are converted to linear about the central value.

**Exclusion rule.** CFG367's, unchanged: m is excluded by a hole if, for every M on a 9-point log grid over its mass range, some l in {1,2,3} reaches 200 e-folds in tau.

**Runs.**
- RUN_A: TIER A objects only (decides the verdict).
- RUN_AB: TIER A + TIER B (indicative).
- RUN_COMB: CFG367's Reynolds rows with any object re-measured in 2019-2026 replaced by its R2 row, plus all new TIER A rows (reported; a superseding lower spin replaces, never adds to, the old one).

**Verdict (on RUN_A, inside 2.0e-20 to 4.4e-20 eV; edges as CFG367's surviving interval [2.01e-20, 4.35e-20]).**
- LIGHT END CLOSED: the whole interval is excluded.
- NARROWED: part is excluded; the surviving sub-interval(s) are reported.
- STAYS OPEN: none is excluded. Then report the alpha values the nearest objects reach and the specific measurement (mass, spin floor, mass precision) that would decide it.
- The same is reported, labelled indicative, for RUN_AB and RUN_COMB.

**Controls.**
- C0: the hash check above.
- C1: CFG367's own CSV, copied byte-identically (sha256 6b3b1c49...d963), run through the wrapper, reproduces CFG367's committed `cfg367_superradiance_results.json` intervals exactly (smbh, xrb, primary, primary+secondary).
- C2: CFG367's internal checks (its C1, C2) pass in every run.
- **MUTATE** (CFG367_MUTATE=1, separate outputs under the run directory, `_MUTATE` suffix): all spins 0 on the RUN_AB list; the union must be empty.

**Departures** from this file are disclosed in README; failed controls are kept.

**Scope.** Gravity-only; bounds where the field's mass can be, detects nothing. The cold-fluid amount stays free. kappa = 1/2 is fitted. No dark-matter particle species is claimed.
