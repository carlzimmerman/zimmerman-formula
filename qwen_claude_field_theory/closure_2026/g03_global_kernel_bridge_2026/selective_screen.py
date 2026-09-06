"""Vary and falsify the matched Newtonian-floor screen, not an entire MOND class.

Replace f34's inside-J higher-spatial-gradient term by
 -A xi^2 (D_i W_j)^2, W_mu=q_mu^nu partial_nu chi-beta a_mu.
The rest of that action is unchanged. beta=1/(1+jN) is tested, not assigned
as a PPN parameter. Work about Minkowski, constant chi, Q0=0, clock rest.
The exact nonlinear action and exclusions are specified in SELECTIVE_SCREEN.md.
All constraint counts below are quadratic scalar Fourier counts, not nonlinear
gravitational DOF counts. k=0 is never obtained by cancelling powers of k.
"""
import argparse
import json
from pathlib import Path
import platform
import time

import sympy as s
from zero_field_source_audit import _build_source


def strings(matrix):
    return [[str(v) for v in row] for row in matrix.tolist()]


def dirac(H, coordinates, momenta):
    """Linear Dirac algorithm: left-null preservation, no expected rank/count."""
    phase = coordinates + momenta
    def pb(f, g):
        return s.expand(sum(s.diff(f, q)*s.diff(g, p)-s.diff(f, p)*s.diff(g, q)
                            for q, p in zip(coordinates, momenta)))
    primary = momenta[:2]
    constraints = list(primary)
    generations = [list(map(str, constraints))]
    def rows(exprs):
        return s.Matrix(exprs).jacobian(phase)
    def remainder(expr):
        R, pivots = rows(constraints).rref()
        for i, pivot in enumerate(pivots):
            expr = s.expand(expr-s.diff(expr, phase[pivot])*(R.row(i)*s.Matrix(phase))[0])
        return expr
    for _ in range(12):  # resource cap, never treated as closure
        A = s.Matrix([[pb(c, p) for p in primary] for c in constraints])
        b = s.Matrix([pb(c, H) for c in constraints])
        added = []
        for left in A.T.nullspace():
            expr = remainder(s.expand((left.T*b)[0]))
            if expr != 0:
                first = next(s.diff(expr, p) for p in phase if s.diff(expr, p) != 0)
                expr = s.expand(expr/first)
                constraints.append(expr)
                added.append(str(expr))
        if not added:
            break
        generations.append(added)
    else:
        raise RuntimeError('Dirac resource cap reached, not a closure result')
    u = s.symbols('u_n u_t')
    b = b.applyfunc(remainder)
    solutions = s.linsolve(list(A*s.Matrix(u)+b), u)
    if solutions is s.EmptySet or not solutions:
        raise RuntimeError('Inconsistent constraint preservation')
    multiplier = list(solutions)[0]
    closed = all(remainder(pb(c, H)+sum(pb(c, p)*v for p, v in zip(primary, multiplier))) == 0
                 for c in constraints)
    bracket = s.Matrix([[pb(c, d) for d in constraints] for c in constraints])
    rank = bracket.rank()
    first_class = len(constraints)-rank
    return {'generations': generations, 'constraints': list(map(str, constraints)),
            'phase_basis': list(map(str, phase)), 'poisson_matrix': strings(bracket),
            'constraint_count': len(constraints), 'bracket_rank': rank,
            'first_class': first_class, 'second_class': rank,
            'quadratic_scalar_modes': str(len(coordinates)-first_class-s.Rational(rank, 2)),
            'multipliers': list(map(str, multiplier)), 'preservation_closed': closed}


def derive():
    started = time.monotonic()
    A, c, c2, K, xi2, k, w, beta, j = s.symbols(
        'A c14 c2 K xi2 k omega beta j', real=True)
    q, x = k**2, xi2*k**2
    B, C = 2-c, 6+4/c2
    D, E, F = c-A*beta**2*x, A*(1+beta*x), A*(1+j+x)
    n, t, P, chi = s.symbols('n t P chi', real=True)
    pn, pt, pP, pc = s.symbols('p_n p_t p_P p_chi', real=True)
    vP, vc = s.symbols('v_P v_chi', real=True)
    # Real-mode ADM action. Both lapse and shift are retained before variation.
    V = q*(2*P**2-4*n*P+c*n**2+2*A*n*chi-A*(1+j)*chi**2)
    screen = -A*xi2*q**2*(chi-beta*n)**2
    L = -6*vP**2+4*q*vP*t-c2*(-3*vP+q*t)**2+K*vc**2+V+screen
    velocities = s.solve([s.diff(L, vP)-pP, s.diff(L, vc)-pc], [vP, vc])
    H = s.factor((pP*vP+pc*vc-L).subs(velocities))

    # Independent live f34 source build, without its caches or scan.
    ns, provenance = _build_source()
    nk, nb, tk, tb = s.symbols('nk nb tk tb')
    sub = {ns['KB']: 2-A, ns['C4']: c-(2-A), ns['C2']: c2,
           ns['K2']: -K, ns['JY']: j, ns['XI2']: xi2,
           ns['a1k']: -s.I*k*tk, ns['a1b']: s.I*k*tb,
           ns['Rk']: 0, ns['Rb']: 0, ns['XA']: 0, ns['XB']: 0,
           ns['XC']: 1, ns['LAM']: 0, ns['kx']: k, ns['om']: w,
           ns['Psik']: nk-s.I*w*tk, ns['Psib']: nb+s.I*w*tb}
    source = s.expand(ns['L2dc'].subs(sub, simultaneous=True))
    source += 2*A*j*xi2*q**2*ns['chib']*ns['chik']
    source -= 2*A*xi2*q**2*(ns['chib']-beta*nb)*(ns['chik']-beta*nk)
    bras = [nb, tb, ns['Phib'], ns['chib']]
    kets = [nk, tk, ns['Phik'], ns['chik']]
    M_source = s.Matrix(4, 4, lambda i, h: s.diff(source, bras[i], kets[h]))
    # Build Fourier bilinear directly from the independent real-mode action.
    ep, em = s.symbols('e_plus e_minus')
    fields = [a*ep+b*em for a, b in zip(kets, bras)]
    dc = s.expand(L.subs(dict(zip([n,t,P,chi,vP,vc], fields + [
        -s.I*w*kets[2]*ep+s.I*w*bras[2]*em,
        -s.I*w*kets[3]*ep+s.I*w*bras[3]*em])), simultaneous=True)).coeff(ep).coeff(em)
    M = s.Matrix(4, 4, lambda i, h: s.diff(dc, bras[i], kets[h]))
    aux = M[:2,:2]
    R = ((M[2:,2:]-M[2:,:2]*aux.inv()*M[:2,2:])/2).applyfunc(s.factor)
    kinetic = R.applyfunc(lambda v: s.expand(v).coeff(w,2))
    stiffness = -R.subs(w,0)
    j0 = A/B-1
    determinant = s.factor(stiffness.det().subs(j,j0))

    # Include lapse at its singular point; do not invert D here.
    z = s.symbols('z', real=True)
    descriptor = s.Matrix([[C*z+2*q,0,-2*q],
                           [0,K*z-F*q,E*q],[-2*q,E*q,D*q]])
    full_det = s.factor(descriptor.det())
    qstar = c/(A*beta**2*xi2)
    crossing = s.factor(full_det.subs(j,j0).subs(k**2,qstar))
    jN = s.symbols('jN', positive=True)
    # Static physical potentials independently varied, with normalized matter source.
    rho, Gt = s.symbols('rho G_tilde', real=True)
    equations = M.subs(w,0)*s.Matrix([n,t,P,chi])-s.Matrix([16*s.pi*Gt*rho,0,0,0])
    static = s.solve(list(equations.subs({j:jN,beta:1/(1+jN)})), [n,t,P,chi])
    Gmeas = s.factor(-q*static[n]/(4*s.pi*rho))

    values = {A:s.Rational(9,5), c:s.Rational(1,100000), c2:s.Rational(1,100),
              K:s.Integer(10), xi2:s.Integer(1), beta:s.Rational(1,4)}
    qcrit = s.factor(qstar.subs(values))
    def poles(qvalue):
        poly = s.Poly(full_det.subs(j,j0).subs(values).subs(k**2,qvalue), z)
        roots = s.solve(poly.as_expr(),z)
        assert all(s.simplify(poly.eval(r)) == 0 for r in roots)
        return [float(s.N(r,30)) for r in roots]
    dirac_results = {}
    for name, factor in [('below',s.Rational(1,2)),('crossing',s.S.One),('above',s.Integer(2))]:
        hw = H.subs(j,j0).subs(values).subs(k**2,qcrit*factor)
        dirac_results[name] = dirac(hw,[n,t,P,chi],[pn,pt,pP,pc])
    cross_poly = s.Poly(crossing.subs(values),z)
    homogeneous_L = s.factor(L.subs(k,0))
    checks = {
        'independent_ADM_equals_live_source_modified_action': (M-M_source).applyfunc(s.simplify).is_zero_matrix,
        'kinetic_is_derived_positive_form': (kinetic-s.diag(C,K)).applyfunc(s.simplify).is_zero_matrix,
        'deep_MOND_stiffness_determinant': s.cancel(determinant-2*A*k**4*x*(B-A*beta)**2/(B*D)) == 0,
        'descriptor_matches_full_determinant': s.cancel(M.det().subs(w**2,z)+16*c2*k**4*full_det) == 0,
        'both_potentials_independently_equal': s.simplify(static[P]-static[n]) == 0,
        'Newtonian_scalar_ratio_derived': s.simplify(static[chi]/static[n]-1/(1+jN)) == 0,
        'Newton_constant_scale_independent': s.diff(Gmeas,k) == 0,
        'Newton_constant_not_assigned_bare': s.simplify(Gmeas-2*Gt/(B-A/(1+jN))) == 0,
        'all_Dirac_preservation_closed': all(r['preservation_closed'] for r in dirac_results.values()),
    }
    return {'source':provenance, 'python':platform.python_version(), 'sympy':s.__version__,
            'assumptions':'A=2-KB>0, 0<c14<KB<2, c2,K,xi2>0, beta=1/(1+jN)',
            'checks':checks, 'real_mode_action':str(L), 'Hamiltonian':str(H),
            'full_matrix_basis':['lapse n','shift t','spatial potential P','chi'],
            'full_matrix':strings(M), 'auxiliary_block_determinant':str(s.factor(aux.det())),
            'reduced_kernel':strings(R), 'kinetic_matrix':strings(kinetic),
            'kinetic_eigenvalues':[float(v) for v in kinetic.subs(values).eigenvals()],
            'deep_MOND_stiffness_determinant':str(determinant),
            'full_lapse_descriptor_determinant':str(full_det), 'q_threshold':str(qstar),
            'k_xi_threshold':float(s.sqrt(qcrit)),
            'crossing_frequency_polynomial_degree':cross_poly.degree(),
            'crossing_finite_omega_squared':float(s.solve(cross_poly.as_expr(),z)[0]),
            'below_threshold_omega_squared':poles(qcrit/2),
            'above_threshold_omega_squared':poles(2*qcrit),
            'G_measured':str(Gmeas), 'static_solutions':{str(v):str(e) for v,e in static.items()},
            'dirac':dirac_results,
            'homogeneous':{'action':str(homogeneous_L), 'screen_contribution':str(screen.subs(k,0)),
                           'velocity_Hessian_rank':s.hessian(homogeneous_L,[vP,vc]).rank(),
                           'nonlinear_count_claimed':False,
                           'caveat':'Homogeneous shift parametrization vanishes. Global nonlinear lapse constraint is not captured by this quadratic Minkowski action; no FLRW or homogeneous physical-mode claim.'},
            'nonclaims':['nonlinear Dirac closure','full relativistic theory','empirical prediction',
                         'finite-xi exact AQUAL','PPN beta or preferred-frame parameters','novelty'],
            'runtime_seconds':round(time.monotonic()-started,3)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--require-stable',action='store_true')
    args = parser.parse_args()
    result = derive()
    serialized = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(serialized)
    for i,(name,ok) in enumerate(result['checks'].items(),1):
        print('[{}] {} {}'.format('ok' if ok else 'FAIL',i,name))
    print('k* xi:',result['k_xi_threshold'])
    print('omega^2 above k*:',result['above_threshold_omega_squared'])
    print('quadratic scalar counts:',{k:v['quadratic_scalar_modes'] for k,v in result['dirac'].items()})
    unstable = min(result['above_threshold_omega_squared']) < 0
    print('Selective screen:', 'FALSIFIED on tested branch' if unstable else 'OPEN')
    raise SystemExit(1 if not all(result['checks'].values()) else 2 if args.require_stable and unstable else 0)
