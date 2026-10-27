"""Plot final-branch evidence; two-seed spans are not confidence intervals."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=Path(__file__).resolve().parent
rows=json.loads((p/'run_analysis_final/results.json').read_text())['rows']
fig,axes=plt.subplots(1,3,figsize=(14,4.8),constrained_layout=True)
x=np.arange(4);colors={0.:'#007c91',.95:'#b56215'}
for branch,sources,style in [('Reversible',('scan_v4','seed_v4'),'--'),('Radiative',('radiative','radiative_seed'),'-')]:
    for f in (0.,.95):
        values=[[100*r['final']['q'] for r in rows if r['source'] in sources and r['profile_index']==i and r['f']==f and r['flat']==.25] for i in range(4)]
        means=np.array([np.mean(v) for v in values]);lo=means-np.array([min(v) for v in values]);hi=np.array([max(v) for v in values])-means
        axes[0].errorbar(x,means,yerr=[lo,hi],fmt='o'+style,color=colors[f],capsize=3,
                        label=branch+(' / rotating' if f else ' / unordered'))
axes[0].set_title('Formation is modest in both kinematics',fontsize=11,fontweight='bold')
axes[0].set(ylabel='Final tethered mass (%)',ylim=(0,40))
axes[0].legend(fontsize=8,frameon=False,loc='upper right')
axes[0].text(.02,.97,'95% target\n(off scale)',transform=axes[0].transAxes,va='top',fontsize=9)
for f in (0.,.95):
    vals=[[100*r['final']['bound_free_fraction'] for r in rows if r['source'] in ('radiative','radiative_seed') and r['profile_index']==i and r['f']==f] for i in range(4)]
    means=np.array([np.mean(v) for v in vals])
    axes[1].errorbar(x,means,yerr=[means-np.array([min(v) for v in vals]),np.array([max(v) for v in vals])-means],
                     fmt='o-',color=colors[f],capsize=3,label='Rotating' if f else 'Unordered')
axes[1].axhline(90,color='#777777',linestyle=':',label='Illustrative 90% gate')
axes[1].set(ylabel='Snapshot-bound F / initial medium (%)',ylim=(70,100))
axes[1].set_title('Radiative branch: substantial free reservoir',fontsize=11,fontweight='bold')
axes[1].legend(fontsize=8,frameon=False,loc='lower left')
for ax in axes[:2]:
    ax.set_xticks(x,['3e5','1e8','6e10','1e14']);ax.set_xlabel('Initial baryon mass (solar masses)')
long=json.loads((p/'run_radiative_long/results.json').read_text())['runs']
for r in long:
    h=r['history'];color='#5b55ab' if r['profile_index']==1 else '#34784c'
    label=('1e8' if r['profile_index']==1 else '6e10')+(' rotating' if r['f'] else ' unordered')
    axes[2].plot([z['t'] for z in h],[100*z['q'] for z in h],color=color,linestyle='-' if r['f'] else '--',label=label)
axes[2].set(xlabel='Initial dynamical times',ylabel='Tethered mass (%)',ylim=(0,40))
axes[2].set_title('Longer radiative runs do not separate',fontsize=11,fontweight='bold')
axes[2].legend(fontsize=8,frameon=False,loc='upper left')
for ax in axes:ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.suptitle('Local reactions and separate 3D transport; monopole tether field\nLeft/middle: two-seed ranges at four dynamical times, 32 packets/component; no observational fit',fontsize=12)
fig.savefig(p/'results.png',dpi=180)
