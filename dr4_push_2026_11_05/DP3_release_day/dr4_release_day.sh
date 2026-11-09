#!/bin/bash
# DP3 Gaia DR4 release-day wrapper: RELEASE_DAY_RUNBOOK_DR4.md, with its checks and STOP points enforced.
#   bash dr4_release_day.sh --check        hashes, guard, approval file, DP1 state, DR4 availability (by date; DP3_PROBE=1 adds ONE HTTP HEAD
#                                          to the public ESA archive documentation page). No data, no archive query.
#   bash dr4_release_day.sh --run          the release-day chain. Every archive step, the account step and the once-only CFG825 --dr4 run
#                                          need a line "GO <step>" in OWNER_APPROVAL_DR4.md (written by the session on the owner's yes in chat,
#                                          never by this script). Resumable: finished steps leave release_2026_12_02/.done_<step>.
#   bash dr4_release_day.sh --dry-run-dr3  the same chain on the DR3 data on disk, socket guard on, no network; outputs in dry_run_dr3/.
# Exit: 0 ok; 2 no approval file; 3 DR4 not yet available; 5 guard (disk / live jobs); 6 a frozen hash differs; 7 a step failed;
#       10 STOP: a step needs the owner's yes (the log says which, with size and time).
# kappa = 1/2 FITTED; footings never pooled; not theory closed. Newton-side wording: "v3s survives", never confirmed.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$ROOT" || exit 9
LANE=dr4_push_2026_11_05/DP3_release_day
PREP=prep_2026/gaia_dr4_prep
READY=$PREP/dr4_ready_1
CFG=campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring
DP1=dr4_push_2026_11_05/DP1_nss_off_rung
DP5=dr4_push_2026_11_05/DP5_dr4_fetchers
DP6=dr4_push_2026_11_05/DP6_cut12_wiring
APPROVAL=$LANE/OWNER_APPROVAL_DR4.md
RELEASE_DATE=2026-12-02
MODE=${1:---check}
case "$MODE" in
  --check) OUT=$LANE/check ;;
  --run) OUT=$LANE/release_2026_12_02 ;;
  --dry-run-dr3) OUT=$LANE/dry_run_dr3 ;;
  *) echo "usage: $0 --check | --run | --dry-run-dr3"; exit 9 ;;
esac
mkdir -p "$OUT"
LOG=$OUT/release_day.log
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY="nice -n 10 python3 -B"

log() {
  local s="$(date -u +%FT%TZ) $*"
  s="${s//$ROOT\//}"; s="${s//$ROOT/<repo>}"; s="${s//$HOME/<home>}"
  echo "$s" | tee -a "$LOG"
}
scrub() { for f in "$@"; do [ -f "$f" ] && sed -i '' "s#$ROOT/##g; s#$HOME#<home>#g" "$f"; done; }

# ---------------------------------------------------------------- pinned hashes (sha256 as committed on 2026-11-05)
HASHES="
7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9 $PREP/wide_binary_pipeline.py
46452daf1f2e2521b6e5a892a7a234e6ad063f2fd4f1c7392664f63f99a507ad $PREP/catalog_builder/build_catalog.py
d826f688e140ebf5f948f518bb2bc0efd754cfb2d0519feada4044861040b46f $PREP/catalog_builder/fetch_extract.py
69280396596de09251f4edea948af20b27ed4770461eebfcaa23020747ec2a16 $PREP/catalog_builder/validate_dr3.py
20677265fdace8e13c93c5b16b5d37255c203b4e4458b4cea8b5ed6d1d7f9388 $PREP/PREREGISTRATION_DR4.md
5768a66c1a0a2c2c39da7811cf7020581cfe20202188618974d9c1653f5e4590 $PREP/OWNER_DECISION_2026-11-05_DR4_FORKS.md
448bf4ef63e253f8f3c306ef0e68836a86ecd221097cbb533abfd7fd711bb17b $PREP/OWNER_DECISION_2026-11-05b_DR4_D7_D8.md
8dfcc1d89bcfc38a294a0ca0aedf5c6ac20080ec78c41f15fbb7d3453d5844aa $PREP/OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF.md
e25be2cf54bdd933743a6b452b20c8fb558572fcfc40d6d3924c4db7e599ffac $PREP/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md
d09a920f8e03fb126a234c5b8a6e8ab18a29803454e4dd638f5da5d1d5b9d22f campaign_fresh_gravity/OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md
50ed835cfab0352dc0994b69fec4f0ef13496534f10e3d949e280cbd4d6ce0ec $CFG/cfg816_r.py
44301ffdec2b97aeaacfb3cfb3e4edbcfebcb07927dab77b09d9fa1e7d8fe050 $CFG/make_pair_table.py
0a259b7da70693add28a3dfd2a65c66ce9e85820b72baf1c7dd9b19f2f4e196e $CFG/build_variant_catalogue.py
558e03f0b87e52aae77a069cea7c1d8ef765b2bbeb8002c028c8357722b3fffb $CFG/FROZEN_CRITERIA.md
687ea154759952fcb64219dba3a97e6e01d29f91195cd343295e60f8ff563d86 $READY/dry_run_driver.py
e324626a95b804d4acf814a64650f2a1f0947d079fdb70e44957aa01f7ce4889 $READY/dr4_archive_fetch.py
c82ac04ff6d77d4f05083665f7ef01bca1719d5c2096c9296d9628d59a0fab30 $READY/q1_cones_dr4.py
e8f70c3fc850429b6693b6085d6c121d40443b5a99cd3e074d083973883b2c0b $READY/cut12_nss_union.py
79b1ab190a8d8e9a888a7ae103ee93699634d64ddc040946f8e9d7ad13f79fa9 $READY/cut13_allsource.py
68de1f1ff47df0a2bcbda4fdcd545e52bf2f5e28901fedd0648459d7198ba147 $READY/join_columns.py
0f94d70e90eae5e32fd440c7aa84100c6bbe3e560961fcc8ce688380a7d0dd62 $READY/seed_sweep.py
786456dde7d5c4f5376ff6d98eedab5870483d8f2efb8702b9669f553fe9062a $READY/seed_label.py
b629dc3322914bb7c749eea9efa8f5349631d65bbbf4eb9576b289fdd0a56580 $READY/amdt14_distances.py
4e0874582a715be94eaaa3fda929d737bc2238b1595784e7da3d17a04d3ace17 $READY/arm_c_rows.py
9e6f711f6ab9cd813420cc5db694da490fa3b38cf67431f47e9f05bd381f8c73 $READY/dr4_q1_estimate.py
cf0c42d63003334d96f80d38f7a2177e09ab5347733d7507616f71f7997e40ae $READY/cones_cut13.py
55c76992476204f52f3d5c9c87dd80c265419e7314fdad7a17f2bca5846a595d $READY/manifest_template_dr4.json
5685feb4d49e6650b3e2419c5b20a67e89df9438b17f3eb322a91e64a0b2a212 doors_push_2026_10_22/D2_wide_binary_fork/d2_sigma_sys_defs.py
"

hash_check() {   # -> 0 if every pinned file matches
  local bad=0 n=0 want path got
  while read -r want path; do
    [ -z "$want" ] && continue
    n=$((n+1))
    got=$(shasum -a 256 "$path" 2>/dev/null | cut -c1-64)
    if [ "$got" != "$want" ]; then log "HASH MISMATCH $path: ${got:-missing} (pinned ${want:0:12}...)"; bad=$((bad+1)); fi
  done <<< "$HASHES"
  if [ -n "$(git status --short -- $PREP/PREREGISTRATION_DR4.md $PREP/AMENDMENT*_HASH.txt $PREP/OWNER_DECISION_2026-11-05*.md 2>/dev/null)" ]; then
    log "prereg directory NOT clean (git status)"; bad=$((bad+1)); fi
  if [ -e "$CFG/cfg816_r_dr4_results.json" ]; then log "CFG825 once-only DR4 slot: PRESENT (cfg816_r_dr4_results.json exists)"; DR4SLOT=used
  else log "CFG825 once-only DR4 slot: absent (unused)"; DR4SLOT=free; fi
  if [ $bad -eq 0 ]; then log "hashes: all $n pinned files OK; prereg = Amendment 22 'after' digest; prereg directory clean"; return 0; fi
  log "hashes: $bad problem(s) of $n"; return 1
}

disk_gb() { df -k "$ROOT" | awk 'NR==2{printf "%d", $4/1048576}'; }
live_1024() { ps -axo rss=,command= | awk '$1 > 1048576 && /1024/ && !/awk/ && !/dr4_release_day/' | head -3; }
live_big_py() { ps -axo rss=,pid=,command= | awk '$1 > 2097152 && $3 ~ /[Pp]ython/ && !/awk/' | awk '{printf "pid %s rss %.1f GB: %s %s %s\n", $2, $1/1048576, $3, $4, $5}' | head -5; }

guard() {   # $1 = strict (refuse on a >2 GB python job) or dry (override allowed)
  local ok=0 dg b p
  dg=$(disk_gb); log "disk free: ${dg} GB (need >= 20)"
  [ "$dg" -ge 20 ] || { log "GUARD: free disk below 20 GB"; ok=1; }
  b=$(live_1024); if [ -n "$b" ]; then log "GUARD: a 1024^3-class process (> 1 GB, '1024' in its command) is live"; ok=1; else log "no 1024^3 run live"; fi
  p=$(live_big_py)
  if [ -n "$p" ]; then
    while read -r l; do log "python job > 2 GB live: $l"; done <<< "$p"
    if [ "$1" = "dry" ] && [ "${DP3_ALLOW_LIVE_JOBS:-0}" = "1" ]; then log "dry run: DP3_ALLOW_LIVE_JOBS=1 given, continuing (the frozen pipeline peaks ~3 GB; check free memory)"
    else log "GUARD: a python job > 2 GB is live (the frozen pipeline needs ~3 GB peak)"; ok=1; fi
  else log "no python job > 2 GB live"; fi
  return $ok
}

dp1_state() {   # REPRODUCED | NOT_REPRODUCED | NO_VERDICT | NO_README: DP1's machine-readable verdict (dr3_check.json), README present
  [ -f "$DP1/README.md" ] || { echo NO_README; return; }
  [ -f "$DP1/dr3_check.json" ] || { echo NO_VERDICT; return; }
  python3 -I -c "import json,sys; v=json.load(open(sys.argv[1])).get('verdict',''); print({'REPRODUCED':'REPRODUCED','NOT REPRODUCED':'NOT_REPRODUCED'}.get(v,'NO_VERDICT'))" "$DP1/dr3_check.json" 2>/dev/null || echo NO_VERDICT
}

available() {   # sets AVAIL=yes|no; the probe is opt-in
  local today; today=$(date -u +%F)
  if [[ "$today" < "$RELEASE_DATE" ]]; then AVAIL=no; log "DR4 not yet available: today $today is before the scheduled release $RELEASE_DATE (ESA, provisional)"
  else AVAIL=yes; log "release date reached ($today >= $RELEASE_DATE): availability is confirmed only by the schema probe of step G4 (needs the owner's yes)"; fi
  if [ "${DP3_PROBE:-0}" = "1" ]; then
    local c; c=$(curl -sSI --max-time 30 "https://gea.esac.esa.int/archive/documentation/GDR4/index.html" 2>/dev/null | tr -d '\r' | awk '/^HTTP/{c=$2} END{print c+0}')
    log "probe (one HTTP HEAD, ESA archive GDR4 documentation page): HTTP $c (information only; 200 = page published)"
  else log "network probe: skipped (opt-in: DP3_PROBE=1)"; fi
}

go() { [ -f "$APPROVAL" ] && grep -Eq "^GO $1( |$)" "$APPROVAL"; }
skip() { [ -f "$APPROVAL" ] && grep -Eq "^SKIP $1( |$)" "$APPROVAL"; }
done_() { [ -f "$OUT/.done_$1" ]; }
mark() { date -u +%FT%TZ > "$OUT/.done_$1"; }
stop() { log "STOP at $1: needs the owner's yes in chat, then the line 'GO $1' in $APPROVAL. $2"; exit 10; }
gate() { done_ "$1" && { log "$1 already done (marker present)"; return 1; }; go "$1" || stop "$1" "$2"; log "$1: GO on record"; return 0; }
need_rc() { [ "$1" -eq 0 ] || { log "STEP FAILED: $2 (exit $1)"; exit 7; }; }

log "DP3 Gaia DR4 release day, mode $MODE. kappa = 1/2 FITTED; footings never pooled; not theory closed."

# ================================================================ --check
if [ "$MODE" = "--check" ]; then
  hash_check; HOK=$?
  guard strict; GOK=$?
  [ -f "$APPROVAL" ] && log "approval file present: $APPROVAL ($(grep -cE '^GO ' "$APPROVAL") GO lines)" || log "approval file absent: $APPROVAL (expected before release day)"
  log "DP1 NSS-off rung state: $(dp1_state) (REPRODUCED -> step G11 runs it; otherwise NOT IMPLEMENTED, D7 N4.1)"
  available
  [ $HOK -eq 0 ] && log "SUMMARY hashes OK" || log "SUMMARY hashes FAIL"
  [ $GOK -eq 0 ] && log "SUMMARY guard OK: a --run would be allowed now" || log "SUMMARY guard: a --run would be REFUSED now (see GUARD lines)"
  [ "$AVAIL" = "no" ] && log "SUMMARY DR4 NOT YET AVAILABLE" || log "SUMMARY release date reached"
  exit 0
fi

# ================================================================ --run (DR4)
if [ "$MODE" = "--run" ]; then
  available
  [ "$AVAIL" = "yes" ] || { log "STOP: DR4 not yet available"; exit 3; }
  [ -f "$APPROVAL" ] || { log "STOP: no owner approval file ($APPROVAL)"; exit 2; }
  hash_check || { log "STOP: a frozen hash differs; find out why before any step"; exit 6; }
  [ "$DR4SLOT" = "free" ] || log "NOTE: CFG825's DR4 slot is already used; step G14 will not run again"
  guard strict || { log "STOP: guard"; exit 5; }
  EXT=real_research/data/widebinaries/dr4_extract
  M=$OUT/manifest_dr4.json; SPEC=$OUT/spec_dr4.json; CAND=$OUT/candidates_dr4.csv; NM=$OUT/neighbours_manifest_dr4.json
  if ! done_ R0; then
    log "R0 self-tests (offline)"
    for t in "$READY/dry_run_driver.py --self-test" "$READY/amdt14_distances.py --self-test" "$READY/arm_c_rows.py --self-test" \
             "$CFG/make_pair_table.py --self-test" "$LANE/dr4_outcome_map.py --self-test"; do
      $PY $t > "$OUT/selftest_$(basename ${t%% *} .py).out" 2>&1; need_rc $? "self-test $t"; done
    mark R0; fi
  if gate G1 "Save the published DR4 data model (URL, UTC time, sha256) into $OUT/datamodel/; write $SPEC (renames only) and $M (from $READY/manifest_template_dr4.json, every null filled, names only) BEFORE any data are opened. A download of the data-model page needs the yes (name, source, size)."; then
    for f in "$SPEC" "$M"; do [ -f "$f" ] || { log "G1: $f missing"; exit 7; }; done
    ls "$OUT"/datamodel/* >/dev/null 2>&1 || { log "G1: no saved data model in $OUT/datamodel/"; exit 7; }
    shasum -a 256 "$OUT"/datamodel/* "$SPEC" "$M" | tee -a "$LOG"; git rev-parse HEAD | sed 's/^/git HEAD /' | tee -a "$LOG"; mark G1; fi
  if ! done_ G2; then
    if skip G2; then log "G2 registered archive account: SKIP on record (anonymous TAP)"; mark G2
    elif go G2; then log "G2 registered archive account: the owner logs in; this script never handles a password. NOTE: the dr4_ready_1 tools and fetch_extract.py query anonymously (no login hook); see the runbook, open issue O3"; mark G2
    else stop G2 "Registered Gaia archive account (higher quotas for the ~47 h cone fetch): the owner's act. Write 'GO G2' (owner logged in) or 'SKIP G2'."; fi; fi
  if gate G3 "Primary base: DP5 fetch_extract_dr4.py --release dr4 (12 sky chunks + Sigma_18 map; frozen WHERE, non_single_star dropped: O1 fixed; DR3: 4,582,547 rows, ~400 MB, 6,461 s; DR4 central x1.54: ~620 MB, ~2.8 h; async jobs, anonymous; DP5_SYNC=1 for --sync-ranges)."; then
    $PY $DP5/fetch_extract_dr4.py --release dr4 --print-queries > "$OUT/G3_queries.adql" 2>&1; need_rc $? "G3 print-queries"
    GO3=$(grep -E '^GO G3' "$APPROVAL" | head -1)
    caffeinate -i $PY $DP5/fetch_extract_dr4.py --release dr4 --manifest $PREP/catalog_builder/manifest_dr4.json ${DP5_SPEC:+--spec-json $DP5_SPEC} ${DP5_SYNC:+--sync-ranges} \
        --owner-go-recorded "$GO3" > "$OUT/G3_fetch_extract.out" 2>&1; need_rc $? "G3 fetch_extract_dr4"; mark G3; fi
  if gate G4 "Stages A-F: build_catalog.py --release dr4 (offline for A-F; DR3 16 min on 16 cores; its own stage G fetches correlations: an archive query). Stage G of the frozen builder is information only; the primary build is step G8."; then
    caffeinate -i $PY $PREP/catalog_builder/build_catalog.py --release dr4 > "$OUT/G4_build_catalog.out" 2>&1; rc=$?
    [ -f "$EXT/stage_F.npz" ] || need_rc 1 "G4 build_catalog (no stage_F.npz)"
    [ $rc -eq 0 ] || log "G4: build_catalog exit $rc after stage F was cached (its own stage G is information only); continuing"; mark G4; fi
  if gate G5 "Cut 12 / joins: run the ADQL of cut12_nss_union.adql_nss() for each Amendment 17 counted table (6 tables; uploads of the sample ids, < 10 MB) via DP5 fetch_nss_dr4.py (inlist transport; O2 fixed for nss_*), the all_source_flags join by hand; record table, solution types and row counts in $M. the builds G6/G8/G10/G11 read them through DP6 (A17_primary, O8 fixed)."; then
    python3 -I -c "import json,sys; c=json.load(open(sys.argv[1]))['cut12_nss']; r=(c.get('readings') or {}).get('A17_primary') or {}; sys.exit(0 if r.get('counted_tables') and c.get('id_files') and c.get('solution_types_recorded') else 1)" "$M" || need_rc 1 "G5: cut12_nss readings.A17_primary / id_files / solution_types_recorded not filled in $M (A17 (d))"
    mark G5; fi
  if gate G6 "Candidates: dry_run_driver.py --release dr4 --manifest M --allow-network --cut13 extract-builder --dump-candidates (stage-G correlation fetch; DR3 ~3,000 ids per 1,000 pairs)."; then
    $PY $DP6/dp6_with_a17.py --a17-manifest "$M" --report-json "$OUT/G6_a17.json" -- $READY/dry_run_driver.py --release dr4 --manifest "$M" --allow-network --cut13 extract-builder --dump-candidates "$CAND" > "$OUT/G6_candidates.json" 2>&1; need_rc $? "G6 candidates"
    $PY $READY/dr4_q1_estimate.py --pairs-csv "$CAND" > "$OUT/G6_q1_prebrief.out" 2>&1; need_rc $? "G6 pre-brief"
    $PY $READY/q1_cones_dr4.py --print-count-queries > "$OUT/G6_count_queries.adql" 2>&1
    $PY $READY/q1_cones_dr4.py --spec dr4_all_source --spec-json "$SPEC" --stage-a $EXT/stage_A.npz --pairs-csv "$CAND" --tag dr4_all \
        --out-dir $EXT/dp3_q1 --manifest "$OUT/manifest_q1_dr4_all.json" --plan-only > "$OUT/G6_q1_plan.out" 2>&1; need_rc $? "G6 Q1 plan-only"
    log "G6 done: read the pre-brief (queries, MB, hours) to the owner before G7"; mark G6; fi
  if ! done_ G7; then
    go G7 || stop G7 "Q1 neighbour-cone fetch (cut 13, Amendment 16(b) primary): central ~39,000 queries, ~1.7 GB accepted, ~47 h serial at the DR3 pace (25k-64k queries, 31-77 h; a slow archive multiplies the hours). The GO line must carry the caps: 'GO G7 accepted_mb=<A> received_mb=<R> max_queries=<Q>' (suggested 1.5x central: 2540 / 3100 / 58900)."
    CAPS=$(grep -E '^GO G7 ' "$APPROVAL" | head -1)
    A=$(echo "$CAPS" | sed -n 's/.*accepted_mb=\([0-9.]*\).*/\1/p'); Rm=$(echo "$CAPS" | sed -n 's/.*received_mb=\([0-9.]*\).*/\1/p'); Q=$(echo "$CAPS" | sed -n 's/.*max_queries=\([0-9]*\).*/\1/p')
    [ -n "$A" ] && [ -n "$Rm" ] && [ -n "$Q" ] || stop G7 "the GO G7 line lacks accepted_mb / received_mb / max_queries"
    caffeinate -i $PY $READY/q1_cones_dr4.py --spec dr4_all_source --spec-json "$SPEC" --stage-a $EXT/stage_A.npz --pairs-csv "$CAND" --tag dr4_all \
        --out-dir $EXT/dp3_q1 --manifest "$OUT/manifest_q1_dr4_all.json" --cap-accepted-mb "$A" --cap-received-mb "$Rm" --max-queries "$Q" \
        --owner-go-recorded "$CAPS" > "$OUT/G7_q1_fetch.out" 2>&1; need_rc $? "G7 Q1 fetch (resumable: rerun --run)"
    [ -f "$NM" ] || { log "G7: write $NM ({table, neighbours, pairs, include}) recording the optional-table decision (Amendment 16(b))"; exit 7; }
    mark G7; fi
  PRIM=$OUT/wide_binaries_dr4.csv
  if gate G8 "Primary build: dry_run_driver.py --cut13 cones-literal (passed explicitly, D7 N9) --allow-network (stage-G correlations; --corr-transport sync only if async fails, recorded)."; then
    $PY $DP6/dp6_with_a17.py --a17-manifest "$M" --report-json "$OUT/G8_a17.json" -- $READY/dry_run_driver.py --release dr4 --manifest "$M" --allow-network --cut13 cones-literal --neighbours-manifest "$NM" --out-csv "$PRIM" \
        ${DP3_CORR_SYNC:+--corr-transport sync} > "$OUT/G8_primary_build.json" 2>&1; need_rc $? "G8 primary build"
    log "G8 manifest record: cut13 = cones-literal (explicit); correlation transport ${DP3_CORR_SYNC:+sync}${DP3_CORR_SYNC:-async}; sha256 $(shasum -a 256 "$PRIM" | cut -c1-16)"
    mark G8; fi
  if ! done_ O9; then
    log "O9 frozen pipeline fit (offline, ~3 GB peak)"
    $PY $PREP/wide_binary_pipeline.py --catalog "$PRIM" > "$OUT/pipeline_dr4.log" 2>&1; need_rc $? "O9 pipeline"
    grep -E "SELF-TEST|catalog \[a0|\[7\(e\)\]|\[gated\]" "$OUT/pipeline_dr4.log" > "$OUT/pipeline_dr4_fitlines.out"
    $PY $READY/amdt14_distances.py --log "$OUT/pipeline_dr4.log" > "$OUT/amdt14_dr4.out" 2>&1; need_rc $? "O9 amdt14"
    $PY $READY/arm_c_rows.py --log "$OUT/pipeline_dr4.log" > "$OUT/arm_c_dr4.out" 2>&1; need_rc $? "O9 arm_c_rows"
    mark O9; fi
  if gate G10 "Amendment 18 seed sweep: seed_sweep.py --release dr4 --mode g-only --K 50 --cut13 extract-builder (D7 N9) --fit --ladder --allow-network (delta correlation fetches; ~100 pipeline fits, ~1-2 h single job), then seed_label.py --evaluate."; then
    $PY $DP6/dp6_with_a17.py --a17-manifest "$M" --report-json "$OUT/G10_a17.json" -- $READY/seed_sweep.py --release dr4 --mode g-only --K 50 --cut13 extract-builder --fit --ladder --allow-network --tag dr4_g50 > "$OUT/G10_seed_sweep.out" 2>&1; need_rc $? "G10 seed sweep"
    cp $EXT/seed_sweep/seed_sweep_manifest_dr4_g50.json "$OUT/" 2>/dev/null
    $PY $READY/seed_label.py --evaluate "$OUT/seed_sweep_manifest_dr4_g50.json" > "$OUT/G10_seed_label.out" 2>&1; need_rc $? "G10 seed label"
    mark G10; fi
  RUNG=""
  if ! done_ G11; then
    st=$(dp1_state)
    if [ "$st" = "REPRODUCED" ]; then
      go G11 || stop G11 "NSS-off rung (DP1 REPRODUCED on DR3): build(drop_nss=True, smax_kau=30) on DR4 through DP1's nss_off_rung.py (stage-G correlation fetch)."
      $PY $DP6/dp6_with_a17.py --a17-manifest "$M" --report-json "$OUT/G11_a17.json" -- $DP1/nss_off_rung.py --release dr4 --manifest "$M" --cut13 cones-literal --neighbours-manifest "$NM" --allow-network --out-csv "$OUT/nss_off_rung_dr4.csv" \
          > "$OUT/G11_nss_off.out" 2>&1; need_rc $? "G11 NSS-off rung"
      echo "IMPLEMENTED (DP1 REPRODUCED)" > "$OUT/nss_off_status.txt"
    else log "G11 NSS-off rung: NOT IMPLEMENTED (DP1 state $st; D7 N4.1): sigma_sys(b) is computed without it, and the report says so"
      echo "NOT IMPLEMENTED (DP1 $st)" > "$OUT/nss_off_status.txt"; fi
    mark G11; fi
  [ -f "$OUT/nss_off_rung_dr4.csv" ] && RUNG="--nss-off $OUT/nss_off_rung_dr4.csv"
  if ! done_ O12; then
    $PY $LANE/dp3_sigma_sys.py --base "$PRIM" $RUNG --seed-manifest "$OUT/seed_sweep_manifest_dr4_g50.json" --tag DR4 --out-json "$OUT/sigma_sys_dr4.json" > /dev/null 2>&1; need_rc $? "O12 sigma_sys"
    [ -f "$OUT/stage_A_nss0.npz" ] || { $PY $DP6/dp6_with_a17.py --write-per-star "$OUT/stage_A_nss0.npz" --stage-a $EXT/stage_A.npz > "$OUT/O12_per_star.out" 2>&1; need_rc $? "O12 per-star file (DP6)"; }
    $PY $CFG/make_pair_table.py --catalogue "$PRIM" --per-star "$OUT/stage_A_nss0.npz" --out "$OUT/pairs_dr4.csv" --declare-neutral non_single_star > "$OUT/O12_pair_table.out" 2>&1; need_rc $? "O12 pair table (D7 N5)"
    mark O12; fi
  if ! done_ G14; then
    if [ "$DR4SLOT" = "used" ]; then log "G14: CFG825's DR4 slot already used; reading its results"
    else
      go G14 || stop G14 "THE ONCE-ONLY CFG825 RUN: python3 $CFG/cfg816_r.py --dr4 $OUT/pairs_dr4.csv (registered catalogue, --declare-neutral non_single_star, D7 N5). It refuses a second run; a change goes under Departures."
      $PY $CFG/cfg816_r.py --dr4 "$OUT/pairs_dr4.csv" > "$OUT/G14_cfg816_r_dr4.out" 2>&1; need_rc $? "G14 cfg816_r --dr4"; fi
    mark G14; fi
  log "O15 final scoring (outcome map, both footings, both g_ext, R, splits)"
  $PY $LANE/dr4_outcome_map.py --pipeline-log "$OUT/pipeline_dr4.log" --sigma-json "$OUT/sigma_sys_dr4.json" --r-json $CFG/cfg816_r_dr4_results.json \
      --tag "DR4 $(date -u +%F)" --out "$OUT/outcome_map_dr4.out" --json-out "$OUT/outcome_map_dr4.json"; need_rc $? "O15 outcome map"
  scrub "$OUT"/*.out "$OUT"/*.json "$OUT"/*.log
  log "done. Write RESULT_2026-12-02.md (no verdict word beyond the filed labels; 'v3s survives', never confirmed), check for home paths, commit with explicit paths only. The CFG825 variant catalogue (build_variant_catalogue.py) is information only (D7 N5)."
  exit 0
fi

# ================================================================ --dry-run-dr3 (offline, DR3 on disk)
EXT=real_research/data/widebinaries/dr3_extract
CONES="--neighbours $EXT/dr4_ready_1/q1_full_neighbours.fits --neighbour-pairs $EXT/wide_binaries_dr3.csv --neighbours $EXT/dr4_ready_1/q1_delta_neighbours.fits --neighbour-pairs $EXT/dr4_ready_1/q1_delta_pairs.csv"
G50=$READY/seed_sweep_manifest_g50_dr3.json
log "DRY RUN on DR3 (offline; every number is a code-path test, NON-SCORING, Amendment 7(e))"
FAIL=0
chk() { if [ "$1" -eq 0 ]; then log "PASS $2"; else log "FAIL $2 (exit $1)"; FAIL=$((FAIL+1)); fi; }
rss() { awk '/maximum resident set size/{printf "%.2f GB", $1/1073741824}' "$1" 2>/dev/null; }
hash_check; chk $? "D0 pinned hashes"
guard dry || { log "STOP: guard (set DP3_ALLOW_LIVE_JOBS=1 to run the dry run beside a live > 2 GB job when memory allows)"; exit 5; }
for t in "$READY/dry_run_driver.py --self-test" "$READY/amdt14_distances.py --self-test" "$READY/arm_c_rows.py --self-test" \
         "$CFG/make_pair_table.py --self-test" "$LANE/dr4_outcome_map.py --self-test"; do
  n=$(basename ${t%% *} .py); $PY $t > "$OUT/D1_selftest_$n.out" 2>&1; chk $? "D1 self-test $n"; done
log "D2 builds (driver, offline)"
$PY $READY/dry_run_driver.py --release dr3 --variant primary --cut13 extract-builder --out-csv "$OUT/wb_dr3_extract_builder.csv" > "$OUT/D2_build_extract_builder.json" 2>&1; chk $? "D2 build extract-builder"
s=$(shasum -a 256 "$OUT/wb_dr3_extract_builder.csv" | cut -c1-16); n=$(($(wc -l < "$OUT/wb_dr3_extract_builder.csv")-1))
[ "$s" = "6fff64d964ebaa72" ] && [ "$n" -eq 6210 ]; chk $? "D2 extract-builder = reference (6,210 pairs, sha256 $s)"
$PY $READY/dry_run_driver.py --release dr3 --variant primary --cut13 cones-literal $CONES --out-csv "$OUT/wb_dr3_cones_literal.csv" > "$OUT/D2_build_cones_literal.json" 2>&1; chk $? "D2 build cones-literal (the release-day primary form, D7 N9)"
log "D2 cones-literal: $(($(wc -l < "$OUT/wb_dr3_cones_literal.csv")-1)) pairs, sha256 $(shasum -a 256 "$OUT/wb_dr3_cones_literal.csv" | cut -c1-16) (code-path number)"
for b in extract_builder cones_literal; do
  /usr/bin/time -l nice -n 10 python3 -B $PREP/wide_binary_pipeline.py --catalog "$OUT/wb_dr3_$b.csv" > "$OUT/pipeline_dr3_$b.log" 2> "$OUT/pipeline_dr3_$b.time"; chk $? "D3 frozen pipeline on $b (peak RSS $(rss "$OUT/pipeline_dr3_$b.time"))"
  grep -q "PIPELINE SELF-TEST: PASS" "$OUT/pipeline_dr3_$b.log"; chk $? "D3 pipeline self-test PASS ($b)"
  grep -E "SELF-TEST|catalog \[a0|\[7\(e\)\]|\[gated\]" "$OUT/pipeline_dr3_$b.log" > "$OUT/pipeline_dr3_${b}_fitlines.out"   # *.log is git-ignored; the fit lines are kept
  $PY $READY/amdt14_distances.py --log "$OUT/pipeline_dr3_$b.log" > "$OUT/amdt14_dr3_$b.out" 2>&1; chk $? "D3 amdt14_distances ($b)"
  $PY $READY/arm_c_rows.py --log "$OUT/pipeline_dr3_$b.log" > "$OUT/arm_c_dr3_$b.out" 2>&1; chk $? "D3 arm_c_rows ($b)"
done
g=$(sed -n 's/^ *catalog \[a0 canonical\] *gamma_inf = \([0-9.]*\).*/\1/p' "$OUT/pipeline_dr3_extract_builder.log" | head -1)
python3 -I -c "import sys; sys.exit(0 if abs(float(sys.argv[1])-1.0750) <= 1e-4 else 1)" "${g:-0}"; chk $? "D3 extract-builder canonical gamma-hat $g = 1.0750 (10-09 dry run)"
log "D4 seed sweep (g-only, extract-builder, K = 2 for time; declared) and the seed label on the committed DR3 G50 manifest"
$PY $READY/seed_sweep.py --release dr3 --mode g-only --K 2 --cut13 extract-builder --fit --ladder --tag dp3dry > "$OUT/D4_seed_sweep.out" 2>&1; chk $? "D4 seed_sweep K 2"
cp $EXT/seed_sweep/seed_sweep_manifest_dp3dry.json $EXT/seed_sweep/seed_sweep_dp3dry.out "$OUT/" 2>/dev/null
$PY $READY/seed_label.py --evaluate "$G50" > "$OUT/D4_seed_label_g50.out" 2>&1; chk $? "D4 seed_label --evaluate (committed DR3 G50 manifest)"
st=$(dp1_state)
if [ "$st" = "REPRODUCED" ]; then
  # DP1's committed DR3 rung catalogue (its build peaks above this lane's 4 GB cap, so it is not rebuilt here); sha256 checked against its manifest
  python3 -I -c "
import json,hashlib,sys
m=json.load(open(sys.argv[1])); h=hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest()
w=[v for k,v in m.items() if 'sha256' in k and isinstance(v,str) and len(v)==64]
print('  DP1 rung CSV sha256', h[:16], 'manifest', [x[:16] for x in w]); sys.exit(0 if h in w else 1)" "$DP1/nss_off_rung_dr3.csv.manifest.json" "$DP1/nss_off_rung_dr3.csv" | tee -a "$LOG"
  chk ${PIPESTATUS[0]} "D5 NSS-off rung: DP1 REPRODUCED; its DR3 rung catalogue matches its manifest"
  RUNG3="--nss-off $DP1/nss_off_rung_dr3.csv"
else log "D5 NSS-off rung: NOT IMPLEMENTED (DP1 state $st; D7 N4.1); the chain continues"; RUNG3=""; fi
log "D6 sigma_sys on the DR3 reference with the D2 lane's NSS-off probe (known answer)"
$PY $LANE/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off $CFG/wide_binaries_dr3_variant.csv --extra V4=$EXT/wide_binaries_dr3_elbadryR.csv \
    --extra V5=$EXT/wide_binaries_dr3_scaled_clean.csv --seed-manifest "$G50" --tag "DR3 DRY RUN" --out-json "$OUT/sigma_sys_dr3.json" > /dev/null 2>&1; chk $? "D6 dp3_sigma_sys"
python3 -I -c "
import json,sys
o=json.load(open(sys.argv[1])); d=json.load(open(sys.argv[2])); ok=True
for f in ('canonical','alt'):
    mine=list(o[f]['shifts'].values()); ref=d['info_'+f]['shifts']
    dd=max(abs(a-b) for a,b in zip(mine,ref)); sb=o[f]['b']; sref=max(0.02,0.5*d['info_'+f]['spread'])
    print(f'  {f}: shifts', ' '.join('%+.4f'%x for x in mine), 'vs D2', ' '.join('%+.4f'%x for x in ref), '; max diff %.4f; (b) %.4f vs %.4f'%(dd,sb,sref))
    ok = ok and dd<=0.002 and abs(sb-sref)<=0.002 and len(mine)==3
sys.exit(0 if ok else 1)" "$OUT/sigma_sys_dr3.json" doors_push_2026_10_22/D2_wide_binary_fork/d2_sigma_sys_defs_results.json | tee -a "$LOG"
chk ${PIPESTATUS[0]} "D6 ladder shifts and sigma_sys(b) reproduce the D2 lane (+-0.002)"
$PY $LANE/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv $RUNG3 --seed-manifest "$G50" --tag "DR3 DRY RUN, release-day path (NSS-off = DP1 rung if REPRODUCED)" \
    --out-json "$OUT/sigma_sys_dr3_releasepath.json" > /dev/null 2>&1; chk $? "D6b dp3_sigma_sys on the release-day path (information)"
log "D7 R (registered catalogue, --declare-neutral non_single_star; CFG825 scored in memory, never --dr3 / --dr4)"
$PY $CFG/make_pair_table.py --catalogue $EXT/wide_binaries_dr3.csv --per-star $EXT/stage_A.npz --out "$OUT/pairs_dr3_ref.csv" --declare-neutral non_single_star > "$OUT/D7_pair_table.out" 2>&1; chk $? "D7 make_pair_table"
$PY $LANE/dp3_r_inmemory.py --table "$OUT/pairs_dr3_ref.csv" --out-json "$OUT/r_dr3_ref.json" > /dev/null 2>&1; chk $? "D7 R in memory (DR4 slot untouched)"
python3 -I -c "
import json,sys
p=json.load(open(sys.argv[1]))['branches']['primary']; q=json.load(open(sys.argv[2]))['branches']['primary']
print('  R %.6f (official C4 %.6f), N_R %d (%d), sigma_R %.4f'%(p['R'],q['R'],p['N'],q['N'],p['sigma_R']))
sys.exit(0 if abs(p['R']-q['R'])<=1e-6 and p['N']==q['N'] else 1)" "$OUT/r_dr3_ref.json" $CFG/cfg816_r_dr3_results.json | tee -a "$LOG"
chk ${PIPESTATUS[0]} "D7 R reproduces the official DR3 C4 (R, N_R)"
log "D8 final scoring step on the DR3 reference chain (DRY RUN, NON-SCORING)"
$PY $LANE/dr4_outcome_map.py --pipeline-log "$OUT/pipeline_dr3_extract_builder.log" --sigma-json "$OUT/sigma_sys_dr3.json" --r-json "$OUT/r_dr3_ref.json" \
    --tag "DR3 DRY RUN, NON-SCORING (Amendment 7(e)); sigma_sys with the D2 probe" --out "$OUT/outcome_map_dr3_dryrun.out" --json-out "$OUT/outcome_map_dr3_dryrun.json" > /dev/null 2>&1; chk $? "D8 dr4_outcome_map on the DR3 chain"
$PY $LANE/dr4_outcome_map.py --pipeline-log "$OUT/pipeline_dr3_extract_builder.log" --sigma-json "$OUT/sigma_sys_dr3_releasepath.json" --r-json "$OUT/r_dr3_ref.json" \
    --tag "DR3 DRY RUN, NON-SCORING (Amendment 7(e)); sigma_sys on the release-day path" --out "$OUT/outcome_map_dr3_dryrun_releasepath.out" > /dev/null 2>&1; chk $? "D8b dr4_outcome_map, release-day path"
[ -e "$CFG/cfg816_r_dr4_results.json" ] && { log "FAIL CFG825 DR4 slot appeared"; FAIL=$((FAIL+1)); } || log "CFG825 DR4 slot still absent"
scrub "$OUT"/*.out "$OUT"/*.json "$OUT"/*.log "$OUT"/*.time
[ $FAIL -eq 0 ] && { log "DRY RUN COMPLETE: every D step PASS"; exit 0; } || { log "DRY RUN: $FAIL step(s) FAILED"; exit 7; }
