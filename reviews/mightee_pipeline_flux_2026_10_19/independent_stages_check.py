"""Independent scalar bin sums and closed-form regressions for stage fluxes."""
from pathlib import Path
import importlib.util,json
import numpy as np
import pandas as pd
import analyze_stages as st
ROOT=st.ROOT;HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('previous_independent',ROOT/'reviews/fashi_mightee_profiles_2026_10_18/independent_check.py');ind=importlib.util.module_from_spec(s);s.loader.exec_module(ind)

def main():
    pairs=pd.read_csv(HERE/'stage_run/paired_fluxes.csv');ms=pd.read_csv(ROOT/'reviews/fashi_mightee_profiles_2026_10_18/run_02/measurements.csv');cat=pd.read_csv(ROOT/'data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv').set_index('ID_catalogue');checks=[]
    for _,r in pairs.iterrows():
        c=cat.loc[r.ID];z=np.load(st.DATA/(r.ID+'.npz'));f=z['frequency_hz']/1e6;v=st.p.C*(c.freq_MHz/f-1);x=v/1000;w=float(ms[(ms.ID==r.ID)&(ms.profile=='m15')&(ms.baseline=='linear')&(ms.expand==0)].halfwidth.iloc[0]);yy,xx=np.indices(z['pre'].shape[1:]);xc,yc=z['centres_xy'][0];mask=(xx-xc)**2+(yy-yc)**2<=(float(z['radius_arcsec'])/8)**2
        for stage in ['pre','post']:
            # Sum source pixels as independent Python/scalar-order reductions for each plane.
            y=np.array([sum(float(t) for t in plane[mask])/float(area) for plane,area in zip(z[stage],z['beam_area_pixels'])]);ok=np.isfinite(y);bn=st.masks(v,ok,w,c,cat);keep=bn.copy()
            for _ in range(4):
                vx=x[keep];vy=y[keep];slope=sum((vx-vx.mean())*(vy-vy.mean()))/sum((vx-vx.mean())**2);intercept=vy.mean()-slope*vx.mean();baseline=intercept+slope*x;res=y-baseline;sigma=1.4826*np.median(abs(res[keep]-np.median(res[keep])));keep=bn&ok&(abs(res)<3.5*max(sigma,1e-12))
            value=ind.integrate_scalar(f,y-baseline,ok,c.freq_MHz,w);diff=abs(value-r[stage]);assert diff<1e-10,(r.ID,stage,diff);checks.append(dict(ID=r.ID,stage=stage,value=value,absolute_difference=diff))
    result=dict(status='passed',n_integrals=len(checks),max_absolute_difference=max(q['absolute_difference'] for q in checks),checks=checks,note='Independent pixel summation, linear-regression formula and scalar bin integration; catalogue-based neighbour exclusion shares the main mask helper.')
    (HERE/'independent_verification.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k!='checks'})

if __name__=='__main__':main()
