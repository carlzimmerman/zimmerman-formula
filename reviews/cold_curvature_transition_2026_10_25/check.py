import argparse,json,math
from pathlib import Path
import sympy as S
from scipy.optimize import brentq

# Set M=DeltaV=1; v remains independent. All derivatives are then explicit.
x,v,s,r=S.symbols('x v s r', positive=True)
F=1-s*x*x/v**2
U=r+(x*x/v**2-1)**2
W=U/F**2
K=1/F+S.Rational(3,2)*(S.diff(F,x)/F)**2
Wp=S.diff(W,x); Wpp=S.diff(Wp,x)
y=(1-s*(1+r))/(1-s)
Fs=S.factor(F.subs(x*x,v*v*y))
Us=S.factor(U.subs(x*x,v*v*y))
# A nonzero stationary point is independently certified by differentiating W.
assert S.simplify((Wp/x).subs(x*x,v*v*y))==0
mass_derived=S.factor((Wpp/K).subs(x*x,v*v*y))
mass_formula=8*y*(1-s)/(Fs*(v*v*Fs+6*s*s*y))
assert S.simplify(mass_derived-mass_formula)==0
H2=Us/(3*Fs**2)
bound=4*(1-s)**2/(r*s*s)
# Exact bound / actual ratio = 1 + positive canonical term / mixing term.
assert S.simplify(bound/(mass_formula/H2)-(1+v*v*Fs/(6*s*s*y)))==0
alpha2=S.factor((S.diff(-S.log(F)/2,x)**2/K).subs(x*x,v*v*y))
assert S.simplify(alpha2-s*s*y/(v*v*Fs+6*s*s*y))==0
massfun=S.lambdify((r,s,v),mass_derived,'math')
wpfun=S.lambdify((x,r,s,v),Wp,'math')


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--mutate',action='store_true');a=ap.parse_args()
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True);rows=[]
 for rr in [.1,1.,10.]:
  for frac in [.1,.5,.9]:
   ss=frac/(1+rr)
   yy=(1-ss*(1+rr))/(1-ss)
   ff=1-ss*yy;uu=rr+(1-yy)**2;hh=uu/(3*ff**2)
   for vv in [1e-6,.1,1.]:
    root=brentq(lambda t:wpfun(t*vv,rr,ss,vv),math.sqrt(yy)*.9,math.sqrt(yy)*1.1,xtol=1e-14)
    assert abs(root**2-yy)<1e-11
    # FR=4U and scalar stationarity with R=4(1-y)/(s v-independent M²).
    curvature=4*(1-yy)/ss
    assert abs(ff*curvature-4*uu)<1e-11
    m2=8*yy*(1-ss)/(ff*(vv*vv*ff+(0 if a.mutate else 6*ss*ss*yy)))
    independent=massfun(rr,ss,vv)
    assert math.isclose(m2,independent,rel_tol=2e-12),'missing gravity kinetic mixing'
    upper=2*(1-ss)/(ss*math.sqrt(rr))
    assert math.sqrt(m2/hh)<=upper*(1+1e-12)
    aa=ss*ss*yy/(vv*vv*ff+6*ss*ss*yy)
    assert 0<aa<=(1/6)*(1+1e-12)
    rows.append(dict(r=rr,s=ss,v_over_M=vv,y=yy,F_over_M2=ff,mphysical_over_HE=math.sqrt(m2/hh),
                     mass_upper_bound=upper,alpha_squared=aa,Rtrigger_over_Rfalse=1/(ss*(1+rr))))
 eta=1500*3.085677581491367e16*1000; Href=1.8e-18
 mu=299792458.**2/(eta*Href)
 smax=2/(mu+2)
 result=dict(scope='new scalar-tensor transition prerequisite test; not CCT completion',rows=rows,
  matching_reference=dict(eta_pc_kms=1500,H_s_inv=Href,required_mass_frequency_over_H=mu,
      r_assumed=1,s_upper_bound=smax,Rtrigger_over_Rfalse_lower_bound=1/(2*smax)),
  symbolic_checks=['Einstein potential stationary point','canonical mass including metric kinetic term',
                   'exact positive-gap mass bound','baryon conformal coupling'],
  finite_checks=['27 bracketed stationary roots','Jordan endpoint trace','mass bound','positive F','alpha bound'])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'cases':len(rows),'matching_reference':result['matching_reference']},indent=2))
if __name__=='__main__':main()
