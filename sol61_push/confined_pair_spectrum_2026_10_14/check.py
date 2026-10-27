"""Finite-well reference spectrum, not finite-shell resonance lifetimes."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.special import spherical_jn,spherical_kn
from scipy.optimize import brentq
prior=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())
pulse=json.loads(Path('sol61_push/confined_pair_pulse_2026_10_14/run/results.json').read_text())
p=prior['preparation']; U=p['wall_eV']; hc=1.973269804e-7; hb=6.582119569e-16
m=1.; a=.02/hc; z=a*math.sqrt(2*m*U)
checks=[]
def ck(name,error,tolerance):
    assert error<=tolerance,(name,error,tolerance)
    checks.append(dict(name=name,error=float(error),tolerance=tolerance))
def det(x,l):
    b=np.sqrt(z*z-np.asarray(x)**2)
    return x*spherical_jn(l,x,derivative=True)-b*spherical_kn(l,b,derivative=True)/spherical_kn(l,b)*spherical_jn(l,x)
def spectrum(N):
    rows=[]
    for l in range(math.ceil(z)+1):
        xs=np.linspace(1e-5,z-1e-8,N); vals=det(xs,l)
        for n,i in enumerate(np.flatnonzero(vals[:-1]*vals[1:]<0),1):
            x=brentq(lambda t:det(t,l),xs[i],xs[i+1],xtol=1e-13)
            rows.append(dict(l=l,n=n,x=x,energy_eV=x*x/(2*m*a*a),degeneracy=2*l+1))
    return sorted(rows,key=lambda r:r['energy_eV'])
a1=spectrum(4000); levels=spectrum(8000)
assert [(r['l'],r['n']) for r in a1]==[(r['l'],r['n']) for r in levels]
ck('grid_refinement_max_energy_eV',max(abs(u['energy_eV']-v['energy_eV']) for u,v in zip(a1,levels)),1e-20)
ck('ground_energy_vs_prior_eV',abs(levels[0]['energy_eV']-p['single_particle_energy_eV']),1e-21)
for row in levels:
    ck('matching_residual',abs(float(det(row['x'],row['l']))),1e-10)
    if row['l']==0:
        x=row['x']; b=math.sqrt(z*z-x*x)
        ck('independent_s_wave_condition',abs(x/math.tan(x)+b),1e-10)
# Ordered species have distinct charges; list i<=j only for energy classification.
pairs=[]
for i,u in enumerate(levels):
    for j in range(i,len(levels)):
        v=levels[j]
        if i==j==0:continue
        E=u['energy_eV']+v['energy_eV']
        pairs.append(dict(first=[u['l'],u['n']],second=[v['l'],v['n']],bare_energy_eV=E,detuning_eV=E-p['dressed_pair_excess_eV'],even_parity=(u['l']+v['l'])%2==0))
pairs.sort(key=lambda r:r['bare_energy_eV'])
allowed=next(r for r in pairs if r['even_parity'])
# Inversion symmetry forbids odd total parity for the stipulated source and wall.
# This does not assert nonzero amplitude for every even-parity channel.
for row in [pairs[0],allowed]:
    w=row['detuning_eV']/hb
    row['angular_detuning_per_s']=w
    row['first_order_population_bound_per_drive_frequency_squared_s2']=(4*math.pi**2/(pulse['ramp_s']**2*w**3))**2
result=dict(scope='Independent-particle reference well spectrum; no excited-state interaction shifts or full multimode evolution',well_depth_eV=U,z=z,levels=levels,
    orbital_multiplets=len(levels),states_including_magnetic_degeneracy=sum(r['degeneracy'] for r in levels),lowest_competitor_any_parity=pairs[0],lowest_even_parity_competitor=allowed,
    nearest_ten_pair_energies=pairs[:10],ground_pair_nonlinear_shift_eV=p['virtual_mediator_self_energy_eV'],checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['levels','checks','nearest_ten_pair_energies']},indent=2))
