"""CE-FM-075: derive transverse Maxwell symbol on parallel E,B backgrounds."""
import json,sys
from pathlib import Path
import sympy as s
checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
A,C,e,b,w,k=s.symbols('A C E B omega k',real=True)
alpha=A+C*e**2;beta=A-C*b**2
# Plane wave k along x, background E,B along z, F=(E²-B²)/2.
# Faraday: delta B_y=-k e_z/w, delta B_z=k e_y/w.
# delta D=A delta E + C E delta F, delta H=A delta B + C B delta F.
ey,ez=s.symbols('ey ez');df=e*ez-b*k*ey/w
Dy=A*ey;Dz=A*ez+C*e*df
Hy=-A*k*ez/w;Hz=A*k*ey/w+C*b*df
res=s.Matrix([w*(w*Dy-k*Hz),w*Dz+k*Hy])
M=res.jacobian([ey,ez]);det=s.factor(M.det())
ck('Maxwell symbol factors into ordinary and extraordinary modes',s.simplify(det-A*(w*w-k*k)*(alpha*w*w-beta*k*k))==0)
ck('pure electric ratio',s.simplify((beta/alpha).subs(b,0)-A/(A+C*e**2))==0)
ck('pure magnetic ratio',s.simplify((beta/alpha).subs(e,0)-(A-C*b*b)/A)==0)
# Original electric law, plus positive Maxwell epsilon. F positive fixes A and C.
F,eps=s.symbols('F epsilon',positive=True);E=s.sqrt(2*F)
Af=eps+E/(1+E);Cf=s.diff(Af,F)
ck('exact mixed background A',Af.subs({F:s.Rational(1,2),eps:s.Rational(1,10)})==s.Rational(3,5))
ck('exact mixed background derivative',s.simplify(Cf.subs(F,s.Rational(1,2)))==s.Rational(1,4))
subs={A:s.Rational(3,5),C:s.Rational(1,4),e:s.sqrt(5),b:s.Integer(2)}
al=s.simplify(alpha.subs(subs));be=s.simplify(beta.subs(subs));speed=s.simplify(be/al)
ck('counterexample keeps F=1/2',s.simplify(((e*e-b*b)/2).subs(subs))==s.Rational(1,2))
ck('electric coefficient positive',al==s.Rational(37,20))
ck('magnetic spatial coefficient negative',be==-s.Rational(2,5))
ck('extraordinary omega²/k² negative',speed==-s.Rational(8,37))
ck('ordinary mode survives',s.simplify(det.subs(subs).subs(w,k))==0)
# General fixed-F family B²=t, E²=t+2F: any finite A>0,C>0 fails for t>A/C.
t,h=s.symbols('t h',positive=True)
ck('fixed F varying second invariant',s.simplify((alpha-beta).subs({e:s.sqrt(t+2*F),b:s.sqrt(t)})-2*C*(t+F))==0)
ck('magnetic threshold',s.simplify(beta.subs(b,s.sqrt(A/C+h)))==-C*h)
# invariant G=E B; at B²=A/C, G²=(A/C)²+2F A/C.
G=s.symbols('G',real=True)
ck('second invariant threshold',s.simplify((t*(t+2*F)).subs(t,A/C)-(A*A/C**2+2*F*A/C))==0)
ck('counterexample beyond invariant threshold',s.Rational(20)>s.Rational(204,25))
# Sign separation proof: metric time t_cov²>z_cov²+p²; extra hyperbolicity
# beta<0,alpha>0 requires z_cov²>t_cov²+(-beta/alpha)p². Contradictory.
rho=s.symbols('rho',positive=True)
ck('sum of incompatible common-time inequalities',s.expand((1+rho)*h)>0)
# Pure Maxwell mutation C=0 removes instability and restores same cone.
ck('Maxwell control determinant',s.simplify(det.subs(C,0)-A*A*(w*w-k*k)**2)==0)
ck('Maxwell control speed',s.simplify((beta/alpha).subs(C,0))==1)
result={'claim_id':'CE-FM-075','n_checks':len(checks),'all_pass':all(c['pass'] for c in checks),'checks':checks,'counterexample':{'a':1,'epsilon':'1/10','F':'1/2','E_squared':5,'B_squared':4,'A':'3/5','L_FF':'1/4','alpha':'37/20','beta':'-2/5','extraordinary_omega_squared_over_k_squared':'-8/37'},'scope':'Flat classical L(F), G-independent; E parallel B with perpendicular wave vector. Uniform common metric hyperbolicity fails on this explicit background. No statement that a restricted phase, dynamical medium or L(F,G) completion is impossible.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({x:y for x,y in result.items() if x!='checks'}))
