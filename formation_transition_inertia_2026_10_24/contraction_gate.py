"""Contraction-dependent barrier, with reciprocal baryonic force."""
import argparse,json,signal,time
from pathlib import Path
import numpy as np
from diffuse import Diffuse,PROFILES,timeout

class Contracting(Diffuse):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Rrot=float(np.dot(self.mb,np.sqrt(self.l2)))**2

    def energy(self,r,x,detail=False):
        if not hasattr(self,'Rrot'):return super().energy(r,x,detail)
        R=float(np.dot(self.mb,r));C=self.f**2*self.Rrot/(R+self.Rrot)
        old=self.C
        self.C=C
        e,g,gx,info=super().energy(r,x,detail)
        self.C=0.
        e0,_,_,_=super().energy(r,x)
        self.C=old
        dC=-C/(R+self.Rrot)
        if C>0:g=g+(e-e0)/C*dC*self.mb
        info['C']=C
        return e,g,gx,info

    def observe(self,t,y):
        row=super().observe(t,y)
        N=len(self.m);R=float(np.dot(self.mb,y[:N]));vb=float(np.dot(self.mb,y[N:2*N]))
        row['C']=self.f**2*self.Rrot/(R+self.Rrot)
        row['nongrav_baryon_acceleration']=float(self.lam*y[2*N+1]-self.Gamma*vb)
        return row

def checks():
    m=Contracting(1e8,1,scale=30);N=len(m.m);y=m.initial();y[2*N]=.4;y[2*N+1]=.1/m.tdyn
    E,g,gx,_=m.energy(y[:N],y[2*N]);dy=m.rhs(0,y)
    dt=1e-5*m.tdyn
    fd=(m.observe(0,y+dt*dy)['energy']-m.observe(0,y-dt*dy)['energy'])/(2*dt)
    errs=[]
    for i in range(m.n):
        r=y[:N].copy();h=1e-5*r[i];r[i]+=h;ep=m.energy(r,y[2*N])[0]
        r[i]-=2*h;em=m.energy(r,y[2*N])[0]
        errs.append(abs((ep-em)/(2*h)-g[i])/max(abs(g[i]),1e-10))
    out=dict(full_force_gradient_relative=float(max(errs)),energy_directional_scaled=float(abs(fd)/(abs(E)/m.tdyn)))
    assert max(errs)<1e-4 and out['energy_directional_scaled']<1e-6
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--n',type=int,default=6);ap.add_argument('--nq',type=int,default=256)
    ap.add_argument('--duration',type=float,default=12);ap.add_argument('--rtol',type=float,default=2e-7)
    ap.add_argument('--alphas',default='.3,1,3,10');ap.add_argument('--iotas',default='.01,.1')
    ap.add_argument('--fs',default='.3,.95');args=ap.parse_args()
    out=dict(checks=checks(),parameters=vars(args),runs=[]);path=Path(args.output)
    signal.signal(signal.SIGALRM,timeout)
    for f in map(float,args.fs.split(',')):
        for a in map(float,args.alphas.split(',')):
            for i in map(float,args.iotas.split(',')):
                row=dict(profile=1,scale=30,f=f,alpha=a,iota=i);start=time.monotonic()
                try:
                    signal.alarm(18);m=Contracting(1e8,1,n=args.n,nq=args.nq,f=f,alpha=a,iota=i,scale=30)
                    row.update(m.run(args.duration,args.rtol))
                except (ValueError,RuntimeError,TimeoutError) as exc:
                    row.update(status='inconclusive' if isinstance(exc,TimeoutError) else 'failed',reason=str(exc))
                finally:signal.alarm(0)
                row['elapsed']=time.monotonic()-start;out['runs'].append(row)
                path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
                print(json.dumps({k:v for k,v in row.items() if k!='history'}),flush=True)
