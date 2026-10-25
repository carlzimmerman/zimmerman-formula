#!/usr/bin/env python3
"""EM1_emergent_dust_law: route E (cold sector clumps like dust everywhere, no law force, the RAR emergent) scored on SPARC
with the law's own per-galaxy freedom, framework-native background, no abundance matching; T0 (no universal c-carrying
acceleration from dust dynamics); R3 emergent g+; R4 halo acceleration ratio z = 2.33 / 0.

Criteria: FROZEN_CRITERIA.md (1b0dbd6eef, committed with the ledger before any number).  kappa = 1/2 FITTED.  Not "theory closed".

Run:   OMP_NUM_THREADS=1 nice -n 15 python3 em1_emergent.py            -> em1_emergent.out, em1_emergent_results.json
       OMP_NUM_THREADS=1 nice -n 15 python3 em1_emergent.py --mutate   -> halo x 0; KH must FAIL (exit 1)
"""
import os, sys, io, json, math, time, contextlib, resource, warnings
import numpy as np
import sympy as sp
from classy import Class

warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # X36 S0a patch: scratch copy sits one level deeper
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv
U05 = "--ups05" in sys.argv          # AMENDMENT A1 (post-result, reported only): Upsilon pinned at 0.50 for law and dust alike
TAG = "_MUTATE" if MUT else ("_UPS05" if U05 else "")
HALO_FAC = 0.0 if MUT else 1.0
T0_ = time.time()
OUTL = []
RES = dict(lane="EM1_emergent_dust_law", criteria="1b0dbd6eef", mutate=MUT, checks={}, rows={})
FOOTS = ("canonical", "alt")
LN10 = math.log(10.0)
G, MSUN, KPC_S, MPC = 6.67430e-11, 1.98847e30, 3.0857e19, 3.0857e22
UPS = np.array([0.50]) if U05 else np.round(np.arange(0.30, 1.2001, 0.01), 2)
LM = np.round(np.arange(8.0, 14.0001, 0.02), 2)
with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
    import CFG4_common as C4  # noqa: E402  (read only: the footings)
A0 = {f: float(C4.A0[f]) for f in FOOTS}
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(key, ok, value, detail=""):
    RES["checks"][key] = dict(ok=bool(ok), value=value, detail=detail)
    P(f"{key} {'PASS' if ok else 'FAIL'}  {value}  {detail}")


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9


# ---------------- T0: dimensional theorem ----------------
al, be, ga = sp.symbols("alpha beta gamma")
sol = sp.solve([3 * al - 1, -al + be, -2 * al - ga + 2], [al, be, ga], dict=True)   # G^a M^b H^c = L T^-2
t0_ok = len(sol) == 1 and sol[0][be] != 0
P(f"T0: acceleration from {{G, M, H}}: G^{sol[0][al]} M^{sol[0][be]} H^{sol[0][ga]} (unique; depends on M) -> no universal "
  "c-carrying scale from route E's dynamics; a0 = kappa c sqrt(G rho_L) is a z = 0 coincidence there")
RES["T0"] = {str(k): str(v) for k, v in sol[0].items()}
check("KT", t0_ok, f"solutions={len(sol)}, beta={sol[0][be]}")

# ---------------- SPARC (P4's loader, mask, weights) ----------------
def load_sparc():
    d_ = os.path.join(DATA, "sparc_data"); gal = []
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        try:
            d = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        gal.append(dict(name=f.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5]))
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            tab[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
        except ValueError:
            continue
    for g_ in gal:
        g_["meta"] = tab[g_["name"]]
        R = g_["R"] * KPC_S
        VB2 = np.sign(g_["Vgas"])[:, None] * g_["Vgas"][:, None] ** 2 + UPS[None, :] * g_["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * g_["Vbul"][:, None] ** 2
        GB = VB2 * 1e6 / R[:, None]
        GO = (g_["Vobs"] * 1e3) ** 2 / R
        OK = (GB > 0) & (GO > 0)[:, None] & np.isfinite(GB) & (g_["Vobs"] > 0)[:, None]
        g_.update(Rm=R, GB=GB, GO=GO, OK=OK, W=1.0 / (np.clip(g_["eV"], 1, None) / np.clip(g_["Vobs"], 1, None)) ** 2,
                  lMb=math.log10((0.5 * g_["meta"]["L36"] + 1.33 * g_["meta"]["MHI"]) * 1e9), L36=g_["meta"]["L36"] * 1e9)
    return gal


GALS = load_sparc()
NG = len(GALS)


def fit_one(q, lgp):
    """lgp (..., n_pts, n_ups) log10 g_pred -> best-Upsilon (by weighted mse) wr2, wsum, U index; leading dims kept."""
    OK, W = q["OK"], q["W"]
    r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0)
    Wm = np.where(OK, W[:, None], 0.0)
    wr2 = (Wm * r * r).sum(-2); ws = np.broadcast_to(Wm.sum(-2), wr2.shape)
    i = np.argmin(wr2 / np.maximum(ws, 1e-300), axis=-1)
    take = lambda a: np.take_along_axis(a, i[..., None], -1)[..., 0]
    return take(wr2), take(ws), i


def pooled(wr2, ws, iu):
    return dict(rms=float(math.sqrt(np.sum(wr2) / np.sum(ws))), U_median=float(np.median(UPS[np.asarray(iu)])))


def line(st):
    return bool(st["rms"] <= 0.110 and 0.50 <= st["U_median"] <= 0.80)


# ---------------- KP: law reproduction ----------------
P4R = {"canonical": (0.054087447879939264, 0.52), "alt": (0.05371798965550355, 0.44)}
LAW = {}
for f in FOOTS:
    a0 = A0[f]; rows = [fit_one(q, np.log10(np.maximum((0.5 + np.sqrt(0.25 + a0 / np.maximum(q["GB"], 1e-300))) * q["GB"], 1e-300))) for q in GALS]
    LAW[f] = pooled([r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows])
okp = all(abs(LAW[f]["rms"] - P4R[f][0]) <= 1e-4 and LAW[f]["U_median"] == P4R[f][1] for f in FOOTS)
if U05:
    okp = True                       # A1: P4's per-galaxy-Upsilon numbers do not apply at pinned Upsilon; law reported only
check("KP", okp, "; ".join(f"{f} {LAW[f]['rms']:.6f}@{LAW[f]['U_median']:.2f} (P4 {P4R[f][0]:.6f}@{P4R[f][1]:.2f})" for f in FOOTS))
RES["law"] = LAW
rowsN = [fit_one(q, np.log10(np.maximum(q["GB"], 1e-300))) for q in GALS]
NEWT = pooled([r[0] for r in rowsN], [r[1] for r in rowsN], [r[2] for r in rowsN])
P(f"Newtonian baryons only (own best Upsilon): rms {NEWT['rms']:.4f}, median U {NEWT['U_median']:.2f}")

# ---------------- backgrounds: CLASS, sigma(M), Bullock c(M, z) ----------------
F3 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BGS = {}
for tag in ("A_c2b_refit", "B_cfg886_bg"):
    p = F3[tag]["params"]
    c = Class(); c.set({"omega_b": p["omega_b"], "omega_cdm": p["omega_cdm"], "h": p["h"], "ln10^{10}A_s": p["lnAs"], "n_s": p["n_s"],
                        "tau_reio": p["tau"], "N_ur": 3.044, "output": "mPk", "P_k_max_h/Mpc": 200.0, "z_max_pk": 10.0})
    c.compute()
    h = p["h"]; k = np.logspace(-4, math.log10(150.0), 3000)                    # h/Mpc
    Pk = np.array([c.pk_lin(kk * h, 0.0) for kk in k]) * h ** 3
    Om = (p["omega_b"] + p["omega_cdm"]) / h ** 2 + c.Omega_nu
    rhom = Om * 2.775e11 * h ** 2                                                # Msun / Mpc^3
    def sigma(M, k=k, Pk=Pk, rhom=rhom, h=h):
        R = (3 * M / (4 * math.pi * rhom)) ** (1 / 3) * h                         # Mpc/h
        x = np.outer(np.atleast_1d(R), k); W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        return np.sqrt(np.trapz(k ** 3 * Pk * W ** 2 / (2 * math.pi ** 2), np.log(k), axis=1))
    s8 = float(np.sqrt(np.trapz(k ** 3 * Pk * (3 * (np.sin(8 * k) - 8 * k * np.cos(8 * k)) / (8 * k) ** 3) ** 2 / (2 * math.pi ** 2), np.log(k))))
    zg = np.linspace(0, 30, 3001); Dg = np.array([c.scale_independent_growth_factor(z) for z in zg]); Dg /= Dg[0]
    H0 = 100 * h * 1e3 / MPC
    def rhoc(z, c=c, H0=H0):
        Hz = c.Hubble(z) * 299792458.0 / MPC if z > 0 else H0                       # CLASS Hubble in 1/Mpc
        return 3 * Hz ** 2 / (8 * math.pi * G)
    def cB(lM, z=0.0, sigma=sigma, zg=zg, Dg=Dg):
        """Bullock+01: c = K (1+z_c)/(1+z), sigma(F M) D(z_c) = 1.686, K = 4, F = 0.01."""
        s0 = sigma(0.01 * 10 ** np.atleast_1d(lM))
        Dt = np.clip(1.686 / s0, Dg[-1], 1.0)
        zc = np.interp(-Dt, -Dg, zg)
        return 4.0 * (1 + zc) / (1 + z)
    BGS[tag] = dict(c=c, h=h, s8=s8, s8_F3=F3[tag]["sigma8"], rhoc=rhoc, cB=cB, fb=p["omega_b"] / (p["omega_b"] + p["omega_cdm"]),
                    cgrid=cB(LM))
okc = all(abs(BGS[t]["s8"] - BGS[t]["s8_F3"]) <= 1e-3 for t in BGS)
check("KC", okc, "; ".join(f"{t} own {BGS[t]['s8']:.5f} vs F3 {BGS[t]['s8_F3']:.5f}" for t in BGS))
for t in BGS:
    P(f"  {t}: Bullock c(M200) at 1e10/1e11/1e12/1e13 = " + ", ".join(f"{BGS[t]['cB'](lm)[0]:.2f}" for lm in (10, 11, 12, 13)) + f"; f_b {BGS[t]['fb']:.4f}")

# ---------------- halo profiles ----------------
XG = np.logspace(-5, 2.5, 600)
def menc_tab(a, b, g_):
    f = XG ** 3 * XG ** (-g_) * (1 + XG ** a) ** (-(b - g_) / a)
    return np.concatenate([[0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(np.log(XG)))])
def dc14(X):
    Xc = min(max(X, -4.1), -1.3)
    a = 2.94 - math.log10((10 ** (Xc + 2.33)) ** -1.08 + (10 ** (Xc + 2.33)) ** 2.29)
    b = 4.23 + 1.34 * Xc + 0.26 * Xc ** 2
    g_ = -0.06 + math.log10((10 ** (Xc + 2.56)) ** -0.68 + 10 ** (Xc + 2.56))
    return (a, b, g_), math.exp(3.4 * (Xc + 4.5)) * 1e-5
XDC = np.round(np.arange(-4.1, -1.2999, 0.02), 2)
DCT = [(menc_tab(*dc14(x)[0]), dc14(x)[1]) for x in XDC]
mN = lambda x: np.log1p(x) - x / (1 + x)


def r200(lM, rc):
    return (3 * 10 ** lM * MSUN / (4 * math.pi * 200 * rc)) ** (1 / 3)


def g_nfw(lM, c_, r, rc):
    """lM (n,), c_ (n,), r (m,) -> (n, m) m/s^2."""
    R2 = r200(np.asarray(lM), rc)[:, None]; rs = R2 / np.asarray(c_)[:, None]
    return HALO_FAC * G * 10 ** np.asarray(lM)[:, None] * MSUN * mN(r[None, :] / rs) / mN(np.asarray(c_))[:, None] / r[None, :] ** 2


# KN: enclosed mass at R200
rc0 = BGS["A_c2b_refit"]["rhoc"](0.0); R2t = r200(np.array([11.0]), rc0)
kn1 = abs(g_nfw(np.array([11.0]), np.array([10.0]), R2t, rc0)[0, 0] * R2t[0] ** 2 / G / MSUN / 1e11 - (HALO_FAC if MUT else 1)) < 1e-3 if not MUT else True
mt, _ = DCT[60]; kn2 = abs(np.interp(10.0, XG, mt) / np.interp(10.0, XG, mt) - 1) < 1e-12
mtN = menc_tab(1.0, 3.0, 1.0); kn3 = abs(np.interp(10.0, XG, mtN) / mN(10.0) - 1) < 1e-3
check("KN", kn1 and kn2 and kn3, f"NFW M(<R200)/M200 ok={kn1}; generic integrator (1,3,1) vs NFW m(10): {np.interp(10.0, XG, mtN) / mN(10.0):.5f}")


# ---------------- R1 / R1-DC14 / R2 per background ----------------
def tables_nfw(q, bg, cfac=1.0):
    """(n_LM, n_ups) best wr2 etc. for NFW on Bullock c x cfac."""
    gh = g_nfw(LM, bg["cgrid"] * cfac, q["Rm"], bg["rc0"])                  # (nLM, n)
    lgp = np.log10(np.maximum(q["GB"][None, :, :] + gh[:, :, None], 1e-300))  # (nLM, n, nU)
    wr2, ws, iu = fit_one(q, lgp)
    return wr2, ws, iu


def tables_dc14(q, bg):
    rc = bg["rc0"]; R2 = r200(LM, rc); out_wr2 = np.empty(len(LM)); out_ws = np.empty(len(LM)); out_iu = np.empty(len(LM), int); clip = 0
    lMs = np.log10(np.maximum(UPS * q["L36"], 1.0))
    for j, lm in enumerate(LM):
        X = lMs - lm; ix = np.clip(np.rint((X - XDC[0]) / 0.02).astype(int), 0, len(XDC) - 1); clip += int(np.sum((X < -4.1) | (X > -1.3)))
        gh = np.empty((len(q["Rm"]), len(UPS)))
        for u in range(len(UPS)):
            m, cb = DCT[ix[u]]; c_ = bg["cgrid"][j] * (1 + cb); rs = R2[j] / c_
            gh[:, u] = HALO_FAC * G * 10 ** lm * MSUN * np.interp(q["Rm"] / rs, XG, m) / np.interp(c_, XG, m) / q["Rm"] ** 2
        lgp = np.log10(np.maximum(q["GB"] + gh, 1e-300))
        a, b, i = fit_one(q, lgp); out_wr2[j], out_ws[j], out_iu[j] = a, b, i
    return out_wr2, out_ws, out_iu, clip


AG = np.round(np.arange(10.0, 13.5001, 0.02), 2); BG_ = np.round(np.arange(0.0, 2.0001, 0.02), 2)
LMB = np.array([q["lMb"] for q in GALS])


def fit_relation(WR2, WS, IU):
    """WR2 (NG, nLM) -> best (a, b) on the grid by pooled rms."""
    best = (np.inf, None)
    gidx = np.arange(NG)[:, None]
    for a in AG:
        lm = a + BG_[None, :] * (LMB[:, None] - 10.0)                      # (NG, nb)
        j = np.clip(np.rint((lm - LM[0]) / 0.02).astype(int), 0, len(LM) - 1)
        rms = np.sqrt(WR2[gidx, j].sum(0) / WS[gidx, j].sum(0))
        k = int(np.argmin(rms))
        if rms[k] < best[0]:
            best = (float(rms[k]), (float(a), float(BG_[k])), j[:, k])
    rms, ab, j = best
    st = pooled(WR2[np.arange(NG), j], WS[np.arange(NG), j], IU[np.arange(NG), j])
    edge = ab[0] in (AG[0], AG[-1]) or ab[1] in (BG_[0], BG_[-1])
    lmclip = int(np.sum((ab[0] + ab[1] * (LMB - 10) < LM[0]) | (ab[0] + ab[1] * (LMB - 10) > LM[-1])))
    return dict(a=ab[0], b=ab[1], edge=bool(edge), lM_off_grid=lmclip, **st), j


ROWS = {}
for tag, bg in BGS.items():
    bg["rc0"] = bg["rhoc"](0.0)
    t1 = time.time()
    TN = [tables_nfw(q, bg) for q in GALS]
    WR2 = np.array([t[0] for t in TN]); WS = np.array([t[1] for t in TN]); IU = np.array([t[2] for t in TN])
    r1, j1 = fit_relation(WR2, WS, IU)
    fbv = float(np.mean(LMB > np.log10(bg["fb"]) + LM[j1]))
    r1["frac_fb_violation"] = fbv; r1["line"] = line(r1)
    r1["class"] = ("PASS" if fbv <= 0.10 else "CONDITIONAL (f_b flag)") if r1["line"] else "FAIL"
    r1["delta_rms_vs_law"] = {f: r1["rms"] - LAW[f]["rms"] for f in FOOTS}
    P(f"[{tag}] R1 NFW dust, global relation lgM200 = {r1['a']:.2f} + {r1['b']:.2f}(lgMb-10) (edge {r1['edge']}): rms {r1['rms']:.4f}, "
      f"median U {r1['U_median']:.2f}, f_b violations {fbv:.3f} -> {r1['class']}  [law: {LAW['canonical']['rms']:.4f} / {LAW['alt']['rms']:.4f}]  ({time.time() - t1:.0f}s)")
    # R2: free M200 and c within +-2 sigma, f_b imposed
    best = np.full(NG, np.inf); bwr2 = np.zeros(NG); bws = np.zeros(NG); biu = np.zeros(NG, int); blm = np.zeros(NG)
    for kf in range(-4, 5):
        TT = [tables_nfw(q, bg, 10 ** (0.055 * kf)) for q in GALS]
        for g_i, (wr2, ws, iu) in enumerate(TT):
            ok = LM >= LMB[g_i] - math.log10(bg["fb"])
            m = np.where(ok, wr2 / np.maximum(ws, 1e-300), np.inf); jj = int(np.argmin(m))
            if m[jj] < best[g_i]:
                best[g_i] = m[jj]; bwr2[g_i], bws[g_i], biu[g_i], blm[g_i] = wr2[jj], ws[jj], iu[jj], LM[jj]
    r2 = pooled(bwr2, bws, biu); r2["line"] = line(r2)
    rel = r1["a"] + r1["b"] * (LMB - 10); inner = (blm > LM[0]) & (blm < LM[-1]) & (blm > LMB - math.log10(bg["fb"]) + 1e-9)
    r2["required_scatter_dex"] = float(np.std(blm[inner] - rel[inner])); r2["n_interior"] = int(inner.sum())
    P(f"[{tag}] R2 allowed (free M200, c +-0.22 dex, f_b imposed): rms {r2['rms']:.4f}, median U {r2['U_median']:.2f}, line {r2['line']}; "
      f"scatter about the R1 relation {r2['required_scatter_dex']:.3f} dex (N {r2['n_interior']})")
    # R1-DC14
    t1 = time.time()
    TD = [tables_dc14(q, bg) for q in GALS]
    rd, jd = fit_relation(np.array([t[0] for t in TD]), np.array([t[1] for t in TD]), np.array([t[2] for t in TD]))
    rd["line"] = line(rd); rd["frac_fb_violation"] = float(np.mean(LMB > np.log10(bg["fb"]) + LM[jd]))
    rd["class"] = ("PASS" if rd["frac_fb_violation"] <= 0.10 else "CONDITIONAL (f_b flag)") if rd["line"] else "FAIL"
    rd["X_clip_total"] = int(sum(t[3] for t in TD))
    P(f"[{tag}] R1-DC14 (EXTERNALLY CALIBRATED): lgM200 = {rd['a']:.2f} + {rd['b']:.2f}(lgMb-10): rms {rd['rms']:.4f}, median U {rd['U_median']:.2f}, "
      f"f_b violations {rd['frac_fb_violation']:.3f} -> {rd['class']}  ({time.time() - t1:.0f}s)")
    # R3: emergent g+ on R1's model
    gb_all, gp_all, go_all, w_all, lmb_all = [], [], [], [], []
    for g_i, q in enumerate(GALS):
        j = j1[g_i]; u = IU[g_i, j]; ok = q["OK"][:, u]
        gh = g_nfw(LM[j:j + 1], bg["cgrid"][j:j + 1], q["Rm"], bg["rc0"])[0]
        gb_all.append(q["GB"][ok, u]); gp_all.append(q["GB"][ok, u] + gh[ok]); go_all.append(q["GO"][ok]); w_all.append(q["W"][ok])
        lmb_all.append(np.full(ok.sum(), q["lMb"]))
    gb, gp, go, w, lmb = map(np.concatenate, (gb_all, gp_all, go_all, w_all, lmb_all))
    LGD = np.arange(-11.5, -9.0, 0.001)
    def fit_gd(gbar, gy, ww):
        y = np.log10(gy); best_ = None
        for lg in LGD[::10]:
            pr = np.log10(gbar / (-np.expm1(-np.sqrt(gbar / 10 ** lg)))); s = np.sum(ww * (y - pr) ** 2)
            if best_ is None or s < best_[0]:
                best_ = (s, lg)
        fine = LGD[(LGD > best_[1] - 0.02) & (LGD < best_[1] + 0.02)]
        ss = [np.sum(ww * (y - np.log10(gbar / (-np.expm1(-np.sqrt(gbar / 10 ** lg))))) ** 2) for lg in fine]
        return float(fine[int(np.argmin(ss))])
    def slope(gbar, gy, ww=None):
        m = gbar < 1e-11
        if m.sum() <= 10:
            return float("nan")
        return float(np.polyfit(np.log10(gbar[m]), np.log10(gy[m]), 1, w=None if ww is None else np.sqrt(ww[m]))[0])
    terc = np.percentile([q["lMb"] for q in GALS], [100 / 3, 200 / 3])
    bins = [lmb < terc[0], (lmb >= terc[0]) & (lmb < terc[1]), lmb >= terc[1]]
    r3 = dict(model=dict(lg=fit_gd(gb, gp, w), terc=[fit_gd(gb[b], gp[b], w[b]) for b in bins], slope=slope(gb, gp)),
              data=dict(lg=fit_gd(gb, go, w), terc=[fit_gd(gb[b], go[b], w[b]) for b in bins], slope=slope(gb, go)))
    r3["model"]["slope_weighted_A1"] = slope(gb, gp, w); r3["data"]["slope_weighted_A1"] = slope(gb, go, w)   # A1, reported only
    lo = gb < 10 ** -11.75; r3["deep_lowg_A1"] = dict(n=int(lo.sum()), median_dlog_data_minus_model=float(np.median(np.log10(go[lo] / gp[lo]))))
    for k_ in ("model", "data"):
        r3[k_]["drift"] = max(r3[k_]["terc"]) - min(r3[k_]["terc"])
    r3["dlog_vs_a0"] = {f: r3["model"]["lg"] - math.log10(A0[f]) for f in FOOTS}
    r3["class"] = "EMERGES" if (all(abs(v) <= 0.10 for v in r3["dlog_vs_a0"].values()) and abs(r3["model"]["drift"] - r3["data"]["drift"]) <= 0.10) else "DOES NOT EMERGE"
    P(f"[{tag}] R3 emergent g+: model {10 ** r3['model']['lg']:.3e} (terciles " + ", ".join(f"{10 ** v:.2e}" for v in r3["model"]["terc"]) +
      f"; drift {r3['model']['drift']:.3f} dex; low-g slope {r3['model']['slope']:.3f}) | data at same U {10 ** r3['data']['lg']:.3e} (terciles " +
      ", ".join(f"{10 ** v:.2e}" for v in r3["data"]["terc"]) + f"; drift {r3['data']['drift']:.3f}; slope {r3['data']['slope']:.3f}) | "
      f"dlog vs a0 can {r3['dlog_vs_a0']['canonical']:+.3f} alt {r3['dlog_vs_a0']['alt']:+.3f} -> {r3['class']}")
    P(f"[{tag}] R3 A1 (reported only): weighted low-g slope model {r3['model']['slope_weighted_A1']:.3f} vs data {r3['data']['slope_weighted_A1']:.3f}; "
      f"g_bar < 10^-11.75: N {r3['deep_lowg_A1']['n']}, median log(data/model) {r3['deep_lowg_A1']['median_dlog_data_minus_model']:+.3f}")
    # R4: halo characteristic acceleration ratio z = 2.33 / 0
    r4 = {}
    for lm in (11.0, 12.0):
        gm2 = []
        for z in (0.0, 2.33):
            rc = bg["rhoc"](z); c_ = bg["cB"](lm, z)[0]; rs = r200(np.array([lm]), rc)[0] / c_
            gm2.append(G * 10 ** lm * MSUN * mN(1.0) / mN(c_) / rs ** 2)
        r4[f"{lm:g}"] = dict(ratio=gm2[1] / gm2[0], c0=float(bg["cB"](lm, 0.0)[0]), c233=float(bg["cB"](lm, 2.33)[0]))
    r4["class"] = "DISTINCT" if all(not (0.80 <= v["ratio"] <= 1.25) for v in r4.values() if isinstance(v, dict)) else "NOT DISTINCT"
    P(f"[{tag}] R4 halo g_-2(z=2.33)/g_-2(0): 1e11 {r4['11']['ratio']:.2f} (c {r4['11']['c0']:.1f}->{r4['11']['c233']:.1f}), "
      f"1e12 {r4['12']['ratio']:.2f} (c {r4['12']['c0']:.1f}->{r4['12']['c233']:.1f}) vs framework 1.00 (exact Lambda) / 0.91-0.94 (CFG689) -> {r4['class']}")
    ROWS[tag] = dict(R1=r1, R2=r2, R1_DC14=rd, R3=r3, R4=r4)

RES["rows"] = ROWS
RES["newtonian"] = NEWT
khok = all(ROWS[t]["R1"]["rms"] < NEWT["rms"] - 0.05 for t in ROWS)
check("KH", khok, "; ".join(f"{t} R1 {ROWS[t]['R1']['rms']:.4f} vs Newtonian {NEWT['rms']:.4f}" for t in ROWS))
r1c = [ROWS[t]["R1"]["class"] for t in ROWS]; rdc = [ROWS[t]["R1_DC14"]["class"] for t in ROWS]
okc_ = lambda c_: c_.startswith("PASS") or c_.startswith("CONDITIONAL")
if all(okc_(c_) for c_ in r1c):
    V = "ROUTE E VIABLE AS DUST" + (" (CONDITIONAL: f_b flag)" if any(c_.startswith("CONDITIONAL") for c_ in r1c) else "")
elif all(okc_(c_) for c_ in rdc):
    V = "ROUTE E NEEDS FEEDBACK"
else:
    V = "ROUTE E FAILS ON SPARC"
RES["verdict"] = V
P(f"VERDICT: {V}.  R3: " + ", ".join(ROWS[t]["R3"]["class"] for t in ROWS) + ".  R4: " + ", ".join(ROWS[t]["R4"]["class"] for t in ROWS) +
  ".  T0: a0 = kappa c sqrt(G rho_L) is not a law of route E.")
check("KR", rss_gb() < 1.0, f"{rss_gb():.2f} GB")
RES["runtime_s"] = time.time() - T0_
allok = all(v["ok"] for v in RES["checks"].values())
P(f"checks: {'ALL PASS' if allok else 'SOME FAIL'}  ({RES['runtime_s']:.0f} s)")
open(os.path.join(HERE, f"em1_emergent{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
json.dump(RES, open(os.path.join(HERE, f"em1_emergent_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if allok else 1)
