import argparse,json
from pathlib import Path
import sympy as s

def run(mutation):
    checks=[]
    def ck(name,ok,detail): checks.append({'name':name,'passed':bool(ok),'detail':detail})
    a,e,b,g,x=s.symbols('a e b g x',positive=True)
    expr=a*(s.sqrt(e**2+4*b/a)-e)/2
    ck('exact radial root',s.simplify(e*expr+expr**2/a-b)==0,'εg+g²/a=b')
    coeff=s.diff(expr,b).subs(b,0)
    if mutation=='drop_linear': coeff=s.oo
    ck('regular weak-source susceptibility',s.simplify(coeff-1/e)==0,'finite1/ε whenε>0')
    ck('second weak-source coefficient',s.simplify(s.diff(expr,b,2).subs(b,0)/2+1/(a*e**3))==0,'−1/(aε³)')
    slope=(e+g/a)/(e+2*g/a)
    ck('implicit logarithmic derivative',s.simplify((e*g+g**2/a)/(g*(e+2*g/a))-slope)==0,'source derivative at fixedradius')
    ck('linear to fractional limits',s.limit(slope,g,0)==1 and s.limit(slope,g,s.oo)==s.Rational(1,2),'1 to1/2')
    ck('flux crossover',s.simplify((e*g+g**2/a).subs(g,e*a)-2*e**2*a)==0,'equal fluxes atb2ε²a')
    ratio=s.sqrt(x/(1+x))
    ck('MOND relative response',s.simplify((g**2/(a*(e*g+g**2/a))).subs(g,x*e*a)-ratio**2)==0,'ratio²=x/(1+x)')
    for delta in [s.Rational(1,100),s.Rational(1,20),s.Rational(1,10)]:
        xm=(1-delta)**2/(1-(1-delta)**2)
        ck('tolerance '+str(delta),s.simplify(ratio.subs(x,xm)-(1-delta))==0,str(xm))
    ck('noncommuting normalized limits',s.limit(expr/s.sqrt(b),b,0)==0 and s.simplify(s.limit(expr,e,0)/s.sqrt(b)-s.sqrt(a))==0,'fixedεthenweaksource differsεzero first')
    d=s.symbols('d',integer=True,positive=True)
    r,GN,M=s.symbols('r GN M',positive=True)
    deep=s.sqrt(a*GN*M/r**(d-2))
    ck('general-d mass exponent',s.simplify(M*s.diff(deep,M)/deep-s.Rational(1,2))==0,'fixedradius and coefficients')
    return {'all_passed':all(c['passed'] for c in checks),'checks':checks,'mutation':mutation,'non_claims':['Does not establish invertibility in any relativistic theory','No high-acceleration calibrated interpolation','No 32pi selection']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutation',default='none',choices=['none','drop_linear']);a=p.parse_args();o=run(a.mutation);Path(a.output).write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({'all_passed':o['all_passed'],'checks':len(o['checks'])}));raise SystemExit(0 if o['all_passed'] else 1)
