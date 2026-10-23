# X2_cluster_outskirts: does F1's "any added cold profile that fixes MID overshoots the outskirts" survive?

Criteria: `FROZEN_CRITERIA.md` (committed alone, 40624db7e9; amendments A1–A3 below). Inputs and classes:
`ASSUMPTION_LEDGER.md`. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. No dark-matter particle. Not
"theory closed". Nothing here says the data favour the framework.

## Verdict (frozen classes; JSON keys in `x2_cluster_outskirts_results.json`)

- **V1 (`V1`): OVERSHOOT WEAKENED BY (e).** The test is a central point mass added Newtonian (PN), solved to bring A_MID to 1.
  For any added component with ρ(r) ≥ 0 non-increasing, πR²ΔΣ is non-decreasing in R. PN therefore adds the least outer
  signal any such component can, so it is the lower bound on the overshoot.
  - **At F1's PRIMARY (C0), PN overshoots in all 4 cells.** A_OUTER is 0.77–0.82, Z_OUT −2.34 / −2.69 (canonical, h 0.672 /
    0.686) and −3.13 / −3.55 (alt) (`rows."C0 (F1 PRIMARY)".PN.boost`).
  - **It still overshoots after (a1), (c1) or (d) alone.**
  - **Propagating the null-test systematics (e) splits it** (`V1_statuses`). At the corrected baseline C*, Z_OUT(PN) is −1.82 /
    −1.99 (canonical) and −2.42 / −2.61 (alt).
  - **The clipped-boost convention gives the same class** (`V1_clip`). The class is not BOOST-DEPENDENT.
  - **The sentence is strongly shape-dependent.** F1's own shape (dust tracing the gas and sourcing AQUAL) reproduces F1's
    needed 1.77 × gas and gives A_OUTER 0.58, Z −5.7 to −9.1, χ² 38–72 (`needed_shapes`). PN's profile χ² at C0 is only
    6.3 / 10.9 / 9.3 / 15.0: in 3 of 4 cells it is under the 11.07 line, although its OUTER band sits 2.3–3.6σ low.
- **V2 (`V2`): A FIXED-FORM COMPONENT PASSES (K-DEB-rule, K-DEB-committed).** This is CFG949's debris in CFG949's own reading
  B0: Newtonian baryons plus debris, with **no law at cluster scale**. It passes in all 4 cells with (e) and with the clipped
  boost; only K-DEB-rule also passes without (e). The FPS form fails, and so does the debris added to the law. Caveats follow
  below.
- **V3 (`V3`, `Z_MID_Cstar`): the core excess is WEAKENED with all systematics** (Z_MID 2.70 / 2.58 / 2.32 / 2.24). Without
  (e) it **SURVIVES** (5.43 / 6.05 / 4.66 / 5.25; `V3_nosys`).
- **V4: the outskirts anchor.** At C*, A_OUTER is 0.932 ± 0.119 / 0.931 ± 0.115 (canonical) and 0.853 ± 0.109 / 0.852 ± 0.105
  (alt). That stacked value averages light clusters lying **below** the law with heavy ones lying **above** it (terciles).

## Step 0: same data, same code

- **Replay R1/R2 (`x2_replay.out`).** The replay reproduces F1's measurement cache exactly: all 326 clusters, D, E, den and
  den_r, max |Δ| = 0 (sha256 961ea4fc…e720). It reproduces F1's cross-shear cache exactly too.
- **R3.** The reduced-shear series matches the exact source average to 1.3e-7. **R4:** 0.657 GB (final run).
- **K0.** C0, built from F1's functions exec'd from its source, reproduces F1's PRIMARY A_MID / A_OUTER / σ to 0.0 in all 4
  cells. My model equals F1's `predict()` to 0.0. The law's χ² is 33.4 / 41.8 / 27.3 / 34.9, against H2's printed 33.4 / 41.8 /
  27.3 / 34.9 (max |Δ| 0.04).
- **K8.** The cross-shear offset reproduces F1's MUTATE PRIMARY h0672 exactly: 0.2093 / 0.1923.
- **K6.** CFG949's R930 debris on CFG687's inputs gives B0 A_MID 1.0105 ± 0.063 and A_OUTER 1.0460 ± 0.089 (record: 1.011 / 1.047).

## Step 1: one change at a time (A_MID ± σ / A_OUTER / profile χ² / Z_OUT of PN)

Keys: `rows.<label>.boost.<foot>|<h>.{MID,OUTER}.{A,s_jk,s_tot}`, `.chi2`, `rows.<label>.PN.boost.<cell>.Z_OUT`.

| change | canonical h 0.672 | alt h 0.672 | canonical h 0.686 | alt h 0.686 |
|---|---|---|---|---|
| C0 F1 PRIMARY | 1.676±0.121 / 0.950 / 33.4 / −2.34 | 1.540±0.111 / 0.870 / 27.3 / −3.13 | 1.720±0.115 / 0.949 / 41.8 / −2.69 | 1.580±0.106 / 0.869 / 34.9 / −3.55 |
| (a1) CFG814 r⁻³ beyond 2.2 R500 | 1.671 / 0.940 / 33.3 / −2.45 | 1.536 / 0.862 / 27.4 / −3.25 | 1.715 / 0.939 / 41.8 / −2.81 | 1.575 / 0.861 / 35.1 / −3.67 |
| (a2) bracket F | 1.671 / 0.941 / 33.3 / −2.44 | 1.536 / 0.862 / 27.4 / −3.24 | 1.715 / 0.940 / 41.8 / −2.80 | 1.575 / 0.861 / 35.1 / −3.67 |
| (a3) bracket r⁻³ from R500 | 1.632 / 1.029 / 35.9 / −1.41 | 1.499 / 0.942 / 28.4 / −2.12 | 1.675 / 1.032 / 44.9 / −1.63 | 1.538 / 0.945 / 36.2 / −2.40 |
| (c1) EFE noclu (y_e 7.8e-4 / 6.5e-4) | 1.673 / 0.946 / 33.3 / −2.38 | 1.537 / 0.867 / 27.3 / −3.17 | 1.717 / 0.945 / 41.7 / −2.73 | 1.577 / 0.866 / 34.9 / −3.59 |
| (c1-loc) local-mass transplant | 1.681 / 0.954 / 33.7 / −2.30 | 1.545 / 0.874 / 27.5 / −3.09 | 1.725 / 0.953 / 42.2 / −2.65 | 1.585 / 0.873 / 35.2 / −3.50 |
| (c2) EFE maxclu (6.4e-3 / 5.3e-3) | 1.659 / 0.952 / 33.5 / −2.28 | 1.524 / 0.873 / 27.2 / −3.05 | 1.702 / 0.952 / 42.2 / −2.61 | 1.564 / 0.873 / 35.0 / −3.45 |
| (c3) EFE P2 catalogue | 1.676 / 0.949 / 33.4 / −2.35 | 1.539 / 0.870 / 27.3 / −3.14 | 1.720 / 0.948 / 41.8 / −2.70 | 1.580 / 0.869 / 34.9 / −3.55 |
| (d) reduced shear | 1.645 / 0.941 / 31.9 / −2.37 | 1.509 / 0.862 / 25.9 / −3.18 | 1.690 / 0.941 / 40.1 / −2.72 | 1.550 / 0.861 / 33.4 / −3.59 |
| (e) systematics | 1.676±0.242 / 0.950 / 22.4 / −1.72 | 1.540±0.223 / 0.870 / 21.0 / −2.30 | 1.720±0.271 / 0.949 / 13.1 / −1.89 | 1.580±0.249 / 0.869 / 14.3 / −2.49 |
| **C\*** = C0 + a1 + c1 + d + e | 1.640±0.237 / 0.932 / 21.7 / −1.82 | 1.505±0.218 / 0.853 / 20.6 / −2.42 | 1.684±0.265 / 0.931 / 13.1 / −1.99 | 1.545±0.244 / 0.852 / 14.6 / −2.61 |
| C* without (e) | 1.640±0.118 / 0.932 / 31.8 / −2.48 | 1.505±0.108 / 0.853 / 26.0 / −3.29 | 1.684±0.113 / 0.931 / 40.2 / −2.84 | 1.545±0.104 / 0.852 / 33.6 / −3.72 |
| C* with (a3) | 1.606 / 1.023 / 20.6 / −1.03 | 1.473 / 0.936 / 18.0 / −1.56 | 1.649 / 1.026 / 11.7 / −1.13 | 1.513 / 0.939 / 11.2 / −1.68 |

**(a) The measured slope.**
- **CFG814's prescription does almost nothing.** It steepens at r200m = 2.2 R500, which is about 1.7 Mpc, and the gas is still
  cut at 3 Mpc. The gas beyond R500 inside 3 Mpc goes from 0.76 to 0.74 of the budget, and A_OUTER moves by −0.01.
  - A_OUTER *falls* because removing gas at 1.7–3 Mpc lowers Σ(R) along the line of sight there.
- **Only steepening at R500 (a3) moves OUTER (+0.08).** That bracket is not the record's prescription. F1's on-disk X-COP
  median gives M_gas(<x) ∝ x^1.03 out to 1.64 R500, which is not r⁻³ there.

**(b) Terciles (`terciles.C0|C*.T1..T3`).** Catalogue Mgas500 medians are 3.3e12 / 1.17e13 / 2.92e13 M☉. At C0, canonical
(alt) at h 0.672:

| tercile | A_MID | A_OUTER |
|---|---|---|
| T1 | 1.12 (1.02), no core excess | 0.50 (0.46), Z −2.3 (−2.8) |
| T2 | 1.88 (1.73) | 0.78 (0.72) |
| T3 | 1.89 (1.74) | **1.40 (1.28), Z +3.8 (+2.9)** |

- The PN overshoot holds in T1 and T2. It is **absent in T3**, where the outskirts also lie above the law.
- At C*: T1 NONE, T2 OVER, T3 NONE (`V1_tercile_statuses`).
- "A_OUTER ≈ 1" is therefore a cancellation, the CFG687 T2 pattern (0.57 / 0.96 / 1.38).

**(c) The external field** moves A by ≤ 0.017, and by ≤ 0.004 for noclu. The local-mass transplant bracket is within 0.008.
Every record field is a galaxy-environment value, and none is measured at these clusters.

**(d) Reduced shear** raises the model by a median of 1.7 % in MID and 0.8 % in OUTER (max factor 1.147, median κ 0.018), so
A_MID falls by 0.03.

**(e) Systematics.**
- **The cross shear dominates (`rows.<label>.boost.<cell>.MID.A_x`).** In MID it is +0.19 to +0.24 in A units, ≈ 1.7–2.1σ. In
  OUTER it is +0.07 to +0.08.
- **Random-minus-random is small:** MID −0.01 to −0.05, OUTER −0.003 to +0.023. CFG687's 2.2σ OUTER R−R does **not** recur
  with F1's randoms.
- **Adding them in quadrature roughly doubles σ_MID.** This is conservative: the cross-shear stack is mostly shape noise.

## Shapes at the needed amount (reported, not graded; `needed_shapes`)

| shape | λ needed (C0) | A_OUTER (C0) | Z_OUT (C0) | χ² (C0) | A_OUTER / Z_OUT at C* |
|---|---|---|---|---|---|
| GS, dust ∝ gas sourcing AQUAL (F1's) | 1.772 / 1.390 × gas (canonical / alt, h 0.672) | 0.556–0.576 | −7.8 to −9.1 | 51–72 | 0.56–0.58 / −5.7 to −6.3 |
| PS, point mass sourcing AQUAL | 0.89–1.25 × Mgas500 | 0.72–0.77 | −3.2 to −4.4 | 8.9–18.8 | 0.72–0.77 / −2.4 to −3.2 |
| PN, point mass Newtonian (graded) | 2.17–2.78 × Mgas500 | 0.77–0.82 | −2.3 to −3.6 | 6.3–15.0 | 0.76–0.81 / −1.8 to −2.6 |

## Step 2: fixed-form components on C* (`components.<name>.rows.boost.<cell>`; pass line χ² ≤ 11.07, |Z_MID|, |Z_OUT| ≤ 2)

| component | A_MID (h 0.672 / 0.686) | A_OUTER | χ² with (e) (stat-only) | A_INNER | pass |
|---|---|---|---|---|---|
| **K-DEB-rule** (CFG949 B0, supply from C* gas; footing-independent) | 0.899 / 0.932 | 1.001 / 1.010 | 2.7 / 3.7 (8.1 / 6.6) | 0.56–0.57 | **yes**: with (e), clipped, and stat-only |
| **K-DEB-committed** (supply from β = 2/3 gas) | 0.857 / 0.886 | 0.953 / 0.958 | 4.2 / 4.0 (11.8 / 9.4) | 0.54–0.55 | **yes** with (e) and clipped; **no** stat-only (Z_MID −2.36, χ² 11.8) |
| K-DEB+law (C* law + debris) | 0.59–0.64 | 0.49–0.52 | 57–86 (189–232) | 0.44–0.46 | no: overshoots both bands |
| K-FPS (Eq. 17, η 8.51, r_c 0.43 Mpc, sources AQUAL) | 0.66–0.74 | 0.53–0.58 | 35–56 (93–153) | 0.63–0.70 | no: overshoots both bands |
| Milgrom 2008 CBDM | — | — | — | — | not tested (no fixed published form) |

- Debris medians: M_ta 4.5e14 (rule) / 5.0e14 (committed) M☉, f_ret 0.90, c 23, r_s 0.23 Mpc, r_b = r_ta 5.4 Mpc.
- FPS's missing mass inside 0.5 Mpc has a median of 2.9e13 M☉, about η e^{−r/r_c} ≈ 3–8 × the gas. It then also sources
  phantom mass.

## Against the record (suggested fixes; no other file edited)

1. **MAP §1.A.1 / §3.** The measured slope cannot be the OUTER anchor's weak point. With CFG814's own steepening radius, the
   share of the gas budget that lies beyond R500 (78 % in CFG949, 76 % here) only drops to 74 %.
   - The anchor's real fragility is the **tercile cancellation**, plus the R500 steepening bracket (a3).
   - Suggest rewording "OUTER ≈ 1 rests on the β = 2/3 gas" to "rests on the tercile mix and on where the steepening starts".
2. **MAP §3 / F1 / THEORY_V3_DRAFT §3.** "Any added cold profile that fixes MID overshoots the outskirts" holds for components
   added to the law at C0 and after each data correction. It weakens to a footing split only under conservative systematics.
   - **CFG949 does not contradict it.** CFG949's pass is the B0 reading, which drops the law on cluster scales. Added to the
     law, the same debris overshoots ×1.6–2.0 (K-DEB+law).
   - CFG727 (law on the retained part plus free cold) was not re-run here.
   - Suggest: "for any monotone component added to the law (Newtonian, point-mass bound), OUTER is overshot by 2.3–3.6σ in
     jackknife errors (1.8–2.6σ with null-test systematics); not in the heaviest tercile".
3. **"Z ≈ +5–6" for the core excess is jackknife-only.** The cross-shear MID offset (1.7–2.1σ) is the largest unpropagated
   systematic. With it, Z_MID = 2.2–2.7. Suggest stating both.
4. **CFG687 M2's OUTER R−R +0.13 (2.2σ)** is not reproduced with F1's randoms (−0.003 to +0.023).
5. **The PN profile χ² passes 11.07 in 3 of 4 C0 cells.** The band-Z and profile-χ² readings of "overshoot" differ.

## Amendments

- **A1 (PRE-RESULT, implementation).** The reduced-shear series goes to 6th order with moments m₂…m₈, because the 4th order
  could not meet R3's 1e-6.
- **A2 (POST-RESULT for R4 only).** Replay RUN1 reproduced F1 exactly but failed R4 at 1.126 GB macOS ru_maxrss. It is kept as
  `x2_replay_RUN1_rss.out` / `_results_RUN1_rss.json`. The memory maps are now reopened every 15 clusters. RUN2 gave R1–R4 PASS
  at 0.662 GB (final re-run 0.657 GB), with byte-identical npz content (same sha256 8d473764…). After the runs, the replay's "wrote" line was changed
  to print the file name instead of an absolute path, and the replay was re-run for the committed `x2_replay.out`. In the kept
  RUN1 file that path was redacted by hand; this is marked in the file.
- **A3 (solver cap).** It was written after a development run had printed the C0 / (a1) / (a2) rows, and before any (c) row was
  seen. The EFE solves use maxit 3000 (F2's 300 stopped short of 1e-9); every solve now converges to ≤ 1.0e-9. That
  development run (old cap, outputs overwritten) gave the same numbers to 3 decimals.
- **Reporting-only edit after the development run.** The null-offset printout block was added; no graded logic changed.

## Checks

- **Replay: 4/4 PASS.** The replay MUTATE (e2 sign flipped, 20 clusters) fails R1/R2 as required.
- **Analysis: 9/9 PASS** (K0, K2–K9, with K1 the recorded shas), 365 s, 0.447 GB.
- **MUTATE: 6/9.** Cross shear as the data, the EFE ratio inverted, and the reduced-shear sign flipped make K0, K4 and K5 FAIL,
  as frozen.

## What this does not show

- **No external field measured at eRASS1 clusters.** Every field used (Chae+21 SPARC environments, P2 GAMA galaxies) is a
  galaxy-environment estimate. The EFE transplant from a point-mass solve is approximate (its local-mass bracket is within
  0.008).
  - The floored projector drops the 9–15 % of far-grid cells where the EFE effective density is negative. That is a far-field
    effect and is not quantified separately.
- **(e) is a conservative allowance, not a measured systematic.** A smaller propagation would leave V1 at OVER and V3 at
  SURVIVES (see "C* without (e)").
- **The K-DEB "pass" is CFG949's untethered reading H-UT, not the law plus a component.**
  - It needs a selector that untethers clusters but not galaxies; CFG939 found it not derivable.
  - It uses the NFW form and C = 3000 as conventions, and it over-predicts INNER ×1.75 (A_INNER 0.56).
  - Only CFG949's primary corner was tested. CFG949 itself is FRAGILE (6 of 40 corners), and it over-predicts ACCEPT.
  - It does not test a₀ or κ.
- **FPS was fitted on 16 massive CLASH clusters** (gas 0.8–5.3e14 M☉) and is applied here unchanged to clusters ~10× lighter.
  The form and parameters are a PROVISIONAL web lookup.
- **Not solved here:** asphericity (AQUAL ≠ QUMOND), the n(z) calibration (F1's C5d bound), member dilution (the boost sign,
  F1 A1; both conventions reported), and terciles under the components.

## Files and runs (`OMP_NUM_THREADS=1 nice -n 15`)

| file | what |
|---|---|
| `x2_replay.py` → `.out`, `_results.json`, `x2_replay_percluster.npz`; `_MUTATE.*`; `_RUN1_rss.*` | replay of F1's measurement |
| `x2_cluster_outskirts.py` → `.out`, `_results.json`; `_MUTATE.*` | steps 0–2 and the verdicts |

- Run the replay as `x2_replay.py <F1 KiDS column cache from f1_extract.py> <dir with f1_meas.pkl and f1_meas_MUTATE.pkl>
  [--mutate]` (~7.5 min).
- Run the analysis as `x2_cluster_outskirts.py [--mutate]` (~6 min).
- Read-only inputs: F1's source, results and MUTATE JSON; H2's printed χ²; F2's `f2_aqual.py`; CFG949's `cfg949.py` (R930
  block); CFG654 tables; CFG687's npz; the Chae+21 CSV; the eRASS1 FITS. Nothing was downloaded.
