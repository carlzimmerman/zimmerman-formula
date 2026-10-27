"""CE-FM-014 reciprocal NR current/dipole coupling has an indefinite velocity block."""
import json,sys
from pathlib import Path
import sympy as s

rho,lam=s.symbols('sigma curvature',positive=True)
v,w,xi,px,pi=s.symbols('v xidot xi p_eta p_xi',real=True)
L=rho*v*v/2+rho*v*w-lam*rho*rho*xi*xi/2
Hess=s.hessian(L,(v,w));checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)
check('nonsingular indefinite Hessian',s.simplify(Hess.det()+rho*rho)==0,str(Hess))
mom={px:s.diff(L,v),pi:s.diff(L,w)}
sol=s.solve((s.Eq(px,mom[px]),s.Eq(pi,mom[pi])),(v,w),dict=True)[0]
Ham=s.simplify((px*v+pi*w-L).subs(sol))
expected=px*pi/rho-pi*pi/(2*rho)+lam*rho*rho*xi*xi/2
check('independent momentum inversion',s.simplify(Ham-expected)==0,str(Ham))
qdot=s.symbols('qdot',real=True)
check('diagonalized negative internal kinetic',s.simplify(L.subs(v,qdot-w)-rho*qdot*qdot/2+rho*w*w/2+lam*rho*rho*xi*xi/2)==0,
      'L=sigma qdot^2/2-sigma xidot^2/2-W; q=eta+xi')
epsilon=s.symbols('epsilon',positive=True)
check('small negative energy direction',s.simplify(Ham.subs({px:0,pi:rho*epsilon,xi:0})+rho*epsilon*epsilon/2)==0,
      'H=-sigma epsilon^2/2 at arbitrarilysmall epsilon')
check('positive potential gives growing internal mode',s.simplify(s.diff(L,xi)/(-rho)-lam*rho*xi)==0,
      'afterconserved qmomentum: xi_ddot=curvature*sigma*xi')
k=s.symbols('kappa',real=True)
extended=s.hessian(L+k*rho*w*w/2,(v,w))
check('extra coefficient threshold',s.simplify(extended.det()-rho*rho*(k-1))==0,'Sylvester: sigma>0 andkappa>1 needed')
rows=[]
for val in (s.Integer(0),s.Rational(1,2),s.Integer(1),s.Integer(2)):
    rows.append(dict(kappa=str(val),determinant_over_sigma_squared=str(s.simplify(extended.det()/rho**2).subs(k,val)),
                     eigenvalues_over_sigma=[str(e) for e in (extended/rho).subs(k,val).eigenvals()]))
result=dict(checks=checks,NR_velocity_hessian=str(Hess),NR_Hamiltonian=str(Ham),additional_term_comparison=rows,
            scope='Locally homogeneous transverse NR dipolarvelocity sector; not fullGRconstraint or quantumvacuum classification. Addedkineticterm remains hypothetical.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
