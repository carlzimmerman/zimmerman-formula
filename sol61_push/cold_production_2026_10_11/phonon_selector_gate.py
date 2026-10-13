"""Condensate phase-action and degeneracy gate for the detuned carrier."""
import json,math
from pathlib import Path
from scipy.special import zeta
p=Path(__file__).parent
par=json.loads((p/'detuned_carrier_run/results.json').read_text())['parameters']
bound=json.loads((p/'nr_quantum_bound_run/results.json').read_text())['NR_coefficients']
m=par['m_eV'];gap=bound['gap_eV'];cc=bound['cubic'];k=bound['quartic'];r2=cc*cc/(gap*k)
checks=[]
def check(n,e,t):checks.append(dict(name=n,error=float(e),passed=bool(abs(e)<t)))
def pressure(y):return y*y/(4*(1-r2/(1-2*y))) if y>0 else 0.
rows=[]
for y in [1e-5,.001,.01,.05,.1]:
 keff=1-r2/(1-2*y);n=y/(2*keff);ns=r2*n*n/(1-2*y)**2
 h=y*1e-4;der=(pressure(y+h)-pressure(y-h))/(2*h)
 check('pressure derivative equals charge '+str(y),der/(n+2*ns)-1,1e-7)
 rows.append(dict(mu_over_gap=y,effective_quartic_over_k=keff,daughter_density_scaled=n,source_density_scaled=ns,pressure_scaled=pressure(y)))
# Low-X exponent diagnostic.
check('low density pressure exponent',math.log(pressure(2e-7)/pressure(1e-7))/math.log(2)-2,1e-6)
hbar=1.054571817e-34;ev=1.602176634e-19;c=299792458.;rho=1e-21;sig=200000.;mk=m*ev/c**2
number=rho/mk;lamT=math.sqrt(2*math.pi)*hbar/(mk*sig);deg=number*lamT**3
sigc=math.sqrt(2*math.pi)*hbar/mk*(number/zeta(1.5,1))**(1/3)
mcrit=(rho*(math.sqrt(2*math.pi)*hbar/sig)**3/zeta(1.5,1))**.25*c*c/ev
check('BEC threshold cross check',(sigc/sig)**3-deg/zeta(1.5,1),1e-15)
out=dict(parameters=par,phase_branch=rows,r_squared=r2,positive_coherent_branch_mu_over_gap_upper=(1-r2)/2,halo_ideal_gas_gate=dict(rho_kg_m3=rho,sigma_one_dimension_m_s=sig,thermal_wavelength_m=lamT,phase_space_density=deg,critical_phase_space_density=float(zeta(1.5,1)),critical_sigma_m_s=sigc,critical_mass_eV_at_fixed_rho_sigma=mcrit),checks=checks,all_pass=all(t['passed'] for t in checks),non_claims=['Coherent uniform saddle and low-gradient phase action, not the multimode halo state','Ideal-gas equilibrium condensation screen, not a no-go for nonequilibrium coherent subcomponents','No baryon coupling or vacuum selector generated'])
(p/'phonon_selector_gate_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
