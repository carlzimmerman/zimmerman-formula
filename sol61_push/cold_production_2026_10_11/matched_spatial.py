"""3D classical two-channel envelope pilot; declared seed, no quantum yield."""
import json,math,itertools
from pathlib import Path
import numpy as np
p=Path(__file__).parent
u=.001;eps=1e-7;R=2*math.sqrt(1+u*u);dq=.4;kappa=.2000001
handoff=json.loads((p/'quantum_handoff_run_v2/results.json').read_text())
checks=[];rows=[]
def run(N,dt,handoff_index=1,seed=471901):
    state=handoff['states'][handoff_index];x_start=state['x'];end=100-x_start
    dt=end/math.ceil(end/dt)
    F=np.array(state['F']);C=np.array(state['C_real'])+1j*np.array(state['C_imag'])
    w=handoff['parameters']['pair_weight'];sv=(F+w/2)/2;mag=np.sqrt(F*(F+w))/2
    large=(sv+mag)/2;small=(w/4)**2/(2*(sv+mag))
    rng=np.random.default_rng(seed)
    z1=(rng.normal(size=len(F))+1j*rng.normal(size=len(F)))/math.sqrt(2)
    z2=(rng.normal(size=len(F))+1j*rng.normal(size=len(F)))/math.sqrt(2)
    left=np.sqrt(large)*z1+np.sqrt(small)*z2
    right=np.exp(1j*np.angle(C))*(np.sqrt(large)*z1.conjugate()-np.sqrt(small)*z2.conjugate())
    seed_modes={}
    for idx,l,r in zip(handoff['pairs'],left,right):
        seed_modes[tuple(idx)]=l;seed_modes[tuple(-i for i in idx)]=r
    initial_charge=sum(abs(v)**2 for v in seed_modes.values())
    B_gaussian=complex(*state['B'])
    B_initial=B_gaussian/abs(B_gaussian)*math.sqrt(1-initial_charge)

    kval=np.fft.fftfreq(N)*N*dq
    q2=kval[:,None,None]**2+kval[None,:,None]**2+kval[None,None,:]**2
    La=(u*u*q2-u*u)/(eps*(np.sqrt(1+u*u*q2)+math.sqrt(1+u*u)))
    Lb=u*u*q2/(eps*(np.sqrt(R*R+u*u*q2)+R))
    Ah=np.zeros((N,N,N),complex)
    for idx,value in seed_modes.items():Ah[tuple(i%N for i in idx)]=value
    A=np.fft.ifftn(Ah,norm='forward');B=np.full_like(A,B_initial)
    phasea=np.exp(-.5j*dt*La);phaseb=np.exp(-.5j*dt*Lb)
    def nonlinear(A,B):return -1j*(B*A.conjugate()+kappa*abs(A)**2*A),-1j*A*A
    def diagnostics(t):
        ah=np.fft.fftn(A,norm='forward');bh=np.fft.fftn(B,norm='forward')
        F=float(np.mean(abs(A)**2));source=float(np.mean(abs(B)**2))
        moving=source-abs(np.mean(B))**2
        energy=float(2*np.sum(La*abs(ah)**2)+np.sum(Lb*abs(bh)**2)+2*np.real(np.mean(B.conjugate()*A*A))+kappa*np.mean(abs(A)**4))
        # UV population screen; not proof of cutoff independence.
        edge=q2>(dq*N/3)**2
        tail=float(np.sum(abs(ah[edge])**2)+np.sum(abs(bh[edge])**2))
        return dict(x=t+x_start,daughter_fraction=F,source_fraction=source,moving_source_fraction=float(moving),charge=F+source,energy=energy,outer_mode_charge=tail)
    snapshots=[diagnostics(0)];steps=round(end/dt)
    for i in range(steps):
        A=np.fft.ifftn(np.fft.fftn(A,norm='forward')*phasea,norm='forward');B=np.fft.ifftn(np.fft.fftn(B,norm='forward')*phaseb,norm='forward')
        a1,b1=nonlinear(A,B);a2,b2=nonlinear(A+dt*a1/2,B+dt*b1/2)
        a3,b3=nonlinear(A+dt*a2/2,B+dt*b2/2);a4,b4=nonlinear(A+dt*a3,B+dt*b3)
        A=A+dt/6*(a1+2*a2+2*a3+a4);B=B+dt/6*(b1+2*b2+2*b3+b4)
        A=np.fft.ifftn(np.fft.fftn(A,norm='forward')*phasea,norm='forward');B=np.fft.ifftn(np.fft.fftn(B,norm='forward')*phaseb,norm='forward')
        if (i+1)%round(.5/dt)==0 or i+1==steps:snapshots.append(diagnostics((i+1)*dt))
    chargeerr=max(abs(r['charge']-1) for r in snapshots)
    energyerr=max(abs(r['energy']-snapshots[0]['energy']) for r in snapshots)
    checks.append(dict(name=f'N{N} dt{dt} charge',passed=chargeerr<1e-4,value=chargeerr))
    checks.append(dict(name=f'N{N} dt{dt} energy diagnostic',passed=energyerr<.01,value=energyerr))
    row=dict(N=N,dt=dt,handoff_target=state['target'],sample_seed=seed,initial_sampled_charge=initial_charge,source_amplitude_adjustment=abs(B_initial-B_gaussian),charge_error=chargeerr,energy_error=energyerr,final=snapshots[-1],snapshots=snapshots)
    print(json.dumps({k:v for k,v in row.items() if k!='snapshots'}),flush=True)
    return row
rows=[run(24,.005,handoff_index=0),run(24,.005,handoff_index=1)]
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),parameters=dict(u=u,epsilon=eps,dq=dq,kappa=kappa,handoff_targets=[1e-5,1e-4],seed=471901),non_claims=['Gaussian-to-classical prescription, not controlled full quantum evolution','Finite periodic box and spectral cutoff','No expansion or gravity','No converged continuum yield claim without grid evidence'])
(p/'matched_spatial_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),out['all_pass'],flush=True)
