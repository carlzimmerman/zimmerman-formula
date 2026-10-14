"""Scoped comparison of assigned portal couplings, not a global exclusion fit."""
import json,math,sys
from pathlib import Path
alpha=1/137.035999084;mmu=105658375.5;g=1e-20;mu=.002;m=1.;delta=2e-9;M=2*m+delta;hb=6.582119569e-16;c=299792458.
y=abs(g)*3*math.pi*mmu/(2*alpha)
beta=math.sqrt(delta*(4*m+delta))/M
width_dark=mu*mu*beta/(16*math.pi*M);width_photon=g*g*M**3/(64*math.pi)
comparisons=[dict(name='HB photon coupling, Eq15',value=g*1e9,bound=6.7e-11,units='GeV^-1'),dict(name='HB muonic scalar Yukawa, Eq16a',value=y,bound=4.6e-9,units='dimensionless'),dict(name='SN cooling scalar cold model, TableI',value=y,bound=4.2e-9,units='dimensionless'),dict(name='SN cooling scalar hot model, TableI',value=y,bound=1.9e-9,units='dimensionless')]
for r in comparisons:r['benchmark_over_reference_bound']=r['value']/r['bound']
assert all(r['benchmark_over_reference_bound']<1 for r in comparisons)
assert abs(2*alpha*y/(3*math.pi*mmu)/g-1)<1e-14
assert 0<width_photon<width_dark
result=dict(scope='Numerical comparison to named source benchmark bounds; added carrier interaction invalidates blanket transfer of the source model',mediator_mass_eV=M,photon_coupling_per_eV=g,photon_coupling_per_GeV=g*1e9,muon_Yukawa_magnitude=y,reference_comparisons=comparisons,dark_partial_width_eV=width_dark,photon_partial_width_eV=width_photon,vacuum_photon_branching_ratio=width_photon/(width_photon+width_dark),vacuum_rest_lifetime_s=hb/(width_photon+width_dark),illustrative_decay_lengths=[dict(energy_eV=E,mean_flight_length_m=c*hb/(width_photon+width_dark)*math.sqrt((E/M)**2-1)) for E in [1e3,1e4,1e8]],assertions_passed=3)
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
