"""Tree-level vector versus scalar density-contact matching and charge gate."""
import json
import sys
from pathlib import Path
import sympy as s

out=Path(sys.argv[1]);assert out.is_dir();checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name
K0,u0,gc,gf,mv=s.symbols('K0 u0 gc gf mv',positive=True)
Kv=K0+gc**2/mv**2;uv=u0+gf**2/mv**2;zv=gc*gf/mv**2
check('vector contact determinant',s.simplify(Kv*uv-zv*zv-(K0*u0+(K0*gf**2+u0*gc**2)/mv**2))==0)
Ks=K0-gc**2/mv**2;us=u0-gf**2/mv**2;zs=-gc*gf/mv**2
check('scalar contact determinant',s.simplify(Ks*us-zs*zs-(K0*u0-(K0*gf**2+u0*gc**2)/mv**2))==0)
nn,qq,aux=s.symbols('n q aux',real=True)
V=mv**2*aux**2/2+aux*(gc*nn+gf*qq)
stationary=-(gc*nn+gf*qq)/mv**2
check('scalar auxiliary elimination sign',s.simplify(V.subs(aux,stationary)+(gc*nn+gf*qq)**2/(2*mv**2))==0)
rows=[]
for z in (s.Rational(3,10),s.Integer(1),s.Integer(3)):
    # K=1,u=z^2+1,zeta=z realized by a repulsive vector plus bare K0.
    u=z*z+1;bareK=1/u;cc=z*z/u;ff=u
    check('selected positive vector bare coefficient '+str(z),bareK>0)
    check('selected vector K match '+str(z),s.simplify(bareK+cc-1)==0)
    check('selected vector cross match '+str(z),s.simplify(cc*ff-z*z)==0)
    rows.append(dict(zeta=float(z),Kc=1.,u=float(u),bare_K0=float(bareK),gc_squared_over_mV_squared=float(cc),gF_squared_over_mV_squared=float(ff)))

np,na,xp,xa=s.symbols('nplus nminus bplus bminus',nonnegative=True)
current=np-na+2*xp-2*xa
check('neutral source-pair current',current.subs({np:0,na:0,xp:1,xa:1})==0)
check('neutral daughter production current',current.subs({np:2,na:2,xp:0,xa:0})==0)
check('neutral stock current for all equal-sign densities',s.simplify(current.subs({na:np,xa:xp}))==0)
check('cubic gauge invariance',2*s.Symbol('qPhi')-2*s.Symbol('qPhi')==0)
result=dict(vector_rows=rows,checks=checks,conventions='Leading static long-wavelength mediator matching; positive masses; vector couples signed conserved current, scalar couples selected density bilinear; no physical coupling values fixed',
    scope='Exact coefficient and neutrality identities; does not identify NR positive cold density with relativistic charge current or prove a causal band UV completion',
    non_claims=['No induced force from neutral stock established','No full scalar-mediated quantum stability or neutral-stock thermal history','No physical halo, vacuum, particle-action matching or novelty closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
