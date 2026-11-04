#!/bin/bash
# FN2 release-day wrapper for ALMA MOUS uid://A001/X3788/Xbfd2: RELEASE_DAY_RUNBOOK.md steps 1-8, with its checks enforced.
# Step 9 (RESULT_2026-11-06.md, commit, push, deleting the cutouts) is left to the supervising session.
#   bash fn2_release_day.sh --check   HEAD requests, disk, machine and approval only. No data.
#   bash fn2_release_day.sh --run     only with OWNER_APPROVAL_2026-11-04_ALMA.md present, HTTP 200 and the listed sizes.
# Exit: 0 ran (science outcome is in the outputs); 2 no approval; 3 not public yet; 4 size differs (back to the owner);
#       5 disk; 6 a stream or provenance check failed; 7 a scorer crashed.
# kappa = 1/2 FITTED; one disc excludes no model; not theory closed.
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT" || exit 9
LANE=finish_2026_11_04/FN2_dated_tests
OUT=$LANE/release_2026_11_06
AC1=rebuild_2026_10_22/AC1_alma_condor_predictions
H=campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_u4.py
SCR="$(cd "$ROOT/.." && pwd)/_external_data/alma_release_2026_11_06"
BASE=https://almascience.eso.org/dataPortal
F25=member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw25.cube.I.pbcor.fits
F23=member.uid___A001_X3788_Xbfd2.UDS28473_sci.spw23.cube.I.pbcor.fits
N25=34749031680
N23=38556031680
APPROVAL=$LANE/OWNER_APPROVAL_2026-11-04_ALMA.md
MODE=${1:---check}
mkdir -p "$OUT"
LOG=$OUT/release_day.log
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1

log() {
  local s="$(date -u +%FT%TZ) $*"
  s="${s//$SCR/<scratch>}"; s="${s//$ROOT/<repo>}"; s="${s//$HOME/<home>}"
  echo "$s" | tee -a "$LOG"
}

head_check() {   # file expected_bytes -> prints "code length", following redirects to the serving mirror
  curl -sSIL --max-time 90 "$BASE/$1" 2>/dev/null | tr -d '\r' | awk 'BEGIN{c="none";l="none"} /^HTTP/{c=$2} tolower($1)=="content-length:"{l=$2} END{print c, l}'
}

disk_gb() { df -k /System/Volumes/Data | awk 'NR==2{printf "%d", $4/1048576}'; }

big_1024() { ps -axo rss=,command= | awk '$1 > 1048576 && /1024/ && !/awk/ && !/fn2_release_day/' | head -3; }

prov_ok() {   # provenance.json expected_bytes -> 0 if source_bytes match and the box is square (not clipped)
  python3 -I -c "
import json,sys
p=json.load(open(sys.argv[1])); b=p['box']
ok=p['source_bytes']==int(sys.argv[2]) and (b[1]-b[0])==(b[3]-b[2])
print('provenance', 'OK' if ok else 'FAIL', 'source_bytes', p['source_bytes'], 'box', b)
sys.exit(0 if ok else 1)" "$1" "$2"
}

log "FN2 release day, mode $MODE. kappa = 1/2 FITTED; not theory closed."
[ -f "$APPROVAL" ] && log "approval file present: $APPROVAL" || log "approval file MISSING: $APPROVAL"
read c25 l25 < <(head_check "$F25"); read c23 l23 < <(head_check "$F23")
log "HEAD spw25: HTTP $c25, length $l25 (listed $N25)"
log "HEAD spw23: HTTP $c23, length $l23 (listed $N23)"
DG=$(disk_gb); log "disk free: ${DG} GB (need >= 10)"
B=$(big_1024); [ -n "$B" ] && log "processes over 1 GB with 1024 in the command line: present" || log "no 1024-cube process over 1 GB"
if [ -d /tmp/alma_v14_pydeps ]; then PY_AC1="env PYTHONPATH=/tmp/alma_v14_pydeps /usr/bin/python3"; log "AC1 scorer: pinned v1.4 environment"
else PY_AC1="python3"; log "AC1 scorer: default python3 (pinned environment gone; ENV OK, NUMBERS DRIFT per fn2_a1_env_default.out)"; fi

if [ "$MODE" = "--check" ]; then
  if [ "$c25" = "200" ] && [ "$c23" = "200" ] && [ "$l25" = "$N25" ] && [ "$l23" = "$N23" ] && [ "$DG" -ge 10 ]; then log "READY TO RUN"
  elif [ "$c25" = "403" ] || [ "$c23" = "403" ]; then log "NOT YET PUBLIC (403): wait for 2026-11-06 02:42:31 UTC"
  else log "NOT READY: see the lines above"; fi
  exit 0
fi
[ "$MODE" = "--run" ] || { log "unknown mode"; exit 9; }
[ -f "$APPROVAL" ] || { log "STOP: no owner approval on record"; exit 2; }
if [ "$c25" != "200" ] || [ "$c23" != "200" ]; then log "STOP: NOT YET PUBLIC"; exit 3; fi
if [ "$l25" != "$N25" ] || [ "$l23" != "$N23" ]; then log "STOP: SIZE DIFFERS from the approved listing; back to the owner"; exit 4; fi
[ "$DG" -ge 10 ] || { log "STOP: disk below 10 GB"; exit 5; }
mkdir -p "$SCR"
waited=0
while [ -n "$(big_1024)" ] && [ $waited -lt 43200 ]; do log "a 1024-cube process is live: waiting 300 s (runbook step 2)"; sleep 300; waited=$((waited+300)); done
set -o pipefail

log "step 4: stream spw25, keep the +-4.5 arcsec U4_28473 cutout"
curl -sSL --fail "$BASE/$F25" | python3 -I $AC1/ac1_stream_cutout.py - "$SCR/U4_28473_spw25_cut.fits" 34.422382000017684 -5.181044500002704 4.5 > "$SCR/spw25.stdout" 2>> "$SCR/spw25.stderr"
rc=$?; log "stream spw25 exit $rc"
[ $rc -eq 0 ] || { log "STOP: spw25 stream failed; rerun step 4 (no --retry: a retried stream repeats bytes)"; exit 6; }
prov_ok "$SCR/U4_28473_spw25_cut.fits.provenance.json" $N25 | while read l; do log "$l"; done
prov_ok "$SCR/U4_28473_spw25_cut.fits.provenance.json" $N25 >/dev/null || { log "STOP: spw25 provenance check failed"; exit 6; }
cp "$SCR/U4_28473_spw25_cut.fits.provenance.json" "$OUT/U4_28473_spw25_cut.provenance.json"

log "step 5: score U4_28473 (AC1; G1-3D decides; all-three-starts gate)"
nice -n 10 $PY_AC1 -B $AC1/ac1_score.py --cube "$SCR/U4_28473_spw25_cut.fits" --output-dir $OUT/ac1 > "$SCR/ac1_true.stdout" 2>&1
rt=$?; log "ac1_score true run exit $rt (expect 0)"
nice -n 10 $PY_AC1 -B $AC1/ac1_score.py --cube "$SCR/U4_28473_spw25_cut.fits" --mutate --output-dir $OUT/ac1 > "$SCR/ac1_mut.stdout" 2>&1
rm=$?; log "ac1_score MUTATE exit $rm (1 = bites; trivial if the true run found no line)"
[ $rt -eq 0 ] || { log "STOP: the AC1 true run did not exit 0"; exit 7; }

log "step 6: stream spw23, keep the +-13 arcsec U4_27928 cutout"
curl -sSL --fail "$BASE/$F23" | python3 -I $AC1/ac1_stream_cutout.py - "$SCR/U4_27928_spw23_cut.fits" 34.42319107055664 -5.182923793792725 13 > "$SCR/spw23.stdout" 2>> "$SCR/spw23.stderr"
rc=$?; log "stream spw23 exit $rc"
rowA=1
if [ $rc -ne 0 ]; then log "row A: spw23 stream failed; rerun step 6"; rowA=0
else
  prov_ok "$SCR/U4_27928_spw23_cut.fits.provenance.json" $N23 | while read l; do log "$l"; done
  if prov_ok "$SCR/U4_27928_spw23_cut.fits.provenance.json" $N23 >/dev/null; then cp "$SCR/U4_27928_spw23_cut.fits.provenance.json" "$OUT/U4_27928_spw23_cut.provenance.json"
  else log "row A: box clipped or bytes differ: the imaged field may not cover this offset (CFG806 note 2026-11-01); row A stops"; rowA=0; fi
fi

if [ $rowA -eq 1 ]; then
  log "step 7: score U4_27928 (CFG806 plan: nu_mono verdict, MUTATE, then readings n1 n2 v3aq)"
  nice -n 10 python3 -B $H --cube "$SCR/U4_27928_spw23_cut.fits" > "$SCR/u4_true.stdout" 2>&1; log "cfg942_u4 true exit $?"
  nice -n 10 python3 -B $H --cube "$SCR/U4_27928_spw23_cut.fits" --mutate > "$SCR/u4_mut.stdout" 2>&1; log "cfg942_u4 MUTATE exit $? (window +2000 is 7 % inside spw23: non-diagnostic)"
  for k in n1 n2 v3aq; do CFG942_KERNEL=$k nice -n 10 python3 -B $H --cube "$SCR/U4_27928_spw23_cut.fits" > "$SCR/u4_$k.stdout" 2>&1; log "cfg942_u4 kernel $k exit $?"; done
fi

log "step 8: scorecard rows"
U4J=campaign_fresh_gravity/CFG942_alma_scoring_readiness/cfg942_u4_RELEASE_results.json
if [ -f "$U4J" ]; then python3 -B $LANE/fn2_scorecard.py --read $OUT/ac1/ac1_score_RELEASE.json --u4 $U4J --tag release_2026_11_06 > "$OUT/scorecard_release.out" 2>&1
else python3 -B $LANE/fn2_scorecard.py --read $OUT/ac1/ac1_score_RELEASE.json --tag release_2026_11_06 > "$OUT/scorecard_release.out" 2>&1; fi
log "scorecard reader exit $?"
for f in "$OUT"/scorecard_release.out "$OUT"/ac1/*; do [ -f "$f" ] && sed -i '' "s#$SCR#<scratch>#g; s#$ROOT/##g; s#$HOME#<home>#g" "$f"; done
log "steps 1-8 done. Step 9 (RESULT_2026-11-06.md, home-path check, commit with explicit paths, push, delete cutouts) is the supervising session's."
exit 0
