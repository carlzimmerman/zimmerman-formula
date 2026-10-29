import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json,sys,time
import numpy as np
sys.set_int_max_str_digits(100000)
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
paths=[Path(__file__),HERE/'DUAL_CRITERIA.md',HERE/'DUAL_ROUTE.md',HERE/'native_matrix_001/native_matrices.npz',HERE/'signed_dot_002_cached/signed_map_evidence.npz',HERE/'signed_dot_002_cached/results.json',HERE.parent/'CSM1_consistent_core_switch/calibration/run_003_audited/results.json'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in paths};nat=np.load(paths[3]);ev=np.load(paths[4]);assert all(json.loads(paths[5].read_text())['checks'].values());foot=json.loads(paths[6].read_text())['levels']['3.75']['lens']['result']['canonical'];prof=foot['profiles'];C0=nat['C'];T0=nat['T'];C=[[F(float(v)) for v in row] for row in C0];T=[[F(float(v)) for v in row] for row in T0];n=60;checks={};t0=time.monotonic();maxbits=0

def bits(v):
 global maxbits
 maxbits=max(maxbits,v.numerator.bit_length(),v.denominator.bit_length());assert maxbits<=20000,'rational bit limit';return v
check=lambda k,v:checks.update({k:bool(v)})
check('symmetric',all(C[i][j]==C[j][i] for i in range(n) for j in range(n)));assert checks['symmetric']
L=[[F(int(i==j)) for j in range(n)] for i in range(n)];D=[]
for k in range(n):
 dk=bits(C[k][k]-sum((L[k][j]**2*D[j] for j in range(k)),F(0)));assert dk>0,'nonpositive LDL pivot';D.append(dk)
 for i in range(k+1,n):L[i][k]=bits((C[i][k]-sum((L[i][j]*L[k][j]*D[j] for j in range(k)),F(0)))/dk)
print('LDL factor complete',time.monotonic()-t0,flush=True)
check('positive_pivots',all(x>0 for x in D));check('full_covariance_reconstruction',all(sum((L[i][k]*D[k]*L[j][k] for k in range(min(i,j)+1)),F(0))==C[i][j] for i in range(n) for j in range(n)))
Y=[F(float(v)) for v in np.array(prof['data']).ravel()];H=[F(float(v)) for v in np.array(prof['H']).ravel()];law=[F(float(v)) for v in np.array(prof['L']).ravel()];bH=[F(float(v)) for v in foot['all']['H2H']['b']];bL=[F(float(v)) for v in foot['all']['L2H']['b']]
rH=[Y[i]-H[i]-sum((T[i][j]*bH[j] for j in range(4)),F(0)) for i in range(n)];raw=np.linalg.solve(C0,np.array([float(v) for v in rH]));check('witness_finite',np.isfinite(raw).all());aa=[F(float(v)) for v in raw];pivots=[]
for b in range(4):
 ids=[i for i in range(n) if T[i][b]!=0];assert ids and all(T[i][bb]==0 for i in ids for bb in range(4) if bb!=b);pivot=max(ids,key=lambda i:abs(T[i][b]));pivots.append(pivot);aa[pivot]=-sum((aa[i]*T[i][b] for i in ids if i!=pivot),F(0))/T[pivot][b]
check('orthogonal_exact',all(sum((aa[i]*T[i][b] for i in range(n)),F(0))==0 for b in range(4)));den=sum((aa[i]*C[i][j]*aa[j] for i in range(n) for j in range(n)),F(0));check('positive_denominator',den>0)
lo=[F(0) for _ in range(n)];hi=lo.copy();weights=ev['weights'];pb=ev['projected_bounds'];nodes=ev['node_indices']
for j,node in enumerate(nodes):
 for b in range(4):
  w=F(float(weights[b,node]));assert w>=0
  for k in range(15):lo[b*15+k]+=w*F(float(pb[j,b,k,0]));hi[b*15+k]+=w*F(float(pb[j,b,k,1]))
rl=[Y[i]-H[i]-hi[i] for i in range(n)];rh=[Y[i]-H[i]-lo[i] for i in range(n)];nl=sum((aa[i]*(rl[i] if aa[i]>=0 else rh[i]) for i in range(n)),F(0));nh=sum((aa[i]*(rh[i] if aa[i]>=0 else rl[i]) for i in range(n)),F(0));dist=nl if nl>0 else -nh if nh<0 else F(0);bound=dist*dist/den

def score(v):
 z=[]
 for i in range(n):z.append(v[i]-sum((L[i][j]*z[j] for j in range(i)),F(0)))
 return sum((z[i]**2/D[i] for i in range(n)),F(0))
exactH=score(rH);exactLaw=score([Y[i]-law[i]-sum((T[i][j]*bL[j] for j in range(4)),F(0)) for i in range(n)]);point=sum((aa[i]*(Y[i]-H[i]) for i in range(n)),F(0))**2/den
check('point_inequality',point<=exactH);check('law_candidate_feasible',all(x>=0 for x in bL));check('law_diagnostic',abs(float(exactLaw)-foot['all']['L2H']['chi2'])<1e-6);check('numerator_order',nl<=nh);mut=aa.copy();mut[pivots[0]]+=F(1,100);check('mutation_detected',sum((mut[i]*T[i][0] for i in range(n)),F(0))!=0);check('inputs_stable',all(sha(ROOT/f)==h for f,h in hashes.items()))
enc=lambda q:str(q.numerator)+'/'+str(q.denominator)
cert=dict(L=[[enc(v) for v in row] for row in L],D=[enc(v) for v in D],a=[enc(v) for v in aa],pivots=pivots,denominator=enc(den),numerator_box=[enc(nl),enc(nh)],native_residual_boxes=[[enc(rl[i]),enc(rh[i])] for i in range(n)],dual_lower=enc(bound),law_candidate_upper=enc(exactLaw),baseline_candidate_score=enc(exactH),point_dual=enc(point),law_b=[enc(v) for v in bL],baseline_b=[enc(v) for v in bH])
(out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n');result=dict(checks=checks,dual_lower=float(bound),law_upper=float(exactLaw),conservative_cut=float(exactLaw+9),lower_exceeds_law_upper_plus9=bound>exactLaw+9,point_dual=float(point),baseline_candidate_score=float(exactH),max_rational_bits=maxbits,runtime_seconds=time.monotonic()-t0,input_sha256=hashes,original_covariance_nuisance_exact_for_stated_boxes=True,full_model_interval_certified=False,scope='Exact covariance dual lower bound conditional on published anchored fixed-projection native boxes; no real-L or global certificate')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
