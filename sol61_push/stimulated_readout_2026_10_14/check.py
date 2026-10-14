"""Optimistic single-pump readout into one independent empty optical mode."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import solve_continuous_lyapunov
from scipy.optimize import minimize_scalar
import sympy as sy
p=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())
omega0=p['preparation']['pair_drive_angular_frequency_per_s'];tau=p['resonances'][2]['single_particle_tunneling_lifetime_s']
w=1+p['preparation']['dressed_pair_excess_eV']/2;ej=1.602176634e-19;c=299792458.;hb=6.582119569e-16
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def eff(eta,gamma,kappa):return 4*eta*eta*kappa/((gamma+kappa)*(gamma*kappa+4*eta*eta))
y,k,e=sy.symbols('gamma kappa eta',real=True)
assert sy.expand((y+k)*(y*k+4*e**2)-k*(y+2*e)**2-y*(k-2*e)**2)==0
# Independent integrated master-amplitude evolution, using well-conditioned dimensionless cases.
for eta in [.001,.1,1.,10.]:
    for kappa in [.01,1.,100.]:
        A=np.array([[-.5,-1j*eta],[-1j*eta,-kappa/2]])
        rho0=np.diag([1.,0.]);integrated=solve_continuous_lyapunov(A,-rho0)
        numerical=float(kappa*integrated[1,1].real)
        ck('integrated_Lyapunov_efficiency',abs(numerical-eff(eta,1,kappa))/max(eff(eta,1,kappa),1e-30),2e-8)
    optimum=minimize_scalar(lambda logk:-eff(eta,1,math.exp(logk)),bounds=(-20,20),method='bounded')
    ck('optimal_output_coupling',abs(math.exp(optimum.x)/(2*eta)-1),2e-5)
rows=[]
for length in [.1,1.,10.]:
    for intensity in [1e8,1e12]:
        power=math.pi*.002**2*intensity/2
        photons=power*length/(c*w*ej)
        Omega=omega0*intensity/1e12;chi=Omega/photons;eta=Omega/math.sqrt(photons);gamma=2/tau
        kopt=2*eta;upper=(2*eta/(gamma+2*eta))**2
        rows.append(dict(effective_traveling_mode_length_m=length,intensity_W_m2=intensity,circulating_power_W=power,coherent_photon_number=photons,bare_four_mode_coupling_per_s=chi,one_pump_readout_coupling_per_s=eta,pair_population_loss_per_s=gamma,optimized_output_decay_per_s=kopt,optimized_photon_storage_time_s=1/kopt,ideal_capture_efficiency_upper_bound=upper,efficiency_at_assigned_output_decay_1000_per_s=eff(eta,gamma,1000.),lossless_swap_time_s=math.pi/(2*eta)))
result=dict(scope='Conditional two-independent-traveling-mode quantization with inherited coherent overlap; zero detuning/dephasing, ideal detection and no additional photon loss',assumed_single_carrier_lifetime_s=tau,photon_energy_eV=w,rows=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
