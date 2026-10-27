#!/usr/bin/env python3
"""Declared physical-unit map and a conditional mode-mass moment control."""
import argparse,json,math
from pathlib import Path
from scipy.integrate import quad

hbar=1.054571817e-34
c=299792458.
eV=1.602176634e-19
G=6.67430e-11
m=1e6*eV/c**2
mb=1.67492749804e-27
lam=.00587528017
gb=2.
K=lam*hbar**3/(4*m**4*c)
Kb=hbar*hbar/(5*mb**(8/3))*(6*math.pi**2/gb)**(2/3)
Gdim=1/(4*math.pi)
Kdim=.5
Kbdim=.4
L0=math.sqrt(K*Gdim/(G*Kdim))
M0=(Kb*Gdim/(G*L0*Kbdim))**3
T0=math.sqrt(Gdim*L0**3/(G*M0))
rho0=M0/L0**3
v02=L0**2/T0**2
taudim=hbar*hbar/(2*m*m)*T0*T0/L0**4
x1=2.36924317416
Nd=1.26043509806
Nb=.841802494120
R=x1*L0
Md=4*math.pi*Nd*M0
Mb=4*math.pi*Nb*M0
pf=hbar*(6*math.pi**2*rho0/(gb*mb))**(1/3)
ascat=lam*hbar/(8*math.pi*m*c)
delta_eV=2e6*(math.sqrt(1+.02**2)-1)
checks=[]
def check(name,condition,value=None):
    assert condition,(name,value)
    checks.append({'name':name,'value':value,'passed':True})
check('G unit map',abs(G*M0*T0*T0/L0**3/Gdim-1)<1e-13)
check('K unit map',abs(K*M0*T0*T0/L0**5/Kdim-1)<1e-13)
check('Kb unit map',abs(Kb*M0**(2/3)*T0*T0/L0**4/Kbdim-1)<1e-13)
compact=G*(Md+Mb)/(R*c*c)
fermi=pf/(mb*c)
dilute=(rho0/m)*ascat**3
source_ratio=(m*v02/eV)/delta_eV
check('weak field for declared TF point',compact<1e-10,compact)
check('nonrelativistic declared ideal fermions',fermi<1e-3,fermi)
check('dilute scalar at TF center',dilute<1e-10,dilute)
check('contact energy below source detuning',source_ratio<1e-6,source_ratio)
check('declared physical parameter is deep TF',taudim<1e-12,taudim)
for cutoff in (1.,2.,10.,100.):
    numeric=quad(lambda d:d**4/(1+d*d)**1.5,0,cutoff,epsabs=1e-10)[0]
    exact=cutoff*math.sqrt(1+cutoff*cutoff)/2+cutoff/math.sqrt(1+cutoff*cutoff)-1.5*math.asinh(cutoff)
    check('conditional target mass moment '+str(cutoff),abs(numeric-exact)<1e-8,exact)
vz=4/45-8/(3*math.pi**2)+20/math.pi**4
C=2/(9*math.pi**2)-4/189
out={'status':'passed','checks':checks,'check_count':len(checks),
 'declared_inputs':{'m_MeV':1.,'lambda_rep':lam,'ideal_fermion_mass_kg':mb,'spin_degeneracy':gb},
 'unit_map':{'K_SI':K,'Kb_SI':Kb,'L0_m':L0,'M0_kg':M0,'T0_s':T0,'rho0_kg_per_m3':rho0,'v0_squared_m2_per_s2':v02,'tau_dimensionless':taudim},
 'formal_TF_point':{'R_m':R,'Md_kg':Md,'Mb_kg':Mb,'compactness':compact,'pF_over_mbc':fermi,'scalar_n_a3':dilute,'contact_over_source_detuning':source_ratio},
 'internal_fluid_moment':{'Vz':vz,'Omega_eff_squared_over_GM_over_R3':vz/(4*C)},
 'limitations':'Declared ideal nonrelativistic baryon EOS only. No claim of ordinary-matter chemical stability, neutron survival, ionization/nuclear/EM closure, formation or a certified finite-GP profile at this tiny tau. TF numbers are scale maps, not the full-GP numerical controls.'}
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);args=pa.parse_args()
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'passed','check_count':len(checks),'tau_dimensionless':taudim,'R_TF_m':R,'Ceff':vz/(4*C)}))
