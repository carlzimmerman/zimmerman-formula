"""Prescribed damped-pump squeezing and inverse collision envelope bounds."""
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).parent;a=json.loads((p/'dilute_decay_v2_run/results.json').read_text())['rows'][-1]
m=a['m_eV'];M=a['M_eV'];G=a['source_width_eV'];O=a['pump_energy_eV'];nq=a['initial_charge_density_eV3'];r=O/G
R=2*r;occ_bound=math.sinh(R)**2
# Integration by parts bounds the full time-dependent alpha, not just its Born value 1.
C=1+math.cosh(R)+r*math.sinh(R);peak=4*r*r
L=1000.;I_envelope=peak*C*C*G/2*math.atan(L)
pstar=math.sqrt((M-2*m)*(M+2*m))/2
# Exact boosted DOS * lab width / angular energy span = Gamma0*M²/(4pi² pstar).
coef=M*M/(4*math.pi**2*pstar)
fraction_per_lifetime=2*coef*I_envelope**2/nq
checks=[];rows=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
for d in [0.,.5,2.,10.]:
    def rhs(t,y):
        alpha,beta=y;z=r*math.exp(-t/2)*np.exp(1j*d*t)
        return [-1j*z*beta,1j*np.conj(z)*alpha]
    t=np.linspace(0,30,1501)
    sol=solve_ivp(rhs,(0,30),np.array([1+0j,0j]),t_eval=t,method='DOP853',rtol=1e-12,atol=1e-14,max_step=.05)
    alpha,beta=sol.y;occ=abs(beta)**2
    born=1j*r*(1-np.exp(-(.5+1j*d)*t))/(.5+1j*d)
    norm=float(np.max(abs(abs(alpha)**2-occ-1)))
    envelope=peak*C*C/(1+4*d*d)
    ck('completed '+str(d),sol.success)
    ck('Bogoliubov normalization '+str(d),norm<1e-11)
    ck('uniform squeeze bound '+str(d),float(occ.max())<=occ_bound*(1+1e-10))
    ck('spectral envelope '+str(d),float(occ.max())<=envelope)
    if d==0:
        exact=np.sinh(2*r*(1-np.exp(-t/2)))**2
        ck('exact resonant solution',float(np.max(abs(occ-exact)))<1e-12)
    rows.append(dict(detuning_over_width=d,max_occupation=float(occ.max()),endpoint_occupation=float(occ[-1]),max_absolute_correction_to_Born=float(np.max(abs(occ-abs(born)**2))),relative_correction_normalized_to_peak=float(np.max(abs(occ-abs(born)**2)))/peak,norm_error=norm))
for eb in [1e-6,.001,.1]:
    P=math.sqrt(eb*(2*M+eb));dos=P*(M+eb)/(2*math.pi**2);half=P*pstar/M;lab=M/(M+eb)
    ck('exact inverse phase space cancellation '+str(eb),abs(dos*lab/(2*half)/coef-1)<1e-12)
ck('small stimulated correction bound',2*occ_bound+occ_bound**2<1e-3)
ck('small line-contained inverse fraction',fraction_per_lifetime<1e-6)
out=dict(rows=rows,uniform_exact_prescribed_pump_occupation_bound=occ_bound,max_gross_Bose_decay_fractional_enhancement=2*occ_bound+occ_bound**2,source_occupation_from_uncorrelated_inverse_upper_bound=occ_bound**2,spectral_envelope_numerator=C,band_halfwidth_in_pair_halfwidths=L,line_contained_inverse_charge_fraction_bound_per_vacuum_lifetime=fraction_per_lifetime,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Prescribed pump is not a self-consistent full field solution','Inverse bound covers particles inside declared line and uncorrelated kinetic reactions','Connected source-pair memory and off-resonant tails not bounded here','No halo formation or source origin'])
(p/'dilute_feedback_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
