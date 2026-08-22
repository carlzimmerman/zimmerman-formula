#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec11_alpha12_preferred_frame.py -- Section 11 part 2: alpha_1, alpha_2
=======================================================================
Ab-initio derivation of the preferred-frame PPN parameters alpha_1,
alpha_2 for the frozen khronon action, cross-checked against the
khronometric literature (Blas-Pujolas-Sibiryakov arXiv:1007.3503,
Eq. (5.34) at beta=0 and Appendix E intermediates).

METHOD (sympy, mostly-minus diag(1,-1,-1,-1), M^2 = 1):
Covariant (Stueckelberg) khronon sector
   S_chi = -(1/2) INT sqrt(-g) [ lam2 (grad_mu u^mu)^2 + alpha a_mu a^mu ],
   u_mu = d_mu phi / sqrt(g^{ab} d_a phi d_b phi),
about flat space with the khronon background of a source moving relative
to the preferred frame:  ubar^0 = sqrt(1+w^2), ubar^i = w^i.
Since K and a_mu VANISH on the background, the quadratic Lagrangian needs
only the O(ep) linearisation of K and a_mu -- everything else is exact.

The map (alpha, lam2) <-> (eta_K, lam_K) is PINNED by matching two
independently verified in-repo results (checks [F1], [F2] below):
G_cosmo/G_local (sec13/14) and the khronon speed (sec12).  Result:
   alpha = eta_eff(x),  lam2 = lam_K - 1,
with the frozen action's anisotropic a^2 coefficient at background x=g/a0
(sec10/12, derived):  eta_eff in [eta_K + 2/(1+x)^2, eta_K + 2/(1+x)];
the isotropic-alpha derivation below is bracketed with that pair.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
XV = (t, x, y, z)
SP = (x, y, z)
alpha, lam2 = sp.symbols('alpha lambda_2', real=True, nonzero=True)
ep, wb = sp.symbols('varepsilon w_b', positive=True)
w1, w2, w3 = sp.symbols('w_1 w_2 w_3', real=True)
wv = [w1, w2, w3]
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True, nonzero=True)
kv = [kx, ky, kz]
Uh = sp.Symbol('Uhat')
I = sp.I
eta = sp.diag(1, -1, -1, -1)

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name, flush=True)

def eptrunc(e, order):
    e = sp.expand(e)
    return sum(e.coeff(ep, n)*ep**n for n in range(order + 1))

def wtrunc(e, order=2):
    e = sp.expand(e)
    return sum(e.coeff(wb, n)*wb**n for n in range(order + 1))

# ----------------------------------------------------------------------
# [A] fields and O(ep) linearisation
# ----------------------------------------------------------------------
hf = {}
for mu in range(4):
    for nu in range(mu, 4):
        hf[(mu, nu)] = sp.Function('h%d%d' % (mu, nu))(x, y, z)
def hcomp(mu, nu):
    return hf[(mu, nu)] if mu <= nu else hf[(nu, mu)]
chi = sp.Function('chi')(x, y, z)

w2s = wb**2*(w1**2 + w2**2 + w3**2)
# NOTE index/sign conventions: our w^i == ubar^i (contravariant khronon flow in the
# source rest frame).  BPS's v is the SOURCE velocity w.r.t. the preferred frame and
# their listed "ubar_i = v^i" is covariant, so  v = -w.  All BPS comparisons below
# substitute v -> -w.  The lapse factor sqrt(1+w^2) is expanded polynomially to O(w^4)
# from the start so that every later w_b-truncation is a legitimate polynomial
# operation (an exact sqrt would silently defeat coefficient-based truncation).
S0 = 1 + w2s/2 - w2s**2/8
phibar = S0*t - wb*(w1*x + w2*y + w3*z)                  # => ubar^i = +w^i + O(w^5)
phi_tot = phibar + ep*chi

H = sp.Matrix(4, 4, lambda a, b: hcomp(a, b))
g_up = eta - ep*(eta*H*eta)                              # O(ep)

Dphi = sp.Matrix([sp.diff(phi_tot, v) for v in XV])
Nsq = sp.expand((Dphi.T*g_up*Dphi)[0, 0])
N0 = Nsq.coeff(ep, 0)
check('[A1] background normalisation: g^{ab} dphi dphi = 1 + O(w^4 truncation)',
      wtrunc(sp.expand(N0 - 1), 3) == 0)
N1 = Nsq.coeff(ep, 1)
Ninv = 1 - ep*N1/2                                       # 1/sqrt(1 + ep N1) to O(ep), O(w^2)

u_dn = [eptrunc(sp.expand(Dphi[m]*Ninv), 1) for m in range(4)]
u_up = [eptrunc(sp.expand(sum(g_up[m, n]*u_dn[n] for n in range(4))), 1) for m in range(4)]
check('[A2] ubar^0 = 1 + w^2/2 + O(w^4), ubar^i = w^i',
      wtrunc(sp.expand(u_up[0].coeff(ep, 0) - (1 + w2s/2)), 3) == 0 and
      all(wtrunc(sp.expand(u_up[i + 1].coeff(ep, 0) - wb*wv[i]), 3) == 0 for i in range(3)))

# sqrt(-g) to O(ep): 1 + (ep/2) eta^{mn} h_mn
trh = sp.expand(sum(eta[m, n]*hcomp(m, n) for m in range(4) for n in range(4)))
sqrtg = 1 + ep*trh/2

# K = (1/sqrt(-g)) d_mu (sqrt(-g) u^mu), static perturbations
K1 = sp.expand(eptrunc(sum(sp.diff(sqrtg*u_up[m], XV[m]) for m in range(4)), 1)).coeff(ep, 1)
check('[A3] K vanishes on the background',
      sp.simplify(sp.expand(sum(sp.diff(sqrtg*u_up[m], XV[m]) for m in range(4))).coeff(ep, 0)) == 0)

Gam1 = [[[sp.Rational(1, 2)*sum(eta[l, s]*(sp.diff(hcomp(s, n), XV[m]) +
                                           sp.diff(hcomp(s, m), XV[n]) -
                                           sp.diff(hcomp(m, n), XV[s])) for s in range(4))
          for n in range(4)] for m in range(4)] for l in range(4)]

ub_up = [u_up[m].coeff(ep, 0) for m in range(4)]
ub_dn = [u_dn[m].coeff(ep, 0) for m in range(4)]
a1 = []
for m in range(4):
    lin = sp.expand(sum(u_up[n]*sp.diff(u_dn[m], XV[n]) for n in range(4))).coeff(ep, 1)
    gam = -sum(ub_up[n]*Gam1[l][n][m]*ub_dn[l] for n in range(4) for l in range(4))
    a1.append(sp.expand(lin + gam))
check('[A4] a_mu vanishes on the background',
      all(sp.simplify(sp.expand(sum(u_up[n]*sp.diff(u_dn[m], XV[n])
          for n in range(4))).coeff(ep, 0)) == 0 for m in range(4)))

K1 = wtrunc(K1, 2)
a1 = [wtrunc(am, 2) for am in a1]
a1sq = sp.expand(sum(eta[m, n]*a1[m]*a1[n] for m in range(4) for n in range(4)))
L2 = wtrunc(sp.expand(-sp.Rational(1, 2)*(lam2*K1**2 + alpha*a1sq)), 2)
print('    L2 built:', len(sp.Add.make_args(L2)), 'terms', flush=True)

# ----------------------------------------------------------------------
# [B] khronon EOM with the Newtonian seed; Fourier solve
# ----------------------------------------------------------------------
def EL(L, f):
    out = sp.diff(L, f)
    for v in SP:
        out -= sp.diff(sp.diff(L, sp.diff(f, v)), v)
    for i in range(3):
        for j in range(i, 3):
            out += sp.diff(sp.diff(L, sp.diff(f, SP[i], SP[j])), SP[i], SP[j])
    return out

ELchi = EL(L2, chi)

Ufun = sp.Function('U')(x, y, z)
seed = {hf[(0, 0)]: 2*Ufun, hf[(1, 1)]: 2*Ufun, hf[(2, 2)]: 2*Ufun, hf[(3, 3)]: 2*Ufun,
        hf[(0, 1)]: sp.S(0), hf[(0, 2)]: sp.S(0), hf[(0, 3)]: sp.S(0),
        hf[(1, 2)]: sp.S(0), hf[(1, 3)]: sp.S(0), hf[(2, 3)]: sp.S(0)}

efac = sp.exp(I*(kx*x + ky*y + kz*z))
Ch = sp.Symbol('Chat')
k2 = kx**2 + ky**2 + kz**2
wk = wb*(w1*kx + w2*ky + w3*kz)

ELchi_seed = ELchi.subs(seed).doit()
ELchi_F = ELchi_seed.subs({Ufun: Uh*efac, chi: Ch*efac}).doit()
ELchi_F = sp.expand(sp.cancel(ELchi_F/efac))
ELchi_F1 = wtrunc(ELchi_F, 1)
Ch_sol = sp.simplify(sp.solve(sp.Eq(ELchi_F1, 0), Ch)[0])
print('    Chat =', Ch_sol, flush=True)
# BPS (E.9)@beta=0 in their v; our v = -w:  Chat = +I(alpha-lam2)(w.k)Uhat/(lam2 k^2)
Ch_bps = I*(alpha - lam2)*wk*Uh/(lam2*k2)
check('[B1] khronon solution == BPS (E.9)@beta=0 under v = -w',
      sp.simplify(Ch_sol - Ch_bps) == 0)

# ----------------------------------------------------------------------
# [C] Theta^{mu nu} on-shell in Fourier
# ----------------------------------------------------------------------
Theta = {}
for mu in range(4):
    for nu in range(mu, 4):
        Tc = EL(L2, hf[(mu, nu)])
        Tc = Tc.subs(seed).doit()
        Tc = Tc.subs({Ufun: Uh*efac, chi: Ch*efac}).doit()
        Tc = sp.expand(sp.cancel(Tc/efac)).subs(Ch, Ch_sol)
        Tc = sp.expand(wtrunc(sp.expand(Tc), 2))
        Theta[(mu, nu)] = Tc if mu == nu else Tc/2
def Th(mu, nu):
    return Theta[(mu, nu)] if mu <= nu else Theta[(nu, mu)]

cons_ok = True
for nu in range(4):
    csum = sp.simplify(wtrunc(sp.expand(sum(I*kv[i]*Th(i + 1, nu) for i in range(3))), 2))
    if csum != 0:
        cons_ok = False
        print('    NONZERO k.Theta for nu =', nu, ':', csum, flush=True)
check('[C1] conservation: k_i Theta^{i nu} = 0 on-shell (to O(w^2))', cons_ok)

# ----------------------------------------------------------------------
# [D] Einstein response: solve and VERIFY the full linearised EOM
# ----------------------------------------------------------------------
hhat = {}
for mu in range(4):
    for nu in range(mu, 4):
        hhat[(mu, nu)] = sp.Symbol('hh%d%d' % (mu, nu))
def hh(mu, nu):
    return hhat[(mu, nu)] if mu <= nu else hhat[(nu, mu)]
Kmu = [sp.S(0), I*kx, I*ky, I*kz]
def Gam1F(l, m, n):
    return sp.Rational(1, 2)*sum(eta[l, s]*(Kmu[m]*hh(s, n) + Kmu[n]*hh(s, m) - Kmu[s]*hh(m, n))
                                 for s in range(4))
def R1F(m, n):
    return sp.expand(sum(Kmu[l]*Gam1F(l, m, n) for l in range(4))
                     - sum(Kmu[n]*Gam1F(l, m, l) for l in range(4)))
R1tr = sp.expand(sum(eta[a, b]*R1F(a, b) for a in range(4) for b in range(4)))
def G1dn(m, n):
    return sp.expand(R1F(m, n) - sp.Rational(1, 2)*eta[m, n]*R1tr)
def G1up(m, n):
    return sp.expand(sum(eta[m, a]*eta[n, b]*G1dn(a, b) for a in range(4) for b in range(4)))

# Newton check on the seed:
seedF = {hhat[(0, 0)]: 2*Uh, hhat[(1, 1)]: 2*Uh, hhat[(2, 2)]: 2*Uh, hhat[(3, 3)]: 2*Uh,
         hhat[(0, 1)]: 0, hhat[(0, 2)]: 0, hhat[(0, 3)]: 0,
         hhat[(1, 2)]: 0, hhat[(1, 3)]: 0, hhat[(2, 3)]: 0}
G00s = sp.simplify(G1up(0, 0).subs(seedF))
print('    G1^00[Newtonian seed] =', G00s, flush=True)
check('[D1] G1^00[seed] = +-2 k^2 Uhat (pure Poisson: seed solves vacuum eqs away from source)',
      sp.simplify(G00s - 2*k2*Uh) == 0 or sp.simplify(G00s + 2*k2*Uh) == 0)

# ansatz: hbar1^{mn} = c0 * Theta^{mn}/k^2, h1 = trace-reverse, c0 fixed by the EOM
c0 = sp.Symbol('c_0')
trTh = sp.expand(sum(eta[a, b]*Th(a, b) for a in range(4) for b in range(4)))
h1_up, h1_dn = {}, {}
for mu in range(4):
    for nu in range(mu, 4):
        hb = c0*Th(mu, nu)/k2
        h1_up[(mu, nu)] = sp.expand(hb - sp.Rational(1, 2)*eta[mu, nu]*c0*trTh/k2)
def h1u(mu, nu):
    return h1_up[(mu, nu)] if mu <= nu else h1_up[(nu, mu)]
for mu in range(4):
    for nu in range(mu, 4):
        h1_dn[(mu, nu)] = sp.expand(sum(eta[mu, a]*eta[nu, b]*h1u(a, b)
                                        for a in range(4) for b in range(4)))
def h1d(mu, nu):
    return h1_dn[(mu, nu)] if mu <= nu else h1_dn[(nu, mu)]

# verify the FULL linearised EOM  s_g * G1^{mn}[h1] = Theta^{mn}  and find (s_g, c0):
subs_h1 = {hhat[(mu, nu)]: h1d(mu, nu) for mu in range(4) for nu in range(mu, 4)}
sg = sp.Symbol('s_g')
sol_c0 = None
eqs = []
for mu in range(4):
    for nu in range(mu, 4):
        lhs = sp.expand(G1up(mu, nu).subs(subs_h1))
        eqs.append(sp.expand(sg*lhs - Th(mu, nu)))
sol = sp.solve([sp.Eq(wtrunc(e, 2), 0) for e in eqs], [sg*c0], dict=True)
# solve for the product p = sg*c0: substitute p:
p_ = sp.Symbol('p_')
eqs_p = [sp.expand(e.subs(sg, p_/c0)) for e in eqs]
solp = sp.solve([sp.Eq(sp.simplify(wtrunc(e, 2)), 0) for e in eqs_p], p_, dict=True)
check('[D2] full linearised Einstein EOM solved by hbar1^{mn} = c0 Theta^{mn}/k^2 for a'
      ' unique s_g c0', len(solp) == 1)
P0 = sp.simplify(solp[0][p_])
print('    s_g * c0 =', P0, flush=True)

# fix c0 (with s_g = +-1 absorbed) by the G_N renormalisation calibration:
# O(w^0): h1_00 must equal +alpha*Uhat  (BPS E.12a/E.13; independently equals the
# frozen action's verified static G_local = G/(1-eta_K/2) with alpha = eta_K:
# h00 = 2U + alpha U => G_N = G(1+alpha/2) = G/(1-alpha/2) to linear order)
h1_00_w0 = sp.simplify(wtrunc(h1d(0, 0), 0))
print('    h1_00|_{w=0} =', h1_00_w0, ' (want alpha*Uhat)', flush=True)
sol_c0 = sp.solve(sp.Eq(h1_00_w0, alpha*Uh), c0)
check('[D3] G_N calibration fixes c0 uniquely (sign of the Einstein coupling)',
      len(sol_c0) == 1)
C0 = sol_c0[0]
print('    c0 =', C0, ';  consistency: s_g =', sp.simplify(P0/C0), flush=True)
# S_EH = s (M^2/2) INT sqrt(-g) R  =>  delta S_EH/delta h = s (M^2/2)(-G^{mn}) -type:
# EOM  s_g G1^{mn} = Theta^{mn}  with  |s_g| = 1/2  (the M^2/2 normalisation), sign
# fixed by the G_N calibration.  s_g = -1/2 corresponds to S_EH = -(1/2) INT sqrt(-g) R
# in this script's Riemann convention -- exactly BPS's (5.27) overall sign.
check('[D4] |s_g| = 1/2 exactly (matches the (M^2/2) EH normalisation; sign = BPS 5.27)',
      sp.simplify(P0/C0 - sp.Rational(1, 2)) == 0 or sp.simplify(P0/C0 + sp.Rational(1, 2)) == 0)

def fix(e):
    return sp.expand(e.subs(c0, C0))

gam_ok = all(sp.simplify(wtrunc(fix(h1d(i, j)), 0) - (alpha*Uh if i == j else 0)) == 0
             for i in range(1, 4) for j in range(i, 4))
check('[D5] h1_ij|_{w=0} = alpha Uhat delta_ij: static gamma_PPN stays 1 (BPS E.12c)', gam_ok)

bps_ok = True
for i in range(3):
    # BPS (E.12b)@beta=0 with v = -w:  hhat_0i = -2 alpha [w_i - (w.k) k_i/k^2] Uhat
    target = sp.expand(-2*alpha*wb*wv[i]*Uh + 2*alpha*wk*kv[i]*Uh/k2)
    dd = sp.simplify(sp.expand(wtrunc(fix(h1d(0, i + 1)), 1) - target))
    if dd != 0:
        bps_ok = False
        print('    E.12b mismatch i =', i, ':', dd, flush=True)
check('[E0] h1_0i == BPS (E.12b)@beta=0 under v = -w', bps_ok)

targ00 = sp.expand(alpha*Uh + 4*alpha*w2s*Uh + (alpha*(alpha - lam2)/lam2)*wk**2*Uh/k2)
d00 = sp.simplify(sp.expand(wtrunc(fix(h1d(0, 0)), 2) - targ00))
check('[E1] h1_00 == BPS (E.12a)@beta=0 incl. the (alpha-lam2)/lam2 anisotropic piece',
      d00 == 0)

# ----------------------------------------------------------------------
# [E] extraction of alpha_1, alpha_2
# ----------------------------------------------------------------------
h0i_full = [sp.expand(wtrunc(fix(h1d(0, i + 1)), 1)) for i in range(3)]
q1s, q2s = sp.symbols('q1 q2')
eqsq = [sp.expand(h0i_full[i] - q1s*wb*wv[i]*Uh - q2s*wk*kv[i]*Uh/k2) for i in range(3)]
solq = sp.solve([sp.Eq(e, 0) for e in eqsq], [q1s, q2s], dict=True)
check('[E2] h0i decomposes exactly into w_i and longitudinal (gauge) structures',
      len(solq) == 1)
Q1 = sp.simplify(solq[0][q1s])
print('    h0i coefficient of w_i Uhat:', Q1, '(longitudinal part gauged away by xi_0)', flush=True)

# (5.33b): h0i = (alpha_1/2) G_N m v^i/r with v = -w and U = -G_N m/r (leading order):
# h0i = (alpha_1/2)(-U)(-w_i) = (alpha_1/2) U w_i  =>  alpha_1 = 2 Q1
alpha1_derived = sp.simplify(2*Q1)
print('    ALPHA_1 =', alpha1_derived, flush=True)
check('[E3] alpha_1 = -4 alpha == BPS (5.34)@beta=0', sp.simplify(alpha1_derived + 4*alpha) == 0)

h00_full = sp.expand(wtrunc(fix(h1d(0, 0)), 2))
# structure extraction done by EVALUATION, not by an underdetermined solve:
# p1 from the w-independent part; p2 from w PERPENDICULAR to k (w.k = 0);
# p2 + p3 from w PARALLEL to k; then VERIFY the full decomposition identically.
P1 = sp.simplify(h00_full.coeff(wb, 0)/Uh)
sub_perp = {w1: 0, w2: 1, w3: 0, kx: sp.Symbol('kk', positive=True), ky: 0, kz: 0}
sub_par = {w1: 1, w2: 0, w3: 0, kx: sp.Symbol('kk', positive=True), ky: 0, kz: 0}
h2part = sp.expand(h00_full.coeff(wb, 2)*wb**2)
P2 = sp.simplify((h2part.subs(sub_perp)/(Uh*wb**2)))
P2P3 = sp.simplify((h2part.subs(sub_par)/(Uh*wb**2)))
P3 = sp.simplify(P2P3 - P2)
resid = sp.simplify(sp.expand(h00_full - P1*Uh - P2*w2s*Uh - P3*wk**2*Uh/k2))
check('[E4] h00 decomposes into {1, w^2, (w.k)^2/k^2} structures (residual identically 0)',
      resid == 0)
print('    h00: p1 =', P1, ' p2 =', P2, ' p3 =', P3, flush=True)

# position dictionary: (w.k)^2/k^2 Uhat  <->  w^i w^j didj psi, lap psi = U:
r_ = sp.sqrt(x**2 + y**2 + z**2)
A_ = sp.Symbol('A', positive=True)
U_pos, psi_pos = -A_/r_, -A_*r_/2
check('[E5] lap psi = U for psi = -Ar/2, U = -A/r',
      sp.simplify(sum(sp.diff(psi_pos, v, 2) for v in SP) - U_pos) == 0)
wx = wb*(w1*x + w2*y + w3*z)
wdd = sp.expand(sum(wb**2*wv[i]*wv[j]*sp.diff(psi_pos, SP[i], SP[j])
                    for i in range(3) for j in range(3)))
check('[E6] dictionary: w^i w^j didj psi = (1/2) w^2 U - (1/2)(w.x/r)^2 U',
      sp.simplify(wdd - (w2s*U_pos/2 - wx**2*U_pos/(2*r_**2))) == 0)
# Fourier check of the dictionary: didj psi <-> -k_i k_j (-Uh/k^2) = k_i k_j Uh/k^2:
# so (w.k)^2/k^2 Uh <-> w^i w^j didj psi  --  used below.

# h00 position form: (2+P1) U + (P2 + P3/2) w^2 U - (P3/2)(w.x/r)^2 U
# (5.33a): h00 = -2 G_N m/r [1 - (a1-a2) w^2/2 - (a2/2)(w.x/r)^2],  -2G_N m/r = (2+P1)U:
#   (P2 + P3/2) = -(2+P1)(a1-a2)/2  ~  -(a1-a2)  at leading coupling order
#   -(P3/2)     = -(2+P1)(a2/2)     ~  -a2       at leading coupling order
alpha2_derived = sp.simplify(P3/2)
alpha1_from00 = sp.simplify(-(P2 + P3/2) + alpha2_derived)
print('    ALPHA_2 =', alpha2_derived, flush=True)
print('    alpha_1 (h00 route) =', alpha1_from00, flush=True)
check('[E7] internal consistency: alpha_1 from the h00 route == alpha_1 from the h0i route',
      sp.simplify(alpha1_from00 - alpha1_derived) == 0)
check('[E8] alpha_2 = alpha(alpha - lam2)/(2 lam2) == BPS (5.34)@beta=0',
      sp.simplify(alpha2_derived - alpha*(alpha - lam2)/(2*lam2)) == 0)

# ----------------------------------------------------------------------
# [F] map to (eta_K, lam_K); Solar-System satisfiability
# ----------------------------------------------------------------------
etaK, lamK, xg = sp.symbols('eta_K lambda_K x_g', positive=True)
ratio_bps = (1 - alpha/2)/(1 + 3*lam2/2)
dmap = sp.simplify(ratio_bps.subs({alpha: etaK, lam2: lamK - 1}) - (2 - etaK)/(3*lamK - 1))
check('[F1] map (G_cosmo/G_local): alpha=eta_K, lam2=lam_K-1 gives (2-eta_K)/(3lam_K-1) EXACTLY',
      dmap == 0)
da, dl = sp.symbols('da dl')
cs_frozen = ((lamK - 1)*(2 - etaK)/(etaK*(3*lamK - 1))).subs({lamK: 1 + dl, etaK: da})
cs_bps = (lam2/alpha).subs({alpha: da, lam2: dl})
lead = sp.simplify(sp.limit(cs_frozen/cs_bps, da, 0).subs(dl, 0)) if True else None
# leading order in (da, dl): cs_frozen -> dl*(2)/(da*2) = dl/da = cs_bps
check('[F2] map (khronon speed): (lam_K-1)(2-eta)/(eta(3lam_K-1)) -> lam2/alpha at leading order',
      sp.simplify(sp.series(cs_frozen*da/dl, da, 0, 1).removeO().subs(dl, 0) - 1) == 0)

print()
print('  FROZEN-ACTION PPN:  alpha_1 = -4 eta_eff,  alpha_2 = eta_eff(eta_eff-(lam_K-1))/(2(lam_K-1))')
print('  with eta_eff(x) in [eta_K + 2/(1+x)^2, eta_K + 2/(1+x)],  x = g/a0 local.')
print('  Minkowski limit x->0: eta_eff -> eta_K + 2  =>  alpha_1 -> -8 at eta_K = 0:')
print('  naive Minkowski PPN would be excluded ~10^4 x; rescued ONLY because the solar')
print('  system sits at x >> 1 (F is non-analytic at X=0: no Minkowski PPN expansion).')

a0N, GN, Msun = 9.3619e-11, 6.674e-11, 1.989e30
AU, Rsun = 1.496e11, 6.957e8
def xat(r):
    return GN*Msun/r**2/a0N
xE, xSun, xNep = xat(AU), xat(Rsun), xat(30.1*AU)
a1_E, a1_Nep = 8/(1 + xE), 8/(1 + xNep)
a2_E, a2_Sun = 1/(1 + xE), 1/(1 + xSun)
print(f'    |alpha_1| floor (eta_K=0): 1 AU {a1_E:.2e} (bound 1e-4, margin {1e-4/a1_E:.0f}x);'
      f' Neptune {a1_Nep:.2e} = AT the current bound scale')
print(f'    |alpha_2| ~ eta_eff/2 for |lam_K-1| >> eta_eff: 1 AU {a2_E:.2e}'
      f' (bound 1.2e-7, margin {1.2e-7/a2_E:.0f}x); solar interior {a2_Sun:.2e}')
lamK_excl = (2/(1 + xE))**2/(2*1.2e-7)
print(f'    alpha_2 pole: |lam_K - 1| >~ {lamK_excl:.1e} needed (at 1-AU eta_eff)')
check('[F3] alpha_1 floor at 1 AU passes with margin > 100x', a1_E < 1e-6)
check('[F4] alpha_2 floor at 1 AU passes the 1.2e-7 bound; solar-interior x: nil',
      a2_E < 1.2e-7 and a2_Sun < 1e-11)
check('[F5] pole sliver |lam_K-1| >~ 4e-9 excluded only: compatible with eta_K=0 and'
      ' BBN lam_K in [0.923, 1.100]', lamK_excl < 1e-7)

print()
n_pass = sum(1 for _, ok in results if ok)
print(f'{n_pass}/{len(results)} checks pass')
import sys
sys.exit(0 if n_pass == len(results) else 1)
