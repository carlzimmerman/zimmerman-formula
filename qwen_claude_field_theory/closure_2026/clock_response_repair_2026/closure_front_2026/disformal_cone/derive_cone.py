#!/usr/bin/env python3
"""Action-derived Maxwell cone and conditional L215 no-slip obstruction.

The unchanged Einstein+cubic action has the g tensor cone on the homogeneous
aligned branch (independent tensor_cone.py regression). This script does not
assume a full nonlinear L215 action or certify PPN parameters.
"""
import json
import sympy as s


def maxwell_coefficients(C, lapse2):
    """Differentiate -sqrt(-gtilde) F_mu_nu F^mu_nu / 4."""
    at, az = s.symbols('A_t A_z', real=True)
    metric = s.diag(-lapse2, C, C, C)
    inverse = metric.inv()
    field = s.zeros(4)
    field[0, 1], field[1, 0] = at, -at
    field[3, 1], field[1, 3] = az, -az
    raised = inverse*field*inverse
    contraction = sum(field[i, j]*raised[i, j] for i in range(4) for j in range(4))
    lagrangian = s.simplify(-s.sqrt(-metric.det())*contraction/4)
    return s.simplify(s.diff(lagrangian, at, 2)), s.simplify(-s.diff(lagrangian, az, 2))


def potential_shifts(c, d):
    """Coefficients of varphi from metric components, not assigned potentials."""
    eps, phi, psi, varphi = s.symbols('eps Phi Psi varphi', real=True)
    C, D = 1+2*c*eps*varphi, 2*d*eps*varphi
    g00, g11 = -1-2*eps*phi, 1-2*eps*psi
    n0_squared = 1+2*eps*phi
    physical00 = C*g00+D*n0_squared
    physical11 = C*g11  # static aligned clock: n_i=0
    Phi = -s.diff(physical00, eps).subs(eps, 0)/2
    Psi = -s.diff(physical11, eps).subs(eps, 0)/2
    return s.simplify(s.diff(Phi, varphi)), s.simplify(s.diff(Psi, varphi))


def derive():
    C, L = s.symbols('C L', positive=True)  # L=C-D>0, nondegenerate Lorentzian metric
    D, c, d, varphi = s.symbols('D c d varphi', real=True)
    kinetic, gradient = maxwell_coefficients(C, L)
    speed2 = s.simplify(gradient/kinetic)
    eta = s.diag(-1, 1, 1, 1)
    n = s.Matrix([-1, 0, 0, 0])
    metric = C*eta+D*n*n.T
    inverse = metric.inv()
    expected_inverse = eta/C-D/(C*(C-D))*(eta*n)*(eta*n).T
    t, x, y, z = s.symbols('t x y z', real=True)
    ray = s.Matrix([t, x, y, z])
    norm_relation = s.expand((ray.T*metric*ray)[0]-C*(ray.T*eta*ray)[0])
    delta_phi, delta_psi = potential_shifts(c, d)
    cone_linear = s.diff(speed2.subs({C: 1+2*c*varphi, L: 1+2*(c-d)*varphi}), varphi).subs(varphi, 0)
    simultaneous = s.solve([delta_phi-delta_psi, cone_linear], [c, d], dict=True)
    checks = {}
    def check(name, lhs, rhs=0):
        checks[name] = s.simplify(lhs-rhs) == 0
        if not checks[name]:
            raise AssertionError((name, lhs, rhs))
    check('Maxwell_null_speed_from_EL', speed2, L/C)
    check('independent_inverse_metric_dispersion', speed2, -inverse[3, 3]/inverse[0, 0].subs(D, C-L))
    check('physical_metric_determinant', metric.det(), -C**3*(C-D))
    for i in range(4):
        for j in range(4):
            check('inverse_%s_%s' % (i, j), inverse[i, j], expected_inverse[i, j])
    check('invariant_ray_norm_difference', norm_relation, D*t**2)
    check('Phi_shift', delta_phi, c-d)
    check('Psi_shift', delta_psi, -c)
    check('first_order_cone_shift', cone_linear, -2*d)
    check('simultaneous_no_slip_common_cone_c', simultaneous[0][c])
    check('simultaneous_no_slip_common_cone_d', simultaneous[0][d])
    # Explicit exact boosts include perfect alignment; alignment never makes a
    # nonzero disformal norm zero for a nonzero g-null ray.
    boost_controls = []
    for w in [s.Rational(0), s.Rational(3, 5), -s.Rational(3, 5)]:
        gamma = 1/s.sqrt(1-w*w)
        covector = s.Matrix([-gamma, gamma*w, 0, 0])
        gtilde = C*eta+D*covector*covector.T
        k = s.Matrix([1, 1, 0, 0])
        check('unit_clock_%s' % w, (covector.T*eta*covector)[0], -1)
        coeff = s.simplify((k.T*gtilde*k)[0]/D)
        check('boost_ray_norm_%s' % w, coeff, (1-w)/(1+w))
        if coeff <= 0:
            raise AssertionError('timelike clock contraction vanished')
        boost_controls.append(dict(w=str(w), norm_over_D=str(coeff)))
    # L215 is specified only to linear order. Do not infer its unknown O(phi²).
    l215_shift = [value.subs({c: -1, d: -2}) for value in (delta_phi, delta_psi)]
    l215_cone_shift = cone_linear.subs(d, -2)
    check('L215_equal_nonzero_shift', l215_shift[0], l215_shift[1])
    check('L215_nonzero_cone_shift', l215_cone_shift, 4)
    # Known TeVeS metric, used only as a comparison, not a new action completion.
    known_speed = s.simplify(speed2.subs({C: s.exp(-2*varphi), L: s.exp(2*varphi)}))
    check('known_exponential_metric_cone', known_speed, s.exp(4*varphi))
    return dict(
        scope='Pointwise disformal kinematics plus Maxwell variation; unchanged tensor cone on aligned homogeneous branch',
        assumptions=['C>0 and C-D>0', 'g-unit timelike clock covector',
                     'photons minimally coupled to physical gtilde=C*g+D*n*n',
                     'tensor cone remains g; baseline Phi=Psi for the shift-only theorem'],
        maxwell_kinetic=str(kinetic), maxwell_gradient=str(gradient),
        photon_speed_squared_over_g_cone=str(speed2.subs(L, C-D)),
        matter_measured_tensor_speed_squared=str(s.simplify(1/speed2).subs(L, C-D)),
        shifts=dict(Phi=str(delta_phi), Psi=str(delta_psi)),
        no_slip_and_common_cone_solution=[{str(k): str(v) for k, v in row.items()} for row in simultaneous],
        L215_first_order_photon_speed_squared='1 + %s*varphi + O(varphi**2)' % l215_cone_shift,
        invariant_norm_difference=str(norm_relation), boost_controls=boost_controls,
        known_TeVeS_metric_speed_squared=str(known_speed), checks=checks,
        non_claims=['No empirical GW exclusion without field profile and emission assumptions',
                    'No full PPN or clock-drag calculation', 'No universal MOND no-go',
                    'No inference of nonlinear L215 completion', 'No proof of arbitrary inhomogeneous tensor characteristics'])


if __name__ == '__main__':
    print(json.dumps(derive(), indent=2))
