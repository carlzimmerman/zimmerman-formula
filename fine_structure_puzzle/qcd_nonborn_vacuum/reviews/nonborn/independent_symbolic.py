"""Exact audit of the nonsingular full-trace reduction and series."""
from pathlib import Path
import json,sys
import sympy as s

t,y,H,J,I=s.symbols('t y H J I')
h=1-y;v=t*h;w=-t*y;q=-t;D=4*v+q*q
B1=s.Rational(3,2)+1/v-(1+1/v)*H-(2+q/v)*J/2
B2=-(s.Rational(3,2)+(s.Rational(1,2)+1/q+1/w)*q/v)-(w*q/D)*(1/v-q/(2*v))+(2-(v/w)*(1-w)+q*w/D)*H/v+(2+3*q/v+q)*J/2
raw=(-3*B1-B2).subs(J,1-t*I)
hp=H+1
stable=t*(s.Rational(1,2)+y*(2/hp+1/(2*hp*hp))+y*(2*h+t*y/hp)/(hp*hp*(4*h+t))-(2+t/2)*I)
numer=s.together(raw-stable).as_numer_denom()[0]
remainder=s.rem(s.Poly(numer,H),s.Poly(H*H-1-t*y,H)).as_expr()
assert s.factor(remainder)==0

# Derive the source's soft coefficients with a parameter-integral series.
z=s.Symbol('z');f=z-h*z*z
js=1-t*s.integrate(f,(z,0,1))/2+3*t*t*s.integrate(f*f,(z,0,1))/8
hs=1+t*y/2-t*t*y*y/8+t**3*y**3/16
series1=s.simplify(s.series(B1.subs({H:hs,J:js}),t,0,2).removeO())
series2=s.simplify(s.series((q/v*B2).subs({H:hs,J:js}),t,0,2).removeO())
assert s.simplify(series1-t*(1-11*y)/24)==0
assert s.simplify(series2-11*t/24)==0
trace_soft=s.expand(-3*series1+h*series2)
assert s.simplify(trace_soft-t*(4+11*y)/12)==0
angular=s.simplify(trace_soft.coeff(y,0)*s.pi/2+trace_soft.coeff(y,1)*s.pi/8)
assert angular==9*s.pi*t/32

# Exact small-mu expansion of the authenticated real covariant formulas.
mu=s.Symbol('mu',positive=True);rt=s.sqrt(4-mu*mu);th=s.acos(mu/2)
A=-44+788*mu**2-1500*mu**4+899*mu**6-215*mu**8+18*mu**10
B=406-737*mu**2+304*mu**4-36*mu**6+2*(mu**2-4)**2*(9-35*mu**2+18*mu**4)*s.log(mu)
P=4-492*mu**2+942*mu**4-424*mu**6+54*mu**8
R=-127+235*mu**2-54*mu**4+(-72+418*mu**2-316*mu**4+54*mu**6)*s.log(mu)
FS=(-2*A*th+mu*rt*B)/(96*rt**5)
FB=(P*th-mu*rt*R)/(192*rt**3)
fs=s.expand(s.series(FS,mu,0,3).removeO())
fb=s.expand(s.series(FB,mu,0,3).removeO())
fc=s.simplify(fs-2*fb)
assert s.simplify(fc-(3*s.pi/256-5*mu/64+147*s.pi*mu*mu/2048))==0
assert fs.coeff(s.log(mu))==3*mu/16
assert fb.coeff(s.log(mu))==3*mu/32
result={'exact_trace_remainder':str(remainder),'B1_soft':str(series1),'S2_over_C0_soft':str(series2),'trace_soft':str(trace_soft),'angular_trace_soft':str(angular),'FS_series':str(fs),'FB_series':str(fb),'FC_series':str(fc),'meaning':'Exact algebra/series in the source sector, not a full-QCD error estimate'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
