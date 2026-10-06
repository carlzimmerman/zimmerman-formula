import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['harmonic','boundary','projector']);args=ap.parse_args()
rows=[]
def check(name,value): rows.append({'name':name,'passed':bool(value)})
def zero(e): return s.factor(e)==0
# Noncommuting actual SPD leaf metrics and a nonsingular basis map.
x=s.Matrix([[3,1],[1,2]]);y=s.Matrix([[2,0],[0,4]]);h=(x+y)/2;d=(x-y)/2;lam=s.Rational(2,3);hl=h+lam*d*h.inv()*d;q=s.Matrix([[1,2],[0,1]])
xq=q.T*x*q;yq=q.T*y*q;hq=(xq+yq)/2;dq=(xq-yq)/2
check('noncommuting_fixture',x*y!=y*x)
check('positive_leaf_metric_fixture',hl[0,0]>0 and hl.det()>0)
check('basis_congruence',hq+lam*dq*hq.inv()*dq==q.T*hl*q)
check('inverse_basis_congruence',(hq+lam*dq*hq.inv()*dq).inv()==q.inv()*hl.inv()*q.T.inv())
check('exchange_symmetry',h+lam*(-d)*h.inv()*(-d)==hl)
check('arithmetic_inverse_schur_identity',(x.inv()+y.inv())/2==(h-d*h.inv()*d).inv())
check('inverse_below_harmonic_fixture',(h.inv()-hl.inv())[0,0]>=0 and (h.inv()-hl.inv()).det()>=0)
eps=s.symbols('eps');hinv=h.inv();d0=s.Matrix([[1,2],[2,-1]])
# Derivative at coincidence is zero: action difference times squared acceleration is >= quartic.
diff=((h+eps*d0).inv()+(h-eps*d0).inv())/2-(h+lam*eps**2*d0*hinv*d0).inv()
check('coincidence_inverse_equal',diff.subs(eps,0)==s.zeros(2))
check('no_first_inverse_difference',diff.diff(eps).subs(eps,0)==s.zeros(2))
# Solve the complete leading auxiliary variational equations directly.
g,j,Ga,ell,e,A,B,D,H,H2=s.symbols('g j Gamma ell e A B D H H2',positive=True)
u,ng,nh,c,w,cd,wd=s.symbols('u ng nh chi w chid wd');Y=cd+e*w;Tw=wd-e*w
L0=2*g*(u+c)*ng+2*j*u*nh+Ga*(Y-ell*u+ng-nh)**2
sol=s.solve([s.diff(L0,v) for v in (u,ng,nh)],(u,ng,nh),simplify=False)
a=g/(g+j);r=j/(g+j);T=g*j/(g+j);E=B*r*r+D*a*a
check('actual_leading_aux_solution_u',zero(sol[u]+a*c))
check('actual_leading_aux_solution_ng',zero(sol[ng]+r*Y+r*(2*a*ell+T/Ga)*c))
check('actual_leading_aux_solution_nh',zero(sol[nh]-a*Y-a*(ell*(1-2*r)+T/Ga)*c))
L0red=s.factor(L0.subs(sol));check('actual_leading_spatial_action',zero(L0red+2*T*c*Y+T*(2*a*ell+T/Ga)*c*c))
L1=A*Tw**2+(A+B)*ng**2-2*A*Tw*ng+D*nh**2
L1red=L1.subs(sol)
check('actual_velocity_gram',zero(L1red.diff(wd,2)/2-A) and zero(L1red.diff(cd,2)/2-(A*r*r+E)) and zero(L1red.diff(wd,cd)/2-A*r))
# Integrate the leading cross with evolving T; take its gradient Schur complement.
Tdot=T*(r*(H-e)+a*(2*ell+H2))
if args.control=='boundary': Tdot=s.Integer(0)
S=s.factor(T*(2*a*ell+T/Ga)-Tdot-(T*e)**2/(g*e))
check('evolving_gradient_schur',zero(S-T*(T/Ga-r*H-a*H2)))
pg,ph,M,av,L,hhat,lp=s.symbols('Pg Ph M av L hhat lambda',positive=True)
gv=M*av**3*pg*H;jv=M*av**3*ph*H2 # L*b^3=a^3 on Q=1.
Gc=M*av**3*pg*ph/(pg+ph);delta=(pg-ph)**2/(pg+ph)**2
check('Q1_actual_threshold',zero((T/(r*H+a*H2)).subs({g:gv,j:jv})-Gc))
Gl=Gc/(1+lp*delta)
if args.control=='projector': Gl=M*av**3*(pg+ph)/4
Sl=T*(T/Gl-r*H-a*H2)
check('new_geometric_stiffness',zero((Sl-lp*T*(r*H+a*H2)*delta).subs({g:gv,j:jv})))
ratio=s.Rational(1,4);Lv=s.Rational(1,8);eta=s.Rational(1,4);b0=3*(1-eta)/eta
c2=lp*ratio*Lv**2*(1-ratio)**2/(b0*(1+ratio)*(1+ratio**2*Lv**2))
check('admitted_relative_speed',zero(c2-lp/s.Integer(5125)))
if args.control=='harmonic': check('false_harmonic_strict_gradient',s.Integer(0)>0)
p=s.symbols('p',positive=True)
C=s.Matrix([[p*Ga*ell**2,p*(g-Ga*ell),p*(j+Ga*ell)],[p*(g-Ga*ell),A+B+p*Ga,-p*Ga],[p*(j+Ga*ell),-p*Ga,D+p*Ga]])
det=s.Poly(s.expand(C.det()),p)
check('finite_k_low_determinant',zero(det.nth(1)-Ga*ell**2*(A+B)*D))
check('finite_k_high_determinant',zero(det.nth(3)+Ga*(g+j)**2))
result={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'Covariant geometry and analytic constrained UV radiation repair; no full finite-k/source/cold/32pi closure'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total'],'failures':[x['name'] for x in rows if not x['passed']]}))
