# BF1_brute_force_law: FROZEN CRITERIA (committed alone, before any script or number)

Owner's go, 2026-11-02: exhaustive search on the Mac. Directory renamed from BF1_brute_force_law, which a gitignore rule hid. **Not blind:** LW1, LM1, GM1, FR1, FR3, SL1 and DR1 are on record and read. kappa = 1/2 FITTED. No cold component, no particle. This reopens no retired sector. Not theory closed. Nothing here says the data favour the framework. PAPER67 is unaffected by any result here.

## Question
Is there one closed-form rule, with no fitted number, built from local baryonic quantities, that lifts the a0 law on clusters and leaves discs alone, and that holds on data it never saw?

SL1 searched cold-sector operators. This searches modifications of the law itself, which nothing on the record has done exhaustively.

## Search space
Leaves per radius, from baryons only, at a0 canonical 9.3603e-11:
- y = g_b / a0
- ell = r a0 / c^2
- f = gas share of enclosed baryons, clipped to [0, 1]

Potential and density against dark energy are products and ratios of y and ell, so they're inside the grammar.

Constants: 1, 2, 1/2, pi. No other float. Unary: sqrt, log1p, 1/(1+x), square. Binary: + - * /.

Three wrappers, law(g, a) = g/2 + sqrt(g^2/4 + a g):
- W1 scale: g = law(g_b, a0 H)
- W2 baryons: g = law(g_b H, a0)
- W3 boost: g = law(g_b, a0) H

Levels: L0 is leaves and constants. L1 and L2 are unary and binary closures, deduplicated by value on the evaluation points, L2 capped at 150,000 by node count, then lexical order. L3 is every binary op on pairs from L2, streamed. H must be finite and positive on every point. Exhaustive within this; the cap is a real limit and gets reported.

## Data
- **Train:** odd positions of the 175 SPARC names, sorted, Q < 3, inclination >= 30, Upsilon disc 0.5, bulge 0.7; X-COP clusters at positions 0, 2, 4, 6 sorted, rows x <= 0.75, hydrostatic masses.
- **Never used in the search:** even SPARC names, the other X-COP clusters, LITTLE THINGS, 63 groups, the 15 cluster keys, Local Group classes, Milky Way, DiskMass, IC 1613.

## Gates
**Stage 1, train, in order.**
1. X-COP train: |mean log10(M_HSE / M_model)| <= 0.05, rms <= 0.10.
2. SPARC train: rms of log10(g_obs / g) <= 1.05 x the law's rms in the same statistic, |median| <= 0.03.

**Stage 2, holdouts run cheap to dear on Stage 1 survivors, ranked by nodes, at most 200.**
3. Even SPARC names, same statistic as gate 2. Other X-COP clusters, same as gate 1.
4. LITTLE THINGS: |median E| <= 0.10.
5. SPARC with FG1's own path: rms, median Upsilon in 0.50-0.80, tilt.
6. Groups, 15 keys, Local Group classes, IC 1613, Milky Way, DiskMass on FG1's lines. The harness for this stage is written after Stage 1 and before any survivor is graded on it, and named in an amendment committed first.

Reported, not a gate: Cassini at Saturn, on H evaluated there.

## Labels
- **SURVIVOR:** passes all of Stage 2. Not a theory: no action, no CMB, and it would still need outside reproduction and a derivation.
- **X-COP AND DISCS ONLY:** passes gates 1-3 and fails later.
- **TRAIN ONLY:** passes Stage 1 and fails gate 3.
- **NO HIT:** nothing passes Stage 1.

## Controls
- **Look-elsewhere control:** the same search with f and ell permuted across X-COP clusters. Survivor counts at each stage are reported beside the real ones. If the real count isn't clearly above the control's, that goes in the title.
- **Planted test,** before the real run: a mock built from a known H of L3 size must be recovered.
- **Known answer:** H = 1 must reproduce the law on X-COP, +0.467 on all seven at the cached rows' constants within 0.01, and fail gate 1.
- **MUTATE:** gate 1's line tightened to 1e-6 must return no survivors.

## Expectation, mine, on record
Stage 1 survivors exist: 90 %, since X-COP's large y-ell contrast with discs is easy to exploit. A rule passing gate 3: 50 %. SURVIVOR: 3 %. The likeliest result is rules that only say "clusters are big".

## Compute
Preemptible: checkpoint per chunk, SIGTERM saves and exits, rerun resumes. nice 15, leaving AR1's cores free.
