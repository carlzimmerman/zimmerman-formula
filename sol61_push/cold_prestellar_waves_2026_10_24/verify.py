"""Orthogonal finite-Hamiltonian and static-well no-capture checks."""
import json,math,hashlib,argparse
from pathlib import Path
import numpy as np
from scipy.special import sph_harm
from scipy.linalg import eigh_tridiagonal
from scipy.linalg.lapack import zgttrf,zgttrs
from numpy.polynomial.legendre import leggauss
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--tag',default='sextans_hybrid');args=parser.parse_args()
run=json.loads((HERE/'runs'/f'{args.tag}.json').read_text());f=np.load(HERE/'runs'/f'{args.tag}_fields.npz')
r=f['r'];w=f['w'];v=f['final'];lm=f['lm'];L=run['parameters']['lmax'];eta=run['physical']['eta_code'];nr=len(r)
hl=np.diff(np.r_[0.,r]);hr=np.diff(np.r_[r,run['parameters']['rmax']])
td=.5*eta**2*(1/hl+1/hr)/w;to=-.5*eta**2/(hr[:-1]*np.sqrt(w[:-1]*w[1:]))
kin1=kin2=0.
for j,(l,m) in enumerate(lm):
    x=v[:,j];u=x/np.sqrt(w)
    kin1+=float(np.sum((td+.5*eta**2*l*(l+1)/r**2)*abs(x)**2)+2*np.real(np.sum(to*x[:-1].conj()*x[1:])))
    kinetic_rad=.5*eta**2*np.sum(abs(np.diff(np.r_[0.,u,0.]))**2/np.r_[hl[0],hr])
    kinetic_ang=.5*eta**2*l*(l+1)*np.sum(abs(x)**2/r**2)
    kin2+=float(kinetic_rad+kinetic_ang)
assert abs(kin1/kin2-1)<1e-9

ct,wt=leggauss(2*L+2);ph=np.arange(4*L+2)*2*math.pi/(4*L+2)
theta=np.repeat(np.arccos(ct),len(ph));phi=np.tile(ph,len(ct));wa=np.repeat(wt,len(ph))*2*math.pi/len(ph)
Y=np.array([sph_harm(int(m),int(l),phi,theta) for l,m in lm]).T
lrho=[(l,m) for l in range(2*L+1) for m in range(-l,l+1)]
YY=np.array([sph_harm(m,l,phi,theta) for l,m in lrho]).T
def W_and_V(z):
    ang=z@Y.T;rho=abs(ang)**2/(w*r*r)[:,None];cr=rho@(wa[:,None]*YY.conj())
    cp=np.empty_like(cr)
    # Direct symmetric Green matrices, independent of production prefix sums.
    for j,(l,m) in enumerate(lrho):
        green=np.minimum(r[:,None],r[None,:])**l/np.maximum(r[:,None],r[None,:])**(l+1)
        cp[:,j]=-4*math.pi/(2*l+1)*(green@(w*r*r*cr[:,j]))
    pang=(cp@YY.T).real
    W=.5*float(np.sum(abs(ang)**2*pang*wa))
    V=np.einsum('ai,ra,aj,a->rij',Y.conj(),pang,Y,wa,optimize=True)
    return W,V
W,V=W_and_V(v)
assert abs(W/run['history'][-1]['Wself']-1)<1e-10
rng=np.random.default_rng(7007);delta=rng.normal(size=v.shape)+1j*rng.normal(size=v.shape);delta/=np.linalg.norm(delta)
eps=1e-6;Wp,_=W_and_V(v+eps*delta);Wm,_=W_and_V(v-eps*delta)
fd=(Wp-Wm)/(2*eps);analytic=2*np.real(np.sum(delta.conj()*np.einsum('rij,rj->ri',V,v)))
assert abs(fd-analytic)<1e-8
ms=lm[:,1];Vz=np.einsum('rij,rj->ri',V,v)
torque=float(2*np.imag(np.sum((ms[None,:]*v).conj()*Vz)))
assert abs(torque)<1e-10
plus=np.zeros((len(lm),len(lm)),complex);modes=[tuple(z) for z in lm]
for j,(ll,mm) in enumerate(modes):
    if mm<ll:plus[modes.index((ll,mm+1)),j]=math.sqrt(ll*(ll+1)-mm*(mm+1))
operators=[(plus+plus.conj().T)/2,(plus-plus.conj().T)/(2j),np.diag(ms)]
torques=[float(2*np.imag(np.sum((v@op.T).conj()*Vz))) for op in operators]
assert max(abs(z) for z in torques)<1e-10

# Linear, stationary, CLOSED well. Explicitly remove pre-existing bound overlap.
pg=-1/5.364/np.sqrt(r*r+25)
evals,U=eigh_tridiagonal(td+pg,to)
bound=evals<0
x=f['initial'][:,0].copy();x-=U[:,bound]@(U[:,bound].T@x);x/=np.linalg.norm(x)
initial_bound=float(np.sum(abs(U[:,bound].T@x)**2));initial_norm=float(np.sum(abs(x)**2))
dt=.04;fac=1j*dt/(2*eta);fact=zgttrf(fac*to,1+fac*(td+pg),fac*to)
for it in range(1000):
    Hx=(td+pg)*x;Hx[1:]+=to*x[:-1];Hx[:-1]+=to*x[1:]
    x,info=zgttrs(*fact[:-1],np.asfortranarray((x-fac*Hx)[:,None]));assert info==0;x=x[:,0]
final_bound=float(np.sum(abs(U[:,bound].T@x)**2));final_norm=float(np.sum(abs(x)**2))
assert initial_bound<1e-20 and final_bound<1e-18 and abs(final_norm-initial_norm)<1e-10
out=dict(status='finite solver self-checks passed; full angular/radial convergence separate',
    kinetic_gradient_identity_relative_error=abs(kin1/kin2-1),direct_Green_relative_error=abs(W/run['history'][-1]['Wself']-1),
    self_energy_gradient_absolute_error=abs(fd-analytic),instantaneous_self_torque=torque,instantaneous_self_torque_vector=torques,
    static_linear_null=dict(bound_states=int(np.sum(bound)),initial_bound_mass=initial_bound,final_bound_mass=final_bound,norm_drift=final_norm-initial_norm),
    checked_field_sha256=hashlib.sha256((HERE/'runs'/f'{args.tag}_fields.npz').read_bytes()).hexdigest())
target=HERE/('verification.json' if args.tag=='sextans_hybrid' else f'verification_{args.tag}.json')
target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
