#!/usr/bin/env python3
"""Exact critical stiff-pair checks plus a non-interval finite-D0 sample."""
import json
import math
import sys
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp

checks = []


def eq(name, left, right=0):
    value = s.simplify(left-right)
    if value != 0:
        raise AssertionError((name, value))
    checks.append(name)


r, k, G, Kb, f, rho0 = s.symbols('r k G Kb f rho0', positive=True)
Kc = Kb/(f*(1+f))
theta = s.sin(k*r)/(k*r)
rhob = rho0*theta
rhoc = f*rhob
mb = -4*s.pi*rho0*r*r*s.diff(theta, r)/(k*k)
mc = f*mb
eq('regular baryon center density', s.limit(rhob, r, 0), rho0)
eq('regular cold center density', s.limit(rhoc, r, 0), f*rho0)
eq('actual baryon enclosed mass', s.diff(mb, r), 4*s.pi*r*r*rhob)
eq('actual cold enclosed mass', s.diff(mc, r), 4*s.pi*r*r*rhoc)
Gsub = Kb*k*k/(2*s.pi*(1+f))
eq('baryonic force balance', s.diff(Kb*rhob**2, r)
   +rhob*Gsub*(mb+mc)/(r*r))
eq('critical charged force balance', s.diff(Kc*rhoc**2, r)
   +rhoc*Gsub*mb/(r*r))
eq('baryon free edge', rhob.subs(r, s.pi/k), 0)
eq('cold free edge', rhoc.subs(r, s.pi/k), 0)
eq('transverse baryon zero', s.diff(theta, r).subs(r, s.pi/k), -k/s.pi)
eq('transverse cold zero', f*s.diff(theta, r).subs(r, s.pi/k), -f*k/s.pi)
eq('finite baryon mass', mb.subs(r, s.pi/k), 4*s.pi**2*rho0/k**3)
eq('fixed Maxwell mass ratio', mc, f*mb)
a, b, ap, bp = s.symbols('a b ap bp', real=True)
u = a+b
v = f*a-(1+f)*b
up = ap+bp
vp = f*ap-(1+f)*bp
A = Kb/(2*s.pi)
eq('congruence derivative terms', A*up**2+Kc/(2*s.pi)*vp**2,
   (1+2*f)*(A/(1+f)*ap**2+A/f*bp**2))
eq('congruence gravity and Coulomb terms', u*u+2*u*v,
   (1+2*f)*(a*a-b*b))
eq('invertible channel map determinant', s.det(s.Matrix([[1,1],[f,-(1+f)]])),
   -(1+2*f))
R0sq = s.pi**2*A/(G*(1+f))
eq('Maxwell attractive radial margin', A/(1+f)*(s.pi**2+2)/R0sq-G,
   2*G/s.pi**2)
D, D0 = s.symbols('D D0', positive=True)
x = s.symbols('x', real=True)
H = D0*D0*(-D/D0-s.log(1-D/D0))
eq('nonlinear electric derivative', s.diff(H,D), D/(1-D/D0))
eq('nonlinear radial Hessian', s.diff(H,D,2), (1-D/D0)**-2)
eq('nonnegative extra electric Hessian factor', (1-x)**-2-1,
   x*(2-x)/(1-x)**2)
eq('Maxwell exterior energy limit', s.limit(H/(D*D),D,0), s.Rational(1,2))
mbv,mcv,t = s.symbols('mbv mcv t',positive=True)
lam = f*(1+f)
zprime = -lam*(mbv-mcv*x/(1-x))/(t*t)+f*(mbv+mcv)/(t*t)
eq('strict support splitting cooperative identity', zprime,
   (f*(mcv-f*mbv)+lam*mcv*x/(1-x))/(t*t))
rho,c,K = s.symbols('rho c K', positive=True)
eq('Gamma2 effective inertia for RTM edge test',
   (rho*c*c+2*K*rho*rho)*(1-2*K*rho/(c*c+2*K*rho)),rho*c*c)
hc=D0*D0*x**3/(1-x)**2
eq('positive finite-field threshold expression',hc.subs(x,s.Rational(1,10)),
   D0*D0/s.Integer(810))
gap=D0*D0*(-x-s.log(1-x)-x*x/2)
eq('phase traction jump increases from zero',s.diff(gap,x),D0*D0*x*x/(1-x))

F = 1341/250  # chosen ratio 5.364, not a derived abundance
LAMBDA = F*(1+F)
BASE_R = math.pi/math.sqrt(1+F)
T0=1e-6
RTOL=2e-11
ATOL=2e-13


def integrate(eta):
    initial = [1-(1+F)*T0*T0/6,
               F-LAMBDA*T0*T0/6+LAMBDA*eta*F*F*T0**3/27,
               T0**3/3,F*T0**3/3]

    def rhs(rr,y):
        tb,tc,mm_b,mm_c=y
        xx=eta*mm_c/(rr*rr)
        if xx>=.9:
            raise ValueError('Declared sample left the pole-safe region')
        return [-(mm_b+mm_c)/(rr*rr),
                -LAMBDA*(mm_b-mm_c*xx/(1-xx))/(rr*rr),
                rr*rr*max(tb,0),rr*rr*max(tc,0)]

    def edge_b(rr,y):return y[0]
    def edge_c(rr,y):return y[1]
    edge_b.direction=edge_c.direction=-1
    sol=solve_ivp(rhs,(T0,2*BASE_R),initial,events=[edge_b,edge_c],
                  rtol=RTOL,atol=ATOL,method='DOP853',dense_output=True,
                  max_step=BASE_R/20)
    assert sol.success and all(len(e)==1 for e in sol.t_events)
    rb=float(sol.t_events[0][0]);rc=float(sol.t_events[1][0]);outer=max(rb,rc)
    state=sol.sol(outer)
    mbfin=float(state[2]);mcfin=float(state[3]);xx=eta*mcfin/(outer*outer)
    no_reentry=mbfin-mcfin*xx/(1-xx)
    kap=(1+2/math.pi**2)*(BASE_R/outer)**2-1
    assert no_reentry>0 and kap>0
    if eta>0:
        assert rb<rc and mcfin/mbfin>F
    grid=np.geomspace(T0,outer,400)
    sample_x=eta*sol.sol(grid)[3]/(grid*grid)
    # A sample only: no interval ODE certification or full supremum claim.
    return {'eta':eta,'baryon_radius':rb,'cold_radius':rc,
            'Maxwell_base_radius':BASE_R,'kappa_L_diagnostic':kap,
            'baryon_mass':mbfin,'cold_mass':mcfin,'mass_ratio':mcfin/mbfin,
            'cold_outer_x':xx,'no_reentry_margin':no_reentry,
            'sampled_max_x':float(np.max(sample_x)),
            'steps':len(sol.t),'rhs_evaluations':sol.nfev}


base=integrate(0)
assert abs(base['baryon_radius']-BASE_R)<1e-8
assert abs(base['cold_radius']-BASE_R)<1e-8
assert abs(base['mass_ratio']-F)<1e-8
samples=[integrate(e) for e in [1e-4,1e-3,1e-2]]
result={'claim_id':'VC3-CRITICAL-STIFF-001','exact_checks':len(checks),
        'check_names':checks,'chosen_f':'1341/250',
        'ODE':{'method':'DOP853','rtol':RTOL,'atol':ATOL,
               'central_start':T0,'outer_stop':'2*Maxwell_base_radius',
               'positive_part_sources':True},
        'Maxwell_base_benchmark':base,'nonlinear_samples':samples,
        'interpretation':'Exact fully dynamical critical Maxwell base; analytic positive radial-energy nonlinear Newtonian branch; floating samples are implementation diagnostics, not interval ODE certificates. RTM finite-D0 taper and vacuum embedding remain obstructed.',
        'nonclaims':['No predicted baryonic EOS or abundance.',
                    'No relativistic vacuum action or RTM causal taper.',
                    'No angular or nonlinear free-boundary PDE theorem.',
                    'No interval certification or quantified universal branch threshold.']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'exact_checks':len(checks),'last_sample':samples[-1]}))
