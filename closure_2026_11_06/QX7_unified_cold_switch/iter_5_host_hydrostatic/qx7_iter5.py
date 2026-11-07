#!/usr/bin/env python3
"""QX7 iter_5 (criteria 2afe6bac03): today's captured dust in hydrostatic n = 1 equilibrium in its HOST's field.
    python3 qx7_iter5.py            # graded: qx7_iter5.json / .out
    python3 qx7_iter5.py --mutate   # MUTATE A-D: qx7_iter5_MUTATE.json / .out
Profile: dM/dr = 4 pi r^2 rho, drho/dr = -(mu^2/4 pi G) g_law(G (M_b + M_d)/r^2), mu = 2 pi/lambda_0; rho_c shot to M_d,tot.
iter_4's prelude (loaders, switch, growth solver, gates' data) is executed from its own source, unchanged.
kappa = 1/2 FITTED; not theory closed. 1 thread."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx7_iter5_MUTATE" if MUT else "qx7_iter5"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)

# ---- iter_4 prelude, executed from its own source (everything before its RES = dict) ----
I4 = os.path.join(HERE, "..", "iter_4_late_evaporation", "qx7_iter4.py")
s4 = open(I4).read(); s4 = s4[:s4.index("RES = dict(")]
argv0, sys.argv = sys.argv, [I4]
N4 = {"__file__": os.path.abspath(I4), "__name__": "iter4_reused"}
exec(compile(s4, I4, "exec"), N4); sys.argv = argv0
G, MS, KPC, A0, glaw, XC, GR, LE, EL = (N4[k] for k in ("G", "MS", "KPC", "A0", "glaw", "XC", "GR", "LE", "EL"))
R, FCAP, r_ta0, Md_iso, G5SYS, g2gen, kJ_of, I2, OD0, ode = (N4[k] for k in ("R", "FCAP", "r_ta0", "Md", "G5SYS", "g2gen", "kJ_of", "I2", "OD0", "ode"))
MPC = 1e3 * KPC
ST4 = json.load(open(os.path.join(HERE, "..", "iter_4_late_evaporation", "qx7_iter4.json")))
P(f"QX7 iter5 {TAG}: R {R:.3f}, f_cap {FCAP}; iter_4 prelude reused; carried cells {len(ST4['evaluated'])}")

# ---- host baryon profiles M_b(<r) [Msun], r in m ----
def pl_profile(rk, Mk):
    """log-log interpolation; power law inward from the first two points; constant beyond the last."""
    lr, lm = np.log(np.asarray(rk, float)), np.log(np.asarray(Mk, float)); s = (lm[1] - lm[0]) / (lr[1] - lr[0])
    def f(r):
        x = np.log(np.maximum(r, 1e-300)); y = np.interp(x, lr, lm)
        y = np.where(x < lr[0], lm[0] + s * (x - lr[0]), y); y = np.where(x > lr[-1], lm[-1], y); return np.exp(y)
    return f
DATA = os.path.join(REPO, "real_research", "data")
XPROF = {}
for name in sorted({z["name"] for z in XC}):
    p_ = os.path.join(DATA, "xcop", name)
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    gr = np.array(gas["RADIUS"], float) * rg500; gM = np.array(gas["MGAS"], float)
    sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float)
    okg = np.isfinite(gM) & (gM > 0) & (gr > 0); oks = np.isfinite(sM) & (sM > 0) & (sr > 0)
    fg, fs = pl_profile(gr[okg], gM[okg]), pl_profile(sr[oks], sM[oks])
    Mlast, tlast = next(z["Mb_last"] for z in XC if z["name"] == name)
    XPROF[name] = (lambda r, fg=fg, fs=fs, Ml=Mlast, tl=tlast * KPC: np.where(r > tl, Ml, fg(r / KPC) + fs(r / KPC)), Mlast)

def point(M): return lambda r: np.full_like(np.asarray(r, float), M)

# ---- the host-hydrostatic n = 1 solver (vectorised over trial central densities) ----
NSTEP = 4000
def profile(Mb_of, Mtot_d, lam0_mpc, a0, host=True, law=True):
    """returns (r_s [m], grid r, M_d(<r) [Msun]) with M_d(r_s) = Mtot_d; None if Mtot_d <= 0."""
    if Mtot_d <= 0: return None
    mu = 2 * math.pi / (lam0_mpc * MPC); Rc = math.pi / mu
    rmin = min(1e-4 * Rc, 0.1 * KPC); r = np.geomspace(rmin, 1.05 * Rc, NSTEP); cmu = mu ** 2 / (4 * math.pi * G)
    Mb = Mb_of(r) * MS if host else np.zeros_like(r)
    def run(rc):
        rho = rc.copy(); M = np.zeros_like(rc); Ms = np.zeros((len(r), len(rc))); Ms[0] = M; alive = np.ones(len(rc), bool)
        rs = np.full(len(rc), np.nan); Mfin = np.full(len(rc), np.nan)
        def deriv(rr, rho_, M_, mb):
            gN = G * (mb + M_) / rr ** 2; gt = glaw(gN, a0) if law else gN
            return -cmu * gt, 4 * math.pi * rr ** 2 * np.maximum(rho_, 0)
        for i in range(len(r) - 1):
            h = r[i + 1] - r[i]; rm = 0.5 * (r[i] + r[i + 1]); mbm = 0.5 * (Mb[i] + Mb[i + 1])
            k1 = deriv(r[i], rho, M, Mb[i]); k2 = deriv(rm, rho + h / 2 * k1[0], M + h / 2 * k1[1], mbm)
            k3 = deriv(rm, rho + h / 2 * k2[0], M + h / 2 * k2[1], mbm); k4 = deriv(r[i + 1], rho + h * k3[0], M + h * k3[1], Mb[i + 1])
            rn = rho + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); Mn = M + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            cross = alive & (rn <= 0)
            if cross.any():
                t = rho[cross] / (rho[cross] - rn[cross]); rs[cross] = r[i] + t * h; Mfin[cross] = M[cross] + t * (Mn[cross] - M[cross])
                alive &= ~cross
            rho = np.where(alive, rn, 0.0); M = np.where(alive, Mn, M); Ms[i + 1] = M
            if not alive.any(): break
        Ms[i + 1:] = M
        return rs, Mfin, Ms
    target = Mtot_d * MS; riso = math.pi * target / (4 * Rc ** 3)
    lo, hi = math.log(riso * 1e-8), math.log(riso * 1e4)
    for _ in range(40):   # numerical bracket expansion only (post-run fix, disclosed in README): host-held solutions can need rho_c >> riso
        _, Mhi, _ = run(np.array([math.exp(hi)]))
        if np.isfinite(Mhi[0]) and Mhi[0] > target: break
        hi += math.log(1e3)
    for _ in range(40):
        _, Mlo, _ = run(np.array([math.exp(lo)]))
        if np.isfinite(Mlo[0]) and Mlo[0] < target: break
        lo -= math.log(1e3)
    for _ in range(5):
        lrc = np.linspace(lo, hi, 24); rs, Mf, Ms = run(np.exp(lrc))
        if np.isnan(Mf).any(): raise RuntimeError("no surface inside 1.05 R_c")
        j = int(np.searchsorted(Mf, target))
        if j == 0 or j == len(lrc): raise RuntimeError("bracket")
        lo, hi = lrc[j - 1], lrc[j]
        if abs(Mf[j] / target - 1) < 1e-6: break
    t = (math.log(target) - math.log(Mf[j - 1])) / (math.log(Mf[j]) - math.log(Mf[j - 1]))
    rs, Mf, Ms = run(np.array([math.exp(lo + t * (hi - lo))]))
    return float(rs[0]), r, Ms[:, 0] / MS * (target / Mf[0])   # last rescale: <= bracket error (< 1e-6 by loop or interp)

CACHE = {}
def dust(key, Mb_of, Mb_tot, lam0, a0, fcap=FCAP, host=True, law=True):
    """M_d(<r) callable [Msun] with r in m; zero if no retention."""
    ck = (key, round(math.log(lam0), 9), a0, fcap, host, law)
    if ck in CACHE: return CACHE[ck]
    Mt = fcap * R * Mb_tot; out = (lambda r: 0.0 * np.asarray(r, float)), None
    if Mt > 0:
        rs, rg, Mg = profile(Mb_of, Mt, lam0, a0, host, law)
        if rs / MPC < r_ta0(Mb_tot): out = (lambda r, rg=rg, Mg=Mg, rs=rs, Mt=Mt: np.where(np.asarray(r) >= rs, Mt, np.interp(np.asarray(r, float), rg, Mg))), rs
        else: out = (lambda r: 0.0 * np.asarray(r, float)), rs
    CACHE[ck] = out; return out

# ---- gates and predictions with a dust provider ----
def lens_mean(a0, lam0, prov):
    d = []
    for i, p in enumerate(LE):
        Mb = p["Mb"] / MS; r = math.sqrt(G * p["Mb"] / p["gbar"]); md = float(prov(("L", round(Mb, 3)), point(Mb), Mb, lam0, a0)(r))
        d.append(math.log10(p["gobs"] / glaw(p["gbar"] + G * md * MS / r ** 2, a0)))
    return float(np.mean(d))
def ell_mean(a0, lam0, prov):
    d = []
    for e in EL:
        Mbt = e["Mbar"](1e9); f = prov(("E", e["name"]), lambda r, e=e: np.array([e["Mbar"](x / KPC) for x in np.atleast_1d(r)]), Mbt, lam0, a0)
        for m in (2, 4, 8):
            rk = m * e["Re"]; rm = rk * KPC; md = float(f(rm))
            Mp = glaw(G * (e["Mbar"](rk) + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; d.append(math.log10(e["Mtot"](rk) / Mp))
    return float(np.mean(d))
def gal_gates(lam0, prov, base):
    g5 = True
    for nm, Mb, ro in G5SYS:
        a0 = A0["canonical"]; g5 &= float(prov(("S", nm), point(Mb), Mb, lam0, a0)(ro * MPC)) / Mb <= 0.3
        a0 = A0["alt"]; g5 &= float(prov(("S", nm), point(Mb), Mb, lam0, a0)(ro * MPC)) / Mb <= 0.3
    g6 = all(abs(lens_mean(a0, lam0, prov) - base[f]["L"]) <= 0.05 for f, a0 in A0.items())
    g7 = all(abs(ell_mean(a0, lam0, prov) - base[f]["E"]) <= 0.15 for f, a0 in A0.items())
    return bool(g5), bool(g6), bool(g7)
def predict(lam0, prov):
    out = {}
    for f, a0 in A0.items():
        xd = []; per = {}
        for z in XC:
            fx, Mt = XPROF[z["name"]]; rm = z["r_kpc"] * KPC; md = float(prov(("X", z["name"]), fx, Mt, lam0, a0)(rm))
            Mp = glaw(G * (z["M_b"] + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; dl = math.log10(z["M_obs"] / Mp); xd.append(dl)
            per.setdefault(z["name"], []).append(round(dl, 4))
        xd = np.array(xd); grp = {}
        for fst in (0.0, 1.0):
            npass = 0; dl = []
            for gp in GR:
                p0, p1 = gp["pts"][0], gp["pts"][1]
                fg = pl_profile([p0["r_kpc"], p1["r_kpc"]], [p0["M_gas"] * (1 + fst), p1["M_gas"] * (1 + fst)])
                Mbt = gp["g5"] * (1 + fst); prof = prov(("G", gp["name"], fst), lambda r, fg=fg: fg(np.asarray(r) / KPC), Mbt, lam0, a0); ok = True
                for p in gp["pts"]:
                    Mb = p["M_gas"] * (1 + fst); rm = p["r_kpc"] * KPC; md = float(prof(rm))
                    Mp = glaw(G * (Mb + md) * MS / rm ** 2, a0) * rm ** 2 / G / MS; dlt = math.log10(p["M_obs"] / Mp); dl.append(dlt)
                    ok &= abs(dlt) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
                npass += ok
            grp[f"fst{fst:g}"] = dict(n_pass=int(npass), median_delta=float(np.median(dl)), pass_=bool(npass >= 16))
        out[f] = dict(X_mean=float(xd.mean()), X_rms=float(np.sqrt((xd ** 2).mean())), X_pass=bool(abs(xd.mean()) <= 0.05 and np.sqrt((xd ** 2).mean()) <= 0.10),
                      X_per_cluster=per, groups=grp, groups_strict=bool(all(g["pass_"] for g in grp.values())), groups_either=bool(any(g["pass_"] for g in grp.values())))
    return out

HOST = lambda key, fM, Mt, lam0, a0, fcap=FCAP: dust(key, fM, Mt, lam0, a0, fcap)[0]
def ISO(fcap=FCAP):   # iter_4's isolated core, as a provider (r in m)
    def prov(key, fM, Mt, lam0, a0): return lambda r: np.vectorize(lambda x: Md_iso(Mt, x / MPC, lam0, fcap))(np.asarray(r, float))
    return prov
BASE = {f: dict(L=lens_mean(a0, 1e9, ISO(0.0)), E=ell_mean(a0, 1e9, ISO(0.0))) for f, a0 in A0.items()}

# ---- K1: isolated Newtonian known answer ----
lamK = 2.0; MK = 1e14; rsK, rgK, MgK = profile(point(0.0), MK, lamK, A0["canonical"], host=False, law=False)
RcK = lamK / 2 * MPC; e_rs = abs(rsK / RcK - 1); e_f = 0.0
for frac in (0.1, 0.3, 0.5, 0.7, 0.9):
    xi = math.pi * frac; ex = (math.sin(xi) - xi * math.cos(xi)) / math.pi; e_f = max(e_f, abs(np.interp(frac * RcK, rgK, MgK) / MK - ex))
K1 = dict(rs_rel_err=e_rs, frac_abs_err=e_f, pass_=bool(e_rs <= 1e-4 and e_f <= 1e-4))
P(f"  K1 (isolated, Newtonian): r_s/R_c - 1 = {e_rs:.2e}, enclosed-fraction err {e_f:.2e} -> {'PASS' if K1['pass_'] else 'FAIL'}")
RES = dict(tag=TAG, criteria="2afe6bac03", R=R, f_cap=FCAP, K1=K1, baselines=BASE, note="kappa = 1/2 FITTED; not theory closed")
l0s = np.geomspace(1e-3, 1e2, 61)

if not MUT:
    # R1: carry check on one window cell
    c = ST4["window"][0]; d = g2gen(kJ_of(c["lambda_star"], c["p"])); R1 = dict(cell=c, recomputed=d, pass_=bool(abs(d - c["dchi2"]) <= 1e-6 * max(1, abs(d))))
    P(f"  R1 (carry): cell lambda_0 {c['lambda_0']:.3g} p {c['p']}: dchi2 {d:.6f} vs stored {c['dchi2']:.6f} -> {'PASS' if R1['pass_'] else 'FAIL'}"); RES["R1"] = R1
    galok = {}
    for l0 in l0s:
        try: galok[float(l0)] = gal_gates(float(l0), HOST, BASE)
        except RuntimeError as ex: galok[float(l0)] = ("ERR", str(ex))
    l0_gal = [l0 for l0, g in galok.items() if g[0] is True and all(g)]
    P(f"  galaxy gates G5/G6/G7 (host profile) pass for lambda_0 in {len(l0_gal)}/61 values" + (f": {min(l0_gal):.3g}-{max(l0_gal):.3g} Mpc" if l0_gal else ""))
    RES["galaxy_gates_by_lambda0"] = {f"{k:.4g}": list(v) for k, v in galok.items()}
    okset = {round(math.log(l0), 6) for l0 in l0_gal}
    window = [c for c in ST4["evaluated"] if c["dchi2"] <= I2.DCHI2_LINE and round(math.log(c["lambda_0"]), 6) in okset]
    P(f"  window (carried G2'+G4' x recomputed G5-G7): {len(window)} cells" + (f", lambda_0 {min(c['lambda_0'] for c in window):.3g}-{max(c['lambda_0'] for c in window):.3g}" if window else ""))
    RES["window"] = window
    preds = {}
    for l0 in l0_gal: preds[f"{l0:.4g}"] = predict(l0, HOST)
    RES["cluster_vs_lambda0_galaxyok"] = preds
    # reported, NOT graded and outside the frozen report list (added post-run, disclosed): clusters at iter_4's window lambda_0
    rep = {}
    for l0 in sorted({c["lambda_0"] for c in ST4["window"]}):
        pr = predict(l0, HOST); rep[f"{l0:.4g}"] = pr
        P(f"   [reported, ungraded] iter_4-window lambda_0 {l0:.3g}: " + "; ".join(f"{f} X {pr[f]['X_mean']:+.3f}/{pr[f]['X_rms']:.3f} groups fst0 {pr[f]['groups']['fst0']['n_pass']} fst1 {pr[f]['groups']['fst1']['n_pass']}" for f in A0))
        P(f"      lensing shift " + ", ".join(f"{f} {lens_mean(a0, l0, HOST) - BASE[f]['L']:+.3f}" for f, a0 in A0.items()))
    RES["reported_clusters_iter4_window"] = rep
    for l0 in l0_gal:
        pr = preds[f"{l0:.4g}"]
        P(f"   lambda_0 {l0:.3g} Mpc: " + "; ".join(f"{f} X {pr[f]['X_mean']:+.3f}/{pr[f]['X_rms']:.3f} groups fst0 {pr[f]['groups']['fst0']['n_pass']} fst1 {pr[f]['groups']['fst1']['n_pass']} (med {pr[f]['groups']['fst0']['median_delta']:+.2f})" for f in A0))
    # reported: Newtonian-g dust variant at galaxy-ok lambda_0; MW retention
    NEWT = lambda key, fM, Mt, lam0, a0: dust(key, fM, Mt, lam0, a0, law=False)[0]
    RES["newtonian_variant"] = {f"{l0:.4g}": {f: {k: predict(l0, NEWT)[f][k] for k in ("X_mean", "X_rms")} for f in A0} for l0 in l0_gal}
    RES["MW_retention"] = {}
    for l0 in l0_gal:
        _, rs = dust(("MW",), point(6e10), 6e10, l0, A0["canonical"]); RES["MW_retention"][f"{l0:.4g}"] = dict(r_s_mpc=rs / MPC, r_ta_mpc=r_ta0(6e10), keeps=bool(rs / MPC < r_ta0(6e10)))
    P("  MW (6e10) keeps dust at: " + (", ".join(k for k, v in RES["MW_retention"].items() if v["keeps"]) or "none of the galaxy-ok lambda_0"))
    wl = {round(math.log(c["lambda_0"]), 6) for c in window}
    if not window: lab = "FAIL (no window)"
    else:
        both = {f: sum(1 for c in window if preds[f"{c['lambda_0']:.4g}"][f]["X_pass"] and preds[f"{c['lambda_0']:.4g}"][f]["groups_strict"]) for f in A0}
        lab = ("PASS" if all(v > 0 for v in both.values()) else "FAIL (clusters)") + " [" + ", ".join(f"{f} {both[f]}/{len(window)}" for f in A0) + "]"
    ctrl_ok = K1["pass_"] and R1["pass_"]
    if not ctrl_ok: lab = "NO VERDICT (control failed) | numbers read " + lab
    RES["label"] = lab; P(f"  LABEL: {lab}")
else:
    # MUTATE A: iter_4 isolated provider reproduces iter_4's stored X-COP at lambda_0 ~ 2.15
    keys = list(ST4["cluster_vs_lambda0_galaxyok"].keys()); k = min(keys, key=lambda s: abs(math.log(float(s) / 2.15)))
    pa = predict(float(k), ISO()); okA = all(abs(pa[f]["X_mean"] - ST4["cluster_vs_lambda0_galaxyok"][k][f]["X_mean"]) <= 2e-3 and abs(pa[f]["X_rms"] - ST4["cluster_vs_lambda0_galaxyok"][k][f]["X_rms"]) <= 2e-3 for f in A0)
    RES["MUTATE_A"] = dict(lambda_0=k, mine={f: (pa[f]["X_mean"], pa[f]["X_rms"]) for f in A0}, iter4={f: (ST4["cluster_vs_lambda0_galaxyok"][k][f]["X_mean"], ST4["cluster_vs_lambda0_galaxyok"][k][f]["X_rms"]) for f in A0}, pass_=bool(okA))
    P(f"  MUTATE A (isolated core = iter_4) at lambda_0 {k}: " + "; ".join(f"{f} {pa[f]['X_mean']:+.4f}/{pa[f]['X_rms']:.4f} vs {ST4['cluster_vs_lambda0_galaxyok'][k][f]['X_mean']:+.4f}/{ST4['cluster_vs_lambda0_galaxyok'][k][f]['X_rms']:.4f}" for f in A0) + f" -> {'REPRODUCES' if okA else 'DIFFERS'}")
    zero = lambda key, fM, Mt, lam0, a0: dust(key, fM, Mt, lam0, a0, fcap=0.0)[0]
    pb = predict(2.0, zero); okB = abs(pb["canonical"]["X_mean"] - 0.4675) <= 1e-3 and abs(pb["alt"]["X_mean"] - 0.4345) <= 1e-3
    RES["MUTATE_B"] = dict(X=(pb["canonical"]["X_mean"], pb["alt"]["X_mean"]), pass_=bool(okB))
    P(f"  MUTATE B (f_cap 0): X-COP {pb['canonical']['X_mean']:+.4f} / {pb['alt']['X_mean']:+.4f} vs +0.4675 / +0.4345 -> {'PASS' if okB else 'FAIL'}")
    g = gal_gates(1e-3, HOST, BASE); okC = not (g[0] and g[1]); RES["MUTATE_C"] = dict(gates=list(g), bites=bool(okC))
    P(f"  MUTATE C (lambda_0 1e-3): G5 {g[0]} G6 {g[1]} G7 {g[2]} -> {'BITES' if okC else 'NO BITE'}")
    tri = lambda key, fM, Mt, lam0, a0: dust(key, fM, Mt, lam0, a0, fcap=3 * FCAP)[0]
    mv = {f: predict(2.15, tri)[f]["X_mean"] - predict(2.15, HOST)[f]["X_mean"] for f in A0}; okD = all(abs(v) > 0.1 for v in mv.values())
    RES["MUTATE_D"] = dict(move=mv, bites=bool(okD))
    P(f"  MUTATE D (f_cap x3 at lambda_0 2.15): move " + ", ".join(f"{f} {v:+.3f}" for f, v in mv.items()) + f" -> {'BITES' if okD else 'NO BITE'}")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
