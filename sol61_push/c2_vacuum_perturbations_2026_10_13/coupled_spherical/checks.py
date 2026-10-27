"""Exact local spherical Einstein constraints and sampled linear metric response."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import cumulative_trapezoid

arg=argparse.ArgumentParser();arg.add_argument('--output',required=True)
OUT=Path(arg.parse_args().output)
checks=[]
def eq(name,e):
    e=s.simplify(e);assert e==0,(name,e)
    checks.append({'name':name,'passed':True})
t,r,th,ph=s.symbols('t r th ph',real=True)
N=s.Function('N')(t,r);B=s.Function('B')(t,r)
coord=[t,r,th,ph];g=s.diag(N**2,-1/B,-r**2,-r**2*s.sin(th)**2);inv=g.inv()
gam={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   v=s.simplify(sum(inv[i,l]*(s.diff(g[l,k],coord[j])+s.diff(g[l,j],coord[k])-s.diff(g[j,k],coord[l])) for l in range(4))/2)
   if v!=0:gam[i,j,k]=v
def C(i,j,k):return gam.get((i,j,k),s.S.Zero)
def ric(i,j):return s.simplify(sum(s.diff(C(k,i,j),coord[k])-s.diff(C(k,i,k),coord[j])+sum(C(k,k,l)*C(l,i,j)-C(k,j,l)*C(l,i,k) for l in range(4)) for k in range(4)))
diag=[ric(i,i) for i in range(4)];scalar=s.simplify(sum(inv[i,i]*diag[i] for i in range(4)))
Gtt=s.simplify(inv[0,0]*diag[0]-scalar/2)
Grr=s.simplify(inv[1,1]*diag[1]-scalar/2)
Grt=s.simplify(inv[1,1]*ric(1,0))
Gang=s.simplify(inv[2,2]*diag[2]-scalar/2)
eq('general_Einstein_tt',Gtt-((1-B)/r**2-s.diff(B,r)/r))
eq('general_Einstein_rr',Grr-((1-B)/r**2-2*B*s.diff(N,r)/(r*N)))
eq('general_Einstein_rt',Grt-s.diff(B,t)/r)
angular=s.Function('e')(t,r)
E=s.diag(0,0,angular,angular)
divEr=sum(s.diff(E[mu,1],coord[mu])+sum(C(mu,mu,la)*E[la,1]-C(la,mu,1)*E[mu,la] for la in range(4)) for mu in range(4))
eq('angular_Bianchi_closure',divEr+2*angular/r)

grav,a,X0,BR,Lambda,Me=s.symbols('G a X0 BR Lambda Me',positive=True)
bb=1-2*grav*Me/r-Lambda*r**2/3
ur=s.Function('U')(r);chi=s.Function('chi')(t,r);dm=s.Function('dm')(t,r);dn=s.Function('dn')(t,r)
ut=BR/bb
ct=-(ur*s.diff(chi,r)+(2*ur/r+s.diff(ur,r))*chi)/ut
mr=8*s.pi*a*X0*r**2*ut*chi
mt=-8*s.pi*a*X0*r**2*ur*chi
nr=grav*dm/(r**2*bb)+grav*dm*s.diff(bb,r)/(r*bb**2)+8*s.pi*grav*a*X0*r*chi*ur**2/bb**2
eq('mass_mixed_derivative',s.diff(mr,t).subs(s.diff(chi,t),ct)-s.diff(mt,r))
lam=s.symbols('lambda',real=True)
be=bb-2*grav*lam*dm/r
ne=s.sqrt(bb/BR)*(1+lam*dn)
geomtt=(1-be)/r**2-s.diff(be,r)/r
geomrr=(1-be)/r**2-2*be*s.diff(ne,r)/(r*ne)
geomrt=s.diff(be,t)/r
eq('linear_Einstein_tt',s.diff(geomtt,lam).subs(lam,0).subs(s.diff(dm,r),mr)-8*s.pi*grav*2*a*X0*chi*ut)
eq('linear_Einstein_rt',s.diff(geomrt,lam).subs(lam,0).subs(s.diff(dm,t),mt)-8*s.pi*grav*2*a*X0*chi*ur)
eq('linear_Einstein_rr',s.diff(geomrr,lam).subs(lam,0).subs(s.diff(dn,r),nr)+8*s.pi*grav*2*a*X0*chi*ur**2/bb)

# Conservation follows directly from continuity and the two geodesic equations.
U=s.Matrix([ut,ur,0,0]);ub=s.Matrix([1,-ur/bb,0,0])
bgmetric=s.diag(bb/BR,-1/bb,-r**2,-r**2*s.sin(th)**2)
bginv=bgmetric.inv();bggam={}
for i in range(4):
 for j in range(4):
  for k in range(4):
   v=s.simplify(sum(bginv[i,l]*(s.diff(bgmetric[l,k],coord[j])+s.diff(bgmetric[l,j],coord[k])-s.diff(bgmetric[j,k],coord[l])) for l in range(4))/2)
   if v!=0:bggam[i,j,k]=v
def BG(i,j,k):return bggam.get((i,j,k),s.S.Zero)
source=2*a*X0*chi*(U*ub.T)
def reduce_background(e):
 e=s.together(e.subs(s.diff(chi,t),ct).subs(s.diff(ur,r),-s.diff(bb,r)/(2*ur)))
 num,den=s.fraction(e)
 num=s.rem(s.Poly(s.expand(num),ur),s.Poly(ur**2-(BR-bb),ur)).as_expr()
 return s.factor(num/den)
for nu in [0,1]:
 div=sum(s.diff(source[mu,nu],coord[mu])+sum(BG(mu,mu,la)*source[la,nu]-BG(la,mu,nu)*source[mu,la] for la in range(4)) for mu in range(4))
 eq('linear_source_conservation_'+str(nu),reduce_background(div))

pit,pir=s.symbols('pit pir')
forcing=chi/(s.sqrt(2*X0)*ut)+s.sqrt(2*X0)*dn-s.sqrt(2*X0)*grav*dm*ur**2/(r*bb*BR)
h00=2*bb/BR*dn;hrr=-2*grav*dm/(r*bb**2)
qpi=s.sqrt(2*X0)*(ut*pit+ur*pir)
metricpart=X0*(h00*ut**2+hrr*ur**2)
eq('phase_includes_constraint_metric',(qpi-metricpart-chi).subs(pit,forcing-ur/ut*pir))
wrong=(qpi-metricpart-chi).subs(pit,chi/(s.sqrt(2*X0)*ut)-ur/ut*pir)
assert s.simplify(wrong)!=0
checks.append({'name':'omitted_metric_phase_term_detected','passed':True,'residual':str(s.simplify(wrong))})

root=Path(__file__).parent.parent
payload=json.loads((root/'numeric_run/results.json').read_text());data=np.load(root/'numeric_run/profiles.npz')
b=payload['b'];cv=payload['C'];br=payload['BR'];alpha=1e-8
labels=data['labels'];times=data['times'];rows=[]
for sign in [-1,1]:
 x,f,J,weight=data['s'+str(sign)]
 mass=cv*b*br*cumulative_trapezoid(weight*f*J,x=labels,axis=0,initial=0)
 invariance=float(np.max(abs(mass-mass[:,[0]])))
 assert invariance<1e-10
 max_dB=0;max_dn=0
 for i,time in enumerate(times):
  bx=1-cv*(2/(3*x[:,i])+x[:,i]**2/3)
  bp=cv*(2/(3*x[:,i]**2)-2*x[:,i]/3)
  ur2=br-bx
  nux=mass[:,i]/(x[:,i]**2*bx)+mass[:,i]*bp/(x[:,i]*bx**2)+b*cv*x[:,i]*f[:,i]*ur2/bx**2
  nu=cumulative_trapezoid(nux,x=x[:,i],initial=0)
  mass_outer=mass[-1,i]
  # Continue the physical metric tail to the stated finite outer radius.
  outside=np.linspace(x[-1,i],1.11,513)
  bo=1-cv*(2/(3*outside)+outside**2/3);bpo=cv*(2/(3*outside**2)-2*outside/3)
  nuo=nu[-1]+cumulative_trapezoid(mass_outer/(outside**2*bo)+mass_outer*bpo/(outside*bo**2),x=outside,initial=0)
  max_dn=max(max_dn,float(max(np.max(abs(nu)),np.max(abs(nuo))))*alpha)
  max_dB=max(max_dB,float(np.max(2*alpha*mass[:,i]/x[:,i]/bx)),float(np.max(2*alpha*mass_outer/outside/bo)))
 assert max_dn<1e-6 and max_dB<1e-6
 rows.append({'sign':sign,'dimensionless_mass_tail_per_alpha':float(mass[-1,-1]),'comoving_mass_invariance_error':invariance,'max_abs_delta_nu':max_dn,'max_abs_delta_B_over_B':max_dB,'alpha':alpha,'outer_radius_over_R':1.11,'quadrature':'257 labels, cumulative trapezoid; finite evaluation only'})
OUT.write_text(json.dumps({'all_passed':True,'count':len(checks),'checks':checks,'general_angular_Einstein':str(Gang),'sampled_linear_metrics':rows,'construction':'delta m and delta nu by radial quadrature; pi by inhomogeneous timelike transport; nonzero outer tails permitted','scope':'local finite-patch spherical linear construction, positive packet changes total charge; no nonlinear or fixed-Q stability theorem'},indent=2)+'\n')
print(json.dumps({'all_passed':True,'count':len(checks),'sampled_linear_metrics':rows}))
