# CFG963: what carries the native shear pass? **The gas expulsion M3, not the cold-sector rules (M3-CARRIED, both footings, every bracket)**

**Plain summary.**
1. The theory-v2 engine beats its plain-gravity control NCS0 on raw KiDS-1000 (Δχ² −10.08 canonical, −9.39 alt). NCS0 does not apply the census gas expulsion M3; the engine does.
2. A control made of plain gravity plus the same gas expulsion (NCS0 × T_M3, with T_M3 measured from the matched 1024³ pair T1x / T12) scores −11.87 against NCS0. That is 118% (canonical) and 126% (alt) of the engine's lead, and the engine then scores +1.78 / +2.47 against it.
3. The cold-sector rules alone (M1+M2) add 0.5–2.6% power and cost +2.66 against plain dust, so the attribution class is **M3-CARRIED on both footings and in all four M3 brackets**. The transfer method closes: −10.21 / −9.51 against the stored −10.08 / −9.39.
4. So the shear pass says two things: "the capped cold sector does not overproduce structure (unlike CFG596's +68.7)" and "gas expulsion lowers power". It is **not** a preference for the framework's law over plain gravity with feedback, and KiDS cannot tell the two apart at this power.
5. The decisive 1024³ control NCS0+M3 is designed but not run (`FROZEN_CRITERIA_1024_DRAFT.md`, about 9–11 h at about 44 GB). Against this feedback-matched control CFG960's SCT-M run SC1x gets worse: EXCLUDED at +55.9 to +59.0, against +47.28 vs NCS0.

- **Date:** 2026-10-21 (criteria and frozen scoring); 2026-10-23 (amendment A1, README). Agent lane, block 960–969.
- **Commits:** criteria `FROZEN_CRITERIA.md` d3b18181c (committed alone, before any script or number); frozen scoring f2354ed22;
  `AMENDMENT_A1_2026-10-23.md` 64718930a (committed alone, before its numbers).
- **Status:** DIAGNOSTIC attribution, reported only, **no verdict weight**. CFG654 A2/A3 (NC1x / NC2x HOLD vs NCS0) stand as frozen.
  This lane changes how that pass is read, not its class.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Raw KiDS-1000 / DES Y3 data, framework-native scoring (the
  frozen CFG654 native scorer, sha256 e5e3da3b…). No HMcode, BAHAMAS or ΛCDM yardstick anywhere. Cold energy mass required. Not
  "theory closed". A CONSISTENT class does not mean the data favour the framework.
- **Process:** scoring and arithmetic only, no PM run. One process at a time, one thread, nice 10, in-script RSS guard at 0.95 GB (peak
  0.26–0.30 GB), memory pause below 3 GB free + inactive.

## 1. Facts from the code (read only)

- **NCS0 has no M3.** NCS0 = CFG654 launcher job `S0`, modules off, native_cmb inputs. In the engine's `forces()`, the S0 switch returns
  the plain Poisson potential φ_k = (−1.5 Ω_m / a) δ_k / k² before any module, census or footing code. So NCS0 has no MOND input, no
  settling source and no gas expulsion.
- **What M3 does.** `expel_m3` runs in every RES force call (dynamical steps and snapshots). It replaces the Newtonian source by
  δ + Σ_k [G_σk ∗ e_k − e_k], where e_k = f_b (1 − f_ret,census,k)(1 + δ) is the census non-retained baryon density on catchment class k and
  G_σk is a unit-mass Gaussian with σ = r_ON,k. Mass is conserved exactly. Only the source is moved; the particles respond through the
  changed potential, so back-reaction is inside the runs. The scorer reads the framework's gravitating spectrum P_grav, which
  contains the re-placement. The expelled gas is 3.2% / 3.7% / 3.7% of all mass at z = 0 / 0.5 / 1 in NC1x and NC2x.
- **M3's rule reads no footing.** f_ret comes from M_ta(r_ON, Δ_ta) and r_ON from the density field, so the footing enters M3 only through
  the evolved field. P_grav(T2x) / P_grav(T1x) is 1.002–1.008 at k ≤ 2.
- **On disk (all read only):**
  - 1024³ native: NCS0, NC1x, NC2x.
  - 1024³ inherited: P0 (S0), T12 (M1+M2), T1x / T2x (M1+M2+M3).
  - 256³ inherited: VLs (S0), V0 (all OFF), VM3 (M3 alone on the all-OFF engine), VM12, VM123.
  - 256³ native: VNcs, VNc12.
  - CFG646's static DIFF-S post-process of CFG596 P1.
  - Missing: no native 1024³ M1+M2 run, no alt M1+M2 run, and no M3 on the S0 engine.

## 2. Transfers (node by node at z = 0, 0.5, 1; T^grav at k = 0.3 / 0.5 / 1 h/Mpc)

| name | definition | z = 0 | z = 1 | role |
|---|---|---|---|---|
| **M3-1024** | P_grav(T1x) / P_grav(T12), 1024³ inherited | **0.967 / 0.947 / 0.919** | 0.964 / 0.930 / 0.881 | PRIMARY T_M3 |
| M3-256 | VM123 / VM12, 256³ | 0.973 / 0.950 / 0.924 | 0.967 / 0.933 / 0.881 | bracket R1 (resolution) |
| M3-alone-256 | VM3 / V0, 256³, all-OFF environment | 0.986 / 0.989 / 0.939 | 0.969 / 0.934 / 0.898 | bracket R2 |
| CFG646-R3 | CFG646 static DIFF-S (no back-reaction) | 0.977 / 0.966 / 0.950 | 0.971 / 0.950 / 0.924 | bracket R3 (A1) |
| M12-1024 | P_grav(T12) / P(P0), 1024³ inherited | 1.005 / 1.013 / 1.026 | 1.001 / 1.003 / 1.010 | PRIMARY T_M12 |
| M12-256n / M12-256i | VNc12 / VNcs; VM12 / VLs | 1.005 / 1.012 / 1.030; 1.005 / 1.014 / 1.031 | ≈ 1.000 / 1.001 / 1.003 | brackets |
| C1-can / C1-alt | P_grav(T1x or T2x) / P(P0) | 0.972 / 0.959 / 0.943; 0.974 / 0.965 / 0.949 | 0.965 / 0.933 / 0.890; 0.965 / 0.934 / 0.896 | closure control |

The dynamical M3 suppression at 1024³ is deeper than CFG646's static estimate (back-reaction). For comparison, NC1x / NCS0 itself is
0.972 / 0.961 / 0.949 at z = 0. M3 alone takes out more power than the whole engine does, because M1+M2 adds some back.

## 3. Controls

| control | result |
|---|---|
| K: re-implemented frozen scorer reproduces stored NC1x / NC2x vs NCS0 (every χ², Δχ², robustness, DESI, class, N_kept) and the MUTATE T-OWN χ² | **exact (max diff 0)** |
| MUTATE M0: T ≡ 1 surrogate vs NCS0 | **Δχ² = 0 exactly** (both surveys, all variants) |
| MUTATE M1: planted T ≡ 0.9 | **bites**: KiDS −20.24, DES −10.24 |
| Scorer MUTATE (NZ1 + T-OWN) on every scored pair | NZ1 bites on every pair × survey; KiDS T-OWN DIAGNOSTIC everywhere (16.0–22.9) |
| C1 closure: NCS0 × (T1x / P0) vs NCS0 against stored NC1x; NCS0 × (T2x / P0) against NC2x | **−10.21 vs −10.08 (diff −0.13); −9.51 vs −9.39 (diff −0.12): PASS** (tolerance ±2) |
| A1-K2: inherited T12 / T1x / T2x vs P0 re-scored from stored outputs | **+2.029 / −7.697 / −7.177, exact** (stored +2.029 / −7.697 / −7.177) |
| A1-K3: NC1x / NC2x vs a control-slot surrogate with T ≡ 1 | **−10.08 / −9.39 exactly** |
| A1-K4: reusable scorer, SC1x vs NCS0 × 1, against CFG960's stored score | **+47.28 exactly** (all fields, both surveys) |

## 4. Scores (KiDS-1000; Δχ² = framework slot − control slot; robustness widen2 / noIA / held / LOC)

| pair | N_kept | χ² control → framework | Δχ² | robustness | class |
|---|---|---|---|---|---|
| NC1x vs NCS0 (stored) | 108 | 154.76 → 144.68 | −10.08 | −6.13 / −13.78 / −8.75 / −12.74 | CONSISTENT |
| NC2x vs NCS0 (stored) | 108 | 154.76 → 145.38 | −9.39 | −5.69 / −12.85 / −7.99 / −11.86 | CONSISTENT |
| **S0+M3 [M3-1024] vs NCS0** | 108 | 154.76 → **142.89** | **−11.87** | −7.20 / −16.44 / −10.95 / −15.09 | CONSISTENT |
| S0+M3 [M3-256] vs NCS0 | 108 | → 143.40 | −11.37 | −6.80 / −15.82 / −10.44 / −14.51 | CONSISTENT |
| S0+M3 [M3-alone-256] vs NCS0 | 108 | → 144.68 | −10.08 | −5.97 / −14.01 / −6.93 / −12.84 | CONSISTENT |
| S0+M3 [CFG646-R3] vs NCS0 (A1) | 108 | → 146.10 | −8.66 | −5.26 / −11.97 / −7.80 / −10.93 | CONSISTENT |
| S0+M12 [M12-1024] vs NCS0 | 108 | → 157.42 | +2.66 | +1.65 / +3.66 / +3.06 / +3.28 | CONSISTENT |
| S0+M12 [256n / 256i] vs NCS0 | 108 | | +2.62 / +2.76 | | CONSISTENT |
| **NC1x vs S0+M3 [M3-1024]** | 107 | 142.83 → 144.61 | **+1.78** | +1.06 / +2.63 / +3.11 / +2.34 | CONSISTENT |
| NC1x vs S0+M3 [M3-256 / alone / R3] | 107 / 107 / 108 | | +1.28 / −0.02 / −1.42 | | CONSISTENT |
| **NC2x vs S0+M3 [M3-1024]** | 107 | 142.83 → 145.30 | **+2.47** | +1.49 / +3.56 / +3.86 / +3.21 | CONSISTENT |
| NC2x vs S0+M3 [M3-256 / alone / R3] | 107 / 107 / 108 | | +1.97 / +0.67 / −0.73 | | CONSISTENT |
| NC1x / NC2x vs S0+M12 [M12-1024] | 110 | 162.80 → 149.61 / 150.32 | −13.19 / −12.49 | | CONSISTENT |

- **DES Y3 (reported).** S0+M3 vs NCS0 −2.17, against NC1x −2.21 and NC2x −2.15, so DES says the same. Against S0+M3 the framework
  scores +0.27 / +0.43. DES is NOT DIAGNOSTIC there: T-OWN fails because the support mask keeps only 59–68 points.
- **Absolute fit.** Plain dust plus the framework's own gas expulsion fits KiDS as well as the framework engine, or slightly better
  (χ² 142.89 vs 144.68 / 145.38). The CFG909 caveat applies to every arm: Δχ² sizes are amplitude-driven.

## 5. Attribution (FROZEN_CRITERIA.md §6; KiDS; primary transfer M3-1024)

f = Δχ²(S0+M3 vs NCS0) / Δχ²(NCx vs NCS0); d = Δχ²(NCx vs S0+M3).

| footing | f (primary) | d (primary) | class (primary) | M3-256 | M3-alone-256 | CFG646-R3 (A1) | KiDS distinguishes? |
|---|---|---|---|---|---|---|---|
| canonical (NC1x) | **1.18** (self-consistent vs C1: 1.16) | **+1.78** | **M3-CARRIED** | f 1.13, d +1.28: M3-CARRIED | f 1.00, d −0.02: M3-CARRIED | f 0.86, d −1.42: M3-CARRIED | **no** (\|d\| < 4) |
| alt (NC2x) | **1.26** (1.25) | **+2.47** | **M3-CARRIED** | f 1.21, d +1.97: M3-CARRIED | f 1.07, d +0.67: M3-CARRIED | f 0.92, d −0.73: M3-CARRIED | **no** |

- f by robustness variant is 1.17–1.25 (canonical) and 1.25–1.37 (alt) for the primary, so no variant changes the reading.
- **Alternative attribution:** f_M12 = −0.26 (canonical) / −0.28 (alt). The cold-sector rules move the score the wrong way, and
  f + f_M12 = 0.91 / 0.98 (Δχ² is not additive; the gap is reported, not interpreted).
- **Inherited pipeline, real runs on the same ICs (A1-K2):** S0 → T12 (adding M1+M2) gives +2.03; T12 → T1x (adding M3) gives −9.73.
  The same decomposition holds without any surrogate.

## 6. Plain consequences for the owner

- **M3-CARRIED, both footings, all brackets.** In plain terms, the native shear pass says:
  1. the framework's capped cold sector does not overproduce structure (CFG596's uncapped engine gave +68.7; theory-v2's cold-sector
     rules cost only about +2.7 against plain dust);
  2. gas expulsion lowers power, and the record's census expulsion lowers it by about the right amount for KiDS.
- It is **not** a preference for the framework's law over plain gravity with feedback. Against plain gravity plus the same
  expulsion, the engine is +1.8 (canonical) / +2.5 (alt) worse. That is within noise (|d| < 4 on every bracket), so **KiDS cannot tell
  the framework's cold sector from plain gravity plus gas expulsion at this power**.
- **The engine-parent problem is not load-bearing for the shear result.** Any parent that clusters like plain dust on k ≲ 1 h/Mpc
  (own boost within a few percent) and expels the census gas would pass. The shear tile therefore constrains a parent's boost budget,
  and the class-A relocation, RMIN and the global phantom (CFG941–952) are not what the pass rests on.
- **SC1x (SCT-M, CFG960 A2, reported only).**
  - The frozen reading comes first: KiDS **+47.28 vs NCS0, EXCLUDED**.
  - Against the feedback-matched control SC1x is worse: **+58.97** (M3-1024), +58.47 (M3-256), +57.18 (M3-alone), +55.94 (CFG646-R3).
    Every bracket is **EXCLUDED** (every robustness value ≥ 38.5).
  - Reading: SCT-M's capped cold sector over-produces structure relative to plain dust plus the same gas expulsion. SC2x was not run,
    so there is no alt statement.
- **Wording.** PAPER56 calls NCS0 the "matched control". It is matched in ICs, not in baryon expulsion. Re-wording published text is
  the owner's call; nothing was edited here.

## 7. What a fair control means for every future engine score (including the screened theory v3 / L1 khronon run)

- **Match the baryon physics in both arms.** If an engine includes the census gas expulsion M3 (or any baryonic expulsion), its
  KiDS / DES score against plain NCS0 contains a credit of roughly −9 to −12 (KiDS, the four M3 brackets) that belongs to the expulsion
  and not to the law. The law's own result is the score against a control with the same expulsion.
  - Today that control is the surrogate NCS0 × F_M3: `cfg963_reuse.py`, `score_vs_feedback_control(run, "M3-1024")`, with brackets
    "M3-256", "M3-alone-256", "CFG646-R3".
  - Decisively, it is the 1024³ NCS0+M3 run (draft below).
- **Report both, in this order:** the frozen score vs NCS0 first, then the score vs the feedback-matched control. An engine without
  expulsion is fairly compared with NCS0. Neither arm then has the gas physics the sky has, and that should be said.
- **What this means for how scores read:**
  - A pass vs NCS0 by an M3-carrying engine tells you only that its own boost does not overproduce structure. A lead vs NCS0 of about
    −10 is what M3 alone delivers.
  - A failure vs NCS0 by an M3-carrying engine is a stronger failure against the fair control (SC1x: +47 → +56 to +59).
- **Scale of what KiDS can resolve.** A cold-sector boost of +0.5 / +1.3 / +2.6% at k 0.3 / 0.5 / 1 costs about +2.7. Differences of a
  few percent in P(k) at k ≲ 1 are therefore within |Δχ²| < 4, and the CFG909 amplitude sensitivity applies to every arm.
- **Before any 1024³ run** of a new engine, a parent's predicted boost budget relative to plain dust can be scored in minutes. Pass
  its own P_grav / P_S0 as a transfer on NCS0 with this lane's framework-slot surrogate (`surrogate_F`), multiplied by F_M3 if the
  engine carries M3.

## 8. The decisive 1024³ control (DRAFT, not frozen, not queued)

`FROZEN_CRITERIA_1024_DRAFT.md`: switch `S0M3` in a lane-owned copy of the CFG654 engine. It runs the census refresh on the RES cadence,
`expel_m3` unchanged, and plain Poisson from the expelled source. There is no MOND input, settling, supply or cap, and no footing, so
one run serves both footings.

- **Inputs:** native_cmb ICs, seed 359.
- **Validation at ≤ 256³:** bit-for-bit S0 reproduction, an f_b → 0 null, mass conservation, and a 256³ check of the transfer.
- **Scoring:** the CFG963 wrapper, with the control slot reading the GRAVITATING spectrum.
- **Cost:** about 9–11 h wall time at 14 threads, peak 40–44 GB, about 0.7 GB of output. Estimated from NCS0's 7.9 h, NC1x's 9.2 h,
  and the T12 → T1x increment.
- **Queue:** only after CFG960's chain is done (its gate pattern does not catch a CFG963 engine) and with owner approval.
- **Optional:** the never-run native NC12 would complete the native factorisation.

## 9. Assumptions and limits (stated with the numbers)

- **Environment.** M3's fractional effect is measured on the M1+M2 background and applied to plain dust. M1+M2 changes P_grav by ≤ 3%
  at k ≤ 1, and the settled source changes by < 1% when M3 is added (CFG650: 0.357 vs 0.359). The real NCS0+M3 run removes this
  assumption.
- **Input set.** Transfers come from inherited-input runs and are applied to native_cmb NCS0. The C1 closure tests the whole transfer
  and holds to 0.13.
- **Footing.** The canonical T_M3 is used for alt.
- **Resolution.** None for the primary; R1 (256³) agrees.
- **Redshift.** No interpolation beyond the scorer's own.
- **k range.** Every scorer node from 0.080 to 8.04 h/Mpc carries a measured transfer; the 256³ / R3 transfers are held constant above
  2.01 h/Mpc.
- **Not an absolute fit, not a verdict.** All arms are mediocre absolute fits (χ² 143–155 on 108 points). DES is mostly not
  diagnostic. The CMB-lensing gate is outside this lane.

## Files

| file | role |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (d3b18181c, committed alone first) |
| `cfg963_attrib.py` → `cfg963_attrib[_MUTATE].out`, `cfg963_attrib_results[_MUTATE].json` | frozen-criteria scoring (MUTATE first) |
| `AMENDMENT_A1_2026-10-23.md` | dated amendment (64718930a, committed alone): K2–K4, bracket R3, SC1x |
| `cfg963_reuse.py` → `cfg963_reuse[_MUTATE].out`, `cfg963_reuse_results[_MUTATE].json` | reusable feedback-matched scorer (importable, writes nothing on import) + A1 items |
| `FROZEN_CRITERIA_1024_DRAFT.md` | DRAFT design of the 1024³ NCS0+M3 control (not frozen, not queued) |

## Disclosures

- Before the criteria, README numbers were seen (listed in the criteria's §1). Before amendment A1, the frozen result and the stored
  SC1x / T12 scores were seen (listed in A1). Neither changes the frozen class; A1's items are reported only.
- The first MUTATE pass (2026-10-21) was stopped by this lane after 4 pairs, to correct a printed column label (the k list had 6
  entries, the header named 5). It was rerun from scratch with the corrected script; no number differs.
- The frozen-criteria passes ran on 2026-10-21. The session then paused, and outputs were committed on 2026-10-23 (f2354ed22) with no
  rerun.
- The new-angles scout (NA-1) predicted this outcome from hand arithmetic ("the lead becomes a tie"). This lane's numbers come from the
  frozen scorer.
- Live heavy jobs were left alone. During A1 a 384³ khronon run was live; this lane stayed at ≤ 0.30 GB on one thread.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
