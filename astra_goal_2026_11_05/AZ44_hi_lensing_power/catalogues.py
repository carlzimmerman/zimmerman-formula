"""AZ44 catalogue metadata and raw FITS row streaming, never large .data."""
import csv,hashlib,json,os
from pathlib import Path
import numpy as np
from astropy.io import fits
ROOT=Path(__file__).resolve().parents[2]
PATHS=dict(alpha=ROOT.parent/'_external_data/alfalfa_sdss/a100.code12.table2.190808.csv',
 stars=ROOT.parent/'_external_data/alfalfa_sdss/durbala2020-table2.21-Sep-2020.fits.gz',
 fashi=ROOT/'_external_data/fashi_dr2_2026_10_18/fashi_dr2.csv',
 match=ROOT/'_external_data/fashi_dr2_2026_10_18/fashi_alfalfa.csv',
 shear=ROOT.parent/'_external_data/kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits',
 bgs=ROOT.parent/'_external_data/desi_dr1_bgs/BGS_BRIGHT_full_HPmapcut.dat.fits')

def atomic_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def metadata(path,columns):
    with fits.open(path,memmap=True,lazy_load_hdus=True) as h:
        hd=h[1].header;dt=h[1].columns.dtype.newbyteorder('>')
        for name in columns:
            i=h[1].columns.names.index(name)+1
            if 'TSCAL'+str(i) in hd or 'TZERO'+str(i) in hd:raise RuntimeError('Scaled raw FITS column '+name)
        st=path.stat()
        info=dict(name=path.name,size=st.st_size,mtime_ns=st.st_mtime_ns,rows=int(hd['NAXIS2']),
                  rowbytes=int(hd['NAXIS1']),offset=h.fileinfo(1)['datLoc'],
                  header_sha256=hashlib.sha256(hd.tostring().encode()).hexdigest())
    if dt.itemsize!=info['rowbytes']:raise RuntimeError('Raw dtype length mismatch')
    return info,dt

def raw_chunks(path,info,dt,chunk,start=0):
    with path.open('rb') as f:
        f.seek(info['offset']+start*info['rowbytes'])
        for lo in range(start,info['rows'],chunk):
            n=min(chunk,info['rows']-lo);buf=f.read(n*info['rowbytes'])
            if len(buf)!=n*info['rowbytes']:raise RuntimeError('Truncated FITS payload')
            yield lo,np.frombuffer(buf,dtype=dt,count=n),hashlib.sha256(buf).hexdigest()

def lenses():
    # Only this small2.7MB compressed table is materialized.
    with fits.open(PATHS['stars'],memmap=False) as h:
        stars={int(r['AGC']):float(r['logMstarTaylor']) for r in h[1].data}
    with PATHS['alpha'].open() as f:alpha=list(csv.DictReader(f))
    with PATHS['match'].open() as f:cross=list(csv.DictReader(f))
    with PATHS['fashi'].open() as f:fashi=list(csv.DictReader(f))
    fmap={};duplicates=0
    for row in cross:
        key=int(float(row['FASHI_ID']))
        if key in fmap:duplicates+=1
        else:fmap[key]=int(float(row['AGCNr']))
    result=[];seen=set();bad=0;no_stars=0;repeated=0
    def add(agc,ra,dec,z,distance,loghi,survey):
        nonlocal bad,no_stars,repeated
        if agc in seen:repeated+=1;return
        ls=stars.get(agc,float('nan'))
        if not np.isfinite(ls):no_stars+=1;return
        values=[ra,dec,z,distance,loghi]
        if not all(np.isfinite(values)) or distance<=0 or not 0<=ra<360 or not -90<=dec<=90:
            bad+=1;return
        with np.errstate(over='ignore',under='ignore'):
            ms=float(np.power(10.,ls));mh=float(np.power(10.,loghi))
        if not np.isfinite(ms+mh) or ms<=0 or mh<=0:bad+=1;return
        seen.add(agc);fg=1.33*mh/(ms+1.33*mh)
        if fg>.6:result.append(dict(AGC=agc,ra=ra,dec=dec,z=z,distance_Mpc=distance,
                      Mstar=ms,MHI=mh,Mb=ms+1.33*mh,fgas=fg,survey=survey))
    for row in alpha:
        add(int(row['AGCNr']),float(row['RAdeg_HI']),float(row['DECdeg_HI']),float(row['Vhelio'])/299792.458,
            float(row['Dist']),float(row['logMH']),'ALFALFA')
    missing_match=0
    for row in fashi:
        agc=fmap.get(int(float(row['fashi_id'])))
        if agc is None:missing_match+=1;continue
        add(agc,float(row['ra']),float(row['dec']),float(row['z_opt']),float(row['distance']),float(row['mass']),'FASHI')
    summary=dict(alpha_rows=len(alpha),durbala_AGCs=len(stars),fashi_rows=len(fashi),match_rows=len(cross),
                 duplicate_FASHI_match_ids=duplicates,FASHI_without_match=missing_match,
                 repeated_AGC_skipped=repeated,invalid_rows=bad,missing_stellar_mass=no_stars,gas_rich_total=len(result))
    hashes={key:hashlib.sha256(PATHS[key].read_bytes()).hexdigest() for key in ['alpha','stars','fashi','match']}
    return result,summary,hashes
