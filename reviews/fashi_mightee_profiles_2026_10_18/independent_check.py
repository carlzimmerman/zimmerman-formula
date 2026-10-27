"""Independent closed-form regression and scalar bin integration for seven primary pairs."""
from pathlib import Path
import json,math
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];C=299792.458
BASE=ROOT/'reviews/fashi_mightee_profiles_2026_10_18'

def integrate_scalar(f,y,ok,fc,w):
    pairs=sorted(zip(f,y,ok));total=0
    low=fc/(1+w/C);high=fc/(1-w/C)
    for i,(nu,flux,valid) in enumerate(pairs):
        if not valid:continue
        left=(pairs[i-1][0]+nu)/2 if i else nu-(pairs[1][0]-nu)/2
        right=(nu+pairs[i+1][0])/2 if i+1<len(pairs) else nu+(nu-pairs[i-1][0])/2
        width=max(0,min(right,high)-max(left,low))
        total+=flux*width*C/fc
    return total

def main():
    table=pd.read_csv(BASE/'run_02/per_galaxy.csv');table=table[table.reliable&(table.alf_code==1)]
    cat=pd.read_csv(ROOT/'data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv').set_index('ID_catalogue')
    measures=pd.read_csv(BASE/'run_02/measurements.csv');checks=[]
    for _,r in table.iterrows():
        z=np.load(ROOT/'_external_data/hi_profiles_2026_10_18'/(r.ID+'.npz'));c=cat.loc[r.ID];fc=c.freq_MHz
        w=float(measures[(measures.ID==r.ID)&(measures.profile=='m15')&(measures.baseline=='linear')&(measures.expand==0)].halfwidth.iloc[0])
        for profile in ['m15','a']:
            is_a=profile=='a';f=z['a_frequency_mhz'] if is_a else z['frequency_mhz'];y=z['a_flux_mjy']/1000 if is_a else z['m15'];ok=np.isfinite(y)
            ok &= ((z['a_flux_mjy']>-900)&(z['a_baseline_mjy']>-900)&(z['a_weight']>=.5)) if is_a else z['beam_valid']
            v=C*(fc/f-1);mask=ok&(abs(v)>w+350)&(abs(v)<1800)
            for nid,nc in cat.iterrows():
                if nid==r.ID:continue
                # Spherical distance, independent of tangent-plane selection in main script.
                ra1,ra2,de1,de2=map(math.radians,[c.RA_deg,nc.RA_deg,c.Dec_deg,nc.Dec_deg])
                a=math.sin((de1-de2)/2)**2+math.cos(de1)*math.cos(de2)*math.sin((ra1-ra2)/2)**2
                sep=2*math.asin(min(1,math.sqrt(a)))*180/math.pi*3600
                if sep<397.5:mask &= abs(v-C*(fc/nc.freq_MHz-1))>max(150,nc.W_50_km_s/2+100)
            keep=mask.copy();x=v/1000
            for _ in range(4):
                xx=x[keep];yy=y[keep];slope=np.sum((xx-xx.mean())*(yy-yy.mean()))/np.sum((xx-xx.mean())**2)
                intercept=yy.mean()-slope*xx.mean();baseline=intercept+slope*x;res=y-baseline
                sigma=1.4826*np.median(abs(res[keep]-np.median(res[keep])))
                keep=mask&np.isfinite(y)&(abs(res)<3.5*max(sigma,1e-12))
            value=integrate_scalar(f,y-baseline,ok,fc,w);expected=r.m15_common if profile=='m15' else r.alf_common
            diff=abs(value-expected);assert diff<1e-10,(r.ID,profile,value,expected)
            checks.append(dict(ID=r.ID,profile=profile,value=value,absolute_difference=diff))
    result=dict(status='passed',n_pairs=len(table),n_independent_integrals=len(checks),max_absolute_difference=max(q['absolute_difference'] for q in checks),checks=checks)
    (BASE/'independent_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='checks'}))

if __name__=='__main__':main()
