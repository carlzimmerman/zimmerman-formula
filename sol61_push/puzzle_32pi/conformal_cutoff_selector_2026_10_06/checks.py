import argparse,json,math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
from scipy.optimize import brentq
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['sign','mass']);args=ap.parse_args();rows=[]
def ck(n,x):rows.append({'name':n,'passed':bool(x)})
def eq(n,x):ck(n,s.factor(x)==0)
d=s.symbols('d',positive=True);a,u,z,p,pp=s.symbols('alpha u z p pp',real=True);beta=2/(d-2);xi=(d-2)/(4*(d-1));c=(d-1)/(d-2)
eq('improved_flat_trace_zero',-(d-2)/2+2*xi*(d-1))
F=1-a*u*u
if args.control=='sign':F=1+a*u*u
q=s.diff(F,u)/F;qd=s.diff(q,u)
eq('actual_log_prefactor',q+2*a*u/(1-a*u*u))
eq('actual_prefactor_second_score',qd+2*a*(1+a*u*u)/(1-a*u*u)**2)
q0=-2*a*u/(1-a*u*u)
eq('critical_second_score',(-2*a*(1+z)/(1-z)**2)-(-4*a*z/(1-z)**2)*(1+z)/(2*z))
Z=(a/xi)/(1-z)+c*4*a*z/(1-z)**2
eq('fixed_xi_kinetic_identity',Z-c*4*a/(1-z)**2)
C=pp+p*p*(1+z)/(2*beta*z);ratio=s.factor((d-1)*(d-2)*C/(2*(c*p*p/(beta*beta*z))))
eq('stationary_mass_ratio',ratio-(2*z*pp/(p*p)+(1+z)/beta))
eq('lower_mass_gap_identity',(1+z)/beta-z/(2*p*p)-1/beta-z*(2*p*p-beta)/(2*beta*p*p))
eq('upper_mass_gap_identity',2/beta-((1+z)/beta)-(1-z)/beta)
# Independent positive finite-window quadrature, with exponentially bounded tails.
def moments(vu,tol=2e-12,window=100):
 def pieces(v):
  t=1/math.sqrt(1+math.exp(-(vu+v)));h=t/(1+t);g=math.exp(-abs(v))/(1+math.exp(-2*abs(v)));el=(1-t)/2
  return h*g,el,-t*(1-t*t)/4
 J=quad(lambda v:pieces(v)[0],-window,window,epsabs=tol,epsrel=tol,limit=180)[0]
 el=quad(lambda v:pieces(v)[0]*pieces(v)[1],-window,window,epsabs=tol,epsrel=tol,limit=180)[0]/J
 second=quad(lambda v:pieces(v)[0]*(pieces(v)[2]+pieces(v)[1]**2),-window,window,epsabs=tol,epsrel=tol,limit=180)[0]/J-el*el
 return 2*math.exp(vu)*J,1+el,second
samples=[]
for gam in [4.,10.,100.]:
 aa=gam/6;left=-1/math.sqrt(aa)
 root=brentq(lambda v:moments(v)[1]+2*aa*v/(1-aa*v*v),left+1e-8,-1e-8,xtol=1e-13)
 A,P,PP=moments(root);zz=aa*root*root;CC=PP+P*P*(1+zz)/(2*zz);ZE=gam/(1-zz)+1.5*P*P;mr=3*CC/ZE
 ck('negative_domain_'+str(gam),left<root<0)
 ck('stationarity_'+str(gam),abs(P+2*aa*root/(1-aa*root*root))<1e-10)
 ck('strict_minimum_'+str(gam),CC>0)
 ck('mass_interval_'+str(gam),1<mr<2)
 ck('small_action_coefficient_'+str(gam),A/2<math.pi/4)
 alt=moments(root,3e-13,120)
 ck('independent_window_precision_'+str(gam),max(abs(x-y) for x,y in zip((A,P,PP),alt))<1e-10)
 samples.append({'gamma':gam,'u':root,'T':math.exp(root),'A_half':A/2,'mass_H_squared':mr,'C':CC})
ck('large_gamma_source_inverse_screen',math.exp(-.045)**2>4/(3*math.sqrt(3)))
if args.control=='mass':ck('false_rapid_cold_mass',samples[-1]['mass_H_squared']>100)
r={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'control':args.control,'samples':samples,'scope':'Analytic improved-stress cutoff/commonvacuum screen; finite quadratures not universal proof; sign control mutates symbolic F only'}
Path(args.out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'total':r['total'],'failures':[x['name'] for x in rows if not x['passed']]}))
