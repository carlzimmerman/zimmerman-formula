"""Ideal zero-temperature, two-spin neutral-atom Fermi reservoir; dilute impurity."""
import json,math,sys
from pathlib import Path
import sympy as s
import numpy as np
from numpy.polynomial.legendre import leggauss
checks=[]
def test(n,x):checks.append({'name':n,'passed':bool(x)});assert x,n
z=s.symbols('z',real=True)
test('energy transfer phase space',s.integrate(z**3*(1-z)**3,(z,0,1))==s.Rational(1,140))
# Number-density structure factor with delta(omega-energy), spin degeneracy two.
def sf(q,w,M,kF):
 kz=M*w/q-q/2
 upper=kF*kF-kz*kz
 lower=kF*kF-(kz+q)**2
 if upper<=0 or w<=0:return 0.
 # Avoid subtracting almost equal disk areas if both cuts are within the Fermi sphere.
 diff=2*M*w if lower>0 else upper
 return M*diff/(4*math.pi**2*q)
def power(v,M,kF,N):
 qn,wt=leggauss(N);zs=(qn+1)/2;weights=wt/2;Q=2*v # impurity m=1, contact g=1
 total=0.
 for z,zw in zip(zs,weights):
  q=Q*z
  for y,yw in zip(zs,weights):
   mu=z+(1-z)*y;omega=v*q*mu-q*q/2
   total+=zw*yw*Q*q*q*(1-z)*omega*sf(q,omega,M,kF)
 return total/(2*math.pi)
rows=[]
for M in [2.,10.511]:
 for v in [.0001,.001,.01]:
  p=power(v,M,1.,32);p2=power(v,M,1.,48);exact=M*M*v**6/(105*math.pi**3)
  test('phase-space power '+str((M,v)),abs(p/exact-1)<1e-10)
  test('quadrature '+str((M,v)),abs(p/p2-1)<1e-10)
  rows.append({'bath_mass_over_impurity':M,'v':v,'power_g1_m1':p,'analytic_ratio':p/exact})
# Direct structure-factor annulus check in arbitrary units.
for q,w in [(.1,.001),(.2,.005),(.01,.00001)]:
 M=3.;kF=1.;kz=M*w/q-q/2
 disk=(kF*kF-kz*kz)-max(0,kF*kF-(kz+q)**2)
 direct=M*max(0,disk)/(4*math.pi**2*q)
 test('annulus '+str((q,w)),abs(sf(q,w,M,kF)/direct-1)<1e-9)
hc=1.973269804e-7;hb=6.582119569e-16;alpha=1/137.035999084;m=1e6;MS=1e7;me=510998.95
red=me*MS/(me+MS);binding=red*alpha*alpha/2;MA=MS+me-binding;n=1e25
kF=hc*(3*math.pi**2*n)**(1/3);EF=kF*kF/(2*MA);a0=hc/(red*alpha)
g=1/(4*m*MS)
bench=[]
for K in [1e-9,1e-7,1e-5]:
 v=math.sqrt(2*K/m);p=g*g*MA*MA*m**4*v**6/(105*math.pi**3)/hb
 # Conditional drift scale, not mean first-passage time or full population temperature.
 bench.append({'K_eV':K,'energy_drift_eV_s':-p,'instantaneous_K_over_abs_drift_years':K/p/(365.25*86400),'v_over_vF':v/(kF/MA),'qmax_over_kF':2*m*v/kF,'qmax_a0_over_hbarc':2*m*v*a0/hc})
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'phase_space_rows':rows,'reservoir':{'n_m3':n,'messenger_mass_eV':MS,'neutral_atom_mass_eV':MA,'hydrogenic_binding_eV':binding,'Bohr_radius_m':a0,'kF_eV':kF,'EF_eV':EF,'T_F_K':EF/8.617333262e-5,'contact_g_eVminus2':g},'benchmarks':bench,'non_claims':['Hypothetical atoms, not observed matter','Ideal unpaired noninteracting bath at T=0, no preparation or phase-stability proof','Single-impurity energy drift only; finite bath and thermal diffusion omitted']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
