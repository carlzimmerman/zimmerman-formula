import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import solve_ivp
p=Path(__file__).parent;old=json.loads((p/'INPUT_WIDTHS.json').read_text());ref=next(r for r in old['rows'] if r['epsilon']==1e-4 and r['x']==2/7)
# Maxwell invariant for parallel-polarized opposite plane waves.
a,b,E=s.symbols('a b E',real=True)
assert s.expand(2*((E*a-E*b)**2-(E*a+E*b)**2)+8*E**2*a*b)==0
assert s.expand(2*((E*a)**2-(E*a)**2))==0
checks=[]
# Driven damped oscillator in tau=Gamma*t; source f/Gamma=1.
for det in [0,.1,1,10]:
 def rhs(t,y):
  re,im=y;return [-re/2+det*im,-im/2-det*re-1]
 end=8.;sol=solve_ivp(rhs,[0,end],[0,0],rtol=1e-11,atol=1e-12)
 z=.5+1j*det;exact=-1j*(1-__import__('cmath').exp(-z*end))/z
 err=abs(complex(*sol.y[:,-1])-exact);assert sol.success and err<1e-9
 checks.append(dict(detuning_over_width=det,error=err))
m=1e6;delta=5.;M=2*m+delta;lam=1e-6;x=2/7;eps=1e-4
n=x*delta*m*m/lam;cutoff=10*M;g=n/(2*m*cutoff**3)
u=(1+x-math.sqrt((1-x)**2+4*eps*x))/2;omega=delta*ref['omega_over_delta']
vertex=math.sqrt(ref['photon_rate_correction']*((1-u)/ref['omega_over_delta'])**4)
hbar=6.582119569e-16;hc=1.973269804e-7;eV=1.602176634e-19;c=299792458.
gamma=old['benchmark']['radiative_width_s_inv'];matter=old['benchmark']['nonradiative_width_s_inv'];total=gamma+matter
rows=[]
for eta in [1e-12,1e-9,1e-6]:
 ns=eta*n;drive=hbar*total*math.sqrt(ns)/2
 unatural=drive*math.sqrt(2*M)/(g*vertex)
 intensity=unatural*eV/hc**3*c
 density_ns=ns/hc**3
 optical=density_ns*omega*eV*gamma
 deposited=density_ns*omega*eV*matter
 rows.append(dict(excited_occupation_density_over_daughters=eta,per_beam_intensity_W_m2=intensity,
  stored_excitation_J_m3=density_ns*omega*eV,spontaneous_photon_power_W_m3=optical,
  matter_decay_power_W_m3=deposited,net_drive_power_W_m3=optical+deposited,
  intensity_over_cutoff_to_fourth=2*unatural/cutoff**4))
result=dict(checks=checks,exact_Maxwell_identities=2,rows=rows,
 optical_pair_frequency_Hz=omega/(2*math.pi*hbar),drive_resonance_FWHM_Hz=total/(2*math.pi),
 amplitude_relaxation_seconds=2/total,
 scope='Undepleted two-plane-wave drive, rotating-wave linear oscillator at k=0, prescribed condensate and Markov damping; static spatial response, propagation and confinement omitted.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
