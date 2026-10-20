#!/usr/bin/env python3
"""CFG893: does any new structure in the cold-energy equations select kappa (a0 = kappa c sqrt(G rho_DE))?

Criteria: FROZEN_CRITERIA.md (committed alone first).  kappa = 1/2 is FITTED; footings 9.3603e-11 (can) / 1.1312e-10 (alt) are
kappa-conditional and never pooled.  Cold energy is real gravitating mass; no particle species; not "theory closed".

Run:     OMP_NUM_THREADS=1 nice -n 10 python3 cfg893.py            -> cfg893.out, cfg893_results.json (exit 0 iff K1-K12 pass)
MUTATE:  CFG893_MUTATE=1 ... (M1 sink sign flipped, M2 gate threshold d > theta rho_m, theta = 1)
         -> cfg893_MUTATE.out, cfg893_results_MUTATE.json; exit 1 by design when every tooth bites (3 if a tooth does not bite).

Inputs (read only): CFG541 results JSON (C1 drift speeds, settling energy per mass); cfg515_lib (census f_ret).  Nothing
downloaded.  One process, seconds to a minute, < 300 MB.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG515_census_edge_resolution"))
from cfg515_lib import fret_census, FB, COLD_PER_B  # noqa: E402  (read-only import)

MUT = os.environ.get("CFG893_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT, RES, KT = [], {"lane": "CFG893", "mutate": MUT}, {}


def log(s=""):
    print(s)
    OUT.append(s)


def kt(name, ok, detail=""):
    KT[name] = dict(ok=bool(ok), detail=str(detail))
    log(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ----------------------------------------------------------------------------------------------------- constants (SI)
G_, C_, MSUN, KPC, MPC = 6.674e-11, 2.99792458e8, 1.989e30, 3.0857e19, 3.0857e22
h = 0.674
OM = 0.14237 / h ** 2                       # engine Omega_m (CFG541 settings)
OL = 0.685                                  # CFG493 definition of rho_Lambda = Omega_Lambda rho_crit
H0 = 100 * h * 1e3 / MPC
RHOCRIT = 3 * H0 ** 2 / (8 * math.pi * G_)
RHOM = OM * RHOCRIT
FOOT = {"can": 9.3603e-11, "alt": 1.1312e-10}
RHOFOOT = {"can": OL * RHOCRIT, "alt": RHOCRIT}   # density each footing's kappa refers to
KFIT = 0.5
R_COLD = COLD_PER_B                          # 5.364 = (1 - f_b)/f_b
KAPPA_RANGE = (0.01, 100.0)
ALPHA_MAX_RECORD = 1.186                     # CFG542 K9 causality maximum (q = 1 - f_b)


def kappa_of(a0, foot):
    return a0 / (C_ * math.sqrt(G_ * RHOFOOT[foot]))


def delta_ta(z=0.0):
    """CFG541's spherical-collapse turnaround overdensity (algorithm copied from cfg541.py, OM engine, OL = 1 - OM)."""
    om, ol = OM, 1.0 - OM
    ai = 1e-3

    def run(di):
        Ri = ai * (1 - di / 3.0)
        GM = 0.5 * om * (1 + di) * Ri ** 3 / ai ** 3
        Hi = math.sqrt(om / ai ** 3 + ol)

        def rhs(t, y):
            a, R, V = y
            return [a * math.sqrt(om / a ** 3 + ol), V, -GM / R ** 2 + ol * R]
        ev = lambda t, y: y[2]
        ev.terminal = True
        ev.direction = -1
        so = solve_ivp(rhs, [0, 50], [ai, Ri, Hi * Ri * (1 - di / 3.0)], events=ev, rtol=1e-10, atol=1e-13)
        if not so.t_events[0].size:
            return None
        a, R, _ = so.y_events[0][0]
        return a, (1 + di) * (Ri / ai) ** 3 * a ** 3 / R ** 3
    at = 1 / (1 + z)
    lo, hi = 1e-4, 0.05
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        r = run(mid)
        if r is None or r[0] > at:
            lo = mid
        else:
            hi = mid
    return run(hi)[1]


# ----------------------------------------------------------------------------------------------------- sympy symbols
P = dict(positive=True)
G, c, a0, kap, M, Mb, Mta, Mcat, Mcl = sp.symbols("G c a0 kappa M M_b M_ta M_cat M_cl", **P)
r, x, rta, rstar, rM, Ls, t = sp.symbols("r x r_ta r_star r_M L_star t", **P)
rho_DE, rho_m, rho_c, rho_ph, rho_e, rho_b = sp.symbols("rho_DE rho_m rho_c rho_ph rho_edge rho_b", **P)
gN, g, y, s, V, sig, vs, tau, taupsi = sp.symbols("g_N g y s V sigma v_s tau tau_psi", **P)
alpha, beta, fb, fret, Dta, q, X, theta, ff, Delta = sp.symbols("alpha beta f_b f_ret Delta_ta q X theta f Delta_loc", **P)
eps, Qb, Hh, Gam, psi, Phi, xi, lam = sp.symbols("epsilon_DE Qbar H Gamma psi Phi xi lambda", **P)
w = sp.Symbol("w", real=True)
u, K, Wp, Lstar, Pp = sp.symbols("u K Wprime Lstar P_pol", **P)

nu_mono = lambda Y: 1 / (1 - sp.exp(-sp.sqrt(Y)))
nu_simp = lambda Y: sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / Y)
KERNELS = {"nu_mono": nu_mono, "simple": nu_simp}

# (M, L, T) dimensions
DIM = {}
for sym_, d_ in [((G, K), (-1, 3, -2)), ((c, V, sig, vs), (0, 1, -1)),
                 ((rho_DE, rho_m, rho_c, rho_ph, rho_e, rho_b), (1, -3, 0)),
                 ((M, Mb, Mta, Mcat, Mcl), (1, 0, 0)), ((r, x, rta, rstar, rM, Ls, Lstar), (0, 1, 0)),
                 ((a0, gN, g, u), (0, 1, -2)), ((t, tau, taupsi), (0, 0, 1)), ((Hh, Gam), (0, 0, -1)),
                 ((psi, Phi), (0, 2, -2)), ((eps,), (1, -1, -2)), ((Qb,), (1, -1, -3)), ((Wp,), (1, -2, 0)),
                 ((Pp,), (1, -2, 0)),
                 ((kap, alpha, beta, fb, fret, Dta, q, X, theta, ff, Delta, y, s, xi, lam, w), (0, 0, 0))]:
    for z_ in sym_:
        DIM[z_] = np.array(d_, float)


def dims(e):
    """(M, L, T) exponents of a sympy expression; raises on inconsistent sums or dimensional function arguments."""
    e = sp.sympify(e)
    if e.is_Number or e in (sp.pi, sp.E):
        return np.zeros(3)
    if e.is_Symbol:
        return DIM[e]
    if isinstance(e, sp.Mul):
        return sum((dims(a) for a in e.args), np.zeros(3))
    if isinstance(e, sp.Pow):
        if not e.exp.is_Number:
            if np.any(dims(e.exp)):
                raise ValueError("dimensional exponent")
            if np.any(dims(e.base)):
                raise ValueError("symbolic power of a dimensional base")
            return np.zeros(3)
        return dims(e.base) * float(e.exp)
    if isinstance(e, sp.Add):
        ds = [dims(a) for a in e.args]
        for d_ in ds[1:]:
            if not np.allclose(d_, ds[0]):
                raise ValueError(f"inconsistent sum {e}")
        return ds[0]
    if isinstance(e, (sp.Function, sp.exp, sp.log)):
        for a in e.args:
            if np.any(dims(a)):
                raise ValueError(f"dimensional argument in {e}")
        return np.zeros(3)
    raise ValueError(f"cannot dimension {e!r}")


def dim_ok(lhs, rhs):
    try:
        return bool(np.allclose(dims(lhs), dims(rhs))), f"{dims(lhs).tolist()} vs {dims(rhs).tolist()}"
    except ValueError as err:
        return False, str(err)


# ----------------------------------------------------------------------------------------------------- the classifier
FREE_CONSTS = {alpha, beta, Ls, Lstar, sig, theta, Delta, q, xi, ff}
EMPIRICAL = {fret, Mcl, X}
OMEGA_LIKE = {rho_m, fb, Dta}               # appear in k only through cosmic density ratios (z-dependent)


def classify(lhs, rhs, kind="eq", hyp=None, solve_var=a0):
    """Frozen classes (FROZEN_CRITERIA section 1), first that applies."""
    e = sp.simplify(sp.expand(lhs - rhs)) if kind == "eq" else None
    if kind == "ineq":
        return dict(cls="JOINT/BOUND", why="inequality")
    if e == 0:
        return dict(cls="IDENTITY", why="holds identically")
    if solve_var not in e.free_symbols:
        return dict(cls="IDENTITY", why="a0-free (holds for every a0)")
    sols = [z_ for z_ in sp.solve(e, solve_var) if z_.is_positive is not False]
    if not sols:
        return dict(cls="EXCLUDED", why="no positive solution for a0")
    sol = sp.simplify(sols[0])
    mexp = sp.simplify(Mb * sp.diff(sol, Mb) / sol) if Mb in sol.free_symbols else sp.Integer(0)
    k = sp.simplify(sol / (c * sp.sqrt(G * rho_DE)))
    base = dict(a0_solution=str(sol), M_b_exponent=str(mexp), k=str(k))
    if mexp != 0:
        return dict(base, cls="MASS-DEPENDENT", why=f"d ln a0/d ln M_b = {mexp}")
    fs = k.free_symbols
    if not fs:
        return dict(base, cls="SELECTED" if hyp is None else f"SELECTED UNDER HYPOTHESIS {hyp}", why=f"k = {k}")
    if fs <= (FREE_CONSTS | EMPIRICAL | OMEGA_LIKE | {rho_DE}):
        return dict(base, cls="JOINT/BOUND", why=f"k depends on {sorted(map(str, fs))}")
    return dict(base, cls="JOINT/BOUND", why=f"not of the form k c sqrt(G rho_DE): k depends on {sorted(map(str, fs))}")


REL = {}


def record(name, label, src, hyp, cls, dimchk, extra=None):
    REL[name] = dict(statement=label, source=src, added_hypothesis=hyp, cls=cls["cls"], why=cls.get("why", ""),
                     dims_ok=dimchk[0], dims=dimchk[1], **{k_: v_ for k_, v_ in cls.items() if k_ not in ("cls", "why")},
                     **(extra or {}))
    log(f"  {name}: [{cls['cls']}] {label}  ({cls.get('why', '')}); dims {'ok' if dimchk[0] else 'FAIL ' + dimchk[1]}")


# =====================================================================================================================
log("CFG893: does any new structure in the cold-energy equations select kappa?  (kappa = 1/2 FITTED; footings never pooled)")
log(f"mode: {'MUTATE (M1 sink sign flipped; M2 gate threshold theta = 1)' if MUT else 'normal'}")
DTA = delta_ta()
log(f"inputs: h {h}, Omega_m {OM:.5f}, Omega_Lambda {OL}, rho_crit {RHOCRIT:.5e} kg/m^3, f_b {FB:.5f}, 5.364 -> {R_COLD:.4f}, "
    f"Delta_ta(0) {DTA:.4f}")

# ------------------------------------------------------------------------------------------------ K-tests: limits etc.
log("\nK-TESTS (identities and limits)")
# K1 deep limit, K2 Newtonian limit
k1, k2 = [], []
for nm, nu in KERNELS.items():
    gexpr = nu(gN / a0) * gN
    lim_deep = sp.limit((gexpr ** 2 / (gN * a0)).subs(gN, a0 * s ** 2), s, 0, "+")
    lim_newt = sp.limit((gexpr / gN).subs(gN, a0 * s ** 2), s, sp.oo)
    k1.append((nm, lim_deep))
    k2.append((nm, lim_newt))
Vsol = sp.solve(sp.Eq((V ** 2 / r) ** 2, (G * Mb / r ** 2) * a0), V)
kt("K1 deep limit g^2/(g_N a0) -> 1; V^4 = G M_b a0", all(sp.simplify(v_ - 1) == 0 for _, v_ in k1)
   and any(sp.simplify(v_ ** 4 - G * Mb * a0) == 0 for v_ in Vsol), f"{k1}; V = {Vsol}")
kt("K2 Newtonian limit g/g_N -> 1", all(sp.simplify(v_ - 1) == 0 for _, v_ in k2), f"{k2}")
# K3 by-construction catchment identity
ratio = sp.simplify(((1 - fb) * Mta) / (fret * fb * Mta))
kt("K3 M_cat/M_b,now = (1-f_b)/(f_b f_ret), a0-free (by construction)",
   sp.simplify(ratio - (1 - fb) / (fb * fret)) == 0 and a0 not in ratio.free_symbols, f"{ratio}")
# K4 census edge, both kernels (point mass: M_ph(<r) = (nu(y) - 1) M, y = (r_M/r)^2 = 1/x^2)
Rs = sp.Symbol("R", positive=True)
xm = sp.solve(sp.Eq(1 / (sp.exp(1 / x) - 1), Rs / fret), x)
xs = sp.solve(sp.Eq(sp.sqrt(sp.Rational(1, 4) + x ** 2) - sp.Rational(1, 2), Rs / fret), x)
xm_expr = [z_ for z_ in xm][0]
xs_expr = [z_ for z_ in xs][0]
xm01 = float(xm_expr.subs({Rs: R_COLD, fret: 0.1}))
xs01 = float(xs_expr.subs({Rs: R_COLD, fret: 0.1}))
lib01 = 1.0 / math.log1p(0.1 * FB / (1 - FB))
kt("K4 census edge: nu_mono r_*/r_M = 1/ln(1 + f_ret f_b/(1-f_b)); simple ~ 54 at f_ret 0.1",
   abs(xm01 - lib01) < 1e-12 * lib01 and abs(xs01 - 54) < 0.5,
   f"nu_mono {sp.simplify(xm_expr)} -> {xm01:.6f} (cfg515 {lib01:.6f}); simple {sp.simplify(xs_expr)} -> {xs01:.4f}")
# K5 SIS Jeans identity (the GF2 1/2)
A_ = sp.Symbol("A", positive=True)
sig2 = sp.solve(sp.Eq(sp.diff(A_ / r ** 2 * sig ** 2, r), -(A_ / r ** 2) * V ** 2 / r), sig ** 2)[0]
ratio_sis = sp.simplify(sig2.subs(V, (G * Mb * a0) ** sp.Rational(1, 4)) / sp.sqrt(G * Mb * a0))
kt("K5 SIS Jeans sigma^2/V^2 = 1/2 for any a0 (record audit: this 1/2 is NOT kappa)",
   sp.simplify(sig2 / V ** 2 - sp.Rational(1, 2)) == 0 and sp.diff(ratio_sis, a0) == 0, f"sigma^2 = {sig2}")
# K6 c_nu
def fmono(yy):
    with np.errstate(over="ignore"):
        return yy / np.expm1(np.sqrt(yy))
grid = np.logspace(-6, 6, 200001)
imax = int(np.argmax(fmono(grid)))
opt = minimize_scalar(lambda ly: -fmono(10 ** ly), bounds=(math.log10(grid[max(imax - 5, 0)]), math.log10(grid[imax + 5])),
                      method="bounded", options=dict(xatol=1e-12))
CNU = {"nu_mono": float(-opt.fun), "simple": 1.0}
YPK = float(10 ** opt.x)
fsimp_sym = y * (nu_simp(y) - 1)
lim_s = sp.limit(fsimp_sym, y, sp.oo)
mono_incr = sp.simplify(sp.diff(sp.sqrt(y ** 2 / 4 + y) - y / 2, y))
grid_ok = bool(np.all(fmono(grid) <= CNU["nu_mono"] * (1 + 1e-12))) and bool(
    np.all(np.sqrt(grid ** 2 / 4 + grid) - grid / 2 <= 1.0))
kt("K6 phantom-field bound g_ph = a0 y(nu-1) <= c_nu a0", grid_ok and lim_s == 1,
   f"nu_mono c_nu = {CNU['nu_mono']:.6f} at y = {YPK:.4f}; simple sup = {lim_s} (y -> oo; d/dy = {mono_incr} > 0)")

# K7 scaling S_lambda: x->lam x, M->lam^3 M, t->t, v->lam v, psi,Phi->lam^2, a0->lam a0 (rho fixed, c fixed)
SC = {r: lam * r, x: lam * x, rta: lam * rta, rstar: lam * rstar, Ls: lam * Ls, Lstar: lam * Lstar,
      M: lam ** 3 * M, Mb: lam ** 3 * Mb, Mta: lam ** 3 * Mta, Mcat: lam ** 3 * Mcat,
      V: lam * V, sig: lam * sig, vs: lam * vs, psi: lam ** 2 * psi, Phi: lam ** 2 * Phi,
      a0: lam * a0, gN: lam * gN, g: lam * g, u: lam * u, Qb: lam ** 2 * Qb, Pp: lam * Pp}


def degree(expr):
    sc = sp.simplify(expr.subs(SC, simultaneous=True) / expr)
    sc = sp.simplify(sp.powsimp(sp.expand_power_base(sc, force=True), force=True))
    return sc


def homog(lhs, rhs):
    dl, dr = degree(lhs), degree(rhs)
    return sp.simplify(dl - dr) == 0, dl, dr


rho_ph_pm = {nm: sp.simplify((1 / (4 * sp.pi * r ** 2)) * sp.diff((nu(G * M / (r ** 2 * a0)) - 1) * M, r))
             for nm, nu in KERNELS.items()}
EQS_CFREE = {
    "Poisson Phi": (Phi / r ** 2, 4 * sp.pi * G * rho_m),
    "deficit Poisson psi": (psi / r ** 2, 4 * sp.pi * G * (rho_ph - rho_c)),
    "drift v_s = alpha tau grad psi": (vs, alpha * tau * psi / r),
    "tau = (4 pi G rho_m)^(-1/2)": (tau, (4 * sp.pi * G * rho_m) ** sp.Rational(-1, 2)),
    "continuity rho/t ~ rho v/x": (rho_c / tau, rho_c * vs / r),
    "law g = nu(g_N/a0) g_N (mono)": (g, nu_mono(G * M / (r ** 2 * a0)) * G * M / r ** 2),
    "law g = nu(g_N/a0) g_N (simple)": (g, nu_simp(G * M / (r ** 2 * a0)) * G * M / r ** 2),
    "round-rule phantom (mono)": (rho_ph, rho_ph_pm["nu_mono"].subs(M, Mb) * rho_ph / rho_ph),
    "energy eq. sink term rho v grad Phi vs dE/dt": (rho_c * V ** 2 / tau, rho_c * vs * Phi / r),
    "energy eq. bath term (alpha/tau) rho sigma^2": (rho_c * V ** 2 / tau, alpha / tau * rho_c * sig ** 2),
    "supply M_ph(<r_*) = 5.364 N M_b": (Mb * (nu_mono(G * Mb / (rstar ** 2 * a0)) - 1), (1 - fb) / (fb * fret) * Mb),
    "catchment M_ta = (4pi/3) Delta rho r_ta^3": (Mta, sp.Rational(4, 3) * sp.pi * Dta * rho_m * rta ** 3),
    "stiffened action K W'(u) = u^2/(a0-u)": (K * Wp * lam / lam, u ** 2 / (a0 - u)),
}
# W' scales like u (acceleration / K): give it the scaling explicitly
SC[Wp] = lam * Wp
EQS_CBREAK = {
    "R2-R4 sink to DE: dE_DE/dt = Qbar (eps_DE fixed)": (eps / t, Qb),
    "R12 causality v_s/c": (vs / c, sp.Integer(1)),
    "R10' damped psi with tau_psi = c/a0": (Gam * c / a0, sp.Integer(1)),
}
k7_ok, k7 = True, {}
# phantom check: evaluate the field at the scaled point
for nm, ex in rho_ph_pm.items():
    ok = sp.simplify(ex.subs({r: lam * r, M: lam ** 3 * M, a0: lam * a0}, simultaneous=True) - ex) == 0
    k7[f"round-rule phantom density invariant ({nm})"] = bool(ok)
    k7_ok &= bool(ok)
for nm, (lh, rh) in EQS_CFREE.items():
    if nm.startswith("round-rule"):
        continue
    ok, dl, dr = homog(lh, rh)
    k7[nm] = bool(ok)
    k7_ok &= bool(ok)
brk = {}
for nm, (lh, rh) in EQS_CBREAK.items():
    ok, dl, dr = homog(lh, rh)
    brk[nm] = dict(homogeneous=bool(ok), lhs_degree=str(dl), rhs_degree=str(dr))
kt("K7 S_lambda homogeneity of every c-free galaxy-scale equation", k7_ok,
   f"{sum(k7.values())}/{len(k7)} homogeneous; c-bearing relations that BREAK S_lambda: "
   + "; ".join(f"{k_} (lhs {v_['lhs_degree']}, rhs {v_['rhs_degree']})" for k_, v_ in brk.items() if not v_['homogeneous']))
RES["K7_scaling"] = dict(cfree=k7, c_bearing=brk)

# K8 footings
a_can = KFIT * C_ * math.sqrt(G_ * OL * RHOCRIT)
a_alt = KFIT * C_ * math.sqrt(G_ * RHOCRIT)
kt("K8 footings reproduce 9.3603e-11 / 1.1312e-10 (rel 5e-4)",
   abs(a_can / FOOT["can"] - 1) < 5e-4 and abs(a_alt / FOOT["alt"] - 1) < 5e-4,
   f"can {a_can:.5e} ({a_can / FOOT['can'] - 1:+.1e}), alt {a_alt:.5e} ({a_alt / FOOT['alt'] - 1:+.1e})")
# K9 dimension null spaces (theorem T1)
cols = {"a0": DIM[a0], "G": DIM[G], "rho": DIM[rho_DE], "c": DIM[c], "M_b": DIM[Mb], "L*": DIM[Ls]}


def nullspace(names):
    Mx = sp.Matrix([[sp.Rational(int(round(2 * cols[n_][i])), 2) for n_ in names] for i in range(3)])
    return Mx.rank(), [list(v_.T / v_[0]) if v_[0] != 0 else list(v_.T) for v_ in Mx.nullspace()]


ns = {k_: nullspace(v_) for k_, v_ in {"a0,G,rho": ["a0", "G", "rho"], "a0,G,rho,c": ["a0", "G", "rho", "c"],
                                       "a0,G,rho,M_b": ["a0", "G", "rho", "M_b"], "a0,G,rho,L*": ["a0", "G", "rho", "L*"]}.items()}
kt("K9 T1: {a0,G,rho} no dimensionless group; with c one group a0 c^-1 G^-1/2 rho^-1/2",
   ns["a0,G,rho"][1] == [] and len(ns["a0,G,rho,c"][1]) == 1
   and ns["a0,G,rho,c"][1][0] == [1, sp.Rational(-1, 2), sp.Rational(-1, 2), -1],
   "; ".join(f"[{k_}] rank {v_[0]}, null {[[str(e_) for e_ in z_] for z_ in v_[1]]}" for k_, v_ in ns.items()))
RES["T1_nullspaces"] = {k_: dict(rank=int(v_[0]), null=[[str(e_) for e_ in z_] for z_ in v_[1]]) for k_, v_ in ns.items()}

# K11 classifier positive controls
ctl = {"P1 a0 = c sqrt(G rho_DE)/2": classify(a0, c * sp.sqrt(G * rho_DE) / 2)["cls"],
       "P2 a0 = G rho^(2/3) M_b^(1/3)": classify(a0, G * rho_m ** sp.Rational(2, 3) * Mb ** sp.Rational(1, 3))["cls"],
       "P3 a0 M_b = a0 M_b": classify(a0 * Mb, a0 * Mb)["cls"]}
kt("K11 classifier controls (SELECTED / MASS-DEPENDENT / IDENTITY)",
   ctl["P1 a0 = c sqrt(G rho_DE)/2"] == "SELECTED" and ctl["P2 a0 = G rho^(2/3) M_b^(1/3)"] == "MASS-DEPENDENT"
   and ctl["P3 a0 M_b = a0 M_b"] == "IDENTITY", f"{ctl}")

# ------------------------------------------------------------------------------------------------ numeric helpers
_rho_ph_sym = {nm: sp.lambdify((r, M, a0), rho_ph_pm[nm].subs(G, G_), "numpy") for nm in KERNELS}


def _rho_ph_mono(rr, Mm, aa):
    """stable closed form of the nu_mono point-mass phantom density: M s e^-s/(4 pi r^3 (1 - e^-s)^2), s = sqrt(y)."""
    ss = np.sqrt(G_ * Mm / (rr ** 2 * aa))
    return Mm * ss * np.exp(-ss) / (4 * math.pi * rr ** 3 * (-np.expm1(-ss)) ** 2)


def _rho_ph_simp(rr, Mm, aa):
    """closed form of the simple-kernel point-mass phantom density: M/(4 pi r^3 y sqrt(1/4 + 1/y))."""
    yy = G_ * Mm / (rr ** 2 * aa)
    return Mm / (4 * math.pi * rr ** 3 * yy * np.sqrt(0.25 + 1 / yy))


rho_ph_num = {"nu_mono": _rho_ph_mono, "simple": _rho_ph_simp}


def log_rho_ph(rr, Mm, aa, nm):
    """log of the point-mass phantom density, evaluated in log space (no underflow deep in the Newtonian regime)."""
    yy = G_ * Mm / (rr ** 2 * aa)
    if nm == "nu_mono":
        ss = math.sqrt(yy)
        return math.log(Mm * ss / (4 * math.pi * rr ** 3)) - ss - 2 * math.log(-math.expm1(-ss))
    return math.log(Mm / (4 * math.pi * rr ** 3)) - math.log(yy * math.sqrt(0.25 + 1 / yy))
_chk = [(nm, rr_, aa_) for nm in KERNELS for rr_ in (1e19, 1e21, 3e22) for aa_ in (1e-11, 1e-10, 1e-9)]
_dev = max(abs(rho_ph_num[nm](rr_, 1e41, aa_) / _rho_ph_sym[nm](rr_, 1e41, aa_) - 1) for nm, rr_, aa_ in _chk)
kt("K6b closed-form phantom densities equal the sympy derivative (rel 1e-9)", _dev < 1e-9, f"max rel dev {_dev:.1e}")


def Mph_pm(rr, Mm, aa, nm):
    yy = G_ * Mm / (rr ** 2 * aa)
    if nm == "nu_mono":
        return Mm / np.expm1(np.sqrt(yy))
    return Mm * (np.sqrt(0.25 + 1 / yy) - 0.5)


def rta_of(Mb_, f_):
    Mta_ = Mb_ / (FB * f_)
    return (3 * Mta_ / (4 * math.pi * DTA * RHOM)) ** (1 / 3), Mta_


def a0_implied_R5(Mb_kg, variant, nm, th=0.0):
    f_ = fret_census(Mb_kg / MSUN)[0]
    rt, _ = rta_of(Mb_kg, f_)
    rho_edge = {"a": (1 - FB) * DTA * RHOM, "b": (1 - FB) * DTA * RHOM / 3, "c": OL * RHOCRIT}[variant] + th * RHOM
    fn = lambda la: log_rho_ph(rt, Mb_kg, 10 ** la, nm) - math.log(rho_edge)
    return 10 ** brentq(fn, -20, -2, xtol=1e-13), f_, rt


def xstar(f_, nm):
    if nm == "nu_mono":
        return 1.0 / math.log1p(f_ * FB / (1 - FB))
    return math.sqrt((R_COLD / f_ + 0.5) ** 2 - 0.25)


def rstar_threshold(Mb_kg, aa, nm, th):
    """point-mass edge with settled profile rho_c = rho_ph - th rho_m (where positive): M_set(<r_*) = M_cat."""
    f_ = fret_census(Mb_kg / MSUN)[0]
    Mcat_ = R_COLD * Mb_kg / f_
    rM_ = math.sqrt(G_ * Mb_kg / aa)
    if th == 0.0:
        return xstar(f_, nm) * rM_
    rr = np.geomspace(1e-3 * rM_, 1e4 * rM_, 400001)
    dens = np.maximum(rho_ph_num[nm](rr, Mb_kg, aa) - th * RHOM, 0.0)
    Mset = np.concatenate([[Mph_pm(rr[0], Mb_kg, aa, nm)],
                           Mph_pm(rr[0], Mb_kg, aa, nm) + np.cumsum(0.5 * (dens[1:] * rr[1:] ** 2 + dens[:-1] * rr[:-1] ** 2)
                                                                    * np.diff(rr)) * 4 * math.pi])
    i = int(np.searchsorted(Mset, Mcat_))
    if i >= len(rr):
        return float("inf")
    return float(np.interp(Mcat_, Mset[i - 1:i + 1], rr[i - 1:i + 1]))


# =====================================================================================================================
log("\nRELATIONS (FROZEN_CRITERIA section 2)")
d541 = json.load(open(os.path.join(HERE, "..", "CFG541_cold_energy_equations_precise", "cfg541_results.json")))
OMC = OM * (1 - FB)

# ---- (a) the dark-energy sink
log("\n(a) the dark-energy sink: Q = rho_c alpha tau 1_B 1_C grad psi . grad Phi >= 0 (CFG542 Pb), eps_DE = rho_DE c^2")
record("R1", "exact Lambda: d eps_DE/dt + 3H(1+w) eps_DE = Qbar with w = -1 and d eps_DE/dt = 0 => Qbar = 0", "CFG541 S(ii)",
       None, classify(eps / t + 3 * Hh * (1 + w) * eps, Qb), dim_ok(eps / t + 3 * Hh * (1 + w) * eps, Qb),
       dict(note="kappa-independent constraint: incompatible with E_sink > 0 (CFG541) for every kappa; dark energy must be "
                 "dynamical (record)"))
SINK = -1.0 if MUT else 1.0
B = {}
for foot in ("can", "alt"):
    dWm = d541["one_d"][foot]["cluster"]["dW_per_mass"]
    B[foot] = SINK * (OMC / OL) * dWm / C_ ** 2
Bn = {foot: (OMC / OL) * d541["one_d"][foot]["cluster"]["dW_per_mass"] / C_ ** 2 for foot in ("can", "alt")}
a0t = sp.Function("a0")
qfun = sp.Function("q_s")
sol_ode = sp.dsolve(sp.Eq(sp.diff(a0t(t), t), a0t(t) * qfun(t) / 2), a0t(t))
r2_cls = dict(cls="IDENTITY", why=f"a0(t) = {sol_ode.rhs}: the integration constant (hence kappa) is free")
dln = {foot: B[foot] / 2 for foot in B}
record("R2", "dynamical DE absorbing Q, a0 = kappa sqrt(G eps_DE): d ln a0/dt = Qbar/(2 eps_DE)", "CFG541 S(ii) + S1 tracking",
       None, r2_cls, dim_ok(1 / t, Qb / (2 * eps)),
       dict(B_budget={k_: float(v_) for k_, v_ in B.items()}, cum_dln_a0_max={k_: float(v_) for k_, v_ in dln.items()},
            cum_dlog10_a0_max={k_: float(v_ / math.log(10)) for k_, v_ in dln.items()},
            note="constrains the a0 drift only (flat a0 to ~1e-6), for any kappa"))
for foot in ("can", "alt"):
    log(f"     {foot}: budget B = (Omega_c/Omega_Lambda)(Delta W/M)_cluster/c^2 = {B[foot]:+.4e}; cumulative "
        f"Delta ln a0 <= {dln[foot]:+.3e} ({dln[foot] / math.log(10):+.3e} dex)")
# R3 / R4: equalities under added hypotheses, kappa scaling B ∝ kappa^(1/2) at fixed M_b (xi held fixed: flagged)
Bk = sp.Symbol("B_fit", real=True)
kreq = {}
for lab, target in (("R3", 1.0), ("R4", 0.01)):
    kreq[lab] = {}
    for foot in ("can", "alt"):
        eq_ = sp.Eq(sp.Float(B[foot]) * sp.sqrt(kap / KFIT), target)
        sols = [float(z_) for z_ in sp.solve(eq_, kap) if z_.is_real and z_ > 0]
        kreq[lab][foot] = sols[0] if sols else None
# symbolic forms (per system class): eps_DE = rho_c,set xi sqrt(G M_b a0) * target
sym_R3 = classify(eps, rho_c * xi * sp.sqrt(G * Mb * a0), hyp="H3")
sym_R3["a0_solution_with_eps=rho_DE c^2"] = str(sp.solve(sp.Eq(rho_DE * c ** 2, rho_c * xi * sp.sqrt(G * Mb * a0)), a0))
for lab, hyp, tgt, txt in (("R3", "H3", 1.0, "DE is the accumulated settling energy: eps_DE = int Qbar dt"),
                           ("R4", "H4", 0.01, "the sink drives a DE evolution of size X = 0.01: int Qbar dt = X eps_DE")):
    cls_ = classify(X * eps if lab == "R4" else eps, rho_c * xi * sp.sqrt(G * Mb * a0), hyp=hyp)
    ex = {f"kappa_required_{f_}": kreq[lab][f_] for f_ in ("can", "alt")}
    ok_num = all(v_ is not None and KAPPA_RANGE[0] <= v_ <= KAPPA_RANGE[1] for v_ in kreq[lab].values())
    ex["numeric_class"] = "within [0.01, 100]" if ok_num else "EXCLUDED (kappa_req non-positive/none or outside [0.01, 100])"
    record(lab, txt, "added hypothesis", hyp, cls_, dim_ok(eps, rho_c * xi * sp.sqrt(G * Mb * a0)), ex)
    log(f"     kappa required (B ∝ kappa^1/2 at fixed M_b): can {kreq[lab]['can']}, alt {kreq[lab]['alt']} -> "
        f"{ex['numeric_class']}")

# ---- (b) gate edge at the catchment edge
log("\n(b) gate edge d = 0 at the catchment edge r_ta [added H5]; deep regime rho_ph = sqrt(M_b a0/G)/(4 pi r^2)")
deep_rho = sp.sqrt(Mb * a0 / G) / (4 * sp.pi * rta ** 2)
rta_expr = (3 * Mb / (fb * fret) / (4 * sp.pi * Dta * rho_m)) ** sp.Rational(1, 3)
r5_sym = {}
for var, rho_edge_expr in (("a", (1 - fb) * Dta * rho_m), ("b", (1 - fb) * Dta * rho_m / 3), ("c", rho_DE)):
    lhs_ = deep_rho.subs(rta, rta_expr)
    r5_sym[var] = classify(lhs_, rho_edge_expr, hyp="H5")
    record(f"R5{var}", f"rho_ph(r_ta) = rho_edge [{ {'a': '(1-f_b) Delta_ta rho_m', 'b': '(1-f_b) Delta_ta rho_m/3', 'c': 'rho_DE'}[var] }]",
           "added hypothesis", "H5", r5_sym[var], dim_ok(deep_rho, rho_edge_expr))
MBS = [1e8, 1e9, 1e10, 1e11, 1e12]
r5num = {}
for nm in KERNELS:
    r5num[nm] = {}
    for var in ("a", "b", "c"):
        rows = []
        for mb in MBS:
            aa, f_, rt = a0_implied_R5(mb * MSUN, var, nm)
            rows.append(dict(M_b=mb, f_ret=f_, r_ta_kpc=rt / KPC, a0=aa, kappa_can=kappa_of(aa, "can"),
                             kappa_alt=kappa_of(aa, "alt"), rM_over_rta=math.sqrt(G_ * mb * MSUN / aa) / rt))
        sl = [math.log(rows[i + 1]["a0"] / rows[i]["a0"]) / math.log(MBS[i + 1] / MBS[i]) for i in range(len(MBS) - 1)]
        r5num[nm][var] = dict(rows=rows, local_slopes=sl)
        log(f"     {nm:8s} R5{var}: implied a0 at M_b 1e8..1e12 = "
            + ", ".join(f"{z_['a0']:.2e}" for z_ in rows)
            + f"; local slopes d ln a0/d ln M_b = {', '.join(f'{v_:.3f}' for v_ in sl)}; kappa_can min..max "
            f"{min(z_['kappa_can'] for z_ in rows):.3g}..{max(z_['kappa_can'] for z_ in rows):.3g}, kappa_alt min..max "
            f"{min(z_['kappa_alt'] for z_ in rows):.3g}..{max(z_['kappa_alt'] for z_ in rows):.3g}")
REL["R5a"]["numeric"] = r5num
# report-only: galaxy mass at which H5(a) would return the fitted a0
mstar = {}
for nm in KERNELS:
    row = r5num[nm]["a"]["rows"][2]
    mstar[nm] = {foot: row["M_b"] * (FOOT[foot] / row["a0"]) ** 3 for foot in FOOT}
log(f"     report-only: M_b at which H5(a) returns each footing's a0 (slope 1/3 from 1e10): {mstar}")
REL["R5a"]["Mb_where_fitted_a0"] = mstar

# ---- (c) supply
log("\n(c) supply: M_ph(<r_*) = 5.364 N M_b, N = 1/f_ret (CFG804); point mass")
supply_x = Mb * (nu_mono(1 / x ** 2) - 1) - (1 - fb) / (fb * fret) * Mb   # r_* = x r_M: a0 cancels
cls_R6 = dict(cls="IDENTITY", why="in r_* = x r_M the relation is a0-free: it fixes x_* = r_*/r_M "
                                  "(kappa-independent constraint on the edge)") if a0 not in supply_x.free_symbols else classify(supply_x, 0)
r6num = {nm: {f_: xstar(f_, nm) for f_ in (0.07, 0.10, 0.18)} for nm in KERNELS}
rs_mw = {foot: {nm: rstar_threshold(6e10 * MSUN, FOOT[foot], nm, 0.0) / KPC for nm in KERNELS} for foot in FOOT}
record("R6", "M_ph(<r_*) = 5.364 N M_b", "record S3 / CFG804", None, cls_R6,
       dim_ok(Mb * (nu_mono(G * Mb / (rstar ** 2 * a0)) - 1), (1 - fb) / (fb * fret) * Mb),
       dict(x_star=r6num, r_star_MW_6e10_kpc=rs_mw,
            note="mass-independent in r_M units iff f_ret is constant (census 0.10 for galaxies); physical r_* ∝ kappa^-1/2"))
log(f"     x_* = r_*/r_M: {r6num}; MW-like 6e10 r_* (kpc): {rs_mw}")
cls_R7 = classify(sp.Symbol("x_s", positive=True) * sp.sqrt(G * Mb / a0), rta_expr, hyp="H7")
DIM[sp.Symbol("x_s", positive=True)] = np.zeros(3)
r7num = {}
for nm in KERNELS:
    rows = []
    for mb in MBS:
        f_ = fret_census(mb)[0]
        rt, _ = rta_of(mb * MSUN, f_)
        aa = G_ * mb * MSUN * xstar(f_, nm) ** 2 / rt ** 2
        rows.append(dict(M_b=mb, f_ret=f_, a0=aa, kappa_can=kappa_of(aa, "can"), kappa_alt=kappa_of(aa, "alt")))
    sl = [math.log(rows[i + 1]["a0"] / rows[i]["a0"]) / math.log(MBS[i + 1] / MBS[i]) for i in range(len(MBS) - 1)]
    r7num[nm] = dict(rows=rows, local_slopes=sl)
record("R7", "supply exhausted exactly at turnaround: r_* = r_ta", "added hypothesis", "H7", cls_R7,
       dim_ok(sp.sqrt(G * Mb / a0), rta_expr), dict(numeric=r7num))
for nm in KERNELS:
    log(f"     {nm:8s} R7: implied a0 at M_b 1e8..1e12 = " + ", ".join(f"{z_['a0']:.2e}" for z_ in r7num[nm]["rows"])
        + f"; slopes {', '.join(f'{v_:.3f}' for v_ in r7num[nm]['local_slopes'])}")

# ---- (d) stationarity / stability of the gated drift and the remaining structures
log("\n(d) gated drift, stability, bath, causality, clump mass, stiffened action")
dsym = rho_ph - rho_c
gate = sp.Heaviside(dsym - theta * rho_m, 0)        # 1[d > theta rho_m]; theta = 0 is the record's gate
grad_psi = sp.Symbol("gradpsi", real=True)
station = rho_c * alpha * tau * gate * grad_psi
st_at = sp.simplify(station.subs(rho_c, rho_ph - theta * rho_m))
rho_ph_a0 = sp.Function("rho_ph_law")(r, a0)
cls_R8 = dict(cls="IDENTITY", why=f"residual at rho_c = rho_ph(a0) - theta rho_m is {st_at} for every a0")
record("R8", "stationarity of v_s = -alpha tau 1[d > theta rho_m] grad psi (theta = 0: CFG639)", "CFG639", None, cls_R8,
       dim_ok(vs, alpha * tau * psi / r))
dpsi_lin = sp.Symbol("delta_rho", real=True)
Gam_expr = sp.simplify(4 * sp.pi * G * alpha * tau * rho_c).subs(tau, (4 * sp.pi * G * rho_m) ** sp.Rational(-1, 2))
record("R9", f"linear relaxation rate Gamma = {sp.simplify(Gam_expr)}", "CFG638 K6", None,
       dict(cls="IDENTITY", why=f"d Gamma/d a0 = {sp.diff(Gam_expr, a0)}"), dim_ok(Gam, 4 * sp.pi * G * alpha * tau * rho_c))
cond_beta = sp.simplify((Gam_expr * beta * (4 * sp.pi * G * rho_m) ** sp.Rational(-1, 2)).subs(rho_c, q * rho_m))
cond_ca0 = sp.simplify((Gam_expr * c / (kap * c * sp.sqrt(G * rho_DE))).subs(rho_c, q * rho_m))
kmin_gal = float((cond_ca0 * kap).subs({alpha: 1, q: 0.5, rho_m: 1e5 * RHOM, rho_DE: OL * RHOCRIT, G: G_}))
record("R10", f"damped-psi stability Gamma tau_psi < 1, tau_psi = beta tau: {cond_beta} < 1", "CFG541 §6 / CFG542 K9", None,
       dict(cls="IDENTITY", why="a0-free (alpha beta q < 1; the record's alpha bound)"), dim_ok(Gam * taupsi, sp.Integer(1)),
       dict(variant_tau_psi_c_over_a0=f"{cond_ca0} < 1  => kappa > {sp.simplify(cond_ca0 * kap)}",
            variant_kappa_min_at_Delta_1e5_alpha1_q05=kmin_gal,
            variant_class="JOINT/BOUND; violated inside galaxies for any O(1) kappa (that is why CFG541 rejected it)"))
log(f"     R10 variant (rejected by CFG541) tau_psi = c/a0: stability needs kappa > {kmin_gal:.1f} at Delta_loc = 1e5, alpha 1, q 0.5")
record("R11", "bath stationarity tr Pi = 3 rho sigma_J^2, deep 1/r^2 halo: sigma^2/V^2 = 1/2", "CFG638 energy eq.; GF2 audit",
       None, dict(cls="IDENTITY", why="sigma^2/V^2 = 1/2 for every a0 (K5); this 1/2 is the SIS ratio, not kappa"),
       dim_ok(3 * rho_c * sig ** 2, rho_c * V ** 2))

# R12 drift causality
log("     R12: |v_s| <= alpha tau |grad psi| <= alpha c_nu a0/sqrt(4 pi G rho_m,loc)  (one-sided deficit, round rule)")
vbound = alpha * sp.Symbol("c_nu", positive=True) * a0 / sp.sqrt(4 * sp.pi * G * rho_m)
DIM[sp.Symbol("c_nu", positive=True)] = np.zeros(3)
vb_kappa = sp.simplify((vbound / c).subs(a0, kap * c * sp.sqrt(G * rho_DE)))
log(f"         |v_s|/c <= {vb_kappa}  (c and galaxy mass cancel)")
STATES = {"(1-f_b)Delta_ta (CFG541 reservoir)": (1 - FB) * DTA, "cosmic mean (1)": 1.0, "f_b (baryons only)": FB}
r12 = {}
tighter = []
for foot in FOOT:
    r12[foot] = {}
    for nm in KERNELS:
        r12[foot][nm] = {}
        for sn, Dl in STATES.items():
            rho_loc = Dl * RHOM
            vb1 = CNU[nm] * KFIT * math.sqrt(RHOFOOT[foot] / (4 * math.pi * rho_loc))      # alpha = 1, fitted kappa
            amax = 1.0 / vb1
            kH12 = math.sqrt(4 * math.pi * rho_loc / RHOFOOT[foot]) / CNU[nm]            # equality v = c at alpha = 1
            r12[foot][nm][sn] = dict(Delta_loc=Dl, vmax_over_c_alpha1=vb1, alpha_max=amax, alpha_max_1pct_margin=0.01 * amax,
                                     kappa_H12_alpha1=kH12)
            if amax < ALPHA_MAX_RECORD:
                tighter.append((foot, nm, sn, amax))
        rc = (CNU[nm] * KFIT) ** 2 * RHOFOOT[foot] / (4 * math.pi)
        r12[foot][nm]["rho_caus_over_rho_m_alpha1"] = rc / RHOM
r12_cls = dict(cls="JOINT/BOUND", why="inequality in alpha*kappa*c_nu*sqrt(rho_foot/(4 pi rho_loc)); state-dependent")
h12 = classify(c, sp.Symbol("alpha_", positive=True) * sp.Symbol("c_nu", positive=True) * a0 / sp.sqrt(4 * sp.pi * G * rho_m), hyp="H12")
record("R12", "|v_s| <= c on B∩C (drift causality)", "record causality (CFG541 C1, CFG542 K9)", None, r12_cls,
       dim_ok(vbound, c), dict(bound_over_c=str(vb_kappa), c_nu=CNU, table=r12, H12_equality_class=h12["cls"],
                               H12_why=h12.get("why", ""), alpha_bounds_tighter_than_record=tighter))
for foot in FOOT:
    for nm in KERNELS:
        log(f"         {foot} {nm:8s}: " + "; ".join(
            f"{sn}: v/c<= {v_['vmax_over_c_alpha1']:.4f} (alpha 1), alpha_max {v_['alpha_max']:.2f}, kappa_H12 {v_['kappa_H12_alpha1']:.2f}"
            for sn, v_ in r12[foot][nm].items() if isinstance(v_, dict))
            + f"; rho_caus/rho_m {r12[foot][nm]['rho_caus_over_rho_m_alpha1']:.4f}")
log(f"         alpha bounds tighter than the record's 1.186: {tighter if tighter else 'none'}; H12 equality: [{h12['cls']}]")

# K12: the bound vs CFG541 C1
k12rows, k12_ok = {}, True
rho_c0 = (1 - FB) * DTA * RHOM
for foot in FOOT:
    for cell in ("MW", "group", "cluster"):
        meas = d541["one_d"][foot][cell]["C1"]["max_vs_over_c"]
        bnd = CNU["nu_mono"] * FOOT[foot] / (C_ * math.sqrt(4 * math.pi * G_ * rho_c0))
        ok = meas <= bnd * (1 + 1e-6)
        if cell == "cluster":
            ok = ok and 0.90 <= meas / bnd <= 1.0 + 1e-6
        k12rows[f"{foot}_{cell}"] = dict(measured=meas, bound=bnd, ratio=meas / bnd, ok=bool(ok))
        k12_ok &= bool(ok)
kt("K12 R12 bound >= CFG541 C1 in all 6 cells; point-mass clusters saturate (ratio in [0.90, 1.00])", k12_ok,
   "; ".join(f"{k_} {v_['measured']:.4e}/{v_['bound']:.4e} = {v_['ratio']:.4f}" for k_, v_ in k12rows.items()))
RES["K12_rows"] = k12rows

# R13 clump mass (by construction in CFG877)
cl13 = classify(Mcl, ff * 81 * sig ** 4 / (4 * G * a0))
record("R13", "M_cl = f 81 sigma^4/(4 G a0) (CFG878)", "record v3 addendum", None,
       dict(cls="IDENTITY", why="CFG877 computes M_cl from sigma and the footing a0, so substituting it back returns a0 for "
                                "every a0 (by construction); as an independent relation it is JOINT (sigma external, M_cl "
                                "measured and dwarf-dependent, CFG880): " + cl13["cls"]),
       dim_ok(Mcl, ff * 81 * sig ** 4 / (4 * G * a0)))
# R14 stiffened action: vacuum offset and a0 as parameter
gPhi, W0 = sp.symbols("gradPhi W0", real=True)
gP = sp.Symbol("gradP", real=True)
Wfun = sp.Function("W_rem")
Lag = -(gPhi - K * Pp) ** 2 / (2 * K) - rho_b * Phi - Wfun(K * Pp) - W0 - (K * Lstar ** 2 / 4) * gP ** 2
el = [sp.diff(Lag, v_) for v_ in (Pp, gPhi, Phi, gP)]
r14ok = all(W0 not in e_.free_symbols for e_ in el)
record("R14", "stiffened action: Euler-Lagrange equations unchanged by W_rem -> W_rem + W0; a0 a parameter of W_rem'",
       "record S2 (CFG807 V0)", None,
       dict(cls="IDENTITY", why=f"W0 absent from all EL terms: {r14ok}; the rest state is the law for every a0"),
       dim_ok(K * Wp, u ** 2 / (a0 - u)))
kt("K10 dimensions of every relation R1-R14", all(v_["dims_ok"] for v_ in REL.values()),
   f"{sum(v_['dims_ok'] for v_ in REL.values())}/{len(REL)} consistent")

# ------------------------------------------------------------------------------------------------ MUTATE teeth
teeth = {}
if MUT:
    log("\nMUTATE TEETH")
    # M1 sink sign
    flip = all(math.copysign(1, dln[f_]) != math.copysign(1, Bn[f_] / 2) for f_ in FOOT)
    noR3 = all(kreq["R3"][f_] is None for f_ in FOOT)
    teeth["M1a R2 Delta ln a0 changes sign"] = flip
    teeth["M1b R3 has no positive real kappa"] = noR3
    # M2 gate threshold
    mref = 10 ** 10.5 * MSUN
    a_n = a0_implied_R5(mref, "a", "nu_mono", 0.0)[0]
    a_m = a0_implied_R5(mref, "a", "nu_mono", 1.0)[0]
    teeth["M2a R5(a) implied a0 moves |d ln a0| >= 0.01"] = abs(math.log(a_m / a_n)) >= 0.01
    rs_n = rstar_threshold(6e10 * MSUN, FOOT["can"], "nu_mono", 0.0)
    rs_m = rstar_threshold(6e10 * MSUN, FOOT["can"], "nu_mono", 1.0)
    teeth["M2b R6/R8 MW-like edge moves |d ln r_*| >= 1e-3"] = abs(math.log(rs_m / rs_n)) >= 1e-3
    RES["mutate_numbers"] = dict(dln_normal=Bn, dln_mutate=dln, R3_kappa=kreq["R3"], R5a_a0_normal=a_n, R5a_a0_theta1=a_m,
                                 rstar_normal_kpc=rs_n / KPC, rstar_theta1_kpc=rs_m / KPC)
    for k_, v_ in teeth.items():
        log(f"  [{'BITES' if v_ else 'DOES NOT BITE'}] {k_}")
    log(f"    numbers: R5(a) a0 {a_n:.4e} -> {a_m:.4e}; MW edge {rs_n / KPC:.2f} -> {rs_m / KPC:.2f} kpc; "
        f"R3 kappa {kreq['R3']}")

# ------------------------------------------------------------------------------------------------ verdict (frozen)
sel = [k_ for k_, v_ in REL.items() if v_["cls"] == "SELECTED"]
sel_h = [k_ for k_, v_ in REL.items() if v_["cls"].startswith("SELECTED UNDER")]
constrains = []
if tighter:
    constrains.append(f"alpha (R12, tighter than 1.186 in {tighter})")
if sel:
    overall = "kappa SELECTED"
elif constrains:
    overall = "CONSTRAINS SOMETHING ELSE"
else:
    overall = "NOT SELECTED"
log("\nCLASSES")
for k_, v_ in REL.items():
    log(f"  {k_:4s} {v_['cls']:22s} {('[' + v_['added_hypothesis'] + '] ') if v_['added_hypothesis'] else ''}{v_['statement']}")
log(f"\nOVERALL (frozen rule): {overall}")
log(f"  SELECTED: {sel or 'none'}; SELECTED UNDER HYPOTHESIS: {sel_h or 'none'}; constrains instead: {constrains or 'no listed constant'}")
log("  non-constant consequences: dark energy must be dynamical (R1); a0 drift <= ~1e-6 (R2); edge r_*/r_M fixed by f_ret (R6);")
log("  drift causality bounds alpha*kappa only jointly and state-dependently (R12); c-free balances are mass-dependent (T1/K7).")
RES.update(dict(relations=REL, ktests=KT, overall=overall, selected=sel, selected_under_hypothesis=sel_h,
                constrains_instead=constrains, c_nu=CNU, y_peak_mono=YPK, Delta_ta=DTA, teeth=teeth,
                settings=dict(h=h, Omega_m=OM, Omega_Lambda=OL, f_b=FB, kappa_fit=KFIT, footings=FOOT, rho_crit=RHOCRIT)))
kfail = [k_ for k_, v_ in KT.items() if not v_["ok"]]
log(f"\nK-tests: {len(KT) - len(kfail)}/{len(KT)} pass" + (f"; FAIL: {kfail}" if kfail else ""))
log("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.")


def _json(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return str(o)


with open(os.path.join(HERE, f"cfg893_results{TAG}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=_json)
with open(os.path.join(HERE, f"cfg893{TAG}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
if MUT:
    sys.exit(1 if teeth and all(teeth.values()) else 3)
sys.exit(0 if not kfail else 1)
