from pathlib import Path
import json,zlib,io,warnings,hashlib,datetime,math
from astropy.io import fits
import numpy as np
P=Path(__file__).resolve().parent;out={};prov=[]
for ver,label in [('21','2.1'),('30','3.0')]:
 f=P/f'fastspec_v{ver}_first2mb.gz';raw=zlib.decompressobj(16+zlib.MAX_WBITS).decompress(f.read_bytes());h=fits.open(io.BytesIO(raw),ignore_missing_end=True,lazy_load_hdus=True);entry={'primary_header':dict(h[0].header),'tables':{}}
 for hd in h:
  if hd.name=='MODELS':break
  if hd.name in ['METADATA','FASTSPEC','SPECPHOT']:
   data=hd.data;ind=np.flatnonzero(data['TARGETID']==39633467440368852);assert len(ind)==1
   keys=[k for k in ['TARGETID','LOGMSTAR','LOGMSTAR_IVAR','SFR','SFR_IVAR','VDISP','VDISP_IVAR','RCHI2','RCHI2_PHOT','APERCORR','APERCORR_G','APERCORR_R','APERCORR_Z','FLUX_G','FLUX_R','FLUX_Z','FLUX_W1','FLUX_W2'] if k in hd.columns.names];r=data[ind[0]];entry['tables'][hd.name]={'row_index':int(ind[0]),'row_count':len(data),'values':{k:r[k].item() if hasattr(r[k],'item') else str(r[k]) for k in keys},'units':{k:hd.columns[k].unit for k in keys},'checksum_valid':int(hd.verify_checksum()),'datasum_valid':int(hd.verify_datasum())}
 out[label]=entry;prov.append({'file':f.name,'url':f'https://data.desi.lbl.gov/public/dr1/vac/dr1/fastspecfit/iron/v{label}/healpix/main/bright/75/7582/fastspec-main-bright-7582.fits.gz','request_range':'bytes=0-2097151','bytes':f.stat().st_size,'sha256_partial_bytes':hashlib.sha256(f.read_bytes()).hexdigest(),'note':'Partialgzipstream;completeverifiedtableHDUsparsed,MODELSdeliberatelynotretrieved'})
(P/'fastspec_range_audit.json').write_text(json.dumps(out,indent=2));(P/'fastspec_range_provenance.json').write_text(json.dumps(prov,indent=2));print({v:{k:x['values'] for k,x in r['tables'].items() if k!='METADATA'} for v,r in out.items()})
assert out['2.1']['tables']['FASTSPEC']['values']['LOGMSTAR']==11.347301483154297
