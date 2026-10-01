#!/usr/bin/env python3
"""Bounded independent audit: fixed-region P2 stationarity, tides, kinetic completion.
MUTATE=1 deletes isotropic tide trace in predicted first-order monopole; named check must fail.
No fit and no claim about a covariant moving-region completion.
"""
import os,json,hashlib,sys
from pathlib import Path
import numpy as np
from scipy.optimize import root
from numpy.polynomial.legendre import leggauss
MUT=os.environ.get('MUTATE')=='1'
OUT=Path(__file__).resolve().parent
G=6.6743e-11; MS=1.98892e30; MPC=3.0857e22
A0={'canonical':9.3603e-11,'alt':1.1312e-10}
checks={}; numbers={}
def check(n,ok,value): checks[n]={'ok':bool(ok),'value':value}
def flux(v):
 r=np.linalg.norm(v,axis=-1); nu=np.sqrt(1+1/np.maximum(r,1e-40)); return (nu-1)[...,None]*v
# A dimensionless three-point unequal-field region, equal volume weights.
g=np.array([[.01,.02,0],[.3,-.03,.01],[-.04,.01,-.02]])
def solve(g): return root(lambda a:flux(g-a).sum(0),g.mean(0),tol=1e-12).x
A=solve(g); shift=np.array([.23,-.71,.55]); Ap=solve(g+shift)
check('uniform_shift_cancels',np.max(abs(Ap-A-shift))<1e-10,float(np.max(abs(Ap-A-shift))))
check('stationarity_residual',np.max(abs(flux(g-A).sum(0)))<1e-10,float(np.max(abs(flux(g-A).sum(0)))))
check('weighted_mean_not_arithmetic_mean',np.linalg.norm(A-g.mean(0))>1e-3,float(np.linalg.norm(A-g.mean(0))))
numbers['stationary_A']=A.tolist(); numbers['arithmetic_A']=g.mean(0).tolist()
# Orthogonal test of strict convexity: radial eigenvalue exact expression.
y=np.geomspace(1e-9,1e5,1001); nu=np.sqrt(1+1/y); eig=nu-1-1/(2*y*nu); exact=(nu-1)**2/(2*nu)
check('P2_radial_positive',np.all(eig>0) and np.max(abs(eig-exact)/(1+abs(exact)))<1e-12,{'minimum':float(eig.min())})
# Sphere quadrature, symmetry resolves trace/shear separately.
z,w=leggauss(96); phi=np.arange(192)*2*np.pi/192
n=np.stack(np.broadcast_arrays(np.sqrt(1-z[:,None]**2)*np.cos(phi),np.sqrt(1-z[:,None]**2)*np.sin(phi),z[:,None]+0*phi),-1)
weights=w[:,None]/(2*len(phi))
for foot,a0 in A0.items():
 r=.3*MPC; y0=G*1e11*MS/r**2/a0; u=np.sqrt(1+1/y0); radial=(u-1)**2/(2*u)
 base=np.sum(weights*np.sum(flux(y0*n)*n,axis=-1))
 for typ,T in [('isotropic',np.eye(3)),('shear',np.diag([1.,-1.,0.]))]:
  eps=y0*1e-4; fn=lambda e:float(np.sum(weights*np.sum(flux(y0*n+e*np.einsum('ij,...j->...i',T,n))*n,axis=-1)))
  derivative=(fn(eps)-fn(-eps))/(2*eps); predicted=radial*np.trace(T)/3
  if MUT and typ=='isotropic': predicted=0.
  check(f'{foot}_{typ}_first_order',abs(derivative-predicted)<1e-7,{'numerical':derivative,'predicted':predicted})
  numbers[f'{foot}/{typ}']={'y0':y0,'base_phantom_radial':float(base),'central_derivative':derivative,'analytic_derivative':radial*np.trace(T)/3,'relative_effect_at_tide_1e-4':(fn(1e-4)/base-1)}
 # Isotropic environment density delta=1 at z=.25, matching source approximation.
 h=.6736; Om=(.02237+.1200)/h**2; H0=100*h*1e3/MPC
 t=Om*H0**2/(2*(1/1.25)**3); e=t*r/a0
 numbers[f'{foot}/environment']={'tidal_at_0.3Mpc_a0':e,'r_trace_balance_Mpc':(G*1e11*MS/t)**(1/3)/MPC,'r_tide_below_10percent_Mpc':(.1*G*1e11*MS/t)**(1/3)/MPC,'monopole_linear_relative':radial*e/base}
# Dimensionless kinetic completion on periodic finite volume: P=I-mean.
# For positive region-fixed C >= max negative curvature, v^T [P diag(Lpp) P + C P] v >=0.
rng=np.random.default_rng(361); N=48; P=np.eye(N)-np.ones((N,N))/N
Lpp=rng.uniform(-9.85,9.85,N); C=max(0.,-Lpp.min()); H=P@np.diag(Lpp)@P+C*P
ev=np.linalg.eigvalsh(H)
check('fixed_region_completion_hessian',ev.min()>-1e-12,{'min_eigenvalue':float(ev.min()),'C':C})
# Shear completion preserves homogeneous expansion: sigma= sym(grad u)-I div(u)/3.
curvature=9.85; Cshear=1.5*curvature; kval=np.geomspace(1e-8,1e8,401)
mL=1+(-curvature+2*Cshear/3)*kval**2; mT=1+Cshear*kval**2/2
check('shear_completion_fourier_positive',min(mL.min(),mT.min())>=1,{'minimum_longitudinal':float(mL.min()),'minimum_transverse':float(mT.min()),'C':Cshear})
sigma_hubble=np.eye(3)-np.eye(3)*np.trace(np.eye(3))/3
check('shear_compensator_zero_on_Hubble',np.max(abs(sigma_hubble))==0,0.)
numbers['shear_completion']={'negative_curvature_bound':curvature,'C_shear':Cshear,'kinetic_eigenvalues':'mL=rho+(Lpp+2C/3)k^2; mT=rho+Ck^2/2','scope':'constant coefficients on periodic or decaying fields, full metric/fluid action not audited'}
# Scale-free scalar shear projection s=Delta^-1 d_i d_j sigma_ij: s=(2/3)theta for nonzero longitudinal k.
Cscalar=2.25*curvature; mScalar=1+(-curvature+4*Cscalar/9)*kval**2
check('scalar_projection_kinetic_positive',mScalar.min()>=1,float(mScalar.min()))
hTT=np.diag([1.,-1.,0.]); direction=np.array([0.,0.,1.]); projected_TT=float(direction@hTT@direction)
check('scalar_projection_TT_zero',projected_TT==0.,projected_TT)
numbers['scalar_projection']={'C':Cscalar,'mL':'rho+(Lpp+4C/9)k^2','tensor_addition':0.,'scope':'nonzero flat Fourier modes, inverse spatial Laplacian and boundary prescription required'}
result={'mutate':MUT,'checks':checks,'numbers':numbers,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'verdict':'pass' if all(c['ok'] for c in checks.values()) else 'failed','scope':'fixed region, prescribed gate, finite quadrature; local Hessian sufficient condition only'}
path=OUT/('frame_tide_results_MUTATE.json' if MUT else 'frame_tide_results.json'); path.write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2)); sys.exit(0 if result['verdict']=='pass' else 1)
