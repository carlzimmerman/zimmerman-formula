from pathlib import Path
import json,sys
import sympy as s

dest=Path(sys.argv[1]);checks=[]
def z(name,e):
 r=s.simplify(s.expand(e));checks.append({'name':name,'passed':r==0,'residual':str(r)})
def yes(name,c):checks.append({'name':name,'passed':bool(c),'condition':str(c)})
a,X0,r0,d,beta,zz=s.symbols('a X0 rho0 d beta z',positive=True)
rho=r0+2*a*X0*d+s.Rational(3,2)*a*d*d;p=-r0+a*d*d/2;e=rho-r0;pd=p+r0
R=rho/r0;P=-p/r0;param={d:X0*zz,a:beta*r0/(2*X0*X0)}
z('density bridge exact normalized a0 squared',R.subs(param)-(1+beta*zz+3*beta*zz*zz/4))
z('minus-pressure bridge exact normalized a0 squared',P.subs(param)-(1-beta*zz*zz/4))
z('density minus pressure readout equals enthalpy',(R-P)-(rho+p)/r0)
z('dimensionless bridge separation',(R-P).subs(param)-beta*zz*(1+zz))
z('density readout linear response at ground',s.diff(R,d).subs(d,0)-2*a*X0/r0)
z('minus-pressure zero linear response',s.diff(P,d).subs(d,0))
z('minus-pressure quadratic response',s.diff(P,d,2)+a/r0)
yes('density and minus-pressure responses differ for prepared buffer',s.simplify((R-P).subs(param)).is_positive)
z('constant-offset bridge has no deposit response',s.diff(r0/r0,d))
eps=s.symbols('epsilon',real=True)
z('DE deviation lower bound margin',(rho+p)/rho-e/rho-pd/rho)
z('exact tolerance budget margin',eps*rho-(rho+p)-(eps*r0-(1-eps)*e-pd))
yes('finite deposit correction in capacity margin is positive',pd.is_positive)
# Mobility is a constitutive input, not a coupling derived here.
mu,u,h,ss=s.symbols('mu u h s',positive=True)
qdot=mu*u*u*ss;pidot=-mu*h*u*ss
z('separable bracket cancels total energy',h*qdot+u*pidot)
z('separable bracket entropy production',ss*qdot-mu*u*u*ss*ss)
yes('positive cold energy import',s.simplify(h*qdot).is_positive)
yes('same event leaves positive-phase healthy ground outward',pidot.is_negative)
yes('uncoupled ghost shift source cannot equal this nonzero rate',pidot!=0)
# Mathematical fixed-volume bookkeeping, with physical floor as a premise.
Ei,Ef,Qc,Fout,base,bi,bf=s.symbols('Ei Ef Qcold Fout Ebase buffer_initial buffer_final',real=True)
ledger=Ei-Ef-Fout
z('exact open-volume gain with excess-energy buffers',ledger.subs({Ei:base+bi,Ef:base+bf})-(bi-bf-Fout))
z('capacity margin equals final buffer',(bi-Fout)-(bi-bf-Fout)-bf)
yes('mutation deleting outward flux detected',s.simplify(ledger-(Ei-Ef))!=0)
z('unbuffered zero-flux gain is minus finalbuffer',(bi-bf-Fout).subs({bi:0,Fout:0})+bf)
out={'all_passed':all(x['passed'] for x in checks),'check_count':len(checks),'checks':checks,
 'derived_inequalities':{'DE_budget':'For rho0>0,e>=0,pdep>=0,0<=epsilon<1 and (e+pdep)/(rho0+e)<=epsilon: e<=epsilon*rho0/(1-epsilon). Hypotheses explicit; this is algebraic necessary capacity, not a selected physical tolerance.','flux_budget':'Finalbuffer>=0 implies Qcold<=initialbuffer−netoutwardflux. Incoming flux is negative Fout and can replenish.','branch_boundary':'For mu>0,u0>0,h*s>0: coldpower>0 and Pi_dot<0 at Pi0=0. Positivephase healthy Pi>=0 requires an actual boundary/coupling rule.'},
 'scope':'Exact bridge/state and constitutive admission identities. Pressure readout is a physical real-acceleration prescription only if minus p>=0; DE-like epsilon<1 ensures this. No derived bridge choice, action/collision rate, global dynamics, gravitational work, observational tolerance or all-reservoir no-go.'}
(dest/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':out['all_passed'],'check_count':len(checks)}));assert out['all_passed']
