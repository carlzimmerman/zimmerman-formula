"""Reciprocal assembly work and live spherical shells; see CONTRACT.md."""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import G, A0, RESERVOIR, PROFILES, mt, outer

def phase(x):
    return (np.sin(np.pi*x/2)**2, np.pi/2*np.sin(np.pi*x),
            np.sin(np.pi*x)**2/np.pi**2, np.sin(2*np.pi*x)/np.pi)

def wf(z):
    if np.any(z >= 1):
        raise ValueError('tether saturation wall reached; no clipping')
    w = np.where(z < .01, sum(z**k/k for k in range(2,10)), -np.log1p(-z)-z)
    return w, z*z/(1-z), z*(2-z)/(1-z)**2

class Live:
    def __init__(self, mass, b, n=12, nq=512, f=.95, alpha=.3, beta=20):
        self.n=n; self.f=f; self.alpha=alpha; self.beta=beta
        self.kappa=A0*b*b/(G*mass)
        self.m=np.r_[np.full(n,1/n),np.full(n,RESERVOIR/n)]
        self.dark=np.r_[np.zeros(n),np.ones(n)]
        self.md=self.m*self.dark; self.mb=self.m*(1-self.dark)
        self.C=f*f
        frac=(np.arange(n)+.5)/n
        trunc=10**3/(1+10**2)**1.5
        rb=1/np.sqrt((frac*trunc)**(-2/3)-1)
        rm=np.sqrt(G*mass/A0); bd=b/rm; rout=outer(bd)
        rc=np.array([brentq(lambda r:mt(r,bd)-z*RESERVOIR,1e-10,rout) for z in frac])*rm/b
        self.r0=3*np.r_[rb,rc]
        edges=np.geomspace(self.r0.min()*.02,self.r0.max()*200,nq+1)
        # Two-point Gauss quadrature within each logarithmic cell.
        mid=(edges[1:]+edges[:-1])/2; width=np.diff(edges)/2
        self.grid=np.ravel(np.column_stack([mid-width/np.sqrt(3),mid+width/np.sqrt(3)]))
        self.weights=np.repeat(width,2); self.rmax=edges[-1]; self.rmin=edges[0]
        node,weight=np.polynomial.legendre.leggauss(32)
        self.tail_t=(node+1)/(2*self.rmax); self.tail_w=weight/(2*self.rmax)
        en,grad,_,_=self.energy(self.r0,0.)
        vc2=np.maximum(self.r0*grad/self.m,1e-12)
        self.l2=.7*vc2*self.r0**2
        self.v0=-.3*np.sqrt(vc2)
        half=float(np.interp(.5,np.cumsum(self.mb[:n]),self.r0[:n]))
        menc=float(np.interp(half,self.grid,self.kernel(self.r0)[0]@self.m))
        self.tdyn=np.sqrt(half**3/menc)
        self.Gamma=10/self.tdyn
        self.eta=.01*abs(en)*self.tdyn
        self.A=alpha*half*self.C

    def kernel(self,r):
        if np.min(r)<=0: raise ValueError('nonpositive shell radius')
        t=self.grid[:,None]/r[None,:]
        a=np.clip((t-.75)/.5,0,1)
        S=a*a*a*(10+a*(-15+6*a))
        dSdt=30*a*a*(1-a)**2/.5
        dSdr=-dSdt*t/r[None,:]
        return S,dSdr

    def energy(self,r,x,detail=False):
        q,hp,s,sp=phase(x); S,dS=self.kernel(r)
        M=S@self.m; Mc=S@self.md
        rad=self.grid; wt=self.weights; kap=self.kappa
        z=q*Mc/(kap*rad**2)
        w,F,Fp=wf(z); coef=self.beta*self.C
        ug=-.5*np.dot(wt,M*M/rad**2)-.5*np.sum(self.m)**2/self.rmax
        ut=kap**2*np.dot(wt,rad**2*(w+coef*s*F))
        zg=q*RESERVOIR*self.tail_t**2/kap
        wg,Fg,Fpg=wf(zg)
        ut+=kap**2*np.dot(self.tail_w,(wg+coef*s*Fg)/self.tail_t**4)
        deriv=z/(1-z)+coef*s*Fp
        gr=-self.m*(dS.T@(wt*M/rad**2))+q*kap*self.md*(dS.T@(wt*deriv))
        gx=kap*hp*np.dot(wt,Mc*deriv)+kap**2*coef*sp*np.dot(wt,rad**2*F)
        gx+=kap*hp*RESERVOIR*np.dot(self.tail_w,(zg/(1-zg)+coef*s*Fpg)/self.tail_t**2)
        gx+=kap**2*coef*sp*np.dot(self.tail_w,Fg/self.tail_t**4)
        info=dict(ug=float(ug),ut=float(ut),max_u=float(np.max(z)))
        if detail:
            info['phi']=-S.T@(wt*M/rad**2)-np.sum(self.m)/self.rmax
            info['M']=M; info['Mb']=S@self.mb
        return float(ug+ut),gr,float(gx),info

    def rhs(self,t,y):
        N=len(self.m); r=y[:N]; v=y[N:2*N]; x=y[2*N]
        _,gr,gx,_=self.energy(r,x)
        vb=float(np.dot(self.mb,v))
        dx=-(gx+self.Gamma*self.A*vb)/(self.eta+self.Gamma*self.A**2)
        slip=vb+self.A*dx
        force=-gr+self.m*self.l2/r**3-self.Gamma*slip*self.mb
        heat=self.Gamma*slip*slip+self.eta*dx*dx
        # Signed state-energy transfer from reciprocal mechanical coupling.
        pump=-self.Gamma*self.A*slip*dx
        return np.r_[v,force/self.m,dx,heat,pump]

    def run(self,duration=30,rtol=2e-7):
        N=len(self.m); y0=np.r_[self.r0,self.v0,0.,0.,0.]
        def boundary(t,y):
            return min(np.min(y[:N])/self.rmin-2,self.rmax/(2*np.max(y[:N]))-1)
        boundary.terminal=True; boundary.direction=-1
        sol=solve_ivp(self.rhs,(0,duration*self.tdyn),y0,method='DOP853',rtol=rtol,
                      atol=rtol*.01,max_step=.2*self.tdyn,dense_output=True,events=boundary)
        if not sol.success: raise RuntimeError(sol.message)
        hist=[]; e0=None
        for t in np.linspace(0,sol.t[-1],101):
            y=sol.sol(t);r=y[:N];v=y[N:2*N];x=y[2*N]
            e,_,_,d=self.energy(r,x,True)
            kin=.5*np.dot(self.m,v*v+self.l2/r**2)
            total=e+kin+y[2*N+1]
            if e0 is None: e0=total; norm=max(abs(e0),abs(d['ug']))
            q=phase(x)[0]
            bound=.5*(v*v+self.l2/r**2)+d['phi']<0
            retained=float(np.dot(self.md,bound)*(1-q)/RESERVOIR)
            order=np.argsort(r[:self.n]); br=r[:self.n][order]
            half=float(np.interp(.5,np.cumsum(self.mb[:self.n][order]),br))
            mask=(self.grid>.5*half)&(self.grid<5*half)&(d['Mb']>1e-8)
            gb=d['Mb']/self.grid**2
            expected=.5*(gb+np.sqrt(gb*gb+4*self.kappa*gb))
            actual=d['M']/self.grid**2
            residual=np.log10(actual[mask]/expected[mask])
            hist.append(dict(t=float(t/self.tdyn),q=float(q),half_radius=half,
                 energy_error=float(abs(total-e0)/norm),bound_free_fraction=retained,
                 bound_free_per_baryon=retained*RESERVOIR,rar_max_dex=float(np.max(abs(residual))),
                 rar_rms_dex=float(np.sqrt(np.mean(residual**2))),receiver=float(y[2*N+1]),
                 pump_work=float(y[2*N+2]),field_energy=d['ut'],gravity=d['ug'],kinetic=float(kin),
                 max_u=d['max_u']))
        return dict(f=self.f,alpha=self.alpha,beta=self.beta,n=self.n,rtol=rtol,
            status='completed' if sol.status==0 else 'radial domain reached',nfev=sol.nfev,
            max_energy_error=max(z['energy_error'] for z in hist),final=hist[-1],history=hist,
            final_radii=sol.y[:N,-1].tolist(),final_radial_v=sol.y[N:2*N,-1].tolist())

def checks():
    m=Live(1e8,1,n=6,nq=512)
    r=m.r0.copy();x=.31;E,g,gx,_=m.energy(r,x)
    errs=[]
    for i in (0,3,6,10):
        d=np.zeros(len(r)); d[i]=1e-5*r[i]
        fd=(m.energy(r+d,x)[0]-m.energy(r-d,x)[0])/(2*d[i])
        errs.append(abs(fd-g[i])/max(abs(g[i]),1e-9))
    fd=(m.energy(r,x+1e-5)[0]-m.energy(r,x-1e-5)[0])/2e-5
    phase_err=abs(fd-gx)/max(abs(gx),1e-9)
    y=np.r_[r,m.v0,x,0.,0.];dy=m.rhs(0,y);N=len(r)
    identity=np.dot(g-m.m*m.l2/r**3,m.v0)+np.dot(m.m*m.v0,dy[N:2*N])+gx*dy[2*N]+dy[2*N+1]
    assert max(errs)<1e-4 and phase_err<1e-4
    assert abs(identity)<1e-9*max(abs(E)/m.tdyn,1e-12)
    return dict(force_relative_error=max(errs),phase_relative_error=phase_err,
                instantaneous_energy_identity=float(identity),mass=float(sum(m.m)))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--n',type=int,default=12);ap.add_argument('--nq',type=int,default=512)
    ap.add_argument('--duration',type=float,default=30);ap.add_argument('--rtol',type=float,default=2e-7)
    ap.add_argument('--alphas',default='0,.1,.3,1,3');ap.add_argument('--profiles',default='0,1,2,3')
    ap.add_argument('--fs',default='0,.3,.95');args=ap.parse_args()
    out=dict(checks=checks(),runs=[],scope='Live spherical collective-phase approximation; no disk formation claim')
    for i in map(int,args.profiles.split(',')):
        _,mass,b,_=PROFILES[i]
        for f in map(float,args.fs.split(',')):
            for alpha in map(float,args.alphas.split(',')):
                try:
                    row=Live(mass,b,args.n,args.nq,f,alpha).run(args.duration,args.rtol)
                except (ValueError,RuntimeError) as err:
                    row=dict(f=f,alpha=alpha,status='failed',reason=str(err))
                row.update(profile_index=i,mass_msun=mass,b_kpc=b)
                out['runs'].append(row)
                print(json.dumps({k:v for k,v in row.items() if k not in ('history','final_radii','final_radial_v')}),flush=True)
                Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
