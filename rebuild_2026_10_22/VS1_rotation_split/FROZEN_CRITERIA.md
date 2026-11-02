# VS1_rotation_split: FROZEN CRITERIA, committed alone before this lane's script or statistic

Owner's go, 2026-11-02: test discs against pressure-supported systems at fixed mass. This reads the retired cold sector's question for one test, and reinstates nothing unless the owner says so. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** I have seen the audit's offsets for NGC 1023, 4365, 4374, 4486, 5846, where the slow rotators sit high. `argon_clues/rotator_test.py` and its frozen files exist. Its numeric outcome is not read. I know mass is the confound and UX3 found no separating switch.

**Bug fixed.** The older script maps names to digits, so NGC 4486A overwrites NGC 4486, labelling M87 fast. M87 is lambda_Re 0.021, slow. This lane matches exact names. The old mapping is rerun as a reported row.

## Question
At fixed mass, does the law's excess follow rotation support?

## Data, all on disk
- Offsets: CFG323 `per_galaxy[footing][NGC]["primary"]`, nu_mono, measured tracers.
- Mass: CFG330 K0 `lMjamlaw`.
- Class: Emsellem+11 table B1, F/S at Re, lamRe. Gives 4 slow (4365, 4374, 4486, 5846), 12 fast.
- Discs: SPARC rotmod, Q < 3, inclination >= 30, Upsilon disc 0.5, bulge 0.7, law g_N = g^2/(g+a0) in closed form, offset = mean log(g_obs/g_law) over the outer half of points, for log M_b >= 10.7.

## Statistic and rule, from `argon_clues/FROZEN_rotator_test.md`, unchanged
D = mean(off slow) - mean(off fast); one-sided permutation p, 1e5 shuffles, fixed seed; OLS off on lMjamlaw + slow.
- **ROTATION SPLIT PASSES:** D >= 0.15, p < 0.05, slow coefficient >= 0.10 at > 2 sigma, on both footings.
- **KILLED:** D <= 0.05, or coefficient within 1 sigma of 0, on either footing.
- **NOT SEPARATED:** anything else.

## Reported, not graded
Mass-matched difference, |dlogM| < 0.25. Spearman offset vs lamRe, raw and with mass regressed out. Same with centrals removed. Old label mapping. SPARC disc arm: mean offset, n, disc minus slow, disc minus fast, noting the kernel and estimator differ from SLUGGS's. Fast mean itself, since the idea needs fast near 0.

## Limits stated now
n = 16, GC tracers, an offset is not a ZN4 halo, this doesn't test the halo's size or its failing shear keys. A pass supports a kinematic correlate, not a mechanism. Stated expectation: positive D, mass-confounded, NOT SEPARATED.

MUTATE: labels shuffled within mass terciles, D must fall toward 0; separate outputs.
