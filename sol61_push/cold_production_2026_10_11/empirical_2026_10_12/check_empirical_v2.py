"""Frozen descriptive RAR check and below-resonance SIDM rate bound."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
P=Path(__file__).resolve().parent
D=np.loadtxt(P/'RAR.mrt',skiprows=13)
assert D.shape==(2693,4) and np.isfinite(D).all()
lgbar,egbar,lgobs,egobs=D.T
gbar=10**lgbar

def h(y):
    return y/np.expm1(np.sqrt(np.minimum(y,1e4)))
def dh(y):
    return (h(y*(1+1e-6))-h(y*(1-1e-6)))/(2e-6*y)
yp=brentq(dh,1,5);hp=h(yp)
ly=np.linspace(-12,12,240001); y=10**ly
slope=np.maximum(dh(y),.05*hp/(y+yp))
hm=h(y[0])+np.r_[0,np.cumsum((slope[1:]+slope[:-1])*.5*np.diff(y))]
def mono(y):return 1+np.interp(np.log10(y),ly,hm)/y
def expnu(y):return 1/(-np.expm1(-np.sqrt(y)))
def stats(pred,mask):
    res=lgobs[mask]-np.log10(pred[mask])
    return dict(n=int(mask.sum()),rms_dex=float(np.sqrt(np.mean(res**2))),median_residual_dex=float(np.median(res)),fraction_within_02dex=float(np.mean(abs(res)<.2)))
rows={}
for name,a0 in [('canonical',9.3603e-11),('alternate',1.1312e-10),('literature_reference',1.2e-10)]:
    row={}
    for law,nu in [('mono',mono),('exponential',expnu)]:
        pred=gbar*nu(gbar/a0)
        row[law]={k:stats(pred,m) for k,m in [('all',np.ones(len(D),bool)),('below_1e10',gbar<1e-10),('above_1e10',gbar>=1e-10)]}
    rows[name]=dict(a0=a0,metrics=row)
newton=stats(gbar,np.ones(len(D),bool))
# Relative-speed Maxwell distribution, 1D single-particle dispersion s.
# Bound integrates only v <= 3000 km/s: x <= .251, safely below pole.
c=299792.458;u=.01

def sig(v):
    x=(v/(2*c*u))**2
    return 4*((2-x/(1-x))/2)**2/(1+u*u*x)
rate=[]
for mean in [1150.,1900.]:
    s=mean*np.sqrt(np.pi)/4
    pdf=lambda v:v*v*np.exp(-v*v/(4*s*s))/(2*np.sqrt(np.pi)*s**3)
    low,err=quad(lambda v:sig(v)*v*pdf(v)/mean,0,3000,epsabs=1e-10)
    weight=quad(lambda v:v*pdf(v)/mean,0,3000)[0]
    rate.append(dict(mean_relative_speed_kms=mean,partial_effective_sigma_over_m_cm2_g=low,rate_weight_below_3000=weight,quadrature_error=err))
checks={'data_count':len(D)==2693,'newton_limit':abs(expnu(1e6)-1)<1e-12,'deep_limit':abs(mono(1e-8)*1e-4-1)<1e-3,'mono_matches_exp_low':bool(np.max(abs(mono(np.logspace(-6,0,100))/expnu(np.logspace(-6,0,100))-1))<1e-6),'cross_section_threshold':sig(0)==4,'below_resonance':(3000/(2*c*u))**2<.5,'maxwell_normalization':abs(quad(lambda v:v*v*np.exp(-v*v/4)/(2*np.sqrt(np.pi)),0,30)[0]-1)<1e-10}
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values()),checks
R=dict(source_url='https://astroweb.case.edu/SPARC/RAR.mrt',data_sha256=hashlib.sha256((P/'RAR.mrt').read_bytes()).hexdigest(),rar=rows,baryons_only=newton,cross_sections={str(v):sig(v) for v in [30,200,1150,1900,3000]},partial_rate_bounds=rate,checks=checks,limits=['Descriptive reuse of calibration data, not held-out validation','No galaxy identifiers/covariances in table: no p-values or pointwise bootstrap','No fitted parameters in this run','Cluster translation conditional on Maxwell speeds, dominant interacting component and published Jeans modelling; not a full exclusion likelihood','Cross section formula used only away from resonance; omitted rate contribution is nonnegative'])
(P/'run_v2'/'results.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps(R,indent=2))
