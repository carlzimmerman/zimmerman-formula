#!/usr/bin/env python3
"""Full IC10 homogeneous transition and isotropic tensor cone, m=h0=1.

No eta=1 pressure is extrapolated: differentiate h=h0+eta(r)*delta_h,
including both switch jets. This is not yet the full scalar characteristic
or distribution-valued field Dirac analysis.
"""
from functools import lru_cache
import argparse
import json
import sympy as s
import mpmath as mp
import ic8_shear_integrability as ingredients
import ic10_local_clock as plateau


@lru_cache(None)
def build():
    old = ingredients.build()
    rho, xi, u = variables = old["rho"], old["xi"], old["u"]
    E, w = s.exp((4-3*u)*xi), (u-1)*xi
    J = s.exp(-2*w-s.Rational(1, 6))
    base = old["htrace"]
    delta = -E*rho*rho*(1/J-1)/3
    r = -rho*E/3
    ell, T = s.log(s.Rational(9, 5)), old["T"]
    a02 = 27*s.exp(-s.Rational(1, 2))/(8*ell*ell)
    pR = s.Rational(8, 3)+4*(3-81/(4*T))/3
    qR = -1-3*pR/8
    F = 3*(pR*(xi-s.Rational(1, 4))+qR*(u-s.Rational(2, 3)))/(16*ell*ell)
    Z = s.exp(-6*w)*rho*rho*F/a02
    data = []
    for expression in (base, delta, r):
        data.extend([expression]+[s.diff(expression, x) for x in variables]+list(s.hessian(expression, variables)))
    evaluate = s.lambdify(variables, s.Matrix(data+[E,J,Z]), "mpmath", cse=True)
    raw = s.lambdify(variables, (base, delta, r), "mpmath", cse=True)
    return dict(variables=variables, base=base, delta=delta, r=r, E=E, J=J, Z=Z,
                evaluate=evaluate, raw=raw)


def activation_value(r):
    d = (r*r-1)**2
    if d <= mp.mpf(1)/16:
        return mp.mpf(1)
    if d >= mp.mpf(1)/4:
        return mp.mpf(0)
    a = mp.exp(-1/(mp.mpf(1)/4-d))
    b = mp.exp(-1/(d-mp.mpf(1)/16))
    return a/(a+b)


def activation(r):
    d = (r*r-1)**2
    if d <= mp.mpf(1)/16:
        return mp.mpf(1), mp.mpf(0), mp.mpf(0)
    if d >= mp.mpf(1)/4:
        return mp.mpf(0), mp.mpf(0), mp.mpf(0)
    left, right = mp.mpf(1)/4-d, d-mp.mpf(1)/16
    L = 1/left-1/right
    dd, ddd = 4*r*(r*r-1), 12*r*r-4
    L1 = (1/left**2+1/right**2)*dd
    L2 = (2/left**3-2/right**3)*dd**2+(1/left**2+1/right**2)*ddd
    tiny = mp.exp(-abs(L))
    value = tiny/(1+tiny) if L > 0 else 1/(1+tiny)
    product = tiny/(1+tiny)**2
    return value, -product*L1, product*((1-2*value)*L1*L1-L2)


def activation_complement(r):
    """Compute 1-eta without cancellation close to the eta=1 boundary."""
    d = (r*r-1)**2
    if d <= mp.mpf(1)/16:
        return mp.mpf(0)
    if d >= mp.mpf(1)/4:
        return mp.mpf(1)
    L = 1/(mp.mpf(1)/4-d)-1/(d-mp.mpf(1)/16)
    tiny = mp.exp(-abs(L))
    return 1/(1+tiny) if L > 0 else tiny/(1+tiny)


def raw_density(rho, xi, u):
    base, delta, r = build()["raw"](rho, xi, u)
    return base+activation_value(r)*delta


def at_point(point):
    rho, xi, u = map(mp.mpf, point)
    data = build()["evaluate"](rho, xi, u)
    pieces = []
    for offset in (0, 13, 26):
        pieces.append((data[offset], mp.matrix(data[offset+1:offset+4]),
                       mp.matrix([[data[offset+4+3*i+j] for j in range(3)] for i in range(3)])))
    (h0,g0,H0),(delta,gd,Hd),(r,gr,Hr) = pieces
    eta, eta1, eta2 = activation(r)
    h = h0+eta*delta
    gradient = g0+eta*gd+eta1*delta*gr
    Hessian = H0+eta*Hd+eta1*(gr*gd.T+gd*gr.T+delta*Hr)+eta2*delta*gr*gr.T
    E, J, Z = data[39:42]
    kinetic_factor = 1+eta*(1/J-1)
    curvature_factor = 1+eta*(J-1)+(1-eta)*Z
    M = Hessian[1:3, 1:3]
    rhodot, logVdot = -mp.mpf(3)*h/2, mp.mpf(3)*gradient[0]/2
    qdot = -(M**-1)*(Hessian[1:3, 0]*rhodot+logVdot*gradient[1:3, :])
    wdot = (u-1)*qdot[0]+xi*qdot[1]
    physical_H = mp.exp(-xi)*(gradient[0]/2+wdot)
    Dirac = mp.matrix(4, 4)
    Dirac[:2, 2:4], Dirac[2:4, :2] = -M, M
    omega = mp.mpf(3)/2*(gradient[1]*Hessian[0,2]-Hessian[0,1]*gradient[2])
    Dirac[2, 3], Dirac[3, 2] = omega, -omega
    preservation = logVdot*gradient[1:3, :]+Hessian[1:3, 0]*rhodot+M*qdot
    return dict(point=[rho,xi,u], h=h, gradient=gradient, hessian=Hessian, eta=eta, eta1=eta1,
                E=E, A=kinetic_factor, C=curvature_factor,
                eta2=eta2, r=r, J=J, Z=Z, auxiliary=M, dirac_matrix=Dirac, qdot=qdot,
                rhodot=rhodot, logVdot=logVdot, physical_H=physical_H,
                tensor_speed_squared=kinetic_factor*curvature_factor,
                tensor_kinetic_coefficient=2*E*kinetic_factor,
                preservation_residual=preservation,
                energy_preservation=logVdot*h+gradient[0]*rhodot+(gradient[1:3, :].T*qdot)[0])


def solve_rho(rho, seed):
    equations = lambda xi,u: tuple(at_point([rho,xi,u])["gradient"][1:3, :])
    jacobian = lambda xi,u: at_point([rho,xi,u])["auxiliary"]
    xi,u = mp.findroot(equations, tuple(seed), J=jacobian, tol=mp.power(10,-mp.mp.dps+10))
    if not 0 < u < 1:
        raise ValueError("Constraint solve left 0<u<1")
    return at_point([rho,xi,u])


def spatial_gradient(point):
    """Full IC5/IC10 gradient block, barred unit-volume convention, m=1."""
    rho, xi, u = map(mp.mpf, point)
    ell = mp.log(mp.mpf(9)/5)
    T = -mp.mpf(27)/16+54/(5*ell)
    alpha, d = 81/(8*T*T), -9/(8*T)
    beta = 2*d-mp.mpf(1)/3-3*alpha/4
    gamma = mp.mpf(1)/16+9*alpha/64-3*d/4
    a02 = 27*mp.exp(-mp.mpf(1)/2)/(8*ell*ell)
    p = mp.exp(-3*(u-1)*xi)*rho
    W = (mp.matrix([[0,u*xi],[u*xi,xi*xi]])
         +3*p*p/(8*a02*ell*ell)*mp.matrix([[alpha,beta/2],[beta/2,gamma]]))
    complement = activation_complement(-rho*mp.exp((4-3*u)*xi)/3)
    return dict(W=W,G=-2*complement*mp.exp(u*xi)*W)


def raw_spatial_density(point, dx, du):
    """Independent uncollected H5 spatial density after IC10 cancellation."""
    rho, xi, u = point
    ell = mp.log(mp.mpf(9)/5)
    T = -mp.mpf(27)/16+54/(5*ell)
    alpha, d = 81/(8*T*T), -9/(8*T)
    beta, gamma = 2*d-mp.mpf(1)/3-3*alpha/4, mp.mpf(1)/16+9*alpha/64-3*d/4
    a02 = 27*mp.exp(-mp.mpf(1)/2)/(8*ell*ell)
    Jbar = 3*(alpha*dx*dx+beta*dx*du+gamma*du*du)/(4*ell*ell)
    D = -mp.exp((6-5*u)*xi)*rho*rho/(2*a02)
    complement = activation_complement(-rho*mp.exp((4-3*u)*xi)/3)
    return complement*(-mp.exp(u*xi)*(2*u*xi*dx*du+xi*xi*du*du)+D*Jbar)


def positive_pencil_roots(M, G):
    """All positive real roots x=k^2 of a symmetric 2x2 pencil determinant."""
    c0 = mp.det(M)
    c1 = M[0,0]*G[1,1]+M[1,1]*G[0,0]-M[0,1]*G[1,0]-M[1,0]*G[0,1]
    c2 = mp.det(G)
    if c2 == 0:
        return [-c0/c1] if c1 != 0 and -c0/c1 > 0 else []
    disc = c1*c1-4*c2*c0
    if disc < 0:
        return []
    root = mp.sqrt(disc)
    q = -(c1+mp.sign(c1)*root)/2 if c1 else -root/2
    roots = [q/c2,c0/q] if q else [mp.mpf(0)]
    return sorted(set(x for x in roots if x > 0))


def auxiliary_poles(bg):
    return positive_pencil_roots(bg["auxiliary"],spatial_gradient(bg["point"])["G"])


def continuation(last_step=500):
    """Actual h_q=0 roots on rho=rho0+n*.001, 0<=n<=last_step."""
    start = plateau.state(mp.mpf("0.2"))
    rho = -3*mp.exp(-mp.mpf(1)/6)*start["H"]
    seed = [mp.mpf("0.2")+start["w"],start["u"]]
    for step in range(last_step+1):
        bg = solve_rho(rho+mp.mpf(step)/1000, seed)
        seed = bg["point"][1:3]
        bg["step"] = step
        yield bg


def report():
    mp.mp.dps = 60
    rows = []
    for bg in continuation():
        spatial = spatial_gradient(bg["point"])
        rows.append({key:mp.nstr(bg[key],24) for key in
                     ("r","eta","physical_H","tensor_speed_squared","h","rhodot")}
                    | {"step":bg["step"],"rho":mp.nstr(bg["point"][0],24),
                       "xi":mp.nstr(bg["point"][1],24),"u":mp.nstr(bg["point"][2],24),
                       "W_eigenvalues":[mp.nstr(x,24) for x in mp.eigsy(spatial["W"],eigvals_only=True)],
                       "auxiliary_eigenvalues":[mp.nstr(x,24) for x in mp.eigsy(bg["auxiliary"],eigvals_only=True)],
                       "positive_auxiliary_k_squared_poles":[mp.nstr(x,24) for x in auxiliary_poles(bg)],
                       "auxiliary_determinant":mp.nstr(mp.det(bg["auxiliary"]),24),
                       "constraint_residual":mp.nstr(mp.norm(bg["gradient"][1:3,:]),8)})
    return dict(candidate="IC10 unchanged full phase action",full_theory="OPEN",continuation=rows,
                nonclaims=["No complete scalar/vector characteristic matrix or all-background causality",
                           "No field-theory DOF count from a homogeneous constraint matrix"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args()
    print(json.dumps(report(),indent=2))
    raise SystemExit(2 if args.require_full_closure else 0)
