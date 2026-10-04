# CFG327 FROZEN CRITERIA: are the MW ultra-faint dwarfs' offsets from the law tidal? (McGaugh & Wolf 2010-type test)

**Lane:** orchestrator; the owner said "yeah run the tidal test boss".
**Hypothesis (framework-favourable):** the UFD offset (+0.32 dex, AUDIT_UFD) is driven by tides, not by the law. If so, the offset should grow with tidal susceptibility, and the least susceptible dwarfs should sit on the law.

## Inputs (all on disk; no downloads)
- **Data:** `real_research/data/dsph/lvd_dwarf_mw.csv`, with the same cut and estimator as AUDIT_UFD.
  - Cut: M_V > −7.7.
  - Estimator: Υ_V = 2 plus 1.33 M_HI; σ² = g r/3 at r = (4/3) r_half with half the mass; g = ν(g_N/a₀) g_N, exponential kernel (equal to ν_mono to 5e-9 at these accelerations).
  - Footings: canonical 9.3603e-11 and alt 1.1312e-10.
  - Per-dwarf offset: Δ = log10(σ_obs/σ_pred). Only the 31 resolved dispersions are used; the 9 upper limits are reported but not used in the correlation.
- **Milky Way potential (framework-native):** the MOND field of the MW's baryons. A point mass of 6e10 M☉ (the record's value) with g = ν(g_N/a₀) g_N, spherical.
- **Orbits:**
  - Initial conditions from ra, dec, distance modulus, vlos_systemic, pmra and pmdec, through astropy Galactocentric at its defaults.
  - Leapfrog integration back 6 Gyr, dt = 0.5 Myr; the pericentre r_p is the minimum.
  - Dwarfs missing proper motions are dropped from metric A and reported.

## Metrics (larger = more tidally susceptible)
- **A (primary):** r_half / r_t(r_p), with r_t(r) = r [M_d,eff / (3 M_MW,eff(r))]^(1/3).
  - M_eff = g r²/G: the dwarf's from its own predicted law field at (4/3) r_half; the MW's from its MOND field at r.
  - No observed σ enters the metric, which keeps it independent of Δ.
- **B (secondary):** the same with r = present Galactocentric distance (no orbit needed).

## Tests (canonical and alt, each separately; never pooled)
- **T1, correlation:** Spearman ρ(Δ, log metric A) > 0 with one-sided p < 0.01.
- **T2, low-susceptibility subset:** the median Δ of the least susceptible third (metric A) is within 2σ of zero (bootstrap error plus the AUDIT_UFD Υ floor of 0.077 dex).

## Decision
- **TIDES EXPLAIN:** T1 and T2 pass on both footings.
- **PARTIAL:** T1 passes, but T2 fails (the least susceptible dwarfs still sit above the law).
- **NOT SUPPORTED:** T1 fails.

Metric B and the "drop the LMC-hosted" and "drop orbits with r_p < 10 kpc" splits are reported only.

## Controls
- **C1:** the offsets reproduce AUDIT_UFD's Kaplan–Meier median (+0.3245 canonical) to 0.005 dex using the measured-plus-limits set, or the measured-only median is printed against the audit's measured-only row.
- **C2:** the orbit integrator conserves energy to better than 1e-4 over 6 Gyr.
- **C3:** a circular orbit at 50 kpc keeps r_p within 1%.
- **MUTATE** (CFG327_MUTATE=1, separate outputs): metric A is shuffled across dwarfs (seed 327); T1 must fail.

## Pre-freeze disclosure
- AUDIT_UFD's distance split (beyond 80 kpc: +0.325) and its recalled disturbed-system cut were known and did not help.
- No pericentre or metric value had been computed.
