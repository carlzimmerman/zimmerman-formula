#!/usr/bin/env python3
"""IC-1 action-derived construction identities; no full-theory certificate.

All output is regenerated from ACTION.md's formulas. Ranks are computed, not
stored expected counts. Exact identities and numerical witnesses are labeled
separately. --require-full-closure deliberately remains nonzero while listed
obligations have no proof; exit zero by itself certifies no physical theory.
"""
import argparse
from functools import lru_cache
import json

import numpy as np
import sympy as s


def potential(c):
    t = 1-c
    return t*(s.log(t)**2-2*s.log(t)+2)-2


def pb(f, g, qs, ps):
    return sum(s.diff(f,q)*s.diff(g,p)-s.diff(f,p)*s.diff(g,q)
               for q,p in zip(qs,ps))


@lru_cache(None)
def kinetic():
    N,m = s.symbols('N m', positive=True)
    u = s.Symbol('u', real=True)
    vs = s.symbols('hd11 hd22 hd33 hd12 hd13 hd23 Nd ud')
    hd = s.Matrix([[vs[0],vs[3],vs[4]], [vs[3],vs[1],vs[5]],
                   [vs[4],vs[5],vs[2]]])
    W = (u-1)*vs[6]/N**2+s.log(N)*vs[7]/N
    Q = hd/(2*N)-s.eye(3)*W
    L = m*N*(s.trace(Q*Q)-s.trace(Q)**2)/2
    momenta = [s.diff(L,v) for v in vs]
    trace = sum(momenta[:3])  # orthonormal frame, no off-diagonal trace
    residuals = [s.expand(momenta[6]+2*(u-1)*trace/N),
                 s.expand(momenta[7]+2*s.log(N)*trace)]
    H = s.hessian(L,vs)
    nulls = [s.Matrix([2*(u-1)/N]*3+[0,0,0,1,0]),
             s.Matrix([2*s.log(N)]*3+[0,0,0,0,1])]
    # General metric coordinates for the canonical brackets. For off-diagonal
    # h_ij the conjugate coordinate momentum is 2*pi^ij; sum(q*p)=h_ij*pi^ij.
    hs, ps = s.symbols('h0:6'), s.symbols('p0:6')
    pN, pu = s.symbols('pN pu')
    pi = sum(q*p for q,p in zip(hs,ps))
    CN, Cu = pN+2*(u-1)*pi/N, pu+2*s.log(N)*pi
    qs, pvec = (*hs,N,u), (*ps,pN,pu)
    point_map=s.Matrix([s.exp(-2*(u-1)*s.log(N))*h for h in hs]+[N,u])
    return dict(L=L,hessian=H,rank=H.rank(),
                primary_residuals=residuals,primaries=[CN,Cu],
                null_residuals=[list((H*v).applyfunc(s.simplify)) for v in nulls],
                bracket=s.simplify(pb(CN,Cu,qs,pvec)),
                missing_term_bracket=s.simplify(pb(CN,pu,qs,pvec)),
                point_map_jacobian=s.simplify(point_map.jacobian(qs).det()))


@lru_cache(None)
def constitutive():
    c,y,a0,g = s.symbols('c y a0 g', positive=True)
    u = s.Symbol('u', real=True)
    U = potential(c)
    Laux = (1-u*u)*g*g-a0*a0*potential(u*u)
    Eu = s.factor(s.diff(Laux,u))
    mu = 1-s.exp(-y)
    primitive = y*y+2*(1+y)*s.exp(-y)-2
    effective = s.simplify(((1-c)*a0*a0*y*y-a0*a0*U).subs(c,mu))
    return dict(auxiliary_equation=Eu,U_prime=s.simplify(s.diff(U,c)),
                legendre_residual=s.simplify(effective-2*a0*a0*(1-(1+y)*s.exp(-y))),
                primitive_residual=s.simplify(s.diff(primitive,y)/(2*y)-mu),
                deep_limit=s.limit(mu/y,y,0),newtonian_limit=s.limit(mu,y,s.oo),
                boundary_auxiliary_equation=Eu.subs(u,0),
                potential_series=s.series(potential(u*u),u,0,9))


@lru_cache(None)
def static_sector():
    m,a0,kappa = s.symbols('m a0 kappa',positive=True)
    phi,psi,u,rho,Lambda = s.symbols('Phi Psi u rho Lambda',real=True)
    gp,gs,gu = [s.symbols(label+'0:3') for label in ('p','s','u')]
    hp,hs = s.symbols('pp0:3'),s.symbols('ss0:3')
    Lgrad = m*(sum(t*t for t in gs)-2*sum(a*b for a,b in zip(gp,gs))
               +(1-u*u)*sum(t*t for t in gp))
    L = Lgrad-rho*phi-m*a0*a0*potential(u*u)
    def derivative(f,i):
        return (s.diff(f,phi)*gp[i]+s.diff(f,psi)*gs[i]+s.diff(f,u)*gu[i]
                +s.diff(f,gp[i])*hp[i]+s.diff(f,gs[i])*hs[i])
    Ephi=s.expand(s.diff(L,phi)-sum(derivative(s.diff(L,gp[i]),i) for i in range(3)))
    Epsi=s.expand(s.diff(L,psi)-sum(derivative(s.diff(L,gs[i]),i) for i in range(3)))
    divmu = u*u*sum(hp)+2*u*sum(a*b for a,b in zip(gu,gp))
    # Both equations are varied before using the slip boundary condition.
    no_slip = {hs[i]:hp[i] for i in range(3)}
    clock = kappa*s.exp(-phi-3*psi)/2
    A,B=s.exp(phi-psi),s.exp(phi-3*psi)
    Lstatic=A*Lgrad-m*B*(Lambda+a0*a0*potential(u*u))+clock
    Ephi_exact=s.expand(s.diff(Lstatic,phi)-sum(derivative(s.diff(Lstatic,gp[i]),i) for i in range(3)))
    Epsi_exact=s.expand(s.diff(Lstatic,psi)-sum(derivative(s.diff(Lstatic,gs[i]),i) for i in range(3)))
    return dict(Ephi=Ephi,Epsi=Epsi,
                exact_conformal_density=Lstatic,
                exact_conformal_Ephi=Ephi_exact,exact_conformal_Epsi=Epsi_exact,
                poisson_residual=s.expand(Ephi.subs(no_slip)-(2*m*divmu-rho)),
                slip_residual=s.expand(Epsi-2*m*(sum(hp)-sum(hs))),
                measured_G=s.simplify(1/(4*s.pi*s.diff(Ephi.subs(no_slip).subs(u,1),hp[0]))),
                clock_lapse_source=s.diff(clock,phi),
                clock_spatial_source=s.diff(clock,psi))


@lru_cache(None)
def homogeneous():
    B,N,m,a0,kappa = s.symbols('B N m a0 kappa',positive=True)
    u,p,pN,pu,Bd,Lambda = s.symbols('u p pN pu Bd Lambda',real=True)
    C=Lambda+a0*a0*potential(u*u)
    r=3*u-4
    L=-3*m*B*Bd*Bd*N**r-m*B**3*N**(r+2)*C+kappa*B**3*N**r/2
    momentum=s.diff(L,Bd)
    velocity=s.solve(s.Eq(p,momentum),Bd)[0]
    H=s.expand((p*Bd-L).subs(Bd,velocity))
    qs,ps=(B,N,u),(p,pN,pu)
    constraints=[pN,pu,s.factor(pb(pN,H,qs,ps)),s.factor(pb(pu,H,qs,ps))]
    omega=s.Matrix([[pb(f,g,qs,ps) for g in constraints] for f in constraints])
    Hess=s.hessian(H,(N,u))
    drift=s.Matrix([pb(c,H,qs,ps) for c in constraints[2:]])
    # C_i=-H_i, so Cdot_i=drift_i-H_ij lambda_j. Derive the two-by-two
    # solve with independent jets; applying this identity to the actual Hess
    # avoids expanding hundreds of identical logarithmic terms unnecessarily.
    j11,j12,j22,d1,d2=s.symbols('j11 j12 j22 d1 d2')
    J=s.Matrix([[j11,j12],[j12,j22]])
    rhs=s.Matrix([d1,d2])
    lam=J.inv()*rhs
    residual=list((rhs-J*lam).applyfunc(s.cancel))
    mapping={j11:Hess[0,0],j12:Hess[0,1],j22:Hess[1,1],d1:drift[0],d2:drift[1]}
    multipliers=[t.subs(mapping,simultaneous=True) for t in lam]
    return dict(symbols=(B,N,u,p,pN,pu,m,a0,kappa,Lambda),L=L,H=H,
                momentum=momentum,velocity=velocity,
                legendre_residual=s.simplify(s.diff(H,p)-velocity),
                constraints=constraints,omega=omega,Hessian=Hess,drift=drift,
                multipliers=multipliers,
                preservation_residuals=[s.simplify(pb(pN,H,qs,ps)-constraints[2]),
                                        s.simplify(pb(pu,H,qs,ps)-constraints[3]),*residual],
                regularity_condition='det d^2 H / d(N,u)^2 != 0')


@lru_cache(None)
def witness():
    d=homogeneous()
    B,N,u,p,pN,pu,m,a0,kappa,Lambda=d['symbols']
    uv=s.Rational(2,3)
    Nv=s.exp(s.Rational(1,4))
    av2=9*s.exp(-s.Rational(1,2))/(16*s.log(s.Rational(5,9))**2)
    Lv=s.exp(-s.Rational(1,2))-av2*potential(uv*uv)
    hv=1/s.sqrt(6)
    pv=-6*Nv**(3*uv-4)*hv
    sub={B:1,N:Nv,u:uv,p:pv,pN:0,pu:0,m:1,a0:s.sqrt(av2),kappa:1,Lambda:Lv}
    omega_exact=d['omega'].subs(sub).applyfunc(s.simplify)
    om=np.array(omega_exact.evalf(30),dtype=float)
    singular=np.linalg.svd(om,compute_uv=False)
    rank=int(np.linalg.matrix_rank(om,tol=1e-10))
    hessian_exact=d['Hessian'].subs(sub).applyfunc(s.simplify)
    Hess=np.array(hessian_exact.evalf(30),dtype=float)
    drift=np.array(d['drift'].subs(sub).evalf(30),dtype=float).ravel()
    multipliers=np.linalg.solve(Hess,drift)
    Bdot=float(d['velocity'].subs(sub).evalf(30))
    Nnum=float(Nv)
    Hphys=(Bdot+float(uv-1)*multipliers[0]/Nnum+float(s.log(Nv))*multipliers[1])/Nnum
    # Constant N,u means p grows as B². Test p_dot from the actual H.
    pdot_exact=s.simplify(-s.diff(d['H'],B).subs(sub))
    return dict(parameters={str(k):str(v) for k,v in sub.items()},
                constraint_residuals=[float(c.subs(sub).evalf(30)) for c in d['constraints']],
                exact_constraint_residuals=[str(s.simplify(c.subs(sub))) for c in d['constraints']],
                omega=om.tolist(),Hessian=Hess.tolist(),
                hessian_determinant_exact=str(s.simplify(hessian_exact.det())),
                singular_values=singular.tolist(),rank=rank,
                first_class=len(d['constraints'])-rank,second_class=rank,
                count=(6-2*(len(d['constraints'])-rank)-rank)/2 if rank==len(d['constraints']) else None,
                multiplier_values=multipliers.tolist(),physical_H=Hphys,
                exact_pdot_residual=str(s.simplify(pdot_exact-2*hv*pv)),
                full_theory_closed=False,
                scope='Homogeneous regular branch only; numerical rank with exact residual controls')


@lru_cache(None)
def homogeneous_family():
    """Exact regular expanding family, with m,kappa,B still arbitrary positive."""
    d=homogeneous()
    B,N,u,p,pN,pu,m,a0,kappa,Lambda=d['symbols']
    ell=s.log(s.Rational(9,5)); f=s.exp(-s.Rational(1,2))
    uv=s.Rational(2,3); Nv=s.exp(s.Rational(1,4))
    av2=9*kappa*f/(16*m*ell**2)
    Lv=kappa*f/m-av2*potential(uv**2)
    h=s.sqrt(kappa/(6*m))
    pv=-6*m*B**2*f*h
    sub={N:Nv,u:uv,p:pv,pN:0,pu:0,a0:s.sqrt(av2),Lambda:Lv}
    def clean(expr):
        return s.simplify(s.expand_log(expr,force=True))
    constraints=[clean(c.subs(sub)) for c in d['constraints']]
    Hd=d['Hessian'].subs(sub).applyfunc(clean)
    change=s.diag(Nv,1)  # On H_i=0, xi=lnN Hessian is J^T H_ij J.
    M=(change*Hd*change/(kappa*B**3*f)).applyfunc(clean)
    D=clean(M.det())
    cross=s.Matrix([s.diff(d['H'],p,N),s.diff(d['H'],p,u)]).subs(sub).applyfunc(clean)
    reduced=clean(s.diff(d['H'],p,2).subs(sub)-(cross.T*Hd.inv()*cross)[0])
    drift=[clean(x.subs(sub)) for x in d['drift']]
    return dict(M=M,determinant=D,
                determinant_residual=clean(D-(72/(5*ell)-s.Rational(45,4))),
                reduced_hessian=reduced,
                reduced_hessian_residual=clean(reduced-3/(2*m*B*f*D)),
                constraint_residuals=constraints,
                flow_residuals=[clean(d['velocity'].subs(sub)-B*h),
                                clean(-s.diff(d['H'],B).subs(sub)-2*h*pv),*drift],
                physical_H=h/Nv,a0_squared=av2,Lambda=clean(Lv),
                logarithm_bound='0 < ln(9/5) < 4/5 implies det(M) > 27/4')


@lru_cache(None)
def spatial_transform():
    """Conformal R3 transformation and one spatial integration by parts."""
    xi,u,dx,du,R=s.symbols('xi u dx du R',real=True)
    w=(u-1)*xi
    dw=s.diff(w,xi)*dx+s.diff(w,u)*du
    dlogweight=s.diff(xi+w,xi)*dx+s.diff(xi+w,u)*du
    # sqrt(h) N R(h)=sqrt(barh) exp(xi+w)[barR-4barDelta(w)-2|Dw|²].
    # Integrating -4 exp(xi+w) Delta(w) contributes +4 D(xi+w) Dw.
    expression=s.expand(R+4*dlogweight*dw-2*dw**2+2*(1-u*u)*dx**2)
    reduced=R+4*u*xi*dx*du+2*xi*xi*du*du
    return dict(transformed_bracket=expression,
                identity_residual=s.expand(expression-reduced),
                mixed_coefficient=s.diff(expression,dx,du),
                lapse_gradient_coefficient=s.diff(expression,dx,2))


@lru_cache(None)
def tensor_sector():
    z=s.Symbol('z',real=True)
    g=s.Function('gamma')(z)
    metric=s.diag(s.exp(g),s.exp(-g),1)
    inverse=metric.inv()
    def dx(f,i):
        return s.diff(f,z) if i==2 else s.S.Zero
    Gamma=[[[s.simplify(sum(inverse[i,l]*(dx(metric[l,k],j)+dx(metric[l,j],k)
                      -dx(metric[j,k],l)) for l in range(3))/2)
             for k in range(3)] for j in range(3)] for i in range(3)]
    Ric=s.Matrix(3,3,lambda i,j: s.simplify(sum(
        dx(Gamma[k][i][j],k)-dx(Gamma[k][i][k],j)
        +sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k]
             for l in range(3)) for k in range(3))))
    R=s.simplify(s.trace(inverse*Ric))
    N,m=s.symbols('N m',positive=True)
    gd,gz,W=s.symbols('gd gz W',real=True)
    Q=s.diag(gd/(2*N)-W,-gd/(2*N)-W,-W)
    L=m*N*(s.trace(Q*Q)-s.trace(Q)**2+R.subs(s.diff(g,z),gz))/2
    kt=s.simplify(s.diff(L,gd,2))
    ks=s.simplify(-s.diff(L,gz,2))
    return dict(R=R,L=L,ricci_residual=s.simplify(R+s.diff(g,z)**2/2),
                kinetic_hessian=kt,physical_speed_squared=s.simplify(ks/(kt*N*N)))


@lru_cache(None)
def matter_ward():
    """Normal-coordinate check for minimally coupled canonical matter psi.

    The equality is tensorial. Covariant derivatives of a scalar commute;
    hence checking arbitrary first/second jets at a normal-coordinate point
    is sufficient for this particular matter-action identity.
    """
    eta=s.diag(-1,1,1,1)
    gradient=s.Matrix(s.symbols('psi0:4'))
    upper=eta*gradient
    entries=s.symbols('psi00 psi01 psi02 psi03 psi11 psi12 psi13 psi22 psi23 psi33')
    Hess=s.zeros(4)
    for v,(i,j) in zip(entries,[(i,j) for i in range(4) for j in range(i,4)]):
        Hess[i,j]=Hess[j,i]=v
    V,Vp=s.symbols('V Vp')
    stress=upper*upper.T-eta*((gradient.T*upper)[0]/2+V)
    diverg=[]
    for nu in range(4):
        diverg.append(s.expand(sum(sum(s.diff(stress[mu,nu],gradient[j])*Hess[mu,j]
                                       for j in range(4))
                                  +s.diff(stress[mu,nu],V)*Vp*gradient[mu]
                                  for mu in range(4))))
    EL=s.trace(eta*Hess)-Vp
    return dict(matter_EL=EL,divergence=diverg,
                residuals=[s.expand(diverg[i]-EL*upper[i]) for i in range(4)])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    kin,con,sta,hom,ten=kinetic(),constitutive(),static_sector(),homogeneous(),tensor_sector()
    result={
        'action_id':'IC-1', 'status':'OPEN',
        'kinetic':{k:kin[k] for k in ('rank','primary_residuals','bracket','missing_term_bracket','point_map_jacobian')},
        'constitutive':con,
        'static':{k:sta[k] for k in ('Ephi','Epsi','poisson_residual','slip_residual','measured_G','clock_lapse_source','clock_spatial_source')},
        'homogeneous':{k:hom[k] for k in ('H','constraints','legendre_residual','preservation_residuals','regularity_condition')},
        'expanding_witness':witness(), 'expanding_family':homogeneous_family(),
        'spatial_transform':spatial_transform(), 'tensor':ten,
        'matter_ward':matter_ward(),
        'unproved':['full functional secondary constraint closure','local scalar/vector reduction and stability',
                    'regular k=0 to k!=0 relation','u=0 nonlinear branch','acceptable instantaneous response',
                    'full physical static solution with clock stress','beta and preferred-frame PPN',
                    'viable cosmic history','empirical fit','global novelty']}
    print(json.dumps(result,default=str,sort_keys=True,indent=2))
    return 2 if args.require_full_closure else 0


if __name__=='__main__':
    raise SystemExit(main())
