import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,inspect,json,sys,time
import numpy as np
from mpmath import iv
sys.set_int_max_str_digits(100000)
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);iv.dps=50;t0=time.monotonic()
source=HERE.parent/'F2_outer_lensing/f2_aqual.py';cache=HERE/'source_audit_numpy_1_26_4';files=[Path(__file__),HERE/'FORWARD_ERROR_CRITERIA.md',HERE/'FORWARD_ERROR_DERIVATION.md',cache/'compiled_base.c',cache/'installed_gradient.py.txt',cache/'SOURCE.json',cache/'numpy_LICENSE.txt',HERE/'projection_anchor_001/projection_primitive_enclosures.npz',HERE/'mass_enclosure_001/outward_mass_vectors.npz',HERE/'native_matrix_001/native_matrices.npz',HERE/'projection_dual_inflation.json',HERE/'exact_dual_001/certificate.json',source];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in files};z=np.load(files[7]);mass=np.load(files[8]);nat=np.load(files[9]);proj={k:z[k] for k in z.files};weights=nat['weights'];mass_upper=mass['upper'];halo_nodes=mass['node_indices'];lookup={int(i):j for j,i in enumerate(halo_nodes)};nodes=proj['node_indices'];profiles=proj['node_mass'];flags=proj['node_halo'];lr=proj['log_radius'];rg=proj['radius'];ch=proj['cosh'];sh=proj['sinh'];th=proj['tanh'];w=proj['weight'];N=2*len(w)+128;u=iv.mpf(2)**-50;eta=iv.mpf(2)**-1022;gamma=N*u/(1-N*u);amplify=1/(1-N*u);pi=iv.mpf(float(np.pi));checks={};conversion=True
check=lambda k,v:checks.update({k:bool(v)})
def cast(q):
 global conversion
 a=float(np.nextafter(float(q.a),-np.inf));b=float(np.nextafter(float(q.b),np.inf));assert np.isfinite([a,b]).all();conversion &= bool(iv.mpf(a)<=q.a and iv.mpf(b)>=q.b);return a,b
check('version_and_gradient',np.__version__=='1.26.4' and inspect.getsource(np.gradient)==files[4].read_text());csource=files[3].read_text();check('interp_source_guard',all(t in csource for t in ['(dy[i+1] - dy[i]) / (dx[i+1] - dx[i])','dres[i] = slope*(x_val - dx[j]) + dy[j];','else if (dx[j] == x_val)']))
dx=np.diff(lr);check('Sterbenz_steps',np.all(lr[1:]/lr[:-1]<=2) and np.all(lr[1:]/lr[:-1]>=.5) and np.all(dx>0) and np.all(dx[1:]/dx[:-1]<=2) and np.all(dx[1:]/dx[:-1]>=.5));aa=-dx[1:]/(dx[:-1]*(dx[:-1]+dx[1:]));bb=(dx[1:]-dx[:-1])/(dx[:-1]*dx[1:]);cc=dx[:-1]/(dx[1:]*(dx[:-1]+dx[1:]));coef=np.r_[aa,bb,cc,1-dx*0,1-th];nz=abs(coef[coef!=0]);check('normal_coefficient_prep',np.isfinite(coef).all() and nz.min()>np.finfo(float).tiny and abs(coef).max()<1e280)
# Positive, profile-aware envelopes aggregate the error bound before projection.
S=[[[iv.mpf(0) for _ in rg] for b in range(4)] for tail in range(2)];W=[[iv.mpf(0) for _ in range(4)] for _ in range(2)]
for j,node in enumerate(nodes):
 tail=0 if flags[j] else 1;v=mass_upper[2*lookup[int(node)]+1] if flags[j] else profiles[j];assert np.isfinite(v).all() and np.all(v>=0)
 for b in range(4):
  ww=iv.mpf(float(weights[b,node]));assert ww.a>=0;W[tail][b]+=ww
  if weights[b,node]==0:continue
  for k,m in enumerate(v):S[tail][b][k]+=ww*iv.mpf(float(m))
X=[iv.mpf(float(v)) for v in lr];RR=[iv.mpf(float(v)) for v in rg];D=[];GV=[]
D.append([(0,1/(X[1]-X[0])/RR[0]),(1,1/(X[1]-X[0])/RR[0])]);GV.append((1/(X[1]-X[0])+1)/RR[0]+1)
for i in range(1,len(rg)-1):
 a,b=X[i]-X[i-1],X[i+1]-X[i];D.append([(i-1,b/(a*(a+b))/RR[i]),(i,abs(b-a)/(a*b)/RR[i]),(i+1,a/(b*(a+b))/RR[i])]);GV.append(5/RR[i]+1)
D.append([(len(rg)-2,1/(X[-1]-X[-2])/RR[-1]),(len(rg)-1,1/(X[-1]-X[-2])/RR[-1])]);GV.append((1/(X[-1]-X[-2])+1)/RR[-1]+1)
GU=[[[sum((coef*S[t][b][j] for j,coef in D[i]),iv.mpf(0)) for i in range(len(rg))] for b in range(4)] for t in range(2)];max_intermediate=0.
def interp(v,U,V,tailU,tailV):
 global max_intermediate
 if v<lr[0]:return U[0],V[0]
 if v>lr[-1]:return tailU,tailV
 i=int(np.clip(np.searchsorted(lr,v,side='right')-1,0,len(rg)-2));offset=iv.mpf(float(v))-X[i];dd=X[i+1]-X[i];assert offset.a>=0 and offset.b<=dd.b;assert .5<=float(v)/lr[i]<=2
 slopeU=(U[i]+U[i+1])/dd;slopeV=(V[i]+V[i+1]+1)/dd+1;max_intermediate=max(max_intermediate,float(np.nextafter(float(slopeU.b),np.inf)));return U[i]+slopeU*offset,V[i]+slopeV*offset+1+V[i]+1

def mult(q,c):return q[0]*abs(c),q[1]*abs(c)+1

def divide(q,c):return q[0]/abs(c),q[1]/abs(c)+1
pathU=np.empty((2,4,15));pathV=np.empty_like(pathU);errors=np.zeros((4,15));test_errors=np.empty_like(pathU);envelopes=np.zeros((2,4,len(rg)))
for t in range(2):
 for b in range(4):
  for k,v in enumerate(S[t][b]):envelopes[t,b,k]=max(0.,float(np.nextafter(float(v.a),-np.inf)))
  for row in range(15):
   R=iv.mpf(float(proj['native_R'][b,row]*1e6));mu,mv=interp(float(proj['evaluation_log'][b,row]),S[t][b],[iv.mpf(0)]*len(rg),S[t][b][-1],iv.mpf(0));sum1U=iv.mpf(0);sum1V=iv.mpf(len(w));sum2U=iv.mpf(0);sum2V=iv.mpf(len(w))
   for k,v in enumerate(proj['query_log'][b,row]):
    fu,fv=interp(float(v),GU[t][b],GV,GU[t][b][-1] if t else iv.mpf(0),GV[-1] if t else iv.mpf(0));q1=(fu,fv)
    for c in (1-iv.mpf(float(th[k])),R,iv.mpf(float(sh[k])),iv.mpf(float(w[k]))):q1=mult(q1,c);max_intermediate=max(max_intermediate,float(np.nextafter(float(q1[0].b),np.inf)))
    q2=mult(divide((fu,fv),iv.mpf(float(ch[k]))),iv.mpf(float(w[k])));sum1U+=q1[0];sum1V+=q1[1];sum2U+=q2[0];sum2V+=q2[1]
   q1=divide((mu+sum1U,mv+sum1V+1),pi*R**2);q2=divide((sum2U,sum2V),2*pi*R);UU=q1[0]+q2[0];VV=q1[1]+q2[1]+1;pathU[t,b,row]=cast(UU)[1];pathV[t,b,row]=cast(VV)[1];err=gamma*UU+eta*W[t][b]*VV*amplify;errors[b,row]+=cast(err)[1];test_errors[t,b,row]=cast(gamma*UU+eta*VV*amplify)[1]
 print('tail complete',t,time.monotonic()-t0,flush=True)
# Account for rounding when the two group error upper bounds were added.
errors=np.nextafter(errors,np.inf);minimum_positive_weight=float(weights[weights>0].min());max_individual_path=cast(iv.mpf(float(max_intermediate))/iv.mpf(minimum_positive_weight))[1];check('path_no_overflow',np.isfinite(max_individual_path) and max_individual_path<np.finfo(float).max/1024 and np.isfinite(max_intermediate) and max_intermediate<np.finfo(float).max/1024)
# Tests use covered full/alternating envelopes and the certified ideal coefficients.
ns={'__file__':str(source),'__name__':'source_forward_readonly'};exec(compile(source.read_text(),str(source),'exec'),ns);LD=np.longdouble;mutation=False;tests=[]
def dotbound(a,v):
 pr=np.asarray(a,LD)*np.asarray(v,LD);sv=np.einsum('i->',pr,optimize=False,dtype=LD);av=np.einsum('i->',abs(pr),optimize=False,dtype=LD);sl=np.nextafter(float(sv),-np.inf);su=np.nextafter(float(sv),np.inf);au=np.nextafter(float(av),np.inf);assert LD(sl)<=sv<=LD(su) and LD(au)>=av;nn=len(v);gu=2*nn*u/(1-2*nn*u);ee=gu*(iv.mpf(float(au))+2*nn*iv.mpf(2)**-1000)/(1-gu)+2*nn*iv.mpf(2)**-1000;return iv.mpf([float(sl),float(su)])+iv.mpf([-1,1])*ee
for t in range(2):
 for b in range(4):
  for stress in (False,True):
   vec=envelopes[t,b].copy()
   if stress:vec[::2]=0
   actual=ns['delta_sigma'](proj['native_R'][b]*1e6,rg,vec,'linear' if t else 'const');assert np.isfinite(actual).all()
   for row in range(15):
    expected=dotbound(proj['binary_coefficients'][t,b,row],vec);extra=iv.mpf(float(proj['row_L1_error'][t,b,row]))*iv.mpf(float(abs(vec).max()));error=iv.mpf(float(test_errors[t,b,row]));box=expected+iv.mpf([-1,1])*(extra+error);ok=bool(box.a<=actual[row] and box.b>=actual[row]);tests.append(ok)
    if not mutation and abs(actual[row])>1e-8:mutation=not bool(box.a<=actual[row]*1.01 and box.b>=actual[row]*1.01)
check('stress_coverage',len(tests)==240);check('stress_tests',all(tests));check('mutation_detected',mutation);check('outward_casts',conversion);check('finite_outputs',np.isfinite(errors).all() and np.isfinite(pathU).all() and np.isfinite(pathV).all())
# Exact inflation of the existing witness; no new score fit.
c=json.loads(files[11].read_text());prior=json.loads(files[10].read_text());aa=list(map(F,c['a']));den=F(c['denominator']);boxes=[]
for i in range(60):
 extra=F(prior['exact_inflation'][i])+F(float(errors.ravel()[i]));lo,hi=map(F,c['native_residual_boxes'][i]);boxes.append((lo-extra,hi+extra))
nl=sum((min(aa[i]*boxes[i][0],aa[i]*boxes[i][1]) for i in range(60)),F(0));nh=sum((max(aa[i]*boxes[i][0],aa[i]*boxes[i][1]) for i in range(60)),F(0));dist=max(nl,-nh,F(0));lower=dist**2/den;law=F(c['law_candidate_upper']);check('inputs_stable',all(sha(ROOT/f)==h for f,h in hashes.items()))
np.savez_compressed(out/'forward_error_evidence.npz',native_errors=errors,path_U=pathU,path_V=pathV,test_errors=test_errors,envelopes=envelopes)
result=dict(checks=checks,N=N,u='2^-50',eta='2^-1022',gamma=str(gamma),max_native_projection_error=float(errors.max()),max_intermediate_absolute_path=max_intermediate,max_individual_absolute_path=max_individual_path,dual_lower_after_error=float(lower),exact_dual_lower=str(lower),law_upper=float(law),conditional_lower_exceeds_law_plus9=lower>law+9,source_tests=len(tests),runtime_seconds=time.monotonic()-t0,input_sha256=hashes,full_model_interval_certified=False,scope='Source-operation-model projection forward error for fixed primitives and covered input masses; mass construction/catalogue stacking/continuum and binary build assumptions remain')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('input_sha256','exact_dual_lower')},indent=2));raise SystemExit(0 if all(checks.values()) else 1)
