#!/usr/bin/env bash
# VERIFY_ALL.sh — unattended, single-file answer to "are all the gates correct, with no bugs?"
#
# Runs every self-check the project has, in order, and writes ONE readable verdict file:
#   results_grind/VERIFY_ALL_STATUS.txt
# Nothing here is a search. Every step either reproduces committed ground truth or re-derives a
# committed number, so a FAIL means the machinery moved, not that physics was found.
#
# WHY IT EXISTS: on 2026-07-27 four bugs surfaced in one session, three of them mine, and every single
# one was caught by RUNNING a check rather than reasoning about it. So the checks get run, unattended,
# and the result is written down whether or not anyone is watching.
set -uo pipefail
cd "$(dirname "$0")"
ST="results_grind/VERIFY_ALL_STATUS.txt"
mkdir -p results_grind
: > "$ST"
say(){ echo "$*" >> "$ST"; }
say "VERIFY_ALL — started $(date '+%F %T')"
say "=============================================================================="

# ---- 1. replay gates: the streamed build must reproduce committed depth-6/7 EXACTLY
for D in 6 7; do
  say ""; say "[replay depth $D]"
  if python3 grind.py --replay "$D" > "/tmp/verify_replay${D}.log" 2>&1; then
    say "  PASS — reproduces committed ground truth exactly"
  else
    say "  ** FAIL ** — see /tmp/verify_replay${D}.log"
  fi
  grep -E "computed=|REPLAY depth" "/tmp/verify_replay${D}.log" 2>/dev/null \
    | sed 's/^/    /' >> "$ST"
done

# ---- 2. holdout scoping: searches must exclude it, replay/retention must include it
say ""; say "[holdout scoping]"
python3 - >> "$ST" 2>&1 <<'PY'
import sys; sys.path.insert(0, '.')
from exhaust_parallel import sm_target_keys
from targets.pdg_constants import load, HOLDOUT_KEYS
import argparse, run_atomos
ds = load()
srch = sm_target_keys()
repl = sm_target_keys(include_holdout=True)
sel  = [t.key for t in run_atomos.select_targets(argparse.Namespace(target=None), ds)]
leak_s = [k for k in srch if k in HOLDOUT_KEYS]
leak_sel = [k for k in sel if k in HOLDOUT_KEYS]
has_r = [k for k in repl if k in HOLDOUT_KEYS]
print(f"    search list (sm_target_keys)     : {len(srch)} targets, leak={leak_s or 'NONE'}")
print(f"    search list (select_targets)     : {len(sel)} targets, leak={leak_sel or 'NONE'}")
print(f"    replay list (include_holdout)    : {len(repl)} targets, holdout present={has_r}")
ok = (not leak_s) and (not leak_sel) and len(has_r) >= 1
print(f"    {'PASS' if ok else '** FAIL **'} — searches exclude the holdout; replay includes it")
# scoring path must still work on a held-back target
s, r, p = ds.score_holdout('koide_Q_lep', 2/3)
print(f"    score_holdout(koide_Q_lep, 2/3)  : {s:.2f} sigma, pass={p}  (2/3 is Koide 1981, NOT evidence)")
PY

# ---- 3. sharded-build correctness gate (the 19%-loss bug lived here)
say ""; say "[sharded build vs serial, depth 8]"
if [ -f results_grind/depth_8/build_meta_sharded.json ]; then
  python3 - >> "$ST" 2>&1 <<'PY'
import json
s = json.load(open("results_grind/depth_8/build_meta.json"))
m = json.load(open("results_grind/depth_8/build_meta_sharded.json"))
ok_r = m["raw_candidates"] == s["raw_candidates"]
ok_d = m["distinct_by_value"] == s["distinct_by_value"]
print(f"    raw      sharded={m['raw_candidates']:,} serial={s['raw_candidates']:,} "
      f"{'MATCH' if ok_r else 'MISMATCH'}")
print(f"    distinct sharded={m['distinct_by_value']:,} serial={s['distinct_by_value']:,} "
      f"{'MATCH' if ok_d else 'MISMATCH'}")
print(f"    {'PASS' if (ok_r and ok_d) else '** FAIL — do NOT trust the sharded path **'}")
PY
else
  say "    (validation still running or not yet merged — check /tmp/val8b.log)"
  grep -E "VALIDATION|MATCH|MISMATCH" /tmp/val8b.log 2>/dev/null | sed 's/^/    /' >> "$ST"
fi

# ---- 4. the committed physics scripts in the main repo still run clean
say ""; say "[zimmerman-formula scripts, exit codes]"
R=/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews
for f in mi_dcac_branch_settled_2026 mi_omegac_anchor_2026 mi_wb_gate_fork_2026 \
         mi_wb_cubic_rise_2026 mi_wb_exponent_pipeline_2026 mi_wb_dr3_feasibility_2026 \
         mi_particle_vs_mode_2026 Z_provenance_audit_2026 two_loop_vs_alpha_2026 \
         alpha_12pi_identity_audit_2026 mi_bh_unravel_desitter_2026 mi_varying_constants_bridge_2026; do
  if timeout 900 python3 "$R/$f.py" >/tmp/vf.log 2>&1; then
    say "    exit 0   $f   $(grep -oE '[0-9]+/[0-9]+ checks PASS' /tmp/vf.log | tail -1)"
  else
    say "    ** NONZERO EXIT **  $f"
  fi
done

say ""; say "=============================================================================="
say "VERIFY_ALL — finished $(date '+%F %T')"
grep -c '\*\* FAIL\|NONZERO' "$ST" | awk '{print ($1==0) ? "OVERALL: ALL CHECKS PASS" : "OVERALL: "$1" FAILURE LINE(S) -- read above"}' >> "$ST"
