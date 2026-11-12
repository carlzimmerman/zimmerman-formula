#!/usr/bin/env python3
"""EUC8 (WIDE-LENS RESIDUAL PROFILE).  Frozen criteria: FROZEN_CRITERIA.md (commit 1c56b3f50c; clarification C1 fa59e21652).

What the extra mass in Euclid's wide-separation lenses must look like.
Part A: how much projected mass law S plus the stars leave unexplained inside the Einstein radius, in physical units.
Part B: how concentrated it is, from two apertures on the same galaxies (Einstein radius; DESI fibre dispersion).

Run:
  python3 -I euc8.py --data-dir <dir with the two ECLIPSE csv files>
  EUC8_MUTATE=sigup   python3 -I euc8.py --data-dir <dir>      (must exit 1)
  EUC8_MUTATE=sigdown python3 -I euc8.py --data-dir <dir>      (must exit 1)
  EUC8_MUTATE=newton  python3 -I euc8.py --data-dir <dir>      (must exit 1)
"""
import argparse, csv, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EUC5 = os.path.join(HERE, "..", "EUC5_dynamical_boost")
sys.path.insert(0, EUC5)
import euc5 as D
E = D.E
MUT = (os.environ.get("EUC8_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
SIGF = {"sigup": 1.30, "sigdown": 0.70}.get(MUT, 1.0)
G, C, MSUN, KPC, PC, ARCSEC = E.G, E.C, E.MSUN, E.KPC, E.PC, E.ARCSEC
RT = 300.0 * KPC
GAM = {"2.5": 2.5, "2.0": 2.0, "1.75": 1.75, "1.5": 1.5, "1.0": 1.0, "0.0": 0.0}
FAMS = ["P", "T", "2.5", "2.0", "1.5", "1.0", "0.0"]
GS = ["0.0", "1.0", "1.5", "2.0", "2.5"]                     # the slope axis, shallow to steep
BSTAR = [-0.10, 0.0, 0.10]
CASES = ["far", "central", "near"]
OMB, SHARE = 0.0488, 5.41
RHOC = 3.0 * (67.74e3 / (1.0e6 * PC)) ** 2 / (8.0 * math.pi * G)
SIG_UNIT = MSUN / PC ** 2
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def zs_case(z, case):
    z = np.asarray(z, float)
    if case == "far": return np.full(z.shape, E.ZS_INF)
    if case == "central": return np.maximum(2.0, z + 0.5)
    return z + 0.5

def mfrac(fam, r, Re, n, rt=RT):
    """enclosed-mass fraction of the extra component, per unit amplitude (kg)."""
    if fam == "P": return np.ones(np.shape(r))
    if fam == "T": return E.M3D_frac(r, Re, n)
    return (np.minimum(r, rt) / rt) ** (3.0 - GAM[fam])

class Lens2:
    """stars + one extra component under law S; projected mass inside R_E on EUC1's nodes; solves the amplitude."""
    def __init__(self, RE, Re, n, Ms, rmax=1.0e6 * KPC):
        RE, Re, n, Ms = (np.asarray(v, float) for v in (RE, Re, n, Ms))
        U = np.arccosh(np.maximum(rmax / RE, 1.0 + 1e-9))
        self.r = RE[:, None] * np.cosh(E.GLX[None, :] * U[:, None])
        self.gs = G * Ms[:, None] * E.M3D_frac(self.r, Re[:, None], n[:, None]) / self.r ** 2
        self.pref = RE ** 2 / G * U; self.N = len(RE); self.Re, self.n = Re, n
    def gx(self, fam, rt=RT):
        return G * mfrac(fam, self.r, self.Re[:, None], self.n[:, None], rt) / self.r ** 2
    def M2D(self, Bs, A, gx, a0):
        gN = Bs * self.gs + np.asarray(A, float)[:, None] * gx
        return self.pref * np.sum(E.GLW[None, :] * E.g_law(gN, a0, "S"), axis=1)
    def solve(self, Mt, Bs, gx, a0, nit=60):
        need = self.M2D(Bs, np.zeros(self.N), gx, a0) < Mt
        lo = np.full(self.N, 0.0); hi = np.full(self.N, 18.0)                   # log10 amplitude in Msun
        for _ in range(nit):
            mid = 0.5 * (lo + hi)
            up = self.M2D(Bs, 10.0 ** mid * MSUN, gx, a0) < Mt
            lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
        return np.where(need, 10.0 ** (0.5 * (lo + hi)) * MSUN, 0.0), need

def predict_set(L, par, keys, Mt, a_fib, fwhm, beta=0.0):
    """fibre dispersion (km/s) for every key = (footing, family, b_star, source case, r_t), and the amplitudes (kg)."""
    Wt = D.ap_weight(D.RANG, a_fib, fwhm); AMP, gxc = {}, {}
    for k in keys:
        nm, fam, bs, case, rt = k
        if (fam, rt) not in gxc: gxc[(fam, rt)] = L.gx(fam, rt)
        AMP[k] = L.solve(Mt[case], 10.0 ** bs, gxc[(fam, rt)], E.FOOT[nm])[0]
    out = {k: np.zeros(L.N) for k in keys}
    for i in range(L.N):
        r, nu, gs = D.sersic_model(par["Ms"][i], par["Re"][i], par["n"][i])
        g = np.empty((len(keys), len(r)))
        for j, k in enumerate(keys):
            nm, fam, bs, case, rt = k
            g[j] = E.g_law(10.0 ** bs * gs + AMP[k][i] * G * mfrac(fam, r, par["Re"][i], par["n"][i], rt) / r ** 2, E.FOOT[nm], "S")
        s = D.sigma_ap(r, nu, g, beta, D.RANG * ARCSEC * par["DA"][i], Wt)
        for j, k in enumerate(keys): out[k][i] = s[j] / 1.0e3
    return out, AMP

def q3(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) == 0: return [float("nan")] * 3
    return [float(np.median(x)), float(np.percentile(x, 16)), float(np.percentile(x, 84))]

def ghat(m):
    """slope at which the median d crosses zero; m = median d on GS (shallow to steep, decreasing)."""
    if m[0] <= 0: return -np.inf
    if m[-1] > 0: return np.inf
    for j in range(len(GS) - 1):
        if m[j] > 0 >= m[j + 1]:
            return GAM[GS[j]] + (GAM[GS[j + 1]] - GAM[GS[j]]) * m[j] / (m[j] - m[j + 1])
    return float("nan")
def gtxt(v):
    return "<0" if v == -np.inf else ">2.5" if v == np.inf else "%.2f" % v
def gsent(v):
    return np.where(np.isneginf(v), -1.0, np.where(np.isposinf(v), 3.5, v))
def gint(v):
    lo, hi = np.percentile(gsent(np.asarray(v, float)), [2.5, 97.5])
    return ("<0" if lo < -0.5 else "%.2f" % lo), (">2.5" if hi > 3.0 else "%.2f" % hi)

def load_slacs():
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}; SL = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"): continue
        qq = l.split("\t")
        if len(qq) < len(hdr): continue
        d = dict(zl=E.fl(qq[col["zlens"]]), zs=E.fl(qq[col["zsrc"]]), RE=E.fl(qq[col["RE"]]), lME=E.fl(qq[col["Mass"]]),
                 Fs=E.fl(qq[col["Fs"]]), ReV=E.fl(qq[col["Re(V)"]]), sig=E.fl(qq[col["sigma"]]))
        if all(np.isfinite(list(d.values()))) and d["RE"] > 0 and d["sig"] > 0: SL.append(d)
    return SL

# ================================================================== main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    t0 = time.time(); tag = "euc8" + ("_MUTATE_" + MUT if MUT else "")
    P("EUC8 (WIDE-LENS RESIDUAL PROFILE)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    RES = dict(lane="EUC8", criteria_commit="1c56b3f50c", clarification_commit="fa59e21652", mutate=MUT, footings=E.FOOT)
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Sm, _ = E.select(rows, ("A", "B")); byid = {r["id"]: r for r in Sm}
    scj = json.load(open(os.path.join(EUC5, "euc5_a2_scale.json")))["scale"]; SC, SC_LO, SC_HI = scj
    WLO, WHI = math.log10(SC_HI / SC), math.log10(SC / SC_LO)          # widening below / above, in log10 sigma

    # ---------------------------------------------------------------- dispersion sample (EUC5 A1's selection)
    best = {}
    for r in csv.DictReader(open(os.path.join(EUC5, "euc5_a1_dispersions.csv"))):
        s, e, V, npx = float(r["sigma"]), float(r["err"]), float(r["V"]), int(r["npix"])
        if not (np.isfinite(s) and 70 <= s <= 500 and e > 0 and e / s <= 0.25 and abs(V) <= 300 and npx >= 800): continue
        prim = r["primary"] in ("True", "true", "1"); k = r["unique_identifier"]
        cand = dict(s=s, e=e, z=float(r["z_ref"]), prim=prim)
        if k not in best or (prim and not best[k]["prim"]) or (prim == best[k]["prim"] and e / s < best[k]["e"] / best[k]["s"]): best[k] = cand
    sel = [byid[i] for i in sorted(best) if i in byid]; ND = len(sel)
    zl = np.array([best[r["id"]]["z"] for r in sel]); vfit = np.array([best[r["id"]]["s"] for r in sel]); ferr = np.array([best[r["id"]]["e"] / best[r["id"]]["s"] for r in sel])
    lmD = E.arr(sel, "lm") + 2.0 * np.log10(E.EUCLID.DL(zl) / E.EUCLID.DL(E.arr(sel, "z")))
    engD, zD, RED, ReD, nD, lmD = E.build(sel, z=zl, lm=lmD)
    parD = dict(Ms=10.0 ** lmD * MSUN, Re=ReD, n=nD, DA=E.EUCLID.DA(zl)); tED = E.arr(sel, "tE")
    sig0 = vfit / SC; sig = sig0 * SIGF
    LD = Lens2(RED, ReD, nD, parD["Ms"])
    MtD = {c: math.pi * RED ** 2 * E.EUCLID.sigcr(zD, zs_case(zD, c)) for c in CASES}
    mD = tED >= 1.3

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    Lk = Lens2(np.array([10.0 * KPC]), np.array([5.0 * KPC]), np.array([4.0]), np.array([1.0e11 * MSUN]))
    Mp = 3.0e11 * MSUN; e3a = abs(float(Lk.M2D(0.0, np.array([Mp]), G / Lk.r ** 2, 1.0e-30)[0]) / Mp - 1.0)
    s2 = (250.0e3) ** 2; ana = 2.0 * s2 * 10.0 * KPC / G * math.acos(10.0 / 1.0e6)
    e3b = abs(float(Lk.M2D(0.0, np.array([1.0]), 2.0 * s2 / Lk.r, 1.0e-30)[0]) / ana - 1.0)
    ck("K3", "projection, Newtonian limit: point mass and isothermal field to 1e-4", "%.1e ; %.1e" % (e3a, e3b), e3a < 1e-4 and e3b < 1e-4)
    SL = load_slacs()
    if not MUT:
        Bm, _ = E.select(rows, ("B",)); WB = [r for r in Bm if r["tE"] >= 1.7]
        eng, z, RE, Re, n, lm = E.build(WB); Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        f = [E.stats(eng.solve_b(Mmin, a0, "S"))["f25"] for a0 in E.FOOT.values()]
        ck("K1", "EUC4 reproduced: grade B, theta_E >= 1.7, N = 124, f25 = 0.758 / 0.702", "N = %d, %.3f / %.3f" % (len(WB), f[0], f[1]),
           len(WB) == 124 and abs(f[0] - 0.758) <= 0.001 and abs(f[1] - 0.702) <= 0.001)
        Wm = [r for r in Sm if r["tE"] >= 1.7]
        eng, z, RE, Re, n, lm = E.build(Wm); Ms = 10.0 ** lm * MSUN; Lw = Lens2(RE, Re, n, Ms); Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        e2 = 0.0; n2 = 0
        for a0 in E.FOOT.values():
            binf = eng.solve_b(Mmin, a0, "S"); A, need = Lw.solve(Mmin, 1.0, Lw.gx("T"), a0)
            e2 = max(e2, float(np.max(np.abs((A[need] / Ms[need]) / (10.0 ** binf[need] - 1.0) - 1.0)))); n2 += int(need.sum())
        ck("K2", "two-component solver against EUC1's (family T amplitude = 10^b_inf - 1) to 1e-4", "max rel. error %.1e on %d lens solutions" % (e2, n2), e2 < 1e-4)
        # K4 (clarification C1): per-lens equivalence on SLACS
        a0k = 1.132e-10
        zls = np.array([d["zl"] for d in SL]); zss = np.array([d["zs"] for d in SL]); DAs = E.AUGER.DA(zls)
        REs = np.array([d["RE"] for d in SL]) * KPC; Res = np.array([d["ReV"] for d in SL]) * ARCSEC * DAs; n4 = np.full(len(SL), 4.0)
        Mss = np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / E.M2D_frac(REs, Res, 4.0) * MSUN
        MtS = math.pi * REs ** 2 * E.AUGER.sigcr(zls, zss); LS = Lens2(REs, Res, n4, Mss); parS = dict(Ms=Mss, Re=Res, n=n4, DA=DAs)
        bl = E.Engine(REs, Res, n4, Mss).solve_b(MtS, a0k, "S")
        kT = ("alt", "T", 0.0, "true", RT); prS, amS = predict_set(LS, parS, [kT], {"true": MtS}, 1.5, 1.5)
        ref = np.array([float(np.exp(np.interp(bl[i], D.LB, np.log(D.sig_of_B(Mss[i], Res[i], 4.0, DAs[i], a0k, "S", 0.0, 1.5, 1.5))))) / 1.0e3 for i in range(len(SL))])
        nz = amS[kT] > 0; e4 = float(np.max(np.abs(prS[kT][nz] / ref[nz] - 1.0)))
        sigS = np.array([d["sig"] for d in SL])
        ck("K4", "SLACS, family T, alt: per-lens dispersion equals EUC5's sig_of_B at b_lens to 0.5% (N >= 30)",
           "max difference %.2e on %d lenses with a non-zero amplitude (of %d); full-sample median predicted/measured %.4f (EUC5 J3: 0.9663)"
           % (e4, int(nz.sum()), len(SL), np.median(prS[kT] / sigS)), e4 <= 0.005 and int(nz.sum()) >= 30)
        bd = np.array([D.b_dyn(sig0[i] * 1.0e3, parD["Ms"][i], ReD[i], nD[i], parD["DA"][i], 9.3603e-11, "S", 0.0, 0.75, 1.1) for i in range(ND)])
        ck("K5", "EUC5's class reading reproduced: theta_E >= 1.3, N = 25, b_dyn = +0.200 canonical (+-0.003)", "N = %d, %+.4f" % (int(mD.sum()), np.median(bd[mD])),
           int(mD.sum()) == 25 and abs(float(np.median(bd[mD])) - 0.200) <= 0.003)

    # ---------------------------------------------------------------- Part B predictions
    keys = [(nm, fam, bs, c, RT) for nm in E.FOOT for fam in FAMS for bs in BSTAR for c in CASES]
    pred, amp = predict_set(LD, parD, keys, MtD, 0.75, 1.1)
    rng = np.random.default_rng(E.SEED)
    def dstat(sg, pr, m, idx):
        d = np.log10(sg[m] / pr[m]); b = np.median(d[idx], axis=1); lo, hi = np.percentile(b, [2.5, 97.5])
        return dict(med=float(np.median(d)), lo=float(lo), hi=float(hi), lo_w=float(lo - WLO), hi_w=float(hi + WHI))
    def gam_block(sg, prd, m, idx, nm, c, bs=0.0, rt=RT):
        dm = np.array([np.log10(sg[m] / prd[(nm, g, bs, c, rt)][m]) for g in GS])
        pt = ghat(np.median(dm, axis=1)); bb = np.array([ghat(np.median(dm[:, ix], axis=1)) for ix in idx])
        lo, hi = gint(bb)
        return dict(gamma=gtxt(pt), lo=lo, hi=hi, scale_lo=gtxt(ghat(np.median(dm, axis=1) - WLO)), scale_hi=gtxt(ghat(np.median(dm, axis=1) + WHI)))
    idxD = rng.integers(0, int(mD.sum()), (2000, int(mD.sum())))

    if not MUT:
        k2 = ("canonical", "2.0", 0.0, "central", RT); mock = pred[k2].copy()
        dm = np.array([np.log10(mock[mD] / pred[("canonical", g, 0.0, "central", RT)][mD]) for g in GS]); g6 = ghat(np.median(dm, axis=1))
        ck("K6", "injection, noise-free, gamma = 2 at the central case: recovered 2.00 +- 0.02", gtxt(g6), np.isfinite(g6) and abs(g6 - 2.0) <= 0.02)
    RES["checks"] = CK; allok = all(v["ok"] for v in CK.values())

    # ---------------------------------------------------------------- Part A
    def part_a():
        eng, z, RE, Re, n, lm = E.build(Sm); Ms = 10.0 ** lm * MSUN; tE = E.arr(Sm, "tE"); N = len(Sm); L = Lens2(RE, Re, n, Ms)
        cls = (("W theta_E >= 1.7", tE >= 1.7), ("1.3 - 1.7", (tE >= 1.3) & (tE < 1.7)), ("1.0 - 1.3", (tE >= 1.0) & (tE < 1.3)), ("below 1.0", tE < 1.0))
        rhoc = SHARE * OMB * RHOC * (1.0 + z) ** 3; A_res = {}; per = {}
        P("\n[Part A: the requirement; law S, stars at the catalogued Salpeter mass (b_star = 0)]")
        P("  cosmic mean cold density used: %.2f x Omega_b x rho_crit (1+z)^3, rho_crit = %.3e kg/m^3" % (SHARE, RHOC))
        for nm, a0 in E.FOOT.items():
            base = L.M2D(1.0, np.zeros(N), 0.0, a0)
            for case in ("far", "central"):
                Mt = math.pi * RE ** 2 * E.EUCLID.sigcr(z, zs_case(z, case)); need = Mt > base; dM = np.where(need, Mt - base, 0.0)
                Sig = dM / (math.pi * RE ** 2); per[(nm, case)] = (dM, Sig, Mt)
                fam = {}
                for f in FAMS:
                    A, _ = L.solve(Mt, 1.0, L.gx(f), a0)
                    Min = A * mfrac(f, RE, Re, n); M300 = A * mfrac(f, np.full(N, RT), Re, n)
                    if f == "P": rho = np.full(N, np.nan)
                    elif f == "T": rho = A * (E.M3D_frac(RE * 1.001, Re, n) - E.M3D_frac(RE * 0.999, Re, n)) / (0.002 * RE) / (4.0 * math.pi * RE ** 2)
                    else: rho = A * (3.0 - GAM[f]) / (4.0 * math.pi * RT ** 3) * (RE / RT) ** (-GAM[f])
                    Vc2 = E.g_law(G * (Ms * E.M3D_frac(RE, Re, n) + Min) / RE ** 2, a0, "S") * RE
                    w = Vc2 / (GAM[f] * C * C) if (f in GAM and GAM[f] > 0) else np.full(N, np.nan)
                    fam[f] = (Min, M300, rho / rhoc, w, np.sqrt(Vc2))
                for cn, m in cls:
                    row = dict(N=int(m.sum()), frac_need=float(np.mean(need[m])), dM_Msun=q3(dM[m] / MSUN), Sigma_Msun_pc2=q3(Sig[m] / SIG_UNIT),
                               Sigma_in_a0_2piG=q3(Sig[m] / (a0 / (2.0 * math.pi * G))), share=q3(dM[m] / Mt[m]), RE_kpc=q3(RE[m] / KPC), fam={})
                    mm = m & need
                    for f in FAMS:
                        Min, M300, over, w, Vc = fam[f]
                        row["fam"][f] = dict(M_in_RE=q3(Min[m] / MSUN), M_300=q3(M300[m] / MSUN), M_300_over_Mstar=q3(M300[m] / Ms[m]),
                                             overdensity=q3(over[mm]), w=q3(w[mm]), Vc_kms=q3(Vc[mm] / 1.0e3))
                    A_res["%s|%s|%s" % (cn, nm, case)] = row
        for nm in E.FOOT:
            for case in ("far", "central"):
                P("\n  %s footing, %s source case:" % (nm, case))
                P("    class              N    need   R_E kpc   excess mass (Msun) [16-84%]         Sigma (Msun/pc^2)   in a0/(2 pi G)   share of lensing mass")
                for cn, _ in cls:
                    r = A_res["%s|%s|%s" % (cn, nm, case)]
                    P("    %-17s %5d  %.3f   %5.1f    %.2e [%.2e, %.2e]    %6.0f [%4.0f, %5.0f]   %6.2f           %.3f [%.3f, %.3f]"
                      % (cn, r["N"], r["frac_need"], r["RE_kpc"][0], r["dM_Msun"][0], r["dM_Msun"][1], r["dM_Msun"][2], r["Sigma_Msun_pc2"][0], r["Sigma_Msun_pc2"][1],
                         r["Sigma_Msun_pc2"][2], r["Sigma_in_a0_2piG"][0], r["share"][0], r["share"][1], r["share"][2]))
                r = A_res["W theta_E >= 1.7|%s|%s" % (nm, case)]
                P("    class W by family:  mass inside R_E sphere | inside 300 kpc | as a multiple of M* | density at R_E / cosmic mean cold | w = Vc^2/(gamma c^2) | Vc km/s")
                for f in FAMS:
                    x = r["fam"][f]
                    P("      %-5s  %.2e | %.2e [%.1e, %.1e] | %8.1f | %s | %s | %.0f"
                      % (("gamma " if f in GAM else "") + f, x["M_in_RE"][0], x["M_300"][0], x["M_300"][1], x["M_300"][2], x["M_300_over_Mstar"][0],
                         ("%.2e" % x["overdensity"][0]) if np.isfinite(x["overdensity"][0]) else "   -    ", ("%.2e" % x["w"][0]) if np.isfinite(x["w"][0]) else "   -    ", x["Vc_kms"][0]))
        if not MUT:
            mW = tE >= 1.7
            with open(os.path.join(HERE, "euc8_wide_per_lens.csv"), "w", newline="") as fcsv:
                w_ = csv.writer(fcsv); w_.writerow(["unique_identifier", "grade", "z_lens", "theta_E_arcsec", "R_E_kpc", "log_Mstar", "excess_far_canonical_Msun", "excess_far_alt_Msun",
                                                    "excess_central_canonical_Msun", "excess_central_alt_Msun", "Sigma_far_canonical_Msun_pc2"])
                for i in np.where(mW)[0]:
                    w_.writerow([Sm[i]["id"], Sm[i]["grade"], "%.3f" % z[i], "%.3f" % tE[i], "%.2f" % (RE[i] / KPC), "%.3f" % lm[i]] +
                                ["%.4e" % (per[k][0][i] / MSUN) for k in (("canonical", "far"), ("alt", "far"), ("canonical", "central"), ("alt", "central"))] +
                                ["%.1f" % (per[("canonical", "far")][1][i] / SIG_UNIT)])
        return A_res
    if MUT in ("", "newton"): RES["partA"] = part_a()
    if MUT == "newton":
        ref = json.load(open(os.path.join(HERE, "euc8_results.json")))["partA"]
        kk = ["W theta_E >= 1.7|%s|far" % nm for nm in E.FOOT]
        up = all(RES["partA"][k]["dM_Msun"][0] > ref[k]["dM_Msun"][0] for k in kk)
        P("\n[MUTATE newton] median far-case excess of W: %.3e / %.3e Msun (ref %.3e / %.3e) -> %s" % (RES["partA"][kk[0]]["dM_Msun"][0], RES["partA"][kk[1]]["dM_Msun"][0],
          ref[kk[0]]["dM_Msun"][0], ref[kk[1]]["dM_Msun"][0], "rose on both footings, as required; exit 1" if up else "DID NOT RISE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if up else 2)

    # ---------------------------------------------------------------- Part B words
    P("\n[Part B: how concentrated; sample D = DESI-dispersion lenses, theta_E >= 1.3 arcsec]")
    P("  lenses with a qualifying dispersion %d; in D %d; medians in D: z_l %.3f, theta_E %.2f\", sigma on the SLACS scale %.0f km/s (error %.0f%%), log M* %.2f"
      % (ND, int(mD.sum()), np.median(zD[mD]), np.median(tED[mD]), np.median(sig[mD]), 100 * np.median(ferr[mD]), np.median(lmD[mD])))
    P("  fibre radius / Einstein radius in D: median %.2f;  scale %.4f [%.4f, %.4f] -> intervals widened by -%.4f / +%.4f in log10 sigma" % (np.median(0.75 / tED[mD]), SC, SC_LO, SC_HI, WLO, WHI))
    PB = {}; words = {nm: {} for nm in E.FOOT}
    for nm in E.FOOT:
        P("\n  %s footing.  d = log10(sigma measured / predicted): median [widened 95%%], b_star = 0" % nm)
        P("    family      far                        central                    near                       | far upper bound at b* -0.10 / 0 / +0.10 | near lower bound       | word")
        for fam in FAMS:
            st = {(bs, c): dstat(sig, pred[(nm, fam, bs, c, RT)], mD, idxD) for bs in BSTAR for c in CASES}
            conc = all(st[(bs, "far")]["hi_w"] < 0 for bs in BSTAR); diff = all(st[(bs, "near")]["lo_w"] > 0 for bs in BSTAR)
            wd = "TOO CONCENTRATED" if conc else "TOO DIFFUSE" if diff else "ALLOWED"; words[nm][fam] = wd
            PB["%s|%s" % (nm, fam)] = dict(word=wd, stats={"%+.2f|%s" % k: v for k, v in st.items()})
            P("    %-10s  %s  %s  %s | %+.3f / %+.3f / %+.3f               | %+.3f / %+.3f / %+.3f | %s"
              % (("gamma " if fam in GAM else "") + fam, *["%+.3f [%+.3f, %+.3f]" % (st[(0.0, c)]["med"], st[(0.0, c)]["lo_w"], st[(0.0, c)]["hi_w"]) for c in CASES],
                 *[st[(bs, "far")]["hi_w"] for bs in BSTAR], *[st[(bs, "near")]["lo_w"] for bs in BSTAR], wd))
    lane = {}
    for nm in E.FOOT:
        w = words[nm]; anyok = any(v == "ALLOWED" for v in w.values()); dif0 = w["0.0"] == "TOO DIFFUSE"; conT = w["T"] == "TOO CONCENTRATED"
        if int(mD.sum()) < 10 or (not MUT and not allok): lane[nm] = "NOT EVALUABLE"
        elif not anyok: lane[nm] = "NO FAMILY FITS"
        elif dif0 and conT: lane[nm] = "SLOPE BRACKETED"
        elif dif0: lane[nm] = "RESIDUAL MUST BE CONCENTRATED"
        elif conT: lane[nm] = "RESIDUAL MUST BE EXTENDED"
        else: lane[nm] = "SLOPE NOT CONSTRAINED"
    verdict = "%s / %s" % (lane["canonical"], lane["alt"]); RES["partB"] = PB; RES["family_words"] = words; RES["verdict"] = verdict
    P("\n  LANE WORD (canonical / alt): %s" % verdict)
    if MUT:
        fam, want = ("0.0", "TOO DIFFUSE") if MUT == "sigup" else ("T", "TOO CONCENTRATED")
        ok = all(words[nm][fam] == want for nm in E.FOOT)
        P("\n[MUTATE %s] dispersions x %.2f: family %s reads %s / %s -> %s" % (MUT, SIGF, fam, words["canonical"][fam], words["alt"][fam],
          "%s on both footings, as required; exit 1" % want if ok else "DID NOT FIRE"))
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ok else 2)

    # ---------------------------------------------------------------- reported, no word
    P("\n[reported: the slope gamma-hat at which the class median d crosses zero; b_star = 0; 95% bootstrap interval; (range over the scale interval)]")
    REP = {}
    for cn, m in (("theta_E >= 1.3 (D)", mD), ("theta_E >= 1.7", tED >= 1.7), ("1.3 - 1.7", (tED >= 1.3) & (tED < 1.7)), ("1.0 - 1.3", (tED >= 1.0) & (tED < 1.3)), ("below 1.0", tED < 1.0)):
        if m.sum() < 5: P("  %-19s N = %d: too few" % (cn, int(m.sum()))); continue
        ix = idxD if cn.endswith("(D)") else np.random.default_rng(E.SEED).integers(0, int(m.sum()), (2000, int(m.sum())))
        for nm in E.FOOT:
            row = {c: gam_block(sig, pred, m, ix, nm, c) for c in CASES}
            for f in ("P", "T"):
                row["d_" + f] = {c: dstat(sig, pred[(nm, f, 0.0, c, RT)], m, ix)["med"] for c in CASES}
            REP["%s|%s" % (cn, nm)] = dict(N=int(m.sum()), **row)
            P("  %-19s N = %2d %-9s  far %5s [%s, %s] (%s to %s)   central %5s [%s, %s] (%s to %s)   near %5s [%s, %s] (%s to %s)   median d of T: %+.3f / %+.3f / %+.3f"
              % (cn, int(m.sum()), nm, *[x for c in CASES for x in (row[c]["gamma"], row[c]["lo"], row[c]["hi"], row[c]["scale_lo"], row[c]["scale_hi"])],
                 *[row["d_T"][c] for c in CASES]))
    RES["gamma_hat"] = REP

    P("\n[reported: stellar normalisation, class D, gamma-hat far / central / near]")
    for bs in BSTAR:
        P("  b_star %+.2f:  " % bs + "   ".join("%-9s %s / %s / %s" % (nm, *[gam_block(sig, pred, mD, idxD, nm, c, bs)["gamma"] for c in CASES]) for nm in E.FOOT))

    P("\n[reported: anisotropy and truncation radius, class D, b_star = 0, gamma-hat far / central / near]")
    VAR = {}
    for lab, beta in (("beta = -0.2", -0.2), ("beta = +0.2", 0.2)):
        kv = [(nm, fam, 0.0, c, RT) for nm in E.FOOT for fam in FAMS for c in CASES]; pv, _ = predict_set(LD, parD, kv, MtD, 0.75, 1.1, beta)
        VAR[lab] = {nm: [gam_block(sig, pv, mD, idxD, nm, c)["gamma"] for c in CASES] for nm in E.FOOT}
        VAR[lab + " d_T"] = {nm: [dstat(sig, pv[(nm, "T", 0.0, c, RT)], mD, idxD)["med"] for c in CASES] for nm in E.FOOT}
        P("  %-12s  " % lab + "   ".join("%-9s %s / %s / %s (T: %+.3f / %+.3f / %+.3f)" % (nm, *VAR[lab][nm], *VAR[lab + " d_T"][nm]) for nm in E.FOOT))
    for rt in (150.0 * KPC, 600.0 * KPC):
        kv = [(nm, g, 0.0, c, rt) for nm in E.FOOT for g in GS for c in CASES]; pv, _ = predict_set(LD, parD, kv, MtD, 0.75, 1.1)
        lab = "r_t = %.0f kpc" % (rt / KPC); VAR[lab] = {nm: [gam_block(sig, pv, mD, idxD, nm, c, 0.0, rt)["gamma"] for c in CASES] for nm in E.FOOT}
        P("  %-12s  " % lab + "   ".join("%-9s %s / %s / %s" % (nm, *VAR[lab][nm]) for nm in E.FOOT))
    RES["variants"] = VAR

    P("\n[reported: SLACS at its true source redshifts (fibre 1.5 arcsec, seeing 1.5 arcsec, published dispersions), N = %d]" % len(SL))
    kS = [(nm, fam, bs, "true", RT) for nm in E.FOOT for fam in FAMS for bs in BSTAR]; prS, amS = predict_set(LS, parS, kS, {"true": MtS}, 1.5, 1.5)
    mS = np.ones(len(SL), bool); ixS = np.random.default_rng(E.SEED).integers(0, len(SL), (2000, len(SL))); SLR = {}
    for nm in E.FOOT:
        for bs in BSTAR:
            dm = np.array([np.log10(sigS / prS[(nm, g, bs, "true", RT)]) for g in GS]); pt = ghat(np.median(dm, axis=1))
            lo, hi = gint(np.array([ghat(np.median(dm[:, ix], axis=1)) for ix in ixS]))
            dT = np.log10(sigS / prS[(nm, "T", bs, "true", RT)]); dP = np.log10(sigS / prS[(nm, "P", bs, "true", RT)])
            SLR["%s|%+.2f" % (nm, bs)] = dict(gamma=gtxt(pt), lo=lo, hi=hi, d_T=float(np.median(dT)), d_P=float(np.median(dP)), d=[float(x) for x in np.median(dm, axis=1)],
                                              frac_need=float(np.mean(amS[(nm, "T", bs, "true", RT)] > 0)))
            P("  %-9s b_star %+.2f: gamma-hat %5s [%s, %s];  median d: P %+.3f, T %+.3f, gamma 2.5 / 2 / 1.5 / 1 / 0: %s;  lenses needing any extra mass %.2f"
              % (nm, bs, gtxt(pt), lo, hi, np.median(dP), np.median(dT), " / ".join("%+.3f" % x for x in np.median(dm, axis=1)[::-1]), SLR["%s|%+.2f" % (nm, bs)]["frac_need"]))
    RES["slacs"] = SLR

    P("\n[reported: sensitivity on mocks (class D's structure and dispersion errors; canonical; central case; b_star = 0; 500 noise draws)]")
    k175 = [("canonical", "1.75", 0.0, "central", RT)]; p175, _ = predict_set(LD, parD, k175, MtD, 0.75, 1.1)
    dm = np.array([np.log10(p175[k175[0]][mD] / pred[("canonical", g, 0.0, "central", RT)][mD]) for g in GS])
    P("  noise-free, injected gamma = 1.75 (off the grid): recovered %s" % gtxt(ghat(np.median(dm, axis=1))))
    rngm = np.random.default_rng(E.SEED + 1); MOCK = {}
    for inj in ("2.0", "1.0", "0.0", "T"):
        base = pred[("canonical", inj, 0.0, "central", RT)][mD]; got = []
        for _ in range(500):
            mk = base * (1.0 + ferr[mD] * rngm.standard_normal(int(mD.sum())))
            got.append(ghat(np.median(np.array([np.log10(np.maximum(mk, 1.0) / pred[("canonical", g, 0.0, "central", RT)][mD]) for g in GS]), axis=1)))
        got = np.array(got); s = gsent(got)
        MOCK[inj] = dict(median=float(np.median(s)), p16=float(np.percentile(s, 16)), p84=float(np.percentile(s, 84)), below0=float(np.mean(np.isneginf(got))), above25=float(np.mean(np.isposinf(got))))
        stxt = lambda v: "<0" if v < -0.5 else ">2.5" if v > 3.0 else "%.2f" % v
        P("  injected %-9s recovered gamma-hat: median %s, 16-84%% %s to %s;  off the low end (<0) %.2f, off the high end (>2.5) %.2f"
          % (("gamma " + inj) if inj in GAM else "family T", stxt(np.median(s)), stxt(np.percentile(s, 16)), stxt(np.percentile(s, 84)), MOCK[inj]["below0"], MOCK[inj]["above25"]))
    RES["mocks"] = MOCK

    with open(os.path.join(HERE, "euc8_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["unique_identifier", "grade", "z_ref", "theta_E_arcsec", "sigma_slacs_scale_kms", "frac_err"] +
                                      ["pred_%s_%s_kms" % (fam, c) for fam in FAMS for c in CASES] + ["amp_T_far_over_Mstar", "amp_gamma2_far_Msun"])
        for i, r in enumerate(sel):
            w.writerow([r["id"], r["grade"], "%.4f" % zl[i], "%.3f" % tED[i], "%.1f" % sig[i], "%.3f" % ferr[i]] +
                       ["%.1f" % pred[("canonical", fam, 0.0, c, RT)][i] for fam in FAMS for c in CASES] +
                       ["%.4f" % (amp[("canonical", "T", 0.0, "far", RT)][i] / parD["Ms"][i]), "%.4e" % (amp[("canonical", "2.0", 0.0, "far", RT)][i] / MSUN)])
    RES["checks_all_pass"] = allok
    P("\n[summary]")
    P("  instrument checks K1-K6: %s" % ("all pass" if allok else "FAILED -> NOT EVALUABLE"))
    P("  LANE WORD (canonical / alt): %s" % verdict)
    P("  kappa = 1/2 FITTED. A test lane; adopts nothing. No outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
