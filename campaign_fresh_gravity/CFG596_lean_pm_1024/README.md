# CFG596: lean 1024³ PM for a decisive framework-native shear test. PRE-FLIGHT STOP: no buildable box makes CFG592's native test DIAGNOSTIC under its frozen rule; L = 400, N = 1024 keeps zero data points

- **Date:** 2026-10-10. **Status:** stopped at the pre-flight, before any engine work, frozen criteria or production run. Nothing was run on the PM; no machine time was committed to a day-long job.
- **Settings:** κ = ½ is FITTED. Footings never pooled. The cold energy's MASS is still required. Not "theory closed". Nothing here says the data favour the framework.
- **Numbers:** every number below comes from `cfg596_preflight.json` and `cfg596_tooth_audit.json`.
- **No verdict role.** This lane issues no class for the framework. It checks whether the planned production *could* change CFG592's NOT DIAGNOSTIC, using CFG592's native machinery unchanged (`cfg592_native.py` is exec'd up to its run section; nothing in it is edited).

## Why a pre-flight

The plan was: build a memory-lean copy of the CFG518 census engine, validate it, run L = 400 Mpc/h, N = 1024 for S0 and the framework (days per run), then re-run CFG592's native likelihood. CFG592's frozen rule needs two things for a run to count:
1. **Support cut:** a data point is kept only if ≥ 90% of its Limber–Hankel integrand lies inside [k_lo, k_hi], with k_hi = πN/(4L). A survey with fewer than 10 kept points is NOT DIAGNOSTIC.
2. **Tooth NZ2:** a 20% excess ramped over k = 0.5 → 1 h/Mpc, injected into the S0 best-fit mock, must give an S0 refit χ²_min ≥ 9 (IA and photo-z free). Otherwise NOT DIAGNOSTIC.

Both depend only on [k_lo, k_hi] and on the S0 spectrum, so they can be checked before any run.

## Method (`cfg596_preflight.py`, `cfg596_tooth_audit.py`)

- **S0 spectrum:** existing S0 PM spectra spliced together: CFG518 S0 L200 N512 below k = 0.5, CFG530 S0 L100 N512 above, matched at k = 0.5. Nodes z = 0, 0.5, 1 come from their JSONs. Beyond the grid, the extension rule is `node_P`'s own.
- **Hypothetical box:** only changes [k_lo, k_hi]. k_lo = 1.276 × 2π/L, the first-bin ratio of the L200 run.
- **Proxy check:** at L100 N512 the proxy keeps 20 KiDS / 40 DES points, and the tooth gives χ² 0.89 / 0.13. CFG592's real run gave 20 / 38 points and 0.79 / 0.04. The proxy reproduces the real run closely.

## Results

**Support cut and frozen tooth** (`cfg596_preflight.out`):

| box | k range (h/Mpc) | KiDS kept | DES kept | frozen NZ2 χ² KiDS / DES |
|---|---|---|---|---|
| L200 N512 (existing) | 0.040–2.01 | 0 | 0 | — |
| L100 N512 (existing) | 0.080–4.02 | 20 | 40 | 0.89 / 0.13 FAILS |
| **L400 N1024 (planned)** | 0.020–2.01 | **0** | **0** | — |
| L400 N768 | 0.020–1.51 | 0 | 0 | — |
| L300 N1024 | 0.027–2.68 | 0 | 0 | — |
| L250 N1024 | 0.032–3.22 | 0 | 6 | — |
| L200 N1024 | 0.040–4.02 | 49 | 57 | 1.32 / 0.36 FAILS |
| L150 N1024 | 0.053–5.36 | 93 | 70 | 4.13 / 0.79 FAILS |
| L100 N1024 | 0.080–8.04 | 119 | 100 | 6.33 / 0.88 FAILS |
| L400 N1536 | 0.020–3.02 | 0 | 0 | — |
| L400 N2048 | 0.020–4.02 | 84 | 153 | 1.39 / 0.82 FAILS |
| L100 N2048 | 0.080–16.1 | 156 | 118 | 7.37 / 1.42 FAILS |
| idealised, everything resolved | 0.005–49 | 225 | 227 | **7.95 / 1.95 FAILS** |

1. **The planned L = 400, N = 1024 production keeps no data point in either survey.** Its k_hi = 2.01 equals the L200 N512 k_hi. The cut is set by k_hi, and lowering k_lo does not rescue small-θ points.
2. **No box passes the frozen tooth, not even the idealised one where every published point is kept.** With all 225 KiDS points the 20% excess gives χ² 7.95 (< 9); DES gives 1.95. Under CFG592's frozen rule the native test is NOT DIAGNOSTIC for every possible PM box. The limit is the data plus the free nuisances, not the PM's k range.

**Tooth audit** (`cfg596_tooth_audit.out`). (b) fixes IA = 0. (c) is the ramp amplitude the data can detect at χ² = 9. (d) injects the framework's own measured boost B = P_grav/P_part (CFG530 L100 N512, z = 0, held at all z, held flat outside k 0.08–4) instead of the 20% ramp.

| box | survey | (a) frozen NZ2 | (b) no IA | (c) amplitude for χ² = 9 | (d) own boost, can / alt |
|---|---|---|---|---|---|
| idealised | KiDS | 7.95 | 9.12 | 0.213 | 16.98 / 22.10 |
| idealised | DES | 1.95 | 2.44 | 0.516 | 17.91 / 16.64 |
| L150 N1024 | KiDS | 4.13 | 4.42 | 0.294 | 14.43 / 18.75 |
| L150 N1024 | DES | 0.79 | 0.89 | 1.056 | 3.40 / 4.21 |
| L100 N1024 | KiDS | 6.33 | 7.41 | 0.238 | 14.64 / 19.14 |
| L100 N1024 | DES | 0.88 | 1.20 | 0.709 | 8.56 / 9.69 |

- **KiDS just misses the frozen tooth.** It needs a 21.3% ramp with everything resolved, and 23.8% at L100 N1024. DES needs ≥ 52%.
- **The framework's own boost is larger than the tooth's 20%.** It would be detectable on KiDS at χ² 14–22 even in boxes of L100–150 at N = 1024. This is the same point CFG592 made at N = 512.
- **The tooth's shape is what fails.** The frozen tooth is a 20% excess concentrated at k ≥ 1. The framework's boost already reaches 1.20 at k = 0.3. The tooth is the frozen criterion, so it stands.

## What this means for the lane

- **Production as specified (L400 N1024) cannot change CFG592's NOT DIAGNOSTIC.** It would keep zero points.
- **No other box can either,** while NZ2 stays as frozen.
- **The engine work (a lean 1024³ PM) was not started.** For reference only, a rough analytic estimate (not measured): float32 positions and velocities for 1024³ particles take 25.8 GB; one float32 1024³ mesh plus its rfft take about 8.6 GB. A chunked engine could plausibly fit under 50 GB. Two other heavy jobs (CFG595, CFG468) were running on the machine at the time.
- **Options that need an owner decision** (none taken here, and each would need its own frozen criteria committed alone):
  1. Accept CFG592's NOT DIAGNOSTIC as final for the native track under its frozen tooth.
  2. Declare a new, separately frozen sensitivity rule, for example a tooth sized at the excess the data can detect, or the framework's own predicted boost shape. **Caution:** this rule would be chosen after seeing that the frozen one is unreachable. It must be disclosed as post-hoc and carries no right to rewrite CFG592.
  3. If option 2 is approved, the useful box is L100–150 at N = 1024 (k_hi 5–8), not L400. It keeps 93–119 KiDS points.

## Disclosures (dated 2026-10-10)

- **No FROZEN_CRITERIA.md was committed for this pre-flight.** It is a feasibility check with no verdict role, it applies CFG592's frozen rule unchanged, and it touches no framework–data Δχ².
- **The (d) injections are mocks.** They use only the S0 best-fit theory and the framework's z = 0 boost; no framework fit to data was computed.
- **The spliced S0 spectrum is a proxy.** The support fractions depend weakly on its shape; the proxy-vs-real check at L100 N512 is above.
- **The idealised box (L1600, N 100000)** is a reference, not a buildable run.

## Scripts

- `cfg596_preflight.py`: about 1 min.
- `cfg596_tooth_audit.py`: about 12 min.
- Run each with `nice -n 10`. Both read CFG592's data in `_external_data/cfg592_work`, and the CFG518 / CFG530 / CFG555 caches, read-only.
