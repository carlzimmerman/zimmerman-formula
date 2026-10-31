#!/usr/bin/env python3
"""GS4 regrade (criteria 1bf15a0aff): ZN3's frozen rule at a measured gas offset. ZN1's grader text with ZN3's patches, only the gas factor 10**0.111 changed. No file of ZN1 or ZN3 is edited or written.
    python3 gs4_regrade.py --k3            # at +0.111 against zn3_results.json
    python3 gs4_regrade.py --dex 0.005 ...
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
ME = os.path.abspath(__file__); HERE4 = os.path.dirname(ME); RB4 = os.path.dirname(HERE4); ZN1D = os.path.join(RB4, "ZN1_zooms_to_z0"); ZN3D = os.path.join(RB4, "ZN3_native_shape_at_1e15"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE);", f"HERE = {ZN1D!r}; RB = {RB4!r};")
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read() + open(""" + repr(repr(os.path.join(ZN3D, "zn3_def.py")))[1:-1] + """).read()""")
_s("""% (10 ** 0.111))""", """% (10 ** float(os.environ["GS4_DEX"])))""")
_k = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:'); exec(compile(T3[:_k], ME, "exec"))   # a --worker run executes and exits inside this
SH = os.path.join(ZN3D, "zn3_shapes.json"); J = json.load(open(os.path.join(ZN3D, "zn3_results.json")))["runs"]
def cls(a, b):
    pa = not a[0] and a[1]; pb = not b[0] and b[1]; xb = a[1] or b[1]; kb = (not a[0]) or (not b[0])
    return "Z0 PROFILE PASSES BOTH" if pa and pb else "F*-DEPENDENT" if pa or pb else "X-COP ONLY" if xb and not kb else "KEYS ONLY" if kb and not xb else "FAILS BOTH" if not xb and not kb else "NEITHER AT ONE f*"
RES = {}
def grade(dex):
    os.environ["GS4_DEX"] = repr(dex); P(f"GS4 regrade, ZN3's rule, gas +{dex:.3f} dex"); FS = ("0.034", "0.0615")
    with ThreadPoolExecutor(2) as ex: RR = list(ex.map(lambda f: run(f, "fs", True, SH), FS))
    L = {f: line(f"f* {f}", R) for f, R in zip(FS, RR)}; V = cls(L["0.034"], L["0.0615"]); P(f"  CLASS at {dex:+.3f}: {V}"); RES[f"{dex:.3f}"] = dict(verdict=V, runs={f: dict(cells=cells(R), xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms")}) for f, R in zip(FS, RR)}); return RR
if "--k3" in sys.argv:
    RR = grade(0.111); d = 0.0; dz = 0.0
    for f, R in zip(("0.034", "0.0615"), RR):
        O = cells(R); C = J[f"f* {f}, X-COP's gas"]
        for h in HH:
            for k in C["cells"][h]: d = max(d, abs(O[h][k]["pred"] - C["cells"][h][k]["pred"])); dz = max(dz, abs(O[h][k]["Z"] - C["cells"][h][k]["Z"]))
        dz = max(dz, abs(R["footings"]["canonical"]["rms"] - C["xcop"]["rms"]))
    ok = d <= 1e-9 and dz <= 1e-9; P(f"K3 at +0.111 against ZN3: preds {d:.1e}, Z and X-COP rms {dz:.1e}: {'PASS' if ok else 'FAIL'}"); open(os.path.join(HERE4, "gs4_k3.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
for a in [float(x) for x in sys.argv[sys.argv.index("--dex") + 1:]]: grade(a)
json.dump(RES, open(os.path.join(HERE4, "gs4_regrade_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE4, "gs4_regrade.out"), "w").write("\n".join(OUT) + "\n")
