"""Static standing-wave scalar potential and a conditional evolution bound."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
p=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())['preparation']
pulse=json.loads(Path('sol61_push/confined_pair_pulse_2026_10_14/run/results.json').read_text())
hc=1.973269804e-7; hb=6.582119569e-16; ej=1.602176634e-19; c=299792458.
m=1.; M=2.+2e-9; mu=.002; g=1e-20; I=1e12
u=(I/c)/(ej/hc**3);omega=(2*m+p['dressed_pair_excess_eV'])/2
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
# Heaviside-Lorentz natural units: a single wave has mean energy density Eamp^2/2.
Eamp=math.sqrt(2*u)
for z in [.1,.7,1.5]:
    for t in [.2,.9,2.1]:
        e1=Eamp*math.cos(z-t);e2=Eamp*math.cos(z+t)
        electric=e1+e2;magnetic=e1-e2
        invariant=2*(magnetic**2-electric**2)
        formula=-8*u*(math.cos(2*z)+math.cos(2*t))
        ck('field_invariant_relative_to_peak',abs(invariant-formula)/(16*u),1e-14)
# Independent Yukawa-kernel normalization in dimensionless radius y=M*r.
ck('positive_Yukawa_inverse_norm',abs(quad(lambda y:y*math.exp(-y),0,math.inf)[0]-1),1e-12)
plane=abs(mu*g)*u/(m*(M*M+4*omega*omega))
bound=abs(mu*g)*u/(m*M*M)
area=pulse['pulse_duration_s']-pulse['ramp_s']
phase=bound*area/hb
result=dict(scope='Prescribed counterpropagating fields, quasistatic free scalar response, bounded carrier-number sector; excludes stimulated sideband losses',wave_energy_density_eV4=u,plane_wave_potential_amplitude_eV=plane,arbitrary_bounded_envelope_potential_bound_eV=bound,ratio_to_ground_orbital_energy=bound/p['single_particle_energy_eV'],ratio_to_wall_barrier=bound/p['wall_eV'],pulse_envelope_integral_s=area,one_carrier_integrated_operator_norm=phase,two_carrier_unitary_state_distance_bound=2*phase,two_carrier_orthogonal_leakage_bound=(2*phase)**2,ten_carrier_cutoff_event_probability_change_bound=10*phase,quasistatic_response_to_ramp_ratio=hb/(M*pulse['ramp_s']),checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
