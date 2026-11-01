#!/usr/bin/env python3
"""ZN4 grade (FROZEN_CRITERIA.md): ZN3's grader text, with ng 80 stacks at 1e14 and 1e15, outputs named zn4. Adds the jobs at +0.092 (frozen) and +0.005 (GS4's measured offset, reported). ZN1's and ZN3's files are read only.
    python3 zn4_grade.py --shapes ../ZN3_native_shape_at_1e15/zn3_shapes.json --k1   # K1: ng 64 stacks reproduce ZN3
    python3 zn4_grade.py [--mutate] [--bootstrap N]
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
HERE4 = os.path.dirname(os.path.abspath(__file__)); RB4 = os.path.dirname(HERE4); ZN1D = os.path.join(RB4, "ZN1_zooms_to_z0"); ZN3D = os.path.join(RB4, "ZN3_native_shape_at_1e15"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(RB, 'ZN1_zooms_to_z0', 'zn1_def.py')!r}).read() + open({os.path.join(RB, 'ZN3_native_shape_at_1e15', 'zn3_def.py')!r}).read()""")
_s('''open(os.path.join(HERE, "zn1_boot_tail.py")).read()''', '''open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_boot_tail.py")).read().replace('("1e13", "1e14")', '("1e13", "1e14", "1e15")')''')
_s('os.path.join(HERE, "zn1_shapes.json")', 'os.path.join(HERE, "zn4_shapes.json")')
_s('TAG = "zn1_MUTATE" if MUT else "zn1"', 'TAG = "zn4_MUTATE" if MUT else "zn4"')
_s('os.environ.get("ZN1_BOOT_TAG", "zn1_boot")', 'os.environ.get("ZN1_BOOT_TAG", "zn4_boot")')
_s('os.path.join(HERE, "zn1_results.json")', 'os.path.join(HERE, "zn4_results.json")', 2)
_s('''P(f"ZN1 grade {TAG}:''', '''P(f"ZN4 grade {TAG}:''')
_s('open(xf, "w").write(GAS if gas else "")', 'open(xf, "w").write(({True: GAS, 92: GAS.replace("0.111", "0.092"), 5: GAS.replace("0.111", "0.005")}[gas]) if gas else "")')
_s('with ThreadPoolExecutor(4) as ex: RR =', 'JOBS += [(f"f* {fs}, gas +{d_}", dict(fs=fs, mode="fs", gas=g_, shapes=SH)) for d_, g_ in (("0.092", 92), ("0.005", 5)) for fs in ("0.034", "0.0615")]\n    with ThreadPoolExecutor(4) as ex: RR =')
_s('json.dump(dict(verdict=V, tags=tags, runs=RES)', 'V92 = cls(res["f* 0.034, gas +0.092"], res["f* 0.0615, gas +0.092"]); V5 = cls(res["f* 0.034, gas +0.005"], res["f* 0.0615, gas +0.005"]); P(f"CLASS at +0.092: {V92}. CLASS at +0.005 (GS4, reported): {V5}")\n    json.dump(dict(verdict=V, v092=V92, v005=V5, tags=tags, runs=RES)')
if "--k1" in sys.argv:
    SHZ = os.path.join(ZN3D, "zn3_shapes.json"); _k = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:'); exec(compile(T3[:_k], __file__, "exec"))
    J = json.load(open(os.path.join(ZN3D, "zn3_results.json")))["runs"]; ok = True
    for fs in ("0.034", "0.0615"):
        R = run(fs, "fs", True, SHZ); O = cells(R); C = J[f"f* {fs}, X-COP's gas"]; d = max(abs(O[h][k]["pred"] - C["cells"][h][k]["pred"]) for h in HH for k in C["cells"][h]); dx = max(abs(R["footings"]["canonical"][k] - C["xcop"][k]) for k in ("mean", "rms")); ok &= d == 0 and dx == 0; P(f"K1 f* {fs}, ng 64 stacks through this path against ZN3: preds {d:.1e}, X-COP {dx:.1e}: {'PASS' if (d == 0 and dx == 0) else 'FAIL'}")
    open(os.path.join(HERE4, "zn4_k1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
exec(compile(T3, os.path.abspath(__file__), "exec"))
