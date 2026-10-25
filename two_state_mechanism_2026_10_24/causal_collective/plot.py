import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
d=json.loads(Path(a.input).read_text());chi=d['summary']['best_static']['chi']
fig,ax=plt.subplots(figsize=(8,4.8),layout='constrained')
for floor in (0.,1e-4,.01):
    r=next(r for r in d['static_scan'] if r['chi']==chi and r['floor']==floor)
    ax.semilogx(d['x_values'],r['residual_dex'],label=f'Lower gap / cutoff = {floor:g}',lw=2)
ax.axhspan(-.05,.05,color='green',alpha=.10,label='Illustrative +/- 0.05 dex band')
ax.axhline(0,color='black',lw=.7)
ax.set(xlabel='Target acceleration g0 / a0',ylabel='log10(predicted g / target g0)',
       title=f'Causal medium static branch: universal susceptibility {chi:.2f}')
ax.grid(alpha=.2);ax.legend(fontsize=9)
fig.text(.5,-.02,'Cold spherical, countercharge-excluded branch; medium gravity neglected. No formation or observational fit.',ha='center',fontsize=8.5)
fig.savefig(a.output,dpi=160,bbox_inches='tight')
