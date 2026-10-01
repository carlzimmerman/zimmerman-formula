import numpy as np,json,os
from pathlib import Path
from exact_moments import kick_moments
mut=os.environ.get('MUTATE')=='1';checks={};rows=[]
# Integrate explicit Cartesian kicks in a basis aligned with v, independently of tensor formulas.
for name,vr,vt,vk,c in [('oblique',3.,4.,6.,-.35),('radial',5.,0.,2.,.2),('tangent',0.,5.,2.,.75),('all',3.,4.,6.,2.),('none',3.,4.,6.,-2.)]:
 speed=np.hypot(vr,vt);phi=-(speed**2+vk**2+2*vk*speed*c)/2
 fe,rr,tt=map(float,kick_moments(vr,vt,phi,vk,mut));cc=np.clip(c,-1,1);fb=(cc+1)/2
 if fb>0:
  x,w=np.polynomial.legendre.leggauss(32);mu=-1+(x+1)*(cc+1)/2
  az=np.arange(64)*2*np.pi/64;e=np.array([vr,vt,0])/speed;b=np.array([-vt,vr,0])/speed;d=np.array([0,0,1.])
  n=mu[:,None,None]*e+np.sqrt(1-mu**2)[:,None,None]*(np.cos(az)[None,:,None]*b+np.sin(az)[None,:,None]*d)
  vel=np.array([vr,vt,0])+vk*n
  qr=np.sum(w*np.mean(vel[:,:,0]**2,axis=1))/2;qt=np.sum(w*np.mean(vel[:,:,1]**2+vel[:,:,2]**2,axis=1))/2
 else:qr=qt=0.
 checks[name+'/fraction']=abs(fe-(1-fb))<1e-14
 checks[name+'/moments']=max(abs(rr-qr),abs(tt-qt))<1e-11
 rows.append(dict(name=name,fe=fe,radial=rr,tangential=tt,quadrature=[qr,qt]))
for name,args,expected in [('rest_bound',(0,0,-20,6),(0,12,24)),('rest_none',(0,0,-10,6),(1,0,0)),('zero_kick',(3,4,-20,0),(0,9,16)),('rest_equality',(0,0,-18,6),(0,12,24))]:
 out=tuple(map(float,kick_moments(*args,mutate=mut)));checks[name]=np.max(np.abs(np.array(out)-expected))<1e-12
out=dict(mutation=mut,checks={k:bool(v) for k,v in checks.items()},rows=rows);Path(__file__).with_name('control_mutation.json' if mut else 'control_main.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
