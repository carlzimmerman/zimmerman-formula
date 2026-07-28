#!/usr/bin/env bash
# parallel_campaign.sh SHARD_INDEX [BATCH]
#
# One deep-sample worker, fully isolated from every other worker and from the original campaign.
# WHY THIS EXISTS: the deep-sample path is single-threaded (measured: 99% of ONE core, 0.08 GB RSS) on
# a 16-core / 69 GB box, so ~13 cores sat idle. Memory is a non-issue in sample mode -- the 40 GB cap
# only ever bound the EXHAUSTIVE build phase -- so this is embarrassingly parallel.
#
# ISOLATION, which is the whole point:
#   * ATOMOS_RESULTS_DIR gives each shard its own results dir, so state.json (atomic write, but
#     concurrent read-modify-write silently LOSES UPDATES) and the append-only SAMPLE_LEDGER.jsonl
#     (interleaved lines would corrupt the hit record) are never shared.
#   * Seeds start at 100000 + 10000*SHARD, so no shard ever repeats another's work or the original
#     campaign's (which is down near seed ~640).
#   * A shard stops on ITS OWN jackpot AND on any other shard's, via the shared flag file below.
#
# STATISTICAL NOTE, so this is not mistaken for buying more than it does: more sampling raises the
# probability of hitting a real relation LINEARLY in the number of expressions tested, but it does NOT
# lower the evidence bar. The bits threshold for a CLAIM stays log2(N(D)) + margin, because the claim is
# that an expression is distinguished among ALL expressions at that depth -- not that the search got
# lucky among the ones it happened to draw. Parallelism buys COVERAGE, not SIGNIFICANCE. Net positive,
# since coverage grows linearly while the bar is fixed.
set -uo pipefail
cd "$(dirname "$0")"

SHARD="${1:?usage: parallel_campaign.sh SHARD_INDEX [BATCH]}"
BATCH="${2:-5000}"
DEPTHS="10 11 12 13 14 15 16 17 18"

export ATOMOS_RESULTS_DIR="$PWD/results_shard${SHARD}"
mkdir -p "$ATOMOS_RESULTS_DIR"
log="$ATOMOS_RESULTS_DIR/campaign.log"
GLOBAL_STOP="$PWD/results_grind/JACKPOT_ANY.flag"

seed=$(( 100000 + 10000*SHARD ))
echo "=== shard $SHARD start seed=$seed batch=$BATCH depths='$DEPTHS' $(date) ===" >> "$log"

while true; do
  for D in $DEPTHS; do
    # stop if any shard (or the original campaign) already found something
    if [ -f "$GLOBAL_STOP" ] || [ -f "$PWD/results_grind/JACKPOT.txt" ]; then
      echo "=== shard $SHARD halting: jackpot flag present $(date) ===" >> "$log"; exit 0
    fi
    python3 grind.py --deep-sample --depth "$D" --seed "$seed" --trials "$BATCH" >> "$log" 2>&1
    hf="$ATOMOS_RESULTS_DIR/sample_d${D}_s${seed}/hits.jsonl"
    if [ -f "$hf" ]; then
      # FIELD NAME MATTERS: the schema key is `gate_status`, and its dead value is "FDR-DEAD".
      # A first version of this script tested r["fdr_dead"] / r["verdict"], neither of which exists, so
      # NOTHING matched and every FDR-DEAD hit was counted as a survivor -- a false JACKPOT on the very
      # first pass (29 "survivors", all FDR-DEAD). This is now the same filter the original campaign has
      # run for three days without a false trip. Do not "simplify" it.
      surv=$(python3 - "$hf" <<'PY'
import json, sys
hits = []
for ln in open(sys.argv[1]):
    try: hits.append(json.loads(ln))
    except Exception: pass
sv = [h for h in hits if h.get("gate_status") != "FDR-DEAD"]
print(len(sv))
if sv:
    # BITS_RULE read-out, straight from the hit schema: fdr_bits is the summed-bits number, and
    # kernel_passed / interlock_passed are Gate B and Gate C. k=1 is noise however many digits show.
    with open(sys.argv[1] + ".SURVIVORS.txt", "w") as f:
        for h in sv:
            f.write(f"target={h.get('target')} rel={h.get('rel_error')} n_sigma={h.get('n_sigma')} "
                    f"fdr_bits={h.get('fdr_bits')} kernel={h.get('kernel_passed')} "
                    f"interlock={h.get('interlock_passed')} tell={h.get('gate_tell')}\n"
                    f"  formula: {h.get('formula')}\n")
PY
)
      if [ "${surv:-0}" -gt 0 ] 2>/dev/null; then
        {
          echo "shard=$SHARD depth=$D seed=$seed survivors=$surv $(date)"
          echo "READ-OUT RULE (BITS_RULE.py): interesting iff summed bits over interlocked FITTABLE"
          echo "targets > log2(N(D)) + 10, AND the r_tau_mu out-of-sample sigma < 2. A Koide Q pass is"
          echo "NOT evidence (exact 2/3 is 0.91 sigma from measured and known since Koide 1981)."
          echo "hits: $hf"
        } > "$ATOMOS_RESULTS_DIR/JACKPOT.txt"
        cp "$ATOMOS_RESULTS_DIR/JACKPOT.txt" "$GLOBAL_STOP" 2>/dev/null
        echo "=== shard $SHARD JACKPOT: $surv survivor(s) depth $D seed $seed $(date) ===" >> "$log"
        exit 0
      fi
    fi
    seed=$((seed+1))
  done
done
