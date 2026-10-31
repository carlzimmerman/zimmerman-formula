#!/usr/bin/env python3
"""AM1_native_abundance_match (FROZEN_CRITERIA.md): Press-Schechter on the native sigma(M) matched to am1_bmf.json; the relation against EM1's; the SPARC line and groups with it.
    python3 am1_match.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72)
if "--worker" in sys.argv:
    WD = os.environ["AM1_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read(); INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
_d = '''AM1_CURVE = json.load(open(os.environ["AM1_CURVE"])) if os.environ.get("AM1_CURVE") else None
def am1_lm(x, bg):
    if AM1_CURVE is None: return bg["a"] + bg["b"] * (x - 10)
    return float(np.interp(x, AM1_CURVE["lMb"], AM1_CURVE["lM200"]))
'''
sub('def sparc(f, tag, rule=True):', _d + 'def sparc(f, tag, rule=True):')
sub('lM = bg["a"] + bg["b"] * (q["lMb"] - 10); M200 = 10 ** lM;', 'lM = am1_lm(q["lMb"], bg); M200 = 10 ** lM;')
sub('M200 = 10 ** (bg["a"] + bg["b"] * (lMb - 10)) * MS540;', 'M200 = 10 ** am1_lm(lMb, bg) * MS540;')
sub('    return max(s, sc), sc > s', '''    return (sc * 10 ** (float(os.environ["AM1_NS"]) * max(0.0, 12.0 - math.log10(M))), True) if os.environ.get("AM1_NS") and ETA_USE["v"] == ETA else (max(s, sc), sc > s)''')
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", '''json.dump(dict(footings={{f_: dict(sparc={{t_: {{k_: RES["footings"][f_]["sparc"][t_][k_] for k_ in ("rms", "U_median", "line")}} for t_ in BGS}}, groups={{k_: RES["footings"][f_]["groups"][k_] for k_ in ("mean", "Z", "verdict", "PASS")}}) for f_ in FEET}}), open(os.environ["AM1_OUT"], "w"), indent=1, default=float); sys.exit(0)''')
"""
    if os.environ.get("AM1_SIGMA"): MY += """
sub('k2 = all(abs(EPS[t]["s8"] - EPS[t]["s8F3"]) <= 1e-3 for t in EPS)', 'e_ = EPS["A_c2b_refit"]; json.dump(dict(lMg=e_["lMg"].tolist(), s2=e_["s2"].tolist(), rhom0=e_["rhom0"], h=e_["h"], DC=DC), open(os.environ["AM1_SIGMA"], "w")); sys.exit(0)')
"""
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
import numpy as np
from scipy.special import erfc
MUT = "--mutate" in sys.argv; TAG = "am1_MUTATE" if MUT else "am1"; OUT = []; TD = tempfile.mkdtemp()
def P(s): print(s, flush=True); OUT.append(s)
def grade(curve, ns=None, lab="x"):
    WD = os.path.join(TD, lab); os.makedirs(WD); o = os.path.join(WD, "o.json"); env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), X73_FSTAR="0.034", X73_SLOPE=SLOPE, AM1_OUT=o, AM1_WD=WD, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    if curve is not None: cf = os.path.join(WD, "c.json"); json.dump(curve, open(cf, "w")); env["AM1_CURVE"] = cf
    if ns is not None: env["AM1_NS"] = str(ns)
    p = subprocess.run(["nice", "-n", "5", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {lab}: exit {p.returncode}: {p.stdout[-300:]} {p.stderr[-1200:]}")
    r = json.load(open(o)); shutil.rmtree(WD, ignore_errors=True); return r
# sigma(M): X73's own table through a small read of its text
def sigma_table():
    WD = tempfile.mkdtemp(); o = os.path.join(WD, "s.json"); env = dict(os.environ, AM1_SIGMA=o, AM1_WD=WD, AM1_OUT=os.path.join(WD, "unused.json"), FC1_MODE="cold", X74_CF="const4", X73_FSTAR="0.034", X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "5", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"no sigma table: {p.stdout[-300:]} {p.stderr[-800:]}")
    J = json.load(open(o)); shutil.rmtree(WD, ignore_errors=True); return J
E = sigma_table(); json.dump(E, open(os.path.join(HERE, "am1_sigma.json"), "w")); LM = np.array(E["lMg"]); SIG = np.sqrt(np.array(E["s2"])); RHO = E["rhom0"]; DC = E["DC"]; dln = np.gradient(np.log(SIG), np.log(10 ** LM)); nu = DC / SIG
FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
P(f"{TAG}: native Press-Schechter against GAMA's baryons; delta_c {DC:.4f}, rho_m {RHO:.4e} Msun/Mpc^3, f_c {FC:.5f}; kappa = 1/2 FITTED; footings never pooled; not theory closed")
fPS = np.sqrt(2 / np.pi) * nu * np.exp(-nu ** 2 / 2); a_, p_, A_ = 0.707, 0.3, 0.3222; fST = A_ * np.sqrt(2 * a_ / np.pi) * (1 + (a_ * nu ** 2) ** (-p_)) * nu * np.exp(-a_ * nu ** 2 / 2)
def nh_cum(f):
    d = RHO / 10 ** LM * f * np.abs(dln) * math.log(10); dl = LM[1] - LM[0]; c = np.concatenate([np.cumsum(0.5 * (d[1:] + d[:-1])[::-1] * dl)[::-1], [0.0]]); return c, d
cPS, dPS = nh_cum(fPS); cST, dST = nh_cum(fST)
mass_int = float(np.trapz(RHO * fPS * np.abs(dln) * math.log(10), LM)); ex = RHO * float(erfc(nu[0] / math.sqrt(2)) - erfc(nu[-1] / math.sqrt(2))); k1 = abs(mass_int - ex) / RHO <= 2e-3; P(f"K1 PS mass integral over the table against erfc: {abs(mass_int - ex) / RHO:.1e} of rho_m: {'PASS' if k1 else 'FAIL'}")
B = json.load(open(os.path.join(HERE, "am1_bmf.json"))); GR = np.array(B["grid"])
def match(key, cH=cPS, fac=1.0):
    nb = np.array(B[key]) * fac; X = np.arange(8.0, 12.26, 0.05); nx = np.exp(np.interp(X, GR, np.log(np.maximum(nb, 1e-30)))); ok = cH > 1e-30; o = np.argsort(np.log(cH[ok])); return X, np.interp(np.log(nx), np.log(cH[ok])[o], LM[ok][o])
def curve(X, lMt):
    i = np.searchsorted(X, 9.0); s = float(np.polyfit(X[i:i + 11], lMt[i:i + 11], 1)[0]); xl = np.arange(6.0, X[0], 0.05); yl = lMt[0] + s * (xl - X[0]); return dict(lMb=np.concatenate([xl, X]).tolist(), lM200=(np.concatenate([yl, lMt]) + math.log10(FC)).tolist())
def read(X, lMt, tag_=""):
    C = curve(X, lMt); f = lambda lg: float(np.interp(lg, C["lMb"], C["lM200"])); k = (X >= 9.5 - 1e-9) & (X <= 10.5 + 1e-9); sl = float(np.polyfit(X[k], lMt[k], 1)[0]); return C, f(10.0), sl, {lg: f(lg) for lg in (9.0, 10.0, 11.0, 11.5)}
EM1 = lambda lg: 11.18 + 0.90 * (lg - 10)
X, lMt = match("cen", fac=2.0 if MUT else 1.0); C0, v10, sl, tb = read(X, lMt)
def cla(v, s): return "AM MATCHES EM1" if abs(v - 11.18) <= 0.12 and abs(s - 0.90) <= 0.10 else "AM HIGH" if v > 11.45 else "AM LOW" if v < 11.06 else "AM INTERMEDIATE"
vT = float(np.interp(10.0, X, lMt)); V = cla(v10, sl); V2 = cla(vT, sl); tags = "" if V == V2 else " [MASS-CONVENTION-DEPENDENT]"
P(f"Match (centrals, PS): cold M200 at lg M_b 10 {v10:.3f} (EM1 11.18, Delta {v10 - 11.18:+.3f}), total M_t {vT:.3f}; slope 9.5-10.5 {sl:.3f} (EM1 0.90); class {V}{tags}; total-mass class {V2}"); P("  relation, cold M200 [EM1]: " + "; ".join(f"lg M_b {lg}: {v:.2f} [{EM1(lg):.2f}]" for lg, v in tb.items()))
if MUT:
    J = json.load(open(os.path.join(HERE, "am1_results.json"))); d = v10 - J["v10"]; ok = abs(d) > 0.03; P(f"MUTATE n_b x 2 moves lg M200 at 1e10 by {d:+.3f}: {'BITES' if ok else 'INSENSITIVE, UNDECIDED'}"); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
REP = {}
for lab, key, cH in (("all galaxies", "all", cPS), ("M* + 0.2 dex", "cen_plus", cPS), ("M* - 0.2 dex", "cen_minus", cPS), ("z < 0.15", "cen_zlow", cPS), ("Sheth-Tormen [BORROWED FIT]", "cen", cST)):
    x_, l_ = match(key, cH); c_, v_, s_, t_ = read(x_, l_); REP[lab] = dict(curve=c_, v10=v_, slope=s_, table=t_); P(f"  reported, {lab}: cold M200 at 1e10 {v_:.3f}, slope {s_:.3f}; " + "; ".join(f"{lg}: {v:.2f}" for lg, v in t_.items()))
dl = LM[1] - LM[0]; w = int(round(0.45 / dl)); gk = np.exp(-0.5 * (np.arange(-w, w + 1) * dl / 0.15) ** 2); gk /= gk.sum(); dC = np.convolve(dPS, gk, mode="same"); cC = np.concatenate([np.cumsum(0.5 * (dC[1:] + dC[:-1])[::-1] * dl)[::-1], [0.0]]); x_, l_ = match("cen", cC); c_, v_, s_, t_ = read(x_, l_); REP["0.15 dex scatter"] = dict(curve=c_, v10=v_, slope=s_, table=t_); P(f"  reported, 0.15 dex of scatter: cold M200 at 1e10 {v_:.3f}, slope {s_:.3f}; " + "; ".join(f"{lg}: {v:.2f}" for lg, v in t_.items()))
def L(R, f="canonical"): s = R["footings"][f]["sparc"]; return s, R["footings"][f]["groups"]
def spt(R, f="canonical"): s, g = L(R, f); return "; ".join(f"[{t[0]}] rms {s[t]['rms']:.4f} U {s[t]['U_median']:.2f} line {'PASS' if s[t]['line'] else 'FAIL'}" for t in s) + f"; groups mean {g['mean']:+.3f} Z {g['Z']:+.2f} {g['verdict']}"
J0 = json.load(open(os.path.join(FC1, "FC1_x74_results_fs0.034_nat_s2.7774.json"))) if os.path.exists(os.path.join(FC1, "FC1_x74_results_fs0.034_nat_s2.7774.json")) else None
JOBS = [("F, EM1's relation (K3)", None, None), ("N1, EM1's relation", None, S1), ("F, native match", C0, None), ("N1, native match", C0, S1), ("F, all galaxies", REP["all galaxies"]["curve"], None), ("N1, all galaxies", REP["all galaxies"]["curve"], S1), ("F, 0.15 dex scatter", REP["0.15 dex scatter"]["curve"], None), ("N1, 0.15 dex scatter", REP["0.15 dex scatter"]["curve"], S1)]
with ThreadPoolExecutor(4) as ex: RR = dict(zip([j[0] for j in JOBS], ex.map(lambda j: grade(j[1], j[2], re.sub(r"\W+", "_", j[0])), JOBS)))
for k, R in RR.items(): P(f"  {k}, canonical: {spt(R)}"); P(f"     alt: {spt(R, 'alt')}")
FX = json.load(open(os.path.join(HERE, "..", "FC1_cold_share_native_eta", "fc1_results.json"))) if os.path.exists(os.path.join(FC1, "fc1_results.json")) else None
def cSP(R, f="canonical"):
    s, g = L(R, f); bad = [t for t in s if not s[t]["line"]]
    if not bad: return "SPARC SURVIVES"
    t = bad[0]; return "SPARC BREAKS (" + ("U low" if s[t]["U_median"] < 0.5 else "U high" if s[t]["U_median"] > 0.8 else "rms") + ")"
P(f"VERDICT A: {V}{tags}. VERDICT B: F canonical {cSP(RR['F, native match'])}; F alt {cSP(RR['F, native match'], 'alt')}; N1 {cSP(RR['N1, native match'])}")
UA = RR["N1, native match"]["footings"]["canonical"]["sparc"]["A_c2b_refit"]["U_median"]; P(f"Argon: AM1 pass lg M200 11.18 +- 0.12, slope 0.90 +- 0.10; fail above 11.45, with SPARC U below 0.42. Measured {v10:.3f}, {sl:.3f}; N1's U on background A {UA:.2f}")
json.dump(dict(verdict_A=V + tags, v10=v10, slope=sl, table=tb, curve=C0, reported=REP, grades=RR, k1=k1), open(os.path.join(HERE, "am1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "am1.out"), "w").write("\n".join(OUT) + "\n")
