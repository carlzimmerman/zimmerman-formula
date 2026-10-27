import json,sys
import sympy as s
q,g,t=s.symbols('q gamma t', positive=True)
z=g*t
remaining=(1+q*z)*s.exp(-z)
hazard=g*(1-q+q*z)/(1+q*z)
checks=[]
def check(name,expression):
    assert s.simplify(expression)==0,name
    checks.append(name)
check('required age-dependent rate',-s.diff(remaining,t)/remaining-hazard)
check('rate derivative',s.diff(hazard,t)-g*g*q*q/(1+q*g*t)**2)
check('initial rate',hazard.subs(t,0)-g*(1-q))
check('late rate',s.limit(hazard,t,s.oo)-g)
check('one-stage exceptional q=0',remaining.subs(q,0)-s.exp(-g*t))
G=s.symbols('Gamma',positive=True)
# Constant rate matching initial and late slopes would need q=0.
check('constant-rate contradiction difference',g-g*(1-q)-g*q)
mu,n=s.symbols('mu n',positive=True)
Q=((4-n)*mu+3-n)/(2*(n+2)*mu+4)
check('q=0 baryon slope',Q.subs(n,(4*mu+3)/(mu+1)))
check('required q=0 slope exceeds three',(4*mu+3)/(mu+1)-3-mu/(mu+1))
json.dump({'claim_id':'CT-002','status':'exact rate identities passed','count':len(checks),'checks':checks,
 'scope':'Local at-rest orbital-clock target cannot be exactly a constant-rate one-stage population decay for mu>0 and 0<=n<=3; spatial transport and stimulated/coherent interactions excluded'},open(sys.argv[1],'w'),indent=2)
