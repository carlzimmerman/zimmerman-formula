#!/usr/bin/env bash
# Iterative driver: N sessions of the agent, each one iteration of LOOP.md; commit after each session if the guard passes.
# Configure AGENT_CMD to your local agent's CLI. It must accept a system-prompt file and a user message and run non-interactively, e.g.
#   export AGENT_CMD='hermes run --system-file hermes_push/PROMPT_HERMES.md --cwd . --allow-write hermes_push --message'
# Usage: ./hermes_push/run_loop.sh 20      (from the repository root)
set -euo pipefail
N="${1:-10}"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
: "${AGENT_CMD:?set AGENT_CMD to your agent's non-interactive command (see comments)}"
MSG='Read hermes_push/LOOP.md, hermes_push/STATE.md, hermes_push/CANDIDATES.md and hermes_push/SCORECARD.md. Run exactly one iteration of the loop: register the candidate, compute in the kill order, write the H-entry, update SCORECARD.md and CANDIDATES.md, rewrite STATE.md, end with one sentence.'
for i in $(seq 1 "$N"); do
  echo "=== hermes iteration $i / $N  $(date -u +%FT%TZ)"
  $AGENT_CMD "$MSG" || { echo "agent exited non-zero at iteration $i"; }
  python3 hermes_push/harness.py || { echo "commit guard failed at iteration $i; fix hermes_push/ before continuing"; exit 1; }
  if ! git diff --quiet -- hermes_push || [ -n "$(git ls-files --others --exclude-standard hermes_push)" ]; then
    git add hermes_push && git commit -q -m "hermes: iteration $i -- $(sed -n 's/^one-sentence status: //p' hermes_push/STATE.md | head -1 | cut -c1-160)" && git push -q origin main || true
  fi
done
