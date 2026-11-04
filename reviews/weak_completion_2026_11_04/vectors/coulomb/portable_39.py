import sys,json,time,resource,hashlib
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'));import numpy as np,scipy
from elastic_builder_v3 import event_arrays_chunked
from binary_events_v2 import BinaryEvents
from scalar_factory_v3 import scalar_events
from common import CommonBackground

def main(out):
 start=time.monotonic();r=json.loads((HERE.parent/'run_portable313001/result.json').read_text());q=np.array(r['q']);W=np.array(r['W']);f=np.array(r['f']);a=event_arrays_chunked(q,W,r['T'],r['m'],np.array(r['md2']),incoming_angles=8,azimuth=2,log_order=2,max_log_span=3.);hashes={k:hashlib.sha256(a[k].tobytes()).hexdigest() for k in r['fingerprints']};equal={k:hashes[k]==r['fingerprints'][k] for k in hashes};ev=BinaryEvents(a['index'],a['weights'],a['coefficient'],a['measure'],a['energy'],a['eta'],a['groups']);rhs=ev.number_rhs(f);J=ev.number_jacobian(f).toarray();d=CommonBackground().at(25.4000254000381);fg=np.full((30,len(q)),1e-45);fg[0]=f;g=scalar_events(d,r['T'],q,W,fg.ravel());R=g.number_rhs(fg.ravel());GJ=g.number_jacobian(fg.ravel()).toarray();errors=dict(local_RHS=float(np.linalg.norm(rhs-r['local_rhs'])/np.linalg.norm(rhs)),local_Jacobian=float(np.linalg.norm(J-r['local_jacobian'])/np.linalg.norm(J)),common_RHS=float(np.linalg.norm(R-r['global_rhs'])/np.linalg.norm(R)),common_Jacobian=float(np.linalg.norm(GJ[:len(q),:len(q)]-r['global_Sc_jacobian'])/np.linalg.norm(GJ[:len(q),:len(q)])),common_mass=abs(d['groups'][0]['mass']/r['global_mass']-1));checks=dict(portable_import=True,geometry_bitwise=bool(equal['index'] and equal['weights']),coefficient_bitwise=bool(equal['coefficient']),numerical_parity=bool(max(errors.values())<1e-10))
 Path(out).write_text(json.dumps(dict(interpreter=sys.version,numpy=np.__version__,scipy=scipy.__version__,fingerprints_equal=equal,errors=errors,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ActualrootXcodePython3.9buildandcommon30embeddingversusaccepted3.13coefficients/RHS/Jacobian; oldstarred-subscriptfilesnotimported.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
