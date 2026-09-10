#!/usr/bin/env python3
"""Homogeneous field equations and exact inverse background completion for S_gamma.

All results follow from the displayed minisuperspace action. This is not an
inhomogeneous Dirac count, MOND law, microphysical derivation, or empirical fit.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def derive():
    H,Q,M,gamma,Lambda=s.symbols('H Q M2 gamma Lambda',real=True)
    x,t=s.symbols('X tau',real=True);P=s.Function('P')(x,t)
    V,W,Wt,Vt,Vtt,Wtt=s.symbols('V W Wtau Vtau Vtautau Wtautau',real=True)
    p=P.subs(x,Q*Q);px=s.diff(P,x).subs(x,Q*Q)
    pt=s.diff(P,t).subs(x,Q*Q);ptx=s.diff(P,x,t).subs(x,Q*Q)
    ptt=s.diff(P,t,2).subs(x,Q*Q)
    f=-3*M*H*H+p-V-M*Lambda-2*gamma*Q**3*H
    momenta=s.Matrix([s.diff(f,H),s.diff(f,Q)])
    kinetic=s.hessian(f,(H,Q));inverse=s.simplify(kinetic.inv())
    assert s.simplify(kinetic*inverse-s.eye(2))==s.zeros(2)
    C=s.simplify(momenta.dot(s.Matrix([H,Q]))-f)
    rho=s.simplify(C+3*M*H*H-M*Lambda)
    Hd,Qd=s.symbols('Hdot Qdot',real=True)
    dtfh=s.diff(momenta[0],H)*Hd+s.diff(momenta[0],Q)*Qd
    scale_equation=s.simplify(f+W-H*momenta[0]-dtfh/3)
    pressure=s.simplify(scale_equation-(2*M*Hd+3*M*H*H-M*Lambda))
    # Envelope identity C_tau|p = -f_tau|vel; H0=-a^3 W.
    T=Vt-pt+3*H*W
    gradT=s.Matrix([s.diff(T,H),s.diff(T,Q)])
    canonical_R=s.Matrix([3*f-3*H*momenta[0],-3*H*momenta[1]])
    Delta=s.simplify(3*H*T+(gradT.T*inverse*canonical_R)[0])
    # Explicit clock flow at fixed momenta plus H0 flow, not fixed H,Q.
    zero_flow=inverse*s.Matrix([3*W,-2*Q*ptx])
    source=s.simplify(Vtt-ptt+3*H*Wt+(gradT.T*zero_flow)[0])
    # Repair unknowns: same prescribed q,H,A,rho,p with delta P(q^2)=0.
    A,q,U,B0,qd,hd=s.symbols('A q U B0 qdot Hdot0',real=True)
    dp1,dw,dv=s.symbols('delta_PX delta_W0 delta_V',real=True)
    changes=s.Matrix([2*q*dp1-6*gamma*H*q*q,
                      2*q*q*dp1+dv-6*gamma*H*q**3,
                      -dv+dw+2*gamma*q*q*qd])
    repair=s.solve(list(changes),(dp1,dw,dv),dict=True)[0]
    assert changes.subs(repair)==s.zeros(3,1)
    # Evaluate the repaired branch without substituting a numerical H or q.
    B=s.diff(p,Q,2)
    replacements={Q:q,p:0,px:A/(2*q)+repair[dp1],
        s.diff(P,x,2).subs(x,Q*Q):(B0-A/q)/(4*q*q),
        pt:-A*qd-6*gamma*q*q*H*qd,
        ptx:(-3*H*A-B0*qd)/(2*q)+3*gamma*(H*qd+q*hd),
        V:U,W:U+repair[dw],Vt:-A*qd-3*H*U,
        Lambda:3*H*H-(q*A+U)/M}
    # Apply function jets before Q->q, because Subs uses Q in its evaluation point.
    jets={k:v for k,v in replacements.items() if k not in (Q,V,W,Vt,Lambda)}
    def on_branch(expr):return s.factor(expr.xreplace(jets).subs({k:v for k,v in replacements.items() if k not in jets}))
    delta_branch=s.factor(on_branch(Delta).subs(hd,-(q*A+U)/(2*M)))
    schur=s.simplify(kinetic[1,1]-kinetic[0,1]**2/kinetic[0,0])
    schur_branch=on_branch(schur)
    assert on_branch(T)==0
    assert on_branch(C)==0
    assert s.simplify(on_branch(momenta[1])-A)==0
    assert s.simplify(on_branch(pressure).subs(Qd,qd))==0
    old=-3*A*H*H*(B0*(qd/H+q*U/(2*M*H*H))+3*A)/B0
    assert s.factor(delta_branch.subs(gamma,0)-old)==0
    v=s.symbols('v',real=True)
    Bstation=A/q+2*A*A/U
    qstation=-3*A*H*v/Bstation-q*U/(2*M*H)
    delta_station=s.factor(delta_branch.subs({B0:Bstation,qd:qstation}))
    compact_gap=9*A*A*((H+gamma*q**3/M)**2/schur_branch-v*H*H/B0)
    assert s.factor(delta_station+compact_gap.subs(B0,Bstation))==0
    # Differentiate the actual repaired clock jets, holding X fixed for P_tau.
    qdd=s.symbols('qddot',real=True)
    Ut=-A*qd-3*H*U
    def along(expr):
        return sum(s.diff(expr,z)*zd for z,zd in
                   ((A,-3*H*A),(q,qd),(H,hd),(U,Ut),(qd,qdd)))
    ptbranch=replacements[pt];ptxbranch=replacements[ptx]
    pttbranch=along(ptbranch)-2*q*qd*ptxbranch
    source_branch=on_branch(source.xreplace({ptt:pttbranch})).subs({
        Vtt:along(Ut),Wt:along(U+repair[dw])}).subs(hd,-(q*A+U)/(2*M))
    assert s.factor(source_branch+delta_branch)==0
    flow_residual=kinetic*s.Matrix([hd,qd])-canonical_R-gradT
    assert all(s.factor(on_branch(e).subs(hd,-(q*A+U)/(2*M)))==0 for e in flow_residual)
    # Dimensionless sign reduction is derived, not a prescribed rank or sign.
    R,z,D=s.symbols('R z D',real=True)
    den=R-6*z+6*z*z
    numerator=s.factor(s.together((1+z)**2/den-v/R)*R*den)
    assert s.expand(numerator-(R*(1-v)+(2*R+6*v)*z+(R-6*v)*z*z))==0
    # Explicit non-uniqueness: background matching cannot fix this coefficient.
    free=s.symbols('lambda',real=True)
    invisible=free*(x-q*q)**2/2
    assert invisible.subs(x,q*q)==0 and s.diff(invisible,x).subs(x,q*q)==0
    invisible_delta_B=s.factor((2*s.diff(invisible,x)+4*q*q*s.diff(invisible,x,2)).subs(x,q*q))
    return dict(action_density_over_Na3=str(f),momenta=[str(z) for z in momenta],
        hamiltonian_constraint_over_a3=str(C),rho=str(rho),pressure=str(pressure),
        scale_Euler_equation=str(scale_equation),kinetic_matrix=str(kinetic),
        kinetic_determinant=str(s.factor(kinetic.det())),kinetic_inverse=str(inverse),
        tertiary_over_a3=str(T),lapse_block_over_a3=str(Delta),lapse_source_over_a3=str(source),
        background_repair={str(k):str(z) for k,z in repair.items()},
        repaired_kinetic_schur=str(schur_branch),repaired_lapse_block=str(delta_branch),
        stationary_lapse_block=str(delta_station),
        compact_lapse_gap=str(compact_gap),dimensionless_gap_numerator=str(numerator),
        repaired_source_plus_lapse_block_is_zero=True,
        actual_hamiltonian_flow_matches_repaired_history=True,
        background_invisible_counterterm=str(invisible),
        counterterm_change_to_kinetic_coefficient=str(invisible_delta_B),
        homogeneous_constraints_and_charge_and_pressure_preserved=True,gamma_zero_regression=True,
        full_theory_status='OPEN'),dict(H=H,q=q,A=A,U=U,M=M,gamma=gamma,B0=B0,qd=qd,
              delta=delta_branch,schur=schur_branch)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    result,_=derive()
    if a.result_file:a.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
