"""Quantify direct cosmological-constant gravity and an optional Ricci mass portal."""
import math,json
from pathlib import Path
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
G=6.67430e-11;c=299792458.;hb=6.582119569e-16;kpc=3.0856775814913673e19
rhoL=6e-27 # declared illustration, not a fitted cosmological measurement
kappa=.5;H2=8*math.pi*G*rhoL/3;a0=kappa*c*math.sqrt(G*rhoL)
checks=[]
def check(n,v):checks.append(dict(name=n,passed=bool(v)))
rows=[]
for speed in [50e3,100e3,200e3,300e3]:
    # Define test baryonic mass using the target law only for comparison.
    Mb=speed**4/(G*a0);rM=math.sqrt(G*Mb/a0);rt=(G*Mb/H2)**(1/3)
    ratio=H2*rM/a0;analytic=8*math.pi/(3*kappa*kappa)*(speed/c)**2
    check('vacuum force ratio elimination',abs(ratio/analytic-1)<1e-14)
    check('turnaround force cancellation',abs((G*Mb/rt**2)/(H2*rt)-1)<1e-13)
    rows.append(dict(target_speed_kms=speed/1000,target_transition_kpc=rM/kpc,
                     direct_vacuum_acceleration_over_a0=ratio,turnaround_kpc=rt/kpc))
# At fixed fraction f of turnaround, actual circular velocity includes repulsion.
f=.5
masses=[1e39,1e40,1e41]
v4=[]
for M in masses:
    rt=(G*M/H2)**(1/3);r=f*rt;v2=G*M/r-H2*r*r
    expected=(G*M)**(2/3)*H2**(1/3)*(1/f-f*f)
    check('circular speed including Lambda',abs(v2/expected-1)<1e-13)
    v4.append(v2*v2)
slope=math.log(v4[-1]/v4[0])/math.log(masses[-1]/masses[0])
check('turnaround-family mass exponent',abs(slope-4/3)<1e-14)
# Scalar curvature energy scale: (hbar c)^2 R=32 pi G rhoL hbar^2.
curv=32*math.pi*G*rhoL*hb*hb
m=params['m_eV'];delta=4*m*m*params['u']**2
check('Ricci scalar scale',abs(curv/(12*H2*hb*hb)-1)<1e-14)
out=dict(all_pass=all(q['passed'] for q in checks),checks=checks,
    illustrative_vacuum_mass_density_kg_m3=rhoL,target_a0_m_s2=a0,rows=rows,
    fixed_turnaround_fraction_v4_mass_exponent=slope,
    ricci_energy_squared_eV2=curv,
    order_one_curvature_mass_shift_over_m2=curv/(m*m),
    xi_chi_minus_4_xi_phi_for_gap_scale_shift=delta/curv,
    xi_phi_for_mass_scale_shift=m*m/curv,
    non_claims=['Direct local Lambda force and optional bare curvature mass terms only',
               'Does not exclude cosmological formation, nonlocal boundary effects or other portals',
               'Large curvature coefficients are not by themselves an inconsistency proof',
               'Target law used only to set comparison masses, never derived'])
(p/'vacuum_selector_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
