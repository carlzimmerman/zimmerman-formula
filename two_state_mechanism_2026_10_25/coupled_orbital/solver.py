"""Hamiltonian lattice test; no galaxy classifications or capture fractions."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq

class Medium:
    def __init__(self,n=4,g=-4/3,source=.02):
        self.n=n; self.N=n**3; self.g=g; self.M=100.;self.K=10.;self.d=.2
        self.kappa=1.;self.Q=1.
        q=2*np.pi*np.fft.fftfreq(n)
        self.ks=np.meshgrid(q,q,q,indexing='ij')
        self.D=[1j*np.sin(k) for k in self.ks]
        self.lap=sum(4*np.sin(k/2)**2 for k in self.ks)
        self.green=np.zeros_like(self.lap); np.divide(1.,self.lap,out=self.green,where=self.lap>1e-14)
        self.hz=2-sum(np.cos(k) for k in self.ks); self.hy=np.sin(self.ks[2])
        self.hnorm=np.sqrt(self.hz**2+self.hy**2)
        self.omega=np.sqrt(self.K*self.lap/self.M)
        coords=np.meshgrid(*[np.arange(n)-(n-1)/2]*3,indexing='ij')
        self.xyz=[c.ravel() for c in coords]
        self.src=source*np.cos(2*np.pi*np.indices((n,n,n))[2]/n)
        self.shape=(n,n,n,2,2*self.N)
    def fft(self,a):return np.fft.fftn(a,axes=(0,1,2))
    def ifft(self,a):return np.fft.ifftn(a,axes=(0,1,2))
    def grad(self,a):
        ak=self.fft(a)
        return np.stack([self.ifft(D*ak).real for D in self.D],axis=-1)
    def div(self,u):return sum(self.ifft(D*self.fft(u[...,a])).real for a,D in enumerate(self.D))
    def h0(self,W):
        w=self.fft(W); out=np.empty_like(w)
        out[...,0,:]=self.hz[...,None]*w[...,0,:]-1j*self.hy[...,None]*w[...,1,:]
        out[...,1,:]=1j*self.hy[...,None]*w[...,0,:]-self.hz[...,None]*w[...,1,:]
        return self.ifft(out)
    def densities(self,W):
        a,b=W[...,0,:],W[...,1,:]
        na=np.sum(abs(a)**2,axis=-1); nb=np.sum(abs(b)**2,axis=-1)
        return na+nb,2*np.real(np.sum(a.conj()*b,axis=-1)),na-nb
    def field(self,W,u):
        n,s,z=self.densities(W)
        P=-u.copy();P[...,2]+=self.d*s
        rho=n-1+self.src-self.div(P)
        phi=self.ifft(self.green*self.fft(rho)).real
        return rho,phi,n,s,z
    def energy(self,W,u,p):
        rho,phi,n,s,z=self.field(W,u)
        band=float(np.vdot(W,self.h0(W)).real)
        ec=.5*float(np.sum(rho*phi))
        kin=float(np.sum(p*p)/(2*self.M))
        elastic=self.K/2*sum(float(np.sum((np.roll(u,-1,axis=a)-u)**2)) for a in range(3))
        deformation=float(self.g*np.sum(self.div(u)*z))
        return dict(band=band,electric=ec,ionic_kinetic=kin,elastic=elastic,deformation=deformation,
                    total=band+ec+kin+elastic+deformation)
    def prepare(self,temperature,rotation):
        eye=np.eye(2*self.N,dtype=complex).reshape(self.shape)
        h=self.h0(eye).reshape(2*self.N,2*self.N)
        X=np.repeat(self.xyz[0],2);Y=np.repeat(self.xyz[1],2)
        vx=1j*(h*X[None,:]-X[:,None]*h)
        vy=1j*(h*Y[None,:]-Y[:,None]*h)
        self.Lz=(X[:,None]*vy+vy*X[None,:]-Y[:,None]*vx-vx*Y[None,:])/2
        ew,v=eigh(h-rotation*self.Lz,check_finite=False)
        def occ(mu):return 1/(1+np.exp(np.clip((ew-mu)/temperature,-700,700)))
        mu=brentq(lambda mu:occ(mu).sum()-self.N,ew[0]-10,ew[-1]+10,xtol=1e-14)
        self.occ=occ(mu)
        return (v*np.sqrt(self.occ)).reshape(self.shape),np.zeros((self.n,)*3+(3,)),np.zeros((self.n,)*3+(3,))
    def free(self,W,u,p,dt):
        w=self.fft(W);a=w[...,0,:].copy();b=w[...,1,:].copy()
        c=np.cos(self.hnorm*dt)[...,None]
        s=(dt*np.sinc(self.hnorm*dt/np.pi))[...,None]
        w[...,0,:]=c*a-1j*s*(self.hz[...,None]*a-1j*self.hy[...,None]*b)
        w[...,1,:]=c*b-1j*s*(1j*self.hy[...,None]*a-self.hz[...,None]*b)
        W=self.ifft(w)
        uk=self.fft(u);pk=self.fft(p);co=np.cos(self.omega*dt)[...,None]
        si=(dt*np.sinc(self.omega*dt/np.pi))[...,None]
        un=co*uk+si*pk/self.M
        pn=co*pk-self.M*self.omega[...,None]**2*si*uk
        return W,self.ifft(un).real,self.ifft(pn).real
    def coulomb(self,W,u,p,dt):
        rho,phi,n,s,z=self.field(W,u);grad=self.grad(phi)
        angle=self.d*grad[...,2]*dt
        a=W[...,0,:].copy();b=W[...,1,:].copy()
        co=np.cos(angle)[...,None];si=np.sin(angle)[...,None];phase=np.exp(-1j*phi*dt)[...,None]
        W[...,0,:]=phase*(co*a-1j*si*b);W[...,1,:]=phase*(co*b-1j*si*a)
        p=p+dt*grad
        return W,u,p
    def deform(self,W,u,p,dt):
        z=self.densities(W)[2]
        phase=np.exp(-1j*self.g*self.div(u)*dt)
        W[...,0,:]*=phase[...,None];W[...,1,:]*=phase.conj()[...,None]
        return W,u,p+dt*self.g*self.grad(z)
    def step(self,W,u,p,dt):
        W,u,p=self.free(W,u,p,dt/2)
        W,u,p=self.coulomb(W,u,p,dt/2)
        W,u,p=self.deform(W,u,p,dt)
        W,u,p=self.coulomb(W,u,p,dt/2)
        return self.free(W,u,p,dt/2)
    def measure(self,W,u,p):
        rho,phi,n,s,z=self.field(W,u);en=self.energy(W,u,p)
        srcphi=self.ifft(self.green*self.fft(self.src)).real
        denom=float(np.sum(srcphi*srcphi))
        amp=float(np.sum(phi*srcphi)/denom) if denom else None
        return dict(energy=en,charge=float(rho.sum()),number=float(n.sum()),
                    field_projection=amp,charge_rms=float(np.std(rho)),
                    density_rms=float(np.std(n)),max_ionic_displacement=float(np.max(np.linalg.norm(u,axis=-1))),
                    internal_polarization_rms=float(self.d*np.std(s)),
                    angular_momentum=float(np.vdot(W.reshape(2*self.N,-1),self.Lz@W.reshape(2*self.N,-1)).real))

def run(n,temp,rot,dt,T,g=-4/3,source=.02):
    m=Medium(n,g,source);W,u,p=m.prepare(temp,rot)
    initial=W.copy();gram=initial.reshape(2*m.N,-1).conj().T@initial.reshape(2*m.N,-1)
    rows=[];steps=round(T/dt)
    for step in range(steps+1):
        if step%max(1,steps//20)==0 or step==steps:
            rows.append(dict(time=step*dt,**m.measure(W,u,p)))
        if step<steps:W,u,p=m.step(W,u,p,dt)
    e0=rows[0]['energy']['total']
    reference=max(abs(e0),1e-15)
    w=W.reshape(2*m.N,-1)
    return dict(n=n,temperature=temp,rotation=rot,dt=dt,T=T,g=g,source=source,
                max_energy_error=max(abs(r['energy']['total']-e0) for r in rows),
                max_relative_energy_error=max(abs(r['energy']['total']-e0)/reference for r in rows),
                max_charge_error=max(abs(r['charge']) for r in rows),
                gram_error=float(np.max(abs(w.conj().T@w-gram))),
                wave_change=float(np.linalg.norm(W-initial)),rows=rows)


def audit():
    m=Medium(4);W,u,p=m.prepare(.2,.1)
    # Deterministic perturbations for derivatives away from a stationary point.
    ix=np.indices((4,4,4));u[...,0]=.003*np.cos(np.pi*ix[1]/2);u[...,2]=.002*np.sin(np.pi*ix[2]/2)
    W,u,p=m.step(W,u,p,.13)
    rho,phi,n,s,z=m.field(W,u)
    grad=m.grad(phi)
    hW=m.h0(W)+phi[...,None,None]*W
    hW[...,0,:]+=m.d*grad[...,2,None]*W[...,1,:]+m.g*m.div(u)[...,None]*W[...,0,:]
    hW[...,1,:]+=m.d*grad[...,2,None]*W[...,0,:]-m.g*m.div(u)[...,None]*W[...,1,:]
    direction=np.exp(1j*np.arange(W.size).reshape(W.shape)*.17)/np.sqrt(W.size)
    analytic=2*np.vdot(direction,hW).real
    eps=1e-6
    numeric=(m.energy(W+eps*direction,u,p)['total']-m.energy(W-eps*direction,u,p)['total'])/(2*eps)
    # General variation need not preserve neutrality: L+ defines energy on zero-mean component.
    du=np.sin(np.arange(u.size).reshape(u.shape)*.31)/np.sqrt(u.size)
    Lu=m.ifft(m.lap[...,None]*m.fft(u)).real
    derivative=m.K*Lu-grad-m.g*m.grad(z)
    ua=float(np.sum(derivative*du))
    un=(m.energy(W,u+eps*du,p)['total']-m.energy(W,u-eps*du,p)['total'])/(2*eps)
    sub=[]
    for name in ['free','coulomb','deform']:
        w1,u1,p1=getattr(m,name)(W.copy(),u.copy(),p.copy(),.07)
        if name=='coulomb':key=['electric']
        elif name=='deform':key=['deformation']
        else:key=['band','ionic_kinetic','elastic']
        en0=m.energy(W,u,p);en1=m.energy(w1,u1,p1)
        sub.append(dict(flow=name,hamiltonian_error=abs(sum(en1[k]-en0[k] for k in key))))
    result=dict(orbital_derivative_error=abs(numeric-analytic),ionic_derivative_error=abs(un-ua),subflow_checks=sub)
    assert result['orbital_derivative_error']<1e-6
    assert result['ionic_derivative_error']<1e-6
    assert max(s['hamiltonian_error'] for s in sub)<1e-9
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    result={'audit':audit(),'runs':[]}
    cases=[(4,t,r,.02,6.,-4/3,.02) for t in [.05,.2,.8] for r in [0.,.05,.15]]
    cases += [(4,.2,.15,.01,6.,-4/3,.02),(4,.2,.15,.005,6.,-4/3,.02),
              (4,.2,.15,.01,6.,0.,.02),(4,.2,0.,.02,6.,-4/3,0.),
              (6,.2,.15,.02,6.,-4/3,.02)]
    for case in cases:
        r=run(*case);result['runs'].append(r)
        print(case,'dE',r['max_energy_error'],'Q',r['max_charge_error'],'field',r['rows'][-1]['field_projection'],flush=True)
        assert r['max_charge_error']<1e-8
        assert r['gram_error']<1e-9
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
