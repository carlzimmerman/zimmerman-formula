"""Finite mass/statistics/force checks for the extended common background."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,resource,math
import numpy as np
from common import CommonBackground,CommonOrbit,vector_mass2,extend_numbers,OLD,T0
from generic_orbit import GenericOrbit
sys.path.insert(0,str(OLD/'cascades'))
from angular_fast import exact_events
from averaged import grid

def main(output):
 start=time.monotonic();bg=CommonBackground();q,W=grid(8);model=CommonOrbit(bg,q,W,16);rows=[]
 for x in (.18444259422092926,1.125,3.82758980,4.0786357,25.4000254000381):
  d=bg.at(x);ev=exact_events(d,T0,q,W,source=d['current_source']);Y=model.measure*np.exp(-ev.energy/.02);gas=model.gas(x,0,Y);h=1e-5;fd=float((model.gas(x+h,0,Y)['rho'][0]-model.gas(x-h,0,Y)['rho'][0])/(2*h));analytic=float(gas['force'][0]);vecmeta=np.array([g['kind']=='V' for g in model.groups]);rows.append(dict(x=x,event_field_energy_absolute=float(max(abs(ev.energy-gas['energy'][0]))),force_derivative_relative=abs(fd-analytic)/max(abs(analytic),1e-300),vector_mass_table_relative=abs(d['m_vector']/bg.base.at(x)['m_vector']-1),vector_mass2=float(vector_mass2(x)),vector_force=float(gas['force_by'][0]@vecmeta)))
 node_error=max(abs(vector_mass2(r['x'])-r['m_vector']**2)/max(r['m_vector']**2,1e-300) for r in bg.base.rows)
 initial=json.loads((OLD/'integration/run_initial001/result.json').read_text());oldY=np.array(initial['state']['Y']);newY=extend_numbers(oldY,bg.base.groups,bg.groups,len(q));oldmodel=GenericOrbit(bg.base,q,W,16);embedding=max(abs(model.gas(x,0,newY)['rho'][0]-oldmodel.gas(x,0,oldY)['rho'][0]) for x in (.18444259422092926,3.8275898,25.4000254));vecempty=float(sum(newY.reshape(model.ns,model.n)[25:].ravel()))
 checks=dict(vector_mass_nodes=node_error<2e-13,empty_vector_embedding=embedding<1e-22 and vecempty==0.,thirty_groups=len(model.groups)==30,physical_degrees=sum(g['degeneracy'] for g in model.groups if g['kind']=='V')==60,bosonic_vectors=bool(np.all(model.eta.reshape(model.ns,model.n)[[g['kind']=='V' for g in model.groups]]==1)),event_gas_mass=all(r['event_field_energy_absolute']<2e-16 for r in rows),force_derivative=all(r['force_derivative_relative']<1e-7 for r in rows))
 checks={k:bool(v) for k,v in checks.items()}
 out=dict(claim_id='CC11_COMMON_BACKGROUND',checks=checks,rows=rows,vector_mass2_node_relative=node_error,empty_vector_embedding_energy_absolute=embedding,groups=bg.groups,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Canonical degrees, common masses/statistics and finite gas force. No vector collision amplitudes, no transport or physical population history is asserted.')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
