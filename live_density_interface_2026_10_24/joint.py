"""Mobile density and phase from one energy; target law only in diagnostics."""
import argparse,json,sys
from pathlib import Path
import numpy as np
import torch
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).parent/'inputs'))
from model import G,A0,RESERVOIR,outer,law
torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)
T=lambda a:torch.tensor(a,dtype=torch.float64)

class Joint:
    def __init__(self,n=96,domain=2,beta=1000,k=120,tau=1,K=.1):
        self.n=n;self.rm=np.sqrt(G*6e10/A0);self.b=3/self.rm
        self.R=domain*outer(self.b);self.beta=beta;self.k=k;self.tau=tau;self.K=K
        # Uniform geometry, no target-law enclosed mass in quadrature.
        edges=np.linspace(0,self.R,n+1);r=(edges[1:]+edges[:-1])/2
        self.r=T(r);self.vol=T(np.diff(edges**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2)
        self.B=T(np.tril(np.ones((n,n)),-1)+.5*np.eye(n));self.A=self.B/self.r[:,None]**2
        self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2)
        self.ell2=(30/self.rm)**2;self.delta=1e-5
        nodes,weights=np.polynomial.legendre.leggauss(48);self.tt=T((nodes+1)/(2*self.R));self.tw=T(weights/(2*self.R))
    def functions(self,u):
        # Exact on physical branch; C2 continuation solely for line searches.
        c=.98;v=torch.clamp(u,max=c);d=u-v
        w=-torch.log1p(-v)-v+d*c/(1-c)+.5*d*d/(1-c)**2
        F=v*v/(1-v)+d*c*(2-c)/(1-c)**2+d*d/(1-c)**3
        return w,F
    def energy(self,z,x):
        m=RESERVOIR*torch.softmax(z,dim=0);q=torch.sin(torch.pi*x/2)**2;mt=m*q;mf=m*(1-q)
        u=self.A@mt;w,F=self.functions(u);s=torch.sin(torch.pi*x)**2/torch.pi**2
        W=torch.sum(self.vol*(w+self.beta*.95*s*F));M=mt.sum()
        W=W+torch.sum(self.tw*self.functions(M*self.tt**2)[0]/self.tt**4)
        uf=(u[1:]+u[:-1])/2;ff=self.functions(uf)[1];dx=x[1:]-x[:-1]
        elastic=.5*self.ell2*torch.sum(self.rf**2/self.dr*ff*dx**2)
        # Response stiffness exterior capacitance to infinity: finite-box
        # interface tail truncation made explicit; candidate requires x_end~0.
        # Exterior gradient coefficient F~r^-4 gives zero infinite capacity.
        dq=q[1:]-q[:-1];reg=self.delta*self.dr;soft=dq*dq/(torch.sqrt(dq*dq+reg*reg)+reg)
        I=torch.sum(self.rf**2*ff*soft);J=torch.sum(self.rf**2*soft)
        surface=self.tau*J+self.k/(I+1e-30)
        gravity=torch.dot(m,self.phib)-.5*torch.dot(m,self.grav@m)
        gas=1.5*self.K*torch.sum(self.vol*(mf/self.vol)**(5/3))
        return W+elastic+surface+gravity+gas
    def fg(self,v):
        a=T(v).requires_grad_(True);E=self.energy(a[:self.n],a[self.n:]);g=torch.autograd.grad(E,a)[0]
        return float(E.detach()),g.detach().numpy()
    def initial(self,scale=1,front=.4):
        r=self.r.numpy();a=scale*self.b
        mass=self.vol.numpy()*(1+(r/a)**2)**(-2.5);z=np.log(mass);z-=z.mean()
        x=.5*(1-np.tanh((r-front*outer(self.b))/(.08*outer(self.b))))
        return np.r_[z,x]
    def report(self,v):
        E,g=self.fg(v);z=v[:self.n];x=v[self.n:];mass=RESERVOIR*np.exp(z-max(z));mass/=sum(mass)/RESERVOIR
        q=np.sin(np.pi*x/2)**2;r=self.r.numpy();mt=mass*q;mf=mass*(1-q)
        enclosed=self.B.numpy()@mass;gb=r/(r*r+self.b*self.b)**1.5;gt=gb+enclosed/r**2;ref=law(gb)
        inner=(r>=.5*self.b)&(r<=5*self.b);out=r>=.8*outer(self.b)
        # Density gradient in softmax is m_i(mu_i-mean_mu); divide to
        # prevent empty cells masquerading as density stationarity.
        active=mass>RESERVOIR*1e-7
        cross=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0]
        projected=g.copy();lo=v[self.n:]<=1e-8;hi=v[self.n:]>=1-1e-8
        projected[self.n:][lo & (g[self.n:]>0)]=0;projected[self.n:][hi & (g[self.n:]<0)]=0
        return dict(n=self.n,R_kpc=self.R*self.rm,beta=self.beta,k=self.k,tau=self.tau,K=self.K,energy=E,gradient_max=float(max(abs(projected))),density_chemical_spread=float(np.ptp(g[:self.n][active]/mass[active])),max_u=float(max(self.A.numpy()@mt)),qinner=float(mass[inner]@q[inner]/sum(mass[inner])),qouter=float(mass[out]@q[out]/sum(mass[out])),inner_mass=float(sum(mass[inner])),outer_mass=float(sum(mass[out])),edge_mass_fraction=float(sum(mass[-max(2,self.n//20):])/RESERVOIR),law_max_dex=float(max(abs(np.log10(gt[inner]/ref[inner])))),free_source_ratio_max=float(max((self.A.numpy()@mf)[inner]/gb[inner])),crossings_kpc=(r[cross]*self.rm).tolist(),r=(r*self.rm).tolist(),mass=mass.tolist(),q=q.tolist(),v=v.tolist(),g_total=gt.tolist(),g_law=ref.tolist())
    def solve(self,v):
        opt=minimize(self.fg,v,jac=True,method='L-BFGS-B',bounds=[(-35,35)]*self.n+[(0,1)]*self.n,options=dict(maxiter=5000,ftol=1e-13,gtol=1e-8,maxls=40,maxcor=25))
        r=self.report(opt.x);r['optimizer']=dict(success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit));return r

def checks():
    m=Joint(n=24,K=.3);v=m.initial(scale=4);v[m.n:]=np.linspace(.7,.2,m.n)
    E,g=m.fg(v);d=np.sin(np.arange(2*m.n)+.4);eps=1e-6
    fd=(m.fg(v+eps*d)[0]-m.fg(v-eps*d)[0])/(2*eps);error=abs(fd-g@d)/max(abs(fd),1)
    assert error<1e-6
    # Gravity has an independent symmetric shell-potential derivative.
    mass=np.linspace(.001,.02,m.n);grad=m.phib.numpy()-m.grav.numpy()@mass
    def grav(a):return a@m.phib.numpy()-.5*a@m.grav.numpy()@a
    fdg=(grav(mass+eps*d[:m.n])-grav(mass-eps*d[:m.n]))/(2*eps)
    ge=abs(fdg-grad@d[:m.n])/max(abs(fdg),1);assert ge<1e-7
    return dict(joint_directional_error=error,gravity_directional_error=ge)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=dict(checks=checks(),runs=[])
    for beta,k,tau in [(20,120,1),(1000,100,.1),(1000,120,1)]:
        for K in [.03,.3,3]:
            m=Joint(beta=beta,k=k,tau=tau,K=K);r=m.solve(m.initial(scale=4));out['runs'].append(r);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['v','r','mass','q','g_total','g_law']},flush=True)
