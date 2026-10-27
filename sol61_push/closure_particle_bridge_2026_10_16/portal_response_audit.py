"""Candidate-specific contact, force-range and halo-occupation diagnostics.

These are chosen density/velocity comparisons, not observational bounds or a
no-go theorem for occupied collective phases. All conversions are explicit.
"""
import json
import math
import sys
from pathlib import Path
from scipy.special import zeta

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent
phase=json.loads((base/'thermal_charge_run_002/results.json').read_text())
p=next(r['parameters'] for r in phase['phase_rows'] if r['parameters']['m']==.002)
c=299792458.;hbarc=1.973269804e-16 # GeV m
gev_j=1.602176634e-10;gev_kg=gev_j/c**2
pc=3.085677581491367e16;msun=1.98847e30
mh=125.;fN=.308;checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name
rows=[]
for density in (.001,.1,1000.):
    rho_kg=density*msun/pc**3
    # J/m^3 -> GeV^4: divide by J/GeV, multiply (hbar c)^3.
    rho_nat=rho_kg*c*c/gev_j*hbarc**3
    shift=-p['lp']*fN*rho_nat/mh**2
    fractional_contact=p['g']**2*shift/(p['gap']**2*p['rep'])
    # Exact algebraic difference, written to avoid subtracting equal floats.
    exact_contact=p['g']**2*shift/(p['gap']*(p['gap']+shift)*p['rep'])
    check('linear contact shift '+str(density),abs(fractional_contact/exact_contact-1)<1e-12)
    check('perturbative source shift '+str(density),abs(shift/p['gap'])<1e-40)
    rows.append(dict(density_Msun_per_pc3=density,density_kg_per_m3=rho_kg,
        density_GeV4=rho_nat,delta_source_mass_squared_GeV2=shift,
        delta_source_mass_squared_over_gap=shift/p['gap'],
        fractional_threshold_contact_shift=fractional_contact))
rhohalo=.3 # GeV cm^-3, rest-mass energy density
velocity=150000. # m/s one-dimensional dispersion
per_sign_n=rhohalo/(2*p['m'])*1e6 # m^-3
thermal_wavelength=math.sqrt(2*math.pi)*hbarc*c/(p['m']*velocity)
occupation=per_sign_n*thermal_wavelength**3
critical=float(zeta(1.5,1))
check('halo gas not quantum degenerate',occupation/critical<1e-15)
mcritical=p['m']*(occupation/critical)**.25
force_ranges={'Higgs_m':hbarc/mh,'daughter_m':hbarc/p['m'],
              'source_m':hbarc/p['M'],'one_kpc_mass_eV':hbarc/(1000*pc)*1e9}
check('kpc mass range inverse identity',abs(force_ranges['one_kpc_mass_eV']*1e-9*1000*pc/hbarc-1)<1e-14)
check('independent density conversion',abs(rows[1]['density_GeV4']/(rows[1]['density_kg_per_m3']/gev_kg*hbarc**3)-1)<1e-14)
result=dict(parameters=p,baryon_response=rows,force_ranges=force_ranges,
    halo=dict(total_rest_density_GeV_per_cm3=rhohalo,one_dimensional_dispersion_m_per_s=velocity,
        per_sign_number_per_m3=per_sign_n,thermal_wavelength_m=thermal_wavelength,
        per_sign_phase_space_occupation=occupation,ideal_Bose_critical_occupation=critical,
        ideal_critical_mass_eV=mcritical*1e9),checks=checks,
    source=dict(arxiv='1708.02245v2',fN=fN,fN_uncertainty=.018,
        meaning='2017 Higgs-nucleon input benchmark; abstract authenticated; no claim to latest determination'),
    non_claims=['No collective-mode exclusion','No galaxy data fit or universal particle mass bound','No prediction of actual halo temperature, state or condensate formation','No complete radiative matching: tree-level lambda_HPhi=0 is a specified matching input'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
