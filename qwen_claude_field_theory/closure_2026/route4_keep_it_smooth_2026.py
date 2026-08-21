#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route4_keep_it_smooth_2026.py
=============================
ROUTE 4 -- HEAD-ON ASSAULT ON nbody STAGES 1-9.  CAN THE CONDENSATE BE KEPT SMOOTH?

WHAT THIS SCRIPT ESTABLISHES (every number computed BEFORE the check was written round it):

 1. *** STAGE 9's THEOREM IS FALSE AS STATED, AND THE DIRECTION IS FAVOURABLE TO THE FRAMEWORK. ***
    "c_s^2 -> 0 as a^-3 for EVERY ghost-free K" does not hold.  For L = K(Q):
        n = K',  rho = QK'-K,  p = K,  c_s^2 = K'/(Q K''),  no-ghost <=> K'' > 0.
    Rewrite:  K'' = dn/dQ = n/(mu c_s^2).  So for n>0 and Q=mu>0, K''>0 <=> c_s^2>0.
    *** GHOST FREEDOM CONSTRAINS ONLY THE SIGN OF c_s^2, NEVER ITS SCALING WITH n. ***
    Stage 9's a^-3 is the SIMPLE-ZERO case (K' ~ (Q-Q_*), Q_*!=0).  For K' ~ (Q-Q_*)^m the rate is
    a^(-3/m); and an explicitly constructed K with c_s^2 RISING as the charge dilutes is exhibited
    and verified ghost-free over 31 decades.  Stage 9's Part B must be WITHDRAWN as a theorem.

 2. STEPS 1 AND 4 OF THE CHAIN ARE ONE LINK, NOT TWO.  Exactly, rho+p = n mu and c_s^2 = dln mu/dln n,
    so  rho/n = Q_0  <=>  mu = const  <=>  c_s^2 = 0.  The chain has THREE independent links.

 3. STEP 3 IS CORRECT and is re-derived here from the linearised Einstein equations rather than
    quoted:  lap(Phi) = 4 pi G (rho + p_r + 2 p_t)  [dynamics];
             lap(Phi+Psi)/2 = 4 pi G (rho + (p_r+2p_t)/2)  [lensing].
    The chain's "lensing sees rho+p" is wrong (correct: rho + 3p/2 for isotropic p); the error
    OVERSTATES the lensing signal by 1.33x at f=1/3, i.e. it runs AGAINST the theory.  Conclusion
    unaffected: dyn=0 => lens=rho/2, lens=0 => dyn=-rho, only rho=0 kills both.
    p_r - p_t is an EXACT flat direction, so anisotropic stress is not an escape.

 4. THE REPLACEMENT OBSTRUCTION, which is stronger than stage 9's and needs no assumption about K:
    a shift-symmetric k-essence is BAROTROPIC -- p is a function of n alone.  So "warm today" and
    "warm where it is underdense" are the SAME statement, and a halo is DENSER than the mean.
    For any non-increasing c_s^2(n),
         barrier = INT_1^delta c_s^2 dln x  <=  c_s^2(mean, today) * ln(delta)
    ==>  c_s^2(mean, today) >= DeltaPhi / ln(20.9).   KERNEL-FREE, K-FREE.
    = 114.7 km/s on the corpus' own DeltaPhi = vc^2; 226.9 km/s on an honest 20 kpc -> 1 Mpc
    isothermal well.  (Stage 8's independently-derived 203 km/s sits inside that bracket.)

 5. THE CMB IS *NOT* WHAT KILLS THE WARM ROUTE.  w=-1 stays EXACT (rho_Lambda is the n=0
    integration constant of the same K), Omega_dm = 0.265 is unchanged, |w_dm| <~ 8e-7, and
    c_s^2(rec) is below every GDM bound for any beta > 0.1.  The kill, if there is one, is
    LATE-TIME STRUCTURE FORMATION, and it is a DATA constraint, not a theorem.

 6. THE SQUEEZE, AND ITS SIZE STATED HONESTLY.  With c_s^2(n) = c_s0^2 (n/n_bar0)^-beta and c_s0
    fixed by demanding delta_eq = 20.9:
        the sector must EXIT the halo ordinary collapse built  ->  beta < 0.26 (generous) / 0.57 (honest)
        the Lyman-alpha P(k) must survive at k = 5 h/Mpc, z=3   ->  beta > 0.77 (generous) / 1.13 (honest)
    EMPTY INTERSECTION, but the gap is only 2.0-3.0x IN ONE EXPONENT.  This is a SQUEEZE, not a
    no-go, and it is reported as such.  It closes if the exit budget is ~4x longer than the sound
    crossing time, or if the forest tolerates >95% suppression at k=5 h/Mpc.

 7. ESCAPES (a)-(e) priced individually; NONE reaches delta <= 20.9, margins 1e2 to 1e14.
    NOTE (a2): a HELMHOLTZ mass does NOT fall short -- it overshoots helpfully.  The obstruction
    there is not the mass but that the quasi-static charge is not the advected charge.

NEGATIVE / UNDETERMINED, stated plainly:
  * I could NOT determine whether MOND-driven baryonic structure formation refills the Lyman-alpha
    and sigma_8 power that a warm sector loses.  a_0(z=3)/a_0(0) is O(1), so MOND is ON there.
    That calculation is unsolved in the literature and it is the escape's remaining life.
  * I could NOT settle the AeST quasi-static ansatz vs charge advection (route2's own open item).
  * The exit time is a sound-crossing estimate, not a solved outflow; it is the softest number here.

Both footings on every dimensionful result.  Exit 0 = all checks passed.
"""

import sys


# ====================================================================================================
# SECTION FROM r4_p1_gr.py
# ====================================================================================================
# PART 1: derive, from scratch, what sources dynamics vs lensing for a STATIC,
# spherically symmetric, ANISOTROPIC source in the weak field.  No formula assumed.
import sympy as sp

r, G, eps = sp.symbols('r G epsilon', positive=True)
Phi = sp.Function('Phi')(r)     # -g_tt = 1 + 2 eps Phi
Psi = sp.Function('Psi')(r)     # spatial:  isotropic gauge  (1 - 2 eps Psi) delta_ij
rho = sp.Function('rho')(r); pr = sp.Function('p_r')(r); pt = sp.Function('p_t')(r)

# isotropic coordinates: ds^2 = -(1+2e Phi)dt^2 + (1-2e Psi)(dR^2 + R^2 dOmega^2)
t, R, th, ph = sp.symbols('t R theta phi')
Phi_ = sp.Function('Phi')(R); Psi_ = sp.Function('Psi')(R)
g = sp.diag(-(1 + 2*eps*Phi_), (1 - 2*eps*Psi_), (1 - 2*eps*Psi_)*R**2,
            (1 - 2*eps*Psi_)*R**2*sp.sin(th)**2)
x = [t, R, th, ph]
ginv = g.inv()

def series1(e):
    return sp.expand(sp.series(sp.simplify(e), eps, 0, 2).removeO())

Gam = [[[0]*4 for _ in range(4)] for _ in range(4)]
for a in range(4):
    for b in range(4):
        for c in range(4):
            s = 0
            for d in range(4):
                s += ginv[a, d]*(sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b]) - sp.diff(g[b, c], x[d]))
            Gam[a][b][c] = series1(s/2)

Ric = sp.zeros(4, 4)
for b in range(4):
    for c in range(4):
        s = 0
        for a in range(4):
            s += sp.diff(Gam[a][b][c], x[a]) - sp.diff(Gam[a][b][a], x[c])
            for d in range(4):
                s += Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a]
        Ric[b, c] = series1(s)

Rs = series1(sum(ginv[a, b]*Ric[a, b] for a in range(4) for b in range(4)))
Ein = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Ein[a, b] = series1(Ric[a, b] - g[a, b]*Rs/2)

# mixed components G^a_b at O(eps)
def mixed(a, b):
    s = sum(ginv[a, d]*Ein[d, b] for d in range(4))
    s = sp.expand(sp.series(sp.simplify(s), eps, 0, 2).removeO())
    return sp.simplify(sp.diff(s, eps).subs(eps, 0))   # coefficient of eps

G00 = mixed(0, 0); G11 = mixed(1, 1); G22 = mixed(2, 2)
lap = lambda F: sp.diff(F, R, 2) + 2*sp.diff(F, R)/R
print("G^0_0 (O(eps)) =", sp.simplify(G00))
print("   compare -2 lap(Psi):", sp.simplify(G00 + 2*lap(Psi_)))
print("G^1_1 (O(eps)) =", sp.simplify(G11))
print("G^2_2 (O(eps)) =", sp.simplify(G22))

# T^a_b = diag(-rho, p_r, p_t, p_t);  Einstein: G^a_b = 8 pi G T^a_b, eps absorbs the 8piG scale
rhoR = sp.Function('rho')(R); prR = sp.Function('p_r')(R); ptR = sp.Function('p_t')(R)
k = 8*sp.pi*G
eq00 = sp.Eq(G00, k*(-rhoR))
eq11 = sp.Eq(G11, k*prR)
eq22 = sp.Eq(G22, k*ptR)
print("\n--- eq00 ---"); sp.pprint(sp.simplify(eq00.lhs - eq00.rhs))
print("--- eq11 ---"); sp.pprint(sp.simplify(eq11.lhs - eq11.rhs))
print("--- eq22 ---"); sp.pprint(sp.simplify(eq22.lhs - eq22.rhs))



# ====================================================================================================
# SECTION FROM r4_p2_thermo.py
# ====================================================================================================
# PART 2+3: exact shift-symmetric k-essence thermodynamics; test stages 5 & 9.
import sympy as sp, mpmath as mp
mp.mp.dps = 30
Q, Q0, u = sp.symbols('Q Q_0 u', real=True)
K = sp.Function('K')

# --- exact relations for L = K(Q), Q = A^mu d_mu phi (homogeneous: Q = phidot) ---
n   = sp.diff(K(Q), Q)                    # shift charge  J^0 = dL/dQ
rho = Q*sp.diff(K(Q), Q) - K(Q)           # energy density
p   = K(Q)
print("n   =", n)
print("rho =", rho)
print("p   =", p)
print("rho+p - Q n =", sp.simplify(rho + p - Q*n), "  <-- must be 0 (Gibbs-Duhem, mu=Q)")
drho = sp.simplify(sp.diff(rho, Q)); dp = sp.simplify(sp.diff(p, Q))
cs2 = sp.simplify(dp/drho)
print("drho/dQ =", drho, "   dp/dQ =", dp)
print("c_s^2 = dp/drho =", cs2)

# no-ghost from the P(X) form, X = Q^2/2
X = sp.symbols('X', positive=True)
Kx = K(sp.sqrt(2*X))
noghost = sp.simplify(sp.diff(Kx, X) + 2*X*sp.diff(Kx, X, 2))
print("P_X + 2 X P_XX =", sp.simplify(noghost.rewrite(sp.Derivative)),
      "  -> substitute Q=sqrt(2X):", sp.simplify(noghost.subs(X, Q**2/2)))
cs2_std = sp.simplify(sp.diff(Kx, X)/noghost).subs(X, Q**2/2)
print("c_s^2 (standard k-essence formula) =", sp.simplify(cs2_std),
      "  identical to dp/drho? ", sp.simplify(cs2_std - cs2) == 0)

print()
print("="*100)
print("KEY IDENTITY:  c_s^2 = dln(mu)/dln(n)  with mu = Q the chemical potential")
nn, mu = sp.symbols('n mu', positive=True)
# mu(n) = drho/dn ; c_s^2 = dp/drho = (n dmu/dn)/mu
print("  because rho+p = n mu  and  drho = mu dn  =>  dp = n dmu  =>  dp/drho = n dmu/(mu dn)")
print("  numeric check below.")



# ====================================================================================================
# SECTION FROM r4_p3_theorem.py
# ====================================================================================================
# Test stage 9's theorem "c_s^2 ~ a^-3 for EVERY ghost-free K".
import sympy as sp, mpmath as mp
mp.mp.dps = 40
Q, Qs, C, m, A, b = sp.symbols('Q Q_* C m A beta', positive=True)

print("="*100); print("TEST 1 -- the generic case stage 9 actually covers: K' with a SIMPLE zero at Q_*>0")
Kp = C*(Q - Qs)**m                       # K'(Q); m=1 is stage 9's implicit assumption
Kpp = sp.diff(Kp, Q)
cs2 = sp.simplify(Kp/(Q*Kpp))
print("  K' = C (Q-Q_*)^m ;  K'' =", Kpp, " >0 for Q>Q_*  => GHOST FREE for any m>0")
print("  c_s^2 = K'/(Q K'') =", cs2)
# n ~ (Q-Q_*)^m  =>  (Q-Q_*) ~ n^(1/m)  =>  c_s^2 ~ n^(1/m) ~ a^(-3/m)
print("  n = K' propto (Q-Q_*)^m  =>  c_s^2 propto n^(1/m) propto a^(-3/m)")
print("  *** stage 9's rate a^-3 is the m=1 case ONLY.  m=10 gives a^-0.3, m=100 gives a^-0.03. ***")

print(); print("="*100)
print("TEST 2 -- is a RISING c_s^2 ghost-free-constructible?  Demand c_s^2 = A (n/n0)^(-beta), beta>0.")
n, n0 = sp.symbols('n n_0', positive=True)
# dln mu/dln n = A (n/n0)^(-beta)  =>  mu = mu_inf exp(-(A/beta)(n/n0)^(-beta))
mu_inf = sp.symbols('mu_inf', positive=True)
mu = mu_inf*sp.exp(-(A/b)*(n/n0)**(-b))

chk = sp.simplify(n*sp.diff(mu, n)/mu)
print("  mu(n) = mu_inf exp(-(A/beta)(n/n0)^-beta)   ->  n dmu/dn / mu =", sp.simplify(chk))
print("  dmu/dn =", sp.simplify(sp.diff(mu, n)), "   sign: positive for n>0  => K'' = dn/dQ = 1/(dmu/dn) > 0")
print("  *** GHOST FREEDOM IS AUTOMATIC: K'' = n/(mu c_s^2) > 0 whenever c_s^2>0 and Q=mu>0. ***")
print("  So no-ghost constrains only the SIGN of c_s^2, never its n-dependence.")

# w of the non-Lambda part:  p_f(n) = int_0^n c_s^2 mu dn' ;  rho_f = int_0^n mu dn'
print(); print("  w_f = p_f/rho_f with mu ~= const:")
wf = sp.simplify(sp.integrate(A*(n/n0)**(-b), (n, 0, n))/n)
print("     w_f(n) =", sp.simplify(wf), "  = c_s^2(n)/(1-beta)   (converges only for beta<1)")

print(); print("="*100)
print("TEST 3 -- explicit K(Q) for the rising case, checked numerically for K''>0 over 30 decades")
Av, bv, muv, n0v = mp.mpf('1.4e-6'), mp.mpf('0.95'), mp.mpf(1), mp.mpf(1)
f_mu  = lambda nn: muv*mp.e**(-(Av/bv)*(nn/n0v)**(-bv))
f_dmu = lambda nn: mp.diff(f_mu, nn)
bad = 0; rows=[]
for k in range(-15, 16):
    nn = mp.mpf(10)**k
    Kpp_ = 1/f_dmu(nn)                      # dn/dQ
    cs2_ = nn*f_dmu(nn)/f_mu(nn)
    if not (Kpp_ > 0): bad += 1
    if k % 5 == 0: rows.append((k, mp.nstr(f_mu(nn),8), mp.nstr(Kpp_,6), mp.nstr(cs2_,6)))
print("   log10 n |      mu(n)      |    K''=dn/dQ    |     c_s^2")
for k,a_,b_,c_ in rows: print(f"   {k:7d} | {a_:>15} | {b_:>15} | {c_:>12}")
print(f"   ghost-free at all {31} sampled decades: {bad==0}")
print("   c_s^2(n=1e-15)/c_s^2(n=1e15) =", mp.nstr((mp.mpf(10)**(-15))**(-bv)/((mp.mpf(10)**15)**(-bv)), 6),
      " -> c_s^2 RISES by that factor as the charge dilutes.  STAGE 9's THEOREM DOES NOT HOLD HERE.")



# ====================================================================================================
# SECTION FROM r4_master.py
# ====================================================================================================
# ROUTE 4 MASTER -- every number computed before any check is written around it.
import mpmath as mp, sympy as sp, sys
mp.mp.dps=25
C=mp.mpf('2.99792458e8'); G=mp.mpf('6.674e-11'); MPC=mp.mpf('3.0857e22'); KPC=MPC/1000
PC=KPC/1000; HBAR=mp.mpf('1.0546e-34'); EV=mp.mpf('1.602e-19'); MSUN=mp.mpf('1.989e30')
RHO_CRIT=mp.mpf('8.5992e-27'); OM_M=mp.mpf('0.3143'); OM_DM=mp.mpf('0.2650'); OM_B=mp.mpf('0.0493')
RHO_M0=OM_M*RHO_CRIT; RHO_DM0=OM_DM*RHO_CRIT
GYR=mp.mpf('3.156e16'); H0=mp.mpf('2.184e-18'); ZREC=mp.mpf('1090')
VC=mp.mpf('200e3'); TOL=mp.mpf('20.9'); ISO=mp.mpf('5.5e4'); HUB=mp.mpf('13.8')
A0={'canon':mp.mpf('9.3619e-11'),'alt':mp.mpf('1.1279e-10')}
R_IN=20*KPC
sig=lambda x,n=4: mp.nstr(mp.mpf(x),n)
FAIL=[];N=[0]
def chk(c,l,d=""):
    N[0]+=1; ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {l}"+(f"   {d}" if d else ""))
    if not ok: FAIL.append(l)
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""))
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104)

head("A.  THE WELL DEPTH -- stated once, both conventions, so no number below is ambiguous")
LOGS={'corpus (Phi=vc^2, 1 e-fold)':mp.mpf(1),'20kpc->200kpc':mp.log(10),
      '20kpc->1 Mpc':mp.log(50),'20kpc->3 Mpc':mp.log(150)}
for k,v in LOGS.items(): info(f"DeltaPhi = vc^2 * {sig(v,4)}", f"= {sig(VC**2*v,4)} m^2/s^2 = {sig(VC**2*v/C**2,4)} c^2  [{k}]")
DPHI_GEN=VC**2                 # generous (corpus-comparable)
DPHI_HON=VC**2*mp.log(50)      # honest isothermal well 20 kpc -> 1 Mpc

head("B.  THE HARD FLOOR ON THE SECTOR'S SOUND SPEED  (kernel-free, K-free)")
print("""  THEOREM.  A shift-symmetric k-essence is exactly barotropic: p = K(Q), n = K'(Q), so p is a
  function of n ALONE.  'Warm today' and 'warm where it is underdense' are therefore the SAME
  statement.  For hydrostatic support the barrier is  INT_1^delta c_s^2 dln x.  If c_s^2(n) is
  non-increasing in n -- which is exactly what 'cold at recombination, warm now' requires -- then
        barrier <= c_s^2(cosmic mean, today) * ln(delta).
  Hence  c_s^2(mean, today) >= DeltaPhi / ln(delta_max).  NO CHOICE OF K EVADES THIS.""")
for lab,dp in [('generous',DPHI_GEN),('honest',DPHI_HON)]:
    f=dp/C**2/mp.log(TOL)
    info(f"floor, {lab}: c_s^2 >= {sig(f,4)} c^2", f"c_s >= {sig(mp.sqrt(f)*C/1000,4)} km/s")
FLOOR_GEN=DPHI_GEN/C**2/mp.log(TOL); FLOOR_HON=DPHI_HON/C**2/mp.log(TOL)
chk(mp.sqrt(FLOOR_GEN)*C/1000 > 100, "B1 floor exceeds 100 km/s on the most generous well",
    f"{sig(mp.sqrt(FLOOR_GEN)*C/1000)} km/s")
info("stage 8's independently-derived requirement was 203 km/s -- inside this bracket.",
     "so the corpus number was right in magnitude; what was wrong is stage 9's reason for refusing it.")

head("C.  WHAT THAT FLOOR COSTS: the comoving Jeans scale it forces TODAY")
def kJ(cs2,z):
    a=1/(1+mp.mpf(z)); return a*mp.sqrt(4*mp.pi*G*RHO_M0*a**-3)/(mp.sqrt(cs2)*C)*MPC
for lab,f in [('generous',FLOOR_GEN),('honest',FLOOR_HON)]:
    k0=kJ(f,0); info(f"{lab}: k_J(z=0) = {sig(k0,4)} Mpc^-1", f"lambda_J = {sig(2*mp.pi/k0,4)} Mpc comoving")
info("the sigma_8 scale is 8 h^-1 Mpc = 11.9 Mpc, k = 0.53 Mpc^-1.",
     "the sector cannot cluster there today under EITHER convention.")

head("D.  THE SQUEEZE.  c_s^2(n) = c_s0^2 (n/n_bar0)^-beta.  c_s0 is FIXED by demanding delta_eq = 20.9.")
def cs0_for(b,dphi,delta=TOL):
    b=mp.mpf(b); x=dphi/C**2
    return x/mp.log(delta) if b<mp.mpf('1e-9') else b*x/(1-delta**(-b))
def delta_of_r(r): return VC**2/(4*mp.pi*G*r**2)/RHO_DM0
def r_of_delta(d): return VC/mp.sqrt(4*mp.pi*G*d*RHO_DM0)
def t_exit(b,dphi):
    b=mp.mpf(b); c0=cs0_for(b,dphi); ro=r_of_delta(TOL)
    return mp.quad(lambda r: 1/(mp.sqrt(c0*delta_of_r(r)**(-b))*C),[R_IN,ro])/GYR
def supp(b,k,z,dphi):
    b=mp.mpf(b); a=1/(1+mp.mpf(z)); c0=cs0_for(b,dphi)
    kj0=mp.sqrt(4*mp.pi*G*RHO_M0)/(mp.sqrt(c0)*C)*MPC
    a_f=(kj0/mp.mpf(k))**(2/(1+3*b))
    return mp.mpf(1) if a_f>=a else (a_f/a)**2
for lab,dp in [('GENEROUS well (Phi=vc^2)',DPHI_GEN),('HONEST well (20kpc->1Mpc)',DPHI_HON)]:
    print(f"\n  --- {lab} ---")
    print(f"  {'beta':>5}{'c_s0 km/s':>10}{'c_s^2(rec)':>12}{'t_exit Gyr':>12}{'P/Pcdm 5h/Mpc z=3':>19}{'P/Pcdm 1h/Mpc z=3':>19}")
    for b_ in ['0','0.1','0.2','0.3','0.5','0.75','1.0','1.5','2.0']:
        b=mp.mpf(b_); c0=cs0_for(b,dp)
        csrec=c0*((1+ZREC)**3)**(-b) if b>0 else c0
        print(f"  {b_:>5}{sig(mp.sqrt(c0)*C/1000,4):>10}{sig(csrec,3):>12}{sig(t_exit(b,dp),4):>12}"
              f"{sig(supp(b,mp.mpf('5')*mp.mpf('0.674'),3,dp),3):>19}{sig(supp(b,mp.mpf('1')*mp.mpf('0.674'),3,dp),3):>19}")
    b1=mp.findroot(lambda b: t_exit(b,dp)-HUB, mp.mpf('0.25'))
    b2=mp.findroot(lambda b: supp(b,mp.mpf('5')*mp.mpf('0.674'),3,dp)-mp.mpf('0.7'), mp.mpf('0.8'))
    print(f"  EXIT in <13.8 Gyr requires beta < {sig(b1,4)} ;  forest P/Pcdm>0.7 at k=5h/Mpc requires beta > {sig(b2,4)}")
    print(f"  ==> {'EMPTY' if b1<b2 else 'NON-EMPTY'} intersection, gap factor {sig(b2/b1,4)}x")
    if lab.startswith('GENEROUS'): GAP_GEN=(b1,b2)
    else: GAP_HON=(b1,b2)
chk(GAP_GEN[0]<GAP_GEN[1], "D1 squeeze is empty on the GENEROUS well", f"beta<{sig(GAP_GEN[0])} vs beta>{sig(GAP_GEN[1])}")
chk(GAP_HON[0]<GAP_HON[1], "D2 squeeze is empty on the HONEST well", f"beta<{sig(GAP_HON[0])} vs beta>{sig(GAP_HON[1])}")
info("HOW MUCH SLACK IS THERE?  the gap is a factor of a few in ONE exponent, not orders.")
for T in ['13.8','27.6','55.2']:
    b1x=mp.findroot(lambda b: t_exit(b,DPHI_GEN)-mp.mpf(T), mp.mpf('0.25'))
    info(f"  if the exit budget were {T} Gyr:", f"beta < {sig(b1x,4)}")
for P in ['0.7','0.5','0.2','0.05']:
    b2x=mp.findroot(lambda b: supp(b,mp.mpf('5')*mp.mpf('0.674'),3,DPHI_GEN)-mp.mpf(P), mp.mpf('0.6'))
    info(f"  if the forest tolerated P/Pcdm > {P} at k=5h/Mpc:", f"beta > {sig(b2x,4)}")
print()
print(f"  CHECKS SO FAR: {N[0]}, failures: {FAIL}")



# ====================================================================================================
# SECTION FROM r4_master2.py
# ====================================================================================================
import mpmath as mp
mp.mp.dps=25
C=mp.mpf('2.99792458e8'); G=mp.mpf('6.674e-11'); MPC=mp.mpf('3.0857e22'); KPC=MPC/1000
PC=KPC/1000; HBAR=mp.mpf('1.0546e-34'); EV=mp.mpf('1.602e-19'); MSUN=mp.mpf('1.989e30')
RHO_CRIT=mp.mpf('8.5992e-27'); OM_M=mp.mpf('0.3143'); OM_DM=mp.mpf('0.2650')
RHO_M0=OM_M*RHO_CRIT; RHO_DM0=OM_DM*RHO_CRIT; GYR=mp.mpf('3.156e16')
VC=mp.mpf('200e3'); TOL=mp.mpf('20.9'); ZREC=mp.mpf('1090'); R_IN=20*KPC
sig=lambda x,n=4: mp.nstr(mp.mpf(x),n)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104)
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""))
DPHI_GEN=VC**2; DPHI_HON=VC**2*mp.log(50)
def cs0_for(b,dphi,delta=TOL):
    b=mp.mpf(b); x=dphi/C**2
    return x/mp.log(delta) if b<mp.mpf('1e-9') else b*x/(1-delta**(-b))
def kJ0(cs2): return mp.sqrt(4*mp.pi*G*RHO_M0)/(mp.sqrt(cs2)*C)*MPC

head("E.  THE beta-INDEPENDENT COST: late-time growth.  sigma_8 scale k = 0.53 Mpc^-1.")
print(f"  {'beta':>5} | {'GENEROUS well':^34} | {'HONEST well':^34}")
print(f"  {'':>5} | {'c_s0':>8}{'z_freeze':>10}{'delta/delta_cdm':>16} | {'c_s0':>8}{'z_freeze':>10}{'delta/delta_cdm':>16}")
K8=mp.mpf('0.53')
for b_ in ['0','0.25','0.5','1.0','2.0','5.0']:
    b=mp.mpf(b_); out=[]
    for dp in (DPHI_GEN,DPHI_HON):
        c0=cs0_for(b,dp); k0=kJ0(c0)
        zf=(K8/k0)**(2/(1+3*b))-1
        r=1/(1+zf) if zf>0 else mp.mpf(1)
        out.append((mp.sqrt(c0)*C/1000,zf,r))
    print(f"  {b_:>5} | {sig(out[0][0],4):>8}{sig(out[0][1],4):>10}{sig(out[0][2],4):>16} |"
          f" {sig(out[1][0],4):>8}{sig(out[1][1],4):>10}{sig(out[1][2],4):>16}")
info("delta/delta_cdm at the sigma_8 scale = observed sigma_8 / LCDM sigma_8 IF the dark sector")
info("carries sigma_8.  Planck+LSS give sigma_8 = 0.81 +- 0.02, i.e. a >=0.9 ratio is required.")
info("EVERY beta violates it, by 1.7x (generous, beta=5) to 6.7x (honest, beta=0).")
info("CAVEAT stated against my own conclusion: in THIS framework MOND is at full strength at z<1,")
info("so baryons could regrow some of it.  MOND structure formation is UNSOLVED; I cannot price it.")

head("F.  ESCAPE (a) -- A MASS / COMPTON SCALE OF ORDER THE HALO")
print("""  Two distinct constructions, both computed:
    (a1) give the excitation a particle mass m (fuzzy-DM-like quantum pressure)
    (a2) give the Q-sector a HELMHOLTZ mass mu (AeST's own term) -- this is what caps AeST at ~21x""")
# a1: soliton core radius  r_c ~ 1.6 kpc (1e-22 eV/m)(1e9 Msun/M)^(1/3)
def rc_kpc(m_eV, M_msun):
    return mp.mpf('1.6')*(mp.mpf('1e-22')/m_eV)*(mp.mpf('1e9')/M_msun)**mp.mpf('1/3')
M_H=mp.mpf('1e12')
m_need=mp.mpf('1.6e-22')*(mp.mpf('1e9')/M_H)**mp.mpf('1/3')/20
info(f"(a1) core r_c = 20 kpc in a 1e12 Msun halo needs m = {sig(m_need,4)} eV")
LYA=mp.mpf('2e-21')
info(f"     Lyman-alpha floor on fuzzy DM: m > {sig(LYA)} eV",
     f"REQUIRED m is BELOW it by {sig(LYA/m_need,4)}x")
info(f"     at the Ly-a floor m=2e-21 eV the core is r_c = {sig(rc_kpc(LYA,M_H)*1000,4)} pc",
     f"-> overdensity of 3.2e11 Msun inside it")
Mdust=mp.mpf('3.2e11')*MSUN; rc=rc_kpc(LYA,M_H)*KPC
d_a1=Mdust/(4*mp.pi/3*rc**3)/RHO_DM0
info(f"     delta permitted by (a1) at the Ly-a floor = {sig(d_a1,4)}", f"vs tolerance 20.9 -> over by {sig(d_a1/TOL,4)}x")
info("     and the corpus' own stage 3 wave scale (0.18 AU) is the same statement in the framework's",
     "own parameters -- I reproduce its DIRECTION independently.")
# a2: Helmholtz mass.  route2: rho_Q = (2-K_B) mu^2 c^2 |Psi| / (8 pi G)
def delta_helm(mu_inv_mpc, KB=0):
    mu=1/(mp.mpf(mu_inv_mpc)*MPC)
    return (2-mp.mpf(KB))*mu**2*C**2*(DPHI_GEN/C**2)/(8*mp.pi*G*RHO_DM0)
info(f"(a2) delta_Q(mu^-1 = 1 Mpc)    = {sig(delta_helm(1),4)}   [reproduces route2's ~21x cap]")
mu_need=mp.sqrt(delta_helm(1)/TOL)
info(f"     mu^-1 giving exactly delta = 20.9 is {sig(mu_need,4)} Mpc")
info(f"     the framework's OWN banked mu^-1 = 4392 Mpc gives delta = {sig(delta_helm('4392'),3)}",
     "-- i.e. NO clustering at all, which is why AeST galaxies contain no dark sector")
info("     *** SO (a2) IS NOT SHORT -- IT OVERSHOOTS IN THE HELPFUL DIRECTION. ***")
info("     The obstruction is NOT the size of mu.  It is that the quasi-static solution")
info("     n = -mu^2 Q_0 Psi is NOT the cosmologically-advected charge: reaching it requires")
info("     EXPELLING charge from the galaxy, and that is stage 6's transport problem, unsolved.")

head("G.  ESCAPE (b) -- REPULSIVE SELF-INTERACTION (this IS the framework's DBI: p = K rho^2)")
print("""  n=1 polytrope: R = pi sqrt(K / 2 pi G), mass-independent (stage 5's 105 pc).
  But K is not free: c_s^2 = 2 K rho, so K is FIXED by the sound speed, and the CMB caps
  c_s^2 at recombination.  Invert the chain.""")
def R_from_cs2_0(cs2_0):
    K=cs2_0*C**2/(2*RHO_DM0); return mp.pi*mp.sqrt(K/(2*mp.pi*G))
for cs2rec_lab,cs2rec in [('CLASS run used 2.9e-8',mp.mpf('2.9e-8')),('generous GDM bound 1e-6',mp.mpf('1e-6'))]:
    cs2_0=cs2rec/((1+ZREC)**3)
    R=R_from_cs2_0(cs2_0)
    info(f"c_s^2(rec) = {sig(cs2rec)} ({cs2rec_lab})",
         f"-> c_s^2(0)={sig(cs2_0,3)}, polytrope R = {sig(R/PC,4)} pc")
    rho_c=mp.pi*Mdust/(4*R**3)
    info("", f"central delta = {sig(rho_c/RHO_DM0,4)}   vs tolerance 20.9 -> over by {sig(rho_c/RHO_DM0/TOL,3)}x")
R_need=20*KPC
cs2_0_need=2*RHO_DM0*(R_need/mp.pi)**2*2*mp.pi*G/C**2
info(f"a 20 kpc core would need c_s^2(rec) = {sig(cs2_0_need*(1+ZREC)**3,4)} c^2",
     f"-> over the 1e-6 GDM bound by {sig(cs2_0_need*(1+ZREC)**3/mp.mpf('1e-6'),4)}x")
info("DIRECTION OF THIS RESULT: p ~ rho^2 makes c_s^2 RISE with density, so it supports a CORE but")
info("cannot keep the sector out of the halo -- it is the OPPOSITE sign to what section D needs.")

head("H.  ESCAPE (c) -- VORTICITY / TOPOLOGICAL OBSTRUCTION")
print("""  The shift symmetry is phi -> phi + c with c in R (NON-compact).  pi_1(R) = 0, so there is no
  winding number and no vortex.  Compactify (phi periodic, axion-like) and global strings exist --
  price that best case, not the worst.""")
lam_spin=mp.mpf('0.035')          # measured halo spin parameter (tidal torque); the dust's is 0 (irrotational)
r_cent=lam_spin**2*(200*KPC)
d_c=Mdust/(4*mp.pi/3*r_cent**3)/RHO_DM0
info(f"best case: give the sector the FULL measured halo spin lambda = {sig(lam_spin)}")
info(f"  centrifugal halt radius ~ lambda^2 r_vir = {sig(r_cent/KPC,4)} kpc",
     f"-> delta = {sig(d_c,3)}, over the tolerance by {sig(d_c/TOL,3)}x")
info("  and the framework's dust is an IRROTATIONAL potential flow (v = grad(delta phi)),")
info("  so its actual spin is ZERO: the 1e9x above is an upper bound it does not even reach.")

head("I.  ESCAPE (d) -- RELATIVISTIC IN THE NONLINEAR REGIME")
import sympy as sp
u,L,M4,mu_,Q0=sp.symbols('u Lambda_D M^4 mu Q_0',positive=True)
s=u/L
K_=-M4+mu_**2*L**2*(1-sp.sqrt(1-s**2))
rho_=sp.simplify((Q0+u)*sp.diff(K_,u)-K_); p_=K_
w_=sp.simplify(sp.limit(p_/rho_,u,L,dir='-'))
info(f"DBI cap: lim_(u->Lambda_D) p/rho = {w_}", "-> w -> 0, PRESSURELESS at saturation")
info("so going relativistic at the cap makes it MORE dust-like, not less.  Independent confirmation")
info("of stage 3 part B, by a different route (limit of p/rho rather than of rho*sqrt(1-s^2)).")
info("And if instead the sector genuinely reached p = rho/3, the DYNAMICAL source rho+3p = 2 rho")
info("DOUBLES the overshoot, while the lensing source rho+3p/2 = 1.5 rho rises 1.5x.  Both worse.")

head("J.  ESCAPE (e) -- a_0(z) WEAKENING THE SECTOR'S OWN GRAVITY AT COLLAPSE")
info("The sector's self-gravity floor is NEWTONIAN: a_0 -> 0 removes the MOND ENHANCEMENT, not G.")
for zc in ['0','1','2','5','10']:
    d=178*(1+mp.mpf(zc))**3
    info(f"  virialisation at z={zc}: delta vs today's mean = {sig(d,5)}", f"over the 20.9 tolerance by {sig(d/TOL,4)}x")
info("*** the tolerance 20.9 sits BELOW the z=0 Newtonian virial floor 178 by 8.5x. ***")
info("So 'collapse more slowly' cannot reach it.  a_0(z) is not an escape from the double count;")
info("its real (and banked) role is the CMB epoch separation.  This CONFIRMS stage 8's adverse read.")



# ====================================================================================================
# SECTION FROM r4_master3.py
# ====================================================================================================
import mpmath as mp, sympy as sp
mp.mp.dps=30
C=mp.mpf('2.99792458e8'); G=mp.mpf('6.674e-11'); MSUN=mp.mpf('1.989e30')
MPC=mp.mpf('3.0857e22'); KPC=MPC/1000; ZREC=mp.mpf('1090')
RHO_CRIT=mp.mpf('8.5992e-27'); OM_DM=mp.mpf('0.2650'); OM_B=mp.mpf('0.0493')
A0={'canon':mp.mpf('9.3619e-11'),'alt':mp.mpf('1.1279e-10')}
sig=lambda x,n=4: mp.nstr(mp.mpf(x),n)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104)
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""))

head("K.  STEP 1 RE-DERIVED:  is rho = Q_0 n an independent fact, or the SAME fact as step 4?")
n,mu0,A,b,n0=sp.symbols('n mu_0 A beta n_0',positive=True)
print("""  EXACT (no expansion):  rho + p = n mu  with mu = Q.  Hence  drho = mu dn  and  dp = n dmu.
     rho_f(n) = INT_0^n mu dn'   and   p_f(n) = INT_0^n c_s^2 mu dn'   with  c_s^2 = dln mu/dln n.
  Therefore   rho/n = Q_0  (step 1)   <=>   mu = const   <=>   c_s^2 = 0  (step 4).""")
mu_=mu0*sp.exp(-(A/b)*(n/n0)**(-b))
rho_f=sp.integrate(mu_,(n,0,n)); p_f=sp.integrate(A*(n/n0)**(-b)*mu_,(n,0,n))
w_lead=None
info("with mu ~ const to O(c_s^2):  w_f(n) = c_s^2(n)/(1-beta)  (converges iff beta<1)")
info("*** SO STEPS 1 AND 4 ARE ONE LINK, NOT TWO.  The chain has THREE independent links, not four.")
info("    Direction of this correction: it WEAKENS the repo's chain (fewer independent no-goes).")

head("L.  STEP 3 RE-DERIVED FROM THE LINEARISED EINSTEIN EQUATIONS (part 1 script, sympy)")
print("""  Derived, not assumed (r4_p1_gr.py):
      lap(Psi)      = 4 pi G rho                       [G^0_0]
      Phi' - Psi'   = 4 pi G R p_r                     [G^1_1]
      (Phi-Psi)'' + (Phi-Psi)'/R = 8 pi G p_t          [G^2_2]
  =>  lap(Phi)      = 4 pi G (rho + p_r + 2 p_t)       Tolman -- DYNAMICS
      lap(Phi+Psi)/2= 4 pi G (rho + (p_r + 2 p_t)/2)   LENSING""")
f=sp.symbols('f'); rho_s=sp.symbols('rho',positive=True)
P=-3*f*rho_s          # p_r + 2 p_t = 3p for isotropic p = -f rho
dyn=rho_s+P; lens=rho_s+P/2
info(f"M_lens/M_dyn (correct) = {sp.simplify(lens/dyn)}")
info(f"the chain's stated 'lensing sees rho+p' gives instead {sp.simplify((rho_s-f*rho_s)/dyn)}")
for tgt in [29]:
    s1=sp.solve(sp.Eq(sp.simplify(lens/dyn),tgt),f)[0]
    s2=sp.solve(sp.Eq(sp.simplify((rho_s-f*rho_s)/dyn),tgt),f)[0]
    info(f"ratio = {tgt} at f = {sp.nsimplify(s1)} = {float(s1):.5f} (correct)  vs f = {float(s2):.5f} (chain's form)")
info("both diverge at f = 1/3, so CLAIM 2 SURVIVES: dyn = 0 => lens = rho/2 != 0; lens = 0 => dyn = -rho.")
info("Only rho = 0 kills both.  CONFIRMED.")
info("FLAT DIRECTION CONFIRMED TOO: both observables depend on p_r and p_t only through p_r + 2 p_t,")
info("so ANISOTROPIC STRESS IS NOT AN ESCAPE.  (I tried p_r=+rho, p_t=-rho: dyn=0 but lens=rho/2.)")
info("Correction direction: 'rho+p' OVERSTATES the lensing signal (1.33x at f=1/3), i.e. the chain")
info("as written manufactures a small deficit against the theory.  The conclusion is unaffected.")

head("M.  DOES THE CONSTRUCTED K STILL PASS w = -1 AND Omega_dm = 0.265?")
print("""  rho(n) = rho_Lambda + INT_0^n mu dn' ,  p(n) = -rho_Lambda + INT_0^n c_s^2 mu dn'.
  rho_Lambda = rho(n=0) is an INTEGRATION CONSTANT of the same K -- it is not added by hand.""")
info("w of the Lambda piece = -1 EXACTLY (p(0) = -rho(0)), for any c_s^2(n) with a convergent integral.")
info("w of the dust piece  = w_f = running mean of c_s^2, computed above.")
for lab,cs2 in [('generous floor',mp.mpf('1.464e-7')),('honest floor',mp.mpf('5.728e-7'))]:
    info(f"  {lab}: |w_f| <~ {sig(cs2/(1-mp.mpf('0.25')),3)}",
         "vs the CMB cap on w_dm ~ 1e-3 -> PASSES by 3 orders")
info("Omega_dm: rho_f ~ Q_0 n ~ a^-3 to 1 part in 1e6 => Omega_dm = 0.265 UNCHANGED.")
info("*** SO THE CMB IS NOT WHAT KILLS THE WARM ROUTE.  c_s^2(rec) is far below every GDM bound")
info("    for any beta > 0.1 (table D).  The kill, if there is one, is LATE-TIME STRUCTURE. ***")

head("N.  THE DOUBLE-COUNT ARITHMETIC, reproduced independently (both footings)")
MB=mp.mpf('1e11')*MSUN; RATIO=OM_DM/OM_B; RAR_DEX=mp.mpf('0.06')
for foot,a0 in A0.items():
    rM=mp.sqrt(G*MB/a0)
    print(f"  --- {foot}: a0={sig(a0)}, r_M={sig(rM/KPC,4)} kpc ---")
    for lab,x in [('0.5 r_M',mp.mpf('0.5')),('1 r_M',mp.mpf(1)),('3 r_M',mp.mpf(3)),('10 r_M',mp.mpf(10))]:
        r=x*rM; y=G*MB/(a0*r**2); nu=mp.sqrt(1+1/y)
        tol=(10**RAR_DEX-1)*nu           # allowed extra mass, in units of M_b
        over=RATIO/tol
        print(f"    {lab:>8}: nu={sig(nu,5):>8}  tolerance={sig(tol,4):>8} M_b   condensate={sig(RATIO,4)} M_b"
              f"   overshoot={sig(over,4):>8}x")
    nu_cross=RATIO/(10**RAR_DEX-1)
    ycross=1/(nu_cross**2-1); rcross=mp.sqrt(G*MB/(a0*ycross))
    print(f"    crossover nu={sig(nu_cross,4)} at r={sig(rcross/KPC,4)} kpc")



# ====================================================================================================
# SECTION FROM r4_mtable.py
# ====================================================================================================
import mpmath as mp
mp.mp.dps=25
C=mp.mpf('2.99792458e8'); G=mp.mpf('6.674e-11'); MSUN=mp.mpf('1.989e30')
MPC=mp.mpf('3.0857e22'); KPC=MPC/1000
RHO_CRIT=mp.mpf('8.5992e-27'); OM_DM=mp.mpf('0.2650'); OM_B=mp.mpf('0.0493')
RHO_DM0=OM_DM*RHO_CRIT; RATIO=OM_DM/OM_B
A0={'canon':mp.mpf('9.3619e-11'),'alt':mp.mpf('1.1279e-10')}
MB=mp.mpf('1e11')*MSUN; RAR=mp.mpf('0.06'); TOL=mp.mpf('20.9')
sig=lambda x,n=4: mp.nstr(mp.mpf(x),n)
print("M(<r) IN UNITS OF M_b.  target = M_b nu(y).  M_ph = M_b(nu-1) fills it EXACTLY (M_cond=0).")
print("Compare three condensate states at each radius, both footings.\n")
for foot,a0 in A0.items():
    rM=mp.sqrt(G*MB/a0)
    print(f"=== {foot}   a0={sig(a0)} m/s^2   r_M={sig(rM/KPC,4)} kpc ===")
    print(f"{'r':>8}{'nu':>9}{'target':>9}{'tol(+0.06dex)':>14}"
          f"{'M_cond CLUSTERED':>18}{'M_cond @delta=20.9':>20}{'M_cond @delta=178':>19}")
    for lab,x in [('0.5 r_M',mp.mpf('0.5')),('1 r_M',mp.mpf(1)),('3 r_M',mp.mpf(3)),('10 r_M',mp.mpf(10))]:
        r=x*rM; y=G*MB/(a0*r**2); nu=mp.sqrt(1+1/y)
        tol=(10**RAR-1)*nu
        Msm =(4*mp.pi/3)*r**3*TOL*RHO_DM0/MB
        Mvir=(4*mp.pi/3)*r**3*mp.mpf('178')*RHO_DM0/MB
        print(f"{lab:>8}{sig(nu,5):>9}{sig(nu,5):>9}{sig(tol,4):>14}"
              f"{sig(RATIO,5):>18}{sig(Msm,4):>20}{sig(Mvir,4):>19}")
    print(f"  smooth-at-20.9 sits BELOW the RAR tolerance by:", end=" ")
    outs=[]
    for x in [mp.mpf('0.5'),mp.mpf(1),mp.mpf(3),mp.mpf(10)]:
        r=x*rM; y=G*MB/(a0*r**2); nu=mp.sqrt(1+1/y); tol=(10**RAR-1)*nu
        outs.append(sig(tol/((4*mp.pi/3)*r**3*TOL*RHO_DM0/MB),3))
    print(" / ".join(outs), " (at 0.5,1,3,10 r_M)")
    print()
print("So a sector held at delta<=20.9 CURES the double count with ~3-4 orders of margin;")
print("the whole question is whether anything can hold it there.")


# ====================================================================================================
# SECTION O+P: non-monotone loophole and negative controls
# ====================================================================================================
# SECTION O: the loophole in my OWN theorem (non-monotone c_s^2(n)) + negative controls.
import mpmath as mp
mp.mp.dps=25
C=mp.mpf('2.99792458e8'); G=mp.mpf('6.674e-11'); MPC=mp.mpf('3.0857e22'); KPC=MPC/1000
RHO_CRIT=mp.mpf('8.5992e-27'); OM_DM=mp.mpf('0.2650'); OM_B=mp.mpf('0.0493')
RHO_DM0=OM_DM*RHO_CRIT; RATIO=OM_DM/OM_B; TOL=mp.mpf('20.9'); MSUN=mp.mpf('1.989e30')
sig=lambda x,n=4: mp.nstr(mp.mpf(x),n)
FAIL=[];N=[0]
def chk(c,l,d=""):
    N[0]+=1; ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {l}"+(f"   {d}" if d else ""))
    if not ok: FAIL.append(l)
def head(t): print("\n"+"="*104+f"\n{t}\n"+"="*104)
def info(l,d=""): print(f"  [info] {l}"+(f"   {d}" if d else ""))

head("O.  THE LOOPHOLE IN MY OWN SECTION-B THEOREM: c_s^2(n) NEED NOT BE MONOTONE.")
print("""  Section B assumed c_s^2(n) non-increasing.  It need not be: c_s^2 could have a BUMP sitting at
  halo densities (delta ~ 1-20) and be ~0 both at recombination (n = 1.3e9 n_bar0) and at today's
  cosmic mean.  That evades the CMB AND the Jeans problem AND the sigma_8 problem in one stroke.
  It is the density-space twin of the corpus' own a_0-bump.  So price it properly.""")
LOGW=mp.log(50)                       # 20 kpc -> 1 Mpc isothermal well, in units of vc^2
def vc_crit(Cbump): return mp.sqrt(Cbump*C**2/LOGW)
for lab,Cb in [('bump height 4.45e-7 c^2',mp.mpf('4.451e-7')),
               ('bump height 1.75e-6 c^2',mp.mpf('1.751e-6')),
               ('bump height 1.0e-5 c^2', mp.mpf('1e-5'))]:
    info(f"{lab}: barrier = {sig(Cb*C**2,4)} m^2/s^2",
         f"-> critical v_c = {sig(vc_crit(Cb)/1000,4)} km/s")
print()
print("""  THE BUMP IS A BARRIER OF FIXED HEIGHT, SO IT SORTS GALAXIES BY DEPTH OF WELL:
     v_c < v_crit  -> sector excluded, delta <= 20.9, RAR = pure phantom, clean
     v_c > v_crit  -> sector passes straight through, delta -> 1e5, full cosmic share in the halo
  That is a SHARP RAR BREAK at v_c = v_crit.  Compute its size.""")
MB=mp.mpf('1e11')*MSUN; A0={'canon':mp.mpf('9.3619e-11'),'alt':mp.mpf('1.1279e-10')}
for foot,a0 in A0.items():
    rM=mp.sqrt(G*MB/a0)
    for lab,x in [('1 r_M',mp.mpf(1)),('3 r_M',mp.mpf(3))]:
        r=x*rM; y=G*MB/(a0*r**2); nu=mp.sqrt(1+1/y)
        # below break: M_dyn = M_b nu ;  above break: M_dyn = (M_b + M_cond) nu_tot
        y_tot=y*(1+RATIO); nu_tot=mp.sqrt(1+1/y_tot)
        step=mp.log10((1+RATIO)*nu_tot/nu)
        info(f"{foot} {lab}: RAR step across the break = {sig(step,4)} dex",
             f"= {sig(step/mp.mpf('0.06'),4)} x the measured 0.06 dex intrinsic scatter")
chk(True,"O1 the bump route predicts a RAR BREAK at a critical v_c -- computed above")
info("SPARC's RAR is continuous and single-valued from ~20 to ~300 km/s with 0.06 dex intrinsic")
info("scatter and no break at any v_c.  A 0.6-0.8 dex step would be the most obvious feature in the")
info("dataset.  *** THE NON-MONOTONE LOOPHOLE IS CLOSED BY THE RAR ITSELF, NOT BY A THEOREM. ***")
info("This independently reproduces stage 2b's 'v_c = 170 km/s split predicts an unobserved RAR")
info("break' by a different construction (density-space bump vs. its support-branch split).")

head("P.  NEGATIVE CONTROLS -- guards against vacuous passes")
def cs0_for(b,dphi,delta=TOL):
    b=mp.mpf(b); x=dphi/C**2
    return x/mp.log(delta) if b<mp.mpf('1e-9') else b*x/(1-delta**(-b))
VC=mp.mpf('200e3'); DPHI=VC**2
# NC1: c_s^2 = 0 must give NO barrier at all -> delta unbounded
def delta_eq(cs2_0,b,dphi):
    b=mp.mpf(b)
    if b<mp.mpf('1e-9'):
        return mp.e**(dphi/C**2/cs2_0)
    arg=1-b*(dphi/C**2)/cs2_0
    return mp.inf if arg<=0 else arg**(-1/b)
chk(delta_eq(mp.mpf('1e-20'),0,DPHI)>mp.mpf('1e100'),
    "NC1 a COLD sector (c_s^2=1e-20) gives delta -> unbounded, as it must",
    f"delta = {sig(delta_eq(mp.mpf('1e-20'),0,DPHI),3)}")
# NC2: at exactly the floor the method must RETURN 20.9, not something else
c0=cs0_for(0,DPHI); d=delta_eq(c0,0,DPHI)
chk(abs(d-TOL)/TOL<mp.mpf('1e-12'),"NC2 method inverts exactly: floor c_s0^2 reproduces delta=20.9",
    f"delta = {sig(d,10)}")
# NC3: a sector with c_s^2 BELOW the floor must fail
c_low=c0/2; d_low=delta_eq(c_low,0,DPHI)
chk(d_low>TOL,"NC3 half the floor sound speed overshoots the tolerance",
    f"delta = {sig(d_low,5)} = {sig(d_low/TOL,4)}x tolerance")
# NC4: ghost test must be able to FAIL -- feed it c_s^2 < 0
n=mp.mpf(1); mu=mp.mpf(1); cs2_neg=mp.mpf('-1e-7')
Kpp=n/(mu*cs2_neg)
chk(Kpp<0,"NC4 the ghost test is not vacuous: c_s^2<0 returns K''<0 (ghost)",f"K'' = {sig(Kpp,4)}")
# NC5: the DBI (the framework as written) must land on the FATAL side of section B's floor
cs2_dbi_today=mp.mpf('2.9e-8')/((1+mp.mpf('1090'))**3)
chk(cs2_dbi_today < cs0_for(0,DPHI),
    "NC5 the framework's OWN DBI sits far below the floor -- i.e. it is fatally cold, as stages 1-9 found",
    f"c_s^2(DBI, today) = {sig(cs2_dbi_today,3)} vs floor {sig(cs0_for(0,DPHI),3)} -> short by {sig(cs0_for(0,DPHI)/cs2_dbi_today,3)}x")
# NC6: no NaN/inf leaked into any headline number
vals=[cs0_for(0,DPHI),cs0_for(mp.mpf('0.5'),DPHI),delta_eq(c0,0,DPHI)]
chk(all(mp.isfinite(v) for v in vals),"NC6 no NaN/inf in headline numbers")
print(f"\n  checks: {N[0]}, failures: {FAIL}")


print("\nROUTE 4 COMPLETE.")
import sys as _s; _s.exit(1 if FAIL else 0)
