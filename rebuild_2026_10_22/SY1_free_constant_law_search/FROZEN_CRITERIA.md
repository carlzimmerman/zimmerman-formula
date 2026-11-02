# SY1_free_constant_law_search: FROZEN CRITERIA, committed alone before any script or number

Owner's go, 2026-11-02: find new law forms by brute force and symbolic regression. **Not blind:** BF1, UX3, LM1, GM1, KS1, SL1, RQ3 and DA1's criteria are read, including BF1's near-miss family. κ = ½ FITTED. No cold component, no particle. Reinstates nothing. Not theory closed. Nothing here says the data favour the framework. A hit here is a description of data, not a theory.

## Question
BF1 searches with no fitted float and three leaves, and it reports both as limits. Does a closed-form rule exist when up to two fitted constants and class-blind profile-shape leaves are allowed, and does it hold on data it never saw?

## Search
Genetic symbolic regression (PySR, on the Mac, all free cores, checkpointed and resumable), 8 seeds, complexity at most 30, over the same three wrappers as BF1 (W1 scale, W2 baryons, W3 boost). Two arms:
- **Arm T, typed:** dimensionless leaves only, at a₀ canonical: y = g_b/a₀, ell = r a₀/c², f = gas share of enclosed baryons, s = dlog g_b/dlog r, D = ρ_b(r)/ρ_DE. Constants 1, 2, ½, π free to use; **at most two fitted floats**, each counted and reported.
- **Arm Z, zero float:** same leaves, no fitted float. This extends BF1's grammar by s and D.

**Class-blind rule.** Every leaf is computed by the same formula on every system. No leaf states what class a system belongs to; temperature, a cluster flag, hot-gas share and any catalogue label are excluded, because UX3 found no measured switch separated from "not a cluster".

## Data
BF1's split, unchanged: train is odd SPARC names, Q < 3, inclination >= 30, Υ disc 0.5, bulge 0.7, plus X-COP at positions 0, 2, 4, 6, x <= 0.75. The loss weights the two classes equally, so SPARC's point count can't swamp clusters. Everything else is never seen by the search.

## Gates
BF1's, numerically unchanged. **Stage 1:** gate 1 X-COP train, gate 2 SPARC train. **Stage 2,** on the Pareto front's survivors, at most 200, cheap to dear: gate 3 even SPARC and other X-COP; gate 4 LITTLE THINGS; gate 5 SPARC on FG1's path. **Stage 3:** `RQ3_acceptance_v2`, unedited, all its rows, reported with its Bullet, Cassini and form-dependent rows. A floats' fit is frozen at train and never refit on a holdout. Both footings at Stage 2 and 3, never pooled.

## Controls, before the real run is read
- **Planted:** BF1's (1 + f) log1p(1/y), plus one planted form with two floats and an s term. Each must be recovered at noise-free and at SPARC's real errors.
- **Scrambled:** y shuffled within class. Same run length. Any Stage 1 count must be stated against it.
- **MUTATE:** gate 1 at 1e-6 must return nothing. Outputs named by mode.
If a planted form isn't recovered, the lane reads NO VERDICT for that arm: a null means nothing if the search can't find a known answer.

## Labels, per arm
**SURVIVOR** clears Stage 3's law-independent rows as RQ3 defines passing; **HOLDS OUT, FAILS ACCEPTANCE** clears Stage 2, not 3, naming rows; **X-COP AND DISCS ONLY**, gates 1-3; **TRAIN ONLY**, Stage 1 only; **NO HIT.** A null applies to this grammar, these leaves, this run length; it isn't a no-go theorem. Fitted floats are stated beside any label, and any float is reported with its value's nearest simple constant only as a note, never a claim.

## Run
Starts when BF1's `L4.done` exists, since the Mac's cores are in use until then. Preemptible: checkpoint on SIGTERM, resume. Yields to any 1024³ run. Checks disk, 30 GB gate only for large outputs; expected under 1 GB.
