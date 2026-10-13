"""3D classical two-channel envelope pilot; declared seed, no quantum yield."""
import json,math,itertools
from pathlib import Path
import numpy as np
p=Path(__file__).parent
u=.001;eps=1e-7;R=2*math.sqrt(1+u*u);dq=.4;kappa=.2000001
handoff=json.loads((p/'expanding_handoff_run/results.json').read_text())
h=handoff['parameters']['H_over_m_epsilon']
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
    Ah=np.zeros((N,N,N),complex)
    for idx,value in seed_modes.items():Ah[tuple(i%N for i in idx)]=value
    A=np.fft.ifftn(Ah,norm='forward');B=np.full_like(A,B_initial)
    Bh=np.fft.fftn(B,norm='forward')
    def coefficients(x):
        a=math.sqrt(1+2*h*x);wa=np.sqrt(1+u*u*q2/a**2);wb=np.sqrt(R*R+u*u*q2/a**2)
        la=(u*u*q2/a**2-u*u)/(eps*(wa+math.sqrt(1+u*u)))
        lb=u*u*q2/(eps*a**2*(wb+R))
        g=a**(-1.5);k=kappa*a**(-3)
        lap=-h*u*u*q2/(eps*a**4*wa);lbp=-h*u*u*q2/(eps*a**4*wb)
        gp=-1.5*h/a**2*g;kp=-3*h/a**2*k
        return a,la,lb,g,k,lap,lbp,gp,kp
    def diagnostics(x):
        a,la,lb,g,k,lap,lbp,gp,kp=coefficients(x)
        AA=abs(Ah)**2;BB=abs(Bh)**2
        F=float(np.sum(AA));source=float(np.sum(BB));moving=source-abs(Bh[0,0,0])**2
        interaction=float(np.real(np.mean(B.conjugate()*A*A)));quartic=float(np.mean(abs(A)**4))
        energy=float(2*np.sum(la*AA)+np.sum(lb*BB)+2*g*interaction+k*quartic)
        work_rate=float(2*np.sum(lap*AA)+np.sum(lbp*BB)+2*gp*interaction+kp*quartic)
        tail=float(np.sum(AA[q2>(dq*N/3)**2])+np.sum(BB[q2>(dq*N/3)**2]))
        return dict(x=x,a=a,daughter_fraction=F,source_fraction=source,moving_source_fraction=float(moving),charge=F+source,energy=energy,work_rate=work_rate,outer_mode_charge=tail)
    first=diagnostics(x_start);snapshots=[first];work=0.;previous_rate=first['work_rate'];max_work_error=0.;max_charge_error=abs(first['charge']-1)
    steps=round(end/dt)
    for i in range(steps):
        x=x_start+i*dt
        a,la,lb,g,k,*_=coefficients(x+dt/2)
        pa=np.exp(-.5j*dt*la);pb=np.exp(-.5j*dt*lb)
        A=np.fft.ifftn(Ah*pa,norm='forward');B=np.fft.ifftn(Bh*pb,norm='forward')
        def nonlinear(A,B):return -1j*(g*B*A.conjugate()+k*abs(A)**2*A),-1j*g*A*A
        a1,b1=nonlinear(A,B);a2,b2=nonlinear(A+dt*a1/2,B+dt*b1/2)
        a3,b3=nonlinear(A+dt*a2/2,B+dt*b2/2);a4,b4=nonlinear(A+dt*a3,B+dt*b3)
        A=A+dt/6*(a1+2*a2+2*a3+a4);B=B+dt/6*(b1+2*b2+2*b3+b4)
        Ah=np.fft.fftn(A,norm='forward')*pa;Bh=np.fft.fftn(B,norm='forward')*pb
        A=np.fft.ifftn(Ah,norm='forward');B=np.fft.ifftn(Bh,norm='forward')
        diag=diagnostics(x_start+(i+1)*dt)
        work+=dt/2*(previous_rate+diag['work_rate']);previous_rate=diag['work_rate']
        max_work_error=max(max_work_error,abs(diag['energy']-first['energy']-work))
        max_charge_error=max(max_charge_error,abs(diag['charge']-1))
        if (i+1)%round(.5/dt)==0 or i+1==steps:
            diag['integrated_work']=work;snapshots.append(diag)
    checks.append(dict(name=f'N{N} dt{dt} charge',passed=max_charge_error<1e-4,value=max_charge_error))
    checks.append(dict(name=f'N{N} dt{dt} expansion work',passed=max_work_error<.01,value=max_work_error))
    row=dict(N=N,dt=dt,handoff_target=state['target'],sample_seed=seed,initial_sampled_charge=initial_charge,source_amplitude_adjustment=abs(B_initial-B_gaussian),charge_error=max_charge_error,work_error=max_work_error,final=snapshots[-1],snapshots=snapshots)
    print(json.dumps({k:v for k,v in row.items() if k!='snapshots'}),flush=True)
    return row
rows=[run(24,.005,handoff_index=1),run(24,.0025,handoff_index=1)]
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),parameters=dict(u=u,epsilon=eps,dq=dq,kappa=kappa,h=h,handoff_targets=[1e-4],seed=471901),non_claims=['Gaussian to classical prescription, not a quantum error theorem','Finite periodic box and one realization','Imposed radiation expansion; no gravity or Friedmann feedback','No relic or halo prediction'])
(p/'expanding_spatial_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),out['all_pass'],flush=True)
