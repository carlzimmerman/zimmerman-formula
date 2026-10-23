"""Conditional source continuation and necessary kinetic-overlap diagnostics.
Retains classical nonlinear fields; DOES NOT propagate a quantum density matrix.
No kinetic switch, thermal matching, particle seed, or abundance is assigned.
"""
from pathlib import Path
import json,sys,subprocess
import numpy as np
from scipy.signal import resample
P=Path(__file__).resolve().parent;lam=.00881292

def diagnostic(state,L):
 q,v=state[:,:2];n=q.shape[1];size=n**3
 kk=2*np.pi*np.fft.fftfreq(n,d=L/n);kx,ky,kz=np.meshgrid(kk,kk,kk,indexing='ij',sparse=True)
 k2=kx*kx+ky*ky+kz*kz;kd2=sum((2*np.sin(x*L/n/2)/(L/n))**2 for x in (kx,ky,kz))
 # Isotropic Hartree mass is a diagnostic choice, not an implemented closure.
 r=float(np.mean(np.sum(q*q,axis=0)));omega=np.sqrt(kd2+2*r)
 fq=np.fft.fftn(q,axes=(1,2,3))*L**1.5/size;fv=np.fft.fftn(v,axes=(1,2,3))*L**1.5/size
 F=np.sum(abs(fq)**2,axis=0);V=np.sum(abs(fv)**2,axis=0);C=np.sum((fq.conj()*fv).real,axis=0)
 dk=2*np.pi/L;bins=np.floor(np.sqrt(k2)/dk+.5).astype(int);nb=n+1
 def sums(x):return np.bincount(bins.ravel(),weights=np.broadcast_to(x,k2.shape).ravel(),minlength=nb)[:nb]
 count=sums(np.ones_like(k2));energy=.5*(V+omega**2*F);occ=energy/(lam*omega)
 e=sums(energy);N=sums(occ);omega_mean=np.divide(sums(omega),count,out=np.zeros(nb),where=count>0)
 # Per real degree of freedom: two Phi components per spatial wavevector.
 occmean=np.divide(N,2*count,out=np.zeros(nb),where=count>0)
 anom_re=sums((omega**2*F-V)/(2*lam*omega));anom_im=sums(C/lam)
 centered=q-q.mean(axis=(1,2,3))[:,None,None,None];cov=centered.reshape(2,-1)@centered.reshape(2,-1).T/size
 wick=np.trace(cov)**2+2*np.trace(cov@cov);fourth=float(np.mean(np.sum(centered**2,axis=0)**2))
 realgrad=.5*np.mean(sum(np.sum((np.roll(q,-1,axis=i)-q)**2,axis=0) for i in (1,2,3)))/(L/n)**2
 spectralgrad=float(.5*np.sum(kd2*F)/L**3)
 grad=.5*kd2*F;uv=k2>(.6*np.pi/(L/n))**2
 return dict(zero_mode_energy_proxy=float(e[0]/e.sum()),mean_square_fraction=float(np.sum(q.mean(axis=(1,2,3))**2)/r),connected_radial_fourth_over_wick=float((fourth-wick)/wick),UV_gradient_fraction=float(grad[uv].sum()/grad.sum()),parseval_gradient_error=abs(realgrad-spectralgrad)/max(realgrad,1e-30),count=count,energy=e,number_proxy=N,occupation=occmean,omega=omega_mean,anomalous_real=anom_re,anomalous_imag=anom_im,dk=dk)

def main():
 O=P/sys.argv[1];O.mkdir(exist_ok=True);h=np.fromfile(P/'coupled_fragmentation_96_run/fine96_initial.bin',count=9)
 original=np.fromfile(P/'coupled_fragmentation_96_run/fine96_final.bin').reshape(2,4,96,96,96)
 rows=[];histories={}
 for name,n,dt in [('base96',96,.01),('time96',96,.005),('space128',128,.01)]:
  state=original.copy()
  if n!=96:
   for ax in (2,3,4):state=resample(state,n,axis=ax)
  hist=[];balance=0.;work=0.;initialE=None
  for j in range(21):
   d=diagnostic(state,float(h[1]));d['z']=200.+j;hist.append(d)
   if j==20:break
   hh=h.copy();hh[0]=n;hh[2]=dt;hh[3]=1.
   with (O/'restart.bin').open('wb') as f:hh.tofile(f);state.astype('<f8').tofile(f)
   subprocess.run([str(P/'coupled_field_restart'),str(O/'restart.bin'),str(O/'step.csv'),str(O/'step_final.bin'),str(200.+j)],check=True)
   tab=np.genfromtxt(O/'step.csv',delimiter=',',names=True)
   if initialE is None:initialE=float(tab['Econf'][0])
   work+=float(tab['work'][-1]);balance=max(balance,abs(float(tab['Econf'][-1])-work-initialE)/abs(initialE))
   state=np.fromfile(O/'step_final.bin').reshape(2,4,n,n,n)
  # Equal-time sample average on 200..220. Not a thermal/ensemble average.
  count=hist[0]['count'];E=np.mean([d['energy'] for d in hist],axis=0);N=np.mean([d['number_proxy'] for d in hist],axis=0)
  occ=np.divide(N,2*count,out=np.zeros_like(N),where=count>0);mask=np.arange(len(E))>0;total=E[mask].sum()
  bands={}
  for label,lo,hi in [('f_below_1',0,1),('f_1_to_10',1,10),('f_10_to_inverse_lambda',10,1/lam),('lambda_f_above_1',1/lam,np.inf)]:
   bands[label]=float(E[mask&(occ>=lo)&(occ<hi)].sum()/total)
  A=np.mean([d['anomalous_real'] for d in hist],axis=0)+1j*np.mean([d['anomalous_imag'] for d in hist],axis=0)
  row=dict(name=name,n=n,dt=dt,energy_work_relative_error=balance,nonzero_energy_proxy_fractions=bands,zero_mode_energy_proxy_time_mean=float(np.mean([d['zero_mode_energy_proxy'] for d in hist])),mean_square_fraction_time_mean=float(np.mean([d['mean_square_fraction'] for d in hist])),radial_fourth_cumulant_range=[float(min(d['connected_radial_fourth_over_wick'] for d in hist)),float(max(d['connected_radial_fourth_over_wick'] for d in hist))],time_averaged_anomalous_ratio=float(np.sum(abs(A[mask]))/np.sum(N[mask])),max_UV_gradient_fraction=float(max(d['UV_gradient_fraction'] for d in hist)),max_parseval_gradient_error=float(max(d['parseval_gradient_error'] for d in hist)))
  np.savez_compressed(O/(name+'_spectra.npz'),z=[d['z'] for d in hist],energy=[d['energy'] for d in hist],number_proxy=[d['number_proxy'] for d in hist],counts=count,dk=hist[0]['dk'],anomalous_real=[d['anomalous_real'] for d in hist],anomalous_imag=[d['anomalous_imag'] for d in hist])
  state.tofile(O/(name+'_final.bin'));rows.append(row);histories[name]=(E,N)
  print(json.dumps(row),flush=True)
 # Common physical band k<=4; avoid comparing different Nyquist cutoffs.
 end=int(4/(2*np.pi/h[1]))+1;baseline=histories['base96'][0][1:end]
 differences={name:float(np.sum(abs(histories[name][0][1:end]-baseline))/np.sum(baseline)) for name in ['time96','space128']}
 checks=dict(energy_balance=all(r['energy_work_relative_error']<1e-4 for r in rows),parseval=all(r['max_parseval_gradient_error']<1e-12 for r in rows),finite=all(np.isfinite(r['time_averaged_anomalous_ratio']) for r in rows))
 out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),rows=rows,common_band_energy_spectrum_L1_relative_differences=differences,scope='Classical-statistical restart-window diagnostic only. 128 grid interpolates the saved 96 state; it does not redo source-to-200 evolution. Occupations and anomalous correlations are isotropic Hartree oscillator proxies, not particles or measured quantum cumulants. No quantum Moyal terms, no bath formation, no surviving abundance. Large lambda*f obstructs a weak quasiparticle expansion for populated soft modes but does not prove that every resummed kinetic description fails.')
 (O/'results.json').write_text(json.dumps(out,indent=2));(O/'restart.bin').unlink();(O/'step_final.bin').unlink();print(json.dumps(differences),flush=True)
 if not out['all_pass']:raise SystemExit(1)
if __name__=='__main__':main()
