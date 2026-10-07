"""CFG377 -- KiDS-1000 isolated lenses vs CFG372's reservoir dip.  Criteria: FROZEN_CRITERIA.md (committed alone, d03819f06).

BARE = CFG100's v_law (copied as source from campaign_fresh_gravity/CFG100_kids_mass_rederivation/cfg100_lib.py, not imported).
RES  = BARE minus the projected ESD of a deficit M_ex spread as a 3D Gaussian of width R_c = 3/h Mpc, M_ex = max(M_d(r_e) - 5.364 M_gal, 0).
Run from anywhere:  nice python3 cfg377_run.py ;  CFG377_MUTATE=1 nice python3 cfg377_run.py  (M_ex x 100, separate outputs).
"""
import os, sys, json, math, time
import numpy as np
from math import erf
from scipy import stats
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
MUTATE = os.environ.get("CFG377_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
MEX_SCALE = 100.0 if MUTATE else 1.0
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, msg))
np.set_printoptions(linewidth=220, precision=4, suppress=False)
T0 = time.time()

# ============================================================ copied from cfg100_lib.py (source copy)
G_MPC = 4.30091727e-9            # Mpc (km/s)^2 / Msun
MPC_M = 3.0856775814913673e22
SI_ACC = 1e6 / MPC_M             # (km/s)^2/Mpc -> m/s^2
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0 = {k: v / SI_ACC for k, v in A0_SI.items()}
OM, H = 0.3153, 0.6736
H0 = 100 * H
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G_MPC)

def _h(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def _dh(y, e=1e-6):
    return (_h(y * (1 + e)) - _h(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(_dh(y)), 1.0, 5.0)
H_P = float(_h(Y_P))
LYG = np.linspace(-14, 14, 280001)
_YG = 10 ** LYG
_DH = np.maximum(_dh(_YG), 0.05 * H_P / (_YG + Y_P))
_HM = float(_h(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), LYG, _HM) / y

def one_plus_delta_ta(a, Om=OM, H0_=H0):
    OL = 1 - Om
    t_a = 2.0 / (3 * H0_ * math.sqrt(OL)) * math.asinh(math.sqrt(OL / Om) * a ** 1.5)
    L = OL * H0_ ** 2
    def tint(w):
        f = lambda p: 2 * math.sin(p) ** 2 / math.sqrt(2 * w - L * math.sin(p) ** 2 * (1 + math.sin(p) ** 2))
        return quad(f, 0, math.pi / 2, epsabs=1e-13, epsrel=1e-12)[0]
    wlo = L * (1 + 1e-5)
    w = brentq(lambda w: tint(w) - t_a, wlo, 1e3 * H0_ ** 2, xtol=1e-16 * H0_ ** 2, rtol=1e-13)
    return 2 * w * a ** 3 / (Om * H0_ ** 2)
_DTA = None
def dta(z):
    global _DTA
    if _DTA is None:
        zs = np.linspace(-0.05, 1.0, 43)
        lna = np.log(1 / (1 + zs))[::-1]
        vals = np.array([math.log(one_plus_delta_ta(1 / (1 + zz))) for zz in zs])[::-1]
        _DTA = CubicSpline(lna, vals)
    return math.exp(float(_DTA(-math.log1p(z))))
def r_ta_law(Mb, a0, z):
    a = 1 / (1 + z)
    rho = OM * RHOC0 / a ** 3 * dta(z)
    f = lambda lr: math.log(Mb * float(nu_mono(G_MPC * Mb / math.exp(2 * lr) / a0))) - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho)
    return math.exp(brentq(f, math.log(1e-5), math.log(1e3), xtol=1e-12))

def dsigma(R, r_edges, M_edges):
    R = np.atleast_1d(np.asarray(R, float))[:, None]
    r1 = r_edges[None, :-1]; r2 = r_edges[None, 1:]
    m = np.diff(M_edges)[None, :]; dr = np.diff(r_edges)[None, :]
    a1 = np.maximum(r1, R); a2 = np.maximum(r2, R)
    F = lambda r: np.sqrt(np.maximum(r * r - R * R, 0.0)) - R * np.arccos(np.minimum(R / r, 1.0))
    Ac = lambda r: np.arccos(np.minimum(R / r, 1.0))
    Mtot = M_edges[-1]
    Mcyl = Mtot - (m / dr * (F(a2) - F(a1))).sum(1)
    dMc = (m / dr * (Ac(a2) - Ac(a1))).sum(1)
    Rr = R[:, 0]
    return Mcyl / (math.pi * Rr ** 2) - dMc / (2 * math.pi * Rr)

GEDGE = np.logspace(math.log10(1e-15), math.log10(5e-12), 16)      # m/s^2
GEDGE_K = GEDGE / SI_ACC
_GL_X, _GL_W = np.polynomial.legendre.leggauss(6)
def _nodes():
    lo, hi = np.log(GEDGE_K[:-1]), np.log(GEDGE_K[1:])
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    g = np.exp(mid[:, None] + half[:, None] * _GL_X[None, :])
    w = half[:, None] * _GL_W[None, :]
    return g, w / g
GN, WN = _nodes()
def _finish(ds_fn, Mg):
    R = np.sqrt(G_MPC * Mg / GN)
    ds = ds_fn(R.ravel()).reshape(GN.shape) * 1e-12
    return (WN * ds).sum(1) / WN.sum(1)
# ============================================================ end of copy

HRC = 0.674; RC = 3.0 / HRC          # Mpc (CFG372)
FCOLD = 5.364                        # CFG372's local cold share
def ds_gauss(R, M, s=RC):            # Msun/Mpc^2, closed form, positive mass M
    R = np.asarray(R, float); q = np.exp(-R * R / (2 * s * s))
    return M * (1 - q) / (math.pi * R * R) - M / (2 * math.pi * s * s) * q
def frac_gauss(r, s=RC):
    x = np.asarray(r, float) / (math.sqrt(2) * s)
    return np.vectorize(erf)(x) - 2 * x * np.exp(-x * x) / math.sqrt(math.pi)

def law_profile(Mg, z, foot):
    a0 = A0[foot]
    re = 0.4 * r_ta_law(Mg, a0, z)
    r = np.geomspace(1e-4, re, 1500)
    Md = Mg * (nu_mono(G_MPC * Mg / r ** 2 / a0) - 1.0)
    Mex = max(float(Md[-1]) - FCOLD * Mg, 0.0)
    return r, Md, re, Mex

def vectors(Mg, z, foot, Rphys):
    """15-bin pair-averaged BARE and dip (RES - BARE at unit MEX_SCALE) vectors [Msun/pc^2], and the same at physical radii Rphys."""
    r, Md, re, Mex = law_profile(Mg, z, foot)
    bare = lambda R: dsigma(R, r, Md) + Mg / (math.pi * R ** 2)
    dip = lambda R: -ds_gauss(R, Mex)
    vb = _finish(bare, Mg); vd = _finish(dip, Mg)
    pb = bare(Rphys) * 1e-12; pd = dip(Rphys) * 1e-12
    return vb, vd, pb, pd, Mex, re
def tmpl_vec(Mg):                    # 2-halo nuisance shape, pair-averaged (R/1 Mpc)^-0.8
    return _finish(lambda R: R ** -0.8 * 1e12, Mg)

P("CFG377  MUTATE=%d (M_ex x %g)" % (MUTATE, MEX_SCALE))
P("R_c = 3/h = %.4f Mpc; cold share %.3f; a0 canonical %.4e / alt %.4e m/s^2 (never pooled)" % (RC, FCOLD, A0_SI["canonical"], A0_SI["alt"]))

# ============================================================ data
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float); logMs = lens["logM"].astype(float); typ = lens["typ"]
jk = np.load(os.path.join(DATA, "lr_esd_jackknife.npz")); patch = jk["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
iso = np.load(os.path.join(DATA, "cfg96_isoflags.npz")); f30 = iso["f30"].astype(bool)
assert np.allclose(pl["gbar_edges"], GEDGE)
nL = len(z)
P("lenses %d, f30 subset %d" % (nL, f30.sum()))

P("== C1 data sums")
mx = 0.0
for a, b in ((WG, jk["wgE"]), (WW, jk["W"])):
    for p in range(NPATCH):
        s = a[patch == p].sum(0); ref = b[p, 0] + b[p, 1]
        mx = max(mx, float(np.max(np.abs(s - ref) / np.maximum(np.abs(ref), 1e-300))))
check("C1 per-patch sums vs June file", mx <= 1e-9, "max rel dev %.2e" % mx)

def esd_full_loo(mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev
def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)

# ============================================================ groups and model tables
lmg = np.log10(Mgal)
key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
_, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
gi = gi.ravel()
GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=z) / cnt
NG = len(cnt); P("groups %d" % NG)

# B21 Fig-3 radii
B21 = os.path.join(DATA, "brouwer2021_rar")
b21 = [np.loadtxt(os.path.join(B21, "Fig-3_Lensing-rotation-curves_Massbin-%d.txt" % i)) for i in (1, 2, 3, 4)]
RB = b21[0][:, 0]
assert all(np.allclose(b[:, 0], RB) for b in b21)

TAB = {}
t = time.time()
for foot in ("canonical", "alt"):
    vb = np.zeros((NG, 15)); vd = np.zeros((NG, 15)); pb = np.zeros((NG, len(RB))); pd = np.zeros((NG, len(RB))); mex = np.zeros(NG)
    for g in range(NG):
        vb[g], vd[g], pb[g], pd[g], mex[g], _ = vectors(GM[g], GZ[g], foot, RB)
    TAB[foot] = dict(vb=vb, vd=vd * MEX_SCALE, pb=pb, pd=pd * MEX_SCALE, mex=mex)
    P("  table %-9s %.1fs; M_ex/M_gal median %.1f" % (foot, time.time() - t, float(np.median(mex / GM))))
TT = np.array([tmpl_vec(GM[g]) for g in range(NG)])

def pstack(tab, mask):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out
gcen = np.sqrt(GEDGE_K[:-1] * GEDGE_K[1:])
def mean_R(mask):
    Rik = np.sqrt(G_MPC * Mgal[mask][:, None] / gcen[None, :])
    return (WW[mask] * Rik).sum(0) / WW[mask].sum(0)

# ============================================================ C2, C3, C4
P("== C2 projector")
rr = np.geomspace(1e-3, 80, 30000)
Menc = 1e12 * frac_gauss(rr); Menc[0] = 0.0
Rt = np.array([0.3, 1.0, 3.0])
num = dsigma(Rt, rr, Menc); ana = ds_gauss(Rt, 1e12)
e2 = float(np.max(np.abs(num / ana - 1)))
pm = dsigma(Rt, np.array([1e-6, 1e-5]), np.array([1e11, 1e11])); e2b = float(np.max(np.abs(pm / (1e11 / (math.pi * Rt ** 2)) - 1)))
check("C2 Gaussian closed form vs shell projector; point mass", e2 < 1e-3 and e2b < 1e-12, "max rel %.2e; point mass %.1e" % (e2, e2b))

P("== C3 reproduction of CFG372 (ii) with its own recipe")
G372 = 4.30091e-9; MPC = 3.0857e22; MSUN = 1.989e30
def nu372(y): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-14))))
rho_m = 0.315 * 3 * (67.4 / 3.0857e19) ** 2 / (8 * math.pi * 6.674e-11) / MSUN * MPC ** 3
ref372 = {("canonical", 10.5): (-0.28, -6.62), ("canonical", 11.0): (-0.27, -6.45), ("alt", 10.5): (-0.28, -6.68), ("alt", 11.0): (-0.27, -6.54)}
ok3 = True; C3 = {}
for (foot, lm), (r1, r3) in ref372.items():
    Mb = 10 ** lm; a0c = A0_SI[foot] / 1e3 * MPC / 1e3
    r = np.geomspace(1e-3, 30, 4000); Mph = Mb * (nu372(G372 * Mb / r ** 2 / a0c) - 1.0)
    rta = r[np.argmin(np.abs((Mb + Mph) / (4 / 3 * math.pi * r ** 3) - 11.806 * rho_m))]; rcut = 0.4 * rta
    Mex = max(float(np.interp(rcut, r, Mph)) - FCOLD * Mb, 0.0)
    fr = [-Mex * float(frac_gauss(R)) / (Mb + float(np.interp(min(R, rcut), r, Mph))) * 100 for R in (1.0, 3.0)]
    # this lane's recipe (nu_mono, CFG100 r_ta at z = 0.2)
    rl, Md, re, Mexl = law_profile(Mb, 0.2, foot)
    fl = [-Mexl * float(frac_gauss(R)) / (Mb + float(np.interp(min(R, re), rl, Md))) * 100 for R in (0.1, 0.3, 1.0, 3.0)]
    good = round(fr[0], 2) == r1 and round(fr[1], 2) == r3
    ok3 &= good
    C3["%s|%.1f" % (foot, lm)] = dict(cfg372_recipe=fr, lane_recipe_r01_03_1_3=fl, lane_Mex=Mexl, lane_re=re)
    P("  %-9s 1e%.1f: CFG372 recipe 1 Mpc %+.2f%% 3 Mpc %+.2f%% (printed %+.2f / %+.2f); lane recipe (z=0.2, nu_mono): r_e %.2f Mpc, M_ex %.2e, "
      "0.1/0.3/1/3 Mpc %+.3f / %+.3f / %+.2f / %+.2f %%" % (foot, lm, fr[0], fr[1], r1, r3, re, Mexl, *fl))
check("C3 CFG372 numbers reproduce", ok3, "to displayed digits")

P("== C4 grouping")
rng = np.random.default_rng(377)
sub = rng.choice(nL, 2000, replace=False)
ex = np.array([vectors(Mgal[i], z[i], "canonical", RB)[1] for i in sub]) * MEX_SCALE
w = WW[sub]
mu_ex = (w * ex).sum(0) / w.sum(0)
mu_gr = (w * TAB["canonical"]["vd"][gi[sub]]).sum(0) / w.sum(0)
Rm_all = mean_R(np.ones(nL, bool))
dipb = Rm_all >= 1.0
e4 = float(np.max(np.abs(mu_ex - mu_gr)[dipb]) / np.max(np.abs(mu_ex))) if dipb.any() else float(np.max(np.abs(mu_ex - mu_gr)) / np.max(np.abs(mu_ex)))
check("C4 grouped vs exact dip (2000 lenses)", e4 < 0.02, "max rel %.2e" % e4)

# ============================================================ scoring
def score(d, C, h, mb, mr, t=None):
    Ci = np.linalg.inv(C)
    rb = d - mb; rr_ = d - mr; mu = mr - mb
    xb = float(h * rb @ Ci @ rb); xr = float(h * rr_ @ Ci @ rr_)
    lam = float(h * mu @ Ci @ mu)
    Ahat = float((mu @ Ci @ rb) / (mu @ Ci @ mu)); sA = 1 / math.sqrt(lam)
    out = dict(chi2_bare=xb, chi2_res=xr, dchi2=xr - xb, lam=lam, Ahat=Ahat, sigA=sA,
               power2=float(stats.norm.cdf(math.sqrt(lam) - 2) + stats.norm.cdf(-math.sqrt(lam) - 2)),
               power3=float(stats.norm.cdf(math.sqrt(lam) - 3) + stats.norm.cdf(-math.sqrt(lam) - 3)),
               s2=math.sqrt(lam / 4), s3=math.sqrt(lam / 9))
    if t is not None:
        def prof(r):
            return float(h * (r @ Ci @ r - (t @ Ci @ r) ** 2 / (t @ Ci @ t))), float((t @ Ci @ r) / (t @ Ci @ t))
        pb, Ab = prof(rb); pr, Ar = prof(rr_)
        out.update(chi2_bare_nuis=pb, chi2_res_nuis=pr, dchi2_nuis=pr - pb, A_nuis_bare=Ab, A_nuis_res=Ar)
    return out

RES = dict(mutate=MUTATE, mex_scale=MEX_SCALE, checks=CHK, C3=C3)
for sname, mask in (("primary", np.ones(nL, bool)), ("S1_f30", f30)):
    d, C = esd_full_loo(mask); h = hart(15); Rm = mean_R(mask)
    tm = pstack(TT, mask)
    P("== %s: %d lenses, Hartlap %.4f" % (sname, mask.sum(), h))
    P("  pair-weighted mean R [Mpc]:", np.round(Rm, 3))
    P("  ESD data [Msun/pc^2]       :", np.round(d, 3))
    P("  jackknife sigma            :", np.round(np.sqrt(np.diag(C)), 3))
    RES[sname] = dict(n=int(mask.sum()), meanR=Rm.tolist(), esd=d.tolist(), sig=np.sqrt(np.diag(C)).tolist(), n_dip_bins=int((Rm >= 1).sum()))
    for foot in ("canonical", "alt"):
        mb = pstack(TAB[foot]["vb"], mask); mu = pstack(TAB[foot]["vd"], mask); mr = mb + mu
        sc = score(d, C, h, mb, mr, tm)
        sc["model_bare"] = mb.tolist(); sc["dip"] = mu.tolist(); sc["dip_frac"] = (mu / mb).tolist()
        dipmask = Rm >= 1.0
        if dipmask.sum() >= 1:
            Cd = C[np.ix_(dipmask, dipmask)]; hd = hart(int(dipmask.sum()))
            sc["dipbins_only"] = {k: v for k, v in score(d[dipmask], Cd, hd, mb[dipmask], mr[dipmask]).items()}
        RES[sname][foot] = sc
        P("  [%s] BARE   :" % foot, np.round(mb, 3))
        P("  [%s] dip    :" % foot, np.round(mu, 4), " frac", np.round(mu / mb, 4))
        P("  [%s] chi2 BARE %.2f  RES %.2f  dchi2 %+.3f | lambda %.4f  A-hat %.2f +- %.2f | power 2sig %.3f 3sig %.3f | s2 %.3f s3 %.3f"
          % (foot, sc["chi2_bare"], sc["chi2_res"], sc["dchi2"], sc["lam"], sc["Ahat"], sc["sigA"], sc["power2"], sc["power3"], sc["s2"], sc["s3"]))
        P("  [%s] with 2-halo nuisance: chi2 BARE %.2f RES %.2f dchi2 %+.3f (A %.3g / %.3g)" % (foot, sc["chi2_bare_nuis"], sc["chi2_res_nuis"], sc["dchi2_nuis"], sc["A_nuis_bare"], sc["A_nuis_res"]))
        if "dipbins_only" in sc:
            s_ = sc["dipbins_only"]; P("  [%s] dip bins only (%d): dchi2 %+.3f lambda %.4f" % (foot, int(dipmask.sum()), s_["dchi2"], s_["lam"]))

# S2: B21 Fig-3
P("== S2 Brouwer+2021 Fig-3 (B21 covariance, m-bias applied, h70 units taken as is)")
cv = np.loadtxt(os.path.join(B21, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"))
mvals = np.unique(cv[:, 0]); rvals = np.unique(cv[:, 2])
nb, nr = len(mvals), len(rvals)
CB = np.zeros((nb * nr, nb * nr))
for row in cv:
    i = np.searchsorted(mvals, row[0]) * nr + np.searchsorted(rvals, row[2]); j = np.searchsorted(mvals, row[1]) * nr + np.searchsorted(rvals, row[3])
    CB[i, j] = row[4] / row[6]
dB = np.concatenate([b[:, 1] / b[:, 4] for b in b21])
assert np.allclose(rvals, np.sort(RB), rtol=1e-3)
edges = [8.5, 10.3, 10.6, 10.8, 11.0]
RES["S2_B21"] = dict(R=RB.tolist(), esd=dB.tolist(), sig=np.sqrt(np.diag(CB)).tolist())
for foot in ("canonical", "alt"):
    mb = []; mu = []
    for i in range(4):
        m = (logMs >= edges[i]) & (logMs < edges[i + 1])
        wg = np.bincount(gi[m], minlength=NG).astype(float)
        mb.append(wg @ TAB[foot]["pb"] / wg.sum()); mu.append(wg @ TAB[foot]["pd"] / wg.sum())
    mb = np.concatenate(mb); mu = np.concatenate(mu)
    sc = score(dB, CB, 1.0, mb, mb + mu)
    sc["dip_frac_outer"] = [(mu / mb)[i * nr + nr - 1] for i in range(4)]
    RES["S2_B21"][foot] = sc
    P("  [%s] chi2 BARE %.2f RES %.2f (/60) dchi2 %+.3f | lambda %.4f | power 2sig %.3f | dip frac at R=%.2f Mpc per mass bin %s"
      % (foot, sc["chi2_bare"], sc["chi2_res"], sc["dchi2"], sc["lam"], sc["power2"], RB[-1], np.round(sc["dip_frac_outer"], 4)))

# ============================================================ forecast numbers: fractional DeltaSigma dip at 1, 2, 3 Mpc
P("== fractional DeltaSigma dip (RES/BARE - 1) at z = 0.2")
FC = {}
for foot in ("canonical", "alt"):
    for lm in (10.5, 11.0):
        Mb = 10 ** lm; r, Md, re, Mex = law_profile(Mb, 0.2, foot)
        Rq = np.array([0.3, 1.0, 2.0, 3.0])
        b = dsigma(Rq, r, Md) + Mb / (math.pi * Rq ** 2); dd = -ds_gauss(Rq, Mex * MEX_SCALE)
        FC["%s|%.1f" % (foot, lm)] = (dd / b).tolist()
        P("  %-9s 1e%.1f: R 0.3/1/2/3 Mpc: %s ; single-radius fractional precision for 2sig / 3sig at 3 Mpc: %.4f / %.4f"
          % (foot, lm, np.round(dd / b, 4), abs(dd[-1] / b[-1]) / 2, abs(dd[-1] / b[-1]) / 3))
RES["dsigma_dip_frac_R_0p3_1_2_3"] = FC

# ============================================================ verdict
VER = {}
for foot in ("canonical", "alt"):
    p = RES["primary"][foot]; s1 = RES["S1_f30"][foot]
    if RES["primary"]["n_dip_bins"] == 0:
        v = "NOT TESTABLE"
    else:
        x = p["dchi2"]
        v = "DISFAVOURED" if x >= 4 else ("FAVOURED-OVER-BARE" if x <= -4 else "CONSISTENT")
        if v == "CONSISTENT" and p["lam"] < 1: v += " (uninformative: lambda < 1)"
        if v in ("DISFAVOURED", "FAVOURED-OVER-BARE"):
            sg = np.sign(x)
            rob = (abs(s1["dchi2"]) >= 4 and np.sign(s1["dchi2"]) == sg) and (abs(p["dchi2_nuis"]) >= 4 and np.sign(p["dchi2_nuis"]) == sg)
            v += " (ROBUST)" if rob else " (NOT ROBUST: 2-halo / isolation)"
    VER[foot] = v
    P("VERDICT [%s]: %s   (dchi2 %+.3f, lambda %.4f, power 2sig %.3f; errors must be multiplied by %.4f for an expected 2 sigma, %.4f for 3 sigma = %.3g / %.3g x the KiDS-1000 pair count)"
      % (foot, v, p["dchi2"], p["lam"], p["power2"], p["s2"], p["s3"], 1 / p["s2"] ** 2, 1 / p["s3"] ** 2))
RES["verdict"] = VER

if MUTATE:
    try:
        main = json.load(open(os.path.join(HERE, "cfg377_results.json")))
        dd = {f: abs(RES["primary"][f]["chi2_res"] - main["primary"][f]["chi2_res"]) for f in ("canonical", "alt")}
        check("MUTATE chi2_RES moves by > 4 (both footings)", min(dd.values()) > 4, "canonical %.2f alt %.2f" % (dd["canonical"], dd["alt"]))
    except FileNotFoundError:
        check("MUTATE chi2_RES moves by > 4 (both footings)", False, "main results file missing; run the main run first")

P("checks: %s" % CHK)
P("elapsed %.0fs" % (time.time() - T0))
json.dump(RES, open(os.path.join(HERE, "cfg377_results%s.json" % TAG), "w"), indent=1)
open(os.path.join(HERE, "cfg377_run%s.out" % TAG), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
