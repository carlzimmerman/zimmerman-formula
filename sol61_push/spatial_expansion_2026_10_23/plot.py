import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;fig,axes=plt.subplots(1,2,figsize=(10,4))
for name,label in [('strong','8 cubed'),('strong_space','12 cubed'),('strong_fine','16 cubed')]:
 r=json.loads((p/name/'result.json').read_text())['rows'];axes[0].loglog([x['z'] for x in r],[x['contrast_c_max'] for x in r],label=label)
for name,label in [('base','start z=1100'),('early','start z=2200'),('earlier','start z=4400')]:
 r=json.loads((p/name/'result.json').read_text())['rows'];axes[1].loglog([x['z'] for x in r],[x['contrast_c_max'] for x in r],label=label)
for ax in axes:ax.invert_xaxis();ax.set_xlabel('Redshift z');ax.set_ylabel('Peak cold density contrast');ax.grid(alpha=.2);ax.legend(fontsize=8)
axes[0].set_title('3% seeds: peak not spatially converged');axes[1].set_title('Weak seeds: preparation history matters');fig.tight_layout();fig.savefig(p/'diagnostics.png',dpi=160)
