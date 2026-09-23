#!/usr/bin/env python3
"""Exact checks of a nonlinear lapse-acceleration static completion.

Run from repo root; --output must name a writable JSON result file.
This checks identities, algebraic counterexamples and analytic proof ingredients,
not cosmological viability, PPN, a PDE existence theorem or full-theory health.
"""
import argparse
import json
from pathlib import Path
import sympy as s

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
args = ap.parse_args()
checks = []
def check(name, assertion, detail=None):
    ok = bool(assertion)
    checks.append({'name': name, 'pass': ok, 'detail': str(detail or '')})
    print(('PASS ' if ok else 'FAIL ') + name)
    if not ok:
        raise AssertionError(name)
def zero(e):
    return s.simplify(e) == 0

# Newtonian action: conformal h_ij=e^{-2Phi}delta_ij, N=1+Psi.
x, ep = s.symbols('x epsilon', real=True)
Phi, Psi, P = [s.Function(q)(x) for q in ('Phi', 'Psi', 'P')]
d, G, rho = s.symbols('d G rho', positive=True)
f, J = s.Function('f'), s.Function('J')
X, Y = s.diff(Psi, x)**2, s.diff(P, x)**2
EH = s.exp(-ep*Phi)*(1+ep*Psi)*(4*ep*s.diff(Phi,x,2)-2*ep**2*s.diff(Phi,x)**2)
EH2 = s.diff(EH,ep,2).subs(ep,0)/2
EH2_ibp = 2*s.diff(Phi,x)**2-4*s.diff(Phi,x)*s.diff(Psi,x)
check('EH Newtonian action modulo explicit boundary derivative',
      zero(EH2-EH2_ibp-s.diff(4*(Psi-Phi)*s.diff(Phi,x),x)))
L = EH2_ibp+f(X)+2*d*s.diff(Psi,x)*s.diff(P,x)-d*J(Y)-16*s.pi*G*rho*Psi
def EL(q):
    return s.diff(L,q)-s.diff(s.diff(L,s.diff(q,x)),x)
fX = s.Subs(s.Derivative(f(s.Symbol('u')),s.Symbol('u')),s.Symbol('u'),X)
jY = s.Subs(s.Derivative(J(s.Symbol('u')),s.Symbol('u')),s.Symbol('u'),Y)
check('lapse equation has L279 factors', zero(EL(Psi)-(4*s.diff(Phi,x,2)-2*s.diff(fX*s.diff(Psi,x),x)-2*d*s.diff(P,x,2)-16*s.pi*G*rho)))
check('spatial metric equation is slip Laplacian', zero(EL(Phi)-4*s.diff(Psi-Phi,x,2)))
check('scalar flux equation has unit lapse coefficient', zero(EL(P)-2*d*s.diff(jY*s.diff(P,x)-s.diff(Psi,x),x)))

# Independent vector Hessian computation using a generic Taylor jet.
gv = s.Matrix(s.symbols('g1:4', real=True))
vv = s.Matrix(s.symbols('v1:4', real=True))
dg = s.Matrix(s.symbols('u1:4', real=True))
dv = s.Matrix(s.symbols('w1:4', real=True))
fx, fxx, jy, jyy = s.symbols('f_X f_XX J_Y J_YY', real=True)
xt, yt = (gv+ep*dg).dot(gv+ep*dg), (vv+ep*dv).dot(vv+ep*dv)
dx, dy = xt-gv.dot(gv), yt-vv.dot(vv)
fjet, jjet = fx*dx+fxx*dx**2/2, jy*dy+jyy*dy**2/2
energy = 2*xt-fjet-2*d*(gv+ep*dg).dot(vv+ep*dv)+d*jjet
q2 = s.diff(energy,ep,2).subs(ep,0)/2
Am = (2-fx)*s.eye(3)-2*fxx*gv*gv.T
Bm = jy*s.eye(3)+2*jyy*vv*vv.T
check('generic six-gradient Hessian from Taylor variation', zero(q2-(dg.dot(Am*dg)-2*d*dg.dot(dv)+d*dv.dot(Bm*dv))))
aa, bb = s.symbols('alpha_theta B_theta', real=True)
M = s.Matrix([[2-aa,-d],[-d,d*bb]])
check('directional static determinant', zero(M.det()-d*((2-aa)*bb-d)))

# Frozen short-wavelength scalar ADM action, without healing for this check.
c2, k2, Kp = s.symbols('c2 k2 Kp', positive=True)
zd, shift, z, n, pp, pd = s.symbols('zdot shift z n p pdot', real=True)
Kmetric = -3*(2+3*c2)*zd**2-2*(2+3*c2)*k2*shift*zd-c2*k2**2*shift**2
shift_sol = s.solve(s.diff(Kmetric,shift),shift)[0]
Kz = s.factor(Kmetric.subs(shift,shift_sol)/zd**2)
check('ADM shift elimination produces positive clock kinetic coefficient', zero(Kz-2*(2+3*c2)/c2))
Lgrad = k2*(2*z**2+4*z*n+aa*n**2+2*d*n*pp-d*bb*pp**2)
n_sol = s.solve(s.diff(Lgrad,n),n)[0]
H = -s.hessian(s.expand(Lgrad.subs(n,n_sol)/k2),(z,pp))/2
H_expected = s.Matrix([[4/aa-2,2*d/aa],[2*d/aa,d*bb+d**2/aa]])
check('frozen lapse elimination spatial matrix', all(zero(e) for e in H-H_expected))
check('dynamic/static determinant relation', zero(H.det()-2*d/aa*((2-aa)*bb-d)))

# Interpolation p=1/2 and p=1.
u, Astar, lo, hi = s.symbols('u Astar alpha_lo alpha_hi', positive=True)
Delta = hi-lo
alpha_half = lo+Delta/s.sqrt(1+u)
alphaL_half = s.simplify(alpha_half+2*u*s.diff(alpha_half,u))
check('p=1/2 longitudinal coefficient', zero(alphaL_half-(lo+Delta/(1+u)**s.Rational(3,2))))
alpha_one = lo+Delta/(1+u)
alphaL_one = s.factor(alpha_one+2*u*s.diff(alpha_one,u))
check('p=1 longitudinal coefficient', zero(alphaL_one-(lo+Delta*(1-u)/(1+u)**2)))
check('p=1 coefficient stationary at u=3', zero(s.diff(alphaL_one,u).subs(u,3)))
check('p=1 minimum value is lo-Delta/8', zero(alphaL_one.subs(u,3)-(lo-Delta/8)))
vals = {lo:s.Rational(1,10**7),hi:s.Rational(1,2),d:s.Rational(9,5)}
negative_min = s.factor(alphaL_one.subs(u,3).subs(vals))
check('p=1 exact proposed-parameter counterexample', negative_min<0, negative_min)
roots_one = s.solve(s.together(alphaL_one.subs(vals)).as_numer_denom()[0],u)
fhalf = lo*u*Astar**2+2*Delta*Astar**2*(s.sqrt(1+u)-1)
fone = lo*u*Astar**2+Delta*Astar**2*s.log(1+u)
check('p=1/2 action primitive', zero(s.diff(fhalf,u)/Astar**2-alpha_half))
check('p=1 action primitive', zero(s.diff(fone,u)/Astar**2-alpha_one))
check('p=1/2 endpoint coefficients', zero(alpha_half.subs(u,0)-hi) and zero(s.limit(alpha_half,u,s.oo)-lo))

# Retuned scalar kernel with bounded v. Domain: 0<=v<V, 0<lo<hi<2.
v, V, g = s.symbols('v V g', positive=True)
Ahi, Alo = 2-hi, 2-lo
b = d/Ahi
Jv = -2*b*V*v-2*b*V**2*s.log(1-v/V)
j = b/(1-v/V)
BLong = s.diff(j*v,v)
check('bounded-kernel action primitive and origin', zero(s.diff(Jv,v)/(2*v)-j) and zero(Jv.subs(v,0)))
check('bounded-kernel longitudinal stiffness', zero(BLong-b/(1-v/V)**2))
v_of_g = V*g/(g+b*V)
check('scalar first integral inverted exactly', zero((j*v).subs(v,v_of_g)-g))
alpha_g = lo+Delta*Astar/s.sqrt(Astar**2+g**2)
Ag = 2-alpha_g
ALg = s.diff(Ag*g,g)
flux = s.factor(Ag*g-d*v_of_g)
flux_expected = Alo*g-Delta*Astar*g/s.sqrt(Astar**2+g**2)-d*V*g/(g+b*V)
check('spherical gravitational flux', zero(flux-flux_expected))
check('positive radial-flux derivative decomposition', zero(s.diff(flux,g)-((ALg-Ahi)+Ahi*(1-(b*V/(g+b*V))**2))))
check('positive transverse flux decomposition', zero(flux/g-((Ag-Ahi)+Ahi*g/(g+b*V))))
check('deep-MOND bare-G coefficient', zero(s.limit(flux/g**2,g,0)-Ahi**2/(d*V)))
check('high-acceleration measured G normalization', zero(s.limit(flux/g,g,s.oo)-Alo))
boost = g-flux/Alo
ceiling = (Delta*Astar+d*V)/Alo
check('bounded total force ceiling', zero(s.limit(boost,g,s.oo)-ceiling))
check('boost approaches ceiling monotonically', zero(s.diff(boost,g)-(Delta*Astar**3/(Astar**2+g**2)**s.Rational(3,2)+d*b*V**2/(g+b*V)**2)/Alo))
a0 = s.symbols('a0',positive=True)
Vcal = a0*Ahi**2/(d*Alo)
check('deep-MOND a0 calibration', zero((d*Alo*V/Ahi**2).subs(V,Vcal)-a0))
beta_old = d/Alo
bad_det = s.factor((Ahi*beta_old-d).subs(vals))
check('unchanged local-baseline scalar kernel is negative at zero field', bad_det<0,bad_det)

# Strong positivity proof ingredients as algebraic nonnegative decompositions.
t = s.symbols('t',nonnegative=True)
ut = s.symbols('u_theta',nonnegative=True)
av = lo+Delta*(1+u*(1-ut))/(1+u)**s.Rational(3,2)
check('directional alpha interpolates its transverse/longitudinal endpoints', zero(av-(alpha_half+ut*(alphaL_half-alpha_half))))
at, bt = s.symbols('a_increment b_increment',nonnegative=True)
check('coupled symbol determinant positivity decomposition', zero((Ahi+at)*(b+bt)-d-(Ahi*bt+b*at+at*bt)))

# Reconstruction target g_N=mu(g)*g, spherical sector only.
mu = s.Function('mu')(g)
vr = g*(Ag-Alo*mu)/d
vrprime = s.diff(vr,g)
check('target-kernel monotonicity derivative', zero(vrprime-(ALg-Alo*s.diff(g*mu,g))/d))
check('target transverse determinant', zero(Ag*g/vr-d-Alo*mu*g/vr))
check('target longitudinal determinant', zero(ALg/vrprime-d-Alo*s.diff(g*mu,g)/vrprime))
C = s.symbols('C',positive=True)
v_exact_ceiling = s.simplify(vr.subs(mu,1-C/g))
check('exact total plateau makes p=1/2 scalar decrease', zero(s.diff(v_exact_ceiling,g)+Delta*Astar**3/(d*(Astar**2+g**2)**s.Rational(3,2))))

# Threshold identities; inequalities are proved in REPORT.md, not inferred from sampling.
ec, el = s.symbols('eps_cos eps_local',positive=True)
rc2, rl2 = (1-ec)**-2-1, el**-2-1
check('cosmological threshold inversion', zero((1+rc2)*(1-ec)**2-1))
check('local threshold inversion', zero((1+rl2)*el**2-1))
af = s.Function('alpha')(g)
check('profile-independent monotone product identity', zero(s.diff(g*af,g)-(af+g*s.diff(af,g))))

result = {
    'status':'exact_identities_and_counterexample_verified',
    'checks_passed':len(checks), 'checks':checks,
    'parameters':{'alpha_lo':'1/10000000','alpha_hi':'1/2','d':'9/5','c2':'3/100'},
    'p1_minimum':str(negative_min),
    'p1_negative_interval_X_over_Astar2':[{ 'exact':str(q),'decimal':str(s.N(q,18)) } for q in roots_one],
    'retained_old_baseline_determinant_factor':str(bad_det),
    'V_over_a0':str(s.factor((Vcal/a0).subs(vals))),
    'G_N_over_G':str(s.factor((2/Alo).subs(vals))),
    'bare_clock_speed_squared_reference':str(s.factor((3*s.Rational(3,100)/(2+3*s.Rational(3,100))))),
    'non_claims':[
        'No PPN or gravitational-Cherenkov bound transfer.',
        'No exact target RAR fit; reconstruction applies to aligned/spherical branch.',
        'No global nonlinear PDE existence, finite-k cosmological health, or cutoff certification.',
        'No empirical assumption about separation of cosmic and local invariant accelerations.'
    ]
}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(f'{len(checks)}/{len(checks)} checks passed; wrote {args.output}')
