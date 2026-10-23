"""Source-adapted canonical Gaussian basis and exact initial residual-norm audit.
This is a representation/kernel calculation, not a bath or late-time solution.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.special import hankel1,h1vp
P=Path(__file__).resolve().parent
lam=.00881292

def mode_covariance(k,source):
 w=source['omega_over_H'];A=source['conformal_scale_over_H'];phi=source['background_over_H'][0];H=source['H_GeV'];m=.001;M=2*m*np.sqrt(1+.02**2)
 nus=np.sqrt(2.25-np.array([3*lam*phi**2+(m/H)**2,lam*phi**2+(m/H)**2,(M/H)**2,(M/H)**2]));pref=w**1.5/A
 result=[]
 for nu in nus:
  u=pref*np.sqrt(np.pi)/2*hankel1(nu,k*w)
  v=-pref*np.sqrt(np.pi)/(2*w)*(.5*hankel1(nu,k*w)+k*w*h1vp(nu,k*w))
  F=abs(u)**2;C=np.real(np.conj(u)*v)
  # Stable pure covariance, using the canonical Wronskian rather than cancellation.
  Pmom=C*C/F+lam**2/(4*F)
  S11=np.sqrt(2*F/lam);S21=C*np.sqrt(2/(lam*F));S22=1/S11
  result.append(dict(F=F,C=C,P=Pmom,S11=S11,S21=S21,S22=S22))
 return result

def kernel(L,kmin,kmax,source,padding_extra=0):
 # Symmetric continuum momentum cube, sphere selected inside it.
 K=int(np.ceil(kmax*L/(2*np.pi)));n=2*K+1;pad=4*K+1+padding_extra
 ints=np.arange(-K,K+1);r2=ints[:,None,None]**2+ints[None,:,None]**2+ints[None,None,:]**2;k=2*np.pi*np.sqrt(r2)/L
 selected=(k>=kmin-1e-13)&(k<=kmax+1e-13)&(k>0)
 cov=mode_covariance(k[selected],source);correlations=[];canonical=0.;reconstruction=0.;variances=[]
 for d in cov:
  canonical=max(canonical,float(np.max(abs(d['S11']*d['S22']-1))))
  reconstruction=max(reconstruction,float(np.max(abs((lam/2*(d['S21']**2+d['S22']**2))/d['P']-1))))
  coeff=np.zeros((pad,pad,pad));grid=np.zeros_like(k);grid[selected]=d['F']
  start=pad//2-K;coeff[start:start+n,start:start+n,start:start+n]=grid
  # No aliasing of momentum conservation in cubic or quartic products: pad>4K.
  corr=np.fft.ifftn(np.fft.ifftshift(coeff)).real*pad**3/L**3
  correlations.append(corr);variances.append(float(np.sum(grid)/L**3))
 f,h,x,y=correlations;q=source['background_over_H'][0]/source['conformal_scale_over_H'];c=source['cubic_coefficient']
 # <0|H_res^2|0>/lambda^2 per spatial volume in source-normal-ordered frame.
 # Wick contractions across the two vertices only. Different particle sectors orthogonal.
 phi3=L**3*np.mean(q*q*(6*f**3+2*f*h*h))/lam**2
 X3=L**3*np.mean(c*c*(2*x*(f*f+h*h)+4*y*f*h))/lam**2
 phi4=L**3*np.mean(1.5*(f**4+h**4)+f*f*h*h)/lam**2
 return dict(L=L,kmin=kmin,kmax=kmax,modes=int(selected.sum()),padding=pad,variances=variances,canonical_error=canonical,covariance_reconstruction_error=reconstruction,initial_residual_probability_curvature_per_volume=dict(Phi_cubic=float(phi3),X_cubic=float(X3),Phi_quartic=float(phi4)),initial_residual_number_curvature_per_volume=float(3*(phi3+X3)+4*phi4),scope='Coefficient of t^2 in residual excitation probability/number for this initial Gaussian state and fixed momentum band; NOT an on-shell production or thermalization rate.')

def main():
 O=P/sys.argv[1];O.mkdir(exist_ok=True);source=json.loads((P/'coupled_fragmentation_96_run/results.json').read_text())['source']
 # Fixed-band momentum refinement varies spacing while holding physical cutoffs fixed.
 low=2*np.pi/32;high=8*low
 refinement=[kernel(L,low,high,source) for L in [32.,48.,64.,96.,128.]]
 # Separate UV test; do not mistake changing physical cutoff for momentum convergence.
 uv=[kernel(32.,low,fac*low,source) for fac in [4,8,12,16,24]]
 independent_padding=kernel(32.,low,high,source,padding_extra=8)
 reference=refinement[0];keys=['Phi_cubic','X_cubic','Phi_quartic']
 paderror=max(abs(independent_padding['initial_residual_probability_curvature_per_volume'][key]/reference['initial_residual_probability_curvature_per_volume'][key]-1) for key in keys)
 # Exact Gaussian canonical transformation can absorb coherent displacements of any size.
 checks=dict(symplectic=all(r['canonical_error']<1e-12 for r in refinement+uv),covariance_reconstruction=all(r['covariance_reconstruction_error']<1e-12 for r in refinement+uv),padding_invariance=paderror<1e-10,nonnegative_norm=all(all(v>=0 for v in r['initial_residual_probability_curvature_per_volume'].values()) for r in refinement+uv))
 rel={key:abs(refinement[-1]['initial_residual_probability_curvature_per_volume'][key]/refinement[-2]['initial_residual_probability_curvature_per_volume'][key]-1) for key in keys}
 out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),fixed_band_refinement=refinement,UV_scan=uv,independent_padding_relative_error=paderror,last_refinement_relative_changes=rel,scope='Source-adapted basis and initial residual interaction kernel. Zero-mode quantum state and interacting initial cumulants not supplied. No time evolution of residual state, bath formation, or relic abundance.')
 (O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
if __name__=='__main__':main()
