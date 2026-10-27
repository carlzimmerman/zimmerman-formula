import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import quad
# Background-field self-energy expansion, with complex scalar loop multiplicity.
g,z,S,L=s.symbols('g z S L',real=True,nonzero=True)
expr=-4*(g+z*S/(4*L**3))**2+4*g*g
assert s.expand(expr).coeff(S,1)==-2*g*z/L**3
assert s.expand(-2*(g+z*S/(4*L**3))**2+2*g*g).coeff(S,1)==-g*z/L**3
# Euclidean zero-external-momentum bubble: radial integral and its exact cutoff form.
checks=[]
a=1.;b=4.
for K in [2,10,100,1000]:
 exact=(-a*math.log1p(K*K/a)+b*math.log1p(K*K/b))/(b-a)/(16*math.pi**2)
 num=quad(lambda t:t/((t+a)*(t+b)),0,K*K,epsabs=1e-11)[0]/(16*math.pi**2)
 assert abs(num-exact)<1e-10
 checks.append(dict(cutoff_over_light_mass=K,integral=exact,quadrature_error=abs(num-exact)))
slope=(checks[-1]['integral']-checks[-2]['integral'])/math.log(10)
assert abs(slope-1/(8*math.pi**2))<1e-5
# Illustrative on-shell finite bubble with an explicitly chosen zero matching coefficient at Lambda.
m=1e6;M=2000005.;cutoff=10*M;delta=5.;kappa=1e-6/(4*m*m);eps=1e-4
c3=math.sqrt(eps*kappa*delta);gc=c3*2*m*math.sqrt(2*M)
def Iren(scale):
 return -quad(lambda x:math.log((x*M*M+(1-x)*m*m-x*(1-x)*m*m)/scale**2),0,1,epsabs=1e-12)[0]/(16*math.pi**2)
loop=-2*gc/cutoff**3*Iren(cutoff)
# Renormalization-scale dependence cancels only when the local coefficient runs.
scales=[]
for Q in [m,M,cutoff]:
 loopQ=-2*gc/cutoff**3*Iren(Q)
 counter=loop-loopQ
 assert abs(counter+loopQ-loop)<1e-38
 scales.append(dict(scale_eV=Q,loop_coefficient_eV_minus2=loopQ,required_local_coefficient_eV_minus2=counter))
fields=[]
for ratio in [.01,.1,1.]:
 Bfield=ratio*cutoff**2
 shift=loop*Bfield**2/m
 fields.append(dict(magnetic_field_over_cutoff_squared=ratio,conditional_magnetic_potential_eV=shift))
needed=math.sqrt(m/abs(loop))/cutoff**2
out=dict(cutoff_checks=checks,logarithmic_slope=slope,expected_asymptotic_slope=1/(8*math.pi**2),
 cubic_coupling_eV=gc,illustrative_C_phi_eV_minus2=loop,scale_checks=scales,field_diagnostics=fields,
 field_over_cutoff_squared_for_one_eV_magnitude=needed,
 scope='Single one-loop bubble and explicit zero-at-cutoff matching illustration. Finite local coefficients remain independent inputs; no UV completion, empirical admission or actual trapping field.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
