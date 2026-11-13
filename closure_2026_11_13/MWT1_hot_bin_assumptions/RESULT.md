# MWT1 RESULT: what RAW1's hot 30-40 kpc bin rests on

2026-11-13. TEST lane. Adopts nothing, relabels nothing (RAW1, HOT1, LMC1 keep their labels), registers nothing.
Criteria `FROZEN_CRITERIA.md` (commit f154c41c0f, alone, before any script or number). No amendment. One graded
run (`mwt1.out`, `mwt1_results.json`, mutations in `mwt1_MUTATE.out`). Line: the framework's no-field line,
external field dropped exactly as RAW1 did (owner note 2026-11-12). Statistic, sample, bins and line are RAW1's,
reused unchanged (raw1.py's functions executed by AST, RAW1's files read-only).

## Labels (as frozen)

| case | label | fragility |
|---|---|---|
| **FW census, canonical** | **FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST: the tracer density beyond the sample's reach** (all four literature two-slope forms) | robust |
| **FW census, alt** | **FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST: the distance scale (x0.9 or x1.1) and the tracer density** | robust |
| FW rc, canonical | FAIL DEPENDS ON AN ASSUMPTION THE DATA CANNOT TEST: distance scale and tracer density | robust |
| FW rc, alt | FAIL REMOVED BY the logg cleaning (L) or by equal hemisphere weighting (F), each alone | FRAGILE (logg 3.5, beta beyond 55 kpc 0.8) |

Read with the checks that failed (below): the rc-alt HIT is at the noise level and should not be read as more.
It awaits an independent re-grade in any case. In none of the four cases does the combination of everything
the data detect pass the bin: under it, 30-40 kpc stays HOT in all four. **Mutation M1 did not bite** (check E
cannot detect a 40 km/s dipole at p < 0.01 in this footprint), so "dipole not detected" carries little weight;
forcing the dipole into the combination (post hoc) changes only rc alt (see Post hoc).

## Every bin against every check (f +/- sigma_f, word; RAW1's own rule |f - 1| <= 2 sigma_f)

FW census, canonical (RAW1: 1.095 HOT, 1.205 HOT, 1.052 PASS, 1.090 PASS) and alt (1.052 PASS, 1.155 HOT,
1.007 PASS, 1.043 PASS):

| check | det.? | canonical 20-30 / 30-40 / 40-55 / 55-80 | alt 20-30 / 30-40 / 40-55 / 55-80 |
|---|---|---|---|
| RAW1 (none) | | 1.095 H / 1.205 H / 1.052 P / 1.090 P | 1.052 P / 1.155 H / 1.007 P / 1.043 P |
| E dipole fitted | no (p 0.015 at 30-40) | 1.090 H / 1.181 H / 1.047 P / 1.061 P | 1.048 P / 1.132 H / 1.003 P / 1.016 P |
| S1 Sgr band 25 deg | no (p 0.078) | 1.089 H / 1.248 H / 1.064 P / 1.096 P | 1.047 P / 1.197 H / 1.019 P / 1.049 P |
| S2 overdensity mask | **yes** (40-55) | 1.097 H / 1.209 H / 1.108 P / 1.090 P | 1.054 P / 1.159 H / 1.061 P / 1.043 P |
| L logg > 3.75 | **yes** | 1.074 H / 1.202 H / 1.013 P / 1.096 P | 1.032 P / 1.152 H / 0.970 P / 1.049 P |
| D-data, break 30 (sample's own) | no (2 dlnL 4.30 < 6.63) | 1.065 P / 1.053 P / 0.919 P / 0.951 P | 1.024 P / 1.009 P / 0.879 P / 0.910 P |
| B-data per-bin beta | **yes** (p 0.0003) | 1.098 H / 1.238 H / 1.104 P / 1.146 P | 1.055 P / 1.187 H / 1.057 P / 1.096 P |
| X-err (error scale 1.31) | **yes** | 1.094 H / 1.204 H / 1.048 P / 1.080 P | 1.052 P / 1.154 H / 1.003 P / 1.033 P |
| F hemisphere equal weight | **yes** (40-55) | 1.094 H / 1.190 H / 1.120 P / 1.089 P | 1.051 P / 1.141 H / 1.072 P / 1.042 P |
| **C = S2+L+B+Xerr+F** | | 1.090 H / **1.225 H** / **1.164 H** / 1.143 P | 1.048 P / **1.174 H** / 1.115 P / 1.094 P |
| U X-dist x0.9, on C | untestable | 1.120 H / 1.186 H / 1.091 P / 1.107 P | 1.076 P / 1.137 P / 1.044 P / 1.059 P |
| U X-dist x1.1, on C | untestable | 1.081 H / 1.142 H / 1.184 H / 1.122 P | 1.038 P / 1.095 P / 1.134 P / 1.073 P |
| U D-lit 2.5 / 4.5, break 25, on C | untestable | **0.921 C** / 1.110 P / 1.057 P / 1.037 P | **0.884 C** / 1.064 P / 1.012 P / 0.992 P |
| U D-lit 2.5 / 4.0, break 30, on C | untestable | **0.802 C** / 1.031 P / 0.982 P / 0.964 P | **0.770 C** / 0.989 P / 0.940 P / 0.922 P |
| U beta 0.2 / 0.8 constant, on C | excluded by the 30-40 PMs (> 3 sigma) | 1.305 H / 1.153 H at 30-40 | 1.252 H / 1.105 P at 30-40 |

sigma_f runs 0.034-0.042 (20-30), 0.051-0.094 (30-40), 0.049-0.085 (40-55), 0.10-0.13 (55-80). FW rc and the
comparators under every check are in `mwt1.out`. FW rc at 30-40: RAW1 1.135 / 1.114 (can / alt), C 1.154 / 1.133
(both HOT), L 1.132 H / 1.111 P, F 1.121 H / 1.100 P, E 1.113 H / 1.092 P. DESI's NFW behaves like the framework
line in every row (30-40: 1.142 H in RAW1, 1.161 H under C, PASS under D-data, X-dist and D-lit), so none of this
singles out the framework.

## What the data support, and what they cannot test

Detected by the frozen rules (p < 0.01) and therefore in the combination:
- **L** contamination: 213 stars in 20-80 kpc have confident LOGG > 3.75 (median of the sample 3.38). Removing
  them cools 20-30 and 40-55 by more than random masks of the same size, and leaves 30-40 unchanged (-0.003).
- **S2** overdensity: a real cold group in **40-55 kpc** (24 flagged stars against 0.9 expected, dispersion
  9.3 km/s). Nothing in 30-40 (2 flagged, 1.1 expected). Removing it heats 40-55 by +0.054.
- **B** anisotropy is not constant (0.671, 0.685, 0.441; p 0.0003). The variable-beta Jeans solution makes 30-40
  hotter (+0.03), as expected.
- **X-err**: repeat observations (1,000 pairs, 752 stars) say the quoted velocity errors are 1.31 +/- 0.05 times
  too small. With errors near 2 km/s against dispersions near 100, this moves f by 0.001 or less.
- **F**: north and south differ in **40-55** (f 0.96 north, 1.28 south, p 0.006), not in 30-40 (p 0.71).
  Equal weighting moves 30-40 by -0.015 and 40-55 by +0.07.
Not detected: E dipole (43 +/- 14 km/s at 30-40, p 0.015; M1 shows the test lacks power), S1 (the 15-25 deg
stars in 30-40 are colder, 95.7 against 110.6, p 0.078), D-data (break at 30: inner 5.71 +/- 0.27, outer
4.33 +/- 0.48, 2 dlnL 4.30, p about 0.04).
Equilibrium diagnostics: the 30-40 bin, and only it, is visibly non-Gaussian. Excess kurtosis is -0.62
(p 0.0085) and the bimodality coefficient 0.41 (p 0.0075). Removing the dipole does not change that. The other
bins are consistent with a Gaussian (p 0.36 to 0.81). Polar cones against the rest: no difference at 30-40
(p 0.19).

Cannot be tested with these files:
- **The tracer slope beyond about 45 kpc, and the completeness model that sets alpha.** The window ends there.
  The sample's own fit with a break at 30 gives 4.33 outside against the single 5.29. That alone, not detected
  at the frozen 0.01, puts every bin of every FW case at PASS, the hot bin included. The literature two-slope
  forms (inner 2.5) also pass 30-40, but they put 20-30 COLD (f 0.74 to 0.92), and the sample measures 5.4 to 5.7
  there. So the inner half of D-lit is contradicted by the data; the outer half is what the data cannot test.
- **The absolute distance scale.** Gaia parallaxes give 1.11 +/- 0.30 of 1/d at 30-40 kpc, which is no test at
  10 per cent. Both x0.9 and x1.1 (whole measurement redone, so alpha, beta and bin membership change) lower
  30-40 enough to pass on alt and on rc, but not on census canonical.
- Spherical symmetry beyond the polar-cone split, and equilibrium beyond first moments: no flattened or mixture
  model was computed.

## Symmetric effect on the passing bins

- The combination of detected corrections turns **40-55 kpc from PASS to HOT for census canonical** (1.052 ->
  1.164 +/- 0.080). That comes from S2, B and F, which act mostly on that bin. For every other case 40-55 stays
  PASS but moves up by 0.07 to 0.11.
- D-lit makes 20-30 COLD in every case (alt and rc included), and 40-55 COLD on the nominal sample for outer
  slope 4.0.
- X-dist x1.1 on C turns 40-55 HOT for census canonical.
- The constant beta 0.2 bracket makes 40-55 and 55-80 HOT. It is excluded by the bin's own PMs.
- The only check that lowers 30-40 without breaking a passing bin is the sample's own break (D-data). It was not
  detected at the frozen threshold.

## Twins, known answers, mutations

- Known answers K0-K3 pass: RAW1's counts, dispersions, alpha, beta and every f and sigma_f reproduced to 1e-10;
  the variable-beta solver at constant beta equals RAW1's to 8e-14; fit_scale equals fit_f; SI check
  g(30 kpc) = 3.611e-11 m/s^2, M = g r^2 / G = 2.331e11 Msun, V = 182.8 km/s.
- T2 (dipole on shuffled velocities): p 0.80, not detected. Passes.
- T1 random masks (100 per mask check): the seeded twin leaves the 30-40 word unchanged in every census and rc
  canonical case. **It FAILS for rc alt** under the S1, S2 and combination-mask sizes: random masks flip that
  bin in 10 to 47 per cent of draws. rc alt sits on its threshold (1.114 against 1 + 2 x 0.054 = 1.108), so its
  REMOVED label is inside what a random mask does. L's shift there (-0.003) is inside the random range.
  F is not a mask: it moves the bin by -0.014.
  Only S2 (at 40-55) and L (at 20-30 and 40-55) move bins beyond the random range. S1's +0.04 at 30-40 is
  inside it.
- **M1 FAILED TO BITE**: a 40 km/s dipole injected into 40-55 is recovered exactly (40.0 +/- 17.1 km/s, 0 deg
  off), and removing it restores f (1.047 -> 1.047). But the detection p is 0.022, not below 0.01. The removal
  works; the frozen detection rule does not have the power to see a dipole of this size here.
- M2 bites: 21 of 25 planted cold stars flagged.
- Reproducibility: the post hoc copy (below) re-ran the whole lane and reproduced every number before the
  combination byte for byte, and the mutations file equally.

## Post hoc (after the graded run; not graded; changes no label)

Because M1 failed, `mwt1_posthoc_E_forced.py` (a copy of `mwt1.py` with E forced into the combination; outputs
`mwt1_posthoc_E_forced.out`, `.json`, `_MUTATE.out`) puts the dipole into C. The 30-40 kpc values become: census
canonical 1.204 H, census alt 1.154 H, rc canonical 1.134 H, rc alt 1.113 +/- 0.063 PASS (row PASSES). The
labels under this reading are: census canonical and alt, and rc canonical, unchanged (DEPENDS); rc alt REMOVED
(by E, L or F alone, and by the combination), FRAGILE on the S2 p < 0.05 bracket.

## What RAW1's fail rests on

**Main reading.** The hot 30-40 kpc bin is a feature of the stars, not of a cleaning step. Removing high-gravity
contaminants, cold groups, Sagittarius-near stars, a fitted sky dipole, and correcting the velocity errors, the
anisotropy profile and the hemisphere balance leaves it 13 to 22 per cent hotter than the line on every case.
Several of those corrections make it hotter. A reader who wants the theory to fail can point to this: the
corrections the data actually support do not remove the fail, and they push a passing bin (40-55) to fail on
census canonical. DESI's own NFW fails the same bin in the same way.

A reader who wants the theory to pass can point to three other things:
- The bin is the only non-Gaussian one (flat-topped, kurtosis p 0.009). That is a sign of unrelaxed material,
  which no mask here isolates.
- The verdict rests on a tracer slope extrapolated beyond the sample's reach. The sample's own two-slope fit
  (outer 4.3 instead of 5.3, about 2 sigma preferred) passes every bin of every case. A 10 per cent shift in the
  distance scale, which the data cannot check, also passes the bin on alt and on rc.

So the fail rests on the outer tracer density and the distance scale, which these files cannot measure, and on
the equilibrium of a bin that looks least equilibrated. It does not rest on anything the data can check and
correct.

## Limits

- Masks keep RAW1's alpha and beta; only distance shifts redo the measurement. S2 flags are fixed at nominal
  distances when distances are shifted.
- The D-data slope is fitted to 20-45 kpc and extrapolated as a constant beyond.
- Equal hemisphere weighting is a fair-sky estimator, not a model of asymmetry.
- The parallax zero point (+0.017 mas) is from memory (PROVISIONAL).
- The literature slopes for D-lit are RAW1's disclosed values from memory, not re-read (PROVISIONAL).
- The frozen label rules do not name the case where the bin turns COLD under the combination. It did not arise.
- The rc-alt label depends on a threshold crossing smaller than random-mask scatter.
- Runtime about 6 minutes per run, one thread.

## Files

`FROZEN_CRITERIA.md`, `mwt1.py`, `mwt1.out`, `mwt1_results.json`, `mwt1_MUTATE.out`; post hoc
`mwt1_posthoc_E_forced.py`, `mwt1_posthoc_E_forced.out`, `mwt1_posthoc_E_forced.json`,
`mwt1_posthoc_E_forced_MUTATE.out`. Data: RAW1's `MWS_BHB.fits` (sha256 5669c821...5246, not in the
repository; checked by the script). Run: `python3 -I -B mwt1.py <MWS_BHB.fits>`.

**Commit ids and the lead's check (added 2026-11-13, after landing; no number or label changes).** Local: criteria
f154c41c0f, script and graded run a981fdcc8e, RESULT 9f1eadc34d (origin tip 3bb9b7e2cd). Pushed. The lead's standing
re-run was NOT done: the star catalogue is held outside the repository and the lead session did not locate it, so this
file has been reproduced by no one but the lane. The lead confirmed in git that the criteria commit holds that one file.
No independent re-grade exists.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
