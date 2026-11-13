"""Fetch only eight observed variable-array byte ranges for SILO790."""
import concurrent.futures,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
URL='https://data.sdss.org/sas/dr16/eboss/spectro/lensing/silo/v5_13_0/v5_13_0/1.0.1/silo_eboss_detections-1.0.1.fits'
RANGES={'WAVE':(19865150,19883637),'FLUX':(48486266,48504753),'IVAR':(77107382,77125869),'AND_MASK':(105728498,105746985),'OR_MASK':(134349614,134368101),'MODEL_SILO':(220212962,220231449),'IVAR_RESCALED':(248834078,248852565),'RESIDUAL_FLUX':(277455194,277473681)}
def fetch(item):
    name,(a,b)=item;dest=HERE/f'silo790_{name}.bin'
    cmd=[sys.executable,str(HERE.parent/'fetch.py'),URL,str(dest),'--byte-range',f'{a}-{b}','--max-bytes',str(b-a+1)]
    r=subprocess.run(cmd,capture_output=True,text=True);return dict(field=name,returncode=r.returncode,output=r.stdout,stderr=r.stderr)
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,RANGES.items()))
    (HERE/'silo790_fetch_summary.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps([{'field':r['field'],'returncode':r['returncode']} for r in results]));raise SystemExit(int(any(r['returncode'] for r in results)))
