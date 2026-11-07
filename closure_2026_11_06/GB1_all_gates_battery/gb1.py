#!/usr/bin/env python3
"""GB1 (criteria e9464bc8ce): one frozen all-gates battery; every live candidate graded through it.
    python3 gb1.py            -> gb1.json / gb1.out          (KA1-KA6, then L0 L1 L2 F1 F2 F3)
    python3 gb1.py --mutate   -> gb1_MUTATE.json / .out      (Newton, b = 1, F = 0; must FAIL)
Read-only use of QX5 (loaders), QX8 (exact-field parts), QX20/QX21/QX26 JSONs, S1, LW1, X1, CFG61, C6P.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, csv, re, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; TAG = "gb1_MUTATE" if MUT else "gb1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ QX5 loaders (QX16-fixed), exactly as QX20 executes them
src = open(os.path.join(CL, "QX5_cluster_terms", "qx5.py")).read(); cut = src.index("XC, SP, EL, LE, GR = ")
NS = {"__file__": os.path.join(CL, "QX5_cluster_terms", "qx5.py"), "__name__": "qx5_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:cut], "qx5_lib", "exec"), NS); sys.argv = _a
G, MS, KPC, C, PC = NS["G"], NS["MS"], NS["KPC"], NS["C"], NS["PC"]
A0, phi_from, tail_phi = NS["A0"], NS["phi_from"], NS["tail_phi"]
XC, SP, EL, GR = NS["xcop"](), NS["sparc"](), NS["ellipticals"](), NS["groups"]()
LSTAR = {"canonical": 21.7, "alt": 22.9}
def glaw(gN, a0): return 0.5 * gN + math.sqrt(0.25 * gN * gN + a0 * gN)
def nu_minus_1(x): return (1.0 / x) / (math.sqrt(0.25 + 1.0 / x) + 0.5)       # g_law/g_N - 1, stable at large x
DATA = os.path.join(REPO, "real_research", "data")
K_TO_S = 1 / 0.63

# ------------------------------------------------------------------ record JSONs (read-only)
Q20 = json.load(open(os.path.join(CL, "QX20_failure_ladder", "qx20.json")))
Q21 = json.load(open(os.path.join(CL, "QX21_step_origin", "qx21.json")))
Q26 = json.load(open(os.path.join(CL, "QX26_imf_variation", "qx26.json")))
C6P = json.load(open(os.path.join(RB, "C6P_cassini_high_precision", "c6p_cassini_hp.json")))
KA20 = {"canonical": dict(X=0.467499, E=0.209888, S=0.027383, G0=0.358644, G1=0.195519),
        "alt": dict(X=0.434523, E=0.188763, S=-0.000603, G0=0.320274, G1=0.158280)}
s26 = open(os.path.join(CL, "QX26_imf_variation", "qx26.py")).read()
SIG0 = eval(re.search(r"^SIG0 = (dict\(.*\))$", s26, re.M).group(1)); AP = float(re.search(r"^AP = ([0-9.]+)", s26, re.M).group(1))
HUM = {}
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
for r in rows[1:]:
    d = dict(zip(rows[0], r)); HUM[d["name"]] = float(d["ups_salp"]) / float(d["ups_krou"])

# ------------------------------------------------------------------ QX8 exact-field parts (T_geom at U = 0.50)
Q8D = os.path.join(CL, "QX8_sparc_exact_field"); NODES = np.array([0.30, 0.42, 0.60, 0.85, 1.20])
q8names = sorted(f[:-11] for f in os.listdir(os.path.join(DATA, "sparc_data")) if f.endswith("_rotmod.dat"))
def tgeom_rows(foot, name):
    i = q8names.index(name); z = np.load(os.path.join(Q8D, "parts", foot, f"{i:03d}.npz"))
    assert str(z["name"]) == name, (name, str(z["name"]))
    T = z["T"]; return np.array([np.interp(math.log(0.5), np.log(NODES), T[:, j]) for j in range(T.shape[1])])
def sparc_okmask(name):  # QX5's own row mask, recomputed to index QX8's per-row T
    a = np.loadtxt(os.path.join(DATA, "sparc_data", name + "_rotmod.dat"), comments="#")
    if a.ndim == 1: a = a[None]
    R, V, eV, Vg, Vd, Vb = a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5]
    vb2 = np.sign(Vg) * Vg ** 2 + 0.5 * np.sign(Vd) * Vd ** 2 + 0.7 * np.sign(Vb) * Vb ** 2
    return (V > 0) & (eV / np.maximum(V, 1e-9) <= 0.1) & (vb2 > 0) & (R > 0)

# ------------------------------------------------------------------ feature builders (per footing)
def star(share, sigma, rsk, key): return dict(share=share, sigma=sigma, rsk=rsk, key=key)
def F_(x, Mb, r, v, sigma, fgas, stars, depth=None, xe=None, Tg=0.0, **kw):
    d = dict(x=x, Mb=Mb, r=r, v=v, sigma=sigma, fgas=fgas, stars=stars, depth=depth, xe=xe, Tgeom=Tg, zf=None); d.update(kw); return d

def build(f, a0):
    S, E, X = [], [], []
    for g in SP:
        r, V = g["R"], g["V"]; gobs = V ** 2 / r; gbar = g["vb2"] / r; gl = np.array([glaw(x, a0) for x in gbar])
        Mtot_b = g["vb2"][-1] * r[-1] / G
        T = tgeom_rows(f, g["name"])[sparc_okmask(g["name"])]; assert len(T) == len(r), g["name"]
        for i in range(len(r)):
            vb2 = g["vb2"][i]; Mb = vb2 * r[i] / G
            stars = [star(max(g["vd2"][i], 0) / vb2, None, K_TO_S, "sig_disc"), star(max(g["vbu2"][i], 0) / vb2, None, K_TO_S, "sig_bul")]
            S.append(dict(D=math.log10(gobs[i] / gl[i]), feat=F_(gbar[i] / a0, Mb / MS, r[i], V[i] / 1e3, None,
                     min(max(g["vg2"][i] / vb2, 0.0), 1.0), stars, depth=phi_from(r, gobs, i, Mtot_b, a0) / C ** 2,
                     Tg=float(T[i]), rrM=r[i] / math.sqrt(G * Mtot_b / a0))))
    for e in EL:
        rg = np.linspace(2 * e["Re"], 8 * e["Re"], 400) * KPC
        gt = np.array([G * e["Mtot"](x / KPC) * MS / x ** 2 for x in rg]); Mbt = e["Mbar"](1e9)
        for m in (2, 4, 8):
            r = m * e["Re"]; rm = r * KPC; Mb = e["Mbar"](r); Mo = e["Mtot"](r)
            gN = G * Mb * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS; i = int(np.argmin(abs(rg - rm)))
            E.append(dict(D=math.log10(Mo / Ml), name=e["name"], feat=F_(gN / a0, Mb, rm, math.sqrt(G * Mo * MS / rm) / 1e3, AP * SIG0[e["name"]], 0.0,
                     [star(1.0, AP * SIG0[e["name"]], HUM[e["name"]], "sig_star")], depth=phi_from(rg, gt, i, e["Mbar"](8 * e["Re"]) * MS, a0) / C ** 2,
                     rrM=rm / math.sqrt(G * Mbt * MS / a0))))
    for z in XC:
        rm = z["r_kpc"] * KPC; gN = G * z["M_b"] * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS
        hr = z["hr"] * KPC; gh = G * z["hM"] * MS / hr ** 2; i = int(np.searchsorted(hr, rm))
        dep = (float(np.trapz(np.concatenate([[G * z["M_obs"] * MS / rm ** 2], gh[i:]]), np.concatenate([[rm], hr[i:]])))
               + tail_phi(z["Mb_last"][0] * MS, z["Mb_last"][1] * KPC, a0)) / C ** 2
        fg = z["M_gas"] / z["M_b"]
        X.append(dict(D=math.log10(z["M_obs"] / Ml), feat=F_(gN / a0, z["M_b"], rm, math.sqrt(G * z["M_obs"] * MS / rm) / 1e3, None, fg,
                 [star(1 - fg, None, K_TO_S, "sig_star")], depth=dep, rrM=rm / math.sqrt(G * z["Mb_last"][0] * MS / a0))))
    return S, E, X

def groups_pts(a0, fst):
    out = []
    for gp in GR:
        sl = math.log(gp["M5"] / gp["M25"]) / math.log(gp["R5"] / gp["R25"]); pts = []
        for j, p in enumerate(gp["pts"]):
            rm = p["r_kpc"] * KPC; Mb = p["M_gas"] * (1 + fst); gN = G * Mb * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS
            rr = np.linspace(p["r_kpc"], gp["R5"], 200) * KPC; Mr = gp["M25"] * (rr / (gp["R25"] * KPC)) ** sl
            dep = ((float(np.trapz(G * Mr * MS / rr ** 2, rr)) if j == 0 else 0.0) + tail_phi(gp["g5"] * MS, gp["R5"] * KPC, a0)) / C ** 2
            pts.append(dict(D=math.log10(p["M_obs"] / Ml), sl=p["eM"] / (p["M_obs"] * math.log(10)),
                            feat=F_(gN / a0, Mb, rm, math.sqrt(G * p["M_obs"] * MS / rm) / 1e3, None, 1 / (1 + fst),
                                    [star(fst / (1 + fst), None, K_TO_S, "sig_star")], depth=dep, kT=gp["kT"],
                                    rrM=rm / math.sqrt(G * gp["g5"] * (1 + fst) * MS / a0))))
        out.append(dict(name=gp["name"], pts=pts))
    return out

S1D = os.path.join(RB, "S1_v3_hosted_small")
UROWS = list(csv.DictReader(open(os.path.join(S1D, "s1_coma_per_galaxy.csv"))))
R1 = json.load(open(os.path.join(S1D, "s1_v3_hosted_small_results.json")))["coma"]
def udgs(f, a0):
    out = []
    for r in UROWS:
        if r["footing"] != f: continue
        Ms = float(r["Mstar"]); rh = 4 / 3 * float(r["Re_kpc"]) * KPC; sg = float(r["sigma"])
        out.append(dict(D=float(r["E_v3_dmean"]) / math.log(10), feat=F_(G * Ms / 2 * MS / rh ** 2 / a0, Ms, rh, sg, sg, 0.0,
                   [star(1.0, sg, K_TO_S, "sig_star")], xe=float(r["x_e_dmean"]), rrM=rh / math.sqrt(G * Ms * MS / a0))))
    return out

LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))
X1R = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv")))}
DCLS = ("MW classical", "bright M31", "MW ultra-faint", "M31 others", "LG field")   # QX21's order
GRADED_D = ("bright M31", "MW classical", "LG field")
def x_from_nu(nu):
    q = (nu - 0.5) ** 2 - 0.25
    return 1.0 / q if q > 0 else float("nan")
def dsphs(f, a0):
    ps = LW["footings"][f]["per_system"]; out = {c: [] for c in DCLS}
    for n, s in ps.items():
        if s["cls"] not in out: continue
        xr = X1R.get((f, n)); x = sg = Ms = rh = None
        if xr is not None:
            x = x_from_nu(10 ** (float(xr["Delta[Newton]"]) - s["plain"])); sg = float(xr["sigma"]); Ms = 10 ** float(xr["logMstar"]); rh = float(xr["rh_pc"]) * PC
            if not (np.isfinite(x) and x > 0): x = None
        out[s["cls"]].append(dict(name=n, D=s["plain"], feat=F_(x, Ms, rh, sg, sg, None, [star(1.0, sg, K_TO_S, "sig_star")], xe=s["xe"])))
    return out

# KiDS (QX21 T1, verbatim logic)
B21 = os.path.join(DATA, "lensing_rar", "brouwer2021_rar")
kd = [np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_Colorbin_{i}.txt")) for i in (1, 2)]
gk = kd[0][:, 0]; Lk = kd[0][:, 1] / kd[0][:, 4]; Ek = kd[1][:, 1] / kd[1][:, 4]
cv = np.loadtxt(os.path.join(B21, "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt"))
C30 = (cv[:, 4] / cv[:, 6]).reshape(2, 2, 15, 15).transpose(0, 2, 1, 3).reshape(30, 30)
K1 = np.arange(8, 15)
def dstat(Lv, Ev):
    n = len(K1); J = np.zeros((n, 30))
    for k, i in enumerate(K1): J[k, i] = -1.0 / Lv[i]; J[k, 15 + i] = 1.0 / Ev[i]
    Cd = J @ C30 @ J.T / np.log(10) ** 2; dv = np.log10(Ev[K1] / Lv[K1]); w = np.linalg.solve(Cd, np.ones(n))
    return float(w @ dv / w.sum()), float(1 / np.sqrt(w.sum()))
DK, SK = dstat(Lk, Ek)
txt61 = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG61_kids_colour_split.out")).read()
rr61 = re.findall(r"K1 g_bar ([0-9.e+-]+): R_med late ([0-9.]+) early ([0-9.]+) Mpc \| late +([0-9.]+) \(L +([0-9.]+), S +[0-9.]+\) \| early +([0-9.]+) \(L +([0-9.]+), S", txt61)
assert len(rr61) == 7
DLAW = float(np.mean(np.log10(np.array([float(r[6]) for r in rr61]) / np.array([float(r[4]) for r in rr61]))))
STOT = float(np.hypot(SK, 0.05)); DX = DK - DLAW
GPC = 4.52e-30
def kids(a0):
    E_, L_ = [], []
    for k, i in enumerate(K1):
        Rl, Re_ = float(rr61[k][1]) * 1e6 * PC, float(rr61[k][2]) * 1e6 * PC
        gol, goe = 4 * GPC * Lk[i] * PC, 4 * GPC * Ek[i] * PC
        L_.append(F_(gk[i] / a0, None, Rl, math.sqrt(gol * Rl) / 1e3, None, None, [star(1.0, None, K_TO_S, "sig_late")]))
        E_.append(F_(gk[i] / a0, None, Re_, math.sqrt(goe * Re_) / 1e3, None, None, [star(1.0, None, K_TO_S, "sig_early")]))
    return E_, L_

GM_SUN = float(C6P["inputs"]["GM"]); AU = 149597870700.0
PLAN = {p: v[0] for p, v in C6P["inputs"]["planets"].items()}; R_CASSINI = 9.58 * AU
def ss_feat(a0, r): return F_(GM_SUN / r ** 2 / a0, 1.0, r, math.sqrt(GM_SUN / r) / 1e3, None, 0.0, [])

# ------------------------------------------------------------------ candidates
class Missing(Exception): pass
def need(feat, k):
    if feat.get(k) is None: raise Missing(k)
    return feat[k]
def alpha(s): return 10 ** (0.38 * math.log10(s / 200.0) - 0.06)
def b_imf(feat):
    b = 1.0
    for s in feat["stars"]:
        if s["share"] <= 0: continue
        if s["sigma"] is None: raise Missing(s["key"])
        b += s["share"] * (max(alpha(s["sigma"]) * s["rsk"], 1.0) - 1.0)
    return b
RZ_TAB = ((0.0, 1.0), (1.0, 0.91), (1.5, 0.94), (2.33, 0.91))
def rz_of(feat):
    if feat.get("rz") is not None: return feat["rz"]
    z = need(feat, "zf"); zz, rv = zip(*RZ_TAB); return float(np.interp(z, zz, rv))
def L0(f, a0): return lambda ft: dict(b=1.0, F=1.0, T=0.0)
def L1(f, a0): return lambda ft: dict(b=b_imf(ft), F=1.0, T=0.0)
def L2(f, a0):
    m = Q20[f]["vars"]["V2_vobs"]["fit"]
    def c(ft):
        v = need(ft, "v")
        return dict(delta=m["A"] * ((v / m["vmed"]) ** m["b"] if v > 0 else 0.0))
    return c
def F1(f, a0): return lambda ft: dict(b=1.0, F=1.0, T=ft["Tgeom"])
def F2(f, a0):
    def c(ft):
        rz = rz_of(ft); x = need(ft, "x"); gN = x * a0
        return dict(delta=math.log10(glaw(gN, rz * a0) / glaw(gN, a0)))
    return c
def F3(f, a0): return lambda ft: dict(b=b_imf(ft), F=1.0, T=ft["Tgeom"])
def NEWTON(f, a0): return lambda ft: dict(b=1.0, F=0.0, T=0.0)
CANDS = {"NEWTON": NEWTON} if MUT else {"L0": L0, "L1": L1, "L2": L2, "F1": F1, "F2": F2, "F3": F3}

def delta(c, ft, a0):
    o = c(ft)
    if "delta" in o: return o["delta"]
    if o["b"] == 1.0 and o["F"] == 1.0: return o["T"]
    gN = need(ft, "x") * a0; gNb = o["b"] * gN; gp = gNb + o["F"] * (glaw(gNb, a0) - gNb)
    return math.log10(gp / glaw(gN, a0)) + o["T"]
def F_ss(c, ft, a0):
    """multiplier on the non-Newtonian field at a Solar-System point (stable at x ~ 1e7)."""
    o = c(ft)
    if "delta" not in o and o["b"] == 1.0 and o["T"] == 0.0: return o["F"]
    d = delta(c, ft, a0); x = ft["x"]; n1 = nu_minus_1(x)            # g_law = g_N (1 + n1)
    return (math.expm1(d * math.log(10)) * (1 + n1) + n1) / n1
def filled(ft, fill):
    if not fill: return ft
    d = dict(ft); d["stars"] = [dict(s, sigma=(fill[s["key"]] if (s["sigma"] is None and s["key"] in fill) else s["sigma"])) for s in ft["stars"]]
    if "rz" in fill and d.get("zf") is None: d["rz"] = fill["rz"]
    return d

# ------------------------------------------------------------------ gates
def dl(c, pts, a0, fill=None): return np.array([delta(c, filled(p["feat"], fill), a0) for p in pts])
def g_sparc(c, B, a0, fill=None):
    res = np.array([p["D"] for p in B["S"]]) - dl(c, B["S"], a0, fill)
    Z = float(res.mean()); rms = float(np.sqrt((res ** 2).mean()))
    ok = abs(Z) <= 0.057 and rms <= B["rms_L0"] + 0.010
    return ok, dict(Z=Z, rms=rms, rms_line=B["rms_L0"] + 0.010)
def g_xcop(c, B, a0, fill=None):
    res = np.array([p["D"] for p in B["X"]]) - dl(c, B["X"], a0, fill); m = float(res.mean()); rms = float(np.sqrt((res ** 2).mean()))
    return (abs(m) <= 0.05 and rms <= 0.10), dict(mean=m, rms=rms)
def g_groups(c, B, a0, fill=None):
    o = {}
    for fst in (0, 1):
        npass = 0; med = []
        for gp in B["GR"][fst]:
            ok = True
            for p in gp["pts"]:
                r = p["D"] - delta(c, filled(p["feat"], fill), a0); med.append(r); ok &= abs(r) <= 2 * p["sl"]
            npass += ok
        o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)))
    return all(v["n_pass"] >= 16 for v in o.values()), o
def g_ell(c, B, a0, fill=None):
    res = np.array([p["D"] for p in B["E"]]) - dl(c, B["E"], a0, fill); m = float(res.mean())
    return abs(m) <= 0.15, dict(mean=m)
def g_udg(c, B, a0, fill=None):
    res = np.array([p["D"] for p in B["U"]]) - dl(c, B["U"], a0, fill); m = float(res.mean())
    return abs(m) <= 2 * B["sigU"], dict(mean=m, sigma_U=B["sigU"], z=m / B["sigU"])
def g_dsph(c, B, a0, fill=None):
    anchor = g_sparc(c, B, a0, fill)[1]["Z"]; rng = np.random.default_rng(21); o = {}; ok = True
    for cls in GRADED_D + ("MW ultra-faint", "M31 others"):
        pts = B["D"][cls]; v = np.array([p["D"] for p in pts]) - dl(c, pts, a0, fill); n = len(v)
        bs = np.median(v[rng.integers(0, n, (10000, n))], axis=1); lo, hi = np.percentile(bs, [2.5, 97.5])
        cont = bool(lo - anchor <= 0 <= hi - anchor)
        o[cls] = dict(N=n, median_minus_anchor=float(np.median(v) - anchor), ci=[float(lo - anchor), float(hi - anchor)], contains0=cont, graded=cls in GRADED_D)
        if cls in GRADED_D: ok &= cont
    return ok, o
def g_kids(c, B, a0, fill=None):
    Ee, Ll = B["K"]; dc = float(np.mean([delta(c, filled(e, fill), a0) - delta(c, filled(l, fill), a0) for e, l in zip(Ee, Ll)]))
    R = DX - dc
    return abs(R) < 2 * STOT, dict(D_cand=dc, R=R, z=R / STOT, sigma_tot=STOT)
def g_ss(c, B, a0, fill=None):
    f = B["f"]; Ls = LSTAR[f]; worst = 0.0; per = {}
    for p, r in PLAN.items():
        ratio = C6P["gate"][f]["G2b"][f"24|{p}"]["hedgehog_over_bound"] * (24.0 / Ls) ** 2
        Fp = F_ss(c, filled(ss_feat(a0, r), fill), a0); per[p] = dict(F=Fp, ratio=ratio, use=abs(Fp) * ratio); worst = max(worst, abs(Fp) * ratio)
    q2r = (24.0 / Ls) ** 3 / C6P["gate"][f]["summary"]["margin_Hees_min"]
    Fc = F_ss(c, filled(ss_feat(a0, R_CASSINI), fill), a0)
    return (worst <= 1 and abs(Fc) * q2r <= 1), dict(planets=per, worst_planet_use=worst, cassini_F=Fc, cassini_use=abs(Fc) * q2r)
GATES = [("G1 SPARC", g_sparc, [{"sig_bul": s, "sig_disc": 60} for s in (100, 150, 200)]),
         ("G2 X-COP", g_xcop, [{"sig_star": s} for s in (250, 300, 350)]),
         ("G3 groups", g_groups, [{"sig_star": s} for s in (200, 250, 300)]),
         ("G4 ellipticals", g_ell, []),
         ("G5 Coma UDGs", g_udg, []),
         ("G6 dSph classes", g_dsph, [{"sig_bul": 150, "sig_disc": 60}]),   # dSphs carry sigma; the fill only reaches the SPARC anchor
         ("G7 KiDS split", g_kids, [{"sig_early": s, "sig_late": 60} for s in (130, 170, 210)]),
         ("G8 Solar System", g_ss, [])]
RZ_FILLS = [{"rz": r} for r in (0.33, 0.91, 0.94, 1.00, 1.21)]

def run_gate(fn, c, B, a0, fills):
    try:
        ok, num = fn(c, B, a0); st = "PASS" if ok else "FAIL"; miss = None
    except Missing as e:
        st, num, miss = "NO VERDICT", None, str(e)
    br = None
    if st == "NO VERDICT":
        fl = fills if miss != "zf" else RZ_FILLS
        if miss == "zf" and fn is g_dsph: fl = RZ_FILLS
        outs = []
        for fill in fl:
            try: ok2, n2 = fn(c, B, a0, fill); outs.append(dict(fill=fill, ok=bool(ok2), num=n2))
            except Missing as e2: outs.append(dict(fill=fill, ok=None, missing=str(e2)))
        oks = [o["ok"] for o in outs]
        br = dict(reading=("PASS for all" if oks and all(o is True for o in oks) else ("FAIL for all" if oks and all(o is False for o in oks) else ("NONE (no bracket)" if not oks else "MIXED"))), runs=outs)
    return dict(status=st, num=num, missing=miss, bracket=br)

# ------------------------------------------------------------------ main
RES = dict(tag=TAG, criteria="e9464bc8ce", note="kappa = 1/2 FITTED; not theory closed", footings={}, KA={})
P(f"GB1 all-gates battery {'MUTATE (Newton)' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")
BATT = {}
for f, a0 in A0.items():
    S, E, X = build(f, a0); GRp = {0: groups_pts(a0, 0.0), 1: groups_pts(a0, 1.0)}; G5p = groups_pts(a0, 0.5)
    U = udgs(f, a0); D = dsphs(f, a0); K = kids(a0)
    st = R1[f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=D, K=K, sigU=sigU)
    B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    BATT[f] = B
    # ---------------- known answers
    cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]),
              G0=np.mean([p["D"] for g in GRp[0] for p in g["pts"]]), G1=np.mean([p["D"] for g in GRp[1] for p in g["pts"]]))
    d1 = max(abs(cm[k] - KA20[f][k]) for k in cm)
    um = float(np.mean([u["D"] for u in U])); d2 = abs(um - st["meanE"] / math.log(10))
    ka = dict(KA1=dict(class_means={k: float(v) for k, v in cm.items()}, G_fst05=float(np.mean([p["D"] for g in G5p for p in g["pts"]])), maxdiff=float(d1), ok=bool(d1 <= 1e-6)),
              KA2=dict(udg_mean=um, diff=d2, ok=bool(d2 <= 1e-9)))
    if not MUT:
        m26 = L1(f, a0); de = np.array([p["D"] for p in E]) - dl(m26, E, a0); d4 = abs(float(de.mean()) - Q26["foot"][f]["ellipticals"]["D_imf"])
        ka["KA4"] = dict(L1_ell=float(de.mean()), qx26=Q26["foot"][f]["ellipticals"]["D_imf"], diff=d4, ok=bool(d4 <= 1e-6))
        sp = float(np.mean(dl(L2(f, a0), S, a0))); d5 = abs(sp - Q20[f]["vars"]["V2_vobs"]["sparc_pred"])
        ka["KA5"] = dict(L2_sparc_pred=sp, qx20=Q20[f]["vars"]["V2_vobs"]["sparc_pred"], diff=d5, ok=bool(d5 <= 1e-9))
    nx = sum(1 for c_ in D.values() for p in c_ if p["feat"]["x"] is None)
    mars = C6P["gate"][f]["G2b"]["24|Mars"]["hedgehog_over_bound"]; hees = C6P["gate"][f]["summary"]["margin_Hees_min"]
    hq = {"canonical": 4.85e7, "alt": 5.70e7}[f]
    ka["KA6"] = dict(dsph_x_missing=nx, mars=mars, hees_margin=hees,
                     ok_as_frozen_1e4=bool(abs(mars / 0.1728 - 1) <= 1e-4 and abs(hees / hq - 1) <= 1e-4),
                     ok_rounding=bool(round(mars, 4) == 0.1728 and abs(hees - hq) <= 0.005e7), ok=bool(nx == 0 and round(mars, 4) == 0.1728 and abs(hees - hq) <= 0.005e7))
    RES["KA"][f] = ka
    P(f"[{f}] KA1 L0 class means X {cm['X']:+.6f} E {cm['E']:+.6f} S {cm['S']:+.6f} G0 {cm['G0']:+.6f} G1 {cm['G1']:+.6f}: max|d| {d1:.1e} -> {'PASS' if ka['KA1']['ok'] else 'FAIL'}")
    P(f"[{f}] KA2 UDG mean {um:+.6f} vs S1 {st['meanE']/math.log(10):+.6f}: |d| {d2:.1e} -> {'PASS' if ka['KA2']['ok'] else 'FAIL'}; sigma_U {sigU:.4f}")
    if not MUT:
        P(f"[{f}] KA4 L1 ellipticals {ka['KA4']['L1_ell']:+.6f} vs QX26 {ka['KA4']['qx26']:+.6f}: |d| {d4:.1e} -> {'PASS' if ka['KA4']['ok'] else 'FAIL'}")
        P(f"[{f}] KA5 L2 SPARC pred {sp:+.9f} vs QX20 {ka['KA5']['qx20']:+.9f}: |d| {d5:.1e} -> {'PASS' if ka['KA5']['ok'] else 'FAIL'}")
    P(f"[{f}] KA6 dSph x missing {nx}; C6P Mars {mars:.6f} (quoted 0.1728), Hees margin {hees:.4e} (quoted {hq:.3e}): 1e-4 as frozen {'PASS' if ka['KA6']['ok_as_frozen_1e4'] else 'FAIL'}, "
      f"to the quoted rounding {'PASS' if ka['KA6']['ok_rounding'] else 'FAIL'} -> {'PASS' if ka['KA6']['ok'] else 'FAIL'}")
    P(f"[{f}] SPARC L0 fixed-Upsilon rms {B['rms_L0']:.4f} -> G1 rms line {B['rms_L0'] + 0.01:.4f}")
# KA3 (footing-free + QX21's dSph replay)
rng = np.random.default_rng(21); d3 = [abs(DK - Q21["T1"]["D"]), abs(SK - Q21["T1"]["s_stat"]), abs(DLAW - Q21["T1"]["D_law"])]
for f in ("canonical", "alt"):
    ps = LW["footings"][f]["per_system"]
    for cls in DCLS:
        v = np.array([ps[n]["plain"] for n in ps if ps[n]["cls"] == cls])
        b = np.array([np.median(rng.choice(v, len(v))) for _ in range(10000)]); q = Q21["T2"][f][cls]
        d3 += [abs(float(np.median(v)) - q["median"]), abs(float(np.percentile(b, 2.5)) - q["ci95"][0]), abs(float(np.percentile(b, 97.5)) - q["ci95"][1])]
RES["KA"]["KA3"] = dict(maxdiff=float(max(d3)), ok=bool(max(d3) <= 1e-9), D=DK, s_stat=SK, D_law=DLAW, s_tot=STOT, DX=DX)
P(f"KA3 QX21: KiDS D {DK:+.6f} s_stat {SK:.6f} D_law {DLAW:+.6f} (D - D_law {DX:+.4f}, s_tot {STOT:.4f}); dSph medians + CIs (5 classes x 2 footings): max|d| {max(d3):.1e} -> {'PASS' if RES['KA']['KA3']['ok'] else 'FAIL'}")
kaok = RES["KA"]["KA3"]["ok"] and all(v["ok"] for f in A0 for v in RES["KA"][f].values())
RES["KA_all"] = bool(kaok)
if not kaok:
    P("KA FAIL: stop; nothing graded (fix the loader)."); RES["graded"] = False
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)

RES["graded"] = True; RES["cands"] = {}
def short(g, r):
    n = r["num"]
    if n is None: return f"NO VERDICT (needs {r['missing']}; bracket {r['bracket']['reading']})"
    if g.startswith("G1"): return f"Z {n['Z']:+.4f} rms {n['rms']:.4f} (line {n['rms_line']:.4f})"
    if g.startswith("G2"): return f"mean {n['mean']:+.4f} rms {n['rms']:.4f}"
    if g.startswith("G3"): return f"pass f*0 {n['fst0']['n_pass']}/20 f*1 {n['fst1']['n_pass']}/20 (med {n['fst0']['median_res']:+.3f}/{n['fst1']['median_res']:+.3f})"
    if g.startswith("G4"): return f"mean {n['mean']:+.4f}"
    if g.startswith("G5"): return f"mean {n['mean']:+.4f} ({n['z']:+.2f} sigma_U)"
    if g.startswith("G6"): return "; ".join(f"{k} {v['median_minus_anchor']:+.3f} [{v['ci'][0]:+.3f},{v['ci'][1]:+.3f}]" for k, v in n.items() if v["graded"])
    if g.startswith("G7"): return f"D_cand {n['D_cand']:+.4f} R {n['R']:+.4f} ({n['z']:+.2f} sigma)"
    if g.startswith("G8"): return f"worst planet use {n['worst_planet_use']:.3g}, Cassini use {n['cassini_use']:.3g}"
for cn, mk in CANDS.items():
    RES["cands"][cn] = {}
    for f, a0 in A0.items():
        c = mk(f, a0); B = BATT[f]; row = {}
        for gname, fn, fills in GATES:
            r = run_gate(fn, c, B, a0, fills); row[gname] = r
            P(f"[{f}] {cn:6s} {gname:17s} {r['status']:10s} {short(gname, r)}")
        row["G9 CMB lensing + growth"] = dict(status="NOT EVALUATED")
        RES["cands"][cn][f] = row
    sts = [RES["cands"][cn][f][g]["status"] for f in A0 for g, _, _ in GATES]
    fails = sorted({g for f in A0 for g, _, _ in GATES if RES["cands"][cn][f][g]["status"] == "FAIL"})
    nvs = sorted({g for f in A0 for g, _, _ in GATES if RES["cands"][cn][f][g]["status"] == "NO VERDICT"})
    lab = ("PASSES ALL STATIC GATES" if all(s == "PASS" for s in sts) else
           (f"FAIL ({', '.join(x.split()[0] for x in fails)})" + (f"; NO VERDICT ({', '.join(x.split()[0] for x in nvs)})" if nvs else "")) if fails else
           f"NOT GRADABLE ({', '.join(x.split()[0] for x in nvs)})")
    RES["cands"][cn]["label"] = lab; P(f"LABEL {cn}: {lab}")
if MUT:
    bites = RES["cands"]["NEWTON"]["label"] != "PASSES ALL STATIC GATES" and all(RES["cands"]["NEWTON"][f]["G1 SPARC"]["status"] == "FAIL" for f in A0)
    RES["MUTATE_bites"] = bool(bites); P(f"MUTATE Newton: {'FAILS the battery (G1 fails on both footings) -> BITES' if bites else 'NO BITE'}")
else:
    win = [c for c in CANDS if RES["cands"][c]["label"] == "PASSES ALL STATIC GATES"]
    RES["winners"] = win; P(f"PASSES ALL STATIC GATES: {', '.join(win) if win else 'none'}. G9 (CMB lensing + growth) NOT EVALUATED.")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (not MUT or RES["MUTATE_bites"]) else 1)
