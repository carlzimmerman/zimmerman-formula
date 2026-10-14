from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
c=json.loads((p/'feedback_run_v1/calculation/history.json').read_text());d=json.loads((p/'scale_cone_run_v2/calculation/history.json').read_text())
fig,ax=plt.subplots(1,3,figsize=(12,3.6),layout='constrained');plt.rcParams.update({'font.size':10})
t=np.array(c['time']);N=np.array(c['N']);rho=np.array(c['canonical_phi_rho']);cut=t>500
com=rho[cut]*np.exp(3*(N[cut]-N[-1]));com/=com[-1]
ax[0].plot(t[cut],com,color='#11765c');ax[0].axhline(1,color='gray',ls=':',lw=1);ax[0].set(xlabel='Reference time',ylabel='a³ × scalar energy, normalized',title='Cold remnant with metric feedback')
t=np.array(d['time']);cut=t<500
ax[1].plot(t[cut],np.array(d['phi'])[cut]/2,label='Field / de Sitter field');ax[1].plot(t[cut],np.array(d['H'])[cut]/np.sqrt(.04/6),label='H / de Sitter H');ax[1].axhline(1,color='gray',ls=':',lw=1);ax[1].legend(fontsize=8);ax[1].set(xlabel='Reference time',ylabel='Normalized values',title='Approach toward stable upper branch')
ax[2].plot(t[cut],np.array(d['scalar_speed_squared'])[cut],label='Scalar diagnostic');ax[2].plot(t[cut],np.array(d['tensor_speed_squared'])[cut],label='Tensor');ax[2].axhline(1,color='black',ls=':',lw=1,label='Matter light cone');ax[2].legend(fontsize=8);ax[2].set(xlabel='Reference time',ylabel='Characteristic speed squared',title='Transient cones exceed matter speed')
fig.suptitle('Assigned models: cold production survives; stable vacuum formation has a cone cost',fontsize=12)
fig.savefig(p/'feedback.png',dpi=160)
