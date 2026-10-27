import os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/cpb_mpl_config')
import json,hashlib,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;r=p/'nonlinear_charge_clumping_run_001'
d=json.loads((r/'results.json').read_text());coarse=np.load(r/'final_N256_dt0.005.npz');fine=np.load(r/'final_N512_dt0.005.npz');large=np.load(r/'final_N256_dt0.01.npz')
spatial=float(np.linalg.norm(abs(coarse['psi'])**2-abs(fine['psi'][::2])**2)/np.linalg.norm(abs(fine['psi'][::2])**2))
temporal=float(np.linalg.norm(abs(coarse['psi'])**2-abs(large['psi'])**2)/np.linalg.norm(abs(large['psi'])**2))
fig,ax=plt.subplots(1,3,figsize=(13,3.6),layout='constrained')
last=d['runs'][-1];I0=last['initial_I'];phaseI=2*I0
ax[0].plot(fine['x'],abs(fine['psi'])**2/I0,label='512 cells',lw=1.8)
ax[0].plot(coarse['x'],abs(coarse['psi'])**2/I0,'--',label='256 cells',lw=1)
ax[0].axhline(2,color='grey',ls=':',label='coexistence density')
ax[0].set(xlim=(0,40),xlabel=r'$x\,m_h$',ylabel=r'$|\Psi|^2/I_{\rm initial}$',title='Final nonlinear density, t=220')
ax[0].legend(fontsize=8)
for row in d['runs']:
 t=np.array([s['t'] for s in row['samples']]);amp=np.array([s['density_mode_fraction'] for s in row['samples']]);err=np.abs(np.array([s['energy'] for s in row['samples']])/row['samples'][0]['energy']-1)
 label=str(row['nodes'])+' cells, dt='+str(row['dt'])
 ax[1].semilogy(t,amp,label=label,lw=1)
 ax[2].semilogy(t,np.maximum(err,1e-16),label=label,lw=1)
ax[1].set(xlabel=r'$t\,m_h$',ylabel='Seed-mode density fraction',title='Growth enters nonlinear regime',ylim=(1e-4,4))
ax[2].set(xlabel=r'$t\,m_h$',ylabel=r'$|E/E_0-1|$',title='Discrete energy conservation',ylim=(1e-12,1e-5))
ax[2].legend(fontsize=8)
fig.suptitle('Specified charged scalar state: 1D periodic diagnostic, not isolated 3D droplets',fontsize=11)
output=p/'NONLINEAR_CLUMPING.png';fig.savefig(output,dpi=170);plt.close(fig)
summary={'input_run':'nonlinear_charge_clumping_run_001','spatial_final_density_relative_L2':spatial,'temporal_final_density_relative_L2':temporal,'fine_final_peak_I_over_initial':float(np.max(abs(fine['psi'])**2)/I0),'fine_final_min_I_over_initial':float(np.min(abs(fine['psi'])**2)/I0),'fine_final_peak_I_over_coexistence':float(np.max(abs(fine['psi'])**2)/phaseI),'figure':output.name,'figure_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'input_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in r.glob('*') if f.suffix in ['.json','.npz']},'software':{'NumPy':np.__version__,'Matplotlib':matplotlib.__version__},'scope':'Postprocessing/aligned sample comparison only; no continuum, late asymptotic or 3D formation proof'}
(p/'clumping_figure_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='input_hashes'},indent=2))
