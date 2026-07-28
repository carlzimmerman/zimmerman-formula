#!/usr/bin/env bash
# Deep-sample lottery campaign across depths 10-14 (the exhaustive grinder's ceiling is depth 9;
# the depth-10 exhaustive build has a CPU-bound dedup pathology that hangs it. Deep-sample samples
# individual candidates via the REAL gates and dodges that entirely).
# Cycles depths 10..14, a fresh seed each pass, BATCH trials per (depth,seed), forever.
# STOPS + writes results_grind/JACKPOT.txt the instant ANY sampled hit survives the FDR gate
# (gate_status != FDR-DEAD) -- that is the only interesting outcome; everything else is a
# CANDIDATE (sampled, non-exhaustive), never a null.
set -u
cd "$(dirname "$0")"
mkdir -p results_grind
DEPTHS="10 11 12 13 14 15 16 17 18"
BATCH="${BATCH:-5000}"
seed="${START_SEED:-100}"          # start above the used seeds (0,1) so batches are fresh tickets
log=results_grind/campaign.log
echo "=== deep-sample campaign start seed=$seed batch=$BATCH depths='$DEPTHS' $(date) ===" >> "$log"
while true; do
  for D in $DEPTHS; do
    python3 grind.py --deep-sample --depth "$D" --seed "$seed" --trials "$BATCH" >> "$log" 2>&1
    hf="results_grind/sample_d${D}_s${seed}/hits.jsonl"
    if [ -f "$hf" ]; then
      surv=$(python3 - "$hf" <<'PY'
import json,sys
hits=[json.loads(l) for l in open(sys.argv[1])]
sv=[h for h in hits if h.get("gate_status")!="FDR-DEAD"]
print(len(sv))
if sv:
    import json as j
    open("results_grind/JACKPOT.txt","w").write(
        "SURVIVOR(S) past the FDR gate -- assess immediately (may still be BAKED-dense, not real):\n"
        + "\n".join(j.dumps(h) for h in sv) + "\n")
PY
)
      if [ "${surv:-0}" != "0" ]; then
        echo "=== JACKPOT: $surv non-FDR-DEAD hit(s) at depth $D seed $seed -- campaign STOPPED $(date) ===" >> "$log"
        exit 0
      fi
    fi
    seed=$((seed+1))
  done
done
