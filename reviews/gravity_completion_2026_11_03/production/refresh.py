"""Preferred evidence refresh with the complete imported local source closure."""
import sys,json,time,resource
from pathlib import Path
sys.dont_write_bytecode=True
import controls_v3,physical_transport,final_checks_v2
HERE=Path(__file__).resolve().parent
def scientific(obj):
    if isinstance(obj,dict):return {k:scientific(v) for k,v in obj.items() if k not in ['runtime_seconds','peak_rss_bytes_macos','peak_rss_bytes']}
    if isinstance(obj,list):return [scientific(v) for v in obj]
    return obj
def main(outdir):
    start=time.monotonic();out=Path(outdir)
    controls_v3.main(str(out/'controls.json'))
    physical_transport.main(str(out/'physical.json'))
    final_checks_v2.main(str(out/'checks.json'))
    pairs=[('controls.json','run_controls_v3/result.json'),('physical.json','run_physical/result.json'),('checks.json','run_final_checks_v2/result.json')]
    checks={a+'_matches_retained_science':scientific(json.loads((out/a).read_text()))==scientific(json.loads((HERE/b).read_text())) for a,b in pairs}
    data=dict(claim_id='GC03_FULL_DEPENDENCY_REFRESH',checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='All actual imported local physics sources pinned; exact scientific outputs compared with retained records, excluding only runtime/RSS fields')
    (out/'result.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
