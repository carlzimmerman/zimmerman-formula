"""Positive-inertia reciprocal formation test. See CONTRACT.md."""
import argparse
import json
import signal
import sys
import time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'inputs'))
from assembly import Live, phase
from model import PROFILES, RESERVOIR


class Inertial(Live):
    def __init__(self, mass, b, n=6, nq=256, f=.95, alpha=1., iota=.1):
        super().__init__(mass, b, n, nq, f, alpha)
        frac=(np.arange(n)+.5)/n
        trunc=10**3/(1+10**2)**1.5
        rb=1/np.sqrt((frac*trunc)**(-2/3)-1)
        self.r0=3*np.r_[rb,3*rb]
        edges=np.geomspace(self.r0.min()*.005,self.r0.max()*400,nq+1)
        mid=(edges[1:]+edges[:-1])/2; width=np.diff(edges)/2
        self.grid=np.ravel(np.column_stack([mid-width/np.sqrt(3),mid+width/np.sqrt(3)]))
        self.weights=np.repeat(width,2); self.rmax=edges[-1]; self.rmin=edges[0]
        nodes,weights=np.polynomial.legendre.leggauss(32)
        self.tail_t=(nodes+1)/(2*self.rmax); self.tail_w=weights/(2*self.rmax)
        en,gr,_,_=self.energy(self.r0,0)
        vc2=np.maximum(self.r0*gr/self.m,1e-12)
        self.l2=.3*vc2*self.r0**2; self.v0=-.3*np.sqrt(vc2)
        half=float(np.interp(.5,np.cumsum(self.mb[:n]),self.r0[:n]))
        menc=float(np.interp(half,self.grid,self.kernel(self.r0)[0]@self.m))
        self.tdyn=np.sqrt(half**3/menc)
        self.J=f*float(np.dot(self.mb,np.sqrt(self.l2)))
        self.lam=alpha*self.J/half
        self.I=iota*RESERVOIR*half**2; self.iota=iota
        self.eta=.2*self.I/self.tdyn; self.Gamma=.2/self.tdyn

    def rhs(self,t,y):
        N=len(self.m); r=y[:N]; v=y[N:2*N]; x,xd=y[2*N:2*N+2]
        _,gr,gx,_=self.energy(r,x)
        vb=float(np.dot(self.mb,v))
        force=-gr+self.m*self.l2/r**3+(self.lam*xd-self.Gamma*vb)*self.mb
        xdd=(-gx-self.lam*vb-self.eta*xd)/self.I
        heat=self.Gamma*vb**2+self.eta*xd**2
        pump=-self.lam*vb*xd
        return np.r_[v,force/self.m,xd,xdd,heat,pump]

    def initial(self):
        return np.r_[self.r0,self.v0,0.,0.,0.,0.]

    def observe(self,t,y):
        N=len(self.m);r=y[:N];v=y[N:2*N];x,xd,Q,pump=y[2*N:]
        e,_,_,d=self.energy(r,x,True)
        kin=.5*np.dot(self.m,v*v+self.l2/r**2); internal=.5*self.I*xd*xd
        q=phase(x)[0]
        # Fixed canonical angular momenta: snapshot diagnostic in reduced model.
        bound=.5*(v*v+self.l2/r**2)+d['phi']<0
        retained=float(np.dot(self.md,bound)*(1-q)/RESERVOIR)
        order=np.argsort(r[:self.n]); br=r[:self.n][order]
        half=float(np.interp(.5,np.cumsum(self.mb[:self.n][order]),br))
        mask=(self.grid>.5*half)&(self.grid<5*half)&(d['Mb']>1e-8)
        gb=d['Mb']/self.grid**2
        expected=.5*(gb+np.sqrt(gb*gb+4*self.kappa*gb))
        residual=np.log10((d['M']/self.grid**2)[mask]/expected[mask])
        return dict(t=float(t/self.tdyn),q=float(q),x=float(x),xd=float(xd),
            energy=float(e+kin+internal+Q),receiver=float(Q),pump_work=float(pump),
            phase_kinetic=float(internal),field_energy=d['ut'],gravity=d['ug'],
            kinetic=float(kin),bound_free_fraction=retained,half_radius=half,
            rar_max_dex=float(max(abs(residual))),rar_rms_dex=float(np.sqrt(np.mean(residual**2))),
            max_u=d['max_u'])

    def run(self,duration=12,rtol=2e-7):
        N=len(self.m); y0=self.initial()
        def boundary(t,y):
            return min(np.min(y[:N])/self.rmin-2,self.rmax/(2*np.max(y[:N]))-1)
        boundary.terminal=True; boundary.direction=-1
        sol=solve_ivp(self.rhs,(0,duration*self.tdyn),y0,method='DOP853',rtol=rtol,
            atol=rtol*.01,max_step=.05*self.tdyn,dense_output=True,events=boundary)
        if not sol.success: raise RuntimeError(sol.message)
        hist=[self.observe(t,sol.sol(t)) for t in np.linspace(0,sol.t[-1],121)]
        norm=max(abs(hist[0]['energy']),abs(hist[0]['gravity']))
        drift=max(abs(h['energy']-hist[0]['energy'])/norm for h in hist)
        late=hist[96:]
        return dict(status='completed' if sol.status==0 else 'radial domain reached',
            nfev=sol.nfev,max_energy_error=drift,peak_q=max(h['q'] for h in hist),
            late_min_q=min(h['q'] for h in late),late_max_rar=max(h['rar_max_dex'] for h in late),
            final=hist[-1],history=hist)


def checks():
    out={}; m=Inertial(1e8,1,n=6,nq=256)
    y=m.initial();N=len(m.m);y[2*N]=.27;y[2*N+1]=.03/m.tdyn
    e,g,gx,_=m.energy(y[:N],y[2*N]);dy=m.rhs(0,y)
    ident=np.dot(g-m.m*m.l2/y[:N]**3,y[N:2*N])+np.dot(m.m*y[N:2*N],dy[N:2*N])+gx*y[2*N+1]+m.I*y[2*N+1]*dy[2*N+1]+dy[-2]
    out['energy_identity_scaled']=float(abs(ident)/(abs(e)/m.tdyn))
    # Directional finite difference of the whole energy along the actual RHS.
    dt=1e-5*m.tdyn
    fd=(m.observe(0,y+dt*dy)['energy']-m.observe(0,y-dt*dy)['energy'])/(2*dt)
    out['energy_directional_scaled']=float(abs(fd)/(abs(e)/m.tdyn))
    errors=[]
    for k in [0,3,6,10]:
        rr=y[:N].copy();step=rr[k]*1e-5;rr[k]+=step
        ep=m.energy(rr,y[2*N])[0];rr[k]-=2*step
        em=m.energy(rr,y[2*N])[0]
        errors.append(abs((ep-em)/(2*step)-g[k])/max(abs(g[k]),1e-10))
    out['force_gradient_relative']=float(max(errors))
    m0=Inertial(1e8,1,alpha=0); d0=m0.rhs(0,m0.initial())
    out['zero_coupling_phase_acceleration']=float(d0[-3])
    rev=Inertial(1e8,1,f=-.95); yr=y.copy();yr[2*N:2*N+2]*=-1
    dr=rev.rhs(0,yr);dr[2*N:2*N+2]*=-1
    out['rotation_reversal_max_error']=float(max(abs(dr-dy)))
    # Kinetic square's Hessian in (Rdot,xdot,thetadot) has positive eigenvalues.
    J=2.;a=.7;x=.4;Irot=3.
    mat=np.diag([1.,m.I,0.])+Irot*np.outer([-a*x,0,1],[-a*x,0,1])
    out['kinetic_min_eigenvalue']=float(np.linalg.eigvalsh(mat)[0])
    assert out['energy_identity_scaled']<1e-10
    assert out['energy_directional_scaled']<1e-6
    assert out['force_gradient_relative']<1e-4
    assert d0[-3]==0 and out['rotation_reversal_max_error']<1e-12
    assert out['kinetic_min_eigenvalue']>0
    return out


def timeout(signum, frame):
    raise TimeoutError('18 second per-trajectory cap')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--n',type=int,default=6);ap.add_argument('--nq',type=int,default=256)
    ap.add_argument('--duration',type=float,default=12);ap.add_argument('--rtol',type=float,default=2e-7)
    ap.add_argument('--profiles',default='0,1,2,3');ap.add_argument('--fs',default='.3,.95')
    ap.add_argument('--alphas',default='0,.3,1,3,10');ap.add_argument('--iotas',default='.01,.1')
    ap.add_argument('--checks-only',action='store_true');args=ap.parse_args()
    out=dict(checks=checks(),runs=[],parameters=vars(args)); path=Path(args.output)
    path.write_text(json.dumps(out,indent=2)+'\n')
    if args.checks_only:return
    signal.signal(signal.SIGALRM,timeout)
    for i in map(int,args.profiles.split(',')):
        _,mass,b,_=PROFILES[i]
        for f in map(float,args.fs.split(',')):
            for alpha in map(float,args.alphas.split(',')):
                for iota in map(float,args.iotas.split(',')):
                    if alpha==0 and iota!=.1:continue
                    start=time.monotonic();row=dict(profile=i,f=f,alpha=alpha,iota=iota)
                    try:
                        signal.alarm(18)
                        m=Inertial(mass,b,args.n,args.nq,f,alpha,iota)
                        row.update(m.run(args.duration,args.rtol))
                    except (ValueError,RuntimeError,TimeoutError) as exc:
                        row.update(status='inconclusive' if isinstance(exc,TimeoutError) else 'failed',reason=str(exc))
                    finally:signal.alarm(0)
                    row['elapsed']=time.monotonic()-start;out['runs'].append(row)
                    path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
                    print(json.dumps({k:v for k,v in row.items() if k!='history'}),flush=True)

if __name__=='__main__':main()
