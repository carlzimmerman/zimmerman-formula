# CFG470 FROZEN CRITERIA: a second hole for the light end, and the PG 1426+015 feasibility memo

Written and committed BEFORE any table is fetched or read for this lane, and before any script exists.

## Scope (standing rules)
- A gravity-only bound on where the wave field's mass can be (light end 2.01-4.35e-20 eV, CFG444's `LIGHT`). It detects nothing.
- kappa = 1/2 is FITTED. No dark-matter particle species is claimed; the cold-fluid amount stays free. The theory is not closed.
- All exclusion numbers come from CFG367's committed `cfg367_superradiance.py` (sha256 d78a38121a865094d8d333108533bd67e378f6c7aabc0ad6edcf74ae8bb0237e), executed from its bytes exactly as CFG394/CFG444 do (CFG444's `run` wrapper method, `__file__` pointed at this lane's `runs/<tag>/`). Nothing in CFG367/CFG394/CFG444 is edited or re-run in place.

## The decider function (frozen; identical to CFG444's `dmask`)
- `mg` = 200 log-spaced masses over LIGHT. For a hole with central M and symmetric 1-sigma fractional error e: row = {set smbh, mass_1e6 = M/1e6, err_lo = err_hi = e*M/1e6, approx 0}; `mass_range(row)` from CFG367; 9 log-spaced hole masses across that range; a field mass is excluded iff `excluded(m, M_i, a, TAU['smbh'])` is true for ALL 9.
- Single fraction f1(M, e, a) = mean of the mask. Pair fraction f2 = mean of (mask_A OR mask_B).
- PG 1426+015 enters at CFG444's central mass (vdB16 table 3, logM 8.96) with e = 0.10 unless a grid value is stated.

## Part A: second-hole search

### Sources (fetch order; real tables only)
1. BASS DR2 broad-line black-hole masses, Mejia-Restrepo et al. 2022, ApJS 261, 5 (VizieR).
2. BASS DR2 catalogue / overview tables, Koss et al. 2022, ApJS 261, 1 and 261, 2 (VizieR): positions, redshifts, BAT fluxes, bolometric/Eddington quantities, best M_BH where given.
3. Reverberation compilations: the van den Bosch 2016 table 3 already in CFG444/data (read-only), and the AGN Black Hole Mass Database (Bentz & Katz) if its table is fetchable as a real table.
If a source cannot be fetched as a table, that is recorded and the search proceeds on what was fetched; it is never filled from a WebFetch summary.

### Selection rules (all must hold)
- S1 mass: catalogue best M_BH in [1.1e9, 2.0e9] Msun. For BASS: Mejia-Restrepo's broad-Halpha mass (their preferred column) where present, else Koss+22's adopted M_BH. Recorded with its method.
- S2 redshift: z <= 0.31 and z > 0.
- S3 GRAVITY K band: at least one of Brgamma (2.1661 um) or Paalpha (1.8756 um) lands in 2.00-2.45 um at the object's z (equivalent to z <= 0.306). Paalpha landing in 2.00-2.06 um (z ~ 0.066-0.10, telluric band) is flagged, not cut.
- S4 VLTI sky: dec <= +30 deg.
- S5 accretion: Eddington ratio >= 0.01, from the catalogue's own value where given; otherwise L_bol = 8 x L(14-195 keV) (CFG444's estimator) over 1.26e38 M.
- S6 broad line: classified as a broad-line AGN (Sy1-1.9 or broad Halpha measured). Mejia-Restrepo rows satisfy this by construction.
- X-ray: every BASS object is a BAT detection; the BAT 14-195 keV flux is recorded and used only as a tie-break, never as a cut.
- Objects that fail S1 only because they sit in [0.8, 1.1e9) or (2.0, 3.0e9] are listed as NEAR MISSES (not ranked).

### Ranking metric (frozen)
- Primary: E98 = expected pair fraction f2(PG 1426 at e = 0.10, candidate at e = 0.10, a >= 0.98), averaged over the candidate's unknown true mass: log M_true ~ Normal(log M_cat, 0.30 dex), evaluated on 21 equally spaced points over +/- 2.5 sigma with normalized Gaussian weights. (The GRAVITY mass would land where the true mass is, not at the virial value.)
- Also reported (not used to rank): E90 (same at a >= 0.9), the central-mass pair fractions C98 / C90, the single-object fractions, and P(close) = Gaussian-weighted share of the 21 mass points where f2(a >= 0.98) >= 0.99.
- Ties (|dE98| < 0.005) broken by E90, then by BAT flux (higher first).
- Verdict words for A: CANDIDATE FOUND if at least one selected object has C98 >= 0.99 (a pair that could close the light end at its catalogue mass); PARTIAL if the best C98 is in [0.80, 0.99); NONE if no object passes S1-S6 or the best C98 < 0.80. The E98 value is quoted beside the verdict in every case.

## Part B: feasibility memo (PROPOSAL_MEMO.md)
- Mass precision: quote GRAVITY / GRAVITY+ achieved BLR-mass precisions on comparable targets from the papers themselves (read from arXiv text/LaTeX; WebFetch summaries are provisional and never a number source unless matched to the paper). The memo states which precision is the realistic one for PG 1426+015 and labels any extrapolation as an estimate.
- Spin exposure: scale from Walton et al. 2025's existing data (128 ks NuSTAR plus the XMM exposure they used) and their published constraints. Any scaling (e.g. statistical error ~ 1/sqrt(exposure)) is labelled an ESTIMATE, and the memo states plainly that the soft-excess model dependence is systematic and does not shrink with exposure.
- Exclusion grid computed by the committed script: f1 for PG 1426+015 and f2 for PG 1426 + the best part-A candidate, over e in {0.05, 0.10, 0.15, 0.20, 0.30} and a in {0.7, 0.9, 0.95, 0.98}. The memo quotes the cells matching the precision the literature supports.
- The memo is a file in the lane. Nothing is submitted, nobody is contacted.

## Controls
- K0: CFG367 code sha256 identical (else stop).
- K1: reproduce CFG444's PG 1426+015 route-B fractions 0.34 (a >= 0.9) and 0.56 (a >= 0.98) to 1e-12 against CFG444's committed results JSON.
- K2: reproduce CFG444's pair PG 1426+015 + Q2237+305 at a >= 0.98 (0.87) from CFG444's committed JSON, if the masses can be read from it.
- MUTATE (CFG470_MUTATE=1): all spins set to 0 -> every single and pair fraction must be 0. Detected -> the script exits 1; not detected (any non-zero fraction) -> exit 2. Outputs carry a _MUTATE suffix.

## Departures
Any change after this commit is disclosed in the README as a departure, with its effect.
