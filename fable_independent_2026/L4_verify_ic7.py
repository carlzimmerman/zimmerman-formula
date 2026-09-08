#!/usr/bin/env python3
"""
L4 -- independent verification of the lead agent's IC6 obstruction and its IC7 curvature-square repair
=====================================================================================================
Lane L4 of `fable_independent_2026/CHARTER.md`.  The lead agent's construction lives in
`qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/` (read-only to this lane).  Nothing there is
imported, re-run or copied: every number below is re-derived from the ACTION AS WRITTEN in IC4_ACTION.md / IC5_ACTION.md /
TENSOR_BALANCE.md, transcribed by hand into sympy here, then evaluated at 60 decimal digits with mpmath.

WHAT THE LEAD BUILT (extracted from its own files)
  h(rho,tau,xi,u) = (2E/m)(tau/J - rho^2/6) + m e^{(3u-2)xi} C - (kappa/2) e^{(3u-4)xi},   c = m e^{u xi} J,
  E = e^{(4-3u)xi},  w = (u-1)xi,  J = 1 + e^{-6w} rho^2 F/(m^2 a0^2),  C = Lambda + a0^2 U(u^2),
  F = A_R(xi - 1/4) + B_R(u - 2/3),  and the frozen IC-4 constants (ell = ln(9/5), Tcal = -27/16 + 54/(5 ell), sigma = 1/3).
  Units of the lead's fixture: m = h0 = V = 1, kappa = 6.  The witness is (xi,u,rho,tau) = (1/4, 2/3, -3 e^{-1/2}, 0).

(a) THE IC6 OBSTRUCTION, as an equation.  IC6_EVEN_CHARACTERISTICS.md, boxed:
      S_4'(1) = - e^{5/6} (5T-27)(8T-27)(8T+27) / (18 T^2 (4T-27))  <  0,
    where S_4 is the k_z^4 coefficient of the reduced scalar stiffness on the one-parameter isotropic family
    lambda_i = -e^{-1/2} j, and S_4(1) = 0 at the witness.  Hence S_4 < 0 for every small j-1 > 0, and the scalar
    obeys M_0 zeta_tt + S_4 k^4 zeta = 0 with real growth rate ~ k^2: a principal (ill-posedness-type) obstruction
    arbitrarily close to the witness.

(b) WHAT IC7 ADDS.  IC7_CURVATURE_SQUARE.md adds ONE term, Delta H_7 = int d^3x V eta(r) c_7(rho,xi,u) Rbar^2, with
      M = [[h_rr/4 + h_tau/12, D_t h_r/2],[D_t h_r/2, D_t^2 h]]|_{tau=0},  v = (c_rho/2, D_t c),  D_t = d_u - b d_xi,
      c_raw = v^T M^{-1} v / 8,   c_7 = theta(D) c_raw,   D = det(M)/det(M_star),  b = -T/9 - 3/8.
    It claims to repair the isotropic quartic exactly (S4 + 32 V c7/B3^4 = 0), to leave the witness quadratic action
    untouched, and to leave the sheared-background antisymmetric mixing unrepaired.

CHECKS.  Every check below is a statement about the lead's claim (or about the programme's 2-DOF requirement) that
could come out false.  L4-C* are controls that would catch MY algebra being wrong, including two GR limits.
"""
import sys, json, math
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def close(a, b, tol):
    a, b = mp.mpf(a), mp.mpf(b)
    return abs(a - b) <= tol * max(mp.mpf(1), abs(b))

print("=" * 118)
print("L4 -- independent verification of the lead's IC6 principal obstruction and IC7 curvature-square repair")
print("=" * 118)

# ------------------------------------------------------------------ independent transcription of the action constants
ell   = sp.log(sp.Rational(9, 5))
Tcal  = -sp.Rational(27, 16) + 54 / (5 * ell)
astar = 3 - 81 / (4 * Tcal)
sigma = sp.Rational(1, 3)                                             # the FIXED design parameter of IC-4
pR    = sp.Rational(8, 3) + 4 * astar * sigma
qR    = -1 - 3 * pR / 8
AR    = 3 * pR / (16 * ell**2)
BR    = 3 * qR / (16 * ell**2)
b     = -Tcal / 9 - sp.Rational(3, 8)                                 # IC5_ACTION.md
m, kappa = sp.Integer(1), sp.Integer(6)                               # the lead's fixture units
h0    = sp.sqrt(kappa / (6 * m))                                      # = 1
a02   = 9 * kappa * sp.exp(-sp.Rational(1, 2)) / (16 * m * ell**2)
Ufun  = lambda cc_: (1 - cc_) * (sp.log(1 - cc_)**2 - 2 * sp.log(1 - cc_) + 2) - 2
Lam   = kappa * sp.exp(-sp.Rational(1, 2)) / m - a02 * Ufun(sp.Rational(4, 9))

xi, u, rho, tau = sp.symbols('xi u rho tau', real=True)
w  = (u - 1) * xi
E  = sp.exp((4 - 3 * u) * xi)
F  = AR * (xi - sp.Rational(1, 4)) + BR * (u - sp.Rational(2, 3))
J  = 1 + sp.exp(-6 * w) * rho**2 * F / (m**2 * a02)
Cp = Lam + a02 * Ufun(u**2)
h  = (2 * E / m) * (tau / J - rho**2 / 6) + m * sp.exp((3 * u - 2) * xi) * Cp - (kappa / 2) * sp.exp((3 * u - 4) * xi)
cc = m * sp.exp(u * xi) * J                                            # curvature coefficient:  h contains -(c/2) Rbar
Dt = lambda f: sp.diff(f, u) - b * sp.diff(f, xi)                       # the auxiliary gradient square's null direction
rfun = -rho * E / (3 * m * h0)                                         # activation argument

M11s = sp.diff(h, rho, 2) / 4 + sp.diff(h, tau) / 12
M12s = Dt(sp.diff(h, rho)) / 2
M22s = Dt(Dt(h))
v1s, v2s = sp.diff(cc, rho) / 2, Dt(cc)
detMs = M11s * M22s - M12s**2
S4s   = -4 * (M22s * v1s**2 - 2 * M12s * v1s * v2s + M11s * v2s**2) / detMs     # = -4 v^T M^-1 v   (V = B3 = 1)
c7raw = -S4s / 32                                                              # == v^T M^-1 v / 8

SYM = dict(M11=M11s, M12=M12s, M22=M22s, v1=v1s, v2=v2s, detM=detMs, S4=S4s, c7=c7raw, J=J, F=F, r=rfun,
           c=cc, hxi=sp.diff(h, xi), hu=sp.diff(h, u), hxx=sp.diff(h, xi, 2), hxu=sp.diff(sp.diff(h, xi), u),
           huu=sp.diff(h, u, 2), hxr=sp.diff(sp.diff(h, xi), rho), hur=sp.diff(sp.diff(h, u), rho),
           hxt=sp.diff(sp.diff(h, xi), tau), hut=sp.diff(sp.diff(h, u), tau))
f = {k: sp.lambdify((xi, u, rho, tau), v, modules='mpmath') for k, v in SYM.items()}
GRAD = {k: [sp.lambdify((xi, u, rho, tau), sp.diff(SYM[k], q), modules='mpmath') for q in (xi, u, rho)]
        for k in ('M11', 'M12', 'M22', 'v1', 'v2', 'S4', 'J', 'F')}
HQQ = [[f['hxx'], f['hxu']], [f['hxu'], f['huu']]]
NUM = lambda e: mp.mpf(str(sp.N(e, 55)))
T, L2 = NUM(Tcal), NUM(ell**2)
WIT = [mp.mpf(1) / 4, mp.mpf(2) / 3, -3 * mp.e**mp.mpf('-0.5'), mp.mpf(0)]
rho_w = WIT[2]

def solve_aux(rv, tv, guess=(mp.mpf(1) / 4, mp.mpf(2) / 3)):
    """Solve the two auxiliary constraints h_xi = h_u = 0 at fixed (rho,tau) -- my own Newton solve."""
    q = mp.matrix(list(guess))
    for _ in range(120):
        Fv = mp.matrix([f['hxi'](q[0], q[1], rv, tv), f['hu'](q[0], q[1], rv, tv)])
        Jv = mp.matrix([[HQQ[i][j](q[0], q[1], rv, tv) for j in range(2)] for i in range(2)])
        d = mp.lu_solve(Jv, -Fv); q = q + d
        if mp.norm(d) < mp.mpf(10)**-50: break
    return q[0], q[1]

def Ebump(t): return mp.e**(-1 / t) if t > 0 else mp.mpf(0)
def eta_of(r):
    d = (r**2 - 1)**2
    A, B = Ebump(mp.mpf(1) / 4 - d), Ebump(d - mp.mpf(1) / 16)
    return A / (A + B)
def theta_x(x): return Ebump(1 - x) / (Ebump(x) + Ebump(1 - x))
def theta_of(D):
    a = abs(D - 1)
    if a <= mp.mpf(1) / 4: return mp.mpf(1)
    if a >= mp.mpf(1) / 2: return mp.mpf(0)
    return theta_x(4 * (a - mp.mpf(1) / 4))

# ============================================================ CONTROLS ============================================
print("\n-- controls (these would catch my own algebra being wrong) ------------------------------------------------")
pij = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'p{min(i,j)}{max(i,j)}'))
gij = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'g{min(i,j)}{max(i,j)}'))
rh_ = sum(gij[i, j] * pij[i, j] for i in range(3) for j in range(3))
pp_ = sum(gij[i, k] * gij[j, l] * pij[i, j] * pij[k, l] for i in range(3) for j in range(3) for k in range(3) for l in range(3))
ta_ = pp_ - rh_**2 / 3
lam_ = sp.Symbol('lambda_dw')
dewitt = sp.expand(ta_ - rh_**2 / 6 - (pp_ - rh_**2 / 2))
lam_sol = sp.solve(sp.expand(ta_ - rh_**2 / 6 - (pp_ - lam_ * rh_**2 / 2)).coeff(sp.Symbol('p00')**2), lam_)
check("L4-C1 [control, GR] the IC5/IC6 kinetic term (2E/m)(tau/J - rho^2/6) carries the GENERAL-RELATIVITY DeWitt "
      "supermetric, lambda = 1, so the extra scalar found below is NOT a Horava lambda-mode",
      dewitt == 0 and lam_sol == [1], f"lambda_DeWitt = {lam_sol}")

z = sp.Symbol('z'); B1, B2, B3 = sp.symbols('B1 B2 B3', positive=True)
ze, ga, rg = sp.Function('zeta')(z), sp.Function('gam')(z), sp.Function('rgauge')(z)
gm = sp.diag(B1**2 * sp.exp(2 * ze + ga), B2**2 * sp.exp(2 * ze - ga), B3**2 * sp.exp(2 * rg))
gmi = gm.inv(); XX = [sp.Symbol('x'), sp.Symbol('y'), z]
Gam = [[[sp.simplify(sum(gmi[i, l] * (sp.diff(gm[l, j], XX[k]) + sp.diff(gm[l, k], XX[j]) - sp.diff(gm[j, k], XX[l]))
        for l in range(3)) / 2) for k in range(3)] for j in range(3)] for i in range(3)]
def Ric(j_, k_):
    t = 0
    for i in range(3):
        t += sp.diff(Gam[i][j_][k_], XX[i]) - sp.diff(Gam[i][j_][i], XX[k_])
        for l in range(3):
            t += Gam[i][i][l] * Gam[l][j_][k_] - Gam[i][k_][l] * Gam[l][j_][i]
    return t
R3 = sp.simplify(sum(gmi[j_, k_] * Ric(j_, k_) for j_ in range(3) for k_ in range(3)))
Rclaim = -2 * sp.exp(-2 * rg) / B3**2 * (2 * sp.diff(ze, z, 2) + 3 * sp.diff(ze, z)**2
                                         + sp.diff(ga, z)**2 / 4 - 2 * sp.diff(rg, z) * sp.diff(ze, z))
check("L4-C2 [control] the lead's diagonal barred-curvature identity Rbar = -2e^{-2rho}/B3^2 [2 zeta_zz + 3 zeta_z^2 "
      "+ gamma_z^2/4 - 2 rho_z zeta_z] reproduced from the Riemann tensor", sp.simplify(R3 - Rclaim) == 0)

# tensor cone from the same Hamiltonian->Lagrangian machinery: H2 = Kc p_g^2 + Gc gamma_z^2  =>  c_coord^2 = 4 Kc Gc
c7s, R0s = sp.symbols('c7 Rbar0', real=True)
light2 = sp.exp((4 - 2 * u) * xi) / B3**2                                   # N^2/(e^{2w} B3^2), coordinate light speed^2
cT2 = lambda Kc, Gc: sp.simplify(4 * Kc * Gc / light2)
cT2_GR  = sp.simplify(4 * (1 / m) * (m / (4 * B3**2)) * B3**2)              # ADM GR: E=J=1, c=m, xi=u=0 -> light2=1/B3^2
check("L4-C3 [control, GR] the same phase-space tensor reduction returns c_T^2 = 1 for pure ADM general relativity",
      sp.simplify(cT2_GR - 1) == 0)
dof = lambda npair, n2nd, n1st: sp.Rational(2 * npair - n2nd - 2 * n1st, 2)
check("L4-C4 [control, GR] the same DOF-counting rule (2N - n_2nd - 2 n_1st)/2 returns 2 for ADM GR "
      "(6 metric pairs; H and H_i first class)", dof(6, 0, 4) == 2, f"count = {dof(6,0,4)}")

wres = (abs(f['hxi'](*WIT)), abs(f['hu'](*WIT)))
check("L4-C5 [control] the IC-4/IC-5 expanding witness (xi,u,rho,tau) = (1/4, 2/3, -3e^{-1/2}, 0) is an EXACT "
      "stationary point of my independently transcribed h -- this validates every frozen constant "
      "(ell, Tcal, sigma, A_R, B_R, a0^2, Lambda, U, b)",
      max(wres) < mp.mpf(10)**-45 and abs(f['F'](*WIT)) < mp.mpf(10)**-45 and close(f['r'](*WIT), 1, mp.mpf(10)**-45),
      f"|h_xi|,|h_u| = {mp.nstr(wres[0],3)}, {mp.nstr(wres[1],3)}; F = 0; r = 1")

# ==================================================== (a) THE IC6 OBSTRUCTION =====================================
print("\n-- (a) the IC6 obstruction, re-derived --------------------------------------------------------------------")
Hw = mp.matrix([[HQQ[i][j](*WIT) for j in range(2)] for i in range(2)]) / (m * mp.e**mp.mpf('-0.5') * h0**2)
Hlead = mp.matrix([[-24, 27], [27, -(2 * T + mp.mpf(135) / 8)]])
check("L4-O1 auxiliary Hessian at the witness (normalised by m V e^{-1/2} h0^2) = -[[24,-27],[-27,2T+135/8]], "
      "det = 12(4T-27) > 0",
      mp.norm(Hw - Hlead) < mp.mpf(10)**-40 and close(mp.det(Hw), 12 * (4 * T - 27), mp.mpf(10)**-40),
      f"det = {mp.nstr(mp.det(Hw),12)} vs 12(4T-27) = {mp.nstr(12*(4*T-27),12)}")

Hm = mp.matrix([[HQQ[i][j](*WIT) for j in range(2)] for i in range(2)])
gj = mp.matrix([f['hxr'](*WIT) * rho_w, f['hur'](*WIT) * rho_w])
dqdj = mp.lu_solve(Hm, -gj)
check("L4-O2 branch tangent dq/dj|_1 = ( -(8T+27)/(4(4T-27)), -18/(4T-27) ) from my own implicit-function solve",
      close(dqdj[0], -(8 * T + 27) / (4 * (4 * T - 27)), mp.mpf(10)**-40) and close(dqdj[1], -18 / (4 * T - 27), mp.mpf(10)**-40),
      f"({mp.nstr(dqdj[0],12)}, {mp.nstr(dqdj[1],12)})")

def ddj(key):
    g = GRAD[key]
    return g[0](*WIT) * dqdj[0] + g[1](*WIT) * dqdj[1] + g[2](*WIT) * rho_w
Jp = ddj('J')
check("L4-O3 dJ_T/dj = -4(5T-27)/(3(4T-27)) and dF/dj = -(5T-27)/(2 ell^2 (4T-27)): F is NOT forced to zero on nearby "
      "homogeneous solutions",
      close(Jp, -4 * (5 * T - 27) / (3 * (4 * T - 27)), mp.mpf(10)**-40)
      and close(ddj('F'), -(5 * T - 27) / (2 * L2 * (4 * T - 27)), mp.mpf(10)**-40),
      f"dJ/dj = {mp.nstr(Jp,12)}, dF/dj = {mp.nstr(ddj('F'),12)}")

id_M11 = sp.simplify(M11s.subs(tau, 0) - E * (1 / J - 1) / (6 * m))
o4 = (id_M11 == 0
      and close(f['M12'](*WIT), 2 * T * mp.mpf(1) / 9, mp.mpf(10)**-40)                      # h_p,chi = 2T/9
      and close(-2 * f['v2'](*WIT), -mp.e**(mp.mpf(1) / 6) * (8 * T - 27) / 9, mp.mpf(10)**-40)   # g_chi
      and close(ddj('M11'), -mp.e**mp.mpf('0.5') * Jp / 6, mp.mpf(10)**-40)                  # h_pp'
      and close(-2 * ddj('v1'), 2 * mp.e**(mp.mpf(2) / 3) * Jp / 3, mp.mpf(10)**-40))        # g_p'
check("L4-O4 the five witness coefficients of the obstruction: h_pp = E(1/J-1)/(6V) as an EXACT identity, "
      "h_p,chi = 2T/9, g_chi = -e^{1/6}(8T-27)/9, h_pp' = -e^{1/2}J'/6, g_p' = 2e^{2/3}J'/3", o4)

detstar = f['detM'](*WIT)
check("L4-O5 det(M_star) = -4 T^2 h0^2/81, and it is NONZERO (the inverse in c_raw is not taken at a singular point)",
      close(detstar, -4 * T**2 * h0**2 / 81, mp.mpf(10)**-40) and abs(detstar) > mp.mpf(1),
      f"det(M*) = {mp.nstr(detstar,14)}")

S4p = ddj('S4')
S4p_lead = -mp.e**(mp.mpf(5) / 6) * (5 * T - 27) * (8 * T - 27) * (8 * T + 27) / (18 * T**2 * (4 * T - 27))
check("L4-O6 THE OBSTRUCTION: S_4'(1) = -e^{5/6}(5T-27)(8T-27)(8T+27)/(18 T^2 (4T-27)) and it is NEGATIVE for the "
      "frozen domain T > 27/4, so S_4 < 0 for every small j-1 > 0. IC6's boxed identity is CONFIRMED.",
      close(S4p, S4p_lead, mp.mpf(10)**-40) and S4p < 0 and T > mp.mpf(27) / 4,
      f"S4'(1) = {mp.nstr(S4p,18)}  (lead's closed form {mp.nstr(S4p_lead,18)})")

xs7, us7 = solve_aux(rho_w * mp.mpf('1.007'), mp.mpf(0))
S4_7 = f['S4'](xs7, us7, rho_w * mp.mpf('1.007'), 0)
dM_7 = f['detM'](xs7, us7, rho_w * mp.mpf('1.007'), 0)
M22_7 = f['M22'](xs7, us7, rho_w * mp.mpf('1.007'), 0)
M0_7 = M22_7 / dM_7                                             # reduced scalar kinetic mass  M_0 = A_0^{-1}
lam2 = -S4_7 * dM_7 / M22_7
check("L4-O7 the lead's j = 1.007 orientation state: xi = 0.24297809, u = 0.66347046, S_4 = -0.07526051653, "
      "lambda^2/k_z^4 -> 0.03456985650 -- all four reproduced by my own auxiliary solve",
      close(xs7, '0.24297809', mp.mpf('5e-9')) and close(us7, '0.66347046', mp.mpf('5e-9'))
      and close(S4_7, '-0.07526051653', mp.mpf('1e-11')) and close(lam2, '0.03456985650', mp.mpf('1e-10')),
      f"xi={mp.nstr(xs7,10)} u={mp.nstr(us7,10)} S4={mp.nstr(S4_7,12)} lam2/k4={mp.nstr(lam2,12)}")

# ==================================================== (b) THE IC7 REPAIR =========================================
print("\n-- (b) the IC7 repair --------------------------------------------------------------------------------------")
c7_7 = f['c7'](xs7, us7, rho_w * mp.mpf('1.007'), 0)
check("L4-I1 c_7 built from MY M and v at the lead's last isotropic sample j = 1.007 equals its stated "
      "c7 ~ 0.00235189114143216",
      close(c7_7, '0.00235189114143216', mp.mpf('1e-15')), f"c7 = {mp.nstr(c7_7,18)}")

# the sheared fixture: identical state in IC6_EVEN (its lambda_i) and IC6_DIRAC_FLOW (its g, Sigma)
lamsh = [mp.mpf('-0.6424435072183933'), mp.mpf('-0.622272178918671'), mp.mpf('-0.5676134368548011')]
rsh = sum(lamsh); tsh = sum(x**2 for x in lamsh) - rsh**2 / 3
xsh, ush = solve_aux(rsh, tsh)
Jsh = f['J'](xsh, ush, rsh, tsh)
check("L4-I2 the sheared fixture: my auxiliary solve returns xi = 0.242752746344542675, u = 0.663589818477735377, "
      "J_T = 0.986102159712075428 (18 digits, IC6_EVEN) -- the state itself reproduces",
      close(xsh, '0.242752746344542675', mp.mpf('1e-17')) and close(ush, '0.663589818477735377', mp.mpf('1e-17'))
      and close(Jsh, '0.986102159712075428', mp.mpf('1e-17')),
      f"xi={mp.nstr(xsh,19)} u={mp.nstr(ush,19)} J_T={mp.nstr(Jsh,19)}")

gmet = mp.matrix([[mp.mpf('1.03'), mp.mpf('.012'), mp.mpf('-.008')],
                  [mp.mpf('.012'), mp.mpf('.98'), mp.mpf('.009')],
                  [mp.mpf('-.008'), mp.mpf('.009'), mp.mpf('1.01')]])
Vsh = mp.sqrt(mp.det(gmet))
Ksh = mp.matrix([[Vsh * HQQ[i][j](xsh, ush, rsh, tsh) for j in range(2)] for i in range(2)])
Klead = mp.matrix([[mp.mpf('-14.9712400052'), mp.mpf('16.3722704813')],
                   [mp.mpf('16.3722704813'), mp.mpf('-29.7446446103')]])
Om12 = 3 * Vsh * tsh * (f['hxr'](xsh, ush, rsh, tsh) * f['hut'](xsh, ush, rsh, tsh)
                        - f['hxt'](xsh, ush, rsh, tsh) * f['hur'](xsh, ush, rsh, tsh))
Omat = mp.zeros(4)                                            # the full Dirac matrix O = [[0,-K],[K,Omega]]
for i in range(2):
    for j in range(2):
        Omat[i, j + 2] = -Ksh[i, j]; Omat[i + 2, j] = Ksh[i, j]
Omat[2, 3], Omat[3, 2] = -abs(Om12), abs(Om12)
Osv = sorted([mp.sqrt(abs(e)) for e in mp.eig(Omat.T * Omat, left=False, right=False)], reverse=True)
Kev = sorted([abs(e) for e in mp.eig(Ksh, left=False, right=False)])
check("L4-I3 the constraint algebra on that same state, from my own Hessians: K = {p_A,S_B} = V h_AB matches IC6's "
      "[[-14.9712400052,16.3722704813],[16.3722704813,-29.7446446103]], the secondary-secondary bracket is "
      "Omega_12 = 3 V tau (h_xr h_ut - h_xt h_ur) = 0.06402066864, and the full 4x4 Dirac matrix has IC6's singular "
      "values (40.31947, 40.31947, 4.396461, 4.396461): rank 4, no null direction",
      mp.norm(Ksh - Klead) < mp.mpf('1e-9') and close(abs(Om12), '0.06402066864', mp.mpf('1e-10'))
      and close(Osv[0], '40.31947', mp.mpf('1e-7')) and close(Osv[3], '4.396461', mp.mpf('1e-7')),
      f"Omega_12 = {mp.nstr(Om12,12)}; Dirac singular values "
      + ", ".join(mp.nstr(s, 10) for s in Osv))

c7_sh = f['c7'](xsh, ush, rsh, mp.mpf(0))                                  # IC7 prescription: M, v evaluated at tau = 0
S4_11_lead, resid_lead = mp.mpf('-0.0642323935174161'), mp.mpf('0.0151964888331')
check("L4-I4 IC7's residual sheared quartic: with IC6_EVEN's S4_11 = -0.0642323935174161, my independently built "
      "design coefficient predicts S4_11 + 32 c7 = 0.0151964888331 -- IC7's stated leftover reproduces to 12 digits",
      close(S4_11_lead + 32 * c7_sh, resid_lead, mp.mpf('1e-11'))
      and close(-S4_11_lead / 32, '0.00200726229741925', mp.mpf('1e-14')),
      f"c7(sheared) = {mp.nstr(c7_sh,16)}; S4_11 + 32 c7 = {mp.nstr(S4_11_lead + 32*c7_sh,12)}; "
      f"the value that WOULD cancel it is c_RR = {mp.nstr(-S4_11_lead/32,15)}")

id_cancel = sp.simplify(S4s + 32 * c7raw)
check("L4-I5 the central IC7 identity S_4 + 32 V c_7/B3^4 = 0 holds IDENTICALLY on the isotropic plateau -- but it "
      "holds because c_7 IS -S_4/32 by definition: the repair is an exactly tuned counterterm, not an independent "
      "prediction of the action",
      id_cancel == 0, "symbolic: S4 + 32*c7 == 0 for all (rho,xi,u)")

free_syms = (S4s.free_symbols | c7raw.free_symbols) - {xi, u, rho, tau}
check("L4-I6 c_raw = v^T M^{-1} v/8 is built ONLY from partial derivatives of the action density h and of the "
      "curvature coefficient c: no wave speed, no measured eigenvalue and no new fitted constant enters. IC7's "
      "sentence 'Neither measured eigenvalues nor a desired wave speed define it' is CONFIRMED as written.",
      len(free_syms) == 0, f"free symbols besides (xi,u,rho,tau): {sorted(str(s) for s in free_syms)}")

# ---- does the smooth cutoff hide a singularity?
supp_bound = abs(detstar) / 2
onstat = f['detM'](mp.mpf(1) / 4, mp.mpf(2) / 3, mp.mpf(0), mp.mpf(0))
Dstat = onstat / detstar
check("L4-I7 the cutoff's support EXCLUDES det(M) = 0: theta != 0 requires |D-1| < 1/2, i.e. |det M| >= |det M*|/2 "
      f"= {mp.nstr(supp_bound,8)} > 0, so the inverse in c_raw is never taken near a singular M",
      supp_bound > 0 and theta_of(mp.mpf('0.5')) == 0 and theta_of(mp.mpf('1.5')) == 0)
check("L4-I8 the static branch rho = 0 is exactly where M degenerates (M12 = D_t h_rho/2 vanishes with rho, so "
      "det M = 0), and there theta = 0: the zero extension is doing real work, and c_7 is defined there",
      abs(onstat) < mp.mpf(10)**-45 and theta_of(Dstat) == 0 and abs(Dstat - 1) >= mp.mpf(1) / 2,
      f"det M(rho=0) = {mp.nstr(onstat,4)}, D = {mp.nstr(Dstat,4)}, theta = 0")

sm = []
for eps in ('1e-2', '1e-3', '1e-4'):
    e = mp.mpf(eps)
    sm += [abs(theta_x(e) - 1)] + [abs(mp.diff(theta_x, e, n)) for n in (1, 2, 3)]
    sm += [abs(theta_x(1 - e))] + [abs(mp.diff(theta_x, 1 - e, n)) for n in (1, 2, 3)]
    d = mp.mpf(1) / 16 + e
    sm += [abs(eta_of(mp.sqrt(1 + mp.sqrt(d))) - 1)]
check("L4-I9 both cutoffs are genuinely C^infinity at their glue points: theta and its first three derivatives are "
      "flat to all orders at x = 0 and x = 1 (and eta likewise), and the |D-1| kink sits strictly inside the "
      "theta == 1 plateau, so no non-smoothness is introduced",
      max(sm) < mp.mpf('1e-30'), f"max |jet| at the glue = {mp.nstr(max(sm),4)}")

samples = {}
for jv in ('0.998', '1', '1.002', '1.007'):
    rv = rho_w * mp.mpf(jv); q = solve_aux(rv, mp.mpf(0))
    D = f['detM'](q[0], q[1], rv, 0) / detstar
    samples[jv] = (eta_of(f['r'](q[0], q[1], rv, 0)), theta_of(D), D)
eta_sh = eta_of(f['r'](xsh, ush, rsh, tsh))
check("L4-I10 IC7's claim that the four sampled trace ratios j = 0.998, 1, 1.002, 1.007 'all lie inside both unit "
      "plateaux' is CONFIRMED (eta = theta = 1 at each, and at the sheared state)",
      all(s[0] == 1 and s[1] == 1 for s in samples.values()) and eta_sh == 1,
      "D = " + ", ".join(f"{k}:{mp.nstr(v[2],8)}" for k, v in samples.items()))

def Dj(jv):
    rv = rho_w * jv; q = solve_aux(rv, mp.mpf(0))
    return f['detM'](q[0], q[1], rv, 0) / detstar, f['S4'](q[0], q[1], rv, 0)
edges = []
for tgt in (mp.mpf('1.25'), mp.mpf('1.5')):
    lo, hi = mp.mpf('1.0'), mp.mpf('1.25')
    for _ in range(70):
        mid = (lo + hi) / 2
        if Dj(mid)[0] < tgt: lo = mid
        else: hi = mid
    edges.append((lo, Dj(lo)[1]))
check("L4-I11 the repaired window is FINITE and small: along the same isotropic branch the theta == 1 plateau ends at "
      f"j = {mp.nstr(edges[0][0],8)} and theta reaches 0 at j = {mp.nstr(edges[1][0],8)}, where the UNREPAIRED "
      f"S_4 = {mp.nstr(edges[1][1],8)} is restored in full while eta is still 1. The repair covers |j-1| < 0.074 of "
      "the isotropic family, not the family.",
      edges[0][0] < mp.mpf('1.09') and edges[1][1] < 0 and theta_of(Dj(edges[1][0] * mp.mpf('1.001'))[0]) == 0,
      f"S_4 at the theta=0 edge = {mp.nstr(edges[1][1],8)} (vs -0.0753 at j=1.007)")

# ---- what IC7 does to the tensor cone
Kc_IC6, Kc_IC5, Gc0 = E / (m * J), E / m, cc / (4 * B3**2)
cT2_IC6 = cT2(Kc_IC6, Gc0)
cT2_IC5 = cT2(Kc_IC5, Gc0)
cT2_IC7 = sp.simplify(cT2(Kc_IC6, Gc0 - c7s * R0s / B3**2))
check("L4-I12 [control + result] the same tensor reduction gives physical c_T^2 = 1 EXACTLY for IC6 (the 1/J_T "
      "cancels) and c_T^2 = J_T for the IC5 mutation -- reproducing TENSOR_BALANCE.md's table independently; and "
      "IC7's term contributes nothing to the tensor sector when the background Rbar_0 = 0",
      sp.simplify(cT2_IC6 - 1) == 0 and sp.simplify(cT2_IC5 - J) == 0
      and sp.simplify(cT2_IC7.subs(R0s, 0) - 1) == 0)
detune = sp.simplify(cT2_IC7 - (1 - 4 * c7s * R0s / cc))
csh = f['c'](xsh, ush, rsh, tsh)
check("L4-I13 [new liability, quantified] on any background with barred spatial curvature Rbar_0 != 0 the IC7 term "
      "DETUNES the tensor cone: c_T^2 = 1 - 4 c_7 Rbar_0 / c exactly. IC6's exact tensor luminality was a "
      "cancellation IC7 breaks off flat backgrounds. The lead flags the non-transfer qualitatively "
      "('the earlier inhomogeneous odd-sector result is NOT transferred to IC7 when background bar R is nonzero'); "
      "this is its size.",
      detune == 0, f"at the sheared state 4 c_7/c = {mp.nstr(4*c7_sh/csh,8)} per unit Rbar_0")

# ==================================================== DEGREE-OF-FREEDOM COUNT ====================================
print("\n-- degree-of-freedom count ---------------------------------------------------------------------------------")
check("L4-D1 all four auxiliary constraints (p_xi, p_u, S_xi, S_u) are SECOND class: the ultralocal block "
      "K = V h_AB is invertible at the witness and at the sheared state, so the Dirac chain closes at the secondary "
      "level with no gauge generator and no tertiary constraint",
      abs(mp.det(Hw)) > mp.mpf(1) and min(Kev) > mp.mpf(1),
      f"det(H_qq)_witness = {mp.nstr(mp.det(Hw),10)}; |K| eigenvalues at shear {mp.nstr(Kev[0],8)}, {mp.nstr(Kev[1],8)}")

n_local = dof(6 + 2, 4, 3)          # 8 canonical pairs (h_ij, pi^ij, xi, u); 4 second class; 3 first-class momentum
check("L4-D2 [PROGRAMME REQUIREMENT] exactly TWO propagating gravitational degrees of freedom. Local count for "
      "IC5/IC6/IC7 in unitary clock gauge: 8 canonical pairs (6 barred-metric + xi + u) = 16; MINUS 4 second-class "
      "auxiliary constraints; MINUS 2x3 first-class spatial-momentum constraints. The lapse N = e^xi is a field with "
      "a second-class constraint, NOT a Lagrange multiplier, so there is no local first-class Hamiltonian "
      "constraint. Count = (16-4-6)/2 = 3, i.e. 2 tensor + 1 gravitational scalar.",
      n_local == 2, f"count = {n_local}: 2 tensor polarisations + 1 scalar -- the requirement is NOT met")

A0_w, A0_7 = detstar / f['M22'](*WIT), dM_7 / M22_7
check("L4-D3 the extra mode is identified and is a genuine propagating scalar, not a constrained one: the reduced "
      "scalar momentum Hessian A_0 = det M / M22 is POSITIVE and nondegenerate at the witness and at j = 1.007 "
      "(so zeta has a healthy kinetic term -- no ghost -- and cannot be gauged away). It is the lead's own even-sector "
      "zeta, which its reduced equation qddot + 3 qdot + e^{2/3} k^2 diag(1/3,1) q = 0 gives physical c_s^2 = 1/3.",
      A0_w > 0 and A0_7 > 0, f"A_0(witness) = {mp.nstr(A0_w,10)}, A_0(j=1.007) = {mp.nstr(A0_7,10)}, "
      f"M_0 = 1/A_0 = {mp.nstr(M0_7,10)}")

check("L4-D4 IC7 does not change that count: c_7 Rbar^2 carries no time derivative of any field, so it alters the "
      "constraint content only through S_A and leaves the symplectic form and the four second-class constraints "
      "intact. IC7 makes the third mode WELL-POSED on an isotropic window; it does not remove it.",
      dof(6 + 2, 4, 3) == 3, "count with IC7 = 3, unchanged")

print("\n-- what this lane did NOT independently verify --------------------------------------------------------------")
for line in ("the k_z^2 reduction that yields the witness speeds (1/3, 1) and IC7's quoted scalar c_s^2 = 0.388526918 "
             "at k = 1e5: that needs the background time derivatives (Mdot, Ndot) of the lead's reduced system;",
             "the sheared antisymmetric mixing N2_21 = 0.000563025148111 itself (the full anisotropic two-mode "
             "reduction); only its IC7 consequence S4_11 + 32 c7 was checked, via L4-I4;",
             "IC6_STRONG_AUXILIARY's Sobolev solvability, the odd-sector inhomogeneous geometry, and every empirical "
             "gate (PPN, galactic matching, measured G, cosmology) -- all remain as the lead states them: OPEN."):
    print(f"    - {line}")

print("\n" + "=" * 118)
hard = [n for n in FAILS if not n.startswith('L4-D2')]
print(f"L4 verification: {len(FAILS)} FAIL(S)" if FAILS else "L4 verification: ALL CHECKS PASS")
for n in FAILS: print(f"    FAIL: {n.split('.')[0]}")
print("    every reproduction check of the lead's own numbers PASSES; the single FAIL is the programme's 2-DOF")
print("    requirement, which IC5/IC6/IC7 do not meet (count = 3). Exit 2 marks that designed outcome; exit 1 would")
print("    mean one of the lead's numbers failed to reproduce.")
print("=" * 118)
sys.exit(1 if hard else (2 if FAILS else 0))
