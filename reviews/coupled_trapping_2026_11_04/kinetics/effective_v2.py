"""Rate-feedback sensitivity only: actual terminal charged deficits, no daughters.
Not a charge/energy-complete cascade: massive neutral endpoint force is omitted.
"""
import sys,os
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,time,resource
import numpy as np
from averaged_v2 import Model,evolve,ROOT,HERE
class Effective(Model):
 def __init__(self,*a,fraction='actual',**kw):
  super().__init__(*a,**kw);self.fraction=fraction
  if fraction=='actual':
   raw=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_network001/result.json').read_text())['cases'];xx=np.array([z['x'] for z in raw]);table=[]
   for x in np.linspace(0,40,401):
    i=min(max(0,int(np.searchsorted(xx,x)-1)),len(xx)-2);alpha=min(1,max(0,(x-xx[i])/(xx[i+1]-xx[i])));parents=[]
    for row,w in ((raw[i],1-alpha),(raw[i+1],alpha)):
     for p in row['neutral_parent_groups']:
      eta=max(0.,1-p['terminal_charged_multiplicity']/2)
      if eta>0:parents.append([p['mass'],w*p['multiplicity']*p['to_light_pair']*eta])
    table.append(dict(x=float(x),parents=parents))
   self.tables=table
 def kernel(self,x,t):return super().kernel(x,t)*(1 if self.fraction=='actual' else float(self.fraction))
def main(out,kind,fraction):
 start=time.monotonic();stat=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text());spins=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text());p=next(p for p in stat['points'] if p['kind']==kind);s=next(z for z in spins['points'] if z['kind']==kind)['spins'][0];model=Effective(p,s,bins=32,orbitn=12,fraction=fraction);run=evolve(model,True,math.log(s['TD_over_mu']/.0005),.0006);run.update(kind=kind,mu_GeV=p['mu_GeV'],fraction=fraction)
 result=dict(claim_id='CT09_EFFECTIVE_CASCADE_FEEDBACK',case=run,checks={'integration_reached_cooling':run['reason']=='target cooling reached','energy_ledger':bool(max(abs(h['energy_ledger_error']) for h in run['history'])<.02),'averaging_hierarchy':bool(run['max_rate_over_oscillation']<.1)},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Effective rate diagnostic only. Fraction actual uses max(0,1-terminal_charged/2) from completed empty-final-state rigid tree decay DAG, linear positive interpolation of complete endpoints on its coarse x grid. Pair multiplication discarded. Retained charged carriers stay fermionic in same bins; no returning daughters, scalar conversion, massive-neutral force, photino distribution or Pauli blocking. Sink energy assigned auxiliary radiation ledger to maintain reduced-system accounting; this is not the physical cascade energy closure and not a complete kinetic history.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));print(kind,fraction,run['reason'],run['history'][-1]);assert all(result['checks'].values())
if __name__=='__main__':main(*sys.argv[1:])
