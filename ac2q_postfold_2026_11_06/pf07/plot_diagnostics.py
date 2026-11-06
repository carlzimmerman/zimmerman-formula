from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
fig,ax=plt.subplots(2,1,figsize=(8,6),sharex=True,constrained_layout=True)
for n,names,color in [(127,['chunk127_m255_t1','chunk127_14'],'#3366aa'),(255,['chunk255_05','chunk255_10','chunk255_14'],'#cc6611')]:
 rows=[]
 for name in names:rows.extend(json.loads((p/name/'result.json').read_text())['records'])
 times=[r['time']for r in rows];grads=[r['q_gradient']for r in rows];res=[r['raw_momentum_normalized']for r in rows]
 ax[0].plot(times,grads,label=f'{n} represented points',color=color)
 ax[1].semilogy(times,[max(x,1e-17)for x in res],color=color)
 for a,ys in zip(ax,[grads,res]):a.plot(times[-1],ys[-1],'x',color=color,ms=8,mew=2)
ax[0].set_ylabel(r'max $|\partial_x q|$');ax[0].legend();ax[0].set_title('Coupled AC2q fixture: steepening before the accuracy limit')
ax[1].axhline(1e-7,color='black',ls='--',lw=1,label='declared stopping threshold');ax[1].set_ylabel('Raw momentum residual\n(normalized)');ax[1].set_xlabel('Scalar-clock time (dimensionless)');ax[1].legend(loc='lower right')
for a in ax:a.grid(alpha=.2)
fig.suptitle('Crosses mark numerical stops, not physical singularities',fontsize=10)
fig.savefig(p/'evolution_diagnostics.png',dpi=170);fig.savefig(p/'evolution_diagnostics.pdf')
