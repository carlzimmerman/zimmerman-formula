#!/usr/bin/env python3
"""HB1, against ZN4 separately (FROZEN_CRITERIA.md): ZN4's chain at gas +0.005, its native z = 0 shape, Form B built numerically from each cluster's M0(r). ZN1, ZN3, ZN4 read only. Each job cached. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
HERE6 = os.path.dirname(os.path.abspath(__file__)); RB6 = os.path.dirname(HERE6); ZN1D = os.path.join(RB6, "ZN1_zooms_to_z0"); ZN4D = os.path.join(RB6, "ZN4_cluster_resolution"); T3 = open(os.path.join(ZN1D, "zn1_grade.py")).read()
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
K = T3.index('if __name__ == "__main__":\n    if "--k3" in sys.argv:')
exec(compile(T3[:K], os.path.abspath(__file__), "exec"))
SH = os.path.join(ZN4D, "zn4_shapes.json"); G5 = GAS.replace("0.111", "0.005"); assert G5 != GAS; CJ = os.path.join(HERE6, "cache_zn4_jobs"); os.makedirs(CJ, exist_ok=True)
WRAP = r'''
import sys as _sy; _sy.path.insert(0, %r); _sy.dont_write_bytecode = True; import hb1_core as _HB
_ZFN0 = zn1_fn; HBZ = dict(nonmono=[], null=[], noroot=0, top=[])
def zn1_fn(foot, tag, pp, z):
    f0 = _ZFN0(foot, tag, pp, z); M0 = np.asarray(f0(RM), float); Mf, s_ = _HB.numeric_B(RM, pp["Mb"], M0); HBZ["nonmono"].append(s_["nonmono"]); HBZ["null"].append(9.9 if s_["null"] is None else s_["null"]); HBZ["noroot"] += int(s_["st"] == 1); HBZ["top"].append(s_["top_ratio"] or 0.0); lr = np.log(RM)
    open(%r, "w").write(json.dumps(dict(n=len(HBZ["null"]), nonmono_med=float(np.median(HBZ["nonmono"])), null_med=float(np.median(HBZ["null"])), null_max=float(np.max(HBZ["null"])), noroot=HBZ["noroot"], Hc_over_top_med=float(np.median(HBZ["top"]))))); return lambda r: np.interp(np.log(np.maximum(np.asarray(r, float), RM[0])), lr, Mf)
'''
def xfile(var, statf):
    if var == "OFF": return G5
    return G5 + "sub('def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):', " + repr(WRAP % (HERE6, statf)) + " + 'def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):')\n"
def job(var, fs):
    f = os.path.join(CJ, f"{var}_{fs}.json"); sf = f[:-5] + "_stat.json"
    if os.path.exists(f): return json.load(open(f))
    R = run(fs, "fs", xfile(var, sf), SH); O = dict(cells=cells(R), xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms")}, stat=json.load(open(sf)) if os.path.exists(sf) else None); json.dump(O, open(f + ".tmp", "w"), default=float); os.replace(f + ".tmp", f); return O
OUTL = []
def PP(s=""): print(s, flush=True); OUTL.append(s)
Z4 = json.load(open(os.path.join(ZN4D, "zn4_results.json")))["runs"]; RES = {}; ok = True; PP("HB1 vs ZN4: chain at gas +0.005, native shape; kappa = 1/2 FITTED, unused; not theory closed")
for fs in ("0.034", "0.0615"):
    A = job("OFF", fs); C = Z4[f"f* {fs}, gas +0.005"]; d = max(abs(A["cells"][h][k]["pred"] - C["cells"][h][k]["pred"]) for h in HH for k in C["cells"][h]); dx = max(abs(A["xcop"][k] - C["xcop"][k]) for k in ("mean", "rms")); oo = d <= 1e-6 and dx <= 1e-6; ok &= oo; PP(f"base f* {fs} against ZN4's job: preds {d:.1e}, X-COP {dx:.1e}: {'PASS' if oo else 'FAIL'}")
    for v in ("OFF", "HB"):
        Q = job(v, fs); bad = sorted({k for h in HH for k, x in Q["cells"][h].items() if abs(x["Z"]) > 2}); RES[f"{v}|{fs}"] = dict(n=15 - len(bad), bad=bad, Z={h: {k: x["Z"] for k, x in Q["cells"][h].items()} for h in HH}, xcop=Q["xcop"], stat=Q["stat"]); PP(f"{v} f* {fs}: {15 - len(bad)} of 15, over 2 {bad}; X-COP {Q['xcop']['mean']:+.3f}, {Q['xcop']['rms']:.3f}; G-OUT-M3 {Q['cells']['h0672']['G-OUT-M3']['Z']:+.2f}/{Q['cells']['h0686']['G-OUT-M3']['Z']:+.2f}; G-IN-Mall {Q['cells']['h0672']['G-IN-Mall']['Z']:+.2f}; stat {Q['stat']}")
json.dump(dict(ok=ok, rows=RES), open(os.path.join(HERE6, "hb1_zn4_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE6, "hb1_zn4.out"), "w").write("\n".join(OUTL) + "\n"); sys.exit(0 if ok else 1)
