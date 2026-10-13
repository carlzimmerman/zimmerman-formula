"""Retarded nodal patch response: interband, spectral and bath audits."""
from pathlib import Path
import json, math, cmath
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
P=Path(__file__).parent
checks={}; euclidean=[]; absorption=[]; baths=[]
# All kernels divided by A*h^2; field is the gap divided by h.
def kernel(m,q,z,longitudinal):
    s=cmath.sqrt(q*q-z*z)
    if m==0:return math.pi*s/4
    if abs(s)<1e-12*m:return complex(2*m if longitudinal else m)
    if longitudinal:return m+(s*s+4*m*m)/(2*s)*cmath.atan(s/(2*m))
    return m+s/2*cmath.atan(s/(2*m))
def loss(m,q,w,longitudinal):
    if w*w<=q*q+4*m*m:return 0.
    t=math.sqrt(w*w-q*q)
    return math.pi/4*((t*t-4*m*m)/t if longitudinal else t)
def raw_euclidean(m,q,omega,longitudinal):
    scale=max(m,q,omega,1.)
    cutoff=2000*scale
    nodes,weights=leggauss(160); theta=(np.arange(768)+.5)*2*np.pi/768
    edges=sorted(set([0.,scale*.1,scale*.5,scale,2*scale,10*scale,100*scale,cutoff]))
    ans=0.
    for lo,hi in zip(edges[:-1],edges[1:]):
        k=((nodes+1)*(hi-lo)/2+lo)[:,None]
        ea=np.sqrt(k*k+q*q/4-k*q*np.cos(theta)+m*m)
        eb=np.sqrt(k*k+q*q/4+k*q*np.cos(theta)+m*m)
        overlap=k*k-q*q/4+m*m*(1-2*longitudinal)
        total=ea+eb
        response=-(1+overlap/(ea*eb))*total/(total*total+omega*omega)
        e=np.sqrt(k*k+m*m)
        zero=-(k*k/e**3 if longitudinal else 1/e)
        ans+=float(np.dot(weights,np.mean(k*(response-zero),axis=1))*(hi-lo)/2)
    return ans
for m,q in [(0.,0.),(0.,1.),(.2,0.),(.2,1.),(1.,.3)]:
 for omega in [.2,2.]:
  for longitudinal in [False,True]:
    k0=kernel(m,q,0j,longitudinal).real
    full=kernel(m,q,1j*omega,longitudinal).real
    spectral=2*omega**2/math.pi*quad(lambda w:loss(m,q,w,longitudinal)/(w*(w*w+omega*omega)),math.sqrt(q*q+4*m*m),np.inf,epsabs=1e-10)[0]
    direct=raw_euclidean(m,q,omega,longitudinal)
    expected=full-(2*m if longitudinal else m)
    key=f'{m}_{q}_{omega}_{longitudinal}'
    checks[key+'_spectral']=abs(spectral-(full-k0))<1e-8
    checks[key+'_interband']=abs(direct-expected)/max(abs(expected),1e-12)<.005
    checks[key+'_positive_Euclidean']=full>0
    euclidean.append(dict(gap=m,q=q,omega_E=omega,longitudinal=longitudinal,closed=expected,direct=direct,spectral_shift=spectral))
for m,q in [(.2,0.),(.2,1.),(1.,.3)]:
 threshold=math.sqrt(q*q+4*m*m)
 for ratio in [.5,.99,1.01,2.]:
  w=ratio*threshold
  for longitudinal in [False,True]:
    actual=-kernel(m,q,complex(w,1e-9*threshold),longitudinal).imag
    expected=loss(m,q,w,longitudinal)
    checks[f'absorption_{m}_{q}_{ratio}_{longitudinal}']=abs(actual-expected)<2e-6*threshold
    absorption.append(dict(gap=m,q=q,w_over_threshold=ratio,longitudinal=longitudinal,loss=actual,expected=expected))
for m in [.1,1.,10.]:
 for longitudinal in [False,True]:
    w=m*1e-3
    actual=((2*m if longitudinal else m)-kernel(m,0.,complex(w,0),longitudinal).real)/w**2
    expected=1/((6 if longitudinal else 4)*m)
    checks[f'positive_inertia_{m}_{longitudinal}']=actual>0 and abs(actual/expected-1)<1e-6
# Finite positive spectral bath realizing the subtracted retarded self-energy.
# q=k, a=Z=I=A*h^2=1; scalar couples to polarization parallel to background.
for k in [.1,1.,3.]:
 m=.3;threshold=math.sqrt(k*k+4*m*m)
 edges=np.geomspace(threshold,100*threshold,81)
 freq=np.sqrt(edges[:-1]*edges[1:]);dw=np.diff(edges)
 c2=np.array([2/math.pi*w*loss(m,k,w,True)*d for w,d in zip(freq,dw)])
 stiff=np.array([[k*k,-k],[-k,1+kernel(m,k,0j,True).real]])
 H=np.zeros((82,82));H[:2,:2]=stiff
 for j,(w,cc) in enumerate(zip(freq,c2),start=2):
    H[1,1]+=cc/w**2;H[j,j]=w*w;H[1,j]=H[j,1]=-math.sqrt(cc)
 eig=np.linalg.eigvalsh(H)
 schur=H[:2,:2]-H[:2,2:]@np.diag(1/freq**2)@H[2:,:2]
 checks[f'bath_positive_{k}']=bool(eig.min()>0)
 checks[f'bath_Schur_{k}']=bool(np.max(abs(schur-stiff))<1e-11)
 baths.append(dict(k=k,bath_modes=len(freq),minimum_frequency_squared=float(eig.min())))
checks={k:bool(v) for k,v in checks.items()}
result=dict(checks=checks,all_pass=all(checks.values()),euclidean=euclidean,absorption=absorption,baths=baths,
scope='Leading axial nodal patch at homogeneous gap, zero T/mu. Positive kinetic terms and static stiffness assumed for added scalar sector. No inhomogeneous galaxy, cosmological medium, finite-T response or UV completion.')
(P/'nodal_dynamics_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(checks=checks,baths=baths),indent=2));assert result['all_pass']
