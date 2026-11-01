#!/usr/bin/env python3
"""DR6 grade (FROZEN_CRITERIA.md): ZN4's grader text at gas +0.005 with the native two-halo term injected as a mass source. No output lands in other lanes. Serial, one thread, resumable: each job's result cached in cache_jobs; SIGTERM exits 75.
    python3 dr6_grade.py            # all jobs, K1, K5, MUTATE-run, tables
kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, signal, sys, tempfile
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
SH = os.path.join(ZN4D, "zn4_shapes.json"); G5 = GAS.replace("0.111", "0.005"); assert G5 != GAS
PK = os.path.join(HERE6, "dr6_pk.json"); CJ = os.path.join(HERE6, "cache_jobs"); os.makedirs(CJ, exist_ok=True); INJT = open(os.path.join(HERE6, "dr6_inject.py")).read()
def xfile(var, sign, rowf):
    head = f"DR6_PK = {PK!r}; DR6_VAR = {var!r}; DR6_SIGN = {sign!r}; DR6_ROWF = {rowf!r}\n"
    return G5 + f"sub('def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):', {(head + INJT)!r} + 'def grade_clusters(foot, rule=True, tag=\"A_c2b_refit\"):')\n" + """sub('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh + (dr6_m2(int(i), pp, Mh, foot, hk) if (SHAPE["s"] == "S" and ETA_USE["v"] == ETA) else 0.0))')\n"""
signal.signal(signal.SIGTERM, lambda *a: (_ for _ in ()).throw(KeyboardInterrupt()))
def job(var, fs, sign=1.0):
    f = os.path.join(CJ, f"{var}_{fs}_{sign:+g}.json"); rowf = f[:-5] + "_rows.json"
    if os.path.exists(f): return json.load(open(f))
    try: R = run(fs, "fs", xfile(var, sign, rowf), SH)
    except KeyboardInterrupt: sys.exit(75)
    O = dict(cells=cells(R), xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms")}, groupsZ=R["grader"]["canonical"]["groups"]["Z"]); json.dump(O, open(f + ".tmp", "w"), default=float); os.replace(f + ".tmp", f); return O
if "--x10" in sys.argv:   # POST-RESULT, disclosed: the frozen MUTATE line 0.5 failed; does the term reach the keys linearly? Reported; doesn't restore a verdict
    R = job("C2", "0.034", 10.0); B = job("OFF", "0.034"); C = job("C2", "0.034"); L = []
    for k in ("G-OUT-M3", "G-OUT-Mall", "G-MID-T3", "G-OUT-M1", "G-IN-Mall"):
        L.append(f"{k} h0672: Z {B['cells']['h0672'][k]['Z']:+.2f} > C2 {C['cells']['h0672'][k]['Z']:+.2f} > C2 x 10 {R['cells']['h0672'][k]['Z']:+.2f}; pred {B['cells']['h0672'][k]['pred']:.3f} > {C['cells']['h0672'][k]['pred']:.3f} > {R['cells']['h0672'][k]['pred']:.3f}")
    bad = sorted({k for h in HH for k, v in R["cells"][h].items() if abs(v["Z"]) > 2}); L.append(f"C2 x 10, f* 0.034: over 2 {bad}"); open(os.path.join(HERE6, "dr6_post_x10.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L)); sys.exit(0)
OUTL = []; 
def PP(s=""): print(s, flush=True); OUTL.append(s)
Z4 = json.load(open(os.path.join(ZN4D, "zn4_results.json")))["runs"]; RES = {}; FS = ("0.034", "0.0615")
PP("DR6 grade: ZN4's chain, gas +0.005, native two-halo term; kappa = 1/2 FITTED, unused; not theory closed")
ok = True
for fs in FS:
    A = job("OFF", fs); C = Z4[f"f* {fs}, gas +0.005"]; d = max(abs(A["cells"][h][k]["pred"] - C["cells"][h][k]["pred"]) for h in HH for k in C["cells"][h]); dx = max(abs(A["xcop"][k] - C["xcop"][k]) for k in ("mean", "rms")); oo = d <= 1e-6 and dx <= 1e-6; ok &= oo
    PP(f"K1 f* {fs} term off against ZN4: preds {d:.1e}, X-COP {dx:.1e}: {'PASS' if oo else 'FAIL'}")
if not ok: sys.exit("K1 failed: no verdict")
for var in ("C1", "C3", "C2"):
    for fs in FS:
        R = job(var, fs); B = job("OFF", fs); RES[f"{var}|{fs}"] = R; bad = sorted({k for h in HH for k, v in R["cells"][h].items() if abs(v["Z"]) > 2}); bad0 = sorted({k for h in HH for k, v in B["cells"][h].items() if abs(v["Z"]) > 2})
        PP(f"{var} f* {fs}: {15 - len(bad)} of 15, over 2 {bad}; X-COP {R['xcop']['mean']:+.3f} {R['xcop']['rms']:.3f}; newly over {sorted(set(bad) - set(bad0))}")
        for h in HH: PP(f"   {h}: " + "; ".join(f"{k} {B['cells'][h][k]['Z']:+.2f}>{v['Z']:+.2f}" for k, v in R["cells"][h].items()))
        for k in ("G-OUT-M3", "G-OUT-Mall", "G-MID-T3"):
            for h in HH:
                b, r = B["cells"][h][k], R["cells"][h][k]; N = b["meas"] - 2 * b["s"] - b["pred"]; PP(f"   supply {k} {h}: pred {b['pred']:.3f} > {r['pred']:.3f} ({r['pred'] / b['pred'] - 1:+.3f}), need {N:+.3f} ({N / b['pred']:+.3f}), fraction {(r['pred'] - b['pred']) / N if N > 0 else float('nan'):.3f}")
R = job("C2", "0.034", -1.0); C2 = job("C2", "0.034"); B = job("OFF", "0.034"); dm = R["cells"]["h0672"]["G-OUT-M3"]["Z"] - B["cells"]["h0672"]["G-OUT-M3"]["Z"]; d2 = C2["cells"]["h0672"]["G-OUT-M3"]["Z"] - B["cells"]["h0672"]["G-OUT-M3"]["Z"]; mut = abs(dm) >= 0.5 and dm * d2 < 0
if abs(dm) < 0.5 and abs(d2) < 0.5: PP(f"MUTATE C2 sign flipped: G-OUT-M3 moves {dm:+.2f}, C2 {d2:+.2f}: {'BITES' if mut else 'DOES NOT BITE (frozen line 0.5)'}")
else: PP(f"MUTATE C2 sign flipped: G-OUT-M3 moves {dm:+.2f}, C2 {d2:+.2f}: {'BITES' if mut else 'DOES NOT BITE'}")
sh = max(abs(RES[f"C1|{fs}"]["cells"][h]["G-OUT-M3"]["pred"] / job("OFF", fs)["cells"][h]["G-OUT-M3"]["pred"] - 1) for fs in FS for h in HH); PP(f"K5 C1's share of G-OUT-M3, worst {sh:.4f}: {'PASS' if sh <= 0.02 else 'FAIL'}")
json.dump(dict(k5=sh, mutate=dict(dm=dm, d2=d2, bites=bool(mut)), runs=RES), open(os.path.join(HERE6, "dr6_results.json"), "w"), default=float, indent=0)
open(os.path.join(HERE6, "dr6.out"), "w").write("\n".join(OUTL) + "\n")
