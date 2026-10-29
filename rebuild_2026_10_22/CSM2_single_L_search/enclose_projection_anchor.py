import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,contextlib,io,json,hashlib,sys,time
import numpy as np
from mpmath import iv
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(HERE));from projection_operator import operator
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True);iv.dps=50;tstart=time.monotonic();checks={};castok=True

def arr(x):
 x=np.asarray(x,float);assert np.isfinite(x).all();return x

def cast(q):
 global castok
 l=float(np.nextafter(float(q.a),-np.inf));h=float(np.nextafter(float(q.b),np.inf));assert np.isfinite([l,h]).all();castok &= bool(iv.mpf(l)<=q.a and iv.mpf(h)>=q.b);return l,h
check=lambda k,v:checks.update({k:bool(v)})
# Capture the unchanged corrected source namespace, retaining all executed artifacts.
replay=HERE.parent/'CSM1_consistent_core_switch/calibration/calibrate_replay.py';ref=replay.parent/'run_003_audited/results.json';text=replay.read_text();prefix=text[:text.index('RESULT=dict(assertion_tested=')];(out/'executed_helper_prefix.py').write_text(prefix);argv=sys.argv;sys.argv=[str(replay),'--output',str(out),'--reference',str(ref),'--skip-baseline'];ns={'__file__':str(replay),'__name__':'projection_anchor_helpers'}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(prefix,str(replay),'exec'),ns)
sys.argv=argv;capture={};old=ns['NS']['run_copy']
def wrapped(*a,**kw):
 s=old(*a,**kw);capture['source']=s;return s
ns['NS']['run_copy']=wrapped
with contextlib.redirect_stdout(io.StringIO()):raw=ns['task']('x53','on','shpS9_L3.75','corrected')
s=capture['source'];native=np.load(HERE/'native_matrix_001/native_matrices.npz');ev=np.load(HERE/'signed_dot_002_cached/signed_map_evidence.npz');savedA=ev['A'];weights=arr(native['weights']);R=arr(native['R']);grid=arr(native['LMG']);mass=np.load(HERE/'mass_enclosure_001/outward_mass_vectors.npz');mlo=mass['lower'];mhi=mass['upper'];halo_nodes=mass['node_indices'];positive=np.flatnonzero(np.any(weights>0,axis=0));rg=arr(s['RGRID_PC']);tt=arr(s['AQ'].TT);lr=arr(np.log(rg));ch=arr(np.cosh(tt));sh=arr(np.sinh(tt));th=arr(np.tanh(tt));w=np.full(len(tt),tt[1]-tt[0]);w[[0,-1]]*=.5;pi=iv.mpf(float(np.pi));n=len(rg)
# Exact fixed-primitive nonuniform derivative coefficients.
x=[iv.mpf(float(v)) for v in lr];rv=[iv.mpf(float(v)) for v in rg];D=[]
D.append([(0,-1/(x[1]-x[0])/rv[0]),(1,1/(x[1]-x[0])/rv[0])])
for i in range(1,n-1):
 a1=x[i]-x[i-1];b=x[i+1]-x[i];D.append([(i-1,-b/(a1*(a1+b))/rv[i]),(i,(b-a1)/(a1*b)/rv[i]),(i+1,a1/(b*(a1+b))/rv[i])])
D.append([(n-2,-1/(x[-1]-x[-2])/rv[-1]),(n-1,1/(x[-1]-x[-2])/rv[-1])]);kernel=[(iv.mpf(1)-iv.mpf(float(th[k])))*iv.mpf(float(sh[k]))*iv.mpf(float(w[k]))-iv.mpf(float(w[k]))/(2*iv.mpf(float(ch[k]))) for k in range(len(tt))]
Alow=np.empty((2,4,15,n));Ahigh=np.empty_like(Alow);Afloat=np.empty_like(Alow);errors=np.empty((2,4,15));queries=np.empty((4,15,len(tt)));elog=np.empty((4,15));benchmark=[];mutation=False;source_const_same=True
for b in range(4):
 for row in range(15):
  rr=float(R[b,row]*1e6);rrv=iv.mpf(rr);q=arr(np.log(rr*ch));queries[b,row]=q;elog[b,row]=np.log(rr);F=[iv.mpf(0) for _ in range(n)];tail=iv.mpf(0)
  for k,v in enumerate(q):
   kk=kernel[k]/(pi*rrv)
   if v<lr[0]:F[0]+=kk
   elif v>lr[-1]:tail+=kk
   else:
    i=int(np.clip(np.searchsorted(lr,v,side='right')-1,0,n-2));alpha=(iv.mpf(float(v))-x[i])/(x[i+1]-x[i]);F[i]+=kk*(1-alpha);F[i+1]+=kk*alpha
  A=[iv.mpf(0) for _ in range(n)];v=elog[b,row]
  if v<=lr[0]:A[0]=1/(pi*rrv**2)
  elif v>=lr[-1]:A[-1]=1/(pi*rrv**2)
  else:
   i=int(np.searchsorted(lr,v,side='right')-1);alpha=(iv.mpf(float(v))-x[i])/(x[i+1]-x[i]);A[i]=(1-alpha)/(pi*rrv**2);A[i+1]=alpha/(pi*rrv**2)
  for i in range(n):
   for j,vv in D[i]:A[j]+=F[i]*vv
  for ti,tname in enumerate(('const','linear')):
   AA=list(A)
   if ti:
    for j,vv in D[-1]:AA[j]+=tail*vv
   af=arr(operator(np.array([rr]),rg,tt,tname)[0]);Afloat[ti,b,row]=af
   if ti==0:source_const_same &= bool(np.array_equal(af,savedA[b,row]))
   err=iv.mpf(0)
   for j,vv in enumerate(AA):
    Alow[ti,b,row,j],Ahigh[ti,b,row,j]=cast(vv);diff=vv-iv.mpf(float(af[j]));err+=max(abs(diff.a),abs(diff.b))
   errors[ti,b,row]=cast(err)[1]
   for name,vec in [('point',np.ones(n)),('linear',rg),('compact',rg**2/(rg+1e5))]:
    expected=float(s['AQ'].delta_sigma(np.array([rr]),rg,vec,tname)[0]);got=float(np.einsum('i,i->',af,vec,optimize=False));scale=max(abs(expected),1e-300);benchmark.append(abs(got-expected)/scale)
    if b==0 and row==0 and ti==0 and name=='point':mutation=abs(got*1.01-expected)/scale>1e-10
 print('coefficient bin complete',b,time.monotonic()-tstart,flush=True)
check('constant_coefficients_identical',source_const_same);check('coefficient_coverage',Alow.shape==(2,4,15,3601));check('outward_coefficient_casts',castok);check('source_benchmarks',len(benchmark)==360 and np.isfinite(benchmark).all() and max(benchmark)<1e-10);check('mutation_detected',mutation)
# Extract positive-weight node profiles, including fixed law vectors not saved before.
profiles=[];flags=[]
for i in positive:
 v,meta=s['mass_H']('canonical',float(grid[i]),.679,s['H_PRIMARY']);profiles.append(arr(v));flags.append(bool(meta[3]))
profiles=arr(profiles);flags=np.array(flags);check('node_coverage',len(positive)==127 and np.array_equal(positive[flags],halo_nodes));refH=arr(json.loads(ref.read_text())['levels']['3.75']['lens']['result']['canonical']['profiles']['H']);sourceH=arr(raw['result']['canonical']['profiles']['H']);check('source_baseline_reproduction',np.max(abs(refH-sourceH))/np.max(abs(refH))<1e-8)
# Derived dot bounds copied from the completed signed-map arithmetic, on fixed binary coefficients.
LD=np.longdouble;fi=np.finfo(LD);assert fi.nmant>=52 and fi.tiny<LD(2)**-1000;u=iv.mpf(2)**-50;eta=iv.mpf(2)**-1000

def dot(a,v):
 pr=np.asarray(a,LD)*np.asarray(v,LD);assert np.isfinite(pr).all();sv=np.einsum('i->',pr,optimize=False,dtype=LD);ab=np.einsum('i->',abs(pr),optimize=False,dtype=LD);sl=np.nextafter(float(sv),-np.inf);su=np.nextafter(float(sv),np.inf);av=np.nextafter(float(ab),np.inf);assert LD(sl)<=sv<=LD(su) and LD(av)>=ab;nn=len(v);g=2*nn*u/(1-2*nn*u);err=g*(iv.mpf(float(av))+2*nn*eta)/(1-g)+2*nn*eta;return iv.mpf([float(sl),float(su)])+iv.mpf([-1,1])*err
anchor=[iv.mpf(0) for _ in range(60)];halo_lookup={int(v):j for j,v in enumerate(halo_nodes)};numerical_stack=np.zeros((4,15))
for j,i in enumerate(positive):
 ti=0 if flags[j] else 1;lo=mlo[2*halo_lookup[int(i)]] if flags[j] else profiles[j];hi=mhi[2*halo_lookup[int(i)]] if flags[j] else profiles[j];vmax=float(max(abs(lo).max(),abs(hi).max()))
 for b in range(4):
  for k in range(15):
   aa=Afloat[ti,b,k];l=dot(aa,np.where(aa>=0,lo,hi));h=dot(aa,np.where(aa>=0,hi,lo));ee=iv.mpf(float(errors[ti,b,k]))*iv.mpf(vmax);box=iv.mpf([l.a,h.b])+iv.mpf([-1,1])*ee;anchor[15*b+k]+=iv.mpf(float(weights[b,i]))*box;numerical_stack[b,k]+=weights[b,i]*np.einsum('i,i->',aa,profiles[j],optimize=False)
anchor_bounds=arr([cast(v) for v in anchor]);deviation=arr([cast(v-iv.mpf(float(sourceH.ravel()[i])))[1] if v.a>=sourceH.ravel()[i] else max(abs(cast(v-iv.mpf(float(sourceH.ravel()[i])))[0]),abs(cast(v-iv.mpf(float(sourceH.ravel()[i])))[1])) for i,v in enumerate(anchor)]);check('stacked_mass_source_control',np.max(abs(numerical_stack-sourceH))/np.max(abs(sourceH))<1e-8);check('finite_outputs',np.isfinite(Alow).all() and np.isfinite(Ahigh).all() and np.isfinite(errors).all() and np.isfinite(anchor_bounds).all());contained=[bool(v.a<=sourceH.ravel()[i] and v.b>=sourceH.ravel()[i]) for i,v in enumerate(anchor)]
inputs=dict(ns['INPUTS'])
for f in [Path(__file__),HERE/'PROJECTION_ANCHOR_CRITERIA.md',HERE/'projection_operator.py',HERE/'native_matrix_001/native_matrices.npz',HERE/'signed_dot_002_cached/signed_map_evidence.npz',HERE/'mass_enclosure_001/outward_mass_vectors.npz']:inputs[str(f)]=sha(f) if 'sha' in globals() else hashlib.sha256(f.read_bytes()).hexdigest()
check('inputs_stable',all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in inputs.items()))
np.savez_compressed(out/'projection_primitive_enclosures.npz',lower=Alow,upper=Ahigh,binary_coefficients=Afloat,row_L1_error=errors,log_radius=lr,radius=rg,native_R=R,cosh=ch,sinh=sh,tanh=th,weight=w,query_log=queries,evaluation_log=elog,node_indices=positive,node_mass=profiles,node_halo=flags,anchor_bounds=anchor_bounds,anchor_deviation=deviation)
result=dict(checks=checks,coefficient_count=int(Alow.size),source_benchmark_cases=len(benchmark),max_source_benchmark_error=max(benchmark),max_coefficient_row_L1_error=float(errors.max()),source_anchor_coordinates_contained=sum(contained),source_anchor_coordinates=60,max_anchor_deviation=float(deviation.max()),runtime_seconds=time.monotonic()-tstart,input_sha256=inputs,scope='Directed coefficients and baseline boxes for frozen source primitive tables and fixed law vectors; original floating source and continuum coverage remain separate',full_model_interval_certified=False)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'},indent=2));raise SystemExit(0 if all(checks.values()) else 1)
