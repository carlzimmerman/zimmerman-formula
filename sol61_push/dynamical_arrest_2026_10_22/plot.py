from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).parent;a=json.loads((p/'run2/result.json').read_text());b=json.loads((p/'feedback_run/result.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
f,ax=plt.subplots(1,3,figsize=(13,4),layout='constrained')
x=[r['edge_pc'] for r in b['rows']];yy=[r['ufd']['mean_log_sigma'] for r in b['rows']];er=[r['ufd']['se'] for r in b['rows']]
ax[0].errorbar(x,yy,yerr=er,fmt='o-',color='#245a81',capsize=3);ax[0].axhline(0,color='gray',lw=1);ax[0].set(xlabel='Trial core edge (pc)',ylabel='Mean ln(observed / model dispersion)',title='Rotational expansion weakens dwarf support')
y=np.linspace(.05,1,400);lower=np.maximum(0,2-3*y);upper=((.95)**-2-1)/2*y
ax[1].plot(y,lower,label='Local stability boundary',color='#c86a35');ax[1].plot(y,upper,label='5% flat-speed limit (n=2)',color='#245a81');ax[1].fill_between(y,lower,upper,where=upper>lower,color='#67a88b',alpha=.35);ax[1].plot(.9,.01,'ko',ms=4);ax[1].set(xlabel='Phase ratio y = chi / chi0',ylabel='Mode coupling q',ylim=(0,.3),title='Conditional weak-drive window');ax[1].legend(fontsize=8,loc='upper right')
g=[z for z in a['growth'] if z['k']==1];ax[2].plot([z['y'] for z in g],[z['amplitude'] for z in g],'o-',color='#245a81');ax[2].axhline(1,color='gray',lw=1);ax[2].set(xlabel='Homogeneous chi / chi0',ylabel='Final growth amplitude / dust',ylim=(.91,1.005),title='Uniform phase reduction worsens growth')
f.suptitle('Dynamical-arrest diagnostics — conditional comparisons, not formation predictions',fontsize=13)
f.savefig(p/'diagnostics.png',dpi=180);f.savefig(p/'diagnostics.pdf')
