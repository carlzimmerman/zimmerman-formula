"""Plot recorded results; does not rerun or fit a model."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=Path(__file__).resolve().parent
def load(name):return json.loads((p/name/'results.json').read_text())
pilot=next(r for r in load('run_pilot')['runs'] if r['profile']==1 and r['f']==.95 and r['alpha']==10 and r['iota']==.1)
diffuse=next(r for r in load('run_diffuse')['runs'] if r['f']==.95 and r['alpha']==3 and r['iota']==.1 and r['scale']==30)
gate=next(r for r in load('run_contraction')['runs'] if r['f']==.95 and r['alpha']==3 and r['iota']==.1)
transport=load('run_stiff3')
fig,axs=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={'width_ratios':[2.2,1]})
colors=['#68869b','#559d91','#df9637','#9b5d8c']
for (label,row),c in zip([('Bound halo + inertial pump',pilot),('Diffuse reservoir',diffuse),('Contraction-built protection',gate),('Plus angular transport',transport)],colors):
    h=row['history'];axs[0].plot([v['t'] for v in h],[100*v['q'] for v in h],label=label,color=c,lw=1.8)
axs[0].axhline(95,color='#333',ls='--',lw=1,label='Declared formation target')
axs[0].set(xlim=(0,12),ylim=(0,102),xlabel='Initial baryon dynamical times',ylabel='Tethered mass (%)',title='No persistent tethered state in these trajectories')
axs[0].legend(fontsize=8,loc='upper right');axs[0].grid(alpha=.15)
b=next(r for r in load('run_bound')['runs'] if r['n']==12 and r['profile']==1 and r['dark_scale']==3)
axs[1].hlines(b['initial_energy'],0,1,color='#333',lw=3)
axs[1].hlines(b['energy_lower_bound'],0,1,color='#a53c3c',lw=3)
axs[1].annotate('',xy=(.5,b['energy_lower_bound']),xytext=(.5,b['initial_energy']),arrowprops=dict(arrowstyle='<->',color='#a53c3c'))
axs[1].text(.03,b['initial_energy']-.06,'Available total energy',fontsize=9)
axs[1].text(.03,b['energy_lower_bound']+.04,'Lower bound at q = 75%',fontsize=9)
axs[1].set(xlim=(0,1),ylim=(-1.5,-.4),xticks=[],ylabel='Energy / (G Mb² / b)',title='Fixed-protection obstruction')
axs[1].text(.5,-1.43,'Bound initial halo only\nFixed individual angular momenta',ha='center',fontsize=8)
fig.suptitle('Formation/transition checkpoint — conditional toy models, not galaxy fits',fontsize=12)
fig.tight_layout();fig.savefig(p/'checkpoint.png',dpi=160)
