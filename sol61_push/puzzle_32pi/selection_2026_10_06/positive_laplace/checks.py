import argparse,json,math
from pathlib import Path
import mpmath as mp
import sympy as s

def run():
    mp.mp.dps=45
    checks=[]
    def ck(name,ok,detail):
        checks.append({'name':name,'passed':bool(ok),'detail':detail})
    y,T,A,Y=s.symbols('y T A Y',positive=True)
    a=s.sqrt(1+1/y)-1
    e=a/(1+y/T)**2
    D=1+2*e+2*y*s.diff(e,y)
    x=y/T;ss=s.sqrt(1+1/y)
    form=1+(ss-2+1/ss)/(1+x)**2-4*x*a/(1+x)**3
    ck('baseline D identity',s.simplify(D-form)==0,'Exact symbolic derivative, not initial heuristic')
    de=A/(1+y/Y)**4
    dd=2*de+2*y*s.diff(de,y)
    ck('deformation D identity',s.simplify(dd-2*A*(1-3*y/Y)/(1+y/Y)**5)==0,'full source derivative')
    moment=s.integrate(y*de,(y,0,s.oo))
    ck('exact deformation vacuum integral',s.simplify(moment-A*Y**2/6)==0,str(moment))
    ck('wrong pole-three normalization rejected',s.simplify(moment-A*Y**2/2)!=0,'quartic pole moment factor is1/6')
    ck('unchanged leading deep and UV coefficients',s.limit(s.sqrt(y)*(e+de),y,0)==1 and s.simplify(s.limit(y**3*(e+de),y,s.oo)-T**2/2)==0,'deep1 and UVT²/2')
    for n in range(5):
        coeff=s.rf(4,n)*A/Y**n
        expected=(-1)**n*coeff/(1+y/Y)**(4+n)
        ck('derivative bound '+str(n),s.simplify(s.diff(de,y,n)-expected)==0,'positive magnitude max at y→0')
    def c1(t):
        return mp.quad(lambda v:t/(mp.sqrt(1+1/(t*v))+1)/(1+v)**2,[0,1,mp.inf])
    def c2(t):
        return mp.quad(lambda z:2*z*t*t/((z+1)*(t*(z*z-1)+1)**2),[1,2,mp.inf])
    tr=mp.findroot(lambda t:c1(t)-32*mp.pi,(200,210))
    ck('independent integral coordinates',abs(c1(tr)-c2(tr))<mp.mpf('1e-35'),str(c1(tr)-c2(tr)))
    ck('fitted root matches benchmark',abs(tr-mp.mpf('202.3676812881133819303795420260172701599'))<mp.mpf('1e-35'),str(tr))
    rows=[]
    for delta,tolerance in ((.01,1e-9),(1.,1e-8),(100.,1e-7)):
        uv=math.sqrt(12*delta/tolerance)
        amp=6*delta/uv**2
        margin=1-2/float(tr)-2*amp
        row={'delta_C':delta,'Y':uv,'A':amp,'global_jet_bounds_N4':[math.prod(range(4,4+n))*amp/uv**n for n in range(5)],'D_global_lower_bound':margin,'tolerance':tolerance}
        rows.append(row)
        ck('uniform small derivative and ellipticity '+str(delta),max(row['global_jet_bounds_N4'])<=tolerance and margin>0,row)
        # Independent dimensionless quadrature, avoiding vastly separated original y.
        val=mp.mpf(amp)*mp.mpf(uv)**2*mp.quad(lambda v:v/(1+v)**4,[0,1,mp.inf])
        ck('numeric shift '+str(delta),abs(float(val)-delta)<1e-12*max(1,delta),str(val))
    ef=s.lambdify((y,T,A,Y),e+de,'math');df=s.lambdify((y,T,A,Y),D+dd,'math')
    minima=[]
    for row in rows:
        vals=[]
        for j in range(241):
            yy=10**(-10+24*j/240)
            ee=ef(yy,float(tr),row['A'],row['Y']);dv=df(yy,float(tr),row['A'],row['Y'])
            vals.append(min(2,2/(1+2*ee),2/dv))
        minima.append(min(vals))
    ck('full NR Hessian corroboration',min(minima)>0,{'241_y_each_three_actions':minima,'nonclaim':'Origin is degenerate, no uniform ellipticity there'})
    return {'all_passed':all(c['passed'] for c in checks),'checks':checks,'T_fitted':str(tr),'C_baseline':str(c1(tr)),'examples':rows,'non_claims':['Not32pi derivation','Not full covariant health','Not physical-time passive susceptibility','No observational likelihood']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);arg=p.parse_args()
    r=run();Path(arg.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'all_passed':r['all_passed'],'checks':len(r['checks']),'T_fitted':r['T_fitted']}));raise SystemExit(0 if r['all_passed'] else 1)
