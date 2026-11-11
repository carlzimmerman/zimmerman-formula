#!/usr/bin/env python3
"""QG1: quantum health of action (A) as an effective field theory (gate T2 of TOE0).

Criteria: FROZEN_CRITERIA.md (committed alone before this script). TEST lane: adopts nothing.
Units in the graded part: hbar = c = 1, energies in eV. Footings never pooled.
Run:      python3 qg1.py                    -> qg1.out, qg1.json       (exit 0 iff every known answer passes)
MUTATE:   QG1_MUTATE=M1|M2|M3|M4 python3 qg1.py -> qg1_MUTATE_<arm>.out/.json (exit 0 iff the twin bites)
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time, math
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ARM = os.environ.get("QG1_MUTATE", "").strip()
if ARM not in ("", "M1", "M2", "M3", "M4"):
    sys.exit("QG1_MUTATE must be one of M1..M4")
STEM = "qg1" if not ARM else f"qg1_MUTATE_{ARM}"
LINES = []


def P_(s=""):
    print(s, flush=True)
    LINES.append(s)


def f(x, n=4):
    return mp.nstr(mp.mpf(x), n) if not isinstance(x, str) else x


RES = {"arm": ARM or "none", "known_answers": {}, "rows": {}, "reports": {}}

# ------------------------------------------------------------------ physical constants (SI) and conversions
G_SI, C_SI, HBAR = mp.mpf("6.6743e-11"), mp.mpf("2.99792458e8"), mp.mpf("1.054571817e-34")
EV, KB = mp.mpf("1.602176634e-19"), mp.mpf("1.380649e-23")
MSUN, MEARTH, REARTH = mp.mpf("1.98847e30"), mp.mpf("5.9722e24"), mp.mpf("6.371e6")
AU, PC = mp.mpf("1.495978707e11"), mp.mpf("3.0856775814913673e16")
KPC, MPC = 1000 * PC, 10 ** 6 * PC
HBARC = HBAR * C_SI / EV                       # eV m
MPL = mp.sqrt(HBAR * C_SI ** 5 / (8 * mp.pi * G_SI)) / EV   # reduced Planck mass, eV
KN = 1 / (2 * MPL ** 2)                        # K = 4 pi G_N = 1/(2 M^2), eV^-2
FOOT = {"canonical": {"a0": mp.mpf("9.3603e-11"), "Lstar_pc": mp.mpf("21.7"), "muK_Mpc": mp.mpf("8.890e6")},
        "alt": {"a0": mp.mpf("1.1312e-10"), "Lstar_pc": mp.mpf("22.9"), "muK_Mpc": mp.mpf("8.889e6")}}
I0G = mp.mpf("4.037e-8") / MPC ** 2            # KD1's I0, m^-2 (SCS1's constant)
KG_SI = 4 * mp.pi * G_SI / C_SI ** 2           # m/kg
RHO_C0 = I0G / (2 * KG_SI)                     # cold charge today, kg/m^3
COLD_SHARE = mp.mpf("5.41")
TCMB = mp.mpf("2.7255")


def L_nat(m):      return m / HBARC                       # length (m) -> eV^-1
def k_nat(m_inv):  return m_inv * HBARC                   # inverse length -> eV
def acc_nat(a):    return a / C_SI ** 2 * HBARC           # acceleration (m/s^2) -> eV
def rho_nat(rho):  return rho * C_SI ** 2 / EV * HBARC ** 3   # kg/m^3 -> eV^4 (energy density)
def rate_nat(r):   return HBAR * r / EV                   # s^-1 -> eV


def rho_rad0():
    rg = (mp.pi ** 2 / 15) * (KB * TCMB) ** 4 / (HBAR * C_SI) ** 3 / C_SI ** 2
    return rg * (1 + mp.mpf("3.046") * mp.mpf(7) / 8 * (mp.mpf(4) / 11) ** (mp.mpf(4) / 3))


def rho_de(a0):    return 4 * a0 ** 2 / (C_SI ** 2 * G_SI)   # rule 4: a0 = (1/2) c sqrt(G rho_DE)


def hubble(z, a0):
    rho = RHO_C0 * (1 + 1 / COLD_SHARE) * (1 + z) ** 3 + rho_rad0() * (1 + z) ** 4 + rho_de(a0)
    return mp.sqrt(8 * mp.pi * G_SI * rho / 3)


# ------------------------------------------------------------------ generic tools shared by known answers and graded rows
def crossing(Rfun, kIR, kmax, per_dec=20):
    """smallest k >= kIR with R(k) >= 1 (log grid then bisection in ln k); returns (k_x, tag)."""
    r0, _ = Rfun(kIR)
    if r0 >= 1:
        return mp.mpf(0), "strong at k_IR"
    n = int(mp.ceil(per_dec * mp.log10(kmax / kIR)))
    prev = kIR
    for i in range(1, n + 1):
        k = kIR * mp.mpf(10) ** (mp.mpf(i) / per_dec)
        r, _ = Rfun(k)
        if r >= 1:
            lo, hi = mp.log(prev), mp.log(k)
            for _ in range(80):
                mid = (lo + hi) / 2
                if Rfun(mp.e ** mid)[0] >= 1:
                    hi = mid
                else:
                    lo = mid
                if hi - lo < mp.mpf("1e-14"):
                    break
            return mp.e ** hi, Rfun(mp.e ** hi)[1]
        prev = k
    return None, "no crossing below k_max"


def zero_point(omega_of_k, kmin, kmax, breaks=()):
    """E_0 = (1/2) Int d^3k/(2pi)^3 |omega| = (1/(4 pi^2)) Int k^3 |omega(k)| d ln k."""
    pts = [mp.log(kmin)] + sorted(mp.log(b) for b in breaks if kmin < b < kmax) + [mp.log(kmax)]
    return mp.quad(lambda lk: mp.e ** (3 * lk) * abs(omega_of_k(mp.e ** lk)), pts) / (4 * mp.pi ** 2)


def c_cross_gauss(c):
    """AMENDMENT A1 item 3 (reported only): 2 E[(Pibar + X)^2 1{X < -Pibar}]/sigma^2, X ~ N(0, sigma^2), c = Pibar/sigma.
    Equals 1 at c = 0 (the frozen value at Pibar = 0) and falls as exp(-c^2/2) for c >> 1."""
    return 2 * ((1 + c ** 2) * mp.ncdf(-c) - c * mp.npdf(c))


# ------------------------------------------------------------------ W(K|P|) directional derivatives (exact, sympy)
_t, _pb, _cd, _K, _a0 = sp.symbols("t pb cd K a0", positive=True)
_p = sp.sqrt(_pb ** 2 + 2 * _K * _pb * _cd * _t + _K ** 2 * _t ** 2)
_W = (_a0 ** 2 / _K) * (-_p / _a0 - sp.log(1 - _p / _a0))
F3 = sp.lambdify((_pb, _cd, _K, _a0), sp.simplify(sp.diff(_W, _t, 3).subs(_t, 0)), "mpmath")
F4 = sp.lambdify((_pb, _cd, _K, _a0), sp.simplify(sp.diff(_W, _t, 4).subs(_t, 0)), "mpmath")


def W_of(p, a0, K):
    return (a0 ** 2 / K) * (-p / a0 - mp.log(1 - p / a0))


# ==================================================================================== KNOWN ANSWERS
KA_OK = True


def ka(name, ok, msg):
    global KA_OK
    KA_OK = KA_OK and bool(ok)
    RES["known_answers"][name] = {"pass": bool(ok), "detail": msg}
    P_(f"{name}: {'PASS' if ok else 'FAIL'}  {msg}")


P_("QG1 - quantum health of action (A), gate T2 of TOE0. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P_(f"arm: {ARM or 'none (main run)'};  M_Pl(reduced) = {f(MPL, 6)} eV;  K = 1/(2 M^2) = {f(KN, 6)} eV^-2")
P_("")
P_("=== Known answers ===")

# ---- KA1: GR graviton on Minkowski
def ka1():
    t, x, y, z, e = sp.symbols("t x y z epsilon", real=True)
    h = sp.Function("h")(t, z)
    X = [t, x, y, z]
    g = sp.diag(-1, 1, 1, 1)
    g[1, 2] = g[2, 1] = e * h
    Hm = sp.zeros(4, 4); Hm[1, 2] = Hm[2, 1] = h
    eta = sp.diag(-1, 1, 1, 1)
    ginv = eta - e * eta * Hm * eta + e ** 2 * eta * Hm * eta * Hm * eta      # truncated inverse, exact to e^2
    def tr(ex):
        ex = sp.expand(ex)
        return sum(ex.coeff(e, n) * e ** n for n in range(3))
    Gam = [[[tr(sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                     for d in range(4)) / 2) for c in range(4)] for b in range(4)] for a in range(4)]
    R = 0
    for b in range(4):
        for c in range(4):
            if ginv[b, c] == 0:
                continue
            Ric = sum(sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c]) for a in range(4))
            Ric += sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for a in range(4) for d in range(4))
            R += ginv[b, c] * Ric
    sqrtg = 1 - e ** 2 * h ** 2 / 2
    L2 = sp.expand(tr(sp.expand(sqrtg * tr(R)))).coeff(e, 2)
    target = (sp.diff(h, t) ** 2 - sp.diff(h, z) ** 2) / 2
    from sympy.calculus.euler import euler_equations
    el_L2 = euler_equations(L2, [h], [t, z])[0].lhs
    el_tg = euler_equations(target, [h], [t, z])[0].lhs
    resid = sp.simplify(el_L2 - el_tg)
    # the coefficient of h_t^2 survives total derivatives only through EL: EL(target) = -(h_tt - h_zz)
    ok = resid == 0
    return ok, f"EL[sqrt(-g)R at eps^2] - EL[(1/2)(h_t^2 - h_z^2)] = {resid} (EL of target: {el_tg}); omega^2 = k^2, kinetic +1/2"


ok, msg = ka1(); ka("KA1 GR graviton", ok, msg)

# ---- KA2 and C-MINK: unitary-gauge scalar sector of the general khronometric form
def adm_scalar():
    t, x, e = sp.symbols("t x epsilon", real=True)
    be, la, al_a, M, mu = sp.symbols("beta lambda alpha_a M mu", real=True)
    al = sp.Function("al")(t, x); B = sp.Function("B")(t, x); ze = sp.Function("ze")(t, x)
    N = 1 + e * al
    def tr(ex, n=2):
        return sp.series(ex, e, 0, n + 1).removeO()
    conf = sp.exp(2 * e * ze)                       # h_ij = conf delta_ij
    d = [lambda f_: sp.diff(f_, x), lambda f_: 0, lambda f_: 0]
    Nl = [e * sp.diff(B, x), 0, 0]                  # N_i = d_i B (lower)
    zeta_d = [sp.diff(ze, x), 0, 0]
    def Gam(k, i, j):                               # Christoffel of e^{2 e ze} delta
        return e * (int(k == i) * zeta_d[j] + int(k == j) * zeta_d[i] - int(i == j) * zeta_d[k])
    Kij = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            DiNj = d[i](Nl[j]) - sum(Gam(k, i, j) * Nl[k] for k in range(3))
            DjNi = d[j](Nl[i]) - sum(Gam(k, j, i) * Nl[k] for k in range(3))
            Kij[i, j] = (sp.diff(conf * int(i == j), t) - DiNj - DjNi) / (2 * N)
    KK = sum(Kij[i, j] ** 2 for i in range(3) for j in range(3)) * sp.exp(-4 * e * ze)
    Ktr = sum(Kij[i, i] for i in range(3)) * sp.exp(-2 * e * ze)
    R3 = -sp.exp(-2 * e * ze) * (4 * e * sp.diff(ze, x, 2) + 2 * e ** 2 * sp.diff(ze, x) ** 2)
    a2 = sp.exp(-2 * e * ze) * sp.diff(sp.log(N), x) ** 2
    sqh = sp.exp(3 * e * ze)
    L = (M ** 2 / 2) * N * sqh * ((1 - be) * KK - (1 + la) * Ktr ** 2 + R3 + al_a * a2) \
        + M ** 2 * mu ** 2 * N * sqh * (1 / N - 1) ** 2
    L2 = sp.expand(sp.diff(L, e, 2).subs(e, 0) / 2)
    from sympy.calculus.euler import euler_equations
    eqs = [q.lhs for q in euler_equations(L2, [al, B, ze], [t, x])]
    w, k = sp.symbols("omega k", positive=True)
    A_, B_, Z_ = sp.symbols("A_ B_ Z_")
    E = sp.exp(sp.I * (k * x - w * t))
    rows = []
    for q in eqs:
        qq = sp.expand(sp.simplify(q.subs({al: A_ * E, B: B_ * E, ze: Z_ * E}).doit() / E))
        rows.append([qq.coeff(A_), qq.coeff(B_), qq.coeff(Z_)])
    det = sp.factor(sp.simplify(sp.Matrix(rows).det()))
    return det, (be, la, al_a, M, mu, w, k)


det, (be, la, al_a, M_, mu_, w_, k_) = adm_scalar()
# KA2: mu = 0, general couplings: nonzero root in omega^2 vs BPS
det0 = sp.factor(det.subs(mu_, 0))
W2 = sp.symbols("W2", positive=True)
poly = sp.Poly(sp.expand(det0.subs(w_, sp.sqrt(W2))), W2)
roots = [r for r in sp.solve(poly.as_expr(), W2) if sp.simplify(r) != 0]
bps = (be + la) * (2 - al_a) / (al_a * (1 - be) * (2 + be + 3 * la)) * k_ ** 2
resid = [sp.simplify(r - bps) for r in roots]
ok2 = len(roots) == 1 and resid[0] == 0
ka("KA2 BPS khronon speed", ok2,
   f"det(omega) = {det0}; nonzero omega^2 roots {roots}; residual vs (beta+lambda)(2-alpha)/[alpha(1-beta)(2+beta+3lambda)] k^2 = {resid}")
# C-MINK: (A) on Minkowski is beta = lambda = 0 with any alpha_a (2 cY) and any mu: only omega = 0
detA = sp.factor(det.subs({be: 0, la: 0}))
degs = sp.Poly(sp.expand(detA), w_).monoms()
only_zero = sp.simplify(detA.subs(w_, 0)) == 0 and all(
    sp.simplify(r) == 0 for r in sp.solve(sp.expand(detA), w_))
RES["reports"]["C_MINK_unitary"] = {"det_beta_lambda_0": str(detA), "only_omega_zero": bool(only_zero)}
P_(f"C-MINK (A) in unitary gauge on Minkowski (beta = lambda = 0, any alpha_a, any mu): det = {detA}; "
   f"every root omega = 0: {only_zero}")
KA_OK = KA_OK and bool(only_zero)

# ---- KA3: Legendre and K J''(0) = 1
def ka3():
    worst = mp.mpf(0)
    a0, K = FOOT["canonical"]["a0"], KG_SI
    for u in (mp.mpf("1e-3"), mp.mpf("0.1"), 1, 10, mp.mpf("1e3")):
        A = u * a0
        # maximise over p = K|P| in (0, a0): P.A - W = (p/K) A - W(p)
        obj = lambda p: (p / K) * A - W_of(p, a0, K)
        pstar = mp.findroot(lambda p: A / K - (a0 / K) * p / (a0 - p), a0 * u / (1 + u))
        J = obj(pstar)
        Jex = (a0 ** 2 / K) * (u - mp.log(1 + u))
        worst = max(worst, abs(J / Jex - 1))
    uu = sp.symbols("u", positive=True)
    Jsym = uu - sp.log(1 + uu)          # (a0^2/K) J; J''(A) = (1/K) d2/du2
    KJpp0 = sp.limit(sp.diff(Jsym, uu, 2), uu, 0)
    return worst < mp.mpf("1e-30") and KJpp0 == 1, f"max rel |J - (a0^2/K)[u - ln(1+u)]| = {f(worst, 3)}; K J''(0) = {KJpp0} (alpha_a = 2 at A = 0)"


ok, msg = ka3(); ka("KA3 Legendre", ok, msg)

# ---- KA4 / KA5: the Newtonian Stueckelberg reduction vs SCS1's closed form; pure dust
def ka4():
    a, b, m, K, mu, G, k, phi, sd, s, X = sp.symbols("a b m K mu G k phi sd s X", real=True)
    # L2 for one longitudinal mode: p (P amplitude) * k * X - p^2/(2 m) + (mu^2/2K) X^2 - (k^2/2K) phi^2 - (G k^2/2) s^2, X = phi - sd
    pp = sp.symbols("pp", real=True)
    L = pp * k * (phi - sd) - pp ** 2 / (2 * m) + (mu ** 2 / (2 * K)) * (phi - sd) ** 2 - (k ** 2 / (2 * K)) * phi ** 2
    psol = sp.solve(sp.diff(L, pp), pp)[0]
    L1 = sp.simplify(L.subs(pp, psol))
    phisol = sp.solve(sp.diff(L1, phi), phi)[0]
    L2 = sp.simplify(L1.subs(phi, phisol))
    Z = sp.simplify(2 * sp.diff(L2, sd, 2) / 2)          # L2 = (Z/2) sd^2
    om2 = sp.simplify(G * k ** 2 / Z)
    scs1 = K * G * ((1 - K * m) * k ** 2 - mu ** 2) / (mu ** 2 + K * m * k ** 2)
    r1 = sp.simplify(om2 - scs1)
    dust = sp.simplify(om2.subs(m, 0) - (K * G / mu ** 2) * (k ** 2 - mu ** 2))
    jeans = sp.limit(-om2.subs(m, 0), k, 0)
    # tilt term: Pbar(x) d_x(sigma_x^2/2) and -(Pbar'(x)) sigma_x^2/2 have the same Euler-Lagrange equation
    x = sp.symbols("x", real=True)
    sig = sp.Function("sigma")(x); Pb = sp.Function("Pb")(x)
    from sympy.calculus.euler import euler_equations
    e1 = euler_equations(Pb * sp.diff(sp.diff(sig, x) ** 2 / 2, x), [sig], [x])[0].lhs
    e2 = euler_equations(-sp.diff(Pb, x) * sp.diff(sig, x) ** 2 / 2, [sig], [x])[0].lhs
    tilt = sp.simplify(e1 - e2)
    return (r1 == 0, f"omega^2 = {om2}; minus SCS1 closed form (Qbar = 1): {r1}; tilt IBP residual {tilt}", tilt == 0,
            dust == 0 and sp.simplify(jeans - K * G) == 0, f"pure dust: omega^2 - (K n/mu^2)(k^2 - mu^2) = {dust}; Jeans rate^2 at k -> 0 = {jeans} (= K G = 4 pi G rho)")


r1ok, r1msg, tiltok, dok, dmsg = ka4()
ka("KA4 SCS1 closed form", r1ok and tiltok, r1msg)
ka("KA5 pure dust", dok, dmsg)

# ---- KA6: |grad phi|^3/a0 strong coupling with the frozen ratio method
def R_relativistic(Z, c3):
    def R(k):
        s2 = k ** 3 / (4 * mp.pi ** 2 * Z * k)
        L2 = (Z * k ** 2 + Z * k ** 2) * s2 / 2
        return abs(c3) * k ** 3 * s2 ** mp.mpf(1.5) / L2, "c3"
    return R


worst6 = mp.mpf(0)
for fo, pars in FOOT.items():
    a0 = acc_nat(pars["a0"])
    for x in (mp.mpf("1e-2"), 1, mp.mpf("1e2")):
        gb = x * a0
        Z = 4 * MPL ** 2 * gb / a0          # L'' of (2/3) M^2 g^3/a0
        c3 = (mp.mpf(2) / 3) * MPL ** 2 / a0 # L'''/6
        kx, _ = crossing(R_relativistic(Z, c3), a0 * mp.mpf("1e-10"), MPL)
        lam = kx / mp.sqrt(2 * mp.pi)
        lam3 = mp.sqrt(12 * MPL * a0 * x ** mp.mpf(1.5))
        worst6 = max(worst6, abs(lam / lam3 - 1))
ka("KA6 |grad phi|^3/a0 strong coupling", worst6 < mp.mpf("1e-6"),
   f"ratio method vs Lambda_3 = sqrt(12 M a0) x^(3/4): max rel {f(worst6, 3)} (x 1e-2, 1, 1e2; both footings); "
   f"at x = 1 canonical Lambda_3 = {f(mp.sqrt(12 * MPL * acc_nat(FOOT['canonical']['a0'])) * 1e3, 4)} meV = 1/({f(HBARC / mp.sqrt(12 * MPL * acc_nat(FOOT['canonical']['a0'])) * 1e3, 4)} mm)")

# ---- KA7: zero-point integrator
cs, Lam, om0 = mp.mpf("1e-3"), mp.mpf("2.5"), mp.mpf("0.7")
e1 = zero_point(lambda k: cs * k, mp.mpf("1e-30"), Lam)
e2 = zero_point(lambda k: om0, mp.mpf("1e-30"), Lam)
r7 = max(abs(e1 / (cs * Lam ** 4 / (16 * mp.pi ** 2)) - 1), abs(e2 / (om0 * Lam ** 3 / (12 * mp.pi ** 2)) - 1))
ka("KA7 zero-point integrator", r7 < mp.mpf("1e-8"), f"max rel {f(r7, 3)}")

# ---- KA8: growth ODE
def growth_f(dlnH, src, Nstart, Nend, D0, dD0):
    """D'' + (2 + dlnH/dN) D' - src(N) D = 0 in N = ln a; returns f = D'/D at Nend (scipy, rtol 1e-12)."""
    from scipy.integrate import solve_ivp
    rhs = lambda N, y: [y[1], -(2 + float(dlnH(N))) * y[1] + float(src(N)) * y[0]]
    sol = solve_ivp(rhs, (float(Nstart), float(Nend)), [float(D0), float(dD0)], method="DOP853", rtol=1e-12, atol=1e-30)
    y = sol.y[:, -1]
    return mp.mpf(y[1]) / mp.mpf(y[0])


fe = growth_f(lambda N: -1.5, lambda N: 1.5, math.log(1e-3), 0.0, 1e-3, 1e-3)
Om = mp.mpf("0.3")
fl = growth_f(lambda N: -1.5 * float(Om) * math.exp(-3 * N) / (float(Om) * math.exp(-3 * N) + 1 - float(Om)),
              lambda N: 1.5 * float(Om) * math.exp(-3 * N) / (float(Om) * math.exp(-3 * N) + 1 - float(Om)),
              math.log(1e-3), 0.0, 1e-3, 1e-3)
ka("KA8 growth ODE", abs(fe - 1) < mp.mpf("1e-8") and abs(fl / Om ** mp.mpf("0.55") - 1) < mp.mpf("0.01"),
   f"EdS f = {f(fe, 12)}; flat Omega_m 0.3: f(0) = {f(fl, 6)} vs Omega_m^0.55 = {f(Om ** mp.mpf('0.55'), 6)} (rel {f(fl / Om ** mp.mpf('0.55') - 1, 3)})")

# C2 (AMENDMENT A1): the Gaussian crossing factor against direct quadrature
c2w = mp.mpf(0)
for cc in (mp.mpf(0), mp.mpf("0.5"), mp.mpf(1), mp.mpf(3)):
    direct = 2 * mp.quad(lambda xx: (cc + xx) ** 2 * mp.npdf(xx), [-mp.inf, -cc])
    c2w = max(c2w, abs(direct - c_cross_gauss(cc)))
ka("C2 Gaussian crossing factor (A1)", c2w < mp.mpf("1e-30") and abs(c_cross_gauss(0) - 1) < mp.mpf("1e-35"),
   f"max |quadrature - closed form| = {f(c2w, 3)} at c = 0, 0.5, 1, 3; value at c = 0: {f(c_cross_gauss(0), 6)}")

# consistency: K G for rho = 1 kg/m^3 equals (hbar sqrt(4 pi G rho)/eV)^2
c0 = KN * rho_nat(mp.mpf(1)) / rate_nat(mp.sqrt(4 * mp.pi * G_SI)) ** 2 - 1
ka("C0 unit chain", abs(c0) < mp.mpf("1e-20"), f"K*rho(eV^4) / (free-fall rate in eV)^2 - 1 = {f(c0, 3)}")
P_(f"Known answers all pass: {KA_OK}")
P_("")

# ==================================================================================== BACKGROUNDS
def law_g(Mb, a0, r):
    gn = G_SI * Mb / r ** 2
    return gn / 2 + mp.sqrt(gn ** 2 / 4 + gn * a0)


def phantom(Mb, a0, r):
    """D.P = (1/(4 pi G r^2)) d(r^2 g)/dr for the law around a point mass (kg/m^3)."""
    return mp.diff(lambda rr: rr ** 2 * law_g(Mb, a0, rr), r) / (4 * mp.pi * G_SI * r ** 2)


def backgrounds(fo, reading="graded"):
    pars = FOOT[fo]
    a0s = pars["a0"]; a0 = acc_nat(a0s)
    Lst = pars["Lstar_pc"] * PC
    gL = KN * L_nat(Lst) ** 2 / 2
    muS = k_nat(pars["muK_Mpc"] / MPC)
    out = {}
    base = dict(a0=a0, gL=gL, foot=fo)
    # MINK (identical in both mu readings: G = 0)
    out["MINK"] = dict(base, uP=mp.mpf(0), G=mp.mpf(0), Pib=mp.mpf(0), nd=mp.mpf(0),
                       mu=(muS if reading == "other" else mp.mpf(0)), H=mp.mpf(0), L=L_nat(mp.mpf("1e-3")),
                       kIR=1 / L_nat(mp.mpf("1")), static=True, desc="Minkowski, L = 1 mm")
    for zz, nm in ((1100, "FRW1100"), (1, "FRW1")):
        rc = RHO_C0 * (1 + zz) ** 3
        Gz = rho_nat(rc)
        Hz = rate_nat(hubble(zz, a0s))
        mu = muS if reading == "graded" else mp.mpf(0)
        Gv = Gz if reading == "graded" else mp.mpf(0)   # with mu_K = 0 there is no dust charge on P = 0
        out[nm] = dict(base, uP=mp.mpf(0), G=Gv, Pib=mp.mpf(0), nd=Gv, mu=mu, H=Hz,
                       L=L_nat(10 * MPC / (1 + zz)), kIR=Hz, static=False, z=zz, rho_c=rc,
                       desc=f"FRW z = {zz}, L = 10 Mpc comoving")
    Mb = mp.mpf("6e10") * MSUN
    for xN, nm in ((mp.mpf("1e-2"), "PM-2"), (mp.mpf(1), "PM0"), (mp.mpf("1e2"), "PM2")):
        r = mp.sqrt(G_SI * Mb / (xN * a0s))
        g = law_g(Mb, a0s, r)
        u = g / a0s
        Gp = rho_nat(phantom(Mb, a0s, r))
        nd = rho_nat(RHO_C0) if reading == "other" else mp.mpf(0)
        out[nm] = dict(base, uP=u, G=Gp + nd, Pib=Gp, nd=nd, mu=(muS if reading == "other" else mp.mpf(0)),
                       H=mp.mpf(0), L=L_nat(KPC), kIR=1 / L_nat(r), static=True, r_m=r, u_law=u, xN=xN,
                       gA=acc_nat(g), gN=acc_nat(G_SI * Mb / r ** 2),
                       desc=f"point mass 6e10 Msun, x_N = {f(xN, 2)} (r = {f(r / KPC, 4)} kpc, x = g/a0 = {f(u, 4)}), L = 1 kpc")
    # Sun at 1 AU: screened polarization (QX17C hedgehog), charge M/(2 pi Lstar^2 r)
    gstar = G_SI * MSUN / Lst ** 2
    Gs = rho_nat(MSUN / (2 * mp.pi * Lst ** 2 * AU))
    nd = rho_nat(RHO_C0) if reading == "other" else mp.mpf(0)
    out["SUN"] = dict(base, uP=gstar / (a0s - gstar), G=Gs + nd, Pib=Gs, nd=nd,
                      mu=(muS if reading == "other" else mp.mpf(0)), H=mp.mpf(0), L=L_nat(AU), kIR=1 / L_nat(AU),
                      static=True, x_sun=G_SI * MSUN / AU ** 2 / a0s, gstar=gstar,
                      gA=acc_nat(G_SI * MSUN / AU ** 2 + gstar), gN=acc_nat(G_SI * MSUN / AU ** 2),
                      desc=f"Sun at 1 AU (x = {f(G_SI * MSUN / AU ** 2 / a0s, 3)}), hedgehog g* = {f(gstar, 3)} m/s^2, L = 1 AU")
    return out


# ==================================================================================== the khronon mode (M-B), frozen coefficients
THETAS = [mp.mpf(0), mp.pi / 2, mp.pi / 4]


def mode(bg, k, th, branch, arm=ARM, G_override=None):
    K, a0, u = KN, bg["a0"], bg["uP"]
    gL = bg["gL"] if branch == "on" else mp.mpf(0)
    s2, c2 = mp.sin(th) ** 2, mp.cos(th) ** 2
    sW = -1 if arm == "M2" else 1
    q = s2 / (1 + u) + c2 / (1 + u) ** 2
    m0 = sW * q / K
    d0 = (s2 * u / (1 + u) + c2 * u * (2 + u) / (1 + u) ** 2) if sW == 1 else 1 + q
    gk = gL * k ** 2 * m0
    m = m0 / (1 + gk)
    oneKm = (d0 + gk) / (1 + gk)
    smu = -1 if arm == "M1" else 1
    mu2 = bg["mu"] ** 2
    a = m * k ** 2 + smu * mu2 / K
    b = k ** 2 / K
    bma = b * oneKm - smu * mu2 / K
    G = bg["G"] if G_override is None else G_override
    if arm == "M3":
        G = mp.mpf(0)
    if bma == 0:
        Z, om2 = mp.inf, mp.mpf(0)
    else:
        Z = a * b / bma
        om2 = G * k ** 2 * bma / (a * b)
    Mk = mp.sqrt(s2 / (1 + u) ** 2 + c2 / (1 + u) ** 4) / (K * abs(1 + gk))
    cd = (mp.sqrt(c2) / (1 + u) ** 2) / mp.sqrt(s2 / (1 + u) ** 2 + c2 / (1 + u) ** 4)
    return dict(m=m, m0=m0, a=a, b=b, bma=bma, Z=Z, om2=om2, G=G, Mk=Mk, cd=cd, gk=gk, sW=sW, smu=smu, mu2=mu2)


def branches(bg):
    return ("on", "off") if bg["Pib"] == 0 else ("on",)


def R_point(bg, k, arm=ARM, gauss=False):
    """max over angles and branches of the frozen vertex ratios; returns (R, tag)."""
    best, tag = mp.mpf(0), ""
    K, a0 = KN, bg["a0"]
    pb = a0 * bg["uP"] / (1 + bg["uP"])
    for br in branches(bg):
        for th in THETAS:
            q = mode(bg, k, th, br, arm)
            om = mp.sqrt(abs(q["om2"]))
            oe = om if bg["static"] else max(om, bg["H"])
            if oe == 0 or q["Z"] == mp.inf:
                return mp.inf, f"omega_eff = 0 (G = {f(q['G'], 3)}), branch {br}"
            Za = abs(q["Z"])
            s2 = k ** 3 / (4 * mp.pi ** 2 * Za * oe)
            s = mp.sqrt(s2)
            dXi = q["b"] * oe * s / abs(q["bma"])
            dP = q["Mk"] * k * dXi
            dPi = abs(q["m"]) * k ** 2 * dXi
            L2 = (Za * oe ** 2 + abs(q["G"]) * k ** 2) * s2 / 2
            if pb == 0:
                f3, f4 = K ** 2 / (3 * a0), K ** 3 / (4 * a0 ** 2)
            else:
                f3 = abs(F3(pb, q["cd"], K, a0)) / 6
                f4 = abs(F4(pb, q["cd"], K, a0)) / 24
            if q["sW"] == -1:
                pass  # |f| unchanged by the sign flip
            V = {"tilt": abs(q["m"]) * k ** 4 * dXi * s2 / 2,
                 "law3": f3 * dP ** 3, "law4": f4 * dP ** 4,
                 "dust3": q["mu2"] / K * dXi * k ** 2 * s2 / 2, "dust4": q["mu2"] * k ** 4 * s2 ** 2 / (8 * K)}
            Rs = {kk: vv / L2 for kk, vv in V.items()}
            gl = bg["gL"]
            if bg["Pib"] == 0:
                ccross = mp.mpf(1)
            elif gauss:
                ccross = c_cross_gauss(bg["Pib"] / dPi)
            else:
                ccross = min(mp.mpf(1), dPi / bg["Pib"])
            Rs["switch"] = gl * k ** 2 * abs(q["m0"]) / 2 * ccross
            kk_, vv_ = max(Rs.items(), key=lambda it: it[1])
            if vv_ > best:
                best, tag = vv_, f"{kk_} (branch {br}, theta {f(th * 180 / mp.pi, 3)} deg)"
    return best, tag


def lambda_s(bg, arm=ARM, gauss=False):
    kmax = 10 * mp.sqrt(2 * mp.pi) * MPL
    kx, tag = crossing(lambda k: R_point(bg, k, arm, gauss), bg["kIR"], kmax)
    if kx is None:
        return MPL, "no crossing below M_Pl (Lambda_s set to M_Pl, a lower bound)", True
    return kx / mp.sqrt(2 * mp.pi), tag, False


# ---------------------------------------------------------------- growth of the cold component on FRW (criterion (i)(e))
def frw_growth_f(z_target, a0s, kcom, muS):
    rc0, rb0, rr0, rde = (float(v) for v in (RHO_C0, RHO_C0 / COLD_SHARE, rho_rad0(), rho_de(a0s)))
    Gf = float(G_SI)
    rho_t = lambda a: (rc0 + rb0) * a ** -3 + rr0 * a ** -4 + rde
    H2 = lambda a: 8 * math.pi * Gf / 3 * rho_t(a)
    dlnH = lambda N: 0.5 * (-3 * (rc0 + rb0) * math.exp(-3 * N) - 4 * rr0 * math.exp(-4 * N)) / rho_t(math.exp(N))
    adec = 1 / 1101.0
    kc, mu_ = float(kcom), float(muS)
    def src(N):
        a = math.exp(N)
        kphys = kc / a
        jeans = mu_ ** 2 / (mu_ ** 2 + kphys ** 2)     # the khronon's own Jeans factor at k (off branch); ~1 at 10 Mpc
        rho_cl = rc0 * jeans * a ** -3 + (rb0 * a ** -3 if a > adec else 0.0)
        return 4 * math.pi * Gf * rho_cl / H2(a)
    Ni, Nt = math.log(1e-5), math.log(1 / (1 + float(z_target)))
    aeq = rr0 / (rc0 + rb0)
    y = 1e-5 / aeq
    fz = growth_f(dlnH, src, Ni, Nt, 1 + 1.5 * y, 1.5 * y)
    at = 1 / (1 + float(z_target))
    return fz, mp.mpf(math.sqrt(4 * math.pi * Gf * rc0 * at ** -3 / H2(at)))


# ---------------------------------------------------------------- (iii) one loop
SM_HEAVY = [("top", "172.69", 12, 1), ("Higgs", "125.25", 1, 0), ("W", "80.377", 6, 0), ("Z", "91.1876", 3, 0)]
SM_ALL = SM_HEAVY + [("bottom", "4.18", 12, 1), ("charm", "1.27", 12, 1), ("tau", "1.77686", 4, 1),
                     ("strange", "0.093", 12, 1), ("muon", "0.1056584", 4, 1), ("down", "0.00467", 12, 1),
                     ("up", "0.00216", 12, 1), ("electron", "0.000510999", 4, 1)]
N_EFF = 121


def eps_matter(lam_c):
    e_cut = N_EFF * lam_c ** 2 / (16 * mp.pi ** 2 * MPL ** 2)
    e_sm = sum(n * (mp.mpf(m) * 10 ** 9) ** 2 * mp.log(MPL ** 2 / (mp.mpf(m) * 10 ** 9) ** 2) for _, m, n, _ in SM_HEAVY) \
        / (16 * mp.pi ** 2 * MPL ** 2)
    return e_cut, e_sm


GL8 = None


def gl_nodes(n=8):
    global GL8
    if GL8 is None:
        xs, ws = [], []
        for i in range(1, n + 1):
            x0 = mp.cos(mp.pi * (i - mp.mpf(1) / 4) / (n + mp.mpf(1) / 2))
            x0 = mp.findroot(lambda x: mp.legendre(n, x), x0)
            dp = mp.diff(lambda x: mp.legendre(n, x), x0)
            xs.append(x0); ws.append(2 / ((1 - x0 ** 2) * dp ** 2))
        GL8 = (xs, ws)
    return GL8


def E0_of_u(bg, u, lam_c, arm=ARM):
    bgu = dict(bg, uP=u)
    xs, ws = gl_nodes()
    def om_avg(k):
        tot = mp.mpf(0)
        for xg, wg in zip(xs, ws):
            if xg <= 0:
                continue
            th = mp.acos(xg)
            best = mp.mpf(0)
            for br in branches(bgu):
                q = mode(bgu, k, th, br, arm)
                best = max(best, mp.sqrt(abs(q["om2"])))
            tot += wg * best
        return tot      # weights over (0,1] sum to 1 (half of [-1,1])
    brk = [1 / L_nat(FOOT[bg["foot"]]["Lstar_pc"] * PC)]
    if bg["mu"] > 0:
        brk.append(bg["mu"])
    if lam_c <= bg["kIR"]:
        return mp.mpf(0)
    return zero_point(om_avg, bg["kIR"], lam_c, brk)


def one_loop(bg, lam_s, arm=ARM):
    lam_c = min(lam_s, MPL)
    e_cut, e_sm = eps_matter(lam_c)
    eps = e_cut + e_sm + (mp.mpf("1e-2") if arm == "M4" else 0)
    a0 = bg["a0"]
    xs = [mp.mpf(10) ** (mp.mpf(i) / 2) for i in range(-4, 5)]
    rows, ok = [], True
    for x in xs:
        h = mp.mpf("1e-6")
        dE = (E0_of_u(bg, x * (1 + h), lam_c, arm) - E0_of_u(bg, x * (1 - h), lam_c, arm)) / (2 * x * h)
        dmu_khr = KN * abs(dE) / a0 / (a0 * x)
        dmu_eps = eps / ((1 + eps) * (1 + x))
        dmu = dmu_khr + dmu_eps
        mu_x = x / (1 + x)
        rel = dmu / mu_x
        ok = ok and rel <= mp.mpf("0.1")
        rows.append({"x": f(x, 4), "dmu_khronon": f(dmu_khr, 4), "dmu_eps": f(dmu_eps, 4), "dmu_over_mu": f(rel, 4)})
    da0 = mp.mpf(rows[0]["dmu_over_mu"])
    ok = ok and da0 <= mp.mpf("0.1")
    return ok, {"Lambda_c_eV": f(lam_c, 6), "eps_cutoff": f(e_cut, 4), "eps_SM_dimreg": f(e_sm, 4), "eps_total": f(eps, 4),
                "dmu_rows": rows, "Delta_a0_over_a0": f(da0, 4)}


# ---------------------------------------------------------------- (i)
def criterion_i(bg, arm=ARM):
    notes, ok = [], True
    K, u, gl = KN, bg["uP"], bg["gL"]
    sW = -1 if arm == "M2" else 1
    ktop = 10 * mp.sqrt(2 * mp.pi) / bg["L"]
    # (a) P-sector Hessian, closed form (AMENDMENT A1 item 1): H_P = sW K diag(1+u, 1+u, (1+u)^2) plus the rank-one
    # stiffness gL k^2 khat khat^T, khat in the x-z plane. The y eigenvalue sW K (1+u) is untouched; the x-z block has
    # det = K^2 (1+u)^3 + sW K gL k^2 [(1+u) cos^2 + (1+u)^2 sin^2] and lambda_min = det/lambda_max.
    worst_eig = mp.inf
    for th in THETAS:
        s2_, c2_ = mp.sin(th) ** 2, mp.cos(th) ** 2
        for kk in (bg["kIR"], ktop, ktop * 1000):
            for br in branches(bg):
                g_ = gl if br == "on" else 0
                ey = sW * (1 + u)
                A11, A22, A12 = sW * (1 + u) + g_ * kk ** 2 * s2_ / K, sW * (1 + u) ** 2 + g_ * kk ** 2 * c2_ / K, \
                    g_ * kk ** 2 * mp.sqrt(s2_ * c2_) / K
                tr_, det_ = A11 + A22, (1 + u) ** 3 + sW * (g_ * kk ** 2 / K) * ((1 + u) * c2_ + (1 + u) ** 2 * s2_)
                lmax = tr_ / 2 + mp.sqrt((A11 - A22) ** 2 / 4 + A12 ** 2)
                lmin = det_ / lmax if lmax != 0 else tr_ / 2 - mp.sqrt((A11 - A22) ** 2 / 4 + A12 ** 2)
                if lmax < 0:
                    lmin = tr_ / 2 - mp.sqrt((A11 - A22) ** 2 / 4 + A12 ** 2)
                worst_eig = min(worst_eig, ey, lmin)
    a_ok = worst_eig > 0
    # (b) tensor
    pb = bg["a0"] * u / (1 + u)
    # (b) AMENDMENT A1 item 2: only anisotropic stress sources the TT mode (2K pi_T). From QX17 E4 the pieces with free
    # P_m are K W' P_m P_n/|P|, 2 P_(m d_n) l and -2 gamma_L P_(m curlyD_n): |pi_T| <= (pbar/K)(K W'(pbar) + 2 g + 2 g_N)
    # (g_N stands for gamma_L |grad Pi|, exact at the hedgehog). Perfect-fluid pieces (dust, g_mn terms) give no TT mass.
    KWp = bg["a0"] * pb / (bg["a0"] - pb) if pb > 0 else mp.mpf(0)
    tens = 2 * pb * (KWp + 2 * bg.get("gA", 0) + 2 * bg.get("gN", 0)) * bg["L"] ** 2
    b_ok = tens <= mp.mpf("1e-6")
    # (c) ghost on the band and in the UV; (d) gradient instability; (e) Jeans
    ngrid = 40
    kgrid = [bg["kIR"] * (ktop / bg["kIR"]) ** (mp.mpf(i) / ngrid) for i in range(ngrid + 1)]
    kuv = [ktop * mp.mpf(10) ** j for j in (0, 1, 2, 3, 6)]
    minZ0, jeans_rate, grad_bad = mp.inf, mp.mpf(0), False
    for br in branches(bg):
        for th in THETAS:
            for kk in kgrid + [ktop * 1000, ktop * 10 ** 6]:
                q = mode(bg, kk, th, br, arm)
                minZ0 = min(minZ0, q["a"] / (kk ** 2 / K))   # Z_0 in units of k^2/K
                if q["om2"] < 0 and kk <= ktop:
                    jeans_rate = max(jeans_rate, mp.sqrt(-q["om2"]))
            seq = [mode(bg, kk, th, br, arm)["om2"] for kk in kuv]
            if all(s_ < 0 for s_ in seq) and all(abs(seq[i + 1]) > abs(seq[i]) for i in range(len(seq) - 1)):
                grad_bad = True
    c_ok = minZ0 > 0
    d_ok = not grad_bad
    e_ok, e_note = True, ""
    if not bg["static"]:
        pars = FOOT[bg["foot"]]
        fz, ffr = frw_growth_f(bg["z"], pars["a0"], 2 * mp.pi / (10 * MPC), pars["muK_Mpc"] / MPC)
        e_ok = fz < 1
        e_note = f"FRW growth rate f = dlnD/dlna = {f(fz, 5)} (< 1 needed); local free-fall rate / H = {f(ffr, 5)}"
        notes.append(e_note)
    elif jeans_rate > 0:
        e_note = f"bounded growth on a static background, max rate {f(jeans_rate / mp.mpf(rate_nat(1)), 3)} s^-1 (reported)"
        notes.append(e_note)
    ok = a_ok and b_ok and c_ok and d_ok and e_ok
    det = {"Hessian_min_eig_over_K": f(worst_eig, 5), "tensor_correction_over_k2_at_1_over_L": f(tens, 3),
           "min_Z0_over_k2_by_K": f(minZ0, 5), "gradient_instability": grad_bad, "jeans": e_note,
           "pass_a_b_c_d_e": [bool(a_ok), bool(b_ok), bool(c_ok), bool(d_ok), bool(e_ok)]}
    return ok, det


# ==================================================================================== GRADED ROWS
def grade_row(name, bg, arm=ARM, do_loop=True):
    i_ok, i_det = criterion_i(bg, arm)
    lam, tag, lower = lambda_s(bg, arm)
    LL = lam * bg["L"]
    ii_ok = LL >= 10
    lamG, tagG, lowerG = lambda_s(bg, arm, gauss=True)
    if lam == 0:
        iii_ok, iii_det = None, {"status": "NOT EVALUABLE (Lambda_s = 0: no loop expansion)"}
    elif do_loop:
        iii_ok, iii_det = one_loop(bg, lam, arm)
    else:
        iii_ok, iii_det = None, {"status": "not run in this arm"}
    lab = "PASS" if (i_ok and ii_ok and iii_ok) else "FAIL" if (i_ok is False or not ii_ok or iii_ok is False) else "OPEN"
    # omega at the band top and the IR end (for the record)
    ktop = 10 * mp.sqrt(2 * mp.pi) / bg["L"]
    om_info = {}
    for nm, kk in (("k_IR", bg["kIR"]), ("k_top", ktop)):
        q = mode(bg, kk, mp.mpf(0), "on", arm)
        om_info[nm] = {"k_eV": f(kk, 4), "omega2_eV2": f(q["om2"], 4), "Z0_over_k2_by_K": f(q["a"] / (kk ** 2 / KN), 4)}
    out = {"desc": bg["desc"], "label": lab, "i": bool(i_ok), "i_detail": i_det, "Lambda_s_eV": f(lam, 6),
           "Lambda_s_length_m": (f(HBARC / lam, 4) if lam > 0 else "inf"), "Lambda_s_L": f(LL, 6), "ii": bool(ii_ok),
           "ii_dominant": tag, "Lambda_s_is_lower_bound": lower, "iii": iii_ok, "iii_detail": iii_det, "omega": om_info,
           "G_eV4": f(bg["G"], 4), "uP": f(bg["uP"], 4),
           "A1_gauss_switch_Lambda_s_eV": f(lamG, 6), "A1_gauss_switch_Lambda_s_L": f(lamG * bg["L"], 6),
           "A1_gauss_switch_set_by": tagG, "A1_gauss_switch_lower_bound": lowerG}
    return out


def print_row(name, fo, r):
    P_(f"[{name} / {fo}] {r['desc']}")
    P_(f"   (i) {'PASS' if r['i'] else 'FAIL'}: {r['i_detail']}")
    P_(f"   (ii) Lambda_s = {r['Lambda_s_eV']} eV (1/{r['Lambda_s_length_m']} m); Lambda_s L = {r['Lambda_s_L']} -> "
       f"{'PASS' if r['ii'] else 'FAIL'}; set by {r['ii_dominant']}{' [lower bound]' if r['Lambda_s_is_lower_bound'] else ''}")
    P_(f"   (ii, A1 diagnostic, not graded) Gaussian switch crossing: Lambda_s L = {r['A1_gauss_switch_Lambda_s_L']}, set by "
       f"{r['A1_gauss_switch_set_by']}{' [lower bound]' if r['A1_gauss_switch_lower_bound'] else ''}")
    iii = r["iii_detail"]
    if "status" in iii:
        P_(f"   (iii) {iii['status']}")
    else:
        worst = max(iii["dmu_rows"], key=lambda q: mp.mpf(q["dmu_over_mu"]))
        P_(f"   (iii) {'PASS' if r['iii'] else 'FAIL'}: Lambda_c {iii['Lambda_c_eV']} eV, eps cutoff {iii['eps_cutoff']}, "
           f"eps SM {iii['eps_SM_dimreg']}; worst |dmu|/mu = {worst['dmu_over_mu']} at x = {worst['x']} "
           f"(khronon {worst['dmu_khronon']}, eps {worst['dmu_eps']}); |Delta a0/a0| = {iii['Delta_a0_over_a0']}")
    P_(f"   omega: {r['omega']}")
    P_(f"   ROW LABEL: {r['label']}")


ROW_ORDER = ["MINK", "FRW1100", "FRW1", "PM-2", "PM0", "PM2", "SUN"]

if not ARM:
    P_("=== Graded rows (record's mu_K reading per row: FRW mu_K*, static rows mu_K = 0) ===")
    labels = {}
    for fo in FOOT:
        bgs = backgrounds(fo, "graded")
        for nm in ROW_ORDER:
            r = grade_row(nm, bgs[nm])
            RES["rows"].setdefault(nm, {})[fo] = r
            labels[(nm, fo)] = r["label"]
            print_row(nm, fo, r)
    P_("")
    P_("=== Other mu_K reading (reported, not graded) ===")
    for fo in FOOT:
        bgs = backgrounds(fo, "other")
        for nm in ROW_ORDER:
            r = grade_row(nm, bgs[nm], do_loop=False)
            RES["reports"].setdefault("other_mu_reading", {}).setdefault(nm, {})[fo] = r
            P_(f"[{nm} / {fo} / other mu] (i) {'PASS' if r['i'] else 'FAIL'} {r['i_detail']['jeans']}; "
               f"Lambda_s L = {r['Lambda_s_L']} ({r['ii_dominant']})")
    P_("")
    # ---------------- null points and the Earth laboratory (reported)
    P_("=== Null points and the Earth laboratory (reported, not graded) ===")
    for fo in FOOT:
        pars = FOOT[fo]; a0s = pars["a0"]; a0 = acc_nat(a0s)
        Mb = mp.mpf("6e10") * MSUN
        prof = []
        for e10 in range(3, 9):
            xN = mp.mpf(10) ** (-e10)
            r = mp.sqrt(G_SI * Mb / (xN * a0s)); g = law_g(Mb, a0s, r)
            bg = dict(a0=a0, gL=KN * L_nat(pars["Lstar_pc"] * PC) ** 2 / 2, foot=fo, uP=g / a0s,
                      G=rho_nat(phantom(Mb, a0s, r)), Pib=rho_nat(phantom(Mb, a0s, r)), nd=mp.mpf(0), mu=mp.mpf(0),
                      H=mp.mpf(0), L=L_nat(KPC), kIR=1 / L_nat(r), static=True)
            lam, tag, _ = lambda_s(bg)
            prof.append({"x_N": f(xN, 2), "r_kpc": f(r / KPC, 4), "Lambda_s_L": f(lam * bg["L"], 4)})
        RES["reports"].setdefault("null_profile", {})[fo] = prof
        P_(f"[{fo}] point-mass profile to x_N = 1e-8: " + "; ".join(f"x_N {q['x_N']} (r {q['r_kpc']} kpc): Lambda_s L {q['Lambda_s_L']}" for q in prof))
        # generic null: g = a0 s/l, l = 10 kpc, G = a0/(K l)
        ell = L_nat(10 * KPC)
        def LsL(u):
            bg = dict(a0=a0, gL=KN * L_nat(pars["Lstar_pc"] * PC) ** 2 / 2, foot=fo, uP=u, G=a0 / (KN * ell),
                      Pib=a0 / (KN * ell), nd=mp.mpf(0), mu=mp.mpf(0), H=mp.mpf(0), L=L_nat(KPC), kIR=1 / ell, static=True)
            return lambda_s(bg)[0] * bg["L"]
        lo, hi = mp.log(mp.mpf("1e-30")), mp.log(mp.mpf(1))
        v_lo, v_hi = LsL(mp.e ** lo), LsL(mp.e ** hi)
        if v_lo >= 10:
            ucrit = mp.mpf(0); note = "Lambda_s L >= 10 down to u = 1e-30"
        elif v_hi < 10:
            ucrit = mp.mpf(1); note = "fails already at u = 1"
        else:
            for _ in range(40):
                mid = (lo + hi) / 2
                if LsL(mp.e ** mid) >= 10: hi = mid
                else: lo = mid
            ucrit = mp.e ** hi; note = "bisection"
        RES["reports"].setdefault("generic_null", {})[fo] = {"u_crit": f(ucrit, 4), "region_pc": f(ucrit * 10 * 1000, 4),
                                                              "Lambda_s_L_at_u_1e-30": f(v_lo, 4), "note": note}
        P_(f"[{fo}] generic null (field a0 s/l, l = 10 kpc, G = a0/(K l)): (ii) fails for u < {f(ucrit, 4)}, i.e. within "
           f"{f(ucrit * 10 * 1000, 4)} pc of the null ({note}; Lambda_s L at u = 1e-30: {f(v_lo, 4)})")
        # Earth laboratory: Sun's and Earth's hedgehogs, L = 1 mm
        Lst = pars["Lstar_pc"] * PC
        Ge = rho_nat(MSUN / (2 * mp.pi * Lst ** 2 * AU) + MEARTH / (2 * mp.pi * Lst ** 2 * REARTH))
        gst = G_SI * (MSUN + MEARTH) / Lst ** 2
        bg = dict(a0=a0, gL=KN * L_nat(Lst) ** 2 / 2, foot=fo, uP=gst / (a0s - gst), G=Ge, Pib=Ge, nd=mp.mpf(0),
                  mu=mp.mpf(0), H=mp.mpf(0), L=L_nat(mp.mpf("1e-3")), kIR=1 / L_nat(REARTH), static=True,
                  desc="Earth-surface laboratory")
        lam, tag, _ = lambda_s(bg)
        lamG, tagG, lowG = lambda_s(bg, gauss=True)
        RES["reports"].setdefault("earth_lab", {})[fo] = {"G_eV4": f(Ge, 4), "Lambda_s_eV": f(lam, 5),
                                                          "Lambda_s_length_m": f(HBARC / lam, 4), "Lambda_s_L": f(lam * bg["L"], 5), "set_by": tag,
                                                          "A1_gauss_Lambda_s_L": f(lamG * bg["L"], 5), "A1_gauss_set_by": tagG,
                                                          "A1_gauss_length_m": f(HBARC / lamG, 4), "A1_gauss_lower_bound": lowG}
        P_(f"[{fo}] Earth-surface lab (charge {f(rho_nat(1) ** -1 * Ge, 3)} kg/m^3 from the hedgehogs): Lambda_s = 1/({f(HBARC / lam, 4)} m), "
           f"Lambda_s x 1 mm = {f(lam * bg['L'], 5)} ({tag}); A1 Gaussian switch: Lambda_s = 1/({f(HBARC / lamG, 4)} m), "
           f"x 1 mm = {f(lamG * bg['L'], 5)} ({tagG}{', lower bound' if lowG else ''})")
    P_("")
    # ---------------- T4 report
    P_("=== T4 report: do matter loops break Lambda = 32 pi a0^2/c^4? ===")
    for fo in FOOT:
        rde = rho_nat(rho_de(FOOT[fo]["a0"]))
        drho = sum((-1 if F else 1) * n * (mp.mpf(m) * 10 ** 9) ** 4 / (64 * mp.pi ** 2) for _, m, n, F in SM_ALL)
        per = {nm: f(n * (mp.mpf(m) * 10 ** 9) ** 4 / (64 * mp.pi ** 2) / rde, 4) for nm, m, n, F in SM_ALL}
        cut = {nm: f(N_EFF * mp.mpf(RES["rows"][nm][fo]["Lambda_s_eV"]) ** 4 / (16 * mp.pi ** 2) / rde, 4)
               for nm in ROW_ORDER if mp.mpf(RES["rows"][nm][fo]["Lambda_s_eV"]) > 0}
        lam_eps = mp.sqrt(mp.mpf("1e-3") * 16 * mp.pi ** 2 / N_EFF) * MPL
        brk = abs(drho) / rde >= 1
        RES["reports"].setdefault("T4", {})[fo] = {"rho_DE_eV4": f(rde, 5), "Delta_rho_dimreg_over_rho_DE": f(abs(drho) / rde, 4),
                                                   "per_species_over_rho_DE": per, "cutoff_reading_over_rho_DE": cut,
                                                   "a0_shift_from_matter": "0 (S_m has no tau, P: no A-term at any loop order)",
                                                   "label": "BREAKS" if brk else "HOLDS",
                                                   "matter_cutoff_where_eps_1e-3_GeV": f(lam_eps / 10 ** 9, 4)}
        P_(f"[{fo}] rho_DE = {f(rde, 4)} eV^4; |Delta rho_vac| (dim reg, one log) / rho_DE = {f(abs(drho) / rde, 4)}; "
           f"electron alone {per['electron']}, top alone {per['top']}; with T2's cutoff per row: {cut}; a0 shift from matter 0; "
           f"T4 relation: {'BREAKS' if brk else 'HOLDS'}. eps reaches 1e-3 (mu(0.01) moved 10 %) only for a matter cutoff "
           f"{f(lam_eps / 10 ** 9, 4)} GeV")
    P_("")
    # ---------------- labels
    P_("=== Labels ===")
    allpass = all(v == "PASS" for v in labels.values())
    anyfail = any(v == "FAIL" for v in labels.values())
    T2 = "PASS" if (allpass and KA_OK) else "FAIL" if (anyfail and KA_OK) else "OPEN"
    for nm in ROW_ORDER:
        P_(f"{nm:8s} canonical {labels[(nm, 'canonical')]:5s} alt {labels[(nm, 'alt')]}")
    P_(f"T2 (QG1) = {T2}  (known answers {'all pass' if KA_OK else 'NOT all pass'}; MUTATE twins: separate runs)")
    RES["T2"] = T2
    RES["labels"] = {f"{k[0]}|{k[1]}": v for k, v in labels.items()}
else:
    # ================================================================== MUTATE arm: primary vs mutated on the target row
    target = {"M1": ("FRW1", "i"), "M2": ("PM0", "i"), "M3": ("PM0", "ii"), "M4": ("PM0", "iii")}[ARM]
    nm, crit = target
    bites = True
    for fo in FOOT:
        bg = backgrounds(fo, "graded")[nm]
        prim = grade_row(nm, bg, arm="", do_loop=(crit == "iii"))
        mut = grade_row(nm, bg, arm=ARM, do_loop=(crit == "iii"))
        b_ = (prim[crit] is True) and (mut[crit] is False)
        bites = bites and b_
        RES["rows"].setdefault(nm, {})[fo] = {"primary": prim, "mutated": mut, "bites": b_}
        P_(f"[{ARM} on {nm} / {fo}] criterion ({crit}): primary {prim[crit]} -> mutated {mut[crit]}  => {'BITES' if b_ else 'DOES NOT BITE'}")
        if crit == "i":
            P_(f"    mutated (i) detail: {mut['i_detail']}")
        if crit == "ii":
            P_(f"    mutated Lambda_s L = {mut['Lambda_s_L']} ({mut['ii_dominant']})")
        if crit == "iii":
            P_(f"    mutated |Delta a0/a0| = {mut['iii_detail'].get('Delta_a0_over_a0')}, eps {mut['iii_detail'].get('eps_total')}")
    RES["bites"] = bites
    P_(f"MUTATE {ARM}: {'BITES (as required)' if bites else 'DOES NOT BITE'}")

RES["runtime_s"] = round(time.time() - T0, 1)
P_(f"runtime {RES['runtime_s']} s")
with open(os.path.join(HERE, STEM + ".out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
with open(os.path.join(HERE, STEM + ".json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
if ARM:
    sys.exit(0 if RES.get("bites") else 2)
sys.exit(0 if KA_OK else 1)
