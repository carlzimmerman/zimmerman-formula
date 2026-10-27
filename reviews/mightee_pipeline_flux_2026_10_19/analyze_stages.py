"""Localize flux changes across the final image-domain continuum subtraction."""
from pathlib import Path
import importlib.util,json,sys
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'_external_data/mightee_pipeline_2026_10_19'
s=importlib.util.spec_from_file_location('profiles',ROOT/'reviews/fashi_mightee_profiles_2026_10_18/compare_profiles.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)

def masks(v,ok,w,c,cat):
    bn=ok&(abs(v)>w+350)&(abs(v)<1800)
    for nid,nc in cat.iterrows():
        if nid==c.name:continue
        sep=3600*np.hypot((nc.RA_deg-c.RA_deg)*np.cos(np.deg2rad(c.Dec_deg)),nc.Dec_deg-c.Dec_deg)
        if sep<397.5:bn&=abs(v-p.C*(c.freq_MHz/nc.freq_MHz-1))>max(150,nc.W_50_km_s/2+100)
    return bn

def gaussian_fit(image,xy,beam):
    yy,xx=np.indices(image.shape);ok=np.isfinite(image);b0=np.median(image[ok]);amp=max(np.max(image[ok])-b0,1e-9)
    def model(t):
        a,x,y,sx,sy,theta,b=t;dx=xx-x;dy=yy-y;u=dx*np.cos(theta)+dy*np.sin(theta);v=-dx*np.sin(theta)+dy*np.cos(theta)
        return a*np.exp(-.5*((u/sx)**2+(v/sy)**2))+b
    t0=[amp,*xy,beam/8/2.35482,beam/8/2.35482,0,b0]
    low=[0,xy[0]-4,xy[1]-4,1,1,-np.pi,-np.inf];high=[amp*10,xy[0]+4,xy[1]+4,25,25,np.pi,np.inf]
    fit=least_squares(lambda t:(model(t)-image)[ok]/amp,t0,bounds=(low,high),max_nfev=1000)
    sizes=sorted(fit.x[3:5]*8*2.35482,reverse=True)
    return dict(success=bool(fit.success),major_arcsec=float(sizes[0]),minor_arcsec=float(sizes[1]),header_beam_arcsec=float(beam),amplitude=float(fit.x[0]),fit_note='Source extension, noise and non-Gaussian structure prevent treating fitted galaxy width as an independent beam calibration.')

def main():
    out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
    implementation_controls=p.controls()
    table=pd.read_csv(ROOT/'reviews/fashi_mightee_profiles_2026_10_18/run_02/per_galaxy.csv');table=table[table.reliable&(table.alf_code==1)]
    mc=pd.read_csv(ROOT/'reviews/fashi_mightee_profiles_2026_10_18/run_02/measurements.csv');cat=pd.read_csv(ROOT/'data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv').set_index('ID_catalogue')
    fig,axes=plt.subplots(4,2,figsize=(13,13));records=[];checks=[];spatial=[];plotrows=[];radial=[];noise=[]
    for ax,(_,r) in zip(axes.flat,table.iterrows()):
        z=np.load(DATA/(r.ID+'.npz'));c=cat.loc[r.ID];fc=c.freq_MHz;f=z['frequency_hz']/1e6;v=p.C*(fc/f-1)
        a=np.load(p.DATA/(r.ID+'.npz'));w=float(mc[(mc.ID==r.ID)&(mc.profile=='m15')&(mc.baseline=='linear')&(mc.expand==0)].halfwidth.iloc[0])
        yy,xx=np.indices(z['pre'].shape[1:]);x,y=z['centres_xy'][0];ap=(xx-x)**2+(yy-y)**2<=(float(z['radius_arcsec'])/8)**2
        spectra={key:np.asarray(z[key],float)[:,ap].sum(axis=1)/z['beam_area_pixels'] for key in ['pre','post']}
        checks.append(dict(ID=r.ID,post_spectrum_max_absolute_difference=float(np.max(abs(spectra['post']-a['m15'])))))
        assert checks[-1]['post_spectrum_max_absolute_difference']<1e-12
        corrected={}
        for kind in ['none','constant','linear']:
            for key in ['pre','post']:
                yy0=spectra[key];ok=np.isfinite(yy0);bn=masks(v,ok,w,c,cat);baseline,n=p.fitbase(v,yy0,bn,kind);yb=yy0-baseline
                for expand in [0,100,250]:
                    flux,cov=p.integrate(f,yb,ok,fc,-w-expand,w+expand)
                    records.append(dict(ID=r.ID,science47=bool(r.science47),stage=key,baseline=kind,expand=expand,flux=flux,coverage=cov,n_baseline=n))
                if kind=='linear':corrected[key]=yb
        assert abs(records[-3]['flux']-r.m15_common)<1e-10
        for stage in ['pre','post']:
            yb=corrected[stage];bn=masks(v,np.isfinite(yb),w,c,cat);idx=np.flatnonzero(bn);runs=np.split(idx,np.flatnonzero(np.diff(idx)>1)+1);sig=1.4826*np.median(abs(yb[bn]-np.median(yb[bn])))
            for n in [1,8,16,32,64]:
                blocks=np.array([yb[run[j:j+n]].sum() for run in runs for j in range(0,len(run)-n+1,n)])
                if len(blocks)<4:continue
                sb=1.4826*np.median(abs(blocks-np.median(blocks)))
                noise.append(dict(ID=r.ID,stage=stage,block_channels=n,n_blocks=len(blocks),variance_ratio=float(sb**2/(n*sig**2))))
        af=a['a_frequency_mhz'];ay=a['a_flux_mjy']/1000;ao=np.isfinite(ay)&(a['a_flux_mjy']>-900)&(a['a_baseline_mjy']>-900)&(a['a_weight']>=.5);order=np.argsort(af);af,ay,ao=af[order],ay[order],ao[order];av=p.C*(fc/af-1);ab,_=p.fitbase(av,ay,masks(av,ao,w,c,cat),'linear');ay-=ab
        bins=np.arange(-450,451,20)
        for key,ff,ys,ok,color,label in [('a',af,ay,ao,'black','ALFALFA'),('pre',f,corrected['pre'],np.isfinite(corrected['pre']),'#ad267d','Before final continuum subtraction'),('post',f,corrected['post'],np.isfinite(corrected['post']),'#1678b5','After final continuum subtraction')]:
            vals=[p.integrate(ff,ys,ok,fc,lo,hi)[0]/(hi-lo)*1000 for lo,hi in zip(bins[:-1],bins[1:])]
            ax.step((bins[:-1]+bins[1:])/2,vals,where='mid',color=color,label=label,lw=1.2)
            plotrows.extend(dict(ID=r.ID,stage=key,velocity_center=float((lo+hi)/2),flux_mjy=float(val)) for lo,hi,val in zip(bins[:-1],bins[1:],vals))
        ax.set_title(r.ID+(' [original science]' if r.science47 else ''),fontsize=10);ax.axvspan(-w,w,color='gray',alpha=.09);ax.axhline(0,color='gray',lw=.5);ax.set_xlabel('Velocity from source centre (km/s)');ax.set_ylabel('Flux density (mJy)')
        # Line moment maps with a per-pixel off-line median for geometric diagnostics only.
        bn=masks(v,np.ones(len(v),bool),w,c,cat);line=abs(v)<=w
        for stage in ['pre','post']:
            cube=np.asarray(z[stage],float);bg=np.median(cube[bn],axis=0);image=np.sum(cube[line]-bg,axis=0)
            fit=gaussian_fit(image,(x,y),float(np.median(z['beam_arcsec'][line])));fit.update(ID=r.ID,stage=stage);spatial.append(fit)
        beam=float(np.median(z['beam_arcsec'][line]));rr=np.hypot(xx-x,yy-y)*8
        for lower,upper in [(0,.5),(.5,1),(1,1.5)]:
            ring=(rr>=lower*beam)&(rr<upper*beam)
            for stage in ['pre','post']:
                flux=np.asarray(z[stage],float)[:,ring].sum(axis=1)/z['beam_area_pixels'];ok=np.isfinite(flux);b,_=p.fitbase(v,flux,masks(v,ok,w,c,cat),'linear')
                val,cov=p.integrate(f,flux-b,ok,fc,-w,w)
                radial.append(dict(ID=r.ID,stage=stage,inner_beams=lower,outer_beams=upper,flux=val,coverage=cov))
    axes[0,0].legend(fontsize=8);axes[-1,-1].axis('off');fig.suptitle('Matched public MIGHTEE products immediately before and after final image-domain subtraction\nSame pixels, beam areas, line windows and broad off-line residual baseline fits',fontsize=12);fig.tight_layout(rect=[0,0,1,.95]);fig.savefig(out/'pipeline_profiles.png',dpi=150);plt.close(fig)
    df=pd.DataFrame(records);df.to_csv(out/'stage_measurements.csv',index=False);pd.DataFrame(plotrows).to_csv(out/'plot_profiles.csv',index=False);pd.DataFrame(radial).to_csv(out/'radial_stage_fluxes.csv',index=False);pd.DataFrame(noise).to_csv(out/'noise_blocks.csv',index=False)
    pair=df.pivot(index='ID',columns=['stage','baseline','expand'],values='flux');rows=[]
    for _,r in table.iterrows():
        q=pair.loc[r.ID];pre=q['pre','linear',0];post=q['post','linear',0]
        rows.append(dict(ID=r.ID,science47=bool(r.science47),alfalfa=r.alf_common,catalogue=r.m_catalogue_rest,pre=pre,post=post,pre_over_post=pre/post,pre_over_alfalfa=pre/r.alf_common,post_over_alfalfa=post/r.alf_common,removed_line_flux=pre-post,removed_fraction_of_pre=(pre-post)/pre,fraction_alfalfa_deficit_explained=(pre-post)/(r.alf_common-post)))
    pairs=pd.DataFrame(rows);pairs.to_csv(out/'paired_fluxes.csv',index=False)
    summary={}
    for name,q in [('all_seven',pairs),('original_science_four',pairs[pairs.science47])]:
        summary[name]={k:float(q[k].median()) for k in ['pre_over_post','pre_over_alfalfa','post_over_alfalfa','removed_fraction_of_pre','fraction_alfalfa_deficit_explained']}
    baseline_sensitivity={}
    for kind in ['none','constant','linear']:
        for expand in [0,100,250]:
            baseline_sensitivity[kind+'_plus'+str(expand)]=float(np.median(pair['pre',kind,expand]/pair['post',kind,expand]))
    result=dict(status='completed',n_pairs=len(pairs),implementation_controls=implementation_controls,post_extraction_checks=checks,summary=summary,pre_post_sensitivity=baseline_sensitivity,spatial_gaussian_fits=spatial,limitations=['pre cube already underwent visibility-domain continuum subtraction and beam homogenization','Pre/post baseline fits mitigate smooth continuum, but residual structure can remain','Gaussian galaxy fits are not independent PSF measurements','Seven selected overlaps do not establish a general correction'])
    (out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
