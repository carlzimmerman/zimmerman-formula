from pathlib import Path
import json,hashlib,sys
root=Path(__file__).resolve().parents[2]
m=json.loads((Path(__file__).parent/'TRANSPORT_MANIFEST.json').read_text())
bad=[]
for e in m['included']:
 p=root/e['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:bad.append(e['path'])
print(json.dumps({'included_checked':len(m['included']),'omitted_local_only':len(m['omitted_local_only']),'failed':bad}))
sys.exit(bool(bad))
