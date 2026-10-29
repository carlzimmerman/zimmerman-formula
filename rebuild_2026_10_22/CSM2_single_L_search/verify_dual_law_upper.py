"""Independent exact solve and residual validation of the law candidate upper."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
import numpy as np
sys.set_int_max_str_digits(100000)
p=Path(__file__).resolve().parent;r=p.parents[1];files=[Path(__file__),p/'exact_dual_001/certificate.json',p/'native_matrix_001/native_matrices.npz',p.parent/'CSM1_consistent_core_switch/calibration/run_003_audited/results.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};c=json.loads(files[1].read_text());nat=np.load(files[2]);f=json.loads(files[3].read_text())['levels']['3.75']['lens']['result']['canonical'];C=[[F(float(v)) for v in row] for row in nat['C']];T=[[F(float(v)) for v in row] for row in nat['T']];L=[[F(v) for v in row] for row in c['L']];D=list(map(F,c['D']));b=list(map(F,c['law_b']));y=list(map(lambda v:F(float(v)),np.array(f['profiles']['data']).ravel()));m=list(map(lambda v:F(float(v)),np.array(f['profiles']['L']).ravel()));res=[y[i]-m[i]-sum((T[i][j]*b[j] for j in range(4)),F(0)) for i in range(60)];forward=[]
for i in range(60):forward.append(res[i]-sum((L[i][j]*forward[j] for j in range(i)),F(0)))
x=[F(0) for _ in range(60)]
for i in range(59,-1,-1):x[i]=forward[i]/D[i]-sum((L[j][i]*x[j] for j in range(i+1,60)),F(0))
checks=dict(exact_solve_residual=all(sum((C[i][j]*x[j] for j in range(60)),F(0))==res[i] for i in range(60)),law_upper_matches_certificate=sum((res[i]*x[i] for i in range(60)),F(0))==F(c['law_candidate_upper']),inputs_stable=all(sha(r/f)==h for f,h in hashes.items()));result=dict(checks=checks,input_sha256=hashes,scope='Exact law candidate quadratic, solved then verified against all original covariance rows')
(p/'dual_law_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(checks);assert all(checks.values())
