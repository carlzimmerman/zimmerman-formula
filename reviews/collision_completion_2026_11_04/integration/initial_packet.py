"""Declared FD-only initial condition on the common leading gravity packet."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'))
from averaged import grid
from consistent_background import ConsistentVertexBackground
from generic_orbit import GenericOrbit
from holes_v2 import QuantumState

def main(output):
 start=time.monotonic();bg=ConsistentVertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');q,W=grid(8);model=GenericOrbit(bg,q,W,8);Y,orb=model.initial(1e-35);state=QuantumState(model.measure,model.eta,Y=Y);h=model.summary(0,Y,orb);h['charged_fraction']=1.;g0=float(orb['weights']@orb['gas']['rho'])
 checks=dict(physical_bounds=bool(min(state.arrays()[0])>=0 and max(state.arrays()[0][model.eta<0])<1),initial_turning_point=abs(orb['x_inner']-.18444259422092926)<1e-9,retained_orbit=orb['x_outer']<model.xhi,positive_action=orb['J']>0)
 out=dict(claim_id='CC10_COMMON_FD_INITIAL_PACKET',checks=checks,case=dict(q=q.tolist(),W=W.tolist(),history=[h],groups=[g['id'] for g in model.groups],seed=1e-35),state=dict(Y=Y.tolist(),Z=state.Z.tolist(),hole_flags=state.holes.tolist(),N=0.,E=orb['E'],E0=orb['E'],work=0.,J0=orb['J'],gas0=g0,initialY=Y.tolist(),xmid=orb['xmid']),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Declared initial condition and positive classical orbit, not a derivation of thermal production or an evolved abundance. InitialFDforce momentum quadrature controlled separately; no asymptotic occupation assumed.')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=checks,initial=h)));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
