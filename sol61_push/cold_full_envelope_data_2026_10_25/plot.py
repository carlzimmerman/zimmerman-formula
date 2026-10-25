"""Standalone scientific figure; predictions are conditional spherical screens."""
import os
os.environ['MPLCONFIGDIR']='/tmp/cct018_mpl'
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,pathlib,math
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize,brentq
import fit_v2 as fit
from physics import *
from data import load,P
D=json.loads((P/'fit_002/result.json').read_text());fig,axs=plt.subplots(2,4,figsize=(17,8.2))
for j,name in enumerate(fit.NAMES):
 d=load(name);meta=D['datasets'][name];a=meta['observed_rhalf_pc'];ms=meta['stellar_mass_Msun'];row=next(r for r in D['rows'] if r['name']==name and r['footing']=='canonical' and r['beta']==0);free=row['free_Plummer'];half=row['fixed_supply_envelopes'][1];R=np.geomspace(10,max(4000,d['R'].max()),170);ax=axs[0,j]
 for model,color,label in [(free,'#2166ac','Free Plummer reference'),(half,'#1b7837','Half-supply envelope')]:
  b=model['scale_pc'];m=model['cold_mass_Msun']
  for k,ar in enumerate(d['aa']):
   sig=project(R,ar,lambda r:baryon_g(r,ms,d['aa'],'canonical')+plummer_g(r,m,b));ax.plot(R,np.sqrt(sig),color=color,lw=1.8,ls='-' if k==0 else '--',label=label if k==0 else None)
 prof=next(p for p in fit.profiles(name) if p['tag']=={'Draco':'Draco_fine_late','Sextans':'Sextans_legacy_late','Fornax':'Fornax_initial','Leo I':'Leo I_initial'}[name]);rr,dm=prof['r'],prof['dm']
 for k,ar in enumerate(d['aa']):
  sig=project(R,ar,lambda r:baryon_g(r,ms,d['aa'],'canonical')+g_cold(r,rr,dm));ax.plot(R,np.sqrt(sig),color='#b2182b',ls='-' if k==0 else '--',lw=1.6,label=('Saved full profile (see text)' if k==0 else None))
 # Four equal-count radial bins. Profile error bars are exploratory, no full selection/foreground model.
 order=np.argsort(d['R'])
 for ix in np.array_split(order,4):
  def obj(x):return -float(np.sum(window_logpdf(d['v'][ix],x[0],np.exp(2*x[1])+d['ev'][ix]**2,d['lo'][ix],d['hi'][ix])))
  vs=float(d['cat']['vlos_systemic']);s=minimize(obj,[np.median(d['v'][ix]),math.log(9.)],bounds=[(vs-15,vs+15),(math.log(.1),math.log(100.))]);sig=float(np.exp(s.x[1]))
  def delta(logsig):
   z=minimize(lambda mu:obj([mu[0],logsig]),[s.x[0]],bounds=[(vs-15,vs+15)]);return float(z.fun-s.fun-.5)
  low=math.exp(brentq(delta,math.log(.1),s.x[1]));high=math.exp(brentq(delta,s.x[1],math.log(100.)))
  ax.errorbar(np.median(d['R'][ix]),sig,yerr=[[sig-low],[high-sig]],fmt='o',color='black',ms=4,capsize=2)
 ax.set_xscale('log');ax.set_ylim(0,max(25,1.1*ax.get_ylim()[1]));ax.set_xlim(10,max(4000,d['R'].max()));ax.set_title(name+' — '+str(len(d['R']))+' selected stars');ax.set_ylabel('Line-of-sight dispersion [km/s]');ax.set_xlabel('Circularized projected R [pc]');ax.grid(alpha=.2)
 if j==0:ax.legend(fontsize=7,loc='upper right')
 ax=axs[1,j];r=np.geomspace(10,1e5,300)
 for model,color,label in [(free,'#2166ac','Free reference'),(half,'#1b7837','Half-supply envelope')]:
  b=model['scale_pc'];m=model['cold_mass_Msun'];ax.plot(r,m*r**3/(r*r+b*b)**1.5,color=color,lw=1.8)
 ax.step(rr,np.cumsum(dm),where='post',color='#b2182b',lw=1.5);R90=meta['coverage']['R_pc_percentiles'][3];ax.axvline(R90,color='gray',ls=':',lw=1.1);ax.axvspan(R90,1e5,color='gray',alpha=.08);ax.text(.04,.94,'dotted: 90% of spectra',transform=ax.transAxes,va='top',fontsize=8);ax.set_xscale('log');ax.set_yscale('log');ax.set_ylim(1e4,1e11);ax.set_xlim(10,1e5);ax.set_xlabel('Spherical radius r [pc]');ax.set_ylabel('Complete cold M(<r) [Msun]');ax.grid(alpha=.2)
fig.suptitle('CCT018: complete envelopes vs actual positions — canonical a0, isotropic moment model\nBlack: binned conditional velocities. Sextans dashed curves: second tracer. Inverse fits are not formation or survival.',fontsize=13)
fig.tight_layout(rect=(0,0,1,.93));fig.savefig(P/'envelope_data.png',dpi=160);plt.close(fig)
