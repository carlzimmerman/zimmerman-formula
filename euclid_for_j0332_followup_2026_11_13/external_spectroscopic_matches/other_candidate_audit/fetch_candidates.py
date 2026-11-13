"""Public, target-only downloads for three already matched SILO candidates."""
import concurrent.futures
import json
import subprocess
import sys
import warnings
from pathlib import Path
import numpy as np
from astropy.io import fits

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
URL='https://data.sdss.org/sas/dr16/eboss/spectro/lensing/silo/v5_13_0/v5_13_0/1.0.1/silo_eboss_detections-1.0.1.fits'

def main():
    targets=json.loads((HERE/'targets.json').read_text())
    raw=(BASE/'inputs/silo_all1551_fixed_rows.bin').read_bytes()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        with fits.open(BASE/'inputs/silo_all1551_fixed_rows.bin') as h:
            header=h[1].header.copy();dtype=h[1].columns.dtype.newbyteorder('>')
    rows=np.frombuffer(raw,dtype=dtype,offset=11520,count=1551)
    heap=11520+header['NAXIS1']*header['NAXIS2']
    tasks=[]
    for t in targets:
        sid=t['silo']['CATALOG_ID'];row=rows[rows['CATALOG_ID']==sid][0];dest=HERE/t['euclid_id'];dest.mkdir(exist_ok=True)
        plate,mjd,fiber=[t['silo'][k] for k in ['PLATE','MJD','FIBER_INDEX']]
        assert (int(t['silo']['SPECOBJID'])>>38)&0x3ff==fiber
        spec=f'spec-{plate:04d}-{mjd}-{fiber:04d}.fits'
        tasks.append(dict(url=f'https://data.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/{plate:04d}/{spec}',path=str(dest/spec)))
        tile=t['raw_catalogue']['id_str_for_cutout']
        tasks.append(dict(url=f'https://euclid-eclipse-lenses.org/files/_site/lenses/{tile}.json',path=str(dest/'portal_record.json')))
        for field in ['WAVE','FLUX','MODEL_SILO','IVAR_RESCALED','RESIDUAL_FLUX']:
            count,offset=row[field];start=heap+int(offset);stop=start+int(count)*4-1
            assert count>4000 and count<5000
            tasks.append(dict(url=URL,path=str(dest/f'silo{sid}_{field}.bin'),byte_range=f'{start}-{stop}',max_bytes=int(count)*4))
    (HERE/'download_plan.json').write_text(json.dumps(tasks,indent=2)+'\n')
    def fetch(t):
        argv=[sys.executable,str(BASE/'fetch.py'),t['url'],t['path']]
        if 'byte_range' in t:argv+=['--byte-range',t['byte_range'],'--max-bytes',str(t['max_bytes'])]
        result=subprocess.run(argv,capture_output=True,text=True)
        print(t['path'],result.returncode,flush=True)
        return dict(**t,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,tasks))
    (HERE/'download_result.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'tasks':len(tasks),'failed':[x['path'] for x in results if x['returncode']]}))

if __name__=='__main__':main()
