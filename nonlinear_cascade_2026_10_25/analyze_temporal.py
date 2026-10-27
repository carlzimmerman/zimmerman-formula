"""Do not mistake kinetic-basis phase winding for a fast density cascade."""
import argparse,json
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();p=Path('nonlinear_cascade_2026_10_25/run_temporal');s=np.load(p/'material_history.npz');t=s['times_Myr'];mass=s['mass'];flux=s['mass_flux'];r=s['r'];vol=s['vol'];rm=float(s['rm']);dt=np.median(np.diff(t));assert np.max(abs(np.diff(t)-dt))<1e-7;freq=2*np.pi*np.fft.rfftfreq(len(t),d=dt);mean=np.mean(mass,axis=0);rho=mean/vol;face=.5*(r[1:]+r[:-1]);dr=np.diff(r);rhoface=.5*(rho[:,1:]+rho[:,:-1]);weight=dr/(2*face*face*np.maximum(rhoface,1e-20));densityweight=1/np.maximum(mean,1e-20);mult=np.ones(len(freq))*2;mult[0]=1;mult[-1]=1 if len(t)%2==0 else 2;rows=[]
for pow in [2,4]:
 window=np.sin(np.pi*(np.arange(len(t))+.5)/len(t))**pow;J=np.fft.rfft(flux*window[:,None,None],axis=0);D=np.fft.rfft((mass-mean)*window[:,None,None],axis=0);Jpow=np.abs(J)**2*weight[None,:,:]*mult[:,None,None];Dpow=np.abs(D)**2*densityweight[None,:,:]*mult[:,None,None];regions={'inner_T_region':face*rm<50,'front_region':(face*rm>=50)&(face*rm<=80),'outer_region':face*rm>80};stats={}
 for name,reg in regions.items():
  en=np.sum(Jpow[:,:,reg],axis=(1,2));stats[name]={'fraction_flux_spectral_proxy_above_1_per_Myr':float(np.sum(en[freq>=1])/np.sum(en)),'fraction_above_0_02_per_Myr':float(np.sum(en[freq>=.02])/np.sum(en))}
 den=np.sum(Dpow[:,:,r*rm<50],axis=(1,2));rows.append({'window_power':pow,'flux_regions':stats,'inner_density_variance_fraction_above_1_per_Myr':float(np.sum(den[freq>=1])/np.sum(den))})
out={'results':rows,'scope':'Temporal spectra of actual full-evolution densities and exact material mass currents. Fixed mean-density weights give a spectral proxy, not an exact split of full nonlinear Hamiltonian energy. Fast kinetic eigenbasis occupation alone is not a fast density/phonon population.','time_Myr':float(t[-1]+dt/2)};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
