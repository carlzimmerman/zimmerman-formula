import json,pathlib,numpy as np
from scipy.linalg import solve
from solver import Grid,Axis,transport
P=pathlib.Path(__file__).resolve().parent
rng=np.random.default_rng(24012);g=Grid(18,8,1.5);eta=.2;dt=.013
p=[.3*x for x in g.xyz];op=Axis(g,eta,p[0],0,dt)
u=rng.normal(size=g.r.shape)+1j*rng.normal(size=g.r.shape);u/=np.linalg.norm(u);q=abs(u)**2*rng.uniform(size=u.shape)
v,qq,err=op.apply(u,q)
j,k=3,7;H=np.diag(op.diag[:,0,0])+np.diag(op.h[:,j,k],1)+np.diag(op.h[:,j,k].conj(),-1);I=np.eye(g.n)
ref=solve(I+1j*dt*H/(2*eta),(I-1j*dt*H/(2*eta))@u[:,j,k])
_,comp,_=op.apply(u,abs(u)**2-q)
# A deliberate through-flow exceeds the old donor's resident mass.
m=np.array([1.,.1,.1]);F=np.array([.8,.7]);tag=np.array([.5,.02,.01]);tt=transport(m,tag,F);mm=m.copy();mm[:-1]-=F;mm[1:]+=F
# Poisson is tested against a directional derivative of its own quadratic energy.
m=abs(u)**2;phi=g.poisson(m);h=rng.normal(size=m.shape);h/=np.linalg.norm(h);eps=1e-6
W=lambda a:.5*np.sum(a*g.poisson(a))
fd=(W(m+eps*h)-W(m-eps*h))/(2*eps)
chirps=[]
for n in (64,128,256):
 z=Grid(n,8,1.5);e=.0046390997853;kap=.3;T=.1;step=.0005
 x=z.x;w=z.w;u1=np.exp(-x*x/2)*np.sqrt(w);p1=-kap*x
 class One:pass
 a=One();a.n=n;a.d=z.d;a.o=z.o;a.w=w
 o=Axis(a,e,p1,0,step);q1=abs(u1)**2
 for it in range(round(T/step)):
  u1=u1*np.exp(-1j*step*p1*p1/(4*e));u1,q1,_=o.apply(u1,q1);u1*=np.exp(-1j*step*p1*p1/(4*e))
 aa=1+1j*kap/e;exact=(1+1j*e*aa*T)**(-.5)*np.exp(-aa*x*x/(2*(1+1j*e*aa*T)))
 physical=u1/np.sqrt(w)*np.exp(-1j*kap*x*x/(2*e))
 chirps.append(dict(n=n,relative_L2=float(np.sqrt(np.sum(w*abs(physical-exact)**2)/np.sum(w*abs(exact)**2)))))
r=dict(seed=24012,CN_dense_error=float(max(abs(v[:,j,k]-ref))),bond_identity=err,mass_error=float(abs(np.sum(abs(v)**2)-1)),tag_min=float(qq.min()),tag_excess=float(np.max(qq-abs(v)**2)),tag_mass_error=float(abs(qq.sum()-q.sum())),complement_error=float(np.max(abs(comp+qq-abs(v)**2))),through_flow=dict(m=mm.tolist(),q=tt.tolist()),poisson_derivative_error=float(abs(fd-np.sum(h*phi))),doubled_source_potential_error=float(np.max(abs(g.poisson(2*m)-2*phi))),doubled_source_energy_error=float(abs(W(2*m)-4*W(m))),chirp=chirps)
assert r['CN_dense_error']<1e-12 and err<1e-12 and r['tag_excess']<1e-12 and r['tag_min']>-1e-12 and r['complement_error']<1e-12
assert r['poisson_derivative_error']<1e-9
assert all(chirps[i+1]['relative_L2']<chirps[i]['relative_L2'] for i in range(2))
(P/'bench.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
