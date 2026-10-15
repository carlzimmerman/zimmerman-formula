"""Exact algebraic controls for the occupied center patch; sign proof is analytic."""
import json
from pathlib import Path
import sys
import sympy as s
E,D0,h,B,w=s.symbols('E D0 h B w', positive=True)
t=D0/(D0+E); p=t*t; x=1-t; hc=D0**2*x**3/(1-x)**2
def N(beta): return h*(p-beta)-E**2*(t-beta)*(t-p)
def F(beta): return p-beta-E**2*(t-beta)**2/(h+E**2*(t-beta))
checks=[]
def exact(name,expr):
    assert s.factor(expr)==0,(name,s.factor(expr))
    checks.append(name)
exact('critical identity',hc-E**2*x)
exact('cone numerator',F(B)*(h+E**2*(t-B))-N(B))
exact('affine blend',N(w/s.Integer(4)+(1-w)*B)-w*N(s.Rational(1,4))-(1-w)*N(B))
betaL=p*(h-hc)/(h-E**2*(t-p))
exact('parent lightcone boundary',N(betaL))
exact('cone derivative',s.diff(F(B),B)+h**2/(h+E**2*(t-B))**2)
a2=D0**2*h/(16*(D0**2+h))
exact('electric scale bound',D0**2/16-a2-D0**4/(16*(D0**2+h)))
exact('inertia scale bound',h/16-a2-h**2/(16*(D0**2+h)))
exact('constant quarter margin',s.Rational(16,25)-s.Rational(1,4)-s.Rational(1,16)-s.Rational(131,400))
exact('branch safety bound',s.Rational(1,16)*s.Rational(1,5)-s.Rational(1,80))
parent=betaL*h/(h+hc)
exact('parent zero field value',s.limit(parent,E,0)-1)
exact('parent zero field slope',s.limit(s.diff(parent,E),E,0)+2/D0)
Le=D0*E-D0**2*s.log(1+E/D0)
exact('electric second derivative at zero',s.diff(Le,E,2).subs(E,0)-1)
exact('electric radial cubic coefficient',s.diff(Le,E,3).subs(E,0)/6+1/(3*D0))
exact('patched zero field gauge speed square',s.Rational(1,4)/1-s.Rational(1,4))
z=s.symbols('z',positive=True)
exact('noncontinuous vacuum coefficient path',s.limit(parent.subs({D0:1,h:z*z}).subs(E,z/(4*s.sqrt(1+z*z))),z,0)-1)
# Finite controls use interior points of the blend domain; they do not prove it.
controls=[]
for hv in [s.Rational(1,1000),s.Integer(1),s.Integer(1000)]:
    av=s.sqrt(a2.subs({D0:1,h:hv}))
    ev=av*s.Rational(3,4)
    bp=parent.subs({D0:1,h:hv,E:ev})
    for weight in [s.Rational(0),s.Rational(1,3),s.Rational(1,2),s.Rational(1)]:
        bv=weight/s.Integer(4)+(1-weight)*bp
        v=F(bv).subs({D0:1,h:hv,E:ev})
        assert v.evalf(50)>0
        controls.append({'h_over_D0_squared':str(hv),'weight':str(weight),'cone_margin':str(v.evalf(22))})
Path(sys.argv[1]).write_text(json.dumps({'claim_id':'AS2-PATCH-001','exact_identity_count':len(checks),'identities':checks,'blend_controls':controls,'scope':'Chosen occupied-phase magnetic response; no vacuum or nonlinear stability theorem.'},indent=2)+'\n')
print(f'PASS: {len(checks)} exact identities and {len(controls)} blend controls.')
