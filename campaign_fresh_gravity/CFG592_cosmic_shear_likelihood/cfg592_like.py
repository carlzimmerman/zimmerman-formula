#!/usr/bin/env python3
"""CFG592 (FROZEN_CRITERIA.md, commit a3a22a833): a real cosmic-shear likelihood (KiDS-1000 xi+-, DES Y3 xi+-) for
LCDM x HMcode-2020 BAHAMAS feedback and for the framework's R(k).

  nice -n 10 python3 cfg592_like.py                  -> cfg592_like.out, cfg592_results.json
  CFG592_MUTATE=1 nice -n 10 python3 cfg592_like.py  -> *_MUTATE.out / *_MUTATE.json (exit 1 = all teeth bite)

Data live outside git in ../_external_data/cfg592_work (relative to the repository's parent); see FETCH_LOG.md.
pyccl (control C2) is imported from the venv there if it is not importable directly.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, glob, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"   # 3 worker processes x 1 thread
import numpy as np
from scipy.optimize import minimize
from scipy.special import j0, jv
import astropy.io.fits as fits
import camb

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(CFG, "..")); WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg592_work"))
MUT = os.environ.get("CFG592_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()

# ------------------------------------------------------------------ cosmology (CFG590's Planck-like set)
H0, OMBH2, OMCH2, NS, S8FID = 67.36, 0.02237, 0.1200, 0.965, 0.811
h = H0 / 100; OM = (OMBH2 + OMCH2) / h ** 2; S8CONV = math.sqrt(OM / 0.3)
TGRID = [round(7.3 + 0.1 * i, 1) for i in range(11)]
SGRID = sorted(set([round(0.60 + 0.02 * i, 2) for i in range(17)] + [S8FID]))
PLANCK_S8 = (0.832, 0.013)   # recalled, PROVISIONAL
C1RHO = 0.0134

# ------------------------------------------------------------------ projection grids
ZG = np.linspace(0.005, 3.5, 350); AG = 1 / (1 + ZG)
LN = np.geomspace(1.0, 1.0e5, 150)                           # ell nodes for C_ell
pB = camb.CAMBparams(); pB.set_cosmology(H0=H0, ombh2=OMBH2, omch2=OMCH2, mnu=0.0, omk=0, num_massive_neutrinos=0)
pB.InitPower.set_params(ns=NS, As=2.1e-9)
pB.set_matter_power(redshifts=list(np.linspace(3.6, 0.0, 61)), kmax=100.0, nonlinear=True)
pB.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=7.8)
RB = camb.get_transfer_functions(pB)
CHI = np.array([RB.comoving_radial_distance(z) for z in ZG]) * h          # Mpc/h
HZ = np.array([RB.hubble_parameter(z) for z in ZG]) / H0                  # E(z)
DCHIDZ = 2997.92458 / HZ                                                  # Mpc/h per unit z
# linear growth D(z), D(0) = 1, flat LCDM (radiation neglected in the growth only)
def _D(a):
    aa = np.linspace(1e-4, a, 4000); E = np.sqrt(OM / aa ** 3 + 1 - OM)
    return 2.5 * OM * np.sqrt(OM / a ** 3 + 1 - OM) * np.trapz(1 / (aa * E) ** 3, aa)
DZ = np.array([_D(a) for a in AG]) / _D(1.0)
KK = (LN[:, None] + 0.5) / CHI[None, :]                                    # h/Mpc, [ell, z]
KMAXE = 1.0e4

# ------------------------------------------------------------------ P_HM(k, z; sigma8, T) grid (cache outside git)
CACHE = os.path.join(WORK, "cfg592_phm_grid.npz")
def build_grid():
    As0 = 2.1e-9
    RB.Params.InitPower.set_params(ns=NS, As=As0); RB.Params.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=7.8)
    RB.calc_power_spectra(RB.Params); s0 = RB.get_sigma8_0()
    G = np.zeros((len(SGRID), len(TGRID), len(LN), len(ZG))); s8chk = {}
    kc = np.clip(KK, 1e-4, KMAXE)
    for i, s8 in enumerate(SGRID):
        As = As0 * (s8 / s0) ** 2
        for j, T in enumerate(TGRID):
            RB.Params.InitPower.set_params(ns=NS, As=As)
            RB.Params.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=T)
            RB.calc_power_spectra(RB.Params)
            if j == 0: s8chk[s8] = float(RB.get_sigma8_0())
            pk = RB.get_matter_power_interpolator(nonlinear=True, hubble_units=True, k_hunit=True, extrap_kmax=KMAXE * 1.01)
            lp = np.array([np.log(pk.P(ZG[m], kc[:, m])) for m in range(len(ZG))]).T
            lp = np.where(KK > KMAXE, lp - 3.0 * np.log(KK / KMAXE), lp)    # k^-3 beyond 1e4 h/Mpc
            G[i, j] = lp
        P(f"    grid sigma8 node {s8:.3f}: CAMB sigma8 = {s8chk[s8]:.5f}")
    np.savez(CACHE, G=G, S=np.array(SGRID), T=np.array(TGRID), L=LN, Z=ZG, s8chk=np.array([s8chk[s] for s in SGRID]))
    return G, s8chk
if os.path.exists(CACHE):
    _c = np.load(CACHE)
    assert np.allclose(_c["S"], SGRID) and np.allclose(_c["T"], TGRID) and np.allclose(_c["L"], LN) and np.allclose(_c["Z"], ZG)
    LPG = _c["G"]; S8CHK = dict(zip(SGRID, _c["s8chk"].tolist()))
else:
    P("  building the P_HM grid (CAMB HMcode-2020 feedback) ...")
    LPG, S8CHK = build_grid()
SA = np.array(SGRID); TA = np.array(TGRID)
def logP(s8, T):
    i = int(np.clip(np.searchsorted(SA, s8) - 1, 0, len(SA) - 2)); wi = (s8 - SA[i]) / (SA[i + 1] - SA[i])
    j = int(np.clip(np.searchsorted(TA, T) - 1, 0, len(TA) - 2)); wj = (T - TA[j]) / (TA[j + 1] - TA[j])
    if abs(wi) < 1e-14 and abs(wj) < 1e-14: return LPG[i, j]
    return ((1 - wi) * (1 - wj) * LPG[i, j] + wi * (1 - wj) * LPG[i + 1, j] + (1 - wi) * wj * LPG[i, j + 1] + wi * wj * LPG[i + 1, j + 1])

# ------------------------------------------------------------------ framework R inputs (read only)
J556 = json.load(open(os.path.join(CFG, "CFG556_halo_model_matter_power", "cfg556_results.json")))
J557 = json.load(open(os.path.join(CFG, "CFG557_settling_catchment_derived", "cfg557_tests_results.json")))
J559 = json.load(open(os.path.join(CFG, "CFG559_kinetic_settled_profile", "cfg559_tests_results.json")))
JPH = json.load(open(os.path.join(CFG, "CFG590_framework_pk_vs_cosmic_shear", "cfg590_posthoc.json")))
KR = np.array(J556["k"])
def R_of(Rarr, k):
    lk = np.log(np.clip(k, KR[0], KR[-1])); r = np.interp(lk, np.log(KR), Rarr)
    return np.where(k < KR[0], 1.0, r)
SZ_N = np.array(sorted(float(z) for z in JPH["s_of_z"])); SZ_V = np.array([JPH["s_of_z"][k] for k in sorted(JPH["s_of_z"], key=float)])
S_OF_Z = np.interp(ZG, SZ_N, SZ_V)                                         # s(z > 1) = s(1.0)
def Rmat(Rarr, zscale=False):
    if Rarr is None: return np.ones_like(KK)
    r = R_of(np.asarray(Rarr, float), KK)
    return 1 + S_OF_Z[None, :] * (r - 1) if zscale else r
def models(foot):
    return {"PRIMARY": (J559["halo_model"][foot]["PRIMARY_kin"]["R"], False),
            "PRIMARY z-scaled": (J559["halo_model"][foot]["PRIMARY_kin"]["R"], True),
            "emergent edge": (J556["cases"][f"{foot}|census|emg"]["R"], False),
            "r200m scope": (J556["cases"][f"{foot}|census|cen|r200scope"]["R"], False),
            "CFG559 full_kin (reported)": (J559["halo_model"][foot]["VARIANT_full_kin"]["R"], False),
            "CFG557 TESTED (reported)": (J557["halo_model"][foot]["TESTED"]["R"], False),
            "CFG556 census|cen (reported)": (J556["cases"][f"{foot}|census|cen"]["R"], False)}
VERDICT_MODELS = ["PRIMARY", "PRIMARY z-scaled", "emergent edge", "r200m scope"]

# ------------------------------------------------------------------ Hankel matrices: ell nodes -> theta-bin-averaged xi+-
LF = np.geomspace(1.0, 1.0e5, 12000); DLF = np.gradient(LF)
TAPER = np.where(LF < 5e4, 1.0, 0.5 * (1 + np.cos(np.pi * (LF - 5e4) / 5e4)))
# linear interpolation in ln ell of ell^2 C_ell, as a matrix acting on C at the nodes
_idx = np.clip(np.searchsorted(np.log(LN), np.log(LF)) - 1, 0, len(LN) - 2)
_w = (np.log(LF) - np.log(LN)[_idx]) / (np.log(LN)[_idx + 1] - np.log(LN)[_idx])
MI = np.zeros((len(LF), len(LN)))
MI[np.arange(len(LF)), _idx] = (1 - _w) * LN[_idx] ** 2 / LF ** 2
MI[np.arange(len(LF)), _idx + 1] = _w * LN[_idx + 1] ** 2 / LF ** 2
def hankel(edges_arcmin, nsub=40):
    Hp, Hm = [], []
    for lo, hi in edges_arcmin:
        th = np.linspace(lo, hi, nsub) * math.pi / (180 * 60); wt = th / th.sum()
        x = LF[None, :] * th[:, None]
        Jp = (wt[:, None] * j0(x)).sum(0); Jm = (wt[:, None] * jv(4, x)).sum(0)
        base = LF * DLF / (2 * math.pi) * TAPER
        Hp.append((base * Jp) @ MI); Hm.append((base * Jm) @ MI)
    return np.array(Hp), np.array(Hm)

# ------------------------------------------------------------------ surveys
def load_kids():
    fn = glob.glob(os.path.join(WORK, "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0]
    F = fits.open(fn); cov = np.array(F["COVMAT"].data, float)
    xp, xm = F["xiP"].data, F["xiM"].data; nzt = F["NZ_SOURCE"].data
    zmid = np.array(nzt["Z_MID"], float); nz = [np.array(nzt[f"BIN{i+1}"], float) for i in range(5)]
    rows = [("+", int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"])) for r in xp] + \
           [("-", int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"])) for r in xm]
    e = np.geomspace(0.5, 300.0, 10); edges = list(zip(e[:-1], e[1:]))
    keep = np.array([(0.5 <= r[4] <= 300.0) if r[0] == "+" else (4.0 <= r[4] <= 300.0) for r in rows])
    angbins = sorted(set(r[3] for r in rows))
    som = np.loadtxt(os.path.join(WORK, "cfg", "SOM_cov_multiplied.asc"))
    return dict(name="KiDS", fn=os.path.basename(fn), cov=cov, rows=rows, keep=keep, zmid=zmid, nz=nz, nbin=5, edges=edges,
                angbin0=min(angbins), L=np.linalg.cholesky(som), mu_u=np.array([0.0, -0.181, -1.110, -1.395, 1.265]))
def load_des():
    fn = os.path.join(WORK, "2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits")
    F = fits.open(fn); H = F["COVMAT"].header
    assert H["NAME_0"].strip() == "xip" and H["NAME_1"].strip() == "xim" and int(H["STRT_1"]) == 200
    cov = np.array(F["COVMAT"].data[:400, :400], float)
    xp, xm = F["xip"].data, F["xim"].data; nzt = F["nz_source"].data
    zmid = np.array(nzt["Z_MID"], float); nz = [np.array(nzt[f"BIN{i+1}"], float) for i in range(4)]
    rows = [("+", int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"]), float(r["ANGLEMIN"]), float(r["ANGLEMAX"])) for r in xp] + \
           [("-", int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"]), float(r["ANGLEMIN"]), float(r["ANGLEMAX"])) for r in xm]
    cuts = {}
    for line in open(os.path.join(WORK, "cfg", "des-y3-scale-cuts.ini")):
        if line.startswith("angle_range_xi"):
            k, v = line.split("="); a, b = v.split()[:2]; cuts[k.strip()] = (float(a), float(b))
    def kp(r):
        s = "xip" if r[0] == "+" else "xim"; lo, hi = cuts[f"angle_range_{s}_{r[1]}_{r[2]}"]; return lo <= r[4] <= hi
    keep = np.array([kp(r) for r in rows])
    angs = {}
    for r in rows: angs[r[3]] = (r[6], r[7])
    a0 = min(angs); edges = [angs[i] for i in sorted(angs)]
    return dict(name="DES", fn=os.path.basename(fn), cov=cov, rows=rows, keep=keep, zmid=zmid, nz=nz, nbin=4, edges=edges, angbin0=a0)

def prepare(S):
    S["Hp"], S["Hm"] = hankel(S["edges"])
    S["d"] = np.array([r[5] for r in S["rows"]])[S["keep"]]
    C = S["cov"][np.ix_(S["keep"], S["keep"])]; S["Cinv"] = np.linalg.inv(C); S["Ndata"] = int(S["keep"].sum())
    nb = S["nbin"]; S["pairs"] = [(a, b) for a in range(1, nb + 1) for b in range(a, nb + 1)]
    pid = {p: i for i, p in enumerate(S["pairs"])}
    S["ip"] = np.array([pid[(min(r[1], r[2]), max(r[1], r[2]))] for r in S["rows"]])[S["keep"]]
    S["ia"] = np.array([r[3] - S["angbin0"] for r in S["rows"]])[S["keep"]]
    S["isp"] = np.array([r[0] == "+" for r in S["rows"]])[S["keep"]]
    S["b1"] = np.array([r[1] for r in S["rows"]])[S["keep"]] - 1; S["b2"] = np.array([r[2] for r in S["rows"]])[S["keep"]] - 1
    # fraction of n(z) beyond the projection grid
    S["nz_lost"] = [float(np.trapz(np.where(S["zmid"] > ZG[-1], n, 0), S["zmid"]) / np.trapz(n, S["zmid"])) for n in S["nz"]]
    return S

# lensing-efficiency matrix: q(chi_j) = pref_j * sum_j' K[j, j'] n(z_j') dz_j'
_wz = np.gradient(ZG)
KLEN = np.where(CHI[None, :] > CHI[:, None], (CHI[None, :] - CHI[:, None]) / CHI[None, :], 0.0) * _wz[None, :]
PREF = 1.5 * OM * (1 / 2997.92458) ** 2 * CHI / AG
WCHI = DCHIDZ * _wz / CHI ** 2                                             # d chi / chi^2 on the z grid
def kernels(S, dz):
    q, I = [], []
    for n, s in zip(S["nz"], dz):
        nn = np.interp(ZG - s, S["zmid"], n, left=0.0, right=0.0); nn = nn / np.trapz(nn, ZG)
        q.append(PREF * (KLEN @ nn)); I.append(nn / DCHIDZ)                   # I per unit chi
    return np.array(q), np.array(I)

def theory(S, par, s8, T, Rm, return_C=False):
    """par: dict with dz (array), A, eta, m (array), dc. Returns the cut theory vector."""
    q, I = kernels(S, par["dz"])
    Pm = np.exp(logP(s8, T)) * Rm                                           # [ell, z]
    F = -C1RHO * OM / DZ * (((1 + ZG) / 1.62) ** par.get("eta", 0.0))
    PW = Pm * WCHI[None, :]
    Ig = I * F[None, :]
    GG = np.einsum("lj,aj,bj->abl", PW, q, q); GI = np.einsum("lj,aj,bj->abl", PW, q, Ig); II = np.einsum("lj,aj,bj->abl", PW, Ig, Ig)
    A = par["A"]; Cab = GG + A * (GI + GI.transpose(1, 0, 2)) + A * A * II
    Cp = np.array([Cab[a - 1, b - 1] for a, b in S["pairs"]])               # [pair, ell]
    XP = Cp @ S["Hp"].T; XM = Cp @ S["Hm"].T                                 # [pair, theta]
    t = np.where(S["isp"], XP[S["ip"], S["ia"]], XM[S["ip"], S["ia"]])
    if "m" in par: t = t * (1 + par["m"][S["b1"]]) * (1 + par["m"][S["b2"]])
    if "dc" in par: t = t + np.where(S["isp"], par["dc"] ** 2, 0.0)
    return (t, Cp) if return_C else t

# ------------------------------------------------------------------ nuisance parameterisation and priors
DES_DZ_SIG = np.array([0.018, 0.015, 0.011, 0.017]); DES_M = np.array([-0.0063, -0.0198, -0.0241, -0.0369]); DES_M_SIG = np.array([0.0091, 0.0078, 0.0076, 0.0076])
KIDS_DC_SIG = 2.3e-4
def nuis_spec(S, widen):
    if S["name"] == "KiDS":
        x0 = np.r_[S["mu_u"], 0.5, 0.0]; lo = np.r_[S["mu_u"] - 5 * widen, -6.0, -1.2e-3 * widen]; hi = np.r_[S["mu_u"] + 5 * widen, 6.0, 1.2e-3 * widen]
        def unpack(x): return dict(dz=S["L"] @ x[:5], A=x[5], dc=x[6])
        def prior(x): return float(np.sum(((x[:5] - S["mu_u"]) / widen) ** 2) + (x[6] / (KIDS_DC_SIG * widen)) ** 2)
    else:
        x0 = np.r_[np.zeros(4), DES_M, 0.5, 0.0]; lo = np.r_[-0.1 * np.ones(4) * widen, DES_M - 0.1 * widen, -5.0, -5.0]; hi = np.r_[0.1 * np.ones(4) * widen, DES_M + 0.1 * widen, 5.0, 5.0]
        def unpack(x): return dict(dz=x[:4], m=x[4:8], A=x[8], eta=x[9])
        def prior(x): return float(np.sum((x[:4] / (DES_DZ_SIG * widen)) ** 2) + np.sum(((x[4:8] - DES_M) / (DES_M_SIG * widen)) ** 2))
    return x0, lo, hi, unpack, prior

def chi2_data(S, t):
    r = S["d"] - t; return float(r @ S["Cinv"] @ r)
def fit(S, Rm, s8_free=False, T_fixed=None, widen=1.0, s8_fixed=None, data=None, starts=None):
    """Minimise total chi2 = data chi2 + Gaussian priors over nuisances (+T unless fixed, +sigma8 if free)."""
    x0n, lo, hi, unpack, prior = nuis_spec(S, widen)
    d_save = S["d"]
    if data is not None: S["d"] = data
    s8c = S8FID if s8_fixed is None else s8_fixed
    def split(x):
        k = len(x0n); xn = x[:k]; i = k
        T = T_fixed if T_fixed is not None else x[i]; i += (T_fixed is None)
        s8 = x[i] if s8_free else s8c
        return xn, T, s8
    def f(x):
        xn, T, s8 = split(x)
        t = theory(S, unpack(xn), s8, T, Rm)
        return chi2_data(S, t) + prior(xn)
    best = None
    Tst = [7.4, 7.8, 8.2] if T_fixed is None else [None]
    S8st = [0.74, 0.81] if s8_free else [None]
    if starts is not None: inits = starts
    else:
        inits = []
        for Ts in Tst:
            for ss in S8st:
                inits.append(np.r_[x0n, [] if Ts is None else [Ts], [] if ss is None else [ss]])
    bounds = list(zip(lo, hi)) + ([] if T_fixed is not None else [(7.3, 8.3)]) + ([(0.60, 0.92)] if s8_free else [])
    for xi in inits:
        r = minimize(f, xi, method="L-BFGS-B", bounds=bounds, options=dict(maxiter=400, ftol=1e-11, gtol=1e-7))
        if best is None or r.fun < best.fun: best = r
    xn, T, s8 = split(best.x)
    t = theory(S, unpack(xn), s8, T, Rm); c2d = chi2_data(S, t)
    S["d"] = d_save
    pr = unpack(xn)
    return dict(chi2=float(best.fun), chi2_data=c2d, prior=float(best.fun - c2d), T=float(T), sigma8=float(s8), S8=float(s8 * S8CONV),
                A_IA=float(pr["A"]), dz=[float(v) for v in pr["dz"]], x=[float(v) for v in best.x],
                eta=float(pr.get("eta", 0.0)), m=[float(v) for v in pr["m"]] if "m" in pr else None, dc=float(pr.get("dc", 0.0)), t=t)
def s8_interval(S, Rm, best):
    """Profile Delta chi2 = 1 interval in S8 (sigma8 scanned, nuisances and T re-minimised, warm start)."""
    s0 = best["sigma8"]; grid = np.round(np.arange(max(0.605, s0 - 0.07), min(0.915, s0 + 0.07) + 1e-9, 0.01), 4)
    prof = []
    xs = best["x"][:-1]
    for s in grid:
        r = fit(S, Rm, s8_fixed=float(s), starts=[np.array(xs)]); prof.append(r["chi2"])
    prof = np.array(prof) - best["chi2"]
    def cross(side):
        g = grid[grid <= s0][::-1] if side < 0 else grid[grid >= s0]; p = prof[grid <= s0][::-1] if side < 0 else prof[grid >= s0]
        for i in range(len(g) - 1):
            if p[i] < 1 <= p[i + 1]: return float(g[i] + (1 - p[i]) * (g[i + 1] - g[i]) / (p[i + 1] - p[i]))
        return None
    lo, hi = cross(-1), cross(+1)
    return dict(S8_lo=None if lo is None else lo * S8CONV, S8_hi=None if hi is None else hi * S8CONV,
                profile={f"{s * S8CONV:.4f}": float(v) for s, v in zip(grid, prof)})

def klass(d_r1, robust):
    if d_r1 >= 9 and min([d_r1] + robust) >= 9: return "EXCLUDED"
    if d_r1 >= 4: return "TENSION"
    if d_r1 < 4 and max(robust) < 9: return "CONSISTENT"
    return "NOT DIAGNOSTIC"
SEV = {"EXCLUDED": 3, "TENSION": 2, "CONSISTENT": 1, "NOT DIAGNOSTIC": 0}

# ------------------------------------------------------------------ run
P("CFG592: real cosmic-shear likelihood (KiDS-1000 xi+-, DES Y3 xi+-), LCDM x HMcode-2020 feedback vs framework R(k)" + (" [MUTATE]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; flat a0; nu_mono; candidate B; cold energy MASS still required; not theory closed.")
P(f"CAMB {camb.__version__}; cosmology h {h}, wb {OMBH2}, wc {OMCH2}, ns {NS}, sigma8 {S8FID} (S8 {S8FID * S8CONV:.4f}), massless nu; T grid {TGRID[0]}-{TGRID[-1]}")
SURVEYS = {"KiDS": prepare(load_kids()), "DES": prepare(load_des())}
for n, S in SURVEYS.items():
    P(f"  {n}: {S['fn']}; N_data after published cuts = {S['Ndata']} (of {len(S['rows'])}); n(z) fraction beyond z = {ZG[-1]}: {max(S['nz_lost']):.2e}")
c3s8 = S8CHK[S8FID]
RS = {f: models(f) for f in ("canonical", "alt")}
c3r = max(abs(float(R_of(np.asarray(v[0], float), np.array([1e-3]))[0]) - 1) for f in RS for v in RS[f].values())
P(f"  C3 CAMB sigma8 at the fiducial node = {c3s8:.5f} ({'PASS' if abs(c3s8 - S8FID) < 1e-3 else 'FAIL'}); max |R(1e-3) - 1| = {c3r:.1e} ({'PASS' if c3r < 1e-3 else 'FAIL'})")
RESULT = dict(lane="CFG592", date="2026-10-10", criteria_commit="a3a22a833", mutate=MUT, camb=camb.__version__,
              cosmology=dict(h=h, ombh2=OMBH2, omch2=OMCH2, ns=NS, sigma8=S8FID, S8=S8FID * S8CONV, Omega_m=OM),
              surveys={n: dict(file=S["fn"], N_data=S["Ndata"], nz_lost=S["nz_lost"]) for n, S in SURVEYS.items()},
              controls=dict(C3_sigma8=c3s8, C3_R=c3r), lcdm={}, framework={}, verdicts={})
ONES = np.ones_like(KK)
def strip(r): return {k: v for k, v in r.items() if k != "t"}

# ---- MUTATE mode
if MUT:
    bite = {}
    for n, S in SURVEYS.items():
        lA = fit(S, ONES); fA = fit(S, Rmat(np.ones_like(KR)))
        lB = fit(S, ONES, s8_free=True); fB = fit(S, Rmat(np.ones_like(KR)), s8_free=True)
        d1 = max(abs(lA["chi2"] - fA["chi2"]), abs(lB["chi2"] - fB["chi2"])); dx = max(np.max(np.abs(np.array(lA["x"]) - np.array(fA["x"]))), np.max(np.abs(np.array(lB["x"]) - np.array(fB["x"]))))
        mu1 = d1 <= 1e-9 and dx <= 1e-9
        P(f"  MU1 {n}: R = 1 vs LCDM: |dchi2| = {d1:.2e}, max |dx| = {dx:.2e} -> {'bites' if mu1 else 'FAILS'}")
        # MU2: injected 20% small-scale excess
        g = np.clip(np.log(np.clip(KR, 1e-9, None) / 0.5) / np.log(2.0), 0, 1); Rinj = 1 + 0.2 * g
        mock = theory(S, nuis_spec(S, 1.0)[3](np.array(lA["x"][:len(nuis_spec(S, 1.0)[0])])), S8FID, lA["T"], Rmat(Rinj))
        lm = fit(S, ONES, data=mock)
        mu2 = lm["chi2"] >= 9
        P(f"  MU2 {n}: LCDM fit to mock with injected 20% excess (k >= 1): chi2_min = {lm['chi2']:.2f} (T {lm['T']:.2f}, A_IA {lm['A_IA']:.2f}) -> {'bites (detected)' if mu2 else 'FAILS (not detected)'}")
        fm = fit(S, Rmat(RS["canonical"]["PRIMARY"][0]), data=mock)
        mu3 = fm["chi2"] >= -1e-6
        P(f"  MU3 {n}: PRIMARY canonical fit to the same mock: chi2_min = {fm['chi2']:.3f} (>= 0) -> {'bites' if mu3 else 'FAILS'}")
        bite[n] = dict(MU1=bool(mu1), MU1_dchi2=float(d1), MU1_dx=float(dx), MU2=bool(mu2), MU2_chi2=lm["chi2"], MU2_fit=strip(lm), MU3=bool(mu3), MU3_chi2=fm["chi2"])
    RESULT["mutate_results"] = bite
    allb = all(v["MU1"] and v["MU2"] and v["MU3"] for v in bite.values())
    P(f"\nMUTATE: all teeth bite = {allb}   ({time.time() - T0:.0f} s)")
    json.dump(RESULT, open(os.path.join(HERE, f"cfg592_results{SUF}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg592_like{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if allb else 0)

# ---- C1 reference from the released KiDS xi+- chain
def kids_chain_s8():
    fn = glob.glob(os.path.join(WORK, "kids", "*", "chains_and_config_files", "main_chains_iterative_covariance", "xipm", "chain", "output_multinest_C.txt"))[0]
    hdr = open(fn).readline().lstrip("#").split()
    dat = np.loadtxt(fn); cols = [c.lower() for c in hdr]
    iS = cols.index("cosmological_parameters--s_8"); iw = cols.index("weight")
    s, w = dat[:, iS], dat[:, iw]; o = np.argsort(s); cw = np.cumsum(w[o]) / w.sum()
    q = lambda p: float(np.interp(p, cw, s[o]))
    return dict(median=q(0.5), lo=q(0.16), hi=q(0.84), mean=float(np.sum(s * w) / w.sum()))
KREF = kids_chain_s8()
S8REF = {"KiDS": KREF["median"], "DES": 0.772}
P(f"  C1 references: KiDS xi+- released chain S8 median {KREF['median']:.4f} (68%: {KREF['lo']:.4f}-{KREF['hi']:.4f}); DES 0.772 (recalled, PROVISIONAL)")
RESULT["controls"]["C1_reference"] = dict(KiDS_chain=KREF, DES_recalled=0.772, tol=0.04)

# ---- C2: pyccl cross-check of the projection
def c2_check(S):
    try:
        import pyccl as ccl
    except ImportError:
        sys.path.insert(0, glob.glob(os.path.join(WORK, "venv", "lib", "python*", "site-packages"))[0]); import pyccl as ccl
    cosmo = ccl.Cosmology(Omega_c=OMCH2 / h ** 2, Omega_b=OMBH2 / h ** 2, h=h, n_s=NS, sigma8=S8FID, m_nu=0.0, transfer_function="bbks")
    RB.Params.InitPower.set_params(ns=NS, As=2.1e-9); RB.Params.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=7.8)
    RB.calc_power_spectra(RB.Params); s0 = RB.get_sigma8_0()
    RB.Params.InitPower.set_params(ns=NS, As=2.1e-9 * (S8FID / s0) ** 2); RB.calc_power_spectra(RB.Params)
    pk = RB.get_matter_power_interpolator(nonlinear=True, hubble_units=True, k_hunit=True, extrap_kmax=KMAXE * 1.01)
    kh = np.geomspace(1e-4, KMAXE, 600); za = np.linspace(0.0, 3.5, 120)[::-1]; aa = 1 / (1 + za)
    pkarr = np.array([pk.P(z, kh) for z in za]) / h ** 3
    p2d = ccl.Pk2D(a_arr=aa, lk_arr=np.log(kh * h), pk_arr=np.log(pkarr), is_logp=True, extrap_order_lok=1, extrap_order_hik=2)
    x0n, _, _, unpack, _ = nuis_spec(S, 1.0); par = unpack(x0n); par["A"] = 0.5
    tr = []
    for n, s in zip(S["nz"], par["dz"]):
        nn = np.interp(ZG - s, S["zmid"], n, left=0.0, right=0.0)
        Fz = 0.5 * (((1 + ZG) / 1.62) ** par.get("eta", 0.0))
        tr.append(ccl.WeakLensingTracer(cosmo, dndz=(ZG, nn), ia_bias=(ZG, Fz)))
    ell = np.unique(np.geomspace(1, 1e5, 400).astype(int)).astype(float)
    th_sub = [np.linspace(lo, hi, 40) for lo, hi in S["edges"]]; thall = np.concatenate(th_sub) / 60.0
    XP, XM = [], []
    for a, b in S["pairs"]:
        cl = ccl.angular_cl(cosmo, tr[a - 1], tr[b - 1], ell, p_of_k_a=p2d)
        xp = ccl.correlation(cosmo, ell=ell, C_ell=cl, theta=thall, type="GG+", method="fftlog")
        xm = ccl.correlation(cosmo, ell=ell, C_ell=cl, theta=thall, type="GG-", method="fftlog")
        def bavg(x):
            out = []; i = 0
            for th in th_sub:
                w = th / th.sum(); out.append(float(np.sum(w * x[i:i + len(th)]))); i += len(th)
            return out
        XP.append(bavg(xp)); XM.append(bavg(xm))
    XP, XM = np.array(XP), np.array(XM)
    tc = np.where(S["isp"], XP[S["ip"], S["ia"]], XM[S["ip"], S["ia"]])
    if "m" in par: tc = tc * (1 + par["m"][S["b1"]]) * (1 + par["m"][S["b2"]])
    tm = theory(S, par, S8FID, 7.8, ONES)
    r = tm - tc; return float(r @ S["Cinv"] @ r), float(np.max(np.abs(r) / np.sqrt(np.diag(np.linalg.inv(S["Cinv"]))))), ccl.__version__
C2 = {}
for n, S in SURVEYS.items():
    c2, mx, ver = c2_check(S); C2[n] = dict(chi2_mine_vs_ccl=c2, max_abs_over_sigma=mx, pyccl=ver, pass_=c2 <= 1.0)
    P(f"  C2 {n}: chi2 distance (own projection vs pyccl {ver}, same P(k,z)) = {c2:.3f}, max |diff|/sigma = {mx:.3f} -> {'PASS' if c2 <= 1.0 else 'FAIL'}")
RESULT["controls"]["C2"] = C2

# ---- LCDM fits
LC = {}
for n, S in SURVEYS.items():
    P(f"\n=== {n}: LCDM (R = 1) ===")
    A = fit(S, ONES); B = fit(S, ONES, s8_free=True); B.update(s8_interval(S, ONES, B))
    rob = {"widen2": fit(S, ONES, widen=2.0)}
    for T in (7.3, 7.8, 8.3): rob[f"T{T}"] = fit(S, ONES, T_fixed=T)
    robB = {"widen2": fit(S, ONES, s8_free=True, widen=2.0)}
    for T in (7.3, 7.8, 8.3): robB[f"T{T}"] = fit(S, ONES, s8_free=True, T_fixed=T)
    c1 = abs(B["S8"] - S8REF[n]) <= 0.04
    tp = (PLANCK_S8[0] - B["S8"]) / math.sqrt(PLANCK_S8[1] ** 2 + (0.5 * ((B["S8_hi"] or B["S8"]) - (B["S8_lo"] or B["S8"]))) ** 2)
    P(f"  mode A (sigma8 0.811): chi2 {A['chi2']:.2f} (data {A['chi2_data']:.2f}, N {S['Ndata']}), T {A['T']:.2f}, A_IA {A['A_IA']:.2f}")
    P(f"  mode B (S8 free): chi2 {B['chi2']:.2f}, S8 {B['S8']:.4f} [{B['S8_lo']}, {B['S8_hi']}], T {B['T']:.2f}, A_IA {B['A_IA']:.2f}; S8-free improvement {A['chi2'] - B['chi2']:.2f}")
    P(f"  C1 S8 {B['S8']:.4f} vs reference {S8REF[n]:.4f} (|d| {abs(B['S8'] - S8REF[n]):.4f} <= 0.04): {'PASS' if c1 else 'FAIL'}; Planck T_P = {tp:+.2f}")
    LC[n] = dict(A=A, B=B, rob=rob, robB=robB, C1=c1, T_P=tp)
    RESULT["lcdm"][n] = dict(modeA=strip(A), modeB=strip(B), robust_A={k: strip(v) for k, v in rob.items()}, robust_B={k: strip(v) for k, v in robB.items()},
                             C1_pass=c1, S8_ref=S8REF[n], Planck_T=tp, chi2_per_N=A["chi2_data"] / S["Ndata"])
survey_ok = {n: (LC[n]["C1"] and C2[n]["pass_"]) for n in SURVEYS}

# ---- framework fits (4 worker processes, one per (footing, model) task)
def run_model(task):
    foot, mname = task; Rarr, zs = RS[foot][mname]
    Rm = Rmat(Rarr, zs); rep = mname in VERDICT_MODELS; lines = [f"\n--- {foot} | {mname} ---"]; out = {}
    for n, S in SURVEYS.items():
        A = fit(S, Rm); dA = A["chi2"] - LC[n]["A"]["chi2"]
        B = fit(S, Rm, s8_free=True); dB = B["chi2"] - LC[n]["B"]["chi2"]
        if rep: B.update(s8_interval(S, Rm, B))
        o = dict(modeA=strip(A), modeB=strip(B), dchi2_A=dA, dchi2_B=dB)
        Ts = (7.3, 7.8, 8.3) if rep else (7.3, 8.3)
        rA = [fit(S, Rm, widen=2.0)["chi2"] - LC[n]["rob"]["widen2"]["chi2"]] + [fit(S, Rm, T_fixed=T)["chi2"] - LC[n]["rob"][f"T{T}"]["chi2"] for T in Ts]
        if rep:
            rB = [fit(S, Rm, s8_free=True, widen=2.0)["chi2"] - LC[n]["robB"]["widen2"]["chi2"]] + [fit(S, Rm, s8_free=True, T_fixed=T)["chi2"] - LC[n]["robB"][f"T{T}"]["chi2"] for T in Ts]
        else:
            rB = [dB]
        cA = klass(dA, rA); cB = klass(dB, rB)
        if not survey_ok[n]: cA = cB = "NOT DIAGNOSTIC"
        sig = 0.5 * ((B.get("S8_hi") or B["S8"]) - (B.get("S8_lo") or B["S8"])) if rep else None
        tp = (PLANCK_S8[0] - B["S8"]) / math.sqrt(PLANCK_S8[1] ** 2 + sig ** 2) if rep else None
        pc = None if tp is None else ("PLANCK-CONSISTENT" if abs(tp) < 2 else "PLANCK-TENSION" if abs(tp) < 3 else "PLANCK-INCONSISTENT")
        o.update(robust_A=rA, robust_B=rB, robust_labels=["widen2"] + [f"T{T}" for T in Ts], class_A=cA, class_B=cB, Planck_T=tp, Planck_class=pc, dS8_vs_LCDM=B["S8"] - LC[n]["B"]["S8"])
        lines.append(f"  {n}: mode A chi2 {A['chi2']:.2f} (T {A['T']:.2f}, A_IA {A['A_IA']:.2f}) dchi2 {dA:+.2f}; robust {[round(x, 2) for x in rA]} -> {cA}")
        lines.append(f"  {n}: mode B S8 {B['S8']:.4f} [{B.get('S8_lo')}, {B.get('S8_hi')}] (LCDM {LC[n]['B']['S8']:.4f}; dS8 {o['dS8_vs_LCDM']:+.4f}); dchi2 {dB:+.2f} -> S8-free class {cB}; Planck T {tp if tp is None else round(tp, 2)} {pc or ''}")
        out[n] = o
    sevs = [out[n]["class_A"] for n in SURVEYS if survey_ok[n]]
    fv = max(sevs, key=lambda c: SEV[c]) if sevs else "NOT DIAGNOSTIC"
    sevsB = [out[n]["class_B"] for n in SURVEYS if survey_ok[n]]
    fvB = max(sevsB, key=lambda c: SEV[c]) if sevsB else "NOT DIAGNOSTIC"
    out["combined_dchi2_A"] = sum(out[n]["dchi2_A"] for n in SURVEYS); out["combined_dchi2_B"] = sum(out[n]["dchi2_B"] for n in SURVEYS)
    out["footing_class_A"] = fv; out["footing_class_B"] = fvB
    lines.append(f"  footing class (mode A): {fv}; S8-free: {fvB}; combined dchi2 (reported) A {out['combined_dchi2_A']:+.2f}, B {out['combined_dchi2_B']:+.2f}")
    return task, out, lines
import multiprocessing as mp
TASKS = [(f, m) for f in ("canonical", "alt") for m in RS[f]]
with mp.get_context("fork").Pool(3) as pool:
    RESS = pool.map(run_model, TASKS, chunksize=1)
for foot in ("canonical", "alt"):
    RESULT["framework"][foot] = {}; RESULT["verdicts"][foot] = {}
for (foot, mname), out, lines in RESS:
    for l in lines: P(l)
    RESULT["framework"][foot][mname] = out; RESULT["verdicts"][foot][mname] = dict(A=out["footing_class_A"], B=out["footing_class_B"])
for foot in ("canonical", "alt"):
    prim = RESULT["verdicts"][foot]["PRIMARY"]["A"]
    vs = [m for m in VERDICT_MODELS[1:] if RESULT["verdicts"][foot][m]["A"] != prim]
    RESULT["verdicts"][foot]["VARIANT_SENSITIVE"] = vs
    P(f"\n  {foot}: PRIMARY {prim}; VARIANT-SENSITIVE: {vs if vs else 'no'}")
RESULT["survey_ok"] = survey_ok
P(f"\ndone in {time.time() - T0:.0f} s")
json.dump(RESULT, open(os.path.join(HERE, f"cfg592_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg592_like{SUF}.out"), "w").write("\n".join(OUT) + "\n")
