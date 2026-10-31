#!/usr/bin/env python3
"""HS1_hsb_lsb_residual_slope (FROZEN_CRITERIA.md): slope of V_model/V_obs - 1 at 2 R_d against lg SBeff, at fixed Upsilon, V_flat 60-120 on SPARC.
    python3 hs1_slope.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE); HMUT = "--mutate" in sys.argv; _av = sys.argv; sys.argv = [sys.argv[0]]
CE = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
LSD = os.path.join(FRB, "LS1_lstar_analogs"); S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(LSD, "ls1_analogs.py")
exec(compile(S[:S.index('P("LS1 SPARC')], "ls1_head", "exec")); HERE = FHERE; sys.argv = _av
from scipy.stats import spearmanr
A0 = NS["A0"]; S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72); S2 = 1.25 * math.log10(8.05 / 5.92); VAR = dict(N0=0.0, N1=S1, N2=S2); OUTL = []
def Pn(s): print(s, flush=True); OUTL.append(s)
SB = {}
for l in open(MRT):
    p = l.split()
    if len(p) < 18: continue
    try: SB[p[0]] = float(p[10])
    except ValueError: pass
def Srule(M, s, tag): Mt = M / FC; return FC * float(np.interp(math.log10(Mt), [12, 13, 14], ETAV)) * 10 ** (s * max(0.0, 12 - math.log10(Mt))) * sigma_coll(tag, Mt)[0] * MSUNE / PC2
def gh_S(q, s, tag, floor=None):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); c = Srule(M, s, tag); c = max(c, floor) if floor is not None else c; r0 = solve_r0(M * MSUNE, R200, c); return GE * math.pi * c * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
def iu_of(U): i = int(np.argmin(abs(UPS - U))); assert abs(UPS[i] - U) < 1e-9; return i
def delta(q, gfun, iu, fac):
    t = TAB[q["name"]]; Rk = q["Rm"] / KPC; R2 = fac * t["rd"]; ok = q["OK"][:, iu]
    if ok.sum() < 2 or R2 < Rk[ok].min() or R2 > Rk[ok].max(): return None
    Vm = np.sqrt(np.maximum(gfun(q, iu) * q["Rm"], 0.0)) / 1e3; return float(np.interp(math.log(R2), np.log(Rk[ok]), Vm[ok] / q["Vobs"][ok] - 1))
def m_route(s, tag, floor=None):
    C = {}
    def f(q, iu):
        if q["name"] not in C: C[q["name"]] = gh_S(q, s, tag, floor)
        return q["GB"][:, iu] + C[q["name"]]
    return f
def m_law(ft):
    def f(q, iu): g = q["GB"][:, iu]; return g * (0.5 + np.sqrt(0.25 + A0[ft] / np.maximum(g, 1e-300)))
    return f
def slope(x, y): x_ = x - x.mean(); return float((x_ * (y - y.mean())).sum() / (x_ * x_).sum())
def boot(x, y, n=10000, seed=1):
    r = np.random.default_rng(seed); b = np.empty(n)
    for i in range(n):
        k = r.integers(0, len(x), len(x)); b[i] = slope(x[k], y[k]) if np.ptp(x[k]) > 0 else np.nan
    return float((np.nanpercentile(b, 84) - np.nanpercentile(b, 16)) / 2)
def measure(gf, lo=60, hi=120, U=0.50, fac=2.0, mut=False):
    iu = iu_of(U); X, Y, nm, drop = [], [], [], 0
    for q in sel(lo, hi):
        d = delta(q, gf, iu, fac)
        if d is None or q["name"] not in SB or SB[q["name"]] <= 0: drop += 1; continue
        X.append(math.log10(SB[q["name"]])); Y.append(d); nm.append(q["name"])
    X, Y = np.array(X), np.array(Y)
    if mut: Y = Y + 0.1 * X
    b = slope(X, Y); s = boot(X, Y); return dict(n=len(X), dropped=drop, b=b, s=s, Z=b / s, cls="FLAT" if abs(b) <= 2 * s else ("TILTED +" if b > 0 else "TILTED -"), rho=float(spearmanr(X, Y)[0]), rms=float(np.sqrt(np.mean(Y ** 2))), mean=float(Y.mean()), x_rng=[float(X.min()), float(X.max())], arr=(X, Y))
TA, TB_ = "A_c2b_refit", "B_cfg886_bg"; SIGF = {f: SIG[f] for f in ("canonical", "alt")}
MOD = lambda tag: {"N1": m_route(S1, tag), "N0": m_route(0.0, tag), "N2": m_route(S2, tag), "F canonical": m_route(0.0, tag, SIGF["canonical"]), "F alt": m_route(0.0, tag, SIGF["alt"]), "law canonical": m_law("canonical"), "law alt": m_law("alt")}
Pn(f"HS1: slope of V_model/V_obs - 1 at 2 R_d against lg SBeff, V_flat 60-120, Q <= 2, Inc >= 30, Upsilon 0.50{' [MUTATE delta + 0.1 x]' if HMUT else ''}; kappa = 1/2 FITTED; footings never pooled; not theory closed")
J = json.load(open(os.path.join(FRB, "NF1_no_floor_rule", "nf1_bins.json"))); k2 = []
for nm, s in (("N1", S1), ("N0", 0.0)):
    U_, D_ = [], []
    for q in sel(60, 100):
        g = gh_S(q, s, TA); _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + g[:, None], 1e-300))); U_.append(UPS[iu]); d = dv(q, g)
        if d is not None: D_.append(d)
    k2.append((abs(float(np.median(U_)) - J[nm]["60-100"]["U"]), abs(float(np.median(D_)) - J[nm]["60-100"]["dV"])))
k2ok = all(a == 0 and b <= 1e-6 for a, b in k2); Pn(f"K2 this path against NF1's table, 60-100: |d U|, |d dV| N1 {k2[0][0]:.3f}, {k2[0][1]:.1e}; N0 {k2[1][0]:.3f}, {k2[1][1]:.1e}: {'PASS' if k2ok else 'FAIL'}")
RES = {}
for tag in (TA, TB_):
    RES[tag] = {}; Pn(f"background {tag}:")
    for nm, gf in MOD(tag).items():
        o = measure(gf, mut=HMUT); x_, y_ = o.pop("arr"); RES[tag][nm] = o
        if nm == "N1" and tag == TA: k1 = abs(o["b"] - float(np.polyfit(x_, y_, 1)[0])) <= 1e-10; Pn(f"K1 slope against polyfit: {abs(o['b'] - float(np.polyfit(x_, y_, 1)[0])):.1e}: {'PASS' if k1 else 'FAIL'}")
        Pn(f"  {nm:14s}: n {o['n']} (dropped {o['dropped']}), b {o['b']:+.4f} +- {o['s']:.4f} per dex ({o['Z']:+.2f} sigma) {o['cls']}; Spearman rho {o['rho']:+.3f}; mean delta {o['mean']:+.3f}, rms {o['rms']:.3f}")
A = RES[TA]; n1, law, F = A["N1"]["cls"].split()[0], A["law canonical"]["cls"].split()[0], A["F canonical"]["cls"].split()[0]
V = {("TILTED", "FLAT"): "N1 TILTED, LAW FLAT", ("FLAT", "FLAT"): "BOTH FLAT", ("FLAT", "TILTED"): "N1 FLAT, LAW TILTED", ("TILTED", "TILTED"): "BOTH TILTED"}[(n1, law)] + ("" if F == n1 else " [F DIFFERS]")
Pn(f"VERDICT on background A, canonical for F and the law: {V}; F {A['F canonical']['cls']}")
def score(b, c, s): return "HIT" if abs(b - c) <= s else "CLOSE" if abs(b - c) <= 2 * s else "MISS"
Pn(f"Argon: N1 +0.085 +- 0.020: measured {A['N1']['b']:+.4f}: {score(A['N1']['b'], 0.085, 0.020)}; law 0.00 +- 0.015: measured {A['law canonical']['b']:+.4f}: {score(A['law canonical']['b'], 0.0, 0.015)}")
if not HMUT:
    Pn("reported: N1 and law canonical, background A, slopes under other choices:"); REP = {}
    for lab, kw in (("U 0.40", dict(U=0.40)), ("U 0.60", dict(U=0.60)), ("1.5 R_d", dict(fac=1.5)), ("3 R_d", dict(fac=3.0)), ("V_flat 40-150", dict(lo=40, hi=150))):
        a = measure(MOD(TA)["N1"], **kw); b = measure(MOD(TA)["law canonical"], **kw); a.pop("arr"); b.pop("arr"); REP[lab] = dict(N1=a, law=b); Pn(f"  {lab}: N1 n {a['n']} b {a['b']:+.4f} +- {a['s']:.4f} {a['cls']}, rms {a['rms']:.3f}; law n {b['n']} b {b['b']:+.4f} +- {b['s']:.4f} {b['cls']}, rms {b['rms']:.3f}")
    json.dump(dict(verdict=V, by_background=RES, reported=REP), open(os.path.join(HERE, "hs1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "hs1.out"), "w").write("\n".join(OUTL) + "\n"); sys.exit(0 if (k1 and k2ok) else 1)
ORIG = json.load(open(os.path.join(HERE, "hs1_results.json")))["by_background"][TA]; dm = max(abs(A[k]["b"] - ORIG[k]["b"] - 0.1) for k in A); ok = dm <= 1e-9; Pn(f"MUTATE changes every slope by +0.1 to within {dm:.1e}: {'BITES' if ok else 'FAIL'}; N1 {ORIG['N1']['cls']} -> {A['N1']['cls']}, law {ORIG['law canonical']['cls']} -> {A['law canonical']['cls']}"); open(os.path.join(HERE, "hs1_MUTATE.out"), "w").write("\n".join(OUTL) + "\n"); sys.exit(0 if ok else 1)
