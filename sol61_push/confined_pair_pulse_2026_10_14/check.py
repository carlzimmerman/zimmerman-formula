import json,math,sys
from pathlib import Path
import numpy as np
from scipy import sparse as sp
from scipy.integrate import solve_ivp,quad
prior=json.loads(Path('sol61_push/silica_shell_retention_2026_10_14/run/results.json').read_text())
p=prior['preparation']; hb=6.582119569e-16
omega=p['pair_drive_angular_frequency_per_s']; J=(p['virtual_mediator_self_energy_eV']+p['pair_contact_shift_eV'])/hb
K=p['pair_contact_shift_eV']/(6*hb)
tau=prior['resonances'][1]['single_particle_tunneling_lifetime_s']; ramp=.005
T=math.pi/(2*omega)+ramp
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
def envelope(t,T=T,ramp=ramp):
    if t<=0 or t>=T:return 0.
    if ramp==0:return 1.
    if t<ramp:return .5*(1-math.cos(math.pi*t/ramp))
    if t>T-ramp:return .5*(1-math.cos(math.pi*(T-t)/ramp))
    return 1.
ck('pulse_area',abs(quad(envelope,0,T,points=[ramp,T-ramp],epsabs=1e-12)[0]*omega-math.pi/2),1e-12)
def evolve(N,tau=tau,J=J,K=K,omega=omega,T=T,ramp=ramp,detuning=0.,tol=2e-9):
    d=N+1; D=d*d; ident=sp.eye(d,format='csr'); I=sp.eye(D,format='csr')
    lower=sp.diags(np.sqrt(np.arange(1,d)),1,format='csr')
    aa=sp.kron(lower,ident,format='csr'); bb=sp.kron(ident,lower,format='csr')
    na=np.repeat(np.arange(d),d); nb=np.tile(np.arange(d),d)
    diag=J*(na*nb-(na+nb)/2)+K*(na*(na-1)+nb*(nb-1))-detuning*(na+nb)/2
    H=sp.diags(diag,format='csr'); drive=omega*(aa.T@bb.T+aa@bb)
    L0=-1j*(sp.kron(I,H,format='csr')-sp.kron(H.T,I,format='csr'))
    L1=-1j*(sp.kron(I,drive,format='csr')-sp.kron(drive.T,I,format='csr'))
    if math.isfinite(tau):
        for op in [aa,bb]:
            number=op.T@op
            L0+=(sp.kron(op,op,format='csr')-.5*sp.kron(I,number,format='csr')-.5*sp.kron(number.T,I,format='csr'))/tau
    initial=np.zeros(D*D,complex);initial[0]=1
    sol=solve_ivp(lambda t,y:L0@y+envelope(t,T,ramp)*(L1@y),(0,T),initial,method='DOP853',rtol=tol,atol=tol*1e-3,t_eval=np.linspace(0,T,61),max_step=T/60)
    assert sol.success
    worst_trace=worst_herm=negative=0.
    for column in sol.y.T[::5]:
        rho=column.reshape((D,D),order='F')
        worst_trace=max(worst_trace,abs(np.trace(rho)-1));worst_herm=max(worst_herm,float(np.max(abs(rho-rho.conj().T))))
        negative=max(negative,max(0.,-float(np.linalg.eigvalsh((rho+rho.conj().T)/2).min())))
    ck('trace',worst_trace,1e-9);ck('Hermiticity',worst_herm,1e-9);ck('positivity_sampled',negative,3e-8)
    rho=sol.y[:,-1].reshape((D,D),order='F');pop=np.real(np.diag(rho)).reshape(d,d)
    ck('charge_mean_symmetry',abs(float(np.sum(pop*(na-nb).reshape(d,d)))),1e-9)
    return dict(cutoff_per_sign=N,pair_11=float(pop[1,1]),vacuum=float(pop[0,0]),
        imbalance=float(sum(pop[i,j] for i in range(d) for j in range(d) if i!=j)),
        higher_balanced_pairs=float(sum(pop[i,i] for i in range(2,d))),
        mean_particles=float(np.sum(pop*(na+nb).reshape(d,d))),
        cutoff_boundary_population=float(np.sum(pop[-1,:])+np.sum(pop[:,-1])-pop[-1,-1]),populations=pop.tolist())
# Genuine external controls for the reduced model: two-level rotation and squeezing.
c=evolve(1,tau=math.inf,J=0,K=0)
ck('two_level_pi_pulse',abs(c['pair_11']-1),2e-8)
squeeze=evolve(6,tau=math.inf,J=0,K=0,T=.3/omega,ramp=0)
q=math.tanh(.3)**2
ck('two_mode_squeezed_distribution',max(abs(squeeze['populations'][i][i]-(1-q)*q**i) for i in range(6)),2e-6)
base=evolve(3);fine=evolve(5);tight=evolve(5,tol=2e-10)
ck('Fock_cutoff_refinement',abs(base['pair_11']-fine['pair_11']),2e-6)
ck('time_tolerance_refinement',abs(fine['pair_11']-tight['pair_11']),2e-7)
assert tight['cutoff_boundary_population']<1e-7
lossless=evolve(5,tau=math.inf)
# Sensitivity of isolated-pair preparation to the assumed nonlinear interaction.
interaction_sensitivity=[dict(J_scale=scale, result=evolve(5,J=J*scale)) for scale in [.5,2.]]
q_full=math.tanh(math.pi/2)**2
noninteracting_exact=dict(pair_11=(1-q_full)*q_full, mean_particles=2*math.sinh(math.pi/2)**2, maximum_single_pair_probability=.25)
# Bound direct free-mediator excitation by the pulse's high-frequency Fourier tail.
# ||f'''|| as a measure (including second-derivative jumps) <=4 pi^2/ramp^2.
hc=1.973269804e-7;cSI=299792458.;ej=1.602176634e-19
an=.02/hc; Lt=.001/hc; F0=1e-20*(1e12/cSI)/(ej/hc**3)/2
normF2=F0*F0*4*math.pi*an*Lt*Lt*quad(lambda x:x*math.exp(-x*x)*math.sqrt(max(0.,1-(Lt*x/an)**2)),0,an/Lt,epsabs=1e-12)[0]
gap_frequency=p['below_mediator_gap_eV']/hb
fourier_bound=4*math.pi**2/(ramp*ramp*gap_frequency**3)
real_R_bound=normF2/(hb*hb)*fourier_bound**2
result=dict(assumed_effective_model='Two fixed carrier orbitals, instantaneous second-order mediator elimination, independent shell leakage',
    pulse_duration_s=T,ramp_s=ramp,peak_drive_per_s=omega,J_per_s=J,K_same_sign_per_s=K,
    single_particle_tunneling_lifetime_s=tau,finite_loss=tight,lossless=lossless,
    interaction_sensitivity=interaction_sensitivity, noninteracting_lossless_exact=noninteracting_exact,
    elimination_scale_diagnostics=dict(memory_time_s=1/gap_frequency, memory_to_ramp=1/(gap_frequency*ramp), single_pair_shift_to_gap=abs(J)/gap_frequency, maximum_cutoff_interaction_scale_to_gap=25*abs(J)/gap_frequency),
    direct_free_mediator_pulse_excitation_upper_bound=real_R_bound,
    direct_source_norm_eV2=normF2,Fourier_tail_bound_s=fourier_bound,
    checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
