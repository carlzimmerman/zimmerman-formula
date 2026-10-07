# CFG392: old tidal-dwarf candidates by gas metallicity, against the RAR

## Verdict: NON-DISCRIMINATING (no galaxy qualifies as a candidate)

| run | footing | N matched | N flagged (>= 0.40 dex) | Delta | verdict |
|---|---|---|---|---|---|
| primary (frozen rules) | canonical 9.3603e-11 | 26 | 0 | — | NON-DISCRIMINATING |
| primary (frozen rules) | alt 1.1312e-10 | 26 | 0 | — | NON-DISCRIMINATING |
| alias-fix (post-freeze, D2) | canonical | 27 | 0 | — | NON-DISCRIMINATING |
| alias-fix (post-freeze, D2) | alt | 27 | 0 | — | NON-DISCRIMINATING |

- 26 SPARC dwarfs have gas-phase O/H in the four compilations: 89 pass the cuts (Q < 3, Inc >= 30, M_b < 1e10 Msun).
- The own-sample mass-metallicity relation (MZR) is 12+log(O/H) = 6.278 + 0.205 log M* (slope ± 0.045), with
  M* = 0.5 L36. Its scatter is 0.183 dex.
- No galaxy sits >= 0.40 dex above the MZR, so the frozen rule (N_flagged < 5) gives NON-DISCRIMINATING. This holds
  on both footings, for both kernels and for both point selections.
- Secondary threshold (>= 0.30 dex): one galaxy, DDO 168 (MZR residual +0.388; O/H 8.30 from the LITTLE THINGS
  compilation).
  - At g_bar < 10^-10.5, its RAR residual (nu_mono) is −0.082 (canonical) and −0.117 (alt).
  - Settling would put it at −0.58 / −0.62.
  - So it is about 0.5 dex above the Newtonian expectation, and within 0.08 dex of the unflagged median.
  - This is one object. Its O/H comes from a single compilation (0.1-dex precision) that this lane did not cross-check.
    Under the frozen rules it counts for nothing. It is an anecdote, not a result.
- Confounder check: across all 26 galaxies, MZR residual and RAR residual are uncorrelated (Spearman ρ = −0.060,
  p = 0.77; alias-fix run −0.012, p = 0.95).

**What this means for the fork.** This lane does not decide between settling (an old TDG is Newtonian) and modified
gravity (it lies on the RAR):
- No SPARC dwarf with a measured abundance is metal-rich enough to be an old-TDG candidate at the frozen threshold.
- The one marginal object is not Newtonian. That leans the same way as the VPOS full-mass-excess result, but it is a
  single object at an unverified threshold.
- The record's young-TDG result (CFG7 FG041: Newtonian, but less than one orbit old) is unchanged.
- The metallicity proxy cannot find old TDGs in SPARC at this sample size. A decisive test needs objects with
  independent evidence of tidal origin, such as old TDG candidates with HI kinematics.

Standing: κ = ½ is FITTED. Both footings run throughout. No dark-matter particle is added; the framework's cold-fluid
mass is still required wherever the law needs it. Nothing here says the data favour the framework over ΛCDM.

## What was run

- `FROZEN_CRITERIA.md` was committed alone first (cccb2275f), before any script, abundance value or result.
- `cfg392_tdg_metallicity.py` is the single script.
  - Primary run: `cfg392_tdg_metallicity.out` / `_results.json`.
  - MUTATE run: `*_MUTATE.out` / `*_results_MUTATE.json`.
  - Alias-fix run (`CFG392_ALIAS=1`): `*_aliasfix*`.
  - Match tables: `match_table.csv` and `match_table_aliasfix.csv`.
- Metallicity sources, one per galaxy, in priority order:
  1. Berg et al. 2012 direct abundances: tables 5 and 7 of the arXiv source, positions from its tables 1 and 6.
  2. van Zee & Haynes 2006 (J/ApJ/636/214), tables 1 and 6.
  3. Hunter et al. 2012 LITTLE THINGS (J/AJ/144/134), measured values only. The six '*' empirical (M_B-based)
     estimates are excluded.
  4. Pilyugin et al. 2014 (J/AJ/147/131), O/H at 0.4 R25.
- Galaxies matched per source: 10 Berg, 9 van Zee, 3 Hunter, 4 Pilyugin. Median MZR residual by source: −0.087,
  +0.024, −0.129, +0.076 dex. Inter-source offsets are below 0.25 dex, but they are not negligible next to a
  0.4-dex flag.
- Fetches are listed in `FETCH_LOG.md`, with URL, bytes and sha256.

## Controls (kept as they fell)

| control | result |
|---|---|
| C1 loader, footings (load-bearing) | PASS |
| C2 match audit (load-bearing) | PASS: 26 matches (27 in alias-fix), no duplicates or conflicts |
| C3 observed g_obs used (load-bearing) | PASS in the main runs |
| C4 sanity: median residual of the dwarfs | PASS (reported): +0.009 dex over 89 dwarfs |
| C5 power: Newtonian injection | **FAIL (reported)**: no flagged galaxy to inject |
| C5 extra: injection on the one 0.30-dex galaxy | Delta −0.577 ± 0.025, still NON-DISCRIMINATING (N < 5 rule) |
| **MUTATE** | **DID NOT BITE: rc = 0**. The frozen MUTATE replaces the flagged galaxies' g_obs with g_bar. With zero flagged galaxies it changes nothing: C3 passes and the verdict stays NON-DISCRIMINATING instead of the required SUPPORTED. Kept as it fell. The test has no power at N_flagged = 0, and the MUTATE shows exactly that. |

## Departures from the frozen criteria (disclosed)

- **D1. Matching used positions as well as names.** Galaxies were matched by normalized name OR by position within
  1′ of `real_research/data/sparc_positions_merged.json`. The frozen text said names plus a hand alias table.
  Positions replaced most of the hand table. Every match is printed with its separation.
- **D2. Alias-fix run, added after the primary results were seen.** The primary run missed two cross-identified
  galaxies:
  - DDO 154 is UGC 8024 in van Zee table 6, a higher-priority source than Hunter (7.67 instead of 7.50).
  - IC 2574 is UGC 5666 in Berg; it lies 1.59′ away, beyond the 1′ tolerance.
  - The alias-fix run uses the Hunter table's NED cross-IDs plus 10 hand groups, and a 2′ tolerance.
  - It adds IC 2574 and changes DDO 154's value. Nothing becomes flagged at 0.40 dex. Under the Theil-Sen MZR,
    DDO 168 reaches 0.40, but that alone is N = 1.
  - The primary run stays the frozen verdict. The alias-fix run is a sensitivity check only.
- **D3. Extra reported lines.** A Newtonian injection on the 0.30-dex flags was added after the first run. It is
  reported only.
- **D4. Output name.** The harness writes `*_results_MUTATE.json`, where the frozen text said `*_MUTATE_results.json`.
- Lee et al. 2006 was not added: it is not on VizieR, and no other compilation was fetched.

## Caveats

- Being metal-rich for one's mass is a weak proxy for tidal origin. Ordinary dwarfs can also be metal-rich:
  - low gas fraction or closed-box evolution;
  - the calibration offset between sources (Pilyugin's 0.4 R25 value against global direct abundances);
  - aperture effects (a single central HII region);
  - distance errors, which move both log M* and the RAR residual.
- A flagged set could therefore be ordinary galaxies. Equally, a real old TDG can look normal in metallicity if it
  formed from the outer, metal-poor gas of its host.
- The SPARC dwarfs with abundances are mostly gas-dominated (median f_gas 0.76), the regime where the RAR residual
  is least sensitive to Υ*.
- The MZR scatter (0.18 dex) makes a 0.4-dex outlier a 2.2σ event (one-sided p = 0.014, hand estimate from the scatter). With 26 galaxies, about 0.4 such outliers are
  expected even from a Gaussian, so a null in the count was likely before any physics enters.

## Owner items

1. A real old-TDG test needs candidates chosen by tidal origin, not by metallicity alone. Examples: TDG candidates
   in old merger remnants and the VPOS/plane members already in the record, which need HI rotation curves. This
   would need a new lane and a new fetch go.
2. If the metallicity route is worth continuing: a larger uniform direct-abundance compilation covering more SPARC
   dwarfs (for example a homogeneous Te-method compilation). Without it, N_flagged stays near 0–1.
3. DDO 168's O/H (8.30 in LITTLE THINGS) should be checked against the original reference before anyone quotes the
   marginal object.
