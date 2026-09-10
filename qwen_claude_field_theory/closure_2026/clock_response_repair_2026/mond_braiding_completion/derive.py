#!/usr/bin/env python3
"""Exact bare-mixing bracket, covariant cubic completion, and static mass-scaling gate.

No coefficient fit, nonlinear DOF count, empirical validation or full theory.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def bare_mixing():
    x=s.symbols('x',real=True)
    a,b,c,Q,chi,N,L=[s.Function(n)(x) for n in ('a','b','c','Q','chi','N','L')]
    pa,pb,pc,M,eta=s.symbols('pa pb pc M2 eta',real=True)
    vol=s.exp(a+b+c);A=vol*s.exp(-2*a);ps=[pa,pb,pc]
    kin=(sum(p*p for p in ps)-sum(ps)**2/2)/(2*M*vol)
    velocities=[s.diff(kin,p) for p in ps]
    def hb(smear):return -eta*A*s.diff(smear,x)*s.diff(chi,x)
    def el(f,z):return s.diff(f,z)-s.diff(s.diff(f,s.diff(z,x)),x)
    raw=sum(v*(L*el(hb(N),z)-N*el(hb(L),z)) for z,v in zip((a,b,c),velocities))
    raw+=Q*(L*el(hb(N),chi)-N*el(hb(L),chi))
    wedge=L*s.diff(N,x)-N*s.diff(L,x)
    coefficient=eta*A*((velocities[0]-velocities[1]-velocities[2])*s.diff(chi,x)-s.diff(Q,x))
    boundary=s.diff(eta*A*Q*wedge,x)
    assert s.simplify(raw-coefficient*wedge-boundary)==0
    # Weak counterexample on C=H_i=0, not merely an off-shell expression.
    # Flat h, chi'=0, p_a=P0 constant, p_b=p_c chosen to solve C pointwise.
    P0,rho,Lambda,eps,q=s.symbols('P0 rho Lambda epsilon q',real=True)
    B=P0/4+M*(rho+M*Lambda)/P0
    cw=s.factor(kin.subs({a:0,b:0,c:0,pa:P0,pb:B,pc:B})+rho+M*Lambda)
    assert cw==0
    # H_x=-p_a'=0; rho may be the actual regular P(X,tau) density.
    witness=eta*eps*s.cos(x)**2
    integral=s.integrate(witness,(x,0,2*s.pi))
    assert s.simplify(integral-s.pi*eta*eps)==0
    return dict(extra_bracket_integrand=str(coefficient*wedge),
        boundary_term_checked=True,hamiltonian_constraint_witness=str(cw),
        witness='flat metric; chi spatially constant; Q=q+epsilon sin(x); N=1; L=sin(x); p_a=P0!=0; p_b=p_c=P0/4+M2*(rho+M2*Lambda)/P0',
        weak_bracket_integral=str(integral),
        conclusion='Lapse affinity of the bare acceleration mixing does not preserve C self-closure.')


def cubic_completion():
    x,t=s.symbols('x t',real=True)
    a,b,c,N,Q,chi=[s.Function(n)(x,t) for n in ('a','b','c','N','Q','chi')]
    gamma=s.symbols('gamma',real=True)
    vol=s.exp(a+b+c);A=vol*s.exp(-2*a);v=s.diff(chi,x)
    Y=s.exp(-2*a)*v*v;X=Q*Q-Y
    K=(s.diff(a,t)+s.diff(b,t)+s.diff(c,t))/N;Z=s.diff(a,t)*Y/N
    lap=s.diff(A*v,x)/vol
    # Direct divergence definition of Box chi, with chi_dot=NQ.
    cov=gamma*X*(-s.diff(vol*Q,t)+s.diff(N*A*v,x))
    adm=N*vol*gamma*(-s.Rational(2,3)*Q**3*K+2*Q*Z+2*Q*Q*lap+s.exp(-2*a)*v*s.diff(Y,x))
    F=gamma*(Q**3/3-Q*Y)
    Bt=-vol*F;Bx=-gamma*N*A*v*(Q*Q+Y)
    residual=s.expand(cov-adm-s.diff(Bt,t)-s.diff(Bx,x))
    residual=residual.subs(s.diff(chi,t,x),s.diff(N*Q,x)).doit()
    assert s.simplify(residual)==0
    # Actual seven-velocity Hessian in a local orthonormal frame, grad chi along x.
    ks=s.symbols('K11 K22 K33 K12 K13 K23',real=True)
    q,y,M,lap0=s.symbols('Q Y M2 lap_chi',real=True);P=s.Function('P')
    tr=sum(ks[:3]);norm=sum(k*k for k in ks[:3])+2*sum(k*k for k in ks[3:])
    kinetic=M*(norm-tr*tr)/2+P(q*q-y)+gamma*(-s.Rational(2,3)*q**3*tr+2*q*ks[0]*y+2*q*q*lap0)
    Hess=s.hessian(kinetic,(*ks,q));metric=Hess[:6,:6];cross=Hess[:6,6]
    schur=s.simplify(Hess[6,6]-(cross.T*metric.inv()*cross)[0])
    B=s.diff(P(q*q-y),q,2)
    expect=B-4*gamma*q*tr+4*gamma*lap0+2*gamma**2*(q*q-y)*(y+3*q*q)/M
    assert s.simplify(schur-expect)==0
    assert s.simplify(Hess.det()-metric.det()*schur)==0
    return dict(covariant_action='S_clock + integral sqrt(-g) gamma X Box(chi), constant gamma; X=-grad(chi)^2',
        ADM_density_over_Nsqrt_h='gamma[-2Q^3 K/3+2Q Kij chi^i chi^j+2Q^2 D^2 chi+chi^i D_i Y]',
        exact_plane_boundary_identity=True,time_boundary=str(Bt),spatial_boundary=str(Bx),
        metric_hessian_determinant=str(s.factor(metric.det())),
        full_hessian_determinant=str(s.factor(Hess.det())),schur_complement=str(s.factor(schur)),
        nonclaim='Velocity regularity and lapse affinity do not prove the combined clock Dirac chain, energy positivity, or MOND.')


def static_gate():
    x=s.symbols('x',real=True);phi,psi,sigma=[s.Function(z)(x) for z in ('Phi','Psi','sigma')]
    M,gamma,q,C,rho=s.symbols('M2 gamma q C rho',real=True)
    # Independent static Einstein spatial-curvature calculation.
    h=s.exp(-2*psi)*s.eye(3);hi=h.inv()
    def D(f,i):return s.diff(f,x) if i==0 else s.S.Zero
    G=[[[sum(hi[i,j]*(D(h[j,k],l)+D(h[j,l],k)-D(h[k,l],j))/2 for j in range(3))
         for l in range(3)] for k in range(3)] for i in range(3)]
    Ric=s.Matrix(3,3,lambda i,j:sum(D(G[k][i][j],k)-D(G[k][i][k],j)
        +sum(G[k][i][j]*G[l][k][l]-G[l][i][k]*G[k][j][l] for l in range(3)) for k in range(3)))
    R=s.simplify(s.trace(hi*Ric))
    EH=M*s.exp(phi-3*psi)*R/2
    first=M*s.exp(phi-psi)*(s.diff(psi,x)**2-2*s.diff(phi,x)*s.diff(psi,x))
    assert s.simplify(EH-first-s.diff(2*M*s.exp(phi-psi)*s.diff(psi,x),x))==0
    def EL(L,f):return s.diff(L,f)-s.diff(s.diff(L,s.diff(f,x)),x)+s.diff(s.diff(L,s.diff(f,x,2)),x,2)
    # Quadratic static cubic density obtained by expanding the exact ADM identity.
    e=s.symbols('epsilon',real=True)
    Ys=s.exp(2*e*psi)*e**2*s.diff(sigma,x)**2
    lap=s.exp(2*e*psi)*(e*s.diff(sigma,x,2)-e**2*s.diff(psi,x)*s.diff(sigma,x))
    Gstatic=s.exp(e*(phi-3*psi))*gamma*(2*q*q*s.exp(-2*e*phi)*lap
        +s.exp(2*e*psi)*e*s.diff(sigma,x)*s.diff(Ys,x))
    G2=s.expand(s.series(Gstatic,e,0,3).removeO()).coeff(e,2)
    mix=2*gamma*q*q*s.diff(phi,x)*s.diff(sigma,x)
    assert all(s.simplify(EL(G2-mix,f))==0 for f in (phi,psi,sigma))
    L2=M*(s.diff(psi,x)**2-2*s.diff(phi,x)*s.diff(psi,x))+mix-C*s.diff(sigma,x)**2-rho*phi
    eqs={str(f):str(s.simplify(EL(L2,f))) for f in (phi,psi,sigma)}
    # Leading local nonlinear radial reduction, retaining the spatial cubic term.
    r=s.symbols('r',positive=True);g,u=s.symbols('g u',real=True);b=s.symbols('b',nonzero=True)
    F=s.Function('F');Lr=r*r*(-M*g*g+b*g*u-F(u*u))-s.Rational(4,3)*gamma*r*u**3
    scalar=s.diff(Lr,u);metric=s.diff(Lr,g)
    # Do not silently discard the radial Galileon flux to manufacture AQUAL.
    f,gN=s.symbols('F_Y g_N',real=True)
    fy_atom=next(iter(scalar.atoms(s.Subs)))
    scalar_eq=s.simplify(scalar.subs(fy_atom,f)/(2*r*r))
    r1,r2,a0=s.symbols('r1 r2 a0',positive=True)
    u_solution=s.solve(s.Eq(-metric/(2*M*r*r),gN),u)[0]
    u_target=s.simplify(u_solution.subs(gN,g*(1-s.exp(-g/a0))))
    f_required=s.solve(scalar_eq,f)[0]
    mismatch=s.factor(f_required.subs(r,r1)-f_required.subs(r,r2))
    assert s.simplify(mismatch-2*gamma*u*(1/r2-1/r1))==0
    return dict(spatial_Ricci=str(R),quadratic_static_Euler=eqs,
        mixing_coefficient='b=2 gamma q^2',slip_scope='Psi=Phi from its own spatial Euler equation at nonzero k with matched homogeneous boundary; not full PPN',
        radial_Lagrangian=str(Lr),radial_scalar_current=str(scalar),radial_metric_current=str(metric),
        scalar_zero_flux_equation=str(scalar_eq),MOND_required_u=str(u_target),
        required_FY=str(f_required),two_radius_mismatch=str(mismatch),
        result='For this reduced local radial model, nonzero constant gamma cannot give a universal acceleration-only exponential law across different source masses.',
        exclusions='Not a no-go for all KGB: potential-dependent coefficients, singular weak-field scaling, nonzero source-dependent scalar charge, time-dependent branches and extra operators are not covered.')


def main():
    return dict(bare=bare_mixing(),completion=cubic_completion(),static=static_gate(),full_theory_status='OPEN')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    r=main()
    if a.result_file:a.result_file.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
