#!/usr/bin/env python3
"""Spectral-notch test for a Duffing orbit; dimensionless, prescribed bath only."""
import json, sys
from pathlib import Path
import numpy as np
from scipy.special import ellipk, ellipj
from scipy.integrate import quad, solve_ivp

checks=[]
def check(name,actual,expected,rtol=1e-7,atol=1e-12):
    actual=float(actual); expected=float(expected)
    checks.append(dict(name=name,actual=actual,expected=expected,rtol=rtol,atol=atol,
                       passed=abs(actual-expected)<=atol+rtol*abs(expected)))

def orbit(E,lam=1.,N=8192):
    a2=2*E if lam==0 else 4*E/(1+np.sqrt(1+4*lam*E))
    a=np.sqrt(a2); w=np.sqrt(1+lam*a2); m=lam*a2/(2*(1+lam*a2))
    T=4*ellipk(m)/w; t=np.arange(N)*T/N
    sn,cn,dn,_=ellipj(w*t,m)
    x=a*cn; p=-a*w*sn*dn
    coeff=np.fft.rfft(x)/N
    return dict(T=T,omega=2*np.pi/T,a=a,x=x,p=p,h=coeff,t=t)

ref=orbit(1.); wr=ref['omega']; tr=ref['T']
def S0(w): return 2/(1+w*w) # OU covariance exp(-abs(t))
def single(w): return (w*w-wr*wr)**2/(1+w*w)**3
# xi(t)=eta(t)-eta(t-tau), exactly realizable as a delayed stationary OU signal.
def comb(w,tau): return 4*np.sin(w*tau/2)**2*S0(w)
def diffusion(o,spectrum,H=64):
    n=np.arange(1,H+1); w=n*o['omega']
    terms=w*w*abs(o['h'][1:H+1])**2*spectrum(w)
    return float(sum(terms)),terms

# Exact Duffing solution independently checked by ODE integration and energy.
sol=solve_ivp(lambda t,z:[z[1],-z[0]-z[0]**3],[0,tr],[ref['a'],0],
              t_eval=ref['t'],rtol=1e-11,atol=1e-12,method='DOP853')
assert sol.success
check('elliptic orbit versus ODE max error',np.max(abs(sol.y[0]-ref['x'])),0,atol=2e-9)
check('energy conservation max error',np.max(abs(ref['p']**2/2+ref['x']**2/2+ref['x']**4/4-1)),0,atol=2e-12)
n=np.arange(1,65)
check('Fourier kinetic Parseval',2*sum((n*wr)**2*abs(ref['h'][1:65])**2),np.mean(ref['p']**2),rtol=1e-10)
Dsingle,terms=diffusion(ref,single)
check('fundamental notch removes n1',terms[0],0,atol=1e-25)
assert terms[2]>1e-6
check('third harmonic dominates residual',sum(terms[1:]),terms[2],rtol=.002)
Dcomb,_=diffusion(ref,lambda w:comb(w,tr))
check('comb cutoff is zero to roundoff',Dcomb,0,atol=1e-25)

# Quadratic coefficient predicted by expansion about E_R=1.
dE=1e-5
wp=(orbit(1+dE)['omega']-orbit(1-dE)['omega'])/(2*dE)
c=float(sum((n*wr)**2*abs(ref['h'][1:65])**2*(n*wp*tr)**2*S0(n*wr)))
rows=[]
for q in [1e-2,1e-3,1e-4,1e-5]:
    o=orbit(1-q); d,_=diffusion(o,lambda w:comb(w,tr))
    d128,_=diffusion(o,lambda w:comb(w,tr),128)
    dn,_=diffusion(orbit(1-q,N=16384),lambda w:comb(w,tr))
    check(f'harmonic truncation q={q}',d,d128,rtol=1e-10,atol=1e-25)
    check(f'FFT resolution q={q}',d,dn,rtol=1e-9,atol=1e-25)
    check(f'quadratic coefficient q={q}',d/q**2,c,rtol=2*q+1e-5)
    rows.append(dict(q=q,D=d,D_over_q2=d/q**2))

# Timing detuning restores a floor ~ delta^2 at the original cutoff.
cdelta=float(sum((n*wr)**2*abs(ref['h'][1:65])**2*(n*wr*tr)**2*S0(n*wr)))
detuning=[]
for delta in [1e-2,1e-3,1e-4]:
    d,_=diffusion(ref,lambda w:comb(w,tr*(1+delta)))
    check(f'detuning quadratic floor delta={delta}',d/delta**2,cdelta,rtol=4e-4)
    detuning.append(dict(relative_delay_error=delta,D_at_original_cutoff=d))

# Harmonic oscillator: one frequency at every E, so a matched delay kills
# diffusion throughout the well, not at one selected energy.
for E in [.1,1.,10.]:
    o=orbit(E,lam=0)
    d,_=diffusion(o,lambda w:comb(w,2*np.pi))
    check(f'isochronous whole-well suppression E={E}',d,0,atol=1e-24)

# D=c*q^2, constant period: normalized target n=1/(2 sqrt(Q q)).
# Integrate q=Q*y^2, where n dq=dy, avoiding the endpoint singularity.
for Q in [.1,1.,10.]:
    norm=quad(lambda y:1.,0,1)[0]
    P=quad(lambda y:c*Q*y*y/2,0,1)[0]
    check(f'normalized target Q={Q}',norm,1.,rtol=1e-12)
    check(f'finite added power Q={Q}',P,c*Q/6,rtol=1e-12)
    q=Q/3; density=1/(2*np.sqrt(Q*q)); npq=-density/(2*q)
    check(f'target current Q={Q}',(1.5*c*q-2*c*q)*density-c*q*q*npq,0,atol=1e-15)
    # External divergence-form drift alone leaves a nonzero positive current.
    check(f'no selector from diffusion alone Q={Q}',-c*q*q*npq,c*q*density/2,rtol=1e-12)

# Time-domain covariance checks and finite-time fluctuations at the exact notch.
# These test secular-zero versus zero fluctuations; they are not nonlinear SDE runs.
def covariance(u):
    return 2*np.exp(-abs(u))-np.exp(-abs(u-tr))-np.exp(-abs(u+tr))
for wtest in [wr,3*wr,.9*wr]:
    spectrum_integral=2*(quad(lambda u:covariance(u)*np.cos(wtest*u),0,tr,epsabs=1e-11)[0]+
        quad(lambda u:covariance(u)*np.cos(wtest*u),tr,np.inf,epsabs=1e-11,limit=300)[0])
    check(f'time versus frequency spectrum w={wtest}',spectrum_integral,comb(wtest,tr),rtol=1e-8,atol=2e-11)
cp_weights=2*(n*wr)**2*abs(ref['h'][1:65])**2
Cp=lambda u: float(sum(cp_weights*np.cos(n*wr*u)))
variance_rows=[]
for periods in [2,5,10,20,50]:
    t=periods*tr
    variance=2*(quad(lambda u:(t-u)*covariance(u)*Cp(u),0,tr,epsabs=1e-10)[0]+
        quad(lambda u:(t-u)*covariance(u)*Cp(u),tr,t,epsabs=1e-10,limit=500)[0])
    assert variance>0
    variance_rows.append(dict(periods=periods,time=t,energy_variance_per_noise_amplitude_squared=variance,
                              apparent_diffusion=variance/(2*t)))
check('bounded transient variance plateau',variance_rows[-1]['energy_variance_per_noise_amplitude_squared'],
      variance_rows[2]['energy_variance_per_noise_amplitude_squared'],rtol=1e-9)
check('apparent diffusion decreases as inverse time',variance_rows[-1]['apparent_diffusion']*5,
      variance_rows[2]['apparent_diffusion'],rtol=1e-9)

r=dict(all_passed=all(t['passed'] for t in checks),check_count=len(checks),checks=checks,
       reference=dict(E_R=1,lambda_=1,T=tr,omega=wr,omega_E=wp,
                      single_notch_floor=Dsingle,third_harmonic_term=float(terms[2]),comb_floor=Dcomb,
                      quadratic_coefficient=c,detuning_coefficient=cdelta),
       gap_grid=rows,detuning_grid=detuning,finite_time_variance=variance_rows,
       scope='Finite harmonic truncation and numerical orbit tests of prescribed spectral filters; no bath feedback or empirical data.')
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='checks'},indent=2))
if not r['all_passed']:print(json.dumps([t for t in checks if not t['passed']],indent=2))
sys.exit(0 if r['all_passed'] else 1)
