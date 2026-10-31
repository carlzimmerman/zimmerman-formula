#!/usr/bin/env python3
"""FC1 reported lines (criteria 061b2e2a1a): LS1's table by V_flat and ET1's intervals, Milky Way and KiDS via X79's text, at S_cold = f_c eta Sigma_coll(M/f_c).
    python3 fc1_down.py ls1|mw|kids   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, subprocess, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE); WHAT = sys.argv[1]
CE = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]
FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
if WHAT in ("mw", "kids"):
    X79 = os.path.join(FRB, "X79_native_eta_mw_kids"); T = open(os.path.join(X79, f"x79_{WHAT}.py")).read(); ev = [FC * v for v in ETAV]; new = f"np.array({ev!r})"
    if WHAT == "mw":
        pat = 'EV = np.array([S77["1e+12_ng64"]["eta_med"], S77["1e+13_ng48"]["eta_med"], S77["1e+14_ng48"]["eta_med"]])'; assert T.count(pat) == 1; T = T.replace(pat, "EV = " + new)
        pat = "sc = eta_of(M200) * sigma_coll(M200) * 1e6"; assert T.count(pat) == 1; T = T.replace(pat, f"sc = eta_of(M200 / {FC!r}) * sigma_coll(M200 / {FC!r}) * 1e6")
    else:
        pat = '_EV = np.array([_S77["1e+12_ng64"]["eta_med"], _S77["1e+13_ng48"]["eta_med"], _S77["1e+14_ng48"]["eta_med"]])'; assert T.count(pat) == 1; T = T.replace(pat, "_EV = " + new)
    me = os.path.join(FHERE, f"x79_{WHAT}.py"); open(me, "w").write(T); before = set(os.listdir(FHERE)); d = os.path.join(FHERE, "x79_rule"); os.makedirs(d, exist_ok=True)
    p = subprocess.run(["nice", "-n", "15", sys.executable, me], cwd=FHERE, capture_output=True, text=True, env=dict(os.environ, X79_ETA="native", PYTHONHASHSEED="0", OMP_NUM_THREADS="1"))
    open(os.path.join(d, f"x79_{WHAT}.log"), "w").write(p.stdout + p.stderr); os.remove(me)
    for f in set(os.listdir(FHERE)) - before - {f"x79_{WHAT}.py", "x79_rule"}:
        if f.startswith("x79_"): os.replace(os.path.join(FHERE, f), os.path.join(d, f))      # only its own outputs: the grader may share this folder
    print(p.stdout[-2500:]); sys.exit(p.returncode)
LSD = os.path.join(FRB, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FHERE
def M200(q, tag=TAG): b = BGS[tag]; return 10 ** (b["a"] + b["b"] * (q["lMb"] - 10))
def eta_conv(M): return float(np.interp(math.log10(M), [12, 13, 14], ETAV))
def rule_S(f, M, F=FC, MC=FC): return max(SIG[f], F * eta_conv(M / MC) * sigma_coll(TAG, M / MC)[0] * MSUNE / PC2)
def gh_rule(q, f, F=FC, MC=FC, tag=TAG):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = M200(q); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3)
    s = rule_S(f, M, F, MC); r0 = solve_r0(M * MSUNE, R200, s); return GE * math.pi * s * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); ET = json.load(open(os.path.join(FRB, "ET1_core_strength_needed", "et1_results.json")))["ups"]["0.50"]["bins"]; R = {}
print(f"FC1 LS1 table, f_c {FC:.5f}; eta table {ETAV}; kappa = 1/2 FITTED; not theory closed")
for f in ("canonical", "alt"):
    R[f] = {}
    for lo, hi in BINS:
        qs = sel(lo, hi); U, D = [], []
        for q in qs:
            gh = gh_rule(q, f); _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + gh[:, None], 1e-300))); U.append(UPS[iu]); d = dv(q, gh)
            if d is not None: D.append(d)
        k = f"{lo}-{hi}"; e = ET[k]; P_ = rule_S(f, 10 ** e["lgM"]) / (MSUNE / PC2); inside = e["ci"][0] <= P_ <= e["ci"][1]
        R[f][k] = dict(n=len(qs), U=float(np.median(U)), dV=float(np.median(D)), S_rule=P_, ET1=e["med"], ET1_ci=e["ci"], inside=bool(inside), lgM=e["lgM"])
        print(f"  {f} {k}: n {len(qs)} U {np.median(U):.2f} dV {np.median(D):+.1f}; rule S {P_:.0f} vs ET1 {e['med']:.0f} [{e['ci'][0]:.0f},{e['ci'][1]:.0f}] {'inside' if inside else 'outside'}", flush=True)
json.dump(R, open(os.path.join(FHERE, "fc1_ls1.json"), "w"), indent=1)
