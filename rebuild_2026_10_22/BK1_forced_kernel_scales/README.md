# BK1_forced_kernel_scales: NO SURVIVOR, AND THE GATE DOES NOT CERTIFY. 5.2e9 trees tried, hits equal the scrambled control (ratio 1.03), 0 pass gate 2. The port re-finds a0's formula, but corrected FDR gives a0 itself 0 bits locally

Criteria: `FROZEN_CRITERIA.md` (a9002cde01), alone first. `AMENDMENT_A1.md` (8c6b6c177b), error budget, before any search. Gate 5 committed before any target search (022dd411ca). Scripts `bk1_budget.py`, `bk1_engine.py`, `bk1_cal.py`, `bk1_search.py`, `bk1_read.py`; numbers `bk1_cal.out`, `bk1_read.out`, `runs/`. **Not blind.** kappa = 1/2 FITTED. Footings never pooled. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## Survivors at each gate
| Gate | Count | Note |
|---|---|---|
| Trees tried | 5.238e9, plus G2 1.4e6 | 14 runs, 13 target-footing rows |
| 1 dimension | 2.607e8 correct | Vacuous for dimensionless targets, as stated before search |
| 2 FDR, hits in 2 sigma | 6.379e7, depth <= 5 | **Control mean 6.188e7, ratio 1.03** |
| 2 pass, reading A (10 bits) | **0** | Could not pass: every target's ceiling is below 10 before look-elsewhere |
| 2 pass, reading B | **not issued** | B_ref is 0 bits, so it can't separate anything |
| 3 forced kernel | **0** | No survivors. 721 of 771 depth <= 3 hits decompose mechanically, but so do 92 % of all such trees |
| 4 interlock | **0** | See below |
| 6 empirical | not reached | |

**Every match is labelled COINCIDENCE.** This includes the tidy ones below.

## Gate 5: DOES NOT CERTIFY, frozen label
| Check | Result |
|---|---|
| C1 `calibrate.py` | 8/8 reproduced as a code test. **Its a0 Gate A pass is a unit mismatch**: a null near 1e-10 compared with target 2.894, P 0, bits infinite. Compared with a0 it gives 5.5 bits, under its own line. Project_atomos not edited; it needs its owner's fix |
| C2 port re-finds c sqrt(G rho_c)/2 | **Yes**, 1.1936e-10, 0.53 % from 1.2e-10, depth 4 in this grammar. MUTATE (G's dimension wrong) loses it |
| C3 kernel | **Yes**, Einstein x Friedmann x free 1/2. Weak: see gate 3 below |
| C4 corrected gate 2 on a0 | **Fails.** Below |
| C5 negatives | All reject, 0 bits. So does k = pi^2. They reject because nothing here gets bits, which isn't a discrimination |

| a0 window | LOCAL +- 1 dex, x15 | LOCAL, no multiplier | SPAN, x15 | SPAN, no multiplier | Ceiling |
|---|---|---|---|---|---|
| +- 2 sigma, sigma 20 % (McGaugh+16, recalled, PROVISIONAL) | 0 | 0 | 1.97 | 5.88 | 2.44 local |
| 5 % half-width | 0 | 0 | 0 | 2.65 | 5.52 |
| 10 % | 0 | 0.20 | 2.47 | 6.38 | 4.52 |

**What this means.** Scrambled targets within a dex of a0 get hit as often as a0. The enumeration's hit carries about no evidence by itself. What's left is the scale (SPAN, up to about 6 bits, and SPAN's range is inflated by Planck-laden trees, with a clip at the histogram edge lg 400), the forced kernel argument, and what the law does on data, which this lane doesn't test. It doesn't say a0's law is wrong. **It says the gate as specified would reject the case it was built around,** and that the record's "certified" line for a0 can't rest on Gate A.

By the frozen rule the search ran for counts, and no gate 2 PASS can be issued.

**Power.** A planted true tree: sqrt(8 pi/3)/2 at sigma 1e-4 gets 1.01 bits (4.92 without x15), found at depth 4. rho/3 at sigma 1e-3 gets 2.89 local, 5.06 span. So at these depths and tolerances **even a true formula doesn't reach 10 bits**. The plant is recovered, the gate lacks power.

## Targets, 2 sigma. Canonical, alt in `bk1_read.out`
Ceiling is the most any single formula could score at this tolerance, before look-elsewhere. "Hits" is depth <= 5, alphabet A, against control mean.

| Target | Value, sigma | Flag | Ceiling, bits | d*, P, bits | Hits vs control | Lowest-depth hit, Z |
|---|---|---|---|---|---|---|
| K | 13.29, 3.23 | BLUNT | 2.12 | 3, 1.0, 0 | 2.71e6 vs 2.70e6 | 1/(3 f_b^2) = 13.44, +0.05 |
| D8 | 7.56, 1.74 | BLUNT, band | 2.21 | 2, 0.81, 0 | 2.75e6 vs 2.69e6 | 1/f_b = 6.35, -0.70 |
| D5 | 5.37, 1.31 | BLUNT, band | 2.10 | 2, 0.84, 0 | 3.20e6 vs 2.99e6 | 1/f_b, +0.75 |
| XR | 5.350, 0.145 | stat missing | 5.41 | 4, 1.0, 0 | 2.29e4 vs 4.69e4 | no hit at depth <= 3 |
| RHO canonical | 2.249e-27, 6.1e-29 | stat missing | 5.41 | 4, 1.0, 0 | 2.76e4 vs 3.20e4 | no hit at depth <= 3 |
| RHO alt | same | | 5.41 | 2, 0.19, 0 | 5.28e4 vs 3.12e4 | rho_total/4, -1.90 |
| FQ | 0.946, 0.154 | BLUNT, contains 1 | 2.76 | 2, 0.94, 0 | 2.04e6 vs 2.07e6 | 6 f_b, -0.01; also 1, +0.35 |
| T | lg 12.29, 0.05 dex | window | 3.32 | none | **0 vs 0** | No hit at any depth |

Second readings (HSC 1.7, 1 % stat) change no label: P rises to 1.0 or stays, bits 0. Using x25 rather than x15 changes nothing at 0 bits. G2 with addition: hits 0.9 to 1.4 times control on K, D8, D5, FQ, 0.56-0.95 on RHO, 0.37-0.44 on XR, no bits (`runs/`).

**T.** The lowest mass in the alphabet is lg 19.3 M_sun (A) and 15.7 (B), so T sits 7 and 3.5 dex below anything reachable. As expected: c, G, rho, a0 and f_b hold no small number. This repeats TD1's missing piece with a0 allowed: **T needs a scale outside this alphabet.**

## Near misses, all COINCIDENCE, with margin to the line
- **1/f_b against the deficit: D8 Z -0.70, D5 Z +0.75, K 2nd reading -1.23.** Margin 10 bits; it has 0. D is a band of a falling function, and 1/f_b sits between bands, so this isn't a fit. And it's the plainest thing in the list: cluster mass tends to the cosmic ratio.
- **XR 5.350 and D5 5.37 agree, difference 0.02 against D5's sigma 1.31.** That's a numeric coincidence of windows as far as this lane can tell. Any XR formula lands in D5's window automatically, so window overlap would give gate 4 for free; scrambled windows that size overlap 24 % of the time. Also 1/f_b - 1 = XR by definition, which is why f_b was removed there. I'm not reading the agreement as support for anything; it isn't derived, and D falls with radius.
- **rho_total/4, alt, Z -1.90**: on the edge, on one footing, canonical has nothing. P 0.19.
- **1/(3 f_b^2) for K, Z +0.05** is one of 36 depth-3 hits against control 37.7. Z near 0 means nothing at sigma 24 %. Bare k also has UX3's and CU1's limit: no k clears every key.
- **f_Q = 1**, Blumenthal, Z +0.35, depth 1 in effect. It's already its own theory's number, so nothing new.

## Gate 3 doesn't separate at this depth
92 % of all dimensionless depth <= 3 trees (2448 of 2672) decompose into the frozen registry, because 1, 3, 4, 6 are all products of 8 pi, 4 pi, 2 pi and 3. So C3's pass for a0 is much weaker than it looks mechanically; **the work is in the written reason why that law acts in that observable**, a human step. I wrote no such line for any hit here, and have none to write: FORCED FACTORS, NO LINK.

## Gate 4
No formula passed gate 2 to be tested. As information: class I targets can't pair with FQ under a factor 2 (windows too far apart), and I-II overlap is by windows, above. T and RHO can't share a skeleton with dimensionless targets. Mode C2 isn't available: the only constants tied by any formula are a0, c, G, rho, whose tie is the fitted 1/2.

## Limits and departures from frozen, all stated
- **Depth.** Full to 4, decoration only at 5, on 4-6 leaves. A true formula deeper than this is missed, though at these tolerances deeper trees only raise the control's rate.
- **Hit rows.** FROZEN says up to 200000 depth 4-5 rows per target. I saved the lowest-Z 2000 rows plus 30 printed, and Z histograms of all hits; depth 5 hits are histogram only.
- **Gate 3 code.** I used a local decomposition against the frozen registry, not an actual call to atomos's `forced_kernel_detector`, which runs on a0 only inside C1.
- **Gate 4.** Reported by window arithmetic, with one scrambled overlap rate, not the full scored count over hits frozen, because no hit reached it.
- **Row count.** x15 frozen, 13 rows, or 25 with alphabets.
- **Budgets.** XR and RHO have no statistical term, as no chain exists; T's sigma is a window read as 2 sigma; McGaugh's a0 error is recalled. A real XR chain could only widen it, and it can't change a 0-bit reading.
- **Controls.** LOCAL +- 1 dex is the record's method but also fixes the ceiling: 2 dex range divided by the window. It's a real limit of the test, and a wider range would raise ceilings. SPAN does this, for dimension-bearing targets only. It didn't help: RHO 0-0.39 bits.
- **Numerics.** matmul warnings are the known Accelerate build artefact (RF5); K3 checks hits exactly.

## Checks and twins
K1 winner arithmetic pass. K2 depth-2 count 59 = hand count; my first hand count in the script said 58, it forgot x/x, the code was right. K3 exact 10 = histogram 10. K4 bits arithmetic pass. K5 peak RSS 2.3 GB, one thread, nice 19; the runs take seconds. Rerun byte-identical, calibration JSON and all of `runs/`. A first calibration rerun differed only on a stored RSS, which I moved out of the JSON. **MUTATE: fails C2 as frozen**, though its gate 5 label doesn't change, since the real one is already DOES NOT CERTIFY. PLANT recovered, above.

## What this leaves
1. The port answers its own question: **on these targets the a0 procedure has no resolving power**, chiefly because K, D, f_Q are known to 16-25 %, and a window that wide has at most 2-3 bits to give. XR at 2.7 % has 5.4 at most.
2. The record's a0 certification needs a repair by its owner: Gate A's unit mismatch, and a decision on whether a0 is held to the FDR line at all.
3. A sharper target would be the only way to change this. I name it and don't run it: k to about 1 %, or D at one radius, needs HSE and lensing masses to agree, which GM1 and UX3 say they don't.

kappa = 1/2 FITTED. Not theory closed.
