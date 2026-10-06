"""Exact identities and bounded independent numerical checks. No covariant health claim."""
import hashlib, json, platform, subprocess, sys
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sp
mp.mp.dps=50
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
RESULT_NAME='manifest.json'
if len(sys.argv)>1:
    OUT=ROOT/sys.argv[1]
    RESULT_NAME='scientific_results.json'
T=mp.mpf('128.9153707043'); Y=mp.mpf(1000); eps=mp.mpf(280)/(3*Y**2)*mp.mpf('0.01')
checks={}
def check(n,b):
    checks[n]=bool(b)
    print(('PASS ' if b else 'FAIL ')+n)
def response(y, bump=False):
    s=mp.sqrt(1+1/y); a=1/(y*(s+1)); q=(y/T)**2
    e=a/(1+q); ep=-1/(2*y*y*s*(1+q))-a*2*y/T**2/(1+q)**2
    if bump and Y<y<2*Y:
        t=(y-Y)/Y
        e+=int(bump)*eps*t**3*(1-t)**3
        ep+=int(bump)*eps/Y*3*t**2*(1-t)**2*(1-2*t)
    return e,ep
# Exact algebra independent of numerical response.
y=sp.symbols('y',positive=True); e=sp.Function('e')(y)
x=y*(1+2*e); z=x*x; m=e/(1+2*e); D=sp.diff(x,y)
check('primitive identity J-I is boundary derivative',sp.simplify(m*sp.diff(z,y)-2*y*e-sp.diff(2*y*y*e*e,y))==0)
Mzz=sp.diff(m,y)/sp.diff(z,y)
check('difference Hessian radial eigenvalue 2/D',sp.simplify(2*(1-2*m-4*z*Mzz)-2/D)==0)
check('difference Hessian transverse eigenvalue 2/(1+2e)',sp.simplify(2*(1-2*m)-2/(1+2*e))==0)
t=sp.symbols('t',real=True)
check('bump integral exact 3/280',sp.integrate((1+t)*t**3*(1-t)**3,(t,0,1))==sp.Rational(3,280))
check('C2 endpoints',all(sp.diff(t**3*(1-t)**3,t,k).subs(t,b)==0 for k in range(3) for b in (0,1)))
# Analytic global positivity certificates: T>=sqrt(8), epsilon bound.
check('global D certificate baseline >=1/2',T*T>=8)
check('global perturbed D certificate >=1/2-25eps/32 >0',mp.mpf('.5')-25*eps/32>0)
a2=1/(2*Y*(mp.sqrt(1+1/(2*Y))+1))
monotone_bound=a2*(2*Y/T**2)/(1+(2*Y/T)**2)**2
check('global bump monotonicity certificate',monotone_bound>3*eps/(16*Y))
check('negative bump retains positive excess',a2/(1+(2*Y/T)**2)>eps/64)
segments=[mp.mpf(0),mp.mpf('.001'),1,10,100,Y,2*Y,mp.inf]
def integrate(fn): return mp.fsum(mp.quad(fn,[a,b]) for a,b in zip(segments[:-1],segments[1:]))
values={}
for bump in (False,True,-1):
    C=integrate(lambda y:y*response(y,bump)[0])
    J=integrate(lambda y:2*y*response(y,bump)[0]*(1+2*response(y,bump)[0]+2*y*response(y,bump)[1]))
    S=integrate(lambda y:-y*y*response(y,bump)[1]/2)
    values[{-1:'negative',0:'base',1:'bump'}[int(bump)]]={'C':str(C),'J_over_2':str(J/2),'epicycle_sum_C':str(S)}
    check('J/2=C '+str(bump),abs(J/2-C)<mp.mpf('1e-35'))
    check('exact epicycle sum rule '+str(bump),abs(S-C)<mp.mpf('1e-35'))
check('delta C=.01',abs(mp.mpf(values['bump']['C'])-mp.mpf(values['base']['C'])-mp.mpf('.01'))<mp.mpf('1e-35'))
check('target base root precision',abs(mp.mpf(values['base']['C'])-32*mp.pi)<mp.mpf('1e-10'))
check('negative bump delta C=-.01',abs(mp.mpf(values['negative']['C'])-mp.mpf(values['base']['C'])+mp.mpf('.01'))<mp.mpf('1e-35'))
check('control doubled integral normalization rejected',abs(mp.mpf(values['base']['J_over_2'])*2-mp.mpf(values['base']['C']))>100)
check('control wrong radial Hessian sign rejected',sp.simplify(2*(1-2*m+4*z*Mzz)-2/D)!=0)
windows=[(0,10),(10,100),(100,1000),(1000,mp.inf)]
values['epicycle_windows']=[{'y_min':str(lo),'y_max':str(hi),'C_lower_bound_contribution':str(mp.quad(lambda yy:-yy**2*response(yy)[1]/2,[lo,hi]))} for lo,hi in windows]
check('window contributions sum to C',abs(mp.fsum(mp.mpf(w['C_lower_bound_contribution']) for w in values['epicycle_windows'])-mp.mpf(values['base']['C']))<mp.mpf('1e-35'))
# Orthogonal full six-component Hessian reconstruction, directions include arbitrary rotations.
rng=np.random.default_rng(73519); maxerr=0.; minval=float('inf')
for yy in np.logspace(-8,8,161):
  for bump in (False,True):
    ee,ep=map(float,response(mp.mpf(str(yy)),bump)); xx=yy*(1+2*ee); dd=1+2*ee+2*yy*ep
    mm=ee/(1+2*ee); mmz=ep/((1+2*ee)**2*2*xx*dd)
    direction=rng.normal(size=3); direction/=np.linalg.norm(direction); vstar=xx*direction
    block=2*mm*np.eye(3)+4*mmz*np.outer(vstar,vstar)
    H=np.block([[2*np.eye(3)-block,block],[block,2*np.eye(3)-block]])
    eig=np.linalg.eigvalsh(H); expected=np.sort([2,2,2,2/(1+2*ee),2/(1+2*ee),2/dd])
    maxerr=max(maxerr,float(np.max(abs(eig-expected)))); minval=min(minval,float(eig.min()))
check('6D Hessian eigenvalues independent reconstruction',maxerr<1e-8 and minval>0)
# Exact small radial oscillations in isolated spherical Newtonian metric limit.
for yy in (1,10,100,float(T),1000,1e5):
    ee,ep=response(mp.mpf(str(yy))); h=-2*yy*ep/(1+ee); ratio=mp.sqrt(1+h)
    values['orbit_'+str(yy)]={'kappa_over_Omega':str(ratio),'apsidal_radians_per_radial_cycle':str(2*mp.pi*(1/ratio-1)),'excess_g_over_a0':str(yy*ee)}
inputs=['sol61_push/vacuum_offset_selection.py','sonnet55_push/puzzle_32pi/p38_high_accel_turnoff.py','citations/works/milgrom-2009-bimetric-mond-gravity.md','sol61_push/puzzle_32pi/README.md','sol61_push/puzzle_32pi/closure_checks.py','sonnet55_push/puzzle_32pi/README.md','sonnet55_push/puzzle_32pi/p25_symmetric_bimond_map.py','sonnet55_push/puzzle_32pi/p44_samplesize_and_bayes.py','sonnet55_push/puzzle_32pi/p45_vacuum_closed_form.py','sonnet55_push/puzzle_32pi/p46_gas_points_trgb.py','fable_independent_2026/lean_2026/PUZZLE_32pi_postulate_status_2026_10_05.lean']
manifest={'checkpoint':'SOL61-32PI-BREAKTHROUGH-2026-10-05','shared_base':'a36191815030afddf1277d413f488fb0c3ac520f','head_at_run':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'sympy':sp.__version__,'mpmath':mp.__version__,'command':'python3 sol61_push/puzzle_32pi/breakthrough_2026_10_05/checks.py','seed':73519,'precision_digits':50,'hessian_grid':{'y_min':1e-8,'y_max':1e8,'points':161,'kernels':2},'checks':checks,'numeric_values':values,'hessian_max_error':maxerr,'sampled_min_eigenvalue':minval,'T':str(T),'Y':str(Y),'epsilon':str(eps),'monotone_base_lower_bound':str(monotone_bound),'monotone_bump_upper_bound':str(3*eps/(16*Y)),'scope':'Analytic proof in report; finite checks corroborate. Degenerate MOND Hessian at zero difference field; covariant health not proved.'}
(OUT/RESULT_NAME).write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(values,indent=2)); sys.exit(0 if all(checks.values()) else 1)
