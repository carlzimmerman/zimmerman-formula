"""Complete ECLIPSE x SILO finite coordinate crossmatch with count audit.
The FITS byte range includes every fixed row, but none of its spectral heap.
"""
import argparse,csv,io,json,struct,warnings,zipfile
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1]
ARCSEC=206264.80624709636

def extract():
    path=BASE/'inputs/silo_all1551_fixed_rows.bin';raw=path.read_bytes()
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter('always')
        with fits.open(path,lazy_load_hdus=True) as hd:
            hdr=hd[1].header.copy();offset=hd[1].fileinfo()['datLoc'];dtype=hd[1].columns.dtype.newbyteorder('>')
    nr=hdr['NAXIS2'];width=hdr['NAXIS1'];assert nr==1551 and width==3386 and offset==11520
    assert len(raw)==offset+nr*width and dtype.itemsize==width
    table=np.frombuffer(raw,dtype=dtype,offset=offset,count=nr)
    # Only fixed fields before the variable-array descriptors are accessed.
    fields=list(dtype.names[:28]);rows=[]
    for rr in table:
        d={}
        for k in fields:
            v=rr[k];d[k]=v.decode('ascii').strip() if isinstance(v,bytes) else v.item()
        rows.append(d)
    # Independent struct decoder cross-checks all coordinates and redshifts.
    for name in ['RA','DEC','DETECTION_Z','Z_NOQSO']:
        field_offset=dtype.fields[name][1]
        direct=np.array([struct.unpack_from('>f',raw,offset+i*width+field_offset)[0] for i in range(nr)])
        assert np.array_equal(direct,np.array([r[name] for r in rows]))
    sex=SkyCoord([r['RA_HMS'] for r in rows],[r['DEC_DMS'] for r in rows],unit=(u.hourangle,u.deg))
    numeric=SkyCoord([r['RA'] for r in rows],[r['DEC'] for r in rows],unit=u.deg)
    diff=numeric.separation(sex).arcsec
    assert hdr['TUNIT25'].strip().lower()=='degree' and max(diff)<.3
    assert len(set(r['CATALOG_ID'] for r in rows))==nr
    summary=dict(rows=nr,row_width_bytes=width,fixed_data_start=offset,actual_download_bytes=len(raw),complete_fixed_rows=True,
        omitted_heap_bytes=hdr['PCOUNT'],numeric_RA_unit=hdr['TUNIT25'],numeric_DEC_unit=hdr['TUNIT26'],
        max_numeric_vs_sexagesimal_separation_arcsec=float(max(diff)),spectra_grade_counts=dict(Counter(r['SPECTRA_GRADE'] for r in rows)),
        total_grade_counts=dict(Counter(r['TOTAL_GRADE'] for r in rows)),scan_type_counts=dict(Counter(r['EMLINE_SCAN_TYPE'] for r in rows)),
        redshift_warning_counts=dict(Counter(str(r['ZWARNING_NOQSO']) for r in rows)),unique_coordinate_pairs=len(set((r['RA'],r['DEC']) for r in rows)),
        background_z_greater_than_foreground_count=sum(r['DETECTION_Z']>r['Z_NOQSO'] for r in rows),
        astropy_partial_file_warnings=[str(w.message) for w in ww],
        data_model_discrepancy='HTML labels RA Hours; actual FITS says Degree and all sexagesimal coordinates independently confirm degrees.')
    return rows,summary

def vectors(ra,dec):
    ra,dec=np.deg2rad(ra),np.deg2rad(dec)
    return np.column_stack([np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)])

def check_population(euclid,silo,brute=False):
    er=np.array([float(x['RA_obj']) for x in euclid]);ed=np.array([float(x['DEC_obj']) for x in euclid])
    sr=np.array([x['RA'] for x in silo]);sd=np.array([x['DEC'] for x in silo])
    assert np.isfinite(er).all() and np.isfinite(ed).all() and np.isfinite(sr).all() and np.isfinite(sd).all()
    ev,sv=vectors(er,ed),vectors(sr,sd);tree=cKDTree(sv);dist,nearest=tree.query(ev,k=1)
    sep=2*np.arcsin(np.minimum(dist/2,1))*ARCSEC
    candidates=tree.query_ball_point(ev,2*np.sin((10/ARCSEC)/2));pairs=[]
    for i,indices in enumerate(candidates):
        for j in indices:
            chord=np.linalg.norm(ev[i]-sv[j]);angle=2*np.arcsin(min(chord/2,1))*ARCSEC
            pairs.append((i,j,float(angle)))
    audit=dict(valid_euclid_rows=len(euclid),valid_silo_rows=len(silo),unique_euclid_ids=len(set(x['Unique_Identifier'] for x in euclid)),
        pairs_within_2arcsec=sum(d<=2 for i,j,d in pairs),pairs_within_10arcsec=len(pairs),
        euclid_objects_within_2arcsec=len(set(i for i,j,d in pairs if d<=2)),silo_rows_within_2arcsec=len(set(j for i,j,d in pairs if d<=2)),
        min_separation_arcsec=float(min(sep)),no_quality_filter_before_matching=True)
    if brute:
        # Full Cartesian-product verification: no sky/grade/photo-z prefilter.
        br=[];bs=[];allpairs=[];rad_sr,rad_sd=np.deg2rad(sr),np.deg2rad(sd)
        comparisons=0
        for start in range(0,len(euclid),256):
            r,d=np.deg2rad(er[start:start+256,None]),np.deg2rad(ed[start:start+256,None])
            hav=np.sin((d-rad_sd[None,:])/2)**2+np.cos(d)*np.cos(rad_sd)[None,:]*np.sin((r-rad_sr[None,:])/2)**2
            ang=2*np.arcsin(np.sqrt(np.clip(hav,0,1)))*ARCSEC
            br.extend(np.argmin(ang,axis=1).tolist());bs.extend(np.min(ang,axis=1).tolist());comparisons+=ang.size
            ii,jj=np.where(ang<=10)
            allpairs.extend((int(i+start),int(j)) for i,j in zip(ii,jj))
        assert comparisons==len(euclid)*len(silo)
        assert set(allpairs)=={(i,j) for i,j,d in pairs}
        # Duplicate SILO coordinates can cause tied nearest indices; compare angles.
        difference=float(max(abs(np.array(bs)-sep)));assert difference<2e-5
        audit.update(independent_haversine_pair_evaluations=comparisons,tree_vs_haversine_max_nearest_difference_arcsec=difference,
            tree_vs_haversine_all_pairs_within_10_identical=True)
    def record(i,j,d):
        e=euclid[i];return dict(euclid_id=e['Unique_Identifier'],euclid_name=e.get('euclj_name'),euclid_RA=float(e['RA_obj']),euclid_DEC=float(e['DEC_obj']),
            euclid_expert_grade=e.get('Expert_Grade'),separation_arcsec=d,silo=silo[j])
    return audit,[record(i,j,d) for i,j,d in sorted(pairs,key=lambda x:x[2])], [record(i,int(nearest[i]),float(sep[i])) for i in np.argsort(sep)[:20]],nearest,sep

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);silo,parse=extract()
    screen=ROOT/'euclid_eclipse_screen_2026_11_13/run_02/screen_all_15072.csv'
    with screen.open() as file:euclid=list(csv.DictReader(file))
    assert len(euclid)==15072 and len(set(x['Unique_Identifier'] for x in euclid))==15072
    mainaudit,pairs,nearest20,idx,sep=check_population(euclid,silo,brute=True)
    archive=ROOT/'euclid_eclipse_screen_2026_11_13/inputs/ECLIPSE_object_catalogue.zip'
    with zipfile.ZipFile(archive) as z:
        full=list(csv.DictReader(io.TextIOWrapper(z.open('ECLIPSE_object_catalogue/ECLIPSE_object_catalogue.csv'))))
    assert len(full)==26662 and len(set(x['Unique_Identifier'] for x in full))==26662
    wholeaudit,wholepairs,wholenearest,_,_=check_population(full,silo,brute=False)
    mainids={x['Unique_Identifier'] for x in euclid}
    extra=[x for x in wholepairs if x['euclid_id'] not in mainids]
    for rec in pairs:
        e=next(x for x in euclid if x['Unique_Identifier']==rec['euclid_id'])
        rec['screen_context']={k:e.get(k) for k in ['final_sample','lens_model_success','eclipse_median_phz','eclipse_log_survived_mass_med','source_redshift','source_redshift_origin']}
    with (out/'nearest_per_ECLIPSE.csv').open('w') as file:
        writer=csv.writer(file);writer.writerow(['euclid_id','nearest_silo_catalog_id','separation_arcsec'])
        writer.writerows((e['Unique_Identifier'],silo[int(j)]['CATALOG_ID'],float(d)) for e,j,d in zip(euclid,idx,sep))
    with (out/'SILO_all_fixed_metadata.csv').open('w') as file:
        writer=csv.DictWriter(file,fieldnames=list(silo[0]));writer.writeheader();writer.writerows(silo)
    result=dict(assertion_tested='Full 15072-by-1551 coordinate crossmatch at <=2 arcsec, retaining every pair <=10 arcsec and global nearest diagnostics; separate complete raw 26662-object archive check.',
        parsing_audit=parse,primary_15072_count_audit=mainaudit,primary_matches_within_2arcsec=[x for x in pairs if x['separation_arcsec']<=2],
        primary_all_pairs_within_10arcsec=pairs,primary_global_nearest20=nearest20,raw_archive_26662_count_audit=wholeaudit,additional_raw_archive_pairs_within_10arcsec=extra,
        raw_archive_global_nearest20=wholenearest,
        non_claims=['A spatial match is a candidate association, not validation of every source redshift or image correspondence.',
        'SILO detection redshifts belong to spectroscopic background candidates with individual grades, not uniformly confirmed strong lenses.',
        'No spectral heap or emission-line-analysis HDU was fetched or re-fitted.','No absence claim outside the explicitly matched catalogues and angular radius.',
        'The 26662-object raw archive and 15072-row screen are distinct populations, reported separately.'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if 'nearest20' not in k}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
