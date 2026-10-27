import json, sys, math
import sympy as s
from scipy.integrate import quad
b,u0,f,c,r=s.symbols('b u0 f c r',positive=True)
a=s.symbols('a0',positive=True)
RR=lambda u:u*u/(a-u)
u=f*u0
g0=b+u0
cold=-g0+u+RR(u)
prec=-g0
mean=c*cold+(1-c)*prec
checks=[]
def exact(name,expr):
    residual=s.factor(expr)
    assert residual==0,(name,str(residual))
    checks.append({'name':name,'type':'exact','residual':str(residual)})
exact('cold includes precursor gravity',cold-(-b-(1-f)*u0+RR(f*u0)))
exact('conversion cannot change total density momentum at equal velocities',c*cold+(1-c)*prec-mean)
# Baryon-only final equilibrium: b=R(u0).
cold_eq=s.factor(cold.subs(b,RR(u0)))
exact('strict negative residual factorization',cold_eq+(1-f)*u0+(1-f)*u0**2*(a*(1+f)-f*u0)/((a-u0)*(a-f*u0)))
exact('total acceleration bound identity',mean.subs(b,RR(u0))-((1-c)*(-RR(u0)-u0)+c*cold_eq))
w=-u-s.log(1-u) # G=a0=1
exact('full field energy slope',s.diff(w,f)/u0-(u/(1-u)))
exact('full field slope is full outward force',u/(1-u)-(u+u*u/(1-u)))
exact('full field energy convex',s.diff(w,f,2)-u0**2/(1-f*u0)**2)
exact('full field zero initial energy',w.subs(f,0))
exact('full field small amplitude coefficient',s.limit(w/f**2,f,0)-u0**2/2)
# Finite regular carrier supply C(r)=S r^3/(r^3+R^3), R=1,S=1/2.
S=0.5
umax=S*2**(2/3)/3
assert 0<umax<1
checks.append({'name':'regular finite profile below wall','type':'numeric','u_max':umax})
def total(x):return S*x**3/(x**3+1)
def fieldenergy(frac):
    def integrand(x):
        if x==0:return 0.0
        z=frac*S*x/(x**3+1)
        if z<1e-4:
            ww=sum(z**n/n for n in range(2,12))
        else:ww=-z-math.log1p(-z)
        return x*x*ww
    return quad(integrand,0,math.inf,epsabs=1e-11,epsrel=1e-10)
def slope(frac):
    return quad(lambda x:(frac*S*x/(x**3+1))/(1-frac*S*x/(x**3+1))*total(x),0,math.inf,epsabs=1e-11)
energies=[]
for frac in (0.1,0.25,0.5,0.75,1.0):
    val,err=fieldenergy(frac)
    h=1e-5
    finite_diff=(fieldenergy(frac+h)[0]-fieldenergy(frac-h)[0])/(2*h)
    deriv,derr=slope(frac)
    assert val>0 and err<1e-8
    assert abs(finite_diff-deriv)<1e-7,(frac,finite_diff,deriv)
    checks.append({'name':'positive finite field energy f='+str(frac),'type':'quadrature','energy':val,'estimated_error':err})
    checks.append({'name':'conversion work independent finite difference f='+str(frac),'type':'quadrature','derivative':deriv,'difference':finite_diff-deriv})
    energies.append(val)
assert all(energies[i]<energies[i+1] for i in range(len(energies)-1))
checks.append({'name':'finite profile field energy monotonic','type':'numeric'})
# rho_C fraction c and enclosed fraction f can differ. Rational controls.
for F,C,X in [(s.Rational(1,2),s.Rational(1,3),s.Rational(1,2)),(s.Rational(1,10),s.Rational(9,10),s.Rational(1,4)),(s.Rational(9,10),s.Rational(1,10),s.Rational(3,4))]:
    cv=cold_eq.subs({f:F,u0:X,a:1})
    mv=mean.subs(b,RR(u0)).subs({f:F,c:C,u0:X,a:1})
    assert cv<0 and mv<0
    checks.append({'name':'partial conversion cold and mixture inward '+str((F,C,X)),'type':'rational','cold':str(cv),'mixture':str(mv)})
json.dump({'claim_id':'CE-FM-040','count':len(checks),'checks':checks,'status':'completed','scope':'Conditional Newtonian reciprocal accounting, full tether field energy, fixed total mass density at rest; no microscopic action or rates derived'},open(sys.argv[1],'w'),indent=2)
