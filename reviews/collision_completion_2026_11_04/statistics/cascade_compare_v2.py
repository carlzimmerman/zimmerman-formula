"""Radial 40->60 control for the actual quantum/classical cascade comparison."""
import sys,json,time,resource
sys.dont_write_bytecode=True
from pathlib import Path
from cascade_compare_v1 import *

def run_refined(out):
 start=time.monotonic();base=json.loads((ROOT/'reviews/collision_completion_2026_11_04/statistics/run_cascade_compare001/result.json').read_text());q,W=grid(12);cases=[];checks={}
 def save():
  Path(out).write_text(json.dumps(dict(claim_id='CC10_CASCADE_QUANTUM_CLASSICAL_V2',checks=checks,cases=cases,q=q.tolist(),W=W.tolist(),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
 for x in [3.,5.]:
  data=table(x);ev=full_events(data,.004,q,W,angles=6,source=background(x));scale=next(g for g in data['groups'] if g['id']=='S8_1')['width'];runs=[simulate(ev,mode,scale) for mode in ['quantum','classical']];baseline=next(c for c in base['cases'] if c['x']==x);changes=[]
  for r in runs:
   old=next(z for z in baseline['runs'] if z['mode']==r['mode'])['history'][-1];new=r['history'][-1]
   changes.append(dict(mode=r['mode'],relative={k:new[k]/old[k]-1 for k in ['charged_fraction','U1_yield','U1_mean_p_over_mu','neutral_force','neutral_massive_energy']}))
  A=runs[0]['history'][-1];B=runs[1]['history'][-1];ratios={k:A[k]/B[k] for k in ['charged_fraction','U1_yield','U1_mean_p_over_mu','neutral_force','neutral_massive_energy']}
  cases.append(dict(x=x,Tc=.004,runs=runs,radial_relative_changes=changes,quantum_over_classical=ratios,scale_B3_width=scale));save()
 checks.update(completed=all(r['success'] for c in cases for r in c['runs']),energy=max(abs(h['energy_relative_error']) for c in cases for r in c['runs'] for h in r['history'])<1e-7,positive=min(h['min_f'] for c in cases for r in c['runs'] for h in r['history'])>-1e-7,quantum_pauli=max(h['max_fermion_f'] for c in cases for r in c['runs'] if r['mode']=='quantum' for h in r['history'])<1+1e-7,radial_U1_yield=max(abs(ch['relative']['U1_yield']) for c in cases for ch in c['radial_relative_changes'])<.05)
 save();print(json.dumps(checks),flush=True);assert all(checks.values())
if __name__=='__main__':run_refined(sys.argv[1])
