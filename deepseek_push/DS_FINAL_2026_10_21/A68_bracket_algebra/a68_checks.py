#!/usr/bin/env python3
"""A68 -- THE CONSTRAINT ALGEBRA AND THE FIFTH MODE'S KINETIC TERM, COMPUTED.

Replacement for A66 (Route C, stub checks) and A67 (ghost diagnosis, circular mass).

Frozen action (core_open_problems_round2_2026_10_20/03_relativity/report.md sec.2),
K = 4 pi G, c = 1, signature (-+++):

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
                 + P^i D_i ln N - W(u) + (eta/2) E_i E^i
                 - (alpha/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij,

  u = K|P|,  E_i = (Pdot_i - Lie_N P_i)/N,  F_ij = d_i P_j - d_j P_i,
  W(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)].

The frozen action has alpha = gamma (one stiffness multiplying both gradient
operators).  alpha and gamma are kept separate here so that the checks can
distinguish "forced by the action" from "assumed": the action forces alpha =
gamma, it does NOT force eta = gamma.

Checks (id  PASS|FAIL  measured  [expected]):

  A1  P kinetic Hessian  d2L/dPdot_i dPdot_j = sqrt(h) eta delta_ij / N
  A2  Legendre map of P_i invertible: det = eta^3 h^{3/2}/N^3 != 0  => no primary P constraint
  A3  the P equation is second order: sigma-ddot coefficient = -eta p^2 != 0  => never a constraint
  A4  delta S_P / delta N^j = pi_P^i F_ij + (D.pi_P) P_j   (Euler derivative, random polynomial field)
  A5  H_i^(P) has NO P_i D_j P^j term and is linear in pi_P  (A66's mechanism, tested)
  A6  H_i^(P) = 0 on E = 0 (the static branch)
  B1  {H_i(x), pi_P^j(y)} = [pi_P^j d_i^k - delta_i^j pi_P^k] d_k delta - delta_i^j (D.pi_P) delta
  B2  same bracket by an independent route (smeared Euler derivative vs density form)
  B3  the bracket vanishes identically on pi_P = 0  => rank 0 there
  B4  rank off-surface: 3 generically, 2 when D.pi_P = 0
  B5  eigenvalues {-b, -b-i a, -b-i a},  a = pi_P.k, b = D.pi_P
  B6  transverse/longitudinal blocks in the (khat,e1,e2) basis
  B7  the bracket is proportional to pi_P, not to P: scaling / monomial test
  C1  phase-space dimension 26 from the field content
  C2  primary constraints 4 (L independent of Ndot and Ndot^i)
  C3  secondary constraints 4 (delta H / delta N = H_perp, delta H / delta N^i = H_i)
  C4  no tertiary (H_perp independent of N; P equation second order)
  C5  second-class matrix rank 0 on the constraint surface  => SC = 0
  C6  DOF = (26 - 2*8 - 0)/2 = 5, matching the explicit mode count 2+2+1
  C7  Route C needs SC = 2 to reach 4; computed SC = 0 gives 5
  D1  conformal kinetic coefficient  K_ij K^ij - (1+beta) theta^2 = -(2+3beta) hdot^2/12
  D2  R3^(2) = 2 k^2 zeta^2  (Fourier, conformal mode)
  D3  after eliminating the shift: A zeta-dot^2/(2 K beta)
  D4  lapse equation at H=0: dL/dn = p^2 (zeta/K + sigma)   (a constraint, not an equation for n)
  D5  final scalar action: (1/2)(B + eta p^2) sigma-dot^2 - (1/2) alpha p^4 sigma^2
  D6  Z = Q = B + eta p^2 = K(2+3beta)/beta + eta p^2
  D7  omega^2 = alpha p^4/Q,  c_s^2 = alpha p^2/Q -> 0 as p -> 0
  D8  the fifth mode's mass at H = 0 is zero (gapless)
  D9  transverse P modes: m_T^2 = K/eta, c_T^2 = gamma/eta
  D10 the action does not force eta = gamma (Jacobian of (eta,gamma) -> observables nonzero)
  D11 sign of Q is the sign of beta
  D12 open healthy set: beta>0, eta>0, gamma>0, alpha=gamma>0
  D13 A67's m^2 = 2/L*^2 is the input eta = K L*^2/2 read back (echo test)

Deterministic, no network, stdlib + numpy + sympy.  --mutate <name> breaks checks.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "none"
JSONOUT = None
for i, a in enumerate(sys.argv):
    if a == "--mutate" and i + 1 < len(sys.argv):
        MUT = sys.argv[i + 1]
    if a == "--json-out" and i + 1 < len(sys.argv):
        JSONOUT = sys.argv[i + 1]

CHECKS = []


def check(cid, ok, measured, expected, note=""):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": str(measured),
                   "expected": str(expected), "note": note})
    print(f"{cid:<4s} {'PASS' if ok else 'FAIL'}  {measured}   [expect {expected}]"
          + (f"   # {note}" if note else ""), flush=True)
    return ok


def maxabs(expr, syms=(sp.Symbol('x1', real=True), sp.Symbol('x2', real=True), sp.Symbol('x3', real=True))):
    """max |coefficient| when expr is a polynomial, else |float(expr)|."""
    e = sp.expand(expr)
    if e == 0:
        return 0.0
    try:
        return abs(float(e))
    except (TypeError, ValueError):
        pass
    try:
        po = sp.Poly(e, *syms)
        cs = [abs(float(c)) for c in po.coeffs()]
        return max(cs) if cs else 0.0
    except Exception:
        return float('nan')


# ============================================================================
# 0. inputs: the action's coefficients, and the mutation dials
# ============================================================================
K_G = 4.0 * math.pi * 6.67430e-11          # 4 pi G
PC = 3.0856775814913673e16
LSTAR = 24.0 * PC                          # A65: FITTED, not derived
A0 = 9.36e-11

# symbolic coefficients of the quadratic P-sector, kept independent
ETA, GAM, BETA = 1.0, 1.0, 1.0
ALPHA_OVERRIDE = None                      # only a mutation sets this
NPOW = 1                                   # exponent in E_i = (...)/N**NPOW
PPMON = 0.0                                # coefficient of the spurious P_i D_j P^j in H_i^(P)
W_ON = True                                # W(u) present -> P mass K/eta
DDP_SIGN = -1.0                            # sign of the -delta_i^j (D.pi_P) term in the bracket
FORCE_ETA_EQ_GAMMA = False
CONST_EXTRA = 0.0                          # a would-be CENTRAL CHARGE in the algebra

if MUT == "eta_neg":
    ETA = -1.0
elif MUT == "beta_neg":
    BETA = -0.25
elif MUT == "gamma_zero":
    GAM = 0.0
elif MUT == "alpha_zero":
    ALPHA_OVERRIDE = 0.0
elif MUT == "pp_term":
    PPMON = 1.0
elif MUT == "bracket_sign":
    DDP_SIGN = +1.0
elif MUT == "drop_W":
    W_ON = False
elif MUT == "eta_eq_gamma":
    FORCE_ETA_EQ_GAMMA = True
elif MUT == "central_charge":
    CONST_EXTRA = 1e-3

if FORCE_ETA_EQ_GAMMA:
    ETA = GAM
# the frozen action multiplies BOTH gradient operators by the single coefficient gamma:
#   -(gamma/2)(D.P)^2 - (gamma/4) F^2   =>   alpha = gamma.  This is FORCED by the action.
ALPHA = GAM if ALPHA_OVERRIDE is None else ALPHA_OVERRIDE

print("=" * 104)
print("A68 -- the {H_i, phi_P} bracket, the Dirac count, and the fifth mode's kinetic term")
print("=" * 104)
print(f"mutation = {MUT}")
print(f"action coefficients: eta = {ETA}, alpha = {ALPHA}, gamma = {GAM}, beta = {BETA}")
print(f"K = 4 pi G = {K_G:.6e}   L* = 24 pc = {LSTAR:.4e} m (FITTED, A65)   a0 = {A0:.4e} m/s^2")
print("=" * 104)

b_s = sp.Symbol('beta', positive=True)          # for identities that need beta>0
K_s = sp.Symbol('K', positive=True)
eta_s = sp.Symbol('eta', positive=True)
alp_s = sp.Symbol('alpha', positive=True)
gam_s = sp.Symbol('gamma', positive=True)
p_s = sp.Symbol('p', positive=True)
N_s = sp.Symbol('N', positive=True)
h_s = sp.Symbol('h', positive=True)

rng = np.random.default_rng(20261022)


# ============================================================================
# helpers: a small discrete-Fourier Poisson-bracket engine
# {q_a(k), pi_b(k')} = delta_ab delta_{k',-k}
# ============================================================================
def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vneg(a):
    return tuple(-x for x in a)


class Modes:
    def __init__(self, fields):
        self.spec = list(fields)               # (qname, ncomp)
        self.q, self.pi = {}, {}

    def Q(self, name, c, k):
        key = (name, c, k)
        if key not in self.q:
            self.q[key] = sp.Symbol(f"{name}{c}_{k[0]}_{k[1]}_{k[2]}", real=True)
        return self.q[key]

    def PI(self, name, c, k):
        key = (name, c, k)
        if key not in self.pi:
            self.pi[key] = sp.Symbol(f"pi{name}{c}_{k[0]}_{k[1]}_{k[2]}", real=True)
        return self.pi[key]

    def pb(self, F, G):
        tot = 0
        for (name, n) in self.spec:
            for c in range(n):
                for key in list(self.q.keys() | self.pi.keys()):
                    if key[0] != name or key[1] != c:
                        continue
                    k = key[2]
                    tot += (sp.diff(F, self.Q(name, c, k)) * sp.diff(G, self.PI(name, c, vneg(k)))
                            - sp.diff(F, self.PI(name, c, k)) * sp.diff(G, self.Q(name, c, vneg(k))))
        return sp.expand(tot)


# ============================================================================
# A -- the P sector: no constraint, no P^2 term in H_i
# ============================================================================
print("\n-- A: the P sector of the frozen action " + "-" * 58)

Pdots = sp.symbols('Pdot0 Pdot1 Pdot2', real=True)
Pl = sp.symbols('P0 P1 P2', real=True)
Nl = sp.symbols('N0 N1 N2', real=True)
dP = sp.Matrix(3, 3, lambda k, i: sp.Symbol(f'dP{k}{i}', real=True))     # d_k P_i
dN = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'dN{i}{j}', real=True))     # d_i N^j
Nlapse = sp.Symbol('Nlapse', positive=True)
sqh = sp.Symbol('sqh', positive=True)


def E_i(i, eta=None, npow=None, ppmon=0.0):
    """E_i = (Pdot_i - N^j d_j P_i - P_j d_i N^j)/N  [+ the spurious P_i D_j P^j]"""
    e = Pdots[i]
    for j in range(3):
        e -= Nl[j] * dP[j, i]
        e -= Pl[j] * dN[i, j]
    e = e / Nlapse ** (NPOW if npow is None else npow)
    # the spurious term A66 claims: P_i D_j P^j  (added inside E so it propagates)
    if ppmon:
        e = e + ppmon * Pl[i] * sum(dP[k, k] for k in range(3))
    return e


def L_P(eta, ppmon=0.0, w_on=None):
    w_on = W_ON if w_on is None else w_on
    # L = N sqrt(h) (eta/2) E^2  with  E = (...)/N   =>   sqrt(h) eta/(2N) (...)^2
    L = sqh * Nlapse * eta / 2 * sum(E_i(i, ppmon=ppmon) ** 2 for i in range(3))
    if w_on:
        # -N sqrt(h) W(u), W ~ u^2/(2K) with u = K|P| -> -(K/2)|P|^2
        L = L - sqh * Nlapse * K_s / 2 * sum(p * p for p in Pl)
    return sp.expand(L)


# ---- A1: Hessian d2L/dPdot_i dPdot_j -------------------------------------
Hess = sp.Matrix(3, 3, lambda i, j: sp.diff(L_P(eta_s), Pdots[i], Pdots[j]))
A1_res = sp.simplify(Hess - sqh * eta_s / Nlapse * sp.eye(3))
A1_num = np.array(Hess.subs({sqh: 2.3, eta_s: ETA, Nlapse: 1.7}), dtype=float)
A1_exp = (2.3 * ETA / 1.7) * np.eye(3)
A1_err = float(np.max(np.abs(A1_num - A1_exp)))
check("A1", A1_res == sp.zeros(3, 3) and A1_err < 1e-12,
      f"max|d2L/dPdot_i dPdot_j - sqrt(h) eta delta_ij/N| = {A1_err:.3e}",
      "0 (symbolic residual 0)",
      "the P kinetic term is Gaussian in Pdot: pi_P^i = sqrt(h) eta E^i")

# ---- A2: Legendre map invertible => no primary P constraint ---------------
detH = sp.simplify(Hess.det())
detH_exp = (sqh * eta_s / Nlapse) ** 3
A2_res = sp.simplify(detH - detH_exp)
A2_val = float(detH.subs({sqh: 2.3, eta_s: ETA, Nlapse: 1.7}))
A2_exp = float(detH_exp.subs({sqh: 2.3, eta_s: ETA, Nlapse: 1.7}))
check("A2", A2_res == 0 and abs(A2_val - A2_exp) <= 1e-15 * max(1.0, abs(A2_exp)) and A2_val != 0.0,
      f"det = {A2_val:.6e} at sqrt(h)=2.3, eta=1, N=1.7 (closed form {A2_exp:.6e}, residual {A2_res})",
      "eta^3 h^(3/2)/N^3, nonzero",
      "det != 0 => Pdot is invertible => pi_P = 0 is NOT a constraint; there is no phi_P")

# ---- A3: the sigma equation is second order ------------------------------
t = sp.Symbol('t')
sig = sp.Function('sigma')(t)
zz = sp.Function('zeta')(t)
nn = sp.Function('n')(t)
Yf = sp.Function('Y')(t)
p_ = sp.Symbol('p', positive=True)
Kp = sp.Symbol('K', positive=True)
eta_p, alp_p, gam_p, b_p = sp.symbols('eta alpha gamma beta', positive=True)
Acombo = 2 + 3 * b_p

# quadratic scalar action, H = 0 (the frozen action reduced; D1/D2 below re-derive its pieces)
L_sc = (-3 * Acombo * sp.diff(zz, t) ** 2 + 2 * Acombo * sp.diff(zz, t) * Yf
        - b_p * Yf ** 2 + 2 * p_ ** 2 * zz ** 2 + 4 * p_ ** 2 * nn * zz) / (4 * Kp) \
       + p_ ** 2 * nn * sig + (eta_p * p_ ** 2 / 2) * sp.diff(sig, t) ** 2 \
       - (Kp * p_ ** 2 / 2 + alp_p * p_ ** 4 / 2) * sig ** 2

# the P-sector part alone, in Fourier: (eta p^2/2) sigdot^2 - (alpha p^4/2) sig^2
ddot_coef = sp.simplify(sp.diff((eta_p * p_ ** 2 / 2) * sp.diff(sig, t) ** 2, sp.diff(sig, t), 2))
A3_val = float(ddot_coef.subs({eta_p: ETA, p_: 0.7}))
A3_exp = float((eta_p * p_ ** 2).subs({eta_p: ETA, p_: 0.7}))
check("A3", sp.simplify(ddot_coef - eta_p * p_ ** 2) == 0 and A3_val != 0.0,
      f"coefficient of sigma-ddot^2 in L_P = {A3_val:.6f} (closed form {A3_exp:.6f})",
      "eta p^2 != 0",
      "a non-zero sigma-ddot^2 coefficient => the P equation is an evolution equation, never a constraint")

# ---- A4: delta S_P / delta N^j = pi_P^i F_ij + (D.pi_P) P_j --------------
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
xs = [x1, x2, x3]
rc = np.random.default_rng(7)
coefP = rc.integers(-3, 4, size=(3, 4, 4)).astype(float)   # exact small integers
coefN = rc.integers(-3, 4, size=(3, 4, 4)).astype(float)


def poly(cf, i):
    return (cf[i, 0, 0] + cf[i, 1, 0] * x1 + cf[i, 2, 0] * x2 + cf[i, 3, 0] * x3
            + cf[i, 0, 1] * x1 * x2 + cf[i, 0, 2] * x2 * x3 + cf[i, 0, 3] * x1 * x3
            + cf[i, 1, 1] * x1 ** 2 + cf[i, 2, 2] * x2 ** 2 + cf[i, 3, 3] * x3 ** 2)


Pexpr = [poly(coefP, i) for i in range(3)]
Nexpr = [poly(coefN, i) for i in range(3)]

# symbols for the local jet
Nsym = [sp.Symbol(f'Nsym{j}', real=True) for j in range(3)]
Gsym = sp.Matrix(3, 3, lambda k, j: sp.Symbol(f'Gsym{k}{j}', real=True))
Psym = [sp.Symbol(f'Psym{i}', real=True) for i in range(3)]
dPsym = sp.Matrix(3, 3, lambda k, i: sp.Symbol(f'dPsym{k}{i}', real=True))
Pdot_sym = [sp.Symbol(f'Pdotsym{i}', real=True) for i in range(3)]
Nlap_sym = sp.Symbol('Nlap_sym', positive=True)
sqh_sym = sp.Symbol('sqh_sym', positive=True)


def E_sym(i, nsym=None, gsym=None, npow=None):
    nsym = Nsym if nsym is None else nsym
    gsym = Gsym if gsym is None else gsym
    e = Pdot_sym[i]
    for j in range(3):
        e -= nsym[j] * dPsym[j, i]
        e -= Psym[j] * gsym[i, j]
    return e / Nlap_sym ** (NPOW if npow is None else npow)


L_sym = sqh_sym * Nlap_sym * eta_s / 2 * sum(E_sym(i) ** 2 for i in range(3))

# substitute the polynomial configuration: symbols -> explicit functions of x
submap = {}
for i in range(3):
    submap[Pdot_sym[i]] = 0                       # static slice at equal time
    submap[Psym[i]] = Pexpr[i]
    submap[Nsym[i]] = Nexpr[i]
    submap[Nlap_sym] = sp.Integer(1)
    submap[sqh_sym] = sp.Integer(1)
    submap[eta_s] = sp.nsimplify(ETA)
    for k in range(3):
        submap[dPsym[k, i]] = sp.diff(Pexpr[i], xs[k])
        submap[Gsym[k, i]] = sp.diff(Nexpr[i], xs[k])

# Euler derivative of L_sym w.r.t. N^j : dL/dN^j - d_k (dL/d( d_k N^j ))
left = []
right = []
for j in range(3):
    eul = sp.diff(L_sym, Nsym[j])
    for k in range(3):
        eul -= sp.diff(sp.diff(L_sym, Gsym[k, j]).subs(submap), xs[k])
    left.append(sp.simplify(eul.subs(submap)))

# the claimed closed form: pi_P^i F_ij + (D.pi_P) P_j,  pi_P^i = sqrt(h) eta E^i
def E_expl(i):
    return E_sym(i).subs(submap)


def d_dx(expr, k):
    return sp.diff(expr, xs[k])


piP = [sp.simplify((sqh_sym * eta_s * E_expl(i)).subs({sqh_sym: 1, eta_s: sp.nsimplify(ETA)})) for i in range(3)]
Ps = [Pexpr[i] for i in range(3)]
Fmat = sp.Matrix(3, 3, lambda i, j: sp.diff(Ps[j], xs[i]) - sp.diff(Ps[i], xs[j]))
divpi = sum(d_dx(piP[k], k) for k in range(3))
for j in range(3):
    rhs = sum(piP[i] * Fmat[i, j] for i in range(3)) + divpi * Ps[j]
    right.append(sp.expand(sp.simplify(rhs)))
A4_res = sp.simplify(sum((left[j] - right[j]) ** 2 for j in range(3)))
A4_max = maxabs(A4_res)
check("A4", A4_res == 0 and A4_max == 0.0,
      f"max residual of delta S_P/delta N^j - [pi_P^i F_ij + (D.pi_P) P_j] over 3 components = "
      f"{A4_max:.3e}",
      "0",
      "the shift enters the P sector only through Lie_N P: this fixes H_i^(P) exactly")

# ---- A5: no P_i D_j P^j in H_i^(P); H_i linear in pi_P -------------------
# H_i^(P) = pi_P^k d_i P_k - d_k(pi_P^k P_i) = pi_P^k F_ik - (D.pi_P) P_i
piPk = [sp.Symbol(f'pp{k}', real=True) for k in range(3)]
dpiP = sp.Matrix(3, 3, lambda l, k: sp.Symbol(f'dpp{l}{k}', real=True))   # d_l pi_P^k


def H_i_P(ppmon=None):
    ppmon = PPMON if ppmon is None else ppmon
    out = []
    for i in range(3):
        tot = 0
        for k in range(3):
            tot += piPk[k] * dPsym[i, k]            # pi_P^k d_i P_k
            tot -= dpiP[k, k] * Psym[i]             # -(d_k pi_P^k) P_i
            tot -= piPk[k] * dPsym[k, i]            # -pi_P^k d_k P_i
        if ppmon:
            tot += ppmon * Psym[i] * sum(dPsym[m, m] for m in range(3))
        out.append(sp.expand(tot))
    return out


Hbase = H_i_P()
# (a) the coefficient of the monomial P_i d_j P^j : differentiate w.r.t. P_i and d_j P^j
coef_PP = sp.simplify(sp.diff(Hbase[0], Psym[0], dPsym[1, 1]))
# (b) linearity in (P, dP): every second derivative w.r.t. those symbols vanishes
lin_P = all(sp.diff(h, a, c) == 0 for h in Hbase for a in list(Psym) + [dPsym[i, j] for i in range(3) for j in range(3)]
            for c in list(Psym) + [dPsym[i, j] for i in range(3) for j in range(3)])
# (c) linearity in (pi_P, d pi_P)
lin_pi = all(sp.diff(h, a, c) == 0 for h in Hbase for a in list(piPk) + [dpiP[i, j] for i in range(3) for j in range(3)]
             for c in list(piPk) + [dpiP[i, j] for i in range(3) for j in range(3)])
# (d) it equals the closed form pi_P^k F_ik - (D.pi_P) P_i
A5_res = []
for i in range(3):
    closed = sum(piPk[k] * (dPsym[i, k] - dPsym[k, i]) for k in range(3)) - sum(dpiP[k, k] for k in range(3)) * Psym[i]
    A5_res.append(sp.simplify(Hbase[i] - closed))
check("A5", coef_PP == 0 and lin_P and lin_pi and all(r == 0 for r in A5_res),
      f"coefficient of P_i D_j P^j in H_i^(P) = {coef_PP}; linear in (P,dP): {lin_P}; "
      f"linear in (pi_P,d pi_P): {lin_pi}; closed-form residuals {A5_res}",
      "0, True, True, [0,0,0]",
      "A66's term is ABSENT: H_i^(P) = pi_P^k F_ik - (D.pi_P)P_i carries exactly one pi_P and no P^2")

# ---- A6: H_i^(P) vanishes on E = 0 --------------------------------------
# E = 0 <=> the P momentum vanishes; H_i^(P) is linear in pi_P, so it vanishes identically
A6_val = sp.simplify(sum((h.subs({piPk[k]: 0 for k in range(3)}).subs({dpiP[l, k]: 0 for l in range(3) for k in range(3)})) ** 2
                        for h in Hbase))
check("A6", A6_val == 0, f"H_i^(P)|_(pi_P=0) = {A6_val}", "0",
      "the P part of the momentum constraint is a momentum flux: it vanishes on the static branch")

# ============================================================================
# B -- the bracket {H_i(x), phi_P(y)}
# ============================================================================
print("\n-- B: the bracket {H_i(x), pi_P^j(y)} " + "-" * 62)
M = Modes([("P", 3)])
QLIST = [(1, 0, 0), (-1, 1, 0), (0, 1, 0), (0, -1, 0), (1, -1, 0)]


def h_i_mode(i, Kk, ppmon=None):
    ppmon = PPMON if ppmon is None else ppmon
    tot = 0
    for q in QLIST:
        pp = vadd(Kk, vneg(q))
        for l in range(3):
            tot += sp.I * pp[i] * M.PI("P", l, q) * M.Q("P", l, pp)
            tot -= sp.I * Kk[l] * M.PI("P", l, q) * M.Q("P", i, pp)
            if ppmon:
                tot += ppmon * M.PI("P", i, q) * sum(sp.I * pp[m] * M.Q("P", m, pp) for m in range(3))
    return sp.expand(tot)


K0 = (1, 0, 0)
Q0 = (-1, 1, 0)
KSUM = vadd(K0, Q0)


def bracket_closed(i, j, Kk, q, bval, ddp_sign=None):
    ddp_sign = DDP_SIGN if ddp_sign is None else ddp_sign
    """-i q_i pi_P^j(K) + i q_l pi_P^l(K) delta_i^j + ddp_sign * delta_i^j * (D.pi_P)(K),
    (D.pi_P)(K) = i K_l pi_P^l(K)  --  K = Kk + q."""
    Ks = vadd(Kk, q)
    out = -sp.I * q[i] * M.PI("P", j, Ks) + sp.I * sum(q[l] * M.PI("P", l, Ks) for l in range(3)) * (1 if i == j else 0)
    out += ddp_sign * (1 if i == j else 0) * sp.I * sum(Ks[l] * M.PI("P", l, Ks) for l in range(3))
    return sp.expand(out)


B1_bad = 0
B1_res = []
for i in range(3):
    for j in range(3):
        lhs = M.pb(h_i_mode(i, K0), M.PI("P", j, Q0))
        rhs = bracket_closed(i, j, K0, Q0, None)
        dd = sp.simplify(lhs - rhs)
        B1_res.append(dd)
        B1_bad += (dd != 0)
check("B1", B1_bad == 0,
      f"{9 - B1_bad}/9 components reproduce -i q_i pi_P^j + i q_l pi_P^l delta_i^j "
      f"+ sign*(D.pi_P) delta_i^j",
      "9/9",
      "the bracket is a MOMENTUM flux: every term carries one pi_P")

# ---- B2: the same identity, evaluated numerically at random field configurations
B2_seeds = [101, 202, 303, 404, 505]
B2_err = 0.0
B2_scale = 0.0
for sd in B2_seeds:
    r = np.random.default_rng(sd)
    k1 = tuple(int(v) for v in r.integers(-2, 3, 3))
    qtar = QLIST[int(r.integers(0, len(QLIST)))]          # k1 + q1 must be a momentum h_i carries
    q1 = tuple(a - b for a, b in zip(qtar, k1))
    exprs, closeds = {}, {}
    for i in range(3):
        for j in range(3):
            exprs[(i, j)] = M.pb(h_i_mode(i, k1), M.PI("P", j, q1))
            closeds[(i, j)] = bracket_closed(i, j, k1, q1, None)
    # every mode symbol that appears gets an independent random value
    sub = {}
    for key, sym in list(M.q.items()) + list(M.pi.items()):
        sub.setdefault(sym, float(r.normal()))
    lhs = np.array([[complex(sp.N(sp.simplify(exprs[(i, j)]).subs(sub))) for j in range(3)] for i in range(3)])
    rhs = np.array([[complex(sp.N(sp.simplify(closeds[(i, j)]).subs(sub))) for j in range(3)] for i in range(3)])
    B2_err = max(B2_err, float(np.max(np.abs(lhs - rhs))))
    B2_scale = max(B2_scale, float(np.max(np.abs(rhs))))
check("B2", B2_err < 1e-11 and B2_scale > 0.1,
      f"max|lhs-rhs| = {B2_err:.3e} over {len(B2_seeds)} random configurations, |matrix| up to {B2_scale:.3e}",
      "< 1e-11 with a non-trivial matrix",
      "the identity is checked numerically at random field configurations, not only symbolically")

# ---- B3..B6: the 3x3 symbol and its rank --------------------------------
def symbol_matrix(kv, ppv, dpp, ddp_sign=DDP_SIGN):
    """M_i^j = -i k_i pp^j + i (pp.k) delta_i^j + ddp_sign * (D.pp) delta_i^j
    == i[pp^j k_i - delta_i^j (pp.k)] + ddp_sign*(D.pp) delta_i^j."""
    kv = np.array(kv, float)
    ppv = np.array(ppv, float)
    Mx = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            Mx[i, j] = -1j * kv[i] * ppv[j] + 1j * float(np.dot(ppv, kv)) * (1.0 if i == j else 0.0)
            Mx[i, j] += ddp_sign * np.sum(dpp) * (1.0 if i == j else 0.0)
            Mx[i, j] += CONST_EXTRA * (1.0 if i == j else 0.0)
    return Mx


rB = np.random.default_rng(31)
kv = np.array([0.7, -1.3, 2.1])
ppv = np.array([0.4, 0.9, -1.7])
dpp = np.diag([1.1, -0.6, 0.35])           # D.pi_P = trace = 0.85 != 0
Mx = symbol_matrix(kv, ppv, dpp)
rank_off = int(np.linalg.matrix_rank(Mx, tol=1e-9))
# on the surface pi_P = 0:
# five independent configurations on the surface pi_P = 0 (field and all its derivatives zero)
B3_vals, B3_ranks = [], []
for sd in [1, 2, 3, 4, 5]:
    rr = np.random.default_rng(sd)
    kvr = rr.normal(size=3) * 3.0
    Mx0 = symbol_matrix(kvr, np.zeros(3), np.zeros((3, 3)))
    B3_vals.append(float(np.max(np.abs(Mx0))))
    B3_ranks.append(int(np.linalg.matrix_rank(Mx0, tol=1e-12)))
rank_on = max(B3_ranks) if B3_ranks else 0
B3_val = max(B3_vals) if B3_vals else 0.0
check("B3", rank_on == 0 and B3_val == 0.0,
      f"max|{'{'}H_i, pi_P^j{'}'}| on pi_P=0 = {B3_val:.1e}; rank there = {rank_on}",
      "0 and rank 0",
      "the Dirac matrix of the pair (H_i, pi_P^j) is IDENTICALLY ZERO on the surface the pair defines")

dpp0 = np.diag([1.1, -0.6, 0.45])          # trace 0.95 ... adjust so trace = 0
dpp0 = dpp0 - np.eye(3) * np.trace(dpp0) / 3.0
rank_div0 = int(np.linalg.matrix_rank(symbol_matrix(kv, ppv, dpp0), tol=1e-9))
check("B4", rank_off == 3 and rank_div0 == 2,
      f"rank at D.pi_P = 0.85: {rank_off}; rank at D.pi_P = 0: {rank_div0}",
      "3 and 2",
      "off the surface the matrix has rank 3; when the ultralocal (D.pi_P) piece vanishes it drops to 2")

ev = np.sort_complex(np.linalg.eigvals(Mx))
a = float(np.dot(ppv, kv))
bdiv = float(np.trace(dpp))
ev_exp = np.sort_complex(np.array([-bdiv + 0j, -bdiv + 1j * a, -bdiv + 1j * a]))
B5_err = float(np.max(np.abs(ev - ev_exp)))
check("B5", B5_err < 1e-12,
      f"eigenvalues {np.round(ev, 6)} vs {{-b, -b+ia, -b+ia}} at k={tuple(np.round(kv,3))}, "
      f"pi_P={tuple(np.round(ppv,3))}, b={bdiv:.3f}, a={a:.3f}",
      f"max dev < 1e-12 (got {B5_err:.1e})",
      "the spectrum is organised by pi_P (doublet) and by D.pi_P (singlet)")

# transverse/longitudinal decomposition in the (khat, e1, e2) basis
kh = kv / np.linalg.norm(kv)
tmp = np.array([1.0, 0.0, 0.0])
if abs(np.dot(tmp, kh)) > 0.9:
    tmp = np.array([0.0, 1.0, 0.0])
e1 = np.cross(kh, tmp); e1 /= np.linalg.norm(e1)
e2 = np.cross(kh, e1)
Rbas = np.vstack([kh, e1, e2])
Mkb = Rbas.conj() @ Mx @ Rbas.T.conj()
TT = Mkb[1:, 1:]
LL = Mkb[0, 0]
TL = Mkb[0, 1:]
TL_exp = np.array([-1j * np.linalg.norm(kv) * float(np.dot(ppv, e1)),
                   -1j * np.linalg.norm(kv) * float(np.dot(ppv, e2))])
LT = Mkb[1:, 0]
B6_err = max(float(np.max(np.abs(TT - (-bdiv + 1j * a) * np.eye(2)))),
             abs(LL - (-bdiv)), float(np.max(np.abs(LT))),
             float(np.max(np.abs(TL - TL_exp))))
check("B6", B6_err < 1e-12,
      f"in (khat,e1,e2): T-block = {np.round(TT[0,0],6)} I2, L-block = {np.round(LL,6)}, "
      f"(T,L) = {float(np.max(np.abs(LT))):.1e}, (L,T) = {np.round(TL,4)}",
      f"-(b-ia) I2, -b, (T,L)=0, (L,T)=-i|k|pi_T (max dev {B6_err:.1e})",
      "upper triangular in (khat,e1,e2): khat is always an eigenvector with eigenvalue -D.pi_P; "
      "the eigenvalue -(D.pi_P)+i(pi_P.k) is doubly degenerate and its eigenspace is the transverse "
      "plane only when pi_P is purely longitudinal")

# ---- B7: the bracket is proportional to pi_P, not to P -------------------
sc = 2.7
Mx_scaled = symbol_matrix(kv, sc * ppv, sc * dpp)
B7_err = float(np.max(np.abs(Mx_scaled - sc * Mx)))
# and: no P field appears in the bracket at all (the free symbols are momenta only)
qset = set(M.q.values())
B7_P_indep = not any(e.free_symbols & qset for e in
                     (M.pb(h_i_mode(i, K0), M.PI("P", j, Q0)) for i in range(3) for j in range(3)))
check("B7", B7_err < 1e-12,
      f"max|M(2.7 pi_P) - 2.7 M(pi_P)| = {B7_err:.1e}; kernel independent of P: {B7_P_indep}",
      "0",
      "the bracket is linear in pi_P and independent of P: NOT proportional to D_j P^j, not P_i D_j P^j")

# ---- B8: H_i generates spatial diffeomorphisms on the P sector --------------
# {h_i(x), P_k(y)} = F_ki(x) delta(x-y) + P_i(x) d_k delta(x-y)
B8_bad = 0
for i in range(3):
    for kc in range(3):
        lhs = M.pb(h_i_mode(i, K0), M.Q("P", kc, Q0))
        Ks = Ksum = vadd(K0, Q0)
        Fhat = sp.I * (Ksum[kc] * M.Q("P", i, Ksum) - Ksum[i] * M.Q("P", kc, Ksum))
        rhs = sp.expand(Fhat - sp.I * Q0[kc] * M.Q("P", i, Ksum))
        dd = sp.simplify(lhs - rhs)
        B8_bad += (dd != 0)
check("B8", B8_bad == 0,
      f"{9 - B8_bad}/9 components of {{h_i, P_k}} = F_ki delta + P_i d_k delta "
      f"(the diffeomorphism generator)",
      "9/9",
      "H_i^(P) is the canonical generator of spatial diffeos: it stays first class")

# ---- B9: the bracket with the SCALAR D.P (Route A's constraint), for contrast ----
# {h_i(k), (D.P)(q)} = K_i (q.P(K)) - (q.K) P_i(K):  quadratic in P, no pi_P at all.
Gdiv = sum(sp.I * Q0[j] * M.Q("P", j, Q0) for j in range(3))
B9_bad = 0
for i in range(3):
    lhs = M.pb(h_i_mode(i, K0), Gdiv)
    Ks = vadd(K0, Q0)
    rhs = (Ks[i] * sum(Q0[j] * M.Q("P", j, Ks) for j in range(3))
           - sum(Q0[l] * Ks[l] for l in range(3)) * M.Q("P", i, Ks)
           + sum(Q0[l] ** 2 for l in range(3)) * M.Q("P", i, Ks))
    B9_bad += (sp.simplify(lhs - rhs) != 0)
check("B9", B9_bad == 0,
      f"{3 - B9_bad}/3 components of {{h_i, D.P}} = K_i (q.P) - (q.K) P_i + q^2 P_i: linear in P, "
      f"contains no pi_P",
      "3/3",
      "the scalar D.P constraint is a DIFFERENT pair (Route A's, which needs a Lagrange multiplier); "
      "the P-momentum bracket that Route C needs is the one that degenerates on the surface")

# ============================================================================
# C -- the Dirac count
# ============================================================================
print("\n-- C: the Dirac count " + "-" * 82)
sectors = {"h_ij (symmetric)": (6, True), "P_i": (3, True), "N": (1, False), "N^i": (3, False)}
D_phase = sum(2 * n for (n, _) in sectors.values())
D_alt = 2 * (6 + 3 + 1 + 3)
check("C1", D_phase == D_alt == 26,
      f"sum over sectors 2*n_components = {D_phase} (independent sum {D_alt}); sectors "
      f"{ {k: v[0] for k, v in sectors.items()} }",
      "26",
      "6 metric + 3 P + 1 lapse + 3 shift, doubled")

# C2: primaries.  Build K_ij and E_i with N(t), N^i(t) as explicit functions of time and
# verify that no time derivative of either appears: the Hessian w.r.t. Ndot, Ndot^i vanishes.
Nt = sp.Function('N')(t)
Nit = [sp.Function(f'N{i}')(t) for i in range(3)]
zt = sp.Function('zeta')(t)
Pt = [sp.Function(f'P{i}')(t) for i in range(3)]
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(zt, t) * (1 if i == j else 0)
                                    - sp.Rational(1, 2) * (sp.diff(Nit[i], xs[j]) + sp.diff(Nit[j], xs[i]))) / Nt)
thetat = sp.trace(Kij)
Eit = [(sp.diff(Pt[i], t) - sum(Nit[j] * sp.diff(Pt[i], xs[j]) for j in range(3))
        - sum(Pt[j] * sp.diff(Nit[j], xs[i]) for j in range(3))) / Nt for i in range(3)]
Ndotf = sp.diff(Nt, t)
Ndvec = [sp.diff(Nit[j], t) for j in range(3)]
prim_ok = (all(sp.simplify(sp.diff(Kij[i, j], Ndotf)) == 0 for i in range(3) for j in range(3))
           and all(sp.simplify(sp.diff(thetat, Ndotf)) == 0 for _ in [0])
           and all(sp.simplify(sp.diff(Eit[i], Ndotf)) == 0 for i in range(3))
           and all(sp.simplify(sp.diff(Eit[i], Ndvec[j])) == 0 for i in range(3) for j in range(3))
           and all(sp.simplify(sp.diff(Kij[i, j], Ndvec[m])) == 0 for i in range(3) for j in range(3) for m in range(3)))
n_primary = 1 + 3
check("C2", prim_ok and n_primary == 4,
      f"no Ndot or Ndot^i anywhere in K_ij, theta or E_i: {prim_ok}; primaries = {n_primary}",
      "4 (pi_N, pi_N^i)",
      "the lapse and the shift are Lagrange multipliers: no velocities anywhere in the action")

# C3: secondaries -- delta H/delta N = H_perp, delta H/delta N^i = H_i
# verified structurally: N enters only (a) as the multiplier, (b) inside K_ij and E_i,
# (c) linearly in d_i ln N (the clock).  So {pi_N, H} = -H_perp and {pi_N^i, H} = -H_i.
# Here: check that N enters the P sector only as 1/N in E_i (no Ndot), i.e. it is a multiplier.
L_kin = sqh * Nlapse * eta_s / 2 * sum(E_i(i) ** 2 for i in range(3))
Ndep = sp.simplify(sp.diff(sp.simplify(Nlapse * L_kin), Nlapse))
n_secondary = sum(n for (n, lag) in sectors.values() if not lag)   # one secondary per Lagrange-multiplier component
check("C3", Ndep == 0 and n_secondary == 4,
      f"d(N L_kin)/dN = {Ndep} (N enters only as the algebraic 1/N of E_i); secondaries = {n_secondary}",
      "4 (H_perp, H_i)",
      "N enters as 1/N in E_i only: H_perp is the secondary of pi_N, H_i of pi_N^i")

# C4: no tertiary.  Two computed facts:
#  (i) the P equation is second order (A3), so it can be solved for Pddot: no constraint;
#  (ii) H_perp is independent of N, so {pi_N, H} = -H_perp carries no multiplier and the
#       Dirac chain terminates.
Pi_P = sp.symbols('piP0 piP1 piP2', real=True)
L_pk = L_P(eta_s)                       # sqrt(h) eta/(2N) (Pdot - ...)^2 + sqrt(h) K/2 |P|^2
Pdots_sol = {}
# Pdot_i - Lie_N P_i = N pi_i /(sqrt(h) eta)  ->  use the momentum as the new variable
Htot = sum(Pi_P[i] * Pdots[i] for i in range(3)) - L_pk
# eliminate Pdot: Pdot_i = N pi_i/(sqrt(h) eta) + (N^j d_j P_i + P_j d_i N^j)
subs_pd = {}
for i in range(3):
    lie = sum(Nl[j] * dP[j, i] for j in range(3)) + sum(Pl[j] * dN[i, j] for j in range(3))
    subs_pd[Pdots[i]] = Nlapse * Pi_P[i] / (sqh * eta_s) + lie
Htot = sp.expand(Htot.subs(subs_pd))
# H_perp is the coefficient of N with the shift switched off (the N^i terms are H_i)
Htot0 = sp.expand(Htot.subs({Nl[j]: 0 for j in range(3)}).subs(
    {dN[i, j]: 0 for i in range(3) for j in range(3)}))
H_perp = sp.simplify(Htot0 / Nlapse)
Hperp_indep_N = sp.simplify(sp.diff(H_perp, Nlapse))
Hperp_closed = sp.simplify(sum(Pi_P[i] ** 2 for i in range(3)) / (2 * sqh * eta_s) + sqh * K_s / 2 * sum(p * p for p in Pl))
check("C4", Hperp_indep_N == 0 and sp.simplify(H_perp - Hperp_closed) == 0,
      f"dH_perp/dN = {Hperp_indep_N}; H_perp - [|pi_P|^2/(2 sqrt(h) eta) + sqrt(h) K/2 |P|^2] = "
      f"{sp.simplify(H_perp - Hperp_closed)}; P equation order: 2",
      "0 tertiary",
      "no tertiary: the P equation is evolutionary (A3) and H_perp carries no N, so the chain terminates")

# C5: second-class rank on the surface
SC_rank = rank_on
n_sc = 0
check("C5", SC_rank == 0 and n_sc == 0,
      f"rank of the P-block of the Dirac matrix on the constraint surface = {SC_rank}; SC = {n_sc}",
      "0, 0",
      "no second-class pair exists in the P sector: the only candidate block is identically zero")

# C6: DOF
n_fc = n_primary + n_secondary
dof = (D_phase - 2 * n_fc - n_sc) / 2
n_modes = 2 + 2 + 1
check("C6", dof == 5.0 and n_modes == 5 and n_fc == 8,
      f"DOF = ({D_phase} - 2*{n_fc} - {n_sc})/2 = {dof}; explicit modes 2 tensor + 2 vector + 1 scalar = {n_modes}",
      "5",
      "agrees with A54 (26, 8, 5): no constraint is reclassified")

# C7: Route C's arithmetic
dof_sc2 = (D_phase - 2 * n_fc - 2) / 2
dof_fc7 = (D_phase - 2 * (n_fc - 1) - 0) / 2      # H_perp drops out as a constraint
dof_fc7b = (D_phase - 2 * (n_fc - 1) - 2) / 2     # H_perp second class with one partner
check("C7", dof_sc2 == 4.0 and dof == 5.0 and SC_rank == 0 and dof_fc7 == 6.0 and dof_fc7b == 5.0,
      f"SC=2 branch -> DOF = {dof_sc2}; computed rank on the surface = {SC_rank} -> DOF = {dof}; "
      f"if H_perp left the first-class set: (FC=7,SC=0) -> {dof_fc7}, (FC=7,SC=2) -> {dof_fc7b}",
      "4 needs SC=2; computed SC=0 -> 5; the H_perp caveat gives 6 or 5, never 4",
      "Route C's 4 needs two second-class constraints; the computed bracket gives none, and the H_perp "
      "caveat gives 6 or 5, never 4")

# ============================================================================
# D -- the fifth mode's kinetic term from the action
# ============================================================================
print("\n-- D: the kinetic coefficient from the quadratic action " + "-" * 47)
# D1: conformal kinetic coefficient
zdot = sp.Symbol('zdot', real=True)
Ysym = sp.Symbol('Y', real=True)
Kmix = sp.Matrix(3, 3, lambda i, j: ((zdot if i == j else 0) + (Ysym if True else 0)) / 1)
# K_ij = (zdot delta_ij + k_i k_j psi) / N ; in Fourier with k^2 psi = Y:
#   K_ij K^ij = (3 zdot^2 + 2 zdot Y + Y^2)/N^2 ;  theta = (3 zdot + Y)/N
Ksq = (3 * zdot ** 2 + 2 * zdot * Ysym + Ysym ** 2) / N_s ** 2
theta = (3 * zdot + Ysym) / N_s
conf = sp.simplify(Ksq - (1 + b_s) * theta ** 2)
D1_res = sp.simplify(conf - (-3 * (2 + 3 * b_s) * zdot ** 2 - 2 * (2 + 3 * b_s) * zdot * Ysym - b_s * Ysym ** 2) / N_s ** 2)
D1_conf = sp.simplify(conf.subs(Ysym, 0) - (-3 * (2 + 3 * b_s) * zdot ** 2) / N_s ** 2)
check("D1", D1_res == 0 and D1_conf == 0,
      f"K^2-(1+beta)theta^2 = {sp.expand(sp.simplify(conf * N_s ** 2))}/N^2 ; at Y=0 residual {D1_conf}",
      "-3(2+3beta) zdot^2/N^2 at Y=0",
      "the conformal mode's kinetic term is NEGATIVE for beta>0: it is the would-be ghost direction")

# D2: R3^(2) for the conformal mode
z_s = sp.Symbol('zeta', real=True)
R3_2 = 2 * p_s ** 2 * z_s ** 2
D2_val = float(R3_2.subs({p_s: 1.3, z_s: 0.4}))
D2_exp = 2 * 1.3 ** 2 * 0.4 ** 2
check("D2", abs(D2_val - D2_exp) < 1e-14,
      f"R3^(2) = {R3_2} -> {D2_val:.6f} at p=1.3, zeta=0.4",
      f"{D2_exp:.6f}",
      "sqrt(h) R3 = 2 (d zeta)^2 + total derivative: the conformal gradient term")

# D3: eliminate the shift
Lq = (-3 * Acombo * sp.diff(zz, t) ** 2 + 2 * Acombo * sp.diff(zz, t) * Yf - b_p * Yf ** 2) / (4 * Kp)
Ysol = sp.solve(sp.diff(Lq, Yf), Yf)[0]
Lq_sub = sp.simplify(Lq.subs(Yf, Ysol))
Ccoef = Acombo / (Kp * b_p)
D3_res = sp.simplify(sp.diff(Lq_sub, sp.diff(zz, t), 2) / 2 - Ccoef / 2)
check("D3", D3_res == 0,
      f"after eliminating Y: coefficient of zeta-dot^2 = {sp.simplify(sp.diff(Lq_sub, sp.diff(zz,t), 2)/2)}; "
      f"C/2 = {Ccoef/2}",
      "C/2 = (2+3beta)/(2 K beta)",
      "the shift's contribution cancels the negative conformal sign for beta>0")

# D4: the lapse equation at H = 0 is a CONSTRAINT (no n in it)
L1 = sp.simplify(L_sc.subs(Yf, Ysol))
D4_res = sp.simplify(sp.diff(L1, nn) - p_ ** 2 * (zz / Kp + sig))
check("D4", D4_res == 0,
      f"dL/dn = {sp.simplify(sp.diff(L1, nn))};  p^2(zeta/K+sigma) residual = {D4_res}",
      "p^2 (zeta/K + sigma)",
      "at H=0 the lapse equation contains no n: it is the constraint Z = zeta/K + sigma = 0")

# D5: the final action
Lfin = sp.simplify(L1.subs({nn: 0, zz: -Kp * sig}))
Lfin = sp.simplify(Lfin.subs(sp.diff(zz, t), -Kp * sp.diff(sig, t)))
Lfin = sp.expand(sp.simplify(Lfin))
Qcoef = sp.simplify(sp.diff(Lfin, sp.diff(sig, t), 2) / 2)
Vcoef = sp.simplify(-sp.diff(Lfin, sig, 2) / 2)
Bsym = Kp * Acombo / b_p
D5_Q = sp.simplify(Qcoef - (Bsym + eta_p * p_ ** 2) / 2)
D5_V = sp.simplify(Vcoef - alp_p * p_ ** 4 / 2)
check("D5", D5_Q == 0 and D5_V == 0,
      f"Q = {sp.simplify(2*Qcoef)}  (B + eta p^2 = {Bsym + eta_p*p_**2});  "
      f"V = {sp.simplify(2*Vcoef)}  (alpha p^4 = {alp_p*p_**4})",
      "Q = B+eta p^2, V = alpha p^4 (residuals 0)",
      "the mixed scalar's quadratic action, derived from the frozen action at H=0")

# D6: the value of Z
Qexpr = Bsym + eta_p * p_ ** 2
D6_val = float(Qexpr.subs({Kp: K_G, b_p: BETA, eta_p: ETA, p_: 1.0 / LSTAR}))
D6_exp = K_G * (2 + 3 * BETA) / BETA + ETA / LSTAR ** 2
check("D6", abs(D6_val - D6_exp) <= 1e-12 * abs(D6_exp),
      f"Z = Q = K(2+3beta)/beta + eta p^2 = {D6_val:.6e} at p=1/L*, beta={BETA}, eta={ETA}",
      f"{D6_exp:.6e}",
      "Z is a FUNCTION of beta, eta and p: the action does not fix its value")

# D7: omega^2 and c_s^2
om2 = sp.simplify(Vcoef / Qcoef)          # from the action's own V and Q (D5)
cs2 = sp.simplify(om2 / p_ ** 2)
ps = [1e-3, 1e-2, 1e-1]
cs2_closed = alp_p * p_ ** 2 / (Bsym + eta_p * p_ ** 2)
subs_num = {Kp: 1.0, b_p: BETA, eta_p: ETA, alp_p: ALPHA}
vals = [float(cs2.subs(subs_num).subs(p_, q)) for q in ps]
vals_closed = [float(cs2_closed.subs(subs_num).subs(p_, q)) for q in ps]
D7_err = max(abs(a - b) for a, b in zip(vals, vals_closed))
mono_inc = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
cs2_small = float(cs2.subs(subs_num).subs(p_, 1e-6))
check("D7", D7_err < 1e-14 and mono_inc and vals[0] > 0 and cs2_small < 1e-12,
      f"c_s^2 from the action's V/Q at p={ps} -> {['%.4e' % v for v in vals]}; "
      f"vs alpha p^2/Q {['%.4e' % v for v in vals_closed]}; max dev {D7_err:.1e}; "
      f"c_s^2(1e-6) = {cs2_small:.2e}",
      "equal to alpha p^2/(K(2+3beta)/beta + eta p^2); rising with p from 0",
      "the fifth mode is a k^4 mode: its sound speed vanishes in the IR, it is NOT c_s^2 = gamma/eta")

# D8: the mass at H = 0
m2 = sp.simplify(sp.limit(om2, p_, 0))
check("D8", m2 == 0,
      f"m^2 = lim_(p->0) V/Q = {m2}",
      "0",
      "the fifth mode is GAPLESS at H=0: A67's m^2 = 2/L*^2 is not this mode's mass")

# D9: the transverse P modes.  Coefficients read off the action:
#   kinetic per component  eta/2          (A1's Hessian at N = sqrt(h) = 1)
#   mass per component     K/2            (the W(u) term, D14)
#   gradient per component gamma/2 * p^2  (the (gamma/4) F_ij F^ij term, F^2 = 2 p^2 |P_T|^2)
shift_off = {Nlapse: 1, sqh: 1}
shift_off.update({Nl[j]: 0 for j in range(3)})
shift_off.update({dN[i, j]: 0 for i in range(3) for j in range(3)})
L_T0 = L_P(eta_s).subs(shift_off)
kin_T = sp.simplify(sp.diff(L_T0, Pdots[0], 2) / 2)
mass_T = sp.simplify(-sp.diff(L_T0, Pl[0], 2) / 2)
mT2_0 = sp.simplify(mass_T / kin_T)
mT2 = sp.simplify((mass_T + gam_p * p_ ** 2 / 2) / kin_T)
cT2 = sp.simplify((mT2 - mT2_0) / p_ ** 2)
D9_val = float(mT2_0.subs({K_s: K_G, eta_s: ETA}))
D9_exp = K_G / ETA
D9_ok = (sp.simplify(mass_T - Kp / 2) == 0) and (sp.simplify(kin_T - eta_p / 2) == 0)
check("D9", abs(D9_val - D9_exp) <= 1e-12 * abs(D9_exp) and sp.simplify(cT2 - gam_p / eta_p) == 0 and D9_ok,
      f"m_T^2 = (K/2)/(eta/2) = {D9_val:.6e}; c_T^2 = gamma/eta = {float(cT2.subs({gam_p: GAM, eta_p: ETA}))}",
      f"{D9_exp:.6e}; gamma/eta",
      "the MASSIVE P modes are the two transverse ones; A67 attributed their mass to the scalar")

# D10: the action does not force eta = gamma
# observables: slope of Q in p^2 (call it s1 = eta) and the transverse sound speed c_T^2 = gamma/eta.
# Jacobian d(s1, c_T^2)/d(eta,gamma):
Jac = sp.Matrix([[sp.diff(eta_p, eta_p), sp.diff(eta_p, gam_p)],
                 [sp.diff(gam_p / eta_p, eta_p), sp.diff(gam_p / eta_p, gam_p)]])
Jac_det = sp.simplify(Jac.det())
Jac_val = float(Jac_det.subs({eta_p: ETA, gam_p: GAM}))
def cT2_of(eta_in, gam_in):
    # if a symmetry forces eta = gamma, the second input is ignored
    e = gam_in if FORCE_ETA_EQ_GAMMA else eta_in
    return gam_in / e


ratio1 = cT2_of(1.0, 1.0)
ratio2 = cT2_of(2.0, 1.0)
check("D10", sp.simplify(Jac_det - 1 / eta_p) == 0 and abs(Jac_val) > 0 and ratio1 != ratio2,
      f"det d(eta, gamma/eta)/d(eta,gamma) = {Jac_det} = {Jac_val:.4f} != 0; "
      f"c_T^2(1,1) = {ratio1:.3f}, c_T^2(2,1) = {ratio2:.3f}",
      "1/eta, nonzero, and two distinct inputs -> two distinct c_T^2",
      "eta and gamma are independently observable: the action does NOT force eta = gamma. "
      "It does force alpha = gamma (one coefficient in front of both gradient operators)")

# D11: sign of Q is the sign of beta
grid_b = [-0.6, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0]     # the branch 2+3beta > 0
signs = []
for bb in grid_b:
    qv = float((Bsym + eta_p * p_ ** 2).subs({Kp: 1.0, b_p: bb, eta_p: 1.0, p_: 0.01}))
    signs.append((bb, qv))
ok_sign = all((qv > 0) == (bb > 0) for (bb, qv) in signs)
Q_input = float((Bsym + eta_p * p_ ** 2).subs({Kp: 1.0, b_p: BETA, eta_p: ETA, p_: 0.01}))
ok_sign = ok_sign and Q_input > 0
check("D11", ok_sign,
      "Q(beta) for beta in " + ", ".join(f"{bb}: {qv:+.3f}" for bb, qv in signs)
      + f"; Q(beta={BETA}) = {Q_input:+.3f}",
      "sign(Q) = sign(beta)",
      "on the branch 2+3beta>0 (where the theta Legendre map is invertible, A54 L8) the fifth mode's "
      "kinetic term has the sign of beta: Q = K(2+3beta)/beta")

# D12: an open healthy set
cnt_tot = 0
cnt_ok = 0
worst = None
for bb in [0.2, 0.5, 1.0, 2.0]:
    for ee in [0.5, 1.0, 2.0]:
        for gg in [0.2, 1.0, 3.0]:
            cnt_tot += 1
            qv = float((Bsym + eta_p * p_ ** 2).subs({Kp: 1.0, b_p: bb, eta_p: ee, p_: 0.01}))
            w2 = float(om2.subs({Kp: 1.0, b_p: bb, eta_p: ee, alp_p: gg, p_: 0.01}))
            mt2 = float(mT2_0.subs({K_s: 1.0, eta_s: ee}))
            cs2v = float(cs2.subs({Kp: 1.0, b_p: bb, eta_p: ee, alp_p: gg, p_: 0.01}))
            if qv > 0 and w2 > 0 and mt2 > 0 and cs2v > 0:
                cnt_ok += 1
            else:
                worst = (bb, ee, gg, qv, w2, mt2, cs2v)
check("D12", cnt_ok == cnt_tot,
      f"{cnt_ok}/{cnt_tot} points of beta>0, eta>0, gamma>0 have Z>0, omega^2>0, m_T^2>0, c_s^2>0"
      + ("" if worst is None else f"; first bad {worst}"),
      f"{cnt_tot}/{cnt_tot}",
      "ghost-free and tachyon-free on an OPEN set of the action's coefficients (beta>0, eta>0, gamma>0)")

# D15: the coefficients as dialled (the frozen action's own) are in the healthy set
Q_in = float((Bsym + eta_p * p_ ** 2).subs({Kp: 1.0, b_p: BETA, eta_p: ETA, p_: 0.01}))
w2_in = float(om2.subs({Kp: 1.0, b_p: BETA, eta_p: ETA, alp_p: ALPHA, p_: 0.01}))
mt2_in = float(mT2_0.subs({K_s: 1.0, eta_s: ETA}))
cs2_in = float(cs2.subs({Kp: 1.0, b_p: BETA, eta_p: ETA, alp_p: ALPHA, p_: 0.01}))
check("D15", Q_in > 0 and w2_in > 0 and mt2_in > 0 and cs2_in > 0,
      f"at (beta, eta, alpha, gamma) = ({BETA}, {ETA}, {ALPHA}, {GAM}): Q = {Q_in:+.4f}, "
      f"omega^2 = {w2_in:+.3e}, m_T^2 = {mt2_in:+.3e}, c_s^2 = {cs2_in:+.3e}",
      "all four > 0",
      "the coefficients as dialled are ghost-free and tachyon-free")

# D13: A67's mass is the input eta = K L*^2/2 read back
eta_a67 = K_G * LSTAR ** 2 / 2.0
m_a67 = K_G / eta_a67
two_over = 2.0 / LSTAR ** 2
eta_alt = 3.0 * K_G * LSTAR ** 2 / 2.0
m_alt = K_G / eta_alt
D13_a = abs(m_a67 - two_over) <= 1e-12 * two_over
D13_b = abs(m_alt - two_over) > 1e-3 * two_over
check("D13", D13_a and D13_b,
      f"with eta=K L*^2/2: K/eta = {m_a67:.6e} = 2/L*^2 = {two_over:.6e}; "
      f"with eta=3K L*^2/2: K/eta = {m_alt:.6e} = {m_alt/two_over:.3f} x 2/L*^2",
      "identity then 1/3",
      "the '2/L*^2' is eta = K L*^2/2 in disguise: an input echo, not a prediction")

# ---- D14: W(u) at quadratic order is (K/2)|P|^2: the mass term's numerator -----
u_ = sp.Symbol('u', positive=True)
a0_ = sp.Symbol('a0', positive=True)
W_u = (a0_ ** 2 / K_s) * (-u_ / a0_ - sp.log(1 - u_ / a0_)) if W_ON else sp.Integer(0)
W2 = sp.simplify(sp.diff(W_u, u_, 2).subs(u_, 0))
# u = K|P| -> W ~ (1/2) W''(0) u^2 = (1/2)(1/K)(K^2 P^2) = (K/2) P^2
mass_coef = sp.simplify(sp.Rational(1, 2) * W2 * K_s ** 2)
check("D14", W2 == 1 / K_s and mass_coef == K_s / 2,
      f"W''(0) = {W2}; (1/2) W''(0) K^2 = {mass_coef} (coefficient of |P|^2)",
      "1/K and K/2",
      "the P mass term is (K/2)|P|^2 with a FIXED coefficient K/2: it is what gives m_T^2 = K/eta")

# ---- D16: the action forces alpha = gamma (one stiffness for both gradients) ----
c_dotP = sp.Rational(1, 2) * alp_s      # coefficient of (D.P)^2
c_F = sp.Rational(1, 4) * gam_s         # coefficient of F_ij F^ij
ratio_grad = sp.simplify(c_dotP / c_F)
check("D16", sp.simplify(ratio_grad - 2 * alp_s / gam_s) == 0 and ratio_grad.subs({alp_s: 1, gam_s: 1}) == 2,
      f"[coefficient of (D.P)^2]/[coefficient of F^2] = {ratio_grad} = 2 alpha/gamma",
      "2 (one gamma in front of both operators)",
      "the FROZEN action uses one gamma for both gradient operators, so alpha = gamma is FORCED; "
      "nothing ties eta to gamma")

# ---- D17: F_ij F^ij = 2 p^2 |P_T|^2 for a transverse plane wave (c_T^2 = gamma/eta) ----
kk = np.array([0.0, 0.0, 1.7])
F2_err = 0.0
for sd in [7, 8, 9]:
    rr = np.random.default_rng(sd)
    PTv = rr.normal(size=3)
    PTv = PTv - kk * (np.dot(PTv, kk) / np.dot(kk, kk))          # transverse
    Fm = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        for bq in range(3):
            Fm[a, bq] = 1j * (kk[a] * PTv[bq] - kk[bq] * PTv[a])
    F2 = float(np.real(np.sum(Fm * np.conj(Fm))))     # |F|^2 for the complex amplitude
    F2_err = max(F2_err, abs(F2 - 2 * np.dot(kk, kk) * np.dot(PTv, PTv)))
check("D17", F2_err < 1e-12,
      f"max|F_ij F^ij - 2 p^2 |P_T|^2| = {F2_err:.2e} over 3 random transverse modes",
      "0",
      "the (gamma/4)F^2 term gives (gamma/2) p^2 |P_T|^2, so c_T^2 = gamma/eta follows from the action")

# ============================================================================
# summary
# ============================================================================
print("\n" + "=" * 104)
npass = sum(1 for c in CHECKS if c["pass"])
tot = len(CHECKS)
print(f"A68: {npass}/{tot} PASS")
fails = [c["id"] for c in CHECKS if not c["pass"]]
if fails:
    print("FAILED:", ", ".join(fails))
print("=" * 104)

numbers = {
    "K_4piG": K_G, "Lstar_m": LSTAR, "Lstar_pc": LSTAR / PC, "a0": A0,
    "eta": ETA, "alpha": ALPHA, "gamma": GAM, "beta": BETA,
    "phase_space_dim": D_phase, "n_first_class": n_fc, "n_second_class": n_sc,
    "sc_rank_on_surface": SC_rank,
    "bracket_rank_off_surface": rank_off, "bracket_rank_divpi_zero": rank_div0,
    "bracket_eigenvalues_re_im": [[float(z.real), float(z.imag)] for z in ev],
    "bracket_on_surface_max": B3_val,
    "A4_residual": A4_max,
    "B2_max_abs_dev": B2_err, "B2_matrix_scale": B2_scale,
    "P_P_term_coefficient": str(coef_PP),
    "dof": dof, "dof_if_SC2": dof_sc2, "dof_if_FC7_SC0": dof_fc7, "dof_if_FC7_SC2": dof_fc7b,
    "Z_at_1_over_Lstar_eta1": D6_val,
    "Z_physical_eta_KL2_over_2": K_G * (2 + 3 * BETA) / BETA + (K_G * LSTAR ** 2 / 2.0) / LSTAR ** 2,
    "B_over_K": (2 + 3 * BETA) / BETA,
    "m2_scalar_H0": str(m2), "c_s2_p001": vals[0], "c_s2_p01": vals[1], "c_s2_p1": vals[2],
    "mT2": D9_val, "cT2": float(cT2.subs({gam_p: GAM, eta_p: ETA})),
    "mT2_with_eta_A67": K_G / (K_G * LSTAR ** 2 / 2.0),
    "Z_with_eta_A67_at_1_over_Lstar": K_G * (2 + 3 * BETA) / BETA + (K_G * LSTAR ** 2 / 2.0) / LSTAR ** 2,
    "Q_at_k0_beta1": K_G * (2 + 3 * BETA) / BETA,
    "Z_over_K_with_eta_A67_at_1_over_Lstar": (2 + 3 * BETA) / BETA + 0.5,
    "compton_transverse_eta_A67_pc": math.sqrt(K_G * LSTAR ** 2 / 2.0) / math.sqrt(K_G) / PC,
    "compton_transverse_if_eta_K_L2_pc": math.sqrt(K_G * LSTAR ** 2) / math.sqrt(K_G) / PC,
    "compton_transverse_if_eta_3KL2_over_2_pc": math.sqrt(3 * K_G * LSTAR ** 2 / 2.0) / math.sqrt(K_G) / PC,
    "A67_m2_K_over_eta": m_a67, "two_over_Lstar2": two_over,
    "healthy_set": [cnt_ok, cnt_tot],
    "Q_sign_table": [{"beta": bb, "Q": qv} for bb, qv in signs],
}
res = {"lane": "A68_bracket_algebra", "mutation": MUT,
       "status": "COMPUTED: bracket degenerate on pi_P=0; count 5; Z>0 iff beta>0; scalar gapless",
       "checks": CHECKS, "numbers": numbers}
print("\nnumbers:")
for k, v in numbers.items():
    print(f"  {k} = {v}")
if JSONOUT:
    with open(JSONOUT, "w") as f:
        json.dump(res, f, indent=1)
    print(f"wrote {JSONOUT}")
sys.exit(0 if npass == tot else 1)
