import sympy as s
import json
C,a,K,u,G,r,L=s.symbols('C a K u G r L',positive=True)
d=s.symbols('d',real=True)
W=lambda C:a*a/K*(C-u/a-s.log(1-u/a))
checks=[]
def ck(name,expr):
 assert s.simplify(expr)==0,(name,expr)
 checks.append(name)
ck('vacuum_shift',W(C+d)-W(C)-d*a*a/K)
for j in range(1,5): ck('response_shift_order_'+str(j),s.diff(W(C+d)-W(C),u,j))
ck('convex_curvature',s.diff(W(C),u,2)-a*a/(K*(a-u)**2))
g=K*s.diff(W(C),u); gn=g-u
ck('local_mond_response',gn-g*g/(a+g))
ck('area_product',s.pi/a**2*(2*C*a**2)-2*s.pi*C)
ck('countermodel_target',2*s.pi*(16*s.pi)-32*s.pi**2)
ck('countermodel_alternative',2*s.pi*(8*s.pi)-16*s.pi**2)
ck('S4_all_scales',s.Rational(8,3)*L**2*(24*s.pi**2/L**2)-64*s.pi**2)
eta=s.diag(-1,1,1,1)
rho,p,rhov=s.symbols('rho p rhov',real=True)
T=s.diag(rho,p,p,p); dust=s.diag(rho,0,0,0); vac=-rhov*eta
def trace(T): return s.trace(eta*T)
def contraction(T,U): return s.trace(eta*T*eta*U)-trace(T)*trace(U)/2
ck('dust_dust',contraction(dust,dust)-rho**2/2)
ck('dust_vacuum',contraction(dust,vac)+rho*rhov)
ck('trace_reversal',T[0,0]+trace(T)/2-(rho+3*p)/2)
# Both h00=-2Phi and the 16pi field-equation prefactor must be retained.
ck('Newton_calibration',8*s.pi*G*(rho+3*p)/2-4*s.pi*G*(rho+3*p))
Phi=-L*r*r/6
ck('vacuum_Poisson',(s.diff(r*r*s.diff(Phi,r),r)/r**2)+L)
ck('vacuum_acceleration',-s.diff(Phi,r)-L*r/3)
# General ball averaging profile, directly integrate the published p=2 case.
R=s.symbols('R',positive=True)
avg=s.integrate((a*a/G)*(R/r)**2*4*s.pi*r*r,(r,0,R))/(4*s.pi*R**3/3)
ck('published_average',avg-3*a*a/G)
ck('average_gives_24pi',8*s.pi*G*avg/a**2-24*s.pi)
assert s.simplify(24*s.pi-32*s.pi)!=0
print(json.dumps({'exact_checks':checks,'count':len(checks),'countermodels':{'C=16pi':'A Lambda=32pi²','C=8pi':'A Lambda=16pi²','common':'same a,K and all local u derivatives; same S4 Euler integral; same spin2 projector'},'scope':'Reduced-response countermodels, not complete cosmological models. Published-preprint averaging is checked, not adopted.'},indent=2))
