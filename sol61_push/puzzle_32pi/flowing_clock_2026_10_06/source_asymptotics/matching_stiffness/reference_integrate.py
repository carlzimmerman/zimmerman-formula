"""Bounded exact exterior IVP from formal inner-flow data; not a matched BVP.
Uses log-radius and logN,logB,w=-V/(HrN),k=rN'/N.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);a=ap.parse_args();base=Path(__file__).resolve().parent;out=a.output_dir.resolve();out.relative_to(base);out.mkdir(parents=True,exist_ok=True)
K=H=1.
def response(gs,A):
 g=abs(gs);ss=math.hypot(g,A/2);wg=g*g/(ss+A/2);wgg=g/ss
 ug=2*K*(gs-math.copysign(wg,gs))
 if g/A<1e-3: leg=2*g**3/(3*A)-4*g**5/(5*A**3)+12*g**7/(7*A**5)
 else:leg=(g*ss-A*A/4*math.asinh(2*g/A))/2
 pressure=2*K*(leg-g*g/2);u=pressure+gs*ug
 return u,ug,2*K*(1-wgg),pressure,wg

def equations(r,y,eta,A):
 N=math.exp(y[0]);B=math.exp(y[1]);w=y[2];kk=y[3];V=-w*H*r*N;P=N*kk/r;c=3*K*eta*H*H;b=2*K*eta*H;veff=3*K*H*H
 gs=P/(N*B);u,ug,ugg,press,wg=response(gs,A);S=2*c*math.log(N)-veff+u
 BP=B*(-P/N-b*r*P/(2*K*V))
 VP=N/(2*K*r*V)*(-K*(N-(N+2*r*P)/B**2+V*V/N-2*r*V*V*P/N**2)-N*r*r*(S-gs*ug)+b*r*r*V*P/N)
 T=2*B*r*V*VP+2*r*BP*V*V+B*V*V
 ENrest=K*(B-1/B+2*r*BP/B**2+T/N**2)+B*r*r*(S+2*c-gs*ug)+b*B*r*r*(VP+BP/B*V+2*V/r)/N
 PP=N*B/(r*r*ugg)*(ENrest-2*r*ug+r*r*ugg*gs*(P/N+BP/B))
 derivative=[kk,r*BP/B,w*(r*VP/V-1-kk),kk+r*r*PP/N-kk*kk]
 gp=PP/(N*B)-gs*(P/N+BP/B)
 # Independent stationary current, not copied from the EL residual combination.
 jrq=b*(P/B**2-3*H*V-V/N*(VP+(BP/B+2/r)*V))+V/(B*r*r)*(2*r*ug+r*r*ugg*gp)
 F=N*N-B*B*V*V
 Fp=2*N*P-2*B*BP*V*V-2*B*B*V*VP
 circspeed=r*Fp/(2*F)
 return derivative,dict(N=N,B=B,w=w,k=kk,V=V,gclock=abs(gs),Wg=wg,F=F,circular_speed2=circspeed,qjr=jrq,theta_over_3H=-(VP+BP/B*V+2*V/r)/(3*H*N),Ugg=ugg,proposed_flux_ratio=wg*r*r)
rows=[]
class EvaluationGuard(Exception):pass
for ratio in [.3,1.,3.]:
 for eta in [.25,.5,.75]:
  m=1e-12;A=ratio*H;L=math.sqrt(m*A);r0=10*L/A;rmax=.03/H;y0=[0.,math.log1p(L),eta,L]
  count=[0];last=[math.log(r0),np.array(y0)]
  def rhs(x,y):
   count[0]+=1;last[:]=[x,y.copy()]
   if count[0]>3000:raise EvaluationGuard('3000RHS evaluation cap')
   return equations(math.exp(x),y,eta,A)[0]
  def horizon(x,y):return equations(math.exp(x),y,eta,A)[1]['F']/math.exp(2*y[0])-.01
  horizon.terminal=True;horizon.direction=-1
  def wzero(x,y):return y[2]-.001
  wzero.terminal=True;wzero.direction=-1
  print('START',ratio,eta,flush=True)
  try:
   sol=solve_ivp(rhs,(math.log(r0),math.log(rmax)),y0,method='DOP853',rtol=1e-10,atol=1e-13,max_step=.1,events=[horizon,wzero],dense_output=True)
  except (EvaluationGuard,OverflowError,ValueError,ZeroDivisionError) as exc:
   yy=last[1];rr=math.exp(last[0]);dd,eev=equations(rr,yy,eta,A)
   rows.append(dict(A_over_H=ratio,eta=eta,m=m,L=L,r0=r0,r_requested=rmax,success=False,message=str(exc),nfev=count[0],last_trial_radius=rr,last_trial=eev))
   (out/'partial_results.json').write_text(json.dumps(rows,indent=2)+'\n');print('GUARD',ratio,eta,rr,flush=True);continue
  points=[]
  for x in np.linspace(sol.t[0],sol.t[-1],65):
   rr=math.exp(float(x));yy=sol.sol(x);dy,z=equations(rr,yy,eta,A)
   points.append(dict(r=rr,**z))
  end=points[-1];print('END',ratio,eta,end['w'],flush=True);rows.append(dict(A_over_H=ratio,eta=eta,m=m,L=L,r0=r0,r_requested=rmax,success=bool(sol.success),message=sol.message,steps=len(sol.t),nfev=sol.nfev,event=[x.tolist() for x in sol.t_events],end=end,clockflow_boundary_defect=end['w']-1,theta_boundary_defect=end['theta_over_3H']-1,max_current_abs=max(abs(z['qjr']) for z in points),samples=points))
# Refinement only if representative scan reached its target; never hide capped cases.
ref=next(z for z in rows if z['A_over_H']==1. and z['eta']==.5)
refdiff={};refsuccess=False
if ref['success'] and not any(ref['event']):
 eta=.5;A=1.;m=1e-12;L=math.sqrt(m*A);r0=10*L/A;y0=[0.,math.log1p(L),eta,L];counter=[0]
 def rhs2(x,y):
  counter[0]+=1
  if counter[0]>3000:raise EvaluationGuard('refinement3000RHS cap')
  return equations(math.exp(x),y,eta,A)[0]
 try:
  s1=solve_ivp(rhs2,(math.log(r0),math.log(.03)),y0,method='DOP853',rtol=1e-11,atol=1e-14,max_step=.05)
  refsuccess=refsuccess
  refdiff={key:float(val-ref['end'][key]) for key,val in equations(.03,s1.y[:,-1],eta,A)[1].items() if key in ['N','B','w','k','theta_over_3H']}
 except EvaluationGuard:refdiff={'evaluation_guard':True}
res={'runs':rows,'refinement':{'success':refsuccess,'end_differences':refdiff},'limitations':['Initialdata from formal branch, no interior','Not a cosmological BVP','No fitted GN or force fidelity','No finitegradient health proof']};(out/'results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'runs':len(rows),'successful':sum(z['success'] for z in rows),'boundary_w':[z.get('end',z.get('last_trial',{})).get('w') for z in rows],'refinement':refdiff}));raise SystemExit(0 if all(z['success'] for z in rows) and refsuccess else 1)
