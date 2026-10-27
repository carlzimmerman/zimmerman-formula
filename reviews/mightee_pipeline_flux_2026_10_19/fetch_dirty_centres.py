"""Small central sightlines from dirty cubes; exploratory earlier-stage diagnostic."""
from pathlib import Path
import concurrent.futures as cf,json,io,time
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
import fetch_stages as fetch

def main():
    start=time.time();root=fetch.ROOT;out=fetch.OUT;cubes=fetch.m.load_cubes();cat=pd.read_csv(fetch.m.CAT).set_index('ID_catalogue');m=pd.read_csv(root/'reviews/fashi_mightee_profiles_2026_10_18/run_02/measurements.csv');table=pd.read_csv(root/'reviews/fashi_mightee_profiles_2026_10_18/run_02/per_galaxy.csv');table=table[table.reliable&(table.alf_code==1)];headers={};records=[]
    for _,r in table.iterrows():
        dest=out/('dirty_'+r.ID+'.npz')
        if dest.exists():continue
        c=cat.loc[r.ID];z=np.load(out/(r.ID+'.npz'));freq=z['frequency_hz'];v=fetch.m.C*(c.freq_MHz*1e6/freq-1);gs=np.rint(fetch.m.g_of_nu(freq)).astype(int)
        w=float(m[(m.ID==r.ID)&(m.profile=='m15')&(m.baseline=='linear')&(m.expand==0)].halfwidth.iloc[0]);select=(abs(v)<=w+100)|((abs(v)>w+350)&(abs(v)<1800)&(gs%6==0));selected=gs[select];data=[];pre=[];post=[]
        for k in np.unique(fetch.m.owner(selected)):
            filename=f'MIGHTEE-HI_DR1_COSMOS_L2_r1p0_dirty_{fetch.m.RANGES[k]}.fits';url=fetch.BASE+filename
            if k not in headers:
                raw=fetch.get(url,0,28799);cards=[raw[i:i+80].decode('ascii',errors='replace') for i in range(0,len(raw),80)];end=next(i for i,t in enumerate(cards) if t.startswith('END     '));h=fits.Header.fromstring(''.join(cards[:end+1]),sep='');offset=((end+1)*80+2879)//2880*2880;headers[k]=(h,offset)
                assert all(h[t]==cubes[k]['hdr'][t] for t in ['NAXIS1','NAXIS2','NAXIS3','CRVAL1','CRVAL2','CDELT1','CDELT2','CRPIX1','CRPIX2','CRPIX3','CRVAL3','CDELT3'])
                (out/f'dirty_header_{k}.txt').write_text(repr(h))
            h,offset=headers[k];nx,ny=h['NAXIS1'],h['NAXIS2'];x,y=WCS(h).celestial.world_to_pixel_values(c.RA_deg,c.Dec_deg);ix,iy=round(float(x)),round(float(y));kg=selected[fetch.m.owner(selected)==k];chs=kg-1000*k
            def read(ch):
                a=offset+4*nx*(iy-1+ny*int(ch));b=offset+4*nx*(iy+1+ny*int(ch)+1)-1
                return np.frombuffer(fetch.get(url,a,b),dtype='>f4').reshape(3,nx)[:,ix-1:ix+2].astype('f4')
            with cf.ThreadPoolExecutor(max_workers=8) as pool:data.extend(pool.map(read,chs))
        # Identical sky pixel centres in the already checked pre/post cutouts.
        cx,cy=z['centres_xy'][0];px,py=round(float(cx)),round(float(cy))
        np.savez_compressed(dest,dirty=np.array(data),pre=z['pre'][select,py-1:py+2,px-1:px+2],post=z['post'][select,py-1:py+2,px-1:px+2],frequency_hz=freq[select],gs=selected)
        print('DIRTY SAVED',r.ID,len(selected),'channels elapsed',round(time.time()-start),flush=True);records.append(dict(ID=r.ID,n_channels=len(selected),dirty_units=h.get('BUNIT','UNSPECIFIED IN HEADER')))
    (out/'dirty_fetch_summary.json').write_text(json.dumps(dict(rows=records,reserved_bytes=fetch.used,elapsed_seconds=time.time()-start,note='Comparisons use central3x3 sightlines, not integrated total fluxes. Dirty PSF side lobes and deconvolution prevent an exact beam-scaling inference.'),indent=2))

if __name__=='__main__':main()
