"""Initial unbound-daughter production from newborn sources in the NR Plummer model."""
import json,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import beta as betaf
from scipy.integrate import quad
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];g=params['cubic_g_eV'];u=params['u']
c=299792458.;G=6.67430e-11;ev=1.602176634e-19;hb=1.054571817e-34;hbev=hb/ev;hc=hbev*c;year=365.25*86400;kpc=3.0856775814913673e19
rho0=1e-21;sigma0=200000.;vstar=u*c
scale=math.sqrt(9*sigma0*sigma0/(2*math.pi*G*rho0));mass=6*sigma0*sigma0*scale/G
esc0=6*sigma0*sigma0/vstar**2;xmax=math.sqrt((2*esc0)**2-1)
w0=(m*u)**3/(2*math.pi**2);K0=g*g*m*m*u**4/(16*math.pi**3)

checks=[]
def check(name,value):checks.append(dict(name=name,passed=bool(value)))
gyr=year*1e9
Gamma=g*g*u/(16*math.pi*m)/hbev*gyr

def escape_kernel(esc,q,A):
    # Probability-weighted decay coefficient for producing ONE unbound daughter.
    a=esc-(1+q*q)/2
    if q<=a:return 0.,0.
    z=a/q
    # Explicit angular quadrature avoids cancellation in the energy-weighted integral.
    zz,ww=leggauss(32);mu=z+(1-z)*(zz+1)/2;weights=ww*(1-z)/2
    boundf=A*((a+q*mu)/esc)**3.5
    stim=1+boundf
    L=Gamma*float(weights@stim)
    E=Gamma*float(weights@(stim*(q*mu-a)))
    analytic=Gamma*((1-z)+A/esc**3.5*((a+q)**4.5-(2*a)**4.5)/(4.5*q))
    check('angular decay integral',abs(L/analytic-1)<2e-10)
    check('positive outgoing orbital energy',E>=0 and E<=L*(q-a)*(1+1e-12))
    return L,E

def local(x,Q):
    esc=esc0/math.sqrt(1+x*x);rhoSI=rho0/(1+x*x)**2.5
    n=rhoSI*c*c/ev*hc**3/m
    A=n/(w0*math.sqrt(2)*esc**1.5*betaf(1.5,4.5))
    z,w=leggauss(Q);qmax=math.sqrt(2*esc-1)
    # Decay escape possible for |q-1|<sqrt(2esc), equivalently q>sqrt(2esc)-1 here.
    split=math.sqrt(2*esc)-1
    birth=number=energy=0.
    for lo,hi in [(0.,split),(split,qmax)]:
        qs=lo+(hi-lo)*(z+1)/2;wq=w*(hi-lo)/2
        ec=1+qs*qs;half=np.minimum(qs,esc-ec/2)
        e1=ec[:,None]/2+half[:,None]*z;e2=ec[:,None]-e1
        shape=np.maximum(1-e1/esc,0)**3.5*np.maximum(1-e2/esc,0)**3.5
        bw=wq*2*qs*half*(shape@w)
        birth+=float(sum(bw))
        for q,weight in zip(qs,bw):
            L,E=escape_kernel(esc,float(q),A)
            number+=weight*L;energy+=weight*E
    charge_rate=2*K0*A*A*birth/(n*hbev)*gyr
    return charge_rate,number/birth,energy/birth

def integrated(R,Q):
    z,w=leggauss(R);birth=number=energy=0.
    for lo,hi in [(0.,1.),(1.,xmax)]:
        for x,weight in zip(lo+(hi-lo)*(z+1)/2,w*(hi-lo)/2):
            rate,L,E=local(float(x),Q)
            term=weight*3*x*x/(1+x*x)**2.5*rate
            birth+=term;number+=term*L/4;energy+=term*E/4
    return dict(radial_order=R,energy_order=Q,birth_charge_rate_per_Gyr=birth,
        unbound_charge_fraction_t2_coefficient_per_Gyr2=number,
        positive_orbital_energy_over_M_vstar2_t2_coefficient_per_Gyr2=energy,
        birth_weighted_escape_decay_coefficient_per_Gyr=4*number/birth,
        mean_unbound_specific_orbital_energy_over_vstar2=energy/number)

runs=[integrated(16,16),integrated(24,24),integrated(40,40)]
for key in ['birth_charge_rate_per_Gyr','unbound_charge_fraction_t2_coefficient_per_Gyr2','positive_orbital_energy_over_M_vstar2_t2_coefficient_per_Gyr2']:
    check('radial/energy refinement '+key,abs(runs[-1][key]/runs[-2][key]-1)<2e-6)
# Independent original birth integral reference; does not validate new decay physics by itself.
reference=json.loads((p/'bound_halo_reactions_run/results.json').read_text())['runs'][-1]
check('original birth normalization',abs(runs[-1]['birth_charge_rate_per_Gyr']/reference['initial_global_source_charge_rate_per_Gyr']-1)<2e-6)
# All-bound final angles contribute zero; no unbound initial occupation or inverse sink.
check('subthreshold angular kernel vanishes',escape_kernel(2.,.1,1e5)==(0.,0.))
out=dict(all_pass=all(c['passed'] for c in checks),check_count=len(checks),
    checks=checks,runs=runs,
    non_claims=['Initial t^2 population with positive orbital energy only; no finite-time error bound',
               'Not outward flux at infinity or permanent mass loss; particles can react or be recaptured',
               'NR incoherent kinetic closure; no coherent field or contact stress',
               'No halo equilibrium, selected profile or vacuum acceleration law'])
(p/'unbound_daughter_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));assert out['all_pass']
