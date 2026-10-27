from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
load=lambda d:{r['label']:r for r in json.loads((p/d/'result.json').read_text())['rows']}
l=load('long_run');f=load('refine_run');s=load('survey_run');M=.08408132497418408;tu=.012074272908402984
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,3,figsize=(13,4),layout='constrained')
x=np.array([.5,1,2,4]);y=[l['long_'+str(v)]['rows'][-1]['masses'][3]/M for v in [.5,1,2,4]]
ax[0].plot(x,x,'--',color='gray',label='All supplied mass');ax[0].plot(x,y,'o-',color='#245a81',label='At 1.45 Gyr');ax[0].plot(4,f['mass4_strong_fine']['rows'][-1]['masses'][3]/M,'s',color='#c86a35',label='Refined heavy run');ax[0].axhline(1,color='#67a88b',ls=':',label='Canonical mass');ax[0].set(xlabel='Initial mass / canonical mass',ylabel='Mass inside 0.88 kpc / canonical mass',title='No common central mass');ax[0].legend(fontsize=8)
for z,lab,col in [(l['long_4'],'256 cells','#245a81'),(f['mass4_strong_fine'],'512 cells','#c86a35')]:
 ax[1].plot([q['time']*tu for q in z['rows']],[100*q['removed']/abs(z['initial_energy']) for q in z['rows']],label=lab,color=col)
ax[1].set(xlabel='Time (Gyr)',ylabel='Absorbed field energy / initial |E| (%)',title='Energy escapes; material mostly remains');ax[1].legend(fontsize=8)
for z,lab,col in [(s['baseline_1_0.02'],'256 cells','#999999'),(s['fine_grid'],'512 cells','#c86a35'),(f['ultrafine'],'1024 cells','#245a81')]:
 rr=np.sort(abs(np.array(z['final_r'])));ax[2].step(rr*.4404221297174536,np.arange(1,len(rr)+1)/len(rr),where='post',label=lab,color=col)
ax[2].set(xlabel='Radius (kpc)',ylabel='Enclosed fraction of initial mass',title='Instantaneous inner profile unresolved',xlim=(0,.9));ax[2].legend(fontsize=8)
fig.suptitle('Conditional radial collapse — bulk results survive refinement; precise dwarf profiles do not',fontsize=13)
fig.savefig(p/'collapse_diagnostics.png',dpi=180);fig.savefig(p/'collapse_diagnostics.pdf')
