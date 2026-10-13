"""Stable scalar extension: stability and incompatible Born scattering slopes."""
from pathlib import Path
import json, math
import sympy as s
from scipy.optimize import brentq
from scipy.integrate import quad
P=Path(__file__).parent
n,g,a,b,k=s.symbols('n g a b k',positive=True) # b is mediator mass squared
D=s.sqrt(b*b+4*a*g*n);z=2*g*n/(D+b);chi=-z
E=k*n*n+b*z*z/2+a*z**3/3-g*n*z
checks={}
checks['stationary_scalar']=s.simplify(b*z+a*z*z-g*n)==0
checks['curvature']=s.simplify(b+2*a*z-D)==0
checks['eliminated_compressibility']=s.simplify(s.diff(E,n,2)-(2*k-g*g/D))==0
p=s.simplify(n*s.diff(D,n)/D)
checks['screening_slope']=s.simplify(p-2*a*g*n/(b*b+4*a*g*n))==0
# F(x) and logarithmic derivative. Use safe moderate x in quadrature checks.
def F(x):return math.log1p(x)-x/(1+x)
def q(x):return x*x/((1+x)**2*F(x))
xhalf=brentq(lambda x:q(x)-1,.1,10)
angular=[]
for x in [.01,.1,1.,xhalf,10.,100.]:
 # dimensionless angular transport integral, t=1-cos(theta)
 integ=quad(lambda t:t/(1+x*t/2)**2,0,2,epsabs=1e-12)[0]
 exact=4*F(x)/(x*x)
 checks['angular_integral_'+str(x)]=abs(integ/exact-1)<1e-10
 angular.append(dict(x=x,q=q(x),density_slope_at_high_density=-q(x)/2,velocity_slope=-4+2*q(x)))
# Stable example g=a=b=k=1 => E''=2-1/sqrt(1+4n)>0.
checks['stable_example_positive']=all(2-1/math.sqrt(1+4*v)>0 for v in [1e-9,.001,1,100,1e9])
R=dict(checks={key:bool(v) for key,v in checks.items()},all_pass=all(checks.values()),velocity_minus_two_x=xhalf,angular_checks=angular,symbolic=dict(chi=str(chi),mass_squared=str(D),compressibility='2*k-g*g/sqrt(b*b+4*a*g*n)',stable_all_density_condition='2*k >= g*g/b',density_mass_squared_slope=str(p)),conclusion='For fixed coupling Born Yukawa scattering and 0<p<=1/2, B=-2 implies A=-p>=-1/2, incompatible with A=-1. Valid pointwise for this class only.')
(P/'screening_run'/'results.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2));assert R['all_pass']
