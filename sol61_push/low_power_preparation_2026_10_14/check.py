"""Power/storage/phase-noise tradeoff in the strong-blockade four-state model."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
p=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())
baseomega=p['preparation']['pair_drive_angular_frequency_per_s'];tau=p['resonances'][2]['single_particle_tunneling_lifetime_s']
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def generator(omega,gamma,leak):
    H=np.zeros((4,4));H[0,1]=H[1,0]=omega;I=np.eye(4)
    L=-1j*(np.kron(I,H)-np.kron(H.T,I))
    a=np.zeros((4,4));a[0,2]=1;a[3,1]=1
    b=np.zeros((4,4));b[0,3]=1;b[2,1]=1
    dephase=np.diag([-1,1,0,0])*math.sqrt(gamma/2)
    for c in [math.sqrt(leak)*a,math.sqrt(leak)*b,dephase]:
        num=c.T@c
        L+=np.kron(c,c)-.5*np.kron(I,num)-.5*np.kron(num.T,I)
    return L
initial=np.zeros(16,complex);initial[0]=1

def evolve(omega,gamma,leak,t):
    rho=(expm(generator(omega,gamma,leak)*t)@initial).reshape((4,4),order='F')
    ck('trace',abs(np.trace(rho)-1),2e-9)
    ck('Hermiticity',float(np.max(abs(rho-rho.conj().T))),1e-10)
    ck('positivity',max(0.,-float(np.linalg.eigvalsh(rho).min())),1e-10)
    return np.real(np.diag(rho))
# Independent analytic damped-Rabi solution at zero leakage.
for gamma in [0.,.3,3.]:
    omega=1.;t=.7
    d=np.sqrt(complex(gamma*gamma/4-4*omega*omega))
    z=np.exp(-gamma*t/2)*(np.cosh(d*t)+gamma/(2*d)*np.sinh(d*t))
    expected=(1-z.real)/2
    ck('analytic_dephased_Rabi',abs(evolve(omega,gamma,0,t)[1]-expected),1e-12)
rows=[]
for intensity in [1e6,1e8,1e9,1e10]:
    omega=baseomega*intensity/1e12;t=math.pi/(2*omega)
    for linewidth in [0.,1e-6,1e-3]:
        gamma=4*math.pi*linewidth
        pop=evolve(omega,gamma,1/tau,t)
        # Solve the steady-state linear system independently of analytic formula.
        L=generator(omega,gamma,1/tau);rhs=np.zeros(16,complex);rhs[0]=1
        L[0,:]=np.eye(4).reshape(16,order='F')
        stationary=np.linalg.solve(L,rhs).reshape((4,4),order='F')
        predicted=omega*omega*tau/(gamma+1/tau+4*omega*omega*tau)
        ck('steady_state_pair_formula',abs(stationary[1,1]-predicted),1e-10)
        ck('steady_single_balance',max(abs(stationary[2,2]-predicted),abs(stationary[3,3]-predicted)),1e-10)
        rows.append(dict(intensity_per_wave_W_m2=intensity,circulating_power_per_wave_W=math.pi*.002**2*intensity/2,drive_per_s=omega,nominal_pi_pulse_s=t, five_ms_ramp_four_state_probability_comparison_bound=omega*.005+2*.005/tau,common_laser_Lorentzian_FWHM_Hz=linewidth,pair_coherence_decay_per_s=gamma,pair_probability_at_pi_time=float(pop[1]),vacuum_probability=float(pop[0]),single_carrier_probability=float(pop[2]+pop[3]),stationary_pair_probability=predicted))
# Orthogonal projection check: retain up to N carriers of EACH sign.
def full_fock(N):
    omega=baseomega*1e-4;gamma=4*math.pi*.001;t=math.pi/(2*omega)
    d=N+1;D=d*d;ident=np.eye(d);I=np.eye(D)
    lower=np.diag(np.sqrt(np.arange(1,d)),1)
    a=np.kron(lower,ident);b=np.kron(ident,lower)
    na=np.repeat(np.arange(d),d);nb=np.tile(np.arange(d),d)
    hb=6.582119569e-16
    J=(p0['virtual_mediator_self_energy_eV']+p0['pair_contact_shift_eV'])/hb
    K=p0['pair_contact_shift_eV']/(6*hb)
    H=np.diag(J*(na*nb-(na+nb)/2)+K*(na*(na-1)+nb*(nb-1)))+omega*(a.T@b.T+a@b)
    L=-1j*(np.kron(I,H)-np.kron(H.T,I))
    for c in [a/math.sqrt(tau),b/math.sqrt(tau),np.diag(na+nb)*math.sqrt(gamma/2)]:
        number=c.T@c
        L+=np.kron(c,c)-.5*np.kron(I,number)-.5*np.kron(number.T,I)
    state=np.zeros(D*D,complex);state[0]=1
    rho=(expm(L*t)@state).reshape((D,D),order='F')
    ck('full_Fock_trace',abs(np.trace(rho)-1),2e-8)
    ck('full_Fock_positivity',max(0.,-float(np.linalg.eigvalsh((rho+rho.conj().T)/2).min())),1e-9)
    return float(rho[d+1,d+1].real)
p0=p['preparation'];f2=full_fock(2);f3=full_fock(3)
reference=next(r['pair_probability_at_pi_time'] for r in rows if r['intensity_per_wave_W_m2']==1e8 and r['common_laser_Lorentzian_FWHM_Hz']==.001)
ck('Fock_cutoff_refinement',abs(f2-f3),2e-7)
ck('four_state_projection_vs_Fock',abs(f3-reference),2e-7)
result=dict(scope='Four-state strong-blockade projection, rectangular pulse, inherited 10mm tunneling only, assigned common-laser phase diffusion; no re-solved thick-shell optics',single_particle_lifetime_s=tau,Fock_validation=dict(N2_pair_probability=f2,N3_pair_probability=f3,four_state_probability=reference),rows=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
