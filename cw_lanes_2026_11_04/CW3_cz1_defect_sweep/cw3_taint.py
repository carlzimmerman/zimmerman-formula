#!/usr/bin/env python3
"""CW3 taint trace for the L? triage rows (AMENDMENTS A6): does an observed-field literal reach a nu argument, or does its
inverted (Newtonian) value reach a mu argument?  Reads files only; runs nothing.  Needs cw3_triage.json.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -I cw3_taint.py  -> cw3_taint.json, cw3_taint.out.  kappa = 1/2 FITTED; not theory closed."""
import os, re, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
T = json.load(open(os.path.join(HERE, "cw3_triage.json")))
src = open(os.path.join(HERE, "cw3_triage.py")).read()
ns = {}; exec(src[src.index("TOK ="):src.index("rows = []")], {"re": re, "os": os, "json": json, "collections": __import__("collections")}, ns)
OBS, INV, CALL, args, strip = ns["OBS"], ns["INV"], ns["CALL"], ns["args"], ns["strip"]
ASG = re.compile(r"^\s*([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*=(?!=)\s*(.*)$")
out = []
for r in T["rows"]:
    if r["cls"] != "L?": continue
    L = [strip(l) for l in open(os.path.join(REPO, r["file"]), encoding="utf-8", errors="replace").read().split("\n")]
    obs, invn = set(), set()
    for _ in range(6):
        n0 = len(obs) + len(invn)
        for c in L:
            m = ASG.match(c)
            if not m: continue
            lhs = [x.strip() for x in m.group(1).split(",")]; rhs = m.group(2)
            hit_o = bool(OBS.search(rhs)) or any(re.search(r"(?<![A-Za-z0-9_])" + re.escape(n) + r"(?![A-Za-z0-9_])", rhs) for n in obs)
            if hit_o and INV.search(rhs): invn.update(lhs)
            elif hit_o: obs.update(lhs)
            elif any(re.search(r"(?<![A-Za-z0-9_])" + re.escape(n) + r"(?![A-Za-z0-9_])", rhs) for n in invn): invn.update(lhs)
        if len(obs) + len(invn) == n0: break
    bad = []
    for k, c in enumerate(L, 1):
        for m in CALL.finditer(c):
            a = args(c, m); isnu = not m.group(1).startswith(("mu", "μ"))
            pool = obs if isnu else invn
            if (isnu and OBS.search(a)) or any(re.search(r"(?<![A-Za-z0-9_])" + re.escape(n) + r"(?![A-Za-z0-9_])", a) for n in pool):
                bad.append((k, ("nu<-obs" if isnu else "mu<-inverted")))
    out.append(dict(file=r["file"], tainted_obs=sorted(obs)[:8], tainted_inv=sorted(invn)[:8], hits=bad[:6], label=("HAND" if bad else "CORRECT (machine triage, A6)")))
json.dump(out, open(os.path.join(HERE, "cw3_taint.json"), "w"), indent=0)
O = [f"L? rows {len(out)}; to hand reading {sum(1 for o in out if o['hits'])}; machine CORRECT {sum(1 for o in out if not o['hits'])}"]
for o in out:
    if o["hits"]: O.append(f"HAND {o['file']} hits {o['hits']} obs-tainted {o['tainted_obs']} inverted {o['tainted_inv']}")
open(os.path.join(HERE, "cw3_taint.out"), "w").write("\n".join(O) + "\n"); print("\n".join(O))
