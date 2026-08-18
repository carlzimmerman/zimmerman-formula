#!/usr/bin/env python3
"""review.py -- read everything the loop produced. Run this in the morning."""
import glob, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
led = os.path.join(H, "LEDGER.md")
rows = re.findall(r"^\|\s*(I\d{3})\s*\|([^|]*)\|([^|]*)\|([^|]*)\|", open(led).read(), re.M) if os.path.exists(led) else []
res = {os.path.basename(p)[:4].upper(): p for p in glob.glob(os.path.join(H, "results", "I*.md"))}
scr = {os.path.basename(p)[:4].upper(): p for p in glob.glob(os.path.join(H, "runs", "i*.py"))}
by = {}
for i, what, num, v in rows:
    by.setdefault(v.strip().upper(), []).append((i, what.strip(), num.strip()))
print(f"{len(rows)} ideas done | {len(res)} result files | {len(scr)} scripts\n")
for v in ("PASS", "PARTIAL", "KILL", "NOT COMPUTED"):
    got = by.get(v, [])
    if not got:
        continue
    print(f"=== {v}  ({len(got)}) ===")
    for i, what, num in got:
        flag = "" if i in res else "   [NO RESULT FILE]"
        print(f"  {i}  {num[:44]:44s}  {what[:58]}{flag}")
    print()
missing = [i for i, *_ in rows if i not in res]
if missing:
    print("LEDGERED BUT NO RESULT FILE (treat as not done):", ", ".join(missing))
print("\nread a result:  cat qwen_claude_field_theory/results/<Ixxx>*.md")
