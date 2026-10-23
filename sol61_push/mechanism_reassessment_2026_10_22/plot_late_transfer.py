import json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
fig,axs=plt.subplots(1,2,figsize=(12,4.5),constrained_layout=True)
for run,name,label in [('late_conversion_refine_run','space48','48³'),('late_conversion_refine_run','space64','64³'),('late_conversion_96_run','space96','96³')]:
 h=np.genfromtxt(P/run/(name+'.csv'),delimiter=',',names=True);r=json.loads((P/run/'results.json').read_text());per=r['parameters']['period']
 ex=h['X_kinetic']+h['X_gradient']+h['X_potential'];ep=h['phi_gradient']+h['phi_kinetic_physical']+h['phi_potential']
 axs[0].plot(h['z']/per,1e4*(1-ex/ex[0]),label=label,lw=1.1)
 if name=='space96':
  axs[1].plot(h['z']/per,1e4*(ep-ep[0])/ex[0],label='Phi positive-energy gain')
  axs[1].plot(h['z']/per,1e4*h['interaction']/ex[0],label='Signed interaction energy')
  axs[1].plot(h['z']/per,1e4*(1-ex/ex[0]),label='Net X energy loss',color='black',lw=1.2)
for ax in axs:
 ax.axhline(0,color='grey',lw=.5);ax.set_xlabel('X oscillations');ax.set_ylabel('Fraction of initial X energy × 10⁴');ax.legend(fontsize=9);ax.grid(alpha=.2)
axs[0].set_title('Small transfer; finite-resolution comparison')
axs[1].set_title('Phi excitation includes reversible interaction energy')
fig.suptitle('Conditional high-H late window — original action, prescribed warm Phi bath',fontsize=12)
fig.savefig(P/'late_transfer.png',dpi=180)
