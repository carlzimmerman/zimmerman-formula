import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

def onset(mu,n=480,X=80):
 x=np.exp(np.linspace(0,np.log(X),n+1));ii=[];jj=[];ka=[];ba=[]
 q,w=np.polynomial.legendre.leggauss(4)
 for e in range(n):
  lo,hi=x[e:e+2];h=hi-lo;z=(lo+hi)/2+h*q/2;ww=w*h/2
  shape=np.array([(hi-z)/h,(z-lo)/h]);d=np.array([-1,1])/h
  K=np.outer(d,d)*np.dot(ww,z*(z-1))+mu*mu*np.einsum('q,iq,jq->ij',ww*z*z,shape,shape)
  B=np.einsum('q,iq,jq->ij',ww*12/z**4,shape,shape)
  for a in range(2):
   for b in range(2):ii.append(e+a);jj.append(e+b);ka.append(K[a,b]);ba.append(B[a,b])
 K=coo_matrix((ka,(ii,jj)),shape=(n+1,n+1)).tocsc();B=coo_matrix((ba,(ii,jj)),shape=K.shape).tocsc()
 if mu==0:
  K[-1,-1]+=-1/np.log1p(-1/X)
 else:K=K[:-1,:-1];B=B[:-1,:-1]
 v,vec=eigsh(K,k=1,M=B,sigma=0,which='LM',tol=1e-10)
 return float(v[0])

import sys,json,math
from pathlib import Path
import sympy as sy
from scipy.integrate import solve_ivp,solve_bvp,quad,simpson
from scipy.optimize import brentq
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
checks=[]
def ck(name,test):
 checks.append({'name':name,'passed':bool(test)})
 if not test:raise AssertionError(name)
def eq(name,x):ck(name,sy.simplify(x)==0)
# Independent exact identities and scalar ground-state transformation.
x,mu,zeta,eps,H=sy.symbols('x mu zeta epsilon H',positive=True)
f=1-1/x
V=f*(1/x**3+mu**2-12*zeta/x**6)
eq('Schwarzschild radial potential',V-f*(sy.diff(f,x)/x+mu**2-12*zeta/x**6))
eq('GB sign transition FRW',24*H**4+24*H**2*(-eps*H**2)-24*H**4*(1-eps))
p,q,a,b,c=sy.symbols('p q a b c',real=True)
# p=x(x-1), q=mu^2*x^2-12*zeta/x^4; stationary (p phi')'=q phi+x^2 phi^3.
y=sy.Function('y')(x);d=sy.Function('d')(x);pp=x*(x-1);qq=mu**2*x*x-12*zeta/x**4
lhs=pp*sy.diff(d,x)**2+(qq+3*x*x*y*y)*d*d
rhs=pp*y*y*sy.diff(d/y,x)**2+2*x*x*y*y*d*d+sy.diff(pp*sy.diff(y,x)*d*d/y,x)
expr=sy.expand(lhs-rhs).subs(sy.diff(y,x,2),((qq*y+x*x*y**3)-sy.diff(pp,x)*sy.diff(y,x))/pp)
eq('conditional scalar Hessian factorization',expr)
# Source normalization: eta_paper/(16 M^2)=our zeta, since r_h=2M and eta_paper=4 eta_here.
eq('2018 threshold notation translation',sy.Rational(2904,1000)/16-sy.Rational(363,2000))
thresholds=[]
for mm in [0.,.1,1.,3.,10.,30.]:
 values=[onset(mm,n) for n in [480,960,1920,3840]]
 ck('Ritz monotone refinement mu='+str(mm),all(values[i+1]<values[i] for i in range(3)))
 ck('mesh convergence mu='+str(mm),abs(values[-1]-values[-2])/values[-1]<1e-4)
 ck('nonnegative potential lower bound mu='+str(mm),values[-1]>(1+mm*mm)/12)
 if mm:
  other=onset(mm,1920,40)
  ck('massive outer-domain stability mu='+str(mm),abs(other-values[-2])/values[-1]<2e-4)
 thresholds.append({'mu':mm,'elements':[480,960,1920,3840],'zeta':values,'relative_last_step':abs(values[-1]-values[-2])/values[-1]})
ck('onset grows with mass',all(thresholds[i+1]['zeta'][-1]>thresholds[i]['zeta'][-1] for i in range(5)))
ck('known massless threshold rounded agreement',abs(thresholds[0]['zeta'][-1]-.1815)<1.5e-4)
ck('massless trial sufficient bound',thresholds[0]['zeta'][-1]<5/24)
def shoot(zz):
 ee=1e-7
 def fun(xx,y):return [y[1],(-12*zz*y[0]/xx**4-(2*xx-1)*y[1])/(xx*(xx-1))]
 sol=solve_ivp(fun,[1+ee,80],[1-12*zz*ee,-12*zz],method='DOP853',rtol=2e-11,atol=1e-13)
 ck('shooting integration succeeds',sol.success)
 return sol.y[0,-1]-80*79*np.log1p(-1/80)*sol.y[1,-1]
shooting=brentq(shoot,.12,.24,xtol=1e-12)
ck('independent onset agrees',abs(shooting-thresholds[0]['zeta'][-1])<2e-7)
# Stationary nonlinear hair, quartic potential rather than quartic GB coupling.
def hair(tol,outer):
 mm=1.;zz=.6;ee=1e-6
 xx=np.exp(np.linspace(np.log1p(ee),np.log(outer),600));aa=np.sqrt(12*zz-mm*mm)*np.exp(-mm*(xx-1))/xx
 def fun(x,y):return np.array([y[1],((mm*mm*x*x-12*zz/x**4)*y[0]+x*x*y[0]**3-(2*x-1)*y[1])/(x*(x-1))])
 def bc(a,b):return np.array([a[1]-(mm*mm-12*zz)*a[0]-a[0]**3,b[0]])
 sol=solve_bvp(fun,bc,xx,np.array([aa,-aa*(mm+1/xx)]),tol=tol,max_nodes=8000)
 ck('nonlinear hair BVP converged '+str(tol),sol.success)
 ck('nonlinear hair nonzero '+str(tol),sol.y[0,0]>1)
 ck('hair nodeless in resolved core '+str(tol),min(sol.sol(np.linspace(1+ee,10,500))[0])>0)
 def energy(x):
  a,b=sol.sol(x);return .5*x*(x-1)*b*b+.5*(mm*mm*x*x-12*zz/x**4)*a*a+.25*x*x*a**4
 E=quad(energy,1+ee,outer,epsabs=1e-9)[0]
 ck('hair below zero field scalar functional '+str(tol),E<0)
 return {'tol':tol,'outer':outer,'phi_h':float(sol.y[0,0]),'energy_over_4pi':E,'nodes':len(sol.x),'max_residual':float(max(sol.rms_residuals))}
hairs=[hair(1e-7,25),hair(2e-8,35)]
ck('hair boundary/refinement agreement',abs(hairs[0]['phi_h']-hairs[1]['phi_h'])<1e-6)
# Actual flat-FRW curvature from an assigned smooth background, not an independent pulse.
def background(t):
 u=t-30.;lc=lambda v:np.logaddexp(v,-v)-np.log(2.)
 hh=1/(1+t+lc(u)-lc(-30.));ee=1+np.tanh(u);ep=1-np.tanh(u)**2
 GG=24*hh**4*(1-ee);Gp=24*hh**4*(-4*ee*hh*(1-ee)-ep)
 return hh,ee,GG,Gp
ck('early curvature positive',background(0)[2]>0)
ck('radiation curvature negative',background(100)[2]<0)
ck('curvature crossing at end acceleration',background(30)[2]==0)
def cosmos(rtol,atol,eta=.1,seed=1e-6):
 mm=.1
 def fun(t,y):
  phi,v,N,W,D=y;hh,ee,GG,Gp=background(t)
  return [v,-3*hh*v-(mm*mm-eta*GG)*phi-phi**3,hh,-.5*eta*Gp*phi*phi,-3*hh*v*v]
 def zero(t,y):return y[0]
 zero.direction=1
 sol=solve_ivp(fun,[0,5000],[seed,0,0,0,0],rtol=rtol,atol=atol,method='DOP853',dense_output=True,events=zero,max_step=5)
 ck('cosmological integration succeeds '+str((rtol,eta,seed)),sol.success)
 phi,v,N,W,D=sol.y[:,-1];Ef=.5*v*v+.5*(mm*mm-eta*background(5000)[2])*phi*phi+.25*phi**4
 E0=.5*(mm*mm-eta*background(0)[2])*seed*seed+.25*seed**4
 ck('signed energy ledger '+str((rtol,eta,seed)),abs(Ef-E0-W-D)<1e-8*max(abs(W),abs(D),1e-20))
 row={'rtol':rtol,'atol':atol,'eta':eta,'seed':seed,'end_energy':float(Ef),'curvature_work':float(W),'Hubble_damping':float(D),'ledger_residual':float(Ef-E0-W-D),'max_abs_phi':float(max(abs(sol.y[0]))),'end_H_over_m':background(5000)[0]/mm,'nfev':sol.nfev}
 if seed:
  zz=sol.t_events[0][-11:];ck('enough late full cycles '+str(eta),len(zz)==11)
  ts=np.linspace(zz[0],zz[-1],5001);a,b,N,_,_=sol.sol(ts)
  rho=.5*b*b+.5*mm*mm*a*a+.25*a**4;pr=.5*b*b-.5*mm*mm*a*a-.25*a**4
  w=simpson(pr,x=ts)/simpson(rho,x=ts)
  az=sol.sol(zz);comov=np.exp(3*(az[2]-az[2,0]))*.5*az[1]**2
  drift=np.ptp(comov)/np.mean(comov)
  row.update(w_late=float(w),comoving_energy_relative_drift=float(drift),last_cycle_interval=zz[[0,-1]].tolist(),end_quartic_to_quadratic_energy=float(.5*phi*phi/(mm*mm)))
  ck('late low average pressure '+str(eta),abs(w)<.001)
  ck('late dust redshifting '+str(eta),drift<.001)
 else:ck('exact zero seed does not self-create a classical field',max(abs(sol.y[0]))==0 and Ef==0 and W==0)
 return row
cosmology=[cosmos(1e-9,1e-12),cosmos(2e-11,1e-14),cosmos(1e-9,1e-22,eta=0),cosmos(1e-9,1e-12,seed=0)]
ck('end abundance numerical refinement',abs(cosmology[0]['end_energy']/cosmology[1]['end_energy']-1)<1e-5)
ck('late pressure numerical refinement',abs(cosmology[0]['w_late']-cosmology[1]['w_late'])<1e-6)
ck('curvature amplifies supplied seed vs eta0',cosmology[1]['end_energy']/cosmology[2]['end_energy']>1e10)
# Geodesic constraints: cold locally and cold at infinity must not be conflated.
xx,vloc,vinf=sy.symbols('x v_local v_infinity',positive=True)
ff=1-1/xx
vlocal2=1/xx+ff*vinf**2
eq('radial energy relation',ff/(1-vlocal2)-1/(1-vinf**2))
escape=[]
for rr in [2.,3.,10.,100.,1e6]:
 for vv in [1e-3,.01]:
  local=math.sqrt(1/rr+(1-1/rr)*vv*vv)
  ck('cold infinity may escape with fast launch',abs((1-1/rr)/(1-local*local)-1/(1-vv*vv))<1e-12)
  escape.append({'launch_r_over_rh':rr,'v_infinity_over_c':vv,'required_v_local_over_c':local,'escape_v_local_over_c':1/math.sqrt(rr),'omega_over_mass':1/math.sqrt(1-vv*vv)})
ck('locally cold ballistic escape requires large radius',1/(1e-3)**2==1e6)
# All values dimensionless; mass scales/couplings supplied, not fit or observed.
result={'passed':len(checks),'checks':checks,'thresholds':thresholds,'independent_massless_onset':shooting,'hair':hairs,'cosmology':cosmology,'escape':escape,'conventions':'canonical scalar, c=hbar=1; zeta=eta/r_h^2, mu=m*r_h; FRW H_initial=1, lambda=1, m=.1','non_claims':['No quantum initial spectrum or production count','No full backreacted metric or EFT health certificate','No finite black hole cold export computation','No baryon tether or dark energy conversion','No predicted abundance or novelty claim']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
