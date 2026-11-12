#!/usr/bin/env python3
"""EW1 computed cells (criteria FROZEN_CRITERIA.md section 3): two fixed static forms through GB1's battery, read-only.
    python3 ew1_static.py            -> ew1_static.json / .out   (LAW_D KA row, E1 BK effective, E2 QUMOND beta 2.5)
    python3 ew1_static.py --mutate   -> ew1_static_MUTATE.json / .out (Newton via the delta path; must FAIL G2)
GB1's source is exec'd with only its candidate list and output paths swapped; its lines, loaders and KAs are unchanged.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GB1 = os.path.join(REPO, "closure_2026_11_06", "GB1_all_gates_battery", "gb1.py")
MUT = "--mutate" in sys.argv
src = open(GB1).read()
rep = [('TAG = "gb1_MUTATE" if MUT else "gb1"', 'TAG = "ew1_static_MUTATE" if MUT else "ew1_static"'),
       ('CANDS = {"NEWTON": NEWTON} if MUT else {"L0": L0, "L1": L1, "L2": L2, "F1": F1, "F2": F2, "F3": F3}',
        'CANDS = {"NEWTON_D": NEWTON_D} if MUT else {"LAW_D": LAW_D, "E1_BK": E1_BK, "E2_BETA25": E2_BETA25}'),
       ('os.path.join(HERE, TAG + ".json")', 'os.path.join(OUTDIR, TAG + ".json")'),
       ('os.path.join(HERE, TAG + ".out")', 'os.path.join(OUTDIR, TAG + ".out")'),
       ('bites = RES["cands"]["NEWTON"]', 'bites = RES["cands"]["NEWTON_D"]'),
       ('all(RES["cands"]["NEWTON"][f]', 'all(RES["cands"]["NEWTON_D"][f]')]
for a, b in rep:
    assert src.count(a) >= 1, a
    src = src.replace(a, b)
EXTRA = '''
def _gN(ft, a0): return need(ft, "x") * a0
def LAW_D(f, a0): return lambda ft: dict(delta=0.0 * _gN(ft, a0))
def E1_BK(f, a0):
    def c(ft):
        gN = _gN(ft, a0); return dict(delta=math.log10((gN + math.sqrt(a0 * gN)) / glaw(gN, a0)))
    return c
def E2_BETA25(f, a0):
    def c(ft):
        gN = _gN(ft, a0); y = gN / a0; return dict(delta=math.log10(gN * (1.0 + y ** -2.5) ** 0.2 / glaw(gN, a0)))
    return c
def NEWTON_D(f, a0):
    def c(ft):
        gN = _gN(ft, a0); return dict(delta=math.log10(gN / glaw(gN, a0)))
    return c
'''
anchor = "def NEWTON(f, a0):"
src = src.replace(anchor, EXTRA + anchor, 1)
NS = {"__file__": GB1, "__name__": "__main__", "OUTDIR": HERE}
code = None
try:
    exec(compile(src, "gb1_via_ew1", "exec"), NS)
except SystemExit as e:
    code = e.code
# ---- EW1 post-processing: labels on G2-G7 only (G1, G8 from AX1 / D7c per criteria), KA vs committed gb1.json
R = json.load(open(os.path.join(HERE, ("ew1_static_MUTATE" if MUT else "ew1_static") + ".json")))
if not R.get("graded"):
    print("GB1 KA failed: nothing graded"); sys.exit(2)
GR = ["G2 X-COP", "G3 groups", "G4 ellipticals", "G5 Coma UDGs", "G6 dSph classes", "G7 KiDS split"]
EW = {}
if not MUT:
    G0 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "GB1_all_gates_battery", "gb1.json")))
    def flat(x, p=""):
        if isinstance(x, dict):
            for k, v in x.items(): yield from flat(v, p + "/" + k)
        elif isinstance(x, list):
            for i, v in enumerate(x): yield from flat(v, p + f"[{i}]")
        elif isinstance(x, (int, float)) and not isinstance(x, bool): yield p, float(x)
    md = 0.0
    for f in ("canonical", "alt"):
        for g in GR:
            a = dict(flat(R["cands"]["LAW_D"][f][g]["num"])); b = dict(flat(G0["cands"]["L0"][f][g]["num"]))
            assert a.keys() == b.keys(), (f, g)
            md = max([md] + [abs(a[k] - b[k]) for k in a])
    EW["KA_law_vs_gb1_L0"] = dict(maxdiff=md, ok=bool(md <= 1e-12))
    print(f"EW1 KA: LAW_D (delta path) vs committed GB1 L0, G2-G7 both footings: max|d| {md:.1e} -> {'PASS' if md <= 1e-12 else 'FAIL'}")
cands = ["NEWTON_D"] if MUT else ["E1_BK", "E2_BETA25"]
for cn in cands:
    EW[cn] = {}
    for f in ("canonical", "alt"):
        st = {g: R["cands"][cn][f][g]["status"] for g in GR}
        EW[cn][f] = dict(cells=st, label=("PASS G2-G7" if all(v == "PASS" for v in st.values()) else "FAIL (" + ", ".join(g.split()[0] for g in GR if st[g] != "PASS") + ")"),
                         reported_only=dict(G1=R["cands"][cn][f]["G1 SPARC"]["status"], G8=R["cands"][cn][f]["G8 Solar System"]["status"]))
        print(f"EW1 [{f}] {cn}: {EW[cn][f]['label']}  (GB1 G1/G8 reported only: {EW[cn][f]['reported_only']})")
if MUT:
    bites = all(R["cands"]["NEWTON_D"][f]["G2 X-COP"]["status"] == "FAIL" for f in ("canonical", "alt"))
    EW["MUTATE_bites"] = bool(bites); print(f"EW1 MUTATE Newton (delta path): G2 FAIL both footings -> {'BITES' if bites else 'NO BITE'}")
R["EW1"] = EW
json.dump(R, open(os.path.join(HERE, ("ew1_static_MUTATE" if MUT else "ew1_static") + ".json"), "w"), indent=1, default=float)
with open(os.path.join(HERE, ("ew1_static_MUTATE" if MUT else "ew1_static") + ".out"), "a") as fo:
    fo.write(json.dumps(EW, indent=1) + "\nkappa = 1/2 FITTED; not theory closed.\n")
ok = (EW["MUTATE_bites"] if MUT else EW["KA_law_vs_gb1_L0"]["ok"])
sys.exit(0 if ok else 1)
