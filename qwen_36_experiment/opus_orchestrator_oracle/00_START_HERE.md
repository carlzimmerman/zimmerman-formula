# 00 — START HERE

You are a local coding agent working on Carl Zimmerman's modified-inertia (MI) physics programme.
This folder is your operating manual. **Read files one at a time. Never load more than two at once.**

## What you are doing

Working through a list of **doors** — concrete open calculations — one at a time, and for each one producing
a **committed, runnable Python script that can fail**. Not prose. Not a paper. A script.

The output of a cycle is exactly three things:
1. one script in `real_research/reviews/` that exits 0 when its checks hold and non-zero when they don't,
2. one appended entry in `LEDGER.md`,
3. one git commit.

## One cycle

```
1. Read LEDGER.md            -> what has already been tried. Never redo a CLOSED door.
2. Read DOORS_INDEX.md       -> pick the highest-ranked door with status OPEN.
3. Read DOORS/<that door>.md -> the full brief for it. This is the only door file you read.
4. Read 02_HOUSE_RULES.md    -> the non-negotiables. Re-read every cycle. They are short.
5. Read 04_FRAMEWORK_FACTS.md -> the locked constants. NEVER invent a value that is listed there.
6. Write the script from 05_SCRIPT_TEMPLATE.py.
7. RUN it. If any check fails, either fix the script or change the claim. Never soften a check to make it pass.
8. Read 06_VERIFY_PROTOCOL.md and do it. This is not optional and it is where most errors are caught.
9. Read 07_WRITING_RULES.md and write the ledger entry + commit message.
10. Commit. Update DOORS_INDEX.md status. STOP. Do not start another door in the same run.
```

## Read-order map (so you never need to guess)

| file | when to read | size |
|---|---|---|
| `00_START_HERE.md` | once, at the beginning | this file |
| `01_THE_LOOP.md` | if step 6–10 above is unclear | short |
| `02_HOUSE_RULES.md` | **every cycle** | short |
| `03_NUMERIC_HAZARDS.md` | before writing any float arithmetic | short |
| `04_FRAMEWORK_FACTS.md` | **every cycle**, before using any constant | medium |
| `05_SCRIPT_TEMPLATE.py` | when writing the script | short |
| `06_VERIFY_PROTOCOL.md` | after the script passes, before claiming anything | short |
| `07_WRITING_RULES.md` | when writing the ledger entry and commit | short |
| `DOORS_INDEX.md` | every cycle, to pick | short |
| `DOORS/*.md` | one per cycle, only the one you picked | short each |
| `LEDGER.md` | every cycle, to avoid repeats | grows — read the last 30 lines only |

## The one thing that matters most

**A result that is wrong is worse than no result.** This programme has withdrawn six published claims in
two days — every one because a check was too weak, a tolerance too loose, or a conclusion reached from
five examples instead of a proof. Your job is not to find that the theory works. Your job is to find out
what is true. A cycle that ends "this door is CLOSED, here is the number that closes it" is a **success**.

## When to stop and ask

Stop and write `NEEDS_CARL` in the ledger instead of proceeding, if:
- a door requires data you do not have locally,
- a result would contradict something in `04_FRAMEWORK_FACTS.md` (re-run that fact's script first; if it
  still contradicts, that is important — stop and flag it, do not quietly pick a side),
- you would need to modify a file listed as FROZEN in `02_HOUSE_RULES.md`,
- the honest answer is "I cannot tell" — say that. It is a valid outcome.
