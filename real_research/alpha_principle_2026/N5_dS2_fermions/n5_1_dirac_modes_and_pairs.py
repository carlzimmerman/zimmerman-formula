#!/usr/bin/env python3
"""N5-1 -- charged Dirac fermion in dS_2 (planar patch): derivation of the mode equations, exact Whittaker modes,
independent ODE validation (incl. k<0), and the pair-production factor by out-mode projection.

Pre-registered in N5_PREREGISTRATION.md (written before this script was run).  Units hbar = c = H = 1, a = -1/tau.
Variables: lambda = eE/H^2 (eA_x = lambda/tau, p = k + lambda/tau), mu = m/H, rho_f = sqrt(mu^2 + lambda^2).
Rescaled spinor Psi = sqrt(a) psi:   i Psi_1' = -p Psi_1 + m a Psi_2,   i Psi_2' = +p Psi_2 + m a Psi_1,   |Psi_1|^2+|Psi_2|^2 = 1.

Checks:  D1 sympy derivation (tetrad, spin connection fixed by covariance of gamma^mu)  M1 Whittaker modes solve the system
         (constant c found from the system, both rows checked)  M1b |c| = 1/mu  M2 norm conserved
         M3 independent ODE integration from the far past (k>0 and k<0) = Whittaker construction   P1 |beta_k|^2 vs Stahl-Strobel-Xue eq.(73)
         P2 massless limit n_k -> theta(k lambda).

Run:     python3 n5_1_dirac_modes_and_pairs.py             (real run; exit 0 iff every check passes)
         python3 n5_1_dirac_modes_and_pairs.py --mutate    (control: the SCALAR index rho_s = sqrt(mu^2+lambda^2-1/4) replaces rho_f in the mode
                                                            construction -- the '1/4' error; M1 must FAIL; the control exits 1 when M1 fails as required)
"""
import sys
import math
import numpy as np
import mpmath as mp
import sympy as sp
from scipy.integrate import solve_ivp

mp.mp.dps = 30
MUTATE = "--mutate" in sys.argv
PI = math.pi
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# ----------------------------------------------------------------------------------------------- D1
def d1_derivation():
    print("\nD1. Dirac equation on ds^2 = a^2 (d tau^2 - dx^2): tetrad e^a_mu = a delta, spin connection fixed by  nabla_mu gamma^nu = 0")
    t, x, k, m, e = sp.symbols("tau x k m e", real=True)
    A = sp.Function("A")(t)
    a = sp.Function("a")(t)
    Psi1 = sp.Function("Psi1")(t)
    Psi2 = sp.Function("Psi2")(t)
    co = (t, x)
    g = sp.diag(a ** 2, -a ** 2)
    ginv = g.inv()
    Gam = [[[sum(ginv[n, s] * (sp.diff(g[s, mu], co[l]) + sp.diff(g[s, l], co[mu]) - sp.diff(g[mu, l], co[s])) for s in range(2)) / 2
             for l in range(2)] for mu in range(2)] for n in range(2)]          # Gam[n][mu][l] = Gamma^n_{mu l}
    g0 = sp.Matrix([[0, 1], [1, 0]])
    g1 = sp.Matrix([[0, 1], [-1, 0]])
    gcurv = [g0 / a, g1 / a]                                                      # gamma^mu = e_a^mu gamma^a
    # unknown spinor connection matrices, traceless
    Om = []
    unk = []
    for mu in range(2):
        u = sp.symbols(f"o{mu}_0:3")
        unk += list(u)
        Om.append(sp.Matrix([[u[0], u[1]], [u[2], -u[0]]]))
    eqs = []
    for mu in range(2):
        for n in range(2):
            M = sp.diff(gcurv[n], co[mu]) + sum((Gam[n][mu][l] * gcurv[l] for l in range(2)), sp.zeros(2, 2)) + Om[mu] * gcurv[n] - gcurv[n] * Om[mu]
            eqs += list(M)
    sol = sp.solve(eqs, unk, dict=True)[0]
    Om = [sp.simplify(O.subs(sol)) for O in Om]
    print("     Omega_tau =", Om[0].tolist(), "   Omega_x =", sp.simplify(Om[1]).tolist())
    psi = sp.Matrix([Psi1, Psi2]) / sp.sqrt(a)
    ikx = sp.I * k
    # [ i gamma^tau (d_tau + Om_tau) + i gamma^x (i k + Om_x + i e A_x) - m ] psi,  psi ~ e^{ikx}
    D = sp.I * gcurv[0] * (sp.diff(psi, t) + Om[0] * psi) + sp.I * gcurv[1] * (ikx * psi + Om[1] * psi + sp.I * e * A * psi) - m * psi
    flat = sp.I * g0 * sp.Matrix([sp.diff(Psi1, t), sp.diff(Psi2, t)]) + sp.I * g1 * (ikx + sp.I * e * A) * sp.Matrix([Psi1, Psi2]) - m * a * sp.Matrix([Psi1, Psi2])
    resid2 = sp.simplify(D * a - flat / sp.sqrt(a))
    ok = (resid2 == sp.zeros(2, 1))
    print("     a * D psi - a^{-1/2} * [flat Dirac operator with m -> m a on Psi] =", resid2.T.tolist())
    # flat operator components -> the first-order system
    p = k + e * A
    row1 = sp.simplify((flat[0]).subs(k, (sp.Symbol("p") - e * A)))
    row2 = sp.simplify((flat[1]).subs(k, (sp.Symbol("p") - e * A)))
    print("     flat rows (p = k + eA):  row1 =", row1, "    row2 =", row2)
    ok_rows = (sp.simplify(row1 - (sp.I * sp.diff(Psi2, t) - sp.Symbol("p") * Psi2 - m * a * Psi1)) == 0 and
               sp.simplify(row2 - (sp.I * sp.diff(Psi1, t) + sp.Symbol("p") * Psi1 - m * a * Psi2)) == 0)
    check("D1 curved Dirac operator reduces to the flat system  i Psi_1' = -p Psi_1 + m a Psi_2, i Psi_2' = p Psi_2 + m a Psi_1", ok and ok_rows)


# ----------------------------------------------------------------------------------------------- modes
def rho_index(lam, mu):
    """Whittaker second index nu: i rho_f (correct) or the scalar-type index (MUTATE)."""
    if MUTATE:
        return 1j * mp.sqrt(mp.mpf(mu) ** 2 + mp.mpf(lam) ** 2 - mp.mpf(1) / 4)
    return 1j * mp.sqrt(mp.mpf(mu) ** 2 + mp.mpf(lam) ** 2)


def w_components(k, lam, mu, tau, c=None):
    """Unnormalised (Psi_1, Psi_2) for k>0: sqrt(a) * (W_{kappa-1/2,nu}(z), c W_{kappa+1/2,nu}(z)), z = 2 i k tau, kappa = -i lambda."""
    kappa = -1j * mp.mpf(lam)
    nu = rho_index(lam, mu)
    z = 2j * mp.mpf(k) * mp.mpf(tau)
    a = -1 / mp.mpf(tau)
    s1 = mp.sqrt(a) * mp.whitw(kappa - mp.mpf(1) / 2, nu, z)
    s2 = mp.sqrt(a) * mp.whitw(kappa + mp.mpf(1) / 2, nu, z)
    return (s1, s2) if c is None else (s1, c * s2)


def find_c(k, lam, mu, tau_ref=-1.0):
    """c from row 1 of the first-order system at tau_ref:  Psi_2 = (i Psi_1' + p Psi_1)/(m a)."""
    kk, ll, mm = mp.mpf(k), mp.mpf(lam), mp.mpf(mu)
    kappa = -1j * ll
    nu = rho_index(lam, mu)

    def psi1(tt):
        return mp.sqrt(-1 / tt) * mp.whitw(kappa - mp.mpf(1) / 2, nu, 2j * kk * tt)
    tt = mp.mpf(tau_ref)
    a = -1 / tt
    p = kk + ll / tt
    psi2_target = (1j * mp.diff(psi1, tt) + p * psi1(tt)) / (mm * a)
    s2 = mp.sqrt(a) * mp.whitw(kappa + mp.mpf(1) / 2, nu, 2j * kk * tt)
    return psi2_target / s2


def system_residual(k, lam, mu, tau, c):
    kk, ll, mm = mp.mpf(k), mp.mpf(lam), mp.mpf(mu)
    kappa = -1j * ll
    nu = rho_index(lam, mu)

    def P1(tt):
        return mp.sqrt(-1 / tt) * mp.whitw(kappa - mp.mpf(1) / 2, nu, 2j * kk * tt)

    def P2(tt):
        return c * mp.sqrt(-1 / tt) * mp.whitw(kappa + mp.mpf(1) / 2, nu, 2j * kk * tt)
    tt = mp.mpf(tau)
    a = -1 / tt
    p = kk + ll / tt
    p1, p2 = P1(tt), P2(tt)
    r1 = 1j * mp.diff(P1, tt) + p * p1 - mm * a * p2
    r2 = 1j * mp.diff(P2, tt) - p * p2 - mm * a * p1
    scale = max(abs(p * p1), abs(mm * a * p2), abs(p * p2), abs(mm * a * p1), mp.mpf("1e-300"))
    return float(max(abs(r1), abs(r2)) / scale)


def f_whittaker(k, lam, mu, tau=-1.0):
    """f = |Psi_1|^2 - |Psi_2|^2 (unit-norm normalised) of the positive-frequency mode at tau; k>0 direct, k<0 via Psi_1<->Psi_2, p->-p (lambda -> -lambda, k -> |k|)."""
    if k < 0:
        return -f_whittaker(-k, -lam, mu, tau)
    c = 1j / mp.mpf(mu)
    s1, s2 = w_components(k, lam, mu, tau, c)
    A, B = abs(s1) ** 2, abs(s2) ** 2
    return float((A - B) / (A + B))


# ----------------------------------------------------------------------------------------------- ODE reference
def f_ode(k, lam, mu, tau_end=-1.0, T=4000.0):
    """Independent numerical integration of the Dirac system from tau0 = -T/|k| with the first-order adiabatic (+omega) eigenvector; returns f at tau_end."""
    tau0 = -T / abs(k)

    def pp(t):
        return k + lam / t

    def rhs(t, y):
        p = pp(t)
        M = mu * (-1.0 / t)
        return [1j * p * y[0] - 1j * M * y[1], -1j * (M * y[0] + p * y[1])]
    p0 = pp(tau0)
    M0 = mu * (-1.0 / tau0)
    om = math.hypot(p0, M0)
    if p0 >= 0:
        u = np.array([M0, om + p0], dtype=complex)
    else:
        u = np.array([om - p0, M0], dtype=complex)
    u /= np.linalg.norm(u)
    sol = solve_ivp(rhs, (tau0, tau_end), u, method="DOP853", rtol=1e-12, atol=1e-14)
    y = sol.y[:, -1]
    return float(abs(y[0]) ** 2 - abs(y[1]) ** 2), float(abs(y[0]) ** 2 + abs(y[1]) ** 2)


# ----------------------------------------------------------------------------------------------- pairs
def unit(vec):
    n = mp.sqrt(abs(vec[0]) ** 2 + abs(vec[1]) ** 2)
    return (vec[0] / n, vec[1] / n)


def out_mode(k, lam, mu, sign, tau):
    """M-Whittaker out mode: Psi_1 = sqrt(a) M_{kappa-1/2, sign*nu}(z), Psi_2 = c_s sqrt(a) M_{kappa+1/2, sign*nu}(z); c_s found from the system."""
    kk, ll, mm = mp.mpf(k), mp.mpf(lam), mp.mpf(mu)
    kappa = -1j * ll
    nu = sign * 1j * mp.sqrt(mm ** 2 + ll ** 2)

    def m1(tt):
        return mp.sqrt(-1 / tt) * mp.whitm(kappa - mp.mpf(1) / 2, nu, 2j * kk * tt)

    def m2(tt):
        return mp.sqrt(-1 / tt) * mp.whitm(kappa + mp.mpf(1) / 2, nu, 2j * kk * tt)
    tt0 = mp.mpf(-1)
    a0 = 1
    p0 = kk + ll / tt0
    c_s = ((1j * mp.diff(m1, tt0) + p0 * m1(tt0)) / (mm * a0)) / m2(tt0)
    tt = mp.mpf(tau)
    return unit((m1(tt), c_s * m2(tt))), c_s


def beta2_numeric(k, lam, mu, tau=-1.0):
    """|beta|^2 = |<out^- | in^+>|^2 (Dirac inner product, conserved), k>0."""
    c = 1j / mp.mpf(mu)
    s1, s2 = w_components(k, lam, mu, tau, c)
    inn = unit((s1, s2))
    op, _ = out_mode(k, lam, mu, +1, tau)
    om, _ = out_mode(k, lam, mu, -1, tau)
    ov = lambda u, v: mp.conj(u[0]) * v[0] + mp.conj(u[1]) * v[1]
    beta = ov(om, inn)
    alpha = ov(op, inn)
    orth = abs(ov(op, om))
    return float(abs(beta) ** 2), float(abs(alpha) ** 2), float(orth)


def n_k_paper(lam, mu, r):
    """Stahl-Strobel-Xue eq. (73): n_k = e^{-pi(rho - r lambda)} sinh(pi(rho + r lambda))/sinh(2 pi rho)  [their |mu| -> rho_f, i r kappa -> r lambda]."""
    rho = math.sqrt(mu * mu + lam * lam)
    return math.exp(-PI * (rho - r * lam)) * math.sinh(PI * (rho + r * lam)) / math.sinh(2 * PI * rho)


# ----------------------------------------------------------------------------------------------- main
print("=" * 110)
print("N5-1 Dirac fermion in dS_2 -- mode: " + ("MUTATE CONTROL (scalar index rho_s in place of rho_f)" if MUTATE else "REAL RUN"))
print("=" * 110)

if not MUTATE:
    d1_derivation()

print("\nM1/M1b. Whittaker modes vs the first-order system (c found at tau_ref = -1, both rows checked at other times)")
M1_POINTS = [(0.7, 0.3, 0.9, -0.6), (1.3, 0.6, 0.6, -1.7), (2.1, -0.4, 0.5, -0.4), (0.4, 1.2, 0.3, -2.2), (3.0, 0.1, 1.5, -0.5), (0.9, 0.8, 0.05, -1.1)]
worst = 0.0
worst_c = 0.0
print("     k     lambda   mu     tau     residual      |c|*mu - 1")
for k, lam, mu, tau in M1_POINTS:
    c = find_c(k, lam, mu)
    r = system_residual(k, lam, mu, tau, c)
    dc = float(abs(abs(c) * mu - 1))
    worst = max(worst, r)
    worst_c = max(worst_c, dc)
    print(f"     {k:4.1f}  {lam:+5.2f}  {mu:5.2f}  {tau:+5.2f}   {r:.2e}     {dc:.2e}   (c = {complex(c):.6f})")
m1_ok = worst <= 1e-12
check("M1 Whittaker modes W_{kappa -+ 1/2, i rho_f}(2 i k tau) satisfy the Dirac system to <= 1e-12", m1_ok, f"(worst {worst:.1e})")
if MUTATE:
    print("\nMUTATE CONTROL: the scalar index rho_s replaced rho_f.")
    print(f"  M1 {'FAILED as required -- the control works' if not m1_ok else 'DID NOT FAIL -- the check has no power'}")
    sys.exit(1 if not m1_ok else 0)
check("M1b |c| = 1/mu (the constant used by the current script)", worst_c <= 1e-10, f"(worst {worst_c:.1e})")

print("\nM2. norm conservation |Psi_1|^2 + |Psi_2|^2 in tau (k = 1.3, lambda = 0.6, mu = 0.6)")
c = 1j / mp.mpf(0.6)
norms = []
for tau in (-0.3, -0.8, -1.0, -2.5, -6.0):
    s1, s2 = w_components(1.3, 0.6, 0.6, tau, c)
    norms.append(abs(s1) ** 2 + abs(s2) ** 2)
spread = float((max(norms) - min(norms)) / min(norms))
print("     norms:", [f"{float(v):.12f}" for v in norms])
check("M2 unit-norm constant in tau", spread <= 1e-12, f"(relative spread {spread:.1e}; the constant only fixes the overall normalisation of the unnormalised construction)")

print("\nM3. independent ODE integration from tau_0 = -4000/|k| (adiabatic eigenvector start) vs Whittaker construction, f = |Psi_1|^2 - |Psi_2|^2 at tau = -1")
M3_TRIPLES = [(0.5, 0.3, 0.9), (2.0, 0.6, 0.6), (1.0, -0.4, 0.5), (-0.5, 0.3, 0.9), (-2.0, 0.6, 0.6), (-1.0, -0.4, 0.5)]
worst3 = 0.0
print("      k     lambda   mu     f(ODE)         f(Whittaker)    |diff|     norm(ODE)-1")
for k, lam, mu in M3_TRIPLES:
    fo, no = f_ode(k, lam, mu)
    fw = f_whittaker(k, lam, mu)
    d = abs(fo - fw)
    worst3 = max(worst3, d)
    print(f"     {k:+5.2f}  {lam:+5.2f}  {mu:5.2f}   {fo:+.8f}    {fw:+.8f}    {d:.1e}    {no - 1:+.1e}")
check("M3 Whittaker Bunch-Davies modes (k>0) and the k<0 swap mapping agree with the far-past ODE integration to <= 1e-4", worst3 <= 1e-4, f"(worst {worst3:.1e})")

print("\nP1. pair production |beta_k|^2 by projection onto the out modes vs Stahl-Strobel-Xue eq. (73)   [k>0; r = sgn(k lambda)]")
P1_TRIPLES = [(1.0, 0.5, 1.0), (1.0, -0.5, 1.0), (0.3, 1.2, 0.3), (0.3, -1.2, 0.3), (2.5, 0.2, 2.0), (2.5, -0.2, 2.0)]
worstp = 0.0
print("      k     lambda    mu      |beta|^2 (numeric)   eq.(73)          rel diff    |alpha|^2+|beta|^2-1   |<out+|out->|")
for k, lam, mu in P1_TRIPLES:
    b2, a2, orth = beta2_numeric(k, lam, mu)
    r = 1 if lam > 0 else -1
    ref = n_k_paper(abs(lam), mu, r)
    rd = abs(b2 / ref - 1)
    worstp = max(worstp, rd)
    print(f"     {k:4.1f}  {lam:+5.2f}  {mu:5.2f}    {b2:.10e}     {ref:.10e}    {rd:.1e}     {a2 + b2 - 1:+.1e}          {orth:.1e}")
b2k1 = beta2_numeric(1.0, 0.5, 1.0)[0]
b2k2 = beta2_numeric(3.7, 0.5, 1.0)[0]
print(f"     k-independence: |beta|^2 at k = 1.0 and k = 3.7 (lambda = 0.5, mu = 1): {b2k1:.10e}  {b2k2:.10e}")
check("P1 numeric |beta_k|^2 equals eq. (73) to <= 1e-6 (both signs of r), independent of |k|", worstp <= 1e-6 and abs(b2k1 / b2k2 - 1) <= 1e-8, f"(worst {worstp:.1e})")

print("\nP2. massless limit (mu = 1e-3): n_k -> theta(k lambda)")
n_scr = beta2_numeric(1.0, 1.0, 1e-3)[0]
n_anti = beta2_numeric(1.0, -1.0, 1e-3)[0]
print(f"     lambda = +1 (screening, k lambda > 0):   n = {n_scr:.6f}")
print(f"     lambda = -1 (anti-screening):            n = {n_anti:.3e}")
check("P2 n_k >= 0.99 for k lambda > 0 and <= 0.01 for k lambda < 0 at mu = 1e-3", n_scr >= 0.99 and n_anti <= 0.01)

print("\n" + "=" * 110)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT (against the declared criteria):")
print("  * The dS_2 Dirac system, its exact Whittaker modes with index i*sqrt(mu^2 + lambda^2), the k<0 mapping and the pair-production factor")
print("    are verified independently of the published formulas (ODE from the far past; out-mode projection).")
print("  * Massless limit: n_k = theta(k lambda) (probability 1 in the screening direction, 0 against it): spectral flow.")
print("  * 2D toy: e has mass dimension 1 here; lambda = eE/H^2 is the only place e enters the pair-production factor.")
sys.exit(0 if passed == len(CHECKS) else 1)
