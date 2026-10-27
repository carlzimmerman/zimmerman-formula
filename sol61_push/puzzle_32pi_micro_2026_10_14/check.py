import sympy as s
import scipy.optimize as opt
import math,json
x,j,m,y,z=s.symbols('x j m y z',positive=True)
h=s.symbols('h',real=True)
checks=[]
def ck(name,expr):
 assert s.simplify(expr)==0,(name,expr)
 checks.append(name)
Z=s.integrate(s.exp(-(1+j)*y),(y,0,s.oo))
ck('positive_partition',Z-1/(1+j))
mean=s.integrate(y*s.exp(-(1+j)*y),(y,0,s.oo))/Z
ck('constitutive_polarization',1-mean-j/(1+j))
K=-s.log(1-h); hs=1-1/m
I=s.simplify(hs*m-K.subs(h,hs))
ck('rate_function',I-(m-1-s.log(m)))
# Log substitution on x<1 performed explicitly; algebra retains log(1-x).
phi=-x-s.log(1-x)
ck('rate_potential',(m-1-s.log(m)).subs(m,1-x)-phi)
ck('legendre_stationary',s.diff(K,h).subs(h,hs)-m)
ck('force',s.diff(phi,x)-x/(1-x))
ck('curvature',s.diff(phi,x,2)-1/(1-x)**2)
ck('rate_minimum',phi.subs(x,0))
ck('shape_quartic',s.diff(phi,x,4)*s.diff(phi,x,2)/s.diff(phi,x,3)**2-s.Rational(3,2))
a,u,G,C=s.symbols('a u G C',positive=True)
W=a*a/G*(C-u/a-s.log(1-u/a))
ck('scale_Ward_all_C',a*s.diff(W,a)+u*s.diff(W,u)-2*W)
# Quantum oscillator spectrum E_k=hw(k+1/2), z=hw/T.
q=s.symbols('q',positive=True)
Zq=s.exp(-z/2)/(1-s.exp(-z))
meanE=-s.diff(s.log(Zq),z)
ck('oscillator_energy',meanE-(s.Rational(1,2)+1/(s.exp(z)-1)))
# Source rescales the oscillator Hamiltonian. Susceptibility normalized to its baseline mean.
# Rewrite exponentials to avoid nonuniform hyperbolic simplifier conventions.
baseline=(1+s.exp(-z))/(2*(1-s.exp(-z)))
ms=(1+s.exp(-(1+j)*z))/(2*(1-s.exp(-(1+j)*z)))/baseline
chi=s.simplify(-s.diff(ms,j).subs(j,0))
ck('quantum_susceptibility',chi-2*z*s.exp(z)/(s.exp(2*z)-1))
ck('classical_susceptibility',s.limit(chi,z,0,dir='+')-1)
ck('zeroT_susceptibility',s.limit(chi,z,s.oo))
# Number cumulants from the geometric distribution, checked by q derivatives.
logZ=-s.log(1-q)
cumulants=[]; cur=logZ
for k in range(1,5):
 cur=s.factor(q*s.diff(cur,q)); cumulants.append(cur)
v=q/(1-q)**2
ck('number_variance',cumulants[1]-v)
ck('number_third',cumulants[2]**2-v*v*(1+4*v))
ck('number_fourth',cumulants[3]-v*(1+6*v))
R=3-cumulants[3]*cumulants[1]/cumulants[2]**2
ck('quantum_rate_shape',R-(2+6*v)/(1+4*v))
ck('shape_gap',R-s.Rational(3,2)-1/(2*(1+4*v)))
# Candidate thermal ENERGY invariant, conditional: no bare offset or interactions.
def ratio(z):
 b=1/math.expm1(z); v=b*(1+b)
 return z*(b+.5)*(1+4*v)/v
root=opt.brentq(lambda z:ratio(z)-64*math.pi,1.,8.,xtol=1e-13)
b=1/math.expm1(root); vv=b*(1+b)
print(json.dumps({'exact_checks':checks,'count':len(checks),'conditional_matching_state':{'z':root,'invariant':ratio(root),'target':64*math.pi,'normalized_response':root/math.sinh(root),'quartic_shape':(2+6*vv)/(1+4*vv),'required_logarithmic_shape':1.5},'interpretation':'State fit only, not derived temperature. Thermal oscillator is not established as vacuum stress; no solved coefficient.'},indent=2))
