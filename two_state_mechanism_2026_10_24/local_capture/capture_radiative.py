"""Local reversible collision capture with distinct T/F particle trajectories."""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model import G,A0,RESERVOIR,PROFILES,mt,outer

def w(z):
    if np.any(z>=1): raise ValueError('saturation domain')
    return np.where(z<.01,sum(z**k/k for k in range(2,10)),-np.log1p(-z)-z)

def local_moments(point,xb,vb,mb,k=None):
    k=min(max(12,int(round(3*np.sqrt(len(xb))))) if k is None else k,len(xb));distance=np.linalg.norm(xb-point,axis=1)
    ids=np.argsort(distance)[:k];h=max(distance[ids[-1]]*1.001,1e-8)
    xx=xb[ids];vv=vb[ids];X=np.column_stack([np.ones(k),(xx-xx.mean(0))/h])
    V=vv-vv.mean(0);XtX=X.T@X
    inv=np.linalg.inv(XtX+np.diag([0,.1,.1,.1]))
    coef=inv@X.T@V;res=V-X@coef
    H=X@inv@X.T;dof=k-2*np.trace(H)+np.sum(H*H)
    sigma2=float(np.sum(res*res)/(3*max(dof,1)))
    J=coef[1:].T/h
    curl=np.array([J[2,1]-J[1,2],J[0,2]-J[2,0],J[1,0]-J[0,1]])
    noise=2*sigma2*np.trace((inv@XtX@inv)[1:,1:])/h**2
    # Conservative signal estimate, calibrated on noise-only controls.
    om2=max(float(curl@curl)-4*noise,0.)
    C=om2/(om2+sigma2/h**2+1e-30)
    weights=np.maximum(1-(distance[ids]/h)**2,0)**2
    # Integral of (1-r²/h²)² over a ball is 32 pi h³/105.
    rho=float(np.dot(mb[ids],weights)/(32*np.pi*h**3/105))
    return dict(C=float(C),sigma2=sigma2,h=h,rho=rho,ids=ids,weights=weights)

def reaction_impulse(vi,vj,mi,mj,n,delta):
    vn=float((vi-vj)@n);mu=mi*mj/(mi+mj);kn=.5*mu*vn*vn
    if vn>=0 or kn<max(delta,0): return None
    newvn=np.sqrt(max(0,vn*vn-2*delta/mu))
    impulse=mu*(newvn-vn)*n
    return vi+impulse/mi,vj-impulse/mj,kn

class Capture:
    def __init__(self,mass,b,n=32,nq=256,f=.95,flat=.25,beta=4,seed=11,soft=.2,cooling=True,energy_budget=5e-5):
        self.n=n;self.f=f;self.flat=flat;self.beta=beta;self.seed=seed;self.soft=soft;self.cooling=cooling
        self.energy_budget=energy_budget
        self.rng=np.random.default_rng(seed);self.kappa=A0*b*b/(G*mass)
        self.m=np.r_[np.full(n,1/n),np.full(n,RESERVOIR/n)];self.state=np.zeros(2*n,dtype=bool)
        frac=(np.arange(n)+.5)/n;trunc=1000/101**1.5
        rb=1/np.sqrt((frac*trunc)**(-2/3)-1)
        rm=np.sqrt(G*mass/A0);bd=b/rm;R=outer(bd)
        rc=np.array([brentq(lambda r:mt(r,bd)-z*RESERVOIR,1e-12,R) for z in frac])*rm/b
        direction=self.rng.normal(size=(2*n,3));direction/=np.linalg.norm(direction,axis=1)[:,None]
        self.x=3*np.r_[rb,rc][:,None]*direction;self.x[:n,2]*=flat
        self.x-=np.average(self.x,axis=0,weights=self.m)
        self.rmax=max(np.linalg.norm(self.x,axis=1))*100
        edges=np.geomspace(soft*.001,self.rmax,nq+1)
        mid=(edges[1:]+edges[:-1])/2;width=np.diff(edges)/2
        self.grid=np.ravel(np.column_stack([mid-width/np.sqrt(3),mid+width/np.sqrt(3)]))
        self.wt=np.repeat(width,2)
        nodes,weights=np.polynomial.legendre.leggauss(32)
        self.tail=(nodes+1)/(2*self.rmax);self.tailwt=weights/(2*self.rmax)
        E,acc,_=self.energy_force(self.x,self.state)
        r=np.linalg.norm(self.x,axis=1);er=self.x/r[:,None]
        vc=np.sqrt(np.maximum(-np.sum(acc*er,axis=1)*r,1e-8))
        random=self.rng.normal(size=(2*n,3));random-=np.sum(random*er,axis=1)[:,None]*er
        random/=np.linalg.norm(random,axis=1)[:,None]
        az=np.column_stack([-self.x[:,1],self.x[:,0],np.zeros(2*n)])
        az/=np.linalg.norm(az,axis=1)[:,None]
        tangent=random.copy();tangent[:n]=f*az[:n]+np.sqrt(1-f*f)*random[:n]
        tangent/=np.linalg.norm(tangent,axis=1)[:,None]
        self.v=vc[:,None]*(np.sqrt(.7)*tangent-.3*er)
        self.v-=np.average(self.v,axis=0,weights=self.m)
        half=np.median(r[:n]);inner=np.sum(self.m[r<half]);self.tdyn=np.sqrt(half**3/max(inner,.01))
        self.Q=0.;self.initialE=E+self.kinetic(self.v);self.norm=max(abs(E),abs(self.initialE))
        self.L0=np.sum(self.m[:,None]*np.cross(self.x,self.v),axis=0)
        self.P0=np.sum(self.m[:,None]*self.v,axis=0)
        self.Lscale=np.sum(self.m*np.linalg.norm(np.cross(self.x,self.v),axis=1))
        self.Pscale=np.sum(self.m*np.linalg.norm(self.v,axis=1))
        self.stats=dict(attempts=0,captures=0,releases=0,energy_rejections=0,barrier_rejections=0,
                        saturation_rejections=0,cooling_events=0,substeps=0,event_energy_error=0.,event_p_error=0.,event_l_error=0.)

    def kinetic(self,v): return .5*float(np.sum(self.m[:,None]*v*v))

    def basis(self,x):
        rel=x-np.average(x,axis=0,weights=self.m)
        radius=np.sqrt(np.sum(rel*rel,axis=1)+self.soft**2)
        t=self.grid[:,None]/radius[None,:];a=np.clip((t-.75)/.5,0,1)
        S=a**3*(10+a*(-15+6*a));dS=-60*a*a*(1-a)**2*t/radius[None,:]
        return S,dS,rel,radius

    def field(self,M,total):
        z=M/(self.kappa*self.grid**2);zt=total*self.tail**2/self.kappa
        E=self.kappa**2*(np.dot(self.wt,self.grid**2*w(z))+np.dot(self.tailwt,w(zt)/self.tail**4))
        return float(E),z

    def energy_force(self,x,state):
        dif=x[:,None,:]-x[None,:,:]
        r2=np.sum(dif*dif,axis=2)+self.soft**2
        inv=1/np.sqrt(r2);np.fill_diagonal(inv,0.)
        phi=-inv@self.m;ug=.5*float(self.m@phi)
        ag=-np.sum(dif*(inv**3*self.m[None,:])[:,:,None],axis=1)
        S,dS,rel,radius=self.basis(x);mT=self.m*state;M=S@mT
        ut,z=self.field(M,float(np.sum(mT)))
        radial=self.kappa*mT*(dS.T@(self.wt*z/(1-z)))
        grad=radial[:,None]*rel/radius[:,None]
        grad-=self.m[:,None]/np.sum(self.m)*np.sum(grad,axis=0)
        return ug+ut,ag-grad/self.m[:,None],dict(phi=phi,ut=ut,max_z=float(np.max(z)))

    def advance(self,x,v,state,dt,depth=0):
        E,acc,_=self.energy_force(x,state);old=E+self.kinetic(v)
        vh=v+.5*dt*acc;xn=x+dt*vh
        try:
            En,an,_=self.energy_force(xn,state);vn=vh+.5*dt*an
            err=abs(En+self.kinetic(vn)-old)
            okay=err<=self.energy_budget*self.norm*dt/self.tdyn
        except ValueError:
            okay=False
        if okay:
            self.stats['substeps']+=1
            return xn,vn
        if depth>=18: raise RuntimeError('unresolved force/energy step near field wall')
        xm,vm=self.advance(x,v,state,dt/2,depth+1)
        return self.advance(xm,vm,state,dt/2,depth+1)

    def collide(self,dt,rate=10):
        S,_,_,_=self.basis(self.x);M=S@(self.m*self.state);total=float(self.m@self.state)
        energy,_=self.field(M,total)
        for i in self.rng.permutation(np.arange(self.n,2*self.n)):
            mom=local_moments(self.x[i],self.x[:self.n],self.v[:self.n],self.m[:self.n])
            j=int(self.rng.choice(mom['ids'],p=mom['weights']/sum(mom['weights'])))
            dr=self.x[i]-self.x[j];normal=dr/np.linalg.norm(dr)
            incoming=-float((self.v[i]-self.v[j])@normal)
            if incoming<=0: continue
            # Position-only reference speed; reaction rate carries collision flux.
            vref=np.sqrt(np.sum(self.m[mom['ids']])/mom['h'])
            hazard=rate*np.sqrt(mom['rho'])*incoming/max(vref,1e-30)
            if self.rng.random()>-np.expm1(-hazard*dt): continue
            self.stats['attempts']+=1
            change=self.m[i]*(1 if not self.state[i] else -1)
            Mp=M+change*S[:,i];tp=total+change
            # Exact zeros avoid cancellation after the last T packet is released.
            if abs(tp)<1e-12:tp=0.;Mp=np.zeros_like(M)
            try:newenergy,_=self.field(Mp,tp)
            except ValueError:
                self.stats['saturation_rejections']+=1;continue
            delta=newenergy-energy
            proposal=reaction_impulse(self.v[i],self.v[j],self.m[i],self.m[j],normal,delta)
            if proposal is None:self.stats['energy_rejections']+=1;continue
            vi,vj,kn=proposal
            vb=self.v[:self.n].copy();vb[j]=vj
            after=local_moments(self.x[i],self.x[:self.n],vb,self.m[:self.n])
            barrier=self.beta*.5*(mom['C']+after['C'])*abs(delta)
            if kn<max(delta,0)+barrier:self.stats['barrier_rejections']+=1;continue
            # A distinct dissipative capture channel, after crossing the same barrier.
            # Outgoing normal speed restitution=.3 for F->T only; Q pays the loss.
            radiation=0.
            if not self.state[i]:
                radiation=(1-.3**2)*max(kn-delta,0.)
                vi,vj,_=reaction_impulse(self.v[i],self.v[j],self.m[i],self.m[j],normal,delta+radiation)
            oldk=.5*(self.m[i]*np.dot(self.v[i],self.v[i])+self.m[j]*np.dot(self.v[j],self.v[j]))
            newk=.5*(self.m[i]*np.dot(vi,vi)+self.m[j]*np.dot(vj,vj))
            dp=self.m[i]*(vi-self.v[i])+self.m[j]*(vj-self.v[j])
            dl=self.m[i]*np.cross(self.x[i],vi-self.v[i])+self.m[j]*np.cross(self.x[j],vj-self.v[j])
            self.stats['event_energy_error']=max(self.stats['event_energy_error'],abs(newk-oldk+delta+radiation)/self.norm)
            self.stats['event_p_error']=max(self.stats['event_p_error'],float(np.linalg.norm(dp))/self.Pscale)
            self.stats['event_l_error']=max(self.stats['event_l_error'],float(np.linalg.norm(dl))/self.Lscale)
            self.stats['releases' if self.state[i] else 'captures']+=1
            self.Q+=radiation
            self.stats['capture_radiation']=self.stats.get('capture_radiation',0.)+radiation
            self.state[i]=not self.state[i];self.v[i]=vi;self.v[j]=vj
            M=Mp;total=tp;energy=newenergy
        if self.cooling:
            for i in self.rng.permutation(self.n):
                mom=local_moments(self.x[i],self.x[:self.n],self.v[:self.n],self.m[:self.n])
                if self.rng.random()>-np.expm1(-np.sqrt(mom['rho'])*dt):continue
                weights=mom['weights'].copy();weights[mom['ids']==i]=0
                j=int(self.rng.choice(mom['ids'],p=weights/sum(weights)))
                normal=self.x[i]-self.x[j];normal/=np.linalg.norm(normal)
                vn=float((self.v[i]-self.v[j])@normal)
                if vn>=0:continue
                mu=self.m[i]*self.m[j]/(self.m[i]+self.m[j]);loss=.5*mu*vn*vn*(1-.5**2)
                impulse=mu*(-.5*vn-vn)*normal
                self.v[i]+=impulse/self.m[i];self.v[j]-=impulse/self.m[j];self.Q+=loss
                self.stats['cooling_events']+=1

    def snapshot(self,t):
        E,acc,d=self.energy_force(self.x,self.state);K=self.kinetic(self.v)
        r=np.linalg.norm(self.x-np.average(self.x,axis=0,weights=self.m),axis=1)
        bary=self.x[:self.n]-np.average(self.x[:self.n],axis=0,weights=self.m[:self.n])
        shape=np.linalg.eigvalsh((bary.T*self.m[:self.n])@bary)
        bound=.5*np.sum(self.v*self.v,axis=1)+d['phi']<0
        free=self.m*(~self.state);free[:self.n]=0
        S,_,_,_=self.basis(self.x);M=S@self.m;Mb=S[:,:self.n]@self.m[:self.n]
        half=np.median(r[:self.n]);mask=(self.grid>.5*half)&(self.grid<5*half)&(Mb>1e-8)
        gb=Mb/self.grid**2;expected=.5*(gb+np.sqrt(gb*gb+4*self.kappa*gb))
        residual=np.log10((M/self.grid**2)[mask]/expected[mask])
        Cs=[local_moments(self.x[i],self.x[:self.n],self.v[:self.n],self.m[:self.n])['C'] for i in range(self.n,2*self.n)]
        L=np.sum(self.m[:,None]*np.cross(self.x,self.v),axis=0);P=np.sum(self.m[:,None]*self.v,axis=0)
        return dict(t=float(t),q=float(self.m@self.state/RESERVOIR),bound_free_fraction=float(free@bound/RESERVOIR),
            energy_error=abs(E+K+self.Q-self.initialE)/self.norm,receiver=self.Q,field_energy=d['ut'],
            rar_max_dex=float(np.max(abs(residual))),rar_rms_dex=float(np.sqrt(np.mean(residual**2))),
            shape_axis_ratio=float(np.sqrt(shape[0]/shape[-1])),local_C_mean=float(np.mean(Cs)),
            momentum_error=float(np.linalg.norm(P-self.P0)/self.Pscale),
            angular_momentum_error=float(np.linalg.norm(L-self.L0)/self.Lscale),max_z=d['max_z'])

    def run(self,duration=8,dt=.02):
        history=[self.snapshot(0)];steps=int(np.ceil(duration/dt));status='completed';reason=None
        for step in range(steps):
            h=min(dt,duration-step*dt)
            try:
                self.x,self.v=self.advance(self.x,self.v,self.state,h*self.tdyn)
                self.collide(h*self.tdyn)
                if np.max(np.linalg.norm(self.x,axis=1))>self.rmax/2:raise RuntimeError('outer domain reached')
            except (ValueError,RuntimeError) as err:
                status='incomplete';reason=str(err);break
            if (step+1)%max(1,steps//40)==0 or step==steps-1:history.append(self.snapshot(min((step+1)*dt,duration)))
        return dict(status=status,reason=reason,n=self.n,seed=self.seed,f=self.f,flat=self.flat,beta=self.beta,
            soft=self.soft,cooling=self.cooling,dt=dt,energy_budget=self.energy_budget,history=history,final=history[-1],stats=self.stats,
            max_energy_error=max(z['energy_error'] for z in history),
            max_angular_momentum_error=max(z['angular_momentum_error'] for z in history),
            final_positions=self.x.tolist(),final_velocities=self.v.tolist(),final_states=self.state.tolist())

def checks():
    m=Capture(1e8,1,n=16,nq=512);m.state[16:20]=True
    E,acc,_=m.energy_force(m.x,m.state);errors=[]
    for i,j in ((0,0),(17,1),(22,2)):
        dx=np.zeros_like(m.x);dx[i,j]=1e-5
        fd=(m.energy_force(m.x+dx,m.state)[0]-m.energy_force(m.x-dx,m.state)[0])/2e-5
        exact=-m.m[i]*acc[i,j];errors.append(abs(fd-exact)/max(abs(exact),1e-9))
    assert max(errors)<1e-4
    rng=np.random.default_rng(91);xb=rng.normal(size=(32,3));vb=np.cross([0,0,2.],xb)+.1*rng.normal(size=(32,3))
    mb=np.ones(32)/32;pt=np.array([.1,.2,.3]);C=local_moments(pt,xb,vb,mb)['C']
    angle=.71;Q=np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]])
    shifted=local_moments(pt+[2,3,4],xb+[2,3,4],vb+[80,-30,5],mb)['C']
    rotated=local_moments(Q@pt,xb@Q.T,vb@Q.T,mb)['C']
    assert max(abs(C-shifted),abs(C-rotated))<1e-10
    vi=np.array([-2.,.3,.5]);vj=np.array([1.,-.2,.7]);n=np.array([1.,0,0]);mi=2.;mj=3.;delta=.7
    a,b,kn=reaction_impulse(vi,vj,mi,mj,n,delta)
    rev=reaction_impulse(-a,-b,mi,mj,n,-delta)
    inverse=max(np.max(abs(rev[0]+vi)),np.max(abs(rev[1]+vj)))
    energy=abs(.5*mi*(a@a-vi@vi)+.5*mj*(b@b-vj@vj)+delta)
    assert inverse<1e-12 and energy<1e-12
    return dict(force_relative_error=max(errors),boost_error=abs(C-shifted),rotation_error=abs(C-rotated),
                impulse_energy_error=energy,inverse_impulse_error=inverse)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=32)
    ap.add_argument('--nq',type=int,default=256);ap.add_argument('--duration',type=float,default=8)
    ap.add_argument('--dt',type=float,default=.02);ap.add_argument('--profiles',default='0,1,2,3')
    ap.add_argument('--fs',default='0,.95');ap.add_argument('--flats',default='1,.25')
    ap.add_argument('--betas',default='0,4,20');ap.add_argument('--seeds',default='11');ap.add_argument('--soft',type=float,default=.2)
    ap.add_argument('--no-cooling',action='store_true');args=ap.parse_args()
    out=dict(checks=checks(),runs=[],scope='3D packet transport with COM-centered monopole tether field; finite synthetic test')
    for i in map(int,args.profiles.split(',')):
        _,mass,b,_=PROFILES[i]
        for f in map(float,args.fs.split(',')):
            for flat in map(float,args.flats.split(',')):
                for beta in map(float,args.betas.split(',')):
                    for seed in map(int,args.seeds.split(',')):
                        row=Capture(mass,b,args.n,args.nq,f,flat,beta,seed,args.soft,not args.no_cooling).run(args.duration,args.dt)
                        row.update(profile_index=i,mass_msun=mass,b_kpc=b)
                        out['runs'].append(row)
                        print(json.dumps({k:v for k,v in row.items() if k not in ('history','final_positions','final_velocities','final_states')}),flush=True)
                        Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
