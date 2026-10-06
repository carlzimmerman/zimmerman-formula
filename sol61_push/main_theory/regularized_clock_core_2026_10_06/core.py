#!/usr/bin/env python3
"""Detuned logKGB response, static constant-density fluid, finite source matching."""
import argparse,json,math,time,traceback
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--control-critical',action='store_true');ap.add_argument('--max-evals',type=int,default=20000);ap.add_argument('--phase-seconds',type=float,default=15);ap.add_argument('--require-exterior',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
eta=.5;A=1.;H=1.;rho=6e6;p0=4.;eps=0. if args.control_critical else .01;kap=1-eps;checks=[]
def ck(n,ok,d):checks.append(dict(name=n,passed=bool(ok),detail=str(d)));print(('PASS ' if ok else 'FAIL ')+n+': '+str(d),flush=True)
Dens=rho+3*p0
rows=[];center={}
if eps>0:
 xp=-eta/(3*kap)
 poly=lambda x:(3*kap*x+eta)*(Dens+6*x*x-6*eta*x-6*(1+eta))-18*eps*eta*x*(x+1)
 x=brentq(poly,-1.,xp,xtol=5e-16,rtol=1e-14)
 n2=(Dens+6*x*x-6*eta*x-6*(1+eta))/(12*eps);b2=2*n2-1.5*x*x+1.5-p0/2;f2=2*n2-x*x
 Ccenter=b2+n2-(rho+p0)/4
 n3,y2=np.linalg.solve(np.array([[3*eps,eta-3*x],[3*(4*x+eta),-12*x*x+2*Ccenter]]),np.array([-4*n2*n2/A,0.]))
 b3=3*n3-4*x*y2
 center=dict(x=x,pole=xp,n2=n2,b2=b2,f2=f2,density=Dens,epsilon=eps,trace_relative_residual=abs((3*kap*x+eta)*n2-1.5*eta*x*(x+1))/(1+abs(n2)))
 ck('high_density_regular_center',n2>0 and f2>0 and -1<x<xp and center['trace_relative_residual']<1e-12,'actual center polynomial with fluidrho6e6,p4; positive physical force')
else:
 ck('high_density_regular_center',Dens<=1.5*(eta+2)**2,'criticalepsilon0 cannot supply real weakcenter for these same physical fluid inputs')

def operator(g):
 ga=abs(g);ss=math.hypot(ga,A/2);wa=ga*ga/(ss+A/2);wgg=ga/ss;qg=2*(kap*g-math.copysign(wa,g));qgg=2*(kap-wgg)
 leg=(ga*ss-A*A/4*math.asinh(2*ga/A))/2 if ga/A>=1e-3 else 2*ga**3/(3*A)-4*ga**5/(5*A**3)+12*ga**7/(7*A**5)
 pressure=2*leg-kap*ga*ga
 return qg,qgg,pressure,wa

def material(r,y,inside):
 lnN,lnB,w,k=y;velsq=math.exp(2*lnB)*r*r*w*w
 if velsq>=1:raise RuntimeError('physical Killing F<=0')
 if not inside:return 0.,0.,0.
 lnFratio=2*lnN+math.log1p(-velsq);p=p0+(rho+p0)*math.expm1(-.5*lnFratio)
 add=(rho+p)*velsq/(1-velsq)
 return rho+add,p+add,p

def rhsraw(t,y,inside):
 r=math.exp(t);lnN,lnB,w,k=map(float,y)
 if abs(lnN)>1 or abs(lnB)>1 or w<=0:raise RuntimeError('declared weak/positive-flow guard')
 N=math.exp(lnN);B=math.exp(lnB);V=-w*r*N;P=N*k/r;g=k/(r*B);qg,qgg,pressure,wa=operator(g)
 if abs(qgg)<1e-7:raise RuntimeError('response acceleration Hessian nearzero')
 energy,srad,p=material(r,y,inside)
 BP=B*k/r*(eta/w-1)+B**3*r*((rho if inside else 0.)+p)/(2*(1-B*B*r*r*w*w))
 curv=N*(-math.expm1(-2*lnB)-2*k*math.exp(-2*lnB))
 VP=N/(2*r*V)*(-curv-V*V/N*(1-2*k)-N*r*r*(6*eta*lnN-3+pressure+srad)+2*eta*r*V*k)
 T=2*B*r*V*VP+2*r*BP*V*V+B*V*V
 rest=2*math.sinh(lnB)+2*r*BP/B**2+T/N**2+B*r*r*(6*eta*lnN-3+pressure+6*eta-energy)+2*eta*B*r*r*(VP+BP/B*V+2*V/r)/N
 PP=N*B/(r*r*qgg)*(rest-2*r*qg+r*r*qgg*g*(P/N+BP/B))
 return np.array([k,r*BP/B,w*(r*VP/V-1-k),k+r*r*PP/N-k*k])

if eps>0:
 for tol in [1e-7,3e-8]:
  start=time.monotonic();counter=[0];r0=1e-13;rupper=5e-6;rout=3e-5;last_t=[math.log(r0)]
  def rhs(t,y,inside=True):
   counter[0]+=1
   last_t[0]=t
   if counter[0]>args.max_evals or time.monotonic()-start>args.phase_seconds:raise RuntimeError('Declared phase evaluation/time cap')
   return rhsraw(t,y,inside)
  def surface(t,y):return material(math.exp(t),y,True)[2]
  surface.terminal=True;surface.direction=-1
  y0=np.array([math.log1p(n2*r0*r0+n3*r0**3),math.log1p(b2*r0*r0+b3*r0**3),-(x+y2*r0)/math.exp(n2*r0*r0+n3*r0**3),(2*n2*r0*r0+3*n3*r0**3)/(1+n2*r0*r0+n3*r0**3)])
  def jac(t,y,inside=True):
   rr=math.exp(t);mat=np.zeros((4,4))
   for col in range(4):
    scale=max(abs(y[col]),abs(n2*rr*rr)) if col!=2 else max(abs(y[col]),.1)
    step=scale*1e-6;yp=y.copy();ym=y.copy();yp[col]+=step;ym[col]-=step
    mat[:,col]=(rhs(t,yp,inside)-rhs(t,ym,inside))/(2*step)
   return mat
  fluiddata={}
  try:
   fluid=solve_ivp(rhs,(math.log(r0),math.log(rupper)),y0,method='Radau',rtol=tol,atol=np.array([tol*1e-7,tol*1e-7,tol*1e-2,tol*1e-7]),jac=jac,first_step=.001,max_step=.06,events=surface,dense_output=True)
   reached=len(fluid.t_events[0])>0
   if not reached:raise RuntimeError('no p0 surface: '+fluid.message)
   rs=math.exp(fluid.t_events[0][0]);ys=fluid.y_events[0][0]
   interior=[]
   for tt in np.linspace(math.log(r0),math.log(rs),61):
    yy=fluid.sol(tt);rr=math.exp(tt);energy,sr,pp=material(rr,yy,True);ddd=rhsraw(tt,yy,True);vv2=math.exp(2*yy[1])*rr*rr*yy[2]**2
    physical=(yy[3]*(1-vv2)-vv2*(ddd[1]+1+ddd[2]/yy[2]))/(rr*math.exp(yy[1])*math.sqrt(1-vv2))
    interior.append(dict(r=rr,p=pp,physical_force=physical,a=yy[3]/(rr*math.exp(yy[1])),Qgg=operator(yy[3]/(rr*math.exp(yy[1])))[1],y=yy.tolist()))
   fluiddata=dict(fluid_success=True,surface=rs,surface_state=ys.tolist(),p_surface=material(rs,ys,True)[2],mb=rho*rs**3/6,fluid_nfev=counter[0],interior=interior)
   counter[0]=0
   start=time.monotonic()
   external=solve_ivp(lambda t,y:rhs(t,y,False),(math.log(rs),math.log(rout)),ys,method='Radau',rtol=tol,atol=np.array([tol*1e-7,tol*1e-7,tol*1e-2,tol*1e-7]),jac=lambda t,y:jac(t,y,False),first_step=.001,max_step=.04,dense_output=True)
   samples=[]
   for tt in np.linspace(math.log(rs),external.t[-1],41):
    rr=math.exp(tt);yy=external.sol(tt);dd=rhsraw(tt,yy,False);lnN,lnB,w,k=yy;clock=k/(rr*math.exp(lnB));Vp= -w*rr*math.exp(lnN)*(dd[2]/w+1+k)/rr;V=-w*rr*math.exp(lnN)
    physical=clock-V*Vp+rr
    mass=rr*rr*(physical-clock+eps*clock+operator(clock)[3]+eta*(V+rr))
    mb=rho*rs**3/6
    samples.append(dict(r=rr,a=clock,Qgg=operator(clock)[1],physical_leading_g=physical,weak_massflux=mass,mb=mb,MOND_ratio=physical/(math.sqrt(mb*A)/rr),y=yy.tolist()))
   rows.append(dict(tol=tol,success=bool(external.success),fluid_success=True,surface=rs,surface_state=ys.tolist(),p_surface=material(rs,ys,True)[2],mb=rho*rs**3/6,end_r=math.exp(external.t[-1]),end_state=external.y[:,-1].tolist(),nfev=counter[0],fluid_nfev=fluiddata['fluid_nfev'],elapsed=time.monotonic()-start,samples=samples,interior=interior))
  except (RuntimeError,ValueError,OverflowError,ZeroDivisionError) as e:rows.append(dict(tol=tol,success=False,message=str(e),attempt_r=math.exp(last_t[0]),traceback=traceback.format_exc(),nfev=counter[0],elapsed=time.monotonic()-start,**fluiddata))
 ck('bounded_conserved_fluid_surface',all(z.get('fluid_success',z['success']) for z in rows),'actual p0 event from exact conserved fluid, independent of exterior continuation status')
 if all(z.get('fluid_success',z['success']) for z in rows):
  ck('bounded_source_tolerance_agreement',abs(rows[0]['surface']/rows[1]['surface']-1)<.002 and max(abs(a-b) for a,b in zip(rows[0]['surface_state'],rows[1]['surface_state']))<1e-6,'two interior tolerances; finite evidence, not certified existence')
 else:ck('bounded_source_tolerance_agreement',False,'source target not reached within declared bounds')
 if all(z.get('fluid_success',z['success']) for z in rows):
  ck('bounded_positive_pressure_and_force',all(pt['p']>=-1e-10 and pt['physical_force']>0 and pt['Qgg']>0 and max(abs(pt['y'][0]),abs(pt['y'][1]))<1e-4 for row in rows for pt in row['interior']),'61 interior points per tolerance; full physical Killing force and positivepressure through surface')
 if args.require_exterior:ck('bounded_exterior_extension',all(z['success'] for z in rows),'larger declared budget tests actual same-state vacuum extension; success never inferred from fluid surface')
result=dict(checks=checks,center=center,runs=rows,control=args.control_critical,phase_evaluation_cap=args.max_evals,phase_wall_seconds=args.phase_seconds,software=dict(numpy=np.__version__),non_claims=['No cosmological normalized boundary condition','No full finitegradient stability','No epsilon selector','Numerical solution not certified globalexistence'])
for row in rows:print(json.dumps({key:row.get(key) for key in ['tol','fluid_success','surface','success','message','attempt_r','fluid_nfev','nfev']}),flush=True)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(z['passed'] for z in checks) else 1)
