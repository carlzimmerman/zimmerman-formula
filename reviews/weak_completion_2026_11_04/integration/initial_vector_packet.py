"""Embed the declared FD initial gas with physically empty vector species."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,resource
import numpy as np
from common import CommonBackground,extend_numbers,OLD
from precise_common import PreciseCommonOrbit
from split_energy_v7 import QuantumState

def main(output):
 start=time.monotonic();prior=json.loads((OLD/'integration/run_initial001/result.json').read_text());q=np.array(prior['case']['q']);W=np.array(prior['case']['W']);bg=CommonBackground();model=PreciseCommonOrbit(bg,q,W,8);Y=extend_numbers(prior['state']['Y'],bg.base.groups,bg.groups,len(q));E=float(prior['state']['E']);orb=model.orbit(0.,Y,E=E,commit=True);model.J0=orb['J'];state=QuantumState(model.measure,model.eta,Y=Y);row=model.summary(0.,Y,orb);gas0=float(orb['weights']@orb['gas']['rho']);checks=dict(energy_identical=abs(orb['E']-prior['state']['E'])<1e-24,vectors_initially_empty=bool(np.all(Y.reshape(30,len(q))[25:]==0)),physical_statistics=bool(np.all(model.eta.reshape(30,len(q))[25:]==1)),initial_turning=abs(orb['x_inner']-.18444259422092926)<1e-9)
 out=dict(claim_id='CC11_FRESH_VECTOR_INITIAL_PACKET',checks={k:bool(v) for k,v in checks.items()},case=dict(q=q.tolist(),W=W.tolist(),groups=[g['id'] for g in bg.groups],history=[row]),state=dict(Y=Y.tolist(),Z=state.Z.tolist(),hole_flags=state.holes.tolist(),N=0.,J=orb['J'],J0=orb['J'],E=orb['E'],initialY=Y.tolist(),gas0=gas0,xmid=orb['xmid'],matched_initial_energy=orb['E'],matched_independent_work=0.),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Fresh declared FD charged-fermion initial state and empty physical vector populations, no evolved abundance or production assertion.')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=out['checks'],initial=row)));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
