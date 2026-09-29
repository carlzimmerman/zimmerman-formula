#!/usr/bin/env python3
"""C3: exact holographic charge equalities (extremal RN entropy; maximal RN-dS charge). See C0_PREREGISTRATION.md.
--mutate : S = 2 pi alpha N^2 and Q^2 = 1/(2 Lambda) are asserted instead (both must FAIL)."""
import sys, math
import sympy as sp
from mpmath import mp, mpf, sqrt, pi
mp.dps = 30
MUT = '--mutate' in sys.argv
fails = []
def check(name, ok):
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok: fails.append(name)

# ---- C3a: extremal RN entropy, Gaussian units. horizon radius r+ = sqrt(G) Q/c^2 (from f = 1 - 2GM/(c^2 r) + G Q^2/(c^4 r^2), extremal double root)
G,c,hb,Q,r,M,N,al = sp.symbols('G c hbar Q r M N alpha', positive=True)
f = 1 - 2*G*M/(c**2*r) + G*Q**2/(c**4*r**2)
Mext = sp.sqrt(G)*Q/G*1  # placeholder; solve properly below
Msol = sp.solve(sp.discriminant(sp.numer(sp.together(f)), r), M)
Msol = [m for m in Msol if m.is_positive is not False][0]
print('extremal mass M = ', sp.simplify(Msol))
rplus = sp.solve(sp.Eq(sp.numer(sp.together(f.subs(M, Msol))), 0), r)[0]
print('r+ = ', sp.simplify(rplus))
S = pi_s = sp.pi*rplus**2*c**3/(G*hb)          # S = A/(4 l_P^2), A = 4 pi r+^2, l_P^2 = G hbar/c^3
Sq = sp.simplify(S.subs(Q, N*sp.sqrt(al*hb*c)))   # Q = N e, e^2 = alpha hbar c
print('S_ext = ', Sq)
want = sp.pi*al*N**2 if not MUT else 2*sp.pi*al*N**2
check('C3a S_ext = pi alpha N^2' + (' [MUTATE: 2 pi alpha N^2]' if MUT else ''), sp.simplify(Sq-want) == 0)
Mq = sp.simplify(Msol.subs(Q, N*sp.sqrt(al*hb*c)))   # M in mass units; M_Pl^2 = hbar c/G
ratio = sp.simplify(Mq**2/(hb*c/G))
print('M_ext^2/M_Pl^2 = ', ratio)
check('C3a extremal mass M = sqrt(alpha) N M_Pl (Gaussian, non-reduced Planck mass)', sp.simplify(ratio - al*N**2) == 0)

# ---- C3b: RN-dS ultracold triple root (geometrized G=c=1): r^2 f = -L/3 r^4 + r^2 - 2 M r + Q2
L, r0, Q2, Mg = sp.symbols('Lambda r0 Q2 M_g', positive=True)
P = -L/3*r**4 + r**2 - 2*Mg*r + Q2
sol = sp.solve([P, sp.diff(P,r), sp.diff(P,r,2)], [r, Mg, Q2], dict=True)
sol = [s for s in sol if all(v.is_positive for v in s.values())]
print('triple-root solution (r, M, Q^2):', sol)
Q2max = sp.simplify(sol[0][Q2])
trial = sp.Rational(1,4)/L if not MUT else sp.Rational(1,2)/L
check('C3b ultracold Q_geo^2 = 1/(4 Lambda)' + (' [MUTATE: 1/(2 Lambda)]' if MUT else ''), sp.simplify(Q2max-trial) == 0)
# also verify residual explicitly with the mutated or true value
rr = sol[0][r]; MM = sol[0][Mg]
res = sp.simplify(P.subs({r:rr, Mg:MM, Q2:trial}))
print('triple-root residual with tested Q^2 =', res)
check('C3b residual of f at the triple point vanishes for the tested Q^2', res == 0)
# geometrized: Q_geo^2 = G Q^2/c^4 = N^2 alpha l_P^2, Lambda l_P^2 = x  ==> N_max^2 = 1/(4 alpha x)

# ---- C3c numbers
G_ = mpf('6.67430e-11'); c_ = mpf('299792458'); hb_ = mpf('1.054571817e-34')
Mpc = mpf('3.0856775814913673e22'); H0 = mpf('67.4')*1000/Mpc; OL = mpf('0.6847')
Lam = 3*OL*H0**2/c_**2
xx = Lam*G_*hb_/c_**3
alpha = 1/mpf('137.035999177')
Nmax = 1/(2*sqrt(alpha*xx))
SdS = 3*pi/xx
print('\nC3c x = Lambda l_P^2 = %s ; S_dS = 3 pi/x = %s ; N_max(alpha=1/137.036) = %s' % (mp.nstr(xx,5), mp.nstr(SdS,5), mp.nstr(Nmax,5)))
print('     N_max/sqrt(S_dS) = %s = 1/(2 sqrt(3 pi alpha)) (a pure function of alpha, not a prediction)' % mp.nstr(Nmax/sqrt(SdS),6))
check('C3c x matches AH5 (2.85e-122 within 1%)', abs(xx/mpf('2.85e-122')-1) < 0.01)
print('     unit-charge extremal object: M/M_Pl = sqrt(alpha) = %s ; S = pi alpha = %s nats ; r+/l_P = sqrt(alpha) = %s' % (mp.nstr(sqrt(alpha),5), mp.nstr(pi*alpha,5), mp.nstr(sqrt(alpha),5)))
print('     => unit charge is sub-Planckian (S<1): not a semiclassical black hole; WGC states are particles, not BHs.')

# ---- C3d alpha-trading test
print('\nC3d: for each alpha, the equality N_max^2 = 1/(4 alpha x) has a solution:')
rejected = 0
for a in [1/mpf('137.036'), mpf(1)/100, mpf(1)/50, mpf(1)/10]:
    n = 1/(2*sqrt(a*xx))
    ok = n > 1
    rejected += (not ok)
    print('   alpha=%s -> N_max=%s (exists=%s)' % (mp.nstr(a,5), mp.nstr(n,5), ok))
check('C3d the holographic equalities reject NO alpha (they trade alpha for the undetermined count N_max)', rejected == 0)
print('exit', 1 if fails else 0)
sys.exit(1 if fails else 0)
