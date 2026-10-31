#!/usr/bin/env python3
"""ZN3 grade (FROZEN_CRITERIA.md): ZN1's grader text, unchanged except that its shape function takes a third tag and its outputs are named zn3. ZN1's files are read only.
    python3 zn3_grade.py --k1            # K1: two tags reproduce ZN1's results; reads no 1e15 zoom
    python3 zn3_grade.py [--mutate] [--bootstrap N]
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
HERE3 = os.path.dirname(os.path.abspath(__file__)); RB3 = os.path.dirname(HERE3); ZN1D = os.path.join(RB3, "ZN1_zooms_to_z0"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(RB, 'ZN1_zooms_to_z0', 'zn1_def.py')!r}).read() + open({os.path.join(HERE, 'zn3_def.py')!r}).read()""")
_s('''open(os.path.join(HERE, "zn1_boot_tail.py")).read()''', '''open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_boot_tail.py")).read().replace('("1e13", "1e14")', '("1e13", "1e14", "1e15")')''')
_s('os.path.join(HERE, "zn1_shapes.json")', 'os.path.join(HERE, "zn3_shapes.json")')
_s('TAG = "zn1_MUTATE" if MUT else "zn1"', 'TAG = "zn3_MUTATE" if MUT else "zn3"')
_s('os.environ.get("ZN1_BOOT_TAG", "zn1_boot")', 'os.environ.get("ZN1_BOOT_TAG", "zn3_boot")')
_s('os.path.join(HERE, "zn1_results.json")', 'os.path.join(HERE, "zn3_results.json")', 2)
_s('''P(f"ZN1 grade {TAG}:''', '''P(f"ZN3 grade {TAG}:''')
_s('''above = 0''' if False else '''JOBS = [(f"f* {fs}, X-COP's gas"''', '''JOBS = [(f"f* {fs}, X-COP's gas"''')
if "--k1" in sys.argv:
    import importlib
    T3 = T3.replace('if __name__ == "__main__":\n    if "--k3" in sys.argv:', 'if __name__ == "__main__":\n    if "--k3" in sys.argv:', 1); os.environ["ZN3_TWO"] = "1"; sys.argv = [sys.argv[0], "--k1run"]
    _k = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:'); exec(compile(T3[:_k], __file__, "exec"))
    J = json.load(open(os.path.join(ZN1D, "zn1_results.json")))["runs"]; SHZ = os.path.join(ZN1D, "zn1_shapes.json"); R = run("0.034", "fs", True, SHZ); O = cells(R); C = J["f* 0.034, X-COP's gas"]; d = max(abs(O[h][k]["pred"] - C["cells"][h][k]["pred"]) for h in HH for k in C["cells"][h]); dx = max(abs(R["footings"]["canonical"][k] - C["xcop"][k]) for k in ("mean", "rms")); ok = d <= 1e-9 and dx <= 1e-9; P(f"K1 two tags through this path against ZN1: preds {d:.1e}, X-COP {dx:.1e}: {'PASS' if ok else 'FAIL'}"); open(os.path.join(HERE3, "zn3_k1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
exec(compile(T3, os.path.abspath(__file__), "exec"))
