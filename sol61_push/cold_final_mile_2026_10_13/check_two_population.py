"""CE-FM-016: static reciprocal source coupling; no formation model."""
import json, math, sys
from pathlib import Path
import sympy as s

K,a,g,u,b,f=s.symbols('K a g u b f', positive=True)
W=(-a*u-a*a*s.log(1-u/a))/K
L=-g*g/(2*K)+u*g/K-W
checks=[]
def check(name,cond):
    checks.append({'name':name,'passed':bool(cond)})
    if not cond: raise AssertionError(name)
check('polarization EL full tether',s.simplify(K*s.diff(L,u)-(g-a*u/(a-u)))==0)
ustar=a*g/(a+g)
check('constitutive inversion',s.simplify((g-a*u/(a-u)).subs(u,ustar))==0)
check('total external source flux',s.simplify((g-u).subs(u,ustar)-g*g/(a+g))==0)
R=u*u/(a-u)
check('additive baryon-only state residual is free gravity',
      s.simplify((R-b-f).subs(b,R)+f)==0)
# Let total cold enclosed acceleration in a0 units be S, baryonic be B.
B,S,T=s.symbols('B S T',positive=True)
Tstar=(B+S)/(1+B+S)
polynomial=T*T-(B+S-T)*(1-T)
check('fixed supply equation linear after cancellation',s.expand(polynomial-((1+B+S)*T-B-S))==0)
check('unique fixed supply split solves tether balance',s.simplify(polynomial.subs(T,Tstar))==0)
check('free fraction nonnegative iff S squared plus BS minus B nonnegative',
      s.simplify((S-Tstar)*(1+B+S)-(S*S+B*S-B))==0)
check('positive static supply threshold',
      s.simplify((S*S+B*S-B).subs(S,(s.sqrt(B*B+4*B)-B)/2))==0)
check('capacity below one at finite positive source',s.simplify(1-Tstar-1/(1+B+S))==0)
check('free mass increases required tether',s.simplify(s.diff(Tstar,S)-1/(1+B+S)**2)==0)
check('free split grows monotonically at fixed baryons',s.simplify(s.diff(S-Tstar,S)-(1-1/(1+B+S)**2))==0)

def extra(x):
    # Cancellation-safe positive solution z^2/(1-z)=x.
    if x==0: return 0.
    return 2*x/(math.sqrt(x*x+4*x)+x)
rows=[]
for yb in [1e-4,.01,1.,100.,1e4]:
    for ratio in [0.,.1,1.,3.,10.]:
        yf=ratio*yb
        ub=extra(yb); uc=extra(yb+yf)
        additive=yb+yf+ub; coupled=yb+yf+uc
        check('positive root balance y=%g ratio=%g'%(yb,ratio),
              abs(uc*uc/(1-uc)-(yb+yf))<2e-8*max(1.,yb+yf))
        check('total force grows relative additive y=%g ratio=%g'%(yb,ratio),coupled>=additive)
        check('tether bounded y=%g ratio=%g'%(yb,ratio),0<uc<1)
        # Independent inversion from g^2/(g+1)=yb+yf.
        x=yb+yf; orthogonal=(x+math.sqrt(x*x+4*x))/2
        check('independent total-field inversion y=%g ratio=%g'%(yb,ratio),
              abs(coupled-orthogonal)<1e-12*max(1.,coupled))
        rows.append(dict(y_b=yb,free_over_baryon=ratio,u_baryon=ub,u_coupled=uc,
                         total_coupled_over_additive=coupled/additive,
                         extra_tether_fraction=uc/ub-1))
split=[]
for bv in [.001,1.,100.]:
    threshold=extra(bv)
    for factor in [.5,1.,2.,10.]:
        sv=factor*threshold; tv=(bv+sv)/(1+bv+sv); fv=sv-tv
        check('fixed supply feasibility B=%g factor=%g'%(bv,factor),
              (fv>=-1e-12)==(factor>=1.))
        check('fixed supply identity B=%g factor=%g'%(bv,factor),
              abs(tv*tv/(1-tv)-(bv+fv))<1e-10*max(1.,bv))
        split.append(dict(B=bv,S=sv,T=tv,F=fv,feasible=factor>=1.))
out=dict(checks=checks,source_grid=rows,fixed_supply_controls=split,
         scope='Corrected spherical static action; conditional identified-carrier dictionary; supplied free profiles. Not halo formation, observational scoring or full relativistic completion.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_passed':all(c['passed'] for c in checks),
                  'max_grid_total_coupled_over_additive':max(r['total_coupled_over_additive'] for r in rows)},indent=2))
