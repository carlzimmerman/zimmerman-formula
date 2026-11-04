#!/usr/bin/env python3
"""NV2 Stage 3: runs ../RQ3_acceptance_v2/acceptance.py from its own source, text unedited, with this lane as its working directory (NP2's np2_stage3 pattern).
  nv2_stage3.py CAND.py [--no-keys] [--no-bullet]                    unedited card (U): RQ3 as is, results/<cand>.{out,json}
  nv2_stage3.py CAND.py --subset rules/<table>.json [--tag NAME]      SUBSET card (S): the same text, executed unedited, with CRG1's load_gal / load_lt and the X1 dwarf list
                                                                       filtered to systems whose E is finite in the table (FROZEN_CRITERIA, Grading). results/<NAME>_S.*
kappa = 1/2 FITTED; not theory closed."""
import csv, hashlib, io, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(os.path.dirname(HERE), "RQ3_acceptance_v2", "acceptance.py"); TXT = open(SRC).read(); SHA = hashlib.sha256(TXT.encode()).hexdigest()[:16]
def fin(v):
    try: return v is not None and math.isfinite(float(v))
    except (TypeError, ValueError): return False
if __name__ == "__main__":
    print("RQ3 acceptance.py sha256", SHA, flush=True)
    if "--subset" not in sys.argv:
        n = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "__main__"}; exec(compile(TXT, SRC, "exec"), n); sys.exit(0)
    a = sys.argv; T = json.load(open(a[a.index("--subset") + 1])); tag = a[a.index("--tag") + 1] if "--tag" in a else os.path.basename([x for x in a[1:] if x.endswith(".py")][0])[:-3]
    path = [x for x in a[1:] if x.endswith(".py")][0]
    n = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "nv2_subset"}; exec(compile(TXT, SRC, "exec"), n)
    n["crg"](); import crg1_sparc as Cs
    lg, ll = Cs.load_gal, Cs.load_lt; keep_d = {k for k, v in T["disc"].items() if fin(v)}; keep_l = {k for k, v in T["dwarf disc"].items() if fin(v)}; keep_w = {k for k, v in T["dwarf"].items() if fin(v)}
    G0, L0 = lg(), ll(); Cs.load_gal = lambda: [g for g in lg() if g["name"] in keep_d]; Cs.load_lt = lambda: [x for x in ll() if x["name"] in keep_l]
    X1P = os.path.join(n["RB"], "X1_hosted_recount", "x1_per_system.csv"); _csv = n["csv"]
    class _C:
        def __getattr__(s, k): return getattr(_csv, k)
        def DictReader(s, f, *aa, **kw):
            rows = _csv.DictReader(f, *aa, **kw)
            return (r for r in rows if r.get("name") in keep_w) if getattr(f, "name", "") == X1P else rows
    n["csv"] = _C()
    info = dict(sparc=[len(Cs.load_gal()), len(G0)], lt=[len(Cs.load_lt()), len(L0)], dwarfs_kept=len(keep_w), dropped_sparc=sorted({g["name"] for g in G0} - keep_d), dropped_lt=sorted({x["name"] for x in L0} - keep_l))
    print("SUBSET:", json.dumps(info), flush=True)
    o = n["scorecard"](path, "--no-keys" not in a, "--no-bullet" not in a); o["subset"] = info; print("\n".join(n["write"](o, tag + "_S")))
