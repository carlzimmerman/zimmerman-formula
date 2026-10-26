import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
b=Path(__file__).resolve().parent
fig,ax=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for basis,labels in [('130 states',['wall_h05','wall_h025','wall_h0125']),('192 states',['ry3_h05','ry3_h025'])]:
 rows=[json.loads((b/('run_'+s)/'results.json').read_text()) for s in labels]
 ax[0].loglog([d['settings']['h'] for d in rows],[d['rows'][1]['ground_to_other'] for d in rows],'o-',label=basis)
ax[0].set(xlabel='Radial spacing h',ylabel='Neutral ground-to-other probability',title='Mesh improves; electronic basis still matters')
ax[0].legend();ax[0].grid(alpha=.2)
d=json.loads((b/'run_ion/results.json').read_text())['rows'][-1];levels=d['bound_energies'];gaps=[x-levels[0] for x in levels]
for i,g in enumerate(gaps):ax[1].hlines(g,0,1,color='black');ax[1].text(1.02,g,f'v={i}',va='center')
for e,c in [(.001,'tab:blue'),(.05,'tab:orange')]:ax[1].axhline(e,color=c,ls='--',label=f'Incident {e}')
ax[1].axhline(d['atomic_threshold']-levels[0],color='red',ls=':',label='Ionic dissociation')
ax[1].set(xlim=(0,1.4),xticks=[],ylabel='Energy above ionic v=0',title='Only some ionic channels are open')
ax[1].legend(loc='upper left',fontsize=8)
fig.suptitle('Convergence and threshold diagnostics — no DR rate or galaxy-selection result',fontsize=11)
fig.savefig(b/'evidence.png',dpi=170);fig.savefig(b/'evidence.pdf')
