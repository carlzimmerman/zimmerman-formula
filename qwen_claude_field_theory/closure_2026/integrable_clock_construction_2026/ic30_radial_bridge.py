"""IC29 spherical action variation and necessary galaxy/cosmology matching data.

No assigned PPN values, constraint ranks, or full-theory certification.
The radial action is vacuum outside baryons; matter remains minimally coupled.
"""
import argparse
from functools import lru_cache
import json
import sys

import mpmath as mp
import sympy as s


def U(c):
    return (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2


def euler(L, f, r, order=1):
    return sum((-1)**j*s.diff(s.diff(L, s.diff(f, r, j)), r, j)
               for j in range(order+1))


@lru_cache(None)
def radial_action():
    r = s.Symbol('r', positive=True)
    names = ('S', 'w', 'Q', 'q', 'z', 'shear', 'beta', 'ell')
    S,w,Q,q,z,bsh,beta,ell = fields = tuple(s.Function(n)(r) for n in names)
    m,a02,lam,kappa,wc = s.symbols('m a02 Lambda kappa wc', real=True)
    Qdot,qdot = s.symbols('Qdot qdot', real=True)
    A,D,E4 = (s.Function(n)(S) for n in ('A','D','E4'))
    eta = s.Function('eta')(q,w)
    xi = S+w
    u = (S+2*w)/xi
    v = m*s.exp(S+2*w)/2
    t = s.exp(2*S)/v
    J = r**2*s.exp(3*Q)
    P0 = -m*s.exp(4*w)*(lam+a02*U(u**2))+kappa*s.exp(2*w-2*S)/2
    mixed = 2*u*xi*s.diff(xi,r)*s.diff(u,r)+xi**2*s.diff(u,r)**2
    L = J*(2*q*Qdot-2*t*bsh**2/3+t*q**2/6+A*q*z
           +s.exp(S)*P0+D*z**2+E4*z**4+eta*s.exp(S)*ell*(w-wc)
           -2*q*(s.diff(beta,r)+3*beta*s.diff(Q,r)+2*beta/r)/3
           -4*bsh*(s.diff(beta,r)-beta/r)/3)
    L += r**2*s.exp(Q)*(2*v*s.diff(Q,r)**2
          +4*v*s.diff(S+2*w,r)*s.diff(Q,r)+2*v*mixed)
    return dict(r=r,fields=fields,m=m,a02=a02,lam=lam,kappa=kappa,wc=wc,
                Qdot=Qdot,qdot=qdot,A=A,D=D,E4=E4,eta=eta,xi=xi,u=u,v=v,t=t,
                J=J,P0=P0,L=L)


def radial_equations():
    """All eight radial EL equations; Qdot is an independent time jet.

    Spatial differentiation of Qdot is unnecessary here: the symplectic term
    contains no radial derivatives. The full time Euler term is subtracted.
    """
    d=radial_action()
    S,w,Q,q,z,bsh,beta,ell=d['fields']
    eq={str(f.func):euler(d['L'],f,d['r']) for f in d['fields']}
    eq['Q'] -= 2*d['J']*d['qdot']+6*d['J']*q*d['Qdot']
    return eq


@lru_cache(None)
def radial_checks():
    d=radial_action()
    r=d['r']; S,w,Q,q,z,bsh,beta,ell=d['fields']
    J,t,A,D,E4,eta=(d[k] for k in ('J','t','A','D','E4','eta'))
    eq=radial_equations()
    pin=eta*s.exp(S)*ell*(w-d['wc'])
    expected={
        'q':2*d['Qdot']+t*q/3+A*z
            -2*(s.diff(beta,r)+3*beta*s.diff(Q,r)+2*beta/r)/3
            +s.diff(pin,q),
        'shear':-4*(t*bsh+s.diff(beta,r)-beta/r)/3,
        'beta':2*s.diff(q,r)/3+4*s.diff(bsh,r)/3+4*(s.diff(Q,r)+1/r)*bsh,
        'z':A*q+2*D*z+4*E4*z**3,
        'ell':eta*s.exp(S)*(w-d['wc'])}
    checks={name:s.simplify(eq[name]/J-value) for name,value in expected.items()}
    v=d['v']; qp=s.diff(Q,r)
    raw=r**2*s.exp(Q)*v*(-4*s.diff(Q,r,2)-8*qp/r-2*qp**2)
    ibp=r**2*s.exp(Q)*(2*v*qp**2+4*s.diff(v,r)*qp)
    checks['curvature_boundary']=s.simplify(raw-ibp+s.diff(4*r**2*s.exp(Q)*v*qp,r))
    # Differentiate the action first, then eliminate the static trace equation.
    zeq=(eq['z']/J).subs(q,-3*A*z/t)
    checks['static_auxiliary_factor']=s.simplify(zeq-z*(2*D-3*A**2/t+4*E4*z**2))
    return checks


@lru_cache(None)
def static_checks():
    d=radial_action(); r=d['r']; S,w,Q,q,z,bsh,beta,ell=d['fields']
    F,P,u=(s.Function(n)(r) for n in ('Phi','Psi','u'))
    substitution={S:(2-u)*F,w:(u-1)*F,Q:-P-(u-1)*F,
                  q:0,z:0,bsh:0,beta:0,ell:0,d['Qdot']:0}
    got=d['L'].subs(substitution, simultaneous=True).doit()
    m,a02,lam,kappa=(d[k] for k in ('m','a02','lam','kappa'))
    want=r**2*(m*s.exp(F-P)*(s.diff(P,r)**2-2*s.diff(F,r)*s.diff(P,r)
                              +(1-u**2)*s.diff(F,r)**2)
         -m*s.exp(F-3*P)*(lam+a02*U(u**2))+kappa*s.exp(-F-3*P)/2)
    # u equation is not divided by u until the regular branch is specified.
    eu=euler(want,u,r)
    target=2*m*r**2*s.exp(F-3*P)*u*(a02*s.log(1-u**2)**2
                                             -s.exp(2*P)*s.diff(F,r)**2)
    c,y=s.symbols('c y', real=True)
    primitive=y**2+2*(1+y)*s.exp(-y)-2
    legendre=((1-c)*y**2-U(c)).subs(c,1-s.exp(-y))
    # log(exp(-y))=-y over real y, an explicit arithmetic-domain assumption.
    checks={'physical_density':s.simplify(got-want),
            'auxiliary_variation':s.simplify(eu-target),
            'legendre_primitive':s.simplify(legendre-(y**2-primitive)),
            'exponential_mu':s.simplify(s.diff(primitive,y)-2*y*(1-s.exp(-y)))}
    # First independent weak-field equations, before imposing Phi=Psi.
    fp,pp=s.diff(F,r),s.diff(P,r)
    weak=m*r**2*(pp**2-2*fp*pp+(1-u**2)*fp**2)
    checks['spatial_weak']=s.simplify(euler(weak,P,r)
                            -2*m*s.diff(r**2*(fp-pp),r))
    checks['lapse_weak']=s.simplify(euler(weak,F,r)
                       -2*m*s.diff(r**2*(pp-(1-u**2)*fp),r))
    return checks


@lru_cache(None)
def static_geometry():
    """Build Ricci from Christoffels, then vary independent radial/angular metrics."""
    r,theta,phi=s.symbols('r theta phi', positive=True)
    F,a,b,u=(s.Function(n)(r) for n in ('Phi','ar','bt','u'))
    x=(r,theta,phi)
    h=s.diag(s.exp(2*a),s.exp(2*b)*r**2,s.exp(2*b)*r**2*s.sin(theta)**2)
    inv=h.inv()
    Gamma=[[[s.simplify(sum(inv[i,l]*(s.diff(h[l,k],x[j])+s.diff(h[l,j],x[k])
                                 -s.diff(h[j,k],x[l]))/2 for l in range(3)))
             for k in range(3)] for j in range(3)] for i in range(3)]
    Ric=s.Matrix(3,3,lambda i,j:s.simplify(sum(
        s.diff(Gamma[k][i][j],x[k])-s.diff(Gamma[k][i][k],x[j])
        +sum(Gamma[k][i][j]*Gamma[l][k][l]-Gamma[l][i][k]*Gamma[k][j][l]
             for l in range(3)) for k in range(3))))
    R=s.simplify(s.trace(inv*Ric)); N=s.exp(F)
    Hess=s.Matrix(3,3,lambda i,j:s.diff(N,x[i],x[j])
                  -sum(Gamma[k][i][j]*s.diff(N,x[k]) for k in range(3)))
    lap=s.simplify(s.trace(inv*Hess))
    m,a02,lam,kappa=s.symbols('m a02 Lambda kappa', real=True)
    C=lam+a02*U(u**2); X=s.exp(-2*F)/2; f=1-u**2
    dens=N*s.exp(a+2*b)*r**2
    acc2=s.exp(-2*a)*s.diff(F,r)**2
    L=dens*(m*R/2+m*f*acc2-m*C+kappa*X)
    Es={str(v.func):s.simplify(euler(L,v,r,2)/dens) for v in (F,a,b,u)}
    div=s.exp(-a-2*b)/r**2*s.diff(s.exp(-a+2*b)*r**2*f*s.diff(F,r),r)
    lapse=m*R/2-m*C-m*f*acc2-2*m*div-kappa*X
    geometric=m*(Ric-h*R/2+(h*lap-Hess)/N
                  +2*f*s.diag(s.diff(F,r)**2,0,0)-f*h*acc2+C*h)-kappa*X*h
    return dict(r=r,F=F,a=a,b=b,u=u,Ric=Ric,R=R,Hess=Hess,N=N,h=h,
                L=L,Es=Es,lapse=lapse,geometric=geometric,m=m,C=C,X=X,kappa=kappa)


@lru_cache(None)
def metric_checks():
    d=static_geometry(); r=d['r']; F,a,b,u=(d[k] for k in ('F','a','b','u'))
    E=d['Es']; T=d['geometric']; h=d['h']
    out={'lapse_from_variation':s.simplify(E['Phi']-d['lapse']),
         'radial_from_variation':s.simplify(E['ar']+T[0,0]/h[0,0]),
         'angular_from_variation':s.simplify(E['bt']+2*T[1,1]/h[1,1])}
    P=s.Function('Psi')(r); fp,pp=s.diff(F,r),s.diff(P,r)
    sub={a:-P,b:-P}
    er=s.simplify((T[0,0]/d['m']).subs(sub).doit())
    et=s.simplify((T[1,1]/(d['m']*r**2)).subs(sub).doit())
    want=2*(fp-pp)/r+pp**2-2*pp*fp+(1-u**2)*fp**2
    want+=s.exp(-2*P)*(d['C']-d['kappa']*d['X']/d['m'])
    diff=s.diff(P-F,r,2)-s.diff(P-F,r)/r+pp**2-2*pp*fp+(1-2*u**2)*fp**2
    out['radial_isotropic']=s.simplify(er-want)
    out['tracefree_isotropic']=s.simplify(er-et-diff)
    # Off-shell radial diffeomorphism identity checks all three metric equations
    # and the auxiliary equation; no angular equation discarded by gauge fixing.
    out['radial_noether']=s.simplify(
        E['Phi']*fp+E['ar']*s.diff(a,r)+E['bt']*(s.diff(b,r)+1/r)
        +E['u']*s.diff(u,r)
        -s.diff(E['ar'],r)-E['ar']*(fp+s.diff(a,r)+2*s.diff(b,r)+2/r))
    return out


def matching(y, epsilon, wc=None):
    """Leading quasistatic MOND boundary jets. epsilon=a0*r/c^2>0.

    The numeric differentiation is independent of the analytic derivative.
    No finite-radius matching solution is claimed.
    """
    y,epsilon=mp.mpf(y),mp.mpf(epsilon)
    wc=mp.mpf('-.025') if wc is None else mp.mpf(wc)
    if y<=0 or epsilon<=0 or wc>=0:
        raise ValueError('Requires y>0, epsilon>0, wc<0')
    mu=-mp.expm1(-y); u=mp.sqrt(mu); lp=mu+y*mp.exp(-y)
    xi=wc/(u-1)
    ryprime=-2*y*mu/lp
    ruprime=mp.diff(lambda v:mp.sqrt(-mp.expm1(-v)),y)*ryprime
    rwprime=xi*ruprime+(u-1)*epsilon*y
    direct=mp.diff(lambda t:(mp.sqrt(-mp.expm1(-(y+ryprime*t)))-1)
                                      *(xi+epsilon*y*t),0)
    return {'y':y,'u':u,'xi':xi,'w_at_join':(u-1)*xi,
            'r_wprime':rwprime,'r_wprime_direct':direct,
            'derivative_residual':rwprime-direct,
            'constitutive_residual':u*u+mp.exp(-y)-1,
            'mass_law_derivative_residual':mp.diff(lambda v:v*(-mp.expm1(-v)),y)
                                               *ryprime+2*y*mu}


@lru_cache(None)
def collar_construction():
    """Exact momentum-compatible initial collar, NOT a full constraint solution.

    Dimensionless radii 1..2, Q spatially constant on this initial slice.
    The q profile is C3 at both ends. All other EL equations remain obligations.
    """
    r=s.Symbol('r',positive=True); R=s.Symbol('R',positive=True)
    x=r-1
    f=35*x**4-84*x**5+70*x**6-20*x**7
    q=-f
    shear=s.factor(-s.integrate(R**3*s.diff(q,r).subs(r,R),(R,1,r))/(2*r**3))
    charge=s.simplify(8*shear.subs(r,2))
    t,H=s.symbols('t H',real=True)
    tail=charge/r**3
    beta=H*r+t*charge/(3*r**2)
    return dict(r=r,q=q,shear=shear,charge=charge,tail=tail,beta=beta,t=t,H=H)


@lru_cache(None)
def collar_checks():
    d=radial_action(); r=d['r']; S,w,Q,q,z,bsh,beta,ell=d['fields']
    eq=radial_equations()
    weighted=r**3*s.exp(3*Q)*bsh
    checks={'integrating_factor':s.simplify(s.diff(weighted,r)
        +r**3*s.exp(3*Q)*s.diff(q,r)/2
        -3*r**3*s.exp(3*Q)*(eq['beta']/d['J'])/4)}
    c=collar_construction(); r=c['r']; qc=c['q']; sh=c['shear']
    checks.update({'collar_momentum':s.simplify(s.diff(qc,r)/2+s.diff(sh,r)+3*sh/r),
        'inner_q':qc.subs(r,1),'outer_q':qc.subs(r,2)+1,
        'inner_shear':sh.subs(r,1),
        'outer_shear_match':s.simplify(sh.subs(r,2)-c['tail'].subs(r,2)),
        'tail_momentum':s.simplify(s.diff(c['tail'],r)+3*c['tail']/r),
        'tail_shift':s.simplify(s.diff(c['beta'],r)-c['beta']/r+c['t']*c['tail'])})
    for j in (1,2,3):
        for end in (1,2):
            checks['q_jet_%s_%s'%(j,end)]=s.diff(qc,r,j).subs(r,end)
    for j in (1,2,3):
        checks['shear_inner_jet_%s'%j]=s.diff(sh,r,j).subs(r,1)
        checks['shear_outer_jet_%s'%j]=s.simplify(
            (s.diff(sh,r,j)-s.diff(c['tail'],r,j)).subs(r,2))
    return checks


def solve_z(q,A,D,E4):
    """Unique real stationary z for D>0,E4>=0, without coefficient retuning."""
    q,A,D,E4=map(mp.mpf,(q,A,D,E4))
    if D<=0 or E4<0:
        raise ValueError('The monotone auxiliary branch requires D>0,E4>=0')
    if E4==0:
        return -A*q/(2*D)
    return 2*mp.sqrt(D/(6*E4))*mp.sinh(mp.asinh(
        -3*A*q*mp.sqrt(6*E4/D)/(4*D))/3)


def collar_auxiliary_rows():
    # These are IC29's coefficient VALUES at S=.1, held fixed through this
    # slice diagnostic. This does not solve the still-missing S,w constraints.
    A,D,E4=map(mp.mpf,('.1','.13','.01'))
    r=s.Symbol('r',positive=True)
    qfun=s.lambdify(r,collar_construction()['q'],'mpmath')
    rows=[]
    for radius in map(mp.mpf,('1','1.1','1.25','1.5','1.75','1.9','2')):
        q=qfun(radius); z=solve_z(q,A,D,E4)
        residual=lambda Z:A*q+2*D*Z+4*E4*Z**3
        jac=mp.diff(residual,z)
        rows.append(dict(r=radius,q=q,z=z,z_residual=residual(z),
                         z_jacobian=jac,z_derivative_residual=
                         mp.diff(lambda qq:solve_z(qq,A,D,E4),q)*jac+A))
    return rows


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--strict',action='store_true')
    parser.add_argument('--equations',action='store_true')
    args=parser.parse_args()
    checks={}
    for label,fn in (('radial',radial_checks),('static',static_checks),
                     ('metric',metric_checks),('collar',collar_checks)):
        checks[label]={k:str(v) for k,v in fn().items()}
    with mp.workdps(50):
        rows=[matching(y,'1e-6') for y in ('.001','.1','1','10')]
        zrows=collar_auxiliary_rows()
        ok=all(v=='0' for group in checks.values() for v in group.values())
        ok=ok and all(row['r_wprime']<0 and abs(row['derivative_residual'])<mp.mpf('1e-40')
            and abs(row['constitutive_residual'])<mp.mpf('1e-40')
            and abs(row['mass_law_derivative_residual'])<mp.mpf('1e-40') for row in rows)
        ok=ok and all(row['z']>=0 and row['z_jacobian']>0
            and abs(row['z_residual'])<mp.mpf('1e-40')
            and abs(row['z_derivative_residual'])<mp.mpf('1e-40') for row in zrows)
        result={'exact_residuals':checks,'matching':[{k:mp.nstr(v,42) for k,v in row.items()}
                 for row in rows],'scoped_checks':bool(ok),'full_theory':'OPEN'}
        result['momentum_collar']={k:str(v) for k,v in collar_construction().items()}
        result['collar_z']=[{k:mp.nstr(v,42) for k,v in row.items()} for row in zrows]
        if args.equations:
            result['radial_equations']={k:str(s.factor(v)) for k,v in radial_equations().items()}
        print(json.dumps(result,indent=2))
    return 1 if not ok else (2 if args.strict else 0)


if __name__=='__main__':
    sys.exit(main())
