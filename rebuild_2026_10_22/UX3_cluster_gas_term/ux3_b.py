#!/usr/bin/env python3
"""UX3 Part B discs and X-COP (FROZEN_CRITERIA.md, AMENDMENT_A1.md). Every rule FITTED (search-picked or fitted k). --mutate: k x 3. kappa = 1/2 FITTED; not theory closed."""
import csv, glob, json, sys
from ux3_common import *
from scipy.optimize import minimize_scalar
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; OUT = []; R = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
S = sparc(); ST, SH = S[1], S[0]; X, nm = xcop(); XT = X[X[:, 4].astype(int) % 2 == 0]; XH = X[X[:, 4].astype(int) % 2 == 1]
INP = os.path.join(RB, "CRG1_clean_room_regrade", "inputs"); KPC = 3.0857e19
T = {}
for l in open(os.path.join(INP, "sparc", "SPARC_Lelli2016c.mrt")):
    t = l.split()
    if len(t) == 19:
        try: T[t[0]] = dict(Inc=float(t[5]), L36=float(t[7]), MHI=float(t[13]), Vflat=float(t[15]), Q=float(t[17]))
        except ValueError: pass
GAL = []
for f_ in sorted(glob.glob(os.path.join(INP, "sparc", "rotmod", "*_rotmod.dat"))):
    n = os.path.basename(f_).replace("_rotmod.dat", ""); a = np.loadtxt(f_, comments="#", ndmin=2); GAL.append(dict(name=n, R=a[:, 0] * KPC, Vobs=a[:, 1].copy(), eV=a[:, 2], Vgas=a[:, 3], Vdisk=a[:, 4], Vbul=a[:, 5], **T[n]))
UPS = np.round(np.arange(.30, 1.2000001, .01), 2)
def pathfit(th, a0, k):
    wr2, ws, Yb = [], [], []
    for g in GAL:
        gas = np.sign(g["Vgas"]) * g["Vgas"] ** 2; VB2 = gas + UPS[:, None] * g["Vdisk"] ** 2 + 1.4 * UPS[:, None] * g["Vbul"] ** 2; gb = VB2 * 1e6 / g["R"]; gO = (g["Vobs"] * 1e3) ** 2 / g["R"]; ok = (gb > 0) & (gO > 0) & np.isfinite(gb) & (g["Vobs"] > 0); W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1)) ** 2
        gg = np.maximum(gas, 0) * 1e6 / g["R"]; fq = np.clip(gg / np.where(gb > 0, gb, 1e300), 0, 1); gp = law(np.maximum(gb, 0), a0) * (1 + th(g["R"], g["Vobs"], fq, a0) * k * gg / a0)
        r = np.where(ok, np.log10(np.where(gO > 0, gO, 1.)) - np.log10(np.maximum(gp, 1e-300)), 0.); A = (W[None, :] * r * r * ok).sum(1); B = (W[None, :] * ok).sum(1); q = np.where(B > 0, A / B, np.inf)
        if not np.isfinite(q).any(): Yb.append(np.nan); wr2.append(0.); ws.append(0.); continue
        i = int(np.argmin(q)); wr2.append(A[i]); ws.append(B[i]); Yb.append(UPS[i])
    Yb = np.array(Yb); Qk = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in GAL]); V = np.array([g["Vflat"] for g in GAL]); lo = Qk & (V > 0) & (V < 100); hi = Qk & (V > 150); return dict(rms=math.sqrt(sum(wr2) / sum(ws)), U=float(np.nanmedian(Yb)), tilt=float(np.nanmedian(Yb[lo]) - np.nanmedian(Yb[hi])))
LT = []
for r in csv.DictReader(open(os.path.join(INP, "little_things", "oh2015_table2.csv"))):
    if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun")):
        gm, sm = float(r["Mgas_1e7Msun"]) * 1e7, float(r["MSED_1e7Msun"]) * 1e7; LT.append((float(r["Rmax_kpc"]) * 3.0857e19, float(r["V_kms"]), gm, sm))
LT = np.array(LT)
def ltE(th, a0, k):
    Rr, V, gm, sm = LT.T; g = G * (gm + sm) * MS / Rr ** 2; f = gm / (gm + sm); gg = g * f; return float(np.median(np.log10((V * 1e3) ** 2 / Rr) - np.log10(law(g, a0) * (1 + th(Rr, V, f, a0) * k * gg / a0))))
FG = dict(canonical=(.0541, .52), alt=(.0537, .44)); P(f"UX3 Part B discs + X-COP{TAG}; all rules FITTED; law row first; X-COP lines |mean| <= 0.05, rms <= 0.10; SPARC even rms <= 1.05 law, |med| <= 0.03; LT |med E| <= 0.10")
for ft, a0 in A0S.items():
    lst = math.sqrt(ST[:, 2].max() * a0 / C ** 2 * XT[:, 2].min() * a0 / C ** 2); lst_r = lst * C ** 2 / a0
    TH = {"C1 s10": lambda r, v, f, a: 100 / (100 + v * v), "C1 s7": lambda r, v, f, a: 49 / (49 + v * v), "C1 s12": lambda r, v, f, a: 144 / (144 + v * v), "C1b s10": lambda r, v, f, a: 10 / np.sqrt(100 + v * v), "C0": lambda r, v, f, a: 0. * v, "C4": lambda r, v, f, a: (r > lst_r) * 1., "C5": lambda r, v, f, a: (f > .5) * 1., "unswitched": lambda r, v, f, a: 1. + 0 * v}
    def Afn(th, k): return lambda y, f, A: 1 + (th(A[:, 2], A[:, 5], f, a0) if A[:, 5].max() > 0 else (1. if True else 0)) * k * y * f
    kfit = minimize_scalar(lambda k: (resid(XT, a0, lambda y, f, A: 1 + k * y * f) ** 2).sum(), bounds=(0, 60), method="bounded", options=dict(xatol=1e-6)).x
    d0s = resid(SH, a0, lambda y, f, A: 1. + 0 * y); r0 = st(d0s)[1]; kk = {"pi2": PI2, "kfit": kfit}; R[ft] = dict(kfit=kfit, ell_star=lst, rows={}); dx0 = resid(X, a0, lambda y, f, A: 1. + 0 * y); law_p = pathfit(lambda r, v, f, a: 0. * v, a0, 0.)
    P(f"\n=== {ft}: k fit X-COP train {kfit:.3f} (pi^2 {PI2:.3f}); ell* {lst:.3e}; even SPARC law rms {r0:.3f} med {np.median(d0s):+.3f}; X-COP all law {st(dx0)[0]:+.3f},{st(dx0)[1]:.3f}; path law rms {law_p['rms']:.4f} U {law_p['U']:.2f}, FG1 {FG[ft]}; K6 {'PASS' if abs(law_p['rms']-FG[ft][0])<6e-4 and abs(law_p['U']-FG[ft][1])<.011 else 'FAIL'}; LT law {ltE(lambda r,v,f,a:0.*v,a0,0.):+.3f}")
    R[ft]["law"] = dict(sh=r0, path=law_p, K6=bool(abs(law_p['rms'] - FG[ft][0]) < 6e-4 and abs(law_p['U'] - FG[ft][1]) < .011))
    for kn, k0 in kk.items():
        k = k0 * (3 if MUT else 1)
        dxh = resid(XH, a0, lambda y, f, A: 1 + k * y * f); dxa = resid(X, a0, lambda y, f, A: 1 + k * y * f); dxt = resid(XT, a0, lambda y, f, A: 1 + k * y * f); xo = dict(train=st(dxt)[:2], hold=st(dxh)[:2], all=st(dxa)[:2], all_bracket=st(dxa - .12)[:2]); xp = abs(xo["hold"][0]) <= .05 and xo["hold"][1] <= .10; xpa = abs(xo["all"][0]) <= .05 and xo["all"][1] <= .10
        P(f"  [{kn} k {k:.3f}] X-COP train {xo['train'][0]:+.3f},{xo['train'][1]:.3f}; unseen {xo['hold'][0]:+.3f},{xo['hold'][1]:.3f} {'PASS' if xp else 'FAIL'}; all 7 {xo['all'][0]:+.3f},{xo['all'][1]:.3f} {'PASS' if xpa else 'FAIL'}; HSE-0.12 dex {xo['all_bracket'][0]:+.3f}")
        for n, th in TH.items():
            H = lambda y, f, A: 1 + th(A[:, 2], A[:, 5], f, a0) * k * y * f; d = resid(SH, a0, H); s_ok = st(d)[1] <= 1.05 * r0 and abs(st(d)[2]) <= .03; dt = resid(ST, a0, H); pf = pathfit(th, a0, k); le = ltE(th, a0, k); lp = abs(le) <= .10; lm = (SH[:, 7] > 0) & (SH[:, 7] < 60); dlaw = d0s[lm]; o = dict(even=st(d)[1:], even_pass=bool(s_ok), train=st(dt)[1:], lowV_d=float(np.median(d[lm]) - np.median(dlaw)), LT=le, LT_pass=bool(lp), path=pf, X_hold=bool(xp), X_all=bool(xpa)); o["disc_pass"] = bool(s_ok and lp); R[ft]["rows"][f"{n}|{kn}"] = o
            P(f"    {n:10s} even SPARC rms {o['even'][0]:.3f} med {o['even'][1]:+.3f} {'PASS' if s_ok else 'FAIL'} | train {o['train'][0]:.3f} | V<60 shift {o['lowV_d']:+.3f} | LT {le:+.3f} {'PASS' if lp else 'FAIL'} | path rms {pf['rms']:.4f} U {pf['U']:.2f} tilt {pf['tilt']:+.2f}")
if not MUT: json.dump({f: R[f]["kfit"] for f in A0S}, open("ux3_kfit.json", "w"))
json.dump(R, open(f"ux3_b{TAG}.json", "w"), indent=1, default=float); open(f"ux3_b{TAG}.out", "w").write("\n".join(OUT) + "\n")
