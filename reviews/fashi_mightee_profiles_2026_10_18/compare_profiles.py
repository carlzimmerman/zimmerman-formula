"""Paired native-channel integrals, with identical windows and residual baselines."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
C=299792.458
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'_external_data/hi_profiles_2026_10_18'

def edges(x):
    x=np.asarray(x);return np.r_[x[0]-(x[1]-x[0])/2,(x[:-1]+x[1:])/2,x[-1]+(x[-1]-x[-2])/2]

def integrate(f,y,ok,fc,lo,hi):
    """Exact frequency-bin overlaps; relative optical velocity differential at fc."""
    e=edges(f);left=fc/(1+hi/C);right=fc/(1+lo/C)
    overlap=np.maximum(0,np.minimum(e[1:],right)-np.maximum(e[:-1],left))
    weights=np.where(ok,overlap,0)
    if weights.sum()==0:return float('nan'),0.0
    return float(np.sum(np.where(ok,y,0)*weights)*C/fc),float(weights.sum()/(right-left))

def fitbase(v,y,mask,kind):
    keep=mask&np.isfinite(y)
    if keep.sum()<32:return np.full(len(y),np.nan),int(keep.sum())
    if kind=='none':return np.zeros(len(y)),int(keep.sum())
    for _ in range(4):
        if kind=='constant':b=np.full(len(y),np.median(y[keep]))
        else:b=np.polyval(np.polyfit(v[keep]/1000,y[keep],1),v/1000)
        resid=y-b;sig=1.4826*np.median(np.abs(resid[keep]-np.median(resid[keep])))
        keep=mask&np.isfinite(y)&(np.abs(resid)<3.5*max(sig,1e-12))
        if keep.sum()<32:return np.full(len(y),np.nan),int(keep.sum())
    return b,int(keep.sum())

def controls():
    f=np.linspace(1390,1410,2001);fc=1400;v=C*(fc/f-1);line=np.where(np.abs(v)<100,.01,0);base=.002+v*1e-6
    mask=(np.abs(v)>500)&(np.abs(v)<1800);b,n=fitbase(v,line+base,mask,'linear')
    assert np.max(np.abs(b-base))<1e-12
    total,_=integrate(f,line,np.ones(len(f),bool),fc,-200,200)
    reb=sum(integrate(f,line,np.ones(len(f),bool),fc,a,a+20)[0] for a in range(-200,200,20))
    assert abs(total-reb)<1e-10
    got,_=integrate(f,line+base-b,np.ones(len(f),bool),fc,-200,200)
    assert abs(got-total)<1e-10
    return dict(sloped_baseline_recovery=True,rebin_integral_conservation=True,injected_line_recovery=True)

def main():
    out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
    checks=controls()
    allm=pd.read_csv(ROOT/'reviews/fashi_mightee_flux_2026_10_18/run_02/matched_sources.csv')
    matches=allm[allm.agc.notna()]
    cat=pd.read_csv(ROOT/'data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv').set_index('ID_catalogue')
    acat=pd.read_csv(ROOT/'campaign_fresh_gravity/CFG304_mightee_flux_scale_alfalfa/cfg304_matched_pairs.csv').set_index('ID')
    old=pd.read_csv(ROOT/'campaign_fresh_gravity/CFG302_mightee_cube_raw_widths/cfg302_per_galaxy.csv').set_index('ID')
    measurements=[];sources=[];spectra={};reproductions=[];cores={}
    unavailable=[]
    fig,axes=plt.subplots(7,3,figsize=(16,24),squeeze=False)
    for ax,(_,r) in zip(axes.flat,matches.iterrows()):
        if not (DATA/(r.ID+'.npz')).exists():
            unavailable.append(r.ID);ax.text(.5,.5,r.ID+'\nOutside downloaded MIGHTEE frequency coverage',ha='center',va='center',transform=ax.transAxes,fontsize=9);ax.axis('off');continue
        z=np.load(DATA/(r.ID+'.npz'));fc=float(cat.loc[r.ID].freq_MHz);aa=acat.loc[r.ID]
        w=max(150,.5*max(r.W50_m,aa.w50_A)+50)
        d={}
        for key in ['m15','m25','a','a_restored']:
            is_a=key.startswith('a');f=z['a_frequency_mhz'] if is_a else z['frequency_mhz']
            y=(z['a_flux_mjy']+(z['a_baseline_mjy'] if key=='a_restored' else 0))/1000 if is_a else z[key]
            ok=np.isfinite(y)
            if is_a:ok&=(z['a_flux_mjy']>-900)&(z['a_baseline_mjy']>-900)&(z['a_weight']>=.5)
            else:ok&=z['beam_valid']
            order=np.argsort(f);f=f[order];y=y[order];ok=ok[order];v=C*(fc/f-1)
            bn=ok&(np.abs(v)>w+350)&(np.abs(v)<1800)
            # Use the same catalogue-based neighbour exclusions for both instruments.
            neighbors=[]
            for nid,nc in cat.iterrows():
                if nid==r.ID:continue
                sep=3600*np.hypot((nc.RA_deg-r.ra_m)*np.cos(np.deg2rad(r.dec_m)),nc.Dec_deg-r.dec_m)
                if sep<2.5*np.median([75])+210:
                    vc=C*(fc/nc.freq_MHz-1);nw=max(150,nc.W_50_km_s/2+100)
                    bn&=np.abs(v-vc)>nw
                    if abs(vc)<w+250:neighbors.append(nid)
            for kind in ['none','constant','linear']:
                b,nb=fitbase(v,y,bn,kind);yb=y-b
                for expand in [0,100,250]:
                    flux,cov=integrate(f,yb,ok&np.isfinite(yb),fc,-w-expand,w+expand)
                    measurements.append(dict(ID=r.ID,profile=key,baseline=kind,expand=expand,halfwidth=w+expand,flux=flux,coverage=cov,n_baseline=nb,baseline_center_mjy=float(np.interp(0,v[::-1],b[::-1])*1000),reliable=bool(r.reliable),science47=bool(r.science47),alf_code=int(r.alf_code),neighbors=';'.join(neighbors)))
                if kind=='linear':d[key]=(f,yb,ok)
            if key=='m15' and r.ID in old.index:
                narrow=r.W50_m/2+50
                # CFG302 used whole channels, no residual baseline subtraction.
                native=float(np.sum(y[np.abs(v)<=narrow])*26124.84126282)
                expected=float(old.loc[r.ID].S_L_Jy_Hz)
                reproductions.append(dict(ID=r.ID,old=expected,new=native,relative_difference=(native-expected)/expected))
        # ALFALFA VHELIO/frequency relation determines its velocity convention empirically.
        mask=(z['a_weight']>=.5)&(z['a_vhelio']>-900)
        optical=C*(1420.40575177/z['a_frequency_mhz'][mask]-1)
        sources.append(dict(ID=r.ID,halfwidth=w,alf_vhel_optical_max_difference=float(np.max(np.abs(optical-z['a_vhelio'][mask])))))
        bins=np.arange(-min(900,w+350),min(900,w+350)+20,20)
        for key,color,label in [('a','black','ALFALFA'),('m15','#1678b5','MIGHTEE 1.5 beam'),('m25','#d68424','MIGHTEE 2.5 beam')]:
            f,y,ok=d[key];vals=[]
            for lo,hi in zip(bins[:-1],bins[1:]):
                flux,cov=integrate(f,y,ok,fc,lo,hi);vals.append(flux/(hi-lo)*1000 if cov>.95 else np.nan)
            ax.step((bins[:-1]+bins[1:])/2,vals,where='mid',lw=1,label=label,color=color,alpha=.9)
        ax.axvspan(-w,w,color='gray',alpha=.09);ax.axhline(0,color='gray',lw=.5)
        ax.set_title(r.ID+'  AGC '+str(int(r.agc))+(' [science]' if r.science47 else ''),fontsize=9)
        ax.set_xlabel('Velocity from MIGHTEE centre (km/s)',fontsize=8);ax.set_ylabel('Flux density (mJy)',fontsize=8);ax.tick_params(labelsize=7)
        spectra[r.ID]=d
        corew=r.W50_m/4
        cores[r.ID]={key:integrate(*d[key],fc,-corew,corew)[0] for key in ['a','m15','m25']}
    axes[0,0].legend(fontsize=7)
    fig.suptitle('Identical windows and robust linear residual baselines; native spectra rebinned to 20 km/s\nGrey: primary line window. Orange: larger aperture, with increased noise and possible neighbours.',fontsize=13)
    fig.tight_layout(rect=[0,0,1,.965]);fig.savefig(out/'profiles.png',dpi=150);plt.close(fig)
    df=pd.DataFrame(measurements);df.to_csv(out/'measurements.csv',index=False)
    checks['old_extraction_reproduced']=all(abs(q['relative_difference'])<1e-6 for q in reproductions)
    summaries={};rng=np.random.default_rng(20261019)
    for subset,select in [('all',matches.ID),('reliable',matches[matches.reliable].ID),('reliable_code1',matches[matches.reliable&(matches.alf_code==1)].ID),('science_code1',matches[matches.reliable&(matches.alf_code==1)&matches.science47].ID)]:
        ss={}
        for kind in ['none','constant','linear']:
            for expand in [0,100,250]:
                q=df[(df.baseline==kind)&(df.expand==expand)&df.ID.isin(select)]
                p=q.pivot(index='ID',columns='profile',values='flux');cov=q.pivot(index='ID',columns='profile',values='coverage')
                for key in ['m15','m25','a_restored']:
                    good=(cov[key]>=.95)&(cov.a>=.95)&(p[key]>0)&(p.a>0);ratio=p.loc[good,key]/p.loc[good,'a']
                    boot=np.median(rng.choice(ratio.to_numpy(),size=(10000,len(ratio)),replace=True),axis=1) if len(ratio) else np.array([np.nan])
                    ss[f'{key}_{kind}_plus{expand}']=dict(n=len(ratio),median_ratio=float(ratio.median()),median_ratio_95ci=np.quantile(boot,[.025,.975]).tolist())
        summaries[subset]=ss
    (out/'results.json').write_text(json.dumps(dict(checks=checks,summaries=summaries,unavailable=unavailable,extraction_reproduction=reproductions,velocity_checks=sources,limitations=['No FAST channel spectra','Bootstrap captures galaxy variation, not calibration systematics','Post-release comparison cannot identify upstream calibration/continuum/cleaning uniquely','Larger aperture includes additional noise and possible neighbours']),indent=2))
    # One row per galaxy, preserving signed wing and baseline contributions.
    q=df.pivot(index='ID',columns=['profile','baseline','expand'],values='flux')
    rows=[]
    for _,r in matches.iterrows():
        if r.ID not in q.index:continue
        s=q.loc[r.ID];a=s['a','linear',0];mm=s['m15','linear',0]
        rows.append(dict(ID=r.ID,agc=int(r.agc),reliable=r.reliable,science47=r.science47,alf_code=r.alf_code,alf_catalogue=float(r.alfalfa)/(1+float(r.z_m_freq)),m_catalogue_rest=r.m_REST,fast_catalogue=r.f_busy,alf_common=a,m15_common=mm,m25_common=s['m25','linear',0],ratio=mm/a,m15_wings_plus250=s['m15','linear',250]-mm,alf_wings_plus250=s['a','linear',250]-a,m15_baseline_change=mm-s['m15','none',0],alf_baseline_change=a-s['a','none',0],alf_restored=s['a_restored','linear',0]))
        rows[-1].update(core_alf=cores[r.ID]['a'],core_m15=cores[r.ID]['m15'],core_m25=cores[r.ID]['m25'])
    summary=pd.DataFrame(rows);summary.to_csv(out/'per_galaxy.csv',index=False)
    print(json.dumps(dict(checks=checks,primary=summaries['reliable_code1']['m15_linear_plus0'],science=summaries['science_code1']['m15_linear_plus0']),indent=2))

if __name__=='__main__':main()
