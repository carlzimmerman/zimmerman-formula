#!/usr/bin/env python3
"""CFG122 summary: reads every *_results.json next to this file and prints the gate verdict table (main runs, MUTATE runs, POST-HOC runs listed separately).
Run: python3 cfg122_summary.py > cfg122_summary.out"""
import os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(HERE, "cfg122_*_results.json"))):
    d = json.load(open(f))
    tag = "MUTATE " + d["mutate"] if d.get("mutate") else ("POST-HOC" if "POSTHOC" in d["slug"] or "posthoc" in d["slug"] else "main")
    rows.append((tag, d["slug"], d["verdicts"], d["check_failures"]))
for section in ("main", "MUTATE", "POST-HOC"):
    print("=" * 110); print(section); print("=" * 110)
    for tag, slug, v, nf in rows:
        if not tag.startswith(section):
            continue
        print(f"{slug}  (harness check failures {nf})")
        for g, x in v.items():
            print(f"    {g:24s} {x['status']:10s} {x['why'][:220]}")
