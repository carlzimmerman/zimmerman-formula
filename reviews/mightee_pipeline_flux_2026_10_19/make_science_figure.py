"""Compact view of the four original science galaxies from saved common-bin profiles."""
from pathlib import Path
import json,hashlib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
d=pd.read_csv(HERE/'stage_run/plot_profiles.csv');pairs=pd.read_csv(HERE/'stage_run/paired_fluxes.csv');pairs=pairs[pairs.science47]
fig,axes=plt.subplots(2,2,figsize=(11,7),sharex=True)
for ax,(_,r) in zip(axes.flat,pairs.iterrows()):
    for key,color,label in [('a','black','ALFALFA'),('pre','#ad267d','Before final subtraction'),('post','#1678b5','After final subtraction')]:
        q=d[(d.ID==r.ID)&(d.stage==key)];ax.step(q.velocity_center,q.flux_mjy,where='mid',color=color,label=label,lw=1.3)
    ax.set_title(r.ID+f'\nMIGHTEE / ALFALFA: {r.pre_over_alfalfa:.2f} before → {r.post_over_alfalfa:.2f} after',fontsize=10)
    ax.axhline(0,color='gray',lw=.5);ax.set_xlim(-350,350);ax.set_xlabel('Velocity from source centre (km/s)');ax.set_ylabel('Flux density (mJy)')
axes[0,0].legend(fontsize=8)
fig.suptitle('Final continuum subtraction removes some flux; most of the shortfall is already present\nFour original science galaxies, identical extraction and broad residual baseline treatment',fontsize=12)
fig.tight_layout(rect=[0,0,1,.90]);fig.savefig(HERE/'science_pipeline_profiles.png',dpi=170);plt.close(fig)
record=dict(n_galaxies=len(pairs),input_profiles_sha256=hashlib.sha256((HERE/'stage_run/plot_profiles.csv').read_bytes()).hexdigest(),figure_sha256=hashlib.sha256((HERE/'science_pipeline_profiles.png').read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),note='Figure is drawn directly from the final stage-run common-bin profiles; flux ratios come from native-channel integrals.')
(HERE/'figure_verification.json').write_text(json.dumps(record,indent=2))
