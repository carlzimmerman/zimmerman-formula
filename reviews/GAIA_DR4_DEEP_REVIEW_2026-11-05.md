# Gaia DR4 deep review, 2026-11-05 (review only; no frozen file edited, nothing fetched)

Gaia DR4 is due 2026-12-02 (ESA page, read 2026-11-04; provisional). Statistic: wide-binary boost gamma_v, Newton = 1.00.
kappa = 1/2 FITTED; footings never pooled; not theory closed. "V" = verified in a file, "I" = inferred.

## 1. The headline

- **The adopted theory (v3s, scoped; owner 2026-11-04, 7ac515f958) predicts Newtonian wide binaries.** CQ2
  (`cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/SEALED_PREDICTION.md`, 95303af61c): gamma_r - 1 = (s/L*)^2 F, about 4.5e-5 at
  30 kAU; through the frozen pipeline gamma_inf is identical to Newton's in every realisation (V). The 1.0019 / 1.0100
  values are the pipeline's Newton draws, not a v3s offset.
- **So DR4 cannot confirm v3s over Newton, ever** (the gap is about 1e-5 against sigma_sys 0.020). It can only kill
  v3s by showing a boost: v3s vs plain QUMOND is SEPARABLE (2.62-5.27 canonical, 2.86-7.08 alt; V).
- **The bare a0 law (plain QUMOND, CW1) predicts 1.149 +- 0.027 / 1.208 +- 0.007.** A Newtonian DR4 excludes it at
  about 5 sigma under the registered error (sigma_tot 0.0276).
- Net: DR4 decides **screened (v3s) vs unscreened (bare law)**, not "framework vs Newton/LCDM". A Newtonian sky is
  survival for v3s and a kill for the bare law; a boost near 1.15 is a kill for v3s.

## 2. Seal inventory (which governs)

| seal / rule | commit | theory | gamma (can / alt) | rule | status |
|---|---|---|---|---|---|
| CQ2 | 532e0dc567 / 95303af61c | v3s (adopted) | = Newton | **none of its own** (labels only) | governing prediction, no verdict rule |
| CW1 | da6917883b / e7672a30e1 | bare law, plain QUMOND | 1.149 / 1.208 | separation labels; DR3 Q rule | bare-law reference; v3s falsifier from above |
| D2 note + A1-A3 | 8658130bd0 ... 3d82af0a7e | law-first vs medium-first/screened | anchor = Arm A floor 1.1614 / 1.1917 | 3 sigma; sigma_sys(b) primary, (a)(e)(g2) must agree | only frozen rule naming both readings; anchor is not the bare law's own number (0.43 / 0.59 sigma) |
| FN6 | 8b1bbea197 / 7ab147288d | screening-length window (not adopted) | 1.00-1.04 (p <= 0.4); 1.13-1.21 alt p 0.45 | 3 sigma_tot | secondary |
| PREREGISTRATION_DR4 + 22 amendments | hash 20677265 | 2026-07 MI/MG, Arms A/B/C | various | error model + guard zone > 1.23 still bind | theory rows superseded |
| CFG740 + CFG800/825 R rule (A22) | c4f88c6eed, a553a4a663 | stiff hedgehog, same s^2 form as v3s, older L* 5.75 pc | <= 8.9e-4 at 50 kAU | KILL iff R-1 >= max(0.01, 3 sigma_R) | only frozen kill rule on a hedgehog form |
| Arm C / A21, GD1, CFG553 | in prereg; 2eeff4935d; 43fb64612 | retired theories | 1.000 (Arm C) | z rows | retired; Arm C's rows are numerically v3s's (I) |

s^TX dipole: void (A5 collapse). Arm B: not a testable arm (A12).

## 3. Contradictions in the record (V)

1. PAPER67 v1.2 (`PAPER67_galaxy_law_and_what_it_leaves_2026.tex` line 315) says a Newtonian 2-30 kAU result counts
   against the law, cites CW1 and FN6, never CQ2, while the same version adopts v3s, which predicts Newton.
2. `ASTRA_HANDOFF_2026-11-04_FINISH_PUSH.md` line 20 lists CW1, D2, FN6 as the DR4 comparisons and omits CQ2.
3. Newton reference differs: FN6's pipeline Newton 0.9919 / 0.9794 vs CW1/CQ2 1.0019 / 1.0100 vs D2/prereg 1.000,
   same pipeline hash 7c884e0e (likely different realisations; I).
4. v3s scope names galaxies, Solar System, lensing, GWs; wide binaries (hosted in the Milky Way) are not named, and the
   MW joint fit is excluded. Whether DR4 scores v3s is not stated.

## 4. Readiness

- Ready and tested: frozen pipeline (sha 7c884e0e), `prep_2026/gaia_dr4_prep/dr4_ready_1/` tools; DR3 dry runs
  (6,210 pairs reproduced byte for byte; gamma 1.075 +- 0.055 non-scoring); CFG943 mock chain (7356bb671d).
- Untested: real DR4 column/table names (draft datamodel 2026-06-26), NSS union on real tables (flagged 0 of 12,420
  on DR3), DR4 joins, NSS-off and RV-screened rungs (NOT IMPLEMENTED, CFG943 N4), `seed_sweep.py` cannot run the
  primary `cones-literal` mode (N9).
- Critical path: cut-13 cone fetch, ~39k queries, **~47 h serial (189 h if the archive is 4x slower)**. Realistic
  scored answer 2-8 days after release.
- No release-day script or scheduled task exists for DR4 (only the ALMA one). Closest: `RELEASE_DAY_CHECKLIST.md`,
  CFG943 README section 5. The driver's default `--cut13 extract-literal` is not the primary.
- Owner-only: a registered Gaia archive account (open in every dry-run record); every query's go; CFG943 notes N1-N11
  unfiled (N1, N4, N5, N9 matter); FN2 item 3 (D2 anchor); CFG825's once-only `--dr4` run.
- Power gap (CFG943 mocks): a MOND-size sky is killed only 2-59 % of the time by the R rule (about 2,100 pairs,
  guard zone, 3-20 kAU rung failing ~40 % under a correct model).

## 5. Power (arithmetic from the frozen formulas; I)

sigma_fit = 0.019 sqrt(30000/N); DR3 suggests ~0.025 at 30k.

| comparison | sigma_sys | 3 sigma | 5 sigma |
|---|---|---|---|
| 1.00 vs 1.15 | 0.020 | N >~ 5-9k | N >~ 20-35k |
| 1.00 vs 1.15 | (b) 0.0375 (DR3) | N >~ 10-17k | never |
| 1.00 vs v3s | any | never | never |

The registered N = 30,000 has no forecast in the record; DR3 gave 6,210.

Trap: sigma_sys(b) includes the NSS-off shift (+0.075 on DR3). If DR4's NSS screen works well, that shift grows and
inflates sigma_sys, so a successful screen weakens the verdict. Only a dated pre-data amendment can change this
(section 1.5: no post-hoc shrinking).

## 6. How to get the final answer sooner (ranked; all pre-data, none changes a prediction)

1. **Owner decisions, filed and dated before 2026-12-02:** (a) name the rule that scores v3s (D2 medium-first rows,
   or Arm C's z rows re-attached, plus the CFG825 R rule at v3s's L* floor); (b) fix the D2 anchor (Arm A floor vs
   CW1 1.149 / 1.208); (c) one Newton reference; (d) state that DR4 wide binaries score v3s; (e) CFG943 N1, N4, N5, N9.
   Then a PAPER67 addendum that lists CQ2.
2. **Register the Gaia archive account** (owner only) now.
3. **Bulk server-side crossmatch for cut 13:** one uploaded-table ADQL join instead of ~39k cones; days -> hours.
   Needs a dated transport amendment (like A19), a DR3 byte-equivalence test against the cone results, and the owner's
   yes for the DR3 test query.
4. **DR4 N and sigma_fit forecast** on the DR3 extract with the frozen DR4 error scaling (local, cheap, no row change).
5. **sigma_sys(b) / NSS-off decision** by pre-data amendment, validated by mock-triple injection, or an explicit
   decision to leave it.
6. **Implement the NSS-off and RV-screened rungs and a cones mode in `seed_sweep.py`** (new code, rows untouched).
7. **One release-day script + scheduled task**, mirroring FN2's: self-tests, hash checks, manifest, `--cut13
   cones-literal`, ~3 GB memory guard, a stop at each owner yes.

Not worth it: mass or separation splits (v3s predicts nothing measurable; gamma_hat already separates law-first vs
Newton). External pre-December data (DESI DR1: 18 pairs with both RVs, 2390b7409e; APOGEE DR17 on disk, unused;
no LAMOST/GALAH) could give a non-scoring DR3 contamination check, nothing that scores DR4. Published wide-binary
results (Chae 2023-24 boost; Banik+24, Pittordis & Sutherland Newton) are recalled, not fetched: provisional.

## 7. Sources

Two read-only review passes this session over: `prep_2026/gaia_dr4_prep/` (prereg, amendments, D2 note, dr4_ready_1,
checklist, dry runs), `cq_lanes_2026_11_04/CQ2_v3s_dr4_seal`, `cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4`,
`finish_2026_11_04/FN6_powerlaw_screening`, `finish_2026_11_04/FN2_dated_tests/fn2_dr4.out`,
`campaign_fresh_gravity/CFG553, CFG740, CFG800, CFG816, CFG200, CFG239, CFG943`, `rebuild_2026_10_22/KT20, KT21, GD1,
DR4_orbit_count_memory, S3_v3_mw_seals`, `reviews/dr4_*_2026_10_26`. CQ2's "identical to Newton" and "NOT SEPARABLE"
lines re-read directly (SEALED_PREDICTION.md lines 33-39).
