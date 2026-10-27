"""Exploratory central brightness comparison; never a total-flux beam correction."""
from pathlib import Path
import json,sys
import numpy as np
import pandas as pd
import analyze_stages as st

def main():
    out=Path(sys.argv[1]);out.mkdir(exist_ok=True);root=st.ROOT;cat=pd.read_csv(root/'data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv').set_index('ID_catalogue');table=pd.read_csv(root/'reviews/fashi_mightee_profiles_2026_10_18/run_02/per_galaxy.csv');table=table[table.reliable&(table.alf_code==1)];ms=pd.read_csv(root/'reviews/fashi_mightee_profiles_2026_10_18/run_02/measurements.csv');rows=[]
    for _,r in table.iterrows():
        z=np.load(st.DATA/('dirty_'+r.ID+'.npz'));c=cat.loc[r.ID];f=z['frequency_hz']/1e6;v=st.p.C*(c.freq_MHz/f-1);w=float(ms[(ms.ID==r.ID)&(ms.profile=='m15')&(ms.baseline=='linear')&(ms.expand==0)].halfwidth.iloc[0]);rec=dict(ID=r.ID)
        # Native line channels were all fetched; sparse sampling occurs only far outside the line.
        line=abs(v)<=w;assert np.max(np.diff(z['gs'][line]))==1
        for kind in ['constant','linear']:
            for stage in ['dirty','pre','post']:
                y=np.asarray(z[stage],float).mean(axis=(1,2));ok=np.isfinite(y);b,n=st.p.fitbase(v,y,st.masks(v,ok,w,c,cat),kind)
                flux,cov=st.p.integrate(f,y-b,ok,c.freq_MHz,-w,w);assert cov>.99
                rec[stage+'_'+kind]=flux
        rec.update(pre_over_dirty=rec['pre_linear']/rec['dirty_linear'],post_over_dirty=rec['post_linear']/rec['dirty_linear']);rows.append(rec)
    df=pd.DataFrame(rows);df.to_csv(out/'central_brightness.csv',index=False)
    result=dict(n_pairs=len(df),median_pre_over_dirty=float(df.pre_over_dirty.median()),median_post_over_dirty=float(df.post_over_dirty.median()),n_pre_dimmer=int((df.pre_over_dirty<1).sum()),median_pre_over_dirty_constant=float(np.median(df.pre_constant/df.dirty_constant)),units='Integrated mean3x3-pixel brightness: Jy/beam times common local-velocity equivalent km/s; these are not integrated total source fluxes',interpretation='Dirty-to-pre transition includes deconvolution, PSF homogenization and mosaicking differences. Central brightness ratios support localization but do not uniquely isolate an area factor or yield a total-flux correction.',limitations=['Dirty and homogenized maps have different effective PSFs','Extended sources, neighbours and dirty PSF shoulders can alter central brightness','No per-pointing model/residual/PSF products or production commit available'])
    (out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
