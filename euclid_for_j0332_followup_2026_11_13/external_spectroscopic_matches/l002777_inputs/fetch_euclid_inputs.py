"""Fetch only L002777's released dataset and diagnostic model products."""
import concurrent.futures,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    r=json.loads((HERE/'portal_lens_record.json').read_text());assert r['id']=='Tile102157516RA1412954672915DEC0634238492404'
    tasks=[(tree,name) for tree,files in r['files'].items() for name in files if not name.endswith('.png') or name in ['rgb.png','vis_pix_fit.png','vis_lp_fit.png','vis_lp_image_with_positions.png','segmentation.png','fit_sersic.png']]
    def fetch(item):
        tree,name=item;dest=HERE/tree/name;url='https://euclid-eclipse-lenses.org/files/'+r['id']+'/'+tree+'/'+name
        cmd=[sys.executable,str(HERE.parent/'fetch.py'),url,str(dest),'--max-bytes','12000000']
        process=subprocess.run(cmd,capture_output=True,text=True)
        print(tree+'/'+name,process.returncode,flush=True)
        return dict(path=str(dest.relative_to(HERE)),url=url,returncode=process.returncode,stdout=process.stdout,stderr=process.stderr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(fetch,tasks))
    (HERE/'fetch_euclid_summary.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(int(any(x['returncode'] for x in result)))
