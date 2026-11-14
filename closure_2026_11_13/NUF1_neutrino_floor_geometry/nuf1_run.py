"""NUF1 (criteria: FROZEN_CRITERIA.md in this folder): the geometry part of the DESI DR2 neutrino-mass tension,
reproduced from the published BAO distances plus DESI's compressed CMB prior, flat LambdaCDM tested on its own terms.

chi2(m) = BAO chi2 + compressed-CMB-prior chi2, profiled over (theta*, omega_b, omega_bc) on a grid of the effective
neutrino mass sum m (eV, may be negative; arXiv:2407.10965 Eq. nu_eff_def). Distances, r_d and theta* from CAMB.

Usage: python3 nuf1_run.py MODE
  real modes : primary, ctl_noLRG1, ctl_noLRG2, ctl_lyaAP, ctl_zgt06,
               ro_w0wa, ro_widen, ro_hfixed, ro_thetamean
  checks     : K1, K2A, K2B, K3   (K3 = mutation twin; exits 3 on pass, 4 on fail; real modes exit 0)
Each mode writes nuf1_<MODE>.json and prints its own log (redirect to nuf1_<MODE>.out)."""
import json, os, sys, time
import numpy as np
import camb
from scipy.optimize import minimize, brentq
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1]
C_KMS = 299792.458

# ---------------- data ----------------
# DESI DR2 BAO, arXiv:2503.14738 Table "tab:alphas" (TeX source): name, z_eff, D_M/r_d, sd, D_H/r_d, sd, r_MH.
# Same vector as closure_2026_11_12/AZ2_flat_a0_lya_ap/az2_flat_a0.py; every value re-checked against the TeX.
GAL = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459),
       ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
       ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416),
       ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
       ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500)]
LYA_BAO = ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)   # arXiv:2503.14738 tab:alphas
LYA_AP = ("Lya", 2.330, 39.32, 0.33, 8.600, 0.066, 0.225)       # arXiv:2607.27410 Eq. dmdh_dr2 (sections/results.tex)
BGS = ("BGS", 0.295, 7.942, 0.075)                              # D_V/r_d, arXiv:2503.14738 tab:alphas
# DESI compressed CMB prior on (theta*, omega_b, omega_bc), arXiv:2503.14738 Appendix A,
# Eqs. CMB_compression_mean and CMB_compression_cov (TeX source, verbatim). theta* in radians.
CMB_MU = np.array([0.01041, 0.02223, 0.14208])
CMB_COV = 1e-9*np.array([[0.006621, 0.12444, -1.1929],
                         [0.12444, 21.344, -94.001],
                         [-1.1929, -94.001, 1488.4]])
THETA_MAIN = 0.0104110          # arXiv:2503.14738 Eq. thetastar_prior: 100 theta* = 1.04110 +- 0.00053
THETA_MAIN_SD = 0.0000053
BBN = (0.02218, 0.00055)        # arXiv:2503.14738 Eq. BBN_LCDM
FLOOR_NO, FLOOR_IO = 0.059, 0.10  # eV; arXiv:2503.14744 (citing NuFIT 6.0, Esteban et al. JHEP 12 (2024) 216)

ZS = [BGS[1]] + [b[1] for b in GAL] + [LYA_BAO[1]]   # every redshift the model is evaluated at

def dataset(name):
    """Return (aniso bins, use_bgs)."""
    if name == "primary": return GAL + [LYA_BAO], True
    if name == "noLRG1": return [b for b in GAL if b[0] != "LRG1"] + [LYA_BAO], True
    if name == "noLRG2": return [b for b in GAL if b[0] != "LRG2"] + [LYA_BAO], True
    if name == "lyaAP": return GAL + [LYA_AP], True
    if name == "zgt06": return [b for b in GAL + [LYA_BAO] if b[1] > 0.6], BGS[1] > 0.6
    raise ValueError(name)

# ---------------- model ----------------
_cache = {}
def raw(conv, p, m, nmass=3, de=None):
    """Observables for a physical m >= 0. conv 'theta': p = (theta*, omega_b, omega_bc); conv 'h': p = (h, ...).
    Returns dict: th (theta*, rad), h, Om, rd, DM/DH/DV over ZS (Mpc)."""
    key = (conv, tuple(np.round(p, 12)), round(m, 9), nmass, de)
    if key in _cache: return _cache[key]
    P = camb.CAMBparams()
    if de is not None: P.set_dark_energy(w=de[0], wa=de[1], dark_energy_model="ppf")
    kw = dict(ombh2=p[1], omch2=p[2] - p[1], mnu=m, num_massive_neutrinos=nmass if m > 0 else 0, nnu=3.044, omk=0)
    if conv == "theta": P.set_cosmology(thetastar=p[0], **kw)
    else: P.set_cosmology(H0=100*p[0], **kw)
    P.WantTransfer = False; P.WantCls = False
    R = camb.get_background(P); d = R.get_derived_params()
    z = np.array(ZS)
    DM = R.comoving_radial_distance(z); DH = C_KMS/R.hubble_parameter(z); DV = (z*DM**2*DH)**(1/3)
    h = P.H0/100
    out = dict(th=d["thetastar"]/100, h=h, Om=(P.ombh2 + P.omch2 + P.omnuh2)/h**2, rd=d["rdrag"],
               vec=np.r_[d["thetastar"]/100, h, DM/d["rdrag"], DH/d["rdrag"], DV/d["rdrag"]])
    if len(_cache) > 20000: _cache.clear()
    _cache[key] = out
    return out

def obs(conv, p, m, nmass=3, de=None):
    """Effective-mass observables, arXiv:2407.10965 Eq. (nu_eff_def): X(m) = X(0) + sgn(m)[X(|m|) - X(0)],
    at fixed sampled parameters p (theta*, omega_b, omega_bc for conv 'theta')."""
    if m >= 0: return raw(conv, p, m, nmass, de)["vec"]
    return 2*raw(conv, p, 0.0, nmass, de)["vec"] - raw(conv, p, -m, nmass, de)["vec"]

NZ = len(ZS)
def unpack(v):
    th, h = v[0], v[1]; DM, DH, DV = v[2:2+NZ], v[2+NZ:2+2*NZ], v[2+2*NZ:2+3*NZ]
    return th, h, DM, DH, DV

def chi2_bao(v, bins, use_bgs, data_override=None):
    th, h, DM, DH, DV = unpack(v); s = 0.0
    for i, b in enumerate(bins):
        nm, z, dm, sdm, dh, sdh, r = b if data_override is None else data_override[i]
        k = ZS.index(z)
        C = np.array([[sdm**2, r*sdm*sdh], [r*sdm*sdh, sdh**2]])
        dv = np.array([dm - DM[k], dh - DH[k]]); s += dv @ np.linalg.solve(C, dv)
    if use_bgs:
        dvb = BGS[2] if data_override is None else data_override[-1][2]
        s += ((dvb - DV[0])/BGS[3])**2
    return s

class Prior:
    def __init__(s, mu=CMB_MU, cov=CMB_COV): s.mu = np.array(mu, float); s.Ci = np.linalg.inv(cov)
    def chi2(s, th, ob, obc):
        d = np.array([th, ob, obc]) - s.mu; return float(d @ s.Ci @ d)

SD = np.sqrt(np.diag(CMB_COV))

# ---------------- profile ----------------
def make_obj(conv, m, bins, use_bgs, prior, nmass=3, w0wa=False, data_override=None):
    def f(x):
        if conv == "theta": p = prior.mu + x[:3]*SD*2; dex = x[3:5] if w0wa else None
        else: p = np.r_[x[0], prior.mu[1:] + x[1:3]*SD[1:]*2]; dex = x[3:5] if w0wa else None
        if conv == "h" and not (0.4 < p[0] < 1.0): return 1e10
        if p[1] <= 0.005 or p[2] - p[1] <= 0.01: return 1e10
        de = None
        if w0wa:
            w0, wa = dex
            if not (-3 <= w0 <= 1 and -3 <= wa <= 2 and w0 + wa < 0): return 1e10
            de = (round(float(w0), 10), round(float(wa), 10))
        try: v = obs(conv, p, m, nmass, de)
        except Exception: return 1e10
        th, h, *_ = unpack(v)
        cb = chi2_bao(v, bins, use_bgs, data_override)
        thp = p[0] if conv == "theta" else th
        return cb + prior.chi2(thp, p[1], p[2])
    return f

def nm(f, x0, step):
    x0 = np.array(x0, float); n = len(x0)
    sim = np.vstack([x0] + [x0 + step[i]*np.eye(n)[i] for i in range(n)])
    r = minimize(f, x0, method="Nelder-Mead",
                 options=dict(initial_simplex=sim, xatol=1e-4, fatol=1e-5, maxiter=4000, maxfev=6000))
    sim = np.vstack([r.x] + [r.x + 0.3*step[i]*np.eye(n)[i] for i in range(n)])
    r2 = minimize(f, r.x, method="Nelder-Mead",
                  options=dict(initial_simplex=sim, xatol=1e-5, fatol=1e-6, maxiter=4000, maxfev=6000))
    return r2 if r2.fun <= r.fun else r

def start_points(conv, w0wa):
    base = [0.0, 0.0, 0.0] if conv == "theta" else [0.68, 0.0, 0.0]
    if not w0wa: return [base]
    return [base + [-1.0, 0.0], base + [-0.5, -1.5], base + [-0.8, -0.7]]

def steps(conv, w0wa):
    s = [0.3, 0.3, 0.3] if conv == "theta" else [0.01, 0.3, 0.3]
    return s + ([0.1, 0.3] if w0wa else [])

def profile(conv, grid, bins, use_bgs, prior, nmass=3, w0wa=False, data_override=None, log=print):
    """Profile chi2 over the sampled parameters at each m, warm-started outward from m = 0."""
    out = {}
    order = sorted(grid, key=lambda m: (abs(m), m))
    pos_prev = neg_prev = None
    for m in order:
        f = make_obj(conv, m, bins, use_bgs, prior, nmass, w0wa, data_override)
        starts = list(start_points(conv, w0wa))
        prev = pos_prev if m >= 0 else neg_prev
        if prev is not None: starts = [prev] if not w0wa else [prev] + starts   # warm start from the neighbour
        best = None
        for s0 in starts:
            r = nm(f, s0, steps(conv, w0wa))
            if best is None or r.fun < best.fun: best = r
        x = best.x
        if m >= 0: pos_prev = x
        if m <= 0: neg_prev = x
        if m == 0: pos_prev = neg_prev = x
        if conv == "theta": p = prior.mu + x[:3]*SD*2
        else: p = np.r_[x[0], prior.mu[1:] + x[1:3]*SD[1:]*2]
        de = (float(x[3]), float(x[4])) if w0wa else None
        v = obs(conv, p, m, nmass, de); th, h, *_ = unpack(v)
        rec = dict(chi2=float(best.fun), chi2_bao=float(chi2_bao(v, bins, use_bgs, data_override)),
                   theta_star=float(p[0] if conv == "theta" else th), omega_b=float(p[1]), omega_bc=float(p[2]),
                   h_eff=float(h))
        if w0wa: rec.update(w0=float(x[3]), wa=float(x[4]))
        out[m] = rec
        log(f"  m {m:+.3f}  chi2 {best.fun:9.4f}  (BAO {rec['chi2_bao']:8.4f})  h_eff {h:.4f}"
            + (f"  w0 {x[3]:+.3f} wa {x[4]:+.3f}" if w0wa else ""))
    return out

def summarise(prof):
    ms = np.array(sorted(prof)); cs = np.array([prof[m]["chi2"] for m in ms])
    sp = CubicSpline(ms, cs)
    fine = np.linspace(ms[0], ms[-1], 200001); cf = sp(fine)
    i = int(np.argmin(cf)); mbest, cmin = float(fine[i]), float(min(cf[i], cs.min()))
    def cross(level):
        """Delta chi2 = level crossings of the spline either side of the minimum (None if not reached on the grid)."""
        g = lambda x: float(sp(x) - cmin - level); above = cf - cmin - level >= 0
        jl = np.where(above[:i])[0]; jr = np.where(above[i:])[0]
        lo = brentq(g, fine[jl[-1]], fine[jl[-1] + 1]) if len(jl) else None
        hi = brentq(g, fine[i + jr[0] - 1], fine[i + jr[0]]) if len(jr) else None
        return [lo, hi]
    D = lambda m: float(prof[m]["chi2"] - cmin)
    return dict(m_best=mbest, chi2_min=cmin, at_grid_edge=bool(i == 0 or i == len(fine) - 1),
                ci68=cross(1.0), ci95=cross(4.0), D_floor_NO=D(FLOOR_NO), D_floor_IO=D(FLOOR_IO),
                D_m0=D(0.0), D_m006=D(0.06))

def word(D):
    if D >= 9: return "FLOOR EXCLUDED AT 3 SIGMA"
    if D >= 4: return "FLOOR DISFAVOURED"
    return "FLOOR ALLOWED"

GRID = sorted(set([round(x, 3) for x in np.arange(-0.50, 0.5001, 0.01)] + [FLOOR_NO, FLOOR_IO]))
GRID_COARSE = sorted(set([round(x, 3) for x in np.arange(-0.50, 0.5001, 0.02)] + [0.0, 0.06, FLOOR_NO, FLOOR_IO]))

# ---------------- run ----------------
def main():
    t0 = time.time(); res = dict(mode=MODE, camb=camb.__version__, numpy=np.__version__)
    log = lambda s: print(s, flush=True)
    log(f"NUF1 mode {MODE}  CAMB {camb.__version__}")
    code = 0
    real = {"primary": "primary", "ctl_noLRG1": "noLRG1", "ctl_noLRG2": "noLRG2", "ctl_lyaAP": "lyaAP",
            "ctl_zgt06": "zgt06"}
    if MODE in real or MODE in ("ro_widen", "ro_hfixed", "ro_thetamean", "ro_w0wa"):
        ds = real.get(MODE, "primary"); bins, use_bgs = dataset(ds); prior = Prior(); conv = "theta"
        grid = GRID; w0wa = False
        if MODE == "ro_widen":
            S = np.diag([1.0, 1.0, 2.0]); prior = Prior(CMB_MU, S @ CMB_COV @ S)
        if MODE == "ro_hfixed": conv = "h"
        if MODE == "ro_thetamean": prior = Prior(np.r_[THETA_MAIN, CMB_MU[1:]], CMB_COV)
        if MODE == "ro_w0wa": w0wa = True; grid = GRID_COARSE
        log(f"dataset {ds}: bins {[b[0] for b in bins]} + BGS {use_bgs}; convention fixed {conv}; w0wa {w0wa}")
        prof = profile(conv, grid, bins, use_bgs, prior, 3, w0wa, log=log)
        S_ = summarise(prof); res.update(dataset=ds, convention=conv, w0wa=w0wa, summary=S_,
                                         word=word(S_["D_floor_NO"]),
                                         profile={f"{m:+.3f}": v for m, v in sorted(prof.items())})
        log(f"best m {S_['m_best']:+.4f} eV  68% {S_['ci68']}  95% {S_['ci95']}  chi2_min {S_['chi2_min']:.3f}")
        log(f"Delta chi2 at NO floor 0.059: {S_['D_floor_NO']:.3f}   at IO floor 0.10: {S_['D_floor_IO']:.3f}")
        log(f"word (NO floor): {res['word']}")
    elif MODE == "K1":
        bins, use_bgs = dataset("primary"); h0 = 0.68; ob = BBN[0]
        def f(x):
            Om, hrd = x
            if not (0.2 < Om < 0.4): return 1e10
            obc = Om*h0**2 - 0.06/93.14   # omega_bc = Om h^2 - omega_nu
            r = raw("h", (h0, ob, obc), 0.06, nmass=1); th, h, DM, DH, DV = unpack(r["vec"])
            sc = r["rd"]*h0/hrd   # D/r_d -> (D h)/(h r_d)
            v = np.r_[th, h, DM*sc, DH*sc, DV*sc]; return chi2_bao(v, bins, use_bgs)
        r = nm(f, [0.30, 101.0], [0.01, 1.0])
        Om, hrd = r.x; obc = Om*h0**2 - 0.06/93.14
        Omc = raw("h", (h0, ob, obc), 0.06, nmass=1)["Om"]
        ok = abs(Omc - 0.2975) <= 0.003 and abs(hrd - 101.54) <= 0.3
        res.update(Om=float(Omc), hrd=float(hrd), chi2=float(r.fun), target=dict(Om=[0.2975, 0.0086], hrd=[101.54, 0.73]),
                   tol=dict(Om=0.003, hrd=0.3), passed=bool(ok))
        log(f"K1 BAO-only LCDM: Om {Omc:.4f} (DESI 0.2975 +- 0.0086)  h r_d {hrd:.2f} Mpc (DESI 101.54 +- 0.73)"
            f"  chi2 {r.fun:.3f}  -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K2A":
        bins, use_bgs = dataset("primary"); prior = Prior()
        lc = None; ww = None
        f = make_obj("theta", 0.06, bins, use_bgs, prior, nmass=1)
        lc = nm(f, [0, 0, 0], steps("theta", False))
        g = make_obj("theta", 0.06, bins, use_bgs, prior, nmass=1, w0wa=True)
        for s0 in start_points("theta", True) + [[0, 0, 0, -0.43, -1.72], [0, 0, 0, -0.3, -2.5]]:
            r = nm(g, s0, steps("theta", True))
            if ww is None or r.fun < ww.fun: ww = r
        d = float(ww.fun - lc.fun); ok = abs(d - (-8.0)) <= 1.0
        res.update(chi2_lcdm=float(lc.fun), chi2_w0wa=float(ww.fun), w0=float(ww.x[3]), wa=float(ww.x[4]),
                   dchi2=d, target=-8.0, tol=1.0, passed=bool(ok))
        log(f"K2A DESI+(theta*,ob,obc)_CMB, m 0.06 (1 massive): chi2 LCDM {lc.fun:.3f}  w0wa {ww.fun:.3f}"
            f" (w0 {ww.x[3]:+.3f} wa {ww.x[4]:+.3f})  dchi2 {d:+.2f} (DESI -8.0) -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K2B":
        bins, use_bgs = dataset("primary")
        def f(x):
            p = np.array([THETA_MAIN + x[0]*THETA_MAIN_SD, BBN[0] + x[1]*BBN[1], 0.142 + x[2]*0.002])
            if p[2] - p[1] <= 0.01: return 1e10
            v = raw("theta", p, 0.06, nmass=1)["vec"]
            return chi2_bao(v, bins, use_bgs) + x[0]**2 + x[1]**2
        r = nm(f, [0, 0, 0], [0.3, 0.3, 1.0])
        p = np.array([THETA_MAIN + r.x[0]*THETA_MAIN_SD, BBN[0] + r.x[1]*BBN[1], 0.142 + r.x[2]*0.002])
        o = raw("theta", p, 0.06, nmass=1)
        ok = abs(o["Om"] - 0.2967) <= 0.00225 and abs(100*o["h"] - 68.45) <= 0.235
        res.update(Om=float(o["Om"]), H0=float(100*o["h"]), chi2=float(r.fun),
                   target=dict(Om=[0.2967, 0.0045], H0=[68.45, 0.47]), tol=dict(Om=0.00225, H0=0.235), passed=bool(ok))
        log(f"K2B DESI+BBN+theta*: Om {o['Om']:.4f} (DESI 0.2967 +- 0.0045)  H0 {100*o['h']:.2f} (DESI 68.45 +- 0.47)"
            f"  chi2 {r.fun:.3f} -> {'PASS' if ok else 'FAIL'}")
    elif MODE == "K3":
        bins, use_bgs = dataset("primary"); prior = Prior()
        truth = CMB_MU.copy(); v = raw("theta", truth, 0.06, 3)["vec"]; th, h, DM, DH, DV = unpack(v)
        over = [(b[0], b[1], DM[ZS.index(b[1])], b[3], DH[ZS.index(b[1])], b[5], b[6]) for b in bins]
        over.append(("BGS", BGS[1], DV[0]))
        log("K3 mutation twin: BAO vector replaced by the model's own prediction at m = 0.06 eV (3 degenerate),"
            " (theta*, omega_b, omega_bc) = prior mean; same covariance.")
        prof = profile("theta", GRID, bins, use_bgs, prior, 3, False, data_override=over, log=log)
        S_ = summarise(prof); lo, hi = S_["ci68"]
        ok = abs(S_["m_best"] - 0.06) <= 0.005 and lo is not None and hi is not None and lo <= 0.06 <= hi
        res.update(summary=S_, passed=bool(ok), profile={f"{m:+.3f}": v for m, v in sorted(prof.items())})
        log(f"K3: best m {S_['m_best']:+.4f}  68% {S_['ci68']}  chi2_min {S_['chi2_min']:.2e} -> {'PASS' if ok else 'FAIL'}")
        code = 3 if ok else 4
    else:
        raise SystemExit(f"unknown mode {MODE}")
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, f"nuf1_{MODE}.json"), "w") as fh: json.dump(res, fh, indent=1)
    log(f"wrote nuf1_{MODE}.json  ({res['seconds']} s)  exit {code}")
    sys.exit(code)

if __name__ == "__main__":
    main()
