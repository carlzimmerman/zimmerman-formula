import json,urllib.request,hashlib,datetime,concurrent.futures,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
r=json.loads((root/'portal_lens_record.json').read_text())
base='https://euclid-eclipse-lenses.org/files/'+r['id']
tasks=[(tree,f) for tree,files in r['files'].items() for f in files if not f.endswith('.png') or f in ['rgb.png','vis_pix_fit.png','segmentation.png']]
def fetch(task):
 tree,name=task;url=base+'/'+tree+'/'+name;dst=root/tree/name;dst.parent.mkdir(parents=True,exist_ok=True)
 subprocess.run(["curl","-sSfL","--max-time","60","-D",str(dst)+".headers","-o",str(dst),url],check=True)
 data=dst.read_bytes();headers=Path(str(dst)+".headers").read_text()
 return dict(path=str(dst.relative_to(root)),url=url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_headers=headers)
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for value in pool.map(fetch,tasks): results.append(value);print(value['path'],value['bytes'],flush=True)
(root/'fetch_provenance.json').write_text(json.dumps(results,indent=2)+'\n')
print('DONE',len(results),sum(x['bytes'] for x in results))
