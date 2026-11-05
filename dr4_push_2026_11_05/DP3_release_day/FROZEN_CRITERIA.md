# DP3 release day: FROZEN CRITERIA for the outcome-map scorer and the test plan

Lane DP3 (Gaia DR4 wide-binary prep; DR4 due 2026-12-02 per ESA, provisional). Written 2026-11-05, before any scorer,
wrapper or test code, and committed alone. Nothing frozen is edited: not `PREREGISTRATION_DR4.md` or its 22 amendments, not
the D2 note (`prep_2026/gaia_dr4_prep/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md`) or A1-A3, not the two owner decisions of
2026-11-05 (413c1c8e24, d71a111d1d), not the 10-21 kill-line note, not CFG740/CFG800/CFG825/CFG943, not
`wide_binary_pipeline.py` (sha256 7c884e0e...). This lane writes new files only. No network query, no download.
κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## 1. The scorer `dr4_outcome_map.py`: inputs

Per footing (canonical, alt), scored separately and never pooled:
- γ̂ and σ_fit: the frozen pipeline's whole-catalogue fit (`catalog [a0 ...] gamma_inf = g +- s` lines of its `--catalog` log),
  or given on the command line.
- σ_sys(b) (A3 primary): either given, or computed as max(0.020, ½ × full spread of {γ̂_base} ∪ {γ̂ of each implementable ladder
  rung} ∪ {γ̂ NSS-off probe}). The baseline is a member of the set (this is how the D2 lane's DR3 value 0.0375 canonical /
  0.0415 alt arises from shifts {0, +0.015, +0.033, +0.075} / {0, −0.013, −0.025, +0.058}). If the NSS-off rung is NOT
  IMPLEMENTED (D7 N4.1), σ_sys(b) is computed without it and the output says so.
- σ_sys for the robustness definitions (a) (= 0.020), (e) (jackknife over the implementable cut variants) and (g2)
  (√(0.020² + σ_build²), Amendment 18 σ_build). Missing values are allowed; then the robustness step cannot pass (§2 step 5).
- R, σ_R, N_R of CFG825's primary branch (optional).

## 2. The label (frozen order of evaluation; σ_d = √(σ_fit² + σ_sys(d)²); "≥ 3σ" inclusive)

Constants from the record: Newton 1.000 (D3(a)); law-first anchor = Arm A floor 1.1614 canonical / 1.1917 alt (D2(a), frozen
D2 rows); guard edge 1.23; gate ceilings σ_sys(b) < 0.048 canonical / < 0.058 alt (D2 A1); k = 3.

1. **GUARD_ZONE** if γ̂ > 1.23: no verdict for every reading (prereg; kill-line note N3).
2. **SUB_NEWTON_NO_VERDICT** if γ̂ ≤ 1 − 3σ_b: pipeline or contamination fault, no verdict for every reading (D4(a)).
3. **UNDECIDED_GATE** if σ_sys(b) ≥ ceiling of the footing: no verdict, whatever γ̂ is.
4. Rows under (b): LF = (anchor − γ̂ ≥ 3σ_b); SC = (γ̂ − 1 ≥ 3σ_b).
   LF and SC → **BOTH_EXCLUDED** (D5(a), the alt overlap); LF only → **LAW_FIRST_EXCLUDED**; SC only → **SCREENED_EXCLUDED**;
   neither → **UNDECIDED**.
5. Robustness (A3.2): if step 4 gave a verdict, the same steps 2 and 4 are run with σ_sys(a), σ_sys(e), σ_sys(g2). Each must
   give the identical label; if any differs, or a value is missing → **UNDECIDED_ROBUSTNESS** (raw numbers still printed).

Plain-words lines (D6(a)), one per label; the word "confirmed" never follows "v3s" except as "not confirmed" / "never confirmed":
- LAW_FIRST_EXCLUDED: "Newton side: v3s survives (not confirmed); bare law excluded (law-first reading, gate holds)".
- SCREENED_EXCLUDED: "boost side: v3s EXCLUDED (screened / medium-first reading); bare law survives this test".
- BOTH_EXCLUDED: "BOTH EXCLUDED (D5): ≥ 3σ above Newton and ≥ 3σ below the law-first anchor; neither reading fits".
- UNDECIDED*, GUARD_ZONE, SUB_NEWTON_NO_VERDICT: no verdict word; raw γ̂, every σ and both distances printed.

Printed beside the label, with **no verdict weight** (information): per frozen g_ext (primary 1.778e-10, alternative 2.078e-10)
the same rows with A3's AQUAL anchor (canonical 1.1667 / 1.1448, alt 1.1986 / 1.1730) and the D2 §4 / CW1 numbers; a
disagreement with the verdict label is printed as an information split at that g_ext (D2(a) keeps the Arm A rows). The edges
anchor − 3σ_b and 1 + 3σ_b; the distances (γ̂ − 1)/σ_b and (anchor − γ̂)/σ_b.

R (10-21 kill line): **KILLED** iff R − 1 ≥ max(0.01, 3σ_R); **CONSISTENT** iff |R − 1| < 0.01 and 2σ_R ≤ 0.01 (unreachable,
σ_R ≥ 0.02); else **UNDECIDED** (neither kill nor survival). The size a kill needs, 1 + max(0.01, 3σ_R), is printed.

Splits, printed as splits and never merged (§2e of 413c1c8e24, N6): canonical vs alt labels differ; γ̂ rows vs R (R KILLED
while the γ̂ label is not SCREENED_EXCLUDED/BOTH_EXCLUDED, or the γ̂ label is SCREENED_EXCLUDED/BOTH_EXCLUDED while R is not
KILLED). Fixed reminders: N4.3 ~40 % false-failure rate of the 3-20 kAU rung beside any "systematic-limited" reading; N7
(CFG740 falsifier 1 beyond ~37 kAU and falsifier 2 not scored); D8 (mock-triple injection is information only).

## 3. Scorer self-test (known answers; all must pass, exit 0)

From the owner decision's §2a/2b/2c (σ_fit = 0.019 √(30000/N); σ_sys(a) = (e) = (g2) = σ_sys(b) unless stated):
| case | footing | N | σ_sys(b) | γ̂ | expected |
|---|---|---|---|---|---|
| T1 | canonical | 30,000 | 0.020 | 1.000 | LAW_FIRST_EXCLUDED |
| T2 | canonical | 30,000 | 0.020 | 1.081 | UNDECIDED |
| T3 | canonical | 30,000 | 0.020 | 1.100 | SCREENED_EXCLUDED |
| T4 | canonical | 30,000 | 0.020 | 1.250 | GUARD_ZONE |
| T5 | canonical | 30,000 | 0.020 | 0.900 | SUB_NEWTON_NO_VERDICT |
| T6 | alt | 30,000 | 0.020 | 1.095 | BOTH_EXCLUDED |
| T7 | canonical | 30,000 | 0.020 | 0.920 | LAW_FIRST_EXCLUDED (just above the 0.917 edge) |
| T8 | canonical | 6,210 | 0.0375 | 1.000 | UNDECIDED ("a Newtonian sky reads UNDECIDED", 2c) |
| T9 | canonical | 6,210 | 0.020 | 1.000 | LAW_FIRST_EXCLUDED (edge 1.022) |
| T10 | canonical | 30,000 | 0.050 | 1.000 | UNDECIDED_GATE |
| T11 | alt | 30,000 | 0.050 | 1.000 | LAW_FIRST_EXCLUDED (alt gate 0.058 passes) |
| T12 | canonical | 30,000 | b 0.020, e 0.025 | 1.075 | UNDECIDED_ROBUSTNESS |
| T13 | canonical | 30,000 | 0.020, robustness values missing | 1.000 | UNDECIDED_ROBUSTNESS |
| T14 | alt | 30,000 | 0.020 | 1.120 | SCREENED_EXCLUDED |
- E1: the 2c edges (law-first ≤ / screened ≥) for the five (N, σ_sys) rows reproduce 1.079/1.083, 1.035/1.126, 1.061/1.100,
  1.022/1.139, 0.993/1.168 to ±0.0006 (the table's rounding), and the alt law-first edges 1.109 (N 30k, 0.020), 1.053
  (6,210, 0.020), 1.023 (6,210, 0.0375) to ±0.0012 (the table rounds the alt shift to "0.03 higher").
- E2: σ_sys(b) from the D2 DR3 shifts = 0.0375 canonical, 0.0415 alt (±1e-9).
- E3: the R rule reproduces CFG816's own case table (`cfg816_r.py` classify cases, 8 of 8) and the kill-line note's "needs
  R ≥ 1.22" at σ_R 0.075 (1.225).
- E4: no output line of any case contains "v3s confirmed" or "v3s is confirmed"; every LAW_FIRST_EXCLUDED line contains
  "v3s survives".
- E5: the split detector flags the MOCK B3 pattern (γ̂ SCREENED_EXCLUDED, R UNDECIDED) and a footing disagreement.

**MUTATE (must bite):** `DP3_MUTATE=1` uses k = 2 instead of 3; `DP3_MUTATE=2` disables the D5 rule (frozen precedence:
overlap reads LAW_FIRST_EXCLUDED). Each must make the self-test FAIL (exit 1). Outputs: `dr4_outcome_map_selftest.out`,
`..._MUTATE1.out`, `..._MUTATE2.out`.

## 4. Test plan for `dr4_release_day.sh`

**--check (today):** must report "DR4 not yet available" (decided by date; the network probe is opt-in, `DP3_PROBE=1`, a single
HTTP HEAD to the public ESA archive, and is NOT run in this test), every pinned hash OK (the four checklist §3 files, the
prereg = Amendment 22's "after" digest 20677265..., the two 11-05 owner decisions, the D2 note, the kill-line note, CFG825's
cfg816_r.py / make_pair_table.py / build_variant_catalogue.py / FROZEN_CRITERIA.md, the dr4_ready_1 tools and manifest
template as committed today), CFG825's once-only DR4 slot absent (`cfg816_r_dr4_results.json` does not exist), the guard
lines (free disk ≥ 20 GB; no 1024³ run; no python job > 2 GB), the approval file state, DP1's state. Exit 0.
**--run (today):** must refuse before any network step (DR4 not yet available; exit 3) and write nothing outside the lane.
**--dry-run-dr3:** the release-day chain on the DR3 data on disk, socket guard on, no network, outputs in
`dry_run_dr3/` of this lane. Steps and pass rules:
- D0 the --check hash block passes.
- D1 self-tests: `dry_run_driver.py --self-test`, `amdt14_distances.py --self-test`, `arm_c_rows.py --self-test`,
  `make_pair_table.py --self-test`, `dr4_outcome_map.py --self-test`: each exits 0.
- D2 builds: `--cut13 extract-builder` must give 6,210 pairs, sha256 prefix 6fff64d964ebaa72 (the reference); the primary form
  `--cut13 cones-literal` on the two DR3 Q1 cone files must run end to end (pairs and sha256 recorded; code-path number).
- D3 the frozen pipeline `--catalog` on both builds: PIPELINE SELF-TEST PASS; the extract-builder fit must give canonical
  γ̂ 1.0750 (±0.0001, the 10-09 dry run); then `amdt14_distances.py` and `arm_c_rows.py` on the log, exit 0.
- D4 seed sweep (Amendment 18, extract-builder mode per D7 N9): `seed_sweep.py --release dr3 --mode g-only --K 2 --fit --ladder
  --tag dp3dry` exits 0 (K reduced from 50 for time; declared); `seed_label.py --evaluate` on the committed DR3 G50 manifest exits 0.
- D5 NSS-off rung: runs only if `dr4_push_2026_11_05/DP1_nss_off_rung/README.md` states REPRODUCED (and not NOT REPRODUCED);
  otherwise the step prints NOT IMPLEMENTED and the chain continues (D7 N4.1).
- D6 σ_sys: `dp3_sigma_sys.py` (new) on the DR3 builder catalogue with the D2 lane's NSS-off probe catalogue must reproduce the
  D2 lane's ladder shifts (canonical +0.015/+0.033/+0.075, alt −0.013/−0.025/+0.058, from `d2_sigma_sys_defs_results.json`)
  to ±0.002, and σ_sys(b) 0.0375 / 0.0415 to ±0.002 (same estimator, same seed and call order: exact expected).
- D7 R: `make_pair_table.py --declare-neutral non_single_star` on the builder catalogue, then CFG825's `read_table` + `score`
  imported read-only, in memory (never `--dr3` or `--dr4`); must reproduce the official C4 primary R 0.97284 and N_R 348 to 1e-6
  when the input is the reference catalogue.
- D8 the final scoring step: `dr4_outcome_map.py` on the D3 log + D6 JSON + D7 JSON exits 0 and prints both footings, both
  g_ext information lines, R and the split lines; every DR3 number is labelled DRY RUN, NON-SCORING (Amendment 7(e)).
**Limits:** OMP_NUM_THREADS=1, nice -n 10, ≤ 4 GB RSS per process (the frozen pipeline peaks ~3 GB), one heavy process at a time.
If any D step fails for a reason outside this lane's code it is reported as found, not repaired by editing a frozen file.
