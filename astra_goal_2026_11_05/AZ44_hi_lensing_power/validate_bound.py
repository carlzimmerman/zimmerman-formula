#!/usr/bin/env python3
"""Prove the frozen point-source Fisher bound and test a noise-only SIS mock."""
import hashlib,json,math,os,time
from pathlib import Path
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[name]='1'
import numpy as np
from numpy.polynomial.legendre import leggauss
import sympy as S
start=time.time();here=Path(__file__).resolve().parent;checks=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
r,R,z,GM,a,G=S.symbols('r R z GM a G',positive=True)
g=GM/(2*r*r)+S.sqrt(GM*GM/(4*r**4)+GM*a/r**2)
f=S.simplify(a*S.diff(g,a))
check('law_S_log_derivative',S.simplify(f-GM*a/S.sqrt(GM**2+4*GM*a*r*r))==0)
u=S.symbols('u',nonnegative=True)
ratio=S.simplify(f/(S.sqrt(GM*a)/(2*r)))
ratio2=S.simplify(-S.diff(f,r)/(S.sqrt(GM*a)/(2*r*r)))
check('positive_derivative_upper_bound',S.simplify(ratio.subs(GM,4*a*r*r*u)-(1+u)**(-S.Rational(1,2)))==0)
check('positive_radial_derivative_upper_bound',S.simplify(ratio2.subs(GM,4*a*r*r*u)-(1+u)**(-S.Rational(3,2)))==0)
I4=S.integrate(1/(R*R+z*z)**2,(z,0,S.oo))
I5=S.integrate(1/(R*R+z*z)**S.Rational(5,2),(z,0,S.oo))
check('Newtonian_projection_known_answer',S.simplify(R*R/(2*S.pi*G)*3*GM*I5-GM/(S.pi*G*R*R))==0)
check('deep_MOND_projection_known_answer',S.simplify(R*R/(2*S.pi*G)*2*S.sqrt(GM*a)*I4-S.sqrt(GM*a)/(4*G*R))==0)
check('log_derivative_projected_bound',S.simplify(R*R/(2*S.pi*G)*S.sqrt(GM*a)*I4-S.sqrt(GM*a)/(8*G*R))==0)
# Spin-2 fixture: a shared source receives two arbitrarily oriented templates.
spin=[]
for angle in [0,.3,1.,math.pi/2,math.pi]:
    vec=1+2*np.exp(2j*angle)
    spin.append(float(abs(vec)**2))
check('two_lens_triangle_bound',max(spin)<=9+1e-14,spin)

c=299792.458;sigma_v=100.;sigma_e=.3;theta_min=.03/100;theta_max=1./100
source_density=10*(180*60/math.pi)**2;amplitude=2*math.pi*sigma_v**2/c**2
analytic=100*2*math.pi*source_density*amplitude**2*math.log(theta_max/theta_min)/sigma_e**2
# Log-angle quadrature, independent of the Monte Carlo area sampling.
vals=[]
for order in [128,256]:
    xx,ww=leggauss(order);lo,hi=math.log(theta_min),math.log(theta_max)
    theta=np.exp((lo+hi)/2+(hi-lo)*xx/2)
    vals.append(float(100*source_density*2*math.pi*(hi-lo)/2*np.dot(ww,theta**2*(amplitude/theta)**2)/sigma_e**2))
check('SIS_quadrature_pair',abs(vals[0]/vals[1]-1)<=1e-8,abs(vals[0]/vals[1]-1))
check('SIS_analytic_integral',abs(vals[1]/analytic-1)<=1e-8,abs(vals[1]/analytic-1))
rng=np.random.default_rng(4410);n=int(round(source_density*math.pi*(theta_max**2-theta_min**2)))
fish=[];noise=[]
for lens in range(100):
    rr=np.sqrt(rng.uniform(theta_min**2,theta_max**2,n));ee=rng.normal(0,sigma_e,n)
    fish.append(float(np.sum((amplitude/rr)**2)/sigma_e**2));noise.append(float(np.sum(ee*ee)))
sim=math.fsum(fish)
check('K3_noise_only_SIS_mock',abs(math.sqrt(sim/analytic)-1)<=.1,math.sqrt(sim/analytic))
check('mock_shape_noise',abs(math.sqrt(math.fsum(noise)/(100*n))/sigma_e-1)<=.1)
obj=dict(status='Bound validated only if every check passes; catalogue forecast pending',
 assumptions='Point-baryon law S, ordinary geometry 0<=Dls/Ds<=1, constant component shape-noise variance',
 checks=checks,SIS_analytic_SNR=math.sqrt(analytic),SIS_mock_SNR=math.sqrt(sim),
 sources_per_mock_lens=n,seconds=time.time()-start,
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),here/'FROZEN_CRITERIA.md']})
out=here/'bound_validation.json';tmp=out.with_suffix('.json.tmp')
with tmp.open('w') as stream:json.dump(obj,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
os.replace(tmp,out)
bad=[v['name'] for v in checks if not v['passed']]
print(json.dumps(dict(passed=len(checks)-len(bad),total=len(checks),failed=bad,SNR_ratio=math.sqrt(sim/analytic)),indent=2))
raise SystemExit(bool(bad))
