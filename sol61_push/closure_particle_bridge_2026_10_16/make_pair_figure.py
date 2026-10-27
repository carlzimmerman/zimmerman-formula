"""Render the declared reduced-model comparison; no extra scientific fit."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

p=Path(__file__).parent
r=json.loads((p/'pair_conversion_run_004/results.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(11,4.3),layout='constrained')
for t,color in ((.3,'#137d68'),(1.,'#225db0'),(3.,'#b06b12')):
    on=next(z for z in r['runs'] if z['initial_Tdark_over_m']==t and z['pair_enabled'])
    off=next(z for z in r['runs'] if z['initial_Tdark_over_m']==t and not z['pair_enabled'])
    x=np.array([s['T_visible_GeV']*1e6 for s in on['samples']])
    y=np.array([s['weighted_yield_ratio'] for s in on['samples']])
    temperature=np.array([s['T_dark_GeV'] for s in on['samples']])
    temperature_off=np.array([s['T_dark_GeV'] for s in off['samples']])
    style='--' if t==3 else '-'
    label=f'Initial dark T / m = {t:g}'
    if t==3: label+=' (dilution gate failed)'
    axs[0].plot(x,y,style,color=color,lw=2,label=label)
    axs[1].plot(x,temperature/temperature_off,style,color=color,lw=2)
axs[0].axhline(1,color='#777777',lw=1,ls=':')
axs[1].axhline(1,color='#777777',lw=1,ls=':')
for ax in axs:
    ax.set_xscale('log');ax.set_xlim(1e4,1)
    ax.set_xlabel('Visible temperature (keV)')
    ax.spines[['top','right']].set_visible(False)
    ax.grid(alpha=.15)
axs[0].set_ylabel('Weighted count / initial weighted count')
axs[1].set_ylabel('Dark temperature: pair on / pair off')
axs[0].set_title('Pair conversion changes the final daughter count')
axs[1].set_title('Rest mass and kinetic energy exchange')
axs[0].legend(fontsize=8,loc='upper right')
fig.suptitle('Specified initial states, m = 2 MeV; reduced classical model',fontsize=13)
fig.savefig(p/'pair_conversion_comparison.png',dpi=180)
print(p/'pair_conversion_comparison.png')
