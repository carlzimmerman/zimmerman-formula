"""Orthogonal dense checks BEFORE new collapse claims."""
import json,pathlib,hashlib
import numpy as np
from scipy.linalg import expm
from angular_fast import Angular
P=pathlib.Path(__file__).resolve().parent
pins={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'angular_fast.py',pathlib.Path(__file__)]}
r=np.geomspace(.03,20,32);w=np.gradient(r);ang=Angular(4,4,r,w);rng=np.random.default_rng(9009)
v=rng.normal(size=(len(r),ang.field.nm))+1j*rng.normal(size=(len(r),ang.field.nm));v/=np.linalg.norm(v)
roundtrip=float(np.max(abs(ang.field.back(ang.field.forward(v))-v)))
pang,c,W=ang.potential(v)
# Dense multipole Green, independent of scaled recurrence.
rho=ang.density.back(abs(ang.field.forward(v))**2/(w*r*r)[:,None,None]);cd=np.empty_like(c)
for j,(l,m) in enumerate(ang.density.lm):
 K=np.minimum(r[:,None],r[None,:])**l/np.maximum(r[:,None],r[None,:])**(l+1)
 cd[:,j]=-4*np.pi/(2*l+1)*K@(w*r*r*rho[:,j])
green=float(np.max(abs(cd-c)))
# Construct P V P by its action on each basis vector, then exact dense exp.
H=np.stack([ang.multiply(np.tile(np.eye(ang.field.nm)[j],(len(r),1)).astype(complex),pang) for j in range(ang.field.nm)],axis=-1)
herm=float(np.max(abs(H-H.swapaxes(-1,-2).conj())))
dt=.07;eta=.13
exact=np.array([expm(-1j*dt*h/eta)@z for h,z in zip(H,v)])
cheb=ang.exp(v,pang,dt,eta);exp_err=float(np.max(abs(cheb-exact)))
norm=float(abs(np.linalg.norm(cheb)**2-np.linalg.norm(v)**2))
# Functional derivative of W and vanishing Jz torque.
z=rng.normal(size=v.shape)+1j*rng.normal(size=v.shape);z/=np.linalg.norm(z);eps=1e-5
fd=(ang.potential(v+eps*z)[2]-ang.potential(v-eps*z)[2])/(2*eps)
exactfd=2*np.real(np.vdot(z,ang.multiply(v,pang)));grad=float(abs(fd-exactfd))
torque=float(abs(2*np.real(np.vdot(v*ang.m,-1j*ang.multiply(v,pang)))))
assert abs(ang.self_energy(v)-W)<1e-12
checks=dict(Parseval_self_energy_error=abs(ang.self_energy(v)-W),roundtrip=roundtrip,direct_Green_max_error=green,Hermiticity=herm,Chebyshev_vs_dense=exp_err,norm_error=norm,W_gradient_absolute_error=grad,Jz_torque=torque)
assert roundtrip<1e-12 and green<1e-12 and herm<1e-12 and exp_err<1e-12 and norm<1e-12 and grad<1e-8 and torque<1e-12,checks
out={'status':'finite independent angular checks passed','seed':9009,'checks':checks,'source_hashes_before':pins,'source_hashes_after':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'angular_fast.py',pathlib.Path(__file__)]}}
assert out['source_hashes_before']==out['source_hashes_after'];(P/'angular_fast_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
