#!/usr/bin/env python3
"""AKS1 symbolic part (sympy, exact): KA1, KA2, H1-H4, and the TOE0 report (FROZEN_CRITERIA.md s. 4, 6, 9).

    python3 aks1_sym.py -> aks1_sym.out / aks1_sym.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os
import sympy as sp
from sympy.calculus.euler import euler_equations

HERE = os.path.dirname(os.path.abspath(__file__))
OUT, RES = [], {'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)


t = sp.symbols('t', real=True)
G, sig, r, R, m, k, Gam, c, a0 = sp.symbols('G sigma r R m k Gamma c a_0', positive=True)

# ---------------- KA1: SIS identities (CFG461 K1) ----------------
rho = sig ** 2 / (2 * sp.pi * G * r ** 2)
x = sp.symbols('x', positive=True)
M = sp.integrate(4 * sp.pi * x ** 2 * rho.subs(r, x), (x, 0, r))
vc2 = sp.simplify(G * M / r)
W = -sp.integrate(G * M.subs(r, x) * sp.diff(M.subs(r, x), x) / x, (x, 0, R))
Kin = sp.Rational(3, 2) * M.subs(r, R) * sig ** 2
E = sp.simplify(Kin + W)
MR = M.subs(r, R)
lamJ2 = sp.simplify(sp.pi * sig ** 2 / (G * rho))
ka1 = {'M': str(sp.simplify(M)), 'vc2': str(vc2), 'E_plus_GM2_over_4R': str(sp.simplify(E + G * MR ** 2 / (4 * R))),
       'lambdaJ2_over_2pi2r2': str(sp.simplify(lamJ2 / (2 * sp.pi ** 2 * r ** 2)))}
ka1['pass'] = (sp.simplify(M - 2 * sig ** 2 * r / G) == 0 and sp.simplify(vc2 - 2 * sig ** 2) == 0
               and sp.simplify(E + G * MR ** 2 / (4 * R)) == 0 and sp.simplify(lamJ2 - 2 * sp.pi ** 2 * r ** 2) == 0)
P('KA1 SIS: M(<r) =', ka1['M'], '; v_c^2 =', ka1['vc2'], '; E + G M^2/(4R) =', ka1['E_plus_GM2_over_4R'],
  '; lambda_J^2/(2 pi^2 r^2) =', ka1['lambdaJ2_over_2pi2r2'], '->', 'PASS' if ka1['pass'] else 'FAIL')
RES['KA1'] = ka1

# ---------------- KA2: Galley's damped oscillator from the doubled action ----------------
qp, qm = sp.Function('qp')(t), sp.Function('qm')(t)
q1, q2 = qp + qm / 2, qp - qm / 2
Lq = lambda q: m * sp.diff(q, t) ** 2 / 2 - k * q ** 2 / 2
Kgal = -m * Gam * qm * sp.diff(qp, t)
Lam = sp.expand(Lq(q1) - Lq(q2) + Kgal)
eq_m = euler_equations(Lam, [qm], t)[0].lhs
phys = sp.simplify(eq_m.subs(qm, 0).doit())
q = sp.Function('q')(t)
target = -(m * sp.diff(q, t, 2) + k * q + m * Gam * sp.diff(q, t))
res_osc = sp.simplify(phys.subs(qp, q) - target)
P('KA2 Galley oscillator: EL_{q_-} at q_- = 0 minus -(m q\'\' + k q + m Gamma q\') =', res_osc,
  '->', 'PASS' if res_osc == 0 else 'FAIL')
RES['KA2_oscillator_residual'] = str(res_osc)

# ---------------- H1: two shells, generic Gamma(A), A_j = a_j(r_1, r_2) ----------------
rp1, rp2, rm1, rm2 = [sp.Function(n)(t) for n in ('rp1', 'rp2', 'rm1', 'rm2')]
m1, m2 = sp.symbols('m1 m2', positive=True)
V = sp.Function('V'); Gf = sp.Function('Gamma_f'); A1 = sp.Function('A1'); A2 = sp.Function('A2')


def Ltot(ra, rb):
    return m1 * sp.diff(ra, t) ** 2 / 2 + m2 * sp.diff(rb, t) ** 2 / 2 - V(ra, rb)


K2 = -(m1 * Gf(A1(rp1, rp2)) * rm1 * sp.diff(rp1, t) + m2 * Gf(A2(rp1, rp2)) * rm2 * sp.diff(rp2, t))
Lam2 = Ltot(rp1 + rm1 / 2, rp2 + rm2 / 2) - Ltot(rp1 - rm1 / 2, rp2 - rm2 / 2) + K2
els = euler_equations(Lam2, [rm1, rm2], t)
r1f, r2f = sp.Function('r1')(t), sp.Function('r2')(t)
sub0 = {rm1: 0, rm2: 0}
h1_res = []
for i, (el, mi, rf, Ai) in enumerate(zip(els, (m1, m2), (r1f, r2f), (A1, A2))):
    e = el.lhs.subs(sub0).doit().subs({rp1: r1f, rp2: r2f})
    e = sp.simplify(e)
    dV = sp.diff(V(r1f, r2f), rf)
    want = -(mi * sp.diff(rf, t, 2) + dV + mi * Gf(Ai(r1f, r2f)) * sp.diff(rf, t))
    h1_res.append(sp.simplify(e - want))
# energy identity
Etot = m1 * sp.diff(r1f, t) ** 2 / 2 + m2 * sp.diff(r2f, t) ** 2 / 2 + V(r1f, r2f)
eom = {sp.diff(r1f, t, 2): (-sp.diff(V(r1f, r2f), r1f) - m1 * Gf(A1(r1f, r2f)) * sp.diff(r1f, t)) / m1,
       sp.diff(r2f, t, 2): (-sp.diff(V(r1f, r2f), r2f) - m2 * Gf(A2(r1f, r2f)) * sp.diff(r2f, t)) / m2}
dE = sp.simplify(sp.diff(Etot, t).subs(eom))
dE_want = -(m1 * Gf(A1(r1f, r2f)) * sp.diff(r1f, t) ** 2 + m2 * Gf(A2(r1f, r2f)) * sp.diff(r2f, t) ** 2)
e_res = sp.simplify(dE - dE_want)
# kinetic matrix of the doubled action: d^2 Lam / d(rp1') d(rm1') = m1 (K adds none)
kin = sp.simplify(sp.diff(Lam2, sp.diff(rp1, t), sp.diff(rm1, t)))
h1_pass = all(x_ == 0 for x_ in h1_res) and e_res == 0 and sp.simplify(kin - m1) == 0
P('H1 two shells, generic Gamma(A(r1, r2)): physical-limit residuals', h1_res, '; energy identity residual', e_res,
  '; kinetic matrix entry d2L/drp1\'drm1\' =', kin, '->', 'PASS' if h1_pass else 'FAIL')
RES['H1'] = {'residuals': [str(x_) for x_ in h1_res], 'energy_identity_residual': str(e_res), 'kinetic_entry': str(kin),
             'pass': bool(h1_pass)}

# ---------------- H2: FRW, linear order ----------------
eps_, a1, w1, H, Rr = sp.symbols('epsilon a1 w1 H R', positive=True)
fs = {'x': lambda X: X, 'x^2': lambda X: X ** 2, 'x/(1+x)': lambda X: X / (1 + X)}
h2 = {}
for name, f in fs.items():
    F_com = -(a0 / c) * f(eps_ * a1 / a0) * (eps_ * w1)              # comoving reading: v_rel = eps w1
    F_kod = -(a0 / c) * f(eps_ * a1 / a0) * (H * Rr + eps_ * w1)       # Kodama reading: v_rel = H R + eps w1
    lin_com = sp.simplify(sp.series(F_com, eps_, 0, 2).removeO().coeff(eps_, 1))
    lin_kod = sp.simplify(sp.series(F_kod, eps_, 0, 2).removeO().coeff(eps_, 1))
    bg = sp.simplify(F_com.subs(eps_, 0))
    h2[name] = {'background_force': str(bg), 'linear_coeff_comoving': str(lin_com), 'linear_coeff_kodama': str(lin_kod)}
    P(f'H2 FRW f = {name}: background drag {bg}; linear coefficient, comoving reading {lin_com}; Kodama reading {lin_kod}')
h2_pass = all(v['background_force'] == '0' and v['linear_coeff_comoving'] == '0' for v in h2.values())
P('H2 (background untouched; drag O(delta^2) in the comoving reading; no kinetic change, H1) ->', 'PASS' if h2_pass else 'FAIL',
  '| Kodama reading: linear drag -(|delta A|/c) H R for f = x, origin-dependent (reported, H-R2)')
RES['H2'] = {'by_f': h2, 'pass': bool(h2_pass and h1_pass)}

# ---------------- H3: damped dispersion around a static state ----------------
om = sp.symbols('omega')
w0sq = sp.symbols('w0sq', real=True)
roots = sp.solve(sp.Eq(om ** 2 + sp.I * Gam * om - w0sq, 0), om)
# omega0^2 > 0: write w0sq = W2 > 0; check Im <= 0 in both regimes
W2 = sp.symbols('W2', positive=True)
ims = []
for rt in roots:
    under = sp.simplify(rt.subs(w0sq, W2))
    # regime 1: 4 W2 > Gamma^2 (oscillatory): Im = -Gamma/2
    s1 = sp.simplify(sp.im(under.subs(W2, Gam ** 2 / 4 + sp.Symbol('d', positive=True))))
    # regime 2: 4 W2 < Gamma^2 (overdamped): W2 = Gamma^2/4 * u, 0 < u < 1
    u = sp.Symbol('u', positive=True)
    s2 = sp.simplify(sp.im(under.subs(W2, Gam ** 2 * u / 4)))
    ims.append((str(s1), str(s2)))
# numeric scan of the overdamped branch to confirm the sign
import numpy as np
ok = True
for G_ in (0.1, 1.0, 10.0):
    for W_ in np.logspace(-4, 3, 50):
        for rt in roots:
            val = complex(rt.subs({Gam: G_, w0sq: W_}).evalf())
            ok &= val.imag <= 1e-12
# Jeans-unstable modes keep their sign
jeans_growth = [complex(rt.subs({Gam: 1.0, w0sq: -1.0}).evalf()).imag for rt in roots]
h3_pass = bool(ok) and max(jeans_growth) > 0
P('H3 static state, omega^2 + i Gamma omega = w0^2: Im(omega) for w0^2 > 0 (oscillatory, overdamped) =', ims,
  '; numeric scan max Im <= 0:', ok, '; Jeans mode (w0^2 = -1, Gamma = 1) growth', [round(g_, 6) for g_ in jeans_growth],
  '(> 0: the sign is kept) ->', 'PASS' if h3_pass else 'FAIL')
RES['H3'] = {'Im_roots_w0sq_pos': ims, 'numeric_scan_ok': bool(ok), 'jeans_growth': jeans_growth, 'pass': h3_pass,
             'law_state_note': "around (A)'s law state SCS1's omega0^2 > 0 enters the same quadratic: Im omega <= 0"}

# ---------------- H4: matter equation has no Gamma ----------------
bp, bmn = sp.Function('bp')(t), sp.Function('bm')(t)
mb = sp.symbols('m_b', positive=True)
U = sp.Function('U')
rr_p, rr_m = sp.Function('rrp')(t), sp.Function('rrm')(t)


def Lmb(rc, bc):
    return m * sp.diff(rc, t) ** 2 / 2 + mb * sp.diff(bc, t) ** 2 / 2 - U(rc, bc)


Kc = -m * Gf(A1(rr_p, bp)) * rr_m * sp.diff(rr_p, t)
Lam4 = Lmb(rr_p + rr_m / 2, bp + bmn / 2) - Lmb(rr_p - rr_m / 2, bp - bmn / 2) + Kc
elb = euler_equations(Lam4, [bmn], t)[0].lhs.subs({rr_m: 0, bmn: 0}).doit()
bf, rf_ = sp.Function('b')(t), sp.Function('rc')(t)
elb = sp.simplify(elb.subs({bp: bf, rr_p: rf_}))
want_b = -(mb * sp.diff(bf, t, 2) + sp.diff(U(rf_, bf), bf))
h4_res = sp.simplify(elb - want_b)
h4_pass = h4_res == 0 and not elb.has(Gf)
P('H4 baryon equation from the doubled action minus the conservative one:', h4_res, '; contains Gamma:', elb.has(Gf),
  '->', 'PASS' if h4_pass else 'FAIL')
RES['H4'] = {'residual': str(h4_res), 'has_Gamma': bool(elb.has(Gf)), 'pass': bool(h4_pass)}

RES['H_pass'] = bool(h1_pass and h2_pass and h3_pass and h4_pass)
P('H (H1-H4):', 'PASS' if RES['H_pass'] else 'FAIL')

# ---------------- F3: per-period damping and terminal speed (Theorem 8's c/v) ----------------
v, Cc = sp.symbols('v C', positive=True)
g = v ** 2 / r
Tper = 2 * sp.pi * r / v
GamT = sp.simplify(Cc * g / c * Tper)
vterm = sp.simplify(g / (Cc * g / c))
P('F3: Gamma = C g/c, g = v^2/r, T = 2 pi r/v: Gamma T =', GamT, '; terminal speed g/Gamma =', vterm)
RES['F3'] = {'GammaT': str(GamT), 'v_terminal': str(vterm)}

# ---------------- TOE0 report (reported only) ----------------
# Decoupling limit, tau = t + pi on Minkowski: Q^2 = (1 + pi_t)^2 - (grad pi)^2; dust F(Q) = mu^2 (Q-1)^2/(4K)
mu, Kc_, al, be, la = sp.symbols('mu K alpha beta lambda', positive=True)
pt, gp = sp.symbols('pi_t g_pi', real=True)
e2 = sp.symbols('e2', positive=True)
Q = sp.sqrt((1 + e2 * pt) ** 2 - (e2 * gp) ** 2)
Fq = mu ** 2 * (Q - 1) ** 2 / (4 * Kc_)
quad = sp.simplify(sp.series(Fq, e2, 0, 3).removeO().coeff(e2, 2))
P('TOE0 report (i): dust term quadratic in pi on Minkowski =', quad, '-> no (grad pi)^2 term: omega^2 = 0 at every k',
  '(no restoring force; QG1\'s Minkowski failure persists without khronometric terms)')
kk, ww = sp.symbols('k omega', positive=True)
Mp2 = sp.symbols('M_P2', positive=True)
# with ordinary khronometric terms (BPS decoupling): L = (Mp2/2)[alpha (d_i pi_t)^2 - (beta+lambda)(Laplacian pi)^2] + dust
disp = sp.solve(sp.Eq(ww ** 2 * (Mp2 * al * kk ** 2 / 2 + mu ** 2 / (4 * Kc_) * 2 / 2), Mp2 * (be + la) * kk ** 4 / 2), ww ** 2)
P('TOE0 report (i\'): with alpha, beta, lambda > 0 the khronon has omega^2 =', [sp.simplify(d) for d in disp],
  '> 0 (weakly coupled), but alpha, beta, lambda are new couplings; with them 0 the row is the old FAIL')
A_ = sp.symbols('A', real=True)
nonan = sp.sqrt(A_ ** 2)
P('TOE0 report (ii) T3(i): conservative action polynomial in (Q, A) once W is removed; the sink with f = x carries',
  '|A| =', nonan, '(non-analytic at A = 0); f = x^2 gives A.A (analytic). The sink is an in-in term: it needs a bath with',
  'its own microscopic theory (a new open item)')
RES['TOE0_report'] = {'dust_quadratic_minkowski': str(quad), 'with_khronometric': [str(sp.simplify(d)) for d in disp],
                      'T3i': 'conservative part analytic after removing W; sink |A| non-analytic for f = x, analytic for f = x^2'}

P('\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.')
open(os.path.join(HERE, 'aks1_sym.out'), 'w').write('\n'.join(OUT) + '\n')
json.dump(RES, open(os.path.join(HERE, 'aks1_sym.json'), 'w'), indent=1, default=str)
