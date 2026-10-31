#!/usr/bin/env python3
"""MA1 stress test, POST-RESULT, reported only; it does not change MA1's frozen verdict. MA1's rule still treats every cluster as seen at z = 0. Here each cluster's formation epoch follows from its own z_obs:
    Lacey-Cole with D_f = DC / (DC / D(z_obs) + omega sqrt(dS)), and R200 at 200 rho_c(z_obs). SPARC and groups stay at z = 0. Physically this pushes S up, so it is the check most likely to hurt the pass.
    python3 ma1_zobs.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta")
ZDEF = '''
ZOBS = dict(D=1.0, E2=1.0); ZSTAT = dict(z=[], Dobs=[], sz=[])
def zobs_set(tag, z):
    e = EPS[tag]; ZOBS["D"] = float(np.interp(z, e["zg"], e["Dg"])); ZOBS["E2"] = NAT_OM * (1 + z) ** 3 + 1 - NAT_OM
def zobs_reset(): ZOBS["D"] = 1.0; ZOBS["E2"] = 1.0
'''
if "--worker" in sys.argv:
    WD = os.environ["MA1_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
    INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    d = open(os.path.join(HERE, "ma1_def.py")).read(); a = 'thr = 200 * rc if MA1_MODE == "m200" else 18 * math.pi ** 2 * NAT_OM * rc'; assert d.count(a) == 1; d = d.replace(a, f"thr = ({a[6:]}) * ZOBS['E2']")
    tail = open(os.path.join(HERE, "ma1_tail.py")).read()
    open(os.path.join(WD, "def.py"), "w").write(d); open(os.path.join(WD, "zdef.py"), "w").write(ZDEF); open(os.path.join(WD, "tail.py"), "w").write(tail)
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
sub('def zform(tag, M):', open({os.path.join(WD, 'zdef.py')!r}).read() + 'def zform(tag, M):')
sub('S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0)); Df = DC / (DC + OMEGA * S)', 'S = math.sqrt(max(s2(math.log10(M / 2)) - s2(math.log10(M)), 0.0)); Df = DC / (DC / ZOBS["D"] + OMEGA * S)')
sub('def grade_clusters(foot, rule=True, tag="A_c2b_refit"):', open({os.path.join(WD, 'def.py')!r}).read() + 'def grade_clusters(foot, rule=True, tag="A_c2b_refit"):')
sub('pp = prep(int(i), foot, hk); Mtot = (pp["Mfair"] + float(pp["Mb"][-1])) / MSUNE', 'pp = prep(int(i), foot, hk); zobs_set(tag, NX["CL"][int(i)]["z"]); Mtot = ma1_arg(foot, tag, pp); _sz = sig_core(foot, tag, Mtot, True)[0]; _d0 = ZOBS["D"]; ZOBS["D"] = 1.0; ZSTAT["sz"].append(_sz / sig_core(foot, tag, Mtot, True)[0]); ZOBS["D"] = _d0; ZSTAT["z"].append(NX["CL"][int(i)]["z"])')
sub('V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)', 'zobs_reset(); V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh)')
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", 'MA1_STAT["zstat"] = dict(z_p16=float(np.percentile(ZSTAT["z"], 16)), z_med=float(np.median(ZSTAT["z"])), z_p84=float(np.percentile(ZSTAT["z"], 84)), z_max=float(np.max(ZSTAT["z"])), s_ratio_med=float(np.median(ZSTAT["sz"])), s_ratio_p84=float(np.percentile(ZSTAT["sz"], 84)), s_ratio_max=float(np.max(ZSTAT["sz"])))\\n' + open({os.path.join(WD, 'tail.py')!r}).read())
"""
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
OUT = []; TD = tempfile.mkdtemp()
def P(s): print(s, flush=True); OUT.append(s)
P("MA1 stress test, POST-RESULT, reported only: formation epoch and R200 from each cluster's own z_obs; SPARC and groups at z = 0; kappa = 1/2 FITTED; footings never pooled; not theory closed [cluster masses ng 48]")
def run(fs, g=1.0):
    tag = f"{fs}_{g:g}"; WD = os.path.join(TD, tag); os.makedirs(WD); T = json.load(open(os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json")))
    for m in ("1e+13", "1e+14"): T["cf_by_mass"][m] *= g ** 0.8
    t = os.path.join(WD, "t.json"); json.dump(T, open(t, "w")); o = os.path.join(WD, "o.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {tag} wrote no result (exit {p.returncode}): {p.stdout[-300:]} {p.stderr[-900:]}")
    r = json.load(open(o)); shutil.rmtree(WD, ignore_errors=True); return r
RES = {}
for fs, g in (("0.034", 1.0), ("0.0615", 1.0), ("0.034", 1.1144), ("0.0615", 1.1144)):
    R = run(fs, g); RES[f"g{g:g}_fs{fs}"] = R; F = R["grader"]["canonical"]; s = F["sparc"]; c = F["clusters"]["cells"]; zs = sorted(((v["Z"], k, h) for h in c for k, v in c[h].items()), key=lambda t: -abs(t[0]))
    ok = all(v["line"] for v in s.values()) and not F["failing"]; st = R["ma1"]["zstat"]; x = R["footings"]["canonical"]
    P(f"  g {g:g} f* {fs}: {'PASS' if ok else 'FAIL'}; SPARC U {s['A_c2b_refit']['U_median']:.3f}/{s['B_cfg886_bg']['U_median']:.3f}; groups Z {F['groups']['Z']:+.2f}; worst " + ", ".join(f"{k} {h} {z:+.2f}" for z, k, h in zs[:4]) + f"; failing {F['failing']}")
    P(f"     z_obs med {st['z_med']:.3f} [{st['z_p16']:.3f}, {st['z_p84']:.3f}], max {st['z_max']:.3f}; S(z_obs)/S(z=0) at same M: med {st['s_ratio_med']:.3f}, p84 {st['s_ratio_p84']:.3f}, max {st['s_ratio_max']:.3f}; X-COP mean {x['mean']:+.3f} rms {x['rms']:.3f}")
json.dump(RES, open(os.path.join(HERE, "ma1_zobs_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ma1_zobs.out"), "w").write("\n".join(OUT) + "\n")
