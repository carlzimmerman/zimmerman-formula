"""3D classical two-channel envelope pilot; declared seed, no quantum yield."""
import json,math,itertools
from pathlib import Path
import numpy as np
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
portal=json.loads((p/'nonlinear_portal_run/results.json').read_text())['softened']
m=params['m_eV'];A0=params['source_amplitude_eV'];g=params['cubic_g_eV']
Astar=portal['Astar_eV2'];S0=portal['S0_eV2'];mbar=math.sqrt(m*m+Astar)
u=params['u']*m/mbar;eps=g*A0/(mbar*mbar);R=2*math.sqrt(1+u*u)
dq=.4;kappa=2*R*params['lambda_']*A0/g
density_ratio=4*A0*A0/S0;d=1/density_ratio;K=Astar/(2*mbar*mbar*eps)

rng=np.random.default_rng(471901)
seed_modes={}
for idx in itertools.product(range(-5,6),repeat=3):
    if 0<sum((dq*j)**2 for j in idx)<=4:
        seed_modes[idx]=rng.normal()+1j*rng.normal()
scale=math.sqrt(1e-8/sum(abs(v)**2 for v in seed_modes.values()))
seed_modes={k:v*scale for k,v in seed_modes.items()}
checks=[];rows=[]
def run(N,dt,end=30.,enabled=True):
    min_local_charge=math.inf;max_residual=0.
    kval=np.fft.fftfreq(N)*N*dq
    q2=kval[:,None,None]**2+kval[None,:,None]**2+kval[None,None,:]**2
    La=(u*u*q2-u*u)/(eps*(np.sqrt(1+u*u*q2)+math.sqrt(1+u*u)))
    Lb=u*u*q2/(eps*(np.sqrt(R*R+u*u*q2)+R))
    Ah=np.zeros((N,N,N),complex)
    for idx,value in seed_modes.items():Ah[tuple(i%N for i in idx)]=value
    A=np.fft.ifftn(Ah,norm='forward');B=np.full_like(A,math.sqrt(1-1e-8))
    phasea=np.exp(-.5j*dt*La);phaseb=np.exp(-.5j*dt*Lb)
    def residual(n):
        return -K*d*d/(np.hypot(n,d)*(np.hypot(n,d)+n))
    def nonlinear(A,B):
        nonlocal min_local_charge,max_residual
        n=abs(A)**2+abs(B)**2
        delta=residual(n) if enabled else np.zeros_like(n)
        min_local_charge=min(min_local_charge,float(np.min(n)))
        max_residual=max(max_residual,float(np.max(abs(delta))))
        return -1j*(B*A.conjugate()+kappa*abs(A)**2*A+delta*A),-1j*(A*A+2*delta*B)
    def diagnostics(t):
        ah=np.fft.fftn(A,norm='forward');bh=np.fft.fftn(B,norm='forward')
        F=float(np.mean(abs(A)**2));source=float(np.mean(abs(B)**2))
        moving=source-abs(np.mean(B))**2
        energy=float(2*np.sum(La*abs(ah)**2)+np.sum(Lb*abs(bh)**2)+2*np.real(np.mean(B.conjugate()*A*A))+kappa*np.mean(abs(A)**4))
        if enabled:
            n=abs(A)**2+abs(B)**2
            energy+=float(2*K*np.mean(d*d/(np.hypot(n,d)+n)))
        # UV population screen; not proof of cutoff independence.
        edge=q2>(dq*N/3)**2
        tail=float(np.sum(abs(ah[edge])**2)+np.sum(abs(bh[edge])**2))
        return dict(x=t,daughter_fraction=F,source_fraction=source,moving_source_fraction=float(moving),charge=F+source,energy=energy,outer_mode_charge=tail)
    snapshots=[diagnostics(0)];steps=round(end/dt)
    for i in range(steps):
        A=np.fft.ifftn(np.fft.fftn(A,norm='forward')*phasea,norm='forward');B=np.fft.ifftn(np.fft.fftn(B,norm='forward')*phaseb,norm='forward')
        a1,b1=nonlinear(A,B);a2,b2=nonlinear(A+dt*a1/2,B+dt*b1/2)
        a3,b3=nonlinear(A+dt*a2/2,B+dt*b2/2);a4,b4=nonlinear(A+dt*a3,B+dt*b3)
        A=A+dt/6*(a1+2*a2+2*a3+a4);B=B+dt/6*(b1+2*b2+2*b3+b4)
        A=np.fft.ifftn(np.fft.fftn(A,norm='forward')*phasea,norm='forward');B=np.fft.ifftn(np.fft.fftn(B,norm='forward')*phaseb,norm='forward')
        if (i+1)%round(.5/dt)==0:snapshots.append(diagnostics((i+1)*dt))
    chargeerr=max(abs(r['charge']-1) for r in snapshots)
    energyerr=max(abs(r['energy']-snapshots[0]['energy']) for r in snapshots)
    checks.append(dict(name=f'N{N} dt{dt} charge',passed=chargeerr<1e-4,value=chargeerr))
    checks.append(dict(name=f'N{N} dt{dt} energy diagnostic',passed=energyerr<.01,value=energyerr))
    row=dict(N=N,dt=dt,portal_enabled=enabled,min_stage_charge_density=min_local_charge,max_residual_phase_rate=max_residual,charge_error=chargeerr,energy_error=energyerr,final=snapshots[-1],snapshots=snapshots)
    print(json.dumps({k:v for k,v in row.items() if k!='snapshots'}),flush=True)
    return row
rows=[run(24,.01),run(24,.005),run(24,.005,enabled=False)]
checks.append(dict(name='time refinement daughter fraction',passed=abs(rows[0]['final']['daughter_fraction']-rows[1]['final']['daughter_fraction'])<1e-4))
difference=max(abs(a['daughter_fraction']-b['daughter_fraction']) for a,b in zip(rows[1]['snapshots'],rows[2]['snapshots']))
checks.append(dict(name='physical residual versus matched linear-mass control',passed=difference<1e-10,value=difference))
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),parameters=dict(mbar_eV=mbar,source_S_over_S0=density_ratio,residual_strength_K=K,u=u,epsilon=eps,dq=dq,kappa=kappa,initial_daughter_charge=1e-8,seed=471901,seed_mode_count=len(seed_modes)),non_claims=['Classical seeded leading-NR nonlinear-portal pilot, not vacuum production','Common linear portal mass shift absorbed into mbar and Mbar; residual retained at leading NR order','No full relativistic error bound or late low-density crossover evolution','Finite periodic box and spectral cutoff','No expansion or gravity','No converged continuum yield claim without grid evidence'])
(p/'portal_production_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),out['all_pass'],flush=True)
