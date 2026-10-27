#!/bin/bash
# One watcher tick: refresh the LLM-ready briefing that Hermes desktop reads.
# Overwrites logs/watch_briefing.txt each run (launchd StandardOutPath only appends, so we redirect here).
cd "$(dirname "$0")" || exit 1
PY="/opt/homebrew/Caskroom/miniconda/base/bin/python3"   # matches this machine; edit if python3 moves
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/local/bin:$PATH"
"$PY" watch.py --prompt > logs/watch_briefing.txt 2>&1
