"""Finite-time retention and laser detuning requirements at the 628W point."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
material=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())['preparation']
prior=json.loads(Path('sol61_push/low_power_preparation_2026_10_14/run/results.json').read_text())
base=next(r for r in prior['rows'] if r['intensity_per_wave_W_m2']==1e8 and r['common_laser_Lorentzian_FWHM_Hz']==.001)
omega=base['drive_per_s'];gamma=base['pair_coherence_decay_per_s'];T=base['nominal_pi_pulse_s'];tau0=prior['single_particle_lifetime_s']
checks=[];max_trace=max_herm=max_neg=0.
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def gen(tau,detuning_Hz):
    H=np.zeros((4,4));H[0,1]=H[1,0]=omega;H[1,1]=-4*math.pi*detuning_Hz
    I=np.eye(4);L=-1j*(np.kron(I,H)-np.kron(H.T,I))
    a=np.zeros((4,4));a[0,2]=1;a[3,1]=1
    b=np.zeros((4,4));b[0,3]=1;b[2,1]=1
    for c in [a/math.sqrt(tau),b/math.sqrt(tau),np.diag([-1,1,0,0])*math.sqrt(gamma/2)]:
        num=c.T@c;L+=np.kron(c,c)-.5*np.kron(I,num)-.5*np.kron(num.T,I)
    return L
initial=np.zeros(16,complex);initial[0]=1
def inspect(vector):
    global max_trace,max_herm,max_neg
    rho=vector.reshape((4,4),order='F')
    max_trace=max(max_trace,float(abs(np.trace(rho)-1)))
    max_herm=max(max_herm,float(np.max(abs(rho-rho.conj().T))))
    max_neg=max(max_neg,max(0.,-float(np.linalg.eigvalsh((rho+rho.conj().T)/2).min())))
    return float(rho[1,1].real)
def probability(tau,detuning_Hz=0):return inspect(expm(gen(tau,detuning_Hz)*T)@initial)
p0=probability(tau0)
ck('prior_baseline',abs(p0-base['pair_probability_at_pi_time']),1e-12)
retention=[dict(lifetime_s=tau,pair_probability=probability(tau)) for tau in [100.,220.6975,1000.,10000.,100000.,tau0]]
minimum_tau=math.exp(brentq(lambda logtau:probability(math.exp(logtau))-.1,math.log(1),math.log(1e8),xtol=1e-12))
ck('10percent_threshold',abs(probability(minimum_tau)-.1),1e-10)
halfwidth=brentq(lambda nu:probability(tau0,nu)-p0/2,0,.1,xtol=1e-14)
ck('halfheight_threshold',abs(probability(tau0,halfwidth)-p0/2),1e-10)
detunings=[]
for nu in [0.,1e-4,1e-3,1e-2,.1]:
    pg=probability(tau0,nu)
    ck('detuning_evenness',abs(pg-probability(tau0,-nu)),1e-12)
    # Independent stationary formula with detuning.
    kappa=gamma+1/tau0;Delta=4*math.pi*nu
    expected=omega**2*kappa/((kappa*kappa+Delta*Delta)/tau0+4*omega**2*kappa)
    A=gen(tau0,nu);A[0,:]=np.eye(4).reshape(16,order='F');rhs=np.zeros(16,complex);rhs[0]=1
    rho=np.linalg.solve(A,rhs).reshape((4,4),order='F')
    ck('detuned_stationary_formula',abs(rho[1,1]-expected),1e-10)
    detunings.append(dict(common_laser_offset_Hz=nu,pair_probability=pg,stationary_pair_probability=expected))
# Deterministic drift across resonance, separate from fast Wiener phase diffusion.
def drift(span,tol):
    sol=solve_ivp(lambda t,y:gen(tau0,span*(t/T-.5))@y,(0,T),initial,rtol=tol,atol=tol*1e-3,method='DOP853')
    assert sol.success
    return inspect(sol.y[:,-1])
drift_rows=[]
for span in [0.,.001,.01]:
    pg=drift(span,1e-8);tight=drift(span,1e-10)
    ck('drift_ODE_refinement',abs(pg-tight),1e-7)
    if span==0:ck('ODE_vs_matrix_exponential',abs(tight-p0),1e-9)
    drift_rows.append(dict(total_laser_frequency_sweep_Hz=span,drift_rate_Hz_per_s=span/T,pair_probability=tight))
ck('all_evolutions_trace',max_trace,2e-9);ck('all_evolutions_Hermiticity',max_herm,1e-10);ck('all_evolutions_positivity',max_neg,1e-9)
hPlanck=2*math.pi*6.582119569e-16
# Leading orbital geometry sensitivity; self-energy derivatives are excluded.
hc=1.973269804e-7;radius=.02;Uwall=material['wall_eV'];E0=material['single_particle_energy_eV']
x=radius/hc*math.sqrt(2*E0);z=radius/hc*math.sqrt(2*Uwall);beta=math.sqrt(z*z-x*x)
Fx=1/math.tan(x)-x/math.sin(x)**2-x/beta
energy_log_slope=2*(-z*z/(beta*x*Fx)-1)
pair_radius_slope=2*E0*energy_log_slope/radius
radius_allowance=2*hPlanck*halfwidth/abs(pair_radius_slope)
result=dict(scope='Four-state finite-time tolerance diagnostics with fixed source strength and assigned dephasing; independent loss and detuning knobs, not a complete material uncertainty propagation',leading_orbital_radius_sensitivity=dict(pair_energy_derivative_eV_per_m=pair_radius_slope,radius_change_for_halfheight_energy_m=radius_allowance,excluded="Derivative of pair self-energy, material barrier and other shifts"),baseline=base,retention_sweep=retention,minimum_single_carrier_lifetime_for_10percent_s=minimum_tau,laser_detuning_halfwidth_at_half_baseline_Hz=halfwidth,pair_energy_halfwidth_eV=2*hPlanck*halfwidth,laser_fractional_halfwidth_at_1eV=halfwidth/(1/hPlanck),detuning_sweep=detunings,linear_drift_sweep=drift_rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
