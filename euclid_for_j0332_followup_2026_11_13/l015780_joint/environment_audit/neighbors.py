from pathlib import Path
import zlib,io,csv,json,numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
p=Path('euclid_for_j0332_followup_2026_11_13/l015780_joint/environment_audit');out=p/'run_01'; target=SkyCoord(151.4073110655*u.deg,67.5075428182*u.deg);zl=.428270373960303;results={}
for v in ['21','30']:
 f=Path('euclid_for_j0332_followup_2026_11_13/l015780_inputs')/f'fastspec_v{v}_first2mb.gz';h=fits.open(io.BytesIO(zlib.decompressobj(31).decompress(f.read_bytes())),ignore_missing_end=True);hd=h['METADATA'];d=hd.data
 assert hd.verify_checksum()==1 and hd.verify_datasum()==1
 assert len(np.unique(d['TARGETID']))==len(d)
 c=SkyCoord(d['RA']*u.deg,d['DEC']*u.deg);sep=c.separation(target).arcsec;dv=299792.458*(d['Z']-zl)/(1+zl);rows=[]
 for j in np.flatnonzero(sep<=600):
  r={k:(d[k][j].item() if hasattr(d[k][j],'item') else str(d[k][j])) for k in ['TARGETID','RA','DEC','Z','ZWARN','DELTACHI2','SPECTYPE','COADD_FIBERSTATUS']};r.update(separation_arcsec=float(sep[j]),dv_rest_kms=float(dv[j]),quality_zwarn0_dchi2gt25_fiber0=bool(d['ZWARN'][j]==0 and d['DELTACHI2'][j]>25 and d['COADD_FIBERSTATUS'][j]==0));rows.append(r)
 rows.sort(key=lambda r:r['separation_arcsec'])
 with open(out/f'neighbors_v{v}.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 good=[r for r in rows if r['quality_zwarn0_dchi2gt25_fiber0'] and r['SPECTYPE'].strip()=='GALAXY' and r['TARGETID']!=39633467440368852]
 results[v]={'metadata_rows':len(d),'checksum':int(hd.verify_checksum()),'datasum':int(hd.verify_datasum()),'within_10arcmin':len(rows),'quality_galaxies_excluding_target':len(good),'within_dv1000':[r for r in good if abs(r['dv_rest_kms'])<=1000],'within_dv3000':[r for r in good if abs(r['dv_rest_kms'])<=3000],'within_10arcsec': [r for r in rows if r['separation_arcsec']<=10]}
(out/'result.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
