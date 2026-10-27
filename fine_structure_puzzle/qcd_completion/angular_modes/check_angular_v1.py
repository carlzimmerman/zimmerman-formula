#!/usr/bin/env python3
"""Immutable bounded J=1 ghost audit; writes one declared JSON result."""
import argparse,json,platform,sys,time
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s
import mpmath as mp

ap=argparse.ArgumentParser(); ap.add_argument('--result',required=True); args=ap.parse_args()
t0=time.monotonic(); exact=[]
def zero(name, expr):
    vals=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    for q in vals:
        assert s.cancel(q)==0,(name,q)
    exact.append(name)

t=s.symbols('t',positive=True); nx,ny,nz=s.symbols('nx ny nz',real=True)
n=s.Matrix([nx,ny,nz]); ns=[nx,ny,nz]; eyes=s.eye(3)
k=s.Function('k')(t); hh=s.Function('h')(t); u=s.Function('u')(t)
def sphere(q):
    num,den=s.fraction(s.together(q))
    num=s.rem(s.Poly(s.expand(num),nz),s.Poly(nz*nz+nx*nx+ny*ny-1,nz)).as_expr()
    return s.cancel(num/den)
def spatial(v,i):
    return v.diff(t)*n[i]+s.Matrix([sum((s.KroneckerDelta(i,j)-n[i]*n[j])*s.diff(v[a],ns[j])/t for j in range(3)) for a in range(3)])
def cov(v,i):
    return spatial(v,i)+(1-k)/t*(eyes[:,i].cross(n)).cross(v)
R=n*nz; E=(eyes[:,2]-n*nz)/s.sqrt(2); M=n.cross(eyes[:,2])/s.sqrt(2)
B=s.Matrix.hstack(R,E,M)
U=s.Matrix([[(2+2*k*k)/t**2,-2*s.sqrt(2)*k/t**2,0],[-2*s.sqrt(2)*k/t**2,hh*hh+(1+k*k)/t**2,0],[0,0,hh*hh+(1+k*k)/t**2]])
for col in range(3):
    c=u*B[:,col]/t
    acted=-sum((cov(cov(c,i),i) for i in range(3)),s.zeros(3,1))-hh*hh*n.cross(n.cross(c))
    expected=(-u.diff(t,2)*B[:,col]+u*B*U[:,col])/t
    zero('Cartesian_D2_column_'+str(col),s.Matrix([sphere(q) for q in acted-expected]))
print('Cartesian covariant action verified',flush=True)

j=s.symbols('j',integer=True,positive=True); C=j*(j+1)
A=s.Matrix([[C+2,-2*s.sqrt(C)],[-2*s.sqrt(C),C]])
e0=s.Matrix([s.sqrt(j),s.sqrt(j+1)])/s.sqrt(2*j+1)
e2=s.Matrix([-s.sqrt(j+1),s.sqrt(j)])/s.sqrt(2*j+1)
zero('general_origin_eigenvalue_l_Jminus1',s.simplify(A*e0-j*(j-1)*e0))
zero('general_origin_eigenvalue_l_Jplus1',s.simplify(A*e2-(j+1)*(j+2)*e2))

z=s.symbols('z',positive=True)
K=2*t*z/(z*z-1); h=(z*z+1)/(z*z-1)-1/t
sh=(z*z-1)/(2*z); ch=(z*z+1)/(2*z)
def dt(q): return q.diff(t)+q.diff(z)*z
def dm(a): return a.applyfunc(dt)
W=s.Matrix([[h,s.sqrt(2)*K/t],[s.sqrt(2)*K/t,-1/t]])
Uer=s.Matrix([[h*h+(1+K*K)/t**2,-2*s.sqrt(2)*K/t**2],[-2*s.sqrt(2)*K/t**2,2*(1+K*K)/t**2]])
zero('BPS_Kprime',dt(K)+K*h); zero('BPS_hprime',dt(h)-(1-K*K)/t**2)
zero('actual_J1_RE_is_QQdagger',W*W+dm(W)-Uer)
y0=s.Matrix([t*dt(K),t*(h+t*dt(h))/s.sqrt(2)])
zero('real_regular_Qkernel',dm(y0)+W*y0)
J=s.Matrix([[0,-1],[1,0]]); f=sh/t**2
z0=-s.sqrt(3)*f*J*y0
zero('J1_regular_Qdagger_kernel',-dm(z0)+W*z0)
F=t**3/s.Integer(6)+t**3/(2*sh**2)*(1-t*ch/sh)
zero('elementary_integral_derivative',dt(F)-(y0.T*y0)[0])
uM=3*(sh/t-t/sh)
zero('magnetic_regular_solution',-dt(dt(uM))+Uer[0,0]*uM)
zero('Wronskian_source',s.det(s.Matrix.hstack(z0,y0))-s.sqrt(3)*f*(y0.T*y0)[0])
print('BPS matrix and exact integral identities verified',flush=True)

# Frobenius construction from the original second-order matrix, in (E,R) order.
K0=t/s.sinh(t); h0=s.coth(t)-1/t
U0=s.Matrix([[h0*h0+(1+K0*K0)/t**2,-2*s.sqrt(2)*K0/t**2],[-2*s.sqrt(2)*K0/t**2,2*(1+K0*K0)/t**2]])
V=[U0.applyfunc(lambda q:s.expand(s.series(q,t,0,9).removeO()).coeff(t,p)) for p in [-2,0,2,4,6]]
A0=V[0]; basis=s.Matrix([[s.sqrt(s.Rational(2,3)),-1/s.sqrt(3)],[1/s.sqrt(3),s.sqrt(s.Rational(2,3))]])
Vrot=[s.simplify(basis.T*a*basis) for a in V]
zero('origin_diagonal',Vrot[0]-s.diag(0,6))
series_cols=[]
for initial in [1,3]:
    coeff={initial:s.Matrix([1,0]) if initial==1 else s.Matrix([0,1])}
    for p in range(initial+2,12,2):
        rhs=s.zeros(2,1)
        for power,vv in zip([0,2,4,6],Vrot[1:]):
            rhs+=vv*coeff.get(p-2-power,s.zeros(2,1))
        mat=p*(p-1)*s.eye(2)-Vrot[0]
        if mat.det()==0:
            assert p==3 and rhs==s.zeros(2,1)
            coeff[p]=s.zeros(2,1) # harmless regular l2 admixture fixed to zero
        else: coeff[p]=s.simplify(mat.inv()*rhs)
    cc=basis*sum((v*t**p for p,v in coeff.items()),s.zeros(2,1))
    series_cols.append(cc)
Ystart=s.Matrix.hstack(*series_cols)
Ys=s.lambdify(t,Ystart,'numpy'); Yps=s.lambdify(t,Ystart.diff(t),'numpy')
# Separate magnetic Frobenius start from its differential expression.
vM=s.series(U0[0,0],t,0,9).removeO().expand()
mc={2:s.Integer(1)}
for p in range(4,12,2):
    rhs=sum(vM.coeff(t,q)*mc.get(p-2-q,0) for q in [0,2,4,6])
    mc[p]=s.cancel(rhs/(p*(p-1)-2))
mstart=sum(a*t**p for p,a in mc.items()); ms=s.lambdify(t,mstart,'numpy'); mps=s.lambdify(t,mstart.diff(t),'numpy')
print('Independent Frobenius construction verified',flush=True)

mp.mp.dps=70
def formulas(x):
    q=mp.mpf(x); ks=q/mp.sinh(q); hs=mp.coth(q)-1/q
    bre=1+3/mp.sinh(q)**2*(1-q*mp.coth(q))
    dre=5*mp.sinh(q)/(2*q**3)*bre
    dmag=3*(mp.sinh(q)/q-q/mp.sinh(q))/q**2
    return dre,dmag

def ode(x,y):
    kk=x/np.sinh(x); ht=1/np.tanh(x)-1/x
    a=ht*ht+(1+kk*kk)/x**2; b=-2*np.sqrt(2)*kk/x**2; d=2*(1+kk*kk)/x**2
    mat=np.array([[a,b],[b,d]])
    Y=y[:4].reshape(2,2); Yp=y[4:8].reshape(2,2)
    return np.concatenate([Yp.ravel(),(mat@Y).ravel(),[y[9],a*y[8]]])
num=[]
for eps in [1e-3,5e-4]:
    init=np.concatenate([np.asarray(Ys(eps),float).ravel(),np.asarray(Yps(eps),float).ravel(),[float(ms(eps)),float(mps(eps))]])
    out=solve_ivp(ode,(eps,20.),init,t_eval=[2.,5.,10.,20.],method='DOP853',rtol=2e-12,atol=2e-13,max_step=.08)
    assert out.success,out.message
    for x,y in zip(out.t,out.y.T):
        dre=float(np.linalg.det(y[:4].reshape(2,2))/x**4); dmag=float(y[8]/x**2)
        re,mag=formulas(str(x)); er=abs(dre/float(re)-1); em=abs(dmag/float(mag)-1)
        assert max(er,em)<2e-7,(eps,x,er,em)
        num.append(dict(origin_cutoff=eps,x=float(x),D_RE_ode=dre,D_M_ode=dmag,D_RE_exact=mp.nstr(re,45),D_M_exact=mp.nstr(mag,45),relative_error_RE=er,relative_error_M=em))

# Direct positive integral checks the simplification independently of rational differentiation.
ints=[]
for x in [2,5,10,20]:
    def density(q):
        if q==0: return mp.mpf('0')
        kk=q/mp.sinh(q); ht=mp.coth(q)-1/q
        return q*q*kk*kk*ht*ht+q*q/2*(mp.coth(q)-q/mp.sinh(q)**2)**2
    integ=mp.quad(density,[0,1,x])
    closed=mp.mpf(x)**3/6*(1+3/mp.sinh(x)**2*(1-x*mp.coth(x)))
    assert abs(integ/closed-1)<mp.mpf('1e-55')
    re,mag=formulas(x)
    rem=mp.log(re*mag)-(2*x-6*mp.log(x)+mp.log(mp.mpf(15)/8))
    ints.append(dict(x=x,integral=mp.nstr(integ,55),closed=mp.nstr(closed,55),log_ghost_per_m_asymptotic_residual=mp.nstr(rem,45)))
print('Original matrix ODE and independent scalar quadrature checks passed',flush=True)
result={'assertion_tested':'J1 static adjoint ghost action, origin channels, exact Dirichlet determinant and finite original-ODE checks', 'exact_symbolic_checks':exact,'numerical_checks':num,'quadrature_checks':ints,'tolerances':{'ODE_relative':2e-7,'quadrature_relative':'1e-55'},'max_ODE_relative_error':max(max(v['relative_error_RE'],v['relative_error_M']) for v in num),'software':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__,'mpmath':mp.__version__},'runtime_seconds':time.monotonic()-t0,'outcome':'conditional on numerical tolerance for finite ODE checks; exact symbolic identities plus displayed hand determinant derivation','non_claims':['No full ten-channel J1 vector determinant','No angular/Fourier sum or UV subtraction','No physical broken-holonomy vacuum comparison','No full physical QCD curvature coefficient or alpha prediction']}
with open(args.result,'w') as f: json.dump(result,f,indent=2); f.write('\n')
print(json.dumps({'checks':len(exact),'numerical_cases':len(num),'max_ODE_relative_error':result['max_ODE_relative_error'],'runtime_seconds':result['runtime_seconds']},sort_keys=True))
