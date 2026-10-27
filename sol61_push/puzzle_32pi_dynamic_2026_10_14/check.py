import sympy as s
import json
M,a,C,H=s.symbols('M a C H', positive=True)
beta=s.symbols('beta', real=True)
V=2*C*M**2*a**2
f=beta*M**2/a**2
hp=2*C*a**2/3
bp=-s.Rational(3,16)/C
checks={}
def eq(name,x,y):
    assert s.simplify(x-y)==0,(name,s.simplify(x-y))
    checks[name]=str(y)
eq('Einstein_vacuum',V/(3*M**2),hp)
res=s.diff(V,a)-24*s.diff(f,a)*H**4
res=res.subs(H**2,hp)
eq('scalar_vacuum_residual',res,4*C*M**2*a*(1+s.Rational(16,3)*beta*C))
eq('selected_branch',res.subs(beta,bp),0)
eq('Lambda_over_a_squared',(3*hp/a**2).subs(C,-s.Rational(3,16)/beta),-s.Rational(3,8)/beta)
eq('required_beta',(-s.Rational(3,8)/beta).subs(beta,-3/(256*s.pi)),32*s.pi)
# Homogeneous lapse constraint eliminates delta H = A delta a+B delta adot.
fp=s.diff(f,a); fpp=s.diff(f,a,2)
A=s.diff(V,a)/(6*M**2*H); B=-4*fp*H**2/M**2
D=1-24*fp*H**2*B
friction=3*H-96*fp*H**3*B-24*fp*H**2*A
mass=s.diff(V,a,2)-24*fpp*H**4-96*fp*H**3*A
on=lambda z:s.simplify(z.subs(H**2,hp).subs(beta,bp))
eq('homogeneous_kinetic',on(D),1+6*M**2/a**2)
eq('homogeneous_friction',on(friction/H),3*(1+6*M**2/a**2))
eq('homogeneous_mass',on(mass),0)
# Independently vary lapse in the homogeneous action density divided by b^3.
N,h,v=s.symbols('N h v',real=True)
lag=-3*M**2*h**2/N+v**2/(2*N)-N*V-8*fp*v*h**3/N**3
eq('lapse_constraint',s.diff(lag,N).subs(N,1),3*M**2*h**2-v**2/2-V+24*fp*v*h**3)
# Local scale relaxation in corrected polar potential, K held fixed.
u,K,m2=s.symbols('u K m2',positive=True)
W=(-a*u-a*a*s.log(1-u/a))/K
Wa=s.diff(W,a)
eq('polar_scale_source_leading',s.limit(Wa/u**3,u,0),-1/(3*K*a**2))
eq('polar_scale_mixed_derivative',s.diff(Wa,u),-u**2/(K*(a-u)**2))
eq('relaxation_energy_leading',-(-1/(3*K*a**2))**2/(2*m2),-1/(18*K**2*a**4*m2))
# Putative compact axion theta=M^2/a^2, period 2pi and integer Euler charge.
eq('theta_potential',V.subs(a,M/s.sqrt(s.Symbol('theta',positive=True))),2*C*M**4/s.Symbol('theta',positive=True))
eq('target_beta_in_Euler_units',(-3/(256*s.pi))*32*s.pi**2,-3*s.pi/8)
# Curvature scalar selector with arbitrary potential: exact stationary relation.
xi,lam,v2,V0=s.symbols('xi lam v2 V0',positive=True)
F=M**2+xi*a**2; U=V0+lam*(a*a-v2)**2/4
station=F*s.diff(U,a)-2*s.diff(F,a)*U
eq('nonminimal_stationary_equation',station,a*(lam*(a*a-v2)*(M*M+xi*v2)-4*xi*V0))
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Classical homogeneous curvature-scalar candidate and local static response; not full theory or coefficient prediction'},indent=2))
