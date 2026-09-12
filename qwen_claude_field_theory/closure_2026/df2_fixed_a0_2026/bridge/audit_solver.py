"""Independent bounded action-energy, EFD, normalization and spherical checks.

Import-safe. Writes JSON only to stdout; the parent run manifest archives it.
These checks concern a conditional nonrelativistic PDE, not observations.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
import scipy


def load_solver():
    path = Path(__file__).resolve().parents[1] / "solver.py"
    spec = importlib.util.spec_from_file_location("independent_df2_solver_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def energy_check(m):
    mesh = m.Mesh(7, 13, 8.)
    R, Z = mesh.nodes.T
    phi = -.06 / np.sqrt(1 + R*R + Z*Z)
    direction = np.sin(.7*R + .2*Z)
    direction[mesh.fixed] = 0.
    residual, H, _, _ = m.assemble(mesh, phi, .06, external=.15)

    def exact_discrete_energy(values):
        internal = np.einsum('eqac,ea->eqc', mesh.grad, values[mesh.ids])
        total = internal + np.array([0., -.15])
        y = np.sqrt(np.sum(total*total, axis=-1))
        rho = 3/(4*np.pi)*(1 + np.sum(mesh.points**2, axis=-1))**(-2.5)
        potential = np.einsum('qa,ea->eq', mesh.shape, values[mesh.ids])
        background_flux = np.array([0., -.15*(1-math.exp(-.15))])
        # Explicit exponential primitive, independently of solver.primitive.
        integrand = (y*y/2 + (1+y)*np.exp(-y) - 1
                     - np.sum(background_flux*internal, axis=-1)
                     + 4*np.pi*.06*rho*potential)
        return float(np.sum(mesh.weight*integrand))

    rows = []
    for step in (3e-4, 1e-4):
        first = (exact_discrete_energy(phi+step*direction)
                 - exact_discrete_energy(phi-step*direction))/(2*step)
        second = (exact_discrete_energy(phi+step*direction)
                  - 2*exact_discrete_energy(phi)
                  + exact_discrete_energy(phi-step*direction))/(step*step)
        rows.append(dict(step=step, gradient_relative_error=first/(residual@direction)-1,
                         hessian_relative_error=second/(direction@(H@direction))-1))
    step = 1e-6
    finite = (m.assemble(mesh, phi+step*direction, .06, hessian=False, external=.15)[0]
              - m.assemble(mesh, phi-step*direction, .06, hessian=False, external=.15)[0])/(2*step)
    exact = H@direction
    jacobian_error = float(np.linalg.norm((finite-exact)[mesh.free]) /
                           np.linalg.norm(exact[mesh.free]))
    skew = H-H.T
    symmetry_error = float(np.max(np.abs(skew.data))) if skew.nnz else 0.
    return dict(energy_differences=rows, jacobian_relative_error=jacobian_error,
                symmetry_error=symmetry_error,
                directional_curvature=float(direction@exact))


def run():
    started = time.perf_counter()
    m, path = load_solver()
    energy = energy_check(m)
    eta, external = 1e-5, .5
    mm = 1-math.exp(-external)
    q = 1+external/(math.exp(external)-1)
    k = math.sqrt(q-1)
    newtonian = math.pi*eta/32
    perpendicular = newtonian*3*((1+k*k)*math.atan(k)-k)/(2*mm*k**3)
    parallel = newtonian*3*(k-math.atan(k))/(mm*k**3)
    efd = []
    for nr, nz, extent in ((49, 97, 32), (97, 193, 32), (57, 113, 64)):
        result = m.solve(eta, external, nr=nr, nz=nz, extent=extent)
        result.update(analytic_perpendicular=perpendicular, analytic_parallel=parallel,
                      perpendicular_relative_error=result['virial_perpendicular']/perpendicular-1,
                      parallel_relative_error=result['virial_parallel']/parallel-1)
        efd.append(result)
    spherical = []
    for ext, newton in ((.1, True), (0., False)):
        result = m.solve(.06, ext, nr=49, nz=97, extent=32, newtonian=newton)
        reference = math.pi*.06/32 if newton else m.spherical_virial(.06)
        result.update(reference=reference,
                      perpendicular_relative_error=result['virial_perpendicular']/reference-1,
                      parallel_relative_error=result['virial_parallel']/reference-1)
        spherical.append(result)
    extent = 32.
    cylinder_mass = (extent/math.sqrt(1+extent**2)
                     - extent/((1+extent**2)*math.sqrt(1+2*extent**2)))
    mass_error = efd[0]['quadrature_mass']-cylinder_mass
    final_energy = energy['energy_differences'][-1]
    checks = dict(
        action_gradient=abs(final_energy['gradient_relative_error']) < 2e-6,
        action_hessian=abs(final_energy['hessian_relative_error']) < 1e-6,
        external_jacobian=energy['jacobian_relative_error'] < 1e-7,
        symmetric_positive_test_direction=(energy['symmetry_error'] < 1e-12
                                          and energy['directional_curvature'] > 0),
        cylinder_mass=abs(mass_error) < 2e-9,
        all_pde_solves_converged=all(row['converged'] for row in efd+spherical),
        efd_coarse=all(abs(efd[0][key]) < .003 for key in
                       ('perpendicular_relative_error', 'parallel_relative_error')),
        efd_fine=all(abs(efd[1][key]) < .0007 for key in
                     ('perpendicular_relative_error', 'parallel_relative_error')),
        efd_large_domain=all(abs(efd[2][key]) < .002 for key in
                             ('perpendicular_relative_error', 'parallel_relative_error')),
        spherical_controls=all(abs(row[key]) < .004 for row in spherical for key in
                               ('perpendicular_relative_error', 'parallel_relative_error')),
    )
    checks = {key: bool(value) for key, value in checks.items()}
    return dict(status='PASS_BOUNDED_CONDITIONAL_PDE_AUDIT' if all(checks.values()) else 'FAIL',
                checks=checks, energy=energy, efd=efd, spherical=spherical,
                analytic_cylinder_mass=cylinder_mass, cylinder_mass_error=mass_error,
                source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                runtime_seconds=time.perf_counter()-started,
                scope='Finite numerical checks; no observational PASS, relativistic bridge, '
                      'interval bound, or equilibrium-distribution existence proof.')


if __name__ == '__main__':
    result = run()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'].startswith('PASS_') else 1)
