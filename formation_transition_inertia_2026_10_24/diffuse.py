"""Same rotor interaction, initially diffuse free material."""
import argparse,json,signal,time
from pathlib import Path
import numpy as np
from experiment import Inertial,PROFILES,RESERVOIR,timeout

class Diffuse(Inertial):
    def __init__(self,mass,b,n=6,nq=256,f=.95,alpha=1,iota=.1,scale=30):
        super().__init__(mass,b,n,nq,f,alpha,iota)
        self.r0[n:]*=scale/3
        en,gr,_,_=self.energy(self.r0,0)
        vc2=np.maximum(self.r0*gr/self.m,1e-12)
        self.l2=.3*vc2*self.r0**2;self.v0=-.3*np.sqrt(vc2)
        half=float(np.interp(.5,np.cumsum(self.mb[:n]),self.r0[:n]))
        menc=float(np.interp(half,self.grid,self.kernel(self.r0)[0]@self.m))
        self.tdyn=np.sqrt(half**3/menc)
        self.J=f*float(np.dot(self.mb,np.sqrt(self.l2)));self.lam=alpha*self.J/half
        self.I=iota*RESERVOIR*half**2
        self.eta=.2*self.I/self.tdyn;self.Gamma=.2/self.tdyn

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--profiles',default='1');ap.add_argument('--fs',default='.95')
    ap.add_argument('--alphas',default='1,3,10');ap.add_argument('--iotas',default='.01,.1')
    ap.add_argument('--scales',default='10,30');ap.add_argument('--n',type=int,default=6)
    ap.add_argument('--nq',type=int,default=256);ap.add_argument('--duration',type=float,default=12)
    ap.add_argument('--rtol',type=float,default=2e-7);args=ap.parse_args()
    out=dict(parameters=vars(args),runs=[]);path=Path(args.output)
    signal.signal(signal.SIGALRM,timeout)
    for i in map(int,args.profiles.split(',')):
        _,mass,b,_=PROFILES[i]
        for f in map(float,args.fs.split(',')):
            for alpha in map(float,args.alphas.split(',')):
                for iota in map(float,args.iotas.split(',')):
                    for scale in map(float,args.scales.split(',')):
                        row=dict(profile=i,f=f,alpha=alpha,iota=iota,scale=scale);t=time.monotonic()
                        try:
                            signal.alarm(18);m=Diffuse(mass,b,args.n,args.nq,f,alpha,iota,scale)
                            row.update(m.run(args.duration,args.rtol))
                        except (ValueError,RuntimeError,TimeoutError) as exc:
                            row.update(status='inconclusive' if isinstance(exc,TimeoutError) else 'failed',reason=str(exc))
                        finally:signal.alarm(0)
                        row['elapsed']=time.monotonic()-t;out['runs'].append(row)
                        path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
                        print(json.dumps({k:v for k,v in row.items() if k!='history'}),flush=True)
