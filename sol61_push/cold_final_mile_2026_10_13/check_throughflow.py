"""CE-FM-005 formal stationary flow and retained-mass receiver consistency."""
import json,sys
from pathlib import Path
import numpy as np
import sympy as s

checks=[]
def check(name,condition,detail):
    checks.append(dict(name=name,passed=bool(condition),detail=detail))
    if not condition:raise AssertionError(name)
r=s.symbols('r',positive=True)
M0=(s.sqrt(1+4*r*r)-1)/2
u0=M0/r**2
u=s.symbols('u',positive=True)
R=u*u/(1-u);Rp=s.diff(R,u)
mu=-r**2*s.diff(M0,r,2)/(Rp.subs(u,u0)*s.diff(M0,r)**3)
simple=-(s.sqrt(1+4*r*r)-1)**2/(16*r*s.sqrt(1+4*r*r))
check('exact leading mass correction',s.simplify(mu-simple)==0,str(simple))
check('exact derivative ratio',s.simplify(s.diff(M0,r,2)/s.diff(M0,r)**3-1/(4*r**3))==0,'M0_doubleprime/M0_prime^3=1/(4r^3)')
check('exact large-radius mass offset',s.limit(simple,r,s.oo)==-s.Rational(1,8),'-1/8')
funcs=[s.lambdify(r,s.diff(expr,r,order),'numpy') for expr in (M0,simple) for order in range(3)]
rs=np.geomspace(2,50,2001)
m0,p0,q0,mm,mp,mq=[f(rs) for f in funcs]
check('numerical correction sign',np.all(mm<0),float(np.max(mm)))
rows=[]
for F in (.015,.03,.05,.1,.15,.3):
    m=m0+F*F*mm;p=p0+F*F*mp;q=q0+F*F*mq
    uu=m/rs**2
    residual=uu**2/(1-uu)-1/rs**2+F*F*q/p**3
    maximum=float(np.max(np.abs(residual)*rs**2))
    check(f'flow comparison domain F={F}',np.all((uu>0)&(uu<1)&(p>0)),{'max_u':float(np.max(uu))})
    rows.append(dict(F=F,max_normalized_residual=maximum,mass_offset_at_50=float(m[-1]-m0[-1]),
                     minimum_speed=float(np.min(F/p)),maximum_speed=float(np.max(F/p))))
ratio=rows[1]['max_normalized_residual']/rows[0]['max_normalized_residual']
check('quartic residual scaling',abs(ratio/16-1)<.05,ratio)

rr,rsink=s.symbols('R r_s',positive=True)
geom=rr**2/(rr-rsink)
check('capacity minimizer',s.simplify(s.diff(geom,rr).subs(rr,2*rsink))==0,'R=2r_s')
check('capacity minimum identity',s.simplify(geom-4*rsink-(rr-2*rsink)**2/(rr-rsink))==0,
      'R^2/(R-r_s)-4r_s=(R-2r_s)^2/(R-r_s)>=0 for R>r_s')
budget=[]
for outer in (5.,20.,50.):
    halo=float((np.sqrt(1+4*outer**2)-1)/2)
    budget.append(dict(outer=outer,halo_mass=halo,growth_time_over_residence_time=1/halo,
                       max_fraction_processed_for_receiver_mass_increase_0_01=.01/halo))
    check(f'one full replacement exceeds central target budget R={outer}',halo>.01,halo)
result=dict(checks=checks,formal_flow=rows,receiver_budget=budget,
            scope='Formal small-flux local expansion, geometry identity and retained-mass budget; no stationary flow existence or formation proof.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
