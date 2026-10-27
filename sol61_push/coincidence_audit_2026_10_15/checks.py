"""Exact identities and provenance-screened scale comparisons, not discovery."""
import json, math
from pathlib import Path
import sympy as s
p=Path(__file__).parent
G,rho,L=s.symbols('G rho L',positive=True)
K=4*s.pi*G
gamma=K*L**2/2
inertia=1/rho
checks={}
checks['mass_displacement_speed']=s.simplify(gamma/inertia-(4*s.pi*G*rho)*L**2/2)==0
# For V=rv+m^2 r^2/2+lambda r^4/4, the dilute cold EOS has
# p=lambda rho_c^2/(4m^4). The n=1 Newtonian TF radius follows.
beta,rv=s.symbols('beta rv',positive=True)
RTF2=s.pi*beta/(8*G*rv)
Rds2=3/(8*s.pi*G*rv)
checks['TF_vacuum_radius']=s.simplify(RTF2/Rds2-s.pi**2*beta/3)==0
checks['linked_square_ratio']=s.simplify((RTF2/Rds2).subs(beta,s.Rational(1,4))-s.pi**2/12)==0
GN=6.67430e-11; hb=1.054571817e-34; c=299792458.; eV=1.602176634e-19
pc=3.085677581491367e16; Gyr=365.25*86400*1e9
Lmin=json.loads(Path('campaign_fresh_gravity/CFG691_stiffness_window/cfg691_results.json').read_text())['numbers']['G_SS']['canonical']['Lmin_pc']
rows=[]
for rgev in [.3,.035]:
    dens=rgev*1e9*eV/(c*c)*1e6
    omg=math.sqrt(4*math.pi*GN*dens)
    rows.append(dict(assigned_density_GeV_cm3=rgev,at_Lmin_wave_speed_m_s=omg*Lmin*pc/math.sqrt(2),inverse_gravitational_rate_Gyr=1/omg/Gyr))
vd=1e5; assigned_m=2e-20*eV/(c*c)
wavelength=2*math.pi*hb/(math.sqrt(2)*assigned_m*vd)/pc
matching_m=2*math.pi*hb/(math.sqrt(2)*Lmin*pc*vd)*c*c/eV
result={'checks':{k:bool(v) for k,v in checks.items()},'illustrative_mass_displacement':rows,
 'near_match':{'stiffness_lower_bound_pc':Lmin,'assigned_mass_eV':2e-20,
 'assigned_demixing_speed_km_s':100,'fastest_wavelength_pc':wavelength,
 'mass_needed_to_match_Lmin_eV':matching_m,'classification':'Input-sensitive; not independent evidence'},
 'linked_square_TF_to_deSitter_ratio':math.pi/math.sqrt(12),
 'nonclaims':['No derivation of Lstar or carrier mass','No identification of quantum-gradient and polarization-gradient operators',
 'TF radius comparison is a formal local Newtonian scaling, not a static horizon-scale solution']}
(p/'run_v1/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
