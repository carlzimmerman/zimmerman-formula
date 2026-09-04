#!/usr/bin/env python3
"""Action-derived spherical MOND orbital shape discriminants.

Only the nonrelativistic AQUAL action and ordinary test-particle kinetic term
are used. No tensor, slip, PPN, cosmology, or relativistic DOF claim is made.
Coordinates x: g/a0 for mu_exp; sqrt(g_N/a0) for nu_rar. Both are positive.
Run from the repository root with python3 <this file>. Prints JSON to stdout.
"""
from functools import lru_cache
import json

import mpmath as mp
import numpy as np
import sympy as sp


@lru_cache(None)
def derive():
    x = sp.Symbol('x', positive=True)
    r, p, pp, a, GN, rho, potential = sp.symbols(
        'r p pp a0 G_N rho Phi', positive=True)
    mu = sp.Function('mu')(p/a)
    primitive = sp.Function('F')(p/a)
    lagrangian = -r*r*(a*a*primitive/(8*sp.pi*GN)+rho*potential)
    derivatives = sp.diff(primitive, p).atoms(sp.Subs)
    if len(derivatives) != 1:
        raise ArithmeticError('unexpected symbolic chain-rule representation')
    primitive_derivative = next(iter(derivatives))
    momentum = sp.diff(lagrangian, p).xreplace({primitive_derivative: 2*p*mu/a})
    el = sp.diff(lagrangian, potential) - sp.diff(momentum, r) - pp*sp.diff(momentum, p)
    flux = 2*p*mu/r + pp*(mu+p*sp.diff(mu, p))-4*sp.pi*GN*rho

    # Ordinary particle action -> radial effective potential curvature.
    rr = sp.Symbol('r', positive=True)
    ell = sp.Symbol('ell', positive=True)
    phi = sp.Function('Phi')(rr)
    effective = phi+ell**2/(2*rr**2)
    ell2 = sp.solve(sp.diff(effective, rr), ell**2)[0]
    omega2 = ell2/rr**4
    kappa2 = sp.diff(effective, rr, 2).subs(ell**2, ell2)

    L = x/(sp.exp(x)-1)
    mue = 1-sp.exp(-x)
    s_exp = x*mue
    # s=g_N/a0 varies as r^-2 outside a fixed spherical source.
    rate_exp = -2*s_exp/sp.diff(s_exp, x)
    q_exp = sp.simplify(3+rate_exp/x)
    y_rar = x*x/(1-sp.exp(-x))
    rate_rar = -x
    q_rar = sp.simplify(3+rate_rar*sp.diff(y_rar, x)/y_rar)
    qs = {'mu_exp': q_exp, 'nu_rar': q_rar}
    rates = {'mu_exp': rate_exp, 'nu_rar': rate_rar}
    flows = {k: sp.simplify(sp.diff(qs[k], x)*rates[k]) for k in qs}
    invariant = {k: sp.limit((flows[k]-(2-qs[k]))/(2-qs[k])**2, x, 0)
                 for k in qs}

    # Parametric RAR primitive F(y(x)) = integral_0^x 2 u^2 y'(u) du.
    # Differentiation by the fundamental theorem gives F_y=2x^2, so
    # F_y/(2y)=1-exp(-x). Its two constitutive Hessian eigenvalues follow.
    integrand = sp.simplify(2*x*x*sp.diff(y_rar, x))
    transverse = sp.simplify(x*x/y_rar)
    longitudinal = sp.simplify(sp.diff(x*x, x)/sp.diff(y_rar, x))
    exp_primitive = x*x+2*(1+x)*sp.exp(-x)-2
    residuals = {
        'radial_action_EL': sp.simplify(el*4*sp.pi*GN/r**2-flux),
        'particle_epicycle': sp.simplify(kappa2-sp.diff(phi, rr, 2)-3*sp.diff(phi, rr)/rr),
        'particle_circular_frequency': sp.simplify(omega2-sp.diff(phi, rr)/rr),
        'exp_primitive_flux': sp.simplify(sp.diff(exp_primitive, x)/(2*x)-mue),
        'exp_q': sp.simplify(q_exp-(1+3*L)/(1+L)),
        'rar_q': sp.simplify(q_rar-1-L),
        'exp_flow': sp.simplify(flows['mu_exp']-4*L*(x+L-1)/(1+L)**3),
        'rar_flow': sp.simplify(flows['nu_rar']-L*(x+L-1)),
        'rar_strict_inequality_identity': sp.simplify(
            2-q_rar-flows['nu_rar']-(1-x*x*sp.exp(x)/(sp.exp(x)-1)**2)),
        'rar_action_flux': sp.simplify(
            (integrand/sp.diff(y_rar, x)/(2*y_rar)-transverse).rewrite(sp.exp)),
    }
    return {'x': x, 'L': L, 'q': qs, 'flow': flows,
            'deep_invariant': invariant, 'action_EL': el,
            'rar_y': y_rar, 'rar_primitive_integrand': integrand,
            'rar_transverse': transverse, 'rar_longitudinal': longitudinal,
            'residuals': residuals}


def inverse_L(ell):
    """Invert x/(exp(x)-1)=ell on x>0; W_0 would give spurious x=0."""
    ell = mp.mpf(ell)
    if not 0 < ell < 1:
        raise ValueError('L must be strictly between zero and one')
    extra = max(0, int(mp.ceil(-2*mp.log10(1-ell))))
    with mp.workdps(max(mp.mp.dps, extra+60)):
        return mp.re(-ell-mp.lambertw(-ell*mp.exp(-ell), -1))


def q_flow(kernel, q):
    """Return dq/d ln r from q alone, with no M, a0, distance or time scale."""
    if kernel not in ('mu_exp', 'nu_rar'):
        raise ValueError('unknown kernel')
    q = mp.mpf(q)
    if not 1 < q < 2:
        raise ValueError('exterior transition branch requires 1<q<2')
    with mp.workdps(max(60, mp.mp.dps)):
        ell = (q-1)/(3-q) if kernel == 'mu_exp' else q-1
        x = inverse_L(ell)
        d = derive()
        return sp.lambdify(d['x'], d['flow'][kernel], 'mpmath')(x)


def acceleration(gbar, a0, kernel):
    """Float64 algebraic accelerations; these are not disk AQUAL solutions."""
    b = np.asarray(gbar, dtype=float)
    if not np.isfinite(a0) or a0 <= 0 or np.any(~np.isfinite(b)) or np.any(b < 0):
        raise ValueError('finite gbar>=0 and a0>0 required')
    if kernel not in ('mu_exp', 'nu_rar'):
        raise ValueError('unknown kernel')
    s = b/a0
    safe = np.where(s > 0, s, 1.)
    if kernel == 'nu_rar':
        return np.where(s > 0, b/-np.expm1(-np.sqrt(safe)), 0.)
    y = np.maximum(np.sqrt(safe), safe)
    for _ in range(50):
        mu = -np.expm1(-y)
        dy = (y*mu-safe)/(mu+y*np.exp(-y))
        y -= dy
        if np.max(np.abs(dy)/y) < 3e-15:
            break
    if np.max(np.abs(y*-np.expm1(-y)/safe-1)) > 1e-13:
        raise ArithmeticError('constitutive inversion did not converge')
    return np.where(s > 0, a0*y, 0.)


def rar_primitive(t):
    """Exact quadrature specification, F(0)=0, evaluated at caller precision."""
    t = mp.mpf(t)
    if t < 0:
        raise ValueError('t>=0 required')
    def integrand(u):
        if u == 0:
            return mp.mpf(0)
        mu = -mp.expm1(-u)
        yp = u*(2*mu-u*mp.exp(-u))/mu**2
        return 2*u*u*yp
    return mp.quad(integrand, [0, t])


def qumond_primitive(t):
    """Q(Z), evaluated parametrically at Z=t^4, not at Z=t or t^2."""
    t = mp.mpf(t)
    if t < 0:
        raise ValueError('t>=0 required')
    return mp.quad(lambda u: 4*u**3/(-mp.expm1(-u)) if u else mp.mpf(0), [0, t])


@lru_cache(None)
def derive_qumond_action():
    """Vary the static two-potential action; audit two naive mis-promotions.

    The canonical calculation is one real, source-static Fourier mode in a
    frozen background. The scalar Lorentzian Hessian is on a fixed metric;
    it is not a substitute for gravitational lapse/shift constraint analysis.
    """
    r, p, h, pp, hp, a, A, rho, phi = sp.symbols(
        'r Phi_r chi_r Phi_rr chi_rr a0 A rho Phi', positive=True)
    primitive = sp.Function('Q')(h*h/(a*a))
    nu = sp.Function('nu')(h/a)
    lagrangian = -r*r*(A*(2*p*h-a*a*primitive)+rho*phi)
    q_derivative = next(iter(sp.diff(primitive, h).atoms(sp.Subs)))
    momenta = [sp.diff(lagrangian, v).xreplace({q_derivative: nu}) for v in (p, h)]
    def radial_derivative(expr):
        return sp.diff(expr, r)+pp*sp.diff(expr, p)+hp*sp.diff(expr, h)
    els = [sp.diff(lagrangian, phi)-radial_derivative(momenta[0]),
           -radial_derivative(momenta[1])]
    poisson = hp+2*h/r-rho/(2*A)
    phantom = pp+2*p/r-(hp*(nu+h*sp.diff(nu, h))+2*h*nu/r)
    residuals = {'Phi_variation_Poisson': sp.simplify(els[0]/(2*A*r*r)-poisson),
                 'chi_variation_phantom_density': sp.simplify(els[1]/(2*A*r*r)-phantom)}

    # Dirac chain for the strictly static NR potential sector.
    f, c, pf, pc, uf, uc = sp.symbols('f c p_f p_c u_f u_c', real=True)
    k, b = sp.symbols('k b', positive=True)
    coordinates, momenta = [f, c], [pf, pc]
    H = A*k*k*(2*f*c-b*c*c)+rho*f
    Htotal = H+uf*pf+uc*pc
    pb = lambda F, G: sp.expand(sum(sp.diff(F, q)*sp.diff(G, pq)-
                                   sp.diff(F, pq)*sp.diff(G, q)
                                   for q, pq in zip(coordinates, momenta)))
    vf, vc = sp.symbols('Phi_dot chi_dot', real=True)
    primaries = [pq-sp.diff(-H, velocity)
                 for pq, velocity in zip(momenta, [vf, vc])]
    secondaries = [pb(C, Htotal) for C in primaries]
    constraints = primaries+secondaries
    matrix = sp.Matrix([[pb(C, D) for D in constraints] for C in constraints])
    preserved = [pb(C, Htotal) for C in secondaries]
    multipliers = sp.solve(preserved, [uf, uc], dict=True)[0]
    residuals.update({f'secondary_preservation_{i}': sp.simplify(e.subs(multipliers))
                      for i, e in enumerate(preserved)})
    jac = sp.Matrix(constraints).jacobian(coordinates+momenta)
    rank = matrix.rank()
    first = len(constraints)-rank
    dof = len(coordinates)-first-sp.Rational(rank, 2)

    # Simply making these TWO independent scalar fields Lorentzian fails:
    # a static spatial-gradient background gives this velocity block.
    temporal_lagrangian = A*(2*vf*vc-b*vc*vc)
    temporal_hessian = sp.hessian(temporal_lagrangian, [vf, vc])
    s = sp.Symbol('s', positive=True)
    nu_s = 1/(1-sp.exp(-sp.sqrt(s)))
    # f23's J'(s)=nu(s) is not Q_Z(Z)=nu(sqrt(Z)).
    wrong_force_sqrt_argument = nu_s/2
    wrong_force_squared_argument = s/(1-sp.exp(-s))
    return {'residuals': residuals, 'EL': els, 'Hamiltonian': H,
            'primaries': primaries, 'secondaries': secondaries,
            'constraint_Jacobian_rank': jac.rank(), 'PB_matrix': matrix,
            'PB_determinant': sp.factor(matrix.det()), 'finite_k_rank': rank,
            'finite_k_first_class': first, 'finite_k_second_class': rank,
            'finite_k_scalar_dof': dof, 'preservation_equations': preserved,
            'multipliers': multipliers, 'zero_k_rank': matrix.subs(k, 0).rank(),
            'zero_k_secondaries': [e.subs(k, 0) for e in secondaries],
            'lorentzian_hessian': temporal_hessian,
            'lorentzian_hessian_determinant': sp.factor(temporal_hessian.det()),
            'wrong_primitive_newton_ratio': sp.limit(wrong_force_sqrt_argument/s, s, sp.oo),
            'wrong_squared_argument_deep_g_over_a0': sp.limit(wrong_force_squared_argument, s, 0)}


def main():
    d = derive()
    checks = {k: v == 0 for k, v in d['residuals'].items()}
    qa = derive_qumond_action()
    checks.update({k: v == 0 for k, v in qa['residuals'].items()})
    with mp.workdps(65):
        examples = {str(q): {k: str(q_flow(k, q)) for k in d['q']}
                    for q in map(mp.mpf, ('1.1', '1.25', '1.5', '1.75', '1.9'))}
        # Report separation in an explicitly bounded scan, not a universal proof.
        grid = [mp.mpf(1)+mp.mpf(i)/100 for i in range(1, 100)]
        gaps = [q_flow('mu_exp', q)-q_flow('nu_rar', q) for q in grid]
    print(json.dumps({'checks': checks,
                      'symbolic': {k: {a: str(b) for a, b in d[k].items()}
                                   for k in ('q', 'flow', 'deep_invariant')},
                      'examples': examples,
                      'qumond_action_audit': {k: str(v) for k, v in qa.items() if k != 'residuals'},
                      'bounded_scan': {'q_min': 1.01, 'q_max': 1.99,
                                       'count': len(grid), 'minimum_gap': str(min(gaps))},
                      'interpretation': 'Derived nonrelativistic spherical corollaries; relativistic completion OPEN'}, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
