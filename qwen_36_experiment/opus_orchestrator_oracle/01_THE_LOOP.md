# 01 — THE LOOP (mechanics of one cycle)

One cycle = one door = one script = one commit. **Never two doors in one run.**

## Where things go

| what | where |
|---|---|
| your script | `real_research/reviews/<name>_2026.py` |
| scratch / throwaway | `/tmp/` — never in the repo |
| your ledger entry | append to `opus_orchestrator_oracle/LEDGER.md` |
| door status update | `opus_orchestrator_oracle/DOORS_INDEX.md` |
| a paper, only if asked | `opus_48_extended_research/papers/<NAME>_<date>.md` |

Naming: `mi_<subject>_2026.py`. Lower case, underscores, ends `_2026`. Look at
`real_research/reviews/mi_crossover_master_formula_2026.py` for the house style — copy its shape.

## The cycle

### 1. Orient (read only)
```bash
tail -40 opus_orchestrator_oracle/LEDGER.md
cat opus_orchestrator_oracle/DOORS_INDEX.md
```
Pick the top `OPEN` door. If its prerequisites (listed in its door file) are not `CLOSED` or `CONFIRMED`, pick
the next one down.

### 2. Load the brief
Read `DOORS/<door>.md`. Read `02_HOUSE_RULES.md`. Read `04_FRAMEWORK_FACTS.md`. That is all you need —
do not read other door files, do not read the whole tn corpus.

### 3. Decide what would settle it
Before writing code, write in the ledger draft: **"this door is settled if \<X\>, and refuted if \<Y\>."**
Both must be things a number can decide. If you cannot write that sentence, the door needs splitting — say so
and stop.

### 4. Write the script
From `05_SCRIPT_TEMPLATE.py`. Read `03_NUMERIC_HAZARDS.md` first if there is any float arithmetic.
Sections S2 (move the number), S3 (refine), S4 (both footings) and S5 (parameter count) are **mandatory** —
they are not optional extras, they are where the errors are.

### 5. Run it
```bash
cd /Users/carlzimmerman/new_physics/zimmerman-formula
timeout 1800 python -u real_research/reviews/<name>_2026.py
```
- **exit 0** → go to step 6.
- **a check failed** → the check is telling you something. Either the script has a bug, or the claim is wrong.
  Fix the bug, or change the claim. **Never widen a tolerance and never delete a failing check to make it pass.**
  If you widen a tolerance you must state in the ledger exactly why the new tolerance is the right one on
  method-precision grounds.
- **crashes** → fix. Keep stdout under ~400 lines; a lane in this project was killed twice by an output limit.

### 6. Verify
Do all six steps of `06_VERIFY_PROTOCOL.md`. Write the answers down.

### 7. Write it up
Per `07_WRITING_RULES.md`: the ledger entry, then the commit message.

### 8. Commit
```bash
cd /Users/carlzimmerman/new_physics/zimmerman-formula
git add real_research/reviews/<name>_2026.py opus_orchestrator_oracle/LEDGER.md opus_orchestrator_oracle/DOORS_INDEX.md
git commit -F <your message file>
git push origin main
```
Never `git add -A`. Never `git add .`. Never commit anything under `ai_slop/`. Never force-push, never
`reset --hard`, never rewrite history — if you think you need to, write `NEEDS_CARL` instead.

### 9. Update the index and STOP
Set the door's status in `DOORS_INDEX.md` to one of:

| status | meaning |
|---|---|
| `OPEN` | not yet attempted |
| `IN PROGRESS` | you are on it (set this at step 3, so a crashed run is visible) |
| `CLOSED` | settled negatively, with the number that closes it. **This is a success.** |
| `CONFIRMED` | settled positively, having cleared all six verify steps |
| `SPLIT` | too big; you wrote the sub-doors into `DOORS/` |
| `NEEDS_CARL` | blocked, or contradicts a framework fact |
| `PARKED` | attempted, inconclusive, and you have said exactly what would decide it |

Then stop. Do not begin another door.

## Budget guidance

If a door has taken more than ~3 hours of wall clock or you have rewritten the script more than 4 times, mark it
`PARKED`, write down precisely where you got stuck and what number would unstick it, and move on. A clear
`PARKED` with a sharp blocker is worth more than a muddled `CONFIRMED`.
