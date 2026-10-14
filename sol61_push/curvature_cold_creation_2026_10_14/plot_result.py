from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
h=json.loads((p/'mode_run_v1/calculation/history.json').read_text());r=json.loads((p/'mode_run_v1/calculation/results.json').read_text())
t=np.array(h['time']);N=np.array(h['N_relative_transition']);rho=np.array(h['canonical_rho']);G=np.array(h['GB']);plt.rcParams.update({'font.size':10})
fig,ax=plt.subplots(1,3,figsize=(12,3.5),layout='constrained')
cut=t<=60
ax[0].plot(t[cut],G[cut],color='#3454a4');ax[0].axhline(0,color='gray',lw=.7);ax[0].set(xlabel='Time in initial Hubble units',ylabel='Gauss–Bonnet curvature / initial H⁴',title='Assigned curvature changes sign',yscale='symlog');ax[0].axvline(30,color='gray',ls=':',lw=1)
cut=N>=0;com=rho[cut]*np.exp(3*(N[cut]-N[-1]));com/=com[-1]
ax[1].plot(N[cut],com,color='#128260');ax[1].axhline(1,color='gray',ls=':',lw=1);ax[1].set(xlabel='ln(a / a at transition)',ylabel='a³ × canonical scalar energy, normalized',title='Late energy approaches dust scaling',yscale='log')
rr=r['rows'][1:];ax[2].loglog([v['k_physical_at_transition_over_H_initial'] for v in rr],[v['late_free_isotropic_mode_w'] for v in rr],'o-',color='#ad5c23');ax[2].set(xlabel='Mode momentum at transition / initial H',ylabel='Late free-mode pressure / energy',title='Short modes still carry pressure')
fig.suptitle('Curvature-triggered scalar example — supplied seed and prescribed background',fontsize=12)
fig.savefig(p/'creation.png',dpi=160)
