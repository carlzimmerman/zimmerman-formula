#!/bin/bash
# retraction_guard.sh — block staged content that uses a RETRACTED claim as if it were live.
# Mechanizes the week's lessons (the "Dchi2~117 / CMB selects declining" regression in particular).
# A hit is only flagged if the line uses a retracted claim WITHOUT a nearby retraction marker
# (retract/superseded/artifact/corrected/wrong/stale/⚠️/~0/was a), so the correction docs themselves pass.
# Usage: tools/retraction_guard.sh [file ...]   (no args -> staged files).  Exit 1 on a live hit.
set -u
FILES="$*"
if [ -z "$FILES" ]; then FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null | grep -E '\.(md|py|tex)$'); fi
[ -z "$FILES" ] && exit 0

# retracted/over-stated claims used as LIVE (extended regex). Keep TIGHT to avoid false positives.
PATTS='CMB SELECTS-DECLINING|CMB selects declining|selects-declining|constant a. is CMB-excluded|excludes constant\+rising|D(chi2|χ²?)\s*[~≈=]\s*117|19[–-]26\s*(σ|sigma)|same kernel (that gives|predicts).{0,30}cluster (failure|breakdown)|lone (CMB )?survivor|0\.74 \(max|0\.737 maximal|syllogism (HOLDS|holds)'
# words that, present on the same line, mean the claim is being retracted/quoted, not asserted:
SAFE='retract|RETRACT|supersed|SUPERSED|artifact|corrected|CORRECTED|⚠|stale|no longer|was a |→\s*~?0|->\s*~?0|not (excluded|a verdict|establish|supported)|wrong|provisional|did not survive|downgrad|rider|method-dependent|method artifact|cherry-pick|leaning against|CONTESTED|OPEN|earlier (draft|edition|version)|an earlier'

hits=0
for f in $FILES; do
  [ -f "$f" ] || continue
  while IFS=: read -r ln text; do
    [ -z "$ln" ] && continue
    echo "$text" | grep -Eiq "$SAFE" && continue   # excused: line is retracting/quoting
    echo "  ⛔ $f:$ln  $(echo "$text" | sed 's/^[[:space:]]*//' | cut -c1-100)"
    hits=$((hits+1))
  done < <(grep -nEi "$PATTS" "$f" 2>/dev/null)
done

if [ "$hits" -gt 0 ]; then
  echo ""
  echo "retraction_guard: $hits line(s) use a RETRACTED claim as live. See real_research/CONVENTION_LOCK.md."
  echo "Fix the wording or add a retraction marker (retract/superseded/⚠️/corrected) on the line, then re-stage."
  exit 1
fi
exit 0
