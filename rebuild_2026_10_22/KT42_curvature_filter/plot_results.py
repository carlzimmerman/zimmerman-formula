"""Plot frozen, finite diagnostic samples; connecting lines are guides only."""
import json
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/kt34_matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
read=lambda p:json.loads((HERE/p).read_text())
s=read('solar/run_002/results.json')
m=read('mw/refine_001/results.json')
d=read('dwarf/run_001/results.json')
fig,axes=plt.subplots(1,3,figsize=(14,5.2))
for foot,color,ls in [('canonical','#2166ac','-'),('alt','#d6604d','--')]:
    rows=s['footings'][foot]['rows']
    x=[float(k)*1000 for k in rows];y=[r['fine']['x_ceiling'] for r in rows.values()]
    axes[0].plot(x,y,'o',color=color,linestyle=ls,ms=4,label=foot)
    rows=[r for r in m['cases'] if r['footing']==foot]
    axes[1].plot([r['width_kpc']*1000 for r in rows],[min(r['profile_R12']['gz']) for r in rows],'o',color=color,linestyle=ls,ms=4)
    rows=[r for r in d['summaries'] if r['footing']==foot and r['name']=='Draco']
    axes[2].plot([r['width_kpc']*1000 for r in rows],[r['variance'] for r in rows],'o',color=color,linestyle=ls,ms=4)
axes[0].set_yscale('log');axes[0].axhline(1,color='#333333',lw=1)
axes[0].set_title('Solar screening disappears',fontsize=11);axes[0].set_ylabel(r'$|Q_2|$ / unchanged Cassini ceiling')
axes[1].axhline(0,color='#333333',lw=1);axes[1].set_title('MW force needs much wider smoothing',fontsize=11)
axes[1].set_ylabel('Minimum sampled vertical derivative\n'+r'[(km/s)$^2$/kpc]')
axes[2].axhline(0,color='#333333',lw=1);axes[2].axhline(6.7**2,color='#777777',lw=1,ls=':')
axes[2].text(.2,46,'6.7 km/s comparison floor',fontsize=8,color='#555555')
axes[2].set_ylim(-32,50);axes[2].set_title('Draco still misses the scalar screen',fontsize=11)
axes[2].set_ylabel(r'$W/(3M)$  [(km/s)$^2$]')
for ax in axes:
    ax.set_xscale('symlog',linthresh=.1,linscale=.4)
    ax.set_xticks([0,.1,1,10,100,1000],['0','0.1','1','10','100','1000'])
    ax.set_xlim(-.02,1300)
    ax.set_xlabel('Curvature smoothing width a [pc]')
    ax.grid(alpha=.16);ax.spines[['top','right']].set_visible(False)
axes[0].legend(frameon=False)
fig.suptitle('KT42: fixed baryons and cuts; sampled widths, not a continuous exclusion',fontsize=13,y=.98)
fig.subplots_adjust(left=.06,right=.99,bottom=.22,top=.86,wspace=.32)
fig.text(.5,.015,'MW: R=12 kpc, z=0.02–1.5 kpc. Solar: uniform external field. Draco: Υ=2, η=0.01. Lines guide the eye.',ha='center',fontsize=9)
fig.savefig(HERE/'scale_conflict.png',dpi=180)
fig.savefig(HERE/'scale_conflict.pdf')
