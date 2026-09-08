#!/usr/bin/env python3
"""IC-6: tensor-balanced revision of the explicit IC-5 phase Hamiltonian.

Exact flat-isotropic tensor calculation, actual homogeneous constraint tangent,
and explicitly limited same-action bridges. Not an all-background certificate.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform

import sympy as s

HERE=Path(__file__).resolve().parent
BASE="6708f1e3e"
INPUTS={
    "IC4_ACTION.md":"cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8",
    "local_clock_wave.py":"a88d84135ea99263c62ecc339feffc76830623fb70b394222a1843174be7511d",
    "scalar_completion.py":"801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745",
    "nonlinear_square_completion.py":"4c9a79caa9a6d54a6a5f006440886f54b9092d68978249fb79f95a0f73229ece",
}


def clean(value):
    if isinstance(value,s.MatrixBase):
        return value.applyfunc(lambda v:s.factor(s.simplify(v)))
    return s.factor(s.simplify(value))


def load_wave():
    for name,digest in INPUTS.items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError("Pinned input changed: "+name)
    path=HERE/"local_clock_wave.py"
    spec=importlib.util.spec_from_file_location("tensor_balance_wave_source",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derive()


def ricci(metric,coordinates):
    inverse=metric.inv()
    connection=[[[clean(sum(inverse[i,l]*(s.diff(metric[l,j],coordinates[k])
        +s.diff(metric[l,k],coordinates[j])-s.diff(metric[j,k],coordinates[l]))
        for l in range(3))/2) for k in range(3)] for j in range(3)] for i in range(3)]
    tensor=s.Matrix(3,3,lambda i,j:clean(sum(
        s.diff(connection[l][i][j],coordinates[l])-s.diff(connection[l][i][l],coordinates[j])
        +sum(connection[l][l][b]*connection[b][i][j]-connection[l][j][b]*connection[b][i][l]
             for b in range(3)) for l in range(3))))
    return connection,tensor,clean(s.trace(inverse*tensor))


@lru_cache(None)
def derive():
    m,A,N,k,a02=s.symbols("m A N k a0_squared",positive=True)
    eps,gamma,gd,HA,wdot,Q,p,Pt,F=s.symbols(
        "epsilon gamma gammadot H_coordinate wdot Q p P_tensor F",real=True)
    xyz=s.symbols("x_coordinate y_coordinate z_coordinate",real=True)
    co,si=s.cos(k*xyz[2]),s.sin(k*xyz[2])
    metric=s.diag(A*A*s.exp(eps*gamma*co),A*A*s.exp(-eps*gamma*co),A*A)
    metric_dot=2*HA*metric+gd*s.diff(metric,gamma)
    Kmixed=clean(metric.inv()*metric_dot/(2*N))
    Qmixed=Kmixed-wdot*s.eye(3)/N
    Qtrace=clean(s.trace(Qmixed))
    QTF=clean(Qmixed-Qtrace*s.eye(3)/3)
    QTF2=clean(s.trace(QTF*QTF))
    connection,Rij,R=ricci(metric,xyz)
    R1=clean(s.diff(R,eps).subs(eps,0))
    R2=clean(s.diff(R,eps,2).subs(eps,0)/2)
    determinant=clean(metric.det())
    PTF=s.diag(eps*Pt*co,-eps*Pt*co,0)
    tensor_norm=clean(s.trace(PTF*PTF))
    JT=1+p*p*F/(m*m*a02)
    branches={}
    residuals={"TT_volume":determinant-A**6,"TT_linear_R":R1,
        "trace_unperturbed":clean(s.diff(Qtrace,eps)),
        "trace_geometry":clean(Qtrace-3*(HA-wdot)/N)}
    p1,p2=s.symbols("p_first_jet p_second_jet",real=True)
    for name,K in (("IC5",s.Integer(1)),("IC6",JT)):
        # The omitted potential/clock terms have no tensor dependence: the
        # exact exponential TT completion has constant volume and fixed xi,u.
        phase=2*s.trace(PTF*QTF)+2*p*Q/3-2*tensor_norm/(m*K)+p*p/(3*m)+m*JT*R/2
        Pt_solution=clean(s.solve(s.diff(phase,Pt),Pt)[0])
        phase_reduced=clean(phase.subs(Pt,Pt_solution))
        pEL=s.diff(phase_reduced,p)
        p0=clean(s.solve(pEL.subs(eps,0),p)[0])
        shifted_EL=pEL.subs(p,p0+eps*p1+eps*eps*p2)
        p1_solution=clean(s.solve(s.diff(shifted_EL,eps).subs(eps,0),p1)[0])
        p2_solution=clean(s.solve((s.diff(shifted_EL,eps,2).subs(eps,0)/2)
                                  .subs(p1,p1_solution),p2)[0])
        p_residual=clean(s.diff(shifted_EL.subs({p1:p1_solution,p2:p2_solution}),eps,2).subs(eps,0))
        # A second-order p response is retained; its action contribution
        # vanishes at this order because the zeroth-order p EL is satisfied.
        shifted_phase=phase_reduced.subs(p,p0+eps*eps*p2_solution)
        action_shift_residual=clean(s.diff(shifted_phase-phase_reduced.subs(p,p0),eps,2).subs(eps,0))
        quadratic=clean(s.diff(phase_reduced,eps,2).subs({eps:0,p:p0})/2)
        twice_average=clean(2*s.expand(quadratic).subs({co**2:s.Rational(1,2),si**2:s.Rational(1,2)}))
        L2=clean(N*A**3*twice_average)
        kinetic=clean(s.diff(L2,gd,2)*2*N/(m*A**3))
        gradient=clean(-s.diff(L2,gamma,2)*2/(m*N*A*k*k))
        coordinate_omega2=clean(-s.diff(L2,gamma,2)/s.diff(L2,gd,2))
        speed=clean(coordinate_omega2*A*A/(N*N*k*k))
        pt_residual=clean(s.diff(phase,Pt).subs(Pt,Pt_solution))
        branches[name]=dict(phase=phase,PTF_solution=Pt_solution,p0=p0,p_linear=p1_solution,
            p_second=p2_solution,p_preservation_residual=p_residual,
            p_second_order_action_residual=action_shift_residual,PTF_EL_residual=pt_residual,
            L2=L2,K_T=kinetic,G_T=gradient,physical_speed_squared=speed)
        residuals[name+":PTF_EL"]=pt_residual
        residuals[name+":p_first"]=p1_solution
        residuals[name+":p_second_EL"]=p_residual
        residuals[name+":p_stationary_quadratic"]=action_shift_residual

    # Derive the coordinate-time equation with the time-dependent measure.
    Jgeneric=s.Symbol("J_T",positive=True)
    Arate,Nrate,Jrate,gdd=s.symbols("A_rate N_rate J_rate gammaddot",real=True)
    Lbalanced=branches["IC6"]["L2"].subs(F,(Jgeneric-1)*a02/Q**2)
    momentum=s.diff(Lbalanced,gd)
    Dtime=lambda expr:(Arate*A*s.diff(expr,A)+Nrate*N*s.diff(expr,N)
                      +Jrate*Jgeneric*s.diff(expr,Jgeneric)+gd*s.diff(expr,gamma)+gdd*s.diff(expr,gd))
    equation=clean((Dtime(momentum)-s.diff(Lbalanced,gamma))/s.diff(momentum,gd))
    damping=clean(s.diff(equation,gd))
    wave_residual=clean(equation-gdd-(3*Arate-Nrate+Jrate)*gd-N*N*k*k*gamma/A**2)
    residuals["time_dependent_measure_wave"]=wave_residual
    residuals["balanced_tensor_coefficients"]=clean(branches["IC6"]["K_T"]-branches["IC6"]["G_T"])
    residuals["balanced_physical_speed"]=clean(branches["IC6"]["physical_speed_squared"]-1)

    # Hamiltonian-only change; retains the original IC5 gradient square.
    psq=s.Symbol("PTF_squared",real=True)
    change=clean(2*psq/m*(1/JT-1))
    # Independent PTF components make first-variation tests genuine at PTF=0.
    t1,t2,t3,t4,t5=s.symbols("tf1 tf2 tf3 tf4 tf5",real=True)
    tfvars=(t1,t2,t3,t4,t5)
    tfnorm=2*(t1*t1+t2*t2+t1*t2+t3*t3+t4*t4+t5*t5)
    change_components=change.subs(psq,tfnorm)
    tfzero=dict.fromkeys(tfvars,0)
    staticjets=s.Matrix([clean(expr.subs(p,0)) for expr in
        [change_components]+[s.diff(change_components,q) for q in (p,F,m,a02)+tfvars]])
    isotropic=clean(change_components.subs(tfzero))
    isotropicjets=s.Matrix([clean(s.diff(change_components,q).subs(tfzero)) for q in (p,F)+tfvars])
    deltaF,deltap=s.symbols("delta_F delta_p",real=True)
    witness_pert=change.subs({F:eps*deltaF,p:p+eps*deltap,psq:eps**2*psq},simultaneous=True)
    secondjet=clean(s.diff(witness_pert,eps,2).subs(eps,0))
    gx,gu=s.symbols("Dxi Du",real=True)
    gradchange=s.hessian(change,(gx,gu))
    residuals.update(static_first_jets=staticjets,isotropic_Hamiltonian=isotropic,
        isotropic_first_jets=isotropicjets,witness_second_jet=secondjet,
        auxiliary_gradient_unchanged=gradchange)

    # Independent same-action homogeneous constraint surface, not arbitrary
    # off-shell F. Its isotropic restriction is unchanged by this revision.
    wave=load_wave()
    T,ell=wave["T"],wave["ell"]
    xi,u,barpi,Lam=s.symbols("xi u bar_pi Lambda",real=True)
    vol,h0,kappa=s.symbols("bar_volume h0 kappa",positive=True)
    U=lambda c:(1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    Hhom=-s.exp((4-3*u)*xi)*barpi**2/(3*m*vol)
    Hhom+=m*vol*s.exp((3*u-2)*xi)*(Lam+a02*U(u*u))-kappa*vol*s.exp((3*u-4)*xi)/2
    q=(xi,u)
    secondary=s.Matrix([s.diff(Hhom,qv) for qv in q])
    Hqq=s.hessian(Hhom,q)
    f=s.exp(-s.Rational(1,2))
    a0w=27*h0*h0*f/(8*ell**2)
    piw=-3*m*vol*f*h0
    witness={xi:s.Rational(1,4),u:s.Rational(2,3),barpi:piw,
        a02:a0w,kappa:6*m*h0*h0,Lam:6*h0*h0*f-a0w*U(s.Rational(4,9))}
    norm=m*vol*f*h0*h0
    def at_witness(expr):
        result=clean(expr.subs(witness,simultaneous=True).subs(s.log(s.Rational(5,9)),-ell))
        return clean(result.subs(1/ell,5*(T+s.Rational(27,16))/54))
    secondary0=at_witness(secondary/norm)
    hessian0=at_witness(Hqq/norm)
    sourcej=at_witness(secondary.diff(barpi)*piw/norm)
    tangent=clean(-hessian0.inv()*sourcej)
    Fselected=wave["action_coefficients"]["A_curvature"]*(xi-s.Rational(1,4))
    Fselected+=wave["action_coefficients"]["B_curvature"]*(u-s.Rational(2,3))
    Fselected=Fselected.subs(wave["target_speed_squared"],s.Rational(1,3))
    dFdj=clean((s.Matrix([s.diff(Fselected,qv) for qv in q]).T*tangent)[0])
    Jbar=1+barpi**2*s.exp(-6*(u-1)*xi)*Fselected/(m*m*vol*vol*a02)
    dJ=s.diff(Jbar,barpi)*piw+sum(s.diff(Jbar,qv)*tangent[i] for i,qv in enumerate(q))
    dJdj=at_witness(dJ)
    tangentres=clean(hessian0*tangent+sourcej)
    residuals["homogeneous_background_constraints"]=secondary0
    residuals["homogeneous_implicit_tangent"]=tangentres
    residuals["homogeneous_regular_mass_bridge"]=clean(hessian0+s.Matrix([[24,-27],[-27,2*T+s.Rational(135,8)]]))

    # Full nonlinear eta=1 plateau: five components in an orthonormal basis
    # of traceless symmetric tensors, with the trace momentum varied last.
    qfive=s.symbols("Qtf1:6",real=True)
    pfive=s.symbols("Ptf1:6",real=True)
    Rh,Cpot,Gsquare,clockX,alphap=s.symbols("Rhat C_potential gradient_square clock_X alpha",real=True)
    qnorm=sum(qi*qi for qi in qfive)
    phase5=2*sum(pi*qi for pi,qi in zip(pfive,qfive))+2*p*Q/3
    phase5-=2*sum(pi*pi for pi in pfive)/(m*JT)
    phase5+=p*p/(3*m)+m*JT*Rh/2-m*Cpot+m*alphap*Gsquare+kappa*clockX
    solved5=s.solve([s.diff(phase5,pi) for pi in pfive],pfive,dict=True)[0]
    after5=clean(phase5.subs(solved5,simultaneous=True))
    envelope=clean(s.diff(after5,p)-s.diff(phase5,p).subs(solved5,simultaneous=True))
    traceEL=s.diff(after5,p)
    psol=clean(s.solve(traceEL,p)[0])
    Y=Rh+qnorm
    K6=1+3*F*Y/(2*a02)
    L6=clean(after5.subs(p,psol))
    compact=m*(Y-2*Q*Q/(3*K6)-2*Cpot+2*alphap*Gsquare)/2+kappa*clockX
    tensorres=s.Matrix([clean(s.diff(phase5,pi).subs(solved5,simultaneous=True)) for pi in pfive])
    plateau=dict(Y=Y,K6=K6,p_solution=psol,PTF_solutions=solved5,
        after_PTF_elimination=after5,lagrangian=L6,compact_lagrangian=compact,
        tensor_EL_residuals=tensorres,envelope_residual=envelope,
        trace_EL_residual=clean(traceEL.subs(p,psol)),
        compact_lagrangian_residual=clean(L6-compact),
        domain="eta=1 plateau, J_T>0, K6!=0; algebraic phase/Lagrangian equivalence, not a full characteristic or DOF statement")
    residuals.update(plateau_tensor_EL=tensorres,plateau_envelope=envelope,
        plateau_trace_EL=plateau["trace_EL_residual"],
        plateau_compact_L=plateau["compact_lagrangian_residual"],
        plateau_trace_solution=clean(psol+m*Q/K6))

    return dict(m=m,A=A,N=N,k=k,a02=a02,eps=eps,gamma=gamma,gammadot=gd,
        coord=xyz[2],Q=Q,p=p,F=F,JT=JT,p0=p0,metric=metric,connection=connection,
        Ricci_tensor=Rij,R=R,R1=R1,R2=R2,QTF2=QTF2,determinant=determinant,
        branches=branches,A_rate=Arate,N_rate=Nrate,J_rate=Jrate,
        balanced_damping=damping,wave_equation=equation,wave_equation_residual=wave_residual,
        PTF_squared=psq,hamiltonian_change=change,static_first_jets=staticjets,
        isotropic_difference=isotropic,isotropic_first_jets=isotropicjets,
        witness_second_jet=secondjet,gradient_change_hessian=gradchange,
        T=T,ell=ell,homogeneous_H=Hhom,homogeneous_hessian=hessian0,
        homogeneous_secondary_at_witness=secondary0,homogeneous_tangent=tangent,
        homogeneous_tangent_residual=tangentres,dF_dj=dFdj,dJT_dj=dJdj,
        plateau=plateau,residuals=residuals)


def encode(value):
    if isinstance(value,dict):
        return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,s.MatrixBase):
        return encode(value.tolist())
    if isinstance(value,(tuple,list)):
        return [encode(v) for v in value]
    if isinstance(value,s.Basic):
        return str(value)
    return value


@lru_cache(None)
def numerical():
    """Re-solve the auxiliary equations using the actual new IC6 density."""
    path=HERE/"nonlinear_square_completion.py"
    if hashlib.sha256(path.read_bytes()).hexdigest()!=INPUTS[path.name]:
        raise RuntimeError("Pinned IC5 solver changed")
    spec=importlib.util.spec_from_file_location("tensor_balance_auxiliary_solver",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    d=module.derive()
    Jbar=1+s.exp(-6*d["w"])*d["trace"]**2*d["F"]/(d["m"]**2*d["vol"]**2*d["a02"])
    delta=d["kinetic_shear"]*(1/Jbar-1)
    own=derive()
    physical_change=own["hamiltonian_change"].subs({
        own["m"]:d["m"],own["a02"]:d["a02"],own["F"]:d["F"],
        own["p"]:d["trace"]*s.exp(-3*d["w"])/d["vol"],
        own["PTF_squared"]:d["shear2"]*s.exp(-6*d["w"])/d["vol"]**2},simultaneous=True)
    bridge=clean(physical_change*s.exp(d["xi"]+3*d["w"])*d["vol"]-delta)
    H6nongrad=d["Hnongrad"]+delta
    result=module.solve_auxiliary_density(d,H6nongrad)
    # Conservative rectangle estimate for the finite grid's positive-JT branch.
    # This is a floating-point check, not certified interval arithmetic or a
    # continuum existence proof. Widen reported extrema before evaluating.
    ell_value=float(s.log(s.Rational(9,5)))
    T_value=-27/16+54/(5*ell_value)
    a0_value=27*math.exp(-.5)/(8*ell_value**2)
    pi_value=-3*math.exp(-.5)
    Fxi=float(s.diff(d["F"],d["xi"]).subs({d["T"]:T_value,d["ell"]:ell_value}))
    Fu=float(s.diff(d["F"],d["u"]).subs({d["T"]:T_value,d["ell"]:ell_value}))
    for record in result["records"]:
        xs=[record["xi_range"][0]-1e-10,record["xi_range"][1]+1e-10]
        us=[record["u_range"][0]-1e-10,record["u_range"][1]+1e-10]
        maxF=max(abs(Fxi*(xx-.25)+Fu*(uu-2/3)) for xx in xs for uu in us)
        maxrho=max(pi_value*pi_value*math.exp(-6*(uu-1)*xx)/a0_value for xx in xs for uu in us)
        record["JT_lower_rectangle_estimate"]=1-maxrho*maxF
    result.update(candidate="IC6 actual modified-density auxiliary solve",
        numpy_version=module.np.__version__,
        density_bridge_residual=str(bridge),density_bridge_passed=bridge==0,
        supplied_density_sha256=hashlib.sha256(s.srepr(H6nongrad).encode()).hexdigest(),
        minimum_JT_lower_bound=min(r["JT_lower_rectangle_estimate"] for r in result["records"]),
        tensor_branch_check="Floating-point conservative rectangle estimate on the finite grid; not interval-certified continuum bounds")
    return result


@lru_cache(None)
def run(include_numeric=True):
    d=derive()
    checks={key:all(s.simplify(v)==0 for v in (list(expr) if isinstance(expr,s.MatrixBase) else [expr]))
            for key,expr in d["residuals"].items()}
    hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUTS}
    result=encode(dict(candidate="IC-6 tensor-balanced phase Hamiltonian; new revision",base=BASE,
        input_hashes_match=hashes==INPUTS,input_sha256=hashes,
        software=dict(python=platform.python_version(),sympy=s.__version__),
        exact_checks_passed=all(checks.values()),exact_checks=checks,exact_residuals=d["residuals"],
        hamiltonian_change=d["hamiltonian_change"],branches=d["branches"],
        balanced_coordinate_wave=d["wave_equation"],homogeneous_hessian=d["homogeneous_hessian"],
        nonlinear_plateau=d["plateau"],
        homogeneous_hessian_determinant=clean(d["homogeneous_hessian"].det()),
        homogeneous_constraint_tangent=d["homogeneous_tangent"],dF_dj=d["dF_dj"],dJT_dj=d["dJT_dj"],
        positive_tensor_domain="m>0, N>0, A>0, a0_squared>0 and J_T=1+p^2 F/(m^2 a0_squared)>0",
        homogeneous_existence_scope="The nonzero auxiliary Hessian and implicit tangent give a smooth nearby isotropic homogeneous constraint surface. Its regular finite-dimensional reduced Hamiltonian generates local homogeneous solutions; F is not identically zero on that surface. No full-field initial-data lift is inferred.",
        transfer_scope="Stationary first jets, isotropic flat homogeneous restriction, and the IC4 witness quadratic jet are unchanged. Generic Bianchi I and nonzero-shear auxiliary mass are not unchanged. The auxiliary spatial-gradient square is unchanged at fixed momenta.",
        full_all_background_causality_proved=False,
        scope="Actual linear TT characteristics on general flat homogeneous isotropic backgrounds of the new action, positive J_T branch. Time-dependent coefficients and physical metric normalization retained. No anisotropic/inhomogeneous characteristic or full nonlinear closure theorem."))
    if include_numeric:
        result["numerical"]=numerical()
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-all-background-causality",action="store_true")
    parser.add_argument("--symbolic-only",action="store_true")
    args=parser.parse_args(argv)
    result=run(not args.symbolic_only)
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["input_hashes_match"] or not result["exact_checks_passed"]:
        return 1
    if not args.symbolic_only and (not result["numerical"]["all_converged"]
        or not result["numerical"]["density_bridge_passed"]
        or result["numerical"]["minimum_JT_lower_bound"]<=0):
        return 1
    return 2 if args.require_all_background_causality else 0


if __name__ == "__main__":
    raise SystemExit(main())
