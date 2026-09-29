#!/usr/bin/env python3
"""C2: emergence (1/e^2 = 0 at the species scale). See C0_PREREGISTRATION.md.
--mutate : uses the wrong one-loop coefficient 1/(3 pi) in the coefficient check (must FAIL)."""
import sys, math
from fractions import Fraction as F
import sympy as sp
from mpmath import mp, mpf, quad, log, pi, sqrt, findroot, exp
mp.dps = 30
MUT = '--mutate' in sys.argv
fails = []
def check(name, ok):
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok: fails.append(name)

# ---- C2a: coefficients, derived not recalled
x = sp.symbols('x')
I = sp.integrate(x*(1-x), (x, 0, 1))
print('int_0^1 x(1-x) dx =', I)
# Pi(q^2) log-Lambda coefficient: -(2 alpha/pi) * I * ln(Lambda^2) => d(1/alpha)/d ln mu = -(2/pi)*... derive:
# alpha_eff = alpha/(1 - Pi), Pi ~ -(2 alpha/pi) I ln(Lambda^2/mu^2)*(-1)... use standard: 1/alpha(mu) = 1/alpha(m) - (4 I/pi) ln(mu/m)
coef = sp.Rational(4,1)*I/sp.pi        # = 2/(3 pi)
print('d(1/alpha)/d ln mu = -%s per Dirac fermion of unit charge' % sp.nsimplify(coef))
target = sp.Rational(2,3)/sp.pi if not MUT else sp.Rational(1,3)/sp.pi
check('C2a QED coefficient equals 2/(3 pi)' + (' [MUTATE uses 1/(3 pi)]' if MUT else ''), sp.simplify(coef-target) == 0)
# numeric cross-check of the Feynman integral
val = quad(lambda t: t*(1-t), [0,1]); check('C2a numeric Feynman integral = 1/6', abs(val-mpf(1)/6) < mpf('1e-25'))
# SM one-loop coefficients from field content (exact)
# per generation Weyl fermions (colour x SU2 multiplicity, Y): Q_L (6,1/6) u_R (3,2/3) d_R (3,-1/3) L (2,-1/2) e_R (1,-1)
Y = [(6,F(1,6)),(3,F(2,3)),(3,F(-1,3)),(2,F(-1,2)),(1,F(-1))]
bY = 3*F(2,3)*sum(n*y*y for n,y in Y) + F(1,3)*2*F(1,4)      # 3 gens + complex Higgs doublet Y=1/2
b2 = -F(22,3)*2/2*1 - F(0)  # placeholder replaced below
b2 = -F(11,3)*2 + F(2,3)*(3*(3+1))*F(1,2)*1 + F(1,3)*F(1,2)      # -22/3 + Weyl doublets (3 gens x (3 colours + 1 lepton) = 12) * T=1/2 * 2/3 + Higgs 1/3 * 1/2
print('b_Y =', bY, ' b_2 =', b2)
check('C2a b_Y = 41/6', bY == F(41,6)); check('C2a b_2 = -19/6', b2 == F(-19,6))

# ---- inputs
Mred = mpf('2.435323e18'); MZ = mpf('91.1876')
ainv_Z = mpf('127.930'); s2 = mpf('0.23122')
ainv_Y_meas = ainv_Z*(1-s2)          # 1/alpha_Y = cos^2/alpha
counts = {'28':28, '118':118, '126':126}
tot_hits = 0; trials = 0
print('\nC2b hypercharge emergence: 1/alpha_Y(M_Z) predicted = (b_Y/2pi) ln(Lambda/M_Z)  ; measured = %s' % mp.nstr(ainv_Y_meas,6))
for k,n in counts.items():
    L = Mred/sqrt(n)
    pred = (mpf(41)/6/(2*pi))*log(L/MZ)
    rel = abs(pred-ainv_Y_meas)/ainv_Y_meas
    trials += 1; tot_hits += rel < mpf('1e-3')
    print('  N=%s Lambda=%s GeV predicted 1/alpha_Y=%s ratio meas/pred=%s' % (k, mp.nstr(L,4), mp.nstr(pred,5), mp.nstr(ainv_Y_meas/pred,4)))
LL = MZ*exp(ainv_Y_meas*2*pi/(mpf(41)/6))
print('  hypercharge Landau pole (one loop) at %s GeV = %s M_red ; alpha_Y would need charged content %.2fx larger for emergence at M_red/sqrt(118)' % (mp.nstr(LL,4), mp.nstr(LL/Mred,4), float(ainv_Y_meas/((mpf(41)/6/(2*pi))*log(Mred/sqrt(118)/MZ)))))
print('  non-abelian: b_2=-19/6<0, b_3<0: 1/g^2 grows in the UV, so 1/g^2(Lambda)=0 cannot hold for them (sign obstruction)')
check('C2b hypercharge emergence does not hit for any count', tot_hits == 0)

# ---- C2c toy QED emergence with measured masses, all charged Dirac fermions, sharp thresholds, no W
ferm = [('e',0.51099895e-3,1,1),('mu',0.1056584,1,1),('tau',1.77686,1,1),
        ('u',2.16e-3,3,mpf(2)/3),('d',4.67e-3,3,-mpf(1)/3),('s',0.0934,3,-mpf(1)/3),
        ('c',1.27,3,mpf(2)/3),('b',4.18,3,-mpf(1)/3),('t',172.57,3,mpf(2)/3)]
print('\nC2c toy QED emergence: 1/alpha(0) = (2/3pi) sum N_c q^2 ln(Lambda/m_f)')
def ainv_toy(L):
    return (mpf(2)/(3*pi))*sum(nc*q*q*log(L/mpf(m)) for _,m,nc,q in ferm)
target = mpf('137.035999177'); h2 = 0
sumq2 = sum(nc*q*q for _,m,nc,q in ferm)
for k,n in counts.items():
    L = Mred/sqrt(n); v = ainv_toy(L); rel = abs(v-target)/target
    trials += 1; h2 += rel < mpf('1e-3')
    print('  N=%s Lambda=%s GeV: 1/alpha_toy = %s (target/toy = %s)' % (k, mp.nstr(L,4), mp.nstr(v,6), mp.nstr(target/v,4)))
tot_hits += h2
check('C2c toy emergence does not hit for any count', h2 == 0)
Lreq = findroot(lambda t: ainv_toy(exp(t))-target, mp.log(Mred))
print('  REPORT ONLY (not scored): the cutoff that would be required is Lambda = %s GeV = %s M_red (a one-parameter solve, can always hit)' % (mp.nstr(exp(Lreq),4), mp.nstr(exp(Lreq)/Mred,4)))
print('  sum N_c q^2 over the charged Dirac fermions = %s' % mp.nstr(sumq2,6))
# ---- C2d precision bound
f = 2
dl = (mpf(2)/(3*pi))*sumq2*log(f)
print('\nC2d delta(1/alpha) from Lambda uncertain by factor 2 = %s  -> relative %s' % (mp.nstr(dl,4), mp.nstr(dl/target,4)))
check('C2d Lambda ambiguity of O(1) exceeds the 1e-3 hit tolerance (emergence cannot fix alpha to 1e-3 without a derived Lambda)', dl/target > mpf('1e-3'))
print('\ntotal scored hit-tests in C2: %d, hits %d, expected chance hits %.2e' % (trials, tot_hits, trials*2e-3/math.log(1e3)))
print('exit', 1 if fails else 0)
sys.exit(1 if fails else 0)
