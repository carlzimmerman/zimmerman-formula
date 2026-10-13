"""Conditional local source-mode relaxation in a stipulated incoherent daughter bath."""
import json,math,itertools
from pathlib import Path
from fractions import Fraction
from scipy.integrate import quad,solve_ivp
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];M=params['M_eV'];g=params['cubic_g_eV'];u=params['u']
c=299792458.;ev=1.602176634e-19;hb=1.054571817e-34;hbev=hb/ev;hc=hbev*c;year=365.25*86400
beta=u/math.sqrt(1+u*u);Gamma=g*g*beta/(8*math.pi*M)
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
# Algebraic cancellation verified exactly, without subtracting large cubic terms.
for f1,f2,F in itertools.product([Fraction(0),Fraction(1,3),Fraction(2),Fraction(100)],repeat=3):
 lhs=f1*f2*(1+F)-F*(1+f1)*(1+f2)
 rhs=f1*f2-F*(1+f1+f2)
 check('exact Bose gain-loss cancellation',lhs==rhs)
for f1,f2,F in itertools.product([.1,1.,10.],repeat=3):
 a=f1*f2*(1+F);b=F*(1+f1)*(1+f2)
 check('entropy production sign',(a-b)*math.log(a/b)>=-1e-13)
# Independent two-body differential phase-space normalization, identical-particle factor 1/2.
pstar=m*u
Gamma2=(4*g*g)*pstar/(8*math.pi*M*M)/2
check('two body width normalization',math.isclose(Gamma,Gamma2,rel_tol=1e-14))
norm=quad(lambda q:math.sqrt(2/math.pi)*q*q*math.exp(-q*q/2),0,math.inf)[0]
check('Gaussian occupation density normalization',abs(norm-1)<1e-12)
rows=[]
for rho_si in [1e-23,1e-21,1e-19]:
 rho=rho_si*c*c/ev*hc**3;n=rho/m
 for sigma_kms in [50,100,200,300,1000]:
  sigma=sigma_kms*1000/c
  f=(2*math.pi)**1.5*n/(m*sigma)**3*math.exp(-u*u/(2*sigma*sigma))
  rate=Gamma*(1+2*f);tau=hbev/rate
  rows.append(dict(rho_kg_m3=rho_si,sigma_1d_kms=sigma_kms,resonant_occupation=f,mode_relaxation_Gyr=tau/year/1e9,rate_over_dephasing_energy=rate/(m*sigma*sigma),mode_equilibrium_occupation=f*f/(1+2*f)))
# Fixed-bath mode equation scaled to equilibrium and relaxation time.
sol=solve_ivp(lambda t,z:[1-z[0]],(0,10),[0.],rtol=1e-11,atol=1e-13,t_eval=[.1,1,3,10])
check('fixed bath kinetic equation',sol.success and max(abs(sol.y[0]-(1-__import__('numpy').exp(-sol.t))))<2e-11)
# Detailed balance using moderate Bose distributions avoids overflow or catastrophic cancellation.
T=.4;mu=.1;E1=1.2;E2=1.5;Echi=E1+E2
f1=1/math.expm1((E1-mu)/T);f2=1/math.expm1((E2-mu)/T);F=1/math.expm1((Echi-2*mu)/T)
check('chemical equilibrium mu_chi=2mu_phi',abs(f1*f2-F*(1+f1+f2))<1e-17)
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,parameters=dict(m_eV=m,M_eV=M,g_eV=g,u=u),vacuum_width_eV=Gamma,vacuum_lifetime_years=hbev/Gamma/year,fastest_sigma_1d_kms=u*c/math.sqrt(3)/1000,non_claims=['Conditional zero-momentum source mode in a fixed isotropic daughter bath','Not a halo heat conduction, condensation, settling or profile-selection time','No transport closure, source backreaction, spatial dynamics or observational viability'])
(p/'resonant_kinetics_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks:',len(checks));assert out['all_pass']
