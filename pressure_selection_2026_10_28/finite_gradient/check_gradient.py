#!/usr/bin/env python3
"""Bounded static finite-gradient experiment; contract.json states its scope."""
import json
import math
import sys
import traceback
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_bvp, solve_ivp
from scipy.optimize import brentq


def local_density(psi):
    p = np.maximum(psi, 0.0)
    return p**1.5 / (1.0 - p**2.5)


def local_solution(pc):
    nc = float(local_density(pc))
    start = 1e-7

    def rhs(r, y):
        return [-y[1] / r**2, r**2 * float(local_density(y[0]))]

    def edge(r, y):
        return y[0]

    edge.terminal = True
    edge.direction = -1
    out = solve_ivp(rhs, (start, 30), [pc - nc * start**2 / 6, nc * start**3 / 3],
                    events=edge, rtol=2e-10, atol=2e-12, max_step=.025,
                    dense_output=True)
    if not out.success or len(out.t_events[0]) != 1:
        raise RuntimeError('auxiliary solution did not find one finite edge')
    radius = float(out.t_events[0][0])
    mass = float(out.y_events[0][0, 1])
    rq = brentq(lambda r: float(local_density(out.sol(r)[0])) - nc / 4,
                start, radius)

    def evaluate(r):
        rr = np.asarray(r)
        safe = np.maximum(rr, start)
        yi = out.sol(np.minimum(safe, radius))
        psi = np.where(rr <= radius, yi[0], -mass / radius + mass / safe)
        der = -yi[1] / safe**2
        der = np.where(rr <= radius, der, -mass / safe**2)
        psi = np.where(rr < start, pc - nc * rr**2 / 6, psi)
        der = np.where(rr < start, -nc * rr / 3, der)
        pp = np.maximum(psi, 0.)
        ss = -np.log1p(-pp**2.5) / 3
        sp = (5. / 6) * pp**1.5 / (1 - pp**2.5) * der
        return np.array([psi, der, ss, sp])

    return {'psi_c': pc, 'density_c': nc, 'radius': radius, 'mass': mass,
            'quarter_radius': rq, 'column': math.sqrt(2.5) * nc * rq,
            's_c': -math.log1p(-pc**2.5) / 3,
            'laplacian_s_c': -(5. / 6) * nc**2}, evaluate


def solve_case(pc, eps, local, guess, refine=False):
    lam = math.sqrt(eps / 3)
    outer = max(local['radius'] + 12 * lam, 1.15 * local['radius'])
    if refine:
        outer += max(6 * lam, .25 * local['radius'])
    tol = 2e-7 if refine else 1e-6
    grid = np.unique(np.concatenate(([0.], np.geomspace(1e-6, outer, 350),
                                     np.linspace(0., min(.5, outer), 200),
                                     np.linspace(0., outer, 450))))
    singular = np.diag([0., -2., 0., -2.])

    def rhs(r, y):
        pp = np.maximum(y[0], 0.)
        ey = np.exp(3 * y[2])
        return np.array([y[1], -pp**1.5 * ey, y[3],
                         (ey * (1 - pp**2.5) - 1) / eps])

    def jac(r, y):
        pp = np.maximum(y[0], 0.)
        ey = np.exp(3 * y[2])
        ans = np.zeros((4, 4, r.size))
        ans[0, 1] = 1
        ans[1, 0] = -1.5 * np.sqrt(pp) * ey
        ans[1, 2] = -3 * pp**1.5 * ey
        ans[2, 3] = 1
        ans[3, 0] = -2.5 * pp**1.5 * ey / eps
        ans[3, 2] = 3 * ey * (1 - pp**2.5) / eps
        return ans

    tail = 1 / lam + 1 / outer

    def bc(a, b):
        return np.array([a[0] - pc, a[1], a[3], b[3] + tail * b[2]])

    sol = solve_bvp(rhs, bc, grid, guess(grid), S=singular, fun_jac=jac,
                    tol=tol, max_nodes=20000)
    record = {'psi_c': pc, 'epsilon': eps, 'refinement': refine,
              'solver_status': int(sol.status), 'solver_message': sol.message,
              'iterations': int(sol.niter), 'nodes': int(sol.x.size),
              'tolerance': tol, 'outer_radius': outer,
              'maximum_rms_residual': float(np.max(sol.rms_residuals)),
              'bc_max_residual': float(np.max(np.abs(bc(sol.y[:, 0], sol.y[:, -1]))))}
    if not sol.success:
        record['passed'] = False
        return record, sol

    def state(r):
        psi, der, ss, sp = sol.sol(r)
        pp = np.maximum(psi, 0.)
        ey = np.exp(3 * ss)
        density = pp**1.5 * ey
        aa = pp**2.5 * ey
        uu = np.expm1(3 * ss) - 3 * ss
        return psi, der, ss, sp, density, aa, uu

    if sol.sol(outer)[0] >= 0:
        raise RuntimeError('matter edge was not enclosed by outer boundary')
    radius = brentq(lambda r: float(sol.sol(r)[0]), 0, outer, xtol=1e-13)
    sc = float(sol.sol(0)[2])
    nc = pc**1.5 * math.exp(3 * sc)
    rq = brentq(lambda r: float(state(r)[4]) - nc / 4, 0, radius, xtol=1e-13)
    mass_slope = -radius**2 * float(sol.sol(radius)[1])

    def integrate(fn, upper=outer):
        points = [radius] if upper > radius else None
        return quad(fn, 0, upper, epsabs=2e-9, epsrel=2e-9,
                    points=points, limit=600)[0]

    mass_quad = integrate(lambda r: r**2 * float(state(r)[4]), radius)
    column = math.sqrt(2.5) * nc * rq
    source = lambda r: math.exp(3 * float(sol.sol(r)[2])) * (
        1 - max(float(sol.sol(r)[0]), 0.)**2.5) - 1
    source_integral = integrate(lambda r: r**2 * source(r))
    source_abs_integral = integrate(lambda r: r**2 * abs(source(r)))
    scalar_boundary = eps * outer**2 * float(sol.sol(outer)[3])
    scalar_error = abs(source_integral - scalar_boundary) / (1 + source_abs_integral)

    def stress(r):
        psi, der, ss, sp, nn, aa, uu = state(r)
        return np.array([aa - uu + 1.5 * eps * sp**2,
                         aa - uu - 1.5 * eps * sp**2])

    # Differentiate the actual total stresses, not the RHS used by the solver.
    rr = np.unique(np.concatenate((np.geomspace(1e-4, .95 * radius, 220),
                                   np.linspace(.05 * radius, .99 * outer, 250))))
    hh = 2e-5 * np.maximum(.01, rr)
    radial_derivative = (-stress(rr + 2 * hh)[0] + 8 * stress(rr + hh)[0]
                         - 8 * stress(rr - hh)[0] + stress(rr - 2 * hh)[0]) / (12 * hh)
    prs = stress(rr)
    force_left = radial_derivative + 2 * (prs[0] - prs[1]) / rr
    sampled = state(rr)
    force_right = 2.5 * sampled[4] * sampled[1]
    force_error = float(np.max(np.abs(force_left - force_right)) /
                        max(1., np.max(np.abs(force_right))))

    erel = integrate(lambda r: 1.5 * r**2 * float(state(r)[5]))
    scalar_potential = integrate(lambda r: r**2 * float(state(r)[6]))
    scalar_gradient = integrate(lambda r: 1.5 * eps * r**2 * float(sol.sol(r)[3])**2)
    grav = integrate(lambda r: 2.5 * r**3 * float(sol.sol(r)[1]) * float(state(r)[4]), radius)
    boundary_stress = outer**3 * float(stress(outer)[0])
    virial_sum = 2 * erel - 3 * scalar_potential - scalar_gradient + grav - boundary_stress
    virial_scale = 2 * erel + 3 * scalar_potential + scalar_gradient + abs(grav)
    virial_error = abs(virial_sum) / virial_scale
    mu_scaled = float(sol.sol(outer)[0]) - mass_slope / outer
    grav_from_potential = integrate(lambda r: 1.25 * r**2 * float(state(r)[4]) *
                                   (mu_scaled - float(sol.sol(r)[0])), radius)
    gravity_error = abs(grav_from_potential / grav - 1)
    sample = state(np.linspace(0, outer, 1500))
    scalar_c_lap = 3 * float(sol.sol(0, 2)[2])
    scalar_c_target = (math.exp(3 * sc) * (1 - pc**2.5) - 1) / eps
    checks = {
        'finite_positive_halo': radius > 0 and radius < outer and mass_slope > 0 and nc > 0,
        'positive_monotone_scalar': float(np.min(sample[2])) > -1e-10 and float(np.max(sample[3])) < 1e-8,
        'monotone_gravity': float(np.max(sample[1])) < 1e-10,
        'regular_boundary_residual': record['bc_max_residual'] < 1e-8,
        'small_outer_scalar': abs(float(sol.sol(outer)[2])) < 1e-6,
        'mass_integral': abs(mass_quad / mass_slope - 1) < 2e-5,
        'scalar_integral': scalar_error < 2e-5,
        'radial_force_balance': force_error < 5e-4,
        'virial_identity': virial_error < 2e-5,
        'gravitational_energy_identity': gravity_error < 2e-5,
    }
    record.update({
        'checks': {k: bool(v) for k, v in checks.items()},
        'passed': bool(all(checks.values())), 'radius': radius,
        'mass_dimensionless': mass_slope, 'density_c': nc, 's_c': sc,
        'quarter_radius': rq, 'core_column_coefficient': column,
        'local_core_column_coefficient': local['column'],
        'column_fractional_departure_from_local': column / local['column'] - 1,
        'central_density_fractional_departure_from_local': nc / local['density_c'] - 1,
        'central_scalar_departure_from_local': sc - local['s_c'],
        'local_scalar_dimensionless_residual_at_center': -eps * local['laplacian_s_c'],
        's_outer': float(sol.sol(outer)[2]), 's_at_matter_edge': float(sol.sol(radius)[2]),
        'mu_over_enthalpy_scale': mu_scaled,
        'mass_quadrature_relative_error': abs(mass_quad / mass_slope - 1),
        'scalar_integrated_error': scalar_error, 'radial_force_scaled_error': force_error,
        'virial_scaled_error': virial_error, 'gravity_energy_relative_error': gravity_error,
        'scalar_center_laplacian': scalar_c_lap,
        'scalar_center_laplacian_from_equation': scalar_c_target,
        'energies_over_4pi_B_ell_cubed': {'relative': erel, 'scalar_excess_potential': scalar_potential,
                                         'scalar_gradient': scalar_gradient, 'gravity': grav},
    })
    return record, sol


def main():
    output = Path(sys.argv[1])
    rows, auxiliary, solutions, profiles = [], {}, {}, {}
    for pc in (.8, .95, .99):
        local, guess = local_solution(pc)
        auxiliary[str(pc)] = local
        for eps in (1e-4, 1e-2):
            try:
                row, sol = solve_case(pc, eps, local, guess)
                solutions[(pc, eps)] = sol
                r = np.linspace(0, row['outer_radius'], 1600)
                profiles[f'p{pc}_e{eps}'] = np.vstack((r, sol.sol(r)))
            except Exception as exc:
                row = {'psi_c': pc, 'epsilon': eps, 'passed': False,
                       'exception': repr(exc), 'traceback': traceback.format_exc()}
            rows.append(row)
            print(json.dumps({k: row.get(k) for k in ('psi_c', 'epsilon', 'solver_status', 'passed',
                              'density_c', 'core_column_coefficient', 'column_fractional_departure_from_local')}), flush=True)
    refinements = []
    for eps in (1e-4, 1e-2):
        pc = .99
        local, guess = local_solution(pc)
        try:
            fine, _ = solve_case(pc, eps, local, guess, refine=True)
            baseline = next(r for r in rows if r['psi_c'] == pc and r['epsilon'] == eps)
            keys = ('radius', 'mass_dimensionless', 'density_c', 'core_column_coefficient')
            fine['relative_changes_from_baseline'] = {
                k: abs(fine[k] / baseline[k] - 1) for k in keys}
            fine['domain_and_tolerance_check'] = max(fine['relative_changes_from_baseline'].values()) < 5e-5
        except Exception as exc:
            fine = {'psi_c': pc, 'epsilon': eps, 'passed': False,
                    'domain_and_tolerance_check': False, 'exception': repr(exc),
                    'traceback': traceback.format_exc()}
        refinements.append(fine)
    checks = {'six_requested_cases': len(rows) == 6,
              'all_six_finite_case_checks': all(r.get('passed', False) for r in rows),
              'both_refined_case_checks': all(r.get('passed', False) for r in refinements),
              'both_domain_and_tolerance_checks': all(r.get('domain_and_tolerance_check', False) for r in refinements)}
    result = {'claim_id': 'PN28_GRAD', 'checks': checks, 'auxiliary_references': auxiliary,
              'cases': rows, 'refinements': refinements,
              'scope': 'Conditional static pi_s=u=0 vacuum continuation; finite cases, not general existence or dynamical stability.'}
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    np.savez_compressed(output.with_name('profiles.npz'), **profiles)
    print(json.dumps(checks, sort_keys=True), flush=True)
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
