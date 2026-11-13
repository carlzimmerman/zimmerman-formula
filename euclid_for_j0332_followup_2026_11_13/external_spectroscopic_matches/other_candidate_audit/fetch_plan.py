"""Execute an inspected public target-only download plan, preserving attempts."""
import concurrent.futures,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
plan=Path(sys.argv[1]);tasks=json.loads(plan.read_text())
def fetch(t):
    path=Path(t['path']).resolve();assert HERE in path.parents
    argv=[sys.executable,str(HERE.parent/'fetch.py'),t['url'],str(path)]
    if 'byte_range' in t:argv+=['--byte-range',t['byte_range']]
    if 'max_bytes' in t:argv+=['--max-bytes',str(t['max_bytes'])]
    r=subprocess.run(argv,capture_output=True,text=True)
    print(path.name,r.returncode,flush=True)
    return dict(**t,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,tasks))
plan.with_name(plan.stem+'_result.json').write_text(json.dumps(results,indent=2)+'\n')
