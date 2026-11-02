#!/usr/bin/env python3
"""LM1 map (FROZEN_CRITERIA.md): the law's missing mass, measured. No rule, no mechanism, no cold sector. Reads lm1_grade.py's dumps and other lanes read only.
    python3 lm1_map.py [--mutate]
kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np, warnings; warnings.simplefilter("ignore")
from astropy.io import fits
from scipy.special import gamma as Gam
from scipy.stats import chi2 as CH2, spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; OUT = []; RES = {}; CHK = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(n, ok, t): CHK.append((n, bool(ok))); P(f"{n} {'PASS' if ok else 'FAIL'}: {t}")
ZLE = 3.34; PLE = 8.27e-4; NB = 2000; SEED = 20261101; FEET = ("canonical", "alt"); A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); AX = 1.5 if MUT else 1.0
G, MS, MPCm, PCm = 6.674e-11, 1.989e30, 3.0857e22, 3.0857e16
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); N = len(X["name"]); HI = {"h0672": 1, "h0686": 2}; HX = {"h0672": 0, "h0686": 1}; names = [str(x).strip() for x in X["name"]]; Mg0 = np.asarray(X["Mgas500"], float); zc = np.asarray(X["z"], float)
RRd = np.load(os.path.join(RB, "M3A1_outer_key_audit", "m3a1_randoms.npz"))
def DP(job): return np.load(os.path.join(HERE, f"cache_{job}", "dump.npz"))
def KJ(job): return json.load(open(os.path.join(HERE, f"cache_{job}", "keys.json")))
B_ = DP("MUTATE_f034" if MUT else "BASE_f034"); RC = B_["RC"]; T3 = B_["T3M"]; PATCH = B_["PATCH"]; TID = B_["TID"]; II = B_["I"]; IB, MB, OB = [0, 1, 2], [3, 4, 5], [6, 7]; BAND = dict(INNER=IB, MID=MB, OUTER=OB); XB = [(0.2, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 5.0)]
FH = np.array([1.021, 1.038, 1.089, 1.114, 1.149, 1.139]); GRZ = np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5])
def nsum(h, D=None, B=None, leak=None):
    i = HI[h]; W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B0 = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); Bv = B0[None, :] if B is None else B; D = X["D"][:, i] if D is None else D; L = X["leakP"][:, HX[h], 0] if leak is None else leak; return W * Bv * (D - L), W
def Btercile(h):
    i = HI[h]; O = np.zeros((N, 8))
    for t in range(3): O[T3 == t] = X["den"][T3 == t, i].sum(0) / X["den_r"][T3 == t, i].sum(0)
    return O
class Cell:
    def __init__(s, d, foot, h, fs, D=None, B=None, leak=None, Fz=None, Vadd=None, mfac=None):
        q = f"{foot}_{h}"; s.foot, s.h, s.fs = foot, h, fs; n, W = nsum(h, D, B, leak); n = n if Fz is None else n * Fz[:, None]; s.n, s.W = n, W; s.V = d["V_" + q] + (0 if Vadd is None else Vadd); s.VN = d["VN_" + q]; s.VNg = s.VN / (1 + fs); s.Mb = d["Mb_" + q]; s.ML = d["ML_" + q]; s.R5 = d["R500_" + h]; s.e = n - s.V; s.Mg = Mg0 if mfac is None else Mg0 * mfac; s.x = RC[None, :] / s.R5[:, None]; s.gN = G * s.Mb * MS / (RC * MPCm) ** 2 / (A0[foot] * AX); s.SigN = np.where(W > 0, s.VN / np.where(W > 0, W, 1), np.nan); s.vC = d["vC_" + q]
GRID = np.arange(-3, 3.0001, 0.01); rng0 = lambda: np.random.default_rng(SEED)
def BOOT(n=NB, N_=N): return rng0().integers(0, N_, (n, N_))
def fit1(e, v, w, x, c=None):
    """e_i = C v_i x_i^p; chi^2 with 1/w_i. returns p, C, edge flag."""
    ok = w > 0; e, v, w, x = e[ok], v[ok], w[ok], x[ok]; c = 1.0 if c is None else c[ok]; F = np.exp(np.outer(GRID, np.log(x))); a = (c * e * v / w) * F; b = (c * v * v / w) * F * F; nu = a.sum(1); de = b.sum(1); g = nu * nu / de; k = int(np.argmax(g)); return GRID[k], nu[k] / de[k], k in (0, len(GRID) - 1)
def counts(idx): return np.bincount(idx, minlength=N).astype(float)
def fitb(e, v, w, x, nb=NB, nulls=0.0, sub=None):
    p, C, ed = fit1(e, v, w, x); B = BOOT(nb); Ps = []; E = 0
    for r in B:
        c = counts(r); a, _, ee = fit1(e, v, w, x, c); Ps.append(a); E += ee
    sb = float(np.std(Ps)); J = []
    for pt in range(30):
        m = PATCH != pt; J.append(fit1(e[m], v[m], w[m], x[m])[0])
    J = np.array(J); sj = float(np.sqrt(29 / 30 * ((J - J.mean()) ** 2).sum())); return dict(v=float(p), C=float(C), s_boot=sb, s_jack=sj, s=max(sb, sj), edge=int(E), edge0=bool(ed))
def label(val, null, sig, prec, n7=False):
    sig = sig * (2 if n7 else 1); t = (val - null) / sig if sig > 0 else float("inf")
    if abs(t) >= ZLE: L = "TREND"
    elif abs(t) < 2 and sig <= prec: L = "CONSTANT"
    else: L = "NOISE-LIMITED" + (" [hint]" if abs(t) >= 2 else "")
    return dict(val=float(val), null=float(null), s=float(sig), t=float(t), label=L + (" [N=7]" if n7 else ""))
def lchi(chi, dof, frac):
    p = float(CH2.sf(chi, dof)) if dof > 0 else float("nan"); L = "TREND" if p <= PLE else ("CONSTANT" if (p > 0.05 and frac < 0.30) else "NOISE-LIMITED"); return dict(chi2=float(chi), dof=int(dof), p=p, frac=float(frac), label=L)
def bandsum(c, mask):
    return (c.e * mask).sum(1), (c.W * mask).sum(1), (c.VNg * mask).sum(1)
def physmask(j): m = np.zeros((N, 8), bool); m[:, j] = True; return m
def xmask(c, lo, hi): return (c.x >= lo) & (c.x < hi)
def stack(c, sel, nb=NB):
    """dDS per bin with bootstrap on sel."""
    sel = np.where(sel)[0]; es, Ws = c.e[sel], c.W[sel]; v = es.sum(0) / Ws.sum(0); B = rng0().integers(0, len(sel), (nb, len(sel))); R = np.array([es[r].sum(0) / Ws[r].sum(0) for r in B]); return v, R
def slope_bins(y, s, j):
    j = list(j); r = RC[j] / 1.0; F = np.exp(np.outer(GRID, np.log(r))); nu = (y[j] * F / s[j] ** 2).sum(1); de = (F * F / s[j] ** 2).sum(1); return GRID[int(np.argmax(nu * nu / de))]
def T2stat(c, j, arr, sel=None, patch=None):
    sel = np.ones(N, bool) if sel is None else sel; xs, ys = [], []
    for t in range(3):
        s = sel & (T3 == t); v = arr[s][:, j].sum() / c.W[s][:, j].sum()
        if v <= 0: return np.nan
        xs.append(np.log10(np.median(c.Mg[s]))); ys.append(np.log10(v))
    return np.polyfit(xs, ys, 1)[0]
def T2jack(c, j, arr):
    J = np.array([T2stat(c, j, arr, PATCH != p) for p in range(30)]); return T2stat(c, j, arr), float(np.sqrt(29 / 30 * np.nansum((J - np.nanmean(J)) ** 2)))
# --------------------------------------------------------- X-COP
DATA = os.path.join(REPO, "real_research", "data")
def li(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
def xcop_load():
    C = []
    for name in sorted(os.listdir(os.path.join(DATA, "xcop"))):
        p_ = os.path.join(DATA, "xcop", name)
        if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))): continue
        with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]
        with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        rows = {}
        for x in (0.1, 0.2, 0.3, 0.5, 0.7, 1.0):
            r = x * r500; mh, mg, ms = li(hm["RADIUS"], hm["M_FORW"], r), li(gas["RADIUS"] * rg500, gas["MGAS"], r), li(st["RADIUS"], st["MSTAR"], r)
            if np.all(np.isfinite([mh, mg, ms])): rows[x] = (r, mh, mg, ms)
        C.append(dict(name=name, rows=rows))
    return C
XC = xcop_load()
def law_mass(Mb, r_kpc, a0):
    rs = r_kpc * 1e3 * PCm; gb = G * Mb * MS / rs ** 2; return (0.5 * gb + np.sqrt(0.25 * gb ** 2 + a0 * gb)) * rs ** 2 / G / MS
def xcop_table(foot, shift=0.0):
    a0 = A0[foot] * AX; T = {}
    for c in XC:
        for x, (r, mh, mg, ms) in c["rows"].items():
            mh2 = mh * 10 ** shift; L = law_mass(mg + ms, r, a0); T.setdefault(x, []).append(dict(cl=c["name"], dM=mh2 - L, ratio=(mh2 - L) / mg, lgf=math.log10(mh2 / L), mg=mg, r=r, gN=G * (mg + ms) * MS / (r * 1e3 * PCm) ** 2 / a0))
    return T
# --------------------------------------------------------- main
LOOK = {}
def run_foot(foot, h="h0672", job=None, fs=0.034, verbose=True):
    d = DP(job or ("MUTATE_f034" if MUT else "BASE_f034")); c = Cell(d, foot, h, fs); R = {}; L = {}
    v, Rb = stack(c, np.ones(N, bool)); s = Rb.std(0); J = np.array([c.e[PATCH != p].sum(0) / c.W[PATCH != p].sum(0) for p in range(30)]); sj = np.sqrt(29 / 30 * ((J - J.mean(0)) ** 2).sum(0)); sg = np.maximum(s, sj); R["dDS_all"] = v.tolist(); R["dDS_all_s"] = sg.tolist()
    if verbose:
        P(f"\n=== {foot} {h} f* {fs}: surface"); P("  R Mpc   " + " ".join(f"{r:7.3f}" for r in RC)); P("  dDS all " + " ".join(f"{a:7.1f}" for a in v)); P("  +-      " + " ".join(f"{a:7.1f}" for a in sg))
    Rt = {}
    for t in range(3):
        vt, rb = stack(c, T3 == t); Rt[t] = (vt, rb); R[f"dDS_M{t + 1}"] = vt.tolist(); R[f"dDS_M{t + 1}_s"] = rb.std(0).tolist()
        Qb = c.e[T3 == t].sum(0) / c.VNg[T3 == t].sum(0); R[f"Q_M{t + 1}"] = Qb.tolist()
        if verbose: P(f"  M{t + 1} (lg Mg {np.log10(np.median(Mg0[T3 == t])):.2f}) dDS " + " ".join(f"{a:7.1f}" for a in vt)); P("     +-            " + " ".join(f"{a:7.1f}" for a in rb.std(0))); P("     Q=dM/Mgas     " + " ".join(f"{a:7.2f}" for a in Qb))
    Qall = c.e.sum(0) / c.VNg.sum(0); Rq = np.array([c.e[r].sum(0) / c.VNg[r].sum(0) for r in BOOT()]); R["Q_all"] = Qall.tolist(); R["Q_all_s"] = Rq.std(0).tolist()
    # law-relative: lensing / law
    fac = c.n.sum(0) / c.V.sum(0); R["obs_over_law"] = fac.tolist()
    # enclosed
    def m2d(y): 
        lr = np.log(RC); I = np.array([np.trapz(y[j:], lr[j:]) for j in range(8)]); return np.pi * (RC * 1e6) ** 2 * (y + 2 * I)
    M2 = m2d(v); M2b = np.array([m2d(a) for a in Rb]); R["M2Dmin"] = M2.tolist(); R["M2Dmin_s"] = M2b.std(0).tolist(); p0 = slope_bins(v, sg, range(8)); gam = 1 - p0; R["gamma"] = float(gam)
    f3 = 4 * Gam(gam / 2) / (math.sqrt(math.pi) * Gam((gam - 1) / 2) * (gam - 1)); M3D = np.pi * (RC * 1e6) ** 2 * v * f3; mgb = (c.Mb.mean(0) / (1 + fs)); R["M3D"] = M3D.tolist(); R["M3D_over_Mgas"] = (M3D / mgb).tolist(); R["M3D_f3"] = float(f3)
    if verbose: P("  Q all   " + " ".join(f"{a:7.2f}" for a in Qall) + "  (projected dM/Mgas)"); P("  +-      " + " ".join(f"{a:7.2f}" for a in Rq.std(0))); P("  obs/law " + " ".join(f"{a:7.2f}" for a in fac)); P("  M2D_min " + " ".join(f"{a:7.1e}" for a in M2) + " Msun (sheet 0)"); P("  +-      " + " ".join(f"{a:7.1e}" for a in M2b.std(0))); P(f"  M3D, local power law, gamma {gam:.2f}: " + " ".join(f"{a:7.1e}" for a in M3D)); P("  M3D/Mgas(<R) mean-gas " + " ".join(f"{a:7.2f}" for a in M3D / mgb))
    # L01-05
    S0 = slope_bins(v, sg, range(8)); S0b = np.array([slope_bins(a, sg, range(8)) for a in Rb]); R["slope_all"] = (float(S0), float(S0b.std()))
    for lk, j in (("L01", IB), ("L02", MB), ("L03", OB)):
        sv = slope_bins(v, sg, j); sb = np.array([slope_bins(a, sg, j) for a in Rb]); ds = float((sb - S0b).std()); L[lk] = dict(label(sv, S0, ds, 0.30), name=f"slope dDS {j}", s_raw=float(sb.std()))
    Cv = np.cov(Rb.T); Cv = 0.95 * Cv + 0.05 * np.diag(np.diag(Cv)); Ci = np.linalg.inv(Cv); F = np.exp(np.outer(GRID, np.log(RC))); best = 1e99
    for f_ in F:
        A = (f_ @ Ci @ v) / (f_ @ Ci @ f_); rr = v - A * f_; best = min(best, float(rr @ Ci @ rr))
    L["L04"] = dict(lchi(best, 6, float(np.median(sg / np.abs(v)))), name="one power law, 8 bins")
    j5 = MB + OB; s1 = slope_bins(Rt[0][0], Rt[0][1].std(0), j5); s3 = slope_bins(Rt[2][0], Rt[2][1].std(0), j5); b1 = np.array([slope_bins(a, Rt[0][1].std(0), j5) for a in Rt[0][1]]); b3 = np.array([slope_bins(a, Rt[2][1].std(0), j5) for a in Rt[2][1]]); L["L05"] = dict(label(s1 - s3, 0.0, float(np.hypot(b1.std(), b3.std())), 0.30), name="slope MID+OUTER, M1 - M3", M1=float(s1), M3=float(s3))
    # gas exponents at fixed x
    xnm = ["x0.2-0.5", "x0.5-1", "x1-2", "x2-5"]; lm = c.Mg / 1e13
    for k, (lo, hi) in enumerate(XB):
        m = xmask(c, lo, hi); e, w, vg = bandsum(c, m); a = fitb(e, w, w, lm); L[f"L{8 + k:02d}"] = dict(label(a["v"], 0.0, a["s"], 0.20), name=f"dDS on Mgas, {xnm[k]}", N=int((w > 0).sum()), C_dDS=a["C"], edge=a["edge"], s_boot=a["s_boot"], s_jack=a["s_jack"])
        b = fitb(e, vg, w, lm); L[f"L{14 + k:02d}"] = dict(label(b["v"], 0.0, b["s"], 0.20), name=f"Q on Mgas, {xnm[k]}", N=int((w > 0).sum()), C_Q=b["C"], edge=b["edge"], s_boot=b["s_boot"], s_jack=b["s_jack"])
    # row 10, L12, L13
    for lk, j, nm in (("L12", OB, "OUTER"), ("L13", MB, "MID")):
        sd, sds = T2jack(c, j, c.n); sl = T2stat(c, j, c.V); sN = T2stat(c, j, c.VN); e, w, _ = bandsum(c, physmask(j)); ae = fitb(e, w, w, lm); L[lk] = dict(label(sd, sl, sds, 0.20), name=f"T2 slope {nm}, data against law on this chain", law=float(sl), newton=float(sN), deficit_exp=ae["v"], deficit_exp_s=ae["s"]); 
    # L18 Q on x
    me = (c.x >= 0.2) & (c.x < 5); wi = c.W * me; Y = (c.e * me).ravel(); VV = (c.VNg * me).ravel(); WW = wi.ravel(); XX = c.x.ravel(); ok = (WW > 0) & (VV > 0)
    def fitp(e, v, w, x, cn=None): 
        F = np.exp(np.outer(GRID, np.log(x))); cc = 1.0 if cn is None else cn; a = (cc * e * v / w) * F; b = (cc * v * v / w) * F * F; nu = a.sum(1); de = b.sum(1); return GRID[int(np.argmax(nu * nu / de))]
    idc = np.repeat(np.arange(N), 8)[ok]; p18 = fitp(Y[ok], VV[ok], WW[ok], XX[ok]); pb = np.array([fitp(Y[ok], VV[ok], WW[ok], XX[ok], counts(r)[idc]) for r in BOOT(500)]); L["L18"] = dict(label(p18, 0.0, float(pb.std()), 0.30), name="Q slope on x, 0.2-5, all clusters")
    # z, BCG partial
    def partial(j, var, sel, lg, nm, prec, lk):
        m = physmask(j); e, w, _ = bandsum(c, m); s_ = sel & (w > 0); a, _, _ = fit1(e[s_], w[s_], w[s_], lm[s_]); ee, ww, xx, yy = e[s_], w[s_], lm[s_], var[s_]
        def two(cn):
            aa = fit1(ee, ww, ww, xx, cn)[0]; v_ = ww * xx ** aa; return fit1(ee, v_, ww, yy, cn)[0]
        p = two(None); Bs = rng0().integers(0, len(ee), (500, len(ee))); bb = np.array([two(np.bincount(r, minlength=len(ee)).astype(float)) for r in Bs]); pz = PATCH[s_]; Jl = []
        for k_ in range(30):
            cn = (pz != k_).astype(float); Jl.append(two(cn))
        Jl = np.array(Jl); sj_ = float(np.sqrt(29 / 30 * ((Jl - Jl.mean()) ** 2).sum())); L[lk] = dict(label(p, 0.0, max(float(bb.std()), sj_), prec), name=nm, gas_exp=float(a), N=int(s_.sum()))
    partial(MB, 1 + zc, np.ones(N, bool), True, "dDS on (1+z), MID, gas removed", 1.0, "L21"); partial(OB, 1 + zc, np.ones(N, bool), True, "dDS on (1+z), OUTER, gas removed", 1.0, "L22")
    P687 = np.load(os.path.join(REPO, "campaign_fresh_gravity", "CFG687_erass1_shear_stack", "cfg687_percluster.npz")); CEN = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG922_cluster_core_baryon_recheck", "cfg922_census_A1.json")))["eRASS1"]; J9 = np.full(N, -1)
    for i in range(N):
        dd = np.hypot((P687["ra"] - X["ra"][i]) * np.cos(np.radians(X["dec"][i])), P687["dec"] - X["dec"][i]) * 3600; j = int(np.argmin(dd))
        if dd[j] < 5 and abs(P687["z"][j] - X["z"][i]) < 1e-3: J9[i] = j
    meas = np.array([j >= 0 and not CEN[j].get("not_measured", False) for j in J9]); bcg = np.array([float(CEN[j]["bcg_med"]) if j >= 0 else np.nan for j in J9]); BC = np.where(meas & (bcg > 0), bcg, np.nan); sb = np.isfinite(BC); R["bcg_n"] = int(sb.sum()); R["bcg_spearman_gas"] = float(spearmanr(BC[sb], c.Mg[sb])[0])
    partial(IB, np.where(sb, BC, 1) / 1e11, sb, True, "dDS on BCG mass, INNER, gas removed", 0.20, "L23"); partial(MB, np.where(sb, BC, 1) / 1e11, sb, True, "dDS on BCG mass, MID, gas removed", 0.20, "L24")
    # scales
    U = dict(L25=("g_N/a0", c.gN), L26=("V_N/W local projected", c.SigN), L27=("r/R500", c.x), L28=("R Mpc", np.broadcast_to(RC, (N, 8))))
    for lk, (nm, u) in U.items():
        lu = np.log10(np.where(u > 0, u, np.nan)); lo = max(np.nanquantile(lu[T3 == t], 0.05) for t in range(3)); hi = min(np.nanquantile(lu[T3 == t], 0.95) for t in range(3)); ed = np.linspace(lo, hi, 6); bi = np.digitize(lu, ed) - 1; bi[np.isnan(lu)] = -1; bi[bi > 4] = -1
        tab = np.full((5, 3), np.nan); er = np.full((5, 3), np.nan); Bs = BOOT(500)
        def Qt(cn):
            O = np.full((5, 3), np.nan)
            for b in range(5):
                ma = bi == b
                for t in range(3):
                    tt = (T3 == t)[:, None] & ma; de = ((c.VN * tt).sum(1) * cn).sum(); O[b, t] = ((c.e * tt).sum(1) * cn).sum() / de if de > 0 and tt.sum() >= 5 else np.nan
            return O
        tab = Qt(np.ones(N)); RR_ = np.array([Qt(counts(r)) for r in Bs]); er = np.nanstd(RR_, axis=0); chi = 0.0; dof = 0; fr = []
        for b in range(5):
            ok_ = np.isfinite(tab[b]) & (er[b] > 0)
            if ok_.sum() < 2: continue
            w_ = 1 / er[b][ok_] ** 2; mu = (w_ * tab[b][ok_]).sum() / w_.sum(); chi += float((w_ * (tab[b][ok_] - mu) ** 2).sum()); dof += int(ok_.sum() - 1); fr.extend((er[b][ok_] / np.abs(mu)).tolist())
        L[lk] = dict(lchi(chi, dof, float(np.median(fr)) if fr else 9), name=f"collapse of Q_b across terciles at fixed {nm}", edges=ed.tolist(), table=tab.tolist(), err=er.tolist())
        if verbose: P(f"  {lk} Q_b at fixed {nm}: edges lg {np.round(ed, 2).tolist()}"); [P("      " + " ".join(f"{tab[b, t]:6.2f}+-{er[b, t]:4.2f}" for t in range(3))) for b in range(5)]
    # L29
    lg = np.log10(c.gN); ed = np.quantile(lg, np.linspace(0, 1, 9)); bi = np.clip(np.digitize(lg, ed) - 1, 0, 7)
    def QB(cn):
        O = []; X_ = []
        for b in range(8):
            ma = bi == b; O.append(((c.e * ma).sum(1) * cn).sum() / ((c.VN * ma).sum(1) * cn).sum()); X_.append(lg[ma].mean())
        return np.array(X_), np.array(O)
    xb, qb = QB(np.ones(N)); Bq = np.array([QB(counts(r))[1] for r in BOOT(500)]); sq = Bq.std(0); okq = qb > 0; yy = np.log10(np.where(okq, qb, np.nan)); sy = sq / (np.abs(qb) * np.log(10)); co = np.polyfit(xb[okq], yy[okq], 2, w=1 / sy[okq]); cb = []
    for a in Bq:
        ok_ = a > 0
        if ok_.sum() >= 4: cb.append(np.polyfit(xb[ok_], np.log10(a[ok_]), 2, w=1 / sy[ok_])[0])
    L["L29"] = dict(label(co[0], 0.0, float(np.std(cb)), 0.30), name="curvature lg Q_b on lg g_N/a0", xb=xb.tolist(), Qb=qb.tolist(), sQ=sq.tolist(), lin=float(np.polyfit(xb[okq], yy[okq], 1, w=1 / sy[okq])[0]))
    if verbose: P("  Q_b by g_N/a0 (lg): " + " ".join(f"{a:.2f}:{b:.2f}" for a, b in zip(xb, qb)))
    # X-COP
    T = xcop_table(foot); XR = {}
    for x, rows in sorted(T.items()): XR[f"{x:g}"] = dict(n=len(rows), lgf=float(np.mean([r["lgf"] for r in rows])), dM=float(np.median([r["dM"] for r in rows])), ratio=float(np.median([r["ratio"] for r in rows])), gN=float(np.median([r["gN"] for r in rows])), ratio_s=float(np.std([r["ratio"] for r in rows], ddof=1) / math.sqrt(len(rows))))
    R["xcop"] = XR; T2_ = xcop_table(foot, -0.12); R["xcop_bracket"] = {f"{x:g}": float(np.median([r["ratio"] for r in rows])) for x, rows in T2_.items()}
    if verbose: P("  X-COP x: " + "; ".join(f"{k}: f {10 ** v['lgf']:.2f}, dM {v['dM']:.2e}, dM/Mgas {v['ratio']:.2f} (HSE-0.12: {R['xcop_bracket'][k]:.2f}), g_N/a0 {v['gN']:.3f}" for k, v in XR.items()))
    cls = [c_["name"] for c_ in XC]; Sl = {}
    for c_ in XC:
        rw = c_["rows"]; a0 = A0[foot] * AX; xs = sorted(rw); r_ = np.array([rw[x][0] for x in xs]); dm = np.array([rw[x][1] - law_mass(rw[x][2] + rw[x][3], rw[x][0], a0) for x in xs]); mg = np.array([rw[x][2] for x in xs]); lx = np.log(xs)
        Sl[c_["name"]] = dict(a=np.polyfit(lx[:3], np.log(dm[:3]), 1)[0], b=np.polyfit(lx[2:], np.log(dm[2:]), 1)[0], r=np.polyfit(lx, np.log(dm / mg), 1)[0], mg=float(np.interp(math.log(0.5), lx, np.log10(mg))), rm=float(np.mean(np.log10((dm / mg)[[i for i, x in enumerate(xs) if 0.3 <= x <= 0.7]]))))
    A = np.array([Sl[k]["a"] for k in cls]); Bb = np.array([Sl[k]["b"] for k in cls]); Rr = np.array([Sl[k]["r"] for k in cls]); Mm = np.array([Sl[k]["mg"] for k in cls]); RM = np.array([Sl[k]["rm"] for k in cls]); bi7 = np.random.default_rng(SEED).integers(0, 7, (NB, 7)); m_ = (A + Bb) / 2; L["L06"] = dict(label(A.mean(), m_.mean(), float((A - m_)[bi7].mean(1).std()), 0.30, True), name="X-COP slope dM, x 0.1-0.3, against mean"); L["L07"] = dict(label(Bb.mean(), m_.mean(), float((Bb - m_)[bi7].mean(1).std()), 0.30, True), name="X-COP slope dM, x 0.3-1, against mean"); L["L19"] = dict(label(Rr.mean(), 0.0, float(Rr[bi7].mean(1).std()), 0.30, True), name="X-COP dM/Mgas slope on x")
    sl20 = np.polyfit(Mm, RM, 1)[0]; bs = []
    for r in bi7:
        if np.ptp(Mm[r]) > 0: bs.append(np.polyfit(Mm[r], RM[r], 1)[0])
    L["L20"] = dict(label(sl20, 0.0, float(np.std(bs)), 0.20, True), name="X-COP dM/Mgas x 0.3-0.7 on Mgas", span_dex=float(np.ptp(Mm)))
    # groups
    Gr = d["groups_" + foot]; dg = Gr[:, 0] - Gr[:, 1]; lgg = np.log10(Gr[:, 5]); dMoverL = 10 ** (2 * dg) - 1; dMoverB = dMoverL * Gr[:, 6] / Gr[:, 7]; R["groups"] = dict(n=len(dg), d_mean=float(dg.mean()), d_median=float(np.median(dg)), gN_range=[float(lgg.min()), float(np.median(lgg)), float(lgg.max())], dMoverL_med=float(np.median(dMoverL)), dMoverB_med=float(np.median(dMoverB)), lgMb_median=float(np.median(Gr[:, 3])), Re_med=float(np.median(Gr[:, 4])))
    rg = np.random.default_rng(SEED).integers(0, len(dg), (NB, len(dg))); sl31 = np.polyfit(lgg, dg, 1)[0]; bb = [np.polyfit(lgg[r], dg[r], 1)[0] for r in rg]; L["L31"] = dict(label(sl31, 0.0, float(np.std(bb)), 0.20), name="groups d on lg g_N/a0")
    xcg = np.array([[r["lgf"], math.log10(r["gN"])] for x, rows in T.items() for r in rows]); ov = (xcg[:, 1] >= lgg.min()) & (xcg[:, 1] <= lgg.max()); gg = (lgg >= xcg[:, 1].min()) & (lgg <= xcg[:, 1].max())
    if ov.sum() >= 5 and gg.sum() >= 5:
        diff = xcg[ov, 0].mean() - (2 * dg[gg]).mean(); ss = math.hypot(xcg[ov, 0].std(ddof=1) / math.sqrt(max(ov.sum() / 5, 2)), 2 * dg[gg].std(ddof=1) / math.sqrt(gg.sum())); L["L30"] = dict(label(diff, 0.0, ss, 0.10), name="X-COP against groups, lg(M_obs/M_law), same g_N", n_xcop=int(ov.sum()), n_groups=int(gg.sum()), xcop=float(xcg[ov, 0].mean()), groups=float((2 * dg[gg]).mean()), range_lg=[float(max(lgg.min(), xcg[:, 1].min())), float(min(lgg.max(), xcg[:, 1].max()))])
    else: L["L30"] = dict(label="NOT COMPUTABLE", name="X-COP against groups: no g_N overlap", n_xcop=int(ov.sum()), n_groups=int(gg.sum()), val=float("nan"), t=float("nan"), s=float("nan"), null=0.0)
    # lensing stack vs groups in g_N, reported, no label
    lgc = np.log10(c.gN); rows = []
    for lo, hi in zip(np.arange(-3.4, -1.0, 0.4), np.arange(-3.0, -0.6, 0.4)):
        ma = (lgc >= lo) & (lgc < hi); g_ = (lgg >= lo) & (lgg < hi)
        if ma.sum() >= 10 and (c.V * ma).sum() > 0: 
            nu_ = (c.n * ma).sum(1); de_ = (c.V * ma).sum(1); br_ = BOOT(500); lb_ = np.array([np.log10(max((nu_[r_]).sum() / de_[r_].sum(), 1e-3)) for r_ in br_]); rows.append(dict(lo=float(lo), hi=float(hi), lens=float(np.log10(nu_.sum() / de_.sum())) if nu_.sum() > 0 else float("nan"), lens_s=float(lb_.std()), groups=float((2 * dg[g_]).mean()) if g_.sum() >= 3 else None, groups_s=float(2 * dg[g_].std(ddof=1) / math.sqrt(g_.sum())) if g_.sum() >= 3 else None, ng=int(g_.sum())))
    if verbose: P("  reported, post-hoc, no label, lg(obs/law) by lg g_N/a0, lensing stack (Delta Sigma ratio) against groups (2d): " + "; ".join(f"[{o_['lo']:.1f},{o_['hi']:.1f}] lens {o_['lens']:+.2f}+-{o_['lens_s']:.2f}" + (f", groups {o_['groups']:+.2f}+-{o_['groups_s']:.2f} (n {o_['ng']})" if o_['groups'] is not None else "") for o_ in rows)); P(f"  groups: {R['groups']}")
    R["lens_vs_groups"] = rows
    R["looks"] = L; return R, c
def L_print(L):
    for k in sorted(L):
        o = L[k]
        if "chi2" in o: P(f"  {k} {o['name']}: chi2 {o['chi2']:.1f}/{o['dof']}, p {o['p']:.2e}, frac err {o['frac']:.2f} -> {o['label']}")
        else: P(f"  {k} {o['name']}: {o.get('val', float('nan')):+.2f} (null {o.get('null', 0):+.2f}) +- {o.get('s', float('nan')):.2f}, t {o.get('t', float('nan')):+.2f} -> {o['label']}" + "".join(f"; {x} {o[x]:.3g}" for x in ("law", "newton", "deficit_exp", "deficit_exp_s", "M1", "M3", "gas_exp", "xcop", "groups", "span_dex", "C_dDS", "C_Q", "lin") if x in o) + (f"; N {o['N']}" if "N" in o else "") + (f"; edge {o['edge']}" if o.get("edge") else ""))
# --------------------------------------------------------- checks
P(f"LM1 map{' MUTATE a0 x 1.5' if MUT else ''}; kappa = 1/2 FITTED; not theory closed; no rule, no mechanism; footings never pooled; look-elsewhere 62 tests, |t| >= {ZLE}")
if not MUT:
    DRo = {f: json.load(open(os.path.join(RB, "LW1_law_scorecard", f"lw1_keys_g005_f{fs}.json"))) for f, fs in (("034", "034"), ("0615", "0615"))}; dmx = 0; dpx = 0; dsum = 0; dn = 0
    for f, job in (("034", "BASE_f034"), ("0615", "BASE_f0615")):
        J = KJ(job); D_ = DP(job)
        for ft in FEET:
            k = f"R1|c0|{ft}"
            for h in ("h0672", "h0686"):
                dmx = max(dmx, max(abs(J[k]["Z"][h][q] - DRo[f][k]["Z"][h][q]) for q in J[k]["Z"][h])); dpx = max(dpx, max(abs(J[k]["preds"][h][q] - DRo[f][k]["preds"][h][q]) for q in J[k]["preds"][h]))
                V = D_[f"V_{ft}_{h}"]; vC = D_[f"vC_{ft}_{h}"]; n = nsum(h)[0]
                for t in range(3):
                    s = T3 == t; dsum = max(dsum, abs(V[s][:, OB].sum() / vC[s][:, OB].sum() - J[k]["preds"][h][f"G-OUT-M{t + 1}"])); dn = max(dn, abs(n[s][:, OB].sum() / vC[s][:, OB].sum() - J[k]["tmpl"][h][f"G-OUT-M{t + 1}"][0]))
                dsum = max(dsum, abs(V[:, OB].sum() / vC[:, OB].sum() - J[k]["preds"][h]["G-OUT-Mall"]), abs(V[:, IB].sum() / vC[:, IB].sum() - J[k]["preds"][h]["G-IN-Mall"])); dn = max(dn, abs(n[:, OB].sum() / vC[:, OB].sum() - J[k]["tmpl"][h]["G-OUT-Mall"][0]))
                for t in range(3):
                    I_ = II[TID == t]; dsum = max(dsum, abs(V[I_][:, OB].sum() / vC[I_][:, OB].sum() - J[k]["preds"][h][f"G-OUT-T{t + 1}"]))
    check("K1", dmx <= 1e-6 and dpx <= 1e-6, f"same-process keys against LW1's JSON, both f*, both h, both footings: |d Z| {dmx:.1e}, |d pred| {dpx:.1e}; canonical f* 0.034 h 0.672 G-OUT-M3 {KJ('BASE_f034')['R1|c0|canonical']['Z']['h0672']['G-OUT-M3']:+.3f}")
    check("K1b", dsum <= 1e-6, f"dump sums reproduce preds, M1-M3, Mall, IN-Mall, OUT-T1-3: {dsum:.1e}"); check("K2", dn <= 1e-6, f"n sums reproduce grader's meas: {dn:.1e}")
    p = np.load(os.path.join(REPO, "campaign_fresh_gravity", "CFG687_erass1_shear_stack", "cfg687_percluster.npz")); W7 = np.where(p["E"] > 0, 1 / p["E"] ** 2, 0); mg = p["mg"]; q = np.quantile(mg, [1 / 3, 2 / 3]); td = np.clip(np.digitize(mg, q), 0, 2); o_ = np.argsort(p["ra"]); pa = np.empty(len(mg), int); pa[o_] = np.arange(len(mg)) * 30 // len(mg); jj = [6, 7]
    def s7(sel, A):
        xs, ys = [], []
        for t in range(3):
            s = sel & (td == t); xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10((W7[s][:, jj] * A[s][:, jj]).sum() / W7[s][:, jj].sum()))
        return np.polyfit(xs, ys, 1)[0]
    al = np.ones(len(mg), bool); so = s7(al, p["D"]); Js = np.array([s7(pa != k, p["D"]) for k in range(30)]); se = float(np.sqrt(29 / 30 * ((Js - Js.mean()) ** 2).sum())); sl = s7(al, p["PL"]); check("K3", abs(so - 0.90) <= 0.005 and abs(se - 0.21) <= 0.005 and abs(sl - 0.47) <= 0.005, f"CFG687 T2: {so:.3f} +- {se:.3f}, law {sl:.3f}; PN {s7(al, p['PN']):.3f}")
    LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_xcop.json"))); dx = 0
    for ft in FEET:
        T = xcop_table(ft); v = np.array([r["lgf"] for x, rows in T.items() if x <= 0.75 for r in rows]); dx = max(dx, abs(v.mean() - LW[ft]["fits"]["mean"]), abs(np.sqrt((v ** 2).mean()) - LW[ft]["fits"]["rms"]))
    check("K4", dx <= 1e-4, f"X-COP builder against LW1's FITS row: {dx:.1e}; rows at x=1: {len(xcop_table('canonical').get(1.0, []))}")
    # K5
    d0 = DP("BASE_f034"); c0 = Cell(d0, "canonical", "h0672", 0.034); e, w, _ = bandsum(c0, physmask(OB)); rs = np.random.default_rng(5); perm = rs.permutation(N); noise = (e - w * (e.sum() / w.sum()))[perm]; lm = c0.Mg / 1e13; a7 = fitb(w * 5 * lm ** 0.7 + noise, w, w, lm, nb=500); a0_ = fitb(w * 5.0 + noise, w, w, lm, nb=500); l0 = label(a0_["v"], 0, a0_["s"], 0.20)["label"]; check("K5", abs(a7["v"] - 0.7) <= 2 * a7["s"] and "TREND" not in l0, f"synthetic p 0.7 recovered {a7['v']:.2f} +- {a7['s']:.2f}; p 0 reads {a0_['v']:.2f} +- {a0_['s']:.2f}, {l0}")
    # K6
    M3Ad = np.load(os.path.join(RB, "M3A1_outer_key_audit", "cache_jobs", "BASE_0.034_dump.npz")); h = "h0672"; V6 = M3Ad[f"V_{h}"]; vC6 = M3Ad[f"vC_{h}"]; base = json.load(open(os.path.join(RB, "M3A1_outer_key_audit", "cache_jobs", "BASE_0.034.json")))["cells"][h]["G-OUT-M3"]; M3s = T3 == 2
    def Z6(n, scale=False): A = n[M3s][:, OB].sum() / vC6[M3s][:, OB].sum(); Pd = V6[M3s][:, OB].sum() / vC6[M3s][:, OB].sum(); return (A - Pd) / (base["s"] * (A / base["meas"] if scale else 1))
    i = HI[h]; Bm3 = X["den"][M3s, i].sum(0) / X["den_r"][M3s, i].sum(0); z4a = Z6(nsum(h, B=Bm3[None, :])[0], True); z4d = Z6(nsum(h, D=X["Draw"][:, i] - RRd["Rt"][:, HX[h]])[0]); z4e = Z6(nsum(h, leak=X["leakT"][:, HX[h], 0])[0]); check("K6", abs(z4a - 4.36) <= 0.01 and abs(z4d - 3.96) <= 0.01 and abs(z4e - 3.73) <= 0.01, f"M3A1's rows on its own V: C4a {z4a:+.3f} (+4.36), C4d {z4d:+.3f} (+3.96), C4e {z4e:+.3f} (+3.73)")
    gz = 0
    for ft in FEET:
        Gr = d0["groups_" + ft]; gz = max(gz, abs((Gr[:, 0] - Gr[:, 1]).mean() - KJ("BASE_f034")[f"R1|c0|{ft}"]["groups"]["mean"]))
    check("K7", gz <= 1e-6, f"groups mean d against the grader's row: {gz:.1e}")
    if not all(c_[1] for c_ in CHK): P("A CHECK FAILED: no reading.")
# --------------------------------------------------------- run
for ft in FEET:
    R_, c_ = run_foot(ft); RES[ft] = R_; P(f"\n  Looks, {ft}, f* 0.034, h 0.672"); L_print(R_["looks"])
    if not MUT:
        R2, _ = run_foot(ft, "h0686", verbose=False); R3, _ = run_foot(ft, "h0672", "BASE_f0615", 0.0615, verbose=False); RES[ft + "_h0686"] = R2; RES[ft + "_f0615"] = R3; ch = {k: (R_["looks"][k]["label"], R2["looks"][k]["label"], R3["looks"][k]["label"]) for k in R_["looks"] if not (R_["looks"][k]["label"] == R2["looks"][k]["label"] == R3["looks"][k]["label"])}; P(f"  Labels that differ with h 0.686 or f* 0.0615 ({ft}): {ch or 'none'}")
        P("  Key exponents across cells (0.672/0.034, 0.686/0.034, 0.672/0.0615): " + "; ".join(f"{k} {R_['looks'][k]['val']:+.2f} {R2['looks'][k]['val']:+.2f} {R3['looks'][k]['val']:+.2f}" for k in ("L08", "L09", "L10", "L11", "L12", "L14", "L15", "L16", "L17")))
if MUT:
    B0 = json.load(open(os.path.join(HERE, "lm1_results.json"))); mv = []
    for ft in FEET: mv += [max(abs(np.array(RES[ft]["dDS_all"]) - np.array(B0[ft]["dDS_all"]))[j] for j in b) for b in BAND.values()]; mv.append(abs(RES[ft]["xcop"]["0.3"]["lgf"] - B0[ft]["xcop"]["0.3"]["lgf"]))
    check("MUTATE", min(mv) > 0, f"every band and X-COP moves, min move {min(mv):.3f}; dDS all canonical " + " ".join(f"{a:.1f}" for a in RES['canonical']['dDS_all']) + " (flips aren't results)")
else:
    # --------------------------------------------------------- systematics
    SY = {}
    def Fzv(h): return np.interp(zc, GRZ, FH)
    for ft in FEET:
        h = "h0672"; q = f"{ft}_{h}"; d0 = DP("BASE_f034"); i = HI[h]; V0 = d0["V_" + q]; dV1 = DP("C1aM3_f034")["V_" + q] - V0; dV1c = DP("C1acapall_f034")["V_" + q] - V0; dV2 = DP("C2a_f034")["V_" + q] - V0; Dx = X["Draw"][:, i] - RRd["Rt"][:, HX[h]]; Bt = Btercile(h); Lk = X["leakT"][:, HX[h], 0]; Fz = Fzv(h); FA = json.load(open(os.path.join(RB, "M3A1_outer_key_audit", "m3a1_factor_C1a_M3.json"))); F2 = json.load(open(os.path.join(RB, "M3A1_outer_key_audit", "m3a1_factor_C2a.json"))); FC = json.load(open(os.path.join(HERE, "lm1_factor_C1a_capall.json"))); ma = np.array([FA[n] for n in names]); m2 = np.array([F2[n] for n in names]); mc = np.array([FC[n] for n in names])
        ROWS = dict(base=dict(), C1a_M3=dict(Vadd=dV1, mfac=ma), C1a_capall=dict(Vadd=dV1c, mfac=mc), C2a=dict(Vadd=dV2, mfac=m2), C4a=dict(B=Bt), C4c=dict(Fz=Fz), C4d=dict(D=Dx), C4e=dict(leak=Lk), net=dict(D=Dx, B=Bt, leak=Lk, Fz=Fz, Vadd=dV1 + dV2, mfac=ma * m2), net_noC4c=dict(D=Dx, B=Bt, leak=Lk, Vadd=dV1 + dV2, mfac=ma * m2), lowering=dict(D=Dx, B=Bt, leak=Lk, Vadd=dV2, mfac=m2), capall_all=dict(D=Dx, B=Bt, leak=Lk, Fz=Fz, Vadd=dV1c + dV2, mfac=mc * m2))
        Tb = {}
        for rn, kw in ROWS.items():
            c = Cell(d0, ft, h, 0.034, **kw); o = {}; lm = c.Mg / 1e13
            for bn, j in BAND.items():
                for t in range(3): s = T3 == t; o[f"{bn}_M{t + 1}"] = float(c.e[s][:, j].sum() / c.W[s][:, j].sum()); o[f"Q{bn}_M{t + 1}"] = float(c.e[s][:, j].sum() / c.VNg[s][:, j].sum())
            o["s_OUT"] = float(T2stat(c, OB, c.n)); o["law_OUT"] = float(T2stat(c, OB, c.V))
            for k, (lo, hi) in enumerate(XB):
                m_ = xmask(c, lo, hi); e, w, vg = bandsum(c, m_); o[f"s_x{k}"] = float(fit1(e, w, w, lm)[0]); o[f"r_x{k}"] = float(fit1(e, vg, w, lm)[0])
            Tb[rn] = o
        LB = {}
        for rn in ("base", "net", "lowering", "net_noC4c"):
            c = Cell(d0, ft, h, 0.034, **ROWS[rn]); lm = c.Mg / 1e13; o = {}
            for k, (lo, hi) in enumerate(XB):
                m_ = xmask(c, lo, hi); e, w, vg = bandsum(c, m_); a = fitb(e, w, w, lm, nb=500); b = fitb(e, vg, w, lm, nb=500); o[f"L{8 + k:02d}"] = label(a["v"], 0.0, a["s"], 0.20); o[f"L{14 + k:02d}"] = label(b["v"], 0.0, b["s"], 0.20)
            sd, sds = T2jack(c, OB, c.n); o["L12"] = label(sd, T2stat(c, OB, c.V), sds, 0.20); sm, sms = T2jack(c, MB, c.n); o["L13"] = label(sm, T2stat(c, MB, c.V), sms, 0.20); LB[rn] = o
        SY[ft] = dict(rows=Tb, labels=LB); P(f"\nSystematics by M3A1 row, {ft}, f* 0.034, h 0.672; C4c uses F(h 0.672), printed in m3a1.out; h 0.686 not printed. C4d and C4e overlap, per M3A1")
        hd = ["INNER_M1", "INNER_M2", "INNER_M3", "MID_M1", "MID_M2", "MID_M3", "OUTER_M1", "OUTER_M2", "OUTER_M3", "s_OUT", "law_OUT", "s_x1", "s_x2", "s_x3", "r_x1", "r_x2", "r_x3"]; P("  row        " + " ".join(f"{a[:9]:>9s}" for a in hd))
        for rn, o in Tb.items(): P(f"  {rn:10s} " + " ".join(f"{o[a]:9.2f}" for a in hd))
        b = Tb["base"]; lo_ = Tb["lowering"]; ne = Tb["net"]; P("  survival, fraction of baseline dDS left, lowering only / net: " + "; ".join(f"{a} {lo_[a] / b[a]:.2f}/{ne[a] / b[a]:.2f}" for a in hd[:9])); SY[ft]["survival"] = {a: dict(lowering=lo_[a] / b[a], net=ne[a] / b[a]) for a in hd[:9]}
        c9 = Cell(d0, ft, h, 0.034); Ma = T3 == 2; conv = c9.vC[Ma][:, OB].sum() / c9.W[Ma][:, OB].sum(); ZT = json.load(open(os.path.join(RB, "M3A1_outer_key_audit", "m3a1_results.json")))["Ztot"]["0.034|h0672"]; sysA = math.sqrt(sum(ZT[k_] ** 2 for k_ in ("gas", "slope", "m", "nz", "leak"))); _, rb_ = stack(c9, Ma); ob_ = np.array([(c9.e[r_][:, OB].sum() / c9.W[r_][:, OB].sum()) for r_ in np.where(Ma)[0][rng0().integers(0, Ma.sum(), (2000, Ma.sum()))]]); P(f"  OUTER M3 dDS {b['OUTER_M3']:.1f} +- {ob_.std():.1f} stat +- {sysA * conv:.1f} sys, M3A1's gas, slope, m, n(z), leak in quadrature, no seed term, canonical terms carried to alt; 1 A unit = {conv:.1f} M_sun/pc^2"); SY[ft]["OUTER_M3"] = dict(v=b["OUTER_M3"], stat=float(ob_.std()), sys=float(sysA * conv), conv=float(conv))
        for rn in ("net", "net_noC4c", "lowering"): P(f"  labels changed under {rn}: " + (", ".join(f"{k} {LB['base'][k]['label']} > {LB[rn][k]['label']}" for k in LB["base"] if LB["base"][k]["label"] != LB[rn][k]["label"]) or "none"))
        P("  base labels here (B=500): " + ", ".join(f"{k} {LB['base'][k]['val']:+.2f} {LB['base'][k]['label']}" for k in sorted(LB["base"])))
    RES["systematics"] = SY
RES["checks"] = {a: b for a, b in CHK}
json.dump(RES, open(os.path.join(HERE, f"lm1_results{TAG}.json"), "w"), indent=0, default=float); open(os.path.join(HERE, f"lm1{TAG}.out"), "w").write("\n".join(OUT) + "\n"); P(f"\nchecks {sum(b for a, b in CHK)}/{len(CHK)}")
