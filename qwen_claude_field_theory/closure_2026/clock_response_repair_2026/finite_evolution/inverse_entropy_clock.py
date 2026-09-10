#!/usr/bin/env python3
"""New constructive route: K(Q,tau), rather than shift-only K(Q).

K remains independent of chi itself: a^3 K_Q is conserved. Its explicit clock
dependence frees Qdot from K_QQ. Impose an exactly dustlike combined background,
Q(1+m)=constant, and solve the finite-k pressure response at the r=0 boundary.
This does not certify nonlinear stability or a MOND action.
"""
import json
import sympy as s


def derive():
    a,H,M,A,B,Q,k2,m=s.symbols('a H M2 A B Q k2 m',positive=True)
    mn,mnn,Bn=s.symbols('dm_dln_a d2m_dln_a2 dB_dln_a',real=True)
    z,sig=s.symbols('z sigma',real=True)
    C=A/(2*Q*(1+m)); W=m*Q*A; g=1/(Q*(1+m))
    qdot=-H*Q*mn/(1+m)
    rates={a:a*H,H:-(1+m)*Q*A/(2*M),A:-3*H*A,Q:qdot,k2:-2*H*k2,m:H*mn,mn:H*mnn,B:H*Bn}
    def dt(x):return sum(s.diff(x,v)*d for v,d in rates.items())
    # The old K(Q) tertiary cannot be reused: Qdot+3HA/B no longer vanishes.
    Pz,Ps=s.symbols('Pz Ps',real=True)
    momentum_constraint=H*(Pz+3*a**3*A*sig)+Q*Ps-2*a**3*M*k2*z
    clock_constraint=-W*(Pz+3*a**3*A*sig)/(2*M)+(qdot+3*H*A/B)*Ps+a**3*k2*(A-2*C*Q)*sig
    canonical_ham=-3*a**3*A**2*sig**2/(4*M)+Ps**2/(2*a**3*B)-a**3*M*k2*z**2+a**3*C*k2*sig**2-A*sig*Pz/(2*M)
    def pb(x,y):return sum(s.diff(x,q)*s.diff(y,p)-s.diff(x,p)*s.diff(y,q) for q,p in ((z,Pz),(sig,Ps)))
    derived_tertiary=dt(momentum_constraint)+pb(momentum_constraint,canonical_ham)
    if s.factor(derived_tertiary-clock_constraint)!=0:raise AssertionError('new tertiary must follow from preservation')
    solved=s.solve([momentum_constraint,clock_constraint],[Pz,Ps])
    pz=s.factor(solved[Pz]); ps=s.factor(solved[Ps])
    ham=-3*a**3*A**2*sig**2/(4*M)+ps**2/(2*a**3*B)-a**3*M*k2*z**2+a**3*C*k2*sig**2-A*sig*pz/(2*M)
    omega=s.factor(s.diff(pz,sig)-s.diff(ps,z))
    zd=s.factor((s.diff(ham,sig)+dt(ps))/omega)
    sd=s.factor((-s.diff(ham,z)-dt(pz))/omega)
    alpha=(zd+A*sig/(2*M))/H
    if s.factor(sd-ps/(a**3*B)-Q*alpha)!=0:raise AssertionError('new chi canonical velocity')
    beta=-pz/(2*a**3*M*k2)
    psi=-z-H*beta; phi=alpha+dt(beta)+s.diff(beta,z)*zd+s.diff(beta,sig)*sd
    if s.factor(phi-psi)!=0:raise AssertionError('independent potentials disagree')
    pressure=A*(sd-Q*alpha)-W*alpha # total Pdot=0 on this constructed background
    # Testing zero response for every state needs no expensive change to (Psi,Psi').
    # Use the two independent reduced coordinates directly.
    response=s.Matrix([[s.diff(pressure,z),s.diff(pressure,sig)]]).applyfunc(s.factor)
    equations=[]
    for v in response:
        equations.extend(s.Poly(s.fraction(v)[0],k2).all_coeffs())
    solutions=s.solve(equations,[Bn,mnn],dict=True)
    verified=[]
    for sol in solutions:
        residual=[s.factor(v.subs(sol)) for v in response]
        if any(v!=0 for v in residual):raise AssertionError('inverse response residual')
        e=qdot/H+Q*W/(2*M*H**2)
        verified.append(dict(solution={str(k):str(v) for k,v in sol.items()},e=str(s.factor(e.subs(sol))),
                             wavenumber_independent=all(k2 not in v.free_symbols for v in sol.values())))
    result=dict(pressure_response_basis=['zeta','sigma'],pressure_response=[str(v) for v in response],
        clock_solutions=verified,independent_no_slip_residual=str(s.factor(phi-psi)),
        domain='K(Q,tau), Q(1+m)=constant, r=0, finite k; not the previously tested K(Q) action',
        remaining=['nonlinear health','homogeneous constraint chain for the new action','complete MOND coupling','empirical fit'])
    return result,dict(a=a,H=H,M=M,A=A,B=B,Q=Q,k2=k2,m=m,mn=mn,mnn=mnn,Bn=Bn,
                      Bprime=solutions[0][Bn] if solutions else None,e=qdot/H+Q*W/(2*M*H**2))


if __name__=='__main__':print(json.dumps(derive()[0],indent=2))
