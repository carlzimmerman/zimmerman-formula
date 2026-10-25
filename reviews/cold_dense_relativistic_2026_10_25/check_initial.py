import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 def eos(E,n=256,virial=False):
  z,w=np.polynomial.legendre.leggauss(n);theta=(z+1)*math.pi/4
  amp=2*math.acos(1/math.sqrt(1.2+math.sqrt(E/10)));q=amp*np.sin(theta);x=1/np.cos(q/2)
  U=10*(x*x-1.2)**2;diff=E-U;assert min(diff)>0
  wt=w*amp*np.cos(theta)/np.sqrt(2*diff);K=np.sum(wt*diff)/np.sum(wt)
  P=2*K-E
  if virial:
   qp=(40*x**3-48*x)*.5*x*np.tan(q/2);kv=np.sum(wt*q*qp/2)/np.sum(wt)
   assert abs(kv/K-1)<1e-7
  return float(P)
 E0=brentq(eos,.41,1.,xtol=1e-12)
 for E in [E0,1.,10.,1e3,1e6,1e10]:
  assert abs(eos(E,256,True)-eos(E,512,True))<1e-6*E
 # Vacuum contribution to the active gravity of a uniform cell:
 # total mu=(E+vac)x^3/3, total P=P-vac -> E/3+P-2vac/3.
 for E,P,V in [(10.,2.,1.6),(2.,.3,1.6)]:
  active=E/3+P+ (2 if a.mutate else -2)*V/3
  assert abs(active-((E+V)/3+P-V))<1e-12,'vacuum force sign'
 central=np.geomspace(E0*1.001,1e6,61);runs=[]
 for ntab,tol in [(800,2e-8),(1600,2e-10)]:
  energies=np.geomspace(E0,1e10,ntab)
  # Cache quadrature nodes once for the table.
  zz,ww=np.polynomial.legendre.leggauss(256);th=(zz+1)*math.pi/4
  pressures=[]
  for E in energies:
   amp=2*math.acos(1/math.sqrt(1.2+math.sqrt(E/10)));qq=amp*np.sin(th);U=10*(1/np.cos(qq/2)**2-1.2)**2;df=E-U
   weights=ww*amp*np.cos(th)/np.sqrt(2*df);pressures.append(2*np.sum(weights*df)/np.sum(weights)-E)
  pressures=np.array(pressures);pressures[0]=0.;assert np.all(np.diff(pressures)>0)
  pofe=PchipInterpolator(energies,pressures);eofp=PchipInterpolator(pressures,energies)
  cs=pofe.derivative()(energies[1:-1]);assert min(cs)>0 and max(cs)<1.001
  rows=[]
  for vac in [1.6,0.]:
   for Ec in central:
    Pc=float(pofe(Ec));active=Ec/3+Pc-2*vac/3
    if active<=0:
     rows.append(dict(vacuum=vac,Ec=float(Ec),status='no_central_pressure_maximum'));continue
    x0=min(1e-6,1e-4/math.sqrt(Ec));mu0=Ec*x0**3/3;pr0=Pc-.5*(Ec+Pc)*active*x0*x0
    def rhs(x,y):
     mu,pr=y;E=float(eofp(np.clip(pr,0,pressures[-1])))
     F=1-2*mu/x-2*vac*x*x/3
     return [x*x*E,-(E+pr)*(mu+x**3*(pr-2*vac/3))/(x*x*max(F,1e-8))]
    def surface(x,y):return y[1]
    def horizon(x,y):return 1-2*y[0]/x-2*vac*x*x/3-1e-5
    def cap(x,y):return pressures[-1]-y[1]
    for ev in [surface,horizon,cap]:ev.terminal=True;ev.direction=-1
    sol=solve_ivp(rhs,[x0,3],[mu0,pr0],events=[surface,horizon,cap],rtol=tol,atol=tol*1e-3,method='DOP853',max_step=.01)
    assert sol.success
    status=next((name for name,times in zip(['surface','metric_cutoff','EOS_cap'],sol.t_events) if len(times)),'radius_cap')
    xr=float(sol.t[-1]);mu=float(sol.y[0,-1]);pr=float(sol.y[1,-1])
    rows.append(dict(vacuum=vac,Ec=float(Ec),status=status,x=xr,mu=mu,P_end=pr,min_sampled_P=float(min(sol.y[1])),metric=1-2*mu/xr-2*vac*xr*xr/3))
  runs.append(dict(table_size=ntab,tolerance=tol,sound_speed_squared_range=[float(min(cs)),float(max(cs))],rows=rows))
 for r,s in zip(runs[0]['rows'],runs[1]['rows']):
  assert r['status']==s['status'],('classification convergence',r,s)
  if r['status']=='surface':
   assert abs(r['x']/s['x']-1)<.01 and abs(r['mu']/s['mu']-1)<.01
 G=6.67430e-11;C=299792458.;PC=3.085677581491367e16;MS=1.98847e30;Dmass=.75*3*(1.8e-18)**2/(8*math.pi*G);ell=C/math.sqrt(4*math.pi*G*Dmass);massunit=C*C*ell/G/MS
 summary=dict(surface_energy_over_D=E0,length_unit_Mpc=ell/PC/1e6,mass_unit_Msun=massunit)
 for vac in [1.6,0.]:
  rr=[r for r in runs[-1]['rows'] if r['vacuum']==vac];summary[str(vac)]={st:sum(r['status']==st for r in rr) for st in sorted(set(r['status'] for r in rr))}
  sf=[r for r in rr if r['status']=='surface']
  if sf:summary[str(vac)]['surface_ranges']=dict(radius_Mpc=[min(r['x'] for r in sf)*ell/PC/1e6,max(r['x'] for r in sf)*ell/PC/1e6],mass_Msun=[min(r['mu'] for r in sf)*massunit,max(r['mu'] for r in sf)*massunit])
 result=dict(summary=summary,runs=runs)
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
