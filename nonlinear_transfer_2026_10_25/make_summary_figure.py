"""Plot recorded evidence only; no dynamics or model fitting."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;c=p.parent/'compression_current_2026_10_25'
def get(root,name):return json.loads((root/name/'results.json').read_text())
plus=get(p,'run_physical_boundary_plus');minus=get(p,'run_physical_boundary_minus');infall=get(p,'run_flux_infall_fine');eq=get(p,'run_exact_equilibrium');weak=get(c,'run_continue_weak');matched=get(c,'run_continue_matched');fig,ax=plt.subplots(2,2,figsize=(11,7.5),constrained_layout=True)
for d,label in [(plus,'initial boundary +0.5 kpc'),(minus,'initial boundary −0.5 kpc')]:
 t=[v['time_Myr'] for v in d['trace']];ax[0,0].plot(t,[v['boundary_kpc'] for v in d['trace']],label=label);ax[0,1].plot(t,[v['law_error_percent'] for v in d['trace']],label=label)
ax[0,0].axhline(eq['scaled_boundary_kpc'],color='k',ls=':',label='equilibrium');ax[0,0].set(title='Released boundary perturbations',xlabel='Time (Myr)',ylabel='Boundary radius (kpc)');ax[0,0].legend(fontsize=8)
ax[0,1].set(title='Law preserved for those two disturbances',xlabel='Time (Myr)',ylabel='Maximum law error (%)');ax[0,1].legend(fontsize=8)
t=[v['time_Myr'] for v in infall['trace']];excess=infall['initial_energy']-eq['energy']
for key,label in [('net_material_to_wave_work','work into scalar'),('far_flux_energy','net through 500 kpc')]:ax[1,0].plot(t,[100*v[key]/excess for v in infall['trace']],label=label)
ax[1,0].set(title='20% core dilation: actual nonlinear infall',xlabel='Time (Myr)',ylabel='Fraction of initial excess energy (%)');ax[1,0].legend(fontsize=8)
for d,label,color in [(weak,'eta = 0.01','C0'),(matched,'eta = 1','C1')]:
 t=[v['time_Myr'] for v in d['trace']];ax[1,1].plot(t,[v['net_material_to_wave_work'] for v in d['trace']],color=color,label=label+' scalar work');ax[1,1].plot(t,[v['far_flux_energy'] for v in d['trace']],color=color,ls='--',label=label+' 500 kpc flux')
ax[1,1].set(title='New compression coupling: partial runs',xlabel='Time (Myr)',ylabel='Energy (Eunit)');ax[1,1].legend(fontsize=8);ax[1,1].ticklabel_format(axis='y',style='sci',scilimits=(-3,3))
fig.suptitle('Synthetic radial benchmark: preservation established locally; formation not established',fontsize=12)
fig.savefig(p/'evidence_summary.png',dpi=170);fig.savefig(p/'evidence_summary.pdf')
