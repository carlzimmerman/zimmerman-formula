import sys,json,time,resource,math,hashlib
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'));import numpy as np,scipy
import elastic_builder_v2 as old
import elastic_builder_v3 as new
from binary_events_v2 import BinaryEvents
from scalar_factory_v3 import scalar_events
from common import CommonBackground

def main(out):
 start=time.monotonic();s=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());q,W,cell=new.grid(np.array(s['q_edges']),1);f=np.full(len(q),1e-45);f[cell>=0]=2*np.array(s['final_fS'])[cell[cell>=0]];m=.003/2*math.sqrt(25.4000254000381**2+2/(31*.003));T=1e-6;md=new.screening(q,W,f,T,m);kw=dict(incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.);a=old.event_arrays_chunked(q,W,T,m,md,**kw);b=new.event_arrays_chunked(q,W,T,m,md,**kw);fields=('index','weights','coefficient','measure','energy');equal={k:bool(np.array_equal(a[k],b[k])) for k in fields};hashes={k:hashlib.sha256(b[k].tobytes()).hexdigest() for k in fields};ev=BinaryEvents(b['index'],b['weights'],b['coefficient'],b['measure'],b['energy'],b['eta'],b['groups']);rhs=ev.number_rhs(f);jac=ev.number_jacobian(f).toarray();del a,b,ev;d=CommonBackground().at(25.4000254000381);fg=np.full((30,len(q)),1e-45);fg[0]=f;e=scalar_events(d,T,q,W,fg.ravel());R=e.number_rhs(fg.ravel());J=e.number_jacobian(fg.ravel()).toarray();checks=dict(source_rewrite_bitwise=all(equal.values()),embedding=bool(np.all(R[len(q):]==0)))
 Path(out).write_text(json.dumps(dict(interpreter=sys.version,numpy=np.__version__,scipy=scipy.__version__,q=q.tolist(),W=W.tolist(),f=f.tolist(),m=m,T=T,md2=md.tolist(),old_vs_portable_equal=equal,fingerprints=hashes,local_rhs=rhs.tolist(),local_jacobian=jac.tolist(),global_rhs=R.tolist(),global_Sc_jacobian=J[:len(q),:len(q)].tolist(),global_mass=d['groups'][0]['mass'],checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
