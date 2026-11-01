#!/usr/bin/env python3
"""OG1_outer_gas_slope (criteria 6e5f42b552): ZN4's rule and shapes at GS4's measured gas +0.005, one gas slope beyond R500 changed. ZN1's grader text with patches; no file of ZN1, ZN3, ZN4 is edited.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 og1.py      (OG1_MUTATE=1 twin)
kappa = 1/2 FITTED; footings never pooled; not theory closed; nothing here says the data favour the framework."""
import json, os, sys, hashlib
from concurrent.futures import ThreadPoolExecutor
ME = os.path.abspath(__file__); HERE1 = os.path.dirname(ME); RB1 = os.path.dirname(HERE1); ZN1D = os.path.join(RB1, "ZN1_zooms_to_z0"); ZN3D = os.path.join(RB1, "ZN3_native_shape_at_1e15"); ZN4D = os.path.join(RB1, "ZN4_cluster_resolution"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE);", f"HERE = {ZN1D!r}; RB = {RB1!r};")
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read() + open({os.path.join(RB, 'ZN3_native_shape_at_1e15', 'zn3_def.py')!r}).read()""")
_s("% (10 ** 0.111))", "% (10 ** 0.005))")
_s("X73_SLOPE=SLOPE", 'X73_SLOPE=os.environ["OG1_S"]')
_k = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:'); exec(compile(T3[:_k], ME, "exec"))   # a --worker run executes and exits inside this
MUT = os.environ.get("OG1_MUTATE", "0") == "1"; TAGO = "_MUTATE" if MUT else ""; S0 = "2.7774425603108597"
SH = os.path.join(ZN4D, "zn4_shapes.json"); J = json.load(open(os.path.join(ZN4D, "zn4_results.json")))["runs"]; FS = ("0.034", "0.0615")
GRID = (("2.04", "2.0448741024"), ("2.2", "2.2"), ("2.4", "2.4"), ("2.5", "2.5"), ("2.676", "2.675568930042712"), ("2.777", S0), ("3.071", "3.0711023902445302"))
def cls(a, b):
    pa = not a[0] and a[1]; pb = not b[0] and b[1]; xb = a[1] or b[1]; kb = (not a[0]) or (not b[0])
    return "Z0 PROFILE PASSES BOTH" if pa and pb else "F*-DEPENDENT" if pa or pb else "X-COP ONLY" if xb and not kb else "KEYS ONLY" if kb and not xb else "FAILS BOTH" if not xb and not kb else "NEITHER"
P(f"OG1_outer_gas_slope (criteria 6e5f42b552){' [MUTATE: slope pinned]' if MUT else ''}; gas +0.005 at R500; kappa = 1/2 FITTED; not theory closed")
RES = dict(criteria="6e5f42b552", mutate=MUT, grid={}); chk = {}
for lab, s in GRID:
    os.environ["OG1_S"] = S0 if MUT else s; P(f"\ns = {lab}")
    with ThreadPoolExecutor(2) as ex: RR = list(ex.map(lambda f: run(f, "fs", True, SH), FS))
    L = {f: line(f"f* {f}", R) for f, R in zip(FS, RR)}; V = cls(L["0.034"], L["0.0615"]); P(f"  CLASS: {V}")
    RES["grid"][lab] = dict(s=float(s), verdict=V, runs={f: dict(bad=L[f][0], xcop_ok=bool(L[f][1]), xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms")}, cells={h: {k: dict(Z=v["Z"], pred=v["pred"], meas=v["meas"]) for k, v in c.items()} for h, c in cells(R).items()}) for f, R in zip(FS, RR)})
    if lab == "2.777":
        d = 0.0
        for f, R in zip(FS, RR):
            O = cells(R); C = J[f"f* {f}, gas +0.005"]; d = max([d] + [abs(O[h][k]["pred"] - C["cells"][h][k]["pred"]) for h in HH for k in C["cells"][h]] + [abs(R["footings"]["canonical"][k] - C["xcop"][k]) for k in ("mean", "rms")])
        chk["K1"] = d <= 1e-9; P(f"K1 s 2.777 against ZN4's gas +0.005 jobs: {d:.1e}: {'PASS' if chk['K1'] else 'FAIL'}")
gz = lambda lab, f: RES["grid"][lab]["runs"][f]["cells"]["h0672"]["G-OUT-M3"]["Z"]
dz = max(abs(gz("2.04", f) - gz("3.071", f)) for f in FS); chk["K2"] = dz > 0.1; P(f"K2 G-OUT-M3 change, s 2.04 to 3.071: {dz:.3f}: {'PASS' if chk['K2'] else 'FAIL'}")
ps = [g["s"] for g in RES["grid"].values() if g["verdict"] == "Z0 PROFILE PASSES BOTH"]
V = "RESCUED WITHIN THE MEASURED SLOPE" if any(2.675 <= x <= 3.072 for x in ps) else "NEEDS A SHALLOWER TAIL THAN MEASURED" if ps else "NOT REACHED"
RES.update(verdict=V, checks=chk, passing_s=ps); P(f"\n=== VERDICT: {V}; passing s {ps}; checks {sum(chk.values())}/{len(chk)}")
fn = os.path.join(HERE1, f"og1_results{TAGO}.json"); json.dump(RES, open(fn, "w"), indent=1, default=float); P(f"results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE1, f"og1{TAGO}.out"), "w").write("\n".join(OUT).replace(RB1, "<rebuild>") + "\n"); sys.exit(0 if all(chk.values()) else 1)
