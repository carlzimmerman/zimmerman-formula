import argparse,json
from pathlib import Path
import sympy as s

def run(mutation):
    checks=[]
    def ck(name,ok,detail):checks.append({'name':name,'passed':bool(ok),'detail':detail})
    X,X0,q,u,p2,B=s.symbols('X X0 q u p2 B',positive=True)
    p0=s.symbols('p0',real=True)
    P=p0+p2*(X-X0)**2/2
    px=s.diff(P,X);pxx=s.diff(px,X)
    ck('critical energy fixed',s.simplify((2*X*px-P).subs(X,X0)+p0)==0,'ρφ=−P0')
    xp=X0-u**2/2
    current=s.simplify(px.subs(X,xp)*u)
    if mutation=='quadratic_flux': current=-p2*u**2/2
    ck('smooth rolling static current',s.simplify(current+p2*u**3/2)==0,'cubic, notquadratic')
    kt=px+2*X*pxx
    ck('finite temporal coefficient',s.simplify(kt.subs(X,X0)-2*X0*p2)==0,'positivePXX givespositiveK_t')
    ck('static transverse sign',s.simplify(px.subs(X,xp)+p2*u**2/2)==0,'negative forp2>0')
    ck('static radial sign',s.simplify((px-u**2*pxx).subs(X,xp)+3*p2*u**2/2)==0,'negative forp2>0')
    n=s.symbols('n',integer=True,positive=True);M,r=s.symbols('M r',positive=True)
    formal=M**s.Rational(1,3)*r**(-(n-1)/3)
    ck('smooth flux exponents',s.simplify(M*s.diff(formal,M)/formal-s.Rational(1,3))==0 and s.simplify(r*s.diff(formal,r)/formal+(n-1)/3)==0,'general-n exponents')
    Pmond=p0-B*(X0-X)**s.Rational(3,2)
    mx=s.diff(Pmond,X);mxx=s.diff(mx,X)
    ck('shifted cubic MOND current',s.simplify(mx.subs(X,xp)*u-3*B*u**2/(2*s.sqrt(2)))==0,'u>0branch')
    ck('shifted cubic temporal divergence',s.limit((mx+2*X*mxx).subs(X,xp),u,0)==-s.oo,'X0>0')
    ck('opposite cubic flips flux',s.simplify(s.diff(-Pmond,X).subs(X,xp)*u+3*B*u**2/(2*s.sqrt(2)))==0,'nohealthypositiveflux repair bysign')
    Z=s.symbols('Z',positive=True)
    ck('clockless cubic temporal coefficient differs',s.simplify((mx+2*X*mxx).subs({X0:0,X:-Z})-3*B*s.sqrt(Z))==0,'X0=0, Xnegative isdifferentbranch')
    return {'all_passed':all(c['passed'] for c in checks),'checks':checks,'mutation':mutation,'non_claims':['Frozen scalarblock only','No fullmetricconstraints','No 32pi derivation']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutation',default='none',choices=['none','quadratic_flux']);a=p.parse_args();o=run(a.mutation);Path(a.output).write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({'all_passed':o['all_passed'],'checks':len(o['checks'])}));raise SystemExit(0 if o['all_passed'] else 1)
