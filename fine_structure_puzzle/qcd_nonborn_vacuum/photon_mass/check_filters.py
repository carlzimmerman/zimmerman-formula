"""Analytic photon-mass derivative filters; no fitted mass/Q2 curve."""
from pathlib import Path
import json
import sys
import mpmath as mp
import sympy as sp

BASE=Path(__file__).resolve().parent
cfg=json.loads((BASE/'INPUTS.json').read_text())
mp.mp.dps=cfg['decimal_digits']
checks=[]

def check(name,ok):
    if not ok:
        raise AssertionError(name)
    checks.append(name)

s,t,T,C=sp.symbols('s t T C',positive=True)
D=lambda f: s*sp.diff(f,s)
def apply_roots(f,roots):
    for root in roots:
        f=sp.expand(D(f)-root*f)
    return sp.simplify(f)
roots3=[0,1,2]
roots5=[0,sp.Rational(1,2),1,sp.Rational(3,2),2]
f=sp.Function('f')(s)
p3=apply_roots(f,roots3)
p5=apply_roots(f,roots5)
check('P3 ordinary derivative form',sp.simplify(p3-s**3*sp.diff(f,s,3))==0)
check('P5 ordinary derivative form',sp.simplify(p5-(sp.Rational(15,4)*s**3*sp.diff(f,s,3)+5*s**4*sp.diff(f,s,4)+s**5*sp.diff(f,s,5)))==0)
for n in roots5:
    check('P5 kills s power '+str(n),apply_roots(s**n,roots5)==0)
check('P5 logarithm normalization',sp.simplify(apply_roots(s**2*sp.log(s),roots5)-sp.Rational(3,2)*s**2)==0)
prop=t/(t+s)
w5=-15*t*s*(3*t-s)*(t-3*s)/(2*(t+s)**6)
check('P5 exact propagator kernel',sp.simplify(apply_roots(prop,roots5)/s**2-w5)==0)
check('P3 exact propagator derivative',sp.simplify(sp.diff(prop,s,3)+6*t/(t+s)**4)==0)
flocal=C*(T**2-2*s*T+2*s**2*sp.log((T+s)/s))
y=T/(T+s)
check('local G3 exact cutoff factor',sp.simplify(-s*sp.diff(flocal,s,3)/(4*C)-y**3)==0)
F5=16*y**5-20*y**4+5*y**3
check('local P5 exact cutoff factor',sp.simplify(-apply_roots(flocal,roots5)/(3*s**2*C)-F5)==0)
check('contact tadpole is not annihilated',sp.simplify(-s*sp.diff(s**2*(sp.log(s)-1)/(16*sp.pi**2),s,3)/4+1/(32*sp.pi**2))==0)
for n in (0,2):
    integ=lambda p: sp.gamma(sp.Rational(p+1,2))*sp.gamma(6-sp.Rational(p+1,2))/(2*sp.gamma(6))
    check('Dirac removed polynomial moment '+str(n),sp.simplify(3*integ(6+n)-10*integ(4+n)+3*integ(2+n))==0)

# Independent coordinate derivative of the 4D scalar propagator.
coordinate=[]
for rr,ss in cfg['coordinate_kernel_tests']:
    r,q=mp.mpf(rr),mp.mpf(ss)
    direct=mp.diff(lambda a: mp.sqrt(a)*mp.besselk(1,mp.sqrt(a)*r)/(4*mp.pi**2*r),q,3)
    bessel=-r*r*mp.besselk(2,mp.sqrt(q)*r)/(32*mp.pi**2*q)
    err=abs(direct-bessel)
    check('coordinate Bessel kernel '+rr+','+ss,err<mp.mpf('1e-48'))
    coordinate.append({'r':rr,'s':ss,'absolute_difference':mp.nstr(err,30)})

# Check exact positive cutoff remainder integral, independent of local mass.
for ss in ['0.01','0.1','0.7']:
    q=mp.mpf(ss); top=mp.mpf('0.25'); yy=top/(top+q)
    numerical=mp.quad(lambda a:a**3/(a+q)**4,[0,top])
    analytic=mp.log(1+top/q)-yy-yy**2/2-yy**3/3
    check('remainder integral '+ss,abs(numerical-analytic)<mp.mpf('1e-48'))

# Source complete strict leading HB piN amplitudes, copied explicitly from
# the frozen finite-band source implementation; no import runs old code.
def amplitudes(r,x):
    tt=r*r; h=1-x*x; v=tt*h; w=-tt*x*x; k=-tt
    H=mp.sqrt(1-w); den=4*v+k*k
    I=mp.atan(r/(2*mp.sqrt(h)))+mp.atan(r*(1-2*x*x)/(2*mp.sqrt(h)*H))
    J=I/mp.sqrt(v)
    B1=mp.mpf(3)/2+1/v-(1+1/v)*H-(2+k/v)*J/2
    B2=-(mp.mpf(3)/2+(mp.mpf(1)/2+1/k+1/w)*k/v)-(w*k/den)*(1/v-k/(2*v))+(2-(v/w)*(1-w)+k*w/den)*H/v+(2+3*k/v+k)*J/2
    return B1,(k/v)*B2

nodes_cache={}
angles_cache={}
def nodes(n):
    if n not in nodes_cache:
        nodes_cache[n]=mp.gauss_quadrature(n,'legendre')
        absc,weights=nodes_cache[n]
        angles_cache[n]=[(mp.sin(mp.pi*(absc[j]+1)/4),mp.cos(mp.pi*(absc[j]+1)/4)**2,weights[j]*mp.pi/2) for j in range(n)]
    return nodes_cache[n]

def angular_ratio(tt,n):
    r=mp.sqrt(tt)
    acc=mp.mpf('0')
    for xx,h,weight in angles_cache[n]:
        b1,b2=amplitudes(r,xx)
        acc+=weight*h*(-3*b1+h*b2)
    return acc/(9*mp.pi*tt/32)

def hb_filters(lam,n):
    absc,weights=nodes(n)
    sig=lam*lam; top=mp.mpf(cfg['hb_ball_Qmax_over_mpi'])**2
    vmax=mp.log(1+top/sig)
    third=fifth=mp.mpf('0')
    for j in range(n):
        vv=vmax*(absc[j]+1)/2
        yy=-mp.expm1(-vv)
        tt=sig*mp.expm1(vv)
        ratio=angular_ratio(tt,n)
        base=weights[j]*mp.exp(-vv)*yy**2*ratio*vmax/2
        third+=3*base
        fifth+=5*base*(4*yy-1)*(4*yy-3)
    return third,fifth

p={k:mp.mpf(v) for k,v in cfg['source_parameter_decimals'].items()}
CHB=9*p['gA']**2/(8192*mp.pi**3*p['M_GeV']*p['fpi_GeV']**2*p['mpi_GeV'])
hb=[]
for raw in cfg['hb_lambda_over_mpi']:
    lam=mp.mpf(raw)
    vals=[hb_filters(lam,n) for n in cfg['hb_quadrature_orders']]
    errors=[abs(vals[-1][j]-vals[-2][j]) for j in (0,1)]
    check('HB nested quadrature '+raw,max(errors)<mp.mpf(cfg['hb_relative_convergence_tolerance']))
    yy=mp.mpf(cfg['hb_ball_Qmax_over_mpi'])**2/(mp.mpf(cfg['hb_ball_Qmax_over_mpi'])**2+lam**2)
    local3=yy**3;local5=16*yy**5-20*yy**4+5*yy**3
    hb.append({'lambda_over_mpi':raw,'G3_over_CHB':mp.nstr(vals[-1][0],45),'minusP5_over_3s2CHB':mp.nstr(vals[-1][1],45),'local_exact_cutoff_G3':mp.nstr(local3,45),'local_exact_cutoff_P5':mp.nstr(local5,45),'full_shape_minus_local_G3':mp.nstr(vals[-1][0]-local3,35),'full_shape_minus_local_P5':mp.nstr(vals[-1][1]-local5,35),'last_quadrature_absolute_changes':[mp.nstr(a,25) for a in errors],'G3_GeV^-4':mp.nstr(CHB*vals[-1][0],45)})
check('HB third filter approaches known soft coefficient',abs(mp.mpf(hb[-1]['G3_over_CHB'])-1)<mp.mpf('0.001'))
check('HB fifth filter approaches known soft coefficient',abs(mp.mpf(hb[-1]['minusP5_over_3s2CHB'])-1)<mp.mpf('0.002'))

# Independent all-momentum point-Dirac test. Set M=1; s=(lambda/M)^2.
def BD(z):
    root=mp.sqrt(1+z*z)
    return (root+2*z)/(root+z)**2

def dirac_radial(lam):
    # P5 integrals of B=1 and B=c z^2 vanish exactly; remove them to
    # avoid cancellation of the s^(1/2),s^(3/2) pieces numerically.
    def fun(v):
        z=lam*v/2
        rem=BD(z)-1+mp.mpf(3)*z*z/2
        return rem*v*v*(3*v*v-1)*(v*v-3)/(1+v*v)**6
    return -15*mp.quad(fun,[0,1,4,1/lam,mp.inf])/(8*mp.pi**2*lam**3)

def dirac_FP(lam):
    q=lam*lam
    def fun(x):
        om=1-x;den=x*x+om*q
        return (1+x)*(-mp.mpf(15)/2*q*om**3/den**3+30*q*q*om**4/den**4-24*q**3*om**5/den**5)/(8*mp.pi**2)
    points=sorted({mp.mpf('0'),lam,min(10*lam,mp.mpf('0.5')),mp.mpf('0.5'),mp.mpf('1')})
    return mp.quad(fun,points)

dirac=[]
target=-3/(64*mp.pi**2)
for raw in cfg['dirac_lambda_over_M']:
    lam=mp.mpf(raw)
    rad=dirac_radial(lam);fp=dirac_FP(lam)
    error=abs(rad-fp)
    check('Dirac radial vs Feynman parameters '+raw,error<mp.mpf(cfg['dirac_independent_integral_tolerance']))
    estimate=-1/(64*mp.pi**2)-rad/3
    dirac.append({'lambda_over_M':raw,'L5_radial':mp.nstr(rad,45),'L5_FP':mp.nstr(fp,45),'absolute_difference':mp.nstr(error,30),'ratio_to_expected_log_limit':mp.nstr(rad/target,35),'inferred_NB_C_times_M4':mp.nstr(estimate,35)})
check('Dirac log limit recovered',abs(mp.mpf(dirac[-1]['ratio_to_expected_log_limit'])-1)<mp.mpf('0.01'))

result={'assertion_tested':'IR logarithm/filter identities; full HBpiN finite-ball filters; independent all-momentum Dirac P5 benchmark','number_checks':len(checks),'checks':checks,'coordinate_checks':coordinate,'CHB_GeV^-4':mp.nstr(CHB,45),'HB_filters':hb,'Dirac_expected_L5':mp.nstr(target,45),'Dirac_filters':dirac,'limitations':cfg['excluded'],'calibration_caveat':cfg['calibration_caveat']}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'CHB_GeV^-4':result['CHB_GeV^-4'],'HB_filters':hb,'Dirac_filters':dirac},indent=2))
