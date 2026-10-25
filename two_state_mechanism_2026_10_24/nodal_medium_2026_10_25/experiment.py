import argparse,json
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import brentq
from scipy.special import expit,logsumexp
CHI=11.220184543019636;F=CHI/(1+CHI)

def gammas():
    I=np.eye(2);sx=np.array([[0,1],[1,0]]);sy=np.array([[0,-1j],[1j,0]]);sz=np.diag([1,-1])
    return [np.kron(sx,I),np.kron(sy,I),np.kron(sz,sx),np.kron(sz,sy),np.kron(sz,sz)]

def occupation(r,t,mu):
    if t==0:return float(r>abs(mu))
    return expit((r+mu)/t)-expit((-r+mu)/t)

def response(e,t=0.,mu=0.):
    R=np.hypot(1,e)
    if t==0:return max(R-max(abs(e),abs(mu)),0.)
    def logc(r):return logsumexp([r/t,-r/t,mu/t,-mu/t])-np.log(2)
    return t*(logc(R)-logc(abs(e)))

def source(x,t=0.,mu=0.):
    e=x/F
    if t==0 and mu==0:return F*x*(e-e*e/(1+np.hypot(1,e)))
    return F*x*(1-response(e,t,mu))

def checks():
    gs=gammas();anti=max(np.linalg.norm(a@b+b@a-(2*np.eye(4) if i==j else 0)) for i,a in enumerate(gs) for j,b in enumerate(gs))
    eigerr=polerr=0.
    for u,v in [(.1,.2),(.7,-.3)]:
        for E in [np.array([.1,0,0]),np.array([.03,.04,.05])]:
            H=u*gs[0]+v*gs[1]-sum(E[i]*gs[i+2] for i in range(3))
            eig,V=np.linalg.eigh(H);r=np.sqrt(u*u+v*v+E@E)
            eigerr=max(eigerr,np.max(abs(eig-[-r,-r,r,r])))
            for t,mu in [(0,0),(.1,0),(.1,.2)]:
                occ=(eig<mu).astype(float) if t==0 else expit((mu-eig)/t)
                density=(V*occ)@V.conj().T
                pol=np.array([np.trace(density@g).real/2 for g in gs[2:]])
                polerr=max(polerr,np.linalg.norm(pol-E/r*occupation(r,t,mu)))
    integralerr=0.
    for e in [.001,.03,.7,3.]:
        for t,mu in [(0,0),(.001,0),(.1,0),(.1,.2)]:
            numerical=quad(lambda u:u/np.hypot(u,e)*occupation(np.hypot(u,e),t,mu),0,1,epsabs=1e-12)[0]
            integralerr=max(integralerr,abs(numerical-response(e,t,mu)))
    assert anti<1e-13 and eigerr<1e-13 and polerr<1e-12 and integralerr<1e-9
    return dict(clifford_error=float(anti),eigenvalue_error=float(eigerr),dipole_trace_error=float(polerr),response_quadrature_error=float(integralerr))

def dos_grid(N):
    a=(np.arange(N)+.5)*2/N-1
    xx,zz=np.meshgrid(a,a,indexing='ij');u=np.hypot(xx,zz);cell=(2/N)**2
    cdf=[dict(u=r,count_area=float(np.sum(u<r)*cell),exact_area=float(np.pi*r*r)) for r in [.2,.4,.6,.8,1.]]
    pol=[]
    for e in [.01,.1,.5]:
        numeric=np.sum(1/np.sqrt(u[u<1]**2+e*e))*cell/(2*np.pi)
        pol.append(dict(e=e,numerical=float(numeric),exact=response(e),relative_error=float(abs(numeric-response(e))/response(e))))
    return dict(N=N,cdf=cdf,polarization=pol)

def dynamic(N,D,rtol):
    nodes,w=np.polynomial.legendre.leggauss(N);u=(nodes+1)/2;w=w/2;n=CHI*u*w
    r=np.zeros((N,3));r[:,2]=-1
    def rhs(t,y):
        r=y.reshape(N,3);E=D-n@r[:,0]
        b=np.column_stack((-np.full(N,E),np.zeros(N),u))
        return (2*np.cross(b,r)).ravel()
    sol=solve_ivp(rhs,(0,10),r.ravel(),method='DOP853',rtol=rtol,atol=rtol*.01,t_eval=np.linspace(0,10,101))
    assert sol.success
    R=sol.y.T.reshape(-1,N,3);E=D-R[:,:,0]@n
    energy=E*E/2+(R[:,:,2]+1)@(n*u)
    return dict(N=N,D=D,rtol=rtol,max_relative_energy_error=float(max(abs(energy-energy[0]))/energy[0]),
                max_bloch_norm_error=float(np.max(abs(np.sum(R*R,axis=2)-1))),final_polarization=float(R[-1,:,0]@n))

def main(output):
    r=dict(checks=checks(),dos=[dos_grid(N) for N in [128,256,512]],dynamics=[],tolerances=[],mass_speed_caps=[])
    for N in [24,48]:
        for D in [.1,.5]:
            for tol in [1e-8,1e-11]:r['dynamics'].append(dynamic(N,D,tol))
    factor=10**.05
    for x in [1e-4,.001,.01,.1]:
        y=source(x)
        t=brentq(lambda t:source(x/factor,t)-y,0,10,xtol=1e-14)
        mu=brentq(lambda mu:source(x/factor,0,mu)-y,0,10,xtol=1e-14)
        r['tolerances'].append(dict(x=x,tau=float(t),mu_over_cutoff=float(mu)))
    G=6.67430e-11;A0=9.3603e-11;HB=1.054571817e-34;C=299792458.;KB=1.380649e-23;MS=1.98847e30;KP=3.085677581491367e19
    for eps in [.1,1e-8]:
        for M,b in [(3e5,.3),(1e8,1),(6e10,3),(1e14,300)]:
            rho=3*5.364*M*MS/(4*np.pi*(b*KP)**3)
            ell=(1+eps)*F*F*A0/(8*np.pi*G*rho)
            r['mass_speed_caps'].append(dict(epsilon=eps,Mb=M,b=b,ell_min_kpc=float(ell/KP),
                cutoff_over_kB_max_K=float(HB*C/(KB*ell)),
                thermal_ceiling_at_x001_K=float(r['tolerances'][2]['tau']*HB*C/(KB*ell))))
    with open(output,'w') as f:json.dump(r,f,indent=2,allow_nan=False)
    print(json.dumps(dict(checks=r['checks'],tolerances=r['tolerances'],caps=r['mass_speed_caps'],
      fine_energy_error=max(x['max_relative_energy_error'] for x in r['dynamics'] if x['rtol']==1e-11))))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
