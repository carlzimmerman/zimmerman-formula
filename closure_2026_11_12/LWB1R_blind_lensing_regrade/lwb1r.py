"""LWB1R: blind re-grade of LWB1 (DESI DR1 Lensing Without Borders Delta Sigma + wp amplitude).
Own code, written from LWB1's FROZEN_CRITERIA.md and this lane's READING.md only. Inputs read from disk (shared with LWB1):
the DESI DR1 release vectors/covariances, BX1's stored pair-A splice spectrum, CO1's stored R_tot, KL1's stored sigma8/Omega_m.
Usage: nice -n 19 python3 lwb1r.py [--mutate MU1]   ->  lwb1r.json / lwb1r_MUTATE_MU1.json (paths relative to this file)
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time
import numpy as np
from scipy.integrate import quad, cumulative_trapezoid
from scipy.interpolate import CubicSpline
from scipy.optimize import least_squares, brentq
from scipy.special import gamma as Gam
from multiprocessing import Pool
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
DATA = os.path.abspath(os.path.join(REPO, '..', '_external_data', 'desi_dr1_lensing', 'extracted'))
MUT = sys.argv[sys.argv.index('--mutate') + 1] if '--mutate' in sys.argv else None
NPROC = 4
RHO_CRIT = 2.775e11            # h^2 Msun Mpc^-3
SIG8_REF = 0.811

# ---------------------------------------------------------------- linear spectrum (EH98 no-wiggle, own code)
H0P = dict(h=0.6736, ob=0.02237, oc=0.1200, ns=0.965)
def T_nw(k, h, ob, oc):
    """Eisenstein & Hu 1998 zero-baryon-shape transfer (eqs 26, 28-31); k in h/Mpc."""
    wm = ob + oc; fb = ob / wm; Om = wm / h**2
    s = 44.5 * np.log(9.83 / wm) / np.sqrt(1.0 + 10.0 * ob**0.75)          # Mpc
    a = 1.0 - 0.328 * np.log(431.0 * wm) * fb + 0.38 * np.log(22.3 * wm) * fb**2
    kmpc = k * h
    G = Om * h * (a + (1.0 - a) / (1.0 + (0.43 * kmpc * s)**4))
    q = k * (2.7255 / 2.7)**2 / G
    L = np.log(2.0 * np.e + 1.8 * q); C = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L / (L + C * q * q)
def W_th(x):
    x = np.asarray(x, float); out = np.ones_like(x); m = x > 1e-4
    xm = x[m]; out[m] = 3.0 * (np.sin(xm) - xm * np.cos(xm)) / xm**3
    return out
def sigma_R(k, P, R=8.0):
    lk = np.log(k)
    return math.sqrt(np.trapz(P * W_th(k * R)**2 * k**3, lk) / (2 * math.pi**2))
KK = np.logspace(-5, 4, 9001)
P_LIN0 = KK**H0P['ns'] * T_nw(KK, H0P['h'], H0P['ob'], H0P['oc'])**2
P_LIN0 *= (SIG8_REF / sigma_R(KK, P_LIN0))**2

def growth_fns(Om):
    E = lambda a: math.sqrt(Om / a**3 + 1.0 - Om)
    g = lambda a: E(a) * quad(lambda u: 1.0 / (u * E(u))**3, 0.0, a, epsabs=0, epsrel=1e-10)[0]
    g1 = g(1.0)
    D = lambda z: g(1.0 / (1.0 + z)) / g1
    def f(z, e=1e-4):
        a = 1.0 / (1.0 + z)
        return (math.log(g(a * (1 + e))) - math.log(g(a * (1 - e)))) / (math.log(1 + e) - math.log(1 - e))
    return D, f

# ---------------------------------------------------------------- stored inputs (shared with LWB1)
SPL = json.load(open(os.path.join(REPO, 'closure_2026_11_10/BX1_fixed_amplitude_reference/bx1_splice_pairA_N512.json')))
CO1 = json.load(open(os.path.join(REPO, 'closure_2026_11_09/CO1_form_b_cosmology_computed/co1_hm.json')))
KL1 = json.load(open(os.path.join(REPO, 'closure_2026_11_10/KL1_lensing_amplitude_survey_assumptions/kl1_nu.json')))
FOOT = {f: dict(s8=KL1['A1'][f]['sigma8_nu'], Om=KL1['A1'][f]['Omega_m'], pars=KL1['A1'][f]['pars']) for f in ('canonical', 'alt')}
NODES = [(0.0, 'z0'), (0.5, 'z0.5'), (1.0, 'z1')]
KN = np.array(SPL['snap']['z0']['k'])
def lnN_nodes():
    out = []
    for z, key in NODES:
        s = SPL['snap'][key]
        Pl = np.interp(np.log(KN), np.log(KK), P_LIN0) * s['D']**2
        out.append(np.log(np.array(s['P']) / Pl))
    return np.array(out)
LNN = lnN_nodes()
def N_of(k, z, tail='const'):
    zs = np.array([n[0] for n in NODES])
    j = min(max(np.searchsorted(zs, z) - 1, 0), len(zs) - 2)
    w = (z - zs[j]) / (zs[j + 1] - zs[j])
    ln = (1 - w) * LNN[j] + w * LNN[j + 1]
    out = np.exp(np.interp(np.log(k), np.log(KN), ln))
    out[k < KN[0]] = 1.0
    if tail == 'zero':
        hi = k > KN[-1]                  # tail removed smoothly (a hard cut rings in the sine transform)
        out[hi] = out[hi] * np.exp(-((k[hi] / KN[-1])**2 - 1.0) * 4.0)
    return out
def Rtot(k, foot):
    kc = np.array(CO1['k']); R = np.array(CO1['primary'][foot]['R_tot'])
    out = np.interp(np.log(k), np.log(kc), R); out[(k < kc[0]) | (k > kc[-1])] = 1.0
    return out
def P_formB(z, foot, variant='primary'):
    """P_B(k, z) at the footing's target sigma8 (s = 1)."""
    D, _ = growth_fns(FOOT[foot]['Om'])
    amp = (FOOT[foot]['s8'] / SIG8_REF)**2 * D(z)**2
    if variant == 'N1':
        return amp * P_LIN0 * Rtot(KK, foot)
    return amp * P_LIN0 * N_of(KK, z, 'zero' if variant == 'Ntail0' else 'const') * Rtot(KK, foot)

_CAMB = {}
def camb_nl(pars, zs, mnu=0.06):
    import camb
    p = camb.CAMBparams()
    p.set_cosmology(H0=100 * pars['h'], ombh2=pars['ob'], omch2=pars['oc'], mnu=mnu, tau=pars.get('tau', 0.0544))
    p.InitPower.set_params(As=math.exp(pars['lnA']) * 1e-10, ns=pars['ns'])
    p.set_matter_power(redshifts=sorted(set(list(zs) + [0.0]), reverse=True), kmax=50.0)
    p.NonLinear = camb.model.NonLinear_both
    p.NonLinearModel.set_params(halofit_version='takahashi')
    r = camb.get_results(p)
    kh, zz, Pnl = r.get_matter_power_spectrum(minkh=1e-4, maxkh=40.0, npoints=800)
    s8 = float(r.get_sigma8_0())
    Om = (pars['ob'] + pars['oc'] + mnu / 93.14) / pars['h']**2
    out = {}
    for z in zs:
        i = int(np.argmin(abs(np.array(zz) - z)))
        lp = np.interp(np.log(KK), np.log(kh), np.log(Pnl[i]))
        # power-law extrapolation outside CAMB's range
        lo = KK < kh[0]; hi = KK > kh[-1]
        slo = (math.log(Pnl[i][1]) - math.log(Pnl[i][0])) / (math.log(kh[1]) - math.log(kh[0]))
        shi = (math.log(Pnl[i][-1]) - math.log(Pnl[i][-2])) / (math.log(kh[-1]) - math.log(kh[-2]))
        lp[lo] = math.log(Pnl[i][0]) + slo * (np.log(KK[lo]) - math.log(kh[0]))
        lp[hi] = math.log(Pnl[i][-1]) + shi * (np.log(KK[hi]) - math.log(kh[-1]))
        out[z] = np.exp(lp)
    return out, s8, Om

# ---------------------------------------------------------------- projections (own code)
RG = np.logspace(-3, 4.3, 900)          # xi grid for real spectra
RG_PL = np.logspace(-3, 5.3, 1000)      # power-law test grid
_LK, _LP = None, None
def _init(lk, lp):
    global _LK, _LP; _LK, _LP = lk, lp
def _xi_one(r):
    if _LP is None:      # power law P = k^(gamma-3), gamma 1.8
        f = lambda k: k**(-0.2) if k > 0 else 0.0
    else:
        f = lambda k: k * math.exp(np.interp(math.log(k), _LK, _LP)) if k > 0 else 0.0
    K = 10 * math.pi / r                     # first five sine cycles on a finite interval (QAWO), the rest by QAWF
    edges = [0.0] + [x for x in (0.1, 1.0, 8.0, 100.0) if x < K] + [K]   # breakpoints so small-r integrals see the low-k power
    v1 = sum(quad(f, a, b, weight='sin', wvar=r, limit=400)[0] for a, b in zip(edges[:-1], edges[1:]))
    kend = None
    if _LP is not None:                      # spectrum effectively zero beyond kend: finite QAWO pieces (QAWF is unstable there)
        dead = np.where(_LP < _LP.max() - 230.0)[0]
        kend = math.exp(_LK[dead[0]]) if len(dead) else None
    if kend is not None and kend > K:
        e2 = np.geomspace(K, kend, 40)
        v2 = sum(quad(f, a, b, weight='sin', wvar=r, limit=400)[0] for a, b in zip(e2[:-1], e2[1:]))
    elif kend is not None:
        v2 = 0.0
    else:
        v2, _ = quad(f, K, np.inf, weight='sin', wvar=r, limlst=400, limit=400)
    return (v1 + v2) / (2 * math.pi**2 * r)
def xi_of(P, rg):
    args = (np.log(KK), np.log(np.maximum(P, 1e-300))) if P is not None else (None, None)
    with Pool(NPROC, initializer=_init, initargs=args) as pool:
        xi = np.array(pool.map(_xi_one, rg, chunksize=20))
    assert np.all(np.isfinite(xi)) and np.abs(xi).max() < 1e7, 'xi transform failed'
    return xi
class Proj:
    """xi on a log grid -> Sigma, Delta Sigma (bin averaged), wp multipole pieces."""
    def __init__(self, rg, xi, rho_m):
        self.rg, self.xi, self.rho = rg, xi, rho_m
        lr = np.log(rg)
        self.spl = CubicSpline(lr, xi * rg**2)
        # xibar, xibarbar with power-law inner extrapolation
        a = -(math.log(abs(xi[1])) - math.log(abs(xi[0]))) / (lr[1] - lr[0])
        c3 = xi[0] * rg[0]**3 / (3 - a); c5 = xi[0] * rg[0]**5 / (5 - a)
        I3 = c3 + cumulative_trapezoid(xi * rg**3, lr, initial=0.0)
        I5 = c5 + cumulative_trapezoid(xi * rg**5, lr, initial=0.0)
        self.xb = CubicSpline(lr, 3 * I3 / rg**3); self.xbb = CubicSpline(lr, 5 * I5 / rg**5)
        self.rmax = rg[-1]
        # Sigma on a log grid, mean Sigma inside R
        self.RS = np.logspace(-3, 2.6, 700)
        self.Sig = np.array([self.sigma(R) for R in self.RS])
        lR = np.log(self.RS)
        b = -(math.log(self.Sig[1]) - math.log(self.Sig[0])) / (lR[1] - lR[0])
        inner = self.Sig[0] * self.RS[0]**2 / (2 - b)
        cum = inner + cumulative_trapezoid(self.Sig * self.RS**2, lR, initial=0.0)
        self.DSg = 2 * cum / self.RS**2 - self.Sig
        self.DSspl = CubicSpline(lR, self.DSg)
    def xif(self, r):
        return self.spl(np.log(r)) / r**2
    def sigma(self, R, nt=6000):
        T = math.acosh(self.rmax / R)
        t = np.linspace(0, T, nt); s = R * np.cosh(t)
        return 2 * self.rho * np.trapz(self.xif(s) * s, t) / 1e12      # h Msun pc^-2
    def ds_bin(self, r1, r2, n=64):
        R = np.linspace(r1, r2, n)
        return np.trapz(self.DSspl(np.log(R)) * R, R) / np.trapz(R, R)
    def ds_at(self, R):
        return float(self.DSspl(math.log(R)))
    def wp_parts(self, rp, pimax, nt=6000):
        T = math.asinh(min(pimax, math.sqrt(self.rmax**2 - rp**2)) / rp)
        t = np.linspace(0, T, nt); s = rp * np.cosh(t); mu = np.tanh(t); w = rp * np.cosh(t)
        lx = np.log(s); xi = self.xif(s); xb = self.xb(lx); xbb = self.xbb(lx)
        P2 = 0.5 * (3 * mu**2 - 1); P4 = (35 * mu**4 - 30 * mu**2 + 3) / 8
        W0 = 2 * np.trapz(xi * w, t)
        W1 = 2 * np.trapz(((2 / 3) * xi + (4 / 3) * (xi - xb) * P2) * w, t)
        W2 = 2 * np.trapz((xi / 5 + (4 / 7) * (xi - xb) * P2 + (8 / 35) * (xi + 2.5 * xb - 3.5 * xbb) * P4) * w, t)
        return np.array([W0, W1, W2])

# ---------------------------------------------------------------- data
SURV = {1: 'KiDS', 2: 'DES', 3: 'HSCY3'}; SURVOPT = {1: 1, 2: 2, 3: 4}
LENS = [  # name, sample, file z tag, index block, ilens in block, rmax lens index, wp file, pairs {isurv: [itom]}
    ('BGS1', 'BGS_BRIGHT', '0.1_zmax_0.2', 'bgs', 1, 1, '0.1_0.2', {1: [4, 5], 2: [3, 4], 3: [2, 3, 4]}),
    ('BGS2', 'BGS_BRIGHT', '0.2_zmax_0.3', 'bgs', 2, 2, '0.2_0.3', {1: [4, 5], 2: [3, 4], 3: [2, 3, 4]}),
    ('BGS3', 'BGS_BRIGHT', '0.3_zmax_0.4', 'bgs', 3, 3, '0.3_0.4', {1: [4, 5], 2: [3, 4], 3: [2, 3, 4]}),
    ('LRG1', 'LRG', '0.4_zmax_0.6', 'lrg', 1, 4, '0.4_0.6', {1: [4, 5], 2: [4], 3: [3, 4]}),
    ('LRG2', 'LRG', '0.6_zmax_0.8', 'lrg', 2, 5, '0.6_0.8', {3: [3, 4]}),
]
RMAX = {(int(r[0]), int(r[1])): r[2] for r in np.loadtxt(os.path.join(DATA, 'covariances/rmax_values.dat'))}
def load_cov(kind, blk):
    idx = np.loadtxt(os.path.join(DATA, f'covariances/bin_ds_kids1000desy3hscy3_desiy1{blk}.dat'))
    c = np.loadtxt(os.path.join(DATA, f'covariances/{kind}covcorr_kids1000desy3hscy3_desiy1{blk}_pzwei.dat'), skiprows=1)
    n = len(idx); C = np.zeros((n, n)); C[c[:, 0].astype(int) - 1, c[:, 1].astype(int) - 1] = c[:, 2]
    return idx, C
def read_ds(kind, survey, sample, ztag, itom):
    pre = 'bmodes_deltasigma' if kind == 'dx' else 'deltasigma'
    return fits.open(os.path.join(DATA, f'ggl/{survey}/{pre}_{sample}_zmin_{ztag}_lenszbin_{itom - 1}_blindA_boost_False.fits'))[1].data
def build_points(kind='ds', rmin=8.0, cut='centre', nomag=False):
    """list of dict per kept DS point; covariance blocks per sample."""
    pts = []
    for li, (name, sample, ztag, blk, il, rl, wpf, pairs) in enumerate(LENS):
        for s, toms in pairs.items():
            for t in toms:
                d = read_ds(kind, SURV[s], sample, ztag, t)
                for j in range(len(d)):
                    Rc = math.sqrt(d['rp_min'][j] * d['rp_max'][j])
                    rmx = RMAX[(SURVOPT[s], rl)]
                    keep = (Rc >= rmin and Rc <= rmx) if cut == 'centre' else (d['rp_min'][j] >= rmin * 0.999 and d['rp_max'][j] <= rmx)
                    if not keep: continue
                    if kind == 'dx': y = d['ds'][j]
                    else: y = d['ds'][j] if nomag else d['ds'][j] - d['magnification_bias'][j]
                    pts.append(dict(lens=li, surv=s, tom=t, isep=j + 1, blk=blk, il=il, y=float(y), r1=float(d['rp_min'][j]),
                                    r2=float(d['rp_max'][j]), rp=float(d['rp'][j]), zl=float(d['z_l'][j])))
    return pts
COV = {k: {b: load_cov(k, b) for b in ('bgs', 'lrg')} for k in ('ds', 'dx')}
def cov_for(pts, kind='ds'):
    n = len(pts); C = np.zeros((n, n)); pos = []
    for p in pts:
        idx, _ = COV[kind][p['blk']]
        m = np.where((idx[:, 1] == p['surv']) & (idx[:, 2] == p['il']) & (idx[:, 3] == p['tom']) & (idx[:, 4] == p['isep']))[0]
        assert len(m) == 1; pos.append(m[0])
    for a in range(n):
        for b in range(n):
            if pts[a]['blk'] == pts[b]['blk']:
                C[a, b] = COV[kind][pts[a]['blk']][1][pos[a], pos[b]]
    return C
def load_wp(rlo=5.0, rhi=20.0):
    out = []
    for li, L in enumerate(LENS):
        f = os.path.join(DATA, f'wp/wp_{L[1]}_GCcomb_{L[6]}_default_angular_bitwise_log2_njack64_nran4_split20.txt')
        a = np.loadtxt(f)
        for row in a:
            if rlo <= row[1] <= rhi:
                out.append(dict(lens=li, rp=float(row[1]), y=float(row[2]), e=float(row[3])))
    return out

# ---------------------------------------------------------------- fit
VECTORS = {'J': (1, 2, 3), 'KiDS': (1,), 'DES': (2,), 'HSCY3': (3,), 'K+D': (1, 2)}
GRID = np.round(np.arange(0.70, 0.90 + 1e-9, 0.0125), 4)
class Fit:
    def __init__(self, pts, C, wps, tmpl_ds, tmpl_wp, f_of, s8t, pm=False, wpcorr=0.0, ds_scale=None, wp_scale=1.0):
        self.lenses = sorted(set(p['lens'] for p in pts)); self.nl = len(self.lenses)
        self.y_ds = np.array([p['y'] for p in pts]) * (ds_scale if ds_scale is not None else 1.0)
        self.t_ds = np.array(tmpl_ds); self.li_ds = np.array([self.lenses.index(p['lens']) for p in pts])
        wps = [w for w in wps if w['lens'] in self.lenses]
        self.y_wp = np.array([w['y'] for w in wps]) * wp_scale
        self.t_wp = np.array([tmpl_wp[i] for i, w in enumerate(wps)]) if len(wps) else np.zeros((0, 3))
        self.li_wp = np.array([self.lenses.index(w['lens']) for w in wps]); self.f = np.array([f_of[l] for l in self.lenses])
        Cw = np.diag([w['e']**2 for w in wps])
        for a in range(len(wps)):
            for b in range(len(wps)):
                if a != b and wps[a]['lens'] == wps[b]['lens']: Cw[a, b] = wpcorr * wps[a]['e'] * wps[b]['e']
        n1 = len(self.y_ds); Ct = np.zeros((n1 + len(wps),) * 2); Ct[:n1, :n1] = C; Ct[n1:, n1:] = Cw
        self.Lw = np.linalg.cholesky(np.linalg.inv(Ct)).T       # whitening: chi2 = |Lw r|^2
        self.y = np.concatenate([self.y_ds, self.y_wp]); self.s8t = s8t; self.pm = pm
        self.pmt = np.array([2 * math.log(p['r2'] / p['r1']) / (p['r2']**2 - p['r1']**2) for p in pts])
        self.ndata = len(self.y); self.npar = 1 + self.nl * (2 if pm else 1)
    def model(self, s8, th):
        s = (s8 / self.s8t)**2; b = th[:self.nl]
        m_ds = b[self.li_ds] * s * self.t_ds
        if self.pm: m_ds = m_ds + th[self.nl:][self.li_ds] * self.pmt
        bw = b[self.li_wp]; fw = self.f[self.li_wp]
        m_wp = s * (bw**2 * self.t_wp[:, 0] + bw * fw * self.t_wp[:, 1] + fw**2 * self.t_wp[:, 2])
        return np.concatenate([m_ds, m_wp])
    def prof(self, s8, th0=None):
        th0 = np.concatenate([np.full(self.nl, 1.5), np.zeros(self.nl if self.pm else 0)]) if th0 is None else th0
        r = least_squares(lambda th: self.Lw @ (self.y - self.model(s8, th)), th0, method='lm', xtol=1e-12, ftol=1e-12)
        return float(2 * r.cost), r.x
    def run(self):
        chi = []; th = None
        for s8 in GRID:
            c, th = self.prof(s8, th); chi.append(c)
        chi = np.array(chi); i = int(np.argmin(chi))
        if i == 0 or i == len(GRID) - 1:        # extend at an edge
            ext = GRID[0] - 0.0125 * np.arange(1, 17) if i == 0 else GRID[-1] + 0.0125 * np.arange(1, 17)
            g2 = np.concatenate([GRID, ext]); chi = list(chi); th = None
            for s8 in ext:
                c, th = self.prof(s8, th); chi.append(c)
            o = np.argsort(g2); g = g2[o]; chi = np.array(chi)[o]
        else:
            g = GRID
        m = chi <= chi.min() + 4.0
        if m.sum() < 3:
            i = int(np.argmin(chi)); m = np.zeros(len(g), bool); m[max(i - 1, 0):i + 2] = True
        a, b_, c_ = np.polyfit(g[m], chi[m], 2)
        best = -b_ / (2 * a); width = 1 / math.sqrt(a) if a > 0 else float('nan')
        # exact continuous profile
        from scipy.optimize import minimize_scalar
        ms = minimize_scalar(lambda s: self.prof(s)[0], bounds=(g[0], g[-1]), method='bounded', options=dict(xatol=1e-6))
        cmin, thb = self.prof(ms.x)
        try:
            lo = brentq(lambda s: self.prof(s)[0] - cmin - 1, max(ms.x - 0.3, 0.3), ms.x)
            hi = brentq(lambda s: self.prof(s)[0] - cmin - 1, ms.x, ms.x + 0.3)
            ex_w = 0.5 * (hi - lo)
        except Exception:
            lo = hi = ex_w = float('nan')
        from scipy.stats import chi2 as C2
        dof = self.ndata - self.npar
        return dict(best=float(best), width=float(width), exact_best=float(ms.x), exact_width=float(ex_w), exact_lo=lo, exact_hi=hi,
                    chi2=float(cmin), dof=int(dof), p=float(C2.sf(cmin, dof)), b=[float(x) for x in thb[:self.nl]],
                    lenses=[LENS[l][0] for l in self.lenses], ndata=self.ndata)

def label(r, s8t):
    g = (s8t - r['best']) / r['width']
    if r['p'] < 0.01: lab = 'NO VERDICT (p < 0.01)'
    elif r['width'] > 0.05: lab = 'NO POWER'
    elif -2 <= g <= 2: lab = 'AMPLITUDE CONSISTENT'
    elif 2 < g <= 3: lab = 'GAP STAYS'
    else: lab = 'TENSION (theory above data)' if g > 3 else 'TENSION (theory below data)'
    return g, lab

# ---------------------------------------------------------------- main
def templates(P, rho, zl, pts, wps, pimax_list, rpcol=False, cache=None):
    xi = xi_of(P, RG); pr = Proj(RG, xi, rho)
    return pr
def main():
    t0 = time.time(); out = dict(lane='LWB1R', note='kappa = 1/2 FITTED; not theory closed; adopts nothing', mutate=MUT)
    # ---- V1 analytic power law
    xi = xi_of(None, RG_PL)
    gam = 1.8; A_xi = Gam(gam - 1) * math.sin(math.pi * (gam - 1) / 2) / (2 * math.pi**2)
    xi_an = A_xi * RG_PL**-gam
    m = (RG_PL >= 0.5) & (RG_PL <= 1e3)
    pr = Proj(RG_PL, xi, 1.0e12)            # rho 1e12 so Sigma = wp numerically
    Bf = Gam(0.5) * Gam((gam - 1) / 2) / Gam(gam / 2)
    rr = np.array([1, 2, 5, 10, 20, 30, 60.0])
    wp_num = np.array([pr.wp_parts(r, 1e9)[0] for r in rr]); wp_an = A_xi * Bf * rr**(1 - gam)
    ds_num = np.array([pr.ds_at(r) for r in rr]); ds_an = wp_an * (gam - 1) / (3 - gam)
    V1 = dict(xi_maxrel_0p5_1e3=float(np.max(abs(xi[m] / xi_an[m] - 1))), wp_rel=list(wp_num / wp_an - 1), ds_rel=list(ds_num / ds_an - 1))
    V1['pass_'] = bool(max(abs(np.array(V1['wp_rel'])).max(), abs(np.array(V1['ds_rel'])).max()) < 0.01)
    out['V1'] = V1; print('V1', V1, flush=True)
    # ---- V1b the sine transform of a real spectrum against brute-force trapezoid integration (k to 3000, Gaussian damping at 1000)
    P = P_formB(0.3, 'canonical'); kb = np.linspace(1e-5, 3000, 6_000_000); Pb = np.exp(np.interp(np.log(kb), np.log(KK), np.log(P)))
    _init(np.log(KK), np.log(P)); V1b = {}
    for r in (0.05, 0.3, 1.9, 12.6, 30.0, 83.0):
        bf = np.trapz(kb**2 * Pb * np.sin(kb * r) / (kb * r) * np.exp(-(kb / 1000)**2), kb) / (2 * math.pi**2)
        V1b[str(r)] = float(_xi_one(r) / bf - 1)
    _init(None, None); out['V1b_xi_vs_bruteforce_rel'] = V1b; print('V1b', V1b, flush=True)
    # ---- V2
    out['V2'] = dict(sigma8=sigma_R(KK, P_LIN0), sigma8_independent_grid=sigma_R(np.logspace(-4, 2, 20000), np.interp(np.log(np.logspace(-4, 2, 20000)), np.log(KK), P_LIN0)))
    out['V2']['pass_'] = abs(out['V2']['sigma8_independent_grid'] / SIG8_REF - 1) < 0.003
    # ---- data
    pts = build_points(); wps = load_wp()
    if MUT == 'MU1':
        for p in pts: p['y'] *= 0.85
    zL = {li: float(np.mean([p['zl'] for p in pts if p['lens'] == li])) for li in range(len(LENS))}
    out['zL'] = {LENS[l][0]: z for l, z in zL.items()}; out['n_ds'] = len(pts); out['n_wp'] = len(wps)
    C_all = cov_for(pts)
    def sel(survs, P=None):
        ii = [i for i, p in enumerate(pts) if p['surv'] in survs]
        return ii
    # ---- spectra and projections per (spectrum, lens)
    def proj_set(Pf, rho):
        return {li: Proj(RG, xi_of(Pf(zL[li]), RG), rho) for li in range(len(LENS))}
    def tmpl(projs, plist, wl, pimax, rpcol=False):
        tds = [projs[p['lens']].ds_at(p['rp']) if rpcol else projs[p['lens']].ds_bin(p['r1'], p['r2']) for p in plist]
        twp = [projs[w['lens']].wp_parts(w['rp'], pimax) for w in wl]
        return tds, twp
    def fit_all(projs, s8t, fz, plist=None, wl=None, C=None, pimax=40.0, rpcol=False, **kw):
        plist = pts if plist is None else plist; wl = wps if wl is None else wl; C = C_all if C is None else C
        tds, twp = tmpl(projs, plist, wl, pimax, rpcol)
        res = {}
        for v, sv in VECTORS.items():
            ii = [i for i, p in enumerate(plist) if p['surv'] in sv]
            lens_in = sorted(set(plist[i]['lens'] for i in ii))
            wi = [j for j, w in enumerate(wl) if w['lens'] in lens_in]
            F = Fit([plist[i] for i in ii], C[np.ix_(ii, ii)], [wl[j] for j in wi], [tds[i] for i in ii], [twp[j] for j in wi], fz, s8t, **kw)
            r = F.run(); r['gap'], r['label'] = label(r, s8t); res[v] = r
        return res
    out['foot'] = {}
    for foot in ('canonical', 'alt'):
        s8t, Om = FOOT[foot]['s8'], FOOT[foot]['Om']; rho = Om * RHO_CRIT
        D, f = growth_fns(Om); fz = {li: f(zL[li]) for li in range(len(LENS))}
        projs = proj_set(lambda z: P_formB(z, foot), rho)
        o = dict(target_s8=s8t, Omega_m=Om, f=fz)
        o['primary'] = fit_all(projs, s8t, fz); print(foot, 'primary', {v: (round(r['best'], 4), round(r['width'], 4), round(r['gap'], 2), r['label']) for v, r in o['primary'].items()}, flush=True)
        if MUT is None:
            for pm in (80.0, 100.0, 1e9):
                o[f'pimax_{int(pm) if pm < 1e8 else "inf"}'] = fit_all(projs, s8t, fz, pimax=pm)
            o['pointmass'] = fit_all(projs, s8t, fz, pm=True)
            o['wpcorr0.5'] = fit_all(projs, s8t, fz, wpcorr=0.5)
            o['rp_column'] = fit_all(projs, s8t, fz, rpcol=True)
            for rmin in (5.0, 12.0):
                pl = build_points(rmin=rmin); o[f'Rmin_{int(rmin)}'] = fit_all(projs, s8t, fz, plist=pl, C=cov_for(pl))
            pl = build_points(cut='edges'); o['cut_edges'] = fit_all(projs, s8t, fz, plist=pl, C=cov_for(pl))
            pl = build_points(nomag=True); o['no_magnification'] = fit_all(projs, s8t, fz, plist=pl, C=cov_for(pl))
            o['N1'] = fit_all(proj_set(lambda z: P_formB(z, foot, 'N1'), rho), s8t, fz)
            o['Ntail0'] = fit_all(proj_set(lambda z: P_formB(z, foot, 'Ntail0'), rho), s8t, fz)
            # CAMB halofit at KL1's pars (neutrino floor 0.06 eV), x R_tot, normalised to the target
            Pc, s8c, _ = camb_nl(FOOT[foot]['pars'], [zL[l] for l in range(len(LENS))])
            o['camb_halofit'] = fit_all(proj_set(lambda z: Pc[z] * (s8t / s8c)**2 * Rtot(KK, foot), rho), s8t, fz)
            # V3 null on the B-mode
            if foot == 'canonical':
                bp = build_points(kind='dx'); Cb = cov_for(bp, 'dx'); tb = np.array([projs[p['lens']].ds_bin(p['r1'], p['r2']) for p in bp])
                yb = np.array([p['y'] for p in bp]); V3 = {}
                for v, sv in (('KiDS', (1,)), ('DES', (2,)), ('HSCY3', (3,)), ('J', (1, 2, 3))):
                    ii = [i for i, p in enumerate(bp) if p['surv'] in sv]; Ci = np.linalg.inv(Cb[np.ix_(ii, ii)])
                    F = tb[ii] @ Ci @ tb[ii]; A = (tb[ii] @ Ci @ yb[ii]) / F; sA = 1 / math.sqrt(F)
                    V3[v] = dict(A=float(A), sigma=float(sA), nsig=float(A / sA))
                V3['pass_'] = bool(all(abs(V3[v]['nsig']) <= 3 for v in ('KiDS', 'DES', 'HSCY3', 'J')))
                out['V3'] = V3; print('V3', V3, flush=True)
        out['foot'][foot] = o
        json.dump(out, open(os.path.join(HERE, f'lwb1r{"_MUTATE_" + MUT if MUT else ""}.json'), 'w'), indent=1, default=float)
    if MUT is None:
        # ---- V5 reference spectrum: Planck 2018 CAMB halofit, same pipeline
        pl18 = dict(h=0.6736, ob=0.02237, oc=0.1200, lnA=3.044, ns=0.9649, tau=0.0544)
        Pc, s8c, Omc = camb_nl(pl18, [zL[l] for l in range(len(LENS))])
        D, f = growth_fns(Omc); fz = {li: f(zL[li]) for li in range(len(LENS))}
        res = fit_all(proj_set(lambda z: Pc[z], Omc * RHO_CRIT), s8c, fz)
        V5 = dict(sigma8_planck=s8c, Omega_m=Omc, rows={})
        for v, r in res.items():
            S8 = r['best'] * math.sqrt(Omc / 0.3); wS = r['width'] * math.sqrt(Omc / 0.3)
            V5['rows'][v] = dict(sigma8=r['best'], width=r['width'], S8=S8, S8_width=wS, p=r['p'],
                                 n_comb_widths_vs_0794=(S8 - 0.794) / math.sqrt(wS**2 + 0.023**2))
        V5['KD_within_2'] = bool(abs(V5['rows']['K+D']['n_comb_widths_vs_0794']) <= 2)
        out['V5'] = V5; print('V5', V5, flush=True)
    # ---- V4 blinding slope (non-tomographic files, diagonal errors)
    if MUT is None:
        V4 = []
        for li, (name, sample, ztag, blk, il, rl, wpf, pairs) in enumerate(LENS[:4]):
            dd = {s: fits.open(os.path.join(DATA, f'ggl/{SURV[s]}/deltasigma_{sample}_zmin_{ztag}_blindA_boost_False.fits'))[1].data for s in (1, 2, 3)}
            for s in (1, 3):
                rmx = min(RMAX[(SURVOPT[s], rl)], RMAX[(SURVOPT[2], rl)])
                a, b = dd[s], dd[2]; R = np.sqrt(a['rp_min'] * a['rp_max'])
                ya = a['ds'] - a['magnification_bias']; yb = b['ds'] - b['magnification_bias']
                m = (R <= rmx) & (yb / b['ds_err'] > 2)
                rat = ya[m] / yb[m]; er = abs(rat) * np.sqrt((a['ds_err'][m] / ya[m])**2 + (b['ds_err'][m] / yb[m])**2)
                X = np.vstack([np.ones(m.sum()), np.log(R[m])]).T; W = 1 / er**2
                Cp = np.linalg.inv(X.T @ (X * W[:, None])); par = Cp @ (X.T @ (W * rat))
                V4.append(dict(lens=name, ratio=f'{SURV[s]}/DES', a=float(par[0]), c=float(par[1]), sc=float(math.sqrt(Cp[1, 1])), n=int(m.sum())))
        w = np.array([1 / v['sc']**2 for v in V4]); c = np.array([v['c'] for v in V4])
        cp = float((w * c).sum() / w.sum()); scp = float(1 / math.sqrt(w.sum()))
        out['V4'] = dict(rows=V4, pooled_c=cp, sigma=scp, nsig=cp / scp, pass_=bool(abs(cp / scp) <= 3))
        print('V4', out['V4']['pooled_c'], out['V4']['nsig'], flush=True)
    out['runtime_s'] = time.time() - t0
    json.dump(out, open(os.path.join(HERE, f'lwb1r{"_MUTATE_" + MUT if MUT else ""}.json'), 'w'), indent=1, default=float)
    print('done', out['runtime_s'])
if __name__ == '__main__':
    main()
