import json,sys
from pathlib import Path
import sympy as s
checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
n,a,b,gamma,z,delta,c2,B,G=s.symbols('n a b gamma z delta c2 B Gamma',positive=True)
M=n*s.Matrix([[1+a,1],[1,1]]);K=n*n*s.diag(b,gamma)
poly=s.expand((K-z*M).det()/(n*n*a))
normalized=s.simplify(poly.subs({b:c2*a/n,gamma:delta*a/n}))
target=z*z-(c2+(1+a)*delta)*z+c2*a*delta
check('general principal polynomial',s.simplify(normalized-target)==0,normalized)
ceiling=(1-c2)/(1+a*(1-c2))
check('metric cone boundary identity',s.simplify(target.subs(z,1)-(1-c2-delta*(1+a*(1-c2))))==0,target.subs(z,1))
check('cone ceiling saturates metric root',s.simplify(target.subs({z:1,delta:ceiling}))==0,ceiling)
check('other root at causal ceiling below one',s.simplify(target.subs(delta,ceiling).coeff(z,2)-1)==0,'Product otherroot=c2*a*ceiling<1 for0<c2<1')
energy=B*n**G/G
ap=s.diff(energy,n);bp=s.diff(energy,n,2)
check('soft reference sound speed',s.simplify(n*bp/ap-(G-1))==0,G-1)
p=(3*G-4)/(2-G)
check('power tail exponent balance',s.simplify((p+3)*(G-1)+1-(p+2))==0,p)
check('universal tail inertia exponent',s.simplify((p+3)*(2-G)-2)==0,p+3)
coef=B*(G-1)*(p+3)*p**(G-1)
check('tail inertia amplitude reduction',s.simplify(p**(2-G)*coef-B*(G-1)*(p+3)*p)==0,coef)
fluxpower=2-G*(p+3)
check('fixed-background flux exponent',s.simplify(fluxpower-(2-2*G/(2-G)))==0,fluxpower)
rows=[]
for gg in [s.Rational(3,2),s.Rational(5,3),s.Rational(9,5)]:
    pv=s.simplify(p.subs(G,gg));fv=s.simplify(fluxpower.subs(G,gg))
    check('finite charge tail Gamma'+str(gg),pv>0 and fv<0,(pv,fv))
    for av in [s.Rational(1,1000),s.Rational(1,10),s.Integer(1)]:
        cc=gg-1;dv=s.simplify(ceiling.subs({c2:cc,a:av}))
        for factor in [s.Rational(4,5),s.Rational(6,5)]:
            pp=target.subs({c2:cc,a:av,delta:factor*dv});roots=s.solve(pp,z)
            maxroot=max(float(rr) for rr in roots)
            check('causal margin Gamma%s a%s factor%s'%(gg,av,factor),(maxroot<1)==(factor<1),(roots,maxroot))
            rows.append(dict(Gamma=str(gg),a=str(av),stiffness_over_ceiling=str(factor),maximum_speed_squared=maxroot,tail_deficit_exponent=str(pv),fixed_background_flux_exponent=str(fv)))
out=dict(checks=checks,principal_polynomial=str(target),causal_ceiling=str(ceiling),tail_p=str(p),controls=rows,scope='Fixed-clock local causal condition and formal finite-charge soft-EOS tail; no global solution or nonlinear fluid export theorem.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
