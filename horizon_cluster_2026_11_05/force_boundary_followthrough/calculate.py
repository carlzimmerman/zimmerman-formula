"""Bounded conditional boundary calculations. Run: python calculate.py.

No input catalog, network, random sampling, or fitted observational errors.
Outputs results.json plus a version-2 computation manifest in this directory.
"""
import datetime
import hashlib
import json
import math
import platform
import subprocess
import sys
import time
import warnings
from pathlib import Path

import scipy
from scipy.integrate import IntegrationWarning, quad, solve_ivp
from scipy.optimize import brentq

warnings.simplefilter('error', IntegrationWarning)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
START = time.perf_counter()
STAMP = datetime.datetime.now(datetime.timezone.utc).isoformat()
INPUTS = [Path(__file__).resolve(), HERE / 'CONTRACT.txt']
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
HASHES = {p: sha(p) for p in INPUTS}
G, C, MS = 6.67430e-11, 299792458., 1.98847e30
MPC, GYR = 3.0856775814913673e22, 365.25 * 86400 * 1e9
LAM = 1.1056e-52
K = LAM * C*C / 3
A0 = C*C * math.sqrt(LAM / (32*math.pi))
TAU = math.sqrt(K) * 13.8 * GYR
CHECKS = []
def check(label, condition, value):
    CHECKS.append({'name': label, 'passed': bool(condition), 'value': value})
    assert condition, (label, value)

def tau_power(x, n, tol=2e-10):
    """r/Rs=x exp(-u^2) regularizes both ends of the orbit-time integral."""
    def f(u):
        z = u*u
        d = z if n == 1 else math.expm1(z)/x
        d -= .5*x*x*(-math.expm1(-2*z))
        return 2*u*x*math.exp(-z)/math.sqrt(2*d)
    return quad(f, 0, 12, epsabs=tol, epsrel=tol)[0]

X = {n: brentq(lambda x: tau_power(x,n)-TAU, .0001,.999,xtol=1e-12)
     for n in [1,2]}
for n in [1,2]:
    small=1e-4
    exact = math.sqrt(math.pi/2)*small if n==1 else math.pi/math.sqrt(8)*small**1.5
    err=abs(tau_power(small,n)/exact-1)
    check('small-radius analytic time n='+str(n),err<1e-7,err)
    diff=abs(tau_power(X[n],n,1e-12)-TAU)
    check('tight quadrature n='+str(n),diff<1e-10,diff)
    # Independent ODE: start at rest at turnaround and fall to a finite radius.
    eps=1e-4
    def event(t,y): return y[0]-eps
    event.terminal=True
    event.direction=-1
    sol=solve_ivp(lambda t,y:[y[1],y[0]-y[0]**(-n)], [0,2], [X[n],0],
                  rtol=1e-10,atol=1e-12,events=event,max_step=.005)
    umax=math.sqrt(math.log(X[n]/eps))
    def f(u):
        z=u*u
        d=(z if n==1 else math.expm1(z)/X[n])-.5*X[n]**2*(-math.expm1(-2*z))
        return 2*u*X[n]*math.exp(-z)/math.sqrt(2*d)
    integral=quad(f,0,umax,epsabs=1e-11)[0]
    error=abs(sol.t_events[0][0]-integral)
    check('ODE vs energy quadrature n='+str(n),error<2e-8,error)

def scales(m):
    gm=G*m*MS
    a=math.sqrt(gm*A0)  # velocity squared
    return gm,a,math.sqrt(a/K),(gm/K)**(1/3)

MASS_ROWS=[]
for m in [6.5e10,1.6e11,1e12,1.5e14]:
    gm,a,rs,rn=scales(m)
    # mu(x)=x/(1+x): at force balance g=Kr, yielding
    # (r/rs)^4 = 1 + (K rs/a0)(r/rs).
    correction=brentq(lambda y:y**4-1-K*rs/A0*y,1,2)
    MASS_ROWS.append({'mass_solar':m,'rM_kpc':math.sqrt(gm/A0)/MPC*1000,
        'isolated_static_Mpc':rs/MPC,'isolated_R0_Mpc':X[1]*rs/MPC,
        'Newton_baryon_static_Mpc':rn/MPC,'Newton_baryon_R0_Mpc':X[2]*rn/MPC,
        'static_internal_over_a0':K*rs/A0,
        'simple_mu_static_Mpc':correction*rs/MPC})

# QUMOND deep external-field radial-force angular mean h=1+K0/3=5/6.
# g_e means PHYSICAL external acceleration. e_N=e^2 only in deep MOND.
H=5/6
gm,a,rs,rn=scales(1.6e11)
EFE=[]
def smooth_time(x,s,tol=2e-10):
    # Potential/A = -asinh(s/x) - x^2/2.
    def f(u):
        z=u*u
        # Exact asinh difference evaluated through log1p and rationalization;
        # subtracting nearly equal asinh values loses accuracy near u=0.
        b=s/x
        h0=math.hypot(1,b)
        h1=math.hypot(1,b*math.exp(z))
        delta=b*math.expm1(z)+b*b*math.expm1(2*z)/(h0+h1)
        d=math.log1p(delta/(b+h0))-.5*x*x*(-math.expm1(-2*z))
        return 2*u*x*math.exp(-z)/math.sqrt(2*d)
    return quad(f,0,12,epsabs=tol,epsrel=tol)[0]

def smooth_solution(e):
    ge=e*A0
    re=H*a/ge
    s=re/rs
    xs=brentq(lambda x:1/(x*math.sqrt(1+(x/s)**2))-x,1e-6,1.0001)
    x0=brentq(lambda x:smooth_time(x,s)-TAU,1e-5,.999*xs,xtol=1e-11)
    return re,s,xs,x0

for e in [.003,.01,.03,.05,.1]:
    ge=e*A0
    re,s,xs,x0=smooth_solution(e)
    tightened=abs(smooth_time(x0,s,1e-12)-TAU)
    check('smooth quadrature e='+str(e),tightened<1e-9,tightened)
    rE=(H*gm/(e*K))**(1/3)
    r0=X[2]*rE
    ratio=(H*gm/e/r0**2)/ge
    EFE.append({'physical_ge_over_a0':e,'static_asymptote_Mpc':rE/MPC,
        'R0_asymptote_Mpc':r0/MPC,'internal_over_external_at_R0':ratio,
        'smooth_static_Mpc':xs*rs/MPC,'smooth_R0_Mpc':x0*rs/MPC,
        'smooth_re_Mpc':re/MPC})

TARGET=.96*MPC
e_fit=H*gm/K*(X[2]/TARGET)**3
e_fit_smooth=brentq(lambda e:smooth_solution(e)[3]*rs-TARGET,.001,.3,xtol=1e-10)
re,s,xs,x0=smooth_solution(e_fit_smooth)
eps=1e-4
def smooth_event(t,y): return y[0]-eps
smooth_event.terminal=True
smooth_event.direction=-1
sol=solve_ivp(lambda t,y:[y[1],y[0]-1/(y[0]*math.sqrt(1+(y[0]/s)**2))],
              [0,2],[x0,0],rtol=1e-10,atol=1e-12,events=smooth_event,max_step=.005)
# The missing time from zero to eps is bounded by eps/speed(eps), since
# the inward speed grows below eps for this monotone potential branch.
d=math.asinh(s/eps)-math.asinh(s/x0)-.5*(x0*x0-eps*eps)
tail_bound=eps/math.sqrt(2*d)
err=abs(TAU-sol.t_events[0][0])
check('smooth ODE vs quadrature with endpoint tail bound',err<tail_bound+1e-8,
      {'difference':err,'tail_bound':tail_bound})
rfitE=TARGET/X[2]
fit_ratio=(H*gm/e_fit/TARGET**2)/(e_fit*A0)
check('fitted EFE asymptote internal/external < .1',fit_ratio<.1,fit_ratio)

# External-field strength needed for isolation at the isolated static radius.
isolation=K*rs/A0

# Finite counterfamily: same deep-MOND galaxy limit and pure-Lambda vacuum.
# g_p=gN+(gdeep-gN) z^p/(1+z^p)-Kr, z=gN/(Kr).
# Only the outer low-acceleration branch is used; the inner Newtonian
# interpolation can be supplied identically to every member.
COUNTER=[]
for p in [0,1,2,4]:
    vals=[]
    for m in [1e10,1e11,1e12,1e13,1e14]:
        gmm,aa,rss,rnn=scales(m)
        def force(logr):
            r=math.exp(logr);gn=gmm/r**2;gd=aa/r;z=gn/(K*r)
            w=1 if p==0 else z**p/(1+z**p)
            return gn+(gd-gn)*w-K*r
        r=math.exp(brentq(force,math.log(rnn),math.log(2*rss)))
        vals.append(r/MPC)
    slope=math.log(vals[-1]/vals[0])/math.log(1e4)
    COUNTER.append({'p':p,'mass_range_solar':[1e10,1e14],
                    'radii_Mpc':vals,'finite_log_slope':slope,
                    'asymptotic_slope':(p+.5)/(3*p+2)})
check('counterfamily gives different outer radii',COUNTER[1]['radii_Mpc'][1]<COUNTER[0]['radii_Mpc'][1],
      [r['radii_Mpc'][1] for r in COUNTER])

# a0 is invisible in Rs(v_flat), but not in Rs(M_b): do not infer its coefficient
# by substituting a mass inferred from the same rotation speed.
v=200e3
blind=[]
for factor in [.1,1,10]:
    aa0=factor*A0;m=v**4/(G*aa0)
    blind.append((G*m*aa0)**.25/math.sqrt(K)/MPC)
check('a0 cancels at fixed rotation speed',max(blind)-min(blind)<1e-12,blind)

RESULT={'constants':{'G':G,'c':C,'Lambda':LAM,'a0_assumed_relation':A0,'age_Gyr':13.8,
          'tau':TAU,'X_MOND':X[1],'X_Newton':X[2]},'mass_rows':MASS_ROWS,
    'EFE_rows':EFE,'Local_Group_illustration':{'mass_solar':1.6e11,'benchmark_R0_Mpc':.96,
       'isolated_external_threshold_over_a0':isolation,'fitted_e_asymptote':e_fit,
       'fitted_e_smooth':e_fit_smooth,'fit_internal_over_external':fit_ratio,
       'fitted_e_axis_range':[e_fit*.75/H,e_fit/H]},
    'counterfamily':COUNTER,'checks':CHECKS}
RESULT['age_mass_sensitivity']=[]
for age in [10.,13.8,17.]:
    xn=brentq(lambda x:tau_power(x,2)-math.sqrt(K)*age*GYR,.0001,.999)
    for m in [.7e11,1.6e11,2e11]:
        e=H*G*m*MS/K*(xn/TARGET)**3
        RESULT['age_mass_sensitivity'].append({'age_Gyr':age,'mass_solar':m,
            'fitted_e_asymptote':e})
OUT=HERE/'results.json'
OUT.write_text(json.dumps(RESULT,indent=2)+'\n')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
dirty=bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip())
manifest={'schema_version':2,'claim_id':'HB-2026-11-05','repository':{'commit':commit,'dirty':dirty},
 'command':['python',str(Path(__file__).resolve())],
 'environment':{'software':[{'name':'Python','version':platform.python_version()},
                           {'name':'SciPy','version':scipy.__version__}], 'hardware':platform.platform()},
 'mathematics':{'assertion_tested':'Conditional time integrals, external-field asymptotes and nonunique boundary family',
 'coefficient_domain':'positive real inputs; double precision evaluation',
 'conventions':'SI; physical external field; inward attraction positive; fixed masses and Lambda',
 'inputs':[{'Lambda':LAM,'age_Gyr':13.8,'a0':A0}],
 'bounds':{'mass_rows':4,'external_fields':5,'counterfamily_models':4,'counterfamily_masses':5},
 'non_claims':['No full cosmological evolution or QUMOND PDE simulation','No coefficient derivation or independent external-field measurement']},
 'randomness':{'used':False,'generator':'','seed':None},
 'run':{'started_at':STAMP,'runtime_seconds':time.perf_counter()-START,'exit_status':0,'status':'completed',
 'resource_limits':{'memory_bytes':None,'cpu_seconds':None,'max_cores':None,'max_threads':None}},
 'outputs':[{'path':str(OUT.relative_to(ROOT)),'sha256':sha(OUT),'kind':'result'}],
 'checks':CHECKS,'result':'Conditional finite results verified; uniqueness refuted within phenomenological premises',
 'residual_risks':['External-field history unspecified','Spherical point-mass approximation','No interval arithmetic'],
 'input_artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':HASHES[p],'sha256_after':sha(p)} for p in INPUTS],
 'declared_results':[str(OUT.relative_to(ROOT))]}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(RESULT,indent=2))
