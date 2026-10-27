"""Compact figure from the same hash-pinned spectra and measured baseline rule."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import compare_profiles as p
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1];OUT=BASE/'run_02'
cat=pd.read_csv(ROOT/'data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv').set_index('ID_catalogue')
summary=pd.read_csv(OUT/'per_galaxy.csv');m=pd.read_csv(OUT/'measurements.csv');s=summary[summary.reliable&(summary.alf_code==1)&summary.science47]
fig,axes=plt.subplots(2,2,figsize=(11,7),sharex=True)
for ax,(_,r) in zip(axes.flat,s.iterrows()):
    z=np.load(p.DATA/(r.ID+'.npz'));c=cat.loc[r.ID];fc=c.freq_MHz
    w=float(m[(m.ID==r.ID)&(m.profile=='m15')&(m.baseline=='linear')&(m.expand==0)].halfwidth.iloc[0])
    for key,color,label in [('a','black','ALFALFA'),('m15','#1678b5','MIGHTEE: 1.5 beam radius'),('m25','#d68424','MIGHTEE: 2.5 beam radius')]:
        a=key=='a';f=z['a_frequency_mhz'] if a else z['frequency_mhz'];y=z['a_flux_mjy']/1000 if a else z[key];ok=np.isfinite(y)
        ok&=((z['a_flux_mjy']>-900)&(z['a_baseline_mjy']>-900)&(z['a_weight']>=.5)) if a else z['beam_valid']
        order=np.argsort(f);f,y,ok=f[order],y[order],ok[order];v=p.C*(fc/f-1);bn=ok&(abs(v)>w+350)&(abs(v)<1800)
        for nid,nc in cat.iterrows():
            if nid==r.ID:continue
            sep=3600*np.hypot((nc.RA_deg-c.RA_deg)*np.cos(np.deg2rad(c.Dec_deg)),nc.Dec_deg-c.Dec_deg)
            if sep<397.5:bn&=abs(v-p.C*(fc/nc.freq_MHz-1))>max(150,nc.W_50_km_s/2+100)
        b,_=p.fitbase(v,y,bn,'linear');y=y-b
        # Check figure uses exactly the reported primary integral.
        value,cov=p.integrate(f,y,ok,fc,-w,w)
        expected=r.alf_common if a else r.m15_common if key=='m15' else r.m25_common
        assert abs(value-expected)<1e-10
        bins=np.arange(-400,401,20);vals=[p.integrate(f,y,ok,fc,lo,hi)[0]/(hi-lo)*1000 for lo,hi in zip(bins[:-1],bins[1:])]
        ax.step((bins[:-1]+bins[1:])/2,vals,where='mid',color=color,lw=1.3,label=label)
    ax.axvspan(-w,w,color='gray',alpha=.09);ax.axhline(0,color='gray',lw=.5)
    ax.set_title(f'{r.ID}   MIGHTEE / ALFALFA = {r.ratio:.2f}',fontsize=10)
    ax.set_ylabel('Flux density (mJy)');ax.set_xlabel('Velocity from MIGHTEE centre (km/s)');ax.set_xlim(-400,400)
axes[0,0].legend(fontsize=8,loc='upper left')
fig.suptitle('Original science sample: four reliable ALFALFA detections with cube coverage\nCommon windows and robust linear residual baselines; 20 km/s bins',fontsize=12)
fig.tight_layout(rect=[0,0,1,.91]);fig.savefig(BASE/'science_profiles.png',dpi=170);plt.close(fig)
record=dict(checks='All 12 plotted primary integrals reproduce the run_02 fluxes to 1e-10',figure_sha256=hashlib.sha256((BASE/'science_profiles.png').read_bytes()).hexdigest(),input_run='run_02/manifest.json',script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(BASE/'figure_verification.json').write_text(json.dumps(record,indent=2))
print(record['checks'])
