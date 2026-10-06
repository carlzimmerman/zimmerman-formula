"""Raw ADM mean sources and actual prepared multishell common rows."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['single_shell_shift','wrong_profile','erase_zero_mode']);ar=ap.parse_args();rows=[]
def eq(n,x):
 x=s.factor(x);rows.append(dict(name=n,passed=x==0,residual=str(x)))
eta,K,a,H,k,r=s.symbols('eta K a H k r',positive=True);u,ux,uxx,uxxx,W,Z,V,Zt,Zx,Zxx,S,Sx=s.symbols('u ux uxx uxxx W Z V Zt Zx Zxx S Sx',real=True);ep=s.symbols('ep');L=0
for sign in (1,-1):
 X=2*Z+sign*u;Y=2*Z-sign*u;N=s.exp(V+sign*u/2)
 Xx=2*Zx+sign*ux;Yx=2*Zx-sign*ux;Yxx=2*Zxx-sign*uxx
 shift=S+sign*H*W;shiftx=Sx-sign*H*u
 kx=(H+Zt-sign*H*u/2-shift*Xx/2-shiftx)/N
 ky=(H+Zt+sign*H*u/2-shift*Yx/2)/N
 Ric=s.exp(-X)/a**2*(-2*Yxx+Xx*Yx-s.Rational(3,2)*Yx*Yx)
 L+=K*a**3*N*s.exp((X+2*Y)/2)*((1-eta)*(kx*kx+2*ky*ky)-(1-eta/3)*(kx+2*ky)**2+Ric)
L+=-12*K*H**2*a**3*s.exp(V+3*Z)+K*a*s.exp(V+Z)*s.cosh(u)*ux*ux
sub={Z:0,V:0,Zt:0,Zx:0,Zxx:0,S:0,Sx:0}
def coeff(expr):return s.expand(s.series(expr.subs(sub).subs({u:ep*u,ux:ep*ux,uxx:ep*uxx,W:ep*W}),ep,0,3).removeO()).coeff(ep,2)
def dx(expr):return s.diff(expr,u)*ux+s.diff(expr,ux)*uxx+s.diff(expr,uxx)*uxxx-s.diff(expr,W)*u
def dtseed(expr):return s.diff(expr,a)*H*a-H*sum(j*s.diff(expr,j) for j in [u,ux,uxx,W])
JV=coeff(s.diff(L,V));JS=coeff(s.diff(L,S))-dx(coeff(s.diff(L,Sx)))
JZ=coeff(s.diff(L,Z))-dtseed(coeff(s.diff(L,Zt)))-dx(coeff(s.diff(L,Zx)))+dx(dx(coeff(s.diff(L,Zxx))))
jv=-K*a*(3*H**2*a*a*u*u-4*H**2*a*a*W*ux+4*u*uxx+4*ux*ux)
js=-s.Rational(2,3)*H*K*a**3*((4*eta-9)*u*ux+(6-4*eta)*W*uxx)
jz=-H**2*K*a**3*(3*u*u-4*W*ux)
eq('raw_multishell_lapse_source',JV-jv);eq('raw_multishell_shift_source',JS-js);eq('raw_multishell_curvature_source',JZ-jz)
jt=H*K*a**3*(u*u+(8*eta-12)*W*ux/3)
eq('actual_shift_primitive',dx(jt)-JS)
clock=dtseed(JV)-H*JZ-dx(JS)/a**2
expectedclock=s.Rational(2,3)*H*K*a*((6-4*eta)*W*uxxx+(8*eta-9)*u*uxx+(4*eta-3)*ux*ux)
eq('multishell_temporal_clock_identity',clock-expectedclock)
# Independently compute exact Laurent coefficients of squared prepared profiles.
f={1:s.Rational(1,2),-1:s.Rational(1,2),3:-s.Rational(1,18),-3:-s.Rational(1,18)}
g={j:b/(j*j) for j,b in f.items()}
def grad(d):return {j:s.I*j*b for j,b in d.items()}
def mul(x,y):
 d={}
 for i,b in x.items():
  for j,c0 in y.items():d[i+j]=d.get(i+j,0)+b*c0
 return {j:s.expand(b) for j,b in d.items()}
af=mul(f,f);bf=mul(grad(g),grad(f));tables={0:(s.Rational(41,81),s.Rational(41,81)),2:(s.Rational(7,18),-s.Rational(37,54)),4:(-s.Rational(1,9),s.Rational(5,27)),6:(s.Rational(1,162),-s.Rational(1,162))}
for j,(aa,bb) in tables.items():
 factor=1 if j==0 else 2
 eq('profile_square_'+str(j),factor*af.get(j,0)-aa)
 eq('inverse_shift_product_'+str(j),factor*bf.get(j,0)-bb)
eq('profile_has_zero_mean',f.get(0,0));eq('zero_Parseval_constraint',af[0]-bf[0])
# Generic nonzero common scalar harmonic, source-aware elimination.
c,p,AA,BB=s.symbols('c p AA BB',positive=True);zd,zdd,t=s.symbols('zd zdd t');F=zd-H*V
Jv=c*r*(H*H*(-3*AA+4*BB)+2*p*AA);Jz=c*H*H*r*(-3*AA+4*BB);Jt=H*c*r*(AA+(8*eta-12)*BB/3)
Lm=2*c*(-6*F*F-4*F*t-s.Rational(2,3)*eta*t*t+2*p*Z*Z+4*p*V*Z)+Jt*t+Jv*V+Jz*Z
st=s.solve(s.diff(Lm,t),t)[0];sv=s.solve(s.diff(Lm.subs(t,st),V),V)[0];lr=Lm.subs(t,st).subs(V,sv)
def dt(expr):return 3*H*c*s.diff(expr,c)-2*H*p*s.diff(expr,p)-2*H*r*s.diff(expr,r)+zd*s.diff(expr,Z)+zdd*s.diff(expr,zd)
zsol=-AA*r/4+3*(1-eta)*H*H*r*(AA+4*BB)/(8*eta*p);vsol=AA*r/4;tsol=-H*r*(3*AA+(12-8*eta)*BB)/(8*eta)
subsol={Z:zsol,zd:dt(zsol),zdd:dt(dt(zsol)),V:vsol,t:tsol}
eq('generic_full_mean_shift',s.diff(Lm,t).subs(subsol))
eq('generic_full_mean_lapse',s.diff(Lm,V).subs(subsol))
def dtall(expr):return dt(expr)+s.diff(expr,V)*dt(vsol)+s.diff(expr,t)*dt(tsol)
eq('generic_full_mean_curvature',(s.diff(Lm,Z)-dtall(s.diff(Lm,zd))).subs(subsol))
for j,(aa,bb) in tables.items():
 if j: eq('actual_profile_mean_solution_'+str(j),(s.diff(lr,Z)-dt(s.diff(lr,zd))).subs({Z:zsol,zd:dt(zsol),zdd:dt(dt(zsol))}).subs({AA:aa,BB:bb,p:j*j/a**2}))
# Independently raw homogeneous tracefree Q Euler, general spatial jets.
Q,Qd=s.symbols('Q Qd');Lq=0
for sg in (1,-1):
 X=s.Rational(2,3)*Q+sg*u;Y=-Q/3-sg*u;N=s.exp(sg*u/2);sh=sg*H*W;shx=-sg*H*u
 kx=(H+Qd/3-sg*H*u/2-sh*sg*ux/2-shx)/N;ky=(H-Qd/6+sg*H*u/2+sh*sg*ux/2)/N
 Ric=s.exp(-X)/a**2*(2*sg*uxx-s.Rational(5,2)*ux*ux)
 Lq+=K*a**3*N*s.exp((X+2*Y)/2)*((1-eta)*(kx*kx+2*ky*ky)-(1-eta/3)*(kx+2*ky)**2+Ric)
Lq+=K*a*s.exp(-2*Q/3)*s.cosh(u)*ux*ux-12*K*H*H*a**3
JQ=coeff(s.diff(Lq,Q).subs({Q:0,Qd:0}))-dtseed(coeff(s.diff(Lq,Qd).subs({Q:0,Qd:0})))
eq('generic_raw_homogeneous_tracefree_source',JQ-s.Rational(4,3)*K*a*(H*H*a*a*(1-eta)*W*ux+2*u*uxx+2*ux*ux))
A0=tables[0][0];f0=-H*r*A0/24
eq('actual_zero_trace_lapse',24*c*H*f0+c*H*H*r*A0)
eq('actual_zero_trace_curvature',24*c*(-2*H*r*s.diff(f0,r)+3*H*f0)+c*H*H*r*A0)
eq('actual_zero_anisotropy',(-4*H*H*r*A0)+3*H*(2*H*r*A0)-2*H*H*r*A0)
# Controls explicitly falsify source/seed/genuine zero-mode requirements.
candidate=JS if ar.control!='single_shell_shift' else JS.subs(W,ux)
eq('control_keeps_actual_inverse_shift',candidate-js)
candidate=2*af[4] if ar.control!='wrong_profile' else 0
eq('control_keeps_two_shell_cross_harmonic',candidate-tables[4][0])
candidate=f0 if ar.control!='erase_zero_mode' else 0
eq('control_keeps_sourced_zero_mode',24*c*H*candidate+c*H*H*r*A0)
out=dict(passed=sum(x['passed'] for x in rows),total=len(rows),checks=rows,control=ar.control,scope='actual f3 prepared common secondorder metric rows; combines separately audited SAMEseed relativeC4block only at formalone-sided secondorder; no nonlinear existence, abundance or selector')
pth=Path(ar.out);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[x['name'] for x in rows if not x['passed']])));sys.exit(not all(x['passed'] for x in rows))
