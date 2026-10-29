"""Exact recomposition and independent interval-grouped catalogue weights."""
from pathlib import Path
from fractions import Fraction as F
from bisect import bisect_right
import hashlib,json,sys
import numpy as np
sys.set_int_max_str_digits(100000)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'catalogue_001';files=[Path(__file__),run/'results.json',p/'native_matrix_001/native_matrices.npz',p/'projection_anchor_001/projection_primitive_enclosures.npz',p/'mass_enclosure_001/outward_mass_vectors.npz',p/'source_forward_review.json',p/'projection_dual_inflation.json',p/'exact_dual_001/certificate.json',r/'real_research/data/lensing_rar/lr_lenses.npz',r/'real_research/data/lensing_rar/cfg110_perlens.npz',p.parent/'X53_outer_lensing_law_vs_halos/x53_outer_lensing.py'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};d=json.loads(files[1].read_text());load=lambda f:dict(np.load(f));nat=load(files[2]);proj=load(files[3]);mass=load(files[4]);src=json.loads(files[5].read_text());prior=json.loads(files[6].read_text());c=json.loads(files[7].read_text());ln=load(files[8]);ww=load(files[9])['WW'].sum(axis=1);bins=np.digitize(ln['logM'],[8.5,10.3,10.6,10.8,11.0001])-1;z=ln['z'];zz=np.linspace(0,1,4001)
def distance(om):
 ez=np.sqrt(om*(1+zz)**3+1-om);y=np.r_[0,np.cumsum((1/ez[1:]+1/ez[:-1])*np.diff(zz)*.5)];return np.interp(z,zz,y)
x=ln['logM']+2*np.log10(.70/.679)+2*np.log10(distance(.3085)/distance(.3));grid=list(map(lambda v:F(float(v)),nat['LMG']));checks={};errors=[];u=F(1,2**50);eta=F(1,2**1022);maxdis=0.;counts=[]
for b in range(4):
 select=bins==b;W=sum((F(float(v)) for v in ww[select]),F(0));S=[F(0) for _ in grid];SW=[F(0) for _ in grid];SX=[F(0) for _ in grid];n=0
 for xx,w in zip(x[select],ww[select]):
  xx,w=F(float(xx)),F(float(w));n+=1
  if xx<=grid[0]:S[0]+=w
  elif xx>=grid[-1]:S[-1]+=w
  else:
   i=bisect_right(grid,xx)-1;SW[i]+=w;SX[i]+=w*xx
 for j in range(len(grid)-1):
  right=(SX[j]-grid[j]*SW[j])/(grid[j+1]-grid[j]);S[j]+=SW[j]-right;S[j+1]+=right
 ideal=[v/W for v in S];checks[f'grouped_exact_weights_{b}']=ideal==list(map(F,d['ideal_weights'][b]));disc=sum((abs(e-F(float(a))) for e,a in zip(ideal,nat['weights'][b])),F(0));checks[f'L1_{b}']=disc==F(d['records'][b]['exact_weight_L1_error']);maxdis=max(maxdis,float(disc));N=2*n+32;gamma=N*u/(1-N*u);step=min(np.diff(grid));minw=min(F(float(v)) for v in nat['weights'][b] if v>0);counts.append(n)
 lookup={int(node):j for j,node in enumerate(mass['node_indices'])};profiles=np.array([mass['upper'][2*lookup[int(node)]+1] if proj['node_halo'][j] else proj['node_mass'][j] for j,node in enumerate(proj['node_indices'])]);active=nat['weights'][b,proj['node_indices']]>0;vmax=profiles[active].max(axis=0);vf=list(map(lambda v:F(float(v)),vmax))
 for k in range(15):
  B=F(d['table_bounds'][b][k]);exact_projection=max(sum((max(abs(F(float(lo))),abs(F(float(hi))))*v for lo,hi,v in zip(proj['lower'][tail,b,k],proj['upper'][tail,b,k],vf)),F(0)) for tail in range(2));assert B>=exact_projection+F(src['exact_review_error_bounds'][b*15+k])/minw
  e=B*disc+3*B*gamma/(1-gamma)+eta*(2*N+32)*(1+B)*(1+W+1/W)**2*(1+1/step)/(1-gamma);errors.append(e);assert e==F(d['exact_stack_error'][b*15+k])
checks['all_60_exact_majorants']=True;checks['all_60_exact_error_budgets']=True;checks['181431_lenses']=sum(counts)==181431;checks['original_controls']=all(d['checks'].values());aa=list(map(F,c['a']));bl=[];bh=[]
for i in range(60):
 lo,hi=map(F,c['native_residual_boxes'][i]);extra=F(prior['exact_inflation'][i])+F(src['exact_review_error_bounds'][i])+errors[i];bl.append(lo-extra);bh.append(hi+extra)
numlo=sum((min(a*l,a*h) for a,l,h in zip(aa,bl,bh)),F(0));numhi=sum((max(a*l,a*h) for a,l,h in zip(aa,bl,bh)),F(0));lower=max(numlo,-numhi,F(0))**2/F(c['denominator']);checks['unchanged_dual']=lower==F(d['exact_dual_lower']);checks['conditional_margin']=lower>F(c['law_candidate_upper'])+9;checks['source_original_stack']=all(s in files[-1].read_text() for s in ['np.interp(lMs_nat, LMG, tab[:, i])','out[b] = vals @ w / w.sum()']);checks['input_hashes']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,exact_majorants_checked=60,lenses=sum(counts),max_weight_L1_discrepancy=maxdis,review_dual_lower=float(lower),input_sha256=hashes,scope='Self/adversarial exact regrouping and recomposition; reviewed implementation/covered-domain premises remain, no full-model real-L certificate');(p/'catalogue_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),all(checks.values()),'lower',float(lower),'L1max',maxdis);assert all(checks.values())
