#!/usr/bin/env python3
"""NZ2_consistent_m200_shell (FROZEN_CRITERIA.md): NZ1's grader text with nz2_def.py appended, CE1's ng 64 tables, one template.
    python3 nz2_grade.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy.stats import chi2
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade"); NZ1 = os.path.join(RB, "NZ1_zoom_core_radius"); MUT = "--mutate" in sys.argv; TAG = "nz2_MUTATE" if MUT else "nz2"
T = open(os.path.join(NZ1, "nz1_grade.py")).read(); a = '    A = "sys.argv = [SRC]\\n"; assert TX.count(A) == 1'; assert T.count(a) == 1; T = T.replace(a, '    MY += open(os.environ["NZ1_XFILE"]).read()\n' + a)
a = "{os.path.join(HERE, 'nz1_def.py')!r}"; assert T.count(a) == 1; T = T.replace(a, f"{os.path.join(NZ1, 'nz1_def.py')!r}).read() + open({os.path.join(HERE, 'nz2_def.py')!r}")
TD = tempfile.mkdtemp(); W = os.path.join(TD, "worker.py"); open(W, "w").write(T.replace('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {NZ1!r}; RB = {RB!r}'))
C = open(os.path.join(NZ1, "nz1_common_gas.py")).read(); i0 = C.index('GAS = """'); i1 = C.index("OUT = []\n"); exec(C[i0:i1])
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
HH = ("h0672", "h0686")
def run(tag, mode, txt, fs, on="1", go="2.65", r0x="1"):
    WD = os.path.join(TD, f"{tag}_{fs}"); os.makedirs(WD); t = os.path.join(CE1, f"CE1_A4_med_fs{fs}_cf_table.json"); o = os.path.join(WD, "o.json"); xf = os.path.join(WD, "x.py"); open(xf, "w").write(txt + DUMP + "\nsub('_OUT.update(ma1=_st,', '_OUT[\"nz2\"] = dict(NZ2_STAT)\\n_OUT.update(ma1=_st,')\n")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, NZ1_MODE=mode, NZ1_R0X=r0x, NZ1_XFILE=xf, NZ2_ON=on, NZ2_GO=go, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "5", sys.executable, W, "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {tag} {fs} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-1200:]}")
    return json.load(open(o))
def fixed(R):
    c = R["grader"]["canonical"]["clusters"]["cells"]; O = {}
    for h in c:
        m = R["M_outer"][f"canonical|{h}"]; O[h] = {k: dict(v) for k, v in c[h].items()}
        for k, A in [("G-OUT-Mall", m["all"])] + [(f"G-OUT-M{t + 1}", m["terc"][t]) for t in range(3)]:
            v = O[h][k]; s = v["s"] * A / v["meas"]; v.update(meas=A, s=s, Z=(A - v["pred"]) / s)
    return O
BA = json.load(open(os.path.join(RB, "BA1_joint_shear_statistic", "ba1_results.json")))
def joint(cells, RJ, h):
    ks = RJ[h]["keys"]; R = np.array(RJ[h]["R_boot"]); d = np.array([cells[h][k]["meas"] - cells[h][k]["pred"] for k in ks]); s = np.array([cells[h][k]["s"] for k in ks]); w, V = np.linalg.eigh(R); ok = w >= 1e-3 * w.max(); z = V[:, ok].T @ (d / s); c2 = float((z * z / w[ok]).sum()); dof = int(ok.sum()); return c2, dof, float(chi2.sf(c2, dof))
def rep(lab, R, gas):
    O = fixed(R); bad = sorted({k for h in HH for k, v in O[h].items() if abs(v["Z"]) > 2}); x = R["footings"]["canonical"]; g = R["grader"]["canonical"]; v = {h: joint(O, BA["R_gas"] if gas else BA["R_orig"], h) for h in HH}; hw = min(HH, key=lambda q: v[q][2]); P(f"  {lab}: {15 - len(bad)} of 15 keys, over 2 {bad}; X-COP {'PASS' if abs(x['mean']) <= 0.05 and x['rms'] <= 0.10 else 'FAIL'} mean {x['mean']:+.3f} rms {x['rms']:.3f} by x " + " ".join(f"{k} {w:+.3f}" for k, w in x["by_x"].items()) + f"; SPARC U {g['sparc']['A_c2b_refit']['U_median']:.2f}/{g['sparc']['B_cfg886_bg']['U_median']:.2f}; groups Z {g['groups']['Z']:+.2f}; joint chi^2 {v[hw][0]:.1f}/{v[hw][1]}, p {v[hw][2]:.2e}; shell cells {R['nz2']['cells']}, fallback {R['nz2']['fallback']}, flat {R['nz2']['flat']}")
    P("     h 0.672: " + "; ".join(f"{k} {w['Z']:+.2f}" for k, w in O["h0672"].items())); P("     h 0.686: " + "; ".join(f"{k} {w['Z']:+.2f}" for k, w in O["h0686"].items())); return bad, bool(abs(x["mean"]) <= 0.05 and x["rms"] <= 0.10), O
P(f"{TAG}: NZ1's core, shell to f_c M200 at R200, tail to M_fair at r_ta, CE1's ng 64 tables, one template; kappa = 1/2 FITTED; footings never pooled; not theory closed")
if MUT:
    b = run("b", "clusters", GAS, "0.034"); m = run("m", "clusters", GAS, "0.034", r0x="1.5"); d = m["footings"]["canonical"]["rms"] - b["footings"]["canonical"]["rms"]; ok = abs(d) > 0.01; P(f"MUTATE r0 x 1.5 moves X-COP rms by {d:+.3f}: {'BITES' if ok else 'INSENSITIVE, UNDECIDED'}"); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
J0 = json.load(open(os.path.join(NZ1, "nz1_a4_results.json")))["runs"]; print(list(J0)[:8], flush=True)
JOBS = [("k1", "clusters", "", "0.034", "0", "2.65")] + [(f"clusters, X-COP's gas, f* {fs}", "clusters", GAS, fs, "1", "2.65") for fs in ("0.034", "0.0615")] + [(f"clusters, eRASS1's gas, f* {fs}", "clusters", "", fs, "1", "2.65") for fs in ("0.034", "0.0615")] + [(f"all, X-COP's gas, f* {fs}", "all", GAS, fs, "1", "2.65") for fs in ("0.034", "0.0615")] + [(f"clusters, X-COP's gas, z_obs, f* {fs}", "clusters", GAS + ZOB, fs, "1", "2.65") for fs in ("0.034", "0.0615")] + [(f"clusters, X-COP's gas, gamma_o {g}, f* 0.034", "clusters", GAS, "0.034", "1", g) for g in ("2.25", "3.0")]
import re
with ThreadPoolExecutor(4) as ex: RR = dict(zip([j[0] for j in JOBS], ex.map(lambda j: run(re.sub(r"\W+", "_", j[0]), j[1], j[2], j[3], j[4], j[5]), JOBS)))
kk = [k for k in J0 if "clusters" in k and "0.034" in k][0]; c0 = J0[kk]["grader"]["canonical"]["clusters"]["cells"]; c1 = RR["k1"]["grader"]["canonical"]["clusters"]["cells"]; d = max(abs(c0[h][k]["pred"] - c1[h][k]["pred"]) for h in HH for k in c0[h]); k1 = d <= 1e-9; P(f"K1 NZ2 off against NZ1's ng 64 predictions ({kk}): {d:.1e}: {'PASS' if k1 else 'FAIL'}")
k2 = max(max(R["nz2"]["k2a"], R["nz2"]["k2b"]) for k, R in RR.items() if k != "k1"); k2ok = k2 <= 1e-9; P(f"K2 M_c(<R200) and M_c(<r_ta) on every shell cell: {k2:.1e}: {'PASS' if k2ok else 'FAIL'}")
RES = {}
for lab in [j[0] for j in JOBS if j[0] != "k1"]: R = RR[lab]; res = rep(lab, R, "X-COP's gas" in lab); RES[lab] = dict(over2=res[0], xcop_pass=res[1], cells=res[2], xcop={k: R["footings"]["canonical"][k] for k in ("mean", "rms", "by_x")}, groupsZ=R["grader"]["canonical"]["groups"]["Z"], nz2=R["nz2"])
def cls(a, b):
    pa = not RES[a]["over2"] and RES[a]["xcop_pass"]; pb = not RES[b]["over2"] and RES[b]["xcop_pass"]; xb = RES[a]["xcop_pass"] or RES[b]["xcop_pass"]; kb = not RES[a]["over2"] or not RES[b]["over2"]
    return "NZ2 PASSES BOTH" if pa and pb else "F*-DEPENDENT" if pa or pb else "X-COP ONLY" if xb and not kb else "KEYS ONLY" if kb and not xb else "FAILS BOTH" if not xb and not kb else "NEITHER AT ONE f*"
V = cls("clusters, X-COP's gas, f* 0.034", "clusters, X-COP's gas, f* 0.0615"); V2 = cls("clusters, eRASS1's gas, f* 0.034", "clusters, eRASS1's gas, f* 0.0615"); tags = "" if V == V2 else " [GAS-SCALE-DEPENDENT]"; P(f"VERDICT: {V}{tags}. eRASS1's own gas: {V2}. This interior contradicts the measured native profile (M(<r_f) about 0.87 M200 in ZN1, 0.50 here).")
json.dump(dict(verdict=V, tags=tags, runs=RES, k1=d, k2=k2), open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if (k1 and k2ok) else 1)
