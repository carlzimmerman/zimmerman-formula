import sympy as s, numpy as np, json
from scipy.integrate import solve_ivp
x,N,w,u,xi,e=s.symbols('x N w u xi e',positive=True)
d=1+(1+6*xi)*x
f2=xi*x/d
h=(1+x)/(x*d)
P=e*(1+(6*xi-3)*x)+x**2*(1+4*xi+(1+6*xi)*x)
c=P/((e+x*x)*d)
# c=1+M*f*U_chi/U; U is proportional to (e+x²)/(1+x)².
logUx=2*x/(e+x*x)-2/(1+x)
checks=[]
def check(name,v):
    assert s.factor(v)==0,name
    checks.append(name)
check('potential feedback factor',c-1-2*xi*x*(1+x)/d*logUx)
xd=-2*(1+x)*w
Nd=1-N-u-N*w*w/(2*f2)
wd=-(1-u)*w/N-h*w*w-u*(c-1)/N
ud=2*u+u*logUx*xd
variables=[x,N,w,u];rhs=[xd,Nd,wd,ud]
def deriv(expr):return sum(s.diff(expr,z)*dz for z,dz in zip(variables,rhs))
a=(1-N-u)/(2*N)+w*w/(4*f2)
y=(a+w)/(1+w)
expected=-((a+w)/N+(u*c/N+h*w*w)*(1-a))/(1+w)**2
check('full coupled derivative agrees with sign reduction',deriv(y)-expected)
par={xi:s.Rational(1,10),e:10}
check('negative feedback example',c.subs(par).subs(x,1)+s.Rational(5,13))
u0=s.Rational(1,10**6);c0=-s.Rational(5,13)
a0=-u0*c0/(1-u0*c0)
N0=(1-u0)/(1+2*a0)
initial={x:1,N:N0,w:0,u:u0}
check('initial flat slope exactly',expected.subs(par).subs(initial))
curvature=s.factor(deriv(expected.subs(par)).subs(par).subs(initial)/y.subs(par).subs(initial))
# At this point y_dot=0 and w=0, so this equals d²log(y)/dlog(R_J)².
f=s.lambdify((x,N,w,u),[z.subs(par) for z in rhs],'numpy')
fy=s.lambdify((x,N,w,u),y.subs(par),'numpy')
fs=s.lambdify((x,N,w,u),(expected/y/(1+w)).subs(par),'numpy')
yinit=np.array([1.,float(N0),0.,float(u0)])
rows=[]
for end in [-np.log(2),np.log(2)]:
    sol=solve_ivp(lambda t,z:np.asarray(f(*z),dtype=float),[0,end],yinit,rtol=1e-10,atol=1e-13,dense_output=True,max_step=.01)
    assert sol.success
    for tt in np.linspace(0,end,5):
        z=sol.sol(tt); yy=float(fy(*z))
        assert z[0]>0 and z[1]>0 and 1+z[2]>0 and 0<yy<1
        # A proportional to (1+x)^(-1/2), normalize R at the initial point.
        RJ=np.exp(tt)*np.sqrt(2/(1+z[0]))
        rows.append({'r_ratio':float(np.exp(tt)),'physical_radius_ratio':float(RJ),'speed_squared_relative_to_initial':yy/float(y.subs(par).subs(initial)),'physical_log_slope':float(fs(*z)),'N':float(z[1])})
print(json.dumps({'symbolic_checks':checks,'initial':{'xi':'1/10','e':10,'x':1,'u':'1/1000000','w':0,'N_exact':str(N0),'speed_squared_exact':str(a0)},'initial_log_speed_squared_curvature_exact':str(curvature),'initial_curvature_approx':float(curvature),'local_ivp_samples':rows,'scope':'Local source-free Einstein-scalar IVP, altered environment; no global source or exterior matching and no stability claim'},indent=2))
