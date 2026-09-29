#!/usr/bin/env python3
"""S2-1 -- ROUTE B: the exactly massless limit of the dS_4 Dirac-fermion induced current, from flat-space QED plus the Weyl anomaly.
Independent of lane Q1's mode sum, Bloch-vector / adiabatic subtraction and of the published closed form; Q1's weak-field function is imported READ-ONLY
only as the comparator (Q1_ds4_fermions/q1_lib.py: hfy_weak).

Pre-registered in S2_PREREGISTRATION.md (before this script was run).  Units H = 1, planar patch, tau = -T (a = 1/T), evaluation at T = 1.
Scheme (stated): ON-SHELL at mass m, i.e. the flat vacuum polarization of the massive field vanishes at q^2 = 0, then m -> 0 (the massless Pi_hat below is the m -> 0 limit
at fixed Q^2 of that on-shell function).  Field: F_{tau z} = E a^2 (force on the charge along -z), linear response.  J_par := current along the force = -J^z.

Run:     python3 s2_1_massless_fermion.py            (real run; exit 0 iff every check passes)
         python3 s2_1_massless_fermion.py --mutate   (control: the Weyl-anomaly term is dropped, coefficient 0 instead of 2; W4b and W6 must both FAIL;
                                                      exit 1 if both fail = the control works, exit 3 if either passes = the control has no power)
Only the literal argument --mutate triggers the control (a positional MUTATE runs the real path).
Set PYTHONDONTWRITEBYTECODE=1 (the script also sets sys.dont_write_bytecode).

Checks: W0 Weyl map (sympy); W1 vacuum-polarization integrals; W2 numerical retarded response of the exact MASSIVE flat Pi_hat (spectral representation) -> massless limit;
W3 plus-distribution evaluation (analytic + numeric) and the Laplace identity; W4 anomaly coefficient (a: D-dim pole algebra, b: de Sitter invariance); W5 assembly; W6 comparison with Q1.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import numpy as np
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "Q1_ds4_fermions"))
from q1_lib import hfy_weak            # comparator only (read-only import)

MUTATE = "--mutate" in sys.argv
CHECKS = {}
GAMMA = float(mp.euler)


def check(tag, ok, detail=""):
    CHECKS[tag.split()[0]] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


# ---------------------------------------------------------------------------------------------------- W0
def gamma_matrices():
    """mostly-plus Clifford: {g^a, g^b} = 2 eta^{ab}, eta = diag(-1,1,1,1); g^a = i * (standard mostly-minus Dirac matrices)."""
    I2 = sp.eye(2)
    Z2 = sp.zeros(2)
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    def blk(a, b, c, d):
        return sp.Matrix(sp.BlockMatrix([[a, b], [c, d]]))
    G0 = blk(I2, Z2, Z2, -I2)
    Gk = [blk(Z2, s, -s, Z2) for s in (sx, sy, sz)]
    return [sp.I * G0] + [sp.I * g for g in Gk]


def w0_weyl_map():
    print("\nW0. Weyl map: the massless Dirac operator in g = a^2 eta acts on psi = a^{-3/2} Xi as a^{-5/2} times the flat operator")
    t, x, y, z = sp.symbols("t x y z", real=True)
    X = [t, x, y, z]
    a = -1 / t
    g = sp.diag(-a ** 2, a ** 2, a ** 2, a ** 2)
    ginv = g.inv()
    Gam = [[[sp.simplify(sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2)
             for n in range(4)] for m in range(4)] for l in range(4)]
    eta = sp.diag(-1, 1, 1, 1)
    e_up = sp.eye(4) / a          # e_b^nu   [b, nu]
    e_dn = sp.eye(4) * a          # e^a_nu   [a, nu]
    gam = gamma_matrices()
    for i in range(4):
        for j in range(4):
            assert sp.simplify(gam[i] * gam[j] + gam[j] * gam[i] - 2 * eta[i, j] * sp.eye(4)) == sp.zeros(4)
    # omega_mu^a_b = e^a_nu (d_mu e_b^nu + Gam^nu_{mu lam} e_b^lam)
    om = [[[sp.simplify(sum(e_dn[A, nu] * (sp.diff(e_up[B, nu], X[mu]) + sum(Gam[nu][mu][lam] * e_up[B, lam] for lam in range(4))) for nu in range(4)))
            for B in range(4)] for A in range(4)] for mu in range(4)]
    def Sigma(mu, c):
        S = sp.zeros(4)
        for A in range(4):
            for B in range(4):
                S += sp.Rational(1, 4) * c * eta[A, A] * om[mu][A][B] * gam[A] * gam[B]      # (c/4) omega_{mu AB} g^A g^B, omega_{AB} = eta_AA omega^A_B
        return S
    # covariantly constant gamma^nu(x) = e_a^nu g^a fixes the sign c
    good = []
    for c in (+1, -1):
        ok = True
        for mu in range(4):
            Sg = Sigma(mu, c)
            for nu in range(4):
                gn = sum((e_up[A, nu] * gam[A] for A in range(4)), sp.zeros(4))
                res = sp.diff(gn, X[mu]) + sum((Gam[nu][mu][lam] * sum((e_up[A, lam] * gam[A] for A in range(4)), sp.zeros(4)) for lam in range(4)), sp.zeros(4)) + Sg * gn - gn * Sg
                if sp.simplify(res) != sp.zeros(4):
                    ok = False
        good.append(ok)
    c = +1 if good[0] else (-1 if good[1] else 0)
    check("W0a spin connection sign found by nabla gamma = 0", c != 0, f"(c = {c}; +1: {good[0]}, -1: {good[1]})")
    Xi = sp.Matrix([sp.Function(f"X{i}")(t, x, y, z) for i in range(4)])
    psi = a ** sp.Rational(-3, 2) * Xi
    Dpsi = sp.zeros(4, 1)
    for mu in range(4):
        gmu = sum((e_up[A, mu] * gam[A] for A in range(4)), sp.zeros(4))
        Dpsi += gmu * (sp.diff(psi, X[mu]) + Sigma(mu, c) * psi)
    flat = sp.zeros(4, 1)
    for A in range(4):
        flat += gam[A] * sp.diff(Xi, X[A])
    res = sp.simplify(Dpsi - a ** sp.Rational(-5, 2) * flat)
    check("W0b D-slash(a^{-3/2} Xi) = a^{-5/2} gamma^a d_a Xi (residual identically 0)", res == sp.zeros(4, 1))
    return c


# ---------------------------------------------------------------------------------------------------- W1
def feynman_pi(Q2, spin="f"):
    """Pi_hat in units alpha/pi:  fermion -2 Int x(1-x) ln(1 + x(1-x) Q2);  scalar -(1/4) Int (1-2x)^2 ln(1 + x(1-x) Q2); m = 1."""
    Q2 = mp.mpf(Q2)
    if spin == "f":
        return -2 * mp.quad(lambda x: x * (1 - x) * mp.log(1 + x * (1 - x) * Q2), [0, 0.5, 1])
    return -mp.mpf(1) / 4 * mp.quad(lambda x: (1 - 2 * x) ** 2 * mp.log(1 + x * (1 - x) * Q2), [0, 0.5, 1])


def R_spec(w, m, spin="f"):
    x = 4 * m ** 2 / w ** 2
    if spin == "f":
        return (1 + x / 2) * mp.sqrt(1 - x)
    return (1 - x) ** mp.mpf(1.5)


BETA = {"f": mp.mpf(1) / 3, "s": mp.mpf(1) / 12}      # units alpha/pi: coefficient of -ln Q^2


def disp_pi(Q2, spin="f"):
    """dispersive form, m = 1, units alpha/pi:  -BETA Q2 Int_4^inf ds R(s)/(s (s+Q2))."""
    Q2 = mp.mpf(Q2)
    f = lambda s: R_spec(mp.sqrt(s), 1, spin) / (s * (s + Q2))
    return -BETA[spin] * Q2 * mp.quad(f, [4, 6, 20, 200, 2000, mp.inf])


def w1_vacuum_polarization():
    print("\nW1. one-loop vacuum polarization, on-shell scheme (recalled; verified here)")
    xs = sp.symbols("x", positive=True)
    val = sp.integrate(xs * (1 - xs) * sp.log(xs * (1 - xs)), (xs, 0, 1))
    check("W1a Int x(1-x) ln(x(1-x)) = -5/18 exactly (sympy)", sp.simplify(val + sp.Rational(5, 18)) == 0, f"({val})")
    mp.mp.dps = 30
    Q2 = mp.mpf(10) ** 8
    lhs = feynman_pi(Q2)
    rhs = -(mp.log(Q2) - mp.mpf(5) / 3) / 3
    check("W1b m -> 0 form: -2 Int x(1-x) ln(1 + x(1-x)Q2/m2) = -(1/3)[ln(Q2/m2) - 5/3] (units alpha/pi) at Q2/m2 = 1e8, to 1e-6", abs(lhs - rhs) < 1e-6, f"(diff {float(lhs - rhs):.2e})")
    lo = feynman_pi(mp.mpf(10) ** -6) / mp.mpf(10) ** -6
    check("W1c small-Q2 slope = -1/15 (units alpha/pi per Q2/m2) to 1e-5", abs(lo + mp.mpf(1) / 15) < 1e-5 * (mp.mpf(1) / 15), f"(slope {float(lo):.8f} vs {-1/15:.8f})")
    worst = 0
    for q in (0.5, 3.0, 40.0):
        worst = max(worst, abs(feynman_pi(q) - disp_pi(q)))
    check("W1d spectral representation -(1/3) Q2 Int ds R(s)/(s(s+Q2)) equals the Feynman-parameter integral at Q2/m2 = 0.5, 3, 40 (1e-8)", worst < 1e-8, f"(worst {float(worst):.2e})")
    return


# ---------------------------------------------------------------------------------------------------- W2
def S_of_w(w):
    """S(w) = Int_0^inf sin(w u)/(1+u)^3 du = (w/2)(1 - w Sn1), Sn1 = cos w (pi/2 - Si w) + sin w Ci w."""
    Sn1 = mp.cos(w) * (mp.pi / 2 - mp.si(w)) + mp.sin(w) * mp.ci(w)
    return (w / 2) * (1 - w * Sn1)


def integrand_K(w, m, spin):
    return R_spec(w, m, spin) / w * (1 - w * S_of_w(w))


def K_of_m(m, spin="f", Omega=300):
    """K(m) = Int_{2m}^inf (dw/w) R(w^2) [1 - w S(w)],  tail beyond Omega by the asymptotic series 1 - wS = sum_{k>=1} (-1)^{k+1} (2k+2)!/2 / w^{2k}."""
    with mp.workdps(30):
        m = mp.mpf(m)
        pts = [2 * m]
        d = 10 ** math.floor(math.log10(float(2 * m)) + 1)
        while d < 1:
            pts.append(mp.mpf(d))
            d *= 10
        k = 1
        while k * math.pi < Omega:
            if k * math.pi > pts[-1]:
                pts.append(mp.mpf(k) * mp.pi)
            k += 1
        pts.append(mp.mpf(Omega))
        val = mp.quad(lambda w: integrand_K(w, m, spin), pts)
        Om = mp.mpf(Omega)
        tail = 0
        for kk in range(1, 6):
            coef = (-1) ** (kk + 1) * mp.factorial(2 * kk + 2) / 2
            tail += coef * Om ** (-2 * kk) / (2 * kk)          # Int_Omega^inf w^{-1} w^{-2k} dw = Omega^{-2k}/(2k)  (Amendment 2: the first run used Omega^{-(2k+1)}/(2k+1))
        return val + tail


def w2_spectral_response(spin, kappa_analytic):
    print(f"\nW2. retarded response of the exact MASSIVE flat Pi_hat ({'fermion' if spin=='f' else 'scalar'}) to D = d_tau F^{{tau z}} at tau = -1: K(m) + ln m -> kappa = 2/3 - gamma_E (analytic value {float(kappa_analytic):.10f})")
    ms = [0.1, 0.03, 0.01, 0.003, 0.001]
    errs = []
    kap = {}
    for m in ms:
        K = K_of_m(m, spin)
        kap[m] = K + mp.log(m)
        errs.append(abs(kap[m] - kappa_analytic))
        print(f"     m = {m:6.3f}   K(m) = {float(K):+.10f}   K + ln m = {float(kap[m]):+.10f}   error vs analytic {float(errs[-1]):.3e}")
    mono = all(errs[i] > errs[i + 1] for i in range(len(errs) - 1))
    return errs, mono, kap


# ---------------------------------------------------------------------------------------------------- W3
def w3_plus_distribution():
    print("\nW3. plus-distribution (time-domain) evaluation of ln(-i w) D, and the Laplace identity")
    mp.mp.dps = 30
    # Laplace identity on a test function f(t) = exp(-b t) theta(t):  (ln s)/(s+b)  <->  -gamma f(t) - lim [ Int_eps^t f(t-u)/u du + f(t) ln eps ]
    b, t0 = mp.mpf("0.7"), mp.mpf("1.3")
    ref = mp.invertlaplace(lambda s: mp.log(s) / (s + b), t0, method="talbot")
    def td(eps):
        integ = mp.quad(lambda u: mp.e ** (-b * (t0 - u)) / u, [eps, 0.1, t0])
        return -mp.euler * mp.e ** (-b * t0) - (integ + mp.e ** (-b * t0) * mp.log(eps))
    val = td(mp.mpf(10) ** -12)
    check("W3a Laplace identity: L^{-1}[ln s/(s+b)](t) = -gamma f - lim[Int_eps f(t-u)/u du + f ln eps] (b = 0.7, t = 1.3), to 1e-8", abs(val - ref) < 1e-8, f"(time-domain {float(val):.12f}, mpmath invertlaplace {float(ref):.12f})")
    # the field D(tau') = 2E/tau'^3 at tau = -T, E = 1: Flim(T) = lim [ Int_eps^inf D(tau - u)/u du + D(tau) ln eps ] = -(2/T^3)(ln T - 3/2)
    T, u, eps = sp.symbols("T u epsilon", positive=True)
    integral = sp.integrate(1 / (u * (T + u) ** 3), (u, eps, sp.oo))
    Flim = sp.limit(sp.simplify(-2 * integral + (-2 / T ** 3) * sp.log(eps)), eps, 0, "+")
    target = -(2 / T ** 3) * (sp.log(T) - sp.Rational(3, 2))
    check("W3b Flim(T) = -(2E/T^3)(ln T - 3/2) (sympy, exact)", sp.simplify(Flim - target) == 0, f"(sympy: {sp.simplify(Flim)})")
    # numeric at T = 1
    def Fnum(eps):
        return mp.quad(lambda uu: -2 / (1 + uu) ** 3 / uu, [eps, 1e-3, 0.1, 1, 10, mp.inf]) + (-2) * mp.log(eps)
    F1, F2 = Fnum(mp.mpf(10) ** -8), Fnum(mp.mpf(10) ** -10)
    check("W3c numeric T = 1 limit is 3 (E = 1) to 1e-7", abs(F2 - 3) < 1e-7 and abs(F1 - 3) < 1e-5, f"(eps = 1e-8: {float(F1):.10f}, 1e-10: {float(F2):.12f})")
    # constant kappa: J_flat = (4 alpha E/(3 pi)) K,  K = -ln m + kappa  ->  from  J_flat = Pi_hat D = -P [2 ln(-iw) D - (2 ln m + 5/3) D], D(-1) = -2E, ln(-iw)D = -gamma D - Flim
    D = -2
    lnD = -mp.euler * D - F2
    bracket = 2 * lnD - (2 * mp.log(mp.mpf("1")) + mp.mpf(5) / 3) * D          # at m = 1, i.e. the m-independent part; ln m term separate (coefficient -2 D = 4)
    # J_flat = -P [ bracket_const + 4 ln m ]*(E) -> in units (4 alpha E/(3 pi)): K = -( bracket_const/4 + ln m )
    kappa = -bracket / 4
    return kappa, F2, sp.simplify(Flim)


# ---------------------------------------------------------------------------------------------------- W4
def w4_anomaly(c_used):
    print("\nW4. Weyl-anomaly coefficient of ln a (units P = alpha/(3 pi) for the fermion)")
    eps, lna, P, Q2, mu2 = sp.symbols("epsilon ln_a P Q2 mu2", positive=True)
    # (a) D-dim pole algebra: Pi_bare = P (2/eps) (Q2/mu2)^(-eps/2) h(eps), counterterm dZ = -P (2/eps) cancels the pole; sqrt(g) F^2 -> a^{D-4} F^2 = a^{-eps} F^2
    Pibare = P * (2 / eps) * (Q2 / mu2) ** (-eps / 2)
    ser = sp.series(Pibare, eps, 0, 1).removeO()
    pole = sp.simplify(ser.coeff(eps, -1))
    logc = sp.expand(sp.expand_log(ser.coeff(eps, 0), force=True))
    dZ = -pole / eps
    extra = sp.series(dZ * (sp.exp(-eps * lna) - 1), eps, 0, 1).removeO()
    c_pole = sp.simplify(extra / (P * lna))
    check("W4a D-dim pole algebra: pole = 2P/eps, ln Q2 coefficient = -P, counterterm times (a^{-eps} - 1) leaves +2 P ln a", pole == 2 * P and sp.simplify(logc.coeff(sp.log(Q2), 1) + P) == 0 and c_pole == 2,
          f"(pole {pole}; finite: {logc}; anomaly coefficient {c_pole} P ln a)")
    # (b) de Sitter invariance: J_phys(T) = T^3 (J_flat(T) + J_an(T)) must be T-independent
    T, E, m, c, gam = sp.symbols("T E m c gamma", positive=True)
    tau = sp.symbols("tau", negative=True)
    D = -2 * E / T ** 3
    Flim = -(2 * E / T ** 3) * (sp.log(T) - sp.Rational(3, 2))
    lnD = -gam * D - Flim
    Jflat = -P * (2 * lnD - (2 * sp.log(m) + sp.Rational(5, 3)) * D)
    a = -1 / tau
    Fup = -E / tau ** 2
    Jan = c * P * sp.diff(sp.log(a) * Fup, tau)
    Jan_T = Jan.subs(tau, -T)
    Jphys = sp.simplify(T ** 3 * (Jflat + Jan_T))
    dJ = sp.simplify(sp.diff(Jphys, T))
    sol = sp.solve(sp.Eq(dJ, 0), c)
    check("W4b dJ_phys/dT = 0 (de Sitter invariance) holds iff the anomaly coefficient is 2 (sympy solve)", sol == [2], f"(solution {sol})")
    used = c_used
    dJ_used = sp.simplify(dJ.subs(c, used))
    check("W4b' the coefficient USED in this run makes the physical current T-independent", dJ_used == 0, f"(c used = {used}; dJ/dT = {dJ_used})")
    return Jphys.subs(c, used)


# ---------------------------------------------------------------------------------------------------- main
def main():
    print("=" * 118)
    print(f"S2-1 massless-limit route for the dS_4 Dirac fermion -- mode: {'MUTATE CONTROL (anomaly term dropped)' if MUTATE else 'REAL RUN'}")
    print("=" * 118)
    w0_weyl_map()
    w1_vacuum_polarization()
    kappa_an = mp.mpf(2) / 3 - mp.euler
    errs, mono, kap = w2_spectral_response("f", kappa_an)
    check("W2 spectral response -> kappa: error at m = 1e-3 <= 1e-4 and monotone decreasing along m = 0.1, 0.03, 0.01, 0.003, 0.001", errs[-1] <= 1e-4 and mono, f"(errors {[f'{float(e):.1e}' for e in errs]})")
    kappa_num, F2, Flim = w3_plus_distribution()
    check("W3d constant kappa from the plus-distribution evaluation equals 2/3 - gamma_E to 1e-8", abs(kappa_num - kappa_an) < 1e-8, f"(kappa = {float(kappa_num):.12f}; 2/3 - gamma = {float(kappa_an):.12f})")
    c_an = 0 if MUTATE else 2
    Jphys = w4_anomaly(c_an)
    # W5 assembly: J^z_flat = (4 alpha E/(3 pi)) K,  K = -ln m + kappa;  J^z_an = (c alpha/(3 pi)) E * (-1) at T = 1;  J_par = -J^z;  sigma_HFY = J_par/(4 pi alpha E)
    print("\nW5. assembly (numerical ingredients): sigma_HFY = (1/(3 pi^2)) (ln M + c_B),  c_B = c_an/4 - kappa")
    c_B = mp.mpf(c_an) / 4 - kappa_num
    print(f"     kappa (W3, numeric) = {float(kappa_num):.12f};  anomaly coefficient used = {c_an};  c_B = {float(c_B):.12f}   [gamma_E - 1/6 = {float(mp.euler - mp.mpf(1)/6):.12f}]")
    c_B_alt = mp.mpf(c_an) / 4 - kap[0.001]                # from the m = 1e-3 spectral response alone
    print(f"     cross-check from the spectral response at m = 1e-3 alone: c_B = {float(c_B_alt):.10f} (difference {float(c_B_alt - c_B):+.2e})")
    # W6 comparison with Q1
    print("\nW6. comparison with lane Q1 (weak-field function sigma_HFY(M), HFY 4.3, imported read-only)")
    Ms = [0.1, 0.03, 0.01, 0.003, 0.001]
    cQ = {}
    print("     M        G_f (Q1, 4pi sigma)      G_f (route B, (4/3pi)(ln M + c_B))    rel diff     c_Q1(M) = 3 pi^2 sigma - ln M")
    for M in Ms:
        s = hfy_weak(M)
        cQ[M] = 3 * math.pi ** 2 * s - math.log(M)
        GQ = 4 * math.pi * s
        GB = 4 / (3 * math.pi) * (math.log(M) + float(c_B))
        print(f"     {M:6.3f}   {GQ:+.10e}         {GB:+.10e}                {abs(GB / GQ - 1):.3e}     {cQ[M]:+.10f}")
    A = np.array([[1.0, M ** 2, M ** 4] for M in (0.01, 0.003, 0.001)])
    bvec = np.array([cQ[M] for M in (0.01, 0.003, 0.001)])
    c0, c1, c2 = np.linalg.solve(A, bvec)
    print(f"     extrapolation (c0 + c1 M^2 + c2 M^4 through M = 0.01, 0.003, 0.001): c_Q1(0) = {c0:.12f}, c1 = {c1:.6f};  gamma_E - 1/6 = {float(mp.euler - mp.mpf(1)/6):.12f}")
    diff = abs(float(c_B) - c0)
    print(f"     |c_B - c_Q1(0)| = {diff:.3e}")
    check("W6 route B constant equals Q1's light-mass constant: |c_B - c_Q1(0)| <= 1e-6 (pre-registered CONFIRMED level)", diff <= 1e-6, f"(difference {diff:.2e})")
    if diff <= 1e-6:
        verdict = "CONFIRMED (fermion-only; the overall route-B verdict additionally needs the scalar validation of s2_2)"
    elif diff > 1e-3:
        verdict = "CONTRADICTED (all ingredient gates pass but the constants differ by > 1e-3) -- must be localised"
    else:
        verdict = "UNDECIDABLE (1e-6 < difference <= 1e-3)"
    ing = all(CHECKS[k] for k in ("W0a", "W0b", "W1a", "W1b", "W1c", "W1d", "W2", "W3a", "W3b", "W3c", "W3d", "W4a", "W4b"))
    print(f"\nroute B fermion-only verdict (ingredient gates {'all pass' if ing else 'NOT all pass -> UNDECIDABLE regardless'}): {verdict if ing else 'UNDECIDABLE'}")
    print("=" * 118)
    n_ok = sum(CHECKS.values())
    print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
    print("Scope: massless conformal Dirac field, on-shell(m) scheme, linear in E, first order; the ln M coefficient is a coefficient identity and is not scored.")
    print("alpha stays an INPUT.  kappa = 1/2 stays FITTED.  The SM-mass wall is unchanged.")
    if MUTATE:
        targeted_failed = (not CHECKS["W4b'"]) and (not CHECKS["W6"])
        if targeted_failed:
            print("\nMUTATE CONTROL: the anomaly term was dropped; W4b' (dS invariance) and W6 FAILED as required -- the control works")
            sys.exit(1)
        print("\nMUTATE CONTROL: a targeted check did NOT fail -- the control has no power")
        sys.exit(3)
    sys.exit(0 if n_ok == len(CHECKS) else 2)


if __name__ == "__main__":
    main()
