# RG1_native_n_regrade: native N costs the Local Group. All five classes now fail, where the floor had four of five. Milky Way keeps its class; SLUGGS improves but fails; X-COP on the S rule fails worse

Criteria: `FROZEN_CRITERIA.md` (bb631b8e9d), committed before any script or number from this regrade. Scripts: `rg1_rule.py`, `rg1_lib.py`, `rg1_dwarfs.py`, `rg1_mw.py`, `rg1_held.py`. κ = ½ FITTED. Halo footings coincide. Not "theory closed". Nothing here says the data favour the framework. One deviation: `rg1_held.py`'s HO1 patch anchor failed twice on a source string that occurs twice; fixed with no number having been produced by HO1's part. HO2's part ran once.

**RG1 line: FAILS on P1, P3, P4, P5. P2 stays FEASIBLE (WIDE PRIORS ONLY).** These are failures of this rule, not closures.

| part | source result | native N | line |
|---|---|---|---|
| **P1 Local Group** (X49, EM1's M200) | floor: 4 of 5 REPRODUCED | **0 of 5** | see below |
| **P2 Milky Way box** | GD3: WIDE PRIORS ONLY, 5 cells, R_d 1.93 | **FEASIBLE (WIDE PRIORS ONLY)**, 7 cells, R_d 1.93–2.27; B: 5 cells | no in-prior cell; best in-prior D 2.53 |
| P2 McMillan 2017 baryons | GD3 V_c 201.7 | V_c 202.8 against Eilers 229.1 ± 4.6, z −5.6; K_z 67.9 passes | ΛCDM-PROCESSED input |
| **P3 SLUGGS** | CL2 +0.152, 1 of 4; X38 +0.197 | **+0.125**, Zc +6.1, 1 of 4: **FAILS** (IMPROVES needs ≤ 0.099 / 0.091) | S 1.8–2.0 Σ_a0 |
| **P4 X-COP, S rule** | CL2 −0.002 / 0.126 FAIL | **−0.186 / 0.214: FAIL (mean + rms, OVER)**; −0.02 at x 0.1, −0.19 to −0.24 beyond | see below |
| **P5 HG2 groups** | D +0.229 FAIL | **D +0.311: FAIL (ABOVE)**; underpowered on residuals, power as HO1 | measured [−0.511, −0.076] |

**P1, E (Z), canonical:**
| rule | MW ultra-faint (31) | bright M31 (25) | M31 others (5) | MW classical (8) | LG field (13) |
|---|---|---|---|---|---|
| floor, Burkert (K1 = X49) | +0.476 (+3.80) | +0.176 (+1.70) | +0.571 (+1.71) | +0.125 (+0.91) | −0.034 (−0.49) |
| **native N, smooth** | **+0.758 (+6.63)** | **+0.390 (+3.29)** | **+1.006 (+3.08)** | **+0.627 (+4.92)** | **+0.338 (+3.58)** |
| native N, Burkert | +0.866 (+7.74) | +0.501 (+4.16) | +1.121 (+3.45) | +0.712 (+5.35) | +0.437 (+4.51) |

All are UNDER: too little central mass. Fair-share M200 doesn't help (+0.51 to +1.29, all Z > 3.8). ND1's free-M200 read of the same rule agrees for four of five classes.

**How hard to read P1.** EM1's M200 relation is carried 3–6 dex below its SPARC fit, with median lg M200 5.7–8.4; S comes from a rule whose lowest zoom is 1e10. Those extrapolations favour neither side by design, but they are large. The floor's 4 of 5 was also a hand-set S. So: the measured collapse rule, extrapolated, does not reach Local Group dwarfs; it doesn't show what happens with a measured low-mass S below 1e10.

**How hard to read P4.** The failure is the S(z_f) rule, not the native halo. ZN3's native z = 0 profile, with no S or r₀, passes X-COP (−0.004 / 0.076) and 15 of 15 keys on X-COP's gas, and gets 11–12 of 15 on eRASS1's own gas. So in clusters the working rule's S form over-predicts and native z = 0 does not. That is a reason to read the cluster side of version N as ZN3's profile. **That is a recommendation, not done here.**

**P2 is not a clean framework verdict:** X5's baryon box and McMillan carry the halo-fit caveats in THEORY_PROGRESS_SUMMARY_2026-10-31.

**Checks.** K0 table to ND1's S: max 0.16 %. K1 floor + Burkert = X49: max |d| 0. K2 OS1 + q_fS = GD3's class and best D: PASS. K3: HO2 copy 9/9 with Step 0 and CL2 row. K4: HO1 copy 9/9 with Step 0. MUTATE (S × 0.5): dwarfs rise +0.18 to +0.23; Milky Way falls to V+K ONLY, D 0.86 → 3.14. SLUGGS, X-COP, HG2 have no mutate twin: their source checks ran instead.

**Carried, not rerun:** SPARC line passes, Υ 0.70 / 0.72; groups Z +1.45 (NF1, X80). LITTLE THINGS +0.138 short; ceilings fail (ND1).
