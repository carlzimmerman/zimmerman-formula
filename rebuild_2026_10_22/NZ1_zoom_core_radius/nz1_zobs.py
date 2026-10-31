#!/usr/bin/env python3
"""NZ1, POST-RESULT, reported only: NZ1's rule with S and r_f at each cluster's own z_obs (MA1's stress test), with and without eRASS1's gas on X-COP's scale (+0.111 dex, SM1). CLUSTERS mode; SPARC and groups at z = 0, unchanged; X-COP keeps its own gas.
    python3 nz1_zobs.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade")
T = open(os.path.join(HERE, "nz1_grade.py")).read()
a = '    A = "sys.argv = [SRC]\\n"; assert TX.count(A) == 1'; assert T.count(a) == 1
T = T.replace(a, '    MY += open(os.environ["NZ1_XFILE"]).read()\n' + a)
TD = tempfile.mkdtemp(); W = os.path.join(HERE, "_nz1_zobs_worker.py"); open(W, "w").write(T)
GAS = """_x = '_g = \\'Mg500 = cl["Mgas500"]*qd**2.5;\\'; assert codeX.count(_g) == 1; codeX = codeX.replace(_g, \\'Mg500 = cl["Mgas500"]*qd**2.5*%r;\\' % (10 ** 0.111))\\n'
sub('NX = {"__file__": X30SRC,', _x + 'NX = {"__file__": X30SRC,')
"""
ZOB = r'''
_z = """ZOBS = dict(D=1.0, E2=1.0); ZSTAT = dict(sz=[])
def zobs_set(tag, z):
    e = EPS[tag]; ZOBS["D"] = float(np.interp(z, e["zg"], e["Dg"])); ZOBS["E2"] = NAT_OM * (1 + z) ** 3 + 1 - NAT_OM
def zobs_reset(): ZOBS["D"] = 1.0; ZOBS["E2"] = 1.0
"""
sub('def zform(tag, M):', _z + 'def zform(tag, M):')
sub('S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0)); Df = DC / (DC + OMEGA * S)', 'S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0)); Df = DC / (DC / ZOBS["D"] + OMEGA * S)')
sub('thr = 200 * rc if MA1_MODE == "m200" else 18 * math.pi ** 2 * NAT_OM * rc', 'thr = (200 * rc if MA1_MODE == "m200" else 18 * math.pi ** 2 * NAT_OM * rc) * ZOBS["E2"]')
sub('pp = prep(int(i), foot, hk); Mtot = ma1_arg(foot, tag, pp)', 'pp = prep(int(i), foot, hk); zobs_set(tag, NX["CL"][int(i)]["z"]); Mtot = ma1_arg(foot, tag, pp)')
sub('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'zobs_reset(); V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)')
'''
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("NZ1 with S and r_f at each cluster's z_obs, POST-RESULT, reported only; CLUSTERS mode; X-COP keeps its own gas and z = 0; kappa = 1/2 FITTED; footings never pooled; not theory closed [cluster masses ng 48]")
RES = {}
try:
    for lab, txt in (("z_obs, gas on X-COP's scale", GAS + ZOB), ("z_obs, eRASS1's own gas", ZOB)):
        for fs in ("0.034", "0.0615"):
            WD = os.path.join(TD, f"{len(RES)}"); os.makedirs(WD); t = os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"); o = os.path.join(WD, "o.json"); xf = os.path.join(WD, "x.py"); open(xf, "w").write(txt)
            env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, NZ1_MODE="clusters", NZ1_R0X="1", NZ1_XFILE=xf, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
            p = subprocess.run(["nice", "-n", "15", sys.executable, W, "--worker"], cwd=WD, env=env, capture_output=True, text=True)
            if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {lab} {fs} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-900:]}")
            R = json.load(open(o)); RES[f"{lab}|{fs}"] = R; F = R["grader"]["canonical"]; c = F["clusters"]["cells"]; x = R["footings"]["canonical"]; n = R["nz1"]
            P(f"  {lab}, f* {fs}: failing {F['failing']}; X-COP mean {x['mean']:+.3f} rms {x['rms']:.3f}; gamma med {n['gam_med']:.3f}; SPARC U {F['sparc']['A_c2b_refit']['U_median']:.2f}/{F['sparc']['B_cfg886_bg']['U_median']:.2f}; groups Z {F['groups']['Z']:+.2f}")
            for h in ("h0672", "h0686"): P(f"     {h}: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in c[h].items()))
finally:
    os.remove(W)
json.dump(RES, open(os.path.join(HERE, "nz1_zobs_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "nz1_zobs.out"), "w").write("\n".join(OUT) + "\n")
