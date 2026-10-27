"""Capped public HTTP-range cutouts of matched pre/post MIGHTEE pipeline stages."""
from pathlib import Path
import importlib.util,threading,concurrent.futures as cf,json,hashlib,time,datetime
import requests
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_external_data/mightee_pipeline_2026_10_19'
BASE='https://archive-gw-1.kat.ac.za/public/repository/10.48479/jkc0-g916/data/MIGHTEE-HI_DR1_L2_r1p0/'
CAP=1500000000;used=0;lock=threading.Lock();local=threading.local()
sp=importlib.util.spec_from_file_location('m302',ROOT/'campaign_fresh_gravity/CFG302_mightee_cube_raw_widths/cfg302_raw_widths.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

def get(url,a,b):
    global used
    if not hasattr(local,'s'):local.s=requests.Session()
    for attempt in range(3):
        with lock:
            assert used+b-a+1<=CAP,'Download cap reached'
            used+=b-a+1
        try:
            t=time.time()
            with local.s.get(url,headers={'Range':f'bytes={a}-{b}'},timeout=60,stream=True) as r:
                assert r.status_code==206,(r.status_code,url)
                cr=r.headers.get('Content-Range','');assert cr.startswith(f'bytes {a}-{b}/'),cr
                data=r.raw.read(b-a+2);assert len(data)==b-a+1,(len(data),b-a+1)
                rec=dict(url=url,start=a,end=b,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),content_range=cr,elapsed_seconds=time.time()-t,etag=r.headers.get('ETag'),utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
            with lock:
                with (OUT/'range_manifest.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
            return data
        except Exception:
            if attempt==2:raise
    raise RuntimeError('unreachable')

def main():
    start=time.time();cubes=m.load_cubes()
    table=pd.read_csv(ROOT/'reviews/fashi_mightee_profiles_2026_10_18/run_02/per_galaxy.csv');table=table[table.reliable&(table.alf_code==1)]
    cat=pd.read_csv(m.CAT).set_index('ID_catalogue');old=pd.read_csv(ROOT/'campaign_fresh_gravity/CFG302_mightee_cube_raw_widths/cfg302_per_galaxy.csv').set_index('ID')
    headers={};summ=[]
    for _,r in table.iterrows():
        dest=OUT/(r.ID+'.npz')
        if dest.exists():print(r.ID,'CACHED',flush=True);continue
        c=cat.loc[r.ID];nu=c.freq_MHz*1e6;radius=float(old.loc[r.ID].R_ap_arcsec)
        lo=max(0,int(np.floor(m.g_of_nu(m.nu_of_v(nu,2200)))));hi=min(m.NG-1,int(np.ceil(m.g_of_nu(m.nu_of_v(nu,-2200)))))
        gs=np.arange(lo,hi+1);pre=[];post=[];areas=[];beams=[];coords=[];h=int(np.ceil(radius/8))+2
        for k in np.unique(m.owner(gs)):
            cb=cubes[k];url=BASE+cb['file'].replace('_contsub','')
            if k not in headers:
                raw=get(url,0,28799);cards=[raw[i:i+80].decode('ascii',errors='replace') for i in range(0,len(raw),80)];end=next(i for i,s in enumerate(cards) if s.startswith('END     '));hdr=fits.Header.fromstring(''.join(cards[:end+1]),sep='');offset=((end+1)*80+2879)//2880*2880
                assert all(hdr[x]==cb['hdr'][x] for x in ['NAXIS1','NAXIS2','NAXIS3','CRVAL1','CRVAL2','CDELT1','CDELT2','CRPIX1','CRPIX2','CRPIX3','CRVAL3','CDELT3'])
                # Read the pre-stage beam extension to verify area identity.
                nbytes=hdr['NAXIS1']*hdr['NAXIS2']*hdr['NAXIS3']*4;extpos=offset+((nbytes+2879)//2880)*2880
                exth=get(url,extpos,extpos+5759);eh=fits.Header.fromstring(exth[:2880].decode('ascii'),sep='')
                # Astropy BinTableHDU reads the standalone extension with a synthetic primary.
                size=eh['NAXIS1']*eh['NAXIS2']+eh.get('PCOUNT',0);extfull=get(url,extpos,extpos+((2880+size+2879)//2880)*2880-1)
                import io
                buf=io.BytesIO();fits.PrimaryHDU().writeto(buf);blob=buf.getvalue()+extfull
                with fits.open(io.BytesIO(blob)) as hd:
                    assert np.array_equal(hd[1].data['BMAJ'],cb['bmaj'])
                    assert np.array_equal(hd[1].data['BMIN'],cb['bmin'])
                headers[k]=(hdr,offset,url)
                (OUT/f'pre_header_{k}.txt').write_text(repr(hdr))
            hdr,offset,url=headers[k];nx=hdr['NAXIS1'];ny=hdr['NAXIS2'];x,y=WCS(hdr).celestial.world_to_pixel_values(c.RA_deg,c.Dec_deg);ix,iy=round(float(x)),round(float(y));x0,x1=ix-h,ix+h;y0,y1=iy-h,iy+h
            assert 0<=x0<x1<nx and 0<=y0<y1<ny
            kg=gs[m.owner(gs)==k];loc=kg-1000*k
            def plane(ch):
                a=offset+4*nx*(y0+ny*int(ch));b=offset+4*nx*(y1+ny*int(ch)+1)-1
                data=get(url,a,b)
                return np.frombuffer(data,dtype='>f4').reshape(y1-y0+1,nx)[:,x0:x1+1].astype('f4')
            with cf.ThreadPoolExecutor(max_workers=8) as pool:
                for j,plane_data in enumerate(pool.map(plane,loc)):
                    pre.append(plane_data)
                    if j%200==0:print(r.ID,'subcube',int(k),'channel',j,'/',len(loc),'reserved_MB',round(used/1e6),flush=True)
            post.extend(np.asarray(cb['mm'][int(loc[0]):int(loc[-1])+1,y0:y1+1,x0:x1+1],dtype='f4'))
            major=cb['bmaj'][loc];minor=cb['bmin'][loc];assert np.all((major>50)&(major<120)&(minor>50)&(minor<120))
            areas.extend(np.pi*major*minor/(4*np.log(2))/64);beams.extend(major);coords.extend([[float(x)-x0,float(y)-y0]]*len(loc))
        np.savez_compressed(dest,pre=np.array(pre),post=np.array(post),frequency_hz=m.nu_g(gs),beam_area_pixels=np.array(areas),beam_arcsec=np.array(beams),centres_xy=np.array(coords),radius_arcsec=radius)
        summ.append(dict(ID=r.ID,shape=list(np.array(pre).shape),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),file=str(dest.relative_to(ROOT))))
        print('SAVED',r.ID,'elapsed',round(time.time()-start),'sec',flush=True)
    (OUT/'fetch_summary.json').write_text(json.dumps(dict(reserved_including_retries_bytes=used,cap_bytes=CAP,elapsed_seconds=time.time()-start,outputs=summ,checks=['Pre/post celestial and spectral grids identical','Pre/post beam axes byte-exact equal','Every request HTTP206 and exact Content-Range verified']),indent=2))

if __name__=='__main__':main()
