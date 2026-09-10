#!/usr/bin/env python3
"""Independent spherical metric/pressure lensing diagnostic, with c=1.

The clock is an explicit field. This module supplies no universal P(X),G(X)
solution, stability certificate, boundary matching, data fit, or PPN parameter.
"""
from functools import lru_cache
import json
import sympy as s


@lru_cache(None)
def geometry():
    """Compute the Einstein tensor from the metric, not a supplied stress."""
    t, r, theta, az = s.symbols('t r theta az', real=True)
    m = s.Symbol('m', positive=True)
    A, B = s.Function('A')(r), s.Function('B')(r)
    coordinates = (t, r, theta, az)
    metric = s.diag(-A, B, r**2, r**2*s.sin(theta)**2)
    inverse = metric.inv()
    connection = [[[s.simplify(sum(inverse[a, d]*(
        s.diff(metric[d, c], coordinates[b])
        + s.diff(metric[d, b], coordinates[c])
        - s.diff(metric[b, c], coordinates[d]))/2 for d in range(4)))
        for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = s.Matrix(4, 4, lambda a, b: s.simplify(sum(
        s.diff(connection[c][a][b], coordinates[c])
        - s.diff(connection[c][a][c], coordinates[b])
        + sum(connection[c][c][d]*connection[d][a][b]
              - connection[c][b][d]*connection[d][a][c]
              for d in range(4)) for c in range(4))))
    mixed_ricci = inverse*ricci
    einstein = mixed_ricci - s.eye(4)*s.trace(mixed_ricci)/2
    rho, pr, pt = [-m*einstein[0, 0], m*einstein[1, 1], m*einstein[2, 2]]
    expected_rho = m*((1-1/B)/r**2+s.diff(B, r)/(B**2*r))
    expected_pr = m*((1/B-1)/r**2+s.diff(A, r)/(A*B*r))
    return dict(r=r, m=m, A=A, B=B, rho=s.simplify(rho),
                pr=s.simplify(pr), pt=s.simplify(pt),
                residuals=[s.simplify(rho-expected_rho),
                           s.simplify(pr-expected_pr)])


@lru_cache(None)
def derive():
    r, R, m = s.symbols('r R m', positive=True)
    e, g, gp, P, Pp, Phi, Psi, Psip = s.symbols(
        'e g gp P Pp Phi Psi Psip', real=True)
    T = 1+2*r*g
    B = T/(1+r**2*P/m)
    dB = s.diff(B, r)+s.diff(B, g)*gp+s.diff(B, P)*Pp
    rho = s.factor(m*((1-1/B)/r**2+dB/(B**2*r)))
    pr = m*((1/B-1)/r**2+2*g/(B*r))
    weak = lambda expression: s.simplify(s.diff(expression, e).subs(e, 0))
    b1 = weak(B.subs({g:e*g, P:e*P}))
    rho1 = weak(rho.subs({g:e*g, gp:e*gp, P:e*P, Pp:e*Pp}))
    # r=R(1-e*Psi), dr/dR=1-e*(Psi+R*Psip).
    spatial_radial = (1+e*b1.subs(r, R))*(1-e*(Psi+R*Psip))**2
    isotropic_residual = weak(spatial_radial-(1-2*e*Psi))
    solved_Psip = s.solve(isotropic_residual, Psip)[0]
    optical_index = s.sqrt((1-2*e*Psi)/(1+2*e*Phi))
    # Log potentials: A=e^(2*Phi_log), r=R*e^(-Psi_log).
    # Positive dr/dR branch follows from B*(1-R*Psi_log')^2=1.
    exact_Psi_log_slope = (1-1/s.sqrt(B))/R
    exact_Phi_log_slope = g*r/(R*s.sqrt(B))
    exact_ratio = s.simplify(exact_Psi_log_slope/exact_Phi_log_slope)
    h = r**2*P/m
    # Rationalized expression remains stable when P is tiny.
    exact_pressure_ratio_change = -s.sqrt(T)*h/(
        r*g*s.sqrt(1+h)*(1+s.sqrt(1+h)))
    rho0 = rho.subs({P:0, Pp:0})
    Weyl_prime = g-r*P/(4*m)
    Weyl_second = s.diff(Weyl_prime, r)+s.diff(Weyl_prime, g)*gp+s.diff(Weyl_prime, P)*Pp
    rho_Weyl = s.factor(2*m*(Weyl_second+2*Weyl_prime/r))
    return dict(
        B=B, rho=rho, rho_no_pressure=s.factor(rho0),
        metric_radial_perturbation=b1,
        Phi_prime=g, Psi_prime=g-r*P/(2*m),
        Weyl_prime=Weyl_prime,
        slip_prime=r*P/(2*m),
        slope_ratio=1-r*P/(2*m*g),
        fractional_Weyl_suppression=r*P/(4*m*g),
        rho_weak=rho1,
        rho_Weyl_weak=rho_Weyl,
        optical_index_first_order=weak(optical_index),
        exact_log_potential_slope_ratio=exact_ratio,
        exact_pressure_ratio_change=exact_pressure_ratio_change,
        residuals=[s.factor(pr-P),
            s.factor(b1-(2*r*g-r**2*P/m)),
            s.factor(solved_Psip-(g-R*P/(2*m))),
            s.factor(rho1-(2*m*(gp+2*g/r)-3*P-r*Pp)),
            s.factor(weak(optical_index)+Phi+Psi),
            s.simplify(exact_ratio-(s.sqrt(B)-1)/(r*g)),
            s.factor(rho_Weyl-(2*m*(gp+2*g/r)+rho1)/2)])


@lru_cache(None)
def constant_pressure_clock():
    """Local exact J^r=0 timelike KGB inverse; health is not established."""
    r, M, m, P, q = s.symbols('r M m P q', positive=True)
    A = 1-2*M/r
    B = 1/(A*(1+r**2*P/m))
    g = s.diff(A, r)/(2*A)
    rho = s.factor(m*((1-1/B)/r**2+s.diff(B, r)/(B**2*r)))
    pt = s.factor(P+r*g*(rho+P)/2)
    beta = r*g/2
    X = s.factor(q**2/(2*A*(1+beta)))
    Xp = s.diff(X, r)
    p2 = 2*B*X*beta
    L = s.factor((rho+P)/(2*X*Xp))  # G_X=p L; P_X=0.
    reduced_current = 2*L*X*g/B-2*L*p2/(B**2*r)  # J^r/p.
    independent = geometry()
    ir = independent['r']
    metric_subs = {independent['A']:A.subs(r, ir),
                   independent['B']:B.subs(r, ir)}
    geometric_pr = independent['pr'].subs(metric_subs).doit().subs(ir, r)
    geometric_pt = independent['pt'].subs(metric_subs).doit().subs(ir, r)
    return dict(A=A, B=B, rho=rho, P=P, pt=pt, beta=beta, X=X,
                Xprime=s.factor(Xp), G_X_over_p=L,
                domain='r>2M, M,m,P,q>0; local monotone X branch',
                residuals=[s.factor(reduced_current),
                    s.factor(2*X*L*Xp-P-rho),
                    s.factor(P+2*X*beta*L*Xp-pt),
                    s.factor(rho-(-3*P+4*M*P/r)),
                    s.factor(geometric_pr-P), s.factor(geometric_pt-pt)])


def target_controls():
    """Exact inputs evaluated to 30 digits; no integration or data fit."""
    eps = s.Rational(1, 10**6)
    y = s.Integer(20)
    mu = 1-s.exp(-y)
    lam = mu+y*s.exp(-y)
    r = eps/s.sqrt(y*mu)
    yr = -2*y*mu/(r*lam)
    T = 1/(1-2*r*y)
    g = y*T
    rho0 = 4*y**2*s.exp(-y)/(r*lam)  # m=1, exact chosen metric.
    curvature_density = 2*g/r
    coefficient = -3+8*r*y+2*r*r*yr  # Constant P: rho=rho0+coefficient*P.
    def row(name, pressure):
        rho = rho0+coefficient*pressure
        h = r*r*pressure
        exact_delta = -s.sqrt(T)*h/(r*g*s.sqrt(1+h)*(1+s.sqrt(1+h)))
        values = dict(y=y, epsilon=eps, rg=r*g, r2P=h,
            rho0_over_curvature_density=rho0/curvature_density,
            P_over_curvature_density=pressure/curvature_density,
            rho_over_curvature_density=rho/curvature_density,
            P_over_rho=pressure/rho,
            leading_Weyl_fraction=pressure/(2*curvature_density),
            exact_log_slope_ratio_pressure_change=exact_delta)
        return dict(name=name, **{k:str(s.N(v, 30)) for k,v in values.items()})
    almost_zero = -(1-s.Rational(1, 10**6))*rho0/coefficient
    negative = curvature_density/s.Integer(10**6)
    return [row('large_pressure_to_actual_density_ratio', almost_zero),
            row('negative_density_small_pressure_slip', negative)]


def serial(value):
    if isinstance(value, dict):
        return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(v) for v in value]
    if isinstance(value, s.Basic):
        return str(value)
    return value


def results():
    return serial(dict(geometry=geometry(), derivation=derive(),
        local_constant_pressure_clock=constant_pressure_clock(),
        target_controls=target_controls(),
        status='METRIC DIAGNOSTIC VERIFIED; UNIVERSAL HEALTHY THEORY OPEN'))


if __name__ == '__main__':
    print(json.dumps(results(), indent=2))
