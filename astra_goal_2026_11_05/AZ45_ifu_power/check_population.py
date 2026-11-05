#!/usr/bin/env python3
"""Independent analytic checks for the frozen equal-third population forecast."""
import hashlib,json,math,platform
from pathlib import Path
import numpy as np
import population as P
checks=[]
def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
z=np.array([.6,1.,1.4]);n=12
# Exact OLS coefficients independently solve the normal equations.
X=np.column_stack([np.ones(3),z]);coeff=np.linalg.solve(X.T@X,X.T)[1]
y=np.array([[-.3,.2,.7],[.1,.1,.1]])
check('OLS_exact_slope',np.allclose(P.slope(y),y@coeff,atol=1e-14,rtol=0))
var=np.array([[.04,.09,.16]])
expected=float(np.sum(coeff**2*var[0]/n))
check('analytic_slope_variance',abs(float(P.slope_variance(var,n)[0])-expected)<1e-14,expected)
rng=np.random.default_rng(2026110545);m=16384
means=.6*(z-1)+rng.normal(size=(m,3))*np.sqrt(var/n)
cover=float(np.mean(abs(P.slope(means)-.6)<=1.959963984540054*math.sqrt(expected)))
bound=3*math.sqrt(.95*.05/m)
check('Gaussian_95_coverage',abs(cover-.95)<=bound,dict(coverage=cover,tolerance=bound))
# Draw indices from the actual resampler; exact template balance is mandatory.
a=np.arange(36,dtype=float).reshape(3,4,3)/100
small=P.resample(a,36,512,[20261105,4500,30,36,0,0])
large=P.resample(a,36,1024,[20261105,4500,30,36,0,0])
check('identical_prefix',all(np.array_equal(x,y[:512]) for x,y in zip(small,large)))
constant=np.broadcast_to((.6*(z-1))[:,None,None],(3,4,3)).copy()
s,v=P.resample(constant,72,32,[1,2,3])
check('zero_scatter_exact_slope',np.allclose(s,.6,atol=1e-14,rtol=0))
check('zero_scatter_variance',np.allclose(v,0,atol=1e-28,rtol=0))
lo,hi=P.wilson(0,1024);check('zero_success_Wilson',lo==0 and 0<hi<.004)
lo,hi=P.wilson(1024,1024);check('all_success_Wilson',hi==1 and .996<lo<1)
check('systematic_floor_detection',not np.any(P.detect(np.array([.6]),np.array([0.]),.20)))
# Unequal template offsets must retain exact four-template balance in every draw.
balanced=np.repeat(np.arange(12,dtype=float).reshape(3,4,1),3,axis=2)
bs,bv=P.resample(balanced,144,64,[45,1])
check('four_templates_exact_balance',np.allclose(bs,P.slope(balanced.mean(axis=(1,2))),atol=1e-14,rtol=0))
flat=np.zeros((3,4,3));rr=P.rates(flat,constant,36,30,0,0)
check('power_fixture_all_floors',[r['rungs'][1]['power_gate'] for r in rr]==[True,True,False])
check('power_fixture_convergence',all(r['converged'] for r in rr))
try:
    P.resample(np.zeros((3,4,2)),36,512,[1])
    rejected=False
except ValueError:rejected=True
check('missing_replicate_rejected',rejected)
obj=dict(source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(P.__file__)]},versions=dict(python=platform.python_version(),numpy=np.__version__),checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),scope='Statistical machinery only; no nonlinear-population verdict')
Path(__file__).with_name('population_checks.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
