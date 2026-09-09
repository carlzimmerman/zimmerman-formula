#!/usr/bin/env python3
"""Explicit IC11 isotropic tensor/auxiliary repair and scalar UV screen.

This changes the full action, preserves its flat homogeneous restriction,
and does not assert global constraint closure or physical phenomenology.
"""
import argparse
import json
import mpmath as mp
import sympy as s
import ic10_transition as original


def symbolic_identities():
    E,J,rho,eta,eta_r,eta_rr,c,Z = s.symbols("E J rho eta eta_r eta_rr c Z", nonzero=True)
    A = 1+eta*(1/J-1)
    C = 1+eta*(J-1)+(1-eta)*Z
    # r=c*rho, c=-E/3; q held fixed for both rho derivatives.
    r0 = s.Symbol("r0")
    # An arbitrary two-jet is exact for this second derivative at r=r0.
    eta_jet = eta+eta_r*(c*rho-r0)+eta_rr*(c*rho-r0)**2/2
    raw = -E*rho*rho*(1+(1/J-1)*eta_jet)/3
    derivative = s.diff(raw,rho,2).subs(r0,c*rho)
    uv = E*A/6+derivative/4
    identity = -E*(1/J-1)*(4*c*rho*eta_r+c*c*rho*rho*eta_rr)/12
    return dict(tensor=s.simplify(A*(C+(1/A-C))-1),
                plateau_curvature=s.simplify((1/A-C).subs(eta,1)),
                static_curvature=s.simplify((1/A-C).subs({eta:0,Z:0})),
                scalar_uv=s.simplify(uv-identity))


def correction_density(point, Rbar, dx, du):
    """N sqrt(h) delta H/V, using barred gradient/curvature arguments."""
    rho,xi,u = point
    E = mp.exp((4-3*u)*xi)
    J = mp.exp(-2*(u-1)*xi-mp.mpf(1)/6)
    # raw expressions are analytic in q for derivative checks.
    values = original.build()["evaluate"](rho,xi,u)
    Z = values[41]
    eta = original.activation_value(-rho*E/3)
    A,C = 1+eta*(1/J-1),1+eta*(J-1)+(1-eta)*Z
    W = original.spatial_gradient(point)["W"]
    f = 1+sum(W[i,j]**2 for i in range(2) for j in range(2))
    complement = original.activation_complement(-rho*E/3)
    return -mp.exp(u*xi)*((1/A-C)*Rbar/2+eta*complement*f*(dx*dx+du*du))


def at_background(bg):
    rho,xi,u = bg["point"]
    eta = bg["eta"]
    W = original.spatial_gradient(bg["point"])["W"]
    f = 1+sum(W[i,j]**2 for i in range(2) for j in range(2))
    fixedW = W+eta*f*mp.eye(2)
    G = -2*original.activation_complement(bg["r"])*mp.exp(u*xi)*fixedW
    ultraviolet = bg["E"]*bg["A"]/6+bg["hessian"][0,0]/4
    identity = -bg["E"]*(1/bg["J"]-1)*(4*bg["r"]*bg["eta1"]+bg["r"]**2*bg["eta2"])/12
    return dict(W=fixedW,G=G,tensor_speed_squared=bg["A"]*(1/bg["A"]),
                positive_auxiliary_poles=original.positive_pencil_roots(bg["auxiliary"],G),
                scalar_UV_kinetic=ultraviolet,scalar_UV_switch_identity=identity)


def report():
    mp.mp.dps = 60
    rows = []
    for bg in original.continuation():
        fixed = at_background(bg)
        rows.append(dict(step=bg["step"],point=[mp.nstr(v,24) for v in bg["point"]],
                         eta=mp.nstr(bg["eta"],24),
                         tensor_speed_squared=mp.nstr(fixed["tensor_speed_squared"],24),
                         minimum_W_eigenvalue=mp.nstr(min(mp.eigsy(fixed["W"],eigvals_only=True)),24),
                         scalar_UV_kinetic=mp.nstr(fixed["scalar_UV_kinetic"],24),
                         scalar_UV_identity_residual=mp.nstr(abs(fixed["scalar_UV_kinetic"]-fixed["scalar_UV_switch_identity"]),8),
                         positive_auxiliary_k_squared_poles=[mp.nstr(v,24) for v in fixed["positive_auxiliary_poles"]],
                         constraint_residual=mp.nstr(mp.norm(bg["gradient"][1:3,:]),8)))
    return dict(candidate="IC11 explicit curvature and auxiliary-gradient correction",full_theory="OPEN",
                symbolic_identities={key:str(value) for key,value in symbolic_identities().items()},
                arithmetic="mpmath 60 decimal digits; numerical samples, no interval certification",
                continuation=rows,
                nonclaims=["No global no-go or full Dirac DOF count",
                           "Isotropic tensor repair is not an all-background characteristic theorem",
                           "Negative scalar UV kinetic rejects this trial as a stable completion"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure",action="store_true")
    args = parser.parse_args()
    print(json.dumps(report(),indent=2))
    raise SystemExit(2 if args.require_full_closure else 0)
