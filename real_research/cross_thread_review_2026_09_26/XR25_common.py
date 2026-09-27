#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR25_common -- shared machinery for the XR25 strong-field lanes (binary pulsars, inspirals, compact objects).

Nothing here runs a lane.  It supplies:
  * Lane: the review-folder conventions (the script writes its own .out through a tee, a results JSON, PASS/FAIL checks,
    rc = 0 only when no load-bearing check fails; MUTATE=1 writes the _MUTATE versions).
  * block(): the chain's root action expanded to second order about Minkowski in unitary gauge (tau = t), one plane wave
    along z, re-derived here (the construction of FP14's unitary_block, extended): the BPS khronon with a beta term (for the
    literature control), the leaf-averaged c_2 term or its c_2 -> oo multiplier -2 mu (K - <K>), and either FP7/FP14's
    AQUAL-type MOND sector (perfect-square chassis on chi = sigma phi, -2 C_phi |D phi|^2, 2 lambda (n.d phi)^2) or FP2's
    C-H sector (2 |DU - a|^2 + 2 C_eff |DU|^2).
  * ppn(): FP2's moving-source pipeline (a source moving at v through the khronon frame, boosted to rest), which reads
    gamma, alpha_1, alpha_2, alpha_3 off the rest-frame h_00 and h_0j.
  * nu_mono (FP2/L340's construction), the P2 kernel's AQUAL coefficients, FP2's real-space filter factors F1, F2, F4.
  * a TOV solver (piecewise polytropes) for the compact-object lanes.
Units in the symbolic block: c = 1, per 1/(16 pi G); the matter source enters as Pf * EL = source, Pf = 1/(16 pi G).
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")

# ------------------------------------------------------------------------------------------------ constants (SI)
cc, Gn = 299792458.0, 6.67430e-11
MSUN, PC_M, AU_M, KPC_M = 1.98847e30, 3.0856775814913673e16, 1.495978707e11, 3.0856775814913673e19
GM_SUN = 1.32712440018e20
HBARC_GEV_M = 1.973269804e-16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
try:
    _n0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))["numbers"]
    A0 = {"canonical": _n0["a0_canonical"], "alt": _n0["a0_rho_total"]}
except Exception:
    pass

# ------------------------------------------------------------------------------------------------ the bounds, with sources
BOUNDS = {
    "alpha1_LLR": dict(value=-7e-5, sigma=9e-5, abs95=2.5e-4,
                       src="lunar laser ranging: alpha_1 = (-7 +- 9) x 1e-5 (1 sigma; Mueller, Williams & Turyshev 2008, "
                           "Astrophys. Space Sci. Libr. 349, 457); |alpha_1| < 2.5e-4 at 2 sigma"),
    "alpha2_LLR": dict(value=1.8e-5, sigma=2.5e-5, abs95=6.8e-5,
                       src="lunar laser ranging: alpha_2 = (1.8 +- 2.5) x 1e-5 (1 sigma; same)"),
    "alpha1_psr": dict(abs95=3.7e-5,
                       src="PSR J1738+0333: alpha_1-hat = -0.4 (+3.7, -3.1) x 1e-5 at 95% CL (Shao & Wex 2012, CQG 29, 215018)"),
    "alpha2_sun": dict(abs95=2.4e-7, src="solar spin-orbit alignment: |alpha_2| < 2.4e-7 (Nordtvedt 1987, ApJ 320, 871)"),
    "alpha2_psr": dict(abs95=1.6e-9,
                       src="isolated millisecond pulsars B1937+21 and J1744-1134: |alpha_2-hat| < 1.6e-9 at 95% CL "
                           "(Shao, Caballero, Kramer, Wex, Champion & Jessner 2013, CQG 30, 165019)"),
}

# ------------------------------------------------------------------------------------------------ the chain's committed inputs
AC_WINDOW = {"floor_XC1_c2inf": 8.2e-16, "floor_torsion_c2inf": 1.6e-40, "cap": 3.2e-9}   # FP14 A3 (c_2 -> oo) and FP2 B4
XI_FLOOR_AQ = {"canonical": 0.0243, "alt": 0.0268}                                         # FP7 A4 (pc)
XI_CEIL_PC = 100.0
C2_FLOOR = 7.2888e-3                                                                      # FP2 C4
V_TRACK = 3 * 600e3
try:
    _f7 = json.load(open(os.path.join(CHAIN, "FP7_aqual_type_repair_results.json")))["numbers"]
    XI_FLOOR_AQ = {f: _f7["A4"]["AQUAL_floors"][f]["floor"] for f in ("canonical", "alt")}
except Exception:
    pass
try:
    _f14 = json.load(open(os.path.join(CHAIN, "FP14_zero_knob_core_results.json")))["numbers"]["A3"]
    AC_WINDOW["floor_XC1_c2inf"] = _f14["oo|XC1 gate"]
    AC_WINDOW["floor_torsion_c2inf"] = _f14["oo|torsion balance"]
except Exception:
    pass


# ================================================================================================ the Lane helper
class _Tee:
    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()

    def close(self):
        self._f.close()


class Lane:
    def __init__(self, name, lane_tag):
        self.here = HERE
        self.mutate = os.environ.get("MUTATE", "0") == "1"
        self.name = name
        self.txt = os.path.join(HERE, name + ("_MUTATE.out" if self.mutate else ".out"))
        self.jsn = os.path.join(HERE, name + ("_results_MUTATE.json" if self.mutate else "_results.json"))
        self.t0 = time.time()
        self.tee = _Tee(self.txt)
        sys.stdout = self.tee
        self.out = {"lane": lane_tag, "mutate": self.mutate, "checks": {}, "numbers": {}, "ledger": []}
        self.ch = []

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def check(self, name, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.ch.append((name, ok, load_bearing))
        self.out["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def finish(self):
        n_fail = sum(1 for _, ok, lb in self.ch if lb and not ok)
        self.out["verdict_counts"] = dict(n_checks=len(self.ch), n_fail_load_bearing=n_fail,
                                          n_fail_reported=sum(1 for _, ok, lb in self.ch if (not lb) and (not ok)))
        json.dump(self.out, open(self.jsn, "w"), indent=1, default=_js_default)
        rc = 0 if n_fail == 0 else 1
        self.P(f"\n  {sum(1 for _, ok, _l in self.ch if ok)}/{len(self.ch)} checks pass; load-bearing failures: {n_fail}; wrote "
               f"{os.path.basename(self.jsn)}  ({time.time() - self.t0:.0f} s)")
        self.P(f"rc = {rc}")
        self.tee.flush()
        sys.stdout = sys.__stdout__
        self.tee.close()
        sys.exit(rc)


def _js_default(o):
    if hasattr(o, "tolist"):
        return o.tolist()
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    return str(o)


# ================================================================================================ the second-order block
TT, XX, YY, ZZ = sp.symbols('t x y z', real=True)
X3 = (XX, YY, ZZ)
EPS = sp.Symbol('e_b')
alc, c2s, Cph, lam, sgm, bet, Ceff = sp.symbols('alpha_c c_2 C_phi lambda sigma beta C_eff', real=True)
kq, wq = sp.symbols('k omega', real=True)
An, Ap, AB, AS, AF, AM = sp.symbols('A_n A_psi A_B A_S A_phi A_mu')
AMP = {"n": An, "psi": Ap, "B": AB, "S": AS, "phi": AF, "mu": AM}


def block(sector="aqual", form="c2", with_beta=False):
    """The root's quadratic action about Minkowski in unitary gauge, re-derived (FP14's unitary_block construction):
    sector = 'aqual' (FP7/FP14: chassis (2 - a_c)[2 a.Dchi - |Dchi|^2], chi = sigma phi, -2 C_phi |D phi|^2, 2 lambda (n.d phi)^2)
           | 'ch'    (FP2: 2 |DU - a|^2 + 2 C_eff |DU|^2)  | 'none' (pure khronometric: GR + BPS);
    form = 'c2' (-c_2 K^2: at k != 0 the leaf-averaged term equals the plain one) | 'mult' (-2 mu K, the c_2 -> oo limit);
    with_beta: add -beta K_ij K^ij (BPS's beta; (1 - beta) K_ij K^ij in ADM form) for the literature control.
    Returns the Fourier-space Euler-Lagrange expressions (plane wave e^{i(kz - wt)}) keyed by field name."""
    nf, pf, Bf, Sf, Ff, Mf = [sp.Function(s_)(TT, XX, YY, ZZ) for s_ in ('n', 'psi', 'B', 'S', 'phi', 'mu')]
    Nl = sp.exp(EPS * nf)
    gam = sp.diag(*[sp.exp(-2 * EPS * pf)] * 3)
    gin = gam.inv()
    Ni = [EPS * (sp.diff(Bf, X3[0]) + Sf), EPS * sp.diff(Bf, X3[1]), EPS * sp.diff(Bf, X3[2])]
    Gm3 = [[[sum(gin[a_, d_] * (sp.diff(gam[d_, b_], X3[c_]) + sp.diff(gam[d_, c_], X3[b_]) - sp.diff(gam[b_, c_], X3[d_]))
                 for d_ in range(3)) / 2 for c_ in range(3)] for b_ in range(3)] for a_ in range(3)]
    DN = [[sp.diff(Ni[j], X3[i]) - sum(Gm3[q][i][j] * Ni[q] for q in range(3)) for j in range(3)] for i in range(3)]
    Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], TT) - DN[i][j] - DN[j][i]) / (2 * Nl))
    Kup = gin * Kij * gin
    KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3))
    trK = sum(gin[i, j] * Kij[i, j] for i in range(3) for j in range(3))

    def Ric3(b_, c_):
        return sum(sp.diff(Gm3[a_][b_][c_], X3[a_]) - sp.diff(Gm3[a_][b_][a_], X3[c_]) +
                   sum(Gm3[a_][a_][d_] * Gm3[d_][b_][c_] - Gm3[a_][c_][d_] * Gm3[d_][b_][a_] for d_ in range(3)) for a_ in range(3))
    R3 = sum(gin[b_, c_] * Ric3(b_, c_) for b_ in range(3) for c_ in range(3))
    ai = [sp.diff(sp.log(Nl), xi_) for xi_ in X3]
    aa = sum(gin[i, j] * ai[i] * ai[j] for i in range(3) for j in range(3))
    Fi = [sp.diff(EPS * Ff, xi_) for xi_ in X3]
    if sector == "aqual":
        Xi = [sgm * Fi[i] for i in range(3)]
        Bch, Cch = 2 * (2 - alc), -(2 - alc)
        mond = (Bch * sum(gin[i, j] * ai[i] * Xi[j] for i in range(3) for j in range(3))
                + Cch * sum(gin[i, j] * Xi[i] * Xi[j] for i in range(3) for j in range(3))
                - 2 * Cph * sum(gin[i, j] * Fi[i] * Fi[j] for i in range(3) for j in range(3)))
        ndphi = (sp.diff(EPS * Ff, TT) - sum(sum(gin[i, j] * Ni[j] for j in range(3)) * Fi[i] for i in range(3))) / Nl
        mond += 2 * lam * ndphi ** 2
    elif sector == "ch":
        Ui = Fi                                                          # U lives in the phi slot
        mond = (2 * sum(gin[i, j] * (Ui[i] - ai[i]) * (Ui[j] - ai[j]) for i in range(3) for j in range(3))
                + 2 * Ceff * sum(gin[i, j] * Ui[i] * Ui[j] for i in range(3) for j in range(3)))
    else:
        mond = 0
    kin = -c2s * trK ** 2 if form == "c2" else -2 * EPS * Mf * trK
    beta_term = -bet * KK if with_beta else 0
    flds = [nf, pf, Bf, Sf] + ([Ff] if sector != "none" else []) + ([Mf] if form == "mult" else [])
    Lfull = Nl * sp.exp(-3 * EPS * pf) * (KK - trK ** 2 + R3 + alc * aa + kin + beta_term + mond)
    L2 = sp.expand((sp.diff(Lfull, EPS, 2) / 2).subs(EPS, 0))
    ELf = euler_equations(L2, flds, [TT, XX, YY, ZZ])
    phs = sp.exp(sp.I * (kq * ZZ - wq * TT))
    fsub = {nf: An * phs, pf: Ap * phs, Bf: AB * phs, Sf: AS * phs, Ff: AF * phs, Mf: AM * phs}
    ELk = [sp.expand(sp.simplify((e_.lhs - e_.rhs).subs(fsub).doit() / phs)) for e_ in ELf]
    return dict(zip([f_.func.__name__ for f_ in flds], ELk))


def mmat(E, order):
    return sp.Matrix([[sp.expand(sp.diff(E[r_], AMP[c_])) for c_ in order] for r_ in order])


# ================================================================================================ FP2's moving-source PPN pipeline
kB, wB, vB, GA, muB = sp.symbols('k omega v G_ae mu', real=True)
kpB = sp.symbols('kp', positive=True)
MB = sp.symbols('M', positive=True)
dlC = sp.Symbol('dlnC', real=True)


def ppn(E, scalar_fields=("phi",), leaf_symbol=None):
    """FP2 B's pipeline, re-implemented: a source of rest mass M moving at v through the khronon frame (momentum rho v,
    stress rho v^2), the block solved for (n, psi, B, scalar(s)), h'_00 in the source's rest frame (boost + Jacobian),
    alpha_1 from the isotropic O(v^2) part, alpha_2 from the (v.k-hat)^2 part, gamma and alpha_3 (g_0j reading) from the
    static solution.  leaf_symbol: a coefficient living on the khronon leaves (C_eff in FP2) is dressed as
    C -> C (1 + dlnC (g^2 - 1) mu^2) (FP2's boosted-leaf |k|^2)."""
    ELB = {k_: v_.subs({kq: kB, wq: wB}) for k_, v_ in E.items()}
    Pf = 1 / (16 * sp.pi * GA)
    gm = 1 / sp.sqrt(1 - vB ** 2)
    BOOST = {kB: kpB * sp.sqrt(1 + (gm ** 2 - 1) * muB ** 2), wB: gm * kpB * muB * vB}
    scal = [s_ for s_ in scalar_fields if s_ in ELB]
    unknowns = [An, Ap, AB] + [AMP[s_] for s_ in scal]

    def ms_solve(rho, sub):
        J_long, Pi = rho * wB, rho * vB ** 2
        eqs = [sp.Eq(Pf * ELB["n"].subs(sub), rho), sp.Eq(Pf * ELB["psi"].subs(sub), Pi),
               sp.Eq(Pf * ELB["B"].subs(sub), sp.I * J_long)] + [sp.Eq(ELB[s_].subs(sub), 0) for s_ in scal]
        s_ = sp.solve(eqs, unknowns, dict=True)
        return s_[0] if s_ else None

    S_PER_J = sp.solve(sp.Eq(Pf * ELB["S"] + 1, 0), AS)[0]

    def h00_rest(sol, rho):
        PhiB = sol[An] - sp.I * wB * sol[AB]
        S_dot_v = S_PER_J * rho * (vB ** 2 - wB ** 2 / kB ** 2)
        h = gm ** 2 * (-2 * PhiB - 2 * vB ** 2 * sol[Ap] + 2 * S_dot_v)
        return gm * h.subs(BOOST)

    def v2_parts(expr):
        s_ = sp.expand(sp.series(expr, vB, 0, 3).removeO())
        return (sp.simplify(s_.coeff(vB, 0)), sp.factor(sp.simplify(s_.coeff(vB, 2).subs(muB, 0))),
                sp.factor(sp.simplify(s_.coeff(vB, 2).coeff(muB, 2))))

    sol = ms_solve(gm * MB, {})
    h = h00_rest(sol, gm * MB)
    if leaf_symbol is not None:
        h = h.subs(leaf_symbol, leaf_symbol * (1 + dlC * (gm ** 2 - 1) * muB ** 2))
    h0 = sp.simplify(h.subs(vB, 0))
    o0, Aiso, Cani = v2_parts(sp.simplify(h / h0))
    alpha1 = sp.factor(-2 * Aiso)
    alpha2 = sp.factor(Cani)
    sol0 = ms_solve(MB, {vB: 0})
    s0 = {kk_: sp.simplify(vv_.subs({vB: 0, wB: 0})) for kk_, vv_ in sol0.items()}
    gamma = sp.simplify(s0[Ap] / s0[An])
    U_obs = sp.simplify(-s0[An])
    h0jT = sp.simplify(-2 * s0[An] - 2 * s0[Ap] + S_PER_J * MB)
    alpha1_g0j = sp.factor(sp.simplify(-2 * h0jT / U_obs))
    return dict(alpha1=alpha1, alpha2=alpha2, gamma=gamma, alpha3=sp.simplify(alpha1 - alpha1_g0j), o0=o0,
                U=sp.factor(U_obs))


# ================================================================================================ kernels
def x_P2(y):
    """P2's two-field AQUAL scalar gradient x = |grad phi|/a0 for a Newtonian field y = g_N/a0: mu_s(x) x = y, mu_s = x/(1 - 2x)."""
    y = np.maximum(np.asarray(y, float), 0.0)
    return np.where(y > 0, 1.0 / (1.0 + np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))), 0.0)


def mu_s(x):
    return x / (1 - 2 * x)


def CT_aq(x):            # transverse AQUAL coefficient mu_s(x)
    return mu_s(x)


def CL_aq(x):            # longitudinal (x mu_s)' = 2x(1 - x)/(1 - 2x)^2
    return 2 * x * (1 - x) / (1 - 2 * x) ** 2


def yN_of(g_obs, a0):
    """P2 inverted: g/a0 = sqrt(yN^2 + yN)."""
    return (-1 + math.sqrt(1 + 4 * (g_obs / a0) ** 2)) / 2


def build_nu_mono():
    """FP2 / L340's nu_mono (the chain's operative kernel), copied from FP2 (its definition, not its numbers)."""
    def h_rar(y):
        y = np.asarray(y, float)
        with np.errstate(over="ignore"):
            return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)

    def dh_rar(y, e=1e-6):
        return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
    Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0)
    H_P = float(h_rar(Y_P))
    DELTA = 0.05
    LYG = np.linspace(-12, 12, 240001)
    YG = 10 ** LYG
    DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
    H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])

    def nu_mono(y):
        y = np.maximum(np.asarray(y, float), 1e-12)
        return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y

    def CT_of(y):
        return nu_mono(y) - 1.0

    def CL_of(y):
        y = np.asarray(y, float)
        e = 1e-5
        return ((y * (1 + e)) * nu_mono(y * (1 + e)) - (y * (1 - e)) * nu_mono(y * (1 - e))) / (2 * y * e) - 1.0
    return dict(nu=nu_mono, CT=CT_of, CL=CL_of, y_p=Y_P, h_p=H_P)


# FP2's real-space conversions of the Gaussian filter's k-space factors (gradient ratios at radius r)
def F1(r, xi):          # e^{-xi^2 k^2}
    return (math.erf(r / (2 * xi)) - (r / (xi * math.sqrt(math.pi))) * math.exp(-r * r / (4 * xi * xi))
            if r / xi > 1e-3 else (r / xi) ** 3 / (6 * math.sqrt(math.pi)))


def F2(r, xi):          # xi^2 k^2 e^{-xi^2 k^2}
    return (r / xi) ** 3 * math.exp(-r * r / (4 * xi * xi)) / (4 * math.sqrt(math.pi))


def F4(r, xi):          # e^{-2 xi^2 k^2}
    return F1(r, math.sqrt(2) * xi)


# ================================================================================================ TOV (piecewise polytropes)
G_CGS, C_CGS, MSUN_G = 6.67430e-8, 2.99792458e10, 1.98847e33
# Read, Lackey, Owen & Friedman 2009 (PRD 79, 124032): SLy's core fit, log10 p1 = 34.384 (p1 in dyn/cm^2 at rho1 =
# 10^14.7 g/cm^3), Gamma = 3.005, 2.988, 2.851 with dividing densities 10^14.7 and 10^15 g/cm^3.  The crust is simplified to
# the last SLy crust piece (p/c^2 = 3.99874e-8 rho^1.35692, g/cm^3 units) continued to zero density; it carries a negligible
# mass and the lane's quantities (compactness, binding fraction, Komar mass) are core-dominated.  Sanity gate: M_max ~ 2.05
# Msun and R(1.4) ~ 11.7 km (Read+09's SLy).
SLY_CRUST_LAST = (3.99874e-8 * C_CGS ** 2, 1.35692)


def make_pp_eos(logp1=34.384, g1=3.005, g2=2.988, g3=2.851):
    """a piecewise-polytropic EOS (cgs): p(rho) [dyn/cm^2], eps(rho) [energy density / c^2, g/cm^3], rho(p)."""
    rho1, rho2 = 10 ** 14.7, 10 ** 15.0
    K1 = 10 ** logp1 / rho1 ** g1
    K2 = K1 * rho1 ** (g1 - g2)
    K3 = K2 * rho2 ** (g2 - g3)
    Kc, Gc = SLY_CRUST_LAST
    rho0 = (Kc / K1) ** (1.0 / (g1 - Gc))                         # crust-core join
    pieces = [(Kc, Gc, 0.0), (K1, g1, rho0), (K2, g2, rho1), (K3, g3, rho2)]
    avals = [0.0]
    for i in range(1, len(pieces)):
        Kp, Gp, _ = pieces[i - 1]
        K, Gm, r0 = pieces[i]
        e_prev = (1 + avals[-1]) * r0 + Kp * r0 ** Gp / (Gp - 1) / C_CGS ** 2
        avals.append(e_prev / r0 - 1 - K * r0 ** (Gm - 1) / (Gm - 1) / C_CGS ** 2)
    starts = np.array([p_[2] for p_ in pieces])

    def piece(rho):
        return max(int(np.searchsorted(starts, rho, side="right") - 1), 0)

    def p_of_rho(rho):
        K, Gm, _ = pieces[piece(rho)]
        return K * rho ** Gm

    def eps_of_rho(rho):
        i = piece(rho)
        K, Gm, _ = pieces[i]
        return (1 + avals[i]) * rho + K * rho ** Gm / (Gm - 1) / C_CGS ** 2

    def rho_of_p(p):
        for i in range(len(pieces) - 1, -1, -1):
            K, Gm, r0 = pieces[i]
            rho = (p / K) ** (1.0 / Gm)
            if rho >= r0 * (1 - 1e-12):
                return rho
        K, Gm, _ = pieces[0]
        return (p / K) ** (1.0 / Gm)
    return dict(p=p_of_rho, eps=eps_of_rho, rho=rho_of_p, pieces=pieces, join=rho0)


def tov_star(eos, rho_c, r_max=4e6, want_profile=False):
    """TOV in cgs; returns M (grav, Msun), R (km), M_baryon (Msun), compactness C = GM/(Rc^2), the binding fraction
    (M_b - M)/M, the Komar mass (Msun) from int 4 pi r^2 e^{Phi + Lambda} (eps + 3p/c^2) dr, and optionally the profile."""
    pc = eos["p"](rho_c)

    def rhs(r, Y):
        m, p, mb, phi, mk = Y
        if p <= 0:
            return [0, 0, 0, 0, 0]
        rho = eos["rho"](p)
        e = eos["eps"](rho)
        fac = 1 - 2 * G_CGS * m / (r * C_CGS ** 2)
        dm = 4 * math.pi * r * r * e
        dp = -G_CGS * (e + p / C_CGS ** 2) * (m + 4 * math.pi * r ** 3 * p / C_CGS ** 2) / (r * r * fac)
        dmb = 4 * math.pi * r * r * rho / math.sqrt(fac)
        dphi = G_CGS * (m + 4 * math.pi * r ** 3 * p / C_CGS ** 2) / (r * r * C_CGS ** 2 * fac)
        dmk = 4 * math.pi * r * r * (e + 3 * p / C_CGS ** 2) * math.exp(phi) / math.sqrt(fac)
        return [dm, dp, dmb, dphi, dmk]

    def surf(r, Y):
        return Y[1] - 1e-12 * pc
    surf.terminal = True
    surf.direction = -1
    r0 = 1.0
    e0 = eos["eps"](rho_c)
    Y0 = [4 / 3 * math.pi * r0 ** 3 * e0, pc, 4 / 3 * math.pi * r0 ** 3 * rho_c, 0.0, 4 / 3 * math.pi * r0 ** 3 * (e0 + 3 * pc / C_CGS ** 2)]
    sol = solve_ivp(rhs, (r0, r_max), Y0, events=surf, rtol=1e-10, atol=1e-30, method="LSODA", dense_output=want_profile)
    R = sol.t[-1]
    m, p, mb, phi, mk = sol.y[:, -1]
    # normalise Phi so that e^{2 Phi(R)} = 1 - 2GM/(Rc^2); the Komar integrand carries e^{Phi}
    shift = 0.5 * math.log(1 - 2 * G_CGS * m / (R * C_CGS ** 2)) - phi
    Mk = mk * math.exp(shift)
    out = dict(M=m / MSUN_G, R_km=R / 1e5, Mb=mb / MSUN_G, C=G_CGS * m / (R * C_CGS ** 2), bind=(mb - m) / m, M_komar=Mk / MSUN_G,
               rho_c=rho_c)
    if want_profile:
        out["sol"] = sol
        out["phi_shift"] = shift
    return out


def star_of_mass(eos, M_target, lo=2e14, hi=10 ** 15.28):
    f = lambda lr: tov_star(eos, 10 ** lr)["M"] - M_target
    lr = brentq(f, math.log10(lo), math.log10(hi), xtol=1e-7)
    return tov_star(eos, 10 ** lr)
