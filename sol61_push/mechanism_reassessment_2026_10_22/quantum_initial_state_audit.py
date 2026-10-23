"""Quantum continuation prerequisites; no invented late state or bath epoch."""
import json, sys, math
from pathlib import Path
import numpy as np
from scipy.special import hankel1,h1vp
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
s=json.loads((P/'coupled_fragmentation_96_run/results.json').read_text())['source']
lam=.00881292;A=s['conformal_scale_over_H'];w=s['omega_over_H'];phi=s['background_over_H'][0];H=s['H_GeV'];m=.001;M=2*m*np.sqrt(1+.02**2)
nu=np.sqrt(2.25-np.array([3*lam*phi**2+(m/H)**2,lam*phi**2+(m/H)**2,(M/H)**2,(M/H)**2]))
pref=w**1.5/A
rows=[]
for n in [32,64,96]:
 L=32.;modes=np.fft.fftfreq(n)*n;kg=np.meshgrid(modes,modes,modes,indexing='ij');k=np.sqrt(sum(x*x for x in kg))*2*np.pi/L;k=k[k>0];kh=k*w
 retained=(kh>=np.exp(-5))&(kh<=.35)
 # Group exactly degenerate continuum Fourier shells for compact future inputs.
 kval,counts=np.unique(k,return_counts=True);khval=kval*w
 data=[];err=0.;oldvar=[];allvar=[];vac=[]
 for v in nu:
  u=np.sqrt(np.pi)/2*hankel1(v,khval);up=-np.sqrt(np.pi)/2*(.5*hankel1(v,khval)+khval*h1vp(v,khval))/w
  F=pref**2*abs(u)**2;C=pref**2*np.real(np.conj(u)*up)
  # Store stable Cholesky factors. This is covariance of nonzero modes only.
  cholq=pref*abs(u);cholp=pref/(2*w*abs(u));cholcross=pref*np.real(np.conj(u)*up)/abs(u)
  Pi=cholcross**2+cholp**2
  wr=-2*pref**2*np.imag(np.conj(u)*up)
  err=max(err,float(np.max(abs(wr/lam-1))))
  det_stable=cholq**2*cholp**2
  selected=(khval>=np.exp(-5))&(khval<=.35)
  oldvar.append(float(np.sum(counts[selected]*F[selected])/L**3));allvar.append(float(np.sum(counts*F)/L**3))
  vac.append(float(np.sum(counts*lam/(2*kval))/L**3))
  data.append(np.array([F,C,Pi,cholq,cholcross,cholp,det_stable]))
 np.savez_compressed(O/('nonzero_mode_covariance_n%d.npz'%n),k=kval,degeneracy=counts,covariance=np.array(data),nu=nu,effective_hbar=lam,box_L=L)
 missing=n**3-1-int(retained.sum())
 rows.append(dict(n=n,nonzero_real_mode_count=n**3-1,retained_count=int(retained.sum()),missing_quantum_covariance_count=missing,missing_fraction=missing/(n**3-1),effective_hbar=lam,expected_minimum_determinant=lam**2/4,max_Wronskian_relative_error=err,retained_variances=oldvar,BD_completed_nonzero_variances=allvar,massless_vacuum_variances=vac,unsubtracted_added_Phi_Hartree_curvature=[3*(allvar[0]-oldvar[0])+(allvar[1]-oldvar[1]),allvar[0]-oldvar[0]+3*(allvar[1]-oldvar[1])]))
checks=dict(source_normalization=abs(w*w/(A*A)/lam-1)<1e-12,retained_modes=all(r['retained_count']==364 for r in rows),Wronskian=all(r['max_Wronskian_relative_error']<1e-10 for r in rows),quantum_uncertainty=all(np.max(abs(np.load(O/('nonzero_mode_covariance_n%d.npz'%r['n']))['covariance'][:,6]/(lam**2/4)-1))<1e-12 for r in rows))
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),rows=rows,scope='Audit of source covariance prescription, not inference of an ensemble from one classical realization. NPZ files complete nonzero finite-box modes with the SAME constant-background Hankel ansatz. Zero-mode quantum state, full interacting inflationary state and renormalization remain unspecified. No thermalization evolution or abundance.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
