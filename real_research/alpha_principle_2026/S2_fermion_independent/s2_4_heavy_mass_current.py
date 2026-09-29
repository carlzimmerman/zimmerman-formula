#!/usr/bin/env python3
"""S2-4 -- ROUTE C, part 2: heavy-mass (derivative / heat-kernel) expansion of the dS_4 induced current, de Sitter evaluation, and comparison with lane Q1's heavy-mass limit.
Independent of lane Q1's mode sum, Bloch-vector / adiabatic subtraction and of the published closed form; Q1's weak-field function is imported READ-ONLY only as the comparator.

Pre-registered in S2_PREREGISTRATION.md (with Amendments 4-5).  Units H = 1, planar patch, a = -1/tau, coordinates (tau, x, y, z), signature (-+++), F_{tau z} = f'(tau) = E a^2 (force on the charge along -z).
Effective action (one loop, Euclidean, heavy mass m):  Gamma_E = (1/(32 pi^2 m^2)) Int sqrt(g) tr a_3  (Dirac),  Gamma_E = -(1/(16 pi^2 m^2)) Int sqrt(g) tr a_3  (complex scalar);  L_Minkowski = -L_E.
tr a_3 restricted to F^2 terms (recalled a_3, gated in s2_3): (q^2/360)[c1 S1 + ... + c6 S6] with
  S1 = (nabla_k F_ij)^2, S2 = (nabla^j F_ij)^2, S3 = F^ij Box F_ij, S4 = R^V_ijkl F^ij F^kl (R^V = -R^MTW), S5 = R_jk F^jn F^k_n, S6 = R F_ij F^ij.
Dirac: c = (28, -8, 72, -36, 16, -20).  Scalar (xi): c = (-8, -2, -12, 6, 4, -5 + 30 xi).
Current: J^z = (1/sqrt(-g)) delta S/delta A_z (Euler-Lagrange in the homogeneous A_z = f(tau)), physical J = a J^z, J_par = -J (force along -z); sigma_HFY M^2 = J_par m^2/(q^2 E) (q = e).

Checks: D0 geometry; D1 Lichnerowicz with the explicit spin connection; D2 Dirac coefficient vs -1/(36 pi^2); D3 vs Q1's closed form extrapolated to M -> infinity; D4 (informational) Drummond-Hathrell action;
D5 tau-independence; D6 pipeline validation on the heavy scalar (xi = 0, 1/6, 1/12) against (7/18 - 2 xi)/(4 pi^2) and the flat scalar Uehling gate.

Run:     python3 s2_4_heavy_mass_current.py            (real run; exit 0 iff every pre-registered check passes; D4 is informational and never affects the exit code)
         python3 s2_4_heavy_mass_current.py --mutate   (control: the recalled coefficient 2 of Omega_ij;j Omega_ik;k is replaced by 1; D2, D3 and D6 (xi = 0) must all FAIL;
                                                        exit 1 if all three fail = the control works, exit 3 otherwise)
Only the literal argument --mutate triggers the control.  Set PYTHONDONTWRITEBYTECODE=1.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import itertools
import numpy as np
import sympy as sp
import mpmath as mp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "Q1_ds4_fermions"))
import s2_1_massless_fermion as F1
from q1_lib import hfy_weak

MUTATE = "--mutate" in sys.argv
CHECKS = {}
INFO = {}
T2COEF = 1 if MUTATE else 2


def check(tag, ok, detail=""):
    CHECKS[tag.split()[0]] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def dirac_coefs():
    """same reduction as s2_3.coef_reduced with the recalled coefficients (T2 possibly mutated)"""
    C = dict(T1=8, T2=T2COEF, T3=12, Riem=-6, Ric=-4, ROO=5, EEii=60, EiEi=30, E3=60, EOO=30, EER=30)
    return [C["T1"] * (-4) + C["EiEi"] * 2, C["T2"] * (-4), C["T3"] * (-4) + C["EEii"] * 2, C["Riem"] * (-4) + C["EOO"] * (-2), C["Ric"] * (-4),
            C["ROO"] * (-4) + C["E3"] * sp.Rational(-3, 2) + C["EOO"] + C["EER"] * 2]


def scalar_coefs(xi):
    """complex scalar, tr 1 = 1, Omega = i q F, E = -xi R: T1 -> -8 S1, T2 -> -2 S2 (mutated: -T2COEF*... same coefficient), T3 -> -12 S3, Riem -> +6 S4, Ric -> +4 S5, ROO -> -5 S6, E Om Om -> +30 xi S6"""
    return [-8, -T2COEF, -12, 6, 4, -5 + 30 * xi]


# ------------------------------------------------------------------------------------ geometry (sympy)
X = sp.symbols("tau x y z", real=True)
tau = X[0]
f = sp.Function("f")
Esym = sp.symbols("E", positive=True)


def build_geometry():
    a = -1 / tau
    g = sp.diag(-a ** 2, a ** 2, a ** 2, a ** 2)
    gi = [1 / g[i, i] for i in range(4)]                       # diagonal inverse metric
    n = 4
    Gam = [[[sp.simplify(gi[l] * (sp.diff(g[l, m], X[nn]) + sp.diff(g[l, nn], X[m]) - sp.diff(g[m, nn], X[l])) / 2) for nn in range(n)] for m in range(n)] for l in range(n)]
    # Riemann (MTW): R^r_{s m n} = d_m Gam^r_{n s} - d_n Gam^r_{m s} + Gam^r_{m l} Gam^l_{n s} - Gam^r_{n l} Gam^l_{m s}
    Rup = [[[[sp.simplify(sp.diff(Gam[r][nn][s], X[m]) - sp.diff(Gam[r][m][s], X[nn]) + sum(Gam[r][m][l] * Gam[l][nn][s] - Gam[r][nn][l] * Gam[l][m][s] for l in range(n)))
              for nn in range(n)] for m in range(n)] for s in range(n)] for r in range(n)]
    RM = [[[[sp.simplify(g[r, r] * Rup[r][s][m][nn]) for nn in range(n)] for m in range(n)] for s in range(n)] for r in range(n)]        # R_{r s m n}, diagonal metric
    Ric = [[sp.simplify(sum(Rup[r][s][r][nn] for r in range(n))) for nn in range(n)] for s in range(n)]
    Rs = sp.simplify(sum(gi[i] * Ric[i][i] for i in range(n)))
    return a, g, gi, Gam, RM, Ric, Rs


def d0_geometry(geo):
    a, g, gi, Gam, RM, Ric, Rs = geo
    print("\nD0. de Sitter geometry (MTW sign)")
    ok_R = sp.simplify(Rs - 12) == 0
    ok_ric = all(sp.simplify(Ric[i][j] - 3 * g[i, j]) == 0 for i in range(4) for j in range(4))
    ok_riem = all(sp.simplify(RM[i][j][k][l] - (g[i, k] * g[j, l] - g[i, l] * g[j, k])) == 0 for i, j, k, l in itertools.product(range(4), repeat=4))
    check("D0a R = 12 H^2, R_mu nu = 3 H^2 g_mu nu, R_{mu nu rho sigma} = H^2 (g g - g g) (sympy, exact)", ok_R and ok_ric and ok_riem)


def field_tensors(geo):
    a, g, gi, Gam, RM, Ric, Rs = geo
    n = 4
    A = [0, 0, 0, f(tau)]
    F = [[sp.diff(A[nn], X[m]) - sp.diff(A[m], X[nn]) for nn in range(n)] for m in range(n)]
    DF = [[[sp.diff(F[m][nn], X[l]) - sum(Gam[r][l][m] * F[r][nn] + Gam[r][l][nn] * F[m][r] for r in range(n)) for nn in range(n)] for m in range(n)] for l in range(n)]
    DDF = [[[[sp.diff(DF[l][m][nn], X[k]) - sum(Gam[r][k][l] * DF[r][m][nn] + Gam[r][k][m] * DF[l][r][nn] + Gam[r][k][nn] * DF[l][m][r] for r in range(n)) for nn in range(n)]
             for m in range(n)] for l in range(n)] for k in range(n)]
    return F, DF, DDF


def structures(geo, ten):
    a, g, gi, Gam, RM, Ric, Rs = geo
    F, DF, DDF = ten
    n = 4
    R = range(n)
    S1 = sum(gi[k] * gi[i] * gi[j] * DF[k][i][j] ** 2 for k in R for i in R for j in R)
    V = [sum(gi[j] * DF[j][i][j] for j in R) for i in R]
    S2 = sum(gi[i] * V[i] ** 2 for i in R)
    S3 = sum(gi[i] * gi[j] * F[i][j] * sum(gi[k] * DDF[k][k][i][j] for k in R) for i in R for j in R)
    Fup = [[gi[i] * gi[j] * F[i][j] for j in R] for i in R]
    S4 = -sum(RM[i][j][k][l] * Fup[i][j] * Fup[k][l] for i in R for j in R for k in R for l in R)         # R^V = -R^MTW
    S5 = sum(Ric[j][k] * (gi[j] * gi[nn] * F[j][nn]) * (gi[k] * F[k][nn]) for j in R for k in R for nn in R)
    S6 = Rs * sum(gi[i] * gi[j] * F[i][j] ** 2 for i in R for j in R)
    F2 = sum(gi[i] * gi[j] * F[i][j] ** 2 for i in R for j in R)
    return dict(S1=S1, S2=S2, S3=S3, S4=S4, S5=S5, S6=S6, F2=F2, V=V)


def current_from_L(Lag, geo):
    """Euler-Lagrange variation of Int d^4x Lag with respect to the homogeneous A_z = f(tau); returns the physical current J^{z-hat}(tau) (with E-substitution f = -E/tau)"""
    a = geo[0]
    eq = euler_equations(Lag, [f(tau)], [tau])[0].lhs
    J_coord = eq / a ** 4                                        # J^z = (1/sqrt(-g)) delta S/delta A_z
    Jphys = J_coord * a                                          # tetrad component
    Jphys = Jphys.subs(f(tau), -Esym / tau).doit()
    return sp.simplify(Jphys)


def d1_lichnerowicz():
    print("\nD1. Lichnerowicz with the explicit spin connection of the dS tetrad")
    t, x, y, z = X
    a = -1 / t
    g = sp.diag(-a ** 2, a ** 2, a ** 2, a ** 2)
    gi = [1 / g[i, i] for i in range(4)]
    Gam = [[[sp.simplify(gi[l] * (sp.diff(g[l, m], X[nn]) + sp.diff(g[l, nn], X[m]) - sp.diff(g[m, nn], X[l])) / 2) for nn in range(4)] for m in range(4)] for l in range(4)]
    eta = sp.diag(-1, 1, 1, 1)
    e_up = sp.eye(4) / a
    e_dn = sp.eye(4) * a
    gam = F1.gamma_matrices()
    om = [[[sp.simplify(sum(e_dn[A, nu] * (sp.diff(e_up[B, nu], X[mu]) + sum(Gam[nu][mu][lam] * e_up[B, lam] for lam in range(4))) for nu in range(4)))
            for B in range(4)] for A in range(4)] for mu in range(4)]
    def Sigma(mu, c):
        S = sp.zeros(4)
        for A in range(4):
            for B in range(4):
                S += sp.Rational(1, 4) * c * eta[A, A] * om[mu][A][B] * gam[A] * gam[B]
        return S
    # sign c fixed by nabla gamma = 0 (as in s2_1 W0)
    cs = []
    for c in (+1, -1):
        ok = True
        for mu in range(4):
            Sg = Sigma(mu, c)
            for nu in range(4):
                gn = sum((e_up[A, nu] * gam[A] for A in range(4)), sp.zeros(4))
                res = sp.diff(gn, X[mu]) + sum((Gam[nu][mu][lam] * sum((e_up[A, lam] * gam[A] for A in range(4)), sp.zeros(4)) for lam in range(4)), sp.zeros(4)) + Sg * gn - gn * Sg
                if sp.simplify(res) != sp.zeros(4):
                    ok = False
        cs.append(ok)
    c = +1 if cs[0] else -1
    Sg = [Sigma(mu, c) for mu in range(4)]
    Om = [[sp.simplify(sp.diff(Sg[nu], X[mu]) - sp.diff(Sg[mu], X[nu]) + Sg[mu] * Sg[nu] - Sg[nu] * Sg[mu]) for nu in range(4)] for mu in range(4)]
    gmu = [sum((e_up[A, mu] * gam[A] for A in range(4)), sp.zeros(4)) for mu in range(4)]
    lhs = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            lhs += sp.Rational(1, 2) * gmu[mu] * gmu[nu] * Om[mu][nu]
    res = sp.simplify(lhs + 12 * sp.eye(4) / 4)
    check("D1 (1/2) gamma^mu gamma^nu [nabla_mu, nabla_nu] = -R/4 with R = +12 H^2 (explicit spin connection, sign found by nabla gamma = 0)", res == sp.zeros(4), f"(sign c = {c})")


def uehling_scalar_gate():
    rng = np.random.default_rng(7)
    cs = scalar_coefs(0)
    worst = 0.0
    mp.mp.dps = 30
    slope = float(F1.feynman_pi(mp.mpf(10) ** -8, "s") / mp.mpf(10) ** -8)              # units alpha/pi per Q2/m2 (expected -1/120)
    for _ in range(10):
        k = rng.normal(size=4)
        a_ = rng.normal(size=4) + 1j * rng.normal(size=4)
        fm = np.outer(k, a_) - np.outer(a_, k)
        ff = np.sum(fm * np.conj(fm)).real
        k2 = k @ k
        S1 = 0.5 * k2 * ff
        S2 = 0.5 * np.sum(np.abs(fm @ k) ** 2)
        S3 = -0.5 * k2 * ff
        comb = float(cs[0]) * S1 + float(cs[1]) * S2 + float(cs[2]) * S3
        L_gil = -comb / (16 * math.pi ** 2 * 360)                                         # scalar: Gamma_E = -(1/(16 pi^2 m^2)) tr a_3, q = 1, m = 1
        L_ueh = 0.25 * (1 / (4 * math.pi ** 2)) * slope * k2 * 0.5 * ff
        worst = max(worst, abs(L_gil / L_ueh - 1))
    check("D6a flat-space scalar gate: (-8 S1 - T2 S2 - 12 S3) reproduces the scalar Uehling coefficient (Feynman-integral slope -1/120) on 10 plane waves (1e-6)", worst < 1e-6, f"(worst {worst:.2e}; slope {slope:.8f})")


def main():
    print("=" * 118)
    print(f"S2-4 heavy-mass current in dS_4 from the derivative expansion -- mode: {'MUTATE CONTROL (coefficient of Om_ij;j Om_ik;k: 2 -> 1)' if MUTATE else 'REAL RUN'}")
    print("=" * 118)
    geo = build_geometry()
    d0_geometry(geo)
    ten = field_tensors(geo)
    S = structures(geo, ten)
    a = geo[0]
    # maximally symmetric identities for the curvature structures (checks the code, not the physics)
    ok = (sp.simplify(S["S4"] + 2 * S["F2"]) == 0) and (sp.simplify(S["S5"] - 3 * S["F2"]) == 0) and (sp.simplify(S["S6"] - 12 * S["F2"]) == 0)
    check("D0b curvature structures in dS: S4 = -2 F^2, S5 = 3 F^2, S6 = 12 F^2 (H = 1)", ok)
    Vz = sp.simplify(S["V"][3].subs(f(tau), -Esym / tau).doit())
    Vphys = sp.simplify(Vz / a)
    print(f"     nabla^j F_zj (coordinate {Vz}); orthonormal-frame magnitude at tau = -1: {sp.simplify(Vphys.subs(tau, -1))}  (Q1: |nabla_nu F^(nu z)| = 2 E H)")
    check("D0c |nabla^j F_zj| = 2 E at tau = -1 (H = 1)", abs(sp.simplify(Vphys.subs(tau, -1))) == 2 * Esym)
    d1_lichnerowicz()
    uehling_scalar_gate()

    def sigma_M2(coefs, prefactor):
        """returns the exact coefficient of sigma_HFY M^2 (units of E-free number) and the tau dependence check"""
        Ls = sum(c * S[k] for c, k in zip(coefs, ("S1", "S2", "S3", "S4", "S5", "S6")))
        L_E = prefactor * Ls / 360                       # per q^2 /m^2
        L_M = -L_E
        Lag = a ** 4 * L_M                               # sqrt(-g) L
        Jphys = current_from_L(Lag, geo)
        return Jphys

    print("\nD2. Dirac fermion: current from the recalled a_3 (F^2 terms) in de Sitter")
    cd = dirac_coefs()
    print(f"     coefficients (28, -8, 72, -36, 16, -20 for the recalled formula): {cd}")
    Jf = sigma_M2(cd, sp.Rational(1, 32) / sp.pi ** 2)
    print(f"     J^(z-hat)(tau) per (q^2/m^2) = {Jf}")
    tf = sp.simplify(Jf)
    Jf1 = sp.simplify(tf.subs(tau, -1))
    cf = sp.simplify(-Jf1 / Esym)                          # J_par/(q^2 E) * m^2  (J_par = -J^z-hat)
    print(f"     sigma_HFY M^2 (Dirac, derived) = {cf} = {float(cf):.10e};  -1/(36 pi^2) = {-1/(36*math.pi**2):.10e}")
    check("D2 derived Dirac coefficient of sigma_HFY M^2 equals -1/(36 pi^2) exactly (sympy)", sp.simplify(cf + 1 / (36 * sp.pi ** 2)) == 0, f"(ratio to -1/(36 pi^2): {float(cf * (-36 * math.pi ** 2)):.12f})")
    tdep = sp.simplify(sp.diff(tf, tau))
    check("D5 dS invariance: the physical current is tau-independent (dJ/dtau = 0)", tdep == 0, f"(dJ/dtau = {tdep})")

    print("\nD3. Q1 closed form (weak field, HFY 4.3, imported read-only): M^2 sigma_HFY as M -> infinity")
    Ms = [10, 20, 40, 80]
    vals = []
    for M in Ms:
        v = hfy_weak(M) * M ** 2
        vals.append(v)
        print(f"     M = {M:3d}   M^2 sigma_HFY = {v:.12e}   (M^2 sigma_HFY)/( -1/(36 pi^2) ) = {v * (-36 * math.pi ** 2):.10f}")
    A = np.array([[1.0, 1.0 / M ** 2, 1.0 / M ** 4] for M in Ms[1:]])
    c0, c1, c2 = np.linalg.solve(A, np.array(vals[1:]))
    print(f"     Richardson (c0 + c1/M^2 + c2/M^4 through M = 20, 40, 80): c0 = {c0:.14e}, c1 = {c1:.6e}")
    rel = abs(c0 / float(cf) - 1)
    print(f"     derived (D2) {float(cf):.14e};  |c0/derived - 1| = {rel:.3e}")
    check("D3 derived coefficient = Q1's heavy-mass limit within 1e-6 relative", rel < 1e-6, f"(rel {rel:.2e})")
    smax_ratio = -80 * (4 * 80 ** 2 + 1) / (9 * math.pi * math.sinh(2 * math.pi * 80)) if 2 * math.pi * 80 < 700 else 0.0
    print(f"     (informational) Hayashinaka-Xue maximal subtraction predicts an exponentially small sigma at M = 80 ({smax_ratio:.1e}), i.e. coefficient 0: contradicted by D2 if D2 holds.")

    print("\nD6. pipeline validation on the heavy charged scalar (E = -xi R): sigma_s M^2 = (7/18 - 2 xi)/(4 pi^2)")
    ok6 = True
    for xi in (sp.Integer(0), sp.Rational(1, 6), sp.Rational(1, 12)):
        Js = sigma_M2(scalar_coefs(xi), -sp.Rational(1, 16) / sp.pi ** 2)
        cs_ = sp.simplify(-Js.subs(tau, -1) / Esym)
        target = (sp.Rational(7, 18) - 2 * xi) / (4 * sp.pi ** 2)
        okx = sp.simplify(cs_ - target) == 0
        ok6 &= okx
        if xi == 0:
            INFO["D6_xi0_ok"] = okx
        print(f"     xi = {xi}: derived {cs_} = {float(cs_):.10e};  target {target} = {float(target):.10e}   {'equal' if okx else 'DIFFERENT'}")
    check("D6 the same pipeline reproduces the scalar heavy-mass law (7/18 - 2 xi)/(4 pi^2) exactly for xi = 0, 1/6, 1/12", ok6)

    print("\nD4. (informational) Drummond-Hathrell curvature-coupled action, recalled coefficients (units alpha/pi): a = -5/720, b = 26/720, c = -2/720, d = -24/720")
    for sR in (+1, -1):
        a_, b_, c_, d_ = (sp.Rational(-5, 720), sp.Rational(26, 720), sp.Rational(-2, 720), sp.Rational(-24, 720))
        LDH = (1 / (4 * sp.pi ** 2)) * (-sR * a_ * S["S6"] - sR * b_ * S["S5"] + sR * c_ * S["S4"] - d_ * S["S2"])
        Lag = a ** 4 * LDH
        Jd = current_from_L(Lag, geo)
        cdh = sp.simplify(-Jd.subs(tau, -1) / Esym)
        print(f"     curvature-sign convention s_R = {sR:+d}: sigma_HFY M^2 (DH) = {cdh} = {float(cdh):.10e}   (Gilkey-based {float(cf):.10e}; ratio {float(cdh / cf):.6f})")
        INFO[f"DH_{sR}"] = sp.simplify(cdh - cf) == 0
    print("     (conventions of the recalled DH paper are not known to me: the two signs are the two possible curvature conventions; a match under either is reported, none is required)")

    print("=" * 118)
    n_ok = sum(CHECKS.values())
    print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
    dh = [k for k, v in INFO.items() if k.startswith("DH_") and v]
    print(f"D4 informational: Drummond-Hathrell matches the Gilkey-based dS current under: {dh if dh else 'neither convention'}")
    print("Scope: heavy Dirac field, linear in E, leading 1/m^2 term of the derivative expansion, on-shell scheme (no 1/m^0 term: the flat vacuum polarization vanishes at q^2 = 0).")
    if MUTATE:
        if (not CHECKS["D2"]) and (not CHECKS["D3"]) and (not CHECKS["D6"]):
            print("\nMUTATE CONTROL: the coefficient 2 -> 1 was used; D2, D3 and D6 FAILED as required -- the control works")
            sys.exit(1)
        print("\nMUTATE CONTROL: a targeted check did NOT fail -- the control has no power")
        sys.exit(3)
    sys.exit(0 if n_ok == len(CHECKS) else 2)


if __name__ == "__main__":
    main()
