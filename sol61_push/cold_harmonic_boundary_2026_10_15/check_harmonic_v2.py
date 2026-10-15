import sys,json
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
x,y,z,M,C,w,kap=s.symbols('x y z M C w kap',real=True)
k=s.symbols('k',positive=True)
checks=[]
def ck(n,e):
 assert s.simplify(e)==0,(n,e)
 checks.append(n)
f=s.exp(k*z)*s.cos(k*x);xx=[x,y,z]
g=s.Matrix([s.diff(f,a) for a in xx]);H=s.hessian(f,xx)
ck('harmonic plane exponential',s.trace(H))
ck('gradient norm',g.dot(g)-k*k*s.exp(2*k*z))
ck('Hessian gradient ratio',s.trace(H*H)-2*k*k*g.dot(g))
F=s.Function('F')(x,y,z);gf=s.Matrix([s.diff(F,a) for a in xx]);hf=s.hessian(F,xx);lap=s.trace(hf)
flux=hf*gf-lap*gf
ck('gradient-shift boundary divergence',sum(s.diff(flux[i],xx[i]) for i in range(3))-s.trace(hf*hf)+lap*lap)
A,B,D,E,G=s.symbols('A B D E G',real=True)
U=s.Matrix([[A,D,E],[D,B,G],[E,G,-A-B]])
ck('tracefree velocity',s.trace(U))
ck('Einstein cross term',(s.trace((U-2*H)**2)-s.trace(U-2*H)**2)/8-(s.trace(4*H*H)-4*s.trace(H)**2)/8-s.trace(U*U)/8+s.trace(U*H)/2)
u=2*w*H/C
J=s.trace(u*u)*(1+kap)/8-s.trace(u*H)/2
ck('core bound remainder',J+s.trace(H*H)*w/(2*C)-s.trace(H*H)*w*((1+kap)*w-C)/(2*C*C))
ck('nonnegative bound decomposition',C-(1+kap)*w-(C*(1-w)+(C-1-kap)*w))
h=s.symbols('h',positive=True)
coeff=2*h-M*M*k*k/(2*C)
ck('negative threshold',coeff+M*M*(k*k-4*C*h/(M*M))/(2*C))
ck('K64 explicit negative coefficient',coeff.subs({h:1,M:1,C:65,k:17})+s.Rational(29,130))
r=s.symbols('r',positive=True)
I=s.pi*s.exp(-2*k)*((2*k*r-1)*s.exp(2*k*r)+(2*k*r+1)*s.exp(-2*k*r))/(4*k)
ck('ball integral',s.integrate(s.pi*k*k*(r*r-z*z)*s.exp(2*k*(z-1)),(z,-r,r))-I)
ck('unit ball integral',I.subs(r,1)-s.pi*((2*k-1)+(2*k+1)*s.exp(-4*k))/(4*k))
low=s.Rational(1633,50)*s.Rational(33,50)/68
ck('capture lower rational',low-s.Rational(53889,170000))
assert low>s.Rational(1,4);checks.append('capture exceeds half of upper total')
lam=s.symbols('lam',real=True)
# New material normal-velocity-gradient regulator, harmonic symmetric-gradient sector.
Jrepair=(1+kap)*s.trace(U*U)/8-s.trace(U*H)/2+lam*s.trace(H*H)/2
sq=(1+kap)*s.trace((U-2*H/(1+kap))**2)/8+(lam-1/(1+kap))*s.trace(H*H)/2
ck('new shear-regulator completed square',Jrepair-sq)
assert 17**2>4*65;checks.append('explicit wavenumber meets strict no-go threshold')
res={'claim_id':'CHB-001','checks_passed':len(checks),'guaranteed_bad_wavenumber':'k^2>4(1+kappa_max)h_max/Mp^2','example':{'kappa_max':64,'h_max':1,'Mp':1,'k':17,'negative_upper_coefficient':'-29/130','capture_inner_radius':'99/100','capture_lower_over_pi':str(low),'upper_total_over_pi':'1/2','I_unit_ball_decimal':float(I.subs({r:1,k:17}).evalf(40))},'repair_family_condition':'lambda >= 1/(1+kappa) on velocity support','scope':'Exact identities and rational bounds; general compact-shift construction and constrained-reduction proof in NO_GO.md. No physical cold carrier or propulsion solution.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(res,indent=2))
