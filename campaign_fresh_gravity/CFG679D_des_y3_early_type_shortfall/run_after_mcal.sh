#!/bin/sh
# CFG679D: queued fetches that must NOT share the DES server with the metacal download. Waits for "mcal: COMPLETE" in
# ../_external_data/cfg679_des/download_mcal.log, then (each step resumable, restarted after server timeouts like run_download.sh):
#   1 listcols index  -> index_columns.json (names + layout of index/select*)
#   2 index           -> select_bin1..4 row lists
#   3 smid            -> stellar-mass coadd_obj_id (GOLD match key)
#   4 resp            -> metacal unsheared R11, R22 on 20 seeded random chunks (resp_chunks.json)
#   5 listcols gold   -> gold_columns.json + gold_choice.json (SOF corrected g, r, i, else GOLD 2.2 default model magnitudes)
#   6 gold            -> GOLD coadd_object_id + g, r, i; --max-gb = what is left of the owner's 30 GB budget (aborts, logged, if over)
#   7 selresp         -> optional: sheared selection lists inside the 20 response chunks (else selection response neglected)
# It does not run the measurement. Network-only jobs: --light-guard (pause only when free+inactive < 8 GB).
cd "$(dirname "$0")"
D=../_external_data/cfg679_des
OUT=run_after_mcal.out
echo "$(date '+%F %T') waiting for mcal: COMPLETE" >> $OUT
while ! grep -q "mcal: COMPLETE" $D/download_mcal.log 2>/dev/null; do sleep 300; done
echo "$(date '+%F %T') mcal COMPLETE seen; starting the queue" >> $OUT
step() {  # step <done-test-command> <args...>
  t="$1"; shift
  for i in $(seq 1 200); do
    sh -c "$t" && return 0
    nice -n 10 python3 cfg679_download.py "$@" --threads 2 --light-guard >> $OUT 2>&1
    sh -c "$t" && return 0
    grep -q "ABORT" $D/download_$1.log 2>/dev/null && { echo "$(date '+%F %T') $1 ABORTED (see log)" >> $OUT; return 1; }
    sleep 120
  done
  return 1
}
step "test -f $D/index_columns.json" listcols --file index
step "grep -q 'index: COMPLETE' $D/download_index.log 2>/dev/null" index
step "grep -q 'smid: COMPLETE' $D/download_smid.log 2>/dev/null" smid --max-gb 30
step "grep -q 'resp: COMPLETE' $D/download_resp.log 2>/dev/null" resp --max-gb 30
step "test -f $D/gold_choice.json" listcols --file gold
LEFT=$(python3 -c "
import json, glob, os
D='$D'; used=0.0
for pj in glob.glob(os.path.join(D, '*', 'pieces.json')):
    tag = os.path.basename(os.path.dirname(pj))
    if tag == 'gold': continue
    js = json.load(open(pj))
    for c, v in js.items():
        n = len(glob.glob(os.path.join(D, tag, c, '[0-9]*.npy')))
        used += sum(p[1] for p in v) * (n / max(len(v), 1)) if tag != 'resp' else 20 * v[0][1]
for f in glob.glob(os.path.join(D, 'index', '*', '*.npy')) + glob.glob(os.path.join(D, 'selresp', '*', '*.npy')):
    used += os.path.getsize(f)
print(round(30.0 - used / 1e9, 3))")
echo "$(date '+%F %T') budget left for GOLD: $LEFT GB" >> $OUT
step "grep -q 'gold: COMPLETE' $D/download_gold.log 2>/dev/null" gold --max-gb $LEFT
step "test -f $D/selresp_done.json" selresp
echo "$(date '+%F %T') RUN_AFTER_MCAL_DONE" >> $OUT
