from pathlib import Path
import json,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/ac2q-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
fig,ax=plt.subplots(figsize=(8,4.5))
for n,keys in [(511,['r511']),(1023,['r1023_a']),(2047,['r2047_a','r2047_b']),(4095,['r4095_a','r4095_b','r4095_c','r4095_d'])]:
 rows=[]
 for key in keys:
  d=json.loads((p/key/'result.json').read_text());rows+=d['records'][:-1] if d['status']=='stopped' else d['records']
 rows=sorted({round(r['time'],10):r for r in rows}.values(),key=lambda r:r['time'])
 ax.plot([r['time']for r in rows],[r['q_gradient']for r in rows],label=f'{n:,} points')
 ax.plot(rows[-1]['time'],rows[-1]['q_gradient'],'o',ms=4,color=ax.lines[-1].get_color())
ax.set(xlim=(1.1,1.49),ylim=(0,7),xlabel='Dimensionless time',ylabel='Peak charge gradient',title='Coupled steepening under spatial refinement')
ax.grid(alpha=.2);ax.legend();fig.text(.5,.015,'Dots mark last accepted steps before accuracy stops—not physical singularities.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.04,1,1));fig.savefig(p/'refinement.png',dpi=170)
