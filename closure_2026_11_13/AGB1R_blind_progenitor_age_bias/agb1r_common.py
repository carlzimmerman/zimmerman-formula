"""AGB1R common code: data, age templates, Part A (flat w0-wa, no radiation) and Part C (CAMB + compressed CMB prior).
Written from scratch for the blind re-grade of AGB1; follows READING.md in this folder."""
import os, json, warnings
import numpy as np
# Apple Accelerate BLAS raises spurious FP flags in matmul (numpy 1.26); results checked finite and equal to einsum.
warnings.filterwarnings("ignore", message=".*encountered in matmul")
from scipy.optimize import minimize
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_simpson

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DES_DIR = os.path.abspath(os.path.join(ROOT, "..", "_external_data", "cfg684_inputs", "des5"))
C_KMS = 299792.458
GYR_PER_INVH0 = 977.792221  # 1/(1 km/s/Mpc) in Gyr

# ---------------- DESI DR2 BAO (copied from nuf1_run.py, arXiv:2503.14738 tab:alphas) ----------------
GAL = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459),
       ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
       ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416),
       ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
       ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500),
       ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = ("BGS", 0.295, 7.942, 0.075)
# compressed CMB prior (theta* rad, omega_b, omega_bc), arXiv:2503.14738 App. A (copied from nuf1_run.py)
CMB_MU = np.array([0.01041, 0.02223, 0.14208])
CMB_COV = 1e-9*np.array([[0.006621, 0.12444, -1.1929],
                         [0.12444, 21.344, -94.001],
                         [-1.1929, -94.001, 1488.4]])
CMB_ICOV = np.linalg.inv(CMB_COV)


class BAO:
    """BAO data vector with block-diagonal covariance. use: 'all' or 'overlap' (BGS, LRG1, LRG2, LRG3+ELG1)."""
    def __init__(self, use="all", override=None):
        bins = GAL if use == "all" else [b for b in GAL if b[1] < 1.2]
        self.bins = bins
        self.zg = np.array([b[1] for b in bins])
        d = []; blocks = []
        for b in bins:
            d += [b[2], b[4]]
            C = np.array([[b[3]**2, b[6]*b[3]*b[5]], [b[6]*b[3]*b[5], b[5]**2]])
            blocks.append(np.linalg.inv(C))
        d.append(BGS[2])
        n = len(d); Wi = np.zeros((n, n))
        for i, B in enumerate(blocks): Wi[2*i:2*i+2, 2*i:2*i+2] = B
        Wi[-1, -1] = 1/BGS[3]**2
        self.d = np.array(d) if override is None else np.array(override)
        self.W = Wi
        self.zall = np.r_[self.zg, BGS[1]]

    def model_vec(self, DM, DH, DMb, DHb):
        """DM, DH at the galaxy/Lya bins; DMb, DHb at BGS. Any common unit (e.g. /r_d or c/H0)."""
        v = np.empty(len(self.d))
        v[0:-1:2] = DM; v[1:-1:2] = DH
        v[-1] = (BGS[1]*DMb**2*DHb)**(1/3)
        return v

    def chi2_fixed(self, m):
        r = self.d - m; return float(r @ self.W @ r)

    def chi2_profile_scale(self, m):
        """m in units of c/H0; profile s = c/(H0 r_d) linearly. Returns chi2, s."""
        Wm = self.W @ m
        s = float(Wm @ self.d)/float(Wm @ m)
        r = self.d - s*m
        return float(r @ self.W @ r), s


# ---------------- supernovae ----------------
def load_des():
    rows = []
    with open(os.path.join(DES_DIR, "DES-Dovekie_HD.csv")) as f:
        for line in f:
            if line.startswith("SN:"):
                p = line.split()
                rows.append((p[1], int(p[2]), float(p[3]), float(p[4]), float(p[5]), float(p[6])))
    cid = np.array([r[0] for r in rows]); ids = np.array([r[1] for r in rows])
    zhd = np.array([r[2] for r in rows]); zhel = np.array([r[3] for r in rows]); mu = np.array([r[4] for r in rows])
    d = np.load(os.path.join(DES_DIR, "STAT+SYS.npz"))
    n = int(d["nsn"][0]); W = np.zeros((n, n)); W[np.triu_indices(n)] = d["cov"]
    il = np.tril_indices(n, -1); W[il] = W.T[il]
    assert n == len(zhd)
    return dict(cid=cid, ids=ids, zhd=zhd, zhel=zhel, mu=mu, W=W)


def sample_keep(D, name):
    ids = D["ids"]; n = len(ids)
    if name in ("full", "bao_overlap"): return np.arange(n)
    if name == "des_only": return np.where(ids == 10)[0]
    if name == "rand197":
        des = np.where(ids == 10)[0]
        drop = np.random.default_rng(20261113).choice(des, 197, replace=False)
        return np.setdiff1d(np.arange(n), drop)
    raise ValueError(name)


class SN:
    """Supernova block: mu_th + M + A*T with M (and A when free) profiled analytically."""
    def __init__(self, D, keep, T, mu_override=None):
        self.z = D["zhd"][keep]; self.zhel = D["zhel"][keep]
        self.mu = (D["mu"] if mu_override is None else mu_override)[keep]
        if len(keep) == len(D["zhd"]): self.W = D["W"].copy()
        else:
            C = np.linalg.inv(D["W"]); Cs = C[np.ix_(keep, keep)]
            self.W = np.linalg.inv(Cs); self.W = 0.5*(self.W + self.W.T)
        self.set_template(T)

    def set_template(self, T):
        """T: array at the kept rows (mag per unit A)."""
        self.T = np.asarray(T, float)
        one = np.ones(len(self.z))
        self.W1 = self.W @ one; self.WT = self.W @ self.T
        self.a11 = float(one @ self.W1); self.a1T = float(one @ self.WT); self.aTT = float(self.T @ self.WT)

    def chi2(self, muth, A=None):
        """Returns chi2, A_used, M."""
        r = self.mu - muth
        Wr = self.W @ r
        rWr = float(r @ Wr); b1 = float(self.W1 @ r); bT = float(self.WT @ r)
        if A is None:
            M = np.array([[self.a11, self.a1T], [self.a1T, self.aTT]]); v = np.array([b1, bT])
            sol = np.linalg.solve(M, v)
            return rWr - float(v @ sol), float(sol[1]), float(sol[0])
        rr = rWr - 2*A*bT + A*A*self.aTT
        bb = b1 - A*self.a1T
        return rr - bb*bb/self.a11, float(A), bb/self.a11


# ---------------- flat w0-wa background without radiation ----------------
def fde(z, w0, wa):
    return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))

def E2(z, Om, w0, wa):
    return Om*(1+z)**3 + (1-Om)*fde(z, w0, wa)

def qz(z, Om, w0, wa):
    w = w0 + wa*z/(1+z)
    ode = (1-Om)*fde(z, w0, wa)/E2(z, Om, w0, wa)
    return 0.5 + 1.5*w*ode

def q0(Om, w0): return 0.5 + 1.5*w0*(1-Om)


class Dist:
    """D_M in units of c/H0 by cumulative Simpson on a uniform grid; cubic Hermite (exact slopes 1/E) to targets."""
    def __init__(self, ztargets, zmax=2.4, dz=2.5e-4):
        self.zg = np.arange(0.0, zmax + dz/2, dz); self.dz = dz
        zt = np.asarray(ztargets, float)
        k = np.minimum((zt/dz).astype(int), len(self.zg) - 2)
        t = (zt - self.zg[k])/dz
        self.k = k; self.t = t
        self.h00 = 2*t**3 - 3*t**2 + 1; self.h10 = t**3 - 2*t**2 + t
        self.h01 = -2*t**3 + 3*t**2; self.h11 = t**3 - t**2

    def DM(self, Om, w0, wa):
        f = 1/np.sqrt(E2(self.zg, Om, w0, wa))
        I = cumulative_simpson(f, dx=self.dz, initial=0.0)
        k = self.k; d = self.dz
        return self.h00*I[k] + self.h10*d*f[k] + self.h01*I[k+1] + self.h11*d*f[k+1]


# ---------------- age templates ----------------
def sfh_behroozi(z):
    with np.errstate(over="ignore"):
        return 1/(10**(-0.997*(z - 1.243)) + 10**(0.241*(z - 1.243)))
def sfh_md14(z): return 0.015*(1+z)**2.7/(1 + ((1+z)/2.9)**5.6)
def dtd_childress(tau, tp=0.3, al=20.0, s=-1.0):
    x = tau/tp; return x**al/(x**(al - s) + 1)
def dtd_powerlaw(tau, slope=-1.13, tmin=0.04): return np.where(tau >= tmin, tau**slope, 0.0)

BG_T = dict(H0=63.6, Om=0.353, w0=-0.42, wa=-1.75)

def cosmic_time_table(H0, Om, w0, wa):
    """t(z) in Gyr on a grid in x = ln(1+z) up to z 1e4, with the matter-only tail added analytically."""
    x = np.linspace(0, np.log(1 + 1e4), 200001)
    z = np.expm1(x)
    Hinv = GYR_PER_INVH0/H0/np.sqrt(E2(z, Om, w0, wa))
    cum = cumulative_simpson(Hinv[::-1], dx=x[1] - x[0], initial=0.0)[::-1]   # integral from x to x_max
    tail = (2/3)*GYR_PER_INVH0/H0/np.sqrt(Om)*np.exp(-1.5*x[-1])
    return z, cum + tail

def median_age(zobs, sfh, dtd, ztab, ttab, ntau=40000):
    t_obs = np.interp(zobs, ztab, ttab)
    lt = np.linspace(np.log(1e-4), np.log(t_obs*(1 - 1e-10)), ntau); tau = np.exp(lt)
    tform = t_obs - tau
    # z_form from t: ttab decreasing in z
    zf = np.interp(tform, ttab[::-1], ztab[::-1])
    w = sfh(zf)*dtd(tau)*tau          # weight per d ln tau
    cdf = cumulative_simpson(w, dx=lt[1] - lt[0], initial=0.0); cdf /= cdf[-1]
    return float(np.exp(np.interp(0.5, cdf, lt)))

def build_template(kind="S", zmax=2.4, dz=0.01, bg=BG_T, slope=0.030):
    ztab, ttab = cosmic_time_table(**bg)
    sfh, dtd = (sfh_behroozi, dtd_childress) if kind == "S" else (sfh_md14, dtd_powerlaw)
    zg = np.round(np.arange(0, zmax + dz/2, dz), 10)
    ages = np.array([median_age(z, sfh, dtd, ztab, ttab) for z in zg])
    dage = ages[0] - ages
    return dict(z=zg, age=ages, dage=dage, T=slope*dage, spline=CubicSpline(zg, slope*dage))


# ---------------- minimiser ----------------
STARTS_A = [(0.31, -1.0, 0.0), (0.32, -0.8, -0.7), (0.35, -0.45, -1.7), (0.37, -0.3, -2.2)]

def in_box(Om, w0, wa):
    return (0.05 < Om < 0.7) and (-3 <= w0 <= 1) and (-3 <= wa <= 2) and (w0 + wa < 0)

def at_edge(Om, w0, wa):
    e = []
    if Om - 0.05 < 0.003 or 0.7 - Om < 0.003: e.append("Om")
    if w0 + 3 < 0.01 or 1 - w0 < 0.01: e.append("w0")
    if wa + 3 < 0.01 or 2 - wa < 0.01: e.append("wa")
    if -(w0 + wa) < 0.01: e.append("w0+wa")
    return e

def nm(f, x0, steps, xatol=1e-7, fatol=1e-8, maxiter=20000):
    x0 = np.asarray(x0, float); n = len(x0)
    sim = np.vstack([x0] + [x0 + np.eye(n)[i]*steps[i] for i in range(n)])
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(initial_simplex=sim, xatol=xatol, fatol=fatol, maxiter=maxiter, maxfev=maxiter*2))
    return r.x, float(r.fun)

def nm_polished(f, x0, steps):
    x, v = nm(f, x0, steps)
    x2, v2 = nm(f, x, [s*0.3 for s in steps])
    return (x2, v2) if v2 <= v else (x, v)


# ---------------- Part A model ----------------
class PartA:
    def __init__(self, sn, bao):
        self.sn = sn; self.bao = bao
        zs = np.array([]) if sn is None else sn.z
        zb = np.array([]) if bao is None else bao.zall
        self.dist = Dist(np.r_[zs, zb])
        self.nsn = len(zs)

    def eval(self, Om, w0, wa, A=None):
        """Returns dict with chi2, chi2_sn, chi2_bao, A, s (BAO scale c/(H0 r_d)), M."""
        if self.sn is None:
            DMall = self.dist.DM(Om, w0, wa); csn, Au, M = 0.0, A, None
        else:
            DMall = self.dist.DM(Om, w0, wa)
            muth = 5*np.log10((1 + self.sn.zhel)*DMall[:self.nsn])
            csn, Au, M = self.sn.chi2(muth, A)
        if self.bao is not None:
            DMb = DMall[self.nsn:]; zb = self.bao.zall
            DH = 1/np.sqrt(E2(zb, Om, w0, wa))
            m = self.bao.model_vec(DMb[:-1], DH[:-1], DMb[-1], DH[-1])
            cb, s = self.bao.chi2_profile_scale(m)
        else:
            cb, s = 0.0, None
        return dict(chi2=csn + cb, chi2_sn=csn, chi2_bao=cb, A=Au, s=s, M=M)


QZ = np.round(np.arange(0, 2.33 + 1e-9, 0.005), 6)
if QZ[-1] < 2.33: QZ = np.r_[QZ, 2.33]

def minq(Om, w0, wa):
    q = qz(QZ, Om, w0, wa); i = int(np.argmin(q)); return float(q[i]), float(QZ[i])


def fit_A(model, A, mode="free", extra_starts=(), lam=None):
    """mode: 'free' (Om,w0,wa), 'q0' (w0 tied), 'never' (penalty). A: number or None (profiled). Returns record."""
    if mode == "q0":
        def unpack(x): Om, wa = x; return Om, -1/(3*(1 - Om)), wa
        starts = [(s[0], s[2]) for s in STARTS_A] + [(e[0], e[2]) for e in extra_starts]
        steps = [0.02, 0.3]
    else:
        def unpack(x): return tuple(x)
        starts = list(STARTS_A) + [tuple(e) for e in extra_starts]
        steps = [0.02, 0.1, 0.3]

    def base(x):
        Om, w0, wa = unpack(x)
        if not in_box(Om, w0, wa): return 1e10
        return model.eval(Om, w0, wa, A)["chi2"]

    best = None
    for s0 in starts:
        if mode == "never":
            x = np.array(s0, float)
            for L in (1e2, 1e4, 1e6, 1e8):
                def f(xx, L=L):
                    v = base(xx)
                    if v >= 1e10: return v
                    mq = minq(*unpack(xx))[0]
                    return v + L*max(0.0, -mq)**2
                x, _ = nm_polished(f, x, steps)
            v = base(x)
            if minq(*unpack(x))[0] < -1e-3: v_rank = v + 1e6
            else: v_rank = v
        else:
            x, v = nm_polished(base, s0, steps); v_rank = v
        if best is None or v_rank < best[2]: best = (x, v, v_rank)
    x, v, _ = best
    Om, w0, wa = unpack(x)
    r = model.eval(Om, w0, wa, A)
    mq, zq = minq(Om, w0, wa)
    rec = dict(Om=float(Om), w0=float(w0), wa=float(wa), q0=float(q0(Om, w0)), chi2=r["chi2"], chi2_sn=r["chi2_sn"],
               chi2_bao=r["chi2_bao"], A=r["A"], hrd=(C_KMS/(100*r["s"]) if r["s"] else None),
               minq=mq, z_minq=zq, edge=at_edge(Om, w0, wa))
    if mode == "never": rec["constraint_met"] = bool(mq >= -1e-3)
    return rec


def a_profile(model, grid, log=print):
    """Two sweeps (up, down), each with the neighbour's best fit as a fifth start; keep the lower."""
    up = {}; prev = None
    for A in grid:
        rec = fit_A(model, A, "free", extra_starts=[] if prev is None else [(prev["Om"], prev["w0"], prev["wa"])])
        up[A] = rec; prev = rec
    dn = {}; prev = None
    for A in grid[::-1]:
        rec = fit_A(model, A, "free", extra_starts=[] if prev is None else [(prev["Om"], prev["w0"], prev["wa"])])
        dn[A] = rec; prev = rec
    out = {}
    for A in grid:
        out[A] = up[A] if up[A]["chi2"] <= dn[A]["chi2"] else dn[A]
        out[A]["sweep_diff"] = abs(up[A]["chi2"] - dn[A]["chi2"])
        log(f"  A {A:+.2f}  chi2 {out[A]['chi2']:.4f}  Om {out[A]['Om']:.4f} w0 {out[A]['w0']:+.4f} wa {out[A]['wa']:+.4f}"
            f"  (sweeps differ {out[A]['sweep_diff']:.2e})")
    return out


def intervals(grid, chis, chi_min, A_best, levels=(1.0, 4.0)):
    """Crossings of chi_min + level by a cubic spline through the grid profile (A_best point included)."""
    g = np.array(grid, float); c = np.array(chis, float)
    if np.all(np.abs(g - A_best) > 1e-6):
        g = np.r_[g, A_best]; c = np.r_[c, chi_min]; o = np.argsort(g); g, c = g[o], c[o]
    sp = CubicSpline(g, c)
    fine = np.linspace(g[0], g[-1], 400001); cf = sp(fine)
    res = {}
    for L in levels:
        inside = cf - chi_min <= L
        idx = np.where(inside)[0]
        if len(idx) == 0: res[L] = None; continue
        lo = fine[idx[0]] if idx[0] > 0 else None
        hi = fine[idx[-1]] if idx[-1] < len(fine) - 1 else None
        res[L] = [None if lo is None else float(lo), None if hi is None else float(hi)]
    i = int(np.argmin(cf))
    return res, float(fine[i]), float(cf[i])


def w1_word(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"

def w2_word(q0best, dtoday):
    if q0best < 0 and dtoday >= 4: return "ACCELERATING TODAY"
    if q0best > 0 and dtoday >= 4: return "DECELERATING TODAY"
    return "SIGN NOT SETTLED"

def w3_word(dnever):
    if dnever >= 9: return "NEVER-ACCELERATED EXCLUDED AT 3 SIGMA"
    if dnever >= 4: return "NEVER-ACCELERATED DISFAVOURED"
    return "NEVER-ACCELERATED ALLOWED"


def dump(obj, path):
    def conv(o):
        if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [conv(v) for v in o]
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, np.ndarray): return conv(o.tolist())
        return o
    with open(path, "w") as f: json.dump(conv(obj), f, indent=1)
