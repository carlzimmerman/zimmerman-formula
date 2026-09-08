"""Localize Delta S_b; check its EL equations and only its auxiliary constraints.

Conventions: L=-Delta_h, n=log N, a_i=D_i n, c=b*tau_T/24,
I=R-4 Delta_h n-2|Dn|^2, Y=m U exp(n/2)/8+W.  The local action is

 int sqrt(h) [m|DU|^2/16 + DW.DV - c V^2 - Y I].

In particular the -W I term is essential.  Varying W, U, V gives
LV=I, LU=sqrt(N)I, LW=2cV. On these equations integration by parts gives
-m<sqrt(N)I,L^-1 sqrt(N)I>/16-c<L^-1 I,L^-1 I>, the actual Delta S_b.

This is a conditional localization on a specified spatial inverse domain:
all displayed pairings must exist and surface terms must vanish.  On R^3,
V^2 requires sufficient falloff (a compact source with nonzero monopole
fails). Zero monopole alone does not guarantee every auxiliary boundary
condition: L^-2 of a dipole need not decay. No open nonlinear finite-action
neighborhood is proved. The compact zero-mean spectral inverse additionally
requires mean constraints/global multipliers and their metric variations;
the unprojected EL equations below do NOT implement those global terms.

The tensor EL formula is checked by actual Christoffel variations for all
six symmetric metric directions on h=exp(2 zeta(x)) delta, with arbitrary
three-coordinate lapse and auxiliary fields. This bounded exact check and
the nonzero-eigenmode auxiliary count are not a full nonlinear gravity count.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path

import sympy as s


def _el(density, field, coordinates):
    """Euler derivative for jets through order two, counting mixed jets once."""
    result = s.diff(density, field)
    for coordinate in coordinates:
        result -= s.diff(s.diff(density, s.diff(field, coordinate)), coordinate)
    for i, first in enumerate(coordinates):
        for second in coordinates[i:]:
            result += s.diff(s.diff(density, s.diff(field, first, second)), first, second)
    return s.simplify(result)


def _pb(first, second, coordinates, momenta):
    return s.expand(sum(s.diff(first, q)*s.diff(second, p)
        - s.diff(first, p)*s.diff(second, q) for q, p in zip(coordinates, momenta)))


@lru_cache(None)
def derive_localization_mode():
    m, c, ell = s.symbols("m c eigenvalue", positive=True)
    U, V, W, source_u, source_v = s.symbols("U V W source_u source_v", real=True)
    fields = [U, V, W]
    action = m*ell*U**2/16 + ell*W*V - c*V**2 - m*U*source_u/8 - W*source_v
    equations = [s.diff(action, field) for field in fields]
    solution = s.solve(equations, fields, dict=True)[0]
    expected = [m*(ell*U-source_u)/8, ell*W-2*c*V, ell*V-source_v]
    on_shell = s.factor(action.subs(solution))
    return dict(m=m, c=c, eigenvalue=ell, U=U, V=V, W=W,
        source_u=source_u, source_v=source_v, fields=fields, action=action,
        equations=equations, solution=solution, on_shell_action=on_shell,
        auxiliary_equation_residuals=[s.simplify(a-b) for a, b in zip(equations, expected)],
        elimination_residual=s.factor(on_shell+m*source_u**2/(16*ell)+c*source_v**2/ell**2))


def _ricci(connection, coordinates):
    return s.Matrix(3, 3, lambda i, j: s.simplify(sum(
        s.diff(connection[k][i][j], coordinates[k])
        - s.diff(connection[k][i][k], coordinates[j])
        + sum(connection[k][k][ell]*connection[ell][i][j]
            - connection[k][j][ell]*connection[ell][i][k] for ell in range(3))
        for k in range(3))))


@lru_cache(None)
def derive_curved_variation():
    coordinates = s.symbols("x y z", real=True)
    x = coordinates[0]
    zeta = s.Function("zeta")(x)
    n, U, V, W = [s.Function(name)(*coordinates) for name in ("n", "U", "V", "W")]
    m, c = s.symbols("m c", positive=True)
    h, inverse = s.eye(3)*s.exp(2*zeta), s.eye(3)*s.exp(-2*zeta)
    volume = s.exp(3*zeta)
    connection = [[[s.simplify(sum(inverse[k, ell]*(
        s.diff(h[ell, j], coordinates[i])+s.diff(h[ell, i], coordinates[j])
        - s.diff(h[i, j], coordinates[ell]))/2 for ell in range(3)))
        for j in range(3)] for i in range(3)] for k in range(3)]
    ricci = _ricci(connection, coordinates)
    curvature = s.simplify(s.trace(inverse*ricci))
    gradient = lambda f: s.Matrix([s.diff(f, coordinate) for coordinate in coordinates])
    dot = lambda f, g: (gradient(f).T*inverse*gradient(g))[0]
    hessian = lambda f: s.Matrix(3, 3, lambda i, j: s.diff(f, coordinates[i], coordinates[j])
        - sum(connection[k][i][j]*s.diff(f, coordinates[k]) for k in range(3)))
    laplacian = lambda f: s.trace(inverse*hessian(f))
    I = curvature-4*laplacian(n)-2*dot(n, n)
    Y = m*U*s.exp(n/2)/8+W
    raw = m*dot(U, U)/16+dot(W, V)-c*V**2-Y*I
    integrated = m*dot(U, U)/16+dot(W, V)-c*V**2-Y*curvature-4*dot(Y, n)+2*Y*dot(n, n)
    divergence = sum(s.diff(volume*Y*(inverse*gradient(n))[i], coordinates[i]) for i in range(3))
    ibp_residual = s.simplify(volume*(raw-integrated)-4*divergence)
    actual_scalar = {name: s.simplify(_el(volume*raw, field, coordinates)/volume)
                    for name, field in (("U", U), ("V", V), ("W", W), ("log_lapse", n))}
    expected_scalar = {
        "U": m*(-laplacian(U)-s.exp(n/2)*I)/8,
        "V": -laplacian(W)-2*c*V,
        "W": -laplacian(V)-I,
        "log_lapse": -m*U*s.exp(n/2)*I/16+4*laplacian(Y)
            -4*(dot(Y, n)+Y*laplacian(n)),
    }
    scalar_residuals = [s.simplify(actual_scalar[name]-expected_scalar[name]) for name in actual_scalar]

    # E_ij=(sqrt h)^-1 delta S_aux/delta h^ij, at fixed n,U,V,W.
    first_derivative_part = integrated+Y*curvature
    metric_el = s.Matrix(3, 3, lambda i, j:
        m*s.diff(U, coordinates[i])*s.diff(U, coordinates[j])/16
        +(s.diff(W, coordinates[i])*s.diff(V, coordinates[j])
          +s.diff(W, coordinates[j])*s.diff(V, coordinates[i]))/2
        -2*(s.diff(Y, coordinates[i])*s.diff(n, coordinates[j])
            +s.diff(Y, coordinates[j])*s.diff(n, coordinates[i]))
        +2*Y*s.diff(n, coordinates[i])*s.diff(n, coordinates[j])
        -h[i, j]*first_derivative_part/2
        -Y*(ricci[i, j]-h[i, j]*curvature/2)
        +hessian(Y)[i, j]-h[i, j]*laplacian(Y))

    # Independent route: differentiate the actual Christoffels for six
    # arbitrary inverse-metric variations M^ij psi(x,y,z); do not insert
    # the known variation of sqrt(h)R or infer shear from a trace test.
    psi = s.Function("metric_variation")(*coordinates)
    metric_residuals = []
    direct_metric_variations = []
    for row in range(3):
        for column in range(row, 3):
            direction = s.zeros(3)
            direction[row, column] = direction[column, row] = 1
            delta_inverse = direction*psi
            delta_h = -h*delta_inverse*h
            delta_connection = [[[s.simplify(sum(
                delta_inverse[k, ell]*(s.diff(h[ell, j], coordinates[i])
                    +s.diff(h[ell, i], coordinates[j])-s.diff(h[i, j], coordinates[ell]))/2
                +inverse[k, ell]*(s.diff(delta_h[ell, j], coordinates[i])
                    +s.diff(delta_h[ell, i], coordinates[j])
                    -s.diff(delta_h[i, j], coordinates[ell]))/2 for ell in range(3)))
                for j in range(3)] for i in range(3)] for k in range(3)]
            delta_ricci = s.Matrix(3, 3, lambda i, j: s.simplify(sum(
                s.diff(delta_connection[k][i][j], coordinates[k])
                -s.diff(delta_connection[k][i][k], coordinates[j])
                +sum(delta_connection[k][k][ell]*connection[ell][i][j]
                    +connection[k][k][ell]*delta_connection[ell][i][j]
                    -delta_connection[k][j][ell]*connection[ell][i][k]
                    -connection[k][j][ell]*delta_connection[ell][i][k]
                    for ell in range(3)) for k in range(3))))
            delta_curvature = s.trace(delta_inverse*ricci+inverse*delta_ricci)
            delta_lap_n = s.trace(delta_inverse*hessian(n))-sum(
                inverse[i, j]*delta_connection[k][i][j]*s.diff(n, coordinates[k])
                for i in range(3) for j in range(3) for k in range(3))
            delta_dot = lambda f, g: (gradient(f).T*delta_inverse*gradient(g))[0]
            delta_I = delta_curvature-4*delta_lap_n-2*delta_dot(n, n)
            delta_density = volume*(m*delta_dot(U, U)/16+delta_dot(W, V)-Y*delta_I
                                     -raw*s.trace(h*delta_inverse)/2)
            direct = s.simplify(_el(s.expand(delta_density), psi, coordinates)/volume)
            expected = sum(metric_el[i, j]*direction[i, j] for i in range(3) for j in range(3))
            direct_metric_variations.append(direct)
            metric_residuals.append(s.simplify(direct-expected))
    return dict(coordinates=coordinates, zeta=zeta, n=n, U=U, V=V, W=W, m=m, c=c,
        metric=h, ricci_scalar=curvature, I=I, Y=Y, raw_action_density=volume*raw,
        integrated_action_density=volume*integrated,
        integration_by_parts_residual=ibp_residual, scalar_el=actual_scalar,
        scalar_el_residuals=scalar_residuals, metric_el=metric_el,
        direct_metric_variations=direct_metric_variations, metric_variation_residuals=metric_residuals)


@lru_cache(None)
def derive_auxiliary_constraints():
    d = derive_localization_mode()
    fields = d["fields"]
    velocities = s.symbols("U_dot V_dot W_dot")
    momenta = list(s.symbols("p_U p_V p_W"))
    velocity_momenta = [s.diff(d["action"], velocity) for velocity in velocities]
    primary = [p-derivative for p, derivative in zip(momenta, velocity_momenta)]
    hamiltonian = -d["action"]
    secondary = [_pb(constraint, hamiltonian, fields, momenta) for constraint in primary]
    constraints = primary+secondary
    matrix = s.Matrix([[_pb(first, second, fields, momenta) for second in constraints]
                       for first in constraints])
    rank = matrix.rank()
    ell_dot, c_dot, source_u_dot, source_v_dot = s.symbols(
        "eigenvalue_dot c_dot source_u_dot source_v_dot", real=True)
    parameters = [d["eigenvalue"], d["c"], d["source_u"], d["source_v"]]
    parameter_velocities = [ell_dot, c_dot, source_u_dot, source_v_dot]
    explicit_derivative = lambda f: sum(s.diff(f, parameter)*velocity
        for parameter, velocity in zip(parameters, parameter_velocities))
    drift = s.Matrix([explicit_derivative(constraint)
        +_pb(constraint, hamiltonian, fields, momenta) for constraint in secondary])
    multiplier_matrix = s.Matrix([[_pb(first, second, fields, momenta) for second in primary]
                                  for first in secondary])
    multipliers = (-multiplier_matrix.inv()*drift).applyfunc(s.factor)
    preservation = (multiplier_matrix*multipliers+drift).applyfunc(s.simplify)
    solution_drift = [s.simplify(multipliers[index].subs(d["solution"])
        -explicit_derivative(d["solution"][field])) for index, field in enumerate(fields)]
    zero_matrix = matrix.subs(d["eigenvalue"], 0)
    return dict(m=d["m"], eigenvalue=d["eigenvalue"], velocity_momenta=velocity_momenta,
        hamiltonian=hamiltonian, primary_constraints=primary, secondary_constraints=secondary,
        poisson_matrix=matrix, poisson_rank=rank, first_class=len(constraints)-rank,
        auxiliary_pairs=s.Rational(2*len(fields)-2*(len(constraints)-rank)-rank, 2),
        multiplier_matrix=multiplier_matrix, multipliers=list(multipliers),
        preservation_residuals=list(preservation), solution_drift_residuals=solution_drift,
        zero_mode=dict(secondary_constraints=[constraint.subs(d["eigenvalue"], 0) for constraint in secondary],
            poisson_rank=zero_matrix.rank(), auxiliary_pairs_claimed=None))


def _encode(value):
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, s.MatrixBase):
        return _encode(value.tolist())
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    if isinstance(value, s.Integer):
        return int(value)
    if isinstance(value, s.Basic):
        return str(value)
    return value


def run():
    mode, geometry, constraints = derive_localization_mode(), derive_curved_variation(), derive_auxiliary_constraints()
    residuals = mode["auxiliary_equation_residuals"]+[mode["elimination_residual"]]
    residuals += geometry["scalar_el_residuals"]+geometry["metric_variation_residuals"]
    residuals += [geometry["integration_by_parts_residual"]]
    residuals += constraints["preservation_residuals"]+constraints["solution_drift_residuals"]
    checked = all(s.simplify(value) == 0 for value in residuals)
    closed = checked and constraints["poisson_rank"] == len(constraints["primary_constraints"]+constraints["secondary_constraints"])
    return _encode(dict(checks_passed=checked, nonzero_mode_auxiliary_closure=closed,
        sympy_version=s.__version__, coefficient_convention="m>0; c=b*tau_T/24>0; eigenvalue>0",
        local_action="int sqrt(h) [m|DU|^2/16 + DW.DV - c V^2 - (m U sqrt(N)/8+W) I]",
        Y="m U sqrt(N)/8+W", I="R-4 Delta_h log(N)-2|D log(N)|^2",
        auxiliary_EL={"U": "m/8 (L U-sqrt(N) I)", "V": "L W-2c V", "W": "L V-I"},
        lapse_EL="(sqrt(h))^-1 delta S/delta log(N) = -m U sqrt(N) I/16 +4 Delta_h Y-4 D_i(Y a^i)",
        metric_EL="E_ij=m U_i U_j/16+W_(i V_j)-4 Y_(i a_j)+2Y a_i a_j-h_ij A/2-Y G_ij+D_iD_jY-h_ij Delta_hY; A=m|DU|^2/16+DW.DV-cV^2-4DY.a+2Y a^2",
        metric_variation_convention="E_ij=(sqrt(h))^-1 delta S_aux/delta h^ij, fixing n,U,V,W; parentheses symmetrize with weight 1/2",
        geometry_checked="h_ij=exp(2 zeta(x)) delta_ij; arbitrary n,U,V,W(x,y,z); all six arbitrary symmetric inverse-metric directions",
        curved_R=geometry["ricci_scalar"], scalar_EL_residuals=geometry["scalar_el_residuals"],
        metric_EL_residuals=geometry["metric_variation_residuals"],
        integration_by_parts_residual=geometry["integration_by_parts_residual"],
        mode_on_shell_action=mode["on_shell_action"], auxiliary_constraints=constraints,
        auxiliary_pairs=constraints["auxiliary_pairs"], full_nonlinear_gravity_count_claimed=None,
        compact_projector_metric_variation_completed=False,
        generic_R3_finite_action_neighborhood_proved=False,
        boundary_scope="Unprojected decay/IBP domain only: inverse prescription, finite pairings and vanishing surface terms required. Compact mean multipliers and metric-dependent projector variations are not included.",
        infrared_scope="For sufficiently localized I, nonzero integral sqrt(h) I produces a V~1/r monopole and divergent integral sqrt(h) V^2. Zero monopole is necessary in this class, not a proved complete nonlinear domain. W=2c L^-2 I need not decay even for dipole I.",
        constraint_scope="Computed auxiliary-only nonzero eigenmode count, with arbitrary time-dependent source/eigenvalue data. In the coupled theory its multiplier equations depend on metric/lapse evolution; the full lapse-conformal functional rank remains unproved."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-auxiliary-closure", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    if args.output:
        with args.output.open("x") as stream:
            json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write("\n")
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    if not result["checks_passed"]:
        return 1
    return 2 if args.require_auxiliary_closure and not result["nonzero_mode_auxiliary_closure"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
