"""CE-FM-059: conditional live charged Plummer core and homology obstruction."""
import sys,json
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def exact(n,e):
    assert s.simplify(e)==0,(n,e)
    checks.append(n)
r,f,gamma=s.symbols('r f gamma',positive=True)
rho=3/(4*s.pi)*(1+r*r)**(-s.Rational(5,2))
g0=r/(1+r*r)**s.Rational(3,2)
x=gamma*g0 # G=M0=b=a0=1; q0=gamma
S=1+f-gamma**2/(1-x)
cs=(1+f-gamma**2/(1-x))/(5*s.sqrt(1+r*r))
exact('charged Euler pressure and barotropic sound',cs*s.diff(rho,r)+rho*g0*S)
exact('neutral Euler normalization',s.diff(f*(1+f)*rho/(6*s.sqrt(1+r*r)),r)+f*rho*(1+f)*g0)
exact('mass preserving homology density integral boundary',s.limit(r**3*rho,r,s.oo))
z,lam=s.symbols('z lambda',positive=True);e=s.Function('e');HH=s.Function('H')
U=lam**-3*e(lam**3*z)
exact('fluid dilation second derivative',s.diff(U,lam,2).subs(lam,1)-(9*z*z*s.diff(e(z),z,2)-12*z*s.diff(e(z),z)+12*e(z)))
F=lam**-3*HH(lam**2*z)
exact('gauge dilation second derivative',s.diff(F,lam,2).subs(lam,1)-(12*HH(z)-10*z*s.diff(HH(z),z)+4*z*z*s.diff(HH(z),z,2)))
h=-z-s.log(1-z)
Fz=12*h-10*z*z/(1-z)+4*z*z/(1-z)**2
exact('gauge homology numerator',12*h-10*z*s.diff(h,z)+4*z*z*s.diff(h,z,2)-Fz)
n=s.symbols('n',integer=True,positive=True)
coef=4*n-14+12/n
exact('series coefficient bound difference',4*(n-2)-coef-(6-12/n))
exact('leading cubic coefficient',coef.subs(n,3)-2)
# w=3r^2/(1+r^2)^3, t=r^2/(1+r^2), W=w(9/5-4t).
def moment(j):return s.Rational(3,2)*s.gamma(s.Rational(3,2)+j)*s.gamma(s.Rational(3,2))/s.gamma(3+j)
I0=moment(0);I1=moment(1);I2=moment(2)
exact('weight normalization',I0-3*s.pi/16)
exact('signed fluid weight',s.Rational(9,5)*I0-4*I1+3*s.pi/80)
exact('Cauchy absolute weight bound squared',s.Rational(81,25)*I0-s.Rational(72,5)*I1+16*I2-I0*s.Rational(26,25))
# Analytic rational upper bound: pi>3, pi<22/7, sqrt26<51/10.
ff=s.Rational(1,1000);gg=s.Rational(1,2)
upper=-(1+ff-gg**2)*s.Rational(9,80)+(gg**2/4)*(3*s.Rational(22,7)/16)*(s.Rational(51,10)/5)+s.Rational(17,4)*gg**3*s.Rational(8,105)
assert upper<0;checks.append('rigorous total homology upper bound negative')
assert 1+ff-gg**2/s.Rational(4,5)>0;checks.append('charged pressure and sound positive')
assert 2*gg/(3*s.sqrt(3))<s.Rational(1,5);checks.append('source field everywhere below1/5')
mp.mp.dps=45
fm=mp.mpf('.001');gm=mp.mpf('.5');xm=lambda t:gm*t/(1+t*t)**mp.mpf('1.5')
W=lambda t:3*t*t/(1+t*t)**4*(mp.mpf(9)/5-mp.mpf(11)/5*t*t)
Sm=lambda t:1+fm-gm*gm/(1-xm(t))
source=mp.quad(lambda t:W(t)*Sm(t),[0,1,3,mp.inf])
neutral=-3*mp.pi/80*fm*(1+fm)
def gauge_series(y):
    return mp.fsum([(4*j-14+mp.mpf(12)/j)*y**j for j in range(3,80)])
gauge=mp.quad(lambda t:t*t*gauge_series(xm(t)),[0,1,3,mp.inf])
assert source+neutral+gauge<0;checks.append('high precision energy comparison')
res={'claim_id':'CE-FM-059','checks_passed':len(checks),'checks':checks,'parameters':{'f':'.001','M_Q_over_M0':'.5','q0':'.5','G=M0=b=a0':1},'rigorous_upper_bound_ignoring_negative_neutral_term':str(upper),'upper_bound_decimal':str(s.N(upper,20)),'numerical_source_fluid_second_variation':str(source),'numerical_neutral_fluid_second_variation':str(neutral),'numerical_gauge_second_variation':str(gauge),'numerical_total_second_variation':str(source+neutral+gauge),'scope':'One explicitly pressure-reconstructed moving charged-source extension in Newtonian rest-mass gravity. Negative mass/charge-preserving homology energy, not a universal no-go or full spectral/Einstein theorem.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
