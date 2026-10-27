"""Vacuum resonance and explicitly conditional classical kinetic diagnostic."""
import json,math,sys
from pathlib import Path
from scipy.integrate import quad
import numpy as np
m=1.; delta=2e-9; MR=2.; hc=1.973269804e-7; hb=6.582119569e-16
c=299792458.; evkg=1.7826619216278976e-36
vr=2*math.sqrt(delta/m); beta=vr/2
sig=30000/c; mean=4*sig/math.sqrt(math.pi)
rho=.3*1e9*evkg*1e6 # assigned 0.3 GeV/cm^3
nopp=rho/(2*m*evkg)
def f(v):return v*v/(2*math.sqrt(math.pi)*sig**3)*math.exp(-v*v/(4*sig*sig))
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
ck('relative_distribution_normalization',abs(quad(lambda x:f(x*sig)*sig,0,20,epsabs=1e-12)[0]-1),1e-12)
ck('mean_relative_speed',abs(quad(lambda x:f(x*sig)*x*sig*sig,0,20,epsabs=1e-14)[0]/mean-1),1e-12)
rows=[]
for lam in [1e-6,1e-15]:
    mu2=lam*MR*MR; width=mu2*beta/(16*math.pi*MR); epsilon=2*width/m
    C=mu2*mu2/(64*math.pi*m**6)
    peak=C/epsilon**2; unitary=16*math.pi/(m*m*vr*vr)
    ck('peak_elastic_unitarity',abs(peak/unitary-1),1e-14)
    # Near-pole constant-width approximation, checked without a missed narrow bin.
    nwa=math.pi*mu2/(4*m**4*vr)*f(vr)
    windows=[]
    for L in [10.,100.]:
        limit=math.atan(L)
        numerical=C/(2*epsilon)*quad(lambda z:f(math.sqrt(vr*vr+epsilon*math.tan(z))),-limit,limit,epsabs=1e-12,epsrel=1e-11)[0]
        expected=nwa*(2*limit/math.pi)
        ck('resolved_pole_window',abs(numerical/expected-1),2e-5)
        windows.append(dict(half_widths=L,ratio_to_window_NWA=numerical/expected))
    sig_eff=nwa/mean*hc*hc
    nominal_collision_rate=nopp*nwa*hc*hc*c
    tau=hb/width
    rows.append(dict(lambda_rep=lam,Gamma_phi_eV=width,lifetime_s=tau,
        unlike_resonance_peak_m2=peak*hc*hc,
        conditional_sigma_eff_per_mass_m2_per_kg=sig_eff/(m*evkg),
        nominal_classical_collision_rate_per_s=nominal_collision_rate,
        collision_rate_times_lifetime=nominal_collision_rate*tau,pole_windows=windows))
ck('rate_lifetime_coupling_cancellation',abs(rows[0]['collision_rate_times_lifetime']/rows[1]['collision_rate_times_lifetime']-1),1e-14)
# Same-sign threshold contact plus t/u exchange; identical final-state factor 1/2.
for row in rows:
    lam=row['lambda_rep']; mu2=lam*MR*MR
    amplitude=-4*lam+2*mu2/(MR*MR)
    cross=amplitude*amplitude/(128*math.pi*m*m)*hc*hc
    ck('same_sign_threshold',abs(cross/(lam*lam/(32*math.pi*m*m)*hc*hc)-1),1e-14)
    row['same_sign_threshold_sigma_per_mass_m2_per_kg']=cross/(m*evkg)
# Phase-space occupancy for an assigned equal-sign Maxwellian gas.
# f_phase(p=0)=(2pi)^3 n_sign/(2pi m^2 sig^2)^(3/2), with n in natural units.
occupancy=(2*math.pi)**1.5*nopp*hc**3/(m*sig)**3
result=dict(resonance_relative_speed_m_per_s=vr*c,
    assigned_density_kg_per_m3=rho,one_particle_1D_dispersion_m_per_s=sig*c,
    nominal_peak_phase_space_occupation_per_sign=occupancy,
    diagnostic_not_empirical_bound='Maxwellian binary-collision interpretation is not admitted at these occupancy and delay parameters',
    cases=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
