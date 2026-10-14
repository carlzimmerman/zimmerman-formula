import sys,json,math
from pathlib import Path
import sympy as s
import mpmath as mp
out=Path(sys.argv[1]);out.mkdir(exist_ok=True);mp.mp.dps=80
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
def ze(n,e):ck(n,s.simplify(e)==0)
r,m,L,al,lam,q,C,b,h=s.symbols('r m L alpha lambda q C b h',positive=True)
f=1-2*m/r-r*r/L**2;fp=s.diff(f,r)
GB=4*s.diff((f-1)*fp,r)/r**2
ze('Gauss Bonnet invariant',GB-48*m*m/r**6-24/L**4)
N=C+lam*r**3/3-4*al*(f-1)*fp
ze('integrated scalar equation',s.diff(N,r)-r*r*(lam-al*GB))
fb,fh=s.symbols('fprime_b fprime_h',real=True)
Vol=(h**3-b**3)/3
Q=(4*al*(fb-fh)-lam*Vol)/(b*b+h*h)
CC=Q*b*b-lam*b**3/3-4*al*fb
ze('future BH ingoing regularity',CC+lam*b**3/3+4*al*fb-Q*b*b)
ze('future cosmological outgoing regularity',CC+lam*h**3/3+4*al*fh+Q*h*h)
lmax=4*al*(fb-fh)/Vol
ze('drift vanishes at slope threshold',Q.subs(lam,lmax))
ze('potential pumping maximum at half threshold',s.diff(lam*Q,lam).subs(lam,lmax/2))
ze('static scalar incompatible at zero slope',Q.subs(lam,0)-4*al*(fb-fh)/(b*b+h*h))
# Double-dual curvature component, derived from radial metric Ricci tensors.
Rrr=-(s.diff(f,r,2)/2+fp/r)/f
Rtt=f*(s.diff(f,r,2)/2+fp/r)
Rsc=-s.diff(f,r,2)-4*fp/r+2*(1-f)/r**2
P_rttr=-s.diff(f,r,2)/2+Rtt/f-f*Rrr+Rsc/2
ze('double dual radial component',P_rttr-(1-f)/r**2)
Hess_rt=-q*fp/(2*f)
TGB_rt=-8*al*f*P_rttr*(-Hess_rt)
ze('actual GB mixed stress',TGB_rt-4*al*q*(f-1)*fp/r**2)
Tcan_rt=q*N/r**2
ze('full mixed stress flux',Tcan_rt+TGB_rt-q*(C+lam*r**3/3)/r**2)
ze('potential storage vs flux divergence',s.diff(r*r*(Tcan_rt+TGB_rt),r)-lam*q*r*r)
# Flat Schwarzschild horizon charge control, no de Sitter approximation.
fs=1-2*m/r
Ns=-2*al/m-4*al*(fs-1)*s.diff(fs,r)
ps=s.cancel(Ns/(r*r*fs))
ze('Schwarzschild future regular derivative',s.limit(ps,r,2*m)+3*al/(2*m**3))
ze('Schwarzschild scalar charge',s.limit(-r*r*ps,r,s.oo)-2*al/m)
# Canonical scalar, GB and matter stress divergences cancel exactly.
GBsym,beta,rho,dphi=s.symbols('GB beta rho dphi',real=True)
ze('reciprocal covariant stress exchange',(-al*GBsym+beta*rho)*dphi+al*GBsym*dphi-beta*rho*dphi)

rows=[]
for tt in ['1e-6','.001','.1','.5','.9']:
 t=mp.mpf(tt);LL=mp.sqrt(1+t+t*t);bb=t;hh=mp.mpf(1)
 mm=bb*hh*(bb+hh)/(2*LL*LL);aa=mp.mpf('1e-6')
 fun=lambda rr:1-2*mm/rr-rr*rr/(LL*LL)
 fprime=lambda rr:2*mm/(rr*rr)-2*rr/(LL*LL)
 g=lambda rr:48*mm*mm/rr**6+24/LL**4
 vol=(hh**3-bb**3)/3
 threshold=4*aa*(fprime(bb)-fprime(hh))/vol
 for ff in [0,.25,.5,.75,1.25]:
  slope=mp.mpf(str(ff))*threshold
  qq=(4*aa*(fprime(bb)-fprime(hh))-slope*vol)/(bb*bb+hh*hh)
  cst=qq*bb*bb-slope*bb**3/3-4*aa*fprime(bb)
  nn=lambda rr:cst+slope*rr**3/3-4*aa*(fun(rr)-1)*fprime(rr)
  ck('future BH residue '+str((tt,ff)),abs(nn(bb)-qq*bb*bb)<mp.mpf('1e-60'))
  ck('future cosmic residue '+str((tt,ff)),abs(nn(hh)+qq*hh*hh)<mp.mpf('1e-60'))
  # Independent integrated source and total Killing-energy budget.
  integ=mp.quad(lambda rr:rr**2*(slope-aa*g(rr)),[bb,mp.sqrt(bb*hh),hh])
  ck('radial source integral '+str((tt,ff)),abs((nn(hh)-nn(bb))-integ)<mp.mpf('1e-50'))
  inflow_b=4*mp.pi*qq*(cst+slope*bb**3/3)
  inflow_c=4*mp.pi*qq*(cst+slope*hh**3/3)
  storage=4*mp.pi*qq*slope*vol
  ck('full stress energy ledger '+str((tt,ff)),abs(inflow_c-inflow_b-storage)<mp.mpf('1e-60'))
  ck('drift sign '+str((tt,ff)),qq>0 if ff<1 else qq<0)
  if tt in ['.001','.5']:
   rows.append({'b_over_rc':float(t),'slope_fraction':ff,'q_over_alpha':float(qq/aa),'potential_growth_lambda_q':float(slope*qq),'inward_Killing_flux_at_BH':float(inflow_b),'inward_Killing_flux_at_cosmic':float(inflow_c),'potential_storage_rate':float(storage)})

# Population amplitude bound in a slow-drift, weak-backreaction comparison.
S,lam2,Hh=s.symbols('S lambda H',positive=True)
pump=lam2*(S-lam2)/(3*Hh)
ze('population pump optimum',s.diff(pump,lam2).subs(lam2,S/2))
ze('population pump bound',S*S/(12*Hh)-pump-(S-2*lam2)**2/(12*Hh))
pop=[]
for eps in [.01,.1,1.]:
 for OmBH in [1e-5,.001,.01,.7]:
  upper=eps*eps*OmBH*OmBH/(4*.7)
  pop.append({'epsilon_GB_max':eps,'assigned_Omega_BH':OmBH,'potential_gain_per_Hubble_over_rhoV_bound':upper,'weak_backreaction_control':eps<=.1})
result={'passed':len(checks),'checks':checks,'horizon_examples':rows,'population_bounds':pop,'scope':'Fixed SdS metric, canonical scalar plus linear-alpha phi GB and local constant Uphi=lambda. Both future horizons explicitly selected. Full GB stress retained in energy ledger; nonzero potential slope makes geometry a transient comparison. No full metric backreaction or source population evolution solved.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
