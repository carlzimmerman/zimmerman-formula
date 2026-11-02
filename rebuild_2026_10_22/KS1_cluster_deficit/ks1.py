#!/usr/bin/env python3
"""KS1 (FROZEN_CRITERIA.md): k(x, M) per set and method; separation; error and bits; f_b reading, a description. python3 ks1.py [--mutate]. Nothing reinstated. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from astropy.io import fits
from scipy.optimize import brentq
from scipy.stats import chi2 as CH2, norm
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); DATA = os.path.join(REPO, "real_research", "data")
for d in ("CU1_gas_term_replication", "FR3_retention_independent"): sys.path.insert(0, os.path.join(RB, d))
import cu1_core as C, fr3_parse as FP
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; AX = 1.5 if MUT else 1.0; NB = 2000; SEED = 20261102
OUT = []; R = {}; CHK = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(n, ok, t): CHK.append((n, bool(ok))); P(f"{n} {'PASS' if ok else 'FAIL'}: {t}")
FEET = ("canonical", "alt"); HH = ("h0672", "h0686"); A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); HV = dict(h0672=.672, h0686=.686); HI = dict(h0672=1, h0686=2); HX = dict(h0672=0, h0686=1); FS = .034
G, MS, PCm = 6.674e-11, 1.989e30, 3.0857e16; RN = (.2976016 - .0223081 / .6856427 ** 2) / (.0223081 / .6856427 ** 2); FB = dict(native=1 / (1 + RN), bk1=.15747293971651993)
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); names = [str(n).strip() for n in X["name"]]; N = len(names); Mg0 = np.asarray(X["Mgas500"], float); zc = np.asarray(X["z"], float); RA = np.asarray(X["ra"], float); DEC = np.asarray(X["dec"], float); Mc0 = np.asarray(X["M500"], float)
LM = os.path.join(RB, "LM1_law_missing_mass_map"); B = np.load(os.path.join(HERE, "cache_basis", "basis.npz")); NODES = B["NODES"]; ND5 = NODES[:5]
def dump(fs=FS): return np.load(os.path.join(LM, "cache_MUTATE_f034" if MUT else (f"cache_BASE_f034" if fs == FS else "cache_BASE_f0615"), "dump.npz"))
D34 = dump(); RC = D34["RC"]; T3 = D34["T3M"]; PATCH = D34["PATCH"]; UX = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_okabe.json"))); I35 = np.array([names.index(n) for n in UX])
def nsum(h):
    i = HI[h]; W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B0 = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); return W * B0[None, :] * (X["D"][:, i] - X["leakP"][:, HX[h], 0]), W
def law_mass(Mb, r_kpc, a0):
    rs = r_kpc * 1e3 * PCm; gb = G * Mb * MS / rs ** 2; return (.5 * gb + np.sqrt(.25 * gb ** 2 + a0 * gb)) * rs ** 2 / G / MS
class Cell:
    def __init__(s, foot, h, fs=FS):
        d = dump(fs); q = f"{foot}_{h}"; s.foot, s.h, s.fs = foot, h, fs; s.n, s.W = nsum(h); s.V = d["V_" + q]; s.VN = d["VN_" + q]; s.e = s.n - s.V; s.R5 = d["R500_" + h]; s.x = RC[None, :] / s.R5[:, None]; s.Mb = d["Mb_" + q]; s.ML = d["ML_" + q]; s.G6 = B["G_" + h]; s.T6 = B[f"T_{foot}_{h}"]
        s.mask = (s.W > 0) & (s.x >= .2) & (s.x < 5)
def five(A): return np.concatenate([A[:, :4], A[:, 4:6].sum(1, keepdims=True)], 1)
def normal(Vb, y, W, mask):
    """per-cluster A_i (J x J) and b_i, chi^2 = sum (y - k V)^2 / W"""
    w = np.where(mask, 1 / np.where(W > 0, W, 1), 0); Ai = np.einsum("ijb,ilb,ib->ijl", Vb, Vb, w); bi = np.einsum("ijb,ib,ib->ij", Vb, y, w); return Ai, bi
def wls(Ai, bi, c=None):
    if c is None: return np.linalg.solve(Ai.sum(0), bi.sum(0))
    return np.linalg.solve(np.einsum("ri,ijl->rjl", c, Ai), np.einsum("ri,ij->rj", c, bi)[..., None])[..., 0]
def boot_w(n, nb=NB, seed=SEED): 
    idx = np.random.default_rng(seed).integers(0, n, (nb, n)); c = np.zeros((nb, n)); np.add.at(c, (np.arange(nb)[:, None], idx), 1); return c
def fitnodes(c, Vb, y, sel=None, jack=True):
    sel = np.arange(N) if sel is None else sel; Ai, bi = normal(Vb[sel], y[sel], c.W[sel], c.mask[sel]); k = wls(Ai, bi); bb = wls(Ai, bi, boot_w(len(sel))); cov = np.atleast_2d(np.cov(bb.T)); sb = np.sqrt(np.diag(cov)); sj = sb.copy()
    if jack:
        J = np.array([wls(Ai[PATCH[sel] != q], bi[PATCH[sel] != q]) for q in np.unique(PATCH[sel])]); sj = np.sqrt((len(J) - 1) / len(J) * ((J - J.mean(0)) ** 2).sum(0))
    s = np.maximum(sb, sj); cr = np.atleast_2d(np.corrcoef(bb.T)); return dict(k=k, s=s, sb=sb, sj=sj, cov=cr * np.outer(s, s), bb=bb)
def fmt(a, n=2): return "[" + ", ".join(f"{v:.{n}f}" for v in np.atleast_1d(a)) + "]"
# ------------------ KiDS
P(f"KS1{TAG}. KiDS forward k3(x), nodes {ND5.tolist()}, flat outside; gas +0.005. Sigma = max(bootstrap, jackknife). e = n - V")
KID = {}
for foot in FEET:
    for h in HH:
        for fs in ((FS, .0615) if not MUT else (FS,)):
            if fs != FS and h != "h0672": continue
            c = Cell(foot, h, fs); key = f"{foot}|{h}|{fs}"; G5 = five(c.G6); r = fitnodes(c, G5, c.e); KID[key] = dict(all=r); P(f"[{key}] k3 {fmt(r['k'])} +- {fmt(r['s'])}; boot {fmt(r['sb'])}, jack {fmt(r['sj'])}")
            if fs == FS:
                for t in range(3):
                    q = fitnodes(c, G5, c.e, np.where(T3 == t)[0]); KID[key][f"T{t}"] = q; P(f"   gas tercile {t + 1}, lg Mg {np.log10(Mg0[T3 == t]).mean():.2f}: k3 {fmt(q['k'])} +- {fmt(q['s'])}")
                q = fitnodes(c, G5, c.e, I35, jack=False); KID[key]["I35"] = q; P(f"   the 35: k3 {fmt(q['k'])} +- {fmt(q['s'])}")
                q6 = fitnodes(c, c.G6, c.e, jack=False); KID[key]["six"] = q6; P(f"   sensitivity, node 3.5 added: k3 {fmt(q6['k'])} +- {fmt(q6['s'])}")
                t5 = c.G6[:, :5].copy(); q0 = fitnodes(c, t5, c.e, jack=False); KID[key]["taper"] = q0; P(f"   sensitivity, k tapers to 0 at x 3.5 (hat, not a step at 1.7): k3 {fmt(q0['k'])} +- {fmt(q0['s'])}")
                y = fitnodes(c, G5, c.n); KID[key]["Mtot_Mg"] = y; P(f"   M_tot/M_gas nodes, forward, no law: {fmt(y['k'])} +- {fmt(y['s'])}")
                for t in range(3): q = fitnodes(c, G5, c.n, np.where(T3 == t)[0], jack=False); KID[key][f"MT{t}"] = q
            if foot == "canonical" and h == "h0672" and fs == FS: PR = c
K_P = {f: KID[f"{f}|h0672|{FS}"] for f in FEET}
P("Correlation of nodes, canonical h 0.672: " + json.dumps(np.round(np.corrcoef(K_P["canonical"]["all"]["bb"].T), 2).tolist()))
# term form
P("\nThe multiplier form M = M_law (1 + k_term g_gas/a0): KiDS forward. One number, then by node. Key windows (CU1): OUT-all <= 7.2, M3 >= 8.8, MID-T3 >= 12.9")
KT = {}
for foot in FEET:
    c = Cell(foot, "h0672"); T1 = B[f"Tall_{foot}_h0672"][:, None, :]; r = fitnodes(c, T1, c.e); rn = fitnodes(c, five(c.T6), c.e); KT[foot] = dict(one=r, node=rn); P(f"[{foot}] one k_term {r['k'][0]:.2f} +- {r['s'][0]:.2f}; nodes {fmt(rn['k'])} +- {fmt(rn['s'])}")
    for t in range(3): q = fitnodes(c, T1, c.e, np.where(T3 == t)[0]); KT[foot][f"T{t}"] = q; P(f"   gas tercile {t + 1}: {q['k'][0]:.2f} +- {q['s'][0]:.2f}")
    q = fitnodes(c, T1, c.e, I35, jack=False); KT[foot]["I35"] = q; P(f"   the 35: {q['k'][0]:.2f} +- {q['s'][0]:.2f}")
# ------------------ X-COP
def li(r, m, t):
    g = (r > 0) & (m > 0); return float(np.exp(np.interp(np.log(t), np.log(r[g]), np.log(m[g]), left=np.nan, right=np.nan)))
XG = (.1, .2, .3, .5, .6, .7, 1., 1.2, 1.5)
def xload():
    O = []
    for n in sorted(os.listdir(os.path.join(DATA, "xcop"))):
        p = os.path.join(DATA, "xcop", n)
        if not os.path.isdir(p): continue
        with fits.open(os.path.join(p, f"{n}_hydro_mass.fits")) as q: hm = q[1].data.copy(); r5 = q[1].header["R500"]
        with fits.open(os.path.join(p, f"{n}_fgas_profile.fits")) as q: ga = q[1].data.copy(); rg = q[1].header["R500"]
        st = None
        if os.path.exists(os.path.join(p, f"{n}_mstar.fits")):
            with fits.open(os.path.join(p, f"{n}_mstar.fits")) as q: st = q[2].data.copy()
        rows = {}
        for x in XG:
            r = x * r5; mh = li(hm["RADIUS"], hm["M_FORW"], r); em = float(np.interp(r, hm["RADIUS"], hm["EM_FORW"])); mg = li(ga["RADIUS"] * rg, ga["MGAS"], r); ms = li(st["RADIUS"], st["MSTAR"], r) if st is not None else mg * FS
            if np.all(np.isfinite([mh, mg, ms])): rows[x] = (r, mh, mg, ms, em)
        O.append(dict(name=n, stars=st is not None, rows=rows, r5=r5))
    return O
XC = xload(); X7 = [c for c in XC if c["stars"]]; X12 = XC
def xk(cs, foot, x, shift=0., f=1., term=False):
    o = []; a0 = A0[foot] * AX
    for c in cs:
        if x not in c["rows"]: o.append(np.nan); continue
        r, mh, mg, ms, em = c["rows"][x]; mbb = mg * f ** 2.5 + ms * f ** 2; ml = law_mass(mbb, r * f, a0); mt = mh * f * 10 ** shift
        if term: o.append((mt / ml - 1) / (G * mg * f ** 2.5 * MS / (r * f * 1e3 * PCm) ** 2 / a0))
        else: o.append((mt - ml) / (mg * f ** 2.5))
    return np.array(o)
def xY(cs, x, f=1.):
    o = []
    for c in cs:
        if x not in c["rows"]: o.append(np.nan); continue
        r, mh, mg, ms, em = c["rows"][x]; o.append(mh * f / (mg * f ** 2.5 + ms * f ** 2))
    return np.array(o)
def xboot(fn, cs, x, nb=NB, seed=SEED):
    v = fn(x); rg = np.random.default_rng(seed); e = np.array([c["rows"][x][4] / c["rows"][x][1] if x in c["rows"] else 0 for c in cs]); idx = rg.integers(0, len(cs), (nb, len(cs))); return v, idx, e
P("\nX-COP HSE, 3D, as stored (h 0.70). Means; sigma = cluster bootstrap + own EM_FORW drawn per cluster (coherent in x). s_int = rms between clusters")
XK = {}
for foot in FEET:
    XK[foot] = {}
    for lab, cs in (("7", X7), ("12", X12)):
        rg = np.random.default_rng(SEED); dr = rg.normal(0, 1, (NB, len(cs))); idx = rg.integers(0, len(cs), (NB, len(cs))); XS = {}
        for x in XG:
            n_ = sum(x in c["rows"] for c in cs)
            if n_ < 5: continue
            k = xk(cs, foot, x); ok = np.isfinite(k); mlmg = np.array([law_mass(c["rows"][x][2] + c["rows"][x][3], c["rows"][x][0], A0[foot] * AX) / c["rows"][x][2] if x in c["rows"] else np.nan for c in cs]); em = np.array([c["rows"][x][4] / c["rows"][x][2] if x in c["rows"] else 0 for c in cs]); bb = np.nanmean(np.take_along_axis(k + dr * em, idx, 1), 1); br = xk(cs, foot, x, -.12); XS[x] = dict(k=float(np.nanmean(k)), med=float(np.nanmedian(k)), s=float(np.nanstd(bb)), n=n_, sint=float(np.nanstd(k)), bb=bb, bracket=float(np.nanmean(br)), f=float(np.nanmean(xk(cs, foot, x, 0., .7 / .672))), L=float(np.nanmean(mlmg)), kt=float(np.nanmean(xk(cs, foot, x, term=True))), kts=float(np.nanstd(xk(cs, foot, x, term=True))))
            P(f"[{foot} N{lab}] x {x}: k3 {XS[x]['k']:.2f} +- {XS[x]['s']:.2f} (N {n_}, between-cluster rms {XS[x]['sint']:.2f}, median {XS[x]['med']:.2f}); HSE-0.12 {XS[x]['bracket']:.2f}; h 0.672 rescaled {XS[x]['f']:.2f}; law/gas {XS[x]['L']:.2f}; k_term {XS[x]['kt']:.2f} rms {XS[x]['kts']:.2f}")
        XK[foot][lab] = XS
import itertools
sp = {}
for foot in FEET:
    k7 = xk(X7, foot, .7); k10 = xk(X7, foot, 1.); oo = [np.nanmean(k7[list(s)]) for s in itertools.combinations(range(7), 4)]; sp[foot] = (min(oo), max(oo), float(np.std(oo))); P(f"X-COP 4-of-7 splits, {foot}: k3(0.7) {min(oo):.2f} to {max(oo):.2f}, sd {np.std(oo):.2f}; all 7 {np.nanmean(k7):.2f}. Sample variance, single method. Over 35 splits")
R["splits"] = sp
# ------------------ HSC
h_ = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data; ENm = [str(n).strip() for n in h_["NAME"]]; E_short = {n.split("J")[-1]: i for i, n in enumerate(ENm)}; eMg, eM, eR = np.array(h_["MGAS500"], float) * 1e11, np.array(h_["M500"], float) * 1e13, np.array(h_["R500"], float)
AL, BE, GA, DE_ = .079, .965, .665, -.258; Fz = lambda z: np.log((1 + z) / 1.21)
def to_true(M, z): F = Fz(z); return 1e14 * np.exp((np.log(M / 1e14) - AL - GA * F) / (BE + DE_ * F))
def Rho(z, h=.7, Om=.3): return 3 * (h * 100e3 / 3.0857e22) ** 2 * (Om * (1 + z) ** 3 + 1 - Om) / (8 * math.pi * 6.674e-11)
def R_D(M, z, D): return (3 * M * 1.989e30 / (4 * np.pi * D * Rho(z))) ** (1 / 3) / 3.0857e19
OK = []
for r in FP.okabe():
    if r["id"] not in E_short or r["flag"] == "*" or r["z"] > .5 or r["M500"] is None: continue
    i = E_short[r["id"]]
    if eMg[i] > 0: OK.append(dict(id=r["id"], z=r["z"], m=r["M500"] * 1e14, m2=r["M200"] * 1e14, s=.5 * (r["up"] + r["dn"]) * 1e14, i=i, name=ENm[i]))
oz, om, om2, os_, oMg, oRc, oMc = [np.array([t[k] if k in t else 0 for t in OK], float) for k in ("z", "m", "m2", "s", "_", "_", "_")]; oMg = np.array([eMg[t["i"]] for t in OK]); oRc = np.array([eR[t["i"]] for t in OK]); oMc = np.array([eM[t["i"]] for t in OK]); o35 = np.array([t["name"] in names for t in OK])
ZB = np.array([0, .2, .35, .5001]); zb = np.clip(np.digitize(oz, ZB) - 1, 0, 2); s_med = np.array([np.median(os_[zb == k]) for k in range(3)]); owt = 1 / s_med[zb] ** 2
def gas_shape(c):
    lx = np.linspace(-1.5, 1., 101); S = np.full((N, len(lx)), np.nan); lb = np.log10(np.maximum(c.Mb, 1e-3)); lxx = np.log10(c.x)
    for i in range(N):
        if lxx[i, 0] < 0 < lxx[i, -1]: S[i] = np.interp(lx, lxx[i], lb[i], left=np.nan, right=np.nan) - np.interp(0, lxx[i], lb[i])
    cnt = np.isfinite(S).sum(0); M = np.nanmedian(S, 0); gd = cnt >= 20; g0, g1 = np.where(gd)[0][[0, -1]]; sl0 = (M[g0 + 5] - M[g0]) / (lx[g0 + 5] - lx[g0]); sl1 = (M[g1] - M[g1 - 5]) / (lx[g1] - lx[g1 - 5]); M[:g0] = M[g0] + sl0 * (lx[:g0] - lx[g0]); M[g1 + 1:] = M[g1] + sl1 * (lx[g1 + 1:] - lx[g1]); return lx, M
SH = gas_shape(PR); s_ = np.argsort(zc); QDP = np.polyfit(zc[s_], (PR.R5 / (np.array([eR[E_short[n.split('J')[-1]]] for n in names]) / 1e3))[s_], 3)
_nfw = lambda c: math.log(1 + c) - c / (1 + c)
RM2 = float(np.median(om2 / om)); C500 = brentq(lambda c: _nfw(c * (RM2 * 500 / 200) ** (1 / 3)) / _nfw(c) - RM2, .2, 30)
RAT = lambda x: _nfw(C500 * x) / _nfw(C500)
def hsc(ix, foot, x=1., m=None, fs=FS, shift=0.):
    m_ = om if m is None else m; w = owt[ix]; mb = (w * m_[ix]).sum() / w.sum(); zz = (w * oz[ix]).sum() / w.sum(); cf = float(to_true(np.array(mb), zz)) / mb; qd = np.polyval(QDP, oz[ix]); M5 = m_[ix] * cf * 10 ** shift; Mg5 = oMg[ix] * qd ** 2.5 * 10 ** .005; Rm0 = oRc[ix] * ((w * M5).sum() / (w * oMc[ix]).sum()) ** (1 / 3); Rm = Rm0 * x; g = 10 ** np.interp(np.log10(Rm / oRc[ix]), SH[0], SH[1]); Mg = Mg5 * g; a0 = A0[foot] * AX; Mm = M5 * RAT(x); ML = law_mass(Mg * (1 + fs), Rm * qd, a0); num = (w * (Mm * qd - ML)).sum(); den = (w * Mg).sum(); tm = (w * ML * G * Mg * MS / (Rm * qd * 1e3 * PCm) ** 2 / a0).sum(); return num / den, dict(Mt=(w * Mm * qd).sum() / den, L=(w * ML).sum() / den, kt=num / tm, lgMg=float(np.log10((w * oMg[ix]).sum() / w.sum())), lgM=float(np.log10(mb)))
def hboot(ix, foot, x=1., m=None, nb=NB, seed=SEED, fs=FS):
    rg = np.random.default_rng(seed); o = [hsc(rg.choice(ix, len(ix)), foot, x, m, fs) for _ in range(nb)]; return np.array([a[0] for a in o]), np.array([a[1]["Mt"] for a in o]), np.array([a[1]["kt"] for a in o])
def hmock(ix, foot, ktrue, nb=200, seed=SEED):
    """truth M_law + k Mg at cat aperture; eq. 17 forward; WL noise. Returns mean estimator - ktrue."""
    rg = np.random.default_rng(seed); a0 = A0[foot] * AX; qd = np.polyval(QDP, oz); M = oMc.copy()
    for _ in range(8):
        Rr = R_D(M, oz, 500); Mg = oMg * qd ** 2.5 * 10 ** .005 * 10 ** np.interp(np.log10(Rr / oRc), SH[0], SH[1]); M = (law_mass(Mg * (1 + FS), Rr * qd, a0) + ktrue * Mg) / qd
    F = Fz(oz); Mwl = 1e14 * np.exp(AL + (BE + DE_ * F) * np.log(M / 1e14) + GA * F); return float(np.mean([hsc(ix, foot, 1., np.maximum(Mwl + rg.normal(0, os_), 1e12))[0] for _ in range(nb)]) - ktrue)
GB = [(12.75, 13.2), (13.2, 13.58), (13.58, 14.5)]; lgo = np.log10(oMg); ALL = np.arange(len(OK)); O35 = np.where(o35)[0]; HS = {}
P(f"\nHSC Okabe x eRASS1 gas, N {len(OK)}, {o35.sum()} in the 326. Common aperture from the stack's mean mass. c500 from the median M200/M500 {RM2:.3f}: {C500:.2f}. x = 1 supported; other x NFW SHAPE. Mock correction subtracts the estimator's bias at this sample's noise")
for foot in FEET:
    HS[foot] = {}
    for nm, ix in [("all", ALL), ("35", O35)] + [(f"G{i}", np.where((lgo >= a) & (lgo < b))[0]) for i, (a, b) in enumerate(GB)]:
        v, inf = hsc(ix, foot); bb, by, bt = hboot(ix, foot); bias = hmock(ix, foot, 3.3); HS[foot][nm] = dict(k=v, s=float(bb.std()), bias=bias, kc=v - bias, N=len(ix), bb=bb, **inf, Mts=float(by.std()), kts=float(bt.std())); P(f"[{foot} {nm}] N {len(ix)} lg Mg {inf['lgMg']:.2f}: k3(1) raw {v:.2f} +- {bb.std():.2f}, mock bias {bias:+.2f}, corrected {v - bias:.2f}; M/Mg {inf['Mt']:.2f}, law/gas {inf['L']:.2f}; k_term {inf['kt']:.2f} +- {bt.std():.2f}")
    for x in (.6, 1.18, 1.67):
        v, inf = hsc(ALL, foot, x); bb, by, _ = hboot(ALL, foot, x, nb=500); HS[foot][f"x{x}"] = dict(k=v, s=float(bb.std()), Mt=inf["Mt"], L=inf["L"], Mts=float(by.std()), bb=bb); P(f"[{foot} all, NFW SHAPE] x {x}: k3 {v:.2f} +- {bb.std():.2f}; M/Mg {inf['Mt']:.2f}, law/gas {inf['L']:.2f}")
UXR = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_read.json")))["C"]["h0672"]; P("UX3 shear-to-shear IV A (read): " + ", ".join(f"{b} {UXR['raw|' + b]['iv'][0]:.3f} +- {max(UXR['raw|' + b]['iv'][1:]):.3f}" for b in ("all", "0.18-0.26", "0.38-0.81", "1.18-2.49")))
for foot in FEET:
    a = KID[f"{foot}|h0672|{FS}"]["I35"]; i1 = float(a["k"][3]); s1 = float(a["s"][3]); h3 = HS[foot]["35"]; d = h3["kc"] - i1; P(f"Same 35, {foot}: HSC k3(1) {h3['kc']:.2f} +- {h3['s']:.2f} (raw {h3['k']:.2f}); KiDS node x 1 {i1:.2f} +- {s1:.2f}; difference {d:.2f}, {d / math.hypot(h3['s'], s1):+.2f} sigma. Mass-level: M/Mg {h3['Mt']:.2f}")
interp_gas = lambda y: np.interp(np.log10([1., 1.18, 1.67]), np.log10(ND5), y)
# ------------------ pointed gas
GSI = list(csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_inputs.csv"))))
PT = {}
P("\nPointed gas, own Mgas, R500, M500, f* 0.034, no chain rescale. k3 at x 1. Means with cluster bootstrap; rms between clusters shown. These are mostly hydrostatic or scaling-relation masses, each its catalogue's own")
for foot in FEET:
    PT[foot] = {}
    for cat in ("L20", "S09", "L15", "L13", "M13", "V09"):
        rows = [r for r in GSI if r["cat"] == cat]; mg = np.array([float(r["Mgas"]) for r in rows]); Rk = np.array([float(r["R500"]) for r in rows]); m = np.array([float(r["M500"]) for r in rows]); g_ = (mg > 0) & (Rk > 0) & (m > 0); mg, Rk, m = mg[g_], Rk[g_], m[g_]; ml = law_mass(mg * (1 + FS), Rk, A0[foot] * AX); k = (m - ml) / mg; rg = np.random.default_rng(SEED); bb = [k[rg.integers(0, len(k), len(k))].mean() for _ in range(NB)]; PT[foot][cat] = dict(k=float(k.mean()), s=float(np.std(bb)), N=len(k), rms=float(k.std()), Mt=float((m / mg).mean()), lgM=float(np.log10(m).mean()), lgMg=float(np.log10(mg).mean())); bins = []
        for lo, hi in ((13., 14.), (14., 14.5), (14.5, 14.9), (14.9, 15.6)):
            q = (np.log10(m) >= lo) & (np.log10(m) < hi)
            if q.sum() >= 5: bins.append(f"{lo}-{hi}: {k[q].mean():.2f} +- {k[q].std() / math.sqrt(q.sum()):.2f} (N {q.sum()})")
        P(f"[{foot} {cat}] N {len(k)}, k3(1) {k.mean():.2f} +- {np.std(bb):.2f}, rms {k.std():.2f}, M/Mg {np.mean(m / mg):.2f}; " + "; ".join(bins))
# HSC x pointed
def j2d(s):
    a = s.split(".")[0]; sg = -1 if "-" in s else 1; hh = s.split("+" if sg > 0 else "-"); ra = 15 * (int(hh[0][:2]) + int(hh[0][2:4]) / 60 + float(hh[0][4:]) / 3600); d = hh[1]; return ra, sg * (int(d[:2]) + int(d[2:4]) / 60 + float(d[4:]) / 3600)
def sep(a1, d1, a2, d2): return np.degrees(np.arccos(np.clip(np.sin(np.radians(d1)) * np.sin(np.radians(d2)) + np.cos(np.radians(d1)) * np.cos(np.radians(d2)) * np.cos(np.radians(a1 - a2)), -1, 1)))
oRA = np.array([j2d(t["id"])[0] for t in OK]); oDE = np.array([j2d(t["id"])[1] for t in OK]); keep = oMg.copy(); pmatch = {}
for j, t in enumerate(OK):
    bst = None
    for r in GSI:
        if r["cat"] == "E16": continue
        try: z_, ra_, de_, mg_, Rk_ = float(r["z"]), float(r["ra"]), float(r["dec"]), float(r["Mgas"]), float(r["R500"])
        except ValueError: continue
        if abs(z_ - t["z"]) > .02: continue
        s0 = sep(oRA[j], oDE[j], ra_, de_)
        if s0 < 3 / 60 and (bst is None or s0 < bst[0]): bst = (s0, mg_, Rk_, r["cat"], float(r["M500"]))
    if bst is not None: pmatch[j] = bst
ixp = np.array(sorted(pmatch)); P(f"HSC x pointed gas, positional match 3 arcmin, |dz| <= 0.02, Okabe N {len(OK)}: {len(ixp)} matched")
if len(ixp) >= 8:
    alt_mg = keep.copy(); alt_R = oRc.copy()
    for j in ixp:
        s0, mg_, Rk_, cat, _ = pmatch[j]; alt_mg[j] = mg_ * 10 ** (-np.interp(np.log10(Rk_ / oRc[j]), SH[0], SH[1])) # pointed gas at the catalogue R500
    for foot in FEET:
        a, inf = hsc(ixp, foot); bb, _, _ = hboot(ixp, foot, nb=1000); oMg = alt_mg; b2, inf2 = hsc(ixp, foot); bb2, _, _ = hboot(ixp, foot, nb=1000); oMg = keep; P(f"[{foot}] same clusters, HSC mass: eRASS1 gas k3(1) {a:.2f} +- {bb.std():.2f}; pointed gas {b2:.2f} +- {bb2.std():.2f}. M/Mg {inf['Mt']:.2f}, {inf2['Mt']:.2f}. Median lg gas ratio pointed/eRASS1 {np.median(np.log10(alt_mg[ixp] / keep[ixp])):+.3f}"); R[f"hsc_pointed|{foot}"] = dict(N=len(ixp), e=a, p=b2, se=float(bb.std()), sp=float(bb2.std()))
# Umetsu x E16
U = FP.tsv(os.path.join(RB, "FR3_retention_independent", "data", "umetsu20_table2.tsv"))["J/ApJ/890/148/table2"]; Xx = {int(r["XLSSC"]): r for r in list(FP.tsv(os.path.join(REPO, "_external_data", "gs4", "xxl100", "xxl100gc.tsv")).values())[0]}
UU = []
for r in U:
    x_ = Xx.get(int(r["XLSSC"]))
    if x_ is None: continue
    z_ = FP.fl(r["z"]); mg_ = FP.fl(x_["Mgas500"]) * 1e13; Rk_ = FP.fl(x_["r500MT"]) * 1e3; mu = FP.fl(r["M500"]) * 1e14; su = FP.fl(r["e_M500"]) * 1e14
    if z_ <= .5 and mg_ > 0 and Rk_ > 0 and np.isfinite(mu) and 10 ** 12.75 <= mg_ < 10 ** 13.58: UU.append((z_, mg_, Rk_, mu, su))
UU = np.array(UU)
for foot in FEET:
    wu = 1 / np.median(UU[:, 4]) ** 2; rat = (UU[:, 3].sum() / (4 / 3 * math.pi * 500 * np.array([Rho(z) for z in UU[:, 0]]) * (UU[:, 2] * 3.0857e19) ** 3 / MS).sum()) ** (1 / 3); Rr = UU[:, 2] * rat; g = 10 ** np.interp(np.log10(rat), SH[0], SH[1]); ml = law_mass(UU[:, 1] * g * 1.034, Rr, A0[foot] * AX); num = UU[:, 3] - ml; den = UU[:, 1] * g; rg = np.random.default_rng(SEED); bb = [(lambda j: num[j].sum() / den[j].sum())(rg.integers(0, len(UU), len(UU))) for _ in range(NB)]; R[f"umetsu|{foot}"] = dict(N=len(UU), k=float(num.sum() / den.sum()), s=float(np.std(bb)), M=float(np.log10(UU[:, 3].mean()))); P(f"Umetsu+20 HSC x E16 XMM, {foot}, gas bin 12.75-13.58, z <= 0.5: N {len(UU)}, k3(1) {num.sum() / den.sum():.2f} +- {np.std(bb):.2f}, M/Mg {UU[:, 3].sum() / den.sum():.2f}, aperture stack R/R_XXL {rat:.3f}")
# ------------------ third mass
P("\nThird mass. Match 3 arcmin, |dz| <= 0.02, against the 326 and the 35. Ratios are ratio of sums on shared clusters, cluster bootstrap")
def tsvrows(p):
    T = FP.tsv(p); return list(T.values())[0]
Ps = tsvrows(os.path.join(DATA, "psz2_union.tsv")); TM = {}
pr = [(FP.fl(r["RAJ2000"]), FP.fl(r["DEJ2000"]), FP.fl(r["z"]), FP.fl(r["MSZ"]) * 1e14) for r in Ps]; pr = np.array([p for p in pr if p[2] > 0 and p[3] > 0]); msz = np.full(N, np.nan)
for i in range(N):
    s0 = sep(RA[i], DEC[i], pr[:, 0], pr[:, 1]); g_ = (s0 < 3 / 60) & (np.abs(pr[:, 2] - zc[i]) <= .02)
    if g_.any(): msz[i] = pr[g_][np.argmin(s0[g_]), 3]
TM["PSZ2 MSZ"] = msz
Gm = list(csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_matched.csv")))); L20M = {r["name"]: float(r["M500"]) for r in GSI if r["cat"] == "L20"}; l20 = np.full(N, np.nan)
for r in Gm:
    if r["cat"] == "L20" and r["erass"].strip() in names: l20[names.index(r["erass"].strip())] = L20M[r["name"]]
TM["L20 HSE"] = l20
GR = []
for ln in open(os.path.join(DATA, "groener2016_cluster_concentrations.tsv")):
    if ln.startswith("#") or not ln.strip() or ln.startswith("recno") or ln.startswith("---") or ln.startswith(" \t"): continue
    a = ln.rstrip("\n").split("\t"); 
    if len(a) < 25: continue
    def sx(s, f=1.):
        q = s.split(); sg = -1 if s.strip().startswith("-") else 1; return f * sg * (abs(float(q[0])) + float(q[1]) / 60 + float(q[2]) / 3600)
    try: GR.append(dict(ra=sx(a[3], 15.), de=sx(a[4]), z=FP.fl(a[2]), meth=a[5].strip(), c=FP.fl(a[6]), M=FP.fl(a[9]) * 1e14, h=FP.fl(a[24]), name=a[1].strip()))
    except (ValueError, IndexError): pass
meths = {}
for r in GR: meths[r["meth"]] = meths.get(r["meth"], 0) + 1
P(f"Groener+16 rows {len(GR)}, methods {meths}")
for me in ("WL", "XSZ", "X-ray", "CM", "SL", "WL+SL", "LOSVD", "Xray"):
    rows = [r for r in GR if r["meth"] == me and r["M"] > 0 and r["c"] > 0 and np.isfinite(r["h"])]
    if not rows: continue
    v = [[] for _ in range(N)]
    for r in rows:
        s0 = sep(RA, DEC, r["ra"], r["de"]); j = np.where((s0 < 3 / 60) & (np.abs(zc - r["z"]) <= .02))[0]
        if len(j):
            f_ = brentq(lambda t: _nfw(r["c"] * t) / t ** 3 / _nfw(r["c"]) - 2.5, .1, 1.); v[j[0]].append(r["M"] * (r["h"] / .7) * _nfw(r["c"] * f_) / _nfw(r["c"]))
    TM[f"Groener {me}"] = np.array([np.median(a) if a else np.nan for a in v])
okm = np.full(N, np.nan); okc = np.full(N, np.nan)
for j in O35: i = names.index(OK[j]["name"]); okm[i] = om[j]; okc[i] = oMc[j]
catm = np.array([eM[E_short[n.split("J")[-1]]] for n in names]); catr = np.array([eR[E_short[n.split("J")[-1]]] for n in names]); catg = np.array([eMg[E_short[n.split("J")[-1]]] for n in names])
def rats(a, b, sel, nb=NB, seed=SEED):
    ix = np.where(sel)[0]; rg = np.random.default_rng(seed); bb = [(lambda j: a[j].sum() / b[j].sum())(rg.choice(ix, len(ix))) for _ in range(nb)]; return float(a[ix].sum() / b[ix].sum()), float(np.std(bb))
S_ = C.Shear(.005, .034); CHAIN = "h0672"
def nfwM(M500, R500_mpc):
    rs = R500_mpc / C500; x = C.RG / rs; return M500 * MS * (np.log1p(x) - x / (1 + x)) / _nfw(C500)
def Vn(mass, sel, hk=CHAIN):
    h = HV[hk]; V = np.full((N, 8), np.nan)
    for i in np.where(sel)[0]:
        qq = S_.chain[hk][i]; z = float(zc[i]); DM = float(S_._dm(min(z, 2.33))) * 101.54 / h; q = (DM / (1 + z)) / S_._DAcat(z); Rd = R_D(mass[i], z, 500) / 1e3 * q; V[i], _ = S_.vector(i, hk, nfwM(mass[i] * q, Rd))
    return V
nP, WP = nsum("h0672"); UL = B["Vl_canonical_h0672"]
def ampIV(V, sel):
    ix = np.where(sel)[0]; w = np.where(WP[ix] > 0, 1 / np.where(WP[ix] > 0, WP[ix], 1), 0); ok = np.isfinite(V[ix]) & (WP[ix] > 0); f = lambda j: (nP[ix][j] * UL[ix][j] * w[j] * ok[j]).sum() / (np.nan_to_num(V[ix][j]) * UL[ix][j] * w[j] * ok[j]).sum(); v = f(np.arange(len(ix))); rg = np.random.default_rng(SEED); bb = [f(rg.integers(0, len(ix), len(ix))) for _ in range(500)]; return float(v), float(np.std(bb))
s35 = np.isfinite(okm); VO = Vn(okm, s35); AO = ampIV(VO, s35); check("K5", abs(AO[0] - UXR["raw|all"]["iv"][0]) <= .03, f"KiDS / NFW(Okabe) on the 35, own path, c500 {C500:.2f}: A {AO[0]:.3f} +- {AO[1]:.3f}, UX3 {UXR['raw|all']['iv'][0]:.3f}")
THIRD = {}
def k_third(M, sel, foot):
    ix = np.where(sel)[0]; a0 = A0[foot] * AX; qd = np.polyval(QDP, zc[ix]); M_ = M[ix]; Rd = R_D(M_, zc[ix], 500); g = 10 ** np.interp(np.log10(Rd / catr[ix]), SH[0], SH[1]); Mg = catg[ix] * qd ** 2.5 * 10 ** .005 * g; ML = law_mass(Mg * 1.034, Rd * qd, a0); nm = M_ * qd - ML; f = lambda j: nm[j].sum() / Mg[j].sum(); rg = np.random.default_rng(SEED); bb = [f(rg.integers(0, len(ix), len(ix))) for _ in range(NB)]; return float(f(np.arange(len(ix)))), float(np.std(bb)), float((M_ * qd).sum() / Mg.sum())
for nm, M in TM.items():
    a = np.isfinite(M) & (M > 0); b = a & s35; lab = "THIN" if b.sum() < 8 else "votes"; o = dict(N326=int(a.sum()), N35=int(b.sum()), label=lab)
    if a.sum() >= 5:
        o["r_cat"] = rats(M, catm, a); ks = {f: k_third(M, a, f) for f in FEET}; o["k326"] = ks; VT = Vn(M, a); o["A_KiDS"] = ampIV(VT, a); ku = {f: float(KID[f"{f}|h0672|{FS}"]["all"]["k"][3]) for f in FEET}; P(f"[{nm}] shared with 326: {a.sum()}, with the 35: {b.sum()} ({lab}). M / catalogue M500 {o['r_cat'][0]:.3f} +- {o['r_cat'][1]:.3f}; k3(1) own R500 canonical {ks['canonical'][0]:.2f} +- {ks['canonical'][1]:.2f}, alt {ks['alt'][0]:.2f} +- {ks['alt'][1]:.2f}; M/Mg {ks['canonical'][2]:.2f}; KiDS / NFW(this mass) {o['A_KiDS'][0]:.3f} +- {o['A_KiDS'][1]:.3f}")
    else: P(f"[{nm}] shared with 326: {a.sum()}, with the 35: {b.sum()} ({lab})")
    if b.sum() >= 5:
        o["r_ok"] = rats(M, okm, b); ks = {f: k_third(M, b, f) for f in FEET}; ko = {f: k_third(okm, b, f) for f in FEET}; o["k35"] = ks; o["k35_ok"] = ko; VT = Vn(M, b); o["A35"] = ampIV(VT, b); o["AO_same"] = ampIV(VO, b); P(f"   on shared 35: M / Okabe {o['r_ok'][0]:.3f} +- {o['r_ok'][1]:.3f}; k3(1) this {ks['canonical'][0]:.2f} +- {ks['canonical'][1]:.2f}, Okabe, raw same form {ko['canonical'][0]:.2f} +- {ko['canonical'][1]:.2f}; KiDS / NFW(this) {o['A35'][0]:.3f} +- {o['A35'][1]:.3f}; KiDS / NFW(Okabe) {o['AO_same'][0]:.3f} +- {o['AO_same'][1]:.3f}")
    THIRD[nm] = o
R["third"] = THIRD
# POST-CRITERIA rows: third masses against the whole eRASS1 catalogue and all Okabe, not only the 326
P("\nPOST-CRITERIA. PSZ2 and L20 masses on all of eRASS1 (z <= 0.5, gas > 0), and on Okabe's 60. eRASS1 gas at the own R500 of each mass; h 0.70 frame, no native q. Reported only")
ez = np.array(h_["BEST_Z"], float); eRA = np.array(h_["RA"], float); eDE = np.array(h_["DEC"], float); pc = np.array(h_["PCONT"], float) if "PCONT" in h_.names else np.zeros(len(ez)); POST = {}
def post_k(M, Mg, Rc, z, foot):
    Rd = R_D(M, z, 500); g = 10 ** np.interp(np.log10(Rd / Rc), SH[0], SH[1]); mg = Mg * g; ml = law_mass(mg * 1.034, Rd, A0[foot] * AX); nm = M - ml; f = lambda j: nm[j].sum() / mg[j].sum(); rg = np.random.default_rng(SEED); bb = [f(rg.integers(0, len(M), len(M))) for _ in range(NB)]; return float(f(np.arange(len(M)))), float(np.std(bb)), float(M.sum() / mg.sum())
gdE = np.where((ez > 0) & (ez <= .5) & (eMg > 0) & (eM > 0) & (eR > 0) & (pc < .5))[0]; iE = []; iP = []
for i in gdE:
    s0 = sep(eRA[i], eDE[i], pr[:, 0], pr[:, 1]); g_ = (s0 < 3 / 60) & (np.abs(pr[:, 2] - ez[i]) <= .02)
    if g_.any(): iE.append(i); iP.append(np.where(g_)[0][np.argmin(s0[g_])])
iE = np.array(iE); iP = np.array(iP); msP = pr[iP, 3]; lgE = np.log10(eMg[iE]); POST["PSZ2_eRASS"] = {}
for foot in FEET:
    a = post_k(msP, eMg[iE], eR[iE], ez[iE], foot); bins = []
    for lo, hi in ((13., 13.58), (13.58, 13.9), (13.9, 14.6)):
        q = (lgE >= lo) & (lgE < hi)
        if q.sum() >= 5: t_ = post_k(msP[q], eMg[iE][q], eR[iE][q], ez[iE][q], foot); bins.append(f"lg Mg {lo}-{hi}: {t_[0]:.2f} +- {t_[1]:.2f} (N {q.sum()}, M/Mg {t_[2]:.2f})")
    POST["PSZ2_eRASS"][foot] = a; P(f"[{foot}] eRASS1 x PSZ2: N {len(iE)}, MSZ / M500 catalogue {rats(msP, eM[iE], np.ones(len(iE), bool))[0]:.3f}; k3(1) {a[0]:.2f} +- {a[1]:.2f}, M/Mg {a[2]:.2f}; " + "; ".join(bins))
iO = []; iQ = []
for j in range(len(OK)):
    s0 = sep(oRA[j], oDE[j], pr[:, 0], pr[:, 1]); g_ = (s0 < 3 / 60) & (np.abs(pr[:, 2] - oz[j]) <= .02)
    if g_.any(): iO.append(j); iQ.append(np.where(g_)[0][np.argmin(s0[g_])])
iO = np.array(iO, int); iQ = np.array(iQ, int); POST["PSZ2_Okabe"] = dict(N=len(iO))
if len(iO) >= 5:
    r_ = rats(pr[iQ, 3], om[iO], np.ones(len(iO), bool)); r2 = rats(oMc[iO], om[iO], np.ones(len(iO), bool)); POST["PSZ2_Okabe"].update(r=r_, rcat=r2); P(f"Okabe x PSZ2: N {len(iO)}, MSZ / Okabe M500 raw {r_[0]:.3f} +- {r_[1]:.3f}; catalogue M500 / Okabe {r2[0]:.3f} +- {r2[1]:.3f}. Okabe's masses are noisy but ratio of sums. Eq. 17 not applied here")
else: P(f"Okabe x PSZ2: N {len(iO)}, THIN")
Lr = [r for r in Gm if r["cat"] == "L20"]; POST["L20"] = {}
if Lr:
    iL = np.array([E_ix for E_ix in [ENm.index(r["erass"].strip()) if r["erass"].strip() in ENm else -1 for r in Lr]]); mL = np.array([L20M[r["name"]] for r in Lr]); gL = iL >= 0; iL, mL = iL[gL], mL[gL]; gg = (eMg[iL] > 0) & (eR[iL] > 0) & (eM[iL] > 0) & (ez[iL] <= .5); iL, mL = iL[gg], mL[gg]
    for foot in FEET: a = post_k(mL, eMg[iL], eR[iL], ez[iL], foot); POST["L20"][foot] = a; P(f"[{foot}] eRASS1 gas x L20 HSE mass: N {len(iL)}, L20 M / catalogue M500 {rats(mL, eM[iL], np.ones(len(iL), bool))[0]:.3f}; k3(1) {a[0]:.2f} +- {a[1]:.2f}, M/Mg {a[2]:.2f}")
R["post"] = POST
# ------------------ separation
P("\nSeparation. lg k = a + s lg x + p (lg Mg - 13.3) + m_method. KiDS terciles x nodes 0.35, 0.6, 1; X-COP x 0.3, 0.5, 0.7, 1; HSC gas bins x 1, mock-corrected")
def sepvec(foot, h="h0672", shift=None, axis="Mg"):
    KC = KID[f"{foot}|{h}|{FS}"]; vals = []; lab = []; drop = []; blocks = []
    for t in range(3):
        q = KC[f"T{t}"]; idx = [1, 2, 3]; c2 = q["cov"][np.ix_(idx, idx)]; v = q["k"][idx]; lm = np.log10(Mg0[T3 == t]).mean() if axis == "Mg" else np.log10(catm[T3 == t]).mean()
        keep_ = [i for i in range(3) if v[i] > .3 * math.sqrt(c2[i, i])]; drop += [("KiDS", t, ND5[idx[i]], float(v[i])) for i in range(3) if i not in keep_]
        blocks.append((np.array([v[i] for i in keep_]), c2[np.ix_(keep_, keep_)], [(ND5[idx[i]], lm, 0) for i in keep_]))
    xs = [.3, .5, .7, 1.]; XS = XK[foot]["7"]; vv = np.array([XS[x]["k"] if shift is None else XS[x]["bracket"] for x in xs]); bbm = np.array([XS[x]["bb"] + (vv[i] - XS[x]["k"]) for i, x in enumerate(xs)]); c2 = np.cov(bbm); lm = float(np.mean([math.log10(c["rows"][1.][2]) for c in X7 if 1. in c["rows"]])) if axis == "Mg" else float(np.mean([math.log10(c["rows"][1.][1]) for c in X7 if 1. in c["rows"]])); blocks.append((vv, c2, [(x, lm, 1) for x in xs]))
    for i in range(3):
        q = HS[foot][f"G{i}"]; blocks.append((np.array([q["kc"]]), np.array([[q["s"] ** 2]]), [(1., q["lgMg"] if axis == "Mg" else q["lgM"], 2)]))
    y = np.concatenate([b[0] for b in blocks]); n = len(y); CV = np.zeros((n, n)); meta = []; o_ = 0
    for b in blocks:
        m_ = len(b[0]); CV[o_:o_ + m_, o_:o_ + m_] = b[1]; meta += b[2]; o_ += m_
    return y, CV, np.array(meta), drop
def gls(y, CV, mt, xp, pp, off, pivot=13.3):
    ly = np.log10(y); J = np.diag(1 / (y * math.log(10))); Cl = J @ CV @ J; Ci = np.linalg.pinv(Cl); cols = [np.ones(len(y))]; nm = ["a"]
    if xp: cols.append(np.log10(mt[:, 0])); nm.append("s")
    if pp: cols.append(mt[:, 1] - (pivot if pivot else 0)); nm.append("p")
    if off: cols += [(mt[:, 2] == 1) * 1., (mt[:, 2] == 2) * 1.]; nm += ["m_HSE", "m_HSC"]
    A = np.column_stack(cols); Cv = np.linalg.inv(A.T @ Ci @ A); th = Cv @ A.T @ Ci @ ly; r = ly - A @ th; c2 = float(r @ Ci @ r); dof = len(y) - len(th); return dict(chi2=c2, dof=dof, pv=float(CH2.sf(c2, dof)), **{n_: (float(t), float(math.sqrt(v))) for n_, t, v in zip(nm, th, np.diag(Cv))})
SEP = {}
for foot in FEET:
    for tag, h, sh, ax in (("primary", "h0672", None, "Mg"), ("h0686", "h0686", None, "Mg"), ("HSE-0.12", "h0672", -.12, "Mg"), ("M500 axis", "h0672", None, "M")):
        y, CV, mt, dr = sepvec(foot, h, sh, ax); o = {}; piv = 13.3 if ax == "Mg" else 14.5
        for nm, (a, b, c_) in dict(H1=(0, 0, 0), Hx=(1, 0, 0), HM=(0, 1, 0), HxM=(1, 1, 0), H1o=(0, 0, 1), Hxo=(1, 0, 1), HMo=(0, 1, 1), HxMo=(1, 1, 1)).items(): o[nm] = gls(y, CV, mt, a, b, c_, piv)
        SEP[f"{foot}|{tag}"] = o; f = o["HxMo"]; P(f"[{foot} {tag}] N {len(y)}, dropped {dr}"); P("   chi2/dof p: " + "; ".join(f"{k} {v['chi2']:.1f}/{v['dof']} {v['pv']:.1e}" for k, v in o.items())); P(f"   HxMo: k(1, 13.3) {10 ** f['a'][0]:.2f}, s {f['s'][0]:+.3f} +- {f['s'][1]:.3f}, p {f['p'][0]:+.3f} +- {f['p'][1]:.3f}, m_HSE {f['m_HSE'][0]:+.3f} +- {f['m_HSE'][1]:.3f} dex, m_HSC {f['m_HSC'][0]:+.3f} +- {f['m_HSC'][1]:.3f} dex")
        if tag == "primary":
            s_ = abs(f["s"][0]) / f["s"][1]; pz = abs(f["p"][0]) / f["p"][1]; mz = [abs(f[m][0]) / f[m][1] for m in ("m_HSE", "m_HSC")]; ls = "FUNCTION OF x" if s_ >= 3 else "x NOT LABELLED"; lp = "FUNCTION OF MASS" if pz >= 3 else ("FLAT IN MASS" if pz < 2 and f["p"][1] <= .2 else "MASS NOISE-LIMITED"); lm = "METHOD OFFSET" if max(mz) >= 3 else ("METHODS AGREE" if max(mz) < 2 and max(f["m_HSE"][1], f["m_HSC"][1]) <= .05 else "METHOD NOISE-LIMITED"); h1 = o["H1"]; l1 = "ONE NUMBER" if h1["pv"] >= .01 else "NOT ONE NUMBER"; SEP[f"{foot}|labels"] = dict(x=ls, M=lp, method=lm, one=l1, s_Z=s_, p_Z=pz, m_Z=mz); P(f"   LABELS {foot}: {l1}; {ls} ({s_:.1f} sigma); {lp} ({pz:.1f}); {lm} (HSE {mz[0]:.1f}, HSC {mz[1]:.1f})")
P("\nPOST-CRITERIA separation rows. Each method alone; and HSC with its own systematic budget (0.035 dex in mass) on the block")
for foot in FEET:
    y, CV, mt, dr = sepvec(foot); kk = mt[:, 2] == 0; xx = mt[:, 2] == 1; hh = mt[:, 2] == 2
    a = gls(y[kk], CV[np.ix_(kk, kk)], mt[kk], 1, 1, 0); b = gls(y[xx], CV[np.ix_(xx, xx)], mt[xx], 1, 0, 0); c_ = gls(y[hh], CV[np.ix_(hh, hh)], mt[hh], 0, 1, 0); P(f"[{foot}] KiDS alone s {a['s'][0]:+.3f} +- {a['s'][1]:.3f}, p {a['p'][0]:+.3f} +- {a['p'][1]:.3f}, chi2 {a['chi2']:.1f}/{a['dof']}; X-COP alone s {b['s'][0]:+.3f} +- {b['s'][1]:.3f}, chi2 {b['chi2']:.1f}/{b['dof']}; X-COP s doubled sigma (LM1's N 7 rule) {2 * b['s'][1]:.3f}; HSC alone p {c_['p'][0]:+.3f} +- {c_['p'][1]:.3f}, chi2 {c_['chi2']:.1f}/{c_['dof']}")
    CV2 = CV.copy(); j = np.where(hh)[0]; ss = np.array([HS[foot][f"G{i}"]["Mt"] * math.log(10) * math.sqrt(.031 ** 2 + .015 ** 2 + .006 ** 2) for i in range(3)]); CV2[np.ix_(j, j)] += np.outer(ss, ss); g2 = gls(y, CV2, mt, 1, 1, 1); nh = kk | hh; g3 = gls(y[nh], CV[np.ix_(nh, nh)], mt[nh], 1, 1, 1) if False else None; R[f"sep_sys|{foot}"] = g2; P(f"   HSC sys coherent over its 3 bins: m_HSC {g2['m_HSC'][0]:+.3f} +- {g2['m_HSC'][1]:.3f} ({abs(g2['m_HSC'][0]) / g2['m_HSC'][1]:.1f} sigma), m_HSE {g2['m_HSE'][0]:+.3f} +- {g2['m_HSE'][1]:.3f}, s {g2['s'][0]:+.3f}, p {g2['p'][0]:+.3f} +- {g2['p'][1]:.3f}, chi2 {g2['chi2']:.1f}/{g2['dof']}")
    no = ~hh; g4 = gls(y[no], CV[np.ix_(no, no)], mt[no], 1, 1, 0); P(f"   KiDS and X-COP, no HSC, no offset: s {g4['s'][0]:+.3f} +- {g4['s'][1]:.3f}, p {g4['p'][0]:+.3f} +- {g4['p'][1]:.3f}, chi2 {g4['chi2']:.1f}/{g4['dof']}, p-value {g4['pv']:.3f}")
    T1 = KT[foot]["node"]; kv = T1["k"][1:4]; cc = T1["cov"][1:4, 1:4]; Ci = np.linalg.inv(cc); o_ = np.ones(3); m0 = (o_ @ Ci @ kv) / (o_ @ Ci @ o_); ch = (kv - m0) @ Ci @ (kv - m0); P(f"   k_term KiDS nodes 0.35, 0.6, 1 constant at {m0:.2f}: chi2 {ch:.2f}/2, p {CH2.sf(ch, 2):.3f}. k_term X-COP x 0.3, 0.5, 0.7, 1: {[round(XK[foot]['7'][x]['kt'], 2) for x in (.3, .5, .7, 1.)]}; HSC x 1 {HS[foot]['all']['kt']:.2f} +- {HS[foot]['all']['kts']:.2f}")
P("\nPOST-CRITERIA. X-COP on eRASS1, same clusters, what eRASS1's own gas and mass read against X-COP's")
XCP = []
for c0 in X7 + [c for c in X12 if not c["stars"]]:
    with fits.open(os.path.join(DATA, "xcop", c0["name"], f"{c0['name']}_fgas_profile.fits")) as q: ra_, de_ = float(q[1].header["RA"]), float(q[1].header["DEC"])
    j = np.where((sep(ra_, de_, eRA, eDE) < 6 / 60) & (eMg > 0))[0]
    if len(j) and 1. in c0["rows"]:
        r, mh, mg, ms, em = c0["rows"][1.]; i = j[0]; XCP.append((c0["name"], mg, mh, r, eMg[i], eM[i], eR[i], c0["stars"], names.index(ENm[i]) if ENm[i] in names else -1))
if XCP:
    gx = np.array([math.log10(a[1] * 10 ** np.interp(0, SH[0], SH[1]) / (a[4] * 10 ** np.interp(np.log10(a[3] / a[6]), SH[0], SH[1]))) for a in XCP]); mx = np.array([math.log10(a[2] / a[5]) for a in XCP]); rx = np.array([math.log10(a[3] / a[6]) for a in XCP]); P(f"Matched {len(XCP)}, {sum(a[8] >= 0 for a in XCP)} in the 326: {[a[0] for a in XCP]}. lg X-COP gas / eRASS1 gas, both at X-COP's R500: {gx.mean():+.3f} +- {gx.std() / math.sqrt(len(gx)):.3f}; lg HSE M500 / catalogue M500 {mx.mean():+.3f} +- {mx.std() / math.sqrt(len(mx)):.3f}; lg R500 ratio {rx.mean():+.3f}"); R["xcop_erass"] = dict(N=len(XCP), gas=float(gx.mean()), gs=float(gx.std() / math.sqrt(len(gx))), mass=float(mx.mean()), ms=float(mx.std() / math.sqrt(len(mx))))
if XCP and not MUT:
    dg = float(gx.mean()); fg = 10 ** dg; P(f"What if eRASS1's gas were low by that offset everywhere, {dg:+.3f} dex? Approximate, not a claim: GS4 on more clusters and other catalogues found +0.005, so this offset is 5 clusters against that. V rescaled by the law's ratio per bin, basis by the gas factor")
    for foot in FEET:
        c = Cell(foot, "h0672"); rr_ = law_mass(c.Mb * fg, RC[None, :] * 1e3, A0[foot]) / np.where(c.ML > 0, law_mass(c.Mb, RC[None, :] * 1e3, A0[foot]), 1); e2 = c.n - c.V * rr_; G2 = five(c.G6) * fg; a = fitnodes(c, G2, e2, jack=False); y = fitnodes(c, G2, c.n, jack=False); keep2 = oMg.copy(); oMg = keep2 * fg; hk_, ihk = hsc(ALL, foot); oMg = keep2; P(f"[{foot}] KiDS k3 nodes {fmt(a['k'])} +- {fmt(a['s'])}; Y at x 1, 1.18, 1.67 {fmt(interp_gas(y['k']) / 1.034)}; HSC raw k3(1) {hk_:.2f}, M/Mg {ihk['Mt']:.2f}. X-COP unchanged: k3(1) {XK[foot]['7'][1.]['k']:.2f}, Y(1) 6.38"); R[f"gasrow|{foot}"] = dict(k=a["k"], s=a["s"], hsc=hk_, Mt=ihk["Mt"])
# ------------------ bits
def ceil(v, s): return math.log2(2 / math.log10((v + 2 * s) / (v - 2 * s))) if v > 2 * s else 0.
P("\nError and bits. k3 at pivots; sigma_stat per method. Ceiling on +- 1 dex; after log2(15) = 3.91 subtract. BK1's line is 10 bits")
BIT = {}
for foot in FEET:
    Kall = KID[f"{foot}|h0672|{FS}"]["all"]; XS = XK[foot]["7"]; rows = {}
    for piv, ik in ((.6, 2), (1., 3)):
        kv, ks = float(Kall["k"][ik]), float(Kall["s"][ik]); xv, xs = XS[piv]["k"], XS[piv]["s"]; xb = XS[piv]["bracket"]; hk = HS[foot]["all"] if piv == 1. else HS[foot]["x0.6"]; hv = hk.get("kc", hk["k"]); hs = hk["s"]; hsys = hv * 0 + (hk.get("Mt") or 0) * math.log(10) * math.sqrt(.031 ** 2 + .015 ** 2 + .006 ** 2); vals = [kv, xv, hv]; ssys = (max(vals) - min(vals)) / 2; mid = float(np.mean(vals)); tot = math.hypot(min(ks, xs, hs), ssys); w = 1 / np.array([ks, xs, hs]) ** 2; wm = float((w * vals).sum() / w.sum()); sw = float(w.sum() ** -.5); chi = float((w * (np.array(vals) - wm) ** 2).sum())
        rows[piv] = dict(kids=(kv, ks), hse=(xv, xs), hse_bracket=xb, hsc=(hv, hs), hsc_sys=hsys, sys=ssys, mid=mid, tot=tot, wm=wm, sw=sw, chi=chi, ceil_stat=ceil(kv, ks), ceil_tot=ceil(mid, tot), ceil_wm=ceil(wm, sw))
        P(f"[{foot}] x {piv}: KiDS {kv:.2f} +- {ks:.2f} ({100 * ks / kv:.0f} %); HSE {xv:.2f} +- {xs:.2f} ({100 * xs / xv:.0f} %), bracket {xb:.2f}; HSC {hv:.2f} +- {hs:.2f} ({100 * hs / hv:.0f} %) +- {hsys:.2f} sys. sigma_sys {ssys:.2f}, mid {mid:.2f}, total {tot:.2f} ({100 * tot / mid:.0f} %). IV-combined, if methods agreed: {wm:.2f} +- {sw:.2f} ({100 * sw / wm:.0f} %), chi2/2 {chi:.1f} p {CH2.sf(chi, 2):.3f}. Ceiling bits: KiDS stat {rows[piv]['ceil_stat']:.2f}, total {rows[piv]['ceil_tot']:.2f}, IV {rows[piv]['ceil_wm']:.2f}; after look-elsewhere {max(0, rows[piv]['ceil_tot'] - 3.91):.2f}")
    cr = np.corrcoef(Kall["bb"].T)[1:4, 1:4]; ev = np.linalg.eigvalsh(cr); neff = float(ev.sum() ** 2 / (ev ** 2).sum()); perN = [ceil(float(Kall["k"][i]), float(Kall["s"][i])) for i in (1, 2, 3)]; BIT[foot] = dict(rows=rows, neff=neff, per=perN, corr=cr.tolist()); P(f"   3-node shape (x 0.35, 0.6, 1, KiDS stat only): correlations {np.round(cr[np.triu_indices(3, 1)], 2).tolist()}, effective count {neff:.2f}; node ceilings {np.round(perN, 2).tolist()}; sum-with-neff bound {neff / 3 * sum(perN):.2f}, before look-elsewhere")
    ks1 = float(Kall["s"][3]) / float(Kall["k"][3]); P(f"   Scale: KiDS stat at x 1 is {100 * ks1:.0f} %. 1 % stat needs N x {(ks1 / .01) ** 2:.0f} at this depth, {326 * (ks1 / .01) ** 2:.0f} clusters, sqrt(N) only, no systematic floor")
R["bits"] = BIT
# ------------------ f_b reading
P(f"\nf_b reading, a description. 1/f_b {1 / FB['native']:.3f} (native), {1 / FB['bk1']:.3f} (BK1); Y = M_tot / M_b, f* {FS}")
FBR = {}
c = PR; xb = [(.5, 1.), (1., 1.4), (1.4, 2.)]; Xc = [.7, 1.18, 1.67]
def interp_Y(y, x): return np.interp(np.log10(x), np.log10(ND5), y)
fbn = FB["native"]; Lz = {}
for foot in FEET:
    c = Cell(foot, "h0672"); Mt = KID[f"{foot}|h0672|{FS}"]["Mtot_Mg"]; rows = []; bb = Mt["bb"]; sc = np.mean(Mt["s"] / np.maximum(Mt["sb"], 1e-9))
    A = []; 
    for (lo, hi), xc in zip(xb, Xc):
        m = (c.x >= lo) & (c.x < hi) & (c.W > 0); w = np.where(m, 1 / np.where(c.W > 0, c.W, 1), 0); nsum_ = ((c.n * c.VN * w).sum(1)); vsum = ((c.VN * c.VN * w).sum(1)); rg = np.random.default_rng(SEED); idx = rg.integers(0, N, (NB, N)); a = nsum_.sum() / vsum.sum() * fbn; ab = nsum_[idx].sum(1) / vsum[idx].sum(1) * fbn; A.append((float(a), float(ab.std())))
        Y = interp_Y(Mt["k"], xc) / (1 + FS); Yb = np.array([interp_Y(r, xc) for r in bb]) / (1 + FS); sY = float(Yb.std() * sc); rows.append(dict(x=xc, Y=float(Y), s=sY, A=a, As=float(ab.std())))
    XS = XK[foot]["7"]; X1 = {}
    for x in (.7, 1., 1.2, 1.5):
        if x in XS:
            y_ = xY(X7, x); rg = np.random.default_rng(SEED); idx = rg.integers(0, 7, (NB, 7)); dr = rg.normal(0, 1, (NB, 7)); em = np.array([c_["rows"][x][4] / (c_["rows"][x][2] + c_["rows"][x][3]) if x in c_["rows"] else 0 for c_ in X7]); by = np.nanmean(np.take_along_axis(y_ + dr * em, idx, 1), 1); X1[x] = dict(Y=float(np.nanmean(y_)), s=float(np.nanstd(by)), N=int(np.isfinite(y_).sum()), Yb=float(np.nanmean(xY(X7, x) * 10 ** -.12)), Yh=float(np.nanmean(xY(X7, x, .7 / .672))))
    H1 = {}
    for x, q in ((1., HS[foot]["all"]), (1.18, HS[foot]["x1.18"]), (1.67, HS[foot]["x1.67"])):
        Mtt = q["Mt"] - (q.get("bias", 0)); H1[x] = dict(Y=Mtt / (1 + FS), s=q["Mts"] / (1 + FS), L=q.get("L"))
    P(f"[{foot}] KiDS, forward: " + "; ".join(f"x {r['x']}: Y {r['Y']:.2f} +- {r['s']:.2f}, A_F {r['A']:.2f} +- {r['As']:.2f}, Z {(r['Y'] - 1 / fbn) / r['s']:+.2f}" for r in rows)); P("   KiDS terciles, Y at x 0.7, 1.18, 1.67: " + "; ".join(f"T{t + 1} " + fmt(interp_Y(KID[f'{foot}|h0672|{FS}'][f'MT{t}']['k'], np.array(Xc)) / (1 + FS)) + " +- " + fmt(np.array([np.std([interp_Y(r, x) for r in KID[f'{foot}|h0672|{FS}'][f'MT{t}']['bb']]) for x in Xc]) / (1 + FS)) for t in range(3)))
    P("   X-COP HSE: " + "; ".join(f"x {x}: Y {v['Y']:.2f} +- {v['s']:.2f} (N {v['N']}), Z {(v['Y'] - 1 / fbn) / v['s']:+.2f}, HSE-0.12 {v['Yb']:.2f}, h 0.672 {v['Yh']:.2f}" for x, v in X1.items()))
    P("   HSC, mock bias off M: " + "; ".join(f"x {x}: Y {v['Y']:.2f} +- {v['s']:.2f}, Z {(v['Y'] - 1 / fbn) / v['s']:+.2f}" for x, v in H1.items()) + " (x > 1 is NFW SHAPE)")
    FBR[foot] = dict(KiDS=rows, XCOP=X1, HSC=H1)
    # power + implied
    Kn = KID[f"{foot}|h0672|{FS}"]; k1 = {"KiDS": float(Kn["all"]["k"][3]), "HSE": XS[1.]["k"], "HSC": HS[foot]["all"]["kc"]}; sk = float(np.polyfit(np.log10(ND5[1:4]), np.log10(np.maximum(Kn["all"]["k"][1:4], .1)), 1)[0]); Lnode = Kn["Mtot_Mg"]["k"] - Kn["all"]["k"]; Lk = lambda x: float(interp_Y(Lnode, x)); LX = {x: XS[x]["L"] for x in (.7, 1., 1.2, 1.5) if x in XS}; LH = {1.: HS[foot]["all"]["L"], 1.18: HS[foot]["x1.18"]["L"], 1.67: HS[foot]["x1.67"]["L"]}; Kf = (1 + FS) / fbn
    KF = dict(KiDS={x: dict(kF=Kf - Lk(x), k=float(interp_Y(Kn["all"]["k"], x)), L=Lk(x)) for x in (.7, 1., 1.18, 1.67)}, XCOP={x: dict(kF=Kf - LX[x], k=XS[x]["k"], s=XS[x]["s"], L=LX[x]) for x in LX}, HSC={x: dict(kF=Kf - LH[x], k=(HS[foot]["all"]["kc"] if x == 1. else HS[foot][f"x{x}"]["k"]), L=LH[x]) for x in LH}); FBR[foot]["k_F"] = KF
    for nm_, q in KF.items(): P(f"   Implied k_F per set, {nm_}: " + "; ".join(f"x {x}: k_F {v['kF']:.2f}, measured {v['k']:.2f} (law/gas {v['L']:.2f})" for x, v in q.items()))
    rows2 = []
    for set_, sY, x0, L0 in (("KiDS", rows[1]["s"], 1.18, Lk(1.18)), ("KiDS", rows[2]["s"], 1.67, Lk(1.67)), ("HSE", X1.get(1.2, X1[1.])["s"], 1.2, LX.get(1.2, LX[1.])), ("HSE", X1.get(1.5, X1[1.])["s"], 1.5, LX.get(1.5, LX[1.])), ("HSC", H1[1.]["s"], 1., LH[1.])):
        Yf = 1 / fbn; k0 = k1[set_]; rv = dict(a=1.2 * Yf, b=(k0 + L0) / (1 + FS), c=(k0 * x0 ** sk + L0) / (1 + FS)); pw = {n: float(norm.sf(3 - abs(v - Yf) / sY) + norm.cdf(-3 - abs(v - Yf) / sY)) for n, v in rv.items()}; rows2.append(dict(set=set_, x=x0, s=sY, frac=3 * sY / Yf, rivals=rv, power=pw)); P(f"   Power {set_} x {x0}: 3 sigma shift {100 * 3 * sY / Yf:.0f} % of 1/f_b; rival Y (a) {rv['a']:.2f} (b) const k {rv['b']:.2f} (c) power law s {sk:.2f} {rv['c']:.2f}; P(|Z| >= 3): " + ", ".join(f"{n} {v:.2f}" for n, v in pw.items()))
    FBR[foot]["power"] = rows2
    def lab(Y, s): z = (Y - 1 / fbn) / s; return "DISAGREES" if abs(z) >= 3 else ("CONSISTENT" if abs(z) < 2 and s / Y <= .15 else "UNDERPOWERED"), z
    L = {"KiDS 1-1.4": lab(rows[1]["Y"], rows[1]["s"]), "KiDS 1.4-2": lab(rows[2]["Y"], rows[2]["s"]), "HSC x 1": lab(H1[1.]["Y"], H1[1.]["s"]), "X-COP x 1": lab(X1[1.]["Y"], X1[1.]["s"])}
    if 1.2 in X1: L["X-COP x 1.2"] = lab(X1[1.2]["Y"], X1[1.2]["s"])
    FBR[foot]["labels"] = L; P("   LABELS: " + "; ".join(f"{k} {v[0]} ({v[1]:+.2f})" for k, v in L.items()) + "; per set, a rival over 0.8: " + ", ".join(f"{r['set']} x {r['x']} {any(v > .8 for v in r['power'].values())}" for r in rows2))
    for fsx in (.0615,):
        cc = Cell(foot, "h0672", fsx); y2 = fitnodes(cc, five(cc.G6), cc.n, jack=False); P(f"   f* 0.0615 row, KiDS Y at x 1.18, 1.67: {fmt(interp_Y(y2['k'], np.array([1.18, 1.67])) / (1 + fsx))}" if not MUT else "")
R["fb"] = FBR
# ------------------ checks
Gr = json.load(open(os.path.join(RB, "GM1_gas_tied_missing_mass", "gm1_results.json")))["ans"]
if MUT: pass
a = Gr["canonical"]["primary"]; xe = a["xeff"][:3]; k3g = a["k3"][:3]; ks = a["k3s"][:3]; Kc = KID[f"canonical|h0672|{FS}"]["all"]; mine = np.interp(np.log10(xe), np.log10(ND5), Kc["k"]); check("K2", np.all(np.abs(mine - k3g) <= np.hypot(ks, 0) ), f"forward vs GM1 at x_eff {np.round(xe, 2).tolist()}: mine {fmt(mine)}, GM1 {fmt(k3g)}, sigma {fmt(ks)}")
Y0 = KID[f"canonical|h0672|{FS}"]; e0 = PR.e; check("K1", True if MUT else float(np.nanmax(np.abs(PR.n - PR.V - PR.e))) == 0, "e = n - V read through, LM1's dump: trivially true of the construction; own-law signal against LM1's V is a separate reading, median ratio " + f"{np.median((B['Vl_canonical_h0672'] / np.where(PR.V != 0, PR.V, np.nan))[PR.W > 0]):.4f}, 99 % {np.nanpercentile((B['Vl_canonical_h0672'] / np.where(PR.V != 0, PR.V, np.nan))[PR.W > 0], 99):.3f} (the difference is C*)")
LMR = {.1: 8.5, .2: 8.0, .3: 6.7, .5: 5.2, .7: 3.9, 1.: 2.3}; dk = {x: abs(XK["canonical"]["7"][x]["med"] - v) for x, v in LMR.items()}; check("K4", max(dk.values()) <= .05, f"X-COP median vs LM1 row: max |d| {max(dk.values()):.3f}; printed precision 0.1. Per x {({k: round(v, 3) for k, v in dk.items()})}")
kw = hsc(ALL, "canonical")[0]; check("K6", abs(kw - 5.48) <= .3, f"HSC common aperture, raw, canonical {kw:.2f}; GM1 5.48")
# K3 injection
if not MUT:
    ktr = lambda x: 6 * np.minimum(np.maximum(x, .2), 3.5) ** -.6; hk = "h0672"; Vi = np.zeros((N, 8))
    for i in range(N):
        c0 = S_.chain[hk][i]; x = C.RG / PR.R5[i]; Vi[i], _ = S_.vector(i, hk, ktr(x) * c0["Mb"] / 1.034)
    Ai, bi = normal(PR.G6, Vi, PR.W, PR.mask); kk = wls(Ai, bi); dv = kk / ktr(NODES) - 1; check("K3a", np.all(np.abs(dv[1:5]) <= .02), f"injected 6 x^-0.6 through CU1's own log projector, nodes {fmt(NODES)}: recovered ratio - 1 {fmt(dv, 4)}. Node 0.2 and 3.5 are edges")
    Vj = np.zeros((N, 8))
    for i in range(N):
        c0 = S_.chain[hk][i]; x = C.RG / PR.R5[i]; Ml = S_.msrc("canonical", i, hk, 0); Mg = c0["Mb"] / 1.034; _, Sb, _ = C.project(Ml + 4 * np.minimum(x ** -.6, 3) * Mg, c0["off"]); fr = np.ones(8); g = X["den"][i, 1] > 0; tot = sum(Sb ** (p + 1) * X["m3to8"][i, 1][p] for p in range(6)); fr[g] = 1 + tot[g] / X["den"][i, 1][g]; P_, _, _ = C.project(ktr(x) * Mg, c0["off"]); Vj[i] = PR.W[i] * P_ * fr
    dv2 = wls(*normal(PR.G6, Vj, PR.W, PR.mask)) / ktr(NODES) - 1; P(f"K3a diagnosis, post-result: same injection with the basis's reduced-shear factor, so only hats and projector differ: ratio - 1 {fmt(dv2, 4)}. So the rest was the reduced-shear factor, a mass-level choice of about 3 %, inside each node's error")
    rg = np.random.default_rng(SEED); G5 = five(PR.G6); sW = np.sqrt(PR.W); Ai5, _ = normal(G5, Vi, PR.W, PR.mask); w5 = np.where(PR.mask, 1 / np.where(PR.W > 0, PR.W, 1), 0); dd = []
    for _ in range(100):
        Yn = Vi + rg.normal(0, 1, Vi.shape) * sW; bin_ = np.einsum("ijb,ib,ib->j", G5, Yn, w5); dd.append(np.linalg.solve(Ai5.sum(0), bin_))
    dd = np.array(dd); t0 = wls(*normal(G5, Vi, PR.W, PR.mask)); bs = (dd.mean(0) - t0) / dd.std(0); check("K3b", np.all(np.abs(bs) <= .5), f"noise only, 100 draws, bias in sigma {fmt(bs)}; shape noise sd {fmt(dd.std(0))} against boot {fmt(KID[f'canonical|h0672|{FS}']['all']['sb'])}")
R["checks"] = CHK
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if k not in ("bb",)}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.floating, np.integer, np.bool_)): return o.item()
    return o
R["kids"] = clean(KID); R["kterm"] = clean(KT); R["xcop"] = clean(XK); R["hsc"] = clean(HS); R["pointed"] = PT; R["sep"] = SEP
json.dump(clean(R), open(os.path.join(HERE, f"ks1_results{TAG}.json"), "w"), indent=0, sort_keys=True, default=float)
P(f"\nchecks {sum(o for _, o in CHK)}/{len(CHK)}: " + ", ".join(f"{n} {'pass' if o else 'FAIL'}" for n, o in CHK)); open(os.path.join(HERE, f"ks1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    bad = [n for n, o in CHK if n in ("K2", "K4") and o]; print("MUTATE K2, K4 must fail; passed:", bad); sys.exit(1)
