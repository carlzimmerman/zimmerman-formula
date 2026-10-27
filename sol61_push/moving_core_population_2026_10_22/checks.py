import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import minimize_scalar,brentq
import sympy as s
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v,flush=True)
r,b,M,G,beta=s.symbols('r b M G beta',positive=True)
rho=3*M*b*b/(4*s.pi*(r*r+b*b)**s.Rational(5,2));phi=-G*M/s.sqrt(r*r+b*b);sig=beta*G*M/(6*s.sqrt(r*r+b*b));mass=M*r**3/(r*r+b*b)**s.Rational(3,2)
ck('Poisson',s.simplify(s.diff(r*r*s.diff(phi,r),r)/r**2-4*s.pi*G*rho)==0,'Plummer')
ck('mass_integral_derivative',s.simplify(s.diff(mass,r)-4*s.pi*r*r*rho)==0,'M(<r)')
ck('Jeans',s.simplify(s.diff(rho*sig,r)+rho*beta*s.diff(phi,r))==0,'isotropic')
# Independent velocity integration in units G=M=b=1, several beta and radii.
maxerr=0
for bet in [.1,.7,1]:
 for rr in [0.,.1,1,10]:
  psi=bet/np.sqrt(1+rr*rr);coeff=24*np.sqrt(2)/(7*np.pi**3*bet**5)
  val=4*np.pi*quad(lambda v:v*v*coeff*max(psi-v*v/2,0)**3.5,0,np.sqrt(2*psi),epsabs=1e-12)[0]
  target=3/(4*np.pi*(1+rr*rr)**2.5);maxerr=max(maxerr,abs(val/target-1))
ck('positive_DF_normalization_12',maxerr<1e-7,maxerr)
for R in [.1,1,10]:
 sigproj=2*quad(lambda z:3/(4*np.pi*(1+R*R+z*z)**2.5),0,np.inf,epsabs=1e-12)[0]
 ck('projection_'+str(R),abs(sigproj*np.pi*(1+R*R)**2-1)<1e-8,sigproj)

root=Path('campaign_fresh_gravity/CFG687_erass1_shear_stack');d=np.load(root/'cfg687_percluster.npz');ref=json.loads((root/'cfg687_results.json').read_text())
D=np.nan_to_num(d['D']);E=d['E'];W=np.where(np.isfinite(E)&(E>0),1/E**2,0);n=len(D);R=np.sqrt(np.geomspace(.15,3,9)[:-1]*np.geomspace(.15,3,9)[1:]);bands={'INNER':[0,1,2],'MID':[3,4,5],'OUTER':[6,7]};patch=np.empty(n,int);patch[np.argsort(d['ra'])]=np.arange(n)*30//n
all_=np.ones(n,bool)
def amp(pred,sel):return {k:float(np.sum(W[sel][:,j]*D[sel][:,j])/np.sum(W[sel][:,j]*pred[sel][:,j])) for k,j in bands.items()}
ck('baseline',max(abs(v-ref['A']['canonical|b0.67|rc0.15|f0.20'][k][0]) for k,v in amp(d['PL'],all_).items())<1e-12,'cached canonical baseline')
clusters=[]
for bn in ['PN','PL']:
 base=d[bn]
 for kind in ['common','gas_R500']:
  masses=np.ones(n)*1e13 if kind=='common' else d['mg'];sizes=np.ones(n) if kind=='common' else d['R500'];bounds=np.log([.01,3 if kind=='common' else 5])
  def template(logb):
   bb=np.exp(logb)*sizes
   return masses[:,None]*R[None,:]**2/(np.pi*(R[None,:]**2+bb[:,None]**2)**2)/1e12
  def fit(sel,data=D):
   wt=W[sel].sum(axis=0);res=np.sum(W[sel]*(data-base)[sel],axis=0)/wt
   def calc(logb,full=False):
    t=np.sum(W[sel]*template(logb)[sel],axis=0)/wt;j=slice(3,6)
    q=max(0,float(np.sum(wt[j]*res[j]*t[j])/np.sum(wt[j]*t[j]**2)))
    score=float(np.sum(wt[j]*(res[j]-q*t[j])**2))
    return (q,score) if full else score
   # Scan first to avoid an unexamined multimodal scalar optimizer.
   grid=np.linspace(*bounds,70);scores=[calc(z) for z in grid];i=int(np.argmin(scores));lo=grid[max(0,i-1)];hi=grid[min(len(grid)-1,i+1)]
   opt=minimize_scalar(calc,bounds=(lo,hi),method='bounded',options={'xatol':1e-8});lb=float(opt.x);q,score=calc(lb,True)
   return q,lb,score
  q,lb,score=fit(all_);A=amp(base+q*template(lb),all_);reps=[]
  for j in range(30):
   sel=patch!=j;qq,ll,_=fit(sel);reps.append(amp(base+qq*template(ll),sel))
  err={k:float(np.sqrt(29/30*np.sum((np.array([v[k] for v in reps])-np.mean([v[k] for v in reps]))**2))) for k in bands}
  masspop=q*masses;sizepop=np.exp(lb)*sizes
  # mcore and rcore are inherited fitted dwarf state, not predictions.
  mcore=1.0949998667344883e7;rcore=.0003214846542759978 # Mpc
  N=masspop/mcore;fill=N*(rcore/sizepop)**3
  Gmpc=4.30091727e-9 # Mpc (km/s)^2 / Msun
  dispersion=np.sqrt(Gmpc*masspop/(6*sizepop));vrel=4*dispersion/np.sqrt(np.pi)
  ncentral=3*N/(4*np.pi*sizepop**3);cross=np.pi*(2*rcore)**2
  # 1 km/s = .001022712 Mpc/Gyr
  overlap=1/(ncentral*cross*vrel*.001022712165)
  clusters.append(dict(baseline=bn,prescription=kind,q=q,b_parameter=float(np.exp(lb)),boundary=bool(min(abs(lb-bounds[0]),abs(lb-bounds[1]))<1e-4),MID_score_not_likelihood=score,mass_median=float(np.median(masspop)),b_median_Mpc=float(np.median(sizepop)),N_median=float(np.median(N)),filling_median=float(np.median(fill)),max_radial_tide_over_self_median=float(np.median(2/2.5**2.5*fill)),overlap_time_central_Gyr_median=float(np.median(overlap)),central_sigma_kms_median=float(np.median(dispersion)),bands={k:dict(A=A[k],sigma=err[k],Z=(A[k]-1)/err[k]) for k in bands}))
  # Interior injected profile with fixed known q and scale; same estimator.
  qi,li,_=fit(all_,base+2*template(np.log(.4)))
  ck('injection_'+bn+'_'+kind,abs(qi/2-1)<1e-5 and abs(np.exp(li)/.4-1)<1e-5,[qi,float(np.exp(li))])

fb=1/6.364;fc=1-fb;N0=-np.log(1101.)
def growth(beta_,sig0,k,tol):
 def fun(N,Y):
  aa=np.exp(N);B,Bp,C,Cp=Y;grav=1.5*(fb*B+fc*C);pressure=(k*sig0/70)**2/aa
  return [Bp,-.5*Bp+grav,Cp,-.5*Cp+beta_*grav-pressure*C]
 ai=np.exp(N0);sol=solve_ivp(fun,(N0,0),[ai]*4,rtol=tol,atol=tol*1e-5,method='DOP853');assert sol.success
 return float(fb*sol.y[0,-1]+fc*sol.y[2,-1])
grows=[]
for bet in [1.,.999,.99,.9]:
 for sig0 in [0.,.1,1.]:
  for k in [.1,1.]:
   val=growth(bet,sig0,k,1e-10);v2=growth(bet,sig0,k,1e-8);grows.append(dict(beta=bet,sigma0_kms=sig0,k_Mpc=k,amplitude=val,repeat_error=abs(val-v2)))
ck('growth_repeat_24',max(v['repeat_error'] for v in grows)<1e-7,max(v['repeat_error'] for v in grows))
ck('dust_growth',abs(growth(1,0,1,1e-11)-1)<1e-9,growth(1,0,1,1e-11))
beta99=brentq(lambda v:growth(v,0,1,1e-10)-.99,.9,1)
# Exact fixed-matrix solution independently checks numerical pressureless history.
from scipy.linalg import expm
bet=.9;mat=np.array([[0,1,0,0],[1.5*fb,-.5,1.5*fc,0],[0,0,0,1],[1.5*bet*fb,0,1.5*bet*fc,-.5]])
Y=expm(-N0*mat)@np.ones(4)*np.exp(N0);exact=fb*Y[0]+fc*Y[2]
ck('growth_matrix_exponential',abs(exact-growth(bet,0,1,1e-11))<1e-9,exact)
# Mass conservation and compensated discreteness normalization.
GSI=6.67430e-11;Mpc=3.085677581491367e22;Msun=1.98847e30;H0=70e3/Mpc;rhoc=.25*3*H0**2/(8*np.pi*GSI)*Mpc**3/Msun;mc=1.0949998667344883e7;nc=rhoc/mc;rlag=(3*mc/(4*np.pi*rhoc))**(1/3)
inv=dict(Omega_c_input=.25,H0_input=70,rhoc_Msun_Mpc3=rhoc,mcore_Msun=mc,n_if_all_cores_Mpc3=nc,mean_spacing_Mpc=nc**(-1/3),Lagrangian_radius_Mpc=rlag,beta_99retention=beta99,inertial_excess_fraction_max=1/beta99-1)
# Exact top-hat small-k expansion: a compensated local rearrangement has k^4 power.
z=s.symbols('z');win=3*(s.sin(z)-z*s.cos(z))/z**3
ck('compensated_shot_noise',s.limit((1-win)**2/z**4,z,0)==s.Rational(1,100),'P=F*m/rhoc*(1-W)^2; small k^4')
out=dict(checks=checks,clusters=clusters,growth=grows,inventory=inv)
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(clusters=clusters,inventory=inv),indent=2));raise SystemExit(0 if all(v['passed'] for v in checks) else 1)
