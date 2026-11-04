"""Independent finite field/event energy matching after source interpolation repair."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from vertices import VertexBackground
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit,T0
from reaction import full_events
from averaged import grid

def main(output):
 start=time.monotonic();table=ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json';bg=ConsistentVertexBackground(table);raw=VertexBackground(table);q,W=grid(8);model=GenericOrbit(bg,q,W,8);rows=[]
 for x in (.125,.18444259422092926,.375,1.025,2.025,3.825,3.83742513487,3.875,4.125,5.125,9.95,25.4000254,30.25,39.75):
  d=bg.at(x);ev=full_events(d,T0,q,W,angles=4,source=d['current_source']);old=raw.at(x);bad=full_events(old,T0,q,W,angles=4,source=old['current_source']);Y=model.measure*np.exp(-ev.energy/.02);gas=model.gas(x,0,Y)
  err=max(abs(ev.energy-gas['energy'][0]));mismatch=max(abs(bad.energy-gas['energy'][0]));f=1/(np.exp(np.minimum(ev.energy/.02,700))-ev.eta);forward,reverse,*_=ev.products(f);db=max(abs(forward-reverse)/np.maximum(forward+reverse,1e-250))
  flux=ev.flux(np.exp(-ev.energy/.02));local=abs(float(ev.energy@np.asarray(ev.S@flux).ravel()))/max(float(np.sum(abs(flux)*ev.energy[ev.index[:,0]])),1e-300)
  rows.append(dict(x=x,event_field_energy_max_absolute=float(err),superseded_max_absolute=float(mismatch),detailed_balance_relative=float(db),local_energy_relative=local))
 checks=dict(common_energy=all(r['event_field_energy_max_absolute']<2e-16 for r in rows),detailed_balance=all(r['detailed_balance_relative']<2e-11 for r in rows),local_energy=all(r['local_energy_relative']<1e-12 for r in rows))
 out=dict(claim_id='CC10_COMMON_MASS_ENERGY_CONTROL',checks=checks,rows=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite field/event consistency after common-mass wrapper. Width interpolation remains a separate finite approximation. Does not certify angular/radial continuum convergence or common physical history.')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
