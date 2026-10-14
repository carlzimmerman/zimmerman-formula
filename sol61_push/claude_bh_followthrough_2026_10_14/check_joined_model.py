import json,sys,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
def ze(n,e):ck(n,s.simplify(e)==0)
# Exact local-vacuum transfer check, in c=1 Cartesian rest coordinates.
t,x,S0,d,k=s.symbols('t x S0 delta k',positive=True)
source=S0*(1+d*s.cos(k*x)); Q0=-source; Qx=0
curl=s.diff(Q0,x)-s.diff(Qx,t)
ze('purely temporal inhomogeneous vacuum transfer not closed',curl-S0*d*k*s.sin(k*x))
V=t*source; fullQ0=-s.diff(V,t);fullQx=-s.diff(V,x)
ze('gradient-completed exchange is closed',s.diff(fullQ0,x)-s.diff(fullQx,t))
ck('gradient completion needs spatial exchange',s.simplify(fullQx)!=0)
B,C,a,Vac,J,H=s.symbols('B C a V J H',positive=True)
ze('baryon-vacuum source energy cancellation',(-J)+a**3*(J/a**3))
surv=s.symbols('survival',positive=True)
ze('cold baryon ratio tracks depletion',(C/(B*surv))/(C/B)-1/surv)

OM=.308;ratio=5.364;Bp=OM/(1+ratio);Cold=ratio*Bp
rhoref=2.775e11*.7**2; Href=70/3.0857e19*3.156e7 # inverse yr, same as CFG775
cSI=299792458.; Hsi=Href/3.156e7; alpha=math.sqrt(3/(32*math.pi))
def psiN(N,norm=1.):
 aa=math.exp(N)
 return norm*.015*aa**(-2.7)/(1+(1/(2.9*aa))**5.6)
def solve(zstart,tol=1e-10,norm=1.,future='continue'):
 ni=-math.log1p(zstart)
 def rhs(N,y,Xi,active=True):
  aa=math.exp(N); bb,vv=y; e=math.sqrt((bb+Cold)/aa**3+vv)
  j=Xi*psiN(N,norm)/(rhoref*Href*e) if active else 0.
  return [-j,j/aa**3]
 def past(Xi):return solve_ivp(lambda n,y:rhs(n,y,Xi),(ni,0),[Bp,0.],rtol=tol,atol=tol*1e-3,dense_output=True,max_step=.08)
 def target(Xi):
  so=past(Xi);bb,vv=so.y[:,-1]
  return bb+Cold+vv-1
 Xi=brentq(target,.001,15,xtol=tol*.01)
 so=past(Xi); bb,vv=so.y[:,-1]
 sf=solve_ivp(lambda n,y:rhs(n,y,Xi,future=='continue'),(0,12),[bb,vv],rtol=tol,atol=tol*1e-3,dense_output=True,max_step=.08)
 ck('past solve '+str((zstart,tol,norm,future)),so.success)
 ck('future solve '+str((zstart,tol,norm,future)),sf.success)
 ck('physical baryons '+str((zstart,tol,norm,future)),min(so.y[0].min(),sf.y[0].min())>0)
 def state(N):return so.sol(N) if N<=0 else sf.sol(N)
 def E(N):
  bb,vv=state(N)
  return math.sqrt((bb+Cold)*math.exp(-3*N)+vv)
 Vinf=float(sf.y[1,-1]);tail=math.exp(-12)/math.sqrt(Vinf)
 def hlength(N):
  # c/Href times this dimensionless length. Independent future branch.
  lo=quad(lambda nn:math.exp(-nn)/E(nn),N,0,epsabs=tol*.1,epsrel=tol,limit=150)[0] if N<0 else 0
  hi=quad(lambda nn:math.exp(-nn)/E(nn),max(N,0),12,epsabs=tol*.1,epsrel=tol,limit=150)[0]
  return math.exp(N)*(lo+hi+tail)
 R0=hlength(0);rows=[]
 for zz in [0,.5,1,1.5,2,2.5,3]:
  N=-math.log1p(zz);bv,vv=state(N);rv=hlength(N)
  densityratio=math.sqrt(vv/so.y[1,-1])
  rows.append({'z':zz,'baryon_survival':float(bv/Bp),'cold_over_surviving_baryon':float(Cold/bv),'V_over_V0':float(vv/so.y[1,-1]),'a0_density_ratio':densityratio,'R_event_Gpc':rv*cSI/Hsi/3.0856775814913673e25,'a0_event_ratio_if_normalized_today':R0/rv,'a0_over_event_horizon_acceleration':alpha*math.sqrt(vv)*rv,'rM_over_sqrt_rg_R_event':1/math.sqrt(2*alpha*math.sqrt(vv)*rv)})
 # Independent source quadratures reconstruct both loss and gain.
 consumed=quad(lambda n:Xi*psiN(n,norm)/(rhoref*Href*E(n)),ni,0,epsabs=tol*.1,epsrel=tol,limit=150)[0]
 gained=quad(lambda n:Xi*psiN(n,norm)*math.exp(-3*n)/(rhoref*Href*E(n)),ni,0,epsabs=tol*.1,epsrel=tol,limit=150)[0]
 ck('comoving baryon budget '+str((zstart,tol,norm,future)),abs((Bp-bb)-consumed)<max(1e-9,tol*50))
 ck('physical vacuum budget '+str((zstart,tol,norm,future)),abs(so.y[1,-1]-gained)<max(1e-9,tol*50))
 ck('flat H today '+str((zstart,tol,norm,future)),abs(E(0)-1)<1e-9)
 ck('cold ratio grows '+str((zstart,tol,norm,future)),Cold/bb>ratio)
 ck('vacuum trend differs from event-horizon trend '+str((zstart,tol,norm,future)),rows[4]['a0_density_ratio']<1<rows[4]['a0_event_ratio_if_normalized_today'])
 return {'z_start':zstart,'tolerance':tol,'SFR_normalization':norm,'future':future,'Xi_shot':Xi,'Omega_b_projected':Bp,'Omega_c_projected':Cold,'Omega_b_today':float(bb),'Omega_DE_today':float(so.y[1,-1]),'baryon_survival_today':float(bb/Bp),'cold_over_surviving_baryon_today':float(Cold/bb),'weighted_mean_a_minus3':gained/consumed,'V_infinity':Vinf,'rows':rows}
primary=solve(8)
fine=solve(8,1e-12)
for key in ['Xi_shot','baryon_survival_today','Omega_DE_today']:
 ck('tolerance convergence '+key,abs(primary[key]/fine[key]-1)<1e-7)
for i in range(7):ck('horizon convergence z='+str(primary['rows'][i]['z']),abs(primary['rows'][i]['R_event_Gpc']/fine['rows'][i]['R_event_Gpc']-1)<1e-7)
double=solve(8,norm=2)
ck('source normalization degeneracy',abs(double['Xi_shot']*2/primary['Xi_shot']-1)<1e-8)
ck('normalization does not fix depletion',abs(double['baryon_survival_today']-primary['baryon_survival_today'])<1e-8)
futureoff=solve(8,future='off')
ck('same past, different horizon',abs(futureoff['rows'][4]['a0_density_ratio']-primary['rows'][4]['a0_density_ratio'])<1e-10 and abs(futureoff['rows'][4]['R_event_Gpc']-primary['rows'][4]['R_event_Gpc'])>1e-4)
sens=[solve(15),solve(30)]
# Background split: a variable-mass dust component remains pressureless unless
# an interaction or a non-dust stress is explicitly supplied.
kk,nn,mm,hh=s.symbols('k n m H',positive=True)
aa=s.symbols('a',positive=True)
rhodust=nn*mm*aa**(kk-3)
ze('variable-mass dust exchange',aa*hh*s.diff(rhodust,aa)+3*hh*rhodust-kk*hh*rhodust)
result={'passed':len(checks),'checks':checks,'primary':primary,'refined':fine,'normalization_x2':double,'future_production_off':futureoff,'zstart_sensitivity':sens,'source_record':'Claude CFG775 pure MD14; full homogeneous baryon-vacuum source equations from Croker2024v3. No Trinca source replication or likelihood.','assigned_rho_crit_ref_Msun_Mpc3':rhoref,'present_ratio_if_survival_0p7':ratio/.7}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
