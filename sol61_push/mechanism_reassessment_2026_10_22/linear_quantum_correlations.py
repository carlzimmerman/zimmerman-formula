"""Pre-backreaction quantum covariance evolution of the existing high-H Phi source.
Leading early conformal quartic sector; not a bath or a relic solver.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.special import hankel1,h1vp
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
s=json.loads((P/'coupled_fragmentation_96_run/results.json').read_text())['source'];lam=.00881292;A=s['conformal_scale_over_H'];w=s['omega_over_H'];c=s['cubic_coefficient'];H=s['H_GeV'];bg=np.array(s['background_over_H']);L=32.
raw=np.fromfile(P/'coupled_fragmentation_96_run/fine96_initial.bin',dtype='<f8');N=int(raw[0]);init=raw[9:].reshape(2,4,N,N,N);q0=float(init[0,0].mean());v0=float(init[1,0].mean());amp=(q0**4+2*v0*v0)**.25
rows={}
for name,n,dt in [('base32',32,.01),('time32',32,.005),('space48',48,.01),('space64',64,.005)]:
 f=np.fft.fftfreq(n)*n;xyz=np.meshgrid(f,f,f,indexing='ij');r2=sum(x*x for x in xyz).ravel();r2=r2[r2>0];r2,deg=np.unique(r2,return_counts=True);k=2*np.pi*np.sqrt(r2)/L;kh=k*w
 nus=np.sqrt(2.25-np.array([3,1])*lam*bg[0]**2);pref=w**1.5/A
 U=np.array([pref*np.sqrt(np.pi)/2*hankel1(nu,kh) for nu in nus]);V=np.array([-pref*np.sqrt(np.pi)/(2*w)*(.5*hankel1(nu,kh)+kh*h1vp(nu,kh)) for nu in nus]);U0=U.copy();V0=V.copy()
 old=(kh>=np.exp(-5))&(kh<=.35);q=q0;v=v0;series=[];cross=None;maxwr=0.;maxe=0.
 for it in range(int(100/dt)+1):
  z=it*dt;freq2=k[None,:]**2+np.array([3,1])[:,None]*q*q
  if it%round(.2/dt)==0:
   omega=np.sqrt(freq2);F=abs(U)**2;Pi=abs(V)**2;C=np.real(np.conj(U)*V)
   tad=F-lam/(2*omega);CL,CT=np.sum(tad*deg,axis=1)/L**3
   back=abs(3*CL+CT)/amp**2
   outside=np.sum((3*tad[0,~old]+tad[1,~old])*deg[~old])/L**3/amp**2
   occupation=(Pi+freq2*F)/(2*lam*omega)-.5
   kappa=(freq2*F-Pi)/(2*lam*omega)+1j*C/lam
   wr=-2*np.imag(np.conj(U)*V)/lam;maxwr=max(maxwr,float(np.max(abs(wr-1))))
   # Quantum purity: Gaussian symplectic eigenvalue remains 1/2 despite n>0.
   # Use Wronskian for stability, not subtracting large squared occupations.
   purity_error=float(np.max(abs(wr*wr-1)))
   e=.5*v*v+.25*q**4;maxe=max(maxe,abs(e/(.5*v0*v0+.25*q0**4)-1))
   series.append([z,q,back,outside,CL,CT,float(np.max(occupation)),purity_error])
   if cross is None and back>=.1:cross=dict(z=z,a=1+z/w,H_over_M=H/(1+z/w)**2/(.002*np.sqrt(1+.02**2)),backreaction=back,outside_old_band_signed_share=float(outside/back))
  if cross is not None:break
  # Joint symplectic propagation in the linearized, prescribed mean background.
  V-=.5*dt*freq2*U;v-=.5*dt*q**3
  U+=dt*V;q+=dt*v
  freq2=k[None,:]**2+np.array([3,1])[:,None]*q*q
  V-=.5*dt*freq2*U;v-=.5*dt*q**3
 arr=np.array(series);np.savetxt(O/(name+'.csv'),arr,delimiter=',',header='z,q,backreaction_adiabatic0_subtracted,outside_old_band_signed,CL,CT,max_instantaneous_n,purity_error',comments='')
 np.savez_compressed(O/(name+'_final.npz'),k=k,degeneracy=deg,U=U,V=V,z=z,q=q,v=v,old_band=old)
 # Bound omitted classical cubic curvature relative to quartic oscillation scale.
 a=1+z/w;Xnorm=np.linalg.norm(bg[2:])/A
 omitted=2*abs(c)*a*a*Xnorm/amp**2
 rows[name]=dict(n=n,dt=dt,first_backreaction_10percent=cross,max_Wronskian_error=maxwr,max_background_energy_error=maxe,max_omitted_frozen_X_curvature_over_quartic_scale=float(omitted),end_z=z)
 print(name,rows[name],flush=True)
checks=dict(Wronskian=all(r['max_Wronskian_error']<1e-9 for r in rows.values()),background_energy=all(r['max_background_energy_error']<1e-4 for r in rows.values()),cubic_early_bound=all(r['max_omitted_frozen_X_curvature_over_quartic_scale']<1e-8 for r in rows.values()),backreaction_reached=all(r['first_backreaction_10percent'] is not None for r in rows.values()))
# Treat crossing convergence as measured, not a proof of physical renormalization.
zs=[r['end_z'] for r in rows.values()]
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),cases=rows,crossing_range=zs,scope='Actual linear quantum nonzero-mode covariance evolution in leading early quartic background from saved source Cauchy mean. Stopped at diagnostic 10% tadpole backreaction, NOT declared thermal. Zeroth-order adiabatic subtraction is a finite-cutoff diagnostic, not full renormalization. No collision self-energies, absorption/inverse, bath formation or surviving abundance in this solver.')
(O/'results.json').write_text(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
