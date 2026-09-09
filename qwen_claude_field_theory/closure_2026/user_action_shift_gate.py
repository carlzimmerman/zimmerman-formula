"""Exact stationary ADM shift dependence of projected scalar derivatives.

Planar metric, tau=t, phi=phi(x). This is not a perturbation DOF count.
"""
import json
import sympy as s
t,x,y,z=s.symbols('t x y z',real=True);coords=(t,x,y,z)
N,a,h,beta,f=[s.Function(n)(x) for n in ('N','a','h','beta','phi')]
metric=s.Matrix([[-N*N+a*a*beta*beta,a*a*beta,0,0],[a*a*beta,a*a,0,0],[0,0,h*h,0],[0,0,0,h*h]])
inverse=s.simplify(metric.inv());ncov=s.Matrix([-N,0,0,0]);n=inverse*ncov
projector=s.simplify(inverse+n*n.T)
df=s.Matrix([s.diff(f,c) for c in coords]);Q=s.simplify(n.dot(df));V=df+ncov*Q
def gamma(k,i,j):
    return s.simplify(sum(inverse[k,l]*(s.diff(metric[l,j],coords[i])+s.diff(metric[l,i],coords[j])-s.diff(metric[i,j],coords[l])) for l in range(4))/2)
DV=s.Matrix(3,3,lambda i,j:s.simplify(s.diff(V[j+1],coords[i+1])-sum(gamma(k,i+1,j+1)*V[k] for k in range(4))))
Y=s.simplify((df.T*projector*df)[0])
H=s.simplify(sum(projector[i+1,k+1]*projector[j+1,l+1]*DV[i,j]*DV[k,l] for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
assert s.diff(Y,beta)==0 and s.diff(H,beta)==0
assert not H.has(s.diff(beta,x))
assert s.simplify(Q+beta*s.diff(f,x)/N)==0
# Unit-clock ADM acceleration and its scalar mixing contraction.
accov=s.Matrix([s.simplify(sum(n[j]*(s.diff(ncov[i],coords[j])-sum(gamma(k,j,i)*ncov[k] for k in range(4))) for j in range(4))) for i in range(4)])
mix=s.simplify((inverse*accov).dot(df))
assert s.simplify(mix-s.diff(N,x)*s.diff(f,x)/(N*a*a))==0
# K'(0), rather than a claimed PPN value, determines the remaining linear term.
k1=s.symbols('Kprime0',real=True)
shift_source=s.simplify(-N*a*h*h*k1*s.diff(Q,beta))
eps=s.symbols('eps',real=True)
K=s.diag(-(a*a*s.diff(beta,x)+a*s.diff(a,x)*beta)/N,
         -h*s.diff(h,x)*beta/N,-h*s.diff(h,x)*beta/N)
hinv=s.diag(1/a**2,1/h**2,1/h**2)
kinvariant=s.trace(hinv*K*hinv*K)
assert s.simplify(s.diff(kinvariant.subs(beta,eps*beta).doit(),eps).subs(eps,0))==0
# Time component of the covariant metric divergence for any stationary
# diagonal metric EL tensor, once its shift components vanish.
ee=s.diag(*[s.Function('E'+str(i))(x) for i in range(4)])
divtime=sum(s.diff(ee[i,0],coords[i]) for i in range(4))
divtime+=sum(gamma(i,i,j)*ee[j,0]+gamma(0,i,j)*ee[i,j] for i in range(4) for j in range(4))
divtime=s.simplify(divtime.subs({beta:0,s.diff(beta,x):0}).doit())
assert divtime==0
print(json.dumps(dict(Q=str(Q),Y=str(Y),projected_derivative=str(DV),
    coherence=str(H),acceleration_mixing=str(mix),
    linear_shift_source_from_K=str(shift_source),stationary_metric_time_divergence=str(divtime),
    condition='Kprime0=0 removes this source; EH and khronometric extrinsic-curvature terms are quadratic about a static zero-shift slice.',
    full_theory='OPEN',scope=__doc__),indent=2))
