import json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
j=json.loads((p/'run_v1/results.json').read_text());q=j['primary'];rows=q['rows'];z=np.array([r['z'] for r in rows])
fig,axes=plt.subplots(1,2,figsize=(11,4.7),layout='constrained')
a=axes[0]
a.plot(z,[r['a0_density_ratio'] for r in rows],'-o',color='#2374ab',label='Vacuum-density law')
a.plot(z,[r['a0_event_ratio_if_normalized_today'] for r in rows],'-o',color='#c36b22',label='Inverse event-horizon radius')
a.axhline(1,color='#888',ls=':',lw=1)
a.set(xlabel='Redshift',ylabel='Acceleration scale / its value today',title='Different mechanisms give opposite evolution')
a.annotate('1.440',xy=(2,1.4399),xytext=(2.12,1.39),fontsize=10,color='#c36b22')
a.annotate('0.850',xy=(2,.8499),xytext=(2.12,.86),fontsize=10,color='#2374ab')
a.grid(alpha=.2);a.legend(fontsize=9,loc='upper left')
b=axes[1];B0=q['Omega_b_projected'];C0=q['Omega_c_projected'];R0=C0/B0
b.plot(z,[r['cold_over_surviving_baryon'] for r in rows],'-o',color='#8f466b',label='Conversion from baryons alone')
b.axhline(R0,color='#277d63',lw=2,label='Equal fractional conversion of both')
b.plot(z,[R0-(1-r['baryon_survival']) for r in rows],'-o',color='#777',label='Conversion from cold matter alone')
b.set(xlabel='Redshift',ylabel='Global cold / surviving baryonic mass',title='Same expansion, different source partitions')
b.grid(alpha=.2);b.legend(fontsize=8.5,loc='upper right')
fig.suptitle('Conserved MD14 background comparison — assigned inputs, no new data fit',fontsize=12)
fig.savefig(sys.argv[1],dpi=170)
