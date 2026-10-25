"""Scientific figure from completed, hashed runs; no new dynamics."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=Path(__file__).resolve().parent
scan=json.loads((p/'run_scan/results.json').read_text())['runs']
ref=json.loads((p/'run_refine/results.json').read_text())['runs']
wide=json.loads((p/'run_wide/results.json').read_text())['runs']
fig,axes=plt.subplots(1,3,figsize=(13.5,4.8),constrained_layout=True)
colors=['#007c91','#5b55ab','#b56215','#34784c']
labels=['3e5 / 0.3','1e8 / 1','6e10 / 3','1e14 / 300']
for i in range(4):
    rows=[r for r in scan if r['profile_index']==i and r['f']==.95]
    axes[0].plot(range(len(rows)),[100*r['final']['q'] for r in rows],'o-',color=colors[i],label=labels[i])
axes[0].set_xticks(range(5),['0','.1','.3','1','3'])
axes[0].set(xlabel='Common coupling strength alpha',ylabel='Final tethered mass (%)',ylim=(0,3.3))
axes[0].set_title('Strong rotation still leaves mostly free matter',fontsize=10,fontweight='bold')
axes[0].text(.03,.97,'Formation target: 95% (off scale)',transform=axes[0].transAxes,va='top',fontsize=9)
axes[0].legend(title='Mass / scale (solar masses / kpc)',fontsize=8,title_fontsize=8,frameon=False,loc='upper left',bbox_to_anchor=(.02,.88))
weak=[next(r for r in ref if r['profile_index']==i and r['f']==.3) for i in range(4)]
strong=[next(r for r in ref if r['profile_index']==i and r['f']==.95) for i in range(4)]
x=np.arange(4)
axes[1].bar(x-.17,[100*r['final']['bound_free_fraction'] for r in weak],.34,label='Weak coherence',color='#007c91')
axes[1].bar(x+.17,[100*r['final']['bound_free_fraction'] for r in strong],.34,label='Strong coherence',color='#b56215')
axes[1].set_xticks(x,labels,rotation=20,ha='right')
axes[1].set(ylabel='Snapshot-bound free mass / initial medium (%)',ylim=(0,105),xlabel='Mass / scale')
axes[1].set_title('Free matter remains abundant in both',fontsize=10,fontweight='bold')
axes[1].legend(fontsize=8,frameon=False,loc='lower left')
for row,style in zip(wide,['--','-']):
    h=row['history'];axes[2].plot([z['t'] for z in h],[100*z['q'] for z in h],style,label=f"{row['nq']} field cells")
axes[2].set(xlabel='Initial dynamical times',ylabel='Tethered mass (%)')
axes[2].set_title('Extended cold collapse: temporary conversion',fontsize=10,fontweight='bold')
axes[2].legend(fontsize=8,frameon=False)
for ax in axes:ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
fig.suptitle('Live spherical assembly: energy closes, formation target fails\nLeft: 12 shells/species; middle: refined 24 shells, alpha=.3; right: one cold case',fontsize=12)
fig.savefig(p/'results.png',dpi=180)

summary=dict(scan_cases=len(scan),scan_max_final_q=max(r['final']['q'] for r in scan),
    scan_max_energy_error=max(r['max_energy_error'] for r in scan),
    refined_max_energy_error=max(r['max_energy_error'] for r in ref),
    refined=[dict(profile_index=r['profile_index'],f=r['f'],**r['final']) for r in ref],
    wide=[dict(nq=r['nq'],**r['final']) for r in wide])
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
