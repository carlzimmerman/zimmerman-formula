#!/usr/bin/env python3
"""FSP-008 exact Born identities and bounded, alpha-free Dirac kernels."""
import json
import sys
from pathlib import Path
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
INPUTS = json.loads((HERE / 'INPUTS.json').read_text())
OUT = Path(sys.argv[1])

z = sp.symbols('z', positive=True)
f1, f2, a, b, kappa = sp.symbols('f1 f2 a b kappa', real=True)
s = sp.sqrt(1 + z*z)
ge = f1-z*z*f2
gm = f1+f2
aa = f1*f1+z*z*f2*f2
cc = (1+z*z)*aa-3*z*z*gm*gm
born = z*(3*f1*f1-aa)/2+cc*(s-z)
checks = []

def exact(name, expr):
    val = sp.simplify(expr)
    if val != 0:
        raise AssertionError((name, str(val)))
    checks.append(name)

exact('Sachs invariant A', aa-(ge*ge+z*z*gm*gm)/(1+z*z))
elastic = 3*z*gm*gm/(2*(1+z*z)) + (ge*ge-2*z*z*gm*gm)/(1+z*z)*((1+z*z)**sp.Rational(3,2)-z**3-sp.Rational(3,2)*z)
exact('WLCM elastic plus Born subtraction', born-elastic+sp.Rational(3,2)*z*(gm*gm-f1*f1))
i0 = sp.pi*(s/z-1)
i2 = sp.pi/2-z*z*i0
trace_integral = 3*sp.pi*f1*f1-6*z*z*gm*gm*i0+2*aa*(i0-i2)
exact('T1 T2 angular trace', born-z*trace_integral/(2*sp.pi))
fd = 2*z**3+(1-2*z*z)*s
stable = (s+2*z)/(s+z)**2
exact('point Dirac Born specialization', born.subs({f1:1,f2:0})-fd)
exact('stable Dirac expression', fd-stable)
primitive = (2*z**4+z*(1-2*z*z)*s+3*sp.asinh(z))/4
exact('exact shell primitive', sp.diff(primitive,z)-fd)
point_tensor_trace = 6+(-6*z*z+2*(1-sp.Symbol('x')**2))/(z*z+sp.Symbol('x')**2)
exact('independent Dirac numerator trace',point_tensor_trace-2*(1+2*sp.Symbol('x')**2)/(z*z+sp.Symbol('x')**2))
series = sp.series(born.subs({f1:1+a*z*z, f2:kappa+b*z*z}),z,0,4).removeO().expand()
c = -sp.Rational(3,2)-6*kappa-2*kappa*kappa+2*a
d = 2+6*kappa+sp.Rational(3,2)*kappa*kappa
exact('soft expansion coefficients including vanishing linear term',series-(1+c*z*z+d*z**3))
rex = sp.symbols('m2_rE2', real=True)
# GE=1-(2/3)m^2 r_E^2 z^2, hence a=kappa-(2/3)m^2 r_E^2.
exact('Sachs-radius conversion', c.subs(a,kappa-sp.Rational(2,3)*rex)-(-sp.Rational(3,2)-4*kappa-2*kappa*kappa-sp.Rational(4,3)*rex))
exact('UV logarithmic coefficient',sp.limit(z*fd,z,sp.oo)-sp.Rational(3,4))
exact('sharp-cutoff finite constant',sp.limit(primitive-sp.Rational(3,4)*sp.log(2*z),z,sp.oo)-sp.Rational(3,16))
q2, lam2 = sp.symbols('q2 lam2',positive=True)
pv = 1-2*q2/(q2+lam2/2)+q2/(q2+lam2)
exact('doubly PV multiplier', pv-lam2**2/(2*(q2+lam2/2)*(q2+lam2)))
x=sp.symbols('x',positive=True)
p = 1/(2*(x+sp.Rational(1,2))*(x+1))
anti = sp.log(x)-2*sp.log(x+sp.Rational(1,2))+sp.log(x+1)
exact('PV logarithmic moment primitive',sp.diff(anti,x)-p/x)
exact('PV versus sharp logarithmic moment',sp.limit((-anti+sp.log(x))/2,x,0)+sp.log(2))

mp.mp.dps=INPUTS['precision_digits']
def bdir(t):
    st=mp.sqrt(1+t*t)
    return (st+2*t)/(st+t)**2
def ppv(t, lam):
    return lam**4/(2*(4*t*t+lam*lam/2)*(4*t*t+lam*lam))
def prim(t):
    return (2*t**4+t*(1-2*t*t)*mp.sqrt(1+t*t)+3*mp.asinh(t))/4
def fmt(x):
    return mp.nstr(x, INPUTS['saved_digits'])
numerical=[]
max_angle=mp.mpf(0)
for zz in INPUTS['angular_z_grid']:
    zz=mp.mpf(zz)
    for p1,p2 in INPUTS['form_factor_test_pairs']:
        p1,p2=mp.mpf(p1),mp.mpf(p2)
        av=p1*p1+zz*zz*p2*p2
        gmv=p1+p2
        tr=lambda xx: mp.sqrt(1-xx*xx)*(6*p1*p1+(-6*zz*zz*gmv*gmv+2*(1-xx*xx)*av)/(zz*zz+xx*xx))
        # Symmetry and an explicit split resolve the narrow forward feature.
        angular=2*mp.quad(tr,[0,min(zz,mp.mpf('0.5')),1])
        bv=zz*(3*p1*p1-av)/2+((1+zz*zz)*av-3*zz*zz*gmv*gmv)/(mp.sqrt(1+zz*zz)+zz)
        err=abs(zz*angular/(2*mp.pi)-bv)
        max_angle=max(max_angle,err)
        assert err<mp.mpf(INPUTS['angular_absolute_tolerance'])
        numerical.append({'z':fmt(zz),'F1':fmt(p1),'F2':fmt(p2),'absolute_error':fmt(err)})

shells=[]
for qa,qb in INPUTS['sharp_shell_Q_over_m']:
    za,zb=mp.mpf(qa)/2,mp.mpf(qb)/2
    integ=mp.quad(bdir,[za,zb])/(2*mp.pi**2)
    closed=(prim(zb)-prim(za))/(2*mp.pi**2)
    err=abs(integ-closed)
    assert err<mp.mpf(INPUTS['shell_absolute_tolerance'])
    shells.append({'Q_min_over_m':qa,'Q_max_over_m':qb,'M_u_over_m':fmt(integ),'closed_form_absolute_error':fmt(err)})

pv_results=[]
max_pv=mp.mpf(0)
uv_constant=(mp.mpf('1.5')-6*mp.log(2))/(16*mp.pi**2)
for raw in INPUTS['PV_Lambda_over_m']:
    ll=mp.mpf(raw)
    integrand=lambda zz:bdir(zz)*ppv(zz,ll)
    # First quadrature uses z over the entire positive line.
    dz=mp.quad(integrand,[0,1,ll,mp.inf])/(2*mp.pi**2)
    # Orthogonal change of variable z=t/(1-t), on the compact interval.
    # Endpoint values are zero at t=1 (the integrand falls as z^-5).
    def compact(t):
        if t==1: return mp.mpf(0)
        zz=t/(1-t)
        return integrand(zz)/(1-t)**2
    dt=mp.quad(compact,[0,mp.mpf('.5'),ll/(1+ll),1])/(2*mp.pi**2)
    err=abs(dz-dt)
    assert err<mp.mpf(INPUTS['PV_absolute_tolerance'])
    max_pv=max(max_pv,err)
    residual=dz-3*mp.log(ll*ll)/(16*mp.pi**2)
    pv_results.append({'Lambda_over_m':raw,'M_u_over_m':fmt(dz),'second_variable_absolute_error':fmt(err),'UV_subtracted':fmt(residual),'difference_from_proved_asymptotic_constant':fmt(residual-uv_constant)})

phi=(1+mp.sqrt(5))/2
special=(1+mp.sqrt(5))/(64*mp.pi**2)+3*mp.log(phi)/(8*mp.pi**2)
assert abs(special-mp.mpf(shells[1]['M_u_over_m']))<mp.mpf('1e-40')
res={
 'schema':'fsp008.proton_kernel.results.v1',
 'assertion_tested':'Exact symbolic Born identities plus specified finite quadrature grid; no physical QCD tensor integrated.',
 'coupling':'u=e^2, alpha=u/(4*pi); no numerical alpha input',
 'symbolic_checks':checks,
 'symbolic_check_count':len(checks),
 'physical_proton_IR_limit_per_u':'1/(4*pi^2)',
 'physical_proton_IR_limit_per_u_numeric':fmt(1/(4*mp.pi**2)),
 'point_Dirac_0_to_m_exact':'(1+sqrt(5))/(64*pi^2)+3*log((1+sqrt(5))/2)/(8*pi^2)',
 'point_Dirac_0_to_m_numeric':fmt(special),
 'point_Dirac_PV_UV_constant_exact':'(3/2-6*log(2))/(16*pi^2)',
 'point_Dirac_PV_UV_constant_numeric':fmt(uv_constant),
 'angular_checks':numerical,'angular_check_count':len(numerical),'max_angular_absolute_error':fmt(max_angle),
 'sharp_shell_results':shells,'PV_results':pv_results,'max_PV_absolute_error':fmt(max_pv),
 'limitations':['mpmath comparisons are not interval-certified error bounds.','No physical-proton all-momentum form factors or non-Born data are imported.','Point-Dirac PV results exclude finite renormalization/matching counterterms.','No global curved-space QCD vacuum response or alpha prediction is calculated.']
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'symbolic_checks':len(checks),'angular_checks':len(numerical),'sharp_shells':len(shells),'PV_integrals':len(pv_results),'point_Dirac_0_to_m':fmt(special),'max_angular_error':fmt(max_angle),'max_PV_difference':fmt(max_pv)},indent=2))
