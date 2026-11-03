#!/usr/bin/env python3
"""WA1 rows: RQ3's row functions under shared shifts. Nuisances enter as a wrapper on the candidate's Q and as patches on the loaders, or in small copies of B1, B2, X-COP, A30 that expose the terms RQ3 folds together. At no shift they must reproduce RQ3 (check K0). kappa = 1/2 FITTED; not theory closed."""
import copy, csv, math, os, sys
from wa1_common import *
A = load_acc(); A.crg(); import crg1_sparc as CS, crg1_lens as Le, crg1_groups as Gr
_G0, _L0, _R0 = CS.load_gal, CS.load_lt, Gr.load
class Wrap:
    """Shifts the baryons a candidate sees. sample tells the system; the disc FIT path (2D gb) is left alone, since free Upsilon absorbs ups."""
    GASS = ("xgroup", "cluster")
    def __init__(s, c, u=0.0, gabs=0.0): s.c, s.u, s.ga = c, u, gabs; s.NAME = getattr(c, "NAME", ""); s.VERTICAL = getattr(c, "VERTICAL", ()); 
    def g(s, Q):
        Q2 = dict(Q); sm = Q2.get("sample"); gb = np.asarray(Q2["gb"], float); fu = 10 ** s.u; fg = 10 ** s.ga if sm in s.GASS else 1.0
        if sm in ("planet", "MW", "merger", "probe", "deep") or (sm == "disc" and gb.ndim > 1) or (fu == 1.0 and fg == 1.0): return s.c.g(A.Q(**Q2))
        gg = np.asarray(Q2.get("gg", np.nan), float)
        if np.all(np.isnan(gg)): Q2["gb"] = gb * fu
        else:
            gs = gb - gg; Q2["gg"] = gg * fg; Q2["gs"] = gs * fu; Q2["gb"] = gs * fu + gg * fg
        return s.c.g(A.Q(**Q2))
def set_dist(dl):
    e = math.exp(dl)
    def lg():
        o = []
        for g in _G0():
            g = dict(g); g["R"] = g["R"] * e; f = math.sqrt(e)
            for k in ("Vgas", "Vdisk", "Vbul"): g[k] = g[k] * f
            for k in ("L36", "MHI"): g[k] = g[k] * e * e
            g["lgMb"] = g["lgMb"] + 2 * dl / math.log(10); o.append(g)
        return o
    def ll():
        return [dict(x, R=x["R"] * e, Mb=x["Mb"] * e * e, lg=x["lg"] + 2 * dl / math.log(10)) for x in _L0()]
    def gr(): return [(x[0] + 2 * dl / math.log(10), x[1], x[2] * e) for x in _R0()]
    CS.load_gal = lg if dl else _G0; CS.load_lt = ll if dl else _L0; Gr.load = gr if dl else _R0
_LC = {}
def lens_tab(w, foot, key):
    if not _LC.get("L"):
        L = Le.load(); st = Le.Stencil(L["Rn"] * 1e6); TH = Le.TwoHalo(L); rex = [.343, .442, .433, .429]; _LC.update(L=L, st=st, T0=np.array([TH.esd2h(L["R"][b], rex[b]) * Le.FF for b in range(4)]))
    k = (key, foot, w.u)
    if k not in _LC:
        L, st = _LC["L"], _LC["st"]; SIk = 1e6 / 3.0857e16; Tb = np.zeros((len(Le.LMG), 60)); a0 = A.A0[foot]
        for i, lm in enumerate(Le.LMG):
            MB, Mbm = Le.baryon(float(lm)); gb = Le.Gpc * MB / Le.RGRID ** 2; gg = Le.Gpc * (MB - 10 ** float(lm)) / Le.RGRID ** 2; v = A.call(w, gb=gb * SIk, gg=gg * SIk, gs=(gb - gg) * SIk, r=Le.RGRID * 3.0857e16, a0=a0, sample="lens"); Tb[i] = st.dsig(MB * v / (gb * SIk), "linear")
        _LC[k] = Le.stack(L, Tb)
    return _LC[k]
def row_lens(w, foot, key, m):
    M = lens_tab(w, foot, key); L = dict(_LC["L"]); L["Yn"] = _LC["L"]["Yn"] * (1 + m); ch, b = Le.fit(L, M, list(range(15)), _LC["T0"]); return (ch - 56) / math.sqrt(112), ch
def row_groups(w, foot):
    P = Gr.P; a0 = A.A0[foot]; rows = Gr.load(); XG, LX, RHO, gt0 = Gr.XG, Gr.LX, Gr.RHO_H, Gr.gN_t
    def ls(lM, Re, dl):
        a = Re * (P.pc * 1e3) / 1.8153; Mb = 10 ** (lM + dl) * P.Msun; U = P.G * Mb / a ** 2; v = gt0 * U; gt = A.call(w, gb=v, gg=v * np.nan, gs=v * np.nan, r=XG * a, a0=a0, sample="group", lgMb=lM + dl) / U; s2 = np.trapz(4 * math.pi * XG ** 2 * RHO * XG * gt * XG, LX) / 3 * P.G * Mb / a; return .5 * math.log10(s2) - 3
    d = np.array([x[0] - ls(x[1], x[2], 0.0) for x in rows]); sl = np.array([(ls(x[1], x[2], .01) - ls(x[1], x[2], -.01)) / .02 for x in rows]); m = float(d.mean()); st = d.std(ddof=1) / math.sqrt(len(d)); return -m / st, -m / math.hypot(st, .10 * sl.mean()), st
def row_b2(c, foot, u, gabs, hse, dl):
    A.OG.b2(A.call, A.zrow, foot, c, A.A0[foot]) if "h7" not in A.OG._C else None
    n = A.OG._C["h7"]; GR, ms5, FIN, SBR = n["gr"], n["mstar500"], n["FIN"], n["SBR"]; G_, KP, MS = n["G"], n["kpc"], n["Msun"]; HSE = math.log10(1.2); e = math.exp(dl); a0 = A.A0[foot]
    def lr(tag, sf):
        o = []
        for g in GR:
            M5 = ms5(g["M500"]) * sf * 10 ** u; Rr, M, Mg, Ms = (g["R500"], g["M500"], g["Mg500"], M5) if tag == "R500" else (g["R2500"], g["M2500"], g["Mg2500"], M5 * np.mean(FIN)); Rr = Rr * e; M = M * e * 10 ** hse; Mg = Mg * e ** 2.5 * 10 ** gabs; Ms = Ms * e * e; r = Rr * KP; f = G_ * MS / r ** 2; v = A.call(c, gb=np.array([f * (Mg + Ms)]), gg=np.array([f * Mg]), gs=np.array([f * Ms]), r=np.array([r]), a0=a0, sample="xgroup")[0]; o.append(math.log10(M / (v / f)))
        return np.array(o)
    Z, Z0 = {}, {}
    for t in ("R500", "R2500"):
        b = lr(t, 1.); med = float(np.median(b)); er = float(np.std(b, ddof=1) / math.sqrt(len(b))); st = .5 * abs(float(np.median(lr(t, SBR))) - float(np.median(lr(t, 1 / SBR)))); Z[t] = med / math.hypot(er, st); Z0[t] = med / math.sqrt(er ** 2 + st ** 2 + HSE ** 2)
    return Z, Z0
_XC = {}
def row_xcop(c, foot, u, gabs, hse, dl):
    """Per cluster and x, log10(M_HSE/M_model). Returns mean per x, the cluster matrix, and RQ3's mean, rms."""
    from astropy.io import fits
    Gm, MSm, PCm = 6.674e-11, 1.989e30, 3.0857e16; D = os.path.join(A.REPO, "real_research", "data", "xcop"); a0 = A.A0[foot]; li = lambda r, m, t: float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    if "rows" not in _XC:
        XC = []
        for name in sorted(os.listdir(D)):
            p = os.path.join(D, name)
            if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{name}_mstar.fits"))): continue
            with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
            with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
            with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
            for x in (.1, .2, .3, .5, .7):
                r = x * r5; mh, mg, ms = li(hm["RADIUS"], hm["M_FORW"], r), li(ga["RADIUS"] * rg, ga["MGAS"], r), li(st["RADIUS"], st["MSTAR"], r)
                if np.all(np.isfinite([mh, mg, ms])): XC.append(dict(n=name, x=x, r=r * 1e3 * PCm, r5=r5 * 1e3 * PCm, mh=mh, mg=mg, ms=ms))
        _XC["rows"] = XC
    XC = _XC["rows"]; e = math.exp(dl); rr = np.array([z["r"] for z in XC]) * e; mg = np.array([z["mg"] for z in XC]) * e ** 2.5 * 10 ** gabs; ms = np.array([z["ms"] for z in XC]) * e * e * 10 ** u; gb = Gm * (mg + ms) * MSm / rr ** 2
    v = A.call(c, gb=gb, gg=Gm * mg * MSm / rr ** 2, gs=Gm * ms * MSm / rr ** 2, r=rr, r500=np.array([z["r5"] for z in XC]) * e, a0=a0, sample="cluster"); Mc = v * rr ** 2 / Gm / MSm; mh = np.array([z["mh"] for z in XC]) * e * 10 ** hse; d = np.log10(mh / Mc); ns = sorted({z["n"] for z in XC}); xs = (.1, .2, .3, .5, .7)
    M = np.full((len(ns), 5), np.nan)
    for z, dd in zip(XC, d): M[ns.index(z["n"]), xs.index(z["x"])] = dd
    by = np.array([d[[z["n"] == n for z in XC]].mean() for n in ns]); return dict(M=M, mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), se=float(by.std(ddof=1) / math.sqrt(len(ns))), n=len(ns))
def ups_boot(c, foot):
    """RQ3's boot per V bin (ul_rows' own), for the correlation of A5 and A6."""
    G = _G0(); a0 = A.A0[foot]
    def model(g, gb):
        gg = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; return A.call(c, gb=gb, gg=np.broadcast_to(gg, gb.shape), gs=gb - gg, r=np.broadcast_to(g["R"], gb.shape), a0=a0, sample="disc", name=g["name"], lgMb=g["lgMb"])
    Yb = CS.fit(G, model)["Yb"]; q = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in G]); V = np.array([g["Vflat"] for g in G]); fb = np.array([g["Vbul"][-1] ** 2 / max(g["Vdisk"][-1] ** 2 + g["Vbul"][-1] ** 2, 1e-9) for g in G]); u = Yb * (1 + .4 * fb); o = {}
    for b in ("60-100", "100-150", "150-200", "200-250", "250-400"):
        a = u[q & (V >= float(b.split("-")[0])) & (V < float(b.split("-")[1]))]; r = np.random.default_rng(1); n = len(a); o[b] = float(np.std(np.log10(np.median(a[r.integers(0, n, (2000, n))], axis=1))))
    return o
def zr(r): return float(r["Z"]) if r and "Z" in r else None
def evaluate(cid, c, foot, th, want=None, mw_cache=None):
    """th: physical shifts relative to RQ3's nominal (ups, gas_abs, dist, lens, hse absolute). Returns lines (Z) and gates. Keys are added elsewhere."""
    u, ga, dl, m, hs = th["ups"], th["gas_abs"], th["dist"], th["lens"], th["hse"]; o, gt = {}, {}; a0 = A.A0[foot]; w = Wrap(c, u, ga); set_dist(dl); sd = {}
    def tr(f, *a):
        try: return f(*a)
        except Exception as e: sd.setdefault("errors", []).append(f"{f.__name__ if hasattr(f, '__name__') else 'row'}: {type(e).__name__}: {str(e)[:60]}"); return None
    if not want or "sparc" in want:
        S0 = tr(A.rows_sparc, Wrap(c, 0.0, 0.0), foot); Su = tr(A.rows_sparc, w, foot) if u else S0
        if S0:
            for k in ("A3",): o[k] = zr(S0[k])
            o["A4"] = zr(Su["A4"]); o["A9"] = zr(Su["A9"]); o["A10"] = zr(Su["A10"]); gt["A1"] = S0["A1"]["value"]; gt["A2"] = S0["A2"]["value"] / 10 ** u; gt["A7"] = zr(S0["A7"]); EST = A.J(A.RB, "UL1_measured_upsilon_test", "ul1_est.json")["primary"]
            for rid, X in (("A5", "GSWLC"), ("A6", "Taylor")):
                for b, z0 in S0[rid]["bins"].items():
                    h = (math.log10(S0[rid]["values"][b]) - math.log10(EST[b][X]["mu"])) / z0 if z0 else 1e9; o[f"{rid}|{b}"] = (math.log10(S0[rid]["values"][b]) - math.log10(EST[b][X]["mu"]) - u) / h; sd.setdefault("h", {})[f"{rid}|{b}"] = h
    if not want or "dw" in want:
        D = tr(A.rows_dwarfs, w, foot)
        if D:
            for rid in ("A12", "A13"):
                for k, v in D[rid]["classes"].items(): o[f"{rid}|{k}"] = v["Z"]
            if "classes" in D.get("A11", {}): sd["A11"] = {k: v["Z"] for k, v in D["A11"]["classes"].items()}
    if not want or "tdg" in want:
        T = tr(lambda: A.OG.a23(A.call, A.zrow, A.NC, foot, w, a0))
        if T:
            o["A23a"] = (T["A23a"]["value"] - 6) / math.sqrt(12); gt["A23a_v"] = T["A23a"]["value"]
            for k, v in T["A23b"]["bins"].items(): o[f"A23b|{k}"] = v
        U = tr(lambda: A.OG.a24(A.call, A.zrow, foot, w, a0)); o["A24"] = zr(U["A24"]) if U else None
        E = tr(lambda: A.OG.a26(A.call, A.zrow, foot, w, a0))
        if E: o["A26a"] = zr(E["A26a"]); o["A26b"] = zr(E["A26b"])
    if not want or "lens" in want:
        r = tr(row_lens, w, foot, cid, m)
        if r: o["A30"] = r[0]
    if not want or "groups" in want:
        r = tr(row_groups, w, foot)
        if r: o["B1"] = r[0]; sd["B1_rq3"] = r[1]
    if not want or "b2" in want:
        r = tr(row_b2, c, foot, u, ga, hs, dl)
        if r:
            for k, v in r[0].items(): o[f"B2|{k}"] = v
            sd["B2_rq3"] = r[1]
    if not want or "xcop" in want:
        r = tr(row_xcop, c, foot, u, ga, hs, dl)
        if r:
            for j, x in enumerate(("0.1", "0.2", "0.3", "0.5", "0.7")): o[f"X|{x}"] = float(np.nanmean(r["M"][:, j]))
            sd["xM"] = np.round(r["M"], 10).tolist(); gt["B24"] = r["rms"]; sd["B23"] = (r["mean"], r["se"])
    if not want:
        Mx = mw_cache if mw_cache is not None else tr(A.rows_mw, c, foot)
        if Mx: o["A15"] = zr(Mx.get("A15")); o["A17"] = zr(Mx.get("A17")); gt["A16"] = Mx.get("A16", {}).get("label")
        DM = tr(A.rows_dm, c, foot)
        if DM: o["A18"] = zr(DM.get("A18"))
        a20 = tr(lambda: A.OG.a20(A.call, A.zrow, foot, c, a0)); o["A20"] = zr(a20["A20"]) if a20 else None
        a25 = tr(lambda: A.OG.a25(A.call, foot, c, a0)); gt["A25"] = a25["A25"]["label"] if a25 else None; gt["A25_v"] = a25["A25"]["value"] if a25 else None
        pl = tr(A.rows_planets, c, foot); gt["C1"] = pl["C1"]["label"] if pl else None; gt["C1_bins"] = pl["C1"]["bins"] if pl else None
    if not want or "a21" in want:
        a21 = tr(lambda: A.OG.a21(A.call, A.lrow, foot, w, a0, CS, A.CRG)); gt["A21"] = a21["A21"]["value"] if a21 else None
    set_dist(0.0); return {k: v for k, v in o.items() if v is not None and np.isfinite(v)}, gt, sd
