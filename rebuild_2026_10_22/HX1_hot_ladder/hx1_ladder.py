#!/usr/bin/env python3
"""HX1 stage 1, the plain ladder (FROZEN_CRITERIA.md, AMENDMENT_A1.md). Per hot system B_need = (D_obs - D_N) / (D_law - D_N) on RQ3's own
estimators: B1's integral on Tian+2026 (MaNGA, ATLAS, groups; dwarfs reported only), A26a's h50 Jeans on SLUGGS (by root, A1), B2's h7 on
Lovisari, B23's X-COP. --checks: K1, K2 only. Env HX1_MUTATE=1: every B_need -> 1/B_need, exit 1 if NEED fails (caught).
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys, types
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path[:0] = [HERE, os.path.join(RB, "TX1_temperature_leaf")]
import numpy as np
from scipy.optimize import brentq
import hx1_acc
n = hx1_acc.load(); OG = n["OG"]; A0 = n["A0"]; FEET = n["FEET"]; call = n["call"]; CRG = n["CRG"]
import tx1_lib as TX
MUT = os.environ.get("HX1_MUTATE") == "1"; CHK = "--checks" in sys.argv; TAG = "_MUTATE" if MUT else ("_checks" if CHK else ""); NB = 2000; NK3 = 200; ZL = 2.0
OUT = open(os.path.join(HERE, f"hx1_ladder{TAG}.out"), "w"); RES = dict(footings={}, checks={})
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
lawf = lambda x, a0: x * (.5 + np.sqrt(.25 + a0 / x))
def mul(B): return types.SimpleNamespace(g=lambda Q: (lambda x: x + B * (lawf(x, Q["a0"]) - x))(np.asarray(Q["gb"], float)))
NEWT, LAW = mul(0.0), mul(1.0)
KEV, MP = 1.602176634e-16, 1.67262192e-27; s_kT = lambda kT: math.sqrt(kT * KEV / (0.6 * MP)) / 1e3
inv = (lambda B: 1.0 / B) if MUT else (lambda B: B)

# ---------- Tian+2026 through B1's integral
n["crg"](); import crg1_groups as Gr
P, XG, LX, RHO, gt0 = Gr.P, Gr.XG, Gr.LX, Gr.RHO_H, Gr.gN_t
TI = []
for l in open(os.path.join(CRG, "inputs", "groups", "J_A_A_710_L39.tsv")):
    if l.startswith("#"): continue
    f = l.rstrip("\n").split("\t")
    if len(f) >= 13 and f[0].strip().isdigit(): TI.append(dict(cls=f[1].strip(), ls=float(f[5]), lM=float(f[7]), lg=float(f[9]), Re=float(f[10])))
def s2(o, dl, c, a0):
    a = o["Re"] * (P.pc * 1e3) / 1.8153; Mb = 10 ** (o["lM"] + dl) * P.Msun; U = P.G * Mb / a ** 2; v = gt0 * U
    gt = call(c, gb=v, gg=v * np.nan, gs=v * np.nan, r=XG * a, a0=a0, sample="group", lgMb=o["lM"] + dl) / U
    return np.trapz(4 * math.pi * XG ** 2 * RHO * XG * gt * XG, LX) / 3 * P.G * Mb / a
def tian(cls, a0, dl=0.0):
    O = [o for o in TI if o["cls"] == cls]; sN = np.array([s2(o, dl, NEWT, a0) for o in O]); sL = np.array([s2(o, dl, LAW, a0) for o in O]); sO = np.array([(10 ** o["ls"] * 1e3) ** 2 for o in O])
    return O, inv((sO - sN) / (sL - sN)), np.array([10 ** o["ls"] for o in O]), sN, sL, sO

# ---------- SLUGGS through A26a's h50 path; B_need by root (A1)
def sluggs(a0, shift=0.0, c_only=None):
    n50 = OG._C["h50"]; G_, KP, MS, GA = n50["G"], n50["kpc"], n50["Msun"], n50["GAMMA"]; Bs, keys, offs = [], [], []
    for r in n50["res"]:
        ah = r["Re"] / 1.8153
        def D(c):
            def gf(rr):
                rr = np.asarray(rr, float); Mb = r["Mstar"] * MS * rr ** 2 / (rr + ah) ** 2; gN = G_ * Mb / (rr * KP) ** 2; return call(c, gb=gN, gg=gN * 0, gs=gN, r=rr * KP, a0=a0, sample="et")
            s = n50["sigma_los"](r["Rb"], n50["sigma_r2"](gf, GA), GA); return s[r["out"]]
        if c_only is not None: return D(c_only)
        so = r["Sb"][r["out"]] * 10 ** shift; DO = float(np.mean(so ** 2)); sL = D(LAW); DN, DL = float(np.mean(D(NEWT) ** 2)), float(np.mean(sL ** 2)); offs.append(float(np.mean(np.log10(r["Sb"][r["out"]] / sL))))
        if DO >= DN: hi = 1.0
        else: Bs.append((DO - DN) / (DL - DN)); keys.append(float(np.mean(r["Sb"][r["out"]]))); continue
        while float(np.mean(D(mul(hi)) ** 2)) < DO: hi *= 2
        Bs.append(brentq(lambda B: float(np.mean(D(mul(B)) ** 2)) - DO, 0.0, hi, xtol=1e-10)); keys.append(float(np.mean(r["Sb"][r["out"]])))
    return inv(np.array(Bs)), np.array(keys), np.array(offs)

# ---------- Lovisari through B2's h7 path
def lovisari(a0, tag, sf=1.0, hse=1.0):
    n7 = OG._C["h7"]; GR, ms5, FIN = n7["gr"], n7["mstar500"], n7["FIN"]; G_, KP, MS = n7["G"], n7["kpc"], n7["Msun"]; Bs, keys, res = [], [], []
    for g in GR:
        M5 = ms5(g["M500"]) * sf; Rr, M, Mg, Ms = (g["R500"], g["M500"], g["Mg500"], M5) if tag == "R500" else (g["R2500"], g["M2500"], g["Mg2500"], M5 * np.mean(FIN))
        r = Rr * KP; f = G_ * MS / r ** 2; gb = np.array([f * (Mg + Ms)]); ML = float(call(LAW, gb=gb, gg=gb * 0, gs=gb * 0, r=np.array([r]), a0=a0, sample="xgroup")[0]) / f; Mo = M * hse
        Bs.append((Mo - (Mg + Ms)) / (ML - (Mg + Ms))); keys.append(s_kT(g["kT"])); res.append(math.log10(M / ML))
    return inv(np.array(Bs)), np.array(keys), np.array(res)

# ---------- X-COP through B23's path
def xcop_points():
    from astropy.io import fits
    D = os.path.join(n["REPO"], "real_research", "data", "xcop"); li = lambda r, m, t: float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan; XC = []
    for name in sorted(os.listdir(D)):
        p = os.path.join(D, name)
        if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{name}_mstar.fits"))): continue
        with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        for x in (.1, .2, .3, .5, .7):
            r = x * r5; mh, mg, ms = li(hm["RADIUS"], hm["M_FORW"], r), li(ga["RADIUS"] * rg, ga["MGAS"], r), li(st["RADIUS"], st["MSTAR"], r)
            if np.all(np.isfinite([mh, mg, ms])): XC.append(dict(n=name, x=x, r=r * 1e3 * 3.0857e16, mh=mh, mg=mg, ms=ms))
    return XC
XC = xcop_points(); TT = TX.tload()
def xcop(a0, dm=0.0, c=LAW):
    Gm, MSm = 6.674e-11, 1.989e30; rr = np.array([z["r"] for z in XC]); mb = np.array([z["mg"] + z["ms"] for z in XC]); gb = Gm * mb * MSm / rr ** 2
    Mc = call(c, gb=gb, gg=gb * 0, gs=gb * 0, r=rr, a0=a0, sample="cluster") * rr ** 2 / Gm / MSm; mh = np.array([z["mh"] for z in XC]) * 10 ** dm
    return inv((mh - mb) / (Mc - mb)), np.array([s_kT(TT[z["n"]]["Tew"]) for z in XC]), np.log10(mh / Mc), mb, Mc

# ---------- statistics
def ylog(B): m = float(np.median(B)); return math.log10(m) if m > 0 else float("nan")
def boot(B, rng, groups=None):
    if groups is None: idx = [rng.integers(0, len(B), len(B)) for _ in range(NB)]
    else:
        u = sorted(set(groups)); gi = {k: np.flatnonzero(np.array(groups) == k) for k in u}; idx = [np.concatenate([gi[u[j]] for j in rng.integers(0, len(u), len(u))]) for _ in range(NB)]
    m = np.array([np.median(B[i]) for i in idx]); y = np.where(m > 0, np.log10(np.maximum(m, 1e-300)), -np.inf); q = np.percentile(y, [16, 84]); return float((q[1] - q[0]) / 2)
def pava(y, w):
    b = [[float(v), float(x), 1] for v, x in zip(y, w)]; i = 0
    while i < len(b) - 1:
        if b[i][0] > b[i + 1][0]:
            W = b[i][1] + b[i + 1][1]; b[i] = [(b[i][0] * b[i][1] + b[i + 1][0] * b[i + 1][1]) / W, W, b[i][2] + b[i + 1][2]]; del b[i + 1]; i = max(i - 1, 0)
        else: i += 1
    return np.concatenate([[v] * k for v, _, k in b])
def iso_fit(keys, y, s):
    o = np.argsort(keys, kind="stable"); k, yy, ww = keys[o], y[o], 1 / s[o] ** 2; uk = np.unique(k); by = np.array([np.sum(yy[k == u] * ww[k == u]) / np.sum(ww[k == u]) for u in uk]); bw = np.array([np.sum(ww[k == u]) for u in uk])
    fb = np.maximum(0.0, pava(by, bw)); f = np.empty_like(y); f[o] = np.array([fb[np.flatnonzero(uk == kk)[0]] for kk in k]); return f, float(np.sum(((y - f) / s) ** 2))
def order_p(keys, y, s, rng, nb=NB):
    if not np.all(np.isfinite(y)): return dict(chi2=float("nan"), p=0.0, f=[float("nan")] * len(y), why="SUB-NEWTONIAN rung")
    f, c = iso_fit(keys, y, s); cs = np.array([iso_fit(keys, f + rng.normal(0, s), s)[1] for _ in range(nb)]); return dict(chi2=c, p=float(np.mean(cs >= c)), f=f.tolist())

# ---------- run
for foot in FEET:
    a0 = A0[foot]; rng = np.random.default_rng(20261103); R = dict(rungs={}, reported={}, tests={}); RES["footings"][foot] = R; say("=" * 100); say(f"HX1 stage 1, {foot}, a0 {a0}{'  [MUTATE: B -> 1/B]' if MUT else ''}")
    OG.a26(call, n["zrow"], foot, LAW, a0); OG.b2(call, n["zrow"], foot, LAW, a0)
    # K1: reproduction at B = 1
    K1 = {}; Og, _, _, sN, sL, sO = tian("Galaxy group", a0); d = np.array([o["ls"] for o in Og]) - 0.5 * np.log10(sL) + 3; K1["B1"] = float(-d.mean())
    _, _, offs = sluggs(a0); K1["A26a"] = float(offs.mean()); K1["B2"] = {t: float(np.median(lovisari(a0, t)[2])) for t in ("R500", "R2500")}; K1["B23"] = float(xcop(a0)[2].mean())
    ref = dict(canonical=dict(B1=-0.010028459614915594, A26a=0.07668459886384758, B2=dict(R500=0.161, R2500=0.349), B23=0.46749944838192325), alt=dict(B1=0.010269366304557246, A26a=0.06203774779553823, B2=dict(R500=0.123, R2500=0.312), B23=0.4345236474485682))[foot]
    ok1 = abs(K1["B1"] - ref["B1"]) < 1e-4 and abs(K1["A26a"] - ref["A26a"]) < 1e-4 and abs(K1["B23"] - ref["B23"]) < 1e-4 and all(abs(K1["B2"][t] - ref["B2"][t]) < 1e-3 for t in ("R500", "R2500"))
    RES["checks"][f"K1_{foot}"] = dict(ok=ok1, got=K1, ref=ref); say(f"K1 {foot}: {'PASS' if ok1 else 'FAIL'}  got {json.dumps(K1)}  ref {json.dumps(ref)}")
    # K2: linearity at B = 2, 5 objects per estimator
    e = []
    for o in [x for x in TI if x["cls"] == "MaNGA elliptical"][:5]: a, b_, c2 = s2(o, 0, NEWT, a0), s2(o, 0, LAW, a0), s2(o, 0, mul(2.0), a0); e.append(abs(c2 - (a + 2 * (b_ - a))) / c2)
    eT = max(e); eS = []
    for i in range(5):
        r = OG._C["h50"]["res"][i]; one = lambda c: (OG._C["h50"].__setitem__("res", [r]), sluggs(a0, c_only=c))[1]; full = OG._C["h50"]["res"]
        try: DN_, DL_, D2_ = (float(np.mean(one(c) ** 2)) for c in (NEWT, LAW, mul(2.0)))
        finally: OG._C["h50"]["res"] = full
        eS.append(abs(D2_ - (DN_ + 2 * (DL_ - DN_))) / D2_)
    _, _, _, mbX, McX = xcop(a0); _, _, _, _, M2X = xcop(a0, c=mul(2.0)); eX = float(np.max(np.abs(M2X - (mbX + 2 * (McX - mbX))) / M2X))
    ok2 = eT < 1e-9 and eX < 1e-9; RES["checks"][f"K2_{foot}"] = dict(ok=ok2, tian=eT, xcop=eX, sluggs_linear_err=max(eS), sluggs_read="A1: by root; linear error reported, must be < 1e-3", sluggs_ok=max(eS) < 1e-3)
    say(f"K2 {foot}: {'PASS' if ok2 else 'FAIL'}  Tian {eT:.1e}, X-COP {eX:.1e} (line 1e-9); SLUGGS linear-formula error {max(eS):.1e} (A1: root used; line 1e-3 {'PASS' if max(eS) < 1e-3 else 'FAIL'})")
    if CHK: continue
    # rungs
    ma = [o for o in TI if o["cls"] == "MaNGA elliptical"]; q = np.percentile([10 ** o["ls"] for o in ma], [25, 50, 75])
    def tian_rung(cls, sel=None):
        O, B, k, *_ = tian(cls, a0); Bp, Bm = tian(cls, a0, .10)[1], tian(cls, a0, -.10)[1]
        if sel is not None: m = sel(k); B, k, Bp, Bm = B[m], k[m], Bp[m], Bm[m]
        y = ylog(B); sy = abs(ylog(Bp) - ylog(Bm)) / 2; sb = boot(B, rng); return dict(y=y, s=math.hypot(sb, sy), s_boot=sb, s_sys=sy, key=float(np.median(k)), n=int(len(B)), Bmed=float(np.median(B)), frac_sub=float(np.mean(B <= 0)))
    for j, (lo, hi) in enumerate(zip([0, *q], [*q, 1e9])): R["rungs"][f"MaNGA Q{j + 1}"] = tian_rung("MaNGA elliptical", lambda k, lo=lo, hi=hi: (k > lo) & (k <= hi))
    R["rungs"]["ATLAS"] = tian_rung("ATLAS elliptical"); R["rungs"]["Tian groups"] = tian_rung("Galaxy group")
    sA = float(offs.std(ddof=1) / math.sqrt(len(offs))); B, k, _ = sluggs(a0); Bp, Bm = sluggs(a0, sA)[0], sluggs(a0, -sA)[0]; sy = abs(ylog(Bp) - ylog(Bm)) / 2; sb = boot(B, rng)
    R["rungs"]["SLUGGS"] = dict(y=ylog(B), s=math.hypot(sb, sy), s_boot=sb, s_sys=sy, key=float(np.median(k)), n=len(B), Bmed=float(np.median(B)), frac_sub=float(np.mean(B <= 0)), sigma_A26a=sA)
    n7 = OG._C["h7"]
    for t in ("R500", "R2500"):
        B, k, _ = lovisari(a0, t); y = ylog(B); st = abs(ylog(lovisari(a0, t, n7["SBR"])[0]) - ylog(lovisari(a0, t, 1 / n7["SBR"])[0])) / 2; sh = abs(ylog(lovisari(a0, t, hse=1.2)[0]) - ylog(lovisari(a0, t, hse=1 / 1.2)[0])) / 2; sb = boot(B, rng)
        R["rungs"][f"Lovisari {t}"] = dict(y=y, s=math.sqrt(sb ** 2 + st ** 2 + sh ** 2), s_boot=sb, s_star=st, s_hse=sh, key=float(np.median(k)), n=len(B), Bmed=float(np.median(B)), frac_sub=float(np.mean(B <= 0)))
    B, k, *_ = xcop(a0); gX = [z["n"] for z in XC]; sy = abs(ylog(xcop(a0, .121)[0]) - ylog(xcop(a0, -.121)[0])) / 2; sb = boot(B, rng, gX)
    R["rungs"]["X-COP"] = dict(y=ylog(B), s=math.hypot(sb, sy), s_boot=sb, s_sys=sy, key=float(np.median(k)), n=len(B), Bmed=float(np.median(B)), frac_sub=float(np.mean(B <= 0)))
    for cls in ("Local Group dwarf", "Fornax dwarf", "Virgo dwarf"):
        O, Bd, kd, *_ = tian(cls, a0); R["reported"][cls] = dict(y=ylog(Bd), Bmed=float(np.median(Bd)), key=float(np.median(kd)), n=len(Bd), frac_sub=float(np.mean(Bd <= 0)))
    names = sorted(R["rungs"], key=lambda r: R["rungs"][r]["key"]); keys = np.array([R["rungs"][r]["key"] for r in names]); y = np.array([R["rungs"][r]["y"] for r in names]); s = np.array([R["rungs"][r]["s"] for r in names])
    s = np.where(np.isfinite(s), s, 1e3)  # A1: a rung whose error band reaches B <= 0 carries no weight in the order
    # K3: power at the real keys and errors
    yl = np.maximum(0, .8 * np.log10(keys / 300)); ell = np.array([r.startswith(("MaNGA", "ATLAS", "SLUGGS")) for r in names]); grp = np.array([r.startswith(("Tian groups", "Lovisari")) for r in names]); yb = np.where(ell, math.log10(2), np.where(grp, 0.0, y))
    ix = names.index("X-COP"); pl, pb, zl = [], [], []
    for _ in range(NK3):
        d1 = yl + rng.normal(0, s); pl.append(order_p(keys, d1, s, rng, 500)["p"]); zl.append(d1[ix] / s[ix]); pb.append(order_p(keys, yb + rng.normal(0, s), s, rng, 500)["p"])
    brk_applies = bool(np.min(keys[grp]) > np.min(keys[ell])); ok3 = np.median(pl) >= .05 and np.median(zl) > ZL and np.median(pb) < .05
    RES["checks"][f"K3_{foot}"] = dict(ok=bool(ok3), ladder_median_p=float(np.median(pl)), ladder_median_Z_need=float(np.median(zl)), break_median_p=float(np.median(pb)), break_has_ellipticals_below_groups=brk_applies, n_planted=NK3, nb_inner=500)
    say(f"K3 {foot}: {'PASS' if ok3 else 'MISS -> stage 1 NOT DIAGNOSTIC'}  planted ladder median p {np.median(pl):.3f}, NEED Z {np.median(zl):.2f}; planted break median p {np.median(pb):.3f} (ellipticals below groups' sigma: {brk_applies})")
    say("-" * 100); say(f"{'rung':16s} {'key sigma':>9s} {'n':>5s} {'median B_need':>13s} {'y':>8s} {'s':>7s}  (s_boot, sys)  frac B<=0")
    for r in names: v = R["rungs"][r]; say(f"{r:16s} {v['key']:9.1f} {v['n']:5d} {v['Bmed']:13.3f} {v['y']:+8.3f} {v['s']:7.3f}  ({v['s_boot']:.3f}, {math.sqrt(max(v['s'] ** 2 - v['s_boot'] ** 2, 0)):.3f})  {v['frac_sub']:.2f}")
    for cls, v in R["reported"].items(): say(f"  reported only: {cls:18s} key {v['key']:6.1f}, n {v['n']}, median B_need {v['Bmed']:.3f}, y {v['y']:+.3f}, frac B<=0 {v['frac_sub']:.2f}")
    # tests
    T = R["tests"]; o = order_p(keys, y, s, rng); T["L-ORDER"] = dict(o, order=names, pass_=bool(o["p"] >= .05)); T["L-NEED"] = dict(Z=float(y[ix] / s[ix]), pass_=bool(y[ix] / s[ix] > ZL))
    Bx, _, *_ = xcop(a0); lx = np.log10([z["x"] for z in XC]); ok = Bx > 0; sl = float(np.polyfit(lx[ok], np.log10(Bx[ok]), 1)[0]); u = sorted(set(gX)); sls = []
    for _ in range(NB):
        ii = np.concatenate([np.flatnonzero((np.array(gX) == u[j]) & ok) for j in rng.integers(0, len(u), len(u))]); sls.append(np.polyfit(lx[ii], np.log10(Bx[ii]), 1)[0])
    e_ = float(np.diff(np.percentile(sls, [16, 84]))[0] / 2); T["L-FLAT X-COP"] = dict(slope=sl, err=e_, Z=sl / e_, n_used=int(ok.sum()), pass_=bool(abs(sl / e_) <= ZL))
    a, b_ = R["rungs"]["Lovisari R2500"], R["rungs"]["Lovisari R500"]; dz = (a["y"] - b_["y"]) / math.hypot(a["s"], b_["s"]); T["L-FLAT Lovisari"] = dict(diff=a["y"] - b_["y"], Z=dz, pass_=bool(abs(dz) <= ZL))
    O, Bm_, km_, *_ = tian("MaNGA elliptical", a0); g_ = np.array([o["lg"] for o in O]); ok = Bm_ > 0; X = np.column_stack([np.ones(ok.sum()), np.log10(km_[ok]), g_[ok]]); Y = np.log10(Bm_[ok]); cf = np.linalg.lstsq(X, Y, rcond=None)[0]
    cb = np.array([np.linalg.lstsq(X[i], Y[i], rcond=None)[0] for i in (rng.integers(0, len(Y), len(Y)) for _ in range(NB))]); ce = cb.std(axis=0); zs, zg = cf[1] / ce[1], cf[2] / ce[2]
    T["L-KEY"] = dict(coef_sigma=float(cf[1]), Z_sigma=float(zs), coef_gbar=float(cf[2]), Z_gbar=float(zg), n=int(ok.sum()), label="SIGMA CARRIES IT" if abs(zs) > ZL and abs(zg) <= ZL else ("GBAR CARRIES IT" if abs(zg) > ZL and abs(zs) <= ZL else ("BOTH" if abs(zs) > ZL else "NEITHER")))
    fl = T["L-FLAT X-COP"]["pass_"] and T["L-FLAT Lovisari"]["pass_"]; R["class"] = ("LADDER" if fl else "LADDER, NOT FLAT") if T["L-ORDER"]["pass_"] and T["L-NEED"]["pass_"] else "NO LADDER"
    if not ok3: R["class"] += " [NOT DIAGNOSTIC: K3]"
    say("-" * 100); say(f"L-ORDER: chi2 {o['chi2']:.2f}, p {o['p']:.4f} -> {'ORDERED' if T['L-ORDER']['pass_'] else 'NOT ORDERED'}" + (f" ({o.get('why')})" if o.get("why") else "")); say("   isotonic fit by rung: " + ", ".join(f"{r} {v:+.3f}" for r, v in zip(names, o["f"])))
    say(f"L-NEED: X-COP Z {T['L-NEED']['Z']:+.2f} -> {'PASS' if T['L-NEED']['pass_'] else 'FAIL'}")
    say(f"L-FLAT X-COP: slope of log B_need on log x {sl:+.3f} +- {e_:.3f}, Z {sl / e_:+.2f} -> {'FLAT' if T['L-FLAT X-COP']['pass_'] else 'NOT FLAT'}; Lovisari R2500 - R500 {a['y'] - b_['y']:+.3f}, Z {dz:+.2f} -> {'FLAT' if T['L-FLAT Lovisari']['pass_'] else 'NOT FLAT'}")
    say(f"L-KEY (MaNGA, n {ok.sum()}): sigma {cf[1]:+.3f} (Z {zs:+.2f}), gbar(Re) {cf[2]:+.3f} (Z {zg:+.2f}) -> {T['L-KEY']['label']}")
    say(f"STAGE 1 CLASS, {foot}: {R['class']}")
json.dump(RES, open(os.path.join(HERE, f"hx1_ladder{TAG}.json"), "w"), indent=1, default=float)
if MUT:
    caught = all(not RES["footings"][f]["tests"]["L-NEED"]["pass_"] for f in FEET); say("MUTATE", "caught: NEED fails on both footings" if caught else "NOT caught"); sys.exit(1 if caught else 0)
