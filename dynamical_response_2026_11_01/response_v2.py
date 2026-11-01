"""Hamiltonian shell response. No computation is executed on import."""
import json,sys,time
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from numpy.polynomial.legendre import leggauss,legvander,legder,legval
from scipy.linalg import eigh,block_diag,solve_triangular
from scipy.integrate import solve_ivp,simpson

def pulse_integral(lam,t,omega,T):
    """Solution of i xdot=lam*x+sin²(pi*t/T)*exp(-i omega*t), x(0)=0."""
    lam=np.asarray(lam)[:,None];t=np.asarray(t)[None,:]
    tt=np.minimum(t,T);out=np.zeros(np.broadcast_shapes(lam.shape,t.shape),complex)
    for c,w in ((.5,omega),(-.25,omega-2*np.pi/T),(-.25,omega+2*np.pi/T)):
        d=lam-w
        # sinc expression is analytic at every exact resonance.
        v=-1j*tt*np.exp(-1j*(lam+w)*tt/2)*np.sinc(d*tt/(2*np.pi))
        out+=c*v
    return out*np.exp(-1j*lam*np.maximum(t-T,0.))

def finite_hamiltonian(V,signs):
    """Low-rank exact square root of H=I+V†diag(signs)V."""
    gram=V@V.conj().T
    ev,vec=eigh(gram);keep=ev>max(ev[-1]*1e-13,1e-24)
    if not np.any(keep):
        return SimpleNamespace(sqrt=lambda x:x.copy(),invsqrt=lambda x:x.copy(),
                               minimum=1.,maximum=1.,rank=0,gram_eigenvalues=np.array([]))
    ev=ev[keep];vec=vec[:,keep]
    Q=V.conj().T@(vec/np.sqrt(ev)[None,:])
    low=np.eye(len(ev))+(np.sqrt(ev)[:,None]*(vec.conj().T@(signs[:,None]*vec)))*np.sqrt(ev)[None,:]
    hs,hu=eigh(low);U=Q@hu
    minimum=float(min(1.,hs[0]))
    if minimum<=0:raise ValueError('Finite Hamiltonian indefinite: '+str(minimum))
    def apply(x,power):
        return x+U@((hs**power-1)* (U.conj().T@x)) if x.ndim==1 else x+U@((hs**power-1)[:,None]*(U.conj().T@x))
    return SimpleNamespace(sqrt=lambda x:apply(x,.5),invsqrt=lambda x:apply(x,-.5),minimum=minimum,
                           maximum=float(max(1.,hs[-1])),rank=len(hs),gram_eigenvalues=ev)

def krylov(matvec,b,count):
    """Hermitian Lanczos with two-pass full reorthogonalization."""
    size=len(b);count=min(count,size);Q=np.zeros((size,count),complex)
    alpha=[];beta=[];q=b/np.linalg.norm(b);prev=np.zeros(size,complex);bp=0.
    for j in range(count):
        Q[:,j]=q;v=matvec(q)-bp*prev;a=float(np.vdot(q,v).real);v-=a*q
        for repeat in range(2):v-=Q[:,:j+1]@(Q[:,:j+1].conj().T@v)
        bn=float(np.linalg.norm(v));alpha.append(a)
        if j==count-1 or bn<1e-13:break
        beta.append(bn);prev=q;q=v/bn;bp=bn
    Q=Q[:,:len(alpha)];T=np.diag(alpha)
    if beta:T+=np.diag(beta,1)+np.diag(beta,-1)
    orth=float(np.max(np.abs(Q.conj().T@Q-np.eye(Q.shape[1]))))
    return Q,T,dict(last_residual=bn,orthogonality=orth,count=len(alpha))

def radial_basis(r,R,count):
    x=np.asarray(r)/R;z=2*x*x-1
    P=legvander(z,count-1).T;dP=[]
    for j in range(count):
        c=np.zeros(j+1);c[j]=1
        dP.append(legval(z,legder(c)) if j else np.zeros_like(x))
    dP=np.asarray(dP)
    u=x*x*P;du=(2*x*P+4*x**3*dP)/R
    Wr=np.vstack((2*x,np.asarray(x**3*P),np.zeros_like(P)))
    Wt=np.vstack((x,np.zeros_like(P),np.asarray(x**3*P)))
    return u,du,Wr,Wt

def force_profile(r,a):
    x=np.asarray(r)/a
    maximum=(2/3)/(1+2/3)**2.5
    return x*x/(1+x*x)**2.5/maximum

def matrices(bg,count,nquad=600):
    x,w=leggauss(nquad);r=(x+1)*bg.R/2;w=w*bg.R/2
    val=bg.values(r);p=val['psi'];s=val['s'];n=val['n'];a=np.exp(-2*s)
    u,du,wr,wt=radial_basis(r,bg.R,count)
    def gram(v,z,weight):return (v*weight)@z.T
    G=gram(du,du,w*r*r)+6*gram(u,u,w)+3*bg.R*np.ones((count,count))
    kap=1.2*bg.eps;c=3.6*np.exp(3*s)+2.4*n*p
    k=np.sqrt(3/bg.eps);L=bg.outer
    beta=k+3/L-k*(2*k*L+3)/((k*L)**2+3*k*L+3)
    # Riccati propagation of the logarithmic derivative avoids growing-tail overflow.
    def rhs(rr,y):
        ss=float(bg.values(rr)['s'])
        return [6/rr**2+3*np.exp(3*ss)/bg.eps-2*y[0]/rr-y[0]**2]
    tail=solve_ivp(rhs,(L,bg.R),[-beta],rtol=2e-10,atol=1e-12)
    if not tail.success:raise RuntimeError('scalar tail Riccati failed')
    tail_stiffness=-kap*bg.R**2*tail.y[0,-1]
    A=kap*(gram(du,du,w*r*r)+6*gram(u,u,w))+gram(u,u,w*r*r*c)+tail_stiffness*np.ones((count,count))
    # 1/gamma=n/(1-exp(-2s)); use expm1 to retain small positive s.
    invgamma=n/(-np.expm1(-2*s))
    C=gram(wr,wr,w*r*r*invgamma)+6*gram(wt,wt,w*r*r*invgamma)
    Ch=[np.linalg.cholesky(M) for M in (G,A,C)]
    force=force_profile(r,.3*bg.original_radius)
    scalar=np.vstack((u,2*p*u,force[None,:]))
    S=1.5*n/p
    dd=gram(scalar,scalar,w*r*r*S)
    cc=gram(wr,wr,w*r*r*n/a)+6*gram(wt,wt,w*r*r*n/a)
    # Feature ordering: gravity, scalar, current, forcing.
    direct=np.zeros((4*count+2,4*count+2))
    indices=list(range(2*count))+[4*count+1]
    direct[np.ix_(indices,indices)]=dd
    direct[2*count:4*count+1,2*count:4*count+1]=cc
    return Ch,direct,dict(scalar_tail_stiffness=float(tail_stiffness),scalar_tail_beta=float(-tail.y[0,-1]),
                           gram_condition_numbers=[float(np.linalg.cond(M)) for M in (G,A,C)])

def assemble(bg,nL,nphase,nharm,nbasis):
    from orbits import OrbitFamily
    family=OrbitFamily(bg)
    xl,wl=leggauss(nL);Ls=(xl+1)*family.Lmax/2;dL=wl*family.Lmax/2
    Ch,direct,diag=matrices(bg,nbasis)
    features=[];freqs=[];core=[];diagnostics=[];measure=0.
    fstar=3/(4*np.pi*2**1.5)
    ns=np.arange(-nharm,nharm+1);indices=ns%nphase
    for L,weight in zip(Ls,dL):
        o=family.orbit(float(L),nphase=nphase)
        r=o['r'];pr=o['pr'];pt=o['pphi'];theta=o['dphi']
        Or=o['Omega_r'];Op=o['Omega_phi']
        mw=(2*np.pi)**3*fstar*2*L*weight/Or
        measure+=mw;sw=np.sqrt(mw/5)
        u,du,wr,wt=radial_basis(r,bg.R,nbasis);psi=bg.values(r)['psi']
        U=force_profile(r,.3*bg.original_radius)
        for k in (-2,0,2):
            Y=(-np.sqrt(5/(16*np.pi)) if k==0 else np.sqrt(15/(32*np.pi)))
            ang=Y*np.exp(1j*k*theta)
            B=np.vstack((u,2*psi*u,pr*wr+1j*k*pt*wt,U[None,:]))*ang
            coeff=np.fft.fft(B,axis=1)[:,indices]/nphase
            corecoeff=np.fft.fft(U*(r<bg.core_radius)*ang)[indices]/nphase
            features.append(sw*coeff.conj());core.append(sw*corecoeff)
            freqs.append(ns*Or+k*Op)
        diagnostics.append({key:float(o[key]) for key in ('L','r_pericenter','r_apocenter','Omega_r','Omega_phi','invariant_residual','dense_period_relative_error','dense_angle_relative_error')})
    B=np.concatenate(features,axis=1);omega=np.concatenate(freqs);bcore=np.concatenate(core)
    spectral=B@B.conj().T
    scale=np.sqrt(np.maximum(np.diag(direct),1e-30))
    gramerr=float(np.max(np.abs(spectral-direct)/np.outer(scale,scale)))
    x,w=leggauss(800);r=(x+1)*bg.R/2;w*=bg.R/2;st=bg.values(r)
    shell_direct=float(4*np.pi*np.sum(w*r*r*1.5*st['n']/st['psi']))
    active=np.abs(omega)>1e-12*bg.omega_dyn
    frozen_norm=float(np.linalg.norm(B[:,~active]))
    raw=B[:,active];om=omega[active]
    V=np.vstack((solve_triangular(Ch[0],raw[:nbasis],lower=True),
                 solve_triangular(Ch[1],raw[nbasis:2*nbasis],lower=True),
                 solve_triangular(Ch[2],raw[2*nbasis:4*nbasis+1],lower=True)))
    signs=np.r_[-np.ones(2*nbasis),np.ones(2*nbasis+1)]
    b=raw[-1].conj()
    diag.update(shell_measure=measure,shell_direct=shell_direct,shell_measure_relative_error=abs(measure/shell_direct-1),
                gram_max_scaled_error=gramerr,active_modes=int(active.sum()),frozen_zero_modes=int((~active).sum()),
                frozen_basis_norm=frozen_norm,orbit_diagnostics=diagnostics)
    return V,signs,om,b,bcore[active],diag

def solve_pulses(V,signs,om,b,bc,bg,nkrylov=256,nt=2049,duration=20.):
    H=finite_hamiltonian(V,signs)
    def matvec(x):return H.sqrt(om*H.sqrt(x))
    source=H.sqrt(om*b);norm=np.linalg.norm(source)
    Q,T,diag=krylov(matvec,source,nkrylov)
    ev,vec=eigh(T);modes=Q@vec;coeff=norm*vec[0,:].conj()
    observ=H.invsqrt(np.column_stack((b,bc))).conj().T@modes
    pulseT=duration/bg.omega_dyn;amp=.001*bg.original_psi
    tt=np.linspace(0,pulseT,nt);envelope=np.sin(np.pi*tt/pulseT)**2
    denvelope=np.pi/pulseT*np.sin(2*np.pi*tt/pulseT)
    rows=[];series={}
    for ratio in (.25,.5,1.,2.,4.):
        wp=ratio*bg.omega_dyn;wd=2*wp
        x=amp*coeff[:,None]*pulse_integral(ev,tt,wd,pulseT)
        obs=observ@x;F=amp*envelope*np.exp(-1j*wd*tt)
        Fe=amp*denvelope*np.exp(-1j*wd*tt);Fd=Fe-1j*wd*F
        power=.5*np.real(obs[0].conj()*Fd)
        torque=np.imag(obs[0].conj()*F) # m=2
        work=float(simpson(power,x=tt));lt=float(simpson(torque,x=tt))
        envwork=float(simpson(.5*np.real(obs[0].conj()*Fe),x=tt))
        corework=float(simpson(.5*np.real(obs[1].conj()*Fd),x=tt))
        xf=x[:,-1];zf=H.invsqrt(modes@xf)
        energy=float(.25*np.vdot(xf,xf).real)
        angular=float(.5*np.sum(abs(zf)**2/om).real)
        scale=max(energy,1e-30)
        late=np.linspace(pulseT,2*pulseT,1025)
        xlate=xf[:,None]*np.exp(-1j*ev[:,None]*(late-pulseT))
        olate=observ@xlate
        peak=float(np.max(abs(obs[0])))
        late_rms=float(np.sqrt(np.mean(abs(olate[0,-256:])**2)))
        residual=diag['last_residual']*abs(vec[-1]@x)/max(amp*norm,1e-30)
        rows.append(dict(pattern_ratio=ratio,forcing_omega=wd,pulse_duration=pulseT,amplitude=amp,
                         work=work,final_energy=energy,work_per_amplitude_squared=work/amp**2,
                         torque_integral=lt,canonical_angular_momentum=angular,envelope_work=envwork,
                         work_energy_relative_error=abs(work-energy)/scale,
                         torque_relative_error=abs(lt-angular)/max(abs(lt),abs(angular),1e-30),
                         jacobi_ledger_relative_error=abs(work-wp*lt-envwork)/max(abs(work),abs(wp*lt),abs(envwork),1e-30),
                         forcing_work_inside_material_core=corework,core_forcing_work_fraction=corework/work if work else None,
                         peak_quadrupole=peak,late_quadrupole_rms=late_rms,late_to_peak=late_rms/peak if peak else None,
                         source_normalized_ode_residual_max=float(np.max(residual))))
        series[str(ratio)]=np.vstack((tt,power,torque,obs[0].real,obs[0].imag,obs[1].real,obs[1].imag))
        series[str(ratio)+'_late']=np.vstack((late,olate[0].real,olate[0].imag))
    # Independent high-frequency sum rule: current feedback restores the
    # physical mass-current inertia. Bare scalar-metric transport has alpha*n.
    gx,gw=leggauss(800);rr=(gx+1)*bg.R/2;gw*=bg.R/2
    vals=bg.values(rr);aa=.3*bg.original_radius;xx=rr/aa
    umax=(2/3)/(1+2/3)**2.5
    U=force_profile(rr,aa);dU=xx*(2-3*xx*xx)/(aa*(1+xx*xx)**3.5*umax)
    radial=gw*vals['n']*(rr*rr*dU*dU+6*U*U)
    sumrule=dict(spectral=float(norm**2),full_continuum=float(np.sum(radial)),
                 bare_continuum=float(np.sum(radial*np.exp(-2*vals['s']))))
    return dict(hamiltonian_minimum=H.minimum,hamiltonian_maximum=H.maximum,hamiltonian_rank=H.rank,
                krylov=diag,high_frequency_sum_rule=sumrule,cases=rows),series

def main():
    from background import Background
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('output');ap.add_argument('--state',default='baseline',choices=['baseline','compact','diffuse'])
    ap.add_argument('--level',type=int,default=0);ap.add_argument('--krylov',type=int,default=256)
    ap.add_argument('--bare',action='store_true');ap.add_argument('--duration',type=float,default=20.)
    ap.add_argument('--nL',type=int);ap.add_argument('--nphase',type=int);ap.add_argument('--nharm',type=int);ap.add_argument('--nbasis',type=int)
    args=ap.parse_args()
    grids=[(16,256,12,6),(24,512,18,8),(40,1024,24,10)]
    start=time.time();bg=Background(args.state);params=list(grids[args.level])
    for i,key in enumerate(('nL','nphase','nharm','nbasis')):
        if getattr(args,key) is not None:params[i]=getattr(args,key)
    print('background',args.state,'R',bg.R,'omega_dyn',bg.omega_dyn,flush=True)
    V,signs,om,b,bc,diag=assemble(bg,*params)
    print('assembled',diag['active_modes'],'gram error',diag['gram_max_scaled_error'],flush=True)
    if args.bare:V=np.zeros_like(V)
    result,series=solve_pulses(V,signs,om,b,bc,bg,args.krylov,duration=args.duration)
    result.update(state=args.state,grid=params,approximation='fast_scalar_kinetic_shell',bare=args.bare,
                  background=dict(radius=bg.R,core_radius=bg.core_radius,omega_dyn=bg.omega_dyn,
                                  reconstruction_errors=bg.reconstruction_errors),assembly=diag,runtime_seconds=time.time()-start)
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    np.savez_compressed(out/'response_series.npz',**series)
    print(json.dumps({'state':args.state,'minimum':result['hamiltonian_minimum'],
                      'work':[r['work'] for r in result['cases']],
                      'energy_error':[r['work_energy_relative_error'] for r in result['cases']]}),flush=True)

if __name__=='__main__':main()
