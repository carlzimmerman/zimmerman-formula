"""Raw ADM mean sources and actual simultaneous second-harmonic rows."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['omit_shear_source','freeze_auxiliary_source','raw_clock_only']);ar=ap.parse_args();rows=[]
def eq(n,x):
 x=s.factor(x);rows.append(dict(name=n,passed=x==0,residual=str(x)))
eta,K,a,H,k,r=s.symbols('eta K a H k r',positive=True);u,ux,Z,V,Zt,Zx,Zxx,S,Sx=s.symbols('u ux Z V Zt Zx Zxx S Sx',real=True);ep=s.symbols('ep');L=0
for sign in (1,-1):
 X=2*Z+sign*u;Y=2*Z-sign*u;N=s.exp(V+sign*u/2)
 Xx=2*Zx+sign*ux;Yx=2*Zx-sign*ux;Yxx=2*Zxx+sign*k*k*u
 shift=S+sign*H*ux/k**2;shiftx=Sx-sign*H*u
 kx=(H+Zt-sign*H*u/2-shift*Xx/2-shiftx)/N
 ky=(H+Zt+sign*H*u/2-shift*Yx/2)/N
 Ric=s.exp(-X)/a**2*(-2*Yxx+Xx*Yx-s.Rational(3,2)*Yx*Yx)
 L+=K*a**3*N*s.exp((X+2*Y)/2)*((1-eta)*(kx*kx+2*ky*ky)-(1-eta/3)*(kx+2*ky)**2+Ric)
L+=-12*K*H**2*a**3*s.exp(V+3*Z)+K*a*s.exp(V+Z)*s.cosh(u)*ux*ux
sub={Z:0,V:0,Zt:0,Zx:0,Zxx:0,S:0,Sx:0}
def coeff(expr):return s.expand(s.series(expr.subs(sub).subs({u:ep*u,ux:ep*ux}),ep,0,3).removeO()).coeff(ep,2)
def dx(expr):return s.diff(expr,u)*ux-s.diff(expr,ux)*k*k*u
def dtseed(expr):return s.diff(expr,a)*H*a-s.diff(expr,u)*H*u-s.diff(expr,ux)*H*ux
JV=coeff(s.diff(L,V));JS=coeff(s.diff(L,S))-dx(coeff(s.diff(L,Sx)))
JZ=coeff(s.diff(L,Z))-dtseed(coeff(s.diff(L,Zt)))-dx(coeff(s.diff(L,Zx)))+dx(dx(coeff(s.diff(L,Zxx))))
jv=-K*a*(3*H**2*a*a*k*k*u*u-4*H**2*a*a*ux*ux-4*k**4*u*u+4*k*k*ux*ux)/k**2
js=-s.Rational(2,3)*H*K*a**3*(8*eta-15)*u*ux
jz=-H**2*K*a**3*(3*k*k*u*u-4*ux*ux)/k**2
eq('raw_mean_lapse_source',JV-jv);eq('raw_mean_shift_source',JS-js);eq('raw_mean_curvature_source',JZ-jz)
clock=dtseed(JV)-H*JZ-dx(JS)/a**2
eq('actual_temporal_Noether_clock_source',clock-K*a*H*(6-s.Rational(16,3)*eta)*(k*k*u*u-ux*ux))
# Orthogonal covariant shear source: sigma2xx=-2H ux²/(3k²), sigma2yy=H ux²/(3k²).
eq('direct_shear_clock_source',4*eta*K*a*dx(dx(-2*H*ux*ux/(3*k*k)))-(-s.Rational(16,3)*eta*K*a*H*(k*k*u*u-ux*ux)))
# Fourier cos(2kx) coefficient, u=vcos, ux=-kv sin, r=v².
def harm2(expr):return s.expand(expr).subs({u*u:r/2,ux*ux:-k*k*r/2})
def avg(expr):return s.expand(expr).subs({u*u:r/2,ux*ux:k*k*r/2})
c,p=s.symbols('c p',positive=True);zd,zdd,t=s.symbols('zd zdd t');Jt=H*c*r*(15-8*eta)/6;Jv=c*r*(p-s.Rational(7,2)*H*H);Jz=-s.Rational(7,2)*c*H*H*r
eq('harmonic2_lapse_source',harm2(JV).subs(k*k,a*a*p/4)-Jv.subs(c,K*a**3))
eq('harmonic2_curvature_source',harm2(JZ)-Jz.subs(c,K*a**3))
jtfield=H*K*a**3*(15-8*eta)*u*u/3
eq('shift_source_actual_antiderivative',dx(jtfield)-JS)
eq('harmonic2_shift_source',harm2(jtfield)-Jt.subs(c,K*a**3))
F=zd-H*V
Lm=2*c*(-6*F*F-4*F*t-s.Rational(2,3)*eta*t*t+2*p*Z*Z+4*p*V*Z)+Jt*t+Jv*V+Jz*Z
st=s.solve(s.diff(Lm,t),t)[0];Lv=Lm.subs(t,st);sv=s.solve(s.diff(Lv,V),V)[0];lr=s.factor(Lv.subs(V,sv))
def dt(expr):return 3*H*c*s.diff(expr,c)-2*H*p*s.diff(expr,p)-2*H*r*s.diff(expr,r)+zd*s.diff(expr,Z)+zdd*s.diff(expr,zd)
E=s.factor(s.diff(lr,Z)-dt(s.diff(lr,zd)));want=c*p*(9*H*H*(1-eta)*r+16*eta*p*Z+2*eta*p*r)/(6*H*H*(eta-1))
eq('complete_source_aware_mean_Euler',E-want)
zsol=-r/8-9*(1-eta)*H*H*r/(16*eta*p);vsol=r/8;tsol=H*r*(9-8*eta)/(16*eta)
subs2={Z:zsol,zd:dt(zsol),zdd:dt(dt(zsol)),V:vsol,t:tsol}
eq('actual_mean_shift_row_solution',s.diff(Lm,t).subs(subs2))
eq('actual_mean_lapse_row_solution',s.diff(Lm,V).subs(subs2))
# Curvature row before auxiliary elimination: dt must differentiate V,t backgrounds.
def dtall(expr):return dt(expr)+s.diff(expr,V)*dt(vsol)+s.diff(expr,t)*dt(tsol)
EZ=s.diff(Lm,Z)-dtall(s.diff(Lm,zd))
eq('actual_mean_curvature_row_solution',EZ.subs(subs2))
# Independent zero-mode trace sources and conservation, no p^-1 extrapolation.
eq('homogeneous_lapse_source',avg(JV)-K*a**3*H*H*r/2)
eq('homogeneous_curvature_source',avg(JZ)-K*a**3*H*H*r/2)
f0=-H*r/48
eq('homogeneous_trace_lapse_row',24*c*H*f0+c*H*H*r/2)
eq('homogeneous_trace_curvature_row',24*c*(-2*H*r*s.diff(f0,r)+3*H*f0)+c*H*H*r/2)
# Homogeneous tracefree action source derived separately from diagonal Q jet.
Q,Qd=s.symbols('Q Qd');Lq=0
for sign in (1,-1):
 X=s.Rational(2,3)*Q+sign*u;Y=-Q/3-sign*u;N=s.exp(sign*u/2);sh=sign*H*ux/k**2;shx=-sign*H*u
 kx=(H+Qd/3-sign*H*u/2-sh*sign*ux/2-shx)/N;ky=(H-Qd/6+sign*H*u/2+sh*sign*ux/2)/N
 Ric=s.exp(-X)/a**2*(-2*sign*k*k*u-s.Rational(5,2)*ux*ux)
 Lq+=K*a**3*N*s.exp((X+2*Y)/2)*((1-eta)*(kx*kx+2*ky*ky)-(1-eta/3)*(kx+2*ky)**2+Ric)
Lq+=K*a*s.exp(-2*Q/3)*s.cosh(u)*ux*ux-12*K*H*H*a**3
jq=avg(coeff(s.diff(Lq,Q).subs({Q:0,Qd:0})))-dtseed(avg(coeff(s.diff(Lq,Qd).subs({Q:0,Qd:0}))))
# dtseed doesn't differentiate r, after averaging; actual rdot=-2Hr must be added.
jq+=2*H*r*s.diff(avg(coeff(s.diff(Lq,Qd).subs({Q:0,Qd:0}))),r)
eq('raw_homogeneous_tracefree_source',jq-2*K*a**3*(1-eta)*H*H*r/3)
eq('homogeneous_tracefree_particular',(-2*H*H*r)+3*H*(H*r)-H*H*r)
# Declared controls reject specific misuses.
cs=Jt if ar.control!='omit_shear_source' else Jt.subs(eta,0)
eq('control_retains_added_shift_source',cs-Jt)
cv=Jv if ar.control!='freeze_auxiliary_source' else 0
eq('control_retains_actual_lapse_source',cv-Jv)
# Incorrectly using homogeneous-eliminated clock response with RAW source gives wrong Z.
zcandidate=zsol
if ar.control=='raw_clock_only':zcandidate=-H**2*r*(9-8*eta)*(1-eta)/(16*eta*p)
eq('control_raw_clock_is_not_eliminated_source',E.subs({Z:zcandidate,zd:dt(zcandidate),zdd:dt(dt(zcandidate))}))
out=dict(passed=sum(x['passed'] for x in rows),total=len(rows),checks=rows,control=ar.control,scope='n3 finiteplane puredecay,actualquadraticmean ADMsource and allmeanrows,idealvacuum sharedclock; relative normcube and full nonlinear admission NOTproved')
pth=Path(ar.out);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[x['name'] for x in rows if not x['passed']])));sys.exit(not all(x['passed'] for x in rows))
