# KT11_compact_kernel_joint: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: push for a result from what was learned. κ = 1/2 FITTED and **held fixed here**: this tests a kernel, not κ. Footings never pooled. Not theory closed. No cold component, no particle. **Not blind:** p = 1's SPARC numbers at stated Upsilon (rho_DE rms 0.1863, median +0.101) and its canonical Cassini 0.376x are seen. KT1's Upsilon-shape degeneracy is known.

## Kernel, chosen before this lane, not scanned
Argon's u' = chi (1 - chi)^2: mu = 2Y - Y^2 for Y <= 1, mu = 1 for Y > 1, Y = g/s. Newtonian above g = s exactly. No other p is run.

## One float
f scales all stellar Upsilon together: disc 0.5 f, bulge 0.7 f. Gas fixed. f fitted on all 155 SPARC galaxies by minimising galaxy-equal mean r^2. Grid 0.5 to 2.0, step 0.01. 2000 galaxy bootstraps, seed 20261102.

## Gates, tolerances set now
- **G1, stellar scale:** f within [0.79, 1.26], that is 0.1 dex either side of 1, the stellar-population M/L error quoted for 3.6 micron. Equivalently disc 0.40 to 0.63.
- **G2, fit:** galaxy-equal rms at best f <= OR mu_2's rms at f = 1 + 0.005 dex, and |median r| <= 0.05 dex.
- **G3, Cassini:** q below ceiling on both footings, with the explicit-corner integrator from KT7 (`argon_p1_recheck.py` method), plus its exponential control reproducing 3.76x within 0.05.
- **G4, trend:** within-galaxy slope T2 interval at best f, reported, with bulgeless T2. Pass if bulgeless T2 contains 0.
- **G5, reported only:** f at fixed bulge 0.7 and disc free; Upsilon x f compared with Sani's median 0.862 for bulges.

## Labels, per footing
**JOINT PASS:** G1 to G4 all pass. A kernel description that passes the Solar System and SPARC at plausible stellar masses. Not a derivation of κ, of the kernel, or of anything else, and not a detection. Next it would owe clusters, lensing, LITTLE THINGS and wide binaries. **FAILS [gates]** otherwise, naming each.

## Controls
**Planted:** mock from p = 1 at f = 1.2, real scatter, must return f within 0.05. **Comparison:** OR mu_2 run the same way, f fitted, reported. **MUTATE:** Cassini with the exponential kernel must fail (expected 3.76x); SPARC with g_obs shuffled must give rms above 0.3. `_MUTATE`, exit 1. No download. Not a kappa route, so no register row. Single thread, minutes.
