"""Ordered angular momentum exchange with explicit viscous heat."""
import argparse,json,signal,time
from pathlib import Path
import numpy as np
from contraction_gate import Contracting

class Transport(Contracting):
    def __init__(self,*args,nu0=1,**kwargs):
        super().__init__(*args,**kwargs)
        self.j0=self.f*np.sqrt(self.l2[:self.n])
        self.random_l2=(1-self.f**2)*self.l2[:self.n].copy()
        half=float(np.interp(.5,np.cumsum(self.mb[:self.n]),self.r0[:self.n]))
        self.nu=nu0*half**2/self.tdyn

    def initial(self):
        return np.r_[super().initial(),self.j0]

    def set_j(self,y):
        j=y[-self.n:]
        self.l2[:self.n]=j*j+self.random_l2

    def rhs(self,t,y):
        self.set_j(y);core=y[:-self.n]
        dy=super().rhs(t,core)
        r=y[:self.n];j=y[-self.n:];mu=self.mb[:self.n]
        omega=j/r**2
        K=np.exp(-.5*np.log(r[:,None]/r[None,:])**2)
        delta=omega[None,:]-omega[:,None]
        dj=self.nu*(K*delta)@mu
        heat=.5*self.nu*np.sum(mu[:,None]*mu[None,:]*K*delta**2)
        dy[-2]+=heat
        return np.r_[dy,dj]

    def observe(self,t,y):
        self.set_j(y);row=super().observe(t,y[:-self.n])
        row['J']=float(np.dot(self.mb[:self.n],y[-self.n:]))
        row['minimum_baryon_radius']=float(min(y[:self.n]))
        return row

def checks():
    m=Transport(1e8,1,scale=30);N=len(m.m);y=m.initial()
    y[2*N]=.4;y[2*N+1]=.1/m.tdyn
    dy=m.rhs(0,y);dt=1e-5*m.tdyn
    ep=m.observe(0,y+dt*dy)['energy'];em=m.observe(0,y-dt*dy)['energy']
    E=m.observe(0,y)['energy'];error=abs((ep-em)/(2*dt))/(abs(E)/m.tdyn)
    torque=float(np.dot(m.mb[:m.n],dy[-m.n:]))
    assert error<1e-6 and abs(torque)<1e-12
    assert dy[2*N+2]>=0
    return dict(full_energy_directional_scaled=float(error),total_torque=torque,heat_rate=float(dy[2*N+2]))

def timeout(signum,frame):raise TimeoutError('30 second transport trajectory cap')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--n',type=int,default=6);ap.add_argument('--nq',type=int,default=256)
    ap.add_argument('--duration',type=float,default=12);ap.add_argument('--rtol',type=float,default=2e-7)
    ap.add_argument('--fs',default='.3,.95');ap.add_argument('--alphas',default='1,3')
    ap.add_argument('--iotas',default='.01,.1');ap.add_argument('--nu',type=float,default=1)
    args=ap.parse_args();out=dict(checks=checks(),parameters=vars(args),runs=[]);path=Path(args.output)
    signal.signal(signal.SIGALRM,timeout)
    for f in map(float,args.fs.split(',')):
        for a in map(float,args.alphas.split(',')):
            for i in map(float,args.iotas.split(',')):
                row=dict(profile=1,scale=30,f=f,alpha=a,iota=i,nu=args.nu);start=time.monotonic()
                try:
                    signal.alarm(30);m=Transport(1e8,1,n=args.n,nq=args.nq,f=f,alpha=a,iota=i,scale=30,nu0=args.nu)
                    row.update(m.run(args.duration,args.rtol))
                    row['max_J_error']=max(abs(h['J']-m.J) for h in row['history'])/max(abs(m.J),1e-12)
                except (ValueError,RuntimeError,TimeoutError) as exc:
                    row.update(status='inconclusive' if isinstance(exc,TimeoutError) else 'failed',reason=str(exc))
                finally:signal.alarm(0)
                row['elapsed']=time.monotonic()-start;out['runs'].append(row)
                path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
                print(json.dumps({k:v for k,v in row.items() if k!='history'}),flush=True)
