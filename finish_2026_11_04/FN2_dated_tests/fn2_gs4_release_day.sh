#!/bin/bash
# FN2 release-day wrapper for GS4_24110 [CI](2-1), MOUS uid://A001/X3845/X3a (RELEASE_DAY_RUNBOOK.md section 4), checks enforced.
# Recording the result, committing, pushing and deleting the cube are left to the supervising session.
#   bash fn2_gs4_release_day.sh --check   HEAD requests, disk, machine and approval only. No data.
#   bash fn2_gs4_release_day.sh --run     only when OWNER_APPROVAL_2026-11-04_GS4.md marks both files APPROVED, HTTP 200, listed sizes.
# Exit: 0 ran; 2 approval incomplete; 3 not public; 4 size differs (back to the owner); 5 disk; 6 a download failed; 7 the true run crashed.
# The frozen MUTATE is expected to exit 2 here (no control on this window): that is reported, not a failure of this wrapper.
# kappa = 1/2 FITTED; one disc excludes no model; not theory closed.
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT" || exit 9
LANE=finish_2026_11_04/FN2_dated_tests
OUT=$LANE/release_2026_11_28
G=campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_gs4.py
SCR="$(cd "$ROOT/.." && pwd)/_external_data/gs4_release_2026_11_28"
BASE=https://almascience.eso.org/dataPortal
FC=member.uid___A001_X3845_X3a.Pointing-F_sci.spw31.cube.I.pbcor.fits
FK=member.uid___A001_X3845_X3a.Pointing-F_sci.spw25_27_29_31.cont.I.pbcor.fits
NC=7018934400
NK=14777280
APPROVAL=$LANE/OWNER_APPROVAL_2026-11-04_GS4.md
MODE=${1:---check}
mkdir -p "$OUT"
LOG=$OUT/release_day.log
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1

log() {
  local s="$(date -u +%FT%TZ) $*"
  s="${s//$SCR/<scratch>}"; s="${s//$ROOT/<repo>}"; s="${s//$HOME/<home>}"
  echo "$s" | tee -a "$LOG"
}
head_check() { curl -sSIL --max-time 90 "$BASE/$1" 2>/dev/null | tr -d '\r' | awk 'BEGIN{c="none";l="none"} /^HTTP/{c=$2} tolower($1)=="content-length:"{l=$2} END{print c, l}'; }
disk_gb() { df -k /System/Volumes/Data | awk 'NR==2{printf "%d", $4/1048576}'; }
big_1024() { ps -axo rss=,command= | awk '$1 > 1048576 && /1024/ && !/awk/ && !/fn2_gs4_release_day/' | head -3; }
approved() { grep -F "\`$1\`" "$APPROVAL" 2>/dev/null | grep -q "| APPROVED |"; }

log "FN2 GS4 release day, mode $MODE. kappa = 1/2 FITTED; not theory closed."
AOK=1
for f in "$FC" "$FK"; do if approved "$f"; then log "approved: $f"; else log "NOT approved yet: $f"; AOK=0; fi; done
read cc lc < <(head_check "$FC"); read ck lk < <(head_check "$FK")
log "HEAD cube: HTTP $cc, length $lc (listed $NC)"
log "HEAD continuum: HTTP $ck, length $lk (listed $NK)"
DG=$(disk_gb); log "disk free: ${DG} GB (need >= 10)"
[ -n "$(big_1024)" ] && log "processes over 1 GB with 1024 in the command line: present" || log "no 1024-cube process over 1 GB"

if [ "$MODE" = "--check" ]; then
  if [ $AOK -eq 1 ] && [ "$cc" = "200" ] && [ "$ck" = "200" ] && [ "$lc" = "$NC" ] && [ "$lk" = "$NK" ] && [ "$DG" -ge 10 ]; then log "READY TO RUN"
  elif [ "$cc" = "403" ] || [ "$ck" = "403" ]; then log "NOT YET PUBLIC (403): wait for 2026-11-28 18:25:24 UTC"
  else log "NOT READY: see the lines above"; fi
  exit 0
fi
[ "$MODE" = "--run" ] || { log "unknown mode"; exit 9; }
[ $AOK -eq 1 ] || { log "STOP: the approval record doesn't mark both files APPROVED"; exit 2; }
if [ "$cc" != "200" ] || [ "$ck" != "200" ]; then log "STOP: NOT YET PUBLIC"; exit 3; fi
if [ "$lc" != "$NC" ] || [ "$lk" != "$NK" ]; then log "STOP: SIZE DIFFERS from the approved listing; back to the owner"; exit 4; fi
[ "$DG" -ge 10 ] || { log "STOP: disk below 10 GB"; exit 5; }
mkdir -p "$SCR"
waited=0
while [ -n "$(big_1024)" ] && [ $waited -lt 43200 ]; do log "a 1024-cube process is live: waiting 300 s"; sleep 300; waited=$((waited+300)); done

for pair in "$FC:$NC" "$FK:$NK"; do
  f=${pair%%:*}; n=${pair##*:}
  log "download $f"
  curl -sSL --fail -o "$SCR/$f" "$BASE/$f"; rc=$?
  got=$(stat -f %z "$SCR/$f" 2>/dev/null || echo 0)
  log "curl exit $rc; bytes $got (expected $n)"
  if [ $rc -ne 0 ] || [ "$got" != "$n" ]; then log "STOP: download failed or short; rerun"; exit 6; fi
  shasum -a 256 "$SCR/$f" | awk '{print $1}' > "$SCR/$f.sha256"; log "sha256 $(cat "$SCR/$f.sha256")"
done

log "score: true run (frozen verdict kernel), then MUTATE (expected exit 2: no control on this window), then readings n1 n2 v3aq"
nice -n 10 python3 -B $G --cube "$SCR/$FC" --cont "$SCR/$FK" > "$SCR/gs4_true.stdout" 2>&1; rt=$?; log "cfg942_gs4 true exit $rt"
nice -n 10 python3 -B $G --cube "$SCR/$FC" --cont "$SCR/$FK" --mutate > "$SCR/gs4_mut.stdout" 2>&1; log "cfg942_gs4 MUTATE exit $? (2 = not runnable on this window, as FN2 found)"
for k in n1 n2 v3aq; do CFG942_KERNEL=$k nice -n 10 python3 -B $G --cube "$SCR/$FC" --cont "$SCR/$FK" > "$SCR/gs4_$k.stdout" 2>&1; log "cfg942_gs4 kernel $k exit $?"; done
[ $rt -eq 0 ] || [ $rt -eq 1 ] || { log "STOP: the true run exited $rt (2 = a frozen file or seal mismatch); see the harness output"; exit 7; }
for f in "$SCR"/*.sha256; do cp "$f" "$OUT/"; done
log "done. Recording (RESULT_2026-11-28.md), commit with explicit paths, push and deleting the cube are the supervising session's."
exit 0
