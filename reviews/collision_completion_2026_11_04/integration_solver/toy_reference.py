"""Independent immutable holes_v2 scalar BE comparison to 100-digit root."""
from control_v1 import *
def main_toy(out):
 start=time.monotonic();rows=[]
 for small,dt in [(1e-12,1.),(1e-20,1.),(1e-24,1.),(1e-24,1e-21)]:
  print('start',small,dt,flush=True);row=toy_control(small,dt);rows.append(row);result=dict(claim_id='CC10_HOLE_SCALAR_REFERENCE',toy=rows,checks=dict(reference=max(x['relative_hole_error'] for x in rows)<1e-7),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);Path(out).write_text(json.dumps(result,indent=2)+'\n');print('done',row,flush=True)
 assert result['checks']['reference']
if __name__=='__main__':main_toy(sys.argv[1])
