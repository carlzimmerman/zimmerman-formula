import sympy as s
import math,json,sys
m,u,g,lam=s.symbols('m u g lambda',positive=True)
M=2*m*s.sqrt(1+u*u)
Delta=4*m*m*u*u
width=g*g*u/(16*s.pi*m*(1+u*u))
checks=[]
def exact(name,x):
    y=s.simplify(x)
    assert y==0,(name,str(y))
    checks.append({'name':name,'type':'exact','residual':str(y)})
exact('on-shell daughter energy conservation',2*s.sqrt(m*m+(m*u)**2)-M)
exact('source excess energy',M-2*m-2*m*(s.sqrt(1+u*u)-1))
exact('phase space root',s.sqrt(1-4*m*m/M**2)-u/s.sqrt(1+u*u))
exact('width actual action normalization',g*g/(8*s.pi*M)*s.sqrt(1-4*m*m/M**2)-width)
exact('positive-potential coupling bound width',width.subs(g*g,lam*Delta)-lam*m*u**3/(4*s.pi*(1+u*u)))
exact('bounded quartic threshold width vanishes',s.limit(width.subs(g*g,lam*Delta),u,0))
exact('cold bounded quartic asymptotic',s.limit(width.subs(g*g,lam*Delta)/u**3,u,0)-lam*m/(4*s.pi))
exact('source excess quadratic',s.limit((M-2*m)/(2*m*u**2),u,0)-s.Rational(1,2))
exact('free daughter speed',((m*u)/(M/2))**2-u**2/(1+u*u))
hbar=6.582119569e-16 # eV seconds, declared numerical convention
sec_gyr=365.25*86400*1e9
mass=1e6
rows=[]
for uu in (.02,.001,.0001):
    for tau in (1.0,3.0):
        target=hbar/(tau*sec_gyr)
        gg=math.sqrt(16*math.pi*mass*(1+uu*uu)*target/uu)
        lmin=gg*gg/(4*mass*mass*uu*uu)
        reconstructed=gg*gg*uu/(16*math.pi*mass*(1+uu*uu))
        assert abs(reconstructed/target-1)<1e-12 and 0<lmin<1
        row={'u':uu,'tau_Gyr':tau,'g_eV':gg,'lambda_min':lmin,'width_eV':target,'source_excess_rest_fraction':math.sqrt(1+uu*uu)-1}
        rows.append(row)
        checks.append({'name':'clock retuning '+str((uu,tau)),'type':'float64','relative_width_error':reconstructed/target-1})
bench_g=2168.0; bench_u=.02
bench_width=bench_g**2*bench_u/(16*math.pi*mass*(1+bench_u**2))
bench_tau=hbar/bench_width
assert 3e-13<bench_tau<4e-13
checks.append({'name':'approximate recorded benchmark lifetime','type':'float64','tau_seconds':bench_tau,'ratio_to_1_Gyr':sec_gyr/bench_tau})
# Constant microscopic parameters imply position-independent rest-frame width.
r=s.symbols('r',positive=True)
exact('constant parameter width has no radius clock',s.diff(width,r))
json.dump({'claim_id':'CE-FM-041','count':len(checks),'checks':checks,'retuning_controls':rows,'status':'completed','limitations':'Dilute vacuum tree decay formulas from project, no medium corrections or rate derived from gravity; retuning is feasibility not prediction.'},open(sys.argv[1],'w'),indent=2)
