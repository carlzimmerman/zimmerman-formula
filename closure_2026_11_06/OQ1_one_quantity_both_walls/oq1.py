#!/usr/bin/env python3
"""OQ1 (criteria 3d8e38ffb2): can one action-native scalar, q = Sigma / rho_DE (the AC2q charge, Sigma = F rho_ph + 2X),
set the extra gravity the hot classes need AND switch the law off on the linear web?
    nice -n 15 python3 oq1.py      -> oq1.json / oq1.out ; oq1_MUTATE_M1.json, oq1_MUTATE_M2.json, oq1_MUTATE_M3.json
Read-only reuse: GB1 (gb1.py, executed up to its main block: QX5 loaders, feature builders, b_imf, C6P), SV5 (sv5_web.py
module: CLASS realisation, projection, hosts). One thread. Preemptible: SIGTERM after the web pass writes oq1_ckpt.npz and exits 3.
kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing."""
import os, sys, json, math, signal, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); RB = os.path.join(REPO, "rebuild_2026_10_22")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("flag", True))
CKPT = os.path.join(HERE, "oq1_ckpt.npz")

# ------------------------------------------------------------------ GB1 (read-only): everything above its main block
GB = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); sgb = open(GB).read()
cut = sgb.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GB, "__name__": "gb1_lib"}; _a = sys.argv; sys.argv = [GB]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(sgb[:cut], GB, "exec"), NS)
sys.argv = _a
G, MS, KPC, PC, CC = NS["G"], NS["MS"], NS["KPC"], NS["PC"], NS["C"]
A0 = NS["A0"]; glaw = NS["glaw"]; nu_minus_1 = NS["nu_minus_1"]; b_imf = NS["b_imf"]; filled = NS["filled"]
LSTAR = NS["LSTAR"]; C6P = NS["C6P"]; PLAN = NS["PLAN"]; GM_SUN = NS["GM_SUN"]; AU = NS["AU"]; R_CASSINI = NS["R_CASSINI"]
Q26 = NS["Q26"]; KA20 = NS["KA20"]; R1S = NS["R1"]; X1R = NS["X1R"]
def rho_de(a0): return 4 * a0 ** 2 / (G * CC ** 2)        # = a0^2 / (kappa^2 c^2 G), kappa 1/2 (QX5, SV5)
FILL = {"sig_bul": 150, "sig_disc": 60, "sig_star": None}  # GB1's bracket middles (post-freeze fill, disclosed)
FILL_STAR = {"xcop": 300, "groups": 250}

# ------------------------------------------------------------------ phantom density of the law, spherical (SV5 iter_2 host formula)
def phi_a(u):  # g_law(u) - u in a0 units, stable at large u
    u = np.asarray(u, float); return u * np.vectorize(nu_minus_1)(u)
def rho_ph_local(x, s, r, a0, eps=1e-3):
    """x = b g_N / a0 at r; s = dlnM/dlnr (local power law). rho_ph = d/dr[r^2 (g - g_N)] / (4 pi G r^2)."""
    rp, rm = r * (1 + eps), r * (1 - eps)
    h = lambda rr: rr ** 2 * phi_a(x * (rr / r) ** (s - 2)) * a0
    return float((h(rp) - h(rm)) / (rp - rm) / (4 * math.pi * G * r ** 2))
def rho_b_local(x, s, r, a0): return x * a0 * s / (4 * math.pi * G * r)   # dM/dr / (4 pi r^2) with M = x a0 r^2/G
def tidal(x, s, r, a0):
    gN = x * a0; t = 4 * math.pi * G * rho_b_local(x, s, r, a0); d2 = t - 2 * gN / r
    e1, e2 = d2 - t / 3, gN / r - t / 3; return math.sqrt(e1 * e1 + 2 * e2 * e2)

# ------------------------------------------------------------------ static classes: per-point records
def xcop_profiles():
    from astropy.io import fits
    D = os.path.join(REPO, "real_research", "data", "xcop"); out = {}
    for name in sorted(os.listdir(D)):
        p_ = os.path.join(D, name)
        if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))): continue
        with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        out[name] = (np.array(gas["RADIUS"], float) * rg500, np.array(gas["MGAS"], float), np.array(st["RADIUS"], float), np.array(st["MSTAR"], float))
    return out
XPROF = xcop_profiles()
_li = NS["NS"]["li"]   # QX5's own log interpolation
def mb_x(name, rk):
    gr, gM, sr, sM = XPROF[name]; return _li(gr, gM, rk) + _li(sr, sM, rk)

def rec(cls, D, x, b, r, s, a0, err=None, **kw):
    xb = b * x; rd = rho_de(a0)
    d = dict(cls=cls, D=float(D), x=float(x), b=float(b), r=float(r), s=float(s), err=err,
             xb=float(xb), ph=float(phi_a(xb)), gl=float(glaw(x, 1.0)), rph=rho_ph_local(xb, s, r, a0) / rd, qb=rho_b_local(xb, s, r, a0) / rd, qt=tidal(xb, s, r, a0) / (4 * math.pi * G * rd))
    d.update(kw); return d

def points(f, a0, fst):
    S, E, X = NS["build"](f, a0); R = []
    # SPARC: M = vb2 r / G, s from the galaxy's own points
    k = 0
    for g in NS["SP"]:
        r = g["R"]; lm = np.log(g["vb2"] * r); s_arr = np.gradient(lm, np.log(r)) if len(r) > 1 else np.full(len(r), 1.0)
        for i in range(len(r)):
            p = S[k]; k += 1; b = b_imf(filled(p["feat"], {"sig_bul": FILL["sig_bul"], "sig_disc": FILL["sig_disc"]}))
            R.append(rec("SPARC", p["D"], p["feat"]["x"], b, r[i], s_arr[i], a0, err=2 * g["eV"][i] / g["V"][i] / math.log(10), gal=g["name"]))
    assert k == len(S)
    # ellipticals (Humphrey, Kroupa; L1 b with the galaxy's sigma_e)
    for e, p in zip([e for e in NS["EL"] for _ in (2, 4, 8)], E):
        a = e["Re"] / 1.8153; rk = p["feat"]["r"] / KPC; s = 2 * a / (rk + a)
        R.append(rec("ellipticals", p["D"], p["feat"]["x"], b_imf(p["feat"]), p["feat"]["r"], s, a0, err=None, gal=e["name"]))
    # X-COP (spherical gas + BCG; b with the X-COP sigma bracket middle)
    for z, p in zip(NS["XC"], X):
        rk = z["r_kpc"]; s = math.log(mb_x(z["name"], rk * 1.05) / mb_x(z["name"], rk / 1.05)) / math.log(1.05 ** 2)
        b = b_imf(filled(p["feat"], {"sig_star": FILL_STAR["xcop"]}))
        R.append(rec("X-COP", p["D"], p["feat"]["x"], b, p["feat"]["r"], s, a0, err=z["eM"] / z["M_obs"] / math.log(10), gal=z["name"]))
    # groups (power-law rho_b between R2500 and R500, frozen construction)
    for gp, gq in zip(NS["GR"], NS["groups_pts"](a0, float(fst))):
        s = math.log(gp["g5"] / gp["pts"][0]["M_gas"]) / math.log(gp["R5"] / gp["R25"])
        for p in gq["pts"]:
            b = b_imf(filled(p["feat"], {"sig_star": FILL_STAR["groups"]}))
            R.append(rec("groups", p["D"], p["feat"]["x"], b, p["feat"]["r"], s, a0, err=p["sl"], sl=p["sl"], gal=gq["name"]))
    # Coma UDGs (Plummer, r_h = 4/3 Re as GB1)
    sP = 3.0 / (1.0 + 1.305 ** 2)
    for u, row in zip(NS["udgs"](f, a0), [r for r in NS["UROWS"] if r["footing"] == f]):
        R.append(rec("Coma UDGs", u["D"], u["feat"]["x"], b_imf(u["feat"]), u["feat"]["r"], sP, a0,
                     err=2 * float(row["esig"]) / float(row["sigma"]) / math.log(10), gal=row["name"]))
    # dSphs: bright M31 and LG field (Plummer at r_h, M fixed by GB1's inverted x)
    Dd = NS["dsphs"](f, a0); nmiss = 0
    for cls in ("bright M31", "LG field"):
        for p in Dd[cls]:
            if p["feat"]["x"] is None: nmiss += 1; continue
            xr = X1R[(f, p["name"])]
            R.append(rec(cls, p["D"], p["feat"]["x"], b_imf(p["feat"]), p["feat"]["r"], sP, a0, err=float(xr["sdMC[Newton]"]), gal=p["name"]))
    # Solar System: the Sun's own field at Earth, Mars, Saturn and 9.58 AU, plus the Galaxy at the Sun (SV5 C4)
    gal_x = G * 6e10 * MS / (8.2 * KPC) ** 2 / a0; gal_rph = rho_ph_local(gal_x, 0.0, 8.2 * KPC, a0) / rho_de(a0)
    Ls = LSTAR[f]
    for pn, rr in list(PLAN.items()) + [("Cassini 9.58 AU", R_CASSINI)]:
        if pn.startswith("Cassini"): use1 = (24.0 / Ls) ** 3 / C6P["gate"][f]["summary"]["margin_Hees_min"]
        else: use1 = C6P["gate"][f]["G2b"][f"24|{pn}"]["hedgehog_over_bound"] * (24.0 / Ls) ** 2
        d = rec("Solar System", 0.0, GM_SUN / rr ** 2 / a0, 1.0, rr, 0.0, a0, gal=pn, use_at_F1=use1)
        d["rph_sun"] = d["rph"]; d["rph"] = d["rph"] + gal_rph; d["rph_gal"] = gal_rph; R.append(d)
    return R, nmiss

# ------------------------------------------------------------------ per-point algebra
def Dpred(p, F):  # predicted offset from the plain law
    xb = p["b"] * p["x"]; return math.log10((xb + F * float(phi_a(xb))) / glaw(p["x"], 1.0))
def Finv(p, d):   # F at which the predicted offset equals d
    xb = p["b"] * p["x"]; return (10 ** d * glaw(p["x"], 1.0) - xb) / float(phi_a(xb))
def Fneed(p): return Finv(p, p["D"])
FHI = 1e9
def solve_mono(fun, target):
    """fun(F) decreasing in F; returns F with fun = target in [0, FHI] (0 or inf at the ends)."""
    if fun(0.0) <= target: return 0.0
    if fun(FHI) > target: return math.inf
    lo, hi = 0.0, 1.0
    while fun(hi) > target: lo, hi = hi, hi * 4
    for _ in range(80):
        m = 0.5 * (lo + hi); lo, hi = (m, hi) if fun(m) > target else (lo, m)
    return 0.5 * (lo + hi)

def arr(pts): return (np.array([p["D"] for p in pts]), np.array([p["xb"] for p in pts]), np.array([p["ph"] for p in pts]), np.array([p["gl"] for p in pts]))
def res_vec(A, F): D, xb, ph, gl = A; return D - np.log10((xb + F * ph) / gl)
def mean_res_fun(pts):
    A = arr(pts)
    def f(F): return float(np.mean(res_vec(A, F)))
    return f
def band_mean(pts, c):  # {F >= 0 : |mean residual| <= c}
    f = mean_res_fun(pts); lo = solve_mono(f, c); hi = solve_mono(f, -c)
    return [(lo, hi)] if lo <= hi else []
BOOT = {}
def band_lg(pts, anchor):
    n = len(pts); key = n
    if key not in BOOT: BOOT[key] = np.random.default_rng(21).integers(0, n, (10000, n))
    ix = BOOT[key]
    A = arr(pts)
    def ci(F):
        v = res_vec(A, F); bs = np.median(v[ix], axis=1); return np.percentile(bs, [2.5, 97.5])
    lo = solve_mono(lambda F: ci(F)[0] - anchor, 0.0); hi = solve_mono(lambda F: ci(F)[1] - anchor, 0.0)
    return [(lo, hi)] if lo <= hi else []
def band_groups(pts):  # >= 80 % (G3's 16 of 20) of the bin's group points inside 2 sigma_log
    iv = []
    for p in pts:
        a, b = max(Finv(p, p["D"] - 2 * p["sl"]), 0.0), Finv(p, p["D"] + 2 * p["sl"])
        if b >= a: iv.append((a, b))
    need = math.ceil(0.8 * len(pts)); ev = sorted({0.0} | {a for a, _ in iv} | {b for _, b in iv})
    out = []
    for i, e in enumerate(ev):
        cands = [e] + ([0.5 * (e + ev[i + 1])] if i + 1 < len(ev) else [])
        for F in cands:
            if sum(1 for a, b in iv if a <= F <= b) >= need:
                if out and out[-1][1] >= F - 1e-12 * max(1, F): out[-1] = (out[-1][0], F)
                else: out.append((F, F))
    return out
def band_2sig(pts, sig_cls, n_cls):
    fn = np.array([Fneed(p) for p in pts]); s = sig_cls * math.sqrt(n_cls / len(pts)); m = float(fn.mean())
    lo, hi = max(m - 2 * s, 0.0), m + 2 * s
    return [(lo, hi)] if hi >= lo else []

def class_band(cls, pts, ctx):
    if cls == "SPARC": return band_mean(pts, 0.057)
    if cls == "X-COP": return band_mean(pts, 0.05)
    if cls == "ellipticals": return band_mean(pts, 0.15)
    if cls == "Coma UDGs": return band_mean(pts, 2 * ctx["sigU"])
    if cls == "LG field": return band_lg(pts, ctx["anchor"])
    if cls == "groups": return band_groups(pts)
    if cls == "bright M31": return band_2sig(pts, ctx["sigM31"], ctx["nM31"])
    if cls == "Solar System":
        if ctx.get("planted_ss"): return [(min(p["Ftrue"] for p in pts) * 0.99, max(p["Ftrue"] for p in pts) * 1.01)]
        return [(0.0, min(1.0 / p["use_at_F1"] for p in pts))]
    if cls == "web": return [(0.0, ctx["Fweb_max"])]
    raise KeyError(cls)

def intersect(sets):
    cur = [(0.0, math.inf)]
    for s in sets:
        nxt = []
        for a, b in cur:
            for c, d in s:
                lo, hi = max(a, c), min(b, d)
                if lo <= hi: nxt.append((lo, hi))
        cur = nxt
    return cur
def project_F(F, s):
    if not s: return F
    best = min(s, key=lambda iv: 0.0 if iv[0] <= F <= iv[1] else min(abs(F - iv[0]), abs(F - iv[1])))
    return min(max(F, best[0]), best[1])
def gap_dex(sets):
    los = [min(a for a, _ in s) for s in sets if s]; his = [max(b for _, b in s) for s in sets if s]
    if not los: return None
    L, H = max(los), min(his)
    return (math.log10(L / H) if H > 0 else math.inf) if L > H else 0.0
BW = 0.2
def bin_of(q): return int(math.floor(math.log10(q) / BW)) if q > 0 else None

def s1_run(pts, ctx, F0, web_hist):
    """section 3 iteration + S1. Each point's F is moved to the nearest value its class allows in its current bin."""
    n = len(pts); F = np.full(n, float(F0)); cls = [p["cls"] for p in pts]; rph = np.array([p["rph"] for p in pts])
    q = F * rph + 2.0; it = 0; conv = False; cyc = False; hist = []; memo = {}
    def cband(c, ix):
        k = (c, tuple(ix))
        if k not in memo: memo[k] = class_band(c, [pts[i] for i in ix], ctx)
        return memo[k]
    for it in range(1, 201):
        bins = [bin_of(x) for x in q]; groups = {}
        for i, (c, b) in enumerate(zip(cls, bins)):
            if b is not None: groups.setdefault((c, b), []).append(i)
        bands = {key: cband(key[0], ix) for key, ix in groups.items()}
        Fn = F.copy()
        for key, ix in groups.items():
            for i in ix: Fn[i] = project_F(F[i], bands[key])
        qn = Fn * rph + 2.0
        ok = (qn > 0) & (q > 0); dq = float(np.max(np.abs(np.log10(qn[ok]) - np.log10(q[ok])))) if ok.any() else 0.0
        F, q = Fn, qn; sig = tuple(np.round(np.log10(np.maximum(q, 1e-300)), 6)); cyc = cyc or (sig in hist); hist.append(sig)
        if dq < 1e-4: conv = True; break
    # final bins and S1
    bins = [bin_of(x) for x in q]; groups = {}
    for i, (c, b) in enumerate(zip(cls, bins)):
        if b is not None: groups.setdefault((c, b), []).append(i)
    bands = {key: cband(key[0], ix) for key, ix in groups.items()}
    wF = ctx["Fweb_max"] if F0 > 0 else 0.0
    wb = web_hist(wF) if web_hist else {}
    allb = sorted({b for (_, b) in groups} | set(wb))
    table = []; dead = []
    for b in allb:
        members = {c: bands[(c, b)] for (c, bb) in groups if bb == b}
        if b in wb: members["web"] = class_band("web", None, ctx)
        inter = intersect(list(members.values())) if len(members) >= 2 else None
        row = dict(bin=b, log10q=[round(b * BW, 3), round((b + 1) * BW, 3)],
                   classes={c: dict(n=(len(groups[(c, b)]) if c != "web" else wb[b]["cells"]), band=v,
                                    **({"mass_frac": wb[b]["mass_frac"]} if c == "web" else {})) for c, v in members.items()})
        if len(members) >= 2:
            row["intersection"] = inter; row["empty"] = not inter
            if not inter:
                row["gap_dex"] = gap_dex(list(members.values()))
                # which pair conflicts worst
                cl = list(members); worst = None
                for i in range(len(cl)):
                    for j in range(i + 1, len(cl)):
                        if not intersect([members[cl[i]], members[cl[j]]]):
                            g_ = gap_dex([members[cl[i]], members[cl[j]]])
                            if worst is None or (g_ or 0) > worst[2]: worst = (cl[i], cl[j], g_ or 0)
                row["worst_pair"] = worst; dead.append(row)
        table.append(row)
    qr = {}
    for c in sorted(set(cls)):
        v = q[[i for i in range(n) if cls[i] == c]]; v = v[v > 0]
        qr[c] = dict(n=int(len(v)), log10q_min=float(np.log10(v.min())) if len(v) else None, log10q_med=float(np.median(np.log10(v))) if len(v) else None,
                     log10q_max=float(np.log10(v.max())) if len(v) else None, n_q_le0=int(sum(1 for i in range(n) if cls[i] == c and q[i] <= 0)))
    return dict(F0=F0, iterations=it, converged=conv, cycled=bool(cyc), q_range=qr, bins=table, dead_bins=dead, S1_holds=not dead,
                web_F=wF, q=q.tolist(), F=F.tolist())

# ------------------------------------------------------------------ S3 (leave-one-class-out), used by M1 and if S1 holds
def s3_run(pts, res, ctx):
    q = np.array(res["q"]); cls = np.array([p["cls"] for p in pts]); out = {}
    for k in sorted(set(cls)):
        nodes = []
        for row in res["bins"]:
            m = {c: v["band"] for c, v in row["classes"].items() if c != k}
            if not m: continue
            it = intersect(list(m.values()))
            if not it: continue
            lo, hi = it[0][0], it[-1][1]; mid = lo if not math.isfinite(hi) else 0.5 * (lo + hi)
            nodes.append(((row["bin"] + 0.5) * BW, mid))
        rows = [r for r in res["bins"] if k in r["classes"]]; graded = []; uncon = 0
        if len(nodes) < 1: out[k] = dict(status="UNCONSTRAINED BY OTHERS", bins=[]); continue
        xs, ys = np.array([a for a, _ in nodes]), np.array([b for _, b in nodes])
        for r in rows:
            ix = [i for i in range(len(pts)) if cls[i] == k and bin_of(q[i]) == r["bin"]]
            lq = float(np.median(np.log10(q[ix]))) if ix else (r["bin"] + 0.5) * BW
            dist = max(xs.min() - lq, lq - xs.max(), 0.0)
            if dist > 0.5: uncon += 1; graded.append(dict(bin=r["bin"], status="UNCONSTRAINED", dist_dex=dist)); continue
            Fp = float(np.interp(lq, xs, ys)) if len(xs) > 1 else float(ys[0])
            band = r["classes"][k]["band"]; inside = any(a <= Fp <= b for a, b in band)
            graded.append(dict(bin=r["bin"], F_pred=Fp, band=band, inside=bool(inside), dist_dex=dist))
        gr = [g for g in graded if "inside" in g]
        st = ("UNCONSTRAINED BY OTHERS" if not gr else ("PASS" if all(g["inside"] for g in gr) else "FAIL"))
        out[k] = dict(status=st, n_bins=len(rows), n_unconstrained=uncon, bins=graded)
    HOT = ("X-COP", "groups", "ellipticals", "Coma UDGs", "bright M31")
    holds = all(v["status"] == "PASS" for v in out.values()) and not any(out.get(h, {}).get("status") == "UNCONSTRAINED BY OTHERS" for h in HOT)
    return dict(per_class=out, S3_holds=bool(holds))

# ------------------------------------------------------------------ the web (SV5 iter_1 machinery, F-quadratic)
def web_pass(f, a0, W, dV, SV):
    np_ = np; ZG = SV.ZG; ZW = [0.25, 0.5, 1.0, 2.0, 3.0]; Hs = SV.H0s; Om = SV.Om; kSI = 1.0 / SV.MPC
    rd = 4 * a0 ** 2 / (SV.G * SV.CC ** 2); A = []; cells = {}; frac = {}; side = {}
    Sst = min(x["rho_ph_rta"] for x in SV.hosts(a0))
    for z in ZG:
        dk, _ = SV.delta_k(W, dV, z); a = 1 / (1 + z)
        phik = -1.5 * Hs ** 2 * Om * dk / (a * SV.K2 * kSI ** 2); phik[0, 0, 0] = 0
        gs = [np.real(np.fft.ifftn(-1j * Kc * kSI * phik)) / a for Kc in (SV.KX, SV.KY, SV.KZ)]
        gn = np.sqrt(gs[0] ** 2 + gs[1] ** 2 + gs[2] ** 2); n1 = SV.nu(gn / a0) - 1.0
        Nk = [np.fft.fftn(g) for g in gs]; divN = SV.KX * Nk[0] + SV.KY * Nk[1] + SV.KZ * Nk[2]; del Nk
        Wk = [np.fft.fftn(n1 * g) for g in gs]; divW = SV.KX * Wk[0] + SV.KY * Wk[1] + SV.KZ * Wk[2]; del Wk
        A.append((SV.shell_mean(np.abs(divN) ** 2), SV.shell_mean(np.real(np.conj(divN) * divW)), SV.shell_mean(np.abs(divW) ** 2)))
        rho = -np.real(np.fft.ifftn(1j * divW)) * kSI / a / (4 * np.pi * SV.G); del divW, divN
        wt = np.maximum(1 + np.real(np.fft.ifftn(dk)), 0.0)
        frac[str(z)] = float((wt * (rho >= Sst)).sum() / wt.sum())
        if z in ZW:
            cells[z] = ((rho / rd).astype(np.float32), wt.astype(np.float32))
            # side tables (no label): q_b = rho_b / rho_DE, q_t = |E| / (4 pi G rho_DE)
            rhob = SV.ob / SV.h ** 2 * 3 * Hs ** 2 / (8 * np.pi * SV.G) * (1 + z) ** 3 * wt
            Tk = {}; trace = 0
            for i_, Ki in enumerate((SV.KX, SV.KY, SV.KZ)):
                for j_, Kj in enumerate((SV.KX, SV.KY, SV.KZ)):
                    if j_ < i_: continue
                    Tk[(i_, j_)] = np.real(np.fft.ifftn(-Ki * Kj * kSI ** 2 * phik)) / a ** 2
            tr = (Tk[(0, 0)] + Tk[(1, 1)] + Tk[(2, 2)]) / 3; e2 = 0
            for (i_, j_), T in Tk.items(): e2 = e2 + (1 if i_ == j_ else 2) * (T - (tr if i_ == j_ else 0)) ** 2
            qt = np.sqrt(e2) / (4 * np.pi * SV.G * rd); del Tk, e2
            side[str(z)] = dict(q_b_pct=np.percentile(rhob / rd, [5, 50, 95]).tolist(), q_t_pct=np.percentile(qt, [5, 50, 95]).tolist())
        del gs, gn, n1, rho, wt, dk, phik
    def r_of(F):
        Bz = [(a0_ + 2 * F * a1 + F * F * a2) / a0_ for a0_, a1, a2 in A]; pr = SV.project(Bz); return pr["r"], pr["dchi2"]
    r1, d1 = r_of(1.0)
    lo, hi = 0.0, 1.0
    for _ in range(50):
        m = 0.5 * (lo + hi); lo, hi = (m, hi) if r_of(m)[0] <= 1 + 3 * SV.sigA else (lo, m)
    Fmax = lo; rmax = r_of(Fmax)
    return dict(r_F1=r1, dchi2_F1=d1, Fweb_max=Fmax, r_at_Fmax=rmax[0], dchi2_at_Fmax=rmax[1], r_line=1 + 3 * SV.sigA,
                Sigma_star_over_rhoDE=Sst / rd, frac=frac, side=side), cells
def web_hist_factory(cells):
    def h(F):
        out = {}
        for z, (rp, wt) in cells.items():
            q = F * rp.astype(np.float64) + 2.0; ok = q > 0; b = np.floor(np.log10(q[ok]) / BW).astype(int); w = wt[ok]
            tot = float(wt.sum())
            for bb in np.unique(b):
                m = b == bb; e = out.setdefault(int(bb), dict(cells=0, mass=0.0, mass_frac=0.0))
                e["cells"] += int(m.sum()); e["mass"] += float(w[m].sum()); e["mass_frac"] += float(w[m].sum()) / tot / len(cells)
        return out
    return h

# ------------------------------------------------------------------ planted twins (M1, M2)
HOT_PLANT = ("X-COP", "groups", "ellipticals")
def plant(pts, qmed, step):
    rng = np.random.default_rng(21); out = []
    for p in pts:
        d = dict(p); r = p["rph"]
        if r > 0:
            sq = (3 * r / math.sqrt(qmed) + math.sqrt(9 * r * r / qmed + 4 * (2 + r))) / 2; qq = sq * sq; Ft = (qq - 2) / r
        else:
            Ft = 1 + 3 * math.sqrt(2 / qmed)
        d["Ftrue"] = Ft
        if p["cls"] != "Solar System":
            e = p["err"] if p["err"] is not None else 0.05
            d["D"] = Dpred(p, Ft) + rng.normal(0.0, e) + (0.3 if (step and p["cls"] in HOT_PLANT) else 0.0)
        out.append(d)
    return out

def ctx_for(pts, f, Fweb, planted=False):
    sp = [p for p in pts if p["cls"] == "SPARC"]; band = band_mean(sp, 0.057)
    Fmid = (0.5 * (band[0][0] + band[0][1]) if band and math.isfinite(band[0][1]) else 1.0)
    anchor = mean_res_fun(sp)(Fmid)
    m31 = [p for p in pts if p["cls"] == "bright M31"]; fn = np.array([Fneed(p) for p in m31])
    bs = fn[np.random.default_rng(21).integers(0, len(fn), (10000, len(fn)))].mean(axis=1)
    st = R1S[f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    return dict(anchor=anchor, Fmid_sparc=Fmid, sparc_band_all=band, sigM31=float(bs.std()), nM31=len(m31), sigU=sigU, Fweb_max=Fweb, planted_ss=planted)

def pct3(v):
    v = [x for x in v if x > 0]
    return np.percentile(np.log10(v), [0, 50, 100]).tolist() if v else None
def label_of(s1s, s3=None):
    if any(not r["S1_holds"] for r in s1s): return "DEAD"
    return "S1 HOLDS (S2 owed)"


def finalize(RES, MUTS):
    """Frozen section 6: M1 must find the planted law, else the run says NO VERDICT. Margins vs the planted-law null reported."""
    m = RES["MUTATE"]; RES["S1_reading"] = RES["label"]
    if not m["M1_power_to_find"]: lab = "NO VERDICT (M1 planted law not recovered: S1 reports false conflicts)"
    elif not m["M2_power_to_kill"]: lab = RES["label"] + " (M2 did not bite)"
    else: lab = RES["label"]
    RES["label_as_frozen"] = lab; marg = {}
    for f in RES["foot"]:
        null = max([max([d["gap_dex"] or 0 for d in r["dead_bins"]] or [0]) for k, v in MUTS["M1"].items() if k.startswith(f + "|") for r in v["runs"].values()])
        per = {}
        for fst in ("fst0", "fst1"):
            for s0, r in RES["foot"][f][fst].items():
                g = [d for d in r["dead_bins"] if (d["gap_dex"] or 0) > null]
                per[f"{fst}|F0={s0}"] = dict(n_dead=len(r["dead_bins"]), n_above_null=len(g), max_gap=max([d["gap_dex"] or 0 for d in r["dead_bins"]] or [0]),
                                             above_null=[dict(log10q=d["log10q"], gap_dex=d["gap_dex"], pair=d["worst_pair"][:2]) for d in g])
        hosts_min = min(min(v["log10q_min"] for c, v in r["q_range"].items() if c not in ("Solar System",) and v["log10q_min"] is not None and v["log10q_min"] > 0.31)
                        for fst in ("fst0", "fst1") for r in RES["foot"][f][fst].values())
        marg[f] = dict(M1_null_max_gap_dex=null, runs=per, all_runs_have_conflict_above_null=all(v["n_above_null"] > 0 for v in per.values()),
                       web_bins=sorted({b["bin"] for fst in ("fst0", "fst1") for r in RES["foot"][f][fst].values() for b in r["bins"] if "web" in b["classes"]}),
                       lowest_host_log10q_above_floor=hosts_min)
    RES["post_freeze_margin_reading"] = dict(note="reported, not a label: conflicts wider than every planted-law false conflict of the same footing", foot=marg)
    return RES

# ------------------------------------------------------------------ main
if __name__ == "__main__" and "--label" in sys.argv:
    RES = json.load(open(os.path.join(HERE, "oq1.json"))); MUTS = {M: json.load(open(os.path.join(HERE, f"oq1_MUTATE_{M}.json")))["runs"] for M in ("M1", "M2", "M3")}
    OUT = open(os.path.join(HERE, "oq1.out")).read().rstrip("\n").split("\n")
    while OUT and (OUT[-1].startswith("LABEL AS FROZEN") or OUT[-1].startswith("  margin") or OUT[-1].startswith("kappa")): OUT.pop()
    RES = finalize(RES, MUTS)
    P(f"LABEL AS FROZEN: {RES['label_as_frozen']}; S1 reading {RES['S1_reading']}")
    for f, v in RES["post_freeze_margin_reading"]["foot"].items():
        P(f"  margin [{f}] M1 null max gap {v['M1_null_max_gap_dex']:.3f} dex; runs with a conflict above it: {sum(1 for x in v['runs'].values() if x['n_above_null'])}/{len(v['runs'])}; "
          f"max gap {max(x['max_gap'] for x in v['runs'].values()):.3f}; web bins {v['web_bins']}; lowest host log10 q {v['lowest_host_log10q_above_floor']:.2f}")
    P("kappa = 1/2 FITTED; not theory closed.")
    json.dump(RES, open(os.path.join(HERE, "oq1.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "oq1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)

if __name__ == "__main__":
    P("OQ1 one quantity, both walls. kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing.")
    RES = dict(lane="OQ1", criteria="3d8e38ffb2", note="kappa = 1/2 FITTED; not theory closed", KA={}, foot={})
    # ---------------- KA1, KA2 (GB1 machinery)
    for f, a0 in A0.items():
        S, E, X = NS["build"](f, a0); GRp = {0: NS["groups_pts"](a0, 0.0), 1: NS["groups_pts"](a0, 1.0)}
        cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S]))
        d1 = max(abs(cm[k] - KA20[f][k]) for k in cm)
        e_l1 = float(np.mean([p["D"] - NS["delta"](NS["L1"](f, a0), p["feat"], a0) for p in E])); d2 = abs(e_l1 - Q26["foot"][f]["ellipticals"]["D_imf"])
        RES["KA"][f] = dict(KA1=dict(means={k: float(v) for k, v in cm.items()}, maxdiff=float(d1), ok=bool(d1 <= 1e-6)),
                            KA2=dict(L1_ell=e_l1, qx26=Q26["foot"][f]["ellipticals"]["D_imf"], diff=d2, ok=bool(d2 <= 1e-6)))
        P(f"[{f}] KA1 GB1 L0 means X {cm['X']:+.6f} E {cm['E']:+.6f} S {cm['S']:+.6f}: max|d| {d1:.1e} -> {'PASS' if d1 <= 1e-6 else 'FAIL'}")
        P(f"[{f}] KA2 L1 ellipticals {e_l1:+.6f} vs QX26 {Q26['foot'][f]['ellipticals']['D_imf']:+.6f}: |d| {d2:.1e} -> {'PASS' if d2 <= 1e-6 else 'FAIL'}")
    # deep-MOND point mass with this lane's rho_ph (KA4 part)
    a0c = A0["canonical"]; Mb = 1e10 * MS; rM = math.sqrt(G * Mb / a0c); rr = 100 * rM
    ratio = rho_ph_local(G * Mb / rr ** 2 / a0c, 0.0, rr, a0c) * 4 * math.pi * G * rr ** 2 / math.sqrt(a0c * G * Mb)
    RES["KA"]["KA4_pointmass_ratio"] = dict(ratio=ratio, ok=bool(abs(ratio - 1) <= 1e-4))
    P(f"KA4 deep-MOND point-mass phantom (this lane's rho_ph, 100 r_M): ratio {ratio:.5f} -> {'PASS' if abs(ratio - 1) <= 1e-4 else 'FAIL'}")
    # ---------------- web (SV5) with checkpoint
    WEB = {}
    if os.path.exists(CKPT):
        z_ = np.load(CKPT, allow_pickle=True); WEB = z_["web"].item(); P(f"resumed web summaries from checkpoint: {list(WEB)}")
    need = [f for f in A0 if f not in WEB]
    CELLS = {}
    SVd = os.path.join(CL, "SV5_growth_mechanism"); sys.path.insert(0, SVd)
    _a = sys.argv; sys.argv = [os.path.join(SVd, "sv5_web.py")]
    with contextlib.redirect_stdout(io.StringIO()): import sv5_web as SV
    sys.argv = _a
    W, dV = SV.realise(5)
    S2J = json.load(open(os.path.join(SVd, "iter_2_charge_switched_sound_speed", "sv5_iter2.json")))
    S1J = json.load(open(os.path.join(SVd, "iter_1_law_on_web", "sv5_iter1.json")))
    for f in A0:
        w, cells = web_pass(f, A0[f], W, dV, SV); CELLS[f] = cells
        if f in need: WEB[f] = w
        np.savez(CKPT, web=np.array(WEB, dtype=object))
        if STOP["flag"]: P("SIGTERM: checkpoint written, exit 3"); open(os.path.join(HERE, "oq1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(3)
        w = WEB[f]
        dr = abs(w["r_F1"] / S1J["foot"][f]["proj"]["r"] - 1)
        ds = abs(w["Sigma_star_over_rhoDE"] - S2J["foot"][f]["Sigma_star_over_rhoDE"]) / S2J["foot"][f]["Sigma_star_over_rhoDE"]
        dfz = max(abs(w["frac"][z] - S2J["foot"][f]["F"][z]) for z in S2J["foot"][f]["F"])
        RES["KA"][f]["KA3"] = dict(r_F1=w["r_F1"], sv5=S1J["foot"][f]["proj"]["r"], rel=dr, ok=bool(dr <= 1e-3))
        RES["KA"][f]["KA4"] = dict(Sigma_star=w["Sigma_star_over_rhoDE"], sv5=S2J["foot"][f]["Sigma_star_over_rhoDE"], rel=ds, frac_maxdiff=dfz, ok=bool(ds <= 1e-3 and dfz <= 1e-3))
        P(f"[{f}] KA3 web lensing amplitude at F = 1: r {w['r_F1']:.4f} vs SV5 {S1J['foot'][f]['proj']['r']:.4f} (rel {dr:.1e}) -> {'PASS' if dr <= 1e-3 else 'FAIL'}")
        P(f"[{f}] KA4 Sigma_* {w['Sigma_star_over_rhoDE']:.4f} vs SV5 {S2J['foot'][f]['Sigma_star_over_rhoDE']:.4f} rho_DE (rel {ds:.1e}); web fractions F_f(z) max|d| {dfz:.1e} -> {'PASS' if (ds <= 1e-3 and dfz <= 1e-3) else 'FAIL'}")
        P(f"[{f}] web: F_web,max = {w['Fweb_max']:.5g} (r {w['r_at_Fmax']:.4f} at the line {w['r_line']:.4f}; shape dchi2 {w['dchi2_at_Fmax']:.3f})")
    if os.path.exists(CKPT): os.remove(CKPT)
    kaok = all(RES["KA"][f][k]["ok"] for f in A0 for k in ("KA1", "KA2", "KA3", "KA4")) and RES["KA"]["KA4_pointmass_ratio"]["ok"]
    RES["KA_all"] = bool(kaok)
    if not kaok:
        P("KA FAIL: stop; nothing graded (fix the loader).")
        json.dump(RES, open(os.path.join(HERE, "oq1.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "oq1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)
    # ---------------- S1 per footing, groups f* = 0 and 1, starts 0 / 1 / 10
    MUTS = {"M1": {}, "M2": {}, "M3": {}}
    for f, a0 in A0.items():
        w = WEB[f]; FR = dict(web=w); wh = web_hist_factory(CELLS[f]); labs = []
        for fst in (0, 1):
            pts, nmiss = points(f, a0, fst); ctx = ctx_for(pts, f, w["Fweb_max"])
            if fst == 0:
                FR["n_points"] = {c: sum(1 for p in pts if p["cls"] == c) for c in sorted({p["cls"] for p in pts})}; FR["dsph_x_missing"] = nmiss
                FR["ctx"] = {k: v for k, v in ctx.items() if k != "planted_ss"}
                # side tables (no label): q_b, q_t per class
                FR["side_q_b_q_t"] = {c: dict(log10_q_b=pct3([p["qb"] for p in pts if p["cls"] == c]),
                                              log10_q_t=pct3([p["qt"] for p in pts if p["cls"] == c]))
                                      for c in FR["n_points"]}
                FR["side_web"] = w["side"]
                FR["F_need_class_mean"] = {c: float(np.mean([Fneed(p) for p in pts if p["cls"] == c])) for c in FR["n_points"] if c != "Solar System"}
                FR["rph_range_log10"] = {c: pct3([p["rph"] for p in pts if p["cls"] == c]) for c in FR["n_points"]}
                FR["rph_le0"] = {c: sum(1 for p in pts if p["cls"] == c and p["rph"] <= 0) for c in FR["n_points"]}
            runs = {}
            for F0 in (0, 1, 10):
                r = s1_run(pts, ctx, F0, wh); runs[str(F0)] = r
                P(f"[{f}] groups f*={fst} start F0={F0}: {r['iterations']} it (conv {r['converged']}, cycle {r['cycled']}); S1 {'HOLDS' if r['S1_holds'] else 'EMPTY in ' + str(len(r['dead_bins'])) + ' bins'}")
                for d in r["dead_bins"][:60]:
                    cs = ", ".join(f"{c}(n {v['n']}, F {['%.3g-%.3g' % (a, b) for a, b in v['band']] or 'none'})" for c, v in d["classes"].items())
                    P(f"     DEAD bin log q {d['log10q']}: gap {d['gap_dex'] if d['gap_dex'] is not None else 'n/a'} dex; worst pair {d['worst_pair']}; {cs}")
            # S3 report for the F0 = 1 run where S1 holds; leave as reported otherwise
            for F0, r in runs.items():
                r["S3"] = s3_run(pts, r, ctx) if r["S1_holds"] else "not run (S1 empty)"
            FR[f"fst{fst}"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("q", "F")} for k, v in runs.items()}
            labs += [label_of([r]) for r in runs.values()]
            # ---------------- MUTATE twins (static classes; web excluded, disclosed)
            if True:
                base = [p for p in pts]; q1 = np.array(runs["1"]["q"]); stat = [i for i, p in enumerate(pts) if p["cls"] != "Solar System" and q1[i] > 0]
                qmed = float(np.median(q1[stat]))
                for M, step in (("M1", False), ("M2", True)):
                    pp = plant(base, qmed, step); cx = ctx_for(pp, f, w["Fweb_max"], planted=True); mr = {}
                    for F0 in (0, 1, 10):
                        r = s1_run(pp, cx, F0, None); r["S3"] = s3_run(pp, r, cx) if r["S1_holds"] else "not run"
                        mr[str(F0)] = {kk: vv for kk, vv in r.items() if kk not in ("q", "F")}
                        P(f"[{f}] {M} f*={fst} F0={F0}: S1 {'HOLDS' if r['S1_holds'] else 'EMPTY (' + str(len(r['dead_bins'])) + ' bins, max gap ' + str(round(max((d['gap_dex'] or 0) for d in r['dead_bins']), 3)) + ' dex)'}"
                          + (f"; S3 {'HOLDS' if r['S3']['S3_holds'] else 'FAILS'} " + str({k: v['status'] for k, v in r['S3']['per_class'].items()}) if r["S1_holds"] else ""))
                    MUTS[M][f"{f}|fst{fst}"] = dict(q_med=qmed, runs=mr)
            # M3: Newton on G1
            if fst == 0:
                sp = [p for p in pts if p["cls"] == "SPARC"]
                Zb = float(np.mean([p["D"] - math.log10(p["x"] / glaw(p["x"], 1.0)) for p in sp]))
                MUTS["M3"][f] = dict(G1_Z_newton=Zb, G1_fails=bool(abs(Zb) > 0.057))
                P(f"[{f}] M3 Newton (F = 0, b = 1): SPARC Z {Zb:+.4f} -> G1 {'FAILS (bites)' if abs(Zb) > 0.057 else 'PASSES (no bite)'}")
        FR["label"] = "DEAD" if "DEAD" in labs else labs[0]
        P(f"[{f}] LABEL: {FR['label']}")
        RES["foot"][f] = FR; del CELLS[f]
    RES["label"] = "DEAD" if any(RES["foot"][f]["label"] == "DEAD" for f in A0) else RES["foot"]["canonical"]["label"]
    # power verdicts
    m1 = all(all(r["S1_holds"] and isinstance(r["S3"], dict) and r["S3"]["S3_holds"] for r in v["runs"].values()) for v in MUTS["M1"].values())
    m2 = all(any(not r["S1_holds"] for r in v["runs"].values()) for v in MUTS["M2"].values())
    m3 = all(v["G1_fails"] for v in MUTS["M3"].values())
    RES["MUTATE"] = dict(M1_power_to_find=bool(m1), M2_power_to_kill=bool(m2), M3_newton_G1_fails=bool(m3))
    P(f"MUTATE: M1 planted law found (S1 holds + S3 holds, every start) {m1}; M2 planted step killed {m2}; M3 Newton fails G1 {m3}")
    P(f"OQ1 LABEL (worse footing): {RES['label']}" + ("" if m2 else " [M2 did not bite: the kill has no demonstrated power]"))
    RES = finalize(RES, MUTS)
    P(f"LABEL AS FROZEN: {RES['label_as_frozen']}; S1 reading {RES['S1_reading']}")
    for f, v in RES["post_freeze_margin_reading"]["foot"].items():
        P(f"  margin [{f}] M1 null max gap {v['M1_null_max_gap_dex']:.3f} dex; runs with a conflict above it: {sum(1 for x in v['runs'].values() if x['n_above_null'])}/{len(v['runs'])}; "
          f"max gap {max(x['max_gap'] for x in v['runs'].values()):.3f}; web bins {v['web_bins']}; lowest host log10 q {v['lowest_host_log10q_above_floor']:.2f}")
    P("kappa = 1/2 FITTED; not theory closed.")
    for M, v in MUTS.items():
        json.dump(dict(lane="OQ1 MUTATE " + M, criteria="3d8e38ffb2", runs=v, verdict=RES["MUTATE"]), open(os.path.join(HERE, f"oq1_MUTATE_{M}.json"), "w"), indent=1, default=float)
    json.dump(RES, open(os.path.join(HERE, "oq1.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "oq1.out"), "w").write("\n".join(OUT) + "\n")
