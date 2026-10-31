#!/usr/bin/env python3
"""NZ1, POST-RESULT, reported only: NZ1's rule with eRASS1's Mgas500 raised by SM1's matched +0.111 dex, as GX2 did for its halos. X-COP keeps its own gas. CLUSTERS mode, SPARC and groups unchanged.
    python3 nz1_gas.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade")
T = open(os.path.join(HERE, "nz1_grade.py")).read()
a = '    A = "sys.argv = [SRC]\\n"; assert TX.count(A) == 1'; assert T.count(a) == 1
T = T.replace(a, '    MY += open(os.environ["NZ1_GASFILE"]).read()\n' + a)
TD = tempfile.mkdtemp(); GF = os.path.join(TD, "gas.py")
open(GF, "w").write("""_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\' % (10 ** 0.111))\\n'
sub('NX = {"__file__": X30SRC,', _x + 'NX = {"__file__": X30SRC,')
""")
W = os.path.join(HERE, "_nz1_gas_worker.py"); open(W, "w").write(T)
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("NZ1 + eRASS1 gas +0.111 dex, POST-RESULT, reported only; CLUSTERS mode; X-COP keeps its own gas; kappa = 1/2 FITTED; footings never pooled; not theory closed [cluster masses ng 48]")
RES = {}
try:
    for fs in ("0.034", "0.0615"):
        WD = os.path.join(TD, fs); os.makedirs(WD); t = os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"); o = os.path.join(WD, "o.json")
        env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, NZ1_MODE="clusters", NZ1_R0X="1", NZ1_GASFILE=GF, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
        p = subprocess.run(["nice", "-n", "15", sys.executable, W, "--worker"], cwd=WD, env=env, capture_output=True, text=True)
        if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-900:]}")
        R = json.load(open(o)); RES[fs] = R; F = R["grader"]["canonical"]; c = F["clusters"]["cells"]; x = R["footings"]["canonical"]; n = R["nz1"]
        P(f"  f* {fs}: failing {F['failing']}; X-COP mean {x['mean']:+.3f} rms {x['rms']:.3f}; gamma med {n['gam_med']:.3f}; SPARC U {F['sparc']['A_c2b_refit']['U_median']:.2f}/{F['sparc']['B_cfg886_bg']['U_median']:.2f}; groups Z {F['groups']['Z']:+.2f}")
        for h in ("h0672", "h0686"): P(f"     {h}: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in c[h].items()))
finally:
    os.remove(W)
json.dump(RES, open(os.path.join(HERE, "nz1_gas_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nz1_gas.out"), "w").write("\n".join(OUT) + "\n")
