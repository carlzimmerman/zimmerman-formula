# CRISP FINDING: an NL1 primary pass would not establish the one-number claim

The finite audit reproduced the ng48 medians and the documented synthetic estimator benchmark. An independent
CLASS/EPS scalar calculation reproduced all six recorded CL3 crossover roots to 1.78e-15 dex. It found two material
claim/implementation mismatches. No existing lane or process was changed.

## 1. The successful calibration uses two distinct prescriptions

The equation page, `rebuild_2026_10_22/THEORY_EQUATIONS_2026-10-28.md:25`, writes

    Sigma_core(M) = max(Sigma_a0, eta(L) Sigma_coll(M)).

CL2/CL3 and NL1's actual LEE1 harness instead use

    c_f(M) = L c_nat(M) / c_nat(1e14),
    Sigma_core(M) = max(Sigma_a0, eta(c_f(M)) Sigma_coll(M)),
    eta(c) = 4/(3 B(1)) c^(5/4).

See `LEE1_look_elsewhere/lee1.py:125` and `:140`. The S9 mass slope therefore changes the collapse contribution by
factors **1.7880593 / 1.1591782 / 1** relative to the displayed eta(L) equation at masses 1e12 / 1e13 / 1e14.

The calibrated CL3 switch uses the constant-L equation to determine T, then overrides the branch flag with M > T
while keeping the mass-dependent S9 core amplitude. These are not branches of the identical surface-density
function. They can still be described as two prescriptions sharing one external L, but that is a different claim.

The independently calculated crossings are log10(T/Msun):

| L | constant-L canonical / alt | actual S9-core crossover canonical / alt |
|---|---|---|
| 3.75 | 12.235678 / 12.573882 | 11.223223 / 11.549190 |
| 3.9 | 12.148813 / 12.485930 | 11.139432 / 11.464471 |
| 4.0 | 12.092887 / 12.429302 | 11.085468 / 11.409915 |
| 7.31 reference | 10.792888 / 11.114167 | 9.826715 / 10.138549 |

For example, at L=3.75 and M=1e12 the canonical S9 collapse contribution is **1.5647808 times the floor**,
yet CL3's switch declares no halo because 12 < 12.235678. On alt the same two values are 1.2948035 and 12 < 12.573882.
Replacing the switch by the actual S9-core crossing would move it by about one dex. This audit does not regrade that
replacement or assert that it passes. The S9 profile below 1e12 is a clamped extrapolation, just as in the harness.

## 2. NL1's pass requires the empirical T=12.3, not the derived-T grade

`NL1_native_level_L/nl1_native_level.py:70` grades PRIMARY at fixed logT=12.3. Lines 75-76 select its success verdict
solely from PRIMARY. `CL3_T` is separately reported and cannot veto the success verdict.

There is a concrete existing counterexample to the general implication: at L=4 the CL2 fixed-T=12.3 canonical
configuration passes every line, while CL3's derived logT=12.092887 fails lensing with delta-chi2 **+22.3947796**
relative to the law. This does not predict the eventual NL1 result. It proves that primary success alone is not the
necessary simultaneous-L-and-T check.

`cl3_T()` at NL1 line 68 also supplies one canonical-only linear approximation as the threshold on **both** footings.
At the three recorded CL3 settings, this undershoots the correct alt threshold by **0.33693-0.33818 dex**.
Canonical interpolation is close near the calibration points (maximum difference 0.001687 dex), but at the frozen
reference L=7.31 it undershoots the freshly solved canonical root by **0.614888 dex** (alt: 0.936167 dex).

A correct later one-number audit would require success at the exact per-footing constant-L crossover for the native
L, explicitly retaining the distinction between that switch and the S9 core prescription. Existing NL1 and its
follower were deliberately preserved.

## 3. Native L is still conditional, even after the pending runs finish

NL1 defines L_nat = 7.31 median(c64,1e12) / 11.63. Its criteria explicitly disclose that the ensembles are unpaired
and assume that the 1e12 resolution ratio transfers to 1e14 while the ng48 S9 shape is retained. Nine ng64 runs at
1e12 cannot test that mass-transfer assumption or continuum convergence at cluster mass.

NL1's 68% bootstrap resamples only the ng64 numerator. It treats both ng48 reference numbers as exact. As a finite
diagnostic, this audit's 2000-resample PCG64 bootstrap of the nine recorded ng48 1e12 seeds gives median c48=11.63020
and interval **[8.37028, 12.74026]**. Inverting those reference endpoints alone produces factors **[0.91285, 1.38944]**
around an L calculated with 11.63. This is not a confidence interval for the unseen ng64 result; it shows an omitted
source of uncertainty. The cluster reference and mass slope also have seed scatter.

The provenance is model dependent. X48's criteria describe Newtonian collisionless dust plus the background Lambda
term, without the acceleration floor and without the failed v3s dynamics. Its formation inputs use background A,
the record's plik-lite CMB refit, rather than the BAO+BBN background used in GS1's budget. Therefore any phrase such
as "only kappa fitted" must be limited to the declared halo-rule coefficients, conditional on fitted background and
primordial-spectrum inputs, survey calibrations and the phenomenological switch. See `ASSUMPTION_LEDGER.md`.

## 4. Live operational observation

At **2026-10-28 17:46:24 UTC** all nine existing ng64 zoom processes were live, with launcher PID 93757 and zoom PIDs
93780-93788. **Zero** final snapshots or done files existed. No partial checkpoint was measured.

The existing NL1 follower, PID **22327**, was already running. It polls every 900 seconds until nine final snapshots
exist or the A3 launcher disappears, then invokes NL1 once and writes `main_stdout.log`. Thus a follower already
exists; starting another would duplicate it. Launcher disappearance can trigger NL1 with fewer than nine finals;
NL1 then applies its own seven-ok readiness rule. No completion ETA is asserted.

The latest logged physical integration times ranged from 3.6341 to 5.4861 of 6.0817 Gyr, with seed 5's log at step600
and the other logs at step800. Log cadence is coarse; this is not a wall-clock forecast. Full time-stamped process
rows, log tails, mutable checkpoint/log hashes and final-file flags are in `LIVE_STATUS_2026-10-28.json`.

## 5. Reproduction, controls and exact scope

Authoritative fresh numerical evidence: `run_003/results.json`, `run_003/stdout.txt` and its v2 `manifest.json`.
It completed in 3.625 seconds, with **10/10** checks and measured peak RSS **0.110952448 GB**, using Python3.13.9,
NumPy1.26.4, SciPy1.14.1 and classy v3.3.4. All declared input hashes were unchanged. The scalar solver uses the
same finite CLASS/EPS discretization as CL3, coded independently, on its fixed background-A vector.

`run_002/results.json` and `run_003/results.json` are byte-identical:

    5c94d1d51c1d0b37835be6cd88c899eb6e1c048728b6214f863957e158d0f81e

`run_004_MUTATE` intentionally corrupts the cached 1e12 median-reference check by 10%; only K1 fails, and the
process exits1 as required. Its failed status is expected control evidence. Both run003 and the mutation manifest
validate against current inputs. `run_001` is retained as launch-failed evidence: macOS rejected the requested
RLIMIT_AS before the scientific child began. No memory cap is claimed for later runs; CPU50s, wall60s, one-thread
environment and observed-RSS checks were retained. `run_002` additionally records sandbox denial of nice; run003
and the mutant ran at nice15 without that error.

The exact child argv is recorded in each manifest. To regenerate in a fresh local output directory with the same
installed interpreter, use the recorded `nice -n 15 <Python3.13.9> -I audit_native_l_t.py --output <new-directory>`
under the computation-audit bounded runner, with `contract.json` and its complete `execution_artifacts` list as
`--input` arguments; add `--mutate` for the control. The contract pins the deterministic finite domain and versions.

The git checkpoint was **7954d48377463cafcae3e8dbb09454134aef384f**, with an already very dirty tree (1355 porcelain
lines at the initial audit observation). No commits were made. Only this new lane directory was written. The old
CL2/CL3 observational grades were read, not independently recomputed from raw observations. The scalar EPS result
does not establish the physical correctness of EPS, spherical collapse, the native zoom dynamics, a condensation
mechanism or a covariant parent. kappa=1/2 remains fitted; both footings remain separate.

Read-only record checks covered the briefs, theory page, NL1 criteria/code, X48 criteria/estimator/common-mode
correction, CL2/CL3, LEE1, DT1, F3 and X41. A bounded prior-record search included the campaign ledgers,
candidate-law register, DS final record, argon, why-4, time and core-open-problem trees. No closed expensive route
was rerun. `INPUT_SHA256.json` contains full source/input hashes; `SHA256SUMS` inventories this lane's artifacts
(excluding the checksum file itself).
