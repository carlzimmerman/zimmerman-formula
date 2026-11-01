#!/usr/bin/env python3
"""OP1 zooms read (FROZEN_CRITERIA.md): measure 1e8, 1e9; rerun P1, P2 with 1e8, 1e9, 1e10 tags interpolated, op1.py's text otherwise; SELF-SIMILAR / BREAKS. kappa = 1/2 FITTED; not theory closed."""
import glob, importlib.util, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN1_zooms_to_z0"); _s = importlib.util.spec_from_file_location("zm", os.path.join(ZD, "zn1_measure.py")); Z = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = ["x"]; _s.loader.exec_module(Z); sys.argv = _a; SHF = os.path.join(HERE, "op1_low_shapes.json")
J = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); X = np.array(J["x"]); mu = lambda y: np.log1p(y) - y / (1 + y); from scipy.optimize import minimize_scalar; sel = (X >= 0.05) & (X <= 1); OUT = []
def PP(s): print(s, flush=True); OUT.append(s)
if "--mutate" not in sys.argv:
    PP("OP1 low zooms; kappa = 1/2 FITTED; not theory closed")
    for M in ("1e8", "1e9"):
        rows = []
        for d in sorted(glob.glob(os.path.join(HERE, "runs", f"M{M}_s?_ng64"))):
            f = os.path.join(d, "snap_z0.00.npz")
            if not os.path.exists(f): continue
            A = np.load(f, allow_pickle=False); me = json.loads(str(A["meta"])); o = Z.measure(A["x"], float(A["m"]), 0.0, me["eps"]); rows.append(dict(seed=os.path.basename(d), lgM=math.log10(o["M200"]), x_edge=o["x_edge"], lnm=o["lnm"], M_over_nom=o["M200"] / me["M"], x_conv=o["x_conv"], R200=o["R200"]))
        assert len(rows) >= 6, M; J[M] = {"0.00": dict(n=len(rows), lgM=float(np.median([q["lgM"] for q in rows])), x_edge=min(q["x_edge"] for q in rows), lnm=np.median([q["lnm"] for q in rows], axis=0).tolist(), seeds=rows)}
    def c200(ln): return float(np.exp(minimize_scalar(lambda q: float(((np.log(mu(np.exp(q) * X[sel]) / mu(np.exp(q))) - np.array(ln)[sel]) ** 2).sum()), bounds=(np.log(.5), np.log(60)), method="bounded").x))
    def stat(t):
        n = J[t]["0.00"]; M = 10 ** n["lgM"]; R = float(np.median([q["R200"] for q in n["seeds"]])); xc = float(np.median([q["x_conv"] for q in n["seeds"]])); return dict(lgM=n["lgM"], c=c200(n["lnm"]), Mr2=math.log10(M * math.exp(float(np.interp(math.log(xc), np.log(X), n["lnm"]))) / (xc * R) ** 2), nom=float(np.median([q["M_over_nom"] for q in n["seeds"]])), xc=xc)
    ST = {t: stat(t) for t in ("1e8", "1e9", "1e10", "1e11", "1e12")}
    for t, v in ST.items(): PP(f"  {t}: n {J[t]['0.00']['n']}; lg M200 {v['lgM']:.3f}, M200/nominal {v['nom']:.3f}, c200 {v['c']:.2f}, lg M/r^2 at 3 eps {v['Mr2']:.3f}, x at 3 eps {v['xc']:.3f}")
    lg = [ST[t]["lgM"] for t in ("1e10", "1e11", "1e12")]; pc = np.polyfit(lg, np.log10([ST[t]["c"] for t in ("1e10", "1e11", "1e12")]), 1); pm = np.polyfit(lg, [ST[t]["Mr2"] for t in ("1e10", "1e11", "1e12")], 1); ss = True
    for t in ("1e9", "1e8"):
        rc = ST[t]["c"] / 10 ** np.polyval(pc, ST[t]["lgM"]); rm = 10 ** (ST[t]["Mr2"] - np.polyval(pm, ST[t]["lgM"])); o = abs(rc - 1) <= .2 and abs(rm - 1) <= .2; ss &= o; PP(f"  {t} against the 1e10-1e12 trend: c200 ratio {rc:.3f}, M/r^2 at 3 eps ratio {rm:.3f}: {'SELF-SIMILAR' if o else 'BREAKS'}")
    PP(f"  overall: {'SELF-SIMILAR' if ss else 'BREAKS'}"); json.dump(J, open(SHF, "w")); open(os.path.join(HERE, "op1_low_zooms.out"), "w").write("\n".join(OUT) + "\n")
T = open(os.path.join(HERE, "op1.py")).read()
def sub(a, b):
    global T
    assert T.count(a) == 1, a
    T = T.replace(a, b)
sub('J = json.load(open(os.path.join(REB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json")))', f'J = json.load(open({SHF!r}))')
sub('if mode == "tag10": return TAGS[0][1]', 'if mode == "tag10": return _low(lg)')
sub('def shape(lg, mode):', '_LT = sorted(((float(J[t]["0.00"]["lgM"]), np.array(J[t]["0.00"]["lnm"])) for t in ("1e8", "1e9", "1e10")), key=lambda x: x[0])\ndef _low(lg):\n    i = 0 if lg < _LT[1][0] else 1; w = float(np.clip((lg - _LT[i][0]) / (_LT[i + 1][0] - _LT[i][0]), 0, 1)); return (1 - w) * _LT[i][1] + w * _LT[i + 1][1]\ndef shape(lg, mode):')
sub('"op1_results" + ("_MUTATE" if MUT else "") + ".json"', '"op1_low_results" + ("_MUTATE" if MUT else "") + ".json"')
exec(compile(T, os.path.join(HERE, "op1.py"), "exec"), {"__file__": os.path.join(HERE, "op1.py"), "__name__": "__main__"})
