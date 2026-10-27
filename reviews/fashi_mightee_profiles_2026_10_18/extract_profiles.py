"""Read small apertures from existing public cubes; no cube-sized allocations."""
from pathlib import Path
import importlib.util, json, hashlib, time
import numpy as np
import pandas as pd
from astropy.io import fits

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'_external_data/hi_profiles_2026_10_18'
spec=importlib.util.spec_from_file_location('m302',ROOT/'campaign_fresh_gravity/CFG302_mightee_cube_raw_widths/cfg302_raw_widths.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def main():
    start=time.time();cubes=m.load_cubes();ng=m.NG;own=m.owner(np.arange(ng))
    for cb in cubes:
        h=cb['hdr'];first=h['CRVAL3']+(1-h['CRPIX3'])*h['CDELT3']
        assert abs(first-m.nu_g(1000*cb['k']))<1
        assert abs(h['CDELT3']-m.DNU)*1055<1
        assert h['BUNIT'].strip()=='Jy/beam'
    major=np.array([cubes[own[g]]['bmaj'][g-1000*own[g]] for g in range(ng)])
    minor=np.array([cubes[own[g]]['bmin'][g-1000*own[g]] for g in range(ng)])
    valid=(major>=50)&(major<=120)&(minor>=50)&(minor<=120)
    maj=np.where(valid,major,[np.median(major[(own==k)&valid]) for k in own])
    mi=np.where(valid,minor,[np.median(minor[(own==k)&valid]) for k in own])
    area=np.pi*maj*mi/(4*np.log(2))/m.PIX**2
    matches=pd.read_csv(ROOT/'reviews/fashi_mightee_flux_2026_10_18/run_02/matched_sources.csv')
    cat=pd.read_csv(m.CAT).set_index('ID_catalogue')
    rows=[]
    for _,r in matches[matches.agc.notna()].iterrows():
        c=cat.loc[r.ID];nu=c.freq_MHz*1e6
        a=max(0,int(np.floor(m.g_of_nu(m.nu_of_v(nu,2200)))));b=min(ng-1,int(np.ceil(m.g_of_nu(m.nu_of_v(nu,-2200)))))
        if a>b:
            rows.append(dict(ID=r.ID,agc=int(r.agc),excluded='Frequency outside downloaded 1290-1396 MHz MIGHTEE cubes',frequency_center_mhz=float(c.freq_MHz)))
            print(r.ID,'OUTSIDE CUBE FREQUENCY COVERAGE',flush=True)
            continue
        gs=np.arange(a,b+1)
        line=np.abs(m.C*(nu/m.nu_g(gs)-1))<=max(1.5*c.W_50_km_s,300)
        beam=float(np.median(maj[gs[line]]))
        payload={'frequency_mhz':m.nu_g(gs)/1e6,'beam_valid':valid[gs]}
        flags=[]
        for mult,key in [(1.5,'m15'),(2.5,'m25')]:
            _,y,pt,edge,info=m.aperture_spectrum(cubes,c.RA_deg,c.Dec_deg,a,b,mult*beam,maj,area)
            payload[key]=y;payload[key+'_point_fraction']=pt
            flags.append(dict(aperture=key,edge=edge,info=info))
        with fits.open(OUT/f'A{int(r.agc):06d}.fits') as h:
            d=h[1].data
            for field,key in [('FREQUENCY','a_frequency_mhz'),('FLUX','a_flux_mjy'),('BASELINE','a_baseline_mjy'),('WEIGHT','a_weight'),('VHELIO','a_vhelio')]:
                payload[key]=np.array(d[field],float)
            ah=dict(h[1].header)
        fn=OUT/(r.ID+'.npz');np.savez_compressed(fn,**payload)
        rows.append(dict(ID=r.ID,agc=int(r.agc),frequency_center_mhz=float(c.freq_MHz),beam_arcsec=beam,n_channels=len(gs),invalid_beam_channels=int((~valid[gs]).sum()),apertures=flags,sha256=hashlib.sha256(fn.read_bytes()).hexdigest(),alfalfa_header={k:v for k,v in ah.items() if k not in ['HISTORY','COMMENT']}))
        print(r.ID,len(gs),flush=True)
    sources=[]
    for cb in cubes:
        st=Path(cb['path']).stat()
        sources.append(dict(path=cb['path'],size=st.st_size,mtime_ns=st.st_mtime_ns,frequency_frame=cb['hdr'].get('SPECSYS'),header=repr(cb['hdr']),beam_unit=cb['tunit']))
    (OUT/'extraction_manifest.json').write_text(json.dumps(dict(elapsed_seconds=time.time()-start,source_cubes=sources,rows=rows,source_hashes_reference='../_external_data/mightee_hi_dr1/FETCH_MANIFEST.jsonl',limitation='Cube hashes taken from historical download manifest, not rehashed in this extraction; recorded size/mtime and headers. Extracted arrays are separately hash-pinned.'),indent=2))

if __name__=='__main__':main()
