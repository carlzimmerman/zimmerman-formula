# CU1_gas_term_replication: FROZEN CRITERIA, committed alone before any script or number of this lane

**Question.** Does g = law x (1 + k g_gas/a0) give the numbers claimed for it when built again from raw inputs, without the code or README of the lanes that made the claim? Owner's go, 2026-11-02. A replication of a claim, not a new rule. kappa = 1/2 FITTED. Cold sector stays retired; no result here reinstates it. No dark matter particle. Nothing here says the data favour the framework. Not theory closed. Footings never pooled.

**Not blind.** Read before this freeze: the claimed numbers in the brief (k about 13.3 canonical, 14.3 alt; canonical 14 of 15, G-OUT-all -2.71, G-OUT-M3 +0.58, joint p 0.38, X-COP all 7 -0.016, rms 0.089; alt 10 of 15; law alone 10 of 15, M3 +4.76, X-COP +0.467); FG1's criteria; LW1's criteria and README head; CRG1's README and SPEC sections 4.1-4.6, A5-A10; BA1's criteria; the project memory index and recent commit subjects, including UX7's subject line, which names local gas F1 and "13 of 15". **Not opened, until my numbers are committed:** UX3_cluster_gas_term, UX7_gas_term_shape, UX6_gas_term_bullet and their scripts. After that, UX3's README only. CRG1's `v1/` code and LW1's scripts are not read either: the implementation is written from the written definitions.

## Inputs
`CRG1_clean_room_regrade/inputs/` (`clusters/`, `xcop/`, `scalars.json`) against its MANIFEST sha256. Definitions: SPEC 4.1-4.3 (selection, measured chain, projection, keys, "one template" for the four outer mass keys). EFE table C(s): the given `efe_table_<foot>.npz`, not solved anew (disclosed limit; the machine is overloaded).

## The model, fixed before any number
- Law: M_law(r) = M_b nu(y), nu = 1/2 + sqrt(1/4 + 1/y), y = G M_b/(r^2 a0). a0 canonical 9.3603e-11, alt 1.1312e-10.
- Term: M_src(r) = M_law(r) (1 + k g_gas/a0), g_gas = G M_gas(<r)/r^2. Gas only, no stars. a0 is the same footing's.
- X-COP: M_gas = li(gas), M_b = li(gas) + li(stars), X-COP's own measured profiles, not scaled. Rows x in (0.1, 0.2, 0.3, 0.5, 0.7), all <= 0.75. d = log10(M_HSE/M_src). X = mean d, rms = sqrt(mean d^2).
- Shear keys: SPEC 4.2 measured chain at f* 0.034, gas +0.005, h 0.672 and 0.686. M_b = capped M_bx, M_gas = M_b/(1+f*), so the gas stops at r_ta as M_b does. C* normaliser unchanged by k.
- The fit: k minimises sum d^2 over the 20 rows of sorted-name positions 0, 2, 4, 6, per footing. Sort is Python's on the directory names. Unweighted, no HSE error used. Brent on k in [0, 100].

## Fit readings I can't settle from the brief
PRIMARY as above. Reported, not graded: k with mean d = 0 on the same rows (R2); linear least squares in M_HSE/M_law - 1 against g_gas/a0 (R3); gas not capped at r_ta on the shear side (R4). If a reading moves the count of passing keys, I say so.

## Step 0: the gate. k = 0 must give the law
Canonical, f* 0.034, gas +0.005: **10 of 15, G-OUT-M3 +4.76 at h 0.672, X-COP +0.467**, with tolerances |dZ| <= 0.02, |dX| <= 0.002. Also compared, not gated: M3 +4.26 at h 0.686, G-MID-T3 +4.86, joint chi^2 65.0, X-COP rms 0.476, alt M3 +3.99, +3.51, alt X-COP +0.434, 0.444. **If the gate fails, I look for a bug once, disclose it, and if it still fails I stop and report NOT REPRODUCED AT THE LAW; no k is fitted.**

## Step 1: the grade
Per footing, per k: all 15 Z at both h, passing if |Z| <= 2 in both h; G-OUT-M3, G-OUT-all; X-COP on all 7 and on the held-out 3 (positions 1, 3, 5) and fit 4 apart. Joint chi^2 by BA1's definition: R from 2,000 common bootstrap draws of the 326 clusters on measured keys, C = R s s, modes with eigenvalue >= 1e-3 of the largest, p from chi^2(dof); headline the worse h. R recomputed on each footing. BA1 builds R at canonical; I use each footing's own and say so. X-COP's line: |mean| <= 0.05 and rms <= 0.10.

## Step 2: commit, then compare
My numbers are committed with their sha256 before UX3's README is opened. Then line by line, each claim labelled:
- **MATCH** |dk| <= 0.2, |dZ| <= 0.05, |dX| <= 0.002, |dp| <= 0.02, count equal
- **CLOSE** |dk| <= 0.5, |dZ| <= 0.20, |dX| <= 0.01, |dp| <= 0.05, count equal
- **DISAGREE** otherwise, or any pass/fail label flip on a key.

**Verdict.** REPRODUCED: all brief claims (k both footings, canonical count, G-OUT-all, G-OUT-M3, joint p, X-COP mean, rms, alt count) MATCH or CLOSE and no key flips. PARTLY REPRODUCED: one or two DISAGREE, none of them a count. NOT REPRODUCED: otherwise. If a DISAGREE is caused by a fit reading, I show it under both readings and the verdict stays on the primary. Reproduced means the numbers follow from the definition. It does not mean the term is physically right, and the fit sample overlaps the graded X-COP row.

## Step 3: stress
- **Bootstrap over clusters.** k on the 4 fit clusters (all 35 multisets, multinomial weights) and on all 7 (2,000 draws, seed 20261102, whole clusters).
- **Leave-one-out.** Of the 4, and of the 7. Every 4-of-7 split (35) with the 3 held out: how k and held-out X move.
- **Propagation.** Grade keys on a k grid spanning all of the above, on both footings. Z(k) per key interpolated. From each bootstrap's k distribution: 16-84 % on G-OUT-all, G-OUT-M3, and joint p, the probability of each pass count, and the probability of 15 of 15, of at least 14. Z_k = dZ/dk x sigma_k, stated per key, stat error only otherwise.
- **Passing-window.** The k interval, per footing, over which each key passes, and the intersection for the most keys. Reported, no k is picked from it.

## Checks
K1 inputs against MANIFEST sha256 and sizes: 326 clusters, 106 KT, 35 X-COP rows. K2 analytic projection: an isothermal sphere's Delta Sigma from my projector, within 1 % across 0.15-3 Mpc. K3 k-limit: k = 0 equals the law to 0 in V; and doubling M_src doubles V before f_red. K4 joint: R = I reproduces sum Z^2 exactly. K5 rerun of the grade byte-identical. **MUTATE** (nu set to 1, separate outputs): Step 0's gate must fail, exit 1. Every failed check is reported.

One thread, nice 15, under 4 GB, short jobs. No downloads, no pushes, no edits to other lanes.
