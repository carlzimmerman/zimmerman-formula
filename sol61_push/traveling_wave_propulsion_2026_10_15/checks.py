"""Conditional wave momentum accounting; no demonstrated dark coupling."""
import json, math
from pathlib import Path
import sympy as s

p = Path(__file__).parent
x,t,k,w,U0=s.symbols('x t k w U0', positive=True, real=True)
U=U0*s.cos(k*x-w*t)
checks={'traveling_source_work_force_identity':s.simplify(s.diff(U,t)+(w/k)*s.diff(U,x))==0}
c=299792458.; G=6.67430e-11; eV=1.602176634e-19
rho=.3e9*eV/c**2*1e6
L=5.7543993733715695*3.085677581491367e16
v=math.sqrt(2*math.pi*G*rho)*L
# Ideal outgoing, gapless, longitudinal waves in the specified displacement lift:
# P=rho*xi; L=dot(P)^2/(2rho)-gamma*(grad P)^2/2.
# Fractional density amplitude delta=k*P0/rho; I=rho*v^3*delta^2/2.
A=100.; delta=.1
I=.5*rho*v**3*delta**2
stress=I/v
rows=[]
for target in [1e-9,1.]:
    area=target/stress
    rows.append({'target_force_N':target,'ideal_wave_power_W':target*v,
                 'effective_wave_area_m2':area,'equivalent_disk_radius_m':math.sqrt(area/math.pi)})
# Independent energy-density route for the same plane-wave field.
omega=v; P0=rho*delta; gamma=v*v/rho
energy_mean=.25*(omega**2/rho+gamma)*P0**2
checks['wave_energy_flux_consistent']=math.isclose(energy_mean*v,I,rel_tol=1e-14)
checks['force_power_ratio_consistent']=math.isclose(stress*v,I,rel_tol=1e-14)
# A single vacuum plane EM wave has invariant E^2-c^2 B^2=0.
E,B=s.symbols('E B',real=True); cc=s.symbols('c',positive=True)
checks['single_plane_wave_invariant_zero']=s.simplify((E**2-cc**2*B**2).subs(B,E/cc))==0
result={'checks':{a:bool(b) for a,b in checks.items()},
 'assigned_inputs':{'density_GeV_cm3':.3,'Lstar_pc':5.7543993733715695,'area_m2':A,'fractional_density_amplitude':delta},
 'benchmark':{'rho_kg_m3':rho,'gapless_wave_speed_m_s':v,'wavelength_1m_frequency_Hz':v,
 'directed_wave_W_per_N':v,'coupling_efficiency_to_beat_photons':v/c,
 'intensity_W_m2':I,'momentum_flux_N_m2':stress,'force_for_assigned_area_N':stress*A,
 'wave_power_for_assigned_area_W':I*A,'targets':rows,
 'static_meter_scale_suppression_estimate':(1/L)**2},
 'nonclaims':['No physical dark species or coupling measured','No source solution or achieved conversion efficiency',
 'No universal wave amplitude or thrust bound','Plane-wave estimate assumes homogeneous medium at rest, a gapless stable longitudinal lift, and weak perturbations',
 'No laboratory apparatus design validated; no claim this density or fluid approximation applies inside apparatus']}
(p/'run_v1/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
