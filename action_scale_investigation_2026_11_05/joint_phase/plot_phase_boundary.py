"""Plot saved free-boundary solutions; no fits or solver reruns."""
from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
b=Path(__file__).resolve().parent
base=json.loads((b/'evidence/false_phase_boundary/result.json').read_text())['cases'][2]
fam=json.loads((b/'evidence/phase_source_followup/result.json').read_text())['cases']
selected=[]
for c,S in [(fam[1],.5),(base,1.),(fam[2],2.)]:
 rt=next(t for t in c['roots'] if t['runs'] and t['runs'][-1]['max_eigen_real']<0)
 selected.append((S,rt))
fig,axs=plt.subplots(2,2,figsize=(10,7),layout='constrained')
for (S,rt),color in zip(selected,['#1565c0','#7c3aed','#d97706']):
 rec=rt['runs'][-1];p=rec['profile'];r=np.array(p['r']);label=f'source × {S:g}, R ≈ {rec["R"]:.2f}'
 axs[0,0].semilogy(r,p['n'],color=color,label=label)
 axs[0,1].plot(r,np.sqrt(p['v2']),color=color,label=label)
 axs[1,0].plot([x['N'] for x in rt['runs']],[x['max_eigen_real']*1e5 for x in rt['runs']],'-o',color=color,label=f'source × {S:g}')
 axs[1,1].bar(str(S),rec['edge_v2']**2/S,color=color)
axs[0,0].set(title='Solved density and selected radius',xlabel='radius',ylabel='number density');axs[0,0].legend(fontsize=8)
axs[0,1].set(title='Circular speed: flatter outer branches',xlabel='radius',ylabel='circular speed')
axs[1,0].set(title='Moving-boundary radial modes',xlabel='radial cells',ylabel='largest Re(eigenvalue) × 10⁵');axs[1,0].legend(fontsize=8)
axs[1,1].set(title='Normalization is not universal',xlabel='prescribed source multiplier S',ylabel='edge speed⁴ / S')
for ax in axs.flat:ax.grid(alpha=.18,axis='y')
fig.suptitle('Phase-confined fluid: higher-energy interior; no imposed radius\nDimensionless examples, γ = 8, Σ = 0.2, ΔV = −0.03; radial stability only',fontsize=12)
fig.savefig(b/'phase_boundary_profiles.png',dpi=180);fig.savefig(b/'phase_boundary_profiles.pdf')
