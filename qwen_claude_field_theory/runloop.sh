#!/usr/bin/env bash
# runloop.sh -- overnight loop, one idea per fresh session.
#   bash qwen_claude_field_theory/runloop.sh
# stop with:  touch qwen_claude_field_theory/STOP     (or Ctrl-C)
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"; REPO="$(dirname "$DIR")"
export ANTHROPIC_BASE_URL="${OLLAMA_URL:-http://localhost:11434}"
export ANTHROPIC_API_KEY="ollama"; export ANTHROPIC_AUTH_TOKEN="ollama"
case "$ANTHROPIC_BASE_URL" in
  http://localhost*|http://127.0.0.1*) ;;
  *) echo "[loop] REFUSING: endpoint $ANTHROPIC_BASE_URL is not local."; exit 1;;
esac
export API_TIMEOUT_MS="${API_TIMEOUT_MS:-600000}"
ITER_TIMEOUT="${ITER_TIMEOUT:-1500}"     # 25 min hard cap per idea -- the anti-stall guard
MAX_TURNS="${MAX_TURNS:-40}"
WORKER_MODEL="${WORKER_MODEL:-}"
LOGS="$DIR/runs/logs"; mkdir -p "$LOGS"
trap 'echo; echo "[loop] stopping."; exit 130' INT TERM
echo "[loop] endpoint $ANTHROPIC_BASE_URL (local only); ${ITER_TIMEOUT}s cap per idea"
i=0
while true; do
  [ -f "$DIR/STOP" ] && { echo "[loop] STOP found."; rm -f "$DIR/STOP"; break; }
  i=$((i+1)); stamp="$(date +%Y%m%d_%H%M%S)"; log="$LOGS/i_${stamp}.log"
  before=$(grep -c '^| I' "$DIR/LEDGER.md" 2>/dev/null || echo 0)
  ( cd "$REPO" && timeout "$ITER_TIMEOUT" claude -p "Run: python $DIR/next_idea.py
Then follow its instructions exactly. One idea only, then end." \
      ${WORKER_MODEL:+--model "$WORKER_MODEL"} \
      --max-turns "$MAX_TURNS" --dangerously-skip-permissions ) > "$log" 2>&1
  rc=$?
  after=$(grep -c '^| I' "$DIR/LEDGER.md" 2>/dev/null || echo 0)
  nres=$(ls -1 "$DIR/results"/*.md 2>/dev/null | wc -l | tr -d ' ')
  nscr=$(ls -1 "$DIR/runs"/*.py 2>/dev/null | wc -l | tr -d ' ')
  echo "[loop] iter $i rc=$rc  ledger $before -> $after  results=$nres scripts=$nscr  $(tail -1 "$DIR/LEDGER.md" | cut -c1-90)"
  [ "$after" -eq "$before" ] && echo "[loop]   NO LEDGER PROGRESS -- see $log"
  if [ "$after" -gt "$before" ] && [ "$nres" -lt "$after" ]; then
    echo "[loop]   WARNING: ledger row written with NO result file -- review $log"
  fi
  sleep 10
done
