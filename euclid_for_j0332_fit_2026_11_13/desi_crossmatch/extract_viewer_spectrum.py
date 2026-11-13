from pathlib import Path
import json,re,base64,gzip,hashlib,numpy as np
P=Path(__file__).resolve().parent;f=P/'target_spectrum_page.html';j=json.loads(re.search(r'<script type="application/json"[^>]*>(.*?)</script>',f.read_text(),re.S).group(1));arrays={};meta={}
def decode(x):
 if isinstance(x,dict) and x.get('type')=='ndarray':
  if isinstance(x['array'],list):return np.array(x['array'])
  raw=base64.b64decode(x['array']['data']);raw=gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw;return np.frombuffer(raw,dtype=np.dtype(x['dtype']).newbyteorder('<')).reshape(x['shape'])
 return x

def walk(o):
 if isinstance(o,dict):
  if o.get('name')=='ColumnDataSource' and 'data' in o.get('attributes',{}):
   a=o['attributes'];d=dict(a['data'].get('entries',[]));band=a.get('name')
   if band in ['b','r','z']:
    for k in ['origwave','origflux0','orignoise0']:arrays[band+'_'+k]=decode(d[k])
   if 'TARGETID' in d and 'Z' in d:
    for k,v in d.items():
     v=decode(v);meta[k]=v.tolist() if hasattr(v,'tolist') else v
  for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
walk(j)
np.savez_compressed(P/'L015780_viewer_spectrum.npz',**arrays);(P/'L015780_viewer_metadata.json').write_text(json.dumps(meta,indent=2));(P/'viewer_extraction_provenance.json').write_text(json.dumps(dict(url='https://www.legacysurvey.org/viewer/desi-spectrum/dr1/targetid39633467440368852',html_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),extraction='Decoded Bokeh origwave,origflux0,orignoise0 ndarray bytes; no resampling or line interpretation',output_sha256=hashlib.sha256((P/'L015780_viewer_spectrum.npz').read_bytes()).hexdigest(),caveat='Viewer values not fullFITS product: no resolution matrices/maskbitvectors. Not independent source-redshift measurement.'),indent=2));print({k:np.shape(v) for k,v in arrays.items()});print({k:meta[k] for k in ['TARGETID','Z','ZERR','SPECTYPE','VI_z','VI_comment'] if k in meta})
