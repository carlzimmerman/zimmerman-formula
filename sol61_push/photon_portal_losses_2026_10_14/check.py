"""Tree-level free-carrier photon scattering and local spontaneous decay diagnostic."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
p=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())['preparation']
pulse=json.loads(Path('sol61_push/confined_pair_pulse_2026_10_14/run/results.json').read_text())
m=1.; M=2.+2e-9; mu=.002; g=1e-20; hc=1.973269804e-7; hb=6.582119569e-16; ej=1.602176634e-19; c=299792458.
w=(2*m+p['dressed_pair_excess_eV'])/2; checks=[]
def ck(name,error,tolerance):
    assert error<=tolerance,(name,error,tolerance)
    checks.append(dict(name=name,error=float(error),tolerance=tolerance))
def dot(a,b):return a[0]*b[0]-np.dot(a[1:],b[1:])
def numerator(u,w=w):
    wp=w/(1+w/m*(1-u)); sn=math.sqrt(1-u*u)
    k=np.array([w,0,0,w]); kp=np.array([wp,wp*sn,0,wp*u])
    eins=[np.array([0,1,0,0]),np.array([0,0,1,0])]
    eouts=[np.array([0,u,0,-sn]),np.array([0,0,1,0])]
    T=lambda e,ep:dot(k,kp)*dot(e,ep)-dot(k,ep)*dot(kp,e)
    polsum=sum(T(e,ep)**2 for e in eins for ep in eouts)/2
    t=-2*w*wp*(1-u)
    return polsum,t,max(abs(T(k,ep)) for ep in eouts),max(abs(T(e,kp)) for e in eins)
for u in [-1,-.8,-.2,.2,.8,.999]:
    pol,t,w1,w2=numerator(u)
    ck('polarization_trace',abs(pol/(t*t/4)-1),1e-12)
    ck('incoming_Ward',w1,1e-12);ck('outgoing_Ward',w2,1e-12)
def cross(w,minimum_q=0.):
    s=m*m+2*m*w; Q=(s-m*m)**2/s
    if Q<=minimum_q:return 0.
    dimensionless=quad(lambda y:y*y/(1+y)**2,minimum_q/M**2,Q/M**2,epsabs=1e-16,epsrel=1e-11)[0]
    return mu*mu*g*g*M*M*dimensionless/(64*math.pi*(s-m*m)**2)*hc*hc
sigma=cross(w)
s=m*m+2*m*w; Q=(s-m*m)**2/s; b=Q/M**2
analytic=mu*mu*g*g*M*M*(b+1-1/(1+b)-2*math.log1p(b))/(64*math.pi*(s-m*m)**2)*hc*hc
ck('analytic_integral_relative',abs(analytic/sigma-1),1e-12)
def lab(u):
    pol,t,_,_=numerator(u); wp=w/(1+w/m*(1-u))
    return mu*mu*g*g*pol/(M*M-t)**2/(32*math.pi*m*m)*(wp/w)**2*hc*hc
angular=quad(lambda u:lab(u)/sigma,-1,1,epsabs=1e-12,epsrel=1e-12)[0]
ck('independent_lab_cross_section',abs(angular-1),1e-12)
# Treat enough recoil to exceed the ideal wall height as a loss diagnostic.
qcut=2*m*(p['wall_eV']-p['single_particle_energy_eV'])
eject=cross(w,qcut);flux=2*1e12/(w*ej)
# Isotropic blackbody number spectrum: collision rate c times density times cross section.
kT=8.617333262e-5*300
thermal=quad(lambda x:x*x/math.expm1(x)*cross(kT*x,qcut)/sigma,1e-7,100,epsabs=1e-11,epsrel=1e-9)[0]*sigma*c*kT**3/(math.pi**2*hc**3)
width=g*g*M**3/(64*math.pi)
virtual=p['virtual_mediator_probability'];pairloss=virtual*width/hb
result=dict(scope='Born free-carrier impulse scattering; vacuum local mediator-width approximation; no stimulated sideband or wall loss calculation',photon_energy_eV=w,photon_wavelength_m=2*math.pi*hc/w,scattering_cross_section_m2=sigma,ejecting_cross_section_m2=eject,peak_two_beam_flux_per_m2_s=flux,peak_independent_beam_collision_rate_per_s=flux*sigma,peak_independent_beam_ejection_rate_per_s=flux*eject,blackbody_300K_ejection_rate_per_s=thermal,mediator_vacuum_photon_width_eV=width,pair_spontaneous_photon_conversion_rate_per_s=pairloss,spontaneous_radiated_power_per_pair_W=pairloss*(2*m+p['dressed_pair_excess_eV'])*ej,pulse_pair_collision_probability_upper_diagnostic=2*flux*sigma*pulse['pulse_duration_s'],pulse_spontaneous_conversion_probability_diagnostic=pairloss*pulse['pulse_duration_s'],checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
