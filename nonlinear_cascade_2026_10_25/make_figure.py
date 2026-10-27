"""Plot recorded evidence, keeping local tests separate from global evolution."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).parent
get=lambda n:json.loads((p/('run_'+n)/'results.json').read_text())
fig,ax=plt.subplots(2,2,figsize=(11,7.8),constrained_layout=True)
for n,label in [('wave_baseline150','linear resonance'),('wave_shift_half','predicted half shift'),('wave_shift_full','predicted initial shift'),('wave_omit','omit nonlinear inertia')]:
 d=get(n);t=[v['time_Myr'] for v in d['trace']];ax[0,0].plot(t,[100*v['daughter_energy_fraction'] for v in d['trace']],label=label);ax[0,1].plot(t,[100*v['escaped_fraction'] for v in d['trace']],label=label)
ax[0,0].set(title='Local mode transfer with depleted pumps',xlabel='Time (Myr)',ylabel='Daughter energy (% of initial local energy)');ax[0,1].set(title='Nonlinear phase match improves actual export',xlabel='Time (Myr)',ylabel='Absorbed outgoing energy (% of initial local energy)')
for a in ax[0]:a.legend(fontsize=8)
s=get('analyze_channel')['rows'];s=[d for d in s if d['run'] in ['wave_time','wave_omit','wave_no_daughter']];labels=['complete cubic','omit inertia','daughter source off'];parent=[100*d['spectral_estimates'][0]['parent_band_fraction'] for d in s];daughter=[100*d['spectral_estimates'][0]['daughter_band_fraction'] for d in s];x=np.arange(3);ax[1,0].bar(x,parent,label='parent pair band');ax[1,0].bar(x,daughter,bottom=parent,label='daughter pair band');ax[1,0].set(xticks=x,xticklabels=labels,ylabel='Windowed radiation signal (%)',title='Radiation spectrum at bare resonance');ax[1,0].legend(fontsize=8)
d=get('long_finer');t=[v['time_Myr'] for v in d['trace']];a=ax[1,1];a.plot(t,[v['law_error_percent'] for v in d['trace']],color='k',label='law error');a.axhline(1,color='k',ls=':',alpha=.5);a.set(title='Global reference evolution (g2 = 0)',xlabel='Time (Myr)',ylabel='Law error (%)',ylim=(0,20));b=a.twinx();b.plot(t,[v.get('density_rebound',np.nan) for v in d['trace']],color='C3',label='density rebound');b.axhline(1.05,color='C3',ls=':',alpha=.5);b.set(ylabel='Density rebound',ylim=(0,7));b.yaxis.label.set_color('C3');a.legend(loc='upper left',fontsize=8);b.legend(loc='lower right',fontsize=8)
fig.suptitle('Local CC transfer and nonlinear phase matching; global formation remains unestablished',fontsize=12)
fig.savefig(p/'cascade_evidence.png',dpi=170);fig.savefig(p/'cascade_evidence.pdf')
