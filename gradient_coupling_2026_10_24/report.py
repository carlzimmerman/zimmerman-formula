import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(__file__).parent;dest=Path(a.output);rows=[]
for directory in ['run_checked','run_intermediate','run_confined_checked']:
 for r in json.loads((p/directory/'results.json').read_text())['runs']:
  rad=np.array(r['r']);q=np.array(r['q']);mass=np.array(r['mass']);R=r['interpolated_crossings_kpc'][-1] if r['interpolated_crossings_kpc'] else 0;edges=[0.]
  for rr in rad:edges.append(2*rr-edges[-1])
  rho=mass/(np.diff(np.array(edges)**3)/3);sel=(rad>15)&(rad<R);rv=rho[sel];reb=float(max(rv/np.minimum.accumulate(rv))) if len(rv) else None;ee=np.log10(np.array(r['g_total'])/r['g_law']);ee=np.r_[ee[(rad>=1.5)&(rad<=50)],np.interp(50,rad,ee),np.interp(1.5,rad,ee)]
  rows.append(dict(source=directory,L=r['density_stiffness_length_kpc'],eta=r['eta'],charge=r['charge'],boundary_crossings=r['interpolated_crossings_kpc'],law_error_dex=float(max(abs(ee))),law_error_fraction=float(max(abs(10**ee-1))),mass_outside50_volume=r['mass_outside50'],allowed_outside50=.5624206540876635,density_rebound=reb,min_cell_mass=r.get('min_transition_cell_mass'),exterior_T_fraction=r['explicit_exterior_T_fraction'],exterior_mass=r['explicit_exterior_mass'],density_KKT=r['density_KKT_max'],optimizer=r['optimizer']))
 continuation=json.loads((p/'run_continue/results.json').read_text());audit=json.loads((p/'run_audit/results.json').read_text());out={'status':'No combined success. Inward redistribution demonstrated, original-law and resolved material-support requirements still fail.','screen':rows,'restoration':[dict(n=r['n'],displacement=r['displacement_kpc'],front_change=r['front_change_kpc'],energy_change=r['energy_difference'],law_error_dex=r['law_endpoint_error_dex'],support=r['support'],density_KKT=r['density_KKT_max']) for r in continuation['runs'] if r['stage']=='recovery'],'force_audit':audit,'limitations':['Supplied charge; no production or microscopic coefficient derivation','Fixed baryons and spherical symmetry; no observational fit or physical dynamics','Finite-grid local restoring Hessian does not override failed refinement','Volume mass reconstruction differs from midpoint force quadrature at finite resolution']};dest.write_text(json.dumps(out,indent=2)+'\n')
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False});fig,ax=plt.subplots(1,3,figsize=(13,4))
for n,col in [(96,'#137e8a'),(144,'#b45a28')]:
 r=[r for r in continuation['runs'] if r['n']==n and r['stage']=='base'][0];rad=np.array(r['r']);mass=np.array(r['mass']);edges=[0.]
 for rr in rad:edges.append(2*rr-edges[-1])
 rho=mass/(np.diff(np.array(edges)**3)/3);ax[0].semilogy(rad,np.maximum(rho,1e-16),color=col,label=f'n={n}');ax[1].plot(rad,r['q'],color=col);ax[2].plot(rad,np.array(r['g_total'])/r['g_law'],color=col)
ax[0].set(xlim=(15,220),ylim=(1e-13,1e-4),xlabel='Radius (kpc)',ylabel='Density (Mb / kpc³, 4π absorbed)',title='Refinement exposes depleted interval');ax[0].legend();ax[1].set(xlim=(15,220),xlabel='Radius (kpc)',ylabel='Converted fraction',title='Boundary shifts 122 → 176 kpc');ax[2].axhline(1,color='black',lw=.7);ax[2].set(xlim=(1.5,50),xlabel='Radius (kpc)',ylabel='Actual gravity / original law',title='Original-law deficit remains');fig.tight_layout();fig.savefig(dest.with_name('refinement.png'),dpi=170);plt.close(fig);print(json.dumps({'status':out['status'],'cases':len(rows),'restoration_trials':len(out['restoration'])}))
