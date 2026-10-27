import sympy as s,numpy as np,json
from scipy.integrate import solve_ivp
phi=s.symbols('phi',real=True)
x,N,w,u=s.symbols('x N w u',positive=True)
# Exact assigned action: M=xi=lambda=1, h=-1, E=13/50.
V=s.Rational(13,50)-phi**2/2+phi**4/4
F=1+phi**2;D=1+7*phi**2;K=D/F**2;U=V/F**2
checks=[]
def check(name,z):
    assert s.factor(z)==0,name
    checks.append(name)
check('potential globally positive decomposition',V-(phi**2-1)**2/4-s.Rational(1,100))
W=s.factor(U+phi*F/D*s.diff(U,phi))
check('negative feedback at positive potential',W.subs(phi,s.sqrt(s.Rational(1,2)))+s.Rational(31,1620))
check('local feedback ratio', (W/U).subs(phi,s.sqrt(s.Rational(1,2)))+s.Rational(155,261))
canonical_curvature=s.factor(s.diff(U,phi,2)/K-s.diff(U,phi)*s.diff(K,phi)/(2*K**2))
check('local scalar curvature positive',canonical_curvature.subs(phi,s.sqrt(s.Rational(1,2)))-s.Rational(568,1215))
check('vacuum scalar curvature positive',canonical_curvature.subs(phi,s.sqrt(s.Rational(51,50)))-s.Rational(10200,41107))
Ux=(s.Rational(13,50)-x/2+x*x/4)/(1+x)**2
Lx=s.diff(Ux,x)/Ux
d=1+7*x;f2=x/d;h=(1+x)/(x*d)
c=s.factor(1+2*x*(1+x)/d*Lx)
xd=-2*(1+x)*w
Nd=1-N-u-N*w*w/(2*f2)
wd=-(1-u)*w/N-h*w*w-u*(c-1)/N
ud=2*u+u*Lx*xd
variables=[x,N,w,u];rhs=[xd,Nd,wd,ud]
def deriv(z):return sum(s.diff(z,v)*dv for v,dv in zip(variables,rhs))
a=(1-N-u)/(2*N)+w*w/(4*f2)
y=(a+w)/(1+w)
yd=-((a+w)/N+(u*c/N+h*w*w)*(1-a))/(1+w)**2
check('coupled ODE agrees with physical orbit derivative',deriv(y)-yd)
u0=s.Rational(1,10**6);c0=-s.Rational(155,261)
a0=-u0*c0/(1-u0*c0);N0=(1-u0)/(1+2*a0)
initial={x:s.Rational(1,2),N:N0,w:0,u:u0}
check('exact stationary circular speed',yd.subs(initial))
curvature=s.factor(deriv(yd).subs(initial)/y.subs(initial))
assert curvature>0
# Generic turning-point identity, no chosen potential derivatives needed:
aa,ww,uu,nn,cc,hh=s.symbols('aa ww uu nn cc hh')
DD=(1-uu)/nn
ad=-DD*aa-uu/nn
wd0=-DD*ww-hh*ww**2-uu*(cc-1)/nn
J=-((aa+ww)/nn+(uu*cc/nn+hh*ww**2)*(1-aa))/(1+ww)**2
dJ=s.diff(J,aa)*ad+s.diff(J,ww)*wd0+s.diff(J,uu)*2*uu+s.diff(J,nn)*(1-nn-uu)
a_flat=-uu*cc/(1-uu*cc);n_flat=(1-uu)/(1+2*a_flat)
check('generic zero-gradient stationary point curvature',
 (dJ/(aa+ww)*(1+ww)).subs(ww,0).subs(aa,a_flat).subs(nn,n_flat)-2/n_flat)

ff=s.lambdify(variables,rhs,'numpy');fy=s.lambdify(variables,y,'numpy');fs=s.lambdify(variables,yd/y/(1+w),'numpy')
z0=np.array([.5,float(N0),0.,float(u0)]);y0=float(a0)
rows=[];max_refinement=0.
for direction in [-1,1]:
    end=direction*np.log(2)
    sols=[]
    for tol,step in [(1e-10,.01),(1e-12,.005)]:
        sol=solve_ivp(lambda t,z:np.asarray(ff(*z),dtype=float),[0,end],z0,rtol=tol,atol=tol*1e-3,dense_output=True,max_step=step)
        assert sol.success;sols.append(sol)
    for tt in np.linspace(0,end,9):
        z=sols[1].sol(tt);zz=sols[0].sol(tt)
        assert z[0]>0 and z[1]>0 and 1+z[2]>0
        yy=float(fy(*z));assert 0<yy<1
        max_refinement=max(max_refinement,abs(float(fy(*zz))-yy)/y0)
        RJ=np.exp(tt)*np.sqrt(1.5/(1+z[0]))
        rows.append({'Einstein_radius_ratio':float(np.exp(tt)),'Jordan_radius_ratio':float(RJ),'speed_squared_ratio':yy/y0,'log_slope':float(fs(*z)),'N':float(z[1]),'phi_squared':float(z[0])})
print(json.dumps({'symbolic_checks':checks,'exact_initial_data':{'x':'1/2','u':'1/1000000','w':0,'N':str(N0),'circular_speed_squared':str(a0)},'log_speed_squared_curvature_exact':str(curvature),'curvature_approximation':float(curvature),'sampled_refinement_difference_normalized_to_initial_speed_squared':max_refinement,'local_IVP_samples':rows,'scope':'Local exact Einstein-scalar initial data plus finite numerical continuation; no source matching, global stability, or coefficient prediction'},indent=2))
