# -*- coding: utf-8 -*-
"""CFG124 G1 -- can any term of the mimetic action make the dust follow CFG44's target?  (frozen: CFG124_FROZEN_CRITERIA.md, e8b9fbcdf)
Everything is dimensionless: s = r/r_M, m_b(s) = M_b(<r)/M, mu(s) = M_c(<r)/M, time in t0 = sqrt(r_M/a0), so a0 and G drop out (the
result is footing-independent and mass-independent for the two declared profiles: point mass and the exponential sphere with
h = 0.5 r_M, which is CFG44's h = 2 kpc at 1e10 Msun rescaled with r_M; the choice h = 0.5 r_M is declared here).
Target (CFG44):  C = rho r u = a0 M_b(<r)/4pi  <=>  d mu/d s = s m_b/(m_b + mu)  (P2 point mass: m_b + mu = sqrt(1+s^2)).
Checks: G1.0 control; G1.1 steady flows (Bernoulli + continuity; generous per-profile optimisation of the free constants);
G1.2 persistence (Lagrangian shells, pre-crossing, Newtonian, class-independent flow, T0.3); G1.3 the pressureless-static identity;
G1.4 reductions of the E couplings.  MUTATE a: dust receives f_ext = g_tot (hand-supplied support);  c: designed sink source;
b, 1: as declared (b unused here).
"""
import os, sys, math, json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from scipy.special import gammainc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG124_common as C

R = C.Report("CFG124_G1_target")
P = R.P
P(__doc__)
S0 = 1e-2
SG = np.geomspace(0.1, 30.0, 61)                    # scoring grid x in [0.1, 30]
GYR_PER_T0 = 1.0                                     # placeholder (time conversion is done in G1.2 with the footing)
PROFILES = {"point": lambda s: np.ones_like(np.asarray(s, float)),
            "expsphere": lambda s: gammainc(3.0, 2.0 * np.asarray(s, float))}           # h = 0.5 r_M -> r/h = 2 s
DMB = {"point": lambda s: np.zeros_like(np.asarray(s, float)),
       "expsphere": lambda s: 0.5 * (2.0 * np.asarray(s, float)) ** 2 * np.exp(-2.0 * np.asarray(s, float)) * 2.0 / 2.0 * 1.0}  # not used


def target_mu(name, sgrid):
    """mu_T(s): P2 closed form for the point mass; ODE d mu/ds = s m_b/(m_b+mu) (CFG44 'encl') for the exponential sphere."""
    mb = PROFILES[name]
    if name == "point":
        return np.sqrt(1 + sgrid ** 2) - 1
    s0 = 1e-4
    m0 = float(mb(s0)); mu0 = m0 * (math.sqrt(1 + s0 * s0 / m0) - 1)
    def rhs(ls, y):
        s = math.exp(ls); m = float(mb(s)); return [s * s * m / max(m + y[0], 1e-300)]
    sol = solve_ivp(rhs, (math.log(s0), math.log(sgrid[-1] * 1.0001)), [mu0], t_eval=np.log(sgrid), rtol=1e-11, atol=1e-16, method="Radau")
    return sol.y[0]


# ---------------------------------------------------------------------------------------------- G1.0 control
R.banner("G1.0  CONTROL (never counted as a pass): prescribing the target as initial data reproduces it; and the dimensionless target equals CFG44's committed target_fields")
sg = np.geomspace(0.1, 30, 2000)
dm = {}
for nm in PROFILES:
    mu = target_mu(nm, sg)
    mb = PROFILES[nm](sg)
    dmu = np.gradient(mu, np.log(sg)) / sg
    rho_t = dmu / (4 * math.pi * sg ** 2)
    ratio = 4 * math.pi * rho_t * sg * (mb + mu) / mb
    dm[nm] = float(np.max(np.abs(ratio[2:-2] - 1)))
R.check("G1.0a", "Cm(x) := C_44 at t0 gives C/C_44 = 1 to numerical differentiation error (initial data reproduces the target by choice: NOT a mechanism)", "max |ratio-1| = %s" % dm, max(dm.values()) < 1e-3)
try:
    B = C.import_bcommon()
    M = 1e10; rM = math.sqrt(B.G * M / B.A0)
    prof = B.exp_sphere(M, 0.5 * rM)
    tf = B.target_fields(prof, r0=1e-4 * rM, r1=40 * rM, n=2001)
    s_c = tf["r"] / rM
    sel = (s_c > 0.1) & (s_c < 30)
    mu_b = tf["w"] / (B.G * M)
    mu_me = target_mu("expsphere", s_c[sel])
    d1 = float(np.max(np.abs(mu_b[sel] / mu_me - 1)))
    R.check("G1.0b", "the dimensionless exponential-sphere target equals CFG44's Bcommon.target_fields (M = 1e10, h = 0.5 r_M) [imported read-only]", "max |mu_mine/mu_CFG44 - 1| = %.2e" % d1, d1 < 1e-4)
except Exception as e:
    R.check("G1.0b", "CFG44 Bcommon import / cross-check", "FAILED: %r" % (e,), False)

# ---------------------------------------------------------------------------------------------- G1.1 steady flows
R.banner("G1.1  stationary irrotational single-stream flows: rho v r^2 = Mdot(r) = A + B r^3 (B: the uniform source of class B), Bernoulli with Phi_tot (dust self-gravity included)")
P("  dimensionless ODE: d mu/ds = mdot(s)/sqrt(2 Psi), d Psi/ds = -(m_b + mu)/s^2, mdot = a + b s^3, Psi(s0) = m_b(s0) e^w / s0 (e^w = 1: parabolic free fall)")
P("  ratio C_flow/C_44 = mdot (m_b + mu)/(m_b s sqrt(2 Psi));  pass: sup |ratio - 1| <= 0.10 on 61 log points of s in [0.1, 30]")
def flow_ratio(name, a, b, w, designed=None):
    mb = PROFILES[name]
    m0 = float(mb(S0)); psi0 = m0 * math.exp(w) / S0
    def rhs(ls, y):
        s = math.exp(ls)
        mu, psi = y
        if psi <= 1e-14: return [0.0, 0.0]
        md = designed(s) if designed is not None else (a + b * s ** 3)
        return [s * md / math.sqrt(2 * psi), -s * (float(mb(s)) + mu) / s ** 2]
    sol = solve_ivp(rhs, (math.log(S0), math.log(SG[-1] * 1.001)), [0.0, psi0], t_eval=np.log(SG), rtol=1e-9, atol=1e-14, method="LSODA")
    if (not sol.success) or sol.y.shape[1] < SG.size:
        return None
    mu, psi = sol.y
    if np.min(psi) <= 1e-10:
        return None
    md = np.array([designed(s) if designed is not None else (a + b * s ** 3) for s in SG])
    return md * (mb(SG) + mu) / (mb(SG) * SG * np.sqrt(2 * psi)), mu, psi

# fast fixed-step RK4 in ln s for the SEARCH (the reported optimum is re-evaluated with LSODA in flow_ratio)
NG = 900
LG = np.linspace(math.log(S0), math.log(31.0), NG + 1); HG = LG[1] - LG[0]
_MB_CACHE = {}
def _mb_arrays(name):
    if name not in _MB_CACHE:
        mbf = PROFILES[name]
        sfull = np.exp(np.linspace(LG[0], LG[-1], 2 * NG + 1))
        _MB_CACHE[name] = (sfull, np.asarray(mbf(sfull), float))
    return _MB_CACHE[name]
def flow_fast(name, a, b, w):
    sfull, mbfull = _mb_arrays(name)
    mu = 0.0; psi = mbfull[0] * math.exp(w) / S0
    MU_ = np.empty(NG + 1); PS_ = np.empty(NG + 1); MU_[0] = mu; PS_[0] = psi
    def f(k, mu_, psi_):                       # k indexes sfull
        if psi_ <= 1e-12: return None
        s = sfull[k]
        return (s * (a + b * s ** 3) / math.sqrt(2 * psi_), -(mbfull[k] + mu_) / s)
    for i in range(NG):
        k0 = 2 * i
        k1 = f(k0, mu, psi)
        if k1 is None: return None
        k2 = f(k0 + 1, mu + 0.5 * HG * k1[0], psi + 0.5 * HG * k1[1])
        if k2 is None: return None
        k3 = f(k0 + 1, mu + 0.5 * HG * k2[0], psi + 0.5 * HG * k2[1])
        if k3 is None: return None
        k4 = f(k0 + 2, mu + HG * k3[0], psi + HG * k3[1])
        if k4 is None: return None
        mu += HG * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        psi += HG * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        MU_[i + 1] = mu; PS_[i + 1] = psi
    if np.min(PS_) <= 1e-10: return None
    lgS = np.log(SG)
    muS = np.interp(lgS, LG, MU_); psS = np.interp(lgS, LG, PS_)
    mbS = np.asarray(PROFILES[name](SG), float)
    return (a + b * SG ** 3) * (mbS + muS) / (mbS * SG * np.sqrt(2 * psS)), muS, psS

def sup_dev(name, a, b, w):
    if not (1e-8 < a < 1e8 and -8 < w < 30 and abs(b) < 1e3):           # search box
        return 1e3
    r = flow_fast(name, a, b, w)
    if r is None: return 1e3
    rat = r[0]
    if not np.all(np.isfinite(rat)) or np.any(rat <= 0): return 1e3
    return float(np.max(np.abs(rat - 1)))

rng = np.random.default_rng(124)
def optimise(name, use_b, seeds=()):
    """generous: random search (4000 / 12000 draws in the box) then Nelder-Mead (1500 its, explicit initial simplex) from the 10 best draws
    and from any supplied seeds; returns (smallest sup|ratio-1|, [log10 a, w, b])."""
    draws = []
    for trial in range(4000 if not use_b else 12000):
        la = rng.uniform(-3, 3); w = rng.uniform(-2, 12)
        b = 0.0
        if use_b:
            b = rng.choice([-1, 1]) * 10 ** rng.uniform(-8, 1)
        draws.append((sup_dev(name, 10 ** la, b, w), (la, w, b)))
    draws.sort(key=lambda q: q[0])
    starts = [np.array(d[1]) for d in draws[:10]] + [np.array(q, float) for q in seeds]
    best = (draws[0][0], np.array(draws[0][1]))
    for x0 in starts:
        if use_b:
            simplex = np.array([x0, x0 + [0.3, 0, 0], x0 + [0, 0.3, 0], x0 + [0, 0, 1e-3 if abs(x0[2]) < 1e-3 else 0.3 * x0[2]]])
            fun = lambda p: sup_dev(name, 10 ** p[0], p[2], p[1])
            res = minimize(fun, x0, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10, maxiter=1500, initial_simplex=simplex))
            cand = (res.fun, res.x)
        else:
            x2 = np.array([x0[0], x0[1]])
            fun = lambda p: sup_dev(name, 10 ** p[0], 0.0, p[1])
            res = minimize(fun, x2, method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10, maxiter=1500))
            cand = (res.fun, np.array([res.x[0], res.x[1], 0.0]))
        if cand[0] < best[0]: best = cand
    return best[0], np.array(best[1], float)

BEST = {}
if not C.MU("c"):
    for nm in PROFILES:
        for use_b in (False, True):
            seeds_ = [] if not use_b else [(BEST[(nm, False)][1][0], BEST[(nm, False)][1][1], sgn * b0) for sgn in (1, -1) for b0 in (1e-4, 1e-3, 1e-2)]
            f, p = optimise(nm, use_b, seeds_)
            if use_b and BEST[(nm, False)][0] < f:          # class A (b = 0) is a member of class B
                f, p = BEST[(nm, False)][0], BEST[(nm, False)][1].copy()
            BEST[(nm, use_b)] = (f, p)
            P("  %-10s class %s: best sup|ratio-1| = %.3f at (log10 a, w, b) = %s" % (nm, "B (a,b,w)" if use_b else "A (a,w)  ", f, np.round(p, 5)))
            r = flow_ratio(nm, 10 ** p[0], p[2], p[1])
            if r is not None:
                P("             LSODA re-evaluation of that optimum: sup|ratio-1| = %.3f (RK4 search value %.3f)" % (float(np.max(np.abs(r[0] - 1))), f))
                rat = r[0]
                P("             ratio at s = 0.1, 0.3, 1, 3, 10, 30: %s" % np.round(np.interp(np.log([0.1, 0.3, 1, 3, 10, 30]), np.log(SG), rat), 3))
    fA = min(BEST[(nm, False)][0] for nm in PROFILES); fB = min(BEST[(nm, True)][0] for nm in PROFILES)
    R.check("G1.1-A", "class A (no source): NO steady flow (a, w free, per profile, generous) lands within 10% of C_44 over x in [0.1, 30]", "best sup|ratio-1| over profiles = %.3f (point %.3f, exp sphere %.3f)" % (fA, BEST[("point", False)][0], BEST[("expsphere", False)][0]), fA > 0.10)
    R.check("G1.1-B", "class B (uniform source, a, b, w free, generous): still NO steady flow within 10%", "best sup|ratio-1| = %.3f (point %.3f, exp sphere %.3f)" % (fB, BEST[("point", True)][0], BEST[("expsphere", True)][0]), fB > 0.10)
    # the frozen screening expectation: 'the steady free-fall profile has slope -3/2 ... agreeing with the target only at x = 1'
    P("  the frozen screening statement compared free fall (w = 0) with the target: check its numbers")
    for nm in PROFILES:
        rr_ = flow_ratio(nm, 10 ** BEST[(nm, False)][1][0], 0.0, 0.0)
        if rr_ is not None:
            P("  %s: pure parabolic free fall (w = 0) with the best class-A Mdot: ratio at s = 0.1, 1, 30 = %s (frozen text: only x = 1 agrees)" % (nm, np.round(np.interp(np.log([0.1, 1, 30]), np.log(SG), rr_[0]), 3)))
    slope_t = lambda s: -1 - s ** 2 / (1 + s ** 2)
    P("  target log-slope d ln rho/d ln r at x = 0.1, 1, 30 = %s ; parabolic free-fall slope tends to -3/2 (r^-1/2 velocity); large-w (v = const) flow tends to -2" % np.round([slope_t(0.1), slope_t(1), slope_t(30)], 3))
    R.num("G1.1_best", {str(k): [float(v[0]), [float(q) for q in v[1]]] for k, v in BEST.items()})
    # implied homogeneous source of the best class-B fit (per profile) in units where S t_dyn is mass-independent: S = 3 b M sqrt(a0 r_M)/(4 pi r_M^4)
    R.num("G1.1_B_fit_b", {nm: float(BEST[(nm, True)][1][2]) for nm in PROFILES})
else:
    # MUTATE c: a designed sink: mdot(s) chosen so the flow IS the target: mdot = m_b s sqrt(2 Psi)/(m_b + mu_T) with Psi from Bernoulli with the target mass
    for nm in PROFILES:
        mbf = PROFILES[nm]
        sgd = np.geomspace(S0, 31, 4000)
        mu_d = target_mu(nm, sgd) if nm == "point" else None
        if nm == "expsphere":
            mu_d = np.interp(np.log(sgd), np.log(np.geomspace(1e-4, 31, 6000)), target_mu("expsphere", np.geomspace(1e-4, 31, 6000)))
        u_d = mbf(sgd) + mu_d
        psi_d = np.concatenate([[0.0], np.cumsum(0.5 * (u_d[1:] / sgd[1:] ** 2 + u_d[:-1] / sgd[:-1] ** 2) * np.diff(sgd))])
        psi_d = psi_d[-1] - psi_d + 5.0                        # Bernoulli: Psi(s) = Psi(31) + int_s^31 u/s'^2 ds', Psi(31) = 5 (free constant)
        md = lambda s, sg_=sgd, mu_=mu_d, ps_=psi_d, mb_=mbf: float(np.interp(s, sg_, mb_(sg_) * sg_ * np.sqrt(2 * ps_) / (mb_(sg_) + mu_)))
        # integrate with mu(s0) = mu_T(s0), Psi(s0) = psi_d[0]
        def rhs(ls, y, md=md, mbf=mbf):
            s = math.exp(ls); return [s * md(s) / math.sqrt(2 * y[1]), -s * (float(mbf(s)) + y[0]) / s ** 2]
        mu0 = float(np.interp(S0, sgd, mu_d))
        sol = solve_ivp(rhs, (math.log(sgd[0]), math.log(30.0)), [mu0, float(psi_d[0])], t_eval=np.log(SG), rtol=1e-10, atol=1e-13, method="LSODA")
        mu, psi = sol.y
        mdv = np.array([md(s) for s in SG])
        rat = mdv * (mbf(SG) + mu) / (mbf(SG) * SG * np.sqrt(2 * psi))
        dev = float(np.max(np.abs(rat - 1)))
        BEST[(nm, "c")] = dev
        P("  MUTATE c, %s: steady flow with the DESIGNED source (mdot(s) built from the target's own m_b + mu) has sup|ratio-1| = %.2e" % (nm, dev))
    R.check("G1.1-A/B (MUTATE c)", "[claim of the main run, now tested with a designed sink] no steady flow within 10%", "designed-sink best sup|ratio-1| = %s" % {k[0]: v for k, v in BEST.items()}, all(v > 0.10 for v in BEST.values()))

# ---------------------------------------------------------------------------------------------- G1.2 persistence
R.banner("G1.2  persistence of the prescribed target (v = 0 at t0): Lagrangian shells, Newtonian, pre-crossing; the flow is class-independent (T0.3a)")
P("  each shell i has Lagrangian mass coordinate mu_in,i = mu_T(s0_i) and falls radially; ordering holds until the inner shell reaches the centre (radial fall from rest),")
P("  so the first shell crossing at x is bracketed by T_ff(s0_i) <= t_cross,i <= T_ff(s0_{i+1}); the class-C source (beta = -gamma) does not move the shells (only the density along them).")
A0S = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KPC_M = 3.0856775814913673e19; G = 4.30091727e-6; GYR_PER_KPC_KMS = KPC_M / 1e3 / 3.15576e16
s_sh = np.geomspace(0.05, 40.0, 240)
def tff_point(s0):
    return math.pi / 2 * np.sqrt(s0 ** 3 / (2 * np.sqrt(1 + s0 ** 2)))          # radial Kepler fall, total inner mass sqrt(1+s0^2)
mu_pt = np.sqrt(1 + s_sh ** 2) - 1
def tff_num(name, s0, mu_in):
    """radial fall from rest to the centre in mb(s)+mu_in (dimensionless GM = 1): T = int ds / sqrt(2 (Phi(s0) - Phi(s))),
    with s = s0 cos^2(eta) (removes the endpoint singularity): T = int_0^{pi/2} 2 s0 cos(eta) sin(eta) d eta / sqrt(2 dPhi(s))."""
    mb = PROFILES[name]
    grid = np.geomspace(1e-7 * s0, s0, 12000)
    g = (mb(grid) + mu_in) / grid ** 2
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(grid))])
    dphi = cum[-1] - cum
    eta = (np.arange(6000) + 0.5) * (math.pi / 2) / 6000
    se = s0 * np.cos(eta) ** 2
    dp = np.interp(se, grid, dphi)
    # near the top dPhi ~ g(s0) (s0 - s): use it where the grid cannot resolve
    top = g[-1] * (s0 - se)
    dp = np.where(s0 - se < 5e-3 * s0, top, dp)
    return float(np.sum(2 * s0 * np.cos(eta) * np.sin(eta) / np.sqrt(2 * dp)) * (math.pi / 2) / 6000)
_chk = [tff_num("point", s0, math.sqrt(1 + s0 ** 2) - 1) / float(tff_point(s0)) - 1 for s0 in (0.1, 1.0, 10.0)]
R.check("G1.2-ctrl", "the numerical fall-time quadrature reproduces the analytic Kepler radial-fall time for the point mass to 1%", "relative errors at s0 = 0.1, 1, 10: %s" % np.round(_chk, 5), max(abs(q) for q in _chk) < 0.01)
mu_exp = target_mu("expsphere", s_sh)
T_ff = {"point": tff_point(s_sh), "expsphere": np.array([tff_num("expsphere", s0, m) for s0, m in zip(s_sh, mu_exp)])}
# time unit t0 = sqrt(r_M / a0)  [kpc/(km/s)] * 0.9778 Gyr
def t0_gyr(M, a0_si):
    a0 = a0_si * KPC_M / 1e6; rM = math.sqrt(G * M / a0); return math.sqrt(rM / a0) * GYR_PER_KPC_KMS
rows = []
tbl = {}
for foot, a0si in A0S.items():
    for M in (1e9, 1e10, 1e11, 1e12):
        t0 = t0_gyr(M, a0si)
        for nm in PROFILES:
            tf_ = T_ff[nm] * t0
            xs = (s_sh >= 0.3) & (s_sh <= 30)
            n_ok = int(np.sum(tf_[xs] >= 10.0))
            tbl[(foot, M, nm)] = (float(t0), float(tf_[xs].min()), float(tf_[xs].max()), n_ok, int(xs.sum()))
P("  T_ff (Gyr) over x in [0.3, 30] and count of shells whose fall time exceeds 10 Gyr (= no crossing before 10 Gyr possible):")
for k, v in tbl.items():
    P("    %-9s M=%.0e %-9s t0 = %.4f Gyr; T_ff(x in [0.3,30]) = %.3f ... %.2f Gyr; shells with T_ff >= 10 Gyr: %d of %d" % (k[0], k[1], k[2], v[0], v[1], v[2], v[3], v[4]))
worst = max(v[2] for v in tbl.values())
P("  largest T_ff over all masses, profiles, footings and x <= 30: %.2f Gyr (so the crossing at every scored x is before 10 Gyr)" % worst)
R.num("G1.2_T_ff_gyr_table", {"%s_%.0e_%s" % k: v for k, v in tbl.items()})
if not C.MU("a"):
    R.check("G1.2a", "NO scored x in [0.3, 30] keeps its shells uncrossed for 10 Gyr, for any of the four masses (both profiles, both footings): C(r) fails persistence at every x", "shells with T_ff >= 10 Gyr = %d of %d" % (sum(v[3] for v in tbl.values()), sum(v[4] for v in tbl.values())), sum(v[3] for v in tbl.values()) == 0)
else:
    R.check("G1.2a (MUTATE a)", "[claim of the main run] no scored shell keeps its target profile for 10 Gyr; with the hand-supplied f_ext = g_tot the shells are exactly static (infinite T_ff)", "with f_ext = g_tot: net acceleration of a shell at rest = g_tot - g_tot = 0 -> T_ff = inf for all %d shells" % sum(v[4] for v in tbl.values()), False)
# density drift before crossing (point mass, analytic Kepler): C(r,t)/C_44 at t = 0.3 T_ff(x=1) for shells x >= 1
def kepler_r(s0, mtot, t):
    """radial fall from rest: r = s0 cos^2 eta, t = sqrt(s0^3/(2 mtot)) (eta + sin eta cos eta)."""
    from scipy.optimize import brentq
    tau = t / math.sqrt(s0 ** 3 / (2 * mtot))
    if tau >= math.pi / 2: return 0.0
    eta = brentq(lambda e: e + math.sin(e) * math.cos(e) - tau, 0, math.pi / 2)
    return s0 * math.cos(eta) ** 2
def drift_point(t):
    s0 = np.geomspace(0.5, 40, 4000)
    mtot = np.sqrt(1 + s0 ** 2)
    r = np.array([kepler_r(a, m, t) for a, m in zip(s0, mtot)])
    ok = r > 0
    dmu_ds0 = s0 / mtot                                   # d mu/d s0 = s0 m_b/(m_b + mu)
    dr = np.gradient(r, s0)
    rho = dmu_ds0 / (4 * math.pi * r ** 2 * dr)
    ratio = 4 * math.pi * rho * r * (1 + (mtot - 1)) / 1.0        # (m_b + mu_in) = mtot ; m_b(r) = 1 for the point mass
    return s0, r, ratio
t_probe = 0.3 * float(tff_point(1.0))
s0d, rd, ratd = drift_point(t_probe)
sel = (rd > 0.1) & (s0d >= 1.0) & np.isfinite(ratd)
dev_probe = np.abs(ratd[sel] - 1)
P("  point-mass Kepler drift at t = 0.3 T_ff(x=1) = %.3f t0: for the shells with x0 in [1, 40], C(r,t)/C_44 - 1 ranges %.2f ... %.2f (median %.2f)" % (t_probe, (ratd[sel] - 1).min(), (ratd[sel] - 1).max(), np.median(ratd[sel] - 1)))
# POST-HOC (added after the G1.2b number was seen; labelled): drift at a fixed FRACTION of each shell's own fall time
def drift_local(frac):
    out = []
    for x0 in (1.0, 3.0, 10.0, 30.0):
        t = frac * float(tff_point(x0))
        s0 = np.geomspace(x0 / 1.3, x0 * 1.3, 401)
        mt = np.sqrt(1 + s0 ** 2)
        r = np.array([kepler_r(a_, m_, t) for a_, m_ in zip(s0, mt)])
        dr = np.gradient(r, s0)
        rho = (s0 / mt) / (4 * math.pi * r ** 2 * dr)
        rat = 4 * math.pi * rho * r * mt
        out.append(float(np.interp(x0, s0, rat)) - 1)
    return out
P("  POST-HOC: C(r,t)/C_44 - 1 for the shell at x0 = 1, 3, 10, 30 at t = 0.3 T_ff(x0): %s ; at t = 0.7 T_ff(x0): %s ; at t = 0.95 T_ff(x0): %s" % (np.round(drift_local(0.3), 3), np.round(drift_local(0.7), 3), np.round(drift_local(0.95), 3)))
R.num("G1.2_posthoc_drift", {"0.3": drift_local(0.3), "0.7": drift_local(0.7), "0.95": drift_local(0.95)})
R.check("G1.2b", "even before any crossing the prescribed profile drifts by more than 10% within 0.3 of the free-fall time at x = 1 (point mass, Kepler)", "median |C/C_44 - 1| over shells x0 in [1,40] = %.2f; max %.2f" % (np.median(dev_probe), dev_probe.max()), np.median(dev_probe) > 0.10 if not C.MU("a") else False)
# class C: rate of the gamma source relative to advection at the G2 bound and at the G1 scale (estimate, no feedback)
P("  class C (gamma): the only effect on eps is the source beta grad^2(theta), beta = -gamma (T0.5); relative to the advection eps*theta it is of order gt c^2/(2 v^2) with v the local circular speed")
for nm_, gt in (("G2-allowed gt ~ 4e-10", 4e-10), ("G1-scale gt ~ 2 sigma^2/c^2 = V_f^2/c^2 (M=1e10: V_f = 76 km/s)", (76.0 / 299792.458) ** 2)):
    vc2 = (76.0 / 299792.458) ** 2
    P("    %-60s gt/(2 vc^2/c^2) = %.2e" % (nm_, gt / (2 * vc2)))
R.num("G1.2_classC_ratio", {"at_G2_bound": 4e-10 / (2 * (76 / 299792.458) ** 2), "at_G1_scale": 0.5})

# ---------------------------------------------------------------------------------------------- G1.3 identity
R.banner("G1.3  pressureless-static identity: p_eff = 0 => the target is static iff f_ext = g_tot (outward) at every r")
mu_p = np.sqrt(1 + sg ** 2) - 1
g_tot = (1 + mu_p) / sg ** 2; y = 1 / sg ** 2; g_law = np.sqrt(y ** 2 + y)
r_pm = float(np.max(np.abs(g_tot / g_law - 1)))
mu_e = target_mu("expsphere", sg); mb_e = PROFILES["expsphere"](sg)
g_tot_e = (mb_e + mu_e) / sg ** 2; y_e = mb_e / sg ** 2; g_law_e = np.sqrt(y_e ** 2 + y_e)
P("  exponential sphere: g_tot(target)/g_law(P2) over x in [0.1, 30]: min %.3f, max %.3f (reported)" % ((g_tot_e / g_law_e).min(), (g_tot_e / g_law_e).max()))
R.check("G1.3a", "point mass: f_ext/g_law = g_tot(target)/g_law(P2) = 1 identically (P2: g = sqrt(g_N^2 + a0 g_N) IS the target's g_tot)", "max |f_ext/g_law - 1| = %.1e" % r_pm, r_pm < 1e-12)
a_res = g_tot                                            # net inward acceleration of the resting dust with f_ext = 0, in units of a0
R.check("G1.3b", "with no external force the resting target dust accelerates inward at a_res = g_tot (order g_law) at every x; a static state needs f_ext = g_tot", "a_res/g_law: point mass min %.3f max %.3f" % ((a_res / g_law).min(), (a_res / g_law).max()), (np.min(a_res / g_law) > 0.99) if not C.MU("a") else False)
P("  corollary (structural): f_ext = g_tot(total) cancels the dust's gravity inside bound systems; in the linear regime at z >~ 10 the dust must feel gravity (G2). The coupling therefore has to switch: Gap 1's owner switch.")

# ---------------------------------------------------------------------------------------------- G1.4 reductions
R.banner("G1.4  reductions of the class E couplings (cited results are NOT re-run)")
import sympy as sp
Fh, Ph, fh, X_ = sp.symbols('F Phi f x')
# E1: X = -F(rho_b): first-order HJ: -(1-2Phi)(1+pi_t)^2 = -F, F = 1+2 f  =>  pi_t = Phi + f
pit = sp.symbols('pit')
sol = sp.solve(sp.Eq((1 - 2 * Ph) * (1 + pit) ** 2, 1 + 2 * fh), pit)
ee = sp.symbols('ee')
lin = [sp.simplify(sp.series(q.subs({fh: ee * fh, Ph: ee * Ph}), ee, 0, 2).removeO().subs(ee, 1)) for q in sol]      # first order in (Phi, f) jointly
ok_e1 = any(sp.simplify(q - (Ph + fh)) == 0 for q in lin)
R.check("G1.4a", "E1 (constraint g^{mu nu} phi_mu phi_nu = -F(rho_b), F = 1 + 2f): the dust's weak-field HJ potential is Phi + f, i.e. an EXTRA LOCAL force -grad f(rho_b)  [-> CFG44 B3 far-shell theorem and reciprocity class]", "linearised branches: %s" % lin, ok_e1)
# E1 locality: two baryon systems with identical rho_b on r >= 1 kpc but different interior mass need different f
Gk, a0 = 4.30091727e-6, 2888.3
def g_p2(Menc, r): gN = Gk * Menc / r ** 2; return np.sqrt(gN ** 2 + a0 * gN)
MA = lambda r, h=2.0, M=1e10: M * gammainc(3.0, r / h)
rr = np.array([3.0, 4.0, 6.0, 10.0]); dM = 5e9                        # B = A + a compact core 5e9 inside 0.3 kpc: rho_b identical for r > 0.3 kpc
gA = g_p2(MA(rr), rr); gB = g_p2(MA(rr) + dM, rr)
R.check("G1.4b", "E1 locality: two baryon systems with IDENTICAL rho_b(r) (and all its derivatives) for r > 0.3 kpc but different interior mass need forces on the dust that differ by > 10%: no local F(rho_b) serves both (consistent with CFG44 B3)", "g_tot(B)/g_tot(A) at r = 3, 4, 6, 10 kpc = %s" % np.round(gB / gA, 3), bool(np.all(np.abs(gB / gA - 1) > 0.10)))
nu_pm = np.sqrt(1 + sg ** 2)
R.check("G1.4c", "E2 (a force proportional to the baryon field, f = beta g_N with a constant beta): needs g_tot/g_N = sqrt(1+x^2) = 1.005 ... 30 over x in [0.1, 30]; no constant beta lands within 10% [CFG44 B2 fixed-kernel exclusion]", "max/min of g_tot/g_N = %.1f" % (nu_pm.max() / nu_pm.min()), nu_pm.max() / nu_pm.min() > 1.21)
P("  E3 (enclosed-mass functional): CFG48 G4 / CFG70 / CFG72 results are cited: reaction 0.06-22 g_law, energy 23-318 x the baryon orbital energy, stability of the coupled operator open/fragile. Not re-run here.")
P("  E4 (local source V(phi, rho_b)): the source is a local function of rho_b(r): the far-shell argument of G1.4b applies; the mass budget also fails: the dust needed at x = 30 is M_c = 29 M_b.")
mass_ratio = float(np.sqrt(1 + 30.0 ** 2) - 1)
R.check("G1.4d", "E4 baryon-to-dust conversion cannot supply the target: M_c/M_b = sqrt(1+x^2) - 1 reaches 29 at x = 30 (baryons cannot be converted into 29 times their own mass); a vacuum-to-dust transfer is door 8", "M_c/M_b(x=30) = %.1f" % mass_ratio, mass_ratio > 10)
if C.MU("a"):
    R.check("G1-MUTATE(a)", "[control] with f_ext = g_tot supplied by hand, G1.2/G1.3 flip to PASS: shells at rest stay at rest", "a_net = g_tot - f_ext = 0", False)
nf = R.write()
sys.exit(1 if nf else 0)
