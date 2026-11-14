"""AGB1 Parts A and C (criteria: FROZEN_CRITERIA.md in this folder).

DESI DR2 BAO + DES-SN5YR Dovekie supernovae in a flat w0-wa background, with an amplitude A on the progenitor-age
correction template: mu_model(z) + M + A x T(z). A = 0 is the published moduli, A = 1 the Son et al. (2025) correction.

Usage: python3 agb1_run.py MODE [outdir]
  checks : KT, K1, K2, K4, K3a (twin, A_true = 1), K3b (twin, A_true = 0)   (twins exit 3 on pass, 4 on fail)
  Part A : A_full, A_des_only, A_rand197, A_bao_overlap
  report : W_full, W_des_only (template T_W), L_full (legacy offset)
  Part C : C_K5, C_full, C_des_only   (with DESI's compressed CMB prior; CAMB)
Each mode writes agb1_<MODE>.json and prints its log (redirect to agb1_<MODE>.out)."""
import json, os, sys, time
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")   # spurious Accelerate BLAS floating-point flags (the twins recover the truth to 1e-5)
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import agb1_template as TPL

REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DES5 = os.path.normpath(os.path.join(REPO, "..", "_external_data", "cfg684_inputs", "des5"))
MODE = sys.argv[1]
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE
C_KMS = 299792.458
SEED = 20261113

# ---------------- BAO (arXiv:2503.14738 tab:alphas; vector as closure_2026_11_13/NUF1 nuf1_run.py) ----------------
GAL = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459),
       ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
       ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416),
       ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
       ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500),
       ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = ("BGS", 0.295, 7.942, 0.075)
CMB_MU = np.array([0.01041, 0.02223, 0.14208])          # theta*, omega_b, omega_bc (arXiv:2503.14738 App. A)
CMB_COV = 1e-9*np.array([[0.006621, 0.12444, -1.1929],
                         [0.12444, 21.344, -94.001],
                         [-1.1929, -94.001, 1488.4]])
CMB_SD = np.sqrt(np.diag(CMB_COV)); CMB_CI = np.linalg.inv(CMB_COV)
MNU, ONU = 0.06, 0.06/93.14


class BAO:
    def __init__(s, which="all"):
        bins = GAL if which == "all" else [b for b in GAL if b[1] < 1.2]
        s.names = ["BGS"] + [b[0] for b in bins]
        s.zb = BGS[1]; s.za = np.array([b[1] for b in bins]); n = 1 + 2*len(bins)
        s.d = np.zeros(n); s.Ci = np.zeros((n, n)); s.d[0] = BGS[2]; s.Ci[0, 0] = 1/BGS[3]**2
        for i, (_, z, dm, sdm, dh, sdh, r) in enumerate(bins):
            C = np.array([[sdm**2, r*sdm*sdh], [r*sdm*sdh, sdh**2]])
            s.Ci[1 + 2*i:3 + 2*i, 1 + 2*i:3 + 2*i] = np.linalg.inv(C); s.d[1 + 2*i] = dm; s.d[2 + 2*i] = dh

    def vec(s, dmb, dhb, dma, dha):
        """Model vector from D_M, D_H at the BGS redshift and at the anisotropic redshifts (any common unit)."""
        m = np.empty(len(s.d)); m[0] = (s.zb*dmb**2*dhb)**(1/3); m[1::2] = dma; m[2::2] = dha
        return m

    def chi2_scale(s, m):
        """chi2 with the overall scale alpha = c/(H0 r_d) profiled; m in units of c/H0."""
        md = m@s.Ci@s.d; mm = m@s.Ci@m
        return float(s.d@s.Ci@s.d - md*md/mm), float(md/mm)

    def chi2_abs(s, m):
        r = s.d - m
        return float(r@s.Ci@r)


# ---------------- background (Part A: flat w0-wa, no radiation) ----------------
XG = np.linspace(0, np.log(3.4), 2401); ZG = np.expm1(XG); DXG = np.diff(XG)
ZQ = np.linspace(0, 2.33, 234)


def ez(z, om, w0, wa):
    a = 1.0/(1.0 + z)
    return np.sqrt(om*(1 + z)**3 + (1 - om)*a**(-3*(1 + w0 + wa))*np.exp(-3*wa*(1 - a)))


def dm_grid(om, w0, wa):
    f = (1 + ZG)/ez(ZG, om, w0, wa)
    return np.concatenate([[0.0], np.cumsum(0.5*(f[1:] + f[:-1])*DXG)])


def qz(z, om, w0, wa):
    a = 1.0/(1.0 + z); de = (1 - om)*a**(-3*(1 + w0 + wa))*np.exp(-3*wa*(1 - a)); m = om*(1 + z)**3
    return 0.5 + 1.5*(w0 + wa*(1 - a))*de/(m + de)


def in_bounds(om, w0, wa):
    return 0.05 < om < 0.7 and -3 <= w0 <= 1 and -3 <= wa <= 2 and w0 + wa < 0


def edge_flags(om, w0, wa):
    e = []
    if om < 0.051 or om > 0.699: e.append("Om")
    if w0 < -2.999 or w0 > 0.999: e.append("w0")
    if wa < -2.999 or wa > 1.999: e.append("wa")
    if w0 + wa > -1e-3: e.append("w0+wa")
    return e


# ---------------- supernovae (loader as CFG684 / the DES likelihood file) ----------------
class SN:
    def __init__(s, sample):
        rows = [l.split() for l in open(os.path.join(DES5, "DES-Dovekie_HD.csv")) if l.startswith("SN:")]
        ids = np.array([int(r[2]) for r in rows]); z = np.array([float(r[3]) for r in rows])
        zh = np.array([float(r[4]) for r in rows]); mu = np.array([float(r[5]) for r in rows])
        npz = np.load(os.path.join(DES5, "STAT+SYS.npz")); n = int(npz[npz.files[0]][0])
        W = np.zeros((n, n)); W[np.triu_indices(n)] = npz[npz.files[1]]; W = W + np.triu(W, 1).T
        sel = z > 0
        if sample == "des_only":
            sel &= ids == 10
        elif sample == "rand197":
            des = np.where(ids == 10)[0]
            drop = np.random.default_rng(SEED).choice(des, int((ids != 10).sum()), replace=False)
            sel[drop] = False
        elif sample != "full":
            raise ValueError(sample)
        if sel.all():
            s.W = W
        else:
            s.W = np.linalg.inv(np.linalg.inv(W)[np.ix_(sel, sel)])
        s.ids, s.z, s.zh, s.mu = ids[sel], z[sel], zh[sel], mu[sel]
        s.n = int(sel.sum()); s.n_des = int((s.ids == 10).sum()); s.sample = sample
        s.W1 = s.W@np.ones(s.n); s.s11 = float(s.W1.sum()); s.T = {}

    def add_template(s, name, vec):
        vec = np.asarray(vec, float)
        s.T[name] = (vec, s.W@vec - s.W1*(s.W1@vec)/s.s11)

    def chi2(s, zgrid, dmg, fixed, free):
        """chi2 with the offset M marginalised analytically; 'fixed' = {template: coefficient}; 'free' = templates whose
        coefficients are profiled analytically. Returns (chi2, {template: coefficient})."""
        r = s.mu - 5*np.log10((1 + s.zh)*np.interp(s.z, zgrid, dmg))
        for k, c in fixed.items():
            if c != 0.0: r = r - c*s.T[k][0]
        b1 = s.W1@r; base = float(r@(s.W@r) - b1*b1/s.s11)
        if not free: return base, {}
        b = np.array([s.T[k][1]@r for k in free]); G = np.array([[s.T[i][0]@s.T[j][1] for j in free] for i in free])
        c = np.linalg.solve(G, b)
        return float(base - b@c), {k: float(v) for k, v in zip(free, c)}


# ---------------- objectives ----------------
def obj_A(sn, bao, fixed, free, con, lam=0.0):
    """Part A objective. con: 'free' (x = Om, w0, wa), 'today' (x = Om, wa; q0 = 0), 'never' (penalty lam on min q < 0)."""
    def unpack(x):
        if con == "today": return float(x[0]), -1.0/(3.0*(1.0 - float(x[0]))), float(x[1])
        return float(x[0]), float(x[1]), float(x[2])

    def f(x, detail=False):
        om, w0, wa = unpack(x)
        if not in_bounds(om, w0, wa): return None if detail else 1e10
        dmg = dm_grid(om, w0, wa); cb, alpha, cs, coef = 0.0, np.nan, 0.0, {}
        if bao is not None:
            m = bao.vec(np.interp(bao.zb, ZG, dmg), 1/ez(bao.zb, om, w0, wa), np.interp(bao.za, ZG, dmg), 1/ez(bao.za, om, w0, wa))
            cb, alpha = bao.chi2_scale(m)
        if sn is not None: cs, coef = sn.chi2(ZG, dmg, fixed, free)
        q = qz(ZQ, om, w0, wa); qm = float(q.min())
        if not detail: return cb + cs + (lam*max(0.0, -qm)**2 if con == "never" else 0.0)
        out = dict(chi2=cb + cs, chi2_bao=cb, chi2_sn=cs, Om=om, w0=w0, wa=wa, q0=float(q[0]), qmin=qm,
                   z_qmin=float(ZQ[int(q.argmin())]), hrd=(C_KMS/100/alpha if alpha == alpha else None),
                   coef={**fixed, **coef}, edge=edge_flags(om, w0, wa), x3=[om, w0, wa])
        return out
    return f


_camb = None


def obj_C(sn, bao, fixed, free, con, lam=0.0, lcdm=False):
    """Part C objective (CAMB background + compressed CMB prior). x = (h, xb, xbc[, w0][, wa]) with omega_b = mean + 2 sd xb,
    omega_bc = mean + 2 sd xbc. con as obj_A; lcdm fixes w0 = -1, wa = 0."""
    global _camb
    if _camb is None:
        import camb as _c; _camb = _c
    camb = _camb
    zsn = np.expm1(np.linspace(0, np.log(2.2), 601))

    def unpack(x):
        h = float(x[0]); ob = CMB_MU[1] + 2*CMB_SD[1]*float(x[1]); obc = CMB_MU[2] + 2*CMB_SD[2]*float(x[2])
        om = (obc + ONU)/h**2
        if lcdm: return h, ob, obc, om, -1.0, 0.0
        if con == "today": return h, ob, obc, om, (-1.0/(3.0*(1.0 - om)) if om < 1 else 9.0), float(x[3])
        return h, ob, obc, om, float(x[3]), float(x[4])

    def f(x, detail=False):
        h, ob, obc, om, w0, wa = unpack(x)
        ok = 0.4 < h < 1.0 and ob > 0.005 and obc - ob > 0.01 and in_bounds(om, w0, wa)
        if not ok: return None if detail else 1e10
        try:
            P = camb.CAMBparams(); P.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
            P.set_cosmology(H0=100*h, ombh2=ob, omch2=obc - ob, mnu=MNU, num_massive_neutrinos=1, nnu=3.044, omk=0)
            P.WantTransfer = False; P.WantCls = False
            R = camb.get_background(P); d = R.get_derived_params()
            rd = d["rdrag"]; th = d["thetastar"]/100; cb = 0.0
            if bao is not None:
                zz = np.r_[bao.zb, bao.za]; DM = R.comoving_radial_distance(zz)/rd; DH = C_KMS/R.hubble_parameter(zz)/rd
                cb = bao.chi2_abs(bao.vec(DM[0], DH[0], DM[1:], DH[1:]))
            cs, coef = (0.0, {})
            if sn is not None:
                dms = R.comoving_radial_distance(zsn); dms[0] = 0.0
                cs, coef = sn.chi2(zsn, np.maximum(dms, 1e-30), fixed, free)
        except Exception:
            return None if detail else 1e10
        dv = np.array([th, ob, obc]) - CMB_MU; cp = float(dv@CMB_CI@dv)
        q = qz(ZQ, om, w0, wa); qm = float(q.min())
        if not detail: return cb + cs + cp + (lam*max(0.0, -qm)**2 if con == "never" else 0.0)
        return dict(chi2=cb + cs + cp, chi2_bao=cb, chi2_sn=cs, chi2_prior=cp, h=h, omega_b=ob, omega_bc=obc, Om=om,
                    w0=w0, wa=wa, q0=float(q[0]), qmin=qm, z_qmin=float(ZQ[int(q.argmin())]), rd=float(rd),
                    theta_star=float(th), coef={**fixed, **coef}, edge=edge_flags(om, w0, wa), x3=[om, w0, wa],
                    xc=[h, float(x[1]), float(x[2]), w0, wa])
    return f


# ---------------- minimiser ----------------
def nm(f, x0, step):
    x0 = np.array(x0, float); n = len(x0); best = None
    for scale, xa, fa in ((1.0, 1e-4, 1e-5), (0.3, 1e-5, 1e-6), (0.1, 1e-6, 1e-7)):
        xs = x0 if best is None else best.x
        sim = np.vstack([xs] + [xs + scale*step[i]*np.eye(n)[i] for i in range(n)])
        r = minimize(f, xs, method="Nelder-Mead", options=dict(initial_simplex=sim, xatol=xa, fatol=fa, maxiter=6000, maxfev=9000))
        if best is None or r.fun <= best.fun: best = r
    return best


START3 = [(0.31, -1.0, 0.0), (0.32, -0.8, -0.7), (0.35, -0.45, -1.7), (0.37, -0.3, -2.2)]
NEVER3 = [(0.30, -0.45, -0.01), (0.35, -0.50, -0.20), (0.40, -0.55, -0.01), (0.33, -0.48, -0.60)]
HSTART = [0.68, 0.67, 0.64, 0.63]
STEP3 = [0.02, 0.1, 0.3]


class Fitter:
    """Part 'A' or 'C' fits with a common interface. A fit returns the detail dict of the best point found."""
    def __init__(s, part, sn, bao):
        s.part, s.sn, s.bao, s.nfit = part, sn, bao, 0

    def _x(s, p3, con, xc=None):
        """Start vector from a (Om, w0, wa) triple (and, for Part C, the nuisance start xc = h, xb, xbc)."""
        om, w0, wa = p3
        if s.part == "A": return [om, wa] if con == "today" else [om, w0, wa]
        h, xb, xbc = xc if xc is not None else (0.68, 0.0, 0.0)
        return [h, xb, xbc, wa] if con == "today" else [h, xb, xbc, w0, wa]

    def _step(s, con):
        base = [] if s.part == "A" else [0.01, 0.3, 0.3]
        if s.part == "A": return [0.02, 0.3] if con == "today" else STEP3
        return base + ([0.3] if con == "today" else [0.1, 0.3])

    def fit(s, fixed, free, con="free", extra=(), fixed_starts=True):
        """extra: detail dicts of earlier fits used as additional starts; fixed_starts = False uses only those
        (Part C profile points, which are warm-started from the neighbouring point and the A-free fit)."""
        mk = obj_A if s.part == "A" else obj_C
        starts = []
        base = (NEVER3 if con == "never" else START3) if fixed_starts else []
        for i, p3 in enumerate(base):
            starts.append(s._x(p3, con, None if s.part == "A" else (HSTART[i], 0.0, 0.0)))
        for e in extra:
            if e is None: continue
            starts.append(s._x(e["x3"], con, None if s.part == "A" else e["xc"][:3]))
        best = None
        for x0 in starts:
            if con == "never":
                r = nm(mk(s.sn, s.bao, fixed, free, con, 1e6), x0, s._step(con))
                r = nm(mk(s.sn, s.bao, fixed, free, con, 1e8), r.x, [0.2*v for v in s._step(con)])
            else:
                r = nm(mk(s.sn, s.bao, fixed, free, con), x0, s._step(con))
            d = mk(s.sn, s.bao, fixed, free, con)(r.x, detail=True); s.nfit += 1
            if d is None: continue
            if con == "never" and d["qmin"] < -1e-3: continue
            if best is None or d["chi2"] < best["chi2"]: best = d
        if best is None: raise RuntimeError(f"no valid fit ({con}, fixed {fixed}, free {free})")
        best["con"] = con
        return best


def summarise(prof):
    As = np.array(sorted(prof)); cs = np.array([prof[a]["chi2"] for a in As])
    sp = CubicSpline(As, cs); fine = np.linspace(As[0], As[-1], 400001); cf = sp(fine)
    i = int(np.argmin(cf)); cmin = float(cf[i])

    def cross(level):
        g = lambda x: float(sp(x) - cmin - level); above = cf - cmin - level >= 0
        jl = np.where(above[:i])[0]; jr = np.where(above[i:])[0]
        lo = brentq(g, fine[jl[-1]], fine[jl[-1] + 1]) if len(jl) else None
        hi = brentq(g, fine[i + jr[0] - 1], fine[i + jr[0]]) if len(jr) else None
        return [lo, hi]
    return dict(A_spline=float(fine[i]), chi2_spline=cmin, at_grid_edge=bool(i == 0 or i == len(fine) - 1),
                ci68=cross(1.0), ci95=cross(4.0))


def run_block(F, tname, grid, forks, log, also_free=()):
    """A free; the A profile on 'grid'; and (forks) the q0 = 0 and never-accelerated fits for A = 0, A = 1 and A free."""
    also = list(also_free)
    free = F.fit({}, [tname] + also)
    log(f"  A free: A {free['coef'][tname]:+.4f}  chi2 {free['chi2']:.4f}  Om {free['Om']:.4f} w0 {free['w0']:+.4f} wa {free['wa']:+.4f}"
        f" q0 {free['q0']:+.4f}  edge {free['edge']}")
    prof, prev = {}, free
    for a in grid:
        r = F.fit({tname: a}, also, extra=(prev, free), fixed_starts=(F.part == "A")); prof[a] = r; prev = r
        log(f"  A {a:+.2f}  chi2 {r['chi2']:10.4f}  Om {r['Om']:.4f} w0 {r['w0']:+.4f} wa {r['wa']:+.4f} q0 {r['q0']:+.4f}  edge {r['edge']}")
    low = min(prof.values(), key=lambda r: r["chi2"])
    if low["chi2"] < free["chi2"] - 1e-7:             # the A-free fit must be the global minimum over A
        free = min([free, F.fit({}, [tname] + also, extra=(low,))], key=lambda r: r["chi2"])
        log(f"  A free re-fitted from the grid minimum: A {free['coef'][tname]:+.4f} chi2 {free['chi2']:.4f}")
    S = summarise(prof)
    S.update(A_free=free["coef"][tname], chi2_free=free["chi2"], D_A0=prof[0.0]["chi2"] - free["chi2"],
             D_A1=prof[1.0]["chi2"] - free["chi2"])
    log(f"  best A {S['A_free']:+.4f} (spline {S['A_spline']:+.4f})  68% {S['ci68']}  95% {S['ci95']}"
        f"  dchi2(A=0) {S['D_A0']:.3f}  dchi2(A=1) {S['D_A1']:.3f}")
    out = dict(free=free, profile={f"{a:+.2f}": v for a, v in prof.items()}, summary=S)
    if forks:
        fk = {}
        for name, fixed, fr, base in (("A0", {tname: 0.0}, also, prof[0.0]), ("A1", {tname: 1.0}, also, prof[1.0]),
                                      ("Afree", {}, [tname] + also, free)):
            today = F.fit(fixed, fr, "today", extra=(base,))
            never = F.fit(fixed, fr, "never", extra=(today, base))
            for c in (today, never):                  # a constrained fit can never beat the unconstrained one
                if c["chi2"] < base["chi2"] - 1e-7:
                    base = min([base, F.fit(fixed, fr, "free", extra=(c,))], key=lambda r: r["chi2"])
            fk[name] = dict(base=base, today=today, never=never, D_today=today["chi2"] - base["chi2"],
                            D_never=never["chi2"] - base["chi2"])
            log(f"  fork {name}: best chi2 {base['chi2']:.4f} Om {base['Om']:.4f} w0 {base['w0']:+.4f} wa {base['wa']:+.4f} q0 {base['q0']:+.4f}"
                f" (min q {base['qmin']:+.4f} at z {base['z_qmin']:.2f}) | q0=0: dchi2 {fk[name]['D_today']:.3f}"
                f" | never accelerated: dchi2 {fk[name]['D_never']:.3f} (Om {never['Om']:.4f} w0 {never['w0']:+.4f} wa {never['wa']:+.4f}"
                f" min q {never['qmin']:+.5f})")
        out["forks"] = fk
    return out


GRID_A = [round(x, 2) + 0.0 for x in np.arange(-1.0, 3.0001, 0.1)]
GRID_C = [round(x, 2) + 0.0 for x in np.arange(-1.0, 3.0001, 0.25)]
TRUTH = (0.31, -0.8, -0.6); HRD_TRUE = 101.6


def main():
    t0 = time.time(); log = lambda m: print(m, flush=True)
    res = dict(mode=MODE, numpy=np.__version__); code = 0
    log(f"AGB1 mode {MODE}")
    if MODE == "KT":
        zs = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.2]
        dS1, tS1, dW12 = float(TPL.dage(1.0, "S")), float(TPL.T(1.0, "S")), float(TPL.dage(1.2, "W"))
        ok = 5.0 <= dS1 <= 5.6 and 0.15 <= tS1 <= 0.17 and 1.7 <= dW12 <= 2.1
        res.update(age0_S=TPL.table("S")[3], age0_W=TPL.table("W")[3], z=zs, dage_S=[float(v) for v in TPL.dage(zs, "S")],
                   T_S=[float(v) for v in TPL.T(zs, "S")], dage_W=[float(v) for v in TPL.dage(zs, "W")],
                   T_W=[float(v) for v in TPL.T(zs, "W")], dage_S_1=dS1, T_S_1=tS1, dage_W_12=dW12,
                   dage_S_1_flat=float(TPL.dage(1.0, "S", (70.0, 0.3, -1.0, 0.0))), passed=bool(ok))
        log(f"KT: median age z=0: S {res['age0_S']:.2f} Gyr, W {res['age0_W']:.2f} Gyr")
        log("   z       " + " ".join(f"{z:6.2f}" for z in zs))
        log("   dage_S  " + " ".join(f"{v:6.2f}" for v in res["dage_S"]))
        log("   T_S     " + " ".join(f"{v:6.3f}" for v in res["T_S"]))
        log("   dage_W  " + " ".join(f"{v:6.2f}" for v in res["dage_W"]))
        log(f"KT: dage_S(1.0) {dS1:.3f} Gyr [5.0, 5.6]; T_S(1.0) {tS1:.4f} mag [0.15, 0.17]; dage_W(1.2) {dW12:.3f} Gyr [1.7, 2.1]"
            f" -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K1":
        bao = BAO("all")
        g = lambda om: obj_A(None, bao, {}, [], "free")([om, -1.0, 0.0])
        r = minimize_scalar(g, bounds=(0.2, 0.4), method="bounded", options=dict(xatol=1e-7))
        d = obj_A(None, bao, {}, [], "free")([r.x, -1.0, 0.0], detail=True)
        ok = abs(d["Om"] - 0.2975) <= 0.003 and abs(d["hrd"] - 101.54) <= 0.3
        res.update(Om=d["Om"], hrd=d["hrd"], chi2=d["chi2"], target=dict(Om=[0.2975, 0.0086], hrd=[101.54, 0.73]),
                   tol=dict(Om=0.003, hrd=0.3), passed=bool(ok))
        log(f"K1 BAO-only flat LCDM: Om {d['Om']:.4f} (DESI 0.2975 +- 0.0086)  h r_d {d['hrd']:.2f} Mpc (DESI 101.54 +- 0.73)"
            f"  chi2 {d['chi2']:.3f} -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K2":
        sn = SN("full")
        g = lambda om: obj_A(sn, None, {}, [], "free")([om, -1.0, 0.0])
        r = minimize_scalar(g, bounds=(0.15, 0.55), method="bounded", options=dict(xatol=1e-7))
        ok = abs(r.x - 0.330) <= 0.0075
        res.update(Om=float(r.x), chi2=float(r.fun), n_sn=sn.n, target=[0.330, 0.015], tol=0.0075, passed=bool(ok))
        log(f"K2 supernovae-only flat LCDM, full ({sn.n}): Om {r.x:.4f} (arXiv:2511.07517: 0.330 +- 0.015)  chi2 {r.fun:.2f}"
            f" -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K4":
        import camb
        om, w0, wa, h = 0.32, -0.8, -0.7, 0.68
        P = camb.CAMBparams(); P.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
        P.set_cosmology(H0=100*h, ombh2=0.02223, omch2=om*h*h - 0.02223, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, omk=0)
        P.WantTransfer = False; P.WantCls = False; R = camb.get_background(P)
        zs = np.array([0.5, 1.0, 2.33]); dmg = dm_grid(om, w0, wa)
        dm_c = R.comoving_radial_distance(zs)*100*h/C_KMS; dh_c = 100*h/R.hubble_parameter(zs)
        dm_o = np.interp(zs, ZG, dmg); dh_o = 1/ez(zs, om, w0, wa)
        rel = np.r_[dm_o/dm_c - 1, dh_o/dh_c - 1]; ok = bool(np.max(np.abs(rel)) <= 1e-3)
        res.update(z=zs.tolist(), rel_DM=(dm_o/dm_c - 1).tolist(), rel_DH=(dh_o/dh_c - 1).tolist(), camb=camb.__version__,
                   tol=1e-3, passed=ok)
        log(f"K4 integrator vs CAMB {camb.__version__} at z {zs.tolist()}: D_M rel {(dm_o/dm_c - 1).tolist()}  D_H rel {(dh_o/dh_c - 1).tolist()}"
            f" -> {'PASS' if ok else 'FAIL'}")
    elif MODE in ("K3a", "K3b"):
        a_true = 1.0 if MODE == "K3a" else 0.0
        sn = SN("full"); bao = BAO("all"); sn.add_template("age", TPL.T(sn.z, "S"))
        dmg = dm_grid(*TRUTH)
        sn.mu = 5*np.log10((1 + sn.zh)*np.interp(sn.z, ZG, dmg)) + a_true*sn.T["age"][0]
        alpha = C_KMS/100/HRD_TRUE
        bao.d = alpha*bao.vec(np.interp(bao.zb, ZG, dmg), 1/ez(bao.zb, *TRUTH), np.interp(bao.za, ZG, dmg), 1/ez(bao.za, *TRUTH))
        log(f"mutation twin: supernova and BAO vectors replaced by the model at (Om, w0, wa) = {TRUTH}, h r_d = {HRD_TRUE},"
            f" plus {a_true} x T_S; covariances unchanged; no noise")
        F = Fitter("A", sn, bao); free = F.fit({}, ["age"]); f0 = F.fit({"age": 0.0}, [], extra=(free,)); f1 = F.fit({"age": 1.0}, [], extra=(free,))
        wrong = (f0 if a_true == 1.0 else f1)["chi2"] - free["chi2"]
        ok = (abs(free["coef"]["age"] - a_true) <= 0.01 and abs(free["w0"] + 0.8) <= 0.01 and abs(free["wa"] + 0.6) <= 0.05
              and free["chi2"] <= 1e-3 and wrong > 0)
        res.update(A_true=a_true, free=free, at_A0=f0, at_A1=f1, D_wrong=wrong, passed=bool(ok))
        log(f"{MODE}: A free {free['coef']['age']:+.5f} (truth {a_true})  w0 {free['w0']:+.5f} wa {free['wa']:+.5f} Om {free['Om']:.5f}"
            f" h r_d {free['hrd']:.3f}  chi2_min {free['chi2']:.2e}  dchi2 at the wrong amplitude {wrong:.3f} -> {'PASS' if ok else 'FAIL'}")
        code = 3 if ok else 4
    elif MODE.startswith(("A_", "W_", "L_")):
        kind, sample = MODE[0], MODE[2:]
        bao = BAO("overlap" if sample == "bao_overlap" else "all")
        sn = SN("full" if sample == "bao_overlap" else sample)
        sn.add_template("age", TPL.T(sn.z, "W" if kind == "W" else "S"))
        log(f"sample {sn.sample}: {sn.n} supernovae ({sn.n_des} DES, {sn.n - sn.n_des} legacy); BAO bins {bao.names};"
            f" template T_{'W' if kind == 'W' else 'S'}")
        F = Fitter("A", sn, bao)
        res.update(sample=sample, n_sn=sn.n, n_des=sn.n_des, bao=bao.names, template="W" if kind == "W" else "S")
        if kind == "L":
            sn.add_template("step", (sn.ids != 10).astype(float))
            d0 = F.fit({"age": 0.0, "step": 0.0}, []); d1 = F.fit({"age": 0.0}, ["step"], extra=(d0,))
            log(f"  legacy offset alone (A = 0): delta {d1['coef']['step']:+.4f} mag  dchi2(delta = 0) {d0['chi2'] - d1['chi2']:.3f}"
                f"  Om {d1['Om']:.4f} w0 {d1['w0']:+.4f} wa {d1['wa']:+.4f} q0 {d1['q0']:+.4f}")
            res.update(step_only=dict(no_step=d0, step=d1, delta=d1["coef"]["step"], D_delta0=d0["chi2"] - d1["chi2"]))
            log("  age amplitude with the legacy offset free:")
            blk = run_block(F, "age", GRID_A, False, log, also_free=["step"])
            blk["delta_at_A_free"] = blk["free"]["coef"]["step"]; res.update(blk)
        else:
            res.update(run_block(F, "age", GRID_A, kind == "A" and sample != "rand197", log))
            if kind == "W":
                f023 = F.fit({"age": 0.23}, [], extra=(res["free"],))
                res["summary"]["D_A023"] = f023["chi2"] - res["summary"]["chi2_free"]
                log(f"  dchi2(A_W = 0.23) {res['summary']['D_A023']:.3f}")
    elif MODE == "C_K5":
        bao = BAO("all")
        fl = obj_C(None, bao, {}, [], "free", lcdm=True); best_l = None
        for h0 in (0.68, 0.67):
            r = nm(fl, [h0, 0.0, 0.0], [0.01, 0.3, 0.3])
            if best_l is None or r.fun < best_l.fun: best_l = r
        F = Fitter("C", None, bao); ww = F.fit({}, [])
        d = ww["chi2"] - float(best_l.fun); ok = abs(d + 8.0) <= 1.0
        res.update(chi2_lcdm=float(best_l.fun), w0wa=ww, dchi2=d, target=-8.0, tol=1.0, passed=bool(ok))
        log(f"K5 BAO + compressed CMB prior: chi2 LCDM {best_l.fun:.3f}  w0wa {ww['chi2']:.3f} (w0 {ww['w0']:+.3f} wa {ww['wa']:+.3f}"
            f" q0 {ww['q0']:+.3f} Om {ww['Om']:.4f} h {ww['h']:.4f})  dchi2 {d:+.2f} (DESI -8.0) -> {'PASS' if ok else 'FAIL'}")
    elif MODE.startswith("C_"):
        sample = MODE[2:]; bao = BAO("all"); sn = SN(sample); sn.add_template("age", TPL.T(sn.z, "S"))
        log(f"Part C, sample {sample}: {sn.n} supernovae ({sn.n_des} DES); BAO {bao.names}; compressed CMB prior; template T_S")
        F = Fitter("C", sn, bao)
        res.update(sample=sample, n_sn=sn.n, n_des=sn.n_des, bao=bao.names, template="S")
        res.update(run_block(F, "age", GRID_C, True, log))
    else:
        raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUTDIR, f"agb1_{MODE}.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log(f"wrote agb1_{MODE}.json  ({res['seconds']} s)  exit {code}")
    sys.exit(code)


if __name__ == "__main__":
    main()
