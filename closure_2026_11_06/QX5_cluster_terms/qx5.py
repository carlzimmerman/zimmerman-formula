#!/usr/bin/env python3
"""QX5 (criteria e3badba22f): new action terms keyed on a cluster-vs-galaxy variable.
    python3 qx5.py            # graded: qx5.json / qx5.out
    python3 qx5.py --mutate   # M1 / M2 power controls: qx5_MUTATE.json / .out
Phantom-multiplier form M = M_b + F(k)(M_law - M_b); monotone F by weighted isotonic regression (PAV).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv; TAG = "qx5_MUTATE" if MUT else "qx5"; OUT = []
GCUT_ENV = os.environ.get("QX5_GCUT")  # reported variant only (iter a file): 0.01
if GCUT_ENV: TAG += "_gcut" + GCUT_ENV.replace(".", "")
def P(s): print(s, flush=True); OUT.append(s)

G, MS, PC, C = 6.674e-11, 1.989e30, 3.0857e16, 2.99792458e8
KPC = 1e3 * PC; MP = 1.6726e-27; KEV = 1.602e-16; MU = 0.6
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}
KAPPA = 0.5; XS = (0.1, 0.2, 0.3, 0.5, 0.7); GCUT = float(GCUT_ENV) if GCUT_ENV else 0.03
def rho_de(a0): return a0 ** 2 / (KAPPA ** 2 * C ** 2 * G)
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * gN)
def li(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))

def tail_phi(Mb_kg, r0, a0, gcut=GCUT):
    """Int_{r0}^{rcut} g_law(G Mb/r^2) dr, rcut where g_law = gcut a0."""
    if Mb_kg <= 0: return 0.0
    f = lambda r: glaw(G * Mb_kg / r ** 2, a0) - gcut * a0
    if f(r0) <= 0: return 0.0
    lo, hi = math.log(r0), math.log(r0) + 1
    while f(math.exp(hi)) > 0: hi += 1
    for _ in range(60):
        m = 0.5 * (lo + hi); lo, hi = (m, hi) if f(math.exp(m)) > 0 else (lo, m)
    rr = np.geomspace(r0, math.exp(hi), 2000); g = glaw(G * Mb_kg / rr ** 2, a0)
    return float(np.trapz(g, rr))

_TC = {}
def phi_from(r_m, g, i, Mb_last, a0):  # data integral from r_i to last + tail (tail cached)
    key = (float(Mb_last), float(r_m[-1]), a0)
    if key not in _TC: _TC[key] = tail_phi(Mb_last, r_m[-1], a0)
    return (float(np.trapz(g[i:], r_m[i:])) if i < len(r_m) - 1 else 0.0) + _TC[key]

# ---------------- samples ----------------
def xcop():
    out = []
    for name in sorted(os.listdir(os.path.join(DATA, "xcop"))):
        p_ = os.path.join(DATA, "xcop", name)
        if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))): continue
        with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]
        with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        hr = np.array(hm["RADIUS"], float); hM = np.array(hm["M_FORW"], float)
        gr = np.array(gas["RADIUS"], float) * rg500; gM = np.array(gas["MGAS"], float)
        sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float)
        Mb_last = None
        for t in hr[::-1]:
            mg, ms = li(gr, gM, t), li(sr, sM, t)
            if np.isfinite(mg) and np.isfinite(ms): Mb_last = (mg + ms, t); break
        for x in XS:
            r = x * r500; mh = li(hr, hM, r); mg = li(gr, gM, r); ms = li(sr, sM, r); em = li(hr, np.array(hm["EM_FORW"], float), r)
            if np.all(np.isfinite([mh, mg, ms])):
                out.append(dict(name=name, r_kpc=r, M_obs=mh, M_b=mg + ms, M_gas=mg, eM=em, hr=hr, hM=hM, Mb_last=Mb_last))
    return out

def sparc():
    Q, INC = {}, {}
    for ln in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        t = ln.split()
        if len(t) < 18: continue
        try: nm = t[0]; inc = float(t[5]); q = int(t[17])
        except ValueError: continue
        Q[nm] = q; INC[nm] = inc
    gals = []
    for fn in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
        if not fn.endswith("_rotmod.dat"): continue
        nm = fn[:-11]
        if nm not in Q or Q[nm] > 2 or INC[nm] < 30: continue
        a = np.loadtxt(os.path.join(DATA, "sparc_data", fn), comments="#")
        if a.ndim == 1: a = a[None]
        R, V, eV, Vg, Vd, Vb = a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5]
        vg2 = np.sign(Vg) * Vg ** 2; vd2 = 0.5 * np.sign(Vd) * Vd ** 2; vbu2 = 0.7 * np.sign(Vb) * Vb ** 2
        vb2 = vg2 + vd2 + vbu2
        ok = (V > 0) & (eV / np.maximum(V, 1e-9) <= 0.1) & (vb2 > 0) & (R > 0)
        if ok.sum() < 2: continue
        gals.append(dict(name=nm, R=R[ok] * KPC, V=V[ok] * 1e3, eV=eV[ok] * 1e3, vg2=vg2[ok] * 1e6, vd2=vd2[ok] * 1e6, vbu2=vbu2[ok] * 1e6, vb2=vb2[ok] * 1e6))
    return gals

def ellipticals():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
    hdr, rows = rows[0], rows[1:]; E = []
    for r in rows:
        d = dict(zip(hdr, r)); LK = float(d["LK_1e11"]) * 1e11; Re = float(d["Re_kpc"]); Mv = float(d["Mvir_1e12"]) * 1e12
        Rv = float(d["Rvir_kpc"]); c = float(d["c"]); Mfit = float(d["ups_fit"]) * LK; Mkr = float(d["ups_krou"]) * LK
        a = Re / 1.8153; rs = Rv / c; Mh = Mv - Mfit; mc = math.log(1 + c) - c / (1 + c)
        # QX16 fix (criteria 7de1a2733f): bind per-row values via default args; before this, Python late binding gave
        # all 7 ellipticals the LAST row's mass model (original outputs kept on record; reruns in QX16 as *_FIXED).
        Mtot = lambda r, Mh=Mh, rs=rs, mc=mc, Mfit=Mfit, a=a: Mh * (math.log(1 + r / rs) - (r / rs) / (1 + r / rs)) / mc + Mfit * r ** 2 / (r + a) ** 2
        Mbar = lambda r, Mkr=Mkr, a=a: Mkr * r ** 2 / (r + a) ** 2
        E.append(dict(name=d["name"], Re=Re, Mtot=Mtot, Mbar=Mbar))
    return E

def lensing():
    mids = [9.4, 10.45, 10.7, 10.9]; Gpc = 4.52e-30; L = []
    for i, lm in enumerate(mids, 1):
        a = np.loadtxt(os.path.join(DATA, "lensing_rar", "brouwer2021_rar", f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt"), comments="#")
        gbar = a[:, 0]; gobs = 4 * Gpc * a[:, 1] / a[:, 4] * PC; err = 4 * Gpc * a[:, 3] / a[:, 4] * PC
        for gb, go, e in zip(gbar, gobs, err):
            if go > 0: L.append(dict(gbar=gb, gobs=go, err=e, Mb=10 ** lm * MS))
    return L

def groups():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "lovisari2015_groups.tsv")) if not l.startswith("#")]
    hdr, rows = rows[0], rows[1:]; out = []
    for r in rows:
        d = dict(zip(hdr, r)); kT = float(d["kT_keV"])
        R5, R25 = float(d["R500_kpc"]), float(d["R2500_kpc"]); M5, M25 = float(d["M500_1e13"]) * 1e13, float(d["M2500_1e13"]) * 1e13
        g5, g25 = float(d["Mgas500_1e12"]) * 1e12, float(d["Mgas2500_1e12"]) * 1e12
        out.append(dict(name=d["name"], kT=kT, pts=[dict(r_kpc=R25, M_obs=M25, M_gas=g25, eM=float(d["eM2500"]) * 1e13),
                                                      dict(r_kpc=R5, M_obs=M5, M_gas=g5, eM=float(d["eM500"]) * 1e13)], R5=R5, R25=R25, M5=M5, M25=M25, g5=g5))
    return out

XC, SP, EL, LE, GR = xcop(), sparc(), ellipticals(), lensing(), groups()
P(f"QX5 {TAG}: X-COP {len(XC)} pts; SPARC {len(SP)} galaxies, {sum(len(g['R']) for g in SP)} pts; ellipticals {len(EL)}; lensing {len(LE)} pts; groups {len(GR)}")

def pav(x, y, w, increasing=True):
    o = np.argsort(x if increasing else -x, kind="mergesort"); xs, ys, ws = x[o], y[o], w[o]
    blocks = []  # [sum wy, sum w, count]
    for yi, wi in zip(ys, ws):
        blocks.append([wi * yi, wi, 1])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            b = blocks.pop(); blocks[-1][0] += b[0]; blocks[-1][1] += b[1]; blocks[-1][2] += b[2]
    fit = np.concatenate([[b[0] / b[1]] * b[2] for b in blocks]); fit = np.maximum(fit, 0.0)
    kx = xs if increasing else -xs  # back to key order for interpolation
    ordk = np.argsort(kx); return kx[ordk], fit[ordk]
def predict(model, k):
    kx, f = model; return np.interp(k, kx, f)

# ---------------- build per-class point tables ----------------
def tables(cls, a0, mut):
    rde = rho_de(a0); T = dict(C=[], X=[], S=[], E=[], L=[], G=[])
    # SPARC
    for g in SP:
        r, V = g["R"], g["V"]; gobs = V ** 2 / r; gbar = g["vb2"] / r; gl = glaw(gbar, a0)
        Mb_last = g["vb2"][-1] * r[-1] / G
        for i in range(len(r)):
            if cls == "a": k = phi_from(r, gobs, i, Mb_last, a0) / C ** 2
            elif cls == "b":
                ms = np.array([max(g["vg2"][i], 0), max(g["vd2"][i], 0), max(g["vbu2"][i], 0)])
                ks = np.array([(1e4 / C) ** 2, (0.2 * V[i] / C) ** 2, V[i] ** 2 / (2 * C ** 2)]); k = float((ms * ks).sum() / ms.sum())
            elif cls == "d": k = 3 * (g["vb2"][i] * r[i] / G) / (4 * math.pi * r[i] ** 3 * rde)
            elif cls == "e": k = G * max(g["vg2"][i] * r[i] / G, 0) / r[i] ** 2 / a0
            row = dict(k=k, gobs=gobs[i], gbar=gbar[i], gl=gl[i])
            T["S"].append(row)
            if (gl[i] - gbar[i]) / gl[i] >= 0.3:
                Fi = (gobs[i] - gbar[i]) / (gl[i] - gbar[i]); sg = gobs[i] * math.hypot(2 * g["eV"][i] / V[i], 0.125)
                T["C"].append(dict(k=k, F=Fi, s=sg / (gl[i] - gbar[i]), src="S"))
    # ellipticals
    for e in EL:
        rl = 8 * e["Re"] * KPC; rg = np.linspace(2 * e["Re"], 8 * e["Re"], 400) * KPC
        gt = np.array([G * e["Mtot"](x / KPC) * MS / x ** 2 for x in rg])
        for m in (2, 4, 8):
            r = m * e["Re"]; rm = r * KPC; Mb = e["Mbar"](r); Mo = e["Mtot"](r)
            gN = G * Mb * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS
            if mut and cls == "a": Mo = Mb + 2.8 * (Ml - Mb)
            i = int(np.argmin(abs(rg - rm)))
            if cls == "a": k = phi_from(rg, gt, i, e["Mbar"](8 * e["Re"]) * MS, a0) / C ** 2
            elif cls == "b": k = G * Mo * MS / rm / (2 * C ** 2)
            elif cls == "d": k = 3 * Mb * MS / (4 * math.pi * rm ** 3 * rde)
            elif cls == "e": k = 0.0
            Fi = (Mo - Mb) / (Ml - Mb); s = Mb * (10 ** 0.15 - 1) / (Ml - Mb) * max(1.0, abs(Fi))
            row = dict(k=k, M_obs=Mo, M_b=Mb, M_law=Ml); T["E"].append(row); T["C"].append(dict(k=k, F=Fi, s=max(s, 0.05), src="E"))
    # lensing (a, d only)
    if cls in ("a", "d"):
        for p in LE:
            r = math.sqrt(G * p["Mb"] / p["gbar"]); gl = glaw(p["gbar"], a0)
            k = tail_phi(p["Mb"], r, a0) / C ** 2 if cls == "a" else 3 * p["Mb"] / (4 * math.pi * r ** 3 * rde)
            T["L"].append(dict(k=k, gobs=p["gobs"], gbar=p["gbar"], gl=gl))
            T["C"].append(dict(k=k, F=(p["gobs"] - p["gbar"]) / (gl - p["gbar"]), s=p["err"] / (gl - p["gbar"]), src="L"))
    # X-COP
    for z in XC:
        rm = z["r_kpc"] * KPC; gN = G * z["M_b"] * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS
        hr = z["hr"] * KPC; gh = G * z["hM"] * MS / hr ** 2; i = int(np.searchsorted(hr, rm))
        if cls == "a":
            k = (float(np.trapz(np.concatenate([[G * z["M_obs"] * MS / rm ** 2], gh[i:]]), np.concatenate([[rm], hr[i:]])))
                 + tail_phi(z["Mb_last"][0] * MS, z["Mb_last"][1] * KPC, a0)) / C ** 2
        elif cls == "b": k = G * z["M_obs"] * MS / rm / (2 * C ** 2)
        elif cls == "d": k = 3 * z["M_b"] * MS / (4 * math.pi * rm ** 3 * rde)
        elif cls == "e": k = G * z["M_gas"] * MS / rm ** 2 / a0
        Mo = z["M_obs"]
        T["X"].append(dict(k=k, M_obs=Mo, M_b=z["M_b"], M_law=Ml, eM=z["eM"]))
    # groups: two stellar allowances
    for gp in GR:
        sl = math.log(gp["M5"] / gp["M25"]) / math.log(gp["R5"] / gp["R25"])
        for j, p in enumerate(gp["pts"]):
            rm = p["r_kpc"] * KPC
            if cls == "a":
                rr = np.linspace(p["r_kpc"], gp["R5"], 200) * KPC; Mr = gp["M25"] * (rr / (gp["R25"] * KPC)) ** sl
                k = ((float(np.trapz(G * Mr * MS / rr ** 2, rr)) if j == 0 else 0.0) + tail_phi(gp["g5"] * MS, gp["R5"] * KPC, a0)) / C ** 2
            elif cls == "b": k = gp["kT"] * KEV / (MU * MP * C ** 2)
            elif cls == "d": k = 3 * p["M_gas"] * MS / (4 * math.pi * rm ** 3 * rde)
            elif cls == "e": k = G * p["M_gas"] * MS / rm ** 2 / a0
            for fst in (0.0, 1.0):
                Mb = p["M_gas"] * (1 + fst); gN = G * Mb * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS
                T["G"].append(dict(k=k, M_obs=p["M_obs"], M_b=Mb, M_law=Ml, fst=fst, vc2half=G * p["M_obs"] * MS / rm / 2, kT=gp["kT"]))
    if mut and cls == "a":  # M1: planted X-COP
        kmaxC = max(c["k"] for c in T["C"])
        for x in T["X"]:
            Ft = 2.8 if x["k"] > kmaxC else 1.0; x["M_obs"] = x["M_b"] + Ft * (x["M_law"] - x["M_b"])
    return T

def stats(T, model):
    F = (lambda k: np.ones_like(np.asarray(k, float))) if model is None else (lambda k: predict(model, np.asarray(k, float)))
    xd = np.array([math.log10(x["M_obs"] / (x["M_b"] + F(x["k"]) * (x["M_law"] - x["M_b"]))) for x in T["X"]])
    sd = np.array([math.log10(s["gobs"] / (s["gbar"] + F(s["k"]) * (s["gl"] - s["gbar"]))) for s in T["S"]])
    ed = np.array([math.log10(e["M_obs"] / (e["M_b"] + F(e["k"]) * (e["M_law"] - e["M_b"]))) for e in T["E"]])
    ld = np.array([math.log10(l["gobs"] / (l["gbar"] + F(l["k"]) * (l["gl"] - l["gbar"]))) for l in T["L"]]) if T["L"] else np.array([0.0])
    gm = {}
    for fst in (0.0, 1.0):
        v = np.array([math.log10(g["M_obs"] / (g["M_b"] + F(g["k"]) * (g["M_law"] - g["M_b"]))) for g in T["G"] if g["fst"] == fst]); gm[fst] = float(v.mean())
    return dict(X_mean=float(xd.mean()), X_rms=float(np.sqrt((xd ** 2).mean())), S_mean=float(sd.mean()), S_rms=float(np.sqrt((sd ** 2).mean())),
                E_mean=float(ed.mean()), L_mean=float(ld.mean()), G_mean_star0=gm[0.0], G_mean_star1=gm[1.0])

def fit(rows, inc):
    k = np.array([r["k"] for r in rows]); F = np.array([r["F"] for r in rows]); w = 1 / np.array([r["s"] for r in rows]) ** 2
    return pav(k, F, w, inc)

DIR = dict(a=True, b=True, d=False, e=True)
RES = dict(tag=TAG, note="kappa = 1/2 FITTED; not theory closed")
classes = ["a"] if (MUT or GCUT_ENV) else ["a", "b", "d", "e"]
for cls in classes:
    RES[cls] = {}
    for f, a0 in A0.items():
        T = tables(cls, a0, MUT); inc = DIR[cls]
        base = stats(T, None)
        mP = fit(T["C"], inc); sP = stats(T, mP)
        Xrows = [dict(k=x["k"], F=(x["M_obs"] - x["M_b"]) / (x["M_law"] - x["M_b"]), s=x["eM"] / (x["M_law"] - x["M_b"])) for x in T["X"]]
        mK = fit(T["C"] + Xrows, inc); sK = stats(T, mK)
        rng = lambda L_: (float(min(r["k"] for r in L_)), float(max(r["k"] for r in L_))) if L_ else None
        keys = dict(SPARC=rng([c for c in T["C"] if c["src"] == "S"]), ellipticals=rng(T["E"]), lensing=rng(T["L"]), XCOP=rng(T["X"]), groups=rng(T["G"]))
        Freq = [r["F"] for r in Xrows]
        def recheck(s):
            return dict(SPARC=bool(s["S_rms"] - base["S_rms"] <= 0.01 and abs(s["S_mean"] - base["S_mean"]) <= 0.02),
                        ellipticals=bool(abs(s["E_mean"] - base["E_mean"]) <= 0.15), lensing=bool(abs(s["L_mean"] - base["L_mean"]) <= 0.05))
        def gx(s): return bool(abs(s["X_mean"]) <= 0.05 and s["X_rms"] <= 0.10)
        def gg(s): lo, hi = sorted([s["G_mean_star0"], s["G_mean_star1"]]); return bool(lo <= 0.05 and hi >= -0.05)
        rP, rK = recheck(sP), recheck(sK)
        passP = gx(sP) and gg(sP) and all(rP.values())
        if passP: lab = "PASS"
        elif not gx(sK) or not all(rK.values()): lab = "DEAD"
        elif not gg(sK): lab = "DEAD-BY-GROUPS"
        else: lab = "CLUSTER-SET"
        gchk = None
        if cls == "b":
            gchk = float(np.median([g["kT"] * KEV / MU / MP / g["vc2half"] for g in T["G"] if g["fst"] == 0.0]))
        RES[cls][f] = dict(label=lab, base=base, P=sP, K=sK, recheck_P=rP, recheck_K=rK, keys=keys,
                           XCOP_F_required=dict(median=float(np.median(Freq)), min=float(min(Freq)), max=float(max(Freq)),
                                                rms_logF_about_median=float(np.sqrt(np.mean((np.log10(np.maximum(Freq, 1e-3)) - math.log10(np.median(Freq))) ** 2)))),
                           F_pred_P_at_XCOP=dict(min=float(predict(mP, np.array([x["k"] for x in T["X"]])).min()), max=float(predict(mP, np.array([x["k"] for x in T["X"]])).max())),
                           kT_over_vc2half_groups=gchk)
        r = RES[cls][f]
        P(f"[{cls}|{f}] keys: " + ", ".join(f"{n} {v[0]:.3g}-{v[1]:.3g}" for n, v in keys.items() if v))
        P(f"   base (F=1): X {base['X_mean']:+.3f}/{base['X_rms']:.3f}; SPARC {base['S_mean']:+.3f}/{base['S_rms']:.3f}; E {base['E_mean']:+.3f}; L {base['L_mean']:+.3f}; groups [{base['G_mean_star1']:+.3f},{base['G_mean_star0']:+.3f}]")
        P(f"   P (calibrated on C only): X {sP['X_mean']:+.3f}/{sP['X_rms']:.3f} (F_pred {r['F_pred_P_at_XCOP']['min']:.2f}-{r['F_pred_P_at_XCOP']['max']:.2f}); SPARC {sP['S_mean']:+.3f}/{sP['S_rms']:.3f}; groups [{sP['G_mean_star1']:+.3f},{sP['G_mean_star0']:+.3f}]; rechecks {rP}")
        P(f"   K (C + X-COP):            X {sK['X_mean']:+.3f}/{sK['X_rms']:.3f}; SPARC {sK['S_mean']:+.3f}/{sK['S_rms']:.3f}; E {sK['E_mean']:+.3f}; L {sK['L_mean']:+.3f}; groups [{sK['G_mean_star1']:+.3f},{sK['G_mean_star0']:+.3f}]; rechecks {rK}")
        P(f"   X-COP F required: median {r['XCOP_F_required']['median']:.2f} [{r['XCOP_F_required']['min']:.2f}, {r['XCOP_F_required']['max']:.2f}], rms log F {r['XCOP_F_required']['rms_logF_about_median']:.3f}" + (f"; groups kT/(mu m_p) over V_c^2/2 median {gchk:.2f}" if gchk else ""))
        P(f"   LABEL [{cls}|{f}]: {lab}")
        if MUT:
            P(f"   M1 (planted X-COP, K must pass G-X): K X {sK['X_mean']:+.3f}/{sK['X_rms']:.3f} -> {'BITES' if gx(sK) else 'NO BITE'}")
            P(f"   M2 (ellipticals F=2.8, P must move X-COP mean <= -0.2 vs F=1): move {sP['X_mean'] - base['X_mean']:+.3f} -> {'BITES' if sP['X_mean'] - base['X_mean'] <= -0.2 else 'NO BITE'}")
            RES[cls][f]["M1_bites"] = gx(sK); RES[cls][f]["M2_bites"] = bool(sP["X_mean"] - base["X_mean"] <= -0.2)
P("[c] khronon bulk velocity: analytic (iter_c file); LG 627 km/s vs CMB vs cluster kSZ peculiar velocities of a few hundred km/s: no window -> DEAD on provisional literature inputs; readings 1/2 = classes a/b")
json.dump(RES, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
