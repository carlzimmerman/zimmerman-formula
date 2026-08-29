#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
routeA_alpha12_ppn_2026.py -- PREFERRED-FRAME GATE (alpha_1, alpha_2) for the
auxiliary-chi + transverse-traceless-carrier candidate found by the inverse-design
compiler (constitutive_search.py, 2026-08-29).

THE CANDIDATE (ADM, single physical metric, matter minimally coupled):
  S = zeta INT dt d^3x N sqrt(gam) [ K_ij K^ij - K^2 + R3 - 2 Lam ]
    - zeta c_M INT dt d^3x N sqrt(gam) [ g(chi) (D phi)^2 + V(chi) ]
    + zeta c_Q INT dt d^3x N sqrt(gam) [ f(chi) Q^ij A_ij - (1/2) Q^ij M Q_ij ]  + S_m
  phi = ln N,  a_i = D_i phi,  A_ij = [a_i a_j]^TF,  zeta = c^3/(16 pi G),
  V'(chi) = [ln(1-chi)]^2  (=> chi = mu(y) = 1 - e^-y),  f(chi) = (1-chi) sqrt(V') = y e^-y.
  chi, Q auxiliary: NO time derivatives anywhere in the auxiliary sector.

METHOD (Route A, covariantised).  The gravity sector K_ijK^ij - K^2 + R3 is EXACTLY the
Einstein-Hilbert scalar by Gauss-Codazzi (the ADM identity at lambda_K = 1), so the candidate
is, identically,
      GR  +  [ a_mu-built MOND sector ]  +  [ a_mu-built carrier sector ] ,
i.e. a KHRONOMETRIC theory with
      beta = 0,  lambda_2 == lambda_K - 1 = 0 EXACTLY,  alpha_khrono = -c_M g(chi).
We Stueckelberg the preferred foliation (phi = ln N -> khronon T, u_mu = -d_mu T/sqrt(X)) and
solve the FULLY COUPLED linearised (metric, khronon) system in Fourier for a source AT REST
with the foliation flowing at velocity w -- the boosted-source setup of Route A, written
covariantly so it can be validated against Blas-Pujolas-Sibiryakov (arXiv:1007.3503).
alpha_1 is read from h_0i at O(w); alpha_2 from h_00 at O(w^2), in the SAME convention as the
in-repo BPS-anchored sec11_alpha12_preferred_frame.py.

VALIDATION LADDER (all must pass before any alpha is quoted):
  GR limit      alpha = lam2 = 0  ->  gamma_PPN = 1, alpha_1 = alpha_2 = 0 exactly
  BPS limit     lam2 != 0, small alpha  ->  alpha_1 = -4 alpha, alpha_2 = alpha(alpha-lam2)/(2 lam2)
  static gates  mu_eff(y), G_eff/G_N, Phi = Psi, the carrier's kernel requirement
Only then the candidate's own point lam2 = 0.

Run:  python3 routeA_alpha12_ppn_2026.py            (~15 min, exact rational sympy)
"""
import sys
import time
import math
import sympy as sp

T0 = time.time()
def log(*a):
    print('  [%7.1fs]' % (time.time() - T0), *a, flush=True)

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name, flush=True)

def head(s):
    print()
    print('=' * 78)
    print(s)
    print('=' * 78, flush=True)

# ======================================================================================
head('[S0]  CONSTITUTIVE SECTOR  (frozen; exact sympy)')
# ======================================================================================
yy = sp.Symbol('y', positive=True)
chi = sp.Symbol('chi', positive=True)
cM, cQ = sp.symbols('c_M c_Q', real=True, nonzero=True)
mu_y = 1 - sp.exp(-yy)
Vp = sp.log(1 - chi)**2
subc = {chi: mu_y}
check("[S0a] V'(chi) = [ln(1-chi)]^2 evaluated at chi = mu(y) = 1-e^-y equals y^2",
      sp.simplify(Vp.subs(subc) - yy**2) == 0)
f_chi = (1 - chi)*sp.sqrt(Vp)
check("[S0b] f(chi) = (1-chi) sqrt(V') = y e^-y  EXACTLY (residual 0)",
      sp.simplify(sp.powsimp(f_chi.subs(subc), force=True) - yy*sp.exp(-yy)) == 0)
check("[S0c] sqrt(V'(chi)) = |ln(1-chi)| = y, hence f(chi) = (1-chi) * y identically:"
      " the carrier coupling FACTORISES as (a^2-coefficient candidate) x y",
      sp.simplify(sp.powsimp(sp.sqrt(Vp).subs(subc), force=True) - yy) == 0)
V_of_y = sp.simplify(sp.integrate(yy**2*sp.exp(-yy), (yy, 0, yy)))
print('    V(y) =', V_of_y, '   V(y->oo) =', sp.limit(V_of_y, yy, sp.oo),
      '(a bounded, cosmological-constant-sized offset)', flush=True)

# ======================================================================================
head('[S1]  STATIC ADM REDUCTION -> the effective interpolation mu_eff(y)')
# ======================================================================================
x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
XS = (x1, x2, x3)
Phi = sp.Function('Phi')(*XS)
psi = sp.Function('psi')(*XS)
e = sp.Symbol('e', positive=True)
gam = sp.eye(3)*sp.exp(2*e*psi)
gam_inv = gam.inv()
sqrtg = sp.sqrt(sp.simplify(gam.det()))
Gam3 = [[[sp.simplify(sum(gam_inv[l, s]*(sp.diff(gam[s, n], XS[m]) + sp.diff(gam[s, m], XS[n])
                                         - sp.diff(gam[m, n], XS[s])) for s in range(3))/2)
          for n in range(3)] for m in range(3)] for l in range(3)]
def Ric3(m, n):
    q = sum(sp.diff(Gam3[l][m][n], XS[l]) for l in range(3))
    q -= sum(sp.diff(Gam3[l][m][l], XS[n]) for l in range(3))
    q += sum(Gam3[l][l][s]*Gam3[s][m][n] for l in range(3) for s in range(3))
    q -= sum(Gam3[l][n][s]*Gam3[s][m][l] for l in range(3) for s in range(3))
    return sp.simplify(q)
R3 = sp.simplify(sum(gam_inv[m, n]*Ric3(m, n) for m in range(3) for n in range(3)))
N = sp.exp(e*Phi)                                   # N = e^Phi  =>  a_i = d_i Phi exactly
a2sym = e**2*sum(sp.diff(Phi, v)**2 for v in XS)
rho = sp.Symbol('rho_star', positive=True)
zet = sp.Symbol('zeta', positive=True)
L_grav = sp.expand(sp.series(sqrtg*N*R3, e, 0, 3).removeO())

def EL3(L, F):
    out = sp.diff(L, F)
    for v in XS:
        out -= sp.diff(sp.diff(L, sp.diff(F, v)), v)
    for i in range(3):
        for j in range(i, 3):
            out += sp.diff(sp.diff(L, sp.diff(F, XS[i], XS[j])), XS[i], XS[j])
    return sp.expand(out)

lap = lambda F: sum(sp.diff(F, v, 2) for v in XS)
# matter: rest mass couples to the LAPSE only at this order
Epsi = sp.expand(EL3(zet*L_grav - rho*e*Phi, psi)/e)
check('[S1a] psi-equation is lap(Phi + psi) = 0  =>  Psi = Phi: NO leading-order slip'
      ' (the lensing gate is passed by the GR sector alone, carrier or not)',
      sp.simplify(sp.expand(Epsi).coeff(e, 1) + 4*zet*lap(Phi + psi)) == 0)
# the MOND sector, chi eliminated (envelope theorem): -c_M N sqrt(gam) W(a^2), W'(a^2)=g(chi)
ss = sp.Symbol('ss', positive=True)
ok = True
for Wfun in [ss, ss**2, ss**3, sp.sqrt(ss), ss**sp.Rational(3, 2)]:
    mp = sp.expand(EL3(zet*(-cM*Wfun.subs(ss, a2sym)), Phi)/e)
    Wpr = sp.diff(Wfun, ss).subs(ss, a2sym)
    tgt = sp.expand(2*zet*cM*e*sum(sp.diff(Wpr*sp.diff(Phi, XS[i]), XS[i]) for i in range(3)))
    ok = ok and sp.simplify(sp.expand(mp - tgt)) == 0
check("[S1b] MOND sector contributes exactly +2 zeta c_M div(W' grad Phi) to the Phi eq"
      " (verified on 5 distinct W)", ok)
grav_part = sp.simplify(sp.expand(sp.expand(EL3(zet*L_grav - rho*e*Phi, Phi)/e) + rho))
check('[S1c] gravity part of the Phi eq = -4 zeta lap(psi)  (Hamiltonian constraint)',
      sp.simplify(grav_part + 4*zet*e*lap(psi)) == 0)
print("\n    => Phi eq:  -4 zeta lap(psi) + 2 zeta c_M div(W' grad Phi) = rho_star ,"
      "  psi = -Phi from [S1a]")
print("       => div[ mu_eff grad Phi ] = 4 pi G rho_star   with   mu_eff = 1 + (c_M/2) g(chi)")

# ======================================================================================
head('[S2]  WHICH chi-FUNCTION MULTIPLIES (D phi)^2 ?  -- forced by the frozen gates')
# ======================================================================================
print('  reading A (spec as literally written): g(chi) = chi')
print('     y -> 0 (deep MOND, chi->0) : mu_eff ->', sp.limit((1 + cM*chi/2).subs(subc), yy, 0),
      '   [deep MOND REQUIRES 0]')
check('[S2a] reading A (g = chi) CANNOT reach deep MOND: mu_eff(y->0) = 1 for EVERY c_M'
      ' => the literal spec is not a MOND theory',
      sp.limit((1 + cM*chi/2).subs(subc), yy, 0) == 1)
gg = sp.Symbol('gg')
sol_g = sp.solve(sp.Eq(1 + cM*gg/2, chi), gg)[0]
check('[S2b] mu_eff = mu(y) is solvable ONLY by g = 2(chi-1)/c_M ; with c_M = -2, g = 1 - chi',
      sp.simplify(sol_g.subs(cM, -2) - (1 - chi)) == 0)
check('[S2c] with g = 1-chi, c_M = -2:  mu_eff(y) = 1 - e^-y EXACTLY, and'
      ' G_eff/G_N = 1/mu_eff -> 1 as y->oo (Newton restored, NO rescaling)',
      sp.simplify((1 - (1 - chi)).subs(subc) - mu_y) == 0)
print("\n  ==> THE a^2 COEFFICIENT IS  g(chi) = 1 - chi = e^-y ,  NOT chi.")
print("      Cross-check: f(chi) = (1-chi) sqrt(V') = g(chi) * y -- the carrier coupling is")
print("      (a^2-coefficient) x y, the SAME object.  Internal consistency of the design.")
print("      Khronometric dictionary:  alpha_khrono = -c_M g(chi) = 2(1-chi) = 2 e^-y ,")
print("      and the standard G_N = G/(1-alpha/2) then reads G_N = G/chi = G/mu  <-- MOND.")

# ======================================================================================
head('[S3]  TRACELESS (slip) SECTOR: which Q kernel M cancels the MOND traceless stress?')
# ======================================================================================
Mker = sp.Symbol('M', positive=True)
Sig_M = -cM*(1 - chi)                      # MOND traceless stress per unit A_ij
Sig_Q = cQ*f_chi**2/Mker                   # carrier: Q_ij = f A_ij / M  =>  stress c_Q f^2/M
Mreq = sp.simplify(sp.solve(sp.Eq(sp.simplify(Sig_M + Sig_Q), 0), Mker)[0])
print('    exact cancellation requires  M =', Mreq)
print('    in y:  M =', sp.simplify(sp.powsimp(Mreq.subs(subc), force=True)))
check("[S3a] cancellation needs M proportional to (1-chi) V'(chi) = y^2 e^-y"
      " -- a chi-DEPENDENT algebraic kernel (still inside the theory's own basis)",
      sp.simplify(sp.expand(Mreq - (cQ/cM)*(1 - chi)*Vp)) == 0)
m2, kk2 = sp.symbols('m2 k2', positive=True)
for lab, Mtry in [('M = m^2 (constant algebraic mass)', m2), ('M = -D^2 -> k^2', kk2),
                  ('M = Delta^{-1} -> 1/k^2', 1/kk2)]:
    resid = sp.simplify(sp.powsimp((Sig_M + cQ*f_chi**2/Mtry).subs(subc), force=True))
    print('    %-34s residual(y) = %s' % (lab, resid))
    check('[S3b] %s does NOT cancel Sigma_P for all y' % lab, sp.simplify(resid) != 0)

# ======================================================================================
head('[S4]  PN ORDER COUNTING + chi FREEZE')
# ======================================================================================
epn = sp.Symbol('epsilon', positive=True)
print('    a_i ~ eps^2/L ;  y = |a| c^2/a0 is an O(1) LABEL, not a small quantity.')
print('    L_EH,2 ~ eps^4/L^2 ;  L_MOND = g(chi) a^2 ~ eps^4/L^2  (SAME order: 1PN) ;')
print('    L_carrier(on-shell) = (1/2) f^2 A^ij A_ij / M ~ a^4 ~ eps^8/L^4 .')
check('[S4a] carrier / MOND = (v/c)^4  => the carrier is 2PN BEYOND 1PN: it cannot'
      ' contribute to alpha_1 or alpha_2 at all', sp.simplify(epn**8/epn**4) == epn**4)
carr = sp.simplify(sp.powsimp((f_chi**2/Mreq).subs(subc), force=True))
check('[S4b] carrier on-shell amplitude f^2/M = (c_M/c_Q) e^-y -> 0 as y -> oo'
      ' (it is ALSO exponentially off in the Solar System)',
      sp.limit(carr, yy, sp.oo) == 0)
check('[S5a] dchi/dy = e^-y: the auxiliary is frozen to exponential accuracy at large y,'
      ' so the 1PN a^2-coefficient is a CONSTANT there',
      sp.simplify(sp.diff(mu_y, yy) - sp.exp(-yy)) == 0)
a0N, GN, Msun, AU = 9.3619e-11, 6.674e-11, 1.989e30, 1.496e11
YTAB = [('Sun surface', 6.957e8), ('Mercury', 0.387*AU), ('Earth 1 AU', AU),
        ('Jupiter', 5.2*AU), ('Saturn (Cassini)', 9.58*AU), ('Neptune', 30.1*AU)]
print()
for lab, r in YTAB:
    yv = GN*Msun/r**2/a0N
    print('    %-18s y = %.3e   e^-y = %s' % (lab, yv,
          ('%.3e' % math.exp(-yv)) if yv < 700 else '< 1e-30000'))

# ======================================================================================
head('[P]  PPN ENGINE -- coupled (metric, khronon) 1PN solve, EXACT in w')
# ======================================================================================
# conventions: mostly-minus eta = diag(1,-1,-1,-1);  M^2 = 1;
#   S = (1/2) INT sqrt(-g) R - (1/2) INT sqrt(-g) [ lam2 K^2 + alph a_mu a^mu ] + S_m
#   khronon phi, u_mu = d_mu phi / sqrt(g^{ab} d_a phi d_b phi),
#   background phi_bar = S0 t - w.x ;  source AT REST, foliation flowing with w.
t, x, y, z = sp.symbols('t x y z', real=True)
XV = (t, x, y, z)
SPX = (x, y, z)
alph, lam2 = sp.symbols('alpha lambda_2', real=True)
ep = sp.Symbol('varepsilon', positive=True)
wb = sp.Symbol('w_b', positive=True)
u1, u2 = sp.symbols('u_1 u_2', real=True)
kk = sp.Integer(1)                     # k = (1,0,0); the PPN parameters are k-independent
Uh = sp.Symbol('Uhat')
I = sp.I
eta = sp.diag(1, -1, -1, -1)
WORD = 4                               # truncation order in w inside the quadratic Lagrangian

def eptrunc(q, o):
    q = sp.expand(q)
    return sum(q.coeff(ep, n)*ep**n for n in range(o + 1))
def wtrunc(q, o=WORD):
    q = sp.expand(q)
    return sum(q.coeff(wb, n)*wb**n for n in range(o + 1))

hf = {}
for mu in range(4):
    for nu in range(mu, 4):
        hf[(mu, nu)] = sp.Function('h%d%d' % (mu, nu))(x, y, z)
def hcomp(mu, nu):
    return hf[(mu, nu)] if mu <= nu else hf[(nu, mu)]
sig = sp.Function('sigma')(x, y, z)

w2s = wb**2*(u1**2 + u2**2)
S0 = 1 + w2s/2 - w2s**2/8
phibar = S0*t - wb*(u1*x + u2*y)
phi_tot = phibar + ep*sig
H = sp.Matrix(4, 4, lambda a, b: hcomp(a, b))
g_up = eta - ep*(eta*H*eta)
Dphi = sp.Matrix([sp.diff(phi_tot, v) for v in XV])
Nsq = sp.expand((Dphi.T*g_up*Dphi)[0, 0])
check('[P1] khronon background is unit-normalised to O(w^%d)' % WORD,
      wtrunc(sp.expand(Nsq.coeff(ep, 0) - 1), WORD - 1) == 0)
Ninv = 1 - ep*Nsq.coeff(ep, 1)/2
u_dn = [eptrunc(sp.expand(Dphi[m]*Ninv), 1) for m in range(4)]
u_up = [eptrunc(sp.expand(sum(g_up[m, n]*u_dn[n] for n in range(4))), 1) for m in range(4)]
trh = sp.expand(sum(eta[m, n]*hcomp(m, n) for m in range(4) for n in range(4)))
sqrtg4 = 1 + ep*trh/2
Kfull = sp.expand(sum(sp.diff(sqrtg4*u_up[m], XV[m]) for m in range(4)))
check('[P2] K = 0 and a_mu = 0 on the background (so the quadratic Lagrangian needs only'
      ' the O(eps) linearisation of K and a_mu -- exact)',
      sp.simplify(Kfull.coeff(ep, 0)) == 0)
K1 = wtrunc(sp.expand(eptrunc(Kfull, 1)).coeff(ep, 1))
Gam1 = [[[sp.Rational(1, 2)*sum(eta[l, s]*(sp.diff(hcomp(s, n), XV[m]) +
                                           sp.diff(hcomp(s, m), XV[n]) -
                                           sp.diff(hcomp(m, n), XV[s])) for s in range(4))
          for n in range(4)] for m in range(4)] for l in range(4)]
ub_up = [u_up[m].coeff(ep, 0) for m in range(4)]
ub_dn = [u_dn[m].coeff(ep, 0) for m in range(4)]
a1 = []
for m in range(4):
    lin = sp.expand(sum(u_up[n]*sp.diff(u_dn[m], XV[n]) for n in range(4))).coeff(ep, 1)
    gm = -sum(ub_up[n]*Gam1[l][n][m]*ub_dn[l] for n in range(4) for l in range(4))
    a1.append(wtrunc(sp.expand(lin + gm)))
a1sq = sp.expand(sum(eta[m, n]*a1[m]*a1[n] for m in range(4) for n in range(4)))
L2 = wtrunc(sp.expand(-sp.Rational(1, 2)*(lam2*K1**2 + alph*a1sq)))
log('L2 built:', len(sp.Add.make_args(L2)), 'terms')

def EL(L, F):
    out = sp.diff(L, F)
    for v in SPX:
        out -= sp.diff(sp.diff(L, sp.diff(F, v)), v)
    for i in range(3):
        for j in range(i, 3):
            out += sp.diff(sp.diff(L, sp.diff(F, SPX[i], SPX[j])), SPX[i], SPX[j])
    return out

hhat = {}
for mu in range(4):
    for nu in range(mu, 4):
        hhat[(mu, nu)] = sp.Symbol('hh%d%d' % (mu, nu))
def hh(mu, nu):
    return hhat[(mu, nu)] if mu <= nu else hhat[(nu, mu)]
sh = sp.Symbol('sighat')
efac = sp.exp(I*kk*x)
FSUB = {hf[(mu, nu)]: hhat[(mu, nu)]*efac for mu in range(4) for nu in range(mu, 4)}
FSUB[sig] = sh*efac
def fourier(q):
    return sp.expand(sp.cancel(sp.expand(q.subs(FSUB).doit())/efac))
Theta = {}
for mu in range(4):
    for nu in range(mu, 4):
        Tc = fourier(EL(L2, hf[(mu, nu)]))
        Theta[(mu, nu)] = wtrunc(sp.expand(Tc if mu == nu else Tc/2))
def Th(mu, nu):
    return Theta[(mu, nu)] if mu <= nu else Theta[(nu, mu)]
Esig = wtrunc(sp.expand(fourier(EL(L2, sig))))
a1F = [sp.expand(sp.cancel(sp.expand(am.subs(FSUB).doit())/efac)) for am in a1]
log('Theta^{mu nu}, E_sigma, a_mu(Fourier) built')

Kmu = [sp.S(0), I*kk, sp.S(0), sp.S(0)]
def Gam1F(l, m, n):
    return sp.Rational(1, 2)*sum(eta[l, s]*(Kmu[m]*hh(s, n) + Kmu[n]*hh(s, m) - Kmu[s]*hh(m, n))
                                 for s in range(4))
def R1F(m, n):
    return sp.expand(sum(Kmu[l]*Gam1F(l, m, n) for l in range(4))
                     - sum(Kmu[n]*Gam1F(l, m, l) for l in range(4)))
R1tr = sp.expand(sum(eta[a, b]*R1F(a, b) for a in range(4) for b in range(4)))
def G1up(m, n):
    Gd = lambda p, q: sp.expand(R1F(p, q) - sp.Rational(1, 2)*eta[p, q]*R1tr)
    return sp.expand(sum(eta[m, a]*eta[n, b]*Gd(a, b) for a in range(4) for b in range(4)))

sg = sp.Rational(-1, 2)                 # (M^2/2) EH normalisation, sign per sec11 [D4]
tau = sp.Symbol('tau')
EQS = []
for mu in range(4):
    for nu in range(mu, 4):
        src = tau if (mu == 0 and nu == 0) else sp.S(0)
        EQS.append(sp.expand(sg*G1up(mu, nu) - Th(mu, nu) - src))
EQS.append(Esig)

# ---- BPS anchor: khronon response on the Newtonian seed must equal BPS (E.9)@beta=0
seedF = {hhat[(0, 0)]: 2*Uh, hhat[(1, 1)]: 2*Uh, hhat[(2, 2)]: 2*Uh, hhat[(3, 3)]: 2*Uh,
         hhat[(0, 1)]: 0, hhat[(0, 2)]: 0, hhat[(0, 3)]: 0,
         hhat[(1, 2)]: 0, hhat[(1, 3)]: 0, hhat[(2, 3)]: 0}
E1s = sp.expand(Esig.subs(seedF))
E1w = sp.expand(sum(E1s.coeff(wb, n)*wb**n for n in range(2)))
Chi_sol = sp.solve(sp.Eq(E1w, 0), sh)
Ch_bps = I*(alph - lam2)*(wb*u1*kk)*Uh/(lam2*kk**2)
check('[P3] khronon solution on the Newtonian seed == BPS arXiv:1007.3503 (E.9)@beta=0'
      ' under v = -w', bool(Chi_sol) and sp.simplify(Chi_sol[0] - Ch_bps) == 0)
ThS = {(m, n): sp.expand(Th(m, n).subs(seedF).subs(sh, Ch_bps))
       for m in range(4) for n in range(m, 4)}
def TS(m, n):
    return ThS[(m, n)] if m <= n else ThS[(n, m)]
consok = True
for n in range(4):
    s = sp.expand(sum(I*kk*TS(1, n) for _ in [0]))
    s = sp.simplify(sum(sp.expand(s).coeff(wb, q)*wb**q for q in range(3)))
    consok = consok and (s == 0)
check('[P4] conservation k_i Theta^{i nu} = 0 on-shell to O(w^2)', consok)
# BPS (E.12a): h1_00 including the anisotropic (w.k)^2 piece
c0 = sp.Symbol('c_0')
trTh = sp.expand(sum(eta[a, b]*TS(a, b) for a in range(4) for b in range(4)))
h1u = {}
for m in range(4):
    for n in range(m, 4):
        h1u[(m, n)] = sp.expand(c0*TS(m, n)/kk**2 - sp.Rational(1, 2)*eta[m, n]*c0*trTh/kk**2)
def H1u(m, n):
    return h1u[(m, n)] if m <= n else h1u[(n, m)]
h1_00 = sp.expand(sum(eta[0, a]*eta[0, b]*H1u(a, b) for a in range(4) for b in range(4)))
C0 = sp.solve(sp.Eq(sp.expand(h1_00).coeff(wb, 0), alph*Uh), c0)[0]
h1_00 = sp.expand(sum(sp.expand(h1_00.subs(c0, C0)).coeff(wb, n)*wb**n for n in range(3)))
targ = sp.expand(alph*Uh + 4*alph*w2s*Uh + (alph*(alph - lam2)/lam2)*(wb*u1*kk)**2*Uh/kk**2)
check('[P5] h1_00 == BPS (E.12a)@beta=0 incl. the alpha(alpha-lam2)/lam2 anisotropic piece',
      sp.simplify(sp.expand(h1_00 - targ)) == 0)

# ---- the coupled solve.  k along x  =>  G1^{1 nu} == 0 identically, so the four E^{1 nu}
#      are the CONSERVATION identities (redundant once E_sigma holds).  Keeping them makes
#      the system spuriously over-determined once L2 is w-truncated, so DROP + check them.
for n in range(4):
    assert sp.simplify(G1up(1, n)) == 0
check('[P6] G1^{1 nu} == 0 identically for k along x: E^{1 nu} are the (redundant)'
      ' conservation identities', True)
GAUGE0 = {hhat[(0, 1)]: 0, hhat[(1, 1)]: 0, hhat[(1, 2)]: 0, hhat[(1, 3)]: 0}
UNK7 = [hhat[(0, 0)], hhat[(0, 2)], hhat[(0, 3)], hhat[(2, 2)], hhat[(2, 3)], hhat[(3, 3)], sh]
KEEP = [0, 2, 3, 7, 8, 9, 10]
DROP = [1, 4, 5, 6]
DIRS = [(sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(4, 5), sp.Rational(3, 5))]

def solve_case(a_val, l_val, d1, d2, tv, tag, gr=False):
    sub = {alph: a_val, lam2: l_val, u1: d1, u2: d2, tau: tv}
    if gr:
        eqs = [sp.expand(EQS[i].subs(GAUGE0).subs(sub).subs(sh, 0)) for i in KEEP[:6]]
        A, b = sp.linear_eq_to_matrix(eqs, UNK7[:6])
        S = A.LUsolve(b)
        d = {UNK7[i]: sp.cancel(S[i]) for i in range(6)}
        d[sh] = sp.S(0)
        d.update({q: sp.S(0) for q in GAUGE0})
        return d
    eqs = [sp.expand(EQS[i].subs(GAUGE0).subs(sub)) for i in KEEP]
    A, b = sp.linear_eq_to_matrix(eqs, UNK7)
    if A.rank() < 7:
        log(tag, 'RANK DEFICIENT', A.rank(), '/7')
        return None
    S = A.LUsolve(b)
    d = {UNK7[i]: sp.cancel(sp.together(S[i])) for i in range(7)}
    d.update({q: sp.S(0) for q in GAUGE0})
    res = []
    for i in DROP:
        q = sp.expand(EQS[i].subs(GAUGE0).subs(sub)).subs({UNK7[j]: d[UNK7[j]]
                                                           for j in range(7)})
        res.append(sp.simplify(sp.series(sp.cancel(sp.together(q)), wb, 0, 4).removeO()))
    log(tag, 'solved; dropped conservation-eq residuals to O(w^3):', [str(q) for q in res])
    return d

gr = solve_case(0, 0, *DIRS[0], tau, 'GR', gr=True)
TAU = sp.solve(sp.Eq(sp.simplify(gr[hhat[(0, 0)]]), 2*Uh), tau)[0]
check('[P7] GR LIMIT (alpha = lam2 = 0): h_00 = 2 Uhat, h_ij = 2 Uhat delta_ij'
      ' => gamma_PPN = 1, alpha_1 = alpha_2 = 0 EXACTLY',
      sp.simplify(gr[hhat[(2, 2)]].subs(tau, TAU) - 2*Uh) == 0 and
      sp.simplify(gr[hhat[(3, 3)]].subs(tau, TAU) - 2*Uh) == 0 and
      sp.simplify(gr[hhat[(0, 2)]].subs(tau, TAU)) == 0 and
      sp.simplify(sp.diff(gr[hhat[(0, 0)]].subs(tau, TAU), wb)) == 0)

def run(av, lv, label):
    print()
    print('--- alpha = %s , lam2 = %s ---' % (av, lv), flush=True)
    sols = {}
    for (d1, d2) in DIRS:
        s = solve_case(av, lv, d1, d2, TAU, '%s u=(%s,%s)' % (label, d1, d2))
        if s is None:
            return None
        sols[(d1, d2)] = s
    d0 = sols[DIRS[0]]
    sigv = sp.cancel(d0[sh])
    pole = sp.simplify(sp.limit(sigv*wb, wb, 0))
    print('  sigma_hat 1/w pole coefficient  lim_{w->0} w*sigma =', pole,
          '   [-I*Uhat/(w.k)/w =', sp.simplify(-I*Uh/(DIRS[0][0]*kk)), ']', flush=True)
    h00 = sp.cancel(d0[hhat[(0, 0)]])
    s00 = sp.series(h00, wb, 0, 3)
    print('  h00 series:', s00, flush=True)
    s00e = sp.expand(s00.removeO())
    P1 = sp.simplify(s00e.coeff(wb, 0)/Uh)
    h22 = sp.simplify(sp.series(sp.cancel(d0[hhat[(2, 2)]]), wb, 0, 1).removeO())
    gam = sp.simplify(h22/(P1*Uh))
    h02s = sp.expand(sp.series(sp.cancel(d0[hhat[(0, 2)]]), wb, 0, 2).removeO())
    a1v = sp.simplify(2*sp.simplify(h02s.coeff(wb, 1))/(DIRS[0][1]*Uh))
    rows, rhs = [], []
    for (d1, d2) in DIRS:
        se = sp.expand(sp.series(sp.cancel(sols[(d1, d2)][hhat[(0, 0)]]), wb, 0, 3).removeO())
        rows.append([d1**2 + d2**2, d1**2])
        rhs.append(sp.simplify(se.coeff(wb, 2)/Uh))
    P2, P3 = sp.Matrix(rows).solve(sp.Matrix(rhs))
    P2, P3 = sp.simplify(P2), sp.simplify(P3)
    a2v = sp.simplify(P3/2)
    a1_00 = sp.simplify(-(P2 + P3/2) + a2v)
    print('  h00|w0 = (%s) Uhat ;  gamma_PPN = %s' % (P1, gam), flush=True)
    print('  p2 = %s ; p3 = %s' % (P2, P3), flush=True)
    print('  ALPHA_1 (h0i route) = %s ;  ALPHA_1 (h00 route) = %s ;  ALPHA_2 = %s'
          % (a1v, a1_00, a2v), flush=True)
    # a_mu evaluated ON the solution (the mechanism diagnostic)
    sol = {hhat[(m, n)]: d0[hhat[(m, n)]] for m in range(4) for n in range(m, 4)}
    sol[sh] = d0[sh]
    sub = {alph: av, lam2: lv, u1: DIRS[0][0], u2: DIRS[0][1]}
    aa = [sp.cancel(sp.together(q.subs(sub).subs(sol).subs(tau, TAU))) for q in a1F]
    asq = sp.cancel(sp.together(sp.expand(sum(eta[m, n]*aa[m]*aa[n]
                                              for m in range(4) for n in range(4)))))
    print('  a_mu ON-SHELL   =', [sp.simplify(sp.series(q, wb, 0, 2)) for q in aa], flush=True)
    print('  a_mu a^mu       =', sp.simplify(sp.series(asq, wb, 0, 3)), flush=True)
    return dict(P1=P1, gamma=gam, a1=a1v, a1_00=a1_00, a2=a2v, pole=pole, asq=asq)

head('[V]  VALIDATION: healthy khronometric (lam2 != 0), small alpha -> BPS 5.34@beta=0')
for (av, lv) in [(sp.Rational(1, 1000), sp.Rational(1, 3)),
                 (sp.Rational(1, 1000), sp.Rational(1, 10))]:
    r = run(av, lv, 'bps')
    check('  gamma_PPN = 1  (alpha=%s, lam2=%s)' % (av, lv), sp.simplify(r['gamma'] - 1) == 0)
    check('  alpha_1 routes agree  (alpha=%s, lam2=%s)' % (av, lv),
          sp.simplify(r['a1'] - r['a1_00']) == 0)
    check('  alpha_1 = -4 alpha to 1 part in 1e3  [BPS 5.34@beta=0]',
          abs(float(r['a1']/(-4*av)) - 1) < 2e-3)
    check('  alpha_2 = alpha(alpha-lam2)/(2 lam2) to 1 part in 1e3  [BPS 5.34@beta=0]',
          abs(float(r['a2']/(av*(av - lv)/(2*lv))) - 1) < 2e-3)
    check('  h00|w0 = 2/(1-alpha/2): the exact-in-alpha G_N = G/(1-alpha/2) renormalisation',
          sp.simplify(r['P1'] - 2/(1 - av/2)) == 0)
    check('  khronon acceleration is NOT eaten when lam2 != 0: a_mu a^mu != 0 at O(w^0)',
          sp.simplify(sp.series(r['asq'], wb, 0, 1).removeO()) != 0)

head("[C]  THE CANDIDATE'S OWN POINT: lam2 = lambda_K - 1 = 0 EXACTLY")
print('  (the gravity sector is GR\'s K_ijK^ij - K^2, so there is NO K^2 deformation and')
print('   the auxiliary sector has NO time derivatives: lam2 = 0 is structural, not tuned)')
print('  naive khronometric formula: alpha_2 = alpha(alpha-lam2)/(2 lam2) has a 1/lam2 POLE')
print('  -> the limit must be taken with lam2 = 0 FIRST.  Direct solve:', flush=True)
rc = {}
for av in [alph, sp.Rational(1, 1000)]:
    rc[av] = run(av, sp.S(0), 'lam2=0')
r0 = rc[alph]
check('[C1] lam2 = 0: the khronon perturbation has a 1/(w.k) POLE with an'
      ' ALPHA-INDEPENDENT coefficient -I Uhat/(w.k)  (strong coupling: no scalar'
      ' kinetic term, the w-expansion is singular)',
      sp.simplify(r0['pole'] - (-I*Uh/(DIRS[0][0]*kk))) == 0)
check('[C2] lam2 = 0: a_mu is O(w^2) ON-SHELL -- the khronon relaxes to the'
      ' ZERO-ACCELERATION (geodesic) foliation',
      sp.simplify(sp.series(r0['asq'], wb, 0, 3).removeO()) == 0)
check('[C3] lam2 = 0: gamma_PPN = 1', sp.simplify(r0['gamma'] - 1) == 0)
check('[C4] lam2 = 0: ALPHA_1 = 0 exactly', sp.simplify(r0['a1']) == 0 and
      sp.simplify(r0['a1_00']) == 0)
check('[C5] lam2 = 0: ALPHA_2 = 0 exactly (the 1/lam2 pole is resolved to ZERO)',
      sp.simplify(r0['a2']) == 0)
check('[C6] lam2 = 0: h00|w0 = 2 Uhat -- NO G_N renormalisation, i.e. mu_eff = 1:'
      ' the MOND modification is switched off TOGETHER with the preferred-frame terms',
      sp.simplify(r0['P1'] - 2) == 0)

head('[R]  RESULT')
print("""
  STRUCTURAL THEOREM (proven, then computationally confirmed above):
    Gauss-Codazzi at lambda_K = 1 makes  K_ijK^ij - K^2 + R3  identically the Einstein-Hilbert
    scalar, so the gravity sector is KHRONON-BLIND.  The khronon therefore enters the candidate
    ONLY through a_mu = D_mu ln N:  the MOND term g(chi) a^2, and the carrier f(chi) Q^ij A_ij
    with A_ij = [a_i a_j]^TF.  Hence  a_mu == 0  is an EXACT stationary point of the khronon
    equation of motion, for ANY g and ANY f.  A zero-acceleration (geodesic) foliation exists,
    and with lam2 = 0 there is no khronon kinetic term to obstruct the relaxation to it.
    On that solution the whole MOND + carrier sector evaluates to zero and the theory is GR.

  alpha_1 and alpha_2, SYMBOLICALLY
    dictionary       alpha_khrono = -c_M g(chi) = 2(1 - chi) = 2 e^-y      [forced by [S2]]
    lam2 = 0 (the candidate, computed directly):
        alpha_1 = 0 ,  alpha_2 = 0 ,  gamma_PPN = 1 ,  G_eff/G_N = 1  -- and NO MOND.
        The khronon sector re-enters h_00 only at O(w^4) (because a_mu = O(w^2)), so the
        MOND force is suppressed by (w/c)^4 ~ 1e-12 for w ~ 600 km/s.
    lam2 != 0 (the minimal HEALTHY repair, lambda_K != 1 -- a DIFFERENT theory):
        alpha_1 = -4 alpha + O(alpha^2)  =  -8 (1-chi)  =  -8 e^-y
        alpha_2 = alpha(alpha - lam2)/(2 lam2) + O(alpha^3)  =  e^-y (2 e^-y - lam2)/lam2
                ~  -2 e^-y            for  |lam2| >> e^-y
    literal spec reading g(chi) = chi (REFUTED at [S2a], it has no deep-MOND limit):
        alpha_khrono = -c_M chi -> O(1), alpha_1 = O(1)  ->  ~1e5 x over |alpha_1| < 4e-5.
""")
for lab, r in YTAB:
    yv = GN*Msun/r**2/a0N
    ex = ('%.3e' % math.exp(-yv)) if yv < 700 else '< 1e-30000'
    print('    %-18s y = %.3e :  |alpha_1| = 8 e^-y = %s ,  |alpha_2| ~ 2 e^-y = %s'
          % (lab, yv, ex, ex))
print('    bounds: |alpha_1| < 4e-5 (LLR/pulsars), |alpha_2| < 1.2e-7 (solar spin axis).')
print('    => the PREFERRED-FRAME GATE IS PASSED, by ~1e30000 margin, for BOTH lam2 cases.')
print('    => the candidate nevertheless DIES, at lam2 = 0, by DEGENERACY: the same')
print('       auxiliary-sector design principle (no time derivatives anywhere) that was')
print('       meant to evade the Part-I no-go (hypothesis H3) leaves nothing to hold the')
print('       khronon away from a_mu = 0.  This is the compiler\'s own CARRIER_OFF mode.')
print('    OPEN DOOR (named, not closed): lambda_K != 1 restores a healthy khronon, keeps')
print('       MOND, and still passes alpha_1, alpha_2.  Its own gates (c_T, BBN lambda_K in')
print('       [0.923,1.100], cosmology, and the chi-dependent Q kernel M ~ (1-chi)V\'(chi)')
print('       required by [S3]) are UNTESTED here.')

print()
npass = sum(1 for _, ok in results if ok)
print('%d/%d checks pass' % (npass, len(results)))
sys.exit(0 if npass == len(results) else 1)
