#!/bin/bash
# DP8 check runner (criteria FROZEN_CRITERIA.md, 4caa8bc91f): checks C1-C7 and their mutation twins, each into its own output under checks/.
#   bash dp8_checks.sh <stage>     stages: pre c1 c2 c4 c5a c7a c7b testcopy c3 c5bc c6pre c6 c6f post
# Every command runs under sandbox-exec with outbound IP connections denied (on top of the python socket guards); heavy stages run
# under /usr/bin/time -l (logs/*.time) one at a time, nice 10, OMP_NUM_THREADS=1. DR3 only; no archive query; no DR4 byte.
# kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$ROOT" || exit 9
L=dr4_push_2026_11_05/DP8_release_path_wiring
DP3=dr4_push_2026_11_05/DP3_release_day
DP7=dr4_push_2026_11_05/DP7_seed_mean_check
DP1=dr4_push_2026_11_05/DP1_nss_off_rung
PREP=prep_2026/gaia_dr4_prep
EXT=real_research/data/widebinaries/dr3_extract
G50=$PREP/dr4_ready_1/seed_sweep_manifest_g50_dr3.json
CONES="--neighbours $EXT/dr4_ready_1/q1_full_neighbours.fits --neighbour-pairs $EXT/wide_binaries_dr3.csv --neighbours $EXT/dr4_ready_1/q1_delta_neighbours.fits --neighbour-pairs $EXT/dr4_ready_1/q1_delta_pairs.csv"
SB='(version 1)(allow default)(deny network-outbound (remote ip))'
SCR=${DP8_SCRATCH:?set DP8_SCRATCH to a scratch folder outside the repo}
O=$L/checks; T=$L/logs; W=$L/work
mkdir -p "$O" "$T" "$W"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
SBX() { sandbox-exec -p "$SB" "$@"; }
TIMED() { local tag=$1; shift; SBX /usr/bin/time -l nice -n 10 "$@" 2> "$T/$tag.time"; }
scrubf() { for f in "$@"; do [ -f "$f" ] && sed -i '' "s#$SCR#<scratch>#g; s#$ROOT/##g; s#$ROOT#<repo>#g; s#$HOME#<home>#g" "$f"; done; }
bigpy() { ps -axo rss=,command= | awk '$1 > 2097152 && $2 ~ /[Pp]ython/' | head -3; }
heavy_ok() { local b; b=$(bigpy); if [ -n "$b" ]; then echo "another python job > 2 GB is live; not starting $1:"; echo "$b" | cut -c1-120; exit 5; fi; }
note() { echo "$(date -u +%FT%TZ) $*" >> "$T/stages.txt"; echo "$*"; }
pins() {   # sha256 of every file pinned in the real wrapper's HASHES block, with the pinned value
  python3 -I - "$DP3/dr4_release_day.sh" <<'EOF'
import hashlib, re, sys
t = open(sys.argv[1]).read()
blk = t.split('HASHES="', 1)[1].split('"', 1)[0]
sub = {"$PREP": "prep_2026/gaia_dr4_prep", "$READY": "prep_2026/gaia_dr4_prep/dr4_ready_1", "$CFG": "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring"}
n = bad = 0
for line in blk.strip().splitlines():
    h, p = line.split()
    for k, v in sub.items():
        p = p.replace(k, v)
    try:
        g = hashlib.sha256(open(p, "rb").read()).hexdigest()
    except FileNotFoundError:
        g = "MISSING"
    n += 1; bad += (g != h)
    print(("ok  " if g == h else "BAD ") + g + "  " + p)
print(f"pinned files: {n}; off their pinned value: {bad}")
EOF
}

case "${1:-}" in
pre)
  note "pre: pins and decision files before the lane's runs; sandbox control"
  pins > "$O/pins_before.txt"; tail -1 "$O/pins_before.txt"
  SBX python3 -I -c "
import socket
s = socket.socket()
s.settimeout(3)
try:
    s.connect(('192.0.2.1', 443)); print('CONNECTED (sandbox did NOT deny)')
except PermissionError as e:
    print('denied by the sandbox (PermissionError):', e)
except OSError as e:
    print('denied / failed (OSError):', e)" > "$O/c6_sandbox_control.out" 2>&1
  cat "$O/c6_sandbox_control.out" ;;

c1)
  note "C1: real wrapper --check; mirror control; MUTATE C1a / C1b on mirror copies"
  SBX bash $DP3/dr4_release_day.sh --check > "$O/c1_check.out" 2>&1; echo "exit $?" >> "$O/c1_check.out"
  M=$SCR/mirror; rm -rf "$M"; mkdir -p "$M"
  python3 -I - "$DP3/dr4_release_day.sh" "$M" <<'EOF'
import os, shutil, sys
t = open(sys.argv[1]).read(); M = sys.argv[2]
blk = t.split('HASHES="', 1)[1].split('"', 1)[0]
sub = {"$PREP": "prep_2026/gaia_dr4_prep", "$READY": "prep_2026/gaia_dr4_prep/dr4_ready_1", "$CFG": "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring"}
paths = []
for line in blk.strip().splitlines():
    p = line.split()[1]
    for k, v in sub.items():
        p = p.replace(k, v)
    paths.append(p)
paths += ["dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh", "dr4_push_2026_11_05/DP1_nss_off_rung/README.md", "dr4_push_2026_11_05/DP1_nss_off_rung/dr3_check.json"]
import glob
paths += sorted(glob.glob("prep_2026/gaia_dr4_prep/AMENDMENT*_HASH.txt"))
for p in paths:
    os.makedirs(os.path.join(M, os.path.dirname(p)), exist_ok=True)
    shutil.copy2(p, os.path.join(M, p))
print(len(paths), "files copied")
EOF
  ( cd "$M" && git init -q && git add -A && git -c user.name=dp8 -c user.email=dp8@invalid commit -q -m mirror ) || exit 7
  SBX bash "$M/dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh" --check > "$O/c1_mirror_control.out" 2>&1; echo "exit $?" >> "$O/c1_mirror_control.out"
  printf ' ' >> "$M/prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md"
  SBX bash "$M/dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh" --check > "$O/c1_MUTATE_15b.out" 2>&1; echo "exit $?" >> "$O/c1_MUTATE_15b.out"
  ( cd "$M" && git checkout -q -- prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md )
  printf ' ' >> "$M/prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md"
  SBX bash "$M/dr4_push_2026_11_05/DP3_release_day/dr4_release_day.sh" --check > "$O/c1_MUTATE_15.out" 2>&1; echo "exit $?" >> "$O/c1_MUTATE_15.out"
  scrubf "$O"/c1_*.out
  grep -h "SUMMARY hashes\|HASH MISMATCH\|NOT clean\|hashes: all" "$O"/c1_*.out ;;

c2)
  note "C2: text-only proof of dp3_sigma_sys.py; seed-mean entry on the release-day path vs DP7; MUTATE without the option"
  git show HEAD:$DP3/dp3_sigma_sys.py > "$W/dp3_sigma_sys_HEAD.py"
  sed 's/max(0.020, 0.5 \* spread)/max(0.021, 0.5 * spread)/' $DP3/dp3_sigma_sys.py > "$W/dp3_sigma_sys_MUTATE_const.py"
  python3 -I - "$W/dp3_sigma_sys_HEAD.py" "$DP3/dp3_sigma_sys.py" > "$O/c2_text_only.out" <<'EOF'
import ast, sys
def blank(p):
    t = ast.parse(open(p).read())
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            n.value = ""
    return ast.dump(t)
a, b = blank(sys.argv[1]), blank(sys.argv[2])
print("AST with every string constant blanked: before (HEAD) vs after:", "IDENTICAL" if a == b else "DIFFERENT")
EOF
  python3 -I - "$W/dp3_sigma_sys_HEAD.py" "$W/dp3_sigma_sys_MUTATE_const.py" > "$O/c2_text_only_MUTATE.out" <<'EOF'
import ast, sys
def blank(p):
    t = ast.parse(open(p).read())
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            n.value = ""
    return ast.dump(t)
a, b = blank(sys.argv[1]), blank(sys.argv[2])
print("MUTATE (0.020 -> 0.021 in (b)): AST with every string constant blanked: before (HEAD) vs mutated copy:", "IDENTICAL" if a == b else "DIFFERENT")
EOF
  heavy_ok c2
  TIMED c2_d6_replay_optoff python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/wide_binaries_dr3_variant.csv \
      --extra V4=$EXT/wide_binaries_dr3_elbadryR.csv --extra V5=$EXT/wide_binaries_dr3_scaled_clean.csv --seed-manifest "$G50" --tag "DR3 DRY RUN" --out-json "$O/c2_d6_replay_optoff.json" > /dev/null
  TIMED c2_d6inputs_seedmean python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/wide_binaries_dr3_variant.csv \
      --extra V4=$EXT/wide_binaries_dr3_elbadryR.csv --extra V5=$EXT/wide_binaries_dr3_scaled_clean.csv --seed-manifest "$G50" --nss-off-seed-mean $DP7/dp7.json \
      --tag "DR3 DRY RUN, D6 inputs + --nss-off-seed-mean (DP7)" --out-json "$O/c2_d6inputs_seedmean.json" > /dev/null
  TIMED c2_seedmean_releasepath python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off $DP1/nss_off_rung_dr3.csv --seed-manifest "$G50" \
      --nss-off-seed-mean $DP7/dp7.json --tag "DR3 DRY RUN, release-day path (NSS-off = DP1 rung) + --nss-off-seed-mean (DP7)" --out-json "$O/c2_seedmean_releasepath.json" > /dev/null
  TIMED c2_MUTATE_no_option python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off $DP1/nss_off_rung_dr3.csv --seed-manifest "$G50" \
      --tag "DR3 DRY RUN, release-day path (NSS-off = DP1 rung) + --nss-off-seed-mean (DP7)" --out-json "$O/c2_MUTATE_no_option.json" > /dev/null
  scrubf "$O"/c2_*.json "$O"/c2_*.out
  cat "$O/c2_text_only.out" "$O/c2_text_only_MUTATE.out" ;;

c4)
  note "C4: the RUWE information call cannot change the main sigma_sys json; MUTATE: --stage-a on the main call"
  heavy_ok c4
  A=$O/c4_main.json
  TIMED c4_main python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off $DP1/nss_off_rung_dr3.csv --seed-manifest "$G50" --nss-off-seed-mean $DP7/dp7.json \
      --tag "DR3 DP8 C4 main (O12 form)" --out-json "$A" > /dev/null
  h1=$(shasum -a 256 "$A" | cut -c1-64)
  TIMED c4_ruwe_info python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off $DP1/nss_off_rung_dr3.csv --seed-manifest "$G50" --nss-off-seed-mean $DP7/dp7.json \
      --stage-a $EXT/stage_A.npz --tag "DR3 DP8 C4 O12r form: RUWE < 1.2 added, information only" --out-json "$O/c4_ruwe_info.json" > /dev/null
  h2=$(shasum -a 256 "$A" | cut -c1-64)
  TIMED c4_main_again python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off $DP1/nss_off_rung_dr3.csv --seed-manifest "$G50" --nss-off-seed-mean $DP7/dp7.json \
      --tag "DR3 DP8 C4 main (O12 form)" --out-json "$W/c4_main_again.json" > /dev/null
  h3=$(shasum -a 256 "$W/c4_main_again.json" | cut -c1-64)
  TIMED c4_MUTATE_merged python3 -B $DP3/dp3_sigma_sys.py --base $EXT/wide_binaries_dr3.csv --nss-off $DP1/nss_off_rung_dr3.csv --seed-manifest "$G50" --nss-off-seed-mean $DP7/dp7.json \
      --stage-a $EXT/stage_A.npz --tag "DR3 DP8 C4 main (O12 form)" --out-json "$O/c4_MUTATE_merged.json" > /dev/null
  h4=$(shasum -a 256 "$O/c4_MUTATE_merged.json" | cut -c1-64)
  printf 'main json sha256 before the RUWE call %s\nmain json sha256 after the RUWE call  %s\nfresh main call after it              %s\n' "$h1" "$h2" "$h3" > "$O/c4_ruwe.out"
  printf 'MUTATE C4 (--stage-a on the main call) sha256 %s (main %s)\n' "$h4" "$h1" > "$O/c4_MUTATE_merged.out"
  scrubf "$O"/c4_*.json
  cat "$O/c4_ruwe.out" "$O/c4_MUTATE_merged.out" ;;

c5a)
  note "C5(i): dp8_sepbins self-test vs XR22's own sepbins; MUTATE C5a: DP8_MUTATE=edges"
  heavy_ok c5a
  TIMED c5_selftest python3 -B $L/dp8_sepbins.py --self-test --out-json "$O/c5_selftest.json" > "$O/c5_selftest.out"; echo "exit $?" >> "$O/c5_selftest.out"
  DP8_MUTATE=edges TIMED c5_selftest_MUTATE python3 -B $L/dp8_sepbins.py --self-test --out-json "$O/c5_selftest_MUTATE.json" > "$O/c5_selftest_MUTATE.out"; echo "exit $?" >> "$O/c5_selftest_MUTATE.out"
  tail -2 "$O/c5_selftest.out"; tail -2 "$O/c5_selftest_MUTATE.out" ;;

c7a)
  note "C7(a): the launcher's DR3 pass-through vs DP7's committed parts k = 0..2; MUTATE C7a: --keep-nss"
  heavy_ok c7a
  rm -rf "$W/c7_eq" "$W/c7_MUTATE"
  TIMED c7_launcher_eq python3 -B $L/dp8_seed_mean_release.py --release dr3 --cut13 cones-literal --fit-path pipeline --K 2 --rung-missing-cones extract-fallback --no-fit-cache \
      --out dp7 --out-dir "$W/c7_eq" > "$O/c7_launcher_eq.out" 2>&1; echo "exit $?" >> "$O/c7_launcher_eq.out"
  heavy_ok c7a-mutate
  TIMED c7_launcher_MUTATE python3 -B $L/dp8_seed_mean_release.py --release dr3 --cut13 cones-literal --fit-path pipeline --K 2 --rung-missing-cones extract-fallback --no-fit-cache --keep-nss \
      --out dp7 --out-dir "$W/c7_MUTATE" > "$O/c7_launcher_MUTATE.out" 2>&1; echo "exit $?" >> "$O/c7_launcher_MUTATE.out"
  for d in c7_eq c7_MUTATE; do mkdir -p "$O/$d"; cp "$W/$d"/dp7.json "$W/$d"/dp7.out "$W/$d"/dp7.dp8.json "$O/$d/" 2>/dev/null; cp "$W/$d"/parts/*.json "$O/$d/" 2>/dev/null; done
  scrubf "$O"/c7_launcher_*.out "$O"/c7_eq/* "$O"/c7_MUTATE/*
  tail -3 "$O/c7_launcher_eq.out" ;;

c7b)
  note "C7(b) mutations: the DR3 rung with --missing-cones error; the count helper on a manifest whose policy is not the fallback"
  heavy_ok c7b
  TIMED c7b_rung_error python3 -B $DP1/nss_off_rung.py --release dr3 --cut13 cones-literal $CONES --missing-cones error --out-csv "$W/nss_off_rung_dr3_cones_error.csv" > "$O/c7b_MUTATE_rung_error.out" 2>&1
  echo "exit $?" >> "$O/c7b_MUTATE_rung_error.out"
  python3 -I -c "
import json; m=json.load(open('$DP1/nss_off_rung_dr3.csv.manifest.json')); json.dump(m, open('$W/c7b_manifest_no_cones.json','w'))"
  SBX python3 -B $L/dp8_fallback_count.py --rung-manifest "$W/c7b_manifest_no_cones.json" --out-json "$W/c7b_count_MUTATE.json" --tag "MUTATE C7b (DP1's extract-builder rung, no cones block)" > "$O/c7b_MUTATE_count.out" 2>&1
  echo "exit $?" >> "$O/c7b_MUTATE_count.out"
  scrubf "$O"/c7b_*.out
  tail -2 "$O/c7b_MUTATE_rung_error.out"; tail -2 "$O/c7b_MUTATE_count.out" ;;

testcopy)
  note "test copy of the wrapper (not committed); its diff against the real file is committed"
  TC=$L/dr4_release_day_TESTCOPY.sh
  sed -e 's#^APPROVAL=\$LANE/OWNER_APPROVAL_DR4.md$#DP8T=dr4_push_2026_11_05/DP8_release_path_wiring; APPROVAL=$DP8T/work/OWNER_APPROVAL_TEST.md#' \
      -e 's#^RELEASE_DATE=2026-12-02$#RELEASE_DATE=${DP8_TEST_RELEASE_DATE:-2026-12-02}#' \
      -e 's#^  --check) OUT=\$LANE/check ;;$#  --check) OUT=$DP8T/check_testcopy ;;#' \
      -e 's#^  --run) OUT=\$LANE/release_2026_12_02 ;;$#  --run) OUT=$DP8T/release_testcopy ;;#' \
      -e 's#^  --dry-run-dr3) OUT=\$LANE/dry_run_dr3 ;;$#  --dry-run-dr3) OUT=$DP8T/dry_run_dr3 ;;#' \
      -e 's#\[ "\$dg" -ge 20 \]#[ "$dg" -ge ${DP8_TEST_MIN_DISK_GB:-20} ]#' $DP3/dr4_release_day.sh > "$TC"
  chmod +x "$TC"
  diff $DP3/dr4_release_day.sh "$TC" > "$O/testcopy.diff"; echo "diff lines: $(grep -c '^[<>]' "$O/testcopy.diff")"; cat "$O/testcopy.diff" ;;

c3)
  note "C3: the test copy's --dry-run-dr3 (outputs in dry_run_dr3/ of this lane)"
  heavy_ok c3
  rm -rf "$L/dry_run_dr3"
  DP8_TEST_MIN_DISK_GB=5 TIMED c3_dry_run bash $L/dr4_release_day_TESTCOPY.sh --dry-run-dr3 > "$O/c3_dry_run.out" 2>&1; echo "exit $?" >> "$O/c3_dry_run.out"
  scrubf "$O/c3_dry_run.out"
  heavy_ok c3-selftests
  for m in 1 2; do DP3_MUTATE=$m SBX python3 -B $DP3/dr4_outcome_map.py --self-test > "$O/c3_outcome_map_MUTATE$m.out" 2>&1; echo "exit $?" >> "$O/c3_outcome_map_MUTATE$m.out"; done
  grep -c "PASS" "$O/c3_dry_run.out"; grep "FAIL\|DRY RUN" "$O/c3_dry_run.out" | tail -5 ;;

c5bc)
  note "C5(ii)-(iii): sepbins standalone on the registered DR3 catalogue (twice) vs the dry run's D9; MUTATE C5b: one row dropped"
  heavy_ok c5bc
  TIMED c5_standalone_1 python3 -B $L/dp8_sepbins.py --catalog $EXT/wide_binaries_dr3.csv --out-json "$O/c5_standalone_1.json" --tag "DR3, report-only, code path (DP8)" > /dev/null
  TIMED c5_standalone_2 python3 -B $L/dp8_sepbins.py --catalog $EXT/wide_binaries_dr3.csv --out-json "$W/c5_standalone_2.json" --tag "DR3, report-only, code path (DP8)" > /dev/null
  head -n -1 $EXT/wide_binaries_dr3.csv > "$W/wide_binaries_dr3_droplast.csv" 2>/dev/null || sed '$d' $EXT/wide_binaries_dr3.csv > "$W/wide_binaries_dr3_droplast.csv"
  TIMED c5_MUTATE_droprow python3 -B $L/dp8_sepbins.py --catalog "$W/wide_binaries_dr3_droplast.csv" --out-json "$O/c5_MUTATE_droprow.json" --tag "DR3, report-only, code path (DP8)" > /dev/null
  for f in "$O/c5_standalone_1.json" "$W/c5_standalone_2.json" "$L/dry_run_dr3/sepbins_dr3.json" "$O/c5_MUTATE_droprow.json"; do echo "$(shasum -a 256 "$f" | cut -c1-64)  $(basename "$f")"; done > "$O/c5_independence.out"
  cat "$O/c5_independence.out" ;;

c6pre)
  note "C6(c) before dp8_checks.json exists: G11S must stop with NEEDS OWNER (exit 7)"
  heavy_ok c6pre
  R=$L/release_testcopy; rm -rf "$R"; mkdir -p "$R" "$W"
  printf '# DP8 test approval file (test copy only)\n' > "$W/OWNER_APPROVAL_TEST.md"
  for s in G1 G3 G4 G5 G6 G7 G8 G10 G11 G14; do echo "GO $s" >> "$W/OWNER_APPROVAL_TEST.md"; done; echo "SKIP G2" >> "$W/OWNER_APPROVAL_TEST.md"
  for s in R0 G1 G2 G3 G4 G5 G6 G7 G8 O9 G10 G11; do date -u +%FT%TZ > "$R/.done_$s"; done; : > "$R/nss_off_rung_dr4.csv"
  DP8_TEST_RELEASE_DATE=2026-11-01 DP8_TEST_MIN_DISK_GB=1 SBX bash $L/dr4_release_day_TESTCOPY.sh --run > "$O/c6_G11S_no_checkfile.out" 2>&1; echo "exit $?" >> "$O/c6_G11S_no_checkfile.out"
  scrubf "$O/c6_G11S_no_checkfile.out"; tail -3 "$O/c6_G11S_no_checkfile.out" ;;

c6)
  note "C6: --run refusals (real wrapper by date; test copy at G1 and at G11S); MUTATE C6: GO G11S given"
  heavy_ok c6
  [ -e $DP3/release_2026_12_02 ] && { echo "DP3 release folder exists before the test; not touching it"; exit 7; }
  SBX bash $DP3/dr4_release_day.sh --run > "$O/c6_run_real.out" 2>&1; echo "exit $?" >> "$O/c6_run_real.out"
  ls -A $DP3/release_2026_12_02 > "$O/c6_run_real_created.txt" 2>&1
  [ "$(ls -A $DP3/release_2026_12_02)" = "release_day.log" ] && rm -r $DP3/release_2026_12_02 && echo "removed the folder this test created (it held only release_day.log)" >> "$O/c6_run_real_created.txt"
  R=$L/release_testcopy; rm -rf "$R"; mkdir -p "$R"
  printf '# DP8 test approval file (test copy only): no GO line\n' > "$W/OWNER_APPROVAL_TEST.md"
  date -u +%FT%TZ > "$R/.done_R0"
  DP8_TEST_RELEASE_DATE=2026-11-01 DP8_TEST_MIN_DISK_GB=1 SBX bash $L/dr4_release_day_TESTCOPY.sh --run > "$O/c6_run_noGO_G1.out" 2>&1; echo "exit $?" >> "$O/c6_run_noGO_G1.out"
  rm -rf "$R"; mkdir -p "$R"
  printf '# DP8 test approval file (test copy only): every gated step but G11S\n' > "$W/OWNER_APPROVAL_TEST.md"
  for s in G1 G3 G4 G5 G6 G7 G8 G10 G11 G14; do echo "GO $s" >> "$W/OWNER_APPROVAL_TEST.md"; done; echo "SKIP G2" >> "$W/OWNER_APPROVAL_TEST.md"
  for s in R0 G1 G2 G3 G4 G5 G6 G7 G8 O9 G10 G11; do date -u +%FT%TZ > "$R/.done_$s"; done; : > "$R/nss_off_rung_dr4.csv"
  DP8_TEST_RELEASE_DATE=2026-11-01 DP8_TEST_MIN_DISK_GB=1 SBX bash $L/dr4_release_day_TESTCOPY.sh --run > "$O/c6_run_noGO_G11S.out" 2>&1; echo "exit $?" >> "$O/c6_run_noGO_G11S.out"
  echo "GO G11S (test copy only)" >> "$W/OWNER_APPROVAL_TEST.md"
  DP8_TEST_RELEASE_DATE=2026-11-01 DP8_TEST_MIN_DISK_GB=1 SBX bash $L/dr4_release_day_TESTCOPY.sh --run > "$O/c6_MUTATE_GO_G11S.out" 2>&1; echo "exit $?" >> "$O/c6_MUTATE_GO_G11S.out"
  cp "$R/G11S_seed_mean.out" "$O/c6_MUTATE_GO_G11S_step.out" 2>/dev/null
  scrubf "$O"/c6_*.out
  for f in c6_run_real c6_run_noGO_G1 c6_run_noGO_G11S c6_MUTATE_GO_G11S; do echo "== $f"; tail -3 "$O/$f.out"; done ;;

c6f)
  note "C6(f) (AMENDMENT A1): O12's stop when the rung exists but the G11S output is missing or not of the decided form; MUTATE: K = 8"
  heavy_ok c6f
  R=$L/release_testcopy; rm -rf "$R"; mkdir -p "$R/G11S_seed_mean"
  printf '# DP8 test approval file (test copy only): C6(f)\n' > "$W/OWNER_APPROVAL_TEST.md"
  for s in G1 G3 G4 G5 G6 G7 G8 G10 G11 G11S G14; do echo "GO $s" >> "$W/OWNER_APPROVAL_TEST.md"; done; echo "SKIP G2" >> "$W/OWNER_APPROVAL_TEST.md"
  for s in R0 G1 G2 G3 G4 G5 G6 G7 G8 O9 G10 G11 G11S; do date -u +%FT%TZ > "$R/.done_$s"; done; : > "$R/nss_off_rung_dr4.csv"
  DP8_TEST_RELEASE_DATE=2026-11-01 DP8_TEST_MIN_DISK_GB=1 SBX bash $L/dr4_release_day_TESTCOPY.sh --run > "$O/c6f_no_output.out" 2>&1; echo "exit $?" >> "$O/c6f_no_output.out"
  python3 -I -c "import json; d=json.load(open('$DP7/dp7.json')); d['release']='dr4'; json.dump(d, open('$R/G11S_seed_mean/dp7_dr4.json','w'))"
  DP8_TEST_RELEASE_DATE=2026-11-01 DP8_TEST_MIN_DISK_GB=1 SBX bash $L/dr4_release_day_TESTCOPY.sh --run > "$O/c6f_form_ok.out" 2>&1; echo "exit $?" >> "$O/c6f_form_ok.out"
  python3 -I -c "import json; d=json.load(open('$DP7/dp7.json')); d['release']='dr4'; d['K']=8; json.dump(d, open('$R/G11S_seed_mean/dp7_dr4.json','w'))"
  DP8_TEST_RELEASE_DATE=2026-11-01 DP8_TEST_MIN_DISK_GB=1 SBX bash $L/dr4_release_day_TESTCOPY.sh --run > "$O/c6f_MUTATE_K8.out" 2>&1; echo "exit $?" >> "$O/c6f_MUTATE_K8.out"
  scrubf "$O"/c6f_*.out
  for f in c6f_no_output c6f_form_ok c6f_MUTATE_K8; do echo "== $f"; tail -2 "$O/$f.out" | cut -c1-260; done ;;

post)
  note "post: pins after the lane's runs"
  pins > "$O/pins_after.txt"; tail -1 "$O/pins_after.txt"
  diff "$O/pins_before.txt" "$O/pins_after.txt" > /dev/null && echo "pins unchanged before/after" || echo "PINS CHANGED" ;;

*) echo "usage: $0 pre|c1|c2|c4|c5a|c7a|c7b|testcopy|c3|c5bc|c6pre|c6|c6f|post"; exit 9 ;;
esac
