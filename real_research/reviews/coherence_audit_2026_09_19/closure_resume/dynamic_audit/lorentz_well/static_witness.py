from pathlib import Path
import sympy as S
import json,sys
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
out.mkdir(exist_ok=True)
n,ep,A,Q0,Q,ss,Y=S.symbols('n epsilon A Q0 Q s Y',positive=True)
U=n*(Q0+ep*S.log(ep*n/A)-ep)
chemical=S.diff(U,n)
assert S.simplify(S.diff(U,n,2)-ep/n)==0
assert S.simplify((n*Q-U).subs(n,A/ep*S.exp((Q-Q0)/ep))-A*S.exp((Q-Q0)/ep))==0
# Auxiliary quadratic action; eliminate density variation from its own equation.
dn,dQ,Y2=S.symbols('delta_n delta_Q Y2',real=True)
L2_aux=dn*dQ-ep*dn*dn/(2*n)-n*Y2/(2*Q)
L2=S.factor(L2_aux.subs(dn,S.solve(S.diff(L2_aux,dn),dn)[0]))
assert S.simplify(L2-n*dQ*dQ/(2*ep)+n*Y2/(2*Q))==0
alpha=S.Rational(1,40000);d=S.Rational(9,5);beta=d/(2-alpha)
y=S.Rational(1,10**8);eps=S.Rational(1,10**9);mu=S.Integer(1);n0=S.Rational(93,50);a0=S.Rational(1,10);Qsq=mu*mu+y
BLold=beta+2*beta*beta*S.sqrt(y)/a0
BLwell=n0/(2*d*mu)*(1+y/mu**2-y/(mu*eps))
BLtotal=BLold+BLwell
static=S.Matrix([[2-alpha,-d],[-d,d*BLtotal]])
oldstatic=S.Matrix([[2-alpha,-d],[-d,d*BLold]])
assert oldstatic.det()>0 and static.det()<0 and static[0,0]>0
# Well temporal Hessian in the coordinate slicing remains positive.
kin=n0*(Qsq/(eps*mu**2)-y/mu**3)
assert kin>0
assert y/Qsq>eps/mu
res={'parameters':{'alpha':str(alpha),'d':str(d),'beta':str(beta),'s':str(mu),'epsilon':str(eps),'n':str(n0),'Y':str(y),'Q_squared':str(Qsq),'a0':str(a0)},'Legendre_potential':str(U),'Legendre_second_derivative':str(S.diff(U,n,2)),'quadratic_auxiliary_action':str(L2_aux),'eliminated_quadratic_action':str(L2),'old_B_L':str(BLold),'well_B_L':str(BLwell),'total_B_L':str(BLtotal),'old_static_determinant':str(oldstatic.det()),'new_static_determinant':str(static.det()),'new_static_determinant_float':float(static.det()),'temporal_well_Hessian':str(kin),'supersonic':True,'scope':'Exact local static principal-block witness at one timelike point; not a full static solution or temporal-instability claim.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
