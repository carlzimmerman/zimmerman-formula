"""Continuum radial audit of initial high-H non-Gaussian residual kernels.
Also supplies an exact potential-kick map; no kinetic/bath evolution claimed.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.integrate import simpson
from scipy.special import roots_legendre
from scipy.interpolate import PchipInterpolator
from moving_source_basis import mode_covariance,lam
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
s=json.loads((P/'coupled_fragmentation_96_run/results.json').read_text())['source'];lo=2*np.pi/32;hi=8*lo;q=s['background_over_H'][0]/s['conformal_scale_over_H'];c=s['cubic_coefficient']
def radial(nk,R,dr):
 x,w=roots_legendre(nk);k=lo+(hi-lo)*(x+1)/2;w=w*(hi-lo)/2
 F=np.array([v['F'] for v in mode_covariance(k,s)]);r=np.linspace(0,R,round(R/dr)+1);K=np.empty((4,len(r)))
 for start in range(0,len(r),256):
  rr=r[start:start+256];K[:,start:start+256]=(F*(w*k*k)[None,:])@np.sinc(k[:,None]*rr[None,:]/np.pi)/(2*np.pi**2)
 f,h,xx,y=K;measure=4*np.pi*r*r/lam**2
 terms=[q*q*(6*f**3+2*f*h*h),c*c*(2*xx*(f*f+h*h)+4*y*f*h),1.5*(f**4+h**4)+f*f*h*h]
 vals=[float(simpson(measure*t,x=r)) for t in terms]
 return dict(nk=nk,R=R,dr=dr,Phi_cubic=vals[0],X_cubic=vals[1],Phi_quartic=vals[2],residual_number_curvature_density=3*(vals[0]+vals[1])+4*vals[2])
rows=[radial(256,128,.1),radial(512,256,.05),radial(1024,512,.05)]
# Independent momentum-space triangle quadrature for integral K_a K_b K_c.
grid=np.geomspace(lo,hi,8192);d=mode_covariance(grid,s);interp=[PchipInterpolator(grid,x['F']) for x in d]
def triple(a,b,cc,n):
 z,w=roots_legendre(n);k=lo+(hi-lo)*(z+1)/2;ww=w*(hi-lo)/2
 x,kp=np.meshgrid(k,k,indexing='ij');weight=ww[:,None]*ww[None,:]*x*kp*interp[a](x)*interp[b](kp)
 low=np.maximum(abs(x-kp),lo);high=np.minimum(x+kp,hi);length=np.maximum(high-low,0)
 z3,w3=roots_legendre(64);inner=np.zeros_like(x)
 for t,wt in zip(z3,w3):
  p=low+length*(t+1)/2;inner+=wt*p*interp[cc](p)*length/2
 return float(np.sum(weight*inner)/(8*np.pi**4))
direct=[]
for n in [128,256]:
 val=q*q*(6*triple(0,0,0,n)+2*triple(0,1,1,n))/lam**2
 direct.append(dict(n=n,Phi_cubic=val))
ref=rows[-1];changes={k:abs(ref[k]/rows[-2][k]-1) for k in ['Phi_cubic','X_cubic','Phi_quartic']};cross=abs(direct[-1]['Phi_cubic']/ref['Phi_cubic']-1)
# Exact kick: N_res(t)/V = t^2 [3 D3 + 4 D4] for normal-ordered residual potential.
# This formula holds for a single frozen potential kick, not full Hamiltonian time evolution.
kicks=[dict(delta_z=t,residual_number_density=t*t*ref['residual_number_curvature_density'],residual_number_in_L32_box=32**3*t*t*ref['residual_number_curvature_density']) for t in [.01,.05,.1]]
checks=dict(radial_refinement=max(changes.values())<.001,independent_cubic_quadrature=cross<.001,direct_refinement=abs(direct[-1]['Phi_cubic']/direct[-2]['Phi_cubic']-1)<.001)
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),radial=rows,independent_momentum_space=direct,radial_last_changes=changes,independent_relative_error=cross,exact_single_kick=kicks,scope='Continuum convergence for FIXED momentum band [2pi/32,pi/2] of initial Gaussian residual kernels. Not the full UV/IR theory, no repeated quantum evolution, no on-shell collision rate or abundance.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
