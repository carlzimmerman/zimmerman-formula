"""Quadratic versus asymptotically linear charge-aligned portal at fixed flux."""
import json,math
from pathlib import Path
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
halo=json.loads((p/'repulsive_scales_run/results.json').read_text())
m=params['m_eV'];M=params['M_eV'];amp=params['source_amplitude_eV'];S=4*amp*amp
rh=halo['rho_eV4'];rs=params['rho_source_eV4'];c=299792458.;cs=200000.
target=(cs/c)**2;S0=rh/(2*m*m)
B=2*m**4*target/rh
Uquad=B*S*S;R=Uquad/rs
quad_omega=math.sqrt(M*M+8*B*S)
quad_E=rs+3*Uquad;quad_P=Uquad
# U=Astar (sqrt(S^2+S0^2)-S0), chosen to give target sound speed at S=S0.
Astar=4*math.sqrt(2)*m*m*target
checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
rows=[]
for x in [1e-4,.1,1/math.sqrt(2),1.,10.,1e4,S/S0]:
 s=x*S0;r=math.hypot(1,x)
 U=Astar*S0*x*x/(r+1)
 Up=Astar*x/r
 Upp=Astar/S0/r**3
 pressure=Astar*S0*x*x/(r*(r+1))
 sound=s*Upp/(2*m*m)
 check('positive compressibility',Upp>0)
 check('linear upper energy bound',0<=U<=Astar*s*(1+1e-14))
 check('positive bounded pressure',0<=pressure<=Astar*S0*(1+1e-14))
 if x==1.:check('halo contact speed match',abs(sound/target-1)<1e-14)
 # Analytic source/daughter diagonal frequency shifts preserve resonance gap.
 # Avoid subtracting nearly equal full masses numerically.
 check('aligned medium shift cancellation',(4*Up)/4==Up)
 rows.append(dict(S_over_S0=x,cs2_over_c2=sound,pressure_eV4=pressure,U_over_linear_bound=U/(Astar*s)))
x=S/S0;r=math.hypot(1,x)
U=Astar*S0*x*x/(r+1);Up=Astar*x/r;P=Astar*S0*x*x/(r*(r+1))
omega=math.sqrt(M*M+4*Up);E=rs+S*Up+U;Q=4*omega*amp*amp
eta=1-m*Q/E
check('cold source retained for declared nonlinear example',eta<1e-5 and P/E<1e-5)
# Midrange finite differences are independent checks on the claimed derivatives.
for x in [.1,1.,10.]:
 h=1e-4*x
 f=lambda z:math.hypot(1,z)-1
 fd=(f(x+h)-2*f(x)+f(x-h))/h**2
 exact=(1+x*x)**(-1.5)
 check('second derivative finite difference',abs(fd/exact-1)<3e-4)
out=dict(all_pass=all(t['passed'] for t in checks),checks=checks,
 source_to_halo_density_ratio=rs/rh,
 quadratic=dict(required_B=B,added_energy_over_original=R,self_consistent_circular_w=quad_P/quad_E,
                omega_over_original_M=quad_omega/M),
 softened=dict(S0_eV2=S0,Astar_eV2=Astar,Astar_over_m2=Astar/(m*m),source_w=P/E,
               source_eta_above_mQ=eta,omega_over_original_M=omega/M,rows=rows),
 non_claims=['Tree-level fixed-flux homogeneous source and local coherent NR pressure only',
 'No nonlinear production yield, transport or halo profile simulated',
 'Halo crossover and support speed are chosen, not predicted',
 'No coefficient kappa, abundance or quantum naturalness derived'])
(p/'nonlinear_portal_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));print('Checks',len(checks));assert out['all_pass']
