#!/usr/bin/env python3
"""COL1 Part 1: the reduced Newtonian spherical system of action (A) and its exact checks (sympy).

    PYTHONHASHSEED=0 python3 col1_system.py              -> col1_system.json / col1_system.out
    PYTHONHASHSEED=0 COL1_MUTATE=1 python3 col1_system.py  -> col1_system_MUTATE.json / .out (must fail R1 and R3)

R1 EL of the reduced Lagrangian = the stated system. R2 leading-order expansion of action (A)'s clock Lagrangian.
R3 WKB = SCS1's closed form. R4 P.A sign flip is a field redefinition. R5 (for KA5) SCS1's high-k frequency on the static
law state = the exact shell frequency at fixed enclosed charge. Criteria: FROZEN_CRITERIA.md section 4.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, time
import sympy as sp

MUT = os.environ.get('COL1_MUTATE') == '1'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT, RES = [], {'mutate': MUT}
T0 = time.time()


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)


t, r = sp.symbols('t r', real=True)
K, mu, a0, rhob = sp.symbols('K mu a0 rho_b', positive=True)
phi = sp.Function('phi')(t, r)
Phi = sp.Function('Phi')(t, r)
c2, c3, c4 = sp.symbols('c2 c3 c4')
Jf = sp.Lambda(sp.Symbol('s_J'), c2 * sp.Symbol('s_J') ** 2 + c3 * sp.Symbol('s_J') ** 3 + c4 * sp.Symbol('s_J') ** 4)  # generic test polynomial (QX17 practice)
SGN = -1 if MUT else 1          # MUTATE: J -> -J in the reduced Lagrangian (M2)

# ---------------- R1: Euler-Lagrange of the reduced Lagrangian ----------------
h = -(sp.diff(phi, t) + sp.diff(phi, r) ** 2 / 2 + Phi)
hr = sp.diff(h, r)
L = r ** 2 * (mu ** 2 * h ** 2 / (2 * K) + SGN * Jf(hr) - sp.diff(Phi, r) ** 2 / (2 * K) - rhob * Phi)
from sympy.calculus.euler import euler_equations
EL = euler_equations(L, [phi, Phi], [t, r])
E_phi, E_Phi = [e.lhs for e in EL]
# the stated system (always the unmutated one)
s_ = sp.Symbol('s')
Jp = sp.Lambda(s_, sp.diff(Jf(s_), s_))  # J'(s)
Pr = -Jp(hr)                                  # P_r = dJ/dA_r with A = -h_r
N = mu ** 2 * h / K + sp.diff(r ** 2 * Pr, r) / r ** 2
cont = sp.diff(r ** 2 * N, t) + sp.diff(r ** 2 * N * sp.diff(phi, r), r)
pois = sp.diff(r ** 2 * sp.diff(Phi, r), r) / K - r ** 2 * (rhob + N)
d1 = sp.simplify(sp.expand(E_phi - cont))
d1b = sp.simplify(sp.expand(E_phi + cont))
d2 = sp.simplify(sp.expand(E_Phi - pois))
d2b = sp.simplify(sp.expand(E_Phi + pois))
r1_phi = (d1 == 0) or (d1b == 0)
r1_Phi = (d2 == 0) or (d2b == 0)
# Euler identity: d_t v + v d_r v = -d_r Phi - d_r h with v = phi_r and h as defined (exact)
v = sp.diff(phi, r)
eul = sp.simplify(sp.diff(v, t) + v * sp.diff(v, r) + sp.diff(Phi, r) + sp.diff(h, r))
RES['R1'] = {'continuity_residual_zero': bool(r1_phi), 'poisson_residual_zero': bool(r1_Phi), 'euler_identity': str(eul),
             'pass': bool(r1_phi and r1_Phi and eul == 0)}
P(f'R1 EL(phi) = clock-charge continuity d_t(r^2 N) + d_r(r^2 N v): {r1_phi}; EL(Phi) = Poisson with rho_b + N: {r1_Phi};'
  f' Euler identity residual {eul} -> {"PASS" if RES["R1"]["pass"] else "FAIL"}  [{time.time() - T0:.1f}s]')

# ---------------- R2: leading-order expansion of action (A)'s clock sector, 1+1 dimensions ----------------
eps, T, x = sp.symbols('epsilon T x', positive=True)
Ph = sp.Function('Phihat')(T, x)
Ps = sp.Function('Psihat')(T, x)
ph = sp.Function('phihat')(T, x)
tt = sp.Symbol('t')
# metric -(1 + 2 eps^2 Phi) dt^2 + (1 - 2 eps^2 Psi) dx^2 ; slow time T = eps t ; tau = t - eps phihat
gtt = -(1 + 2 * eps ** 2 * Ph); gxx = (1 - 2 * eps ** 2 * Ps)
dtau_t = 1 - eps ** 2 * sp.diff(ph, T)        # d_t tau = 1 - eps * eps * phihat_T
dtau_x = -eps * sp.diff(ph, x)
Q2 = -(dtau_t ** 2 / gtt + dtau_x ** 2 / gxx)
Q = sp.sqrt(Q2)
Qs = sp.series(Q, eps, 0, 4).removeO()
hhat = -(sp.diff(ph, T) + sp.diff(ph, x) ** 2 / 2 + Ph)
r2_Q = sp.simplify(sp.expand(Qs - (1 + eps ** 2 * hhat)))
# acceleration A_x = -h_x^n d_n ln Q ; h_x^n = delta_x^n + n_x n^n ; n_m = -d_m tau / Q
n_lo = [-dtau_t / Q, -dtau_x / Q]                 # (t, x) lower components
ginv = [1 / gtt, 1 / gxx]
n_up = [ginv[0] * n_lo[0], ginv[1] * n_lo[1]]
lnQ = sp.log(Q)
d_lnQ = [eps * sp.diff(lnQ, T), sp.diff(lnQ, x)]   # d_t = eps d_T
A_x = -(d_lnQ[1] + n_lo[1] * (n_up[0] * d_lnQ[0] + n_up[1] * d_lnQ[1]))
A_s = sp.series(A_x, eps, 0, 4).removeO()
r2_A = sp.simplify(sp.expand(A_s - (-eps ** 2 * sp.diff(hhat, x))))
# L_K = mu^2 (Q-1)^2/(2K): leading term eps^4 mu^2 hhat^2/(2K); sqrt(-g) = 1 + O(eps^2)
LK = sp.series(mu ** 2 * (Q - 1) ** 2 / (2 * K), eps, 0, 5).removeO()
r2_LK = sp.simplify(sp.expand(LK - eps ** 4 * mu ** 2 * hhat ** 2 / (2 * K)))
sqrtg = sp.series(sp.sqrt(-gtt * gxx), eps, 0, 2).removeO()
RES['R2'] = {'Q_minus_(1+eps^2 h)': str(r2_Q), 'A_x_plus_eps^2 h_x': str(r2_A), 'L_K_leading': str(r2_LK),
             'sqrt_g_to_O(eps)': str(sqrtg), 'pass': bool(r2_Q == 0 and r2_A == 0 and r2_LK == 0 and sqrtg == 1)}
P(f'R2 weak field: Q = 1 + eps^2 h + O(eps^4): {r2_Q == 0}; A_x = -eps^2 h_x + O(eps^4): {r2_A == 0};'
  f' L_K = eps^4 mu^2 h^2/(2K) + O(eps^6): {r2_LK == 0}; sqrt(-g) = 1 + O(eps^2): {sqrtg == 1}'
  f' -> {"PASS" if RES["R2"]["pass"] else "FAIL"}  [{time.time() - T0:.1f}s]')
P('   so P.A - W -> P.(-grad h) - W(K|P|) at leading order; maximising over P gives J(|grad h|) (QX17 K0).')

# ---------------- R3: WKB about a static background = SCS1's closed form ----------------
w, k, m, N0 = sp.symbols('omega k m N0', positive=True)
dphi, dN, dPhi = sp.symbols('dphi dN dPhi')
# linearised, local: delta h = i w dphi - dPhi ; continuity -i w dN - N0 k^2 dphi = 0 ;
# dN = (mu^2/K + SGN m k^2) delta h  [m = longitudinal J'' ; MUTATE flips the polarization sign] ; Poisson -k^2 dPhi = K dN
I = sp.I
dh = I * w * dphi - dPhi
eqs = [sp.Eq(-I * w * dN - N0 * k ** 2 * dphi, 0), sp.Eq(dN, (mu ** 2 / K + SGN * m * k ** 2) * dh), sp.Eq(-k ** 2 * dPhi, K * dN)]
M = sp.Matrix([[sp.diff(e.lhs - e.rhs, v_) for v_ in (dphi, dN, dPhi)] for e in eqs])
det = sp.factor(sp.simplify(M.det()))
wsol = sp.solve(sp.Eq(det, 0), w ** 2) if det.has(w) else []
w2 = [sp.simplify(s) for s in sp.solve(det, w)]
w2sq = sp.simplify(w2[-1] ** 2) if w2 else None
scs1 = K * N0 * ((1 - K * m) * k ** 2 - mu ** 2) / (mu ** 2 + K * m * k ** 2)
r3 = sp.simplify(w2sq - scs1) if w2sq is not None else None
RES['R3'] = {'omega2': str(w2sq), 'SCS1': str(scs1), 'residual': str(r3), 'pass': bool(r3 == 0)}
P(f'R3 WKB omega^2 = {w2sq}; SCS1 (Qbar = 1, G = N0) = {scs1}; residual {r3} -> {"PASS" if r3 == 0 else "FAIL"}  [{time.time() - T0:.1f}s]')

# ---------------- R4: P.A sign flip is a field redefinition ----------------
p, A = sp.symbols('p A', positive=True)
W = (a0 ** 2 / K) * (-K * p / a0 - sp.log(1 - K * p / a0))
# max over P along -A of (-P.A - W): P = -p Ahat gives +p A - W ; same stationary point as the original
stat = sp.solve(sp.diff(p * A - W, p), p)
Jval = sp.simplify((p * A - W).subs(p, stat[0]))
Jtarget = (a0 ** 2 / K) * (A / a0 - sp.log(1 + A / a0))
r4 = sp.simplify(sp.expand_log(Jval - Jtarget, force=True))
RES['R4'] = {'stationary_p': str(stat), 'J_residual': str(r4), 'pass': bool(r4 == 0)}
P(f'R4 max_P[-P.A - W] (P = -p Ahat): K p = {sp.simplify(K * stat[0])}; value - J = {r4} -> {"PASS (M2a cannot bite)" if r4 == 0 else "FAIL"}')

# ---------------- R5: SCS1 high-k frequency = exact shell frequency on the static law state (mu_K = 0) ----------------
u, rr, beta = sp.symbols('u r beta', positive=True)      # u = g/a0 ; beta = G M_b/a0 ; law: u^2/(1+u) = beta/r^2
# shell frequency at fixed enclosed charge: f(r) = -g_b - y + U(y), y = G m / r^2, U(y) = a0 y/(a0 - y)
G_, Mb, mm, R = sp.symbols('G M_b m R', positive=True)
yv = G_ * mm / R ** 2
f = -G_ * Mb / R ** 2 - yv + a0 * yv / (a0 - yv)
om2_shell = -sp.diff(f, R)
# static law state: x = y/a0 = u/(1+u), g_b = a0 u^2/(1+u)
om2_shell_s = sp.simplify(om2_shell.subs({mm: R ** 2 * a0 * (u / (1 + u)) / G_, Mb: R ** 2 * a0 * u ** 2 / ((1 + u) * G_)}))
# SCS1 high-k: G (1 - K m)/m, G = D.P = phantom density, K m = 1/(1+u)^2 (longitudinal J''), K Pi = (1/r^2) d(r^2 a0 x)/dr
ufun = sp.Function('u')(rr)
lawrel = sp.Eq(ufun ** 2 / (1 + ufun), beta / rr ** 2)
up = sp.solve(sp.diff(lawrel.lhs - lawrel.rhs, rr), sp.diff(ufun, rr))[0]
KPi = sp.diff(rr ** 2 * a0 * ufun / (1 + ufun), rr) / rr ** 2
KPi = KPi.subs(sp.diff(ufun, rr), up)
KPi = sp.simplify(KPi.subs(beta, rr ** 2 * ufun ** 2 / (1 + ufun)).subs(ufun, u))
Km = 1 / (1 + u) ** 2
om2_scs1 = sp.simplify(KPi * (1 - Km) / Km)          # G (1 - K m)/m with G = Pi: K Pi (1 - Km)/(K m)
r5 = sp.simplify(om2_shell_s - om2_scs1.subs(rr, R))
RES['R5'] = {'omega2_shell_on_law_state': str(om2_shell_s), 'omega2_SCS1_highk': str(om2_scs1), 'residual': str(r5),
             'X14_small_x_form': '2 a0 x^2 / r', 'exact': '2 a0 u^2 / r = 2 a0 x^2/(r (1-x)^2)', 'pass': bool(r5 == 0)}
P(f'R5 shell frequency on the static law state: {om2_shell_s}; SCS1 high-k G(1-Km)/m: {om2_scs1}; residual {r5}'
  f' -> {"PASS" if r5 == 0 else "FAIL"} (X14 quoted the small-x form 2 a0 x^2/r)')

ok = all(RES[k_]['pass'] for k_ in ('R1', 'R2', 'R3', 'R4', 'R5'))
RES['all_pass'] = ok
P(f'\nCOL1 Part 1 symbolic checks: {"ALL PASS" if ok else "FAIL"}{" (MUTATE run: R1/R3 must FAIL)" if MUT else ""}; {time.time() - T0:.1f}s')
P('kappa = 1/2 FITTED; not theory closed. Adopts nothing.')
suf = '_MUTATE' if MUT else ''
json.dump(RES, open(os.path.join(HERE, f'col1_system{suf}.json'), 'w'), indent=1)
open(os.path.join(HERE, f'col1_system{suf}.out'), 'w').write('\n'.join(OUT) + '\n')
sys.exit(0 if (ok and not MUT) or (MUT and not ok) else 1)
