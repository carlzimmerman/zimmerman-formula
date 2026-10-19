#!/usr/bin/env python3
"""Independent angular source-table and n=2,4 endpoint controls; no author imports."""
import json, re, sys
from pathlib import Path
from fractions import Fraction
import mpmath as mp

BASE=Path('fine_structure_puzzle/qcd_hard_vacuum/reviews/hard')
SOURCE=json.loads((BASE/'SOURCE_NODES.json').read_text())
AUTHOR=json.loads(Path('fine_structure_puzzle/qcd_hard_vacuum/hard_proton/run_001/result.json').read_text())
checks=[]
def check(name,x,y,tol='1e-24'):
    error=abs(x-y)
    assert error<mp.mpf(tol), (name,str(error))
    checks.append({'name':name,'absolute_error':str(error),'tolerance':tol})

def value_error(s):
    central,err=re.fullmatch(r'(-?\d+\.\d+)\((\d+)\)',s).groups()
    return mp.mpf(central),mp.mpf(err)*mp.power(10,-len(central.split('.')[1]))

def density_coefficients(t,m):
    z=mp.sqrt(t)/(2*m); tau=z*z
    def angular(E,G):
        F=(E+tau*G)/(1+tau); A=(E*E+tau*G*G)/(1+tau)
        def integrand(theta):
            x=mp.cos(theta)
            T1=2*(tau*G*G/(tau+x*x)-F*F)
            T2=2*A/(tau+x*x)
            return mp.sin(theta)**2*(-3*T1+(1-x*x)*T2)
        return mp.quad(integrand,[0,mp.pi/2,mp.pi])/(32*mp.pi**3*m*m)
    ee=angular(1,0); mm=angular(0,1); em=angular(1,1)-ee-mm
    return ee,em,mm

def weights(ts):
    lo,hi=Fraction('0.56'),Fraction('0.88'); out=[Fraction(0) for _ in ts]
    for i,(a,b) in enumerate(zip(ts,ts[1:])):
        l,r=max(a,lo),min(b,hi)
        if r<=l:continue
        # Integrate affine basis using endpoint trapezoids, independent of author weights.
        out[i]+=(r-l)*((b-l)+(b-r))/(2*(b-a))
        out[i+1]+=(r-l)*((l-a)+(r-a))/(2*(b-a))
    assert sum(out)==hi-lo
    assert sum(x*w for x,w in zip(ts,out))==(hi*hi-lo*lo)/2
    return [mp.mpf(w.numerator)/w.denominator for w in out]

def tables():
    result=[]
    for short,rows in SOURCE['nodes'].items():
        ws=weights([Fraction(r['t']) for r in rows]); full=conn=sf=sc=mp.mpf(0)
        for w,row in zip(ws,rows):
            if not w:continue
            a,b,c=density_coefficients(mp.mpf(row['t']),mp.mpf('0.9389'))
            E,dE=value_error(row['GEp']); G,dG=value_error(row['GMp'])
            Ec,dEc=value_error(row['GEuc']); Ev,dEv=value_error(row['GEuv'])
            Gc,dGc=value_error(row['GMuc']); Gv,dGv=value_error(row['GMuv'])
            C=Ec/6+Ev/2; H=Gc/6+Gv/2
            full+=w*(a*E*E+b*E*G+c*G*G)
            conn+=w*(a*C*C+b*C*H+c*H*H)
            sf+=w*(abs(2*a*E+b*G)*dE+abs(b*E+2*c*G)*dG)
            sc+=w*(abs(2*a*C+b*H)*(dEc/6+dEv/2)+abs(b*C+2*c*H)*(dGc/6+dGv/2))
        expected=next(r['reference'] for r in AUTHOR['table_results'] if r['ensemble'][1]==short)
        for key,actual in [('K_full_light',full),('K_light_connected',conn),('linearized_sigma_ceiling_full',sf),('linearized_sigma_ceiling_difference',sf+sc)]:
            check('angular '+short+' '+key,actual,mp.mpf(expected[key]),'3e-17')
        result.append({'ensemble':short,'full':str(full),'connected':str(conn),'difference':str(full-conn),'sigma_ceiling_full':str(sf),'sigma_ceiling_difference':str(sf+sc)})
    return result

def dirac():
    c=1/(16*mp.pi**2)
    def f(s):return c*mp.quad(lambda x:(4-2*x)*mp.log(1/((1-x)**2+x*s))+(2*x-2),[0,.5,1])
    def fd(n,s):return (-1)**n*mp.factorial(n-1)*c*mp.quad(lambda x:(4-2*x)*x**n/((1-x)**2+x*s)**n,[0,.5,1])
    def B(z):return (mp.sqrt(1+z*z)+2*z)/(mp.sqrt(1+z*z)+z)**2
    def rad_integral(fun):return mp.quad(lambda z:B(z)*fun(4*z*z),[0,1,10,mp.inf])/(2*mp.pi**2)
    check('evanescent integral',mp.quad(lambda x:2*x-2,[0,1]),-1)
    check('massless MSbar finite 4',f(0),4*c)
    out=[]
    for n in [2,4]:
        for s in map(mp.mpf,['0.003','2.7','79']):
            radial=(-1)**n*mp.factorial(n)*rad_integral(lambda t:t/(t+s)**(n+1))
            check('radial derivative n=%s s=%s'%(n,s),radial,fd(n,s))
        for L in map(mp.mpf,['3','17']):
            I=rad_integral(lambda t:(L/(t+L))**n)
            endpoint=f(L)+sum((-L)**k*fd(k,L)/mp.factorial(k) for k in range(1,n))
            check('finite L n=%s L=%s'%(n,L),I+endpoint,f(0))
            out.append({'n':n,'L':str(L),'radial_integrated_curvature':str(I),'endpoint':str(endpoint),'reconstruction':str(I+endpoint)})
        H=sum(mp.mpf(1)/k for k in range(1,n))
        J=c*mp.quad(lambda x:(4-2*x)*(mp.log(x/(1-x)**2)-H),[0,.5,1])
        check('infinite subtracted n='+str(n),mp.mpf('2.5')*c+3*c*H+J,4*c)
    # The evanescent contact is invisible to all positive derivatives.
    check('contact drop shifts f0',f(0)+c,5*c)
    return out

results=[]
for dps in [32,48]:
    mp.mp.dps=dps
    results.append({'dps':dps,'tables':tables(),'dirac':dirac()})
sigma=mp.mpf(5)*mp.mpf('41.9')/18+mp.mpf('3.636')*mp.mpf('1.08')/6+mp.mpf(30)/9+mp.mpf(4)*82/9
ct=mp.mpf('2.5')*sigma/(16*mp.pi**2)
check('quark sigma mass ct',ct,mp.mpf(AUTHOR['quark_finite_matching']['finite_quark_counterterm_at_mu_equal_Lambda_MeV_per_u']),'3e-15')
output={'assertion_tested':'Independent full angular source-table transformation and Dirac endpoint/derivative checks at n=2,4; not a physical QCD calculation','results':results,'sigma_weighted_MeV':str(sigma),'finite_quark_ct_MeV_per_u':str(ct),'checks':checks,'passed_count':len(checks)}
Path(sys.argv[1]).write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'passed_count':len(checks),'source_numeric_cells_verified':SOURCE['numeric_column_comparisons'],'max_error':max(mp.mpf(x['absolute_error']) for x in checks).__str__(),'tables':results[-1]['tables']}))
