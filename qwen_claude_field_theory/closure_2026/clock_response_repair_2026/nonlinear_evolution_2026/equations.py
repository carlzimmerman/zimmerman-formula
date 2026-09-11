#!/usr/bin/env python3
"""Full-gradient spherical time equations and preserved clock constraint.

Every reduction starts with the already varied, unfixed covariant action.
Shift=0 is a coordinate choice; A,R,chi_r and Q remain arbitrary functions.
This is not a Dirac constraint classification or a health certificate.
"""
import contextlib
from functools import lru_cache
import importlib.util
import io
import json
from pathlib import Path
import time

import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def derive():
    started = time.monotonic()
    path = HERE.parent/"spherical_baryon_bridge/action/derive.py"
    spec = importlib.util.spec_from_file_location("unfixed_clock_action",path)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    k,h,Q,kr,hr,Qr,Qrr,kd,hd,Qd = s.symbols("k h Q kr hr Qr Qrr kd hd Qd",real=True)
    rho,w = s.symbols("rho w",real=True)
    eta=s.symbols("constraint_addition",real=True)
    Ptt,Vtt,WYYY,WYYt = s.symbols("P_tt V_tt W_YYY W_YYt",real=True)
    N,A,R,u,ur = m.N,m.A,m.R,m.u,m.ur
    Nr,Nrr,Ar,Rr,Rrr = m.Nr,m.jets["N",0,2],m.Ar,m.Rr,m.jets["R",0,2]
    M,g = m.M2,m.gamma
    substitutions = {
        m.At:N*A*k,m.Rt:N*R*h,m.ct:N*Q,
        m.jets["A",2,0]:A*(N*kd+m.Nt*k+N*N*k*k),
        m.jets["R",2,0]:R*(N*hd+m.Nt*h+N*N*h*h),
        m.jets["c",2,0]:m.Nt*Q+N*Qd,
        m.jets["A",1,1]:Nr*A*k+N*Ar*k+N*A*kr,
        m.jets["R",1,1]:Nr*R*h+N*Rr*h+N*R*hr,
        m.jets["c",1,1]:Nr*Q+N*Qr,
        m.jets["c",1,2]:Nrr*Q+2*Nr*Qr+N*Qrr,
    }
    substitutions.update({z:0 for (name,i,j),z in m.jets.items() if name=="v"})

    def pull(expr):
        return s.cancel(expr.subs(substitutions,simultaneous=True))

    checks = {}
    def check(name,expr):
        checks[name] = s.cancel(s.expand(expr))==0
        if not checks[name]:
            raise AssertionError(name+": "+str(s.factor(expr)))

    Jsp = m.dr(R**2*m.WY*u/A)/(A*R**2)
    T = m.Vt-m.Pt+m.W*(m.k+2*m.h)-2*m.WY*m.k*m.Y-2*m.Q*Jsp
    Tt = m.dt(T)+s.diff(T,m.Pt)*(Ptt+m.PXt*m.dt(m.X))+s.diff(T,m.Vt)*Vtt
    Tt += s.diff(T,m.WYY)*(WYYY*m.dt(m.Y)+WYYt)
    # Normal dust velocity sqrt(1+w²/A²); spatial radial stress rho*w²/A².
    equations = s.Matrix([pull(m.E["A"])/R**2+N*rho*w*w/A**2,
                           pull(m.E["R"])/(A*R),
                           -pull(m.E["c"])/(A*R**2),pull(Tt)])
    for i,equation in enumerate(equations):
        check("no_lapse_time_derivative_%d"%i,s.diff(equation,m.Nt))
    # Retain Hamiltonian, momentum, and clock constraints as independent monitors.
    ham = pull(m.E["N"])/(A*R**2)-rho*(1+w*w/A**2)
    mom = pull(m.E["v"])/(A*R**2)-rho*s.sqrt(1+w*w/A**2)*w
    tau = pull(T)
    # Standard spatial Ricci evolution (eta=1) versus raw Einstein spatial
    # evolution (eta=0). These have identical physical solutions when ham=0;
    # the addition is a numerical constraint-propagation choice, not a new action.
    evolution_equations=equations+s.Matrix([eta*N*ham,2*eta*N*ham,0,0])
    full,rhs = s.linear_eq_to_matrix(evolution_equations,[kd,hd,Qd,Nrr,Nr,N])
    for i,residual in enumerate(full*s.Matrix([kd,hd,Qd,Nrr,Nr,N])-rhs-evolution_equations):
        check("linear_evolution_lapse_reconstruction_%d"%i,residual)
    matrix = full[:,:4]
    forcing = (-full[:,4]).row_join(-full[:,5]).row_join(rhs)
    # Exact action Noether identities (before imposing matter equations).
    radial=m.Nr*m.E["N"]+m.Ar*m.E["A"]+m.Rr*m.E["R"]+m.u*m.E["c"]
    radial+=m.vr*m.E["v"]-m.dr(A*m.E["A"]-m.v*m.E["v"])-m.dt(m.E["v"])
    check("radial_noether_identity",pull(radial))
    temporal=-N*m.dt(m.E["N"])+m.At*m.E["A"]+m.Rt*m.E["R"]+m.ct*m.E["c"]
    temporal+=-N*A*R**2*T+m.dr(N*N*m.E["v"]/A**2)
    check("time_noether_identity_shift_zero",pull(temporal))

    H,q = s.symbols("H q",real=True)
    initial = {R:m.r,Rr:1,Rrr:0,k:H,h:H,Q:q,kr:0,hr:0,Qr:0,Qrr:0,u:0,ur:0,w:0}
    lap = (Nrr+(2/m.r-Ar/A)*Nr)/A**2
    check("initial_tau_preservation",equations[3].subs(initial)
          -(Vtt-Ptt+3*H*m.Wt+m.W*(kd+2*hd)-2*q*m.PXt*Qd-2*q*q*m.WY*lap))
    J = 2*q*m.PX-6*g*H*q*q
    check("initial_scalar_current",equations[2].subs(initial)
          -((2*m.PX+4*q*q*m.PXX-12*g*H*q)*Qd-2*g*q*q*(kd+2*hd)
            +3*N*H*J+2*q*m.PXt+2*g*q*q*lap))
    check("initial_clock_constraint",tau.subs(initial)-(m.Vt-m.Pt+3*H*m.W))
    check("initial_momentum",mom.subs(initial))
    # Gamma=0 control: no cubic braiding survives in the scalar momentum.
    check("gamma_zero_scalar_momentum",pull(m.p).subs(g,0)-2*A*R**2*Q*m.PX)
    symbols = {str(z):z for z in set().union(*(e.free_symbols for e in
                      list(matrix)+list(forcing)+[ham,mom,tau]))}
    symbols.update(u=u,ur=ur,Qr=Qr)
    return dict(matrix=matrix,forcing=forcing,constraints=s.Matrix([ham,mom,tau]),
                symbols=symbols,checks=checks,equations=equations,evolution_equations=evolution_equations,
                inherited_check_count=len(m.checks),seconds=time.monotonic()-started)


@lru_cache(maxsize=1)
def compiled():
    data = derive()
    expressions = list(data["matrix"])+list(data["forcing"])+list(data["constraints"])
    args = sorted(set().union(*(e.free_symbols for e in expressions)),key=str)
    return [str(z) for z in args],s.lambdify(args,expressions,"numpy",cse=True)


def evaluate(values):
    names,func = compiled()
    inputs = [np.asarray(values[name]) for name in names]
    shape = np.broadcast_shapes(*(a.shape for a in inputs))
    raw = func(*inputs)
    flat = np.stack([np.broadcast_to(x,shape) for x in raw],axis=-1)
    return (flat[...,:16].reshape(shape+(4,4)),
            flat[...,16:28].reshape(shape+(4,3)),flat[...,28:31])


@lru_cache(maxsize=1)
def compiled_constraints():
    data=derive();eqs=data["constraints"]
    variables=[data["symbols"][name] for name in ("Ar","hr","k")]
    matrix,rhs=s.linear_eq_to_matrix(eqs,variables)
    expressions=list(matrix)+list(rhs)
    args=sorted(set().union(*(e.free_symbols for e in expressions)),key=str)
    return [str(z) for z in args],s.lambdify(args,expressions,"numpy",cse=True)


def constraint_rates(values):
    names,func=compiled_constraints()
    output=np.asarray(func(*(values[n] for n in names)),dtype=float)
    return np.linalg.solve(output[:9].reshape(3,3),output[9:])


if __name__ == "__main__":
    data = derive()
    print(json.dumps(dict(status="formal_full_gradient_reduction_passed",
        checks=data["checks"],inherited_checks=data["inherited_check_count"],
        matrix_shape=list(data["matrix"].shape),
        free_inputs=compiled()[0],seconds=data["seconds"],
        non_claims=["not a validated finite-time evolution", "not a Dirac or stability certificate"]),indent=2))
