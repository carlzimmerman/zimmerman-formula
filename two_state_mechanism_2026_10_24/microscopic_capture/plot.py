import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
d=json.loads(Path(a.input).read_text());rows=d['ratios']
fig,ax=plt.subplots(figsize=(8,5),layout='constrained')
for j,label in enumerate(['3e5 Msun / 0.3 kpc','1e8 Msun / 1 kpc','1e14 Msun / 300 kpc']):
    ax.loglog([r['alpha'] for r in rows],[r['disk_over_others'][j] for r in rows],label='Relative to '+label,lw=2)
ax.axhline(16,color='black',ls='--',label='Required for 80% versus 20% bound')
ax.set(xlabel='Universal dark coupling alpha_D',ylabel='Formation exposure ratio: 6e10 Msun / 3 kpc to other',
       title='Atomic ground-state channel: insufficient dwarf separation')
ax.grid(alpha=.2,which='both');ax.legend(fontsize=9,loc='upper left')
fig.text(.5,-.015,'Fixed-temperature, radiative-only proxy; common age and mass ratio. No tether field or live gravity.',ha='center',fontsize=9)
fig.savefig(a.output,dpi=160,bbox_inches='tight')
