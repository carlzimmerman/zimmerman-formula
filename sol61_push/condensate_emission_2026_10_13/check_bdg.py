#!/usr/bin/env python3
"""Conditional condensate final-state emission; finite-volume factors and SI scales."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
import sympy as s
checks=[]
def check(name,a,b,rtol=1e-9,atol=1e-12):
 checks.append(dict(name=name,actual=float(a),expected=float(b),passed=bool(abs(a-b)<=atol+rtol*abs(b))))
N,k=s.symbols('N k',real=True)
assert s.expand(k*((N+2)*(N+1)-N*(N-1))-k*(4*N+2))==0
x=s.symbols('x',real=True)
assert s.factor(s.diff(x*x*(1-x)**4,x))==2*x*(x-1)**3*(3*x-1)
assert s.expand(s.Rational(4,27)-x*(1-x)**2-(x-s.Rational(1,3))**2*(s.Rational(4,3)-x))==0
assert s.factor(s.diff(x*x*(1-x)**5,x))==-x*(x-1)**4*(7*x-2)
for n in [0,1,10,100]:
 dim=n+4;a=np.diag(np.sqrt(np.arange(1,dim)),1);ket=np.eye(dim)[:,n]
 check(f'Fock final-state factor N={n}',np.linalg.norm(a.T@a.T@ket)**2,(n+1)*(n+2))
for n in [10,1000,100000]:
 # n and volume grow together: enhancement becomes density squared, not N^2 luminosity.
 V=n/3.
 check(f'thermodynamic factor N={n}',(n+1)*(n+2)/V**2,9*(1+3/n+2/n**2))
# Independent Lane-Emden mass integral for n=1 contact-fluid profile.
I=quad(lambda z:z*math.sin(z),0,math.pi,epsabs=1e-12)[0]
check('n=1 profile mass integral',I,math.pi)
# Exact frozen-background lower chemical-potential branch versus dilute mixing.
background=[]
def gapped_mode(eps,X):
 u=(1+X-math.sqrt((1-X)**2+4*eps*X))/2
 A=X-u/2;C=math.sqrt(eps*X);D=1-u;mu=u/2
 L=np.array([[A,C,mu,0],[C,D,0,0],[-mu,0,-A,-C],[0,0,-C,-D]])
 vals,vecs=np.linalg.eig(L);idx=int(np.argmax(vals.real));omega=float(vals[idx].real)
 v=vecs[:,idx].real;norm=np.dot(v[:2],v[:2])-np.dot(v[2:],v[2:])
 assert norm>0 and abs(vals[idx].imag)<1e-10
 v=v/math.sqrt(norm);B=-.5*math.sqrt(eps*X)/D
 vertex=v[1]+v[3]+2*B*(v[0]+v[2])
 return omega,float(vertex*vertex),D*D+X*(X-u)+2*eps*X
for eps in [1e-4,1e-8]:
 for X in [.1,2/7,1/3,.8]:
  u=(1+X-math.sqrt((1-X)**2+4*eps*X))/2
  check(f'background stationary identity eps={eps} x={X}',(X-u)*(1-u),eps*X)
  omega,vertex2,gap2=gapped_mode(eps,X)
  check(f'Bogoliubov gap eps={eps} x={X}',omega*omega,gap2)
  background.append(dict(epsilon=eps,x=X,twice_mu_over_delta=u,effective_gap_over_delta=1-u,
   full_gapped_frequency_over_delta=omega,photon_vertex_squared_relative_to_bare=vertex2,
   mode_radiative_rate_over_bare=vertex2*(omega/(1-u))**4,
   coherent_source_charge_fraction_relative_to_daughters=eps*X/(2*(1-u)**2)))
# Physical rows use leading weak-mixing density x=2/7 (power optimum).
m=1e6;delta=5.;M=2*m+delta;cutoff=10*M;eps=1e-4;X=2/7
hbar=6.582119569e-16;hc=1.973269804e-7;eV=1.602176634e-19;clight=299792458.;G=6.67430e-11
physical=[]
for lam in [1.,1e-3,1e-6,1e-9,1e-12]:
 kappa=lam/(4*m*m);n=X*delta/(4*kappa)
 u=(1+X-math.sqrt((1-X)**2+4*eps*X))/2;gap=delta*(1-u)
 c3=math.sqrt(eps*kappa*delta);B=-c3*n/gap
 Imaxwell=1+2*B*n/(2*m*math.sqrt(2*M)*cutoff**3)
 radiative=n*n*gap**4/(256*math.pi*M*m*m*cutoff**6)/hbar
 g=c3*2*m*math.sqrt(2*M)
 vacuum_g0=g*g/(8*math.pi*M)*math.sqrt(1-4*m*m/(M*M))/hbar
 rho=n/hc**3*m*eV/clight**2
 cs=clight*math.sqrt(X*delta/(2*m))
 K=cs*cs/(2*rho);R=math.sqrt(math.pi*K/(2*G));mass=4*rho*R**3/math.pi
 photon_energy=gap/2
 physical.append(dict(lambda_tot=lam,density_kg_m3=rho,photon_energy_eV=photon_energy,wavelength_nm=1239.8419843320026/photon_energy,
  radiative_partial_rate_s_inv=radiative,power_per_kg_of_added_source_excitations_W=radiative*gap/M*clight**2,
  vacuum_ordinary_width_s_inv=vacuum_g0,radiative_over_vacuum_ordinary=radiative/vacuum_g0,
  maxwell_kinetic_coefficient=Imaxwell,positive_Maxwell=bool(Imaxwell>0),
  daughter_field_over_cutoff=math.sqrt(n/(2*m))/cutoff,source_background_field_over_cutoff=abs(B)/math.sqrt(2*M)/cutoff,
  gap_narrowness=hbar*radiative/gap,sound_speed_m_s=cs,
  sound_crossing_one_cm_s=.01/cs,TF_self_gravitating_radius_m=R,TF_mass_at_given_central_density_kg=mass,
  compactness_2GM_Rc2=2*G*mass/(R*clight**2)))
result=dict(all_passed=all(c['passed'] for c in checks),checks=checks,symbolic_identities=4,background=background,physical=physical,
 scope='Projected condensate final-state transition and weak-mixing background; photon vacuum escape and prepared source excitations stipulated. Negative Maxwell rows are rejected. No full in-medium spectral function, source inventory, confinement, optical transport, empirical validation or device.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
sys.exit(0 if result['all_passed'] else 1)
