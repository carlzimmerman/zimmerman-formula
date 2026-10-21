"""CFG956 (criteria 707cdf4cb4 + amendment A1 8debb62336): the largest wave in a0(z) that the framework's own expansion
constraint allows -- CFG689's primary likelihood (native-ruler DESI DR2 BAO + Pantheon+, curvature free), re-implemented
line for line from its committed script and read-only use of its committed cfg689.json (stored ruler, best fit).

The oscillating-a0(z) hypothesis, including its damped form, is the owner's idea (2026-10-21).

Law: a0(z) = kappa c sqrt(G rho_DE(z)), kappa = 1/2 FITTED, so a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)); footings
9.3603e-11 / 1.1312e-10 m s^-2 never pooled (every bound here is on the ratio; kappa is fitted per footing).
Wave family (base section 3): rho_DE/rho_crit,100 = W A(z)^2 [1 + eps (1+z)^beta sin(2 pi ln(1+z)/P + phi)]^2,
  a0(z)/a0(0) = A(z) [1 + eps (1+z)^beta sin(...)] / (1 + eps sin phi); beta = 0 for the plain wave (MAIN),
  beta in {0, 0.5, 1, 2} with the 'on the way down now' phase constraint for the damped family (DAMPED, A1.2).
Branches: S = CFG689 best-fit node curve (shape fixed), C = constant, N = six free nodes (reported only).

Modes:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg956_a0z_wave.py K | MUTATE | MAIN | DAMPED
Outputs cfg956_K / cfg956_MUTATE / cfg956 / cfg956_DAMPED  (.out, .json).  One core, < 1 GB.
kappa fitted; not a closed theory; a constant rho_DE is LCDM's background, so nothing here favours the framework over LCDM.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import json, time, csv, re, hashlib, math, warnings
warnings.filterwarnings("ignore", message=r".*encountered in matmul")   # numpy-Accelerate spurious matmul warnings (as disclosed in CFG689); K1 reproduces chi2 exactly
import numpy as np
from scipy.optimize import least_squares, brentq
from scipy.interpolate import PchipInterpolator
from scipy.stats import chi2 as CHI2, norm as NORM

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); ROOT = os.path.dirname(CFG)
EXTD = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data")); EXT = os.path.join(EXTD, "pantheonplus_dr")
D689 = os.path.join(CFG, "CFG689_native_ruler_bao")
MODE = sys.argv[1] if len(sys.argv) > 1 else "K"
TAG = {"K": "_K", "MUTATE": "_MUTATE", "MAIN": "", "DAMPED": "_DAMPED"}[MODE]
OUTF = open(os.path.join(HERE, f"cfg956{TAG}.out"), "w")
T0 = time.time(); WALL_CAP = 4*3600.0
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
P(f"CFG956 mode {MODE}  (criteria 707cdf4cb4 + A1 8debb62336)")

# ---------------------------------------------------------------- CFG689 committed products (read-only)
J689 = json.load(open(os.path.join(D689, "cfg689.json")))
c6 = J689["cfg"]
assert J689["mode"] == "primary" and c6["freek"] and c6["sn"] == "PP" and c6["snz"] == "zHD" and c6["snzmin"] == 0.01 and not c6["theta"]
assert c6["mnu"] == 0.0 and c6["f"] == 0.0 and c6["rho"] == 0.0 and c6["rds"] == 1.0 and not c6["wcfree"] and c6["wmin"] == -2.0
R0, BEXP, CEXP = (J689["ruler"][k] for k in ("r_d0", "b", "c"))
P2 = J689["BAO+SN"]["P2"]; PB = np.array(P2["pbest"], float); CHI_FREE, CHI_CONST, W_CONST = P2["chi2_free"], P2["chi2_const"], P2["w_const"]
NODES = np.array(c6["nodes"], float); NN = len(NODES); WBEST = PB[:NN]
wb0, sb, wc0, sc = c6["wb"], c6["sb"], c6["wc"], c6["sc"]
P(f"CFG689 primary: ruler r_d0 {R0:.5f} b {BEXP:.6f} c {CEXP:.6f}; best fit nodes {np.round(WBEST, 5).tolist()} omega_k {PB[6]:+.5f} "
  f"omega_b {PB[7]:.6f} omega_c {PB[8]:.6f}; chi2 free {CHI_FREE:.4f}, constant {CHI_CONST:.4f}")

# ---------------------------------------------------------------- constants and data (verbatim from cfg689 primary)
C = 299792.458; G = 6.67430e-11; CMS = 2.99792458e8; RHO100 = 1.87847e-26; OMG = 2.4728e-5
OMR = OMG*(1 + 0.2271*3.044)
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
ISO = [(0.295, 7.942, 0.075)]
zg = np.linspace(0, 2.5, 5001); LN1Z = np.log1p(zg); ZS = (1.0, 1.2, 1.5, 2.33)
def cumchi(Hg, z=zg): return np.r_[0, np.cumsum(0.5*(1/Hg[1:] + 1/Hg[:-1])*np.diff(z))]*C
CINV = [np.linalg.inv(np.array([[s1**2, r*s1*s2], [r*s1*s2, s2**2]])) for (_, _, _, s1, _, s2, r) in ANISO]
LTB = [np.linalg.cholesky(Ci).T for Ci in CINV]           # Ci = L L^T  ->  chi2 = |L^T (d - m/rd)|^2
def rdrag(wb, wc): return R0*(wb/wb0)**(-BEXP)*(wc/wc0)**(-CEXP)
def dm_from_chi(chi, wk):
    if wk == 0: return chi
    s = 100*np.sqrt(abs(wk))/C
    return np.sinh(s*chi)/s if wk > 0 else np.sin(s*chi)/s

raw = np.genfromtxt(os.path.join(EXT, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
covfull = np.loadtxt(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1); NSN = int(round(np.sqrt(covfull.size))); covfull = covfull.reshape(NSN, NSN)
sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)
zsn, zhel, MB_DATA = raw["zHD"][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float)
Wsn = np.linalg.inv(covfull[np.ix_(sel, sel)]); del covfull
LsT = np.ascontiguousarray(np.linalg.cholesky(Wsn).T); one = np.ones(len(MB_DATA)); A11 = one@Wsn@one
SHAS = {"PantheonPlusSH0ES.dat": sha(os.path.join(EXT, "PantheonPlusSH0ES.dat")), "PantheonPlusSH0ES_STAT+SYS.cov": sha(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov")),
        "cfg689.json": sha(os.path.join(D689, "cfg689.json"))}
P(f"SN: {len(MB_DATA)} Pantheon+ non-calibrators zHD > 0.01; BAO {[t[0] for t in ANISO]} + BGS D_V; sha256 cov {SHAS['PantheonPlusSH0ES_STAT+SYS.cov'][:8]}")
DATA = dict(A=list(ANISO), I=list(ISO), MB=MB_DATA)

# ---------------------------------------------------------------- CFG689 primary chi2, line for line (walls included)
def bg(wde, wb, wc, wk):
    om = wb + wc
    E2 = om*(1 + zg)**3 + OMR*(1 + zg)**4 + wk*(1 + zg)**2 + wde
    if np.any(E2 <= 1e-8): return None
    Hg = 100*np.sqrt(E2); chi = cumchi(Hg); return om, Hg, dm_from_chi(chi, wk), chi
def bao_pred(Hg, DM, D):
    ms = [np.array([np.interp(t[1], zg, DM), C/np.interp(t[1], zg, Hg)]) for t in D["A"]]
    mv = [(t[0]*np.interp(t[0], zg, DM)**2*C/np.interp(t[0], zg, Hg))**(1/3) for t in D["I"]]
    return ms, mv
def bao_chi2(Hg, DM, rd, D):
    ms, mv = bao_pred(Hg, DM, D); ds = [np.array([t[2], t[4]]) for t in D["A"]]
    if rd is None:
        s = (sum(m@Ci@d for m, d, Ci in zip(ms, ds, CINV)) + sum(v*t[1]/t[2]**2 for v, t in zip(mv, D["I"])))/(
             sum(m@Ci@m for m, Ci in zip(ms, CINV)) + sum(v*v/t[2]**2 for v, t in zip(mv, D["I"])))
    else: s = 1/rd
    return sum((d - s*m)@Ci@(d - s*m) for m, d, Ci in zip(ms, ds, CINV)) + sum(((t[1] - s*v)/t[2])**2 for v, t in zip(mv, D["I"]))
def sn_chi2(DM, D):
    r = D["MB"] - 5*np.log10((1 + zhel)*np.interp(zsn, zg, DM)); v = Wsn@r; b = one@v
    return r@v - b*b/A11
def prior(wb, wc): return ((wb - wb0)/sb)**2 + ((wc - wc0)/sc)**2
def chi2_689(p, D=DATA):
    wn, wk, wb, wc = np.asarray(p[:NN]), p[NN], p[-2], p[-1]
    if np.any(wn < -2.0) or np.any(wn > 3) or abs(wk) > 0.25 or not (0 < wb < 0.05) or not (0.05 <= wc <= 0.25): return 1e9
    b = bg(np.interp(zg, NODES, wn), wb, wc, wk)
    if b is None: return 1e9
    om, Hg, DM, chi = b
    return bao_chi2(Hg, DM, rdrag(wb, wc), D) + prior(wb, wc) + sn_chi2(DM, D)

# ---------------------------------------------------------------- residual form for least squares (M explicit = analytic marginalisation)
NRES = 2*len(ANISO) + len(ISO) + 2 + len(MB_DATA)
def residuals(wde, wk, wb, wc, M, D, blocks=False):
    om = wb + wc
    E2 = om*(1 + zg)**3 + OMR*(1 + zg)**4 + wk*(1 + zg)**2 + wde
    if np.any(E2 <= 1e-8): return np.full(NRES, 1e3)
    Hg = 100*np.sqrt(E2); DM = dm_from_chi(cumchi(Hg), wk); rd = rdrag(wb, wc)
    ms, mv = bao_pred(Hg, DM, D)
    eb = [L@(np.array([t[2], t[4]]) - m/rd) for L, m, t in zip(LTB, ms, D["A"])]
    ei = [(t[1] - v/rd)/t[2] for v, t in zip(mv, D["I"])]
    ep = [(wb - wb0)/sb, (wc - wc0)/sc]
    es = LsT@(D["MB"] - 5*np.log10((1 + zhel)*np.interp(zsn, zg, DM)) - M)
    if blocks:
        out = {t[0]: float(e@e) for t, e in zip(D["A"], eb)}; out["BGS"] = float(sum(e*e for e in ei)); out["priors"] = float(sum(e*e for e in ep))
        out["SN"] = float(es@es); return out
    return np.concatenate([np.concatenate(eb), np.array(ei), np.array(ep), es])
def m_analytic(wde, wk, wb, wc, D):
    b = bg(wde, wb, wc, wk); r = D["MB"] - 5*np.log10((1 + zhel)*np.interp(zsn, zg, b[2])); return float(one@(Wsn@r)/A11)

def lsq(fun, x0, lb, ub, xs, free, nfev=200):
    x0 = np.asarray(x0, float).copy(); idx = np.where(free)[0]
    def f(y):
        x = x0.copy(); x[idx] = y; return fun(x)
    lo, hi = lb[idx], ub[idx]; y0 = np.clip(x0[idx], lo, hi)
    sol = least_squares(f, y0, bounds=(lo, hi), x_scale=xs[idx], method="trf", ftol=1e-10, xtol=1e-10, gtol=1e-10, max_nfev=nfev)
    x = x0.copy(); x[idx] = sol.x
    return float(2*sol.cost), x

A2S = np.interp(zg, NODES, WBEST)/WBEST[0]                  # branch S shape A(z)^2 (constant beyond 2.33)
APRIME0_S = 0.5*(WBEST[1]/WBEST[0] - 1)/0.4                 # d A/dz at z = 0 for branch S (node segment 0 - 0.4)

class Prof:
    """profile chi2 over (base, omega_k, omega_b, omega_c, M, phi) at fixed eps (x[-1]); x = [base(1|6), wk, wb, wc, M, phi, eps]"""
    def __init__(s, branch, P_, beta, D, phi_lo=-np.inf, phi_hi=np.inf, cap=1.0, window=None):
        s.br, s.P, s.beta, s.D, s.cap = branch, P_, beta, D, cap
        s.nb = NN if branch == "N" else 1
        s.amp = (1 + zg)**beta; s.k = 2*np.pi/P_
        s.win = np.ones_like(zg) if window is None else (zg > window).astype(float)
        s.lb = np.r_[[-2.0]*NN if branch == "N" else [1e-6], -0.25, 1e-4, 0.05, -np.inf, phi_lo, 0.0]
        s.ub = np.r_[[3.0]*NN if branch == "N" else [3.0], 0.25, 0.0499, 0.25, np.inf, phi_hi, cap]
        s.xs = np.r_[[0.03]*s.nb, 0.01, sb, sc, 0.01, 0.3, 0.05*cap]
        s.nfit = 0
    def wde(s, x):
        g = 1 + x[-1]*s.amp*s.win*np.sin(s.k*LN1Z + x[-2])
        base = np.interp(zg, NODES, x[:NN]) if s.br == "N" else (x[0]*A2S if s.br == "S" else x[0])
        return base*g*g
    def res(s, x):
        return residuals(s.wde(x), x[s.nb], x[s.nb + 1], x[s.nb + 2], x[s.nb + 3], s.D)
    def chi2(s, x): e = s.res(x); return float(e@e)
    def fit(s, x0, free_phi=True, free_eps=False, nfev=200):
        free = np.ones(len(x0), bool); free[-2] = free_phi; free[-1] = free_eps; s.nfit += 1
        return lsq(s.res, x0, s.lb, s.ub, s.xs, free, nfev)

BASE_EPS = [0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.45, 0.6, 0.8, 1.0]
PGRID = [0.05, 0.0625, 0.075, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]
PREP = [0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0]
D95 = 3.84

def start_x(branch, D):
    if branch == "N": x = np.r_[WBEST, PB[6], PB[7], PB[8], 0.0, 0.0, 0.0]
    elif branch == "S": x = np.r_[WBEST[0], PB[6], PB[7], PB[8], 0.0, 0.0, 0.0]
    else: x = np.r_[W_CONST, 0.0, wb0, wc0, 0.0, 0.0, 0.0]
    base = np.interp(zg, NODES, x[:NN]) if branch == "N" else (x[0]*A2S if branch == "S" else np.full_like(zg, x[0]))
    nb = NN if branch == "N" else 1
    x[-3] = m_analytic(base, x[nb], x[nb + 1], x[nb + 2], D)
    return x

def profile(pr, base_x, eps_grid, phis, label=""):
    """eps-profile with phi profiled; returns dict (base criteria section 4 / A1.2)"""
    t0 = time.time()
    x = base_x.copy(); x[-1] = 0.0
    chi0, x0 = pr.fit(x, free_phi=False)
    starts = []
    for ph in phis:
        xx = x0.copy(); xx[-2] = ph; starts.append(xx)
    rows = [dict(eps=0.0, chi=chi0, phi=None, x=x0.tolist())]; sols = {0.0: [s_.copy() for s_ in starts]}
    for e in eps_grid[1:]:
        new = []
        for st in starts:
            st = st.copy(); st[-1] = e; new.append(pr.fit(st))
        starts = [xx for _, xx in new]; sols[e] = [s_.copy() for s_ in starts]
        c, xx = min(new, key=lambda t: t[0])
        rows.append(dict(eps=e, chi=c, phi=float(xx[-2]), x=xx.tolist()))
    # global minimum: free eps refit from the three best grid rows
    order = np.argsort([r["chi"] for r in rows])
    best = (rows[order[0]]["chi"], np.array(rows[order[0]]["x"]))
    for i in order[:3]:
        if rows[i]["eps"] == 0.0: continue
        c, xx = pr.fit(np.array(rows[i]["x"]), free_phi=True, free_eps=True, nfev=400)
        if c < best[0]: best = (c, xx)
    chimin, xhat = best; ehat = float(xhat[-1])
    dd = np.array([r["chi"] - chimin for r in rows]); eg = np.array([r["eps"] for r in rows])
    def prof_at(e, sts):
        out = []
        for st in sts:
            st = np.array(st, float).copy(); st[-1] = e; out.append(pr.fit(st))
        return min(out, key=lambda t: t[0])
    res = dict(label=label, branch=pr.br, P=pr.P, beta=pr.beta, cap=pr.cap, chi0=chi0, chimin=chimin, eps_hat=ehat, phi_hat=float(xhat[-2]),
               x_hat=xhat.tolist(), x0=x0.tolist(), d0=float(chi0 - chimin), eps_grid=eg.tolist(), dchi2_grid=dd.tolist(), phi_grid=[r["phi"] for r in rows])
    p0 = float(CHI2.sf(max(res["d0"], 0), 2)); res["p0_local"] = p0; res["sigma0_local"] = float(NORM.isf(p0/2)) if p0 > 0 else 99.0
    # upper crossing
    up = [j for j in range(len(eg)) if eg[j] > ehat and dd[j] >= D95]
    res["eps95"], res["phi95"], res["x95"], res["bound_class"] = None, None, None, None
    if not up:
        res["bound_class"] = "NO BOUND" if pr.cap == 1.0 else "NO BOUND BELOW THE CAP"; res["eps95"] = pr.cap
    else:
        j = up[0]; lo = max(eg[j - 1], ehat); sts = sols[eg[j - 1]] + [np.array(rows[j]["x"])]
        if lo == ehat: sts = sts + [xhat]
        cache = {}
        def f(e):
            c, xx = prof_at(e, sts); cache[e] = xx; return c - chimin - D95
        try:
            if f(lo) >= 0: lo = ehat if ehat < lo else lo
            e95 = brentq(f, lo, eg[j], xtol=1e-3); xb = cache.get(e95)
            if xb is None: _, xb = prof_at(e95, sts)
            res["eps95"], res["phi95"], res["x95"], res["bound_class"] = float(e95), float(xb[-2]), xb.tolist(), "BOUNDED"
        except Exception as ex:
            res["eps95"], res["phi95"], res["x95"], res["bound_class"] = float(eg[j]), rows[j]["phi"], rows[j]["x"], f"BOUNDED (grid point; root failed: {ex})"
        res["disjoint"] = bool(any(dd[k] < D95 for k in range(j + 1, len(eg))))
        if res["disjoint"]: res["bound_class"] += " DISJOINT"
    # lower end of the 95% interval
    res["eps_lo"] = 0.0
    if res["d0"] >= D95 and ehat > 0:
        lows = [j for j in range(len(eg)) if eg[j] < ehat and dd[j] >= D95]
        j = lows[-1]; hi = min(eg[j + 1], ehat) if j + 1 < len(eg) else ehat
        sts = (sols[eg[j + 1]] if eg[j + 1] in sols and eg[j + 1] <= ehat else []) + [xhat]
        try:
            res["eps_lo"] = float(brentq(lambda e: prof_at(e, sts)[0] - chimin - D95, eg[j], hi, xtol=1e-3))
        except Exception:
            res["eps_lo"] = float(eg[j])
    res["seconds"] = time.time() - t0; res["nfit"] = pr.nfit
    return res

def wave_ratio(z, eps, P_, phi, beta=0.0):
    return (1 + eps*(1 + z)**beta*np.sin(2*np.pi*np.log1p(z)/P_ + phi))/(1 + eps*np.sin(phi))
def A_of(z, branch): return np.sqrt(np.interp(z, NODES, WBEST)/WBEST[0]) if branch == "S" else np.ones_like(np.asarray(z, float))
def wall():
    if time.time() - T0 > WALL_CAP:
        P(f"WALL CAP {WALL_CAP/3600:.1f} h EXCEEDED -> stop (base section 9: amendment before any rerun)"); return True
    return False
def summ(r):
    return (f"P {r['P']:<6} beta {r['beta']:<3} {r['branch']}: chi2_min {r['chimin']:.3f} eps_hat {r['eps_hat']:.4f} (phi {r['phi_hat'] % (2*np.pi):.2f}) "
            f"d0 {r['d0']:.2f} ({r['sigma0_local']:.2f} sigma local, 2 dof) | 95%: [{r['eps_lo']:.4f}, {r['eps95']:.4f}] {r['bound_class']} "
            f"phi95 {(r['phi95'] % (2*np.pi)) if r['phi95'] is not None else float('nan'):.2f}  ({r['seconds']:.0f} s, {r['nfit']} fits)")
def dump(obj, name):
    json.dump(obj, open(os.path.join(HERE, name), "w"), indent=1, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else float(o))
    P(f"wrote {name}  ({(time.time() - T0)/60:.1f} min)")

# ============================================================================================ K
if MODE == "K":
    out = dict(mode="K", sha256=SHAS, checks={})
    t = time.time(); c1 = chi2_689(PB); dt = time.time() - t
    out["checks"]["K1"] = dict(chi2=c1, stored=CHI_FREE, ok=bool(abs(c1 - CHI_FREE) <= 1e-3))
    P(f"K1: chi2 at CFG689 stored pbest {c1:.6f} vs stored {CHI_FREE:.6f} -> {'PASS' if out['checks']['K1']['ok'] else 'FAIL'}  ({dt*1e3:.2f} ms/eval)")
    e = residuals(np.interp(zg, NODES, WBEST), PB[6], PB[7], PB[8], m_analytic(np.interp(zg, NODES, WBEST), PB[6], PB[7], PB[8], DATA), DATA)
    out["checks"]["K1_residual_form"] = dict(chi2=float(e@e), ok=bool(abs(e@e - c1) <= 1e-6)); P(f"K1 residual form: {e@e:.6f} (same point, M explicit)")
    k2 = {}
    for br, tgt, tol in (("S", CHI_FREE, (0.05, 0.01)), ("C", CHI_CONST, (0.02, 0.02))):
        pr = Prof(br, 1.0, 0.0, DATA); x = start_x(br, DATA); c, xx = pr.fit(x, free_phi=False)
        k2[br] = dict(chi2=c, stored=tgt, x=xx.tolist(), ok=bool(tgt - tol[0] <= c <= tgt + tol[1]))
        P(f"K2 branch {br} at eps 0: chi2 {c:.4f} vs CFG689 {tgt:.4f} -> {'PASS' if k2[br]['ok'] else 'FAIL'}  (W {xx[0]:.5f} omega_k {xx[1]:+.5f} omega_b {xx[2]:.6f} omega_c {xx[3]:.5f})")
    out["checks"]["K2"] = dict(branches=k2, ok=bool(all(v["ok"] for v in k2.values())))
    # K3: CFG681 reproduction (CFG689's own K3)
    from scipy.optimize import minimize
    OMR681 = 2.469e-5/0.68**2*(1 + 0.2271*3.046); H2 = 0.68**2
    def chi681(om, use_sn):
        if not 0.15 <= om <= 0.45: return 1e9
        Hg = 100*np.sqrt(om*H2*(1 + zg)**3 + OMR681*H2*(1 + zg)**4 + (1 - om - OMR681)*H2)
        I = cumchi(Hg); return bao_chi2(Hg, I, None, DATA) + (sn_chi2(I, DATA) if use_sn else 0.0)
    r1 = minimize(lambda p: chi681(p[0], False), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
    r2 = minimize(lambda p: chi681(p[0], True), [0.30], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
    ok3 = bool(abs(r1.fun - 10.5515) <= 0.01 and abs(r1.x[0] - 0.2970) <= 0.001 and abs(r2.fun - 1400.143) <= 0.02 and abs(r2.x[0] - 0.3039) <= 0.001)
    out["checks"]["K3"] = dict(bao=[float(r1.fun), float(r1.x[0])], bao_sn=[float(r2.fun), float(r2.x[0])], ok=ok3)
    P(f"K3: BAO chi2 {r1.fun:.4f} Om {r1.x[0]:.5f} (10.5515, 0.2970); BAO+SN {r2.fun:.3f} Om {r2.x[0]:.5f} (1400.143, 0.3039) -> {'PASS' if ok3 else 'FAIL'}")
    # K5: a wave windowed to z > 2.5 (and, reported, z > 2.34) changes chi2 by exactly 0
    x = np.array(k2["S"]["x"]); base = Prof("S", 1.0, 0.0, DATA).chi2(x); k5, k5b = [], []
    for P_ in PGRID:
        for win, lst in ((2.5, k5), (2.34, k5b)):
            pr = Prof("S", P_, 0.0, DATA, window=win); xx = x.copy(); xx[-1] = 1.0
            lst.append(max(abs(pr.chi2(np.r_[xx[:-2], ph, 1.0]) - base) for ph in np.linspace(0, 2*np.pi, 8, endpoint=False)))
    out["checks"]["K5"] = dict(max_abs_dchi2_window_2p5=max(k5), max_abs_dchi2_window_2p34_reported=max(k5b), ok=bool(max(k5) <= 1e-9))
    P(f"K5: wave confined to z > 2.5 at eps 1, all 19 P, 8 phases: max |dchi2| = {max(k5):.2e} -> {'PASS' if max(k5) <= 1e-9 else 'FAIL'}; (reported) z > 2.34: {max(k5b):.2e}")
    # K4: CFG689's band at its nodes from this implementation, with CFG689's own sampler
    NSTEP = 60000
    s_ = np.r_[[0.03]*NN, 0.01, sb, sc]; f = lambda xx: chi2_689(PB + xx*s_); n = len(PB)
    def hess(fn, x0, h=0.1):
        H = np.zeros((n, n)); E = np.eye(n)*h
        for i in range(n):
            for j in range(i, n):
                H[i, j] = H[j, i] = (fn(x0 + E[i] + E[j]) - fn(x0 + E[i] - E[j]) - fn(x0 - E[i] + E[j]) + fn(x0 - E[i] - E[j]))/(4*h*h)
        return H
    H = hess(f, np.zeros(n))
    try: Cx = 2*np.linalg.inv(H); np.linalg.cholesky(Cx); hok = True
    except np.linalg.LinAlgError: Cx = np.diag(2/np.maximum(np.abs(np.diag(H)), 1e-6)); hok = False
    Lp = np.linalg.cholesky((2.38**2/n)*Cx); Ls = np.linalg.cholesky(Cx); chains, accs = [], []
    for seed in (6891, 6892, 6893, 6894):
        rng = np.random.default_rng(seed); xx = Ls@rng.standard_normal(n); fx = f(xx); k = 0
        while fx >= 1e8 and k < 60: xx = 0.5*xx; fx = f(xx); k += 1
        ch = np.empty((NSTEP, n)); acc = 0
        for i in range(NSTEP):
            y = xx + Lp@rng.standard_normal(n); fy = f(y)
            if fy < 1e8 and np.log(rng.random()) < -0.5*(fy - fx): xx, fx = y, fy; acc += 1
            ch[i] = xx
        chains.append(PB + ch[int(0.2*NSTEP):]*s_); accs.append(acc/NSTEP); P(f"  K4 chain seed {seed}: acceptance {acc/NSTEP:.4f}  ({(time.time() - T0)/60:.1f} min)")
    chains = np.array(chains); S = chains.reshape(-1, n)
    def rhat(c):
        m, nn = c.shape; W_ = c.var(axis=1, ddof=1).mean(); B = nn*c.mean(axis=1).var(ddof=1)
        return float(np.sqrt(((nn - 1)/nn*W_ + B/nn)/W_)) if W_ > 0 else float("inf")
    def wvec(z): return np.array([np.interp(z, NODES, np.eye(NN)[i]) for i in range(NN)])
    def sqx(Sx, z):
        wn = Sx[..., :NN]; w0 = wn[..., 0]; wz = wn@wvec(z); X = np.where(w0 > 0, wz/np.where(w0 > 0, w0, 1.0), -1.0); return np.sqrt(np.clip(X, 0, None))
    Q = [2.5, 16, 50, 84, 97.5]; band, okb = {}, []
    for z in ZS:
        q = np.percentile(sqx(S, z), Q); st = J689["BAO+SN"]["P1"][str(z)]["sqrtX_q"]
        tol = (0.02, 0.02, 0.02) if z < 2 else (0.10, 0.05, 0.05)      # (q16, q50, q84)
        d = [abs(q[1] - st[1]), abs(q[2] - st[2]), abs(q[3] - st[3])]; ok = all(a <= b for a, b in zip(d, tol)); okb.append(ok)
        band[str(z)] = dict(q=q.tolist(), stored=st, absdiff_q16_q50_q84=d, tol=tol, ok=bool(ok))
        P(f"K4 z {z}: sqrtX 68% [{q[1]:.3f}, {q[3]:.3f}] median {q[2]:.3f}  vs CFG689 [{st[1]:.3f}, {st[3]:.3f}] {st[2]:.3f} -> {'PASS' if ok else 'FAIL'}")
    nm, nsd = S[:, :NN].mean(0), S[:, :NN].std(0); smn, ssd = np.array(J689["BAO+SN"]["posterior"]["node_mean"]), np.array(J689["BAO+SN"]["posterior"]["node_std"])
    okn = bool(np.all(np.abs(nm - smn) <= 0.25*ssd) and np.all(np.abs(nsd/ssd - 1) <= 0.15))
    rh = {f"par{i}": rhat(chains[..., i]) for i in range(n)}; rh.update({f"sqrtX_{z}": rhat(sqx(chains, z)) for z in ZS}); okr = bool(max(rh.values()) < 1.02)
    P(f"K4 nodes: mean {np.round(nm, 4).tolist()} vs {np.round(smn, 4).tolist()}; std {np.round(nsd, 4).tolist()} vs {np.round(ssd, 4).tolist()} -> {'PASS' if okn else 'FAIL'}; "
      f"max R-hat {max(rh.values()):.4f} -> {'PASS' if okr else 'FAIL'}; acceptance {np.round(accs, 3).tolist()}; hessian_ok {hok}")
    out["checks"]["K4"] = dict(band=band, node_mean=nm.tolist(), node_std=nsd.tolist(), nodes_ok=okn, rhat=rh, rhat_ok=okr, accept=accs, hessian_ok=hok,
                               ok=bool(all(okb) and okn and okr))
    # A1.3 posterior fractions (reported): w(0.4) > w(0) and w(0.7) > w(0)  ->  a0 falling toward today
    dw4, dw7 = S[:, 1] - S[:, 0], S[:, 2] - S[:, 0]
    out["A13_posterior"] = dict(frac_w04_gt_w0=float(np.mean(dw4 > 0)), frac_w07_gt_w0=float(np.mean(dw7 > 0)), dw04_mean=float(dw4.mean()), dw04_std=float(dw4.std()),
                                dw07_mean=float(dw7.mean()), dw07_std=float(dw7.std()), n_samples=int(len(S)))
    P(f"A1.3 (reported): posterior P(w(0.4) > w(0)) = {np.mean(dw4 > 0):.3f} (dw {dw4.mean():+.4f} +- {dw4.std():.4f}); P(w(0.7) > w(0)) = {np.mean(dw7 > 0):.3f} (dw {dw7.mean():+.4f} +- {dw7.std():.4f})")
    allok = all(out["checks"][k]["ok"] for k in ("K1", "K2", "K3", "K4", "K5"))
    out["K_PASS"] = bool(allok); P(f"\nK overall: {'PASS' if allok else 'FAIL'}  (" + "; ".join(f"{k} {'PASS' if out['checks'][k]['ok'] else 'FAIL'}" for k in ("K1", "K2", "K3", "K4", "K5")) + ")")
    dump(out, "cfg956_K.json"); sys.exit(0)

# ============================================================================================ mocks (MUTATE)
def mock_data(eps, P_, phi, beta=0.0):
    wtrue = np.interp(zg, NODES, WBEST)*(1 + eps*(1 + zg)**beta*np.sin(2*np.pi*LN1Z/P_ + phi))**2
    om, Hg, DM, _ = bg(wtrue, PB[7], PB[8], PB[6]); rd = rdrag(PB[7], PB[8]); ms, mv = bao_pred(Hg, DM, DATA)
    DA = [(t[0], t[1], m[0]/rd, t[3], m[1]/rd, t[5], t[6]) for t, m in zip(ANISO, ms)]; DI = [(t[0], v/rd, t[2]) for t, v in zip(ISO, mv)]
    return dict(A=DA, I=DI, MB=5*np.log10((1 + zhel)*np.interp(zsn, zg, DM)))
def phis16(): return list(np.arange(16)*2*np.pi/16)
def phi_window(P_, beta):
    d = math.atan2(2*np.pi/P_, beta); return -d, np.pi - d
def phis8(P_, beta):
    lo, hi = phi_window(P_, beta); return [lo + (hi - lo)*(k + 0.5)/8 for k in range(8)]

if MODE == "MUTATE":
    out = dict(mode="MUTATE", rows={})
    Dm = mock_data(0.3, 0.5, 0.0)
    for P_ in (0.5, 0.25, 1.0):
        pr = Prof("S", P_, 0.0, Dm); r = profile(pr, start_x("S", Dm), BASE_EPS, phis16(), f"MUT-A P {P_}"); out["rows"][f"MUT-A P{P_}"] = r; P(summ(r))
    a = out["rows"]["MUT-A P0.5"]
    ok = bool(a["d0"] >= D95 and a["eps_lo"] <= 0.3 <= a["eps95"] and abs(a["eps_hat"] - 0.3) <= 0.03)
    out["MUT_A"] = dict(pass_=ok, d0=a["d0"], eps_hat=a["eps_hat"], interval=[a["eps_lo"], a["eps95"]])
    P(f"MUT-A (frozen): injected eps 0.3, P 0.5, phi 0 -> d0 {a['d0']:.1f} >= 3.84, eps_hat {a['eps_hat']:.4f}, 95% [{a['eps_lo']:.4f}, {a['eps95']:.4f}] -> {'PASS' if ok else 'FAIL'}")
    D0 = mock_data(0.0, 0.5, 0.0); pr = Prof("S", 0.5, 0.0, D0); r = profile(pr, start_x("S", D0), BASE_EPS, phis16(), "MUT-0 P 0.5"); out["rows"]["MUT-0"] = r; P(summ(r))
    out["MUT_0"] = dict(reported_only=True, d0=r["d0"], ok=bool(r["d0"] <= 0.1)); P(f"MUT-0 (reported): no injected wave -> d0 {r['d0']:.4f} (<= 0.1: {r['d0'] <= 0.1}); eps95 {r['eps95']:.4f}")
    cap = 3.5**-1.0; Dd = mock_data(0.1, 0.5, np.pi/2, beta=1.0); lo, hi = phi_window(0.5, 1.0)
    pr = Prof("S", 0.5, 1.0, Dd, phi_lo=lo, phi_hi=hi, cap=cap); r = profile(pr, start_x("S", Dd), [cap*e for e in BASE_EPS], phis8(0.5, 1.0), "MUT-D")
    out["rows"]["MUT-D"] = r; P(summ(r))
    okd = bool(r["d0"] >= D95 and r["eps_lo"] <= 0.1 <= r["eps95"] and abs(r["eps_hat"] - 0.1) <= 0.01)
    out["MUT_D"] = dict(pass_=okd, d0=r["d0"], eps_hat=r["eps_hat"], interval=[r["eps_lo"], r["eps95"]], cap=cap)
    P(f"MUT-D (frozen, A1.2): injected damped beta 1, P 0.5, eps0 0.1, phi pi/2 -> d0 {r['d0']:.1f}, eps0_hat {r['eps_hat']:.4f}, 95% [{r['eps_lo']:.4f}, {r['eps95']:.4f}] -> {'PASS' if okd else 'FAIL'}")
    out["MUTATE_PASS"] = bool(ok and okd); P(f"\nMUTATE overall (frozen MUT-A, MUT-D): {'PASS' if ok and okd else 'FAIL'}")
    dump(out, "cfg956_MUTATE.json"); sys.exit(0)

# ============================================================================================ galaxy points (base section 6)
A0C, A0A = 9.3603e-11, 1.1312e-10; FOOTS = {"canonical": A0C, "alt": A0A}
def galaxy_points():
    pts = []
    for r in csv.DictReader(open(os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv"))):
        if r["no_root"] == "0" and r["s_star"] not in ("", "nan"):
            pts.append(dict(label=f"{r['lane']} {r['object']}", src="chart_a0z_points.csv", z=float(r["z"]), s=float(r["s_star"]), lo68=float(r["stat68_lo"]), hi68=float(r["stat68_hi"])))
    j = json.load(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE_results.json"))); j = j.get("numbers", j)["points"]
    for grp, key in (("RC100", "B Q1"), ("RC100", "B Q2"), ("RC100", "B Q3"), ("CRISTAL", "R_e native, six"), ("CRISTAL", "R_out native, six, outermost data marker (primary)")):
        r = j[grp][key]; pts.append(dict(label=f"CFG303 {grp} {key}", src="CFG303", z=r["z_med"], s=r["s"], lo68=r["lo68"], hi68=r["hi68"]))
    r = j["RC100"]["B Q4"]; pts.append(dict(label="CFG303 RC100 B Q4 (no root; 95% upper bound only)", src="CFG303", z=r["z_med"], s=None, lo68=None, hi68=None, upper95=r["hi95"]))
    f9 = json.load(open(os.path.join(CFG, "CFG309_mightee_width_frame", "cfg309_cfg301chain_FRAME_summary.json")))["frame"]
    c1 = json.load(open(os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain", "cfg301_stageB_results.json")))["numbers"]["results"]
    pts.append(dict(label="CFG309 MeerKAT HI", src="CFG309/CFG301", z=float(np.median([c1[w]["z_med"] for w in ("W1", "W2", "W3")])), s=f9["s"], lo68=f9["q_a0"][1]/A0C, hi68=f9["q_a0"][2]/A0C))
    for p in pts:
        p["sigma_dex"] = None if p["lo68"] is None else 0.5*(math.log10(p["hi68"]) - math.log10(p["lo68"]))
        p["ratio_by_footing"] = None if p["s"] is None else {k: p["s"]*A0C/v for k, v in FOOTS.items()}
    return pts
PHIG = np.linspace(0, 2*np.pi, 720, endpoint=False)
def g1_shift(z, eps_list, beta=0.0, phi_ok=None):
    """largest |log10 (g(z)/g(0))| over (P, eps95) pairs and phi (conservative); returns (dex, P at max)"""
    best, Pb = 0.0, None
    for P_, e in eps_list:
        ph = PHIG if phi_ok is None else PHIG[phi_ok(P_)]
        r = (1 + e*(1 + z)**beta*np.sin(2*np.pi*np.log1p(z)/P_ + ph))/(1 + e*np.sin(ph))
        v = float(np.max(np.abs(np.log10(np.clip(r, 1e-3, None)))))
        if v > best: best, Pb = v, P_
    return best, Pb
zg6 = np.linspace(0, 6, 12001)
def dm_ext(x, branch, P_, beta=0.0):
    """D_M on z 0-6 for profile vector x (S/C branches), A(z) constant beyond 2.33, wave extended (base section 6, G2)"""
    eps, phi = x[-1], x[-2]; wk, wb, wc = x[1], x[2], x[3]
    base = x[0]*np.interp(zg6, NODES, WBEST)/WBEST[0] if branch == "S" else np.full_like(zg6, x[0])
    w = base*(1 + eps*(1 + zg6)**beta*np.sin(2*np.pi*np.log1p(zg6)/P_ + phi))**2
    E2 = (wb + wc)*(1 + zg6)**3 + OMR*(1 + zg6)**4 + wk*(1 + zg6)**2 + w
    return dm_from_chi(cumchi(100*np.sqrt(np.clip(E2, 1e-8, None)), zg6), wk)

# ============================================================================================ MAIN (plain wave, beta = 0)
if MODE == "MAIN":
    kj = json.load(open(os.path.join(HERE, "cfg956_K.json"))); KOK = kj["K_PASS"]
    P(f"K status from cfg956_K.json: {'PASS' if KOK else 'FAIL (main numbers unverified, no verdict)'}")
    out = dict(mode="MAIN", K_PASS=KOK, sha256=SHAS, P_grid=PGRID, eps_grid=BASE_EPS, rows={"S": [], "C": [], "N": []})
    stop = False
    for br, plist in (("S", PGRID), ("C", PGRID), ("N", PREP)):
        P(f"\n=== branch {br} ({'reported only' if br == 'N' else 'verdict'}) ===")
        for P_ in plist:
            if wall(): stop = True; break
            pr = Prof(br, P_, 0.0, DATA); r = profile(pr, start_x(br, DATA), BASE_EPS, phis16(), f"{br} P {P_}"); out["rows"][br].append(r); P(summ(r))
        if stop: break
    out["wall_cap_exceeded"] = stop
    if not stop:
        # wave preference class and representative table
        for br in ("S", "C", "N"):
            rr = out["rows"][br]; mx = max(rr, key=lambda r: r["d0"])
            cls = "NO WAVE PREFERRED" if mx["d0"] < 5.99 else ("LOCAL HINT" if mx["d0"] < 11.83 else "LOCAL >= 3 sigma (uncorrected)")
            emax = max(rr, key=lambda r: r["eps95"]); emin = min(rr, key=lambda r: r["eps95"])
            out[f"summary_{br}"] = dict(pref_class=cls, d0_max=mx["d0"], P_at_d0_max=mx["P"], eps_hat_at_d0_max=mx["eps_hat"], eps95_max=emax["eps95"], P_at_eps95_max=emax["P"],
                                        eps95_min=emin["eps95"], P_at_eps95_min=emin["P"], n_no_bound=sum(r["bound_class"].startswith("NO BOUND") for r in rr),
                                        n_disjoint=sum("DISJOINT" in r["bound_class"] for r in rr), weight="reported only" if br == "N" else "verdict")
            P(f"\nbranch {br}: eps95 from {emin['eps95']:.4f} (P {emin['P']}) to {emax['eps95']:.4f} (P {emax['P']}); wave preference: largest d0 {mx['d0']:.2f} at P {mx['P']} "
              f"(eps_hat {mx['eps_hat']:.3f}) -> {cls} [local, 2 dof; Bonferroni x{len(rr)} not applied]")
        # envelope of a0(z)/a0(0) at the bound (z 0.5, 1, 1.5, 2.33)
        ZE = (0.5, 1.0, 1.5, 2.33); env = {}
        for br in ("S", "C"):
            env[br] = []
            for r in out["rows"][br]:
                e = min(r["eps95"], 1.0); A = A_of(np.array(ZE), br)
                exact = (A*wave_ratio(np.array(ZE), e, r["P"], r["phi95"])).tolist() if r["phi95"] is not None else None
                env[br].append(dict(P=r["P"], eps95=e, lo=(A*(1 - e)).tolist(), hi=(A*(1 + e)).tolist(), at_bound_phi=exact))
        out["envelope_z"] = ZE; out["envelope"] = env
        # rho_DE share of H^2 at the CFG689 best fit (z > 2.5 is rho_m dominated)
        sh = {}
        for z in (2.5, 3.5, 4.5):
            wde = WBEST[-1]; E2 = (PB[7] + PB[8])*(1 + z)**3 + OMR*(1 + z)**4 + PB[6]*(1 + z)**2 + wde
            sh[str(z)] = dict(share=wde/E2, share_eps1_peak=4*wde/(E2 + 3*wde), H_change_eps1_peak=math.sqrt((E2 + 3*wde)/E2) - 1, H_change_eps1_trough=math.sqrt((E2 - wde)/E2) - 1)
        out["rhoDE_share_highz"] = sh
        P("rho_DE share of H^2 at the CFG689 best fit (reported): " + "; ".join(f"z {z}: {v['share']:.3f} (eps 1 peak: H {100*v['H_change_eps1_peak']:+.1f}%, trough {100*v['H_change_eps1_trough']:+.1f}%)" for z, v in sh.items()))
        # galaxy-side check (reported only)
        pts = galaxy_points(); gal = []
        for p in pts:
            row = dict(p)
            for br in ("S", "C"):
                el = [(r["P"], min(r["eps95"], 1.0)) for r in out["rows"][br]]
                v, Pm = g1_shift(p["z"], el); row[f"G1_{br}_dex"] = v; row[f"G1_{br}_P"] = Pm
                row[f"G1_{br}_over_sigma"] = None if p["sigma_dex"] is None else v/p["sigma_dex"]
                g2 = 0.0
                for r in out["rows"][br]:
                    if r["x95"] is None: continue
                    d1 = np.interp(p["z"], zg6, dm_ext(np.array(r["x95"]), br, r["P"])); d0_ = np.interp(p["z"], zg6, dm_ext(np.array(r["x0"]), br, r["P"]))
                    g2 = max(g2, abs(-2*math.log10(d1/d0_)))
                row[f"G2_{br}_dex"] = g2; row[f"G2_{br}_over_sigma"] = None if p["sigma_dex"] is None else g2/p["sigma_dex"]
            row["above_2p5_no_expansion_bound"] = bool(p["z"] > 2.5); gal.append(row)
            if p["sigma_dex"] is not None:
                P(f"  galaxy {p['label'][:58]:58s} z {p['z']:.3f} sigma68 {p['sigma_dex']:.3f} dex | G1 S {row['G1_S_dex']:.3f} ({row['G1_S_over_sigma']:.2f} sigma) "
                  f"C {row['G1_C_dex']:.3f} ({row['G1_C_over_sigma']:.2f}) | G2 S {row['G2_S_dex']:.4f} C {row['G2_C_dex']:.4f}" + ("  [z > 2.5: expansion allows eps <= 1 here]" if p["z"] > 2.5 else ""))
        out["galaxy"] = gal
        nexc = sum(1 for g in gal if g["sigma_dex"] is not None and max(g["G1_S_over_sigma"], g["G1_C_over_sigma"]) > 1)
        out["galaxy_summary"] = dict(n_points=sum(g["sigma_dex"] is not None for g in gal), n_G1_exceeds_sigma=nexc,
                                     n_G2_exceeds_sigma=sum(1 for g in gal if g["sigma_dex"] is not None and max(g["G2_S_over_sigma"], g["G2_C_over_sigma"]) > 1))
        P(f"galaxy-side (reported only): {nexc} of {out['galaxy_summary']['n_points']} points see an allowed-wave shift of the predicted a0 larger than their 68% error (G1, conservative); "
          f"G2 (distance) exceeds sigma for {out['galaxy_summary']['n_G2_exceeds_sigma']}")
        # ---------------- illustrative sketch (base section 5; A1.4: labelled 'illustrative sketch', never headlined)
        zs_, ss_ = np.array([0, 0.5, 2.5, 4.5]), np.array([1.0, 2.0, 0.3, 3.0])
        PCH = PchipInterpolator(np.log1p(zs_), np.log(ss_))
        def S_of(z): u = np.clip(np.log1p(np.asarray(z, float)), 0, np.log1p(4.5)); return np.exp(PCH(u))
        S2 = S_of(zg)**2
        def res_sk(x, Wfix=None):
            W = x[0] if Wfix is None else Wfix; o = 0 if Wfix is None else -1
            return residuals(W*S2, x[1 + o], x[2 + o], x[3 + o], x[4 + o], DATA)
        x0 = np.r_[WBEST[0], PB[6], PB[7], PB[8], m_analytic(WBEST[0]*S2, PB[6], PB[7], PB[8], DATA)]
        lb = np.r_[1e-6, -0.25, 1e-4, 0.05, -np.inf]; ub = np.r_[3.0, 0.25, 0.0499, 0.25, np.inf]; xs = np.r_[0.03, 0.01, sb, sc, 0.01]
        best = None
        for Wst in (0.05, 0.1, 0.2, WBEST[0]):
            xx = x0.copy(); xx[0] = Wst; xx[4] = m_analytic(Wst*S2, PB[6], PB[7], PB[8], DATA); c, xb = lsq(res_sk, xx, lb, ub, xs, np.ones(5, bool), 400)
            if best is None or c < best[0]: best = (c, xb)
        csk, xsk = best
        cfx, xfx = lsq(lambda y: res_sk(y, Wfix=WBEST[0]), x0[1:], lb[1:], ub[1:], xs[1:], np.ones(4, bool), 400)
        cC = min(r["chi0"] for r in out["rows"]["C"])
        blocks = residuals(xsk[0]*S2, xsk[1], xsk[2], xsk[3], xsk[4], DATA, blocks=True)
        blocks_ref = residuals(np.interp(zg, NODES, WBEST), PB[6], PB[7], PB[8], m_analytic(np.interp(zg, NODES, WBEST), PB[6], PB[7], PB[8], DATA), DATA, blocks=True)
        dC = csk - cC; cls = "EXCLUDED" if dC >= 9 else ("DISFAVOURED" if dC >= 4 else "ALLOWED")
        om = PB[7] + PB[8]; z5 = 0.5
        Eref = om*(1 + z5)**3 + OMR*(1 + z5)**4 + PB[6]*(1 + z5)**2 + np.interp(z5, NODES, WBEST)
        Esk = om*(1 + z5)**3 + OMR*(1 + z5)**4 + PB[6]*(1 + z5)**2 + float(S_of(z5))**2*WBEST[0]
        Eown = (xsk[2] + xsk[3])*(1 + z5)**3 + OMR*(1 + z5)**4 + xsk[1]*(1 + z5)**2 + float(S_of(z5))**2*xsk[0]
        H0ref = 100*math.sqrt(om + OMR + PB[6] + WBEST[0])
        z51 = 0.51; rdb = rdrag(PB[7], PB[8])
        Hsk51 = 100*math.sqrt(om*(1 + z51)**3 + OMR*(1 + z51)**4 + PB[6]*(1 + z51)**2 + float(S_of(z51))**2*WBEST[0])
        Hown51 = 100*math.sqrt((xsk[2] + xsk[3])*(1 + z51)**3 + OMR*(1 + z51)**4 + xsk[1]*(1 + z51)**2 + float(S_of(z51))**2*xsk[0])
        dh_sk, dh_own = C/Hsk51/rdb, C/Hown51/rdrag(xsk[2], xsk[3])
        out["illustrative_sketch"] = dict(points=dict(z=zs_.tolist(), s=ss_.tolist()), chi2=csk, x=xsk.tolist(), dchi2_vs_CFG689_nodes=csk - CHI_FREE,
            dchi2_vs_constant=dC, chi2_constant_this_impl=cC, class_vs_constant=cls, chi2_W_fixed=cfx, dchi2_W_fixed_vs_nodes=cfx - CHI_FREE, blocks=blocks, blocks_CFG689_best=blocks_ref,
            H_shift_z05_fixed_today=math.sqrt(Esk/Eref) - 1, H_shift_z05_own_fit=math.sqrt(Eown/Eref) - 1, H_ref_z05=100*math.sqrt(Eref), H0_ref=H0ref,
            own_fit_H0=100*math.sqrt(xsk[2] + xsk[3] + OMR + xsk[1] + xsk[0]),
            DH_rd_LRG1_fixed_today=dh_sk, DH_rd_LRG1_own_fit=dh_own, LRG1_DH_rd=21.863, LRG1_sigma=0.425,
            pull_LRG1_fixed_today=(dh_sk - 21.863)/0.425, pull_LRG1_own_fit=(dh_own - 21.863)/0.425)
        sk = out["illustrative_sketch"]
        P(f"\nILLUSTRATIVE SKETCH (not the hypothesis; A1.4): chi2 {csk:.1f} (W {xsk[0]:.4f}, omega_k {xsk[1]:+.4f}); dchi2 vs CFG689 nodes {csk - CHI_FREE:.1f}, vs constant {dC:.1f} -> {cls}; "
          f"W fixed at w_best(0): dchi2 {cfx - CHI_FREE:.1f}")
        P(f"  blocks (sketch fit): " + ", ".join(f"{k} {v:.1f}" for k, v in blocks.items()))
        P(f"  H(0.5) shift: {100*sk['H_shift_z05_fixed_today']:+.1f}% at fixed present-day parameters (rho_DE(0.5) = 4 w_best(0)); {100*sk['H_shift_z05_own_fit']:+.1f}% at the sketch's own fit; "
          f"D_H/r_d at z 0.51: {dh_sk:.3f} (fixed) / {dh_own:.3f} (own fit) vs LRG1 21.863 +- 0.425 -> pulls {sk['pull_LRG1_fixed_today']:+.1f} / {sk['pull_LRG1_own_fit']:+.1f} sigma")
    out["wording"] = "kappa = 1/2 FITTED; footings never pooled (ratio bounds identical on both by construction); not a closed theory; a bound on a wave is not evidence for a wave; nothing here favours the framework over LCDM."
    dump(out, "cfg956.json"); sys.exit(0)

# ============================================================================================ DAMPED (A1.2, A1.3)
if MODE == "DAMPED":
    kj = json.load(open(os.path.join(HERE, "cfg956_K.json"))); KOK = kj["K_PASS"]
    P(f"K status from cfg956_K.json: {'PASS' if KOK else 'FAIL (unverified, no verdict)'}")
    BETAS = (0.0, 0.5, 1.0, 2.0); ZA = (0.5, 1.0, 2.33, 3.0, 5.0); ZW = (3.0, 3.5, 4.0, 4.5, 5.0)
    out = dict(mode="DAMPED", K_PASS=KOK, betas=BETAS, P_grid=PGRID, rows={}, amp_z=ZA, window_z=ZW)
    stop = False
    for beta in BETAS:
        cap = 3.5**-beta
        for br in ("S", "C"):
            key = f"beta{beta}_{br}"; out["rows"][key] = []; P(f"\n=== damped beta {beta} branch {br} (cap eps0 <= {cap:.4f}; phase on the way down) ===")
            for P_ in PGRID:
                if wall(): stop = True; break
                lo, hi = phi_window(P_, beta); pr = Prof(br, P_, beta, DATA, phi_lo=lo, phi_hi=hi, cap=cap)
                r = profile(pr, start_x(br, DATA), [cap*e for e in BASE_EPS], phis8(P_, beta), f"damped {key} P {P_}")
                e = r["eps95"]; r["amp_at_z"] = {str(z): e*(1 + z)**beta for z in ZA}
                r["amp_flag_gt1"] = {str(z): bool(e*(1 + z)**beta > 1) for z in ZA}
                ph = r["phi95"]
                r["slope_z0_total"] = None if ph is None else float((APRIME0_S if br == "S" else 0.0) + e*(beta*np.sin(ph) + 2*np.pi/P_*np.cos(ph))/(1 + e*np.sin(ph)))
                # high-z window: eps0 in eps95*(0..1), every allowed phi; ratio clipped at 0
                phs = np.linspace(lo, hi, 181); win = {}
                for z in ZW:
                    A = float(A_of(np.array(z), br)); vals = []
                    for f_ in np.linspace(0, 1, 11):
                        vals.append(A*wave_ratio(z, f_*e, P_, phs, beta))
                    v = np.clip(np.concatenate(vals), 0, None); win[str(z)] = [float(v.min()), float(v.max())]
                r["window"] = win; out["rows"][key].append(r)
                P(summ(r) + "  amp z0.5/1/2.33/3/5: " + "/".join(f"{r['amp_at_z'][str(z)]:.3f}" for z in ZA))
            if stop: break
        if stop: break
    out["wall_cap_exceeded"] = stop
    if not stop:
        tab = {}
        for key, rr in out["rows"].items():
            mx = max(rr, key=lambda r: r["d0"]); cls = "NO WAVE PREFERRED" if mx["d0"] < 5.99 else ("LOCAL HINT" if mx["d0"] < 11.83 else "LOCAL >= 3 sigma (uncorrected)")
            amax = {str(z): max(r["amp_at_z"][str(z)] for r in rr) for z in ZA}
            wmin = {str(z): min(r["window"][str(z)][0] for r in rr) for z in ZW}; wmax = {str(z): max(r["window"][str(z)][1] for r in rr) for z in ZW}
            tab[key] = dict(pref_class=cls, d0_max=mx["d0"], P_at_d0_max=mx["P"], eps0_95_min=min(r["eps95"] for r in rr), eps0_95_max=max(r["eps95"] for r in rr),
                            n_no_bound=sum(r["bound_class"].startswith("NO BOUND") for r in rr), amp_max_at_z=amax, window_all_P=dict(lo=wmin, hi=wmax))
            P(f"\n{key}: eps0_95 {tab[key]['eps0_95_min']:.4f}-{tab[key]['eps0_95_max']:.4f} ({tab[key]['n_no_bound']} periods at the cap); largest allowed amplitude z0.5/1/2.33/3/5 = "
              + "/".join(f"{amax[str(z)]:.3f}" for z in ZA) + " (z 3, 5: no expansion datum; > 1 means a0 < 0 at troughs, physical cap 1); "
              f"z 3-5 window a0/a0(0) " + ", ".join(f"z{z}: [{wmin[str(z)]:.2f}, {wmax[str(z)]:.2f}]" for z in ZW) + f"; preference {cls} (d0 max {mx['d0']:.2f} at P {mx['P']})")
        out["summary"] = tab
        # galaxy-side (reported only) for the damped bound waves
        pts = galaxy_points(); gal = []
        for p in pts:
            if p["sigma_dex"] is None: continue
            row = dict(label=p["label"], z=p["z"], sigma_dex=p["sigma_dex"])
            for key, rr in out["rows"].items():
                beta = rr[0]["beta"]; el = [(r["P"], r["eps95"]) for r in rr]
                v, Pm = g1_shift(p["z"], el, beta=beta, phi_ok=lambda P_, b=beta: (b*np.sin(PHIG) + 2*np.pi/P_*np.cos(PHIG)) >= 0)
                row[f"G1_{key}"] = v; row[f"G1_{key}_over_sigma"] = v/p["sigma_dex"]
            gal.append(row)
        out["galaxy"] = gal
        for g in gal:
            worst = max((k for k in g if k.endswith("_over_sigma")), key=lambda k: g[k])
            P(f"  galaxy {g['label'][:58]:58s} z {g['z']:.3f} sigma {g['sigma_dex']:.3f} | largest damped G1/sigma {g[worst]:.2f} ({worst[3:-11]})" + ("  [z > 2.5: family extrapolation]" if g["z"] > 2.5 else ""))
        # A1.3: does CFG689's best fit prefer a0 rising or falling toward today?
        def res_nodes(x): return residuals(np.interp(zg, NODES, x[:NN]), x[NN], x[NN + 1], x[NN + 2], x[NN + 3], DATA)
        xN = np.r_[WBEST, PB[6], PB[7], PB[8], m_analytic(np.interp(zg, NODES, WBEST), PB[6], PB[7], PB[8], DATA)]
        lbN = np.r_[[-2.0]*NN, -0.25, 1e-4, 0.05, -np.inf]; ubN = np.r_[[3.0]*NN, 0.25, 0.0499, 0.25, np.inf]; xsN = np.r_[[0.03]*NN, 0.01, sb, sc, 0.01]
        cfree, xfree = lsq(res_nodes, xN, lbN, ubN, xsN, np.ones(len(xN), bool), 600); cfree = min(cfree, CHI_FREE)
        a13 = {}
        for j, zj in ((1, 0.4), (2, 0.7)):
            def res_tied(y, j=j):
                x = np.r_[y[:j], y[0], y[j:]]; return res_nodes(x)
            y0 = np.r_[np.delete(xN, j)]; y0[0] = 0.5*(WBEST[0] + WBEST[j])
            ct, yt = lsq(res_tied, y0, np.delete(lbN, j), np.delete(ubN, j), np.delete(xsN, j), np.ones(len(y0), bool), 600)
            d = ct - cfree; sgn = np.sign(WBEST[j] - WBEST[0])
            a13[f"w({zj}) vs w(0)"] = dict(dchi2_tied=float(d), sigma_signed=float(sgn*math.sqrt(max(d, 0))), best_fit_diff=float(WBEST[j] - WBEST[0]),
                                           reading="a0 falling toward today (larger in the past)" if sgn > 0 else "a0 rising toward today")
            P(f"A1.3 tied fit w({zj}) = w(0): dchi2 {d:.3f} -> {sgn*math.sqrt(max(d, 0)):+.2f} sigma (profile, 1 dof); best-fit w({zj}) - w(0) = {WBEST[j] - WBEST[0]:+.4f} -> {a13[f'w({zj}) vs w(0)']['reading']}")
        a13["posterior_from_K4"] = kj.get("A13_posterior"); a13["chi2_free_used"] = cfree
        a13["slope_dA_dz_z0_bestfit"] = APRIME0_S
        out["A13_rising_or_falling"] = a13
        # A1.3: the record's DESI DR2 CPL products (comparison only)
        pdir = os.path.join(ROOT, "sonnet55_push", "puzzle_32pi"); desi = {}
        try:
            txt = open(os.path.join(pdir, "p13c_desi_dr2_chains_a0z.out")).read()
            for m in re.finditer(r"PASS\s+A\s+(\S+): chain w0 (-?[0-9.]+)\+-([0-9.]+), wa (-?[0-9.]+)\+-([0-9.]+)", txt):
                w0, sw0 = float(m.group(2)), float(m.group(3))
                desi[m.group(1)] = dict(w0=w0, sigma_w0=sw0, wa=float(m.group(4)), sigma_wa=float(m.group(5)), dlnrho_dlna_today=-3*(1 + w0),
                                        sign_drho_dt_today="decreasing (a0 on the way down)" if w0 > -1 else "increasing", one_plus_w0_over_sigma=(1 + w0)/sw0)
            q = {}
            for r in csv.DictReader(open(os.path.join(pdir, "p13c_desi_dr2_chains_a0z.csv"))):
                if abs(float(r["z"]) - 0.05) < 1e-9: q[r["fit"]] = dict(q16=float(r["q16"]), q50=float(r["q50"]), q84=float(r["q84"]))
            for k, v in q.items(): desi.setdefault(k, {})["a0_ratio_z0p05"] = v
            out["A13_DESI_record"] = dict(source="sonnet55_push/puzzle_32pi/p13c_desi_dr2_chains_a0z.{out,csv} (record; not framework-native; comparison only)", fits=desi)
            for k, v in desi.items():
                P(f"A1.3 record DESI CPL (comparison only) {k}: " + (f"w0 {v['w0']:+.3f} +- {v['sigma_w0']:.3f} -> d ln rho_DE/d ln a = {v['dlnrho_dlna_today']:+.2f}, rho_DE {v['sign_drho_dt_today']} ((1+w0)/sigma {v['one_plus_w0_over_sigma']:+.1f}); " if "w0" in v else "")
                  + (f"a0(0.05)/a0(0) = {v['a0_ratio_z0p05']['q50']:.4f} [{v['a0_ratio_z0p05']['q16']:.4f}, {v['a0_ratio_z0p05']['q84']:.4f}]" if "a0_ratio_z0p05" in v else ""))
        except FileNotFoundError:
            out["A13_DESI_record"] = "not in record"; P("A1.3 DESI CPL: not in record")
    out["attribution"] = "The oscillating-a0(z) hypothesis, including its damped form, is the owner's idea (2026-10-21)."
    out["wording"] = "kappa = 1/2 FITTED; footings never pooled; z > 2.5 has no expansion datum (the z 3-5 window is a family extrapolation); not a closed theory; nothing here favours the framework over LCDM."
    dump(out, "cfg956_DAMPED.json"); sys.exit(0)
