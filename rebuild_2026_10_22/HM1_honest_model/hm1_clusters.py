#!/usr/bin/env python3
"""HM1 clusters (FROZEN_CRITERIA.md): ZN4's grader text with the response on the native shape. No output lands in other lanes. Each job caches per cell; SIGTERM exits 75, rerun resumes.
    python3 hm1_clusters.py JOB [...]; jobs below.
kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, signal, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HM1 = HERE; RB6 = os.path.dirname(HERE); ZN1D = os.path.join(RB6, "ZN1_zooms_to_z0"); ZN4D = os.path.join(RB6, "ZN4_cluster_resolution"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
def _s(a, b, n=1):
    global T3
    assert T3.count(a) == n, a
    T3 = T3.replace(a, b)
_s("""_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(HERE, 'zn1_def.py')!r}).read()""", """_d = open({os.path.join(MA1, 'ma1_def.py')!r}).read() + open({os.path.join(RB, 'ZN1_zooms_to_z0', 'zn1_def.py')!r}).read() + open({os.path.join(RB, 'ZN3_native_shape_at_1e15', 'zn3_def.py')!r}).read()""")
_s('open(os.path.join(HERE, "zn1_boot_tail.py")).read()', 'open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_boot_tail.py")).read()')
_s('open(xf, "w").write(GAS if gas else "")', 'open(xf, "w").write(gas)')
_s('{int(gas)}', '{abs(hash(gas)) % 10 ** 8}')
_s('["nice", "-n", "5", sys.executable', '["nice", "-n", "15", sys.executable')
_s('t = os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json")', 't = os.environ.get("HM1_CF") or os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json")')
_s('''_znf = zn1_fn(foot, _TBG, dict(Mb=_mbx, Mfair=Mfair, rta=rta), _XM[nm]["z"]); k2.append(0.0 if sat else''', '''_znf = hm1_x(zn1_fn(foot, _TBG, dict(Mb=_mbx, Mfair=Mfair, rta=rta), _XM[nm]["z"]), _mbx, rta, Mfair, Mbt, foot); k2.append(0.0 if sat else''')
_s('open(os.path.join(WD, "tail.py"), "w").write(tail)', '''_eh = 'json.dump(_OUT, open(os.environ["XH1_OUT"], "w"), indent=1, default=float)\\nsys.exit(0)'; assert tail.count(_eh) == 1; tail = tail.replace(_eh, "import time\\n" + open(os.environ["HM1_TAIL"]).read() + _eh); open(os.path.join(WD, "tail.py"), "w").write(tail)''')
K = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:')
HERE_SAVE = HERE
exec(compile(T3[:K], os.path.join(ZN1D, "zn1_grade.py") if "--worker" not in sys.argv else os.path.abspath(__file__), "exec"), globals())
HERE = HERE_SAVE
SH = os.path.join(ZN4D, "zn4_shapes.json"); RES = os.path.join(HERE, "cache_cells"); os.makedirs(RES, exist_ok=True)
def xf(gasv, zero=False):
    g = "" if gasv is None else GAS.replace("0.111", gasv)
    return g + f"""
_hmd = open({os.path.join(HM1, 'hm1_def.py')!r}).read()
sub('def grade_clusters(foot, rule=True, tag="A_c2b_refit"):', _hmd + 'def grade_clusters(foot, rule=True, tag="A_c2b_refit"):')
sub('if SHAPE["s"] == "S" and ETA_USE["v"] == ETA: Mh = zn1_fn(foot, tag, pp, NX["CL"][int(i)]["z"])(RM)', 'if SHAPE["s"] == "S" and ETA_USE["v"] == ETA and HM["path"] in ("native", "hybrid"): Mh = zn1_fn(foot, tag, pp, NX["CL"][int(i)]["z"])(RM)')
sub('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, hm1_src(int(i), foot, hk, pp, Mh, s, tag, NX["CL"][int(i)]["z"]))')
"""
PRIM = [("off|none", dict(f=0.0)), ("fq|bcg", dict(f=0.872, bcg=True, alt=True)), ("fq|none", dict(f=0.872)), ("blum|bcg", dict(f=1.0, bcg=True)), ("blum|none", dict(f=1.0)), ("gn|bcg", dict(f=1.0, gn=True, bcg=True)), ("gn|none", dict(f=1.0, gn=True))]
JOBS = {f"N_{g}_{fs}": dict(fs=fs, gas=g, cells=PRIM + ([("fq|bcg|cn1F", dict(f=0.872, bcg=True, fmode="cn1"))] if g == "0.005" and fs == "0.034" else []) + ([("MUTATE fq05|bcg", dict(f=0.436, bcg=True))] if g == "0.005" and fs == "0.034" else [])) for g in ("0.005", "0.111") for fs in ("0.034", "0.0615")}
NR2T = os.path.join(RB6, "NR2_low_mass_ng80", "NR2_MEDIAN_cf_table.json")
SC = [("S|off|none", dict(path="S", f=0.0, dump=True)), ("S|blum|bcg", dict(path="S", f=1.0, bcg=True)), ("S|fq|bcg", dict(path="S", f=0.872, bcg=True)), ("off|none", dict(f=0.0, dump=True)), ("fq|bcg", dict(f=0.872, bcg=True, dump=True)), ("hybrid", dict(path="hybrid", f=0.0)), ("hybrid|fq|bcg", dict(path="hybrid", f=0.872, bcg=True))]
JOBS["S_erass_0.034"] = dict(fs="0.034", gas=None, cf=NR2T, cells=SC[:3]); JOBS["S_0.005_0.034"] = dict(fs="0.034", gas="0.005", cf=NR2T, cells=SC)
JOBS["cn1F_0.005"] = dict(fs="0.034", gas="0.005", cells=[("fq|bcg|cn1F", dict(f=0.872, bcg=True, fmode="cn1"))])
JOBS["S_cn1F_erass"] = dict(fs="0.034", gas=None, cf=NR2T, cells=[("S|blum|bcg|cn1F", dict(path="S", f=1.0, bcg=True, fmode="cn1"))])
for _g in ("0.005", "0.111"):
    for _fs in ("0.034", "0.0615"): JOBS[f"A1_{_g}_{_fs}"] = dict(fs=_fs, gas=_g, cells=[("fq|bcg|A1", dict(f=0.872, bcg=True, amend=True)), ("fq|none|A1", dict(f=0.872, amend=True)), ("blum|bcg|A1", dict(f=1.0, bcg=True, amend=True))] if _fs == "0.034" else [("fq|bcg|A1", dict(f=0.872, bcg=True, amend=True))])
JOBS["P_0.005"] = dict(fs="0.034", gas="0.005", cf=NR2T, cells=[("S|off|none", dict(path="S", f=0.0, dump=True)), ("off|none", dict(f=0.0, dump=True)), ("fq|bcg", dict(f=0.872, bcg=True, dump=True)), ("hybrid", dict(path="hybrid", f=0.0, dump=True))])
JOBS["K4diag"] = dict(fs="0.034", gas="0.005", cells=[("fq|bcg", dict(f=0.872, bcg=True))])
signal.signal(signal.SIGTERM, lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))
def job(n):
    J = JOBS[n]; f = os.path.join(RES, n + ".json")
    if os.path.exists(f): return json.load(open(f))
    os.environ.update(HM1_TAIL=os.path.join(HM1, "hm1_tail.py"), HM1_PART=os.path.join(RES, n + ".part.json"), HM1_CELLS=json.dumps(J["cells"]))
    if J.get("cf"): os.environ["HM1_CF"] = J["cf"]
    else: os.environ.pop("HM1_CF", None)
    try: R = run(J["fs"], "fs", xf(J["gas"]), SH)
    except KeyboardInterrupt: sys.exit(75)
    O = dict(base=cells(R), base_x={k: R["footings"]["canonical"][k] for k in ("mean", "rms", "by_x")}, hm1=R["hm1"], K3=R["hm1_K3"], Rgrid=R["hm1_R"], T3=R["hm1_T3"], groupsZ=R["grader"]["canonical"]["groups"]["Z"], x1=R.get("hm1_x1")); json.dump(O, open(f + ".tmp", "w"), default=float); os.replace(f + ".tmp", f); return O
if __name__ == "__main__":
    for n in (sys.argv[1:] or list(JOBS)): O = job(n); print(n, "done", list(O["hm1"]), flush=True)
