import json,os
from pathlib import Path
B=Path(__file__).resolve().parent;os.environ.setdefault('MPLCONFIGDIR',str(B/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=json.loads((B/'force002/results.json').read_text());nom=next(z for z in r['models'] if z['stellar_setting']==[.5,.7])
f,ax=plt.subplots(figsize=(8,4.6),layout='constrained')
ax.errorbar(r['r_kpc'],r['vobs'],r['errV'],fmt='o',color='#222222',ms=4,capsize=2,label='Measured rotation')
for k,col,lab in [('central','#ba4c35','Amplified central force: 25.2 km/s'),('inverse_r','#9580b8','Inverse-radius force: 12.0 km/s'),('constant_g','#087f8c','Constant acceleration: 2.54 km/s')]:
 ax.plot(r['r_kpc'],nom['models'][k]['predicted_v'],color=col,lw=2,label=lab)
ax.set(xlabel='Radius (kpc)',ylabel='Rotation speed (km/s)',title='NGC 7331: explicit extra-force fits')
ax.legend(title='Alternating-radius held-out errors',fontsize=9,title_fontsize=9,loc='lower left')
ax.spines[['top','right']].set_visible(False)
f.text(.5,-.035,'Fixed stellar M/L: disk 0.5, bulge 0.7. One galaxy; constant-force test added after free-power fit.',ha='center',fontsize=9)
f.savefig(B/'records/HC011_force.png',dpi=160,bbox_inches='tight')
