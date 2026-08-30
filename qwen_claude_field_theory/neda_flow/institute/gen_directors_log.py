#!/usr/bin/env python3
"""Director's Log generator -- the live status board, built from ACTUAL institute state (not prose).
Run any time: python3 institute/gen_directors_log.py"""
import json, os, collections
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
S = os.path.join(H, "state"); DB = os.path.join(H, "database")
def J(p): return json.load(open(os.path.join(S, p)))
def rows(f):
    out=[]
    p=os.path.join(DB,f)
    if os.path.exists(p):
        for l in open(p):
            l=l.strip()
            if l:
                try: out.append(json.loads(l))
                except: pass
    return out

dead=J("DEAD_CLASSES.json")["classes"]
cov=J("COVERAGE_MATRIX.json")["families"]
og=J("OPEN_GATES.json")["open_gates"]
cands=rows("candidates.jsonl")
status=collections.Counter()
seen={}
for r in cands:
    if r.get("candidate_id") and "status" in r: seen[r["candidate_id"]]=r["status"]
for v in seen.values(): status[v]+=1
by_stat=collections.Counter(m.get("status") for m in cov.values())

L=[]
L.append("# DIRECTOR'S LOG — live research frontier")
L.append("*Auto-generated from institute state. Regenerate: `python3 institute/gen_directors_log.py`*\n")
L.append("## Standing verdict of the search")
L.append(f"- Theory space mapped by the Coverage Office: **{len(cov)} architecture families** "
         f"({by_stat.get('dead',0)} dead · {by_stat.get('active',0)} active · "
         f"{by_stat.get('unexplored',0)} unexplored · {by_stat.get('tested',0)} tested).")
L.append(f"- Proven no-go theorems (dead classes): **{len(dead)}**.")
L.append(f"- Candidates on record: **{len(seen)}** ({dict(status)}).\n")
L.append("## THE OPEN FRONTIER (where the live physics is)")
for g in og[:4]:
    L.append(f"- **{g['gate']}**\n  - {g['why'][:400]}")
L.append("\n## ACTIVE families (in progress)")
for name,m in cov.items():
    if m.get("status")=="active":
        L.append(f"- **{name}** — {m.get('implication', m.get('why',''))[:220]}")
L.append("\n## UNEXPLORED families (breadth queue)")
for name,m in cov.items():
    if m.get("status")=="unexplored":
        L.append(f"- {name} — {m.get('why','')[:150]}")
L.append("\n## Recently proven dead (last 6 no-go theorems)")
for c in dead[-6:]:
    L.append(f"- **{c['class_id']} {c['name']}** — {c.get('decisive','')[:180]}")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"DIRECTORS_LOG.md"),"w").write("\n".join(L)+"\n")
print("DIRECTORS_LOG.md regenerated")
