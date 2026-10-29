"""Independent normal-equation check of the completed QR/whitening preflight."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import hashlib,json
import numpy as np
p=Path(__file__).resolve().parent;root=p.parents[1]
paths=[p/'native_matrix_001/results.json',p/'native_matrix_001/native_matrices.npz',root/'rebuild_2026_10_22/CSM1_consistent_core_switch/calibration/run_003_audited/results.json',root/'rebuild_2026_10_22/CSM1_consistent_core_switch/calibration/run_004_replay/results.json',Path(__file__)]
hashes={str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
d=json.loads(paths[0].read_text());a=np.load(paths[1]);C,T=a['C'],a['T'];ci=np.linalg.inv(C);g=np.einsum('ia,ij,jb->ab',T,ci,T);ct=np.einsum('ij,ja->ia',ci,T);K=ci-np.einsum('ia,aj->ij',ct,np.linalg.solve(g,ct.T));assert all(np.all(np.isfinite(x)) for x in (ci,g,ct,K))
saved={}
for f in paths[2:4]:saved.update({str(float(k)):v for k,v in json.loads(f.read_text())['levels'].items()})
checks={};errors=[]
for r in d['records']:
 pro=saved[r['L']]['lens']['result'][r['foot']]['profiles'];z=np.array(pro['data']).ravel()-np.array(pro['H']).ravel();v=float(np.einsum('i,ij,j->',z,K,z));err=abs(v-r['free']);errors.append(err);checks[r['L']+'|'+r['foot']]=bool(np.isfinite(v) and err<1e-8)
checks['matrix_finite']=bool(np.all(np.isfinite(K)));checks['positive_semidefinite_tolerance']=bool(np.linalg.eigvalsh((K+K.T)/2).min()>-1e-8);checks['native_count']=sum(r['n'] for r in d['inventory'])==181431 and d['distinct_positive_nodes']==127
# Constraint boundary is real: the alt L=3.75 unrestricted fit is negative
# in bin1 and has a strictly smaller score. Requiring equality would be wrong.
r=next(x for x in d['records'] if x['L']=='3.75' and x['foot']=='alt');checks['constraint_boundary']=r['unrestricted_amplitudes'][0]<0 and r['free']<r['constrained']
result=dict(checks=checks,max_absolute_normal_equation_error=max(errors),input_sha256=hashes,review='Self/adversarial algebraic implementation review; not independent-agent or interval proof review',limitations=['Floating point validation, not outward-rounded interval certification','No mapping from an L interval to bounded predictions yet','No additional fitted parameter or passing witness'])
(p/'native_matrix_review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
