"""Independent source identity and omitted kinetic-stiffness audit."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline,PchipInterpolator
from branch_checked import Branch

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();b=Branch();L=.5;R=b.Rf-.05
# Split at BOTH density-cell and translated phase knots. The older fixed
# cell quadrature did not resolve every PCHIP second-derivative break.
cuts=np.unique(np.r_[b.edges,b.rad-b.Rf+R]);cuts=cuts[(cuts>=0)&(cuts<=b.edges[-1])];nd,wt=np.polynomial.legendre.leggauss(24);r=((cuts[:-1,None]+cuts[1:,None])/2+np.diff(cuts)[:,None]*nd/2).ravel();w=(np.diff(cuts)[:,None]*wt/2).ravel();cell=np.clip(np.searchsorted(b.edges,r,side='right')-1,0,b.m.n-1);rho=b.rho0[cell]+L*b.drho[cell];Q=np.r_[0,np.cumsum(b.dm)][cell]+b.drho[cell]*(r**3-b.edges[cell]**3)/3;x,xr=b.phase(r,R);q=np.sin(np.pi*x/2)**2;qr=np.pi/2*np.sin(np.pi*x)*xr
source=np.array([-sum(w*Q*qr),-sum(w*r*r*rho*qr)]);mtgrad=np.array([sum(w*r*r*b.drho[cell]*q),-sum(w*r*r*rho*qr)]);err=float(np.linalg.norm(source-mtgrad)/np.linalg.norm(mtgrad));assert err<1e-11
src=json.loads(Path('front_dynamics_2026_10_25/run_branch_checked/results.json').read_text())['runs'][-1];a=np.array(src['rows']);lam=a[:,0];logG=PchipInterpolator(lam,np.log(a[:,7]));G=np.exp(logG(lam));v2=np.maximum(2*(a[0,2]-a[:,2])/G,0);acc=(-a[:,3]-.5*G*logG(lam,1)*v2)/G
out={'source_identity_split_knots_relative_error':err,'source_integrals':source.tolist(),'continuous_mass_derivatives':mtgrad.tolist(),'kinetic_stiffness_runs':[]}
for h in [1e-3,5e-4]:
 Bz=[];Azz=[]
 for row in a:
  l,R=row[:2];u=np.array([1.,row[6]]);g=b.tensors(l,R)['G'];gp=b.tensors(l,R+h)['G'];gm=b.tensors(l,R-h)['G'];d=(gp-gm)/(2*h);dd=(gp-2*g+gm)/(h*h);Bz.append(float(d[1]@u));Azz.append(float(u@dd@u))
 Bz=np.array(Bz);Azz=np.array(Azz);corr=Bz*acc+(CubicSpline(lam,Bz)(lam,1)-.5*Azz)*v2;ratio=corr/a[:,5]
 out['kinetic_stiffness_runs'].append({'R_step_dimensionless':h,'max_absolute_kinetic_correction_over_static_curvature':float(max(abs(ratio))),'minimum_effective_curvature':float(min(a[:,5]+corr)),'effective_curvature':(a[:,5]+corr).tolist(),'B_z':Bz.tolist(),'A_zz':Azz.tolist()});Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out['kinetic_stiffness_runs'][-1].items() if k not in ['effective_curvature','B_z','A_zz']},flush=True)
