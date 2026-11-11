"""Blind regrade of TOE0-P (KA1-KA3, P1, P2 frozen + amended, M1, M2, reported numbers).

Independent code. Routes chosen to differ from a plain sympy-generic-metric variation:
  * Noether current: high-precision NUMERICAL differentiation (mpmath, 60 digits) of the
    Lagrangian w.r.t. d_m tau on random non-diagonal Lorentzian numeric metrics; plus an
    FRW minisuperspace Euler-Lagrange derivation with a free lapse; plus (third check) a
    sympy variation with a fully generic symbolic inverse metric.
  * Asymmetries: polylog closed form (massless FD), Bessel-K series (massive FD/BE),
    cross-checked against tanh-sinh quadrature.
Definitions (QX17 sec 0/1): Q = sqrt(-g^{mn} d_m tau d_n tau), n_m = -d_m tau / Q,
dust term of (A) = 2 mu_K^2 (Q-1)^2 /(4K) = mu_K^2 (Q-1)^2/(2K).
"""
import json
import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 60
rng = np.random.default_rng(20261110)
out = {}

# ---------------------------------------------------------------- Noether current, route 1
def rand_metric():
    while True:
        eta = mp.diag([-1, 1, 1, 1])
        h = mp.matrix(4, 4)
        for i in range(4):
            for j in range(i, 4):
                x = mp.mpf(rng.uniform(-0.35, 0.35))
                h[i, j] = x
                h[j, i] = x
        g = eta + h
        ev = mp.eig(g)[0]
        neg = sum(1 for e in ev if mp.re(e) < 0)
        if neg == 1:
            return g


def current_check(drop_cJ=False, c_on=True, ntrial=8):
    worst = mp.mpf(0)
    worst_ref = mp.mpf(0)
    for _ in range(ntrial):
        g = rand_metric()
        gi = g ** -1
        muK = mp.mpf(rng.uniform(0.5, 2.0))
        K = mp.mpf(rng.uniform(0.5, 2.0))
        c = mp.mpf(rng.uniform(-3, 3)) if c_on else mp.mpf(0)
        J = [mp.mpf(rng.uniform(-1, 1)) for _ in range(4)]
        # timelike covector v = d tau
        while True:
            v = [mp.mpf(1 + rng.uniform(0, 0.6))] + [mp.mpf(rng.uniform(-0.2, 0.2)) for _ in range(3)]
            X = -sum(gi[a, b] * v[a] * v[b] for a in range(4) for b in range(4))
            if X > 0:
                break

        def L(*vv):
            Q = mp.sqrt(-sum(gi[a, b] * vv[a] * vv[b] for a in range(4) for b in range(4)))
            return muK**2 * (Q - 1) ** 2 / (2 * K) + c * sum(vv[a] * J[a] for a in range(4))

        Q = mp.sqrt(X)
        n_low = [-v[a] / Q for a in range(4)]
        n_up = [sum(gi[a, b] * n_low[b] for b in range(4)) for a in range(4)]
        rhoQ = muK**2 * (Q - 1) / K
        for m in range(4):
            orders = [0, 0, 0, 0]
            orders[m] = 1
            jm = mp.diff(L, v, tuple(orders))
            target = rhoQ * n_up[m] + (0 if drop_cJ else c * J[m])
            d = abs(jm - target)
            worst = max(worst, d)
            worst_ref = max(worst_ref, abs(jm))
    return worst, worst_ref

ka1_w, ka1_ref = current_check(c_on=False)
p1_w, p1_ref = current_check()
m2_w, m2_ref = current_check(drop_cJ=True)
out["route1_numeric"] = {"KA1_maxdiff": mp.nstr(ka1_w, 5), "P1_maxdiff": mp.nstr(p1_w, 5),
                         "M2_maxdiff": mp.nstr(m2_w, 5), "scale": mp.nstr(p1_ref, 5)}

# ---------------------------------------------------------------- route 2: generic symbolic inverse metric
v = sp.symbols('v0:4', real=True)
J = sp.symbols('J0:4', real=True)
G = sp.Matrix(4, 4, lambda i, j: sp.Symbol('G%d%d' % (min(i, j), max(i, j)), real=True))
muK, K, c = sp.symbols('mu_K K c_X', positive=True)
X = -sum(G[a, b] * v[a] * v[b] for a in range(4) for b in range(4))
Qs = sp.sqrt(X)
Lsym = muK**2 * (Qs - 1) ** 2 / (2 * K) + c * sum(v[a] * J[a] for a in range(4))
nup = [sum(G[a, b] * (-v[b] / Qs) for b in range(4)) for a in range(4)]
rho = muK**2 * (Qs - 1) / K
sym_P1 = [sp.expand(sp.diff(Lsym, v[m]) - (rho * nup[m] + c * J[m])) for m in range(4)]
sym_M2 = [sp.expand(sp.diff(Lsym, v[m]) - rho * nup[m]) for m in range(4)]
sym_KA1 = [sp.expand(sp.diff(Lsym.subs(c, 0), v[m]) - rho * nup[m]) for m in range(4)]
out["route2_symbolic"] = {"KA1": [str(e) for e in sym_KA1], "P1": [str(e) for e in sym_P1],
                          "M2": [str(e) for e in sym_M2]}

# ---------------------------------------------------------------- route 3: FRW minisuperspace EL with lapse
t = sp.symbols('t', real=True)
tau = sp.Function('tau')(t)
N = sp.Function('N')(t)
a = sp.Function('a')(t)
nX = sp.Function('n_X')(t)
Qf = tau.diff(t) / N
# sqrt(-g) = N a^3; comoving current J^t = n_X / N; d_m tau J^m = tau' n_X / N
Ldens = N * a**3 * (muK**2 * (Qf - 1) ** 2 / (2 * K) + c * tau.diff(t) * nX / N)
el = sp.euler_equations(Ldens, [tau], t)[0].lhs  # = -d/dt (dL/dtau')
pi_tau = sp.diff(Ldens, tau.diff(t))
pi_expected = a**3 * (muK**2 * (Qf - 1) / K + c * nX)
frw_charge_ok = sp.simplify(pi_tau - pi_expected) == 0
# P1's FRW statement: d(a^3 rho_Q)/dt = -c d(a^3 n_X)/dt on shell
rhoQ_f = muK**2 * (Qf - 1) / K
stmt = sp.diff(a**3 * rhoQ_f, t) + c * sp.diff(a**3 * nX, t)
frw_stmt_ok = sp.simplify(stmt + el) == 0  # el = -d/dt pi_tau, so stmt == -el identically
# M2 in FRW: drop c n_X from the momentum
frw_M2 = sp.simplify(pi_tau - a**3 * muK**2 * (Qf - 1) / K)
out["route3_frw"] = {"momentum_is_a3(rhoQ+c nX)": bool(frw_charge_ok),
                     "EL == -[d(a^3 rhoQ)/dt + c d(a^3 nX)/dt]": bool(frw_stmt_ok),
                     "M2_residual": str(frw_M2)}

# KA3: X conserved -> div J = (1/(N a^3)) d/dt (a^3 n_X) = 0 -> a^3 n_X = C
Cc = sp.symbols('C')
divJ = sp.diff(N * a**3 * nX / N, t) / (N * a**3)
ka3_divJ_form = sp.simplify(divJ - sp.diff(a**3 * nX, t) / (N * a**3)) == 0
ka3_change = sp.simplify((-c * sp.diff(a**3 * nX, t)).subs(nX, Cc / a**3).doit())
# also: L_c alone gives tau-equation c * d_m(sqrt(-g) J^m) = c sqrt(-g) div J -> 0 when conserved
elc = sp.euler_equations(a**3 * c * tau.diff(t) * nX, [tau], t)[0].lhs
elc_conserved = sp.simplify(elc.subs(nX, Cc / a**3).doit())
out["KA3"] = {"divJ_form_ok": bool(ka3_divJ_form), "d(a^3 rhoQ)/dt with a^3 nX const": str(ka3_change),
              "Lc-alone tau eq with conserved X": str(elc_conserved)}

# ---------------------------------------------------------------- asymmetries
mp.mp.dps = 32
def asym_series(m, mu, stat):
    """n(mu)-n(-mu), T = 1, g = 1, via Bessel series; needs |mu| < m."""
    s = mp.mpf(0)
    sgn = 1
    for k in range(1, 2000):
        term = mp.sinh(k * mu) * mp.besselk(2, k * m) / k
        s += (sgn if stat == 'FD' else 1) * term
        if stat == 'FD':
            sgn = -sgn
        if abs(term) < mp.mpf(10) ** (-36) and k > 5:
            break
    return m**2 / mp.pi**2 * s

def asym_polylog_FD0(mu):
    return -(mp.polylog(3, -mp.e**mu) - mp.polylog(3, -mp.e**(-mu))) / mp.pi**2

def asym_quad(m, mu, stat):
    sgn = 1 if stat == 'FD' else -1
    def f(p):
        E = mp.sqrt(p * p + m * m)
        return p * p * (1 / (mp.e**(E - mu) + sgn) - 1 / (mp.e**(E + mu) + sgn))
    return mp.quad(f, [0, 1, 5, 20, mp.inf]) / (2 * mp.pi**2)

_cache = {}
def asym(m, mu, stat):
    key = (m, str(mu), stat)
    if key not in _cache:
        _cache[key] = _asym(m, mu, stat)
    return _cache[key]

def _asym(m, mu, stat):
    if stat == 'FD' and m == 0:
        return asym_polylog_FD0(mu)
    if stat == 'BE' and m == 0:
        return mp.mpf(0) if mu == 0 else None  # undefined: pole at p = |mu|
    return asym_series(m, mu, stat)

# KA2: massless FD exact vs numerical integral
ka2 = []
for mu in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5')]:
    exact = mu / 6 + mu**3 / (6 * mp.pi**2)
    num = asym_quad(0, mu, 'FD')
    pl = asym_polylog_FD0(mu)
    ka2.append({"mu": float(mu), "rel_quad": mp.nstr(abs(num / exact - 1), 3),
                "rel_polylog": mp.nstr(abs(pl / exact - 1), 3)})
out["KA2"] = ka2
KA2_pass = all(float(r["rel_quad"]) <= 1e-12 and float(r["rel_polylog"]) <= 1e-12 for r in ka2)

# cross-check series vs quadrature on massive rows
xmax = mp.mpf(0)
for stat in ['FD', 'BE']:
    for m in [1, 5]:
        for mu in [mp.mpf('-0.5'), mp.mpf('0.25'), mp.mpf('0.5')]:
            s1 = asym_series(m, mu, stat)
            s2 = asym_quad(m, mu, stat)
            xmax = max(xmax, abs(s1 / s2 - 1))
out["series_vs_quad_maxrel"] = mp.nstr(xmax, 3)

# BE m=0, mu != 0: show the antiparticle occupation has a pole -> integral diverges
mu_t = mp.mpf('0.2')
eps_list = [mp.mpf(10) ** (-k) for k in (2, 4, 6)]
div = []
for eps in eps_list:
    # integral of p^2/(e^{p-mu}-1) up to mu - eps (for the side with +mu in the "particle" with mu>0)
    val = mp.quad(lambda p: p * p / (mp.e**(p - mu_t) - 1), [0, mu_t - eps])
    div.append(mp.nstr(val, 6))
out["BE_m0_divergence_partial_integrals(mu=0.2, cut eps=1e-2,1e-4,1e-6)"] = div

# ---------------------------------------------------------------- P2 grid
grid = [mp.mpf(-0.5) + mp.mpf(1) * i / 40 for i in range(41)]
rows = [('FD', 0), ('FD', 1), ('FD', 5), ('BE', 0), ('BE', 1), ('BE', 5)]
Q = mp.mpf(1)

def grade(rowlist, flip=False):
    neg = pos = zero = undef = 0
    minval = None
    for stat, m in rowlist:
        for mu in grid:
            cX = mu / Q          # mu_X = c_X Q, both signs of c_X sit on the grid
            n = asym(m, mu, stat)
            if n is None:
                undef += 1
                continue
            if flip:
                n = -n
            val = cX * n
            minval = val if minval is None else min(minval, val)
            if val < 0:
                neg += 1
            elif val == 0:
                zero += 1
            else:
                pos += 1
    if undef == 0 and neg == 0:
        lab = 'DRAINS'
    elif neg > 0:
        lab = 'CREATES'
    else:
        lab = 'UNDECIDED'
    return {"label": lab, "points": neg + pos + zero + undef, "neg": neg, "pos": pos,
            "zero": zero, "undefined": undef, "min_cX_n": mp.nstr(minval, 5)}

P2_frozen = grade(rows)
P2_amended = grade([r for r in rows if r != ('BE', 0)])
M1_frozen = grade(rows, flip=True)
M1_amended = grade([r for r in rows if r != ('BE', 0)], flip=True)
# susceptibility sign check (dn/dmu > 0) on amended rows at mu = 0
chis = {}
for stat, m in [r for r in rows if r != ('BE', 0)]:
    chis[f"{stat} m/T={m}"] = mp.nstr(mp.diff(lambda x: asym(m, x, stat), 0) / 2, 8)
out["P2_frozen"] = P2_frozen
out["P2_amended"] = P2_amended
out["M1_frozen"] = M1_frozen
out["M1_amended"] = M1_amended
out["chi_per_species_dn/dmu_(n-nbar)/2"] = chis

P1_pass = (p1_w < mp.mpf(10) ** -35) and all(e == 0 for e in sym_P1) and frw_charge_ok and frw_stmt_ok
KA1_pass = (ka1_w < mp.mpf(10) ** -35) and all(e == 0 for e in sym_KA1)
M2_bites = (m2_w > mp.mpf(10) ** -3) and any(e != 0 for e in sym_M2) and frw_M2 != 0
KA3_pass = ka3_divJ_form and ka3_change == 0 and elc_conserved == 0

def label(p1, p2):
    if p1 and p2 == 'DRAINS':
        return 'CANNOT FIX 5.41'
    if p1 and p2 == 'CREATES':
        return 'CAN FIX 5.41 IN PRINCIPLE'
    return 'NO VERDICT'

out["grades"] = {"KA1": KA1_pass, "KA2": KA2_pass, "KA3": KA3_pass, "P1": "PASS" if P1_pass else "FAIL",
                 "P2_frozen": P2_frozen["label"], "P2_amended": P2_amended["label"],
                 "TOE0P_frozen": label(P1_pass, P2_frozen["label"]),
                 "TOE0P_amended": label(P1_pass, P2_amended["label"]),
                 "M1_bites(amended->CREATES)": M1_amended["label"] == 'CREATES',
                 "M1_frozen_reading": M1_frozen["label"],
                 "M2_bites(P1 FAIL)": bool(M2_bites)}

# ---------------------------------------------------------------- reported numbers
mp.mp.dps = 30
m_p = mp.mpf('0.93827208816')
cX = mp.mpf('5.41') * m_p
T = mp.mpf(130)
gstar = mp.mpf('106.75')
s_over_ngamma = mp.mpf('7.04')
rep = {"cX_GeV": mp.nstr(cX, 8)}
for Nf in (6, 5):
    def eta_of(c, cubic=False):
        muq = c / 3
        dn_q = 6 * (muq * T**2 / 6 + (muq**3 / (6 * mp.pi**2) if cubic else 0))  # 2 spins x 3 colours
        nB = Nf * dn_q / 3
        s = 2 * mp.pi**2 / 45 * gstar * T**3
        return s_over_ngamma * nB / s
    e_lin = eta_of(cX)
    e_cub = eta_of(cX, cubic=True)
    c_obs = mp.findroot(lambda c: eta_of(c) - mp.mpf('6.1e-10'), mp.mpf('1e-6'))
    rep[f"Nf={Nf}"] = {"eta(cX)": mp.nstr(e_lin, 6), "eta(cX)_with_cubic": mp.nstr(e_cub, 6),
                      "eta/6.1e-10": mp.nstr(e_lin / mp.mpf('6.1e-10'), 5),
                      "cX_for_obs_eta_GeV": mp.nstr(c_obs, 5),
                      "drain_over_rho_b = cX/m_p": mp.nstr(c_obs / m_p, 5)}
out["reported"] = rep

# ---------------------------------------------------------------- illustration (not graded): relaxation ODE
def run(cX_, Gamma, conserved=False):
    # units: a = 1/T, radiation era, H = 1/(2t); chi(T) = chi0 T^2; clock charge rho_Q; mu = cX Q, Q ~ 1
    t0, t1, nst = 1.0, 200.0, 200000
    ts = np.linspace(t0, t1, nst)
    dt = ts[1] - ts[0]
    a_ = lambda tt: np.sqrt(tt)
    A3n = 0.0  # a^3 n_X, zero start
    A3rho0 = 1.0
    chi0 = 1.0
    for tt in ts[:-1]:
        def f(tt, y):
            a3 = a_(tt) ** 3
            Tt = 1 / a_(tt)
            neq = chi0 * Tt**2 * cX_
            return 0.0 if conserved else -Gamma * (y - a3 * neq)
        k1 = f(tt, A3n); k2 = f(tt + dt / 2, A3n + dt * k1 / 2)
        k3 = f(tt + dt / 2, A3n + dt * k2 / 2); k4 = f(tt + dt, A3n + dt * k3)
        A3n += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    A3rho = A3rho0 - cX_ * A3n  # exact first integral of the clock equation
    return A3rho - A3rho0, A3n
ill = {}
for cc in (0.3, -0.3):
    for G_ in (0.05, 5.0):
        d, n = run(cc, G_)
        ill[f"c={cc},Gamma={G_}"] = {"Delta(a^3 rhoQ)": d, "a^3 nX final": n}
    d, n = run(cc, 1.0, conserved=True)
    ill[f"c={cc},conserved"] = {"Delta(a^3 rhoQ)": d, "a^3 nX final": n}
out["illustration_relaxation"] = ill

print(json.dumps(out, indent=1, default=str))
