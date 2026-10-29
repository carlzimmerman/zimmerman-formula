from pathlib import Path
from fractions import Fraction as F
import hashlib,json,resource,signal,sys,time
import numpy as np
import mpmath as mp
resource.setrlimit(resource.RLIMIT_CPU,(120,120));signal.alarm(150);sys.set_int_max_str_digits(100000)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'comparator_001';paths=[Path(__file__),run/'results.json',run/'analytic_comparator.npz',p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'catalogue_001/results.json',p/'native_matrix_001/native_matrices.npz',p/'exact_dual_001/certificate.json',p.parent/'CSM1_consistent_core_switch/calibration/run_003_audited/results.json'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in paths};read=lambda i:json.loads(paths[i].read_text());load=lambda i:dict(np.load(paths[i]));d=read(1);ev=load(2);proj=load(3);cat=read(4);nat=load(5);cert=read(6);prof=read(7)['levels']['3.75']['lens']['result']['canonical']['profiles'];checks={};t0=time.monotonic();nodes=ev['node_indices'];lookup={int(v):j for j,v in enumerate(nodes)};weights=[[F(v) for v in row] for row in cat['ideal_weights']];aggregate_tests=0
for b in range(4):
 for k in [0,720,1440,2160,2880,3600]:
  lo=sum((weights[b][int(node)]*F(float(ev['mass_lower'][j,k])) for j,node in enumerate(nodes)),F(0));hi=sum((weights[b][int(node)]*F(float(ev['mass_upper'][j,k])) for j,node in enumerate(nodes)),F(0));assert F(float(ev['aggregate_lower'][b,k]))<=lo<=hi<=F(float(ev['aggregate_upper'][b,k]));aggregate_tests+=1
checks['24_exact_aggregates']=aggregate_tests==24;dot_tests=0
for b in range(4):
 al=list(map(lambda v:F(float(v)),ev['aggregate_lower'][b]));ah=list(map(lambda v:F(float(v)),ev['aggregate_upper'][b]))
 for row in range(15):
  lo=F(0);hi=F(0)
  for k in range(3601):
   a,beta=F(float(proj['lower'][1,b,row,k])),F(float(proj['upper'][1,b,row,k]));lo+=a*(al[k] if a>=0 else ah[k]);hi+=beta*(ah[k] if beta>=0 else al[k])
  assert F(float(ev['native_bounds'][b*15+row,0]))<=lo<=hi<=F(float(ev['native_bounds'][b*15+row,1]));dot_tests+=1
checks['60_exact_signed_dots']=dot_tests==60;mp.mp.dps=90;M=lambda v:mp.mpf(float(v));a0=M(9.3603e-11)*M(3.0857e16)/M(1e6);law_tests=0
for j in np.linspace(0,126,13,dtype=int):
 lm=M(nat['LMG'][nodes[j]]);ms=mp.power(10,lm);mc=mp.power(10,lm+M(-.69)*(lm-2*mp.log10(M(.70)/M(.679)))+M(6.63))
 for k in [0,900,1800,2700,3600]:
  rad=M(ev['radius_pc'][k]);mb=ms+mc+ms/2*min(1,(rad/M(1e5))**3);v=mb/2+mp.sqrt(mb*mb/4+mb*a0*rad*rad/M(4.30091e-3));assert M(ev['mass_lower'][j,k])<=v<=M(ev['mass_upper'][j,k]);law_tests+=1
checks['65_90digit_law_values']=law_tests==65;L=[[F(v) for v in row] for row in cert['L']];D=list(map(F,cert['D']));bb=list(map(F,cert['law_b']));T=[[F(float(v)) for v in row] for row in nat['T']];Y=list(map(lambda v:F(float(v)),np.array(prof['data']).ravel()));center=[];radius=[]
for i in range(60):
 base=Y[i]-sum((T[i][j]*bb[j] for j in range(4)),F(0));lo=base-F(float(ev['native_bounds'][i,1]));hi=base-F(float(ev['native_bounds'][i,0]));assert [lo,hi]==list(map(F,d['exact_residual_boxes'][i]));center.append((lo+hi)/2);radius.append((hi-lo)/2)
zc=[];zr=[]
for i in range(60):
 zc.append(center[i]-sum((L[i][j]*zc[j] for j in range(i)),F(0)));zr.append(radius[i]+sum((abs(L[i][j])*zr[j] for j in range(i)),F(0)));assert [zc[i]-zr[i],zc[i]+zr[i]]==list(map(F,d['exact_triangular_boxes'][i]))
upper=sum(((abs(zc[i])+zr[i])**2/D[i] for i in range(60)),F(0));checks['exact_center_radius_score']=upper==F(d['exact_candidate_score_upper']);checks['candidate_feasible']=all(v>=0 for v in bb);checks['common_scope_margin']=F(d['exact_hybrid_lower'])>upper+9;checks['finite_outputs']=all(np.isfinite(ev[k]).all() for k in ev);checks['original_controls']=all(d['checks'].values());checks['input_hashes']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,exact_signed_dot_tests=dot_tests,exact_aggregate_tests=aggregate_tests,independent_law_values=law_tests,reviewed_candidate_upper=float(upper),exact_reviewed_upper=str(upper),runtime_seconds=time.monotonic()-t0,input_sha256=hashes,scope='Exact all-row projection/LDL interval upper within fixed-primitive analytic numerical-grid interpretation; original floating evaluator/globalL not certified');(p/'analytic_comparator_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'upper',float(upper));assert all(checks.values())
