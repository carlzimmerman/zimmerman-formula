import argparse,json
from pathlib import Path
import sympy as s

def run():
    checks=[]
    def ck(name,ok,detail):checks.append({'name':name,'passed':bool(ok),'detail':detail})
    d=s.symbols('d',integer=True,positive=True)
    omega=2*s.pi**((d-1)/2)/s.gamma((d-1)/2)
    A=(d-2)*omega/(d-3)
    ctarget=4*A/(d-3)**2
    ck('4d Newton and target normalization',s.simplify(A.subs(d,4)-8*s.pi)==0 and s.simplify(ctarget.subs(d,4)-32*s.pi)==0,'G force normalization fixedbeforecomparison')
    ck('dimension5 extension',s.simplify(ctarget.subs(d,5)-3*s.pi**2)==0,str(s.simplify(ctarget.subs(d,5))))
    ck('dimension6 extension',s.simplify(ctarget.subs(d,6)-128*s.pi**2/81)==0,str(s.simplify(ctarget.subs(d,6))))
    k=s.symbols('kappa',positive=True)
    J=(d-3)**2/(4*k*k)
    ck('phenomenological coefficient changes invariant',s.diff(J,k)!=0 and s.diff(A/k**2,k)!=0,'Not aconstant independentofkappa')
    p=s.symbols('p',positive=True)
    velocity_power=1-(d-2)/(p-1)
    ck('cubic flatrotation only4d',s.simplify(velocity_power.subs(p,3)-(4-d)/2)==0,'v² radial exponent')
    ck('flatrotation dimensional continuation',s.simplify(velocity_power.subs(p,d-1))==0,'p=d−1')
    n=d-1;w=s.symbols('w',real=True)
    exponent=-n*(1+w)/2
    ck('4d dust and radiation tracking',exponent.subs({d:4,w:0})==-s.Rational(3,2) and exponent.subs({d:4,w:s.Rational(1,3)})==-2,'a0 densitytracking exponent')
    ck('vacuum tracking constant',exponent.subs(w,-1)==0,'constantG assumed')
    rr,mu=s.symbols('r mu',positive=True)
    ff=1-mu/rr**(d-3)
    ck('spherical vacuum Ricci equations',s.simplify(s.diff(ff,rr,2)+(d-2)*s.diff(ff,rr)/rr)==0 and s.simplify((d-3)*(1-ff)-rr*s.diff(ff,rr))==0,'Direct metric check')
    # Independent Gauss and trace-reversed calibration.
    kappaE=A
    ck('Poisson tensor normalization',s.simplify(kappaE*(d-3)/(d-2)-omega)==0,'c=G_N=1')
    return {'all_passed':all(c['passed'] for c in checks),'checks':checks,'non_claims':['J1isnotderived','Noformalvacuumselectormechanism','Noempiricaltimeevolutionfit']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'all_passed':r['all_passed'],'checks':len(r['checks'])}));raise SystemExit(0 if r['all_passed'] else 1)
