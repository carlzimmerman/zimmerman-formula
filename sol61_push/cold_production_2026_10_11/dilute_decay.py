"""Dilute near-threshold decay branch and narrow-line number-conservation audit."""
import json,math
from pathlib import Path
from scipy.integrate import quad
p=Path(__file__).parent
base=json.loads((p/'detuned_carrier_run/results.json').read_text())['parameters']
hb=6.582119569e-16;u=base['u'];rho=base['rho_source_eV4'];alpha=2.
rows=[];checks=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
for m in [base['m_eV'],1e4,1e5,3e5,1e6]:
    M=2*m*math.sqrt(1+u*u);lm=base['lambda_min']*(m/base['m_eV'])**1.5
    g=2*m*u*math.sqrt(lm);A=math.sqrt(rho)/(math.sqrt(2)*M)
    width=g*g*(u/math.sqrt(1+u*u))/(8*math.pi*M)
    pump=2*g*A/M
    peak=4*(pump/width)**2
    # Exact constant-DOS identity at line centre, narrow-line Wigner-Weisskopf approximation.
    E0=M/2;pstar=m*u;dos=E0*pstar/(2*math.pi**2)
    daughter_line_number=dos*math.pi*pump*pump/width
    nq=2*rho/M
    ck('narrow line number normalization '+str(m),abs(daughter_line_number/nq-1)<1e-12)
    rows.append(dict(m_eV=m,M_eV=M,lambda_min=lm,lambda_rep=alpha*lm,lambda_total=(1+alpha)*lm,cubic_g_eV=g,source_amplitude_eV=A,epsilon=g*A/(m*m),source_width_eV=width,source_lifetime_seconds=hb/width,pump_energy_eV=pump,width_over_pump=width/pump,asymptotic_peak_daughter_occupation=peak,uniform_time_occupation_bound=4*peak,width_over_gap=width/(M-2*m),threshold_sigma_over_mass_cm2_g=alpha**2,initial_charge_density_eV3=nq,initial_free_pressure_over_energy=u*u/(3*(1+u*u))))
chosen=rows[-1]
# In units y=2*pair detuning/Gamma, tau=Gamma*t, the line integral is analytic.
# |beta|²=peak*[1+exp(-tau)-2exp(-tau/2)cos(y*tau/2)]/(1+y²).
controls=[]
for tau in [.1,1.,5.,10.]:
    L=1000.
    norm=2*math.atan(L)
    oscill=quad(lambda y:1/(1+y*y),0,L,weight='cos',wvar=tau/2,epsabs=1e-11,epsrel=1e-11,limit=200)[0]*2
    I=(1+math.exp(-tau))*norm-2*math.exp(-tau/2)*oscill
    frac=I/(2*math.pi)
    exact=1-math.exp(-tau)
    bound=(1+math.exp(-tau/2))**2*(math.pi-norm)/(2*math.pi)
    ck('finite line integral tail bound '+str(tau),abs(frac-exact)<=bound+1e-10)
    controls.append(dict(Gamma_t=tau,finite_band_daughter_charge_fraction=frac,infinite_constant_DOS_value=exact,absolute_tail_bound=bound))
ck('chosen branch dilute through bounded pulse',chosen['uniform_time_occupation_bound']<1e-3)
ck('chosen branch narrow line',chosen['width_over_gap']<1e-4)
ck('chosen branch quartic perturbative scale',chosen['lambda_total']<.1)
out=dict(rows=rows,line_integral_controls=controls,checks=checks,all_pass=all(c['passed'] for c in checks),scope='Positive-square action, alpha2; fixed source energy density and u; masses vary holding illustrative threshold sigma/m=4 cm2/g; narrow-line vacuum decay approximation',non_claims=['No microscopic origin of initial charged source','No full renormalized quantum evolution','No cosmological transfer or halo formation','No observational viability of chosen self interaction'])
(p/'dilute_decay_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
