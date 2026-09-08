#!/usr/bin/env python3
"""Full IC4 gravity/clock Hamiltonian identities and local auxiliary jets.

These are exact nonlinear identities on the regular metric Legendre branch.
They do not certify invertibility of a spatial differential operator, full
functional closure, matter completion, or nonlinear stability/causality.
"""
import argparse
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

import sympy as s

BASE = "6708f1e3e695a99f3fc3f121e14528f68ace641c"
SOURCE = Path(__file__).with_name("IC4_ACTION.md")
SOURCE_HASH = "cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8"
PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
WEIGHTS = (1, 1, 1, 2, 2, 2)


def symmetric(entries):
    out = s.zeros(3)
    for (i, j), value in zip(PAIRS, entries):
        out[i, j] = out[j, i] = value
    return out


def zero_matrix(matrix):
    return all(s.cancel(s.expand(v)) == 0 for v in matrix)


def potential(u):
    c = u*u
    return (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2


@lru_cache(None)
def derive_point_transform():
    xi, u, xid, ud, advw = s.symbols("xi u xidot udot shift_dot_grad_w", real=True)
    g = symmetric(s.symbols("g11 g22 g33 g12 g13 g23", real=True))
    gd = symmetric(s.symbols("v11 v22 v33 v12 v13 v23", real=True))
    lie = symmetric(s.symbols("l11 l22 l33 l12 l13 l23", real=True))
    w, N = (u-1)*xi, s.exp(xi)
    wd = s.diff(w,xi)*xid+s.diff(w,u)*ud
    physical_metric = s.exp(2*w)*g
    physical_dot = s.exp(2*w)*(gd+2*wd*g)
    physical_lie = s.exp(2*w)*(lie+2*advw*g)
    K = (physical_dot-physical_lie)/(2*N)
    W = (wd-advw)/N
    Q = K-physical_metric*W
    target = s.exp(2*w)*(gd-lie)/(2*N)
    # The original physical canonical one-form fixes the sign of the new
    # auxiliary momenta, including both contributions to dw.
    pi = symmetric(s.symbols("pi11 pi22 pi33 pi12 pi13 pi23", real=True))
    dg = symmetric(s.symbols("dg11 dg22 dg33 dg12 dg13 dg23", real=True))
    dx, du, px, pu = s.symbols("dx du p_xi_physical p_u_physical", real=True)
    trace = s.trace(physical_metric*pi)
    original = sum(pi[i,j]*s.exp(2*w)*(dg[i,j]+2*g[i,j]*((u-1)*dx+xi*du))
                   for i in range(3) for j in range(3))+px*dx+pu*du
    transformed = sum(s.exp(2*w)*pi[i,j]*dg[i,j] for i in range(3) for j in range(3))
    transformed += (px+2*(u-1)*trace)*dx+(pu+2*xi*trace)*du
    wrong_Q = K-physical_metric*((u-1)*xid-advw)/N
    return dict(residuals={"actual_Q_pullback":0 if zero_matrix(Q-target) else 1,
        "no_xidot":0 if zero_matrix(Q.diff(xid)) else 1,
        "no_udot":0 if zero_matrix(Q.diff(ud)) else 1,
        "actual_symplectic_one_form":s.expand(original-transformed)},
        omit_auxiliary_velocity_mutation=(wrong_Q-target).applyfunc(s.simplify),
        momenta="barpi^ij=exp(2w)*pi_physical^ij; p_xi_bar=p_xi_physical+2(u-1)*pi_trace; p_u_bar=p_u_physical+2xi*pi_trace. Barred p_xi=p_u=0.",
        scope="Point transformation on timelike-clock unitary slices; Einstein-Hilbert ADM boundary term treated separately")


@lru_cache(None)
def derive_legendre():
    C = s.Symbol("C", positive=True)
    t = s.Symbol("t", nonzero=True, real=True)
    gij = s.symbols("g11 g22 g33 g12 g13 g23", real=True)
    velocities = s.symbols("gdot11 gdot22 gdot33 gdot12 gdot13 gdot23", real=True)
    momenta = s.symbols("p11 p22 p33 p12 p13 p23", real=True)
    g = symmetric(gij)
    inv = g.inv()
    V = symmetric(velocities)/2
    trace = s.trace(inv*V)
    L = C*(s.trace(inv*V*inv*V)+(t-s.Rational(1, 3))*trace**2)
    p = s.Matrix([s.diff(L, v) for v in velocities])
    tensor_momentum = C*(inv*V*inv+(t-s.Rational(1, 3))*trace*inv)
    expected = s.Matrix([weight*tensor_momentum[i, j]
                         for (i, j), weight in zip(PAIRS, WEIGHTS)])
    Pi = symmetric([p/weight for p, weight in zip(momenta, WEIGHTS)])
    pi = s.trace(g*Pi)
    PiTF = Pi-pi*inv/3
    # This candidate is tested against the differentiated six-component map.
    Vinverse = (g*PiTF*g+pi*g/(9*t))/C
    inverse_velocity = {v:2*Vinverse[i, j] for v, (i, j) in zip(velocities, PAIRS)}
    inversion = p.subs(inverse_velocity, simultaneous=True)-s.Matrix(momenta)
    H = (s.trace(g*PiTF*g*PiTF)+pi*pi/(9*t))/C
    # Euler homogeneity avoids expanding a large substituted quadratic form:
    # with p=dL/dgdot and inversion verified, p.gdot-L=p.gdot/2.
    contraction = sum(pv*inverse_velocity[v]/2 for pv, v in zip(momenta, velocities))
    orth = {gij[0]:1, gij[1]:1, gij[2]:1, gij[3]:0, gij[4]:0, gij[5]:0}
    hessian = s.hessian(L.subs(orth), velocities)
    residuals = {
        "actual_component_momenta": 0 if zero_matrix(p-expected) else 1,
        "general_metric_legendre_inverse": 0 if zero_matrix(inversion) else 1,
        "euler_quadratic_identity": s.cancel(sum(p[i]*velocities[i] for i in range(6))-2*L),
        "actual_hamiltonian": s.cancel(contraction-H),
        "orthonormal_determinant": s.factor(hessian.det()-3*C**6*t/8),
    }
    return dict(C=C, t=t, component_weights=WEIGHTS,
        metric=g, tensor_momentum=tensor_momentum, inverse_velocity=Vinverse,
        hamiltonian=H, orthonormal_hessian=hessian, residuals=residuals,
        general_hessian_determinant="3*C^6*t/(8*det(barh)^4); Sym^2 congruence from the checked orthonormal Hessian",
        domain="positive definite barh, C>0, t!=0; t=0 is not eliminated")


@lru_cache(None)
def derive_spatial():
    xi, u = s.symbols("xi u", real=True)
    aa, ab, bb, lap_xi, lap_u = s.symbols("aa ab bb lap_xi lap_u", real=True)
    dw2 = (u-1)**2*aa+2*(u-1)*xi*ab+xi**2*bb
    lap_w = (u-1)*lap_xi+xi*lap_u+2*ab
    grad_log_weight_dot_dw = u*(u-1)*aa+xi*(2*u-1)*ab+xi**2*bb
    raw = -4*lap_w-2*dw2+2*(1-u*u)*aa
    divergence = 4*(lap_w+grad_log_weight_dot_dw)
    after = s.expand(raw+divergence)
    # Explicit connection calculation at a point for h=e^(2w)*delta.
    a = s.symbols("w1:4", real=True)
    hess = symmetric(s.symbols("w11 w22 w33 w12 w13 w23", real=True))
    delta = s.eye(3)
    connection = [[[delta[k, i]*a[j]+delta[k, j]*a[i]-delta[i, j]*a[k]
                    for j in range(3)] for i in range(3)] for k in range(3)]
    def dg(k, i, j, r):
        return delta[k, i]*hess[j, r]+delta[k, j]*hess[i, r]-delta[i, j]*hess[k, r]
    ricci = s.Matrix(3, 3, lambda i, j: sum(
        dg(k, i, j, k)-dg(k, i, k, j)
        +sum(connection[k][k][l]*connection[l][i][j]
             -connection[k][j][l]*connection[l][i][k] for l in range(3))
        for k in range(3)))
    curvature_residual = s.expand(s.trace(ricci)+4*s.trace(hess)+2*sum(v*v for v in a))
    omitted = s.expand(-2*(u-1)**2*aa+2*(1-u*u)*aa+4*u*(u-1)*aa
                       +4*xi*(u-1)*ab-after)
    return dict(xi=xi, u=u, raw_spatial_gradient=raw,
        boundary_divergence_over_weight=divergence,
        gradient_coefficients=tuple(after.coeff(j) for j in (aa, ab, bb)),
        omit_xi_du_mutation=omitted,
        residuals={"conformal_connection_scalar":curvature_residual,
                   "spatial_ibp":s.expand(after-4*u*xi*ab-2*xi*xi*bb)},
        boundary="L_before=L_after-4*sqrt(barh)*D_i(A*D^i w), A=(m/2)*exp(u*xi); fix/vanish this boundary flux")


@lru_cache(None)
def derive_density():
    xi, u, R = s.symbols("xi u Rbar", real=True)
    m, a0, kap = s.symbols("m a0 kappa", positive=True)
    Lam, alpha, beta, gamma, AR, BR = s.symbols("Lambda alpha beta gamma A_R B_R", real=True)
    ell = s.Symbol("ell", positive=True)
    STF, P2, t = s.symbols("P_TF_squared P_trace_squared t", real=True)
    aa, ab, bb = s.symbols("aa ab bb", real=True)
    a, b = s.symbols("xi1:4", real=True), s.symbols("u1:4", real=True)
    w = (u-1)*xi
    j0 = 3/(4*ell**2)
    f = AR*(xi-s.Rational(1, 4))+BR*(u-s.Rational(2, 3))
    j = j0*(alpha*aa+beta*ab+gamma*bb)
    theta = -s.Rational(2, 3)+s.exp(-2*w)*(j+f*R)/a0**2
    prefactor = 2*s.exp((4-3*u)*xi)/m
    kinetic = prefactor*(STF+P2/(9*t))
    spatial = -m*s.exp(u*xi)*(R+4*u*xi*ab+2*xi*xi*bb)/2
    vacuum = m*s.exp((3*u-2)*xi)*(Lam+a0*a0*potential(u))
    clock = -kap*s.exp((3*u-4)*xi)/2
    scalar = kinetic+spatial+vacuum+clock
    jets = {aa:sum(v*v for v in a), ab:sum(v*w for v, w in zip(a, b)), bb:sum(v*v for v in b)}
    Tcal = -s.Rational(27, 16)+54/(5*ell)
    e = s.Rational(1, 8)
    d = -9*e/Tcal
    a_star = 3-81/(4*Tcal)
    sigma = s.Rational(1, 3)
    pR = s.Rational(8, 3)+4*a_star*sigma
    qR = -1-3*pR/8
    coefficient_dictionary = {alpha:81*e/Tcal**2,
        beta:2*d-s.Rational(1, 3)-3*(81*e/Tcal**2)/4,
        gamma:e-s.Rational(1, 16)+9*(81*e/Tcal**2)/64-3*d/4,
        AR:3*pR/(16*ell**2), BR:3*qR/(16*ell**2), ell:s.log(s.Rational(9, 5))}
    return dict(xi=xi, u=u, R=R, m=m, a0=a0, kappa=kap, Lambda=Lam,
        alpha=alpha, beta=beta, gamma=gamma, AR=AR, BR=BR, ell=ell,
        STF=STF, P2=P2, t=t, aa=aa, ab=ab, bb=bb, a=a, b=b,
        prefactor=prefactor, t_definition=theta, t_jets=theta.subs(jets),
        gradient_invariants=jets, scalar=scalar, scalar_jets=scalar.subs(jets),
        spatial=spatial, kinetic=kinetic, vacuum=vacuum, clock=clock,
        coefficient_dictionary=coefficient_dictionary,
        residuals={"kinetic_measure":s.simplify(s.exp(3*w-xi)-s.exp((3*u-4)*xi)),
            "spatial_measure":s.simplify(s.exp(xi+w)-s.exp(u*xi)),
            "vacuum_measure":s.simplify(s.exp(xi+3*w)-s.exp((3*u-2)*xi)),
            "clock_measure":s.simplify(s.exp(xi+3*w)*s.exp(-2*xi)-s.exp((3*u-4)*xi)),
            "potential_derivative":s.simplify(s.diff(potential(u),u)+2*u*s.log(1-u*u)**2)},
        convention="H0=int sqrt(barh)*scalar; P^ij=pi^ij/sqrt(barh), P2=(barh_ij P^ij)^2; displayed t is replaced by t_definition after differentiation")


@lru_cache(None)
def derive_auxiliary():
    d = derive_density()
    xi, u, t, theta = d["xi"], d["u"], d["t"], d["t_jets"]
    q = (xi, u)
    gradients = d["a"]+d["b"]
    L = d["scalar_jets"]
    def derivative(expr, variable):
        return s.diff(expr, variable)+s.diff(expr, t)*s.diff(theta, variable)
    partial = s.Matrix([derivative(L, j) for j in q])
    flux = s.Matrix([derivative(L, j) for j in gradients])
    H00 = s.Matrix(2, 2, lambda i, j: derivative(partial[i], q[j]))
    H01 = s.Matrix(2, 6, lambda i, j: derivative(partial[i], gradients[j]))
    H10 = s.Matrix(6, 2, lambda i, j: derivative(flux[i], q[j]))
    H11 = s.Matrix(6, 6, lambda i, j: derivative(flux[i], gradients[j]))
    theta1 = s.Matrix([s.diff(theta, j) for j in gradients])
    theta2 = s.hessian(theta, gradients)
    independent = d["prefactor"]*d["P2"]/9*(2*theta1*theta1.T/t**3-theta2/t**2)
    independent += s.hessian(d["spatial"].subs(d["gradient_invariants"]), gradients)
    actual = L.subs(t, theta)
    # Direct differentiation of the uncompressed action checks the chain map.
    # Denominators are compressed again only after this independent derivative.
    def compress(expr):
        return expr.subs(theta, t)
    first_residuals = [s.simplify(compress(s.diff(actual,j))-derivative(L,j)) for j in q+gradients]
    hessian_residual = H11-independent
    residuals = {"actual_first_derivatives":0 if all(v==0 for v in first_residuals) else 1,
        "actual_gradient_hessian":0 if zero_matrix(hessian_residual) else 1,
        "auxiliary_mixed_partials":0 if zero_matrix(H00-H00.T) else 1,
        "auxiliary_gradient_mixed_partials":0 if zero_matrix(H10-H01.T) else 1,
        "gradient_mixed_partials":0 if zero_matrix(H11-H11.T) else 1}
    # Do not expand covariant divergence: its coefficients also depend on
    # metric, curvature and momentum jets, whose derivatives must be retained.
    return dict(q=q, gradients=gradients, partial=partial, flux=flux,
        H00=H00, H01=H01, H10=H10, principal_gradient_hessian=H11,
        residuals=residuals,
        secondary="S_A=delta H0/dq_A=sqrt(barh)*(partial_A-D_i flux_A^i)",
        auxiliary_operator="M_AB eta_B=H00_AB eta_B+H01_A,Bj D_j eta_B-D_i(H10_Ai,B eta_B+H11_Ai,Bj D_j eta_B)",
        principal_symbol="H11_Ai,Bj k_i k_j; no invertibility, sign or kernel asserted",
        matter="Add (1/sqrt(barh))*delta H_m/dq_A and its actual Frechet derivative; not represented by an absent matter Lagrangian")


@lru_cache(None)
def derive_operator_control():
    # Independent polynomial variational-jet benchmark, with nonconstant
    # coefficients and mixed gradients, checks signs and both divergence terms.
    q, u, q1, u1, q2, u2 = s.symbols("q u q1 u1 q2 u2", real=True)
    e, f, e1, f1, e2, f2 = s.symbols("eta rho eta1 rho1 eta2 rho2", real=True)
    q0, qd, qdd = (q, u), (q1, u1), (q2, u2)
    eta, etad, etadd = (e, f), (e1, f1), (e2, f2)
    def total(expr):
        return sum(s.diff(expr,a)*b for a,b in zip(q0+qd+eta+etad, qd+qdd+etad+etadd))
    H = (1+q*q)*q1*q1/2+q*u*q1*u1+(2+u*u)*u1*u1/2+q*q*u
    S = s.Matrix([s.diff(H,a)-total(s.diff(H,b)) for a,b in zip(q0,qd)])
    direct = s.Matrix([sum(s.diff(val,a)*b for a,b in zip(q0+qd+qdd,eta+etad+etadd)) for val in S])
    assembled = s.Matrix([sum(s.diff(H,a,c)*v+s.diff(H,a,cd)*vd
        -total(s.diff(H,ad,c)*v+s.diff(H,ad,cd)*vd)
        for c,cd,v,vd in zip(q0,qd,eta,etad)) for a,ad in zip(q0,qd)])
    missing = direct-s.hessian(H,q0)*s.Matrix(eta)
    return dict(secondary=S, operator_action=assembled,
        omit_divergence_mutation=missing,
        residuals={"frechet_vs_euler":0 if zero_matrix(direct-assembled) else 1})


@lru_cache(None)
def derive_bracket_control():
    a, p, m, a0, kap = s.symbols("a p_a m a0 kappa", positive=True)
    xi, u, Lam = s.symbols("xi u Lambda", real=True)
    # This exact homogeneous restriction is computed from the full invariant
    # Hamiltonian: piTF=0, pi=a*p_a/2, C=m*a^3*exp((3u-4)xi)/2.
    H = -s.exp((4-3*u)*xi)*p*p/(12*m*a)+a**3*(
        m*s.exp((3*u-2)*xi)*(Lam+a0*a0*potential(u))-kap*s.exp((3*u-4)*xi)/2)
    Sxi, Su = s.diff(H,xi), s.diff(H,u)
    bracket = s.diff(Sxi,a)*s.diff(Su,p)-s.diff(Sxi,p)*s.diff(Su,a)
    reverse = s.diff(Su,a)*s.diff(Sxi,p)-s.diff(Su,p)*s.diff(Sxi,a)
    # Do not retune the action's Lambda/a0/kappa witness relations to choose
    # a phase-space fixture: this bracket is nonzero for their actual values.
    fixture = {a:1,p:1,xi:0,u:s.Rational(1,2)}
    fixture_secondary = tuple(s.simplify(v.subs(fixture)) for v in (Sxi,Su))
    return dict(a0=a0, H=H, secondary=(Sxi,Su), bracket=s.factor(bracket),
        off_shell_fixture=s.simplify(bracket.subs(fixture)),
        fixture_secondary=fixture_secondary,
        fixture_satisfies_auxiliary_constraints=all(v==0 for v in fixture_secondary),
        antisymmetry_residual=s.expand(bracket+reverse),
        scope="off-constraint regular homogeneous phase point: rules out an identically zero Omega, not a weak/on-constraint nonzero claim")


@lru_cache(None)
def derive_metric_variation_control():
    # Direct six-component differentiation verifies the normalized momentum
    # invariants appearing in the metric derivative of a smeared secondary.
    gvars = s.symbols("g11 g22 g33 g12 g13 g23", real=True)
    g = symmetric(gvars)
    inv = g.inv()
    pi = symmetric(s.symbols("pi11 pi22 pi33 pi12 pi13 pi23", real=True))
    root = s.sqrt(g.det())
    P = pi/root
    trace = s.trace(g*P)
    B = trace**2
    A = s.trace(g*P*g*P)-B/3
    Ametric = 2*P*g*P-2*trace*P/3-A*inv
    Bmetric = 2*trace*P-B*inv
    rA = s.Matrix([s.diff(A,v)-weight*Ametric[i,j]
        for v,(i,j),weight in zip(gvars,PAIRS,WEIGHTS)])
    rB = s.Matrix([s.diff(B,v)-weight*Bmetric[i,j]
        for v,(i,j),weight in zip(gvars,PAIRS,WEIGHTS)])
    # Flat-point actual deltaR=partial_i partial_j delta g_ij-Delta tr(delta g).
    # Integration by parts twice puts its adjoint on f_R, with a positive sign.
    k = s.Matrix(s.symbols("k1:4", real=True))
    variation = symmetric(s.symbols("v11 v22 v33 v12 v13 v23", real=True))
    fR = s.Symbol("f_R")
    deltaR = -(k.T*variation*k)[0]+(k.dot(k))*s.trace(variation)
    adjoint = fR*(-k*k.T+s.eye(3)*k.dot(k))
    pairing = sum(adjoint[i,j]*variation[i,j] for i in range(3) for j in range(3))
    return dict(residuals={"normalized_TF_metric_variation":0 if zero_matrix(rA) else 1,
        "normalized_trace_metric_variation":0 if zero_matrix(rB) else 1,
        "curvature_adjoint":s.expand(pairing-fR*deltaR)},
        omit_curvature_derivatives_mutation=pairing,
        smeared_secondary="S[f]=int sqrt(barh)*fhat, fhat=f_A*H_qA+(D_i f_A)*H_qAi",
        metric_derivative="E_f^ij=sqrt(barh)*[barh^ij*fhat/2+(partial fhat/partial barh_ij)_(pi,R,q,Dq,Df)-fhat_R*Rbar^ij+(D^i D^j-barh^ij Delta)fhat_R]",
        momentum_derivative="B_f,ij=sqrt(barh)*(partial fhat/partial pi^ij)_sym",
        bracket="Omega[f,g]=int(E_f^ij B_g,ij-B_f,ij E_g^ij)+ordinary-matter canonical PB if present; auxiliary p does not contribute because S is p-independent",
        note="Algebraic metric derivative holds covectors Dq,Df fixed; includes the determinant in P=pi/sqrt(barh). All ordered i,j summed; off-diagonal tensor derivatives are half independent-component derivatives.")


@lru_cache(None)
def derive_block_control():
    # A noncommuting finite matrix benchmark verifies the operator block
    # algebra; it does not approximate or prove an inverse of the PDE operator.
    K = s.Matrix([[2,1],[1,3]])
    Omega = s.Matrix([[0,5],[-5,0]])
    block = s.BlockMatrix([[s.zeros(2),-K],[K,Omega]]).as_explicit()
    proposed = s.BlockMatrix([[K.inv()*Omega*K.inv(),K.inv()],[-K.inv(),s.zeros(2)]]).as_explicit()
    wrong = s.BlockMatrix([[s.zeros(2),K.inv()],[-K.inv(),s.zeros(2)]]).as_explicit()
    return dict(inverse_residual=block*proposed-s.eye(4),
        inverse_without_omega_residual=block*wrong-s.eye(4),
        primary_secondary_sign="{p[f],S[g]}=-<g,M f>; {S[f],p[g]}=<f,M g>",
        operator_matrix="[[0,-K],[K,Omega]] in coordinate-density pairing, K=sqrt(barh)*M is the actual Hessian of H0; formal self-adjointness requires the stated boundary terms to vanish",
        conditional_inverse="[[K^-1 Omega K^-1,K^-1],[-K^-1,0]]",
        multiplier_equation="M lambda=-(1/sqrt(barh))*{S,H0} modulo spatial transport, after S=0",
        condition="M must be a two-sided domain-compatible invertible operator; formal self-adjointness or a principal symbol does not prove this",
        constraints="p_xi=p_u=P_shift_i=0; S_xi=S_u=0; H_i=-2 barh_ik D_j pi^jk+p_xi D_i xi+p_u D_i u (+H_mi). Extended H_i differs from the raw Legendre shift coefficient only by primaries.")


def encode(value):
    if isinstance(value, s.MatrixBase):
        return [[encode(value[i,j]) for j in range(value.cols)] for i in range(value.rows)]
    if isinstance(value, s.Basic):
        return str(value)
    if isinstance(value, dict):
        return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value, (tuple,list)):
        return [encode(v) for v in value]
    return value


def run():
    started = time.monotonic()
    started_at = datetime.now(timezone.utc).isoformat()
    sections = {"point_transform":derive_point_transform(), "legendre":derive_legendre(), "spatial":derive_spatial(),
        "density":derive_density(), "auxiliary":derive_auxiliary(),
        "variational_control":derive_operator_control(), "bracket_control":derive_bracket_control(),
        "metric_variation":derive_metric_variation_control(), "block_control":derive_block_control()}
    checks = {name+":"+key:value==0 for name,data in sections.items()
              for key,value in data.get("residuals",{}).items()}
    checks["nonzero_omega_control"] = sections["bracket_control"]["off_shell_fixture"] != 0
    checks["bracket_antisymmetry"] = sections["bracket_control"]["antisymmetry_residual"] == 0
    checks["conditional_block_inverse"] = sections["block_control"]["inverse_residual"] == s.zeros(4)
    if not all(checks.values()):
        raise AssertionError({k:v for k,v in checks.items() if not v})
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    self_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    repo = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=SOURCE.parent, text=True).strip())
    actual_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=normal"], cwd=repo, text=True).strip())
    software = [{"name":"Python", "version":platform.python_version()}, {"name":"SymPy", "version":s.__version__}]
    manifest = dict(schema_version=1, claim_id="IC4-nonlinear-Hamiltonian-identities-not-functional-closure",
        repository={"commit":actual_commit, "dirty":dirty},
        command="nonlinear_hamiltonian.run() in-process; regeneration: python3 -B nonlinear_hamiltonian.py",
        environment={"software":software, "hardware":platform.machine()},
        mathematics={"assertion_tested":"Nonlinear six-component Legendre inversion, conformal spatial identity, exact local auxiliary jets and conditional constraint-block algebra",
            "coefficient_domain":"Exact real symbolic algebra with exp and log; no floating-point ranks",
            "conventions":"Symmetric off-diagonal momentum has weight two; coordinate density Hessian K=sqrt(g) M",
            "inputs":[{"path":str(SOURCE.relative_to(repo)),"sha256":source_hash}],
            "bounds":{"metric_components":6,"auxiliary_fields":2,"spatial_dimensions":3,
                "branch":"positive definite metric, 0<u<1, finite xi, t_K!=0", "off_shell_bracket_fixtures":1,
                "resource_caps":"No explicit OS cap; bounded finite symbolic expressions, no enumeration or PDE solve"},
            "non_claims":["No functional operator inverse", "No complete matter-sector count", "No nonlinear stability or causality"]},
        randomness={"used":False,"generator":"none","seed":None},
        run={"started_at":started_at,"runtime_seconds":time.monotonic()-started,
             "exit_status":0,"scope":"Successful in-process exact computation; CLI requirement gate may separately return 2"},
        outputs=[{"path":str(Path(__file__).resolve().relative_to(repo)),"sha256":self_hash}],
        checks=[{"name":k,"passed":v} for k,v in checks.items()],
        result="Exact identities pass; full functional closure remains conditional",
        residual_risks=["Version 1 manifest has no enforced OS resource limits or separate immutable result artifact",
            "Input source pin is checked; source authenticity is project-local, not an external theorem",
            "Smoothness, boundary domain, constraint solvability, rank persistence, and ordinary matter are not established"])
    # The output omits bulky general-metric formulas whose generating code and
    # exact residuals remain reproducible. Compact nonlinear scalar jets stay.
    sections["legendre"] = {k:v for k,v in sections["legendre"].items()
                             if k not in ("tensor_momentum","inverse_velocity","hamiltonian")}
    sections["auxiliary"] = {k:v for k,v in sections["auxiliary"].items()
                              if k not in ("H00","H01","H10","principal_gradient_hessian")}
    return encode(dict(base=BASE, source_sha256=source_hash,
        input_hash_matches=source_hash==SOURCE_HASH,
        self_sha256=self_hash, computation_manifest=manifest,
        software={"python":platform.python_version(),"sympy":s.__version__},
        elapsed_seconds=time.monotonic()-started, checks=checks, checks_passed=all(checks.values()),
        sections=sections, full_functional_closure_proved=False,
        computation_contract="Exact real symbolic algebra, arbitrary positive-definite 3-metric and six symmetric velocities; smooth 0<u<1, finite xi, a0,m,kappa>0, t!=0. Covariant first auxiliary jets and curvature retained. One off-shell homogeneous PB fixture, no numerical scan.",
        remaining_gap="Specify boundary/function spaces; prove existence/regularity and two-sided inverse (or classify kernel/compatibility) of the nonlinear auxiliary Frechet operator and invariance of that rank branch. Include actual ordinary-matter Hamiltonian in this operator and its PB before a full-theory count. No stability/locality/nonlinear lift certified."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-functional-closure", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["input_hash_matches"]:
        return 1
    return 2 if args.require_functional_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
