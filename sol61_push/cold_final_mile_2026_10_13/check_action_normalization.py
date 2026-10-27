"""CE-FM-010: completed square and full/residual potentials must not double count."""
import json,sys
from pathlib import Path
import sympy as s

K,a,u,g,n=s.symbols('K a0 u g gN',positive=True)
Wfull=(-a*u-a*a*s.log(1-u/a))/K
Wrem=Wfull-u*u/(2*K)
Lunsq=-g*g/(2*K)+u*g/K-Wfull
Lsq=-(g-u)**2/(2*K)-Wrem
Lliteral=-(g-u)**2/(2*K)-Wfull
checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)

check('canonical actions identical',s.simplify(Lunsq-Lsq)==0,'Wrem=Wfull-u^2/(2K)')
fullprime=s.factor(K*s.diff(Wfull,u));remprime=s.factor(K*s.diff(Wrem,u))
check('full potential derivative',s.simplify(fullprime-a*u/(a-u))==0,str(fullprime))
check('residual potential derivative',s.simplify(remprime-u*u/(a-u))==0,str(remprime))
correctEL=s.factor(K*s.diff(Lsq,u));literalEL=s.factor(K*s.diff(Lliteral,u))
check('canonical P equation',s.simplify(correctEL-(g-fullprime))==0,str(correctEL))
check('literal P equation',s.simplify(literalEL-(g-u-fullprime))==0,str(literalEL))
check('literal EL leaves nonzero residual on desired law',s.simplify(literalEL.subs(g,fullprime)+u)==0,'EL residual=-u')

ucorrect=(s.sqrt(n*n+4*a*n)-n)/2
uliteral=a*n/(a+n)
gcorrect=n+ucorrect;gliteral=n+uliteral
check('correct Poisson constitutive law',s.simplify(n-u*u/(a-u)).subs(n,u*u/(a-u))==0,'gN=R(u)')
check('literal static solution',s.simplify(literalEL.subs({g:n+uliteral,u:uliteral}))==0,str(gliteral))
check('literal deep ratio is two',s.limit(gliteral/n,n,0,dir='+')==2,'nu->2')
check('correct deep amplitude',s.limit(gcorrect/s.sqrt(a*n),n,0,dir='+')==1,'g/sqrt(a0 gN)->1')
rr,GM=s.symbols('r GM',positive=True)
check('literal point-mass flat speed vanishes',s.limit(rr*gliteral.subs(n,GM/rr**2),rr,s.oo)==0,'r*g->0')
check('correct point-mass flat speed',s.limit(rr*gcorrect.subs(n,GM/rr**2),rr,s.oo)==s.sqrt(a*GM),'r*g->sqrt(a0 GM)')

rows=[]
for y in (.0001,.01,.1,1.,10.,100.):
    nc=float(gcorrect.subs({a:1,n:y}))/y
    nl=float(gliteral.subs({a:1,n:y}))/y
    rows.append(dict(y=y,canonical_nu=nc,literal_nu=nl))
result=dict(checks=checks,fullprime=str(fullprime),remprime=str(remprime),canonical_EL=str(correctEL),literal_EL=str(literalEL),
            finite_laws=rows,scope='Exact written-action correspondence audit. No empirical fitting, covariant completion or microscopic derivation.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
