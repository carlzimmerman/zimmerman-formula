"""PF06b: constrained, unfiltered pre-break planar ADM experiment (on branch)."""
import argparse,json,time
from pathlib import Path
import numpy as np
from adm_initial_v2 import build


class System:
    def __init__(self,n,k):
        self.n=n;self.k=k;self.g=.1;self.s2=.01;self.V=.01;self.M=1.;self.K=.5;self.a0=.3
        modes=np.fft.fftfreq(n,1/n)
        self.D=np.fft.ifft(1j*modes[:,None]*np.fft.fft(np.eye(n),axis=0),axis=0).real
        self.Dx=k*self.D;self.Dxx=self.Dx@self.Dx;self.modes=modes
        self.P=np.zeros(n);self.max_res=0.;self.calls=0;self.newton=0

    def inverse_theta(self,q):
        f=np.fft.fft(q);den=1j*self.modes;den[0]=1;f=f/den;f[0]=0
        if self.n%2==0:f[self.n//2]=0
        return np.fft.ifft(f).real

    def unpack(self,y):
        n=self.n;return y[0],y[1:1+n],y[1+n:1+2*n],y[1+2*n:]

    def fields(self,y,P,jac=False):
        lam,b,pl,pb=self.unpack(y);vol=np.exp(lam+2*b);bx=self.Dx@b;bxx=self.Dxx@b
        hk=(pl*pl-2*pl*pb)/(4*self.M*vol)
        h=hk/vol+self.M*np.exp(-2*lam)*(2*bxx+3*bx*bx)
        op=np.exp(-lam)*(self.Dx+np.diag(2*bx));d=op@P
        cap=self.K*np.abs(P)/self.a0
        if np.max(cap)>=1:raise ValueError('flux cap')
        W=self.a0**2/self.K*(-cap-np.log1p(-cap));Wp=self.K*P/(1-cap);Wpp=self.K/(1-cap)**2
        den=1-2*self.g*d
        X=-(h+d+self.V+W+self.g*d*d/2)/den
        if np.min(X)<=0:raise ValueError('X nonpositive')
        N=np.sqrt(self.s2/(2*X));q=d+2*X
        if np.min(q)<=0:raise ValueError('switch reached')
        T=1+self.g*q
        R=np.exp(-lam)*(self.Dx@(N*T))-N*Wp
        J=None
        if jac:
            Xj=((-1-self.g*d+2*self.g*X)[:,None]*op-np.diag(Wp))/den[:,None]
            Nj=(-N/(2*X))[:,None]*Xj
            Tj=self.g*(op+2*Xj)
            J=np.exp(-lam)*self.Dx@(T[:,None]*Nj+N[:,None]*Tj)-Wp[:,None]*Nj-np.diag(N*Wpp)
        return R,J,dict(lam=lam,b=b,pl=pl,pb=pb,vol=vol,bx=bx,hk=hk,d=d,X=X,N=N,q=q,T=T,W=W,cap=cap)

    def constrain(self,y):
        P=self.P.copy()
        for it in range(20):
            R,J,f=self.fields(y,P,True);norm=float(np.max(np.abs(R)))
            if norm<2e-9:
                self.P=P;self.max_res=max(self.max_res,norm);self.newton+=it
                return f
            step=np.linalg.solve(J,-R);accepted=False
            for j in range(20):
                pp=P+step*2.**(-j)
                try:rr,_,_=self.fields(y,pp)
                except ValueError:continue
                if np.max(np.abs(rr))<norm:
                    P=pp;accepted=True;break
            if not accepted:raise RuntimeError(f'Newton line search residual {norm}')
        raise RuntimeError(f'Newton limit residual {norm}')

    def rhs(self,y):
        self.calls+=1;f=self.constrain(y)
        l,b,pl,pb,vol,bx,hk,d,X,N,T,W=[f[z]for z in ['lam','b','pl','pb','vol','bx','hk','d','X','N','T','W']]
        rate=N*(pl-pb)/(2*self.M*vol);ldot=rate.mean()
        ws=self.inverse_theta(ldot-rate)
        Nx=self.Dx@N
        Lsp=self.M*np.exp(-l+2*b)*(2*Nx*bx+N*bx*bx)
        F=-d+X-self.V-W-self.g*d*d/2-2*self.g*d*X
        Lm=N*vol*F;FD=-T
        bdot=-N*pl/(2*self.M*vol)+ws*(self.D@b)
        pldot=N*hk+N*vol*(F-FD*d)-Lsp+self.D@(ws*pl)
        flux=2*self.M*np.exp(-l+2*b)*(Nx+N*bx)+2*N*np.exp(2*b)*self.P*FD
        pbdot=2*N*hk+2*Lm+2*Lsp-self.Dx@flux+self.D@(ws*pb)
        return np.concatenate([[ldot],bdot,pldot,pbdot])

    def initial(self,homogeneous=False):
        n=self.n;th=2*np.pi*np.arange(n)/n
        H=np.sqrt((self.s2/2+self.V)/(3*self.M));pl=np.full(n,-2*self.M*H)
        if homogeneous:
            self.P=np.zeros(n);return np.concatenate([[0],np.zeros(n),pl,2*pl])
        _,sol,nf=build(self.k,1e-12);z=np.cos(th);N=nf(z,sol.sol(z)[0]);self.P=.002/self.k*np.sin(th)
        d=self.Dx@self.P;X=self.s2/(2*N*N);cap=self.K*np.abs(self.P)/self.a0
        W=self.a0*self.a0/self.K*(-cap-np.log1p(-cap))
        hs=-d-X-self.V-W-self.g*d*d/2+2*self.g*d*X
        pb=pl/2-2*self.M*hs/pl
        return np.concatenate([[0],np.zeros(n),pl,pb])

    def diagnostic(self,y,t):
        f=self.constrain(y);pl=f['pl'];pb=f['pb'];bx=f['bx'];q=f['q']
        mom=self.Dx@pl-bx*pb
        qs=np.fft.fft(q-q.mean());tail=np.abs(self.modes)>=self.n/3
        return dict(time=t,q_min=float(q.min()),q_max=float(q.max()),q_gradient=float(np.max(np.abs(self.Dx@q))),
                    X_min=float(f['X'].min()),lapse_max=float(f['N'].max()),cap=float(f['cap'].max()),
                    momentum_abs=float(np.max(np.abs(mom))),momentum_normalized=float(np.max(np.abs(mom))/(self.k*np.max(np.abs(pl)))),
                    polarization_residual=self.max_res,spectral_tail=float(np.sum(np.abs(qs[tail])**2)/(np.sum(np.abs(qs)**2)+1e-100)))


def rk4(sys,y,dt):
    a=sys.rhs(y);b=sys.rhs(y+dt*a/2);c=sys.rhs(y+dt*b/2);d=sys.rhs(y+dt*c)
    return y+dt*(a+2*b+2*c+d)/6


def validation():
    sys=System(16,128);y=sys.initial(True);dt=.0025
    for _ in range(40):y=rk4(sys,y,dt)
    lam,b,pl,pb=sys.unpack(y)
    ss=sys.s2;VV=sys.V;t=.1
    yy=np.sqrt(2*VV/ss)*np.sinh(np.arcsinh(np.sqrt(ss/(2*VV)))-np.sqrt(3*ss/(2*sys.M))*t)
    beta=-np.log(yy)/3;bd=np.sqrt((ss/2+VV*np.exp(6*beta))/(3*sys.M))
    err=max(abs(lam-beta),np.max(np.abs(b-beta)),np.max(np.abs(pl+2*sys.M*bd)),np.max(np.abs(pb+4*sys.M*bd)))
    sh=System(32,128);yh=sh.initial();R,J,_=sh.fields(yh,sh.P,True)
    th=2*np.pi*np.arange(32)/32;direction=np.sin(th)+.3*np.cos(2*th)+.2
    ep=1e-10
    rp,_,_=sh.fields(yh,sh.P+ep*direction);rm,_,_=sh.fields(yh,sh.P-ep*direction)
    fd=(rp-rm)/(2*ep);pred=J@direction
    je=float(np.max(np.abs(fd-pred))/np.max(np.abs(pred)))
    return dict(FRW_error=float(err),jacobian_relative_error=je,pass_checks=bool(err<1e-8 and je<1e-4))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=32)
    ap.add_argument('--dt',type=float,default=.0025);ap.add_argument('--tmax',type=float,default=.1);ap.add_argument('--validation-only',action='store_true');a=ap.parse_args()
    t0=time.time();out={'validation':validation(),'n':a.n,'dt':a.dt,'tmax':a.tmax,'scope':'unfiltered on-branch pre-break coupled planar ADM; no post-shock prescription'}
    if not out['validation']['pass_checks']:
        out['status']='validation failed'
    elif a.validation_only:
        out['status']='validated only'
    else:
        sy=System(a.n,128);y=sy.initial();t=0;records=[]
        try:
            records.append(sy.diagnostic(y,t))
            while t<a.tmax-1e-12:
                dt=min(a.dt,a.tmax-t);y=rk4(sy,y,dt);t+=dt
                if len(records)==0 or t-records[-1]['time']>=.099*a.dt/.0025 or t>=a.tmax-1e-12:
                    r=sy.diagnostic(y,t);records.append(r)
                    if r['spectral_tail']>1e-3:raise RuntimeError('resolved pre-break stop: spectral tail >1e-3')
            out['status']='completed pre-break'
        except (ValueError,RuntimeError,np.linalg.LinAlgError) as e:
            out['status']='stopped';out['reason']=str(e);out['stopped_time']=t
        out.update(records=records,calls=sy.calls,newton_iterations=sy.newton,final_state=y.tolist(),final_P=sy.P.tolist())
    out['seconds']=time.time()-t0
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['final_state','final_P']},indent=2))
    raise SystemExit(0 if out['status']in ['validated only','completed pre-break']else 1)


if __name__=='__main__':main()
