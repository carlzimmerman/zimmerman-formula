import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
import json
x,e,U,Ux=s.symbols('x e U Ux',positive=True)
fx=1/(4*x**3); h2=U/3
up,hp=s.symbols('up hp')
sol=s.solve([e*up-24*fx*h2*hp+Ux-24*fx*h2**2,8*fx*h2*up+2*hp],[up,hp])
ct=s.factor(1+8*fx*sol[up]); w=(s.Rational(2,3)*U**2)/(e*x**6+s.Rational(2,3)*U**2)
q=3*x**3*Ux/U**2
we=-1-2*sol[hp]/(3*h2)
cs=(e-32*(2+ct+6*we)*h2**2*fx**2)/(e+96*h2**2*fx**2)
checks=[]
def ck(name,z):
 assert s.simplify(z)==0,(name,z)
 checks.append(name)
ck('tensor_at_rest',ct-(1+w*(2-q)))
ck('scalar_at_rest',cs-(1-w**2*(2-q)))
n=s.symbols('n',positive=True); t=s.symbols('t',real=True)
v=1-t**2/(16*n); vprime=-t*(1-t**2)/(2*x)
ck('shape_q',2*v-x*vprime-(2-t**2/(8*n)+t*(1-t**2)/2))
tx=s.tanh(4*n*s.log(x)); V=3*x**2/(1-tx**2/(16*n))
ck('vacuum_value',V.subs(x,1)-3)
ck('vacuum_slope',s.diff(V,x).subs(x,1)-6)
ck('vacuum_mass',s.diff(V,x,2).subs(x,1)-6-6*n)
C,M,b=s.symbols('C M b',positive=True)
ck('C_cancellation',(-3*M**2/(16*C*(b*x)**2))*(2*C*b**2/3)/M**2+1/(8*x**2))
ck('extra_stationary_factor',2-t**2/(8*n)+t*(1-t**2)/2-2-t*(4*n*(1-t**2)-t)/(8*n))

def trial(n,x0,eps=1e-6,rtol=1e-9,step=.025):
 def pot(x):
  t=np.tanh(4*n*np.log(x)); v=1-t*t/(16*n)
  vp=-t*(1-t*t)/(2*x)
  return 3*x*x/v,6*x/v-3*x*x*vp/v**2
 def rhs(t,y):
  x,u,h=y; fx=1/(4*x**3); fxx=-3/(4*x**4)
  U,Ux=pot(x)
  mat=np.array([[eps,-24*fx*h*h],[8*fx*h*h,2+16*h*fx*u]])
  vec=np.array([-3*eps*h*u-Ux+24*fx*h**4,-eps*u*u+8*h**3*fx*u-8*h*h*fxx*u*u])
  up,hp=np.linalg.solve(mat,vec)
  return np.array([u,up,hp])
 def stop(t,y): return min(y[0]-.05,3-y[0],y[2]-.01,5-y[2])
 stop.terminal=True
 sol=solve_ivp(rhs,[0,100],[x0,0,np.sqrt(pot(x0)[0]/3)],rtol=rtol,atol=rtol*.01,max_step=step,events=stop)
 x,u,h=sol.y
 fx=1/(4*x**3); fxx=-3/(4*x**4)
 deriv=np.array([rhs(t,y) for t,y in zip(sol.t,sol.y.T)])
 up=deriv[:,1]; hp=deriv[:,2]
 qt=1+8*h*fx*u; ft=1+8*(fx*up+fxx*u*u); ct=ft/qt
 ks=eps*qt+96*h**4*fx**2; we=-1-2*hp/(3*h*h)
 cs=(eps*qt-32*(2+ct+6*we)*h**4*fx**2)/ks
 Us=np.array([pot(z)[0] for z in x]); residual=3*h*h-(eps*u*u/2+Us-24*h**3*fx*u)
 out={'n':n,'eps':eps,'x0':x0,'success':bool(sol.success),'end_time':float(sol.t[-1]),'final_x':float(x[-1]),'final_u':float(u[-1]),'final_h':float(h[-1]),'min_QT':float(qt.min()),'min_FT':float(ft.min()),'min_Ks':float(ks.min()),'min_cs2':float(cs.min()),'max_cs2':float(cs.max()),'max_ct_deviation':float(abs(ct-1).max()),'constraint_relative':float(np.max(abs(residual)/(3*h*h))),'samples':len(x)}
 assert out['success'] and out['constraint_relative']<1e-6,out
 return out
rows=[trial(n,x0) for n,x0 in [(10.,.9),(10.,1.01),(10.,1.1),(100.,.99),(100.,1.001),(100.,1.01)]]
ref=trial(10.,.9,rtol=1e-11,step=.0125)
assert abs(ref['final_x']-rows[0]['final_x'])<1e-7
print(json.dumps({'symbolic_checks':checks,'trajectories':rows,'refinement':ref,'scope':'Six fixed trajectories, no full basin proof. Exact at-rest formulas and conditional polynomial bounds separate from finite evolution.'},indent=2))
