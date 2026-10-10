#!/usr/bin/env python3
"""CFG592 PART B (ADDENDUM_2026-10-10.md, commit 65fa05a07): the FRAMEWORK-NATIVE cosmic-shear test.
The framework's own PM gravitating-field P(k, z) (CFG555 machinery caches) against its matched S0 PM run, both projected
onto the measured KiDS-1000 / DES Y3 xi+- with the published covariance and n(z); measurement nuisances only.
NO HMcode, NO BAHAMAS, NO halo-model mass function in the primary (feedback enters only as flagged context).

  nice -n 10 python3 cfg592_native.py                  -> cfg592_native.out, cfg592_native_results.json
  CFG592_MUTATE=1 nice -n 10 python3 cfg592_native.py  -> *_MUTATE.out / *_MUTATE.json (exit 1 = all teeth bite)

kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, glob, time, importlib.util
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.optimize import minimize
from scipy.special import j0, jv
from scipy.integrate import quad
import astropy.io.fits as fits

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(CFG, "..")); EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg592_work")
MUT = os.environ.get("CFG592_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
NPROC = 4
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()

# ------------------------------------------------------------------ PM constants and background (engine values, cfg424_pm.py L352 set)
h = 0.6736; om_b, om_c = 0.02237, 0.1200; Om = (om_b + om_c) / h ** 2; NS, SIG8 = 0.965, 0.811
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def T_eh(k):   # EH no-wiggle, copied from cfg424_pm.py (the engines' IC spectrum; k in 1/Mpc)
    OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_KG = np.geomspace(1e-5, 100, 40000); _PK = _KG ** NS * T_eh(_KG * h) ** 2
_W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_PK *= SIG8 ** 2 / (np.trapz(_PK * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))
def P_lin0(k): return np.exp(np.interp(np.log(np.maximum(k, 1e-5)), np.log(_KG), np.log(_PK)))
E_PM = lambda a: math.sqrt(Om / a ** 3 + 1 - Om)
def Dgrow(a):
    g = lambda x: quad(lambda u: 1.0 / (u * E_PM(u)) ** 3, 0, x)[0] * E_PM(x)
    return g(a) / g(1.0)

ZG = np.linspace(0.005, 3.5, 350); AG = 1 / (1 + ZG); _wz = np.gradient(ZG)
DZG = np.array([Dgrow(a) for a in AG])
def background(Om_b, w0=-1.0, wa=0.0):
    Ez = lambda z: math.sqrt(Om_b * (1 + z) ** 3 + (1 - Om_b) * (1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z)))
    chi = np.array([quad(lambda x: 1 / Ez(x), 0, z)[0] for z in ZG]) * 2997.92458
    dchidz = 2997.92458 / np.array([Ez(z) for z in ZG])
    return chi, dchidz
BG = {"PM": background(Om)}

# ------------------------------------------------------------------ DESI DR2 + CMB + DES-Y5 CPL chain (distance variant)
def desi_median():
    d = os.path.join(EXT, "desi_dr2_chains", "desy5"); fn1 = os.path.join(d, "chain.1.txt")
    hdr = open(fn1).readline().lstrip("#").split(); names = ("weight", "w", "wa", "omegam"); cols = [hdr.index(c) for c in names]
    xs = []
    for kk in range(1, 5):
        x = np.loadtxt(os.path.join(d, f"chain.{kk}.txt"), usecols=cols); xs.append(x[int(0.3 * len(x)):])
    x = np.vstack(xs); w = x[:, 0]
    def wmed(v):
        o = np.argsort(v); c = np.cumsum(w[o]) / w.sum(); return float(np.interp(0.5, c, v[o]))
    return dict(w0=wmed(x[:, 1]), wa=wmed(x[:, 2]), Om=wmed(x[:, 3]), n=int(len(x)))
DESI = desi_median()
BG["DESI"] = background(DESI["Om"], DESI["w0"], DESI["wa"])

# ------------------------------------------------------------------ ell / Hankel machinery (as cfg592_like.py)
LN = np.geomspace(1.0, 1.0e5, 150)
LF = np.geomspace(1.0, 1.0e5, 12000); DLF = np.gradient(LF)
TAPER = np.where(LF < 5e4, 1.0, 0.5 * (1 + np.cos(np.pi * (LF - 5e4) / 5e4)))
_idx = np.clip(np.searchsorted(np.log(LN), np.log(LF)) - 1, 0, len(LN) - 2)
_w = (np.log(LF) - np.log(LN)[_idx]) / (np.log(LN)[_idx + 1] - np.log(LN)[_idx])
MI = np.zeros((len(LF), len(LN)))
MI[np.arange(len(LF)), _idx] = (1 - _w) * LN[_idx] ** 2 / LF ** 2
MI[np.arange(len(LF)), _idx + 1] = _w * LN[_idx + 1] ** 2 / LF ** 2
def hankel(edges_arcmin, nsub=40):
    Hp, Hm, Ap, Am = [], [], [], []
    base = LF * DLF / (2 * math.pi) * TAPER
    for lo, hi in edges_arcmin:
        th = np.linspace(lo, hi, nsub) * math.pi / (180 * 60); wt = th / th.sum()
        x = LF[None, :] * th[:, None]
        Jp = (wt[:, None] * j0(x)).sum(0); Jm = (wt[:, None] * jv(4, x)).sum(0)
        Hp.append((base * Jp) @ MI); Hm.append((base * Jm) @ MI)
        Ap.append((base * np.abs(Jp)) @ MI); Am.append((base * np.abs(Jm)) @ MI)
    return np.array(Hp), np.array(Hm), np.array(Ap), np.array(Am)

# ------------------------------------------------------------------ surveys (published cuts, as cfg592_like.py)
def load_kids():
    fn = glob.glob(os.path.join(WORK, "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0]
    F = fits.open(fn); cov = np.array(F["COVMAT"].data, float); nzt = F["NZ_SOURCE"].data
    rows = [(s, int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"])) for s, ext in (("+", "xiP"), ("-", "xiM")) for r in F[ext].data]
    e = np.geomspace(0.5, 300.0, 10)
    keep = np.array([(0.5 <= r[4] <= 300.0) if r[0] == "+" else (4.0 <= r[4] <= 300.0) for r in rows])
    som = np.loadtxt(os.path.join(WORK, "cfg", "SOM_cov_multiplied.asc"))
    return dict(name="KiDS", cov=cov, rows=rows, pubkeep=keep, zmid=np.array(nzt["Z_MID"], float), nz=[np.array(nzt[f"BIN{i+1}"], float) for i in range(5)],
                nbin=5, edges=list(zip(e[:-1], e[1:])), angbin0=min(r[3] for r in rows), L=np.linalg.cholesky(som), mu_u=np.array([0.0, -0.181, -1.110, -1.395, 1.265]))
def load_des():
    fn = os.path.join(WORK, "2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits")
    F = fits.open(fn); cov = np.array(F["COVMAT"].data[:400, :400], float); nzt = F["nz_source"].data
    rows = [(s, int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"]), float(r["ANGLEMIN"]), float(r["ANGLEMAX"])) for s, ext in (("+", "xip"), ("-", "xim")) for r in F[ext].data]
    cuts = {}
    for line in open(os.path.join(WORK, "cfg", "des-y3-scale-cuts.ini")):
        if line.startswith("angle_range_xi"):
            k, v = line.split("="); a, b = v.split()[:2]; cuts[k.strip()] = (float(a), float(b))
    keep = np.array([cuts[f"angle_range_{'xip' if r[0] == '+' else 'xim'}_{r[1]}_{r[2]}"][0] <= r[4] <= cuts[f"angle_range_{'xip' if r[0] == '+' else 'xim'}_{r[1]}_{r[2]}"][1] for r in rows])
    angs = {r[3]: (r[6], r[7]) for r in rows}
    return dict(name="DES", cov=cov, rows=rows, pubkeep=keep, zmid=np.array(nzt["Z_MID"], float), nz=[np.array(nzt[f"BIN{i+1}"], float) for i in range(4)],
                nbin=4, edges=[angs[i] for i in sorted(angs)], angbin0=min(angs))
SURV = {"KiDS": load_kids(), "DES": load_des()}
for S in SURV.values():
    S["Hp"], S["Hm"], S["Ap"], S["Am"] = hankel(S["edges"])
    nb = S["nbin"]; S["pairs"] = [(a, b) for a in range(1, nb + 1) for b in range(a, nb + 1)]; pid = {p: i for i, p in enumerate(S["pairs"])}
    S["ip_all"] = np.array([pid[(min(r[1], r[2]), max(r[1], r[2]))] for r in S["rows"]]); S["ia_all"] = np.array([r[3] - S["angbin0"] for r in S["rows"]])
    S["isp_all"] = np.array([r[0] == "+" for r in S["rows"]]); S["b1_all"] = np.array([r[1] for r in S["rows"]]) - 1; S["b2_all"] = np.array([r[2] for r in S["rows"]]) - 1
    S["d_all"] = np.array([r[5] for r in S["rows"]])

C1RHO = 0.0134
def kernels(S, dz, bg):
    chi, dchidz = BG[bg]
    KLEN = np.where(chi[None, :] > chi[:, None], (chi[None, :] - chi[:, None]) / chi[None, :], 0.0) * _wz[None, :]
    pref = 1.5 * Om * (1 / 2997.92458) ** 2 * chi / AG
    q, I = [], []
    for n, s in zip(S["nz"], dz):
        nn = np.interp(ZG - s, S["zmid"], n, left=0.0, right=0.0); nn = nn / np.trapz(nn, ZG)
        q.append(pref * (KLEN @ nn)); I.append(nn / dchidz)
    return np.array(q), np.array(I), dchidz * _wz / chi ** 2
def C_ell(S, par, Pm, bg):
    q, I, wchi = kernels(S, par["dz"], bg)
    F = -C1RHO * Om / DZG * (((1 + ZG) / 1.62) ** par.get("eta", 0.0))
    PW = Pm * wchi[None, :]; Ig = I * F[None, :]
    GG = np.einsum("lj,aj,bj->abl", PW, q, q)
    A = par["A"]
    if A != 0.0:
        GI = np.einsum("lj,aj,bj->abl", PW, q, Ig); II = np.einsum("lj,aj,bj->abl", PW, Ig, Ig)
        Cab = GG + A * (GI + GI.transpose(1, 0, 2)) + A * A * II
    else: Cab = GG
    return np.array([Cab[a - 1, b - 1] for a, b in S["pairs"]])
def theory(S, D, par, Pm, bg):
    Cp = C_ell(S, par, Pm, bg); XP = Cp @ S["Hp"].T; XM = Cp @ S["Hm"].T
    t = np.where(D["isp"], XP[D["ip"], D["ia"]], XM[D["ip"], D["ia"]])
    if "m" in par: t = t * (1 + par["m"][D["b1"]]) * (1 + par["m"][D["b2"]])
    return t

DES_DZ_SIG = np.array([0.018, 0.015, 0.011, 0.017]); DES_M = np.array([-0.0063, -0.0198, -0.0241, -0.0369]); DES_M_SIG = np.array([0.0091, 0.0078, 0.0076, 0.0076])
def nuis_spec(S, widen, ia):
    if S["name"] == "KiDS":
        x0 = np.r_[S["mu_u"], 0.5 if ia else 0.0]; lo = np.r_[S["mu_u"] - 5 * widen, -6.0 if ia else 0.0]; hi = np.r_[S["mu_u"] + 5 * widen, 6.0 if ia else 0.0]
        unpack = lambda x: dict(dz=S["L"] @ x[:5], A=float(x[5]))
        prior = lambda x: float(np.sum(((x[:5] - S["mu_u"]) / widen) ** 2))
    else:
        x0 = np.r_[np.zeros(4), DES_M, 0.5 if ia else 0.0, 0.0]
        lo = np.r_[-0.1 * widen * np.ones(4), DES_M - 0.1 * widen, -5.0 if ia else 0.0, -5.0 if ia else 0.0]
        hi = np.r_[0.1 * widen * np.ones(4), DES_M + 0.1 * widen, 5.0 if ia else 0.0, 5.0 if ia else 0.0]
        unpack = lambda x: dict(dz=x[:4], m=x[4:8], A=float(x[8]), eta=float(x[9]))
        prior = lambda x: float(np.sum((x[:4] / (DES_DZ_SIG * widen)) ** 2) + np.sum(((x[4:8] - DES_M) / (DES_M_SIG * widen)) ** 2))
    return x0, lo, hi, unpack, prior
def fit(S, D, Pm, bg="PM", widen=1.0, ia=True, data=None):
    x0, lo, hi, unpack, prior = nuis_spec(S, widen, ia); d = D["d"] if data is None else data
    def f(x):
        r = d - theory(S, D, unpack(x), Pm, bg); return float(r @ D["Cinv"] @ r) + prior(x)
    starts = [x0] + ([np.r_[x0[:-2], -0.5, 0.0] if S["name"] == "DES" else np.r_[x0[:-1], -0.5]] if ia else [])
    best = None
    for xs in starts:
        bnd = [(a, b) if b > a else (a, a + 1e-300) for a, b in zip(lo, hi)]
        r = minimize(f, xs, method="L-BFGS-B", bounds=[(a, b) for a, b in zip(lo, hi)], options=dict(maxiter=400, ftol=1e-12, gtol=1e-8))
        if best is None or r.fun < best.fun: best = r
    par = unpack(best.x); t = theory(S, D, par, Pm, bg); r_ = d - t
    return dict(chi2=float(best.fun), chi2_data=float(r_ @ D["Cinv"] @ r_), A_IA=par["A"], dz=[float(v) for v in par["dz"]], x=[float(v) for v in best.x], t=t)

# ------------------------------------------------------------------ runs (CFG555 map, read only)
_sp = importlib.util.spec_from_file_location("cfg555c", os.path.join(CFG, "CFG555_growth_on_gravitating_field", "cfg555_compute.py"))
os.environ["CFG555_THREADS"] = "1"; C555 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C555)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
W555 = os.path.join(EXT, "cfg555_work"); PROF530 = os.path.join(EXT, "cfg530_work", "profiles"); R530 = os.path.join(EXT, "cfg530_work", "runs")
PRIMARY = ["425_R3_can_512", "439_A_alt_512", "439_B_DEcan_512", "460_can_512_s360", "518_DCcan_512",
           "530_LRcan_L200_N512", "530_LRalt_L200_N512", "530_LRcan_L100_N512", "530_LRalt_L100_N512"]
REPORTED = ["424_TAcan", "424_TAalt", "425_R1_can_s360", "425_R2_can_s361", "426_D1_DEcan", "426_D2_DEalt", "426_A1_alt_s360", "426_A2_alt_s361",
            "518_DCcan", "518_DCalt", "527_LRcan_L200", "527_LRalt_L200"] + \
           [f"530_LR{f}_L{L}_N{N}" for N in (128, 256) for L in (200, 100) for f in ("can", "alt")]
def snaps(js):
    s = json.load(open(js))["snap"]; return {z: (np.array(s[k]["k"]), np.array(s[k]["P"])) for z, k in ((0.0, "z0"), (0.5, "z0.5"), (1.0, "z1")) if k in s}
def load_run(name):
    if name.startswith("530_"):
        _, run, Ls, Ns = name.split("_"); L = int(Ls[1:]); N = int(Ns[1:]); foot = "canonical" if "can" in run else "alt"
        d = np.load(os.path.join(PROF530, f"N{N}", f"cfg526_{run}_L{L}.npz")); s0 = np.load(os.path.join(PROF530, f"N{N}", f"cfg526_S0_L{L}.npz"))
        k = np.array(d["kgrav"]); pgF = np.array(d["pgrav"]); ppF = np.array(d["ppart"]); k0 = np.array(s0["kgrav"]); ppS = np.array(s0["ppart"])
        jf = glob.glob(os.path.join(R530, f"{run}_L{L}_N{N}", "cfg527_RES_*.json")); js = glob.glob(os.path.join(R530, f"S0_L{L}_N{N}", "cfg527_S0_*.json"))
        sF = snaps(jf[0]) if jf else {}; sS = snaps(js[0]) if js else {}
        branch = "FLAT"; lane = "CFG530"
    else:
        spec, s0base = C555.RUNS[name]; d = json.load(open(os.path.join(W555, f"cfg555_{name}.json")))
        k = np.array(d["k"]); pgF = np.array(d["P_grav"]); ppF = np.array(d["P_part"]); N = spec["N"]; foot = spec["foot"]; branch = spec["branch"]
        L = float(json.load(open(spec["base"] + ".json"))["L"]); sF = snaps(spec["base"] + ".json"); sS = snaps(s0base + ".json")
        k0, ppS = sS[0.0]; lane = "CFG" + name.split("_")[0]
    assert np.allclose(k, k0, rtol=1e-6), name
    have_z = all(z in sF for z in (0.5, 1.0)) and all(z in sS for z in (0.5, 1.0))
    # node spectra (z = 0 from the CFG555 / CFG530 caches; z > 0 particle P from the run JSONs, or D^2 scaling for both if either lacks them)
    nodes = {}
    for z in (0.0, 0.5, 1.0):
        if z == 0.0: pF, pS = ppF, ppS
        elif have_z: pF, pS = sF[z][1], sS[z][1]
        else: g = (Dgrow(1 / (1 + z))) ** 2; pF, pS = ppF * g, ppS * g
        nodes[z] = (pF, pS)
    z0chk = float(np.max(np.abs(sF[0.0][1] / ppF - 1))) if 0.0 in sF else None
    return dict(name=name, lane=lane, N=int(N), L=float(L), foot=foot, branch=branch, k=k, B=pgF / ppF, nodes=nodes, have_z=have_z, z0chk=z0chk,
                k_lo=float(k[0]), k_hi=float(math.pi * N / (4 * L)))

def node_P(kb, pb, k_lo, k_hi, kq):
    """log-log interpolation inside [k_lo, k_hi]; EH matched below; own power law above."""
    m = kb <= k_hi * 1.0000001; kb_, pb_ = kb[m], pb[m]
    lp = np.interp(np.log(np.clip(kq, k_lo, k_hi)), np.log(kb_), np.log(pb_))
    sel = (kb_ >= k_hi / 2); s = np.polyfit(np.log(kb_[sel]), np.log(pb_[sel]), 1)[0]
    p_hi = np.exp(np.interp(np.log(k_hi), np.log(kb_), np.log(pb_)))
    low = P_lin0(kq) * (pb_[0] / P_lin0(np.array([kb_[0]]))[0])
    out = np.where(kq < k_lo, low, np.where(kq > k_hi, p_hi * (kq / k_hi) ** s, np.exp(lp)))
    return out
NODEZ = np.array([0.0, 0.5, 1.0])
def Pmat(run, which, boost="held", bg="PM", fb=None, inject=None):
    """[ell node, z] matrix of P(k = (ell + 1/2)/chi, z) for model 'F' or 'S0' (or 'F0' = framework path with source = 0 on S0 spectra)."""
    chi = BG[bg][0]; KK = (LN[:, None] + 0.5) / chi[None, :]
    lnP = []
    for z in NODEZ:
        pF, pS = run["nodes"][z]
        if which == "F":
            B = run["B"] if boost == "held" else 1 + (1 - z) * (run["B"] - 1)
            pb = pF * B
        elif which == "F0": pb = pS * 1.0     # framework code path, source = 0, S0 particles
        else: pb = pS
        lnP.append(np.log(node_P(run["k"], pb, run["k_lo"], run["k_hi"], KK)))
    lnP = np.array(lnP)                                   # [node, ell, z]
    Pm = np.empty_like(KK)
    for j, z in enumerate(ZG):
        if z <= 1.0:
            i = 0 if z <= 0.5 else 1; w = (z - NODEZ[i]) / 0.5
            Pm[:, j] = np.exp(lnP[i, :, j] + w * (lnP[i + 1, :, j] - lnP[i, :, j]))
        else:
            Pm[:, j] = np.exp(lnP[2, :, j]) * (DZG[j] / Dgrow(0.5)) ** 2
    if fb is not None: Pm = Pm * fb(KK, bg)
    if inject is not None: Pm = Pm * inject(KK)
    return Pm
D1 = Dgrow(0.5)

def support_mask(S, run, Pm0, bg="PM"):
    """fraction of each data point's absolute integrand inside [k_lo, k_hi] (S0 spectrum, nominal nuisances, no IA)."""
    x0, _, _, unpack, _ = nuis_spec(S, 1.0, False); par = unpack(x0)
    q, I, wchi = kernels(S, par["dz"], bg); chi = BG[bg][0]; KK = (LN[:, None] + 0.5) / chi[None, :]
    inside = (KK >= run["k_lo"]) & (KK <= run["k_hi"])
    PW = Pm0 * wchi[None, :]
    tot = np.einsum("lj,aj,bj->abl", PW, q, q); ins = np.einsum("lj,aj,bj->abl", PW * inside, q, q)
    Ct = np.array([tot[a - 1, b - 1] for a, b in S["pairs"]]); Ci = np.array([ins[a - 1, b - 1] for a, b in S["pairs"]])
    fp = (Ci @ S["Ap"].T) / (Ct @ S["Ap"].T); fm = (Ci @ S["Am"].T) / (Ct @ S["Am"].T)
    f = np.where(S["isp_all"], fp[S["ip_all"], S["ia_all"]], fm[S["ip_all"], S["ia_all"]])
    return f
def subset(S, keep):
    D = dict(keep=keep, d=S["d_all"][keep], ip=S["ip_all"][keep], ia=S["ia_all"][keep], isp=S["isp_all"][keep], b1=S["b1_all"][keep], b2=S["b2_all"][keep], N=int(keep.sum()))
    D["Cinv"] = np.linalg.inv(S["cov"][np.ix_(keep, keep)]) if D["N"] > 0 else None
    return D

# ------------------------------------------------------------------ feedback context (externally calibrated; CAMB HMcode-2020 ratio)
FB_T = (7.6, 7.8, 8.0)
def make_fb():
    import camb
    p = camb.CAMBparams(); p.set_cosmology(H0=100 * h, ombh2=om_b, omch2=om_c, mnu=0.0, omk=0, num_massive_neutrinos=0)
    p.InitPower.set_params(ns=NS, As=2.1e-9); p.set_matter_power(redshifts=list(np.linspace(3.6, 0, 61)), kmax=100.0, nonlinear=True)
    p.NonLinearModel.set_params(halofit_version="mead2020"); r = camb.get_transfer_functions(p); r.calc_power_spectra(r.Params)
    s0 = r.get_sigma8_0(); r.Params.InitPower.set_params(ns=NS, As=2.1e-9 * (SIG8 / s0) ** 2)
    kt = np.geomspace(1e-4, 1e4, 400); zt = np.linspace(0, 3.5, 36)
    def tab():
        r.calc_power_spectra(r.Params); pk = r.get_matter_power_interpolator(nonlinear=True, hubble_units=True, k_hunit=True, extrap_kmax=1.01e4)
        return np.array([pk.P(z, kt) for z in zt])
    r.Params.NonLinearModel.set_params(halofit_version="mead2020"); dmo = tab(); out = {}
    for T in FB_T:
        r.Params.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=T); out[T] = tab() / dmo
    from scipy.interpolate import RegularGridInterpolator
    fns = {T: RegularGridInterpolator((zt, np.log(kt)), out[T], bounds_error=False, fill_value=None) for T in FB_T}
    def fb_of(T):
        def f(KK, bg):
            Z = np.broadcast_to(ZG[None, :], KK.shape); return fns[T](np.stack([Z.ravel(), np.log(np.clip(KK, 1e-4, 1e4)).ravel()], -1)).reshape(KK.shape)
        return f
    return {T: fb_of(T) for T in FB_T}

def klass(d, robust, N_ok):
    if not N_ok: return "NOT DIAGNOSTIC"
    if d >= 9 and min([d] + robust) >= 9: return "EXCLUDED"
    if d >= 4: return "TENSION"
    if d < 4 and max(robust) < 9: return "CONSISTENT"
    return "NOT DIAGNOSTIC"
def strip(r): return {k: v for k, v in r.items() if k != "t"}
G_INJ = lambda KK: 1 + 0.2 * np.clip(np.log(np.clip(KK, 1e-9, None) / 0.5) / math.log(2.0), 0, 1)

def do_run(name):
    run = load_run(name); lines = [f"\n--- {name} ({run['lane']}, {run['foot']}, {run['branch']}, N {run['N']}, L {run['L']:.0f}; k {run['k_lo']:.3f}-{run['k_hi']:.3f} h/Mpc; z snapshots {'yes' if run['have_z'] else 'NO (D^2 scaling, both)'}) ---"]
    res = dict(lane=run["lane"], foot=run["foot"], branch=run["branch"], N=run["N"], L=run["L"], k_lo=run["k_lo"], k_hi=run["k_hi"], have_z_snapshots=run["have_z"],
               z0_cache_vs_json=run["z0chk"], B_at={str(kk): float(np.interp(math.log(kk), np.log(run["k"]), run["B"])) for kk in (0.3, 0.5, 1.0, 2.0) if kk <= run["k"][-1]}, surveys={})
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F"); PFf = Pmat(run, "F", boost="fade")
    PS0d = Pmat(run, "S0", bg="DESI"); PFd = Pmat(run, "F", bg="DESI")
    for sn, S in SURV.items():
        f = support_mask(S, run, PS0); keep = S["pubkeep"] & (f >= 0.9); D = subset(S, keep)
        Npub = int(S["pubkeep"].sum()); r = dict(N_kept=D["N"], N_published=Npub, frac_lost=1 - D["N"] / Npub)
        kept_th = {}
        for (s, a, b, ab, ang, *_), kp in zip(S["rows"], keep):
            if kp: kept_th.setdefault(f"xi{s}_{a}{b}", []).append(round(ang, 2))
        r["kept_theta"] = {k_: [min(v), max(v), len(v)] for k_, v in kept_th.items()}
        N_ok = D["N"] >= 10
        if not MUT and name in PRIMARY:
            # POST-HOC (not in the addendum; no verdict): looser support thresholds, IA marginalised
            ph = {}
            for thr in (0.8, 0.7):
                Dp = subset(S, S["pubkeep"] & (f >= thr))
                if Dp["N"] >= 10:
                    a_ = fit(S, Dp, PS0); b_ = fit(S, Dp, PF); c_ = fit(S, Dp, PFf)
                    ph[str(thr)] = dict(N=Dp["N"], chi2_S0=a_["chi2"], chi2_F=b_["chi2"], dchi2=b_["chi2"] - a_["chi2"], dchi2_fade=c_["chi2"] - a_["chi2"])
                else: ph[str(thr)] = dict(N=Dp["N"])
            r["posthoc_support"] = ph
            lines.append(f"  {sn}: POST-HOC support thresholds (no verdict): " + "; ".join(f"f>={t_}: N {v['N']}" + (f", dchi2 {v['dchi2']:+.2f} (fade {v['dchi2_fade']:+.2f})" if "dchi2" in v else "") for t_, v in ph.items()))
        if MUT:
            if D["N"] == 0: r["MUT"] = dict(N=0); res["surveys"][sn] = r; continue
            s0 = fit(S, D, PS0); f0 = fit(S, D, Pmat(run, "F0"))
            nz1 = abs(s0["chi2"] - f0["chi2"]) <= 1e-9 and np.max(np.abs(np.array(s0["x"]) - np.array(f0["x"]))) <= 1e-9
            mock = theory(S, D, nuis_spec(S, 1.0, True)[3](np.array(s0["x"])), Pmat(run, "S0", inject=G_INJ), "PM")
            fm = fit(S, D, PS0, data=mock); nz2 = fm["chi2"] >= 9
            # POST-HOC (not in the addendum; no verdict effect): the same 20% excess moved to the kept points' scales (ramp 0.15 -> 0.3 h/Mpc)
            G_PH = lambda KK: 1 + 0.2 * np.clip(np.log(np.clip(KK, 1e-9, None) / 0.15) / math.log(2.0), 0, 1)
            mock2 = theory(S, D, nuis_spec(S, 1.0, True)[3](np.array(s0["x"])), Pmat(run, "S0", inject=G_PH), "PM")
            fm2 = fit(S, D, PS0, data=mock2)
            lines.append(f"  {sn}: POST-HOC tooth (20% excess at k >= 0.3, no verdict effect): S0 chi2_min {fm2['chi2']:.2f}")
            r["MUT"] = dict(NZ1=bool(nz1), NZ1_dchi2=abs(s0["chi2"] - f0["chi2"]), NZ2=bool(nz2), NZ2_chi2=fm["chi2"], N=D["N"], posthoc_tooth_k03_chi2=fm2["chi2"])
            lines.append(f"  {sn}: N {D['N']}; NZ1 |dchi2| {abs(s0['chi2'] - f0['chi2']):.1e} -> {'bites' if nz1 else 'FAILS'}; NZ2 injected 20% excess: S0 chi2_min {fm['chi2']:.2f} -> {'bites (detected)' if nz2 else 'FAILS (not detected)'}")
            res["surveys"][sn] = r; continue
        if D["N"] == 0:
            r["class"] = r["class_noIA"] = "NOT DIAGNOSTIC"; lines.append(f"  {sn}: N_kept 0 of {Npub} -> NOT DIAGNOSTIC"); res["surveys"][sn] = r; continue
        out = {}
        for ia in (True, False):
            tag = "IA" if ia else "noIA"
            s0 = fit(S, D, PS0, ia=ia); fF = fit(S, D, PF, ia=ia)
            out[tag] = dict(S0=strip(s0), F=strip(fF), dchi2=fF["chi2"] - s0["chi2"])
        d = out["IA"]["dchi2"]
        rob = dict(widen2=fit(S, D, PF, widen=2.0)["chi2"] - fit(S, D, PS0, widen=2.0)["chi2"],
                   noIA=out["noIA"]["dchi2"],
                   fade=fit(S, D, PFf)["chi2"] - out["IA"]["S0"]["chi2"],
                   DESI=fit(S, D, PFd, bg="DESI")["chi2"] - fit(S, D, PS0d, bg="DESI")["chi2"])
        cls = klass(d, list(rob.values()), N_ok)
        rob_noIA = dict(widen2=fit(S, D, PF, widen=2.0, ia=False)["chi2"] - fit(S, D, PS0, widen=2.0, ia=False)["chi2"],
                        fade=fit(S, D, PFf, ia=False)["chi2"] - out["noIA"]["S0"]["chi2"],
                        DESI=fit(S, D, PFd, bg="DESI", ia=False)["chi2"] - fit(S, D, PS0d, bg="DESI", ia=False)["chi2"])
        cls_noIA = klass(out["noIA"]["dchi2"], list(rob_noIA.values()), N_ok)
        from scipy.stats import chi2 as CH
        pS = float(CH.sf(out["IA"]["S0"]["chi2_data"], D["N"])); pF = float(CH.sf(out["IA"]["F"]["chi2_data"], D["N"]))
        r.update(fits=out, robust=rob, robust_noIA=rob_noIA, dchi2=d, dchi2_noIA=out["noIA"]["dchi2"], **{"class": cls}, class_noIA=cls_noIA, p_S0=pS, p_F=pF)
        lines.append(f"  {sn}: N_kept {D['N']} of {Npub} published ({100 * r['frac_lost']:.0f}% lost); chi2 S0 {out['IA']['S0']['chi2']:.2f} (p {pS:.3f}), F {out['IA']['F']['chi2']:.2f} (p {pF:.3f}) "
                     f"-> dchi2 {d:+.2f} (A_IA S0 {out['IA']['S0']['A_IA']:.2f}, F {out['IA']['F']['A_IA']:.2f}); robust {({k_: round(v, 2) for k_, v in rob.items()})} -> {cls}")
        lines.append(f"  {sn}: no IA: S0 {out['noIA']['S0']['chi2']:.2f}, F {out['noIA']['F']['chi2']:.2f} -> dchi2 {out['noIA']['dchi2']:+.2f}; robust {({k_: round(v, 2) for k_, v in rob_noIA.items()})} -> {cls_noIA}")
        res["surveys"][sn] = r
    return name, res, lines

# ------------------------------------------------------------------ run
P("CFG592 PART B: FRAMEWORK-NATIVE cosmic-shear test (own PM gravitating-field P(k,z) vs matched S0 PM; no HMcode / BAHAMAS / mass function)" + (" [MUTATE]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; flat a0 (FLAT) and a0 tracking DE (DE runs); nu_mono; candidate B; cold energy MASS still required; not theory closed.")
P(f"PM background: flat w = -1, Om {Om:.5f} (h {h}, wb {om_b}, wc {om_c}); DESI distance variant (desy5 chain median, n = {DESI['n']}): w0 {DESI['w0']:.3f}, wa {DESI['wa']:.3f}, Om {DESI['Om']:.4f}")
RESULT = dict(lane="CFG592 PART B", date="2026-10-10", addendum_commit="65fa05a07", mutate=MUT, background=dict(PM=dict(Om=Om, w0=-1, wa=0), DESI=DESI), runs={})
import multiprocessing as mp
names = PRIMARY + ([] if MUT else REPORTED)
with mp.get_context("fork").Pool(NPROC) as pool:
    RR = pool.map(do_run, names, chunksize=1)
for name, res, lines in RR:
    for l in lines: P(l)
    res["primary_set"] = name in PRIMARY; RESULT["runs"][name] = res
if MUT:
    allb = all(s["MUT"].get("NZ1", True) for r in RESULT["runs"].values() for s in r["surveys"].values())
    nz2 = {n: {sn: s["MUT"].get("NZ2") for sn, s in r["surveys"].items()} for n, r in RESULT["runs"].items()}
    RESULT["NZ1_all_bite"] = allb; RESULT["NZ2"] = nz2
    nz2_any = all(any(v for v in d.values() if v is not None) for d in nz2.values())
    P(f"\nMUTATE: NZ1 (source = 0 reproduces S0 exactly) all bite = {allb}; NZ2 per run x survey = {nz2}")
    P(f"  NZ2 detected in at least one survey for every PRIMARY run: {nz2_any}   ({time.time() - T0:.0f} s)")
    json.dump(RESULT, open(os.path.join(HERE, f"cfg592_native_results{SUF}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg592_native{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if (allb and nz2_any) else 0)

# NZ2 status from the MUTATE JSON (if present) -> NOT DIAGNOSTIC where the tooth failed
mfn = os.path.join(HERE, "cfg592_native_results_MUTATE.json")
NZ2 = json.load(open(mfn))["NZ2"] if os.path.exists(mfn) else {}
for n, r in RESULT["runs"].items():
    for sn, s in r["surveys"].items():
        if NZ2.get(n, {}).get(sn) is False:
            s["class"] = s["class_noIA"] = "NOT DIAGNOSTIC"; s["NZ2_failed"] = True
# feedback context (externally calibrated; no verdict), PRIMARY runs, IA marginalised
P("\nFeedback context (HMcode-2020 BAHAMAS ratio, EXTERNALLY CALIBRATED, T fixed, not fitted; no verdict):")
FB = make_fb()
def fb_run(name):
    run = load_run(name); out = {}
    for sn, S in SURV.items():
        f = support_mask(S, run, Pmat(run, "S0")); keep = S["pubkeep"] & (f >= 0.9); D = subset(S, keep)
        if D["N"] < 10: continue
        out[sn] = {}
        for T in FB_T:
            s0 = fit(S, D, Pmat(run, "S0", fb=FB[T])); fF = fit(S, D, Pmat(run, "F", fb=FB[T]))
            out[sn][str(T)] = dict(chi2_S0=s0["chi2"], chi2_F=fF["chi2"], dchi2=fF["chi2"] - s0["chi2"])
    return name, out
with mp.get_context("fork").Pool(NPROC) as pool:
    FBR = pool.map(fb_run, PRIMARY, chunksize=1)
for name, out in FBR:
    RESULT["runs"][name]["feedback_context"] = out
    for sn, v in out.items():
        P(f"  {name} {sn}: " + "; ".join(f"T {T}: S0 {x['chi2_S0']:.1f}, F {x['chi2_F']:.1f}, dchi2 {x['dchi2']:+.2f}" for T, x in v.items()))
# footing summaries (PRIMARY set)
SUM = {}
for foot in ("canonical", "alt"):
    SUM[foot] = {}
    for sn in SURV:
        for key in ("class", "class_noIA"):
            cl = {n: RESULT["runs"][n]["surveys"][sn][key] for n in PRIMARY if RESULT["runs"][n]["foot"] == foot}
            v = set(cl.values())
            SUM[foot][f"{sn}|{key}"] = dict(summary="EXCLUDED" if v == {"EXCLUDED"} else "CONSISTENT" if v == {"CONSISTENT"} else "NOT DIAGNOSTIC (every run)" if v == {"NOT DIAGNOSTIC"} else "MIXED", runs=cl)
            P(f"  footing {foot} {sn} [{key}]: {SUM[foot][f'{sn}|{key}']['summary']}  {cl}")
RESULT["footing_summary"] = SUM
P(f"\ndone in {time.time() - T0:.0f} s")
json.dump(RESULT, open(os.path.join(HERE, f"cfg592_native_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg592_native{SUF}.out"), "w").write("\n".join(OUT) + "\n")
