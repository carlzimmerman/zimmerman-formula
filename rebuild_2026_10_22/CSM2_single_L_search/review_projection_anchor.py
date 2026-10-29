"""Exact frozen-primitive quadrature review on12 predeclared profile/row cases.
Rows(bin0,row0) and(bin3,row14), both tails, point/linear/compact vectors.
Main computation encloses all432120coefficients; this is a selected exact review.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
import numpy as np
sys.set_int_max_str_digits(100000)
p=Path(__file__).resolve().parent;r=p.parents[1];run=p/'projection_anchor_001';files=[Path(__file__),run/'results.json',run/'projection_primitive_enclosures.npz'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};d=json.loads(files[1].read_text());z=np.load(files[2]);arrays={k:z[k] for k in z.files};lr=list(map(lambda x:F(float(x)),arrays['log_radius']));rg=arrays['radius'];rp=list(map(lambda x:F(float(x)),rg));pi=F(float(np.pi));ch,sh,th,w=[[F(float(v)) for v in arrays[name]] for name in ('cosh','sinh','tanh','weight')];checks={};cases=0
for name,vec in [('point',np.ones(len(rg))),('linear',rg),('compact',rg**2/(rg+1e5))]:
 m=list(map(lambda x:F(float(x)),vec));g=[(m[1]-m[0])/(lr[1]-lr[0])/rp[0]]
 for i in range(1,len(m)-1):
  a,b=lr[i]-lr[i-1],lr[i+1]-lr[i];g.append((-b/(a*(a+b))*m[i-1]+(b-a)/(a*b)*m[i]+a/(b*(a+b))*m[i+1])/rp[i])
 g.append((m[-1]-m[-2])/(lr[-1]-lr[-2])/rp[-1])
 def interp(v,values,tail):
  if v<lr[0]:return values[0]
  if v>lr[-1]:return tail
  i=int(np.clip(np.searchsorted(arrays['log_radius'],float(v),side='right')-1,0,len(lr)-2));a=(v-lr[i])/(lr[i+1]-lr[i]);return values[i]+a*(values[i+1]-values[i])
 for b,row in ((0,0),(3,14)):
  R=F(float(arrays['native_R'][b,row]*1e6));qr=list(map(lambda v:F(float(v)),arrays['query_log'][b,row]));er=F(float(arrays['evaluation_log'][b,row]))
  for ti in (0,1):
   ff=[interp(v,g,g[-1] if ti else F(0)) for v in qr];mc=interp(er,m,m[-1])+sum((ff[k]*(1-th[k])*R*sh[k]*w[k] for k in range(len(w))),F(0));sig=sum((ff[k]/ch[k]*w[k] for k in range(len(w))),F(0))/(2*pi*R);exact=mc/(pi*R*R)-sig;lo=sum((F(float(a))*v for a,v in zip(arrays['lower'][ti,b,row],m)),F(0));hi=sum((F(float(a))*v for a,v in zip(arrays['upper'][ti,b,row],m)),F(0));checks[f'{name}|{b}|{row}|{ti}']=lo<=exact<=hi;cases+=1
checks['coverage']=cases==12;checks['finite_saved_arrays']=all(np.isfinite(v).all() for v in arrays.values());checks['original_controls']=all(d['checks'].values());checks['inputs_stable']=all(sha(r/f)==h for f,h in hashes.items());result=dict(checks=checks,cases=cases,input_sha256=hashes,scope='Exact-rational direct quadrature reconstruction of selected frozen-primitive projections; not original float evaluation or real-L certification')
(p/'projection_anchor_review.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(checks),'allpass',all(checks.values()));assert all(checks.values())
