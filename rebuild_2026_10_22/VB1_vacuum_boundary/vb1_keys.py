#!/usr/bin/env python3
"""VB1 post-result key read (FROZEN_CRITERIA.md, 'reported not graded'): ZN3's grader text with the 1e14 node replaced by one VB1 run's
shape (A: RS 1.5 control, B: RS 2.0), 1e13 from ZN1 and 1e15 from ZN3 unchanged; X-COP's gas +0.111, eRASS1's own gas, and GS4's measured
+0.005 all reported. Outputs vb1_keys_{A,B}.out / _results.json here; ZN1's and ZN3's files are read only. A single ng 48 seed stands in
for a nine-seed ng 64 stack, so A against B is the comparison, not A against ZN3.
    python3 vb1_keys.py A | B
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, sys
TAGV = sys.argv.pop(1) if len(sys.argv) > 1 and sys.argv[1] in ("A", "B") else os.environ.get("VB1_TAG"); assert TAGV in ("A", "B"); os.environ["VB1_TAG"] = TAGV   # the grader re-runs this file as its worker
HEREV = os.path.dirname(os.path.abspath(__file__)); RBV = os.path.dirname(HEREV); ZN1D = os.path.join(RBV, "ZN1_zooms_to_z0"); ZN3D = os.path.join(RBV, "ZN3_native_shape_at_1e15")
S = json.load(open(os.path.join(ZN3D, "zn3_shapes.json"))); V = json.load(open(os.path.join(HEREV, f"vb1_shape_{TAGV}.json"))); S["1e14"] = V; json.dump(S, open(os.path.join(HEREV, f"vb1_shapes_{TAGV}.json"), "w"))
T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(RB, 'ZN1_zooms_to_z0', 'zn1_def.py')!r}).read() + open({os.path.join(RB, 'ZN3_native_shape_at_1e15', 'zn3_def.py')!r}).read()""")
_s('''open(os.path.join(HERE, "zn1_boot_tail.py")).read()''', '''open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_boot_tail.py")).read().replace('("1e13", "1e14")', '("1e13", "1e14", "1e15")')''')
_s('os.path.join(HERE, "zn1_shapes.json")', f'os.path.join(HERE, "vb1_shapes_{TAGV}.json")')
_s('TAG = "zn1_MUTATE" if MUT else "zn1"', f'TAG = "vb1_keys_{TAGV}_MUTATE" if MUT else "vb1_keys_{TAGV}"')
_s('os.environ.get("ZN1_BOOT_TAG", "zn1_boot")', f'os.environ.get("ZN1_BOOT_TAG", "vb1_keys_{TAGV}_boot")')
_s('os.path.join(HERE, "zn1_results.json")', f'os.path.join(HERE, "vb1_keys_{TAGV}_results.json")', 2)
_s('''P(f"ZN1 grade {TAG}:''', f'''P(f"VB1 key read, run {TAGV} at 1e14 {{TAG}} (reported, not graded):''')
_s('open(xf, "w").write(GAS if gas else "")', 'open(xf, "w").write(({True: GAS, 5: GAS.replace("0.111", "0.005")}[gas]) if gas else "")')
_s('with ThreadPoolExecutor(4) as ex: RR =', 'JOBS += [(f"f* {fs}, gas +0.005", dict(fs=fs, mode="fs", gas=5, shapes=SH)) for fs in ("0.034", "0.0615")]\n    with ThreadPoolExecutor(4) as ex: RR =')
_s('json.dump(dict(verdict=V, tags=tags, runs=RES)', 'V5 = cls(res["f* 0.034, gas +0.005"], res["f* 0.0615, gas +0.005"]); P(f"CLASS at +0.005 (GS4, measured): {V5}")\n    json.dump(dict(verdict=V, v005=V5, tags=tags, runs=RES)')
exec(compile(T3, os.path.abspath(__file__), "exec"))
