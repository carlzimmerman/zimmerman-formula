"""Display the saved finite evidence; no additional model fitting."""
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='polarization-mpl-'))
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
def load(name):
    return json.loads((HERE/name/'results.json').read_text())
screen=load('screen')
verify=load('verify')
contraction=load('contraction')
zero=load('zero_initial')
cases=[('Abrupt compact source',screen['rows'][0],'#a64146'),
       ('Gradual source growth',verify['rows'][0],'#b77f14'),
       ('Contraction: prepared fields',contraction['rows'][1],'#217858'),
       ('Contraction: zero fields',zero['rows'][1],'#315daa')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,2,figsize=(13.2,5.7),gridspec_kw={'width_ratios':[1.25,1]})
for name,row,color in cases:
    samples=[s for s in row['samples'] if s['time']>=row['T']]
    time=[s['time']-row['T'] for s in samples]
    error=[100*s['force_rms_fractional_error'] for s in samples]
    ax[0].plot(time,error,label=name,color=color,lw=2)
    force=row.get('force',row.get('late_force',[None])[-1])
    ax[1].plot(row['r'],np.array(force)/np.array(row['target']),color=color,lw=2)
ax[0].axhline(10,color='#555555',ls='--',lw=1)
ax[0].text(8,11.5,'Predeclared 10% gate',color='#555555',fontsize=10)
ax[0].set_yscale('log')
ax[0].set(xlabel='Time since assembly ended (dimensionless)',ylabel='RMS force error on r = 2–20 (%)',xlim=(0,640))
ax[0].legend(frameon=False,fontsize=9,loc='lower left')
ax[0].grid(axis='y',alpha=.16,which='major')
ax[1].axhline(1,color='#555555',ls='--',lw=1)
ax[1].set(xlabel='Radius (dimensionless)',ylabel='Final force / static target',xlim=(2,20))
ax[1].grid(axis='y',alpha=.16)
fig.suptitle('Assembly history changes the polarization response',x=.075,ha='left',fontsize=18,fontweight='bold')
fig.text(.075,.905,'Existing effective model • prescribed baryon motion • no added drag',fontsize=11,color='#555555')
fig.text(.075,.025,'Finite simulation evidence. The kernel is imposed; physical timescales, live baryons and relativistic lensing remain open.',fontsize=10,color='#555555')
fig.subplots_adjust(top=.82,bottom=.15,left=.075,right=.98,wspace=.27)
fig.savefig(HERE/'assembly_result.png',dpi=170,facecolor='white')
