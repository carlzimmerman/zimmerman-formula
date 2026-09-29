#!/usr/bin/env python3
"""S2-3 -- ROUTE C, part 1: gates on the RECALLED heat-kernel coefficient a_3 (Gilkey; Vassilevich's review, eq. for a_6) used to obtain the heavy-mass expansion of the dS_4 Dirac current.
Independent of lane Q1 (no mode sum, no adiabatic subtraction, no published closed form).  A recalled coefficient that fails a gate is NOT adjusted: the route is then UNDECIDABLE.

Pre-registered in S2_PREREGISTRATION.md (before this script was run).  Euclidean formulas, orthonormal frame, F = field strength of the U(1) connection D = nabla + i q A, so [D_i, D_j] contains i q F_ij.
Operator -D-slash^2 + m^2 = -(nabla^2 + E) + m^2, E = -R/4 + (i q/2) gamma^i gamma^j F_ij, Omega_ij = i q F_ij + (1/4) R^M_ijab gamma^a gamma^b (R^M: MTW sign, sphere positive),
Vassilevich sign for the Riemann tensor in the formula: R^V_ijkl = -R^M_ijkl, R_jk = R^M_ijik.  F-dependent, F-quadratic part of tr a_3 (recalled):
 (1/360) tr[ 8 Om_ij;k Om_ij;k + 2 Om_ij;j Om_ik;k + 12 Om_ij;kk Om_ij - 12 Om_ij Om_jk Om_ki - 6 R^V_ijkl Om_ij Om_kl - 4 R_jk Om_jn Om_kn + 5 R Om_kn Om_kn
            + 60 E E;ii + 30 E;i E;i + 60 E^3 + 30 E Om_ij Om_ij + 30 R E E + (terms linear in E or pure gravity, whose F^2 part vanishes) ].
Gates:  H0 explicit 4x4 gamma-matrix traces = reduced tensor formula on 20 random draws;  H1 flat-space derivative terms = the Uehling coefficient obtained from the small-Q^2 slope of the Feynman integral;
        H2 Lichnerowicz sign identity;  H3 exact spectral test of the a_2 F^2 coefficient on S^2 x S^2 with monopole fluxes;  H4 the same for the a_3 F^2 R terms.

Run:     python3 s2_3_heat_kernel_gates.py            (real run; exit 0 iff every gate passes)
         python3 s2_3_heat_kernel_gates.py --mutate   (control: the recalled coefficient 5 of R tr(Om_kn Om_kn) is replaced by 4; H4 must FAIL;
                                                       exit 1 if it fails = the control works, exit 3 if H4 passes = the control has no power)
Only the literal argument --mutate triggers the control.  Set PYTHONDONTWRITEBYTECODE=1.
"""
import sys
sys.dont_write_bytecode = True
import os
import itertools
import math
import numpy as np
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s2_1_massless_fermion as F1          # vacuum-polarization Feynman integral (H1)

MUTATE = "--mutate" in sys.argv
CHECKS = {}
COEF = dict(T1=8, T2=2, T3=12, Om3=-12, Riem=-6, Ric=-4, ROO=(4 if MUTATE else 5), EEii=60, EiEi=30, E3=60, EOO=30, EER=30)


def check(tag, ok, detail=""):
    CHECKS[tag.split()[0]] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def coef_reduced(C=COEF):
    """coefficients (per q^2, before the overall 1/360) of S1..S6 in the reduced tensor form, derived from the recalled coefficients C (see the docstring / preregistration)."""
    return dict(
        S1=C["T1"] * (-4) + C["EiEi"] * 2,
        S2=C["T2"] * (-4),
        S3=C["T3"] * (-4) + C["EEii"] * 2,
        S4=C["Riem"] * (-4) * (+1) * (-1) * (-1) + C["EOO"] * (-2),      # -6 R^V Om Om -> +24 S4 ;  30 tr(E 2 Om_F Om_s) -> -60 S4
        S5=C["Ric"] * (-4),
        S6=C["ROO"] * (-4) + C["E3"] * sp.Rational(-3, 2) + C["EOO"] * 1 + C["EER"] * 2,
    )


# ------------------------------------------------------------------------------------ tensor contractions with plain loops (work for Rational and float)
def contractions(F, DF, DDF, RM):
    n = 4
    R = range(n)
    Ric = [[sum(RM[i][j][i][k] for i in R) for k in R] for j in R]
    Rs = sum(Ric[j][j] for j in R)
    RV = lambda i, j, k, l: -RM[i][j][k][l]
    S1 = sum(DF[k][i][j] * DF[k][i][j] for k in R for i in R for j in R)
    V = [sum(DF[j][i][j] for j in R) for i in R]
    S2 = sum(v * v for v in V)
    S3 = sum(DDF[k][k][i][j] * F[i][j] for k in R for i in R for j in R)
    S4 = sum(RV(i, j, k, l) * F[i][j] * F[k][l] for i in R for j in R for k in R for l in R)
    S5 = sum(Ric[j][k] * F[j][n_] * F[k][n_] for j in R for k in R for n_ in R)
    S6 = Rs * sum(F[i][j] * F[i][j] for i in R for j in R)
    return dict(S1=S1, S2=S2, S3=S3, S4=S4, S5=S5, S6=S6)


def reduced_a3F(F, DF, DDF, RM, C=COEF):
    S = contractions(F, DF, DDF, RM)
    c = coef_reduced(C)
    return sum(c[k] * S[k] for k in S) / 360            # per q^2


# ------------------------------------------------------------------------------------ explicit gamma-matrix evaluation
def euclid_gammas():
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    return [np.kron(sx, sx), np.kron(sx, sy), np.kron(sx, sz), np.kron(sy, I2)]


def explicit_a3(t, q, F, DF, DDF, RM, G, C=COEF):
    """tr a_3 (recalled formula, the terms with F / curvature that can produce F^2, F^3 or gravity-only pieces), with F -> t F, evaluated with explicit 4x4 matrices."""
    n = 4
    R = range(n)
    I4 = np.eye(4, dtype=complex)
    Ric = np.array([[sum(RM[i, j, i, k] for i in R) for k in R] for j in R])
    Rs = np.trace(Ric)
    RV = -RM
    def spin(i, j):
        return sum(0.25 * RM[i, j, a, b] * G[a] @ G[b] for a in R for b in R)
    Om = [[1j * q * t * F[i, j] * I4 + spin(i, j) for j in R] for i in R]
    Omk = [[[1j * q * t * DF[k, i, j] * I4 for j in R] for i in R] for k in R]              # Omega_ij;k = Omk[k][i][j]
    Omkk = [[1j * q * t * sum(DDF[k, k, i, j] for k in R) * I4 for j in R] for i in R]
    E = -Rs / 4 * I4 + 0.5j * q * t * sum(F[i, j] * G[i] @ G[j] for i in R for j in R)
    Ek = [0.5j * q * t * sum(DF[k, i, j] * G[i] @ G[j] for i in R for j in R) for k in R]
    Ekk = 0.5j * q * t * sum(DDF[k, k, i, j] * G[i] @ G[j] for k in R for i in R for j in R)
    tr = np.trace
    tot = 0
    tot += C["T1"] * sum(tr(Omk[k][i][j] @ Omk[k][i][j]) for k in R for i in R for j in R)
    tot += C["T2"] * sum(tr(sum((Omk[j][i][j] for j in R), np.zeros((4, 4), dtype=complex)) @ sum((Omk[k][i][k] for k in R), np.zeros((4, 4), dtype=complex))) for i in R)
    tot += C["T3"] * sum(tr(Omkk[i][j] @ Om[i][j]) for i in R for j in R)
    tot += C["Om3"] * sum(tr(Om[i][j] @ Om[j][k] @ Om[k][i]) for i in R for j in R for k in R)
    tot += C["Riem"] * sum(RV[i, j, k, l] * tr(Om[i][j] @ Om[k][l]) for i in R for j in R for k in R for l in R)
    tot += C["Ric"] * sum(Ric[j, k] * tr(Om[j][nn] @ Om[k][nn]) for j in R for k in R for nn in R)
    tot += C["ROO"] * Rs * sum(tr(Om[k][nn] @ Om[k][nn]) for k in R for nn in R)
    tot += C["EEii"] * tr(E @ Ekk)
    tot += C["EiEi"] * sum(tr(Ek[i] @ Ek[i]) for i in R)
    tot += C["E3"] * tr(E @ E @ E)
    tot += C["EOO"] * sum(tr(E @ Om[i][j] @ Om[i][j]) for i in R for j in R)
    tot += C["EER"] * Rs * tr(E @ E)
    return tot / 360


def random_curvature(rng):
    """algebraic curvature tensor (MTW sign, all Riemann symmetries) as a sum of Kulkarni-Nomizu products of random symmetric matrices"""
    n = 4
    RM = np.zeros((n, n, n, n))
    for _ in range(3):
        h = rng.normal(size=(n, n)); h = h + h.T
        g = rng.normal(size=(n, n)); g = g + g.T
        RM += (np.einsum("ik,jl->ijkl", h, g) + np.einsum("ik,jl->ijkl", g, h) - np.einsum("il,jk->ijkl", h, g) - np.einsum("il,jk->ijkl", g, h))
    return RM


def h0_reduction(rng):
    print("\nH0. explicit 4x4 gamma traces versus the reduced tensor formula (t^2 coefficient of the recalled tr a_3, 20 random draws)")
    G = euclid_gammas()
    ok = all(np.allclose(G[a] @ G[b] + G[b] @ G[a], 2 * (a == b) * np.eye(4)) for a in range(4) for b in range(4))
    check("H0a Euclidean gamma matrices satisfy {g_a, g_b} = 2 delta_ab", ok)
    worst = 0.0
    for trial in range(20):
        A = rng.normal(size=(4, 4)); F = A - A.T
        Bt = rng.normal(size=(4, 4, 4)); DF = Bt - Bt.transpose(0, 2, 1)
        Ct = rng.normal(size=(4, 4, 4, 4)); DDF = Ct - Ct.transpose(0, 1, 3, 2)
        RM = random_curvature(rng)
        q = 1.0
        ts = np.array([-2.0, -1.0, 1.0, 2.0])
        vals = np.array([explicit_a3(t, q, F, DF, DDF, RM, G) for t in ts])
        V = np.vander(ts, 4, increasing=True)                    # columns t^0..t^3
        coeffs = np.linalg.solve(V, vals)
        t2 = coeffs[2]
        red = float(reduced_a3F(F.tolist(), DF.tolist(), DDF.tolist(), RM.tolist()))
        worst = max(worst, abs(t2 - red) / max(1e-12, abs(red)), abs(coeffs[1]), abs(coeffs[3]) / max(1.0, abs(red)))
        if trial == 0:
            print(f"     draw 0: t^2 coefficient explicit {t2.real:+.10f}{t2.imag:+.1e}j   reduced {red:+.10f};  t^1 coeff {abs(coeffs[1]):.1e}, t^3 coeff {abs(coeffs[3]):.1e}")
    check("H0b reduced formula = explicit traces (relative 1e-9); the t^1 and t^3 parts vanish (Furry: no F-linear, no F^3 trace terms)", worst < 1e-9, f"(worst {worst:.2e})")
    return coef_reduced()


def h1_flat(rng):
    print("\nH1. flat space: derivative terms of the recalled a_3 reduce to -(96/360) q^2 (d_j F_ij)^2 and reproduce the Uehling coefficient from the Feynman integral")
    cr = coef_reduced()
    worst = 0.0
    for _ in range(10):
        k = rng.normal(size=4)
        a = rng.normal(size=4) + 1j * rng.normal(size=4)
        f = np.outer(k, a) - np.outer(a, k)                           # F_ij = d_i A_j - d_j A_i for A = Re(a e^{ikx}); Bianchi automatically
        ff = np.sum(f * np.conj(f)).real
        k2 = k @ k
        S1 = 0.5 * k2 * ff
        v = f @ k                                                    # k_j f_ij
        S2 = 0.5 * np.sum(np.abs(v) ** 2)
        S3 = -0.5 * k2 * ff
        comb = cr["S1"] * S1 + cr["S2"] * S2 + cr["S3"] * S3
        # (a) reduces to -96 S2
        red_ok = abs(comb - (-96) * S2)
        # (b) Uehling: L_E(a_3) = (1/(32 pi^2)) (1/360) q^2 comb (m = 1)   vs   (1/4) < F Pi_hat F >,  Pi_hat = (alpha/pi) slope k^2,  alpha = q^2/(4 pi),  <F F> = ff/2
        mp.mp.dps = 30
        slope = F1.feynman_pi(mp.mpf(10) ** -8) / mp.mpf(10) ** -8            # units alpha/pi, per Q^2/m^2
        L_gil = comb / (32 * math.pi ** 2 * 360)
        L_ueh = 0.25 * (1 / (4 * math.pi ** 2)) * float(slope) * k2 * 0.5 * ff
        worst = max(worst, red_ok / abs(comb), abs(L_gil / L_ueh - 1))
    check("H1 derivative combination = -96 (d_j F_ij)^2 exactly and L_E(a_3) = L_E(Uehling from the Feynman integral slope -1/15) on 10 random plane waves (1e-6)", worst < 1e-6, f"(worst {worst:.2e}; S1..S3 coefficients {cr['S1']}, {cr['S2']}, {cr['S3']})")


def lich_lhs(G, RM):
    """(1/2) gamma^i gamma^j Omega^s_ij with Omega^s_ij = (1/4) R^M_ijab gamma^a gamma^b  (explicit matrix products; Amendment 4: the first run used elementwise * by an operator-precedence slip)"""
    out = np.zeros((4, 4), dtype=complex)
    for i, j, a, b in itertools.product(range(4), repeat=4):
        out += 0.5 * 0.25 * RM[i, j, a, b] * ((G[i] @ G[j]) @ (G[a] @ G[b]))
    return out


def h2_lichnerowicz(rng):
    print("\nH2. Lichnerowicz: with Omega^s_ij = +(1/4) R^M_ijab gamma^a gamma^b,  (1/2) gamma^i gamma^j Omega^s_ij = -R/4  (R = R^M_ijij > 0 for a sphere)")
    G = euclid_gammas()
    worst = 0.0
    for _ in range(5):
        RM = random_curvature(rng)
        Rs = sum(RM[i, j, i, j] for i in range(4) for j in range(4))
        lhs = lich_lhs(G, RM)
        worst = max(worst, np.max(np.abs(lhs + Rs / 4 * np.eye(4))))
    K = 1.0
    RM = np.zeros((4, 4, 4, 4))
    for i, j, a, b in itertools.product(range(4), repeat=4):
        RM[i, j, a, b] = K * ((i == a) * (j == b) - (i == b) * (j == a))
    Rs = sum(RM[i, j, i, j] for i in range(4) for j in range(4))
    lhs = lich_lhs(G, RM)
    worst = max(worst, np.max(np.abs(lhs + Rs / 4 * np.eye(4))))
    check("H2 (1/2) gamma gamma Omega^s = -R/4 for random algebraic curvature tensors and for the unit S^4 (R = 12 > 0)", worst < 1e-12 and abs(Rs - 12) < 1e-12, f"(worst {worst:.1e}, R(S^4) = {Rs})")


# ------------------------------------------------------------------------------------ spectral test on S^2 x S^2
_S, _K = sp.symbols("s k")


def T_series(n, order=4):
    """Tr e^{s D-slash^2} on the unit S^2 with monopole flux n (>= 0): spectrum k(k+n), multiplicity 2(n+2k) (k >= 1), n zero modes; Euler-Maclaurin, exact in s to O(s^order)."""
    nn = sp.Integer(n)
    g = (nn + 2 * _K) * sp.exp(-_S * _K * (_K + nn))
    tot = 2 / _S
    for m in range(1, order + 3):
        d = sp.expand(sp.diff(g, _K, 2 * m - 1).subs(_K, 0))
        tot += -2 * sp.bernoulli(2 * m) / sp.factorial(2 * m) * d
    tot = sp.expand(tot)
    return sum(tot.coeff(_S, p) * _S ** p for p in range(-1, order + 1))


def spectral_side(n1, n2, r1sq, r2sq, order=2):
    T1 = T_series(n1).subs(_S, _S / r1sq)
    T2 = T_series(n2).subs(_S, _S / r2sq)
    T10 = T_series(0).subs(_S, _S / r1sq)
    T20 = T_series(0).subs(_S, _S / r2sq)
    D = sp.expand(T1 * T2 - T10 * T20)
    return [sp.nsimplify(D.coeff(_S, p) / (r1sq * r2sq)) for p in (0, 1)]         # tr a_2^F, tr a_3^F


def geometry_side(n1, n2, r1sq, r2sq):
    K1, K2 = 1 / sp.Rational(r1sq), 1 / sp.Rational(r2sq)
    b1, b2 = sp.Rational(n1) / (2 * sp.Rational(r1sq)), sp.Rational(n2) / (2 * sp.Rational(r2sq))          # b_i = q B_i = n_i/(2 r_i^2)
    RM = [[[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for (lo, K) in ((0, K1), (2, K2)):
        for i, j, a, b in itertools.product(range(2), repeat=4):
            RM[lo + i][lo + j][lo + a][lo + b] = K * ((i == a) * (j == b) - (i == b) * (j == a))
    F = [[sp.Integer(0)] * 4 for _ in range(4)]
    F[0][1], F[1][0], F[2][3], F[3][2] = b1, -b1, b2, -b2
    zero3 = [[[sp.Integer(0)] * 4 for _ in range(4)] for _ in range(4)]
    zero4 = [zero3 for _ in range(4)]
    a3 = reduced_a3F(F, zero3, zero4, RM)
    a2 = sp.Rational(1, 360) * (180 * 2 * sum(F[i][j] ** 2 for i in range(4) for j in range(4)) + 30 * (-4) * sum(F[i][j] ** 2 for i in range(4) for j in range(4)))
    return sp.nsimplify(a2), sp.nsimplify(a3)


def h3_h4_spectral():
    print("\nH3/H4. exact spectrum of the Dirac operator on S^2(r_1) x S^2(r_2) with monopole fluxes (n_1, n_2): flux-dependent part of the heat trace vs the recalled a_2, a_3")
    print("     (the S^2 spectrum is recalled; its a_0, a_1, a_2 are also checked below against the geometric values)")
    T0 = T_series(0)
    check("H3a unit S^2, n = 0: Tr e^{sD^2} = 2/s - 1/3 + ... (tr a_1 = 2(R/6 - R/4) = -1/3 with R = 2)", sp.simplify(T0.coeff(_S, 0) + sp.Rational(1, 3)) == 0, f"(s^0 coefficient {T0.coeff(_S, 0)})")
    configs = [(1, 0, 1, 1), (0, 2, 1, 2), (1, 3, 1, 2), (3, 2, 3, 1)]
    ok3, ok4 = True, True
    for (n1, n2, r1, r2) in configs:
        sa2, sa3 = spectral_side(n1, n2, r1, r2)
        ga2, ga3 = geometry_side(n1, n2, r1, r2)
        e2 = sp.simplify(sa2 - ga2); e3 = sp.simplify(sa3 - ga3)
        ok3 &= (e2 == 0); ok4 &= (e3 == 0)
        print(f"     (n1, n2; r1^2, r2^2) = ({n1}, {n2}; {r1}, {r2}):  tr a_2^F spectral {sa2}  geometry {ga2}   |  tr a_3^F spectral {sa3}  geometry {ga3}")
    check("H3 the recalled a_2 F^2 coefficient equals the exact spectral value (exact rational agreement, 4 configurations)", ok3)
    check("H4 the recalled a_3 F^2 R coefficients equal the exact spectral values (exact rational agreement, 4 configurations; mixed R_(i) F_(j)^2 and same-sphere structures)", ok4)


def main():
    print("=" * 118)
    print(f"S2-3 heat-kernel gates for the heavy-mass route -- mode: {'MUTATE CONTROL (coefficient of R tr Om Om: 5 -> 4)' if MUTATE else 'REAL RUN'}")
    print("=" * 118)
    rng = np.random.default_rng(20260929)
    cr = h0_reduction(rng)
    print(f"     reduced coefficients per q^2/360: {cr}")
    h1_flat(rng)
    h2_lichnerowicz(rng)
    h3_h4_spectral()
    print("=" * 118)
    n_ok = sum(CHECKS.values())
    print(f"CHECKS: {n_ok}/{len(CHECKS)} passed")
    print("Scope: only the F-quadratic part of the RECALLED a_3; derivative terms are gated in flat space only (the curved-space reordering of the derivative terms is NOT tested here).")
    if MUTATE:
        if not CHECKS["H4"]:
            print("\nMUTATE CONTROL: the recalled coefficient 5 -> 4 was used; H4 FAILED as required -- the control works")
            sys.exit(1)
        print("\nMUTATE CONTROL: H4 did NOT fail -- the control has no power")
        sys.exit(3)
    sys.exit(0 if n_ok == len(CHECKS) else 2)


if __name__ == "__main__":
    main()
