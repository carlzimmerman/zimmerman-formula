#!/usr/bin/env bash
# autoloop.sh -- indefinite one-task-per-session autoresearch loop for the local worker.
#
# Run FROM THE REPO ROOT in a terminal (Android Studio's terminal pane is fine):
#     bash qwen_38_experiment/autoloop.sh
# Stop it gracefully:   touch qwen_38_experiment/STOP     (or Ctrl-C)
#
# Each iteration launches a FRESH headless Claude Code session (fresh context -- this is
# what stops the timeout death-spiral), pointed at whatever backend the environment
# already configures (your Ollama Qwen). One task per iteration; LEDGER.md is the memory.
#
# Ollama tips (set BEFORE starting, in the same shell):
#     export OLLAMA_KEEP_ALIVE=24h      # keep the model in VRAM between iterations
#     (and keep the model's num_ctx modest, 16-32k -- oversized contexts cause timeouts)

set -u
DIR="$(cd "$(dirname "$0")" && pwd)"

export ANTHROPIC_BASE_URL="${OLLAMA_URL:-http://localhost:11434}"
export ANTHROPIC_API_KEY="ollama"
export ANTHROPIC_AUTH_TOKEN="ollama"
case "$ANTHROPIC_BASE_URL" in
  http://localhost*|http://127.0.0.1*) ;;
  *) echo "[autoloop] REFUSING TO START: ANTHROPIC_BASE_URL is not a local endpoint" \
        "($ANTHROPIC_BASE_URL). This loop must NEVER touch the Anthropic API."; exit 1;;
esac
echo "[autoloop] endpoint locked to $ANTHROPIC_BASE_URL (local only)"
REPO="$(dirname "$DIR")"
LOGDIR="$DIR/runs/loop_logs"
mkdir -p "$LOGDIR"
ITER_TIMEOUT="${ITER_TIMEOUT:-3600}"     # seconds per task session
WORKER_MODEL="${WORKER_MODEL:-}"         # e.g. qwen3.8:27b-mlx; empty = default model
MAX_TURNS="${MAX_TURNS:-40}"
COOLDOWN="${COOLDOWN:-15}"               # pause between sessions

trap 'echo; echo "[autoloop] Ctrl-C -- stopping."; exit 130' INT TERM
echo "[autoloop] starting; stop with Ctrl-C or: touch $DIR/STOP"
i=0
while true; do
  [ -f "$DIR/STOP" ] && { echo "[autoloop] STOP file found -- exiting."; rm -f "$DIR/STOP"; break; }
  i=$((i+1))
  stamp="$(date +%Y%m%d_%H%M%S)"
  log="$LOGDIR/iter_${stamp}.log"
  before=$(wc -l < "$DIR/LEDGER.md")
  echo "[autoloop] iter $i -> $log"
  ( cd "$REPO" && timeout "$ITER_TIMEOUT" claude -p "$(cat "$DIR/LOOP_PROMPT.md")" \
        ${WORKER_MODEL:+--model "$WORKER_MODEL"} \
        --max-turns "$MAX_TURNS" --dangerously-skip-permissions ) > "$log" 2>&1
  rc=$?
  after=$(wc -l < "$DIR/LEDGER.md")
  new=$((after - before))
  echo "[autoloop] iter $i done (rc=$rc, +$new ledger rows): $(tail -1 "$DIR/LEDGER.md" | cut -c1-120)"
  if [ "$new" -eq 0 ]; then
    echo "[autoloop] no ledger progress this iteration (rc=$rc) -- see $log"
  fi
  sleep "$COOLDOWN"
done
