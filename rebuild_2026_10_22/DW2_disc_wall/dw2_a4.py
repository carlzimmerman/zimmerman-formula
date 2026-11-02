#!/usr/bin/env python3
"""DW2 A4: absent (LAW + cold) vs term off (OFF, MAX). Per-galaxy U path, slope, LT, X-COP, UL1 Z, budget, scatter. kappa = 1/2 FITTED; not theory closed."""
import sys
from dw2_core import *
from astropy.io import fits
OUT = []; RES = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
GAL = load(); BY = [[g for g in GAL if binof(g) == i] for i in range(6)]; ULO = np.round(np.arange(.05, 1.2000001, .01), 2)
PAIR = {(g["name"], m): cold_pair(g, 0.5, m) for g in GAL for m in ("em1", "share")}
def gc_of(g, mass, f): a, b = PAIR[(g["name"], mass)]; return a + f * (b - a)
def pred(form, gb, gc, a0):
    if form == "LAW": return law(gb, a0)
    if form == "N": return law(gb, a0) + gc
    if form == "OFF": return gb + gc
    if form == "MAX": return np.maximum(law(gb, a0), gb + gc)
EST = json.load(open(os.path.join(RB, "UL1_measured_upsilon_test", "ul1_est.json")))["primary"]
def path(form, mass, f, a0):
    W2 = WS = 0.0; Yb, Vf, TOT, br = [], [], [], {}
    for g in GAL:
        gO = g["V"] ** 2 * KMS2 / g["R"]; gc = gc_of(g, mass, f); W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["V"], 1)) ** 2; A = []; B = []
        for U in ULO:
            gb = gbar(g, float(U)); ok = (gb > 0) & (gO > 0) & (g["V"] > 0); p = pred(form, np.maximum(gb, 1e-30), gc, a0); r = np.where(ok, np.log10(np.where(gO > 0, gO, 1.) / p), 0.); A.append(float((W * r * r * ok).sum())); B.append(float((W * ok).sum()))
        A = np.array(A); B = np.array(B); q = np.where(B > 0, A / np.where(B > 0, B, 1), np.inf); i = int(np.argmin(q)); W2 += A[i]; WS += B[i]; Yb.append(ULO[i]); Vf.append(g["Vflat"]); TOT.append(g["TOT"])
        gb = np.maximum(gbar(g, float(ULO[i])), 1e-30); br.setdefault(binof(g), []).append(float(np.mean((gb + gc) > law(gb, a0))))
    Yb, Vf, TOT = np.array(Yb), np.array(Vf), np.array(TOT); lo = (Vf > 0) & (Vf < 100); hi = Vf > 150; by = [float(np.median(Yb[(Vf >= a) & (Vf < b)])) for a, b in BINS]; byT = [float(np.median((Yb * TOT)[(Vf >= a) & (Vf < b)])) for a, b in BINS]
    # bootstrap tilt
    r_ = np.random.default_rng(20261102); bt = [float(np.median(Yb[lo][r_.integers(0, lo.sum(), lo.sum())]) - np.median(Yb[hi][r_.integers(0, hi.sum(), hi.sum())])) for _ in range(2000)]
    Z = {}
    for x in ("GSWLC", "Taylor"):
        ms = np.log10(byT[1:]); mu = np.log10([EST[b][x]["mu"] for b in BN[1:]]); h = np.array([math.sqrt((1.25 * EST[b][x]["sig"] / math.sqrt(len(BY[i + 1]))) ** 2 + 0.04 ** 2) for i, b in enumerate(BN[1:])]); dd = ms - mu; st = (np.diff(ms) - np.diff(mu)) / np.sqrt(h[:-1] ** 2 + h[1:] ** 2); Z[x] = dict(Z=(dd / h).tolist(), steps=st.tolist())
    return dict(rms=math.sqrt(W2 / WS), U=float(np.median(Yb)), byU=by, tilt=float(np.median(Yb[lo]) - np.median(Yb[hi])), tilt_s=float(np.std(bt)), branch=[float(np.mean(br.get(i, [0]))) for i in range(6)], Z=Z, floor=float(np.mean(Yb <= ULO[0])))
SBT = None
def slope_A4(form, mass, f, a0, U=0.5):
    X, Y = [], []
    for g in GAL:
        if not (60 <= g["Vflat"] < 120) or g["SB"] <= 0: continue
        gb = gbar(g, U); ok = (gb > 0) & (g["V"] > 0); Rk = g["R"] / KPC; R2 = 2 * g["Rd"]
        if ok.sum() < 2 or R2 < Rk[ok].min() or R2 > Rk[ok].max(): continue
        Vm = np.sqrt(np.maximum(pred(form, np.maximum(gb, 1e-30), gc_of(g, mass, f), a0) * g["R"], 0)) / 1e3; Y.append(float(np.interp(math.log(R2), np.log(Rk[ok]), Vm[ok] / g["V"][ok] - 1))); X.append(math.log10(g["SB"]))
    X, Y = np.array(X), np.array(Y); sl = lambda x, y: float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()); r = np.random.default_rng(1); b = []
    for _ in range(2000):
        k = r.integers(0, len(X), len(X)); b.append(sl(X[k], Y[k]))
    return dict(n=len(X), b=sl(X, Y), s=float((np.percentile(b, 84) - np.percentile(b, 16)) / 2))
LT = []
for r in csv.DictReader(open(os.path.join(INP, "little_things", "oh2015_table2.csv"))):
    if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun")): LT.append((float(r["Rmax_kpc"]) * KPC, float(r["V_kms"]), float(r["Mgas_1e7Msun"]) * 1e7, float(r["MSED_1e7Msun"]) * 1e7))
LT = np.array(LT)
def lt_E(form, mass, a0):
    R, V, g_, s = LT.T; gb = G * (g_ + s) * MS / R ** 2; gO = V ** 2 * KMS2 / R; gc = np.array([G * float(Mc_native(em1(math.log10(m)) if mass == "em1" else share200(m), r_)) * MS / r_ ** 2 for r_, m in zip(R, g_ + s)]); return boot_med(np.log10(gO / pred(form, gb, gc, a0)))
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
XC = []; DX = os.path.join(REPO, "real_research", "data", "xcop"); XS = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
for n in sorted(os.listdir(DX)):
    p_ = os.path.join(DX, n)
    if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{n}_mstar.fits"))): continue
    with fits.open(os.path.join(p_, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
    row = {x: (x * r5, li(hm["RADIUS"], hm["M_FORW"], x * r5), li(ga["RADIUS"] * rg5, ga["MGAS"], x * r5), li(st["RADIUS"], st["MSTAR"], x * r5)) for x in XS}; XC.append(row)
def xcop(form, a0):
    """M200 solved so the native total shape holds M_HSE at R500; cold share FC of it. A generous mapping: mass tied to the data."""
    L = []
    for row in XC:
        if 1.0 not in row or not np.isfinite(row[1.0][1]): continue
        r5k, m5, _, _ = row[1.0]; lo, hi = m5, 5 * m5
        for _ in range(30):
            c = math.sqrt(lo * hi); R = r200(c) / KPC; v = c * float(np.exp(np.interp(np.log(min(r5k / R, 1)), LX, lnm(math.log10(c))))); lo, hi = (c, hi) if v < m5 else (lo, c)
        M200 = c
        for x, (r, mh, mg, ms) in row.items():
            if not np.isfinite(mh + mg + ms): continue
            Rm = r * KPC; gb = G * (mg + ms) * MS / Rm ** 2; gc = G * float(Mc_native(M200, Rm)) * MS / Rm ** 2; L.append((x, math.log10((G * mh * MS / Rm ** 2) / float(pred(form, gb, gc, a0)))))
    L = np.array(L); return dict(mean=float(L[:, 1].mean()), rms=float(np.sqrt((L[:, 1] ** 2).mean())), byx={str(x): float(L[L[:, 0] == x, 1].mean()) for x in XS})
RES["footings"] = {}
for ft in FEET:
    a0 = A0[ft]; R = {}; P(f"\n===== {ft}")
    rows = [("LAW", "em1", 0.0)] + [(fm, m, f) for fm in ("N", "OFF", "MAX") for m in ("em1", "share") for f in (0.0, FQ)]
    for fm, m, f in rows:
        k = f"{fm}|{m}|f{f}"; q = path(fm, m, f, a0); s_ = slope_A4(fm, m, f, a0); e = lt_E(fm, m, a0); xc = xcop(fm, a0) if fm != "LAW" else xcop("LAW", a0)
        dfix = []
        for gs in BY:
            dfix.append(float(np.median([np.mean(np.log10((g["V"] ** 2 * KMS2 / g["R"]) / pred(fm, np.maximum(gbar(g, .5), 1e-30), gc_of(g, m, f), a0))[outer(g)]) for g in gs])))
        R[k] = dict(path=q, slope=s_, LT=e, xcop=xc, d_fixed=dfix)
        P(f"{k:18s} rms {q['rms']:.4f} U {q['U']:.2f} byV " + " ".join(f"{u:.2f}" for u in q['byU']) + f" tilt {q['tilt']:+.2f}+-{q['tilt_s']:.2f} floor {q['floor']:.2f} | b {s_['b']:+.3f}+-{s_['s']:.3f} (n {s_['n']}, Z {s_['b'] / s_['s']:+.1f}) | LT {e[0]:+.3f}+-{e[1]:.3f} | X-COP {xc['mean']:+.3f} rms {xc['rms']:.3f}")
        P(f"    cold branch by bin " + " ".join(f"{a:.2f}" for a in q['branch']) + " | d at U .5 " + " ".join(f"{a:+.3f}" for a in dfix) + " | Z GSWLC " + " ".join(f"{a:+.1f}" for a in q['Z']['GSWLC']['Z']) + " steps " + " ".join(f"{a:+.1f}" for a in q['Z']['GSWLC']['steps']) + " | Z Taylor " + " ".join(f"{a:+.1f}" for a in q['Z']['Taylor']['Z']))
    # budget, scatter
    P("-- Budget: Gamma_off at outer third, U .5, median +- boot; native M_c/M_b at R_last, EM1 and share")
    R["budget"] = {}
    for i, gs in enumerate(BY):
        Go = []; Ge = []; Gs = []
        for g in gs:
            m = outer(g); gb = np.maximum(gbar(g, .5), 1e-30); gO = g["V"] ** 2 * KMS2 / g["R"]; Go.append(float(np.mean(((gO - gb) / gb)[m]))); Ge.append(float(np.mean((gc_of(g, "em1", 0.) / gb)[m]))); Gs.append(float(np.mean((gc_of(g, "share", 0.) / gb)[m])))
        a, b = boot_med(Go); R["budget"][BN[i]] = dict(Goff=(a, b), em1=float(np.median(Ge)), share=float(np.median(Gs))); P(f"   {BN[i]:8s} Gamma_off {a:.2f}+-{b:.2f}  native EM1 {np.median(Ge):.2f}  share {np.median(Gs):.2f}  need/share-native {a / np.median(Gs):.2f}  need/EM1 {a / np.median(Ge):.2f}")
    sc = {}
    for m in ("em1", "share"):
        x = []; xm = []
        for g in GAL:
            gb = gbar(g, .5); gO = g["V"] ** 2 * KMS2 / g["R"]; need = gO - gb; ok = (need > 0) & (g["V"] > 0); v = np.log10(need[ok] / gc_of(g, m, 0.)[ok]); x.extend(v.tolist()); xm.append(float(np.mean(v))) if ok.any() else None
        sc[m] = dict(rms=float(np.std(x)), rms_gal=float(np.std(xm)), mean=float(np.mean(x)))
    lr = np.concatenate([np.log10((g["V"] ** 2 * KMS2 / g["R"])[(gbar(g, .5) > 0) & (g["V"] > 0)] / law(gbar(g, .5)[(gbar(g, .5) > 0) & (g["V"] > 0)], a0)) for g in GAL]); sc["law_rms"] = float(np.std(lr)); R["scatter"] = sc; P(f"-- Scatter: log(g_c needed / native), per point, per-galaxy means: {sc}")
    RES["footings"][ft] = R
json.dump(RES, open(os.path.join(HERE, f"dw2_a4_results{TAG}.json"), "w"), indent=1, default=float, sort_keys=True); open(os.path.join(HERE, f"dw2_a4{TAG}.out"), "w").write("\n".join(OUT) + "\n")
