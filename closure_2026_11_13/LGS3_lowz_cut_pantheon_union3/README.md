# LGS3 — X54's Pantheon+ and Union3 profiles with the low-redshift supernovae cut

Criteria, harness and collector: a2555cf0a4 (alone first, before any cut number). Labels: `lgs3_collect.out`,
`lgs3_results.json`. Commit ids, local / origin: criteria a2555cf0a4 / 1090a533ed; result 9afd5c1b7d / d46836968e.
A re-read of committed lanes (follow-on to LGS2). It adopts nothing and edits no ledger.

## Verdict
- **The lane's question, the LEAN reading** (frozen; from M-D's Δχ² at ξ = 0):
  - **Pantheon+: UNDECIDED.** The lean does go away when the low-redshift supernovae are cut: Δχ² 1.94 → 0.53. But the
    frozen size control (613 random supernovae dropped above z 0.087) also takes it away (0.44). So this lane cannot say
    whether the low-redshift supernovae or the loss of data did it.
  - **Union3: LEAN NOT FROM LOW-Z.** Δχ² 1.86 → 1.63 with the z = 0.05 node marginalised out; the control gives 1.79.
    Union3's cut is coarse: one spline node, and the z = 0.10 node still carries supernovae down to about 0.05.
- **So "a low-redshift supernova artefact" is not shown beyond DES-SN5YR.** It holds there (LGS2), is undecided for
  Pantheon+, and is not supported for Union3.
- **M-C (the primary exchange form) is UNCHANGED and STABLE in every cut,** for both compilations.
- **Reported:** in Pantheon+, dropping the very survey families that make up Dovekie's legacy set (CSP, CfA3, CfA4,
  Foundation; 374 rows) keeps the lean (Δχ² 1.82).
- **CFG689 TF and TU3F (optional part):** tracking bands STABLE at every z*, classes UNCHANGED, P2 still HINT
  (TF 2.44σ → 2.20σ, TU3F 2.61σ → 2.56σ).

## What each cut removed (counted from the files before any fit)
| compilation | sample | removed | kept |
|---|---|---|---|
| Pantheon+ (loader: non-calibrators, zHD > 0.01; 1,580) | `zcut` (zHD > 0.0870) | 613 | 967 |
| | `legacy_surveys` (IDSURVEY 5, 63, 64, 65, 66, 150) | 374 (372 at zHD ≤ 0.087) | 1,206 |
| | `rand` (control: random, from zHD > 0.0870, seed 20261114) | 613 (63 % of the z > 0.087 set) | 967 |
| Union3 (22 spline nodes) | `zcut` (node z ≤ 0.0870) | 1 node (z 0.05) | 21 |
| | `node055` (control: closest conditional precision, 1,744 vs 1,877) | 1 node (z 0.55) | 21 |

## Harness checks: PASS, exact
- **X54.** `full` equals the committed `x54_cold_de_exchange_results.json` at every graded grid point of M-C and M-D, for
  Pantheon+ and Union3 (max |Δχ²| 0, max |Δξ| 0). Every run passes Step 0 and K1–K4 (7/7). Each run used LGS2's
  rebuild, whose patch is identical to X54's.
- **CFG689.** TF's tracking quantiles are within 2.5e-6 of the committed file; TU3F's are exact. Both are within the
  0.005 line, and K4 is ok in all runs.
- The committed X54 and CFG689 folders are untouched.

## Part A — X54
| compilation | model | sample | ξ̂ | 95 % interval | 68 % interval | Δχ²(ξ = 0) | class | √X(2.33) → a0 grade |
|---|---|---|---|---|---|---|---|---|
| Pantheon+ | M-C | committed = full | −0.00133 | [−0.00363, +0.00102] | [−0.00251, −0.00014] | 1.25 | EXCLUDED BEYOND | 0.9971 CONSISTENT |
| | M-C | zcut | −0.00149 | [−0.00380, +0.00087] | [−0.00267, −0.00029] | 1.54 | EXCLUDED BEYOND | 0.9968 CONSISTENT |
| | M-C | legacy_surveys | −0.00134 | [−0.00366, +0.00100] | [−0.00253, −0.00015] | 1.27 | EXCLUDED BEYOND | 0.9971 CONSISTENT |
| | M-C | rand | −0.00156 | [−0.00388, +0.00079] | [−0.00275, −0.00036] | 1.69 | EXCLUDED BEYOND | 0.9967 CONSISTENT |
| | M-D | committed = full | +0.099 | [−0.041, +0.20 grid edge] | [+0.028, +0.169] | 1.94 | UNDECIDED | 1.0615 TENSION |
| | M-D | zcut | +0.064 | [−0.111, +0.20 grid edge] | [−0.025, +0.150] | 0.53 | UNDECIDED | 1.0392 CONSISTENT |
| | M-D | legacy_surveys | +0.104 | [−0.048, +0.20 grid edge] | [+0.027, +0.179] | 1.82 | UNDECIDED | 1.0646 TENSION |
| | M-D | rand | +0.053 | [−0.106, +0.20 grid edge] | [−0.027, +0.132] | 0.44 | UNDECIDED | 1.0323 CONSISTENT |
| Union3 | M-C | committed = full | −0.00141 | [−0.00370, +0.00095] | [−0.00259, −0.00022] | 1.39 | EXCLUDED BEYOND | 0.9970 CONSISTENT |
| | M-C | zcut | −0.00141 | [−0.00372, +0.00095] | [−0.00259, −0.00021] | 1.38 | EXCLUDED BEYOND | 0.9970 CONSISTENT |
| | M-C | node055 | −0.00139 | [−0.00372, +0.00096] | [−0.00258, −0.00019] | 1.35 | EXCLUDED BEYOND | 0.9970 CONSISTENT |
| | M-D | committed = full | +0.117 | [−0.052, +0.20 grid edge] | [+0.032, +0.200] | 1.86 | UNDECIDED | 1.0732 TENSION |
| | M-D | zcut | +0.111 | [−0.061, +0.20 grid edge] | [+0.024, +0.196] | 1.63 | UNDECIDED | 1.0693 CONSISTENT |
| | M-D | node055 | +0.116 | [−0.055, +0.20 grid edge] | [+0.030, +0.199] | 1.79 | UNDECIDED | 1.0720 TENSION |

a0 bands (X54's own): CFG689 TF [0.68, 1.05] for Pantheon+, TU3F [0.69, 1.07] for Union3. M-D's upper side stays open
in every run: ξ = 0.4 fails in CLASS's θ_s shooting, as committed.

**Labels** (each cut against the committed numbers):
- **M-C, both compilations, every cut:** class UNCHANGED, a0 grade UNCHANGED on both footings, STABLE at 95 % and 68 %.
  The control reading has nothing to attribute.
- **M-D, Pantheon+:**
  - Class UNCHANGED (UNDECIDED) and STABLE at 95 % and 68 % for every cut.
  - a0 grade CHANGED (TENSION → CONSISTENT) on both footings for `zcut` and also for `rand`.
  - Absolute a0(2.33), canonical / alt: 9.936e-11 / 1.2007e-10 → 9.727e-11 / 1.1755e-10 (`zcut`) and 9.662e-11 /
    1.1677e-10 (`rand`). `legacy_surveys` UNCHANGED.
- **M-D, Union3:**
  - Class UNCHANGED and STABLE for both runs.
  - a0 grade CHANGED for `zcut` only: √X(2.33) 1.0732 → 1.0693, against the band edge 1.07, so it crosses by 0.0007.
    Absolute a0(2.33) 1.0045e-10 / 1.2140e-10 → 1.0009e-10 / 1.2096e-10. `node055` UNCHANGED (1.0720).
- **Control readings (class, 95 %, 68 %):** "no change for zcut" everywhere. The control rule does not read the a0 grade.
  For Pantheon+ M-D, the a0 change appears for `zcut` and the control alike.
- **LEAN:** Pantheon+ UNDECIDED (0.53 for `zcut`, 0.44 for the control). Union3 LEAN NOT FROM LOW-Z (1.63).

**Reported, no label:**
- **F_made at ξ̂ [95 % ends], M-D:** Pantheon+ +8.2 % [−4.0, ≥ +15.0] → +5.5 % [−11.8, ≥ +15.0] (`zcut`), +4.6 %
  [−11.2, ≥ +15.0] (`rand`). Union3 +9.5 % → +9.1 % (`zcut`).
- **CPL fit at ξ̂, M-D:** Pantheon+ (−0.61, −1.95) → (−0.77, −1.10) for `zcut`, (−0.82, −0.86) for `rand`.
  Union3 (−0.53, −2.43) → (−0.55, −2.27).
- **The ξ = 0 refit barely moves:** H0 68.50 → 68.55 (Pantheon+ `zcut`), 68.52 → 68.52 (Union3); Ω_m within 0.001.

## Part B — CFG689 (flat + acoustic angle, 60,000 steps, same seeds)
| mode | z* | committed 68 % (median) | zcut 68 % (median) | B1 |
|---|---|---|---|---|
| TF (Pantheon+) | 1.0 | 0.877–0.999 (0.939) | 0.873–0.999 (0.936) | STABLE |
| TF | 1.2 | 0.882–0.991 (0.937) | 0.878–0.991 (0.935) | STABLE |
| TF | 1.5 | 0.804–1.052 (0.933) | 0.802–1.049 (0.932) | STABLE |
| TF | 2.33 | 0.679–1.047 (0.880) | 0.679–1.047 (0.882) | STABLE |
| TU3F (Union3) | 1.0 | 0.900–1.027 (0.964) | 0.900–1.028 (0.964) | STABLE |
| TU3F | 1.2 | 0.904–1.017 (0.960) | 0.902–1.017 (0.960) | STABLE |
| TU3F | 1.5 | 0.821–1.073 (0.954) | 0.819–1.073 (0.951) | STABLE |
| TU3F | 2.33 | 0.690–1.067 (0.897) | 0.692–1.069 (0.896) | STABLE |

- **B2:** CLASS UNCHANGED in both modes (P1 DEGENERACY BROKEN).
- **B3:** P2 UNCHANGED (HINT). TF Δχ² 14.13 → 12.57 (2.44σ → 2.20σ); TU3F 15.36 → 14.97 (2.61σ → 2.56σ).
- **Reported:** TF's native H0 median 67.56 → 67.65 km/s/Mpc, with the 68 % band widening from 66.97–68.17 to
  66.80–68.50.
- So with Pantheon+ and Union3, the cut moves none of CFG689's bands. With DES-SN5YR (LGS1), dropping the legacy set
  moved TD5F's P2 from HINT to CONSISTENT WITH CONSTANT and its H0 by +1.5.

## Reading
- In DES-SN5YR the M-D lean sat in the 197 legacy supernovae (LGS2). They sit about +0.065 mag off DES in Dovekie's
  calibration (arXiv:2610.23657).
- In Pantheon+, the same survey families (here in Pantheon+'s own calibration) do not carry the lean: dropping them
  leaves Δχ² 1.82.
- Cutting all of Pantheon+'s low-redshift supernovae weakens the lean. A random cut of the same size above z 0.087
  weakens it as much, so the frozen test cannot locate it.
- Union3's low-redshift node does not carry it.
- The M-D lean is under 2σ in every compilation, before and after every cut.

## On the coordinating session's guess
"Pantheon+'s M-D lean goes away under `zcut`; Union3 unclear."
- **The first half is right in number** (Δχ² 1.94 → 0.53). It is not confirmed as low-redshift, because the matched
  control loses the lean too. The reason given (overlap with the CfA / CSP / Foundation supernovae) is not supported:
  dropping exactly those survey families keeps the lean (1.82).
- **Union3:** its one low-redshift node does not carry the lean (1.86 → 1.63).

## Not run
- X54's DES-SN5YR profiles (loaded from the committed results; LGS2 covers them), MUTATE and S1.
- CFG689 for `legacy_surveys` and the controls, and its other modes. RF5 (not asked).
- No guard or wall-time limit was hit. Free disk stayed at 16–17 GB.

## Files
- **Harness, collector and criteria:** `lgs3_run.py`, `lgs3_collect.py`, `FROZEN_CRITERIA.md`.
- **X54 runs:** `lgs3_x54_<PP|U3>_<sample>.{out,json}`.
- **CFG689 runs:** `lgs3_cfg689_<TF|TU3F>_<full|zcut>.{out,json}`.
- **Logs:** `logs/*.txt` (`.txt` because the repo ignores `*.log`), with home paths replaced and numpy's matmul warnings
  removed.

## What this does and does not say
- X54's primary bound does not lean on any compilation's low-redshift supernovae.
- The M-D lean is a low-redshift (legacy-set) effect in DES-SN5YR only. For Pantheon+ this lane cannot separate the cut
  from the loss of data; for Union3 the low-redshift node does not carry it.
- It does not say which supernovae are right, and it does not test arXiv:2610.23657's offset.
- Nothing here measures H0 or a0, and nothing here grades the framework.

## Commit ids
Local / origin: criteria a2555cf0a4 / 1090a533ed; result 9afd5c1b7d / d46836968e (origin ids differ because the lane
commits were replayed onto origin/main without a checkout).

kappa = 1/2 FITTED; not theory closed.
