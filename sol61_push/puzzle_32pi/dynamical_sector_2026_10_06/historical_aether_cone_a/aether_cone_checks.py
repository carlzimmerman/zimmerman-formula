import argparse,json
from pathlib import Path
import sympy as s

def run(mutation):
    rows=[]
    def ck(name,ok,detail):rows.append({'name':name,'passed':bool(ok),'detail':detail})
    n=s.symbols('n',integer=True,positive=True);lam,eta,v,t,z=s.symbols('lam eta v t z',real=True)
    temporal=n*(1-n*lam)*v**2+2*(n*lam-1)*v*t+(1-lam)*t**2
    shift=(n*lam-1)*v/(lam-1)
    A=(n-1)*(n*lam-1)/(lam-1)
    ck('shift equation',s.simplify(s.diff(temporal,t).subs(t,shift))==0,'ΔB solved λneq1')
    ck('reduced scalar kinetic',s.simplify(temporal.subs(t,shift)-A*v**2)==0,'general-n')
    spatial=(n-1)*(n-2)*z**2+2*(n-1)*t*z+eta*t**2
    lapse=-(n-1)*z/eta
    B=(n-1)*((n-1)/eta-(n-2))
    ck('lapse equation',s.simplify(s.diff(spatial,t).subs(t,lapse))==0,'ηneq0')
    ck('reduced scalar gradient',s.simplify(spatial.subs(t,lapse)+B*z**2)==0,'general-n')
    h,cs,Q=s.symbols('h cs Q',positive=True)
    c2=s.symbols('c2',real=True)
    l=1-c2*h*Q
    ck('linear endpoint calibration',s.simplify(l.subs({c2:-s.Rational(1,2),h:s.Rational(1,10),Q:1})-s.Rational(21,20))==0,'λ1.05')
    speed=s.simplify((B/A).subs({n:3,eta:s.Rational(1,10),lam:s.Rational(21,20)}))
    ck('endpoint scalar speed',speed==s.Rational(19,43),str(speed))
    for nn in [2,3,4,5]:
        val=s.simplify(A.subs({n:nn,lam:(1+s.Rational(1,nn))/2}))
        if mutation=='ghost_sign_flip' and nn==3: val=s.Abs(val)
        ck('ghost interval n'+str(nn),val<0,str(val))
    xx=s.symbols('xx',positive=True);hh=s.Function('h')(xx)
    ck('root monotonicity identity',s.simplify(s.diff(s.sqrt(xx)*hh,xx)-(hh+2*xx*s.diff(hh,xx))/(2*s.sqrt(xx)))==0,'Q sign controls√zh')
    return {'all_passed':all(r['passed'] for r in rows),'checks':rows,'mutation':mutation,'non_claims':['Only geodesic homogeneous principal sector','No acceleratedgalaxy completion','No 32pi derivation']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutation',default='none',choices=['none','ghost_sign_flip']);a=p.parse_args();o=run(a.mutation);Path(a.output).write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({'all_passed':o['all_passed'],'checks':len(o['checks'])}));raise SystemExit(0 if o['all_passed'] else 1)
