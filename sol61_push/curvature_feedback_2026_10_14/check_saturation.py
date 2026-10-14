import json,sys,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import brentq
from scipy.integrate import simpson
from background import evolve,detail,rhs
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
checks=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def eq(n,v):ck(n,s.simplify(v)==0)
p,m2,eta,sc=s.symbols('phi mass_squared eta scale',positive=True)
U=m2*p*p/2;F=eta*sc*sc*(1-s.exp(-p*p/(sc*sc)))/2;H2=U/3
fp=s.diff(F,p);fpp=s.diff(F,p,2);etads=m2*s.exp(p*p/(sc*sc))/(24*H2*H2)
C=s.diff(U,p,2)-24*fpp*H2**2-384*fp*fp*H2**3
Z=1+96*fp*fp*H2**2
Cds=s.simplify(C.subs(eta,etads));Zds=s.simplify(Z.subs(eta,etads))
eq('saturating coupling derivative',fp-eta*p*s.exp(-p*p/sc**2))
eq('general coupled restoring coefficient',Cds-2*m2*(p*p/sc**2-2))
eq('positive de Sitter homogeneous kinetic',Zds-(1+6/p**2))
y=s.symbols('y',positive=True)
eq('stable branch mass gap',s.simplify((Cds/(Zds*H2)).subs(p,sc*s.sqrt(y)))-12*(y-2)/(sc*sc*y+6))
eq('fixed point coupling relation',(etads*m2*sc**4).subs(p,sc*s.sqrt(y))-3*s.exp(y)/(2*y*y))
eq('branch merger at y2',s.diff(y*y*s.exp(-y),y).subs(y,2))
# Independent effective-potential check: paper uses -F G and U_paper=M_P^2/2.
Ve=-1/(4*U)-2*F/3
eq('effective potential stationarity',s.diff(Ve,p).subs(eta,etads))
eq('effective potential stability matches C',s.diff(Ve,p,2).subs(eta,etads)-Cds/(4*U*U))
# General power-law obstruction is avoided because the saturating coupling is not a positive monomial.
a,n,b,q=s.symbols('a n b q',positive=True);V=a*p**n;G=b*p**q
Cg=s.diff(V,p,2)-s.diff(G,p,2)/s.diff(G,p)*s.diff(V,p)-2*s.diff(V,p)**2/V
eq('positive monomial U and F obstruction',Cg+n*(n+q)*V/p**2)
eta4=3*np.exp(4)/(2*.01*16);target=16*np.exp(-4)
low=brentq(lambda yy:yy*yy*np.exp(-yy)-target,1e-6,1.999)
ck('two distinct branches',0<low<2<4)
fixed=[]
for pp in [1.98,2.02]:
 sol,row=evolve(lam=0,eta=eta4,scale=1,phi=pp,inflaton=0,end=1000,rtol=2e-10,atol=1e-13)
 ck('nonlinear return to stable branch '+str(pp),row['termination']=='end time' and abs(row['end_phi']-2)<1e-7)
 ck('de Sitter Hubble target '+str(pp),abs(row['end_H']/math.sqrt(.04/6)-1)<1e-7)
 ck('perturbed stable branch tensor screen '+str(pp),min(row['min_QT'],row['min_FT'])>.9)
 ck('stable branch constraint '+str(pp),row['max_Friedmann_relative_residual']<1e-9)
 fixed.append(row)
sol,cold=evolve(lam=0,eta=eta4,scale=1,phi=.02,inflaton=0,end=5000,rtol=2e-10,atol=1e-13)
ck('same action has a cold low-field basin',cold['termination']=='end time' and min(cold['min_QT'],cold['min_FT'])>.9)
ck('cold basin not automatically the de Sitter basin',cold['end_H']<.01*math.sqrt(.04/6) and abs(cold['end_phi'])<.02)
ts=np.linspace(4000,5000,8001);a=sol.sol(ts)[0];roots=[]
for i in range(len(ts)-1):
 if a[i]<0<=a[i+1]:roots.append(brentq(lambda t:sol.sol(t)[0],ts[i],ts[i+1]))
z=roots[-11:];ck('cold basin full cycles',len(z)==11)
t=np.linspace(z[0],z[-1],5001);p0,v,_,_,_,_,N=sol.sol(t);rho=.5*v*v+.005*p0*p0;pressure=.5*v*v-.005*p0*p0
cold['cycle_w']=float(simpson(pressure,x=t)/simpson(rho,x=t))
ck('cold basin low average pressure',abs(cold['cycle_w'])<.001)
_,rejected=evolve(lam=0,eta=eta4,scale=1,phi=.2,inflaton=0,end=100)
ck('intermediate initial amplitude fails tensor screen',rejected['termination']=='initial tensor screen fails')
# Test formation rather than inferring it from endpoint stability.
formation=[];hist=None
for scale in [.5,1.,2.,3.,5.,10.]:
 ee=eta4/scale**4
 ss,row=evolve(lam=0,eta=ee,scale=scale,end=1000,rtol=2e-10,atol=1e-13)
 ck('formation numerical integration '+str(scale),row['success'])
 ck('formation constraint '+str(scale),row['max_Friedmann_relative_residual']<1e-6)
 if scale<10:
  ck('formation encounters tensor gradient boundary '+str(scale),row['termination']=='tensor gradient zero')
  state=ss.y[:,-1];vel=np.array(rhs(ss.t[-1],state,0,ee,scale));dt=1e-6
  slope=(detail(state+dt*vel,0,ee,scale)[3]-detail(state-dt*vel,0,ee,scale)[3])/(2*dt)
  row['FT_directional_slope_at_boundary']=float(slope)
  ck('boundary crosses toward negative gradient '+str(scale),slope<0)
 else:
  ck('weak coupling trajectory reaches end',row['termination']=='end time')
  ck('weak coupling trajectory misses upper branch',abs(row['end_phi'])<.1*2*scale)
 if scale==1:
  tt=np.linspace(0,ss.t[-1],2001);yy=ss.sol(tt);vv=np.array([detail(a,0,ee,scale) for a in yy.T]);hist={'time':tt.tolist(),'phi':yy[0].tolist(),'QT':vv[:,2].tolist(),'FT':vv[:,3].tolist(),'H':yy[5].tolist()}
 formation.append(row)
# Refine the v1 first gradient crossing.
_,ref=evolve(lam=0,eta=eta4,scale=1,end=1000,rtol=2e-12,atol=1e-15)
ck('refined formation hits same boundary',ref['termination']=='tensor gradient zero')
ck('gradient boundary time refinement',abs(ref['end_time']-formation[1]['end_time'])<1e-5)
damped=[]
for rate in [.1,1.,10.,100.]:
 _,row=evolve(lam=0,eta=eta4,scale=1,end=1000,rtol=2e-10,atol=1e-13,damping=rate)
 ck('damped conserved constraint '+str(rate),row['max_Friedmann_relative_residual']<1e-6)
 ck('tested damping does not remove boundary '+str(rate),row['termination']=='tensor gradient zero')
 damped.append(row)
# At the endpoint m_eff/H cannot be both enormous and supplied by an order-one y.
scales=[]
for yy in [3.,4.,10.,100.]:
 for vv in [.01,.1,1.,10.]:
  ratio=12*(yy-2)/(vv*vv*yy+6)
  ck('mass gap bound y='+str((yy,vv)),ratio<2*(yy-2))
  scales.append({'y':yy,'scale_over_MP':vv,'mass_gap_squared_over_H_squared':ratio,'log_eta_m_squared_scale4_over_MP4':math.log(1.5)+yy-2*math.log(yy)})
result={'passed':len(checks),'checks':checks,'eta_at_v1':eta4,'lower_branch_y':low,'upper_branch_y':4,'fixed_point_returns':fixed,'cold_basin':cold,'rejected_initial':rejected,'formation':formation,'refined_crossing':ref,'damping':damped,'mass_gap_examples':scales,'scope':'Different saturating-coupling action with quadratic potential. Stable homogeneous endpoint and positive tensor coefficients there do not prove a healthy trajectory or all scalar perturbations. Finite formation scans do not exclude other initial conditions/couplings. No derived baryon tether or measured DE scale.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'gradient_history.json').write_text(json.dumps(hist)+'\n');print(json.dumps(result,indent=2))
