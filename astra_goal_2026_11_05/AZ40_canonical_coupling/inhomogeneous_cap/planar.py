#!/usr/bin/env python3
"""Full plane-symmetric cap action: constrained, reflection-symmetric Hamiltonian."""
import os
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[name]='1'
import argparse,json,time,hashlib
from pathlib import Path
import numpy as np
import torch
from scipy.integrate import DOP853

torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.set_default_dtype(torch.float64)

class BranchError(RuntimeError):pass

class Model:
    def __init__(self,n=17,cap=True,amplitude=.15):
        assert n%2==1
        self.n=n;self.cap=cap;self.amplitude=amplitude;self.x=np.arange(n)*2*np.pi/n;self.dx=2*np.pi/n
        wave=np.fft.fftfreq(n,d=1/n)
        self.D=np.fft.ifft(1j*wave[:,None]*np.fft.fft(np.eye(n),axis=0),axis=0).real
        self.D2=self.D@self.D;ks=np.arange(1,(n+1)//2)
        self.S=np.sin(self.x[:,None]*ks);self.C=np.cos(self.x[:,None]*ks)
        self.Cdense=np.cos(np.arange(4*n)[:,None]*(2*np.pi/(4*n))*ks)
        self.Dt=torch.tensor(self.D);self.D2t=torch.tensor(self.D2)
        self.M=1.;self.K=.5;self.beta=2/3;self.xi=.5/(1+self.beta);self.G=1/(8*np.pi)
        self.Vstar=.01*np.sinh(1);self.gamma=.25;self.b=.1;self.T=1.
        self.calls=0;self.last=None
    def functions(self,phi):
        if np.min(phi)<=0:raise BranchError('scalar phi crossed its positive sinh domain')
        V=self.Vstar/np.sinh(phi);a=np.sqrt(self.xi*self.G*V)
        star=np.sqrt(6*V/(1+self.beta))/np.tanh(phi)
        return V,a,star
    def lam(self,rA,rB,star):
        if not self.cap:return np.zeros_like(rA)
        lam=-(rA+rB+2*star)/3
        for j in range(80):
            hyp=np.hypot(lam,self.b*self.T)
            res=(3*lam+rA+rB+2*star)/2+self.T*lam/hyp
            step=res/(1.5+self.T*(self.b*self.T)**2/hyp**3)
            lam-=step
            if max(abs(step))<1e-13*(1+max(abs(lam))):return lam
        raise BranchError('cap auxiliary solve did not converge')
    def background(self,state):
        A,B,phi,pa,pb,pphi=state[:6]
        if max(np.max(abs(A)),np.max(abs(B)))>100:raise BranchError('metric exponential exceeded numerical representation bound')
        vol=np.exp(A+2*B);V,a,star=self.functions(phi)
        rA=pa/vol;rB=pb/vol;lam=self.lam(rA,rB,star)
        ky=-(rA+lam)/2;kx=(rA-rB-lam)/2;theta=kx+2*ky
        U=self.T*lam*lam/(np.hypot(lam,self.b*self.T)+self.b*self.T) if self.cap else np.zeros(self.n)
        Ax=self.D@A;Bx=self.D@B;phix=self.D@phi
        R3=np.exp(-2*A)*(-4*(self.D2@B)-6*Bx*Bx+4*Ax*Bx)
        base=-2*kx*ky-ky*ky-lam*star-U-R3/2+pphi*pphi/(2*vol*vol)+.5*np.exp(-2*A)*phix*phix+V
        Dop=np.exp(-A)[:,None]*(self.D+np.diag(2*Bx))
        return dict(vol=vol,V=V,a=a,star=star,lam=lam,kx=kx,ky=ky,theta=theta,U=U,R3=R3,base=base,Dop=Dop)
    def polar(self,P,a):
        z=self.K*abs(P)/a
        if np.max(z)>=1 or not np.all(np.isfinite(z)):raise BranchError('polarization potential outside |K P|<a')
        f=-z-np.log1p(-z)
        small=z<.01
        f=np.where(small,sum(z**j/j for j in range(2,16)),f)
        return a*a/self.K*f,self.K*P/(1-z),z
    def auxiliary(self,state):
        bg=self.background(state);m=self.S.shape[1];p=np.zeros(m)
        # Start from the regular zero-polarization branch; do not clip a solution.
        for iteration in range(45):
            P=self.S@p;W,Wp,z=self.polar(P,bg['a']);dp=bg['Dop']@P;F=1+self.gamma*dp
            hd=bg['vol']*(bg['base']+W+self.gamma*dp*dp/2+dp)
            g=2/self.n*self.C.T@hd
            mat=bg['vol'][:,None]*(Wp[:,None]*self.S+F[:,None]*(bg['Dop']@self.S))
            jac=2/self.n*self.C.T@mat
            scale=1+max(abs(hd))+max(abs(bg['vol']*bg['base']))
            if max(abs(g))<2e-12*scale:break
            try:step=np.linalg.solve(jac,-g)
            except np.linalg.LinAlgError as exc:raise BranchError('polarization constraint Jacobian singular') from exc
            merit=np.linalg.norm(g)
            for ls in range(32):
                trial=p+step*(.5**ls)
                try:
                    Pt=self.S@trial;Wt,_,_=self.polar(Pt,bg['a']);dt=bg['Dop']@Pt
                    ht=bg['vol']*(bg['base']+Wt+self.gamma*dt*dt/2+dt)
                    gt=2/self.n*self.C.T@ht
                except BranchError:continue
                if np.linalg.norm(gt)<merit*(1-1e-4*.5**ls) or max(abs(gt))<2e-12*scale:
                    p=trial;break
            else:raise BranchError('polarization constraint line search stalled')
        else:raise BranchError('polarization constraint iterations exhausted')
        dh0=np.mean(mat,axis=0)
        try:ncoef=-2*np.linalg.solve(jac.T,dh0)
        except np.linalg.LinAlgError as exc:raise BranchError('lapse null-vector solve singular') from exc
        N=1+self.C@ncoef;Ndense=1+self.Cdense@ncoef
        if min(Ndense)<=0:raise BranchError('lapse lost positivity on resolved interpolation')
        pstat=np.max(abs(mat.T@N/self.n))/(1+max(abs(hd)))
        Cmom=state[3]*(self.D@state[0])+state[4]*(self.D@state[1])+state[5]*(self.D@state[2])-self.D@state[3]
        bg.update(P=P,N=N,N_dense_min=min(Ndense),Dp=dp,F=F,z=z,hd=hd,E=float(np.mean(hd)),pstat=float(pstat),Cmom=Cmom,jac_cond=float(np.linalg.cond(jac)),newton=iteration+1)
        return bg
    def hamiltonian(self,state,P,N,lam):
        A,B,phi,pa,pb,pphi=state
        vol=torch.exp(A+2*B);V=self.Vstar/torch.sinh(phi);a=torch.sqrt(self.xi*self.G*V)
        star=torch.sqrt(6*V/(1+self.beta))/torch.tanh(phi)
        rA=pa/vol;rB=pb/vol;ky=-(rA+lam)/2;kx=(rA-rB-lam)/2
        U=self.T*lam*lam/(torch.sqrt(lam*lam+(self.b*self.T)**2)+self.b*self.T) if self.cap else torch.zeros_like(lam)
        Ax=self.Dt@A;Bx=self.Dt@B;phix=self.Dt@phi
        R3=torch.exp(-2*A)*(-4*(self.D2t@B)-6*Bx*Bx+4*Ax*Bx)
        z=self.K*torch.abs(P)/a
        f=torch.where(z<.01,sum(z**j/j for j in range(2,16)),-z-torch.log1p(-z))
        W=a*a/self.K*f;dp=torch.exp(-A)*(self.Dt@P+2*Bx*P)
        hd=vol*(-2*kx*ky-ky*ky-lam*star-U-R3/2+pphi*pphi/(2*vol*vol)+.5*torch.exp(-2*A)*phix*phix+V+W+self.gamma*dp*dp/2+dp)
        return self.dx*torch.sum(N*hd)
    def rhs(self,t,flat):
        state=flat.reshape(7,self.n);bg=self.auxiliary(state);self.calls+=1
        st=torch.tensor(state[:6],requires_grad=True)
        ham=self.hamiltonian(st,torch.tensor(bg['P']),torch.tensor(bg['N']),torch.tensor(bg['lam']))
        grad=torch.autograd.grad(ham,st)[0].detach().numpy()/self.dx
        rhs=np.concatenate([grad[3:],-grad[:3],bg['N'][None,:]],axis=0)
        # Restriction to the stated exact reflection symmetry, up to roundoff.
        rhs=(rhs+rhs[:,(-np.arange(self.n))%self.n])/2
        self.last=(t,bg)
        return rhs.ravel()
    def initial(self):
        state=np.zeros((7,self.n));state[2]=1;state[3]=.35;state[4]=.7+self.amplitude*np.cos(self.x)
        bg=self.background(state)
        root=-2*bg['base']
        if min(root)<=0:raise BranchError('initial scalar momentum is not real')
        state[5]=bg['vol']*np.sqrt(root)
        return state
    def diagnostics(self,t,state):
        bg=self.auxiliary(state);v=bg['vol'];shear=(bg['kx']-bg['ky'])**2/3
        phix=self.D@state[2];kinphi=.5*((state[5]/v)**2-np.exp(-2*state[0])*phix**2)
        norm=1+max(abs(v*bg['base']))+max(abs(bg['hd']))
        return dict(t=float(t),E=bg['E'],H_res=float(max(abs(bg['hd']))/norm),M_res=float(max(abs(bg['Cmom']))/(1+max(abs(state[3]))+max(abs(state[4]))+max(abs(state[5])))),P_res=bg['pstat'],min_volume=float(min(v)),max_volume=float(max(v)),min_N=float(bg['N_dense_min']),max_N=float(max(bg['N'])),min_Q=float(1/max(bg['N'])),cap_gap=float(min(1-abs((bg['theta']-bg['star'])/self.T))) if self.cap else None,max_lambda=float(max(abs(bg['lam']))),max_shear=float(max(shear)),max_R3=float(max(abs(bg['R3']))),max_polarization_ratio=float(max(bg['z'])),min_polarization_factor=float(min(bg['F'])),min_phi=float(min(state[2])),min_scalar_X=float(min(kinphi)),max_proper_time=float(max(state[6])),min_proper_time=float(min(state[6])),max_aux_condition=bg['jac_cond'],max_theta=float(max(bg['theta'])),min_theta=float(min(bg['theta'])))

def check_model(model):
    state=model.initial();bg=model.auxiliary(state);rhs=model.rhs(0,state.ravel()).reshape(7,model.n)
    checks={}
    checks['initial_hamiltonian']=max(abs(bg['hd']))<1e-11
    checks['initial_momentum']=max(abs(bg['Cmom']))<1e-11
    checks['initial_polarization_and_lapse']=max(abs(bg['P']))<1e-11 and max(abs(bg['N']-1))<1e-11
    checks['canonical_metric_velocities']=max(abs(rhs[0]-bg['N']*bg['kx']))<1e-10 and max(abs(rhs[1]-bg['N']*bg['ky']))<1e-10
    checks['canonical_scalar_velocity']=max(abs(rhs[2]-bg['N']*state[5]/bg['vol']))<1e-10
    # Off-background Hamiltonian finite differences at fixed auxiliaries test
    # differentiation; reduced-energy differences test the constraint envelope.
    rng=np.random.default_rng(713);direction=rng.normal(size=(6,model.n));direction=(direction+direction[:,(-np.arange(model.n))%model.n])/2
    st=torch.tensor(state[:6],requires_grad=True);P=torch.tensor(bg['P']);N=torch.tensor(bg['N']);la=torch.tensor(bg['lam'])
    value=model.hamiltonian(st,P,N,la);grad=torch.autograd.grad(value,st)[0].detach().numpy()
    prediction=float(np.sum(grad*direction));errs=[];red_err=[]
    for h in [1e-5,5e-6]:
        plus=model.hamiltonian(torch.tensor(state[:6]+h*direction),P,N,la).item();minus=model.hamiltonian(torch.tensor(state[:6]-h*direction),P,N,la).item()
        errs.append(abs((plus-minus)/(2*h)-prediction)/(1+abs(prediction)))
        sp=state.copy();sm=state.copy();sp[:6]+=h*direction;sm[:6]-=h*direction
        ep=model.auxiliary(sp)['E']*2*np.pi;em=model.auxiliary(sm)['E']*2*np.pi
        red_err.append(abs((ep-em)/(2*h)-prediction)/(1+abs(prediction)))
    checks['automatic_gradient_finite_difference']=max(errs)<1e-7
    checks['reduced_constraint_envelope']=max(red_err)<1e-6
    hom=Model(model.n,model.cap,amplitude=0);hs=hom.initial();hr=hom.rhs(0,hs.ravel()).reshape(7,hom.n)
    checks['homogeneous_preservation']=max(np.ptp(hr,axis=1))<1e-10
    return dict(checks={k:bool(v) for k,v in checks.items()},finite_difference_errors=errs,reduced_envelope_errors=red_err,initial=model.diagnostics(0,state))

def evolve(model,args,out):
    start=time.monotonic();state=model.initial();times=[0.];states=[state.copy()];diags=[model.diagnostics(0,state)]
    rtol=args.rtol;atol=rtol/100;status='running';reason=None;accepted=0;retries=0;nextsave=.01
    solver=DOP853(model.rhs,0,state.ravel(),args.end,rtol=rtol,atol=atol)
    def save():
        result=dict(status=status,reason=reason,n=model.n,cap=model.cap,rtol=rtol,atol=atol,target=args.end,last_time=float(times[-1]),accepted_steps=accepted,RHS_calls=model.calls,retries=retries,wall_seconds=time.monotonic()-start,diagnostics=diags)
        tmp=out/'results.tmp';tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(out/'results.json')
        np.savez_compressed(out/'trajectory.npz',time=np.array(times),state=np.array(states),x=model.x)
    save()
    while solver.status=='running':
        if time.monotonic()-start>args.wall:status='wall_limit';reason='internal bounded-run wall limit';break
        before_t=solver.t;before_y=solver.y.copy();before_h=solver.h_abs
        try:
            solver.step()
            if solver.status=='failed':raise BranchError('DOP853 step failed')
            dense=solver.dense_output()
        except (BranchError,np.linalg.LinAlgError,FloatingPointError) as exc:
            retries+=1;step=min(before_h*.5,args.end-before_t)
            if retries>=14 or step<1e-8:
                status='unable_to_advance';reason=str(exc);break
            try:solver=DOP853(model.rhs,before_t,before_y,args.end,rtol=rtol,atol=atol,first_step=step,max_step=step)
            except BranchError as nested:status='accepted_state_auxiliary_failure';reason=str(nested);break
            continue
        accepted+=1
        try:
            while nextsave<=solver.t+1e-12:
                snapshot=dense(nextsave).reshape(7,model.n)
                dg=model.diagnostics(nextsave,snapshot)
                times.append(nextsave);states.append(snapshot.copy());diags.append(dg);nextsave=round(nextsave+.01,12)
            if accepted%20==0:save()
        except BranchError as exc:status='output_interpolation_failure';reason=str(exc);break
    if solver.status=='finished' and status=='running':status='completed'
    elif status=='running':status='integrator_stopped'
    if solver.t>times[-1]+1e-12:
        try:
            snapshot=solver.y.reshape(7,model.n);dg=model.diagnostics(solver.t,snapshot)
            times.append(solver.t);states.append(snapshot.copy());diags.append(dg)
        except BranchError:pass
    save()
    print(json.dumps({'status':status,'reason':reason,'n':model.n,'cap':model.cap,'last_time':times[-1],'accepted':accepted,'calls':model.calls,'last_diagnostics':diags[-1]},indent=2))
    return status=='completed'

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['check','evolve'],required=True);ap.add_argument('--n',type=int,default=17);ap.add_argument('--uncapped',action='store_true');ap.add_argument('--rtol',type=float,default=1e-7);ap.add_argument('--end',type=float,default=3.);ap.add_argument('--wall',type=float,default=110);ap.add_argument('--out',required=True);args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);m=Model(args.n,not args.uncapped)
    if args.mode=='check':
        r=check_model(m);(out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));ok=all(r['checks'].values())
    else:ok=evolve(m,args,out)
    raise SystemExit(int(not ok))
