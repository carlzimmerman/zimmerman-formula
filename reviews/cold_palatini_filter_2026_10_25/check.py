import argparse,json,math
from pathlib import Path
import sympy as S
x,v,s,r,k=S.symbols('x v s r k',positive=True)
F=1-s*x*x/v**2; U=r+(x*x/v**2-1)**2;W=U/F**2
A=F**(-S.Rational(1,2));Wp=S.diff(W,x);Wpp=S.diff(Wp,x)
y=(1-s*(1+r))/(1-s); ff=1-s*y;uu=r+(1-y)**2;H2=uu/(3*ff**2)
# General positive Einstein kinetic value k, evaluated at the stationary point.
m2=(Wpp/k).subs(x*x,v*v*y)
a2=(S.diff(S.log(A),x)**2/k).subs(x*x,v*v*y)
identity=24*(1-s)**2/(r*s*s)
assert S.simplify(m2/(H2*a2)-identity)==0
# Palatini K=1/F, M=DeltaV=1.
mp=S.factor((Wpp*F).subs(x*x,v*v*y))
ap=S.factor((S.diff(S.log(A),x)**2*F).subs(x*x,v*v*y))
assert S.simplify(mp-8*y*(1-s)/(v*v*ff**2))==0
assert S.simplify(ap-s*s*y/(v*v*ff))==0
mpfun=S.lambdify((r,s,v),mp,'math');apfun=S.lambdify((r,s,v),ap,'math')
crit=4*((1-s)/s-r)
# At phi=0: m_in²=U''(0)+xi R, R=rho+4U(0), xi=s/v².
d=S.symbols('d',positive=True)
min2=S.diff(U,x,2).subs(x,0)+(s/v**2)*(d+4*U.subs(x,0))
assert S.simplify(min2-s*(d-crit)/v**2)==0
massratio=s*ff*(d-crit)/(8*y*(1-s))
assert S.simplify(min2/(ff*mp)-massratio)==0
minfun=S.lambdify((r,s,v,d),min2,'math')

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True);vac=[];inside=[]
 for rr in [.1,1.,10.]:
  for frac in [.1,.5,.9]:
   ss=frac/(1+rr);yy=(1-ss*(1+rr))/(1-ss);f=1-ss*yy;u=rr+(1-yy)**2;h=u/(3*f*f)
   threshold=4*((1-ss)/ss-rr)
   assert threshold>0
   for vv in [1e-6,.1,1.]:
    mass=mpfun(rr,ss,vv);alpha=apfun(rr,ss,vv)
    assert math.isclose(mass/(h*alpha),24*(1-ss)**2/(rr*ss*ss),rel_tol=1e-12)
    vac.append(dict(r=rr,s=ss,v_over_M=vv,mE_over_HE=math.sqrt(mass/h),alpha_squared=alpha,rho_crit_over_DeltaV=threshold))
    for mult in [1.1,2.,10.,100.]:
     density=mult*threshold
     direct=minfun(rr,ss,vv,density)/(mass*(1 if args.mutate else f))
     expected=ss*f*(density-threshold)/(8*yy*(1-ss))
     assert math.isclose(direct,expected,rel_tol=1e-12),'Jordan mass conversion missing'
     inside.append(dict(r=rr,s=ss,v_over_M=vv,density_over_DeltaV=density,m_in_J_squared_over_m_out_J_squared=direct))
 assert len(vac)==27 and len(inside)==108
 rr=1.;ss=.25;yy=2/3;f=5/6;u=10/9;h=u/(3*f*f)
 mu=299792458.**2/(1500*3.085677581491367e16*1000*1.8e-18)
 vv=math.sqrt(8*yy*(1-ss)/(f*f*h))/mu
 alpha=math.sqrt(apfun(rr,ss,vv))
 threshold=8.; equal=threshold+8*yy*(1-ss)/(ss*f)
 result=dict(scope='Palatini candidate and local WKB mass filter; not halo fit',vacuum_cases=vac,interior_cases=inside,
  illustrative_match=dict(r=rr,s=ss,required_m_over_H=mu,v_over_M=vv,alpha=alpha,
    rho_restoration_over_DeltaV=threshold,rho_local_J_mass_equality_over_DeltaV=equal,
    rho_Killing_energy_barrier_flat_E_metric_over_DeltaV=threshold+(equal-threshold)/f,
    vacuum_F_over_M2=f,delta_log_A= -.5*math.log(f)),
  symbolic_checks=['general positive kinetic cancellation','Palatini mass','Palatini matter coupling',
   'density restoration','Jordan physical mass comparison'],finite_checks=['27 vacuum cases','108 interior cases'])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['illustrative_match'],indent=2))
if __name__=='__main__':main()
