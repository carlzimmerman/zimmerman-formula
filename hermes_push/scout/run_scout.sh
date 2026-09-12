#!/usr/bin/env bash
# The always-on loop. One cycle per interval, each cycle producing exactly one output.
# Configure AGENT_CMD so that "$AGENT_CMD <message>" runs the agent headlessly on that message.
# With the Hermes CLI on this machine, the working form is:
#   export AGENT_CMD='hermes --in . --yolo -m <model> -z'
# The -z flag takes the prompt as its argument and runs without a terminal; --in sets the working directory; --yolo lets it use
# tools without stopping to ask. Add --provider if the model needs one. Test a single cycle before letting it loop:
#   ./hermes_push/scout/run_scout.sh 60 1
# Usage from the repository root:  ./hermes_push/scout/run_scout.sh [interval_seconds] [max_cycles]
# Alternatively schedule it with the agent's own scheduler instead of this loop; see README.md in this folder.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT"
INT="${1:-1800}"; MAX="${2:-0}"; N=0
: "${AGENT_CMD:?set AGENT_CMD to your local model's non-interactive command (see comments at the top of this file)}"
while :; do
  N=$((N+1))
  echo "=== scout cycle $N  $(date -u +%FT%TZ)"
  MSG="Read hermes_push/scout/SCOUT.md and follow it for exactly one cycle. This is cycle $N, so write $( [ $((N%2)) -eq 1 ] && echo 'a Lean candidate' || echo 'a proposal' ). Read git log --oneline -15 and the newest entries of fable_independent_2026/FINDINGS.md first. Produce one output, verify it if it is Lean, append it to hermes_push/scout/PROPOSALS.md, and stop."
  $AGENT_CMD "$MSG" || echo "  (agent exited non-zero; continuing)"
  if ! git diff --quiet -- hermes_push/scout || [ -n "$(git ls-files --others --exclude-standard hermes_push/scout)" ]; then
    if git status --porcelain | grep -v '^.. hermes_push/scout' | grep -q .; then
      echo "  REFUSING TO COMMIT: the agent touched files outside hermes_push/scout -- inspect with git status and revert them"
    else
      git add hermes_push/scout && git commit -q -m "scout: cycle $N" && git push -q origin main 2>/dev/null || true
      echo "  committed"
    fi
  else
    echo "  no output this cycle"
  fi
  [ "$MAX" -gt 0 ] && [ "$N" -ge "$MAX" ] && break
  sleep "$INT"
done
