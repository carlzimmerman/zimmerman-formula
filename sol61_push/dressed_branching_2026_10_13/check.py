#!/usr/bin/env python3
"""Tree-level homogeneous Beliaev channel, canonical NR two-field Hamiltonian."""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from itertools import permutations

def modes(q,eps,x):
 u=(1+x-math.sqrt((1-x)**2+4*eps*x))/2
 A=q*q/2+x-u/2; C=math.sqrt(eps*x); D=q*q/4+1-u
 L=np.array([[A,C,u/2,0],[C,D,0,0],[-u/2,0,-A,-C],[0,0,-C,-D]])
 vals,vs=np.linalg.eig(L)
 assert max(abs(vals.imag))<1e-7
 out=[]
 for j in np.argsort(vals.real):
  if vals[j].real>1e-8:
   v=vs[:,j].real; norm=v[:2]@v[:2]-v[2:]@v[2:]
   assert norm>0
   v/=math.sqrt(norm)
   assert np.linalg.norm(L@v-vals[j].real*v)<1e-8
   out.append((float(vals[j].real),v))
 return out

def cubic(initial,final,eps,x):
 # Each row holds coefficients of initial annihilation z, final creations y,w.
 ua,ub,va,vb=initial; U,V,W,Z=final
 a=np.array([ua,W,W]); ad=np.array([va,U,U])
 b=np.array([ub,Z,Z]); bd=np.array([vb,V,V])
 def coeff(p,q,r): return sum(p[i]*q[j]*r[k] for i,j,k in permutations(range(3)))
 c3=.5*math.sqrt(eps*x); kap=x/4
 return c3*(coeff(bd,a,a)+coeff(b,ad,ad))+2*kap*(coeff(ad,a,a)+coeff(ad,ad,a))

def row(eps,x):
 omega,initial=modes(0,eps,x)[-1]
 q=brentq(lambda q:2*modes(q,eps,x)[0][0]-omega,1e-4,4,xtol=1e-13)
 w,final=modes(q,eps,x)[0]
 # Hellmann-Feynman in the indefinite Bogoliubov metric.
 metric=np.diag([1,1,-1,-1]); dL=np.diag([q,q/2,-q,-q/2])
 velocity=float(final@metric@dL@final)
 h=1e-5
 fd=(modes(q+h,eps,x)[0][0]-modes(q-h,eps,x)[0][0])/(2*h)
 assert abs(fd-velocity)<1e-7
 amp=cubic(initial,final,eps,x)
 ratio=q*q*amp*amp/(eps*x*velocity)
 # Photon operator and same correction used in prior run.
 u=(1+x-math.sqrt((1-x)**2+4*eps*x))/2
 B=-.5*math.sqrt(eps*x)/(1-u)
 vertex=initial[1]+initial[3]+2*B*(initial[0]+initial[2])
 return dict(epsilon=eps,x=x,omega_over_delta=omega,q=q,energy_residual=abs(2*w-omega),
  amplitude_dimensionless=amp,group_velocity_dimensionless=velocity,derivative_error=abs(fd-velocity),
  nonradiative_over_NR_vacuum=ratio,photon_rate_correction=vertex**2*(omega/(1-u))**4)
rows=[row(e,x) for e in [1e-8,1e-6,1e-4,.01] for x in [.001,.1,2/7,1/3,.8]]
# Independent vacuum vertex normalization and low-density benchmark.
assert abs(cubic(np.array([0,1,0,0]),np.array([1,0,0,0]),1e-4,.1)-math.sqrt(1e-5))<1e-14
vac=row(1e-4,1e-6)
assert abs(vac['nonradiative_over_NR_vacuum']-1)<1e-5
# Exact coefficient extracted independently by polynomial convolution for one mode.
e=1e-4;x=2/7;r=row(e,x);ini=modes(0,e,x)[-1][1];fin=modes(r['q'],e,x)[0][1]
import sympy as s
z,y,w=s.symbols('z y w');ua,ub,va,vb=ini;U,V,W,Z=fin
a=ua*z+W*(y+w);ad=va*z+U*(y+w);b=ub*z+Z*(y+w);bd=vb*z+V*(y+w)
H=.5*math.sqrt(e*x)*(bd*a*a+b*ad*ad)+x/2*(ad*a*a+ad*ad*a)
ind=float(s.Poly(s.expand(H),z,y,w).coeff_monomial(z*y*w))
assert abs(ind-r['amplitude_dimensionless'])<1e-12
# Physical benchmark inherited from prior package, lambda_tot=1e-6.
m=1e6;delta=5;M=2*m+delta;lam=1e-6;kappa=lam/(4*m*m);n=x*delta/(4*kappa)
hbar=6.582119569e-16;c3sq=e*kappa*delta
nr_vac=c3sq*m**1.5*math.sqrt(delta)/math.pi/hbar
nonrad=nr_vac*r['nonradiative_over_NR_vacuum']
u=(1+x-math.sqrt((1-x)**2+4*e*x))/2
gap=delta*(1-u); cutoff=10*M
rad=n*n*gap**4/(256*math.pi*M*m*m*cutoff**6)/hbar*r['photon_rate_correction']
result=dict(rows=rows,vacuum_limit=vac,independent_vertex_error=abs(ind-r['amplitude_dimensionless']),
 benchmark=dict(nonradiative_width_s_inv=nonrad,radiative_width_s_inv=rad,branching_fraction=rad/(rad+nonrad),lifetime_seconds=1/(rad+nonrad)),
 scope='Zero-temperature homogeneous tree-level gapped-mode decay into two lower-branch excitations; M=2m in kinetic dispersion, delta/m neglected. No finite-cloud transport, preparation or experimental validation.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['benchmark'],indent=2));print('rows',len(rows),'vacuum ratio',vac['nonradiative_over_NR_vacuum'])
