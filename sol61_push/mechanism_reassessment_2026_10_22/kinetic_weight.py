import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,cumulative_trapezoid
from scipy.optimize import brentq
from scipy.special import roots_legendre
from scipy.stats import qmc
p=Path(__file__).parent
refs=json.load(open(p/'cold_limit_run/results.json'))['rows'];omega=json.load(open(p/'cold_spectrum_run/results.json'))['spectra'][-1]['omega'][0]
power=int(sys.argv[2]) if len(sys.argv)>2 else 10
rows=[]
for ref in refs[-1:]:
 A=ref['A'];pc=ref['Psi_c'];r0=1e-6
 def fun(r,y):
  m,psi=y;q=m/r**2;rho=A*max(psi,0)**2.5/(1+r*r);chi=2.5*rho/psi if psi>0 else 0
  return [r*r*rho,(q*q/(1-q)-r/(1+r*r)**1.5+.02*r*rho/(1+r*r))/(1+.01*chi)]
 def edge(r,y):return y[1]
 edge.terminal=True;edge.direction=-1
 sol=solve_ivp(fun,[r0,100],[A*pc**2.5*r0**3/3,pc],rtol=2e-13,atol=2e-16,events=edge,dense_output=True,max_step=.05)
 R=sol.t[-1];rr=np.linspace(r0,R,80001);mm,psi=sol.sol(rr);rho=A*np.maximum(psi,0)**2.5/(1+rr*rr)
 q=mm/rr**2;dp=np.array([fun(float(x),y)[1] for x,y in zip(rr,sol.sol(rr).T)]);drho=2.5*A*np.maximum(psi,0)**1.5*dp/(1+rr*rr)-2*rr*rho/(1+rr*rr)
 integ=cumulative_trapezoid(q*(2-q)/(1-q)**2*rr*rho,rr,initial=0);potential=-(integ[-1]-integ)-.01*(3*rho+rr*drho);potential_norm=float(max(abs(potential)));potential/=potential_norm
 grid=np.linspace(r0,1.01*R,100001)
 def chemical(lam):
  x=grid/lam;bounded=np.minimum(np.maximum(x,r0),R);ym,yp=sol.sol(bounded)
  ym=np.where(x>=R,sol.y[0,-1],ym);ym=np.where(x<r0,A*pc**2.5*x**3/3,ym)
  dens=np.where(x<R,A*np.maximum(yp,0)**2.5/(1+x*x)/lam**3,0)
  qq=ym/grid**2;integ=cumulative_trapezoid(qq*qq/(1-qq),grid,initial=0)
  return integ[-1]-integ+.01*dens
 eps=1e-5;fd=(chemical(1+eps)-chemical(1-eps))/(2*eps)
 analytic=np.interp(grid,rr,potential*potential_norm,right=0)
 derivative_error=float(max(abs(fd-analytic))/potential_norm)
 cdf=cumulative_trapezoid(rr*rr*rho,rr,initial=0);cdf/=cdf[-1]
 u=qmc.Sobol(3,scramble=False).random_base2(power);u=(u*(2**power-1)+.5)/(2**power)
 r=np.interp(u[:,0],cdf,rr);pp=sol.sol(r)[1];ss=np.linspace(0,1,30001);speeds=np.sqrt(2*pp)*np.interp(u[:,1],(5*ss**3-3*ss**5)/2,ss)
 vr=speeds*u[:,2];vt=speeds*np.sqrt(1-u[:,2]**2)/np.sqrt(1+r*r);L=r*vt;E=.5*(vr*vr+vt*vt)-pp
 omegas=[];errors=[];turnerrs=[];couplings=[];coupling_errors=[]
 for radius,l,e in zip(r,L,E):
  def v2(x):return 2*(e+sol.sol(x)[1])-l*l/x**2
  rp=brentq(v2,r0,radius,xtol=1e-13);ra=brentq(v2,radius,R,xtol=1e-13)
  vals=[]
  for order in [64,128]:
   nodes,w=roots_legendre(order);theta=(nodes+1)*np.pi/4;x=rp+(ra-rp)*np.sin(theta)**2
   speed2=v2(x)
   if min(speed2)<=0:raise RuntimeError('quadrature reached nonpositive speed')
   half=np.sum(w*(ra-rp)*np.sin(2*theta)/np.sqrt(speed2))*np.pi/4;vals.append(np.pi/half)
  coeffs=[]
  for count in [1024,2048]:
   theta=(np.arange(count)+.5)*np.pi/(2*count);xx=rp+(ra-rp)*np.sin(theta)**2
   weights=(ra-rp)*np.sin(2*theta)/np.sqrt(v2(xx));phase=np.pi*(np.cumsum(weights)-weights/2)/weights.sum()
   mu=np.interp(xx,rr,potential);coeffs.append(np.array([np.sum(weights*mu*np.cos(n*phase))/weights.sum() for n in range(1,17)]))
  couplings.append(coeffs[-1]);coupling_errors.append(float(max(abs(coeffs[0]-coeffs[1]))))
  omegas.append(vals[-1]);errors.append(abs(vals[0]/vals[1]-1));turnerrs.extend([abs(v2(rp)),abs(v2(ra))])
 o=np.array(omegas)
 C=np.array(couplings);Q=-E-L*L/2;freq=o[:,None]*np.arange(1,17)[None,:];M=float(sol.y[0,-1])
 strength=2*freq**2*C**2/Q[:,None]
 moment=float(M*np.mean(strength.sum(axis=1)));exact=float(np.trapz(rr*rr*rho*np.gradient(potential,rr)**2,rr))
 responses={}
 for width in [.1,.03,.01]:
  z=omega+1j*width;terms=-strength/(freq**2-z*z);value=M*np.mean(terms.sum(axis=1))
  responses[str(width)]=dict(real=float(value.real),imag=float(value.imag),absorptive=float(-value.imag),harmonics=(-M*np.mean(terms,axis=0).imag).tolist())
 rows.append(dict(A=A,samples=2**power,mass=M,potential_normalization=potential_norm,dilation_derivative_error=derivative_error,max_quadrature_error=max(errors),max_turning_residual=max(turnerrs),max_fourier_absolute_error=max(coupling_errors),sum_rule_sample=moment,sum_rule_integral=exact,sum_rule_relative_error=abs(moment/exact-1),minimum_Q=float(Q.min()),responses=responses,omega_samples=o.tolist(),Q_samples=Q.tolist(),couplings=C.tolist()))

checks=dict(sum_rule=all(x['sum_rule_relative_error']<.1 for x in rows),passivity=all(v['absorptive']>=0 for x in rows for v in x['responses'].values()),dilation_derivative=all(x['dilation_derivative_error']<1e-4 for x in rows),fourier=all(x['max_fourier_absolute_error']<1e-4 for x in rows),mass=all(abs(x['mass']-1)<1e-5 for x in rows),quadrature=all(x['max_quadrature_error']<1e-4 for x in rows),turning=all(x['max_turning_residual']<1e-8 for x in rows))
out=dict(cold_collective_omega=omega,quantile_levels=[0,.01,.1,.5,.9,.99,1],checks=checks,all_pass=all(checks.values()),rows=rows,scope='derivative-weighted prescribed trial response with finite broadening; no self-consistent pole or damping rate')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps({**out,'rows':[{k:v for k,v in r.items() if k not in ['omega_samples','Q_samples','couplings']} for r in rows]},indent=2));sys.exit(0 if out['all_pass'] else 1)
