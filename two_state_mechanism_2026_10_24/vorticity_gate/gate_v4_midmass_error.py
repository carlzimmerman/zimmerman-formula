"""Label-blind effective barrier on a constrained spherical T/F mass field.

Fixed total density and fixed baryon moments: not a live gravitational run.
All scientific scope and predeclared criteria are in CONTRACT.md.
"""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.linalg import cho_factor,cho_solve

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model import G,A0,PROFILES,RESERVOIR,law,excess,mb,mt,outer


def h(x): return x*x*(3-2*x)
def hp(x): return 6*x*(1-x)
def hpp(x): return 6-12*x
def s(x): return x*x*(1-x)**2
def sp(x): return 2*x*(1-x)*(1-2*x)
def spp(x): return 2-12*x+12*x*x


def w(z):
    z=np.asarray(z)
    if np.any(z>=1): raise ValueError('saturation wall crossed')
    answer=-np.log1p(-z)-z
    small=z<.01
    answer=np.where(small,sum(z**k/k for k in range(2,10)),answer)
    return answer


def F(z): return z*z/(1-z)
def Fp(z): return z*(2-z)/(1-z)**2


def curl_matrix(J):
    return np.array([J[2,1]-J[1,2],J[0,2]-J[2,0],J[1,0]-J[0,1]])


def moment_C(gradient,velocities,grad_logrho,hess_logrho):
    centered=velocities-np.mean(velocities,axis=0)
    sigma2=np.mean(centered*centered)
    invL2=np.dot(grad_logrho,grad_logrho)+np.linalg.norm(hess_logrho)
    om2=np.dot(curl_matrix(gradient),curl_matrix(gradient))
    denom=om2+sigma2*invL2
    return om2/denom if denom else 0.


class Field:
    def __init__(self,mass,b_kpc,n=64,length_kpc=0.,grid='log'):
        self.mass=mass
        self.rm=np.sqrt(G*mass/A0)
        self.b=b_kpc/self.rm
        self.R=outer(self.b)
        self.n=n
        edges=np.r_[0.,np.geomspace(self.R*1e-4,self.R,n)] if grid=='log' else np.linspace(0,self.R,n+1)
        self.grid=grid
        self.r=(edges[:-1]+edges[1:])/2
        self.vol=np.diff(edges**3)/3
        self.m=np.diff(np.r_[0.,mt(edges[1:],self.b)])
        self.a=self.vol/self.r**2
        self.baryon_g=mb(self.r,self.b)/self.r**2
        self.g0=law(self.baryon_g)
        nodes,weights=np.polynomial.legendre.leggauss(48)
        self.tail_t=(nodes+1)/(2*self.R)
        self.tail_w=weights/(2*self.R)
        self.u0=self.u(np.ones(n))
        self.mu0=self.mu(self.u0,np.zeros(n),0.,np.zeros(n))
        self.mobility_denom=self.m*self.mu0
        self.normalization=float(np.sum(self.mobility_denom))
        self.length_kpc=length_kpc
        self.links=(length_kpc/self.rm)**2*((self.r[:-1]+self.r[1:])/2)**2/np.diff(self.r)
        self.Lmat=np.zeros((n,n))
        for i,weight in enumerate(self.links):
            self.Lmat[i,i]+=weight; self.Lmat[i+1,i+1]+=weight
            self.Lmat[i,i+1]-=weight; self.Lmat[i+1,i]-=weight
        self.A=(np.tril(np.ones((n,n)),-1)+.5*np.eye(n))*self.m[None,:]/self.r[:,None]**2
        assert np.all(self.m>0) and np.max(self.u0)<1

    def u(self,q):
        mT=self.m*q
        return (np.cumsum(mT)-.5*mT)/self.r**2

    def tail_mu(self,M):
        if M<=0: return 0.
        return np.sqrt(M)*np.arctanh(np.sqrt(M)/self.R)

    def mu(self,u,x,beta,C):
        deriv=u/(1-u)+beta*C*s(x)*Fp(u)
        terms=self.a*deriv
        # Tail has no internal material or barrier; its W energy remains.
        M=float(np.sum(self.m*h(x))) if beta else None
        # Caller can set beta=0 with x=0 for initial all-T reference.
        if M is None:
            # Infer total from actual q in the last u is ambiguous; only used
            # for the all-T initialization above. General energy_grad below
            # supplies the mass explicitly and does not use this shortcut.
            M=RESERVOIR
        return np.cumsum(terms[::-1])[::-1]-.5*terms+self.tail_mu(M)

    def kinematics(self,f):
        r=self.r; b=self.b; core=.1*b
        y=self.baryon_g
        dgdy=.5*(1+(y+2)/np.sqrt(y*y+4*y))
        dlogg=(y/self.g0)*dgdy*(1-3*r*r/(r*r+b*b))
        alpha=.5*(1+dlogg)+core*core/(r*r+core*core)
        vphi=f*np.sqrt(r*self.g0)*r/np.sqrt(r*r+core*core)
        omega=(1+alpha)*vphi/r
        radial=np.geomspace(r[0]*.5,max(self.R,b)*1e5,12000)
        rho=(1+(radial/b)**2)**-2.5
        g=law(mb(radial,b)/radial**2)
        integrand=rho*g*(1-f*f*radial**2/(radial**2+core**2))
        pressure=-cumulative_trapezoid(integrand[::-1],radial[::-1],initial=0)[::-1]
        sig2=np.interp(r,radial,pressure/rho)
        grad=-5*r/(r*r+b*b)
        Hr=-5*(b*b-r*r)/(r*r+b*b)**2
        Ht=-5/(r*r+b*b)
        invL2=grad*grad+np.sqrt(Hr*Hr+2*Ht*Ht)
        C=omega*omega/(omega*omega+sig2*invL2)
        assert np.all((C>=0)&(C<=1)) and np.all(sig2>0)
        return dict(C=C,omega=omega,sigma2=sig2,vphi=vphi,invL2=invL2)

    def energy_grad(self,x,beta,C):
        q=h(x); u=self.u(q); sx=s(x)
        M=float(np.dot(self.m,q))
        tail=float(np.dot(self.tail_w,w(M*self.tail_t**2)/self.tail_t**4))
        E=float(np.dot(self.vol,w(u)+beta*C*sx*F(u))+tail)
        terms=self.a*(u/(1-u)+beta*C*sx*Fp(u))
        mu=np.cumsum(terms[::-1])[::-1]-.5*terms+self.tail_mu(M)
        grad=hp(x)*self.m*mu+beta*C*sp(x)*F(u)*self.vol
        diff=np.diff(x); flux=self.links*diff
        E+=.5*float(np.dot(diff,flux))
        grad[:-1]-=flux; grad[1:]+=flux
        return E,grad

    def hessian(self,x,beta,C):
        q=h(x); u=self.u(q); Hprime=hp(x)
        M=float(np.dot(self.m,q))
        terms=self.a*(u/(1-u)+beta*C*s(x)*Fp(u))
        mu=np.cumsum(terms[::-1])[::-1]-.5*terms+self.tail_mu(M)
        d2=self.vol*(1/(1-u)**2+beta*C*s(x)*2/(1-u)**3)
        J=self.A*Hprime[None,:]
        H=J.T@(d2[:,None]*J)
        cross=J.T*(self.vol*beta*C*sp(x)*Fp(u))[None,:]
        H+=cross+cross.T
        H+=np.diag(hpp(x)*self.m*mu+self.vol*beta*C*spp(x)*F(u))
        dmu=(np.arctanh(np.sqrt(M)/self.R)/(2*np.sqrt(M))+
              1/(2*self.R*(1-M/self.R**2))) if M>1e-16 else 1/self.R
        mhp=self.m*Hprime
        H+=dmu*np.outer(mhp,mhp)
        return H+self.Lmat

    def stability(self,beta,C):
        # Hessian is diagonal at pure T since h'(1)=s'(1)=0.
        curvature=-6*self.m*self.mu0+2*beta*C*F(self.u0)*self.vol
        crit=np.divide(3*self.m*self.mu0,C*F(self.u0)*self.vol,
                       out=np.full(self.n,np.inf),where=C>0)
        return curvature,crit

    def evolve(self,f,beta,seed=.999,duration=100.,rtol=1e-8,gradient_damping=False):
        kin=self.kinematics(f); C=kin['C']
        x0=np.full(self.n,seed)
        E0,_=self.energy_grad(x0,beta,C)
        metric=np.diag(self.mobility_denom)+(self.Lmat if gradient_damping else 0.)
        factor=cho_factor(metric)
        def mobility(v): return cho_solve(factor,v)
        def rhs(t,y):
            _,grad=self.energy_grad(y[:-1],beta,C)
            dx=-mobility(grad)
            heat=float(np.dot(grad,-dx))/self.normalization
            return np.r_[dx,heat]
        def jac(t,y):
            _,grad=self.energy_grad(y[:-1],beta,C)
            H=self.hessian(y[:-1],beta,C)
            matrix=np.zeros((self.n+1,self.n+1))
            matrix[:-1,:-1]=-mobility(H)
            matrix[-1,:-1]=2*mobility(grad)@H/self.normalization
            return matrix
        times=np.linspace(0,duration,51)
        sol=solve_ivp(rhs,(0,duration),np.r_[x0,0.],method='BDF',jac=jac,t_eval=times,
                      rtol=rtol,atol=rtol*.01)
        if not sol.success: raise RuntimeError(sol.message)
        x=sol.y[:-1,-1]; q=h(x)
        if np.min(sol.y[:-1]) < -1e-6 or np.max(sol.y[:-1])>1+1e-6:
            raise ValueError('phase coordinate escaped [0,1]: '+str((np.min(sol.y[:-1]),np.max(sol.y[:-1]))))
        balances=[]
        for j in range(sol.y.shape[1]):
            e,_=self.energy_grad(sol.y[:-1,j],beta,C)
            balances.append(abs(e+sol.y[-1,j]*self.normalization-E0)/max(abs(E0),1e-30))
        frac=float(np.dot(self.m,q)/RESERVOIR)
        mF=np.cumsum(self.m*(1-q))-.5*self.m*(1-q)
        gf=mF/self.r**2
        conditional_g=law(self.baryon_g+gf)
        disk_range=(self.r>=.5*self.b)&(self.r<=min(5*self.b,self.R))&(q>=.95)
        rar=np.log10(conditional_g/self.g0)
        T_required=self.r*self.r*excess(self.baryon_g+gf)
        T_total=float(np.dot(self.m,q))
        curvature,crit=self.stability(beta,C)
        # Cold force residual at near-endpoints, ignoring intermediate barrier
        # stresses; report only where local and all barrier terms are tiny.
        result=dict(f=f,beta=beta,n=self.n,seed=seed,duration=duration,length_kpc=self.length_kpc,grid=self.grid,
            gradient_damping=gradient_damping,
            tethered_mass_fraction=frac,free_mass_fraction=1-frac,
            energy_receiver_balance_max=max(balances),
            receiver_energy_normalized=float(sol.y[-1,-1]),
            initially_unstable_T_mass_fraction=float(np.sum(self.m[curvature<0])/RESERVOIR),
            mass_balance_relative_error=abs(float(np.dot(self.m,q)+np.dot(self.m,1-q))-RESERVOIR)/RESERVOIR,
            C_mass_mean=float(np.dot(self.m,C)/RESERVOIR),
            protected_target_pass=bool(frac>=.95) if f>=.95 and seed>.5 else None,
            conversion_target_pass=bool(frac<=.1) if f<=.3 and seed>.5 else None,
            conditional_RAR_max_dex=float(np.max(rar[disk_range])) if np.any(disk_range) else None,
            conditional_T_supply_available=bool(np.max(T_required[disk_range])<=T_total) if np.any(disk_range) else None,
            diagnostic_active_radial_cells=int(np.sum(disk_range)),
            r_over_b=(self.r/self.b).tolist(),q=q.tolist(),C=C.tolist(),
            critical_beta=np.where(np.isfinite(crit),crit,-1).tolist(),
            free_to_baryon_enclosed=(gf/self.baryon_g).tolist(),
            conditional_RAR_dex=rar.tolist(),
            history=[dict(t=float(t),tethered_fraction=float(np.dot(self.m,h(sol.y[:-1,j]))/RESERVOIR)) for j,t in enumerate(times)])
        return result


def checks():
    field=Field(1e8,1.,32)
    C=field.kinematics(.95)['C']
    x=np.linspace(.2,.9,32)
    E,grad=field.energy_grad(x,20.,C)
    errors=[]
    for i in (0,5,15,25,31):
        step=.01 if abs(grad[i])<1e-6 else .001
        d=np.zeros(32); d[i]=step
        fd=(-field.energy_grad(x+2*d,20.,C)[0]+8*field.energy_grad(x+d,20.,C)[0]
            -8*field.energy_grad(x-d,20.,C)[0]+field.energy_grad(x-2*d,20.,C)[0])/(12*step)
        errors.append(abs(fd-grad[i])/max(abs(grad[i]),1e-10))
    assert max(errors)<2e-5
    one=np.ones(32)
    Ebar,gbar=field.energy_grad(one,20.,C)
    Eoff,goff=field.energy_grad(one,0.,C)
    assert abs(Ebar-Eoff)<1e-12 and np.max(abs(gbar))<1e-12
    curv,crit=field.stability(20.,C)
    curverr=[]
    for i in (5,15,25):
        d=np.zeros(32); d[i]=1e-5
        numeric=(field.energy_grad(one+d,20.,C)[1][i]-field.energy_grad(one-d,20.,C)[1][i])/2e-5
        curverr.append(abs(numeric-curv[i])/max(abs(curv[i]),1e-12))
    assert max(curverr)<1e-5
    stiff=Field(1e8,1.,32,length_kpc=1.)
    H=stiff.hessian(x,20,C)
    herrors=[]
    for i in (0,5,15,25,31):
        d=np.zeros(32);d[i]=1e-5
        fd=(stiff.energy_grad(x+d,20,C)[1]-stiff.energy_grad(x-d,20,C)[1])/(2e-5)
        herrors.append(np.linalg.norm(fd-H[:,i])/np.linalg.norm(H[:,i]))
    assert max(herrors)<1e-6
    # Direct data moment calculation, with uniform boosts and rotations.
    J=np.array([[0.,-2.,0.],[3.,0.,0.],[0.,0.,0.]])
    velocities=np.r_[np.eye(3)*3,-np.eye(3)*3]+[12.,-9.,4.]
    gl=np.array([1.,2.,0.]); H=np.diag([2.,-1.,.3])
    base=moment_C(J,velocities,gl,H)
    boosted=moment_C(J,velocities+[1000.,-400.,20.],gl,H)
    angle=.7
    Q=np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1]])
    rotated=moment_C(Q@J@Q.T,velocities@Q.T,Q@gl,Q@H@Q.T)
    assert max(abs(base-boosted),abs(base-rotated))<1e-12
    return dict(gradient_relative_error=max(errors),curvature_relative_error=max(curverr),
                stiffness_hessian_relative_error=max(herrors),
                endpoint_barrier_energy_change=Ebar-Eoff,
                boost_invariance_error=abs(base-boosted),rotation_invariance_error=abs(base-rotated),
                direct_rotational_gap_force_ratio_example=2.)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    ap.add_argument('--mode',choices=['scan','refine'],default='scan')
    args=ap.parse_args()
    check=checks(); rows=[]
    if args.mode=='scan':
        settings=[(64,f,beta,.999) for f in (0.,.3,.7,.95,.99) for beta in (0.,10.,20.,40.)]
    else:
        settings=[(n,f,20.,seed) for n in (128,256) for f,seed in ((.3,.999),(.95,.999),(.99,.999),(.99,.001))]
    for profile_index,(_,mass,b,_) in enumerate(PROFILES):
        for n,f,beta,seed in settings:
            row=Field(mass,b,n).evolve(f,beta,seed)
            row.update(profile_index=profile_index,baryon_mass_msun=mass,b_kpc=b)
            rows.append(row)
            print(json.dumps({k:row[k] for k in ('profile_index','n','f','beta','seed','tethered_mass_fraction','energy_receiver_balance_max','conditional_RAR_max_dex')}),flush=True)
    output=dict(checks=check,runs=rows,kinematics='same continuous streaming family applied to every mass/size profile',
                claim='effective interaction test; no microscopic derivation or live spatial evolution')
    Path(args.output).write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')


if __name__=='__main__': main()
