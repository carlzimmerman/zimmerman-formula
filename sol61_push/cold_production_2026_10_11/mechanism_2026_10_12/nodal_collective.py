"""Isotropic gapless ring ensemble: slow mode and perturbative damping."""
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
P=Path(__file__).parent
checks={};orientation=[];modes=[]
def F(x):
    # Real positive frequency 0<x<1, retarded convention exp(-i omega*t).
    return complex(math.pi*(1-x*x)/4,-(x-(1-x*x)*np.arctanh(x))/2)
for x in [.01,.1,.5,.9]:
    u0=math.sqrt(1-x*x)
    real=quad(lambda u:math.sqrt(max(0.,1-u*u-x*x)),0,u0,epsabs=1e-12)[0]
    imag=-quad(lambda u:math.sqrt(max(0.,u*u+x*x-1)),u0,1,epsabs=1e-12)[0]
    checks[f'orientation_{x}']=abs(complex(real,imag)-F(x))<1e-11
    checks[f'passive_{x}']=F(x).imag<0
    orientation.append(dict(x=x,real=real,imag=imag))
eta=math.pi**2/16
b=math.pi/12
def determinant(k,w):
    pi=math.pi/4*k*F(w/k)
    return (k*k-w*w)*(1+pi-w*w)-k*k
for k in [1e-4,3e-4,.001,.003,.01,.03,.1,.3,1.]:
    root=brentq(lambda w:determinant(k,w).real,0,k*(1-1e-9),xtol=1e-16)
    step=root*1e-4
    deriv=(determinant(k,root+step).real-determinant(k,root-step).real)/(2*step)
    damping=determinant(k,root).imag/deriv
    checks[f'mode_below_vk_{k}']=0<root<k
    checks[f'damping_positive_{k}']=damping>0
    checks[f'weak_damping_{k}']=damping/root<.1
    if k<=.001:
        checks[f'soft_frequency_{k}']=abs(root/(math.sqrt(eta)*k**1.5)-1)<.002
        checks[f'soft_damping_{k}']=abs(damping/(b*eta*k**3/2)-1)<.004
    modes.append(dict(k=k,frequency=root,estimated_damping=damping,damping_over_frequency=damping/root,frequency_over_k=root/k))
slope=float(np.polyfit(np.log([r['k'] for r in modes[:4]]),np.log([r['frequency'] for r in modes[:4]]),1)[0])
checks['frequency_power']=abs(slope-1.5)<.002
checks={k:bool(v) for k,v in checks.items()}
result=dict(checks=checks,all_pass=all(checks.values()),orientation=orientation,modes=modes,frequency_power=slope,
scope='Homogeneous zero-gap critical medium, isotropic identical-ring ensemble, a=Z=I=A*h^2=v=1. Real-part mode roots and first-order damping estimates, not exact second-sheet poles. No inhomogeneous halo or absolute timescale prediction.')
(P/'nodal_collective_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert result['all_pass']
