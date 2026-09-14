#!/usr/bin/env python3
"""Inspect the corpus schema: per-ring columns, survey counts, available metadata."""
import json, collections, os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "data", "rotation_curve_corpus_v7.json")))
gals = d["galaxies"]

for survey in ["SPARC", "THINGS", "LITTLE_THINGS", "WALLABY"]:
    found = False
    for g in gals:
        if g.get("survey") == survey and len(g.get("data", [])) > 0:
            print(f"--- {survey}: {g['galaxy']} (n={len(g['data'])}) ---")
            print("  columns:", json.dumps(g["columns"]))
            print("  row0   :", json.dumps(g["data"][0]))
            print("  row1   :", json.dumps(g["data"][1]))
            found = True
            break
    if not found:
        print(f"--- {survey}: NO DATA ROWS ---")

cnt = collections.Counter()
for g in gals:
    cnt[(g.get("survey"), len(g.get("data", [])) > 0)] += 1
print("\ncounts (survey, has_data):", dict(cnt))

keys = collections.Counter()
for g in gals:
    for k in g:
        keys[k] += 1
print("\nall keys across 438 galaxies:")
for k, v in sorted(keys.items()):
    print(f"  {k}: {v}")

# check the m2l fields for SPARC (disk M/L present?) and whether any mass metadata exists
sparc_m2l = [g.get("m2l_disk") for g in gals if g.get("survey") == "SPARC"]
print("\nSPARC m2l_disk: n =", len(sparc_m2l),
      "non-null:", sum(1 for x in sparc_m2l if x is not None),
      "unique:", sorted(set(x for x in sparc_m2l if x is not None))[:10])
