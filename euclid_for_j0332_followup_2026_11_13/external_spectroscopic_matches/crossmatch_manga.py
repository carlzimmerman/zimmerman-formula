"""Supplementary complete MaNGA SILO v1.0.4 overview crossmatch."""
import argparse,csv,io,json,sys,zipfile
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from astropy.io import fits
from crossmatch_silo import check_population,BASE,ROOT

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);path=BASE/'inputs/silo_manga_detections-1.0.4.fits'
    records=[]
    with fits.open(path) as hd:
        h=hd['CANDIDATE_OVERVIEW'];assert len(h.data)==457
        fields=[c.name for c in h.columns if not str(c.format).startswith(('P','Q'))]
        for r in h.data:
            d={k:(r[k].strip() if isinstance(r[k],str) else r[k].item()) for k in fields}
            d.update(RA=d['RA_IFU'],DEC=d['DEC_IFU'],CATALOG_ID=d['BACKGROUND_ID']);records.append(d)
        structure=[dict(extension=h.name,rows=h.header.get('NAXIS2'),columns=h.header.get('TFIELDS')) for h in hd]
    gradecounts=dict(Counter(r['SOURCE_GRADE'] for r in records));assert sum(gradecounts.values())==457
    primary=list(csv.DictReader(open(ROOT/'euclid_eclipse_screen_2026_11_13/run_02/screen_all_15072.csv')));assert len(primary)==15072
    audit,pairs,near,idx,sep=check_population(primary,records,brute=True)
    with zipfile.ZipFile(ROOT/'euclid_eclipse_screen_2026_11_13/inputs/ECLIPSE_object_catalogue.zip') as z:
        full=list(csv.DictReader(io.TextIOWrapper(z.open('ECLIPSE_object_catalogue/ECLIPSE_object_catalogue.csv'))))
    fullaudit,fpairs,fnear,_,_=check_population(full,records,brute=False)
    def rename(rows):
        for r in rows:r['manga']=r.pop('silo')
        return rows
    # All overview rows are matched; SOURCE_GRADE identifies lens candidates,
    # whereas X grades are backgrounds not classified as plausible strong lenses.
    result=dict(assertion_tested='Complete crossmatch against all457 MaNGA v1.0.4 overview rows, with grade information preserved and no prefilter.',
        FITS_structure=structure,overview_source_grade_counts=gradecounts,unique_IFU_coordinates=len(set((r['RA'],r['DEC']) for r in records)),
        primary_15072_count_audit=audit,primary_matches_within10arcsec=rename(pairs),primary_nearest20=rename(near),
        raw_archive_26662_count_audit=fullaudit,raw_archive_matches_within10arcsec=rename(fpairs),raw_archive_nearest20=rename(fnear),
        non_claims=['SOURCE_GRADE X backgrounds are not promoted to strong lenses.','Mean source redshift scatter is not automatically an independent measurement error.',
        'Coordinates are the target IFU center, not individual source emission coordinates.','Variable-array Einstein-radius predictions and spectra are not used.'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    with (out/'all_overview_fixed_metadata.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    print(json.dumps({k:v for k,v in result.items() if 'nearest20' not in k}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
