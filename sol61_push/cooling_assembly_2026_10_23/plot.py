import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;r=json.loads((p/'endpoint/result.json').read_text())['records']
fig,ax=plt.subplots(figsize=(9,5.5))
for z,f in [(10,2),(20,1),(20,2),(30,1),(30,2)]:
 a=[x for x in r if x['z']==z and x['factor']==f];line,=ax.loglog([x['M'] for x in a],[x['cooling_Gyr']/x['age_Gyr'] for x in a],alpha=.45,label=f'z={z}, frequency={f} x dynamical')
 w=[x for x in a if x['weak']];ax.scatter([x['M'] for x in w],[x['cooling_Gyr']/x['age_Gyr'] for x in w],s=14,color=line.get_color())
ax.axhline(1,color='black',ls='--',label='Efficiency time equals cosmic age')
ax.set(xlabel='Gaussian source mass (solar masses)',ylabel='Prescribed radiation efficiency time / cosmic age',title='Cosmological size scaling: weak-source radiation is too slow')
ax.legend(fontsize=8,loc='upper left');ax.grid(alpha=.2);fig.text(.5,.01,'Dots pass static weak-field criteria; lines include unsupported cases. 10% prescribed radius oscillations.',ha='center',fontsize=8);fig.tight_layout(rect=(0,.035,1,1));fig.savefig(p/'cooling.png',dpi=170)
