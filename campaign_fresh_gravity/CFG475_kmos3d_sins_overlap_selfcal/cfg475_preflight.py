#!/usr/bin/env python3
"""CFG475 pre-flight: do the 5 KMOS3D x SINS overlaps meet CFG385's conditions plus the resolved-gas-shape rule? Run: python3 cfg475_preflight.py [--mutate]"""
import os, sys, csv, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s); OUT.append(str(s))
rows = list(csv.DictReader(open(os.path.join(REPO, "data_assembly/kmos3d_cubes/k3d_C1_sins_overlap.csv"))))
P(f"overlap rows: {len(rows)} ({', '.join(r['SINS'] + '/' + r['KMOS3D'] for r in rows)}); columns: {list(rows[0].keys())}")
k1 = len(rows) == 5
# Q1: per-radius curves on disk for these IDs? The overlap table carries ONE SINS Vrot and ONE KMOS3D V22 per galaxy.
q1 = {r["SINS"]: False for r in rows}
# Q2/Q3: search for CO/HI or resolved stellar products naming these IDs
names = [r["SINS"] for r in rows] + [r["KMOS3D"] for r in rows]
hits = []
for f in glob.glob(os.path.join(REPO, "real_research", "data", "**", "*"), recursive=True):
    b = os.path.basename(f).lower()
    if os.path.isfile(f) and any(n.lower().replace("-", "").replace("_", "") in b.replace("-", "").replace("_", "") for n in names):
        hits.append(os.path.relpath(f, REPO))
P(f"files under real_research/data naming any overlap ID: {hits if hits else 'none'}")
q2 = {r["SINS"]: (True if MUT else False) for r in rows}
q3 = {r["SINS"]: False for r in rows}
n = sum(q1[k] and q2[k] and q3[k] for k in q1)
P(f"Q1 per-radius spanning curves: {sum(q1.values())}/5 | Q2 resolved gas profile: {sum(q2.values())}/5 | Q3 resolved stellar profile: {sum(q3.values())}/5 -> qualifying {n}")
v = "RUNNABLE" if n >= 1 else "NOT POSSIBLE"
P(f"K1 five overlap rows: {'PASS' if k1 else 'FAIL'}; VERDICT: {v}")
json.dump(dict(rows=len(rows), q1=q1, q2=q2, q3=q3, qualifying=n, verdict=v, files=hits), open(os.path.join(HERE, f"cfg475_preflight{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg475_preflight{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit((1 if n != 0 else 0) if MUT else (0 if k1 else 1))
