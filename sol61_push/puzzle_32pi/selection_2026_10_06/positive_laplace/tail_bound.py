import argparse,json
from pathlib import Path
import mpmath as mp
import sympy as s

def run():
    mp.mp.dps=45;checks=[]
    def ck(name,ok,detail):checks.append({'name':name,'passed':bool(ok),'detail':detail})
    h,t,Y=s.symbols('h t Y',positive=True)
    ck('minimum tail triangle area',s.integrate(h-t/2,(t,0,2*h))==h*h,'f prime≥−1/2')
    d0=s.symbols('d0',nonnegative=True)
    ck('uniform ellipticity margin tail area',s.simplify(s.integrate(h-(1-d0)*t/2,(t,0,2*h/(1-d0)))-h*h/(1-d0))==0,'Requiresd0<1')
    a=s.sqrt(1+1/Y)-1;r=s.sqrt(Y*Y+Y)
    P=(Y+s.Rational(1,2))*r/2-Y*Y/2-s.log(2*Y+1+2*r)/8
    ck('P2 primitive derivative',s.simplify(s.diff(P,Y)-Y*a)==0,'Exact derivative')
    def aa(y):return 1/(y*(mp.sqrt(1+1/y)+1))
    def pp(y):
        q=mp.sqrt(y*y+y)
        return (y+mp.mpf('.5'))*q/2-y*y/2-mp.log(2*y+1+2*q)/8
    target=32*mp.pi
    root=mp.findroot(lambda y:pp(y)+(y*aa(y))**2-target,(200,210))
    one=mp.findroot(lambda y:y*y*aa(y)*(mp.mpf('.5')+aa(y))-target,(400,410))
    q=mp.quad(lambda v:v*aa(v),[0,1,root])
    ck('primitive agrees independent quadrature',abs(q-pp(root))<mp.mpf('1e-35'),str(q-pp(root)))
    ck('P2 prefix threshold',abs(root-mp.mpf('202.112560248705598869062256563406160434'))<mp.mpf('1e-35'),str(root))
    ck('prefix and point thresholds distinct',root<one,{'prefix':str(root),'point':str(one)})
    values=[]
    for cut in (100,202,203,300):
        lower=pp(cut)+(cut*aa(cut))**2
        values.append({'Y':cut,'strict_lower_C':str(lower),'excludes_32pi':bool(lower>=target)})
    ck('witness exact P2 through203 excludes target',values[2]['excludes_32pi'] and not values[1]['excludes_32pi'],values)
    # Independent integration of a positive slope-limited near-extremal tail.
    for margin in (mp.mpf('0'),mp.mpf('.2'),mp.mpf('.8')):
        hh=mp.mpf('.4');width=2*hh/(1-margin)
        area=mp.quad(lambda u:hh-(1-margin)*u/2,[0,width])
        ck('tail area margin '+str(margin),abs(area-hh*hh/(1-margin))<mp.mpf('1e-40'),str(area))
    # Endpoint bound algebra.
    E,C=s.symbols('E C',positive=True)
    cap=(s.sqrt(1+16*C/Y**2)-1)/4
    ck('one point response cap',s.simplify(Y*Y*cap*(s.Rational(1,2)+cap)-C)==0,'Root of endpoint inequality')
    return {'all_passed':all(c['passed'] for c in checks),'checks':checks,'P2_prefix_Ystar':str(root),'P2_single_point_Ystar':str(one),'non_claims':['No galaxy or planetary observations fitted','No selection of32pi','ConditionalNR and vacuum convention']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=run();Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'all_passed':r['all_passed'],'checks':len(r['checks']),'P2_prefix_Ystar':r['P2_prefix_Ystar'],'P2_single_point_Ystar':r['P2_single_point_Ystar']}));raise SystemExit(0 if r['all_passed'] else 1)
