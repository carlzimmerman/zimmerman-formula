
import os, sys, io, csv, json, math, hashlib, time
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gammainc

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
MODE = "MUTATE" if MUTATE else "main"
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/"
LENS_F = DATA + "slacs_auger2009_lenses.tsv"
ATL_F = DATA + "atlas3d_fj_table.tsv"
T0 = time.time()

FAILS = []      # load-bearing failures (controls, headline)
REPRO = []      # reproduction lines (reported)
def check(name, ok, detail="", kind="control"):
    tag = "PASS" if ok else "FAIL"
    print(f"{tag} [{kind}] {name}" + (("  " + detail) if detail else ""), flush=True)
    if not ok and kind in ("control", "headline"):
        FAILS.append(name)
def repro(name, mine, target, tol3, tolres, unit=""):
    d = mine - target
    v = "REPRODUCED-3dp" if abs(d) <= tol3 else ("REPRODUCED-within-resolution" if abs(d) <= tolres else "NOT-REPRODUCED")
    REPRO.append((name, mine, target, d, v))
    print(f"  {v:28s} {name}: mine {mine:+.4f}  target {target:+.4f}  diff {d:+.4f}{unit}", flush=True)

frozen = open(os.path.join(HERE, "CFG87_FROZEN.txt")).read().strip()
check("FROZEN docstring == CFG87_FROZEN.txt", frozen == (__doc__ or "").strip(),
      "sha256 " + hashlib.sha256(frozen.encode()).hexdigest()[:16], kind="control")
print("MODE", MODE, flush=True)

# ============================================================== constants
G_SI, c_SI, kpc, Msun = 6.674e-11, 2.99792458e8, 3.0857e19, 1.989e30
ARCSEC = 1 / 206264.806
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
C_KMS = 299792.458
G = 4.30091e-6                      # kpc (km/s)^2 / Msun (LCDM side)
FB = 0.02237 / (0.02237 + 0.1200)
H_HALO = 0.674
H0_HALO = 67.4 / 1000.0
RHOC0 = 3 * H0_HALO**2 / (8 * np.pi * G)
H_LENS = 0.7
OM, OL = 0.3, 0.7
SIGMA_FLOOR = 0.10
NB = 2000
QUAL_MIN = 1

# ============================================================== data
def load_lenses():
    lines = [l for l in open(LENS_F, encoding="latin-1") if not l.startswith("#")][1:]
    rows = list(csv.reader(io.StringIO("".join(lines)), delimiter="\t"))
    hdr = rows[0]
    data = [r for r in rows[3:] if len(r) == len(hdr)]
    ix = {h: i for i, h in enumerate(hdr)}
    def f(r, c):
        try: return float(r[ix[c]])
        except Exception: return float("nan")
    out, out86 = [], []
    for r in data:
        d = dict(name=r[ix["SDSS"]].strip(), zl=f(r, "zlens"), zs=f(r, "zsrc"), sig=f(r, "sigma"), RE=f(r, "RE"),
                 lME=f(r, "Mass"), Fs=f(r, "Fs"), lMs=f(r, "logMs"), lMc=f(r, "logMc"), ReV=f(r, "Re(V)"), ReI=f(r, "Re(I)"))
        need = ["zl", "zs", "sig", "RE", "lME", "Fs", "lMs"]
        if all(np.isfinite(d[c]) for c in need):
            out86.append(d["name"])
            if np.isfinite(d["ReV"]) or np.isfinite(d["ReI"]):
                out.append(d)
    return len(data), out, out86

def load_atlas():
    rows = [l.rstrip("\n").split("\t") for l in open(ATL_F) if not l.startswith("#")]
    hdr = rows[0]
    ix = {h: i for i, h in enumerate(hdr)}
    out = []
    for r in rows[1:]:
        try:
            d = {c: float(r[ix[c]]) for c in ["logsig_e", "logML_JAM", "logL", "logML_Salp", "logr12", "Dist_Mpc"]}
            d["qual"] = int(r[ix["qual"]]); d["name"] = r[ix["name"]]
            out.append(d)
        except ValueError:
            continue
    return len(rows) - 1, out

n85, LENS, names86 = load_lenses()
_, ATL = load_atlas()
check("C0 counts: 85 rows -> 70 lenses (my rule)", (n85, len(LENS)) == (85, 70), f"{n85},{len(LENS)}")
check("C0 my 70-lens set == CFG86 rule's set", sorted(d["name"] for d in LENS) == sorted(names86), f"{len(names86)}")
check("C0 counts: 258 ATLAS usable", len(ATL) == 258, str(len(ATL)))
CAL = [a for a in ATL if a["qual"] >= QUAL_MIN]
check("C0 counts: 187 Q>=1", len(CAL) == 187, str(len(CAL)))
nboth = sum(1 for d in LENS if np.isfinite(d["ReV"]) and np.isfinite(d["ReI"]))
print(f"  lenses with both Re(V) and Re(I): {nboth}/70", flush=True)
check("C0 Re(V),Re(I) both finite for >=60 of 70 (reported)", nboth >= 60, str(nboth), kind="reported")

def Ez(z): return math.sqrt(OM * (1 + z)**3 + OL)
def comoving_kpc(z1, z2):
    dh = C_KMS / (100 * H_LENS) * 1000.0
    return dh * quad(lambda z: 1.0 / Ez(z), z1, z2, epsabs=1e-13, epsrel=1e-13)[0]
def geom(zl, zs, RE):
    Dl = comoving_kpc(0, zl) / (1 + zl); Ds = comoving_kpc(0, zs) / (1 + zs); Dls = comoving_kpc(zl, zs) / (1 + zs)
    Sc = C_KMS**2 / (4 * np.pi * G) * Ds / (Dl * Dls)
    return Dl, np.pi * RE**2 * Sc

nL = len(LENS)
L_z = np.array([d["zl"] for d in LENS]); L_R = np.array([d["RE"] for d in LENS])
L_DA = np.zeros(nL); L_ME = np.zeros(nL)
for i, d in enumerate(LENS):
    L_DA[i], L_ME[i] = geom(d["zl"], d["zs"], d["RE"])
L_MS = 10**np.array([d["lMs"] for d in LENS])
L_FS = np.array([d["Fs"] for d in LENS])
L_MC = 10**np.array([d["lMc"] for d in LENS])
L_sig = np.array([d["sig"] for d in LENS]); L_x = np.log10(L_sig) - 2.3
dME = np.abs(np.log10(L_ME) - np.array([d["lME"] for d in LENS]))
check("C0 M_E vs tabulated Mass <=0.01 dex", dME.max() <= 0.01, f"max {dME.max():.4f} median {np.median(dME):.4f}")
# effective radii in kpc, both bands, missing band replaced by the other
def re_kpc(band):
    out = np.zeros(nL)
    for i, d in enumerate(LENS):
        a = d["Re" + band]
        if not np.isfinite(a): a = d["Re" + ("I" if band == "V" else "V")]
        out[i] = a * ARCSEC * L_DA[i]
    return out
L_RE = {"V": re_kpc("V"), "I": re_kpc("I")}
if MUTATE:      # Einstein masses doubled at fixed stars
    L_ME = 2 * L_ME; L_FS = L_FS / 2
S_CHAB = float(np.median(10**(np.array([d["lMc"] for d in LENS]) - np.array([d["lMs"] for d in LENS]))))

A_sig = 10**np.array([a["logsig_e"] for a in CAL]); A_x = np.log10(A_sig) - 2.3
A_L = 10**np.array([a["logL"] for a in CAL])
A_MJ = 10**np.array([a["logML_JAM"] for a in CAL]) * A_L
A_MS = 10**np.array([a["logML_Salp"] for a in CAL]) * A_L
A_r = 10**np.array([a["logr12"] for a in CAL]) * np.array([a["Dist_Mpc"] for a in CAL]) * 1000.0 / 206264.806   # kpc
nD = len(CAL)

# ============================================================== B: kernels
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y):
    y = np.asarray(y, float)
    s = np.sqrt(np.minimum(y, 1e4))
    with np.errstate(over="ignore", invalid="ignore"):
        e = np.expm1(s)
        d = 1.0 / e - (s / 2) * np.exp(s) / e**2
    return np.where(y < 1e4, d, 0.0)
def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 / (-np.expm1(-np.sqrt(y)))
def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0, xtol=1e-14)
H_P = float(h_rar(Y_P))
LYG = np.linspace(-14, 14, 280001)
_YG = 10**LYG
_DH = np.maximum(dh_rar(_YG), 0.05 * H_P / (_YG + Y_P))
_HM = float(h_rar(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), LYG, _HM) / y
def nu_one(y): return np.ones_like(np.asarray(y, float))

# ============================================================== B: stars
SN = 4.0
BN = 2 * SN - 1 / 3. + 4 / (405 * SN) + 46 / (25515 * SN**2)
PP = 1 - 0.6097 / SN + 0.05463 / SN**2
def M2D_star(x): return gammainc(2 * SN, BN * np.maximum(np.asarray(x, float), 1e-12)**(1 / SN))
def M3D_star(x): return gammainc(SN * (3 - PP), BN * np.maximum(np.asarray(x, float), 1e-12)**(1 / SN))

# Gauss-Legendre nodes
def gl(n, a, b):
    t, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * t + 0.5 * (b + a), 0.5 * (b - a) * w
NGL_T, NGL_U = 64, 300

def project(Mfun, R, rmax, nt=NGL_T, nu_=NGL_U):
    """M2D(R) of a spherical M(r) truncated at rmax: M(rmax) w(rmax) + int_0^{acos(R/rmax)} M(R/cos t) cos t dt (split t<=pi/3, u>=ln2)."""
    th, wt = gl(nt, 0.0, math.pi / 3)
    part1 = np.sum(wt * Mfun(R / np.cos(th)) * np.cos(th))
    U = math.log(rmax / R)
    u, wu = gl(nu_, math.log(2.0), U)
    part2 = np.sum(wu * Mfun(R * np.exp(u)) * np.exp(-2 * u) / np.sqrt(-np.expm1(-2 * u)))
    w_end = 1 - math.sqrt(1 - (R / rmax)**2)
    return part1 + part2 + float(Mfun(np.array([rmax]))[0]) * w_end

class BModel:
    def __init__(self, a0, nufun=nu_mono, rmax=3000.0):
        self.a0, self.nu, self.rmax = a0, nufun, rmax
        self.qa = (G_SI * Msun / kpc**2) / a0 if a0 > 0 else 0.0     # y = qa M[Msun] / r[kpc]^2
    def phantom(self, Mstar, Re, r):
        Mb = Mstar * M3D_star(r / Re)
        if self.a0 <= 0: return np.zeros_like(r)
        y = self.qa * Mb / r**2
        return (self.nu(y) - 1.0) * Mb
    def boost(self, Mstar, Re, R, rmax=None, nt=NGL_T, nu_=NGL_U):
        rmax = self.rmax if rmax is None else rmax
        if self.a0 <= 0: return 1.0
        ph = project(lambda r: self.phantom(Mstar, Re, r), R, rmax, nt, nu_)
        return 1.0 + ph / (Mstar * float(M2D_star(R / Re)))
    def kbar(self, i, alpha, band, fs=None, ms=None):
        fs = L_FS[i] if fs is None else fs; ms = L_MS[i] if ms is None else ms
        return alpha * fs * self.boost(alpha * ms, L_RE[band][i], L_R[i])
    def alpha_lens(self, i, band, fs=None, ms=None):
        f = lambda la: self.kbar(i, 10**la, band, fs, ms) - 1.0
        if f(-3.0) > 0 or f(1.5) < 0: return float("nan")
        return brentq(f, -3.0, 1.5, xtol=1e-13, rtol=1e-14)          # log10 alpha
    def alpha_dyn(self, j, MJ=None):
        MJ = A_MJ[j] if MJ is None else MJ; r = A_r[j]
        if self.a0 <= 0: return math.log10(MJ / A_MS[j])
        qd = self.qa / 2.0
        f = lambda lm: (10**lm) * float(self.nu(qd * 10**lm / r**2)) - MJ
        if f(3.0) > 0 or f(14.5) < 0: return float("nan")
        return brentq(f, 3.0, 14.5, xtol=1e-13, rtol=1e-14) - math.log10(A_MS[j])

def solve_B(model, band, fs=None, ms=None):
    la = np.array([model.alpha_lens(i, band, None if fs is None else fs[i], None if ms is None else ms[i]) for i in range(nL)])
    ld = np.array([model.alpha_dyn(j) for j in range(nD)])
    return la, ld

# ============================================================== statistic + paired bootstrap
def fit_ls(xd, yd):
    xm, ym = xd.mean(), yd.mean()
    s = ((xd - xm) * (yd - ym)).sum() / ((xd - xm)**2).sum()
    return s, ym - s * xm
def point_stat(la, ld):
    ok_l, ok_d = np.isfinite(la), np.isfinite(ld)
    s, a = fit_ls(A_x[ok_d], ld[ok_d])
    return float(np.median(la[ok_l] - (a + s * L_x[ok_l]))), s, a
rngB = np.random.default_rng(87)
IC = np.stack([rngB.integers(0, nD, nD) for _ in range(NB)])
IL = np.stack([rngB.integers(0, nL, nL) for _ in range(NB)])
def boot_delta(la, ld):
    ok_l, ok_d = np.isfinite(la), np.isfinite(ld)
    out = np.empty(NB); sl = np.empty(NB)
    for b in range(NB):
        ic = IC[b]; il = IL[b]
        ic = ic[ok_d[ic]]; il = il[ok_l[il]]
        s, a = fit_ls(A_x[ic], ld[ic])
        out[b] = np.median(la[il] - (a + s * L_x[il])); sl[b] = s
    return out, sl
def boot_perlens(laB, ldB, laL, ldL):
    okl = np.isfinite(laB) & np.isfinite(laL); okd = np.isfinite(ldB) & np.isfinite(ldL)
    out = np.empty(NB)
    for b in range(NB):
        ic = IC[b]; il = IL[b]
        ic = ic[okd[ic]]; il = il[okl[il]]
        sB, aB = fit_ls(A_x[ic], ldB[ic]); sL, aL = fit_ls(A_x[ic], ldL[ic])
        out[b] = np.median((laB[il] - (aB + sB * L_x[il])) - (laL[il] - (aL + sL * L_x[il])))
    return out
def stat_block(la, ld):
    d, s, a = point_stat(la, ld)
    bd, bs = boot_delta(la, ld)
    err = float(np.std(bd))
    return dict(delta=d, err=err, slope=s, slope_err=float(np.std(bs)), bd=bd,
                z=d / math.sqrt(err**2 + SIGMA_FLOOR**2), zstat=d / err,
                n_lens=int(np.isfinite(la).sum()), n_cal=int(np.isfinite(ld).sum()),
                a_lens=float(10**np.median(la[np.isfinite(la)])), a_dyn=float(10**np.median(a + s * L_x)))

# ============================================================== LCDM side (CFG86 model functions, copied)
def shmr_logMs(logMh, z=0.0):
    zz = z / (1 + z)
    logM1 = 11.590 + 1.195 * zz; N = 0.0351 - 0.0247 * zz; beta = 1.376 - 0.826 * zz; gam = 0.608 + 0.329 * zz
    x = 10**(logMh - logM1)
    return logMh + np.log10(2 * N / (x**(-beta) + x**gam))
_GRID = np.linspace(9.0, 15.5, 13001)
_inv_cache = {}
def halo_logmass_fn(z=0.0):
    key = round(z, 6)
    if key not in _inv_cache:
        ls = shmr_logMs(_GRID, z); assert np.all(np.diff(ls) > 0); _inv_cache[key] = ls
    ls = _inv_cache[key]
    return lambda logMs: float(np.interp(logMs, ls, _GRID))
def c_duffy_full(Mh, z=0.0, zc=False): return 5.71 * (Mh / (2e12 / H_HALO))**-0.084 * ((1 + z)**-0.47 if zc else 1.0)
def c_duffy_rel(Mh, z=0.0, zc=False): return 6.71 * (Mh / (2e12 / H_HALO))**-0.091 * ((1 + z)**-0.44 if zc else 1.0)
def c_dm(Mh, z=0.0, zc=False):
    if zc:
        a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z**1.21); b = -0.101 + 0.026 * z
    else:
        a, b = 0.905, -0.101
    return 10**(a + b * math.log10(Mh / (1e12 / H_HALO)))
CREL = {"duffy": c_duffy_full, "relaxed": c_duffy_rel, "dm": c_dm}
def mfun(t): return np.log1p(t) - t / (1 + t)
def r200(Mh, rhoc): return (3 * Mh / (4 * np.pi * 200 * rhoc))**(1 / 3)
def m3d(r, Mh, c, R200):
    x = np.clip(r / R200, 1e-4, 5.0); return Mh * mfun(c * x) / mfun(c)
def hfun(X):
    X = float(X)
    if abs(X - 1) < 1e-7: return 1 + math.log(0.5)
    if X < 1:
        s = math.sqrt(1 - X * X); eps = X * X / (1 + s)
        return -X * X * math.log(X) / (s * (1 + s)) + (math.log1p(-eps / 2) + eps * math.log(2)) / s
    return math.log(X / 2) + math.acos(1 / X) / math.sqrt(X * X - 1)
def m2d(R, Mh, c, R200): return Mh * hfun(c * R / R200) / float(mfun(c))
def rhoc_z(z): return RHOC0 * (OM * (1 + z)**3 + OL)

class Cfg:
    def __init__(self, mult=1.0, tie="solved_salp", zmode="z0", crel="duffy", dzero=0.0, zrho=False, zc=False, zmost=False):
        self.mult, self.tie, self.crel, self.dzero = mult, tie, crel, dzero
        if zmode == "full": zrho = zc = zmost = True
        self.zrho, self.zc, self.zmost = zrho, zc, zmost
    def label(self):
        z = "zfull" if (self.zrho and self.zc and self.zmost) else ("z0" if not (self.zrho or self.zc or self.zmost) else
            "z[" + ("r" if self.zrho else "") + ("c" if self.zc else "") + ("m" if self.zmost else "") + "]")
        return f"m={self.mult:g} tie={self.tie} {z} c={self.crel}"
def make_halo(cfg, logMs, z, fixed_logMs=None):
    f = halo_logmass_fn(z if cfg.zmost else 0.0)
    if cfg.tie == "solved_salp": lm = f(logMs)
    elif cfg.tie == "solved_chab": lm = f(logMs + math.log10(S_CHAB))
    else: lm = f(fixed_logMs)
    Mh = 10**lm * cfg.mult
    zc_ = z if cfg.zc else 0.0
    c = CREL[cfg.crel](Mh, zc_, cfg.zc)
    rc = rhoc_z(z) if cfg.zrho else RHOC0
    return Mh, c, r200(Mh, rc), lm
def kbar_lens(logMs, i, cfg, fs=None, ms=None, me=None):
    d = cfg.dzero
    MS = (L_MS[i] if ms is None else ms) * 10**d; FS = (L_FS[i] if fs is None else fs) * 10**d
    ME = L_ME[i] if me is None else me
    Mh, c, R200, lm = make_halo(cfg, logMs, L_z[i], fixed_logMs=math.log10(L_MC[i]))
    return (10**logMs) / MS * FS + (1 - FB) * m2d(L_R[i], Mh, c, R200) / ME - 1.0
def solve_lens(i, cfg, **kw):
    f = lambda lm: kbar_lens(lm, i, cfg, **kw)
    if f(8.0) > 0 or f(13.5) < 0: return None
    return brentq(f, 8.0, 13.5, xtol=1e-12, rtol=1e-14)
def dyn_resid(logMs, j, cfg):
    Mstar = 10**logMs
    Mh, c, R200, lm = make_halo(cfg, logMs, 0.0, fixed_logMs=math.log10(A_MS[j] * S_CHAB))
    return 0.5 * Mstar + (1 - FB) * float(m3d(A_r[j], Mh, c, R200)) - A_MJ[j] / 2
def solve_dyn(j, cfg):
    f = lambda lm: dyn_resid(lm, j, cfg)
    if f(8.0) > 0 or f(13.5) < 0: return None
    return brentq(f, 8.0, 13.5, xtol=1e-12, rtol=1e-14)
def solve_L(cfg):
    la = np.full(nL, np.nan); ld = np.full(nD, np.nan)
    for i in range(nL):
        v = solve_lens(i, cfg)
        if v is not None: la[i] = v - math.log10(L_MS[i] * 10**cfg.dzero)
    for j in range(nD):
        v = solve_dyn(j, cfg)
        if v is not None: ld[j] = v - math.log10(A_MS[j])
    return la, ld

# ============================================================== CONTROLS (before results)
print("\n=== CONTROLS: kernel ===", flush=True)
ys = np.logspace(-8, 0, 400)
rel = np.max(np.abs(nu_mono(ys) / nu_rar(ys) - 1))
check("C1 nu_mono == nu_RAR to 1e-5 for 1e-8<=y<=1", rel < 1e-5, f"max rel {rel:.2e}")
yy = np.logspace(-12, 8, 4001)
check("C1 nu_mono >= 1 and y*nu_mono strictly increasing (1e-12..1e8)", bool(np.all(nu_mono(yy) >= 1) and np.all(np.diff(yy * nu_mono(yy)) > 0)))
check("C1 nu_mono-1 < 2e-3 at y=1e3", float(nu_mono(1e3)) - 1 < 2e-3, f"{float(nu_mono(1e3))-1:.2e}")
check("C1 Y_P = 2.5396 +- 1e-3", abs(Y_P - 2.5396) < 1e-3, f"{Y_P:.5f}, H_P {H_P:.5f}")
print(f"  (nu_mono at y=1,3,10,30: {[round(float(nu_mono(v)),5) for v in (1,3,10,30)]}; nu_RAR: {[round(float(nu_rar(v)),5) for v in (1,3,10,30)]})", flush=True)

print("\n=== CONTROLS: projection and stars ===", flush=True)
e1 = abs(project(lambda r: np.ones_like(r), 5.0, 1e7) / 1.0 - 1)
e1b = abs(project(lambda r: np.ones_like(r), 5.0, 3000.0) - 1)
check("C2 point mass -> M2D = M to 1e-9", max(e1, e1b) < 1e-9, f"{e1:.1e} {e1b:.1e}")
kk, R, rm = 1.7, 5.0, 3000.0
tr = kk * (rm * (1 - math.sqrt(1 - R**2 / rm**2)) + R * math.acos(R / rm))
e2 = abs(project(lambda r: kk * r, R, rm) / tr - 1)
e3 = abs(project(lambda r: kk * r, R, 1e7) / (math.pi / 2 * kk * R) - 1)
check("C2 SIS truncated closed form (1e-7)", e2 < 1e-7, f"{e2:.1e}")
check("C2 SIS untruncated (pi/2) k R (1e-6)", e3 < 1e-6, f"{e3:.1e}")
BM = {(fn, b): BModel(A0[fn]) for fn in A0 for b in "VI"}
mB = BModel(A0["canonical"])
conv = []; brute = []; trunc = []
for i in [0, 7, 15, 31, 47, 63]:
    Ms = L_MS[i] * 0.9; Re = L_RE["V"][i]; Rr = L_R[i]
    a = mB.boost(Ms, Re, Rr); a2 = mB.boost(Ms, Re, Rr, nt=2 * NGL_T, nu_=2 * NGL_U)
    conv.append(abs((a - 1) / (a2 - 1) - 1))
    rr = np.geomspace(1e-5 * Re, 3000 * kpc / kpc, 6000)
    ph = mB.phantom(Ms, Re, rr); dM = np.gradient(ph, rr)
    w = np.where(rr <= Rr, 1.0, 1.0 - np.sqrt(np.clip(1.0 - (Rr / np.maximum(rr, 1e-30))**2, 0, 1)))
    bf = float(np.trapz(dM * w, rr))
    brute.append(abs(bf / (Ms * float(M2D_star(Rr / Re)) * (a - 1)) - 1))
    trunc.append(abs((mB.boost(Ms, Re, Rr, rmax=1e6) - 1) / (mB.boost(Ms, Re, Rr, rmax=1e7) - 1) - 1))
check("C2 quadrature convergence (nodes x2) <= 1e-7 (6 lenses)", max(conv) < 1e-7, f"max {max(conv):.1e}")
check("C2 brute-force trapezoid projection agrees <= 5e-3 (6 lenses)", max(brute) < 5e-3, f"max {max(brute):.1e}")
check("C2 untruncated 1e6 vs 1e7 kpc stable to 1e-4", max(trunc) < 1e-4, f"max {max(trunc):.1e}")
xs = np.array([1e3, 1e5])
check("C3 Sersic 2D and 3D fractions -> 1 at large x (1e-9)", abs(float(M2D_star(1e3)) - 1) < 1e-9 and abs(float(M3D_star(1e3)) - 1) < 1e-9)
def dens(x): x = np.maximum(x, 1e-12); return x**(-PP) * np.exp(-BN * x**(1 / SN))
rr = np.geomspace(1e-6, 3000.0, 20001)
m3 = np.array([quad(lambda r: 4 * np.pi * r * r * dens(r), 0, 400, limit=400)[0]])[0]
Mr = np.concatenate([[0], np.cumsum(0.5 * (4 * np.pi * rr[1:]**2 * dens(rr[1:]) + 4 * np.pi * rr[:-1]**2 * dens(rr[:-1])) * np.diff(rr))])
Mr /= Mr[-1]
worst = 0
for xr in (0.3, 0.6, 1.0, 2.0):
    val = project(lambda r: np.interp(r, rr, Mr), xr, 3000.0)
    worst = max(worst, abs(val / float(M2D_star(xr)) - 1))
check("C3 numerical projection of the PS density vs exact Sersic within 3% (x=0.3..2)", worst < 0.03, f"worst {worst:.4f}")
# consistency of my M3D_star with the numerically integrated PS density (normalised)
w3 = max(abs(np.interp(x_, rr, Mr) / float(M3D_star(x_)) - 1) for x_ in (0.1, 0.5, 1, 3, 10))
check("C3 regularised-gamma M3D_star == numerically integrated PS density to 1e-4", w3 < 1e-4, f"{w3:.1e}")

# ============================================================== B solves
print("\n=== B SOLVES ===", flush=True)
CELLS_B = [("canonical", "V"), ("canonical", "I"), ("alt", "V"), ("alt", "I")]
NAMEB = {c: f"{c[0][:3]} {c[1]}" for c in CELLS_B}
solB = {}
kbar1 = {}
for c in CELLS_B:
    m = BModel(A0[c[0]])
    la, ld = solve_B(m, c[1])
    solB[c] = (la, ld)
    kbar1[c] = float(np.median([m.kbar(i, 1.0, c[1]) for i in range(nL)]))
    print(f"  B {NAMEB[c]}: solved lenses {int(np.isfinite(la).sum())}/{nL}, calibrators {int(np.isfinite(ld).sum())}/{nD}", flush=True)
check("P1 B: 70/70 lenses and 187/187 calibrators solved (all cells)", all(np.isfinite(v[0]).all() and np.isfinite(v[1]).all() for v in solB.values()))
res_l = 0.0
for c in CELLS_B:
    m = BModel(A0[c[0]])
    for i in range(nL):
        res_l = max(res_l, abs(m.kbar(i, 10**solB[c][0][i], c[1]) - 1))
res_d = 0.0
for c in CELLS_B:
    m = BModel(A0[c[0]])
    for j in range(nD):
        Ms = 10**(solB[c][1][j] + math.log10(A_MS[j]))
        res_d = max(res_d, abs(Ms * float(m.nu(m.qa / 2 * Ms / A_r[j]**2)) - A_MJ[j]) / A_MJ[j])
check("C4 kbar(alpha_lens)=1 (1e-9) and nu M_*=M_JAM (1e-9)", res_l < 1e-9 and res_d < 1e-9, f"{res_l:.1e} {res_d:.1e}")
# closed-form dynamics limits
m0 = BModel(A0["canonical"])
Mj_deep = 1e5; r_ = 1.0
Mstar_cf = G_SI * (Mj_deep * Msun)**2 / (2 * (r_ * kpc)**2 * A0["canonical"]) / Msun
y_deep = m0.qa / 2 * Mstar_cf / r_**2
lm_deep = brentq(lambda lm: 10**lm * float(m0.nu(m0.qa / 2 * 10**lm / r_**2)) - Mj_deep, -3.0, 12.0, xtol=1e-14)
e_deep = abs(10**lm_deep / Mstar_cf - 1)
check("C4 deep-MOND limit M_*=G M_JAM^2/(2 r^2 a0) (y<=1e-8, 2e-4)", y_deep < 1e-8 and e_deep < 2e-4, f"y {y_deep:.1e} rel {e_deep:.1e}")
Mj_n = 1e11; r_n = 0.2
lm_n = brentq(lambda lm: 10**lm * float(m0.nu(m0.qa / 2 * 10**lm / r_n**2)) - Mj_n, 5.0, 13.0, xtol=1e-14)
y_n = m0.qa / 2 * 10**lm_n / r_n**2
check("C4 Newtonian limit M_*=M_JAM (y>=1e3, 3e-3)", y_n > 1e3 and abs(10**lm_n / Mj_n - 1) < 3e-3, f"y {y_n:.1e} rel {abs(10**lm_n/Mj_n-1):.1e}")

# reproduction: kappa-bar at alpha=1
print("\n=== P2: kappa-bar at Salpeter (alpha=1) ===", flush=True)
tg = {("canonical", "V"): 0.834, ("canonical", "I"): 0.807, ("alt", "V"): 0.859, ("alt", "I"): 0.825}
for c in CELLS_B:
    repro(f"nu_mono kbar(1) {NAMEB[c]}", kbar1[c], tg[c], 0.0006, 0.005)
tgr = {("canonical", "V"): 0.8246, ("canonical", "I"): 0.7938, ("alt", "V"): 0.8542, ("alt", "I"): 0.8124}
kbar1_rar = {}
for c in CELLS_B:
    m = BModel(A0[c[0]], nufun=nu_rar)
    kbar1_rar[c] = float(np.median([m.kbar(i, 1.0, c[1]) for i in range(nL)]))
    repro(f"nu_RAR kbar(1) {NAMEB[c]} (h53)", kbar1_rar[c], tgr[c], 0.0006, 0.005)

# ============================================================== LCDM base + halo-off cross code
print("\n=== LCDM BASE (CFG86 code) ===", flush=True)
BASE = Cfg()
laL0, ldL0 = solve_L(BASE)
sbase = stat_block(laL0, ldL0)
print(f"  LCDM base: n={sbase['n_lens']}/{sbase['n_cal']} Delta {sbase['delta']:+.4f} err {sbase['err']:.4f} zstat {sbase['zstat']:+.2f} z {sbase['z']:+.2f}", flush=True)
if not MUTATE:
    check("P4/C-copy LCDM base +0.0370 +- 0.0015, err 0.0247 +- 0.003", abs(sbase["delta"] - 0.0370) < 0.0015 and abs(sbase["err"] - 0.0247) < 0.003,
          f"{sbase['delta']:+.4f} {sbase['err']:.4f}")
check("P1 LCDM 70/70 and 187/187", sbase["n_lens"] == 70 and sbase["n_cal"] == 187)

# phantom off
print("\n=== C5: phantom off ===", flush=True)
mo1 = BModel(0.0)
la_o = np.array([mo1.alpha_lens(i, "V") for i in range(nL)]); ld_o = np.array([mo1.alpha_dyn(j) for j in range(nD)])
mo2 = BModel(1e-30)
la_o2 = np.array([mo2.alpha_lens(i, "V") for i in range(nL)]); ld_o2 = np.array([mo2.alpha_dyn(j) for j in range(nD)])
e_a = max(abs(10**la_o[i] * L_FS[i] - 1) for i in range(nL))
e_b = max(abs(10**ld_o[j] * A_MS[j] / A_MJ[j] - 1) for j in range(nD))
e_c = max(np.max(np.abs(la_o2 - la_o)), np.max(np.abs(ld_o2 - ld_o)))
check("C5 phantom off (nu==1): alpha_lens=1/Fs, alpha_dyn=M_JAM/M_Salp (1e-9)", max(e_a, e_b) < 1e-9, f"{e_a:.1e} {e_b:.1e}")
check("C5 a0=1e-30 through the nu_mono table == phantom off (1e-9)", e_c < 1e-9, f"{e_c:.1e}")
gap_off, _, _ = point_stat(la_o, ld_o)
cfg_off = Cfg(mult=1e-30)
laLo, ldLo = solve_L(cfg_off)
gap_offL, _, _ = point_stat(laLo, ldLo)
err_off = stat_block(la_o, ld_o)
check("C5 B-code halo-free gap == LCDM-code halo x1e-30 gap (1e-9): two codes, one number", abs(gap_off - gap_offL) < 1e-9, f"{gap_off:+.6f} vs {gap_offL:+.6f}")
if not MUTATE:
    check("C5 halo-free gap = +0.191 +- 0.0006 (CFG86)", abs(gap_off - 0.191) < 0.0006, f"{gap_off:+.4f}, err {err_off['err']:.4f}, z_stat {err_off['zstat']:.2f}")
else:
    check("C5 halo-free gap = +0.191 +- 0.0006 (CFG86) [must FAIL under MUTATE]", abs(gap_off - 0.191) < 0.0006, f"{gap_off:+.4f}")

# estimator closed forms
print("\n=== C6: estimator closed forms ===", flush=True)
r_ = np.random.default_rng(1)
xd = r_.uniform(-0.3, 0.4, 80); ldd = -0.1 + 0.2 * xd; xl = r_.uniform(-0.1, 0.35, 30)
s_, a_ = fit_ls(xd, ldd)
check("C6 lenses on the fit line -> Delta=0 (1e-12)", abs(np.median((-0.1 + 0.2 * xl) - (a_ + s_ * xl))) < 1e-12)
check("C6 lenses = fit + k -> Delta=k (1e-12)", abs(np.median((-0.1 + 0.2 * xl + 0.137) - (a_ + s_ * xl)) - 0.137) < 1e-12)
check("C6 fit recovers synthetic law (1e-10)", abs(s_ - 0.2) < 1e-10 and abs(a_ + 0.1) < 1e-10)
_bd, _ = boot_delta(laL0, ldL0)
check("C6 identical resamples for B:=L give D^b == 0", float(np.max(np.abs(_bd - _bd))) == 0.0)

# zero point
print("\n=== C7: zero point ===", flush=True)
mzB = BModel(A0["canonical"])
zp_err = 0.0
if not MUTATE:
    d0B = point_stat(*solve_B(mzB, "V"))[0]
    d0L = point_stat(laL0, ldL0)[0]
    for dz in (0.10, -0.10):
        laB_d = np.array([mzB.alpha_lens(i, "V", fs=L_FS[i] * 10**dz, ms=L_MS[i] * 10**dz) for i in range(nL)])
        ldB = solB[("canonical", "V")][1]
        dB = point_stat(laB_d, ldB)[0]
        laL_d, ldL_d = solve_L(Cfg(dzero=dz))
        dL = point_stat(laL_d, ldL_d)[0]
        zp_err = max(zp_err, abs((dB - d0B) + dz), abs((dL - d0L) + dz))
    check("C7 zero-point d=+-0.1: Delta_B and Delta_L both shift by exactly -d (1e-9)", zp_err < 1e-9, f"{zp_err:.1e}")

# ============================================================== MAIN: gaps, reproduction
print("\n=== B GAPS (P3) ===", flush=True)
stB = {c: stat_block(*solB[c]) for c in CELLS_B}
tgap = {("canonical", "V"): 0.159, ("canonical", "I"): 0.171, ("alt", "V"): 0.152, ("alt", "I"): 0.168}
terr = {("canonical", "V"): 0.021, ("canonical", "I"): 0.022, ("alt", "V"): 0.022, ("alt", "I"): 0.022}
tz = {("canonical", "V"): 1.56, ("canonical", "I"): 1.68, ("alt", "V"): 1.49, ("alt", "I"): 1.64}
tzs = {("canonical", "V"): 7.6, ("canonical", "I"): 7.8, ("alt", "V"): 6.9, ("alt", "I"): 7.5}
tal = {("canonical", "V"): 1.23, ("canonical", "I"): 1.27, ("alt", "V"): 1.20, ("alt", "I"): 1.24}
tad = {("canonical", "V"): 0.86, ("canonical", "I"): 0.86, ("alt", "V"): 0.85, ("alt", "I"): 0.85}
for c in CELLS_B:
    s = stB[c]
    print(f"  B {NAMEB[c]:8s}: Delta {s['delta']:+.4f} err {s['err']:.4f} z(floor) {s['z']:+.2f} z_stat {s['zstat']:+.2f}  alpha_lens {s['a_lens']:.3f}  alpha_dyn@lenses {s['a_dyn']:.3f}  slope {s['slope']:+.3f}+-{s['slope_err']:.3f}", flush=True)
    repro(f"gap {NAMEB[c]}", s["delta"], tgap[c], 0.0006, 0.005)
    repro(f"err {NAMEB[c]}", s["err"], terr[c], 0.0006, 0.003)
    repro(f"z(floor) {NAMEB[c]}", s["z"], tz[c], 0.006, 0.05)
    repro(f"z_stat {NAMEB[c]}", s["zstat"], tzs[c], 0.06, 0.2)
    repro(f"alpha_lens {NAMEB[c]}", s["a_lens"], tal[c], 0.006, 0.01)
    repro(f"alpha_dyn@lenses {NAMEB[c]}", s["a_dyn"], tad[c], 0.006, 0.01)
repro("B dynamics slope canonical V (H3)", stB[("canonical", "V")]["slope"], 0.204, 0.0006, 0.02)
head_ok = all(abs(stB[c]["delta"]) <= 2 * math.sqrt(stB[c]["err"]**2 + SIGMA_FLOOR**2) for c in CELLS_B)
check("H2 [HEADLINE] B passes CFG33's gate with the floor in all four cells", head_ok, "z = " + ", ".join(f"{stB[c]['z']:+.2f}" for c in CELLS_B), kind="headline")
print(f"  LCDM gate with floor: Delta {sbase['delta']:+.4f} z {sbase['z']:+.2f} -> {'PASS' if abs(sbase['z'])<=2 else 'FAIL'}", flush=True)

# ============================================================== PAIRED base cell
print("\n=== PAIRED B - LCDM, base LCDM cell (P5) ===", flush=True)
tP = {("canonical", "V"): (0.122, 0.016), ("canonical", "I"): (0.135, 0.017), ("alt", "V"): (0.115, 0.015), ("alt", "I"): (0.132, 0.016)}
pair_base = {}
for c in CELLS_B:
    D = stB[c]["delta"] - sbase["delta"]
    Db = stB[c]["bd"] - sbase["bd"]
    ep = float(np.std(Db)); eu = math.sqrt(stB[c]["err"]**2 + sbase["err"]**2)
    sh = float(np.std(stB[c]["bd"] - np.roll(sbase["bd"], 1)))
    pl = boot_perlens(*solB[c], laL0, ldL0)
    # per-lens point estimate
    okd_B = np.isfinite(solB[c][1]); okd_L = np.isfinite(ldL0)
    sB_, aB_ = fit_ls(A_x[okd_B], solB[c][1][okd_B]); sL_, aL_ = fit_ls(A_x[okd_L], ldL0[okd_L])
    Dpl = float(np.median((solB[c][0] - (aB_ + sB_ * L_x)) - (laL0 - (aL_ + sL_ * L_x))))
    pair_base[c] = dict(D=D, err_pair=ep, err_unp=eu, err_shuffle=sh, z_pair=D / ep, D_perlens=Dpl, err_perlens=float(np.std(pl)))
    print(f"  {NAMEB[c]:8s}: D = {D:+.4f} +- {ep:.4f} (paired) [{D/ep:.1f} sigma]   unpaired {eu:.4f} [{D/eu:.1f}]   shuffled {sh:.4f}   per-lens estimator {Dpl:+.4f} +- {np.std(pl):.4f}", flush=True)
    repro(f"paired D {NAMEB[c]} (CFG80)", D, tP[c][0], 0.0006, 0.003)
    repro(f"paired err {NAMEB[c]} (CFG80)", ep, tP[c][1], 0.0006, 0.003)
    check(f"C8 shuffle error within 10% of quadrature ({NAMEB[c]})", abs(sh / eu - 1) < 0.10, f"shuffled {sh:.4f} vs quadrature {eu:.4f}; paired/unpaired {ep/eu:.2f}")

# ============================================================== B variants (paired against LCDM base)
print("\n=== B VARIANTS (paired vs LCDM base; reported) ===", flush=True)
a0_exact = {}
H0_ = 67.4e3 / 3.0856775814913673e22
rhoc_ = 3 * H0_**2 / (8 * math.pi * 6.67430e-11)
a0_exact["canonical"] = 0.5 * c_SI * math.sqrt(6.67430e-11 * 0.6847 * rhoc_)
a0_exact["alt"] = 0.5 * c_SI * math.sqrt(6.67430e-11 * 1.0 * rhoc_)
var_defs = {
    "P2 kernel": lambda fn: BModel(A0[fn], nufun=nu_p2),
    "nu_RAR (h53)": lambda fn: BModel(A0[fn], nufun=nu_rar),
    "untruncated cylinder": lambda fn: BModel(A0[fn], rmax=1e7),
    "a0 from FP0 formula": lambda fn: BModel(a0_exact[fn]),
}
varres = {}
for vn, mk in var_defs.items():
    row = []
    for c in CELLS_B:
        m = mk(c[0])
        la, ld = solve_B(m, c[1])
        s = stat_block(la, ld)
        Dv = s["delta"] - sbase["delta"]; ep = float(np.std(s["bd"] - sbase["bd"]))
        row.append((s["delta"], s["err"], Dv, ep))
        varres[(vn, c)] = dict(delta=s["delta"], err=s["err"], D=Dv, err_pair=ep)
    print(f"  {vn:22s} gaps " + " ".join(f"{r[0]:+.4f}" for r in row) + "   | paired D " + " ".join(f"{r[2]:+.4f}+-{r[3]:.4f}" for r in row), flush=True)
print(f"  (FP0-formula a0: canonical {a0_exact['canonical']:.4e}, alt {a0_exact['alt']:.4e})", flush=True)

# ============================================================== 54 + 18 cell grid
print("\n=== GRID: LCDM cells, paired against B ===", flush=True)
grid = []
tg0 = time.time()
for m in [1 / 3, 1, 3, 0.1, 10]:
    for tie in ["solved_salp", "solved_chab", "fixed_chab"]:
        for zm in ["z0", "full"]:
            for cr in ["duffy", "relaxed", "dm"]:
                cfg = Cfg(mult=m, tie=tie, zmode=zm, crel=cr)
                la, ld = solve_L(cfg)
                if np.isfinite(la).sum() < 5 or np.isfinite(ld).sum() < 5:
                    print("   UNFIT cell", cfg.label()); continue
                s = stat_block(la, ld)
                g = dict(axes=(m, tie, zm, cr), delta=s["delta"], err=s["err"], zstat=s["zstat"], z=s["z"],
                         n_lens=s["n_lens"], n_cal=s["n_cal"])
                g["Sa"] = abs(s["delta"]) <= 2 * s["err"]
                for c in CELLS_B:
                    D = stB[c]["delta"] - s["delta"]
                    Db = stB[c]["bd"] - s["bd"]
                    ep = float(np.std(Db)); eu = math.sqrt(stB[c]["err"]**2 + s["err"]**2)
                    g[c] = dict(D=D, err_pair=ep, err_unp=eu, Sb_pair=D > 2 * ep, Sb_unp=D > 2 * eu)
                # worst-case B cell: smallest D
                cmin = min(CELLS_B, key=lambda c: g[c]["D"])
                g["cmin"] = cmin
                g["Sb_min"] = g[cmin]["Sb_pair"]
                g["W_min"] = g["Sa"] and g[cmin]["Sb_pair"]
                g["W_all"] = g["Sa"] and all(g[c]["Sb_pair"] for c in CELLS_B)
                g["Sb_all"] = all(g[c]["Sb_pair"] for c in CELLS_B)
                g["Sb_min_unp"] = g[cmin]["Sb_unp"]
                grid.append(g)
print(f"  grid time {time.time()-tg0:.0f}s", flush=True)
core = [g for g in grid if g["axes"][0] in (1 / 3, 1, 3)]
ext = [g for g in grid if g["axes"][0] in (0.1, 10)]
print(f"{'m':>5} {'tie':12s} {'z':5s} {'c':8s}  DeltaL   errL  Sa | D(min B)  err_pair  z_pair  Sb_pair Sb_unp  W_min  [D canV canI altV altI]")
for g in grid:
    m, tie, zm, cr = g["axes"]; cm = g["cmin"]
    print(f"{m:5.2f} {tie:12s} {zm:5s} {cr:8s} {g['delta']:+.4f} {g['err']:.4f} {int(g['Sa'])}  | {g[cm]['D']:+.4f}  {g[cm]['err_pair']:.4f}  {g[cm]['D']/g[cm]['err_pair']:6.1f}   {int(g[cm]['Sb_pair'])}      {int(g[cm]['Sb_unp'])}     {int(g['W_min'])}   " +
          " ".join(f"{g[c]['D']:+.3f}" for c in CELLS_B))
def frac(lst, key): return sum(1 for g in lst if g[key]) / len(lst)
print(f"\nDECLARED RANGE ({len(core)} cells): S_a {frac(core,'Sa'):.3f} ({sum(g['Sa'] for g in core)}/{len(core)})  S_b(paired, worst B cell) {frac(core,'Sb_min'):.3f} ({sum(g['Sb_min'] for g in core)}/{len(core)})  "
      f"S_b(unpaired, worst B cell) {frac(core,'Sb_min_unp'):.3f}  W_min {frac(core,'W_min'):.3f} ({sum(g['W_min'] for g in core)}/{len(core)})  W_all-four-B-cells {frac(core,'W_all'):.3f}")
for c in CELLS_B:
    n_sb = sum(1 for g in core if g[c]["Sb_pair"]); n_w = sum(1 for g in core if g["Sa"] and g[c]["Sb_pair"])
    print(f"   B cell {NAMEB[c]:8s}: S_b(paired) {n_sb}/{len(core)}  W {n_w}/{len(core)}  D range {min(g[c]['D'] for g in core):+.3f}..{max(g[c]['D'] for g in core):+.3f}  median {np.median([g[c]['D'] for g in core]):+.3f}  "
          f"err_pair range {min(g[c]['err_pair'] for g in core):.4f}..{max(g[c]['err_pair'] for g in core):.4f}")
print(f"EXTENDED context ({len(ext)} cells): S_a {frac(ext,'Sa'):.3f}  S_b(paired, worst) {frac(ext,'Sb_min'):.3f}  W_min {frac(ext,'W_min'):.3f}")
print("gap range over the 54 cells: LCDM Delta %+.3f .. %+.3f ; D(worst B cell) %+.3f .. %+.3f, median %+.3f; min z_pair %.1f" % (
    min(g['delta'] for g in core), max(g['delta'] for g in core),
    min(g[g['cmin']]['D'] for g in core), max(g[g['cmin']]['D'] for g in core), np.median([g[g['cmin']]['D'] for g in core]),
    min(g[g['cmin']]['D'] / g[g['cmin']]['err_pair'] for g in core)))
print("axis marginals in the 54 cells (fraction with S_a | S_b_pair(worst B) | W_min):")
for ai, nm, levels in [(0, "m", [1 / 3, 1, 3]), (1, "tie", ["solved_salp", "solved_chab", "fixed_chab"]), (2, "z", ["z0", "full"]), (3, "c", ["duffy", "relaxed", "dm"])]:
    for lv in levels:
        sub = [g for g in core if g["axes"][ai] == lv]
        print(f"   {nm}={lv!s:12s} n={len(sub):2d}  S_a {frac(sub,'Sa'):.2f}  S_b {frac(sub,'Sb_min'):.2f}  W {frac(sub,'W_min'):.2f}   mean D(worst B) {np.mean([g[g['cmin']]['D'] for g in sub]):+.3f}  mean err_pair {np.mean([g[g['cmin']]['err_pair'] for g in sub]):.4f}")
Wfrac = frac(core, "W_min")
verdict = "ROBUST" if Wfrac >= 0.9 else ("CONDITIONAL" if Wfrac >= 0.5 else "NOT SUPPORTED")
print(f"VERDICT on 'B-specific statistically' (S_a and S_b(paired), worst B cell) over the 54 cells: {verdict} ({Wfrac:.3f})")
print(f"   S_b(paired) flips (fails) in {sum(1 for g in core if not g['Sb_min'])} of {len(core)} cells: " + "; ".join(f"{g['axes']}" for g in core if not g['Sb_min']))

# ============================================================== JSON + exit
def clean_g(g):
    out = {k: v for k, v in g.items() if k not in CELLS_B and k != "cmin"}
    out["axes"] = [str(a) for a in g["axes"]]
    for c in CELLS_B: out[NAMEB[c]] = g[c]
    out["cmin"] = NAMEB[g["cmin"]]
    return {k: (bool(v) if isinstance(v, (np.bool_,)) else v) for k, v in out.items()}
js = dict(mode=MODE, B={NAMEB[c]: {k: v for k, v in stB[c].items() if k != "bd"} for c in CELLS_B},
          kbar1_nu_mono={NAMEB[c]: kbar1[c] for c in CELLS_B}, kbar1_nu_rar={NAMEB[c]: kbar1_rar[c] for c in CELLS_B},
          lcdm_base={k: v for k, v in sbase.items() if k != "bd"}, pair_base={NAMEB[c]: pair_base[c] for c in CELLS_B},
          halo_free_gap=gap_off, variants={f"{k[0]}|{NAMEB[k[1]]}": v for k, v in varres.items()},
          grid=[clean_g(g) for g in grid], verdict=verdict, W_frac=Wfrac,
          repro=[dict(name=n, mine=m, target=t, diff=d, verdict=v) for n, m, t, d, v in REPRO], fails=FAILS)
json.dump(js, open(os.path.join(HERE, f"CFG87_results_{MODE}.json"), "w"), indent=1, default=float)
print(f"\nFAILED CHECKS ({len(FAILS)}):", FAILS)
print(f"total time {time.time()-T0:.0f}s")
sys.exit(1 if FAILS else 0)
