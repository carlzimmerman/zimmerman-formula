import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
r,A,g,w=s.symbols('r A gamma Wp',positive=True)
H=r*r/2+(A*r-1-g*r*r)**2/(2*g);h=s.diff(H,r);R=s.diff(h,r);c2=h/(r*R);f=w*(1+c2)/r**2
at={r:1,A:s.Rational(11,10),g:s.Rational(1,10)}
a,b,alpha,beta=s.symbols('a b alpha beta',real=True)
rr=s.exp(-alpha)*s.sqrt(a*a-b*b)
m=s.exp(2*beta)*h.subs(r,rr)*a/rr
dm=s.exp(2*beta-2*alpha)*(R.subs(r,rr)*a*a*rr-h.subs(r,rr)*b*b)/rr**3
t,x=s.symbols('t x');ph=s.Function('phi')(t,x);AA=s.Function('A')(t,x);PP=s.Function('Pi')(t,x)
# Topological Euler coefficient for delta Pi: -dt(A phi_x)+dx(A phi_t).
epi=-s.diff(AA*s.diff(ph,x),t)+s.diff(AA*s.diff(ph,t),x)
# Divergence of A curl Pi.
dtop=s.diff(AA*s.diff(PP,x),t)-s.diff(AA*s.diff(PP,t),x)
checks={'R_local':R.subs(at)==s.Rational(91,10),'c_squared_local':s.simplify(c2.subs(at))==s.Rational(10,91),'c_squared_derivative':s.simplify(s.diff(c2,r).subs(at))==s.Rational(7911,8281),'loop_coefficient':s.simplify(s.diff(f,r).subs(at)/w)==-s.Rational(10471,8281),'Legendre_derivative':s.simplify(s.diff(m,a)-dm)==0,'Pi_topological_variation':s.simplify(epi-(s.diff(ph,t)*s.diff(AA,x)-s.diff(ph,x)*s.diff(AA,t)))==0,'current_product_identity':s.simplify(dtop-(s.diff(AA,t)*s.diff(PP,x)-s.diff(AA,x)*s.diff(PP,t)))==0}
out={'checks':checks,'all_pass':all(checks.values()),'scope':'Exact algebra only; no postbreak existence, uniqueness, or dynamically realized loop.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass'] else 1)
