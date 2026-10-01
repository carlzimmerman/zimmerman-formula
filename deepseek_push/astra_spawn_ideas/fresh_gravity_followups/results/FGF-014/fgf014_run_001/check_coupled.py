"""Finite implementation controls for the exact conditional FGF014 derivation."""
import json, math, itertools
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh

BASE=Path(__file__).resolve().parent
checks=[]
def check(name, value, tol=0.0, detail=None):
    passed=bool(value <= tol)
    checks.append(dict(name=name,observed=float(value),tolerance=tol,passed=passed,detail=detail))
    if not passed: raise AssertionError(checks[-1])

def coeff(law,B):
    if law=='Q':
        g=math.sqrt(B*B+B); lam=2*g/(2*B+1)
    else:
        t=math.sqrt(B); den=-math.expm1(-t)
        g=B/den; FB=1/den-t*math.exp(-t)/(2*den*den); lam=1/FB
    return g,B/g,lam,g*lam-B

def threshold(L,d,m,J,cs,nu):
    A=cs*cs*L*J; b=cs*cs*(L*m-d)-nu*J
    D=math.sqrt(b*b+4*A*nu*m)
    return 2*nu*m/(b+D) if b>=0 else (-b+D)/(2*A)

def mats(k,L,q,h,m,J,cs,nu,K,v):
    H=np.array([[L*k*k,-q*k*h,math.sqrt(nu)*k],[-q*k*h,J*k*k+m,0.],[math.sqrt(nu)*k,0.,cs*cs*k*k]])
    M=np.diag([K,J/v**2,1.])
    return H,M

worst_det=0.; worst_threshold=0.; wrong_inertia=0; worst_marginal=0.
worst_q0=0.; worst_rho0=0.; cells=[]
for law,B,h,margin,cs,nu,K in itertools.product(['Q','R'],[.01,1.,100.],[0.,.6,1.],[.1,1.],[.1,.4],[.01,1.],[.2,2.]):
    g,mu,lam,q=coeff(law,B); L=mu*(1-h*h)+lam*h*h; d=q*q*h*h
    m=q*q/lam+margin; J=.7; v=.6
    yj=threshold(L,d,m,J,cs,nu); kj=math.sqrt(yj)
    residual=abs(cs*cs*yj*(L-d/(J*yj+m))-nu)/nu
    worst_threshold=max(worst_threshold,residual)
    for kr in [.01,.1,.5,.99,1.,1.01,2.,10.,100.]:
        k=kr*kj; H,M=mats(k,L,q,h,m,J,cs,nu,K,v); xs=eigvalsh(H,M)
        scale=max(1.,float(np.max(abs(xs))))
        if kr==1.:
            worst_marginal=max(worst_marginal,abs(xs[0])/scale)
        else:
            wrong_inertia+=int(np.sum(xs < -1e-11*scale)!=(1 if kr<1 else 0))
        # Orthogonal determinant evaluation at non-eigenvalue probes.
        for x in [-.37*scale,.23*scale]:
            Dp=L*k*k-K*x; Dc=J*k*k+m-J*x/v**2
            terms=[(Dp*Dc-d*k*k)*(x-cs*cs*k*k),nu*k*k*Dc]
            P=sum(terms); det=np.linalg.det(H-x*M)
            worst_det=max(worst_det,abs(det+P)/max(1.,abs(det),sum(abs(t) for t in terms)))
    k=.7*kj
    H,M=mats(k,L,0.,h,m,J,cs,nu,K,v)
    s=cs*cs*k*k; z=L*k*k/K; disc=math.sqrt((s-z)**2+4*nu*k*k/K)
    expected=sorted([(s+z-disc)/2,(s+z+disc)/2,(J*k*k+m)*v*v/J])
    worst_q0=max(worst_q0,float(np.max(abs(eigvalsh(H,M)-expected)))/max(1.,max(abs(z) for z in expected)))
    H,M=mats(k,L,q,h,m,J,cs,0.,K,v)
    expected=sorted([*eigvalsh(H[:2,:2],M[:2,:2]),s])
    worst_rho0=max(worst_rho0,float(np.max(abs(eigvalsh(H,M)-expected)))/max(1.,max(abs(z) for z in expected)))
    cells.append(dict(law=law,B_over_a=B,cos_theta=h,margin=margin,cs_over_c=cs,nu=nu,K=K,kJ=kj,old_kJ=math.sqrt(nu/(cs*cs*L))))
check('threshold equation relative residual',worst_threshold,1e-12)
check('finite inertia classifications',wrong_inertia)
check('marginal smallest root normalized',worst_marginal,1e-11)
check('determinant vs proposed polynomial',worst_det,1e-11)
check('q=0 exact factorization roots',worst_q0,1e-11)
check('rho=0 field plus test-fluid roots',worst_rho0,1e-11)
# Constrained K limit: deliberately moderate coefficients, finite roots separated.
k=1.3; L=.8; q=.2; h=.7; m=1.; J=.7; cs=.4; nu=.2; v=.6
He=np.array([[J*k*k+m-q*q*h*h/L,q*h*math.sqrt(nu)/L],[q*h*math.sqrt(nu)/L,cs*cs*k*k-nu/L]])
Me=np.diag([J/v**2,1.]); target=eigvalsh(He,Me); singular=[]
for K in [.01,.001,.0001,.00001,.000001]:
    H,M=mats(k,L,q,h,m,J,cs,nu,K,v); xs=eigvalsh(H,M)
    err=float(np.max(abs(xs[:2]-target)))
    singular.append(dict(K=K,finite_error=err,large_mode_ratio=float(xs[2]*K/(L*k*k))))
check('K limit final two finite roots',singular[-1]['finite_error'],1e-6)
check('K limit diverging root',abs(singular[-1]['large_mode_ratio']-1),1e-6)
check('K limit finite errors decrease',int(not all(a['finite_error']>b['finite_error'] for a,b in zip(singular,singular[1:]))))
# Negative controls are expected failures of deliberately wrong models.
H,M=mats(.5,1.,0.,1.,1.,1.,1.,1.,1.,1.)
actual=eigvalsh(H,M)[0]
check('attractive coupling has known -1/4 eigenvalue',abs(actual+.25),1e-14)
# Wrong repulsive sign gives (x-.25)^2+.25, not the negative root.
check('wrong matter sign rejected at known root',int(abs((actual-.25)**2+.25)<.1))
H,M=mats(.1,1.,1.,1.,.1,1.,1.,0.,1.,1.)
check('violating field Schur creates negative field mode',int(eigvalsh(H,M)[0]>=0))
# Dropping mixing leaves old Jeans cutoff and wrongly declares this interval stable.
L=1.;q=1.;h=1.;m=1.1;J=.7;cs=1.;nu=1.;K=1.;v=.6
new=math.sqrt(threshold(L,q*q,m,J,cs,nu)); mid=(1+new)/2
H,M=mats(mid,L,q,h,m,J,cs,nu,K,v)
check('omitted-mixing old-threshold control rejected',int(eigvalsh(H,M)[0]>=0 or mid<=1))
# Dimensional restorations: distinct frozen histories, not dynamical solutions.
c=299792458.;G=6.67430e-11
rest=[]
for a0 in [9.3619e-11,1.1279e-10]:
    for label,E in [('constant_vacuum',1.),('frozen_H_z3',math.sqrt(.315*4**3+.685))]:
        a=a0*E
        rest.append(dict(a0_m_s2=a0,branch=label,a_star_m_s2=a,length_unit_m=c*c/a,time_unit_s=c/a,omega_unit_s_inv=a/c,density_unit_kg_m3=a*a/(4*math.pi*G*c*c)))
out=dict(status='passed',coefficient_cells=len(cells),spectral_cases=len(cells)*9,checks=checks,worst_metrics=dict(determinant=worst_det,threshold=worst_threshold),cells=cells,K_limit=singular,dimensional_restorations=rest,seed=None,arithmetic='binary64')
(BASE/'numeric_001'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','coefficient_cells','spectral_cases','checks']},indent=2))
